# MC OPTIONS INDEPENDENT BACKTEST — MC1

Research project: independent, reproducible backtest of the **NIFTY BATMAN** strategy on **NIFTY 50** and **S&P BSE SENSEX** index options.

## Final rule (locked)

> **NIFTY BATMAN**
> - When: D3 trading session before expiry
> - Signal: 09:30 IST
> - Model: 756-session bootstrap MC, 5,000 paths
> - Gate: gross MC-EV > 0
> - Strikes: P20, P35, P65, P80 MC terminal quantiles mapped to nearest unique available strikes
> - Position: +1 P35 PE, −2 P20 PE, +1 P65 CE, −2 P80 CE
> - Execution: first executable observation after 09:30
> - Exit: expiry
> - Primary research slippage: 2 option points per execution leg
> - Costs: brokerage + STT + historical lot size
> - Sizing: ES95/ES99 risk proxy, not maximum-profit sizing

The backtest implementation must treat this block as the immutable strategy specification. Any change becomes a new research phase/branch and is recorded in the change log.

## Research scope

Primary instruments:
- NSE NIFTY 50 index options
- BSE SENSEX index options

Primary questions:
1. Does the locked rule generate positive gross and net expectancy after the specified execution slippage and applicable costs?
2. How stable are results across market regimes, years, expiry vintages, and volatility states?
3. How sensitive are results to bootstrap window length, path count, execution timing, strike-availability mapping, and cost assumptions?
4. What are the ES95/ES99 risk distributions and realistic capital requirements after historical lot-size changes?
5. Are NIFTY and SENSEX results materially different because of exchange-specific expiry calendars, strike grids, lot sizes, liquidity, and transaction costs?

## Research phases

| Phase | Branch | Purpose | Status |
|---|---|---|---|
| 0 | phase-0-governance | Repo setup, locked rule, research protocol, error/logging controls | Complete |
| 1 | phase-1-data | Source audit, data acquisition, provenance, caching, data QA | Complete |
| 2 | phase-2-model | MC model, strike mapping, gate, execution/cost engine | Complete |
| 3 | phase-3-validation | Unit tests, invariants, leakage checks, synthetic tests | Complete |
| 4 | phase-4-nifty | Full NIFTY backtest and diagnostics | Complete |
| 5 | phase-5-sensex | Full SENSEX backtest and diagnostics | Complete |
| 6 | phase-6-robustness | Cross-index comparison, sensitivity and regime analysis | Complete* |
| 7 | phase-7-manuscript | Final manuscript, figures, tables, appendices, supplements | Complete* |
| 8 | phase-8-methodological-revalidation | Correct development-history framing, leakage chronology audit, clustered uncertainty, full raw-option calibration, execution/capital/strike robustness | In progress |

## Data principles

- Prefer exchange-origin data (NSE/BSE) for contract metadata and settlement information.
- Use independent datasets only when exchange archives do not expose the required intraday history; provenance must be recorded.
- Never silently substitute another data source.
- Preserve small, reproducibility-critical extracts in the repo; large raw datasets are referenced by immutable source/version metadata and cached in workflow storage where appropriate.
- Historical contract specifications (expiry day and lot size) are date-dependent and must be modeled from effective-date schedules rather than hard-coded current values.

## Cost principles

The backtest includes the requested 2-point-per-leg primary slippage assumption plus brokerage and STT. The implementation keeps other statutory/venue costs configurable and reports which costs are included in each result set.

## Reproducibility

Every phase has its own branch and a manually runnable GitHub Actions workflow. Each phase writes:
- phase status
- data/source manifest
- validation results
- errors encountered and resolutions
- research notes and conclusions

## Status

Phases 0-7 produced the locked-rule historical sample; Phase 8 methodological revalidation is now in progress. The validated primary sample remains 63 NIFTY trades and 61 SENSEX trades over the available 1-minute option history beginning in October 2024. The final manuscript records the positive sample results, tail risk, execution sensitivity, and the infrastructure-constrained raw-option MC calibration sensitivity limitation.

See:
- [research protocol](research/RESEARCH_PROTOCOL.md)
- [research log](research/logs/RESEARCH_LOG.md)
- [error log](research/logs/ERROR_LOG.md)
- [strategy specification](research/STRATEGY_SPEC.md)
- [Phase 6 robustness plan](research/PHASE6_ROBUSTNESS_PLAN.md)
- [Phase 6 external-context sources](research/data/PHASE6_EXTERNAL_CONTEXT_SOURCES.md)
- [Final manuscript](research/manuscript/NIFTY_BATMAN_MANUSCRIPT.md)
- [Supplement](research/manuscript/SUPPLEMENT.md)
- [References](research/manuscript/REFERENCES.md)
- [Figures and charts](research/manuscript/FIGURES.md)
- [Manuscript tables](research/manuscript/tables/PRIMARY_STATS.csv)
- [Phase 8 methodological revalidation plan](research/PHASE8_METHODOLOGICAL_REVALIDATION_PLAN.md)
- [BATMAN development history](research/DEVELOPMENT_HISTORY.md)
- [Prospective frozen validation protocol](research/PROSPECTIVE_FROZEN_VALIDATION_PROTOCOL.md)
- [Phase 8 contract and cost source audit](research/data/PHASE8_CONTRACT_COST_SOURCE_AUDIT.md)
- [Final conclusion](research/FINAL_CONCLUSION.md)
- [Phase 6 robustness plan](research/PHASE6_ROBUSTNESS_PLAN.md)
- [Phase 6 external-context sources](research/data/PHASE6_EXTERNAL_CONTEXT_SOURCES.md)


### Phase 8 status
Phase 7 remains the numerical baseline, but its claims of pre-specification/no parameter search are amended. Earlier BATMAN development included joint tuning, so the 63/61-trade sample is not called independently out-of-sample without a genuine unseen split. Phase 8 is the corrective validation phase and does not change the locked strategy. Implementation is complete; the final validation workflow is waiting for hosted-runner capacity. No Phase 8 numerical output has been promoted to the manuscript yet.
