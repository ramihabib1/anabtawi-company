# Decision: what runs the company (control plane)

Date: 2026-09-05. Status: decided, with exit conditions. Inputs: the four surveys in `docs/research/` (Paperclip deep-dive, horizontal platforms, vertical Amazon platforms, goal patterns) plus the 12 earlier surveys in the anabtawi-os repo.

## The question Rami asked

"Before we lock in, compare the options for my exact use case. I want the system to handle all aspects of the business, manage goals, and create tasks for me, not the other way around."

Weights used (Rami's priorities, agreed 2026-09-05):

| Criterion | Weight |
|---|---|
| Holds strategy and goals, works toward them | 20% |
| Creates decisions and tasks for Rami (not the reverse) | 20% |
| Runs all departments unattended, money gated by approval | 20% |
| Subscription CLIs, no vendor or API-only lock-in | 15% |
| MCP tools and departments as portable text | 10% |
| Audit trail and budgets | 10% |
| Maturity and maintenance load for a solo operator | 5% |

## Verdict in one paragraph

Keep the company as text in this repo. Build the goal layer (a CEO agent, `strategy/STRATEGY.md`, `strategy/GOALS.md`, a daily ranked "Decisions and Tasks for Rami" file) in the repo, because no product surveyed has a usable goal object: Paperclip goals have no metric, deadline, owner or progress; 5dive goals are task graphs, not KPIs; every hosted product is worse. For the runner (scheduler, approvals inbox, budgets, kill switch), use Paperclip on the Mac, pinned to one version, bound to loopback or Tailscale only, with the repo as the system of record and Paperclip as replaceable plumbing. 5dive is the runner-up and the first thing to re-check in three months. The Grok Bots pilot stays only as a fallback scheduler and as a chat surface until the first Paperclip brief lands, then it is paused.

The honest caveat: Paperclip wins by a small margin and only because the goal layer is ours either way. Its own goal model scored 2/5 in the deep-dive. If it were the goal keeper it would lose.

## What has to be built regardless of the runner

Every option, including Paperclip, needs these written by us as text in this repo:

- `strategy/STRATEGY.md`: mission, north star metric, quarterly posture, department mandates and boundaries, non-negotiables, deferred items, revision log.
- `strategy/GOALS.md`: quarter, north star target and baseline, 1 to 3 objectives with key results (metric, target, baseline, current, as-of), owner department, definition of done, review cadence, anti-thrash lock date and override triggers, weekly scorecard table (append-only).
- A CEO department: reads state files and GOALS.md after the departments run, scores each key result, flags only two-consecutive-week breaches, appends the scorecard, and writes `briefs/YYYY-MM-DD-decisions.md`: a ranked list capped at five items, each with evidence pointer, expected impact, deadline, and approve/reject where money is involved. It may propose quarterly changes but never apply them outside the quarter boundary.
- A run-procedure change: every department names which objective its run served, and requests carry a `goal_id`.

Templates for all of the above are in `docs/research/goal-patterns-report.md`, section 6. The Chief of Staff stays as the operational coordinator; the CEO owns goals and the ranked list for Rami.

## Scored comparison

Scores are 1 to 10 on Rami's criteria, using the deep-dive evidence, not vendor claims. "Goals" scores how well the runner supports the text goal layer above, since none has a real one of its own.

| Criterion (weight) | Paperclip | 5dive | Bare CLI + launchd | OpenCompany | Grok Bots (pilot) |
|---|---|---|---|---|---|
| Goals and strategy (20) | 6 | 7 | 5 | 4 | 4 |
| Decisions and tasks for Rami (20) | 7 | 8 | 5 | 5 | 6 |
| Unattended with approvals (20) | 8 | 7 | 6 | 7 | 7 |
| Subscription CLIs, no lock-in (15) | 9 | 10 | 10 | 7 | 5 |
| MCP and portable text (10) | 8 | 6 | 10 | 6 | 7 |
| Audit and budgets (10) | 8 | 5 | 5 | 6 | 3 |
| Maturity and maintenance (5) | 4 | 2 | 9 | 4 | 6 |
| **Weighted** | **7.35** | **7.10** | **6.65** | **5.65** | **5.45** |

Hosted platforms (Lindy, Relevance, Dust, Zapier Agents, Notion agents, Frontier, Agentforce and 15 others) all fail the subscription and lock-in criterion outright and none has a goal object. Best of them, Relevance AI, scored 3.75 in the survey. Vertical Amazon tools (Jarvio, Atomic One, Amazon Seller Assistant) do not hold cross-department goals, cannot use Rami's subscriptions, and only Seller Assistant has a documented per-action approval gate; it is Amazon-only and not portable. They are not control-plane candidates.

## Option notes

**Paperclip (chosen, with conditions).** Verified from the repo at commit 8430bd8: org chart with CEO by convention, heartbeats with timer, assignment and automation wake reasons, Routines with cron and catch-up, issue checkout locks, three-level budgets with hard stops, formal approvals plus agent-proposed Decisions with up to eight options, triage and seven-day expiry, `claude_local` and `codex_local` adapters that inherit host subscription logins, per-company isolation for future brands, and a markdown export format designed to be runtime-independent. Real gaps: goals are title-only with no progress; no outbound webhooks, so Telegram push must be a small script of our own; export drops approval and cost history; about 2,200 open issues; weekly releases with breaking changes and automatic DB migrations; CVSS 10 remote code execution (CVE-2026-41679) in the company-import path on network-exposed instances, patched; reported coordination overhead past three or four concurrent agents. Our design runs departments in sequential calendar slots, so at most the CEO and one department run at once, which sidesteps the concurrency ceiling.

**5dive (runner-up).** MIT, no open-core, built by a solo team that runs their own company on it. Goal command turns an outcome into a guarded task graph with verification gates, org chart tracks agent-to-agent handoffs, approval questions arrive as Telegram tap-to-answer buttons, wraps Claude, Codex, Grok and other CLIs on subscriptions, SQLite, 1 GB Linux box. Why not now: 55 stars, each agent is a systemd-managed Linux user so it does not run natively on the Mac mini, no documented MCP broker (MCP still works through each CLI's own config, but nothing is documented), cost tracking is best-effort. Revisit when it runs on macOS or when a small Linux box is acceptable, and when it passes roughly 500 stars with a release cadence.

**Bare CLI plus launchd (fallback and exit path).** launchd jobs run `claude -p` or `codex exec` in each department folder, the repo is the inbox, a 30-line script pushes new approvals and the decisions file to Telegram. Highest portability and maturity, zero new dependencies. Loses on checkout locks, budgets, a decisions UI and multi-company views, all of which we would script by hand. This is what we fall back to if Paperclip breaks, and nothing in the repo changes when we do.

**OpenCompany.** Temporal durable execution and natural-language cron with 24-hour catch-up are the most production-grade scheduling found. But API keys are the primary framing, no blocking pre-spend gate is documented, and 857 stars. Watch.

**Grok Bots (current pilot).** Proved in three days that the text company works: scheduled runs, inbox corrections changing behaviour without prompt edits, real findings on stock and compliance. But it locks reasoning to xAI models, cannot run Claude or Codex on their subscriptions, has no budgets or ledger, and the Chief of Staff bot stalled on multi-step work. Keep as fallback scheduler and chat surface only.

**Claude Cowork and Amazon Seller Assistant.** Complements, not control planes. Cowork's "work in the background, leave a draft for review" is a candidate review surface on the same Claude subscription. Seller Assistant in suggest-only mode is a free second opinion on inventory and compliance; never a write path, never a source of truth.

## Conditions for running Paperclip

1. Pin one release. Upgrade deliberately, monthly at most, after reading the release notes' breaking-changes section. Never auto-update.
2. Bind to loopback or the Tailscale tailnet only. Never expose on LAN or the internet. Registration is closed after Rami's own account exists.
3. The repo is the system of record. State files, requests, approvals, ledger and briefs live in git. Paperclip holds scheduling, locks, budgets and its own approval records; a nightly export plus a copy of pending approvals into `approvals/` covers the export gap.
4. Money gate stays in the repo and the hands runner. Paperclip approvals are the UI; the hands runner only acts on an approval file in `approvals/` marked approved by Rami.
5. Concurrency of one department at a time, per `docs/CALENDAR.md`. CEO runs last.
6. No API keys in the Paperclip environment. Host logins for `claude` and `codex` only. A missing login fails the run rather than falling back to API billing.
7. Telegram push is our script, read-only: it posts new items from `briefs/` and `approvals/`. Approve and reject happen in Paperclip's UI or by editing the approval file, not in chat, until the inbound path is built and reviewed.
8. Same secrets rules as everywhere: `${NAME}` references in `.mcp.json`, values from the vault at start.

## Exit conditions and revisit dates

- Paperclip: if a pinned release cannot be held for 60 days without a security patch forcing an upgrade with breaking changes, or if open issues in adapters or approvals hit us twice in a month, move to bare CLI plus launchd. Nothing in the repo changes.
- 5dive: re-evaluate 2026-12-01 (macOS support, stars, MCP docs, release cadence).
- Codex "persistent Goals with token budgets": reported but unverified; test hands-on when the Mac mini is set up. If real, it is the first native goal object worth binding GOALS.md to.
- Whole decision: re-run this comparison at 2027-Q2, after the US launch, or earlier if Paperclip Labs changes the license.

## Next steps

1. Build the CEO layer in the repo (strategy files, CEO charter, run-procedure change, decisions format). One session.
2. Install Paperclip on the MacBook per `runtimes/paperclip/SETUP.md`, hire from `runtimes/paperclip/agents/*.json`, add the CEO agent, run one full calendar day.
3. After the first Paperclip brief lands, pause the Grok bots' schedules and keep their chats read-only.
4. Move to the Mac mini when it arrives: clone, restore Paperclip data, sign in to both CLIs, export secrets, start.
