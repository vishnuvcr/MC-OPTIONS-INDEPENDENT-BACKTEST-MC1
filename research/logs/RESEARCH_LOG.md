# Research Log

## 2026-09-21 — Phase 0 initialization

### User-specified research target
Backtest the locked **NIFTY BATMAN** strategy on NIFTY and SENSEX using the repository vishnuvcr/MC-OPTIONS-INDEPENDENT-BACKTEST-MC1.

### Environment / repository findings
- Repository exists, is public, writable, and currently contains no committed files.
- Direct runtime git clone is unavailable because the execution environment cannot resolve github.com.
- GitHub repository APIs are available and will be used for inspection and versioned writes.
- GitHub Actions will be used for reproducible internet-backed data acquisition and execution.

### Initial literature/data scan
- NSE exposes current option-chain downloads and historical F&O reports, including F&O bhavcopy, contract-wise price/volume data, participant-wise open interest, FII derivatives statistics, and historical index/VIX archives.
- A public Hugging Face dataset rissin/nse-options-intraday reports 1-minute NIFTY/BANKNIFTY/SENSEX options from Oct 2024→2026, plus long historical daily data for NIFTY/BANKNIFTY.
- Public GitHub tooling exists for NSE historical options and BSE SENSEX options extraction.
- Paytm Money publishes brokerage/cost information; the research model will keep cost schedules versioned and date-aware.
- Historical lot sizes changed materially in 2024–2026 and must be date-aware.

### Important methodological decision
The primary research will not assume a constant current expiry weekday or lot size. Both are resolved from historical contract metadata/effective-date schedules.

### Next phase
Phase 1: acquire and validate reproducible historical option and underlying data and write a source/version manifest.


## 2026-09-21 — Phase 1 data start

- Phase 1 branch created.
- Public Hugging Face option dataset selected as the primary intraday source for 1-minute NIFTY/SENSEX option observations.
- Daily NIFTY/SENSEX underlying history is acquired via yfinance as a secondary source for the 756-session bootstrap history.
- Historical lot-size and expiry changes are explicitly recorded instead of assuming current contract specifications.
- A manual and pull-request GitHub Actions workflow was added for reproducible acquisition, cache, QA, and artifact publication.
- Phase 1 data QA is pending the first workflow execution.


## Phase 1 QA result (2026-09-21)

- GitHub Actions run 3 completed successfully.
- Dataset revision: 8f7739cab3f38abdcbc6332a6d0a83e1341326e3.
- 2024 NIFTY and SENSEX option parquet files downloaded and passed structural QA.
- NIFTY and SENSEX daily index histories passed the 756-session minimum check.
- Phase 1 artifact upload completed successfully.

## 2026-09-21 — Phase 2 complete

- Unit tests passed.
- Fresh Phase 2 workflow run 14 completed successfully.
- Primary gate was enforced before execution.
- Executed sample: 63 NIFTY trades and 61 SENSEX trades.
- Gate failures: 30 NIFTY candidates and 31 SENSEX candidates.
- Signal-data gaps: 21 NIFTY and 13 SENSEX D3 candidates had no usable pre-09:30 snapshot.
- Candidate descriptive net mean: NIFTY Rs 1,183.66 per executed trade; SENSEX Rs 2,507.53.
- Candidate ES95: NIFTY Rs -30,889.80; SENSEX Rs -26,807.30.
- Candidate ES99: NIFTY Rs -38,992.43; SENSEX Rs -38,352.77.
- These figures are not final until Phase 3 validation.

## Phase 3 validation complete (2026-09-21)

- Validation workflow run 3 passed all tests and contract checks.
- Leakage test confirms post-signal observations are excluded from the 756-session bootstrap input.
- Execution test confirms strict post-09:30 common-timestamp selection.
- Strike mapping uniqueness, 5,000 MC path count, strategy rule text, and historical-lot-size safeguards all passed.

## Phase 4 NIFTY complete (2026-09-21)

- Dedicated NIFTY workflow run 3 completed successfully.
- Executed trades: 63; coverage through 2026-07-21.
- Mean net P&L: Rs 1,183.66 per executed trade.
- Net ES95: Rs -30,889.80; ES99: Rs -38,992.43.

## Phase 5 SENSEX complete (2026-09-21)

- Dedicated SENSEX workflow run 1 completed successfully.
- Executed trades: 61; coverage through 2026-07-16.
- Mean net P&L: Rs 2,507.53 per executed trade.
- Net ES95: Rs -26,807.30; ES99: Rs -38,352.77.

## Phase 6 complete with infrastructure constraint (2026-09-21)

- Primary-trade bootstrap confidence intervals, cost attribution, slippage stress, yearly stability, and cross-index bootstrap comparison were completed from the validated Phase 2 artifact.
- NIFTY mean net P&L: Rs 1,183.66; SENSEX mean net P&L: Rs 2,507.53.
- 95% bootstrap mean intervals include zero for both indices.
- Slippage stress to 5 points/leg leaves NIFTY approximately flat in sample mean and SENSEX positive.
- The raw-option MC calibration matrix (504/756/1008 windows × 1,000/5,000/10,000 paths) remains implemented in the manual Phase 6 workflow but was not executed because the GitHub Actions runner queue remained unavailable.
- Phase 6 is therefore marked complete with an explicit infrastructure limitation, and Phase 7 proceeds with that limitation as a manuscript item.

## Phase 7 manuscript complete (2026-09-21)

- Final manuscript created at `research/manuscript/NIFTY_BATMAN_MANUSCRIPT.md`.
- Supplementary methods/audit trail created at `research/manuscript/SUPPLEMENT.md`.
- References created at `research/manuscript/REFERENCES.md`.
- Repository-native charts and source-value tables created under `research/manuscript/`.
- Manual Phase 7 validation workflow added.
- Final manuscript distinguishes validated primary results from the infrastructure-constrained raw-option MC calibration sensitivity.
- The research plan is complete through Phase 7; future work is documented rather than extending the present study indefinitely.


## 2026-09-21 — Phase 8 methodological revalidation initiated

External scientific review identified material issues in the Phase 7 framing: earlier BATMAN development included joint tuning; MC-EV chronology needs timestamp proof; iid trade bootstrap is insufficient as the sole uncertainty method; four-leg execution and strike mapping need realism diagnostics; capital/margin analysis is incomplete; and the raw-option 504/756/1008 × 1,000/5,000/10,000 matrix remains outstanding.

Branch phase-8-methodological-revalidation was created. The locked strategy rule is unchanged. This phase corrects research claims and adds validation; it does not retune BATMAN.

## 2026-09-21 — Phase 8 implementation findings

- Added trade-level gate premium timestamp/source, execution-leg volume, available strike-grid, strike displacement, and lot-size source fields.
- Added dependence-aware block bootstrap, paired signal-date NIFTY/SENSEX comparison, strike-mapping audit, execution-volume audit, payoff-structure analysis, and ES95 sizing examples.
- Added full raw-option 9-scenario matrix runner per index (18 total scenarios) and pull-request/dispatch GitHub Actions workflow.
- Added Paytm Money brokerage sensitivity and contract/cost source audit.
- Critical data-governance finding: NIFTY lot-size changes are contract-cohort/effective-date dependent, so expiry-only hard-coded lot-size logic is not sufficient when contract-level lot size is unavailable. Phase 8 now prefers contract-level lot_size from the raw dataset and records the provenance source.

## 2026-09-21 — Phase 8 first workflow validation result

The first Phase 8 GitHub Actions run reached the test suite and correctly stopped before downloading market data. 15 tests passed and one legacy validation test failed because the execution function was extended from a 2-tuple to a 3-tuple carrying execution volumes. The test was updated to match the new audited return shape. No numerical backtest result was accepted from the failed run.

## 2026-09-21 — Phase 8 lot-size correction

Official NSE cohort dates showed that the earlier fallback schedule was too coarse. The fallback was corrected to NIFTY 25 before 20-Nov-2024, 75 for contracts from 20-Nov-2024 through 05-Jan-2026, and 65 from 06-Jan-2026 onward. Because the pinned intraday dataset has no lot_size column, this corrected fallback remains the active provenance path for this raw-option dataset.

## 2026-09-21 — Phase 8 entry-cost chronology correction

A cost-date audit found that entry STT was keyed to expiry rather than actual execution. This could misclassify trades around the 1-Apr-2026 STT boundary. The engine now keys entry brokerage/venue/STT calculations to the first executable timestamp, while expiry STT remains keyed to the expiry date. A boundary unit test was added.

## 2026-09-22 — Phase 8 execution bottleneck correction

The monitoring UI disconnected while GitHub Actions was being polled, and the authoritative workflow was queued. The Phase 8 workflow previously requested two simultaneous hosted runners. It was consolidated to a single ubuntu-24.04 job executing both index matrices sequentially. This preserves the full 18-scenario design while reducing runner requirements and avoiding a two-runner scheduling bottleneck.

## 2026-09-22 — Phase 8 local validation attempt

A local clone/pytest attempt was blocked because the execution container could not resolve github.com. Therefore no local numerical output is accepted; GitHub Actions remains the authoritative reproducibility path.

## 2026-09-22 — Phase 8 infrastructure stop condition

The consolidated Phase 8 workflow was reduced to one job and moved to an alternate hosted runner image. The latest authoritative run (run 102, head 5cb604dcfa5a7bab0b39ebd1cd80bea192b2ef11) remains queued with no job steps started. Direct local execution is also unavailable because this environment cannot resolve GitHub/Hugging Face hosts. The research therefore stops at the approved Phase 8 infrastructure boundary rather than substituting data, changing the model, or inventing numerical results.


## 2026-09-22 — Phase 8 authoritative execution started

- After runner-capacity mitigation, authoritative GitHub Actions run 35641908887 transitioned from queued to in progress.
- Job setup, checkout, Python environment, tests, dataset-revision pinning, Hugging Face cache setup, NIFTY/SENSEX raw-data downloads, and raw-schema audit all completed successfully.
- The NIFTY full raw-option 18-scenario calibration matrix is currently executing; SENSEX and the downstream Phase 8 audits remain pending.
- This supersedes the earlier infrastructure-stop wording for the current execution state. No numerical Phase 8 result is accepted before the full chain and audits complete.


## 2026-09-22 — Phase 8 numerical revalidation complete

- Authoritative run 35641908887 completed successfully.
- All 18 raw-option calibration scenarios completed: 3 bootstrap windows (504/756/1008) × 3 MC path counts (1,000/5,000/10,000) for each of NIFTY and SENSEX.
- Primary 756/5,000 result: NIFTY 63 trades, mean net ₹966.46/trade, enhanced-friction mean ₹936.45; SENSEX 61 trades, mean net ₹2,508.06/trade, enhanced-friction mean ₹2,478.65.
- Cluster/block-bootstrap 95% mean-P&L intervals include zero for both indices: NIFTY ₹-1,985.18 to ₹3,955.42; SENSEX ₹-479.84 to ₹5,530.85.
- Gate chronology and execution-volume audits passed at 100% in the primary scenario; final strike uniqueness was 100%, with non-zero strike displacement from theoretical quantiles.
- Paired NIFTY/SENSEX analysis had only one common signal date and therefore did not support paired inference.
- Full results and calibration matrix are recorded in research/PHASE8_RESULTS.md.
