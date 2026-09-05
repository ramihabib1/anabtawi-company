# Anabtawi Operating System — the design

Date: 2026-09-05. Status: proposed, for Rami's approval before any restructuring of the live repo. Supersedes `docs/DECISION-CONTROL-PLANE.md` where the two disagree (section 3 says where and why). Rendered copy: https://claude.ai/code/artifact/e33797fc-8b24-4c6a-a2fc-d65b8ba45d9e (also `docs/OPERATING-SYSTEM-DESIGN.html`). Fact sheets that trace each reused claim to its survey: `docs/research/digests/`.

Inputs: the constitution and nine charters in this repo; the three-day Grok Bot pilot (state files, inbox files, memory, git log); the four surveys in `docs/research/`; the twelve surveys and the V2 and V3 designs in the anabtawi-os repo; and three Claude Code documentation pages fetched today (routines, cloud environments, GitHub Actions). Every claim below is tagged VERIFIED (primary source read), REPORTED (secondary source) or UNKNOWN. Facts reused from the earlier surveys keep their original tag; the digests that trace each one to its survey are in `docs/research/digests/`.

A note on process. This session ran unattended, so the questions I would have asked first are in section 1 with the assumption I built under. Eight web-research agents were launched twice and both times were cut off by the account's session limit before writing anything; the design therefore rests on the sixteen existing surveys, the pilot evidence, and the three pages I fetched myself. Where that leaves a gap, it says UNKNOWN and names the test that closes it.

---

## 0. The verdict in one page

The company is **Claude Code sessions over a git repository, scheduled by Claude Code Routines on your Max plan, with GitHub as the system of record and the approval mechanism, DataDoe as the read and alert layer, and a deterministic "hands" workflow that executes approved money moves with credentials no reasoning model can read.**

What that means concretely:

- **A department is a folder of text** (charter, skills, memory, `.mcp.json`). This stands. The pilot proved it: two departments produced daily, cited, correct findings and changed behaviour from inbox files without prompt edits.
- **The unit of work is a run**, not a persistent agent: a fresh Claude Code session, one prompt, one charter, one repo, then it ends. State lives in files, never in the session. Persistent agents are what stalled in the pilot; runs are what worked.
- **The scheduler is Claude Code Routines** (VERIFIED today: Pro and Max plans, cron with a one-hour minimum, fresh cloud session per fire, connectors and a committed `.mcp.json` available, pushes to `claude/` branches, counts against the subscription plus a daily run cap). No server. Nothing to babysit. The exit path is a 40-line launchd plist on the Mac mini that runs the same `claude -p` command; departments do not change.
- **Approval is a pull request merge.** A department proposes by opening a PR that moves an approval file from `pending/` to `approved/`. You read the PR body on your phone and tap Merge. Nothing else in the company can perform that merge. This gives you push notification, one-tap approval, a second confirmation dialog, expiry, an audit trail, and family visibility, with zero code and zero server.
- **Money moves only through the hands workflow**: a GitHub Actions job triggered by that merge, running a deterministic Python script (no model in the loop) that fetches the SP-API refresh token from 1Password at run time, executes exactly the payload in the approved file, appends the ledger, and moves the file to `executed/`. The reasoning model never sees a write credential. Amazon's Section 19 obligations (registered app, `Agent/` header, 12-month log, human authorization) are met by construction.
- **The goal layer is text in the repo** (`strategy/STRATEGY.md`, `strategy/GOALS.md`, a decision journal, a prediction log) and is owned by the Chief of Staff's weekly run, which scores every key result, writes the scorecard, and produces the ranked "Decisions and tasks for Rami" list. The CEO agent from the earlier decision memo is folded into this department as separate runs; two agents grading each other's work bought nothing but cost.
- **Learning compounds through five files, not a memory product**: dated observations, a pruned MEMORY.md per department, playbooks with provenance and 90-day decay, a prediction log that is scored monthly (did the PO prevent the stockout, did the price test lift margin), and a decision journal. The monthly run tries to falsify each playbook against thirty days of outcomes.
- **Paperclip is dropped.** It was a server to maintain, with weekly breaking releases and a title-only goal object, adopted to get scheduling, approvals and budgets that Routines, GitHub and the subscription already provide. The Grok Bot pilot is retired once the first Routine brief lands. Codex stays only as an optional independent reviewer of money proposals, run from the Mac mini.
- **The Mac mini is the hands and the fallback**, not the company. It holds the Codex login, the launchd fallback scheduler, and nothing that must be up for the company to run. If it is off, the company still runs.
- **A second brand is a new repo from the template, a new DataDoe organisation, new Routines, and one afternoon.** The operating system itself ships as a Claude Code plugin (skills, hooks, scripts, templates) shared by every brand repo.

Monthly cost outside launch sprints: about USD 400 to 550 on top of the subscriptions you already pay, of which DataDoe, Keepa, QuickBooks and A2X are most.

---

## 1. Questions I would have asked, and the assumptions used

| # | Question | Assumption used in this design | If the answer differs |
|---|---|---|---|
| 1 | Which account holds the Max plan the company will run on? The account this session runs in already has an unrelated Routine, whose last run was abandoned. | Rami's own Max 20x account, dedicated to the company and his own sessions. | On Max 5x, halve the daily schedule (section 10.4). |
| 2 | ChatGPT tier: Plus or Pro? | Plus. Codex is an optional reviewer, not a department brain. | On Pro, Codex can also carry two analysis departments from the Mac mini. |
| 3 | What do the two family members need: read the brief, or also decide? | Read the brief and yesterday's numbers; occasionally answer a non-money question; never approve money. | If they must approve money when Rami is away, add them as GitHub reviewers on a second approval rule (section 8.6). |
| 4 | Is the manufacturer family-owned, so a PO is an internal transfer rather than an external payment? | Treated as money either way: every PO stays T2. | No change to the design; only the cash forecast treats it differently. |
| 5 | Guardrail numbers in AGENTS.md section 4 (PO ceiling, daily ad cap, margin floor, cover floor, approval expiry). | Placeholders kept. | Edit one file. |
| 6 | Preferred phone channel: GitHub app, Slack, Telegram, email? | GitHub app for approvals, Slack for the brief, email for family. Telegram only if you want it, since it needs a script. | Section 9 lists the swap cost of each. |
| 7 | Is the private SP-API app registered, and is the Ads API credential approved? | Neither yet. Both are week-one tasks. | Skip those tasks. |
| 8 | Walmart Canada: live listings or dormant? | Set up, dormant, Q1 2027 activation. | No change until then. |
| 9 | Keep SuperGrok? | Cancel after the Routine brief replaces the Grok chat, unless you value the chat surface. | Keep it as a credential-free market-research bot only. |
| 10 | Is the current restock (shipped 2026-09-04) the whole answer to the 28 out-of-stock SKUs? | Yes for now; the first week's build is aimed at cover and the US launch calendar, not at new POs. | Supply Chain writes PO proposals in week two instead of week four. |
| 11 | Should the git history be rewritten so every commit is authored by you? Routines refuse to push to a branch carrying commits by someone else, and the pilot's commits are by the bot identity. | Yes, once, during migration (the repo is three days old). Departments then push to `claude/` branches and PRs anyway, so this only matters for state auto-merge. | Keep history and rely entirely on the PR path (section 8.3). |

---

## 2. What the evidence says

### 2.1 What the pilot proved (VERIFIED from the repo)

- Two departments on a shared cloud computer, at T0, with one read-only key, ran three days and produced: a 29-row daily cover table with velocity, cover, lost revenue (CAD 1,241 to 1,286 a day), inbound ETAs, expiry flags and five cited export ids; an account-health file that classed three suppressed parents correctly as a catalog attribute fix (T2) rather than an appeal (T3), sent a compliance hold, and found that DataDoe's real-time notification sources are disabled and the listings table was 15 to 20 percent loaded.
- Both refused to guess: lead time TBD, capacity unavailable, no PO proposal when told not to.
- Inbox corrections changed behaviour with no prompt edits. An urgent request was superseded by a normal one an hour later; the department read both, marked the first superseded, and honoured "no PO this week" in every later run.
- Failures, each with a structural cause: the first run failed on a shared clone and relative paths (fixed by Rami in the run procedure); Supply Chain filed three near-duplicate requests to a department that does not exist (fixed by "one open request per type per SKU set"); the Chief of Staff stalled on its multi-step bootstrap (six of eight bots never hired, no brief ever posted, Rami's second request unanswered past its deadline); every commit carries one shared identity.

The lesson is not that coordination fails. It is that a persistent chat bot asked to execute a multi-step checklist across days is the wrong unit of work, while a scheduled, bounded run with a fixed procedure and a state file is the right one. The design keeps everything the pilot proved and replaces the one thing that stalled.

### 2.2 What the surveys established that this design leans on

| Fact | Tag | Consequence |
|---|---|---|
| Only the unmodified `claude` binary, `codex`, and `grok` can spend the subscriptions; every open harness needs an API key; Anthropic forbids third parties routing through Max credentials. | VERIFIED (Anthropic legal page) | No orchestrator may sit between the subscription and the model. Routines and the CLI are the only legal spenders. |
| Routines: Pro/Max/Team/Enterprise; scheduled, API and GitHub triggers; one-hour minimum; run on Anthropic cloud; "no permission-mode picker and no approval prompts"; all connectors included by default; a committed `.mcp.json` is honoured; pushes to `claude/` branches always accepted; count against subscription usage plus a daily run cap; one-off runs exempt from the cap. | VERIFIED (fetched 2026-09-05) | A hosted scheduler exists on the plan you already pay for. |
| Cloud environments on Pro/Max: API credentials are attached by Anthropic's agent proxy to requests for listed hosts; "the key never reaches Claude, the commands it runs, or the session's environment variables". Environment variables are readable by anyone using the environment. GitHub credentials stay outside the VM behind a proxy. | VERIFIED (fetched 2026-09-05) | Read-only keys (DataDoe, Keepa) can be held where no model can read them. Write credentials still go to the hands workflow, not to any session. |
| GitHub Actions for Claude Code accepts "a long-lived token with your Claude subscription" as an alternative to an API key. | VERIFIED (fetched 2026-09-05) | A second hosted scheduler exists, on the same subscription, for anything that must run inside a GitHub workflow. |
| A green Routine status "does not mean the task in your prompt succeeded". | VERIFIED | The company needs its own dead-man's switch (section 10.5). |
| Managed Agents: API key only, scheduled deployments, vaults, memory stores, about USD 0.08 per session-hour plus tokens. | VERIFIED docs / REPORTED price | The graduation path if the plan's limits ever bind; not the start. |
| Paperclip: goal object has no metric, target, owner or progress; no outbound webhooks; approvals never expire; weekly releases with breaking changes and automatic migrations; a CVSS 10 remote code execution patched in April; about 2,200 open issues; reports that it performs worse than plain Claude Code. | VERIFIED repo / REPORTED press | Dropped. Section 3. |
| Amazon Section 19: registered SP-API app, `Agent/name` header, 12-month action log, human authorization for price moves over 20 percent in 24 hours and bulk edits of 500 or more, no scraped competitor data in pricing, cease on request. | REPORTED (never fetched; six independent summaries) | Every obligation is met structurally in section 8. Confirm the live text before the first write. |
| SP-API: private self-authorized app, non-restricted roles for Pricing, Listings, Inventory, Finance, Brand Analytics; developer fees cancelled May 2026; Featured Offer Expected Price batch; Automated Pricing rules with min and max via API; Listings Items JSON Patch validated against per-marketplace product type schemas. | VERIFIED changelog / REPORTED | The hands workflow covers prices, listings, inbound plans and review solicitations with first-party APIs. |
| Amazon Ads MCP: official, Amazon-hosted, open beta since February 2026, needs your own Ads API credential, sees only ad data. | VERIFIED press | Advertising's T1 write path, called directly, guardrailed by a hook. |
| DataDoe: hosted MCP with an export-job model; Actions with dry run, per-type enable and audit; COGS upsert; Skill Hub with 47 skills; scheduled agents with Slack delivery; BigQuery backfill; USD 97 flat, one seat; no FBA inbound creation, no reimbursement cases. | VERIFIED tool contract / REPORTED features | The read layer and the alert layer. Never the write path. |
| Project Vend 2: a manager agent with a stated target, a margin floor, and a forced procedure cut unauthorized discounts by 80 percent; "production-grade AI operations need layers". | REPORTED | Three layers: departments, Chief of Staff, human approval on money. |
| Anthropic multi-agent research: orchestrator plus workers, 90 percent quality gain at about 15 times the tokens; share state through files, not chat. | VERIFIED | Meetings are one run with subagents, rare; daily work is single runs over shared files. |

---

## 3. Where this overturns the control-plane decision of 2026-09-05

| Decision then | Decision now | Why |
|---|---|---|
| Paperclip on the Mac as scheduler, approvals inbox, budgets and kill switch. | Claude Code Routines as scheduler; GitHub PRs as approvals; the subscription's own limits and a hook-enforced daily ad cap as budgets; a Routine toggle plus key revocation as kill switch. | Paperclip won 7.35 to 6.65 against "bare CLI plus launchd" on a scorecard where the goal layer was ours either way, so its edge was scheduling, approvals and budgets. Routines and GitHub provide all three, hosted, on the plan, with no server. What Paperclip adds is a Postgres to back up, weekly breaking migrations, a bus factor of one, and a second approval record that has to be mirrored into the repo. The decision memo's own exit conditions (pinned release not holding 60 days; adapter issues twice a month) are, on its release evidence (patch two days after a release, 172 commits in one), likely to trigger within the first quarter. |
| A CEO agent separate from the Chief of Staff. | One Office department with three distinct runs (daily brief, weekly review, monthly review). | Fresh context per run already gives the isolation the memo wanted from two agents. Two agents means two charters, two inboxes, and an argument about who owns the decisions list. The scoring step still runs isolated per key result inside the weekly run (section 6). |
| Mac mini as the box the company runs on. | Mac mini as hands (Codex login, launchd fallback, interactive re-auth), optional for daily operation. | "Nothing I babysit, no server I maintain" is a non-negotiable. A hosted scheduler on the plan you already pay for satisfies it; a machine at home that must stay awake and signed in does not. |
| Grok Bot kept as fallback scheduler and chat surface. | Retired at first Routine brief. | It cannot run Claude or Codex, has no budgets, and its coordinator stalled. Keeping two schedulers alive is the kind of surface a solo operator should not carry. |
| Nine departments. | Eight: Customer and Account Health merge into one daily "Customer and Health" department. | Both listen and flag, both never write, both read the same DataDoe sources at the same hour. One fewer daily run and one fewer inbox; the charters keep separate sections. Everything else in the department list survived the question in section 4.2. |
| Approval channel: a Telegram bot script. | GitHub PR merge, with Slack or email as the notification mirror. | The 120-line bot was the largest piece of custom code and the one that holds a chat token. GitHub already has push notifications, buttons, a confirmation dialog, required reviewers, and an immutable log; and a merge is exactly the state transition the approval file needs. |

What stays from that memo: the repo as system of record; the goal-layer templates; the run-procedure change that names the objective each run served; the concurrency rule of one department at a time; "no API keys in the runtime"; the ratchet; the exit conditions on 5dive and Codex Goals as items to re-check.

---

## 4. Architecture

### 4.1 The picture

```
                       ┌──────────────────────────────────────────────────────────────┐
                       │                    BOARD (Rami, family)                      │
                       │  GitHub app: PRs = approvals, Issues = tasks for Rami        │
                       │  Slack / email: daily brief, alerts, questions               │
                       │  Claude Code session on the repo: "ask the company"          │
                       └───────────────▲──────────────────────────────▲───────────────┘
                                       │ brief, decisions, PRs        │ merge = approve
┌──────────────────────────────────────┴──────────────────────────────┴───────────────┐
│  SYSTEM OF RECORD: the brand repo on GitHub (text only, git history = audit)         │
│  strategy/  departments/  state/  requests/  approvals/  ledger/  products/ ...      │
└──────▲───────────────────────────▲──────────────────────────────▲───────────────────┘
       │ clone, run, push claude/* │ clone, run, push                │ on merge to main
┌──────┴──────────────┐  ┌─────────┴──────────────┐   ┌─────────────┴──────────────────┐
│ RUNS (brains)        │  │ OFFICE (Chief of Staff)│   │ HANDS (no model)               │
│ Claude Code Routines │  │ daily brief 07:00      │   │ GitHub Actions workflow         │
│ one per department   │  │ weekly review Monday   │   │ python hands.py <approval file> │
│ fresh session, 1 run │  │ monthly review 1st     │   │ secrets from 1Password at run   │
│ reads: DataDoe MCP,  │  │ scores GOALS.md, ranks │   │ SP-API private app, Agent/ hdr  │
│ Keepa, Ads MCP (T1)  │  │ decisions, expires PRs │   │ appends ledger, moves file      │
└──────┬──────────────┘  └────────────────────────┘   └────────────────────────────────┘
       │ T1 ads writes guarded by PreToolUse hook; every write logged by PostToolUse hook
┌──────┴──────────────────────────────────────────────────────────────────────────────┐
│  DATA AND EVENTS: DataDoe (reads, COGS, scheduled agents -> Slack / routine /fire)    │
│  Amazon Ads MCP (official)  Keepa API  QuickBooks MCP (read)  Freightos  web search   │
└─────────────────────────────────────────────────────────────────────────────────────┘
  FALLBACK AND EXTRAS: Mac mini with launchd running the same claude -p commands;
  Codex CLI as second-opinion reviewer of money proposals; Managed Agents if limits bind.
```

### 4.2 Six layers, each replaceable

| Layer | Choice | Beats | Exit cost |
|---|---|---|---|
| Departments | Folders of text in the brand repo: `AGENTS.md`, `skills/`, `memory/`, `.mcp.json`. Open standards (AGENTS.md, Agent Skills). | A database of agents (Paperclip, hosted platforms); a Python package (v1). | None; this is the asset. |
| Brains | Claude Code, unmodified binary, on the Max plan, invoked by Routines; Codex CLI on the Mac mini as optional reviewer. | Agent SDK (API-billed), open harnesses (API-only), Grok Build (exfiltration record). | Change one command line per department. |
| Scheduler | Claude Code Routines (hosted, on plan). | Paperclip (server, churn), launchd (machine must be up), GitHub Actions cron (works, second choice), Managed Agents (API-billed), n8n (server). | A launchd plist per department, one evening. |
| Record and approval | GitHub: repo, PRs, Issues, Actions. | Telegram bot script, Paperclip approvals, artifact inbox, Notion or Linear. | Files do not change; a new channel reads the same `approvals/` folder. |
| Hands | GitHub Actions workflow running a deterministic Python executor with 1Password secrets; SP-API private app; Amazon Ads MCP for T1. | DataDoe Actions (runs under DataDoe's app identity, no inbound or reimbursements), a Mac mini daemon (must be up), an SP-API MCP server (0 to 31 stars). | Same script runs on the Mac mini under launchd. |
| Knowledge | Markdown in the repo: strategy, playbooks, dossiers, memory, ledgers as JSONL and CSV, DuckDB for queries. | Mem0, Letta, Zep, a wiki product. | None. |

### 4.3 The rule of the company, restated

Every component is a hosted service we pay for, a first-party CLI on a subscription, a GitHub feature, or a text file in the repo. Custom code is four scripts, listed in section 8.7, under 500 lines in total, each replaceable in an afternoon. Anything beyond that is drift toward v1 and gets questioned in the Monday review.

---

## 5. Departments: definition, list, unit of work, coordination

### 5.1 What a department is

A department is a folder `departments/<name>/` containing:

- `AGENTS.md`: mandate, tier, schedule, tools, the run procedure for each of its runs, guardrails, and grading criteria. Under 150 lines.
- `skills/<skill>/SKILL.md`: procedures in the Agent Skills format (cover computation, PO proposal, negatives threshold, listing standard). Skills are the company's know-how and are shared across brands through the plugin (section 12).
- `memory/MEMORY.md` (durable, under 300 lines, each fact with `since` and `source`) and `memory/YYYY-MM-DD.md` (that day's observations, never edited later).
- `.mcp.json`: the only tools the department may use, with `${NAME}` references and no values.

It has no process, no session, and no state outside these files and `state/<name>.md`.

### 5.2 The list, and why each survived

| Department | Cadence | Tier | Why it exists as its own folder |
|---|---|---|---|
| Chief of Staff (the Office) | daily 07:00, Monday 06:00, first business day 06:00 | T0 | Holds the rhythm, the goals, the decisions list, the calendar, the escalations, the tier ratchet. Section 6. |
| Finance and Planning | Monday, monthly, on request | T2 (reimbursement claims, cost changes) | Contribution margin per SKU per marketplace is the number every other department's proposal must cite. Nobody else can own the cash forecast and the PO ceiling. |
| Supply Chain | daily 06:15, Monday, monthly | T2 (POs, inbound plans) | Proved in the pilot. The stockout problem is the company's problem today. |
| Advertising | daily 06:35, Monday | T1 hygiene, T2 structure | The one department with a bounded write class through a first-party MCP. Its guardrails are enforced in code (section 8.4). |
| Catalog and Brand | Monday, monthly | T2 (any listing change) | Listing writes are JSON patches validated against per-marketplace schemas; food attributes and bilingual labels are specialist work. |
| Pricing and Market Intel | daily 06:30, Monday | T2 (outside the band) | Buy Box, Featured Offer Expected Price, Keepa history, competitor stock. Inside the band Amazon's Automated Pricing rules act; outside it, a proposal. Kept separate from Advertising because the two must be able to disagree (a ranking push and a price cut on the same SKU is the classic conflict). |
| Customer and Health (merged) | daily 06:15 | T0, drafts only | Returns and reasons, review flags, buyer message drafts, listing issues, account status, compliance calendar, Agent Policy self-audit. Both halves listen and flag; neither writes. |
| Expansion and BizDev | Monday, monthly gates | T3 packets | The US launch is date-driven with thirteen gates; Walmart and the second brand follow the same pipeline. |

Questioned and rejected: a separate "Data" or "Analytics" department (every department pulls its own exports through one shared skill; a data department becomes a bottleneck); a "Creative" department (image and A+ briefs sit in Catalog until there is volume); a "Legal and Tax" department (T3 packets from Customer and Health plus an accountant).

### 5.3 The unit of work is a run

A run is: one Routine fire, one fresh Claude Code cloud session, one prompt ("Run the `<name>` department's `<daily|weekly|monthly|assignment>` run per `AGENTS.md` and `shared-skills/run-procedure/SKILL.md`"), one clone of the repo at `main`, work through the department's tools, one push to a `claude/<dept>/<date>` branch, one pull request (or a direct merge for state-only changes, section 8.3), then the session ends.

Why runs and not agents, skills or workflows:

- A persistent agent identity with a chat surface is what stalled in the pilot and what Vending-Bench shows melting down over long horizons: coherence failures that are uncorrelated with context size. A run cannot drift across days because it has no days.
- Skills alone are procedures; they need a caller with a mandate and a schedule. Workflows-as-code alone need a programmer for every change; the pilot showed that the changes that matter are corrections in plain text. The run is the composition: a charter (mandate) calls skills (procedure) on a schedule (workflow), with the deterministic parts pushed into scripts and hooks.
- A run is idempotent by construction: it reads today's state, and the worst case of a duplicate fire is a second identical state file and a PR that GitHub marks as no diff.

### 5.4 The run procedure, version 2

Same as the constitution's section 7 with these changes:

1. Start from a clean clone of `main` (Routines do this). No department clone directories, no `git pull --rebase`.
2. Read `AGENTS.md`, the charter, `memory/MEMORY.md`, `strategy/GOALS.md` (the current quarter's objectives), then the inbox, then the state files the charter names and `state/calendar.md`.
3. Answer inbox items first. An assignment wake (an API-trigger fire carrying `text`, or an inbox item outside the scheduled slot) means answer and stop.
4. Do the charter's work. Every account write goes through either the Ads MCP under the hook (T1) or an approval file (T2 and above).
5. Write `state/<name>.md` with today's date and, new, a `served_objectives:` list naming the `GOALS.md` objective ids the run advanced, and a `predictions:` block for any proposal (section 7.4).
6. Write `memory/<date>.md`. Update `MEMORY.md` only for durable facts.
7. Commit as the department (`git -c user.name="anabtawi/<dept>"`), push to `claude/<dept>/<date>`, open one PR titled `<dept>: <date> <run>`. State-only PRs auto-merge (section 8.3); PRs containing approval files or playbook changes wait.

### 5.5 Coordination

Three channels, in rising cost, unchanged in spirit from the constitution and now with the mechanics that the pilot showed were missing:

- **Shared state** (`state/*.md`): the blackboard. Read before proposing. The Chief of Staff rejects proposals that ignore relevant state and says so in the brief.
- **Typed requests** (`requests/<dept>/inbox/`): unchanged schema, with two rules from the pilot promoted into the run procedure: one open request per type per SKU set, updated not duplicated; and a request to a department that has not run in seven days is answered by the Chief of Staff on its behalf and flagged in the brief. Requests carry a `goal_id`.
- **Meetings**: a single Chief of Staff run that spawns one subagent per department (the Claude Code Agent tool, available in cloud sessions) to state a position from that department's files, then resolves against the constitution and writes `meetings/<date>-<name>.md`. Monday business review and monthly S&OP are scheduled; event meetings fire from the API trigger. A meeting is the only time departments "talk", and even then through a coordinator with a fixed template.

Why the coordinator will not stall this time: it never executes multi-step work across days. Bootstrap steps (creating Routines, connectors, secrets) are Rami's, listed in section 14; the Office's runs are each one bounded procedure with a state file and a hard stop. Escalation is a rule the run applies to files, not a memory it has to keep.

---

## 6. Strategy and the goal loop

### 6.1 The files

- `strategy/STRATEGY.md`: mission; north star metric and how it is computed; current posture (rewritten quarterly, proposed by the Office, edited by Rami); department mandates and what each may not decide; non-negotiables (pointer to the constitution); this quarter's one or two wildly important goals (pointer to GOALS.md); explicitly deferred items with their trigger conditions; revision log.
- `strategy/GOALS.md`: YAML front matter with quarter, north star target and baseline, one to three objectives each with key results (metric, target, baseline, current, as-of), owner department, definition of done, review cadence, status; anti-thrash lock date and override triggers; then an append-only weekly scorecard table. The template is in `docs/research/goal-patterns-report.md` section 6 and is adopted as is, with the department names of this repo.
- `strategy/decisions.md`: the decision journal. One entry per T2 or T3 decision and per plan change: date, what was decided, the evidence pointer, the predicted outcome, the review date. Replaces `ledger/decisions.md`.
- `ledger/predictions.jsonl`: one line per proposal with `id`, `metric`, `predicted`, `horizon_days`, `source`; scored by the monthly run (section 7.4).

North star for the first quarter: contribution margin after ads, CAD-normalised, CA plus US, monthly. Planning targets from the constitution become key results: CA revenue CAD 20k a month by March 2027 with ten activated SKUs; hero SKU stockout days zero; US stock live 2027-01-15.

### 6.2 The Office's three runs

**Daily brief (07:00 Asia/Jerusalem, after the department runs).** Reads every state file (any not dated today is a failed department and leads the brief), `approvals/pending/` (expires what is past `expires`, closing the PR), every inbox (lists items past `needed-by` with both positions in two lines), yesterday's numbers from DataDoe by marketplace against the seven-day average, and writes `briefs/<date>.md` in the existing brief skill's format, capped at 400 words, every number cited. Then it posts the brief to Slack and emails it to the family list through the connectors, and opens or updates GitHub Issues labelled `for-rami` for any task that is Rami's (a supplier email to send, a Seller Central check, a document to sign), each with evidence, impact, and deadline. Hard cap of five decisions a day; if there are none it says so in one line.

**Weekly review (Monday 06:00, after the Monday department runs).** Scores each key result in `GOALS.md` from state files and `ledger/kpis.csv`, one isolated subagent per key result so the grader does not see the narrative; flags only two-consecutive-week breaches; appends the scorecard row; writes the ranked "Decisions and tasks for Rami" section of `briefs/<date>-weekly.md`; runs the Monday meeting; proposes tier promotions when the ratchet's numbers are met (30 days, 20 approvals, under 5 percent rejected) by opening a PR that edits one line of the department's charter, which Rami merges or closes.

**Monthly review (first business day 06:00).** Chairs S&OP (demand to supply to cash to launch calendar); runs the falsification pass over playbooks (section 7.3); scores the prediction log (section 7.4); proposes scoped repairs to monthly milestones as a diff, never a rewrite; writes the one-paragraph posture update to `STRATEGY.md` as a PR; prunes `MEMORY.md` files over 300 lines; runs the Agent Policy self-audit over the ledger.

### 6.3 Anti-thrash rules (adopted from the survey, enforced by the Office)

Quarterly objectives are locked until the date in `GOALS.md`, changeable only at the boundary or by a named override trigger (marketplace suspension, stockout crisis on more than three hero SKUs, account deactivation). Monthly milestones change only by a scoped repair naming the line and the reason. Weekly tasks regenerate freely. A single week's breach changes nothing. Every plan change is a decision-journal entry with an evidence pointer. The Office may propose a quarterly change at any time as a PR; it may never merge one.

---

## 7. Knowledge and learning

### 7.1 Where knowledge lives

| Kind | File | Written by | Read by |
|---|---|---|---|
| Company facts | `products/<sku>.md`, `suppliers/<name>.md`, `markets/<mkt>.md` | the owning department, by PR | everyone |
| Procedures | `departments/*/skills/`, `shared-skills/` (moved into the plugin, section 12) | Rami and the Monday review, by PR | every run |
| Playbooks | `playbooks/<topic>.md`, each fact with `since`, `source`, `confidence`, `last_reinforced` | Monday review compiles; monthly review falsifies | the departments they concern |
| Department memory | `departments/<d>/memory/MEMORY.md` and dated files | the department | the department |
| Outcomes | `ledger/actions.jsonl`, `ledger/kpis.csv`, `ledger/predictions.jsonl`, `strategy/decisions.md` | hooks, Finance, the Office | the Office and Finance |
| Strategy | `strategy/` | the Office proposes, Rami merges | every run |

Nothing lives in Claude Code's auto memory: cloud sessions are fresh VMs, so any memory not in the repo does not exist. That is a feature; it forces the discipline that makes the second brand cheap.

### 7.2 The compounding loop

Daily observations (facts with sources) accumulate in dated files. The Monday review classifies the week's observations as new, reinforcing, or contradicting an existing playbook fact, and writes the diffs as part of its PR. Any playbook fact not reinforced in 90 days is marked decaying and dropped from the "active" section into an archive section; a decayed fact cited in a proposal has to be re-verified first. The monthly review takes each active playbook fact and tries to falsify it against the last thirty days of `kpis.csv` and ledger outcomes, writing the verdict as its own record. The brief's "Learned" section lists what was promoted or demoted, so Rami sees the company's beliefs change.

### 7.3 Provenance

Every durable fact carries `since`, `source` (an export id, a ledger line, an observation file), and `confidence`. The pilot's supply-chain memory already does this. It is the difference between a wiki that decays and a wiki that can be audited.

### 7.4 Getting measurably better: the prediction log

Every proposal states what it expects to happen and by when: "PO of 480 units prevents stockout through 2026-11-30; expected cover on 2026-10-15: 41 days", "bid increase on X lifts orders from 12 to 16 a week at ACOS under 28 percent". The Office scores each prediction at its horizon from the actual number and keeps a running calibration per department and per action class. This is the one mechanism that answers "is the system learning" with a number rather than a feeling, and it is also the evidence the ratchet should require: an action class earns T1 not just by approvals but by predictions that came true.

### 7.5 Retrieval

Grep over a few hundred markdown files, and DuckDB over the JSONL and CSV ledgers, until the repo outgrows them (thousands of files). No vector store, no memory vendor. The cost of adding one later is a weekend; the cost of adding one now is a dependency the second brand has to inherit.

### 7.6 Evals

A `evals/` folder of twenty to thirty golden cases: past state files with the decision Rami actually made. Quarterly, a run replays each case against the current charters and skills and reports agreement. When a charter or skill changes, the Monday review can replay the affected cases. Cheap, on-plan, and the only way to know a prompt edit did not regress a department.

---

## 8. The approval and money path, end to end

### 8.1 Tiers and the ratchet

Unchanged from the constitution: T0 observe, T1 act inside guardrails and log, T2 propose and Rami approves, T3 Rami only. The ratchet adds one condition (section 7.4): the class's predictions scored at least 70 percent within tolerance over the period. The Amazon floor (20 percent in 24 hours, 500 ASINs) is checked in the hands script, not only in the constitution.

### 8.2 A T2 proposal, step by step

1. A department run decides a proposal is warranted, checks state and inbox, sends any prerequisite request (`need-cash-check`), and writes `approvals/pending/<id>.md` with the existing front-matter schema plus `prediction:` fields and `payload:` in the exact shape the hands script executes.
2. The run pushes and opens a PR titled with the one-line proposal ("supply-chain: PO ANB-017, 480 units, CAD 6,400, ship by Sep 12"). The PR body is the proposal's "Proposal" paragraph, "Reasoning and evidence", "Projected impact", and "What happens if rejected". The PR carries labels `approval`, `t2`, `money` (if cost is non-zero), and the department.
3. GitHub notifies Rami's phone. He reads the body (twenty seconds), opens the file diff if he wants the numbers, and taps Merge. GitHub's confirm dialog is the second tap. For labels `money`, branch protection requires one approving review, so the sequence is Approve then Merge: two deliberate taps, the maker-checker the survey asked for.
4. Merging moves the file from `pending/` to `approved/` (the PR contains that rename) and sets `decided_by: rami`, `decided_at` (a tiny Actions step fills these on merge from the merger's identity, so the model cannot forge them).
5. The `hands` workflow triggers on push to `main` touching `approvals/approved/**`. It runs `scripts/hands.py <file>`: validates the front matter and payload against a schema per `action_type`, checks expiry, checks the Amazon floor, fetches the SP-API refresh token (or Ads credential) from 1Password with a service-account token held as a GitHub secret, executes the call with `User-Agent: Agent/AnabtawiOS`, writes the request and response to `ledger/actions.jsonl`, moves the file to `executed/` (or `failed/` with the error), commits as `anabtawi/hands`, and posts one line to Slack.
6. Rejection is closing the PR; the Office moves the file to `rejected/` on its next run and records the reason from the closing comment. Expiry is the Office closing PRs older than 48 hours and moving files to `expired/`; expired proposals are re-proposed with fresh data, never executed stale.

### 8.3 State changes that do not need Rami

Daily state files, memory files, inbox answers and briefs would drown Rami in PRs. Two options, pick one in week two:

- **A. Path-scoped auto-merge (recommended).** A branch rule allows auto-merge; a 30-line Actions check passes only when a PR from a `claude/` branch touches nothing outside `state/`, `departments/*/memory/`, `requests/`, `briefs/`, `meetings/`, `ledger/kpis.csv`. Anything else waits for a human. The PR still exists, so history is complete.
- **B. Direct push to `main`** for those paths, with a pre-receive check impossible on GitHub, so enforced by the run procedure only. Requires the history rewrite in section 1, question 11. Simpler, weaker.

### 8.4 T1: advertising hygiene under a hook

Advertising calls the official Ads MCP directly in its run. A `PreToolUse` hook in the repo's `.claude/settings.json` runs `scripts/guard_ads.py` on every Ads MCP write call: it parses the tool input, compares against the current bid and budget (from the day's report the run already exported), enforces plus or minus 15 percent on bids, plus 25 percent on budgets, the daily cap across campaigns, one change per target per 24 hours (from the ledger), and the blackout and stockout-risk lists in `state/`. It exits non-zero with the reason on any breach, which blocks the call. A `PostToolUse` hook appends every successful write to `ledger/actions.jsonl` with the run id. Hooks in committed settings run in cloud sessions (VERIFIED: settings files committed to the repo apply to cloud sessions). Guardrails therefore live in code, which is what the long-horizon guardrail literature and Project Vend 2 both ask for.

### 8.5 What never goes to a model

SP-API refresh token and client secret; the Ads API refresh token used by hands; the 1Password service-account token; GitHub credentials (the cloud GitHub proxy keeps them outside the VM; VERIFIED). Read-only keys (DataDoe, Keepa) are stored as cloud-environment API credentials on the Max plan so the agent proxy attaches them and "the key never reaches Claude" (VERIFIED). Whether the API-credential feature can attach DataDoe's custom `datadoe-mcp-key` header is UNKNOWN; the test is in week one, and the fallback is an environment variable with the read-only key, which a compromised run could read but which can only read data and is revoked in one click.

### 8.6 Family and delegation

Father and brother are GitHub collaborators with read access and are on the brief's email list. If Rami wants either to approve while he travels, a second branch rule requires an approving review from a named team on `money` PRs, and a merge by either counts; the ledger records who. Otherwise their surface is the brief and the ability to reply by email, which the Office reads through the Gmail connector and turns into inbox requests.

### 8.7 The only custom code

| Script | Lines | Runs where | Replaces |
|---|---|---|---|
| `scripts/hands.py` | ~250 | GitHub Actions, or launchd on the Mac mini | the Paperclip-era hands runner |
| `scripts/guard_ads.py` | ~100 | PreToolUse hook in every Advertising run | prompt-only guardrails |
| `scripts/ledger_hook.py` | ~40 | PostToolUse hook in every run | model-written ledger lines |
| `scripts/state_check.py` | ~40 | Actions cron at 07:30 | a dead-man's switch |
| `.github/workflows/*.yml` | ~120 total | GitHub | Paperclip |

Under 600 lines. No Telegram bot, no sync, no database.

### 8.8 Section 19 compliance map

| Obligation (REPORTED) | Met by |
|---|---|
| Registered SP-API app; no scraping or browser automation | Private app for writes; DataDoe and the Ads MCP for reads; web fetch only for public pages. The constitution's hard rule 1 stands. |
| `Agent/` identification | `hands.py` sets it on every call; the Ads MCP identifies itself. |
| Action log, 12 months, inputs and outputs | `ledger/actions.jsonl` in git, written by hooks and by hands, never by a model. |
| Human authorization above thresholds | Every price change is T2; `hands.py` refuses any price move over 20 percent in 24 hours and any batch over 500 regardless of approval. |
| No scraped competitor data in pricing | Pricing reads SP-API pricing data through DataDoe, and Keepa. |
| Cease on request | Kill switch: pause all Routines at claude.ai/code/routines (one toggle each), revoke the DataDoe key and the Ads credential, disable the `hands` workflow. Runbook step one. |

---

## 9. The human interface

### 9.1 Rami

- **Decisions**: the GitHub mobile app. Every T2 proposal is a PR; every T3 packet is an Issue with the packet attached. Push notification, one screen, two taps.
- **Brief**: Slack channel `#anabtawi` via the Slack connector in the Office's Routine (connectors can post to Slack as you; VERIFIED in the Routines doc). Chunked at headings under 4,000 characters. Full brief in `briefs/`.
- **Questions to the company**: open a Claude Code session on the repo (web, mobile, or `claude` in the terminal) with the DataDoe connector. This is the loop that already worked, now with the company's state, strategy and memory in the working directory. Ask "why did Supply Chain propose 480 and not 360" and it reads the proposal, the cover skill and the export.
- **Corrections**: a file in `requests/<dept>/inbox/` (from the session, or by editing on GitHub mobile) or a reply in Slack that the Office converts. The pilot proved this changes behaviour.
- **State and history**: the repo on GitHub; `state/` for today, git log for any day.

### 9.2 Family

Email. The Office sends the daily brief and, on Monday, the weekly scorecard through the Gmail connector to two addresses. They reply in plain language; the Office reads replies on its next run and files them as `info` requests with the sender named. No app to install, no login, nothing to maintain. Slack is the upgrade if they want to see the channel; GitHub read access if they want the files.

### 9.3 Alternatives beaten

| Option | Why not primary |
|---|---|
| Telegram bot with buttons | Best chat UX, but a script holding a chat token, running somewhere that must stay up. Keep as an optional add-on once the Mac mini is on; the approval files do not change. |
| Claude.ai artifact as dashboard and inbox | Artifacts can render state, but a public artifact is readable by anyone with the link and viewers' actions run through the viewer's connectors; approval state would live outside the repo. Good for a read-only dashboard later. |
| Claude in Slack (Claude Tag) | Attractive for "ask the company" from the phone, but organisation-managed and, on the docs read, tied to Team or Enterprise environments. UNKNOWN for a Max account; check in week three. |
| Notion, Linear, monday.com | A second system of record for tasks. Issues on the repo already do this and keep the audit in one place. |
| Paperclip's Decisions page | A good inbox design, on a server, with its own record to mirror. |

---

## 10. The runner and the schedule

### 10.1 Routines

One Routine per department run, on the Anthropic-hosted Default environment (Trusted network; connectors go through Anthropic's servers and need no allowlist changes), with the brand repo attached and only the connectors that department's `.mcp.json` names. Prompt: the one-line run instruction from section 5.3. Times in Asia/Jerusalem, converted by the form.

| Routine | Cron (local) | Connectors |
|---|---|---|
| customer-health daily | 06:15 daily | DataDoe |
| supply-chain daily | 06:15 daily | DataDoe, Freightos |
| pricing-intel daily | 06:30 daily | DataDoe, Keepa |
| advertising daily | 06:35 daily | Ads MCP, DataDoe |
| office brief | 07:00 daily | DataDoe, Slack, Gmail |
| finance weekly | 06:00 Monday | DataDoe, QuickBooks |
| supply-chain weekly | 06:10 Monday | DataDoe, Freightos |
| pricing weekly, advertising weekly, catalog weekly, expansion weekly | 06:15 to 06:35 Monday | as daily, plus Helium 10 during sprints |
| office weekly review and meeting | 06:45 Monday | DataDoe, Slack, Gmail |
| office monthly, finance monthly, supply monthly | first business day 06:00 | as above |
| event wake (one Routine, API trigger) | on demand | DataDoe |

Five daily runs plus the brief; about twelve on a Monday. The daily run cap's number is UNKNOWN (the docs say "see your current limits at claude.ai/code/routines"); week one reads it. If it binds, departments bundle: one "morning" Routine spawns the four daily departments as subagents in calendar order and then the brief, which costs one run and keeps fresh context per department.

### 10.2 Event-driven wakes

DataDoe scheduled agents watch for Buy Box loss, cover under floor, listing suppressed, one-star review, spend over twice baseline, account status change, and post to Slack (REPORTED capability). If DataDoe can call a webhook (UNKNOWN; test in week two), it POSTs to the event Routine's `/fire` endpoint with the alert as `text`; the Routine's prompt is written to act on the fire payload, which arrives labelled as untrusted data (VERIFIED). If it cannot, the next scheduled run reads the Slack channel through the connector. Either way no AWS queue, no server.

### 10.3 Usage and capacity

Routines "draw down subscription usage the same way interactive sessions do" (VERIFIED). The V3 estimate of 150k to 500k tokens per department run stands as the planning number, so five daily runs are roughly one to two and a half million tokens a day. Max 20x is expected to carry the daily calendar plus Rami's own sessions; the Monday morning is the peak. Week one measures real consumption at claude.ai/settings/usage and adjusts before adding departments. Anthropic's "ordinary, individual usage" clause (VERIFIED wording) is the one policy risk; Routines are an Anthropic feature designed for unattended runs on these plans, which is the strongest available signal that this pattern is intended. If usage credits are turned on, overage is metered rather than refused.

### 10.4 Fallback: the Mac mini and launchd

`runtimes/launchd/` holds one plist per Routine that runs `claude -p "<same prompt>" --permission-mode bypassPermissions --mcp-config departments/<d>/.mcp.json` in a fresh clone under the same user, with secrets injected by `op run`. Sleep disabled, auto-login, Tailscale only. Switching is: pause the Routines, load the plists. Departments, files, approvals and hands do not change. The Mac mini also hosts the Codex login for the optional reviewer (section 10.6) and is the walk-up machine for re-authentication.

### 10.5 Dead-man's switch

A GitHub Actions workflow on cron at 07:30 checks that `briefs/<today>.md` and every daily `state/*.md` are dated today; if not, it emails and posts to Slack through a webhook. Independent of Anthropic, DataDoe and the Mac mini. Free.

### 10.6 Codex as the second opinion

Optional, and only if the ChatGPT plan has room. A launchd job on the Mac mini runs `codex exec` nightly over `approvals/pending/`: for each money proposal it writes a one-paragraph independent review as a PR comment (does the arithmetic hold, is the cited export consistent with the claim, what is the strongest reason to reject). Two different model families disagreeing on a purchase order is cheap insurance, and it uses the subscription you already pay for through the unmodified `codex` binary. Codex never holds a credential beyond read access to the repo.

### 10.7 Graduation path

If the plan's limits bind for good, or if a marketplace needs runs more often than hourly, Managed Agents (API-billed, scheduled deployments, vaults) run the same department folders. That is the measured, metered ceiling; it is not the plan.

---

## 11. The DataDoe plan

| DataDoe feature | Use | Notes |
|---|---|---|
| MCP exports | Every department's reads, through `shared-skills/datadoe-export`. | The proven loop. Cite export ids. |
| COGS upsert | Finance, after every executed PO. | The one write DataDoe performs, T2 through hands or in Rami's session. |
| Scheduled agents and alerts | The event layer (section 10.2): Buy Box loss, stockout, anomaly, account status. | Delivery to Slack REPORTED; webhook UNKNOWN. |
| Skill Hub | Read the 47 skills in week two; fork the useful ones into the plugin as our own SKILL.md files with our guardrails. | Whether they are forkable text is UNKNOWN; if they are app-only, treat them as reference. |
| Actions | Disabled for every Routine. Enabled per type only in Rami's interactive session for one-off edits while the private app is being registered, dry run on, ledger line written by hand. | Writes must run under our app identity for Section 19; DataDoe cannot create inbound plans or reimbursement cases. |
| BigQuery backfill | Later, when Finance wants SQL over two years of raw data. | No build cost. |
| Memories and files plugins | Not used. Memory lives in the repo. | |
| Second brand | A second DataDoe organisation, USD 97. | Per-org key; per-brand `.mcp.json`. |

Risk of leaning on it: one hosted vendor holds the SP-API read integration and the alert layer. Mitigation: the export skill is the only place its tool names appear, Nova Analytics (read-only MCP, from USD 29) is the drop-in cross-check to trial for a month, and the private SP-API app can serve reads too if DataDoe goes away. The pilot already found one incident (orders delayed from 2026-09-01) and two coverage gaps (notification sources disabled; listings 15 to 20 percent loaded); both are week-one tickets with DataDoe support.

---

## 12. Multi-brand

The operating system becomes a Claude Code plugin in its own repository, `anabtawi-os` (reusing the name of the retired v1): `skills/` (run procedure, DataDoe export, cover, PO proposal, negatives, listing standard, brief, review, falsification), `hooks/` (guard and ledger), `scripts/` (hands, state check), `templates/` (constitution, charters, GOALS.md, product and supplier dossiers, workflows), and `agents/` (the department subagent definitions used in meetings). Brand repos install the plugin by version and hold only what is theirs: the constitution's numbers, the charters' tier lines, `products/`, `suppliers/`, `markets/`, `state/`, `memory/`, `ledger/`, `strategy/`.

Instantiating a brand: create the repo from the template, fill the constitution's targets and guardrails, connect a DataDoe organisation, register the brand's SP-API app and Ads credential in 1Password, create the Routines from the calendar, add the Slack channel and email list. One afternoon; the first week runs at T0 as the constitution requires. Isolation is by repo, by DataDoe organisation, by vault item, and by Routine; nothing is shared but the plugin. Playbooks are brand-specific by default; a fact promoted to the plugin's shared playbooks needs two brands' evidence.

---

## 13. Migration from what exists

Nothing in the live repo moves until Rami approves this document. Then, in order:

1. **Keep**: `AGENTS.md`, all charters and skills, `state/`, `requests/`, `approvals/`, `ledger/`, `products/`, `suppliers/`, `markets/`, `playbooks/`, `docs/CONVENTIONS.md`, `docs/CALENDAR.md`, the research folders.
2. **Add**: `strategy/` (three files from the templates, filled with the constitution's targets), `.github/workflows/` (hands, auto-merge check, expiry, dead-man), `.claude/settings.json` (hooks), `scripts/` (four scripts), `evals/`, `runtimes/routines/` (one file per Routine with prompt, cron, connectors) and `runtimes/launchd/` (plists), `docs/RUNBOOK.md` (kill switch, re-auth, fallback switch).
3. **Edit**: the constitution's section 7 for the run procedure v2 and section 8 for the PR channel; charters for the Customer and Health merge and the `served_objectives` line; `docs/CONVENTIONS.md` for `prediction` and `goal_id` fields; `docs/MCP-SERVERS.md` for API credentials.
4. **Retire**: `runtimes/grok-bot/` and `runtimes/paperclip/` move to `runtimes/archive/` with a one-line note each; `ledger/decisions.md` becomes `strategy/decisions.md`.
5. **Fix the pilot's leftovers**: seed `products/` from a DataDoe catalog export and mark the top ten heroes; fill `suppliers/anabtawi.md` (lead time, MOQ, case packs, terms; every cover number today assumes lead time zero); replace the 09-03 calendar line with the in-transit shipment; answer the open request to the Chief of Staff; clear the three duplicate stockout-risk requests; decide the history rewrite (question 11).
6. **Retire the Grok bots** the morning after the first Routine brief lands, and keep their chats read-only for a week as a comparison.

---

## 14. Build order, week by week

Each week ends with an exit test. Rami's time is the constraint; the estimate is his hours.

| Week | Build | Exit test | Rami hours |
|---|---|---|---|
| 1 (Sep 8) | Approve the design. Register the private SP-API app and apply for the Ads API credential. Put DataDoe and Keepa keys in 1Password and as cloud-environment API credentials; test whether the DataDoe header is attached (fallback: env var). Create `strategy/` from the templates with real targets. Create the four daily Routines and the brief Routine at T0. Read the daily run cap and usage. Seed `products/`, fill `suppliers/anabtawi.md`. Open DataDoe tickets for the disabled notification sources and the listings load. | Five consecutive automated briefs from live data, every daily state file dated, usage numbers known. | 6 to 8 |
| 2 (Sep 15) | Hooks and scripts: `guard_ads.py`, `ledger_hook.py`, `state_check.py`, the auto-merge check, the expiry job. Choose option A or B in 8.3. Slack channel and family email list live through the connectors. Test DataDoe alerts to Slack and the webhook question. Read the Skill Hub. Retire the Grok bots. | State PRs auto-merge; dead-man fires when a state file is stale; family receives the brief. | 4 to 6 |
| 3 (Sep 22) | `hands.py` for `price_change` and `listing_change` first, in dry-run mode against the private app; branch rules for `money` PRs; first T2 proposal flows end to end in dry run, then live for one listing fix (the three suppressed parents are the candidate). Mac mini arrives: auto-login, sleep off, Tailscale, `op`, both CLIs signed in, launchd plists loaded but unloaded. | First executed T2 action in the ledger with the `Agent/` header; fallback switch rehearsed once. | 6 to 8 |
| 4 (Sep 29) | Advertising to T1 under the hook once the Ads credential is approved. Weekly review Routine live with the scorecard and the ranked decisions list. First Monday meeting with subagents. Finance's first weekly P&L and cash forecast; A2X connected. `hands.py` gains `purchase_order` (a supplier email draft plus ledger) and `fba_shipment`. | A Monday pack Rami reads in 90 minutes and acts on; the first PO proposal with Freightos landed cost. | 4 to 6 |
| 5 (Oct 6) | Monthly review Routine: S&OP, falsification, prediction scoring, tier review. Prediction log populated by every proposal. `evals/` seeded with the first twenty golden cases from September's decisions. Codex reviewer job if the ChatGPT plan allows. | September close in QuickBooks; first falsification verdicts in a playbook; first tier-promotion PR opened by the Office. | 3 to 4 |
| 6 (Oct 13) | Plugin extraction: move shared skills, hooks, scripts and templates into `anabtawi-os`; the brand repo installs it. US launch program on the calendar with owners and dates; Expansion's gate list current; FDA and accountant engaged. Runbook complete. | A dry run of "instantiate brand two" from the template reaches a T0 brief in one afternoon. | 4 to 6 |

After week six the company runs on the calendar and Rami's recurring time is the brief (ten minutes), the Monday pack (ninety minutes), and the monthly S&OP (an hour).

---

## 15. Monthly cost

| Item | USD per month | Note |
|---|---|---|
| Claude Max 20x | 200 | already paid; carries the company and Rami's sessions |
| ChatGPT Plus | 20 | already paid; optional reviewer |
| SuperGrok | 0 | cancel after week two unless kept for research |
| Anthropic usage credits | 0 to 100 | only if a cap is hit and overage is enabled |
| DataDoe | 97 | read and alert layer |
| Keepa | ~55 | entry tier, EUR 49 |
| QuickBooks Online Plus | ~99 | first-party MCP |
| A2X | 29 | plus 79 for Walmart later |
| Helium 10 Diamond | 0 or 279 | launch sprints only |
| 1Password (individual or family) | ~5 | vault; service account included |
| GitHub | 0 | private repo, Actions minutes within free tier |
| Slack | 0 | free workspace |
| Mac mini | one-time 600 to 900 | plus about 2 in electricity |
| Reimbursement recovery | 25 percent of recovered | Getida or Refunds Manager |
| **Run rate** | **~305 to 405 new, ~525 to 625 all-in** | outside launch sprints; up to ~900 during a Helium 10 sprint with overage |

Against the alternatives: Paperclip's cost was the same subscriptions plus a machine that must stay up and one to three hours a month of maintenance; a full agency at the March 2027 target would be USD 2,000 to 7,000 a month.

---

## 16. The finalists against your weights

Scores 1 to 10 on the evidence above. "Goals" scores how well the option carries the text goal layer, since none has one of its own.

| Criterion (weight) | A. Routines + GitHub + hands (this design) | B. Paperclip on Mac mini (prior decision) | C. Bare CLI + launchd | D. Managed Agents | E. 5dive on a Linux box |
|---|---|---|---|---|---|
| Strategy and goals (20) | 8 | 6 | 6 | 7 | 7 |
| Decisions and tasks for Rami (20) | 9 | 7 | 5 | 7 | 8 |
| Unattended with approvals (20) | 9 | 8 | 6 | 8 | 7 |
| Subscriptions and no lock-in (15) | 8 | 9 | 10 | 3 | 9 |
| Portability and tool access (10) | 9 | 8 | 10 | 7 | 6 |
| Audit and budgets (10) | 8 | 8 | 5 | 8 | 5 |
| Maturity and maintenance (5) | 8 | 4 | 9 | 6 | 2 |
| **Weighted** | **8.50** | **7.35** | **6.95** | **6.60** | **7.10** |

Why A scores where it does: the goal layer is the same text in every option, but A is the only one where the Office's decisions arrive as native push notifications with one-tap approval and no code; unattended operation needs no machine of ours; the lock-in point (Anthropic hosts the scheduler) costs one evening of launchd plists to leave, which is the definition of "days, not the company"; audit is git plus GitHub's own logs; maintenance is re-authentication a few times a year and reading a usage page.

Where A is weakest: Routines are in research preview and their daily cap is unknown; the "ordinary individual usage" clause; the DataDoe header question. Each has a named test in week one and a fallback that keeps the departments unchanged.

---

## 17. Risks, exits, and the disagreements with the brief

Risks and their tripwires:

- Routines change or vanish: switch to launchd on the Mac mini, or GitHub Actions cron with the subscription token. Tripwire: two missed daily runs in a week not explained by usage.
- Usage cap binds: bundle departments into one morning Routine; then usage credits; then Managed Agents. Tripwire: the brief is late twice.
- Anthropic enforces the individual-usage clause: same ladder; a funded API key keeps the calendar running at metered cost. One email to Anthropic describing the use is the cheapest insurance and is a week-one task.
- DataDoe lag or outage: Nova trial as cross-check; the private app can read.
- Section 19 text differs from the reports: the hands script is where the thresholds live; edit one file.

Where I disagree with the brief, said once:

- "Subscriptions first, no lock-in" and "no server I maintain" pull against each other, and the earlier designs resolved it toward a machine at home. I resolved it toward Anthropic's hosted scheduler because the departments do not depend on it and the exit is a plist. The Mac mini still earns its place as the hands and the fallback.
- The Mac mini should not be the company's heartbeat. It should be its hands and its safety net.
- Nine departments were one too many for a CAD 10k a month brand at five-figure token budgets; Customer and Health merge. Split them again when volume justifies it.
- Grok should go. Three surfaces is two too many for one operator.

Everything else in the brief is built as asked.
