# NIFTY BATMAN on NIFTY 50 and S&P BSE SENSEX Index Options
## Reproducible Independent Backtest, Risk Analysis, Robustness, and Capital Interpretation

**Publication version:** 1.0  
**Publication date:** 22 September 2026  
**Status:** Repository-public research preprint; not peer reviewed or journal accepted.  
**Repository:** `vishnuvcr/MC-OPTIONS-INDEPENDENT-BACKTEST-MC1`  
**Strategy version:** Locked NIFTY BATMAN rule  
**Primary option-data revision:** `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`

> **Publication note.** Phase 8 is the authoritative methodological revalidation and Phase 9 is the authoritative capital/return interpretation. Historical Phase 7 values are retained below only where needed for auditability; they are not the publication headline results.


## Abstract

This study evaluates a locked four-leg index-option strategy, named **NIFTY BATMAN**, on NSE NIFTY 50 and BSE SENSEX index options. The rule is deterministic: on the third trading session before expiry, at a 09:30 IST information cut-off, the strategy constructs a 756-session bootstrap Monte Carlo distribution with 5,000 paths, accepts a trade only when gross Monte Carlo expected value (MC-EV) is positive, maps terminal P20/P35/P65/P80 quantiles to nearest unique available strikes, enters a +1/-2/+1/-2 four-leg portfolio, executes at the first common executable observation after 09:30, and exits at expiry. Primary implementation friction is fixed at 2 option points of adverse slippage per execution leg, with brokerage, STT and historical lot size applied.

Phase 8 revalidated the raw-option implementation on an intraday option dataset beginning in October 2024, with 63 NIFTY and 61 SENSEX executed trades under the common 756-session/5,000-path primary calibration. Mean net P&L per executed trade is ₹966.46 for NIFTY and ₹2,508.06 for SENSEX; the enhanced-friction means are ₹936.45 and ₹2,478.65. Block-bootstrap 95% intervals for the mean net P&L include zero for both indices, and ES95 is -₹31,753.75 and -₹26,807.30 respectively. The full 504/756/1008 × 1,000/5,000/10,000 raw-option calibration matrix was completed. NIFTY is materially calibration-sensitive, while SENSEX remains positive across all nine tested settings.

The evidence establishes reproducible positive sample means under the locked primary assumptions, but it does **not** establish a durable trading edge or production readiness. The study's strongest evidence concerns execution friction, tail risk, and calibration sensitivity. Phase 8 subsequently completed the full raw-option MC-calibration matrix (504/756/1008 bootstrap windows × 1,000/5,000/10,000 paths) for both indices. The common primary calibration remains 756 sessions × 5,000 paths; the matrix is treated as sensitivity/revalidation, not as a basis for selecting different settings per index.

---

## 1. Introduction

Index-option strategies can show attractive in-sample economics while failing after execution costs, structural market changes, or tail losses. Recent NIFTY option research similarly emphasizes the gap between theoretical volatility premia and tradeability after implementation frictions and extreme events [1,2].

This study addresses that problem with a locked, chronology-preserving strategy specification and an explicit cost model. The objective of the present locked-rule analysis is not to introduce additional optimization. However, the broader BATMAN research lineage included joint tuning of entry day, entry timing and exit methodology before the final specification was frozen. Accordingly, the existing 63/61-trade results are historical locked-rule results following research-stage selection; they are not described here as independent out-of-sample validation unless a genuinely unseen validation period is demonstrated.

The selected public option dataset describes a 1-minute intraday track covering NIFTY, BANKNIFTY and SENSEX from October 2024 through 2026, assembled from Upstox historical API candles, with daily history derived from NSE F&O bhavcopy. [3] NSE also maintains historical contract-wise price/volume data, F&O bhavcopy/UDiFF reports, settlement data, India VIX history, participant-wise derivatives reports and FII derivatives statistics. [4,5]

---

## 2. Research Questions

### RQ1 — Economic value
Does the locked NIFTY BATMAN rule generate positive gross and net expectancy after the specified 2-point-per-leg slippage, brokerage, STT and historical lot size?

### RQ2 — Risk
What are the realized P&L distribution, ES95, ES99, drawdown, loss frequency and outcome dispersion?

### RQ3 — Stability
How do outcomes vary by calendar year and execution-friction regime?

### RQ4 — Robustness
How sensitive are results to bootstrap-window length, Monte Carlo path count, slippage and additional costs?

### RQ5 — Cross-index comparison
How do the NIFTY and SENSEX implementations differ after exchange-specific expiries, strike grids, lot sizes and cost schedules?

---

## 3. Locked Strategy Specification

The strategy definition is immutable:

| Component | Rule |
|---|---|
| Timing | D3 trading session before expiry |
| Signal | 09:30 IST |
| Bootstrap | 756 historical sessions |
| MC paths | 5,000 |
| Gate | Gross MC-EV > 0 |
| Quantiles | P20, P35, P65, P80 of terminal underlying distribution |
| Strike mapping | Nearest unique listed strikes |
| Position | +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE |
| Entry | First common executable observation strictly after 09:30 |
| Exit | Expiry |
| Primary slippage | 2 index-option points per leg |
| Costs | Brokerage + STT + historical lot size |
| Sizing | ES95/ES99 risk proxy |

No additional parameter search was performed in the locked-rule implementation. Earlier development/tuning is disclosed above and is treated as part of the strategy-development phase. The 756/5,000 setting is the common primary calibration for both indices.

---

## 4. Data

### 4.1 Primary intraday option data

The primary source is the pinned Hugging Face dataset revision `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`. The dataset documentation states that the intraday track contains 1-minute NIFTY/SENSEX options from October 2024 onward and identifies the upstream source as Upstox historical API candles. [3]

### 4.2 Underlying history

Daily NIFTY 50 and SENSEX histories were acquired in the production workflow using a secondary public daily-price source for the bootstrap return history. This is a documented provenance limitation; the study does not present that series as exchange-native.

### 4.3 Contract metadata

Historical lot sizes and expiry conventions are treated as date-effective rather than hard-coded. The model therefore uses:
- NIFTY lot-size regimes of 25, 75 and 65 units over the principal sample;
- SENSEX lot-size regimes of 10 and 20 units;
- actual historical contract expiry fields rather than a fixed current weekday.

### 4.4 Data eligibility

NIFTY: 115 D3 candidates were encountered:
- 21 had no usable pre-09:30 snapshot;
- 30 failed gross MC-EV > 0;
- 1 failed unique-strike mapping;
- 63 executed.

SENSEX: 105 candidates:
- 13 had no usable pre-09:30 snapshot;
- 31 failed gross MC-EV > 0;
- 61 executed.

The excluded candidates remain in structured error output.

---

## 5. Scientific Methodology

### 5.1 D3 identification

For each historical expiry, the strategy counts backward over actual trading sessions and selects the third prior trading session as D3.

### 5.2 Information set

Only data available on or before the 09:30 IST signal cut-off may influence:
- the signal spot estimate;
- the 756-session return window;
- the Monte Carlo terminal distribution;
- the four strike selections.

### 5.3 Signal spot

Where sufficient CE/PE information exists, put-call parity across common strikes provides a contemporaneous spot proxy. Otherwise the previous valid underlying close is used as a documented fallback.

### 5.4 Monte Carlo

Historical log returns are drawn with replacement from the preceding 756 sessions. Each path contains a number of daily return steps equal to the number of trading sessions from D3 to expiry. The default seed is 756. Five thousand terminal paths are generated.

### 5.5 Strike mapping

Terminal P20/P35/P65/P80 quantiles are mapped to the nearest unique available strike. The mapping order is deterministic:
1. P20 PE
2. P35 PE
3. P65 CE
4. P80 CE

### 5.6 MC-EV gate

For each terminal path, the four-leg expiry payoff is calculated. Gross MC-EV is the average terminal portfolio payoff minus the signal-time entry premium available from the 09:30 information set, before execution slippage and transaction costs. The later first-common-executable price is not permitted to determine whether the gate passes. Phase 8 adds a trade-level timestamp audit for this ordering.

Only positive gross MC-EV observations are eligible for execution.

### 5.7 Execution and exit

All four legs must share a common executable observation strictly after 09:30 IST. A leg is executable when the source record contains a positive option price and, when available, positive volume.

Exit occurs at contract expiry using the historical index settlement observation.

### 5.8 Costs

The 2-point-per-leg assumption is a research stress assumption, not a validated estimate of four-leg market impact or simultaneous fill quality. Primary net P&L includes:
- 2 option points adverse slippage for each of four entry legs;
- ₹20 brokerage per entry order;
- date-effective STT;
- historical lot size.

The 2-point slippage assumption is intentionally isolated as the primary research friction.

### 5.9 Statistical analysis

The study reports:
- mean and median net P&L;
- mean MC-EV;
- profitable-trade share;
- ES95 and ES99;
- sequential maximum drawdown;
- yearly stratification;
- bootstrap confidence intervals for the mean and median;
- cross-index bootstrap comparison;
- slippage stress.

Expected shortfall is emphasized because tail risk is a central property of option strategies and can be poorly summarized by averages alone [6,7].

---

## 6. Validation and Leakage Controls

The automated Phase 3 validation suite passed:
- no post-signal option observations in strike selection;
- no post-signal underlying returns in the bootstrap input;
- strict post-09:30 execution;
- four unique mapped strikes;
- exactly 5,000 primary MC paths;
- deterministic MC seed;
- date-aware lot-size logic;
- locked strategy text checks.

No unresolved model-correctness error remained after Phase 3.

---

## 7. Results

### 7.1 Phase 7 historical baseline (preserved)

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Executed trades | 63 | 61 |
| Mean MC-EV | 52.15 pts | 234.74 pts |
| Median MC-EV | 27.44 pts | 136.91 pts |
| Mean gross P&L | ₹2,077.29 | ₹2,861.86 |
| Mean net P&L | **₹1,183.66** | **₹2,507.53** |
| Median net P&L | ₹2,149.25 | ₹3,318.19 |
| Profitable net trades | 66.7% | 77.0% |
| Total net P&L | ₹74,570.44 | ₹152,959.12 |
| ES95 | -₹30,889.80 | -₹26,807.30 |
| ES99 | -₹38,992.43 | -₹38,352.77 |
| Max sequential drawdown | -₹50,343.72 | -₹66,886.42 |
| Minimum trade | -₹38,992.43 | -₹38,352.77 |
| Maximum trade | ₹22,311.80 | ₹28,499.89 |

### 7.2 Phase 8 raw-option revalidation primary results

| Metric | NIFTY | SENSEX |
|---|---:|---:|
| Executed trades | 63 | 61 |
| Mean net P&L | **₹966.46** | **₹2,508.06** |
| Mean net P&L with enhanced friction | **₹936.45** | **₹2,478.65** |
| Block-bootstrap 95% CI for mean | **-₹1,985.18 to ₹3,955.42** | **-₹479.84 to ₹5,530.85** |
| ES95 | **-₹31,753.75** | **-₹26,807.30** |
| Mean absolute strike displacement | 12.14 points | 24.83 points |
| Maximum absolute strike displacement | 24.90 points | 97.86 points |

Phase 8 is the current methodological result. The Phase 7 values above remain in the manuscript as a reproducibility baseline; they are not silently overwritten because the raw-option revalidation changed the NIFTY sample estimate materially.

### 7.3 Distributional statistics

| Statistic | NIFTY | SENSEX |
|---|---:|---:|
| Net P&L SD | ₹10,918.11 | ₹11,114.27 |
| Skewness | -1.70 | -1.21 |
| MC-EV/P&L correlation | 0.274 | 0.303 |
| Cohen-type mean/SD ratio | 0.108 | 0.226 |

The negative skewness indicates that mean P&L is exposed to relatively large downside observations. The correlation between MC-EV and realized net P&L is positive but moderate, so the gate does not eliminate realized-outcome uncertainty.

### 7.4 Mean uncertainty

Bootstrap 95% intervals for mean net P&L:
- NIFTY: approximately **-₹1,585 to ₹3,727**.
- SENSEX: approximately **-₹388 to ₹5,163**.

A conventional one-sample t-test is secondary because the observed P&L distributions are negatively skewed:
- NIFTY: t ≈ 0.86, p ≈ 0.39.
- SENSEX: t ≈ 1.76, p ≈ 0.083.

These tests do not provide evidence of a precisely estimated positive mean at conventional 5% significance.

---

## 8. Slippage and Cost Sensitivity

The observed slippage stress should not be interpreted as proof of real executable fills. A four-leg basket can experience leg-by-leg timing, spread, queue and stale-quote effects. Phase 8 therefore treats fixed point slippage as a sensitivity parameter and adds bid/ask/fill analysis where source data permit.

### 8.1 Slippage stress

| Slippage/leg | NIFTY mean net | SENSEX mean net |
|---:|---:|---:|
| 0 | ₹1,959.27 | ₹2,741.45 |
| 1 | ₹1,571.46 | ₹2,624.49 |
| **2 primary** | **₹1,183.66** | **₹2,507.53** |
| 3 | ₹795.85 | ₹2,390.57 |
| 5 | ₹20.24 | ₹2,156.64 |

The NIFTY result is materially execution-sensitive. At 5 points per leg the mean becomes approximately flat in this sample. SENSEX shows greater tolerance to the same point-based stress because the historical lot size structure produces a smaller rupee impact per option point.

### 8.2 Cost attribution

Average brokerage is ₹80 per trade for four orders.

Average entry+expiry STT:
- NIFTY: approximately ₹37.44;
- SENSEX: approximately ₹40.23.

The fixed 2-point slippage contributes approximately:
- NIFTY: ₹776/trade;
- SENSEX: ₹234/trade.

Therefore, execution friction is a material driver of the net/gross difference.

---

## 9. Calendar-Year Stability

| Year | NIFTY trades | NIFTY mean net | SENSEX trades | SENSEX mean net |
|---|---:|---:|---:|---:|
| 2024 | 8 | -₹613.87 | 9 | -₹1,129.62 |
| 2025 | 30 | ₹894.17 | 29 | ₹851.63 |
| 2026* | 25 | ₹2,106.25 | 23 | ₹6,018.63 |

*Through July 2026.

The negative 2024 means and much stronger 2026-to-date SENSEX contribution demonstrate sample-period dependence. The dataset is too short to claim stable calendar-year stationarity.

---

## 10. Cross-Index Comparison

Observed mean net P&L difference:

**NIFTY - SENSEX = -₹1,323.87 per executed trade.**

Bootstrap 95% interval:

**approximately -₹5,194 to ₹2,513.**

The interval spans zero. The available sample does not precisely distinguish the two mean trade outcomes.

---

## 11. Robustness Status

### Completed
- trade-level and block-bootstrap uncertainty;
- mean/median uncertainty;
- yearly stratification;
- slippage 0/1/2/3/5 points;
- baseline and enhanced cost attribution;
- ES95/ES99 and sizing examples;
- strike-mapping and execution-volume audits;
- full raw-option 504/756/1008 × 1,000/5,000/10,000 matrix;
- paired NIFTY/SENSEX analysis where dates permit.

### Remaining outside Phase 8 scope
- full historical India VIX/FII-DII/global-market synchronized trade-level regime join;
- genuinely unseen prospective validation.

The completed matrix re-runs the full raw-option chain rather than perturbing the already-selected trade list.

---

## 12. Market-Regime and Institutional-Flow Context

NSE provides historical index data, India VIX history, contract-wise price/volume information, F&O daily settlement data and participant-wise/FII derivatives reports. [4,5]

NSE's FII/FPI and DII data are explicitly described as provisional and subject to custodial confirmation and later modification. [5] Consequently, current-only flow pages are not substituted for historical synchronized data.

The study therefore treats:
- India VIX;
- S&P 500;
- Cboe VIX;
- USD/INR;
- gold;
- prior-day NIFTY/SENSEX returns;
- FII/FPI and DII activity

as future explanatory/regime variables rather than hidden trading rules.

---

## 13. Literature Review

The literature relevant to this study falls into four groups.

### Indian index-option risk premia
Recent NIFTY research documents volatility-risk-premium behavior but emphasizes implementation friction and structural regime changes. [1,2]

### Transaction costs
Option strategy and replication literature repeatedly demonstrates that proportional transaction costs alter the economic result and the attainable strategy risk profile. [8-10]

### Expected shortfall
Expected shortfall is specifically designed to capture tail losses that average returns and VaR can understate. [6,7]

### Regime dependence
The post-2024 Indian derivatives environment has undergone material contract and market-structure changes. Recent 2026 reporting also describes proposed revisions to expiry-day settlement arrangements in response to expiry-related volatility. [11] This strengthens the case for regime separation rather than pooling all observations blindly.

---

## 14. Discussion

### 14.1 Economic interpretation

Under the locked primary specification, both indices show positive sample mean net P&L. This is useful evidence that the rule can produce favorable realized outcomes on the selected sample, but the uncertainty intervals include zero and the dispersion is much larger than the mean.

### 14.2 Why the MC gate should not be treated as a guarantee

The moderate positive MC-EV/P&L correlation shows that a positive model expectation is associated with better realized outcomes on average, but the relationship is far from deterministic. The gate filters trades; it does not remove tail risk.

### 14.3 Execution is central

The 2-point-per-leg primary friction is economically significant. NIFTY is particularly sensitive because the point-based slippage translates into a substantial rupee impact under historical lot sizes. This is consistent with the broader option-strategy literature in which transaction costs can change attainable performance. [8-10]

### 14.4 Tail losses matter more than headline hit rate

A 66.7% NIFTY profitable-trade share and 77.0% SENSEX profitable-trade share coexist with ES95 losses of tens of thousands of rupees. A strategy can win frequently and still have a fragile mean due to a small number of large losses.

### 14.5 Cross-index differences are not precisely identified

The SENSEX sample mean is higher, but the cross-index interval spans zero. Differences in lot size, strike spacing, liquidity and execution economics are plausible contributors, but this sample is not large enough to attribute the difference causally.

### 14.6 What the current study can and cannot claim

It can claim:
- reproducible implementation;
- successful leakage and chronology validation;
- positive sample means under the locked primary calibration;
- strong tail-risk presence;
- material execution and NIFTY calibration sensitivity.

It cannot claim:
- a statistically precise positive population mean;
- calibration-invariant robustness for NIFTY;
- production readiness;
- guaranteed future profitability.

### 14.7 Calibration setting and why it is kept common

Phase 8 shows a material calibration sensitivity for NIFTY: the nine tested settings produce mean net P&L from approximately ₹13 to ₹1,469 per trade. SENSEX is positive across all nine settings, with means from approximately ₹1,641 to ₹2,773. These differences are informative about robustness, but they do not justify choosing one setting for NIFTY and another for SENSEX from the same historical evaluation sample. Doing so would be post hoc parameter selection. The study therefore retains the same locked primary setting—756 sessions and 5,000 paths—for both indices. Instrument-specific calibration remains a future research question requiring a pre-registered selection rule and genuinely unseen validation data.

---

## 15. Strengths

1. The rule was locked before final result interpretation.
2. The primary workflow preserves the pre-signal information set.
3. Historical lot-size changes are modeled explicitly.
4. The gate is gross MC-EV > 0 before execution friction.
5. Execution uses a common timestamp strictly after the signal.
6. The requested 2-point/leg slippage is applied directly.
7. ES95/ES99 and drawdown are reported rather than only average P&L.
8. NIFTY and SENSEX are analyzed separately before comparison.
9. Errors are logged and corrected in version control.
10. Each research phase has a separate branch and workflow.

---

## 16. Limitations

1. The selected intraday option history begins in October 2024. [3]
2. The intraday source is an aggregation from Upstox data rather than a direct raw exchange archive. [3]
3. The production bootstrap history uses a secondary daily-price source.
4. The sample contains only 124 executed trades across both indices.
5. The mean P&L confidence intervals include zero.
6. The sample is concentrated in 2025 and 2026-to-date.
7. The raw-option MC calibration matrix is complete, but the NIFTY result is materially calibration-sensitive and therefore is not promoted as robust across calibration choices.
8. All-in statutory/venue costs remain a robustness layer rather than a claim of exact live account-specific costs.
9. Historical FII/DII/global-regime synchronization was not forced where reliable historical data were unavailable.
10. No paper-trading or live execution validation was performed.

---

## 17. Conclusion

Phase 8 is now the authoritative methodological revalidation of the historical sample. Under the common locked primary calibration (756 sessions × 5,000 paths), the raw-option recomputation produced:

- NIFTY: **₹966.46 mean net P&L/trade**, or **₹936.45** under the enhanced friction layer;
- SENSEX: **₹2,508.06 mean net P&L/trade**, or **₹2,478.65** under the enhanced friction layer.

The block-bootstrap 95% mean-P&L intervals include zero for both indices: NIFTY **₹-1,985.18 to ₹3,955.42** and SENSEX **₹-479.84 to ₹5,530.85**. NIFTY is materially calibration-sensitive across the 18-scenario matrix; SENSEX remains positive across all nine tested calibration configurations. Exact theoretical quantile strikes were not observed in the primary trades, with mean absolute displacement of 12.14 index points for NIFTY and 24.83 for SENSEX.

The scientifically supported conclusion is therefore:

> **The historical sample provides reproducible positive sample means under the locked primary assumptions, with substantial tail risk and execution/calibration sensitivity; it does not establish a stable population-level or production-ready trading edge.**

The Phase 7 results remain preserved as a historical baseline. Phase 8 does not retune the strategy and does not select different settings for NIFTY and SENSEX. The next high-value step is genuinely unseen prospective validation with the 756/5,000 rule frozen, followed by exchange-grade data extension and synchronized regime analysis.

---

## 18. Future Research

### Priority 1 — Prospective frozen validation
Evaluate genuinely unseen future expiries using the locked 756-session/5,000-path rule without re-estimation or index-specific retuning.

### Priority 2 — Exchange-grade historical extension
Extend NIFTY and SENSEX intraday option data before October 2024 where legally/reproducibly possible.

### Priority 3 — Full all-in cost model
Add:
- GST;
- exchange transaction charges;
- SEBI fees;
- stamp duty;
- clearing charges;
- realistic bid/ask rather than fixed point slippage.

### Priority 4 — Regime-conditioned analysis
Synchronize:
- India VIX;
- FII/FPI/DII;
- global equity returns;
- Cboe VIX;
- USD/INR;
- gold;
- market breadth.

### Priority 5 — Out-of-sample forward test
Lock all parameters and evaluate unseen future expiries without re-estimation.

---

## References

[1] Ashwin R. John (2026), *Harvesting the Volatility Risk Premium in Nifty Index Options: Out-of-Sample Evidence and the Post-2024 Regulatory Regime Break*. DOI 10.13140/RG.2.2.20010.99528.

[2] Sumin Pillai (2026), *Trading the Volatility Risk Premium on Nifty 50: Strategy Backtest with Realistic Frictions*. SSRN 6876580.

[3] rissin, *nse-options-intraday*, Hugging Face dataset card.

[4] NSE India, *All Reports — Derivatives*, including historical F&O bhavcopy, contract-wise price/volume, settlement, participant-wise reports and FII derivatives statistics.

[5] NSE India, *FII/FPI & DII Trading Activity*.

[6] Du, Z. & Escanciano, J.C. (2016), *Backtesting Expected Shortfall: Accounting for Tail Risk*, Management Science, 63(4), 940-958.

[7] Pochart, B. & Bouchaud, J.P. (2004), *Option Pricing and Hedging with Minimum Local Expected Shortfall*, Quantitative Finance, 4(5), 607-618.

[8] Boyle, P. (1992), transaction-cost-aware discrete-time option replication.

[9] Toft, K.B. (2009), option replication and transaction costs.

[10] Chidambaran (2007), Monte Carlo density estimation for option strategies under transaction costs.

[11] Reuters (15-Sep-2026), India derivatives-settlement reform proposals and expiry-day volatility context.

---

## Reproducibility Links

- Locked strategy: `research/STRATEGY_SPEC.md`
- Research protocol: `research/RESEARCH_PROTOCOL.md`
- Data manifest: `research/data/SOURCE_MANIFEST.md`
- Contract schedule: `research/data/CONTRACT_SCHEDULES.md`
- Cost schedule: `research/data/COST_SCHEDULE.md`
- NIFTY results: `research/results/NIFTY_FINAL_BACKTEST.md`
- SENSEX results: `research/results/SENSEX_FINAL_BACKTEST.md`
- Phase 6 robustness: `research/results/PHASE6_ROBUSTNESS_RESULTS.md`
- Error log: `research/logs/ERROR_LOG.md`
- Research log: `research/logs/RESEARCH_LOG.md`
- Phase 6 workflow: `.github/workflows/phase-6-robustness.yml`


---

## 15. Methodological Revalidation Amendment

### 15.1 Development versus validation

The research history is separated into strategy-development/tuning, locked-rule specification, historical locked-rule evaluation, and prospective or genuinely unseen validation if a clean date split is available. The existing 63 NIFTY and 61 SENSEX observations remain descriptive outputs of the locked implementation, but are not represented as independently out-of-sample evidence if those observations were available during development.

### 15.2 MC-EV chronology audit

Phase 8 records the gate-premium timestamp separately from the later execution timestamp and verifies that the gate uses the signal-time information set. Gate-timestamp validity was 100% in the primary NIFTY and SENSEX scenarios.

### 15.3 Dependence-aware inference

The iid trade-bootstrap interval remains a descriptive secondary measure. Phase 8 adds expiry-cluster/block-bootstrap intervals to preserve temporal dependence and regime clustering. The paired NIFTY/SENSEX analysis found only one common signal date and therefore did not support paired inference.

### 15.4 Strike mapping and capital

Phase 8 quantified strike displacement, uniqueness, payoff structure and ES95 sizing examples. Final strike uniqueness was 100% in the primary scenarios; exact theoretical-target strikes were 0%; mean absolute displacement was 12.14 NIFTY points and 24.83 SENSEX points. The ES95 sizing proxy remains a risk indicator rather than a full broker margin model.

### 15.5 Coverage dates

The 2026 results are coverage-to-date for the available intraday dataset, not full calendar-year results through 21 September 2026. The available NIFTY and SENSEX samples currently end in July 2026.

### 15.6 Raw-option calibration matrix

Phase 8 reran the full raw-option chain for all 18 scenarios: 504/756/1008 bootstrap sessions × 1,000/5,000/10,000 paths × NIFTY/SENSEX. The matrix was executed successfully in run 35641908887. It is treated as sensitivity/revalidation, not as a parameter-selection exercise.


### 15.7 Contract and brokerage qualification

Historical NIFTY lot size cannot be treated as a simple expiry-date constant because NSE revisions apply by contract cohort/effective date. Phase 8 therefore prefers contract-level lot size when present in the raw data and records the source; otherwise the fallback schedule is explicitly identified as a limitation. Separately, Paytm Money brokerage depends on account vintage and published pricing has changed over time, so ₹20/order is retained as the study's historical assumption while ₹10/₹15/₹20 sensitivity is reported. The study does not claim that ₹20 is universal for every Paytm Money account.


### 15.8 Enhanced friction model

The primary headline result remains based on the locked 2-point-per-leg slippage plus brokerage and STT model. Phase 8 additionally computes an enhanced statutory/venue-friction layer incorporating premium-based exchange transaction charges, SEBI turnover fee, buyer-side stamp duty and GST on broker/venue service fees. Because Paytm Money brokerage is account-vintage dependent, ₹10/₹15/₹20 per order is also treated as a sensitivity range. These enhanced results are robustness diagnostics rather than a claim that every account incurs exactly the same all-in charges.


### 15.9 Capital, Margin Proxy, and Return Interpretation (Phase 9)

Phase 9 uses the locked Phase 8 primary trade files without changing the strategy or calibration. The objective is to distinguish realized P&L from the capital required to carry the strategy.

| Measure | NIFTY | SENSEX |
|---|---:|---:|
| Mean net P&L / trade | ₹966.46 | ₹2,508.06 |
| ES95 loss | ₹31,753.75 | ₹26,807.30 |
| ES99 loss | ₹38,992.43 | ₹38,352.77 |
| Maximum historical drawdown | ₹61,576.41 | ₹66,886.42 |
| Maximum simultaneous positions | 2 | 2 |
| Conservative research capital proxy | ₹63,507.51 | ₹66,886.42 |
| Mean P&L / ES95 | 3.04% | 9.36% |
| Mean P&L / conservative capital proxy | 1.52% | 3.75% |

The conservative research capital proxy is defined as max(ES95 × observed maximum concurrent positions, observed maximum drawdown). It is a historical P&L-derived reserve and must not be described as exchange or broker margin. The mean P&L/ES95 figures are risk-capital ratios per completed trade. The lower 1.52% and 3.75% ratios use the conservative reserve that accounts for both overlap and historical drawdown.

The mean net entry premium cashflows were credits of ₹2,957.76 for NIFTY and ₹4,686.03 for SENSEX, while the maximum observed long-leg premium cash outlays were approximately ₹38,964 and ₹38,905 respectively. The negative net premium does not imply negligible capital because the short options require exchange-defined initial margin.

NSE Clearing describes equity-derivatives initial margin as portfolio-based SPAN with a 99% one-day VaR framework, and Paytm Money states that its option-writing margin is exchange-defined and that its margin calculator accounts for SPAN, exposure, and hedge benefits. Because the Phase 8 trade files lack date-specific SPAN risk arrays and broker margin snapshots, this study does not claim an exact historical Paytm Money/NSE/BSE margin figure.

The simple linear annual P&L-to-capital ratios (53.96% NIFTY and 129.93% SENSEX) are mechanical turnover-normalized historical ratios, not compounded returns or forecasts. They are shown only to quantify how often the historical trade opportunity reused the same research capital proxy.

See `research/PHASE9_RESULTS.md` and `research/data/PHASE9_CAPITAL_MARGIN_SOURCE_AUDIT.md` for the complete capital definitions and source audit.


---

## Publication record

This version consolidates the authoritative Phase 8 raw-option revalidation and Phase 9 capital interpretation. For reproducibility, the repository retains the earlier manuscript, supplements, results, plans, research log, and error log. The publication does not redistribute the large raw-option dataset; it records the immutable dataset revision and workflow provenance instead.
