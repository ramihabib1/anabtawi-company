---
department: supply-chain
date: 2026-09-10
run: scheduled
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
Daily cover check: CA Inventory Health latest snap 2026-09-09; estimated OOS lost revenue about CAD 1314.02/day. Hero under floor (lead TBD=0 for status): 18-116Z-1R77, ASW-H50, GG-0DC1-SKHG, T8-2W2X-INOK, YE-HCDW-4UYW. Stranded 0; aged>180: 0C-45D7-6JUB (1); expiry within 90d: YE-HCDW-4UYW inbound 2026-11-23. Monday hero PO proposals remain pending; stockout-risk request updated. Manufacturer IN_TRANSIT FBA19NZ90PPZ still open; READY_TO_SHIP FBA19NSL8M11 near-duplicate not double-counted.

## Data
Sellers: CA `5692b95f-f3f0-4063-9c1c-40177c54f408 (ANABTAWI SWEETS CA)`; US `822ebf46-c2bc-4350-86d3-dcf1bc8d5469 (ANABTAWI SWEETS US)`. Floor: 14 days. Lead time: TBD (suppliers/anabtawi.md). Seasonal buffer not active (Ramadan ~2027-02-08). Currency: CAD for CA.
velocity_30: if fulfillable>0 use last-30 calendar units÷30; if stockout in window use units÷days-in-stock from Inventory Health history when >0, else up to last 30 historical sale days (vel_denom). cover_days=(fulfillable+inbound)÷velocity_30. cover_adjusted=cover_days (no seasonal multiplier).
Heroes = top 10 by 90-day CA order revenue (products/ empty). Inventory Health latest snapshot date in export: 2026-09-09.

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-31 to 2026-09-10 job d4cb1b9e-631d-45ad-a9e4-49fb03ad13b9
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-12 to 2026-09-10 job 4722be6f-f5c8-4783-a5cc-a0c8d4846fcc (440 raw rows)
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job 2e5c1fca-6a92-423f-a048-92775ee85c4c (17 raw rows; RECEIVING counted in full; IN_TRANSIT vs READY_TO_SHIP near-duplicate plans took IN_TRANSIT)
- DataDoe export FBA Stranded Inventory (amazon_fba_stranded_inventory / a4d08771c8) snapshot job 3e02beba-389e-40c1-9df8-5a7939a038bb (0 rows)
- DataDoe export FBA Inventory Health US (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-31 to 2026-09-10 job dd186e4f-0f9b-4093-b832-9265857dbe34
- DataDoe export Order Line Items US job 5f4fec25-6dfa-4c80-91c6-1943ccd6e006 (0 rows)
- DataDoe export FBA Inbound Shipments US snapshot job fca28718-a148-4cae-ac85-190abac79d0f

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
| 8 | T8-2W2X-INOK | 607.86 | 14 |
| 9 | 18-116Z-1R77 | 415.84 | 16 |
| 10 | TB-PIST-120 | 389.70 | 30 |

### Cover table (CA) — under floor / OOS / watch / risk / critical
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | cover_adjusted | floor | lead_time | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| 1 | ca | ASW-H50 | true | 0 | 0 | none | 2.3333 | 6 | 0.00 | 0.00 | 14 | TBD | 2026-09-01 | 59.99 | 2.3333 | 139.98 | critical |
| 2 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 2.1176 | 17 | 17.00 | 17.00 | 14 | TBD | on-or-before-2026-08-30 | 55.99 | 2.1176 | 118.57 | watch |
| 3 | ca | FO-SE3J-T74M | true | 0 | 53 | in-transit,receiving-now | 3.0833 | 12 | 17.19 | 17.19 | 14 | TBD | on-or-before-2026-08-30 | 32.99 | 3.0833 | 101.72 | watch |
| 4 | ca | 5G-ZW6Q-WOZG | true | 0 | 68 | in-transit,receiving-now | 2.7500 | 12 | 24.73 | 24.73 | 14 | TBD | on-or-before-2026-08-30 | 32.99 | 2.7500 | 90.72 | ok |
| 5 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.6000 | 25 | 24.62 | 24.62 | 14 | TBD | on-or-before-2026-08-30 | 32.99 | 2.6000 | 85.77 | ok |
| 6 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 39.99 | 2.0000 | 79.98 | critical |
| 7 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.40 | 6.40 | 14 | TBD | on-or-before-2026-08-30 | 59.99 | 1.2500 | 74.99 | critical |
| 8 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.4000 | 10 | 0.00 | 0.00 | 14 | TBD | unknown (no FBA inventory rows in export window) | 42.99 | 1.4000 | 60.19 | critical |
| 9 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 21.99 | 2.5000 | 54.97 | critical |
| 10 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 1.6429 | 14 | 13.39 | 13.39 | 14 | TBD | on-or-before-2026-08-30 | 29.99 | 1.6429 | 49.27 | critical |
| 11 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.6667 | 6 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 27.99 | 1.6667 | 46.65 | critical |
| 12 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.7143 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 26.99 | 1.7143 | 46.27 | critical |
| 13 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 42.99 | 1.0000 | 42.99 | critical |
| 14 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 39.99 | 1.0000 | 39.99 | critical |
| 15 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.4545 | 11 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 25.99 | 1.4545 | 37.80 | critical |
| 16 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 34.99 | 1.0000 | 34.99 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.6250 | 8 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 17.99 | 1.6250 | 29.23 | critical |
| 18 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 2 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 28.99 | 1.0000 | 28.99 | critical |
| 19 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 19.99 | 1.4286 | 28.56 | critical |
| 20 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 28.00 | 1.0000 | 28.00 | critical |
| 21 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.0000 | 15 | 15.00 | 15.00 | 14 | TBD | on-or-before-2026-08-30 | 12.99 | 2.0000 | 25.98 | watch |
| 22 | ca | KP-MEL9-XYGW | false | 0 | 18 | in-transit | 1.2222 | 9 | 14.73 | 14.73 | 14 | TBD | on-or-before-2026-08-30 | 19.99 | 1.2222 | 24.43 | watch |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.00 | 0.00 | 14 | TBD | on-or-before-2026-08-30 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |
| 26 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |
| 27 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 0.00 | 0.0000 | 0.00 | critical |
| 28 | ca | ZK-4NDS-MNA9 | false | 0 | 18 | in-transit | 0.0000 | 0 |  |  | 14 | TBD | on-or-before-2026-08-30 | 23.99 | 0.0000 | 0.00 | critical |

### Cover OK (CA fulfillable > 0 and status ok)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | cover_adjusted | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | 0 | none | 0.0333 | 30.00 | 30.00 | 2026-09-09 | 59.99 | ok |
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.1333 | 277.50 | 277.50 | 2026-09-09 | 19.99 | ok |
| ca | OA-26MX-IHV0 | 45 | 54 | receiving-now | 0.1667 | 594.00 | 594.00 | 2026-09-09 | 21.00 | ok |

### OOS fulfillable but inbound cover ≥ floor (still not sellable)
| marketplace | sku | hero | inbound_qty | cover_days | status |
|---|---|---|---:|---:|---|
| ca | 5G-ZW6Q-WOZG | true | 68 | 24.73 | ok |
| ca | H8-PWJ0-3B1Y | true | 64 | 24.62 | ok |

### US marketplace
| marketplace | sku | fulfillable | inbound_qty | velocity_30 | cover_days | status | note |
|---|---|---:|---:|---:|---:|---|---|
| us | ASW-H50 | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-09 |
| us | YE-HCDW-4UYW | 0 | 0 | 0.0000 |  | critical | US orders export 0 rows; US inbound export mirrors CA confirmations — not applied to US cover; snap 2026-09-09 |

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
| before 2026-09-03 | 2026-09-04 | IN_TRANSIT FBA19NZ90PPZ (updated 2026-09-05); READY_TO_SHIP FBA19NSL8M11 treated as near-duplicate | 5G-ZW6Q-WOZG 32; FO-SE3J-T74M 17; KP-MEL9-XYGW 18; ZK-4NDS-MNA9 18 | in transit | suppliers/anabtawi.md + DataDoe inbound |

### Capacity / IPI
Not available from the DataDoe sources used this run (no capacity/IPI columns in FBA Inventory Health / Inbound exports pulled).

### Aged inventory (>180 days) and expiry
| marketplace | sku | units_aged_over_180 | source |
|---|---|---:|---|
| ca | 0C-45D7-6JUB | 1 | Inventory Health inv_age_181+ buckets on snap 2026-09-09 |
Expiry within 90 days: YE-HCDW-4UYW inbound lot expiration 2026-11-23.
Stranded: FBA Stranded Inventory export returned 0 rows.

## Exceptions
- Inventory Health latest date in export window is 2026-09-09; Amazon business day closes 07:00 Asia/Jerusalem.
- suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD.
- products/ empty — heroes by 90-day CA revenue.
- Inventory Health inbound_* columns remain unreliable vs FBA Inbound Shipments; cover uses inbound shipments export with IN_TRANSIT vs READY_TO_SHIP near-duplicate dedupe.
- US: orders export 0 rows; inbound export returns CA confirmation IDs under US seller — not used for US cover.
- Capacity/IPI unavailable.
- Monday weekly forecast/ROP/PO proposals already filed 2026-09-07; daily run does not rewrite them.
- OOS velocity: when no days-in-stock in the last 30 Inventory Health snaps, use up to last 30 historical sale days (not sparse in-window sale days alone).

## Requests sent
- updated 20260905-0620-supply-chain-stockout-risk → advertising (## Update 2026-09-10 daily)
- prior unanswered: requests/advertising/inbox/20260903-1955-supply-chain-stockout-risk.md
- prior unanswered: requests/advertising/inbox/20260904-0625-supply-chain-stockout-risk.md
- prior unanswered: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md (from Monday weekly)

## Proposals written
- (none new this daily run; Monday pending files retained)
- approvals/pending/20260907-supply-chain-po-H8-PWJ0-3B1Y.md
- approvals/pending/20260907-supply-chain-po-EU-Z87B-ZRBZ.md
- approvals/pending/20260907-supply-chain-po-FO-SE3J-T74M.md
- approvals/pending/20260907-supply-chain-po-5G-ZW6Q-WOZG.md
- approvals/pending/20260907-supply-chain-po-YE-HCDW-4UYW.md
- approvals/pending/20260907-supply-chain-po-ASW-H50.md
- approvals/pending/20260907-supply-chain-po-GG-0DC1-SKHG.md
- approvals/pending/20260907-supply-chain-po-T8-2W2X-INOK.md
- approvals/pending/20260907-supply-chain-po-18-116Z-1R77.md
- approvals/pending/20260907-supply-chain-po-TB-PIST-120.md
