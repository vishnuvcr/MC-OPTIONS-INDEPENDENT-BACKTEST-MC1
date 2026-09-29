# Master Candle 09:35–09:45 — Backtest Research Plan

Status: MC0 COMPLETE; MC1 COMPLETE — negative baseline discovery; MC2 COST COMPLETE; MC2 EXECUTION GRID CALCULATION COMPLETE — aggregation rerun required
Main research track: PAUSED (unchanged)
Side-analysis branch: side-analysis/master-candle-935-mc2

## Research objective
Evaluate the NIFTY intraday “09:35–09:45 master candle breakout” strategy described by the user, with explicit option execution, risk, slippage, brokerage, statutory charges, historical contract specifications, and statistical uncertainty.

## Research questions
1. Does the 09:35–09:45 NIFTY master-candle breakout produce positive directional expectancy before and after option execution friction?
2. Does a 25-day EMA filter materially change breakout outcomes?
3. Does the option layer add positive expectancy beyond the underlying breakout signal?
4. How do results vary by DTE, especially 0DTE versus non-0DTE?
5. How sensitive are results to breakout confirmation, option strike selection, expiry selection, stop-loss execution, and slippage?
6. Are the published video-level performance claims internally reproducible from a point-in-time dataset?
7. What capital measure is actually required: premium cash, worst-case loss reserve, concurrent-position reserve, broker/exchange margin, or some combination?

## Aims
- Reconstruct the strategy into an executable, chronology-safe specification.
- Test the underlying signal separately from the option implementation.
- Quantify net P&L after realistic, date-effective costs.
- Decompose results by expiry proximity, volatility regime, trend regime, and breakout characteristics.
- Produce confidence intervals and tail-risk measures rather than relying on cumulative P&L alone.
- Freeze one primary specification before any out-of-sample evaluation.

## Objectives
- Use 1-minute NIFTY underlying and option observations wherever available.
- Resolve historical NIFTY lot sizes and expiry dates from date-effective contract metadata.
- Avoid any post-signal information in the EMA, strike selection, expiry selection, or trade gate.
- Model entry/exit slippage explicitly and stress it.
- Report gross, cost, and net P&L separately.
- Report max drawdown, ES95/ES99, consecutive losses, monthly hit rate, profit factor, and trade-level dispersion.
- Split development, validation, and forward periods before performance conclusions are made.

## Planned phases
### Phase MC0 — Source/specification audit
Status: COMPLETE

### Phase MC1 — Historical data acquisition and QA
Status: COMPLETE
Authoritative one-lot baseline run 36523896565: 671 executed trades, -₹138,608.27 net; 2026 source coverage through 2026-07-01.

### Phase MC2 — Cost/friction and execution-rule robustness
Status: COST COMPLETE; 18-VARIANT EXECUTION GRID CALCULATIONS COMPLETE; AGGREGATION RERUN PENDING
Cost workflow 36524250868 is authoritative for the primary full-cost audit. Execution workflow 36524818652 completed all 18 variant calculations and uploads, but its aggregate job failed on an aggregator path/schema defect. No variant is promoted or ranked as a winner.

### Phase MC3 — Underlying signal decomposition
Status: NOT STARTED
Separate underlying breakout efficacy from option implementation, including EMA-on/off and point-in-time signal metrics.

### Phase MC4 — Option execution and baseline reconstruction
Status: NOT STARTED
Lock the primary option execution specification and reproduce the baseline with the final cost stack.

### Phase MC5 — Statistical inference and regime analysis
Status: NOT STARTED
Date-block bootstrap, year/month stability, 0DTE vs non-0DTE, volatility/trend/gap/range conditioning, and tail-risk analysis.

### Phase MC6 — Frozen out-of-sample validation
Status: NOT STARTED
No parameter changes after freeze; evaluate unseen dates.

### Phase MC7 — Manuscript and final evidence package
Status: NOT STARTED
Manuscript, charts, tables, appendices, data manifest, errors, reproducibility links, and final conclusion.

## Proposed sample split
Development: 2021–2023
Validation: 2024–2025
Frozen forward test: 2026, limited to source coverage

## Stop conditions
The study will not claim reproducible 2021–2026 performance if the historical dataset cannot support that period with documented intraday option observations. No production-readiness claim will be made from cumulative P&L alone.

## Current execution-grid gate
All 18 predefined variants must be aggregated successfully before MC2 execution robustness can close. The grid is descriptive; no historical winner is selected.