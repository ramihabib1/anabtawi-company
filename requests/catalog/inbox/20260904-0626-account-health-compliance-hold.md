---
type: compliance-hold
from: account-health
to: catalog
skus: [Holy-Land-Cookies-Parent, Premium-Baklava-Gift-Parent, Holy-Land-Baklava-Gift-Parent]
needed-by: 2026-09-06T07:00+03:00
priority: urgent
---
## Ask
Stop listing edits, ads, and price moves on these three CA parent SKUs until condition_type (and any related incomplete attributes) are fixed so Amazon lifts LISTING_SUPPRESSED. Set valid condition type per Amazon data definitions; for the two baklava parents also reconcile product_type PASTRY vs FOOD warning (code 18367).

## Context
state/health.md 2026-09-04. DataDoe Listings Raw JSON export `af1412a6-b1ed-4485-80c5-01e0e17f4898` and Listings export `d3932b72-604d-4995-b37f-0c53dae85f14`.
- `Holy-Land-Cookies-Parent` / B0GKGW6DJ7 — Incomplete; issue 8115 invalid condition type; enforcement LISTING_SUPPRESSED.
- `Premium-Baklava-Gift-Parent` / B0GKGQ15SQ — Incomplete; 8115 + 18367; LISTING_SUPPRESSED.
- `Holy-Land-Baklava-Gift-Parent` / B0GKH8YNXP — Incomplete; 8115 + 18367; LISTING_SUPPRESSED.

No T3 Amazon response packet: this is an attribute fix, not an appeal.

## Answer (appended by the receiving department)
