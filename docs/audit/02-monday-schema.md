# Audit — the monday.com workspace schema

Scope: `docs/monday-schema.yaml` against research 01/02, design §4–§5, `record-schemas.yaml`. Verified live with read-only monday MCP tools and the JSON schemas of `create_view`, `create_view_table`, `create_column`, `create_widget`, `create_dashboard`, `create_form`, `form_questions_editor`, `create_automation`. **Nothing was created, updated or deleted.** Account live: `tier: pro`, `active_members_count: 3` — design and brief both say 2 seats; find out who the third is before granting anything.

---

## BLOCKERS

**B1. Board views of type kanban / chart / timeline cannot be created at all — not by the API, not by `--init`.**
`get_type_details("BoardViewTypeValues")` returns exactly five values, VERIFIED live: `TableBoardView, CalendarBoardView, FormBoardView, DocBoardView, EmptyBoardView`; the MCP `create_view` narrows further to `TABLE | DASHBOARD | FORM | APP`. The YAML asks for `type: kanban` twice (`work_items`, `sku_profiles`), `chart` once (`scorecard_history`) and `timeline` once (`projects`). Research 01 §1 says Chart and Timeline *views* exist on Pro; it never says they are API-creatable.
**Fix:** delete all four. Kanban-by-class becomes a TABLE view with `settings.group_by.conditions[{columnId: class}]`. Timeline and chart exist only as dashboard widgets — a different object.

**B2. Six column ids are invalid and would be rejected by `create_column`.**
Custom ids are supported (`create_column(id:)`, REPORTED via developer_docs) but must be **1–20 chars, lowercase `a-z` and `_` only, unique, never reusable after deletion**. Digits are illegal. Invalid: `avg_4wk`, `firings_90d`, `units_7d`, `expiry_lt90`, `ad_spend_14d`, `tacos_14d`. `work_items.subitems.steps` also contains the literal entry `status(Todo|Doing|Done)`, not an id.
**Fix:** rename to `avg_four_wk`, `firings_ninety_d`, `units_seven_d`, `expiry_lt_ninety`, `ad_spend_fourteen_d`, `tacos_fourteen_d`; give steps a typed column list. Add a CI check for `^[a-z_]{1,20}$`. Because ids are not reusable, a half-failed `--init` cannot be re-run on the same board: it must read existing columns first, or drop and recreate the board.

**B3. The MCP `create_column` tool cannot set an id, so §4.1 principle 5 fails as written.**
The tool takes `boardId, columnType, columnTitle, columnDescription, columnSettings` — no `id`; only raw GraphQL accepts one. And 202 of the 233 columns have **no `title`**, so an MCP-based `--init` would title-case ids and let monday auto-generate `text`, `text0`, `status_1`…, leaving the projection addressing columns that do not exist.
**Fix:** `--init` goes through `all_api_write` raw GraphQL with an explicit `id:` on every column and writes back `docs/monday-ids.json` (schema id → board id, group id, real column id) that departments resolve at boot. Add a `title` to all 202 columns — the title is what Rami reads on the phone.

**B4. `bin/project-monday.py` does not exist.** `bin/` contains only `README.md`. This whole file is a plan for a script nobody has written; say so in the header, or it reads as if the workspace is one command away.

**B5. Dashboard widgets cannot be filtered through the API — every filtered widget in the YAML is unbuildable.**
`all_widgets_schema` (VERIFIED live) returns 7 kinds; every settings schema is `additionalProperties: false` with **no filter property**, and `create_widget` takes only `parent_container_id, parent_container_type, widget_kind, widget_name, settings`. Consequences:
- `NUMBER` accepts only `counter_data {calculation_type: columns|count, column_ids_per_board, counter_type: sum|average|median|min|max}`. So every filtered NUMBER in the YAML — `count {group: Today}`, `min cover_days filtered to Hero`, `count status [Blocked, Waiting on Rami]`, `count Validated within 30d` — is impossible, and `{value: {metric_id: net_revenue_ca_7d}}` doubly so: there is no "value of one named item" widget.
- `LISTVIEW` settings contain no board and no view reference, so `{kind: LISTVIEW, board: decisions, view: Today}` cannot be expressed.
- `CHART` requires `graph_type, x_axis_columns, y_axis_columns` as `{board_id: [column_id]}` maps; the YAML writes scalar `x:`/`y:` and omits `y_axis_columns` on the donut. `group_by` is legal only when `x_axis_group_by == "date"`, enum `month|week|day|quarter|year` — so `scorecard_history.group_by: metric_id` is doubly invalid. Stacking by metric needs `z_axis_columns` on a stacked graph type.
- `{filter: {margin_pct: below margin_floor}}` compares two columns. monday filters compare a column to a literal, never to another column — impossible on any surface.
- The Finance widgets (cash available, PO ceiling used, TACoS, reimbursements pending) and the US Launch widgets (SKUs through gate, slack days, readiness by gate) name no board and no column. They are captions, not specs.
**Fix:** rewrite `dashboards:` in the real widget grammar, mark every filtered widget `manual: true` (a one-time UI click after `--init`), and replace "value of one metric item" with a plain Numbers column the build writes.

**B6. Date-range view filters ("Due ≤3 days", "within last 7 days") do not exist.**
`get_column_type_info(date, guidelines)` VERIFIED live: date supports only `any_of, not_any_of, greater_than, lower_than` with `["EXACT","YYYY-MM-DD"] | TODAY | TOMORROW | THIS_WEEK | ONE_WEEK_AGO`. `create_view`/`create_view_table` document no `within_the_next`/`within_the_last` operator at all. So `tasks_for_rami` "Due ≤3 days" — one of the two Cockpit list widgets — and `knowledge` "What changed this week" and "Up for review" cannot be built.
**Fix:** the nightly build writes a filterable status column (`due_soon` on Tasks, `changed_recently` on Knowledge). Compute the window in the repo, where the timezone is already right.

**B7. The "Ask the company" form cannot be built as specified.**
(a) `create_form` "also creates a backing board to store responses" — it takes `destination_workspace_id`/`destination_name`, not an existing `board_id`, so it cannot write into a hidden group on Requests. (b) Question types are wrong: `form_questions_editor` enumerates 24 types (`LongText, ShortText, SingleSelect, MultiSelect, Number, Date, …`); the YAML uses monday *column* types (`long_text`, `dropdown`, `text`, `status`), none of which are valid. (c) Requests has no column for `question`, `about`, `sku`, `urgency` or `wants`.
**Fix:** the form gets its own board, "Ask the company", with columns matching the questions; question types become `LongText, SingleSelect, ShortText, SingleSelect, SingleSelect`; the projection reads that board into `requests/ceo/inbox/`. Drop `hidden_group`.

**B8. "Board owner only" is not a monday permission, and it contradicts §4.2.**
Research 01 §10 (VERIFIED) lists the Pro permission sets: *Edit everything / Only edit content / View and comment*, plus *Only edit assigned items*. There is no owner-only set — it means a **Private board**. But §4.2 says all boards are Main so the workspace can be templated for brand two, and research 01 §1 states VERIFIED that templates carry **only Main boards**. `owner_only: [decisions, suppliers_pos, strategy, key_results, initiatives]` and the brand-two template plan cannot both hold. The block also self-contradicts: `viewers_later` grants `decisions(view)` while `owner_only` includes `decisions`; and `guests_later` puts a guest on `wholesale_pipeline`, but guests require **Shareable** boards, again not Main.
**Fix:** drop the permission section for v1 — all boards Main, with a note that owner-only costs the template and guest boards must be Shareable. Decide at month three.

**B9. Two overlapping state machines per board, with no rule for who moves items between groups.**
Decisions: groups `Today · This week · Deferred · Executed · Closed` vs status `Pending · Approved · Rejected · Deferred · Expired · Executing · Executed · Failed`. No automation moves items between groups, so the "History" view (`group: [Executed, Closed]`) stays empty forever and the Cockpit's "Decisions today" count grows without bound. Work Items: groups include `Done`, status does not (it has `Answered`); status has `Answered/Superseded/Escalated`, groups have none — and the `needed_by` automation says "status not Answered/Done" where `Done` is a group.
**Fix:** status is authoritative; groups are for phone scanning and are moved by the projection every run. Make the group set a strict function of the status set.

**B10. "monday writes the repo through exactly two doors" (§4.1) is false in this same schema.**
Six write-back paths exist: `decisions.decision`, `decisions.snooze_until`, `tasks_for_rami.status`, `work_items.status` ("reads back only the status Rami may set", §4.11), `strategy.proposal`, `suppliers_pos.po.paid_on`.
**Fix:** enumerate them in the YAML as a `read_back:` list and make it the poller's only allowlist.

**B11. `sku_profiles` declares two subitem structures.** A board has exactly one subitems board, so `cost_rows` and `competitors` cannot both be subitems of SKU Profiles.
**Fix:** cost rows stay in `products/<sku>.md` (`record-schemas.yaml:105`) and never enter monday; competitors become the subitems. Note AGENTS.md Hard Rule 2: competitor rows must come from Product Pricing or Keepa only — the `source` field allows that but does not enforce it.

**B12. Telegram.** §4.6 ("the same failure also goes to Telegram from the wrapper") and §9.3 step 6 ("monday push and Telegram carry the card") contradict the standing constraint: monday notifications only. Every alert path here must be a monday automation or `create_notification`. Delete the Telegram references, or the automation table understates what monday must carry.

---

## MAJOR

**M1. `decided_at` as `last_updated` is wrong.** `last_updated` fires on *any* column change, so the nightly rewrite of `rank`/`score` overwrites it and `decided_at` becomes meaningless. The correct source is VERIFIED: `StatusValue.updated_at` on the `decision` column, read in the same poll. Delete the column.

**M2. `card: true` is not a monday concept.** Thirteen `sku_profiles` columns carry it, but nothing pins columns to the mobile item card. The only mechanism is column order (§5.5 admits this); `column_order_first_three` *is* buildable via `create_view_table.settings.columns.column_order`. Delete `card:`, keep the order.

**M3. `products.listings` and `sku_profiles.product` are one relationship declared twice.** A connect-boards column can auto-create the mirrored column on the target board; declaring both yields four columns and duplicated linkages. Declare one side, mark `creates_reverse: true`. Separately: **Pro's 20-connected-boards ceiling is not breached** — worst case is Key Results at 6 distinct connected boards. Say so in the YAML so nobody re-litigates it.

**M4. Status filters need numeric label indexes, not text.** VERIFIED in research 02 §3: `any_of ["New"]` returns zero rows; label text works only with `contains_terms`. Every `filter: {status: Red}` in this file is text. `--init` must create the column, read back the label ids, then create the view. (`create_view_table.conditional_coloring` resolves human-readable values; filters do not.)

**M5. Columns the build must write that no record defines.** `sku_profiles.fba_available`, `inbound`, `listing_health`, `cogs_status`, `top_keyword`, `owner_dept`, `next_action` (the rule set is nowhere), `products.category`, `unit_dims`, `pkg_dims`, `decisions.rank`, `decisions.dry_run`, and `requests.type` labels (the record has an 8-value enum the YAML leaves blank). Worse, `record-schemas.yaml:95` defines `sku_snapshot` as "the board's 34 columns" — the record depending on its own projection, the inversion §8 forbids. Give `sku_snapshot` an explicit field list and derive the board from it. Record fields with no column: `decision_item.goal_id`, `type (approve|choose|ratify)`, `impact_basis`, `deadline_reason`, `reproposal_of`, `times_reproposed`.

**M6. `decisions.outcome` cannot represent `unmeasurable`.** Labels are `Pending · Hit · Miss · Inconclusive`; the `ledger/outcomes.csv` verdict enum is `hit, miss, inconclusive, unmeasurable`, and `unmeasurable` is defined as a schema bug that opens a finance work item. Add the label.

**M7. `suppliers_pos.country` is a `country` column; the supplier record stores a plain string.** The write shape needs `{"countryCode","countryName"}`, both required. Store the ISO code in the record or make the column `text`.

**M8. Two automations require branching, which `create_automation` forbids** ("Use one trigger… Multiple conditions mean AND… **Do not use branching**", VERIFIED). "Milestone due arrives and status not Done → set Late, **notify only if gate**" must be split in two. "Decision changes to Deferred → set `snooze_until` +7 days **if empty**" depends on a "set date N days from now" recipe that is not enumerable through the API (research 02 §6); the blocks observed live here are `when item created`, `notify someone`, `set date`, `when date arrives`. Mark it UNKNOWN; let the CEO run set `snooze_until` in the repo.
The rest are expressible: item-created-in-group → notify; status-changes-to → notify; when-date-arrives + condition + set-status + notify (`dateTriggerConfig {hour, minute, timezone: "Asia/Jerusalem"}` VERIFIED here); subitem-status-changed → set date + notify. Self-notification does fire for your own changes (REPORTED by monday's KB) but depends on Rami's personal settings having automations on. Test it day one — the alerting design rests on it.

**M9. `api_budget` is asserted, not shown, and contradicts itself.** `daily_calls_pro: 10000` is VERIFIED. But `never_at_runtime: [filtered items_page in loops]` is violated by the design's own 5-minute approvals poll (§9.3 steps 5 and 8) — 288 filtered reads a day at ~5,020 complexity each. That is comfortable against 10,000 calls and 20M complexity/minute; the *rule* is wrong. A personal API token also shares **one 10M/min budget across reads and writes** (research 01 §6), budgeted nowhere. `--init` alone is ~370 calls (18 boards, 229 columns, ~40 subitem columns, groups, views, widgets), with `create_board` capped at 40/minute. And `ingest_items` is not a drop-in mutation — it returns a job id and an upload URL; `update_items` (≤40 items/call) is the right nightly primitive.
**Fix:** replace `never_at_runtime` with a budget table — init ~370 one-time; nightly SKU sync 3 calls for 120 rows; poll 288; run health 9; departments ~200. Under 600/day steady state.

**M10. Column counts disagree.** §5.3 is titled "34 columns" and lists 36 rows; §4.3 repeats "the 34 columns"; the YAML lists 35 (omitting `name`). Pick one.

---

## MINOR

- Five dropdowns have no labels (`products.brand`, `products.category`, `strategy.quarter`, `requests.type`, `projects.subitems.owner_dept`); the header only promises labels for status columns.
- Four boards use typed subitem column lists, two use bare name lists (`work_items.steps`, `sku_profiles.cost_rows`/`competitors`).
- `projects.subitems.milestones` has both `timeline` and `due`; the timeline already carries the end date.
- `run_health.writer: run_wrapper` — not one of the nine departments, not defined in `AGENTS.md`.
- Naming drift with no mapping written down: `value`/`target_num` vs the record's `current`/`target`; `effort_est` vs `effort_est_min`; `owner_dept` vs `owner`.
- `scorecard_history.week` is redundant: the only view over it charts `as_of`, and `get_column_type_info(week, guidelines)` returns `filter: null` — `week` cannot be filtered server-side.
- `decisions.dry_run` is `long_text`, capped at 2,000 characters (VERIFIED). A before/after table overflows silently — put the diff in the linked packet.
- Views on `key_results`, `tasks_for_rami`, `work_items` and `projects` omit `type`. Default them to TABLE.
- Dashboard `boards:` lists are stale: Cockpit declares 5, its widgets reference 8. Pro allows 20 boards and 30 widgets per dashboard, so there is headroom.

---

## The minimum to build tonight

Four boards, one dashboard, three automations. No folders, relations, subitems, docs or form. Every name and id below is final, so each later addition is a new column, never a rename. **Ids cannot be reused after deletion.** Workspace `Anabtawi OS`, all boards `boardKind: public` (Main), built with raw GraphQL `create_column(id:…)` through `all_api_write`, writing `docs/monday-ids.json` as you go.

**1. `Decisions`** — groups `Today, This week, Deferred, Done`.
`dec_id` text, `decision` status (Pending, Approved, Rejected, Deferred, Expired, Executing, Executed, Failed), `rank` numbers, `tier` status (T2, T3), `dept` dropdown (nine departments), `impact_cad` numbers, `expires` date+time, `if_ignored` long_text, `evidence` long_text, `approval_file` link.
View **"Today"**: TABLE, filter group `Today`, sort `rank` asc, column order `decision, if_ignored, impact_cad, expires`.
Automations: item created in group Today → notify Rami; `decision` changes to Approved or Rejected → notify Rami.

**2. `SKU Profiles`** — item name `<SKU>, <MARKET>`; groups `Hero, Core, Long-tail, Kill, Planned`.
`next_action` status (Nothing, Watch, Reorder now, Approve price, Fix listing, Review reviews, Blocked), `cover_days` numbers, `margin_pct` numbers, `price` numbers, `units_seven_d` numbers, `fba_available` numbers, `tacos_fourteen_d` numbers, `bsr` numbers, `rating` numbers, `marketplace` status (CA, US, WMT), `class` status (Hero, Core, Long-tail, Kill), `listing_health` status (Live, At risk, Suppressed), `data_health` status (Fresh, Stale, Broken), `data_asof` text.
View **"Rami — today"**: TABLE, filter `next_action not_any_of [Nothing]`, sort `cover_days` asc, `column_order` starting `next_action, cover_days, margin_pct`. (The "or data_health = Broken" arm needs a second view or a build-written flag — a view filter is one boolean operator, not a tree.)

**3. `Run Health`** — nine items, one per department.
`status` status (OK, Stale, Failed, Paused), `last_run` date+time, `state_date` date, `harness` dropdown (claude-code, codex, routine, grok), `tools_failed` text, `log` link.
Automation: `status` changes to Failed or Stale → notify Rami.

**4. `Tasks for Rami`** — groups `This week, Next, Waiting, Done`.
`status` status (Open, Done, Won't do), `due` date, `due_soon` status (No, Under three days, Overdue) *written by the build, because the date-window filter does not exist*, `why_human` long_text, `est_minutes` numbers, `consequence` long_text, `dept` dropdown, `evidence` link.
View **"Due soon"**: TABLE, filter `due_soon any_of [Under three days, Overdue]` AND `status not_any_of [Done]`.

**5. Dashboard `Cockpit`** — `board_ids` = those four. BATTERY over `Run Health.status` with `done_text: "OK"` ("Company alive"), NUMBER min of `cover_days`, NUMBER average of `margin_pct`, NUMBER count on Decisions, LISTVIEW Decisions, LISTVIEW Tasks for Rami. The four filters those widgets want (group Today, class Hero, view Today, due soon) are **one-time UI clicks after `--init`** — there is no API for them. No CHART, GANTT or CALENDAR tonight.

**Waits, at no cost:** the other fourteen boards, the Ask-the-company form and its board, the Finance and US Launch dashboards, all docs, every `board_relation`, every subitem board, and the permissions section. A board added later is one `create_board`; a relation is one `create_column` per side. Nothing above needs renaming to accommodate any of it.
