---
department: supply-chain
date: 2026-09-05
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily CA cover check: 28 SKUs at fulfillable 0; estimated lost revenue about CAD 1286.26/day while OOS. Hero SKUs under floor (lead time TBD=0): 18-116Z-1R77, ASW-H50, T8-2W2X-INOK, YE-HCDW-4UYW. FBA inbound still 13 lines (9 RECEIVING + 4 READY_TO_SHIP on FBA19NSL8M11 with selected delivery window 2026-09-11→2026-09-17). Manufacturer restock shipped 2026-09-04 (ETA at FBA TBD). YE-HCDW-4UYW inbound lot expires 2026-11-23 (within 90 days). No PO proposals this week per inbox 20260903-1700. US FBA: 2 SKUs listed, both fulfillable 0, no US orders export this run.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408 (ANABTAWI SWEETS CA)`; US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469 (ANABTAWI SWEETS US)`. Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30 = units on last known in-stock days ÷ those days; denom noted when not 30.
cover_days = (fulfillable + inbound in cover window) ÷ velocity_30. cover_adjusted = cover_days (no seasonal multiplier today).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-04 (no 2026-09-05 rows yet).

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-29 to 2026-09-05 job f2a41d74-0aad-478d-a737-49b853647e40
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-07 to 2026-09-05 job 4b3eb3d9-b94d-4c78-b491-94c5a5779bdd
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job ba09ef57-12e0-4124-b0fe-2545f1988148
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job bc9bad32-484e-4494-8862-e63205057636 (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-29 to 2026-09-05 job b42a44a7-1d58-4ad2-a4a1-95830b49da5f

### Heroes (top 10 by 90-day CA revenue)
| rank | sku | rev_90_CAD | units_90 |
|---:|---|---:|---:|
| 1 | H8-PWJ0-3B1Y | 2144.35 | 65 |
| 2 | EU-Z87B-ZRBZ | 2015.64 | 36 |
| 3 | FO-SE3J-T74M | 1220.63 | 37 |
| 4 | 5G-ZW6Q-WOZG | 1088.67 | 33 |
| 5 | YE-HCDW-4UYW | 899.85 | 15 |
| 6 | ASW-H50 | 839.86 | 14 |
| 7 | GG-0DC1-SKHG | 689.77 | 23 |
| 8 | T8-2W2X-INOK | 652.85 | 15 |
| 9 | 18-116Z-1R77 | 571.78 | 22 |
| 10 | TB-PIST-120 | 389.70 | 30 |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 2.2500 | 16 | 16.0 | 16.0 | 14 | TBD | on-or-before-2026-08-29 | 55.99 | 2.2500 | 125.98 | watch |
| 2 | ca | ASW-H50 | true | 0 | 0 | none | 1.6250 | 8 | 0.0 | 0.0 | 14 | TBD | 2026-08-31 | 59.99 | 1.6250 | 97.48 | critical |
| 3 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | 2026-09-11,receiving-now | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 2.7500 | 90.72 | ok |
| 4 | ca | FO-SE3J-T74M | true | 0 | 53 | 2026-09-11,receiving-now | 2.6429 | 14 | 20.05 | 20.05 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 2.6429 | 87.19 | watch |
| 5 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 39.99 | 2.0000 | 79.98 | critical |
| 6 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.4074 | 27 | 26.58 | 26.58 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 2.4074 | 79.42 | ok |
| 7 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.4 | 6.4 | 14 | TBD | on-or-before-2026-08-29 | 59.99 | 1.2500 | 74.99 | critical |
| 8 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.2500 | 12 | 0.0 | 0.0 | 14 | TBD | unknown (no FBA inventory rows in export window) | 44.99 | 1.2500 | 56.24 | critical |
| 9 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 21.99 | 2.5000 | 54.97 | critical |
| 10 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.5000 | 8 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 33.99 | 1.5000 | 50.98 | critical |
| 11 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.3333 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 34.99 | 1.3333 | 46.65 | critical |
| 12 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 1.5333 | 15 | 14.35 | 14.35 | 14 | TBD | on-or-before-2026-08-29 | 29.99 | 1.5333 | 45.98 | watch |
| 13 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 44.99 | 1.0000 | 44.99 | critical |
| 14 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.5714 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 27.99 | 1.5714 | 43.98 | critical |
| 15 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 42.99 | 1.0000 | 42.99 | critical |
| 16 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.5714 | 14 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 25.99 | 1.5714 | 40.84 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.8571 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 17.99 | 1.8571 | 33.41 | critical |
| 18 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 1.0000 | 32.99 | critical |
| 19 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 19.99 | 1.4286 | 28.56 | critical |
| 20 | ca | KP-MEL9-XYGW | false | 0 | 16 | 2026-09-11 | 1.2222 | 9 | 13.09 | 13.09 | 14 | TBD | on-or-before-2026-08-29 | 22.99 | 1.2222 | 28.10 | critical |
| 21 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 28.00 | 1.0000 | 28.00 | critical |
| 22 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.1429 | 14 | 14.0 | 14.0 | 14 | TBD | on-or-before-2026-08-29 | 12.99 | 2.1429 | 27.84 | watch |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 0C-45D7-6JUB | false | 1 | 0 | none | 0.5000 | 10 | 2.0 | 2.0 | 14 | TBD | 2026-09-04 | 59.99 | 0.0000 | 0.00 | critical |
| 26 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 0.00 | 0.0000 | 0.00 | critical |
| 27 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 0.00 | 0.0000 | 0.00 | critical |
| 28 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 0.00 | 0.0000 | 0.00 | critical |
| 29 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | 2026-09-11 | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 0.00 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.7368 | 50.22 | 50.22 | 2026-09-04 | 19.99 | ok |
| ca | OA-26MX-IHV0 | 48 | 54 | receiving-now | 0.5455 | 186.98 | 186.98 | 2026-09-04 | 21.00 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |
| ca | H8-PWJ0-3B1Y | true | 64 | 26.58 | ok |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | no US orders export this run; snap 2026-09-04 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | no US orders export this run; snap 2026-09-04 |

### Inbound ETAs (CA FBA shipments export)
| sku | qty | status | confirmation | window/ETA |
|---|---:|---|---|---|
| 26-JITG-E4FU | 18 | RECEIVING:18 | see export | receiving-now |
| 5G-ZW6Q-WOZG | 68 | READY_TO_SHIP:32;RECEIVING:36 | FBA19NSL8M11 | 2026-09-11,receiving-now |
| EU-Z87B-ZRBZ | 36 | RECEIVING:36 | see export | receiving-now |
| FO-SE3J-T74M | 53 | READY_TO_SHIP:17;RECEIVING:36 | FBA19NSL8M11 | 2026-09-11,receiving-now |
| GG-0DC1-SKHG | 22 | RECEIVING:22 | see export | receiving-now |
| H8-PWJ0-3B1Y | 64 | RECEIVING:64 | see export | receiving-now |
| KP-MEL9-XYGW | 16 | READY_TO_SHIP:16 | FBA19NSL8M11 | 2026-09-11 |
| OA-26MX-IHV0 | 54 | RECEIVING:54 | see export | receiving-now |
| TB-PIST-120 | 30 | RECEIVING:30 | see export | receiving-now |
| YE-HCDW-4UYW | 8 | RECEIVING:8 | see export | receiving-now |
| ZK-4NDS-MNA9 | 18 | READY_TO_SHIP:18 | FBA19NSL8M11 | 2026-09-11 |

### Manufacturer open order (not yet an FBA inbound row)
| placed | ships | ETA at FBA | lines | status | source |
|---|---|---|---|---|---|
| before 2026-09-03 | 2026-09-04 | TBD | TBD (Rami to add) | shipped / in transit from 2026-09-04 | suppliers/anabtawi.md |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 2 | Inventory Health inv_age_181+ buckets on snap 2026-09-04 |
Expiry within 90 days: YE-HCDW-4UYW inbound RECEIVING lot expiration 2026-09-05+79d = 2026-11-23 (DataDoe FBA Inbound Shipments expiration field). Other inbound expirations are 2027-06-12/13.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-04; no 2026-09-05 snapshot rows yet (Amazon business day closes 07:00 Asia/Jerusalem).
- Orders export may still be incomplete from 2026-09-01 (state/company-smoke-test.md historical note).
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export.
- READY_TO_SHIP plan FBA19NSL8M11 now shows selected delivery window 2026-09-11→2026-09-17 (was ship window 2026-09-04 on prior run).
- products/ empty — heroes by 90-day CA revenue. suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD.
- No Freightos landed-cost run (no PO proposals this week).
- US: no orders export this run; 2 catalog SKUs at fulfillable 0.
- Capacity/IPI unavailable.

## Requests sent
- 20260905-0620-supply-chain-stockout-risk → advertising (hero SKUs under floor+lead: ASW-H50, YE-HCDW-4UYW, T8-2W2X-INOK, 18-116Z-1R77)
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md

## Proposals written
- none (inbox 20260903-1700: do not write purchase order proposals this week; manufacturer restock shipped 2026-09-04)
