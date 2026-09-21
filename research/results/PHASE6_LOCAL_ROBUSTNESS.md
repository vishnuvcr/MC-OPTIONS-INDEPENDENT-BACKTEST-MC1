# Phase 6 — Local Robustness Diagnostics

This file records diagnostics computed from the already-validated Phase 2 trade-level artifact while GitHub Actions was queued.

Source artifact:
- GitHub Actions run 14
- dataset revision `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`
- 63 NIFTY executed trades
- 61 SENSEX executed trades

## Bootstrap confidence intervals for mean net P&L

| Index | Mean net | 95% bootstrap CI |
|---|---:|---:|
| NIFTY | ₹1,183.66 | -₹1,570.02 to ₹3,719.11 |
| SENSEX | ₹2,507.53 | -₹366.61 to ₹5,168.90 |

These intervals are descriptive uncertainty intervals for the observed trade sample, not proof of future performance.

## Slippage stress

| Index | 0 pts | 1 pt | 2 pts primary | 3 pts | 5 pts |
|---|---:|---:|---:|---:|---:|
| NIFTY mean net/trade | ₹1,959.27 | ₹1,571.46 | ₹1,183.66 | ₹795.85 | ₹20.24 |
| SENSEX mean net/trade | ₹2,741.45 | ₹2,624.49 | ₹2,507.53 | ₹2,390.57 | ₹2,156.64 |

At 5 points per execution leg, the NIFTY sample is approximately flat in mean net P&L, while SENSEX retains positive sample mean. This is a stress result, not a forecast.

## Cross-index bootstrap comparison

Observed mean difference (NIFTY minus SENSEX): **-₹1,323.87/trade**.

95% bootstrap interval for the difference: **-₹5,160.73 to ₹2,467.13**.

In the paired-independent trade bootstrap used here, the proportion of resamples with NIFTY mean above SENSEX mean was about 24.8%. This is not a ranking or recommendation; it only describes uncertainty around the observed mean difference.

## Year effects

Both indices show negative mean net P&L in the limited 2024 sub-sample and positive means in 2025 and 2026-to-date. The 2026 contribution is especially sensitive for SENSEX because the available option sample ends in July 2026.

## What this local diagnostic cannot establish

The local artifact does not contain the raw option-chain windows needed to reconstruct how changing the 756-session bootstrap window or Monte Carlo path count changes the gate and strike selection. Those dimensions remain delegated to the parallel GitHub Actions Phase 6 matrix.

Therefore this file is **partial Phase 6 evidence**, not the final robustness result.
