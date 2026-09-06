# Plan — tonight (day 0) and the day ladder

Everything below was cut to what the six audits in `docs/audit/` confirmed is buildable. Rami's inputs are marked **INPUT**. Times are working minutes.

## Tonight, in order

| # | Who | Step | Input | Min | Test |
|---|---|---|---|---|---|
| 0 | Rami | Create an empty private GitHub repo `anabtawi-os`; tell Claude. Claude pushes this tree to its `main`. | **INPUT: repo exists** | 3 | `git clone` on the MacBook shows `SPEC.md` |
| 1 | Rami | monday: profile → Developers → generate a personal API token. Note your user id (108169876). | **INPUT: token, on the MacBook only** | 5 | `python3 bin/monday_api.py` style check: `me` returns 108169876 |
| 2 | Rami on MacBook | Write `~/.anabtawi/env` with `export DATADOE_MCP_KEY=…` and `export MONDAY_API_TOKEN=…`; `chmod 600`. Never in the repo. | **INPUT: DataDoe MCP key** | 5 | `source ~/.anabtawi/env` sets both |
| 3 | Claude Code on MacBook | `bin/build-monday.py --render` then `--init` from Rami's token: workspace, 4 boards, columns with explicit ids, groups, Run Health items. Commits `ops/monday-ids.json`. | | 15 | `--verify` prints OK; boards visible on the phone |
| 4 | Rami in monday UI | The three automations, the three views and the Cockpit dashboard exactly as listed in `docs/monday-schema.yaml` (no API path exists for filtered views and widgets). | | 20 | Cockpit shows the battery and four numbers |
| 5 | Claude Code on MacBook | `bin/run-job.py ops.preflight`: proves the DataDoe key, records table names and freshness in `state/preflight.md` and `ops/OPERATING-NOTES.md`. | | 15 | `state/preflight.md` dated today with a max_date row. If yesterday has zero rows (fresh connection), stop here and resume tomorrow after the fetch |
| 6 | Claude Code on MacBook | `bin/run-job.py --chain account-health.daily` runs account-health → supply-chain → ceo. | | 40 | three state files dated today; `briefs/<today>-decisions.md` exists |
| 7 | Claude Code on MacBook | Write one real T2 packet by hand from the brief (supply-chain, a reorder proposal in dry-run mode) so the loop has something to carry; `bin/validate-records.py`. | **INPUT: confirm the 14-day cover floor** | 10 | validator prints records OK |
| 8 | Claude Code on MacBook | `bin/project-monday.py` | | 5 | Run Health shows OK for the three, Not scheduled for the rest; the packet is an item in Decisions group Today |
| 9 | Rami on phone | Open the item, read `if_ignored`, tap `decision` → Approved | | 2 | status shows Approved |
| 10 | Claude Code on MacBook | `hands/observe.py` | | 5 | packet in `approvals/approved/` with `decided_at`; one ledger row with status dry-run; `state/hands.md` written |
| 11 | Rami | DataDoe Settings → Actions: confirm every action type is disabled; screenshot into `docs/policy/`. | | 5 | screenshot committed |

About 2 hours 10 minutes of work. Nothing touches Amazon. Nothing moves money.

## What is not possible tonight and why
Any real Amazon write (by design). SP-API and Ads API registration (Amazon-side; submit tomorrow). Keepa, QuickBooks, Walmart (not bought or not set up). A reliable schedule on a laptop that sleeps (run the chain by hand until the Mac mini). The vault (`~/.anabtawi/env` tonight, 1Password `op run` on the Mac mini). Trusting the monday tap as authorization (needs the day-5 identity test).

## The ladder after tonight
See `SPEC.md` §3. One capability a day, each with a one-minute test, nothing added while yesterday's is red.

## Fixes applied from the audit (so Rami can check them in five seconds)
- Telegram removed everywhere; monday is the only channel.
- Constitution reduced to one page; guardrails in one table, each marked confirmed / unconfirmed / reported; meltable window corrected to 16 Oct – 14 Apr; shelf life corrected to 105 days at receipt.
- The ratchet lives in `department.yaml` only; every department carries `tier: {default: T0, classes: {}}`.
- Only `bin/project-monday.py` writes monday; only `hands/ledger.py` writes the ledger.
- `ops/PAUSE` is committable (was gitignored).
- Both JSON schemas rewritten: `if_ignored`, scoring fields required, money as decimal strings, every ads class named, no `other`, no names from any earlier design.
- `docs/record-schemas.yaml` now parses (it never had) and carries ids for observations and facts, currency on every money row, a purchase-order record so the monthly ceiling is computable.
- monday schema cut to four buildable boards with legal column ids; stable ids are set explicitly by `bin/build-monday.py`, never by the MCP.
- Jobs are defined, not vague: `docs/jobs.json` with reads, tools, steps, writes, timeout, failure behaviour and done conditions; the morning scans were deleted because the data they read does not exist at that hour.
- WebFetch, WebSearch and curl are denied in `.claude/settings.json`; auto-memory is off.
- Watchdog derives the expected departments from `docs/jobs.json`, handles DST, and opens an issue.
- Cost stated once: about USD 350 a month for six months, then about USD 250, on top of subscriptions already held.
