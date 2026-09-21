# Publication Figures and Charts — Version 1.0

## Figure 1 — Mean net P&L across MC calibration settings

```mermaid
xychart-beta
    title "Mean Net P&L by MC Calibration"
    x-axis ["504/1k","504/5k","504/10k","756/1k","756/5k","756/10k","1008/1k","1008/5k","1008/10k"]
    y-axis "₹ per trade" 0 --> 3000
    line [350,13,84,1469,966,410,1228,554,608]
    line [1641,1646,1794,2051,2508,2427,2133,2579,2773]
```

First line: NIFTY. Second line: SENSEX.

## Figure 2 — Mean P&L versus conservative research capital

```mermaid
xychart-beta
    title "Mean Net P&L and Conservative Research Capital"
    x-axis ["NIFTY","SENSEX"]
    y-axis "₹" 0 --> 70000
    bar [966,2508]
    bar [63508,66886]
```

First bar series: mean net P&L/trade. Second bar series: conservative research capital proxy.

## Figure 3 — Brokerage sensitivity

```mermaid
xychart-beta
    title "Mean Net P&L vs Brokerage per Order"
    x-axis ["₹10","₹15","₹20"]
    y-axis "₹ per trade" 0 --> 3000
    line [1006,986,966]
    line [2548,2528,2508]
```

First line: NIFTY. Second line: SENSEX.

## Figure 4 — Tail-risk summary

| Measure | NIFTY | SENSEX |
|---|---:|---:|
| ES95 loss | ₹31,753.75 | ₹26,807.30 |
| ES99 loss | ₹38,992.43 | ₹38,352.77 |
| Maximum drawdown | ₹61,576.41 | ₹66,886.42 |
| Conservative capital proxy | ₹63,507.51 | ₹66,886.42 |