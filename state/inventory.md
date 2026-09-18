---
department: supply-chain
date: 2026-09-18
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily cover check: CA Inventory Health latest snap 2026-09-17; estimated OOS lost revenue about CAD 1106.00/day (vs CAD 1083.22 on 2026-09-17). Receiving: heroes fulfillable>0: FO-SE3J-T74M (15), 5G-ZW6Q-WOZG (13). Hero under floor (lead TBD=0 for status): AN-9938-NXOT, ASW-H50, EU-Z87B-ZRBZ, GG-0DC1-SKHG, T8-2W2X-INOK, YE-HCDW-4UYW. Hero watch: TB-PIST-120. Stranded 0; aged>180: 0C-45D7-6JUB (1); expiry within 90d: YE-HCDW-4UYW inbound 2026-11-23. Monday 20260914 hero PO proposals remain pending; stockout-risk request updated. Manufacturer FBA19NZ90PPZ still DELIVERED; READY_TO_SHIP FBA19NSL8M11 near-duplicate not double-counted. Fulfillable progress vs prior: 5G-ZW6Q-WOZG 14->13.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408` (ANABTAWI SWEETS CA); US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469` (ANABTAWI SWEETS US). Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30: if fulfillable>0 use last-30 calendar units÷30; if stockout, units sold on afn_fulfillable in-stock days ÷ those unique days when >0; else up to last 30 historical sale days (vel_denom). Prefer shipped order lines. cover_days=(fulfillable+inbound)÷velocity_30. cover_adjusted=cover_days (no seasonal multiplier).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-17.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-19 to 2026-09-18 job 44f64d20-080e-462c-ab6f-1816824a894e
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-20 to 2026-09-18 job 72dbf97f-4f08-4763-9418-1782be4360a9 (418 raw rows; 352 shipped used)
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job b196423b-b8ac-4e4f-affd-4c1ea0ef0d64 (17 raw rows; RECEIVING counted in full; DELIVERED preferred over IN_TRANSIT/READY_TO_SHIP near-duplicates)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job 0866eeda-dd3d-4b09-bd60-a6c50e213672 (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-19 to 2026-09-18 job 668bdebb-5874-4157-8128-89dc31dff1de
- DataDoe export Order Line Items US job 785451b9-260a-4ee0-a5c8-336fc3866391 (0 rows)
- DataDoe export FBA Inbound Shipments US snapshot job f5580d35-e385-4ab2-993d-ac8181e2f868

### Heroes (top 10 by 90-day CA revenue)
| rank | sku | rev_90_CAD | units_90 |
|---:|---|---:|---:|
| 1 | H8-PWJ0-3B1Y | 2111.36 | 64 |
| 2 | EU-Z87B-ZRBZ | 2015.64 | 36 |
| 3 | FO-SE3J-T74M | 1286.61 | 39 |
| 4 | 5G-ZW6Q-WOZG | 1154.65 | 35 |
| 5 | YE-HCDW-4UYW | 899.85 | 15 |
| 6 | ASW-H50 | 839.86 | 14 |
| 7 | GG-0DC1-SKHG | 659.78 | 22 |
| 8 | T8-2W2X-INOK | 429.90 | 10 |
| 9 | TB-PIST-120 | 389.70 | 30 |
| 10 | AN-9938-NXOT | 330.88 | 12 |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 3.8000 | 5 | 9.47 | 9.47 | 14 | TBD | 2026-08-23 | 55.99 | 3.8000 | 212.76 | critical |
| 2 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.6667 | 24 | 24.00 | 24.00 | 14 | TBD | on-or-before-2026-08-19 | 32.99 | 2.6667 | 87.97 | ok |
| 3 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 39.99 | 2.0000 | 79.98 | critical |
| 4 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.40 | 6.40 | 14 | TBD | 2026-08-20 | 59.99 | 1.2500 | 74.99 | critical |
| 5 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 2.5000 | 4 | 8.80 | 8.80 | 14 | TBD | 2026-08-22 | 29.99 | 2.5000 | 74.97 | critical |
| 6 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 21.99 | 2.5000 | 54.97 | critical |
| 7 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.2500 | 8 | 0.00 | 0.00 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.2500 | 53.74 | critical |
| 8 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.6667 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 27.99 | 1.6667 | 46.65 | critical |
| 9 | ca | AN-9938-NXOT | true | 0 | 0 | none | 1.7143 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 26.99 | 1.7143 | 46.27 | critical |
| 10 | ca | ASW-H50 | true | 0 | 0 | none | 0.7500 | 12 | 0.00 | 0.00 | 14 | TBD | 2026-08-31 | 59.99 | 0.7500 | 44.99 | critical |
| 11 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 42.99 | 1.0000 | 42.99 | critical |
| 12 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 39.99 | 1.0000 | 39.99 | critical |
| 13 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 34.99 | 1.0000 | 34.99 | critical |
| 14 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.6250 | 8 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 17.99 | 1.6250 | 29.23 | critical |
| 15 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 28.99 | 1.0000 | 28.99 | critical |
| 16 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 19.99 | 1.4286 | 28.56 | critical |
| 17 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 28.00 | 1.0000 | 28.00 | critical |
| 18 | ca | 18-116Z-1R77 | false | 0 | 0 | none | 1.0000 | 5 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-19 | 25.99 | 1.0000 | 25.99 | critical |
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
| ca | OA-26MX-IHV0 | 44 | 54 | receiving-now | 0.1667 | 588.00 | 588.00 | 2026-09-17 | 21.00 | ok |
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.1000 | 370.00 | 370.00 | 2026-09-17 | 19.99 | ok |
| ca | KP-MEL9-XYGW | 16 | 18 | delivered | 0.0000 |  |  | 2026-09-17 | 19.99 | ok |
| ca | FO-SE3J-T74M | 15 | 53 | delivered,receiving-now | 0.9333 | 72.86 | 72.86 | 2026-09-17 | 32.99 | ok |
| ca | 5G-ZW6Q-WOZG | 13 | 68 | delivered,receiving-now | 0.0667 | 1215.00 | 1215.00 | 2026-09-17 | 32.99 | ok |
| ca | 0C-45D7-6JUB | 1 | 0 | none | 0.0333 | 30.00 | 30.00 | 2026-09-17 | 59.99 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | H8-PWJ0-3B1Y | true | 64 | 24.00 | ok |
| ca | TB-PIST-120 | true | 30 | 15.00 | watch |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | OA-26MX-IHV0 | 44 | 0 | 0.0000 |  | ok | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 26-JITG-E4FU | 19 | 0 | 0.0000 |  | ok | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | KP-MEL9-XYGW | 16 | 0 | 0.0000 |  | ok | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | FO-SE3J-T74M | 15 | 0 | 0.0000 |  | ok | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 5G-ZW6Q-WOZG | 13 | 0 | 0.0000 |  | ok | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 0C-45D7-6JUB | 1 | 0 | 0.0000 |  | ok | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 09-AJOP-CS83 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 18-116Z-1R77 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 1S-ITGB-CZFR | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 3I-SHTN-9CKQ | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 9J-ASSK-BVKC | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | 9Z-KUHZ-FU2I | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | AN-9938-NXOT | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | BU-6GOS-GW5Q | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | C5-TXQU-Y67R | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | E3-DSPC-O2UN | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | EU-Z87B-ZRBZ | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | FX-M8MA-MMSA | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | GG-0DC1-SKHG | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | H8-PWJ0-3B1Y | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | KL-GDUL-HEA1 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | O3-V1B9-CH1H | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | RL-KMFR-SEGS | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | TB-PIST-120 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | VH-ZTOC-GW1Q | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | W3-UQRU-PGRR | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | Y4-Y8EE-VEOD | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |
| us | ZK-4NDS-MNA9 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-17 |

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
| before 2026-09-03 | 2026-09-04 | DELIVERED FBA19NZ90PPZ; READY_TO_SHIP FBA19NSL8M11 treated as near-duplicate | 5G-ZW6Q-WOZG 32; FO-SE3J-T74M 17; KP-MEL9-XYGW 18; ZK-4NDS-MNA9 18 | delivered at Amazon; fulfillable on snap 2026-09-17: 5G-ZW6Q-WOZG (13), FO-SE3J-T74M (15), KP-MEL9-XYGW (16), ZK-4NDS-MNA9 (0) | suppliers/anabtawi.md + DataDoe inbound + Inventory Health |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-17 |
Expiry within 90 days: YE-HCDW-4UYW inbound lot expiration 2026-11-23.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-17; Amazon business day closes 07:00 Asia/Jerusalem (Sep 18 snap may not be available yet at this run).
- suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD — status thresholds use lead TBD=0.
- products/ empty — heroes by 90-day CA revenue (shipped lines); #10 is AN-9938-NXOT.
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with DELIVERED > IN_TRANSIT > READY_TO_SHIP near-duplicate dedupe.
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover. US Inventory Health snap now lists multiple SKUs with afn_fulfillable matching CA levels (possible NA/shared visibility).
- Capacity/IPI unavailable.
- Fresh Monday PO proposals dated 20260914 remain pending; no new PO files written on this daily run.
- finance need-cash-check 20260914-0610 still unanswered at write time.
- Fulfillable progress vs 2026-09-17 known prior: 5G-ZW6Q-WOZG 14->13.

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-18 daily)
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
