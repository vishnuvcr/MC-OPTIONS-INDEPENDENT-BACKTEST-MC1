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
        parts.append(q[['timestamp','close']].assign(label=leg.label))
    wide=pd.concat(parts, ignore_index=True).pivot_table(index='timestamp', columns='label', values='close', aggfunc='last')
    labels=[leg.label for leg in LEGS]
    wide=wide.dropna(subset=labels)
    if wide.empty: return None
    ts=wide.index.min()
    return ts,{k:float(wide.loc[ts,k]) for k in labels}
