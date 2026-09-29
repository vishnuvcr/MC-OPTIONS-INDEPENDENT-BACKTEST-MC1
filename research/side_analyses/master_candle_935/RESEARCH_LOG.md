[object Object]
## 2026-09-29 — MC1 closure
- Authoritative workflow 36523896565 completed all six yearly workers successfully.
- 1-lot baseline consolidated: 671 executed trades, -₹138,608.27 baseline net P&L.
- Weekly test: 258 non-empty weeks; 34.50% positive; 12.79% reached ≥₹5,000.
- 2026 is partial through 2026-07-01 in the selected data source.
- MC1 closed as negative discovery; MC2 opened for full cost reconstruction and robustness.

## 2026-09-29 — MC2 cost robustness
- Workflow 36524250868 completed successfully using frozen MC1 ledgers.
- Primary full-cost scenario: negative ₹146,774.55 over 671 trades; profit factor 0.820; 33.72% positive weeks; 12.02% weeks at or above ₹5,000.
- Slippage sensitivity at 0.5/1/2 points per side remained negative.
- Brokerage sensitivity at ₹10/₹15/₹20 per order remained negative.
- MC2 cost block closed; execution-rule robustness block started.

## 2026-09-29 — MC2 execution grid calculation
- Workflow 36524818652 completed all 18 variant calculation jobs and all 18 artifact uploads successfully.
- Aggregate job failed before producing the grid because `aggregate_mc2_execution.py` did not discover the downloaded summary files with its shallow glob and then attempted to sort an empty DataFrame.
- No variant is accepted as selected/promoted. The aggregation defect is being repaired with recursive discovery plus an 18-row completeness assertion.