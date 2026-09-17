---
department: health
date: 2026-09-17
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings remain suppressed for invalid condition type (age 13 days); CA Active listings rose 6→7 as `ZK-4NDS-MNA9` became Active (FBA avail 0). US launch gate 1 remains overdue (due 2026-09-15). Real-time listing/account notification sources remain disabled in DataDoe.

## Data
### Account status (DataDoe export `424dc05b-e840-4df0-b419-e343412c403b`, Seller Account Health Metrics, window 2026-09-01→2026-09-17; latest CA row 2026-09-16, latest US row 2026-09-16)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `8a1b0940-d05c-4eaf-87b8-6f06899a08c9`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 7 | 24 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 44), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `FO-SE3J-T74M` (B0FT8GSHMV, FBA avail 15), `5G-ZW6Q-WOZG` (B0FT3KLFHK, FBA avail 14), `KP-MEL9-XYGW` (B0FXXQHDHP, FBA avail 16), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1), `ZK-4NDS-MNA9` (B0FT3L774Y, FBA avail 0). Status change vs yesterday: `ZK-4NDS-MNA9` Inactive→Active.

### Open listing issues with Amazon enforcement (DataDoe export `a25a7042-ff06-4cc9-9f9f-20bb470df9cb`, Listings Raw JSON; compared to state/health.md 2026-09-16)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 13 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 13 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 13 (first seen 2026-09-04) |

No new suppressed SKUs vs yesterday. No Amazon appeal packet: fix remains a listing attribute update (catalog), not a response to Amazon. Prior compliance-hold `requests/catalog/inbox/20260904-0626-account-health-compliance-hold.md` still unanswered (needed-by 2026-09-06T07:00+03:00, now overdue); update appended today; no duplicate hold sent.

### Deadlines within 30 days
| due | item | owner | source |
|---|---|---|---|
| 2026-09-15 | Confirm North America unified account covers US; US tax interview done | Rami | playbooks/us-launch.md gate 1 (OVERDUE) |
| 2026-09-20 | Grocery category requirements / ungating for top 10 SKUs, US | account-health | playbooks/us-launch.md gate 3; open item |
| 2026-09-20 | FDA agent engaged; FSVP QI named; supplier verification file opened | account-health | playbooks/us-launch.md gate 4 |
| 2026-09-30 | Brand Registry US | Rami | playbooks/us-launch.md gate 2 |
| 2026-10-01 | FDA Food Facility Registration renewal window opens (through 2026-12-31) | account-health | state/calendar.md |
| 2026-10-15 | Cross-border accountant: 1120-F protective filing decision, nexus posture | finance | playbooks/us-launch.md gate 13 |

### Monday AHR reminder
Not Monday; weekly Seller Central AHR recording reminder not issued today. DataDoe metrics show CA 212 GREAT / US 200 GREAT as of 2026-09-16.

## Exceptions
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` remains 100%; 39 rows returned. CA mix vs 2026-09-16: Active 6→7 / Inactive 25→24 / Incomplete 6 (unchanged).
- Metrics: latest CA and US dates both now 2026-09-16 (advanced from 2026-09-15; no 2026-09-17 rows yet).
- Hero Active FBA available qtys vs 2026-09-16: `OA-26MX-IHV0`=44, `26-JITG-E4FU`=19, `0C-45D7-6JUB`=1, `FO-SE3J-T74M`=15, `5G-ZW6Q-WOZG`=14 (was 16), `KP-MEL9-XYGW`=16; new Active `ZK-4NDS-MNA9`=0.
- US launch gate 1 due 2026-09-15 is overdue with no status update in playbooks/us-launch.md.

## Requests sent
- none new this run (open hold already with catalog: 20260904-0626-account-health-compliance-hold; ## Update 2026-09-17 appended)

## Proposals written
- none (no Amazon response required)
