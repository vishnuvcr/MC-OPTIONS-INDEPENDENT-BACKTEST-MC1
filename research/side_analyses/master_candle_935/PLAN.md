# Master Candle 09:35–09:45 — Backtest Research Plan

Status: MC0 COMPLETE; MC1 IN PROGRESS — 1-lot runner corrected
Main research track: PAUSED (unchanged)
Side-analysis branch: side-analysis/master-candle-935

## Research objective
Evaluate the NIFTY intraday “09:35–09:45 master candle breakout” strategy described by the user, with explicit option execution, risk, slippage, brokerage, statutory charges, historical contract specifications, and statistical uncertainty.

The study must distinguish: (1) what is explicitly stated in the source material supplied by the user, (2) what is inferred/ambiguous, and (3) what is actually reproduced from historical data.

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
Capture user-supplied rules, identify ambiguities, validate arithmetic consistency of the published claims, and freeze a primary interpretation only after the ambiguity register is explicit.

### Phase MC1 — Historical data acquisition and QA
Status: IN PROGRESS
Primary candidate: 1-minute NIFTY index + option dataset covering approximately 2021–2026. Validate coverage, strike completeness, expiries, timestamps, duplicate keys, missingness, and liquidity. Cross-check selected dates against exchange/public sources where feasible.

### Phase MC2 — Underlying signal engine
Status: NOT STARTED
Construct 09:35–09:45 master candle; apply point-in-time 25-day daily EMA by default interpretation; generate breakout events and directional labels; measure underlying-only signal efficacy.

### Phase MC3 — Option execution engine
Status: NOT STARTED
Resolve ATM definition, nearest-expiry contract rule, entry after 09:45 breakout, 40% premium stop, alternative EMA-based exit, and one-trade-per-session rule unless the frozen specification explicitly says otherwise.

### Phase MC4 — Baseline backtest
Status: NOT STARTED
Run the locked primary rule across all eligible sessions. Apply historical lot sizes and date-effective trading costs. Produce trade-level ledger and daily equity curve.

### Phase MC5 — Robustness and sensitivity
Status: NOT STARTED
Test breakout touch vs close confirmation; stop 30/40/50%; slippage stress; ATM timing; expiry selection; time/EMA exits; and broker/cost alternatives.

### Phase MC6 — Statistical inference and regime analysis
Status: NOT STARTED
Use date-block bootstrap; examine year/month stability; 0DTE vs non-0DTE; India VIX/volatility regime; gap, range-width, trend, and day-of-week conditioning. Treat sensitivity results as descriptive unless pre-registered.

### Phase MC7 — Frozen out-of-sample validation
Status: NOT STARTED
No parameter changes after freeze. Evaluate genuinely unseen dates. Keep 2026 forward period separate from development.

### Phase MC8 — Manuscript and final evidence package
Status: NOT STARTED
Produce manuscript, tables, charts, appendices, data manifest, errors, reproducibility links, and final conclusion.

## Proposed sample split
Development: 2021–2023
Validation: 2024–2025
Frozen forward test: 2026
This split is provisional until dataset coverage and availability are confirmed.

## Stop conditions
The study will not claim reproducible 2021–2026 performance if the historical dataset cannot support that period with documented intraday option observations. A shorter but auditable sample is preferable to silently mixing incompatible sources.
No production-readiness claim will be made from cumulative P&L alone.
