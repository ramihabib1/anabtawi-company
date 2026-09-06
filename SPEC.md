# Anabtawi OS — Specification

What Rami reads. Three pages. Every sentence is a fact, a number or an instruction. Reasons and alternatives are in `docs/archive/DESIGN-2026-09.md`; anything there that conflicts with this file is wrong.

## 1. What this is

Nine departments, each a folder of text in this repository, read the business through MCP servers and write one thing a human sees: a monday board with at most five decisions a day for Rami to approve or reject. The repository is the company. monday displays it. Claude Code runs the departments headless on Rami's Max subscription. A separate runner with no model inside is the only process that may ever hold a write credential, and tonight it holds none.

**The company.** Anabtawi, Middle Eastern food. Amazon Canada live. Amazon US launches for Ramadan 2027, which begins about 8 February 2027; US stock must be sellable by about 10 January 2027, so the launch shipment sails by 25 November 2026 on a six-week door-to-sellable assumption (the ten-week case is the risk). Walmart Canada is monitor-only until February 2027. Rami is the only approver. Times are Asia/Jerusalem.

**Tiers.** T0 reads and proposes. T1 acts inside guardrails and logs. T2 proposes and Rami approves. T3 is Rami only. Every department is T0 today. A class moves to T1 only after thirty days, twenty approved packets, zero rejections, zero failed read-backs, zero policy events and zero edits by Rami, and only when Rami adds the class to that department's `department.yaml`. One incident demotes it. Money leaving a bank is T3 forever.

**Guardrails.** The table in `AGENTS.md` §4 is the only copy. Every number there is marked confirmed, unconfirmed (Rami's default) or reported (Amazon's rule as reported by research, to be verified against the policy text).

**Departments.** ceo · finance · supply-chain · advertising · catalog · pricing-intel · customer · account-health · expansion. Three run tonight: account-health, supply-chain, ceo. The others are added one at a time (§3).

## 2. How a day runs

**Cadence.** The only place a time is written is `docs/jobs.json`. A job names its department, trigger, files to read, MCP tools it may call, steps, files it may write, timeout, and the machine-checked conditions that mean it is done. `bin/run-job.py <id>` turns a job into one headless Claude Code call, and if the model fails or times out the wrapper writes the state file itself, so a failed run is never silent. Jobs run as a chain, one after another, never on overlapping clocks. Tonight's chain: `ops.preflight` → `account-health.daily` → `supply-chain.daily` → `ceo.daily`. The daily chain is scheduled for 15:45 once the Mac mini exists; on the MacBook it is run by hand. Data from DataDoe for yesterday's Canadian day lands about 12:00 Jerusalem; nothing is scheduled before that except by explicit exception.

**A run.** Read `AGENTS.md`, then the charter, then the inbox. Do the job's steps with the job's tools and nothing else; WebFetch, WebSearch and curl are disabled. Write `state/<dept>.md` dated today, observations to `departments/<dept>/memory/<date>.md`, proposals to `approvals/pending/`. Commit and push.

**A decision.** A department writes a packet: id, class, marketplace, currency, cost as a decimal string, evidence lines, impact, "if ignored", the metric that will judge it, the expected value, a review date and the measurement design. The CEO job ranks packets and writes `briefs/<date>-decisions.md` with at most five items, each citing a state-file line; an empty list states why. `bin/project-monday.py` mirrors the brief onto the Decisions board and department status onto Run Health. Rami taps `decision` on his phone. `hands/observe.py` polls, moves the packet to `approvals/approved/`, and writes one dry-run ledger row. Nothing executes: the runner contains no write path. Execution is added only after the two-identity test (§3, day 5) proves the tap came from Rami's monday user and not from a script.

**Rami's three gestures.** Tap a status on Decisions or Tasks. Submit the "Ask the company" form (day 4 or later). Edit a file in GitHub if monday is down.

**Notifications.** monday only: a push per Decisions item created in group Today, a push when Run Health turns Failed or Stale. If monday is not opened, nothing reaches Rami; that is the accepted cost.

**Stopping.** Create `ops/PAUSE` (committed, so it works from the GitHub app); every job exits at start. Disable action types in DataDoe. Revoke keys.

## 3. What is built when

One new capability a day, each with a test Rami can run in under a minute. Nothing is added while yesterday's capability is red.

| Day | Capability | Test |
|---|---|---|
| **0, tonight** | The loop: repo → department → packet → monday → tap → file moves. Four boards, one dashboard, three departments, the observing runner. | A packet born in the repo is Approved on the phone and the file is in `approvals/approved/` with a dry-run ledger row |
| 1 | Truth: the daily build writes `state/skus/<date>.jsonl` and the SKU Profiles board (14 columns) from DataDoe exports. Submit SP-API private-developer and Ads API self-service registrations (they take days). | Board values equal the export for three SKUs picked at random |
| 2 | The card: finance and advertising at T0; CEO scoring (impact, deadline, cost of delay, irreversibility, confidence) at cap 3. | ≤ 3 items, every one citing an export id; Rami grades them |
| 3 | It runs without Rami: watchdog reading `docs/jobs.json`, catch-up job, validator in CI. | Three consecutive days of dated state files Rami did not trigger |
| 4 | Ask the company form; Tasks for Rami written by the CEO job; the remaining four departments at T0, one charter each. | Every department has a state file dated today |
| 5 | Two-identity test: a second monday user for the machine; the poller requires the activity-log user id to be Rami's. Products and Suppliers boards; first product files. | A tap by the machine user is refused; a tap by Rami is accepted |
| Week 2 | The hands runner gains its first write path at `dryRun:true` against DataDoe; Automate Pricing bands mirrored from product files; Mac mini with launchd, vault, watchdog. | A band change approved by Rami produces a dry-run diff and no Amazon write |
| Week 3 | Knowledge: librarian pass, patterns, outcome scoring; Work Items and Projects boards with the US launch milestones. | First pattern promoted with three cited observations |
| Week 4 | First execution class enabled (band changes) after the identity test, chain verification and kill-switch drill. | One real Automate Pricing band change, read back, in the ledger |

**Open questions that change a decision** (owner, by when): DataDoe freshness hour for CA tables (Rami, day 1); whether DataDoe has a budget action and per-key scopes (Rami, day 1); BSA §19 text pasted into `docs/policy/` (Rami, day 2); Amazon Ads MCP acceptance of self-service credentials (Rami, week 2); whether monday's activity log attributes writes to the second user (day 5 test).

**Where detail lives.** Constitution `AGENTS.md`. Jobs `docs/jobs.json`. Servers `docs/mcp-servers.json`. monday `docs/monday-schema.yaml`. Record formats `docs/record-schemas.yaml`, `docs/schemas/`. Plan for tonight `docs/PLAN.md`. Audit `docs/audit/`. Research `docs/research/`. Design reasoning `docs/archive/`.
