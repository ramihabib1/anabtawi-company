# 03 — How top Amazon private-label operators run a brand week to week (2026), and what an AI-department company should copy

Research date: 2026-09-06. Author: research agent. Audience: Rami (solo operator, Anabtawi brand).

---

## 0. Method, and a hard limit on verification

**I could not open a single primary source today.** The egress proxy blocked `WebFetch` for every domain tried — `sellercentral.amazon.com`, `sell.amazon.com`, `advertising.amazon.com`, `www.fda.gov`, `inspection.canada.ca`, even `en.wikipedia.org`. Search worked; fetch did not. So **VERIFIED is used zero times** here; **REPORTED** means the claim returned consistently across search summaries and secondary write-ups (URL given); **UNKNOWN** means I could not confirm and say what I tried. **Consequence:** every number here touching money, fees or policy must be re-confirmed in Seller Central by Rami (a human in a browser is legal — BSA §19 bans *automated* browsing) or via a DataDoe/SP-API read before an agent encodes it as a guardrail.

One correction to the brief up front:

> **Ramadan 2027 begins on or about Monday 8 February 2027, not 17 February.** Eid al-Fitr falls ~9–10 March 2027. [REPORTED — https://www.islamicfinder.org/special-islamic-days/ramadan-2027/ ; https://www.jordannews.jo/Section-20/Middle-East/Date-of-the-First-Day-of-Ramadan-2027-According-to-Astronomical-Calculations-52316 ; https://truecalendar.com/eid-al-fitr/2027]. Dates are provisional until the Sha'ban crescent is sighted, but the astronomical projection is stable to ±1 day. **17 February is Ramadan 2026, not 2027.** The whole US launch schedule moves nine days earlier than the brief assumed. This is the single most consequential finding in this report.

---

## 1. The operating cadence of a top operator

### 1.1 The shape everyone converges on

Serious operators — aggregators, agencies, Amazon itself — run the same three layers: a **daily exception scan** (minutes, alarm-driven), a **weekly business review** (the real decision meeting), and a **monthly/quarterly plan-and-falsify cycle**.

Amazon's own mechanism is canonical: a WBR deck read in silence then walked page by page, built on **controllable input metrics** rather than outputs, upstream of monthly/quarterly reviews and annual OP1/OP2 planning [REPORTED — https://workingbackwards.com/concepts/amazon-operating-cadence/ ; https://commoncog.com/the-amazon-weekly-business-review/]. Steal the input/output distinction: revenue is an output; sessions, CVR, in-stock rate, review velocity and share of voice are the levers.

Agency SOP libraries run the same shape smaller — a PPC SOP with daily budget checks (5–10 min), weekly search-term work (30–45 min), monthly strategy review (1–2 hrs), each with a named owner and quarterly review [REPORTED — https://taskip.net/how-to-create-agency-sops/ ; https://myamazonguy.com/sop/amazon-sop-library/]. Aggregators (Thrasio-style) used standardised relaunch playbooks — PPC, listing, supply chain, expansion — applied uniformly across a portfolio [REPORTED — https://teardowns.sandhill.io/p/thrasio]. Their failure is instructive: the autopsies blame over-standardisation and headcount ("teams of ten doing the work of two") and the assumption that all FBA assets behave alike, not the cadence [REPORTED — https://www.marketplacepulse.com/articles/death-by-valuation-the-amazon-aggregator-autopsy ; https://restructuringnewsletter.com/p/trash-io-the-stumble-from-scale-and-short-term-solutions]. **Copy the cadence, not the headcount. The cadence is the part that automates.**

### 1.2 What is checked when, and what triggers action

- **Daily (07:15 Asia/Jerusalem, after Amazon's 07:00 business-day close):** AHR and new policy violations; stranded/unfulfillable/suppressed listings; Buy Box loss; ad spend vs pace; hero-SKU units on hand; new 1–2★ reviews and returns. *Triggers:* any violation → T3 escalation same day; Buy Box loss >4h → pricing check; hero SKU below cover floor → supply-chain wake; spend >110% of pace → throttle.
- **Weekly (Mon):** Search Query Performance (Amazon weeks run Sun–Sat, so Monday is the first day the prior week is complete [REPORTED — https://kapoq.com/search-query-performance-report-explained/ ; https://perpetua.io/blog-amazon-search-query-performance/]); Business Reports; ad search-term report → negatives and keyword promotion; restock report and cover; VOC/NCX; review velocity; competitor prices. *Triggers:* click- or purchase-share down >20% w/w on a top-20 keyword → investigation; NCX above threshold → CX ticket; cover below floor → PO proposal.
- **Monthly:** full P&L by SKU (contribution margin after ads, TACoS), every fee line, reimbursement recovery, IPI, returns, forecast vs actual. *Triggers:* CM below floor → price/cost action; any fee line >3% of SKU revenue → structural fix.
- **Quarterly:** assortment kill/double-down, supplier lead-time re-measurement, two-quarter promo calendar, playbook falsification against 90 days of outcomes, guardrail re-tune and the T2→T1 ratchet review.

### 1.3 The metric map, and what each one is actually for

- **TACoS** — ad spend ÷ total revenue; the composite health number. Established brands sit ~10–15%; brand-defence campaigns 5–10% ACoS, category-conquest 25–40% if buyers repeat [REPORTED — https://canopymanagement.com/ultimate-guide-to-acos-and-tacos/ ; https://www.velocitysellers.com/2026/04/19/tacos-ceiling-amazon-ad-spend-data/]. Better sources reject benchmark-chasing and derive the target from unit economics: *40% gross margin, 15% needed after ads ⇒ target ACoS 25%* [REPORTED — https://marketplacevalet.com/how-to-set-tacos-targets-by-product-lifecycle-and-contribution-margin/].
- **Contribution margin per unit** — revenue − COGS − fulfilment − referral − other variable − ads. Audited brands land at 12–22% once everything is counted [REPORTED — https://www.brandgrowthiq.com/blog/amazon-profitability-playbook/]. This is what the AGENTS.md 15% floor must be measured against, and it must carry the 2026 fee lines (§7) or it lies.
- **Sessions and unit session % (CVR)** — separates a demand problem from a listing problem. Grocery converts unusually well (~15–21%), carries the lowest ACoS of any major category (~21–24%) and a low CTR (~0.40–0.55%) [REPORTED — https://sellermetrics.app/amazon-conversion-rate/ ; https://autron.ai/blog/amazon-advertising-benchmarks-2026 ; https://keywords.am/blog/amazon-cpc-benchmarks/]. **A grocery CVR under 10% is a listing problem, not a traffic problem.**
- **Search Query Performance (Brand Analytics)** — weekly impressions/clicks/purchases plus *share* metrics for the top 1,000 queries; the best organic-vs-paid diagnostic Amazon gives brands [REPORTED — https://www.amalytix.com/en/knowledge/controlling/amazon-search-query-performance-report/]. **BSR and Buy Box share** — rank and competition. **IPI, restock, capacity** — §7. **VOC/NCX, returns, review velocity, AHR, violations** — §9.

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
| **Finance** | Unit economics, P&L by SKU, cash, fee forensics, reimbursements, targets | Contribution margin/unit after ads, TACoS, fee-line % of revenue, cash days, forecast accuracy (MAPE) | Fri CM refresh; Wed fee anomaly + reimbursement scan; monthly full P&L; monthly target revision | CM after ads <15% → flag; <10% → mandatory price/cost proposal. Fee line >3% of SKU revenue → structural fix. Reimbursement claims filed within **60 days** (was 18 months) and at manufacturing cost, not sale price [REPORTED — https://www.leviathansellers.com/blog/amazon-fba-reimbursement-policy-2026 ; https://www.ecomengine.com/blog/fba-reimbursement-policy] |
| **Supply Chain / Inventory** | Forecast, reorder points, POs, FBA shipments, expiry/FEFO, restock limits, capacity | Days of cover, in-stock rate, IPI, sell-through, aged units, stranded units, expiry runway | Tue forecast + reorder; daily cover check; weekly FEFO aging; monthly capacity/limit review | Reorder when cover ≤ (lead time + safety). Hero cover floor 14 days, seasonal buffer 6 weeks (AGENTS.md). Never below **28 days of supply** (low-inventory-level fee) nor above **22 weeks** account-wide (utilisation surcharge) — see §7 |
| **Advertising** | All SP/SB/SD campaigns, bids, budgets, negatives, placements, dayparting | ACoS, TACoS, CPC, CTR, CVR, share of voice, % sales from ads, new-to-brand | Mon harvest + negatives + promotions; Thu bid/budget check; daily pace check; monthly structure review | T1: bid ±15%, budget +25%/action to cap, one change per target/24h, negatives above statistical threshold. New campaigns T2. Daily cap CAD 150 |
| **Catalog / Listing** | Titles, bullets, A+, images, video, backend keywords, variations, listing health | Sessions, unit session %, SQP click share & purchase share, suppression count | Mon SQP diagnosis; Thu hygiene sweep; monthly A+/image test readout | Any listing text/image change **T2**. CVR drop >25% w/w on a top-10 ASIN → diagnosis within 24h |
| **Pricing & Market Intel** | Price bands, Automate Pricing rules, promos, coupons, deals, competitor watch | Buy Box share, price vs band, promo ROI, elasticity estimate | Tue price/promo review; daily Buy Box + offer-change watch; weekly Keepa competitor pass | All price changes **T2**. Amazon's floor: human authorisation for >20% moves in 24h and bulk edits ≥500 ASINs. Keepa API + SP-API pricing only, never scraped data |
| **Customer** | Reviews, VOC/NCX, returns analysis, buyer messages, Request-a-Review | NCX rate, return rate + reasons, review velocity, star average, response time | Mon VOC/returns review; daily new-negative-review scan | Buyer messages **T2**. Request-a-Review is a strong bounded-T1 candidate once ratcheted (§10) |
| **Account Health & Compliance** | AHR, policy violations, IP complaints, food/label compliance, appeals | AHR score, violation count by severity, suppression count, ODR | Daily exception scan; weekly compliance file review; monthly label/reg audit | AHR <200 "At Risk", <100 suspension risk [REPORTED — https://ensobrands.com/amazon-account-health-rating/]. Any violation → same-day T3 packet. Appeals/POA **T3** |
| **Expansion** | US launch, Walmart, new marketplaces, brand registry, importer setup | Milestone burn-down, launch-readiness %, first-shipment ETA | Wed workstream review | New marketplaces **T3**. Contracts, payment terms **T3** |
| **Creative** | Photography, video, packaging, Ramadan/Eid seasonal assets | Production vs plan, CTR/CVR lift per test | Fortnightly standup | Publishing any asset is **T2** |
| **Chief of Staff / CEO layer** | Cadence, WBR/MBR/QBR, approval queue, ranked daily decision list, ratchet | Decisions/week, approval latency, rejection rate, stale-state count | Mon WBR; Fri approval hygiene; monthly MBR; quarterly QBR + ratchet | Proposal expiry 48h. Ratchet: 30 days + ≥20 approvals + <5% rejection |

---

## 4. Food and grocery specifics

This is where a generic Amazon playbook gets a food brand suspended.

**Expiry and FBA date rules.** **105 days of remaining shelf life at the moment of receipt** is the standard FBA requirement for expiration-dated products; short shipments are rejected, and Amazon disposes of units automatically at **~50 days before expiry** [REPORTED — https://fivestarcommerce.com/guide-on-the-expiration-date-on-amazon-fba/ ; https://help.scanpower.com/en/articles/9854207-amazon-product-expiration-guidelines]. Multi-packs must carry the expiry date **on the outer box and on every unit inside**, with the outer date equal to the **earliest** date inside [REPORTED — https://www.sitruna.com/guides/sitruna-guides-fba-requirements]. *Design consequence:* forecast against effective sellable life (`shelf life − 105 − 50 − transit`), not calendar life, and make FEFO a first-class state file. A 12-month product with 45-day transit has ~165 sellable days — that is the planning horizon.

**Meltables.** No meltable inventory is accepted into FBA between **15 April and 15 October**; the window is 16 Oct – 14 Apr, and stock left after 15 April may be marked unfulfillable and disposed of for a fee from 1 May. "Meltable" means heat-sensitive above ~155°F — chocolate, gummies, jelly- and wax-based products [REPORTED — https://www.sellerassistant.app/blog/amazon-meltable-fba-inventory-all-you-need-to-know/ ; https://riverbendconsulting.com/blog/amazon-meltable-policy/]. *Design consequence:* chocolate, chocolate-coated halva and jelly sweets get an annual ~1 April inbound deadline and a 15 April removal deadline. Ramadan 2027 sits safely inside the window, but lunar drift moves Ramadan ~11 days earlier each year and by the early 2030s it lands inside the blackout. Encode it as a calendar rule now.

**Gating.** Grocery & Gourmet Food requires a Professional account plus category approval, with supplier invoices dated within 180 days showing 10+ units, sometimes GFSI/HACCP and FDA evidence; clean established accounts are sometimes auto-approved. Grocery must list under the **manufacturer's UPC**, sealed and shipping-suitable [REPORTED — https://litcommerce.com/blog/selling-groceries-on-amazon/ ; https://gigacommerce.co/amazon-ungating/].

**Canada — CFIA / SFCR.** Bilingual (EN+FR) labelling is mandatory for common name, net quantity, ingredients, allergens, Nutrition Facts table (Health Canada's prescribed bilingual format), country of origin and the responsible Canadian party [REPORTED — https://www.nexreg.com/canadian-food-labelling-requirements-guide]. **Front-of-package nutrition symbol: transition ended 31 Dec 2025, so from 1 Jan 2026 all labels must comply**, with the symbol required where saturated fat, sugars or sodium reach ≥15% DV [REPORTED — https://www.nsf.org/ca/en/knowledge-library/calling-canadas-food-businesses-ready-labelling-changes]. This is live now and applies to the existing Canadian catalogue — halva, date syrup and tahini plausibly cross the thresholds. Importing also requires an SFC licence [REPORTED — https://jwsmith.com/guides/how-to-import-food-into-canada].

**United States — FDA.** List imported food on Amazon US and FDA treats you as the importer, with the full **FSVP** verification obligation; a foreign brand must appoint a **US-based FSVP agent** [REPORTED — https://qualitysmartsolutions.com/blog/what-amazon-usa-sellers-need-to-know-about-fsvp-compliance ; https://globalimportagent.com/fsvp-amazon-fda-agent-gad01/]. Every shipment needs an FDA **Prior Notice** confirmation number or cargo is held [REPORTED — https://www.fda.itbhdg.com/blog/fulfillment-by-amazon-fba/]. **Amazon will not act as importer of record for FBA inventory** — any shipment, any size, any origin — so the Canadian entity must register as US IOR (CBP Form 5106), post a customs bond, and carry full liability for classification and entry [REPORTED — https://carraglobe.com/importer-of-record-amazon-fba/]. **Hazmat: UNKNOWN** — could not confirm which SKUs would be flagged; Amazon runs a dangerous-goods review on new ASINs, so check per SKU at listing time.

**Bundles.** Since **14 October 2024**, consumables bundles may only be listed if created by the original manufacturer, who must own the brand of every item; mixed-manufacturer, "Generic" and reseller bundles are barred in grocery, pet, baby and health & beauty [REPORTED — https://myfbaprep.com/blog/amazon/navigating-amazons-new-consumables-bundling-policy/]. Anabtawi owns its brand, so **multi-packs and gift sets remain available** — the cleanest lever for raising AOV into Ramadan without touching unit price. Virtual Bundles are the lower-risk option for cross-SKU sets.

**Subscribe & Save.** Seller-funded tier (commonly 5% or 10%); Amazon funds an extra 5% when a delivery contains 5+ subscribed items; no participation fee beyond standard FBA. Grocery, beauty and pet are ~70% of S&S volume [REPORTED — https://www.themarketplaceguys.com/en/blog/amazon-subscribe-and-save]. But reported average subscriber lifetime in CPG is only **2.4–3.8 deliveries** [REPORTED — https://www.velocitysellers.com/2026/07/05/amazon-subscribe-save-data-deep-dive-2026/], so at 10% over 3 deliveries you pay ~30% of one order's revenue to acquire ~2 extra orders. Usually good for a pantry staple, usually bad for a gift item.

---

## 5. The Amazon US launch from a Canadian base

### 5.1 NARF / Remote Fulfillment — the wrong tool here

Remote Fulfillment with FBA (formerly NARF) fulfils **amazon.ca and amazon.com.mx** orders from **US** inventory, at fees higher than domestic FBA [REPORTED — https://www.ecomcrew.com/what-is-amazons-narf-beta-program/ ; https://www.frisbi.com/blog/the-ultimate-guide-to-amazons-north-american-remote-fulfillment-narf-program]. It serves Canada from a US base, not the reverse. For a Ramadan launch with a seasonal spike and Prime-speed expectations, **separate US FBA inventory is the only serious option**. NARF matters later: once US volume dwarfs Canadian, running Canada off US stock could retire an inbound lane — a 2028 conversation, and one that collides with CFIA bilingual labelling.

### 5.2 Launch mechanics worth encoding

- **Brand Registry:** a Canadian (CIPO) mark does not confer US Brand Registry rights; a USPTO mark is generally needed for the US store [REPORTED — https://gobrandwoven.com/resources/articles/amazon-brand-registry-trademark-application-benefits-and-barriers/]. **If a USPTO application is not filed, this is the long pole** — examination runs months. UNKNOWN: current pendency.
- **Pricing parity / FX:** no contractual parity clause remains in the US BSA (removed 2019), but the **Marketplace Fair Pricing Policy** is enforced independently — Amazon can suppress the Featured Offer, remove the offer or suspend selling privileges over a price significantly higher than elsewhere, on or off Amazon [REPORTED — https://www.pattern.com/blog/amazons-price-parity-s-4-seller-term-has-changed ; https://www.kaspien.com/blog/amazon-fair-pricing-policy-which-marketplaces-does-amazon-price-match/]. US and CA prices must be defensible against each other after FX, and a Walmart Canada price below the Amazon price can suppress the Buy Box. Price the US catalogue in USD from US unit economics, never by converting CAD.
- **Sales tax:** Amazon collects and remits as marketplace facilitator in essentially all states; FBA placement still creates physical presence in states you did not choose, and non-marketplace sales remain your own filing obligation [REPORTED — https://salaccounting.ca/blog/us-sales-tax-requirements-for-canadian-sellers/].
- **Vine:** needs Brand Registry, FBA, image and description, and fewer than 30 reviews; up to 30 units per parent. Reported 2026 change: **$0 enrolment for products under $100** from March 2026 ($200 per parent for $100–$499); no charge until the first Vine review publishes, none at all if none arrives in 90 days [REPORTED — https://sellercards.com/blog/amazon-vine-program-eligibility-2026 ; https://www.bellavix.com/amazon-vine-program-costs-in-2026-what-sellers-and-vendors-need-to-know/]. For a sub-$100 food catalogue Vine is effectively free — **enrol every US ASIN at launch**.
- **FBA New Selection Program (2026 version, live 30 July 2026):** instant referral-fee credits (capped to 10% on the first 100 units, 5% on the next 100), 120 days free storage, free returns and liquidations on the first 200 units, no low-inventory-level fee or utilisation surcharge on those units, plus $50 coupon and $75 Vine credits, with a reported **31 October enrolment deadline** [REPORTED — https://novadata.io/resources/news/amazon-fba-new-selection-program-expansion-july-30-2026 ; https://damlawfirm.com/blog/amazon-fba-new-selection-program-2026/]. **UNKNOWN whether that deadline is a 2026 one-off or annual, and whether it is per-marketplace.** If US ASINs must exist to enrol by 31 Oct 2026, US listing creation pulls forward ~10 weeks. **Confirm this first.**
- **Reviews, compliant:** Request-a-Review on every eligible order is the sanctioned mechanism, and using it means not also sending review requests via Buyer-Seller Messaging. Neutral, non-incentivised inserts are tolerated; asking for a *positive* review, offering reward, or filtering by sentiment is review manipulation [REPORTED — https://salesduo.com/blog/how-to-get-reviews-on-amazon/ ; https://www.sellersprite.com/en/blog/amazon-review-manipulation-suspension].
- **Launch PPC:** auto + manual-exact per hero ASIN from day one, ~$30–50/day each on ~5 priority keywords, launch ACoS **40–60% above the mature target**, tightened as reviews and rank build; keep ≥15–30 clicks/day on the hero campaign or data accrues too slowly [REPORTED — https://www.velocitysellers.com/2026/06/29/amazon-product-launch-strategy-2026-first-90-days/]. The "honeymoon" (~2–4 weeks of elevated visibility) is folklore with a grain of truth — do not bet the plan on it.

### 5.3 Ramadan 2027 US launch — backward schedule

Anchors: **Ramadan ~8 Feb 2027; Eid al-Fitr ~9–10 Mar 2027** [REPORTED, §0]. Pre-Ramadan shopping builds **2–3 weeks ahead** [REPORTED — https://www.golocad.com/blog/increase-sales-during-ramadan-in-the-middle-east/], so demand turns up **mid-to-late January 2027**. Sea freight to the US East Coast plus customs plus FBA receiving realistically consumes **6–10 weeks** door-to-sellable [REPORTED — https://ship4wd.com/logistics-shipping/how-long-does-freight-shipping-take ; FBA receive adds 3–14 days per https://www.inventoryhero.ai/guides/amazon-fba-reorder-point]. "Stock in US FBA by mid-January" is right, and with a Feb 8 start it is **tight, not comfortable**.

| When | Milestone | Owner | Why this date |
|---|---|---|---|
| **Sep–Oct 2026 (now)** | Confirm FBA New Selection 2026 enrolment deadline and whether US ASINs must exist to qualify | Expansion | Reported 31 Oct deadline could force everything forward (§5.2) |
| **Sep 2026** | USPTO trademark status check; file if not filed | Expansion / Rami (T3) | Gates Vine, A+, SQP, brand protection |
| **Oct 2026** | US entity/tax decisions, CBP Form 5106 IOR registration, customs bond, US FSVP agent appointed, FDA facility registration confirmed | Expansion / Rami (T3) | Amazon will not be IOR; no bond, no entry (§4) |
| **Oct 2026** | US grocery category approval application (invoices, GFSI/HACCP if requested) | Compliance | Gated category; latency unknown |
| **Oct–Nov 2026** | US label artwork finalised: FDA nutrition panel, allergens, US English; production run scheduled | Creative + Compliance | Canadian bilingual labels are not US-compliant |
| **Nov 2026** | PO issued to supplier for US launch quantity (Ramadan quantity + 6-week seasonal buffer per AGENTS.md) | Supply Chain → Rami (T2/T3) | Production and booking precede sailing |
| **Nov–Dec 2026** | US listings created (draft), images, A+ content, backend keywords; keyword research off Canadian SQP + US competitor set | Catalog | Must be live before Vine and before arrival |
| **~1 Dec 2026** | Cargo sails | Supply Chain | 6–10 weeks door-to-sellable ⇒ latest safe sailing |
| **Dec 2026** | Prior Notice filed per shipment; FSVP records assembled | Compliance | Missing Prior Notice = FDA hold |
| **Early Jan 2027** | Port arrival, customs clearance, transload, FBA inbound plan created; inbound placement option chosen | Supply Chain | Placement-fee vs split-shipment trade-off |
| **~15 Jan 2027** | **Stock checked in and sellable in US FBA** | Supply Chain | Hard gate; everything downstream depends on it |
| **~15 Jan 2027** | Vine enrolled on every eligible US ASIN (30 units/parent) | Catalog | Vine reviews take weeks — enrol the day stock is live |
| **~18 Jan 2027** | PPC live: auto + manual-exact per hero ASIN, launch ACoS 40–60% above mature target | Advertising | ~3 weeks of learning before demand turns up |
| **~25 Jan 2027** | Demand-curve inflection: shift budget from discovery to defence; Ramadan/Eid creative live; S&S enabled on pantry staples | Advertising + Creative | 2–3 weeks pre-Ramadan build-up |
| **~1 Feb 2027** | Restock decision point #1: is a second air/expedited shipment needed? | Supply Chain → Rami | Air freight is the only lever left after this date |
| **8 Feb 2027** | **Ramadan begins** | — | Peak sell-through, days 1–15 |
| **~20 Feb 2027** | Eid gifting push: multi-packs/gift sets, coupons, Eid creative | Pricing + Creative | Eid demand is gift-shaped, not pantry-shaped |
| **9–10 Mar 2027** | **Eid al-Fitr** | — | Demand cliff immediately after |
| **Mar–Apr 2027** | Post-season: sell-down plan, removal/liquidation of surplus, **meltable removal before 15 Apr**, retrospective into playbooks | Supply Chain + CoS | Aged-inventory and meltable deadlines (§4) |

---

## 6. Advertising for a 10–15 winner catalogue

### 6.1 Architecture

The consensus structure for a small catalogue is deliberately boring, which is why it automates well: **SP Auto** per hero ASIN as the discovery engine (run 7–14 days before harvesting); **SP Manual Broad/Phrase** for mid-funnel expansion; **SP Manual Exact** for proven converters, bid aggressively; **SP Product Targeting** for conquest and own-catalogue defence; **Sponsored Brands** for category headline terms and Ramadan/Eid creative into a Brand Store; **Sponsored Display** for remarketing and defending hero detail pages [REPORTED — https://ecombrainly.com/amazon-ppc-campaign-structure/ ; https://adlabs.app/guides/amazon-campaign-structure-guide/].

**The negative-keyword bridge is the load-bearing rule.** When an auto-campaign search term produces **3+ sales**, promote it to Manual Exact *and simultaneously add it as negative exact in the auto campaign* — otherwise the two campaigns bid against each other and inflate your own CPC [REPORTED — https://sellermetrics.app/negative-keywords-amazon-ppc/ ; https://www.off-hours.app/blog/amazon-ppc-campaign-structure]. Mechanical, compounding, and the thing humans forget weekly: the best T1 candidate after bid hygiene.

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

**Dayparting:** only worth it once hourly data is significant. The obvious Ramadan play is shifting budget to late-evening, post-iftar hours — but I found **no data** confirming that pattern on Amazon US/CA. **UNKNOWN**; test it with a two-week A/B in Feb 2027, do not ship it as a rule. **Budget pacing:** hold TACoS as a *range*, not a ceiling — 10–15% composite established, higher through launch and Ramadan build-up, lower in the post-Eid trough [REPORTED — https://pare.so/blog/amazon-tacos-range-not-ceiling-ppc-hire-signal-2026].

### 6.3 The Amazon Ads MCP server

Amazon opened **open-beta access to an official Amazon Ads MCP Server on 2 February 2026**: agent-driven campaign creation, bid management, reporting, account settings and billing across SP/SB/SD/DSP/AMC, explicitly compatible with Claude, ChatGPT, Gemini and custom agents, for anyone with Ads API credentials [REPORTED — https://www.sellerlabs.com/blog/amazon-ads-mcp-server-what-sellers-need-to-know/ ; https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta]. This is the sanctioned, policy-clean surface for the Advertising department's T1 authority and matches AGENTS.md §3 exactly. **It requires Ads API credentials** — a separate registration from SP-API.

---

## 7. Inventory planning

### 7.1 Formulas

- **Reorder point = (average daily sales × lead time in days) + safety stock** [REPORTED — https://www.spscommerce.com/community/articles/amazon-reorder-point ; https://sellerlegend.com/glossary/reorder-point].
- **Safety stock = (max daily sales × max lead time) − (avg daily sales × avg lead time)** — sizes the buffer to the worst realistic case and captures both demand spikes and freight delay [REPORTED — https://www.inventoryhero.ai/guides/safety-stock-amazon-fba].
- **Lead time must include FBA check-in**, which adds **3–14 days** most sellers omit [REPORTED — https://www.inventoryhero.ai/guides/amazon-fba-reorder-point]. For food imports add customs and, for the US, FDA prior-notice/hold risk.
- **Forecasting:** a weighted moving average with a seasonality index is adequate and auditable at 50 SKUs with known seasonality. I found **no evidence** that tool-based ML beats a well-specified seasonal WMA at this scale — **UNKNOWN**. WMA's real advantage here is that the agent can show its work: `forecast = WMA(last 8 weeks) × seasonality_index × trend_factor`, every input citable. Because the Islamic calendar drifts ~11 days a year, **the Ramadan index must be keyed to the lunar date, not the Gregorian month**, or the model systematically mis-times the biggest season.

### 7.2 The 2026 fee cliffs the forecast must respect

| Constraint | Threshold | Reported effect |
|---|---|---|
| **Low-inventory-level fee** | 30-day *and* 90-day days-of-supply both below **28 days** | $0.32–$2.09/unit; from 2026 assessed at **FNSKU** level, not parent ASIN [REPORTED — https://novadata.io/resources/news/amazon-low-inventory-level-fee-2026] |
| **Storage utilisation surcharge** | Account cover above **22 weeks** (13-wk avg inventory volume ÷ 13-wk avg shipped ÷ 7) | $0.44/cu ft at 22–28 weeks rising to $1.88 above 52. Exempt: <365 days since first FBA shipment, Individual accounts, <25 cu ft average [REPORTED — https://mysellerhub.com/blog/amazon-fba-storage-fees-explained-base-utilization-and-aged-inventory-surcharges/] |
| **Aged inventory surcharge** | US from **181 days**; Canada reported to start at **271 days** | US ~$1.50/cu ft at 271 days, $6.90/cu ft (or $0.15/unit) past 365, **on top of** base storage [REPORTED — https://www.conversionperk.com/amazon-fba-storage-fees-2026/ ; https://ecomcalctools.com/blog/fees-amazon/amazon-fees-canada-2026/] |
| **Base monthly storage** | US $0.78/cu ft Jan–Sep, **$2.40 Oct–Dec**; Canada ~CAD 1.02 Jan–Sep + 3.5% fuel surcharge | Q4 roughly triples US storage cost [REPORTED — same] |
| **Inbound placement fee** | Updated 15 Jan 2026 | Standard-size minimal-split up ~$0.05/unit average; new weight bands. Verify per ASIN in the Revenue Calculator [REPORTED — https://amzprep.com/amazon-inbound-placement-fees/] |
| **Prep & labelling services** | Discontinued **US 1 Jan 2026**, **Canada 1 Jul 2026** | Inventory must arrive shelf-ready; a prep partner is now mandatory [REPORTED — https://www.sellerapp.com/blog/amazon-fba-fees-calculator-guide/ ; https://ecomcalctools.com/blog/fees-amazon/amazon-fees-canada-2026/] |
| **IPI / capacity** | Threshold reported at **400**; 500+ gets better allocation | Mid-2025 tightening reportedly cut allowance from six to five months of forecast sales and reactivated ASIN-level restock limits [REPORTED — https://www.sellerlabs.com/blog/amazon-ipi-score-2026/ ; https://novadata.io/resources/blog/amazon-fba-restock-limits] |

**The corridor this creates is the core inventory problem:** above 28 days of cover per FNSKU, below 22 weeks account-wide, out of the 181-day aged band, above 105 days remaining shelf life at receipt — simultaneously, for a brand whose demand triples for four weeks a year. **No operator holds that by intuition. It is the strongest argument in this report for automating supply chain first.**

---

## 8. Pricing, promotions, and competitor intelligence

- **Automate Pricing** is free in Seller Central: predefined rules ("beat the Buy Box price", "stay below lowest price") plus custom rules, mandatory **minimum** and optional **maximum** boundaries, per-SKU or bulk, executing continuously, able to reference external prices; also manageable via SP-API [REPORTED — https://wiseppc.com/blog/automate-pricing-rules/ ; https://developer-docs.amazon/sp-api/docs/manage-automated-pricing-rules]. **This is the right home for the per-SKU band in `products/<sku>.md`:** mirror min/max into Amazon's own tool, let Amazon execute inside the band, make any band *change* a T2 proposal. Continuous Buy Box protection with no agent touching price.
- **Competitor monitoring without scraping:** SP-API `ANY_OFFER_CHANGED` (price changes among the top 20 offers or the Featured Offer) and `PRICING_HEALTH` (your offer becomes Featured-Offer-ineligible through external competition or an atypically high price) [REPORTED — https://developer-docs.amazon/sp-api/docs/pricing-faq]. Keepa supplies historical price/BSR via a token-metered API from ~€49/month, with a hosted MCP server on the same key [REPORTED — https://revenuegeeks.com/software/keepa/api ; https://keepa.com/api-docs/]. Together these satisfy AGENTS.md §6.2 with no scraped page. **Cost caveat:** a **$1,400 annual third-party developer subscription from 31 Jan 2026** is reported [REPORTED — https://blog.ppcassist.com/2025/12/14/amazon-sp-api-pricing-2026-optimization-guide/]; **UNKNOWN** whether it hits a seller's own private registration or only app publishers.
- **Promotion fee math (US, reported):** coupons **$5 flat per coupon + 2.5% of coupon sales** (from 2 June 2025, replacing $0.60/redemption); Lightning Deals **$70/day + 1% of deal sales, variable capped at $2,000**; peak events revert to fixed premium fees (~$500 Lightning, ~$1,000 Best Deal). Prime Exclusive Discounts are cheaper and need less depth [REPORTED — https://nivoads.com/blog/amazon-coupon-deals-fees-2025/ ; https://www.adverio.io/coupons-vs-best-deals-vs-lightning-deals-amazon/].
  **The ROI test an agent can run:** approve only if `incremental units × CM/unit > (discount × total promo units) + fixed fee + variable fee`, with "incremental" estimated from a matched pre-period and the rank/review halo stated as an explicitly separate, unquantified argument. Never let the halo carry the decision silently.
- **Promotion calendar:** Prime Day (2026 ran four days in late June [REPORTED — https://www.consumerreports.org/money/sales-promotions/best-amazon-prime-day-lightning-deals-a5109927191/]), an autumn Prime event, BFCM, Christmas — and for Anabtawi the two that matter, **Ramadan (8 Feb – 9 Mar 2027)** and **Eid al-Fitr (~9–10 Mar 2027)**. Ramadan e-commerce in Muslim-majority markets reportedly surges 30–50% over baseline, Amazon Saudi +38% orders in Ramadan 2026 [REPORTED — https://themiddleeastinsider.com/2026/03/14/saudi-ramadan-economy-2026-spending-retail-trends/]. **Those are MENA figures; the magnitude does not transfer to a North American diaspora market, only the shape.** Anabtawi's own Canadian 2026 Ramadan curve is the only reliable index for the US 2027 forecast — building it from DataDoe history is a Supply Chain task this month.
- **MAP:** Brand Registry does **not** enforce MAP for you and does not override Fair Pricing enforcement [REPORTED — https://www.enceiba.com/post/demystifying-amazon-brand-registry-what-it-does-and-what-it-doesn-t-do]. MAP is a contract matter (T3), not an Amazon feature.

---

## 9. Compliance and account health

**Account Health Rating** is a 0–1,000 near-real-time score rolling up policy compliance, order performance and shipping metrics: ≥200 healthy, 100–199 at risk, <100 suspension risk. Violations carry severity (critical/high/medium/low) and deduct points [REPORTED — https://ensobrands.com/amazon-account-health-rating/ ; https://www.sellerlabs.com/knowledge-base/how-amazon-account-health-rating-ahr-works-the-complete-seller-s-guide/].

**What actually causes suspensions in food:** expired-product complaints, product-safety complaints, and authenticity/IP complaints. A single serious safety complaint can trigger investigation or listing removal; multiple can suspend the account [REPORTED — https://amazonsellersappeal.com/expired-products-complaints/ ; https://theappealguru.com/amazon-suspension-for-food-and-product-safety-issues-what-are-they/]. For a 105-day-shelf-life-gated, FEFO-dependent food catalogue, **expiry is the top existential risk and it is also the most automatable to prevent.**

**Plan of Action SOP:** (1) specific root cause; (2) immediate corrective action — remove/dispose affected stock, change supplier; (3) **systemic** prevention — FEFO enforcement, automated expiry checks, revised SOPs, inspection cadence; (4) documentary evidence [REPORTED — https://amazonsellersappeal.com/expired-products-complaints/ ; https://www.amazonsellers.attorney/safety-complaint-suspensions.html]. Note the irony worth exploiting: "we automated expiry checks and enforce FEFO through a documented system with an immutable action log" is *exactly* what a POA needs to say — and `ledger/actions.jsonl` produces that evidence as a by-product.

**Monitoring:** VOC/NCX weekly, AHR and violations daily, plus SP-API `LISTINGS_ITEM_ISSUES_CHANGE` for suppression events (**note: v1.0 closes to new subscriptions 14 Aug 2026 and stops delivering 26 Aug 2026 — use the current version**) [REPORTED — https://developer-docs.amazon.com/sp-api/changelog].

**Appeals, POAs, and IP complaint responses stay T3.** They are legal writing under time pressure with account-ending downside; an agent should assemble the evidence packet and draft, and Rami should send.

---

## 10. What the AI departments should own end-to-end vs. propose

For a solo operator who wants zero babysitting: **automate what is reversible, high-frequency and rule-shaped; propose what is irreversible, low-frequency or judgement-shaped.** The failure mode to avoid is not "the agent did something wrong" — it is "the agent produced 40 proposals a week and the operator became a rubber stamp." A rubber-stamped T2 is worse than a well-guardrailed T1: it launders automation through a human who is not actually reading.

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

**Three highest-value automations, in order:** (1) the inventory fee-and-expiry corridor (§7) — four simultaneous constraints, weekly recomputation, real money, no judgement required; (2) the PPC negative-keyword bridge (§6.1) — mechanical and compounding; (3) the daily exception scan (§1.2) — not hard, but exactly what a human stops doing in week three.

---

## Implications for the design

1. **Fix the Ramadan date in every plan today.** Ramadan 2027 starts ~8 February, not 17. Nine days out of a schedule whose critical path is ocean freight is the difference between a launch and a miss. Put lunar dates through 2032 in `state/calendar.md` and key the seasonality index to them, not to Gregorian months.
2. **Confirm the FBA New Selection 2026 deadline before anything else.** If the reported 31 October enrolment requires live US ASINs, the US timeline compresses ~10 weeks — and the programme waives exactly the costs a launch incurs (referral credits, 120 days free storage, low-inventory and utilisation fees, $75 Vine credit).
3. **Promote Supply Chain toward T1 before Advertising.** The constitution gives Advertising the only T1 class, but §7's fee corridor is where money silently leaks and the rules are cleanest. Give Supply Chain T1 monitoring-and-escalation now; ratchet reorder-point recalculation next.
4. **Put price bands in Amazon's Automate Pricing, not an agent loop.** The band lives in `products/<sku>.md`, mirrored into Amazon's min/max; Amazon executes; the agent only *audits the band*. Satisfies "money never moves on T1" while keeping continuous Buy Box protection, and is provably policy-clean.
5. **The Ads MCP server is the sanctioned T1 surface — check the credential path in week one.** Official, Claude-compatible, covering exactly the bid/budget/negative operations AGENTS.md permits. Confirm whether DataDoe's Ads access satisfies it or whether Rami needs his own Ads API registration.
6. **Without the 2026 fee lines, the 15% contribution-margin floor is fiction.** Low-inventory-level fee, utilisation and aged-inventory surcharges, inbound placement, the 3.5% Canadian fuel surcharge and the end of Amazon prep (US Jan 2026, CA Jul 2026) all sit between gross and contribution margin. Each needs a named line in Finance's SKU model.
7. **Reimbursements became a 60-day, cost-basis game.** Fill the per-unit cost field for every SKU (Amazon substitutes a lower internal estimate when it is blank), and make reimbursement detection a weekly Finance job with a hard 60-day SLA.
8. **Design the approval queue for scarcity.** Batch T2 proposals into the Monday WBR and Friday hygiene pass; aim for under ten decisions a week reaching Rami. Any class producing more than five proposals a week is either a ratchet candidate or a badly-drawn boundary.
9. **The compliance ledger is a launch asset, not overhead.** `ledger/actions.jsonl` plus the FEFO state file *is* the documentary evidence a food POA requires. Put that in the Compliance charter so the department writes for that audience from day one.
10. **Copy the aggregator cadence, refuse the aggregator uniformity.** Thrasio's playbooks worked; its assumption that all FBA assets behave alike did not. `products/<sku>.md` — own band, cover floor, shelf life, meltable flag, seasonality index — is the structural answer: shared cadence, never shared parameters.

---

## Open questions

1. **FBA New Selection Program 2026 — is the 31 October deadline a 2026 one-off or annual, is it per-marketplace, and must US ASINs be live to enrol?** Highest-priority unknown. [Tried: search only; could not open Seller Central.]
2. **SP-API's reported $1,400/year developer fee from 31 Jan 2026 — does it apply to a seller's own private developer registration?** Determines whether registering for SP-API is a $0 or $1,400/year decision, and therefore how much weight DataDoe carries. [Tried: search; developer-docs.amazon fetch blocked.]
3. **Does DataDoe's Ads access satisfy the Amazon Ads MCP Server's credential requirement, or is a separate Ads API registration needed?** Gates the Advertising department's entire T1 authority. [Tried: search; vendor docs not fetchable.]
4. **Which Anabtawi SKUs are meltable, and which are hazmat?** Needs a per-SKU classification pass against Amazon's own dangerous-goods and meltable definitions. Meltable SKUs acquire a hard 1 April inbound deadline and a 15 April removal deadline every year. [Not researchable without the SKU list.]
5. **Canada FOP labelling — which Anabtawi SKUs cross the 15% DV thresholds for saturated fat, sugars or sodium?** The rule has been in force since 1 January 2026, so any non-compliant label is already non-compliant. Halva, tahini, date products and sweets are the likely candidates. [Tried: inspection.canada.ca blocked; needs nutritional data per SKU.]
6. **Is the 105-day rule measured at receipt or at shipment creation, and is the disposal trigger really 50 days?** The whole FEFO model keys off these two numbers. [Tried: Seller Central blocked.]
7. **What is Anabtawi's own Ramadan 2026 Canadian lift by SKU?** The only trustworthy basis for the US 2027 forecast; MENA's +30–50% does not transfer. [Available internally via DataDoe.]
8. **What is the real door-to-sellable lead time on Anabtawi's supplier lane?** I used a generic 6–10 weeks; §5.3 is only as good as this number. Measure it from the last three Canadian shipments.
9. **USPTO trademark status for the Anabtawi mark.** Gates US Brand Registry, which gates Vine, A+, SQP and brand protection. If unfiled, it may be the true critical path, ahead of freight.
10. **Do published default bid-rule thresholds exist for Pacvue/Perpetua?** I found feature descriptions only, so §6.2 is a design proposal to be tuned against Anabtawi's own 60-day outcome data, not inherited wisdom. **Also UNKNOWN: whether Canadian restock limits and IPI mechanics differ from the US.**
