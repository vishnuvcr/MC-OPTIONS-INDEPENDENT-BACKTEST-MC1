# Phase 4 — NIFTY Backtest

Workflow: Phase 4 run 3  
Dataset revision: 8f7739cab3f38abdcbc6332a6d0a83e1341326e3

## Executed sample

- Executed trades: 63
- Coverage: 2024-10-10 to 2026-07-21
- Gate failures: 30
- Signal snapshot gaps: 21
- Strike-mapping failures: 1

## Descriptive results

| Metric | NIFTY |
|---|---:|
| Mean MC-EV (points) | 52.146 |
| Median MC-EV (points) | 27.443 |
| Mean gross P&L (Rs) | 2,077.29 |
| Mean net P&L (Rs) | 1,183.66 |
| Median net P&L (Rs) | 2,149.25 |
| Net profitable trade share | 66.7% |
| Total net P&L (Rs) | 74,570.44 |
| ES95 (Rs) | -30,889.80 |
| ES99 (Rs) | -38,992.43 |
| Max sequential drawdown (Rs) | -50,343.72 |

## Yearly net P&L

| Year | Trades | Mean net (Rs) | Sum net (Rs) |
|---|---:|---:|---:|
| 2024 | 8 | -613.87 | -4,910.92 |
| 2025 | 30 | 894.17 | 26,825.00 |
| 2026* | 25 | 2,106.25 | 52,656.36 |

*Through July 2026 in the available option dataset.

This is the locked rule with the primary 2-point-per-leg slippage, brokerage, STT, and historical lot-size model. No parameter optimization was applied.
