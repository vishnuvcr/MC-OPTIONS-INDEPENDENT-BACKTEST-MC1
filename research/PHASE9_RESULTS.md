# Phase 9 — Capital and Return Analysis Results

## Validation status
Provisional numerical results computed deterministically from the pinned Phase 8 artifact `phase8-final` (artifact ID `10659054480`) using the locked primary 756-session / 5,000-path trade files. GitHub Actions validation of the Phase 9 analysis code is the remaining acceptance check before this phase is marked complete.

## Primary capital and return results

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Executed trades | 63 | 61 |
| Mean net P&L / trade | ₹966.46 | ₹2,508.06 |
| Enhanced-friction mean / trade | ₹936.45 | ₹2,478.65 |
| VaR95 loss | ₹26,289.43 | ₹14,139.65 |
| ES95 loss | ₹31,753.75 | ₹26,807.30 |
| VaR99 loss | ₹36,219.47 | ₹33,043.57 |
| ES99 loss | ₹38,992.43 | ₹38,352.77 |
| Maximum observed single-trade loss | ₹38,992.43 | ₹38,352.77 |
| Maximum historical drawdown | ₹61,576.41 | ₹66,886.42 |
| Maximum simultaneous BATMAN positions observed | 2 | 2 |
| ES95 capital proxy / position | ₹31,753.75 | ₹26,807.30 |
| Conservative research capital proxy | ₹63,507.51 | ₹66,886.42 |
| Mean P&L / ES95 | 3.04% | 9.36% |
| Mean P&L / conservative capital proxy | 1.52% | 3.75% |
| Enhanced mean / conservative capital proxy | 1.47% | 3.71% |
| Observed trades / year | 35.46 | 34.65 |
| Simple linear annual P&L | ₹34,266.49 | ₹86,905.30 |
| Simple linear annual P&L / conservative capital proxy | 53.96% | 129.93% |

## What the capital numbers mean

### NIFTY
- One-position ES95 risk proxy: about ₹31,754.
- A reserve covering the observed maximum of two simultaneous BATMAN positions at ES95 plus the observed historical drawdown gives a conservative research capital proxy of about ₹63,508.
- Mean net P&L divided by one-position ES95 is 3.04% per completed trade.
- Mean net P&L divided by the more conservative two-position/drawdown reserve is 1.52% per completed trade.

### SENSEX
- One-position ES95 risk proxy: about ₹26,807.
- The observed drawdown is larger than two times ES95, so the conservative research capital proxy is about ₹66,886.
- Mean net P&L divided by one-position ES95 is 9.36% per completed trade.
- Mean net P&L divided by the conservative drawdown/concurrency reserve is 3.75% per completed trade.

## Entry premium cash requirement

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Mean long-leg premium cash | ₹16,497.51 | ₹16,512.62 |
| Maximum long-leg premium cash | ₹38,964.25 | ₹38,905.00 |
| Mean short-leg premium credit | ₹19,455.27 | ₹21,198.65 |
| Mean net entry premium cashflow | -₹2,957.76 | -₹4,686.03 |
| Largest net entry debit observed | ₹937.50 | ₹1,607.00 |

A negative mean net entry premium cashflow means the four-leg basket was, on average, entered for a net credit in the recorded execution prices. This does not imply that only the net credit is required as capital: the short options require exchange-defined margin.

## Overlap analysis

- NIFTY had one observed period with two active BATMAN positions; the overlapping pair finished with a combined positive P&L of ₹18,918.93, so no overlapping-loss episode was observed in the sample.
- SENSEX had two overlapping pair episodes; the worst combined overlapping P&L was a loss of ₹17,076.03.

## Return interpretation

The 3.04% (NIFTY) and 9.36% (SENSEX) figures are mean P&L divided by the one-position ES95 risk proxy. The 1.52% and 3.75% figures use the more conservative capital proxy that covers observed concurrency and drawdown.

The simple linear annual ratios of 53.96% and 129.93% are not compounded portfolio returns and should not be presented as a forecast or guaranteed annual return. They are mechanical turnover-normalized ratios computed from the observed trade frequency in this historical sample.

## Margin conclusion

Actual Paytm Money or exchange margin is **not** identified by these results. NSE Clearing describes equity-derivatives initial margin as portfolio-based SPAN with a 99% one-day VaR framework and additional exposure components. Paytm Money states that option-writing margin is exchange-defined and that its margin calculator incorporates SPAN, exposure and hedge benefits. The Phase 8 trade files do not contain the date-specific SPAN risk arrays or broker margin snapshots needed to reconstruct exact historical margin.

Therefore the correct terminology for Phase 9 is **capital proxy**, not **broker margin**.

## Scientific inference

Phase 9 changes the interpretation of the ₹966 and ₹2,508 mean P&L figures materially: the figures are small relative to the study's tail-risk reserves, and the denominator matters. The study can quantify risk-capital ratios, but it still cannot claim a production return-on-margin without a historical exchange/broker margin reconstruction or prospective broker statements.

## Limitations

- The conservative capital proxy is derived from realized P&L and observed concurrency/drawdown, not from SPAN risk arrays.
- The annual ratios are historical turnover ratios, not compounded returns.
- The sample remains limited to the Phase 8 option-data period and the 63/61 executed-trade primary sample.
- The 2-point-per-leg slippage model remains a research stress assumption.

## Source audit

See `research/data/PHASE9_CAPITAL_MARGIN_SOURCE_AUDIT.md` for the exchange and broker margin-source definitions and the exact data gap.