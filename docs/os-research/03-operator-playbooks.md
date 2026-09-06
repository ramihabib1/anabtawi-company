# 03 — How top Amazon private-label operators run a brand week to week (2026), and what an AI-department company should copy

Research date: 2026-09-06. Author: research agent. Audience: Rami (solo operator, Anabtawi brand).

---

## 0. Method, and a hard limit on verification

**I could not open a single primary source today.** The session's egress proxy blocked `WebFetch` for every domain tried — `sellercentral.amazon.com`, `sell.amazon.com`, `advertising.amazon.com`, `www.fda.gov`, `inspection.canada.ca`, even `en.wikipedia.org` — all `EGRESS_BLOCKED`. Search worked; fetch did not. Therefore:

- **VERIFIED** — used **zero times** here. I opened no primary source, so nothing qualifies.
- **REPORTED** — returned consistently across search summaries and/or secondary write-ups; URL given. This is the tag on almost everything.
- **UNKNOWN** — could not confirm; I say what I tried.

**Consequence for the design:** every number here touching money, fees, or policy must be re-confirmed in Seller Central by Rami (a human in a browser is legal — BSA §19 bans *automated* browsing) or via a DataDoe/SP-API read before an agent encodes it as a guardrail. Several 2026 fee changes are recent.

One correction to the brief up front:

> **Ramadan 2027 begins on or about Monday 8 February 2027, not 17 February.** Eid al-Fitr falls ~9–10 March 2027. [REPORTED — https://www.islamicfinder.org/special-islamic-days/ramadan-2027/ ; https://www.jordannews.jo/Section-20/Middle-East/Date-of-the-First-Day-of-Ramadan-2027-According-to-Astronomical-Calculations-52316 ; https://truecalendar.com/eid-al-fitr/2027]. Dates are provisional until the Sha'ban crescent is sighted, but the astronomical projection is stable to ±1 day. **17 February is Ramadan 2026, not 2027.** The whole US launch schedule moves nine days earlier than the brief assumed. This is the single most consequential finding in this report.

---

## 1. The operating cadence of a top operator

### 1.1 The shape everyone converges on

Serious operators — aggregators, agencies, Amazon itself — run the same three layers: a **daily exception scan** (minutes, alarm-driven), a **weekly business review** (the real decision meeting), and a **monthly/quarterly plan-and-falsify cycle**.

Amazon's own mechanism is canonical: a WBR deck read in silence then walked page by page, built on **controllable input metrics** rather than outputs, upstream of monthly/quarterly reviews and annual OP1/OP2 planning [REPORTED — https://workingbackwards.com/concepts/amazon-operating-cadence/ ; https://commoncog.com/the-amazon-weekly-business-review/]. Steal the input/output distinction: revenue is an output; sessions, CVR, in-stock rate, review velocity and share of voice are the levers.

Agency SOP libraries run the same shape smaller — a PPC SOP with daily budget checks (5–10 min), weekly search-term work (30–45 min), monthly strategy review (1–2 hrs), each with a named owner and quarterly review [REPORTED — https://taskip.net/how-to-create-agency-sops/ ; https://myamazonguy.com/sop/amazon-sop-library/]. Aggregators (Thrasio-style) used standardised relaunch playbooks — PPC, listing, supply chain, expansion — applied uniformly across a portfolio [REPORTED — https://teardowns.sandhill.io/p/thrasio]. Their failure is instructive: the autopsies blame over-standardisation and headcount ("teams of ten doing the work of two") and the assumption that all FBA assets behave alike, not the cadence [REPORTED — https://www.marketplacepulse.com/articles/death-by-valuation-the-amazon-aggregator-autopsy ; https://restructuringnewsletter.com/p/trash-io-the-stumble-from-scale-and-short-term-solutions]. **Copy the cadence, not the headcount. The cadence is the part that automates.**

### 1.2 What is checked when, and what triggers action

| Cadence | Metrics / reports checked | Trigger for action |
|---|---|---|
| **Daily (07:15 Asia/Jerusalem, after Amazon's 07:00 business-day close)** | Account Health Rating and new policy violations; stranded / unfulfillable / suppressed listings; Buy Box (Featured Offer) loss; yesterday's ad spend vs pace; out-of-stock and units-on-hand for hero SKUs; new 1–2★ reviews and returns; order defect signals | AHR drop or any new violation → immediate escalation, T3. Buy Box loss > 4h → pricing check. Any hero SKU below cover floor → supply chain wake. Spend > 110% of daily pace → budget throttle |
| **Weekly (Mon)** | Search Query Performance (Amazon weeks run Sun–Sat, so Monday is the first day the prior week is complete) [REPORTED — https://kapoq.com/search-query-performance-report-explained/ ; https://perpetua.io/blog-amazon-search-query-performance/]; Business Reports (sessions, unit session %, page views); ad search-term report → negative harvesting + keyword promotion; restock report and days of cover; Voice of the Customer / NCX rate; review velocity; competitor price movement | Click-share or purchase-share drop > 20% w/w on a top-20 keyword → listing/PPC investigation. NCX above category threshold → CX ticket. Cover < floor → PO proposal |
| **Bi-weekly / fortnightly** | Placement performance and placement modifiers; bid ladder review; A+ / image test readouts; Subscribe & Save subscriber count and churn | Placement ROAS spread > 30% → modifier change |
| **Monthly** | Full P&L by SKU: contribution margin per unit after ads; TACoS by SKU; storage fees, aged-inventory surcharge, storage-utilisation surcharge, low-inventory-level fee, inbound placement fee; reimbursement recovery; IPI; returns rate; forecast vs actual | CM% below floor → price or cost action, T2. Any fee line > 3% of revenue → structural fix |
| **Quarterly** | Assortment review (kill / double-down); supplier terms and lead-time re-measurement; promo calendar for next two quarters; playbook falsification against last 90 days of outcomes; guardrail re-tuning and the T2→T1 ratchet review | Any SKU below CM floor for two consecutive quarters → discontinue proposal, T3 |

### 1.3 The metric map, and what each one is actually for

- **TACoS** — ad spend ÷ total revenue; the composite health number. Established brands sit ~10–15%; brand-defence campaigns 5–10% ACoS, category-conquest 25–40% if buyers repeat [REPORTED — https://canopymanagement.com/ultimate-guide-to-acos-and-tacos/ ; https://www.velocitysellers.com/2026/04/19/tacos-ceiling-amazon-ad-spend-data/]. Better sources reject benchmark-chasing and derive the target from unit economics: *40% gross margin, 15% needed after ads ⇒ target ACoS 25%* [REPORTED — https://marketplacevalet.com/how-to-set-tacos-targets-by-product-lifecycle-and-contribution-margin/].
- **Contribution margin per unit** — revenue − COGS − fulfilment − referral − other variable − ads. Audited brands land at 12–22% once everything is counted [REPORTED — https://www.brandgrowthiq.com/blog/amazon-profitability-playbook/]. This is what the AGENTS.md 15% floor must be measured against, and it must carry the 2026 fee lines (§7) or it lies.
- **Sessions and unit session % (CVR)** — separates a demand problem from a listing problem. Food & grocery converts unusually well: ~15–21% reported [REPORTED — https://sellermetrics.app/amazon-conversion-rate/ ; https://autron.ai/benchmark/amazon-ppc-benchmarks-by-category-2026], with the lowest ACoS of any major category (~21–24%) and low CTR (~0.40–0.55%) [REPORTED — https://autron.ai/blog/amazon-advertising-benchmarks-2026 ; https://keywords.am/blog/amazon-cpc-benchmarks/]. **A grocery CVR under 10% is a listing problem, not a traffic problem.**
- **BSR and Buy Box share** — leading indicators of rank and of pricing/competition trouble. **IPI, restock limits, capacity** — §7. **VOC/NCX, returns, review velocity, AHR, violations** — §9.
- **Search Query Performance (Brand Analytics)** — impressions, clicks, purchases plus *share* metrics per query, weekly, top 1,000 queries; the best organic-vs-paid diagnostic Amazon gives brands [REPORTED — https://www.amalytix.com/en/knowledge/controlling/amazon-search-query-performance-report/].

---

## 2. Weekly operating calendar

All times Asia/Jerusalem. Amazon's business day closes 07:00 local, so the daily pass runs after that. Assumes DataDoe as the read layer (the only Amazon access today) and a local "hands" runner on the Mac mini for T1/T2 execution.

| Day / time | Department | Job | Data source | Output |
|---|---|---|---|---|
| Daily 07:15 | Account Health & Compliance | Exception scan: AHR, policy violations, suppressed/stranded/unfulfillable, listing issues | DataDoe (Account Health, Listings), SP-API `LISTINGS_ITEM_ISSUES_CHANGE` when available | `state/compliance.md`; T3 escalation file if any violation |
| Daily 07:20 | Supply Chain | Units on hand + inbound, days of cover per SKU vs floor, restock-limit headroom | DataDoe FBA Inventory / Restock report | `state/supply-chain.md`; reorder alert if cover < floor |
| Daily 07:25 | Advertising | Spend pacing vs daily cap, yesterday's ACoS/TACoS by campaign, zero-impression and runaway campaigns | Amazon Ads MCP / Ads API | T1 bid & budget actions logged to `ledger/actions.jsonl` |
| Daily 07:30 | Pricing & Market Intel | Buy Box status, competitor offer changes, price-band breaches | SP-API `ANY_OFFER_CHANGED` / `PRICING_HEALTH`; Keepa API | Alert or T2 price proposal |
| Daily 07:40 | CEO / Chief of Staff | Assemble the ranked decision list from all departments | `state/*.md`, `approvals/pending/` | `briefs/<date>-daily.md` — Rami's one screen |
| **Mon 08:00** | **Advertising** | **Weekly PPC review: search-term harvest, negatives, keyword promotion, placement modifiers, bid ladder** | Ads API search-term report; SQP | Bid/negative changes (T1); new-campaign proposals (T2) |
| Mon 09:00 | Catalog / Creative | SQP click-share & purchase-share deltas on top-20 ASINs; conversion diagnosis; A+/image backlog | Brand Analytics SQP; Business Reports | Listing change proposals (T2) |
| Mon 10:00 | Customer | VOC/NCX review, new negative reviews, returns reasons, buyer messages | DataDoe VOC / Returns | CX fix tickets; requests to Catalog/Supply Chain |
| Mon 11:00 | Chief of Staff | Weekly Business Review: input metrics deck, forecast vs actual, decisions queued | All `state/*.md` | `meetings/<date>-wbr.md`; approvals batch for Rami |
| Tue 08:00 | Supply Chain | Forecast refresh, reorder-point recalculation, PO proposals, expiry/FEFO aging report | DataDoe inventory + sales history; supplier lead-time log | PO proposals (T2/T3) in `approvals/pending/` |
| Tue 10:00 | Pricing | Weekly price/promo review, Automate Pricing band audit, coupon/deal ROI check | SP-API pricing; Keepa; ledger | Price proposals (T2) |
| Wed 08:00 | Expansion | US launch workstream (until Feb 2027), then Walmart; compliance and logistics milestones | Project plan in repo | `state/expansion.md`; milestone requests |
| Wed 10:00 | Finance | Cash, ad-spend burn vs cap, fee anomaly scan, reimbursement candidates | DataDoe payments/fee reports; QuickBooks | Reimbursement claim proposals (T2) |
| Thu 08:00 | Advertising | Mid-week bid check + budget re-pacing; dayparting review | Ads API | T1 actions logged |
| Thu 10:00 | Catalog | Listing hygiene sweep: suppressed attributes, image count, keyword coverage, variation health | DataDoe Listings | Fix proposals |
| Fri 08:00 | Finance | Weekly contribution-margin-per-unit refresh by SKU; TACoS by SKU; flag SKUs below floor | Fee + sales + ad data | `state/finance.md` |
| Fri 10:00 | Chief of Staff | Approval hygiene: expire >48h proposals, re-propose with fresh data; ledger audit | `approvals/`, `ledger/actions.jsonl` | Clean approval queue |
| Fri 11:00 | All | Memory pass: observations → `memory/<date>.md` | — | Daily memory files |
| **Mon (monthly, 1st Mon)** | **Finance + CoS** | **MBR: full P&L by SKU, fee-line analysis, target revision, guardrail re-tune** | All | `meetings/<date>-mbr.md` |
| Quarterly (1st Mon of quarter) | All | Assortment review, playbook falsification, supplier re-measurement, T2→T1 ratchet review | 90 days of ledger + outcomes | `meetings/<date>-qbr.md`; playbook diffs |

---

## 3. Department charter table

Thresholds below are **proposed defaults** for Anabtawi, derived from the practice described in the sources plus the constitution's existing guardrails. They are starting values, not verified industry constants.

| Department | Owns | Key metrics | Weekly SOPs | Decision thresholds (proposed) |
|---|---|---|---|---|
| **Finance** | Unit economics, P&L by SKU, cash, fee forensics, reimbursements, targets | Contribution margin/unit after ads, TACoS, fee-line % of revenue, cash days, forecast accuracy (MAPE) | Fri CM refresh; Wed fee anomaly + reimbursement scan; monthly full P&L; monthly target revision | CM after ads < 15% → flag; < 10% → mandatory price/cost proposal. Any fee line > 3% of SKU revenue → structural fix. Reimbursement claims filed within **60 days** (window compressed from 18 months) [REPORTED — https://www.leviathansellers.com/blog/amazon-fba-reimbursement-policy-2026 ; https://www.ecomengine.com/blog/fba-reimbursement-policy] |
| **Supply Chain / Inventory** | Forecast, reorder points, POs, FBA shipments, expiry/FEFO, restock limits, capacity | Days of cover, in-stock rate, IPI, sell-through, aged units, stranded units, expiry runway | Tue forecast + reorder; daily cover check; weekly FEFO aging; monthly capacity/limit review | Reorder when cover ≤ (lead time + safety). Hero cover floor 14 days, seasonal buffer 6 weeks (per AGENTS.md). Never let a SKU fall under **28 days of supply** on the 30- and 90-day measures (low-inventory-level fee trigger) [REPORTED — https://www.inventoryhero.ai/guides/amazon-fba-reorder-point]. Never exceed **22 weeks** of cover account-wide (storage-utilisation surcharge) [REPORTED — https://mysellerhub.com/blog/amazon-fba-storage-fees-explained-base-utilization-and-aged-inventory-surcharges/] |
| **Advertising** | All SP/SB/SD campaigns, bids, budgets, negatives, placements, dayparting | ACoS, TACoS, CPC, CTR, CVR, share of voice, % sales from ads, new-to-brand | Mon harvest + negatives + promotions; Thu bid/budget check; daily pace check; monthly structure review | T1 only: bid ±15%, budget +25%/action to daily cap, one change per target/24h, negatives above statistical threshold (per AGENTS.md). New campaigns = T2. Daily total cap CAD 150 |
| **Catalog / Listing** | Titles, bullets, A+, images, video, backend keywords, variations, listing health | Sessions, unit session %, SQP click share & purchase share, suppression count | Mon SQP diagnosis; Thu hygiene sweep; monthly A+/image test readout | Any listing text/image change is **T2** (per AGENTS.md). CVR drop > 25% w/w on a top-10 ASIN → mandatory diagnosis within 24h |
| **Pricing & Market Intel** | Price bands, Automate Pricing rules, promos, coupons, deals, competitor watch | Buy Box share, price vs band, promo ROI, elasticity estimate | Tue price/promo review; daily Buy Box + offer-change watch; weekly Keepa competitor pass | All price changes **T2**. Amazon's own floor: human authorisation for >20% moves in 24h and bulk edits ≥500 ASINs — no tier may be looser. Never use scraped data (per AGENTS.md); Keepa API + SP-API pricing only |
| **Customer** | Reviews, VOC/NCX, returns analysis, buyer messages, Request-a-Review | NCX rate, return rate + reasons, review velocity, star average, response time | Mon VOC/returns review; daily new-negative-review scan | Buyer messages **T2** (per AGENTS.md). Request-a-Review may be automated on eligible orders as a bounded T1 class once ratcheted — see §8 |
| **Account Health & Compliance** | AHR, policy violations, IP complaints, food/label compliance, appeals | AHR score, violation count by severity, suppression count, ODR | Daily exception scan; weekly compliance file review; monthly label/reg audit | AHR < 200 → "At Risk"; < 100 → suspension risk [REPORTED — https://ensobrands.com/amazon-account-health-rating/]. Any violation → same-day T3 packet. Appeals/POA are **T3** |
| **Expansion** | US launch, Walmart, new marketplaces, brand registry, importer setup | Milestone burn-down, launch-readiness %, first-shipment ETA | Wed workstream review | New marketplaces **T3**. Contracts, payment terms **T3** |
| **Creative** | Photography, video, packaging, Ramadan/Eid seasonal assets | Asset production vs plan, CTR/CVR lift per test | Fortnightly production standup | Publishing any asset is **T2** (it's a listing change) |
| **Chief of Staff / CEO layer** | Cadence, WBR/MBR/QBR, approval queue, ranked daily decision list, ratchet | Decisions/week, approval latency, rejection rate, stale-state count | Mon WBR; Fri approval hygiene; monthly MBR; quarterly QBR + ratchet | Proposal expiry 48h. T2→T1 ratchet: 30 days + ≥20 approvals + <5% rejection |

---

## 4. Food and grocery specifics

This is where a generic Amazon playbook gets a food brand suspended. The rules below are the ones that actually bite.

### 4.1 Expiry, shelf life and FBA date rules

- **105 days remaining shelf life at the moment of receipt** at the fulfilment centre is the standard FBA requirement for expiration-dated products; shipments arriving with less are rejected [REPORTED — https://fivestarcommerce.com/guide-on-the-expiration-date-on-amazon-fba/ ; https://help.scanpower.com/en/articles/9854207-amazon-product-expiration-guidelines].
- Amazon **disposes of units automatically at ~50 days before expiry** [REPORTED — same sources]. So the *sellable* window is roughly `shelf life − 105 − 50` days minus transit.
- Multi-packs and case packs: the expiry date must appear **on the outer box and on every individual unit inside**, and the outer date must equal the **earliest** date inside [REPORTED — https://www.sitruna.com/guides/sitruna-guides-fba-requirements ; https://www.stratosphereprep.com/amazon-fba-bundles-prep-guide-2026].
- **Design consequence:** forecast against *effective sellable life*, not calendar life; FEFO must be a first-class state file. A 12-month product with 45-day transit has ~165 sellable days. That is the real planning horizon.

### 4.2 Meltables

Amazon does not accept meltable inventory into FBA between **15 April and 15 October**; the acceptance window is 16 October – 14 April. Meltable stock left in fulfilment centres after 15 April may be marked unfulfillable and disposed of for a fee from 1 May. "Meltable" covers heat-sensitive goods that melt above ~155°F — chocolate, gummies, jelly- and wax-based products [REPORTED — https://www.sellerassistant.app/blog/amazon-meltable-fba-inventory-all-you-need-to-know/ ; https://riverbendconsulting.com/blog/amazon-meltable-policy/ ; https://amzprep.com/amazon-meltable-inventory/].

**Design consequence:** any SKU with chocolate, chocolate-coated halva, or gummy/jelly sweets carries an annual ~1 April inbound deadline and a 15 April removal deadline. Ramadan 2027 sits safely inside the window, but the lunar drift moves Ramadan ~11 days earlier each year and by the early 2030s it lands inside the blackout. Encode it as a calendar rule now.

### 4.3 Gating and category approval

Grocery & Gourmet Food is gated: Professional account plus category approval, with supplier invoices dated within 180 days showing 10+ units, and sometimes GFSI/HACCP and FDA evidence. Established accounts with clean metrics are sometimes auto-approved [REPORTED — https://litcommerce.com/blog/selling-groceries-on-amazon/ ; https://gigacommerce.co/amazon-ungating/]. Grocery must be listed under the **manufacturer's UPC**, sealed and shipping-suitable [REPORTED — same].

### 4.4 Canada — CFIA / SFCR labelling

- Bilingual (EN+FR) labelling is mandatory for common name, net quantity, ingredients, allergens, Nutrition Facts table (in Health Canada's prescribed bilingual format), country of origin, and the responsible Canadian party's name and address [REPORTED — https://www.nexreg.com/canadian-food-labelling-requirements-guide ; https://businesscentralconsultants.com/blog/bilingual-labelling-compliance-sfcr-canadian-food-manufacturers/].
- **Front-of-package nutrition symbol:** transition ended 31 Dec 2025; from **1 Jan 2026** all labels must comply, symbol required where saturated fat, sugars or sodium reach ≥15% DV [REPORTED — https://www.nsf.org/ca/en/knowledge-library/calling-canadas-food-businesses-ready-labelling-changes]. **Live now, and it applies to the existing Canadian catalogue** — halva, date syrup and tahini plausibly cross the thresholds.
- Importing food into Canada requires an SFC licence and CFIA/CBSA compliance [REPORTED — https://jwsmith.com/guides/how-to-import-food-into-canada].

### 4.5 United States — FDA, FSVP, prior notice

- **FSVP:** list imported food on Amazon US and FDA treats you as the importer, with the full FSVP verification obligation. A foreign brand must appoint a **US-based FSVP agent** [REPORTED — https://qualitysmartsolutions.com/blog/what-amazon-usa-sellers-need-to-know-about-fsvp-compliance ; https://globalimportagent.com/fsvp-amazon-fda-agent-gad01/].
- **Prior Notice:** food shipments need an FDA Prior Notice confirmation number or cargo is held and detained; FDA facility registration feeds the process [REPORTED — https://www.fda.itbhdg.com/blog/fulfillment-by-amazon-fba/].
- **Amazon will not act as importer of record for FBA inventory** — any shipment, any size, any origin. The Canadian entity must register as US IOR (CBP Form 5106) and post a customs bond, carrying full liability for classification and entry [REPORTED — https://carraglobe.com/importer-of-record-amazon-fba/].
- **Hazmat: UNKNOWN.** Could not confirm which SKUs would be flagged; alcohol-containing extracts and pressurised/flammable items are the usual triggers, and Amazon runs a dangerous-goods review on new ASINs. Needs a per-SKU check at listing time.

### 4.6 Bundles and multi-packs

Since **14 October 2024**, consumables bundles may only be listed if created and offered by the original manufacturer, who must be brand owner of every item; mixed-manufacturer, "Generic"-brand and reseller-created bundles are barred in grocery, pet, baby and health & beauty [REPORTED — https://myfbaprep.com/blog/amazon/navigating-amazons-new-consumables-bundling-policy/ ; https://alpharepricer.com/blogs/amazon-fba-bundling-compliance-packaging-buy-box/]. Anabtawi owns its brand, so **multi-packs and gift sets remain available** — the cleanest lever for raising AOV into Ramadan without touching unit price. Virtual Bundles are the lower-risk option for cross-SKU sets.

### 4.7 Subscribe & Save economics

Sellers choose the funded tier (commonly 5% or 10%; some categories offer more). When a customer's delivery contains 5+ subscribed items, Amazon funds an additional 5% at no cost to the seller. There is no separate participation fee — only standard FBA fees. Grocery, beauty and pet dominate S&S volume (~70%) [REPORTED — https://www.themarketplaceguys.com/en/blog/amazon-subscribe-and-save ; https://amzdudes.com/all-you-need-to-know-about-amazon-subscribe-save-program-for-sellers/]. The caution worth encoding: reported average subscriber lifetime in CPG is only **2.4–3.8 deliveries** [REPORTED — https://www.velocitysellers.com/2026/07/05/amazon-subscribe-save-data-deep-dive-2026/]. So S&S is a simple LTV test — at 10% funded over 3 deliveries you pay ~30% of one order's revenue to acquire ~2 extra orders. Usually good for a pantry staple, usually bad for a gift item.

---

## 5. The Amazon US launch from a Canadian base

### 5.1 NARF / Remote Fulfillment — and why it is the wrong tool here

Remote Fulfillment with FBA (the programme formerly known as NARF) fulfils **amazon.ca and amazon.com.mx** orders from **US** inventory. It runs US → CA/MX, not CA → US, and remote fulfilment fees are materially higher than domestic FBA [REPORTED — https://www.ecomcrew.com/what-is-amazons-narf-beta-program/ ; https://www.frisbi.com/blog/the-ultimate-guide-to-amazons-north-american-remote-fulfillment-narf-program]. It serves Canada from a US base, not the reverse. For a Ramadan launch with a seasonal spike and Prime-speed expectations, **separate US FBA inventory is the only serious option**. NARF matters *later*: once US volume dwarfs Canadian, running Canada off US stock could retire a whole inbound lane — a 2028 conversation, and one that collides with CFIA bilingual labelling, since US-held stock still needs compliant Canadian labels.

### 5.2 Launch mechanics worth encoding

- **Brand Registry:** enrol the brand in the US marketplace; a Canadian (CIPO) trademark does not automatically confer US Brand Registry rights and a USPTO mark is generally needed for the US store [REPORTED — https://gobrandwoven.com/resources/articles/amazon-brand-registry-trademark-application-benefits-and-barriers/]. **If a USPTO application is not already filed, this is the long pole** — examination timelines are months, not weeks. UNKNOWN: current USPTO pendency; not confirmable today.
- **Pricing parity:** no contractual price-parity clause remains in the US BSA (removed 2019), but the **Marketplace Fair Pricing Policy** is enforced independently — Amazon can suppress the Featured Offer, remove the offer, or suspend selling privileges over a price significantly higher than elsewhere, on or off Amazon [REPORTED — https://www.pattern.com/blog/amazons-price-parity-s-4-seller-term-has-changed ; https://www.kaspien.com/blog/amazon-fair-pricing-policy-which-marketplaces-does-amazon-price-match/]. Practically: US and CA prices must be defensible against each other after FX, and a Walmart Canada price below the Amazon price can suppress the Buy Box. Price the US catalogue in USD from US unit economics, not by converting CAD.
- **Sales tax:** Amazon collects and remits as marketplace facilitator in essentially all states; FBA placement still creates physical presence in states you did not choose, and non-marketplace sales remain the seller's own filing obligation [REPORTED — https://salaccounting.ca/blog/us-sales-tax-requirements-for-canadian-sellers/].
- **Vine:** requires Brand Registry, FBA, an image and description, and fewer than 30 reviews; up to 30 units per parent ASIN. Reported 2026 change: enrolment fee reduced to **$0 for products under $100** from March 2026 ($200 per parent ASIN for $100–$499; $500+ adds $100 per child ASIN); sellers are not charged until the first Vine review publishes and not charged at all if none arrives within 90 days [REPORTED — https://sellercards.com/blog/amazon-vine-program-eligibility-2026 ; https://www.bellavix.com/amazon-vine-program-costs-in-2026-what-sellers-and-vendors-need-to-know/]. For a food catalogue almost certainly under $100/unit, **Vine is effectively free and should be enrolled on every US ASIN at launch**.
- **FBA New Selection Program (2026 version, live 30 July 2026):** instant referral-fee credits (capped to 10% on the first 100 units, 5% on the next 100), 120 days of free storage, free returns and liquidations on the first 200 units, no low-inventory-level fee or storage-utilisation surcharge on those units, plus $50 coupon-fee credit and $75 Vine credit. A **31 October enrolment deadline** is reported [REPORTED — https://novadata.io/resources/news/amazon-fba-new-selection-program-expansion-july-30-2026 ; https://damlawfirm.com/blog/amazon-fba-new-selection-program-2026/ ; https://datadive.tools/amazon-new-selection-program-2026/]. **UNKNOWN whether that deadline is a 2026 one-off or annual, and whether it is per-marketplace.** If US ASINs must exist to enrol by 31 Oct 2026, US listing creation pulls forward by ~10 weeks. **Confirm this first.**
- **Review strategy, compliant:** Request-a-Review on every eligible order is the sanctioned mechanism; using it means not also sending review requests via Buyer-Seller Messaging. Neutral, non-incentivised inserts are tolerated; anything that asks for a *positive* review, offers reward, or filters by sentiment is review manipulation [REPORTED — https://salesduo.com/blog/how-to-get-reviews-on-amazon/ ; https://www.goatconsulting.com/merchandising/amazon-product-review-guidelines ; https://www.sellersprite.com/en/blog/amazon-review-manipulation-suspension].
- **Launch PPC:** auto + manual-exact per hero ASIN from day one, ~$30–50/day each on ~5 priority keywords, launch ACoS budgeted **40–60% above the mature target** and tightened as reviews and rank build; keep ≥15–30 clicks/day on the hero campaign or data accrues too slowly to optimise [REPORTED — https://www.velocitysellers.com/2026/06/29/amazon-product-launch-strategy-2026-first-90-days/ ; https://www.amazongrowthlab.com/blogs/amazon-product-launch-strategy]. The "honeymoon" (~2–4 weeks of elevated visibility) is folklore with a grain of truth — do not bet the plan on it.

### 5.3 Ramadan 2027 US launch — backward schedule

Anchors: **Ramadan begins ~8 Feb 2027; Eid al-Fitr ~9–10 Mar 2027** [REPORTED, §0]. Pre-Ramadan shopping builds **2–3 weeks before** the start [REPORTED — https://www.golocad.com/blog/increase-sales-during-ramadan-in-the-middle-east/], so the demand curve turns up around **mid-to-late January 2027** and peaks in the first half of Ramadan. Sea freight to the US East Coast plus customs plus FBA receiving realistically consumes **6–10 weeks** door-to-sellable [REPORTED — https://ship4wd.com/logistics-shipping/how-long-does-freight-shipping-take ; https://www.freightamigo.com/en/blog/logistics/understanding-shipping-times-a-comprehensive-guide/ ; FBA receive adds 3–14 days per https://www.inventoryhero.ai/guides/amazon-fba-reorder-point]. The brief's "stock in US FBA by mid-January" is correct and, with the Feb 8 start, is **tight rather than comfortable**.

| When | Milestone | Owner | Why this date |
|---|---|---|---|
| **Sep–Oct 2026 (now)** | Confirm FBA New Selection 2026 enrolment deadline and whether US ASINs must exist to qualify | Expansion | Reported 31 Oct deadline could force everything forward [REPORTED, §5.2] |
| **Sep 2026** | USPTO trademark status check; file if not filed | Expansion / Rami (T3) | Brand Registry gates Vine, A+, SQP, and brand protection |
| **Oct 2026** | US entity/tax decisions, CBP Form 5106 IOR registration, customs bond, US FSVP agent appointed, FDA facility registration confirmed | Expansion / Rami (T3) | Amazon will not be IOR; no bond = no entry [REPORTED, §4.5] |
| **Oct 2026** | US grocery category approval application (invoices, GFSI/HACCP if requested) | Compliance | Gated category; approval latency unknown |
| **Oct–Nov 2026** | US label artwork finalised: FDA nutrition panel, allergens, US English; production run scheduled | Creative + Compliance | Canadian bilingual labels are not US-compliant; separate SKU/label run |
| **Nov 2026** | PO issued to supplier for US launch quantity (Ramadan quantity + 6-week seasonal buffer per AGENTS.md) | Supply Chain → Rami (T2/T3) | Production + booking must precede sailing |
| **Nov–Dec 2026** | US listings created (draft), images, A+ content, backend keywords; keyword research off Canadian SQP + US competitor set | Catalog | Listings must be live before Vine and before inventory arrives |
| **~1 Dec 2026** | Cargo sails | Supply Chain | 6–10 weeks door-to-sellable ⇒ latest safe sailing for mid-Jan availability |
| **Dec 2026** | Prior Notice filed per shipment; FSVP records assembled | Compliance | Missing PN = FDA hold [REPORTED, §4.5] |
| **Early Jan 2027** | Port arrival, customs clearance, transload, FBA inbound plan created; inbound placement option chosen | Supply Chain | Placement fee vs split-shipment trade-off (§6) |
| **~15 Jan 2027** | **Stock checked in and sellable in US FBA** | Supply Chain | Hard gate. All downstream dates depend on this |
| **~15 Jan 2027** | Vine enrolled on every eligible US ASIN (30 units/parent) | Catalog | Vine reviews take weeks; enrol the day stock is live |
| **~18 Jan 2027** | PPC live: auto + manual-exact per hero ASIN, launch ACoS 40–60% above mature target | Advertising | ~3 weeks of learning before demand turns |
| **~25 Jan 2027** | Demand-curve inflection: shift budget from discovery to defence; Ramadan/Eid creative live; S&S enabled on pantry staples | Advertising + Creative | 2–3 weeks pre-Ramadan build-up [REPORTED] |
| **~1 Feb 2027** | Restock decision point #1: is a second air/expedited shipment needed? | Supply Chain → Rami | Air freight is the only lever left after this date |
| **8 Feb 2027** | **Ramadan begins** | — | Peak sell-through, days 1–15 |
| **~20 Feb 2027** | Eid gifting push: multi-packs/gift sets, coupons, Eid creative | Pricing + Creative | Eid demand is gift-shaped, not pantry-shaped |
| **9–10 Mar 2027** | **Eid al-Fitr** | — | Demand cliff immediately after |
| **Mar–Apr 2027** | Post-season: sell-down plan, removal/liquidation of surplus, **meltable removal before 15 Apr**, retrospective into playbooks | Supply Chain + CoS | Aged-inventory and meltable deadlines [REPORTED, §4.2] |

---

## 6. Advertising for a 10–15 winner catalogue

### 6.1 Architecture

The consensus structure for a small catalogue is deliberately boring, and that is why it automates well:

1. **SP Auto** per hero ASIN — discovery engine. Let it run 7–14 days before harvesting, depending on click volume [REPORTED — https://ecombrainly.com/amazon-ppc-campaign-structure/ ; https://adlabs.app/guides/amazon-campaign-structure-guide/].
2. **SP Manual Broad/Phrase** — mid-funnel expansion of harvested themes.
3. **SP Manual Exact** — proven converters, bid aggressively, tight control.
4. **SP Product Targeting (ASIN)** — competitor conquest and own-catalogue defence.
5. **Sponsored Brands** — brand headline on category terms; the natural home for Ramadan/Eid seasonal creative and for a Brand Store landing page.
6. **Sponsored Display** — remarketing and defensive placement on own detail pages; the cheapest way to protect a hero ASIN's page from competitor SD.

**The negative-keyword bridge is the load-bearing rule.** When a search term in the auto campaign produces **3+ sales**, promote it to Manual Exact *and simultaneously add it as negative exact in the auto campaign*, or the two campaigns bid against each other and inflate your own CPC [REPORTED — https://ecombrainly.com/amazon-ppc-campaign-structure/ ; https://sellermetrics.app/negative-keywords-amazon-ppc/ ; https://www.off-hours.app/blog/amazon-ppc-campaign-structure]. This is a mechanical rule an agent can execute perfectly and a human forgets weekly. It is the single best candidate for early T1 automation after bid hygiene.

### 6.2 Rule-based bid management the tools encode

Pacvue and Perpetua both sell rule-based *plus* algorithmic bidding, dayparting, share-of-voice tracking, budget forecasting, and "action queues" that route reporting signals into governed change workflows [REPORTED — https://pacvue.com/marketplaces/pacvue-for-amazon/ ; https://novadata.io/resources/blog/best-amazon-ppc-software ; https://lumian.ai/resources/top-amazon-ppc-automation-software-2026]. The specific rule *thresholds* those platforms ship with are not published — **UNKNOWN**; I found only feature descriptions, no rule cards. So the ruleset below is a design proposal consistent with the constitution's T1 envelope, not a copied industry standard:

| Condition (rolling 14 days unless noted) | Action | Tier |
|---|---|---|
| Target has ≥ 2× breakeven-CVR clicks and 0 orders | Reduce bid 15%; if it recurs twice, pause target | T1 |
| Target ACoS > 1.5× SKU target ACoS, ≥ 15 clicks | Reduce bid 15% | T1 |
| Target ACoS < 0.6× SKU target ACoS, ≥ 3 orders | Raise bid 15% | T1 |
| Campaign hits budget before 18:00 local, ACoS at/below target | Raise budget +25%, capped by daily cap | T1 |
| Campaign spends < 60% of budget for 7 days | Reduce budget to 120% of actual spend | T1 |
| Search term with ≥ 3 orders in auto/broad | Promote to Manual Exact + add negative exact in source | T1 (once ratcheted; T2 initially) |
| Search term with clicks ≥ 2× breakeven and 0 orders | Add negative exact | T1 above statistical threshold |
| Placement (top-of-search / rest-of-search / product pages) ROAS spread > 30% | Adjust placement modifier ≤ 20 pts per change | T2 initially |
| Any new campaign, new ad group, new campaign type | Propose | **T2 always** |
| Total daily spend projected > CAD 150 cap | Proportional throttle across campaigns | T1 (protective) |

**One change per target per 24 hours**, per AGENTS.md. Enforce it in the runner, not in the prompt.

**Dayparting:** worth doing only once there is enough hourly data to be significant. For a food brand, the obvious Ramadan-specific play is shifting budget toward late-evening hours (post-iftar browsing) during Ramadan — but I found **no data** confirming that pattern on Amazon US/CA. **UNKNOWN.** Treat it as a hypothesis to test with a 2-week A/B in Feb 2027, not a rule to ship.

**Budget pacing:** hold TACoS as a *range* rather than a ceiling — 10–15% composite for an established brand, higher during launch and Ramadan build-up, lower in the post-Eid trough [REPORTED — https://pare.so/blog/amazon-tacos-range-not-ceiling-ppc-hire-signal-2026].

### 6.3 The Amazon Ads MCP server

Amazon opened **beta access to an official Amazon Ads MCP Server on 2 February 2026**, giving anyone with Ads API credentials agent-driven campaign creation, bid management, reporting, account settings and billing access across SP/SB/SD/DSP/AMC — with explicitly stated compatibility with Claude, ChatGPT and Gemini and with custom agents [REPORTED — https://www.sellerlabs.com/blog/amazon-ads-mcp-server-what-sellers-need-to-know/ ; https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta ; https://sellershorts.com/resources/ai-for-amazon-sellers/amazon-ads-mcp-server-guide]. This is the sanctioned, policy-clean path for the Advertising department's T1 authority and directly matches AGENTS.md §3. **It requires Ads API credentials**, which is a separate registration from SP-API — worth confirming whether DataDoe's Ads access satisfies this or whether Rami needs his own Ads API app.

---

## 7. Inventory planning

### 7.1 Formulas

- **Reorder point = (average daily sales × lead time in days) + safety stock** [REPORTED — https://www.spscommerce.com/community/articles/amazon-reorder-point ; https://sellerlegend.com/glossary/reorder-point].
- **Safety stock = (max daily sales × max lead time) − (avg daily sales × avg lead time)** — sizes the buffer to the worst realistic case and captures both demand spikes and freight delay [REPORTED — https://www.inventoryhero.ai/guides/safety-stock-amazon-fba].
- **Lead time must include FBA check-in**, which adds **3–14 days** most sellers omit [REPORTED — https://www.inventoryhero.ai/guides/amazon-fba-reorder-point]. For food imports add customs and, for the US, FDA prior-notice/hold risk.
- **Forecasting:** a weighted moving average with a per-month seasonality index is adequate and auditable for a 50-SKU catalogue with strong, known seasonality (Ramadan/Eid, Christmas, BFCM). I found **no evidence** that tool-based ML forecasting beats a well-specified seasonal WMA at this scale — **UNKNOWN**. The advantage of WMA for this design is that an agent can show its work: `forecast = WMA(last 8 weeks) × seasonality_index(month) × trend_factor`, every input citable. Because the Islamic calendar drifts ~11 days a year, **the Ramadan index must be keyed to the lunar date, not the Gregorian month** — a Gregorian seasonality index will systematically mis-time Anabtawi's biggest season. This is a real modelling requirement, not a detail.

### 7.2 The 2026 fee cliffs the forecast must respect

| Constraint | Threshold | Reported effect |
|---|---|---|
| **Low-inventory-level fee** | Both 30-day and 90-day historical days-of-supply below **28 days** | $0.32–$2.09 per unit; from 2026 assessed at **FNSKU** level rather than parent ASIN [REPORTED — https://novadata.io/resources/news/amazon-low-inventory-level-fee-2026 ; https://www.prepvia.com/blogs/amazon-low-inventory-level-fee-explained] |
| **Storage utilisation surcharge** | Account-level cover above **22 weeks** (13-week avg inventory volume ÷ 13-week avg shipped volume ÷ 7) | Standard-size $0.44/cu ft at 22–28 weeks rising to $1.88 above 52 weeks. Exempt: sellers <365 days since first FBA shipment, Individual accounts, and accounts averaging <25 cu ft [REPORTED — https://mysellerhub.com/blog/amazon-fba-storage-fees-explained-base-utilization-and-aged-inventory-surcharges/ ; https://www.sellerapp.com/blog/amazon-fba-fees-calculator-guide/] |
| **Aged inventory surcharge (US)** | From **181 days**, escalating; reported $1.50/cu ft at 271 days and $6.90/cu ft (or $0.15/unit, greater) past 365 days | Charged **in addition to** base storage, so a Q4 aged unit pays peak base + full surcharge [REPORTED — https://www.conversionperk.com/amazon-fba-storage-fees-2026/ ; https://warehousingcosts.com/guides/amazon-fba-storage-fees] |
| **Aged inventory surcharge (Canada)** | Reported to begin at **271 days**, not 181 | Materially more forgiving than the US [REPORTED — https://ecomcalctools.com/blog/fees-amazon/amazon-fees-canada-2026/] |
| **Base monthly storage (US 2026)** | $0.78/cu ft Jan–Sep; **$2.40/cu ft Oct–Dec** | Q4 tripling [REPORTED — https://www.conversionperk.com/amazon-fba-storage-fees-2026/] |
| **Base monthly storage (Canada 2026)** | ~CAD $1.02/cu ft Jan–Sep, higher in Q4; 3.5% fuel/logistics surcharge applies | No general 2026 increase to CA referral/base FBA fees was announced [REPORTED — https://ecomcalctools.com/blog/fees-amazon/amazon-fees-canada-2026/] |
| **Inbound placement service fee** | Updated 15 Jan 2026; standard-size minimal-split rose ~$0.05/unit on average; small-standard now 2 weight bands, large-standard 5 | Verify per ASIN in the Revenue Calculator [REPORTED — https://amzprep.com/amazon-inbound-placement-fees/ ; https://www.goatconsulting.com/amazon-fulfillment/amazon-fba-fee-changes-for-2026] |
| **Prep and labelling services** | Discontinued: **US from 1 Jan 2026**, **Canada from 1 Jul 2026** | Inventory must arrive shelf-ready; a prep partner or in-house prep is now mandatory [REPORTED — https://www.sellerapp.com/blog/amazon-fba-fees-calculator-guide/ ; https://ecomcalctools.com/blog/fees-amazon/amazon-fees-canada-2026/] |
| **IPI / capacity** | Minimum threshold reported at **400**; 500+ associated with better capacity allocation. Mid-2025 tightening reportedly cut storage allowance from six months to five months of forecast sales and reactivated ASIN-level restock limits | [REPORTED — https://www.sellerlabs.com/blog/amazon-ipi-score-2026/ ; https://novadata.io/resources/blog/amazon-fba-restock-limits] |

**The corridor this creates is narrow and is the core inventory problem:** stay above 28 days of cover per FNSKU, below 22 weeks account-wide, out of the 181-day aged band, and above the 105-day-remaining shelf-life rule at receipt — all at once, for a seasonal food brand whose demand triples for four weeks a year. **An operator cannot hold this corridor by intuition. This is the strongest argument in the whole report for automating supply chain first.**

---

## 8. Pricing, promotions, and competitor intelligence

- **Automate Pricing** is free in Seller Central, supports predefined rules ("beat the Buy Box price", "stay below lowest price") and custom rules, with mandatory **minimum** and optional **maximum** price boundaries, applied per SKU or in bulk, executing continuously; it can also reference external (off-Amazon) prices [REPORTED — https://wiseppc.com/blog/automate-pricing-rules/ ; https://salesduo.com/blog/how-to-use-amazon-automated-pricing/]. Automated pricing rules are also manageable via SP-API [REPORTED — https://developer-docs.amazon/sp-api/docs/manage-automated-pricing-rules]. **This is the right home for the per-SKU price band in `products/<sku>.md`:** set min/max in Amazon's own tool, let Amazon execute inside the band, and make any band *change* a T2 proposal. That gives continuous protection without any agent touching price.
- **Competitor monitoring without scraping:** SP-API `ANY_OFFER_CHANGED` (fires on price changes among the top 20 offers or the Featured Offer) and `PRICING_HEALTH` (fires when your offer becomes Featured-Offer-ineligible due to external competition or an atypically high price) [REPORTED — https://developer-docs.amazon/sp-api/docs/pricing-faq ; https://www.deltologic.com/blog/harnessing-amazon-sp-api-notifications-api-for-your-amazon-business]. Keepa provides historical price/BSR via a token-metered API from ~€49/month for 20 tokens/minute, with a hosted MCP server on the same key [REPORTED — https://revenuegeeks.com/software/keepa/api ; https://keepa.com/api-docs/]. Together these fully satisfy AGENTS.md §6.2 without a single scraped page.
- **Note on SP-API cost:** a **$1,400 annual third-party developer subscription fee from 31 January 2026** is reported [REPORTED — https://blog.ppcassist.com/2025/12/14/amazon-sp-api-pricing-2026-optimization-guide/]. **UNKNOWN** whether this applies to a seller's own private developer registration or only to third-party app publishers. This materially affects the "register for SP-API" decision and should be confirmed before budgeting.
- **Promotion fee math (US, reported):** coupons cost **$5 flat per coupon created + 2.5% of coupon sales** (changed 2 June 2025 from $0.60/redemption); Lightning Deals **$70/day + 1% of deal-attributed sales, variable capped at $2,000**; peak events revert to fixed premium fees (~$500 Lightning, ~$1,000 Best Deal) [REPORTED — https://nivoads.com/blog/amazon-coupon-deals-fees-2025/ ; https://www.adverio.io/coupons-vs-best-deals-vs-lightning-deals-amazon/ ; https://capybaras.agency/types-of-discounts-on-amazon-complete-2026-guide/]. Prime Exclusive Discounts are cheaper and require less depth [REPORTED — same].
  **The ROI test an agent can run:** a promotion is approved only if `incremental units × contribution margin per unit > (discount × total promo units) + fixed fee + variable fee`, with "incremental" estimated from a matched pre-period, and with the rank/review halo stated as an explicitly separate, unquantified argument. Never let the halo carry the decision silently.
- **Promotion calendar:** Prime Day (2026 ran late June, four days [REPORTED — https://www.consumerreports.org/money/sales-promotions/best-amazon-prime-day-lightning-deals-a5109927191/]); an autumn Prime event; BFCM; Christmas; and for Anabtawi the two that matter most, **Ramadan (8 Feb – 9 Mar 2027)** and **Eid al-Fitr (~9–10 Mar 2027)**. Ramadan e-commerce activity in Muslim-majority markets is reported to surge 30–50% over baseline, with Amazon Saudi reporting +38% orders in Ramadan 2026 [REPORTED — https://themiddleeastinsider.com/2026/03/14/saudi-ramadan-economy-2026-spending-retail-trends/ ; https://www.golocad.com/blog/increase-sales-during-ramadan-in-the-middle-east/]. **These are MENA figures, not North American diaspora figures — the magnitude does not transfer, only the shape.** Anabtawi's own Canadian 2026 Ramadan data is the only reliable index for the US 2027 forecast, and building that index from `state/` and DataDoe history should be a Supply Chain task this month.
- **MAP:** Brand Registry does **not** enforce MAP or unilateral pricing policies on your behalf, and does not override Fair Pricing enforcement [REPORTED — https://www.enceiba.com/post/demystifying-amazon-brand-registry-what-it-does-and-what-it-doesn-t-do ; https://www.brandalignment.com/amazon-price-parity/]. If Anabtawi has wholesale/retail distribution, MAP is a contract matter (T3), not an Amazon feature.

---

## 9. Compliance and account health

**Account Health Rating** is a 0–1,000 near-real-time score rolling up policy compliance, order performance and shipping metrics: ≥200 healthy, 100–199 at risk, <100 suspension risk. Violations carry severity (critical/high/medium/low) and deduct points [REPORTED — https://ensobrands.com/amazon-account-health-rating/ ; https://www.sellerlabs.com/knowledge-base/how-amazon-account-health-rating-ahr-works-the-complete-seller-s-guide/].

**What actually causes suspensions in food:** expired-product complaints, product-safety complaints, and authenticity/IP complaints. A single serious safety complaint can trigger investigation or listing removal; multiple can suspend the account [REPORTED — https://amazonsellersappeal.com/expired-products-complaints/ ; https://theappealguru.com/amazon-suspension-for-food-and-product-safety-issues-what-are-they/]. For a 105-day-shelf-life-gated, FEFO-dependent food catalogue, **expiry is the top existential risk and it is also the most automatable to prevent.**

**Plan of Action SOP** (the shape appeals must take): (1) root cause, stated specifically; (2) immediate corrective action — remove/dispose affected stock, change supplier; (3) **systemic** preventive action — FIFO/FEFO enforcement, automated expiry checks, revised SOPs, inspection cadence; (4) documentary evidence [REPORTED — https://amazonsellersappeal.com/expired-products-complaints/ ; https://www.amazonsellers.attorney/safety-complaint-suspensions.html]. Note the irony worth exploiting: "we automated expiration checks and enforce FEFO through a documented system with an immutable action log" is *exactly* what Amazon wants to read in a POA — and this repo's `ledger/actions.jsonl` produces that evidence as a by-product.

**Monitoring:** VOC/NCX weekly, AHR and violations daily, plus SP-API `LISTINGS_ITEM_ISSUES_CHANGE` for suppression events (**note: v1.0 closes to new subscriptions 14 Aug 2026 and stops delivering 26 Aug 2026 — use the current version**) [REPORTED — https://developer-docs.amazon.com/sp-api/changelog].

**Appeals, POAs, and IP complaint responses stay T3.** They are legal writing under time pressure with account-ending downside; an agent should assemble the evidence packet and draft, and Rami should send.

---

## 10. What the AI departments should own end-to-end vs. propose

Judged from the position of a solo operator who wants zero babysitting: **automate the things that are reversible, high-frequency, and rule-shaped; propose the things that are irreversible, low-frequency, or judgement-shaped.** The failure mode to avoid is not "the agent did something wrong" — it is "the agent generated 40 proposals a week and the operator became a rubber stamp." A rubber-stamped T2 is worse than a well-guardrailed T1, because it launders automation through a human who is not actually reading.

| Class | Own end-to-end (T0/T1) | Propose (T2) | Rami only (T3) |
|---|---|---|---|
| **Monitoring & reporting** | Everything. All state files, all metric assembly, the ranked daily decision list, anomaly detection, WBR/MBR deck generation | — | — |
| **Advertising** | Bid ±15%, budget +25%/action to cap, negatives above threshold, pausing zero-converting targets, budget throttling at cap, search-term harvesting (after ratchet) | New campaigns, new ad types, placement modifiers, structural rebuilds, seasonal budget step-changes | Total monthly ad budget |
| **Inventory** | Forecast, reorder-point calculation, cover/limit/fee-corridor monitoring, FEFO aging, removal-order *recommendations*, restock-limit tracking | POs, FBA shipment creation, removal/disposal orders, inbound placement choice | POs above the CAD 15,000 monthly ceiling, supplier terms |
| **Pricing** | Monitoring band breaches, Buy Box loss detection, promo ROI post-mortems, maintaining Automate Pricing rules *within* an approved band | Any price change, band changes, coupons, deals, Prime Exclusive Discounts, S&S tier changes | Anything >20% in 24h (Amazon's floor), portfolio-wide repricing |
| **Catalog** | Listing-health monitoring, keyword research, draft copy and A+ layouts, suppression detection | All published listing text, images, A+, variations, new ASINs | Brand Registry actions |
| **Customer** | Review/return/NCX analysis, root-cause attribution, drafting responses, Request-a-Review on eligible orders (strong T1 candidate after ratchet — it is a single sanctioned button with no message content) | Buyer messages, response templates, Vine enrolment | — |
| **Compliance** | Daily AHR/violation scan, label-requirement checks, expiry-risk scoring, evidence packet assembly, POA drafting | Reimbursement claims, listing reinstatement requests | All appeals, POAs, IP responses, regulatory filings |
| **Expansion** | Milestone tracking, research, document preparation, vendor comparison | Programme enrolments (New Selection, Vine) | New marketplaces, entity/tax/legal, contracts, IOR and bond |

**The three highest-value automations for this specific business, in order:**
1. **The inventory fee-and-expiry corridor** (§7). Four simultaneous constraints, weekly re-computation, real money, zero judgement required. Nothing else in the business punishes inattention this reliably.
2. **The PPC negative-keyword bridge** (§6.1). Purely mechanical, compounding, and the thing solo operators universally let slip.
3. **The daily exception scan** (§1.2). Not because each check is hard, but because doing all of them every morning at 07:15 is exactly what a human stops doing in week three.

---

## Implications for the design

1. **Fix the Ramadan date in every plan, today.** Ramadan 2027 starts ~8 February, not 17 February. Nine days out of a schedule whose critical path is ocean freight is the difference between a launch and a miss. Put the lunar calendar in `state/calendar.md` with Ramadan/Eid dates through 2032, and make the seasonality index lunar-keyed, not Gregorian.
2. **Confirm the FBA New Selection 2026 deadline before anything else.** If the reported 31 October enrolment deadline requires live US ASINs, the entire US timeline compresses by ~10 weeks, and the programme's value (referral-fee credits, 120 days free storage, waived low-inventory and utilisation fees, $75 Vine credit) is exactly the set of costs a launch incurs. This is a single question with a large answer.
3. **Supply Chain should be the first department promoted toward T1, not Advertising.** The constitution currently gives Advertising the only T1 class. But the fee corridor in §7 is where money silently leaks and where automation has the cleanest rules. Give Supply Chain T1 for *monitoring and alerting with mandatory escalation* immediately, and ratchet reorder-point recalculation and removal-order recommendation next.
4. **Put price bands in Amazon's Automate Pricing, not in an agent loop.** The band lives in `products/<sku>.md`, is mirrored into Amazon's own min/max, and Amazon executes. The agent's job is to *audit the band*, not to move prices. This satisfies the "money never moves on T1" rule while still getting continuous Buy Box protection, and it is provably policy-clean.
5. **The Ads MCP server is the sanctioned T1 surface — but check the credential path.** It is an official Amazon product, explicitly Claude-compatible, covering exactly the bid/budget/negative operations AGENTS.md permits. Confirm whether DataDoe's Ads access satisfies it or whether Rami needs his own Ads API registration; if the latter, that is a week-one task, not a someday task.
6. **Model contribution margin with the 2026 fee lines or the 15% floor is fiction.** Low-inventory-level fee, storage-utilisation surcharge, aged-inventory surcharge, inbound placement, the 3.5% Canadian fuel surcharge, and the end of Amazon prep services (US Jan 2026, Canada Jul 2026) all sit between gross margin and contribution margin. Finance's SKU model needs every one as a named line.
7. **Reimbursements became a 60-day, cost-basis game.** Reimbursement is now at manufacturing cost, not sale price, with a ~60-day claim window and stricter documentation — and Amazon substitutes its own low estimate if the per-unit cost field is blank. Two concrete actions: fill the cost field for every SKU, and make reimbursement candidate detection a weekly Finance job with a hard 60-day SLA.
8. **Design the approval queue for scarcity.** Batch T2 proposals into the Monday WBR and the Friday hygiene pass rather than streaming them. Aim for fewer than ten decisions per week reaching Rami. The 48-hour expiry in AGENTS.md is right; add a rule that any class generating more than five proposals a week is a ratchet candidate or a badly-drawn boundary.
9. **The compliance ledger is a launch asset, not overhead.** `ledger/actions.jsonl` plus the FEFO state file is the documentary evidence a food POA requires. Say so in the Compliance charter, so the department writes for that audience from day one.
10. **Copy the aggregator cadence, refuse the aggregator uniformity.** Thrasio's playbooks worked; its assumption that all FBA assets behave alike did not. The per-SKU file (`products/<sku>.md`) with its own band, cover floor, shelf life, meltable flag and seasonality index is the structural answer — the cadence is shared, the parameters never are.

---

## Open questions

1. **FBA New Selection Program 2026 — is the 31 October deadline a 2026 one-off or annual, is it per-marketplace, and must US ASINs be live to enrol?** Highest-priority unknown. [Tried: search only; could not open Seller Central.]
2. **SP-API's reported $1,400/year developer fee from 31 Jan 2026 — does it apply to a seller's own private developer registration?** Determines whether registering for SP-API is a $0 or $1,400/year decision, and therefore how much weight DataDoe carries. [Tried: search; developer-docs.amazon fetch blocked.]
3. **Does DataDoe's Ads access satisfy the Amazon Ads MCP Server's credential requirement, or is a separate Ads API registration needed?** Gates the Advertising department's entire T1 authority. [Tried: search; vendor docs not fetchable.]
4. **Which Anabtawi SKUs are meltable, and which are hazmat?** Needs a per-SKU classification pass against Amazon's own dangerous-goods and meltable definitions. Meltable SKUs acquire a hard 1 April inbound deadline and a 15 April removal deadline every year. [Not researchable without the SKU list.]
5. **Canada FOP labelling — which Anabtawi SKUs cross the 15% DV thresholds for saturated fat, sugars or sodium?** The rule has been in force since 1 January 2026, so any non-compliant label is already non-compliant. Halva, tahini, date products and sweets are the likely candidates. [Tried: inspection.canada.ca blocked; needs nutritional data per SKU.]
6. **Is the 105-day rule measured at receipt or at shipment creation, and what is Amazon's exact disposal trigger (50 days is reported, not confirmed)?** The whole FEFO model keys off these two numbers. [Tried: Seller Central blocked.]
7. **What is Anabtawi's own Ramadan 2026 Canadian lift by SKU?** The only trustworthy basis for the US 2027 forecast. MENA's reported +30–50% does not transfer to a North American diaspora market. [Available internally via DataDoe; not researched here.]
8. **What is the actual door-to-sellable lead time on Anabtawi's real supplier lane?** I used a generic 6–10 weeks. The backward schedule in §5.3 is only as good as this number, and it should be measured from the last three Canadian shipments rather than assumed.
9. **USPTO trademark status for the Anabtawi mark.** Gates US Brand Registry, which gates Vine, A+, SQP and brand protection. If unfiled, this may be the true critical path, ahead of freight.
10. **Do published rule-thresholds exist for Pacvue/Perpetua's default bid rules?** I found feature descriptions only. The §6.2 table is a design proposal, and its thresholds should be tuned against Anabtawi's own outcome data after 60 days rather than trusted as inherited wisdom.
11. **Amazon Canada restock limits and IPI — do they differ from the US?** I found US detail and Canadian fee differences, but nothing authoritative on Canadian capacity mechanics. [Tried: search; no clear source.]
