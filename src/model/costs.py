from __future__ import annotations

import pandas as pd


def brokerage_per_order(trade_date: pd.Timestamp) -> float:
    # Paytm Money aligned brokerage to a flat Rs 20 across segments from 15-Jan-2025.
    # The primary study applies Rs 20 per executed entry order throughout the sample;
    # pre-2025 account-vintage alternatives are a robustness sensitivity.
    return 20.0


def stt_sale_rate(trade_date: pd.Timestamp) -> float:
    d = pd.Timestamp(trade_date).date()
    if d < pd.Timestamp("2024-10-01").date():
        return 0.000625
    if d < pd.Timestamp("2026-04-01").date():
        return 0.001
    return 0.0015


def stt_exercise_rate(trade_date: pd.Timestamp) -> float:
    d = pd.Timestamp(trade_date).date()
    if d < pd.Timestamp("2026-04-01").date():
        return 0.00125
    return 0.0015


def entry_slipped_price(mid_or_close: float, quantity: int, slippage_points: float = 2.0) -> float:
    if quantity == 0:
        return float(mid_or_close)
    # Buy pays up; sell receives down.
    return float(mid_or_close + (slippage_points if quantity > 0 else -slippage_points))


def entry_costs(prices: dict[str, float], quantities: dict[str, int], lot_size: int, trade_date: pd.Timestamp) -> dict[str, float]:
    brokerage = 4.0 * brokerage_per_order(trade_date)
    stt = 0.0
    rate = stt_sale_rate(trade_date)
    # STT on sale of options is charged to the seller: the two short legs.
    for label, q in quantities.items():
        if q < 0:
            stt += rate * abs(q) * prices[label] * lot_size
    return {"brokerage": brokerage, "stt_entry": stt}


def expiry_stt(
    expiry_date: pd.Timestamp,
    settlement_spot: float,
    strikes: dict[str, float],
    quantities: dict[str, int],
    lot_size: int,
) -> float:
    rate = stt_exercise_rate(expiry_date)
    stt = 0.0
    # Long ITM options are treated as exercised at expiry for STT purposes.
    for label, q in quantities.items():
        if q <= 0:
            continue
        if label.endswith("PE"):
            intrinsic = max(strikes[label] - settlement_spot, 0.0)
        else:
            intrinsic = max(settlement_spot - strikes[label], 0.0)
        stt += rate * q * intrinsic * lot_size
    return stt


def exchange_transaction_rate_per_crore(underlying: str, trade_date: pd.Timestamp) -> float:
    d = pd.Timestamp(trade_date).date()
    if d < pd.Timestamp("2024-10-01").date():
        raise ValueError("enhanced exchange transaction schedule is not defined before 2024-10-01")
    if underlying == "NIFTY":
        return 3553.0
    if underlying == "SENSEX":
        return 3250.0
    raise ValueError(underlying)


def enhanced_entry_costs(
    underlying: str,
    prices: dict[str, float],
    quantities: dict[str, int],
    lot_size: int,
    trade_date: pd.Timestamp,
    brokerage_override: float | None = None,
) -> dict[str, float]:
    brokerage_rate = brokerage_per_order(trade_date) if brokerage_override is None else float(brokerage_override)
    brokerage = 4.0 * brokerage_rate
    premium_turnover = sum(abs(q) * abs(float(prices[label])) * lot_size for label, q in quantities.items())
    exchange_txn = exchange_transaction_rate_per_crore(underlying, trade_date) / 1e7 * premium_turnover
    sebi = 0.000001 * premium_turnover
    stamp = 0.00003 * sum(max(q, 0) * abs(float(prices[label])) * lot_size for label, q in quantities.items())
    gst = 0.18 * (brokerage + exchange_txn + sebi)
    return {
        "brokerage": brokerage,
        "stt_entry": sum(
            stt_sale_rate(trade_date) * abs(q) * abs(float(prices[label])) * lot_size
            for label, q in quantities.items() if q < 0
        ),
        "exchange_transaction": exchange_txn,
        "sebi_turnover": sebi,
        "stamp_duty": stamp,
        "gst_on_brokerage_and_venue_fees": gst,
        "total_enhanced_entry_cost": brokerage + exchange_txn + sebi + stamp + gst,
    }
