# monday.com as the management surface for a company of AI agents

Research date: **2026-09-06**. Researcher: Claude (agent). Account context: Anabtawi account is on **monday Work Management, Pro tier, 2 active members** (VERIFIED — `get_user_context` via the official monday MCP server returned `{"tier":"pro","active_members_count":2,"products":[{"kind":"core","tier":"pro"}]}`).

## Method and how to read the tags

**Important constraint on this research run:** this session's network egress policy **blocks every `*.monday.com` domain** (`monday.com`, `developer.monday.com`, `support.monday.com` all returned `EGRESS_BLOCKED`). I could not open monday's own pages in a browser-equivalent fetch, and the session's web-search budget was exhausted partway through.

Everything below therefore comes from one of three places:

1. **monday's own knowledge bases, read through the official monday MCP server** — `get_monday_knowledge(kind:"general")` returns verbatim snippets from support.monday.com articles with URLs; `get_monday_knowledge(kind:"developer_docs")` returns answers with deep links into developer.monday.com. These are monday's primary documentation, retrieved today through monday's own retrieval service. I tag these **VERIFIED** and give the article URL, with the caveat that I read the snippet monday returned rather than the rendered page.
2. **Direct introspection of the live account** — `get_user_context`, `get_graphql_schema`, `get_type_details`, `all_widgets_schema`, `agent_catalog`. This is the strongest evidence available: it is the API answering about itself. Tagged **VERIFIED (live introspection)**.
3. **Third-party sources** (pricing blogs, analyst posts) reached by web search. Tagged **REPORTED**.

Anything I could not pin down is tagged **UNKNOWN** with a note on what I tried. No monday account was created, modified or deleted; only read-only tools were called.

Prices are USD, as of 2026-09-06, and monday changes them — re-check before committing.

---

## 1. Boards, columns, views, structure

### Item and board limits

| Limit | Value | Tag | Source |
|---|---|---|---|
| Items per board, Free/Basic/Standard/Pro | **10,000** | VERIFIED | [Item and subitem limits per board](https://support.monday.com/hc/en-us/articles/4404058746642-Item-and-subitem-limits-per-board) |
| Items per board, Enterprise | **100,000** | VERIFIED | same |
| Items per account, Free plan | 200 items, +100 per referral; 2 seats; 3 boards total | VERIFIED | [Understanding the Free Plan](https://support.monday.com/hc/en-us/articles/360010487220-Understanding-the-Free-Plan) / [Available plan types on Work Management](https://support.monday.com/hc/en-us/articles/115005320209-Available-plan-types-on-Work-Management) |
| Items per account, Basic and up | Unlimited ("Unlimited items" from Basic) | VERIFIED | Work Management plan article |
| Archived/deleted items count toward limits | **No** | VERIFIED | Free Plan article |
| Boards per account | No documented cap on paid plans | UNKNOWN | asked the KB directly; not covered |
| Columns per board | monday CRM Pro article mentions "75 columns per board"; no Work Management figure found | UNKNOWN | KB returned no Work Management column cap |

For ~60 SKUs with a few hundred rows of daily metrics, **10,000 items per board is the binding number, not 100,000.** A "SKU × day × metric" board would blow through 10k in weeks. Design implication in §13.

### Connect Boards (board relations) and mirror/lookup

| Limit | Basic | Standard | Pro | Enterprise | Tag |
|---|---|---|---|---|---|
| Different boards connectable to one board | 1 | 5 | **20** | 200 (max 60 per column) | VERIFIED |
| Connected items (linkages) per board | 10,000 | 10,000 | 10,000 | 100,000 | VERIFIED |
| Connected items per cell | 750 | 750 | 750 | 750 | VERIFIED |

Source: [Linkage limitations for the Connect Boards Column](https://support.monday.com/hc/en-us/articles/360021743500-Linkage-limitations-for-the-Connect-Boards-Column) (VERIFIED).

**Pro's 20-connected-boards ceiling is a real architectural constraint** for a hub-and-spoke design where one "SKU master" board is connected to finance, supply, ads, catalog, pricing, customer, compliance boards plus their sub-boards.

### Columns

The full column type list is enumerable from the API (VERIFIED, live introspection via `get_column_type_info` enum): `auto_number, board_relation, button, checkbox, color_picker, country, creation_log, date, dependency, direct_doc, doc, dropdown, email, file, formula, group, hour, integration, item_assignees, item_id, last_updated, link, location, long_text, mirror, name, numbers, people, phone, progress, rating, status, subtasks, tags, team, text, time_tracking, timeline, unsupported, vote, week, world_clock`.

Plan gating (VERIFIED, [Work Management plan article](https://support.monday.com/hc/en-us/articles/115005320209-Available-plan-types-on-Work-Management)):
- **Free and Basic**: "Limited Column Center — most columns available *except* the Formula Column and the Time Tracking Column."
- **Standard**: same exclusion — Formula and Time Tracking still excluded (VERIFIED for monday service; the Work Management article words it as "limited column center" on Free/Basic and "full access to the column center" from Pro).
- **Pro and up**: "Full access to the column center. This includes the Time Tracking Column, the Formula Column, and all AI-powered columns," plus the **Tags column** and **Dependencies**.
- **Dependency column**: documented as a Pro-plan feature (VERIFIED for monday service; Work Management wording puts Dependencies in the same Pro bullet list).

**Formula column is Pro-and-up. That matters:** the whole "computed contribution margin" idea sits behind Pro.

### Views

| View | Plan | Tag |
|---|---|---|
| Table (main), Kanban, Files, Forms | Free and up | VERIFIED |
| Calendar, Timeline (Gantt-style), Map | Standard and up | VERIFIED |
| **Chart view**, **Workload view** | **Pro and up** ("full access to the views center... as well as the amazing chart view") | VERIFIED |

Source: Work Management / CRM / service plan articles (VERIFIED).

### Groups, subitems, board templates and duplication

- Subitems exist and appear in Kanban; **no documented cap on subitems per item** (UNKNOWN — asked the KB, not covered; the article title is "Item and subitem limits per board" and only gives the per-board figure, which subitems count against).
- **Save board as template** and **save an entire workspace as a template** are both supported from the UI. Workspace templates carry boards, docs, WorkForms and dashboards together, but **only Main boards** — Private and Shareable boards are not carried over (VERIFIED — [The Template Editor](https://support.monday.com/hc/en-us/articles/19105791772690-The-Template-Editor), [Workspace settings and customization](https://support.monday.com/hc/en-us/articles/28869384701586-Workspace-settings-and-customization)).
- **Managed Templates** (governed, centrally updatable) are **Enterprise-only beta** (VERIFIED — Template Editor article).
- API: `duplicate_board`, `duplicate_group`, `duplicate_item`, `duplicate_doc`, `duplicate_view` and **`use_template`** all exist as mutations (VERIFIED, live introspection of the mutation schema).
- **Caveat that matters for second-brand instantiation:** the mondayDB 2.0 article states that on the new engine "while you can duplicate the *structure* of a board, duplicating a board or column **with values** is not currently supported" (VERIFIED — [mondayDB 2.0](https://support.monday.com/hc/en-us/articles/20705455822354-mondayDB-2-0)). It also says the Auto Number column is unsupported and you cannot change an existing column's type. Structure-only duplication is actually what you want for a second brand — but verify against your own boards before relying on it.

Rate limit on duplication: **create_board / duplicate_board / duplicate_group are capped at 40 mutations per minute** (VERIFIED, developer docs via MCP).

---

## 2. monday workdocs

| Capability | Status | Tag |
|---|---|---|
| Create doc in a workspace or on an item (Doc column) | Yes; `create_doc` mutation with `location: {workspace:{...}}` or `{board:{item_id, column_id}}` | VERIFIED (dev docs + mutation schema) |
| Write content programmatically | `add_content_to_doc_from_markdown`, `import_doc_from_html`, `create_doc_block(s)`, `update_doc_block`, `update_doc_name` | VERIFIED (live mutation schema) |
| Read doc content and blocks | `docs(ids/object_ids/workspace_ids, include_blocks:true)`; blocks have `id, type, parent_block_id, position, content` (delta format) | VERIFIED (dev docs) |
| **Export doc as markdown via API** | `export_markdown_from_doc` query exists — "Converts document content into standard markdown format for external use, backup, or processing… whole document by default, or specific blocks" | **VERIFIED (live introspection)** |
| **Version history via API** | `doc_version_history` and `doc_version_diff` queries exist; MCP `read_docs` supports `mode:"version_history"` with `include_diff` | **VERIFIED (live introspection + dev docs)** |
| Embed a board / widget / another doc inside a doc | Block types `BOARD`, `WIDGET`, `DOC` embed, `GIPHY` exist, but **can only be created and deleted, never updated in place** | VERIFIED (dev docs) |
| Turn doc text into board items | Highlight text → "+ item" → choose board and group | VERIFIED ([Integrate workdocs into your workflow](https://support.monday.com/hc/en-us/articles/24108289323282-Integrate-workdocs-into-your-workflow)) |
| Docs included in full account export | **No** — "Archived boards and workdocs are not supported when exporting the account data… export your workdocs as a PDF before exporting" | VERIFIED ([How to export your entire account's data](https://support.monday.com/hc/en-us/articles/360002543719-How-to-export-your-entire-account-s-data)) |
| Required scope for doc writes | `docs:write` | VERIFIED (dev docs) |
| Plan gating for workdocs | No plan gate found in the docs | UNKNOWN |

**This is the single most useful finding for a knowledge-layer design.** Docs are fully round-trippable through the API — markdown in, markdown out, with version history and diffs. A monday doc can mirror a repo file both ways.

---

## 3. Dashboards and widgets

| Limit | Free | Basic | Standard | Pro | Enterprise | Tag |
|---|---|---|---|---|---|---|
| Boards per dashboard | 1 | 1 | 5 | **20** | 50 | VERIFIED |
| Dashboards per account | Unlimited (CRM Pro caps at 50 custom dashboards) | | | | | VERIFIED |
| Widgets per dashboard | **30** (text widgets excluded from the count) | | | | | VERIFIED |
| Items across all connected boards per dashboard | **20,000** hard cap; you get prompted to disconnect boards above it | | | | | VERIFIED |
| Enterprise mondayDB 2.0 raise | Chart / Battery / Numbers widgets up to **500,000** items per dashboard; **Gantt, Timeline, Workload and Table widgets stay at 20,000** | | | | Ent | VERIFIED |
| Textual search in dashboards | Not supported | | | | | VERIFIED |

Sources: [The Dashboards](https://support.monday.com/hc/en-us/articles/360002187819-The-Dashboards), [mondayDB 2.0](https://support.monday.com/hc/en-us/articles/20705455822354-mondayDB-2-0) (both VERIFIED). Plan articles say "15 available widgets" across tiers.

**Widget types creatable through the API/MCP** (VERIFIED, live introspection via `all_widgets_schema`) are a narrower set than the UI offers: `CHART`, `NUMBER` (counter), `BATTERY`, `CALENDAR`, `GANTT` (timeline), `LISTVIEW`, `APP_FEATURE` (embed a monday app, including a Vibe app). The chart widget supports pie, donut, column, bar, area, line, smooth_line, bubbles and all the stacked/percent-stacked variants, with x/y/z axis column mapping, `calc_function_type` of sum/average/min/max/count, and date grouping by day/week/month/quarter/year.

**Mobile rendering:** dashboards *are* viewable on mobile (VERIFIED — [Basic reporting](https://support.monday.com/hc/en-us/articles/360013878299-Basic-reporting-with-monday-com)), but **Gantt, Workload, Chart and "Default" board views are browser-only** (VERIFIED — [Mobile app board views](https://support.monday.com/hc/en-us/articles/360015740220-Mobile-app-board-views)). So a chart *widget on a dashboard* renders on mobile, but a chart *view on a board* does not.

---

## 4. Automations, workflows and webhooks

### Action budgets — the number that decides the plan

| Plan | Automation actions / month | Integration actions / month | Tag |
|---|---|---|---|
| Free | none / not stated | none / not stated | UNKNOWN |
| Basic | not stated in the plan article | not stated | UNKNOWN |
| **Standard** | **250** | **250** | VERIFIED |
| **Pro** | **25,000** | **25,000** | VERIFIED |
| **Enterprise** | **250,000** | **250,000** | VERIFIED |

Sources: [Available plan types on Work Management](https://support.monday.com/hc/en-us/articles/115005320209-Available-plan-types-on-Work-Management), [monday dev](https://support.monday.com/hc/en-us/articles/26061127699730-Available-plan-types-on-monday-dev), [Automation and Integration actions](https://support.monday.com/hc/en-us/articles/360017556179-Automation-and-Integration-actions) (VERIFIED).

Accounting rules that bite (VERIFIED, Automation and Integration actions article):
- A custom template mixing automation and integration blocks charges **everything to the Automation bucket**.
- **Actions consumed by any monday app also charge the Automation bucket.**
- Standard's 250/month is a rounding error for an agent company. **Pro's 25,000/month is the realistic floor.**

Separately there are **per-minute rate limits** on automations and integrations — each recipe can only run so many triggers/actions per minute, and you are most likely to hit them "if you are using the API or webhooks to trigger your automations" or "use Batch Actions to trigger many automation recipes at once" (VERIFIED — [Automation and integration rate limits](https://support.monday.com/hc/en-us/articles/9060097050258-Automation-and-integration-rate-limits)). The exact numbers are not published (UNKNOWN).

### Scheduling

"**Every time period**" is a first-class trigger. Through the agent/workflow API it takes a `schedulerConfig` of shape `{type: "Daily"|"Weekly"|"Monthly", occurrences: 1-99, hour: 0-23, minute: 0-59, timezone: IANA string, days: int[]}` — and the tool's own example uses `"timezone": "Asia/Jerusalem"` (VERIFIED, live introspection via `agent_catalog(list_triggers)`, block_reference_id `10380125`). Date-based automations can run exactly on the date, on a recurring schedule, or at midnight after the date passed (VERIFIED — [Alerts and Reminders with Automations](https://support.monday.com/hc/en-us/articles/360000227739-Alerts-and-Reminders-with-Automations)).

### The full programmable trigger catalog

VERIFIED (live introspection, `agent_catalog(list_triggers)`) — 18 trigger types are addable programmatically: When item created / deleted / archived; When column changes; When status changes to something; When button clicked; When update created; When form is submitted; When item moves to board; When board created; When subitem created / deleted / archived / status changes; When user joined the account; **Every time period**; When Notetaker meeting ended; Wait for Microsoft Teams button clicked.

Explicit note in the tool output: **OAuth/third-party triggers (Slack, Gmail, Salesforce…) cannot be added programmatically and must be set up in the monday UI.** That is a real automation-of-automation limit.

### Outgoing webhooks

VERIFIED (dev docs). Created via UI (Automations → Integrations → webhooks app) or `create_webhook(board_id, url, event, config)` with scope `webhooks:write`. monday POSTs a `challenge` string on registration which your endpoint must echo back.

Supported events: `create_item, change_name, item_archived, item_deleted, item_moved_to_any_group, item_moved_to_specific_group, item_restored, change_column_value, change_specific_column_value, change_status_column_value, create_column, create_subitem, change_subitem_name, change_subitem_column_value, move_subitem, subitem_archived, subitem_deleted, create_update, edit_update, delete_update, create_subitem_update`.

Payload is a single `event` object: `userId, boardId, pulseId, pulseName, groupId, groupName, columnId, columnType, columnTitle, value, previousValue, changedAt, app, type, triggerTime, subscriptionId, triggerUuid, originalTriggerUuid` (+ `parentItemId`/`parentItemBoardId` for subitems). `originalTriggerUuid` is your loop-prevention hook.

### Workflows (the new builder)

- **Available on Pro and Enterprise plans** (VERIFIED — [The AI workflow builder: FAQs](https://support.monday.com/hc/en-us/articles/11378232387730-The-AI-workflow-builder-FAQs)).
- Visual canvas of blocks; unlike a board automation, a workflow is built **at the workspace level across multiple boards**, not scoped to one board (VERIFIED).
- Features include delayed starts, "get item from a previous step", subitem integration, duplicating workflows, change any column value, **create and duplicate board** blocks, push/set date blocks, and "the triggering user" (VERIFIED — [Get started with AI workflows](https://support.monday.com/hc/en-us/articles/11065311570066-Get-started-with-AI-workflows)).
- **AI blocks** usable in Workflow Builder, Automations and Columns: Custom AI Prompt, Assign Labels, Assign People, Suggest action items, Detect Sentiment, Detect language, Improve text, Prioritize, Summarize text, Write, Extract, Generate docs. **8 credits per action**, and all actions on the same item within 24 hours count once (VERIFIED — [AI Feature Catalog](https://support.monday.com/hc/en-us/articles/24047211522194-AI-Feature-Catalog)).
- MCP exposes `create_workflow`, `validate_workflow`, `publish_workflow`, `run_workflow_once`, `stop_workflow_run_once`, `get_workflow_run_once_status`, `invoke_workflow_expert`, `invoke_process_planner`, `list_automations`, `manage_automations`, `get_automation_runs`, `get_automation_statistics` (VERIFIED — tool list present in this session).

### Integration recipes worth knowing

Slack, Gmail, Outlook, Microsoft Teams, Google Calendar, Outlook Calendar, Excel, Google Drive, Dropbox, HubSpot, Pipedrive, Facebook Ads, GitHub, GitLab, CircleCI are all named in monday's own docs (VERIFIED, various plan/integration articles).

**QuickBooks: the QuickBooks integration is documented under "Unique features found only in monday CRM"** (VERIFIED — [Unique features found only in monday CRM](https://support.monday.com/hc/en-us/articles/8675571451282-Unique-features-found-only-in-monday-CRM)). On a Work Management–only Pro account it is very likely not available; buying a CRM product seat bundle would be required. Treat as a **blocker for "QuickBooks in monday"** until tested.

**Shopify**: a third-party "Shopify Integration" listing exists on the monday marketplace (REPORTED — marketplace listing surfaced in search; I could not open it because monday.com is egress-blocked). **Amazon Seller Central: no monday marketplace app found** (UNKNOWN/likely none) — which is consistent with the plan to keep Amazon access in DataDoe and push results into monday.

---

## 5. monday AI: sidekick, AI blocks, agents

### The pricing model

- **AI credits cost $0.01 each on yearly billing, $0.0125 on monthly** (25% uplift). CAD is listed at 0.01375 yearly / 0.0175 monthly; ILS at 0.0375 / 0.04625 (VERIFIED — AI Feature Catalog, currency table).
- Every account gets a **one-time trial of 6,000 credits (non-Enterprise) or 12,000 (Enterprise)**. After that you buy an AI credits add-on (VERIFIED — [AI Credits](https://support.monday.com/hc/en-us/articles/29544502265746-AI-Credits)).
- **AI features are not available on Free or non-paying NGO Pro accounts** (VERIFIED — AI Feature Catalog).
- Most AI block actions cost **8 credits**; a Vibe app triggering an integration costs **2 credits per integration trigger** (VERIFIED — [monday vibe: Permissions and Pricing](https://support.monday.com/hc/en-us/articles/32833842348178-monday-vibe-Permissions-and-Pricing); note the AI Credits article says "one AI credit" in one place and the Vibe article says two — monday's own docs disagree, flagged as a discrepancy).
- **monday MCP usage is listed as Free** in the AI Feature Catalog (VERIFIED). So driving monday from Claude Code costs no AI credits.
- REPORTED (third-party, could not verify against monday's pricing page because it is egress-blocked): monthly credit minimums of **1,000 (Basic) / 2,000 (Standard) / 3,000 (Pro)**, with Pro able to buy 3,000 / 4,000 / 8,000 / 20,000 per month; sidekick credit consumption starting 2026-05-20 and agent credit consumption starting 2026-06-08; accounts signing up from 2026-05-06 must buy credits alongside seats. **Verify on the pricing page before budgeting.**

### monday sidekick (the assistant)

VERIFIED — [Get started with monday sidekick](https://support.monday.com/hc/en-us/articles/26701503726610-Get-started-with-monday-sidekick):

| Tier | Included on | Limits |
|---|---|---|
| sidekick lite | Standard and Pro | **5 messages/actions per user per day**; single workspace context only |
| sidekick Plus | Included in Enterprise; purchasable on Standard/Pro | 100 messages/user/day, 2 generated images or videos/day, **account-wide context** |
| Super sidekick | "Coming soon", purchasable on Enterprise/Pro/Standard | 500 messages/user/day, 10 assets/day |

**Basic has no sidekick.** Sidekick is not supported on monday dev or monday CRM entity boards.

Capabilities: take actions (send Slack messages, tag teammates, update work), analyze board data, research the web, generate docs/images, **create, edit, update and delete items, groups, columns and labels**, read subitems, voice mode with readback/confirmation on impactful changes.

**5 messages/day on Pro is a toy.** Sidekick is not the automation surface; agents and the API are.

### monday agents (the "digital workforce")

VERIFIED — [Get started with the monday AI Agent builder](https://support.monday.com/hc/en-us/articles/33347027353746-Get-started-with-the-monday-AI-Agent-builder):

- **Availability: monday work management, "availability on all products coming soon". Currently in Gradual Release.** Admin permissions required to create or manage agents. Agents can be deactivated at any time.
- **"monday agents will be monetized in the future"** — the support doc states this explicitly and gives **no agent-seat price**. Agent seat pricing is therefore **UNKNOWN** from primary sources.
- Two flavours: **Expert Agents** (pre-built: CRM AI Lead Agent, CRM Sales Agent) and the **AI Agent builder** for custom agents.
- **Agent Factory** is a *separate, standalone product outside monday.com* — do not confuse it with the in-platform agent builder (VERIFIED).

**What a monday agent can actually do unattended** (VERIFIED, direct quotes from the article):
- *Understand context*: use boards, data, docs, workflows and permissions; "understand external context by connecting external files with specific knowledge."
- *Make decisions*: apply rules, priorities, tone and thresholds you define to triage, route, escalate, prioritize.
- *Take action*: **create and update items, assign owners, change statuses, draft messages, log outcomes, execute follow-ups.**
- *Operate within governance controls*: act only where permissions allow.
- *Run based on triggers*: on events, at defined times, or on an ongoing cadence — "agents will keep working even when you are asleep."

**What that list does NOT include: calling arbitrary external tools, moving money, or writing to a git repo.** The action surface is monday objects plus whatever connected integrations exist.

**Skills catalog** (VERIFIED, live introspection via `agent_catalog(list_skills)`) — 11 skills exist on this account today: Project risk insights, Social post creator, HTML Email builder, Rewrite and refine, Meeting actions, Weekly team digest (sends to Slack), Executive summary, Feedback insights, **Smart web research**, Duplicate finder, Format monday updates. Custom skills can be authored (`manage_agent_skills action:"create"`).

**Agent management via MCP**: `manage_agent`, `manage_agent_skills`, `manage_agent_knowledge`, `manage_agent_triggers`, `agent_catalog`, `connect_external_agent` (VERIFIED — tools present in this session).

### Connecting an EXTERNAL agent — the important part

VERIFIED (developer docs via MCP). The Agents API is **pre-release and requires the `API-Version: dev` request header**. Two connection modes:

1. **Managed provider** — e.g. a "Claude Managed Agent"; monday orchestrates the calls. Mutation: `connect_external_agent` (async).
2. **Custom agent via webhook** — you supply an HTTPS callback URL. Mutation: `connect_external_agent_sync(input:{custom:{name, callback_url}})`, which returns `agent_id`, `signing_secret`, `api_token`, `instructions`. **The secret and token are returned exactly once.** The mutation can take ~25 seconds.

Runtime contract:
- monday POSTs a signed `agent_triggered` event with headers `x-monday-agent-id`, `x-monday-signature`, `x-monday-timestamp`.
- Verify with **HMAC-SHA256 over `${timestamp}.${rawBody}`** using the signing secret.
- **Chat triggers**: hold the connection and reply with an SSE stream or JSON within ~30 seconds.
- **Mention / assignment triggers**: return HTTP 200 immediately, then use the agent's own `api_token` to write back to the board via GraphQL.

Once connected, an external agent is a **first-class entity: it can be assigned to items, @mentioned in updates, and interacts with boards** (VERIFIED).

**Protocols: this is monday's own signed-webhook protocol, not A2A.** I explicitly asked the developer-docs KB about A2A / agent-to-agent and it returned: "the provided knowledge sources do not mention an 'A2A protocol'." (VERIFIED that the docs do not mention it; whether monday supports A2A elsewhere is **UNKNOWN**.) **MCP is the other supported path** — the hosted Platform MCP server is explicitly framed as the way to connect "MCP-compatible external agent tooling (such as Cursor, Claude, or ChatGPT)".

**Agents get a bigger API budget: 20,000,000 complexity points per minute versus 5,000,000 for normal access** (VERIFIED, dev docs rate-limits table).

---

## 6. Developer platform

### Rate and complexity limits by plan

VERIFIED (developer docs via MCP, citing developer.monday.com/api-reference/docs/rate-limits and .../build-on-monday-with-ai#rate-limits):

| Limit | Free / Basic / Standard | Pro | Enterprise |
|---|---|---|---|
| Daily API calls (resets midnight UTC) | 1,000 | **10,000** | 25,000 |
| Queries per minute | 1,000 | 2,500 | 5,000 |
| Concurrency | 40 | 100 | 250 |
| IP rate | 5,000 req / 10s | same | same |
| Complexity points / minute | 5,000,000 | 5,000,000 | 5,000,000 |
| Complexity points / minute **for agents** | 20,000,000 | 20,000,000 | 20,000,000 |

Additional complexity rules (VERIFIED):
- A **single query cannot exceed 5,000,000 complexity points**.
- **App tokens**: 5M/min read and 5M/min write, separately.
- **Personal API tokens**: reads and writes share a **combined 10M/min** budget (1M for trial/NGO/free).
- API Playground: 5M each (1M on trial/free).
- Developer sandbox accounts: 10M.

Named per-minute mutation caps (VERIFIED):
- `create_board` / `duplicate_board` / `duplicate_group`: **40 per minute**.
- `connect_project_to_portfolio`: 15–40 per minute.
- **Formula `display_value`: up to 10,000 formula values per minute, max 5 formula columns per request.**
- `app_subscriptions` query: 120 per minute.

**Pro's 10,000 API calls/day is comfortable for a 60-SKU daily sync** — even a chatty design that writes 60 SKUs × 20 metrics one call at a time is 1,200 calls. Batch with `change_multiple_column_values` and it is a few dozen.

### Formula and mirror columns via the API — a real trap

VERIFIED (developer docs via MCP):

| | Formula | Mirror |
|---|---|---|
| Readable? | **Yes, but only via `display_value`** on `FormulaValue`. `text` returns `""` and `value` returns `null`. | Yes via `display_value` (comma-separated text) on `MirrorValue`, or richer via `mirrored_items { linked_item, mirrored_value }` with inline fragments |
| Writable / clearable via API? | **No** | **No** |
| Filterable in `items_page`? | **No** | **No** |
| Formula referencing a mirror or connect-boards column | **`display_value` will not populate** | — |

So the common claim "formula columns aren't readable via API" is **half-true and out of date**: they are readable through `display_value`, subject to 10,000 values/minute and 5 formula columns per request, **but a formula that references a mirror column returns nothing**. Since mirroring is how you'd pull a supplier cost onto a SKU row, this combination silently breaks. **Do the arithmetic outside monday and write plain Numbers columns.**

### Auth, versioning, apps

- **Auth**: personal API token (mirrors the user's UI permissions, `Authorization: Bearer <token>`) or **OAuth 2.0/2.1 authorization-code** with monday as IdP; you can register your own OAuth app in the Developer Center to cap scopes and get independent audit/revocation (VERIFIED).
- **Versioning**: `API-Version` header. Three versions live at any time — release candidate, current, maintenance — with a new RC each quarter and at least six months of stability per version; deprecations announced ≥6 months ahead. `version` and `versions` queries exist in the live schema (VERIFIED, live introspection + REPORTED for the cadence details from developer.monday.com/api-reference/docs/api-versioning). **2026-10 is listed as a release candidate; 2024-10 and 2025-01 were deprecated on 2026-02-15 and now route to 2025-04** (REPORTED — search result summaries; I could not open the changelog).
- **Live schema surface** (VERIFIED, live introspection): **102 query fields and 213 mutations**. Notable for this design: `audit_logs` + `audit_event_catalogue`, `items_history`, `activity_logs`, `next_items_page`, `items_page_by_column_values`, `complexity`, `usage`, `export_markdown_from_doc`, `doc_version_history`, `doc_version_diff`, `export_job_status`; mutations `create_board_export`, `ingest_items`, `backfill_items`, `bulk_archive_items`, `bulk_delete_items`, `change_multiple_column_values`, `create_notification`, `run_prompt`, `create_webhook`, `use_template`, `duplicate_board`, and per-AI-column configurators (`configure_summarize_ai_column`, `configure_extract_ai_column`, `configure_categorize_ai_column`, `configure_person_assignment_ai_column`, `configure_write_me_ai_column`, `configure_translate_ai_column`, `configure_improve_text_ai_column`, `configure_open_block_ai_column`, `remove_ai_from_column`).
- **`connect_external_agent` does not appear in the default mutation list** — consistent with it being gated behind `API-Version: dev` (VERIFIED, live introspection; absence is the evidence).
- **Board export via API**: `create_board_export` mutation + `export_job_status` / `export_events` queries exist (VERIFIED, live introspection). monday's security checklist also says "you can set up custom exports using the API" (VERIFIED).

---

## 7. The official monday MCP server

VERIFIED (developer docs via MCP + the tool list present in this session).

| | Platform MCP | Apps MCP |
|---|---|---|
| Hosting | **Hosted remote**, `https://mcp.monday.com/mcp` | **Local**, `npx @mondaydotcomorg/monday-api-mcp -t <token> --mode apps` |
| Transport | **Streamable HTTP only** — the old SSE endpoint `https://mcp.monday.com/sse` is deprecated and unsupported | stdio |
| Auth | OAuth 2.0/2.1 (one-click connector for Cursor, Claude, VS Code, Windsurf; or your own OAuth app) **or a personal API token in the `Authorization: Bearer` header** | personal API token via `-t` |
| Purpose | read/write monday data, 60+ tools, plus `all_monday_api` for raw GraphQL | scaffold/deploy monday apps, semantic search over developer docs |

**Headless use from Claude Code / Codex / any harness is explicitly supported** via a static personal API token in the Authorization header — no interactive OAuth needed (VERIFIED). The token mirrors that user's UI permissions.

**Cost: monday MCP is listed as Free in the AI Feature Catalog** — it consumes no AI credits (VERIFIED).

**Tool surface observed in this session** (VERIFIED — these are the tools this session actually has): board/item CRUD (`create_board`, `create_item(s)`, `update_items`, `change_item_column_values`, `create_column`, `create_group`, `move_object`), views and dashboards (`create_view`, `create_view_table`, `create_dashboard`, `create_widget`, `all_widgets_schema`), docs (`create_doc`, `update_doc`, `read_docs`), forms (`create_form`, `form_questions_editor`, `create_form_submission`), automations and workflows (`create_automation`, `manage_automations`, `create_workflow`, `validate_workflow`, `publish_workflow`, `run_workflow_once`, `get_automation_runs`, `get_automation_statistics`), agents (`manage_agent`, `manage_agent_skills`, `manage_agent_knowledge`, `manage_agent_triggers`, `agent_catalog`, `connect_external_agent`), Vibe (`vibe_create`, `vibe_update`, `vibe_get`, `vibe_list`, `vibe_delete`, `vibe_ask`, `vibe_publication`), raw API (`all_monday_api`, `all_api_read`, `all_api_write`, `get_graphql_schema`, `get_type_details`), knowledge (`get_monday_knowledge`), analytics (`board_insights`, `get_board_activity`), notifications (`create_notification`), meetings/notetaker (`explore_meetings`, `get_meetings_content`, `search_meetings_content`), and **`execute_code`**.

**Rate limit observed live:** `get_monday_knowledge(kind:"developer_docs")` is capped at **10 requests per 600 seconds** and returns HTTP 429 with `retryAfter` (VERIFIED — I hit it repeatedly during this research). The `general` knowledge tool has a materially higher budget (25+ calls without a 429).

---

## 8. Vibe (monday's AI app builder)

VERIFIED — [monday vibe: Permissions and Pricing](https://support.monday.com/hc/en-us/articles/32833842348178-monday-vibe-Permissions-and-Pricing), [AI Permissions and Governance](https://support.monday.com/hc/en-us/articles/30934592475410-AI-Permissions-and-Governance):

- AI-powered no-code app builder inside monday. Prompt → custom app; refine in chat.
- **Any monday user can access it provided AI permissions are enabled** in Administration. Not tied to a specific plan tier in the docs (but AI is unavailable on Free).
- **Building and testing are free in "draft" mode. You pay only when you publish.** Pricing is a **paid add-on charged by the number of published apps** (tiered); the price list is only visible in-product at Administration → Vibe apps → See plans (**UNKNOWN** amount — the pricing page is egress-blocked).
- The "Publish Vibe apps" permission is on for admins by default, off for everyone else.
- **A Vibe app can be added as a board view** to create a custom app experience on top of board data — "an internal portal, time tracker, or interactive dashboard" (VERIFIED — [Get started with monday work management](https://support.monday.com/hc/en-us/articles/115005305649-Get-started-with-monday-work-management)). It can also be embedded via the `APP_FEATURE` dashboard widget (VERIFIED, widget schema).
- A Vibe app triggering an integration consumes **2 AI credits per trigger** (VERIFIED, Vibe article; the AI Credits article says 1 — discrepancy noted).
- `vibe_*` tools in MCP include `vibe_create/update/get/list/delete/ask/publication` and there is a `VibeAppStorage` type in the GraphQL schema (VERIFIED, live introspection) — meaning **Vibe apps have their own persistent storage**.

**Can it host a custom SKU-profile app?** Yes, in the sense that a Vibe app can be a board view or dashboard widget rendering SKU data with its own storage, built from a prompt, without leaving monday. Cost is per published app and unquantified. It is a presentation/interaction layer, not a place to run your business logic.

---

## 9. Mobile app

VERIFIED where cited:

| Thing | Mobile status | Source |
|---|---|---|
| Boards and most board views | Yes | [Basic reporting](https://support.monday.com/hc/en-us/articles/360013878299-Basic-reporting-with-monday-com) |
| **Gantt, Workload, Chart, "Default" views** | **Browser only** | [Mobile app board views](https://support.monday.com/hc/en-us/articles/360015740220-Mobile-app-board-views) |
| Dashboards | Yes, viewable | Basic reporting article |
| Offline mode | Yes | same |
| Push notifications | Yes — "push notifications on your mobile device would be synonymous with your bell notifications" | [Notifications via automations and integrations](https://support.monday.com/hc/en-us/articles/31399443744530-Notifications-via-automations-and-integrations) |
| Per-channel notification control (Bell / Email / Mobile) | Yes, in My profile → Notifications | [Notifications explained](https://support.monday.com/hc/en-us/articles/360001292545-Notifications-explained) |
| Workdocs on mobile | Not documented | UNKNOWN |
| "My Work" on mobile | Not documented | UNKNOWN |
| Minimum app versions (for CRM features) | Android 4.92, iOS 4.60 | [monday CRM on mobile](https://support.monday.com/hc/en-us/articles/7085413771666-monday-CRM-on-mobile) |

**One-tap approval on mobile:** monday has **no native "approvals" object** (VERIFIED by absence — I asked the KB directly and it returned only "build an approval pipeline board with status columns and cross-board automations"). The practical pattern is: push notification → open item on phone → **tap the Status column and pick Approved/Rejected** → a `change_status_column_value` webhook fires to the hands runner. That is two taps, works on mobile, and is fully API-observable. A **Button column** also exists and has a "When button clicked" trigger (VERIFIED, trigger catalog) — that is genuinely one tap, but I could not confirm the Button column renders on the mobile item card (**UNKNOWN**).

---

## 10. Permissions, seats, export, residency

VERIFIED — [Permissions on monday.com](https://support.monday.com/hc/en-us/articles/360019222479-Permissions-on-monday-com), [Board permissions](https://support.monday.com/hc/en-us/articles/115005315809-Board-permissions), [User types explained](https://support.monday.com/hc/en-us/articles/360002144900-User-types-explained), [Pricing for guests](https://support.monday.com/hc/en-us/articles/360000305419-Pricing-for-guests):

| Capability | Plan |
|---|---|
| Board permission sets: Edit everything / Only edit content / View and comment | all paid |
| **Only edit assigned items** | **Pro+** |
| **Column permissions (restrict column view or edit)** | **Enterprise only** |
| Enterprise role model (built-in roles + per-category tailoring: Items, Subitems, General, Updates, Columns, Groups, Views, Forms) | Enterprise |
| Private boards | Pro+ |
| Shareable boards (guest collaboration) | Standard+ |
| Guests | Standard: 3 free, then 4 guests = 1 billed seat. **Pro/Enterprise: unlimited guests** |
| **Viewers** | **Unlimited and free from Basic up** |
| Custom account roles | Enterprise |
| Closed workspaces, SSO/SAML, panic button, session timeout, granular board permissions, HIPAA | Enterprise |
| Board owners always bypass board permissions | all |

**Activity log retention by plan** (VERIFIED — [The Activity Log](https://support.monday.com/hc/en-us/articles/115005310745-The-Activity-Log)): Basic = past **week**; Standard = **6 months**; Pro = **1 year**; Enterprise = **5 years**. The log records the change, who made it, item/group, column, and old→new value; it does **not** record updates/comments. It is queryable via API.

**Audit log** (account security events) is accessible via API for SIEM integration (VERIFIED — [secure configuration checklist](https://support.monday.com/hc/en-us/articles/34336185460498-monday-com-secure-configuration-checklist)); the `audit_logs` and `audit_event_catalogue` queries exist in the live schema with filters for user, events, IP and time range (VERIFIED, live introspection). **Which plan gates the audit log is UNKNOWN** — not stated in any article the KB returned; industry-standard is Enterprise.

**Export** (VERIFIED — [How to export your entire account's data](https://support.monday.com/hc/en-us/articles/360002543719-How-to-export-your-entire-account-s-data)):
- Board → Excel (any plan).
- Admin → full account export to a zip of Excel sheets + uploaded files. **Once every 24 hours; may take 24 hours; download link valid 24 hours; all admins notified each time.** **Excludes archived boards, workdocs and dashboards.**
- API export: `create_board_export` mutation, `export_markdown_from_doc` query (VERIFIED, live introspection).

**Data residency** (REPORTED — could not open monday's own residency page; from search summaries of monday.com blog/support): regions are **US, EU (Germany), AU**, plus IL for monday code. Storing data in the EU region is available for **Enterprise, and for Standard/Pro accounts created on or after 2023-01-23**; but **only Enterprise EU accounts get region-bound residency including sub-processors**.

---

## 11. Notifications and "My Work"

VERIFIED — [Bell Notifications](https://support.monday.com/hc/en-us/articles/360015535060-Bell-Notifications), [Notifications explained](https://support.monday.com/hc/en-us/articles/360001292545-Notifications-explained):

- **Bell** = things about you: @mentions, replies to your updates, assignment to a People column, being made admin. Has an "Assigned to me" tab, filter-by-person, and search.
- **Inbox / Update Feed** = every update from boards you subscribe to (broader, noisier).
- **Email** and **desktop** notifications, configurable per event type.
- **Mobile push ≡ bell notifications.**
- **My Work** collects everything assigned to you across the account.
- Automations can send custom bell and email notifications; `create_notification` is an API mutation (VERIFIED, live introspection), so an external agent can push a notification to Rami directly.

---

## 12. Capability table

| Capability | Tier required | Price delta vs Pro | Status | Source |
|---|---|---|---|---|
| 10,000 items/board | any paid | — | VERIFIED | support: item limits |
| 100,000 items/board | Enterprise | quote-only | VERIFIED | same |
| Connect 20 boards to one board | Pro | — | VERIFIED | support: linkage limits |
| Connect 200 boards / 60 per column | Enterprise | quote-only | VERIFIED | same |
| Mirror column | Basic+ (in column center) | — | VERIFIED | plan articles |
| **Formula column** | **Pro** | — | VERIFIED | plan articles |
| Time tracking column | Pro | — | VERIFIED | plan articles |
| Dependency column | Pro | — | VERIFIED | plan articles (service/CRM wording) |
| Timeline / Calendar / Map views | Standard | −$7/seat/mo | VERIFIED | plan articles |
| **Chart view, Workload view** | **Pro** | — | VERIFIED | plan articles |
| Kanban, Form, Files, Table views | Free | — | VERIFIED | plan articles |
| 5 boards per dashboard | Standard | −$7/seat/mo | VERIFIED | The Dashboards |
| **20 boards per dashboard** | **Pro** | — | VERIFIED | The Dashboards |
| 50 boards per dashboard | Enterprise | quote-only | VERIFIED | The Dashboards |
| 30 widgets/dashboard, 20k items/dashboard | all | — | VERIFIED | The Dashboards |
| 500k items/dashboard for Chart/Battery/Numbers | Enterprise | quote-only | VERIFIED | mondayDB 2.0 |
| 250 automation + 250 integration actions/mo | Standard | −$7/seat/mo | VERIFIED | plan articles |
| **25,000 automation + 25,000 integration actions/mo** | **Pro** | — | VERIFIED | plan articles |
| 250,000 + 250,000 actions/mo | Enterprise | quote-only | VERIFIED | plan articles |
| **Workflow builder (multi-board workflows)** | **Pro** | — | VERIFIED | AI workflow builder FAQs |
| AI blocks in automations/workflows | any paid + AI credits | 8 credits/action = $0.08 | VERIFIED | AI Feature Catalog |
| Outgoing webhooks (API + UI) | any paid | — | VERIFIED | dev docs: webhooks |
| "Every time period" trigger | any paid | — | VERIFIED | agent_catalog live |
| **monday agents (Digital Workforce)** | Work Management, gradual release, admin only | **"will be monetized in the future" — price UNKNOWN** | VERIFIED (availability) / UNKNOWN (price) | AI Agent builder |
| Connect external agent (webhook or managed) | pre-release, `API-Version: dev` | unknown | VERIFIED | dev docs: agents |
| sidekick lite (5 msg/user/day) | Standard, Pro | — | VERIFIED | sidekick article |
| sidekick Plus (100 msg/day, account context) | Enterprise incl.; add-on on Standard/Pro | add-on, price UNKNOWN | VERIFIED | sidekick article |
| **monday MCP server** | any paid | **free, no AI credits** | VERIFIED | AI Feature Catalog |
| API: 10,000 calls/day, 2,500 q/min, 100 concurrency | **Pro** | — | VERIFIED | dev docs: rate limits |
| API: 25,000 calls/day | Enterprise | quote-only | VERIFIED | dev docs |
| Agent complexity budget 20M/min | any (agent context) | — | VERIFIED | dev docs |
| Formula readable via `display_value` | Pro (needs formula column) | — | VERIFIED | dev docs: formula |
| Formula/mirror writable or filterable via API | **never** | — | VERIFIED | dev docs: coverage gaps |
| Doc markdown export + version history via API | any paid | — | VERIFIED | live schema |
| Board export via API (`create_board_export`) | any paid | — | VERIFIED | live schema |
| Full account export (zip) | any paid, admin, 1×/24h | — | VERIFIED | export article |
| Audit log API | UNKNOWN (likely Enterprise) | — | UNKNOWN | secure config checklist |
| Activity log retention 1 year | Pro | — | VERIFIED | The Activity Log |
| Activity log retention 5 years | Enterprise | quote-only | VERIFIED | The Activity Log |
| Board permission "only edit assigned items" | Pro | — | VERIFIED | Board permissions |
| **Column-level permissions** | **Enterprise** | quote-only | VERIFIED | Permissions on monday.com |
| Private boards | Pro | — | VERIFIED | plan articles |
| Unlimited guests | Pro | — | VERIFIED | Pricing for guests |
| Unlimited free viewers | Basic+ | — | VERIFIED | plan articles |
| SSO/SAML, custom roles, panic button, closed workspaces, HIPAA | Enterprise | quote-only | VERIFIED | plan articles |
| EU region-bound residency incl. sub-processors | Enterprise | quote-only | REPORTED | monday blog/support via search |
| Managed (governed) templates | Enterprise beta | quote-only | VERIFIED | Template Editor |
| Workspace-as-template (second brand) | any paid; **Main boards only** | — | VERIFIED | Workspace settings |
| Vibe app building/testing | any paid with AI on | free in draft | VERIFIED | Vibe pricing |
| Vibe app **publishing** | any paid | **add-on priced per published app — amount UNKNOWN** | VERIFIED (model) / UNKNOWN (amount) | Vibe pricing |
| QuickBooks integration | **monday CRM product** | extra product seats | VERIFIED | Unique features found only in monday CRM |
| Mobile: Gantt / Workload / Chart board views | none — browser only | — | VERIFIED | Mobile app board views |
| Seat pricing Basic / Standard / Pro (annual) | $9 / $12 / $19 per seat/mo | — | REPORTED | third-party pricing roundups |
| Yearly billing discount | 18% vs monthly | — | VERIFIED | Plans and pricing article |
| Seat "bucket" pricing: min 3, then multiples of 5 | all paid | — | VERIFIED | Plans and pricing article |
| AI credits $0.01 (yearly) / $0.0125 (monthly); CAD 0.01375 / 0.0175 | all paid | — | VERIFIED | AI Feature Catalog |
| One-time 6,000 AI credit trial (12,000 Enterprise) | all paid | — | VERIFIED | AI Credits |

---

## 13. Implications for the design

### Build in monday

1. **The decision surface, not the data warehouse.** monday should hold: the daily ranked decision list for Rami, the approval queue, department state summaries, the SKU master (one row per SKU, ~60 rows), the calendar/blackout board, and the request/inbox routing between departments. All of that is hundreds of items, not tens of thousands.
2. **Approvals.** One "Approvals" board. Status column with Pending / Approved / Rejected / Expired, a 48-hour expiry automation, a `change_status_column_value` webhook to the hands runner, and `create_notification` + mobile push to Rami. Two taps on a phone. Every approval is an item with a permanent activity-log entry (1 year retention on Pro).
3. **The daily brief.** A dashboard with Chart, Numbers and Battery widgets over the SKU master + approvals + a "signals" board. It renders on mobile. Add a Vibe app as a board view later if a richer SKU profile card is wanted.
4. **Docs as the compounding knowledge layer.** `create_doc` / `add_content_to_doc_from_markdown` in, `export_markdown_from_doc` out, `doc_version_history` + `doc_version_diff` for the Monday review. This is a genuine two-way bridge between `memory/MEMORY.md` and a surface Rami can read on a phone. **Note: docs are excluded from the full account export — the repo stays the system of record.**
5. **Scheduling of department runs.** The "Every time period" trigger takes an IANA timezone and monday's own example uses `Asia/Jerusalem`. Use it to poke the hands runner via webhook, or to fire a monday agent, rather than maintaining cron on the Mac mini for anything monday can see.

### Build elsewhere (the repo, DataDoe, the Mac mini hands runner)

1. **All time-series and metric history.** 60 SKUs × daily metrics hits the 10,000-items-per-board wall fast, dashboards cap at 20,000 items across all connected boards, and dashboard textual search does not exist. Keep history in the repo/DataDoe; push only current-state and deltas into monday.
2. **All arithmetic.** Formula columns are Pro-only, unwritable, unfilterable, capped at 10,000 values/minute and 5 columns per request, and **silently return nothing when they reference a mirror column**. Compute contribution margin, stock cover and ROAS in the agent and write plain Numbers columns. Use monday formulas only for cosmetics.
3. **Money and Amazon writes.** Nothing in monday's agent capability list touches an external account. The hands runner on the Mac mini stays the only thing that executes.
4. **The ledger.** `ledger/actions.jsonl` in git, forever. monday's activity log is 1 year on Pro and is not exportable in the account zip in a form you'd want to depend on.
5. **Second-brand instantiation.** Save the whole workspace as a template (Main boards only — so keep the brand workspace's boards Main). Structure duplicates; values do not. Combine with `use_template` / `duplicate_board` via API and a repo-side seeding script. Budget 40 board-creating mutations per minute.

### What genuinely needs Enterprise

Only four things, and none of them are needed in 2026–2027 at this scale:
- **Column-level permissions** (hiding cost/margin columns from a future VA or partner). Board-level "view and comment" plus a separate private board is the Pro workaround.
- **>10,000 items on a single board** and >20 connected boards.
- **Region-bound EU residency including sub-processors**, 5-year activity log, SSO/SAML, HIPAA.
- **Managed templates** for governed multi-brand rollout — relevant only at brand #3+.

Enterprise requires a 12-month minimum term and, reportedly, meaningful seat counts. **Do not buy it.**

### Recommended plan tier and cost

**Stay on Work Management Pro.** Everything the design needs that is plan-gated — formula column, chart and workload views, 20 boards per dashboard, 25,000 automation actions/month, the multi-board workflow builder, private boards, unlimited guests, 10,000 API calls/day, 1-year activity log, monday agents (Work Management only) — lands exactly at Pro. Standard fails on four counts at once: 250 actions/month, 5 boards per dashboard, no formula column, no workflow builder.

Costs (USD, annual billing, as of 2026-09-06; seat prices REPORTED, structure VERIFIED):

| Scenario | Seats billed | Seat cost/mo | AI credits/mo | Total/mo |
|---|---|---|---|---|
| **Now — Rami alone** | current account is a legacy 2-seat Pro bucket; a new purchase would be the **3-seat minimum** | 2 × $19 = **$38** (legacy) or 3 × $19 = **$57** (new) | 6,000 one-time trial ≈ 750 AI-block actions, then a Pro pack — REPORTED minimum 3,000 credits ≈ **$30** | **$38–57**, rising to **~$68–87** once the trial burns out |
| **Later — 3 seats** | 3 (still inside the minimum bucket) | 3 × $19 = **$57** | 3,000–8,000 credits = **$30–80** | **$87–137** |
| **If a 4th seat is ever added** | jumps to the **5-seat bucket** | 5 × $19 = **$95** | as above | **$125–175** |

Notes on that table:
- The 2-seat Pro subscription on the account today is below monday's current 3-seat minimum — it is a grandfathered bucket. **Do not cancel or downgrade it**; re-subscribing would cost the 3-seat minimum. (Structure VERIFIED via [Plans and pricing](https://support.monday.com/hc/en-us/articles/4405633151634-Plans-and-pricing-for-monday-com); the grandfathering inference is mine.)
- **Monthly billing costs 18% more** — annual is the right call (VERIFIED).
- **Viewers are free and unlimited from Basic up, and guests are unlimited on Pro.** A future VA, accountant or partner should be a guest or viewer, not a seat. This is how you stay in the 3-seat bucket.
- **Budget AI credits as a variable, not a subscription.** At 8 credits per AI block action, $0.01/credit, one AI action costs $0.08. A department running 20 AI-block actions a day across 9 departments is 180 actions/day ≈ 5,400/month ≈ **$54/month**. Doing that reasoning in Claude Code instead costs monday nothing, because **monday MCP consumes zero AI credits**. That is a strong argument for keeping intelligence in the harness and using monday's AI only where it must run unattended inside a monday workflow.
- Vibe publishing and any future monday-agent seat charge are **unbudgeted unknowns**. Keep agents in Claude Code / the hands runner until monday publishes agent pricing.

### On monday agents specifically

Do not build the company on them. They are in gradual release, Work Management only, admin-only to manage, explicitly "will be monetized in the future" at an unpublished price, and their action surface is monday objects — create/update items, assign, change status, draft messages, log outcomes. They cannot call DataDoe, cannot touch Amazon, cannot write to git.

**The right use of the agent layer is the inverse: register the external agents as monday agents.** `connect_external_agent_sync` gives a signed-webhook contract (HMAC-SHA256 over `${timestamp}.${rawBody}`, 30-second SSE reply window for chat, 200-then-write-back for mentions and assignments) and returns an `api_token` scoped to that agent. That makes each department a first-class monday entity Rami can @mention on an item and assign work to — with the actual reasoning running in Claude Code or on the Mac mini, and with a 20M-complexity-per-minute API budget. It is pre-release (`API-Version: dev`), so build the plain-webhook + MCP path first and treat agent registration as an upgrade.

---

## Open questions

1. **What does a monday agent seat cost, and when does billing start?** monday's own doc says only "will be monetized in the future." Third parties report agent credit consumption beginning 2026-06-08. Needs a look at the in-product pricing page.
2. **Are the per-plan monthly AI credit minimums (1,000/2,000/3,000) real, and are they now mandatory alongside seats?** Third-party REPORTED only; monday's support articles still describe a one-time 6,000-credit trial. These two models contradict each other. Check Administration → Usage stats → AI → "Go to AI credit plans" on the live account.
3. **What does publishing one Vibe app cost?** Only visible at Administration → Vibe apps → See plans.
4. **Is the audit log API gated to Enterprise?** The `audit_logs` query exists in the schema this Pro account introspected, but that proves schema presence, not authorization. Try one read-only `audit_logs` call.
5. **Does the Button column render and fire on the mobile item card?** Decides whether approval is one tap or two.
6. **Is QuickBooks reachable at all from a Work Management–only account,** or does it require buying monday CRM seats?
7. **Does "duplicating a board with values is not supported" apply to this account's boards,** or only to Enterprise mondayDB 2.0 boards? Decides the second-brand seeding strategy.
8. **What is the current stable API version** (2026-07 vs 2026-04)? A `{ version { value kind } }` query answers it in one call; my attempt was blocked by the read-only tool set I was asked to use.
9. **Per-minute automation rate limits** are acknowledged in monday's docs but never numbered. Matters if the hands runner triggers automations via API writes.
10. **Exact Free/Basic automation action allowances** — the plan articles never state them.
