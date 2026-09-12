---
department: supply-chain
date: 2026-09-12
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily cover check: CA Inventory Health latest snap 2026-09-11; estimated OOS lost revenue about CAD 1368.28/day. Hero under floor (lead TBD=0 for status): EU-Z87B-ZRBZ, FO-SE3J-T74M, YE-HCDW-4UYW, T8-2W2X-INOK, GG-0DC1-SKHG, ASW-H50, 18-116Z-1R77. Stranded 0; aged>180: 0C-45D7-6JUB (1); expiry within 90d: YE-HCDW-4UYW inbound 2026-11-23. Monday hero PO proposals remain pending; stockout-risk request updated. Manufacturer FBA19NZ90PPZ still DELIVERED; READY_TO_SHIP FBA19NSL8M11 near-duplicate not double-counted.

## Data
Seller: `5692b95f-f3f0-4063-9c1c-40177c54f408` (ANABTAWI SWEETS CA); US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469` (ANABTAWI SWEETS US). Marketplace: ca (primary). Floor: 14 days. Lead time: TBD (`suppliers/anabtawi.md`). Seasonal buffer not active (Ramadan ~2027-02-18). Currency: CAD for CA.
velocity_30: if fulfillable>0 use last-30 calendar units÷30; if stockout, units sold on afn_fulfillable in-stock days ÷ those unique days when >0; else up to last 30 historical sale days (vel_denom). cover_days=(fulfillable+inbound)÷velocity_30. cover_adjusted=cover_days (no seasonal multiplier).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-11.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-13 to 2026-09-12 job 04d65ca4-90d3-4786-b479-259e4b25886e
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-14 to 2026-09-12 job 5d453f8f-2de2-41c4-b026-08ca889858ab (434 raw rows)
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job 47fb54b9-88b4-4577-9bfc-36d3077f0a10 (17 raw rows; RECEIVING counted in full; DELIVERED preferred over IN_TRANSIT/READY_TO_SHIP near-duplicates)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job b0dc3bd9-a76e-4ea6-9ccf-49393aef55a4 (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-13 to 2026-09-12 job 4b9a57ec-c24d-4af1-81c9-bb1afb251998
- DataDoe export Order Line Items US job 17683989-d16f-4f32-9341-529b50ffd0be (0 rows)
- DataDoe export FBA Inbound Shipments US snapshot job 7a1f7ee7-1818-44c0-8286-ab27c45a1bc3

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
| 9 | 18-116Z-1R77 | 389.85 | 15 |
| 10 | TB-PIST-120 | 389.70 | 30 |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 3.6667 | 6 | 9.82 | 9.82 | 14 | TBD | 2026-08-23 | 55.99 | 3.6667 | 205.30 | critical |
| 2 | ca | FO-SE3J-T74M | true | 0 | 53 | delivered,receiving-now | 4.4000 | 5 | 12.05 | 12.05 | 14 | TBD | 2026-08-22 | 32.99 | 4.4000 | 145.16 | critical |
| 3 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | delivered,receiving-now | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | 2026-08-13 | 32.99 | 2.7500 | 90.72 | ok |
| 4 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.6000 | 25 | 24.62 | 24.62 | 14 | TBD | on-or-before-2026-08-11 | 32.99 | 2.6000 | 85.77 | ok |
| 5 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 39.99 | 2.0000 | 79.98 | critical |
| 6 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.40 | 6.40 | 14 | TBD | 2026-08-20 | 59.99 | 1.2500 | 74.99 | critical |
| 7 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.4000 | 10 | 0.00 | 0.00 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.4000 | 60.19 | critical |
| 8 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 2.0000 | 5 | 11.00 | 11.00 | 14 | TBD | 2026-08-22 | 29.99 | 2.0000 | 59.98 | critical |
| 9 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 2.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 27.99 | 2.0000 | 55.98 | critical |
| 10 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 21.99 | 2.5000 | 54.97 | critical |
| 11 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.7143 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 26.99 | 1.7143 | 46.27 | critical |
| 12 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 42.99 | 1.0000 | 42.99 | critical |
| 13 | ca | ASW-H50 | true | 0 | 0 | none | 0.7143 | 14 | 0.00 | 0.00 | 14 | TBD | 2026-09-01 | 59.99 | 0.7143 | 42.85 | critical |
| 14 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 39.99 | 1.0000 | 39.99 | critical |
| 15 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.5000 | 10 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 25.99 | 1.5000 | 38.98 | critical |
| 16 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 34.99 | 1.0000 | 34.99 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.6250 | 8 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 17.99 | 1.6250 | 29.23 | critical |
| 18 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 28.99 | 1.0000 | 28.99 | critical |
| 19 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 19.99 | 1.4286 | 28.56 | critical |
| 20 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 28.00 | 1.0000 | 28.00 | critical |
| 21 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.0000 | 15 | 15.00 | 15.00 | 14 | TBD | 2026-08-13 | 12.99 | 2.0000 | 25.98 | watch |
| 22 | ca | KP-MEL9-XYGW | false | 0 | 18 | delivered | 1.2222 | 9 | 14.73 | 14.73 | 14 | TBD | on-or-before-2026-08-11 | 19.99 | 1.2222 | 24.43 | watch |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-11 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-11 | 0.00 | 0.0000 | 0.00 | critical |
| 26 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-11 | 0.00 | 0.0000 | 0.00 | critical |
| 27 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-11 | 0.00 | 0.0000 | 0.00 | critical |
| 28 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | delivered | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-11 | 23.99 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | OA-26MX-IHV0 | 44 | 54 | receiving-now | 0.2000 | 490.00 | 490.00 | 2026-09-11 | 21.00 | ok |
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.1000 | 370.00 | 370.00 | 2026-09-11 | 19.99 | ok |
| ca | 0C-45D7-6JUB | 1 | 0 | none | 0.0333 | 30.00 | 30.00 | 2026-09-11 | 59.99 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |
| ca | H8-PWJ0-3B1Y | true | 64 | 24.62 | ok |
| ca | TB-PIST-120 | true | 30 | 15.00 | watch |
| ca | KP-MEL9-XYGW | false | 18 | 14.73 | watch |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-11 |
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-11 |

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
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-11 |
Expiry within 90 days: YE-HCDW-4UYW inbound lot expiration 2026-11-23.

## Exceptions
- Inventory Health latest date in export window is 2026-09-11; Amazon business day closes 07:00 Asia/Jerusalem.
- suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD.
- products/ empty — heroes by 90-day CA revenue.
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with DELIVERED > IN_TRANSIT > READY_TO_SHIP near-duplicate dedupe.
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover.
- Capacity/IPI unavailable.
- Monday weekly forecast/ROP/PO proposals already filed 2026-09-07; daily run does not rewrite them.
- OOS velocity: afn_fulfillable in-stock days only (ignore available-only early rows); units sold on those days ÷ days; if none, up to last 30 historical sale days.

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-12 daily)
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md
- prior unanswered: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md (from Monday weekly)

## Proposals written
- (none new this daily run; Monday pending files retained)
- approvals/pending/20260907-supply-chain-po-18-116Z-1R77.md
- approvals/pending/20260907-supply-chain-po-5G-ZW6Q-WOZG.md
- approvals/pending/20260907-supply-chain-po-ASW-H50.md
- approvals/pending/20260907-supply-chain-po-EU-Z87B-ZRBZ.md
- approvals/pending/20260907-supply-chain-po-FO-SE3J-T74M.md
- approvals/pending/20260907-supply-chain-po-GG-0DC1-SKHG.md
- approvals/pending/20260907-supply-chain-po-H8-PWJ0-3B1Y.md
- approvals/pending/20260907-supply-chain-po-T8-2W2X-INOK.md
- approvals/pending/20260907-supply-chain-po-TB-PIST-120.md
- approvals/pending/20260907-supply-chain-po-YE-HCDW-4UYW.md
