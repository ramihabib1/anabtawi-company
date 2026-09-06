# 07 — Approvals, coordination, and the money path

Research date: 2026-09-06. Author: research agent. Audience: Rami + the Chief of Staff / CEO department.

---

## 0. Verification status — read this before you trust anything below

This session's egress proxy blocked **every** domain I tried to open directly except `github.com`. Blocked and confirmed blocked today: `sellercentral.amazon.com`, `developer-docs.amazon.com`, `advertising.amazon.com`, `docs.anthropic.com`, `langchain-ai.github.io`, `en.wikipedia.org`, `ppc.land`, `ecommercebytes.com`, `sellersprite.com`, `developer.intuit.com`. So:

| Tag | What it means here | How much of this report |
|---|---|---|
| VERIFIED | I opened the primary source today and read it | ~5% (two GitHub READMEs) |
| REPORTED | Web-search index summaries of secondary sources, or vendor/press pages I could not open | ~75% |
| UNKNOWN | Could not confirm; I say what I tried | ~20% |

**The Amazon BSA Section 19 text is NOT VERIFIED.** I could not open `sellercentral.amazon.com/help/hub/reference/external/G1791` (the BSA) or the forum announcement. What follows is the consistent account given by eight independent secondary sources (law firms, trade press, seller-tool vendors) indexed today. That consistency is meaningful but it is not the policy text. **Before this design goes live, Rami must open the BSA in Seller Central himself, copy Section 19 verbatim into `docs/policy/amazon-agent-policy.md`, and date-stamp it.** Every guardrail number below that claims an Amazon origin must be re-checked against that copy. Treat this report's Amazon numbers as a design hypothesis until then.

---

## 1. Amazon's rules for agents (REPORTED, needs primary verification)

### 1.1 What Section 19 says, per the secondary record

- Section 19 ("Agent Policy") was added to the Amazon Services Business Solutions Agreement, **announced 2026-02-17, effective 2026-03-04**, with a 90-day transition ending early June 2026; enforcement is now active. (REPORTED — [EcomCrew](https://www.ecomcrew.com/amazon-bans-ai-agents-seller-platform/), [MyAmazonGuy](https://myamazonguy.com/news/amazon-services-business-solutions-agreement/), [DAM Law Firm](https://damlawfirm.com/blog/amazon-bsa-ai-agent-policy-update/))
- "Agent" is defined broadly: automated software, AI systems or bots that access Amazon Services — repricers, PPC tools, browser extensions, fulfilment scripts. One source gives Amazon's definition of an **"AI seller agent" as any system making or executing decisions on a seller account without real-time human input for each action** — which is exactly what this company is. (REPORTED — [Digital Applied](https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules))
- Three headline obligations: **(a) self-identify as automated**, **(b) comply with the Agent Policy at all times**, **(c) cease access immediately on Amazon's request**. (REPORTED — [SellerSprite](https://www.sellersprite.com/en/blog/amazon-bsa-agent-policy-2026), [Profasee](https://profasee.com/blog/amazon-ai-agent-policy-what-sellers-need-to-know/))
- **Browser automation and Seller Central scraping are explicitly prohibited**, including homegrown scripts and commercial tools with an AI wrapper. Every automated seller action must be traceable to a **registered SP-API application with an application ID linked to a verified developer account**. (REPORTED — same sources)
- **Audit logging**: a retrievable log of every action — timestamp, action type, input data, output — retained **at least 12 months**, producible on Amazon's request. (REPORTED — [Digital Applied](https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules), [SellerShorts](https://sellershorts.com/resources/ai-for-amazon-sellers/amazon-ai-agent-policy))

### 1.2 Amazon's own floors for automated action

| Floor | Threshold | Requirement | Tag |
|---|---|---|---|
| Automated price change | >20% on an ASIN within 24 hours | documented human authorization in the audit trail | REPORTED ([amazonsellers.attorney](http://www.amazonsellers.attorney/blog/the-20-rule-avoiding-suspensions-under-amazons-2026-ai-agent-policy)) |
| Bulk listing create/modify | ≥500 ASINs in one batch | documented human authorization | REPORTED (same) |
| Account-level configuration changes | any | documented human authorization | REPORTED (same) |

`AGENTS.md` §5 already states these two floors correctly. Keep them; verify the wording.

### 1.3 Amazon's own agentic products

- **Seller Assistant** became agentic in Sept 2025; free to US 3P sellers; runs on Bedrock (Nova + Claude); monitors inventory/account health, flags compliance, and can plan multi-step tasks. Roadmap includes restock orders and price adjustments, **but the human stays in the approval loop today**. Canvas (visual dashboards) shipped for US/UK. (REPORTED — [SellerSprite](https://www.sellersprite.com/en/blog/amazon-ai-seller-assistant-agentic-2026), [Nova Analytics](https://novadata.io/resources/news/amazon-seller-assistant-agentic-ai))
- **Amazon Ads MCP Server**: closed beta Nov 2025 → **open beta 2026-02-02**, global to Ads partners with active API credentials; 50+ tools across Sponsored Products/Brands/Display, DSP, AMC — campaign creation, reporting, bid management, account settings, billing views; works with Claude, ChatGPT, Bedrock, AgentCore. (REPORTED — [MediaPost](https://www.mediapost.com/publications/article/412481/amazon-ads-mcp-server-moves-to-open-beta.html), [AdExchanger](https://www.adexchanger.com/marketers/amazon-ads-opens-a-beta-test-for-its-new-mcp-server/), [Digiday](https://digiday.com/media-buying/ad-tech-briefing-amazon-launches-mcp-server-for-agent-driven-advertising/))
- **Ads Agent**: announced unBoxed 2025, beta through 2026, in the Ads console; natural-language campaign creation, bid optimisation, Creative Agent. Beta requested via Seller Central → Advertising → Beta Programs, priority to $5k+/month ad spend. No fee. (REPORTED — [Feedvisor](https://feedvisor.com/university/what-is-amazon-ads-agent/), [SellerApp](https://www.sellerapp.com/blog/amazon-ads-agent/)) — Anabtawi at CAD 8-10k/month revenue is unlikely to hit the $5k/month ad-spend priority bar; treat as "watch, not plan".
- **SP-API MCP** — important correction to a common misreading. Amazon ships `@amazon-sp-api-release/sp-api-dev-mcp` from `amzn/selling-partner-api-samples`, containing **two MCP servers: an "SP-API Dev Assistant" and an "SP-API Workflow Builder"**. (VERIFIED — I opened [the README](https://github.com/amzn/selling-partner-api-samples/blob/main/README.md) today.) This is **developer tooling** — doc search, endpoint browsing, code generation, live calls with auth handled for the developer — not a production write path for an unattended business. It is a good thing to give Claude Code while *building* the runner; it is not the runner. Third-party SP-API MCP servers exist on GitHub/Glama/Pipedream but none is Amazon-official (REPORTED).

---

## 2. The write path for a solo seller

### 2.1 Three candidate write paths

| Path | What it can write | Compliance posture | Effort | Verdict |
|---|---|---|---|---|
| **DataDoe Actions** (hosted) | reprice SKUs, fix listings, negative keywords, adjust PPC, cancel orders, confirm shipments; per-type controls, `dryRun` validation, per-write approval gate, full audit log | DataDoe holds a registered SP-API/Ads app; actions are traceable to it. Rami never registers as a developer. | ~0 (already subscribed, $97/mo) | **Start here.** (REPORTED — [DataDoe platform](https://www.datadoe.com/platform), [pricing](https://www.datadoe.com/pricing)) |
| **Own private SP-API app** (self-authorized) | anything the granted roles allow | Rami is the verified developer; his own app ID on every call; maximum control and maximum obligation | weeks: developer profile, roles, use cases, security controls, DPP acceptance, Amazon case review | **Register in parallel, use later.** |
| **Official Amazon Ads MCP** | ads only: bids, budgets, negatives, campaigns | Amazon's own server, Amazon's own auth | days once Ads API credentials approved | **Already the T1 path in `AGENTS.md`. Correct.** |

**Recommendation:** DataDoe Actions is the write path for v1 of every non-ads class, and the Amazon Ads MCP is the write path for ads. Register the private SP-API app now anyway, because (a) it is the only path that survives DataDoe disappearing, (b) Amazon's traceability requirement is cleanest when the app ID is yours, and (c) the US launch in Jan 2027 will want FBA Inbound v2024-03-20 directly.

### 2.2 SP-API private developer registration — what's involved

Complete the developer registration form; under Data Access select **"Private Developer: I build application(s) that integrate my own company with Amazon Services APIs"**; select roles; enter use cases and **security controls**; accept the Solution Provider Portal Agreement, Acceptable Use Policy and **Data Protection Policy**; register. Amazon evaluates and opens a case — **respond within five days or the case closes**. Private applications are **self-authorized in draft status**; there is no reason to publish. (REPORTED — [SP-API registration overview](https://developer-docs.amazon.com/sp-api/docs/sp-api-registration-overview), [Authorize Private Applications](https://developer-docs.amazon.com/sp-api/docs/self-authorization), [Register as a Private SP-API Developer](https://developer-docs.amazon.com/sp-api/docs/register-as-a-private-developer)) **Timeline to approval: UNKNOWN** — no source I could reach gives a number; plan for weeks, not days, and start before the US launch critical path.

**Roles and PII.** Restricted operations need a general role *plus* a restricted role (Direct-to-Consumer Shipping, Tax Invoicing, Tax Remittance). Restricted access triggers a two-phase review — business verification, then a data-security assessment. The Data Protection Policy for PII handlers requires penetration tests every 365 days, vulnerability scans every 180 days plus continuous monitoring, PII deletion within 30 days of shipment absent a legal basis, and 24-hour incident notification to Amazon. (REPORTED — [role mappings](https://developer-docs.amazon.com/sp-api/docs/role-mappings), [Cybersecify on the DPP](https://cybersecify.com/blog/amazon-sp-api-data-protection-policy-pentest/), [DataDoe on restricted PII](https://www.datadoe.com/blog-posts/amazon-sp-api-restricted-pii))

**Design consequence: do not request any restricted PII role.** A solo operator running a Mac mini cannot honestly attest to annual pen tests and continuous monitoring. Buyer-address data is not needed for anything in the charter. **Pricing, inventory, listings, feeds, reports, notifications, FBA inbound are all non-restricted.** Messaging (buyer messages) is the one place PII pressure appears — keep buyer messaging at T2 with Rami sending, or route it through DataDoe/Seller Central rather than holding a PII role.

### 2.3 The writes that matter, and their shape

| Capability | API | Notes | Tag |
|---|---|---|---|
| Price / quantity | Listings Items v2021-08-01 `PATCH` | only top-level attributes patchable, no nested; quantity via merge-patch on `fulfillmentAvailability`; ~5 req/s burst, 5/s (some sources say 0.5/s sustained) | REPORTED ([patchListingsItem](https://developer-docs.amazon.com/sp-api/reference/patchlistingsitem), [use-case guide](https://spapi.vip/en/use-case/listings-items-api-v2021-08-01-use-case-guide.html)) |
| Bulk changes | Feeds API | the right tool above a few dozen SKUs; but see the ≥500-ASIN human-authorization floor | REPORTED |
| FBA shipments | Fulfillment Inbound v2024-03-20 | replaces `createInboundShipmentPlan`; **all POSTs are asynchronous — you must poll `getInboundOperationStatus`**; 1,500 SKUs/plan; interchangeable with Send to Amazon | REPORTED ([use-case guide](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-use-case-guide)) |
| Events | Notifications API | push instead of poll for listing/offer/inventory changes | REPORTED |
| Buyer messages | Messaging API | PII-adjacent; keep at T2 | REPORTED |
| Reports | Reports API | own burst quotas, retry-after | REPORTED |

**Rate limits are not uniform.** They vary by seller tier, marketplace, time of day and endpoint; some endpoints carry daily caps regardless of pacing; `x-amzn-RateLimit-Limit` returns the applied plan. (REPORTED — [Nova SP-API rate limit guide](https://novadata.io/resources/blog/amazon-sp-api-rate-limits-guide)) The runner must read that header and back off, not hard-code a number.

### 2.4 Automate Pricing as a bounded-autonomy primitive

Amazon's own **Automate Pricing** is free, lives in Seller Central under Pricing → Automate Pricing, adjusts prices in near real time against predefined or custom rules, requires a **minimum price** and supports an optional **maximum price** per SKU, applies per-SKU or in bulk, and its price changes **do not count toward the daily price-update allotment**. It is also manageable via SP-API. (REPORTED — [sell.amazon.com/tools/automate-pricing](https://sell.amazon.com/tools/automate-pricing), [Automate Pricing rules](https://sell.amazon.com/blog/automate-pricing-rules), [SP-API automated pricing rules](https://developer-docs.amazon.com/sp-api/docs/manage-automated-pricing-rules))

**This is the single best piece of leverage in the whole design.** It is a first-party, Amazon-operated, band-bounded autonomy primitive: Rami approves a *band* once (T2 on the band), and Amazon moves prices inside it forever without any agent taking a write action, without any Section 19 exposure, and without consuming the price-change allotment. The `products/<sku>.md` "Automated Pricing band" in `AGENTS.md` §4 should be implemented literally as an Automate Pricing rule, not as an agent-enforced band. Agents then only ever propose **band changes** (rare, T2) rather than **price changes** (frequent, T2) — which collapses the highest-volume approval class to near zero.

---

## 3. Human-in-the-loop: the patterns worth stealing

**The core finding that should shape everything:** Anthropic's own research reports that **users approve ~93% of permission prompts** — approval fatigue makes per-action confirmation behaviourally unreliable as a sole safety mechanism, and the correct response is to define *boundaries* the agent works freely inside rather than adding more prompts. (REPORTED — [Anthropic, measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy), [Backslash on the shared responsibility model](https://www.backslash.security/blog/anthropics-shared-responsibility-security-model-for-ai-agents)) Anthropic's shared-responsibility model splits agent security into Model / Harness / Tools / Environment, with **three of the four layers the deployer's responsibility**.

Applied here: **Rami will rubber-stamp if the daily brief has ten approvals in it.** The design must aim for **≤3 approvals a day**, each one genuinely consequential, and push everything else into bands, budgets and blocked actions. A cap of five ranked items already exists in `DECISION-CONTROL-PLANE.md`; make it a hard cap on *approvals*, not just brief items.

Patterns from the frameworks, all convergent:

- **OpenAI Agents SDK**: `needs_approval` on tools; the run pauses and returns `interruptions` (`ToolApprovalItem` with agent name, tool name, arguments); state serialises with `state.to_json()` and restores with `RunState.from_json()` so an approval can take a day; sticky `always_approve=True` survives serialisation. (REPORTED — [HITL guide](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/), [guardrails & approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals))
- **LangGraph**: `interrupt()` inside a node checkpoints and freezes the run; `Command(resume=...)` on the same `thread_id` continues from the exact checkpoint; a durable checkpointer is what makes a day-long pause possible. (REPORTED — [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts))
- **Temporal**: approvals as Signals, durable timers for expiry, workflows consume no compute while waiting; **signals may be duplicated, so signal handlers must be idempotent**; activities carry idempotency keys built from workflow ID + step ID. (REPORTED — [Temporal HITL approvals](https://temporal.io/blog/human-in-the-loop-approvals), [reliable document approvals](https://docs.temporal.io/guides/reliable-document-approvals))
- **Fintech / maker-checker**: AI proposes, human confirms, **and the server re-validates independently** — the re-validation is the part most designs skip. Six standard spend guardrails: spending limits, velocity caps, allowlists, approval workflows, policy-engine enforcement, virtual-card scoping. Guardrails stack weakest→strongest: prompt instructions < application checks < card-level controls < ledger-enforced balances. Maturity ladder: **Ask → Execute → Autonomous**. FINRA's 2026 report treats AI agents as a distinct supervisory category and names guardrails as a required supervisory consideration. (REPORTED — [Formance](https://www.formance.com/blog/industry-analysis/ai-agent-spending-limits), [Fystack](https://fystack.io/blog/6-guardrails-to-limit-ai-agent-spending-on-payment-rails), [ATXP](https://atxp.ai/blog/ai-agents-fintech/))
- **Idempotency**: client-generated UUIDv4 key; server stores the status code and body of the first request for that key and replays it for retries **including 500s**; parameters are compared and a mismatch errors; Stripe prunes keys at ~24h. Effect: at-least-once delivery + duplicate collapse = effectively-once. (REPORTED — [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests), [Stripe blog](https://stripe.com/blog/idempotency))
- **Hash-chained ledger**: append-only JSONL; each row carries a monotonic sequence number, `prev_hash`, and `hash = SHA-256(prev_hash ‖ seq ‖ canonical-JSON(row))`. Tamper-*evidence*, not immutability — the anchor and the write path must be protected, so **periodically anchor a checkpoint in a separate trust domain**. (REPORTED — [AgentPatterns](https://agentpatterns.ai/security/cryptographic-governance-audit-trail/), [C# Corner](https://www.c-sharpcorner.com/article/building-tamper-evident-audit-logs-for-ai-agent-actions/)) Here the second trust domain is free: **git commits are already signed-ish and pushed to GitHub**, so the daily commit hash *is* the external anchor. Record the previous day's head commit SHA in the first ledger row of each day.
- **Secrets**: 1Password CLI `op run` resolves `op://vault/item/field` references into a temporary sub-shell's environment for the life of the process only; non-interactive auth via `OP_SERVICE_ACCOUNT_TOKEN`. MCP servers over stdio inherit only a limited env subset, so secrets must be passed explicitly via the `env` block — which is exactly the `${NAME}` convention already in `docs/MCP-SERVERS.md`. (REPORTED — [1Password: load secrets into the environment](https://developer.1password.com/docs/cli/secrets-environment-variables))

---

## 4. The hands runner on the Mac mini

**Design rule: the reasoning model never holds a write credential.** Department agents get read-only tools (DataDoe read key, Keepa, QBO with `QUICKBOOKS_DISABLE_WRITE/UPDATE/DELETE=true`). The only process on the machine that can write to Amazon or QuickBooks is a **deterministic Python script with no LLM in it**, launched by `launchd`, wrapped in `op run` so credentials exist only in that process's memory for the seconds it runs.

```
launchd (every 5 min)
  └─ op run -- python3 hands/runner.py
       1. git pull
       2. scan approvals/approved/*.md
       3. for each: re-validate (schema, expiry, guardrails, budget, lock, duplicate)
       4. dry-run via the tool's own dryRun / preview
       5. execute with idempotency_key
       6. read-back verify
       7. append hash-chained line to ledger/actions.jsonl
       8. move file to approvals/executed/, set ledger_ref
       9. git commit && push
      10. (optional) push status back to monday + Telegram
```

Note step 3: **the runner re-validates independently of the agent that proposed and of Rami who approved.** This is the maker-checker "server re-validates" leg. It must fail closed — an approval whose numbers no longer hold at execution time is re-queued, never executed.

### 4.1 Trigger mechanism — the comparison you asked for

| Option | Inbound exposure | Latency | Failure mode | Cost / tier | Verdict |
|---|---|---|---|---|---|
| **Poll monday GraphQL every 5 min** | none | ≤5 min | poll fails → nothing happens, next poll retries; entirely self-healing | ~288 calls/day of the Pro plan's 10,000/day (REPORTED — [monday plans](https://pipeline.zoominfo.com/sales/monday-com-api)) | **Recommended** |
| monday webhook → your endpoint | requires a public HTTPS endpoint | seconds | missed delivery = missed approval unless you also poll; webhooks are **per-board**, a new board inherits nothing | needs a tunnel | reject |
| monday automation → webhook action (Pro) | same | seconds | same, plus consumes the plan's automation action allowance | Pro | reject |
| Poll the git repo only (no monday call at all) | none | ≤5 min | simplest possible; Rami approves by editing a file / merging | free | **fallback** |
| Cloudflare Tunnel / Tailscale Funnel / ngrok | opens a path into the home LAN | seconds | one more always-on daemon, one more auth surface, one more thing to babysit | free tiers exist (REPORTED — [comparison](https://insights.nomadlab.cc/blog/2026/04/tailscale-vs-cloudflare-tunnel-vs-ngrok-2026)) | not needed |

**Recommendation: pure poll, no inbound exposure, ever.** The argument is not cost, it is failure semantics. A poll loop's failure mode is *delay*; a webhook's failure mode is *silent loss*. For a system whose whole purpose is that money never moves unnoticed, delay is acceptable and silent loss is not. Approvals in this business are never latency-sensitive — the 48h expiry window and the 07:00 Amazon business-day close mean a 5-minute poll is 100× faster than needed. It also matches the existing decision in `DECISION-CONTROL-PLANE.md` condition 2 (loopback/tailnet only) and condition 7 (Telegram push is read-only).

Concretely: **monday is the approval UI, git is the transport, the poller is the bridge.** A `hands/monday_sync.py` run on the same 5-minute timer reads the Approvals board's Status column, and for each item that flipped to Approved, moves the corresponding file `approvals/pending/ → approvals/approved/` and stamps `decided_by`/`decided_at` from the monday activity log. If monday is down, Rami can still approve by editing the file — **two independent approval paths, one system of record**. If Cloudflare Tunnel is ever wanted later, it should be for Rami's own read access to a dashboard, never for an inbound execute path.

---

## 5. Tiered autonomy, guardrails and the ratchet

### 5.1 Tier table with initial guardrail numbers

Tiers as defined in `AGENTS.md` §3. Numbers below are the recommended concrete instantiation of the §4 placeholders.

| Action class | Tier | Guardrail parameters (initial) | Write path | Blast radius cap |
|---|---|---|---|---|
| Read / report / observe | T0 | none | DataDoe read key | n/a |
| Ad bid change | **T1** | ±15% per change; 1 change per target / 24h; only if target has ≥30 clicks in 14d | Amazon Ads MCP | 25 targets/run |
| Ad budget increase | **T1** | +25% per action, hard ceiling **CAD 150/day total spend across all campaigns**; never raises total above cap | Amazon Ads MCP | 10 campaigns/run |
| Negative keyword add | **T1** | only above the statistical threshold (≥10 clicks, 0 orders, spend ≥ 2× target CPA) | Amazon Ads MCP | 25/run |
| Price change **inside** an approved Automate Pricing band | **T1 (Amazon-operated)** | band set per SKU in `products/<sku>.md`; min price ≥ cost + 15% contribution margin after ads | Amazon Automate Pricing | per-SKU |
| Price change **outside** the band, or band change | **T2** | never >20% in 24h (Amazon floor); min 15% contribution margin after ads | DataDoe Action / Listings PATCH | 5 SKUs per packet |
| Purchase order | **T2** ≤ CAD 15,000/month cumulative; **T3** above | monthly PO ceiling CAD 15,000; cash check from Finance required; hero SKU cover floor 14 days, seasonal buffer 6 weeks | packet to Rami → manual bank transfer | 1 supplier/packet |
| New ad campaign | **T2** | must fit inside the CAD 150/day cap; starting budget ≤ CAD 20/day | Amazon Ads MCP | 1 campaign/packet |
| Listing text / images | **T2** | never ≥500 ASINs in a batch (Amazon floor); ≤5 ASINs per packet | DataDoe Action / Listings PATCH | 5 ASINs |
| FBA shipment creation | **T2** | must match an approved PO or existing stock; async — poll `getInboundOperationStatus` | Fulfillment Inbound v2024-03-20 | 1 plan/packet |
| Coupons / deals | **T2** | max discount 20%; projected margin after discount ≥ 10%; max CAD 500 exposure/promotion | DataDoe / Seller Central | 1 promo/packet |
| Buyer messages | **T2** | Rami sends or approves verbatim text; no PII role held | Messaging API / Seller Central | 1 message/packet |
| Vine enrolment | **T2** | ≤ 2 SKUs per quarter | Seller Central | 2 SKUs |
| Reimbursement claim | **T2** | file only inside the eligible window — **60 days** for most manual US/UK claims, 60–120 days for FBA customer-returns claims; some case types reject if filed too early (REPORTED — [SPS Commerce](https://www.spscommerce.com/community/articles/amazon-reimbursement-policy/), [Leviathan](https://www.leviathansellers.com/blog/amazon-fba-reimbursement-policy-2026)) | Seller Central case | 10 claims/packet |
| New marketplace, contracts, payment terms, spend > ceiling, appeals, POAs, IP responses, anything legal | **T3** | Rami only; agents prepare the packet | none | n/a |
| Any money leaving a bank account | **T3, always, permanently** | no ratchet, no exception | Rami's banking app | n/a |
| Approval expiry | all T2 | **48 hours**; expired → re-proposed with fresh data, never executed stale | runner | n/a |

Two additions I recommend beyond `AGENTS.md` as written:

1. **A daily approval budget, not just a spend budget.** Max 5 pending T2 packets at any time; max 3 new ones per day. If a department wants a sixth, it must withdraw one. This is the direct countermeasure to the 93%-approval-fatigue finding.
2. **A global kill file.** `ops/PAUSE` existing in the repo makes the runner exit at step 2 with a ledger line and no action. One `touch` from Rami's phone via the GitHub app stops the company. This is the operational form of `AGENTS.md` §6 rule 9.

### 5.2 The ratchet

`AGENTS.md` §5 gives: 30 days elapsed, ≥20 approved proposals of that class, <5% rejected. Keep it, and add three conditions that cost nothing and prevent the obvious failure:

**Promotion T2 → T1 requires ALL of:**
- ≥30 days since the class was first proposed
- ≥20 approved proposals of that class
- rejection rate <5% (so ≤1 rejection in 20)
- **zero executions of that class that failed read-back verification**
- **zero Amazon policy notifications, account-health events, or listing suppressions attributable to the class**
- **no edit by Rami to any packet of that class in the last 10** (an edited approval is a near-rejection; counting it as an approval overstates agreement)
- Chief of Staff proposes; **Rami confirms by editing the department's `AGENTS.md`** — the promotion is itself a T3 act

**Demotion T1 → T2 is automatic and immediate on ANY of:**
- one execution that failed read-back verification
- one action outside the class's guardrail numbers
- any account-health event, policy warning, or Amazon agent-policy contact
- daily ad cap breached
- three consecutive runs with a `tools_failed` entry for that class's write path
- Rami says so, by editing one line

Promotion is slow and multi-conditional; demotion is fast and single-condition. That asymmetry is the whole safety argument. Nothing ratchets a money-moving class to T1, ever.

---

## 6. Schemas

### 6.1 Approval packet

The repo already stores these as markdown with YAML front matter (`docs/CONVENTIONS.md`). Keep that — it is human-readable and git-diffable. What follows is the **normative schema** the front matter must satisfy; the runner validates against it and refuses anything that does not parse.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ApprovalPacket",
  "type": "object",
  "required": ["id","schema_version","department","tier","action_class","status",
               "created","expires","marketplace","currency","idempotency_key",
               "payload","preconditions","guardrails","evidence","impact","if_rejected"],
  "properties": {
    "id":              {"type":"string","pattern":"^[0-9]{8}-[a-z-]+-[a-z_]+-[A-Za-z0-9-]+$"},
    "schema_version":  {"const":"1.0"},
    "department":      {"enum":["finance","supply-chain","advertising","catalog",
                                "pricing-intel","customer","account-health","expansion",
                                "chief-of-staff","ceo"]},
    "tier":            {"enum":["T2","T3"]},
    "action_class":    {"enum":["purchase_order","price_change","pricing_band_change",
                                "listing_change","fba_shipment","campaign_create",
                                "coupon","buyer_message","vine_enrolment",
                                "reimbursement_claim","other"]},
    "status":          {"enum":["pending","approved","rejected","expired",
                                "executing","executed","failed","superseded"]},
    "created":         {"type":"string","format":"date-time"},
    "expires":         {"type":"string","format":"date-time",
                        "description":"created + 48h for T2"},
    "marketplace":     {"enum":["ca","us","walmart-ca"]},
    "currency":        {"enum":["CAD","USD"]},
    "estimated_cost":  {"type":["number","null"],
                        "description":"minor-unit-safe decimal string preferred; in `currency`"},
    "skus":            {"type":"array","items":{"type":"string","pattern":"^ANB-[0-9]{3}$"}},
    "asins":           {"type":"array","items":{"type":"string"}},
    "idempotency_key": {"type":"string","format":"uuid",
                        "description":"UUIDv4 generated by the proposing department; the runner sends it to the API and stores it. Never regenerated on retry."},
    "payload":         {"type":"object",
                        "description":"class-specific; validated by a per-class sub-schema"},
    "preconditions":   {"type":"array","items":{
                          "type":"object",
                          "required":["check","source","observed","asserted_at"],
                          "properties":{
                            "check":     {"type":"string"},
                            "source":    {"type":"string","description":"file path, report id, or ledger seq"},
                            "observed":  {},
                            "asserted_at":{"type":"string","format":"date-time"},
                            "revalidate":{"type":"boolean","default":true,
                                          "description":"runner re-reads this before executing"}}}},
    "guardrails":      {"type":"object",
                        "required":["class_limits_checked","within_limits"],
                        "properties":{
                          "class_limits_checked":{"type":"array","items":{"type":"string"}},
                          "within_limits":       {"type":"boolean"},
                          "amazon_floors":       {"type":"object","properties":{
                             "price_delta_pct_24h":{"type":["number","null"]},
                             "asin_batch_size":    {"type":["integer","null"]}}},
                          "budget_remaining":    {"type":["number","null"]},
                          "budget_period":       {"type":["string","null"]}}},
    "dry_run":         {"type":["object","null"],
                        "description":"tool's own dryRun/preview output, captured at proposal time",
                        "properties":{"ran_at":{"type":"string","format":"date-time"},
                                      "tool":{"type":"string"},
                                      "diff":{"type":"array","items":{"type":"object",
                                        "required":["field","from","to"]}},
                                      "warnings":{"type":"array","items":{"type":"string"}}}},
    "locks":           {"type":"array","items":{"type":"string"},
                        "description":"lock keys this packet needs, e.g. sku:ANB-017:price:2026-09-06"},
    "goal_id":         {"type":["string","null"]},
    "evidence":        {"type":"array","minItems":1,"items":{"type":"string"},
                        "description":"every claim cites its export/report/ledger seq — AGENTS.md §6.7"},
    "impact":          {"type":"string"},
    "if_rejected":     {"type":"string"},
    "requires_second_check": {"type":"boolean","default":false,
                        "description":"true for T3 and for any packet > CAD 5,000; forces a 12h cooling period between approval and execution"},
    "decided_by":      {"type":["string","null"]},
    "decided_at":      {"type":["string","null"],"format":"date-time"},
    "decision_channel":{"enum":["monday","file-edit","telegram",null]},
    "executed_at":     {"type":["string","null"],"format":"date-time"},
    "ledger_ref":      {"type":["integer","null"],"description":"ledger seq of the execution row"},
    "supersedes":      {"type":["string","null"]},
    "monday_item_id":  {"type":["string","null"]}
  }
}
```

Changes from the current `CONVENTIONS.md` front matter, and why each earns its place: `schema_version` (so the runner can refuse packets it doesn't understand); `idempotency_key` (double-execution defence); `preconditions` with `revalidate` (the runner re-checks, not just re-reads); `dry_run` (Rami sees the diff, not the intent); `locks` (cross-department collision defence); `marketplace` + `currency` on every packet (wrong-marketplace defence); `requires_second_check` (dual control substitute for a solo operator); `decision_channel` and `monday_item_id` (two approval paths, one record); `supersedes` (re-proposal after expiry links to the original).

### 6.2 Ledger entry

Extends the existing `ledger/actions.jsonl` line — every current field is preserved, so old rows stay valid.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LedgerEntry",
  "type": "object",
  "required": ["seq","ts","schema_version","department","tier","action_class",
               "runtime","target","input","output","approval_id","reason",
               "idempotency_key","prev_hash","hash"],
  "properties": {
    "seq":            {"type":"integer","minimum":1,"description":"monotonic, gapless"},
    "ts":             {"type":"string","format":"date-time","description":"Asia/Jerusalem offset"},
    "schema_version": {"const":"1.0"},
    "department":     {"type":"string"},
    "tier":           {"enum":["T0","T1","T2","T3"]},
    "action_class":   {"type":"string"},
    "action_type":    {"type":"string","description":"legacy alias of action_class"},
    "runtime":        {"enum":["claude-code","codex","grok-bot","paperclip","hands-runner","human"]},
    "actor":          {"type":"string","description":"e.g. hands-runner@macmini, rami"},
    "marketplace":    {"enum":["ca","us","walmart-ca",null]},
    "currency":       {"enum":["CAD","USD",null]},
    "amount":         {"type":["string","null"],
                       "description":"decimal STRING, never a float; e.g. \"6400.00\""},
    "target":         {"type":"object","description":"sku/asin/campaign_id/keyword_id/po_id"},
    "input":          {"type":"object","description":"exact request sent"},
    "output":         {"type":"object","required":["status"],
                       "properties":{"status":{"enum":["ok","failed","partial","noop","dry-run"]},
                                     "api":{"type":"string"},
                                     "http_status":{"type":["integer","null"]},
                                     "response_id":{"type":["string","null"]},
                                     "error":{"type":["string","null"]}}},
    "verification":   {"type":["object","null"],
                       "required":["method","expected","observed","passed","checked_at"],
                       "description":"read-back after write"},
    "approval_id":    {"type":["string","null"]},
    "idempotency_key":{"type":["string","null"],"format":"uuid"},
    "attempt":        {"type":"integer","default":1},
    "reason":         {"type":"string"},
    "evidence":       {"type":"array","items":{"type":"string"}},
    "goal_id":        {"type":["string","null"]},
    "prev_hash":      {"type":"string","pattern":"^[a-f0-9]{64}$|^GENESIS$"},
    "hash":           {"type":"string","pattern":"^[a-f0-9]{64}$",
                       "description":"SHA-256 over canonical JSON of all fields except `hash`"},
    "git_anchor":     {"type":["string","null"],
                       "description":"on the day's first row, the previous day's pushed head commit SHA"}
  }
}
```

Every **attempted** write gets a row, including failures, dry runs and no-ops. A row is never edited; a correction is a new row referencing the old `seq`. `hash` verification is a 20-line script that should run at the start of every hands-runner invocation and refuse to proceed if the chain is broken. **`amount` is a string, always** — see §9 on rounding.

---

## 7. The end-to-end money path

Numbered, with the component at each step. Steps 1–7 involve no credentials that can move anything.

1. **Detect.** Department agent (reasoning model, T0 read-only tools: DataDoe MCP read key, Keepa, QBO read-only) runs in its calendar slot, reads `state/*.md`, `products/`, `ledger/kpis.csv`, its `memory/MEMORY.md`, and its inbox. *Component: agent harness (Claude Code / Codex / Paperclip).*
2. **Consult.** If the action needs another department's fact, it writes a typed request (`need-cash-check`, `need-margin-floor`) and **stops**, resuming next slot. *Component: `requests/` files.*
3. **Check locks and blackouts.** Reads `state/locks.md` and `state/calendar.md`. If another department holds `sku:ANB-017:price` today, it does not propose. *Component: lock file (§8).*
4. **Dry-run.** Calls the write tool's preview: DataDoe `dryRun`, or Ads MCP read-then-simulate, or a local computation for a PO. Captures the diff. *Component: DataDoe Actions / Amazon Ads MCP.*
5. **Propose.** Writes `approvals/pending/<id>.md` conforming to §6.1: idempotency key, preconditions, dry-run diff, evidence citations, guardrail arithmetic, 48h expiry. *Component: repo file + git commit.*
6. **Validate (machine, no LLM).** `hands/validate.py` on the 5-minute timer checks: schema; expiry not already past; guardrails arithmetic recomputed independently; budget remaining recomputed from `ledger/actions.jsonl`, not from the packet's claim; Amazon floors (>20%/24h, ≥500 ASINs) not crossed; no duplicate idempotency key in the ledger; ≤5 pending packets. A failing packet moves to `approvals/rejected/` with a machine reason. *Component: deterministic Python.*
7. **Present.** `hands/monday_sync.py` creates or updates a monday Approvals-board item: title, one-paragraph proposal, cost, diff, expiry, deadline. Telegram push (read-only) posts the link. The CEO department ranks it into `briefs/YYYY-MM-DD-decisions.md`, capped at five. *Component: monday.com Pro + Telegram bot + brief file.*
8. **Decide.** Rami sets the monday Status column to Approved/Rejected, or edits the file directly. Both paths are recorded; `decision_channel` says which. *Component: Rami.*
9. **Sync the decision.** The poller reads monday, moves `pending/ → approved/`, stamps `decided_by`, `decided_at`, `decision_channel` from monday's activity log, commits, pushes. *Component: `hands/monday_sync.py`.*
10. **Re-validate at execution time.** The runner repeats step 6 **plus** re-reads every `precondition` with `revalidate: true` against live data. If cover, price, competitor state, cash or budget has moved, the packet goes back to `pending/` with a `supersedes` note and Rami is told why. If `requires_second_check` and less than 12h has passed since approval, it waits. *Component: `hands/runner.py`.*
11. **Acquire the execution lock.** File lock on the packet's `locks[]` keys, plus a machine-level lock so two runner invocations cannot overlap. *Component: `flock` on the Mac mini.*
12. **Execute.** `op run` injects the write credential; the runner calls the API **once** with `idempotency_key`. Batch actions are chunked with a per-chunk key so a partial failure is resumable. *Component: DataDoe Actions API / Amazon Ads MCP / SP-API.*
13. **Verify by read-back.** Re-read the mutated object (`getListingsItem`, campaign read, `getInboundOperationStatus` polled to terminal state) and compare observed to expected. *Component: the same API, read side.*
14. **Ledger.** Append a hash-chained row per §6.2, including `verification`. Failed and partial writes get rows too. *Component: `ledger/actions.jsonl`.*
15. **Close the loop.** Move the file to `approvals/executed/` (or `failed/`), set `ledger_ref`; update the monday item to Executed with the ledger seq; commit and push. Next day's git head SHA becomes the ledger's external anchor. *Component: git + monday.*

**Where actual money leaves a bank account, the path forks at step 8 and never rejoins:**

8b. **Payment packet.** For an approved PO, the runner generates `approvals/executed/<id>-payment-packet.md` — supplier legal name, bank details **read from `suppliers/<name>.md` and displayed for Rami to compare against what he has on file, never auto-filled into anything**, amount and currency, PO reference, what it buys, which SKUs, expected ship date, cover impact, remaining monthly PO ceiling, the two prior payments to this supplier with dates and amounts, and a one-line "what changes if you don't pay this".
8c. **Rami pays**, manually, in his bank, on his device. No agent, no runner, no API ever touches a bank.
8d. **Rami marks paid** on the monday item (date + reference).
8e. **Books.** The runner (or Finance next run) records the bill/payment in QuickBooks Online via the Intuit MCP. Note: **QBO write is a separate credential and a separate approval class from Amazon write.** Today, per `docs/MCP-SERVERS.md`, QBO is read-only and A2X posts the Amazon settlements — keep that; the only QBO write worth adding is bill creation, and only after 30 days of clean operation.

**Definition of "money moves" for this business, and how each is gated:**

| Money move | Real mechanism | Gate |
|---|---|---|
| PO to supplier | bank transfer by Rami | T2 packet ≤ CAD 15k/mo, T3 above; payment always manual |
| Amazon ads spend | Amazon bills the account | T1 inside the CAD 150/day cap; the cap is the gate |
| Coupons / deals | forgone revenue | T2, margin floor + CAD 500 exposure cap |
| Price cuts | forgone revenue | T1 inside the Automate Pricing band; T2 to move the band |
| Reimbursement claims | money **in**, but a false claim is an account-health risk | T2 |
| Refunds / concessions | money out via Amazon | T2, and prefer letting Amazon's own policy handle it |
| FBA/inbound fees, storage | Amazon bills | consequence of an approved shipment; surfaced in the packet |
| Subscriptions (DataDoe, monday, Keepa) | card on file | T3, Rami only, reviewed at month close |

---

## 8. Coordination between departments, without a chat

Four mechanisms, all files, all already half-present in the repo:

1. **Blackboard.** `state/<dept>.md`, overwritten each run, dated, with a stable `## Data` table. `AGENTS.md` §6.6 already makes a stale state file a failed run — that is the right severity, because every downstream decision reads it.
2. **Typed requests.** `requests/<dept>/inbox/`, enumerated types, `needed-by`, answer appended in-file. Add one field: **`goal_id`**, per `DECISION-CONTROL-PLANE.md`.
3. **Locks.** New: `state/locks.md`, one line per held lock, written by the acquiring department and released at end of run or on expiry.
   ```
   sku:ANB-017:price   | pricing-intel | 2026-09-06 | expires 2026-09-07T07:00+03:00 | approvals/pending/20260906-pricing-intel-price_change-ANB-017
   sku:ANB-017:listing | catalog       | 2026-09-06 | expires 2026-09-07T07:00+03:00 | —
   ```
   Lock keys are `<scope>:<id>:<dimension>`. **One change per SKU per dimension per day.** The runner refuses to execute a packet whose lock is held by another department, which makes the lock enforceable rather than advisory. Locks expire at the next Amazon business-day close (07:00 Asia/Jerusalem) so a crashed run cannot deadlock the company.
4. **Conflict rules** — a fixed precedence list, so no negotiation is needed:
   1. **account-health outranks everything.** A `compliance-hold` on a SKU voids all pending packets touching it.
   2. **supply-chain outranks advertising on stockout.** A `stockout-risk` request forces advertising to throttle before it may scale.
   3. **finance outranks supply-chain on cash.** An unanswered or negative `need-cash-check` blocks a PO packet.
   4. **pricing-intel outranks catalog on price; catalog outranks pricing-intel on content.** Disjoint dimensions, so the lock keys keep them apart.
   5. **A `blackout` request beats any pricing action** for its stated window.
   6. Ties go to the **earlier-created packet**; the later one is marked `superseded`.

**Sequencing.** `docs/CALENDAR.md` already runs one department at a time in fixed slots, with the Chief of Staff at 07:00 and the CEO last. That sequential design is worth more than it looks: it makes locks nearly redundant, it sidesteps the Paperclip concurrency ceiling noted in the control-plane decision, and it means every department reads state written earlier the same morning rather than mid-flight. Keep it. The orchestrator's only real jobs are: run the slots in order, skip a department whose upstream dependency failed, escalate unanswered requests past `needed-by`, and hold the approval-count cap.

---

## 9. Failure modes and the check that catches each

| Failure mode | How it happens here | Check that catches it |
|---|---|---|
| **Stale approval** | Rami approves Friday, runner executes Monday, cover/price/competitor moved | 48h `expires` + step-10 re-validation of `preconditions` with `revalidate:true`. Expired → `supersedes` re-proposal with fresh data, never execution |
| **Double execution** | runner crashes after the API call, before the ledger write; retries | `idempotency_key` sent to the API **and** checked against the ledger before every call; step-13 read-back detects "already at target" and writes a `noop` row |
| **Partial failure mid-batch** | 5-SKU price packet, SKU 3 fails | chunk per SKU with a per-chunk idempotency key; per-chunk ledger rows; packet ends `partial`, moves to `approvals/failed/`, remaining chunks re-proposed. Never "retry the whole packet" |
| **FBA async write looks like a failure** | Inbound v2024-03-20 POSTs return before the work is done | must poll `getInboundOperationStatus` to a terminal state before writing the ledger row; a timeout is `output.status="partial"`, not `failed` |
| **Currency / rounding** | CAD packet executed against a USD marketplace; float arithmetic drifts | `currency` and `marketplace` mandatory on every packet and ledger row; runner asserts `packet.marketplace == credential.marketplace_id`; **all money as decimal strings, never floats**; round half-up to the marketplace's minor unit **once**, at the boundary, and log both the pre- and post-rounded value |
| **Wrong marketplace** | US launch: same SKU, two ASINs, two price bands | marketplace in the packet `id`, in the lock key, in the credential selection, and asserted at execution; separate Automate Pricing rules per marketplace; a packet with no `marketplace` fails schema validation |
| **Guardrail drift** | budget "remaining" computed by the agent from stale state | runner recomputes budget remaining from the ledger, ignoring the packet's claim |
| **Approval fatigue** | ten packets a day, all rubber-stamped | max 3 new / 5 pending; CEO brief capped at 5 ranked items; band changes replace price changes |
| **Broken audit chain** | a bad edit or a manual fix to `actions.jsonl` | chain verify at every runner start; refuse to proceed; daily git head SHA as external anchor |
| **Credential leakage into a reasoning model's context** | someone adds an SP-API key to a department `.mcp.json` | `${NAME}` references only; runner-only credentials in a separate 1Password vault the agent harnesses cannot reach; a repo pre-commit secret scan |
| **Amazon says stop** | Section 19 (c) — cease access on request | `ops/PAUSE` file; documented kill order in `AGENTS.md` §6.9; a rehearsed drill, not just a paragraph |
| **DataDoe disappears / changes terms** | single point of failure for reads *and* writes | private SP-API app registered in parallel as the escape hatch |
| **Reimbursement filed outside the window** | 60-day / 60–120-day windows, plus early-filing rejections | window arithmetic in the packet's `preconditions`, re-validated at execution |

---

## 10. Implications for the design

1. **Verify Section 19 in Rami's own Seller Central account this week, and paste it into the repo.** Everything in `AGENTS.md` §5–6 rests on text nobody in this project has read in the original. This is the highest-value hour available.
2. **Make Automate Pricing the pricing engine.** Approving a band once beats approving prices forever, it is Amazon's own tool, it does not consume the price-change allotment, and it removes the single largest source of approval volume. Rewrite the pricing department's charter around proposing *bands*, not prices.
3. **The runner polls. Nothing inbound. Ever.** No tunnel, no webhook, no Funnel. monday is the UI, git is the transport, a 5-minute `launchd` job is the trigger, and the failure mode is delay rather than loss.
4. **Split the credential domains three ways**: read-only agent tools (DataDoe read key, Keepa, QBO read) in department `.mcp.json` via `${NAME}`; write credentials in a separate 1Password vault used only by `op run` around the runner; banking nowhere. The reasoning model should be structurally incapable of moving money, not merely instructed not to.
5. **Re-validation at execution time is the load-bearing control**, more than the approval itself. Rami approving is one signal; the machine independently confirming the numbers still hold at T-minus-zero is what stops the stale-approval class of loss.
6. **Budget the approvals, not just the money.** Three new packets a day. If the departments generate more, they are proposing at the wrong altitude.
7. **Register the private SP-API app now, request no restricted PII roles.** The DPP obligations that come with PII are not honestly satisfiable by a solo operator on a Mac mini, and nothing in the charter needs buyer addresses.
8. **The ratchet must be asymmetric**: six conditions to promote, one to demote, and no money-moving class ever promotes.

---

## 11. Open questions

1. **What does Section 19 actually say?** Specifically: is there an agent *registration* step beyond having an SP-API app ID? Is there a required self-identification mechanism (a header? a user-agent? a declaration in Seller Central)? Does "documented human authorization" have a prescribed format? Does the policy apply to a seller automating their *own* account, or only to third-party tools? Blocked: I could not open the BSA.
2. **Does DataDoe's SP-API app satisfy "traceable to a registered application" for actions Rami's agents originate?** If Amazon's view is that the *seller's* agent must be registered, a hosted intermediary may not be sufficient. Ask DataDoe in writing and keep the answer in the repo.
3. **How long does private SP-API developer approval take in 2026, for a Canadian seller?** UNKNOWN. Materially affects the January 2027 US FBA deadline.
4. **Does Amazon's 20%/24h price floor apply per ASIN, per SKU, or per marketplace-offer?** And does an Automate Pricing move inside a band count toward it? The sources are silent; the conservative reading (per ASIN, and Automate Pricing exempt because Amazon operates it) is what the tier table assumes.
5. **Does the Amazon Ads MCP expose a dry-run or preview?** If not, the T1 ads class has no diff preview and relies entirely on the ±15% / +25% bounds plus read-back. Worth confirming before ads go T1.
6. **monday.com Pro API allowance**: 10,000 calls/day is reported; the complexity budget resets every 60s and is per-account regardless of plan. A 5-minute poll is trivially inside it, but confirm the complexity cost of the board query before adding a second poller.
7. **Is Seller Assistant safe to use as a read-only second opinion?** It is Amazon's own agent operating inside Amazon's own account, so Section 19 presumably does not bind it — but confirm it cannot take actions without an explicit per-action approval before letting any department consult it.
8. **What is the actual monthly cadence of QBO writes worth automating?** If A2X already posts settlements and Rami pays suppliers manually, the QBO write scope may reduce to zero — which would be the best possible answer.

---

## Sources

Amazon Agent Policy (all REPORTED, primary blocked): [EcomCrew](https://www.ecomcrew.com/amazon-bans-ai-agents-seller-platform/) · [MyAmazonGuy](https://myamazonguy.com/news/amazon-services-business-solutions-agreement/) · [DAM Law Firm](https://damlawfirm.com/blog/amazon-bsa-ai-agent-policy-update/) · [SellerSprite](https://www.sellersprite.com/en/blog/amazon-bsa-agent-policy-2026) · [Profasee](https://profasee.com/blog/amazon-ai-agent-policy-what-sellers-need-to-know/) · [Digital Applied](https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules) · [amazonsellers.attorney](http://www.amazonsellers.attorney/blog/the-20-rule-avoiding-suspensions-under-amazons-2026-ai-agent-policy) · [SellerShorts](https://sellershorts.com/resources/ai-for-amazon-sellers/amazon-ai-agent-policy)

Amazon products: [Amazon Ads MCP open beta](https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta) · [MediaPost](https://www.mediapost.com/publications/article/412481/amazon-ads-mcp-server-moves-to-open-beta.html) · [AdExchanger](https://www.adexchanger.com/marketers/amazon-ads-opens-a-beta-test-for-its-new-mcp-server/) · [Digiday](https://digiday.com/media-buying/ad-tech-briefing-amazon-launches-mcp-server-for-agent-driven-advertising/) · [Feedvisor on Ads Agent](https://feedvisor.com/university/what-is-amazon-ads-agent/) · [Nova on Seller Assistant](https://novadata.io/resources/news/amazon-seller-assistant-agentic-ai) · [Automate Pricing](https://sell.amazon.com/tools/automate-pricing)

SP-API: **VERIFIED** [amzn/selling-partner-api-samples README](https://github.com/amzn/selling-partner-api-samples/blob/main/README.md) · [registration overview](https://developer-docs.amazon.com/sp-api/docs/sp-api-registration-overview) · [self-authorization](https://developer-docs.amazon.com/sp-api/docs/self-authorization) · [role mappings](https://developer-docs.amazon.com/sp-api/docs/role-mappings) · [patchListingsItem](https://developer-docs.amazon.com/sp-api/reference/patchlistingsitem) · [Fulfillment Inbound v2024-03-20](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-use-case-guide) · [Cybersecify on the DPP](https://cybersecify.com/blog/amazon-sp-api-data-protection-policy-pentest/) · [Nova rate-limit guide](https://novadata.io/resources/blog/amazon-sp-api-rate-limits-guide)

Agent HITL: [Anthropic — measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) · [Anthropic — safe and trustworthy agents](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents) · [OpenAI Agents SDK HITL](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/) · [OpenAI guardrails & approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) · [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) · [Temporal HITL approvals](https://temporal.io/blog/human-in-the-loop-approvals) · [Stripe idempotency](https://docs.stripe.com/api/idempotent_requests) · [AgentPatterns audit trail](https://agentpatterns.ai/security/cryptographic-governance-audit-trail/) · [Formance spend limits](https://www.formance.com/blog/industry-analysis/ai-agent-spending-limits) · [Fystack guardrails](https://fystack.io/blog/6-guardrails-to-limit-ai-agent-spending-on-payment-rails)

Infrastructure: **VERIFIED** [intuit/quickbooks-online-mcp-server README](https://github.com/intuit/quickbooks-online-mcp-server/blob/main/README.md) · [1Password op run](https://developer.1password.com/docs/cli/secrets-environment-variables) · [monday webhooks](https://developer.monday.com/api-reference/reference/webhooks) · [monday automation rate limits](https://support.monday.com/hc/en-us/articles/9060097050258-Automation-and-integration-rate-limits) · [monday API plans](https://pipeline.zoominfo.com/sales/monday-com-api) · [tunnel comparison](https://insights.nomadlab.cc/blog/2026/04/tailscale-vs-cloudflare-tunnel-vs-ngrok-2026) · [DataDoe platform](https://www.datadoe.com/platform) · [DataDoe pricing](https://www.datadoe.com/pricing) · [Amazon reimbursement windows](https://www.spscommerce.com/community/articles/amazon-reimbursement-policy/)
