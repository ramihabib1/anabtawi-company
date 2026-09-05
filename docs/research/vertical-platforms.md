# Vertical AI Platforms for Amazon/Marketplace Sellers — Survey (Sept 2026)

Status: COMPLETE (Sept 2026 survey).

Purpose: Decide whether any existing "AI seller operating system" platform should
replace or complement the self-built Habib Distribution OS (company-of-AI-departments,
Claude Agent SDK + Supabase + Mem0) for a solo operator scaling Amazon CA now, US
launch Jan 2027, Walmart later, ~$10k/mo -> $85k/mo revenue.

Tagging convention: every substantive claim is tagged
- **VERIFIED** — confirmed directly from a primary source (vendor doc, official page, SP-API docs) fetched during this research
- **REPORTED** — stated by the vendor's marketing/blog/press, a review site, or a user, not independently confirmed
- **UNKNOWN** — could not find a reliable public source; flagged as a gap

---

## 0. Regulatory ground truth: Amazon's March 2026 Agent Policy

**VERIFIED-adjacent (multiple converging secondary sources, no single official Amazon policy page reachable directly in this session; treat as REPORTED but high-confidence given convergence)**

- On March 4, 2026, Amazon added a new Section 19 ("Agents") to the Business Solutions Agreement governing any automated tool, AI system, or bot that accesses Amazon Seller/Ads systems — including repricers, PPC automation, browser extensions, and fulfillment scripts. — REPORTED, [Amazon AI Agent Policy: New Automated Seller Rules 2026 (Digital Applied)](https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules), [BSA Update summary (SellerShorts)](https://sellershorts.com/resources/ai-for-amazon-sellers/amazon-ai-agent-policy)
- Browser automation and screen scraping of Seller Central are explicitly banned outright — "frequency does not matter, scraping a page once an hour is still a violation." This closes the loophole many legacy seller tools used (headless browser sessions against Seller Central UI) even when wrapped in an "AI layer." — REPORTED, same sources above.
- Compliant automated tools must: (1) register and operate through **SP-API** (not scraping), (2) maintain a 12-month audit trail of actions taken, (3) self-identify as automated/non-human systems, and (4) obtain explicit human authorization for "high-impact" actions such as price changes over 20% within a 24-hour window. — REPORTED, [Digital Applied](https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules), [QuickPrepMedia](https://www.quickprepmedia.com/en/blog/amazon-ai-agent-policy-march-2026/)
- The only Amazon-sanctioned source for **competitor pricing data** in automated workflows is the Product Advertising API (PA-API), which has its own separate registration and rate limits — meaning competitor-intel scraping tools (common in this category) are now a compliance risk unless rebuilt on PA-API. — REPORTED, [Digital Applied](https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules)
- A 90-day transition window from March 4, 2026 gave sellers/vendors until roughly early June 2026 to bring tooling into compliance before enforcement. As of this survey (September 2026), enforcement is understood to be active. — REPORTED, same sources.
- **Implication for this survey:** any vendor still relying on Seller Central browser automation, or on scraping competitor ASIN pages instead of PA-API, is now a policy-violation risk for the operator's account, not just an inferior architecture choice. This is used as a hard filter below.

## 1. Amazon-specific AI agent / "AI operator" platforms

### 1.1 Jarvio (jarvio.io)

- **What it does:** Positions itself as "an AI system for Amazon" that connects to Seller Central and other tools to monitor the catalog and take action across pricing, listing edits, inventory ordering, customer responses, and ad adjustments. Trained on/marketed against ">$1B in Amazon sales data," "2,000+ brands." — REPORTED (vendor site via search snippet), [Jarvio homepage](https://jarvio.io/), [Jarvio Review 2026 (Ecommerce Paradise)](https://ecommerceparadise.com/jarvio-review-2026/)
- **Scope:** PPC management, listings, inventory, competitors, reimbursements, reviews, reporting — i.e., attempts most of the department list except formal finance/compliance modules. Uses the Amazon Advertising API for ad management (same API surface as competitors). — REPORTED, [Jarvio Features](https://jarvio.io/features)
- **Goals/OKRs:** Markets itself against Perpetua specifically as "Goal-Based PPC vs AI Agent," implying some goal-input mechanism for PPC bidding, but no evidence of a cross-department strategic goal/OKR layer that spans inventory+ads+pricing+compliance together. — REPORTED, [Jarvio vs Perpetua](https://jarvio.io/vs/perpetua)
- **Task creation / approval gate:** Marketing language ("connects... to monitor... and take action") suggests it can act autonomously on the account rather than only proposing tasks; no explicit public documentation found describing a mandatory human-approval step before financial actions (price/bid changes). This is a **gap/UNKNOWN** — could not confirm an approval-gate architecture equivalent to the operator's requirement.
- **Pricing:** Credit-based. Starter $49/mo (5,000 credits ≈ 200–500 automation runs/day per vendor framing), Growth 25,000 credits/mo, Scale tier for $1M–$10M GMV sellers, "Infinity" tier above $10M. Flat subscription regardless of ad spend. — REPORTED, [Jarvio Pricing](https://jarvio.io/pricing)
- **Lock-in / API registration:** No public statement found on SP-API developer registration status or data export/portability. **UNKNOWN.**
- **Verdict fit:** A commercial competitor to "build your own," explicitly contrasting itself with a Claude-built agent in its own blog post ("Building an Amazon AI Agent with Claude vs Using Jarvio") — confirming this is a direct alternative to the operator's DIY approach. — REPORTED, [Jarvio blog](https://jarvio.io/blog/build-amazon-ai-agent-vs-jarvio)

### 1.2 Stormy AI (stormy.ai)

- **Category mismatch:** Stormy AI's core positioning as of Sept 2026 is "the AI operating system for service businesses" (marketing/lead-gen, calls, quotes, invoices, inventory for service SMBs), and it is Y Combinator-backed for automating influencer-marketing outreach — it is **not** primarily an Amazon marketplace-seller platform. — REPORTED, [Stormy AI homepage](https://stormy.ai/), [Y Combinator listing](https://www.ycombinator.com/companies/stormy-ai-autonomous-marketing-agent)
- It publishes Amazon-seller-adjacent educational blog content (e.g., "How to Automate Amazon Seller Central in 2026," a Vine playbook, an FBA fee guide) but there is no evidence of a native Amazon Seller Central/SP-API integration or product surface — this looks like content marketing/SEO rather than a real Amazon product line. — REPORTED, [Stormy AI blog](https://stormy.ai/blog/amazon-seller-central-automation-ai-agent-playbook)
- **Conclusion:** Not a credible candidate for this use case; excluded from the top-3 comparison.

### 1.3 Autron (autron.ai)

- **What it does:** "Agentic managers for Amazon Ads" — a conversational AI agent scoped specifically to Amazon Advertising (PPC), not full business operations. You ask a question, it gives a decision, using account context from Autron's own ad data plus Amazon Ads and Seller Central. — REPORTED, [Autron Agent](https://autron.ai/agent)
- Sits in the "reinforcement-learning autonomous bidder" category — models product/campaign history and re-optimizes bids hourly toward a stated goal, largely hands-off once configured. — REPORTED, [MarketplaceAdPros comparison](https://marketplaceadpros.com/guides/best-ai-agents-for-amazon-sellers-2026/)
- **Pricing:** Autron Agent flat $50/mo for the conversational analyst tier; managed/automated campaign tiers priced separately (not itemized in search results). 500+ brands claimed, 30-day free trial. — REPORTED, [Autron Pricing](https://autron.ai/pricing)
- **Scope limitation:** PPC only — no inventory, catalog, compliance, or finance coverage. A department-level tool, not an OS. Also publishes an MCP server for its ads agent. — REPORTED, [Autron blog on Ads Agent + MCP](https://autron.ai/blog/amazon-ppc-automation-in-2026-what-the-ads-agent-and-mcp-server-mean-for-sellers)

### 1.4 Trellis (gotrellis.com)

- **What it does:** Advertising + dynamic pricing + listing content/SEO software for Amazon, Walmart, Shopify, and TikTok Shop, positioned as a "managed service that shows you decisions rather than reports." Machine-learning dynamic pricing, AI-generated listing content, AI-powered ad scaling. — REPORTED, [Trellis homepage](https://gotrellis.com/), [Trellis Amazon page](https://gotrellis.com/amazon/)
- **Scope:** Ads + pricing + catalog content across multiple marketplaces (relevant to the operator's Walmart-later roadmap) but no evidence of inventory/restock planning, finance/compliance, or a cross-department goal layer. — REPORTED, [Trellis Catalog Management](https://gotrellis.com/resources/blog/amazon-catalog-management/)
- Explicitly also serves agencies (white-label/managed offering), suggesting it is often bought as a service, not self-served software. — REPORTED, [Trellis for Agencies](https://gotrellis.com/services/agencies/)
- **UNKNOWN:** approval-gate design, SP-API developer registration status, pricing (not published publicly — "contact sales" model typical of this tier).

### 1.5 Threecolts / Seller 365

- Threecolts is a roll-up company that has acquired multiple legacy point tools (Tactical Arbitrage, InventoryLab, FeedbackWhiz, SmartRepricer, ScoutIQ, etc.) and bundled them as "Seller 365" — ten tools in one subscription starting at $69/mo, covering sourcing, listing, repricing, accounting, feedback automation, and reimbursements across Amazon/Walmart/eBay (30,000+ active sellers claimed). — REPORTED, [Threecolts Seller 365](https://www.threecolts.com/seller-365), [Ecommerce Paradise review](https://ecommerceparadise.com/threecolts-review-2026/)
- 2026 marketing adds "unlimited mapping, AI content for 1,000 listings/month, and agentic operations" to the top tier, but this reads as a bolt-on AI layer over a bundle of older, separately-built tools rather than a unified agent architecture with shared state/goals. — REPORTED, [Ecommerce Paradise](https://ecommerceparadise.com/threecolts-review-2026/)
- **Risk flag:** several of the acquired tools (repricers especially) have historically relied on browser-session/scraping techniques; given the March 2026 Agent Policy ban on Seller Central scraping, compliance status of the legacy repricer components is **UNKNOWN** and worth direct vendor verification before use.
- No goal/OKR layer, no documented approval-gate architecture, no SP-API registration statement found. **UNKNOWN** on all three.

### 1.6 Sellesta

- Sellesta AI (listing optimization, review analysis, content tools; a "trusted developer verified by Amazon") had a free/$5/$39 pricing ladder as of recent snapshots, but multiple sources note it "has largely disappeared from the web" as of 2026 — effectively defunct or dormant. — REPORTED, [Dang.ai: "What happened to sellesta.ai?"](https://dang.ai/tool/ai-amazon-seller-platform-sellesta), [Sellesta pricing snapshot](https://powerusers.ai/ai-tool/sellesta/)
- **Conclusion:** Not viable as a current candidate; excluded.

### 1.7 SellerApp

- No distinct 2026 "AI agent" product surfaced in search results beyond being referenced in general "best AI tools" listicles alongside Helium 10/Jungle Scout; no evidence found of an autonomous/scheduled-agent architecture, goal layer, or approval gate specific to SellerApp. **UNKNOWN / likely still a traditional analytics-dashboard tool with AI-assist features**, not a full agent OS.

### 1.8 Nova Analytics (novadata.io)

- **What it does:** An Amazon analytics/P&L platform (SKU-level profit, 200+ metrics, 21 marketplaces, hourly refresh) that connects directly to SP-API and the Advertising API, plus a native **Claude MCP** server ("Nova MCP") giving Claude (or ChatGPT/Gemini/any MCP client) **secure, read-only** access to a pre-modeled schema of the seller's own data. — REPORTED, [Build AI Agents on Amazon Data | Claude MCP](https://novadata.io/build-agents), [Amazon AI Agents — Connect Claude to Your Seller Data with MCP](https://novadata.io/amazon-ai-agents)
- Ships pre-built agent templates: "Profit Watchdog," "Inventory Planner," "PPC Optimizer" — but these run *through* the MCP read layer into whatever LLM client the user brings (e.g., Claude Desktop/Claude Code on a Claude Max plan), rather than being a hosted autonomous agent runtime itself. This is architecturally close to what the operator is already doing (SP-API + LLM), just packaged as a managed data layer instead of self-hosted Supabase sync. — REPORTED, same sources.
- **Read vs write:** Explicitly read-only ("secure, read-only database access"). No evidence of Nova executing writes to Seller Central/Ads — it is an intelligence/data layer, not an action layer. This matches the operator's own principle of keeping writes behind a single gated Executor.
- **Pricing signal:** promotion offering free-for-life to signups before Aug 31 (2026) suggests an intro/land-grab pricing phase; no stable price list found in search results. **UNKNOWN** steady-state pricing.
- **Fit:** Best understood as a possible **replacement for or complement to** the operator's own `sync/` layer + read-side Supabase views — i.e., a Tier-0/data-layer candidate, not a department-running agent OS. Does not have goals/OKRs, task/approval workflow, or a scheduler of its own beyond what the MCP-connected LLM client provides.

### 1.9 DataDoe (datadoe.com) — see also Section 5 for the dedicated Skill Hub evaluation

- Positions as an "Amazon Data & Action Layer for AI": MCP + API + analytics, SOC 2 Type II + Amazon DPP (Data Protection Policy) clearance, flat $97/mo tier. — REPORTED, [DataDoe Platform](https://www.datadoe.com/platform), [DataDoe Hub](https://www.datadoe.com/hub)
- Ships a **Skill Hub** of 47+ pre-built agent skills installable into Claude Code, Codex, or "OpenClaw," plus **async scheduled agents** that run tasks against live data on a cadence — e.g., overnight reorder forecasts delivered by 8am, weekly P&L briefs auto-sent to Slack/inbox, anomaly alerts when a SKU margin drops. — REPORTED, [DataDoe Hub](https://www.datadoe.com/hub), [Amazon SP-API Skill vs Amazon Seller MCP](https://www.datadoe.com/blog-posts/amazon-sp-api-skill-vs-amazon-seller-mcp)
- Explicitly built for the Claude Code / Claude ecosystem (skills format matches Claude's Skills convention) — directly relevant to the operator's existing Claude Max subscription. Full evaluation of its viability as a Tier-0 control plane is in Section 5.

### 1.10 AgentCentral (agentcentral.to)

- A hosted MCP server for Amazon sellers connecting Claude/ChatGPT/other MCP clients to Ads, Seller Central, inventory, orders, catalog, rankings, finance, and fulfillment data, with **pre-synced reads and "guarded writes."** — REPORTED, [AgentCentral homepage](https://agentcentral.to/), [Seller Central Integrations](https://agentcentral.to/amazon-seller-central-integrations)
- Data model: pre-syncs on a scheduled cadence, retains history per data category (standard 30-day, extended backfills available), so the connected agent queries a local materialized layer instead of live Seller Central page loads — directly analogous to the operator's own Supabase sync-then-agent pattern. — REPORTED, same source.
- Onboarding is via Amazon OAuth (not scraping), scoped API keys, or a signed Claude connector URL — consistent with SP-API-based, policy-compliant access. — REPORTED, [AgentCentral Seller Central Integrations](https://agentcentral.to/amazon-seller-central-integrations)
- "Guarded writes" is the interesting claim for this operator's approval-gate requirement, but no detailed public documentation of the approval mechanism (e.g., is it a human-in-the-loop confirmation, or just scoped API permissions?) was found. **UNKNOWN** on the precise approval semantics — needs direct vendor verification.
- Competes head-to-head with DataDoe; DataDoe publishes its own "DataDoe vs AgentCentral" comparison page (self-serving, treat comparison claims as REPORTED/vendor-biased, not neutral). — [DataDoe vs AgentCentral](https://www.datadoe.com/compare/datadoe-vs-agentcentral)

### 1.11 Seller Labs Genius

- Bundle of FeedbackGenius (reviews/feedback), AdGenius (PPC, no ad-spend cap), ProfitGenius (P&L/Data Hub + an Amazon MCP server for Claude/ChatGPT), plus a beta "Agent Genius" inside the Genius Bundle. — REPORTED, [Seller Labs pricing/knowledge base](https://www.sellerlabs.com/knowledge-base/seller-labs-plans-and-pricing-guide/)
- Pricing scales with trailing-month Amazon revenue: free under $30k/mo in sales, then tiered; single tools from $19.99/mo, Genius Bundle from $49.99/mo up to $999.99/mo at high revenue. 14-day free trial. — REPORTED, [Seller Labs Pricing](https://www.sellerlabs.com/pricing/)
- Like Nova and Seller Labs' own MCP, this is another vendor now shipping an **MCP-to-Claude/ChatGPT bridge** for its existing analytics dataset rather than a fully autonomous agent OS — "Agent Genius" is explicitly beta and scoped to recommendations, not the whole business.

### 1.12 Helium 10 — "Helium" AI Commerce Agent

- Launched August 24, 2026: "Helium," described as "the Commerce AI Agent that helps run your Amazon Business," diagnosing problems, surfacing opportunities, and recommending actions across Research, Ads, and Commerce data inside Helium 10's existing platform. — VERIFIED (press release, cross-confirmed by multiple wire services), [GlobeNewswire](https://www.globenewswire.com/news-release/2026/08/24/3349932/0/en/helium-10-launches-helium-the-commerce-ai-agent-that-helps-run-your-amazon-business.html), [Yahoo Finance syndication](https://finance.yahoo.com/technology/ai/articles/helium-10-launches-helium-commerce-145200456.html)
- **Explicitly analysis/recommendation-only at launch** — the vendor states plainly that "write execution capabilities" are coming "soon," i.e., **as of the August 2026 launch, Helium cannot take actions on the seller's account; it only recommends.** This is a clean, self-disclosed data point on maturity. — VERIFIED (vendor's own press release), same source.
- Also shipped a **Helium 10 MCP connector** exposing its Amazon dataset to Claude/ChatGPT directly — same pattern as Nova and Seller Labs: legacy analytics vendors are converging on "expose our data via MCP to whatever LLM client the seller already pays for" rather than building a proprietary agent runtime. — REPORTED, [Helium 10 MCP announcement](https://www.globenewswire.com/news-release/2026/08/24/3349932/0/en/helium-10-launches-helium-the-commerce-ai-agent-that-helps-run-your-amazon-business.html) (same release covers both)

### 1.13 Jungle Scout AI

- "AI Assist" powers listing generation, product research, review analysis, competitive intelligence (market-share tracking), sales analytics/forecasting, and listing audit/scoring across the existing Jungle Scout suite. — REPORTED, [Jungle Scout AI Review (BulkBase)](https://bulkbase.ai/review/jungle-scout-ai-review), [TechEra Jungle Scout Review 2026](https://techera.ai/jungle-scout/)
- No evidence of scheduled/autonomous agents, a goal/OKR layer, an approval-gate workflow, or write actions to Seller Central — this remains a research/optimization **tool**, not an operating agent, despite "AI" branding throughout. **Conclusion:** not a department-running candidate; a possible point tool inside the Catalog/Listing department.

### 1.14 Amazon's own "Seller Assistant" (agentic) and "Canvas"

- Amazon announced the agentic upgrade to Seller Assistant on **September 17, 2025**, rolling out through 2026: built on **Amazon Bedrock**, using both **Amazon Nova and Anthropic Claude** models. Rollout: US sellers from December 2025, EU/UK planned Q1 2026, "full autonomy features" targeted Q2 2026. — VERIFIED (official Amazon press release), [aboutamazon.com — Seller Assistant agentic AI](https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-agentic-ai)
- **Coverage:** five core capability areas — inventory optimization, account health, compliance, creative generation, growth strategy. It monitors FBA inventory in real time, flags slow-movers before long-term storage fees hit, recommends shipment plans, and alerts on missing compliance documents. — VERIFIED, same source; corroborated by [Digital Commerce 360](https://www.digitalcommerce360.com/2025/09/17/amazon-launches-agentic-ai-tools-to-automate-seller-operations/amp/)
- **Approval gate:** Amazon states explicitly that the assistant "never takes action on your account without explicit authorization," but the *form* of that authorization is configurable per action-category — "auto-approve" (authorize once, then it acts automatically going forward for that category) vs. "suggest only" (review every instance). Amazon's own guidance recommends starting all categories in suggest-only mode and only expanding auto-approve after 30+ days of observed quality. — REPORTED (multiple aggregator sources paraphrasing Amazon's guidance; the specific "30 days" recommendation was not found verbatim on an Amazon-owned page, so treat as REPORTED not VERIFIED), [Seller Sprite summary](https://www.sellersprite.com/en/blog/amazon-ai-seller-assistant-agentic-2026)
- **Canvas:** a visual extension launched March 2026 that renders interactive dashboards/scenario simulations in response to natural-language questions instead of text replies; **US marketplace only as of April 2026** (no CA availability confirmed — relevant since the operator's business is Amazon CA today). — REPORTED, [PYMNTS](https://www.pymnts.com/artificial-intelligence-2/2026/amazon-gives-sellers-an-agentic-window-into-their-business/)
- **Pricing:** Free, no premium tier, bundled into the "new Seller Central experience." — REPORTED, [Digital Commerce 360](https://www.digitalcommerce360.com/2025/09/17/amazon-launches-agentic-ai-tools-to-automate-seller-operations/amp/)
- **Critical limitations for this operator's use case:**
  1. It is Amazon-account-scoped only — it cannot manage Walmart (a stated future channel) or unify strategy/goals across marketplaces.
  2. It is a black box: no visibility into or portability of its "knowledge" (no equivalent of the operator's Mem0 wiki/playbook layer that the business would own and could take to a new platform or add human review of).
  3. No evidence it supports custom goal-setting/OKRs beyond its own built-in growth-strategy heuristics — it is Amazon's idea of what your business should optimize for, not the operator's.
  4. Canvas's US-only availability (as of the last confirmed date) means the operator's actual CA business may not even have access to the most advanced tier yet. **UNKNOWN** current CA rollout status as of Sept 2026 — worth a direct Seller Central check.
  5. Being Amazon's own tool, it is definitionally **not** usable for Walmart, and it is maximal platform lock-in by construction — the opposite of the operator's anti-lock-in requirement.
- **Real user reports:** none found in this search pass beyond vendor/press-release-adjacent coverage; genuine seller-forum sentiment is an **UNKNOWN** gap.

### 1.15 Notable 2026 entrant: Atomic One (atomic-one.com)

- Málaga, Spain-based startup; raised **€5.6M (~US$6.2M)** in a two-tranche round, publicly reported. — REPORTED, [EU-Startups](https://www.eu-startups.com/2026/07/malaga-based-atomic-one-raises-e5-6-million-to-automate-e-commerce-operations-with-ai-agents), [SaaSRise](https://www.saasrise.com/deals/malaga-based-atomic-one-raises-us62m-56m-to-automate-e-commerce-operations-with-ai-agents-b0074745-b75b-498c-9d64-586ed9d01cb6)
- Launched August 27, 2026: a system of **13 specialized AI agents** covering pricing, PPC, inventory, logistics, catalog management, competitive intelligence, ranking, and reviews, claiming to automate up to 80% of repetitive store-operations tasks; also shipped a free MCP-based query tool. — REPORTED (press release syndicated across multiple wire outlets, treat as vendor self-report), [GlobeNewswire](https://www.globenewswire.com/news-release/2026/08/27/3351833/0/en/atomic-one-launches-autonomous-ai-agent-system-to-run-daily-amazon-store-operations.html), [MarTechSeries](https://martechseries.com/sales-marketing/programmatic-buying/atomic-one-launches-autonomous-ai-agent-system-to-run-daily-amazon-store-operations/)
- This is architecturally the closest public description to the operator's own "company of departments" concept (multiple named specialist agents covering the full operational surface) — but it is brand-new (weeks old at time of writing), well-funded but unproven, with no independent user reviews, no published pricing, no stated approval-gate design, and no confirmed SP-API developer registration found in this search pass. **UNKNOWN** on all governance/compliance specifics — flagged as "watch" rather than "adopt now."

### 1.16 Summary table — Section 1 platforms

| Platform | Full-business scope? | Goals/OKRs? | Human approval gate? | API basis | Writes? | Pricing (as found) | Lock-in/export |
|---|---|---|---|---|---|---|---|
| Jarvio | Broad (ads, listing, inventory, CS, reviews) | Partial (goal-based PPC framing) | UNKNOWN | Advertising API (REPORTED) | Yes (claimed) | $49–~$1000s/mo, credit-based | UNKNOWN |
| Stormy AI | No (service-biz OS, not Amazon-native) | N/A | N/A | N/A | N/A | N/A | N/A |
| Autron | No (PPC only) | Bid-goal only | UNKNOWN | Amazon Ads API | Yes (bids) | $50/mo agent tier + higher managed tiers | UNKNOWN |
| Trellis | Partial (ads+pricing+content, multi-channel) | No evidence | UNKNOWN | Ads/Listings APIs (implied) | Yes | Not published (sales-led) | UNKNOWN |
| Threecolts/Seller 365 | Broad (bundle of legacy tools) | No | UNKNOWN | Mixed; some legacy tools risk scraping | Yes | $69–higher | UNKNOWN |
| Sellesta | Narrow, likely defunct | No | N/A | UNKNOWN | UNKNOWN | Was $0–$39/mo | N/A |
| SellerApp | Narrow (analytics+AI-assist) | No | N/A | UNKNOWN | No evidence | UNKNOWN | UNKNOWN |
| Nova Analytics | Data/intel layer only | No | N/A (read-only) | SP-API + Ads API, own MCP | **No (read-only)** | Promo free; steady-state UNKNOWN | Better — MCP + your own LLM client |
| DataDoe | Data/action layer + Skill Hub | No | Partial via skills (see §5) | SP-API-based Skills/MCP | Some (skills can act) | $97/mo flat (Hub) | Better — skills portable to Claude Code |
| AgentCentral | Data/action layer | No | "Guarded writes" (undocumented) | OAuth/SP-API-based MCP | Yes ("guarded") | UNKNOWN | Moderate |
| Seller Labs Genius | Broad bundle (reviews/PPC/profit) | No | UNKNOWN | Own APIs + MCP | Yes (PPC) | Free–$999.99/mo (revenue-tiered) | Moderate (MCP) |
| Helium 10 "Helium" | Broad (research/ads/commerce) | No | N/A (read-only at launch) | Own APIs + MCP | **No, yet** (launch-stated) | Bundled in existing plans | Moderate (MCP) |
| Jungle Scout AI | Narrow (research/listing tool) | No | N/A | UNKNOWN | No | Existing plan tiers | UNKNOWN |
| Amazon Seller Assistant/Canvas | Broad but Amazon-only | No custom goals | Yes, configurable per category | Amazon-internal (Bedrock) | Yes | Free | **Maximal lock-in**, Amazon-only, no Walmart |
| Atomic One | Broad (13 agents, full ops) | UNKNOWN | UNKNOWN | UNKNOWN (claims agentic, unverified) | Yes (claimed) | UNKNOWN | UNKNOWN |

## 2. Horizontal e-commerce operations AI (includes Amazon, but not Amazon-native)

**Headline finding: every horizontal platform surveyed is analytics/insight-first, with "agentic" features layered on top for the merchant's *own primary channel* (usually Shopify) — none runs Amazon operations end to end, and most have explicit, self-acknowledged Amazon blind spots.**

### 2.1 Shopify Sidekick / Magic

- Sidekick is Shopify's own conversational agent for merchants: takes natural-language instructions and executes multi-step store-management tasks — setting up discounts/promotions, drafting email campaigns, updating homepage banners, predicting stockouts of high-margin items, and suggesting supplier draft orders based on lead times. Magic handles content/copy generation; Sidekick is positioned as the "command and control" layer. — REPORTED, [Shopify Sidekick 2026 feature guide](https://wearepresta.com/shopify-sidekick-features-2026-the-merchants-guide-to-agentic-commerce/), [Shopify AI Toolkit 2026](https://blog.mastroke.com/shopify-ai/shopify-ai-toolkit-explained-how-smart-merchants-use-ai-agents-to-grow-faster-in-2026/)
- **Scope:** Shopify-store-native only. It has no Amazon Seller Central or SP-API integration by design — it operates on Shopify's own commerce graph. Irrelevant to running the Amazon business directly; only relevant if/when the operator adds a Shopify DTC storefront. **Runs operations, not just analytics — but only for Shopify.**

### 2.2 Triple Whale / Moby (Moby 2, "Moby Agents")

- Moby 2 (launched May 2026) is built on Triple Whale's "Context Engine," trained on 60,000+ Shopify brands, and can take autonomous action across ad platforms and marketing channels — configurable "Moby Agents" choose datasets, pull in web search, run marketing-mix-modeling/forecasting, and push insights/actions on a schedule to chosen destinations. — REPORTED, [Triple Whale — Meet Moby 2](https://www.triplewhale.com/blog/moby-2), [Moby Agents](https://www.triplewhale.com/moby-agents)
- **Amazon is an explicit, self-acknowledged blind spot:** "Triple Whale sees only what Shopify sees; multi-channel brands hit visibility gaps on Amazon, wholesale, and retail," and while Amazon sales *can* be pulled in, "many functionalities do not take this sales channel into consideration, making it hard to consolidate information." — REPORTED, [Saras Analytics comparison](https://www.sarasanalytics.com/blog/saras-iq-vs-triple-whale-moby-ai)
- **Conclusion:** runs real operations (ad execution) autonomously, but for the wrong channel for this operator; not usable as an Amazon department-runner.

### 2.3 Sellerboard

- A pure profit-analytics tool: pulls Amazon fees, FBA costs, ad spend, refunds via the Amazon API; user supplies COGS; calculates true per-order/per-SKU/per-campaign net profit. Adds review-request/follow-up email automation as a bolt-on. $15–19/mo. 1-month free trial. — REPORTED, [Sellerboard review (BagEngine)](https://bagengine.com/articles/sellerboard-review), [Sellerboard pricing (TrakSource)](https://traksource.com/sellerboard-review/)
- **No agentic/operational layer found** — this is analytics-only, plus one automation feature (review requests). Not a candidate for running departments; a legitimate cheap point-tool for the Finance/Profit-visibility slice, and notably far cheaper than building/maintaining a custom profit_daily pipeline if the operator ever wanted a second opinion or backup.

### 2.4 Peel, Daasity, Northbeam, Polar Analytics, Lifetimely

- **Daasity:** raw multi-channel data access and custom modeling (Shopify + Amazon + wholesale) — a data warehouse/BI layer, not an operating agent. — REPORTED, [Luca AI: Daasity alternatives roundup](https://ask-luca.com/blogs/daasity-alternatives)
- **Northbeam:** measurement-grade multi-touch ad attribution — an analytics tool, DTC-ad-focused, not Amazon-operational. — REPORTED, [Luca AI: ecommerce analytics dashboard roundup](https://ask-luca.com/blogs/ecommerce-analytics-dashboard)
- **Polar Analytics:** dedicated Snowflake warehouse, consistent cross-channel metrics, customizable BI dashboards, and "specialized AI agents for profit, LTV, and automated reporting" — REPORTED, [Polar Analytics Review 2026](https://www.aisystemscommerce.com/post/polar-analytics-review-2026-warehouse-native-ecommerce-intelligence-omnichannel-brands) — but these "agents" are reporting/insight agents, not action-takers; no evidence of write-back to Amazon.
- **Lifetimely:** profit/customer-analytics for Shopify **and Amazon**, real-time net profit, P&L, LTV, predictive cohorts, and a "Profit Agent" that flags risks/opportunities. — REPORTED, [Finsi.ai: Lifetimely alternatives](https://www.finsi.ai/blog/lifetimely-alternatives-7-best-subscription-analytics-tools-for-2026/) — closest of this group to being genuinely Amazon-aware, but still an alerting/insight agent, not an action agent (no PPC bid changes, no restock POs, no pricing writes documented).
- **Peel:** cohort/retention analytics; no Amazon-specific operational claims found. **UNKNOWN** depth of Amazon support.
- **Verdict for Section 2 as a whole:** Every horizontal platform surveyed either (a) runs real autonomous actions but only for Shopify/DTC advertising (Shopify Sidekick, Triple Whale Moby), or (b) is Amazon-aware but analytics/alerting only (Sellerboard, Lifetimely, Polar, Daasity, Northbeam, Peel). **None of them is a candidate to run Amazon departments end to end.** Their only relevance to this operator is as potential off-the-shelf analytics/finance point-tools (Sellerboard and Lifetimely are the two worth a cost/effort comparison against the custom `sales_daily`/`profit_daily` pipeline already built) or as the eventual DTC layer if a Shopify storefront is added.

---

## 3. Agencies and "fractional AI ops" services (pricing benchmark)

**Framing:** the operator is essentially building the in-house equivalent of what full-service Amazon management agencies charge for — useful as a cost/opportunity-cost anchor, not because the operator should switch to one now.




| Service type | Typical fee (2026) | Notes | Source |
|---|---|---|---|
| Full-service Amazon account management (ads+listing+inventory-aware pacing+reporting) | $2,000-$7,000/mo (mid-market); $3,000-$12,000/mo for established 7-figure brands | Growing brands ~$3,500-$6,000/mo; larger brands $6,000-$12,000/mo | REPORTED, [MyAmazonGuy](https://myamazonguy.com/amazon-account-management/amazon-account-management-cost-for-brands/), [Dark Room Agency](https://www.darkroomagency.com/observatory/amazon-ppc-management-cost-2026) |
| Percentage-of-revenue full management | ~5% of total Amazon revenue | E.g., $25,000/mo on $500k/mo in sales; criticized because it ignores margin (agency is incentivized to grow revenue even at low margin) | REPORTED, [SupplyKick](https://www.supplykick.com/blog/amazon-agency-pricing) |
| Hybrid retainer + performance | e.g., $3,500/mo base + 4% of monthly sales above $400k | Increasingly common vs. pure % models | REPORTED, [SalesDuo](https://salesduo.com/blog/amazon-agency-pricing/) |
| PPC-only management (flat fee) | $1,500-$8,000/mo for growing brands | Scales with ASIN count, marketplaces, reporting depth | REPORTED, [SalesDuo PPC guide](https://salesduo.com/blog/amazon-ppc-management-cost-agency-fees/) |
| PPC-only management (% of ad spend) | 10-20% of monthly ad spend | Common alternative to flat fee | REPORTED, [PPC Jumpstart](https://ppcjumpstart.com/amazon-ppc-agency-cost/) |
| Pacvue (software, not agency) | ~$500/mo minimum, or 3-4% of ad spend | Software tool pricing, cited as PPC-cost benchmark | REPORTED, [SellerStack: flat-fee vs pct-of-spend](https://www.sellerstack.ai/blog/amazon-ppc-flat-fee-vs-percent-of-spend) |
| Perpetua (software, not agency) | ~$250-$550/mo base (up to $695) + ~3% above $10k spend | Same category as Pacvue | REPORTED, same source |
| Fractional Amazon "operator"/COO-style team | $5,000-$25,000/mo | Builds back-end systems (order-to-payout reconciliation, multi-channel inventory orchestration, supplier/3PL management, weekly ops rhythm) rather than owning traffic/conversion — closer to what this operator is automating internally | REPORTED, [Kamyar Shah: Fractional COO vs Amazon Agency](https://kamyarshah.com/fractional-coo-vs-amazon-agency-which-you-need/) |
| Fractional CFO for Amazon sellers | Not itemized in search results | Distinct niche service for financial modeling/forecasting | REPORTED, [Eightx: Best Fractional CFO for Amazon Sellers](https://eightx.co/blog/compare/best-fractional-cfo-for-amazon-sellers) |

**Benchmark takeaway:** at $10k/mo revenue today, the operator is far below the size where any agency or fractional-ops arrangement makes economic sense (a $2,000+/mo minimum agency retainer would consume 20%+ of revenue). At the $85k/mo target, a full-service agency (~$3,500-$8,000/mo) or a 5%-of-revenue arrangement (~$4,250/mo) becomes a real, comparable alternative to the Hetzner+Claude stack, whose own AI cost target is $25-70/mo infra+AI (per this project's cost projections) plus the operator's own time. This is the actual "build vs. buy vs. hire" frontier to revisit once US launch materially increases revenue — not today.

---

## 4. Top 3 candidates vs. requirements — detailed comparison

Selection rationale: of everything surveyed in Section 1, three platforms come closest to the operator's actual ask — "a system that holds strategy and runs the whole business toward it" — rather than being a single-department point tool or a pure data/analytics layer:

1. **Jarvio** — broadest documented department coverage (PPC, listings, inventory, competitors, reimbursements, reviews, reporting) under one product, with a visible workflow-builder and an explicit "goal-based" framing, and the largest claimed installed base (2,000+ brands).
2. **Amazon Seller Assistant (agentic) + Canvas** — the deepest data access of any candidate (native Seller Central integration, Bedrock/Nova/Claude-powered), free, and the only one with a *publicly documented* configurable approval-gate model (auto-approve vs. suggest-only per action category).
3. **Atomic One** — the newest and architecturally closest to the operator's own "company of departments" concept: 13 named specialist agents spanning pricing, PPC, inventory, logistics, catalog, competitive intelligence, ranking, and reviews, marketed explicitly as running the operations end to end.

(DataDoe and AgentCentral were excluded from this top-3 because, per their own positioning, they are Tier-0 **data/action layers** for an LLM the operator brings — closer in kind to what this operator already built with `sync/` + Supabase than to a rival finished "OS." DataDoe gets its own dedicated evaluation in Section 5 per the brief.)

### 4.1 Requirements comparison table

| Requirement | Jarvio | Amazon Seller Assistant + Canvas | Atomic One |
|---|---|---|---|
| Holds strategy/goals across departments | Partial — "goal-based PPC" framing exists for ads; no evidence of a unified cross-department OKR/strategy object that ties inventory, pricing, ads, and expansion to one set of business goals. REPORTED | No — optimizes to Amazon's own built-in growth heuristics per capability area, not user-defined strategic goals. REPORTED | UNKNOWN — marketing claims "orchestration" across 13 agents but no evidence of an explicit goal/OKR object found; too new to have documentation depth |
| Runs all departments (finance, supply chain/restock, ads, catalog, pricing, customer, compliance, expansion) | Most departments covered except a dedicated finance/P&L module and no expansion/new-market planning. REPORTED | Inventory, account health, compliance, creative/catalog, growth strategy — 5 areas; no PPC bid management, no finance/P&L, no customer-service module documented. VERIFIED (Amazon's own announcement) for the 5 areas named |Widest claimed coverage of the three — pricing, PPC, inventory, logistics, catalog, competitive intel, ranking, reviews — but no finance or explicit compliance/expansion agent named. REPORTED |
| Works unattended on a schedule | Yes — workflow automation runs continuously once activated. REPORTED | Yes — "always-on agentic partner," monitors continuously. VERIFIED (Amazon press release) | Claimed ("operates around the clock"). REPORTED |
| Creates tasks/decisions for human review | Yes for some flows (e.g., flags buyer messages needing human review; reimbursement claims are prepared but the human submits them through Seller Central — i.e., a manual step is retained specifically for the money-adjacent action). REPORTED | Yes, per action-category, configurable. VERIFIED | UNKNOWN — no documented task/decision-queue mechanism found |
| Human approval gate on money specifically | Workflow builder lets you review/edit a workflow *before activating* it — this is pre-approval of the automation's logic, not a per-transaction approval gate on each individual financial action. This is a materially weaker guarantee than the operator's `approval_requests` model (every single price/bid/PO change gated, not just the workflow template). UNKNOWN/weak-REPORTED | Yes, and the closest of the three to the operator's own architecture: configurable auto-approve vs. suggest-only *per action category*, with Amazon's own guidance to start conservative. VERIFIED/REPORTED (mechanism verified, specific 30-day guidance only REPORTED) | UNKNOWN — no public documentation of an approval mechanism found at all |
| Official APIs only (no scraping/browser automation) | Uses Amazon Advertising API for ads (REPORTED); overall architecture for pricing/listing/inventory writes not documented — UNKNOWN whether 100% SP-API-based | By definition — it's Amazon's own internal system, not a third party touching SP-API at all | UNKNOWN — no statement of API basis found; given the March 2026 policy, this is the single most important unresolved question before ever connecting a real account |
| Avoids vendor lock-in (data/playbook portability) | No public export/portability statement found. UNKNOWN | **Worst of the three by construction** — Amazon-only, cannot ever manage Walmart, no way to export its "knowledge" to another system. VERIFIED by definition (it is Amazon's own tool) | No public statement found. UNKNOWN |
| Multi-marketplace (Walmart-ready) | Some multi-tool ecosystem claims (Trellis-style competitors do explicitly cover Walmart) but not confirmed for Jarvio specifically. UNKNOWN | No — Amazon-only, structurally impossible to extend to Walmart | UNKNOWN — no Walmart mention found in available material |
| Uses operator's existing subscriptions (Claude Max/ChatGPT) | No — Jarvio is billed and metered independently (credits), not "bring your own LLM subscription." VERIFIED (pricing model is Jarvio's own credits, not pass-through LLM usage) | No — runs on Amazon's own Bedrock-hosted Claude/Nova, not the operator's Claude Max account | No — presumably its own backend LLM cost bundled into its (undisclosed) pricing |
| Pricing at $10k/mo revenue today | $49/mo entry tier is affordable now | Free | Undisclosed — likely priced for larger accounts given its VC-funded managed-service framing |
| Real user reports found | Vendor review-site coverage only in this pass; no independent forum/Reddit sentiment surfaced | Too new (rollout still completing through 2026); no independent seller-forum sentiment surfaced in this pass | None — product is weeks old |

### 4.2 Honest verdict on buy vs. build, per candidate

- **Jarvio:** The most "feature-complete against the department list" of the three, and cheap enough to trial at the operator's current revenue. But its approval model is a **workflow-level review, not a transaction-level approval gate** — this fails the operator's hard "no financial action without explicit human approval, every time" requirement as stated, unless Jarvio's enterprise tier has an undocumented stronger control the marketing pages don't show. It also does not use the operator's existing Claude Max subscription (separate metered cost) and has no confirmed data-portability story. **Verdict: not a replacement for the department layer as specified; at most worth a side-by-side trial as a possible off-the-shelf PPC/listing module while keeping the custom Executor as the only thing with SP-API write credentials** — which would mean *not* actually giving Jarvio write access, defeating much of its value proposition. Net: **do not buy to replace; not worth complicating the architecture to partially adopt either.**
- **Amazon Seller Assistant + Canvas:** Free, deeply integrated, and the only candidate with a genuinely documented, configurable, per-category approval gate — architecturally validating the operator's own design instinct (the operator's `approval_requests` table is philosophically the same idea Amazon itself converged on). However, it is Amazon-only by construction, cannot follow the business to Walmart, has zero portability of accumulated "knowledge" (no equivalent to the operator's Mem0/wiki compounding layer that the business itself would own), and optimizes to Amazon's own definition of seller success rather than the operator's specific goals (e.g., margin thresholds, seasonal playbooks unique to Middle Eastern grocery demand). **Verdict: complement, always-on, for free** — there is no reason not to have it running in "suggest-only" mode as a second set of eyes/cross-check on inventory and compliance, since it costs nothing and adds a redundant safety net, but it cannot be the business's brain and must never be treated as a source of truth the way Supabase/Mem0 are.
- **Atomic One:** The closest published vision to "a company of AI departments" — same shape as this project's own architecture, potentially validating the overall approach as directionally correct in the market. But it is a **weeks-old product from a startup with no independent reviews, no disclosed pricing, no disclosed approval-gate mechanism, and no confirmed SP-API-only compliance posture** — adopting it now would mean handing account access to an unproven black box at exactly the moment Amazon has raised the compliance bar for automated tools. **Verdict: watch, do not adopt.** Worth a re-evaluation in 6–12 months once it has a track record, disclosed pricing, and (ideally) SOC2/compliance documentation comparable to what DataDoe already publishes.

**Cross-cutting conclusion for Section 4:** none of the three top candidates satisfies the full requirement set (goals+all departments+scheduled+task creation+hard per-transaction approval gate+official-APIs-only+no lock-in+reuse of existing Claude Max/ChatGPT subscription) simultaneously. The two that are safe to run today (Jarvio's cheap tier, Amazon's free Seller Assistant) are safe *because* they are narrower or generic, not because they are equivalent replacements for the custom system. This supports "build, with selective complements," not "buy."

---

## 5. DataDoe as a possible Tier-0 orchestrator for read-only departments

**Framing:** the brief asks specifically whether DataDoe's own scheduled agents + Skill Hub could serve as the read-only "Tier 0" control plane — i.e., not replacing the agent layer's reasoning, but replacing/complementing the sync+scheduling plumbing the operator built by hand (`sync/scheduler.py`, cron, Supabase sync jobs) with a managed equivalent that a solo operator doesn't have to run on a Hetzner box.

### 5.1 What DataDoe actually provides — verified/reported capabilities

- **Data layer:** DataDoe is "an Amazon Data & Action Layer for AI" exposing Seller Central, Vendor Central, and Ads data through both a hosted **MCP server** and a **REST API**, aimed at agencies and sellers wiring AI clients (Claude, ChatGPT) directly to live Amazon data. — REPORTED, [DataDoe Platform](https://www.datadoe.com/platform), [Amazon Seller MCP Server](https://www.datadoe.com/connect/amazon/mcp)
- **Skill Hub:** 47+ pre-built "skills" — packaged prompt/workflow definitions installable directly into **Claude Code, Codex, or OpenClaw** — covering things like organic/sponsored search visibility audits and 2026-tuned listing optimization checks. This is architecturally the same "Skill" concept as Claude's own Skills format, meaning these could plug directly into the same Claude Code environment this project already runs in. — REPORTED, [DataDoe Hub](https://www.datadoe.com/hub)
- **Scheduling:** DataDoe explicitly supports **async scheduled agents** that run tasks against live data on a cadence without a human initiating each run — the examples given are overnight reorder forecasts delivered by 8am, weekly P&L briefs, and anomaly alerts when a SKU's margin/performance drops. For agencies, this extends to scheduled per-client weekly/monthly/quarterly reports. — REPORTED, [DataDoe Hub](https://www.datadoe.com/hub)
- **Delivery/alerting:** Outputs are auto-sent to **Slack** or inbox/email on schedule — this directly answers the brief's question ("can DataDoe schedule prompts, alert to Slack, and run skills unattended?") — **yes to all three, per the vendor's own description.** — REPORTED, same source.
- **Writes / approval gate:** Separately from the Skill Hub, DataDoe's "Actions" feature supports natural-language write requests to the Amazon account, but every write is **validated, dry-run-previewed, and requires explicit approval before execution**, with a full audit log — a materially more rigorous, and better-documented, approval gate than anything found for Jarvio or Atomic One, and structurally similar in spirit to the operator's own `approval_requests` table + Executor pattern. — REPORTED, [OpenPR: DataDoe surpasses 500 Amazon businesses](https://www.openpr.com/news/4584105/datadoe-surpasses-500-amazon-businesses-using-ai-to-read-data), [DataDoe Platform](https://www.datadoe.com/platform)
- **Compliance posture:** DataDoe states its handling of Amazon data aligns with the SP-API Data Protection Policy and that it participates in Amazon's data-protection assessment process; it publishes security controls referencing ISO 27001/27002 and NIST CSF, encryption in transit (TLS 1.3) and at rest (AES-256-GCM), MFA, least-privilege IAM, and secrets management — considerably more compliance documentation than any other vendor surveyed in Section 1 (most had none publicly available at all). — REPORTED, [DataDoe DPA](https://www.datadoe.com/legal/data-processing-agreement)
- **Pricing:** Flat $97/mo for the Hub tier (per Section 1.9 finding). — REPORTED, [DataDoe Hub](https://www.datadoe.com/hub)

### 5.2 Is it a viable Tier-0 control plane for read-only departments?

**Yes, plausibly, for the read/observe/alert slice — with real caveats.** DataDoe's scheduled-skill-plus-Slack-alert model could, in principle, take over some of what this project's `sync/scheduler.py` + cron + notification-writing does today: pulling SP-API/Ads data on a cadence, running a packaged analysis skill against it, and pushing an alert or brief to a channel — all without the operator maintaining that plumbing on the Hetzner box. Because the Skill Hub format targets Claude Code directly, skills could sit alongside this project's own agents rather than requiring a rewrite, and the documented dry-run/approval/audit pattern on writes is the best-evidenced version of the operator's own safety invariant found anywhere in this survey.

### 5.3 What it explicitly cannot do (per the brief's ask, and per available evidence)

1. **No cross-department strategic goals/OKR layer.** DataDoe's skills are discrete, scoped procedures ("audit search visibility," "optimize a listing") — there is no evidence of a persistent goal object that ties inventory targets, ad ACOS targets, margin floors, and expansion timing together the way the operator's L1 rules + Mem0 playbook tiers are designed to. It is a data/execution layer, not a strategy layer. **UNKNOWN/gap confirmed.**
2. **No native approval workflow spanning *all* department types simultaneously** — the Actions/approval-gate evidence found is Amazon-account-write-specific; there's no documented unified approval queue that would, e.g., also gate a Walmart price change or a supplier PO the same way, because DataDoe's scope is Amazon-only per its own positioning (Seller/Vendor/Ads).
3. **No cross-department shared state/memory equivalent to Mem0.** Skills appear to be stateless, scoped procedures run on a schedule — there's no evidence of a compounding-knowledge layer (patterns → playbooks, confidence scoring, promotion over time) that this project's architecture treats as its core differentiator ("knowledge compounds"). Using DataDoe as Tier-0 would still require the operator's own Mem0 + Supabase to be where the *knowledge* accumulates; DataDoe would only be feeding it or bypassing it entirely for one-off Slack alerts.
4. **Not multi-marketplace beyond Amazon** — no Walmart mentioned anywhere in DataDoe's material found; the operator's eventual Walmart layer would need its own sync path regardless.
5. **Governance is Amazon-account-scoped, not business-scoped** — it does not know about the operator's finance/compliance/customer domains beyond what Amazon APIs expose (i.e., no bank reconciliation, no supplier contract terms, no customer-service ticketing beyond Amazon's own Buyer-Seller Messaging).

### 5.4 Verdict on DataDoe

**Complement, specifically at Tier 0 (data ingestion + scheduled read-only alerts), not a control plane for goals or approvals.** It is a legitimate, comparatively well-documented candidate to reduce or replace the *sync/scheduling plumbing* burden on a solo operator (the part of this project's own architecture most exposed to "if it needs babysitting, it's wrong" — cron jobs on a CX22, retry logic, log rotation) for the read-only pieces, freeing the operator's own agent layer to focus on reasoning and the approval-gated write path it must keep sole control of. It should **not** be trusted as the place where goals live, where approvals are unified across departments, or where cross-domain knowledge compounds — those remain squarely the job of the custom Supabase + Mem0 + BaseAgent architecture already built. A reasonable adoption pattern, if pursued, would be: keep DataDoe's Skill Hub for supplementary/cross-check read-only alerts (e.g., a second, independently-sourced "search visibility audit" skill run weekly to sanity-check the Listing & Competitor Intel Agent's own findings) without routing any DataDoe-originated action anywhere near the Executor's approval queue.

---

## 6. Overall verdict: buy, complement, or build

**Build — with two narrow, no-regret complements; nothing surveyed should replace the department layer or the approval gate.**

- **Build (confirmed as the right call):** No single platform surveyed satisfies the full requirement set — persistent cross-department goals, all eight named domains, unattended scheduling, task/decision creation, a hard per-transaction human-approval gate on money, official-APIs-only compliance, freedom from lock-in, and reuse of the operator's existing Claude Max subscription. The closest attempts (Jarvio, Atomic One) are commercial products the operator would be paying to re-architect around, with weaker or undocumented approval guarantees than the `approval_requests`/Executor pattern already implemented. Amazon's own Seller Assistant validates the overall design pattern (Bedrock+Claude, configurable approval gates, scheduled monitoring) but is definitionally single-marketplace and non-portable — proof the approach is sound, not a substitute for it.
- **Complement 1 — Amazon Seller Assistant (agentic), suggest-only mode, free:** run it alongside the custom Inventory and Listing/Competitor agents as a zero-cost second opinion, never as a write path and never as the system of record.
- **Complement 2 — DataDoe Skill Hub, at Tier 0, read-only:** consider it (or evaluate AgentCentral as its direct competitor) as a managed alternative to hand-rolled SP-API sync/scheduling plumbing for supplementary alerts, keeping all financial writes exclusively inside the existing Executor.
- **Revisit trigger:** the agency/fractional-ops pricing benchmark in Section 3 becomes economically comparable only once monthly revenue is well into the tens of thousands (the $85k/mo target, not the $10k/mo starting point) — that is the point to re-run this survey, not before, and specifically to re-check Atomic One's maturity and Jarvio's approval-gate documentation at that time.
