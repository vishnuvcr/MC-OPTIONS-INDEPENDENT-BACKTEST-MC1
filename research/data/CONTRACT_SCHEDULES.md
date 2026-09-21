# Historical Contract Schedules

This file contains the date-effective assumptions required to avoid using current contract specifications for historical trades.

## NIFTY 50 lot size

- Through the first revised contracts in 2024, NIFTY moved from a 50-unit lot to a 25-unit lot for contracts introduced after the April 2024 effective date.
- New index contracts introduced from November 20, 2024 moved NIFTY from 25 to 75 units.
- From late 2025, new NIFTY contracts move from 75 to 65 units; weekly/monthly contracts transition according to the exchange effective-date schedule.

Implementation rule: resolve lot size from the expiry/contract introduction schedule, never from today's lot size.

## SENSEX lot size

- Historical SENSEX contracts used a 10-unit lot before the November 2024 contract revision.
- BSE revised the market lot for newly introduced SENSEX index derivatives to 20 units from November 20, 2024; existing unexpired contracts retained their previous lot until expiry.

Implementation rule: resolve lot size from the specific contract's effective-date regime.

## Expiry weekday

- NIFTY's expiry weekday changed in 2025; the historical contract record is authoritative.
- SENSEX expiry conventions changed during 2024–2025; the specific historical contract expiry field is authoritative.

No workflow is permitted to infer expiry weekday from a current fixed weekday when a contract expiry field is available.

## Source references

- NSE contract/expiry circular: NSE/FAOP/68747, 25-Jun-2025.
- NSE lot-size revision notices for April 2024, November 2024, and late 2025.
- BSE Notice 20241021-13 for the November 2024 SENSEX lot-size revision.
- BSE/NSE expiry-day notices as archived and recorded in the research bibliography.
