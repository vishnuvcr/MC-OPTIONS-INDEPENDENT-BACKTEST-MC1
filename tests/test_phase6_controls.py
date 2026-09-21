import numpy as np
import pandas as pd

from src.model.mc import historical_log_returns, simulate
from src.model.strategy import mc_terminal_paths


def test_primary_defaults_and_sensitivity_controls():
    r = np.array([0.001, -0.001, 0.0005] * 400)
    a = simulate(100.0, r, 3)
    b = simulate(100.0, r, 3, paths=1000, bootstrap_window=504)
    assert len(a) == 5000
    assert len(b) == 1000
    assert np.isfinite(a).all() and np.isfinite(b).all()


def test_window_is_respected():
    dates = pd.date_range("2020-01-01", periods=900, freq="D")
    daily = pd.DataFrame({"date": dates, "close": np.exp(np.linspace(0, 0.9, len(dates)))})
    signal = dates[-1]
    r504 = historical_log_returns(daily, signal, window=504)
    r756 = historical_log_returns(daily, signal, window=756)
    assert len(r504) == 504
    assert len(r756) == 756


def test_primary_mc_seed_is_deterministic():
    r = np.array([0.001, -0.001, 0.0005] * 400)
    a = mc_terminal_paths(100.0, r, 4, seed=756, paths=5000, bootstrap_window=756)
    b = mc_terminal_paths(100.0, r, 4, seed=756, paths=5000, bootstrap_window=756)
    assert np.array_equal(a, b)
