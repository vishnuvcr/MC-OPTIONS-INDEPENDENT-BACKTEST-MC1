import numpy as np
import pandas as pd

from src.analysis.phase8 import block_bootstrap_mean, payoff_structure, sizing_examples


def test_block_bootstrap_reproducible():
    x=np.arange(20,dtype=float)
    a=block_bootstrap_mean(x,block_len=4,reps=200,seed=20260921)
    b=block_bootstrap_mean(x,block_len=4,reps=200,seed=20260921)
    assert a==b
    assert a[0]==x.mean()


def test_payoff_structure_has_unbounded_upper_tail():
    p=payoff_structure()
    assert p["expiry_payoff_at_S0_points"] == -5.0
    assert p["upper_tail_slope_points_per_index_point"] == -1.0
    assert p["upper_tail_loss"].startswith("unbounded")


def test_sizing_examples_es95_proxy():
    out=sizing_examples(-30000,(50000,100000))
    assert out["whole_batman_units"].tolist()==[1,3]
