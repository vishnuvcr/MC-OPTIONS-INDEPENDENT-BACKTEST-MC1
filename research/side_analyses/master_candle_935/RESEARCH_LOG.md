# Research Log — Master Candle 09:35–09:45

## 2026-09-29 — MC0 initiation
- Main Daily Options v1 research track is paused; no main-strategy conclusion changed.
- New side analysis created on branch side-analysis/master-candle-935.
- Existing repository research governance and error-logging standards were reviewed before starting.
- User-supplied strategy rules were converted into a provisional executable specification.
- Major ambiguity discovered: long-vs-short option wording.
- Major ambiguity discovered: meaning/timeframe of “25-day EMA”.
- Major ambiguity discovered: breakout confirmation and exit logic.
- Arithmetic audit found that listed annual profits sum to ₹2.29 crore, not the claimed ₹2.76 crore.
- Existing validated intraday data begins Oct-2024; a separate 2021–2026 dataset candidate is required.

## 2026-09-29 — MC1 runner implemented
- Added a reproducible GitHub Actions backtest runner using the public 1-minute NIFTY index/options dataset candidate.
- Baseline uses long ATM directional option buying, first 1-minute close beyond the 09:35–09:45 range, prior-day daily 25 EMA filter, nearest listed expiry, 40% premium stop, one trade/day, 15:15 time exit, 10 lots, date-effective NIFTY lot-size proxy, ₹20/order brokerage, STT, and 1 option point adverse slippage per side.
- Full all-in venue/statutory friction remains a later robustness stage rather than being guessed into the baseline.
