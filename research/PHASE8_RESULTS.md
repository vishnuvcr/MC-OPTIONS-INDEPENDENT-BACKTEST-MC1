# Phase 8 — Raw-Option MC Revalidation Results

Run: 35641908887
Dataset revision: 8f7739cab3f38abdcbc6332a6d0a83e1341326e3
Status: completed successfully

## Primary 756-session / 5,000-path result

| Index | Executed trades | Mean net P&L | Mean net P&L with enhanced friction | Block-bootstrap 95% CI | ES95 |
|---|---:|---:|---:|---:|---:|
| NIFTY | 63 | ₹966.46 | ₹936.45 | ₹-1,985.18 to ₹3,955.42 | ₹-31,753.75 |
| SENSEX | 61 | ₹2,508.06 | ₹2,478.65 | ₹-479.84 to ₹5,530.85 | ₹-26,807.30 |

The block-bootstrap confidence intervals for mean net P&L include zero for both indices.

## Calibration sensitivity

### NIFTY — mean net P&L (₹/trade)

| Window | 1,000 paths | 5,000 paths | 10,000 paths |
|---|---:|---:|---:|
| 504 | 349.83 | 13.11 | 84.45 |
| 756 | 1,468.59 | 966.46 | 409.98 |
| 1008 | 1,228.30 | 553.63 | 607.63 |

### SENSEX — mean net P&L (₹/trade)

| Window | 1,000 paths | 5,000 paths | 10,000 paths |
|---|---:|---:|---:|
| 504 | 1,640.50 | 1,645.82 | 1,794.45 |
| 756 | 2,050.82 | 2,508.06 | 2,426.82 |
| 1008 | 2,132.92 | 2,579.47 | 2,773.43 |

The primary NIFTY result is materially sensitive to calibration choice; the SENSEX result is positive across all nine tested configurations.

## Calibration-setting policy

The study retains one common locked primary calibration for both indices: **756 historical sessions × 5,000 MC paths**. The 18-scenario matrix is a sensitivity/revalidation analysis, not a parameter-selection exercise. Although the highest observed sample mean differs across the tested settings, selecting an index-specific setting from these same historical outcomes would be post hoc tuning and is therefore not adopted. Any future instrument-specific calibration must be selected by a pre-registered rule using development data and then evaluated on genuinely unseen expiries.

## Execution and gate audits

For the primary scenario:
- Gate timestamp validity: 100% for both indices.
- Execution after signal: 100% for both indices.
- All four execution-leg volumes observed: 100%.
- All four execution-leg volumes positive: 100%.
- Final strike uniqueness: 100%.
- Exact four-target strike match: 0%.
- Mean absolute strike displacement: 12.14 NIFTY points; 24.83 SENSEX points.
- Maximum absolute strike displacement: 24.90 NIFTY points; 97.86 SENSEX points.

The absence of exact target strikes is expected under nearest-available-strike mapping, but the displacement should be treated as an execution/modeling sensitivity rather than ignored.

## Cross-index pairing

The paired-date analysis returned only 1 common signal date in the primary files and therefore reported insufficient_common_signal_dates. No paired cross-index inference is made.

## Cost sensitivity

At ₹10/₹15/₹20 brokerage per order:
- NIFTY mean net: ₹1,006.46 / ₹986.46 / ₹966.46.
- SENSEX mean net: ₹2,548.06 / ₹2,528.06 / ₹2,508.06.

## Interpretation

Phase 8 confirms that the raw-option implementation can execute the full 18-scenario calibration matrix and that the locked primary configuration produces positive sample mean net P&L in both indices after the specified 2-point-per-leg slippage and baseline costs. However, the block-bootstrap intervals include zero, and NIFTY's mean is sensitive to MC calibration parameters. These results are sample evidence, not independent proof of future profitability.

No strategy retuning was performed in Phase 8.