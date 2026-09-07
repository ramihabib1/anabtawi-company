---
id: 20260907-supply-chain-po-H8-PWJ0-3B1Y
department: supply-chain
tier: T2
action_type: purchase_order
status: pending
created: 2026-09-07T06:10+03:00
expires: 2026-09-09T06:10+03:00
estimated_cost: 434.7 CAD (product only; landed PENDING Freightos)
skus: [H8-PWJ0-3B1Y]
payload:
  supplier: anabtawi
  quantity: 46
  unit_cost: 9.45
  ship_by: 2026-09-14
  landed_cost_per_unit: PENDING_FREIGHTOS
  assumptions: lead_21d_moq_1_case_1
decided_by: null
decided_at: null
executed_at: null
ledger_ref: null
---
## Proposal
Restock CA hero `H8-PWJ0-3B1Y` with 46 units (ASSUMED MOQ/case=1) to cover lead 21d + weekly review 7d + buffer 14d at velocity 2.600/day. product cash ~CAD 434.70. Landed cost PENDING — Freightos MCP not connected on grok-bot. Propose ship-by 2026-09-14. Tier T2 observation-only file; do not execute on this runtime.

## Reasoning and evidence
Cover before 24.6 days (fulfillable 0, inbound 64, status ok) — state/inventory.md 2026-09-07. Velocity 2.6000/day via units90/sale_days90 (denom 25) from DataDoe orders job 445627c9-8169-40c0-8fc4-629ff39db773. Target units 109.2; ROP 72.8 using ASSUMED lead 21 from suppliers/anabtawi.md TBD. Unit cost: 9.45 CAD (median cogs_item_value/qty from CA orders export). need-cash-check filed: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md (unanswered at write).

## Projected impact
Cover after receipt ~42.3 days at current velocity if qty arrives as fulfillable. Does not create FBA shipment (T0).

## What happens if rejected
Inbound may carry short-term cover, but ASSUMED lead+buffer target is not met after current inbound; risk of returning under floor within ~24.6 days of inbound burning down. Re-propose next week with Freightos + confirmed MOQ/case.

