"""
Master Candle 09:35–09:45 baseline backtest.

Primary interpretation:
- NIFTY 1-minute underlying
- master candle = 09:35 through 09:44 IST
- breakout = first 1-minute close beyond master high/low after 09:45
- prior completed daily 25-day EMA filter
- breakout up -> buy nearest ATM CE; breakout down -> buy nearest ATM PE
- nearest listed expiry on/after trade date
- 40% premium stop
- no re-entry
- time exit 15:15 IST
- 1 historical NIFTY lot per trade
- historical contract-cohort lot-size proxy
- 1 option point adverse slippage per side
- brokerage ₹20/order in baseline
- STT on option sale at exit, date-effective
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd
from huggingface_hub import HfApi, hf_hub_download


DATASET = "thetrademarkk/india-index-options-1m"
REVISION = "main"
TZ = "Asia/Kolkata"
LOTS = 1
BROKERAGE_PER_ORDER = 20.0
SLIPPAGE_PER_SIDE = 1.0
STOP_PCT = 0.40
TIME_EXIT = "15:15"


@dataclass
class Trade:
    trading_day: str
    signal_ts: str
    breakout_direction: str
    master_high: float
    master_low: float
    master_range: float
    ema25_prev_day: float
    spot_at_breakout: float
    expiry: str
    dte: int
    option_type: str
    strike: float
    entry_market: float
    entry_exec: float
    stop_market: float
    exit_ts: str
    exit_market: float
    exit_exec: float
    exit_reason: str
    lot_size: int
    quantity: int
    gross_pnl: float
    brokerage: float
    stt: float
    slippage: float
    net_pnl: float


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="artifacts/master_candle_935")
    p.add_argument("--start", default="2021-05-27")
    p.add_argument("--end", default="2026-08-04")
    return p.parse_args()


def download_index(cache_dir: str) -> Path:
    path = hf_hub_download(
        repo_id=DATASET,
        filename="index/NIFTY.parquet",
        repo_type="dataset",
        revision=REVISION,
        cache_dir=cache_dir,
    )
    return Path(path)


def list_option_files() -> dict[date, str]:
    api = HfApi()
    files = api.list_repo_files(DATASET, repo_type="dataset", revision=REVISION)
    out: dict[date, str] = {}
    for f in files:
        if not f.startswith("options/NIFTY/") or not f.endswith(".parquet"):
            continue
        stem = Path(f).stem
        try:
            exp = pd.to_datetime(stem, format="%Y-%m-%d").date()
        except ValueError:
            continue
        out[exp] = f
    return dict(sorted(out.items()))


def nifty_lot_size(expiry: date) -> int:
    # Research proxy based on NSE effective-date circulars.
    if expiry <= date(2021, 6, 25):
        return 75
    if expiry <= date(2024, 4, 25):
        return 50
    if expiry < date(2024, 11, 20):
        return 25
    if expiry < date(2026, 1, 6):
        return 75
    return 65


def stt_rate(exit_day: date) -> float:
    if exit_day < date(2024, 10, 1):
        return 0.000625
    if exit_day < date(2026, 4, 1):
        return 0.001
    return 0.0015


def build_signal_table(index: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    x = index.copy()
    x["timestamp"] = pd.to_datetime(x["timestamp"], utc=False)
    if getattr(x["timestamp"].dt, "tz", None) is None:
        x["timestamp"] = x["timestamp"].dt.tz_localize(TZ)
    else:
        x["timestamp"] = x["timestamp"].dt.tz_convert(TZ)

    x = x.sort_values("timestamp")
    x = x[(x["timestamp"] >= start) & (x["timestamp"] <= end)]

    # Prior-day daily EMA, never including current-session data.
    daily = (
        x.assign(day=x["timestamp"].dt.date)
         .groupby("day", as_index=False)
         .agg(close=("close", "last"))
         .sort_values("day")
    )
    daily["ema25"] = daily["close"].ewm(span=25, adjust=False).mean()
    daily["ema25_prev"] = daily["ema25"].shift(1)
    ema_map = dict(zip(daily["day"], daily["ema25_prev"]))

    rows = []
    for day, g in x.groupby(x["timestamp"].dt.date):
        if len(g) == 0:
            continue
        g = g.sort_values("timestamp")
        master = g[(g["timestamp"].dt.time >= pd.Timestamp("09:35").time()) &
                   (g["timestamp"].dt.time < pd.Timestamp("09:45").time())]
        if len(master) < 8:
            continue
        master_high = float(master["high"].max())
        master_low = float(master["low"].min())
        after = g[g["timestamp"].dt.time >= pd.Timestamp("09:45").time()]
        if after.empty:
            continue

        signal = None
        for _, r in after.iterrows():
            c = float(r["close"])
            if c > master_high:
                signal = ("UP", r)
                break
            if c < master_low:
                signal = ("DOWN", r)
                break
        if signal is None:
            continue

        direction, r = signal
        ema_prev = ema_map.get(day)
        if ema_prev is None or pd.isna(ema_prev):
            continue
        spot = float(r["close"])
        if direction == "UP" and not (spot > float(ema_prev)):
            continue
        if direction == "DOWN" and not (spot < float(ema_prev)):
            continue

        rows.append({
            "trading_day": str(day),
            "signal_ts": r["timestamp"],
            "breakout_direction": direction,
            "master_high": master_high,
            "master_low": master_low,
            "master_range": master_high - master_low,
            "ema25_prev_day": float(ema_prev),
            "spot_at_breakout": spot,
        })
    return pd.DataFrame(rows)


def nearest_expiry(signal_day: date, expiries: list[date]) -> date | None:
    for e in expiries:
        if e >= signal_day:
            return e
    return None


def pick_option_rows(opt: pd.DataFrame, ts: pd.Timestamp, option_type: str):
    g = opt[(opt["timestamp"] == ts) & (opt["option_type"] == option_type)]
    if g.empty:
        return g
    return g.dropna(subset=["strike", "close"]).copy()


def process_expiry_group(
    opt_file: str,
    expiry: date,
    signals: pd.DataFrame,
    cache_dir: str,
) -> list[Trade]:
    local = hf_hub_download(
        repo_id=DATASET,
        filename=opt_file,
        repo_type="dataset",
        revision=REVISION,
        cache_dir=cache_dir,
    )
    opt = pd.read_parquet(local)
    opt["timestamp"] = pd.to_datetime(opt["timestamp"], utc=False)
    if getattr(opt["timestamp"].dt, "tz", None) is None:
        opt["timestamp"] = opt["timestamp"].dt.tz_localize(TZ)
    else:
        opt["timestamp"] = opt["timestamp"].dt.tz_convert(TZ)

    opt = opt.sort_values("timestamp")
    opt["option_type"] = opt["option_type"].astype(str).str.upper()
    trades = []

    for _, s in signals.iterrows():
        day = pd.Timestamp(s["trading_day"]).date()
        sig_ts = pd.Timestamp(s["signal_ts"])
        opt_type = "CE" if s["breakout_direction"] == "UP" else "PE"
        exact = pick_option_rows(opt, sig_ts, opt_type)
        if exact.empty:
            continue

        exact["distance"] = (exact["strike"] - float(s["spot_at_breakout"])).abs()
        chosen = exact.sort_values(["distance", "strike"]).iloc[0]
        strike = float(chosen["strike"])
        entry_market = float(chosen["close"])
        if entry_market <= 0:
            continue

        stop_market = entry_market * (1.0 - STOP_PCT)
        entry_exec = entry_market + SLIPPAGE_PER_SIDE

        later = opt[
            (opt["timestamp"] > sig_ts)
            & (opt["timestamp"].dt.date == day)
            & (opt["option_type"] == opt_type)
            & (opt["strike"] == strike)
        ].copy()
        later = later.sort_values("timestamp")

        exit_ts = None
        exit_market = None
        exit_reason = None
        for _, r in later.iterrows():
            ts = r["timestamp"]
            if ts > pd.Timestamp(f"{day} {TIME_EXIT}", tz=TZ):
                break
            low = float(r["low"])
            opn = float(r["open"])
            if low <= stop_market:
                exit_ts = ts
                exit_market = opn if opn < stop_market else stop_market
                exit_reason = "40pct_premium_stop"
                break

        if exit_ts is None:
            end_bar = later[later["timestamp"].dt.time <= pd.Timestamp(TIME_EXIT).time()]
            if end_bar.empty:
                continue
            r = end_bar.iloc[-1]
            exit_ts = r["timestamp"]
            exit_market = float(r["close"])
            exit_reason = "15:15_time_exit"

        exit_exec = max(0.0, float(exit_market) - SLIPPAGE_PER_SIDE)
        lot = nifty_lot_size(expiry)
        qty = LOTS * lot
        gross = (exit_exec - entry_exec) * qty
        brokerage = 2.0 * BROKERAGE_PER_ORDER
        stt = (exit_exec * qty) * stt_rate(day)
        slippage = 2.0 * SLIPPAGE_PER_SIDE * qty
        net = gross - brokerage - stt

        dte = (expiry - day).days
        trades.append(Trade(
            trading_day=str(day),
            signal_ts=sig_ts.isoformat(),
            breakout_direction=s["breakout_direction"],
            master_high=float(s["master_high"]),
            master_low=float(s["master_low"]),
            master_range=float(s["master_range"]),
            ema25_prev_day=float(s["ema25_prev_day"]),
            spot_at_breakout=float(s["spot_at_breakout"]),
            expiry=str(expiry),
            dte=int(dte),
            option_type=opt_type,
            strike=strike,
            entry_market=entry_market,
            entry_exec=entry_exec,
            stop_market=stop_market,
            exit_ts=exit_ts.isoformat(),
            exit_market=float(exit_market),
            exit_exec=exit_exec,
            exit_reason=exit_reason,
            lot_size=lot,
            quantity=qty,
            gross_pnl=float((exit_market - entry_market) * qty),
            brokerage=float(brokerage),
            stt=float(stt),
            slippage=float(slippage),
            net_pnl=float(net),
        ))
    return trades


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = str(out_dir / "hf_cache")
    os.makedirs(cache_dir, exist_ok=True)

    idx_path = download_index(cache_dir)
    index = pd.read_parquet(idx_path)
    signals = build_signal_table(
        index,
        pd.Timestamp(args.start, tz=TZ),
        pd.Timestamp(args.end + " 23:59:59", tz=TZ),
    )
    signals.to_csv(out_dir / "signals.csv", index=False)

    files = list_option_files()
    expiries = list(files)
    if not expiries:
        raise RuntimeError("No NIFTY option expiry files found")

    all_trades = []
    for exp in expiries:
        group = signals[pd.to_datetime(signals["trading_day"]).dt.date.map(
            lambda d: nearest_expiry(d, expiries) == exp
        )]
        if group.empty:
            continue
        all_trades.extend(process_expiry_group(files[exp], exp, group, cache_dir))

    trades = pd.DataFrame([t.__dict__ for t in all_trades])
    if trades.empty:
        raise RuntimeError("No trades produced")

    trades = trades.sort_values(["trading_day", "signal_ts"]).drop_duplicates("trading_day", keep="first")
    trades.to_csv(out_dir / "trades.csv", index=False)

    summary = {
        "strategy": "master_candle_935_primary",
        "dataset": DATASET,
        "revision": REVISION,
        "coverage_start": str(trades["trading_day"].min()),
        "coverage_end": str(trades["trading_day"].max()),
        "lots_per_trade": LOTS,
        "trades": int(len(trades)),
        "mean_net_pnl": float(trades["net_pnl"].mean()),
        "median_net_pnl": float(trades["net_pnl"].median()),
        "sum_net_pnl": float(trades["net_pnl"].sum()),
        "win_rate": float((trades["net_pnl"] > 0).mean()),
        "profit_factor": float(
            trades.loc[trades["net_pnl"] > 0, "net_pnl"].sum()
            / abs(trades.loc[trades["net_pnl"] < 0, "net_pnl"].sum())
        ) if (trades["net_pnl"] < 0).any() else None,
        "max_loss": float(trades["net_pnl"].min()),
        "max_drawdown": float(
            (trades["net_pnl"].cumsum() - trades["net_pnl"].cumsum().cummax()).min()
        ),
        "zero_dte_trades": int((trades["dte"] == 0).sum()),
        "zero_dte_net_pnl": float(trades.loc[trades["dte"] == 0, "net_pnl"].sum()),
    }
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
