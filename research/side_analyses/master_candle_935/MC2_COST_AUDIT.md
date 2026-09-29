# MC2 — Paytm Money / NSE Full Friction Audit

**Status:** IN PROGRESS  
**Branch:** `side-analysis/master-candle-935-mc2-cost-audit`  
**Workflow:** authoritative execution run 36523421079

## Cost model being tested

- Paytm Money brokerage: ₹20 per executed order. Paytm Money states that its flat ₹20 brokerage across segments began 15 Jan 2025; older accounts may have retained legacy ₹10 F&O pricing, so ₹20 is intentionally conservative for the research baseline.
- NSE equity-options transaction charge: ₹3,553 per crore of premium value each side from 1 Mar 2026, equivalent to 0.03553% each side.
- SEBI turnover fee: 0.0001% of turnover.
- Equity-options stamp duty: 0.003% on the buyer.
- GST: 18% on brokerage plus applicable exchange/SEBI service charges.
- STT: 0.0625% before 1 Oct 2024, 0.10% from 1 Oct 2024 through 31 Mar 2026, and 0.15% from 1 Apr 2026.
- Slippage: 1 option point adverse on entry and 1 option point adverse on exit.

## Source notes

Paytm Money's current F&O FAQ states ₹10 per executed F&O order, while its 2024/2025 pricing communications document the subsequent flat-₹20 structure for newer/current pricing. The research uses ₹20/order conservatively rather than inferring the user's account-specific historical tariff.

NSE documents the ₹3,553/crore equity-options premium transaction-charge level effective 1 Mar 2026 and the STT changes effective 1 Apr 2026. Exact historical NSE transaction-charge schedules before the uniform October 2024 regime are more complex; MC2 therefore treats the fixed 0.03553% transaction charge as a conservative friction stress for earlier years rather than claiming it is the exact historical member tariff.

## Research purpose

MC2 is not allowed to retune the strategy. It only asks whether the already-frozen MC1 result changes materially after a more complete friction stack.

If the strategy remains negative, no optimization is authorized inside this side-analysis branch. The next permitted work is robustness/interpretation testing or closure.
