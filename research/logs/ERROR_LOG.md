[object Object]
| 2026-09-21 | 6 | Workflow scheduling | Pull-request triggers on completed phases caused every Phase 6 commit to queue redundant Phase 1-5 runs. | Completed-phase workflows are now manual-only; Phase 6 retains automatic PR validation plus manual dispatch. | Resolved |

| 2026-09-21 | 6 | Error | External market-context join failed because pandas used different datetime resolutions for trade and context keys. | Cast both merge keys to datetime64[ns] and added a regression test. | Resolved |
