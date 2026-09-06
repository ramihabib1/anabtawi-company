# 09 — The Tool Layer: best-in-class per department, MCP/API required

Research date: **2026-09-06**. Author: research agent. Currency assumptions at bottom.

## Source access note (read this before trusting a tag)

This session's network egress allowed **github.com**, **raw.githubusercontent.com** and
**registry.modelcontextprotocol.io** only. Every vendor pricing page, every Amazon developer-docs page,
`advertising.amazon.com`, `developer-docs.amazon.com`, `keepa.com`, `carbon6.io`, `junglescout.com`,
`smithery.ai`, `glama.ai`, `mcp.so` and ~45 other hosts returned **403 at the egress proxy**. The web-search
budget (200 calls) was also exhausted mid-run by parallel agents.

Consequence, stated plainly:

- **VERIFIED** here means *I opened the artifact today over the network and read it* — that is limited to
  GitHub repositories and the official MCP registry API.
- **REPORTED** means a search engine returned a synthesis of secondary/vendor pages that I could not open
  myself. Every price below is REPORTED unless stated otherwise. **Re-check every price before you pay.**
- **UNKNOWN** means I tried and failed.

A follow-up run from an unrestricted network should re-verify the pricing column. Nothing in the
recommendation depends on a price being exact to the dollar, but several *do* depend on order of magnitude.

---

## 0. The finding that reframes everything

**The SP-API developer fees were announced and then cancelled.** Amazon announced on 2025-11-03 that from
2026-01-31 all third-party SP-API developers would pay **USD 1,400/year**, plus per-GET-call usage fees from
2026-04-30. Following developer backlash, Amazon reversed it.

- The fee announcement and the community reaction are **VERIFIED** —
  [amzn/selling-partner-api-models discussion #5025](https://github.com/amzn/selling-partner-api-models/discussions/5025),
  opened today, documents the Nov 2025 announcement, the tier table, and a later comment referencing an
  Amazon page announcing "cancellation of SP-API fees."
- The cancellation date (2026-05-12 email to developers, both the annual fee and the USD 0.40/1,000 GET
  overage withdrawn) is **REPORTED** —
  [novadata.io chronology](https://novadata.io/resources/news/amazon-sp-api-subscription-fees-2026) (host blocked; search summary only).

**Why this reframes the whole layer:** the company's stated position is "DataDoe is the Amazon read layer and
currently the *only* Amazon access. No SP-API private developer registration yet." That was the right call
when SP-API might have cost USD 1,400/year. It is the wrong call now. A **private developer registration for
your own seller account is free, is not a "public app", and does not require the Solutions-Architecture
architecture review** that public apps with restricted roles must pass (role review still applies to
restricted/PII roles — [role mappings](https://developer-docs.amazon.com/sp-api/docs/role-mappings), REPORTED).

Same for advertising: Amazon Ads API has a documented **self-service path for an advertiser to call the API on
behalf of its own account**, distinct from the third-party/tool-provider path
([advertising.amazon.com/about-api](https://advertising.amazon.com/about-api), REPORTED — host blocked).
The Ads API remains free.

So the highest-leverage item in this entire report costs **CAD 0**: register as your own private SP-API
developer and get self-service Ads API access. Everything below is scored against that baseline.

---

## 1. Advertising

Ad spend is CAD 1,500–5,000/month. That number is the whole analysis. A tool at USD 500–700/month is
**10–45% of ad spend** and 5–8% of gross revenue. Every enterprise PPC platform is disqualified on arithmetic
before a feature is discussed.

| Tool | What it does for us | MCP/API status | Monthly cost (tier) | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **Amazon Ads API (self-service, own account)** | Full campaign/bid/budget/negative CRUD + reports. The substrate everything else wraps. | API **REPORTED** — free, application + approval; self-service path for own-account advertisers ([about-api](https://advertising.amazon.com/about-api)) | **0** | Yes, with our own guardrails | None. Our rules live in the repo. | **Adopt (first)** |
| **Amazon official Ads MCP server** | 50+ tools, SP/SB/SD + DSP + AMC, natural-language → API calls. | MCP **REPORTED** — open beta since 2026-02-02; requires *active Amazon Ads API credentials* ([Sellershorts guide](https://sellershorts.com/resources/ai-for-amazon-sellers/amazon-ads-mcp-server-guide), [Synter](https://syntermedia.ai/blog/mcp-server-amazon-ads)). **Not in the official MCP registry and no MCP repo exists in the `amzn` GitHub org (VERIFIED today).** | 0 | Only behind our tier gate — it has no native bid/budget ceilings | None | **Adopt (once Ads API creds land)** |
| **KuudoAI `amazon_ads_mcp`** | Open-source Ads MCP; "100s of tools"; Code Mode cuts tool-catalog context from ~32k to ~470 tokens; BYO-app OAuth via LWA. | **VERIFIED** — [github.com/KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp), MIT, 67★, updated 2026-08-29 | 0 (self-host) | Yes — we own the process | MIT, forkable | **Adopt as fallback/backup to the official server** |
| **SellerMate Amazon Ads MCP** | Remote hosted MCP, `https://api.sellermate.ai/mcp/sse`, OAuth 2.1+PKCE, 50+ tools. **Server-side guardrails: bid/budget floors and ceilings, change-multiplier caps, per-currency limits, optional admin approval, audit trail. Read-only by default.** | **VERIFIED** — [github.com/SellerMate-AI/amazon-ads-mcp](https://github.com/SellerMate-AI/amazon-ads-mcp); listed in the official registry as `ai.sellermate/amazon-ads` (VERIFIED) | Free to read; writes on paid plan (amount UNKNOWN) | Yes — this is the only vendor whose guardrail model matches our T1 rules out of the box | Hosted; our campaign state stays at Amazon, so exit is cheap | **Evaluate** — the fastest path to a compliant T1 with no code |
| **Scale Insights** | Explicit **rules engine** (you write conditions/actions), dayparting, negatives, 11 algorithms, 200+ parameters. Priced by *automated ASIN count*, not spend. 30-day trial. | API/MCP **UNKNOWN** — no API documented in any source I could reach | ~USD 50–100 at 10–30 automated ASINs (REPORTED, [revenuegeeks](https://revenuegeeks.com/scale-insights-pricing/)) | Yes — it is literally a rules runner | Rules are in their UI, not our repo → real lock-in of *logic* | **Evaluate** — buy only if building rules on the Ads API proves slower than expected |
| **Helium 10 Adtomic** | PPC automation bundled into a suite we may buy anyway for keywords. | Cerebro/API only on **Enterprise** (REPORTED, [enjoy-aiia](https://enjoy-aiia.com/helium-10-api/)) | Bundled in Diamond USD 279–359, or Platinum + 2% ad-spend fee (REPORTED, conflicting) | No API → not unattended | Suite lock-in | **Skip for ads** (see §6 for keywords) |
| **Perpetua (Flywheel)** | Goal-based algorithmic bidding. | API UNKNOWN | **USD 695/mo flat up to USD 10k spend**, then flat + undisclosed % (REPORTED, [xneeti](https://xneeti.com/blog/perpetua-pricing)) | n/a | Black-box bidding = no auditability | **Skip** — 14–46% of our ad spend |
| **Pacvue** | Enterprise retail-media suite. | API UNKNOWN | No public pricing; USD 500+/mo minimum, ~3–5% of spend, annual contracts, ACV ~USD 26k (REPORTED, [sellerstack](https://www.sellerstack.ai/compare/pacvue)) | n/a | Annual contract | **Skip** |
| **Intentwise Ad Optimizer** | Ads + AMC + analytics cloud. | Uses Ads API + SP-API internally; customer-facing API UNKNOWN | ~USD 499+/mo; AMC USD 1,000+; suite USD 2,500+ (REPORTED, [revenuegeeks](https://revenuegeeks.com/software/intentwise/pricing)) | n/a | — | **Skip** |
| **Ad Badger** | Bid automation. | API UNKNOWN | From **USD 400/mo** (REPORTED, [adbadger](https://www.adbadger.com/best-amazon-ppc-tools/)) | n/a | — | **Skip** |
| **Sellozo** | Managed bidding. | API UNKNOWN | ~USD 250/mo (REPORTED) | n/a | — | **Skip** |
| **BidX** | Automation + agency hybrid. | API UNKNOWN | From **USD 149/mo** (REPORTED) | n/a | — | **Skip** |
| **m19** | AI bidding, cheapest credible entry. | API UNKNOWN | **USD 49–59/mo** entry; USD 479 + 3% at scale (REPORTED, [revenuegeeks](https://revenuegeeks.com/software/m19)) | Black-box | Logic not ours | **Skip** (bidding logic must be auditable per AGENTS.md §6.7) |
| **Quartile / Nozzle** | Enterprise / rank-tracking. | UNKNOWN | UNKNOWN | — | — | **Skip** |

**Verdict:** the AGENTS.md T1 class ("bids ±15%, budgets +25% up to daily cap, negatives above threshold, one
change per target per 24h") is ~200 lines of code against the Ads API. Every paid tool either re-implements
that with less auditability or costs more than the spend it manages. **Build it; use SellerMate free-tier as
the read-side MCP while building, and its paid guardrailed writes as the fallback if the Ads API application
stalls.**

**Where a specialist beats DataDoe:** DataDoe exposes Ads *data and campaign actions* (VERIFIED, below), but
the report should not assume it exposes dayparting, placement multipliers, or negative-keyword bulk operations
at the granularity a rules engine needs. Direct Ads API removes that uncertainty entirely.

---

## 2. Pricing and competitor intelligence (no scraping)

AGENTS.md §6.2 bans scraped competitor data in pricing decisions. That eliminates most of the category and
leaves exactly three legal sources: SP-API, Keepa's API, and DataDoe's synced data.

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **SP-API Product Pricing v2022-05-01** | `getCompetitiveSummary` returns top-20 lowest-priced offers, reference prices, `CompetitivePrice` (lowest equivalent price found at another reputable retailer) and `WasPrice` (90-day median paid on Amazon). Plus pricing notifications for event-driven repricing. | API **REPORTED** — [changelog](https://developer-docs.amazon.com/sp-api/changelog/update-the-product-pricing-api-v2022-05-01-getcompetitivesummary-operation-now-provides-the-top-20-lowest-priced-offers-and-reference-prices), [pricing FAQ](https://developer-docs.amazon.com/sp-api/docs/pricing-faq). Model JSON is on GitHub. | **0** | Read-only = yes | None | **Adopt** |
| **Amazon Automate Pricing** | Native Seller-Central rule repricer. Free, first-party, cannot violate BSA. | Managed via SP-API ([solutions page](https://developer.amazonservices.com/solutions-automated-pricing-management-on-amazon), REPORTED) | **0** | Yes — inside the per-SKU band from `products/<sku>.md`; band changes are T2 | None | **Adopt** as the execution surface for approved bands |
| **Keepa API** | The only legal source of long-run price / BSR / offer-count history and review-count history. Token-metered. | API **REPORTED** — from **€49/mo** for 20 tokens/min, no free tier; tiers €459 / €2,499 / €11,099; prepaid via Stripe, no discounts ([revenuegeeks](https://revenuegeeks.com/software/keepa/api)). Separate from the €29 Keepa Pro seat. | **€49** (~CAD 74) | Yes | Data is exportable; we cache history in the repo/duckdb | **Adopt** |
| **Keepa MCP (community)** | 6 tools: product, price history, sales-rank history, search, best-sellers, deals. | **VERIFIED** — [github.com/purahmanian/keepa-mcp](https://github.com/purahmanian/keepa-mcp), MIT, in the official registry as `io.github.purahmanian/keepa-mcp`. **Maturity: 0★, 11 commits — treat as sample code, not a dependency.** Its README claims a "free tier, 100 tokens/min", which **contradicts** the reported "no free tier" — resolve before budgeting. | 0 | Fork it; don't depend on upstream | MIT | **Adopt (as a forked ~150-line wrapper)** |
| **SmartScout API** | Brand/category-level market structure, seller-level data. | API **REPORTED**, pricing UNKNOWN (host blocked) | UNKNOWN | — | — | **Evaluate later** (US category mapping, Phase 3) |
| **Jungle Scout API** | "2B+ data points", custom apps. | API exists ([junglescout.com/products/jungle-scout-api](https://www.junglescout.com/products/jungle-scout-api/), REPORTED); price UNKNOWN and historically enterprise-quoted | UNKNOWN | — | — | **Skip** — Keepa + SP-API covers our decisions |
| **DataDive** | Keyword/listing analytics, now natively ingests Jungle Scout data. | API/MCP **UNKNOWN** | ~USD 79–199 (REPORTED, low confidence) | No | — | **Skip** |
| **Aura** | Buy-Box repricer, strong Walmart support, 10-second updates. | API UNKNOWN | ~USD 97+ (REPORTED, [revenuegeeks](https://revenuegeeks.com/aura-repricer-review/)) | — | — | **Skip** — we are the brand owner; we don't fight for a Buy Box we already own |
| **Profasee** | Brand-owner dynamic pricing (demand/inventory-driven, not Buy-Box-driven). | API UNKNOWN | From **USD 299** (REPORTED, [profasee comparison](https://profasee.com/profasee-vs-feedvisor/)) | — | Pricing logic offboard | **Skip** at current revenue; revisit above CAD 40k/mo |
| **Feedvisor** | Repricing + ads, for >USD 5M/yr sellers. | UNKNOWN | ~USD 500+ | — | — | **Skip** |
| **Brand Analytics / Search Query Performance** | Query-level impressions/clicks/cart-adds/purchases and our share of each — the single best signal for the US launch. | **REPORTED**: five Brand Analytics report families exposed via SP-API reports — Search Catalog Performance, **Search Query Performance**, Market Basket, Amazon Search Terms, Repeat Purchase ([report-type-values-analytics](https://developer-docs.amazon.com/sp-api/docs/report-type-values-analytics), [brand-analytics-role](https://developer-docs.amazon.com/sp-api/docs/brand-analytics-role)). Requires the **Brand Analytics role** on the developer registration. | 0 | Read-only | None | **Adopt** — request the Brand Analytics role in the same application |

**Where a specialist beats DataDoe:** Keepa, unambiguously. DataDoe reads *our* Seller/Vendor/Ads data;
it cannot give us a competitor's 2-year price and BSR curve. Keepa is the one paid data subscription that is
not substitutable.

---

## 3. Accounting and finance

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **QuickBooks Online** | Already the book of record. | REST API, OAuth 2.0 | already paid | — | Standard exports | **Keep** |
| **Intuit official QuickBooks Online MCP server** | **145 tools, 29 entity types (full CRUD), 11 financial reports** (P&L, Balance Sheet…). Runs as a **local stdio subprocess** — perfect for the Mac mini. OAuth 2.0 with auto-rotating refresh tokens; production requires a public HTTPS callback (ngrok workaround documented); `QUICKBOOKS_TOKEN_STORE_PATH` for read-only filesystems. Apache-2.0. | **VERIFIED** — [github.com/intuit/quickbooks-online-mcp-server](https://github.com/intuit/quickbooks-online-mcp-server), 383★, 93 commits, in the `intuit` org. **Not present in the official MCP registry (VERIFIED).** | **0** | Reads yes; writes are T2 (they touch the books) | Official, Apache-2.0 | **Adopt** — this is the finance department's hands |
| **Link My Books** | Amazon settlement → QBO journal entries with correct tax treatment. | API UNKNOWN; QBO integration is the product | **USD 21** (≤200 orders) / **41** (1k) / **60** (5k) (REPORTED, [taxomate comparison](https://taxomate.com/blog/best-quickbooks-amazon-integration-tool-taxomate-vs-a2x-vs-link-my-books)) | Yes (it posts summarised entries; we review) | Journals land in QBO — exit is clean | **Adopt** |
| **A2X** | Same job, the incumbent, better multi-currency reputation (converts settlement at payout-date rate). | API UNKNOWN | USD 29–1,039; **USD 169** at 5k orders — ~3× Link My Books at the same volume (REPORTED, same source) | Yes | Same | **Skip** unless multi-currency US+CA reconciliation breaks Link My Books in practice |
| **Sellerboard** | SKU-level real profit: FBA + referral fees, PPC, returns, promos, storage. Cheapest honest P&L in the category. | Consumes SP-API; **customer-facing API UNKNOWN** | **USD 19/mo** Standard ≤3,000 orders (REPORTED, [affmaven](https://affmaven.com/sellerboard-pricing/)) | Read-only dashboards; no API → data does not reach the repo automatically | Real: no export API found | **Evaluate** — buy only if DataDoe's COGS + our own settlement parsing leaves a gap |
| **SP-API settlement report parsing** | Ground truth. Settlement reports → duckdb → contribution margin per SKU, reconciled against Getida credits and Amazon's automated reimbursements. | API, free | 0 | Yes | None — this is the anti-lock-in play | **Adopt** |
| **FX (CAD / USD / ILS)** | Three currencies: CAD revenue, USD revenue from 2027, ILS costs. | QBO multi-currency (native); rate feed from any free source; Wise/Amazon Currency Converter for the actual conversion | 0–small | Rates yes; conversions are **T3** (money moves) | — | **Adopt QBO multi-currency; log the rate used with every entry (§6.7)** |
| **Canadian GST/HST + US sales tax** | Amazon is a **marketplace facilitator** in Canada and in every US sales-tax state — it collects and remits marketplace sales. Our residual obligation is registration/filing, not per-transaction calculation. | — | 0 | — | — | **Skip TaxJar/Avalara at this scale.** Revisit only when DTC (Shopify) or wholesale invoicing starts |
| **Avalara MCP suite** | If tax ever needs automating: **8 official Avalara MCP servers in the registry** — `com.avalara/avatax` (calculation, transactions, nexus), `/returns`, `/cross-border` (duty rates, HS), `/classification` (HS codes — relevant for food imports), `/bl`, `/elr`, `/atc`, `/docs`. | **VERIFIED** — official-namespace entries in [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/v0/servers?search=avalara) | Enterprise, UNKNOWN | — | — | **Skip now, note for Phase 4** — the HS-code/cross-border server is genuinely useful for US import duty on food |
| **Community QuickBooks MCPs** (`NyxToolsDev`, `asklokesh`, `amin-ale`, `laf-rge`, `codespar`, `com.caribooks/quickbooks`, `com.accountingqb/*`) | Alternatives to Intuit's. | **VERIFIED present in registry** | 0 | — | — | **Skip** — Intuit's own server exists and is better maintained |

**Cash-flow forecasting:** no tool. A duckdb model over settlement history + open POs + Keepa seasonality is
better than any SaaS at this size and lives in the repo, which AGENTS.md §2 requires anyway.

---

## 4. Supply chain and inventory

Two facts change this section for a **food** brand:

1. **From 2026-01-01 Amazon no longer provides in-house prep or item labelling for FBA** — units must arrive
   FNSKU-labelled, polybagged/bubble-wrapped, bundled, cartonised with valid box-content data (REPORTED,
   [amzprep](https://amzprep.com/best-amazon-fba-prep-centers/)). A prep partner is now structural, not optional.
2. **Expiry / FEFO tracking is not solved by any tool on this list.** Amazon requires ≥90 days remaining shelf
   life at receipt for expiry-dated FBA goods. None of the forecasting SaaS below models lot codes.

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **SP-API Fulfillment Inbound v2024-03-20** | `createInboundPlan` → placement options → shipments. 1,500 SKUs/plan (vs 200 in v0). v0's 13 operations were deprecated 2024-12-20; the new experience replaced all references from 2025-05-28. | API **REPORTED** — [reference](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-reference); known failure mode "Prep classification for this SKU was missing" is **VERIFIED** in [issue #556](https://github.com/amzn/selling-partner-api-models/issues/556) — set prep classification per SKU *before* automating | 0 | **No — T2.** Shipment creation is listed as T2 in AGENTS.md §3 and should stay there | None | **Adopt (T2 proposals)** |
| **duckdb + SP-API/DataDoe exports in-repo** | Demand forecast, days-of-cover vs the 14-day floor and 6-week seasonal buffer, reorder points against supplier lead time, **lot/expiry ledger with FEFO**. | Ours | **0** | Yes | Zero | **Adopt — this is the department** |
| **SoStocked (Carbon6)** | 12-month demand forecast, AWD/FBA fee planning, PO generation with lead times and safety stock. Best-in-class for Amazon-native forecasting. | Pulls Amazon APIs; **customer-facing API/MCP UNKNOWN** | ProfitFlow **USD 97**; Inventory add-on **from USD 250** (REPORTED, [revenuegeeks](https://revenuegeeks.com/software/sostocked)) | Forecast yes; POs are T2 | Forecast logic offboard; no export API found | **Skip at CAD 8–10k/mo.** USD 347 to forecast 10–15 winners is indefensible. Re-evaluate at CAD 40k+/mo |
| **Inventory Planner / Flieber / Forecastly / RestockPro** | Same category. | UNKNOWN (search budget exhausted before reaching them) | UNKNOWN | — | — | **Skip / UNKNOWN** — flag for a follow-up run |
| **Extensiv (Skubana) / Cin7 / Katana MRP** | Multi-channel OMS / small-manufacturer MRP. Katana is the only one that models *production*, which matters if we ever co-pack. | All three publish REST APIs (REPORTED, unverified); pricing UNKNOWN this run | UNKNOWN, historically USD 200–1,000+ | — | Heavy — these become the system of record | **Skip** — we sell 50–60 SKUs on two marketplaces; an OMS is a solution to a problem we don't have |
| **Freight: Flexport / Freightos** | Quotes, bookings, tracking. Freightos has a rate-search API; Flexport has a partner API. | REPORTED, unverified | Per-shipment | No | — | **Skip API; use the web UIs manually.** ~6–10 shipments/year does not justify integration |
| **Prep/3PL Canada + US** | AMZ Prep (Toronto/Vancouver/Calgary + US), SHIPHYPE (US+CA), Stallion Express (CA, PARS/PAPS customs). All advertise Seller-Central integration and real-time inventory sync. ShipBob has 60+ FCs but FBA prep is an add-on and inbound to FCs is slower. | Integration **REPORTED**; documented public APIs **UNKNOWN** | Per-unit | No | Physical switching cost | **Evaluate two Canadian and two US prep partners in Q4 2026 — this is a T3 contract decision, not a tool choice** |

**Where a specialist beats DataDoe:** nowhere that matters. DataDoe + SP-API give inventory and sales;
forecasting is arithmetic we should own, and expiry is a domain nobody sells.

---

## 5. Reimbursements and account health

The economics of this category collapsed in 2025 and most vendor marketing has not caught up.

- Claim window cut from **18 months to 60 days** on 2024-10-23.
- From **2025-03-10** Amazon reimburses lost/damaged FBA inventory at **manufacturing/sourcing cost, not
  selling price**. Reported recoveries fell **50–75%**.
- Amazon's own automated reimbursements now cover part of the flow but **~40% of eligible reimbursements
  reportedly still go unclaimed**, and automated credits "rarely match unit value."
  (All REPORTED — [ecomengine](https://www.ecomengine.com/blog/fba-reimbursement-policy),
  [leviathansellers](https://www.leviathansellers.com/blog/amazon-fba-reimbursement-policy-2026).)

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **Getida** | Audits and files claims; **25% of recovered funds**, no subscription, no minimum; Pro from USD 89/mo at 18%; first USD 400 free. | API/MCP **UNKNOWN** | **0 fixed** | Human-in-loop by design | Low — they file on our behalf | **Adopt** — zero fixed cost, pure upside, no engineering |
| **Our own SP-API reconciliation** | Compare Amazon's automated reimbursement lines against our **landed cost** per unit; flag underpayments; watch the 60-day clock per case type. This is the part Getida cannot do — they don't know our COGS. | API, free | 0 | Read/alert = T0/T1; filing a claim = **T2** (AGENTS.md §3) | None | **Adopt** — highest-value item in this section |
| **Seller Investigators / Refunds Manager / Carbon6 Seller Locker** | Same commission model, 15–25%. | UNKNOWN | 0 fixed | — | — | **Skip** — one recovery vendor is enough |
| **SP-API Notifications** | Event-driven account-health, listing, and pricing alerts without polling. | API, free | 0 | Yes | None | **Adopt** |
| **Bindwise** | Read-only monitoring on the official Amazon API: hijacker/piggybacker start *and stop*, 404 "dog page" blocked listings, detail-page content changes, fee changes, Buy-Box loss. Claims an Amazon-audited (Deloitte) integration. | Official-API-based, **REPORTED**; customer API UNKNOWN ([bindwise.threecolts.com](https://bindwise.threecolts.com/alerts/features)) | UNKNOWN (low, historically <USD 30) | Alerts only | Low | **Evaluate** — cheap insurance for the US launch window; SP-API notifications may cover 80% for free |
| **Sellerise / Seller Labs / SentryKit / AMZAlert / SellerSonar** | Same alert category. | UNKNOWN | UNKNOWN | — | — | **Skip** |

---

## 6. Listing and catalog

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **SP-API Listings Items API** | Create/patch listings programmatically; the write path for the 10 SKU activations and the whole US catalog build. | API **REPORTED** ([role mappings](https://developer-docs.amazon.com/sp-api/docs/role-mappings)) | 0 | **No — T2** (listing text/images are explicitly T2) | None | **Adopt (T2)** |
| **SP-API Listings Restrictions API** | Pre-flight check per ASIN per marketplace; returns approval next-step links when restricted. Critical for a food category in a new marketplace. | API **REPORTED** | 0 | Read-only → T0 | None | **Adopt** — run it before every US listing proposal |
| **SP-API A+ Content API** | Programmatic A+ modules. Requires Brand Registry. | API **REPORTED**; requires appropriate role | 0 | T2 | None | **Adopt (T2), Phase 2** |
| **Helium 10 (Cerebro / Magnet / Listing Builder)** | Keyword discovery for the US launch and the 10 CA activations. The one job our own data genuinely cannot do — we have no US sales history to mine. | **API only on Enterprise** (REPORTED). Platinum/Diamond are human tools; data leaves as CSV. | Platinum **USD 99 annual / 129 monthly**; Diamond 279/359 (REPORTED, [demandsage](https://www.demandsage.com/helium-10-pricing/)). Starter USD 39 retired for new subs. | No — human-driven, CSV → repo | Moderate; CSVs export cleanly | **Adopt Platinum for ~6 months (Oct 2026 – Mar 2027), then cancel.** Budget it as a project cost, not a subscription |
| **Search Query Performance (§2)** | Once US traffic exists, SQP replaces most of what Helium 10 is for — and it's free and first-party. | REPORTED | 0 | T0 | None | **Adopt; it is the reason H10 is temporary** |
| **Amazon's own AI listing tools** | Generative listing/A+ assist in Seller Central. | Browser-only → **forbidden by AGENTS.md §6.1** | 0 | **No** | — | **Skip** |
| **Image generation pipeline** | Claude/OpenAI/Grok image models + the session's Higgsfield/Magnific/Canva MCPs for pack shots, lifestyle, infographic overlays. | MCP available in-session (VERIFIED by tool presence) | inside existing subs | Generation T1; publishing T2 | None | **Adopt** — no new spend |
| **Bilingual FR/EN (Canada)** | Amazon.ca requires French. LLM translation + a native review pass. | Existing subs | 0 | Draft T1, publish T2 | None | **Adopt** — do **not** buy a translation SaaS |
| **Walmart listing tools** | See §8. | | | | | |
| **DataDive / Jungle Scout listing-quality scores** | Nice-to-have. | UNKNOWN | USD 29–199 | — | — | **Skip** |

---

## 7. Customer and reviews

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **SP-API Solicitations API (Request a Review)** | One template-based call per eligible order requests **both a product review and seller feedback**. Buyers cannot reply; nothing appears in Message Center. Compliant by construction — no custom copy to get wrong. | API **REPORTED** — [Solicitations API](https://developer-docs.amazon.com/sp-api/docs/solicitations-api), [solicit feedback for an order](https://developer-docs.amazon.com/sp-api/docs/solicit-feedback-for-an-order) | **0** | **Strong T1 candidate** — the action is bounded, idempotent, one-per-order, and has no free text. Note AGENTS.md currently lists buyer messages as T2; Solicitations deserves its own carve-out | None | **Adopt — replaces the entire email-automation category** |
| **SP-API Messaging API** | Includes `createNegativeFeedbackRemoval` after resolving a buyer issue. | API REPORTED | 0 | **T2** (free-text to buyers) | None | **Adopt (T2)** |
| **FeedbackFive** | Review-request automation + **ASIN review monitoring from ~USD 4–10/mo standalone (50 ASINs)**. | API UNKNOWN | USD 24–199 full; USD 10 monitoring-only (REPORTED, [revenuegeeks](https://revenuegeeks.com/feedbackfive-pricing/)) | Yes | Low | **Evaluate the USD 10 monitoring-only tier** — cheapest way to get new-negative-review alerts; skip the request automation (Solicitations does it free) |
| **FeedbackWhiz** | From USD 19.99; A/B tests request templates. | API UNKNOWN | USD 19.99+ | Yes | Low | **Skip** — overlaps Solicitations |
| **eDesk** | Multi-channel helpdesk (acquired FeedbackExpress). | API exists (REPORTED) | UNKNOWN | — | Helpdesk lock-in | **Skip** — one person, low ticket volume |
| **Review monitoring via Keepa** | Keepa tracks review count and rating over time per ASIN — enough to detect a drop and trigger a look. **SP-API does not expose review text.** | Keepa API (already bought) | included | T0 | None | **Adopt** — free rider on the Keepa subscription |
| **VOC dashboard** | Amazon's Voice of the Customer / NCX data. | Report availability via SP-API **UNKNOWN** this run | 0 | — | — | **Open question — verify next run** |

---

## 8. Expansion

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **Walmart Global Marketplace APIs** | **Urgent:** the Canada-specific API integration **ceased to work after 2026-07-31**; all CA sellers had to migrate to Global Marketplace APIs and regenerate keys in the Developer Portal. Today is 2026-09-06 — **if keys were ever generated on the CA endpoints they are dead now.** | API **REPORTED** — [Walmart CA migration notice](https://marketplacelearn.walmart.com/ca/guides/Other%20Topics/Announcements/switch-to-global-apis-now-and-unlock-new-possibilities-), [Global Marketplace APIs](https://developer.walmart.com/ca-marketplace/docs/global-marketplace-apis) | 0 | Read = T0 (Walmart is monitor-only until Feb 2027 per the plan) | None | **Adopt read-only now; verify key status this week** |
| **`mcp-walmart-marketplace` (alyiox)** | 6 meta-tools (`list_endpoints`, `describe_endpoint`, `call_endpoint`, `upload_feed`, …) over **234 operations / 28 OpenAPI specs**; automatic OAuth2 token management. | **VERIFIED** — [github.com/alyiox/mcp-walmart-marketplace](https://github.com/alyiox/mcp-walmart-marketplace), MIT, in the official registry. **Caveat, from its own README: US marketplace only; only 7 operations tested against production; feed upload untested end-to-end.** | 0 | Not yet | MIT | **Evaluate / fork** — the meta-tool pattern is right; the coverage is not proven, and it does not target CA |
| **`mcp-walmart-ads` (alyiox)** | Walmart Connect Sponsored Search + Display. | **VERIFIED in registry** | 0 | — | MIT | **Skip for now** |
| **Walmart Connect Ads API** | Programmatic display/sponsored-search. **Access is restricted to Walmart Connect Partner Network (WCPN) partners** — not open to an individual advertiser. | REPORTED — [Walmart Connect intro](https://developer.walmart.com/advertising-partners/docs/introduction-to-walmart-connect-ads-apis) | — | — | — | **Skip** — gated |
| **Amazon UK/EU** | Same SP-API/Ads API, different marketplace IDs; adds VAT/EPR/food-labelling compliance. | Same APIs | 0 | — | — | **Skip until after US Ramadan 2027 lands** |
| **Shopify (DTC)** | Three **official** MCP servers: **Dev MCP** (`@shopify/dev-mcp`, open-sourced into the Shopify AI Toolkit on 2026-04-09; the old `Shopify/dev-mcp` repo now 404s but the npm package is unchanged), **Storefront MCP**, and **Customer Accounts MCP** (both remote, hosted per store). This session also carries a first-party Shopify MCP. | **REPORTED** for the toolkit move ([wearepresta](https://wearepresta.com/shopify-mcp-server-the-standardized-interface-for-agentic-commerce-2026/)); Shopify MCP presence **VERIFIED** in this session's toolset | Shopify Basic ~USD 39 | — | Moderate | **Skip until Amazon US is stable.** DTC is a second business, not a channel |
| **Faire / wholesale** | Middle-Eastern food has a real specialty-grocery wholesale channel. | API UNKNOWN | — | — | — | **Skip — but this is the highest-margin unexplored channel; worth a dedicated research pass** |

---

## 9. Cross-cutting

The Mac mini changes this section: a free, always-on, local runner beats every hosted orchestrator.

| Tool | What it does for us | MCP/API status | Monthly cost | Unattended-safe? | Lock-in / export | Recommendation |
|---|---|---|---|---|---|---|
| **1Password** | Secrets vault + `op` CLI + `op run --env-file` injection. An MCP for service accounts exists in the registry (`io.github.CakeRepository/1password`, community, **VERIFIED present**). | CLI mature; MCP community | Teams Starter **USD 19.95/mo up to 10 members**; Business USD 7.99/user; **no secrets-only plan** (REPORTED, [infisical comparison](https://infisical.com/blog/secrets-manager-pricing)) | Yes | Low — export supported | **Adopt if already paying for 1Password** |
| **Doppler** | Developer tier **free for up to 3 users**; CLI, service tokens, 5 config syncs, 3-day audit log. | CLI + API; no registry MCP found | **0** | Yes | Low | **Adopt if not already on 1Password** — this is the default recommendation |
| **Infisical** | Open source, self-hostable, 27k★; free tier 5 clients / 500 secrets. | CLI + API | 0 | Yes | None (self-host) | **Skip** — self-hosting violates "Rami maintains no servers" |
| **launchd (Mac mini)** | Primary scheduler. Native, free, survives reboot, runs in Asia/Jerusalem local time — which matters because Amazon's business day closes 07:00 local. | n/a | 0 | Yes | None | **Adopt — primary** |
| **GitHub Actions** | Backstop scheduler for anything that must run when the Mac mini is down, plus the commit/push path in AGENTS.md §7.10. | n/a | 0 (public/free minutes) | Yes | None | **Adopt — secondary** |
| **Trigger.dev / Inngest** | Durable workflow engines. | Good APIs | free tiers exist; UNKNOWN current | Yes | Moderate | **Skip** — solving a problem launchd + git already solves |
| **n8n / Zapier / Make** | Visual automation. | APIs + community MCPs (`io.github.RPGMais/mcp-n8n`, 43 tools, **VERIFIED in registry**) | USD 20–100 | Partly | **High — logic in a GUI violates AGENTS.md §2** ("nothing important lives outside this repo") | **Skip** |
| **monday.com** | Already paid (Pro, 2 seats); **full MCP in this session (VERIFIED)** — boards, items, docs, notifications, dashboards. The approved management surface. | MCP VERIFIED | already paid | Yes | Accepted per non-negotiables | **Adopt — the decision queue and daily ranked list live here** |
| **Telegram bot** | Push to Rami's phone. Free, instant, scriptable, works from launchd with one `curl`. Several MCPs in the registry (**VERIFIED**), including `io.github.ParthJadhav/telegram-notify-mcp`. | Bot API, free | **0** | Yes | None | **Adopt** |
| **Slack / Pushover** | Alternatives. Pushover is USD 5 once per platform. | APIs | ~0 | Yes | None | **Skip** — Telegram + monday is enough for one person |
| **Healthchecks.io** | Dead-man's switch per department run. If the Advertising 06:00 job doesn't ping, Rami gets told. Free tier historically 20 checks. **Four MCP servers in the registry (VERIFIED)**, incl. `io.usefulapi/healthchecksio` and `io.github.ni-c/healthchecks-mcp` ("read why one failed"). | API + MCP **VERIFIED in registry**; pricing **UNKNOWN this run** (host blocked, search budget exhausted) | 0 (free tier) | Yes | None — self-hostable OSS | **Adopt** |
| **Cronitor / BetterStack** | Same category, richer. | APIs | USD 10–30 | Yes | Low | **Skip** |
| **Stripe MCP** (`com.stripe/mcp`, official, VERIFIED in registry) | Only if DTC happens. | VERIFIED | — | — | — | **Note for Phase 4** |

---

## Recommended stack

Excludes DataDoe (researched separately) and things already paid for (monday.com Pro, QuickBooks, Claude Max,
ChatGPT, SuperGrok, API credits).

| Line | Tier | USD/mo | CAD/mo |
|---|---|---:|---:|
| SP-API private developer registration (own account) | — | 0 | 0 |
| Amazon Ads API self-service (own account) | — | 0 | 0 |
| Amazon official Ads MCP (needs the above) | open beta | 0 | 0 |
| Keepa API | €49 Starter, 20 tokens/min | ~53 | ~74 |
| Link My Books | 1,000-order tier | 41 | 57 |
| Helium 10 Platinum | annual billing, **6 months only** | 99 | 137 |
| Intuit QuickBooks Online MCP | Apache-2.0, local | 0 | 0 |
| Doppler Developer (or existing 1Password) | free ≤3 users | 0 | 0 |
| Healthchecks.io | free tier | 0 | 0 |
| Telegram + launchd + GitHub Actions | — | 0 | 0 |
| Getida | 25% success fee, no fixed cost | 0 | 0 |
| **Total, months 1–6** | | **~193** | **~268** |
| **Total, month 7+** (H10 cancelled) | | **~94** | **~131** |

Contingency line, not in the total: **SellerMate Ads MCP paid writes** or **Scale Insights** (~USD 50–100)
if the in-repo Ads rules engine slips past December. Budget USD 100/mo as a reserve.

At CAD 8–10k/month revenue this is **2.7% of revenue** falling to **1.3%**. For comparison, a single
Perpetua seat would be 8% of revenue.

## Minimal stack

Rami's time is the constraint. If only three things get bought:

1. **Keepa API — €49/mo (~CAD 74).** Non-substitutable. No other legal source of competitor price/BSR history.
2. **Link My Books — USD 41/mo (~CAD 57).** Removes the single most time-consuming recurring manual task
   (settlement → books) and keeps the finance department honest.
3. **Getida — CAD 0 fixed.** Free money with zero setup time.

**Minimal total: ~USD 94 / ~CAD 131 per month**, plus the free layer (SP-API + Ads API registrations,
Intuit's QBO MCP, Doppler, Healthchecks, Telegram, launchd, GitHub Actions).

Helium 10 is the only judgement call excluded — buy it only when US keyword work actually starts, and cancel
it the day Search Query Performance has US data.

## Phased adoption order

**Phase 0 — September 2026 (cost CAD 0). Do this before anything else.**
1. Apply for **SP-API private developer registration** for the Anabtawi seller account. Request roles:
   Pricing, Inventory/FBA, Finance, Listings, Brand Analytics, Notifications, Selling Partner Insights.
2. Apply for **Amazon Ads API self-service access** on behalf of our own advertising account.
3. **Verify Walmart CA API keys** — the CA-specific endpoints died 2026-07-31; regenerate on Global APIs.
4. Stand up the Mac mini: Doppler (or 1Password) vault, launchd slots in Asia/Jerusalem, Healthchecks ping per
   department, Telegram bot for the daily ranked list.
5. Wire **Intuit's QuickBooks MCP** locally, read-only, and confirm P&L pulls.

**Phase 1 — October 2026 (+~CAD 131/mo).**
6. Keepa API + a forked ~150-line Keepa MCP wrapper. Start the competitor price/BSR history cache in duckdb.
7. Link My Books → QuickBooks. Reconcile one full month against a hand-parsed settlement report before trusting it.
8. Getida onboarding, plus our own SP-API reimbursement reconciliation against landed cost.
9. Build the Ads rules engine against the Ads API. Run it **T0 (propose only)** for 30 days — which is exactly
   the ratchet condition in AGENTS.md §5.

**Phase 2 — November–December 2026 (+~CAD 137/mo, temporary).**
10. Helium 10 Platinum for US keyword research and the 10 CA SKU activations.
11. Listings Restrictions API pre-flight on every candidate US ASIN — do this *before* committing inventory.
12. A+ Content API + image pipeline for the US catalog. All T2.
13. Promote Ads hygiene to **T1** if the ratchet conditions are met.

**Phase 3 — January–February 2027 (+CAD 0).**
14. FBA Inbound v2024-03-20 as T2 proposals for the US shipment. **Set prep classification per SKU first** —
    the missing-prep-classification failure is documented and will otherwise block `createInboundPlan`.
15. Turn on Solicitations API (Request a Review) — propose it as its own T1 carve-out.
16. Expiry/FEFO lot ledger in the repo, enforced against the 90-day-remaining-shelf-life rule.
17. Walmart CA read-only monitoring via Global APIs.

**Phase 4 — post-Ramadan 2027, revisit only if the numbers moved.**
18. Cancel Helium 10 once SQP has US data.
19. Re-evaluate Scale Insights (only if our rules engine is a maintenance burden), Sellerboard (only if
    settlement parsing is a gap), Profasee (only above CAD 40k/mo), Avalara cross-border/classification MCP
    (only when import duty on food becomes material), Shopify DTC, Faire wholesale.

---

## Implications for the design

1. **The tool layer is mostly a registration layer, not a purchasing layer.** Free Amazon APIs plus one paid
   data feed (Keepa) plus one paid bookkeeping bridge (Link My Books) covers eight of nine departments. The
   constitution's rule of the company — "a hosted tool we buy, an open-source tool we run, or a plain text
   file in this repo" — resolves overwhelmingly to the third option at this revenue.
2. **Rewrite the DataDoe-only assumption.** "DataDoe is the only Amazon access" was defensible when SP-API
   might cost USD 1,400/yr. With fees cancelled, DataDoe should become the *convenience* layer (hosted,
   pre-authorised, Skills/Memories, dry-run Actions) while direct SP-API and Ads API become the *authority*
   layer. Both is better than either: DataDoe survives a Mac-mini outage; direct API survives a DataDoe
   outage or price change. That redundancy is worth more than the marginal cost of both.
3. **Guardrails are our differentiator and we should not outsource them.** SellerMate is the only vendor whose
   published guardrail model (bid/budget floors and ceilings, change-multiplier caps, per-currency limits,
   admin approval, audit trail) matches AGENTS.md §3 — and it is a hosted third party we'd be trusting with
   write access. Building the same in-repo is a few hundred lines and makes every action auditable in
   `ledger/actions.jsonl` as §6.4 requires.
4. **Solicitations API deserves its own tier row.** AGENTS.md lumps "buyer messages" into T2. Solicitations is
   template-only, buyer-unreplyable, one-per-order and idempotent — structurally incapable of the harms T2
   guards against. Splitting it out unlocks a real recurring win at zero risk.
5. **Two dated cliffs are already behind us and need checking this week:** Walmart CA-specific APIs stopped
   working 2026-07-31, and Amazon stopped providing FBA in-house prep and labelling on 2026-01-01. The second
   makes a prep partner a **T3 contract decision** that must be made well before the mid-January 2027 US FBA
   deadline — the supply-chain department should be proposing partners now, not in December.
6. **Food-specific gaps have no vendor.** Expiry/FEFO, lot codes, 90-day shelf-life at receipt, and
   temperature-sensitive freight are unmodelled by every tool reviewed. That is a feature: it is exactly the
   kind of durable, compounding knowledge `memory/MEMORY.md` and `playbooks/` exist to hold, and it is
   defensible against a competitor who just buys SoStocked.
7. **The reimbursement department's real job changed.** Post-March-2025, chasing claims is worth 50–75% less;
   auditing Amazon's *automated* credits against our landed cost is worth more. Getida cannot do that job
   because they don't have our COGS. We do.
8. **Second-brand instantiation is nearly free under this stack.** New SP-API + Ads API registrations (CAD 0),
   a second Keepa key or shared tokens, a second Link My Books channel, a `git clone` of the repo. The only
   per-brand fixed cost is bookkeeping. That validates the design goal.

## Open questions

1. **Does the Amazon official Ads MCP accept self-service (own-account) Ads API credentials, or only
   partner-tier credentials?** Sources conflict — one says "available to Amazon Ads API partners with active
   credentials", another says "partner-level, not something a solo seller flips on." This determines whether
   Phase 1 uses Amazon's MCP or KuudoAI's. **Highest-priority unknown in this report.**
2. **Confirm the SP-API fee cancellation from an Amazon-owned page**, not a chronology blog. Everything in
   Phase 0 rests on it.
3. **Keepa API free tier: does it exist?** The community MCP README claims 100 tokens/min free; the pricing
   research says no free tier and €49 minimum. €588/year hangs on this.
4. **Does Getida expose an API or MCP?** If yes, recovery data can flow into `ledger/` automatically. UNKNOWN.
5. **Is Search Query Performance available for Amazon.ca**, or US-only? Determines whether Helium 10 is needed
   for the Canadian activations too, or only the US launch.
6. **Sellerboard export path.** No customer API found. If genuinely absent, it is unusable under §2.
7. **Which Canadian and US prep centres publish a real API** (inbound ASN, inventory levels, lot/expiry
   fields)? Nobody answered this; it needs a dedicated call with 3–4 providers, and lot/expiry field support
   should be a hard requirement in the RFP.
8. **Voice of the Customer / NCX report availability via SP-API** — unverified.
9. **Healthchecks.io, Cronitor and BetterStack current pricing** — the search budget ran out before these.
   Assumed free tier is sufficient; verify before relying on it.
10. **Do any of Amazon's Ads MCP write operations bypass the BSA Section 19 concern entirely, or do agent
    actions through it still need the human-authorisation floor** (>20% price move in 24h, bulk edits ≥500
    ASINs)? Our tiers are already stricter, but the answer should be recorded in `playbooks/`.

---

### Currency assumptions

Converted at **USD 1.00 = CAD 1.39** and **EUR 1.00 = CAD 1.52** (approximate; **UNKNOWN** — live rates could
not be fetched this session). Treat CAD figures as ±5%.

### Sources

- [amzn/selling-partner-api-models discussion #5025 — SP-API fees](https://github.com/amzn/selling-partner-api-models/discussions/5025) (VERIFIED)
- [amzn/selling-partner-api-models issue #556 — createInboundPlan prep classification](https://github.com/amzn/selling-partner-api-models/issues/556) (VERIFIED)
- [intuit/quickbooks-online-mcp-server](https://github.com/intuit/quickbooks-online-mcp-server) (VERIFIED)
- [SellerMate-AI/amazon-ads-mcp](https://github.com/SellerMate-AI/amazon-ads-mcp) (VERIFIED)
- [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) (VERIFIED)
- [Deltologic/datadoe-mcp](https://github.com/Deltologic/datadoe-mcp) (VERIFIED)
- [purahmanian/keepa-mcp](https://github.com/purahmanian/keepa-mcp) (VERIFIED)
- [alyiox/mcp-walmart-marketplace](https://github.com/alyiox/mcp-walmart-marketplace) (VERIFIED)
- [jshorwitz/awesome-agentic-advertising](https://github.com/jshorwitz/awesome-agentic-advertising) (VERIFIED)
- [Official MCP registry API](https://registry.modelcontextprotocol.io/v0/servers) (VERIFIED — Avalara, Stripe, SellerMate, DataDoe, Keepa, Walmart, Healthchecks, n8n, Telegram, 1Password entries)
- [Amazon Ads API](https://advertising.amazon.com/about-api) (REPORTED — host blocked)
- [SP-API Product Pricing v2022-05-01 changelog](https://developer-docs.amazon.com/sp-api/changelog/update-the-product-pricing-api-v2022-05-01-returns-new-competitive-price-and-deprecates-competitivepricethreshold) (REPORTED)
- [SP-API Fulfillment Inbound v2024-03-20 reference](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-reference) (REPORTED)
- [SP-API Solicitations API](https://developer-docs.amazon.com/sp-api/docs/solicitations-api) (REPORTED)
- [SP-API Brand Analytics reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-analytics) (REPORTED)
- [SP-API role mappings](https://developer-docs.amazon.com/sp-api/docs/role-mappings) (REPORTED)
- [Walmart CA → Global APIs migration](https://marketplacelearn.walmart.com/ca/guides/Other%20Topics/Announcements/switch-to-global-apis-now-and-unlock-new-possibilities-) (REPORTED)
- [Walmart Connect Ads APIs intro](https://developer.walmart.com/advertising-partners/docs/introduction-to-walmart-connect-ads-apis) (REPORTED)
- [Amazon Ads MCP open beta guide — Sellershorts](https://sellershorts.com/resources/ai-for-amazon-sellers/amazon-ads-mcp-server-guide) (REPORTED)
- [Keepa API pricing — RevenueGeeks](https://revenuegeeks.com/software/keepa/api) (REPORTED)
- [A2X vs Link My Books pricing — Taxomate](https://taxomate.com/blog/best-quickbooks-amazon-integration-tool-taxomate-vs-a2x-vs-link-my-books) (REPORTED)
- [Sellerboard pricing — Affmaven](https://affmaven.com/sellerboard-pricing/) (REPORTED)
- [Helium 10 pricing — DemandSage](https://www.demandsage.com/helium-10-pricing/) (REPORTED)
- [Perpetua pricing — Xneeti](https://xneeti.com/blog/perpetua-pricing) (REPORTED)
- [Pacvue pricing — SellerStack](https://www.sellerstack.ai/compare/pacvue) (REPORTED)
- [Scale Insights pricing — RevenueGeeks](https://revenuegeeks.com/scale-insights-pricing/) (REPORTED)
- [Getida pricing — RevenueGeeks](https://revenuegeeks.com/software/getida/pricing) (REPORTED)
- [FBA reimbursement policy — ecomengine](https://www.ecomengine.com/blog/fba-reimbursement-policy) (REPORTED)
- [FBA 60-day rule — Leviathan Sellers](https://www.leviathansellers.com/blog/amazon-fba-reimbursement-policy-2026) (REPORTED)
- [SoStocked pricing — RevenueGeeks](https://revenuegeeks.com/software/sostocked) (REPORTED)
- [FBA prep changes + Canadian 3PLs — AMZ Prep](https://amzprep.com/best-amazon-fba-prep-centers/) (REPORTED)
- [Bindwise alert features](https://bindwise.threecolts.com/alerts/features) (REPORTED)
- [FeedbackFive pricing — RevenueGeeks](https://revenuegeeks.com/feedbackfive-pricing/) (REPORTED)
- [Secrets manager pricing — Infisical](https://infisical.com/blog/secrets-manager-pricing) (REPORTED)
- [Shopify MCP / AI Toolkit — WeArePresta](https://wearepresta.com/shopify-mcp-server-the-standardized-interface-for-agentic-commerce-2026/) (REPORTED)
