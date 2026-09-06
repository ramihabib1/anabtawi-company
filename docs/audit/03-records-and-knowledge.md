# Audit 03 — Record schemas and the knowledge loop

Scope: `docs/record-schemas.yaml`, `docs/schemas/*.json`, design §5 / §7.1 / §8 and Appendix A/B, `AGENTS.md` §10 —
cross-checked against `docs/monday-schema.yaml`, `departments/*/department.yaml`, and the repository as it stands.

---

## BLOCKERS

**B1 — `docs/record-schemas.yaml` is not valid YAML and never has been.** `yaml.safe_load` fails at line 52. Fifteen
lines pack two or more mapping keys onto one line with `;`, which YAML forbids: 52, 101, 103, 104, 106, 115, 116, 117,
118, 143, 144, 145, 146, 147, 148. Line 52: `decaying: "last_seen > 90 days"; archived: "last_seen > 180 days (…)"`.
Fix: one key per line at the same indent (l.52 → 2 lines, l.101 → 3, etc.). Until then every claim in the file is
decorative — nothing can read it.

**B2 — The enforcement mechanism does not exist.** Line 2 states `bin/validate-records.py checks every file against
these on commit and in CI`. `bin/` contains only `README.md`, which does not list it; `.github/workflows/` holds only
`staleness.yml`; there are no pre-commit hooks. Design §8.1 rests harness portability on this script ("what makes
harness portability enforceable rather than hoped for"). Fix: write the validator for the six records below, or amend
l.2–3 and §8.1 to say the schema is advisory.

**B3 — Observations and facts have no id, so the loop's first arrow cannot be drawn.** `observation.line` (l.17) is
`- <ISO time> · obs · scope:… · <claim> · source:… · ledger:<seq|none>`, `required: [time, scope, claim, source]` — no
id. Yet `pattern.body["## Evidence"]` (l.46) demands `<observation or ledger id>`, and `fact.line` (l.23) offers
`superseded_by:<fact-id>` while facts have no id either. Fix: mint `obs-YYYYMMDD-<dept>-NN` and `fact-<dept>-NN`; add
both to `conventions.ids`.

**B4 — Skill → decision → outcome is missing; `hit_rate` and `firings_90d` are not computable.** `skill.front_matter`
carries both; `AGENTS.md` §10 demotes "below a 60% hit rate"; §8.2 computes "hit rate per validated rule over ≥10
firings". Nothing records a firing: `approval-packet.schema.json` has no field naming the skill or pattern behind the
proposal, `outcome.columns` (l.86) has no rule id, the ledger has none either. §8.2's "write back to … every playbook
whose evidence produced the rule" has no join key. Fix: add required `rule_refs: [string]` to the packet schema; add
`rule_refs` and `pattern_id` to `outcome.columns`; derive `hit_rate`/`firings_90d` from `outcomes.csv` and say so in
`computed:`.

**B5 — The packet's scoring fields are declared twice and implemented nowhere.** `record-schemas.yaml` l.76 declares
nine `scoring_fields` (`goal_id, metric, scope, baseline, expected, measure_window, review_on, design, control_set`);
design Appendix B calls `metric, baseline, expected, review_on, design` *required*; `approval-packet.schema.json`
defines only `goal_id`. So `AGENTS.md` §6.7 is unenforceable and `outcomes.csv` cannot be filled from packets. Fix: add
all nine to the JSON schema, put `metric, expected, review_on, design` in `required`, set
`design: {enum:[ab,prepost-matched,prepost,none]}`, and reconcile Appendix B to the same nine.

**B6 — Leftovers from the earlier design are baked into the normative JSON schemas.**
`approval-packet.schema.json` l.11–13: `department` enum includes `"chief-of-staff"` — no such department exists here
(`departments/` has nine, none of them), it is absent from `conventions.departments` and monday-schema's `&departments`
anchor, and `AGENTS.md` replaced it with `ceo`. Imported from the older *anabtawi-company* constitution; delete it.
l.28 `skus` pattern `^ANB-[0-9]{3}$` hard-codes the brand prefix and exactly three digits into a schema monday-schema
l.1 says "brand two reuses"; it also contradicts `products/<brand>/<sku>.md`. Use `^[A-Z]{2,5}-[0-9]{3,5}$`, or drop the
pattern and have the validator check the SKU exists under `products/`. l.72 `decision_channel` contains `"telegram"`
and §7.6 still routes P0 "via Telegram and monday push" — Rami's constraint is monday only; delete from both.
`ledger-entry.schema.json` l.15 `action_type` is called a "legacy alias" — there is no legacy; delete it, but note the
Decisions board column is *named* `action_type`, so pick one name company-wide.

**B7 — Enum vocabularies diverge across the four files; any projection script crashes or silently drops rows.**
*marketplace*: `ca`/`us` (record example) vs `ca, us, walmart-ca` (packet) vs the same plus `null` (ledger) vs
`CA, US, WMT` + calendar's `All` (monday). *harness*: free text in the state header vs
`claude-code, codex, grok-bot, paperclip, hands-runner, human` (ledger) vs `claude-code, codex, routine, grok`
(run_health) vs `routine, claude-code-api, codex-api` (`department.yaml` fallbacks). *action class*:
`vine_enrolment`/`reimbursement_claim` (packet) vs `vine`/`reimbursement` plus an extra `strategy` (Decisions board),
free string in the ledger. *knowledge status*: pattern `[hypothesis…archived]` plus skill
`[draft, validated, playbook, demoted, retired]` collapse into one monday column
`[Hypothesis, Supported, Validated, Playbook, Decaying, Falsified, Archived]` that cannot represent a `draft`,
`demoted` or `retired` skill — the exact state a demoted rule ends in, i.e. the output the whole §8 loop exists to
produce. Fix: one `conventions.enums` block as the single source; the projection script holds one lower-case → monday
mapping table, not one per board.

**B8 — Margin is the central guardrail and is not computable from any defined record.** §4 sets a 15% minimum
contribution margin after ads; `sku_profiles.margin_pct` is sourced "build". That needs price, landed cost, referral
fee, FBA fee and ad spend. `product.cost_rows` gives cogs/freight/duty/prep only — **there is no fee field in any record
and no fee source named**. The §5.2 example puts `currency: USD` cost rows under a CA listing with a CAD band, and there
is no FX record, rate source, or `landed_cost` formula. `kpi_row.columns` (l.92) has `revenue`, `ad_spend`,
`contribution_margin` and **no currency column**, so CA and US rows are unadditive. Fix: add
`fees: {referral_pct, fba_fee, currency, as_of, source}` per listing; add `currency` to `kpi_row`; add an `fx` record or
state that money is stored in marketplace currency and converted only at report time; write the `landed_cost` and
`margin_pct` formulas into `computed:`.

**B9 — Purchase orders have no record format.** `po_ref` is a bare string in `lot` and `cost_rows`, a packet
`action_class`, and half a board name — but `records:` has no `purchase_order` key, and the packet `payload` is
"class-specific; validated by a per-class sub-schema" with **no per-class sub-schema in `docs/schemas/`**. So
`sku_profiles.next_po_eta` ("source: approvals") has nothing to read, and `suppliers_pos.last_po`, `projects.spent_cad`
and the CAD 15,000 monthly ceiling are unbackable. The largest money object in the company is undefined. Fix: add a
`purchase_order` record (`po_ref, supplier, sku_lines[], currency, total, ordered_on, ship_by, eta, destination,
status, approval_id`) and `docs/schemas/payload-purchase-order.schema.json` as the first sub-schema.

**B10 — Pattern promotion gates cannot be evaluated from the pattern's fields.** `gates.supported` (l.49) needs "≥2
distinct days, ≥2 distinct sources, 0 unexplained contradictions"; `gates.validated` needs "≥2 SKUs and ≥30 days, plus a
machine-evaluable threshold written down". The front matter offers only `confirmations` and `contradictions` as ints.
Distinct days and sources would have to be parsed from the free-text Evidence body, whose line format (l.46) carries a
date and an id but **no source field**; nothing marks a contradiction "explained"; `scope` is prose
(`"marketplace:ca; department:advertising; skus:[ANB-017]"`) so "≥2 SKUs" is a regex over prose; and the threshold has
no field to live in. Fix: fixed 5-field evidence line `<date> · confirms|contradicts|explained · <obs id> · <source
class> · <sku|—>`; add `distinct_days`, `distinct_sources`, `distinct_skus`, `unexplained_contradictions` as `computed:`
counters; add `threshold: {type: string}`, required when `status: validated`.

**B11 — `state_file` is the one record with no front matter, and it is what a first run must write.**
`conventions.front_matter` (l.6) says "YAML between `---` fences at the top of **every** markdown record"; `state_file`
(l.129–133) specifies a `#` heading instead. Self-contradictory, and a generic validator cannot read the file the
watchdog, Run Health and §6.6 all depend on. `slot:<slot>` has no vocabulary anywhere (`department.yaml` uses `daily`;
§8 gives times; `bin/run-dept.sh <dept> <slot>` takes it as an argument), and Run Health needs `status`,
`proposals_open` and `log`, none of which the header carries. Fix: front matter
`{dept, date, slot, harness, run_minutes, tools_failed: [], status, proposals_open}` + the five `##` sections; enumerate
`slot: [exception, daily, weekly, monthly, quarterly]`.

**B12 — `ledger/kpis/README.csv` contradicts the schema and poisons the query path.** It has ten columns;
`kpi_row.columns` declares seventeen (adds `price, sessions, cvr, buybox_pct, bsr, rating, reviews`). It is also matched
by the documented `read_csv('ledger/kpis/*.csv')` glob, becoming a phantom row source in every DuckDB query. Fix: rename
it out of the glob; make its columns the schema's plus `currency`.

**B13 — Files the run procedure requires do not exist and are not schematized.** §7.2 fixes the load order and names
`strategy/CURRENT.md`: it does not exist (only a two-line `STRATEGY.md`), has no `records:` entry, and monday-schema
l.482 projects a doc from it. `requests/` does not exist **at all**, so §7.3 step 3 fails on run one for every
department. Also referenced but undefined: `state/integrity.md` (§5.4), `TARGETS.yaml`, `CHANGELOG.md`, `THRASH.md`,
`quarters/`, `playbooks/INDEX.md`, `memory/weekly/<week>.md` (repo-root `memory/`, while observations live under
`departments/<dept>/memory/`), `ledger/decisions.md` (Appendix A), and `briefs/<date>-tasks.md` — the whole Tasks for
Rami board (`why_human`, `est_minutes`, `hard_deadline`, `consequence`) exists in no record.

**B14 — Objectives and playbooks are boards and doc sources with no record behind them.** §7.1 makes quarterly
objectives an object sourced from `strategy/GOALS.md` and `projects.objective` is a `board_relation → strategy`, but no
`objective` record exists and the Strategy board has **no id column**, so nothing can be related to. Likewise §8.1 names
"Playbooks / skills" a knowledge class and the Knowledge board has `kind: Playbook`, but only `skill` is defined.
Decide: a playbook is a skill (delete the word) or a distinct record (define it).

---

## MAJOR

**M1 — "34 columns" is wrong in three places.** §5.3's heading says 34; its table has **36 rows**; monday-schema
`sku_profiles` has **35** explicit columns (the 36th, `name`, being monday's implicit item name); `record-schemas.yaml`
l.95 repeats "the board's 34 columns". Fix to 36 everywhere, or cut two.

**M2 — monday-schema columns carry no `source` key.** The only column keys used anywhere are `card, id, labels, note,
required, time, title, to, type, writer`. The repo→board mapping exists solely as a prose column in §5.3, so
`bin/build-sku-profiles.py` has no machine-readable input and the column↔field round-trip cannot be automated. Fix: add
`source: {kind: git|build|amazon|ads|keepa|approvals|lots, ref: <record>.<field>|<formula id>}` to every column.

**M3 — git-sourced board columns with no field in the product record.** `sku_profiles.owner_dept` (source: git) has no
front-matter field; nor do `products.category`, `unit_dims`, `pkg_dims`. Board `margin_floor` vs record
`margin_floor_pct` — pick one. Listing-level `lifecycle` is `{type: string}` with no enum while product-level has one,
and the board grain is SKU × marketplace, so the un-enumerated one renders. The `listings` key vocabulary is undeclared
(B7).

**M4 — Derived numbers with no formula.** `reorder_point`, `work_item.priority` ("from KR score, due date and blocking
count"), `projects.progress`, `project.slack_days` (`computed: true`), `landed_cost`. §7.4's decision score *is* fully
specified — that is the standard. Every `computed:` must be an expression or a named formula id, not a sentence.

**M5 — `cogs_status` cannot be satisfied.** §5.4 caps `economics` freshness at 36h, but `cost_rows` change per PO
(63-day lead times), so every SKU reads `Stale` forever. Split the stamp: `economics_fetched` (fees, ads: 36h) vs
`costs_effective_from` (per PO).

**M6 — `decision_item` and the Decisions board disagree both ways.** Board-only: `rank`, `dry_run`, `sku_link`,
`decision`, `outcome`. Record-only: `impact_basis`, `deadline_reason`, `actions`, `reproposal_of`, `times_reproposed`,
and `type: {enum:[approve,choose,ratify]}`, which is load-bearing in §7.3.

**M7 — Two different things are called "confidence".** §7.3's decision confidence is an evidence *class*
(0.3/0.6/0.9/1.0), stored on the board as `Low/Medium/High/Certain` with no declared mapping; `pattern.confidence` is a
continuous formula stored as numbers. §7.3's gate "a one-way door needs confidence ≥0.6" does not say which. Rename the
decision one `evidence_class`.

**M8 — The confidence formula's recency baseline is missing.** l.39 gives `recency 1.0 ≤30d, 0.8 ≤60d…` without saying
of what, measured from when. Research report 05 (l.132) supplies it — recency runs on `last_seen` relative to today —
so this is transcription loss, not a design gap. Write `recency(today − last_seen)` into `computed:`.

**M9 — Ledger integrity is neither reproducible nor concurrency-safe.** `hash` is "SHA-256 over canonical JSON" with no
canonicalization named, over arbitrary `input`/`output` objects: two harnesses produce different bytes. Name RFC 8785.
`seq` is "monotonic, gapless" in a file the hands runner (every 5 min) and a department run both append to, with no
allocation rule — make the hands runner the sole writer. `verification` is optional in the schema while §6.4 requires
it on every write row.

**M10 — Smaller mismatches.** The `requests` board `type` dropdown has **no labels** while the record enumerates eight;
§9 writes `needed-by`, the record `needed_by`; `work_item.effort_est_min` vs board `effort_est` (units unstated);
`supplier.lead_time_days_measured` is a list projecting to one board number with no aggregation rule; `scorecard_week`
lacks the board's `unit` and `as_of`; the Scorecard `target` is text while History's `target_num` is numbers;
`lock.line`'s `<dimension>` vocabulary is undefined though §9 enforces "one change per SKU per dimension per day";
`calendar_entry`'s `<kind>` is undefined while the board enumerates nine; `work_item.opened_by: {enum: departments +
rami}` is prose inside a schema; and `work_item`, `project`, `initiative`, `lot` and `supplier` have no title field,
so they cannot become monday items. Three id shapes coexist — the packet regex (ambiguous: `[a-z-]+-[a-z_]+` cannot be
parsed back into department and class), `dec-20260904-01` in §5.2, and `PO-2026-019` — and §5.2's decision-history
example does not match the format its own record declares.

---

## MINOR

`records:` keys mix entity names with row/period names (`kpi_row`, `sku_snapshot`, `scorecard_week`). §8.1 is headed
"Eight classes" and lists **nine**. `outcomes.csv` is unpartitioned though §8.4 ranks CSV bloat a risk, and has no row
id, so a re-scored approval collides. `ledger/actions.jsonl` is empty with no rule that `seq: 1` carries
`prev_hash: GENESIS`. `markets/` has no record type.
`approvals/{approved,rejected,expired,failed}/` are in the record path but absent from the repo.

---

## The minimum record set needed tonight

A first run must read state, write a state file, write an observation, write a proposal. Six records, three of them
shrunk.

**Get right first — none of this is additively fixable; every row written from tonight inherits it:**

1. **Directories.** `mkdir -p requests/<each of nine>/{inbox,done}` and `approvals/{approved,rejected,expired,failed}`.
   Without the first, §7.3 step 3 fails on run one.
2. **`conventions.enums`** — one block fixing `marketplace: [ca, us, walmart-ca]`, `department` (the nine, no
   chief-of-staff), `harness`, `action_class`, `slot`, `currency`; everything else references it by name.
3. **Ids** — observation, fact, and one packet id shape. Retrofitting ids onto written records is the one thing this
   design cannot do cheaply.
4. **Money** — decimal strings, and `currency` on every money-bearing record including `kpi_row`.

**The six records:**

5. **`state_file`** with YAML front matter `{dept, date, slot, harness, run_minutes, tools_failed, status,
   proposals_open}` + the five `##` sections. This is what the watchdog and Run Health read.
6. **`observation`** — one line, six fields: `obs-id · time · scope · claim · source · ledger`.
7. **`approval_packet`, thin** — enforce `id, schema_version, department, tier, action_class, status, created,
   expires, marketplace, currency, evidence[], impact, if_rejected` plus `metric, expected, review_on, design`. Drop
   `preconditions`, `guardrails`, `dry_run`, `locks`, `idempotency_key` from `required` until the hands runner exists:
   nothing executes tonight, so a packet is a proposal document, not an execution order. Delete `chief-of-staff` and
   the `ANB-` pattern while in the file.
8. **`request`** as written, plus its eight `type` labels copied onto the board.
9. **`product`**, cut to what a T0 run reads: `sku, brand, name, class, lifecycle, listings.<mkt>.{asin, price_band,
   margin_floor_pct, safety_stock_days, lead_time_days}`, one `cost_rows` entry with `currency`, and a `fees` block
   (B8). Seed **one** real SKU. `season_index`, `certifications`, `hazmat`, `readiness`, `freshness` are additive.
10. **`fact`** as written, plus an id.

**Safe to defer:** `pattern`, `skill` and every promotion gate (nothing to harvest until the first Monday — but fix B3
and B10 *before* that librarian pass, not after); `lot`, `purchase_order`, `supplier`; `project`, `key_result`,
`initiative`, `objective`, `scorecard_week`, `decision_item`; `lock`, `calendar_entry`, `integrity_report`;
`sku_snapshot`, `kpi_row`, `outcome`, `ledger_entry` (at T0 nothing writes to an account, so the ledger stays empty and
M9 can wait); the 36-column board and the whole monday projection.

**One deletion tonight:** create `strategy/CURRENT.md` or strike it from §7.2. A mandated load order naming a missing
file makes every run open with an error — the "flaw in five seconds" complaint, mechanised.

**Rule that makes later growth cheap:** the validator accepts unknown front-matter keys and validates the known ones.
New fields and new record types are then free; only items 2–4 are not.
