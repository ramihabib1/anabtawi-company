> Research report produced 2026-09-06 during the founding engagement. Where it mentions files of an earlier repository, treat those as context the researcher had, not as part of this design. The design that governs is docs/ANABTAWI-OS-DESIGN.md.

# Harnesses, schedulers, and the legal position of running AI departments unattended

Research date: **2026-09-06**. Everything time-sensitive below is date-stamped. Author: research agent for Rami Anabtawi.

---

## 0. Method, and a disclosure about what could not be opened

This session's network egress is on an allowlist. Hosts that **answered**: `code.claude.com`, `platform.claude.com`, `docs.claude.com`, `github.com`, `raw.githubusercontent.com`, `registry.npmjs.org`, `cloud.google.com` (root only), plus the live monday.com API through its MCP server. Hosts that were **blocked by the egress proxy (403 on CONNECT)** and therefore could not be read as primary sources today: `www.anthropic.com` (so `/legal/consumer-terms`, `/legal/aup`, `/legal/commercial-terms`), `support.claude.com`, `www.claude.com` (so `claude.com/pricing`), `openai.com`, `help.openai.com`, `developers.openai.com`, `chatgpt.com`, `x.ai`, `docs.x.ai`, `ai.google.dev`, `policies.google.com`, `docs.cloud.google.com`, `monday.com`/`support.monday.com`, `modelcontextprotocol.io`, `agentskills.io`, `agents.md`, `n8n.io`, `trigger.dev`, `inngest.com`, `temporal.io`, `docs.github.com`. The session's web-search budget was also exhausted mid-task (200/200 calls, shared with other agents), so secondary confirmation stops where noted.

Consequence for you: **the Anthropic clauses below that come from `code.claude.com/docs/en/legal-and-compliance` are VERIFIED** (I opened the page today and quote it exactly). **The Consumer Terms clause everyone cites is REPORTED, not VERIFIED** — I could not open `anthropic.com/legal/consumer-terms`. Before anything expensive depends on the OpenAI, xAI, or Google positions, someone with an unrestricted browser must re-verify sections 2-4. I flag each of those.

Tags used: **VERIFIED** (primary source opened today, URL given) · **REPORTED** (secondary source or vendor marketing) · **UNKNOWN** (could not confirm; what I tried is stated).

---

## 1. The verdict table

| Vendor | Unattended use on a consumer subscription | Basis |
|---|---|---|
| **Anthropic (Claude Max)** | **ALLOWED** for the subscriber running Anthropic's own unmodified surfaces (Claude Code CLI headless, Routines, Desktop scheduled tasks, GitHub Actions with a subscription OAuth token). **GREY** the moment a third-party product holds or brokers the credential. **PROHIBITED** to resell, share, or intermediate. | VERIFIED |
| **OpenAI (ChatGPT Plus/Pro + Codex)** | **GREY.** Codex CLI/cloud are first-party and support non-interactive `codex exec`, but I found no vendor statement blessing unattended scheduled runs on a plan credential, and sign-in is an interactive device-code flow. API key is the unambiguous path. | REPORTED |
| **xAI (SuperGrok / Grok bots)** | **GREY.** Grok's own "bots + routines" product is first-party scheduling, which is by construction permitted on the plan that sells it; but I could not open xAI's terms today, and there is a live security concern in this repo's own notes. | UNKNOWN on terms |
| **Google (Gemini CLI on AI Pro/Ultra)** | **GREY.** Gemini CLI is Apache-2.0 and ships a headless `-p` mode, but OAuth-login quota and terms live on a Google page I could not open. API key / Vertex is unambiguous. | UNKNOWN on terms |
| **monday.com agents** | **ALLOWED** — it is a first-party scheduled-agent product. But it is not a viable department harness (see §6). | VERIFIED (live API) |

---

## 2. Anthropic

### 2.1 The clauses that actually govern this

VERIFIED, `https://code.claude.com/docs/en/legal-and-compliance` (opened 2026-09-06). Quoted exactly:

> **Acceptable use.** "Claude Code usage is subject to the Anthropic Usage Policy. **Advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK.**"

> **Authentication and credential use.** "**OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude Code and other native Anthropic applications.**"

> "Developers building products or services that interact with Claude's capabilities, including those using the Agent SDK, **should use API key authentication** through Claude Console or a supported cloud provider. **Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, or Max plan credentials on behalf of their users. Moreover, developers may not collect, store, or intermediate Claude.ai credentials or session tokens** — sign-in to a Claude account must complete through Anthropic's own flow."

> "This does not restrict how customers provision and manage their own API keys ... **Nor does it prevent an end user from signing in to the unmodified Claude Code binary with their own Claude subscription**, including where a platform hosts Claude Code as described under *Can customers offer Claude Code in their products?*"

> **Hosting Claude Code in a product** requires Commercial Terms and: "**The Claude Code binary must not be modified.**" and "**Customers may not pay for, resell, or intermediate Claude usage on their end users' behalf.**"

> "Anthropic reserves the right to take measures to enforce these restrictions and may do so without prior notice."

REPORTED (could not open `anthropic.com/legal/consumer-terms`; hosts blocked, search budget exhausted): the Consumer Terms prohibit accessing the Services "through automated or non-human means, whether through a bot, script, or otherwise" except via an Anthropic API key or where explicitly permitted; and Anthropic moved on ~2026-04-05 to block third-party agents (OpenClaw named) that piggyback on individual subscriptions. Sources found in search but not openable: theregister.com (2026-02-20), daimonlegal.com, marketingagent.blog (2026-04-04).

**How to read the two together.** The "automated or non-human means" clause has an "**or where explicitly permitted**" carve-out, and Anthropic's own product documentation is that explicit permission: it documents subscription-authenticated headless runs, subscription-authenticated CI, cloud Routines that "run autonomously" on Pro and Max, and Desktop scheduled tasks. The line Anthropic is drawing is **not** attended-vs-unattended. It is **first-party-and-yours** vs **third-party-and-brokered**.

### 2.2 What is documented as working on a Max subscription

All VERIFIED on `code.claude.com/docs`, 2026-09-06:

- **Headless CLI.** `claude -p "..."` with `--output-format json`, `--json-schema`, `--permission-mode`, `--mcp-config`, `--allowedTools`. Normal mode uses your subscription login; **`--bare` deliberately does not** — "In bare mode, Claude Code never reads OAuth credentials or the system keychain" (`/docs/en/headless`). So never pass `--bare` on a subscription box.
- **Long-lived subscription token.** `claude setup-token` mints a **one-year OAuth token**; "This token authenticates with your Claude subscription and requires a Pro, Max, Team, or Enterprise plan. It can only make model requests, so it can't establish Remote Control sessions or fetch claude.ai connectors. MCP servers you configure locally still work." (`/docs/en/authentication`). Set it as `CLAUDE_CODE_OAUTH_TOKEN`. Bare mode ignores it.
- **GitHub Actions on the subscription.** The official action takes `claude_code_oauth_token`; "If you authenticate with an OAuth token, runs use your Claude subscription instead of API billing." Anthropic also warns: "For a secret shared across repositories, authenticate with an API key ... since an OAuth token is tied to the subscription of the person who ran `claude setup-token`." (`/docs/en/github-actions`).
- **Routines** (cloud, research preview). Available on **Pro, Max, Team, Enterprise**. Triggers: schedule (min interval **1 hour**), HTTP API (`POST .../routines/<id>/fire` with a bearer token), GitHub events. "Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode picker and no approval prompts during a run." They clone GitHub repos (no local files), use claude.ai connectors or a committed `.mcp.json`, and "**draw down subscription usage the same way interactive sessions do**", plus a **daily cap on runs per account**. (`/docs/en/routines`).
- **Desktop scheduled tasks** (local). Min interval **1 minute**, per-task permission mode, access to local files and local MCP config files, **only fire while the Desktop app is open and the computer is awake**; one catch-up run on wake for the most recent missed slot. Stored as `~/.claude/scheduled-tasks/<name>/SKILL.md`. (`/docs/en/desktop-scheduled-tasks`).
- **`/loop`** — session-scoped only, dies with the session. Not a scheduler.
- **Channels** (research preview, Pro/Max ✓) — an MCP server pushes webhooks/Telegram/Discord events **into a running session**. Requires the session to stay open.
- **Subagents** (`.claude/agents/*.md`, YAML frontmatter + system prompt body), **hooks** (`settings.json`), **skills** (`SKILL.md` with `name`/`description`/`disable-model-invocation`/`allowed-tools`/`context: fork`), **CLAUDE.md**, **plugins**, **MCP** — all available on every provider.
- **Claude in Chrome** — drives a real Chrome sharing your logged-in browser state. **This is exactly the capability Amazon BSA §19 forbids against Seller Central.** Do not install the Chrome extension on the ops user.
- **Anthropic's own docs assume unattended operation.** From `/docs/en/authentication`: "Renewing early matters most for **sessions that run unattended**."

### 2.3 Limits

REPORTED (support.claude.com blocked): Max 5x ≈ $100/mo, Max 20x ≈ $200/mo; a rolling **5-hour window** plus **weekly caps** tracked separately for Opus and non-Opus; Max 20x roughly 240-480 weekly Sonnet hours and 24-40 Opus hours; a temporary +50% Claude Code boost ran to 2026-08-31 and settles to a permanent +25% over the pre-July baseline from **2026-09-14**. Re-verify at `support.claude.com/en/articles/11049741-what-is-the-max-plan`.

VERIFIED mechanics (`/docs/en/costs`): `/usage` shows plan-limit breakdown; **usage credits** (metered overage) can be switched on at `claude.ai/settings/usage` with a monthly spend limit, and Routines that exceed the daily cap continue on metered overage only if usage credits are on. `autoContinueAtUsageLimit` makes a session wait for the window to reset instead of dying — relevant for unattended runs.

### 2.4 Cowork

REPORTED only (no Cowork page exists on `code.claude.com/docs`; `claude.com/docs` blocked): Cowork launched Jan 2026 macOS-only for Max, became generally available on paid plans on macOS+Windows; **scheduled tasks landed 2026-04-09**; connectors reach Gmail/Notion/Calendar/Figma; memory unified across chat and Cowork on **2026-08-25**. `/docs/en/costs` VERIFIES that on Team/Enterprise the seat allowance "is shared with Claude chat and Cowork" — i.e. Cowork spends the same pool.

**Verdict — Anthropic: ALLOWED**, for Rami running the unmodified `claude` binary and Anthropic's own scheduling surfaces on his own Max subscription. The quote that carries it: *"Nor does it prevent an end user from signing in to the unmodified Claude Code binary with their own Claude subscription"* combined with *"Advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK."* The exposure is the phrase **"ordinary, individual usage"** — nine departments × 3 runs/day, forever, is defensible as one person's ordinary usage; forty brands on one login is not.

---

## 3. OpenAI

VERIFIED (`raw.githubusercontent.com/openai/codex/main/README.md`, 2026-09-06): Codex CLI is installed from `chatgpt.com/codex/install.sh`; "Run `codex` and select **Sign in with ChatGPT**. We recommend signing into your ChatGPT account to use Codex as part of your Plus, Pro, Business, Edu, or Enterprise plan." API-key auth exists as a documented alternative. The repo's `docs/*.md` are now **stubs pointing at `developers.openai.com/codex/...`**, which is blocked here — so config reference, MCP config, and non-interactive mode could not be read primary today.

REPORTED (search, 2026-09-06): Codex is included in Free/Go/Plus/Pro/Business/Edu/Enterprise; Pro is 5x or 20x Plus; usage runs on a **rolling 5-hour window shared by local CLI and cloud chats**, with additional weekly limits; on 2026-07-12 OpenAI temporarily removed the 5-hour restriction for Plus/Business/Pro with no published end date; Pro from $100/mo. Also reported: "Signing in with a ChatGPT plan needs a human in the terminal once for the device code (the fully headless path is an API key)" and "a Plus login on an always-on instance is still a Plus login, so unattended, high-volume work belongs on an API key."

UNKNOWN: whether OpenAI's Terms of Use contain an automated-access prohibition equivalent to Anthropic's, and whether Codex cloud has recurring scheduled runs today (ChatGPT "Tasks"/"Automations" exist for chat; I could not confirm they drive Codex). `AGENTS.md` is OpenAI's convention and is VERIFIED as an open format (`github.com/openai/agents.md`) — this repo already uses it, which is the right bet regardless.

**Verdict — OpenAI: GREY.** No vendor text was reachable today that either blesses or forbids scheduled unattended `codex exec` on a ChatGPT plan. Treat as: fine for a human-adjacent second opinion, not the load-bearing scheduler; if a department must run on Codex unattended, put it on an OpenAI API key.

---

## 4. xAI

UNKNOWN. `x.ai`, `docs.x.ai`, `console.x.ai` are all blocked from this session and the search budget was gone before I could substitute secondary sources. I therefore cannot quote SuperGrok's terms, Grok Build's terms, Grok bot/routine limits, MCP support, or xAI API prices today.

What is VERIFIED from inside this repo (`runtimes/grok-bot/`): the pilot already assumes Grok bots have **routines (scheduled runs)** and **Bring-Your-Own-MCP connectors**, that all bots on one account **share one cloud computer**, and it records: *"xAI's Grok Build client was found in July 2026 uploading repositories including secret files."* The pilot is correctly scoped to **T0 only, read-only DataDoe key, deploy key limited to this repo, no Ads/SP-API/QuickBooks/Keepa secrets.**

**Verdict — xAI: GREY, and the security posture already in the repo is the right one.** Because the scheduling is xAI's own first-party feature sold on the subscription, "unattended" is not the problem; **credential exposure on a shared cloud computer** is. Keep it at T0 and keep every secret off it.

---

## 5. Google

VERIFIED (`raw.githubusercontent.com/google-gemini/gemini-cli/main/README.md`, 2026-09-06): Apache-2.0; MCP servers configured in `~/.gemini/settings.json`; context file is `GEMINI.md`; **non-interactive mode** is `gemini -p "..."` with `--output-format json`; "Run non-interactively in scripts for workflow automation" is an advertised use. Auth options: **Sign in with Google** (OAuth; "Free tier: 60 requests/min and 1,000 requests/day", governed by the Gemini Code Assist licence and the quotas page), **Gemini API key** (1,000 requests/day free tier), **Vertex AI**.

UNKNOWN: `cloud.google.com/gemini/docs/quotas` 301s to `docs.cloud.google.com`, which is blocked — so the Code Assist quota table and any automation clause could not be read. Google AI Pro/Ultra subscription entitlements for Gemini CLI, and Antigravity, are likewise unverified today.

**Verdict — Google: GREY on the subscription/OAuth path, unambiguous on the API-key path.** Gemini is not needed for this design; skip it rather than research it further.

---

## 6. monday.com as a harness

Queried live through the monday MCP server on 2026-09-06. **VERIFIED:**

- **Account**: tier `pro`, product `core`, **2 active members**, not in trial.
- **Agent triggers**: 18 trigger types are programmatically attachable. One of them is **`Every time period` (block_reference_id 10380125)** — "Configure recurring trigger, based on cron config", schema `{ type: Daily|Weekly|Monthly, occurrences, hour, minute, timezone: IANA string, days[] }`. So **yes, a monday agent can run on a schedule, in Asia/Jerusalem.** Other triggers are board events (item/subitem created, status change, column change, form submitted, button clicked, item moved, board created, user joined, Notetaker meeting ended, Teams button clicked). The catalog note is explicit that **OAuth/3rd-party triggers (Slack, Gmail, Salesforce) cannot be added programmatically** and need UI setup.
- **Agent skills**: exactly **11** in the account catalog — Project risk insights, Social post creator, HTML Email builder, Rewrite and refine, Meeting actions, Weekly team digest, Executive summary, Feedback insights, Smart web research, Duplicate finder, Format monday updates. **None of them calls an external MCP server or an arbitrary webhook.**
- **AI credits**: one-time trial of **6,000 credits for non-Enterprise plans** (12,000 Enterprise); after that you buy an AI credits add-on; usage tracked at Administration → Usage stats → AI. Repeating AI on the same item is charged once.
- **Direction of MCP**: monday's own FAQ says external agents (ChatGPT, Claude, Copilot) "consume monday context and will be able to **activate the monday agents** using the MCP protocol" — i.e. **monday is an MCP server, not an MCP client**. Whether a monday agent can call *out* to an external MCP server is **UNKNOWN** (the developer-docs query hit a 429 rate limit; retry later).
- **Model**: **UNKNOWN.** monday does not disclose the underlying model in its knowledge base.

**Verdict — monday.com: keep it as the management surface, not as a harness.** It can schedule, but its agents cannot reach DataDoe or the Amazon Ads MCP, cannot read the repo, run on an opaque model, and burn a finite credit pool with no published per-plan allowance. Use monday exactly as `_CONTEXT.md` intends: boards, the daily ranked decision list, and approvals — driven *from* the repo by a department that calls the monday MCP as a client.

---

## 7. Orchestrators and schedulers for a zero-maintenance Mac mini

| Option | Maintenance | Portability | Failure notification | Legality with a subscription | Verdict |
|---|---|---|---|---|---|
| **macOS `launchd` (LaunchAgent, `StartCalendarInterval`)** | Lowest. Built in, no service to update. | Total — it just runs `claude -p`. | None built in; you write a wrapper that posts on non-zero exit. | Fine — it is you running your own binary. | **Primary scheduler.** |
| `cron` on macOS | Low, but deprecated on macOS and needs Full Disk Access grants; no Keychain session. | Total. | None. | Fine. | Fallback only. |
| **Claude Code Routines** (cloud) | Zero. Anthropic-managed. | Low — Anthropic-only, research preview, "behavior, limits, and the API surface may change". No local files (fresh git clone), min 1h, daily run cap. | Run list + session transcripts; a green status "does not mean the task succeeded". | Explicitly ALLOWED on Max. | **Backup runner** for the daily brief when the Mac is down. Never load-bearing. |
| **Claude Code Desktop scheduled tasks** | Low, but requires the app open and the machine awake; sleeps skip runs. | Low — Anthropic-only. | Desktop notifications; skipped-run history with reasons. | ALLOWED. | Useful for Rami's own laptop, not for the always-on box. |
| Codex scheduled runs | UNKNOWN (docs unreachable). | Low. | UNKNOWN. | GREY. | Do not depend on it. |
| **Paperclip** (`paperclipai`) | Medium. **VERIFIED npm**: MIT, created 2026-03-03, latest `2026.831.1` published 2026-09-02, canary `2026.906.0` today, Node ≥24.11, "orchestrate AI agent teams to run a business". Ships adapters `claude_local` / `codex_local` that shell out to the **host CLI login** — which lands inside Anthropic's "unmodified Claude Code binary with their own Claude subscription" carve-out. | Medium — agents defined as JSON in this repo (`runtimes/paperclip/agents/*.json`), so re-hiring is minutes. Embedded Postgres is the state you'd lose. | Per-agent budgets and pause-on-overspend; audit log export. | **GREY-to-ALLOWED**: it launches the unmodified binary rather than brokering the token, which is the permitted shape. It is six months old and shipping nightly. | **Adopt with a hard rule: Paperclip may launch the CLI, never hold a Claude credential.** |
| **OpenClaw** | Medium. **VERIFIED npm**: MIT, `2026.9.2` published 2026-09-05; gateway + channels (WhatsApp/Telegram/Slack/Signal/iMessage). | Medium. | Gateway dashboard. | **REPORTED: Anthropic blocked OpenClaw from individual Claude subscriptions around 2026-04-05.** Unverified but plausible given the "may not ... intermediate Claude.ai credentials" clause. | **Avoid on the Claude subscription.** Fine as a messaging gateway on API keys. |
| **n8n** (self-hosted) | Medium-high: Docker, Postgres, upgrades. **VERIFIED npm**: `2.37.10`, 2026-09-04, "SEE LICENSE IN LICENSE.md" (Sustainable Use Licence — internal business use OK, resale not). | Medium — workflows are JSON, not files in this repo. | Built-in error workflows and retries. | Only if it calls an API key, not a subscription. | Skip. It adds a second source of truth outside the repo, which violates §2 of the constitution. |
| **Trigger.dev** (`@trigger.dev/sdk` 4.5.16, MIT, 2026-09-02) / **Inngest** (`inngest` 4.20.0, Apache-2.0, 2026-09-04) | Medium. Cloud control planes; you write TypeScript. | Low-medium — vendor SDK in your code. | Excellent (retries, alerting, replay). | Only with API keys. | Overkill for 27 runs/day. Revisit at 10 brands. |
| **GitHub Actions cron** | Low. Free minutes on public repos; paid on private. | High — YAML in this repo. | Email/webhook on workflow failure, free. | **ALLOWED with a subscription**: `claude_code_oauth_token` is Anthropic-documented (§2.2). Note GitHub's own caveat that scheduled workflows are best-effort and can be delayed or disabled after 60 days of repo inactivity (REPORTED, docs.github.com blocked). | **Adopt as the second scheduler** — it is the failure-notification layer the Mac mini lacks. |
| **Temporal Cloud** | High conceptually, low operationally. | Low (workflow code). | Excellent. | API keys only. | No. Wrong scale. |

---

## 8. Harness-portable agent definitions

### 8.1 What is portable today

| Artifact | Claude Code | Codex CLI | Gemini CLI | Portable? |
|---|---|---|---|---|
| Charter / constitution | `CLAUDE.md` (this repo already `@AGENTS.md` from it) | `AGENTS.md` | `GEMINI.md` | **Yes** — one `AGENTS.md`, one-line include files per harness. Already done here. |
| Procedure as a skill | `SKILL.md` (`name`, `description`, `disable-model-invocation`, `allowed-tools`, `context: fork`) | plain markdown referenced from `AGENTS.md` | plain markdown | **Mostly.** The Agent Skills folder format (`SKILL.md` + resources) is the closest thing to a standard; Anthropic points at **agentskills.io** for the spec and keeps the spec in `github.com/anthropics/skills/spec` (VERIFIED). Frontmatter fields are Claude-specific — keep them minimal. |
| Tool list | `.mcp.json` (`mcpServers`, `type: http\|sse\|ws\|stdio`) | `config.toml` | `~/.gemini/settings.json` | **Structurally yes** — same server list, three encodings. Generate all three from one source file. |
| Memory | `memory/MEMORY.md` + dated observation files (this repo's own convention) | same files | same files | **Yes, because you made memory a file.** Claude Code's *auto memory* is not portable — do not depend on it. |
| Subagents | `.claude/agents/*.md` | ✗ | ✗ | **No.** |
| Hooks | `settings.json` hook events | Codex lifecycle hooks (different schema) | ✗ | **No.** |
| Scheduling | Routines / Desktop tasks / `/loop` | ? | ✗ | **No.** Keep scheduling outside the harness — that is what launchd is for. |
| Channels / cross-session messaging / agent teams | Claude-only, research preview | ✗ | ✗ | **No.** |

**Rule to adopt:** a department is `AGENTS.md` + `SKILL.md` files + `.mcp.json` + `memory/` + `state/`. Anything a harness offers beyond reading files and calling MCP tools is a convenience, never a dependency. The thin adapter per runtime is a single shell script that (a) exports the right credential, (b) renders the MCP list into the harness's format, (c) invokes the harness's headless entry point with the run prompt. `runtimes/*/RUN.md` already encodes exactly this — keep it.

### 8.2 State of the protocols

- **MCP**: **VERIFIED** — `LATEST_PROTOCOL_VERSION = "2026-07-28"` in `schema/2026-07-28/schema.ts` on `modelcontextprotocol/modelcontextprotocol@main` (read today). Client capabilities in that schema include **`sampling`** (with tool-use support) and **`elicitation`** (with **form and URL modes**; URL elicitation carried error code `-32042` in the 2025-11-25 revision). Remote transports in Claude Code today: **streamable HTTP** (with OAuth), **SSE**, **WebSocket** (header auth only — "HTTP supports OAuth and the `claude mcp add --transport` flag, while WebSocket supports neither"), and local **stdio**. Project scope is a committed `.mcp.json`; `${VAR}` expansion works, with a caveat that `${CLAUDE_PROJECT_DIR}` needs a default in project scope.
- **A2A**: **VERIFIED alive** — `a2aproject/A2A` on GitHub, Apache-2.0, a2a-sdk on PyPI: "an open protocol enabling communication and interoperability between opaque agentic applications ... discover each other's capabilities ... securely collaborate on long-running tasks ... without exposing their internal state, memory, or tools." I could not read a version number today. **Not needed for this design.** Departments here communicate through files in git, which is stricter, auditable forever, and free. Revisit only if a second brand runs on separate infrastructure.
- **AGENTS.md**: **VERIFIED** open format, `github.com/openai/agents.md` — "a README for agents". Zero lock-in.

---

## 9. Cost model

**VERIFIED API prices** (`platform.claude.com/docs/en/about-claude/pricing`, 2026-09-06, per million tokens):

| Model | Input | Cache write (5m) | Cache read | Output |
|---|---|---|---|---|
| Opus 5 | $5 | $6.25 | $0.50 | $25 |
| Sonnet 5 | $2 | $2.50 | $0.20 | $10 |
| Haiku 4.5 | $1 | $1.25 | $0.10 | $5 |

Batch API is **50% off** both directions. Note also VERIFIED: Claude 4.7-and-later models use a tokenizer producing **~30% more tokens for the same text**, so cost comparisons against older models understate.

**Workload.** 9 departments × 1-3 runs/day ≈ **540-810 runs/month**. A department run is: read constitution + charter + memory + 3-5 state files (~40-60k tokens, almost all cacheable), 5-15 MCP tool calls returning data, write a state file and 0-2 proposals (~8-20k output). Realistic per-run cost on **Sonnet 5** with caching working: **$0.15-0.60**. On **Opus 5**: **$0.40-1.50**.

| Scenario | Monthly |
|---|---|
| All departments on Sonnet 5 via API, 2 runs/day | **~$160-330** |
| Mixed (Opus 5 for Chief of Staff + Finance + Pricing, Sonnet 5 for the rest), 2 runs/day | **~$250-450** |
| All Opus 5, 3 runs/day | **~$700-1,200** |
| Max 20x subscription (REPORTED ~$200/mo) covering the same work | **$200 flat**, plus your interactive use, subject to 5-hour and weekly windows |

**Subscription stack (REPORTED prices, re-verify):** Max 20x ~$200 + ChatGPT Pro ~$100 + SuperGrok ~$30 + monday Pro 2 seats ~$40-60 = **~$370-390/month** for all three harnesses and the management surface.

**Conclusion.** For this workload the Max 20x subscription is the cheapest correct answer and has a large margin: 540 runs/month is roughly 125/week, which at 5-15 minutes of model time each is 10-30 hours/week against a reported 240-480 weekly Sonnet hours. **API credits become necessary, not cheaper, in three cases:** (1) a burst that would starve Rami's interactive work inside a 5-hour window; (2) anything a third party operates or that holds the credential in a way the §2 clauses forbid; (3) a second brand — a separate brand is a separate business, so give it a separate API key rather than stretching "ordinary, individual usage". Budget **$50/month of API credits as the overflow lane** and turn on usage credits with a monthly spend limit so a runaway loop cannot become a $900 surprise.

---

## 10. Recommendation

### 10.1 Harness per department

| Department | Default harness | Why | Fallback 1 | Fallback 2 |
|---|---|---|---|---|
| Chief of Staff | Claude Code headless (Max) | Needs the whole repo, cross-department reads, meeting minutes | Claude Code Routine (cloud) | Codex CLI on API key |
| Finance | Claude Code headless | QuickBooks MCP + numbers discipline | Codex CLI (API key) | — |
| Supply chain | Claude Code headless | DataDoe + Freightos MCP | Grok bot (T0 read-only) | — |
| Advertising | Claude Code headless | **Only** T1 department; needs the official Amazon Ads MCP and the ledger | none — advertising never runs on a harness that cannot write `ledger/actions.jsonl` | — |
| Catalog | Claude Code headless | Long text, image/listing proposals | Codex CLI | — |
| Pricing & market intel | Claude Code headless | Keepa + SP-API pricing data | Grok bot (T0) | — |
| Customer | Claude Code headless | Buyer-message drafts are T2 | Codex CLI | — |
| Account health & compliance | Claude Code headless | Reads only; must never touch a browser | Grok bot (T0) | Routine |
| Expansion | Codex CLI (second opinion) or Claude Code | Research-shaped, benefits from a different model | Claude Code | — |

**Fallback order, one line:** *Claude Code on Max (local, launchd) → Claude Code Routine (cloud) → Claude Code on API key → Codex CLI on API key → stop and tell Rami.* Never fall back to a browser, ever (BSA §19). Never fall back to a harness that holds a secret it is not entitled to.

### 10.2 Scheduler

**launchd LaunchAgents on the Mac mini, plus a GitHub Actions cron as the watchdog.** Two schedulers, different failure modes, both free.

- launchd runs the departments at their `docs/CALENDAR.md` slots (Asia/Jerusalem), with `StartCalendarInterval`.
- A single GitHub Actions workflow runs once daily at 09:00 Asia/Jerusalem, pulls the repo, and checks that **every `state/*.md` carries today's date**. If any is stale it opens an issue and emails Rami. That is the dead-man's switch the constitution's §6.6 already implies ("A stale state file is treated as a failed run") but nothing currently enforces.
- Paperclip may sit on top as the agent-team surface, but it launches the CLI; it does not become the scheduler of record and it never holds a Claude credential.

### 10.3 Mac mini layout

1. **Users.** One standard (non-admin) user `ops`. Rami's own account is separate. Enable auto-login for `ops` so LaunchAgents run in a real GUI session (a `LaunchDaemon` runs as root with no login keychain and will fail Claude Code's credential read).
2. **Credentials.** Do **not** rely on the Keychain for unattended runs. Run `claude setup-token` once as `ops`, store the one-year token in the vault (1Password/Infisical), and have each run wrapper export `CLAUDE_CODE_OAUTH_TOKEN` from `op run --env-file=...` at launch. Same pattern for MCP secrets, which `.mcp.json` already references as `${NAME}`. Nothing secret is ever written into the repo (constitution §6.3). Set a calendar reminder **11 months out** to re-mint the token; Claude Code warns 3 days before a login expires, which is useless to an unattended job.
3. **No `--bare`.** Bare mode ignores both the OAuth token and the Keychain and skips `.mcp.json` and `CLAUDE.md` — it would silently run a department with no charter and no tools.
4. **Sleep.** `sudo pmset -a sleep 0 disablesleep 1` and `caffeinate -dimsu` under launchd; Desktop scheduled tasks and launchd jobs both skip when the machine sleeps.
5. **Clones.** One clone per department (`~/ops/wt/<dept>`), as the Grok pilot already established — unstaged changes in a shared clone block every other department's pull.
6. **Logs.** `~/ops/logs/<dept>/YYYY-MM-DD.log`, one file per run, plus a weekly launchd job that deletes anything older than 90 days and `gzip`s the rest. Do not use `newsyslog` — it is one more thing to maintain.
7. **Watchdog + notification.** Every department run goes through `~/ops/bin/run-dept.sh <dept>`, which: acquires a per-department `flock`, times out at 20 minutes, tees to the log, and on non-zero exit or timeout posts one line to Rami's Telegram and writes `FAILED <dept> <date>: <error>` into `state/<dept>.md`. This matches the existing `CHATS.md` alert protocol so the same discipline holds on both runtimes.
8. **Ledger.** `ledger/actions.jsonl` is append-only and committed every run; commit message `<dept>: <date> run` per §7.10.

### 10.4 Exit path from each vendor, in days

| Vendor | What you lose | Exit |
|---|---|---|
| **Anthropic (Max)** | Routines, Desktop tasks, Channels, connectors. **Not** the departments — they are files. | Cancel at period end. Delete `CLAUDE_CODE_OAUTH_TOKEN` from the vault. Set `ANTHROPIC_API_KEY` in the same wrapper and every launchd job keeps running unchanged. **Same day.** Precondition: never put a load-bearing schedule in Routines. |
| **OpenAI (ChatGPT)** | Codex second opinions. | Cancel; `codex` runs on an OpenAI API key with the same `AGENTS.md`. **Same day.** |
| **xAI (SuperGrok)** | The T0 pilot bots. | Delete the bots, revoke the DataDoe bot key, revoke the deploy key. Departments move to launchd. **1 day.** |
| **monday.com** | Boards, the decision list. | The record is the repo (§8), so export boards to CSV via the monday API for archive and stop paying. **2 days.** |
| **Paperclip** | Agent-team UI, budgets, audit log. | MIT, local embedded Postgres. Agents are JSON in `runtimes/paperclip/agents/`; export the audit log to `ledger/`, stop the service, run launchd directly. **1 day.** |
| **DataDoe** | Amazon read layer — **the real lock-in**, since there is no SP-API registration yet. | No same-week exit. This is the single-vendor risk in the whole design; SP-API developer registration is the mitigation and should be started now, not at US launch. |

---

## Implications for the design

1. **The legal question resolves in your favour, but only for the shape you already chose.** Anthropic's own compliance page permits an end user signing in to the unmodified Claude Code binary with their own subscription, and documents subscription OAuth tokens for CI. What it forbids is a *product* holding your credential. So: launchd calling `claude -p` is clean; Paperclip calling `claude -p` is clean; any orchestrator that stores or forwards a Claude OAuth token is not. Write that as a one-line rule in `AGENTS.md` §6 — it is currently missing.
2. **Delete "unattended" from the risk register and replace it with "ordinary, individual".** The enforcement surface is scale and sharing, not automation. Nine departments for one operator is fine. The second brand needs its own API key, and that changes the cost model for brand #2 by roughly $200-400/month, not $0. Plan for it now.
3. **Keep every scheduler outside every harness.** Routines are a research preview whose "behavior, limits, and the API surface may change", capped at 1 hour and a daily run allowance; Desktop tasks need an open app and an awake machine; `/loop` dies with the session. launchd + a GitHub Actions dead-man's switch costs nothing and survives all three changing.
4. **The constitution says a stale state file is a failed run but nothing checks.** Ship the GitHub Actions staleness check before adding any new department. It is 30 lines of YAML and it is the difference between a company and a cron job that quietly stopped in March.
5. **Ban the Chrome extension on the ops machine explicitly.** Claude in Chrome "shares your browser's login state, so it can access any site you're already signed into." That is a one-click BSA §19 violation waiting to happen on a machine that has Seller Central cookies. Add it to §6.1.
6. **monday is a client, not a harness.** Its agents can schedule but cannot reach DataDoe or the Ads MCP, run on an undisclosed model, and spend a 6,000-credit one-time pool. Drive monday from the repo via its MCP server; do not move any department onto it.
7. **Budget the API overflow lane at ~$50/month and turn on usage credits with a spend limit.** Subscriptions first is right; a hard wall in hour 4 of a 5-hour window on the morning of a stockout is not.

## Open questions

1. **The Consumer Terms clause itself.** Someone must open `anthropic.com/legal/consumer-terms` and `anthropic.com/legal/aup` on an unrestricted browser and paste the automated-access clause verbatim into this file, with its effective date. Everything in §2 hangs on the interaction between that clause and the "or where explicitly permitted" carve-out.
2. **Whether Anthropic's April 2026 enforcement action against third-party agents extends to a locally-installed orchestrator like Paperclip that shells out to the unmodified binary.** The legal page's wording says no. Confirm with Anthropic sales before Paperclip becomes the primary runner.
3. **OpenAI's terms on unattended Codex on a ChatGPT plan** — `developers.openai.com/codex/*` and `help.openai.com` must be read directly. Also: does Codex cloud have recurring scheduled runs today?
4. **xAI's terms, Grok bot limits, and the July 2026 Grok Build repository-upload incident.** The repo asserts the incident; it needs a citation before it is quoted to anyone outside.
5. **Can a monday agent call an external MCP server or a webhook?** The developer-docs query hit a 429; retry. If the answer is yes, monday becomes a viable T0 harness and the design simplifies.
6. **Max 20x's actual weekly caps after 2026-09-14**, when the temporary boost settles at a reported +25%. Re-run the cost model against the real number once `/usage` shows it on the Mac mini.
7. **SP-API developer registration timeline.** DataDoe is the only Amazon access and the only vendor with no same-week exit. Everything else in this document is reversible in a day; that one is not.
