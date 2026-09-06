# 06 — The CEO layer: strategy, goals, and decision generation

Research date: 2026-09-06. Author: research agent. Audience: Rami (board of one) and whoever implements the CEO department.

**Sourcing note, read this first.** This session's egress proxy blocked direct fetches to `rework.withgoogle.com`, `aboutamazon.com`, `s2.q4cdn.com`, `sre.google`, `eosworldwide.com`, `commoncog.com`, `chernev.com`, `anthropic.com`, `arxiv.org`, `learn.microsoft.com`, `monday.com` and `docs.crewai.com` (403 from the policy proxy, 2026-09-06). Claims from those bodies of work are therefore tagged **REPORTED** from search-result summaries with the canonical URL given, not VERIFIED. What I could open today — GitHub raw files, the monday.com first-party API and knowledge service, and this repo — is tagged **VERIFIED**. The web-search budget for the session was exhausted after 200 queries, so a few intended checks are tagged **UNKNOWN** with what I tried.

---

## 0. What the CEO layer is, in one paragraph

Nine departments already produce state files, requests and approval proposals (VERIFIED — `AGENTS.md` §7, `docs/CONVENTIONS.md`, read 2026-09-06). The Chief of Staff already compiles a brief and keeps the operational queue (VERIFIED — `departments/chief-of-staff/AGENTS.md`). What is missing is the thing above them: an object that says what the company is trying to do, a number that says whether it is happening, a rule that turns "not happening" into a small number of decisions, and a lock that stops the plan being rewritten every time a number wobbles. That is the CEO layer. It owns four artifacts (strategy, scorecard, decision list, task list) and one property: **Rami is the only writer of intent, and he writes it only at review boundaries; everything else the CEO layer derives.**

---

## 1. Strategy object model

### 1.1 The five objects

| Object | Cardinality | Changes | Lives in (source of truth) | Surfaced on |
|---|---|---|---|---|
| Mission | 1 | ~never | `strategy/STRATEGY.md` §1 | Strategy board header |
| 12-month targets | 3–4 | quarterly, T3 | `strategy/STRATEGY.md` §2 + `strategy/TARGETS.yaml` | Strategy board, top group |
| Quarterly objective | ≤3 | quarter boundary only | `strategy/GOALS.md` front matter | Strategy board = groups |
| Key result | 2–4 per objective, ≤8 total | never mid-quarter (value updates daily; *definition* frozen) | `strategy/GOALS.md` + `strategy/metrics/<metric_id>.md` | KR board = items |
| Initiative (a bet) | ≤5 live | any time, but must be killed or renewed at monthly review | `strategy/initiatives/<id>.md` | Initiatives board / KR subitems |
| Constraint / guardrail | fixed set | T3 only | `AGENTS.md` §4 — **referenced, never duplicated** | Strategy board read-only mirror |

Cardinality is chosen, not copied. Lattice's published guidance is 3–5 objectives per group with 2–4 (elsewhere 3–5) key results each (REPORTED — lattice.com/articles/how-to-write-effective-okrs-plus-examples, lattice.com/articles/okr-template). For a one-person company with nine agent departments, the binding constraint is not ambition but Rami's review time, so the ceiling is 3 objectives / 8 KRs — below every published recommendation on purpose.

### 1.2 Key result schema (the load-bearing object)

```yaml
- id: kr-2026q4-02a                     # immutable
  objective: obj-2026q4-02
  name: "US launch SKUs through the readiness gate"
  metric_id: us_gate_passed_count.v1    # points at strategy/metrics/<id>.md
  definition_ref: strategy/metrics/us_gate_passed_count.v1.md
  data_source: repo:products/*.md + state/catalog.md   # DataDoe | ads-mcp | ledger/kpis.csv | repo | manual
  direction: up                          # up | down | band
  baseline: 0
  baseline_date: 2026-10-01
  target: 15
  current: 3
  as_of: 2026-09-06
  owner_dept: expansion
  contributing_depts: [catalog, account-health, supply-chain]
  definition_of_done: >
    15 SKUs each with: validated US product-type JSON, FDA panel, FSVP file,
    inbound plan costed. Verified against products/<sku>.md gate block.
  review_cadence: weekly
  cost_of_miss_cad: 180000               # see §3.4 — prices strategic decisions
  slack_weeks: 6
  status: yellow
  status_since: 2026-09-02
  thrash_count: 0
  frozen_until: 2026-12-01
```

Three rules make this survive contact with agents:

1. **A metric definition is immutable; changing it mints a new `metric_id`** (`contribution_margin_ca.v1` → `.v2`). History is never rewritten, and "the number improved" can never be an artefact of a redefinition. This is the anti-gaming rule the whole scorecard rests on.
2. **`current` is written only by the owning department**, from its state file; the CEO layer copies and timestamps, never recomputes. Two computations of the same number is how a company acquires two truths.
3. **Guardrails are referenced, not copied.** `AGENTS.md` §4 is canonical (CAD 15,000 monthly PO ceiling, CAD 150/day ad cap, 15% minimum contribution margin, 14-day hero cover floor, 48-hour approval expiry — VERIFIED, read today). A duplicated guardrail is a guardrail that will drift.

### 1.3 Initiatives are bets, and bets carry falsifiers

```yaml
id: init-2026q4-03
hypothesis: "Four-campaign structure on ANB-017 lifts organic rank enough that TACoS falls below 9% within 6 weeks."
serves: kr-2026q4-01b
cost_cap_cad: 900
decision_date: 2026-11-15
falsifier: "TACoS not below 11% by week 5, or organic rank for the two head terms not inside top 20."
status: running | won | lost | killed
```
The falsifier is mandatory and is written *before* the bet runs. Perdoo's model separates outcomes (OKRs/KPIs) from the activities meant to deliver them (initiatives) (REPORTED — perdoo.com/resources/blog/initiatives-in-perdoo). We adopt the separation and add the falsifier, because an agent company will otherwise keep every bet alive forever.

### 1.4 Versioning

Git is the version control; monday is the surface. Concretely:

- Every write to `strategy/**` is a commit `ceo: YYYY-MM-DD <objective-set|kr-repair|scorecard|decisions>` and appends one line to `strategy/CHANGELOG.md`: date, object id, field, old → new, reason, evidence link, authority (Rami / CEO-proposal-approved).
- Every monday item carries two extra columns, `repo_path` (text) and `commit` (text). A board row that cannot name its commit is stale by definition and the CEO layer flags it.
- Direction of sync: **repo → monday** every run. monday → repo only through one door: a `Proposed` status on the Strategy board becomes a `requests/ceo/inbox/` item, which the CEO run turns into a proposal at the next review boundary. This preserves "no lock-in beyond monday as management surface" (`docs/os-research/_CONTEXT.md`, VERIFIED).
- monday's own OKR pattern maps cleanly: groups = objectives, items = key results, subitems = initiatives/tactics, columns People/Status/Timeline/Formula (VERIFIED via monday first-party knowledge API today, citing support.monday.com/hc/en-us/articles/4402057681298-OKR-management-using-monday-com).

One implementation fact worth knowing before designing rollups: monday's GraphQL API **does** expose `FormulaValue.display_value` ("a string representing all the formula values, separated by commas") and `MirrorValue.mirrored_items` (VERIFIED — schema introspection via the monday MCP, 2026-09-06). So formula columns are readable by agents. I still recommend computing every score in the repo and writing a plain `numbers` column: a formula lives in one account's board settings, a Python function lives in git and is diffable, testable and portable to the next runtime.

Plan limits that shape the board design (VERIFIED via monday knowledge API today, citing support.monday.com articles 360021743500 and 26061127699730): Pro allows **20 connected boards per board**, 10,000 connected items per board, 750 per item, 25,000 automation + 25,000 integration actions/month, 20 boards per dashboard. The account is Pro with 2 active seats (VERIFIED — monday `get_user_context`, 2026-09-06). Six boards and a daily sync sit far inside those ceilings.

---

## 2. The weekly scorecard

Amazon's WBR reviews 400–500 metrics weekly and insists on **controllable input metrics**, not just outputs, and expects metrics to be *retired* when they stop moving the output they were chosen for (REPORTED — commoncog.com/the-amazon-weekly-business-review/, workingbackwards.com/blog/how-amazons-weekly-business-review-drives-data-driven-leadership/). EOS's Scorecard is the opposite extreme: a handful of weekly numbers, each owned, each on-track/off-track, and an off-track number is not solved in the scorecard segment — it is dropped to the issues list for IDS (REPORTED — eosworldwide.com/level-10-meeting). We want Amazon's input-metric discipline at EOS's size.

**Twelve core rows plus up to three campaign rows.** Twelve because a phone screen holds twelve table rows without scrolling twice, and because every row must have a named owner and a named source, and nine departments cannot honestly own more.

| # | Metric | L/L | Owner | Source | Green | Yellow | Red |
|---|---|---|---|---|---|---|---|
| 1 | Net revenue CA, 7-day, CAD | lag | finance | `ledger/kpis.csv` | ≥ trajectory to 20k/mo | −10% | −20% or 2 wks down |
| 2 | Contribution margin after ads, blended CA % | lag | finance | kpis.csv | ≥18% | 15–18% | <15% (guardrail floor) |
| 3 | Cash available for POs, CAD | lag | finance | QuickBooks + kpis | ≥ 1.5× monthly PO ceiling | 1.0–1.5× | <1× |
| 4 | TACoS blended % | lag | advertising | Ads MCP + kpis | ≤10% | 10–13% | >13% |
| 5 | SKUs with cover <14 days (count) | **lead** | supply-chain | `state/inventory.md` | 0 | 1–2 | ≥3 or any hero |
| 6 | Min hero cover (days) | **lead** | supply-chain | inventory.md | ≥28 | 14–28 | <14 |
| 7 | Ad spend vs daily cap, 7-day avg CAD | **lead** | advertising | Ads MCP | 70–95% of cap | 95–100% | >100% |
| 8 | Wasted spend, 14-day zero-conversion CAD | **lead** | advertising | Ads MCP | <3% of spend | 3–6% | >6% |
| 9 | Buy Box win %, revenue-weighted | **lead** | pricing-intel | SP-API pricing via DataDoe | ≥95% | 85–95% | <85% |
| 10 | Hero unit-session % (conversion) | **lead** | catalog | DataDoe sales & traffic | ≥12% | 9–12% | <9% |
| 11 | Listing defects: suppressed + stranded + open violations | **lead** | account-health | DataDoe listing issues | 0 | 1–2 | ≥3 or any hero |
| 12 | Account Health Rating / ODR | **lead** | account-health | Rami reads AHR weekly; ODR via DataDoe | AHR ≥250, ODR <0.5% | AHR 200–249 or ODR 0.5–0.8% | AHR <200 or ODR ≥0.8% |
| C1 | US gate: SKUs ready of 15 | **lead** | expansion | `products/*.md` gate block | on burn-down | 1 wk behind | ≥2 wks behind |
| C2 | Slack days to "US FBA stocked by mid-Jan 2027" | **lead** | expansion | critical path in `playbooks/us-launch.md` | >21 | 7–21 | <7 |
| C3 | Walmart CA: monitor-only checks passed | lead | expansion | manual | n/a until Feb 2027 | | |

Row 12's thresholds use Amazon's published bands: AHR ≥200 healthy, 100–199 at risk, <100 suspension risk; ODR threshold 1% with early flags reported near 0.8% (REPORTED — appealsdoctor.com, feedvisor.com/university/seller-rating/, ensobrands.com; Amazon's own Seller Central pages were not reachable today, so treat the 0.8% early-flag figure as practitioner lore, not policy).

**Status is not computed from one week.** A cell turns red only when one of three SPC-style conditions fires (see §4.1). This is the single most important difference between this scorecard and a dashboard.

**Retirement rule (from the WBR):** at each monthly review, any lead metric that has not moved its paired lag metric in 90 days is proposed for retirement and replacement. The scorecard is capped at 12+3; adding a row requires removing one.

**Phone format** — six columns maximum, one screen:

```
SCORECARD  wk 2026-W37          2 red · 3 yellow
metric                now    Δ4wk   target  st
margin after ads CA  16.1%   +0.5    ≥18%   🟡
SKUs cover <14d          3     +2       0   🔴
min hero cover        11d     -6d    ≥28d   🔴
...
Reds are items 1 and 2 on today's decision list.
```

---

## 3. The daily decision list

### 3.1 Pipeline

```
candidates ──► gates ──► scoring ──► ordering ──► cap ──► publish ──► close the loop
```

**Candidates** come from four places: (a) `approvals/pending/*.md` written by departments (T2/T3); (b) CEO-generated decisions from red KRs ("cut this, or fund that"); (c) escalations from requests past `needed-by` (Chief of Staff already detects these — VERIFIED, its charter); (d) expired items eligible for re-proposal.

**Gates run before scoring** and are cheap to check. An item is bounced back to its department, not shown, if any fail:

| Gate | Rule |
|---|---|
| Evidence | every numeric claim cites an export, report, ledger line or state file (`AGENTS.md` §6.7) |
| Freshness | evidence ≤ 48h old for ops decisions, ≤ 7 days for strategy |
| Guardrail | the action is inside `AGENTS.md` §4, or is explicitly labelled a guardrail-breach request |
| Reversibility floor | a one-way door needs confidence ≥ 0.6 **and** a named falsifier or exit condition |
| Duplicate | no open item on the same target and action type (cooldown table, §4.2) |
| Tier | anything a department could have done at T1 is *not* a decision — it is a bug in the tier table |

That last gate matters more than it looks. Bezos's Type 1 / Type 2 split says the failure mode of an organisation is applying the heavyweight Type 1 process to Type 2 decisions, producing "slowness, unthoughtful risk aversion, failure to experiment sufficiently" (REPORTED — 2015 letter to shareholders, s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF; also the "roughly 70% of the information you wish you had" rule). A daily list that fills up with two-way doors is the same disease. The gate makes the disease visible.

### 3.2 What a decision item contains

```yaml
id: dec-20260906-01
title: "Approve PO 480 units ANB-017"        # imperative, ≤50 chars (ADR convention)
type: approve | choose | ratify              # approve = yes/no; choose = pick from ≤3 options
department: supply-chain
tier: T2
action_type: purchase_order
goal_id: kr-2026q4-01a
impact_cad: 4800                             # 30-day expected value or loss avoided, signed
impact_basis: "9 projected stockout days × 42 units/day × CAD 12.7 contribution"
confidence: 0.9                              # evidence class, §3.3
reversibility: one_way                       # two_way | costly | one_way
deadline: 2026-09-07T10:00+03:00
deadline_reason: "21-day lead time vs 11.2-day cover"
expires: 2026-09-08T06:30+03:00              # 48h, AGENTS.md §4
evidence:
  - "cover 11.2d — state/inventory.md 2026-09-06"
  - "velocity 42/day 30d — DataDoe orders_daily export 2026-09-06"
  - "cash ok — requests/finance/done/20260906-0622-...md"
if_ignored: "Stockout from ~Sep 15; recommend throttling ANB-017 ads Sep 10; est. CAD 4,800 lost + rank decay."
actions: [approve, reject, defer(until)]
approval_file: approvals/pending/20260906-supply-chain-po-anb-017.md
score: 84.4
reproposal_of: null
times_reproposed: 0
```

`if_ignored` is mandatory and is the field Rami should read first on a phone. The structure follows two conventions worth borrowing: the 12-factor-agents pattern of contacting humans through a **typed** tool call with `intent`, `question`, `context` and `options` including urgency and response format (VERIFIED — github.com/humanlayer/12-factor-agents `content/factor-07-contact-humans-with-tools.md`), and the decision-record template's title/status/issue/positions/selection/implications skeleton (VERIFIED — github.com/joelparkerhenderson/decision-record README; note its own caution that in practice records are treated as living documents rather than immutable).

### 3.3 Confidence, by evidence class — not by vibe

| C | Class | Test |
|---|---|---|
| 0.3 | single observation, single source, <7 days | one export, no corroboration |
| 0.6 | trend, single source, ≥14 days, or two sources agreeing once | e.g. Ads MCP only |
| 0.9 | two independent sources agree, or ≥3 observations over ≥14 days | inventory state + DataDoe export |
| 1.0 | deterministic | contract date, cash balance, published Amazon deadline |

Confidence multiplies the score, so a 0.3-confidence item must be ~3× the value of a 0.9 item to outrank it. That is the intended bias.

### 3.4 The scoring function

```
score = 100 × C × ( 0.40·v̂ + 0.25·d̂ + 0.15·û + 0.20·r̂ )

v̂ = min(1, log10(1 + |impact_cad|) / log10(5001))     # CAD 5,000 ≈ 1.0; log so one big item can't own the list
d̂ = 1.0 if deadline ≤24h; 0.8 ≤48h; 0.5 ≤7d; 0.2 otherwise
û = share of impact lost per week of delay, clamped 0–1   # cost of delay, not deadline
r̂ = 0.2 two_way | 0.6 costly | 1.0 one_way
C = 0.3 | 0.6 | 0.9 | 1.0                                  # §3.3
```

Design notes:

- The shape is Weighted-Shortest-Job-First reasoning without the job-size denominator: WSJF is cost of delay ÷ job size, with cost of delay built from value + time criticality + risk reduction (REPORTED — framework.scaledagile.com/wsjf). Job size is irrelevant here because the *agents* do the work; the scarce resource is Rami's attention, which is roughly constant per item. So the denominator drops out and `d̂`/`û` carry time criticality. RICE was rejected for the same reason — "reach" and "effort" are not this company's constraints (REPORTED — productplan.com glossary).
- `r̂` **raises** the rank of irreversible items. This looks backwards against "make two-way-door decisions fast", but it is the correct reading: reversible decisions should not be in this queue at all (the tier gate removes them). Among the items that survive, the one-way doors are precisely the ones that deserve the reading minutes, and the ones where *not deciding* is most expensive.
- **Strategic items with no direct CAD get priced, not exempted.** Every objective carries `cost_of_miss_cad` and `slack_weeks` (Rami sets both once, at quarterly planning). A decision on that objective's critical path takes `impact_cad = cost_of_miss_cad / slack_weeks × weeks_at_risk`. This is what makes "sign the FSVP supplier agreement" competitive with "approve a PO" on the same list, without hand-waving.
- **Staleness decay**: `score × 0.9^days_open`. An item that keeps losing should expire and be re-proposed with fresh data, per `AGENTS.md` §4.

Worked, using today's repo example: PO ANB-017. impact 4,800 → v̂ 0.995; deadline 24h → d̂ 1.0; a week's delay costs ~60% of the value → û 0.6; one-way → r̂ 1.0; C 0.9. **score 84.4.** Versus "pause a keyword saving CAD 14/day" (impact 420, no deadline, two-way, C 0.9): **score 36.8** — and it should never have reached the list at all, because it is T1 hygiene.

### 3.5 The cap: five, hard, with a fifth that is usually empty

Rami asked "why five?". Here is the actual argument, in the order the number should be derived.

1. **Derive from the time budget, not from folklore.** The requirement is a 10-minute phone read. A decision item with three evidence lines, an impact number and an `if_ignored` clause takes 90–120 seconds to read and judge honestly; the scorecard header and the task list take 2 minutes. That leaves ~8 minutes → 4–5 items. **Five is the largest number that fits the stated constraint.**
2. **Three is too few given the arrival process.** Nine departments; typical days generate 1–3 genuine T2 items, but PO weeks, Ramadan buffer sizing and US-launch gates generate 6–9 on the same morning. With a cap of 3 and a 48-hour approval expiry, a peak day forces real money decisions into expiry and re-proposal — which consumes *more* of Rami's attention later and delays 21-day-lead-time purchases. Cap 3 optimises the median day and fails the days that matter.
3. **Seven breaks the read.** Choice-overload evidence: 24 jams attracted more attention than 6 but converted 3% vs 40% (REPORTED — Iyengar & Lepper 2000 via multiple summaries); the Chernev/Böckenholt/Goodman meta-analysis of 99 studies finds the effect strongest exactly where the chooser is effort-minimising and the choices are complex (REPORTED — chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf, could not be opened today). A ranked list is not a choice set, which softens the effect — but a phone at 07:10 is the effort-minimising case, and item 7 will be rubber-stamped or ignored. A rubber-stamped one-way door is worse than a deferred one.
4. **The ops-analogue agrees.** Google SRE's on-call guidance is a maximum of ~2 actionable incidents per 12-hour shift, and 8–10 means you have an alerting problem, not an on-call problem (REPORTED — sre.google/sre-book/being-on-call/). Our items are batched and pre-reasoned rather than interrupting, so 5 is deliberately above 2; but the diagnostic transfers exactly: **if the list is full every day, the tier table is wrong, not Rami.**
5. **The ratchet does not need more.** Promoting a class from T2 to T1 requires ≥20 approved proposals of that class in 30 days (VERIFIED — `AGENTS.md` §5). Five/day allows ~150/month; even 3/day allows ~90. Throughput is not the binding constraint, so it cannot be used to argue the cap up.
6. **Dynamic caps fail for a different reason.** "More items when urgent" gives the system an incentive to label things urgent. Instead: fixed cap 5, plus a **P0 lane outside the cap** (§7) that is rate-limited to one wake per 6 hours, plus a **weekly cap of 15** so a burst day cannot be followed by five more full days. The cap flexes *down* automatically (see §4.4) and never up.

**The list may be empty, and often should be.** Empty is a valid output: "Nothing needs you today. 3 items running, 2 due Thursday." Padding a list to look busy is the failure mode that kills every digest ever built.

**Deferred pressure is visible.** Below the five, one line: `deferred: 4 (2 PO, 1 coupon, 1 listing) — highest 61.2`. If `deferred > 3` for three consecutive days, the CEO layer must make that item #1 the next morning: *"the queue is over capacity — promote class X to T1, widen guardrail Y, or accept slower decisions"*. The queue reports its own overload rather than silently dropping work.

### 3.6 Ordering, expiry, re-proposal

Order strictly by score, with three overrides:
1. Any item whose deadline is inside 24 hours floats above all others.
2. **No more than 2 items from one department in the five** — one noisy department cannot own the morning. The displaced item keeps its score and reappears tomorrow.
3. Ties break on earliest `expires`, then on higher `r̂`.

Expiry is 48 hours (`AGENTS.md` §4). An expired item is **not** silently re-listed: re-proposal requires fresh data, sets `reproposal_of` and increments `times_reproposed`. At `times_reproposed ≥ 3` it stops being a daily decision and becomes a **monthly-review agenda item** titled "we keep asking about X" — because three re-proposals means the question is wrong, not the answer. `defer` is first-class: it sets `snooze_until`, and the item cannot reappear before that date except on a threshold breach.

### 3.7 Tasks are not decisions

| | Decisions | Tasks for Rami |
|---|---|---|
| Verb | decide (yes/no/pick) | do (a physical act) |
| Executed by | hands runner, after approval | Rami, in the world |
| Cadence | daily, capped at 5 | weekly list; only ≤3-days-due items appear on the daily card |
| Cap | count (5) | **effort**: ≤60 min of estimated Rami-time visible per week |
| Extra required field | `if_ignored` | `why_human` — which rule or capability prevents an agent doing this |

`why_human` is not bureaucracy. The single largest source of tasks here is structural: agents may never log into Seller Central or automate a browser (VERIFIED — `AGENTS.md` §6.1, citing Amazon BSA §19, effective 2026-03-04), so reading the Account Health Rating, most appeals, and some ungating steps are permanently human. Everything *else* on the task list should be attacked as a delegation bug. A task whose `why_human` is "no MCP for this yet" is a roadmap item.

A third class — FYI/observation — is **banned from both lists** and aggregated into the weekly review.

---

## 4. Anti-thrash

An agent company's characteristic failure is not laziness, it is churn: nine departments each proposing a change every morning, none of it attributable.

### 4.1 Minimum evidence windows (status changes)

A KR or scorecard cell changes status only when one of these fires:

- **R1** two consecutive weekly observations beyond the threshold, same side; or
- **R2** three of the last four observations beyond the threshold; or
- **R3** eight consecutive observations on one side of the target line, even inside the threshold (trend detection).

R3 is the Western Electric run rule; eight consecutive points on one side has probability ≈ 1/256 under a stable process, and Nelson's 1984 revision uses nine (REPORTED — qualitygurus.com/nelson-rules-and-western-electric-rules-for-control-charts/, metricgate.com/blogs/western-electric-vs-nelson-rules-spc/). Eight weekly points is two months, which is the right patience for a business this size. R1 alone (the rule already in `docs/DECISION-CONTROL-PLANE.md`) catches step changes but is blind to slow drift; R3 is the drift detector.

KR *targets and definitions* never change on evidence. They change at a review boundary, or not at all (§4.3).

### 4.2 Cooldowns (per target, per action type)

| Action | Cooldown | Basis |
|---|---|---|
| Bid change, same target | 24h (existing T1 rule); **7 days if same direction twice** | practitioner guidance is ~1 week between optimisation runs, and ~15–20 clicks before judging a keyword at 10% CVR (REPORTED — adlabs.app, sellerapp.com) |
| Budget increase after a decrease | 72h | prevents oscillation around the daily cap |
| Price change, same SKU | 14 days | plus Amazon's own floor: human authorisation for >20% moves in 24h (VERIFIED — `AGENTS.md` §5) |
| Listing text/images | 21 days | indexing and conversion need to settle before re-reading the result |
| Campaign structure | 14 days | no rule automation under 10 days of history (VERIFIED — advertising charter) |
| PO, same SKU | 1 per lead-time window (21 days) | avoids double-ordering across two runs |
| Coupon/deal, same SKU | 21 days | protects reference price |

Cooldowns are enforced at the **gate**, before scoring, and every blocked proposal is logged. The log of blocked proposals is itself a thrash metric.

### 4.3 Change budget and strategy freeze

- **Weekly change budget:** at most **20% of active targets** (SKUs × action types) may be touched in a week, and at most **2 structural changes** (campaign structure, listing rewrite, price-band edit) company-wide. If departments want more, they must retire something. The point is attribution: if everything changes every week, no outcome can ever be attributed to a change, and the knowledge layer never compounds.
- **Strategy freeze:** objectives and KRs are frozen between monthly reviews and quarterly boundaries. Four named override triggers unfreeze them, and only these: (1) account suspension or AHR <200; (2) hero SKU stocked out >3 days; (3) cash below one PO cycle; (4) an Amazon/xAI/Anthropic/OpenAI policy change touching automated access (the `AGENTS.md` §6.9 kill-switch condition). The CEO layer may *propose* a change any day; it may *apply* one only at a boundary or under a named trigger.
- **Monthly repairs, not rewrites:** a mid-quarter KR repair must be a diff naming the exact field, the reason and the evidence — never a silent full rewrite. (The plan-stability literature's finding that repairing a plan beats replanning from scratch is cited in the earlier `docs/research/goal-patterns-report.md` — REPORTED, ICAPS 2006 plan-stability paper.)

### 4.4 Promotion thresholds for knowledge

| Level | Bar | Effect |
|---|---|---|
| E0 | 1 observation | stays in `memory/<date>.md`; never cited in a proposal as a rule |
| E1 | ≥3 observations, same direction, spanning ≥2 weeks | candidate pattern in `memory/MEMORY.md`, marked `candidate` |
| E2 | E1 + one ledger-verified action→outcome pair | playbook entry with `since:` and `source:` |
| E3 | survived one monthly falsification attempt against the last 30 days | promoted; may be cited as a rule |

Decay at 90 days without reinforcement is already law (`AGENTS.md` §9, VERIFIED).

### 4.5 The CEO layer measures its own thrash

`state/ceo.md` carries these six every week, and `strategy/THRASH.md` every month:

| Metric | Definition | Alarm |
|---|---|---|
| Reversal rate | actions reversed or undone within 14 days ÷ actions taken | >10% |
| Re-proposal rate | decisions proposed ≥2 times ÷ decisions presented | >20% |
| Plan-edit count | KR/objective field edits per month | >2 |
| Attribution rate | decisions with a measured 30-day outcome ÷ decisions executed | <60% |
| Override rate | Rami rejections ÷ items presented | >30% (weights are wrong) or <2% (rubber-stamping) |
| Queue pressure | mean deferred count | >3 for 3 days |

**Auto-throttle:** if reversal rate >10% or re-proposal rate >20% in a week, the daily cap drops to **3** for the following week and the CEO layer files a decision item explaining why. A system that churns should ask for *less* of Rami's attention, not more — this is the mechanism that stops an unhealthy CEO layer from consuming its board.

Note the override-rate band is two-sided on purpose. Near-zero rejection means the list has become a formality; the monthly review then re-checks whether those classes should have ratcheted to T1 already.

---

## 5. Meeting rhythm as agent runs

All times Asia/Jerusalem. Amazon's business day closes 07:00 local (VERIFIED — `AGENTS.md` §1), so every CEO run sits after 07:00 and sees a complete day.

| Cadence | When | Run | Produces | Rami's time |
|---|---|---|---|---|
| Daily stand-up | 06:15–06:40 depts → 07:00 Chief of Staff brief → **07:10 CEO** | aggregate state files, gate + score candidates | `briefs/<date>-decisions.md` (≤5) and `briefs/<date>-tasks.md` (due ≤3 days), Decisions board updated, push card | **≤10 min** |
| Weekly review | Mon 06:00–06:35 depts → **07:15 CEO** | scorecard, KR status via R1/R2/R3, work-item closure | `meetings/<date>-weekly.md`: card + 12-row scorecard + ≤5 IDS issues (issue, owner, next step, by when) + week's decisions | **10 min** (15 if reds) |
| Monthly strategy | 1st business day, after Chief of Staff S&OP, **08:00 CEO** | falsify playbooks, thrash report, KR repairs, tier ratchet, guardrail proposals | `meetings/<date>-monthly-strategy.md` + `strategy/THRASH.md` | **30 min**, the one long meeting |
| Quarterly planning | Dec 15 / Mar 15 / Jun 15 / Sep 15 | propose ≤3 objectives, ≤8 KRs, ≤5 initiatives, `cost_of_miss_cad` per objective, guardrail numbers, blackouts | `strategy/quarters/<q>.md` (T3 — Rami decides) | **60 min**, once a quarter |

EOS's L10 is 90 minutes with a fixed seven-part agenda and 3–5 issues solved per meeting (REPORTED — eosworldwide.com/level-10-meeting). We keep the *shape* (scorecard → headlines → IDS → to-dos) and delete the meeting: the agents do segue, scorecard and headlines in files; Rami does only the IDS answers that are actually his, which is what the decision list is.

**Every artifact starts with a Card.** Max 12 lines, no tables, no links needed to act — the push message is the card, the file is the detail. This is the only formatting rule that makes 10 minutes on a phone possible.

---

## 6. Cascade without Rami creating tasks

The loop, once a week, with a daily fast path:

1. **Derive.** For every KR that is not green, the CEO layer writes a **work item** into the owning department's inbox: `goal_id`, the gap (current vs target vs date), binding constraints (guardrails, cooldowns, blackouts), the expected form of the answer (proposal / data / plan), and `needed-by`. It never specifies *how*; departments own method (`AGENTS.md` §7.5).
2. **Departments derive their own job list.** Weekly job list = standing charter duties + open work items ordered by their KR's score. Nothing else. The charters already say what each department does; the work items say which of it matters this week.
3. **Write back.** Results land in `state/<dept>.md` and in proposals; every proposal names `goal_id` (already mandated in `docs/DECISION-CONTROL-PLANE.md`, VERIFIED).
4. **Close the loop.** At the next weekly run every work item must be *answered*, *superseded* or *dropped with a reason*. Unanswered past `needed-by` becomes an escalation and a scorecard row ("work items overdue").
5. **Progress ledger.** The CEO keeps `strategy/PROGRESS.md` with, per work item: `is_satisfied`, `is_progress_being_made`, `is_in_loop`, `next_owner`, `instruction`. These field names are lifted deliberately from Magentic-One's Orchestrator progress ledger — `is_request_satisfied`, `is_progress_being_made` ("True if just starting, or recent messages are adding value"), `is_in_loop` (detects "repeated requests and/or getting the same responses as before"), `next_speaker`, `instruction_or_question` — with an outer loop that revises the fact sheet and plan when progress stalls, asking the model to "explain what went wrong on this last run (the root cause)" (VERIFIED — `raw.githubusercontent.com/microsoft/autogen/main/python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_magentic_one/_prompts.py`, read 2026-09-06). The adaptation that matters for us: **`is_in_loop = true` does not trigger a re-plan; it escalates to the monthly review.** Magentic-One re-plans because it is solving a task in one session. A company re-planning weekly is thrashing.

Rami's only input path is `requests/ceo/inbox/` (or a `Proposed` row on the Strategy board), which becomes a candidate objective at the next boundary. He never writes a work item, and never assigns a department.

Orchestrator-worker delegation is the standard shape across the current generation of frameworks — CrewAI's hierarchical process with a manager agent, the OpenAI Agents SDK's handoffs, agents-as-tools and guardrails (VERIFIED — github.com/openai/openai-agents-python README: "Delegating to other agents for specific tasks", "Configurable safety checks for input and output validation"), and Anthropic's lead-agent/subagent research system (REPORTED — cited in `docs/research/goal-patterns-report.md`). The relevant lesson for us is the failure mode all of them document: **over-decomposition and duplicated work when task descriptions are vague.** Hence the required fields on a work item and the ≤8 KR ceiling.

---

## 7. Escalation and silence

| Lane | Trigger | Channel | Rate limit |
|---|---|---|---|
| **P0 — wake now** | account suspension/deactivation; AHR <200 or any *critical* policy violation; hero SKU listing takedown; hero SKU projected OOS inside lead time with no PO possible; suspected fraud or unauthorised account access; disbursement/payment hold; a write that failed mid-execution leaving inconsistent state; Amazon/model-provider notice touching automated access; ad spend >2× daily cap | push, any hour | **1 wake / 6h**; coincident P0s merge into one message |
| **P1 — daily list** | anything involving money; deadline inside 7 days; a KR that turned red under R1/R2/R3; an expired approval worth re-proposing | 07:10 card | cap 5 |
| **P2 — weekly** | single-week yellow; competitor moves without margin impact; patterns at E1/E2; tier-ratchet candidates | Monday card | ≤5 IDS issues |
| **P3 — silence** | everything below threshold | `state/*.md`, `memory/<date>.md` only | — |

Two rules keep P0 honest:

- **Corroboration.** A P0 should be confirmed by a second data path before it wakes Rami. DataDoe is currently the only Amazon access (VERIFIED — `docs/os-research/_CONTEXT.md`), so corroboration is often impossible; the rule is therefore: single-source P0 is permitted **only** for the enumerated list above, and the message must say `single source — unconfirmed`. Everything else with one source is P1.
- **Tool failure is not silence.** If a tool fails, the department says so in its state file and stops (`AGENTS.md` §6.8). The CEO layer converts "department did not run" into a visible line at the top of the card. A quiet morning must be provably quiet, not merely empty.

---

## 8. Board schemas

Six boards, all mirrors of repo files, all carrying `repo_path` + `commit`.

**Strategy board** (groups = quarters; items = objectives)
`name` · `quarter` (dropdown) · `status` (Green/Yellow/Red/Done) · `owner_dept` (dropdown) · `north_star_link` (link) · `cost_of_miss_cad` (numbers) · `slack_weeks` (numbers) · `frozen_until` (date) · `override_triggers` (dropdown, multi) · `key_results` (connect → KR board) · `initiatives` (connect) · `narrative` (long_text) · `repo_path` · `commit` · `last_updated`

**KR board** (groups = objectives; items = key results)
`name` · `kr_id` (text) · `metric_id` (text) · `definition` (link) · `direction` (status: up/down/band) · `baseline` (numbers) · `baseline_date` (date) · `target` (numbers) · `current` (numbers) · `as_of` (date) · `owner_dept` (dropdown) · `data_source` (dropdown) · `status` (Green/Yellow/Red/Unknown) · `status_since` (date) · `status_rule` (dropdown: R1/R2/R3) · `confidence` (numbers 0–10) · `definition_of_done` (long_text) · `cadence` (dropdown) · `thrash_count` (numbers) · `work_items` (connect) · `repo_path` · `commit`

**Decisions board** (groups = Today / This week / Deferred / Closed)
`title` · `dec_id` · `status` (Pending/Approved/Rejected/Deferred/Expired/Executed/Failed) · `department` (dropdown) · `tier` (dropdown T2/T3) · `action_type` (dropdown, the enumerated list in `docs/CONVENTIONS.md`) · `score` (numbers, computed in repo) · `impact_cad` (numbers) · `confidence` (status L/M/H) · `reversibility` (status two-way/costly/one-way) · `deadline` (date) · `expires` (date) · `goal_id` (connect → KR) · `evidence` (long_text) · `if_ignored` (long_text) · `approval_file` (link) · `snooze_until` (date) · `reproposal_of` (text) · `times_reproposed` (numbers) · `decided_by` (people) · `decided_at` (last_updated) · `outcome_cad_30d` (numbers, filled at +30d) · `ledger_ref` (text)

There is deliberately **no manual priority column.** Priority is computed; a human-editable priority field is how a scoring system dies.

**Tasks-for-Rami board** (groups = This week / Next / Waiting / Done)
`task` · `why_human` (long_text, required) · `est_minutes` (numbers) · `due` (date) · `hard_deadline` (checkbox) · `consequence_if_missed` (long_text) · `goal_id` (connect) · `department` · `status` · `evidence` (link) · `recurring` (dropdown) · `repo_path`

**Work-items board** (CEO → departments): `title` · `goal_id` (connect) · `dept` · `expected_output` (dropdown: proposal/data/plan) · `needed_by` (date) · `constraints` (long_text) · `is_satisfied` / `is_progress` / `is_in_loop` (checkboxes) · `answer_ref` (link) · `status`.

**Scorecard board** (12+3 items, one per metric): `metric` · `type` (lead/lag) · `owner_dept` · `source` · `green/yellow/red` (text) · `current` (numbers) · `prev` · `avg_4wk` · `status` · `status_rule` · `note`. Weekly history is appended in `strategy/scorecard/YYYY-Www.md`, never overwritten.

---

## Implications for the design

1. **Build the CEO layer as a scoring function plus four files, not as a smarter agent.** The gates, the cooldown table, the score and the cap are deterministic Python over YAML. The model writes prose (`if_ignored`, narratives, IDS issues) and proposes; it does not rank. A ranking an LLM re-derives every morning is a ranking that thrashes.
2. **The cap is 5, hard, dropping to 3 automatically when the layer is churning, with a P0 lane outside it and a weekly cap of 15.** The list may be empty. Deferred count is always shown.
3. **Move the gate before the score.** Most of the value is in what never reaches the list. The "could this have been T1?" gate is the ratchet's feedback loop; log every bounce.
4. **Immutable metric ids and repo-side computation** are what make the scorecard trustworthy across runtimes. monday's formula and mirror values are API-readable today (VERIFIED), but the score belongs in git.
5. **Price the strategic work.** `cost_of_miss_cad` and `slack_weeks` per objective are the single cheapest change that lets US-launch decisions compete honestly with Canadian PO decisions on one list. Ask Rami for these two numbers per objective at quarterly planning; they take two minutes each and they do more work than any other input.
6. **`why_human` on every task turns the task list into a delegation roadmap.** Today most entries will read "BSA §19 — no browser automation"; those are permanent. The rest are missing tools.
7. **The CEO layer must publish its own thrash metrics before it is allowed to publish anyone else's.** Ship `state/ceo.md` with the six metrics in week one, at T0, before it is allowed to generate decisions.
8. **Sequence:** week 1, CEO at T0 — writes scorecard and shadow decision list, no push, Rami grades it against what he would have done. Week 2, the daily card goes live at cap 3. Week 4, cap 5 and work items start cascading. Quarterly planning for 2026-Q4 is the first real boundary.

## Open questions

1. **`cost_of_miss_cad` for the US launch.** What is missing "stock in US FBA by mid-January 2027" actually worth — the whole Ramadan 2027 window, or a deferral to the next year? Every strategic ranking depends on this one number, and only Rami can set it.
2. **Guardrail numbers are still placeholders** (`AGENTS.md` §4 says "TODO — Rami confirms in week one"). The scoring function is calibrated against CAD 5,000 as "full impact"; if the monthly PO ceiling moves, `v̂`'s normaliser moves with it.
3. **Which of the 12 scorecard rows can actually be computed from DataDoe today?** Buy Box win %, unit-session %, ODR and stranded inventory each need a specific synced report. Untested here; a one-run spike would settle it and might force manual rows.
4. **AHR is human-read only.** Amazon's own account-health pages could not be opened today, and the agent policy bars browsing them. Is there any API/MCP path to AHR, or is row 12 permanently a weekly Rami task?
5. **Weight calibration.** The 0.40/0.25/0.15/0.20 weights are a prior, not a finding. After ~40 decisions, check rank-correlation between score and (approve/reject × realised 30-day impact) and re-fit at a quarterly boundary.
6. **Viva Goals / Ally.io status** — could not confirm today (learn.microsoft.com blocked, search budget exhausted). Relevant only as a cautionary tale about hosting the goal object in a vendor product; the design here does not depend on it.
7. **Second brand instantiation.** The strategy objects are per-company files; the scoring function and gates are shared. Confirm the intended layout (`companies/<brand>/strategy/**` vs one repo per brand) before the CEO layer hard-codes paths.
