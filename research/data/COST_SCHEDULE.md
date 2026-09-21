# Trading Cost Schedule

## Paytm Money brokerage

Primary assumption: Rs 20 brokerage per executed entry order.

Paytm Money's January 2025 pricing update states that brokerage was aligned to a flat Rs 20 across all segments effective 15-Jan-2025. The primary research therefore uses Rs 20 per executed entry order across the study window; pre-2025 account-vintage alternatives are a sensitivity, not the primary estimate.

Source: https://www.paytmmoney.com/blog/all-new-paytm-money-updates-revisions-and-more/

## Securities Transaction Tax (STT)

The statutory STT schedule is date-effective:
- Before 01-Oct-2024: 0.0625% on sale of an option premium.
- 01-Oct-2024 through 31-Mar-2026: 0.10% on sale of an option premium.
- From 01-Apr-2026: 0.15% on sale of an option premium.
- Exercise/expiry STT is modeled on intrinsic value for long ITM options using 0.125% before 01-Apr-2026 and 0.15% from 01-Apr-2026.

Sources:
- Finance (No. 2) Act 2024: https://incometaxindia.gov.in/documents/20117/6476327/finance-no.2-act-2024.pdf
- Finance Bill 2026 / Budget 2026 STT revision: https://www.incometaxindia.gov.in/documents/20117/15766092/Finance_Bill-2026.pdf
- Budget 2026 STT FAQ: https://incometaxindia.gov.in/Documents/Budget2026/FAQs-Budget-2026.pdf

## Included vs excluded

Included in the primary model:
- 2 option points slippage per execution leg.
- Brokerage for four entry orders.
- Entry STT on short option sales.
- Expiry/exercise STT on long ITM options.

Excluded from the primary model unless separately stress-tested:
- GST on brokerage.
- SEBI turnover fees.
- Stamp duty.
- Exchange transaction charges.
- Clearing charges.
- Slippage beyond the fixed 2-point rule.

The exclusions are deliberate so the requested primary rule remains isolated; an all-in sensitivity should be added in Phase 6 before final conclusions.
