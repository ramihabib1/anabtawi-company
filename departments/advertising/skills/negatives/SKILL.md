---
name: negatives
description: When a search term may be negated. Use before proposing or applying any negative keyword.
---
# Negative keyword threshold

Compute the account's trailing 90-day conversion rate, cvr90, from the Ads MCP search-term report.
A term may be negated only if: clicks ≥ ceil(3 ÷ cvr90) and orders = 0, or spend ≥ 2 × the SKU's target CPA with ACOS > 2 × target for 14 days.
Negate as negative exact in the campaign where it spent, and as negative phrase upstream only when the term is clearly irrelevant (different product category), never for a low-converting relevant term.
Log each negative in `ledger/actions.jsonl` with clicks, spend, cvr90, and the rule that fired.
