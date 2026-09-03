---
name: campaign-structure
description: The four-campaign structure per hero SKU and the graduation rules. Use when auditing structure or proposing a new campaign.
---
# Structure per hero SKU

| Campaign | Type | Purpose | Bid posture |
|---|---|---|---|
| `<SKU> Discovery Auto` | Auto, all four match groups | harvest | ~50% of exact bids |
| `<SKU> Discovery Broad` | Broad | harvest with semantic matching | ~50% of exact bids |
| `<SKU> Phrase` | Phrase | confirm converters | slightly under exact |
| `<SKU> Exact Rank` | Exact | rank acquisition | highest; may run above target ACOS during a push named in `state/calendar.md` |
| `<Brand> Defence` | Exact, brand terms and own ASINs | defend | low |

Rules: branded and non-branded never share a campaign. Graduate a search term from Discovery to Phrase after 2 orders; from Phrase to Exact after 3 orders at or under target ACOS. Add the graduated term as a negative exact in the campaign it came from. No dayparting or rule automation under 10 days of history. Starting split of spend: 20–25% discovery, 25–30% phrase, 45–55% exact and defence. Target ACOS per SKU = contribution margin before ads − desired margin after ads, from `state/cash.md`.
