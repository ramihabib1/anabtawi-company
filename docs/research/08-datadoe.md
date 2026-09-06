> Research report produced 2026-09-06 during the founding engagement. Where it mentions files of an earlier repository, treat those as context the researcher had, not as part of this design. The design that governs is docs/ANABTAWI-OS-DESIGN.md.

# 08 — DataDoe as the Amazon data and action layer

Research date: 2026-09-06. Author: research agent. Audience: Rami.

## 0. Method and a hard access caveat — read this first

**`datadoe.com`, `www.datadoe.com`, `mcpmarket.com`, `deltologic.com` and `advertising.amazon.com` are all blocked by this environment's network egress proxy.** I could not open a single DataDoe-hosted page today. I tried direct fetch on `datadoe.com`, `www.datadoe.com`, and the vendor's parent-company blog at `deltologic.com`; every one returned `EGRESS_BLOCKED`.

So the evidence tiers in this report are:

- **VERIFIED** — I opened the page today and it said so. In practice this means `github.com` and `raw.githubusercontent.com` pages in DataDoe's own two public repositories (`Deltologic/datadoe-mcp`, `Deltologic/datadoe-ai-skills`). These are vendor-authored primary artifacts — the MCP schema facade and the actual `SKILL.md` files their agents run — and are the strongest evidence in this report.
- **REPORTED** — the claim comes from DataDoe's own marketing pages (`datadoe.com/pricing`, `/platform`, `/faq`, `/changelog`, `/enterprise`, `/legal/terms-of-service`, `/hub`) reached through a search index that summarised those pages for me, or from third-party coverage. I never rendered the page myself. **Treat every REPORTED number as a vendor claim to be checked in the app, not as fact.** Where two sources disagreed I say so.
- **UNKNOWN** — could not confirm; I say what I tried.

Deltologic (the Polish SP-API consultancy that builds DataDoe) also publishes comparison blog posts about its own product. Those are marketing, and I have tagged them REPORTED and attributed accordingly. Do not weigh "DataDoe completed 29/30 tasks, Amazon 19/30" as independent evidence.

The single most useful thing Rami can do after reading this is to open his own DataDoe account and answer the twelve UNKNOWNs in §12.

---

## 1. What DataDoe is

DataDoe is a hosted Amazon data warehouse plus a hosted MCP server plus a write-action gateway, sold as one subscription. It holds an Amazon-approved SP-API and Ads API developer application, does the OAuth dance with your Seller/Vendor/Ads accounts, pulls the reports on a schedule into a BigQuery layer, normalises them into flat tables, and exposes those tables — plus a set of write actions — over MCP, REST and direct BigQuery. (REPORTED — datadoe.com/platform, /platform/data-layer; VERIFIED for the MCP tool surface, see §3.)

The strategic point for this company: **it removes the SP-API private developer registration from the critical path.** Rami does not have that registration and does not want to maintain it. DataDoe's Amazon app is the one that is registered, audited, and rate-limited. (REPORTED — datadoe.com/connect/amazon/mcp: "no SP-API project or code required"; VERIFIED indirectly — the `datadoe-mcp` README states the service handles developer registration, OAuth and rate limiting.)

The vendor is Deltologic. The product's public GitHub org is `Deltologic`. (VERIFIED — https://github.com/Deltologic/datadoe-mcp.)

---

## 2. Commercials (all REPORTED, all dated 2026-09-06, all to be re-checked in the app)

| Item | Claim | Source |
|---|---|---|
| Price | **USD 97/month**, one plan, 14-day free trial | datadoe.com/pricing |
| Accounts | Unlimited Seller, Vendor and Ads connections — never billed per account | datadoe.com/pricing |
| Marketplaces | All Amazon marketplaces incl. CA and US on the same subscription | datadoe.com |
| Data rows | 10M rows included; extra 5M blocks purchasable in-app | datadoe.com/pricing |
| Seats | Extra user seats purchasable in-app; count included per plan **UNKNOWN** | datadoe.com/pricing |
| "AI tokens" | Included allowance per month — **sources conflict: 1,500 vs 2,000 (doubled to 4,000 for first 3 months)** | datadoe.com/pricing vs datadoe.com/faq |
| Token overage | USD 0.04 per token, capped at a spending limit you set; **default limit is $0**, so no overage unless you opt in | datadoe.com/faq |
| What burns tokens | Exports, Actions (writes), BigQuery queries, webhook deliveries | datadoe.com/faq |
| Action cost | **2 tokens per action** for up to 100 entities, +1 token per additional 100 entities | **VERIFIED** — Deltologic/datadoe-mcp README |
| Enterprise | Separate tier: SSO, RBAC, unlimited seats, EU-hosted option, negotiated uptime | datadoe.com/enterprise |
| SLA | **Standard plans have no SLA**; enterprise may negotiate one | datadoe.com/legal/terms-of-service |

Commercial read: at USD 97/month flat for unlimited accounts and marketplaces, DataDoe is the cheapest thing in this design by a wide margin, and it is the *only* item whose price does not scale when the US marketplace and a second brand arrive. That is unusually well-matched to the plan. The token meter is the variable, and the $0 default spending limit means the failure mode is "agent runs out of tokens and stops", not "agent runs up a bill" — which is the right failure mode for an unattended system. Confirm that default is actually $0 on day one.

**Cost discipline note:** a naive agent that calls `exports_create` for every question will burn tokens fast. The departments must cache exports into the repo (`state/`, `ledger/kpis.csv`) and re-read the file, not re-export. Budget for this explicitly in each department's skill.

---

## 3. The MCP server — what an agent actually gets

Endpoint and auth (VERIFIED — Deltologic/datadoe-mcp README):

```json
{ "mcpServers": { "datadoe": {
  "url": "https://mcp.datadoe.com/mcp/v1",
  "headers": { "datadoe-mcp-key": "<YOUR_DATADOE_MCP_KEY>" } } } }
```

This matches what is already in `departments/*/.mcp.json` in this repo. Good.

**Complete MCP tool surface (VERIFIED — Deltologic/datadoe-mcp README):**

| Category | Tools |
|---|---|
| Account | `sellers_and_vendors_list`, `organization_and_subscription_details_get` |
| Data | `exports_sources_get`, `exports_create`, `exports_get`, `exports_list`, `exports_raw_url_get`, `exports_raw_download`, `exports_delete` |
| Files | `files_create`, `files_list`, `files_get`, `files_download_url_get`, `files_delete` |
| **Actions** | `actions_details_schema_get`, `actions_start`, `actions_get`, `actions_list` |
| COGS / Vendor | `cogs_upsert`, `cogs_delete`, `vendor_code_upsert`, `vendor_code_delete` |
| Docs & Plugins | `datadoe_user_docs_table_of_contents_get`, `datadoe_user_docs_page_get`, `plugins_get`, `plugins_memories_create`, `plugins_memories_edit`, `plugins_skills_get`, `plugins_files_get` |

Three observations that matter for the design:

1. **The whole read layer is one tool, `exports_create`**, taking a source table plus columns, filters, sort, date range and output format. It is a SQL-shaped tool, not 114 typed tools. That is good for token economy and bad for discoverability — the agent must first call `exports_sources_get` to learn the table and column names. Every department skill should hard-code the table and column names it needs so the agent does not spend a turn discovering them.
2. **`cogs_upsert` is a first-class MCP tool.** Finance's charter already says "keep COGS current in DataDoe through its COGS tool after every executed PO" — that is exactly right, and it is the one write DataDoe accepts that is not an Amazon write. COGS lives in DataDoe, so DataDoe's profit tables are only as true as our PO discipline.
3. **`plugins_memories_create` / `plugins_memories_edit` exist** — DataDoe has its own memory store. **Do not use it.** The constitution says nothing important lives outside this repo. Memory belongs in `memory/`. (Rule of the company, §2.)

Rate limits (REPORTED — datadoe.com/faq): no rate limit on DataDoe's own data layer; DataDoe absorbs Amazon's SP-API limits server-side. One real cap: **exports are 2,500 rows per call, paginate with `skip`.** For ~60 SKUs across two marketplaces that is rarely binding, except for order-line and search-term pulls, which will paginate.

API keys and scopes (REPORTED — datadoe.com/solutions/amazon/developers): keys are org-scoped, revocable at `app.datadoe.com/integrations/mcp`, and carry **per-key scopes for data domains, tables and fields**. If true this is the single most important control in the whole product for us — see §7 and §12.

---

## 4. Data coverage, refresh, history

**Coverage** (REPORTED — datadoe.com/platform, /platform/data-layer, /changelog): "100+ normalized tables", elsewhere "114 clean tables", across Seller Central, Vendor Central and Amazon Ads, unifying six Amazon APIs plus Amazon Marketing Stream and restricted-PII reports.

| Domain | Present? | Evidence |
|---|---|---|
| Orders, order lines, refunds | Yes | REPORTED + implied by skills |
| Settlements, fees, reserves | Yes | REPORTED — /platform |
| Profit by Date, Profit by SKU & Date (sales+traffic+PPC+fees+COGS+profit in one table) | Yes, added 2026 | REPORTED — /changelog |
| FBA inventory + **`amazon_fba_inventory_health`** (available, inbound, days of supply, recommended ship qty/date) | Yes | **VERIFIED** — restock-priority-alert SKILL.md |
| FBA inbound shipments (full table) | Yes | REPORTED — /changelog |
| Inventory ledger (unit movement) | Yes | REPORTED — /platform |
| Listings / catalog / listing issues / suppressed | Yes | REPORTED + implied by suppressed-inactive-listings-check skill |
| Buy Box / Featured Offer | Yes | REPORTED + buy-box-loss-root-cause skill |
| Brand Analytics search terms (daily/weekly/monthly, search+click+conversion share) | Yes | REPORTED — /changelog |
| Search Query Performance (weekly) | Yes | REPORTED — /hub keyword tracker; **VERIFIED** skill name `keyword-rank-sqp-tracker` |
| Ads: SP / SB / SD, campaigns / ad groups / ads / targets, search terms by campaign by date | Yes | **VERIFIED** — `amazon_ads_search_terms_by_campaign_by_date`, "Keyword Targeting Performance" export |
| Ads: DSP raw, TV | Yes (DSP raw added 2026) | REPORTED — /changelog |
| Returns + reason codes, FBA vs FBM | Yes | REPORTED — /changelog |
| **`amazon_seller_performance`** — AHR, ODR, late shipment, cancellation, valid tracking, on-time delivery, six policy-violation categories, with Amazon's own target thresholds as columns | Yes | **VERIFIED** — daily-account-health-check SKILL.md |
| Promotions and Coupons performance (Seller + Vendor) | Yes, added 2026 | REPORTED — /changelog |
| Vendor Central (real-time + reports) | Yes | REPORTED |
| Restricted PII (buyer data) via Amazon RDT | Yes, gated | REPORTED — /faq, /blog-posts/amazon-sp-api-restricted-pii |
| Customer reviews | Claimed in third-party comparison, **not confirmed on a DataDoe page** | REPORTED (weak) — deltologic.com top-10 post |
| **Walmart, Shopify** | **Not available. "Coming soon"; enterprise-only custom integration today.** | REPORTED — datadoe.com/integrations, /enterprise |
| Keepa-style competitor price/rank history | **No** | absence of evidence across all pages |
| QuickBooks / accounting | **No** | absence of evidence |
| Supplier POs / landed cost | **No** | absence of evidence |

**Refresh** (REPORTED — /changelog, /faq): daily fetch starts 02:00, most tables ready ~05:00 marketplace time; selected tables refresh intraday; orders update intraday *and* via live SP-API notifications and Amazon Marketing Stream.

This is the single most operationally important number in the report and it lands well: the constitution's departments run 06:00–07:00 Asia/Jerusalem against an Amazon business day that closes at 07:00 local. If "05:00 marketplace time" means 05:00 in the *marketplace's* timezone, then for amazon.ca (America/Toronto, UTC−4/5) that is roughly 12:00 Asia/Jerusalem — **i.e. yesterday's Canadian data may not be complete when Finance runs at 06:00 Jerusalem.** This is a real scheduling risk and it is UNKNOWN whether "marketplace time" means marketplace-local or account-local. **Rami must check the actual freshness timestamp in his account at 06:00 Jerusalem before the schedules are trusted.** If it does not clear, either move the daily runs later or have each department read the max date in the table and refuse to report on an incomplete day (which the constitution's rule 8 already implies).

**History**: up to **735 days backfilled on connect**, then retained from the connect date forward. (REPORTED — /faq.) That is generous — better than the official Ads MCP's 95-day SP window (REPORTED — deltologic.com). It means Ramadan 2026 Canadian seasonality is available for the Ramadan 2027 US forecast, provided the account is connected soon. **Connect early; the backfill window is a wasting asset.**

**Multi-account / multi-brand**: unlimited connections at no extra cost, `sellers_and_vendors_list` picks the seller per call, and read/write permission is set **per Seller and per Vendor** (REPORTED — /changelog). This is exactly the shape needed for "instantiate a second brand cheaply": brand two is a new connection under the same subscription, and its department folders differ only by a seller id.

---

## 5. Actions — the write layer, and what "approval" really means

**Action types (VERIFIED — Deltologic/datadoe-mcp README and the two write SKILL.md files):**

| Action | What it writes |
|---|---|
| `AMAZON_LISTINGS_UPDATE` | title, bullets, description, **price**, keywords |
| `AMAZON_ORDERS_CANCEL` | cancel items with reason |
| `AMAZON_ORDERS_CONFIRM_SHIPMENT` | upload tracking |
| `AMAZON_ADS_TARGETS_FIND` | read current bid + targetId (authoritative, live from Ads API) |
| `AMAZON_ADS_TARGETS_UPDATE` | **apply bid changes**; also used with `negative: true, targetType: "KEYWORD"` to create negatives at campaign/ad-group scope |
| Ads campaign / ad group / ad management across SP, SB, SD, TV, DSP | claimed: campaign states, budgets, keyword creation (REPORTED — /platform: "bid management, campaign states, keyword creation, price adjustments, inventory updates, listing creation, and Multi-Channel Fulfillment") |

**The three-step protocol (VERIFIED):** `actions_details_schema_get` → `actions_start` with `dryRun: true` → on approval, `actions_start` with `dryRun: false` → poll `actions_get`. `actions_list` gives the history.

**Two controls that live in the platform, not in the agent (VERIFIED — ppc-bid-optimizer-apply SKILL.md):**

1. **Action types are disabled by default and must be enabled per type in Settings → Actions.**
2. **The connection must be READ_WRITE**, set per Seller/Vendor.
3. And critically: **`dryRun` works even when the action type is not enabled.**

That third fact is a gift. It means the whole T0 first week can be run at full fidelity — every department can compute, validate against Amazon's real schema, and produce a proven-valid payload — with the account physically unable to be written to. **Recommendation: keep every action type disabled in DataDoe for the T0 week, and enable exactly one (`AMAZON_ADS_TARGETS_UPDATE`) when Advertising is promoted to T1.** That is a real, platform-enforced kill switch, and it satisfies the constitution's §6.9 requirement better than any repo-level rule.

**Now the uncomfortable finding. DataDoe's "approval-gated" is not our T2 approval.**

The marketing says every write is "previewed and approval gated" and "approved by you before it reaches Amazon" (REPORTED — datadoe.com, /platform). What the actual skill files do (VERIFIED) is: print a before/after table into the chat and say *"Reply 'apply' to push these bids"*. The approver is whoever is sitting in the MCP client conversation. There is no durable approval object, no second identity, no expiry, no out-of-band signature. In an unattended agent run, **the agent is the approver**, and "approval-gated" collapses to "the model was asked to confirm with itself".

I found no evidence of a platform-side approval queue where a named human signs off asynchronously, and no evidence of an "approval" tool in the MCP surface (`actions_*` has no approve/reject verb). UNKNOWN whether one exists in the web app; nothing in the tool list suggests it.

**Design consequence, and it is the central one in this report: DataDoe's dry-run is a *validator*, not an *authorisation*. The T2 authority path must stay exactly where the constitution already puts it — an approval file in `approvals/pending/`, flipped by Rami, executed by the hands runner.** DataDoe's contribution to T2 is that the dry-run result (validated payload + before/after table) becomes the evidence attached to the approval file. That makes our approvals *better* than they would otherwise be: Rami approves a payload Amazon has already said it will accept.

**Audit trail**: `actions_list` plus a claimed full action log with payloads and actor ("who ran what, from where" — REPORTED, /platform). Useful as a second copy, but the constitution's `ledger/actions.jsonl` remains the authoritative log; the DataDoe action id should be written into the ledger entry as the approval/execution reference.

---

## 6. The Skill Hub

DataDoe claims a **"47-skill Hub"** of pre-built workflows installable into Claude Code, Codex or OpenClaw via `npx skills@latest add Deltologic/datadoe-ai-skills --agent claude-code --skill <name>` (REPORTED — /hub, /compare/datadoe-vs-agentcentral).

The **public repository contains 17** (VERIFIED — github.com/Deltologic/datadoe-ai-skills, branch `development`). The other 30 are either in-app only or the number is marketing. Treat 17 as the real, inspectable set.

| Skill | Access | Output | Category | What it does |
|---|---|---|---|---|
| `weekly-sales-briefing` | read | report | Reporting | HTML briefing: KPIs, top SKUs, WoW trend |
| `sales-movers-scanner` | read | report | Reporting | Catalog-wide biggest movers with decomposition |
| `create-orders-manager` | read | app | Reporting | Single-page orders app, seller/vendor picker |
| `create-amazon-reconciliation-dashboard` | read | report | Reporting | Orders vs settlements, month switcher |
| `weekly-business-review` | read | report | Profit | Profit, margin, ad efficiency card |
| `net-profit-pl-analyzer` | read | report | Profit | True net profit by SKU, all fees |
| `return-refund-analyzer` | read | report | Profit | SKUs with highest return-driven margin loss + root cause |
| `daily-account-health-check` | read | report | Account Health | AHR, ODR, LSR, cancellation, VTR, OTDR, 6 policy-violation categories vs Amazon targets, from `amazon_seller_performance` |
| `restock-priority-alert` | read | report | Inventory | OUT NOW / IMMINENT / COVERED tiers from `amazon_fba_inventory_health`; 30-day lead time default; **not available in Mexico** |
| `buy-box-loss-root-cause` | read | report | Listings | Which SKUs lost Featured Offer and why (price / OOS / fulfilment) |
| `amazon-listing-optimizer` | read | report | Listings | Funnel benchmark, intent coverage, rewritten title/bullets/backend terms; tuned for 2026 rules (75-char title cap, COSMO, Rufus) |
| `suppressed-inactive-listings-check` | read | report | Listings | Silently non-selling listings ranked by revenue risk |
| `amazon-asin-search-auditor` | read | report | Search | Organic + sponsored visibility audit — **uses live Amazon search results and screenshots** |
| `keyword-rank-sqp-tracker` | read | report | Search | WoW organic rank + share of query from weekly SQP |
| `ppc-wasted-spend-watchdog` | read | report | Ads | Underperforming search terms and budget waste |
| **`ppc-negative-keyword-applier`** | **write** | action | Ads | Negatives for terms with ≥10 clicks, 0 orders, spend ≥ 2× target CPA; dry-run then explicit apply |
| **`ppc-bid-optimizer-apply`** | **write** | action | Ads | `new bid = current bid × (target ACoS / actual ACoS)`, clamped ±30% and to min/max; dry-run then explicit apply |

**Red flag: `amazon-asin-search-auditor` "combines DataDoe search-term data, live Amazon search results, owned-ASIN matching, screenshots"** (REPORTED — datadoe.com/hub page for that skill). "Live Amazon search results and screenshots" is browser-fetched public search-result data. That is precisely the class of activity the constitution bans in §6.1 and §6.2, regardless of who wrote the skill. **Do not adopt this skill. Do not fork it.** If Rami wants share-of-voice, buy it from a licensed data vendor or derive it from Brand Analytics / SQP share columns, which DataDoe has legitimately.

---

## 7. Scheduled agents and delivery

This is the weakest-evidenced area and the answers matter.

- **Recurring exports** are real and specific: define a relative period and a cron schedule, pick recipients (individual emails or the whole organisation, each getting their own copy), format CSV / TSV / JSON / XML / Excel. (REPORTED — /faq, /changelog.) They cost tokens (REPORTED — /faq).
- **Webhook delivery** is metered in tokens alongside exports, Actions and BigQuery queries (REPORTED — /faq), which strongly implies webhooks exist as a delivery target. The mechanics are **UNKNOWN**.
- **"Async AI agents run scheduled tasks — overnight scans, weekly client briefs auto-sent to each brand owner, anomaly alerts when ACoS spikes or inventory drops"** (REPORTED — /solutions/amazon/agencies). Slack and email delivery are named (REPORTED — /solutions/amazon/agencies, /platform/data-layer).
- **Which model runs these agents, at what cost per run, whether they can call Actions, and whether they can be triggered by webhook — all UNKNOWN.** I could not reach a docs page. There is no scheduling tool in the MCP surface (VERIFIED absence), so scheduled agents are an in-app feature, not something an agent harness can create or read.

**Recommendation regardless of the answers: do not put the company's cadence inside DataDoe.** The constitution's rhythm lives in `runtimes/` and the departments' schedules. If DataDoe's scheduler is used at all, use it for exactly one thing — a **safety-net alerting layer that fires when the agents themselves are down**: a daily anomaly email to Rami (ACoS spike, inventory drop, account-health change) that arrives whether or not the Mac mini ran. That is real value and creates no lock-in. Everything else scheduled belongs in the repo.

Use **recurring exports** more freely — a nightly CSV of yesterday's orders/ads/inventory dropped to a fixed location is a cheap, boring, restartable input that makes departments resilient to an MCP outage. That is worth setting up.

---

## 8. Security, legal, and Amazon's Agent Policy

- **SOC 2 Type II** claimed, reports on request; AES-256 at rest, TLS 1.3 in transit; pen tests and sub-processor list on request; EU-hosted option; standard DPA with SCCs and the UK IDTA. (REPORTED — /enterprise, /legal/data-processing-agreement.) No public trust portal found. **UNKNOWN** whether the Type II report is real and current — ask for it.
- **Amazon DPP clearance / restricted-PII authorisation**: DataDoe claims it passed Amazon's full security audit and is authorised for restricted PII via short-lived RDT tokens. (REPORTED — /faq.) If true, this is meaningful — it is the audit most tools fail — and it is checkable: Amazon publishes app-store listings for approved applications.
- **Terms** (REPORTED — /legal/terms-of-service): service "as is", no warranty; **DataDoe disclaims all liability for decisions made on AI outputs and for consequences of any action you authorise**; you retain ownership of your Amazon data; DataDoe may suspend or terminate at any time with or without notice; data deleted 30 days after termination. The liability disclaimer is normal and unremarkable, but it is the reason the constitution's approval gate has to be real: **if an agent misprices a SKU through DataDoe, that is entirely Rami's loss.**
- **Agent Policy (BSA §19, effective 2026-03-04)**: DataDoe uses official Amazon OAuth and official APIs, and is SP-API compliant (REPORTED — /faq, /connect/amazon/mcp). I found **no page on datadoe.com that names BSA Section 19 or the Agent Policy explicitly, and no statement about agent self-identification headers.** Third-party analysis is consistent that a compliant tool must identify itself as automated at the protocol level and that browser-automation tools are the ones at risk (REPORTED — ppc.land, sellersprite, damlawfirm coverage of the March 2026 change).

**Assessment:** the *transport* is compliant — DataDoe is an Amazon-registered application calling official APIs, which is the safe side of §19. Two residual risks:
1. **Self-identification is DataDoe's to make, not ours.** We cannot verify from outside that DataDoe's SP-API calls identify as an automated agent. Account Health's monthly Agent Policy self-audit (already in its charter) should include "asked DataDoe in writing how it self-identifies under BSA §19" as a one-time item, and file the answer.
2. **The `amazon-asin-search-auditor` skill is a policy landmine inside an otherwise compliant product.** Banning it by name in the Catalog and Pricing charters is cheap insurance.

---

## 9. Where DataDoe stops — the gap list

Hard gaps, all confirmed by absence across every page and repo I could reach:

1. **No QuickBooks, no accounting.** Month close, tax set-asides, cash forecast all need QuickBooks + A2X. DataDoe gives Finance the Amazon-side truth only.
2. **No supplier POs, no landed cost, no supplier communication.** Supply Chain's actual decisions live outside DataDoe.
3. **No Walmart, no Shopify** (claimed "coming soon", enterprise-only today). Walmart Canada monitoring from Feb 2027 has no DataDoe path.
4. **No competitor price/rank/stock history.** Keepa remains mandatory for Pricing & Market Intel. DataDoe sees *your* Buy Box status and offers; it does not see a competitor's 90-day price curve.
5. **No FBA shipment creation.** Actions cover orders, listings and ads. Inbound shipment creation is claimed once on a marketing page ("inventory updates", "MCF") but is not in the verified action list. Treat as **UNKNOWN, assume no.**
6. **No buyer messaging / Solicitations API in the action list.** Customer's review-request loop needs the hands runner and a private app, as its charter already assumes.
7. **No reimbursement case submission in the verified action list**, despite `reimbursement.recover()` / `dispute.discover()` marketing copy. **UNKNOWN, assume no.**
8. **No Vine, no coupons/deals creation** in the verified action list (coupon *performance* data exists; coupon *creation* does not).
9. **No durable human approval queue** (§5).
10. **No SLA on the $97 plan.** A DataDoe outage stops the entire company's read layer. This is the single biggest concentration risk in the design, and the mitigation is the recurring-export CSV drop in §7 plus the constitution's rule 8 ("if a tool fails, say so and stop").

---

## 10. Comparison: DataDoe against the alternatives as an MCP data layer

All rows REPORTED unless marked. Prices are list, dated 2026-09-06.

| Tool | MCP? | Read coverage | Write actions | Scheduling | Cost | Verdict for this company |
|---|---|---|---|---|---|---|
| **DataDoe** | **Yes, hosted, first-party** (VERIFIED) | Seller + Vendor + Ads + SQP + BA + PII, 100+ tables, 735-day backfill | **Yes** — listings incl. price, orders, ads bids/negatives/campaigns (VERIFIED) | Recurring exports + in-app agents (details UNKNOWN) | **$97/mo flat, unlimited accounts** | **Core. Adopt.** |
| **Official Amazon Ads MCP** | Yes, Amazon's own, open beta since 2026-02-02 | Ads only. SP 95-day, SB/SD 60-day windows. No sales/inventory/profit | Yes — 50+ tools, full campaign creation, bids, budgets, settings | No | Free, but **requires active Ads API credentials (LWA app, partner-level approval)** | **Get the credentials. Second ads surface.** Rami does not have it today |
| **Official SP-API** | **No official Seller MCP exists** — all third-party | Everything, raw | Everything | No | Free + registration burden | Deliberately avoided; DataDoe exists to avoid it |
| **Helium 10 MCP** | Yes, launched 2026-07-16 | H10 account data: research, keywords, ad diagnostics, P&L breakdown | No | No | Diamond plan; +$50 / 500 extra calls | Keep only for launch keyword research (Catalog charter already does) |
| **Jungle Scout** | No MCP found (API add-on only, POA pricing) | Market/competitor estimates | No | No | from $49/mo + API add-on | Skip |
| **Sellerboard** | No MCP | Profit, orders, PPC, stock, repeat customers | Review requests via Solicitations | **Yes** — scheduled CSV/Excel to email or protected feed URL | ~$19+/mo | Redundant with DataDoe. Skip |
| **Keepa API** | No MCP (plain REST) | **Competitor price / Buy Box / rank history, 6B ASINs** | No | No | from €49/mo (20 tokens/min) | **Buy. Fills DataDoe's biggest gap.** Wrap in a tiny local MCP or call REST |
| **Pacvue** | Yes, MCP since 2026-05-14 — but **Report MCP only** (pull existing reports as CSV/Excel) | Retail media across Amazon/Walmart/Instacart | Not via MCP (platform has them) | Platform-side | Enterprise | Overkill and over-priced at this size |
| **Perpetua / Flywheel** | No MCP found | Ads | Autonomous bidding on hourly Marketing Stream | Continuous | % of ad spend | A competitor to our agent loop, not a data layer |
| **Intentwise AI Gateway** | Yes | Ads + DSP + retail + inventory + SQP + Share of Voice, semantic layer | No | UNKNOWN | Enterprise/POA | The closest philosophical competitor to DataDoe; more expensive, ads-weighted |
| **Scale Insights** | No MCP | Ads | **Yes — deterministic rules engine**, 200+ parameters, unlimited rule stacking | Continuous | by automated ASIN, or 1% of ad spend for unlimited | See §11 — the honest alternative to an agent |
| **Sellerise** | Yes, MCP for Claude | Sellerise workspace data | UNKNOWN | No | subscription | Redundant |
| **Carbon6 / Threecolts** | No MCP found | Suites (reimbursements, PPC, inventory, analytics) | Per-product | Per-product | Per-product | Roll-ups, not data layers. Skip |
| **Nozzle** | No MCP; SERP-focused, Amazon coverage unclear | Rank tracking | No | Yes | from $59/mo | Skip; SQP covers rank-share needs |

**Conclusion: DataDoe is the right core, and it is not close.** Nothing else combines a hosted first-party MCP, Seller+Vendor+Ads under one schema, write actions, a 735-day backfill and a flat $97 with unlimited accounts. The stack is **DataDoe (core) + Keepa (competitor history) + official Amazon Ads MCP (ads writes, once credentialed) + Helium 10 (launch research only)**. Everything else on that table is either redundant, unreachable, or a competitor to the operating system itself.

---

## 11. The advertising operating loop on DataDoe

This is the department Rami wants running on agents, so it gets the detailed treatment.

### 11.1 What DataDoe exposes for ads

Verified: `amazon_ads_search_terms_by_campaign_by_date` (search-term × campaign × date, filterable by `ad_campaign_type` = SPONSORED_PRODUCTS), and a "Keyword Targeting Performance" export groupable by keyword, match type, campaign and ad group. Live bids and `targetId` come from `AMAZON_ADS_TARGETS_FIND`, not from the warehouse — DataDoe is explicit that the FIND action is the authoritative source for current bid. Campaigns, ad groups, ads and targets exist as raw tables (REPORTED — /changelog). DSP raw tables added 2026.

**Placement-level data: UNKNOWN.** No source named a placement table. This matters — placement multipliers (top-of-search vs rest-of-search vs product pages) are a standard lever and the charter's "optimizes placements" ambitions depend on it. Check `exports_sources_get` on day one.

**Hourly data: UNKNOWN, probably not.** DataDoe ingests Amazon Marketing Stream and says ads updates are "near real-time" (REPORTED), but every ads table named is `_by_date`. Assume **daily granularity** for planning. This is a genuine capability gap versus Perpetua and Scale Insights, which bid on hourly Marketing Stream. For a 60-SKU Canadian food brand at CAD 150/day cap, daily granularity is adequate; it would not be at 50× the spend.

### 11.2 What DataDoe can write for ads

Verified: bids (`AMAZON_ADS_TARGETS_UPDATE`), negatives (same action, `negative: true`, `targetType: "KEYWORD"`, at campaign/ad-group scope, `NEGATIVE_EXACT` recommended). Claimed but unverified: campaign state (pause/enable), budgets, keyword creation, campaign/ad-group/ad creation across SP/SB/SD/TV/DSP.

**Budgets are the gap that matters.** The constitution's T1 hygiene class includes "budgets within +25% per action up to the daily cap". I could not verify a budget-update action anywhere. **This is the first thing to test in the account.** If budget writes are not available through DataDoe, the T1 class must shrink to bids + negatives + pausing until the official Ads MCP is credentialed.

### 11.3 The recommended loop

Daily 06:35, Advertising department, on the Mac mini:

1. **Read state first** — `state/inventory.md`, `state/calendar.md`, `state/cash.md`. Any stock-out risk or blackout SKU is excluded before any data is pulled. (Already in the charter; keep it.)
2. **Pull** yesterday's search-term and keyword-targeting exports from DataDoe, paginated, and **write them to the repo**. Never re-export the same day twice.
3. **Compute** the proposed changes locally, in our own skill code, against our own thresholds — not DataDoe's. Fork `ppc-bid-optimizer-apply`'s formula (`new bid = current bid × target ACoS / actual ACoS`, clamped) but replace its ±30% clamp with the constitution's **±15%**, and replace "target ACoS" with the per-SKU target derived from contribution margin in `state/cash.md`. Fork `ppc-negative-keyword-applier`'s thresholds (≥10 clicks, 0 orders, spend ≥ 2× target CPA) but drive the click threshold from the trailing 90-day conversion rate as the charter's `negatives/SKILL.md` already specifies.
4. **Get live bids** via `AMAZON_ADS_TARGETS_FIND` immediately before writing. Never write a bid computed from a warehouse row without re-reading the live value — the warehouse is up to 24 hours stale and someone (Amazon's own rules, Rami) may have moved it.
5. **Dry run every change**, always, T1 or T2. `actions_start` with `dryRun: true`. A dry-run failure is a stop, not a retry with different numbers.
6. **T1 path (bids, negatives, pausing zero-order targets):** after a clean dry run, and only if every constitution guardrail holds (±15% bid, one change per target per 24h, daily cap respected, no blackout, no stock-out), call `actions_start` with `dryRun: false` and write the action id, before/after values, tier and reasoning into `ledger/actions.jsonl`.
7. **T2 path (new campaigns, structure, budgets above cap, deals, coupons):** write the *validated dry-run payload* into `approvals/pending/` as the proposal body, with the before/after table and the citation. Rami approves; the hands runner replays the identical payload with `dryRun: false`.
8. **Write `state/ads.md`.** Always, even on a failed run.

### 11.4 Can T1 auto-changes really be bounded?

Yes — but **the bounds live in our repo, not in DataDoe.** DataDoe gives three coarse platform controls (connection READ vs READ_WRITE, per-action-type enablement, token spending limit) and one procedural one (dry run). None of them can express "±15%" or "one change per target per 24 hours". Those are ours to enforce and ours to get wrong.

So the safety architecture is:
- **DataDoe enforces:** *can this class of write happen at all* (action type toggle) and *is the payload valid* (dry run).
- **Our skill enforces:** *is this specific change inside the band*, computed before the call and re-checked after `TARGETS_FIND`.
- **The ledger enforces:** *has this target already been touched today* — a `ledger/actions.jsonl` read is a mandatory precondition of every bid write.
- **Rami enforces:** everything T2, through the approval file.

That is a sound three-layer design, and it is honest about the fact that DataDoe is not a policy engine.

### 11.5 DataDoe vs the official Ads MCP vs a rules tool — recommendation

**Official Amazon Ads MCP** has the fuller write surface (50+ tools, campaign creation end-to-end), is Amazon's own and therefore the least policy-ambiguous, and is free. Its problems for us: it requires **active Amazon Ads API credentials** — an LWA application and partner-level approval Rami does not have (REPORTED); it is ads-only, so no query can cross ads and inventory or ads and margin; and its retention windows (SP 95 days, SB/SD 60 days) are shorter than the seasonal cycle we plan against.

**A rules tool (Scale Insights)** is the deterministic alternative: 200+ parameters, stackable rules, hourly execution, priced by automated ASIN or ~1% of ad spend. It would do the hygiene class more reliably than an agent and with zero prompt risk. What it cannot do is reason across ads, margin, stock cover and the launch calendar — which is the entire premise of this operating system.

**Recommendation:**

1. **Run the ads loop on DataDoe now.** It is the only surface Rami has, it has the verified bid and negative actions, and its dry-run gives the T0 week real teeth.
2. **Amend the constitution.** §3 currently says the sole T1 action class is "Advertising hygiene through the official Amazon Ads MCP". Rami has no access to that server, so **as written, ads T1 is currently unreachable and the department is stuck at T0 indefinitely.** Change the line to "through the official Amazon Ads MCP or DataDoe Actions", or the ratchet can never fire.
3. **Apply for Amazon Ads API credentials in parallel**, this month. It is a separate, lighter approval than SP-API private developer registration, it costs nothing, and it gives a second independent ads write path plus a check on DataDoe's numbers. When it lands, move *campaign creation and budgets* to the official server and keep *reporting and cross-domain analysis* on DataDoe.
4. **Do not buy a rules tool.** Revisit only if, after 90 days, the agent loop's approved-proposal rejection rate is above the ratchet's 5% threshold or the hygiene class is demonstrably losing money against a held-out set of campaigns. Buying Scale Insights now would mean paying to keep the decision that this whole company was designed to automate.

---

## 12. Department mapping

Coverage % = share of that department's *scheduled weekly work* (as written in its charter) for which DataDoe supplies the data or the action. It is not a quality score.

| Department | DataDoe covers | Adopt as-is | Fork | Write from scratch | DataDoe gaps |
|---|---|---|---|---|---|
| **Finance** | **60%** | `net-profit-pl-analyzer`, `weekly-business-review`, `create-amazon-reconciliation-dashboard`, `return-refund-analyzer` | — | 8-week cash forecast; PO ceiling; tax set-asides; tool ROI | QuickBooks, A2X, bank cash, reimbursement filing |
| **Supply Chain** | **45%** | `restock-priority-alert` (read side) | — | 12-week forecast; reorder points; PO proposals; supplier scorecards; landed cost | Supplier POs, Freightos, lead times, FBA shipment creation, Gmail |
| **Advertising** | **80%** | — | `ppc-bid-optimizer-apply` (±30%→±15%, margin-derived ACoS), `ppc-negative-keyword-applier` (charter thresholds), `ppc-wasted-spend-watchdog` | Campaign structure (4-per-hero-SKU); harvest ladder; pacing vs daily cap; anomaly rules; deals/coupon calendar | Placement data (UNKNOWN), hourly data, budget writes (UNVERIFIED), deals/coupon creation |
| **Catalog & Brand** | **65%** | `suppressed-inactive-listings-check` | `amazon-listing-optimizer` (add our listing standard + food attributes + CA/US localisation) | A+ comparison charts; image standard; launch pages; per-marketplace schema validation | Image upload, A+ publishing (claimed, unverified), Walmart |
| **Pricing & Market Intel** | **40%** | `buy-box-loss-root-cause` | — | Band setting per SKU; price-test design; 20%-in-24h guard; competitor synthesis | **Competitor price/rank/stock history — Keepa is mandatory**; Automated Pricing rule management |
| **Customer & Reputation** | **55%** | `return-refund-analyzer` | — | Sentiment themes; quality memo; buyer-message drafts; Vine packets | Review text/velocity (UNVERIFIED), Solicitations API, buyer messaging |
| **Account Health & Compliance** | **70%** | **`daily-account-health-check`** — the single best fit in the Hub; `amazon_seller_performance` carries AHR, ODR, LSR, cancellation, VTR, OTDR and six policy-violation categories with Amazon's own thresholds as columns | — | Compliance calendar; FDA/CFIA tracking; T3 appeal packets; **monthly Agent Policy self-audit** | Performance notifications inbox, appeals, IP complaints — all T3 by design |
| **Expansion & BizDev** | **35%** | `sales-movers-scanner` (dormant-SKU ranking) | — | Gate lists; US launch plan; Walmart plan; second-brand playbook; manufacturer evaluation | **No US marketplace data until the account exists; no Walmart at all** |
| **CEO / Chief of Staff** | **50%** | `weekly-sales-briefing` (as a numbers input to the brief, not the brief) | — | The brief itself; decision queue; escalations; meetings; tier ratchet | Everything non-Amazon; the brief is the company's own artifact and must never be outsourced |

**Scheduled agents to set up in DataDoe (deliberately few, all safety-net only):**

| Cadence | What | Delivery | Why in DataDoe and not the repo |
|---|---|---|---|
| Daily 05:30 marketplace | Recurring export: yesterday's orders, ads by campaign/target/search term, FBA inventory health | file/email drop the Mac mini reads | Survives an MCP outage and a runner outage |
| Daily 07:00 | Anomaly alert: ACoS spike, inventory drop, account-health change | email to Rami | Fires even if the agents did not run |
| Weekly Mon | Recurring export: weekly SQP + Brand Analytics search terms | file drop | Weekly-only data, cheap to schedule |
| Monthly | Recurring export: settlements + fees for the close | file drop for A2X/QuickBooks reconciliation | Month close is Finance's, but the raw file should exist regardless |

**Actions to enable behind Rami's approval, in order:**

1. **Now (T0 week):** none enabled. Dry-run everything.
2. **On Advertising's T1 promotion:** `AMAZON_ADS_TARGETS_UPDATE` only.
3. **On the first approved price proposal:** `AMAZON_LISTINGS_UPDATE`, executed only by the hands runner from `approvals/approved/`, never by a department.
4. **Never enable** `AMAZON_ORDERS_CANCEL`. There is no workflow in this company that needs an agent to cancel a customer's order, and the blast radius is customer-facing.

---

## 13. Implications for the design

1. **DataDoe is load-bearing and single-sourced. Treat it as infrastructure, not a tool.** Every department except Expansion depends on it. It has no SLA. The recurring-export file drop (§7) is not a nice-to-have; it is the redundancy that keeps the company readable when the MCP is down.
2. **Connect the account this week.** The 735-day backfill starts from the connect date. Every day of delay is a day of Ramadan 2026 history that will not be there for the Ramadan 2027 forecast.
3. **DataDoe's "approval" is not approval.** The `approvals/` folder plus the hands runner stays exactly as designed. DataDoe's contribution is that the thing Rami approves is now a payload Amazon has pre-validated. Upgrade the approval-file schema in `docs/CONVENTIONS.md` to carry a `dry_run_action_id` and the before/after table.
4. **The constitution has a contradiction to fix.** §3 makes the official Amazon Ads MCP the sole T1 surface; Rami cannot reach that server. Either amend §3 to name DataDoe Actions, or Advertising stays at T0 forever.
5. **Action-type toggles are the real kill switch.** §6.9 says the kill switch is "revoke the DataDoe key and Ads token". Add a softer first stage: disable all action types in DataDoe Settings → Actions. That halts every write in seconds while leaving the read layer alive so the company can still see what is happening.
6. **Ban the search-auditor skill by name** in the Catalog and Pricing charters. A policy-compliant vendor shipping one non-compliant skill is exactly how a good account gets suspended.
7. **Keepa is not optional.** Pricing & Market Intel's charter already lists it; DataDoe confirms the gap. Budget €49/month.
8. **The token meter shapes agent design.** Cache exports to the repo, hard-code table and column names in skills, never re-export a day already on disk, and keep the spending limit at $0 until the run rate is known.
9. **Second brand costs $0 in DataDoe.** Unlimited connections on a flat plan, per-seller read/write permissions, `sellers_and_vendors_list` as the switch. The "instantiate a second brand cheaply" requirement is satisfied on this axis. Write the seller id into each department's charter as a variable now, before there is a second one.

---

## 14. Open questions — the twelve things Rami should check in his DataDoe account

Ranked by how much of the design depends on the answer.

1. **Freshness at 06:00 Asia/Jerusalem.** Open the app at 06:00 and read the max date on the Canadian orders and ads tables. Is yesterday complete? If not, the entire 06:00–07:00 schedule moves.
2. **Is there a budget-update action?** Call `actions_details_schema_get` for the ads action types. If campaign budget writes do not exist, the T1 hygiene class must shrink today.
3. **Is there a placement dimension?** Run `exports_sources_get` and look for placement in the ads tables. Determines whether placement optimisation is possible at all.
4. **Is any ads table hourly?** Or is everything `_by_date`? Determines whether we are competitive with Perpetua-class bidding.
5. **Does a platform-side approval queue exist** — somewhere a named human approves a pending action asynchronously — or is "approval" only the in-chat confirm the skills implement? If one exists, it changes §5 materially.
6. **What exactly is the included token allowance** — 1,500 or 2,000 (or 4,000 promo)? And **is the spending limit really $0 by default?**
7. **What do the scheduled agents actually do**: which model, what does a run cost in tokens, can they call Actions, can they deliver to Slack and to a webhook?
8. **How many skills are really in the Hub** — 17 (the public repo) or 47? Are the extra 30 inspectable before installing?
9. **Are customer review text and velocity actually available as tables?** Customer's charter assumes yes; I could not confirm it on any DataDoe page.
10. **Do MCP key scopes really restrict tables and fields?** If yes, issue a *read-only, ads-and-inventory-only* key to Advertising and a separate write-capable key held only by the hands runner. That would make the tier system enforceable at the credential level, which is far stronger than enforcing it in prompts.
11. **How does DataDoe self-identify to Amazon under BSA §19?** Ask in writing; file the answer in `docs/`. Also ask for the SOC 2 Type II report and the sub-processor list.
12. **Walmart Canada: what is the actual date?** "Coming soon" is not a plan, and Walmart monitoring is scheduled for Feb 2027. If DataDoe cannot commit, Expansion needs a different Walmart path.

---

*Sources opened today: [github.com/Deltologic/datadoe-mcp](https://github.com/Deltologic/datadoe-mcp), [raw README](https://raw.githubusercontent.com/Deltologic/datadoe-mcp/main/README.md), [github.com/Deltologic/datadoe-ai-skills](https://github.com/Deltologic/datadoe-ai-skills), [skills tree](https://github.com/Deltologic/datadoe-ai-skills/tree/master/skills), [ppc-bid-optimizer-apply/SKILL.md](https://raw.githubusercontent.com/Deltologic/datadoe-ai-skills/development/skills/ppc-bid-optimizer-apply/SKILL.md), [ppc-negative-keyword-applier/SKILL.md](https://raw.githubusercontent.com/Deltologic/datadoe-ai-skills/development/skills/ppc-negative-keyword-applier/SKILL.md), [restock-priority-alert/SKILL.md](https://raw.githubusercontent.com/Deltologic/datadoe-ai-skills/development/skills/restock-priority-alert/SKILL.md), [daily-account-health-check/SKILL.md](https://raw.githubusercontent.com/Deltologic/datadoe-ai-skills/development/skills/daily-account-health-check/SKILL.md).*

*Sources reached only through a search index, never rendered (all blocked by this environment's egress proxy): [datadoe.com](https://www.datadoe.com/), [/pricing](https://www.datadoe.com/pricing), [/platform](https://www.datadoe.com/platform), [/platform/data-layer](https://www.datadoe.com/platform/data-layer), [/faq](https://www.datadoe.com/faq), [/changelog](https://www.datadoe.com/changelog), [/hub](https://www.datadoe.com/hub), [/enterprise](https://www.datadoe.com/enterprise), [/legal/terms-of-service](https://www.datadoe.com/legal/terms-of-service), [/legal/data-processing-agreement](https://www.datadoe.com/legal/data-processing-agreement), [/solutions/amazon/agencies](https://www.datadoe.com/solutions/amazon/agencies), [/solutions/amazon/developers](https://www.datadoe.com/solutions/amazon/developers), [/compare/datadoe-vs-agentcentral](https://www.datadoe.com/compare/datadoe-vs-agentcentral), [/connect/amazon/mcp](https://www.datadoe.com/connect/amazon/mcp), [deltologic.com head-to-head](https://www.deltologic.com/blog/datadoe-mcp-vs-amazon-native-mcp-comparison-2026), [deltologic.com top-10](https://www.deltologic.com/blog/top-10-mcp-servers-amazon-sellers-2026-ranked), [advertising.amazon.com Ads MCP open beta](https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta), [helium10.com MCP](https://www.helium10.com/tools/mcp/), [keepa.com/api-docs](https://keepa.com/api-docs/), [scaleinsights.com](https://scaleinsights.com/), [pacvue.com MCP launch](https://pacvue.com/newsroom/pacvue-launches-mcp-server-making-commerce-media-data-accessible-across-enterprise-ai-tools/), [intentwise.com/amazon-mcp](https://www.intentwise.com/amazon-mcp).*
