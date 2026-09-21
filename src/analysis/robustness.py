from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from src.model.costs import entry_costs, entry_slipped_price, expiry_stt


QUANTITIES = {"P35_PE": 1, "P20_PE": -2, "P65_CE": 1, "P80_CE": -2}
OPTION_TYPES = {"P35_PE": "PE", "P20_PE": "PE", "P65_CE": "CE", "P80_CE": "CE"}


def parse_json_col(v):
    if pd.isna(v) or v == "":
        return {}
    return json.loads(v)


def ci_bootstrap(values: np.ndarray, stat: str, seed: int = 20260921, reps: int = 20000) -> tuple[float, float, float]:
    x = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(x, size=(reps, len(x)), replace=True)
    if stat == "mean":
        boot = draws.mean(axis=1)
        point = float(x.mean())
    else:
        boot = np.median(draws, axis=1)
        point = float(np.median(x))
    lo, hi = np.quantile(boot, [0.025, 0.975])
    return point, float(lo), float(hi)


def summarize(df: pd.DataFrame) -> dict:
    x = df[df["executed"] == True].copy()
    if x.empty:
        raise ValueError("no executed trades")
    x["net_realized_rupees"] = pd.to_numeric(x["net_realized_rupees"], errors="coerce")
    x = x.dropna(subset=["net_realized_rupees"]).sort_values("expiry")
    cum = x["net_realized_rupees"].cumsum()
    dd = cum - cum.cummax()
    mean, mean_lo, mean_hi = ci_bootstrap(x["net_realized_rupees"].to_numpy(), "mean")
    med, med_lo, med_hi = ci_bootstrap(x["net_realized_rupees"].to_numpy(), "median")
    return {
        "trades": int(len(x)),
        "start": str(pd.to_datetime(x["expiry"]).min().date()),
        "end": str(pd.to_datetime(x["expiry"]).max().date()),
        "mean_mc_ev_points": float(pd.to_numeric(x["mc_ev_points"]).mean()),
        "median_mc_ev_points": float(pd.to_numeric(x["mc_ev_points"]).median()),
        "mean_net_rupees": mean,
        "mean_net_ci95_low": mean_lo,
        "mean_net_ci95_high": mean_hi,
        "median_net_rupees": med,
        "median_net_ci95_low": med_lo,
        "median_net_ci95_high": med_hi,
        "net_profit_share": float((x["net_realized_rupees"] > 0).mean()),
        "sum_net_rupees": float(x["net_realized_rupees"].sum()),
        "es95_rupees": float(x["net_realized_rupees"][x["net_realized_rupees"] <= x["net_realized_rupees"].quantile(0.05)].mean()),
        "es99_rupees": float(x["net_realized_rupees"][x["net_realized_rupees"] <= x["net_realized_rupees"].quantile(0.01)].mean()),
        "max_drawdown_rupees": float(dd.min()),
    }


def recompute_net(row: pd.Series, slippage_points: float, extra_per_order: float = 0.0) -> float:
    strikes = parse_json_col(row["strikes"])
    raw = parse_json_col(row["execution_prices_raw"])
    settle = float(row["settlement_spot"])
    lot = int(row["lot_size"])
    slipped = {
        k: entry_slipped_price(float(raw[k]), QUANTITIES[k], slippage_points)
        for k in QUANTITIES
    }
    gross_pts = 0.0
    net_pts = 0.0
    for label, q in QUANTITIES.items():
        k = float(strikes[label])
        intrinsic = max(k - settle, 0.0) if OPTION_TYPES[label] == "PE" else max(settle - k, 0.0)
        gross_pts += q * (intrinsic - float(raw[label]))
        net_pts += q * (intrinsic - slipped[label])
    trade_date = pd.to_datetime(row["execution_timestamp"]).tz_localize(None) if pd.to_datetime(row["execution_timestamp"]).tzinfo else pd.to_datetime(row["execution_timestamp"])
    c = entry_costs(slipped, QUANTITIES, lot, trade_date)
    c["stt_expiry"] = expiry_stt(pd.to_datetime(row["expiry"]), settle, strikes, QUANTITIES, lot)
    return float(net_pts * lot - c["brokerage"] - c["stt_entry"] - c["stt_expiry"] - 4.0 * extra_per_order)


def slippage_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for s in (0.0, 1.0, 2.0, 3.0, 5.0):
        vals = df.apply(lambda r: recompute_net(r, s), axis=1)
        rows.append({
            "slippage_points_per_leg": s,
            "trades": len(vals),
            "mean_net_rupees": float(vals.mean()),
            "median_net_rupees": float(vals.median()),
            "profit_share": float((vals > 0).mean()),
            "sum_net_rupees": float(vals.sum()),
            "es95_rupees": float(vals[vals <= vals.quantile(0.05)].mean()),
            "es99_rupees": float(vals[vals <= vals.quantile(0.01)].mean()),
        })
    return pd.DataFrame(rows)


def extra_cost_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for fee in (0.0, 5.0, 10.0, 20.0, 40.0):
        vals = df.apply(lambda r: recompute_net(r, 2.0, extra_per_order=fee), axis=1)
        rows.append({
            "extra_cost_rupees_per_order": fee,
            "mean_net_rupees": float(vals.mean()),
            "profit_share": float((vals > 0).mean()),
            "sum_net_rupees": float(vals.sum()),
        })
    return pd.DataFrame(rows)


def load_context() -> pd.DataFrame:
    tickers = {
        "india_vix": "^INDIAVIX",
        "sp500": "^GSPC",
        "us_vix": "^VIX",
        "usdinr": "INR=X",
        "gold": "GC=F",
        "nifty": "^NSEI",
        "sensex": "^BSESN",
    }
    series = {}
    for name, ticker in tickers.items():
        try:
            d = yf.download(ticker, period="max", interval="1d", auto_adjust=False, progress=False)
            if isinstance(d.columns, pd.MultiIndex):
                d.columns = [c[0] for c in d.columns]
            d = d.reset_index()
            date_col = "date" if "date" in [str(c).lower() for c in d.columns] else "Date"
            if date_col != "date":
                d = d.rename(columns={date_col: "date"})
            d.columns = [str(c).lower() for c in d.columns]
            d["date"] = pd.to_datetime(d["date"], utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize()
            s = d[["date", "close"]].rename(columns={"close": name}).dropna().drop_duplicates("date")
            series[name] = s.set_index("date")
        except Exception:
            continue
    if not series:
        return pd.DataFrame()
    context = pd.concat(series.values(), axis=1, sort=False).sort_index()
    for c in ["sp500","usdinr","gold","nifty","sensex"]:
        if c in context:
            context[c+"_ret"] = context[c].pct_change()
    if "india_vix" in context:
        context["vix_252_pct"] = context["india_vix"].rolling(252, min_periods=60).apply(
            lambda z: float((z.iloc[-1] >= z).mean()), raw=False
        )
    return context


def attach_regimes(df: pd.DataFrame, context: pd.DataFrame) -> pd.DataFrame:
    if context.empty:
        out = df.copy()
        out["india_vix_regime"] = "unavailable"
        return out
    out = df.copy()
    out["signal_date_dt"] = pd.to_datetime(out["signal_date"]).dt.normalize().astype("datetime64[ns]")
    ctx = context.reset_index().rename(columns={"index":"date"})
    ctx["date"] = pd.to_datetime(ctx["date"]).dt.normalize().astype("datetime64[ns]")
    ctx = ctx.sort_values("date")
    out = pd.merge_asof(
        out.sort_values("signal_date_dt"),
        ctx.sort_values("date"),
        left_on="signal_date_dt",
        right_on="date",
        direction="backward",
        allow_exact_matches=False,
    )
    if "vix_252_pct" in out:
        out["india_vix_regime"] = pd.cut(
            out["vix_252_pct"],
            bins=[-np.inf, 1/3, 2/3, np.inf],
            labels=["low","mid","high"],
        ).astype(str)
    else:
        out["india_vix_regime"] = "unavailable"
    out["sp500_prior_sign"] = np.where(out.get("sp500_ret", 0) >= 0, "up", "down")
    out["usdinr_prior_sign"] = np.where(out.get("usdinr_ret", 0) >= 0, "up", "down")
    out["gold_prior_sign"] = np.where(out.get("gold_ret", 0) >= 0, "up", "down")
    return out


def regime_table(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col not in df.columns:
        return pd.DataFrame()
    g = df.groupby(col, dropna=False)["net_realized_rupees"]
    out = g.agg(["count","mean","median","sum"]).reset_index()
    out["profit_share"] = df.groupby(col, dropna=False)["net_realized_rupees"].apply(lambda s: float((s>0).mean())).values
    out = out.rename(columns={"count":"trades","mean":"mean_net_rupees","median":"median_net_rupees","sum":"sum_net_rupees"})
    return out


def scenario_summary(directory: Path) -> pd.DataFrame:
    rows = []
    import re
    for p in sorted(directory.glob("*.csv")):
        if "_errors" in p.name:
            continue
        x = pd.read_csv(p)
        if x.empty:
            continue
        m = re.search(r"_w(\d+)_p(\d+)$", p.stem)
        window = int(m.group(1)) if m else 756
        paths = int(m.group(2)) if m else 5000
        s = summarize(x)
        s.update({"bootstrap_window": window, "mc_paths": paths, "file": p.name})
        rows.append(s)
    return pd.DataFrame(rows)


def write_single(index_name: str, primary_path: Path, scenario_dir: Path, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(primary_path)
    df = df[df["executed"] == True].copy()
    primary = summarize(df)
    (outdir / "primary_summary.json").write_text(json.dumps(primary, indent=2), encoding="utf-8")
    slippage_table(df).to_csv(outdir / "slippage_sensitivity.csv", index=False)
    extra_cost_table(df).to_csv(outdir / "extra_cost_sensitivity.csv", index=False)
    scenario_summary(scenario_dir).to_csv(outdir / "mc_sensitivity.csv", index=False)

    context = load_context()
    enriched = attach_regimes(df, context)
    if not context.empty:
        context.reset_index().to_csv(outdir / "market_context.csv", index=False)
    for c in ["india_vix_regime","sp500_prior_sign","usdinr_prior_sign","gold_prior_sign"]:
        t = regime_table(enriched, c)
        if not t.empty:
            t.to_csv(outdir / f"regime_{c}.csv", index=False)

    report = [f"# Phase 6 Robustness — {index_name}", "", "## Primary", ""]
    for k,v in primary.items():
        report.append(f"- {k}: {v}")
    report += ["", "## Slippage sensitivity", "", slippage_table(df).to_markdown(index=False), "", "## Extra-cost stress", "", extra_cost_table(df).to_markdown(index=False)]
    sc = scenario_summary(scenario_dir)
    report += ["", "## MC calibration sensitivity", "", sc.to_markdown(index=False)]
    report += ["", "## Market-regime context", "", "Context variables are descriptive and use the latest observation strictly before the signal date."]
    for c in ["india_vix_regime","sp500_prior_sign","usdinr_prior_sign","gold_prior_sign"]:
        t = regime_table(enriched, c)
        if not t.empty:
            report += [f"", f"### {c}", "", t.to_markdown(index=False)]
    report_text = chr(10).join(report)
    (outdir / "PHASE6_INDEX_REPORT.md").write_text(report_text, encoding="utf-8")


def compare_indices(nifty_summary: Path, sensex_summary: Path, outdir: Path) -> None:
    n = pd.read_csv(nifty_summary)
    s = pd.read_csv(sensex_summary)
    n = n[n["executed"] == True]["net_realized_rupees"].dropna().to_numpy(dtype=float)
    s = s[s["executed"] == True]["net_realized_rupees"].dropna().to_numpy(dtype=float)
    rng = np.random.default_rng(20260921)
    reps = 20000
    ni = rng.integers(0, len(n), size=(reps, len(n)))
    si = rng.integers(0, len(s), size=(reps, len(s)))
    diff = n[ni].mean(axis=1) - s[si].mean(axis=1)
    point = float(n.mean() - s.mean())
    lo, hi = np.quantile(diff, [0.025, 0.975])
    comp = pd.DataFrame([{
        "nifty_trades": len(n),
        "sensex_trades": len(s),
        "mean_net_nifty": float(n.mean()),
        "mean_net_sensex": float(s.mean()),
        "mean_difference_nifty_minus_sensex": point,
        "difference_ci95_low": float(lo),
        "difference_ci95_high": float(hi),
        "median_difference": float(np.median(n) - np.median(s)),
    }])
    outdir.mkdir(parents=True, exist_ok=True)
    comp.to_csv(outdir / "cross_index_comparison.csv", index=False)
    cross_text = "# Cross-Index Comparison" + chr(10) + chr(10) + comp.to_markdown(index=False) + chr(10)
    (outdir / "CROSS_INDEX_REPORT.md").write_text(cross_text, encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", choices=["NIFTY","SENSEX"])
    ap.add_argument("--primary")
    ap.add_argument("--scenario-dir")
    ap.add_argument("--output-dir")
    ap.add_argument("--compare-nifty")
    ap.add_argument("--compare-sensex")
    a = ap.parse_args()
    if a.compare_nifty and a.compare_sensex:
        compare_indices(Path(a.compare_nifty), Path(a.compare_sensex), Path(a.output_dir))
    else:
        write_single(a.index, Path(a.primary), Path(a.scenario_dir), Path(a.output_dir))
