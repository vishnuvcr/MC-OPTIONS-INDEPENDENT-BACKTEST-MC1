from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.model.engine import load_daily, read_expiries, run_trade

WINDOWS=(504,756,1008)
PATHS=(1000,5000,10000)

def run_matrix(underlying:str, years:list[int], outdir:Path)->None:
    outdir.mkdir(parents=True,exist_ok=True)
    ticker="^NSEI" if underlying=="NIFTY" else "^BSESN"
    daily=load_daily(ticker)
    for w in WINDOWS:
        for paths in PATHS:
            rows=[]; errors=[]
            for year in years:
                path=Path("data/raw/hf")/underlying/f"{underlying}_{year}.parquet"
                if not path.exists():
                    errors.append({"year":year,"reason":"missing_file"})
                    continue
                for expiry in read_expiries(path):
                    try:
                        r,reason=run_trade(underlying,path,daily,pd.Timestamp(expiry),bootstrap_window=w,mc_paths=paths)
                    except Exception as e:
                        r,reason=None,type(e).__name__+": "+str(e)
                    if r: rows.append(r)
                    else: errors.append({"expiry":str(pd.Timestamp(expiry).date()),"reason":reason})
            stem=f"{underlying.lower()}_w{w}_p{paths}"
            pd.DataFrame(rows).to_csv(outdir/f"{stem}.csv",index=False)
            (outdir/f"{stem}_errors.json").write_text(json.dumps(errors,indent=2),encoding="utf-8")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--underlying",choices=["NIFTY","SENSEX"],required=True)
    ap.add_argument("--years",default="2024,2025,2026")
    ap.add_argument("--output-dir",required=True)
    a=ap.parse_args()
    run_matrix(a.underlying,[int(x) for x in a.years.split(",") if x.strip()],Path(a.output_dir))
