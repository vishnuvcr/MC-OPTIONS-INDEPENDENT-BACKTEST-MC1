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
