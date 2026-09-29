# MC1 Baseline Result — Master Candle 09:35, 1 Lot

**Status:** COMPLETE — negative baseline discovery  
**Authoritative GitHub Actions run:** 36522552275  
**Commit:** 49e63c527ef46c5c8e4003b1a4b54817df938314  
**Dataset:** thetrademarkk/india-index-options-1m, revision main  
**Position sizing:** exactly 1 historical NIFTY lot per trade

## Baseline definition

- 09:35–09:44 IST master candle.
- First 1-minute close beyond the master high/low after 09:45.
- Prior completed daily 25-day EMA filter.
- Upside breakout: buy nearest ATM CE.
- Downside breakout: buy nearest ATM PE.
- Nearest listed expiry.
- 40% option-premium stop.
- One trade per session, no re-entry.
- 15:15 time exit.
- Date-effective historical NIFTY lot-size proxy.
- ₹20/order brokerage assumption.
- 1 option-point adverse slippage per side.
- Date-effective option-sale STT assumption.

## Yearly results

| Year | Trades | Net P&L (₹) | Mean/trade (₹) | Win rate | Profit factor | Max DD (₹) | 0-DTE trades | 0-DTE P&L (₹) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021* | 85 | -24,068.70 | -283.16 | 24.71% | 0.730 | -34,049.38 | 22 | -9,500.56 |
| 2022 | 132 | +23,564.79 | +178.52 | 40.15% | 1.186 | -24,004.00 | 26 | +18,813.86 |
| 2023 | 150 | -24,160.23 | -161.07 | 34.67% | 0.820 | -40,249.40 | 31 | -883.25 |
| 2024 | 122 | -78,506.17 | -643.49 | 26.23% | 0.442 | -80,281.77 | 29 | -15,776.57 |
| 2025 | 126 | -45,407.73 | -360.38 | 30.95% | 0.798 | -64,697.34 | 26 | -18,760.03 |
| 2026** | 56 | +9,969.77 | +178.03 | 42.86% | 1.103 | -39,685.88 | 10 | +5,228.89 |
| **Total** | **671** | **-138,608.27** | **-206.57** | **32.94%** | — | — | **144** | **-20,877.66** |

\* 2021 source coverage begins 2021-05-27.  
\*\* 2026 source coverage in this run ends 2026-07-01, despite the requested 2026-08-04 end date.

## Immediate findings

1. Across 671 executed baseline trades, cumulative net P&L is **-₹138,608.27** at one historical lot.
2. The weighted average net result is **-₹206.57/trade**.
3. Only 2022 and the available 2026 sample are positive; 2021, 2023, 2024 and 2025 are negative.
4. The aggregate 0-DTE contribution is **-₹20,877.66** across 144 trades (~21.5% of all trades).
5. Non-0-DTE trades therefore account for approximately **-₹117,730.61**.
6. The observed yearly drawdowns are material relative to one-lot P&L and do not support a claim of stable weekly income.
7. The source's annual coverage is not identical across all calendar years, so the result is a dataset-backed reconstruction, not an exchange-certified reproduction of the video's claimed backtest.

## ₹5,000/week objective

The baseline does not support the requested ₹5,000/week objective at one lot. The aggregate sample is negative before completing the final statutory-cost audit. Additional exchange/regulatory/tax costs would not turn a negative baseline into a positive one.

## Important qualification

This is a **baseline discovery**, not the final manuscript conclusion. MC1 still requires:

- complete Paytm Money historical/current brokerage and statutory-cost reconciliation;
- execution-cost sensitivity;
- breakout-rule sensitivity;
- EMA interpretation sensitivity;
- option-selection/expiry sensitivity;
- data-quality and missing-bar audit;
- walk-forward/holdout analysis where sample coverage permits;
- explicit weekly consistency statistics;
- capital and drawdown analysis;
- comparison with the alternative short-option interpretation.

No video headline result is being treated as independently validated.
