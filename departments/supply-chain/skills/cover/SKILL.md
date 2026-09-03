---
name: cover
description: Compute days of cover per SKU per marketplace with inbound and seasonality. Use in the daily Supply Chain run.
---
# Days of cover

For each SKU and marketplace:

- velocity_30 = units sold in the last 30 days ÷ 30 (DataDoe orders export). If a stockout occurred in the window, use the days in stock as the denominator and note it.
- fulfillable = FBA fulfillable units (DataDoe FBA inventory export). Reserved units are not fulfillable.
- inbound_in_window = units on inbound shipments with ETA inside the cover window (DataDoe inbound export).
- cover_days = (fulfillable + inbound_in_window) ÷ velocity_30.
- seasonal multiplier: apply the SKU's multiplier from `products/<sku>.md` for windows in `state/calendar.md` (Ramadan, Q4). Report both raw and adjusted cover.

Thresholds from the constitution: floor 14 days; hero seasonal buffer 6 weeks. Lead time from `suppliers/<name>.md`.

Output table columns: sku, marketplace, fulfillable, inbound, velocity_30, cover_days, cover_adjusted, floor, lead_time, status (ok | watch | risk | critical).
- watch: cover_adjusted < floor + lead_time + 7
- risk: cover_adjusted < floor + lead_time
- critical: cover_adjusted < floor
