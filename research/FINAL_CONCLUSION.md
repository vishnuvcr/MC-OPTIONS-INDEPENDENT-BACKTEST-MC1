# Final Research Conclusion

## Validated primary result

The locked NIFTY BATMAN rule generated:
- NIFTY: 63 executed trades, mean net P&L Rs 1,183.66/trade, ES95 -Rs 30,889.80, ES99 -Rs 38,992.43.
- SENSEX: 61 executed trades, mean net P&L Rs 2,507.53/trade, ES95 -Rs 26,807.30, ES99 -Rs 38,352.77.

## Evidence interpretation

The positive sample means are not statistically precise enough to establish a stable population-level edge. Bootstrap 95% intervals for mean net P&L include zero for both indices.

The strongest robustness result is execution sensitivity:
- NIFTY mean net falls to approximately Rs 20/trade at 5 points of slippage per execution leg.
- SENSEX remains positive in that stress case at approximately Rs 2,157/trade.

## Scientific conclusion

The research establishes a reproducible positive sample outcome under the locked primary assumptions, with meaningful tail risk and material execution sensitivity. It does not establish production readiness or a durable future trading edge.

## Outstanding future experiment

The exact raw-option MC calibration matrix (504/756/1008 bootstrap windows × 1,000/5,000/10,000 paths) remains a manual reproducibility workflow because GitHub Actions runner capacity was unavailable during this session. It must be run before any stronger robustness claim is made.
