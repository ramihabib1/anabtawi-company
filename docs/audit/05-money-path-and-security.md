# Audit 05 — the approval and money path, the hands runner, credentials, kill switches

Scope: design §9, `AGENTS.md` §3–6, `docs/schemas/*.json`, `hands/README.md`, `docs/monday-schema.yaml` (Decisions), `docs/research/07`, `08`.

---

## BLOCKERS

**B1 — The CEO agent holds a monday token that can write the `decision` column, and the poller treats that column as authorization.**
`departments/ceo/department.yaml` grants `mcp: [datadoe-read, monday]`. Design §4.8: the ops identity "uses Rami's API token … all agent writes appear as Rami". `monday-schema.yaml:29` marks `decision` `writer: rami`, but "writer" is a comment, not a permission — Pro has no column permissions. Design §9.3 step 8 then moves `pending/ → approved/` on that column alone. So the LLM that ranks a packet can approve it with its own credentialed tool, and the runner cannot tell. `change_item_column_values`, `create_update` and `execute_code` (research 02: the sandbox has authenticated API access with "authentication handled automatically") all reach the same column.
Fix, strongest first: (a) **the `decision` column is not an authorization signal until two identities exist.** Give the ops machine the second grandfathered seat as its own monday user, keep Rami as board owner, and have the poller read `get_board_activity` and require the `change_status_column_value` event's `user_id == RAMI_USER_ID` and `!= OPS_USER_ID`; abort on ambiguity. Research 02 open question 7 marks agent-write attribution on 2-seat Pro as UNKNOWN, so test it first: have the ops identity flip a test item and confirm the activity row names the ops user. (b) Until that passes, require a second signal the CEO cannot produce — the approval must also appear as a commit to the packet file authored by Rami's GitHub identity, which is outside the agents' token domain. (c) Remove `monday` from every department's `mcp:` except a projection process that never writes Decisions.

**B2 — `ops/PAUSE` is in `.gitignore` (line 3), so the documented kill switch cannot be pulled.**
Design §9.4 and `AGENTS.md` §6.9 both say `touch ops/PAUSE` "from the GitHub app on Rami's phone". A gitignored path cannot be committed there, and the runner's `git pull` never sees it: the switch works only at the Mac. Fix: delete `.gitignore` line 3; the runner checks the file at start, after every pull, and before every write call.

**B3 — The monthly PO ceiling is not computable, because PO money never enters the ledger.**
`AGENTS.md` §4 sets CAD 15,000 cumulative monthly; §9.3 step 5 recomputes budget "from the ledger, not from the packet's claim". But the PO path forks at step 7 and "never rejoins" — Rami pays in his bank, no row is written. The ledger holds zero PO amounts, so remaining is always CAD 15,000 and two CAD 9,000 POs both validate. Fix: the runner writes a row when it generates the payment packet (`output.status: "handoff"`, a new enum value, with `amount`), and a second when Rami marks the subitem Paid; the ceiling sums `action_class == purchase_order` rows for the calendar month.

**B4 — `requires_second_check` is self-declared, undefined, and deadlocks against the 48h expiry.**
The proposing department sets it (schema line 68), so an agent decides whether its own CAD 12,000 packet cools off; and `estimated_cost` is not in `required`, so omitting the amount dodges the >CAD 5,000 test entirely. The "check" is a bare timer with no second checker and no revocation path — §9.3 never says what happens if Rami flips the item back to Rejected during the 12 hours. A packet approved at hour 40 executes at hour 52, past `expires`. Fix: (i) the runner computes the flag from `estimated_cost` and `tier` and ignores the packet's claim; (ii) `estimated_cost` becomes required and a decimal string; (iii) `expires` bounds *approval*, with a separate `execute_by = decided_at + 12h + 6h`; (iv) the runner re-reads the monday decision immediately before executing and aborts on anything but Approved.

**B5 — `tier` is self-declared and no machine-readable tier table exists.**
Every `department.yaml` carries `tier: {}` plus a comment. `AGENTS.md` §3 puts tiers in `department.yaml`; design §9.2 says Rami promotes "by editing one line in the department's `AGENTS.md`" — two files, and the real value is an empty map, so no validator can answer "is this department allowed this class at this tier?". Fix: `tier: {default: T0, classes: {}}`; anything not explicitly listed is T0 and refused. Delete the `AGENTS.md` variant in §9.2.

**B6 — The idempotency key cannot be sent to the write path that exists.**
§9.3 step 11 and §9.5 rest on "one API call with the idempotency key". Research 08 §5 verifies DataDoe's surface as `actions_details_schema_get / actions_start / actions_get / actions_list` — **no idempotency parameter**; the Ads MCP's behaviour is unstated. The fallback ("checked against the ledger before every call") is a check-then-act race across exactly the crash it must survive. Fix: write an intent row *before* the call (`output.status: "in-flight"`, new enum value); chain verification at runner start refuses all work until every in-flight row is reconciled via `actions_list` matched on payload plus a read-back. Add `dry_run.action_id` as the correlator (research 08 recommends this). Demote "idempotency key sent to the API" to a week-one verification item.

**B7 — Concurrent writers to `ledger/actions.jsonl` with a "monotonic, gapless" `seq`.**
`AGENTS.md` §3 has T1 departments logging their own actions, §7 has all nine committing and pushing each run, and the runner pushes every 5 minutes. Two processes take seq N and collide at the same EOF on every push. Fix: **only `hands/ledger.py` appends.** A T1 department writes an intent packet to `approvals/approved/` with `tier: T1`; the runner executes and logs it. Make this a hard rule in §6.4.

**B8 — Bank details: two files give opposite instructions.**
`record-schemas.yaml:127` — "bank details never in the repository". Research 07 §8b — the payment packet reads them "from `suppliers/<name>.md`". Design §9.3 is ambiguous between the two. Fix: the payment packet prints supplier legal name, supplier id, PO ref, amount, currency, and "compare against the saved payee in your bank". No account number, IBAN or SWIFT is ever read, stored or rendered.

**B9 — Appendix B and the normative schema disagree on required fields.**
Appendix B (line 875) requires `if_ignored` plus `metric, baseline, expected, review_on, design`; the schema requires `if_rejected` and has none of the five scoring fields, which `AGENTS.md` §6.7 mandates and `ledger/outcomes.csv` needs as columns. Because neither schema sets `additionalProperties: false`, `if_ignored` passes silently as an unknown extra while the required `if_rejected` is missing. Fix: standardise on `if_ignored` (what monday and the card use), add the scoring block from `record-schemas.yaml:76`, set `"additionalProperties": false` on both schemas.

---

## MAJOR

**M1 — Brand-specific and stale leftovers; both schemas are verbatim copies of research 07 §6.** `department` enum includes `chief-of-staff`, not one of the nine departments here. `skus` pattern `^ANB-[0-9]{3}$` hard-codes brand one against §12 multi-brand and is unverified against Rami's real seller SKUs. `runtime` enum keeps `paperclip` and `grok-bot`. Fix: drop `chief-of-staff`; drop the SKU pattern or generalise to `^[A-Z]{2,4}-[0-9]{3,4}$`; prune the runtime enum to harnesses that survive.

**M2 — `action_class` cannot express the classes the design ships, and `"other"` voids the gate.** Missing `ad_bid_change`, `ad_budget_change`, `negative_keyword`, `request_a_review`, `qbo_bill`, `deal`. An ads packet must be `"other"`, which has no per-class sub-schema, so its guardrails are unenforceable by construction. Fix: enumerate every class in §9.1's table and delete `"other"`; unknown class = rejection.

**M3 — Money typed as JSON numbers.** `estimated_cost` (line 26) and `budget_remaining` (line 52) are `number` while §9.5 says "all money as decimal strings, never floats". Fix: `{"type":["string","null"],"pattern":"^-?[0-9]+\\.[0-9]{2}$"}`. Add `amount_pre_round` to the ledger — §9.5 promises both values logged and there is one field.

**M4 — No FX rule; the ceilings are single-currency.** `currency` is CAD|USD, the ceilings are CAD, and nothing names a rate, source or as-of date, so from the US launch both are uncomputable. Fix: `fx: {rate, base, quote, as_of, source}` on any packet whose currency differs from the ceiling's; store native and converted amounts.

**M5 — `marketplace` is claimed as a defence but is unimplemented.** §9.5 says it lives "in the packet `id`, in the lock key, in the credential selection"; the `id` pattern has no marketplace segment, and `ca|us|walmart-ca` are local tokens with no mapping to Amazon marketplace ids, so `packet.marketplace == credential.marketplace_id` cannot be evaluated. `walmart-ca` is in the enum though §1 makes Walmart monitor-only. Fix: add the id segment and a mapping file (`A2EUQ1WPHNCC`, `ATVPDKIKX0DER`); reject `walmart-ca` on write classes.

**M6 — The ratchet's six conditions are not computable.** "≥20 approved packets", "rejection rate <5%", "no Rami edits to the last ten", "zero policy events attributable to the class": the ledger records executions, not decisions; `approvals/rejected|expired|failed/` do not exist on disk; a Rami edit is indistinguishable from an agent edit in git under B1; and no field attributes an account-health event to a class. Fix: create the directories; emit a `decision` ledger row on every approve/reject/expire/withdraw carrying `action_class` and `decided_by`; add `attributable_class` to account-health records; ship `hands/ratchet.py` as the single computation and require its output in the promotion packet.

**M7 — Poll design: no write atomicity, no external heartbeat.** `validate.py` runs on the same 5-minute timer as the 15:45–16:55 department runs and moves failures to `approvals/rejected/`, so a packet caught mid-write is permanently rejected; there is no `.tmp`+rename convention. Fix: read packets only at git HEAD (`git show HEAD:approvals/pending/<f>`), never the working tree, and retry a first-seen packet once before rejecting. Separately, the runner and the watchdog are both `launchd` jobs on one machine, so a sleeping MacBook is silent failure; the 09:00 GitHub Actions watchdog checks state files, not the runner. Add a committed heartbeat file and a CI check that fails when it is over 30 minutes old.

**M8 — "Daily git head as external anchor" is not external.** Every agent can push to the same repo that anchors the chain. Fix (free): GitHub branch protection blocking force-push and deletion makes history append-only server-side — a genuinely separate domain. Also the hash formula differs between files: research 07 §6.2 says `SHA-256(prev_hash ‖ seq ‖ canonical-JSON(row))`, the schema says "over canonical JSON of all fields except `hash`". Keep the schema's (it already contains `prev_hash` and `seq`) and name the canonicalization — RFC 8785 JCS, UTF-8, sorted keys, no whitespace — or two implementations will disagree.

**M9 — `verification` is optional on a write row**, though `AGENTS.md` §6.4 requires it. Require it whenever `output.status ∈ {ok, partial}`.

**M10 — Credential separation is unenforceable on DataDoe as understood today.** §9.4 and §6.3 say departments hold read-only keys and only the runner holds write keys. Research 08 §3 tags per-key scopes as REPORTED and open question 10 as UNKNOWN, and action types are enabled **per org** in Settings → Actions, not per key. If so, a department key can call `actions_start` with `dryRun:false` for any enabled type, and §9.4's "structurally incapable of moving money" is false. The only verified control is the org-level toggle. Fix: say so plainly; keep every type disabled; make key-scope verification a week-one blocker; have the runner refuse to start if a write-scoped variable appears in any department's rendered `.mcp.json`.

**M11 — `format` is annotation-only in 2020-12.** Unless the validator opts into the format-assertion vocabulary, no `date-time` and no `uuid` in either schema is actually validated. Add explicit `pattern`s.

**M12 — Telegram survives in the design and the schema, against "monday notifications only".** `decision_channel` includes `"telegram"` (line 72) — approval by chat message, with no authentication whatsoever — and §9.3 step 6, §10.1, line 145 and the cost table all assume a bot. Delete the enum value and replace every Telegram path with a monday notification.

**M13 — Ads T1 is unreachable tonight and partly unverified.** `AGENTS.md` §3 no longer names a surface, so research 08's "official Ads MCP only" contradiction is fixed here. What remains: the DataDoe **budget action is unverified** (research 08 open question 2), which §9.1 concedes; and the ratchet needs 20 approved packets of one class under a budget of 3 new packets a day across *all* classes, so the earliest promotion is well past 30 days even spending every slot on it. Say this in §13 week 7–8 instead of implying ads T1 is near.

---

## MINOR

- `monday-schema.yaml:62`: Deferred sets `snooze_until` +7 days, but packets live 48 hours — deferral guarantees expiry. Use +1 day, or make Deferred trigger re-proposal.
- `monday-schema.yaml:49`: `decided_at` is a `last_updated` column, which moves on *any* change — the CEO's nightly rank update overwrites it. Use a plain date-time written by the poller from the activity log.
- monday's expiry automation runs in the account timezone, the runner in Asia/Jerusalem. Pin the account timezone.
- §9.4 says the runner exits at "step 5" on PAUSE; research 07 §5.2 says step 2. Say "before any validation and again before any write".
- `status` lacks `partial` (though §9.5 says "packet ends `partial`") and `withdrawn` (though the approval budget requires withdrawal to propose a sixth).
- Appendix A lists `approvals/approved|rejected|expired|failed/`, `ledger/decisions.md`, `state/locks.md`, `state/calendar.md`; none exist.
- §9.5 claims "a repo pre-commit secret scan"; no hook, no CI job — `staleness.yml` is the only automation.
- The Claude `setup-token` is named once (line 524), its storage never specified, while §6.3 forbids products storing a Claude credential. Say: the `ops` user's login keychain, never the runner's vault, never the repo.
- Doppler appears only as a parenthetical (lines 144, 773). Commit to 1Password `op run` — the one research 07 verified — and delete the alternative.

---

## The minimum safe money path for tonight

Everything at T0, every DataDoe action type disabled. Target: a packet is written, appears on monday, Rami approves it, and **nothing executes**. The strongest guarantee available tonight is not a flag but an absence: **the runner contains no code path that can call Amazon, DataDoe, QuickBooks or a bank, and holds no write credential.** Tonight's approval is a *recorded intent*, not an authorization — B1 is unsolved, and the `decision` column must not be trusted with execution until the two-identity test passes. Nothing is trusted with execution tonight, so it need not be.

**Text changes first (~30 minutes, no code):** delete `ops/PAUSE` from `.gitignore`; `mkdir approvals/{approved,rejected,expired,failed}`; fix both schemas (drop `chief-of-staff` and the `ANB-` pattern; money to decimal strings; `additionalProperties:false`; `if_ignored`; add the scoring block, the real `action_class` values, `mode`, `dry_run.action_id`, statuses `partial`/`withdrawn`); set `tier: {default: T0, classes: {}}` in all nine `department.yaml`; delete `"telegram"`; add "only `hands/ledger.py` appends to the ledger" to §6.4; turn on branch protection.

**Packet format:** keep `approvals/pending/<id>.md`, but make the front matter a fenced ```json block rather than YAML. Still human-readable and diffable, and it parses with the standard library — macOS's system Python ships neither PyYAML nor `jsonschema`, and tonight is the wrong night to find that out.

**The runner — `hands/observe.py`, Python 3 stdlib only, ~180 lines**, one `launchd` job every 5 minutes. Checks in order, each fail-closed:

1. Refuse to start if any write-scoped variable is in the environment (`DATADOE_WRITE_*`, `ADS_*`, `SP_API_*`, `QBO_*`). Five lines, and it is the real guarantee.
2. `flock` a single-instance lock; exit quietly if held.
3. Exit 0 if `ops/PAUSE` exists, after one line to `state/hands.md`.
4. `git pull --rebase --autostash`; any failure is a stop with non-zero exit, never a guess.
5. Verify the hash chain from GENESIS; refuse all work if broken (handle the empty file).
6. Read packets only at git HEAD, never from the working tree.
7. Validate: required fields; `schema_version == "1.0"`; `tier == T2` (T3 refused outright — the runner never touches T3); `mode == "dry-run"`; `expires` in the future; `marketplace` and `currency` present; `estimated_cost` matches the decimal pattern; `idempotency_key` unseen in the ledger; ≤5 pending, ≤3 created today. Failures move to `approvals/rejected/` with a machine reason, except a packet first seen this tick, retried once.
8. Project each valid packet to Decisions with one `urllib.request` POST to `api.monday.com/v2` (token via `op run`), then read back its `decision` label and `get_board_activity` row.
9. On Approved: move to `approvals/approved/`, stamp `decided_by` (the activity-log user id, recorded but not trusted — B1), `decided_at`, `decision_channel: monday`, and append **one** ledger row with `output.status: "dry-run"`, `verification: null`, `reason: "execution disabled: no write path compiled in"`. Then stop. Nothing reads `approvals/approved/`.
10. Commit and push with `git pull --rebase` retry; write `state/hands.md` and a heartbeat every tick, including on failure.

**What waits:** execution and read-back, `op run` write credentials, idempotency against a live API, the 12-hour cooling rule, per-class payload sub-schemas, FX, the ratchet computation, Automate Pricing mirroring, QuickBooks, the payment-packet fork. Each depends on B1, B3, B5, B6 or M10; none of those close tonight.
