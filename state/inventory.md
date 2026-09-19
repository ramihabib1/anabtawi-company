---
department: supply-chain
date: 2026-09-19
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily cover check: CA Inventory Health latest snap 2026-09-18; estimated OOS lost revenue about CAD 1125.90/day (vs CAD 1106.00 on 2026-09-18). Receiving: heroes fulfillable>0: FO-SE3J-T74M (14), 5G-ZW6Q-WOZG (13), 0C-45D7-6JUB (1). Hero under floor (lead TBD=0 for status): ASW-H50, EU-Z87B-ZRBZ, GG-0DC1-SKHG, T8-2W2X-INOK, YE-HCDW-4UYW. Hero watch: TB-PIST-120. Stranded 0; aged>180: 0C-45D7-6JUB (1); expiry within 90d: YE-HCDW-4UYW inbound 2026-11-23. Monday 20260914 hero PO proposals remain pending; stockout-risk request updated. Manufacturer FBA19NZ90PPZ still DELIVERED; READY_TO_SHIP FBA19NSL8M11 near-duplicate not double-counted. Fulfillable progress vs prior: FO-SE3J-T74M 15->14.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408` (ANABTAWI SWEETS CA); US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469` (ANABTAWI SWEETS US). Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30: if fulfillable>0 use last-30 calendar units÷30; if stockout, units sold on afn_fulfillable in-stock days ÷ those unique days when >0; else up to last 30 historical sale days (vel_denom). Prefer shipped order lines. cover_days=(fulfillable+inbound)÷velocity_30. cover_adjusted=cover_days (no seasonal multiplier).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-18.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-20 to 2026-09-19 job 74c3c324-e596-4667-b73c-73be402d6852
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-21 to 2026-09-19 job 1c436568-8b4d-4968-aa33-e2b510954d6f (414 raw rows; 349 shipped used)
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job 5dfce0a9-e145-4b59-8346-035bb9e3340c (17 raw rows; RECEIVING counted in full; DELIVERED preferred over IN_TRANSIT/READY_TO_SHIP near-duplicates)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job a0645a88-cb7d-4f03-824d-159ff654e60d (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-20 to 2026-09-19 job b098b780-574d-4dc5-9999-57285632256f
- DataDoe export Order Line Items US job 030aad84-9d7a-4e1a-94b7-423850f2e5f6 (0 rows)
- DataDoe export FBA Inbound Shipments US snapshot job 4688b781-3f8d-4617-8d5e-6df709e64d2b

### Heroes (top 10 by 90-day CA revenue)
| rank | sku | rev_90_CAD | units_90 |
|---:|---|---:|---:|
| 1 | H8-PWJ0-3B1Y | 2078.37 | 63 |
| 2 | EU-Z87B-ZRBZ | 2015.64 | 36 |
| 3 | FO-SE3J-T74M | 1286.61 | 39 |
| 4 | 5G-ZW6Q-WOZG | 1187.64 | 36 |
| 5 | YE-HCDW-4UYW | 899.85 | 15 |
| 6 | ASW-H50 | 839.86 | 14 |
| 7 | GG-0DC1-SKHG | 659.78 | 22 |
| 8 | T8-2W2X-INOK | 429.90 | 10 |
| 9 | TB-PIST-120 | 389.70 | 30 |
| 10 | 0C-45D7-6JUB | 299.95 | 5 |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 4.2500 | 4 | 8.47 | 8.47 | 14 | TBD | 2026-08-23 | 55.99 | 4.2500 | 237.96 | critical |
| 2 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.7391 | 23 | 23.37 | 23.37 | 14 | TBD | on-or-before-2026-08-19 | 32.99 | 2.7391 | 90.36 | ok |
| 3 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 39.99 | 2.0000 | 79.98 | critical |
| 4 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.40 | 6.40 | 14 | TBD | 2026-08-20 | 59.99 | 1.2500 | 74.99 | critical |
| 5 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 2.0000 | 3 | 11.00 | 11.00 | 14 | TBD | 2026-08-22 | 29.99 | 2.0000 | 59.98 | critical |
| 6 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 21.99 | 2.5000 | 54.97 | critical |
| 7 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.2500 | 8 | 0.00 | 0.00 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.2500 | 53.74 | critical |
| 8 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.8333 | 6 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 26.99 | 1.8333 | 49.48 | critical |
| 9 | ca | ASW-H50 | true | 0 | 0 | none | 0.8182 | 11 | 0.00 | 0.00 | 14 | TBD | 2026-08-31 | 59.99 | 0.8182 | 49.08 | critical |
| 10 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.6667 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 27.99 | 1.6667 | 46.65 | critical |
| 11 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 42.99 | 1.0000 | 42.99 | critical |
| 12 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 39.99 | 1.0000 | 39.99 | critical |
| 13 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 34.99 | 1.0000 | 34.99 | critical |
| 14 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.6250 | 8 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 17.99 | 1.6250 | 29.23 | critical |
| 15 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 28.99 | 1.0000 | 28.99 | critical |
| 16 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 19.99 | 1.4286 | 28.56 | critical |
| 17 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 28.00 | 1.0000 | 28.00 | critical |
| 18 | ca | 18-116Z-1R77 | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 25.99 | 1.0000 | 25.99 | critical |
| 19 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.0000 | 15 | 15.00 | 15.00 | 14 | TBD | on-or-before-2026-08-19 | 12.99 | 2.0000 | 25.98 | watch |
| 20 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 21.99 | 1.0000 | 21.99 | critical |
| 21 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 21.99 | 1.0000 | 21.99 | critical |
| 22 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-19 | 0.00 | 0.0000 | 0.00 | critical |
| 23 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-19 | 0.00 | 0.0000 | 0.00 | critical |
| 24 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-19 | 0.00 | 0.0000 | 0.00 | critical |
| 25 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | delivered | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-19 | 23.99 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | OA-26MX-IHV0 | 44 | 54 | receiving-now | 0.1667 | 588.00 | 588.00 | 2026-09-18 | 21.00 | ok |
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.1000 | 370.00 | 370.00 | 2026-09-18 | 19.99 | ok |
| ca | KP-MEL9-XYGW | 16 | 18 | delivered | 0.0000 |  |  | 2026-09-18 | 19.99 | ok |
| ca | FO-SE3J-T74M | 14 | 53 | delivered,receiving-now | 0.8000 | 83.75 | 83.75 | 2026-09-18 | 32.99 | ok |
| ca | 5G-ZW6Q-WOZG | 13 | 68 | delivered,receiving-now | 0.1000 | 810.00 | 810.00 | 2026-09-18 | 32.99 | ok |
| ca | 0C-45D7-6JUB | 1 | 0 | none | 0.0333 | 30.00 | 30.00 | 2026-09-18 | 59.99 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | H8-PWJ0-3B1Y | true | 64 | 23.37 | ok |
| ca | TB-PIST-120 | true | 30 | 15.00 | watch |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-18 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-18 |

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
| before 2026-09-03 | 2026-09-04 | DELIVERED FBA19NZ90PPZ; READY_TO_SHIP FBA19NSL8M11 treated as near-duplicate | 5G-ZW6Q-WOZG 32; FO-SE3J-T74M 17; KP-MEL9-XYGW 18; ZK-4NDS-MNA9 18 | delivered at Amazon; fulfillable on snap 2026-09-18: 5G-ZW6Q-WOZG (13), FO-SE3J-T74M (14), KP-MEL9-XYGW (16), ZK-4NDS-MNA9 (0) | suppliers/anabtawi.md + DataDoe inbound + Inventory Health |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-18 |
Expiry within 90 days: YE-HCDW-4UYW inbound lot expiration 2026-11-23.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-18; Amazon business day closes 07:00 Asia/Jerusalem (Sep 19 snap may not be available yet at this run).
- suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD — status thresholds use lead TBD=0.
- products/ empty — heroes by 90-day CA revenue (shipped lines); #10 is 0C-45D7-6JUB (AN-9938-NXOT dropped out of top 10).
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with DELIVERED > IN_TRANSIT > READY_TO_SHIP near-duplicate dedupe.
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover. US Inventory Health snap 2026-09-18 has only 2 SKUs (ASW-H50, YE-HCDW-4UYW); prior snap 2026-09-17 had 30 SKUs — treat 2026-09-18 US snap as incomplete.
- Capacity/IPI unavailable.
- Fresh Monday PO proposals dated 20260914 remain pending; no new PO files written on this daily run.
- finance need-cash-check 20260914-0610 still unanswered at write time.
- Fulfillable progress vs 2026-09-18 prior run known levels: FO-SE3J-T74M 15->14.

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-19 daily)
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md
- prior unanswered: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md
- prior unanswered: requests/finance/inbox/20260914-0610-supply-chain-need-cash-check.md

## Proposals written
- none (daily cover check; Monday 20260914 hero PO proposals already pending)
- still pending from Monday: approvals/pending/20260914-supply-chain-po-EU-Z87B-ZRBZ.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-FO-SE3J-T74M.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-5G-ZW6Q-WOZG.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-H8-PWJ0-3B1Y.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-YE-HCDW-4UYW.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-T8-2W2X-INOK.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-GG-0DC1-SKHG.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-AN-9938-NXOT.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-ASW-H50.md
- still pending from Monday: approvals/pending/20260914-supply-chain-po-TB-PIST-120.md
