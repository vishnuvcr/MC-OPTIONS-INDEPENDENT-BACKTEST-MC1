import numpy as np
import pandas as pd

from src.model.engine import historical_log_returns
from src.model.execution import first_executable
from src.model.strategy import LEGS, choose_unique_strikes


def test_bootstrap_uses_only_pre_signal_history():
    dates=pd.date_range("2022-01-01", periods=1000, freq="D")
    close=np.exp(np.linspace(0,0.5,1000))
    daily=pd.DataFrame({"date":dates,"close":close})
    # A huge post-signal move must not enter the 756-return information set.
    daily.loc[daily["date"]=="2024-12-31","close"] *= 1000
    signal=pd.Timestamp("2024-12-30")
    r=historical_log_returns(daily, signal)
    assert len(r)==756
    assert np.max(np.abs(r)) < 1.0


def test_execution_is_strictly_after_signal_and_common_timestamp():
    signal=pd.Timestamp("2024-01-02 09:30:00")
    rows=[]
    strikes={"P35_PE":100.0,"P20_PE":95.0,"P65_CE":105.0,"P80_CE":110.0}
    for leg in LEGS:
        rows.append({
            "timestamp":pd.Timestamp("2024-01-02 09:30:00"),
            "option_type":leg.option_type,
            "strike":strikes[leg.label],
            "close":10.0,
            "volume":1,
        })
        rows.append({
            "timestamp":pd.Timestamp("2024-01-02 09:31:00"),
            "option_type":leg.option_type,
            "strike":strikes[leg.label],
            "close":11.0,
            "volume":1,
        })
    x=pd.DataFrame(rows)
    out=first_executable(x,signal,strikes)
    assert out is not None
    ts, prices=out
    assert ts == pd.Timestamp("2024-01-02 09:31:00")
    assert all(v==11.0 for v in prices.values())


def test_four_target_strikes_are_unique():
    out=choose_unique_strikes(
        {"PE":np.array([95,100,105,110]),"CE":np.array([105,110,115,120])},
        {"P20_PE":99,"P35_PE":101,"P65_CE":108,"P80_CE":116},
    )
    assert len(set(out.values()))==4


def test_mc_path_count_is_locked():
    from src.model.mc import simulate
    returns=np.array([0.001,-0.001,0.0005]*300)
    paths=simulate(100.0,returns,3,seed=756,paths=5000)
    assert len(paths)==5000
