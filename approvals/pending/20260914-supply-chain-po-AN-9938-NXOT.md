---
id: 20260914-supply-chain-po-AN-9938-NXOT
department: supply-chain
tier: T2
action_type: purchase_order
status: pending
created: 2026-09-14T06:10+03:00
expires: 2026-09-16T06:10+03:00
estimated_cost: 735.84 CAD (product only; landed PENDING Freightos)
skus: [AN-9938-NXOT]
payload:
  supplier: anabtawi
  quantity: 72
  unit_cost: 10.22
  ship_by: 2026-09-21
  landed_cost_per_unit: PENDING_FREIGHTOS
  assumptions: lead_21d_moq_1_case_1
decided_by: null
decided_at: null
executed_at: null
ledger_ref: null
---
## Proposal
Restock CA hero `AN-9938-NXOT` with 72 units (ASSUMED MOQ/case=1) to cover lead 21d + weekly review 7d + buffer 14d at velocity 1.714/day. product cash ~CAD 735.84. Landed cost PENDING — Freightos MCP not connected on grok-bot. Propose ship-by 2026-09-21. Tier T2 observation-only file; do not execute on this runtime.

## Reasoning and evidence
Cover before 0.0 days (fulfillable 0, inbound 0, status critical) — state/inventory.md 2026-09-14. Velocity 1.7143/day (vel_denom 7) from DataDoe shipped orders job 5a4823aa-7eff-44f4-88fb-2ef4b55f4916. Target units 72.0; ROP 48.0 using ASSUMED lead 21 from suppliers/anabtawi.md TBD. Unit cost: 10.22 CAD (median cogs_item_value/qty from CA shipped orders export; null if missing/zero). need-cash-check filed: requests/finance/inbox/20260914-0610-supply-chain-need-cash-check.md (unanswered at write).

## Projected impact
Cover after receipt ~42.0 days at current velocity if qty arrives as fulfillable (includes current inbound). Does not create FBA shipment (T0).

## What happens if rejected
Hero remains under target cover; estimated lost sales continue ~CAD 46.27/day while fulfillable=0. Keep advertising throttled via stockout-risk. Re-propose next Monday with fresh velocity and Freightos quote.
