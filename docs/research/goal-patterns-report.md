# Goal & Strategy Patterns for an Autonomous AI Company of Departments
### A sourced survey for the Habib Distribution OS CEO agent, STRATEGY.md, and GOALS.md
Tags: **VERIFIED** = confirmed by direct primary-source retrieval or well-established published fact; **REPORTED** = based on search-engine snippet synthesis of secondary/tertiary sources (live fetch of primary source was blocked in this environment) or a single practitioner account not independently cross-checked; **UNKNOWN** = no reliable source found, my own synthesis/recommendation only.

---

## 1. Goal frameworks that translate into machine-checkable files

Four human management systems and one product-analytics framework are relevant, and each contributes a different piece of a machine-checkable schema — none of them was designed for machines, so the job is to extract their *shape*, not adopt any one wholesale.

**EOS (Traction) Rocks + Scorecard.** A Rock is one of 3–7 priorities a team commits to for a 90-day quarter; the weekly Scorecard is a short list of *leading*-indicator numbers, each with a named owner and a numeric goal, reviewed in under 15 minutes as a binary hit/miss (REPORTED — eosworldwide.com/blog/identifying-quarterly-rocks; eosworldwide.com/blog/how-to-hit-small-business-kpis-with-the-eos-scorecard). The contribution to a goal file: hard caps on concurrent objectives (3–7, not 30), and a Scorecard row shape of `{metric, owner, target, actual, status}` reviewed weekly rather than continuously.

**4DX (Four Disciplines of Execution).** Discipline 1 forces narrowing to one or two Wildly Important Goals (WIGs) instead of "whirlwind" busywork. Discipline 2 is the lead/lag distinction: lag measures (revenue, ACOS) are outcomes you can't act on directly; lead measures are the predictive, influenceable activities a team controls. Discipline 3 is a visible scoreboard carrying both lead and lag numbers so anyone can tell "winning or losing" at a glance. Discipline 4 is a short recurring commitment cadence — review last week's commitments, make new ones (REPORTED — perdoo.com/resources/online-guides/4dx; tojukaka.medium.com summary). Contribution: the lead/lag *tag* on every metric node, and the discipline of never diluting the WIG mid-quarter.

**Amazon's Weekly Business Review (WBR).** Amazon's leadership reviews 400–500 metrics in roughly an hour, every week, in an identical deck format so that anomalies are visible by pattern-break rather than by re-reading numbers. The central discipline is separating *output* metrics (results) from *input* metrics (controllable drivers) and focusing the actual discussion on inputs, because those are what next week's action can change (REPORTED — medium.com/@pjhab2020/the-amazon-weekly-business-review; medium.com/@fergusb/amazon-mechanism-weekly-business-review; nastengraph.substack.com "How to Measure Your Business the Amazon Way"). Contribution: the discipline that every scorecard row must be classified input/output, and that identical week-over-week structure (not narrative prose) is what makes drift visible to a human skimming fast.

**North Star Metric tree (Amplitude).** One output North Star Metric sits at the top; 3–5 input metrics, organized by dimensions such as breadth/depth/frequency, "ladder up" to it and are the metrics teams can actually move day to day. The NSM itself should not be directly actionable — only its inputs are (REPORTED — amplitude.com/blog/product-north-star-metric; amplitude.com/books/north-star). Contribution: the hierarchical decomposition itself — one lag output at the top, department-owned lead inputs below it, each input belonging to exactly one owning team.

**OKRs adapted for agents (2026 practitioner writing).** The emerging practitioner pattern explicitly used by 2026 agent-orchestration writers is: the Objective stays a natural-language outcome statement, but each Key Result is written as a *numeric, machine-scorable check* (e.g., "ACOS ≤ 25%") that an evaluator step or script can grade against live telemetry rather than requiring human judgment of "did we do this" (REPORTED — quasa.io/media/okrs-for-ai-bridging-human-management-practices-to-agent-orchestration). A June 2026 first-person account of building a multi-agent OKR-scoring system reported that the hard part was *not* the LLM scoring step — it was the underlying data-plumbing problem of getting trustworthy, comparable inputs so a KR score isn't silently wrong or gameable (REPORTED — heemeng.medium.com, "I Tried Building a Multi-Agent System to Score OKRs. The Hard Part Wasn't the Agents"). This is the single most important practical warning in this whole survey for Habib OS: the SP-API sync layer's data quality *is* the goal system's reliability ceiling — a perfectly designed GOALS.md schema fed by a stale or wrong `sales_daily` row produces a confidently wrong Key Result.

**Verdict.** No single framework maps cleanly onto a YAML file. The composite schema this survey recommends (built into GOALS.md below) borrows: OKR's `objective + numeric key results` shape, 4DX's `lead/lag` tag and one-WIG-per-quarter discipline, EOS's `owner + weekly Scorecard row + red/green status` cadence, WBR's `input vs output` split and identical-format-over-time principle, and North Star's hierarchical department-owned decomposition.

---

## 2. The manager-agent / planner-worker pattern

**Anthropic's "Building Effective Agents"** (Dec 2024, still the standard reference cited across 2026 practitioner sites) draws the key architectural line between fixed-path *workflows* — prompt chaining, routing, parallelization, **orchestrator-workers**, and **evaluator-optimizer** — and open-ended *agents* where the LLM directs its own steps. Orchestrator-workers is explicitly the pattern for tasks whose subtask breakdown can't be predicted ahead of time: a central LLM plans and delegates to workers, then synthesizes (VERIFIED as an existing, well-known Anthropic publication; live fetch of anthropic.com was blocked in this session, corroborated via github.com/anthropics/anthropic-cookbook and agentpatterns.ai). This is the architecture to use for a CEO agent decomposing a quarterly goal to department agents.

**Anthropic's multi-agent research system writeup** describes a production version of this: a lead/orchestrator agent plans and spins up 3–5 subagents in parallel, each with its own context window and toolset, then synthesizes with a separate verification pass. It beat single-agent Opus 4 by 90.2% on their internal eval, at roughly 15× the token cost — and Anthropic explicitly warns the pattern is a poor fit when subagents need to share context or have many interdependencies (REPORTED — claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them, corroborated by multiple secondary summaries). This directly validates Habib OS's existing "no agent-to-agent communication, share state only via Supabase" rule: three independent department agents fit this pattern; three agents that needed to negotiate live with each other would not.

**HumanLayer's 12-Factor Agents** is a principles guide (not a framework) organized around *ownership*: own the prompt, own the context, own the control flow, own the state, own how humans enter the loop. Its Factor 8 ("Own your control flow") argues explicitly that agents should be interruptible and resumable specifically *between tool selection and tool invocation* (VERIFIED — full text fetched from github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md). That is precisely the shape of Habib OS's existing `approval_requests` gate: the agent selects an action, the system pauses, a human or the Executor invokes it.

**Google's Agent Development Kit (ADK)** formalizes three composable workflow primitives — `SequentialAgent`, `ParallelAgent`, `LoopAgent` — under a coordinator/root agent in a parent/sub-agent tree, using "description-driven delegation" where the coordinator routes a task to whichever sub-agent's stated description matches (REPORTED — developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk). This maps directly onto a CEO agent routing "inventory risk" to the Inventory agent by description match rather than hard-coded logic.

**LangGraph's Plan-and-Execute pattern** separates a planner (one LLM call, produces a multi-step plan) from executor steps (can use a cheaper model, no re-consultation needed after each action) and a replanner node that consumes accumulated past-steps and either revises the remaining plan or ends (REPORTED — langchain.com/blog/planning-agents). The "replan on new evidence without restarting from scratch" discipline is the direct analogy for a CEO agent's weekly re-plan of monthly objectives, and pairs with the anti-thrash literature in Section 4.

**MetaGPT / ChatDev's SOP-based role design** ("Code = SOP(Team)") encodes standard operating procedures per role — PM, architect, engineer, QA — as fixed prompt sequences with defined inputs/outputs rather than free-form chat between agents, and the MetaGPT paper's own comparison found domain-specific SOP-constrained pipelines beat general-purpose agent loops on structured-output tasks (VERIFIED — arxiv.org/abs/2308.00352). This validates Habib OS's existing `BaseAgent` template-method design (fixed `fetch_data → analyze → process_response → write_observations` pipeline, strict JSON output schema) over a more open-ended agentic loop.

**2026 "one-person company" case studies** (solo founders running agent fleets past $1M ARR, e.g., Pieter Levels/PhotoAI at $1.8M ARR) converge on a common operating model: MCP as the standard tool-calling substrate, agents escalate only on edge cases, and the founder's real job becomes "train the agent on edge cases" and "step in when the agent escalates" (REPORTED — knowlee.ai/blog/one-person-ai-company-2026; getpancake.ai/blog/how-to-run-one-person-company-2026). This is management-by-exception as the *actual*, not aspirational, 2026 operating model for solo-operator AI companies.

**Andon Labs / Anthropic's Project Vend and Vending-Bench** are the most load-bearing evidence in this survey. Vending-Bench (arXiv 2502.15840, VERIFIED via direct arXiv listing) is a benchmark of long-horizon business coherence: agents manage a simulated vending machine over runs exceeding 20M tokens. Even strong models (Claude 3.5 Sonnet, o3-mini) show high run-to-run variance, and critically, "meltdown" collapses show **no correlation with context-window exhaustion** — degeneration is a coherence failure, not a memory-capacity failure. Project Vend Phase 1 (mid-2025) gave "Claudius" full pricing/ordering/customer-relations autonomy in a real office vending machine; it showed real competence (finding suppliers, adapting to requests) alongside severe failures — rejecting a $100 offer for $15 of inventory, selling below cost, fabricating payment records, and a roughly two-day episode of hallucinated identity and conversations (REPORTED — futurism.com/future-society/anthropic-ai-vending-machine, corroborated by multiple outlets). **Project Vend Phase 2** (2026) added a manager-level agent ("Seymour Cash") that set explicit numeric objectives (weekly revenue target, a hard floor of no under-50%-margin orders) and forced Claudius through a fixed lookup-cost → research-market-rate → set-price *procedure* instead of free-form pricing judgment. Result: unauthorized discounts dropped ~80%, giveaways halved. The reported conclusion: "constraint is not the enemy of performance... production-grade AI operations need layers: workers doing tasks and oversight layers catching mistakes" (REPORTED — anthropic.com/research/project-vend-2, live fetch blocked in this session but corroborated by enterprisedna.co and inkeep.com summaries). This is the strongest direct evidence for a three-layer design: CEO/manager agent sets objectives and required procedure → department agents execute within that procedure → human approves anything financial.

---

## 3. Proactive task creation the owner will actually act on

The AWS Well-Architected Framework's Operational Excellence pillar formalizes "escalation is encouraged" as a named practice (OPS03-BP03/OPS10-BP04): escalate early and often, with pre-defined escalation paths and pre-approved actions decided *before* the moment of crisis, so a human is pulled in only when a real threshold is crossed (VERIFIED — docs.aws.amazon.com/wellarchitected, official AWS documentation). A 2026 arXiv paper on agentic retail supply-chain monitoring ("Flowr") operationalizes this with an "Exception and Alert Agent" that scans the full replenishment lifecycle and surfaces structured alerts only when a risk condition is detected — the human is never shown a full backlog, only exceptions (VERIFIED — arxiv.org/pdf/2604.05987).

Among consumer productivity tools, the split between Motion/Reclaim (maximal automation — the algorithm reshuffles the human's calendar) and Sunsama (a small, deliberate human ritual — manually pick 3–5 top priorities, estimate effort not duration, hard-cap the daily list) is instructive: the tool that forces a small, capped, human-confirmed list is the one associated with sustained daily engagement rather than "set and ignore" (REPORTED — skedul.ai/blog/sunsama-vs-motion-vs-reclaim). For an AI-generated daily list this argues strongly for a hard cap (not an auto-growing backlog) and ranking (not a flat list).

The clearest and most sobering 2025–2026 evidence on *why owners ignore AI output* comes from Stack Overflow's 2025 Developer Survey and follow-on retrospectives: 84% of developers use AI tools, yet only ~3% report high trust in AI-generated output, and the dominant complaint is content that "looked right but didn't feel trustworthy" — thin evidence trails behind a claim (VERIFIED — stackoverflow.blog/2025/12/29, official Stack Overflow blog). 75% of people who distrust an AI answer go verify with a human anyway, which defeats the entire point of proactive task generation if evidence isn't attached (REPORTED, same source, secondary interpretation). The direct design implication: every generated task or decision must show its evidence (the underlying data point, the memory it draws on, the exact threshold crossed) and a numeric expected impact, or the human will not act on it — he will re-derive it himself, which is strictly worse than not automating at all.

---

## 4. Long-horizon reliability guardrails

Vending-Bench and Project Vend, taken together, are the most concrete sourced evidence base for what breaks agents over weeks, and what fixes it:

1. **Meltdown loops uncorrelated with context length** → the fix is not "give it a bigger context window," it's periodic hard checkpoints of working state and a bounded recovery procedure, because collapse is a coherence failure (REPORTED — Vending-Bench, arXiv 2502.15840; the-decoder.com).
2. **Hallucinated business facts** (fabricated payment records, invented conversations) → every claimed fact or outcome must trace to a queryable database row or memory id; an agent should never be allowed to assert a business fact "from memory" alone without a citation back to Supabase or Mem0 (REPORTED, derived from Project Vend Phase 1 failure catalog).
3. **Irrational pricing / rejecting profitable trades / selling below cost** → hard numeric floors and ceilings enforced in code, not merely in a prompt — exactly Habib OS's existing L1 rules pattern, and exactly what Project Vend Phase 2 added (REPORTED — Project Vend Phase 2 coverage).
4. **The single most quotable, sourced lesson**: "constraint is not the enemy of performance... production-grade AI operations need layers: workers doing tasks and oversight layers catching mistakes," and adding a manager layer plus a forced procedure cut bad pricing behavior by ~80% (REPORTED — Project Vend Phase 2 coverage, multiple outlets).

Anthropic's evaluator-optimizer pattern (a generator produces output, a separate evaluator/critic call grades it against explicit written criteria and returns PASS/FAIL plus structured feedback, looping to a cap) is the right shape for a periodic critic pass — and Anthropic's evals engineering guide adds that each rubric dimension should be graded by an *isolated* judge call rather than one judge scoring everything, to avoid halo effects (REPORTED — anthropic.com/engineering/demystifying-evals-for-ai-agents, live fetch blocked, corroborated via anthropic-cookbook on GitHub, VERIFIED). Applied to Habib OS: a critic step checks each department agent's claimed observations against the underlying Supabase numbers before they enter Mem0, and a weekly critic pass checks whether last week's approved actions produced the predicted outcome (outcome logging + prediction scoring).

No single named source gives a verbatim "definition of done" pattern for business-agent goal tracking; this survey's UNKNOWN/derived recommendation, consistent with 4DX's scoreboard discipline and WBR's "commit to specific next actions with owners and dates," is that a task cannot be closed by the agent's own say-so — only by matching a human-authored, pre-committed completion condition captured at task-creation time.

**Concrete guardrail set (synthesized, REPORTED/derived):**
- Every observation/decision links to a `source_run_id` and an underlying table row or Mem0 memory id — no bare assertions.
- A weekly reflection job scores whether last week's approved actions matched their predicted outcome against real Supabase data, building a running prediction-accuracy score per agent/domain.
- Every plan/objective carries a `created_date` and staleness rule: unreviewed past its cadence, it is auto-flagged stale and demoted, never silently carried forward.
- Hard numeric floors/ceilings (margin floor, price bounds, budget caps) are enforced in code the agent cannot override via prompt.
- Every task/objective has a human-authored `definition_of_done` string at creation time; only an exact match (checked by a critic step or a human) can close it.

---

## 5. Metric tree for a 15-SKU Amazon brand

Sourced lead/lag benchmarks: Conversion Rate is repeatedly named the top listing-health lead indicator (9–15% for established products; falling CVR with stable traffic isolates to a listing problem, falling traffic with stable CVR isolates to a visibility/ad problem) (REPORTED — canopymanagement.com, financialmodelslab.com). CTR benchmark ~0.3–0.5%, isolating to image/title/price/review-count issues specifically (REPORTED, same sources). ACOS benchmark 15–25% for established products, 30–45% acceptable during launch — already mirrored in Habib OS's L1 rules (REPORTED — sellerlabs.com). TACoS (= total ad spend ÷ total sales, ad + organic; healthy range ~5–10% for mature private label) is the better lag-side check on whether advertising is still buying incremental growth versus harvesting organic demand, since ACOS improves mechanically as a keyword matures even while total ad dependence holds flat (VERIFIED — perpetua.io, daniks.ai, formula confirmed across multiple independent seller-tool sources). Sell-Through Rate (units sold/shipped over trailing 90 days ÷ average FBA units held; target >60%/month) and Amazon's own Inventory Performance Index (IPI, 0–1000, factoring velocity/excess/storage-fee exposure) are the two clearest inventory-side lead measures (REPORTED — canopymanagement.com, sarasanalytics.com).

**Proposed metric tree:**

- **North Star (lag, monthly):** Net Profit, CAD-normalized, across CA+US — chosen because margin erosion, ACOS creep, and stockouts all eventually surface here, and (per North Star discipline) it cannot be moved directly, only via department inputs (UNKNOWN/derived — no source gives this exact brand's NSM, this is this survey's application of the Amplitude framework).
- **Inventory dept lead measures:** days-of-supply per SKU (14d warning/7d critical, existing L1 rule), Sell-Through Rate (>60% target), IPI score, count of SKUs with an open replenishment gap.
- **PPC dept lead measures:** ACOS per campaign (15–25% band), TACoS (5–10% band), wasted-spend $ (spend with zero conversions in 14+ days), CTR (0.3–0.5% band).
- **Competitor/Listing dept lead measures:** CVR per SKU (9–15% band), Buy Box win %, count of open competitor alerts, review-rating trend.

**Weekly scorecard columns** (composite of EOS Scorecard + WBR input/output split + 4DX lead/lag tag): `Metric | Owner (agent/dept) | Type (lead/lag) | Target | This Week | Last Week | 4-wk avg | Trend | Status (green/yellow/red) | Note + action owner/date`.

---

## 6. Deliverables (templates below are ready to copy into the repo)

### (a) STRATEGY.md — section outline
```
# STRATEGY.md
## 1. Mission (one sentence, rarely changes)
## 2. North Star Metric (the one lag number; how it's computed; who owns the source data)
## 3. Current Strategic Posture (2-4 paragraphs: market position, moat, biggest risk, biggest bet — rewritten quarterly)
## 4. Department Charters (one paragraph each: Inventory, PPC, Competitor/Listing — mandate + explicit boundaries of what they may NOT decide)
## 5. Non-Negotiables (L1 Rules — margin floors, approval gate, seasonal multipliers — pointer to core/config.py, not duplicated)
## 6. This Quarter's Wildly Important Goal (max 1-2, 4DX-style — pointer to GOALS.md current quarter)
## 7. Explicitly Deferred (things we are NOT doing yet and the trigger condition that would change that — mirrors CLAUDE.md Section 16.1)
## 8. Revision Log (date, what changed, why — append-only)
```

### (b) GOALS.md — YAML front matter schema + example quarter
```yaml
---
quarter: "2026-Q4"
status: active
north_star:
  metric: net_profit_cad_normalized
  target: 42000
  baseline: 31000
  as_of: 2026-09-01
objectives:
  - id: obj-2026q4-01
    title: "Protect Canada margin through Q4 seasonal peak"
    type: lag
    owner: ceo_agent
    department: inventory
    key_results:
      - id: kr-01a
        metric: fba_margin_pct_ca
        target: ">=18"
        baseline: 15.4
        current: 16.1
        as_of: 2026-09-01
      - id: kr-01b
        metric: stockout_days_q4
        target: "<=0"
        baseline: 6
        current: 6
        as_of: 2026-09-01
    definition_of_done: "18%+ blended CA margin sustained for 4 consecutive weeks through Dec 31, verified against profit_daily"
    review_cadence: weekly
    status: on_track
    last_reviewed: 2026-09-01
  - id: obj-2026q4-02
    title: "Reach US-launch readiness"
    type: lag
    owner: ceo_agent
    department: competitor_listing
    key_results:
      - id: kr-02a
        metric: us_listings_live
        target: 15
        baseline: 0
        current: 3
      - id: kr-02b
        metric: us_ppc_acos_first_30d
        target: "<=40"
        baseline: null
        current: null
    definition_of_done: "15/15 SKUs live on ATVPDKIKX0DER with Buy Box, first 30-day blended ACOS <=40%"
    review_cadence: weekly
    status: at_risk
    last_reviewed: 2026-09-01
  - id: obj-2026q4-03
    title: "Maintain >=21-day stock cover on all core SKUs"
    type: lead
    owner: inventory_agent
    department: inventory
    key_results:
      - id: kr-03a
        metric: skus_below_14d_supply
        target: 0
        current: 2
    definition_of_done: "0 SKUs under 14-day supply for 2 consecutive weekly snapshots"
    review_cadence: weekly
    status: on_track
    last_reviewed: 2026-09-01
anti_thrash:
  quarterly_objectives_locked_until: "2026-12-01"
  override_triggers: ["marketplace_suspension", "stockout_crisis_gt_3_skus"]
---

# Q4 2026 Goals — Habib Distribution

## Why these three objectives
[narrative — filled by CEO agent monthly, human-edited]

## Weekly Scorecard
| Metric | Owner | Type | Target | This Wk | Last Wk | 4-wk avg | Trend | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| fba_margin_pct_ca | inventory_agent | lag | >=18% | 16.1% | 15.8% | 15.6% | up | yellow | Ramadan buffer stock landing Oct 3 |
| acos_ca_baklava | ppc_agent | lead | 15-25% | 22% | 24% | 23% | down | green | |
| skus_below_14d_supply | inventory_agent | lead | 0 | 2 | 3 | 3 | down | yellow | SKU-017, SKU-022 |
```

### (c) CEO agent charter — outline
```
# CEO Agent Charter

## Inputs (read-only)
- STRATEGY.md, GOALS.md (current + prior quarter)
- Supabase: agent_runs, decision_log, profit_daily, sales_daily (last 90d)
- Mem0: patterns + playbooks (all domains), last 4 weeks of observations

## Weekly loop (runs after all 3 department agents complete, before daily brief)
1. Read each department's latest observations + this week's scorecard numbers.
2. Score each Key Result against its target (evaluator step, isolated per KR).
3. Flag 2-consecutive-week same-direction breaches only (anti-thrash rule).
4. Write/update the Weekly Scorecard table in GOALS.md (append, never silently overwrite history).
5. Generate the ranked "Decisions & Tasks for Rami" list (max 5 items) — see (d).
6. Log a decision_log entry for any objective status change (on_track/at_risk/off_track).

## Monthly loop (1st of month, after monthly_review consolidation)
1. Re-read promoted playbooks and pattern decay flags from consolidation.
2. Propose (never silently apply) revisions to monthly milestones under active quarterly objectives — a scoped "repair," not a full rewrite.
3. Write a one-paragraph strategic-posture update to STRATEGY.md Section 3 for human review.
4. If any objective's definition_of_done is met, mark it done and log evidence.

## What it MAY do
- Read all Supabase/Mem0 data.
- Write to GOALS.md, decision_log, notifications.
- Re-rank or re-scope WEEKLY tasks freely.
- Propose (not apply) monthly milestone edits and STRATEGY.md updates.

## What it MAY NOT do
- Create, close, or reword a quarterly objective outside the quarterly boundary, except via a named override_trigger in GOALS.md.
- Write to approval_requests with a payload it did not receive from a department agent (no financial invention).
- Mark any objective's definition_of_done met without a citation to a Supabase row/query.
- Silently overwrite scorecard history (writes are append-only rows, not in-place edits).

## How it writes tasks for the human
Ranked list, hard-capped at 5 items/day, HTML-formatted for Telegram, each item: evidence pointer, numeric expected impact, deadline, one-tap approve/reject where financial.
```

### (d) "Decisions & Tasks for Rami" — daily section format
```
🧭 DECISIONS & TASKS — Sep 5, 2026 (5 items, ranked)

1. 🔴 APPROVE: Restock SKU-017 Baklava — 200 units
   Evidence: 6.2 days supply (profit_daily + inventory_snapshots, run_20260905_0530)
   Impact: prevents ~$1,100 lost revenue over projected 9-day gap
   Deadline: Sep 6, 10:00 AM (ships Sep 8 to clear FBA lead time)
   [Approve] [Reject] [Dashboard]

2. 🟡 DECIDE: Pause keyword "middle eastern sweets" (Baklava CA)
   Evidence: ACOS 38% vs 24% campaign avg, 0 conversions in 16 days (ppc_keyword_stats_daily)
   Impact: saves ~$14/day spend, no sales lost (14-day zero-conversion window)
   Deadline: none — recommend acting this week
   [Approve] [Reject] [Dashboard]

3. 🟢 FYI: Competitor B0xxx dropped tahini price 12% — no action needed, margin still >18% at current price
```
Rule: nothing appears below severity/exception threshold; list is never empty-padded to look busy; if there is truly nothing, it says so in one line.

### (e) Anti-thrash rule set
1. Quarterly objectives are locked for the quarter; they can be replaced only at the quarter boundary, or via a named `override_trigger` explicitly listed in GOALS.md front matter (e.g., marketplace suspension, stockout crisis).
2. Monthly milestones may be edited mid-month only as a scoped *repair* (diff naming the exact line changed and why) — never a silent full rewrite (plan-repair-over-replanning, ICAPS 2006).
3. Weekly tasks are the only layer regenerated freely every cycle.
4. A metric flipping status for a single week does not trigger any plan change; only 2 consecutive weeks of the same-direction breach does.
5. Every plan-change event is logged to `decision_log` with the specific KR/observation that justified it — a plan can never change for a reason that isn't traceable to a row in Supabase or Mem0.
6. The CEO agent may *propose* a quarterly-objective change at any time (goes into `notifications` for human review) but may never *apply* one outside the rules above.

---

## Sources cited
- eosworldwide.com/blog/identifying-quarterly-rocks · eosworldwide.com/blog/how-to-hit-small-business-kpis-with-the-eos-scorecard · tability.io/odt/articles/eos-rocks
- perdoo.com/resources/online-guides/4dx · tojukaka.medium.com/summary-of-the-four-disciplines-of-execution-4dx
- medium.com/@pjhab2020/the-amazon-weekly-business-review · medium.com/@fergusb/amazon-mechanism-weekly-business-review · nastengraph.substack.com "How to Measure Your Business the Amazon Way" · dataanalysis.substack.com/p/how-amazon-runs-a-weekly-business-review
- amplitude.com/blog/product-north-star-metric · amplitude.com/books/north-star
- quasa.io/media/okrs-for-ai-bridging-human-management-practices-to-agent-orchestration · heemeng.medium.com "I Tried Building a Multi-Agent System to Score OKRs"
- anthropic.com/engineering/building-effective-agents · github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/evaluator_optimizer.ipynb · anthropic.com/engineering/demystifying-evals-for-ai-agents
- claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them · theaiengineer.substack.com/p/how-anthropic-built-multi-agent-deep
- github.com/humanlayer/12-factor-agents (Factor 8 fetched directly)
- developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk
- langchain.com/blog/planning-agents
- arxiv.org/abs/2308.00352 (MetaGPT)
- knowlee.ai/blog/one-person-ai-company-2026 · getpancake.ai/blog/how-to-run-one-person-company-2026
- arxiv.org/abs/2502.15840 (Vending-Bench) · andonlabs.com/evals/vending-bench · futurism.com/future-society/anthropic-ai-vending-machine · anthropic.com/research/project-vend-2 · enterprisedna.co/resources/news/anthropic-project-vend-2 · inkeep.com/blog/anthropics-ai-shopkeeper-experiment-reveals-agent-limitations
- docs.aws.amazon.com/wellarchitected (OPS03-BP03, OPS10-BP04) · arxiv.org/pdf/2604.05987 (Flowr)
- skedul.ai/blog/sunsama-vs-motion-vs-reclaim · morgen.so/blog-posts/best-ai-planning-assistants
- stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai · coderabbit.ai/blog/2025-was-the-year-of-ai-speed-2026-will-be-the-year-of-ai-quality
- cdn.aaai.org/ICAPS/2006/ICAPS06-022.pdf (Plan Stability) · apxml.com iterative-planning-re-planning-prompts
- canopymanagement.com/metrics-every-amazon-seller-should-track · financialmodelslab.com/blogs/kpi-metrics/fba · sellerlabs.com/knowledge-base/amazon-metrics-that-actually-matter · perpetua.io/blog-amazon-tacos · daniks.ai/blog/what-is-amazon-tacos-complete-guide · sarasanalytics.com/blog/amazon-kpi
