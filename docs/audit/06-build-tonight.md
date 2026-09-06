# Audit 06 — Feasibility of a minimal working core tonight; build order (§13, §11)

Scope: can a working core be built in one evening on Rami's MacBook, and does §13/§11 support that. All monday checks below were read-only (`get_user_context`, `list_workspaces`, `workspace_info`, `get_board_info`, `all_widgets_schema`, plus tool *schemas* read without calling). Nothing was created or modified.

---

## Findings

### BLOCKER 1 — §13 week 1 is not executable: every artifact it names is absent
`bin/` and `hands/` contain a README each and no code. Zero of the 17 `prompt:` files referenced across the nine `department.yaml` files exist (`departments/*/prompts/` is `.gitkeep`). No `.mcp.json` exists anywhere. All nine charters are stubs — `departments/finance/AGENTS.md`: "(To be written from docs/ANABTAWI-OS-DESIGN.md §6 … at build time, week 1.)". The constitution's run procedure (`AGENTS.md` §7) additionally requires `requests/<dept>/inbox/` (**no `requests/` directory on this branch**), `strategy/CURRENT.md` (only `STRATEGY.md` exists), `state/calendar.md`, `state/locks.md`, and `docs/CONVENTIONS.md` (referenced by §9 and design §6.4; does not exist). A department run tonight fails at step 1 (no `run-dept.sh`) and again at step 3 (no inbox).
**Fix:** add to §13 a numbered "before any run can happen" list of exactly six files — `bin/run-dept.sh`, one `prompts/daily.md`, one filled charter, `.mcp.json`, `strategy/CURRENT.md`, `state/calendar.md` — and create `requests/`, `state/locks.md`, `docs/CONVENTIONS.md` as empty-but-present.

### BLOCKER 2 — the stable column ids the whole schema rests on cannot be created through the monday MCP
`create_column`'s schema (read today) accepts `boardId, columnType, columnTitle, columnDescription, columnSettings` — **there is no `id` parameter**. Confirming evidence in this account: `Leads` (board 5099972568, in a workspace whose own description says "Built via the monday MCP") carries `color_mm526wdm`, `numeric_mm522ymv`, `date_mm52630p` — auto-ids. Design §4.1 principle 5 ("Every column is created with an explicit id … so brand two and the runner share one config"), all of `docs/monday-schema.yaml`, and §12's brand-two story depend on ids that this path cannot set. The raw-GraphQL escape (`all_api_write` → `create_column(id:)`) is untested here and carries two traps the schema already violates: monday ids are `[a-z0-9_]` ≤20 chars, and `status` — used as a column id on six boards in the schema — collides with the default Status column monday creates on a new board.
**Fix:** drop the principle. Create columns by *title*, read ids back with `get_board_info`, write them to `ops/monday-ids.json`, and make that file the contract the projection and the poller both load. Add "column titles are the stable identifier; ids are cached" to §4.1.

### BLOCKER 3 — the Cockpit widgets in `monday-schema.yaml` cannot be built as specified
From `all_widgets_schema` today: `NUMBER.counter_data` has **no filter and no group selector** (only `calculation_type`, `column_ids_per_board`, `counter_type`); `CHART` has **no filter property** at all; `LISTVIEW` settings contain only display options — **no board and no view binding**. Therefore `{NUMBER, count: {group: Today}}`, `{NUMBER, min: cover_days, filter: {class: Hero}}`, `{NUMBER, value: {metric_id: net_revenue_ca_7d}}`, the filtered 13-week `CHART`, and `{LISTVIEW, view: Today}` are all unbuildable. Only `BATTERY` (has `groups_data`) and `CALENDAR` support filtering. Six of the Cockpit's eleven widgets are fiction.
**Fix:** add a one-item board **Cockpit** whose Numbers columns the projection writes (`decisions_today`, `min_hero_cover`, `margin_after_ads`, `net_rev_7d`, `depts_ran`), and point every NUMBER widget at one column of it (`counter_type: max` over a one-row board returns that value). Keep BATTERY on Run Health. Rewrite `dashboards.cockpit` accordingly.

### BLOCKER 4 — two live constitutions in one repository
`origin/main` carries a different `AGENTS.md` ("Anabtawi Company — Constitution") and a different layout (`runtimes/`, `shared-skills/`, `requests/`). `origin/anabtawi-os` carries this one. `CLAUDE.md` on both is `@AGENTS.md`, so whichever branch Rami clones tonight silently becomes the law. Neither README says the other is superseded.
**Fix:** tonight, before any clone: merge `anabtawi-os` into `main` or push a one-line "superseded by branch anabtawi-os" into `main/README.md`.

### BLOCKER 5 — the monday MCP connection available for the build is not Rami's
`get_user_context` returns user `110208327` "maree khalila"; Rami is `108169876`. Boards created from this connection are owned by Maree. Design §4.8 ("Rami: admin, owner of every board") and the Decisions permission rule ("never grant edit rights on the Decisions board to a seat or guest") are violated from the first minute, and the approval audit trail attributes Rami's taps to the wrong account.
**Fix:** pass `boardOwnerIds: ["108169876"]` on every `create_board`, and have Rami re-check board ownership before the first packet. Better: build from Rami's own connection.

### MAJOR 6 — Telegram is load-bearing in five places and the brief forbids it
Design §3 (diagram), §6.3 step 7 ("posts one line to Telegram"), §7.6 (P0 lane "via Telegram and monday push"), §10.1 ("a Telegram line only if a P0 fired"), §11.1 (stack row). The brief: "No Telegram, no Slack: monday notifications only."
**Fix:** strike all five; replace the P0 lane with `create_notification` plus a Run Health status change to Failed, and say explicitly that a P0 that fires while monday is unreachable is *lost* — that is the accepted cost.

### MAJOR 7 — `bin/project-monday.py` is cited as if it exists and is never specified
Named in README, §4.10 (the exit path), §9.3 step 6 (how a decision reaches Rami) and §12 (how brand two is instantiated). It does not exist and the design never states its input→output contract: which columns it writes, how it resolves board and column ids, what it does on a title collision, what it reads back. The single most load-bearing script in the design is a filename.
**Fix:** ten-line spec in §4: reads `docs/monday-schema.yaml` + `ops/monday-ids.json`, upserts by `dec_id`/`wi_id`, writes only columns whose `writer` is a repo process, never deletes, exits non-zero on an unresolved id.

### MAJOR 8 — the approval packet schema and the constitution disagree
`docs/schemas/approval-packet.schema.json` `required` omits the four scoring fields `AGENTS.md` §6.7 demands ("Every proposal names the metric that will judge it, the expected value, the review date and the measurement design") — they appear only in `record-schemas.yaml` as `scoring_fields`, which is not the validator. And the schema's field is `if_rejected` while the monday column, the card format (§10.2) and the `decision_item` record all say `if_ignored`. A packet written tonight validates and still breaks the constitution, and the projection reads a key that is not there.
**Fix:** add `metric, expected, review_on, design` to `required`; pick one of `if_ignored` / `if_rejected` and change the other three places.

### MAJOR 9 — §13's week 1 cannot start tonight and has no internal order
Week 1 bundles Mac mini setup, vault, `setup-token`, Healthchecks, Telegram, repo layout, nine `department.yaml`, generated `.mcp.json`, watchdog, pre-commit scan, ledger verifier, full DataDoe verification, the whole monday workspace and the Meta Ads recipe fix behind one exit test. The Mac mini **arrives next week**, so half of it is blocked; nothing inside it is ordered; and the exit test ("every department runs once") gates on nine charters and nine prompts that do not exist. It is a list, not a build order.
**Fix:** replace with the day ladder in §D below.

### MAJOR 10 — account facts have already drifted from §4.1/§11.1
`active_members_count` is **3** today, not the 2 the "grandfathered 2-seat bucket" assumes (research 02 recorded 2 on the same date). The account also holds two workspaces and a 295-item production CRM (`Maree Real Estate Command`); §4.2 says nothing about coexisting with them. **Fix:** one line in §4.2, and re-check the seat count before relying on the Pro seat maths.

### MAJOR 11 — §11.1 does not mark which tools the first working core needs
Nineteen tools, eight unbought or unregistered, no "minimum viable" marker; the core needs four — monday Pro, Claude Max, DataDoe, git. **Fix:** add a `core / week-2 / later` column.

### MINOR 12–15
§4.2's folder table omits Scorecard History, which `monday-schema.yaml` puts in "1 Command" — 17 boards from one file, 18 from the other. · `ledger/kpis/README.csv` has 10 columns; `record-schemas.yaml:kpi_row` specifies 17. · `staleness.yml` hard-codes all nine departments, so with one live it fails every morning and trains Rami to ignore the watchdog — read the list from a file. · `AGENTS.md` §5 says the ratchet is confirmed in `department.yaml`; design §6.1/§9.2 say `AGENTS.md`.

---

## A. What can genuinely be built and demonstrated in four hours

Yes, all four, in this order, if scope is cut as in §E:

1. **The monday workspace** — 3 boards, not 18; ~28 columns, not ~250; one dashboard, 5 widgets; 0–1 automations; no views, forms, docs or subitems. Creation is one MCP call each; the cost is verification.
2. **One department headless against DataDoe writing a state file** — `claude -p` with a `.mcp.json` holding the DataDoe key from an env var. Use **supply-chain**: one VERIFIED table (`amazon_fba_inventory_health`, research 08 §4, from DataDoe's own `restock-priority-alert` SKILL.md) and the clearest T2 packet (a reorder proposal).
3. **Projection into monday** — a ~120-line script writing Run Health + Cockpit numbers and upserting Decisions items via a monday API token and `ops/monday-ids.json`.
4. **Proposal → tap → poller** — a second ~80-line script polling the `decision` column, moving `approvals/pending/<id>.md` → `approved/`, stamping `decided_by`, `decided_at`, `decision_channel: monday`, committing and pushing.

That demonstrates the whole spine: repo → department → packet → monday → human tap → repo. Nothing touches Amazon.

## B. What is genuinely not possible tonight

- **Any DataDoe verification from this session.** No DataDoe tools are exposed here; the key is on Rami's machine. Every DataDoe claim in the design is REPORTED or VERIFIED-from-GitHub, never tested in his account. And if the Amazon account was connected recently, research 08 §4 says the daily fetch runs 02:00–~05:00 marketplace time — a same-day connection may return **zero rows tonight**. Step 3 below tests this first.
- **SP-API private developer app and Ads API self-service** — Amazon-side approvals; §14.2 lists the timeline as UNKNOWN. Submit, do not wait.
- **Keepa** (€49, not bought) → pricing-intel cannot run. **QuickBooks MCP** (Intuit OAuth) → finance has no cash data. **Official Ads MCP** (no credentials) → advertising has no write path even in dry-run.
- **A reliable schedule.** Research 10 §10.3: launchd jobs and Desktop tasks both skip when the machine sleeps, and the fix (`pmset -a disablesleep 1`, auto-login `ops`, `caffeinate`) is Mac-mini setup. On a laptop that closes, run manually or in a foreground `while … sleep 300` loop.
- **Any real Amazon write** — correct by design (research 08 §6: types disabled by default, `dryRun` works anyway). Tonight's "execution" is a dry-run diff.
- **1Password `op run`** — not installed. Tonight: `~/.anabtawi/env`, `chmod 600`, outside the repo. Log as debt in `ops/OPERATING-NOTES.md`.
- **The 34-column SKU Profiles board**, the nightly build, the CEO scoring function, the hands runner, the ledger hash chain, `validate.py`, work items, projects, knowledge.

## C. Exact sequence for tonight

| # | Who | Step | Input from Rami | Min | Test that proves it worked |
|---|---|---|---|---|---|
| 0 | Rami | Resolve the two constitutions (BLOCKER 4): merge `anabtawi-os` → `main`, or note supersession in `main/README.md` | decision | 5 | `git clone` + `cat CLAUDE.md` on the MacBook loads the OS constitution |
| 1 | Rami | monday: profile → Developers → generate a **personal API token**; note his user id `108169876` | token | 5 | `curl` a `me { id }` query returns 108169876 |
| 2 | Rami on MacBook | Clone repo; write `~/.anabtawi/env` with `DATADOE_MCP_KEY` and `MONDAY_TOKEN`; `chmod 600` | DataDoe key | 10 | `claude mcp` lists `datadoe`; `sellers_and_vendors_list` returns the CA seller |
| 3 | Claude Code on MacBook | `exports_sources_get`; hard-code the table + column names for FBA inventory health into the department prompt; paste the table list into `ops/OPERATING-NOTES.md` | — | 20 | one `exports_create` returns ≥1 row **for yesterday**; if zero rows, stop and use a fixture |
| 4 | Claude (build session) via monday MCP | Create workspace `Anabtawi OS`, 3 boards with `boardOwnerIds:["108169876"]`, columns by title, groups; read ids back and commit `ops/monday-ids.json` | — | 30 | `get_board_info` returns every column; Rami sees the boards on his phone |
| 5 | Claude (build session) via monday MCP | Create dashboard **Cockpit**: BATTERY over Run Health `status` (done `OK`) + 4 NUMBER widgets over the one-item Cockpit board | — | 15 | all five widgets render a number, not an error |
| 6 | Claude Code on MacBook | Write `bin/project-monday.py` (repo → Run Health, Cockpit, Decisions upsert by `dec_id`) | — | 40 | run it with the repo empty: Run Health shows one item, status `Stale` |
| 7 | Claude Code on MacBook | Write `departments/supply-chain/prompts/daily.md`, fill its charter, `.mcp.json`, `bin/run-dept.sh`; run `claude -p` headless | confirm cover floor 14d | 45 | `state/supply-chain.md` dated today + one `approvals/pending/<id>.md` validating against the packet schema |
| 8 | Claude Code on MacBook | Run the projection | — | 5 | the packet appears as a Decisions item in group **Today** with `if_ignored`, impact and a GitHub link |
| 9 | Rami on phone | Open the item, tap `decision` → **Approved** | 1 tap | 2 | the status shows Approved |
| 10 | Claude Code on MacBook | Write and run `bin/poll-decisions.py` | — | 30 | file moved to `approvals/approved/`, `decided_by`/`decided_at`/`decision_channel: monday` stamped, committed and pushed |
| 11 | Rami | Confirm in DataDoe Settings → Actions that **every action type is disabled** | 1 min | 5 | screenshot pasted into `docs/policy/` |

≈3h20 of work plus slack. Guardrail numbers, Keepa, QBO, the vault and the Mac mini are all out of tonight's path.

## D. Replacement for §13 — a day ladder, one capability a day

- **Day 1 (tonight): the approval loop.** §C. Exit test: a proposal born in the repo is approved on a phone and the file moves; nothing executed against Amazon.
- **Day 2: truth.** Nightly build: DataDoe exports → `state/skus/<date>.jsonl` and `ledger/kpis/<month>.csv`; **SKU Profiles with 8 columns** (sku·marketplace, next_action, cover_days, fba_available, units_7d, price, margin_pct, data_health), not 34. Submit the SP-API and Ads registrations today — they take days. Exit test: the board matches the export.
- **Day 3: the card.** finance and advertising at T0; the CEO run — gate, score (§7.4), cap 3 — writing `briefs/<date>-decisions.md` and the Cockpit numbers. Exit test: ≤3 ranked items, each citing an export id.
- **Day 4–5: it runs without Rami.** `bin/validate.py`, the ledger hash chain, the watchdog reading its department list from a file, a foreground runner loop. When the Mac mini lands: `ops` user, `pmset`, `claude setup-token`, launchd, vault. Exit test: three consecutive days of dated state files Rami did not trigger.
- **Week 1 (rest): breadth and safety.** The other six departments as thin T0 runs; the hands runner at `dryRun:true` only; kill-switch drill; BSA §19 and Anthropic terms into `docs/policy/`; Keepa and QBO bought or deferred with a reason.

Rule that replaces the week grid: **one new capability a day, each with a test Rami can run in under a minute, and nothing is added while yesterday's capability is red.**

## E. Day-1 cut list

**Boards — 3 of 18.** `Decisions` (groups: Today, Decided; columns `dec_id, decision, dept, tier, impact_cad, expires, if_ignored, evidence, approval_file, repo_path` — 10 of 25); `Run Health` (`last_run, state_date, status, tools_failed, log` — 5 of 8, one item); `Cockpit` (new, one item "Today": `decisions_today, min_hero_cover, margin_after_ads, net_rev_7d, depts_ran`). **Deferred: 15** — Strategy, Key Results, Initiatives, Scorecard, Scorecard History, Tasks for Rami, Work Items, Projects, Products, SKU Profiles (day 2), Suppliers & POs, Knowledge, Calendar, Requests, and both "4 Later" boards.

**Dashboards — 1** (Cockpit, 5 widgets). **Automations — 1** ("when item created in group Today → notify Rami"); if `create_automation`'s natural-language path does not produce it in two attempts, ship zero — the poller does not depend on notifications. **Forms 0, docs 0, views 0, subitems 0, workflows 0, agents 0** (note: the existing MCP-built board in this account has `views: []`, so treat view creation as unproven and day-2).

**Departments — 1 of 9:** supply-chain. **Record types — 5 of 23:** `state_file`, `approval_packet`, `observation`, `operating_note`, `decision_item`. Deferred: the other 18, including every pattern, skill, KPI, lot, supplier and outcome record. **Jobs — 2 of ~20:** one department daily slot, one decision poll. Deferred: the 15 other department slots, the nightly build, the librarian pass, the weekly/monthly/quarterly reviews and the watchdog.
