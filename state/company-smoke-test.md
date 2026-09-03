---
department: chief-of-staff
date: 2026-09-03
run: assignment
runtime: grok-bot
status: ok
tools_failed: []
---
## Headline
DataDoe smoke export for CA orders, last 7 days grouped by day, completed. Five orders / five units / CAD 220.96 across four active days.

## Data
Source: DataDoe export `5b93ce3e-a7f9-4543-97bb-9674b6888bd7` (`exports_create` + `exports_raw_download`), source `Order Line Items` (`89b27535d2` / `amazon_order_items_with_cogs`), seller `5692b95f-f3f0-4063-9c1c-40177c54f408` (ANABTAWI SWEETS CA), range 2026-08-28 to 2026-09-03, grouped by `date`. Currency: CAD.

| date | orders (distinct amazon_order_id) | units (sum quantity) | item_price_value CAD |
|---|---:|---:|---:|
| 2026-08-28 | 2 | 2 | 40.99 |
| 2026-08-29 | 1 | 1 | 59.99 |
| 2026-08-30 | 0 | 0 | 0.00 |
| 2026-08-31 | 0 | 0 | 0.00 |
| 2026-09-01 | 1 | 1 | 59.99 |
| 2026-09-02 | 1 | 1 | 59.99 |
| 2026-09-03 | 0 | 0 | 0.00 |
| **total** | **5** | **5** | **220.96** |

Days with no row in the export are shown as zero.

## Exceptions
- DataDoe flagged an ongoing incident: orders and sales data in `amazon_order_items_with_cogs` may be delayed or incomplete from 2026-09-01 onwards. 2026-09-03 has no row.

## Requests sent
- none

## Proposals written
- none
