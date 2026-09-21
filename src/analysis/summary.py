from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def es(series: pd.Series, alpha: float) -> float:
    q = series.quantile(1 - alpha)
    tail = series[series <= q]
    return float(tail.mean())


def main(path: str, output: str):
    df = pd.read_csv(path)
    x = df[df["executed"] == True].copy()
    if x.empty:
        raise RuntimeError("No executed trades")
    x["expiry"] = pd.to_datetime(x["expiry"])
    x = x.sort_values("expiry")
    x["cum_net"] = x["net_realized_rupees"].cumsum()
    x["peak"] = x["cum_net"].cummax()
    x["drawdown"] = x["cum_net"] - x["peak"]
    summary = {
        "trades": int(len(x)),
        "start": str(x["expiry"].min().date()),
        "end": str(x["expiry"].max().date()),
        "mean_mc_ev_points": float(x["mc_ev_points"].mean()),
        "median_mc_ev_points": float(x["mc_ev_points"].median()),
        "mean_gross_rupees": float(x["gross_realized_rupees"].mean()),
        "mean_net_rupees": float(x["net_realized_rupees"].mean()),
        "median_net_rupees": float(x["net_realized_rupees"].median()),
        "net_profit_share": float((x["net_realized_rupees"] > 0).mean()),
        "sum_net_rupees": float(x["net_realized_rupees"].sum()),
        "es95_rupees": es(x["net_realized_rupees"], 0.95),
        "es99_rupees": es(x["net_realized_rupees"], 0.99),
        "max_drawdown_rupees": float(x["drawdown"].min()),
    }
    yearly = x.assign(year=x.expiry.dt.year).groupby("year").agg(
        trades=("net_realized_rupees","size"),
        mean_net_rupees=("net_realized_rupees","mean"),
        sum_net_rupees=("net_realized_rupees","sum"),
        median_net_rupees=("net_realized_rupees","median"),
    ).reset_index()
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = "# Summary\n\n" + "\n".join(f"- {k}: {v}" for k, v in summary.items()) + "\n\n## By year\n\n" + yearly.to_markdown(index=False) + "\n"
    out.write_text(report, encoding="utf-8")
    print(out.read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    main(a.path, a.output)
