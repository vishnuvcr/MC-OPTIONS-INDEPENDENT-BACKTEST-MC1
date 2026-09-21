# BATMAN Development and Validation History

## Purpose

This file separates strategy development from evaluation. It is a scientific provenance record, not a trading recommendation.

## Development / tuning phase

Earlier BATMAN research jointly evaluated entry day, entry timing, and exit methodology before the final rule was frozen. Those choices were research-stage decisions and therefore create a model-selection history.

## Rule freeze

The current immutable BATMAN specification is:

- D3 trading session before expiry
- 09:30 IST information cut-off
- 756-session bootstrap Monte Carlo
- 5,000 terminal paths
- gross MC-EV > 0 gate
- P20/P35/P65/P80 terminal quantiles mapped to nearest unique available strikes
- +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE
- first common executable observation strictly after 09:30
- expiry exit
- primary 2-point-per-leg slippage
- brokerage + STT + historical lot size

No additional parameter optimization is introduced by Phase 8.

## Historical locked-rule evaluation

The existing 63 NIFTY and 61 SENSEX trade results are retained as locked-rule historical sample results. They are not labeled independently out-of-sample unless a date split demonstrates that the evaluation observations were unavailable during development.

## Prospective validation

A future genuinely unseen expiry set should be frozen before execution and evaluated without re-estimation. The Phase 8 manuscript amendment uses this distinction explicitly.
