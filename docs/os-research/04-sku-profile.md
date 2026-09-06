# 04 — The SKU Profile

*Research date: 2026-09-06. Author: research agent. Client: Rami Anabtawi / Anabtawi Company.*

Every factual claim below is tagged **VERIFIED** (primary source opened today, URL given), **REPORTED** (secondary source or vendor marketing, URL given), or **UNKNOWN** (could not confirm; what I tried is stated).

---

## 0. What this document decides

One living record per product that nine AI departments read and write, that survives a runtime change, and that Rami can open on his phone in the checkout line and know whether to act. The question is not "what fields exist" — the tools below answer that generously. The question is **which fields belong in a record at all, who owns each one, and where the record physically lives** so that it is never simultaneously stale, unauditable, and unreadable on a phone.

Headline recommendation: **a hybrid.** `products/<brand>/<sku>.md` in this git repo is the system of record for everything a human or an agent *decides*; a narrow monday board (one item per SKU × marketplace, ~34 columns) is the system of engagement for Rami and the write target for live numbers; a nightly build on the Mac mini composes one from the other. Detail and dissent in §4.

---

## 1. How the best tools model a product

I could not open several vendor sites directly — `developer-docs.amazon.com`, `keepa.com`, `sellerboard.com`, `helium10.com`, `datadive.tools`, `sostocked.com`, `perpetua.io`, `docs.akeneo.com`, `monday.com` and `developer.monday.com` are all blocked by this environment's egress proxy (tried `WebFetch` and `curl` on each; all returned `EGRESS_BLOCKED` or connection code 000). Where the blocked source had an official mirror I used it: Amazon's own OpenAPI models on `raw.githubusercontent.com/amzn/selling-partner-api-models`, and the live monday.com GraphQL API via its MCP server. Vendor claims are otherwise tagged REPORTED.

### 1.1 Amazon's own object model — the floor everyone else builds on

**Catalog Items v2022-04-01** — the `Item` object has exactly eleven top-level members: `asin`, `attributes`, `classifications`, `dimensions`, `identifiers`, `images`, `productTypes`, `relationships`, `salesRanks`, `summaries`, `vendorDetails`. `ItemSummaryByMarketplace` carries `marketplaceId, adultProduct, autographed, brand, browseClassification, color, contributors, itemClassification, itemName, manufacturer, memorabilia, modelNumber, packageQuantity, partNumber, releaseDate, size, style, tradeInEligible, websiteDisplayGroup, websiteDisplayGroupName`. `ItemDimensionsByMarketplace` splits `item` from `package`, each a `Dimensions` of `height, length, weight, width`. `ItemRelationship` gives `childAsins, parentAsins, variationTheme, type`. `ItemClassificationSalesRank` gives `classificationId, title, link, rank`. **VERIFIED** — https://raw.githubusercontent.com/amzn/selling-partner-api-models/main/models/catalog-items-api-model/catalogItems_2022-04-01.json

The structural lesson: **Amazon scopes nearly everything by marketplace.** Summaries, dimensions, identifiers, images, product types, relationships and sales ranks are all `...ByMarketplace` arrays. That is not an accident and it decides §6.

**Listings Items v2021-08-01** — `Item` has `sku, summaries, attributes, issues, offers, fulfillmentAvailability, procurement, relationships, productTypes`. `ItemSummaryByMarketplace` adds `asin, productType, conditionType, status, fnSku, itemName, createdDate, lastUpdatedDate, mainImage`. `status` is an array over the enum `BUYABLE`, `DISCOVERABLE` — those two booleans are the entire truth about whether a listing is live. `Issue` carries `code, message, severity` (`ERROR|WARNING|INFO`), `attributeNames`, `categories` (`INVALID_ATTRIBUTE`, `MISSING_ATTRIBUTE`, …), `enforcements` with actions including `LISTING_SUPPRESSED` and `ATTRIBUTE_SUPPRESSED`, and `marketplaceIds`. `FulfillmentAvailability` is `fulfillmentChannelCode` + `quantity`. `ItemProcurement` is `costPrice`. **VERIFIED** — https://raw.githubusercontent.com/amzn/selling-partner-api-models/main/models/listings-items-api-model/listingsItems_2021-08-01.json

This is where the profile's `listing_status` and `suppression` fields should come from — not from a scrape, not from a screenshot, and not from a human's memory.

**FBA Inventory v1** — `InventorySummary` is `asin, fnSku, sellerSku, condition, inventoryDetails, lastUpdatedTime, productName, totalQuantity, stores`. `InventoryDetails` is `fulfillableQuantity, inboundWorkingQuantity, inboundShippedQuantity, inboundReceivingQuantity, reservedQuantity, researchingQuantity, unfulfillableQuantity`. `ReservedQuantity` decomposes into `totalReservedQuantity, pendingCustomerOrderQuantity, pendingTransshipmentQuantity, fcProcessingQuantity`. `UnfulfillableQuantity` decomposes into `totalUnfulfillableQuantity, customerDamagedQuantity, warehouseDamagedQuantity, distributorDamagedQuantity, carrierDamagedQuantity, defectiveQuantity, expiredQuantity`. **VERIFIED** — https://raw.githubusercontent.com/amzn/selling-partner-api-models/main/models/fba-inventory-api-model/fbaInventory.json

Note `expiredQuantity` and `lastUpdatedTime`. Amazon hands you both the expiry write-off and the freshness stamp. Use both.

**Product Pricing v0** — `Summary` gives `TotalOfferCount, NumberOfOffers, LowestPrices, BuyBoxPrices, ListPrice, CompetitivePriceThreshold, SuggestedLowerPricePlusShipping, SalesRankings, BuyBoxEligibleOffers`. `BuyBoxPriceType` and `LowestPriceType` each give `condition, fulfillmentChannel, LandedPrice, ListingPrice, Shipping, Points, sellerId`. `OfferDetail` gives `MyOffer, SellerId, SellerFeedbackRating, ShippingTime, ListingPrice, Shipping, ShipsFrom, IsFulfilledByAmazon, PrimeInformation, IsBuyBoxWinner, IsFeaturedMerchant`. **VERIFIED** — https://raw.githubusercontent.com/amzn/selling-partner-api-models/main/models/product-pricing-api-model/productPricingV0.json

This is the *legal* competitor-price source under the constitution's Hard Rule 2. Everything a competitor panel needs — buy-box landed price, offer count, whether we hold the box — is here, plus Keepa for history.

**Sales & Traffic report** — `SalesAndTrafficByAsin` is `parentAsin, childAsin, sku, salesByAsin, trafficByAsin`. `SalesByAsin`: `unitsOrdered, unitsOrderedB2B, orderedProductSales, orderedProductSalesB2B, totalOrderItems, totalOrderItemsB2B`. `TrafficByAsin`: `sessions, pageViews, buyBoxPercentage, unitSessionPercentage` and their browser/mobile/B2B variants. **VERIFIED** — https://raw.githubusercontent.com/amzn/selling-partner-api-models/main/schemas/reports/sellerSalesAndTrafficReport.json

`unitSessionPercentage` (conversion) and `buyBoxPercentage` are the two traffic numbers worth a column. The rest is analysis, not profile.

**Brand Analytics — Search Query Performance** exposes, per query: search query volume, search query score, and impressions / clicks / cart adds / purchases with total count, ASIN count and ASIN share; an ASIN view breaks it to individual products. It covers organic + Sponsored Products on search pages only, not Sponsored Brands/Display or detail-page placements. **REPORTED** — https://www.amalytix.com/en/knowledge/controlling/amazon-search-query-performance-report/ , https://kapoq.com/search-query-performance-report-explained/

That share-of-clicks number per top keyword is the only defensible "keyword rank" field. Everything else in the rank-tracking world is inference.

**Food-specific constraints that must be columns, not lore:** food and beverage products must be lot-controlled with more than 90 days remaining shelf life, and units within 50 days of expiry on arrival are marked for disposal; meltables are accepted by FBA only between 1 October and 30 April, and meltable inventory in an FC after 1 May is marked unfulfillable and disposed of; dangerous-goods items require an SDS uploaded via Amazon's tool. **REPORTED** — https://www.ecomengine.com/blog/amazon-expiration-dates , https://riverbendconsulting.com/blog/amazon-meltable-policy/ , https://sellercentral.amazon.com/gp/help/external/G201003420

For a Middle Eastern food brand — tahini, halva, date paste, chocolate-coated anything — `meltable` and `oldest_expiry_date` are not nice-to-haves. They are the two fields most likely to destroy a Ramadan 2027 US launch if they are wrong, because the US FBA stock must land by mid-January and the meltable window closes 30 April.

### 1.2 What the seller tools add on top

| Tool | What it models per product | Refresh | What to steal |
|---|---|---|---|
| **Sellerboard** | Per-product, per-day: Units Sold, Refunds, Sales, Promo, Ads, Amazon Fees, CoGS, Gross Profit, Net Profit, Estimated Payout, Margin, ROI, BSR, Real ACoS, Sessions. COGS settable by period, by batch, or FIFO. **REPORTED** — https://blog.sellerboard.com/2025/06/28/mastering-sellerboards-profitability-dashboard-tiles-charts-pl-map-and-trends/ , https://sellerboard.com/en/faq | Daily (UNKNOWN exact cadence — FAQ blocked) | **COGS is time-versioned, not a scalar.** A single `cogs` number is a lie the moment a second PO lands at a different price. |
| **Helium 10 Profits / Inventory** | SKU-level revenue, fees, ads, COGS, refunds; inventory view carries COGS + COGS status, estimated Amazon fees, fulfilment type (FBA/FBM/SFP); reorder points and demand forecast. **REPORTED** — https://www.helium10.com/tools/analytics/profits/ , https://revenuegeeks.com/helium10-profits/ | Daily | A **"COGS status"** field — a flag saying whether the cost number is trustworthy — is worth more than a third decimal place on the cost itself. |
| **Data Dive** | Per-listing: Master Keyword List, Product Scorecard, Ranking Juice listing score, Rank Radar daily organic rank + PPC context + "action signal"; per-keyword search volume, relevancy, exact-match suggested bid and bid range. **REPORTED** — https://datadive.tools/ , https://jordiob.com/amazon-tools/product/data-dive-tools/ | Daily rank | The **action signal**: a per-product field whose value is a verb, not a number. Rami's card needs exactly one of these. |
| **SoStocked (Carbon6)** | Forecast from velocity, seasonality, lead time, buffer stock, promotions; per-order default/backup lead times; min/max restocking with a default 35-day minimum / 90-day maximum supply window. **REPORTED** — https://help.sostocked.com/article/311-sostocked-demo-overview , https://carbon6.io/sostocked | Daily | Lead time is **per-PO**, not per-SKU. Safety stock is a *policy* field (human-set) sitting next to a *computed* cover-days field. Never merge them. |
| **Jungle Scout / Keepa** | Keepa's product object stores history as a two-dimensional `csv` array — one first-level index per history type (Amazon price, new price, used price, sales rank, Buy Box), entries alternating Keepa-time and value, with shipping-inclusive types using timestamp/price/shipping triplets and `-1` meaning "no offer". **REPORTED** — https://keepaapi.readthedocs.io/en/latest/product_query.html (page itself blocked; description via search index, 2026-09-06) | Per Keepa token budget (entry tier, 20 tokens/min per `docs/MCP-SERVERS.md`) | **History belongs in a time-series, not in the record.** Keepa does not put 400 price columns on a product. Neither should we. |
| **Perpetua / ads layer** | TACoS = ad spend ÷ *total* sales, computed per-ASIN by joining the ASIN's business-report total sales to that ASIN's ad spend across all campaigns targeting it. **REPORTED** — https://perpetua.io/blog-amazon-tacos/ | Daily | TACoS is a **join**, not a field Amazon gives you. Someone must own computing it; make that explicit. |
| **DataDoe** | 114 clean tables across Seller Central, Vendor Central and Amazon Ads, refreshed daily; MCP tools include `exports_sources_get`, `exports_create` (SQL-like filters, GROUP BY, aggregations, DAY/WEEK/MONTH intervals), `actions_start` with `dryRun`, and — critically — **`cogs_upsert` / `cogs_delete`**, plus `plugins_memories_create`. **VERIFIED** (official Deltologic repo, MIT) — https://raw.githubusercontent.com/Deltologic/datadoe-mcp/main/README.md ; table count REPORTED — https://www.datadoe.com/hub/data-scheme | Daily (REPORTED) | DataDoe will hold COGS if we push it. That makes it a **mirror**, not a source. The source stays in git next to the supplier invoice. |
| **PIM practice (Akeneo / Plytix)** | Entities kept distinct: product, variant, classification, category, asset, channel, locale. Attributes are global-base + channel-specific sets + a localization layer. Completeness is computed **per channel/locale combination** from the family's mandatory attributes. **REPORTED** — https://www.atropim.com/en/blog/product-information-management-data-model , https://www.xictron.com/en/blog/pim-strategy-product-data-sovereignty-shops-2026/ , https://www.plytix.com/blog/pim-features-capabilities/ | On edit | The single most transferable idea: **completeness is a computed status per channel**, and it is what tells you whether SKU #31 is ready for the US launch. |

The pattern across all of them: a product record is really **four records wearing one name** — an immutable-ish physical/identity record, a per-marketplace listing record, a per-day metrics series, and a human decision log. Tools that flatten these into one table become unreadable at ~40 columns. Tools that split them (Akeneo, Amazon itself) stay usable at 400.

---

## 2. The field inventory

~110 fields. Column key: **Type** = number / status / text / date / link / mirror (derived from another record) / json. **Writer** = the department that owns the value; `agent` means computed by the nightly build, `Rami` means human-only. **Mobile** = shows on Rami's phone card (Y), one tap deeper (·), or never (n).

### 2.1 Identity — 21 fields

| Field | Source of truth | Cadence | Writer | Type | Mobile |
|---|---|---|---|---|---|
| sku | git `products/` | on create | catalog | text | Y |
| marketplace | git | on create | catalog | status (CA/US/WMT-CA) | Y |
| asin | Listings Items `summaries.asin` | weekly | catalog | text | · |
| fnsku | Listings Items `summaries.fnSku` | weekly | catalog | text | n |
| parent_asin | Catalog Items `relationships.parentAsins` | weekly | catalog | text | n |
| variation_theme | Catalog Items `relationships.variationTheme` | weekly | catalog | text | n |
| upc_ean | git (from supplier/GS1) | on create | catalog | text | n |
| product_name | Listings Items `summaries.itemName` | weekly | catalog | text | Y |
| brand | git | on create | catalog | status | n |
| product_type | Listings Items `summaries.productType` | weekly | catalog | text | n |
| browse_node | Catalog `summaries.browseClassification` | monthly | catalog | text | n |
| unit_dimensions / unit_weight | Catalog `dimensions.item` | monthly | supply-chain | json | n |
| package_dimensions / package_weight | Catalog `dimensions.package` | monthly | supply-chain | json | n |
| case_pack | git (supplier spec) | on change | supply-chain | number | n |
| moq | git (supplier spec) | on change | supply-chain | number | n |
| supplier_ref | git `suppliers/<name>.md` | on change | supply-chain | link | n |
| shelf_life_days | git (supplier spec) | on change | supply-chain | number | n |
| meltable | git, per Amazon meltable policy | on change | supply-chain | status | · |
| hazmat_class | git + SDS on file | on change | account-health | status | n |
| country_of_origin | git | on create | catalog | text | n |
| certifications | git (halal, CFIA, FDA FCE/SID) | on renewal | account-health | text + file | · |

Identity is the only group that is mostly **authored**, not fetched. That is why it belongs in git and only mirrors to monday.

### 2.2 Economics — 18 fields

| Field | Source of truth | Cadence | Writer | Type | Mobile |
|---|---|---|---|---|---|
| price | Listings Items `offers.price` | daily | pricing-intel | number | **Y** |
| currency | git | static | finance | status | n |
| map_price | git (brand policy) | on change | Rami | number | n |
| price_band_min / price_band_max | git `products/<sku>.md` | on change | Rami (T2/T3) | number | · |
| cogs_unit | git, **time-versioned rows** (`effective_from`, `po_ref`) | per PO | finance | number | · |
| freight_duty_unit | git (Freightos quote / actual) | per PO | supply-chain | number | n |
| landed_cost_unit | agent = cogs + freight + duty + prep | per PO | finance | number | · |
| cogs_status | agent (fresh / estimated / stale) | nightly | finance | status | · |
| referral_fee | SP-API / DataDoe fees | monthly | finance | number | n |
| fba_fulfilment_fee | SP-API / DataDoe fees | monthly | finance | number | n |
| storage_fee_unit | DataDoe settlement | monthly | finance | number | n |
| returns_cost_unit | DataDoe returns | monthly | finance | number | n |
| ad_cost_per_unit | agent = ad spend 30d ÷ units 30d | daily | advertising | number | n |
| contribution_margin_unit | agent | daily | finance | number | · |
| contribution_margin_pct | agent | daily | finance | number | **Y** |
| margin_floor_pct | git (constitution default 15%) | on change | Rami | number | n |
| breakeven_price | agent | daily | finance | number | · |
| net_payout_unit | DataDoe settlement | monthly | finance | number | n |

`cogs_unit` as a single number is the single most common way a profit dashboard lies. Sellerboard models it by period/batch/FIFO for a reason (§1.2). Model it as rows in the git file with `effective_from`; publish only the current one to monday.

### 2.3 Inventory — 18 fields

| Field | Source of truth | Cadence | Writer | Type | Mobile |
|---|---|---|---|---|---|
| fba_available | `inventoryDetails.fulfillableQuantity` | daily 07:05 | supply-chain | number | **Y** |
| inbound_working / shipped / receiving | same object | daily | supply-chain | number | · |
| reserved_total | `reservedQuantity.totalReservedQuantity` | daily | supply-chain | number | n |
| unfulfillable_total | `unfulfillableQuantity.totalUnfulfillableQuantity` | daily | supply-chain | number | · |
| expired_units | `unfulfillableQuantity.expiredQuantity` | daily | supply-chain | number | · |
| researching_units | `researchingQuantity` | daily | supply-chain | number | n |
| stranded_flag | DataDoe stranded-inventory table | daily | account-health | status | · |
| off_amazon_stock | git (3PL/warehouse count) | weekly | supply-chain | number | n |
| units_per_day_7 / _30 | agent from Sales & Traffic `unitsOrdered` | daily | supply-chain | number | **Y** (7d) |
| cover_days | agent = fba_available ÷ units_per_day_7 | daily | supply-chain | number | **Y** |
| safety_stock_days | git (policy; floor 14d per constitution) | on change | Rami | number | n |
| reorder_point_units | agent = (lead_time + safety) × velocity | daily | supply-chain | number | · |
| next_po_ref / next_po_eta | git `approvals/` + ledger | on approval | supply-chain | link + date | · |
| lead_time_days | git, per supplier and per PO | per PO | supply-chain | number | n |
| oldest_expiry_date | git (lot record at PO receipt) | per shipment | supply-chain | date | · |
| expiry_lt90_units / expiry_90_180_units | agent from lot record + FBA age | weekly | supply-chain | number | · |

Amazon's `lastUpdatedTime` on the inventory summary is the freshness stamp for this whole group — do not invent one.

### 2.4 Advertising — 10 fields

`ad_spend_14d`, `ad_sales_14d`, `acos_14d`, `tacos_14d`, `cpc_14d`, `ad_units_14d`, `top_keyword_1..3` (with share-of-clicks from Brand Analytics SQP), `campaign_links` (link), `daily_budget_total`, `last_bid_change_at`. Source: Amazon Ads MCP (official) or DataDoe ads tables; writer: advertising; cadence: daily, except SQP keywords (weekly). Mobile: **TACoS 14d = Y**; the rest `·`. TACoS must be computed by the advertising department as a join, never read off a vendor tile (§1.2).

### 2.5 Listing — 13 fields

`listing_status` (BUYABLE/DISCOVERABLE, from Listings Items `summaries.status`), `issue_errors` / `issue_warnings` (counts from `issues[].severity`), `suppression_action` (`LISTING_SUPPRESSED` / `ATTRIBUTE_SUPPRESSED` from `issues[].enforcements`), `title`, `bullets_count`, `images_count`, `main_image_url`, `aplus_status`, `video_status`, `completeness_pct` (agent, PIM-style per marketplace — §1.2), `listing_score` (catalog audit, /20 per the existing product template), `last_catalog_audit` (date). Writer: catalog; cadence: daily for status/issues, on-change for content, monthly for the audit. Mobile: `listing_health` rollup = **Y**, the rest `·`.

### 2.6 Reviews and voice of customer — 8 fields

`rating`, `review_count`, `reviews_30d`, `last_negative_date`, `last_negative_excerpt`, `return_rate_30d`, `top_return_reason`, `ncx_status`. Sources: Keepa (rating/count history), DataDoe returns tables, Seller Central VOC via DataDoe. Writer: customer. Cadence: daily for rating/count, weekly for returns. Mobile: `rating` = **Y**; `last_negative_date` = `·`.

### 2.7 Competitors — 8 fields

`buybox_landed_price`, `buybox_win_pct`, `offer_count`, `our_bsr`, `comp_asin_1..3`, `comp_price_gap_pct`, `comp_bsr_median`, `comp_oos_flag`. Sources: **Product Pricing v0 and Keepa only** — Hard Rule 2 forbids anything else driving a price decision. Writer: pricing-intel. Cadence: daily. Mobile: `our_bsr` = **Y**, `comp_price_gap_pct` = `·`.

### 2.8 Seasonality — 5 fields

`season_index` (12 monthly multipliers, json), `ramadan_multiplier`, `q4_multiplier`, `peak_event`, `blackout_until` (date — set by the `blackout` request type in `docs/CONVENTIONS.md`). Source: git, revised monthly from history. Writer: supply-chain proposes, Rami confirms. Mobile: `blackout_until` = `·`.

### 2.9 History — 7 fields

`launch_date`, `first_sale_date`, `price_changes_90d` (count), `stockout_days_365`, `last_decision_date`, `decisions_doc` (link), `git_path` (link). Source: git + ledger. Writer: agent. Mobile: `last_decision_date` = **Y**, `decisions_doc` = **Y** (it is the "last 3 decisions" tap).

### 2.10 Status — 7 fields

`lifecycle_stage` (Planned / Launching / Active / Declining / Discontinued), `class` (Hero / Core / Long-tail / Kill), `owner_dept`, `next_review_date`, `data_health` (Fresh / Stale / Broken), `listing_health` (Live / At risk / Suppressed), `open_approvals` (count + link). Writer: chief-of-staff for class and review date, agent for health, Rami for kill decisions. Mobile: **all three statuses = Y**, plus `next_action` (§5).

---

## 3. Where the profile should live — honest comparison

Constraints that actually bind: 60 SKUs × 2 marketplaces ≈ 120 records now, ~250 at brand two; ~110 fields; nine agent writers on four different harnesses; Rami on a phone; the constitution's "nothing important lives outside this repo" and "logs are retained forever in git"; Rami "maintains no servers and babysits nothing".

| Criterion | (a) monday only | (b) monday + git markdown | (c) SQLite/Postgres/Supabase + monday mirror | (d) monday Vibe app |
|---|---|---|---|---|
| **Phone UX** | Good. Item Details shows the first three columns by default and is customisable per user via "Customize"; Android card view allows up to three columns plus a people column, with chosen order. **VERIFIED** — https://support.monday.com/hc/en-us/articles/7085413771666-monday-CRM-on-mobile | Same as (a) — monday is still the surface | Same as (a), one sync hop behind | Uncertain: **Vibe apps cannot be built on mobile** ("As of now, not yet") and viewing custom item views on mobile is not documented. **VERIFIED** — https://support.monday.com/hc/en-us/articles/32833743243282-monday-vibe-FAQs-and-Troubleshooting |
| **Agent read/write** | Good via monday MCP / GraphQL. But **formula, mirror, item_id, last_updated, creation_log and progress columns are read-only via API**, and formula returns its result only in `display_value` (`text` empty, `value` null); mirror returns a comma-joined string in `display_value`. **VERIFIED** — monday GraphQL introspection today; https://developer.monday.com/api-reference/reference/column-types-reference#read-only-columns | Best: agents write plain text in git (trivial on any harness), one process writes monday | Good, but every harness now needs DB credentials — against Hard Rule 3's spirit of minimal credentials | Adds an app runtime between agent and data for no read/write benefit |
| **History / audit** | Weak. Activity log on **Pro retains 1 year** (Basic 1 week, Standard 6 months, Enterprise 5 years). **VERIFIED** — https://support.monday.com/hc/en-us/articles/115005310745-The-Activity-Log . Constitution says forever. | Strong. git diffs are permanent and free; monday's `items_history`, `activity_logs` and `audit_logs` queries add a queryable 1-year layer on top. **VERIFIED** — GraphQL introspection today | Strong if you also back it up; you now own backups | Inherits (a) |
| **Size** | Fits easily: **1,000 columns and 10,000 items per board**. **VERIFIED** — https://developer.monday.com/apps/docs/limits#platform . But 110 columns is unusable as a UI and expensive per query. | Fits: ~34 columns on the board, the rest in git | Fits | Fits |
| **Formulas** | Mediocre. Formula columns can't be written by API, aren't supported by all dashboard widgets, and don't accept every column type; mirror columns have no column summary and only group-by under narrow conditions. **VERIFIED** — https://support.monday.com/hc/en-us/articles/360001235445-The-Formula-Column ; https://support.monday.com/hc/en-us/articles/360001733859-The-Mirror-Column | Good — compute in the agent, write a plain number column | Best | Good |
| **Export / lock-in** | Moderate. Exportable, but the record only exists in a vendor | Best — the record is a text file | Good, but you now run a database | Worst — logic lives in generated app code inside monday |
| **Multi-brand** | Duplicate board; column IDs differ per board, so every integration needs a per-board map | Same board duplication, but the schema itself is one versioned file | Clean (a `brand` column) | Rebuild or re-scope the app |
| **Cost** | Included in existing Pro seats | Included; git is free | Supabase/Postgres adds a subscription and an operational surface. Exact pricing UNKNOWN — supabase.com not reachable from this environment | Vibe requires a paying account; AI usage metered per account. **VERIFIED** — same Vibe FAQ URL |

**Recommendation: (b), with a specific division of labour.**

- **git is the system of record for authored fields**: identity, supplier and cost rows, policy (price band, margin floor, safety stock, class), seasonality, decisions, narrative. One file per SKU: `products/<brand>/<sku>.md`, YAML front-matter for the structured half, markdown below for history and open questions — an extension of the existing `docs/PRODUCT-TEMPLATE.md`.
- **monday is the system of engagement and the live-number surface**: one item per SKU × marketplace, ~34 columns, all plain types (numbers, status, date, text, link), no formulas an agent depends on.
- **The nightly build on the Mac mini** reads DataDoe + Amazon Ads MCP + Keepa + git, computes the derived fields, writes monday, writes the day's snapshot back into git, and commits. Agents that aren't the build never write monday numbers — they write proposals and git.

**Why not (a):** the 1-year Pro activity-log ceiling directly contradicts "logs retained forever in git", and a 110-column board is a bad phone experience and an expensive query.
**Why not (c):** it is the technically cleanest option and I still reject it — it adds a service Rami must keep alive, credentials in every harness, and a backup duty, for a dataset of 120 rows. Revisit at ~5 brands or when per-day metrics history genuinely needs SQL. A defensible middle: a **derived** SQLite file committed to git nightly (`state/skus.sqlite`), read-only, rebuildable from git + APIs. That gets SQL without a server.
**Why not (d):** Vibe is a *view*, not a store; it can't be built on mobile, and it puts business logic inside vendor-generated code. Build it later as a nicer face on the same board if the item card proves too cramped.

**Fallback:** if the hands runner is down or the sync proves flaky, the board must remain independently operable — every column Rami needs is a plain type he can edit by hand, and the nightly build treats a human edit as authoritative for that field until the next authored change in git (§4).

---

## 4. Proposed monday column schema — the SKU board

Board `SKU Profiles — Anabtawi`, one item per SKU × marketplace, item name `ANB-017 · CA`. Group by `class` (Hero / Core / Long-tail / Kill). 34 columns.

| Column name | monday column type | Example | Source | Writer | Cadence | Mobile? |
|---|---|---|---|---|---|---|
| Name | `name` | `ANB-017 · CA` | git | build | on create | Y |
| Product | `board_relation` → Products board | `ANB-017 Tahini 400g` | git | build | on create | Y |
| Marketplace | `status` | `CA` | git | build | on create | Y |
| ASIN | `text` | `B0C1XYZ123` | Listings Items `summaries.asin` | build | weekly | · |
| SKU | `text` | `ANB-017-CA` | git | build | on create | · |
| Class | `status` | `Hero` | git (chief-of-staff proposes) | build | weekly | Y |
| Lifecycle | `status` | `Active` | git | build | on change | · |
| Next action | `status` | `Reorder now` | agent decision rule | build | daily | **Y** |
| Owner dept | `dropdown` | `supply-chain` | git | build | on change | · |
| Price | `numbers` (CAD) | `18.99` | Listings Items `offers.price` | build | daily | **Y** |
| Price band | `text` | `17.49–21.99` | git | build | on change | · |
| Margin % | `numbers` | `21.4` | agent (finance formula) | build | daily | **Y** |
| Margin floor % | `numbers` | `15` | git | build | on change | n |
| Landed cost | `numbers` | `7.85` | git cost rows (current) | build | per PO | · |
| COGS status | `status` | `Fresh` | agent | build | nightly | · |
| Units/day 7d | `numbers` | `9.4` | Sales & Traffic `unitsOrdered` | build | daily | **Y** |
| FBA available | `numbers` | `412` | FBA Inventory `fulfillableQuantity` | build | daily 07:05 | **Y** |
| Inbound | `numbers` | `600` | FBA Inventory inbound\* sum | build | daily | · |
| Cover days | `numbers` | `44` | agent | build | daily | **Y** |
| Reorder point | `numbers` | `310` | agent | build | daily | · |
| Next PO ETA | `date` | `2026-10-14` | git `approvals/` | build | on approval | · |
| Oldest expiry | `date` | `2027-06-30` | git lot record | build | per shipment | · |
| Expiry <90d units | `numbers` | `0` | agent | build | weekly | · |
| Meltable | `status` | `Yes` | git | build | on change | · |
| Ad spend 14d | `numbers` | `184.20` | Ads MCP / DataDoe | build | daily | · |
| TACoS 14d % | `numbers` | `7.8` | agent join | build | daily | **Y** |
| Top keyword | `text` | `tahini 400g` | Brand Analytics SQP | build | weekly | · |
| Campaigns | `link` | Ads console deep link | advertising | build | on change | n |
| Rating | `rating` (or `numbers`) | `4.4` | Keepa / DataDoe | build | daily | **Y** |
| Reviews | `numbers` | `287` | Keepa / DataDoe | build | daily | · |
| BSR | `numbers` | `3,412` | Catalog `salesRanks` | build | daily | **Y** |
| Buy box % | `numbers` | `98.2` | Sales & Traffic `buyBoxPercentage` | build | daily | · |
| Listing health | `status` | `Live` | Listings Items `status` + `issues` | build | daily | **Y** |
| Data health | `status` | `Fresh` | nightly integrity check | build | nightly | **Y** |
| Data as-of | `text` (7 stamps) | `inv 07:05 · ads 07:20 · fin 03:00` | build | build | nightly | · |
| Open approvals | `numbers` + `link` | `1` | `approvals/pending/` | build | on change | **Y** |
| Decisions | `doc` (or `link` to git) | doc | chief-of-staff | build + Rami | on decision | **Y** |
| Profile (git) | `link` | `products/anabtawi/ANB-017.md` | git | build | on create | · |

Deliberately **not** columns: every fee component (they live in the git file and roll into Margin %), every inventory sub-quantity, per-keyword rank tables, competitor ASIN rows, price history, seasonality indices. Those go in the git profile, in `state/`, or in subitems.

**Subitems** carry the two genuinely repeating structures: *cost rows* (`effective_from`, `cogs`, `freight`, `duty`, `po_ref`) and *competitor rows* (`asin`, `price`, `bsr`, `seen_at`). Subitems cap at **100 per item** (**VERIFIED**, same limits page), which is ample and is also the reason daily snapshots must not be subitems.

**A second board, `Products`** — one item per SKU, marketplace-independent: brand, case pack, MOQ, supplier link, shelf life, hazmat, certifications, unit and package dimensions, meltable. The SKU board connects to it and mirrors down what it needs. This is the Akeneo product/variant split (§1.2) and it stops brand-level facts from being edited twice and diverging between CA and US.

---

## 5. Keeping it true

### 5.1 Precedence — which source wins

Precedence is **per field group, not global**. Write it once, in `docs/CONVENTIONS.md`, and have the nightly build enforce it.

| Group | Winner | Loser (evidence only) | Rule |
|---|---|---|---|
| Account facts — inventory, listing status, issues, fees, BSR, buy box | Amazon (SP-API via DataDoe / Ads MCP) | anything else | Amazon is definitionally right about Amazon. Never overwrite. |
| Price | Amazon for *what the price is*; git for *what it may be* | — | If observed price falls outside the git band → raise a `compliance-hold`-style exception, do not "fix" the band. |
| Cost | git (supplier invoice + freight actual) | DataDoe COGS, Sellerboard, any tool | Push to DataDoe via `cogs_upsert`; never read it back as truth. |
| Competitor price / BSR history | Product Pricing v0, then Keepa | everything else banned by Hard Rule 2 | Two independent sources disagreeing >5% ⇒ flag, don't average. |
| Policy — band, floor, class, safety stock, kill | git / Rami | agent proposals | Agents may only propose (T2/T3). |
| Derived — cover days, TACoS, margin, reorder point | the nightly build | monday formulas, tool dashboards | One computation, one place. Formula columns are read-only via API anyway (§3). |
| Narrative, decisions | git | monday item updates | An update in monday is copied into git; git is canonical. |

Conflict handling has exactly three outcomes: **overwrite** (Amazon over stale mirror), **flag** (two legal sources disagree), **halt** (a source failed — Hard Rule 8 says say so and stop, never guess).

### 5.2 Freshness stamps

Seven stamps, not 110 — one per field group: `identity_asof`, `economics_asof`, `inventory_asof`, `ads_asof`, `listing_asof`, `voc_asof`, `competitors_asof`. Store them in the git profile front-matter and render them into the single `Data as-of` text column on the board. Inventory's stamp should be Amazon's own `lastUpdatedTime`, not the time our job ran — the distinction matters when Amazon's feed lags.

Max ages (proposed; Rami confirms with the week-one guardrails): inventory 24h, economics 36h, ads 24h, listing 48h, competitors 48h, VOC 8 days, identity 35 days.

### 5.3 Stale-flagging and the nightly integrity check

`data_health` per record: **Fresh** (all groups inside max age), **Stale** (any group over, none critical), **Broken** (inventory or economics over max age, or an assertion fails). A Broken record is excluded from the daily decision list with a reason, rather than silently producing a confident wrong number.

Nightly check (runs after the build, writes `state/integrity.md`, opens a `requests/.../inbox` item on failure):

1. Every SKU in `products/` has a monday item per active marketplace, and vice versa — no orphans either way.
2. `sku` → `asin` → `fnsku` mapping matches Listings Items; a changed ASIN is an alert, not an update.
3. `price` inside `[price_band_min, price_band_max]`; else flag T2.
4. `contribution_margin_pct ≥ margin_floor_pct`; else flag.
5. `landed_cost_unit > 0` and its cost row's `effective_from` is within 180 days; else `cogs_status = Stale`.
6. `cover_days` recomputes from stored `fba_available ÷ units_per_day_7` within 1 day.
7. `fulfillable + inbound* + reserved + unfulfillable + researching == totalQuantity` from the FBA object.
8. Hero SKUs: `cover_days ≥ 14`; seasonal buffer ≥ 6 weeks inside a peak window (constitution §4).
9. `meltable = Yes` ⇒ no inbound shipment ETA between 1 May and 30 Sep.
10. `oldest_expiry_date` more than 90 days out for anything inbound; nothing within 50 days on arrival.
11. `listing_status` contains BUYABLE and `issue_errors = 0`; else `listing_health = At risk/Suppressed`.
12. Sum of ad spend across SKUs ≤ the daily ad cap (CAD 150).
13. Every `open_approvals` link resolves to a file in `approvals/pending/` that has not expired (48h).
14. Every group's `*_asof` is inside max age.
15. Sum of monday `Price × units/day` reconciles to DataDoe revenue for the day within 2%.

### 5.4 How history is kept — all three, for different jobs

- **Per-field change log:** monday gives this free. `activity_logs` on a board returns `event`, `data` (column values in string form), `created_at`, `user_id`; `items_history` and `aggregate_history` queries exist; `audit_logs` covers account-level security events. **VERIFIED** — GraphQL introspection, 2026-09-06. Retention on Pro is 1 year (§3), so treat it as a convenience layer, not the archive.
- **Daily snapshot rows:** in **git, not monday**. One append-only `state/skus/YYYY-MM-DD.jsonl`, 120 lines a day, ~40 MB a year uncompressed and far less in git. Putting snapshots in monday would consume the 10,000-item board cap in about 83 days (120 × 365 = 43,800) — a hard, verified reason not to.
- **git diffs:** the authored half. Every change to a price band, a class, a cost row or a decision is a commit with a department and a date, per the constitution's run procedure step 10. This is the forever archive and the only one that satisfies "logs are retained forever in git".

Rule of thumb: **numbers get snapshots, decisions get diffs, and the board gets the last value plus a stamp.**

---

## 6. The one-screen card for Rami

Rami should be able to answer "does this SKU need me today?" without scrolling. Eight numbers, three statuses, three decisions.

**Eight numbers:** Price · Margin % · Units/day (7d) · Cover days · FBA available · TACoS 14d · Rating · BSR.
**Three statuses:** Next action (the verb — `Reorder now` / `Approve price` / `Watch` / `Nothing`) · Listing health · Data health.
**Three decisions:** the last three lines of the decisions log, newest first, each one line: date, what changed, who proposed, ledger link.

Shaping monday to that:

- Mobile Details shows the **first three columns by default** and the set is user-customisable via "Customize" (**VERIFIED**, monday CRM on mobile article above). So order the board columns so that Next action, Cover days and Margin % are first, and have Rami tick the eight numbers plus three statuses in Customize once.
- Put the last-three-decisions block in a **pinned item update** (`Update.pinned_to_top` exists — **VERIFIED**, introspection) refreshed nightly by the build, so it sits at the top of the item's Updates tab. That is the "tap for why" surface, and it also gives Rami a reply box — his reply is a decision the next run picks up.
- The `Decisions` `doc` column holds the full narrative for when he wants it; the git file is the archive behind it.
- Keep a saved board view "Rami — today", filtered to `Next action ≠ Nothing` **or** `Data health = Broken`, sorted by Class then Cover days. That view, not the full board, is the thing that gets a phone shortcut.
- Do **not** rely on formula columns for anything on this card: they are read-only to the API and not supported by every dashboard widget (§3). Every number on the card is a plain `numbers` column the build wrote.

One caution, stated honestly: monday's mobile item page is a vertical list, not a designed card. Eight numbers plus three statuses will be roughly one and a half screens on a phone. If that proves too loose after a month of use, the right fix is a **Vibe item view** rendering exactly this card over the same board — a view layer, not a second store, and reversible.

---

## 7. Parent/child and marketplace grain

**Recommendation: one profile per SKU × marketplace, with a marketplace-independent parent record — not marketplace sub-records.**

Three grains actually exist, and conflating any two of them causes a specific failure:

1. **Product** (marketplace-independent): recipe, case pack, supplier, shelf life, meltable, hazmat, certifications, dimensions. One record per SKU. → the `Products` board + `products/<brand>/<sku>.md`.
2. **Listing** (SKU × marketplace): everything else. Amazon itself is built this way — summaries, dimensions, identifiers, images, relationships and sales ranks are all `...ByMarketplace` arrays (§1.1, VERIFIED). → the `SKU Profiles` board, one item each.
3. **Variation family** (parent ASIN): a *presentation* fact, not an operational one, for a 60-SKU food brand. Store `parent_asin` and `variation_theme` as fields on the listing record and group by them in views. Do not create parent items until a real variation family exists with shared inventory decisions.

Why not marketplace sub-records under one SKU item: subitems in monday are second-class for filtering, dashboards and mobile; mirrored subitem values group only under narrow conditions and have no column summary (§3, VERIFIED). More decisively, ~70% of the fields are marketplace-scoped, so the "shared" parent would be thin and the sub-record fat — the tail wagging the dog. And the US launch is precisely a case where the same product needs a completely independent price band, cost (freight and duty differ), inventory, ads and listing health. Two items, one product link.

Practical consequence for the US launch: a US listing record can exist in `Planned` lifecycle with no ASIN, carrying the target price band, the landed-cost model with US freight and duty, and a completeness percentage — so the "are we ready for mid-January?" question becomes a filter on one board rather than a research project.

---

## 8. Multi-brand instantiation

The template must be data, not documentation.

1. **One schema file:** `docs/SKU-SCHEMA.yaml` lists every field with its group, type, monday column type, source, writer department, cadence, max age and mobile flag. The tables in §2 and §4 are generated from it. Changing the schema is a commit and a review, not a click in a board.
2. **Board instantiation:** for brand two, create a new monday workspace and run `create_board` + `create_column` from the schema file (both are available as MCP tools). Column **IDs differ per board**, so the build resolves *column title → column id* at boot and caches the map in `runtimes/monday-columns-<board_id>.json`. Never hard-code a monday column id in a department skill; that is the single most likely thing to break brand two.
3. **git layout:** `products/<brand>/<sku>.md`, `suppliers/<brand>/`, `markets/<brand>-<marketplace>.md`. Departments already read `products/`; scoping by brand keeps one runtime able to serve both.
4. **What is shared vs copied:** the schema, the department charters, the playbooks and the integrity checks are **shared**. Guardrail numbers, price bands, seasonality indices, supplier records and the DataDoe/Ads credentials are **per brand**. A brand-two bootstrap is therefore: new workspace, generate boards from schema, create `brands/<brand>/GUARDRAILS.md`, connect its DataDoe seller id, run the build once in T0.
5. **Cost check:** brand two adds monday items (well within 10,000) and DataDoe seller connections. It should not add a database, an app, or a seat if the boards live in the same account. UNKNOWN: whether monday Pro's 2 seats and its per-plan API daily call cap (Pro: 10,000 calls/day, **VERIFIED** via developer docs cited in §3) stay comfortable at two brands — at 250 records × ~6 writes/day plus reads, it should, but measure in month one.

---

## Implications for the design

1. **Split the record into four, then rejoin it in one view.** Product / listing / metrics-series / decisions. Every tool that flattens these becomes unreadable; Amazon and the PIM world both split them.
2. **git holds what we decide; monday holds what we watch.** This is the only arrangement that satisfies both "nothing important lives outside this repo" and "Rami opens it on his phone", given that monday Pro forgets its activity log after a year.
3. **No agent should write a monday number except the nightly build.** Nine writers on one board is a reconciliation problem you cannot debug at 07:00. Agents write proposals and git; the build writes monday.
4. **Never depend on a monday formula.** They are read-only to the API, return values only in `display_value`, and aren't supported by every widget. Compute in the agent, write a plain number.
5. **COGS is a table, not a number.** Time-versioned rows with `effective_from` and `po_ref`, plus a `cogs_status` flag. Push to DataDoe via `cogs_upsert`; never read it back as truth.
6. **Meltable and expiry are first-class fields for this brand.** The FBA meltable window (1 Oct – 30 Apr) and the >90-day / 50-day shelf-life rules can void a US Ramadan launch outright; they belong in the nightly integrity check, not in a playbook paragraph.
7. **`data_health` before every number.** A Broken record must be excluded from the decision list with a stated reason. Hard Rule 8 already says stop rather than guess; this makes it mechanical.
8. **Snapshots go to git, never to monday items.** 120 records × 365 days exceeds the verified 10,000-item board cap in under three months.
9. **Two marketplaces means two records from day one** — build the US listing records now, in `Planned`, so launch readiness is a board filter rather than a project.

## Open questions

1. **Guardrail confirmations (constitution §4 is still TODO):** max ages per field group, `safety_stock_days` per class, and whether the 15% margin floor is pre- or post-ads for the profile's `contribution_margin_pct`.
2. **DataDoe's actual table and field names.** The schema page (`datadoe.com/hub/data-scheme`) is unreachable from here; the 114-table count is REPORTED. Before writing the build, run `exports_sources_get` and pin the exact source names and their refresh times into `docs/CONVENTIONS.md`.
3. **DataDoe refresh timing vs Amazon's 07:00 Asia/Jerusalem close.** "Refreshed daily" is REPORTED with no stated hour. The build's schedule depends on it.
4. **Keepa token budget.** 20 tokens/min on the entry tier (per `docs/MCP-SERVERS.md`) against 120 records daily — needs a cost model and probably a weekly-not-daily cadence for competitor history.
5. **Brand Analytics access via DataDoe** for SQP at ASIN granularity in Canada — brand-registry-gated, and whether the CA marketplace exposes ASIN view is UNKNOWN.
6. **monday API daily call ceiling at two brands.** Pro is 10,000 calls/day (VERIFIED); measure actual usage in month one before brand two.
7. **Expiry lots.** Amazon's `expiredQuantity` tells you what already expired; it does not tell you what will. `oldest_expiry_date` has to come from our own lot record at PO receipt — confirm the supplier will print and share lot/expiry per carton.
8. **Whether Rami wants the item-update reply loop.** Replying to the pinned decisions update is the cheapest possible approval gesture on a phone, but it is not the T2 approval path in `approvals/` — decide whether a reply is a signal or a decision.
