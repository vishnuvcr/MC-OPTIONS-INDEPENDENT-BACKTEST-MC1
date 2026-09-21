# Prospective Frozen Validation Protocol

## Objective

Evaluate the frozen BATMAN specification on expiries that are genuinely unseen during strategy development.

## Freeze requirements

Before the first prospective expiry:
- strategy rule version is frozen;
- MC bootstrap window/path count are frozen;
- strike mapping and tie-breaking are frozen;
- 09:30 gate-premium source is frozen;
- execution definition and slippage model are frozen;
- cost schedule/version is frozen;
- lot-size/expiry metadata source is frozen;
- no threshold or entry/exit tuning is allowed.

## Data firewall

Development-era observations must not be used to choose or alter parameters. Prospective expiry results must be appended in chronological order without re-estimation.

## Primary outcomes

Report:
- trade eligibility rate;
- gross MC-EV;
- realized gross and net P&L;
- mean/median and confidence intervals;
- ES95/ES99;
- drawdown;
- slippage/cost sensitivity;
- execution-quality diagnostics;
- strike displacement;
- regime stratification.

## Stop rule

Prospective validation ends at the pre-agreed expiry count or calendar date. No mid-study rule tuning is permitted.
