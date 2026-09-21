# Phase 1 — Data Source Manifest

## Primary option-data source

**Dataset:** Hugging Face `rissin/nse-options-intraday`  
**URL:** https://huggingface.co/datasets/rissin/nse-options-intraday  
**Reported scope:** 1-minute NIFTY, BANKNIFTY, SENSEX options from Oct 2024 through 2026; historical daily data for selected NSE indices.  
**Schema:** date, timestamp, underlying, expiry, strike, option_type, exercise_style, OHLC, volume, OI, settle_price, source, granularity.

This dataset is a public aggregation. Its README states that the intraday track was assembled from Upstox 1-minute candles and that daily data was assembled from NSE F&O bhavcopy history. It is therefore not treated as a raw exchange archive; provenance is retained exactly.

## Independent option-data sources inspected

- NSE historical F&O reports and option-chain facilities.
- Public GitHub project `mehulhere/fnopy`, which exposes an NSE historical F&O API wrapper and a BSE SENSEX Selenium provider.
- Kaggle NIFTY 2024 historical options dataset.
- Public market-data collector projects.

These sources are recorded as independent corroboration/reference, not silently mixed into the primary sample.

## Underlying daily data

Primary backtest bootstrap history uses daily NIFTY 50 and S&P BSE SENSEX index closes. The Phase 1 automated acquisition uses Yahoo Finance via `yfinance` as a secondary public source because it is straightforward to obtain a long daily history in the reproducible GitHub Actions environment.

This is a known provenance limitation. The robustness phase will cross-check return distributions against exchange/index sources where practical.

## Contract specifications

Expiry calendars and historical lot sizes are date-dependent and are versioned in `research/data/CONTRACT_SCHEDULES.md`. Exchange circulars are the authority for changes.

## Caching policy

- Raw parquet files are not committed to Git history because of size.
- GitHub Actions cache is keyed by dataset revision + underlying + year.
- Small derived extracts (eligible sessions, selected 09:30+ rows, executed trade inputs, settlement rows) are committed in later phases.
- Workflow artifacts preserve larger intermediate datasets for each completed run.

## Acceptance criteria

Phase 1 passes only if:
1. NIFTY and SENSEX option files are readable.
2. Both option types exist.
3. Timestamped intraday rows exist.
4. Expiry dates are populated.
5. Underlying daily data contains at least 756 valid sessions before the first eligible option backtest date.
6. No duplicate primary keys are detected in the filtered dataset.
7. The dataset source/version is captured in the manifest output.
