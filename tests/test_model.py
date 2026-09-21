import numpy as np
import pandas as pd

from src.model.costs import entry_slipped_price, stt_sale_rate
from src.model.mc import simulate
from src.model.strategy import choose_unique_strikes, portfolio_payoff


def test_mc_reproducible():
    r=np.array([0.01,-0.005,0.002]*300,dtype=float)
    a=simulate(100.0,r,3,seed=756,paths=5000)
    b=simulate(100.0,r,3,seed=756,paths=5000)
    assert a.shape==(5000,)
    assert np.array_equal(a,b)


def test_unique_strike_mapping():
    out=choose_unique_strikes(
        {"PE":np.array([95,100,105]),"CE":np.array([105,110,115])},
        {"P20_PE":98,"P35_PE":100,"P65_CE":106,"P80_CE":111},
    )
    assert len(set(out.values()))==4


def test_payoff_zero_at_strikes():
    s=np.array([100.0])
    k={"P20_PE":95,"P35_PE":100,"P65_CE":100,"P80_CE":105}
    assert portfolio_payoff(s,k)[0] == 0.0


def test_slippage_direction():
    assert entry_slipped_price(10,1,2)==12
    assert entry_slipped_price(10,-1,2)==8
    assert stt_sale_rate(pd.Timestamp("2025-01-01"))==0.001

from src.model.execution import first_executable

def test_first_executable_common_timestamp():
    rows=[
        {"timestamp":"2026-01-01 09:31:00+05:30","strike":95,"option_type":"PE","close":10,"volume":1},
        {"timestamp":"2026-01-01 09:31:00+05:30","strike":100,"option_type":"PE","close":12,"volume":1},
        {"timestamp":"2026-01-01 09:31:00+05:30","strike":105,"option_type":"CE","close":14,"volume":1},
        {"timestamp":"2026-01-01 09:31:00+05:30","strike":110,"option_type":"CE","close":16,"volume":1},
    ]
    import pandas as pd
    x=pd.DataFrame(rows)
    out=first_executable(x,pd.Timestamp("2026-01-01 09:30:00+05:30"),{"P20_PE":95,"P35_PE":100,"P65_CE":105,"P80_CE":110})
    assert out is not None
    assert str(out[0])[:16]=="2026-01-01 09:31"


def test_nifty_lot_size_cohort_dates():
    from src.model.engine import lot_size
    assert lot_size("NIFTY", pd.Timestamp("2024-11-14")) == 25
    assert lot_size("NIFTY", pd.Timestamp("2024-11-21")) == 75
    assert lot_size("NIFTY", pd.Timestamp("2025-12-30")) == 75
    assert lot_size("NIFTY", pd.Timestamp("2026-01-06")) == 65
