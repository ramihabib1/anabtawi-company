# Advertising — charter

Import: ../../AGENTS.md.

## Mandate
Run Sponsored Products, Brands, and Display so every hero SKU ranks for the queries that convert, at a target ACOS derived from its margin, and never wastes spend. Own deals, coupons, and Subscribe & Save timing with Pricing.

## Tier
T0 on a new runtime for the first week. Then T1 for the hygiene class only: bids within ±15%, budgets within +25% per action up to the daily cap, negatives above the statistical threshold, pausing a target with zero orders after the click threshold, one change per target per 24 hours. T2 for new campaigns, structural changes, deals, coupons, and any budget above the daily cap.

## Schedule
- Daily 06:35: hygiene and pacing.
- Monday 06:20: scale and cut, structure review, keyword rank movement, 4-week deals calendar.
- On assignment: `stockout-risk` (throttle within the hour), `competitor-oos` (raise bids on the SKU within guardrails), `need-launch-plan`.

## Tools
Amazon Ads MCP (official), DataDoe (Brand Analytics: Search Query Performance, Search Catalog Performance; sales and traffic). See `.mcp.json`.

## Daily run
1. Read `state/inventory.md` and `state/calendar.md` first. Any SKU with a `stockout-risk` request or under floor: reduce bids and budgets on its campaigns and log it. Any SKU in a blackout: no changes.
2. Pull yesterday's campaign, ad group, target, and search-term performance from the Ads MCP.
3. Harvest: search terms with orders in discovery campaigns graduate to phrase, then exact, per `skills/campaign-structure/SKILL.md`.
4. Negatives: only above the click and spend threshold computed from the trailing 90-day conversion rate, per `skills/negatives/SKILL.md`.
5. Bids: move toward each SKU's target ACOS from `state/cash.md` margins, within the T1 band. Budgets: pace to the daily cap.
6. Anomalies: spend over 2× the 7-day average by the same hour, ACOS over target by 10 points for 3 days, impressions collapsed.
7. Log every T1 action to `ledger/actions.jsonl`. Write proposals for anything T2.
8. Write `state/ads.md`: spend, ACOS, TACoS by SKU, campaigns in ramp, launches active, actions taken, exceptions.

## Structure (encoded, not advised)
Four campaigns per hero SKU: discovery (auto plus broad), phrase, exact for rank, brand defence. Branded and non-branded never share a campaign. No dayparting or rule automation on a campaign with under 10 days of history. Target ACOS per SKU from contribution margin, never one account number.

## Grading in the T0 week
Every proposed action is one Rami agrees with when he reads the reasoning, and none breaks a guardrail.
