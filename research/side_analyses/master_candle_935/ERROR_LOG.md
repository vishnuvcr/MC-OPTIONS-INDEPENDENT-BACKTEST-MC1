# Error Log — Master Candle 09:35–09:45

| Date | Phase | Issue | Resolution / disposition |
|---|---|---|---|
| 2026-09-29 | MC0 | Direct YouTube URL could not be fetched by the available web cache. | Treat the user’s strategy transcript/summary as the supplied source of record; do not claim the video itself was independently verified. |
| 2026-09-29 | MC0 | Existing BATMAN intraday dataset starts Oct-2024 and cannot cover 2021–2026. | Identify a separate 2021–2026 candidate dataset; keep provenance caveat explicit. |
| 2026-09-29 | MC0 | “Selling ATM directional options” conflicts with “option buying” and premium-rise examples. | Preserve long-option buying as the primary hypothesis; retain short-option interpretation as a separate audit scenario. |
| 2026-09-29 | MC0 | 25-day EMA timeframe not explicit. | Default to prior-day daily EMA; make 10-minute EMA a separate sensitivity scenario. |
| 2026-09-29 | MC0 | Published yearly profit figures do not reconcile to stated ₹2.76 crore total. | Require reconstruction of missing years/definitions before accepting headline totals. |

| 2026-09-29 | MC1 | The available GitHub connector did not surface a workflow-dispatch/run result for the new baseline workflow. | Do not treat the runner as numerically completed. Keep MC1 status IN PROGRESS until an authoritative workflow result/artifact is available. |

| 2026-09-29 | MC1 | Baseline runner initially encoded 10 lots, inconsistent with user's later sizing instruction. | Corrected constant to LOTS=1 and logged the change; no numerical result from the old 10-lot runner is accepted. |

| 2026-09-29 | Infrastructure | Attempted unavailable GitHub connector function for default-branch lookup. | Stopped that call and continued using available branch/PR/workflow primitives; no research result affected. |

| 2026-09-29 | Infrastructure | GitHub Actions run remains unavailable through the connector after adding a main-branch execution path; local Git clone also failed because outbound GitHub DNS/network access is unavailable in the sandbox. | No numerical backtest result accepted. Runner remains ready for an authoritative Actions execution. |

| 2026-09-29 | MC1 | Serial full-universe option processing was effectively stalled/opaque. | Replaced with six parallel year-partitioned workers; all six completed successfully in authoritative run 36522552275. |
| 2026-09-29 | MC1 | 2026 source coverage ends 2026-07-01 rather than requested 2026-08-04. | Recorded explicitly in result; no extrapolation beyond observed source coverage. |
| 2026-09-29 | MC1 | Baseline friction model is not yet the complete Paytm Money/NSE statutory stack. | MC1 result is labelled baseline discovery; MC2 will reconcile full historical/current charges. |

| 2026-09-29 | MC1 infrastructure | Yearly artifacts were hundreds of MB because the HF market-data cache was uploaded with each result. | Workflow changed to remove `hf_cache` before upload and retain only summary/signals/trades. Prior numerical outputs remain provisional until the clean rerun completes. |

| 2026-09-29 | MC2 execution grid | Four variant calculations succeeded but artifact upload failed because exit-time colons were used in artifact names. | Artifact names changed to sanitized matrix job indexes; incomplete outputs are not accepted. |
