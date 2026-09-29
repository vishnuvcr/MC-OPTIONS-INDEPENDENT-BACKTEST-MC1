# MC2 — Cost and Slippage Robustness

**Authoritative workflow:** 36524250868  
**Input:** frozen MC1 trade ledgers from workflow 36523896565.

## Primary current-cost scenario

- Execution: 1 historical NIFTY lot.
- Slippage: 1.0 option point adverse on each side.
- Paytm Money brokerage: ₹20 per executed order.
- STT: date-effective.
- NSE equity-option transaction charge: 0.03552% of premium turnover per side for the current standardized sensitivity.
- SEBI turnover fee: 0.0001% of premium turnover.
- Buyer stamp duty: 0.003% on option purchase premium.
- GST: 18% on brokerage + exchange + SEBI charges.

### Result

| Metric | Result |
|---|---:|
| Trades | 671 |
| Net P&L | **-₹1,46,774.55** |
| Mean/trade | **-₹218.74** |
| Win rate | **32.94%** |
| Profit factor | **0.820** |
| Max observed trade loss | **-₹8,224.25** |
| Sequence max drawdown | **-₹1,69,015.16** |
| Positive weeks | **33.72%** |
| Weeks ≥ ₹5,000 | **12.02%** |
| Mean weekly P&L | **-₹568.89** |
| Median weekly P&L | **-₹1,349.77** |
| 0-DTE trades | **144** |
| 0-DTE net P&L | **-₹22,250.29** |

### Slippage sensitivity

Using the same full statutory cost stack and ₹20/order brokerage:

| Slippage each side | Net P&L |
|---:|---:|
| 0.5 point | -₹1,10,434.55 |
| 1.0 point | -₹1,46,774.55 |
| 2.0 points | -₹2,19,454.55 |

The sign of the result does not change across these tested slippage levels.

### Brokerage sensitivity

At 1 point slippage and full statutory cost stack:

| Brokerage/order | Net P&L |
|---:|---:|
| ₹10 | -₹1,30,938.95 |
| ₹15 | -₹1,38,856.75 |
| ₹20 | -₹1,46,774.55 |

The sign also does not change across these brokerage assumptions.

## Interpretation

The negative baseline is not explained by brokerage alone. It remains negative after removing the fuller cost stack and at materially lower slippage, and it becomes substantially worse as friction increases.

The 0-DTE subset is also negative in the primary full-cost scenario, so the observed result is not being driven solely by 0-DTE trades.

This phase does **not** test every possible Master Candle rule. It therefore does not justify a universal claim about all opening-range strategies.

## Phase status

**MC1 — CLOSED / NEGATIVE DISCOVERY.**

**MC2 cost block — COMPLETE.**

**Next: MC2 execution-rule robustness**, with preregistered alternatives only:
- breakout touch vs 1-minute close confirmation;
- prior-day EMA vs same-day completed-session EMA interpretation where causally valid;
- 30%, 40%, 50% premium stop;
- 14:30, 15:00, 15:15 exits;
- no-retuning year/regime stability;
- fixed holdout evaluation.

No parameter will be selected because it produces the best historical P&L.
