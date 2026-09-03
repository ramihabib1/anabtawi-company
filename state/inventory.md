---
department: supply-chain
date: 2026-09-03
run: assignment
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
CA cover check / stockout audit: 28 SKUs at fulfillable 0 and 29 SKUs with fulfillable=0 or cover under the 14-day floor; estimated lost revenue about CAD 1241.28/day while OOS. Manufacturer restock ships 2026-09-04 (suppliers/anabtawi.md; ETA at FBA TBD). Nine FBA inbound lines already RECEIVING at Amazon. No PO proposals this week per inbox 20260903-1700.

## Data
Seller: `5692b95f-f3f0-4063-9c1c-40177c54f408 (ANABTAWI SWEETS CA)`. Marketplace: ca. Floor: 14 days. Currency: CAD.
velocity_30 = units on last known in-stock days (orders + inventory health) ÷ those days; denom noted when not 30.
cover_days = (fulfillable + inbound in cover window) ÷ velocity_30. Inbound qty from FBA Inbound Shipments (RECEIVING); inventory-health inbound fields were 0.
Heroes = top 10 by 90-day order revenue (products/ empty). Price = last non-zero inventory your_price else last order unit price.
Orders export may be incomplete from 2026-09-01 (DataDoe incident).

### Export citations
- DataDoe export FBA Inventory Health (amazon_fba_inventory_health / 44fc5ba0ce) 2026-08-28 to 2026-09-03 job edab5677-b0a6-42eb-92c1-50c24bce368a
- DataDoe export Order Line Items (amazon_order_items_with_cogs / 89b27535d2) 2026-06-05 to 2026-09-03 job 1b412934-0932-46a9-92d5-90275f46b598
- DataDoe export FBA Inbound Shipments (amazon_fba_inbound_shipments / 8bc6f4bd09) snapshot job 0113c93d-458c-467f-983f-93e7e25329cd

### Heroes (top 10 by 90-day revenue)
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

### Stockout / under-floor audit (ranked by lost revenue/day)
| rank | marketplace | sku | hero | fulfillable | inbound_qty | inbound_eta | velocity_30 | vel_denom | cover_days | last_in_stock | price_CAD | lost_units_day | lost_rev_day_CAD | status |
|---:|---|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---|
| 1 | ca | EU-Z87B-ZRBZ | true | 0 | 36 | receiving-now | 2.2500 | 16 | 16.0 | on-or-before-2026-08-27 | 55.99 | 2.2500 | 125.98 | critical |
| 2 | ca | 5G-ZW6Q-WOZG | true | 0 | 36 | receiving-now | 2.7500 | 12 | 13.09 | on-or-before-2026-08-27 | 32.99 | 2.7500 | 90.72 | critical |
| 3 | ca | FO-SE3J-T74M | true | 0 | 36 | receiving-now | 2.6429 | 14 | 13.62 | on-or-before-2026-08-27 | 32.99 | 2.6429 | 87.19 | critical |
| 4 | ca | ASW-H50 | true | 0 | 0 | none | 1.4000 | 10 | 0.0 | 2026-09-01 | 59.99 | 1.4000 | 83.99 | critical |
| 5 | ca | C5-TXQU-Y67R | false | 0 | 0 | none | 2.0000 | 2 | 0.0 | on-or-before-2026-08-27 | 39.99 | 2.0000 | 79.98 | critical |
| 6 | ca | H8-PWJ0-3B1Y | true | 0 | 64 | receiving-now | 2.4074 | 27 | 26.58 | on-or-before-2026-08-27 | 32.99 | 2.4074 | 79.42 | critical |
| 7 | ca | YE-HCDW-4UYW | true | 0 | 8 | receiving-now | 1.2500 | 12 | 6.4 | on-or-before-2026-08-27 | 59.99 | 1.2500 | 74.99 | critical |
| 8 | ca | KL-GDUL-HEA1 | false | 0 | 0 | none | 2.5000 | 2 | 0.0 | on-or-before-2026-08-27 | 21.99 | 2.5000 | 54.97 | critical |
| 9 | ca | T8-2W2X-INOK | true | 0 | 0 | none | 1.2308 | 13 | 0.0 | unknown (no FBA inventory rows in export window) | 42.99 | 1.2308 | 52.91 | critical |
| 10 | ca | E3-DSPC-O2UN | false | 0 | 0 | none | 1.3333 | 3 | 0.0 | on-or-before-2026-08-27 | 34.99 | 1.3333 | 46.65 | critical |
| 11 | ca | GG-0DC1-SKHG | true | 0 | 22 | receiving-now | 1.5333 | 15 | 14.35 | on-or-before-2026-08-27 | 29.99 | 1.5333 | 45.98 | critical |
| 12 | ca | W3-UQRU-PGRR | false | 0 | 0 | none | 1.5714 | 7 | 0.0 | on-or-before-2026-08-27 | 27.99 | 1.5714 | 43.98 | critical |
| 13 | ca | 9Z-KUHZ-FU2I | false | 0 | 0 | none | 1.0000 | 2 | 0.0 | on-or-before-2026-08-27 | 42.99 | 1.0000 | 42.99 | critical |
| 14 | ca | AN-9938-NXOT | false | 0 | 0 | none | 1.5000 | 8 | 0.0 | on-or-before-2026-08-27 | 26.99 | 1.5000 | 40.48 | critical |
| 15 | ca | 1S-ITGB-CZFR | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | on-or-before-2026-08-27 | 39.99 | 1.0000 | 39.99 | critical |
| 16 | ca | 18-116Z-1R77 | true | 0 | 0 | none | 1.5333 | 15 | 0.0 | on-or-before-2026-08-27 | 25.99 | 1.5333 | 39.85 | critical |
| 17 | ca | BU-6GOS-GW5Q | false | 0 | 0 | none | 1.8571 | 7 | 0.0 | on-or-before-2026-08-27 | 17.99 | 1.8571 | 33.41 | critical |
| 18 | ca | 3I-SHTN-9CKQ | false | 0 | 0 | none | 1.4286 | 7 | 0.0 | on-or-before-2026-08-27 | 19.99 | 1.4286 | 28.56 | critical |
| 19 | ca | FX-M8MA-MMSA | false | 0 | 0 | none | 1.0000 | 1 | 0.0 | on-or-before-2026-08-27 | 28.00 | 1.0000 | 28.00 | critical |
| 20 | ca | TB-PIST-120 | true | 0 | 30 | receiving-now | 2.1429 | 14 | 14.0 | on-or-before-2026-08-27 | 12.99 | 2.1429 | 27.84 | critical |
| 21 | ca | Y4-Y8EE-VEOD | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | on-or-before-2026-08-27 | 24.99 | 1.0000 | 24.99 | critical |
| 22 | ca | KP-MEL9-XYGW | false | 0 | 0 | none | 1.2222 | 9 | 0.0 | on-or-before-2026-08-27 | 19.99 | 1.2222 | 24.43 | critical |
| 23 | ca | 09-AJOP-CS83 | false | 0 | 0 | none | 1.0000 | 4 | 0.0 | on-or-before-2026-08-27 | 21.99 | 1.0000 | 21.99 | critical |
| 24 | ca | O3-V1B9-CH1H | false | 0 | 0 | none | 1.0000 | 3 | 0.0 | on-or-before-2026-08-27 | 21.99 | 1.0000 | 21.99 | critical |
| 25 | ca | 0C-45D7-6JUB | false | 1 | 0 | none | 0.5000 | 10 | 2.0 | 2026-09-03 | 59.99 | 0.0000 | 0.00 | critical |
| 26 | ca | VH-ZTOC-GW1Q | false | 0 | 0 | none | 0.0000 | 0 |  | on-or-before-2026-08-27 | 49.99 | 0.0000 | 0.00 | critical |
| 27 | ca | ZK-4NDS-MNA9 | false | 0 | 0 | none | 0.0000 | 0 |  | on-or-before-2026-08-27 | 23.99 | 0.0000 | 0.00 | critical |
| 28 | ca | 9J-ASSK-BVKC | false | 0 | 0 | none | 0.0000 | 0 |  | on-or-before-2026-08-27 | 0.00 | 0.0000 | 0.00 | critical |
| 29 | ca | RL-KMFR-SEGS | false | 0 | 0 | none | 0.0000 | 0 |  | on-or-before-2026-08-27 | 18.99 | 0.0000 | 0.00 | critical |

### Cover OK (fulfillable > 0 and cover ≥ 14)
| marketplace | sku | fulfillable | inbound_qty | inbound_eta | velocity_30 | cover_days | last_in_stock | price_CAD | status |
|---|---|---:|---:|---|---:|---:|---|---:|---|
| ca | 26-JITG-E4FU | 19 | 18 | receiving-now | 0.7778 | 47.57 | 2026-09-03 | 19.99 | ok |
| ca | OA-26MX-IHV0 | 48 | 54 | receiving-now | 0.6000 | 170.0 | 2026-09-03 | 21.00 | ok |

### Manufacturer open order (not yet an FBA inbound row)
| placed | ships | ETA at FBA | lines | status | source |
|---|---|---|---|---|---|
| before 2026-09-03 | 2026-09-04 | TBD | TBD (Rami to add) | in transit from 2026-09-04 | suppliers/anabtawi.md |

## Exceptions
- DataDoe orders/sales may be delayed or incomplete from 2026-09-01 (state/company-smoke-test.md).
- Inventory Health snapshot window is 2026-08-28 to 2026-09-03 only; many SKUs show last_in_stock on-or-before-2026-08-27.
- Inventory Health inbound_* columns were 0 while FBA Inbound Shipments shows RECEIVING qty; audit uses inbound shipments export.
- T8-2W2X-INOK appears in orders (hero) but has no FBA Inventory Health rows in the export window.
- products/ empty — heroes by 90-day revenue. suppliers/anabtawi.md lead time/MOQ/case pack/payment terms TBD.
- state/cash.md not yet run — cash/PO-ceiling fields unavailable.
- No Freightos landed-cost run this assignment.

## Requests sent
- 20260903-1955-supply-chain-stockout-risk → advertising

## Proposals written
- none (inbox 20260903-1700: do not write purchase order proposals this week; manufacturer restock already placed)
