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
