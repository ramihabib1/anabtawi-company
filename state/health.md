---
department: health
date: 2026-09-04
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings are suppressed for invalid condition type; CA late-shipping rate is FAIR. Real-time listing/account notification sources are disabled in DataDoe, so coverage is export-only.

## Data
### Account status (DataDoe export `9706bd0a-e451-4655-8728-6e8d7eccc47d`, Seller Account Health Metrics, window 2026-09-01→2026-09-04)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | 0 | 0 | 0 | GOOD | GOOD (0) | FAIR | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | 0 | 0 | 0 | GOOD | GOOD (0) | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `d3932b72-604d-4995-b37f-0c53dae85f14`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 3 | 28 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 48), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1).

### Open listing issues with Amazon enforcement (DataDoe export `af1412a6-b1ed-4485-80c5-01e0e17f4898`, Listings Raw JSON; first run so age starts today)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 0 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 0 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 0 (first seen 2026-09-04) |

No Amazon appeal packet written: fix is a listing attribute update (catalog), not a response to Amazon.

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
- CA `seller_late_shipping_rate_30d_status` = FAIR (export `9706bd0a…`). Watch; not a compliance-hold.
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` was 20% at source discovery; 39 rows returned. Treat catalog completeness as provisional until load hits 100%.
- Prior `state/health.md` was placeholder (`not-yet-run`); cannot compare deltas to a prior real run.

## Requests sent
- 20260904-0626-account-health-compliance-hold → catalog (three suppressed parent SKUs)

## Proposals written
- none (no Amazon response required)
