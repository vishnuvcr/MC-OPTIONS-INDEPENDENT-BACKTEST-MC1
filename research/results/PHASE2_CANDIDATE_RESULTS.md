# Phase 2 Candidate Backtest Results

Artifact: GitHub Actions run 14, artifact ID 10654231266  
Dataset revision: `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`

## Coverage

- NIFTY executed trades: 63
- SENSEX executed trades: 61
- NIFTY trade coverage: 2024-10-10 through 2026-07-21
- SENSEX trade coverage: 2024-10-11 through 2026-07-16
- The sample is constrained by the available 1-minute option dataset and is not a full pre-2024 history.

## Gate / data exclusions

- NIFTY: 30 candidates failed gross MC-EV > 0.
- SENSEX: 31 candidates failed gross MC-EV > 0.
- NIFTY: 21 D3 expiry candidates lacked a usable pre-09:30 signal snapshot.
- SENSEX: 13 D3 expiry candidates lacked a usable pre-09:30 signal snapshot.
- NIFTY: 1 candidate failed unique-strike mapping.

These exclusions are recorded as data/model eligibility outcomes, not silently dropped.

## Executed-trade economics

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Executed trades | 63 | 61 |
| Mean MC-EV (index points) | 52.146 | 234.738 |
| Median MC-EV | 27.443 | 136.912 |
| Mean gross P&L (Rs) | 2,077.29 | 2,861.86 |
| Mean net P&L (Rs) | 1,183.66 | 2,507.53 |
| Median net P&L (Rs) | 2,149.25 | 3,318.19 |
| Net profitable trade share | 66.7% | 77.0% |
| Gross profitable trade share | 79.4% | 77.0% |
| Net P&L sum (Rs) | 74,570.44 | 152,959.12 |
| Net ES95 (Rs) | -30,889.80 | -26,807.30 |
| Net ES99 (Rs) | -38,992.43 | -38,352.77 |
| Max drawdown, sequential trades (Rs) | -50,343.72 | -66,886.42 |

## Calendar-year net P&L

| Year | NIFTY trades | NIFTY mean net | SENSEX trades | SENSEX mean net |
|---|---:|---:|---:|---:|
| 2024 | 8 | -613.87 | 9 | -1,129.62 |
| 2025 | 30 | 894.17 | 29 | 851.63 |
| 2026* | 25 | 2,106.25 | 23 | 6,018.63 |

*2026 coverage ends in July in the current option dataset.

## Interpretation status

These are **candidate descriptive backtest results**, not a final inference. Phase 3 still needs leakage checks, deterministic invariants, statistical uncertainty, and execution/cost validation before the strategy can be considered fully validated.
