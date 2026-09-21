# Phase 9 — Capital, Margin Proxy, and Return Analysis

## Trigger
User requested capital-required and return-percentage interpretation for both NIFTY and SENSEX using the locked Phase 8 primary result.

## Scope lock
This phase does not change the BATMAN rule, MC calibration, strike mapping, execution rule, slippage, cost model, or primary sample. It uses the existing Phase 8 primary 756-session / 5,000-path trade-level outputs for NIFTY and SENSEX.

The phase has a finite scope:
1. quantify entry premium cash requirements;
2. quantify historical loss, VaR95/VaR99, ES95/ES99 and maximum drawdown;
3. quantify simultaneous-position overlap;
4. define a conservative research capital proxy from observed tail risk and observed drawdown;
5. calculate per-trade and simple annualized P&L-to-capital ratios;
6. distinguish these research proxies from actual broker/exchange SPAN margin;
7. record the exact data gap for a future exchange-margin reconstruction without changing the strategy.

## Research questions

### RQ9.1 — Capital
What capital reserve is implied by the Phase 8 historical P&L distribution for one BATMAN position and for the observed maximum number of simultaneous BATMAN positions?

### RQ9.2 — Cash-flow
How large are the long-option premium outlays, short-option premium receipts, and net entry premium cashflows per BATMAN?

### RQ9.3 — Return
What is the mean net P&L as a percentage of (a) ES95 risk capital per position and (b) a conservative capital proxy that also covers observed drawdown and simultaneous-position overlap?

### RQ9.4 — Broker/exchange margin
Can the study claim an actual Paytm Money/NSE/BSE margin requirement from the available Phase 8 data? If not, what is the exact limitation?

## Aims
1. Translate Phase 8 P&L into capital-aware, user-readable quantities for both indices.
2. Avoid calling a risk proxy an exchange or broker margin figure.
3. Provide transparent return percentages with explicit denominators.
4. Establish a reproducible bridge to an eventual historical SPAN-margin reconstruction.

## Objectives
- Reuse the immutable Phase 8 primary trade outputs.
- Compute premium cash-flow statistics from the recorded execution prices, quantities and lot sizes.
- Compute loss quantiles, ES95/ES99, maximum drawdown, and maximum concurrent positions.
- Compute the worst observed combined P&L across overlapping positions.
- Define ES95 capital proxy per position as absolute ES95 loss.
- Define observed-drawdown reserve as absolute maximum historical drawdown for one-unit trading.
- Define conservative research capital proxy as max(ES95 × maximum concurrent positions, observed-drawdown reserve).
- Report mean net P&L divided by ES95.
- Report mean net P&L divided by the conservative research capital proxy.
- Report simple linear annual P&L divided by the conservative research capital proxy.
- Report the same return ratios under Phase 8 enhanced friction as a robustness check.
- Document that actual historical broker margin is not reconstructed in this phase.

## Scientific methodology

### Input
Phase 8 artifact: phase8-final, artifact ID 10659054480.
Primary files: data/processed/phase8/nifty/scenarios/nifty_w756_p5000.csv and data/processed/phase8/sensex/scenarios/sensex_w756_p5000.csv.

### Premium cash-flow reconstruction
For each trade and each lot:
- Long-premium cash outflow = sum of positive leg quantities × slipped entry price × historical lot size.
- Short-premium credit = sum of absolute negative leg quantities × slipped entry price × historical lot size.
- Net premium cashflow = long-premium outflow − short-premium credit.
A negative net premium cashflow represents a net credit at entry. This is not treated as required capital because short-option margin is still required.

### Loss distribution
Define loss = − realized net P&L.
Report VaR95, VaR99, ES95 and ES99.

### Drawdown
Construct the sequential cumulative net-P&L series in chronological trade order and compute maximum peak-to-trough drawdown.

### Concurrency
Treat each trade as active from signal date through expiry date. Determine maximum simultaneous active positions and the worst combined realized P&L over overlapping active positions.

### Capital proxies
1. ES95 capital proxy: |ES95|.
2. Observed-drawdown reserve: |maximum drawdown|.
3. Conservative research capital proxy: max(|ES95| × max_concurrent_positions, |maximum_drawdown|).
This is a research reserve, not a broker margin requirement.

### Return calculations
Per-trade risk-return ratio = mean net P&L / |ES95|.
Capital-proxy return per trade = mean net P&L / conservative research capital proxy.
Observed annual trade-frequency estimate = executed trades / elapsed years between first and last expiry.
Simple linear annual P&L = mean net P&L × observed annual trade frequency.
Simple linear annualized capital-proxy ratio = simple linear annual P&L / conservative research capital proxy.
These annual figures are turnover-normalized ratios, not compounded portfolio returns. They assume capital can be reused and do not claim a guaranteed annual return.

## Margin-source interpretation
NSE Clearing documents that equity-derivatives initial margin is computed using portfolio-based SPAN, with a 99% VaR framework and additional exposure components. Paytm Money states that option-writing margin is exchange-defined and its margin calculator incorporates SPAN + exposure and hedge benefits. Therefore the backtest trade files alone do not identify the exact historical broker margin at each entry timestamp.
This phase may state risk-capital proxies and cash requirements, but it must not call them Paytm Money margin or NSE margin.

## Acceptance criteria
- NIFTY and SENSEX both processed from the same locked Phase 8 primary scenario.
- Premium cashflow, ES95/ES99, drawdown, concurrency, and capital proxies are reported.
- Return percentages identify the denominator explicitly.
- Actual broker/exchange margin is not invented.
- Workflow is manually runnable and also executes on the Phase 9 PR.
- Results, errors, source audit, and status are committed to the Phase 9 branch.
- README and final conclusion are updated after successful workflow validation.

## Status
Implementation created; numerical results are accepted only from the Phase 9 GitHub Actions run.