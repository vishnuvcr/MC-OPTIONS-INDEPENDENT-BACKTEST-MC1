# Final Research Conclusion — Phase 8 Revalidation

## Current status

Phase 8 methodological revalidation is complete. The full raw-option calibration matrix was executed successfully on the pinned dataset revision `8f7739cab3f38abdcbc6332a6d0a83e1341326e3` in authoritative GitHub Actions run `35641908887`. The locked BATMAN strategy itself was not changed.

The earlier Phase 7 numerical results remain preserved as a historical baseline. Phase 8 is the current methodological result because it reruns the full raw-option chain after the chronology, contract-cost, execution-audit, and dependence-aware inference corrections.

## Calibration-setting decision

The study uses one common locked primary setting for both indices:

- **Bootstrap window:** 756 historical sessions
- **Monte Carlo paths:** 5,000

The 504/756/1008 × 1,000/5,000/10,000 matrix is a sensitivity/revalidation exercise. It is **not** used to select different settings for NIFTY and SENSEX. Choosing the highest historical mean separately for each index would be post hoc tuning. Any future instrument-specific calibration must be selected by a pre-registered rule using development data and evaluated on genuinely unseen expiries.

## Validated Phase 8 primary result

Under the common 756/5,000 calibration:

- **NIFTY:** 63 executed trades; mean net P&L **₹966.46/trade**; enhanced-friction mean **₹936.45/trade**; ES95 **-₹31,753.75**.
- **SENSEX:** 61 executed trades; mean net P&L **₹2,508.06/trade**; enhanced-friction mean **₹2,478.65/trade**; ES95 **-₹26,807.30**.

Block-bootstrap 95% confidence intervals for the mean net P&L include zero:

- NIFTY: **₹-1,985.18 to ₹3,955.42**
- SENSEX: **₹-479.84 to ₹5,530.85**

## Calibration sensitivity

NIFTY's nine tested configurations ranged from approximately **₹13 to ₹1,469 mean net P&L/trade**, showing substantial sensitivity to calibration choices.

SENSEX remained positive in all nine configurations, ranging from approximately **₹1,641 to ₹2,773/trade**.

This is a robustness finding, not a basis for selecting different production settings from the same sample.

## Other Phase 8 audits

- Gate timestamp validity: 100% for both indices in the primary scenario.
- Execution-after-signal validity: 100%.
- All four execution-leg volumes observed and positive: 100%.
- Final strike uniqueness: 100%.
- Exact theoretical-target strike matches: 0%.
- Mean absolute strike displacement: 12.14 NIFTY points; 24.83 SENSEX points.
- Maximum displacement: 24.90 NIFTY points; 97.86 SENSEX points.
- Paired NIFTY/SENSEX inference: not performed because only one common signal date was available.

The 2-point-per-leg slippage assumption remains a research stress assumption rather than a validated estimate of live four-leg market impact or simultaneous fills.

## Scientific conclusion

The study establishes a reproducible historical sample with positive means under the locked primary assumptions, but the uncertainty intervals include zero, the tail losses are substantial, and NIFTY is materially calibration-sensitive. The evidence does not establish a stable population-level or production-ready trading edge.

## Strengths

- Full raw-option calibration revalidation across 18 scenarios.
- Chronology/leakage audit.
- Dependence-aware block-bootstrap uncertainty.
- Explicit execution-volume and strike-mapping diagnostics.
- Historical contract/lot-size and cost-date corrections.
- Separate NIFTY and SENSEX analysis with no post hoc index-specific parameter selection.

## Limitations

- The intraday option source begins in October 2024 and is not a complete long-run exchange-native history.
- The sample contains only 124 executed trades across both indices.
- The confidence intervals include zero.
- The fixed 2-point/leg slippage model is a stress assumption.
- Only one common signal date was available for paired cross-index inference.
- Full synchronized historical India VIX/FII-DII/global-market regime conditioning was outside the approved Phase 8 execution scope.
- No genuinely unseen prospective validation has yet been performed.

## Future direction

The next research phase should be a prospective frozen validation: no retuning, no index-specific calibration selection, and no use of post-signal information. After that, exchange-grade historical extension and synchronized regime analysis can be added as separate pre-specified phases.

## Repository references

- Phase 8 results: `research/PHASE8_RESULTS.md`
- Phase 8 plan: `research/PHASE8_METHODOLOGICAL_REVALIDATION_PLAN.md`
- Prospective protocol: `research/PROSPECTIVE_FROZEN_VALIDATION_PROTOCOL.md`
- Error log: `research/logs/ERROR_LOG.md`
- Research log: `research/logs/RESEARCH_LOG.md`
- Full manuscript: `research/manuscript/NIFTY_BATMAN_MANUSCRIPT.md`

## Phase 9 — Capital and return interpretation

Phase 9 translates the Phase 8 primary trade results into capital-aware quantities without changing the strategy. NIFTY mean net P&L is ₹966.46 per trade against an ES95 loss proxy of ₹31,753.75; the observed maximum drawdown is ₹61,576.41 and the observed maximum simultaneous position count is two. The resulting conservative research capital proxy is ₹63,507.51. SENSEX mean net P&L is ₹2,508.06 per trade against ES95 of ₹26,807.30; observed maximum drawdown is ₹66,886.42 and maximum simultaneous count is two, giving a conservative research capital proxy of ₹66,886.42.

Using one-position ES95 as denominator, mean P&L/ES95 is 3.04% for NIFTY and 9.36% for SENSEX. Using the more conservative capital proxy, the per-trade ratios are 1.52% and 3.75%. These are risk-capital ratios, not returns on broker margin. The simple linear annualized ratios of 53.96% and 129.93% are turnover-normalized historical calculations, not compounded forecasts.

Average net entry premium cashflow is a credit of ₹2,957.76 for NIFTY and ₹4,686.03 for SENSEX, but this does not eliminate capital requirements because the short options require exchange-defined margin.

Actual historical Paytm Money/NSE/BSE margin is not reconstructed here because the Phase 8 trade files do not contain date-specific SPAN risk arrays, exposure-margin parameters, or broker margin snapshots. See `research/PHASE9_RESULTS.md` and `research/data/PHASE9_CAPITAL_MARGIN_SOURCE_AUDIT.md`.
