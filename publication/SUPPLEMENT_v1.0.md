# Supplementary Methods and Audit Trail — Publication Version 1.0

## S1. Portfolio payoff

For each leg j:

- Put payoff: max(K_j - S_T, 0)
- Call payoff: max(S_T - K_j, 0)

Portfolio payoff:

`Pi_T = sum(q_j * payoff_j)`

Gross MC-EV:

`MC-EV = mean(Pi_T) - EntryPremium`

Gate:

`MC-EV > 0`

## S2. Primary portfolio

- +1 P35 PE
- -2 P20 PE
- +1 P65 CE
- -2 P80 CE

## S3. Bootstrap and calibration

Primary setting: 756 prior sessions and 5,000 paths with deterministic seed 756.

Revalidation sensitivity: 504, 756 and 1008 historical sessions crossed with 1,000, 5,000 and 10,000 paths.

The 18 total index/scenario combinations are sensitivity/revalidation only and are not used for post hoc index-specific parameter selection.

## S4. Dependence-aware uncertainty

Phase 8 adds expiry-cluster/block-bootstrap uncertainty so that the main interval does not rely only on iid resampling of individual trades.

## S5. ES definitions

Loss is negative realized net P&L.

- VaR95: 95th percentile of loss
- VaR99: 99th percentile of loss
- ES95: mean loss at or beyond VaR95
- ES99: mean loss at or beyond VaR99

## S6. Capital proxy

`C_research = max(abs(ES95) * maximum_concurrent_positions, abs(maximum_drawdown))`

This is a historical P&L-derived reserve and is not exchange SPAN margin.

## S7. Premium cashflow

Long-premium cash outflow is the sum of positive-leg slipped premiums multiplied by historical lot size. Short-premium credit is the absolute value of negative-leg slipped premiums multiplied by historical lot size. Net entry premium cashflow is long outflow minus short credit.

## S8. Margin limitation

NSE states that equity-derivatives initial margin is portfolio-based SPAN and that initial-margin requirements are based on 99% one-day VaR. Paytm Money states that option-writing initial margin comprises SPAN plus exposure margin and that hedge positions can reduce margin requirements.

The Phase 8 trade files do not contain date-specific SPAN risk arrays, exposure parameters or broker margin snapshots. Exact historical broker/exchange margin is therefore not claimed.

## S9. Error control

All material implementation and infrastructure errors remain in `research/logs/ERROR_LOG.md`.

## S10. Publication hierarchy

The publication headline values come from Phase 8 raw-option revalidation and Phase 9 capital interpretation. Historical Phase 7 values are retained only for auditability and are not used as the current headline results.