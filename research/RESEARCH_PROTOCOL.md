# Research Protocol

## Research questions

### RQ1 — Economic value
For each eligible D3 expiry observation, does the locked NIFTY BATMAN portfolio have positive gross Monte Carlo expected value (MC-EV), and does realized expiry P&L remain economically meaningful after 2 index-option points of slippage per execution leg, brokerage, STT, and historical lot size?

### RQ2 — Risk
What are the realized return and P&L distributions, ES95, ES99, maximum drawdown, loss frequency, tail loss, and capital usage for NIFTY and SENSEX?

### RQ3 — Stability
How do outcomes vary by calendar year, volatility regime, direction/regime, expiry vintage, and strike-availability condition?

### RQ4 — Robustness
How sensitive are results to:
- bootstrap window: 756 sessions (locked primary; sensitivity only outside primary result)
- Monte Carlo paths: 5,000 (locked primary)
- execution: first executable observation after 09:30
- slippage: 2 points per leg (locked primary)
- cost assumptions
- strike mapping when the exact quantile target is unavailable

### RQ5 — Cross-index comparability
How do NIFTY and SENSEX differ after exchange-specific expiry calendars, strike grids, lot sizes, and trading-cost schedules are correctly applied?

## Aims

1. Produce a reproducible, leakage-controlled historical backtest of the locked rule.
2. Quantify gross and net economics separately.
3. Quantify tail risk using ES95/ES99 and realistic historical contract sizes.
4. Identify data or microstructure constraints that materially affect inference.

## Objectives

- Build an auditable expiry/D3 calendar from actual trading sessions.
- Reconstruct the 09:30+ option snapshot using timestamped observations.
- Generate the 756-session bootstrap terminal distribution using only information available before the signal.
- Map the P20/P35/P65/P80 terminal quantiles to nearest unique listed strikes by option type.
- Apply the exact four-leg portfolio.
- Apply the gross MC-EV gate before execution.
- Execute at the first executable observation after 09:30 IST.
- Exit at actual expiry settlement.
- Apply slippage and costs.
- Report NIFTY and SENSEX independently before pooled comparison.

## Scientific methodology

1. **Eligibility:** identify every historical expiry with sufficient lookback and a valid D3 trading session.
2. **Information set:** only data timestamped at or before the signal can enter the MC input or strike-selection state.
3. **Bootstrap:** resample 756 historical session returns with replacement; form 5,000 terminal paths for the underlying from the signal-time reference level. The exact resampling transform is versioned in code.
4. **Quantiles:** calculate empirical terminal P20/P35/P65/P80 quantiles from the 5,000 terminal paths.
5. **Strike selection:** for each quantile, map to the nearest unique available strike on the corresponding side; enforce uniqueness across the four target strikes.
6. **Portfolio EV:** compute expected expiry portfolio payoff less the entry premium cashflow. The gate is gross MC-EV > 0 before primary execution slippage and trading costs.
7. **Execution:** select the first executable observation after 09:30 IST for all four legs. Executable means valid price/volume/contract record under the selected source's schema.
8. **Exit:** cash-settle each option at the exchange-defined expiry settlement outcome.
9. **Costs:** apply primary slippage of 2 option points per execution leg, brokerage, STT, and historical lot size; all other costs are explicit configuration items.
10. **Sizing:** translate the unscaled strategy return into an ES95/ES99 risk proxy. This is not maximum-profit sizing and must not use future observations.

## Statistical analysis

Primary:
- trade count
- hit rate
- mean/median net P&L
- mean gross MC-EV
- mean realized gross and net P&L
- median and percentile P&L
- cumulative equity curve
- annualized return proxy where a capital series is defensible
- max drawdown
- ES95 and ES99
- bootstrap confidence intervals for mean and median trade P&L
- paired comparison of NIFTY vs SENSEX trade outcomes where date/market conditions permit

Secondary:
- year/regime stratification
- volatility-state stratification
- distributional tests
- sensitivity analysis
- execution and cost stress tests

No result will be called statistically meaningful solely on a p-value. Effect size, uncertainty, sample size, and data quality will be reported together.

## Leakage controls

- No use of post-signal option observations for strike selection.
- No use of post-signal underlying returns in the terminal-distribution fit.
- No use of future lot size, expiry, or contract availability information beyond contract metadata known at the signal.
- Every trade stores a provenance hash/version for its inputs.

## Data provenance priorities

1. NSE/BSE exchange data and circulars.
2. Independent public datasets with clear schema/provenance.
3. Secondary vendor data only when required for missing intraday history.
4. All deviations from primary sources must be documented.

## Development-history rule

The final locked specification is immutable, but scientific status depends on how it was selected. Any earlier joint tuning of entry day, entry time, exit method, bootstrap settings, or related parameters must be disclosed. Historical results produced after research-stage selection are not described as independently out-of-sample unless validation dates were genuinely unseen during development.

## Required chronology audit

The MC-EV gate must use information available at the 09:30 signal cut-off. The premium used by the gate must be identified by timestamp and cannot be selected from the later execution observation.

## Dependence-aware uncertainty

Primary uncertainty must include expiry-cluster/block bootstrap or an equivalent chronology-preserving resampling method. Trade-level iid bootstrap remains a descriptive secondary analysis. NIFTY/SENSEX comparison should use paired differences on comparable dates where the design permits.

## Execution realism

The 2-point-per-leg slippage assumption is a research stress assumption, not a validated market-impact estimate. Where executable bid/ask data permit, spread/fill sensitivity should be reported separately.

## Stop conditions

The research stops after the approved methodological revalidation phase. A result can be reported only if the critical validation suite passes and all material data gaps are disclosed. No new parameter optimization is introduced by this corrective phase.
