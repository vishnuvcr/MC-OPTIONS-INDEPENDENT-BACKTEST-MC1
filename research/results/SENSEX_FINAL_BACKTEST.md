# Phase 5 — SENSEX Backtest

Workflow: Phase 5 run 1  
Dataset revision: 8f7739cab3f38abdcbc6332a6d0a83e1341326e3

## Executed sample

- Executed trades: 61
- Coverage: 2024-10-11 to 2026-07-16
- Gate failures: 31
- Signal snapshot gaps: 13
- Unique-strike failures: none reported in the Phase 2 error summary

## Descriptive results

| Metric | SENSEX |
|---|---:|
| Mean MC-EV (points) | 234.738 |
| Median MC-EV (points) | 136.912 |
| Mean gross P&L (Rs) | 2,861.86 |
| Mean net P&L (Rs) | 2,507.53 |
| Median net P&L (Rs) | 3,318.19 |
| Net profitable trade share | 77.0% |
| Total net P&L | 152,959.12 |
| ES95 (Rs) | -26,807.30 |
| ES99 (Rs) | -38,352.77 |
| Max sequential drawdown (Rs) | -66,886.42 |

## Yearly net P&L

| Year | Trades | Mean net (Rs) | Sum net (Rs) |
|---|---:|---:|---:|
| 2024 | 9 | -1,129.62 | -10,166.60 |
| 2025 | 29 | 851.63 | 24,697.20 |
| 2026* | 23 | 6,018.63 | 138,428.52 |

*Through July 2026 in the available option dataset.

The rule is unchanged from the NIFTY specification.
