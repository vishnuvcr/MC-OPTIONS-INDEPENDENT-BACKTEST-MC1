# MC1 — 1-Lot Master Candle 09:35 Baseline Results

**Authoritative workflow:** 36523896565  
**Commit:** c45a07e3e6a1f5a83f54f2171ceeae2cd2374326  
**Execution size:** exactly 1 historical NIFTY lot per trade.

## Scope

The baseline used the frozen MC1 interpretation:

- NIFTY 1-minute underlying.
- Master candle 09:35–09:44 IST.
- First 1-minute close beyond master high/low after 09:45.
- Prior completed daily 25-day EMA directional filter.
- Upside breakout: buy ATM CE; downside breakout: buy ATM PE.
- Nearest listed expiry.
- 40% premium stop.
- One trade per session; no re-entry.
- 15:15 time exit.
- Date-effective NIFTY lot-size schedule.
- 1-point adverse slippage per side.
- ₹20 brokerage per executed order in the baseline.
- STT applied on option sale using date-effective rates.

## Yearly baseline results

| Period | Trades | Net P&L (₹) | Win rate | Profit factor | Max DD (₹) | 0-DTE trades | 0-DTE P&L (₹) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2021-05-28–2021-12-30 | 85 | -24,068.70 | 24.71% | 0.730 | -34,049.38 | 22 | -9,500.56 |
| 2022 | 132 | +23,564.79 | 40.15% | 1.186 | -24,004.00 | 26 | +18,813.86 |
| 2023 | 150 | -24,160.23 | 34.67% | 0.820 | -40,249.40 | 31 | -883.25 |
| 2024 | 122 | -78,506.17 | 26.23% | 0.442 | -80,281.77 | 29 | -15,776.57 |
| 2025 | 126 | -45,407.73 | 30.95% | 0.798 | -64,697.34 | 26 | -18,760.03 |
| 2026-01-02–2026-07-01 | 56 | +9,969.77 | 42.86% | 1.103 | -39,685.88 | 10 | +5,228.89 |

**Combined:** 671 executed trades, **-₹1,38,608.27** baseline net P&L.

The 2026 source coverage ends at 2026-07-01 despite the requested 2026-08-04 endpoint; therefore 2026 is a partial-year observation.

## Weekly consistency

Across 258 non-empty trading weeks:

- Mean weekly baseline P&L: **-₹537.24**
- Median weekly baseline P&L: **-₹1,327.26**
- Positive weeks: **34.50%**
- Weeks ≥ ₹5,000: **12.79%**
- Best week: **₹18,606.51**
- Worst week: **-₹12,076.37**

A full-cost sensitivity (current documented NSE statutory/exchange charges plus 18% GST on brokerage/exchange/SEBI charges, 0.003% buyer stamp duty, current ₹20/order brokerage, and the same STT/slippage assumptions) gives approximately **-₹1,46,745.76**, with mean weekly P&L about **-₹568.78** and ≥₹5,000 weeks about **12.02%**. This is a sensitivity, not yet the final historical cost reconstruction.

## Capital / risk observations

For the executed 1-lot trades:

- Mean premium cash outlay including entry slippage: about **₹5,740**.
- Median: about **₹4,685**.
- 95th percentile: about **₹12,889**.
- Maximum observed entry cash outlay: **₹26,231**.
- Maximum theoretical 40%-stop loss plus baseline charges observed: about **₹10,606**.

These are option-premium cash requirements for the modeled long-option strategy, not exchange margin requirements.

## Important integrity findings

- 679 unique signal days generated 738 signal rows; 671 unique executed trades were produced.
- 2021, 2022, 2024 and 2025 each had only 1–2 signal/execution mismatches.
- 2026 had 118 signal rows but only 56 executable trades because the option source currently ends on July 1. This makes 2026 unsuitable for a full-year conclusion.
- No duplicated trading day remains in the consolidated executed ledger.
- No 10-lot scaling was used.

## Interpretation

The frozen baseline does **not** support a positive long-run result over the available 2021–2026 source window. Only 2022 and the partial 2026 sample were positive. 2024 is particularly weak, with a profit factor of 0.442 and approximately ₹80.3k observed sequence drawdown at one lot.

The baseline also does not support a ₹5,000/week consistency objective: only about 12.8% of observed non-empty weeks reached ₹5,000 before the fuller cost sensitivity, and about 12.0% under the fuller sensitivity.

These findings are descriptive results of this specific implementation/data source, not a claim that every possible Master Candle variant is unprofitable.

## Next phase

**MC1 CLOSED — baseline negative discovery.**

**MC2 IN PROGRESS — cost reconstruction + robustness/sensitivity analysis.**

MC2 will test:
1. complete historical Paytm Money/NSE cost schedule;
2. 0.5×, 1× and 2× slippage;
3. breakout-touch vs close-confirmation;
4. EMA interpretation variants;
5. 40% stop sensitivity;
6. time-exit sensitivity;
7. 0-DTE vs non-0-DTE contribution;
8. year/regime stability;
9. walk-forward / holdout robustness;
10. whether any preregistered variant can meet the user's ₹5,000/week target without data-mined retuning.
