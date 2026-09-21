# Phase 6 — Robustness and Cross-Index Analysis

## Locked primary result

Primary strategy parameters remain:
- bootstrap window = 756 sessions
- Monte Carlo paths = 5,000
- gross MC-EV gate > 0
- execution = first executable observation after 09:30 IST
- slippage = 2 option points per leg
- Paytm Money brokerage + STT + historical lot size

## Sensitivity dimensions

### A. Bootstrap window
- 504 sessions
- 756 sessions (primary)
- 1008 sessions

### B. Monte Carlo path count
- 1,000
- 5,000 (primary)
- 10,000

The strategy rule is not optimized across these settings. They are robustness diagnostics only.

### C. Slippage stress
Reprice the executed primary trades at:
- 0 points/leg
- 1 point/leg
- 2 points/leg (primary)
- 3 points/leg
- 5 points/leg

Brokerage/STT are recomputed consistently with the stressed execution premium.

### D. Market-regime conditioning
At the signal date, use information available no later than the prior trading-day close:
- India VIX level and percentile regime.
- S&P 500 prior-day return.
- Cboe VIX prior-day level/return.
- USD/INR prior-day return.
- Gold futures (GC=F) prior-day return.
- NIFTY/SENSEX prior-day return.

These are contextual variables, not additional trading rules.

### E. Institutional-flow audit
NSE exposes FII/FPI & DII trading activity plus participant-wise derivatives reports. The historical interface is documented, but a trade-level historical FII/DII join is not forced when only current/provisional data are retrievable. Using current-only flow data to explain historical trades would create a false historical covariate.

### F. Cross-index comparison
Compare NIFTY and SENSEX on:
- mean/median net P&L
- mean MC-EV
- profitable-trade share
- ES95 / ES99
- maximum sequential drawdown
- bootstrap confidence interval for mean net P&L difference
- sensitivity to slippage and MC calibration

## Statistical methods

- Deterministic bootstrap confidence intervals for mean and median net P&L.
- Welch-style descriptive comparison plus non-parametric rank comparison.
- Scenario-by-scenario robustness tables.
- Regime counts and conditional trade outcomes.
- No p-value-only conclusions.

## Multiplicity

Sensitivity results are descriptive robustness evidence. They are not treated as independent hypothesis tests.

## Stop condition

Phase 6 is complete after:
1. all requested sensitivity scenarios finish for both indices;
2. no unresolved critical validation failures remain;
3. data provenance and unavailable institutional-flow history are explicitly disclosed;
4. cross-index comparison is generated;
5. a research interpretation and limitations note is committed.
