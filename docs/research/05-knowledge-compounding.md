> Research report produced 2026-09-06 during the founding engagement. Where it mentions files of an earlier repository, treat those as context the researcher had, not as part of this design. The design that governs is docs/ANABTAWI-OS-DESIGN.md.

# 05 — Knowledge and memory that compounds

Research date: 2026-09-06. Author: research agent. Scope: what the Anabtawi company must remember, where it should live, and the loop that turns observations into validated procedure across Claude Code, Codex CLI, Grok, Claude Cowork and monday agents.

## 0. Method, and an honest note on sourcing

Network egress from this session is restricted to an allowlist. `code.claude.com`, `platform.claude.com` and the monday.com first-party MCP were reachable and were opened directly today — those claims are tagged **VERIFIED**. `agents.md`, `developers.openai.com`, `docs.mem0.ai`, `docs.letta.com`, `getzep.com`, `supabase.com`, `duckdb.org`, `arxiv.org` and `developer.monday.com` were all refused by the proxy (`EGRESS_BLOCKED` / `CONNECT tunnel failed, 403`); claims about those products come from search-engine result summaries and are tagged **REPORTED**, with the primary URL given so Rami can open it in a browser. Anything I could not pin down is tagged **UNKNOWN** with what I tried. Vendor pricing is date-stamped and should be re-checked before any commitment.

---

## 1. Taxonomy: what this business has to remember

Eight classes. The split is not academic — each class has a different write frequency, a different reader, and, most importantly, **a different retrieval mode**. Getting the retrieval mode right is what decides whether you need a vector database at all.

| # | Class | Example | Who writes | Write freq | Who reads | Read freq | Size @ 12 months (1 brand) | Retrieval need |
|---|---|---|---|---|---|---|---|---|
| 1 | **Raw observations** | "ANB-017 buy-box lost 3h on Sep 4, competitor at 18.90" | every department | daily, append-only | weekly reviewer only | weekly (batch) | ~2,250 files, 4–8 MB | time-range scan + grep; never loaded whole |
| 2 | **Durable facts** | supplier lead time 21d; FDA FFR window Oct 1–Dec 31; CA seller UUID | department, on promotion from (1) | ~weekly | every run of the owning dept | every run | 9 × ≤300 lines ≈ 110 KB | exact lookup, loaded whole |
| 3 | **Patterns** (hypotheses with counters) | "Negating a relevant low-CVR term costs rank within 10 days" | weekly review agent | weekly | weekly review; any dept proposing in that domain | weekly + on demand | 60–150 files, ~200 KB | tag/scope filter, then exact read |
| 4 | **Playbooks / skills** (validated procedure with thresholds) | `negatives/SKILL.md` threshold formula | monthly review, CEO-approved | monthly | every relevant run | on trigger | 25–45 skills, ~300 KB | description-matched trigger (Level-1 metadata), then exact read |
| 5 | **Decisions and outcomes** | approval `20260904-supply-chain-po-anb-017` + what happened | departments write; scoring job writes back | daily | proposal-time precedent check; monthly falsification | daily + monthly | 1,200–2,500 approval files; outcomes.csv ~2k rows | exact by id; aggregate by action_type; **time-series** |
| 6 | **SKU histories** | ANB-017: price, velocity, ads, returns, every decision that touched it | Finance (numbers), depts (narrative) | daily (numbers), episodic (narrative) | pricing, supply chain, catalog, CEO | daily | kpis: ~65k rows/yr ≈ 7 MB; 60 narrative files | **time-series aggregation** (SQL), plus exact narrative read |
| 7 | **Strategy / goal state** | north star, quarterly KRs, current vs target, revision log | CEO agent; Rami approves | weekly append, quarterly rewrite | every dept (extract), CEO (whole) | every run | <60 KB | exact, loaded whole (extract) |
| 8 | **Agent operating notes** | "DataDoe `exports_sources_get` times out over 90 days; page it"; "Grok bot stalls past 4 tool calls" | any agent, on failure | on incident | every run, all harnesses | every run | <40 KB | exact, loaded whole |

Two classes that are deliberately **not** memory:

- **Raw data exports** (DataDoe pulls, Ads reports). Re-fetchable from the source of truth. Committing them is how a 7 MB repo becomes a 4 GB repo. Cache them outside git (`.exports/`, gitignored), cite them by report id and date in the observation that used them.
- **Harness-native memory.** Claude Code auto memory writes to `~/.claude/projects/<project>/memory/` and is explicitly **machine-local: "Files are not shared across machines or cloud environments"** (VERIFIED, https://code.claude.com/docs/en/memory, opened 2026-09-06). Codex keeps `~/.codex/memory/` per machine (REPORTED, https://codex.danielvaughan.com/2026/04/06/codex-cli-persistent-memory-mcp-servers/). Grok memory is account-bound with no documented export (REPORTED, https://blog.memoryplugin.com/how-grok-memory-works/). Claude Cowork memory is shared with chat memory but **only for cloud runs — local Cowork sessions do not use it** (REPORTED, https://techcrunch.com/2026/08/25/claude-cowork-finally-remembers-what-you-told-the-app-in-chat/). None of these is portable, auditable, or forkable to a second brand. **Recommendation: treat all harness-native memory as scratch, and turn Claude Code auto memory off for this repo** (`{"autoMemoryEnabled": false}` in `.claude/settings.json` — VERIFIED same doc). If a harness learns something durable, the run procedure must make it write that fact into the repo, not into its own store.

The retrieval-mode column is the finding that matters: **six of eight classes are exact lookup or time-series. Only class 3 and class 5 precedent search ever want semantic retrieval, and both are small enough (≤150 pattern files, ≤2,500 approvals) that a generated index plus grep beats an embedding store at this scale.** That kills the case for a cloud memory vendor in year one.

---

## 2. Candidate layers, scored

Scoring 1–5, higher is better, against the criteria Rami asked for. "Harness-portability" means every harness can read *and write* it with zero custom code.

| Criterion | Git markdown repo | monday docs + boards | SQLite/DuckDB file | Supabase PG + pgvector | Mem0 cloud | Letta cloud | Zep | Obsidian vault synced |
|---|---|---|---|---|---|---|---|---|
| Harness portability | **5** | 3 | 4 | 3 | 2 | 1 | 2 | 4 |
| Phone readability | 3 | **5** | 1 | 2 | 2 | 2 | 1 | **5** |
| Structure for numbers | 2 | 3 | **5** | **5** | 1 | 1 | 2 | 2 |
| Semantic retrieval | 2 | 3 | 1 | **5** | **5** | 4 | **5** | 3 |
| Versioning / audit | **5** | 2 | 2 | 2 | 2 | 2 | 4 | 3 |
| Cost | **5** | 4 | **5** | 3 | 2 | 3 | 2 | 4 |
| Maintenance for a solo operator | 4 | 3 | 3 | 2 | 3 | 2 | 3 | 3 |
| Multi-brand isolation | **5** | 4 | **5** | 4 | 3 | 3 | 3 | 4 |
| Export | **5** | 3 | **5** | 4 | 2 | 2 | 2 | **5** |
| **Total (45)** | **36** | 30 | 31 | 30 | 22 | 20 | 24 | 33 |

Justification for the non-obvious scores:

**Git markdown repo (36).** Portability 5: every harness reads markdown from a working directory with no adapter. Claude Code loads `CLAUDE.md` from cwd and every parent directory, concatenated root-down, with `@path` imports to four hops — the `CLAUDE.md` → `@AGENTS.md` bridge already in this repo (VERIFIED, code.claude.com/docs/en/memory). Codex chains `~/.codex/AGENTS.md` plus every `AGENTS.md` from git root down, capped at 32 KiB with silent truncation (REPORTED, https://www.codegateway.dev/en/blog/agents-md-playbook-2026). Versioning 5: git is the only candidate where "when did we learn this and who changed it" is free and permanent, which the constitution already requires (§6.4). Numbers 2 is the real weakness — markdown tables do not aggregate.

**monday docs + boards (30).** monday's own knowledge service states custom agents "Use your boards, data, docs, workflows, and permissions to analyze and connect signals" and can "understand external context, by connecting external files" (VERIFIED via the monday MCP, queried 2026-09-06, citing https://support.monday.com/hc/en-us/articles/33347027353746-Get-started-with-the-monday-AI-Agent-builder). Agent knowledge is granted per resource, `READ`/`READ_WRITE` on a `BOARD` or `DOC`; docs are readable and writable by any MCP-capable harness and carry a native version history with diffs (VERIFIED — `manage_agent_knowledge` and `read_docs` tool schemas, inspected today). But audit is per-doc, not cross-repo; budgets are ~5–10M complexity points/min and 10,000 daily calls on Pro (REPORTED, https://developer.monday.com/api-reference/docs/rate-limits, page blocked); and a board is a poor home for 65k KPI rows. **monday is the surface, not the store.**

**SQLite/DuckDB file (31).** The right shape for classes 5 and 6 — one `duckdb` invocation answers "median ACOS by SKU for the 14 days after each approved bid change", which no markdown layout can. Versioning 2 because the file is binary and git cannot diff or merge it (REPORTED, https://sqlite.org/whynotgit.html). Fix: keep the *source* as partitioned CSV in git and rebuild the database on demand (REPORTED, csvdb pattern, https://github.com/jeff-gorelick/csvdb). That raises versioning to 5 and is what I recommend.

**Supabase Postgres + pgvector (30).** The best answer if the numbers layer outgrows a file; free tier holds ~50–80k vectors, Pro $25/mo removes inactivity pauses (REPORTED, 2026, https://aibizhub.io/articles/supabase-vector-free-tier-2026/). Adds a service, a credential and no history unless you build it. Not year one.

**Mem0 (22) / Letta (20) / Zep (24).** Strong at the thing this business needs least. Mem0: Hobby free (10k memories), Starter $19/mo, Pro $249/mo with graph memory gated to Pro (REPORTED, https://theaiagentindex.com/agents/mem0). Letta's memory blocks with sleep-time agents that asynchronously refine shared blocks is architecturally closest to what we want, but is bound to Letta's own agent runtime (REPORTED, https://docs.letta.com/guides/agents/architectures/sleeptime/). Zep/Graphiti is the most interesting: a bi-temporal graph where each edge carries `t_valid`/`t_invalid`, so "the FBA fee changed on Apr 15, our old fact is invalid from then" is first-class rather than a manual edit (REPORTED, https://arxiv.org/abs/2501.13956). We will hand-roll that with `since:` and `superseded_by:`. **All three lose on the same three axes: no git audit trail, weak export, and a second brand means a second tenant with a second bill.**

**Obsidian vault synced (33).** The same plain markdown as candidate A plus a genuinely good phone client, but Obsidian Sync is not git — no commit, no PR, no blame. **Best use: point Obsidian at the git working copy**, so Rami reads on his phone exactly what the agents commit. A free upgrade, not a separate layer.

### The pick

**Git markdown repo as the spine + partitioned CSV/DuckDB for numbers + monday as the human surface + Obsidian pointed at the same folder.** No vector database, no memory vendor, in year one.

- **Git markdown** holds classes 1, 2, 3, 4, 7, 8 and the narrative half of 5 and 6. It is the only candidate that scores 5 on portability, audit, cost, multi-brand and export simultaneously.
- **CSV in git + DuckDB at query time** holds the numeric half of 5 and 6. Partitioned `ledger/kpis/YYYY-MM.csv` stays diffable and greppable; `duckdb -c "select ... from read_csv('ledger/kpis/*.csv')"` gives real aggregation with zero infrastructure and zero cost. The `.duckdb` file itself is a build artifact, gitignored.
- **monday** holds the approval queue, the daily decision list, and dashboards over data pushed from `ledger/`. It is a projection, never a source of truth. This matches the control-plane decision already made in `docs/DECISION-CONTROL-PLANE.md`.
- **Skills (`SKILL.md`)** are the transport for class 4 and are the one genuinely cross-harness format available: required frontmatter is only `name` (≤64 chars, lowercase/digits/hyphens, must match folder name) and `description` (≤1024 chars, must say both what it does and when to use it); metadata costs ~100 tokens per skill at startup and the body only loads on trigger, under 5k tokens (VERIFIED, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, opened 2026-09-06). Codex loads the same format from `.agents/skills` (REPORTED, https://www.agensi.io/learn/codex-cli-agents-md-complete-guide), and Grok shipped a "Skills" procedural-memory feature in Grok 4.3 on 2026-05-18 (REPORTED, https://theplanettools.ai/blog/xai-grok-skills-cross-conversation-persistence-document-generation-may-2026 — whether Grok ingests a SKILL.md folder verbatim is **UNKNOWN**; x.ai docs were egress-blocked).

---

## 3. The compounding loop

The design principle comes from Agentic Context Engineering (ICLR 2026): treat the context as an **evolving playbook that accumulates and organizes strategies** rather than a summary that gets rewritten, because rewriting causes *brevity bias* (dropping domain detail) and *context collapse* (erosion over iterations); reported gains of +10.6% on agent benchmarks and +8.6% on finance (REPORTED, https://arxiv.org/abs/2510.04618, abstract page egress-blocked, figures from search summary 2026-09-06). Its Generator / Reflector / Curator split maps cleanly onto departments / weekly review / Chief of Staff.

**The operating rule that follows: never rewrite a playbook wholesale. Append or amend numbered entries, each with its own evidence and status.**

### 3.1 Daily — every department (already in the run procedure, §7.9)

Append to `departments/<dept>/memory/YYYY-MM-DD.md`. One observation per line, never edited after the day:

```
- 2026-09-06T06:41 · obs · scope:ANB-017/ca · Buy box lost 3h10m; competitor SELLER-X at CAD 18.90 vs our 19.75.
  source: datadoe:buybox_hourly@2026-09-06 · ledger: none
```

### 3.2 Weekly — Monday 06:00, Chief of Staff wearing the Librarian hat

Runs *before* the departments, so the week starts with updated knowledge. Four steps, all mechanical:

1. **Harvest.** Read the last 7 days of every department's observation files. Group by `scope` and by claim.
2. **Promote or reinforce.** Any claim seen ≥3 times, on ≥2 distinct days, from ≥2 distinct sources, becomes or reinforces a pattern file. Increment `confirmations`, update `last_seen`, append the evidence link.
3. **Contradict.** Any observation that contradicts a live pattern increments `contradictions` and is appended to the pattern's evidence list with `contradicts: true`. Contradictions are never deleted — that is the difference between a knowledge base and a diary.
4. **Decay sweep.** Anything whose `last_seen` is >90 days sets `status: decaying`; >180 days moves to `memory/archive/` (still in git, still greppable, no longer loaded).

Output: a diff-only commit plus 10 lines in `state/chief-of-staff.md` naming what was promoted, contradicted and decayed.

### 3.3 Pattern file format — `patterns/<scope>-<slug>.md`

```yaml
---
id: ads-negating-relevant-terms-costs-rank
status: hypothesis | supported | validated | falsified | decaying | archived
claim: Negating a relevant low-CVR search term in exact loses organic rank on that term within 10 days.
scope: marketplace:ca; department:advertising; skus:[ANB-017, ANB-021]
first_seen: 2026-08-11
last_seen: 2026-09-02
confirmations: 4
contradictions: 1
confidence: 0.62
seasonality_guard: false        # true if the evidence window contains Ramadan / Q4
supersedes: null
superseded_by: null
next_test: Hold ANB-034 negatives for 14d and compare rank drift.
owner: advertising
---
## Evidence
- 2026-08-11 · confirms · departments/advertising/memory/2026-08-11.md#L14 · rank 7→19 in 9d after negating "tahini organic"
- 2026-08-25 · confirms · ledger/actions.jsonl:2026-08-25T06:44:02+03:00
- 2026-09-02 · CONTRADICTS · departments/advertising/memory/2026-09-02.md#L6 · rank held on ANB-021; term had 0 organic impressions before negation
## Reading
The contradiction suggests the rule only holds for terms with existing organic impressions. Narrow the claim before promoting.
```

**Confidence must be dumb and reproducible**, not a model's vibe: `confidence = (confirmations / (confirmations + contradictions + 1)) × recency`, where `recency = 1.0` if `last_seen` within 30d, `0.8` within 60d, `0.6` within 90d, `0.3` beyond. Any agent can recompute it and get the same number. Write the formula into `docs/CONVENTIONS.md` so it is auditable.

**Promotion gates:**

| Transition | Gate |
|---|---|
| observation → `hypothesis` | 1 observation with a source link |
| `hypothesis` → `supported` | ≥3 confirmations, ≥2 distinct days, ≥2 distinct sources, 0 unexplained contradictions |
| `supported` → `validated` | ≥5 confirmations across ≥2 SKUs **and** ≥30 days, **and** a threshold a machine can evaluate is written down |
| `validated` → playbook/skill | CEO run proposes; Rami approves the diff; skill gets `evidence:` frontmatter listing the pattern id |
| any → `falsified` | contradictions > confirmations, or a monthly falsification run fails it |

### 3.4 Monthly — first Monday, CEO agent + Chief of Staff

The falsification pass. This is the step everyone skips and the one that makes the difference between compounding and accumulating.

1. For each `validated` pattern and each playbook rule with a numeric threshold, pull the last 30 days of outcomes from `ledger/outcomes.csv` and `ledger/kpis/*.csv`.
2. Compute the rule's realised hit rate: of the N times the rule fired, how many produced the predicted direction of movement?
3. Write the result to the playbook's own evidence log as a dated line. **Demote** below 60% hit rate over ≥10 firings; **retire** below 40%. A rule with <10 firings in 90 days is flagged `unexercised`, not demoted — that is a different problem (nobody is using it).
4. Contradiction check across departments: grep all `MEMORY.md` durable facts for the same `scope` and flag any two facts that disagree. Single-writer rule: each fact class has exactly one owning department; a second department wanting to change it files a typed request.
5. Update `strategy/STRATEGY.md` assumptions. Every strategy assumption gets an id and a linked pattern. If the pattern falsifies, the assumption is marked `assumption_status: challenged` and appears in the CEO's ranked list for Rami — never silently rewritten. Quarterly boundary is the only place an objective changes (already the anti-thrash rule in `DECISION-CONTROL-PLANE.md`).

### 3.5 Playbook / skill format additions

Skill frontmatter stays spec-legal (only `name` and `description` are read by the runtimes; spec-compliant runtimes ignore unknown keys — VERIFIED, platform.claude.com), so we add our governance fields underneath without breaking portability:

```yaml
---
name: negatives
description: When a search term may be negated. Use before proposing or applying any negative keyword.
# --- company fields, ignored by runtimes ---
status: validated
since: 2026-07-14
last_falsified: 2026-09-01
hit_rate: 0.78            # over 23 firings
evidence: [ads-negating-relevant-terms-costs-rank, ads-cvr90-threshold]
scope: marketplace:ca
owner: advertising
review_by: 2026-12-01
---
```

---

## 4. How outcomes get scored

Today an approval says what it expects ("Zero stockout days through Ramadan buffer") in prose. Prose cannot be scored. Three additions close the loop.

**(a) Every approval declares its metric.** Add to the `approvals/` front-matter schema in `docs/CONVENTIONS.md`:

```yaml
goal_id: KR-CA-REV-Q1
metric: cover_days | acos | units | contribution_margin | stockout_days | session_cvr
scope: ANB-017/ca
baseline: 11.2
expected: ">= 21 by 2026-10-05"
measure_window: 14d_after_execution
review_on: 2026-10-05
design: ab | prepost | prepost-matched | none
control_set: [ANB-021, ANB-034]     # required when design=prepost-matched
```

**(b) A scoring job.** Finance's daily run, step 0, at 07:15 Asia/Jerusalem (after Amazon's 07:00 business-day close). For every approval in `approvals/executed/` whose `review_on <= today` and `scoring_status: pending`:

1. Query `ledger/kpis/*.csv` via DuckDB for `metric` on `scope` over `measure_window`, and for the `control_set` over the same window.
2. Compute `actual`, `delta_vs_baseline`, and where a control set exists, `delta_net_of_control`.
3. Append one row to `ledger/outcomes.csv`:
   `approval_id,goal_id,metric,scope,design,baseline,expected,actual,delta,delta_net_of_control,verdict,scored_on,evidence_query`
   where `verdict ∈ {hit, miss, inconclusive, unmeasurable}`.
4. Write back in three places: set `outcome:` and `scoring_status: scored` in the approval file; append a dated line to `products/<sku>.md` under `## Decision history`; append a dated line to the evidence log of every playbook whose `evidence:` list produced the rule that fired.
5. Anything `unmeasurable` is a schema bug, not a business result — it goes into `state/cash.md` exceptions so it gets fixed.

**(c) Be honest about causality.** Most of these are not experiments. A price change during Ramadan, scored pre/post, measures Ramadan. Hence the mandatory `design` field and the matched control set: comparing ANB-017 against three untouched SKUs in the same category over the same window nets out seasonality without pretending to be an RCT. Where a true split *is* available — ads at campaign level, coupons on near-identical SKUs, price bands across a portfolio — use it and mark `design: ab`. The monthly falsification run should weight `ab` outcomes above `prepost-matched`, and ignore `prepost` alone for promotion decisions. Writing `design: prepost` and calling the result proof is the single easiest way for this system to teach itself something false.

The `ledger/decisions.md` file already exists; it becomes the human-readable index generated from `outcomes.csv`, not a hand-maintained file.

---

## 5. Getting the same knowledge into every harness

### 5.1 Loading order (identical everywhere)

| # | Layer | Source | Budget (tokens) |
|---|---|---|---|
| 1 | Constitution | `AGENTS.md` (root), reached by `CLAUDE.md` → `@AGENTS.md` | ~2,000 |
| 2 | Department charter | `departments/<dept>/AGENTS.md` | ~1,400 |
| 3 | Goal extract | generated `strategy/CURRENT.md` — this quarter's KRs, current vs target, lock date | ~400 |
| 4 | Durable facts | `departments/<dept>/memory/MEMORY.md`, hard cap 300 lines | ~3,000 |
| 5 | Operating notes | `ops/OPERATING-NOTES.md` — what tools flake, what formats work | ~500 |
| 6 | Today's state | only the `state/*.md` the charter names | ~2,400 (3 files) |
| 7 | Inbox | `requests/<dept>/inbox/*` | ~600 |
| 8 | Skill metadata | ~100 tokens per skill × 30 (VERIFIED, platform.claude.com) | ~3,000 |
| | **Resident total** | | **~13,300; hard ceiling 20,000** |
| 9 | Skill bodies, patterns, ledger queries | on demand only | not resident |

The ceiling is not arbitrary. Anthropic's own guidance is "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence" (VERIFIED, code.claude.com/docs/en/memory). Context-rot work reports measurable degradation in all 18 frontier models tested as input length grows (REPORTED, https://www.morphllm.com/context-rot). At 13k resident tokens the department keeps ~95% of its window for actual work, and no instruction competes with 40 pages of history for attention.

### 5.2 One source, five harnesses

- **Claude Code** — `CLAUDE.md` containing `@AGENTS.md` (already in place; VERIFIED this is the documented bridge, and that Claude Code reads `CLAUDE.md`, *not* `AGENTS.md`). Skills live in `.claude/skills/`. Auto memory **off**.
- **Codex CLI** — reads `AGENTS.md` natively, root-down concatenation, **32 KiB cap with silent truncation** (REPORTED). This is a live constraint: the root `AGENTS.md` is currently ~6.7 KB; the chain root + department must stay under 32 KiB forever. Add a CI check. Skills at `.agents/skills/` (symlink to `shared-skills/` and the department skills).
- **Claude Cowork** — same repo; note its local sessions do not use Claude's account memory (REPORTED), which is fine because we do not rely on it. Cowork is a review surface, per the control-plane decision.
- **Grok** — cannot mount the repo. Generate `runtimes/grok/BOOTSTRAP.md` from layers 1–5 with a build script (`make bootstrap`), pasted or synced into the bot's system prompt. Regenerated on every commit that touches those layers; stale bootstrap is a lint failure.
- **monday agents** — grant the agent `READ` on the boards/docs that mirror layers 3, 6 and 7, and `READ_WRITE` only on the decision board (VERIFIED, `manage_agent_knowledge` supports exactly `BOARD`/`DOC` × `READ`/`READ_WRITE`). A nightly job publishes `strategy/CURRENT.md` and the ranked brief into monday docs via `create_doc`/`update_doc`.

### 5.3 Summarization rules (how it stays small)

1. **Observations never shrink and never load.** They are grepped, not read.
2. **MEMORY.md is capped at 300 lines** (already the convention). Eviction rule when full: drop the entry with the oldest `since:` that has not been cited by a pattern or playbook in 90 days. Log the eviction — never silent.
3. **State files are overwritten each run** (already the convention). They are a snapshot, not a log.
4. **Patterns are appended to, never rewritten.** The ACE anti-collapse rule.
5. **Playbooks amend numbered entries.** A superseded threshold gets `superseded_by:` and stays.
6. **The ledger is never summarized.** It is queried. Any "summary" of the ledger is generated on demand and not committed.
7. **Weekly digest**: the Chief of Staff writes ≤20 lines per department per week into `memory/weekly/YYYY-Www.md`. This is the only compression step in the system, and it compresses observations *into pattern evidence*, not into prose.

---

## 6. Multi-brand

Split the repo along the seam between **Amazon mechanics** and **this brand's facts**:

| Shared (brand-agnostic) | Brand-specific |
|---|---|
| Run procedure, conventions, tier model, approval schema | `products/`, `suppliers/`, `markets/` |
| Ads campaign structure, negatives thresholds *as formulas* | the threshold *values* fitted to this brand's CVR |
| Listing standard, FBA shipment procedure, ungating checklists | `state/`, `ledger/`, `approvals/`, `briefs/` |
| Account-health playbooks, FDA/FSVP calendars (US grocery) | `strategy/`, `departments/*/memory/` |
| DataDoe export recipes, MCP config templates (`${VAR}` refs) | credentials (vault, never in repo) |

**Mechanism.** Promote `shared-skills/` and the brand-agnostic playbooks into their own private repo, `anabtawi-core`, consumed two ways from one copy:

- **Claude Code**: publish it as a plugin marketplace. `marketplace.json` can source plugins from a separate GitHub repo and pin them with `ref` (branch/tag) or `sha` (exact commit, takes precedence), and a plugin bundles `skills`, `commands`, `agents`, `hooks` and `mcpServers` together. Private distribution works by hosting `marketplace.json` in a private repo — access control falls back to the git host (VERIFIED, https://code.claude.com/docs/en/plugin-marketplaces, opened 2026-09-06).
- **Codex / anything else**: a git submodule at `.agents/skills/core` pinned to the same tag.

A second brand is then: `git init brand-two`, add the core submodule/marketplace at the pinned tag, write `strategy/`, `products/`, `suppliers/`, `markets/`, a monday workspace, a DataDoe credential. **Zero new subscriptions, one afternoon.** Pinning by tag is what stops a fix made for brand two from silently changing brand one's ads thresholds — bump deliberately, per the same discipline already applied to Paperclip releases.

Isolation that must hold: separate ledgers, separate approval queues, separate monday workspaces, separate credentials. Cross-brand learning happens exactly once a month, in one direction: a pattern validated in two brands gets promoted into core with `scope: brand-agnostic`. A pattern validated in one brand never enters core.

DataDoe's Skill Hub ships pre-built Amazon workflows installable into Claude Code and Codex (REPORTED, https://www.datadoe.com/hub). Treat those as **source material to vendor into `anabtawi-core` at a pinned copy**, not as live dependencies — otherwise a vendor edit changes company procedure with no diff, no approval and no ledger entry, which violates §6.4 of the constitution.

---

## 7. Concrete recommendation

### 7.1 Layout (additions marked `NEW`)

```
anabtawi-company/
├── AGENTS.md                       # constitution (must stay ≪32 KiB with dept charter)
├── CLAUDE.md                       # @AGENTS.md
├── strategy/
│   ├── STRATEGY.md                 # assumptions carry ids + linked pattern ids   NEW
│   ├── GOALS.md
│   └── CURRENT.md                  # generated quarter extract, ~400 tok          NEW
├── ops/
│   └── OPERATING-NOTES.md          # class 8: what flakes, what format works      NEW
├── patterns/                       # class 3, one file per hypothesis             NEW
│   └── ads-negating-relevant-terms-costs-rank.md
├── playbooks/                      # class 4, narrative; thresholds live in skills
├── shared-skills/                  # → becomes anabtawi-core (pinned)
├── departments/<dept>/
│   ├── AGENTS.md
│   ├── skills/*/SKILL.md
│   └── memory/{MEMORY.md, YYYY-MM-DD.md, weekly/YYYY-Www.md, archive/}   NEW dirs
├── ledger/
│   ├── actions.jsonl
│   ├── kpis/YYYY-MM.csv            # partitioned                                  NEW
│   ├── outcomes.csv                # decision → metric → verdict                  NEW
│   └── decisions.md                # generated index
├── approvals/{pending,approved,rejected,expired}/
│   └── executed/YYYY/MM/           # partitioned                                  NEW
├── products/<sku>.md               # + "## Decision history" section              NEW
├── runtimes/grok/BOOTSTRAP.md      # generated                                    NEW
├── .exports/                       # gitignored DataDoe/Ads pulls                 NEW
└── docs/CONVENTIONS.md             # + pattern schema, confidence formula, scoring schema
```

Who runs what: **Chief of Staff** — weekly Librarian pass, Monday 06:00 (before departments). **Finance** — daily scoring job at 07:15. **CEO** — monthly falsification, first Monday, and the strategy-assumption update. **Every department** — daily observations, and the rule that any durable fact learned goes into the repo, never into harness memory.

### 7.2 What breaks first at 12 months

Ranked by likelihood × damage.

1. **Nobody runs the weekly review; the whole thing degrades into a diary.** Highest risk by far. Fix: the Librarian pass is a scheduled department run with its own state file, so a missed run shows as stale in the brief (§6.6 already makes a stale state file a failed run).
2. **`ledger/kpis` at ~65k rows/year becomes unreadable to agents and bloats git.** Fix: monthly partitioning + DuckDB-at-query-time from day one, not month nine.
3. **`approvals/executed/` reaches 1,500+ files in one directory**, and a glob dumps the listing into context. Fix: `YYYY/MM/` partitioning from day one.
4. **Codex's 32 KiB AGENTS.md cap silently truncates** as the constitution and charters grow (REPORTED). Fix: a CI check failing the commit if root + any department charter exceeds 28 KiB.
5. **Playbook fossilization across markets and seasons.** A rule fitted on CA data in a Ramadan window applied to US. Fix: mandatory `scope:` plus `seasonality_guard`; a guarded rule cannot reach `validated` without non-seasonal evidence.
6. **Evidence links rot** when files move. Fix: cite stable ids (approval id, ledger timestamp, pattern id), not paths; link-check weekly.
7. **Two sources of truth** — Rami approves against a stale monday card. Fix: monday is strictly a projection, every published doc stamped `generated_from: <commit sha>`.
8. **MEMORY.md contradiction drift** across nine departments. Fix: single-writer rule per fact class, monthly cross-department contradiction grep.
9. **PII creeping into memory files** from buyer messages. Fix: pre-commit scan, and a hard rule that customer observations record the *pattern*, never the buyer.
10. **Repo size** from committed exports. Fix: `.exports/` gitignored, 256 KB per-file limit in the pre-commit hook.

---

## Implications for the design

1. **Do not buy a memory product this year.** Six of eight knowledge classes need exact lookup or time-series retrieval, at volumes (150 patterns, 2,500 approvals, 65k KPI rows) where grep and DuckDB beat embeddings on accuracy, cost, auditability and portability. Mem0/Letta/Zep all fail the same three tests: no git audit trail, weak export, per-brand billing. Zep's bi-temporal fact validity is the one idea worth stealing — steal it as `since:` / `superseded_by:` fields, not as a subscription.
2. **Turn off harness-native memory and say so in the constitution.** Claude Code auto memory is machine-local and unsynced (VERIFIED); Codex and Grok are equally non-portable. A company whose knowledge lives in three machines' home directories cannot be forked, audited or handed to a second harness. Add a hard rule to §6: *no agent may store a durable fact anywhere but this repo.*
3. **The three schema additions are the whole project.** Pattern front-matter with confirmations/contradictions; approval front-matter with metric/review_on/design; `outcomes.csv`. Without them the loop is prose and nothing compounds. With them, everything else is a cron job.
4. **The `design:` field is the integrity of the system.** Pre/post scoring during Ramadan will manufacture confident, false playbooks. Mandating a matched control set — or an honest `design: none` — is the difference between a business that learns and one that hallucinates a strategy.
5. **Partition on day one.** KPI CSVs by month, executed approvals by year/month. Both are five minutes now and a migration in month nine.
6. **Skills are the only true cross-harness knowledge format that exists**, and the ~100-tokens-at-startup / body-on-trigger economics (VERIFIED) is exactly the budget shape a nine-department company needs. Encode every validated threshold as a skill, not as prose in a charter.
7. **Multi-brand is a pinning problem, not an architecture problem.** `anabtawi-core` as a private plugin marketplace pinned by `sha`, consumed by Claude Code natively and by Codex as a submodule. Second brand costs one afternoon and zero new subscriptions.

## Open questions

1. **Does Grok ingest a `SKILL.md` folder, or only its own in-product Skills object?** x.ai docs were egress-blocked. If it is the latter, `runtimes/grok/BOOTSTRAP.md` must also carry the top ~5 skill bodies inline, which changes the Grok budget materially. Rami should check https://docs.x.ai directly.
2. **Codex's `~/.codex/memory/` — is it per-machine only, and can it be pointed at a repo path?** If it can be redirected (as Claude Code's `autoMemoryDirectory` can be — VERIFIED), we could let Codex write observations natively rather than through the run procedure. Primary doc was blocked.
3. **monday API budget under a daily sync.** Reported figures are 10,000 daily calls and 5–10M complexity points/min on Pro (REPORTED, unverified). Publishing nine state docs plus a decision board nightly should be trivial, but a dashboard over 65k KPI rows through the API would not be. Confirm before designing any monday dashboard that reads item-level history.
4. **monday doc version history depth and retention** — `read_docs` exposes restoring points with diffs (VERIFIED as a capability), but how far back and for how long is **UNKNOWN**. Matters only if monday ever becomes more than a projection; it should not.
5. **Anthropic Skills and ZDR**: the platform doc states Agent Skills is *not* covered by zero-data-retention arrangements (VERIFIED). Irrelevant for Claude Code filesystem skills, relevant if any skill is ever uploaded through the API. Worth a line in the constitution before that happens.
6. **What is the right hit-rate threshold for demotion?** I proposed 60% demote / 40% retire over ≥10 firings from first principles, not evidence. After two months of `outcomes.csv` the thresholds should be refit against the actual distribution — and that refit is itself the first real test of whether this loop works.

---

### Sources

VERIFIED (opened 2026-09-06): [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory) · [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) · [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · monday.com first-party knowledge service and MCP tool schemas (`get_monday_knowledge`, `manage_agent_knowledge`, `read_docs`), citing [Get started with the monday AI Agent builder](https://support.monday.com/hc/en-us/articles/33347027353746-Get-started-with-the-monday-AI-Agent-builder)

REPORTED (search summaries; primary pages egress-blocked): [Agentic Context Engineering, ICLR 2026](https://arxiv.org/abs/2510.04618) · [Zep temporal knowledge graph](https://arxiv.org/abs/2501.13956) · [Zep](https://www.getzep.com/) · [Letta sleep-time agents](https://docs.letta.com/guides/agents/architectures/sleeptime/) · [Mem0 review and pricing](https://theaiagentindex.com/agents/mem0) · [LangMem SDK](https://www.langchain.com/blog/langmem-sdk-launch) · [Cognee memory agents](https://www.cognee.ai/blog/guides/most-popular-memory-agents-developers) · [Codex CLI persistent memory](https://codex.danielvaughan.com/2026/04/06/codex-cli-persistent-memory-mcp-servers/) · [AGENTS.md playbook 2026](https://www.codegateway.dev/en/blog/agents-md-playbook-2026) · [Codex CLI skills + AGENTS.md](https://www.agensi.io/learn/codex-cli-agents-md-complete-guide) · [Cowork memory](https://techcrunch.com/2026/08/25/claude-cowork-finally-remembers-what-you-told-the-app-in-chat/) · [Claude memory everywhere](https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it) · [Grok memory](https://blog.memoryplugin.com/how-grok-memory-works/) · [Grok Skills](https://theplanettools.ai/blog/xai-grok-skills-cross-conversation-persistence-document-generation-may-2026) · [Notion Lore shared agent memory](https://www.notion.com/blog/building-shared-memory-for-ai-agents-in-notion) · [DataDoe Hub](https://www.datadoe.com/hub) · [monday API rate limits](https://developer.monday.com/api-reference/docs/rate-limits) · [Supabase pgvector free tier 2026](https://aibizhub.io/articles/supabase-vector-free-tier-2026/) · [Why SQLite does not use git](https://sqlite.org/whynotgit.html) · [csvdb](https://github.com/jeff-gorelick/csvdb) · [Context rot](https://www.morphllm.com/context-rot) · [Context rot explained](https://redis.io/blog/context-rot/) · [Obsidian + MCP agent workflows](https://www.savemarkdown.co/blog/obsidian-ai-agent-mcp-markdown-workflow/)

UNKNOWN (tried, blocked by the egress proxy on 2026-09-06): agents.md spec text and its 2026 governance change; developers.openai.com Codex memory reference; docs.mem0.ai; getzep.com pricing page; docs.x.ai; developer.monday.com rate-limit page; arxiv.org abstracts (figures taken from search summaries).
