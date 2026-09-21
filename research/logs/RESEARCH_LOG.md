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
