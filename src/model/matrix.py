from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.model.engine import load_daily, read_expiries, read_window, run_trade

WINDOWS=(504,756,1008)
PATHS=(1000,5000,10000)

def run_matrix(underlying:str, years:list[int], outdir:Path)->None:
    outdir.mkdir(parents=True,exist_ok=True)
    ticker="^NSEI" if underlying=="NIFTY" else "^BSESN"
    daily=load_daily(ticker)
    # Cache each expiry's raw option window once and reuse it across all nine MC calibrations.
    cached={}
    missing=[]
    for year in years:
        path=Path("data/raw/hf")/underlying/f"{underlying}_{year}.parquet"
        if not path.exists():
            missing.append({"year":year,"reason":"missing_file"})
            continue
        for expiry in read_expiries(path):
            expiry=pd.Timestamp(expiry)
            sessions_dates=pd.to_datetime(daily["date"]).dt.normalize().tolist()
            idx=next((i for i,d in enumerate(sorted(sessions_dates)) if d==expiry.normalize()),None)
            if idx is None or idx < 3:
                cached[(year,str(expiry.date()))]=None
                continue
            signal_date=sorted(sessions_dates)[idx-3]
            try:
                cached[(year,str(expiry.date()))]=read_window(path,expiry,pd.Timestamp(signal_date))
            except Exception:
                cached[(year,str(expiry.date()))]=None

    for w in WINDOWS:
        for paths in PATHS:
            rows=[]; errors=list(missing)
            for year in years:
                path=Path("data/raw/hf")/underlying/f"{underlying}_{year}.parquet"
                if not path.exists():
                    continue
                for expiry in read_expiries(path):
                    expiry=pd.Timestamp(expiry)
                    raw_window=cached.get((year,str(expiry.date())))
                    try:
                        r,reason=run_trade(underlying,path,daily,expiry,bootstrap_window=w,mc_paths=paths,raw_window=raw_window)
                    except Exception as e:
                        r,reason=None,type(e).__name__+": "+str(e)
                    if r: rows.append(r)
                    else: errors.append({"expiry":str(expiry.date()),"reason":reason})
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
