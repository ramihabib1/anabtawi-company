---
department: health
date: 2026-09-05
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings remain suppressed for invalid condition type (age 1 day); CA late-shipping rate still FAIR. Real-time listing/account notification sources remain disabled in DataDoe, so coverage is export-only.

## Data
### Account status (DataDoe export `04ceb720-9793-41f2-a312-d7aa7bbccbe8`, Seller Account Health Metrics, window 2026-09-01→2026-09-05; latest rows dated 2026-09-04)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | 0 | 0 | 0 | GOOD | GOOD (0) | FAIR | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | 0 | 0 | 0 | GOOD | GOOD (0) | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `947a053e-236d-4e1c-a076-28b9e70f5651`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 3 | 28 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 48), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1).

### Open listing issues with Amazon enforcement (DataDoe export `e43b1f51-c156-499b-9d8b-95ec614980b9`, Listings Raw JSON; compared to state/health.md 2026-09-04)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 1 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 1 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 1 (first seen 2026-09-04) |

No new suppressed SKUs vs yesterday. No Amazon appeal packet: fix remains a listing attribute update (catalog), not a response to Amazon. Prior compliance-hold `requests/catalog/inbox/20260904-0626-account-health-compliance-hold.md` still unanswered; no duplicate hold sent.

### Deadlines within 30 days
| due | item | owner | source |
|---|---|---|---|
| 2026-09-15 | Confirm North America unified account covers US; US tax interview done | Rami | playbooks/us-launch.md gate 1 |
| 2026-09-20 | Grocery category requirements / ungating for top 10 SKUs, US | account-health | playbooks/us-launch.md gate 3; open item |
| 2026-09-20 | FDA agent engaged; FSVP QI named; supplier verification file opened | account-health | playbooks/us-launch.md gate 4 |
| 2026-09-30 | Brand Registry US | Rami | playbooks/us-launch.md gate 2 |
| 2026-10-01 | FDA Food Facility Registration renewal window opens (through 2026-12-31) | account-health | state/calendar.md |

### AHR recording reminder
Not Monday — no reminder this run. Next Monday remind Rami to record Seller Central AHR into this file (he reads it himself).

## Exceptions
- CA `seller_late_shipping_rate_30d_status` = FAIR (export `04ceb720…`, unchanged vs 2026-09-04). Watch; not a compliance-hold.
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` was 15% at source discovery; 39 rows returned (same row count as yesterday). Treat catalog completeness as provisional until load hits 100%.
- Metrics export latest date is 2026-09-04 (no 2026-09-05 row yet in window).

## Requests sent
- none this run (open hold already with catalog: 20260904-0626-account-health-compliance-hold)

## Proposals written
- none (no Amazon response required)
