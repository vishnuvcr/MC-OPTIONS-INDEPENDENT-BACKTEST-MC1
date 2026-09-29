from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path("artifacts/mc1")
OUT = Path("artifacts/mc2")
OUT.mkdir(parents=True, exist_ok=True)

# Current documented standardized scenario:
# Paytm Money ₹20/order, NSE option transaction charge 0.03552% each side,
# SEBI turnover fee 0.0001% each side, buyer stamp duty 0.003%,
# GST 18% on brokerage + exchange + SEBI, and date-effective STT.
def stt_rate(day):
    day = pd.Timestamp(day).date()
    if day < pd.Timestamp("2024-10-01").date():
        return 0.000625
    if day < pd.Timestamp("2026-04-01").date():
        return 0.001
    return 0.0015

frames = []
for p in sorted(ROOT.glob("*/trades.csv")):
    x = pd.read_csv(p)
    x["source_year"] = p.parent.name
    frames.append(x)
if not frames:
    raise RuntimeError("No MC1 trade ledgers found")
t = pd.concat(frames, ignore_index=True)
t["trading_day"] = pd.to_datetime(t["trading_day"])
t = t.sort_values("trading_day").drop_duplicates("trading_day", keep="first")

t["buy_value"] = t["entry_market"] * t["quantity"]
t["sell_value"] = t["exit_market"] * t["quantity"]
t["premium_turnover"] = t["buy_value"] + t["sell_value"]

def scenario(slippage_points, brokerage_order, full_cost=True):
    entry = t["entry_market"] + slippage_points
    exit_ = (t["exit_market"] - slippage_points).clip(lower=0)
    slippage = 2 * slippage_points * t["quantity"]
    gross_after_slip = (exit_ - entry) * t["quantity"]
    brokerage = 2 * brokerage_order
    stt = t["sell_value"] * t["trading_day"].map(stt_rate)
    if full_cost:
        exchange = 0.0003552 * t["premium_turnover"]
        sebi = 0.000001 * t["premium_turnover"]
        stamp = 0.00003 * t["buy_value"]
        gst = 0.18 * (brokerage + exchange + sebi)
    else:
        exchange = 0.0
        sebi = 0.0
        stamp = 0.0
        gst = 0.0
    net = gross_after_slip - brokerage - stt - exchange - sebi - stamp - gst
    return net

rows = []
for slip in [0.5, 1.0, 2.0]:
    for brokerage in [10.0, 15.0, 20.0]:
        for full_cost in [False, True]:
            net = scenario(slip, brokerage, full_cost)
            rows.append({
                "slippage_points_each_side": slip,
                "brokerage_per_order": brokerage,
                "full_statutory_cost_stack": full_cost,
                "trades": len(net),
                "net_pnl": float(net.sum()),
                "mean_trade": float(net.mean()),
                "win_rate": float((net > 0).mean()),
                "profit_factor": float(net[net > 0].sum() / abs(net[net < 0].sum())) if (net < 0).any() else None,
                "max_trade_loss": float(net.min()),
                "max_drawdown": float((net.cumsum() - net.cumsum().cummax()).min()),
            })
res = pd.DataFrame(rows)

# Primary current-cost scenario at 1 point and ₹20/order.
primary = res[(res.slippage_points_each_side == 1.0) &
              (res.brokerage_per_order == 20.0) &
              (res.full_statutory_cost_stack == True)].iloc[0]

# Weekly target and 0-DTE contribution under the primary scenario.
net = scenario(1.0, 20.0, True)
z = t["dte"].eq(0)
weekly = pd.DataFrame({"net": net.values}, index=t["trading_day"]).resample("W-FRI").sum()["net"]
weekly = weekly[weekly != 0]
znet = float(net[z].sum())

summary = {
    "trades": int(len(t)),
    "primary_full_cost_net_pnl": float(primary.net_pnl),
    "primary_mean_trade": float(primary.mean_trade),
    "primary_win_rate": float(primary.win_rate),
    "primary_profit_factor": float(primary.profit_factor),
    "primary_max_drawdown": float(primary.max_drawdown),
    "positive_week_fraction": float((weekly > 0).mean()),
    "weeks_ge_5000_fraction": float((weekly >= 5000).mean()),
    "mean_weekly": float(weekly.mean()),
    "median_weekly": float(weekly.median()),
    "zero_dte_net_pnl": znet,
    "zero_dte_trades": int(z.sum()),
}
res.to_csv(OUT / "cost_sensitivity.csv", index=False)
weekly.rename("net_pnl").to_csv(OUT / "primary_weekly.csv")
with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
