from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from src.model.costs import entry_costs, entry_slipped_price, expiry_stt, enhanced_entry_costs
from src.model.mc import gross_mc_ev, historical_log_returns, select_strikes, simulate
from src.model.strategy import LEGS, expiry_sessions, signal_spot_from_parity
from src.model.execution import first_executable


def read_expiries(path: Path) -> list[pd.Timestamp]:
    df = pq.read_table(path, columns=["expiry"]).to_pandas()
    return sorted(pd.to_datetime(df["expiry"], errors="coerce").dropna().dt.normalize().unique())


def read_window(path: Path, expiry: pd.Timestamp, start: pd.Timestamp) -> pd.DataFrame:
    available = set(pq.read_schema(path).names)
    base_cols=["date","timestamp","expiry","strike","option_type","close","volume"]
    if "lot_size" in available:
        base_cols.append("lot_size")
    table = pq.read_table(
        path,
        columns=base_cols,
        filters=[
            ("expiry","=",expiry.strftime("%Y-%m-%d")),
            ("date",">=",start.strftime("%Y-%m-%d")),
            ("date","<=",expiry.strftime("%Y-%m-%d")),
        ],
    )
    x = table.to_pandas()
    x["date"] = pd.to_datetime(x["date"], errors="coerce").dt.normalize()
    x["timestamp"] = pd.to_datetime(x["timestamp"], errors="coerce")
    x["expiry"] = pd.to_datetime(x["expiry"], errors="coerce").dt.normalize()
    x["strike"] = pd.to_numeric(x["strike"], errors="coerce")
    x["close"] = pd.to_numeric(x["close"], errors="coerce")
    x["volume"] = pd.to_numeric(x["volume"], errors="coerce")
    if "lot_size" in x.columns:
        x["lot_size"] = pd.to_numeric(x["lot_size"], errors="coerce")
    return x.dropna(subset=["date","timestamp","strike","option_type","close"])


def load_daily(ticker: str) -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(ticker, period="max", interval="1d", auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns=[c[0] for c in df.columns]
    df=df.reset_index()
    df.columns=[str(c).lower().replace(" ","_") for c in df.columns]
    c="date" if "date" in df.columns else "datetime"
    df[c]=pd.to_datetime(df[c],utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize()
    return df.rename(columns={c:"date"})[["date","close"]].dropna().drop_duplicates("date").sort_values("date")


def signal_snapshot(window: pd.DataFrame, signal_date: pd.Timestamp):
    x = window.copy()
    x["timestamp"] = pd.to_datetime(x["timestamp"], errors="coerce")
    if x["timestamp"].dt.tz is None:
        x["timestamp"] = x["timestamp"].dt.tz_localize("Asia/Kolkata")
    else:
        x["timestamp"] = x["timestamp"].dt.tz_convert("Asia/Kolkata")
    cutoff = pd.Timestamp(f"{signal_date.date()} 09:30:00", tz="Asia/Kolkata")
    x = x[x["timestamp"] <= cutoff]
    if x.empty:
        return None, None
    ts = x["timestamp"].max()
    return ts, x[x["timestamp"] == ts].copy()


def signal_prices(snapshot: pd.DataFrame, strikes: dict[str,float]) -> dict[str,float]:
    out={}
    for leg in LEGS:
        x=snapshot[
            (snapshot["option_type"]==leg.option_type)
            &(snapshot["strike"]==float(strikes[leg.label]))
            &(snapshot["close"]>0)
        ]
        if x.empty:
            raise ValueError("missing signal price "+leg.label)
        out[leg.label]=float(x["close"].iloc[-1])
    return out


def lot_size(underlying: str, expiry: pd.Timestamp) -> int:
    if underlying=="NIFTY":
        if expiry<pd.Timestamp("2024-05-01"): return 50
        if expiry<pd.Timestamp("2024-11-20"): return 25
        if expiry<pd.Timestamp("2026-01-06"): return 75
        return 65
    if underlying=="SENSEX":
        return 10 if expiry<pd.Timestamp("2024-11-20") else 20
    raise ValueError(underlying)


def run_trade(
    underlying: str,
    path: Path,
    daily: pd.DataFrame,
    expiry: pd.Timestamp,
    bootstrap_window: int = 756,
    mc_paths: int = 5000,
    slippage_points: float = 2.0,
    raw_window: pd.DataFrame | None = None,
):
    sessions=expiry_sessions(daily["date"].tolist(), expiry)
    if sessions is None:
        return None,"missing_d3"
    signal_date=sessions[0]
    window=raw_window if raw_window is not None else read_window(path, expiry, signal_date)
    signal_ts,snap=signal_snapshot(window, signal_date)
    if snap is None:
        return None,"missing_signal_snapshot"
    fallback=float(daily.loc[daily["date"]<signal_date,"close"].iloc[-1])
    s0,s0_source=signal_spot_from_parity(snap,fallback)
    returns=historical_log_returns(daily,signal_date,window=bootstrap_window)
    if len(returns)<bootstrap_window:
        return None,f"missing_{bootstrap_window}_history"
    terminals=simulate(
        s0,
        returns,
        len(sessions)-1,
        paths=mc_paths,
        bootstrap_window=bootstrap_window,
    )
    qtargets,strikes=select_strikes(terminals,snap)
    sig_prices=signal_prices(snap,strikes)
    ev=gross_mc_ev(terminals,strikes,sig_prices)
    if ev <= 0:
        return None,"mc_ev_gate_fail"
    ex=first_executable(window,signal_ts,strikes)
    if ex is None:
        return None,"missing_common_execution"
    exec_ts,raw,raw_volume=ex
    qty={x.label:x.quantity for x in LEGS}
    slipped={k:entry_slipped_price(v,qty[k],slippage_points) for k,v in raw.items()}
    settle=float(daily.loc[daily["date"]==expiry,"close"].iloc[0])
    gross_pts=0.0
    net_pts=0.0
    for leg in LEGS:
        intr=max(strikes[leg.label]-settle,0.0) if leg.option_type=="PE" else max(settle-strikes[leg.label],0.0)
        gross_pts += leg.quantity*(intr-raw[leg.label])
        net_pts += leg.quantity*(intr-slipped[leg.label])
    if "lot_size" in window.columns and window["lot_size"].notna().any():
        vals=window["lot_size"].dropna().astype(int).unique()
        if len(vals) != 1:
            raise ValueError(f"multiple lot sizes in contract data: {vals.tolist()}")
        lot=int(vals[0])
        lot_source="contract_data"
    else:
        lot=lot_size(underlying,expiry)
        lot_source="fallback_schedule"
    displacement = {k: float(strikes[k]) - float(qtargets[k]) for k in strikes}
    costs=entry_costs(slipped,qty,lot,expiry)
    costs["stt_expiry"]=expiry_stt(expiry,settle,strikes,qty,lot)
    enhanced=enhanced_entry_costs(underlying,slipped,qty,lot,expiry)
    enhanced["stt_expiry"]=costs["stt_expiry"]
    enhanced_extra = enhanced["exchange_transaction"] + enhanced["sebi_turnover"] + enhanced["stamp_duty"] + enhanced["gst_on_brokerage_and_venue_fees"]
    return {
        "underlying":underlying,
        "expiry":str(expiry.date()),
        "signal_date":str(signal_date.date()),
        "signal_timestamp":str(signal_ts),
        "execution_timestamp":str(exec_ts),
        "gate_premium_timestamp":str(signal_ts),
        "gate_premium_source":"latest_common_option_snapshot_at_or_before_09:30_IST",
        "s0":s0,
        "s0_source":s0_source,
        "settlement_spot":settle,
        "mc_ev_points":ev,
        "gate":True,
        "executed":True,
        "strikes":json.dumps(strikes,sort_keys=True),
        "quantile_targets":json.dumps(qtargets,sort_keys=True),
        "strike_displacement_points":json.dumps(displacement,sort_keys=True),
        "max_abs_strike_displacement_points":max(abs(v) for v in displacement.values()),
        "mean_abs_strike_displacement_points":sum(abs(v) for v in displacement.values())/len(displacement),
        "exact_strike_target_count":sum(abs(displacement[k]) < 1e-9 for k in displacement),
        "signal_prices":json.dumps(sig_prices,sort_keys=True),
        "execution_prices_raw":json.dumps(raw,sort_keys=True),
        "execution_volume":json.dumps(raw_volume,sort_keys=True),
        "available_strikes_by_type":json.dumps({t:sorted(set(float(v) for v in snap.loc[snap["option_type"]==t,"strike"].dropna())) for t in ("PE","CE")},sort_keys=True),
        "execution_prices_slipped":json.dumps(slipped,sort_keys=True),
        "lot_size":lot,
        "lot_size_source":lot_source,
        "gross_realized_rupees":gross_pts*lot,
        "net_realized_rupees":net_pts*lot-costs["brokerage"]-costs["stt_entry"]-costs["stt_expiry"],
        "net_realized_rupees_enhanced_friction":net_pts*lot-enhanced["total_enhanced_entry_cost"]-enhanced["stt_expiry"],
        "enhanced_extra_entry_friction_rupees":enhanced_extra,
        "brokerage":costs["brokerage"],
        "stt_entry":costs["stt_entry"],
        "stt_expiry":costs["stt_expiry"],
        "exchange_transaction":enhanced["exchange_transaction"],
        "sebi_turnover":enhanced["sebi_turnover"],
        "stamp_duty":enhanced["stamp_duty"],
        "gst_on_brokerage_and_venue_fees":enhanced["gst_on_brokerage_and_venue_fees"],
        "enhanced_total_entry_cost":enhanced["total_enhanced_entry_cost"],
    },None
