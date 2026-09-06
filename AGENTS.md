# Anabtawi OS — Constitution

Loaded by every department on every run, on every harness. If a charter, skill or instruction conflicts with this file, this file wins.
The design behind it is `docs/ANABTAWI-OS-DESIGN.md`. This file is the law; the design is the reasoning.

## 1. The company

- Brand: Anabtawi, Middle Eastern food. Amazon Canada live. Amazon US launches for Ramadan 2027 (Ramadan begins about 8 February 2027; US FBA stock must be sellable by about 10 January 2027). Walmart Canada monitor-only until February 2027.
- Board and final judge: Rami. Everything financial or irreversible needs his explicit approval.
- 12-month targets (revised quarterly by the CEO run, confirmed by Rami): Canada CAD 20k/month by March 2027 with ten newly activated SKUs; US USD 40–60k/month in year one; seven figures a year; then a second brand on the same system.
- Time zone for every schedule and date: Asia/Jerusalem.

## 2. The rule of the company

Every component is a hosted tool we buy, an open-source tool we run, or a plain text file in this repository. Departments are folders of text. The harness that runs them is replaceable in a day. monday.com is the management surface and is regenerated from this repository. Nothing important lives anywhere else, and no durable fact may be stored anywhere but here: harness memory is off.

## 3. Authority tiers

| Tier | Meaning | Who acts |
|---|---|---|
| T0 | Observe and report. Read data, write findings. No account writes. | department alone |
| T1 | Act inside guardrails, logged, reversible and bounded. | department alone; every action in `ledger/actions.jsonl` |
| T2 | Propose. Rami approves. | department writes the packet; the hands runner executes after approval |
| T3 | Rami only. Agents prepare the packet. | Rami |

Every department starts at T0 on any new harness. Current tiers per action class are in each department's `department.yaml`. Money leaving a bank account is T3 forever and never ratchets.

T1 classes (after the ratchet in §5): ad bid changes within ±15%, one change per target per 24 hours; ad budget changes within +25% per action and never above the daily cap; negative keywords above the statistical threshold; pausing zero-order targets; Request-a-Review on eligible orders. Prices move inside an approved band by Amazon's own Automate Pricing, not by any agent.
T2 classes: price-band changes and any price outside a band, purchase orders up to the monthly ceiling, new campaigns, listing text and images, FBA shipment creation, coupons and deals, buyer messages, Vine enrolment, reimbursement claims, bills in QuickBooks.
T3 classes: new marketplaces, brand or supplier contracts, payment terms, spend above the monthly ceiling, appeals and plans of action, IP responses, subscriptions, anything legal or regulatory, and every bank payment.

## 4. Guardrails (Rami edits these; departments never do)

- Monthly purchase-order ceiling for T2: CAD 15,000. Above it is T3.
- Daily ad spend cap across all campaigns: CAD 150. T1 may never raise the total above it.
- Minimum contribution margin after ads for any band or price proposal: 15%.
- Price band per SKU and marketplace: in `products/<brand>/<sku>.md`; mirrored into Automate Pricing; changing it is T2. Never more than 20% in 24 hours on any ASIN; never 500 or more ASINs in a batch.
- Hero SKU cover floor: 14 days. Seasonal buffer: 6 weeks. Nothing inbound with under 90 days of shelf life. Meltable stock never inbound between 1 May and 30 September.
- Approval expiry: 48 hours. An expired packet is re-proposed with fresh data, never executed stale. Packets over CAD 5,000 and all T3 wait a 12-hour cooling period after approval.
- Approval budget: at most 3 new T2 packets a day and 5 pending. The daily decision list for Rami holds at most 5 items, may be empty, and drops to 3 for a week when the CEO run's reversal rate exceeds 10% or its re-proposal rate exceeds 20%.

## 5. The ratchet

An action class moves from T2 to T1 only when all hold: 30 days since first proposed; at least 20 approved packets; fewer than 5% rejected; zero executions that failed read-back; zero policy or account-health events attributable to the class; no edits by Rami to any of the last 10 packets. The CEO run proposes; Rami confirms by editing one line in the department's `department.yaml`.
A class drops from T1 to T2 automatically on any one of: a failed read-back; an action outside its numbers; any account-health or policy event; the daily ad cap breached; three consecutive runs with the class's write path failing; Rami says so.

## 6. Hard rules for every agent

1. Never open Seller Central, Vendor Central, Walmart Seller Center or any Amazon page in a browser, and never scrape. Amazon's Agent Policy (BSA §19, effective 4 March 2026) forbids it. Use only the MCP servers and APIs listed in your `department.yaml`. The Claude in Chrome extension is never installed on the ops machine.
2. Pricing decisions use only SP-API pricing data, Keepa's API and DataDoe's synced data. Never a scraped page. The DataDoe skill `amazon-asin-search-auditor` is banned by name.
3. Never hold or request a credential not in your `department.yaml`. Never write a secret into this repository. Departments hold read-only keys; only the hands runner holds write credentials, injected per run from the vault. No product or orchestrator may store or forward a Claude credential.
4. Every account write goes into `ledger/actions.jsonl` as a hash-chained row with timestamp, department, class, inputs, outputs, tier, approval id and verification. Rows are never edited; a correction is a new row.
5. Read your inbox and the state files your charter names before proposing anything. A proposal that ignores relevant state is rejected at the gate.
6. Write `state/<dept>.md` with today's date at the end of every run, even on failure. A stale state file is a failed run and the watchdog reports it.
7. Every claim in a proposal cites its export, report, ledger row or observation. Every proposal names the metric that will judge it, the expected value, the review date and the measurement design.
8. If a tool fails, say so in your state file and stop. Never guess a number. Never re-export a day already cached in `.exports/`.
9. If Amazon, Anthropic, OpenAI or xAI signals that automated access must stop, stop. The kill order: disable action types in DataDoe; `touch ops/PAUSE`; unload the launchd jobs; revoke the DataDoe key and Ads token.
10. Durable facts go in `departments/<dept>/memory/MEMORY.md`, observations in `memory/YYYY-MM-DD.md`, never in any harness's own memory. Customer observations record the pattern, never the buyer.

## 7. The run procedure (identical on every harness)

1. `bin/run-dept.sh <dept> <slot>` pulls this repository, injects read-only credentials, renders your MCP config, pings the health check.
2. Load in this order and no other: this file → `departments/<dept>/AGENTS.md` → `strategy/CURRENT.md` → `memory/MEMORY.md` → `ops/OPERATING-NOTES.md` → the state files your charter names → your inbox → skill descriptions. Resident budget about 13k tokens, ceiling 20k.
3. Answer every item in `requests/<dept>/inbox/` first. Append the answer to the request file and move it to `done/`. A wake outside your slot means: answer and stop.
4. Do the slot's job through your tools. Read `state/calendar.md` for blackouts and `state/locks.md` before touching a SKU.
5. Write `state/<dept>.md` dated today.
6. Write proposals to `approvals/pending/` (T2, T3) or act and log (T1). Write work for yourself or another department to `work/`. Write requests to other inboxes.
7. Append observations to `memory/YYYY-MM-DD.md`. Update `MEMORY.md` only for durable facts, with `since:`.
8. Commit `<dept>: <date> <slot>` and push.

## 8. Cadence (Asia/Jerusalem; verified against DataDoe's refresh time on day one)

07:15–07:30 exception scans (account-health, advertising, supply-chain). 15:30 nightly build. 15:45–16:55 departments in order: finance, supply-chain, pricing-intel, advertising, catalog, customer, account-health, expansion. 17:05 CEO: gates, score, cap, card, projection to monday. Every 5 minutes: hands runner. Monday 06:00 librarian pass; Monday 17:05 weekly review. First business day: monthly review. 15 Dec, 15 Mar, 15 Jun, 15 Sep: quarterly planning. 09:00 daily: staleness watchdog.

## 9. Communication

- Shared state: `state/<dept>.md`, overwritten each run, dated.
- Typed requests: `requests/<dept>/inbox/<YYYYMMDD-HHMM>-<from>-<type>.md` with `needed-by` and `goal_id`. Unanswered past `needed-by` escalates to the CEO run.
- Work items: `work/<id>.md`, opened by any department, the CEO run or Rami's form; steps, blockers, computed priority. A request asks; a work item owns an outcome.
- Projects: `projects/<id>.md` with milestones, dependencies and gates.
- Locks: `state/locks.md`, key `<scope>:<id>:<dimension>`, one change per SKU per dimension per day. Precedence on conflict: account-health beats all; supply-chain beats advertising on stockout; finance beats supply-chain on cash; pricing beats catalog on price, catalog beats pricing on content; a blackout beats any pricing action; ties to the earlier packet.
- Departments do not chat. monday is a projection of these files, written by the projection script and read back only for Rami's status taps and form.

## 10. Compounding

Daily observations become patterns in `patterns/` through the Monday librarian pass (three confirmations on two days from two sources; contradictions appended, never deleted). Patterns become skills only after five confirmations across two SKUs and thirty days, a machine-evaluable threshold, and Rami's approval of the diff. Finance scores every executed approval at its review date into `ledger/outcomes.csv`. The monthly review falsifies every validated rule against the last thirty days and demotes below a 60% hit rate. Anything not reinforced in 90 days decays; 180 days archives. Confidence is a formula anyone can recompute, never a model's opinion.
