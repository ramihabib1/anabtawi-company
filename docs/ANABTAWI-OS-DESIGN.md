# Anabtawi OS — the operating system that runs the company

**Version 1.1 — 2026-09-06 — designed from a blank page; for Rami's approval before anything is built in monday. This repository is the company; nothing in it descends from an earlier design.**

This is the design document. It is the output of a founding engagement that started from a blank page, ran ten parallel research surveys (in `docs/os-research/01..10`), scored four finalist architectures against Rami's weights, and chose one. Every component below names the alternatives it beat. Every claim that could not be opened at its primary source today is marked and collected in §14 as a week-one verification list, because the research environment could reach GitHub, Anthropic's docs and the live monday API but not Amazon, DataDoe, OpenAI, xAI or monday's help centre.

Read §0 first. It is one page and it is the whole decision.

---

## 0. The decision on one page

**What we build.** A company of nine AI departments defined entirely as text in one git repository, run headless on Rami's Claude Max subscription by `launchd` on the Mac mini, reading the business through MCP servers (DataDoe for Amazon, Keepa for competitors, Intuit's QuickBooks MCP for the books, the official Amazon Ads MCP when credentials land), and writing everything a human needs to see into one monday.com workspace: strategy, key results, projects and milestones, work items, decisions, the SKU catalog, and the knowledge the company has validated. A separate deterministic "hands" runner on the same machine, with no language model inside it, is the only process that holds a write credential. It polls the monday Decisions board and the repo every five minutes, re-validates each approved packet against live data, executes it through the official API, verifies by read-back, and appends a hash-chained line to the ledger. A CEO layer, itself just a scoring function plus four files, owns strategy and key results, produces a weekly scorecard, and hands Rami at most five ranked decisions a day with evidence, impact, deadline and an approve/reject status he taps on his phone.

**Why this beat the alternatives.** It scored 87 of 100 against Rami's weights. "monday-native" (monday agents as departments) scored 48: verified today, a monday agent cannot reach DataDoe or any external MCP server, monday's code sandbox is network-locked to `api.monday.com`, and Pro keeps the activity log for one year. "Orchestrator platform" (Paperclip-class control plane with its own database) scored 68: it adds a second source of truth, a six-month-old dependency shipping nightly, and a credential-holding process the vendor terms forbid. "Hosted vendor agents" (DataDoe scheduled agents plus Claude Routines, no Mac mini) scored 51: nothing in that stack holds a durable approval object, and Routines are a research preview capped at one run per hour with a daily allowance. Custom software was excluded on Rami's own evidence.

**What it costs.** About CAD 285 a month in new tools for six months, falling to about CAD 150 (DataDoe USD 97, Keepa €49, Link My Books USD 41, Helium 10 USD 99 for six months only, Getida on success fee). Subscriptions already held cover the models. Budget USD 50 a month of API credits as an overflow lane. Second brand: one afternoon, one new API key.

**What changes from the brief, stated once with evidence.**
1. Ramadan 2027 begins about **8 February 2027**, not 17 February (that is Ramadan 2026). The US stock-in date moves to **about 10 January 2027**. Sailing must leave by late November.
2. Register as a **private SP-API developer and self-service Ads API advertiser this month**. Amazon announced USD 1,400/year developer fees in November 2025 and cancelled them in May 2026 (announcement VERIFIED on GitHub, cancellation REPORTED). "DataDoe only" was correct under fees and is now the single point of failure in the design. DataDoe stays the core read layer and the first write path; the private app is the exit.
3. **Five decisions a day, hard cap**, derived from a ten-minute phone read at 90–120 seconds per honestly judged item, with a P0 lane outside the cap (one wake per six hours), a weekly cap of 15, and an automatic drop to three when the layer's own reversal or re-proposal rate alarms. The list may be empty. Approvals are budgeted separately: at most three new money packets a day, five pending.
4. **The daily cadence is data-driven, not 07:00.** DataDoe refreshes North-American marketplaces at about 05:00 marketplace time, which is early afternoon in Jerusalem. The main department runs are placed at 15:30–16:30 Asia/Jerusalem with the decision card at 17:00, so Rami decides in the evening and the hands runner executes overnight. A light 07:15 exception scan covers account health and ad pacing from intraday data. Day one verifies the actual freshness timestamp and may shift the slots.
5. **Amazon's own Automate Pricing is the pricing engine.** Rami approves a price band per SKU once; Amazon moves the price inside it; agents propose band changes only. This collapses the largest approval class to near zero and is policy-clean by construction.
6. **monday agents are not a harness.** They schedule and summarise; they never touch money or Amazon. monday is the management surface and the approval UI, driven from the repo through its MCP server.

**The first four weeks.** Week 1: registrations, vault, Mac mini, DataDoe freshness check, BSA §19 text pasted into the repo, monday workspace built from this schema, all departments at T0. Week 2: SKU profiles live, scorecard live, shadow decision list graded by Rami. Week 3: daily card live at cap 3, hands runner executing approved band changes and dry-run-validated ads packets. Week 4: cap 5, work items cascading, first monthly review scheduled. §13 has the full build order.

---

## 1. Goal, constraints, and where I disagree

### 1.1 The goal, restated as testable properties

The system is done when, for thirty consecutive days:

| Property | Test |
|---|---|
| Runs unattended | every `state/<dept>.md` carries that day's date without Rami touching a keyboard |
| Creates work for Rami, not the reverse | Rami has created zero tasks; every decision he took arrived on the card |
| Money never moves without him | the ledger shows no T2/T3 execution without an approval id, and the bank shows no payment the ledger did not predict |
| Learns | `patterns/` has grown, at least one pattern has been promoted or falsified by evidence, and `ledger/outcomes.csv` scores every decision older than its review window |
| Portable | one department has been run on a second harness from the same folder with a one-line adapter change |
| Exportable | monday boards can be regenerated from the repo, and the repo needs nothing from monday to run |
| Multi-brand ready | a second brand can be instantiated from the schema file in an afternoon |

### 1.2 Constraints that actually bind

- Amazon BSA §19 (effective 2026-03-04): no browser automation, no scraping; every automated action traceable to a registered application; documented human authorisation for price moves over 20% in 24 hours and batches of 500 or more ASINs (REPORTED from eight consistent secondary sources; the policy text itself must be pasted into `docs/policy/amazon-agent-policy.md` in week one).
- Anthropic's compliance page (VERIFIED): an end user may sign in to the unmodified Claude Code binary with their own subscription, and Anthropic documents a one-year subscription OAuth token for unattended CI. What is prohibited is a third-party product holding or brokering the credential. Ordinary individual usage is the enforcement surface, so brand two gets its own API key.
- monday Pro (VERIFIED live): 10,000 API calls a day, ~20M complexity a minute, formula and mirror columns read-only and unfilterable, activity log kept one year, agents cannot call external MCP servers, `execute_code` cannot leave `api.monday.com`.
- DataDoe (VERIFIED from its public repos): every write is an `actions_start` call with `dryRun`; action types are disabled by default and enabled per type; dry run works even when the type is disabled; its "approval" is an in-chat confirm, not a durable object.
- Rami's time: ten minutes a day on a phone, thirty minutes once a month, an hour once a quarter.

### 1.3 Where I disagree with the brief

Beyond the six changes in §0: the brief lists "seats for two non-technical family members" as a first-class requirement. Rami later said only he manages everything for now. The design keeps the seats as a permission layout that can be switched on in an hour (§10.4) and spends no build time on them before month three. And the brief treats "DataDoe's scheduled agents and Actions" as candidate substitutes for departments. They are not: the scheduled agents run an undisclosed model with no callable API, and the Actions approval is not an approval. They are adopted as a safety net and a validator, not as departments.

---

## 2. Finalists and scoring

Weights are Rami's: strategy and goals 20, decisions and tasks for him 20, unattended with approvals 20, subscriptions and no lock-in 15, portability and tool access 10, audit and budgets 10, maturity and maintenance 5. Each criterion scored 1–10, weighted, out of 100.

| Finalist | Strategy | Decisions | Unattended | Subs / lock-in | Portability | Audit | Maturity | **Total** |
|---|---|---|---|---|---|---|---|---|
| **B. Git spine, monday surface, Mac mini hands** | 9 | 9 | 8 | 9 | 9 | 9 | 7 | **87** |
| C. Orchestrator platform (Paperclip-class) | 7 | 7 | 8 | 6 | 6 | 7 | 3 | 68 |
| D. Hosted vendor agents, no machine | 5 | 5 | 5 | 6 | 4 | 5 | 5 | 51 |
| A. monday-native | 7 | 6 | 4 | 3 | 3 | 4 | 6 | 48 |

**Why B wins on the heavy criteria.** Strategy and decisions are files plus a deterministic scoring function, which any harness can run and any reviewer can diff; A and D would put them inside a vendor's agent whose model and cost are opaque. Unattended-with-approvals needs a durable approval object with expiry, re-validation and a ledger; only B has one, because the runner is ours. Subscriptions and no lock-in: B runs on Max under the exact carve-out Anthropic documents, and every vendor exit in §12 is a day, except DataDoe, which the SP-API registration fixes.

**Why C loses despite being close in spirit.** A control plane with its own Postgres is a second source of truth, which the constitution forbids; the package is six months old; and an orchestrator that holds a Claude credential is the shape Anthropic explicitly prohibits. C survives as an optional UI later, under a hard rule: it may launch the CLI, never hold the credential.

**What B borrows from D.** DataDoe recurring exports as a nightly file drop and one daily anomaly email, so the company stays readable when the Mac mini or the MCP is down; and a Claude Code Routine as a cloud backup for the daily brief only.

---

## 3. Architecture

```
┌──────────────────────────────── RAMI (phone) ───────────────────────────────┐
│  monday mobile: Cockpit dashboard · Decisions board (tap Approve/Reject)     │
│  SKU Profiles · Tasks for me · Scorecard          Telegram: P0 wakes, card  │
└───────────────▲───────────────────────────────────────────────▲─────────────┘
                │ projection (repo → monday, nightly + per run)  │ decisions (monday → repo, 5-min poll)
┌───────────────┴───────────────────────────────────────────────┴─────────────┐
│  MANAGEMENT SURFACE  monday.com Pro · one workspace per brand                │
│  Boards: Strategy · Key Results · Scorecard · Decisions · Tasks for Rami ·   │
│  Work Items · Products · SKU Profiles · Suppliers & POs · Calendar ·         │
│  Run Health      Docs: Strategy · Weekly Review · Playbook Index            │
│  Dashboards: Cockpit · Finance · US Launch      Forms: Ask the company       │
└───────────────▲───────────────────────────────────────────────▲─────────────┘
                │ monday MCP (read/write as Rami)                │
┌───────────────┴──────────────────────────┐   ┌────────────────┴─────────────┐
│  BRAIN  (Mac mini, user `ops`, launchd)  │   │  HANDS  (Mac mini, launchd)   │
│  9 departments = folders of text         │   │  hands/runner.py  no LLM      │
│  Claude Code headless on Max (default)   │   │  every 5 min: pull → poll →   │
│  Codex CLI (2nd opinion) · Routine (bkp) │   │  re-validate → dry-run →      │
│  read-only credentials only              │   │  execute → read-back → ledger │
│  writes: repo + monday projection        │   │  write credentials via op run │
└──────┬─────────────────────────┬─────────┘   └───────┬──────────────────────┘
       │ MCP reads               │ git                  │ official APIs, writes
┌──────▼──────────┐  ┌───────────▼───────────────┐  ┌───▼──────────────────────┐
│  DATA (read)     │  │  KNOWLEDGE (git, private)  │  │  WRITE PATHS              │
│  DataDoe MCP     │  │  AGENTS.md · departments/  │  │  DataDoe Actions (dryRun) │
│  Keepa API       │  │  products/ · patterns/     │  │  Amazon Ads MCP (own creds)│
│  QuickBooks MCP  │  │  playbooks/ · state/       │  │  SP-API private app       │
│  Ads MCP (read)  │  │  approvals/ · ledger/      │  │  Automate Pricing (bands) │
│  Walmart API     │  │  strategy/ · memory/       │  │  QBO MCP (bills, later)   │
└─────────────────┘  └───────────────────────────┘  └──────────────────────────┘
      Safety nets: DataDoe recurring exports + anomaly email · GitHub Actions staleness check ·
      Healthchecks.io dead-man pings · Claude Routine backup for the daily brief
```

### 3.1 The six layers and the one rule each

| Layer | What it is | The rule |
|---|---|---|
| Management surface | monday.com, one workspace per brand | A projection of the repo. Every board row carries `repo_path` and `commit`. Rami's only inputs are status taps on Decisions and the "Ask the company" form. |
| Brain | Nine department folders run headless | Reads through MCP with read-only keys; writes only files and the monday projection. Never holds a write credential. |
| Hands | `hands/runner.py`, deterministic Python | The only process with Amazon or QuickBooks write credentials, injected per run by `op run`. No model inside. Polls; nothing inbound. |
| Knowledge | The git repository | System of record for everything authored: strategy, charters, playbooks, patterns, SKU facts, approvals, ledger. Harness memory is turned off. |
| Data | DataDoe, Keepa, QuickBooks, Ads, Walmart | Read through MCP or REST, cached into the repo once per day, never re-fetched for the same day. |
| Scheduler | `launchd` plus a GitHub Actions watchdog | Schedules live outside every harness. A stale state file is a failed run and is enforced, not implied. |

### 3.2 Components and the alternatives each beat

| Component | Chosen | Beat | Why |
|---|---|---|---|
| Management surface | monday Pro, one workspace per brand | Notion, Linear, a Vibe app, a custom web app | Rami's decision; mobile status taps are the cheapest approval gesture; MCP is first-party and verified; structural board duplication makes brand two native |
| Department harness | Claude Code headless on Max via `launchd` | monday agents; Paperclip; Routines as primary; Grok bots | Only harness with a verified legal path for unattended subscription use, local files, `.mcp.json`, and no credential brokering; Routines are a research preview with a 1-hour floor; monday agents cannot reach tools |
| Scheduler | `launchd` LaunchAgents + GitHub Actions cron watchdog | n8n, Trigger.dev, Inngest, Temporal, Routines, Desktop tasks | Zero maintenance, survives harness changes, and the watchdog is the failure-notification layer the Mac lacks |
| Hands trigger | 5-minute poll of monday and git, nothing inbound | monday webhook to a tunnel; monday automation calling a webhook | A poll fails into delay; a webhook fails into silent loss; approvals here are never latency-sensitive |
| Amazon read layer | DataDoe MCP (core) + recurring exports as file drop | Direct SP-API only; Helium 10 MCP; Sellerboard; Pacvue | Hosted, first-party MCP, Seller + Vendor + Ads in one schema, 735-day backfill, USD 97 flat for unlimited accounts |
| Amazon write paths | DataDoe Actions now; own Ads API + SP-API private app registered now; Automate Pricing for bands | DataDoe only; a repricer; SellerMate hosted guardrails | Redundancy: DataDoe survives a Mac outage, direct APIs survive a DataDoe outage; bands remove the largest approval class |
| Competitor data | Keepa API (+ forked 150-line MCP wrapper) | Jungle Scout, SmartScout, DataDive, any scraper | The only legal, non-substitutable price/BSR history under BSA §19 and Hard Rule 2 |
| Accounting | QuickBooks Online + Intuit's official MCP (read now, bills later) + Link My Books | A2X (3× the price at this volume), Sellerboard | Official, Apache-2.0, local stdio, write flags; settlement posting outsourced to the cheaper bridge |
| Knowledge layer | git markdown spine + monthly CSV + DuckDB at query time + monday docs as projection | Mem0, Letta, Zep, Supabase + pgvector, Obsidian Sync, monday docs as store | Six of eight knowledge classes need exact or time-series retrieval; scored 36/45 vs 30 for monday and ≤24 for memory vendors |
| SKU profile | Products board + SKU Profiles board (SKU × marketplace) + `products/<brand>/<sku>.md`; nightly build is the sole writer of numbers | monday-only; Postgres + mirror; Vibe app as store | monday Pro forgets its activity log after a year; 120 records × 365 snapshots would exhaust the 10,000-item cap in 83 days; Vibe cannot be built on mobile |
| CEO layer | YAML strategy objects + deterministic gate/score/cap in Python + four boards | An LLM that re-ranks every morning; monday AI; an OKR SaaS | A ranking an LLM re-derives daily thrashes; a scoring function is diffable and portable |
| Approval object | Markdown packet with YAML front matter in `approvals/`, mirrored to the Decisions board | DataDoe's in-chat "reply apply"; monday-only status; LangGraph interrupts | Durable, expiring, re-validated at execution, two independent approval paths, one record |
| Secrets | 1Password CLI `op run` (or Doppler free) | Keychain, `.env` files, Infisical self-host | Secrets exist only in the process's memory for the seconds it runs; nothing in the repo; no server to maintain |
| Notifications | monday push + Telegram bot | Slack, email, Pushover | monday is where the tap happens; Telegram is a one-line `curl` from `launchd` for P0 and run failures |
| Reimbursements | Getida (success fee) + own reconciliation against landed cost | Seller Investigators, Carbon6 | Zero fixed cost; and after March 2025 the value moved to auditing Amazon's automated credits, which needs our COGS |
| Listing research | Helium 10 Platinum for six months, then Search Query Performance | DataDive, Jungle Scout, Amazon's browser-only AI tools | The one job our own data cannot do before US traffic exists; cancel the day SQP has US data |

---

## 4. The monday workspace, down to the schema

### 4.1 Principles that the verified limits force

1. **monday is a projection.** The repo writes monday; monday writes the repo through exactly two doors: a status tap on the Decisions board and a submission of the "Ask the company" form. Every item carries `repo_path` and `commit` so a stale row is visible.
2. **No number lives behind a formula or mirror column.** Both are read-only and unfilterable through the API, and a formula referencing a mirror silently returns nothing. Every number Rami sees is a plain Numbers column written by the nightly build.
3. **Hundreds of items, not thousands.** Boards hold current state. History lives in git (`ledger/kpis/`, `state/skus/`). This keeps every board far below 10,000 items and every query cheap.
4. **Budget the API, not the complexity.** Pro allows 10,000 calls a day. The projection uses `update_items` (40 items a call) and `ingest_items` for bulk; nine departments plus the nightly build should stay under 1,500 calls a day. `get_monday_knowledge` is never called at runtime.
5. **Stable column ids.** Every column is created with an explicit id (lowercase, from the schema file), so brand two and the runner share one config. Never hard-code a numeric board id in a skill; resolve by board name at boot and cache.
6. **Stay on Pro.** Everything needed is at Pro; Enterprise buys column permissions, bigger boards and residency, none needed before brand three. Keep the grandfathered 2-seat bucket. Family members join as free viewers or unlimited guests, not seats.

### 4.2 Workspace layout

Workspace **`Anabtawi OS`** (one per brand; brand two gets `<Brand> OS`). Four folders.

| Folder | Boards | Docs |
|---|---|---|
| **1 Command** | Strategy · Key Results · Initiatives · Scorecard · Decisions · Tasks for Rami | Strategy (mirror of `strategy/STRATEGY.md`) · Weekly Review (one doc per week) · Monthly Review |
| **1b Work** | Projects & Milestones · Work Items | Project briefs (attached to each project) |
| **2 Catalog** | Products · SKU Profiles · Suppliers & POs | SKU decision docs (one per SKU, attached to the item) |
| **3 Operations** | Knowledge · Calendar & Blackouts · Run Health · Requests (inter-department, read-only mirror) | Playbook Index · Patterns Digest · Operating Notes |
| **4 Later** | Wholesale Pipeline (sales seat, month 3+) · Finance Close (finance seat, month 3+) | — |

Dashboards: **Cockpit** (Rami's home), **Finance**, **US Launch**. Forms: **Ask the company**. All boards are Main boards (not private) so the workspace can be saved as a template for brand two; sensitive columns are handled by keeping Suppliers & POs on a separate board with view-only permissions for guests.

### 4.3 Board schemas

Column ids are the identifiers the runner and departments use. Types are monday column types. "Writer" is the only process allowed to write that column.

**Decisions** (groups: Today · This week · Deferred · Executed · Closed) — the approval queue and Rami's ranked list, one item per decision packet.

| id | Title | Type | Writer | Notes |
|---|---|---|---|---|
| name | Title | name | CEO | imperative, ≤50 chars |
| dec_id | Decision id | text | CEO | `dec-YYYYMMDD-NN`, matches `approvals/` file |
| decision | Decision | status | **Rami** | Pending · Approved · Rejected · Deferred · Expired · Executing · Executed · Failed. The runner reads this. |
| rank | Rank | numbers | CEO | 1–5 today; blank if deferred |
| score | Score | numbers | CEO | computed in repo (§7.4) |
| dept | Department | dropdown | CEO | nine departments |
| tier | Tier | status | CEO | T2 · T3 |
| action_type | Action | dropdown | CEO | purchase_order, pricing_band_change, price_change, listing_change, fba_shipment, campaign_create, coupon, buyer_message, vine, reimbursement, strategy, other |
| impact_cad | Impact CAD (30d) | numbers | CEO | signed |
| confidence | Confidence | status | CEO | Low · Medium · High · Certain |
| reversibility | Reversibility | status | CEO | Two-way · Costly · One-way |
| deadline | Deadline | date | CEO | with time |
| expires | Expires | date | CEO | created + 48h |
| if_ignored | If ignored | long_text | CEO | the first thing Rami reads |
| evidence | Evidence | long_text | CEO | citations, ≤2,000 chars |
| dry_run | Dry-run diff | long_text | CEO | before/after table from DataDoe or Ads dry run |
| sku_link | SKUs | board_relation → SKU Profiles | CEO | |
| kr_link | Key result | board_relation → Key Results | CEO | |
| approval_file | Packet | link | CEO | GitHub URL of `approvals/pending/<id>.md` |
| snooze_until | Snooze until | date | Rami | set when Deferred |
| decided_at | Decided at | last_updated | monday | read by the runner for `decided_at` |
| ledger_ref | Ledger seq | numbers | Hands | filled after execution |
| outcome | Outcome | status | Finance | Pending · Hit · Miss · Inconclusive (at review_on) |
| repo_path / commit | | text | CEO | staleness stamp |

**Key Results** (groups = objectives) — `kr_id` text · `metric_id` text · `direction` status (Up · Down · Band) · `baseline` numbers · `baseline_date` date · `target` numbers · `current` numbers · `as_of` date · `owner_dept` dropdown · `data_source` dropdown · `status` status (Green · Yellow · Red · Unknown) · `status_rule` dropdown (R1 · R2 · R3) · `definition_of_done` long_text · `cost_of_miss_cad` numbers · `frozen_until` date · `thrash_count` numbers · `work_items` board_relation → Work Items · `repo_path` · `commit`. Writer: CEO only.

**Strategy** (groups = quarters; items = objectives) — `quarter` dropdown · `status` status · `owner_dept` dropdown · `cost_of_miss_cad` numbers · `slack_weeks` numbers · `frozen_until` date · `narrative` long_text · `key_results` board_relation → Key Results · `repo_path` · `commit`. Plus one status column `proposal` (None · Proposed) that Rami may set to signal "I want to change this" — the only human input on the board; the CEO run turns it into a request.

**Scorecard History** (append-only, 15 rows a week, about 780 a year, archived yearly) — `week` week · `metric_id` text · `kind` status · `value` numbers · `target_num` numbers · `status` status · `as_of` date. Exists only so Chart widgets can show a 13-week trend on the phone; the record is `strategy/scorecard/`.

**Scorecard** (15 items, one per metric) — `metric_id` text · `kind` status (Lead · Lag) · `owner_dept` dropdown · `current` numbers · `prev` numbers · `avg_4wk` numbers · `target` text · `status` status (Green · Yellow · Red) · `status_rule` dropdown · `unit` text · `note` text · `as_of` date. History appended in `strategy/scorecard/YYYY-Www.md`, never here.

**Tasks for Rami** (groups: This week · Next · Waiting · Done) — `why_human` long_text (required) · `est_minutes` numbers · `due` date · `hard_deadline` checkbox · `consequence` long_text · `dept` dropdown · `status` status (Open · Done · Won't do) · `kr_link` board_relation · `evidence` link · `repo_path`. Rami sets `status`; nothing else.

**Work Items** (anyone → anyone; see §4.11) — `wi_id` · `type` status (Proposal · Data · Plan · Fix · Research · Build · Milestone) · `opened_by` dropdown (nine departments or rami) · `dept` dropdown (assigned) · `priority` numbers (computed) · `due` · `needed_by` · `effort_est` numbers · `project` board_relation → Projects · `milestone` text · `kr_link` board_relation · `blocked_by` dependency (self) · `expected_output` status · `constraints` long_text · `is_satisfied` / `is_progress` / `is_in_loop` checkboxes · `answer_ref` link · `status` status (Open · In progress · Blocked · Waiting on Rami · Answered · Superseded · Dropped · Escalated) · `last_touch` · `repo_path`. Subitems are steps (step, owner, status, evidence). Groups: Open · In progress · Blocked · Waiting on Rami · Done · Dropped.

**Projects & Milestones** (§4.11) — `project_id` · `owner_dept` · `objective` board_relation → Strategy · `kr_link` · `timeline` timeline · `status` status (On track · At risk · Late · Blocked · Done) · `progress` numbers (milestones done %) · `next_milestone` text · `next_due` date · `slack_days` numbers (computed) · `critical_path` checkbox · `cost_cap_cad` · `spent_cad` · `brief` doc · `repo_path`. Milestone subitems: `ms_id` · `owner_dept` · `timeline` · `due` · `depends_on` dependency · `gate` checkbox (needs Rami's decision to pass) · `status` (Todo · Doing · Done · Late · Blocked) · `work_items` board_relation · `evidence` link. Seeded projects: US launch 2027 (fifteen milestones from trademark check to post-season sell-down, sailing by 25 Nov, stock sellable by 10 Jan, Ramadan 8 Feb), ten CA activations, Walmart CA monitor, prep-partner selection, brand-two dry run.

**Initiatives** (bets) — `init_id` · `hypothesis` long_text · `serves` board_relation → Key Results · `owner_dept` · `cost_cap_cad` · `spent_cad` · `decision_date` date · `falsifier` long_text · `status` (Running · Won · Lost · Killed) · `project` board_relation · `repo_path`. Killed or renewed at every monthly review.

**Knowledge** (read-only mirror of `patterns/` and skill governance front matter; groups Hypothesis · Supported · Validated · Playbook · Decaying · Falsified) — `kind` status (Pattern · Playbook · Skill · Fact) · `claim` long_text · `scope` text · `owner_dept` · `status` · `confidence` numbers (the reproducible formula) · `confirmations` · `contradictions` · `first_seen` · `last_seen` · `hit_rate` · `firings_90d` · `seasonality_guard` checkbox · `next_test` text · `review_by` date · `evidence` link · `decisions` board_relation → Decisions (the decisions this rule produced) · `repo_path` · `commit`. Views: "What changed this week", "Up for review", "Falsified". No human edits; a disagreement goes through the form and becomes a contradiction with a source.

**Products** (one item per SKU, marketplace-independent) — `sku` text · `brand` dropdown · `category` dropdown · `case_pack` numbers · `moq` numbers · `shelf_life_days` numbers · `meltable` status (Yes · No) · `hazmat` status · `certifications` text · `unit_dims` text · `pkg_dims` text · `supplier` board_relation → Suppliers & POs · `lifecycle` status (Planned · Launching · Active · Declining · Discontinued) · `class` status (Hero · Core · Long-tail · Kill) · `profile` link (git file) · `listings` board_relation → SKU Profiles.

**SKU Profiles** (one item per SKU × marketplace; groups = Hero · Core · Long-tail · Kill · Planned) — the 34 columns in §5.3. Writer: the nightly build only, except `next_action` which departments may set through the build.

**Suppliers & POs** — items are suppliers; subitems are POs. Supplier: `legal_name` text · `country` country · `payment_terms` text · `lead_time_days` numbers · `lead_time_measured` numbers · `bank_on_file` checkbox (never the details) · `contact` email · `last_po` date · `scorecard` numbers. PO subitems: `po_ref` text · `status` status (Proposed · Approved · Paid · Shipped · Received · Closed) · `amount` numbers · `currency` status (CAD · USD) · `skus` text · `ship_date` date · `eta` date · `paid_on` date (Rami sets) · `approval_id` text. Guests never see this board.

**Calendar & Blackouts** — `kind` status (Ramadan · Eid · Prime Day · BFCM · Christmas · Meltable window · Blackout · Fee change · Deadline) · `start` date · `end` date · `marketplace` dropdown · `applies_to` text (SKU list or All) · `source` link. Lunar dates through 2032 are seeded from the repo.

**Run Health** (one item per department) — `dept` name · `last_run` date · `state_date` date · `status` status (OK · Stale · Failed · Paused) · `harness` dropdown (claude-code · codex · routine · grok) · `tools_failed` text · `proposals_open` numbers · `run_minutes` numbers · `log` link. Written by the run wrapper; drives the Cockpit's "is the company alive" battery.

**Requests** (read-only mirror of `requests/*/inbox`) — `from` dropdown · `to` dropdown · `type` dropdown · `needed_by` date · `status` status (Open · Answered · Escalated) · `file` link. Rami can watch inter-department traffic without opening git.

### 4.4 Views

- SKU Profiles: **"Rami — today"** (filter `next_action ≠ Nothing` or `data_health = Broken`, sort Class then Cover days) with columns ordered so the first three are Next action, Cover days, Margin %. Kanban by `class`. Table "US launch readiness" (filter marketplace = US, lifecycle = Planned, show completeness).
- Decisions: **"Today"** (group Today, sorted by rank), "History" (Executed + Closed, last 90 days).
- Tasks for Rami: "Due ≤3 days".
- Key Results: "Reds and yellows".
- Run Health: single table sorted by status.
- Work Items: kanban by status; "Blocked"; "Waiting on Rami"; table grouped by assigned department.
- Projects: timeline view; "Critical path".
- Knowledge: "What changed this week"; "Up for review"; "Falsified".

### 4.5 Dashboards and widgets

**Cockpit** (mobile-first, ≤10 widgets): Battery over Run Health status ("company alive") · Number: decisions pending today · Number: min hero cover days · Number: blended margin after ads · Number: 7-day net revenue CA · Chart: scorecard status counts · List: Decisions "Today" · List: Tasks due ≤3 days · Number: work items blocked or waiting on Rami · Number: patterns validated this month.
**Finance**: Numbers for cash available, PO ceiling used, TACoS, reimbursements pending · Chart of margin by class · List of SKUs below margin floor.
**US Launch**: Number: SKUs through readiness gate of 15 · Number: slack days to 10 Jan 2027 · Chart: readiness by gate · Gantt over the US launch project's milestones · List: blocked or late work items on the project · List: Tasks for Rami tagged expansion · Calendar widget over Calendar & Blackouts.
All widgets read plain Numbers and Status columns. Chart, Gantt and Workload views are browser-only on mobile, so the Cockpit uses Number, Battery and List widgets.

### 4.6 Automations (board recipes, all inside the 25,000 actions a month)

| Board | Recipe | Purpose |
|---|---|---|
| Decisions | when item created in group Today → notify Rami (bell + mobile push) | the daily card arrives as up to five pushes, or one digest notification created by the CEO run via `create_notification` |
| Decisions | when `decision` changes to Approved or Rejected → notify "hands" user (Rami's own account) with the item id | visible receipt; the runner still polls |
| Decisions | when `expires` date arrives and `decision` is Pending → set `decision` to Expired and notify Rami | matches the 48-hour rule without code; the runner also enforces it |
| Decisions | when `decision` changes to Deferred → set `snooze_until` to +7 days if empty | |
| Run Health | when `status` changes to Failed or Stale → notify Rami | the same failure also goes to Telegram from the wrapper |
| Tasks for Rami | when `due` arrives and status Open → notify Rami at 08:00 Asia/Jerusalem | |
| Key Results | when `status` changes to Red → create item in Work Items? **No.** The CEO run does this in the repo, so the two stay consistent. | |
| Suppliers & POs (subitems) | when `status` changes to Paid → notify Rami's finance view and set `paid_on` to today | |
| Work Items | when `status` changes to Waiting on Rami → notify Rami; when `needed_by` arrives and not answered → set Escalated and notify | escalation without a chat |
| Projects (milestones) | when `due` arrives and status not Done → set Late; notify Rami only if `gate` | the critical path announces itself |

Estimated consumption: under 600 actions a month. No AI blocks are used; every AI action costs 8 credits and the reasoning already happens in Claude Code, where monday MCP consumes zero credits.

### 4.7 Workflows, agents, forms, apps

- **Workflows (Pro builder):** none in v1. The multi-board engine cannot reach outside monday; every cross-board update is done by the projection. Revisit if an approval-routing workflow with delay blocks proves useful for the family seats.
- **monday agents:** none in v1. Their model and cost are opaque, they cannot call DataDoe or the Ads MCP, and `run` is fire-and-forget. One candidate later: a "Weekly digest" agent reading the Weekly Review doc, only if Rami wants a monday-native summary.
- **External agent registration:** an upgrade in month three. `connect_external_agent_sync` (pre-release, `API-Version: dev`) would let Rami @mention `@Finance` on a SKU item and have the Mac mini answer. It requires an HTTPS callback, which is exactly the inbound exposure §9 avoids, so it waits until there is a reason.
- **Forms:** one WorkForm, **Ask the company**, writing to a hidden group on the Requests board: `question` long_text · `about` dropdown (SKU · Strategy · Money · Other) · `sku` text · `urgency` status · `wants` status (An answer · A change · A project). The projection copies it into `requests/ceo/inbox/` on the next poll and, when Rami wants a change or a project, opens a Work Item with `opened_by: rami` so he can watch it move. This is Rami's only free-text input path and it is deliberately one form.
- **Vibe:** none in v1. A Vibe item view rendering the one-screen SKU card (§5.5) is the first candidate if the mobile item page proves too loose after a month.

### 4.8 Permissions

| Who | Now | Month 3+ |
|---|---|---|
| Rami | admin, owner of every board | same |
| `ops` machine identity | uses Rami's API token (Pro has no service seat; all agent writes appear as Rami in the activity log, which is why the repo ledger is the audit record) | same |
| Finance family member | — | free **viewer** on Finance dashboard, Scorecard, Decisions (view only); later a seat with "only edit assigned items" on Finance Close if they reconcile payouts |
| Sales family member | — | **guest** on Wholesale Pipeline (edit content), viewer on Products |
| Accountant | — | viewer on Finance dashboard |

Decisions, Suppliers & POs, Strategy, Key Results and Initiatives stay owner-only. Column-level permissions are Enterprise, so on Pro the `decision` column is protected only by board permissions: never grant edit rights on the Decisions board to a seat or guest. The general workaround is separate boards, which is why Suppliers & POs is its own board.

### 4.9 Mobile

Rami's phone home is the Cockpit dashboard. Approval is two taps: open the pushed Decision item, tap the `decision` status, pick Approved or Rejected. Whether the Button column renders and fires on the mobile item card is UNKNOWN; if it does, add a one-tap Approve button in week two. The SKU card is the "Rami — today" view with the first three columns pinned and the last three decisions in a pinned item update refreshed nightly.

### 4.10 Export and exit

Everything on these boards is regenerated from the repo by `bin/project-monday.py`. The exit is: `create_board_export` for each board and `export_markdown_from_doc` for each doc into `exports/monday/`, then stop paying. Two days, verified primitives, and nothing the departments need lives only in monday.

### 4.11 Project management, work tracking and visible knowledge

Three boards make the company's work and learning visible without giving monday any authority over them.

**Work Items** is the general work-tracking object. Anyone opens one: the CEO run from a red key result or a project milestone; any department for itself or for another department (at most five a week per pair, more is a request to the CEO run); Rami through the form. The record is `work/<id>.md` in the repo; the projection mirrors it and reads back only the status Rami may set. A work item has a type, an assigned department, a computed priority (from the key result's score, the due date and how many items it blocks; there is no manual priority column, by design), steps as subitems, `blocked_by` as a dependency on other work items, and the progress-ledger checkboxes. `Waiting on Rami` is a status that must correspond to a Decision or a Task for Rami; the projection refuses it otherwise, so nothing waits on him invisibly. Unanswered past `needed_by` becomes Escalated and reaches his card.

**Projects & Milestones** holds multi-step work with a timeline. A project is owned by one department, serves an objective, has a cost cap, and carries a computed `slack_days` on its critical path. Milestones are subitems with timeline, dependency, owner and a `gate` flag; a gate milestone cannot pass without a Decision. Work items link to the milestone they serve, so the US Launch dashboard shows the Gantt, the blocked items and the days of float in one place. The record is `projects/<id>.md`, and the expansion department's weekly run updates it; the CEO run derives work items from milestones that are due inside two weeks and unstarted.

**Initiatives** are the bets from §7.1 as a board, so the monthly "kill or renew" is a status change Rami can see coming (`decision_date`) with the falsifier written before the bet ran.

**Knowledge** is the compounding loop made visible. Every pattern and every governed playbook or skill is one item, grouped by status from Hypothesis to Falsified, with confidence, confirmations, contradictions, hit rate, firings, `next_test`, `review_by`, and a relation to the Decisions the rule produced. The librarian pass writes it on Mondays and the monthly review rewrites the Playbook group. Rami never edits it: a disagreement goes through the form and becomes a contradiction with a source, which is how a human observation enters the same loop as an agent's. The Patterns Digest doc is the weekly "what we learned" in prose.

What monday does not get: authority. Priority, slack, confidence and status transitions are computed in the repo and written to plain Numbers and Status columns, for the same reason as every other number on these boards.

---

## 5. The SKU profile

### 5.1 Four records wearing one name

Amazon scopes almost everything by marketplace (VERIFIED against its OpenAPI models), and every tool that flattens a product into one table becomes unusable at forty columns. So the profile is four records joined in one view:

| Record | Grain | Lives in | Writer |
|---|---|---|---|
| Product | one per SKU | `products/<brand>/<sku>.md` front matter + Products board | catalog and supply chain (git); build (board) |
| Listing | one per SKU × marketplace | `products/<brand>/<sku>.md` (`listings:` block) + SKU Profiles board | build only |
| Metrics series | one row per SKU × marketplace × day | `state/skus/YYYY-MM-DD.jsonl` and `ledger/kpis/YYYY-MM.csv` in git | build |
| Decisions log | append-only | `## Decision history` in the SKU file, mirrored into the SKU's attached monday doc and pinned update | scoring job, departments |

Grain decision: one board item per SKU × marketplace, not marketplace sub-records, because about 70% of fields are marketplace-scoped and the US launch needs independent cost, band, inventory and ads. US listing records are created now in `Planned`, so launch readiness becomes a board filter.

### 5.2 The git file

```yaml
---
sku: ANB-017
brand: anabtawi
name: Tahini 400g
class: hero                 # hero | core | long-tail | kill
lifecycle: active
supplier: al-arz
case_pack: 12
moq: 240
shelf_life_days: 540
meltable: false
hazmat: none
certifications: [halal, cfia-bilingual, fda-ffr]
season_index: {ramadan: 2.8, eid: 1.6, q4: 1.2, default: 1.0}   # lunar-keyed for ramadan/eid
cost_rows:                  # time-versioned; never a scalar
  - {effective_from: 2026-06-01, po_ref: PO-2026-014, cogs: 4.90, freight: 0.85, duty: 0.32, prep: 0.40, currency: USD}
listings:
  ca:
    asin: B0C1XYZ123
    price_band: {min: 17.49, max: 21.99, currency: CAD}   # mirrored into Automate Pricing
    margin_floor_pct: 15
    safety_stock_days: 21
    lead_time_days: 63
  us:
    asin: null
    lifecycle: planned
    price_band: {min: 12.99, max: 16.99, currency: USD}
    readiness: {product_type_json: true, fda_panel: false, fsvp: false, inbound_costed: false}
freshness: {identity: 2026-09-01, economics: 2026-09-06, inventory: 2026-09-06, ads: 2026-09-06, listing: 2026-09-05, voc: 2026-09-02, competitors: 2026-09-06}
---
## Notes
## Decision history
- 2026-09-04 · PO-2026-019 approved (dec-20260904-01) · expected cover ≥21d by 2026-10-05 · outcome: pending
```

Authored fields (identity, cost rows, bands, policy, seasonality, decisions) are edited only in git through proposals. Fetched fields (inventory, prices, ads, listing status, reviews, competitors) are never stored in front matter; they go to the daily snapshot and the board.

### 5.3 The SKU Profiles board (34 columns)

| id | Title | Type | Source | Cadence | Card |
|---|---|---|---|---|---|
| name | `ANB-017 · CA` | name | git | create | ● |
| product | Product | board_relation → Products | git | create | ● |
| marketplace | Marketplace | status CA · US · WMT | git | create | ● |
| asin | ASIN | text | Listings Items | weekly | |
| class | Class | status | git | weekly | ● |
| lifecycle | Lifecycle | status | git | change | |
| next_action | Next action | status: Nothing · Watch · Reorder now · Approve price · Fix listing · Review reviews · Blocked | decision rules | daily | ● |
| owner_dept | Owner | dropdown | git | change | |
| price | Price | numbers | Listings Items offers | daily | ● |
| price_band | Band | text | git | change | |
| margin_pct | Margin % after ads | numbers | build | daily | ● |
| margin_floor | Floor % | numbers | git | change | |
| landed_cost | Landed cost | numbers | git cost rows | per PO | |
| cogs_status | COGS status | status Fresh · Estimated · Stale | build | nightly | |
| units_7d | Units/day 7d | numbers | Sales & Traffic | daily | ● |
| fba_available | FBA available | numbers | FBA Inventory | daily | ● |
| inbound | Inbound | numbers | FBA Inventory | daily | |
| cover_days | Cover days | numbers | build | daily | ● |
| reorder_point | Reorder point | numbers | build | daily | |
| next_po_eta | Next PO ETA | date | approvals | on approval | |
| oldest_expiry | Oldest expiry | date | lot record | per shipment | |
| expiry_lt90 | Units expiring <90d | numbers | build | weekly | |
| meltable | Meltable | status | git | change | |
| ad_spend_14d | Ad spend 14d | numbers | Ads | daily | |
| tacos_14d | TACoS 14d % | numbers | build (join) | daily | ● |
| top_keyword | Top keyword | text | SQP | weekly | |
| rating | Rating | numbers | Keepa / DataDoe | daily | ● |
| reviews | Reviews | numbers | Keepa / DataDoe | daily | |
| bsr | BSR | numbers | Catalog salesRanks | daily | ● |
| buybox_pct | Buy Box % | numbers | Sales & Traffic | daily | |
| listing_health | Listing health | status Live · At risk · Suppressed | Listings Items status + issues | daily | ● |
| data_health | Data health | status Fresh · Stale · Broken | integrity check | nightly | ● |
| data_asof | Data as-of | text (7 stamps) | build | nightly | |
| open_approvals | Open approvals | numbers | approvals | change | ● |
| decisions_doc | Decisions | doc (attached) | build + scoring job | on decision | ● |
| profile | Profile (git) | link | git | create | |

Subitems carry the two repeating structures: cost rows and the top-three competitor rows (ASIN, price, BSR, seen_at, from Product Pricing or Keepa only). Snapshots never become subitems.

### 5.4 Keeping it true

- **Precedence per field group.** Amazon wins on account facts; git wins on cost and policy; the build wins on derived numbers; two legal competitor sources disagreeing by more than 5% produce a flag, never an average. Three outcomes only: overwrite, flag, halt.
- **Seven freshness stamps**, one per group, with maximum ages (inventory 24h, economics 36h, ads 24h, listing 48h, competitors 48h, VOC 8 days, identity 35 days). Inventory's stamp is Amazon's own `lastUpdatedTime`.
- **`data_health`** is Fresh, Stale or Broken. A Broken record is excluded from the decision list with a stated reason. Hard Rule 8 made mechanical.
- **Nightly integrity check** (fifteen assertions, from orphan detection to `fulfillable + inbound + reserved + unfulfillable + researching == total`, price inside band, margin above floor, meltable inbound outside 1 May–30 Sep, nothing inbound with under 90 days shelf life, ad spend under the daily cap, revenue reconciles to DataDoe within 2%). Writes `state/integrity.md` and opens a request on failure.
- **History**: numbers get daily snapshot rows in git; decisions get diffs; the board gets the last value plus a stamp.

### 5.5 Rami's one-screen card

Eight numbers (Price · Margin % · Units/day · Cover days · FBA available · TACoS · Rating · BSR), three statuses (Next action · Listing health · Data health), and the last three decisions in a pinned update. Column order on the board puts Next action, Cover days and Margin % first, because mobile Details shows the first three columns by default and the rest are one "Customize" away. If the vertical list proves too loose, a Vibe item view over the same board is the reversible fix.

---

## 6. Departments: definition, coordination, scheduling, portability

### 6.1 Nine departments

| Department | Owns | Tier now | First T1 candidates |
|---|---|---|---|
| **ceo** (CEO layer + chief of staff) | strategy, key results, scorecard, decision list, work items, weekly/monthly/quarterly reviews, the librarian pass, approval hygiene, the ratchet | T0 | never; it proposes |
| **finance** | unit economics, P&L by SKU, cash, fee forensics, reimbursement reconciliation, outcome scoring, QuickBooks | T0 | none (bills in QBO after 30 clean days, T2) |
| **supply-chain** | forecast, reorder points, POs, FBA shipments, FEFO and expiry, restock limits, prep partner | T0 | monitoring with mandatory escalation; reorder-point recalculation |
| **advertising** | all campaigns, bids, budgets, negatives, placements, pacing | T0 → T1 after ratchet | bids ±15%, budgets +25% to cap, negatives above threshold, pausing zero-order targets |
| **catalog** | titles, bullets, A+, images, backend keywords, variations, listing health, US listing build | T0 | none (all publishing is T2) |
| **pricing-intel** | price bands, Automate Pricing audit, promotions, coupons, competitor watch via Keepa and SP-API pricing | T0 | none (bands are T2, prices inside bands are Amazon's) |
| **customer** | reviews, VOC, returns, buyer messages, Request-a-Review | T0 | Request-a-Review on eligible orders (template-only, one per order) |
| **account-health** | AHR, violations, IP, food and label compliance, appeals packets, monthly BSA §19 self-audit | T0 | none; all appeals are T3 |
| **expansion** | US launch workstream to Feb 2027, Walmart CA monitor-only, brand registry, IOR, FSVP, prep partners, second brand | T0 | none |

Creative work (images, video, seasonal assets) is a skill inside catalog, not a department: it has no cadence of its own and every publish is a listing change.

### 6.2 A department is a folder of text

```
departments/<dept>/
├── AGENTS.md          # charter: mission, owns, tier per action class, weekly jobs, metrics, hard rules
├── department.yaml    # machine-readable: schedule slots, harness default + fallbacks, mcp servers, state files read, budgets
├── skills/<name>/SKILL.md   # procedures with thresholds (Agent Skills format; only name+description are harness-read)
├── memory/MEMORY.md   # durable facts, ≤300 lines
├── memory/YYYY-MM-DD.md     # daily observations, append-only
└── .mcp.json          # generated from department.yaml; secrets as ${VAR}
```

`department.yaml` is the single source from which the adapters generate Claude Code's `.mcp.json`, Codex's `config.toml`, and a Grok bootstrap. Example:

```yaml
name: advertising
schedule:                       # Asia/Jerusalem
  - {slot: morning-scan, at: "07:20", prompt: prompts/exception-scan.md, timeout_min: 10}
  - {slot: daily, at: "15:50", prompt: prompts/daily.md, timeout_min: 20}
  - {slot: weekly, on: Mon, at: "16:30", prompt: prompts/weekly.md, timeout_min: 30}
harness: {default: claude-code, fallbacks: [routine, claude-code-api, codex-api]}
model: {default: sonnet, escalate_to: opus, when: [weekly, ratchet-review]}
mcp: [datadoe-read, amazon-ads-read, keepa]
reads_state: [inventory, calendar, cash, compliance]
budgets: {datadoe_tokens_per_run: 6, monday_calls_per_run: 40, resident_tokens: 20000}
tier: {bid_change: T1, budget_change: T1, negative_add: T1, campaign_create: T2, placement_modifier: T2}
```

### 6.3 The run procedure (identical on every harness)

1. `bin/run-dept.sh <dept> <slot>` acquires a per-department `flock`, pulls the department's own clone, exports credentials from the vault with `op run`, renders the MCP config, pings Healthchecks "start".
2. Loading order, fixed and budgeted at about 13k resident tokens: constitution → charter → `strategy/CURRENT.md` (this quarter's KRs) → `MEMORY.md` → `ops/OPERATING-NOTES.md` → the state files the charter names → inbox → skill metadata. Skill bodies, patterns and ledger queries load on demand.
3. Answer every inbox item first; an assignment wake outside the slot answers and stops.
4. Do the slot's job through read-only tools. Cache every export into `.exports/` (gitignored) and never re-export a day already on disk.
5. Write `state/<dept>.md` with today's date, even on failure ("tools_failed: datadoe exports_create timeout").
6. Write proposals to `approvals/pending/`, requests to other inboxes, observations to `memory/<date>.md`.
7. Commit `<dept>: <date> <slot>` and push; the wrapper pings Healthchecks "done", writes Run Health, and on non-zero exit or timeout posts one line to Telegram.

### 6.4 Coordination without a chat

- **Blackboard:** `state/<dept>.md`, overwritten each run, with a stable `## Data` table. Stale means failed.
- **Typed requests:** `requests/<dept>/inbox/<YYYYMMDD-HHMM>-<from>-<type>.md`, types enumerated in `docs/CONVENTIONS.md`, `needed-by`, `goal_id`, answer appended in place. Unanswered past `needed-by` escalates to the CEO run.
- **Work items:** `work/<id>.md` for anything that must be tracked to done rather than merely answered: a step in a project, a fix, a build, research. Opened by any department, the CEO run or Rami's form; steps, blockers and a computed priority; mirrored to the Work Items board (§4.11). A request asks a question; a work item owns an outcome.
- **Projects:** `projects/<id>.md` for multi-step work with a timeline and gates, mirrored to Projects & Milestones. The US launch is the first.
- **Locks:** `state/locks.md`, key `<scope>:<id>:<dimension>`, one change per SKU per dimension per day, expiring at the next data-day boundary. The hands runner refuses a packet whose lock another department holds, which makes the lock enforceable.
- **Precedence:** account-health beats everything; supply-chain beats advertising on stockout; finance beats supply-chain on cash; pricing beats catalog on price and catalog beats pricing on content; a blackout beats any pricing action; ties go to the earlier packet.
- **Sequencing:** departments run one at a time in fixed slots so every run reads state written earlier the same afternoon. The CEO run is last.

### 6.5 The daily calendar (Asia/Jerusalem; verify freshness on day one)

| Time | Run | Why here |
|---|---|---|
| 07:15 | account-health morning scan (AHR, violations, suppressions) | intraday data suffices; this is the P0 detector |
| 07:20 | advertising morning scan (spend pacing vs cap, runaway campaigns) | protective T1 throttle only |
| 07:30 | supply-chain morning scan (hero cover vs floor) | P0 stockout detector |
| 15:30 | nightly build for yesterday: DataDoe + Keepa + Ads exports → `state/skus/`, `ledger/kpis/`, SKU Profiles board, integrity check | after DataDoe's North-American refresh lands (about 05:00 marketplace time) |
| 15:45 | finance (scoring job first, then cash, fees, margins) | |
| 15:55 | supply-chain | |
| 16:05 | pricing-intel | |
| 16:15 | advertising | |
| 16:25 | catalog | |
| 16:35 | customer | |
| 16:45 | account-health (full) | |
| 16:55 | expansion (Mon/Wed/Fri) | |
| 17:05 | **ceo**: gates, scoring, cap, card; projection to monday; push | Rami reads in the evening |
| every 5 min | hands: poll Decisions + git, validate, execute, ledger | overnight execution lands before the next Amazon day |
| Mon 06:00 | ceo librarian pass (observations → patterns; decay sweep) | before the week's runs |
| Mon 17:05 | ceo weekly review (scorecard, KR status by R1/R2/R3, IDS issues, weekly card) | |
| 1st business day 17:30 | ceo monthly review (falsification, thrash report, KR repairs, ratchet proposals, guardrail proposals) | Rami's 30 minutes |
| Dec 15 / Mar 15 / Jun 15 / Sep 15 | ceo quarterly planning packet | Rami's 60 minutes |
| 09:00 daily | GitHub Actions watchdog: every `state/*.md` dated today or an issue + email | dead-man's switch |

### 6.6 Harnesses and moving between them

| Harness | Role | Legal basis | Adapter |
|---|---|---|---|
| Claude Code headless on Max, `launchd` | default for all nine | Anthropic compliance page (VERIFIED): unmodified binary, own subscription, one-year `setup-token` | `claude -p` with `--mcp-config` rendered from `department.yaml`, `--permission-mode` per slot, JSON output; never `--bare` |
| Claude Code Routine (cloud) | backup for the 17:05 CEO card only | allowed on Max; research preview, 1-hour floor, daily cap | committed `.mcp.json`; clones the repo |
| Claude Code on API key | overflow when a 5-hour window would starve Rami's interactive work; brand two | commercial terms | same wrapper, `ANTHROPIC_API_KEY` instead of the OAuth token |
| Codex CLI | expansion's second opinion; fallback for research-shaped work | GREY on a ChatGPT plan for unattended use (terms unreachable today); use an OpenAI API key for anything scheduled | `codex exec` with `config.toml` rendered from the same YAML; reads `AGENTS.md` natively (32 KiB cap enforced in CI) |
| Grok bots | T0 read-only pilots only | terms unreachable; a Grok Build client incident uploading repositories with secret files was reported in July 2026 | generated `runtimes/grok/BOOTSTRAP.md`; no secrets beyond a read-only DataDoe key |
| Claude Cowork | Rami's review surface, not a runner | | none |

Moving a department is one line in `department.yaml` (`harness.default`). Nothing a harness offers beyond reading files and calling MCP tools is a dependency: no subagents, no hooks, no harness memory (Claude Code auto-memory is switched off in `.claude/settings.json`), no in-harness scheduling. Exit from any model vendor is the same day: swap the credential in the wrapper.

Model choice: Sonnet-class for daily runs, Opus-class for the weekly and monthly CEO runs, the ratchet review and finance's monthly close. Cost fits inside Max 20x with margin (540–810 runs a month at 5–15 minutes each against a reported 240–480 weekly Sonnet hours). Usage credits switched on with a monthly limit so a runaway loop cannot become a surprise.

---

## 7. The CEO layer: strategy, goals, decisions

### 7.1 Objects

| Object | Count | Changes | Source of truth |
|---|---|---|---|
| Mission | 1 | ~never | `strategy/STRATEGY.md` |
| 12-month targets | 3–4 | quarterly, T3 | `strategy/TARGETS.yaml` |
| Quarterly objectives | ≤3 | quarter boundary only | `strategy/GOALS.md` |
| Key results | ≤8 total | value daily, definition never mid-quarter | `strategy/GOALS.md` + `strategy/metrics/<metric_id>.md` |
| Initiatives (bets with falsifiers) | ≤5 live | any time; killed or renewed monthly | `strategy/initiatives/<id>.md` |
| Guardrails | fixed set | T3 | `AGENTS.md` §4, referenced never copied |

Rules: metric definitions are immutable (a redefinition mints `.v2`); `current` is written only by the owning department from its state file; every objective carries `cost_of_miss_cad` and `slack_weeks` so strategic decisions can be priced against operational ones.

Initial 2026-Q4 objectives (proposed, for Rami's quarterly packet): **O1 Canada to CAD 20k/month run-rate by March 2027** (KRs: net revenue 7-day, margin after ads ≥18%, 10 SKUs activated through the readiness gate, hero cover never below 14 days); **O2 US stocked for Ramadan 2027** (KRs: 15 SKUs through the US gate, stock sellable in US FBA by 10 Jan 2027, slack days to the critical path); **O3 The company runs itself** (KRs: 30 consecutive days of fresh state files, decisions per day ≤5 with rejection rate 2–30%, at least one class ratcheted to T1).

### 7.2 Weekly scorecard

Twelve core rows plus three US-launch rows, each with owner, source and three thresholds: net revenue CA 7-day · margin after ads · cash available for POs · TACoS · SKUs with cover under 14 days · min hero cover · ad spend vs cap · wasted spend 14-day · Buy Box win % · hero conversion · listing defects · AHR/ODR · US gate SKUs ready · slack days to 10 Jan · Walmart monitor checks. Four are lagging, the rest are controllable inputs.

A cell changes status only under SPC-style rules: two consecutive weeks beyond threshold (R1), three of the last four (R2), or eight consecutive points on one side of target (R3, the drift detector). Retirement rule: a lead metric that has not moved its lag metric in 90 days is proposed for replacement; adding a row requires removing one.

### 7.3 The daily decision pipeline

`candidates → gates → score → order → cap → publish → close the loop`

Candidates: `approvals/pending/*`, CEO-generated decisions from red KRs, escalations past `needed-by`, expired items eligible for re-proposal. Gates bounce an item back to its department before scoring: evidence cited; evidence fresher than 48h (7 days for strategy); inside guardrails or explicitly labelled a breach request; a one-way door needs confidence ≥0.6 and a named falsifier; no duplicate on the same target and action type inside its cooldown; and **anything a department could have done at T1 is not a decision but a bug in the tier table** (logged; the log feeds the ratchet).

Every decision item carries: title, type (approve · choose · ratify), department, tier, action type, `goal_id`, `impact_cad` with its basis, confidence by evidence class (0.3 single observation · 0.6 trend or two sources once · 0.9 two independent sources · 1.0 deterministic), reversibility, deadline with reason, expiry, evidence lines, `if_ignored` (the first thing Rami reads), actions, the packet link, and `dry_run` diff.

### 7.4 Scoring, ordering, cap

```
score = 100 × C × (0.40·v̂ + 0.25·d̂ + 0.15·û + 0.20·r̂) × 0.9^days_open
v̂ = min(1, log10(1+|impact_cad|)/log10(5001))      # CAD 5,000 ≈ 1
d̂ = 1.0 if deadline ≤24h; 0.8 ≤48h; 0.5 ≤7d; 0.2 otherwise
û = share of impact lost per week of delay, 0–1
r̂ = 0.2 two-way | 0.6 costly | 1.0 one-way             # irreversible items deserve the minutes
C = confidence class
```

Order by score with three overrides: a deadline inside 24h floats to the top; at most two items from one department in the five; ties break on earliest expiry then higher irreversibility.

**Cap: five, hard.** Derived from a ten-minute phone read minus two minutes for the scorecard and tasks, at 90–120 seconds per honestly judged item. Three fails peak days (PO weeks, launch gates) against a 48-hour expiry and 63-day lead times; seven gets item seven rubber-stamped. Guards: a P0 lane outside the cap rate-limited to one wake per six hours; a weekly cap of 15; an automatic drop to three for a week when reversal rate exceeds 10% or re-proposal rate exceeds 20%; deferred count always shown, and if it exceeds three for three days the queue's overload becomes item one ("promote class X to T1, widen guardrail Y, or accept slower decisions"). The list may be empty and often should be. Separately, money packets are budgeted at three new and five pending per day: departments that want a sixth must withdraw one.

Expiry 48 hours; an expired item is re-proposed only with fresh data and `reproposal_of` set; at three re-proposals it becomes a monthly agenda item ("we keep asking about X"). Tasks for Rami are a separate list capped by effort (≤60 minutes visible a week) and require `why_human`, which turns the task list into a delegation roadmap.

### 7.5 Anti-thrash

Cooldowns per target and action type (bid 24h, 7 days if same direction twice; budget increase after decrease 72h; price change 14 days; listing 21 days; campaign structure 14 days; PO once per lead-time window; coupon 21 days), enforced at the gate and logged. A weekly change budget: at most 20% of active targets touched and two structural changes company-wide. Strategy freeze between reviews with four named override triggers (suspension or AHR under 200; hero stockout over 3 days; cash below one PO cycle; a policy change from Amazon or a model vendor). Mid-quarter KR repairs are diffs naming field, reason and evidence, never rewrites.

The CEO layer publishes its own six thrash metrics weekly in `state/ceo.md` (reversal rate, re-proposal rate, plan-edit count, attribution rate, override rate with a two-sided alarm at under 2% or over 30%, queue pressure) before it is allowed to publish anyone else's.

### 7.6 Cascade and escalation

Weekly, for every KR not green, and for every project milestone due inside two weeks and unstarted, the CEO opens a work item (`work/<id>.md`, mirrored to the Work Items board) for the owning department: gap, constraints, expected output, `needed-by`, computed priority. Departments derive their job list from standing duties plus open work items ordered by KR score. Every work item is answered, superseded or dropped with a reason at the next weekly run; the progress ledger tracks `is_satisfied`, `is_progress`, `is_in_loop`, and a loop escalates to the monthly review rather than re-planning. Rami's only input path is the "Ask the company" form or a `Proposed` status on the Strategy board.

Escalation lanes: **P0 wake now** (suspension, AHR under 200, hero listing takedown, hero stockout inside lead time with no PO possible, fraud or unauthorised access, payment hold, a write that failed mid-execution, a vendor notice about automated access, ad spend over 2× cap) via Telegram and monday push, one per six hours, single-source P0 permitted only for that enumerated list and labelled as unconfirmed; **P1** the daily card; **P2** the weekly card; **P3** silence in state and memory. A department that did not run is a visible line at the top of the card. Quiet must be provably quiet.

### 7.7 Meeting rhythm

| Cadence | Produces | Rami's time |
|---|---|---|
| Daily 17:05 | `briefs/<date>-decisions.md` (≤5), `briefs/<date>-tasks.md`, Decisions board, push | ≤10 min |
| Weekly Mon | `meetings/<date>-weekly.md`: 12-line card, scorecard, ≤5 IDS issues, week's decisions; Weekly Review doc | 10 min |
| Monthly | `meetings/<date>-monthly.md` + `strategy/THRASH.md`: falsification results, KR repairs, ratchet and guardrail proposals | 30 min |
| Quarterly | `strategy/quarters/<q>.md`: ≤3 objectives, ≤8 KRs, ≤5 initiatives, `cost_of_miss_cad` per objective | 60 min |

Every artifact starts with a card of at most twelve lines that can be acted on without opening a link.

---

## 8. Knowledge that compounds

### 8.1 Eight classes, one rule each

Every record format below, and every other file the company writes, is defined in `docs/record-schemas.yaml`: front matter fields, enums, computed fields, promotion gates and CI checks. That file is the schema of the knowledge layer; `docs/monday-schema.yaml` is its projection. `bin/validate-records.py` rejects a malformed file whichever harness wrote it, which is what makes harness portability enforceable rather than hoped for.

| Class | Lives in | Retrieval | Rule |
|---|---|---|---|
| Raw observations | `departments/<d>/memory/YYYY-MM-DD.md` | grep by scope and date | never edited, never loaded whole |
| Durable facts | `departments/<d>/memory/MEMORY.md` (≤300 lines) | loaded whole | single writer per fact class; `since:` and `superseded_by:` fields (Zep's bi-temporal idea, hand-rolled) |
| Patterns | `patterns/<scope>-<slug>.md` | tag filter then exact read | append-only evidence; reproducible confidence |
| Playbooks / skills | `departments/<d>/skills/*/SKILL.md`, `playbooks/` | description-matched trigger | thresholds live in skills with `evidence:`, `hit_rate:`, `review_by:` front matter |
| Decisions and outcomes | `approvals/executed/YYYY/MM/`, `ledger/outcomes.csv` | exact by id; SQL by class | every approval declares `metric`, `baseline`, `expected`, `review_on`, `design` |
| SKU histories | `state/skus/*.jsonl`, `ledger/kpis/YYYY-MM.csv`, SKU file decision history | DuckDB at query time | partitioned monthly from day one |
| Inventory lots | `suppliers/lots/<po_ref>.md` | exact by PO; FEFO derived nightly | expiry is a lot fact, never a SKU scalar |
| Strategy state | `strategy/**` + `CHANGELOG.md` | loaded as a 400-token extract | changes only at boundaries |
| Operating notes | `ops/OPERATING-NOTES.md` | loaded whole | what flakes, what formats work |

Not memory: raw exports (cached in `.exports/`, gitignored, cited by id) and harness-native memory (off everywhere; a constitution rule says no durable fact may live anywhere but the repo).

No vector database and no memory vendor in year one: six of eight classes need exact or time-series retrieval, and the two that want semantic search top out at about 150 patterns and 2,500 approvals, where a generated index plus grep beats embeddings on accuracy, cost, audit and portability (scored 36/45 for git markdown vs 30 monday, 31 DuckDB, 30 Supabase, 24 Zep, 22 Mem0, 20 Letta). Obsidian pointed at the working copy gives Rami a phone reader for free.

### 8.2 The loop

- **Daily**: departments append observations with `scope:` and `source:`.
- **Weekly (Mon 06:00, CEO as librarian)**: harvest seven days; a claim seen ≥3 times on ≥2 days from ≥2 sources becomes or reinforces a pattern (`confirmations++`); contradictions are appended, never deleted; `last_seen` over 90 days sets `decaying`, over 180 archives. Output: a diff-only commit plus ten lines in `state/ceo.md`.
- **Pattern gates**: hypothesis → supported (≥3 confirmations, ≥2 days, ≥2 sources, no unexplained contradiction) → validated (≥5 confirmations across ≥2 SKUs and ≥30 days, plus a machine-evaluable threshold written down) → skill (CEO proposes, Rami approves the diff). Confidence is a formula anyone can recompute: `confirmations / (confirmations + contradictions + 1) × recency`. A `seasonality_guard` blocks validation on Ramadan or Q4 evidence alone.
- **Daily scoring (finance, 15:45)**: for every executed approval with `review_on ≤ today`, query `ledger/kpis` for the metric on the scope over the window and on the matched control set; write a row to `ledger/outcomes.csv` (`hit · miss · inconclusive · unmeasurable`); write back to the approval, the SKU history and every playbook whose evidence produced the rule. `design:` is mandatory (`ab · prepost-matched · prepost · none`) and monthly falsification ignores plain `prepost` for promotion, because pre/post scoring during Ramadan measures Ramadan.
- **Monthly (CEO)**: realised hit rate per validated rule over ≥10 firings; demote under 60%, retire under 40%, flag under 10 firings as unexercised; cross-department contradiction grep; strategy assumptions linked to patterns are marked `challenged` and surface on the card, never silently rewritten.

### 8.3 monday's role in knowledge

Docs are a projection: `strategy/CURRENT.md`, the Weekly Review, the Patterns Digest, the Playbook Index and each SKU's decision history are published nightly with `add_content_to_doc_from_markdown` and stamped `generated_from: <commit>`. The Knowledge board (§4.11) mirrors every pattern and governed playbook with its status, confidence, contradictions and hit rate, so compounding is visible on a phone and a future seat can see what the company believes and why. Doc version history and diffs are a convenience; docs are excluded from monday's full account export, which is one more reason the repo is the record.

### 8.4 Size and what breaks first

Resident context per run about 13k tokens, hard ceiling 20k; `MEMORY.md` capped with a logged eviction rule; observations never shrink and never load; the ledger is queried, never summarised. Ranked risks at twelve months: nobody runs the weekly review (mitigated: it is a scheduled run with a state file, so a miss shows as stale); KPI CSV bloat (partitioned from day one); `approvals/executed` directory listing dumps into context (partitioned by year/month); Codex's 32 KiB `AGENTS.md` cap (CI check at 28 KiB); playbook fossilisation across markets and seasons (mandatory `scope:` and `seasonality_guard`); evidence links rot (cite ids, not paths); PII creeping into memory from buyer messages (pre-commit scan; record the pattern, never the buyer).

---

## 9. The approval and money path, end to end

### 9.1 Tiers

| Tier | Meaning | Who acts |
|---|---|---|
| T0 | observe and report; read data, write findings; no account writes | department alone |
| T1 | act inside guardrails, logged, reversible and bounded | department alone, every action in the ledger |
| T2 | propose; Rami approves; the hands runner executes | department writes the packet |
| T3 | Rami only; agents prepare the packet | Rami |

Every department starts at T0 on any new harness. Money leaving a bank account is T3 forever, with no ratchet.

| Action class | Tier | Guardrail (initial; editable in `AGENTS.md` §4) | Write path |
|---|---|---|---|
| Ad bid change | T1 after ratchet | ±15% per change; one change per target per 24h; ≥30 clicks in 14d; 25 targets a run | DataDoe `AMAZON_ADS_TARGETS_UPDATE` now; official Ads MCP when credentialed |
| Ad budget change | T1 after ratchet, **only if a budget action is verified in DataDoe** | +25% per action; total never above CAD 150/day | as above |
| Negative keyword | T1 after ratchet | ≥10 clicks, 0 orders, spend ≥2× target CPA | as above |
| Price inside an approved band | Amazon-operated | band min ≥ cost + 15% margin after ads | Automate Pricing |
| Band change or price outside band | T2 | never >20% in 24h; ≤5 SKUs per packet | DataDoe `AMAZON_LISTINGS_UPDATE` or SP-API Listings PATCH |
| Purchase order | T2 ≤ CAD 15,000/month cumulative; T3 above | cash check from finance required; hero cover floor 14d; seasonal buffer 6 weeks | packet → Rami pays manually |
| New campaign | T2 | inside the daily cap; starting budget ≤ CAD 20/day | Ads MCP |
| Listing text or images | T2 | ≤5 ASINs per packet | DataDoe / Listings API |
| FBA shipment | T2 | must match an approved PO or existing stock; async, polled to terminal state | SP-API Fulfillment Inbound v2024-03-20 |
| Coupons and deals | T2 | discount ≤20%; margin after discount ≥10%; exposure ≤ CAD 500 | DataDoe / Seller Central by Rami |
| Buyer message | T2 | Rami approves verbatim; no PII role held | Messaging API |
| Request-a-Review | T1 candidate (own carve-out) | one per eligible order; template-only; idempotent | SP-API Solicitations |
| Vine enrolment | T2 | ≤2 SKUs per quarter | Seller Central by Rami |
| Reimbursement claim | T2 | inside the 60-day window | Seller Central case by Rami, or Getida |
| Bills in QuickBooks | T2 after 30 clean days | separate credential and class from Amazon writes | Intuit QBO MCP |
| Contracts, marketplaces, appeals, IP, legal, spend over ceiling, subscriptions | T3 | | Rami |

### 9.2 The ratchet

Promotion T2 → T1 requires all of: 30 days since first proposal; ≥20 approved packets of the class; rejection rate under 5%; zero executions that failed read-back; zero policy events attributable to the class; no Rami edits to any of the last ten packets (an edited approval is a near-rejection); the CEO proposes and Rami confirms by editing one line in the department's `AGENTS.md`. Demotion T1 → T2 is automatic on any one of: a failed read-back; an action outside the numbers; any account-health or policy event; the daily ad cap breached; three consecutive runs with the class's write path failing; Rami says so. Six conditions to promote, one to demote, and no money-moving class ever promotes.

### 9.3 The path

1. **Detect** (department, read-only tools) in its slot, after reading state, locks and the calendar.
2. **Consult** if another department's fact is needed: typed request, stop, resume next slot.
3. **Dry-run** through the tool's own preview (`actions_start dryRun:true`; works even with the action type disabled) and capture the diff.
4. **Propose**: `approvals/pending/<id>.md` with schema version, idempotency key (UUIDv4, never regenerated), preconditions with `revalidate: true`, guardrail arithmetic, `marketplace` and `currency`, locks, evidence, impact, `if_ignored`, `metric`/`expected`/`review_on`/`design`, 48h expiry.
5. **Validate (machine)**: `hands/validate.py` on the five-minute timer checks schema, expiry, independently recomputed guardrails, budget remaining from the ledger (not from the packet's claim), Amazon floors, duplicate keys, the pending cap. Failures go to `approvals/rejected/` with a machine reason.
6. **Present**: the CEO run gates, scores and ranks; `bin/project-monday.py` creates or updates the Decisions item with the diff; monday push and Telegram carry the card.
7. **Decide**: Rami taps `decision` to Approved or Rejected on his phone, or edits the file directly. Two independent paths, one record; `decision_channel` says which.
8. **Sync**: the poller reads the Decisions board, moves `pending/ → approved/`, stamps `decided_by`, `decided_at`, commits, pushes.
9. **Re-validate at execution time** (the load-bearing control): the runner repeats step 5 and re-reads every precondition against live data. If cover, price, competitor state, cash or budget moved, the packet returns to pending with `supersedes` and Rami is told why. Packets over CAD 5,000 or T3 wait a 12-hour cooling period (`requires_second_check`).
10. **Lock**: `flock` on the packet's lock keys plus a machine-level lock so two runner invocations cannot overlap.
11. **Execute**: `op run` injects the write credential; one API call with the idempotency key; batches chunked per SKU with per-chunk keys so partial failure is resumable.
12. **Verify by read-back**: re-read the mutated object (listing, campaign, inbound operation status polled to terminal) and compare expected to observed.
13. **Ledger**: append a hash-chained row (`seq`, `prev_hash`, `hash`, `amount` as a decimal string, `verification`, `git_anchor` on the day's first row). Failed, partial, no-op and dry-run attempts get rows too. Chain verification runs at every runner start and refuses to proceed if broken.
14. **Close**: file to `approvals/executed/YYYY/MM/`, `ledger_ref` on the monday item, status Executed, commit and push.

**Where money leaves a bank, the path forks at step 7 and never rejoins.** For an approved PO the runner generates a payment packet: supplier legal name and the bank details Rami has on file (displayed for comparison, never auto-filled anywhere), amount and currency, PO reference, what it buys, cover impact, remaining monthly ceiling, the two prior payments to that supplier, and what changes if he does not pay. Rami pays in his bank on his device, marks the PO subitem Paid with date and reference, and finance records the bill in QuickBooks on its next run. No agent, runner or API ever touches a bank.

### 9.4 Credentials, secrets, kill switches

Three credential domains. Read-only keys (DataDoe read-scoped key, Keepa, QBO with the write/update/delete disable flags, Ads read) referenced as `${VAR}` in department `.mcp.json` and injected per run. Write credentials (DataDoe write-scoped key, Ads API, SP-API private app, QBO write) in a separate 1Password vault reachable only by the runner's `op run`. Banking nowhere. The reasoning model is structurally incapable of moving money, not merely instructed not to. If DataDoe's per-key scopes truly restrict tables and fields (UNKNOWN), tiers become credential-enforced: issue Advertising a read-only ads-and-inventory key.

Kill switches, in order of softness: disable action types in DataDoe Settings → Actions (writes stop in seconds, reads survive); `touch ops/PAUSE` in the repo from the GitHub app on Rami's phone (the runner exits at step 5 with a ledger line); unload the `launchd` jobs; revoke the DataDoe key and Ads token. The drill is rehearsed in week two.

### 9.5 Failure modes the checks catch

Stale approval (expiry plus step-9 re-validation); double execution (idempotency key sent to the API and checked against the ledger, read-back detects "already at target" and writes `noop`); partial batch (per-chunk keys and rows, packet ends `partial`, remainder re-proposed); async FBA writes that look like failures (poll to terminal, timeout is `partial` not `failed`); currency and rounding (all money as decimal strings, rounded once at the boundary, `marketplace` asserted against the credential); guardrail drift (budget recomputed from the ledger); approval fatigue (three new packets a day; bands replace prices); broken audit chain (verify at start; daily git head as external anchor); a credential in a reasoning model's context (`${NAME}` only; pre-commit secret scan; separate vault); Amazon says stop (`ops/PAUSE` and the documented order); DataDoe disappears (private SP-API app registered now); a reimbursement filed outside its window (window arithmetic in preconditions).

---

## 10. The human interface

### 10.1 Rami's day

- **Morning (optional, 30 seconds):** a Telegram line only if a P0 fired overnight or a department failed. Otherwise nothing.
- **Evening (≤10 minutes):** one monday push per ranked decision (or a single digest), opened on the Cockpit. For each: title, `if_ignored`, impact, deadline, three evidence lines, the dry-run diff, and a status to tap. Then Tasks due in three days. Then, if red, the scorecard.
- **Monday evening (10 minutes):** the weekly card in the Weekly Review doc and the scorecard.
- **First business day of the month (30 minutes):** the monthly card: falsification results, thrash report, KR repairs, ratchet and guardrail proposals, each as a Decision item.
- **Quarterly (60 minutes):** the planning packet, answered by editing the Strategy board's `proposal` status and the two numbers per objective.

Rami never creates a task. His three input gestures are: tap a status, submit the "Ask the company" form, edit a file in GitHub if monday is down.

### 10.2 The card format

Twelve lines maximum, no tables, actionable without links. Example of an evening card:

```
ANABTAWI · Sun 6 Sep · 3 decisions · 1 task · scorecard 1 red
1. APPROVE PO 480u ANB-017 · CAD 4,800 · deadline Tue 10:00 · if ignored: stockout ~15 Sep
2. APPROVE band change ANB-021 CA 14.99–17.49 → 15.49–17.99 · margin 16→19% · one-way? no
3. CHOOSE prep partner shortlist (2 of 4) · why you: contract · due Fri
TASK  read Account Health Rating in Seller Central (BSA §19) · 2 min · due Tue
RED   min hero cover 11d (ANB-017) — item 1 fixes it
deferred: 2 (1 coupon, 1 listing) · all departments ran · data fresh 15:41
```

### 10.3 Phone surfaces in monday

Cockpit dashboard (home); Decisions "Today" view; SKU Profiles "Rami — today" view and the per-SKU item with its pinned decisions update; Tasks "Due ≤3 days"; Run Health. Everything else is desktop.

### 10.4 Family seats (month three or later, one hour to enable)

Finance: a free viewer on the Finance dashboard, Scorecard and Decisions; if they reconcile payouts, a seat with "only edit assigned items" on a Finance Close board whose items are month-close checklists generated by finance. Sales: a guest on a Wholesale Pipeline board (leads, accounts, orders, samples) that the expansion department reads for a wholesale KR when that channel opens. Neither can approve money; the Decisions board's `decision` column is owner-editable only. Both boards are in the "Later" folder and cost nothing until used.

---

## 11. The tool plan and monthly cost

### 11.1 Stack

| Tool | Role | Access | Monthly (approx.) | Status |
|---|---|---|---|---|
| monday.com Work Management Pro | management surface | first-party MCP + GraphQL | already paid (grandfathered 2 seats; keep) | keep |
| Claude Max 20x | default harness for nine departments | Claude Code headless | already paid | keep |
| ChatGPT (Codex) | second opinion; expansion research | `codex exec`; API key for anything scheduled | already paid | keep |
| SuperGrok | T0 read-only pilots only | Grok bots | already paid | keep, no secrets |
| Anthropic API credits | overflow lane, brand two | API key | USD 50 budget | new |
| DataDoe | Amazon read layer, first write path, recurring exports, anomaly email | hosted MCP + REST | USD 97 | keep; connect all accounts now (735-day backfill is a wasting asset) |
| Keepa API | competitor price/BSR/review history | REST + forked 150-line MCP | €49 (~CAD 74) | new |
| Amazon SP-API private developer app | authority read/write path; exit from DataDoe | REST | 0 (fees cancelled May 2026, REPORTED) | register now |
| Amazon Ads API self-service + official Ads MCP | ads reads now, T1 writes later | MCP | 0 | apply now |
| Amazon Automate Pricing | pricing engine inside bands | Seller Central rule, managed via SP-API | 0 | adopt |
| QuickBooks Online + Intuit official MCP | books; read now, bills later | local stdio MCP | already paid; MCP 0 | adopt |
| Link My Books | settlements → QBO | hosted | USD 41 | new (A2X is 3× at this volume) |
| Getida | reimbursement recovery | success fee 25% | 0 fixed | new |
| Helium 10 Platinum | US keyword research and 10 CA activations | CSV → repo | USD 99, six months only | new, then cancel when SQP has US data |
| 1Password (or Doppler free) | vault, `op run` | CLI | 0–20 | new |
| Healthchecks.io | dead-man pings per run | API | 0 | new |
| Telegram bot | P0 and failure lines, the card | Bot API | 0 | new |
| GitHub (private repos) | knowledge layer, watchdog cron | git + Actions | 0–4 | keep |
| Walmart Global Marketplace API | monitor-only CA | REST | 0 | verify keys now (CA endpoints died 2026-07-31) |

Skipped with reasons: Pacvue, Perpetua, Intentwise, Ad Badger, m19 (10–45% of ad spend, black-box or unauditable bidding); SoStocked (USD 347 to forecast 15 winners); A2X (price); Sellerboard (no export API); Jungle Scout, DataDive (Keepa plus SQP suffice); n8n, Zapier, Make (logic outside the repo); Mem0, Letta, Zep, Supabase (no case in year one); TaxJar, Avalara (Amazon is marketplace facilitator; revisit at DTC); Scale Insights and SellerMate hosted guardrails (contingency reserve USD 100 if the in-repo ads rules slip past December).

### 11.2 Monthly cost of new tools

| | Months 1–6 | Month 7+ |
|---|---|---|
| DataDoe | USD 97 | USD 97 |
| Keepa | USD 53 | USD 53 |
| Link My Books | USD 41 | USD 41 |
| Helium 10 | USD 99 | 0 |
| API overflow budget | USD 50 | USD 50 |
| Vault, monitoring, Telegram, GitHub | ~USD 10 | ~USD 10 |
| **Total new** | **~USD 350 (~CAD 485)** | **~USD 250 (~CAD 350)** |

At CAD 8–10k revenue that is about 5% falling to 3.5%, and it does not grow with the US marketplace or brand two except for one API key. The minimal stack if only three things are bought: Keepa, Link My Books, Getida.

---

## 12. Multi-brand

The seam is Amazon mechanics versus this brand's facts.

| Shared (in `anabtawi-core`, a private plugin marketplace pinned by tag or SHA) | Per brand (its own repo) |
|---|---|
| constitution template, run procedure, conventions, tier model, approval and ledger schemas, scoring function, gates, cooldowns | `strategy/`, `products/`, `suppliers/`, `markets/`, `state/`, `ledger/`, `approvals/`, `memory/`, `patterns/` |
| department charters and skills with thresholds as formulas | threshold values fitted to the brand |
| the monday schema file (`docs/monday-schema.yaml`) and `bin/project-monday.py` | the monday workspace, board ids cache, guardrail numbers |
| DataDoe export recipes, MCP config templates | credentials (own vault), DataDoe seller connection (free on the same subscription), own Anthropic API key |

Instantiating brand two: `git init <brand>`; add the core marketplace or submodule at the pinned tag; write `strategy/`, `products/`, `suppliers/`, `markets/`; create the monday workspace by saving `Anabtawi OS` as a template or by `duplicate_board(duplicate_board_with_structure)` per board and `bin/project-monday.py --init`; connect the seller in DataDoe; register its SP-API and Ads apps (free); run all departments at T0 for a week. One afternoon of Rami's time, zero new subscriptions except an API key (about USD 200–400 a month at the same run rate, because "ordinary, individual usage" of one Max plan should not stretch to a second business). Cross-brand learning flows one way, once a month: a pattern validated in two brands is promoted into core with `scope: brand-agnostic`.

---

## 13. Build order, week by week

Nothing is built in monday until Rami approves this document. Weeks count from approval.

| Week | Build | Rami's part | Exit test |
|---|---|---|---|
| **1 Foundations** | Mac mini: `ops` user, auto-login, sleep off, `launchd` skeleton, vault, `claude setup-token`, Healthchecks, Telegram bot, Obsidian on the working copy. Repo: new layout, `department.yaml` for all nine, generated `.mcp.json`, staleness watchdog on GitHub Actions, pre-commit secret scan, ledger chain verifier. DataDoe: connect every account, check freshness at 15:00 Jerusalem, run `exports_sources_get`, confirm budget action, placement data, key scopes; keep all action types disabled. monday: create workspace, boards, columns, views, dashboards, form, automations from `docs/monday-schema.yaml`; fix the failing legacy Meta Ads recipe. | Register SP-API private developer (no PII roles) and Ads API self-service. Paste BSA §19 and Anthropic's terms into `docs/policy/`. Confirm guardrail numbers. Answer the twelve DataDoe unknowns. | every department runs once at T0 and writes a dated state file; the watchdog fires on a deliberately stale file |
| **2 Truth** | Nightly build populates SKU Profiles and Products for CA and Planned US records; integrity check live; Keepa cache started; QBO MCP read-only; Link My Books reconciling one month; scorecard computed; shadow decision list written to `briefs/` but not pushed; kill-switch drill. | Grade the shadow list against what he would have done (three evenings). Set `cost_of_miss_cad` and `slack_weeks` for the three objectives. Confirm which SKUs are meltable or hazmat and which cross Canada FOP thresholds. | integrity check passes; Rami's grading disagrees with the ranking on fewer than 2 of 5 items |
| **3 Decisions** | Daily card live at cap 3; Decisions board and poller live; hands runner executing the first real class, band changes into Automate Pricing, and DataDoe dry-run-validated ads packets at T2; approval budget 3/5; Automate Pricing rules mirrored from every SKU file. | Approve or reject on the phone. Sign the prep-partner shortlist decision. | first packet executed end to end with read-back and a chained ledger row; an expired packet re-proposed correctly |
| **4 Cascade** | Cap 5; work items cascading from red KRs; weekly review and librarian pass live; `outcomes.csv` scoring the first decisions; Getida onboarded; US listing gate checklist generating tasks; first monthly review scheduled. | Quarterly packet for 2026-Q4 (60 minutes). Confirm the FBA New Selection deadline question and the USPTO trademark status. | thirty days of consecutive fresh state begins counting |
| **5–6 US critical path** | Helium 10 keyword pass for 15 US ASINs and 10 CA activations; Listings Restrictions pre-flight per US ASIN; US label and FDA panel tasks; PO packets for the Ramadan quantity with the 8 Feb anchor; FBA Inbound v2024 prep classification set per SKU; Walmart Global API keys verified. | IOR registration, customs bond, FSVP agent, US grocery approval (T3). Approve the launch PO (T3 if above ceiling). | sailing date locked no later than late November |
| **7–8 Ratchet and hardening** | Advertising's 30-day T1 evidence reviewed; promotion proposal if the six conditions hold; DataDoe `AMAZON_ADS_TARGETS_UPDATE` enabled only then; official Ads MCP wired if credentials landed; Routine backup for the card; Solicitations carve-out proposed; external-agent registration evaluated. | Edit one line to promote, or not. | first T1 class live with the demotion rules armed |
| **Month 3** | Family seat boards; Vibe SKU card if wanted; brand-two dry run from the schema file. | | second brand instantiated in an afternoon (rehearsal) |

---

## 14. Risks, and the week-one verification list

### 14.1 Top risks

1. **DataDoe is single-sourced with no SLA.** Mitigated by recurring exports as a file drop, the anomaly email, and the private SP-API app as the exit.
2. **BSA §19 is known only through secondary sources.** Every guardrail number claiming an Amazon origin is a hypothesis until Rami pastes the text. Highest-value hour of week one.
3. **Data freshness versus the schedule.** If DataDoe's Canadian tables are not complete by 15:00 Jerusalem, the slots move; the departments already refuse to report on an incomplete day.
4. **Approval fatigue.** Users approve about 93% of prompts (Anthropic research, REPORTED). Bands, budgets, the gate and the cap exist to keep the daily count near three.
5. **Nobody runs the weekly review.** It is a scheduled run with a state file, so a miss is visible.
6. **Ads T1 is unreachable if DataDoe has no budget action and Ads API credentials stall.** Then T1 shrinks to bids, negatives and pausing, and the contingency reserve buys a hosted guardrail if needed.
7. **A vendor changes terms.** Exit from every harness and model vendor is a same-day credential swap; monday two days; DataDoe is the one that needs the registration done now.

### 14.2 Verify in week one (could not be opened from the research environment)

- Amazon: BSA §19 text; the 20%/24h and 500-ASIN floors; whether an agent registration or self-identification step exists; SP-API fee cancellation on an Amazon page; private developer approval timeline; whether the official Ads MCP accepts self-service credentials; FBA New Selection 2026 enrolment deadline and whether US ASINs must be live; 105-day and 50-day expiry rules; Canadian restock and IPI mechanics.
- DataDoe: freshness time; budget action; placement and hourly data; a real approval queue; token allowance and the USD 0 default limit; scheduled agents' model and cost; review tables; key scopes; BSA §19 self-identification in writing; Walmart date. Ban the `amazon-asin-search-auditor` skill by name.
- Anthropic: paste the Consumer Terms automation clause and the compliance page; confirm Paperclip-style launchers are inside the carve-out before any orchestrator is added. OpenAI and xAI terms for unattended plan use.
- monday: agent seat pricing and AI-credit minimums; Button column on the mobile item card; QuickBooks integration availability on Work Management (assumed unavailable; not needed); audit-log API on Pro; duplicating boards with values on this account.
- Keepa free tier (100 tokens/min claimed by a community wrapper vs no free tier reported); Getida API; SQP availability on amazon.ca; VOC report via SP-API; Healthchecks pricing.
- Business facts only Rami has: meltable and hazmat SKUs; Canada FOP threshold SKUs; measured door-to-sellable lead time from the last three shipments; Ramadan 2026 Canadian lift by SKU; USPTO status; `cost_of_miss_cad` for the US launch.

---

## Appendix A. Repository layout

```
<brand>-company/
├── AGENTS.md  CLAUDE.md (@AGENTS.md)  GEMINI.md (@AGENTS.md)
├── strategy/  STRATEGY.md TARGETS.yaml GOALS.md CURRENT.md CHANGELOG.md THRASH.md metrics/ initiatives/ quarters/ scorecard/
├── departments/<dept>/  AGENTS.md department.yaml skills/ memory/ .mcp.json
├── products/<brand>/<sku>.md   suppliers/   markets/
├── state/  <dept>.md integrity.md locks.md calendar.md skus/YYYY-MM-DD.jsonl
├── requests/<dept>/inbox|done/
├── work/<id>.md            projects/<id>.md
├── approvals/  pending/ approved/ rejected/ expired/ executed/YYYY/MM/ failed/
├── ledger/  actions.jsonl kpis/YYYY-MM.csv outcomes.csv decisions.md
├── patterns/   playbooks/   briefs/   meetings/
├── hands/  runner.py validate.py monday_sync.py ledger.py
├── bin/  run-dept.sh project-monday.py build-sku-profiles.py render-mcp.py bootstrap-grok.py
├── ops/  OPERATING-NOTES.md PAUSE (absent unless paused) launchd/*.plist
├── docs/  ANABTAWI-OS-DESIGN.md monday-schema.yaml record-schemas.yaml schemas/ policy/ research/
├── suppliers/<id>.md   suppliers/lots/<po_ref>.md
└── .github/workflows/staleness.yml  .exports/ (gitignored)
```

## Appendix B. Approval packet and ledger schemas

The normative JSON Schemas are in `docs/schemas/approval-packet.schema.json` and `docs/schemas/ledger-entry.schema.json` (drafted in research report 07 §6). Required packet fields: `id, schema_version, department, tier, action_class, status, created, expires, marketplace, currency, idempotency_key, payload, preconditions[], guardrails, evidence[], impact, if_ignored`, plus `metric, baseline, expected, review_on, design` for scoring. Required ledger fields: `seq, ts, schema_version, department, tier, action_class, runtime, target, input, output, approval_id, reason, idempotency_key, prev_hash, hash`, with `amount` always a decimal string.

## Appendix C. Research index

| # | Report | Decides |
|---|---|---|
| 01 | monday capabilities and plan tiers | Pro is right; formula/mirror trap; action budgets; agents and external agents; export |
| 02 | monday MCP verified read-only | tool inventory, column write shapes, API limits, sandbox network lock, account state |
| 03 | operator playbooks | cadence, department charters, food rules, Ramadan 2027 schedule, PPC rules, fee corridor |
| 04 | SKU profile | four-record model, hybrid location, 34-column board, integrity check |
| 05 | knowledge compounding | git spine, no vector DB, pattern and outcome schemas, loading order |
| 06 | CEO layer | strategy objects, scorecard, scoring function, cap of five, anti-thrash |
| 07 | approvals and money path | tiers, ratchet, runner, polling, packet and ledger schemas |
| 08 | DataDoe | tool surface, actions and dry-run, "approval" caveat, department coverage |
| 09 | tool layer | SP-API fee reversal, stack and cost, skips |
| 10 | harnesses and terms | Anthropic ALLOWED, others GREY, launchd + watchdog, Mac mini layout, exits |
