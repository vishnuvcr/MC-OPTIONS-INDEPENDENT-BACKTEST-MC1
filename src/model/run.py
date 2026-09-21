from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.model.engine import load_daily, read_expiries, run_trade


def run(
    underlying: str,
    years: list[int],
    out: Path,
    bootstrap_window: int = 756,
    mc_paths: int = 5000,
    slippage_points: float = 2.0,
):
    ticker = "^NSEI" if underlying == "NIFTY" else "^BSESN"
    daily = load_daily(ticker)
    rows, errors = [], []
    for year in years:
        path = Path("data/raw/hf") / underlying / f"{underlying}_{year}.parquet"
        if not path.exists():
            errors.append({"year": year, "reason": "missing_file"})
            continue
        for expiry in read_expiries(path):
            try:
                r, reason = run_trade(
                    underlying,
                    path,
                    daily,
                    pd.Timestamp(expiry),
                    bootstrap_window=bootstrap_window,
                    mc_paths=mc_paths,
                    slippage_points=slippage_points,
                )
            except Exception as e:
                r, reason = None, type(e).__name__ + ": " + str(e)
            if r:
                rows.append(r)
            else:
                errors.append({"expiry": str(pd.Timestamp(expiry).date()), "reason": reason})
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    out.with_name(out.stem + "_errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    print(f"{underlying}: trades={len(rows)}, errors={len(errors)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--underlying", required=True, choices=["NIFTY","SENSEX"])
    ap.add_argument("--years", default="2024,2025,2026")
    ap.add_argument("--output", default=None)
    ap.add_argument("--bootstrap-window", type=int, default=756)
    ap.add_argument("--paths", type=int, default=5000)
    ap.add_argument("--slippage-points", type=float, default=2.0)
    a = ap.parse_args()
    years=[int(x) for x in a.years.split(",") if x.strip()]
    output=Path(a.output or f"data/processed/phase2/{a.underlying.lower()}_trades.csv")
    run(
        a.underlying,
        years,
        output,
        bootstrap_window=a.bootstrap_window,
        mc_paths=a.paths,
        slippage_points=a.slippage_points,
    )
