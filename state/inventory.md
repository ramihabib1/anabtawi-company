---
department: supply-chain
date: 2026-09-07
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: [freightos]
---
## Headline
Monday weekly: 12-week forecast refreshed from CA orders 2026-06-09..2026-09-07; ROP recomputed with ASSUMED lead=21d/MOQ=1/case=1 (suppliers/anabtawi.md still TBD). Estimated OOS lost revenue about CAD 1297.31/day. Hero under floor (lead TBD=0 for status): 18-116Z-1R77, ASW-H50, GG-0DC1-SKHG, T8-2W2X-INOK, YE-HCDW-4UYW. 10 hero PO proposals written as T2 files with product cash from COGS where known; Freightos landed cost blocked (MCP not connected) so status degraded. Manufacturer IN_TRANSIT FBA19NZ90PPZ still open; READY_TO_SHIP FBA19NSL8M11 near-duplicate not double-counted.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408 (ANABTAWI SWEETS CA)`; US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469 (ANABTAWI SWEETS US)`. Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30: if fulfillable>0 use last-30 calendar units÷30; if stockout in window use units_90÷sale_days_90 (vel_denom=sale_days). cover_days=(fulfillable+inbound)÷velocity_30. cover_adjusted=cover_days (no seasonal multiplier).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-06.
PO sizing ASSUMED (labeled in proposals): lead 21d, review 7d, buffer 14d, MOQ 1, case pack 1 — replace when suppliers/anabtawi.md is filled.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-31 to 2026-09-07 job aa3050af-f7ca-4c5f-b445-b3a46ea1a2b3
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-09 to 2026-09-07 job 445627c9-8169-40c0-8fc4-629ff39db773
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job a6085637-2395-46f8-ad6d-9b3427aaf116 (17 raw rows; RECEIVING counted in full; IN_TRANSIT vs READY_TO_SHIP near-duplicate plans took IN_TRANSIT)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job dd7f31cd-4d4d-479c-b279-e7351541fbca (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-31 to 2026-09-07 job df4464d1-1eb0-49c5-bf9b-0e10d165b28c
- DataDoe export Order Line Items US job d9895d09-8f34-48b4-b765-0899f0bea64b (0 rows)
- DataDoe export FBA Inbound Shipments US snapshot job 171b5f6c-a753-4bc0-9ddc-781da06de9e5

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
| 9 | 18-116Z-1R77 | 545.79 | 21 |
| 10 | TB-PIST-120 | 389.70 | 30 |

### 12-week forecast (heroes) — weekly units
Method: mean of last up to 8 ISO weeks of CA shipped units; forward 12 weeks = flat mean (playbooks/ has only us-launch.md; no CA seasonality multipliers; no launches in state/calendar.md).
| sku | avg_weekly | fwd_weekly_x12 | recent_hist (week:units) |
|---|---:|---|---|
| H8-PWJ0-3B1Y | 7.88 | 7.88 × 12 | 2026-W33:10.0, 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0 |
| EU-Z87B-ZRBZ | 4.50 | 4.50 × 12 | 2026-W33:3.0, 2026-W34:24.0, 2026-W35:2.0, 2026-W36:0.0 |
| FO-SE3J-T74M | 4.62 | 4.62 × 12 | 2026-W33:6.0, 2026-W34:28.0, 2026-W35:1.0, 2026-W36:0.0 |
| 5G-ZW6Q-WOZG | 4.12 | 4.12 × 12 | 2026-W33:23.0, 2026-W34:3.0, 2026-W35:0.0, 2026-W36:0.0 |
| YE-HCDW-4UYW | 0.88 | 0.88 × 12 | 2026-W33:4.0, 2026-W34:1.0, 2026-W35:0.0, 2026-W36:0.0 |
| ASW-H50 | 1.75 | 1.75 × 12 | 2026-W33:0.0, 2026-W34:1.0, 2026-W35:12.0, 2026-W36:1.0 |
| GG-0DC1-SKHG | 2.75 | 2.75 × 12 | 2026-W33:5.0, 2026-W34:13.0, 2026-W35:1.0, 2026-W36:0.0 |
| T8-2W2X-INOK | 0.12 | 0.12 × 12 | 2026-W33:0.0, 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0 |
| 18-116Z-1R77 | 0.12 | 0.12 × 12 | 2026-W33:1.0, 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0 |
| TB-PIST-120 | 3.75 | 3.75 × 12 | 2026-W33:15.0, 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0 |

### Reorder points (ASSUMED lead 21d + review 7d)
| sku | hero | velocity_30 | ROP_units | target_units (ROP+buffer14) | fulfillable | inbound | po_qty_assumed | status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| ASW-H50 | true | 2.0000 | 56.0 | 84.0 | 0 | 0 | 84 | critical |
| FO-SE3J-T74M | true | 3.0833 | 86.3 | 129.5 | 0 | 53 | 77 | watch |
| 18-116Z-1R77 | true | 1.5000 | 42.0 | 63.0 | 0 | 0 | 63 | critical |
| T8-2W2X-INOK | true | 1.3636 | 38.2 | 57.3 | 0 | 0 | 58 | critical |
| TB-PIST-120 | true | 2.0000 | 56.0 | 84.0 | 0 | 30 | 54 | watch |
| EU-Z87B-ZRBZ | true | 2.1176 | 59.3 | 88.9 | 0 | 36 | 53 | watch |
| 5G-ZW6Q-WOZG | true | 2.7500 | 77.0 | 115.5 | 0 | 68 | 48 | ok |
| GG-0DC1-SKHG | true | 1.6429 | 46.0 | 69.0 | 0 | 22 | 47 | critical |
| H8-PWJ0-3B1Y | true | 2.6000 | 72.8 | 109.2 | 0 | 64 | 46 | ok |
| YE-HCDW-4UYW | true | 1.2500 | 35.0 | 52.5 | 0 | 8 | 45 | critical |
| KL-GDUL-HEA1 | false | 2.5000 | 70.0 | 105.0 | 0 | 0 | 105 | critical |
| C5-TXQU-Y67R | false | 2.0000 | 56.0 | 84.0 | 0 | 0 | 84 | critical |
| AN-9938-NXOT | false | 1.7143 | 48.0 | 72.0 | 0 | 0 | 72 | critical |
| W3-UQRU-PGRR | false | 1.6667 | 46.7 | 70.0 | 0 | 0 | 70 | critical |
| BU-6GOS-GW5Q | false | 1.6250 | 45.5 | 68.2 | 0 | 0 | 69 | critical |
| 3I-SHTN-9CKQ | false | 1.4286 | 40.0 | 60.0 | 0 | 0 | 60 | critical |
| 09-AJOP-CS83 | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| 1S-ITGB-CZFR | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| 9Z-KUHZ-FU2I | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| E3-DSPC-O2UN | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| FX-M8MA-MMSA | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| O3-V1B9-CH1H | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| Y4-Y8EE-VEOD | false | 1.0000 | 28.0 | 42.0 | 0 | 0 | 42 | critical |
| KP-MEL9-XYGW | false | 1.2222 | 34.2 | 51.3 | 0 | 18 | 34 | watch |
| 0C-45D7-6JUB | false | 0.0333 | 0.9 | 1.4 | 1 | 0 | 1 | ok |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | ASW-H50 | true | 0 | 0 | none | 2.0000 | 7 | 0.00 | 0.00 | 14 | TBD | 2026-09-01 | 59.99 | 2.0000 | 119.98 | critical |
| 2 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 2.1176 | 17 | 17.00 | 17.00 | 14 | TBD | on-or-before-2026-08-30 | 55.99 | 2.1176 | 118.57 | watch |
| 3 | ca | FO-SE3J-T74M | true | 0 | 53 | in-transit,receiving-now | 3.0833 | 12 | 17.19 | 17.19 | 14 | TBD | on-or-before-2026-08-30 | 32.99 | 3.0833 | 101.72 | watch |
| 4 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | in-transit,receiving-now | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | on-or-before-2026-08-30 | 32.99 | 2.7500 | 90.72 | ok |
| 5 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.6000 | 25 | 24.62 | 24.62 | 14 | TBD | on-or-before-2026-08-30 | 32.99 | 2.6000 | 85.77 | ok |
| 6 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 39.99 | 2.0000 | 79.98 | critical |
| 7 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.40 | 6.40 | 14 | TBD | on-or-before-2026-08-30 | 59.99 | 1.2500 | 74.99 | critical |
| 8 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.3636 | 11 | 0.00 | 0.00 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.3636 | 58.62 | critical |
| 9 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 21.99 | 2.5000 | 54.97 | critical |
| 10 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 1.6429 | 14 | 13.39 | 13.39 | 14 | TBD | on-or-before-2026-08-30 | 29.99 | 1.6429 | 49.27 | critical |
| 11 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.6667 | 6 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 27.99 | 1.6667 | 46.65 | critical |
| 12 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.7143 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 26.99 | 1.7143 | 46.27 | critical |
| 13 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 42.99 | 1.0000 | 42.99 | critical |
| 14 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 39.99 | 1.0000 | 39.99 | critical |
| 15 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.5000 | 14 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 25.99 | 1.5000 | 38.98 | critical |
| 16 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 34.99 | 1.0000 | 34.99 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.6250 | 8 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 17.99 | 1.6250 | 29.23 | critical |
| 18 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 28.99 | 1.0000 | 28.99 | critical |
| 19 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 19.99 | 1.4286 | 28.56 | critical |
| 20 | ca | KP-MEL9-XYGW | false | 0 | 18 | in-transit | 1.2222 | 9 | 14.73 | 14.73 | 14 | TBD | on-or-before-2026-08-30 | 22.99 | 1.2222 | 28.10 | watch |
| 21 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 28.00 | 1.0000 | 28.00 | critical |
| 22 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.0000 | 15 | 15.00 | 15.00 | 14 | TBD | on-or-before-2026-08-30 | 12.99 | 2.0000 | 25.98 | watch |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |
| 26 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |
| 27 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |
| 28 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | in-transit | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | 0 | none | 0.0333 | 30.00 | 30.00 | 2026-09-06 | 59.99 | ok |
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.1333 | 277.50 | 277.50 | 2026-09-06 | 19.99 | ok |
| ca | OA-26MX-IHV0 | 45 | 54 | receiving-now | 0.1667 | 594.00 | 594.00 | 2026-09-06 | 21.00 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |
| ca | H8-PWJ0-3B1Y | true | 64 | 24.62 | ok |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-06 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-06 |

### Inbound ETAs (CA FBA shipments export, deduped)
| sku | qty | status | confirmation | window/ETA |
|---|---:|---|---|---|
| 26-JITG-E4FU | 18 | RECEIVING:18 | FBA19H427DS7 | receiving-now |
| 5G-ZW6Q-WOZG | 68 | RECEIVING:36;IN_TRANSIT:32 | FBA19H427DS7,FBA19NZ90PPZ | in-transit,receiving-now |
| EU-Z87B-ZRBZ | 36 | RECEIVING:36 | FBA19H427DS7 | receiving-now |
| FO-SE3J-T74M | 53 | RECEIVING:36;IN_TRANSIT:17 | FBA19H427DS7,FBA19NZ90PPZ | in-transit,receiving-now |
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
| before 2026-09-03 | 2026-09-04 | IN_TRANSIT FBA19NZ90PPZ (updated 2026-09-05); READY_TO_SHIP FBA19NSL8M11 treated as near-duplicate | 5G-ZW6Q-WOZG 32; FO-SE3J-T74M 17; KP-MEL9-XYGW 18; ZK-4NDS-MNA9 18 (and possibly more) | in transit | suppliers/anabtawi.md + DataDoe inbound |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-06 |
Expiry within 90 days: YE-HCDW-4UYW inbound lot expiration 2026-11-23.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-06; Amazon business day closes 07:00 Asia/Jerusalem.
- Freightos MCP is configured in departments/supply-chain/.mcp.json but is not connected on this grok-bot runtime — landed cost cannot be computed; PO proposals include product cash (COGS×qty) only and mark landed cost PENDING.
- suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD — PO quantities use ASSUMED lead 21d, MOQ 1, case pack 1.
- state/cash.md has never been run; need-cash-check sent to finance, unanswered at write time.
- products/ empty — heroes by 90-day CA revenue.
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with IN_TRANSIT vs READY_TO_SHIP near-duplicate dedupe.
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover.
- Capacity/IPI unavailable.
- Prior Rami hold (requests/supply-chain/done/20260903-1700-rami-info.md) was for that week only; Monday weekly run resumes PO proposals.

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-07)
- new 20260907-0610-supply-chain-need-cash-check → finance
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md

## Proposals written
- approvals/pending/20260907-supply-chain-po-ASW-H50.md (qty 84; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-EU-Z87B-ZRBZ.md (qty 53; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-FO-SE3J-T74M.md (qty 77; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-5G-ZW6Q-WOZG.md (qty 48; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-H8-PWJ0-3B1Y.md (qty 46; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-YE-HCDW-4UYW.md (qty 45; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-T8-2W2X-INOK.md (qty 58; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-GG-0DC1-SKHG.md (qty 47; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-18-116Z-1R77.md (qty 63; landed cost PENDING Freightos)
- approvals/pending/20260907-supply-chain-po-TB-PIST-120.md (qty 54; landed cost PENDING Freightos)
- departments/supply-chain/drafts/20260907-supplier-restock-anabtawi.md
