import pandas as pd
from src.model.strategy import LEGS

def first_executable(x, signal_time, strikes):
    z=x.copy()
    z['timestamp']=pd.to_datetime(z['timestamp'], errors='coerce')
    z['strike']=pd.to_numeric(z['strike'], errors='coerce')
    z['close']=pd.to_numeric(z['close'], errors='coerce')
    parts=[]
    for leg in LEGS:
        q=z[(z.option_type==leg.option_type)&(z.strike==float(strikes[leg.label]))&(z.timestamp>signal_time)&(z.close>0)].copy()
        if 'volume' in q:
            q['volume']=pd.to_numeric(q['volume'], errors='coerce')
            q=q[(q.volume>0)|q.volume.isna()]
        if q.empty: return None
        cols=['timestamp','close'] + (['volume'] if 'volume' in q.columns else [])
        parts.append(q[cols].assign(label=leg.label))
    price_frames=[]
    volume_frames=[]
    for p in parts:
        pf=p.pivot_table(index='timestamp', columns='label', values='close', aggfunc='last')
        price_frames.append(pf)
        if 'volume' in p.columns:
            vf=p.pivot_table(index='timestamp', columns='label', values='volume', aggfunc='last')
            volume_frames.append(vf)
    wide=pd.concat(price_frames,axis=1)
    labels=[leg.label for leg in LEGS]
    wide=wide.loc[:,~wide.columns.duplicated()]
    wide=wide.dropna(subset=labels)
    if wide.empty: return None
    ts=wide.index.min()
    prices={k:float(wide.loc[ts,k]) for k in labels}
    volumes={}
    if volume_frames:
        vw=pd.concat(volume_frames,axis=1)
        vw=vw.loc[:,~vw.columns.duplicated()]
        for k in labels:
            volumes[k]=None if k not in vw.columns or pd.isna(vw.loc[ts,k]) else float(vw.loc[ts,k])
    return ts,prices,volumes
