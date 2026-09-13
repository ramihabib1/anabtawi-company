---
department: health
date: 2026-09-13
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings remain suppressed for invalid condition type (age 9 days); CA late-shipping rate still FAIR. Listing status mix unchanged vs yesterday; metrics latest date advanced to 2026-09-12 on both marketplaces. Real-time listing/account notification sources remain disabled in DataDoe.

## Data
### Account status (DataDoe export `91c96e9c-9454-424b-9f45-27702c4552cf`, Seller Account Health Metrics, window 2026-09-01→2026-09-13; latest CA row 2026-09-12, latest US row 2026-09-12)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD (0) | FAIR | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD (0) | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `e295d929-65a1-4b84-aeb5-c9efa94f6e61`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 7 | 24 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 44), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1), `ZK-4NDS-MNA9` (B0FT3L774Y, FBA avail 0), `FO-SE3J-T74M` (B0FT8GSHMV, FBA avail 0), `5G-ZW6Q-WOZG` (B0FT3KLFHK, FBA avail 0), `KP-MEL9-XYGW` (B0FXXQHDHP, FBA avail 0).

### Open listing issues with Amazon enforcement (DataDoe export `90e878e3-ef9c-4036-8bfb-238888c40418`, Listings Raw JSON; compared to state/health.md 2026-09-12)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 9 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 9 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 9 (first seen 2026-09-04) |

No new suppressed SKUs vs yesterday. No Amazon appeal packet: fix remains a listing attribute update (catalog), not a response to Amazon. Prior compliance-hold `requests/catalog/inbox/20260904-0626-account-health-compliance-hold.md` still unanswered (needed-by 2026-09-06T07:00+03:00, now overdue); update appended today; no duplicate hold sent.

### Deadlines within 30 days
| due | item | owner | source |
|---|---|---|---|
| 2026-09-15 | Confirm North America unified account covers US; US tax interview done | Rami | playbooks/us-launch.md gate 1 |
| 2026-09-20 | Grocery category requirements / ungating for top 10 SKUs, US | account-health | playbooks/us-launch.md gate 3; open item |
| 2026-09-20 | FDA agent engaged; FSVP QI named; supplier verification file opened | account-health | playbooks/us-launch.md gate 4 |
| 2026-09-30 | Brand Registry US | Rami | playbooks/us-launch.md gate 2 |
| 2026-10-01 | FDA Food Facility Registration renewal window opens (through 2026-12-31) | account-health | state/calendar.md |
| 2026-10-15 | Cross-border accountant: 1120-F protective filing decision, nexus posture | finance | playbooks/us-launch.md gate 13 |

## Exceptions
- CA `seller_late_shipping_rate_30d_status` = FAIR (export `91c96e9c…`, latest CA metrics date 2026-09-12). Watch; not a compliance-hold.
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` remains 100%; 39 rows returned. CA Active/Inactive/Incomplete unchanged vs 2026-09-12 (7/24/6).
- Metrics: latest CA and US dates both now 2026-09-12 (advanced from 2026-09-11; no 2026-09-13 rows yet).
- Hero Active FBA available qtys vs 2026-09-12: `OA-26MX-IHV0`=44, `26-JITG-E4FU`=19, `0C-45D7-6JUB`=1 (unchanged).

## Requests sent
- none new this run (open hold already with catalog: 20260904-0626-account-health-compliance-hold; ## Update 2026-09-13 appended)

## Proposals written
- none (no Amazon response required)
