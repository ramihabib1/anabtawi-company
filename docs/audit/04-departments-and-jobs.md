# Audit 04 — departments, scheduled jobs, the harness

Scope: `departments/*/AGENTS.md` + `department.yaml`, `AGENTS.md` §7–8, design §6, `bin/`+`hands/` READMEs,
`.github/workflows/staleness.yml`, research 08 and 10. Prose is ~2,000 words; the two YAML blocks are the
requested deliverable (a job catalog format, filled) and are counted separately.

---

## Findings

### BLOCKER

**B1 — All 17 slots point at files that do not exist.** Every `department.yaml` names `prompts/daily.md`,
`prompts/exception-scan.md`, `prompts/weekly.md`, `prompts/librarian.md`, `prompts/monthly.md`;
`departments/*/prompts/` holds only `.gitkeep`. Nothing is runnable. *Fix:* the prompt is not a file — it is a
`steps:` list in `docs/jobs.yaml` (below), rendered into `-p` by the wrapper.

**B2 — "Departments run one at a time" is arithmetically false.** Design §6.4 claims sequencing; §6.5 spaces slots
10 minutes apart while `timeout_min` is 15–25. finance 15:45+20 = 16:05 = pricing-intel's start; supply-chain
15:55+20 = 16:15 = advertising's start; expansion 16:55+25 = 17:20, after the CEO run began. The `flock` in §6.3 is
*per department* and serialises nothing, so two departments push concurrently on day one and the second push loses.
*Fix:* stop scheduling by clock — one job at 15:45 runs `bin/run-day.sh`, executing the cycle sequentially, each
department with its own timeout, `git pull --rebase` before each push, CEO last.

**B3 — The mandatory load order names four files that do not exist.** `AGENTS.md:63` requires
`strategy/CURRENT.md`; the repo has `strategy/STRATEGY.md`; `record-schemas.yaml:159` calls it
`strategy/GOALS.md` — three names for one file. `:64` requires `requests/<dept>/inbox/`, `:65` requires
`state/calendar.md` and `state/locks.md`, `:78` points at `docs/CONVENTIONS.md` — none exist; the last is
superseded by `record-schemas.yaml`. A first run aborts at step 2 or invents the contents. *Fix:* one name,
`strategy/CURRENT.md`; create the nine `requests/<dept>/{inbox,done}/`, `state/calendar.md` and `state/locks.md`
with their header lines from `record-schemas.yaml`; delete the `CONVENTIONS.md` reference.

**B4 — The three morning scans read data that does not exist at that hour.** 07:15–07:30 Asia/Jerusalem is
00:15–00:30 America/Toronto. Research 08:119 (REPORTED): DataDoe's daily fetch *starts* 02:00 and most tables land
~05:00 marketplace time, so the newest complete daily table at 07:20 covers **D−2**; research 08:274: every ads
table is `_by_date`, hourly "UNKNOWN, probably not". Advertising's "spend pacing vs cap" and supply-chain's "hero
cover" scans are ~30 hours stale while design §6.5 sells them as the P0 detector. *Fix:* delete the 07:xx scans
until `exports_sources_get` proves per-table intraday freshness; keep only orders (the one thing 08:119 calls
intraday) and print the freshness timestamp into the state file.

**B5 — `department.yaml` cannot render a `claude -p` invocation.** Verified flags (research 10:57) are
`--output-format json`, `--json-schema`, `--permission-mode`, `--mcp-config`, `--allowedTools`; the YAML supplies
only a server *name list*. Missing: `permission_mode` (design §6.6 asserts "`--permission-mode` per slot" — no such
field exists), allowed/disallowed tools, output format, clone path, env-var names, retries, `on_failure`, and any
definition of success. *Fix:* `docs/jobs.yaml`, below.

**B6 — No MCP server is defined anywhere.** The six names are referenced nine times and resolve to nothing; there
are no `.mcp.json` files. (Research 08:65's "this matches what is already in `departments/*/.mcp.json`" refers to
the *earlier* repo, per that file's header.) Two are unbuildable today: `keepa` needs the forked ~150-line wrapper
(research 09:104 — upstream is 0★ sample code) and `amazon-ads-read` needs credentials not applied for. *Fix:*
`docs/mcp-servers.yaml`, below.

**B7 — Nothing disables the browser.** `AGENTS.md:49` forbids opening any Amazon page; Claude Code ships
`WebFetch`/`WebSearch` enabled and `Bash` can `curl`. No field and no `.claude/settings.json` turns them off — and
that file does not exist, despite design §6.6 asserting auto-memory is "switched off" in it. The hardest rule in
the constitution is enforced by nothing but instruction. *Fix:* `disallowed_tools: [WebFetch, WebSearch]` on every
job, an explicit Bash allowlist, and commit `.claude/settings.json`.

**B8 — The watchdog contradicts the schedule it polices.** `staleness.yml:13` demands a fresh state file from all
nine daily, but `expansion` runs Mon/Wed/Fri — so it fails four days a week by construction; nothing says whether
the cycle runs Sat/Sun; `state/` holds only `skus/`, so it fails today too. And it only `exit 1`s, while design
§6.5 and research 10:222 promise "an issue + email" — the whole point of a dead-man's switch. *Fix:* derive the
expected set for the weekday from `docs/jobs.yaml`; add `gh issue create`; settle the weekend question (recommend
7 days — Amazon does not take Saturday off).

### MAJOR

**M1 — DST.** `cron: "0 6 * * *"` is 09:00 only on IDT; Israel leaves DST 2026-10-25 and it becomes 08:00. GitHub
cron is UTC-only, so "adjust for DST in week 1" describes work no cron edit can do. *Fix:* two schedules
(`0 6 * * *`, `0 7 * * *`) plus `[ "$(TZ=Asia/Jerusalem date +%H)" = "09" ] || exit 0`. Separately: the
Jerusalem↔Toronto gap is 7 hours except **2026-10-25 → 2026-11-01**, when it is 6, so every slot justified by "after
the marketplace refresh" shifts an hour that week. Also note research 10:142 — Actions schedules are best-effort
and disabled after 60 days of repo inactivity.

**M2 — All nine charters are stubs.** `departments/*/AGENTS.md:6–11` read "(To be written … week 1.)". A department
loaded tonight has one `owns:` sentence and no thresholds, so each run invents its own job. This is the direct
cause of "the scheduled tasks are vague".

**M3 — `reads_state: []` in all nine.** Contradicts `AGENTS.md:53`, `:63` and the design's own example
(`reads_state: [inventory, calendar, cash, compliance]`, design:471). As written no department reads another's
state and the §6.4 blackboard does nothing.

**M4 — Budgets are wrong or unverifiable.** `monday_calls_per_run: 40` appears on seven departments with no monday
server in `mcp:`. `datadoe_tokens_per_run: 6` is identical for all nine, yet research 08:42–45 VERIFIES only the
*action* cost (2 tokens ≤100 entities); export cost is REPORTED and the allowance disputed (1,500 vs 2,000).
*Fix:* budget `datadoe_exports`, a countable thing; drop `monday_calls` where there is no server.

**M5 — Fallback chains contradict research 10 and the design.** All nine carry
`fallbacks: [routine, claude-code-api, codex-api]`, yet design:525 and research 10:135 make a Routine the backup
"for the 17:05 CEO card only" and "never load-bearing". A Routine cannot run a department at all: research 10:60 —
Routines clone a repo, have **no local files**, no local MCP config, no permission-mode picker. Research 10:208
gives advertising **no** fallback; the yaml gives it two. *Fix:* `fallbacks: []` for eight; `[routine]` on the CEO
card slot only, documented as "reads the pushed repo, writes a card, nothing else".

**M6 — Three scheduled things have no owner or definition.** (a) the 15:30 nightly build (`AGENTS.md:73`, design
§6.5) is the input to every later run, is in no `department.yaml`, and `build-sku-profiles.py` is unwritten;
(b) quarterly planning (15 Dec/Mar/Jun/Sep) is in the cadence and in no yaml; (c) the 5-minute hands runner is
week 3 (`hands/README.md`), so **no T2 packet can execute until then** — state it, don't leave it inferred.

**M7 — Timeout policy conflicts and timeout behaviour is undefined.** Research 10:233 specifies a fixed 20-minute
wrapper timeout; `ceo/department.yaml:7` sets 60. No slot says what happens when it fires: if the process is killed
no state file is written, so a slow run is indistinguishable from a dead machine. *Fix:* `on_failure` in the job
schema — the *wrapper*, not the model, writes the failure state file.

**M8 — The notification channel contradicts the owner.** Design §6.3 step 7, §6.5, §10.1 and §11.1 make Telegram
the failure and P0 channel; the brief says monday only, no Telegram. *Fix:* strike Telegram, or have Rami
re-approve it explicitly.

**M9 — Four harness claims overstated against research 10.**
- design:133 "Only harness with a **verified** legal path for **unattended** subscription use." Research 10 verifies
  the *credential* clauses only (10:35–47). The step to "unattended is permitted" is the researcher's reading of an
  "or where explicitly permitted" carve-out in a Consumer Terms clause that is **REPORTED, not VERIFIED** (10:13,
  10:49, 10:51), and open question 1 still asks someone to read it. *Fix:* "the only harness whose credential terms
  we have read in the primary source; the unattended reading rests on a REPORTED Consumer Terms clause."
- design:527 "32 KiB cap **enforced in CI**" — the cap is REPORTED from one blog (research 05:56) and no CI check
  exists; `.github/workflows/` holds only `staleness.yml` and `record-schemas.yaml:191` lists the check as *wanted*.
- design:531 states the July 2026 Grok Build repository-upload incident as fact; research 10:98/264 says the repo
  asserts it and it "needs a citation before it is quoted to anyone outside".
- design:535 "Cost fits inside Max 20x with margin … 240–480 weekly Sonnet hours" — REPORTED, and research 10:70
  says the boost settles to +25% from **2026-09-14**, eight days away.

Not overstated, keep: never `--bare` (10:57, 229); one-year `setup-token` (10:58); Actions on
`claude_code_oauth_token` (10:59); Routines' 1-hour floor, daily cap, no local files (10:60); Desktop tasks need
the app open and machine awake (10:61); monday is an MCP server, not a harness (10:125).

**M10 — `AGENTS.md:71`'s "verified against DataDoe's refresh time on day one" has no job that verifies it and no
file to write it into.** Design §14.1 says 15:00 Jerusalem; §6.5 builds at 15:30. *Fix:* the `preflight` job below.

### MINOR

- **m1** Design:463–472 gives advertising **15:50** and `keepa`; §6.5 and the yaml give **16:15** and no keepa.
- **m2** `model: sonnet` is a moving alias; pin the exact id and record it in `ops/OPERATING-NOTES.md`.
- **m3** Two model-selection mechanisms coexist: `model.escalate_to` (no `when:`, unlike design:469) and per-slot
  `model: opus`. Keep per-slot.
- **m4** `GEMINI.md` is `@AGENTS.md`; `@` import is a Claude Code memory feature (research 05:56) and nothing
  verifies Gemini CLI resolves it.
- **m5** `ledger/actions.jsonl` is empty with no genesis row, yet `AGENTS.md:52` requires a hash chain — the first
  writer must invent `prev_hash`.

---

## Every slot, graded

**R** reads · **T** tools (named tools/tables, not a server list) · **W** writes · **L** time limit · **F** failure
behaviour · **D** "done" test. `½` = partly, from a general rule elsewhere.

| Slots | R | T | W | L | F | D | /6 |
|---|---|---|---|---|---|---|---|
| The 16 department slots (3 morning scans, 9 daily, 2 weekly, ceo weekly, ceo monthly) | ✗ | ½ | ½ | ✓ | ✗ | ✗ | **2** |
| ceo librarian Mon 06:00 — no tool could make a pattern from zero observations | ✗ | ✗ | ½ | ✓ | ✗ | ✗ | 1½ |
| nightly build 15:30 · hands every 5 min · quarterly 15 Dec/Mar/Jun/Sep | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **0 — not slots at all** |

All 17 score alike because they differ only in clock time, `timeout_min` and the server list. The `W` half-mark is
earned entirely by `record-schemas.yaml:129` (`state_file`) — header, five sections, "not dated today is a failed
run". It is the one thing here a job can be tested against, so every job below writes it. **The schedule defines
when, and nothing else:** no slot names a table, a threshold, an output beyond the state file, or a condition under
which the run was worth doing.

---

## What runs tonight and tomorrow on a MacBook

Tonight is **Sunday 2026-09-06, evening**: 15:30 and 15:45–17:05 have passed, so nothing is late. Tomorrow is
**Monday** — in this cadence also the 06:00 librarian pass and the 17:05 weekly review, both of which would run
against zero observations and zero scorecard history. Do not schedule either this week.

On a laptop that sleeps, **launchd is not a scheduler tonight**: research 10:230 says launchd jobs skip when the
machine sleeps and prescribes `pmset -a sleep 0 disablesleep 1` — advice for a Mac mini, not a MacBook that closes
at midnight. So: **tonight**, run by hand in the foreground — `preflight`, then account-health, supply-chain, ceo;
the point is proving the loop, not automating it. **Overnight**, nothing: no T1 class, no hands runner, and the
Canadian tables do not refresh until ~12:00 Jerusalem anyway. **Tomorrow 09:00**, the only job that survives a
closed lid is **GitHub Actions** (VERIFIED path, research 10:59) — the staleness watchdog, after B8 and M1 are
fixed. **Tomorrow afternoon**, if the lid is open at 15:45, run the chain manually again; move to launchd when the
Mac mini arrives, because a `StartCalendarInterval` job that silently doesn't fire is worse than a manual run Rami
knows he owes.

**The three departments needed tonight: account-health, supply-chain, ceo** — the two P0 detectors plus the surface
Rami reads. Finance is excluded deliberately: no `products/<brand>/<sku>.md` and no COGS exist, so it cannot
compute a margin tonight.

---

## Proposed `docs/mcp-servers.yaml`

Single definition of every server; `bin/render-mcp.py` turns a job's `tools:` into `.mcp.json` or `config.toml`.
Variable names only, never values.

```yaml
version: 1
servers:
  datadoe-read:
    transport: http
    url: https://mcp.datadoe.com/mcp/v1              # VERIFIED, research 08 §3
    headers: {datadoe-mcp-key: "${DATADOE_READ_KEY}"}
    env: [DATADOE_READ_KEY]
    scope: read
    allowed_tools: [exports_sources_get, exports_create, exports_get, exports_list, exports_raw_download]
    denied_tools: [actions_start, actions_get, actions_cancel, exports_delete]
    banned_skills: [amazon-asin-search-auditor]      # AGENTS.md §6.2
    limits: {rows_per_export: 2500, paginate_with: skip}
    status: unverified            # -> verified only after a run connects
  monday:
    transport: http
    url: https://mcp.monday.com/mcp                  # VERIFIED, research 02
    env: [MONDAY_API_TOKEN]
    scope: write                                     # boards only; never money
    allowed_tools: [get_board_info, get_board_items_page, create_item, change_item_column_values, create_update]
    status: unverified
  quickbooks-read:
    transport: stdio                                 # Intuit official server, research 09:124
    command: npx
    args: ["-y", "@intuit/quickbooks-online-mcp-server"]
    env: [QUICKBOOKS_CLIENT_ID, QUICKBOOKS_CLIENT_SECRET, QUICKBOOKS_TOKEN_STORE_PATH]
    scope: read
    denied_tools: ["*create*", "*update*", "*delete*", "*send*"]
    status: not_built             # OAuth callback + token store not set up
  keepa:           {status: not_built, note: "needs the forked ~150-line wrapper; research 09:104"}
  amazon-ads-read: {status: not_built, note: "self-service credentials not applied for"}
  walmart-read:    {status: not_built, note: "CA endpoints died 2026-07-31; verify keys first"}
```

**Rule:** a job may not reference a server whose `status` is `not_built`. That alone removes four of the six
undefined names from tonight's path.

---

## Proposed `docs/jobs.yaml` — schema

```yaml
version: 1
defaults:
  harness: claude-code                 # claude-code | claude-code-api | routine | codex-api
  permission_mode: acceptEdits         # T0 jobs write files; they call no write tool
  output_format: json
  disallowed_tools: [WebFetch, WebSearch]     # AGENTS.md §6.1, enforced not implied
  retries: 0                                  # a department never retries itself
jobs:
  - id:         <dept>.<slot>                 # stable; appears in the commit message
    dept:       <dept|ops>
    trigger:    {type: manual|clock|weekday|actions|chain, at: "HH:MM", tz: Asia/Jerusalem,
                 days: [...], after: <job id>}          # chain = runs when `after` exits 0
    reads:      [<path>, ...]                           # exact paths, loaded in this order
    tools:      [<server>.<tool>, ...]                  # named tools, not server names
    data:       [<table> <columns> <window>, ...]       # the exact rows this job may export
    steps:      [<imperative line>, ...]                # becomes -p; each step is checkable
    writes:     [<path>, ...]                           # the only paths it may touch
    timeout:    <minutes>                               # wrapper kills and writes the failure state file
    model:      <alias or pinned id>
    budget:     {datadoe_exports: n, monday_calls: n, tokens_resident_max: n}
    on_failure: [<ordered wrapper action>, ...]
    done_when:  [<machine-checkable assertion>, ...]    # all must hold, checked after exit
```

`done_when` is checked by `bin/check-job.sh` after the process exits, so "done" is never the model's opinion.

## `docs/jobs.yaml` — the minimum set, filled

```yaml
jobs:

- id: ops.preflight
  dept: ops
  trigger: {type: manual}
  reads: [docs/mcp-servers.yaml]
  tools: [datadoe-read.exports_sources_get, datadoe-read.exports_create, datadoe-read.exports_get,
          monday.get_board_info]
  data: ["per candidate table: max(date), row count, one sample row"]
  steps:
    - "exports_sources_get; write every source name and its columns to .exports/sources.json."
    - "For amazon_seller_performance, the FBA inventory table and the orders table, export one day each and record
       max(date) plus the Jerusalem clock time of the call."
    - "One monday.get_board_info call to prove the token. Create nothing."
    - "Write state/preflight.md: table | max_date | lag_days | checked_at_jerusalem."
    - "Append the exact table names the other jobs must use to ops/OPERATING-NOTES.md."
  writes: [state/preflight.md, ops/OPERATING-NOTES.md, .exports/sources.json]
  timeout: 20
  model: sonnet
  budget: {datadoe_exports: 4, monday_calls: 1, tokens_resident_max: 20000}
  on_failure: ["write state/preflight.md with tools_failed:<tool>", "stop; run no other job tonight"]
  done_when: ["state/preflight.md dated today lists max_date for at least amazon_seller_performance",
              "no file outside `writes` changed"]

- id: account-health.daily
  dept: account-health
  trigger: {type: chain, after: ops.preflight}
  reads: [AGENTS.md, departments/account-health/AGENTS.md, departments/account-health/memory/MEMORY.md,
          ops/OPERATING-NOTES.md, state/preflight.md]
  tools: [datadoe-read.exports_create, datadoe-read.exports_get]
  data: ["amazon_seller_performance — AHR, ODR, late shipment, cancellation, VTR, OTDR, the six policy-violation
          counts, each with Amazon's own target column — latest available date, marketplace CA"]
  steps:
    - "If preflight lag_days > 2 for this table, write the state file saying so and stop."
    - "Export the row. Compare every metric to Amazon's target column in the same row."
    - "AHR < 200 or any violation count > 0 => P0. Any metric worse than target => P1. Else quiet."
    - "Write state/account-health.md to the record-schemas.yaml state_file schema; ## Data = metric | value |
       target | verdict."
    - "Append one observation line per P0/P1 to departments/account-health/memory/<today>.md."
  writes: [state/account-health.md, departments/account-health/memory/YYYY-MM-DD.md]
  timeout: 12
  model: sonnet
  budget: {datadoe_exports: 1, monday_calls: 0, tokens_resident_max: 20000}
  on_failure: ["wrapper writes state/account-health.md with tools_failed:<tool>", "continue the chain"]
  done_when: ["state/account-health.md dated today with the five required sections",
              "## Data has one row per metric with value, target and verdict",
              "no file outside `writes` changed"]

- id: supply-chain.daily
  dept: supply-chain
  trigger: {type: chain, after: account-health.daily}
  reads: [AGENTS.md, departments/supply-chain/AGENTS.md, departments/supply-chain/memory/MEMORY.md,
          ops/OPERATING-NOTES.md, state/preflight.md, state/account-health.md]
  tools: [datadoe-read.exports_create, datadoe-read.exports_get]
  data: ["FBA inventory by SKU (name pinned by preflight) — available, inbound, reserved, CA",
         "orders or sales by SKU by date — last 28 days, CA"]
  steps:
    - "If preflight lag_days > 2 for either table, write the state file saying so and stop."
    - "cover_days = available ÷ (28-day units ÷ 28), per SKU. No smoothing, no forecast."
    - "Flag every SKU under the 14-day floor (AGENTS.md §4). Rank by units/day descending."
    - "Write state/supply-chain.md; ## Data = sku | available | inbound | units_per_day | cover_days | flag."
    - "Write no proposal: T0, and no supplier file exists to price a PO against."
  writes: [state/supply-chain.md, departments/supply-chain/memory/YYYY-MM-DD.md]
  timeout: 15
  model: sonnet
  budget: {datadoe_exports: 2, monday_calls: 0, tokens_resident_max: 20000}
  on_failure: ["wrapper writes the failure state file", "continue the chain"]
  done_when: ["state/supply-chain.md dated today, one ## Data row per active CA SKU",
              "every flag carries a cover_days number, never a word",
              "approvals/pending/ unchanged"]

- id: ceo.daily
  dept: ceo
  trigger: {type: chain, after: supply-chain.daily}
  reads: [AGENTS.md, departments/ceo/AGENTS.md, departments/ceo/memory/MEMORY.md, ops/OPERATING-NOTES.md,
          state/preflight.md, state/account-health.md, state/supply-chain.md]
  tools: [monday.get_board_info, monday.create_item, monday.change_item_column_values]
  data: []
  steps:
    - "Read the two state files. Any not dated today is reported as 'did not run', by name, at the top."
    - "Write briefs/<today>-decisions.md: at most 5 items; an empty list is a correct answer. Every item cites the
       state-file line it came from. Nothing may be invented from a metric that was not exported today."
    - "Write state/ceo.md; ## Data = department | ran | dated | p0 | p1."
    - "Create ONE monday item on the Decisions board with the headline and a link to the brief. If the board does
       not exist, record 'monday: board absent' under ## Blocked and create nothing."
  writes: [briefs/YYYY-MM-DD-decisions.md, state/ceo.md, departments/ceo/memory/YYYY-MM-DD.md]
  timeout: 20
  model: sonnet
  budget: {datadoe_exports: 0, monday_calls: 5, tokens_resident_max: 20000}
  on_failure: ["wrapper writes state/ceo.md with tools_failed", "wrapper prints the brief path to the terminal"]
  done_when: ["briefs/<today>-decisions.md exists, ≤5 items, every item cites a state-file line",
              "state/ceo.md names every department that did not run",
              "at most one monday item created"]

- id: ops.staleness
  dept: ops
  trigger: {type: actions, at: "09:00", tz: Asia/Jerusalem}   # two UTC crons + a TZ guard step
  reads: [docs/jobs.yaml, state/]
  tools: []
  steps:
    - "Build today's expected department set from docs/jobs.yaml, not from a hard-coded list."
    - "Assert state/<dept>.md line 1 carries today's Asia/Jerusalem date."
    - "On any miss: open a GitHub issue 'STALE <date>' naming each, and fail the job."
  writes: [github issue]
  timeout: 5
  model: none
  on_failure: ["the failing workflow is the signal; the issue is the notification"]
  done_when: ["every expected state file is dated today, or an issue names each that is not"]

- id: ops.catchup
  dept: ops
  trigger: {type: manual}          # launchd RunAtLoad once the Mac mini exists
  reads: [docs/jobs.yaml, state/]
  tools: []
  steps:
    - "For each daily job whose state file is older than today and whose slot has passed, run the chain now."
    - "Never more than one catch-up cycle per calendar day."
  writes: []
  timeout: 60
  model: none
  on_failure: ["log and stop"]
  done_when: ["every daily job has today's state file, or the day is recorded as skipped in ops/OPERATING-NOTES.md"]
```

---

## Minimal charters for the three departments needed tonight

Each replaces lines 6–13 of that department's `AGENTS.md`.

**account-health** — *Mission:* detect in one export a day whether Amazon is about to stop us selling, and say so
before anything else is discussed. *Judged by:* a P0 Rami learns from Amazon before he learns it from us is a
failed department, whatever else the run produced. *Thresholds:* AHR < 200, any policy-violation count > 0, or any
metric worse than Amazon's own target column in the same row = escalate; within target and unchanged = silence.
*Hard rules:* the only source is `amazon_seller_performance`; no appeal, message or listing edit is ever drafted
here — appeals are T3 (§3); if the table's `max(date)` is more than two days old, report the staleness and stop.

**supply-chain** — *Mission:* know the cover days of every active CA SKU daily and name the ones under the 14-day
floor. *Judged by:* a stockout appearing in the data before it appears in a state file. *Thresholds:* hero cover
floor 14 days, seasonal buffer 6 weeks (§4); `cover_days = available ÷ (28-day units ÷ 28)`, no smoothing and no
forecast until a `products/<brand>/<sku>.md` exists to forecast against. *Hard rules:* propose no PO until a
supplier file with lead time and price exists; nothing inbound under 90 days of shelf life; no meltable stock
inbound 1 May–30 September.

**ceo** — *Mission:* turn today's state files into at most five decisions or a defensible zero, and make any
department that did not run the first line Rami sees. *Judged by:* Rami's grading (design §13 week 2); until then,
by whether every item cites a line in a state file dated today. *Thresholds:* cap 5, dropping to 3 for a week if
the reversal rate exceeds 10% (§4); an item with no citation is deleted, not softened. *Hard rules:* never writes
another department's state file, never opens an approval packet on their behalf, writes exactly one monday item per
run. Quiet must be provably quiet — "no P0" is only true if the export ran.
