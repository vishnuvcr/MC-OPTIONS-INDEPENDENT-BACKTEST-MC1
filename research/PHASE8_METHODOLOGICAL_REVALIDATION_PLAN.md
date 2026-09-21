# Phase 8 — Methodological Revalidation

## Trigger
External scientific review identified methodological-framing and validation gaps in the Phase 7 manuscript. This phase is corrective revalidation; it does not alter the locked BATMAN rule.

## Required work
1. Reconstruct and document the full strategy-development/tuning history.
2. Separate development/tuning data from any genuinely unseen validation data.
3. Audit MC-EV chronology and prove the gate cannot depend on the later execution premium.
4. Add trade-level provenance fields for signal, gate-premium, and execution timestamps.
5. Add expiry-cluster/block-bootstrap uncertainty and paired NIFTY/SENSEX comparisons where dates are comparable.
6. Complete raw-option MC calibration sensitivity: 504/756/1008 sessions × 1,000/5,000/10,000 paths, rerunning the full chain.
7. Quantify strike-mapping robustness, displacement and collisions.
8. Add payoff, margin/capital, ES sizing and tail/gap analysis.
9. Reframe slippage as a research stress assumption unless independently validated from executable bid/ask data.
10. Clarify dataset coverage dates versus manuscript date.
11. Update manuscript and README while preserving prior results and errors.

## Acceptance criteria
- No unsupported claim of pre-specification or no parameter search.
- No post-signal information can enter the MC-EV gate.
- Cluster-aware uncertainty is reported.
- Raw-option calibration matrix is executed or explicitly blocked with reproducible reason.
- Capital/risk interpretation is numerically defined.
- Manuscript distinguishes sample evidence from independent out-of-sample evidence.

## Status
**Blocked by GitHub-hosted runner capacity.** Implementation and validation controls are complete, but the authoritative single-runner workflow remains queued (run 102). No Phase 8 numerical result is accepted until that run executes. This is an infrastructure stop condition, not a model-result conclusion.
