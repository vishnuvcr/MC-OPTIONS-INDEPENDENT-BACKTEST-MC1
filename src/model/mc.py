from __future__ import annotations

import numpy as np
import pandas as pd
from src.model.strategy import choose_unique_strikes, portfolio_payoff, mc_terminal_paths


def historical_log_returns(daily: pd.DataFrame, signal_date: pd.Timestamp) -> np.ndarray:
    d = daily[daily["date"] < signal_date].copy()
    d["logret"] = np.log(d["close"].astype(float)).diff()
    return d["logret"].dropna().to_numpy(dtype=float)[-756:]


def simulate(s0: float, returns: np.ndarray, horizon: int, seed: int = 756, paths: int = 5000) -> np.ndarray:
    return mc_terminal_paths(s0, returns, horizon=horizon, paths=paths, seed=seed)


def select_strikes(terminals: np.ndarray, snapshot: pd.DataFrame) -> tuple[dict[str,float],dict[str,float]]:
    targets = {
        "P20_PE": float(np.quantile(terminals, 0.20)),
        "P35_PE": float(np.quantile(terminals, 0.35)),
        "P65_CE": float(np.quantile(terminals, 0.65)),
        "P80_CE": float(np.quantile(terminals, 0.80)),
    }
    by_type = {
        "PE": snapshot.loc[snapshot["option_type"] == "PE", "strike"].dropna().unique(),
        "CE": snapshot.loc[snapshot["option_type"] == "CE", "strike"].dropna().unique(),
    }
    return targets, choose_unique_strikes(by_type, targets)


def gross_mc_ev(terminals: np.ndarray, strikes: dict[str,float], signal_prices: dict[str,float]) -> float:
    payoff = float(np.mean(portfolio_payoff(terminals, strikes)))
    entry = float(signal_prices["P35_PE"] - 2*signal_prices["P20_PE"] + signal_prices["P65_CE"] - 2*signal_prices["P80_CE"])
    return payoff - entry
