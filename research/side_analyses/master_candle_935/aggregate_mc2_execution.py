import json
from pathlib import Path
import pandas as pd

ROOT=Path("artifacts/variants")
OUT=Path("artifacts/mc2_execution")
OUT.mkdir(parents=True,exist_ok=True)

rows=[]
for p in ROOT.glob("*/summary.json"):
    with open(p) as f: s=json.load(f)
    trades_path=p.parent/"trades.csv"
    t=pd.read_csv(trades_path)
    t["trading_day"]=pd.to_datetime(t["trading_day"])
    weekly=t.groupby(t["trading_day"].dt.to_period("W-FRI"))["net_pnl"].sum()
    rows.append({
        "variant":p.parent.name,
        "breakout_mode":s["breakout_mode"],
        "stop_pct":s["stop_pct"],
        "time_exit":s["time_exit"],
        "trades":int(len(t)),
        "net_pnl":float(t["net_pnl"].sum()),
        "win_rate":float((t["net_pnl"]>0).mean()),
        "profit_factor":float(t.loc[t.net_pnl>0,"net_pnl"].sum()/abs(t.loc[t.net_pnl<0,"net_pnl"].sum())) if (t.net_pnl<0).any() else None,
        "max_drawdown":float((t.net_pnl.cumsum()-t.net_pnl.cumsum().cummax()).min()),
        "positive_week_fraction":float((weekly>0).mean()),
        "weeks_ge_5000_fraction":float((weekly>=5000).mean()),
        "zero_dte_net_pnl":float(t.loc[t.dte==0,"net_pnl"].sum()),
    })
res=pd.DataFrame(rows).sort_values(["breakout_mode","stop_pct","time_exit"])
res.to_csv(OUT/"execution_variant_grid.csv",index=False)
with open(OUT/"status.json","w") as f:
    json.dump({"variants_completed":len(res),"note":"Descriptive robustness grid; no variant is promoted by historical rank."},f,indent=2)
print(res.to_string(index=False))
