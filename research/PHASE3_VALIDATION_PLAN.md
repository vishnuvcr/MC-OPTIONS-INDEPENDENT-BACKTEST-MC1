# Phase 3 Validation Plan

## Required checks

1. Unit-test all mathematical primitives.
2. Check bootstrap chronology and confirm no post-signal data enters the 756-session return set.
3. Check execution timestamps are strictly after 09:30 and common to all four legs.
4. Check all four mapped strikes are unique.
5. Check the MC path count is exactly 5,000 for the primary run.
6. Check the gross MC-EV gate is applied before execution.
7. Check slippage direction is correct for buys and sells.
8. Check historical lot-size logic is date-aware.
9. Confirm current lot size is never substituted for historical contracts.
10. Preserve failed eligibility cases in error logs.

## Acceptance

Phase 3 passes only when the automated tests and contract checks are green and there are no unresolved critical validation errors.
