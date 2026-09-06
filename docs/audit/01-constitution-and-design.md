# Audit 01 — the constitution (`AGENTS.md`), the design (`docs/ANABTAWI-OS-DESIGN.md`), `README.md`

Cross-checked against `docs/monday-schema.yaml`, `docs/record-schemas.yaml`, `docs/schemas/*.json`,
`departments/*/department.yaml`, `docs/research/01..10`. Line numbers as of 2026-09-06.

## BLOCKERS

**B1 · Telegram is still the notification channel.** Design lines 85, 145, 265, 484, 595, 693, 721, 775, 790, 818; plus
`approval-packet.schema.json:72` (`decision_channel` enum). The constitution names **no** channel at all (§9), so the two
files also disagree. Fix: delete every Telegram line; add to constitution §9 — *"Rami is notified only by monday: a push
per Decisions item, and a push from Run Health when a department is Failed or Stale. There is no other channel."*
Set `decision_channel` to `["monday","file-edit",null]`; §7.6's P0 lane becomes a monday push. Say what is lost: if
monday is not opened, nothing reaches him.

**B2 · The ratchet is confirmed in two different files.** Constitution §5 line 44: Rami edits `department.yaml`. Design
§9.2 line 684: Rami edits the department's `AGENTS.md`. The shipped `department.yaml` files say "Rami edits this line".
Fix: `department.yaml` wins; correct §9.2, §6.1's "Tier now" column, and delete "tier per action class" from the charter
description at line 452 so the tier has one home.

**B3 · Nobody knows who writes monday.** Constitution §9 line 82: written "by the projection script" only. Design §4.3 and
`monday-schema.yaml` name six writers (`ceo`, `hands`, `finance`, `build`, `run_wrapper`, `monday`, `rami`); §4.1.4 budgets
"nine departments plus the nightly build"; §6.2 gives all nine `monday_calls_per_run: 40` — yet only `ceo` and `finance`
have the monday MCP. Fix: *"`bin/project-monday.py` is the only process that writes monday; the nightly build, the CEO run
and the hands runner invoke it. No department calls the monday API."*

**B4 · The monthly cost is stated twice, 70% apart.** §0 line 17: "about CAD 285 … falling to about CAD 150". §11.2 line
791: "~CAD 485" then "~CAD 350". §11.2 adds up (97+53+41+99+50+10 USD). Fix §0.

**B5 · The packet schema does not match the design.** Appendix B, §4.3, §7.3 and `monday-schema.yaml:42` use
**`if_ignored`**; `approval-packet.schema.json` *requires* **`if_rejected`**. Appendix B also calls `metric, baseline,
expected, review_on, design` required — the schema defines none of them, so nothing enforces the outcome scoring of §8.2.
Fix: rename in the schema and add the five fields to `required`.

**B6 · The meltable guardrail is six weeks looser than the researched policy.** Constitution §4 line 38 and design line
421: "never inbound between 1 May and 30 September". `research/03:99` (REPORTED): no meltable inbound **15 April – 15
October**, disposal from 1 May. Fix: "inbound only 16 October – 14 April", tagged REPORTED until Rami confirms.

**B7 · The shelf-life guardrail is below Amazon's floor.** Constitution §4: "nothing inbound with under 90 days".
`research/03:97` (REPORTED): **105 days remaining at receipt**, auto-disposal at ~50 days before expiry. Fix: "nothing
inbound that will have under 105 days of shelf life at receipt; plan against shelf life − 105 − 50 − transit."

**B8 · The Cockpit contradicts itself three lines apart.** §4.5 line 252 lists "Chart: scorecard status counts"; line 255
says charts are browser-only "so the Cockpit uses Number, Battery and List widgets". Fix: "Number: scorecard reds".

**B9 · The design's example `department.yaml` contradicts the shipped ones and the tier rule.** §6.2 shows advertising's
daily slot at **15:50** (§6.5 and the real file: **16:15**) and ships `tier: {bid_change: T1, …}` while lines 26 and 661
say every department starts at **T0**. Fix: make the example a verbatim copy, `tier: {}` included. Also advertising's Mon
16:30 and supply-chain's Tue 16:30 weekly slots overlap catalog's 16:25 daily slot (20-min timeout), breaking §6.4's
"departments run one at a time"; move both to 17:30.

**B10 · Two rules ask for opposite rejection rates.** §7.1 line 552 (objective O3): "rejection rate 2–30%". §5/§9.2: a
class promotes at "fewer than 5% rejected", which with the ≥20-packet minimum means **zero rejections**. Fix: O3's KR is
the *override* rate (§7.5 already alarms outside 2–30%); rename it, and write the ratchet condition as "zero rejected
packets in the last twenty".

**B11 · Dead names from the earlier repository survive in the normative schemas.** `approval-packet.schema.json`
`department` enum contains `"chief-of-staff"`, which is not one of the nine; `ledger-entry.schema.json` `runtime` enum
contains `"paperclip"` (the orchestrator §2 rejected) and an `action_type` field marked "legacy alias". Delete all three.

**B12 · The repo advertises the earlier design in order to deny it.** `README.md:3`, design lines 3 and 5 ("blank page",
"nothing … descends from an earlier design"); Appendix A line 854 still names the root `<brand>-company/`. Fix: delete the
three sentences, rename the root `<brand>-os/`.

**B13 · The coupon guardrail breaches the margin floor.** Constitution §4: minimum margin after ads 15%. Design §9.1 line
674: coupons need "margin after discount ≥10%". Fix: one floor, or an explicit, time-boxed coupon exemption in §4.

## MAJOR

**M1 · The approval budget is stated three ways.** "3 new **T2 packets**" (constitution §4) / "three new **money
packets**" (§0.3, §7.4) / "three new **packets**" (§9.5); and "five pending *per day*" mixes a stock with a flow. Fix: "at
most 3 new T2 packets created per day, at most 5 pending at any moment."

**M2 · Guardrail numbers live in two files while §7.1 claims they live in one.** §7.1 says guardrails are "§4, referenced
never copied", but §9.1 holds a dozen numbers absent from §4 (≥30 clicks/14d, 25 targets a run, ≤5 SKUs per packet,
campaign start ≤CAD 20/day, coupon ≤20% and ≤CAD 500 exposure, Vine ≤2/quarter). Fix: all numbers into §4 with a
"confirmed / research tag" column; §9.1 keeps class names and write paths only.

**M3 · Three cadences.** §0.4: runs "15:30–16:30", card at "17:00". §6.5 and constitution §8: 15:45–16:55, card 17:05.
The 15:30 job is called the "nightly build" and runs in the afternoon. Fix: one table, renamed "the daily build".

**M4 · `decided_at` cannot mean what the runner reads it as.** Line 204 and `monday-schema.yaml:49` type it
`last_updated`, which changes on every projection write. Fix: the poller stamps `decided_at` when it observes the status
change.

**M5 · The column that authorises money has four writers.** §4.3 gives `decision` to Rami and says the writer is "the only
process allowed to write that column"; §4.6 automations set Expired and `snooze_until`; §9.3 step 14 sets Executed. Fix:
state the true rule (Rami: Approved/Rejected/Deferred; automation: Expired; runner: Executing/Executed/Failed).

**M6 · The constitution demands a ledger field the schema makes optional.** §6.4 requires "approval id and
**verification**"; `ledger-entry.schema.json` omits `verification` from `required`. Fix: require it, `null` only for
`dry-run`/`failed`.

**M7 · Two versions of the run procedure.** Constitution §7 (8 steps) vs design §6.3 (7). Only the design has `flock`, the
per-department clone and the `.exports` rule; only the constitution has `locks.md` and `calendar.md`. Fix: one list, in
the constitution; §6.3 becomes a pointer.

**M8 · "Own carve-out" is undefined.** Constitution §3 puts Request-a-Review in T1 "after the ratchet"; §9.1 line 676
calls it "T1 candidate (own carve-out)". Fix: it ratchets like everything else, or §5 names the exception.

**M9 · "T2 after 30 clean days" (QuickBooks bills, §9.1 and §6.1) never defines "clean".** Reuse the ratchet conditions or
delete the phrase.

**M10 · "A CEO layer, itself just a scoring function plus four files" (line 13).** §7.1 lists ten paths under `strategy/`.
Name the four or drop the claim.

**M11 · Keepa's MCP does not exist.** §0 lists it among the MCP servers; §3.2/§11.1 reveal it is a "forked 150-line MCP
wrapper" of an unnamed repo, unbuilt and unowned. `research/03:220` reports Keepa ships a hosted MCP on the same key. Fix:
use the hosted server, or make the fork a week-one build item with an owner.

**M12 · Brand two costs nothing in §0 and USD 200–400/month in §12** (line 808) — roughly the whole current stack. Put the
number in §0.

**M13 · The US critical path has no slack at the researched upper bound.** §4.3/§13 fix sailing at 25 Nov for stock
sellable 10 Jan; `research/03:131` reports door-to-sellable at **6–10 weeks**, i.e. 3 February at the slow end. Fix: state
the 6-week assumption and list the 10-week case as a risk.

**M14 · `reads_state: []` in all nine `department.yaml`** while constitution §7.4 and §6.3.2 both require "the state files
your charter names". Fill the lists or delete the rule.

**M15 · §4.3 says the SKU Profiles board has 34 columns; §5.3 lists 36.**

**M16 · §4.2 says "Four folders" above a table of five**, and the table omits Scorecard History, which §4.3 defines.
Renumber "1b Work".

**M17 · "Version 1.1" with no v1.0 and no change log.**

**M18 · No path for tonight's machine.** Everything assumes the Mac mini, `launchd`, `op run` and the hands runner (§3,
§6.3, §13). The MacBook appears nowhere, so the document cannot be executed on the day it is approved. Fix: a "Night 0"
row in §13 — see below.

**M19 · The constitution states as law what the design calls a hypothesis.** §4's "never more than 20% in 24 hours; never
500 or more ASINs" is flat law; §1.2 and §14.1 call both REPORTED and "a hypothesis until Rami pastes the text". Fix: tag
them in §4 too, and mark the PO ceiling and ad cap as Rami's defaults, not Amazon's.

**M20 · The ratchet may be arithmetically unreachable:** ≥20 approved packets of one class in 30 days, under a
company-wide budget of 3 new packets a day across nine departments and a weekly change budget of ≤20% of targets. Fix: add
a per-class weekly quota, or lower to 10 packets over 60 days, and show the arithmetic once.

## MINOR

m1 · Rami is "the board" while a department is named `ceo`, so "the CEO run proposes; Rami confirms" reads backwards;
prefer `command`. m2 · Constitution §8 is a paragraph of eighteen times where design §6.5 is a table — keep the table,
delete the paragraph. m3 · `resident_tokens: 20000` in every `department.yaml` is the ceiling, not the 13k budget.
m4 · §6.2 already bans `amazon-asin-search-auditor`; §14.2 still lists banning it as week-one work. m5 · Keepa is €49 in
§0/§11.1 and USD 53 in §11.2; "about 5% falling to 3.5%" holds only at CAD 10k, not the CAD 8k in the same sentence.
m6 · The packet `action_class` enum lacks `strategy`, `request_a_review` and `bills`, which §9.1 and the Decisions board
both use. m7 · The ledger `tier` enum includes `T0`, which performs no account write.

## Readability: the ten passages most responsible for "nothing is clear"

| # | Where | Proposed sentence |
|---|---|---|
| 1 | Design line 13 — the 190-word §0 opening | Nine departments, each a folder of text in this repository, read the business through MCP servers and write one thing a human sees: a monday board with at most five decisions a day for Rami to approve or reject. |
| 2 | Constitution §2 line 15 — five claims in one paragraph | Everything the company knows lives in this repository as text; monday.com only displays it, and any harness that can read files and call MCP tools can run the company. |
| 3 | Constitution §8 — eighteen times in prose | Every run's time is in the cadence table in `SPEC.md`; nothing is scheduled anywhere else. |
| 4 | Constitution §4 line 40 — two different caps in one bullet | Rami sees at most five decisions a day; departments may create at most three new T2 packets a day and hold at most five pending. |
| 5 | Constitution §5 line 44 — six ratchet conditions in one sentence | A class moves from T2 to T1 only after thirty days, twenty approved packets, zero rejections, zero failed read-backs, zero policy events and zero edits by Rami — all six, or it stays. |
| 6 | Constitution §9 line 81 — six precedence rules, semicolons | When two departments want the same SKU on the same day, this order decides: account-health, then a blackout, then finance, then supply-chain, then pricing, then catalog. |
| 7 | Constitution §10 — nine rules, one paragraph | An observation becomes a pattern after three sightings, a pattern becomes a skill after five sightings across two SKUs and thirty days with Rami's approval, and anything unconfirmed for ninety days is marked decaying. |
| 8 | Design §7.4 line 581 — the cap paragraph, eight clauses | The daily list is capped at five items, drops to three for a week if too many decisions are reversed or re-proposed, and may be empty. |
| 9 | Design §6.6 line 533 — "Cost fits inside Max 20x with margin (540–810 runs…)" | At roughly 600 runs a month of five to fifteen minutes each, the departments use well under half of what a Max 20x plan reportedly allows. |
| 10 | Design §9.3 — fourteen numbered paragraphs | A packet is proposed with a dry run, machine-validated, ranked onto Rami's list, approved by him, re-validated against live data, executed once with an idempotency key, read back, and written to the ledger. |

Unactionable as written and belonging in an archive, not in the document Rami reads: **§2** (finalists and weights — the
decision is made), **§12** (multi-brand, month 3+), **Appendix C** (research index), **§4.4–4.7** (views, widgets and
automations, which are build detail for `monday-schema.yaml`).

## Tonight-minimum

Tonight there is a MacBook, Claude Code on Max, the DataDoe MCP, an unbuilt monday workspace and QuickBooks — no Mac mini,
no `launchd`, no vault, no hands runner, therefore **no write path at all**. That removes most of the constitution from
tonight's critical path.

**Must exist — one page of `AGENTS.md`:**
1. **The company.** Brand, marketplaces, the two dates (Ramadan ~8 Feb 2027; US stock sellable ~10 Jan 2027), Rami the
   only approver, Asia/Jerusalem. Four lines.
2. **One tier line.** "Every department is T0 tonight: read data, write files, propose. No agent holds a write credential
   and nothing executes until the hands runner exists." This replaces §3, §5 and half of §9.
3. **Six hard rules.** No browser or scraping on any Amazon surface; pricing data only from SP-API, Keepa and DataDoe;
   no secret in the repo; write `state/<dept>.md` dated today every run, even on failure; cite the export behind every
   claim; if a tool fails, say so and stop.
4. **The run procedure, five steps.** Read this file and your charter → read your inbox → do the job with read-only tools
   → write your state file → commit and push.
5. **The guardrail table,** every number tagged `UNCONFIRMED` until Rami confirms, with B6 and B7 already corrected.
   It binds nothing tonight, but it must be a table, not prose.
6. **Where Rami looks tonight:** `briefs/<date>-decisions.md` in the repo. Not monday — the workspace does not exist.

**Can wait:** the ratchet (§5) until a T1 class is proposed; locks, precedence, work items, projects and typed requests
(§9) until two departments run on the same day; compounding (§10) until there are seven days of observations; every monday
board, automation and form; both JSON Schemas until something can execute; the runner, vault, `launchd` and watchdog.

**Delete tonight, not later:** every Telegram line, `"chief-of-staff"`, `"paperclip"`, `"legacy alias"`, and the three
sentences about an earlier design (B1, B11, B12). They cost nothing to remove and they are the first things Rami sees.

## Proposed `SPEC.md` — three pages

`ANABTAWI-OS-DESIGN.md` becomes `docs/archive/DESIGN-2026-09.md`. `SPEC.md` is what Rami reads and what every run loads
beside `AGENTS.md`.

**Page 1 — What this is (≈450 words).** The company in five sentences (nine departments, one repository, monday as the
surface, five decisions a day, no agent moves money) · the guardrail table, each number marked confirmed or unconfirmed ·
the four tiers in four lines, ending "money leaving a bank is T3 forever".

**Page 2 — How a day runs (≈550 words).** The cadence table, the only place a time is written (replaces constitution §8,
design §0.4 and §6.5) · the run procedure in five lines (replaces constitution §7 and design §6.3) · the approval path in
eight lines (replaces §9.3's fourteen paragraphs) · Rami's three gestures: tap a status, submit the form, edit a file ·
the kill order in four lines.

**Page 3 — What is built when, and what we do not know (≈450 words).** Build order, one row each with its exit test:
Night 0 (MacBook, one department, manual, T0), Week 1 (Mac mini, watchdog, monday workspace), Week 2 (SKU profiles,
integrity check, shadow decision list), Week 3 (decisions at cap 3), Week 4 (cap 5) · open questions reduced to those that
change a decision, each with an owner and a date · pointers to where detail lives.

Rule for the rewrite: every sentence states a fact, a number or an instruction; nothing explains why an alternative lost.
