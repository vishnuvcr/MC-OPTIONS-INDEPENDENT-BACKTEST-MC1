# Master Candle 09:35–09:45 — Strategy Specification

## User-supplied core
- Chart: 10-minute NIFTY chart.
- Master candle: 09:35–09:45 IST.
- Mark master-candle high and low.
- Breakout determines direction.
- Trend filter: 25-day EMA.
- Directional option trade described by the user as ATM.
- Risk: fixed 40% premium stop; alternatively/trailing exit involving EMA 25.
- Friction: slippage + broker charges explicitly accounted for.
- Published backtest claim: 10 lots over a broad 2021–2026 period.

## Critical interpretation register

### 1. Long versus short option
The supplied summary says “selling At-The-Money directional options”, but the same description says “option buying”, refers to a call premium increasing by 122 points, and describes a fixed percentage stop on the premium. These statements are internally inconsistent.
Primary test hypothesis: breakout up -> BUY ATM CE; breakout down -> BUY ATM PE.
Secondary audit scenario only: breakout up -> SELL ATM CE; breakout down -> SELL ATM PE.

### 2. Breakout confirmation
Candidate interpretations: first intrabar touch after 09:45; first 1-minute close beyond the level; first 10-minute close beyond the level. Primary execution test should use a touch rule only if source evidence demonstrates stop-order/touch execution; otherwise 1-minute close confirmation is the conservative reproducible default.

### 3. 25-day EMA
Default interpretation: EMA of the daily NIFTY closing price, calculated only from completed prior trading sessions and projected as an intraday filter. Alternative: 25-period EMA on 10-minute bars. These are economically different indicators and must not be silently conflated.

### 4. EMA filter direction
Primary interpretation: long breakout allowed only when NIFTY is above the daily 25-day EMA; short breakout allowed only when NIFTY is below it.

### 5. ATM strike
Primary: nearest listed strike to NIFTY spot at the actual breakout timestamp. Sensitivity: nearest strike at 09:45, nearest strike at session open, and one-strike ITM/OTM alternatives.

### 6. Expiry selection
Primary: nearest listed expiry after the breakout timestamp. Historical expiry date must be read from the contract record, never inferred from today’s weekday.

### 7. 40% stop
For a long option: initial stop = 60% of entry premium. If the option gaps through the stop, fill at the available next observation/marketable price plus modeled slippage. For a short option, a “40% stop” must be defined as a 40% adverse increase in premium unless source evidence shows another rule.

### 8. Exit
The supplied wording is ambiguous between premium stop only + end-of-day exit, premium stop + trailing 25 EMA on NIFTY, 25 EMA on 10-minute NIFTY, or another source-specific rule. No exit rule is allowed to change during baseline testing.

### 9. Re-entry / opposite breakout
Default: one trade per session; no re-entry after stop. Sensitivity: allow second trade after an opposite breakout only as a separate scenario.

### 10. Time exit
Primary candidate: 15:15 IST to avoid end-of-session microstructure. This remains to be aligned with the source/video wording.

## Point-in-time constraints
- EMA may use only prior completed daily data.
- Breakout is measured from the completed 09:35–09:45 candle.
- Strike selection may use only spot information available at the breakout.
- Option premium used for stop initialization must be the actual executable entry observation.
- No post-entry data may influence the initial signal.
- Historical lot size must be resolved from the contract cohort/date.

## Cost model
Primary report includes brokerage, STT, stamp duty, exchange transaction charges, SEBI fee, GST, and explicit option slippage. Where a source or account-vintage cost is uncertain, report a range rather than silently selecting a convenient value.

## Required trade record
Every trade should store: date, signal timestamp, breakout direction, master high/low, master range width, EMA value, spot at breakout, selected expiry, DTE, strike, option type, entry premium, stop premium, stop timestamp, exit timestamp, exit premium, gross P&L, each cost component, slippage assumption, lot size, quantity, net P&L, MFE, MAE, and exit reason.
