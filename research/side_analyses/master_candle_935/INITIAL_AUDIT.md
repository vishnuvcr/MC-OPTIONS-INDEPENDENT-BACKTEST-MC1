# Initial Audit — Master Candle 09:35–09:45

## A. Published-claim arithmetic
The user-supplied annual figures are: 2021 ₹87 lakh; 2022 ₹29 lakh; 2023 ₹53 lakh; 2026 YTD ~₹60 lakh. These sum to approximately ₹229 lakh = ₹2.29 crore. The user also reports overall gross profit of ₹2.76 crore. Difference: ₹47 lakh. Therefore the listed annual figures do not reconcile to the stated total. Possible explanations include omitted 2024/2025 results, different gross/net definitions, or different sample windows. This must be resolved before treating the figures as one internally consistent series.

## B. 0DTE contribution
Reported 0DTE profit: ~₹26 lakh. Relative to ₹2.76 crore, this is ~9.4%. Relative to ₹2.29 crore, ~11.4%. It is material enough to analyze, but not the majority of reported profit.

## C. Capital arithmetic
The user reports 10 lots, maximum drawdown ~₹24 lakh, and capital requirement ~₹1.2–1.3 crore. Illustration only: a NIFTY lot size of 65, 10 lots, and ₹200 premium requires roughly ₹1.30 lakh of premium cash, not ₹1.3 crore. At ₹1,000 premium, ~₹6.50 lakh. Therefore ₹1.2–1.3 crore cannot mean simple premium cash for one 10-lot long-option position. It likely represents a larger reserve, scaling convention, short-option margin, or another capital definition.

## D. Historical contract risk
A 2021–2026 backtest cannot use the modern NIFTY lot size throughout. NSE revisions changed NIFTY lot size across the period, so quantity must be contract/date effective.

## E. Data feasibility
The repository’s currently validated intraday dataset rissin/nse-options-intraday starts in October 2024. It cannot reproduce a 2021–2026 option backtest on its own. A separate candidate is https://huggingface.co/datasets/thetrademarkk/india-index-options-1m, which advertises approximately 2021–2026 1-minute index/option coverage but also states that option coverage is partial and that some far/illiquid strikes are sparse or absent. It is therefore a candidate for reconstruction, not yet an accepted research-grade source.

## F. Primary methodological risks
1. Ambiguous long vs short option wording.
2. Ambiguous breakout confirmation.
3. Ambiguous meaning of “25-day EMA”.
4. Ambiguous expiry selection.
5. Ambiguous exit rule.
6. Historical bid/ask is generally unavailable in public 1-minute OHLC datasets, so fixed slippage is a stress assumption.
7. Option coverage sparsity can bias ATM selection or exclude trades that would have existed in the source strategy.
8. Data survivorship/selection bias is possible if only currently available contract files are retained.
9. Changing lot sizes can distort a multi-year cumulative P&L if the source used a fixed modern lot multiplier.

## Audit conclusion
The strategy is backtestable in principle, but the published result cannot yet be accepted as reproducible. The correct next step is point-in-time data/strategy reconstruction, not blind replication of the headline P&L.
