from pathlib import Path
import hashlib
import json
import os
import pandas as pd
import yfinance as yf

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def daily(ticker):
    df=yf.download(ticker, period="max", interval="1d", auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns=[c[0] for c in df.columns]
    df=df.reset_index()
    df.columns=[str(c).lower().replace(" ","_") for c in df.columns]
    c="date" if "date" in df.columns else "datetime"
    df[c]=pd.to_datetime(df[c], utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize()
    df=df.rename(columns={c:"date"})[["date","close"]].dropna().drop_duplicates("date").sort_values("date")
    if len(df)<756:
        raise RuntimeError(f"{ticker}: {len(df)} sessions, expected >=756")
    return df

def main():
    years=[int(x) for x in os.environ.get("YEARS","2024").split(",") if x.strip()]
    root=Path("data/raw/hf")
    out=Path("data/processed/phase1")
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    for u in ("NIFTY","SENSEX"):
        for y in years:
            p=root/u/f"{u}_{y}.parquet"
            if not p.exists():
                raise FileNotFoundError(str(p))
            df=pd.read_parquet(p, columns=["date","timestamp","underlying","expiry","strike","option_type","close","volume","oi","source","granularity"])
            if df.empty:
                raise RuntimeError(f"{p} is empty")
            if not set(["CE","PE"]).issubset(set(df["option_type"].dropna().unique())):
                raise RuntimeError(f"{p}: missing CE or PE")
            rows.append({"path":str(p),"sha256":sha256(p),"rows":int(len(df)),"date_min":str(df["date"].min()),"date_max":str(df["date"].max())})
    daily("^NSEI").to_csv(out/"nifty_daily.csv", index=False)
    daily("^BSESN").to_csv(out/"sensex_daily.csv", index=False)
    payload={"years":years,"files":rows,"generated_at":pd.Timestamp.utcnow().isoformat()}
    (out/"phase1_manifest.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2))

if __name__=="__main__":
    main()
