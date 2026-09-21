# Supplementary Methods and Audit Trail

## S1. Portfolio payoff

For each leg q_j, strike K_j, and terminal index level S_T:

- Put payoff: max(K_j - S_T, 0)
- Call payoff: max(S_T - K_j, 0)

Portfolio payoff:

`Pi_T = sum_j q_j * payoff_j(S_T, K_j)`

Gross MC-EV:

`MC-EV = mean(Pi_T) - EntryPremium`

The gate is `MC-EV > 0`.

## S2. Primary four-leg structure

- Long P35 PE: +1
- Short P20 PE: -2
- Long P65 CE: +1
- Short P80 CE: -2

## S3. Slippage

A buy leg pays `p + 2` option points.

A sell leg receives `p - 2` option points.

For four legs, the point-level adverse execution effect is 8 option points before translating through the historical lot size.

## S4. Historical lot sizes

NIFTY:
- 2024 sample contracts: 25 units.
- 2025 sample contracts: 75 units.
- 2026 sample contracts in the current dataset: 65 units.

SENSEX:
- 2024 sample spans 10- and 20-unit regimes.
- 2025-2026 sample contracts use 20 units.

## S5. Candidate denominators

NIFTY:
`63 executed + 30 gate failures + 1 strike failure + 21 signal-data gaps = 115 candidates`.

SENSEX:
`61 executed + 31 gate failures + 13 signal-data gaps = 105 candidates`.

## S6. Statistical uncertainty

The primary uncertainty interval for the mean is a nonparametric trade-bootstrap interval with 20,000 resamples and seed 20260921.

This interval quantifies uncertainty in the empirical trade sample. It does not correct for nonstationarity, regime change, or data-source uncertainty.

## S7. ES calculation

ES95 is calculated as the average of trade P&L observations at or below the empirical 5th percentile.

ES99 is calculated as the average of observations at or below the empirical 1st percentile.

With 61-63 trades, ES99 is effectively driven by the single most adverse observation. It should therefore be interpreted as a tail-loss indicator, not as a highly precise population estimate.

## S8. Gate and execution ordering

The engine sequence is:

1. construct historical return window;
2. simulate terminal paths;
3. calculate terminal quantiles;
4. map strikes;
5. calculate signal premiums;
6. calculate gross MC-EV;
7. reject if MC-EV <= 0;
8. locate first common executable timestamp after 09:30;
9. apply slippage;
10. hold to expiry;
11. apply brokerage/STT/lot size.

This ordering prevents post-entry information from influencing the gate.

## S9. Audit of errors resolved

All discovered implementation errors are recorded in `research/logs/ERROR_LOG.md`.

The most material production-code correction was the four-leg execution join and timestamp normalization, which changed the initial zero-trade result into the validated executed sample.

## S10. Reproduction artifacts

- Primary NIFTY trade CSV: GitHub Actions Phase 4 artifact.
- Primary SENSEX trade CSV: GitHub Actions Phase 5 artifact.
- Primary Phase 2 artifact: GitHub Actions run 14.
- Dataset revision: `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`.

## S11. Outstanding robustness workflow

The manual Phase 6 workflow remains in:

`.github/workflows/phase-6-robustness.yml`

It contains exact replays for:
- 504 / 756 / 1008 bootstrap sessions;
- 1,000 / 5,000 / 10,000 MC paths.

Those scenarios must be run from raw option data because they can change the gate and strike-selection outcome.
