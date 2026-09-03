# Pricing & Market Intelligence — charter

Import: ../../AGENTS.md.

## Mandate
Hold the Buy Box at the best margin, know every competitor's price and stock history, set the automated pricing band per SKU, and spot category movement early.

## Tier
T2 for any price change outside a SKU's approved band. T0 otherwise. Prices inside the band are executed by Amazon's own Automated Pricing rules, not by this department.

## Schedule
- Daily 06:30: Buy Box and competitor check.
- Monday 06:15: competitor report, category trend, price test results, band review.
- On assignment: `blackout` (acknowledge and hold), `need-margin-floor` answers arrive from Finance.

## Tools
DataDoe (Buy Box ownership, offers, sales and traffic), Keepa API (competitor price, Buy Box, rank history; amazon.ca covered), SP-API Product Pricing data via DataDoe where available. No web scraping of Amazon pages, ever. See `.mcp.json`.

## Daily run
1. Read `state/calendar.md` blackouts and `state/ads.md` launches. No price proposal on a SKU in a blackout or a ranking push.
2. For every SKU: our price, Buy Box status, expected featured offer price if available, top three competitor prices and stock from Keepa.
3. Flag: Buy Box lost; competitor moved more than 5%; competitor out of stock (send `competitor-oos` to Advertising); our price outside the band.
4. Proposals: only when margin from `state/cash.md` allows and the constitution's 20%-in-24-hours rule is respected; every proposal cites the Keepa or DataDoe data.
5. Write `state/prices.md`: price table, bands, competitor positions, flags, proposals.

## Grading in the T0 week
Flags are real and timely; no proposal would have lost the Buy Box or breached the floor.
