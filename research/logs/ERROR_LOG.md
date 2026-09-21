# Error Log

| Date | Phase | Severity | Error / issue | Resolution | Status |
|---|---|---|---|---|---|
| 2026-09-21 | 0 | Informational | Direct git clone failed because the runtime could not resolve github.com. | Use GitHub repository connector for version control and GitHub Actions for remote execution/data acquisition. | Resolved |
| 2026-09-21 | 0 | Informational | Repository contents API initially reported an empty repository. | Initialized governance/scaffold from the empty default branch. | Resolved |
| 2026-09-21 | 1 | Informational | One large Phase 1 implementation write did not pass the execution-environment guard. | Split the implementation into smaller versioned files. | Resolved |
| 2026-09-21 | 1 | Error | Hugging Face files were downloaded but workspace QA could not see hard-linked copies. | Replaced hardlinking with `shutil.copy2` and pinned dataset revision. | Resolved |
| 2026-09-21 | 2 | Error | Pytest could not import `src` because repository root was absent from the test path. | Added `tests/conftest.py`. | Resolved |
| 2026-09-21 | 2 | Error | GitHub cache key rejected comma-separated year input. | Switched cache key to dataset revision identity. | Resolved |
| 2026-09-21 | 2 | Error | First model run produced zero trades because of repeated four-leg merge logic and mixed timestamp timezone states. | Rewrote the four-leg execution join and normalized timestamps to Asia/Kolkata. | Resolved |
| 2026-09-21 | 3 | Error | Synthetic leakage fixture used a 1,000-date index with an 800-value close vector. | Corrected fixture length; production code unchanged. | Resolved |
| 2026-09-21 | 4 | Error | NIFTY summary formatter had an unterminated multiline string literal. | Replaced multiline literal assembly with explicit string construction. | Resolved |
| 2026-09-21 | 6 | Tooling | Initial Phase 6 workflow writer hit JavaScript template interpolation on shell variables. | Rewrote workflow using literal line-array generation. | Resolved |
| 2026-09-21 | 6 | Error | Phase 6 robustness report writer had an unterminated multiline string literal. | Replaced report assembly with `chr(10)`-based joins. | Resolved |
| 2026-09-21 | 6 | Workflow design | Matrix scenarios initially used identical artifact filenames, risking overwrite during merged artifact download. | Scenario names were made unique and primary scenario explicitly identified as 756/5,000. | Resolved |
| 2026-09-21 | 6 | Workflow scheduling | Phase 6 created 10 queued matrix jobs and the GitHub Actions runner queue did not start them. | Collapsed the matrix to two runner jobs, each executing five scenarios sequentially; manual workflow remains available. | Infrastructure limitation |
| 2026-09-21 | 6 | Environment | Direct local access to huggingface.co was unavailable from the execution container. | Retained pinned dataset revision and used completed GitHub Actions artifacts for validated trade-level diagnostics. | Infrastructure limitation |

No unresolved strategy/model correctness error remains from Phases 0-5. The only unresolved item is the infrastructure-constrained raw-option MC calibration sensitivity matrix described in the Phase 6 results.

| 2026-09-21 | 8 | Methodology | Phase 7 stated the final rule was pre-specified and that no parameter search occurred, but earlier BATMAN development included joint tuning. | Reframe development/tuning → rule freeze → validation; classify existing results according to whether their dates were seen during development. | Open |
| 2026-09-21 | 8 | Methodology | MC-EV premium timestamp was not explicit enough to rule out post-signal execution-price leakage. | Add timestamp-level gate audit and require the gate premium to be sourced from the 09:30 information set. | Open |
| 2026-09-21 | 8 | Statistics | Primary uncertainty used iid trade bootstrap only. | Add expiry-cluster/block bootstrap and paired date-level NIFTY/SENSEX comparison. | Open |
| 2026-09-21 | 8 | Execution | First common executable observation is not equivalent to four-leg simultaneous fill. | Add bid/ask/spread/fill sensitivity where data permit and label fixed slippage as a stress assumption. | Open |
| 2026-09-21 | 8 | Risk | Capital/margin and payoff-bound analysis was incomplete. | Add payoff diagrams, margin/capital requirement, ES sizing example, and tail/gap analysis. | Open |
| 2026-09-21 | 8 | Robustness | Raw-option MC calibration matrix was not executed. | Re-run the full chain for all 18 calibration scenarios (9 per index) when runner capacity permits. | Open |
| 2026-09-21 | 8 | Planning | Phase 8 plan initially referred to 27 calibration scenarios. | Corrected arithmetic: 3 bootstrap windows × 3 path counts = 9 scenarios per index, 18 total across NIFTY and SENSEX. | Resolved |\n| 2026-09-21 | 8 | Contract metadata | Historical NIFTY lot-size rules include contract-cohort effective dates; expiry-only fallback cannot prove the correct lot size for every contract. | Prefer contract-level lot_size from raw data and record source; otherwise require contract-master resolution. | Open |
| 2026-09-21 | 8 | Brokerage | Paytm Money published pricing is account-vintage dependent; current FAQ states ₹10/order while 2023 new-user pricing stated ₹20/order. | Keep ₹20/order as the locked historical assumption and add ₹10/₹15/₹20 sensitivity; do not present ₹20 as universal. | Open |
| 2026-09-21 | 8 | Test failure | Updated execution engine now returns execution volumes as a third tuple element, but legacy test_validation expected two. | Updated test to unpack timestamp, prices, volumes; no production logic bypassed. | Resolved |
| 2026-09-21 | 8 | Workflow scheduling | Legacy Phase 6 PR workflow continued consuming runners while Phase 8 was validating, creating queue contention. | Added a Phase 8 branch guard to legacy Phase 6 jobs; existing in-flight run remains a historical infrastructure event and is not used for Phase 8 results. | Mitigated |
| 2026-09-21 | 8 | Lot-size model | Original fallback used 25 through 2024-12-31 and 65 from 2025-12-25, which did not match NSE's cohort-effective dates. | Corrected to 25 before 2024-11-20, 75 from 2024-11-20 through 2026-01-05, and 65 from 2026-01-06; contract-level source still preferred when available. | Resolved |
