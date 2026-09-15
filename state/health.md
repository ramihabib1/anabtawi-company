---
department: health
date: 2026-09-15
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings remain suppressed for invalid condition type (age 11 days); CA late-shipping rate still FAIR. CA Active listings dropped 7→6 (`ZK-4NDS-MNA9` Active→Inactive); restocked FBA on `FO-SE3J-T74M`, `5G-ZW6Q-WOZG`, `KP-MEL9-XYGW`. Metrics latest date advanced to 2026-09-14 on both marketplaces. US launch gate 1 (unified account / tax interview) is due today. Real-time listing/account notification sources remain disabled in DataDoe.

## Data
### Account status (DataDoe export `bed84ba5-403d-40ed-8899-245b2aba4499`, Seller Account Health Metrics, window 2026-09-01→2026-09-15; latest CA row 2026-09-14, latest US row 2026-09-14)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | FAIR | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `716e49ad-7be0-4cff-809e-b62681cf3ba8`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 6 | 25 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 43), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `FO-SE3J-T74M` (B0FT8GSHMV, FBA avail 15), `5G-ZW6Q-WOZG` (B0FT3KLFHK, FBA avail 16), `KP-MEL9-XYGW` (B0FXXQHDHP, FBA avail 16), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1). `ZK-4NDS-MNA9` moved Active→Inactive vs yesterday.

### Open listing issues with Amazon enforcement (DataDoe export `00af2175-31c9-4bac-8a92-6cfdec3955ef`, Listings Raw JSON; compared to state/health.md 2026-09-14)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 11 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 11 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 11 (first seen 2026-09-04) |

No new suppressed SKUs vs yesterday. No Amazon appeal packet: fix remains a listing attribute update (catalog), not a response to Amazon. Prior compliance-hold `requests/catalog/inbox/20260904-0626-account-health-compliance-hold.md` still unanswered (needed-by 2026-09-06T07:00+03:00, now overdue); update appended today; no duplicate hold sent.

### Deadlines within 30 days
| due | item | owner | source |
|---|---|---|---|
| 2026-09-15 | Confirm North America unified account covers US; US tax interview done | Rami | playbooks/us-launch.md gate 1 (due today) |
| 2026-09-20 | Grocery category requirements / ungating for top 10 SKUs, US | account-health | playbooks/us-launch.md gate 3; open item |
| 2026-09-20 | FDA agent engaged; FSVP QI named; supplier verification file opened | account-health | playbooks/us-launch.md gate 4 |
| 2026-09-30 | Brand Registry US | Rami | playbooks/us-launch.md gate 2 |
| 2026-10-01 | FDA Food Facility Registration renewal window opens (through 2026-12-31) | account-health | state/calendar.md |
| 2026-10-15 | Cross-border accountant: 1120-F protective filing decision, nexus posture | finance | playbooks/us-launch.md gate 13 |

### Monday AHR reminder
Not Monday; weekly Seller Central AHR recording reminder not issued today. DataDoe metrics show CA 212 GREAT / US 200 GREAT as of 2026-09-14.

## Exceptions
- CA `seller_late_shipping_rate_30d_status` = FAIR (export `bed84ba5…`, latest CA metrics date 2026-09-14). Watch; not a compliance-hold.
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` remains 100%; 39 rows returned. CA mix changed vs 2026-09-14: Active 7→6, Inactive 24→25, Incomplete 6 unchanged.
- Metrics: latest CA and US dates both now 2026-09-14 (advanced from 2026-09-13; no 2026-09-15 rows yet).
- Hero Active FBA available qtys vs 2026-09-14: `OA-26MX-IHV0`=43, `26-JITG-E4FU`=19, `0C-45D7-6JUB`=1; `FO-SE3J-T74M`=15 (was 0), `5G-ZW6Q-WOZG`=16 (was 0), `KP-MEL9-XYGW`=16 (was 0).

## Requests sent
- none new this run (open hold already with catalog: 20260904-0626-account-health-compliance-hold; ## Update 2026-09-15 appended)

## Proposals written
- none (no Amazon response required)
