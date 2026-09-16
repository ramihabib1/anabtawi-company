---
department: health
date: 2026-09-16
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: []
---
## Headline
CA and US Account Health Rating GREAT (CA 212, US 200) with zero policy-violation counts; three CA parent listings remain suppressed for invalid condition type (age 12 days); CA late-shipping rate improved FAIR→GOOD on latest metrics date 2026-09-15. CA Active listings unchanged at 6. US launch gate 1 (unified account / tax interview) is now overdue (due 2026-09-15). Real-time listing/account notification sources remain disabled in DataDoe.

## Data
### Account status (DataDoe export `5dcee674-e910-4255-8794-8c2c22d5619b`, Seller Account Health Metrics, window 2026-09-01→2026-09-16; latest CA row 2026-09-15, latest US row 2026-09-15)
| marketplace | seller_account_status | AHR 6m status | AHR score | listing policy count | food/safety count | IP received | IP suspected | other policy | docs requests | ODR FBA | late ship 30d | on-time delivery | valid tracking | pre-fulfill cancel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ca | null | GREAT | 212 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |
| us | null | GREAT | 200 | 0 | 0 | GOOD | 0 | 0 | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD |

### Listing status summary (DataDoe export `e351f6b0-ce59-47c2-b4d3-ed08d58d8b2d`, Listings, 39 rows)
| marketplace | Active | Inactive | Incomplete | rows |
|---|---|---|---|---|
| ca | 6 | 25 | 6 | 37 |
| us | 0 | 2 | 0 | 2 |

CA Active SKUs: `OA-26MX-IHV0` (B0FT3DNMJR, FBA avail 44), `26-JITG-E4FU` (B0FXXM1CK8, FBA avail 19), `FO-SE3J-T74M` (B0FT8GSHMV, FBA avail 15), `5G-ZW6Q-WOZG` (B0FT3KLFHK, FBA avail 16), `KP-MEL9-XYGW` (B0FXXQHDHP, FBA avail 16), `0C-45D7-6JUB` (B0FXX2QVF8, FBA avail 1). No Active↔Inactive status changes vs yesterday.

### Open listing issues with Amazon enforcement (DataDoe export `8667b0ca-ac66-49af-98ca-f6d05ce2c9bb`, Listings Raw JSON; compared to state/health.md 2026-09-15)
| sku | asin | marketplace | status | issue | enforcement | age_days |
|---|---|---|---|---|---|---|
| Holy-Land-Cookies-Parent | B0GKGW6DJ7 | ca | Incomplete | code 8115 invalid condition type | LISTING_SUPPRESSED | 12 (first seen 2026-09-04) |
| Premium-Baklava-Gift-Parent | B0GKGQ15SQ | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 12 (first seen 2026-09-04) |
| Holy-Land-Baklava-Gift-Parent | B0GKH8YNXP | ca | Incomplete | code 8115 invalid condition type; code 18367 product_type PASTRY→FOOD note | LISTING_SUPPRESSED | 12 (first seen 2026-09-04) |

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
Not Monday; weekly Seller Central AHR recording reminder not issued today. DataDoe metrics show CA 212 GREAT / US 200 GREAT as of 2026-09-15.

## Exceptions
- CA `seller_late_shipping_rate_30d_status` improved FAIR→GOOD on latest metrics date 2026-09-15 (export `5dcee674…`); prior FAIR on 2026-09-14.
- DataDoe sources `Listings Item Issues Change Notifications`, `Listings Item Status Change Notifications`, and `Account Status Changed Notifications` are enabled=false for this org — no near-real-time policy/account notices available.
- Listings table `initialLoadProgress` remains 100%; 39 rows returned. CA mix unchanged vs 2026-09-15: Active 6 / Inactive 25 / Incomplete 6.
- Metrics: latest CA and US dates both now 2026-09-15 (advanced from 2026-09-14; no 2026-09-16 rows yet).
- Hero Active FBA available qtys vs 2026-09-15: `OA-26MX-IHV0`=44 (was 43), `26-JITG-E4FU`=19, `0C-45D7-6JUB`=1, `FO-SE3J-T74M`=15, `5G-ZW6Q-WOZG`=16, `KP-MEL9-XYGW`=16.
- US launch gate 1 due 2026-09-15 is overdue with no status update in playbooks/us-launch.md.

## Requests sent
- none new this run (open hold already with catalog: 20260904-0626-account-health-compliance-hold; ## Update 2026-09-16 appended)

## Proposals written
- none (no Amazon response required)
