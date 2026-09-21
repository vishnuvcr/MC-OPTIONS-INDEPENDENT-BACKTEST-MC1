from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Leg:
    label: str
    option_type: str
    quantity: int
    target_quantile: float


LEGS = (
    Leg("P35_PE", "PE", 1, 0.35),
    Leg("P20_PE", "PE", -2, 0.20),
    Leg("P65_CE", "CE", 1, 0.65),
    Leg("P80_CE", "CE", -2, 0.80),
)

TARGETS = {
    "P20_PE": 0.20,
    "P35_PE": 0.35,
    "P65_CE": 0.65,
    "P80_CE": 0.80,
}


def expiry_sessions(trading_dates: Iterable[pd.Timestamp], expiry: pd.Timestamp):
    dates = sorted(pd.Timestamp(x).normalize() for x in trading_dates)
    expiry = pd.Timestamp(expiry).normalize()
    idx = next((i for i, d in enumerate(dates) if d == expiry), None)
    if idx is None or idx < 3:
        return None
    signal = dates[idx - 3]
    return signal, dates[idx - 2], dates[idx - 1], expiry


def choose_unique_strikes(
    strikes_by_type: dict[str, np.ndarray],
    quantile_strikes: dict[str, float],
) -> dict[str, float]:
    assigned: set[float] = set()
    result: dict[str, float] = {}
    order = ["P20_PE", "P35_PE", "P65_CE", "P80_CE"]

    for label in order:
        side = "PE" if label.endswith("PE") else "CE"
        candidates = np.asarray(sorted(set(float(x) for x in strikes_by_type[side])), dtype=float)
        if candidates.size == 0:
            raise ValueError(f"No available strikes for {side}")
        target = float(quantile_strikes[label])
        distances = np.abs(candidates - target)
        # Deterministic tie break: lower strike first.
        ranks = np.lexsort((candidates, distances))
        picked = None
        for j in ranks:
            k = float(candidates[j])
            if k not in assigned:
                picked = k
                break
        if picked is None:
            raise ValueError(f"Could not map unique strike for {label}")
        assigned.add(picked)
        result[label] = picked
    return result


def portfolio_payoff(terminal_spot: np.ndarray, strikes: dict[str, float]) -> np.ndarray:
    payoff = np.zeros_like(terminal_spot, dtype=float)
    for leg in LEGS:
        k = strikes[leg.label]
        if leg.option_type == "PE":
            intrinsic = np.maximum(k - terminal_spot, 0.0)
        else:
            intrinsic = np.maximum(terminal_spot - k, 0.0)
        payoff += leg.quantity * intrinsic
    return payoff


def mc_terminal_paths(
    s0: float,
    historical_log_returns: np.ndarray,
    horizon: int,
    paths: int = 5000,
    seed: int = 756,
) -> np.ndarray:
    if s0 <= 0:
        raise ValueError("s0 must be positive")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    hist = np.asarray(historical_log_returns, dtype=float)
    hist = hist[np.isfinite(hist)]
    if hist.size < 756:
        raise ValueError(f"need >=756 historical returns, got {hist.size}")
    hist = hist[-756:]
    rng = np.random.default_rng(seed)
    sample_idx = rng.integers(0, hist.size, size=(paths, horizon))
    sampled = hist[sample_idx]
    terminals = s0 * np.exp(sampled.sum(axis=1))
    return terminals


def signal_spot_from_parity(snapshot: pd.DataFrame, fallback: float) -> tuple[float, str]:
    required = {"strike", "option_type", "close"}
    if not required.issubset(snapshot.columns):
        return float(fallback), "previous_close_fallback"
    x = snapshot.copy()
    x["strike"] = pd.to_numeric(x["strike"], errors="coerce")
    x["close"] = pd.to_numeric(x["close"], errors="coerce")
    x = x[(x["close"] > 0) & x["strike"].notna()]
    ce = x[x.option_type == "CE"][["strike", "close"]].rename(columns={"close": "ce"})
    pe = x[x.option_type == "PE"][["strike", "close"]].rename(columns={"close": "pe"})
    m = ce.merge(pe, on="strike", how="inner")
    if m.empty:
        return float(fallback), "previous_close_fallback"
    m["spot_hat"] = m["strike"] + m["ce"] - m["pe"]
    m = m[np.isfinite(m["spot_hat"]) & (m["spot_hat"] > 0)]
    if m.empty:
        return float(fallback), "previous_close_fallback"
    band = m[np.abs(m["strike"] - fallback) <= 0.02 * fallback]
    if band.empty:
        band = m
    return float(band["spot_hat"].median()), "put_call_parity_snapshot"


def execution_rows(option_window: pd.DataFrame, signal_time: pd.Timestamp, strikes: dict[str, float]):
    rows = []
    x = option_window.copy()
    x["timestamp"] = pd.to_datetime(x["timestamp"], errors="coerce")
    for leg in LEGS:
        sub = x[
            (x["option_type"] == leg.option_type)
            & (pd.to_numeric(x["strike"], errors="coerce") == strikes[leg.label])
            & (x["timestamp"] > signal_time)
        ].copy()
        sub["close"] = pd.to_numeric(sub["close"], errors="coerce")
        if "volume" in sub:
            sub["volume"] = pd.to_numeric(sub["volume"], errors="coerce")
            sub = sub[(sub["close"] > 0) & ((sub["volume"] > 0) | sub["volume"].isna())]
        else:
            sub = sub[sub["close"] > 0]
        if sub.empty:
            return None
        rows.append(sub[["timestamp", "close"]].assign(label=leg.label))
    merged = rows[0]
    for r in rows[1:]:
        merged = merged.merge(r, on="timestamp", how="inner", suffixes=("", "_r"))
    if merged.empty:
        return None
    ts = merged["timestamp"].min()
    prices = {}
    for leg in LEGS:
        col = "close" if leg.label == "P35_PE" else f"close_{leg.label}"
    for leg in LEGS:
        if leg.label == "P35_PE":
            prices[leg.label] = float(merged.loc[merged.timestamp == ts, "close"].iloc[0])
        else:
            # Columns are created sequentially by pandas merge.
            target = rows[0]
            col = None
            for c in merged.columns:
                if c.startswith("close") and c != "close" and c.endswith(leg.label):
                    col = c
            if col is None:
                # Fall back to explicit row lookup; robust to merge suffix differences.
                rr = x[
                    (x["timestamp"] == ts)
                    & (x["option_type"] == leg.option_type)
                    & (pd.to_numeric(x["strike"], errors="coerce") == strikes[leg.label])
                ]
                if rr.empty:
                    return None
                prices[leg.label] = float(rr["close"].iloc[0])
            else:
                prices[leg.label] = float(merged.loc[merged.timestamp == ts, col].iloc[0])
    return ts, prices
