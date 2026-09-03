---
name: po-proposal
description: Write a purchase order proposal as an approval file. Use when a SKU is at risk or the weekly forecast calls for a reorder.
---
# Purchase order proposal

Before writing: send `need-cash-check` to Finance and wait for the answer if the run is scheduled (not an assignment wake). Read `suppliers/<name>.md` for MOQ, case pack, lead time, payment terms.

Quantity = max(MOQ, round up to case pack of: (forecast daily velocity × (lead_time + review_period + buffer_days)) − fulfillable − inbound).
Buffer: 14 days normal; 42 days when a seasonal window starts inside the coverage period.

Landed cost per unit = unit cost + freight + duties + inbound fees, from Freightos for freight and duties. State the currency.

Write `approvals/pending/<date>-supply-chain-po-<sku>.md` per `docs/CONVENTIONS.md`, `action_type: purchase_order`, with: quantity, unit cost, landed cost, cash out and date, ship-by and ETA, cover before and after, what happens if rejected. Mark `tier: T3` if cash out exceeds the PO ceiling remaining in `state/cash.md`.
