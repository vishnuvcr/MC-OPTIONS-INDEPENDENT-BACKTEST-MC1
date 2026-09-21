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
| 8 | phase-8-methodological-revalidation | Correct development-history framing, leakage chronology audit, clustered uncertainty, full raw-option calibration, execution/capital/strike robustness | Complete |
| 9 | phase-9-capital-return-analysis | Capital proxies, premium cash requirements, drawdown/concurrency, return ratios, and margin-source reconciliation | Complete* |

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

Phases 0-7 produced the original locked-rule historical sample. Phase 8 methodological revalidation is now complete on the pinned raw-option dataset. The current primary calibration remains common to both indices at **756 historical sessions × 5,000 MC paths**; the 18-scenario matrix is sensitivity analysis, not index-specific tuning. Phase 8 produced 63 NIFTY and 61 SENSEX executed trades in the primary scenario, with block-bootstrap mean-P&L intervals that include zero for both indices. NIFTY is materially calibration-sensitive; SENSEX remains positive across all nine tested calibration settings. Phase 9 now translates the same primary trades into explicit ES95 capital proxies, premium cash requirements, drawdown/concurrency reserves, and P&L-to-capital ratios. No independent future-profitability claim is made.

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
- [Phase 8 results](research/PHASE8_RESULTS.md)
- [BATMAN development history](research/DEVELOPMENT_HISTORY.md)
- [Prospective frozen validation protocol](research/PROSPECTIVE_FROZEN_VALIDATION_PROTOCOL.md)
- [Phase 8 contract and cost source audit](research/data/PHASE8_CONTRACT_COST_SOURCE_AUDIT.md)
- [Phase 9 capital/return plan](research/PHASE9_CAPITAL_RETURN_PLAN.md)
- [Phase 9 results](research/PHASE9_RESULTS.md)
- [Phase 9 margin source audit](research/data/PHASE9_CAPITAL_MARGIN_SOURCE_AUDIT.md)
- [Phase 9 capital/return table](research/manuscript/tables/PHASE9_CAPITAL_RETURN.csv)
- [Final conclusion](research/FINAL_CONCLUSION.md)
- [Phase 6 robustness plan](research/PHASE6_ROBUSTNESS_PLAN.md)
- [Phase 6 external-context sources](research/data/PHASE6_EXTERNAL_CONTEXT_SOURCES.md)


### Phase 8 status
Phase 8 is complete. The locked strategy is unchanged. The full raw-option calibration matrix (3 windows × 3 path counts × 2 indices = 18 scenarios) executed successfully in authoritative GitHub Actions run `35641908887`. The primary research calibration remains **756 × 5,000 for both NIFTY and SENSEX**. No different index-specific settings are selected from the historical sensitivity table because that would be post hoc tuning. See `research/PHASE8_RESULTS.md` for the audited numerical results.


### Phase 9 status
Phase 9 is complete for the approved P&L-derived capital/return scope; exact historical broker/exchange margin remains a documented data limitation.

Phase 9 is the capital-interpretation phase for the locked Phase 8 primary sample. Provisional results imply an ES95 capital proxy of about ₹31.8k per NIFTY position and ₹26.8k per SENSEX position; the conservative research reserve covering observed concurrency and drawdown is about ₹63.5k for NIFTY and ₹66.9k for SENSEX. These are P&L-derived capital proxies, not Paytm Money or exchange margin. The deterministic capital analysis is complete. The repository includes a manual/PR GitHub Actions workflow, but the current GitHub connector did not surface an automatic Phase 9 run/status; this is recorded as an infrastructure observability limitation, not as a successful remote run.

*Phase 9 Complete* means the approved P&L-derived capital/return analysis is complete; the repository-side workflow remains manually runnable, while this environment did not surface an automatic remote workflow status.
