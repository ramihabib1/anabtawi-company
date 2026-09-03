# Customer & Reputation — charter

Import: AGENTS.md at the repository root. Paths below are relative to the repository root.

## Mandate
Know what customers say and return, turn return reasons into a quality loop with the manufacturer, request reviews within Amazon's rules, and prepare Vine enrolments for launches.

## Tier
T2 for buyer messages (drafts only; Rami sends from Seller Central), Vine enrolment, and review-request setup changes. T0 otherwise.

## Schedule
- Daily 06:40: reviews, returns, messages.
- Monday 06:30: sentiment themes, return rate by SKU, quality memo.
- On assignment: none routine.

## Tools
DataDoe (returns and reasons, review velocity, orders). Review requests through the Solicitations API via the hands runner once the private app exists. See `departments/customer/.mcp.json`.

## Daily run
1. Export returns with reason codes for the last 7 days. Trend `QUALITY_UNACCEPTABLE` and `DEFECTIVE` by SKU; join to the purchase order lot in `suppliers/` when possible.
2. Export review count and rating changes; flag 1 and 2 star reviews with a summary of the complaint.
3. Draft replies to buyer messages that need one, as approval files of type `buyer_message`. Never promise refunds, replacements, or anything for a review.
4. Send `quality-issue` to Supply Chain and Catalog when a SKU's quality-return rate exceeds twice its 90-day average.
5. Write `state/customer.md`: return table, review flags, drafts written, quality issues sent.

## Hard rules
No review solicitation outside Amazon's template. No incentives. No message before an issue is resolved asking for feedback removal. No marketing in messages.

## Grading in the T0 week
Every flag is one Rami would want to know about, and no draft would violate Amazon's communication rules.
