# Error Log

| Date | Phase | Severity | Error / issue | Resolution | Status |
|---|---|---|---|---|---|
| 2026-09-21 | 0 | Informational | Direct git clone failed because the runtime could not resolve github.com. | Use GitHub repository connector for reads/writes and GitHub Actions for remote execution/data acquisition. | Resolved |
| 2026-09-21 | 0 | Informational | Repository contents API reports repository is empty. | Initialize governance/scaffold from an empty default branch. | Resolved |

No unresolved critical errors at Phase 0 start.

| 2026-09-21 | 1 | Informational | One large implementation write did not pass the execution environment guard. | Split the Phase 1 implementation into smaller files; no research-method change was made. | Resolved |

| 2026-09-21 | 1 | Error | Hugging Face files were downloaded but workflow QA could not see workspace copies because hardlink materialization was invalid across the cache/workspace boundary. | Replace hardlinking with shutil.copy2 and pin hf_hub_download to the resolved dataset revision. | Resolved in commit 294b2bda |

| 2026-09-21 | 2 | Error | Phase 2 pytest could not import src because repository root was not on the test import path. | Added tests/conftest.py to insert the repository root into sys.path. | Resolved |

| 2026-09-21 | 2 | Error | GitHub Actions cache key rejected comma-separated year input. | Cache key changed to dataset-revision-only; year selection still controls downloads. | Resolved |

| 2026-09-21 | 2 | Error | First Phase 2 full run produced zero trades: execution join used repeated pandas merges and signal timestamps mixed naive/IST-aware values. | Rewrote the four-leg execution join as one wide timestamp join, normalized all timestamps to Asia/Kolkata, and enforced the MC-EV gate before execution. | Fixed |
