# Phase 9 — Capital and Margin Source Audit

## Purpose
Document what can and cannot be called capital required for the BATMAN strategy.

## Exchange margin
NSE Clearing states that equity-derivatives initial margin is computed using the portfolio-based SPAN system. The SPAN framework evaluates combined futures/options portfolios under predefined price and volatility scenarios; the exchange also publishes SPAN risk parameter files. The published margin framework uses a 99% one-day VaR basis for initial margin.
Official source:
- NSE Equity Derivatives Margins: https://www.nseindia.com/static/products-services/equity-derivatives-margins
- NSE Clearing SPAN: https://www.nseindia.com/static/products-services/equity-derivatives-nse-clearing-span
- NSE SPAN risk parameter files / historical report access: https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files and https://www.nseindia.com/all-reports-derivatives

## Broker margin
Paytm Money documents that margin for option writing is exchange-defined and that initial margin comprises SPAN + exposure margin. Its margin calculator can evaluate multi-leg positions and hedge benefits.
Official sources:
- Paytm Money Margin Calculator: https://www.paytmmoney.com/blog/margin-calculator/
- Paytm Money F&O margin FAQ: https://www.paytmmoney.com/stocks/customer/fno-faq/margin-leverage/margin/what-is-margin-call-requirement-received-notification-email-from-paytm-money
- Paytm Money product page noting the multi-leg F&O margin calculator: https://www.paytmmoney.com/open-demat-trading-account

## Study limitation
The Phase 8 trade output stores executed option prices, quantities, lot sizes, dates, and realized P&L, but it does not store the historical SPAN risk array, exposure-margin parameter, or broker-specific haircut/margin snapshot for each entry date.
Accordingly:
- premium cash requirements can be reconstructed directly;
- historical P&L-derived ES95/ES99 and drawdown reserves can be reconstructed directly;
- actual historical NSE/BSE/Paytm Money margin cannot be claimed from Phase 8 data alone.

## Terminology lock
Use: ES95 capital proxy; observed-drawdown reserve; conservative research capital proxy.
Do not use: Paytm Money margin required; NSE margin required; exact broker capital requirement.

## Future finite extension
A separate exchange-margin reconstruction can ingest historical SPAN risk parameter files and date-specific exposure parameters for the exact four-leg portfolio. That is outside this Phase 9 result and must be pre-registered before execution.