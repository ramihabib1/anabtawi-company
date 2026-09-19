---
department: health
date: 2026-09-19
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings remain suppressed for invalid condition type (age 15 days); CA Active listings rose to 8 (`GG-0DC1-SKHG` Inactive→Active). US launch gate 1 remains overdue (due 2026-09-15); gates 3–4 due 2026-09-20 (1 day). Real-time listing/account notification sources remain disabled in DataDoe.

## Data
### Account status (DataDoe export `25fd7411-a8a6-4338-a1b1-0d6606777c16`, Seller Account Health Metrics, window 2026-09-01→2026-09-19; latest CA row 2026-09-18, latest US row 2026-09-18)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `d01744ac-4cb6-4947-be18-1aeefe743999`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 8 | 23 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 44), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `KP-MEL9-XYGW` (B0FXXQHDHP, FBA avail 16), `FO-SE3J-T74M` (B0FT8GSHMV, FBA avail 14), `5G-ZW6Q-WOZG` (B0FT3KLFHK, FBA avail 13), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1), `ZK-4NDS-MNA9` (B0FT3L774Y, FBA avail 0), `GG-0DC1-SKHG` (B0FTSQ8M46, FBA avail 0). Status change vs yesterday: `GG-0DC1-SKHG` Inactive→Active.

### Open listing issues with Amazon enforcement (DataDoe export `22b4c6c9-a973-4c0c-bbbe-dbe89d863ebe`, Listings Raw JSON; compared to state/health.md 2026-09-18)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 15 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 15 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 15 (first seen 2026-09-04) |

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
Not Monday; weekly Seller Central AHR recording reminder not issued today. DataDoe metrics show CA 212 GREAT / US 200 GREAT as of 2026-09-18.

## Exceptions
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` remains 100%; 39 rows returned. CA mix vs 2026-09-18: Active 8 / Inactive 23 / Incomplete 6 (was Active 7 / Inactive 24 / Incomplete 6).
- Metrics: latest CA and US dates both now 2026-09-18 (advanced from 2026-09-17; no 2026-09-19 rows yet).
- Hero Active FBA available qtys vs 2026-09-18: `OA-26MX-IHV0`=44, `26-JITG-E4FU`=19, `KP-MEL9-XYGW`=16, `FO-SE3J-T74M`=14 (was 15), `5G-ZW6Q-WOZG`=13, `0C-45D7-6JUB`=1, `ZK-4NDS-MNA9`=0, `GG-0DC1-SKHG`=0 (new Active).
- US launch gate 1 due 2026-09-15 is overdue with no status update in playbooks/us-launch.md.
- US launch gates 3–4 due 2026-09-20 are 1 day out; ungating and FDA/FSVP remain open items for this department.

## Requests sent
- none new this run (open hold already with catalog: 20260904-0626-account-health-compliance-hold; ## Update 2026-09-19 appended)

## Proposals written
- none (no Amazon response required)
