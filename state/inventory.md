---
department: supply-chain
date: 2026-09-04
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily CA cover check: 28 SKUs at fulfillable 0; estimated lost revenue about CAD 1243.94/day while OOS. Hero SKUs under floor (lead time TBD=0): ASW-H50, YE-HCDW-4UYW, T8-2W2X-INOK, 18-116Z-1R77. New FBA inbound READY_TO_SHIP plan FBA19NSL8M11 (4 lines, ship window 2026-09-04). Manufacturer restock ships 2026-09-04 (ETA at FBA TBD). No PO proposals this week per inbox 20260903-1700. US FBA: 2 SKUs listed, both fulfillable 0, no US orders export this run.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408 (ANABTAWI SWEETS CA)`; US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469 (ANABTAWI SWEETS US)`. Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30 = units on last known in-stock days ÷ those days; denom noted when not 30.
cover_days = (fulfillable + inbound in cover window) ÷ velocity_30. cover_adjusted = cover_days (no seasonal multiplier today).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-03 (no 2026-09-04 rows yet).

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-28 to 2026-09-04 job a04473db-5761-4309-9bda-8cf7dff5ee66
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-06 to 2026-09-04 job b903c6d3-f2e2-4a49-86f6-6cf45c6b2b6f
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job 52b9a2fc-bec3-46c1-8010-1dba1cbe8906
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job 8dac8444-d875-489f-8b0a-0eb8c962cb55 (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-28 to 2026-09-04 job fa065dd7-2cd2-41d1-837c-beb6ea6d2c38

### Heroes (top 10 by 90-day CA revenue)
| rank | sku | rev_90_CAD | units_90 |
|---:|---|---:|---:|
| 1 | H8-PWJ0-3B1Y | 2144.35 | 65 |
| 2 | EU-Z87B-ZRBZ | 2015.64 | 36 |
| 3 | FO-SE3J-T74M | 1220.63 | 37 |
| 4 | 5G-ZW6Q-WOZG | 1088.67 | 33 |
| 5 | YE-HCDW-4UYW | 899.85 | 15 |
| 6 | ASW-H50 | 839.86 | 14 |
| 7 | T8-2W2X-INOK | 697.84 | 16 |
| 8 | GG-0DC1-SKHG | 689.77 | 23 |
| 9 | 18-116Z-1R77 | 597.77 | 23 |
| 10 | TB-PIST-120 | 389.70 | 30 |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 2.2500 | 16 | 16.0 | 16.0 | 14 | TBD | on-or-before-2026-08-27 | 55.99 | 2.2500 | 125.98 | watch |
| 2 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | 2026-09-04,receiving-now | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | on-or-before-2026-08-27 | 32.99 | 2.7500 | 90.72 | ok |
| 3 | ca | FO-SE3J-T74M | true | 0 | 53 | 2026-09-04,receiving-now | 2.6429 | 14 | 20.05 | 20.05 | 14 | TBD | on-or-before-2026-08-27 | 32.99 | 2.6429 | 87.19 | watch |
| 4 | ca | ASW-H50 | true | 0 | 0 | none | 1.4444 | 9 | 0.0 | 0.0 | 14 | TBD | 2026-08-31 | 59.99 | 1.4444 | 86.65 | critical |
| 5 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 39.99 | 2.0000 | 79.98 | critical |
| 6 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.4074 | 27 | 26.58 | 26.58 | 14 | TBD | on-or-before-2026-08-27 | 32.99 | 2.4074 | 79.42 | ok |
| 7 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.4 | 6.4 | 14 | TBD | on-or-before-2026-08-27 | 59.99 | 1.2500 | 74.99 | critical |
| 8 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 21.99 | 2.5000 | 54.97 | critical |
| 9 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.2308 | 13 | 0.0 | 0.0 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.2308 | 52.91 | critical |
| 10 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.3333 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 34.99 | 1.3333 | 46.65 | critical |
| 11 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 1.5333 | 15 | 14.35 | 14.35 | 14 | TBD | on-or-before-2026-08-27 | 29.99 | 1.5333 | 45.98 | watch |
| 12 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.5714 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 27.99 | 1.5714 | 43.98 | critical |
| 13 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 42.99 | 1.0000 | 42.99 | critical |
| 14 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.5000 | 8 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 26.99 | 1.5000 | 40.48 | critical |
| 15 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 39.99 | 1.0000 | 39.99 | critical |
| 16 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.5333 | 15 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 25.99 | 1.5333 | 39.85 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.8571 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 17.99 | 1.8571 | 33.41 | critical |
| 18 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 19.99 | 1.4286 | 28.56 | critical |
| 19 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 28.00 | 1.0000 | 28.00 | critical |
| 20 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.1429 | 14 | 14.0 | 14.0 | 14 | TBD | on-or-before-2026-08-27 | 12.99 | 2.1429 | 27.84 | watch |
| 21 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 24.99 | 1.0000 | 24.99 | critical |
| 22 | ca | KP-MEL9-XYGW | false | 0 | 16 | 2026-09-04 | 1.2222 | 9 | 13.09 | 13.09 | 14 | TBD | on-or-before-2026-08-27 | 19.99 | 1.2222 | 24.43 | critical |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-27 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 0C-45D7-6JUB | false | 1 | 0 | none | 0.5000 | 10 | 2.0 | 2.0 | 14 | TBD | 2026-09-03 | 59.99 | 0.0000 | 0.00 | critical |
| 26 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-27 | 0.00 | 0.0000 | 0.00 | critical |
| 27 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-27 | 0.00 | 0.0000 | 0.00 | critical |
| 28 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-27 | 0.00 | 0.0000 | 0.00 | critical |
| 29 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | 2026-09-04 | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-27 | 0.00 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.7778 | 47.57 | 47.57 | 2026-09-03 | 19.99 | ok |
| ca | OA-26MX-IHV0 | 48 | 54 | receiving-now | 0.6000 | 170.0 | 170.0 | 2026-09-03 | 21.00 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | H8-PWJ0-3B1Y | true | 64 | 26.58 | ok |
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | no US orders export this run; snap 2026-09-03 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | no US orders export this run; snap 2026-09-03 |

### Inbound ETAs (CA FBA shipments export)
| sku | qty | status | confirmation | window/ETA |
|---|---:|---|---|---|
| 26-JITG-E4FU | 18 | RECEIVING:18 | see export | receiving-now |
| 5G-ZW6Q-WOZG | 68 | READY_TO_SHIP:32;RECEIVING:36 | see export | 2026-09-04,receiving-now |
| EU-Z87B-ZRBZ | 36 | RECEIVING:36 | see export | receiving-now |
| FO-SE3J-T74M | 53 | READY_TO_SHIP:17;RECEIVING:36 | see export | 2026-09-04,receiving-now |
| GG-0DC1-SKHG | 22 | RECEIVING:22 | see export | receiving-now |
| H8-PWJ0-3B1Y | 64 | RECEIVING:64 | see export | receiving-now |
| KP-MEL9-XYGW | 16 | READY_TO_SHIP:16 | see export | 2026-09-04 |
| OA-26MX-IHV0 | 54 | RECEIVING:54 | see export | receiving-now |
| TB-PIST-120 | 30 | RECEIVING:30 | see export | receiving-now |
| YE-HCDW-4UYW | 8 | RECEIVING:8 | see export | receiving-now |
| ZK-4NDS-MNA9 | 18 | READY_TO_SHIP:18 | see export | 2026-09-04 |

### Manufacturer open order (not yet an FBA inbound row)
| placed | ships | ETA at FBA | lines | status | source |
|---|---|---|---|---|---|
| before 2026-09-03 | 2026-09-04 | TBD | TBD (Rami to add) | ships today / in transit from 2026-09-04 | suppliers/anabtawi.md |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 2 | Inventory Health inv_age_181+ buckets on snap 2026-09-03 |
Expiry within 90 days: no expiry-date field in the DataDoe exports used; not assessed.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-03; no 2026-09-04 snapshot rows yet (Amazon business day closes 07:00 Asia/Jerusalem).
- Orders export may still be incomplete from 2026-09-01 (state/company-smoke-test.md historical note).
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export.
- New READY_TO_SHIP inbound plan FBA19NSL8M11 (updated 2026-09-03) for KP-MEL9-XYGW, ZK-4NDS-MNA9, 5G-ZW6Q-WOZG, FO-SE3J-T74M.
- products/ empty — heroes by 90-day CA revenue. suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD.
- No Freightos landed-cost run (no PO proposals this week).
- US: no orders export this run; 2 catalog SKUs at fulfillable 0.
- Capacity/IPI unavailable; expiry unavailable.

## Requests sent
- 20260904-0625-supply-chain-stockout-risk → advertising (hero SKUs under floor+lead: ASW-H50, YE-HCDW-4UYW, T8-2W2X-INOK, 18-116Z-1R77)
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md

## Proposals written
- none (inbox 20260903-1700: do not write purchase order proposals this week; manufacturer restock ships 2026-09-04)
