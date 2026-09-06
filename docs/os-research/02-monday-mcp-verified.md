# monday.com MCP + API — hands-on verification in Rami's account

**Date of verification: 2026-09-06. All hands-on checks were read-only.** No board, item, column, doc, workflow, automation, agent, app, view, form, dashboard or workspace was created, updated, moved or deleted. Where a tool would have written, only its published description was read and is quoted below.

**Tagging.** `VERIFIED` = I called the tool / ran the query in this account today and this is what came back (or: I read the tool's own schema description as served by the monday MCP server today). `REPORTED` = monday's own developer-docs assistant (`get_monday_knowledge kind:"developer_docs"`) returned it with a docs URL, but I could not open the page directly — `developer.monday.com` and `support.monday.com` are both blocked by this environment's egress proxy (`EGRESS_BLOCKED`), and the session's web-search budget was exhausted. `UNKNOWN` = could not confirm; what I tried is stated.

Account under test: `ramikhalaile10's Team`, account id `35918339`, **tier `pro`, `active_members_count: 2`, not in trial, products: `[{kind: core, tier: pro}]`** — VERIFIED via `get_user_context` and `account { id name slug tier }`. No monday-dev, no monday-CRM, no monday-service product is on this account, which matters: several tools in the server (`get_monday_dev_sprints_boards`, `get_sprint_summary`, `get_sprints_metadata`) target products this account does not have.

---

## 1. MCP tool inventory

94 monday tools are exposed to this session. Grouped, with direction. Tier limits are almost never stated in tool descriptions — where a description says something about limits, it is quoted.

### Boards, items, columns, views (read)
| Tool | Dir | Notes (VERIFIED from tool schema) |
|---|---|---|
| `get_user_context` | R | user id/name, account tier, `active_members_count`, favorites, most-visited boards |
| `list_workspaces` | R | paged, max 100/page |
| `workspace_info` | R | "returns up to 100 of each object type" (boards, docs, folders) per workspace |
| `get_board_info` | R | columns (with raw `settings` + `revision`), groups, owners, views, `hierarchy_type`, `items_count`, `items_limit`. Warns: views `settings` "can be multi-MB" |
| `get_board_items_page` | R | cursor pagination, `limit` max 500, structured `filters`, `orderBy`, `searchTerm`, `includeSubItems` |
| `board_insights` | R | server-side group-by/aggregate: `SUM AVERAGE MEDIAN MIN MAX COUNT COUNT_ITEMS COUNT_DISTINCT DATE_TRUNC_* LABEL IS_DONE …`, `limit` max 1000 |
| `get_column_type_info` | R | `fetchMode: schema` (JSON-schema for column *settings*) or `guidelines` (filter/aggregation rules) |
| `search` | R | `BOARD DOCUMENTS FOLDERS WORKSPACES UPDATES ITEMS TIMELINE_ITEMS DASHBOARDS`, `limit` max 20, **requires a non-empty search term — no "list everything" mode** |
| `get_updates` | R | item or board updates, max 100/page, optional replies + assets |
| `get_board_activity` | R | activity log, default last 30 days, source of `action_record_uuid` for `undo_action` |
| `get_assets`, `get_asset_upload_url` | R | asset metadata; public URL "valid for 1 hour"; upload max **500 MB** |
| `list_users_and_teams` | R | users/teams incl. team membership |
| `get_graphql_schema`, `get_type_details` | R | schema introspection |
| `all_api_read` | R | arbitrary GraphQL **queries only** — "mutations are rejected with an error before the request is sent" |
| `get_monday_dev_sprints_boards`, `get_sprint_summary`, `get_sprints_metadata` | R | monday-dev only; not applicable to this account |

### Boards, items, columns, views (write — description only, not called)
`create_board`, `create_column`, `update_column`, `create_group`, `create_item`, `create_items` (≤20/call), `create_update`, `change_item_column_values`, `update_items` (**≤40 items/call, can span boards**), `create_view`, `create_view_table`, `update_view`, `update_view_table`, `delete_view`, `create_workspace`, `update_workspace`, `create_folder`, `update_folder`, `move_object`, `finalize_asset_upload`, `all_api_write`, `all_monday_api`.

Notable: `create_board` takes a free-text `creationPrompt` ("Describe in free text how you want the board to be built") and `useMlsTemplate` for multi-level boards. `create_view` supports `TABLE | DASHBOARD | FORM | APP`.

### Docs
`read_docs` (R), `create_doc` (W), `update_doc` (W). Covered in §7.

### Dashboards & widgets
`all_widgets_schema` (R), `create_dashboard` (W, ≤50 boards), `create_widget` (W). Plus four **UI-render-only** tools that draw in the chat surface and touch nothing in the account: `show-table`, `show-chart`, `show-battery`, `show-assign`.

### Automations (board recipes)
`list_automations` (R), `get_automation_runs` (R), `get_automation_statistics` (R), `create_automation` (W), `manage_automations` (W: activate/deactivate/delete).

### Workflows (the newer multi-step engine)
`create_workflow` (W), `invoke_workflow_expert` (W — edits a workflow), `invoke_process_planner` (R-ish: "does not execute any changes"), `validate_workflow` (R — "does NOT modify the workflow"), `publish_workflow` (W), `run_workflow_once` (W, **real side effects**), `get_run_once_trigger_entities` (R), `get_workflow_run_once_status` (R), `stop_workflow_run_once` (W).

### Agents
`agent_catalog` (R — "READ-ONLY — no agent_id required"), `manage_agent` (R+W), `manage_agent_knowledge` (R+W), `manage_agent_skills` (W + catalog create), `manage_agent_triggers` (R+W), `connect_external_agent` (W). §4.

### Forms (WorkForms)
`get_form` (R), `create_form` (W), `update_form` (W), `form_questions_editor` (W), `create_form_submission` (W — submits a response).

### Vibe apps
`vibe_list` (R), `vibe_get` (R), `vibe_ask` (R — "read-only, no code changes"), `vibe_create` (W), `vibe_update` (W), `vibe_delete` (W, "Destructive"), `vibe_publication` (W). §8.

### Code execution
`execute_code` (W-capable), `create_action` / `update_action` / `delete_action` / `get_action` / `list_actions` / `run_action` (saved scripts). §9.

### Meetings (monday Notetaker)
`explore_meetings` (R), `search_meetings_content` (R), `get_meetings_content` (R). Discovery is keyword-ranked, "not semantic". Only indexed meetings are candidates.

### Misc
`get_monday_knowledge` (R — official KB Q&A, two corpora: `general` and `developer_docs`), `submit_bug_or_feature_request` (W to monday, not to the account).

**Tier gating actually observed:** none of the tool descriptions state per-tier limits except `vibe_create` ("the number allowed depends on your account tier") and `vibe_publication` ("respects the published-apps license limit"). VERIFIED. Everything else that is tier-limited (seats, API daily calls, automation actions) is limited server-side, not in tool metadata.

---

## 2. Column types

**Full enum, VERIFIED** via `get_type_details("ColumnType")` — 43 values:

`auto_number, board_relation, button, checkbox, color_picker, country, creation_log, date, dependency, direct_doc, doc, dropdown, email, file, formula, group, hour, integration, item_assignees, item_id, last_updated, link, location, long_text, mirror, name, numbers, people, person, phone, progress, rating, status, subtasks, tags, team, text, time_tracking, timeline, unsupported, vote, week, world_clock`

**Read-only column types — REPORTED** (monday developer docs via `get_monday_knowledge`, citing `developer.monday.com/api-reference/reference/column-types-reference#read-only-columns`):

> `creation_log`, `formula`, `item_id`, `last_updated`, `mirror`, `progress` (progress tracking), and `subtasks` — "the column itself is read-only; nested items must be managed via `create_subitem` or `delete_item`".

**Corroborating VERIFIED signal:** `get_column_type_info fetchMode:"guidelines"` returns `filter: null` for `mirror`, `formula`, `timeline`, `dropdown`, `board_relation` — i.e. those types have no documented filter rules and mirror/formula cannot even be filtered on server-side. Practical consequence: **you cannot query "all SKUs where the mirrored cover-days < 14" through `items_page` filters.** You must pull and filter client-side, or store the number in a real `numbers` column.

### Write shapes for `change_multiple_column_values` (`column_values` is a **stringified JSON object** keyed by column id)

VERIFIED from MCP tool descriptions (`create_item`, `change_item_column_values`, `update_items`):
> "Status and dropdown columns must use `{ "label": "..." }` (or `{ "labels": ["...", "..."] }` for multi-select dropdown). Date columns use `{ "date": "YYYY-MM-DD" }`. Text/number/email/phone use plain strings."
> `createLabelsIfMissing` — "missing status/dropdown labels … will be auto-created … Requires permission to change board structure."

REPORTED (monday docs via the KB tool, one docs URL per row):

| Column | JSON value | Source page |
|---|---|---|
| status | `{"label":"Done"}` or `{"index":1}` | `/docs/change-column-values` |
| dropdown | `{"ids":[1,2]}` or `{"labels":["A","B"]}` | `/reference/dropdown#update-value` |
| date | `{"date":"2026-06-15","time":"09:00:00"}` (omit `time` for date-only) | `/reference/date#mutations` |
| timeline | `{"from":"2026-01-01","to":"2026-03-31"}` | `/docs/portfolio-skill-update-project-status` |
| link | `{"url":"https://…","text":"Go to monday!"}` | `/reference/link#mutations` |
| board_relation ("connect boards") | `{"item_ids":[1122334455, 5544332211]}` — **boards must already be connected in column settings** | `/reference/connect#mutations` |
| people | `{"personsAndTeams":[{"id":48202303,"kind":"person"},{"id":51166,"kind":"team"}]}` — **replaces all assignees** | `/reference/people#mutations` |
| email | `{"text":"a@b.com","email":"a@b.com"}` | `/reference/columns#mutations` |
| phone | `{"phone":"+12025550169","countryShortName":"US"}` | `/reference/phone#mutations` |
| country | `{"countryCode":"US","countryName":"United States"}` (both required) | `/reference/country#mutations` |
| tags | `{"tag_ids":[295026,295064]}` — tags must exist first; replaces all | `/reference/tags#mutations` |
| hour | `{"hour":16,"minute":42}` | `/reference/hour#mutations` |
| week | `{"week":{"startDate":"2026-03-16","endDate":"2026-03-22"}}` — must span exactly 7 days aligned to the account's first-day-of-week | `/reference/week#mutations` |
| rating | `{"rating":5}` (1..column max) | `/reference/rating#mutations` |
| checkbox | `{"checked":"true"}`; `null` to clear | `/reference/checkbox#mutations` |
| long_text | `{"text":"…"}` — **2,000 character cap** | `/reference/long-text#mutations` |
| world_clock | supports `change_multiple_column_values` but **not** `change_simple_column_value`; exact payload not in the KB | `/reference/world-clock` |

UNKNOWN (the KB explicitly said its sources don't cover them; docs pages unreachable from this environment): exact JSON for `numbers` (plain string works per the MCP tool description), `file`, `color_picker`, `dependency`, `vote`, `doc`, `button`. For `file`, the supported path is the dedicated mutation `add_file_to_column(column_id, file: File!, item_id)` or the MCP pair `get_asset_upload_url` → HTTP PUT → `finalize_asset_upload`.

**Read-back shapes VERIFIED** on the live `Leads` board: `status` → `{"index":17}`; `numbers` → `"2500000"`; `date` → `{"date":"2026-07-21","time":null,"changed_at":…}`; `long_text` → `{"text":"…","changed_at":…}`; empty `board_relation` → `null`.

---

## 3. GraphQL schema facts

All VERIFIED via `get_graphql_schema`, `get_type_details`, and live read queries.

- **Schema size:** 102 root query fields, **213 mutation fields**, 1,366 types.
- **Pagination.** `boards { items_page(limit, query_params, cursor) { cursor items { … } } }` returns `ItemsResponse { cursor, items }`. `cursor` is an opaque string; `null` means no more pages. Confirmed live: a 3-item page on the 295-item board returned `cursor: "MSw1MDk5OTcyNTY4LEh1WWVUMFhMdllFeWJqVWNwbXdVViwyOTUsMyx8MzU2NTgxMjM5Mw"`. `next_items_page` is the root query for continuing by cursor. The MCP wrapper caps `limit` at 500.
- **Filtering.** `query_params: ItemsQuery` = `{ rules: [ItemsQueryRule!], groups: [ItemsQueryGroup!], operator: ItemsQueryOperator (default and), ids: [ID!] (max 100), order_by: [ItemsQueryOrderBy!] }`. `ItemsQueryRule = { column_id: ID!, compare_value: CompareValue!, compare_attribute: String, operator: ItemsQueryRuleOperator (default any_of) }`.
  `ItemsQueryRuleOperator` enum: `any_of, not_any_of, is_empty, is_not_empty, within_the_last, within_the_next, greater_than, greater_than_or_equals, lower_than, lower_than_or_equal, between, starts_with, ends_with, contains_text, contains_terms, not_contains_text`.
  **Gotcha VERIFIED the hard way:** I filtered a status column with `compare_value: ["New"] / any_of` and got zero rows even though matching rows exist. `get_column_type_info(status, guidelines)` explains: `any_of`/`not_any_of` need the **numeric label id**; label *text* only works with `contains_terms`. Dates need `["EXACT","2026-01-01"]` or `TODAY|TOMORROW|THIS_WEEK|ONE_WEEK_AGO`. People need `"person-<id>"`, `"team-<id>"` or `"assigned_to_me"`.
- **Complexity.** `Complexity { before, after, query, reset_in_x_seconds }`. Live: budget observed at **19,999,977 → 20,000,000-class, `reset_in_x_seconds` 51–52** (sliding 60s window). A 3-item × 5-column `items_page` cost **65 points**; the same shape with `query_params` + `order_by` and `limit: 2` cost **5,020**. Filtered queries are ~75× more expensive than unfiltered pages — budget accordingly.
  REPORTED (docs): app tokens get 5M read + 5M write per minute; **AI agents get 20M/min** (matches what this MCP connection sees); personal tokens 10M shared; a single query may not exceed 5M.
- **Daily call limit.** VERIFIED live: `platform_api { daily_limit { base total consumption } }` → `{"base":10000,"total":10000,"consumption":81}`. REPORTED: Free/Basic/Standard 1,000 · **Pro 10,000** · Enterprise 25,000, reset at midnight UTC. Also REPORTED: minute limit Pro 2,500 queries/min; concurrency Pro 100.
- **`get_monday_knowledge` has its own limiter, VERIFIED:** `429 TOO_MANY_REQUESTS_EXCEPTION, limit: 10, windowSeconds: 600` — 10 KB questions per 10 minutes, **shared across every agent using this account**. I hit it repeatedly.

### Mutation signatures relevant to us (VERIFIED by `__type(name:"Mutation")` introspection)

```
create_item(board_id: ID!, item_name: String!, column_values: JSON, group_id: String,
            create_labels_if_missing: Boolean, position_relative_method: PositionRelative, relative_to: ID)
create_subitem(parent_item_id: ID!, item_name: String!, column_values: JSON, create_labels_if_missing: Boolean)
change_column_value(board_id: ID!, item_id: ID, column_id: String!, value: JSON!, create_labels_if_missing: Boolean)
change_multiple_column_values(board_id: ID!, item_id: ID, column_values: JSON!, create_labels_if_missing: Boolean)
change_simple_column_value(board_id: ID!, item_id: ID, column_id: String!, value: String, …)
create_update(item_id: ID, body: String!, parent_id: ID, mentions_list: [UpdateMention],
              original_creation_date: String, use_app_info: Boolean)
create_notification(user_id: ID!, target_id: ID!, target_type: NotificationTargetType!, text: String!)
create_webhook(board_id: ID!, url: String!, event: WebhookEventType!, config: JSON)
create_doc(location: CreateDocInput!, doc_owner_ids: [ID!])
add_content_to_doc_from_markdown(docId: ID!, markdown: String!, afterBlockId: String)
create_doc_blocks(docId: ID!, blocksInput: […]!, afterBlockId: String)
set_item_description_content(item_id: ID!, markdown: String!)
add_file_to_column(item_id: ID!, column_id: String!, file: File!)
add_file_to_update(update_id: ID!, file: File!)
duplicate_board(board_id: ID!, duplicate_type: DuplicateBoardType!, board_name: String,
                workspace_id: ID, folder_id: ID, keep_subscribers: Boolean)
create_board(board_name: String!, board_kind: BoardKind!, template_id: ID, prompt: String,
             workspace_id: ID, folder_id: ID, empty: Boolean, use_mls_template: Boolean, …)
use_template(template_id: Int!, destination_workspace_id: Int, destination_name: String,
             callback_url_on_complete: String, solution_extra_options: JSON, …)
move_item_to_board(board_id: ID!, group_id: ID!, item_id: ID!,
                   columns_mapping: [ColumnMappingInput!], subitems_columns_mapping: [ColumnMappingInput!])
archive_item(item_id: ID)
bulk_delete_items(board_id: ID!, item_ids: [ID!]!)        # "Asynchronously delete items on a board"
ingest_items(board_id: ID!, group_id: ID!, on_match: OnMatchInput)
                                    # "ongoing integrations with full side effects and a 10k row limit"
undo_action(job_id: ID!)
run_prompt(prompt: String!, config: RunPromptConfigInput)  # AI completion, first-party
create_view(board_id: ID!, type: ViewKind!, filter: ItemsQueryGroup, sort: […], settings: JSON, …)
create_dashboard(name: String!, workspace_id: ID!, board_ids: [ID!]!, kind: DashboardKind, …)
create_widget(parent: WidgetParentInput!, kind: ExternalWidget!, name: String!, settings: JSON!, …)
delete_board_automation(id: ID!, board_id: ID!)
```

`DuplicateBoardType` = `duplicate_board_with_pulses | duplicate_board_with_pulses_and_updates | duplicate_board_with_structure` — **`duplicate_board_with_structure` is the second-brand instantiation primitive.**

`run_prompt` config: `{ model: AiModel, system_prompt, temperature, max_tokens }`, `AiModel = MONDAY_FAST | MONDAY_STANDARD | MONDAY_POWERFUL` — a first-party LLM call available straight from the API, no key of ours.

`WebhookEventType` (21 values, VERIFIED): `change_column_value, change_specific_column_value, change_status_column_value, change_name, change_subitem_column_value, change_subitem_name, create_item, create_subitem, create_column, create_update, create_subitem_update, edit_update, delete_update, item_archived, item_deleted, item_restored, item_moved_to_any_group, item_moved_to_specific_group, move_subitem, subitem_archived, subitem_deleted`. **There is no time/schedule webhook and no "doc changed" webhook.** Current webhooks on `Leads`: none (`webhooks(board_id: …)` → `[]`).

---

## 4. Agents and dashboard widgets

### `agent_catalog action:"list_triggers"` — 18 triggers, VERIFIED

| block_reference_id | Trigger | Required fields |
|---|---|---|
| `10380125` | **Every time period** | `schedulerConfig` = `{type: Daily\|Weekly\|Monthly, occurrences 1-99, hour 0-23, minute 0-59, timezone: IANA, days[]}` — e.g. `{type:"Weekly", days:[3,4], hour:18, minute:0, timezone:"Asia/Jerusalem"}` |
| `10380130` | When item created | boardId |
| `10380132` / `10380134` | When item deleted / archived | boardId |
| `10380147` | When column changes | boardId, columnId |
| `10380154` | When status changes to something | boardId, statusColumnId, desiredStatusColumnValue |
| `10380139` | When button clicked | boardId, buttonColumnId |
| `10380151` | When form is submitted | boardId, formId (optional) |
| `10439524` | When update created | boardId |
| `11576972` | When item moves to board | targetBoardId |
| `12004624` | When board created | workspaceId |
| `10458532`/`10470886`/`10470892`/`10470901` | Subitem created / archived / deleted / status changed | boardId (+ status fields) |
| `10571999` | When user joined the account | — |
| `11840114` | When Notetaker meeting ended | isAdminKeyId |
| `15988055` | Wait for Microsoft Teams button clicked | — |

The catalog explicitly warns: **"OAuth/3rd-party triggers (Slack, Gmail, Salesforce, etc.) require user setup in the monday.com UI and will not appear here."** No email trigger, no inbound-webhook trigger, no "when a doc changes".

### `agent_catalog action:"list_skills"` — 11 skills, VERIFIED
`18587329` Project risk insights · `18583395` Social post creator · `18583805` HTML Email builder · `18576511` Rewrite and refine · `18583851` Meeting actions · `18585064` Weekly team digest (sends to Slack) · `18585656` Executive summary · `18586028` Feedback insights · `18586358` Smart web research · `18587045` Duplicate finder · `20637285` Format monday updates.

**Custom skills are authorable**: `manage_agent_skills action:"create" {name, content (markdown instructions), description}` — "creates a new custom skill in the **account-wide** catalog… available to all agents in the account." That is the injection point for our department playbooks.

### `manage_agent` (description, VERIFIED — not called with any write action)
> "monday platform agents are user-built work orchestrators on monday.com. Each has a profile, goal, and agent-level Identity. Jobs define specific work, instructions, and triggers. Agents in state ACTIVE can be triggered automatically. **They are NOT local LangChain or MCP agents.**"

Actions: `create` (AI-generated from a `prompt`), `create_blank`, `get` (one or list-owned), `update`, `delete` ("permanent and irreversible"), `activate`, `deactivate`, `run`. **"Created agents start INACTIVE"**; `run` is **"fire-and-forget. Returns trigger_uuid — no run-status query exists, treat successful enqueue as the only signal."** States: `ACTIVE | INACTIVE | ARCHIVED | FAILED`.

`agent_model` enum (VERIFIED): `CLAUDE_SONNET_4_6, CLAUDE_OPUS_4_7, CLAUDE_SONNET_5, CLAUDE_OPUS_5, CLAUDE_FABLE_5, GPT_5_2, GPT_5_6, GPT_5_6_LUNA, GPT_5_6_SOL, GEMINI_3_7_FLASH, GEMINI_3_5_FLASH_LITE, GEMINI_2_5_FLASH`. **monday runs the model; we do not supply a key and do not see token cost.**

`manage_agent_knowledge`: grants an agent `READ` or `READ_WRITE` on a **`BOARD` or `DOC`** — this is the per-agent permission boundary and it is exactly the T0/T1/T2 lever we want.

**Gap, VERIFIED:** every agent tool description points at `manage_agent_jobs` ("Do not put job-specific instructions in Identity. Configure them with manage_agent_jobs") — **but `manage_agent_jobs` is not exposed by this MCP server.** I searched the tool registry; only `manage_agent`, `manage_agent_knowledge`, `manage_agent_skills`, `manage_agent_triggers`, `agent_catalog` exist. So per-job instructions can only be set in the monday UI. `manage_agent_triggers` is described as "**Legacy** flat-trigger management … When jobs with instructions are enabled, use manage_agent_jobs".

### `connect_external_agent` (description, VERIFIED — not called)
> `{ custom: { name, callback_url? } }` — "Returns the new agent_id plus a one-time **signing_secret** and **api_token** used to verify webhook requests and call the monday.com API/MCP server — both are shown ONLY in this response". "Omitting callback_url creates the agent without a webhook — it won't be mentionable/assignable until one is added." "This tool is for CUSTOM agents only. For Claude, OpenAI, and other supported providers, use manage_agent."

So: an external agent is an HTTPS endpoint monday POSTs to **when it is @mentioned or assigned**, plus a token that lets our side call back into the monday API. Protocol details beyond that (payload schema, signature algorithm) — UNKNOWN; docs unreachable.

### `all_widgets_schema` — VERIFIED, 7 widget kinds
`APP_FEATURE, BATTERY, CALENDAR, CHART, GANTT, LISTVIEW, NUMBER`. Each returns a full JSON-Schema-7. `CHART` requires `graph_type` (pie/donut/column/bar/line/area/smooth_line/bubbles + stacked and percent-stacked variants), `x_axis_columns`, `y_axis_columns` (`default-label-count` to count items, or a numeric column id), optional `z_axis_columns` for stacking, `calc_function_type: sum|average|min|max|count`, `group_by: month|week|day|quarter|year` when `x_axis_group_by:"date"`. `NUMBER` requires `counter_data {calculation_type: columns|count, column_ids_per_board, counter_type: sum|average|median|min|max}` plus `number_format: number|percentage|currency` and a `counter_unit`. `BATTERY` requires `battery_data.status_column_ids_per_board` and a `done_text`. **That is the whole visualisation vocabulary — good enough for a KPI wall, not for anything analytical.**

---

## 5. Workflows

Descriptions only; nothing was created, validated against a real workflow, published or run.

- `create_workflow(workspaceId, title?, privacyKind: PUBLIC|PRIVATE|SHARE, description?, folderId?, ownerIds?)` → returns `workflowObjectId` + `workflowDraftId`. Creates an **empty** workflow.
- `invoke_workflow_expert(workflowObjectId, prompt, workflowDraftId?)` is how blocks actually get added: "answers questions about the workflow's structure and configuration, or **makes changes to it** (create, update, delete steps, and configure step fields)… **works on ONE workflow at a time.**" Field values "reference resources (boards, columns, people, channels, projects, …) **from monday or any external app** — all handled the same way… the expert resolves names to IDs and asks the user when it's ambiguous."
- `validate_workflow` (read-only) enumerates what the engine cares about, which is the best available inventory of block semantics: **"a missing trigger or action block, a delay/wait-trigger block left as a leaf, an empty loop, unknown blocks, missing required inputs, type mismatches between a variable and the field it's bound to, cross-branch node-results references, or invalid variable values."** So the engine has **triggers, actions, conditions, branches, loops, and delay/wait-for-event blocks**.
- `publish_workflow(workflowObjectId, workflowDraftId, shouldActivate=true)` — validates first; refuses and returns issues if unresolved.
- `run_workflow_once` — **"THIS PERFORMS REAL SIDE EFFECTS… items get created and updated, notifications and emails go out, external systems are called. Nothing is simulated and nothing is rolled back."** Mandatory sequence: `get_run_once_trigger_entities` → explicit user confirmation naming the entity → run. Statuses: `running | validation_failed | failed`; then poll `get_workflow_run_once_status` → `success | failure | exhausted | stopped | zero_actions | running | waiting | not_indexed_yet`, with per-block `errorReason`. `stop_workflow_run_once` is best-effort: "steps that already executed keep their effects".
- `invoke_process_planner` plans from scratch, "does NOT have access to any specific workflow's current state… It does not execute any changes."

**AI blocks / HTTP blocks / approval blocks: UNKNOWN.** No tool enumerates the block catalog, and the only ways to find out (calling `invoke_process_planner` or `invoke_workflow_expert`) were out of scope for a read-only pass. What *is* certain from the workflow evidence in this account: the live board automations use blocks `10380130` (when item created), `10380156` (**Notify someone**), `10505052` (**Set date**), `10676985` (**When date arrives**, with `dateTriggerConfig {hour, minute, timezone:"Asia/Jerusalem"}`) — VERIFIED from `list_automations`. Scheduling and notification blocks definitively exist; nothing observed proves an HTTP/webhook-out block or an approval block.

---

## 6. Automations

- `list_automations(boardId)` returns **two groups, VERIFIED**: `workflows` (manageable, cursor-paginated) and `legacyAutomations` — "**READ-ONLY** automations set up in an older way… they cannot be activated, deactivated, edited, or deleted, and manage-automations does not operate on them." Integration recipes (Meta Ads → create item) land in `legacyAutomations`. **Anything installed from the integrations store is invisible to our write path.**
- `create_automation(boardId, userPrompt)` takes structured natural language, not block ids: "The caller does not need to know the exact available automation blocks or their required fields." Constraints stated: **"Use one trigger. Conditions are optional. Multiple conditions mean AND. Use one or more actions. Do not use branching."** Returns `status: "needs_clarification"` with unresolved fields when it can't map intent. Recipe coverage is therefore *whatever monday's recipe store contains* — not enumerable through the API.
- `manage_automations(workflowId, action: activate|deactivate|delete)`.
- `get_automation_statistics` — **VERIFIED live, account-wide totals: `success=42, failure=14, total=56`.** `breakdown:"by_entity"` with `runStatus:"failure"` returned `{"183141726": {"total": 14, "automations.history.failed_trigger_details.error_reason.change_column_value_failed": 14}}` — i.e. it reports **run counts and typed error reasons, not an action budget.** No quota or remaining-actions figure is exposed anywhere I could find. UNKNOWN whether the Pro plan's automation-actions/month allowance is readable via API; `platform_api.daily_limit` covers API calls only.
- `get_automation_runs` — paginated run feed with state, duration, error reason; `mode:"detail"` by `triggerUuid` returns **block steps and MCP tool calls** (`includeToolEvents`). This is the closest thing to an audit trail for agent-driven automation and it is readable.

---

## 7. Docs

- `read_docs` (R). Two modes: `content` (full **markdown** content; `include_blocks` for block ids/types/positions, 25 blocks/page default; `include_comments` with block anchors and selection ranges) and `version_history` (restoring points newest-first, optional `include_diff`, `since`/`until`). VERIFIED description.
- `create_doc(doc_name, markdown, location)` — `location: "workspace"` (with `workspace_id`, `doc_kind: private|public|share`, optional `folder_id`, `docOwnerIds`) **or `location: "item"`** — VERIFIED: **"Creates a document attached to an item (requires item_id, optional column_id)… If not provided, the tool will create a new doc column automatically."** So yes: docs attach to items, and `docOwnerIds` exists specifically so an agent stays an owner ("Ownership is set inside the creation mutation itself, bypassing the permission checks that would block a subsequent add_subscribers_to_object call").
- `update_doc(doc_id | object_id, operations[≤25])`. Operations: `set_name`, `add_markdown_content` (append, or insert after a block — "Best for text, headings, lists, simple tables — no block IDs needed"), `update_block`, `create_block`, `delete_blocks` (1–100 per call), `replace_block`, `add_comment` (doc-level, block-level, or text-selection; HTML body; `mentions_list`).
  Block types creatable: `text` (NORMAL_TEXT / LARGE_TITLE / MEDIUM_TITLE / SMALL_TITLE / QUOTE), `list_item` (BULLETED / NUMBERED / CHECK_LIST), `code`, `divider`, `page_break`, `image` (public URL or `asset_id`), `video`, `notice_box` (INFO/TIPS/WARNING/GENERAL), `table` (≤25 rows × ≤10 cols), `layout` (2–6 columns).
  **Hard limits VERIFIED from the description:** `BOARD`, `WIDGET`, `DOC`-embed and `GIPHY` blocks — "**delete_blocks only (no public API to create these)**". Table cell-level nesting is not supported (must be created pre-populated via a markdown table); **layout columns "can only be created empty… No workaround exists to populate layout columns through the API."** Inline live column values are supported: `{insert: {column_value: {item_id, column_id}}}`, plus `mention` blots for `USER | DOC | BOARD`.
- Also at GraphQL level: `add_content_to_doc_from_markdown`, `create_doc_blocks`, `import_doc_from_html`, `export_markdown_from_doc`, `duplicate_doc`, `doc_version_history`, `doc_version_diff`, and `set_item_description_content(item_id, markdown)` — "Markdown does not support text colors or background highlights."

**Current state: `docs(limit: 25)` returns `[]` — this account has zero docs.** VERIFIED.

---

## 8. Vibe apps

`vibe_list` VERIFIED live → `{"apps": [], "page": 1, "limit": 50}` — **no Vibe apps exist in this account.** (There is a board literally named "Build Vibe app" with 0 items.)

From descriptions (VERIFIED, none called with a write action):
- `vibe_create(prompt, variant, workspace_id?, board_ids?, view_id?, model?)`. **Variants: `board_view`, `item_view`, `vibe_item_view`, `object`, `vibe_dashboard_widget`, `object_fullstack`, `monday_campaigns`.** So a Vibe app can be embedded **as a board view, as an item view, or as a dashboard widget**.
- Data model: `board_ids` — "Existing board IDs to connect… For multi-board variants (`object`, `object_fullstack`) these are connected as **data sources**; **the number allowed depends on your account tier**. For single-board variants… provide one board id, used as the host board. Omit to have a new board created automatically." **Boards are the database.** Whether the app reads them *live* at runtime is strongly implied ("connected as data sources") but not stated in so many words — REPORTED/partly UNKNOWN.
- Hosting: monday hosts it. `editor_link = https://{accountSlug}.monday.com/vibe/app/{appId}`. Generation is async (`created → generating → processing_message → deploying → ready`), driven by an LLM you may choose: `GEMINI_3_5_FLASH, CLAUDE_4_5_SONNET, CLAUDE_OPUS_4_6, GEMINI_3_7_FLASH, CLAUDE_5_SONNET, CLAUDE_OPUS_5`.
- `vibe_publication action:"publish"` — "requires the app to be deployed and **respects the published-apps license limit**". `vibe_ask` is a read-only Q&A against an app, blocking up to 45s.

---

## 9. `execute_code` and saved Actions

VERIFIED from descriptions:
- **Languages:** `javascript, typescript, python, bash`. Code ≤1 MB.
- **Auth:** "The sandbox has **authenticated access to the monday.com API**. You can make HTTP requests with GraphQL queries and mutations — **authentication is handled automatically**." So yes — this is the sync-script path, and no token has to live in our repo.
- **Network:** "restricted to the following hosts: **[api.monday.com/, mcp.monday.com/mcp]**. Requests to any other host (**or a different path on a restricted host**) will be blocked." **This kills the idea of using `execute_code` to call DataDoe, Amazon, QuickBooks or anything else. It is a monday-only sandbox.**
- **Lifecycle:** "**THE SANDBOX IS PER-CALL: a new empty container every call, destroyed when the call returns. Nothing written to disk survives, /tmp included.**" No state carries between calls.
- **Time limit: 300 s.** Files in (≤32, 512 KB inline each / 1 MB total, or by presigned URL), files out (`output_files` or `return_outputs` → up to 20 files, 25 MB each, 100 MB total, returned as presigned S3 URLs).
- **Failure semantics:** "A run that prints an error and exits 0 is recorded as a **success**. The monday.com API returns HTTP 200 with an `errors` array, so check the parsed body rather than the status code and raise when it is present."
- Recommended for: "Bulk / multi-item work — batch operations, dedup, aggregations, joins across boards (one script beats N tool calls)… File I/O — parsing uploaded CSV/XLSX to import items, producing downloadable exports."
- `create_action` saves such a script for reuse with a `vars_schema` injected as env vars, discovered/run later by `list_actions` / `run_action`. Same host allowlist. **VERIFIED live: `list_actions` → `{"actions": []}` — none saved.**

---

## 10. Existing account state (brief, no personal data)

**Workspaces (2)** — VERIFIED via `list_workspaces` / `workspace_info`:
- `6988200` **Main workspace** (default, created 2026-07-08), 1 board, 0 docs, 0 folders.
- `6988425` **Maree Real Estate Command** (created 2026-07-08), 4 boards, 0 docs, 0 folders, 3 subscribers.

**Boards (5, all `active`, all `public`, all `hierarchy_type: classic`, `items_limit: 10000`)**
| id | name | items | workspace |
|---|---|---|---|
| 5099972568 | Leads | 295 | Maree Real Estate Command |
| 5099974104 | Properties | 4 | " |
| 5099974105 | Deals | 1 | " |
| 5101138236 | Build Vibe app | 0 | " |
| 5099967845 | aa | 3 | Main workspace |

**`Leads` columns (16):** `name`; status × 6 (`Market`, `Type`, `Stage`, `Currency`, `Purpose`, `Language`, `Source` — 7 status columns in total); `numbers` Budget; `phone`; `email`; `date` × 2 (Last contact, Next follow-up); `long_text` Criteria/notes; `people` Owner; `board_relation` → Properties; `board_relation` → Deals. Groups: 4. Views: none returned. Note: the `Market` status column has 24 labels of which 21 are duplicate placeholders reading "Cyprus" — a real data-hygiene bug in the existing setup.

**`Deals` columns (12):** name; `board_relation` → Leads (single); `board_relation` → Properties (single); status Market/Stage/Currency/Probability; `numbers` Deal value, Commission expected; `date` Expected close, Next step date; `text` Next step.

**`aa` columns (4):** name, `people` Owner, `status` Status (Working on it / Done / Stuck / Not Started), `date` Due date. This is an untouched default template board.

**Automations:** `Leads` has **2 manageable workflows** — (a) when item created → notify the item's Owner + set `Next follow-up` to today; (b) when `Next follow-up` date arrives at 09:00 `Asia/Jerusalem` → notify the Owner. Plus **2 read-only legacy integration recipes**: Meta Ads lead forms → create item (recipe id 494, app `facebookAds`), mapping full name / phone / email into board columns. `Deals` has 0. Account-wide automation runs: 42 success / 14 failure; **all 14 failures come from one Meta Ads recipe with `error_reason.change_column_value_failed`** (it writes the literal text "Cyprus " into the `Market` status column — which is why that column is full of duplicate labels).

**Agents:** `manage_agent action:"get"` → `{"count": 0, "agents": []}`. **Zero agents exist.**
**Vibe apps:** 0. **Docs:** 0. **Saved actions:** 0. **Webhooks on Leads:** 0. **Dashboards:** none found.

---

## Implications for the design

1. **monday is a good control surface and a poor execution engine.** Everything the operating system needs to *show* Rami — a ranked decision list, per-department state, approvals with a status column, a KPI wall — maps cleanly onto boards, status columns, updates, notifications, `board_insights` and the 7 widget kinds. Everything the OS needs to *do* against Amazon, DataDoe, QuickBooks or a git repo has to happen on the Mac mini, because `execute_code` can only reach `api.monday.com`, and monday agents cannot hold our credentials.
2. **Build the hands runner as a monday client, not a monday resident.** The Mac mini polls/receives, does the Amazon work through DataDoe's MCP, and writes results back with `change_multiple_column_values` + `create_update`. `create_webhook` gives near-real-time signal for the approval loop: a `change_status_column_value` webhook on the Approvals board is the cleanest "Rami said yes" trigger available — no polling, no seat cost.
3. **The approval path is fully expressible.** Approvals board, one item per proposal, `status` column with `Pending / Approved / Rejected / Expired`, a `date` column for the 48-hour expiry, a doc or `long_text` holding the packet, `create_notification` to Rami's bell. T2 → T3 escalation is a status label. The 48-hour expiry can be a native automation ("when date arrives") — no code.
4. **Do not put numbers behind `formula` or `mirror` columns.** Both are read-only *and* unfilterable, so no agent can query on them. Write the computed value into a real `numbers` column from the runner. Mirrors are for humans to look at, nothing else.
5. **Budget: 10,000 API calls/day is the binding constraint, not complexity.** 20M complexity/minute is enormous; we burned 65 points on a normal page read. But filtered `items_page` queries cost ~5,000 each and every MCP tool call is a call against the 10,000/day. Nine departments × several runs/day is fine; a naive per-item loop is not. Prefer `execute_code` (one call, many GraphQL ops inside) or `update_items` (40 items per call) for bulk writes.
6. **monday platform agents are worth exactly one job: the scheduled nudge.** The `Every time period` trigger with an `Asia/Jerusalem` `schedulerConfig` is a free, hosted cron that can wake something at 07:05 local when Amazon's day closes. But `run` is fire-and-forget with no status query, `manage_agent_jobs` is not exposed here (so per-job instructions are UI-only), custom skills are account-global rather than per-agent, and the model is monday's — meaning cost and behaviour we cannot audit. Use monday agents for scheduling and human-facing summarisation; never for anything financial or irreversible.
7. **Second-brand instantiation is cheap and native.** `duplicate_board(duplicate_type: duplicate_board_with_structure)` per board, into a new workspace, plus `use_template`. The board/column layer of the OS is therefore genuinely portable, exactly as the constitution demands. Keep column *ids* stable across brands or the runner's config forks.
8. **Two seats is the real ceiling.** Everything above assumes the agents act as the connected user. There is no service-account seat in the plan (`create_service_user` exists in the schema but is an enterprise-shaped mutation), so all agent writes will be attributed to a human, which muddies `get_board_activity` as an audit trail. `ledger/actions.jsonl` in the repo remains the authoritative log; monday's activity log is a convenience copy.
9. **Fix the existing Meta Ads recipe before building on this account.** 14 of 56 automation runs fail because a legacy, unmodifiable integration writes free text into a status column. It has polluted `Market` with 21 duplicate labels. Legacy recipes cannot be edited via API — that one needs Rami in the UI.
10. **Docs are a decent knowledge surface, with one caveat.** Markdown in, markdown out, version history with diffs, comments anchored to text ranges, docs attachable to items, agents grantable `READ`/`READ_WRITE` per doc. But board-embed and widget-embed blocks cannot be created via API, and layout columns cannot be populated. Keep the compounding-knowledge layer in git (`memory/`, `playbooks/`) and mirror it into monday docs for reading, not the reverse.

## Open questions

1. **Does the workflow engine have an HTTP/webhook-out block or an approval block?** Unresolved — the block catalog is not enumerable read-only. If it has an outbound HTTP block, the Mac mini could be pull-free. Test with a single `invoke_process_planner` call (it changes nothing) before committing to the polling design.
2. **What is the Pro plan's automation-actions/month allowance and is it readable?** `get_automation_statistics` returns run counts and error reasons but no quota. If our automations are cheap this is moot; if we drive hundreds of runs/day it is a hard wall we cannot see.
3. **`connect_external_agent` protocol.** What exactly does monday POST to `callback_url`, how is `signing_secret` applied, and what can the returned `api_token` do? This is the most interesting integration path (mention `@Anabtawi Finance` on an item, our Mac mini answers) and it is completely undocumented from inside the MCP.
4. **Do Vibe apps read board data live at runtime, and how many boards may a Pro account connect?** "the number allowed depends on your account tier" — the number itself is not exposed.
5. **`ingest_items` (10k row limit, `on_match` upsert semantics)** looks like the right primitive for nightly Amazon-data sync. Its `OnMatchInput` shape was not inspected; worth one `get_type_details` before designing the sync.
6. **Write-side complexity budget.** I measured the read budget (20M/min) live but could not measure the write budget without writing. Docs say reads and writes are separate 5M budgets for app tokens and 20M for AI agents; whether the MCP connection's write budget is also 20M is UNKNOWN.
7. **Seat/attribution.** Can a monday platform agent hold its own identity for `get_board_activity` attribution on a 2-seat Pro plan, or does every agent write appear as the connected human? Determines whether monday's activity log has any audit value.
8. **`get_monday_knowledge` is limited to 10 questions per 10 minutes account-wide.** If several departments run concurrently and all consult it, they will starve each other. Cache its answers in the repo rather than asking at runtime.
