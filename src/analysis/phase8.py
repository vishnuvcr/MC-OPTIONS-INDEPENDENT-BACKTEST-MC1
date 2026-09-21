from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def _executed(path: Path) -> pd.DataFrame:
    x = pd.read_csv(path)
    if "executed" in x:
        x = x[x["executed"].astype(bool)].copy()
    x["expiry"] = pd.to_datetime(x["expiry"])
    x["signal_date"] = pd.to_datetime(x["signal_date"])
    x["net_realized_rupees"] = pd.to_numeric(x["net_realized_rupees"], errors="coerce")
    return x.dropna(subset=["net_realized_rupees"]).sort_values("expiry").reset_index(drop=True)


def block_bootstrap_mean(x: np.ndarray, block_len: int = 4, reps: int = 20000, seed: int = 20260921) -> tuple[float, float, float]:
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n == 0:
        raise ValueError("empty sample")
    rng = np.random.default_rng(seed)
    starts = np.arange(max(1, n - block_len + 1))
    vals = np.empty(reps, dtype=float)
    need_blocks = int(np.ceil(n / block_len))
    for r in range(reps):
        idx = []
        for _ in range(need_blocks):
            s = int(rng.choice(starts))
            idx.extend(range(s, min(s + block_len, n)))
        vals[r] = x[np.asarray(idx[:n])].mean()
    point = float(x.mean())
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return point, float(lo), float(hi)


def paired_mean_bootstrap(nifty_path: Path, sensex_path: Path, reps: int = 20000, seed: int = 20260921) -> dict:
    n = _executed(nifty_path)[["signal_date","net_realized_rupees"]].rename(columns={"net_realized_rupees":"nifty"})
    s = _executed(sensex_path)[["signal_date","net_realized_rupees"]].rename(columns={"net_realized_rupees":"sensex"})
    z = n.merge(s, on="signal_date", how="inner").sort_values("signal_date")
    if len(z) < 2:
        return {"paired_dates": int(len(z)), "status":"insufficient_common_signal_dates"}
    d = (z["nifty"] - z["sensex"]).to_numpy(float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(d, size=(reps, len(d)), replace=True).mean(axis=1)
    lo, hi = np.quantile(draws, [0.025,0.975])
    return {
        "paired_dates": int(len(d)),
        "mean_difference_nifty_minus_sensex": float(d.mean()),
        "ci95_low": float(lo),
        "ci95_high": float(hi),
        "status":"ok",
    }


def strike_mapping_audit(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    labels=["P20_PE","P35_PE","P65_CE","P80_CE"]
    for _,r in df.iterrows():
        targets=json.loads(r["quantile_targets"])
        strikes=json.loads(r["strikes"])
        grids=json.loads(r["available_strikes_by_type"])
        naive={}
        for label in labels:
            side="PE" if label.endswith("PE") else "CE"
            arr=np.asarray(grids[side],dtype=float)
            naive[label]=float(arr[np.argmin(np.abs(arr-float(targets[label])))])
        collisions=len(naive.values())-len(set(naive.values()))
        disp=json.loads(r["strike_displacement_points"])
        rows.append({
            "expiry":str(r["expiry"].date()),
            "exact_all_four":all(abs(float(disp[k]))<1e-9 for k in labels),
            "exact_leg_share":sum(abs(float(disp[k]))<1e-9 for k in labels)/4.0,
            "mean_abs_displacement":float(np.mean([abs(float(disp[k])) for k in labels])),
            "max_abs_displacement":float(np.max([abs(float(disp[k])) for k in labels])),
            "naive_nearest_collision":int(collisions>0),
            "final_unique_collision":int(len(set(strikes.values()))<4),
        })
    return pd.DataFrame(rows)


def execution_audit(df: pd.DataFrame) -> dict:
    rows=[]
    for _,r in df.iterrows():
        volumes=json.loads(r.get("execution_volume","{}"))
        vals=[v for v in volumes.values() if v is not None and np.isfinite(float(v))]
        rows.append({
            "expiry":str(r["expiry"].date()),
            "all_four_volume_observed":len(vals)==4,
            "all_four_volume_positive":len(vals)==4 and all(float(v)>0 for v in vals),
            "signal_before_or_equal_0930":pd.to_datetime(r["gate_premium_timestamp"]).tz_convert("Asia/Kolkata").time().isoformat() <= "09:30:00" if "+" in str(r["gate_premium_timestamp"]) else str(r["gate_premium_timestamp"])[11:19] <= "09:30:00",
            "execution_after_signal":pd.to_datetime(r["execution_timestamp"]) > pd.to_datetime(r["gate_premium_timestamp"]),
        })
    z=pd.DataFrame(rows)
    return {
        "trades":int(len(z)),
        "gate_timestamp_ok_share":float(z["signal_before_or_equal_0930"].mean()),
        "execution_after_signal_share":float(z["execution_after_signal"].mean()),
        "all_four_volume_observed_share":float(z["all_four_volume_observed"].mean()),
        "all_four_volume_positive_share":float(z["all_four_volume_positive"].mean()),
    }


def payoff_structure() -> dict:
    return {
        "portfolio":"+1 P35 - 2 P20 + 1 C65 - 2 C80",
        "expiry_payoff_at_S0_points":-5.0,
        "upper_tail_slope_points_per_index_point":-1.0,
        "upper_tail_loss":"unbounded as terminal index increases",
        "lower_domain_floor_points_at_S_equals_zero":-5.0,
        "interpretation":"unscaled expiry payoff before entry premiums, slippage, costs and lot size",
    }


def sizing_examples(es95: float, budgets=(50000,100000,250000,500000)) -> pd.DataFrame:
    risk=abs(float(es95))
    rows=[]
    for b in budgets:
        rows.append({"risk_budget_rupees":b,"es95_risk_proxy_per_batman_rupees":risk,"whole_batman_units":int(np.floor(b/risk)) if risk>0 else 0})
    return pd.DataFrame(rows)


def write_index(index: str, path: Path, outdir: Path):
    df=_executed(path)
    outdir.mkdir(parents=True,exist_ok=True)
    if len(df)==0:
        raise ValueError("no executed trades")
    point,lo,hi=block_bootstrap_mean(df["net_realized_rupees"].to_numpy(),block_len=4)
    audit=execution_audit(df)
    sm=strike_mapping_audit(df)
    sm.to_csv(outdir/"strike_mapping_audit.csv",index=False)
    audit["index"]=index
    audit["block_bootstrap_mean"]=point
    audit["block_bootstrap_ci95_low"]=lo
    audit["block_bootstrap_ci95_high"]=hi
    (outdir/"execution_and_uncertainty.json").write_text(json.dumps(audit,indent=2),encoding="utf-8")
    payoff=payoff_structure()
    (outdir/"payoff_structure.json").write_text(json.dumps(payoff,indent=2),encoding="utf-8")
    es95=float(df["net_realized_rupees"][df["net_realized_rupees"]<=df["net_realized_rupees"].quantile(0.05)].mean())
    sizing_examples(es95).to_csv(outdir/"es95_sizing_examples.csv",index=False)
    summary=pd.DataFrame([{
        "index":index,
        "trades":len(df),
        "mean_net":float(df["net_realized_rupees"].mean()),
        "block_bootstrap_ci95_low":lo,
        "block_bootstrap_ci95_high":hi,
        "exact_all_four_share":float(sm["exact_all_four"].mean()),
        "mean_abs_strike_displacement":float(sm["mean_abs_displacement"].mean()),
        "max_abs_strike_displacement":float(sm["max_abs_displacement"].max()),
        "naive_collision_share":float(sm["naive_nearest_collision"].mean()),
        "all_final_unique_share":float(1-sm["final_unique_collision"].mean()),
        "es95":es95,
        "upper_tail_loss_unbounded":True,
    }])
    summary.to_csv(outdir/"phase8_summary.csv",index=False)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--index",choices=["NIFTY","SENSEX"])
    ap.add_argument("--trades")
    ap.add_argument("--output-dir",required=True)
    ap.add_argument("--paired-nifty")
    ap.add_argument("--paired-sensex")
    a=ap.parse_args()
    out=Path(a.output_dir)
    if a.paired_nifty and a.paired_sensex:
        result=paired_mean_bootstrap(Path(a.paired_nifty),Path(a.paired_sensex))
        out.mkdir(parents=True,exist_ok=True)
        (out/"paired_cross_index.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    else:
        write_index(a.index,Path(a.trades),out)
