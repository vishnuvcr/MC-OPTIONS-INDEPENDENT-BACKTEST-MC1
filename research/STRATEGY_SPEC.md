# NIFTY BATMAN — Locked Strategy Specification

## Rule block

**When:** D3 trading session before expiry  
**Signal:** 09:30 IST  
**Model:** 756-session bootstrap MC, 5,000 paths  
**Gate:** gross MC-EV > 0  
**Strikes:** P20, P35, P65, P80 MC terminal quantiles mapped to nearest unique available strikes  
**Position:** +1 P35 PE, −2 P20 PE, +1 P65 CE, −2 P80 CE  
**Execution:** first executable observation after 09:30  
**Exit:** expiry  
**Primary research slippage:** 2 option points per execution leg  
**Costs:** brokerage + STT + historical lot size  
**Sizing:** ES95/ES99 risk proxy, not maximum-profit sizing

## Interpretation conventions

- D3 means the third trading session before the expiry trading session, counting backward over actual exchange trading sessions for the relevant underlying/exchange.
- P20/P35/P65/P80 are terminal Monte Carlo empirical quantiles, not option-premium percentiles.
- A PE leg is selected from the put strike grid; a CE leg is selected from the call strike grid.
- nearest unique available strikes means choose nearest listed strikes while ensuring all four target strikes are unique. Tie-breaking is deterministic and version-controlled.
- first executable observation after 09:30 means the earliest timestamp strictly after the 09:30 signal at which the required contract record is executable under the source data rules.
- expiry is the actual contract's last trading/settlement date from the historical contract record.
- Gross MC-EV includes entry premium cashflow and terminal payoff, but excludes execution slippage and trading costs.
- Realized net P&L applies the documented slippage and cost model.

## Strategy P&L

For leg quantity q, strike K, and entry premium p:

- Put expiry payoff per index point: max(K - S_T, 0)
- Call expiry payoff per index point: max(S_T - K, 0)
- Entry premium cashflow: -q * p
- Expiry P&L per index point: q * payoff(S_T,K) - q * p

The portfolio is the sum across the four legs.

## Immutable change policy

Changes to this specification are not patch fixes. They require a new strategy version and a new research phase/branch with explicit rationale.
