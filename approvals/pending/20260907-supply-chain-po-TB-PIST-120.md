---
id: 20260907-supply-chain-po-TB-PIST-120
department: supply-chain
tier: T2
action_type: purchase_order
status: pending
created: 2026-09-07T06:10+03:00
expires: 2026-09-09T06:10+03:00
estimated_cost: unknown CAD (COGS missing; landed PENDING Freightos)
skus: [TB-PIST-120]
payload:
  supplier: anabtawi
  quantity: 54
  unit_cost: null
  ship_by: 2026-09-14
  landed_cost_per_unit: PENDING_FREIGHTOS
  assumptions: lead_21d_moq_1_case_1
decided_by: null
decided_at: null
executed_at: null
ledger_ref: null
---
## Proposal
Restock CA hero `TB-PIST-120` with 54 units (ASSUMED MOQ/case=1) to cover lead 21d + weekly review 7d + buffer 14d at velocity 2.000/day. product cash unknown (COGS missing). Landed cost PENDING — Freightos MCP not connected on grok-bot. Propose ship-by 2026-09-14. Tier T2 observation-only file; do not execute on this runtime.

## Reasoning and evidence
Cover before 15.0 days (fulfillable 0, inbound 30, status watch) — state/inventory.md 2026-09-07. Velocity 2.0000/day via units90/sale_days90 (denom 15) from DataDoe orders job 445627c9-8169-40c0-8fc4-629ff39db773. Target units 84.0; ROP 56.0 using ASSUMED lead 21 from suppliers/anabtawi.md TBD. Unit cost: unknown (COGS missing or 0 in order export). need-cash-check filed: requests/finance/inbox/20260907-0610-supply-chain-need-cash-check.md (unanswered at write).

## Projected impact
Cover after receipt ~42.0 days at current velocity if qty arrives as fulfillable. Does not create FBA shipment (T0).

## What happens if rejected
Inbound may carry short-term cover, but ASSUMED lead+buffer target is not met after current inbound; risk of returning under floor within ~15.0 days of inbound burning down. Re-propose next week with Freightos + confirmed MOQ/case.

