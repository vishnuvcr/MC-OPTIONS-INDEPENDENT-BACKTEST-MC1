# Data and Literature Source Audit — Master Candle 09:35–09:45

## Primary market-data candidate

Hugging Face dataset:
https://huggingface.co/datasets/thetrademarkk/india-index-options-1m

The dataset card describes 1-minute OHLCV(+OI) bars for NSE/BSE NIFTY, BANKNIFTY and SENSEX from approximately 2021–2026. It is licensed CC-BY-NC-4.0, identifies separate index and option parquet structures, and explicitly states that option coverage is partial and that illiquid/far strikes may be sparse or absent. The NIFTY option directory contains files beginning 2021-05-27.

This source is therefore suitable as a reproducible candidate for research reconstruction, but not as an exchange-certified substitute. The backtest must report missing/sparse contracts and compare selected sessions against an exchange/public source where practical.

## Existing repository source

The already validated BATMAN intraday dataset:
https://huggingface.co/datasets/rissin/nse-options-intraday

Its intraday track begins in October 2024, so it cannot independently reproduce the video’s claimed 2021–2026 option history.

## Historical contract metadata

NSE circular dated 31-Mar-2021 revised NIFTY lot size from 75 to 50 for the relevant contracts, with July 2021 monthly and August 2021 weekly contracts onward using the revised lot size:
https://archives.nseindia.com/content/circulars/FAOP47854.pdf

NSE later revised NIFTY index-derivative lot sizes again, including a 75-lot regime in late 2024. The currently published NSE contract information also states that the permitted lot size for futures and options is exchange-defined and date/version dependent.

The research therefore uses date-effective lot-size logic, not the current 2026 lot size for all historical observations.

## Opening-range literature

Holmberg, Lönnbark & Lundström, “Assessing the profitability of intraday opening range breakout strategies”, Finance Research Letters 10(1), 2013, evaluates mechanical opening-range breakout rules and reports evidence of intraday trending in crude-oil futures:
https://doi.org/10.1016/j.frl.2012.09.001

Tsai et al., “Assessing the Profitability of Timely Opening Range Breakout on Index Futures Markets”, IEEE Access 2019, evaluates 1-minute opening-range breakout rules across multiple index futures markets:
https://doi.org/10.1109/ACCESS.2019.2899177

A 2026 exploratory QQQ study on breakout/retest sequencing emphasizes that conclusions depend strongly on precise operational definitions of breakout, retest and outcome:
https://doi.org/10.2139/ssrn.6745958

These sources support researching the opening-range mechanism, but they do not validate this specific NIFTY 09:35–09:45 option strategy.

## Execution-cost literature

Option-trading research has repeatedly shown that bid/ask spreads, execution lag and transaction costs can materially change apparent trading profits. For example, historical option-market efficiency tests explicitly account for bid/ask prices, execution lag and transaction costs:
https://doi.org/10.1016/0304-405X(83)90034-X

The side analysis therefore does not treat an OHLC close as equivalent to a guaranteed executable fill.

## Current status

MC0 specification/audit: complete enough to permit a baseline implementation.

MC1 data runner: implemented.

Open research limitations:
- candidate dataset starts 2021-05-27 rather than Jan-2021;
- option coverage is partial;
- historical bid/ask is not represented in the candidate 1-minute OHLC schema;
- full date-effective statutory/venue cost stack still needs source-by-source implementation;
- exact video rules for breakout confirmation, exit and long-vs-short option direction remain unverified because the supplied YouTube page could not be independently retrieved through the available web cache.
