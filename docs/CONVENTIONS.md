# Conventions and schemas

## State files — `state/<dept>.md`

```
---
department: supply-chain
date: 2026-09-04
run: scheduled | assignment | manual
runtime: grok-bot | paperclip | claude-code | codex | human
status: ok | degraded | failed
tools_failed: []
---
## Headline
One or two sentences the Chief of Staff can lift into the brief.

## Data
Tables the other departments read. Keep column names stable across days.

## Exceptions
Anything outside normal bounds, with the number and the threshold.

## Requests sent
- 20260904-0620-supply-chain-stockout-risk → advertising

## Proposals written
- approvals/pending/20260904-supply-chain-po-anb-017.md
```

## Typed requests — `requests/<to-dept>/inbox/<YYYYMMDD-HHMM>-<from-dept>-<type>.md`

```
---
type: need-cash-check
from: supply-chain
to: finance
skus: [ANB-017, ANB-021]
needed-by: 2026-09-05T07:00+03:00
priority: normal | urgent
---
## Ask
What is the PO ceiling remaining this month after the two pending proposals, and can a CAD 6,400 PO for ANB-017 ship on Sep 12?

## Context
state/inventory.md 2026-09-04, approvals/pending/20260904-supply-chain-po-anb-017.md

## Answer (appended by the receiving department)
```

Enumerated types:

| type | from → to | meaning |
|---|---|---|
| need-cash-check | supply-chain → finance | confirm cash and PO ceiling for a proposal |
| need-forecast | advertising → supply-chain | demand and cover before scaling spend |
| need-margin-floor | pricing-intel → finance | current contribution margin and floor for a SKU |
| need-launch-plan | supply-chain → advertising, catalog | launch timing before inbound sizing |
| blackout | advertising or catalog → pricing-intel | do not change price on SKU until date |
| stockout-risk | supply-chain → advertising | throttle spend on SKU |
| competitor-oos | pricing-intel → advertising | opportunity: raise bids on SKU |
| quality-issue | customer → supply-chain, catalog | return-reason spike on SKU |
| compliance-hold | account-health → any | stop actions on SKU until resolved |
| info | any → any | no action required |

Answered files move to `requests/<to-dept>/done/`. Unanswered past `needed-by` are listed by the Chief of Staff in the brief.

## Approvals — `approvals/pending/<YYYYMMDD>-<dept>-<action>-<sku>.md`

```
---
id: 20260904-supply-chain-po-anb-017
department: supply-chain
tier: T2
action_type: purchase_order | price_change | listing_change | fba_shipment | campaign_create | coupon | buyer_message | vine_enrolment | reimbursement_claim
status: pending | approved | rejected | expired | executed | failed
created: 2026-09-04T06:30+03:00
expires: 2026-09-06T06:30+03:00
estimated_cost: 6400 CAD
skus: [ANB-017]
payload:
  supplier: <name>
  quantity: 480
  unit_cost: 12.10
  ship_by: 2026-09-12
decided_by: null
decided_at: null
executed_at: null
ledger_ref: null
---
## Proposal
One paragraph a human can decide on in 20 seconds.

## Reasoning and evidence
Cover 11.2 days (state/inventory.md 2026-09-04). 30-day velocity 42/day (DataDoe export orders_daily 2026-09-04). Lead time 21 days (suppliers/<name>.md). Cash check answered: yes (requests/finance/done/20260904-0622-supply-chain-need-cash-check.md).

## Projected impact
Zero stockout days through Ramadan buffer; cash out CAD 6,400 on Sep 12.

## What happens if rejected
Stockout projected Sep 15; recommend throttling ads on ANB-017 from Sep 10.
```

Only the approval channel (Telegram bot, or Rami editing the file) moves a file from `pending/` to `approved/` or `rejected/` and sets `decided_by` and `decided_at`. Only the hands runner moves `approved/` to `executed/` and sets `ledger_ref`.

## Ledger — `ledger/actions.jsonl`

One JSON object per line, append only:

```
{"ts":"2026-09-04T06:41:12+03:00","department":"advertising","tier":"T1","action_type":"bid_change","runtime":"codex","target":{"campaign_id":"…","keyword_id":"…"},"input":{"old_bid":1.20,"new_bid":1.35},"output":{"status":"ok","api":"amazon-ads-mcp"},"approval_id":null,"reason":"CVR 18% vs campaign 12%, ACOS 22% under target 28%"}
```

## KPIs — `ledger/kpis.csv`

`date,marketplace,sku,units,revenue,ad_spend,acos,tacos,contribution_margin,cover_days` — one row per SKU per marketplace per day, appended by Finance.

## Memory

- `departments/<dept>/memory/MEMORY.md` — durable facts and patterns, each with a `since:` date and a `source:` link. Under 300 lines; prune monthly.
- `departments/<dept>/memory/YYYY-MM-DD.md` — that day's observations. Never edited after the day.

## Dates, units, names

ISO dates. Currency stated on every number (CAD or USD). SKUs by internal code `ANB-nnn` with the ASIN in `products/`. Marketplaces: `ca`, `us`, `walmart-ca`.
