---
department: supply-chain
date: 2026-09-06
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily CA cover check: 28 SKUs at fulfillable 0; estimated lost revenue about CAD 1252.43/day while OOS. Hero SKUs under floor (lead time TBD=0): 18-116Z-1R77, T8-2W2X-INOK, YE-HCDW-4UYW, ASW-H50. FBA inbound: RECEIVING still open on FBA19H427DS7/FBA19JXFX4KT; new IN_TRANSIT FBA19NZ90PPZ (plan updated 2026-09-05, likely manufacturer restock) for 5G-ZW6Q-WOZG/FO-SE3J-T74M/KP-MEL9-XYGW/ZK-4NDS-MNA9 — READY_TO_SHIP FBA19NSL8M11 treated as near-duplicate and not double-counted. YE-HCDW-4UYW inbound lot expires 2026-11-23 (within 90 days). No PO proposals this week per inbox 20260903-1700. US FBA: 2 SKUs listed, both fulfillable 0; US orders export 0 rows.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408 (ANABTAWI SWEETS CA)`; US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469 (ANABTAWI SWEETS US)`. Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30 = units on last known in-stock days ÷ those days; denom noted when not 30.
cover_days = (fulfillable + inbound in cover window) ÷ velocity_30. cover_adjusted = cover_days (no seasonal multiplier today).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-05.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-30 to 2026-09-06 job 55d4002e-a652-40ed-99f9-ed331fb8a1f6
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-08 to 2026-09-06 job 6593e1b9-7c05-4954-9f90-a006e7d10df4
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job 9a1cf79e-7489-4f44-82ea-8987040b2012 (17 raw rows; Counted RECEIVING in full; for IN_TRANSIT vs READY_TO_SHIP near-duplicate plans took IN_TRANSIT (or max) to avoid double-count)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job f3c012fc-0bdf-4ba4-af9c-4918740f9372 (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-30 to 2026-09-06 job ac51369c-07f6-4db9-9764-a3832f5ac88b
- DataDoe export Order Line Items US job e53c092b-756e-4486-9b54-a12f18371962 (0 rows)
- DataDoe export FBA Inbound Shipments US job 047a1780-07f2-40cb-9e39-b6935161d993 (mirrors CA confirmation IDs; not applied to US cover)

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
| 2 | ca | ASW-H50 | true | 0 | 0 | none | 1.5556 | 9 | 0.0 | 0.0 | 14 | TBD | 2026-09-01 | 59.99 | 1.5556 | 93.32 | critical |
| 3 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | receiving-now,in-transit | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 2.7500 | 90.72 | ok |
| 4 | ca | FO-SE3J-T74M | true | 0 | 53 | receiving-now,in-transit | 2.6429 | 14 | 20.05 | 20.05 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 2.6429 | 87.19 | watch |
| 5 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 39.99 | 2.0000 | 79.98 | critical |
| 6 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.4074 | 27 | 26.58 | 26.58 | 14 | TBD | on-or-before-2026-08-29 | 32.99 | 2.4074 | 79.42 | ok |
| 7 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.4 | 6.4 | 14 | TBD | on-or-before-2026-08-29 | 59.99 | 1.2500 | 74.99 | critical |
| 8 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 21.99 | 2.5000 | 54.97 | critical |
| 9 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.2500 | 12 | 0.0 | 0.0 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.2500 | 53.74 | critical |
| 10 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.3333 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 34.99 | 1.3333 | 46.65 | critical |
| 11 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 1.5333 | 15 | 14.35 | 14.35 | 14 | TBD | on-or-before-2026-08-29 | 29.99 | 1.5333 | 45.98 | watch |
| 12 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.5714 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 27.99 | 1.5714 | 43.98 | critical |
| 13 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 42.99 | 1.0000 | 42.99 | critical |
| 14 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.5714 | 14 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 25.99 | 1.5714 | 40.84 | critical |
| 15 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.5000 | 8 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 26.99 | 1.5000 | 40.48 | critical |
| 16 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 39.99 | 1.0000 | 39.99 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.8571 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 17.99 | 1.8571 | 33.41 | critical |
| 18 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 19.99 | 1.4286 | 28.56 | critical |
| 19 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 28.00 | 1.0000 | 28.00 | critical |
| 20 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.1429 | 14 | 14.0 | 14.0 | 14 | TBD | on-or-before-2026-08-29 | 12.99 | 2.1429 | 27.84 | watch |
| 21 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 24.99 | 1.0000 | 24.99 | critical |
| 22 | ca | KP-MEL9-XYGW | false | 0 | 18 | in-transit | 1.2222 | 9 | 14.73 | 14.73 | 14 | TBD | on-or-before-2026-08-29 | 19.99 | 1.2222 | 24.43 | watch |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | 0.0 | 14 | TBD | on-or-before-2026-08-29 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 0C-45D7-6JUB | false | 1 | 0 | none | 0.5000 | 10 | 2.0 | 2.0 | 14 | TBD | 2026-09-05 | 59.99 | 0.0000 | 0.00 | critical |
| 26 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 18.99 | 0.0000 | 0.00 | critical |
| 27 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 49.99 | 0.0000 | 0.00 | critical |
| 28 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 0.00 | 0.0000 | 0.00 | critical |
| 29 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | in-transit | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-29 | 23.99 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.7368 | 50.21 | 50.21 | 2026-09-05 | 19.99 | ok |
| ca | OA-26MX-IHV0 | 46 | 54 | receiving-now | 0.8182 | 122.22 | 122.22 | 2026-09-05 | 21.00 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |
| ca | H8-PWJ0-3B1Y | true | 64 | 26.58 | ok |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-05 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-05 |

### Inbound ETAs (CA FBA shipments export, deduped)
| sku | qty | status | confirmation | window/ETA |
|---|---:|---|---|---|
| 26-JITG-E4FU | 18 | RECEIVING:18 | FBA19H427DS7 | receiving-now |
| 5G-ZW6Q-WOZG | 68 | RECEIVING:36;IN_TRANSIT:32 | FBA19H427DS7,FBA19NZ90PPZ | receiving-now,in-transit |
| EU-Z87B-ZRBZ | 36 | RECEIVING:36 | FBA19H427DS7 | receiving-now |
| FO-SE3J-T74M | 53 | RECEIVING:36;IN_TRANSIT:17 | FBA19H427DS7,FBA19NZ90PPZ | receiving-now,in-transit |
| GG-0DC1-SKHG | 22 | RECEIVING:22 | FBA19H427DS7 | receiving-now |
| H8-PWJ0-3B1Y | 64 | RECEIVING:64 | FBA19H427DS7 | receiving-now |
| KP-MEL9-XYGW | 18 | IN_TRANSIT:18 | FBA19NZ90PPZ | in-transit |
| OA-26MX-IHV0 | 54 | RECEIVING:54 | FBA19H427DS7 | receiving-now |
| TB-PIST-120 | 30 | RECEIVING:30 | FBA19JXFX4KT | receiving-now |
| YE-HCDW-4UYW | 8 | RECEIVING:8 | FBA19H427DS7 | receiving-now |
| ZK-4NDS-MNA9 | 18 | IN_TRANSIT:18 | FBA19NZ90PPZ | in-transit |

### Manufacturer open order (not yet fully received into fulfillable)
| placed | ships | ETA at FBA | lines | status | source |
|---|---|---|---|---|---|
| before 2026-09-03 | 2026-09-04 | likely reflected as IN_TRANSIT FBA19NZ90PPZ (updated 2026-09-05); full line list TBD | 5G-ZW6Q-WOZG 32; FO-SE3J-T74M 17; KP-MEL9-XYGW 18; ZK-4NDS-MNA9 18 (and possibly more) | in transit | suppliers/anabtawi.md + DataDoe inbound |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-05 |
Expiry within 90 days: YE-HCDW-4UYW inbound RECEIVING lot expiration 2026-11-23 (DataDoe FBA Inbound Shipments expiration field). Other inbound expirations are 2027-06-12/13.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-05; Amazon business day closes 07:00 Asia/Jerusalem.
- Orders export may still be incomplete near the current day (historical note in state/company-smoke-test.md).
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with IN_TRANSIT vs READY_TO_SHIP near-duplicate dedupe.
- READY_TO_SHIP plan FBA19NSL8M11 still shows selected delivery window starting 2026-09-11; overlapping SKUs also appear IN_TRANSIT on FBA19NZ90PPZ (2026-09-05) — counted once.
- products/ empty — heroes by 90-day CA revenue. suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD.
- No Freightos landed-cost run (no PO proposals this week).
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover; 2 catalog SKUs at fulfillable 0.
- Capacity/IPI unavailable.

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-06; hero SKUs under floor+lead: 18-116Z-1R77, T8-2W2X-INOK, YE-HCDW-4UYW, ASW-H50)
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md

## Proposals written
- none (inbox 20260903-1700: do not write purchase order proposals this week; manufacturer restock shipped 2026-09-04 / IN_TRANSIT visible)
