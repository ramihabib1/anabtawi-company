# Digest: anabtawi-company research surveys, control-plane decision, and Grok Bot pilot evidence

Compiled 2026-09-05 from: `docs/research/{paperclip-deep,horizontal-platforms,vertical-platforms,goal-patterns,goal-patterns-report,README}.md`, `docs/DECISION-CONTROL-PLANE.md`, `runtimes/grok-bot/*.md`, `state/*.md`, `requests/**/*.md`, `departments/*/memory/*.md`, git log. Tags carried through from the sources: VERIFIED / REPORTED / UNKNOWN. Extraction only; no new claims.

Note from `docs/research/README.md`: two surveys (horizontal, vertical) were briefed against the OLD Supabase-based "Habib Distribution OS" design (`agent_runs`, `approval_requests`, Mem0, Hetzner CX22, `sync/scheduler.py`). Read those references as `ledger/`, `approvals/`, `state/` in this repo.

---

## 1. Paperclip (docs/research/paperclip-deep.md)

Source: shallow clone of github.com/paperclipai/paperclip at HEAD 2026-09-05, **commit 8430bd8**, plus paperclipai/paperclip-docs. Latest release tags seen: `v2026.817.0` -> `v2026.824.0` -> `v2026.831.0` -> `v2026.831.1` (patch two days later). All repo quotes VERIFIED; security/press claims REPORTED (primary fetches blocked by egress proxy).

### 1.1 Verified capabilities (object model)
- Company = isolation boundary (own goals, agents, tasks, budgets). Multiple companies per instance, switched in sidebar. VERIFIED.
- Board Operator = human owner ("the founder, the board, and the ultimate authority"). VERIFIED.
- Goal fields: `title`, `description`, `level` (company/team), `status` (planned|active|achieved|cancelled), `parentId`. **No metric, target, deadline, owner, or progress fields.** "Paperclip does not compute a numerical percentage on goals." Parent status not auto-computed from children. VERIFIED.
- Chain: `Goal -> Project -> Issue -> Execution workspace -> Agent run`. Goals link to Projects many-to-many; issues inherit goals transitively via project only. VERIFIED.
- Project: groups issues, binds to repo/cwd, own budget envelope; status backlog|planned|in_progress|completed|cancelled. VERIFIED.
- Issue (= Task): title, description, priority, status (backlog->todo->in_progress->in_review->done, plus blocked, cancelled), assignee, comments, sub-tasks. "Atomic checkout" on in_progress claims exclusive ownership. VERIFIED.
- Agents: strict single-manager org chart; CEO reports to board. VERIFIED.
- Approvals: types `hire_agent`, `approve_ceo_strategy`, budget-override, generic `request_board_approval`. States pending -> approved | rejected | revision_requested -> resubmitted -> pending. **Approvals never expire**; blocked agent waits indefinitely. VERIFIED.
- Budgets: three independent levels (company, agent monthly, project lifetime, metric `billed_cents`). 80% warning; 100% hard stop pauses agent/project. VERIFIED.
- Company Package format (`agentcompanies/v1-draft`): `COMPANY.md`, `TEAM.md`, `AGENTS.md`, `PROJECT.md`, `TASK.md`, `SKILL.md` with YAML front matter; explicitly export/portability format, not live runtime store. `TASK.md` supports `recurring: true`; cron lives in vendor extension `.paperclip.yaml` (`routines.<name>.triggers[].kind: schedule / cronExpression`). VERIFIED.

### 1.2 CEO pattern and delegation
- CEO is a convention (first agent, no manager) plus its `AGENTS.md` prompt, not a schema type. "If AGENTS.md is missing or doesn't mention delegation, the CEO won't know to break down goals and assign work." VERIFIED.
- Built-in agents subsystem (`briefs`, `learning`, hypothetical `digest`): registry-owned system utilities, provisioned without hire approval. `learning` is a one-line registry entry; maturity UNKNOWN.
- Delegation flow: set goal -> CEO heartbeat -> CEO proposes strategy (approval) -> human approves -> CEO creates tasks for reports -> reports wake by assignment -> execute -> CEO monitors/unblocks/escalates. "Nothing proceeds until you approve this." VERIFIED.
- Four wake reasons: `timer`, `assignment`, `on_demand`, `automation`. Concurrent wakeups coalesced. Fifth narrow reason `finish_successful_run_handoff` (one bounded corrective retry when a run ends without disposition, then hands to a "recovery owner"). VERIFIED.
- Guardrails: paused-assignee refusal; delegation-cycle refusal (`delegation_cycle` conflict code); "Escalation path is paused" banner. VERIFIED.
- No built-in goal-decomposition algorithm; delegation quality is 100% prompt engineering.

### 1.3 Proactive tasks/decisions for the human (three mechanisms)
1. Formal Approvals via `POST /api/companies/{companyId}/approvals`. Block downstream work. No expiry.
2. `request_confirmation` interactions (`POST /api/issues/{issueId}/interactions`): lightweight in-thread yes/no, idempotency key, `supersedeOnUserComment: true`.
3. Agent-proposed **Decisions** (`paperclip_version: v2026.824.0`, ~2 weeks old at evaluation): question + explanation + up to 8 options, each spelling out the exact side effect (comment, create issue, change status, reassign, clear blocker, cancel subtree). Required human fields, **7-day default expiry**, drift detection ("1 target changed since this was proposed"), triage (decide-by today/this week/whenever/date, snooze, named queues). Dismissal is a recorded "no". VERIFIED.
- Decisions page = unified human inbox (approvals, blocked issues, agent questions, join requests, failed runs, budget alerts). Not a scheduled push.
- Surfaces: web UI, REST API, `paperclipai` CLI (1:1 with API). Human teammates with Viewer/Operator/Admin/Owner roles.
- **No outbound webhooks.** Quote: "Paperclip does not push outbound webhooks today — the routine + agent pair *is* the push." Slack/Discord recipe = hire a notifier agent, 60s Routine, poll `GET .../approvals?status=pending` and `GET .../issues?status=blocked&priority=critical,high`, diff against a cursor stored as a comment, POST to a webhook. No Telegram guide; no inbound chat-button approve/reject anywhere. Inbound webhook triggers exist only for Routines (bearer, hmac_sha256, github_hmac). VERIFIED.

### 1.4 Heartbeat semantics
- Nine-step protocol on every wake: `GET /api/agents/me`; resolve `PAPERCLIP_APPROVAL_ID` first if set; `GET issues?assigneeAgentId=...&status=todo,in_progress,in_review,blocked`; pick work (in_progress > in_review-if-woken-by-comment > todo; `PAPERCLIP_TASK_ID` overrides; read @-mention thread first); **checkout** `POST /api/issues/{id}/checkout` with `X-Paperclip-Run-Id` and `expectedStatuses` — 409 on conflict, "Never retry a 409"; read issue+comments+ancestors; do concrete work in the same heartbeat; `PATCH /api/issues/{id}` with status + comment; delegate via child issues (`parentId` + `goalId` required). VERIFIED.
- Durable state = issue status/comments/documents in Postgres. Adapter session resume is a convenience layer only.
- Lock = issue-scoped checkout only, not a global agent lock.
- Missed ticks (machine asleep): Routine catch-up policy. Default **skip missed**; optional `enqueue_missed_with_cap`. Overlap policy default coalesce. VERIFIED.
- New agents ship with timer heartbeats **off**; recommended combination "Heartbeat on interval = off, Wake on demand = on"; recurring work belongs in **Routines** (first-class cron/webhook object that creates-and-assigns an issue). Pause (hard stop, blocks all four wake types) differs from heartbeat-off. VERIFIED.

### 1.5 Pipelines
- Only in paperclip repo (`docs/pipelines-tutorial.md`), self-labelled v1/provisional. Stage machine (`open|working|review|done|cancelled`), `autoAdvanceOnChildrenTerminal`, review stages with `approveToStageKey`/`rejectToStageKey`/`requestChangesToStageKey`/`reviewerKind: "human"`. Work items are "cases" with parent/child, `blockedByCaseKeys` (409 `blocked`), free-form JSON `fields`, optimistic `version` (409 `version_conflict`). `pipelines set-automation --stage drafting --routine <id>` binds a routine to a stage. No goal/business-ops template; example domain is content publishing. VERIFIED.

### 1.6 `claude_local` / `codex_local` adapters
- `claude_local` config: `cwd` (required), `model`, `promptTemplate` (`{{agentId}}`, `{{companyId}}`, `{{runId}}`, `{{agent.name}}`, `{{company.name}}`), `env` (secret refs), `timeoutSec`, `graceSec`, `maxTurnsPerRun` (default 300), **`dangerouslySkipPermissions` default `true`**. `bootstrapPromptTemplate` deprecated. VERIFIED.
- Session resume via `--resume`, cwd-aware (changed cwd = fresh session). Documented bug class: "poisoned `previous_message_id`" (malformed transcript JSONL -> permanent API 400); mitigation = retry once fresh, delete transcript, `clearSession: true` (tickets RED-976/RED-978). VERIFIED.
- Skills: `claude_local` symlinks into temp dir via `--add-dir`; `codex_local` symlinks into global `~/.codex/skills` (may collide, does not overwrite). VERIFIED.
- MCP config schema for these adapters: **UNKNOWN** (`docs/how-to/add-mcp-server-to-agent.md` not fully read).
- Cost tracking: subscription runs are NOT $0; distinct "subscription" biller, estimated as plan price / billing cycle length, flipped to authoritative when invoice imported. Quota-windows UI for Anthropic Pro/Max 5-hour/daily/weekly caps. VERIFIED.
- Credential ownership asymmetry in managed sandboxes: `claude_local` snapshot-owns-auth; `codex_local` host-owns-auth. VERIFIED.
- Self-acknowledged unimplemented warning in `codex-local.md` for subscription-token sharing across concurrent sandboxes. VERIFIED.

### 1.7 Multi-company and `@paperclipai/mcp-server`
- `paperclip-mcp-server` binary: thin wrapper over REST, auth by `PAPERCLIP_API_URL` + `PAPERCLIP_API_KEY` (+ optional company/agent/run ids). VERIFIED.
- Issues: full tools (`paperclipCreateIssue`, `paperclipUpdateIssue`, `paperclipCheckoutIssue`, `paperclipReleaseIssue`, `paperclipAddComment`). Goals: read-only tools (`paperclipListGoals`, `paperclipGetGoal`); create/update only via generic `paperclipApiRequest` against `POST /api/companies/{companyId}/goals` / `PATCH /api/goals/{goalId}`. Approvals fully covered, including `paperclipApprovalDecision` — the propose/decide separation depends solely on who holds the API key. VERIFIED.
- Cross-company roll-up dashboard: UNKNOWN.

### 1.8 Maturity and risk
- Release cadence VERIFIED: ~200 commits/week (Aug 29 – Sep 5, 2026 = PRs ~#12360 to ~#12875), weekly dated releases, 4-channel canary -> nightly -> beta -> stable (from `v2026.817.0`), `v2026.824.0` "carries 172 commits".
- Breaking changes every release. Examples from `v2026.824.0`: chat-style tasks default; flags `streamAgentSessionOutput`, `useSessions`, `useLogStream` removed; interaction-policy default change; managed dev runtimes loopback -> Tailscale HTTPS with new 409 codes. `v2026.831.0`: bad agent bearer tokens now 401; Grok adapter permission-mode default removed. 11–28+ automatic DB migrations per release. VERIFIED.
- Maintainer: "Paperclip Labs" appears in-product; MIT license; structured CONTRIBUTING (Greptile 5/5, Discord #dev). Legal entity UNKNOWN.
- **~2,200 open issues** (VERIFIED via GitHub UI); themes: adapter/integration, auth/env-var leakage, cascade-delete/orphaned FKs, timeouts, doc-vs-field mismatches.
- **CVE-2026-41679, CVSS 10.0 RCE** (REPORTED, ~8 outlets): unauthenticated self-registration -> self-approve CLI auth challenge -> board-level key -> company-import with malicious `process`-adapter agent executes as server. Patched in **v2026.416.0** (imports now require instance-admin / existing-company access). Architecture (config-as-executable via `process`/`http` adapters, importable `.paperclip.yaml`) gated, not eliminated.
- User complaints (REPORTED, 3 secondary sources): "performing a lot worse than just using Claude Code", "bugs and unreliable execution", coordination overhead dominates "somewhere past three to four concurrent agents".
- Export (VERIFIED, good): markdown package with agents, projects, skills, tasks + comments/documents/blocked-by, routines+triggers, attachments. **Does not travel: secret values, machine paths, DB ids, approvals, cost history, activity log.**

### 1.9 Gaps against the use case
- No Amazon/SP-API/Shopify/e-commerce adapter, skill, or built-in agent. Only generic MCP attachment, draft `external-task-protocol.md` (Linear/Jira/Asana/Notion/Trello/GitHub sync), `process`/`http` adapters. VERIFIED.
- Gap 1: chat/mobile delivery (Telegram with inline approve/reject) must be hand-built: outbound notifier + net-new inbound callback -> approval decision.
- Gap 2: typed goal schema with metric/target/deadline/owner absent; nearest typed primitive is Pipeline case `fields`.
- Gap 3: Amazon-writes executor still hand-built; Paperclip approvals can replace the approval record only.
- Gap 4: no knowledge-compounding layer (no vector memory, no fact extraction, no wiki); Skills are human-authored; `learning` built-in is a stub.
- Gap 5: coordination overhead past 3–4 concurrent agents vs 8 domains.
- Transfers cleanly: approval/decision model with revisions and drift, CEO delegation guardrails, 3-level budgets, dashboard/CLI/REST/MCP, subscription adapters with cost amortization, Routines with catch-up/concurrency policy, export format.

### 1.10 Fit scores (1–5)
| Dimension | Score |
|---|---|
| Goal management | 2 |
| Proactive task creation for the human | 3 |
| Unattended department operation | 3 |
| Subscription model backends | 4 |
| Auditability and governance | 4 |
| Multi-brand | 4 |
| Maturity risk | 2 |
| Maintenance burden | 2 |

### 1.11 Exit conditions and run conditions (from docs/DECISION-CONTROL-PLANE.md)
Conditions for running Paperclip:
1. Pin one release; upgrade deliberately, monthly at most, after reading breaking-changes; never auto-update.
2. Bind to loopback or Tailscale tailnet only; registration closed after Rami's account exists.
3. Repo is system of record; Paperclip holds scheduling, locks, budgets, its own approval records; nightly export plus copy of pending approvals into `approvals/`.
4. Money gate stays in repo + hands runner; Paperclip approvals are UI only; hands runner acts only on an approval file marked approved by Rami.
5. Concurrency of one department at a time per `docs/CALENDAR.md`; CEO runs last.
6. No API keys in Paperclip environment; host logins for `claude` and `codex` only; missing login fails the run.
7. Telegram push is our read-only script posting from `briefs/` and `approvals/`; approve/reject in Paperclip UI or by editing the file until inbound path is built and reviewed.
8. `${NAME}` references in `.mcp.json`, values from vault at start.

Exit conditions:
- **Paperclip**: if a pinned release cannot be held 60 days without a security patch forcing a breaking upgrade, or adapter/approval open issues hit us twice in a month -> move to bare CLI + launchd; nothing in the repo changes.
- **5dive**: re-evaluate 2026-12-01 (macOS support, stars, MCP docs, release cadence).
- **Codex "persistent Goals with token budgets"**: REPORTED, unverified; test hands-on when Mac mini is set up.
- **Whole decision**: re-run at 2027-Q2 after US launch, or earlier if Paperclip Labs changes the license.

---

## 2. Horizontal platforms (docs/research/horizontal-platforms.md, 2026-09-05)

Scope excluded already-evaluated: Paperclip, OpenClaw, Hermes, NanoClaw, n8n, Windmill, Temporal, LangGraph, CrewAI.

### 2.1 Scored table (survey's own, weights per brief)
| Criterion (weight) | Paperclip (placeholder, not re-researched) | Relevance AI (best hosted) | 5dive (best OSS) | Claude Code, no product |
|---|---|---|---|---|
| Goals & strategy (20%) | 8 | 3 | 7 | 2 |
| Proactive task creation for human (20%) | 8 | 4 | 8 | 3 |
| Unattended ops with approvals (20%) | 8 | 5 | 7 | 5 |
| Subscription-CLI, no API lock-in (15%) | 6 | 1 | 10 | 10 |
| MCP & portable text departments (10%) | 7 | 6 | 3 | 9 |
| Auditability & budgets (10%) | 7 | 4 | 5 | 4 |
| Maturity & maintenance (5%) | 6 | 7 | 2 | 10 |
| **Weighted total** | **7.45** | **3.75** | **6.75** | **5.60** |

Paperclip row explicitly a placeholder inferred from the operator's framing.

### 2.2 Decision memo's rescored table (docs/DECISION-CONTROL-PLANE.md, deep-dive evidence, Rami's weights agreed 2026-09-05)
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

Memo caveat: "Paperclip wins by a small margin and only because the goal layer is ours either way. Its own goal model scored 2/5 in the deep-dive. If it were the goal keeper it would lose."

### 2.3 Hosted platforms (20) — all disqualified: none runs on Claude Code / Codex subscription; all bill own credits/seats/API
| Product | Why it lost (per survey) |
|---|---|
| Lindy | Flat list of bots, no org chart/OKR; routines exist; pause-and-ask is task-level gating; per-seat $49.99–199.99/mo (REPORTED); no self-host; high lock-in |
| **Relevance AI** (closest hosted) | "Workforce" of named coworker roles + MCP + 2,000 integrations (REPORTED); no OKR/strategy object; no confirmed enforced pre-spend gate; Vendor Credits $234–349/mo Team (REPORTED); no self-host |
| Beam AI | Enterprise process automation, ~$299/mo (REPORTED, low confidence); claims on-prem (unverified); no goals, no MCP evidence |
| Sintra | 12 fixed "AI Helpers", $39–97/mo; revenue target is a marketing input not a tracked goal; no MCP/self-host |
| Artisan (Ava) | Single-purpose AI BDR; opaque sales-gated pricing $280–3,000/mo; no goals/MCP/self-host |
| Dust | "OS for AI agents", native MCP, credit-metered ($0/30/150 per mo); self-host option REPORTED via one aggregator, unverified; knowledge-assistant model, not goals/org chart; $40M Series B May 2026 |
| Motion | Personal AI project manager/auto-scheduler; reschedules existing tasks, does not originate them; no MCP/self-host/money gate |
| Wordware | Agent IDE; inconsistent pricing; no goals/org |
| Gumloop | No-code workflow builder; MCP **server** on Pro (inverse direction); no self-host; no goals |
| Zapier Agents/Central | 9,000+ apps; approvals are user-built patterns not enforced objects; no goals/self-host/subscription |
| Make.com AI Agents (Maia) | Open beta Feb 2, 2026; BYO API key (still API billing); no goals/MCP-client/self-host |
| Notion Custom Agents | Shipped Feb 24, 2026 (VERIFIED); scheduled/event-triggered, MCP-connected; 2,800 internal agents (self-report); no goal object, no money gate, no subscription-CLI. Most transferable pattern |
| Asana AI Teammates | Workflow Optimizer flags stalls and builds automations (REPORTED); operates inside Asana graph only; Goals feature static |
| monday.com | "AI Work Platform"/"digital workforce" (IR marketing); MCP server + agent tools VERIFIED by tool presence in session; goals depth untested |
| Linear Agent | Public beta March 2026 (VERIFIED); real proactive issue creation; software-scoped; no money gate |
| Airtable | UNKNOWN, not pursued |
| Salesforce Agentforce | RBAC inheritance, MCP bundled Enterprise+ (VERIFIED); ~$0.10/action Flex Credits (REPORTED); CRM-native, massive lock-in |
| Microsoft Agent 365 / Copilot | GA May 1, 2026 (VERIFIED); A2A GA Aug 2026 (VERIFIED); governance control plane, M365-centric, no subscription-CLI |
| Google Gemini Enterprise Agent Platform | Rebranded Agentspace at Cloud Next 2026; $9/25/45 per user tiers (REPORTED); $0.085/vCPU-hr (VERIFIED); GCP lock-in |
| OpenAI Frontier | Launched Feb 5, 2026 (VERIFIED TechCrunch/CNBC); "open platform" managing agents "like employees"; OpenAI enterprise billing = second vendor |
| Amazon Bedrock AgentCore | 12 billable components, $0.0895/vCPU-hr (VERIFIED); Gateway is an MCP broker; substrate, not a company product; AWS lock-in |

### 2.4 Open source — three near-matches, mature ecosystem lacks the company layer
- **5dive** (github.com/5dive-ai/5dive, VERIFIED): "Run a company of AI agents on a server you own." `5dive goal add` -> guarded task graph with dependencies and verification gates; `5dive org set`; `5dive task need DIVE-42 --type=approval --ask=... --options=ship|hold` -> Telegram tap-to-answer; recurring templates `--recurring="0 7 * * *"`; `5dive heartbeat on ops --every=30m`; wraps Claude, Codex, Antigravity, Grok, Devin, Hermes, OpenClaw, OpenCode, Pi as systemd-managed Linux users; installer expects "your own agent-CLI subscription or API key (Claude Pro/Max, OpenAI, etc.)"; Ubuntu 22.04+, root install, SQLite, 1 GB VM; MIT, "no open-core"; `5dive run ls|show|events|logs|retry|metrics`, `5dive trace`, `5dive account usage`; cost "best-effort". Gaps: no documented MCP broker (UNKNOWN), cost precision. **55 stars**, ~1,889 commits, "we run our own company on this"; companion `5dive-plugins` with Telegram bridge. Decision memo adds: each agent is a systemd Linux user so does not run natively on the Mac mini.
- **OpenGoat** (github.com/marian2js/opengoat, VERIFIED): `opengoat agent create 'CTO' --manager --reports-to goat`; tasks are agent-to-agent delegation; no human approval surface, no money gate, no goal object, no MCP, no scheduling documented; Node >= 20.11, Docker; MIT, 427 stars.
- **OpenCompany** (github.com/zeenie-ai/OpenCompany, VERIFIED): orchestrator + durable Task Manager (3 concurrent descendants); 77 skills across 19 folders; Stripe node with spend tracking but no documented blocking pre-spend gate; natural-language cron with 24-hour catch-up; Claude Code CLI and Codex CLI as backends; Temporal durable execution; framing "Bring your own API keys, or run models locally"; MIT, 857 stars, ~1,220 commits, self-described "production-ready".
- Clawe: Kanban for OpenClaw agents (Next.js 16 + Convex); coordination tooling only.
- MetaGPT/ChatDev/CAMEL: 2023 research artifacts; MetaGPT pivoted to hosted MGX; "teams of agents did not get automatically smarter than one good agent" (REPORTED).
- Agency Swarm: org-role framework but OpenAI Agents SDK/Responses API coupled.
- AutoGPT Platform: Platform components under **Polyform Shield** (source-available, not OSI); classic parts MIT; no company abstraction.
- SuperAGI: stalled, unaddressed security debt (REPORTED); excluded.
- Letta/MemGPT: memory substrate only; LettaBot archived May 2026 into Letta Code; Pro $20/mo.
- Agno/AgentOS: 41,000+ stars, native MCP + A2A, framework+runtime+control plane; no goals/org/approval; API-direct.
- Mastra: TypeScript, bidirectional MCP; no goals/org/approval.
- CrewAI AMP/Factory: $60–120K/yr estimates; self-host needs DevOps team (REPORTED); stick to OSS core.
- LangGraph Platform: Plus $39/user/mo needs LangSmith Plus; self-host on Enterprise; no new company abstraction.
- Dify: 149,000+ stars, 1.15.0 (Jun 25, 2026), bidirectional MCP H1 2026; no goals/org/approval; API-key model calls.
- Activepieces: MIT, 400+ integrations each an MCP server; no company abstraction.
- Flowise: code freeze Jul 29, 2026, archived Aug 10, support ends Aug 31, 2026 (Workday acquisition); excluded.
- Prefect acquired Dagster (Jul 13, 2026) + FastMCP; Kestra "deterministic workflows and autonomous agents side by side"; execution engines, no company layer.

### 2.5 Claude Code / Codex as bare orchestrator
- Claude Code scheduling: `/loop` (in-session, min 1 minute, **expires after 3 days**, VERIFIED); Desktop local Routines (fire only with app open, machine awake, VERIFIED); **Cloud Routines** (shipped April 14, 2026, research preview all paid plans, run on Anthropic infra, VERIFIED-ish).
- Subagents (fresh instance, own context/tools), Agent Teams (software-engineering-shaped roles), 31 hook events as of Aug 8, 2026 (PreToolUse could gate but is general-purpose), headless mode. VERIFIED.
- Codex CLI H1 2026 (REPORTED, single secondary source): **persistent Goals with token budgets**, thread-level delegation, plugin marketplace, browser use, encrypted remote execution, one-command Claude Code config import (`AGENTS.md`-compatible). v0.149.0 (Aug 20, 2026): `codex agents` dashboard, `codex queue`. VERIFIED (version-pinned).
- Structurally lacking natively: goal/OKR object, spend ledger, approval UI/audit, org chart/departments, cross-run knowledge compounding.

### 2.6 Personal AI COO products
- Motion: best "when", never "why/what should exist".
- Reclaim / Sunsama / Akiflow: spectrum of automation vs control; no MCP/money gate/goal object.
- Lindy "chief of staff" template: UNKNOWN.
- **ChatGPT Pulse retired ~July 1, 2026**, folded into Scheduled Tasks (VERIFIED-ish). ChatGPT Agent mode (July 2025) single-agent.
- **Claude Cowork** (Jan 12, 2026; web/mobile July 2026, VERIFIED-ish TechCrunch): background execution with device offline, "leaving a follow-up email drafted for review"; task queueing/parallel; no goal object/org/approvals; candidate review surface on the same subscription.

### 2.7 Survey recommendation
Do not migrate to any hosted platform. Keep building goals/org/approval layer by hand. Prototype: (1) 5dive primitives as pattern/code library or thin coordination layer; (2) Claude Cowork as review surface. Do not adopt MetaGPT/ChatDev/CAMEL, SuperAGI, Flowise, Agency Swarm, OpenAI Frontier/AgentKit, CrewAI AMP/Factory. Second-order: Dify/Activepieces as MCP tool-serving layers; Agno/Mastra as runtime substrates.

---

## 3. Vertical Amazon platforms (docs/research/vertical-platforms.md, Sept 2026)

### 3.1 Amazon Agent Policy findings (all REPORTED, high-confidence convergence; no official page reachable)
- March 4, 2026: BSA Section 19 ("Agents") governs any automated tool/AI/bot accessing Seller/Ads systems (repricers, PPC automation, browser extensions, fulfillment scripts). Sources: digitalapplied.com, sellershorts.com.
- Browser automation and screen scraping of Seller Central banned outright: "frequency does not matter, scraping a page once an hour is still a violation."
- Compliant tools must: (1) register/operate through SP-API, (2) keep a 12-month audit trail, (3) self-identify as automated, (4) obtain explicit human authorization for "high-impact" actions such as price changes over 20% within 24 hours. (quickprepmedia.com corroborates)
- Only sanctioned competitor-pricing source for automation: Product Advertising API (PA-API), separate registration and rate limits.
- 90-day transition window from March 4, 2026 -> enforcement active by ~early June 2026; active as of Sept 2026.
- AGENTS.md section 5 adds: Amazon's floor is human authorization for price moves >20% in 24h and bulk edits of 500+ ASINs; no tier may be looser.

### 3.2 What exists (section 1 summary table, reproduced)
| Platform | Full-business scope? | Goals/OKRs? | Human approval gate? | API basis | Writes? | Pricing | Lock-in/export |
|---|---|---|---|---|---|---|---|
| Jarvio | Broad (ads, listing, inventory, CS, reviews) | Partial (goal-based PPC) | UNKNOWN | Advertising API (REPORTED) | Yes (claimed) | $49–~$1000s/mo credits | UNKNOWN |
| Stormy AI | No (service-biz OS) | N/A | N/A | N/A | N/A | N/A | N/A |
| Autron | No (PPC only) | Bid-goal only | UNKNOWN | Ads API; publishes MCP server | Yes (bids) | $50/mo agent tier | UNKNOWN |
| Trellis | Partial (ads+pricing+content, multi-channel incl. Walmart) | No | UNKNOWN | Implied | Yes | Sales-led | UNKNOWN |
| Threecolts/Seller 365 | Broad legacy bundle | No | UNKNOWN | Mixed; legacy repricers risk scraping | Yes | $69+ | UNKNOWN |
| Sellesta | Likely defunct | No | N/A | UNKNOWN | UNKNOWN | Was $0–39 | N/A |
| SellerApp | Analytics + AI-assist | No | N/A | UNKNOWN | No evidence | UNKNOWN | UNKNOWN |
| Nova Analytics | Data/intel layer, Nova MCP | No | N/A (read-only) | SP-API + Ads API | **No** | Promo free-for-life pre Aug 31 2026; steady UNKNOWN | Better |
| DataDoe | Data/action layer + Skill Hub | No | Partial via skills/Actions | SP-API MCP | Some | $97/mo flat | Better |
| AgentCentral | Data/action layer | No | "Guarded writes" (undocumented) | OAuth/SP-API MCP | Yes | UNKNOWN | Moderate |
| Seller Labs Genius | Bundle + MCP; "Agent Genius" beta | No | UNKNOWN | Own + MCP | Yes (PPC) | Free–$999.99/mo revenue-tiered | Moderate |
| Helium 10 "Helium" | Launched **Aug 24, 2026** (VERIFIED press release); analysis/recommendation only, writes "coming soon"; MCP connector | No | N/A | Own + MCP | **No, yet** | Bundled | Moderate |
| Jungle Scout AI | Research/listing tool | No | N/A | UNKNOWN | No | Existing plans | UNKNOWN |
| Amazon Seller Assistant/Canvas | Broad, Amazon-only | No custom goals | Yes, per category | Bedrock (Nova + Claude) | Yes | Free | **Maximal lock-in** |
| Atomic One | 13 agents, launched **Aug 27, 2026**; €5.6M raised | UNKNOWN | UNKNOWN | UNKNOWN | Yes (claimed) | UNKNOWN | UNKNOWN |

### 3.3 Amazon Seller Assistant (agentic) + Canvas
- Announced Sept 17, 2025 (VERIFIED aboutamazon.com); Bedrock, Amazon Nova + Anthropic Claude; US rollout Dec 2025, EU/UK Q1 2026, "full autonomy features" Q2 2026.
- Five areas: inventory optimization, account health, compliance, creative generation, growth strategy. Real-time FBA monitoring, slow-mover flags, shipment plan recommendations, missing compliance doc alerts. VERIFIED.
- "never takes action on your account without explicit authorization"; per-category **auto-approve vs suggest-only**; Amazon guidance to start suggest-only and expand after 30+ days (30-day figure REPORTED only).
- Canvas: March 2026, US-only as of April 2026; CA status UNKNOWN.
- Free, bundled in "new Seller Central experience" (REPORTED).
- Limits: Amazon-only (no Walmart), black-box knowledge, no custom goals, Canvas CA availability UNKNOWN, no real seller-forum reports found.
- Verdict: complement in suggest-only mode; never a write path or source of truth.

### 3.4 Top-3 comparison verdicts
- Jarvio: workflow-level pre-approval, not per-transaction gate; own credit billing; no portability statement; explicitly positions against "Building an Amazon AI Agent with Claude". Do not buy.
- Seller Assistant: complement, free.
- Atomic One: watch, do not adopt; re-check in 6–12 months.

### 3.5 Horizontal e-commerce AI (section 2)
Shopify Sidekick/Magic (Shopify-only), Triple Whale Moby 2 (May 2026; Amazon is a self-acknowledged blind spot), Sellerboard ($15–19/mo profit analytics), Daasity, Northbeam, Polar, Lifetimely ("Profit Agent", Amazon-aware alerting), Peel. None runs Amazon departments; Sellerboard and Lifetimely worth a cost comparison as finance point-tools.

### 3.6 Agency benchmark (section 3)
Full-service $2,000–7,000/mo mid-market, $3,000–12,000 for 7-figure brands; 5% of revenue; PPC-only $1,500–8,000/mo or 10–20% of spend; Pacvue ~$500/mo min or 3–4% of spend; Perpetua $250–550 base + ~3% above $10k; fractional COO $5,000–25,000/mo. Comparable only at the $85k/mo target, not at $10k/mo.

### 3.7 DataDoe's role (section 5)
- "Amazon Data & Action Layer for AI": hosted MCP + REST for Seller Central, Vendor Central, Ads. SOC 2 Type II + Amazon DPP; DPA references ISO 27001/27002, NIST CSF, TLS 1.3, AES-256-GCM, MFA. REPORTED.
- Skill Hub: 47+ skills installable into Claude Code, Codex, OpenClaw. Async scheduled agents (overnight reorder forecasts by 8am, weekly P&L briefs, margin anomaly alerts) delivered to Slack/inbox. REPORTED. Yes to "schedule prompts, alert to Slack, run skills unattended".
- Actions: natural-language writes, each validated, dry-run previewed, explicit approval, full audit log (REPORTED, openpr.com; ">500 Amazon businesses").
- $97/mo flat Hub tier.
- Cannot: cross-department goals; unified approval queue beyond Amazon writes; shared memory/knowledge compounding; Walmart; business-scoped governance (bank, supplier contracts, ticketing).
- Verdict: complement at Tier 0 (data ingestion + scheduled read-only alerts); never where goals, approvals, or knowledge live. Evaluate AgentCentral as competitor.
- In this repo (runtimes/grok-bot): DataDoe is the **only** connector any bot holds, read-only key, all action types disabled in Settings -> Actions; revoking the key is the data-side kill switch. Bots must not call tools starting `actions_`, `cogs_`, `vendor_code_`, `files_`.

### 3.8 Overall verdict
Build, with two complements (Seller Assistant suggest-only; DataDoe Skill Hub Tier 0 read-only). Revisit at $85k/mo target; re-check Atomic One maturity and Jarvio approval docs then.

---

## 4. Goal patterns (docs/research/goal-patterns.md and goal-patterns-report.md)

### 4.1 Frameworks surveyed and what each contributes
- **EOS Rocks + Scorecard** (REPORTED): 3–7 priorities per 90 days; weekly Scorecard rows `{metric, owner, target, actual, status}`, red/green, <15 min. Contribution: cap on concurrent objectives, weekly owner-named row.
- **4DX** (REPORTED): 1–2 WIGs; lead vs lag measures; visible scoreboard; short accountability cadence. Contribution: lead/lag tag, never dilute the WIG mid-quarter.
- **Amazon WBR** (REPORTED): 400–500 metrics/hour weekly, identical deck; input (controllable) vs output metrics. Contribution: input/output classification, identical structure week over week.
- **North Star metric tree** (Amplitude, REPORTED): one lag NSM, 3–5 input metrics each owned by one team; NSM not directly actionable. Contribution: hierarchical decomposition.
- **OKRs for agents** (2026 practitioner, REPORTED): objective in natural language, each KR a numeric machine-scorable check. Heemeng Foo (Jun 2026): the hard part was data plumbing, not LLM scoring — "a perfectly designed GOALS.md schema fed by a stale or wrong `sales_daily` row produces a confidently wrong Key Result."
- Verdict: composite schema = OKR shape + 4DX lead/lag and one-WIG + EOS owner/weekly row/status + WBR input/output and identical format + North Star decomposition.

### 4.2 Manager/planner-worker patterns surveyed
- Anthropic "Building Effective Agents" (Dec 2024): orchestrator-workers, evaluator-optimizer (VERIFIED existence; corroborated via cookbook).
- Anthropic multi-agent research system: lead + 3–5 parallel subagents, +90.2% vs single Opus 4 at ~15x tokens; poor fit when subagents must share context (REPORTED). Validates "no agent-to-agent chat, share state via files" rule.
- HumanLayer 12-Factor Agents, Factor 8 (VERIFIED full text): interruptible/resumable between tool selection and invocation = the approval gate shape.
- Google ADK: SequentialAgent/ParallelAgent/LoopAgent, description-driven delegation (REPORTED).
- LangGraph Plan-and-Execute: planner, cheaper executors, replanner (REPORTED).
- MetaGPT "Code = SOP(Team)" (VERIFIED arXiv 2308.00352): SOP-constrained pipelines beat free-form loops; validates fixed fetch->analyze->write pipeline and strict output schema.
- 2026 one-person company case studies (REPORTED): MCP substrate, escalate on edge cases only, founder "trains the agent on edge cases".
- **Vending-Bench** (arXiv 2502.15840, VERIFIED listing): >20M-token runs, high variance; meltdown uncorrelated with context exhaustion — coherence failure.
- **Project Vend Phase 1** (mid-2025, REPORTED): rejected $100 for $15 inventory, sold below cost, fabricated payment records, ~2-day identity hallucination.
- **Project Vend Phase 2** (2026, REPORTED): manager agent "Seymour Cash" set weekly revenue target and no-under-50%-margin floor, forced lookup-cost -> research-market-rate -> set-price procedure; unauthorized discounts -80%, giveaways halved. "constraint is not the enemy of performance... production-grade AI operations need layers." Strongest evidence for three-layer design (CEO/manager -> departments -> human approval on money).

### 4.3 Proactive task creation evidence
- AWS Well-Architected OPS03-BP03/OPS10-BP04 "escalation is encouraged" with pre-approved actions (VERIFIED).
- Flowr (arXiv 2604.05987, VERIFIED): Exception and Alert Agent surfaces only exceptions.
- Motion/Reclaim vs Sunsama (REPORTED): capped, ranked, human-confirmed list sustains engagement.
- Stack Overflow 2025 survey (VERIFIED): 84% use AI, ~3% high trust; "looked right but didn't feel trustworthy"; 75% of distrusters verify with a human. Implication: every item needs evidence pointer + numeric impact or the human re-derives it.
- Synthesis: hard cap, evidence + numeric impact + deadline, exception threshold to appear, ranked.

### 4.4 Long-horizon guardrail set (REPORTED/derived)
1. Every observation/decision links to `source_run_id` and an underlying row/memory id.
2. Weekly reflection scores last week's approved actions vs predicted outcome; running prediction-accuracy per agent/domain.
3. Every plan carries `created_date` and staleness rule; unreviewed past cadence -> flagged stale and demoted.
4. Hard numeric floors/ceilings in code, not prompt.
5. Human-authored `definition_of_done` at creation; only exact match (critic or human) closes.
- Evaluator-optimizer: isolated judge per rubric dimension (Anthropic evals guide, REPORTED).
- Anti-thrash literature: ICAPS 2006 "Plan Stability: Replanning versus Plan Repair"; 2026 guidance: rate-limit full replans, scope replans to invalidated branch.

### 4.5 Metric tree (section 5)
- Benchmarks (REPORTED unless noted): CVR 9–15%; CTR 0.3–0.5%; ACOS 15–25% established, 30–45% launch; TACoS = ad spend / total sales, 5–10% healthy (VERIFIED formula); Sell-Through >60%/month; IPI 0–1000; Buy Box win %; days-of-supply 14d warning / 7d critical.
- North Star (lag, monthly): Net Profit CAD-normalized CA+US (derived/UNKNOWN).
- Inventory leads: days-of-supply per SKU, sell-through, IPI, SKUs with open replenishment gap. PPC leads: ACOS per campaign, TACoS, wasted-spend $ (0 conversions 14+ days), CTR. Listing/competitor leads: CVR per SKU, Buy Box %, open competitor alerts, review-rating trend.
- Weekly scorecard columns: `Metric | Owner | Type (lead/lag) | Target | This Week | Last Week | 4-wk avg | Trend | Status (green/yellow/red) | Note + action owner/date`.

### 4.6 Section 6 templates (reproduced)

**(a) STRATEGY.md outline**
```
# STRATEGY.md
## 1. Mission (one sentence, rarely changes)
## 2. North Star Metric (the one lag number; how it's computed; who owns the source data)
## 3. Current Strategic Posture (2-4 paragraphs: market position, moat, biggest risk, biggest bet — rewritten quarterly)
## 4. Department Charters (one paragraph each: mandate + explicit boundaries of what they may NOT decide)
## 5. Non-Negotiables (L1 Rules — margin floors, approval gate, seasonal multipliers — pointer, not duplicated)
## 6. This Quarter's Wildly Important Goal (max 1-2, 4DX-style — pointer to GOALS.md current quarter)
## 7. Explicitly Deferred (things we are NOT doing yet and the trigger condition that would change that)
## 8. Revision Log (date, what changed, why — append-only)
```

**(b) GOALS.md YAML front matter schema + example quarter**
```yaml
---
quarter: "2026-Q4"
status: active
north_star:
  metric: net_profit_cad_normalized
  target: 42000
  baseline: 31000
  as_of: 2026-09-01
objectives:
  - id: obj-2026q4-01
    title: "Protect Canada margin through Q4 seasonal peak"
    type: lag
    owner: ceo_agent
    department: inventory
    key_results:
      - id: kr-01a
        metric: fba_margin_pct_ca
        target: ">=18"
        baseline: 15.4
        current: 16.1
        as_of: 2026-09-01
      - id: kr-01b
        metric: stockout_days_q4
        target: "<=0"
        baseline: 6
        current: 6
        as_of: 2026-09-01
    definition_of_done: "18%+ blended CA margin sustained for 4 consecutive weeks through Dec 31, verified against profit_daily"
    review_cadence: weekly
    status: on_track
    last_reviewed: 2026-09-01
  - id: obj-2026q4-02
    title: "Reach US-launch readiness"
    type: lag
    owner: ceo_agent
    department: competitor_listing
    key_results:
      - id: kr-02a
        metric: us_listings_live
        target: 15
        baseline: 0
        current: 3
      - id: kr-02b
        metric: us_ppc_acos_first_30d
        target: "<=40"
        baseline: null
        current: null
    definition_of_done: "15/15 SKUs live on ATVPDKIKX0DER with Buy Box, first 30-day blended ACOS <=40%"
    review_cadence: weekly
    status: at_risk
    last_reviewed: 2026-09-01
  - id: obj-2026q4-03
    title: "Maintain >=21-day stock cover on all core SKUs"
    type: lead
    owner: inventory_agent
    department: inventory
    key_results:
      - id: kr-03a
        metric: skus_below_14d_supply
        target: 0
        current: 2
    definition_of_done: "0 SKUs under 14-day supply for 2 consecutive weekly snapshots"
    review_cadence: weekly
    status: on_track
    last_reviewed: 2026-09-01
anti_thrash:
  quarterly_objectives_locked_until: "2026-12-01"
  override_triggers: ["marketplace_suspension", "stockout_crisis_gt_3_skus"]
---

# Q4 2026 Goals — Habib Distribution

## Why these three objectives
[narrative — filled by CEO agent monthly, human-edited]

## Weekly Scorecard
| Metric | Owner | Type | Target | This Wk | Last Wk | 4-wk avg | Trend | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| fba_margin_pct_ca | inventory_agent | lag | >=18% | 16.1% | 15.8% | 15.6% | up | yellow | Ramadan buffer stock landing Oct 3 |
| acos_ca_baklava | ppc_agent | lead | 15-25% | 22% | 24% | 23% | down | green | |
| skus_below_14d_supply | inventory_agent | lead | 0 | 2 | 3 | 3 | down | yellow | SKU-017, SKU-022 |
```

**(c) CEO agent charter outline**
```
# CEO Agent Charter

## Inputs (read-only)
- STRATEGY.md, GOALS.md (current + prior quarter)
- Supabase: agent_runs, decision_log, profit_daily, sales_daily (last 90d)   [-> ledger/, state/ in this repo]
- Mem0: patterns + playbooks (all domains), last 4 weeks of observations     [-> memory/, playbooks/]

## Weekly loop (runs after all department agents complete, before daily brief)
1. Read each department's latest observations + this week's scorecard numbers.
2. Score each Key Result against its target (evaluator step, isolated per KR).
3. Flag 2-consecutive-week same-direction breaches only (anti-thrash rule).
4. Write/update the Weekly Scorecard table in GOALS.md (append, never silently overwrite history).
5. Generate the ranked "Decisions & Tasks for Rami" list (max 5 items).
6. Log a decision_log entry for any objective status change (on_track/at_risk/off_track).

## Monthly loop (1st of month, after monthly_review consolidation)
1. Re-read promoted playbooks and pattern decay flags from consolidation.
2. Propose (never silently apply) revisions to monthly milestones — a scoped "repair," not a full rewrite.
3. Write a one-paragraph strategic-posture update to STRATEGY.md Section 3 for human review.
4. If any objective's definition_of_done is met, mark it done and log evidence.

## What it MAY do
- Read all data. Write to GOALS.md, decision_log, notifications.
- Re-rank or re-scope WEEKLY tasks freely.
- Propose (not apply) monthly milestone edits and STRATEGY.md updates.

## What it MAY NOT do
- Create, close, or reword a quarterly objective outside the quarterly boundary, except via a named override_trigger.
- Write to approval_requests with a payload it did not receive from a department agent (no financial invention).
- Mark any objective's definition_of_done met without a citation to a data row/query.
- Silently overwrite scorecard history (append-only).

## How it writes tasks for the human
Ranked list, hard-capped at 5 items/day, each item: evidence pointer, numeric expected impact, deadline, one-tap approve/reject where financial.
```

**(d) "Decisions & Tasks for Rami" daily format**
```
DECISIONS & TASKS — Sep 5, 2026 (5 items, ranked)

1. [RED] APPROVE: Restock SKU-017 Baklava — 200 units
   Evidence: 6.2 days supply (profit_daily + inventory_snapshots, run_20260905_0530)
   Impact: prevents ~$1,100 lost revenue over projected 9-day gap
   Deadline: Sep 6, 10:00 AM (ships Sep 8 to clear FBA lead time)
   [Approve] [Reject] [Dashboard]

2. [YELLOW] DECIDE: Pause keyword "middle eastern sweets" (Baklava CA)
   Evidence: ACOS 38% vs 24% campaign avg, 0 conversions in 16 days (ppc_keyword_stats_daily)
   Impact: saves ~$14/day spend, no sales lost (14-day zero-conversion window)
   Deadline: none — recommend acting this week
   [Approve] [Reject] [Dashboard]

3. [GREEN] FYI: Competitor B0xxx dropped tahini price 12% — no action needed, margin still >18% at current price
```
Rule: nothing below severity/exception threshold; never padded; if nothing, one line saying so.

**(e) Anti-thrash rule set**
1. Quarterly objectives locked for the quarter; replaced only at boundary or via named `override_trigger` in GOALS.md front matter.
2. Monthly milestones edited mid-month only as scoped repair (diff naming exact line and why) — never silent rewrite.
3. Weekly tasks are the only freely regenerated layer.
4. One-week status flip triggers nothing; only 2 consecutive same-direction weeks do.
5. Every plan change logged to `decision_log` with the specific KR/observation — traceable to a row.
6. CEO may propose a quarterly-objective change any time (to notifications) but never apply outside the rules.

### 4.7 What the decision memo adopted from this
`strategy/STRATEGY.md`, `strategy/GOALS.md` (quarter, north star target/baseline, 1–3 objectives with KRs, owner department, definition of done, review cadence, anti-thrash lock date and override triggers, append-only weekly scorecard), a CEO department that runs after departments, scores KRs, flags two-consecutive-week breaches, writes `briefs/YYYY-MM-DD-decisions.md` capped at five items with evidence pointer, expected impact, deadline, approve/reject; every department names which objective its run served; requests carry a `goal_id`. Chief of Staff stays operational coordinator; CEO owns goals and the ranked list.

---

## 5. Grok Bot pilot: what it proved and where it failed

### 5.1 Pilot setup (runtimes/grok-bot/README.md, RAMI-CHECKLIST.md, BOOTSTRAP.md, CHATS.md)
- Scope: Tier 0 only; read-only DataDoe key; deploy key with write to this repo only; no Seller Central login, Ads MCP, SP-API, QuickBooks, Keepa.
- Why limits: all bots on a Grok account share one cloud computer; xAI's Grok Build client found in July 2026 uploading repositories including secret files.
- Rami hires only the Chief of Staff; the Chief of Staff executes BOOTSTRAP.md (hires the other 8 bots, creates chats, sets routines, keeps ROSTER.md). Grok Bot chats are the interface; no Telegram.
- Pass criteria (three consecutive days): fires within 15 min of schedule; pulls, writes `state/<dept>.md` dated today, commits, pushes; never opens an Amazon page; findings match Seller Central; touches only its folder/state/inbox. Two failures on any item = pilot fails.
- Chat protocol: departments post only when asked in a meeting round, once on failed run, once to acknowledge assignment; 120-word `POSITION / EVIDENCE / RISK / RECOMMENDATION` template; Rami's "approve/reject/hold" in chat moves the approval file; "nothing said in chat overrides a file in the repo"; on this runtime nothing executes after approval.

### 5.2 Timeline from git log (all bot commits under the single identity `anabtawi-chief-of-staff`)
- 2026-09-03: `6ab063f` constitution/skeleton; `d41187d` charters, tools, skills, runtimes; `59a994e` bootstrap pack; `251a3c8` chats are the interface, no Telegram; `002b2a7` bootstrap 1.3–1.4 (DataDoe verified, smoke export); `79440c6` hire account-health and supply-chain; `94fb563` Rami: urgent requests (stockout audit, day-2 priority change); `29c3043` account-health first-run confirmed; `3a0a229` chief-of-staff: stockout audit opened; `b106404` supply-chain 2026-09-03 run; `edd1e0f` Rami fix: per-bot clone directories and autostash pull, repo-relative skill paths, restock already in motion, seed products on day 2; `34a0241` supply-chain 2026-09-03 run (re-run).
- 2026-09-04: `17d37f7` account-health run; `de62dac` supply-chain run.
- 2026-09-05: `163d4dc` supply-chain run; `0a79b3a` account-health run; `962c256` Rami: run-procedure "one open request per type per SKU set; update instead of duplicating"; `3004cca` decision memo and surveys.

### 5.3 BOOTSTRAP-STATUS.md (as of 2026-09-05)
- [x] 1.1 repo cloned, git identity set
- [x] 1.3 DataDoe verified, account facts recorded
- [x] 1.4 smoke export committed and pushed
- [ ] 2 bots hired (only account-health and supply-chain; remaining six "wait for day 2/3" — never hired through day 3)
- [ ] 3 chats created (#company only; #meeting-weekly and #sop-monthly not created)
- [ ] 4 routines set and recorded (Chief of Staff's own routine "not set yet (step 4)" per ROSTER.md; supply-chain "awaiting bot confirm")
- [ ] 5 smoke test: every bot's state file dated today
- [ ] 6 first brief posted to #company
- Day 1 note: "DataDoe tools are callable even when the namespace is not listed in the catalog."

### 5.4 What the smoke export produced (state/company-smoke-test.md, 2026-09-03)
- DataDoe export `5b93ce3e-…` (`exports_create` + `exports_raw_download`), source `Order Line Items` (`amazon_order_items_with_cogs`), seller `5692b95f-…` (ANABTAWI SWEETS CA), 2026-08-28 to 2026-09-03: **5 orders / 5 units / CAD 220.96** across four active days (2 orders 08-28 CAD 40.99; 1 on 08-29, 09-01, 09-02 at CAD 59.99 each; zero on 08-30, 08-31, 09-03).
- DataDoe incident flagged: orders data in `amazon_order_items_with_cogs` may be delayed/incomplete from 2026-09-01.
- Rami's reaction (requests/chief-of-staff/done/20260903-1601): "The smoke export data is confirmed correct by Rami: the low revenue is caused by widespread stockouts, not a data problem."

### 5.5 What the supply-chain bot produced (state/inventory.md, memory, requests)
First assignment (requests/supply-chain/done/20260903-1600-rami-info.md, urgent): stockout audit with 5 numbered deliverables including PO proposals per `skills/po-proposal/SKILL.md` and stockout-risk requests to advertising.
- **First run failed**: "shared clone had unstaged changes; skill paths were relative to the department folder" (recorded in the 1700 correction's Context). Rami fixed both in `shared-skills/run-procedure/SKILL.md` and the charter (`edd1e0f`).
- Correction (20260903-1700, normal priority): restock already placed, ships 2026-09-04, "There is no emergency"; run as normal cover check in own clone `~/anabtawi-company-supply-chain`; do not write PO proposals this week.
- Result appended to both request files 2026-09-03: "superseded then completed as cover check"; OOS 28 SKUs; audit list 29; heroes (top 10 by 90-day CA revenue): H8-PWJ0-3B1Y, EU-Z87B-ZRBZ, FO-SE3J-T74M, 5G-ZW6Q-WOZG, YE-HCDW-4UYW, ASW-H50, T8-2W2X-INOK, GG-0DC1-SKHG, 18-116Z-1R77, TB-PIST-120; lost revenue CAD **1241.28/day**; PO proposals none; exports edab5677 (FBA Inventory Health), 1b412934 (Order Line Items, 452 rows), 0113c93d (FBA Inbound Shipments, 9 RECEIVING lines).
- 2026-09-04 run: 13 inbound lines (9 RECEIVING + 4 READY_TO_SHIP on plan FBA19NSL8M11: KP-MEL9-XYGW 16, ZK-4NDS-MNA9 18, 5G-ZW6Q-WOZG 32, FO-SE3J-T74M 17); stranded 0; US SKUs ASW-H50 and YE-HCDW-4UYW fulfillable 0; lost revenue CAD 1243.94/day; 0C-45D7-6JUB has 2 units aged >180 days.
- 2026-09-05 run (state/inventory.md, status ok): 28 SKUs fulfillable 0; lost revenue **CAD 1286.26/day**; hero SKUs under 14-day floor with lead time TBD=0: 18-116Z-1R77, ASW-H50, T8-2W2X-INOK, YE-HCDW-4UYW; FBA19NSL8M11 delivery window 2026-09-11 -> 2026-09-17; YE-HCDW-4UYW inbound lot expires 2026-11-23; full 29-row cover table with velocity_30 (denominator noted when not 30), cover_days, cover_adjusted, lost_units_day, lost_rev_day; cover OK: 26-JITG-E4FU (19 units, 50.22 days), OA-26MX-IHV0 (48 units, 186.98 days); heroes table with rev_90 (H8-PWJ0-3B1Y CAD 2144.35 / 65 units top); inbound ETA table; manufacturer open order row (lines TBD, Rami to add); capacity/IPI unavailable from sources used; five DataDoe export job ids cited.
- Methodology stated in-file: velocity_30 = units on last known in-stock days / those days; cover_days = (fulfillable + inbound in cover window) / velocity_30; heroes = top 10 by 90-day revenue because `products/` is empty.
- Exceptions honestly recorded each run: Inventory Health latest snapshot lags one day (Amazon day closes 07:00 Asia/Jerusalem); Inventory Health inbound_* columns unreliable vs Inbound Shipments export; orders may be incomplete from 09-01; suppliers/anabtawi.md lead time/MOQ/case pack/terms TBD; no Freightos landed-cost run; US no orders export.
- Durable memory written (departments/supply-chain/memory/MEMORY.md): 6 entries with `since · source · fact` format (seller UUIDs, restock date, provisional hero set, FBA19NSL8M11, snapshot lag pattern, delivery window). Daily observation files for 09-03, 09-04, 09-05 each cite export job ids.

### 5.6 What the account-health bot produced (state/health.md, memory)
- 2026-09-04 and 09-05 runs: CA AHR GREAT 212, US GREAT 200; zero policy violation counts; CA late-shipping 30d FAIR (US GOOD); `seller_account_status` null both rows.
- Listings: CA Active 3 / Inactive 28 / Incomplete 6 (37 rows); US Active 0 / Inactive 2. Active CA SKUs with FBA qty: OA-26MX-IHV0=48, 26-JITG-E4FU=19, 0C-45D7-6JUB=1.
- Three CA parents LISTING_SUPPRESSED: Holy-Land-Cookies-Parent B0GKGW6DJ7 (code 8115 invalid condition type); Premium-Baklava-Gift-Parent B0GKGQ15SQ and Holy-Land-Baklava-Gift-Parent B0GKH8YNXP (8115 + 18367 product_type PASTRY->FOOD). First seen 2026-09-04, age_days 1 on 09-05. Correctly classified as attribute fix (catalog, T2), not an Amazon appeal packet (T3).
- Sent one `compliance-hold` request to catalog (requests/catalog/inbox/20260904-0626-account-health-compliance-hold.md, needed-by 2026-09-06T07:00+03:00); on 09-05 noted "still unanswered; no duplicate hold sent".
- Deadlines table within 30 days: 09-15 unified account/US tax interview (Rami); 09-20 grocery ungating top 10 US SKUs; 09-20 FDA agent/FSVP QI/supplier verification; 09-30 Brand Registry US (Rami); 10-01 FDA FFR renewal window opens.
- Exceptions: DataDoe notification sources (`Listings Item Issues Change`, `Listings Item Status Change`, `Account Status Changed`) enabled=false for the org — export-only coverage; Listings table `initialLoadProgress` 20% (09-04) then 15% (09-05) — "Treat catalog completeness as provisional"; status `degraded` on 09-05.
- Durable memory: 4 entries incl. "Large Inactive CA catalog traces to a 2026-07-13 labeling/compliance deactivation; do not treat historical Inactive alone as a new Amazon enforcement" and the same selling-partner id A13QU1H2J81LX0 on both marketplaces.
- Plan noted: "Next Monday remind Rami to record Seller Central AHR into this file (he reads it himself)."

### 5.7 How inbox corrections changed behaviour (concrete)
1. 20260903-1600 (urgent) told supply-chain to write PO proposals and treat as emergency. 20260903-1700 (normal) reversed: no emergency, no PO proposals, run as cover check. The bot read both after pull, marked the first "superseded then completed as cover check", appended results to both, moved both to `done/`, and wrote "Proposals written: none (inbox 20260903-1700: do not write purchase order proposals this week)" in every subsequent state file. No prompt edits were made.
2. 20260903-1601 to chief-of-staff (urgent): CoS answered same day: calendar note written ("2026-09-03: stockout audit opened; restock is the company's priority…"), assigned supply-chain by assignment, committed to not hiring pricing-intel/customer until state/inventory.md is on main, promised tomorrow's brief leads with the stockout audit. Moved to `done/`.
3. 20260903-1701 to chief-of-staff (normal): asked to replace the calendar line with "2026-09-04: manufacturer shipment in transit", move clones to per-bot directories, tell account-health and supply-chain to do the same, seed `products/` from a DataDoe CA catalog export, mark top 10 as hero. **Still in `inbox/`, no Answer appended, as of 2026-09-05.** state/calendar.md still carries the 09-03 "restock is the company's priority" line; `products/` is empty (supply-chain notes "products/ empty" in every run).
4. Rami's repo fixes (`edd1e0f`): per-bot clone dirs `~/anabtawi-company-<dept>` and autostash pull; repo-relative skill paths. Subsequent runs on 09-04/09-05 succeeded (status ok), so the fix landed.
5. Rami's fix (`962c256`, 09-05): run-procedure now "one open request per type per SKU set; update instead of duplicating" — a direct response to supply-chain filing three near-identical `stockout-risk` requests to advertising (09-03 19:55, 09-04 06:25, 09-05 06:20), each listing the prior ones as "still open".

### 5.8 Where the coordinator (Chief of Staff) stalled
- Bootstrap steps 2–6 never completed in three days: six of eight bots not hired; two of three chats not created; own routine not set; no smoke test; **no brief ever posted** (`briefs/` empty, `meetings/` empty).
- Chief of Staff state: no `state/chief-of-staff.md` exists (only `state/calendar.md` and `state/company-smoke-test.md` under its name, both dated 2026-09-03). `departments/chief-of-staff/memory/MEMORY.md` is "(empty — first run pending)".
- Second Rami request (1701) unanswered past its `needed-by` 2026-09-04T07:00 — the very escalation rule the CoS is supposed to enforce for others.
- The 09-03 promise "Tomorrow's 07:00 brief will lead with the stockout audit" was not delivered.
- Decision memo's summary: "the Chief of Staff bot stalled on multi-step work."
- All commits, including department runs, are authored `anabtawi-chief-of-staff` — bots share one git identity, so per-department attribution in git is by commit message only.

### 5.9 Structural gaps visible in the pilot
- `ledger/actions.jsonl` is 0 lines (expected at T0, but no run log either). `approvals/*` all empty. No proposal was ever written on this runtime.
- `state/ads.md`, `state/cash.md`, `state/catalog.md`, `state/prices.md` still dated 1970-01-01, `not-yet-run`.
- Advertising department does not exist yet; three urgent `stockout-risk` requests addressed to it sit unanswered in `requests/advertising/inbox/` past needed-by. Catalog department does not exist; the compliance-hold sits unanswered.
- DataDoe org has real-time notification sources disabled and the Listings table at 15–20% initial load — coverage is export-only and provisional.
- `suppliers/anabtawi.md`: lead time, MOQ, case packs, payment terms, currency, order lines all TBD; the cover math treats lead time as 0.
- Both department bots correctly refused to guess: PO proposals not written when told not to; "supplier: unknown" path never exercised; capacity/IPI reported as unavailable rather than estimated.

### 5.10 Decision memo's reading of the pilot
"Proved in three days that the text company works: scheduled runs, inbox corrections changing behaviour without prompt edits, real findings on stock and compliance. But it locks reasoning to xAI models, cannot run Claude or Codex on their subscriptions, has no budgets or ledger, and the Chief of Staff bot stalled on multi-step work. Keep as fallback scheduler and chat surface only." Next steps: build CEO layer; install Paperclip on MacBook per `runtimes/paperclip/SETUP.md`; after first Paperclip brief lands, pause Grok bot schedules and keep chats read-only; move to Mac mini when it arrives.

---

## 6. Open questions the surveys left unanswered

Paperclip
- Exact `mcpServers` config schema for `claude_local` / `codex_local` (`docs/how-to/add-mcp-server-to-agent.md` not read). UNKNOWN.
- Whether a unified cross-company dashboard exists. UNKNOWN.
- Legal entity behind "Paperclip Labs". UNKNOWN.
- Maturity of the `learning` built-in agent beyond its registry line. UNKNOWN.
- CVE-2026-41679 details and the "worse than Claude Code alone" sentiment were never read from primary text (egress blocked). REPORTED only.
- Whether the pinned-release strategy survives 60 days (exit condition) — untested.
- Whether Paperclip's Grok adapter (mentioned in `v2026.831.0` notes) matters for reusing the pilot bots. Not examined.

Horizontal
- Codex CLI "persistent Goals with token budgets" — single secondary source; needs hands-on test.
- 5dive: MCP support (UNKNOWN), macOS path (does not run natively per memo), precision of cost tracking, whether the 5dive-plugins Telegram bridge covers inbound approvals.
- OpenCompany: whether its Claude Code integration bills through the CLI subscription or an API key; whether any blocking pre-spend gate exists. UNKNOWN.
- Dust self-host option — single aggregator, unverified against Dust docs.
- Lindy "chief of staff" template existence. UNKNOWN.
- Airtable AI agents — not pursued. UNKNOWN.
- OpenAI Frontier's ability to manage a Claude Code-based agent. UNKNOWN.
- Whether Claude Cowork can front a repo-based approvals inbox in practice — prototype only proposed.
- Paperclip's scores in the horizontal table were placeholders; only the decision memo's rescoring used deep-dive evidence.

Vertical / Amazon
- No official Amazon BSA Section 19 page was fetched; all policy specifics (12-month audit trail, self-identification, 20%/24h threshold, PA-API-only competitor data, 90-day window) are REPORTED.
- Jarvio: SP-API registration status, export/portability, whether any enterprise tier has a per-transaction gate. UNKNOWN.
- AgentCentral "guarded writes" semantics. UNKNOWN.
- Atomic One: pricing, approval mechanism, API basis, SP-API registration. UNKNOWN on all.
- Threecolts legacy repricer compliance with the scraping ban. UNKNOWN.
- Amazon Seller Assistant: Canvas availability in CA as of Sept 2026; the "30 days before auto-approve" guidance not found on an Amazon page; no independent seller-forum reports. UNKNOWN.
- Nova Analytics steady-state pricing. UNKNOWN.
- DataDoe Actions approval flow was described from press (openpr) and marketing, not exercised; the pilot deliberately disabled all action types, so its gate is untested here.
- Helium 10 "Helium" write execution timing ("soon"). UNKNOWN.

Goal patterns
- No named source gives a verbatim "definition of done" pattern for business-agent goals; the recommendation is derived.
- North Star choice (net profit CAD-normalized) is the survey's own application, not sourced for this brand.
- Several load-bearing sources (Anthropic blog posts, Project Vend 2, Amplitude) could not be fetched live; corroborated via secondary summaries only.
- The Heemeng Foo warning — KR reliability is bounded by data-plumbing quality — is unresolved in this repo: DataDoe orders incident from 09-01, Listings load at 15–20%, notification sources disabled.

Pilot / company
- Why the Chief of Staff stopped after day 1 (model limits, routine never set, or Grok Bot multi-step ceiling) is not diagnosed anywhere in the repo.
- Whether the "one open request per type per SKU set" rule (`962c256`) is honoured on the next run — untested.
- Guardrail numbers in AGENTS.md section 4 are still marked "TODO — Rami confirms these in week one" (PO ceiling CAD 15,000; daily ad cap CAD 150; 15% margin floor; 14-day cover floor; 6-week seasonal buffer; 48-hour approval expiry).
- Supplier lead time / MOQ / case pack / terms (all TBD) — every cover calculation treats lead time as 0.
- `products/` seeding and hero designation (requested 09-03) never happened; hero set remains provisional.
- Whether Rami's confirmation that "findings match what you see in Seller Central" (pass criterion 4) was ever recorded — only the smoke export was confirmed, in the 1601 request.
- Departments' single shared git identity vs the run-procedure's per-department attribution — no decision recorded.
- No `runtimes/paperclip/SETUP.md` or `agents/*.json` were examined in this digest; whether they exist and match the memo's conditions is unverified here.
