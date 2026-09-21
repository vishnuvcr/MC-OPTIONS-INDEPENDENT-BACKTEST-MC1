# Phase 6 — Robustness Results and Research Interpretation

## Status

Phase 6 produced a complete primary-trade robustness diagnostic from the validated trade-level artifact. The pre-specified MC-calibration sensitivity matrix (504/756/1008 bootstrap windows and 1,000/5,000/10,000 paths) remains implemented as a manual workflow but was infrastructure-blocked by the GitHub Actions runner queue during this research session.

This is therefore **infrastructure-constrained Phase 6**, not a claim that all requested sensitivity dimensions were completed.

## Dataset and sample

Dataset revision: `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`.

The Hugging Face dataset describes the 1-minute intraday option track as NIFTY/SENSEX coverage from October 2024 through 2026 and identifies the source as Upstox historical API candles, while daily history derives from NSE F&O bhavcopy. citeturn948658search0

Validated executed trades:
- NIFTY: 63
- SENSEX: 61

## Primary sample statistics

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Mean net P&L/trade | ₹1,183.66 | ₹2,507.53 |
| Median net P&L/trade | ₹2,149.25 | ₹3,318.19 |
| Std. dev. | ₹10,918.11 | ₹11,114.27 |
| Net profitable share | 66.7% | 77.0% |
| Mean MC-EV | 52.15 pts | 234.74 pts |
| MC-EV/P&L correlation | 0.274 | 0.303 |
| ES95 | -₹30,889.80 | -₹26,807.30 |
| ES99 | -₹38,992.43 | -₹38,352.77 |
| Max sequential drawdown | -₹50,343.72 | -₹66,886.42 |
| Minimum net trade | -₹38,992.43 | -₹38,352.77 |
| Maximum net trade | ₹22,311.80 | ₹28,499.89 |

The sample means are noisy relative to trade-level dispersion. Approximate 95% bootstrap intervals for the mean are:
- NIFTY: -₹1,585 to ₹3,727.
- SENSEX: -₹388 to ₹5,163.

Thus the observed positive sample means are not separated from zero with high precision in this sample.

## Slippage stress

The primary study uses 2 option points per execution leg.

| Slippage/leg | NIFTY mean net | SENSEX mean net |
|---:|---:|---:|
| 0 pts | ₹1,959.27 | ₹2,741.45 |
| 1 pt | ₹1,571.46 | ₹2,624.49 |
| 2 pts | ₹1,183.66 | ₹2,507.53 |
| 3 pts | ₹795.85 | ₹2,390.57 |
| 5 pts | ₹20.24 | ₹2,156.64 |

The stress therefore shows substantial sensitivity for NIFTY to execution quality. At 5 points per leg the NIFTY sample mean is approximately flat, whereas the SENSEX sample remains positive.

The fixed 2-point rule itself contributes approximately ₹776/trade of adverse execution effect for NIFTY and ₹234/trade for SENSEX because the historical lot sizes differ.

## Cost attribution

Average brokerage is ₹80/trade for four entry orders.

Mean entry+expiry STT is approximately:
- NIFTY: ₹37.44/trade.
- SENSEX: ₹40.23/trade.

The remaining primary net-vs-gross difference is dominated by the requested slippage assumption:
- NIFTY mean slippage effect: about ₹776/trade.
- SENSEX mean slippage effect: about ₹234/trade.

This makes execution friction a material component of observed economics rather than a cosmetic adjustment.

## Candidate and gate diagnostics

From the Phase 2 trade/error outputs:

### NIFTY
- 115 D3 candidates encountered.
- 21 lacked a usable pre-09:30 signal snapshot.
- 30 failed gross MC-EV > 0.
- 1 failed unique-strike mapping.
- 63 executed.

### SENSEX
- 105 D3 candidates encountered.
- 13 lacked a usable pre-09:30 signal snapshot.
- 31 failed gross MC-EV > 0.
- 61 executed.

These missing-data cases are retained in the error log rather than silently excluded from the denominator.

## Calendar-year stability

| Year | NIFTY mean net | SENSEX mean net |
|---|---:|---:|
| 2024 | -₹613.87 | -₹1,129.62 |
| 2025 | ₹894.17 | ₹851.63 |
| 2026* | ₹2,106.25 | ₹6,018.63 |

*2026 option coverage ends in July in the pinned intraday source.

Both indices show a negative mean in the short 2024 sub-sample and positive means in 2025 and 2026-to-date. The year effect should therefore not be treated as stable evidence because the sample is short and the 2026 contribution is incomplete.

## Cross-index descriptive comparison

Observed difference in mean net P&L (NIFTY minus SENSEX): -₹1,323.87/trade.

Bootstrap 95% interval for the difference: approximately -₹5,194 to ₹2,513.

The interval spans zero. The trade samples therefore do not support a precise separation of mean net P&L between the two indices.

## External market-context plan

NSE publishes historical index data, historical India VIX, contract-wise price/volume data, F&O daily settlement prices, participant-wise open interest/trading volumes and FII derivatives statistics. citeturn557398search0turn557398search1

NSE's FII/FPI and DII page also notes that the flow data are provisional and may change following custodial confirmation and related adjustments. citeturn557398search4

The Phase 6 design therefore treats VIX/FII/DII/global-market context as explanatory variables rather than new entry rules. The current execution environment did not provide a reliable historical join of all such series to every trade, so these are retained as a future robustness layer rather than fabricated into the present sample.

## Literature context

Recent NIFTY option research continues to emphasize the gap between theoretical volatility premia and realized tradeability after tail risk and implementation frictions. A 2026 NIFTY volatility-risk-premium preprint reports a post-2024 regime break and explicitly models transaction costs. citeturn440012search0 Another 2026 NIFTY study reports negative net returns across several volatility-risk-premium strategies and identifies tail risk as a major driver of losses. citeturn440012search1

The use of ES95/ES99 is consistent with literature that treats expected shortfall as a more informative tail-risk measure than VaR alone. citeturn440012search4turn440012search7

## Phase 6 inference

The locked strategy produced positive sample mean net P&L on the available 2024-10 to 2026-07 option sample for both NIFTY and SENSEX after the requested primary slippage, brokerage, STT and historical lot sizes.

However:
1. confidence intervals around mean P&L include zero;
2. NIFTY economics deteriorate sharply as execution slippage increases;
3. tail losses are large relative to the mean trade outcome;
4. results are concentrated in the incomplete 2025-2026 portion of the sample;
5. the complete MC-calibration sensitivity matrix is still outstanding.

Accordingly, this study does **not** establish that the observed positive mean is a stable or durable trading edge. It establishes a reproducible positive-sample result under the locked primary assumptions, together with clear execution and tail-risk constraints.

## Strengths

- Locked rule specified before final results.
- Chronology-preserving 756-session bootstrap.
- 5,000-path primary MC.
- Explicit MC-EV gate.
- Deterministic unique-strike mapping.
- First-executable post-09:30 execution.
- Historical lot-size handling.
- Explicit 2-point/leg slippage.
- Brokerage and STT modeled.
- Leakage tests and automated validation.
- Separate NIFTY and SENSEX analysis.

## Limitations

- Intraday option history begins in October 2024 in the selected public source. citeturn948658search0
- The source is an aggregation built from Upstox intraday data rather than a direct raw exchange archive. citeturn948658search0
- The underlying bootstrap series uses a secondary public daily source in the production workflow.
- The complete 504/756/1008 × 1,000/5,000/10,000 MC sensitivity matrix could not complete because the GitHub Actions runner queue remained unavailable.
- Historical all-in costs beyond the primary brokerage/STT/slippage model are still a sensitivity rather than the base case.
- Institutional-flow and global-regime joins were not forced when reliable historical synchronized data were unavailable.
- The sample is too small to make precise distributional claims.

## Decision for Phase 7

Proceed to the manuscript with an explicit distinction between:
- **validated primary result**, and
- **outstanding MC-calibration robustness item**.

The manuscript must not describe the strategy as proven, robust, or production-ready.
