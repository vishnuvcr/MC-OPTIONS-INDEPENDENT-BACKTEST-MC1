# Contract and cost source audit — Phase 8

## NSE lot-size evidence

NSE Circular 128/2024 (18-Oct-2024) revised NIFTY 50 market lot from 25 to 75 for new index derivative contracts introduced from 20-Nov-2024 onward.

NSE Circular 176/2025 (03-Oct-2025) revised NIFTY 50 market lot from 75 to 65. The circular states that weekly/monthly contracts keep the existing lot size through the 30-Dec-2025 expiry and the first revised weekly expiry is 06-Jan-2026; the first revised monthly expiry is 27-Jan-2026. Quarterly/half-yearly handling is separately specified.

**Implication:** expiry-date-only lot-size logic is not sufficient to establish historical lot size for every contract cohort. Phase 8 now prefers a contract-level `lot_size` field from the raw dataset when present and records `lot_size_source`. When that field is absent, the fallback schedule is explicitly identified as a limitation requiring contract-master resolution.

## Paytm Money brokerage evidence

Paytm Money's published 2023 pricing update states that new users opening accounts on/after 25-Aug-2023 were charged ₹20 per executed order for Stock Delivery/Intraday/F&O, while older account vintages retained lower rates.

Paytm Money's current F&O FAQ states ₹10 per unique executed order. Therefore, a single universal brokerage rate is account-plan dependent and should not be presented as an exchange-invariant historical fact.

**Primary backtest convention:** retain ₹20/order as the locked historical cost assumption used in Phases 2-7, but report ₹10/₹15/₹20 order brokerage sensitivity in Phase 8. This is a research assumption, not a claim about the user's personal Paytm Money tariff.

## Official sources

- NSE Circular 128/2024: https://nsearchives.nseindia.com/content/circulars/FAOP64625.pdf
- NSE Circular 176/2025: https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf
- Paytm Money 2023 pricing update: https://www.paytmmoney.com/blog/brokerage-charges-increase-from-25th-aug-23-existing-users-will-continue-on-old-brokerage-charges/
- Paytm Money current F&O FAQ: https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web


## STT evidence

Government of India Budget 2026 documentation states that STT on options premium and option exercise was proposed to rise to 0.15% from 0.10% and 0.125%, respectively, effective 1-Apr-2026. The repository cost engine uses those date-effective rates.

Earlier 2024 budget material records the prior option-sale STT change to 0.10%, consistent with the sample-period implementation from October 2024.


## Raw option dataset schema audit

The pinned Hugging Face dataset's intraday schema has 16 columns and does not include a lot_size field. Therefore the Phase 8 engine cannot use a contract-level lot-size field from this dataset. The corrected fallback schedule is now driven by the official NSE cohort dates rather than the earlier expiry-date thresholds.
