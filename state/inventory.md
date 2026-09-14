---
department: supply-chain
date: 2026-09-14
run: scheduled
runtime: grok-bot
status: degraded
tools_failed: [freightos]
---
## Headline
Monday weekly: 12-week forecast refreshed from CA shipped orders 2026-06-16..2026-09-14; ROP recomputed with ASSUMED lead=21d/MOQ=1/case=1 (suppliers/anabtawi.md still TBD). Estimated OOS lost revenue about CAD 1363.95/day. Hero under floor (lead TBD=0 for status): AN-9938-NXOT, ASW-H50, EU-Z87B-ZRBZ, FO-SE3J-T74M, GG-0DC1-SKHG, T8-2W2X-INOK, YE-HCDW-4UYW. 10 hero PO proposals written as T2 files with product cash from COGS where known; Freightos landed cost blocked (MCP not connected) so status degraded. Manufacturer FBA19NZ90PPZ still DELIVERED; READY_TO_SHIP FBA19NSL8M11 near-duplicate not double-counted.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408` (ANABTAWI SWEETS CA); US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469` (ANABTAWI SWEETS US). Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30: if fulfillable>0 use last-30 calendar units÷30; if stockout, units sold on afn_fulfillable in-stock days ÷ those unique days when >0; else up to last 30 historical sale days (vel_denom). Prefer shipped order lines. cover_days=(fulfillable+inbound)÷velocity_30. cover_adjusted=cover_days (no seasonal multiplier).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-13.
PO sizing ASSUMED (labeled in proposals): lead 21d, review 7d, buffer 14d, MOQ 1, case pack 1 — replace when suppliers/anabtawi.md is filled.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-15 to 2026-09-14 job 0f39fcb5-61cd-40e8-9452-c68958898e66
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-16 to 2026-09-14 job 5a4823aa-7eff-44f4-88fb-2ef4b55f4916 (432 raw rows; 367 shipped used)
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job b7db61a9-0d3e-4553-868f-3863212edc30 (17 raw rows; RECEIVING counted in full; DELIVERED preferred over IN_TRANSIT/READY_TO_SHIP near-duplicates)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job 60c437b9-2f07-4ce4-9408-03357061c7a2 (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-15 to 2026-09-14 job 7c9b67f1-ba19-4bf8-b3fe-d2041864bde2
- DataDoe export Order Line Items US job 44038378-90ec-4864-8908-6000aaf8ae5d (0 rows)
- DataDoe export FBA Inbound Shipments US snapshot job 148e82de-d9ec-4888-a610-d2c18f4650fb

### Heroes (top 10 by 90-day CA revenue)
| rank | sku | rev_90_CAD | units_90 |
|---:|---|---:|---:|
| 1 | H8-PWJ0-3B1Y | 2144.35 | 65 |
| 2 | EU-Z87B-ZRBZ | 2015.64 | 36 |
| 3 | FO-SE3J-T74M | 1220.63 | 37 |
| 4 | 5G-ZW6Q-WOZG | 1088.67 | 33 |
| 5 | YE-HCDW-4UYW | 899.85 | 15 |
| 6 | ASW-H50 | 839.86 | 14 |
| 7 | GG-0DC1-SKHG | 659.78 | 22 |
| 8 | T8-2W2X-INOK | 607.86 | 14 |
| 9 | TB-PIST-120 | 389.70 | 30 |
| 10 | AN-9938-NXOT | 330.88 | 12 |

### 12-week forecast (heroes) — weekly units
Method: mean of last up to 8 ISO weeks of CA shipped units; forward 12 weeks = flat mean (playbooks/ has only us-launch.md; no CA seasonality multipliers; no launches in state/calendar.md).
| sku | avg_weekly | fwd_weekly_x12 | recent_hist (week:units) |
|---|---:|---|---|
| H8-PWJ0-3B1Y | 7.25 | 7.25 × 12 | 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0, 2026-W37:0.0 |
| EU-Z87B-ZRBZ | 4.38 | 4.38 × 12 | 2026-W34:24.0, 2026-W35:2.0, 2026-W36:0.0, 2026-W37:0.0 |
| FO-SE3J-T74M | 4.62 | 4.62 × 12 | 2026-W34:28.0, 2026-W35:1.0, 2026-W36:0.0, 2026-W37:0.0 |
| 5G-ZW6Q-WOZG | 4.12 | 4.12 × 12 | 2026-W34:3.0, 2026-W35:0.0, 2026-W36:0.0, 2026-W37:0.0 |
| YE-HCDW-4UYW | 0.88 | 0.88 × 12 | 2026-W34:1.0, 2026-W35:0.0, 2026-W36:0.0, 2026-W37:0.0 |
| ASW-H50 | 1.75 | 1.75 × 12 | 2026-W34:1.0, 2026-W35:12.0, 2026-W36:1.0, 2026-W37:0.0 |
| GG-0DC1-SKHG | 2.62 | 2.62 × 12 | 2026-W34:13.0, 2026-W35:1.0, 2026-W36:0.0, 2026-W37:0.0 |
| T8-2W2X-INOK | 0.00 | 0.00 × 12 | 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0, 2026-W37:0.0 |
| TB-PIST-120 | 3.75 | 3.75 × 12 | 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0, 2026-W37:0.0 |
| AN-9938-NXOT | 0.00 | 0.00 × 12 | 2026-W34:0.0, 2026-W35:0.0, 2026-W36:0.0, 2026-W37:0.0 |

### Reorder points (ASSUMED lead 21d + review 7d)
| sku | hero | velocity_30 | ROP_units | target_units (ROP+buffer14) | fulfillable | inbound | po_qty_assumed | status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| FO-SE3J-T74M | true | 4.4000 | 123.2 | 184.8 | 0 | 53 | 132 | critical |
| EU-Z87B-ZRBZ | true | 3.6667 | 102.7 | 154.0 | 0 | 36 | 118 | critical |
| AN-9938-NXOT | true | 1.7143 | 48.0 | 72.0 | 0 | 0 | 72 | critical |
| GG-0DC1-SKHG | true | 2.0000 | 56.0 | 84.0 | 0 | 22 | 62 | critical |
| T8-2W2X-INOK | true | 1.4000 | 39.2 | 58.8 | 0 | 0 | 59 | critical |
| TB-PIST-120 | true | 2.0000 | 56.0 | 84.0 | 0 | 30 | 54 | watch |
| 5G-ZW6Q-WOZG | true | 2.7500 | 77.0 | 115.5 | 0 | 68 | 48 | ok |
| H8-PWJ0-3B1Y | true | 2.6000 | 72.8 | 109.2 | 0 | 64 | 46 | ok |
| YE-HCDW-4UYW | true | 1.2500 | 35.0 | 52.5 | 0 | 8 | 45 | critical |
| ASW-H50 | true | 0.7143 | 20.0 | 30.0 | 0 | 0 | 30 | critical |
| KL-GDUL-HEA1 | false | 2.5000 | 70.0 | 105.0 | 0 | 0 | 105 | critical |
| C5-TXQU-Y67R | false | 2.0000 | 56.0 | 84.0 | 0 | 0 | 84 | critical |
| W3-UQRU-PGRR | false | 2.0000 | 56.0 | 84.0 | 0 | 0 | 84 | critical |
| BU-6GOS-GW5Q | false | 1.6250 | 45.5 | 68.2 | 0 | 0 | 69 | critical |
| 3I-SHTN-9CKQ | false | 1.4286 | 40.0 | 60.0 | 0 | 0 | 60 | critical |
| 18-116Z-1R77 | false | 1.3333 | 37.3 | 56.0 | 0 | 0 | 56 | critical |
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
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 3.6667 | 6 | 9.82 | 9.82 | 14 | TBD | 2026-08-23 | 55.99 | 3.6667 | 205.30 | critical |
| 2 | ca | FO-SE3J-T74M | true | 0 | 53 | delivered,receiving-now | 4.4000 | 5 | 12.05 | 12.05 | 14 | TBD | 2026-08-22 | 32.99 | 4.4000 | 145.16 | critical |
| 3 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | delivered,receiving-now | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | on-or-before-2026-08-15 | 32.99 | 2.7500 | 90.72 | ok |
| 4 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.6000 | 25 | 24.62 | 24.62 | 14 | TBD | on-or-before-2026-08-15 | 32.99 | 2.6000 | 85.77 | ok |
| 5 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 39.99 | 2.0000 | 79.98 | critical |
| 6 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.40 | 6.40 | 14 | TBD | 2026-08-20 | 59.99 | 1.2500 | 74.99 | critical |
| 7 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.4000 | 10 | 0.00 | 0.00 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.4000 | 60.19 | critical |
| 8 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 2.0000 | 5 | 11.00 | 11.00 | 14 | TBD | 2026-08-22 | 29.99 | 2.0000 | 59.98 | critical |
| 9 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 2.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 27.99 | 2.0000 | 55.98 | critical |
| 10 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 21.99 | 2.5000 | 54.97 | critical |
| 11 | ca | AN-9938-NXOT | true | 0 | 0 | none | 1.7143 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 26.99 | 1.7143 | 46.27 | critical |
| 12 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 42.99 | 1.0000 | 42.99 | critical |
| 13 | ca | ASW-H50 | true | 0 | 0 | none | 0.7143 | 14 | 0.00 | 0.00 | 14 | TBD | 2026-09-01 | 59.99 | 0.7143 | 42.85 | critical |
| 14 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 39.99 | 1.0000 | 39.99 | critical |
| 15 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 34.99 | 1.0000 | 34.99 | critical |
| 16 | ca | 18-116Z-1R77 | false | 0 | 0 | none | 1.3333 | 9 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 25.99 | 1.3333 | 34.65 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.6250 | 8 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 17.99 | 1.6250 | 29.23 | critical |
| 18 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 28.99 | 1.0000 | 28.99 | critical |
| 19 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 19.99 | 1.4286 | 28.56 | critical |
| 20 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 28.00 | 1.0000 | 28.00 | critical |
| 21 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.0000 | 15 | 15.00 | 15.00 | 14 | TBD | on-or-before-2026-08-15 | 12.99 | 2.0000 | 25.98 | watch |
| 22 | ca | KP-MEL9-XYGW | false | 0 | 18 | delivered | 1.2222 | 9 | 14.73 | 14.73 | 14 | TBD | on-or-before-2026-08-15 | 19.99 | 1.2222 | 24.43 | watch |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-15 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-15 | 0.00 | 0.0000 | 0.00 | critical |
| 26 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-15 | 0.00 | 0.0000 | 0.00 | critical |
| 27 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-15 | 0.00 | 0.0000 | 0.00 | critical |
| 28 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | delivered | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-15 | 23.99 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | 0 | none | 0.0333 | 30.00 | 30.00 | 2026-09-13 | 59.99 | ok |
| ca | OA-26MX-IHV0 | 43 | 54 | receiving-now | 0.2000 | 485.00 | 485.00 | 2026-09-13 | 21.00 | ok |
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.1000 | 370.00 | 370.00 | 2026-09-13 | 19.99 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |
| ca | H8-PWJ0-3B1Y | true | 64 | 24.62 | ok |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-13 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-13 |

### Inbound ETAs (CA FBA shipments export, deduped)
| sku | qty | status | confirmation | window/ETA |
|---|---:|---|---|---|
| 26-JITG-E4FU | 18 | RECEIVING:18 | FBA19H427DS7 | receiving-now |
| 5G-ZW6Q-WOZG | 68 | RECEIVING:36;DELIVERED:32 | FBA19H427DS7,FBA19NZ90PPZ | delivered,receiving-now |
| EU-Z87B-ZRBZ | 36 | RECEIVING:36 | FBA19H427DS7 | receiving-now |
| FO-SE3J-T74M | 53 | RECEIVING:36;DELIVERED:17 | FBA19H427DS7,FBA19NZ90PPZ | delivered,receiving-now |
| GG-0DC1-SKHG | 22 | RECEIVING:22 | FBA19H427DS7 | receiving-now |
| H8-PWJ0-3B1Y | 64 | RECEIVING:64 | FBA19H427DS7 | receiving-now |
| KP-MEL9-XYGW | 18 | DELIVERED:18 | FBA19NZ90PPZ | delivered |
| OA-26MX-IHV0 | 54 | RECEIVING:54 | FBA19H427DS7 | receiving-now |
| TB-PIST-120 | 30 | RECEIVING:30 | FBA19JXFX4KT | receiving-now |
| YE-HCDW-4UYW | 8 | RECEIVING:8 | FBA19H427DS7 | receiving-now |
| ZK-4NDS-MNA9 | 18 | DELIVERED:18 | FBA19NZ90PPZ | delivered |

### Manufacturer open order (not yet fully received into fulfillable)
| placed | ships | ETA at FBA | lines | status | source |
|---|---|---|---|---|---|
| before 2026-09-03 | 2026-09-04 | DELIVERED FBA19NZ90PPZ; READY_TO_SHIP FBA19NSL8M11 treated as near-duplicate | 5G-ZW6Q-WOZG 32; FO-SE3J-T74M 17; KP-MEL9-XYGW 18; ZK-4NDS-MNA9 18 | delivered at Amazon, not yet fulfillable on Inventory Health snap | suppliers/anabtawi.md + DataDoe inbound |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-13 |
Expiry within 90 days: YE-HCDW-4UYW inbound lot expiration 2026-11-23.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-13; Amazon business day closes 07:00 Asia/Jerusalem.
- Freightos MCP is configured in departments/supply-chain/.mcp.json but is not connected on this grok-bot runtime — landed cost cannot be computed; PO proposals include product cash (COGS×qty) only and mark landed cost PENDING.
- suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD — PO quantities use ASSUMED lead 21d, MOQ 1, case pack 1.
- state/cash.md has never been run; need-cash-check sent to finance, unanswered at write time.
- products/ empty — heroes by 90-day CA revenue (shipped lines); this week #10 is AN-9938-NXOT (18-116Z-1R77 drops to #11 on current 90d window).
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with DELIVERED > IN_TRANSIT > READY_TO_SHIP near-duplicate dedupe.
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover.
- Capacity/IPI unavailable.
- Prior Monday 20260907 pending PO files are expired (>48h); left in place; fresh 20260914 proposals written.

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-14 weekly)
- new 20260914-0610-supply-chain-need-cash-check → finance
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md
- prior unanswered: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md

## Proposals written
- approvals/pending/20260914-supply-chain-po-EU-Z87B-ZRBZ.md (qty 118; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-FO-SE3J-T74M.md (qty 132; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-5G-ZW6Q-WOZG.md (qty 48; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-H8-PWJ0-3B1Y.md (qty 46; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-YE-HCDW-4UYW.md (qty 45; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-T8-2W2X-INOK.md (qty 59; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-GG-0DC1-SKHG.md (qty 62; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-AN-9938-NXOT.md (qty 72; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-ASW-H50.md (qty 30; landed cost PENDING Freightos)
- approvals/pending/20260914-supply-chain-po-TB-PIST-120.md (qty 54; landed cost PENDING Freightos)
- departments/supply-chain/drafts/20260914-supplier-restock-anabtawi.md
