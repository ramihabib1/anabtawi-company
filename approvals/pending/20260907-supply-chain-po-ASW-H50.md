---
id: 20260907-supply-chain-po-ASW-H50
department: supply-chain
tier: T2
action_type: purchase_order
status: pending
created: 2026-09-07T06:10+03:00
expires: 2026-09-09T06:10+03:00
estimated_cost: 2540.16 CAD (product only; landed PENDING Freightos)
skus: [ASW-H50]
payload:
  supplier: anabtawi
  quantity: 84
  unit_cost: 30.24
  ship_by: 2026-09-14
  landed_cost_per_unit: PENDING_FREIGHTOS
  assumptions: lead_21d_moq_1_case_1
decided_by: null
decided_at: null
executed_at: null
ledger_ref: null
---
## Proposal
Restock CA hero `ASW-H50` with 84 units (ASSUMED MOQ/case=1) to cover lead 21d + weekly review 7d + buffer 14d at velocity 2.000/day. product cash ~CAD 2540.16. Landed cost PENDING — Freightos MCP not connected on grok-bot. Propose ship-by 2026-09-14. Tier T2 observation-only file; do not execute on this runtime.

## Reasoning and evidence
Cover before 0.0 days (fulfillable 0, inbound 0, status critical) — state/inventory.md 2026-09-07. Velocity 2.0000/day via units90/sale_days90 (denom 7) from DataDoe orders job 445627c9-8169-40c0-8fc4-629ff39db773. Target units 84.0; ROP 56.0 using ASSUMED lead 21 from suppliers/anabtawi.md TBD. Unit cost: 30.24 CAD (median cogs_item_value/qty from CA orders export). need-cash-check filed: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md (unanswered at write).

## Projected impact
Cover after receipt ~42.0 days at current velocity if qty arrives as fulfillable. Does not create FBA shipment (T0).

## What happens if rejected
Hero remains under floor; estimated lost sales continue ~CAD 119.98/day while fulfillable=0. Keep advertising throttled via stockout-risk. Re-propose next Monday with fresh velocity and Freightos quote.

