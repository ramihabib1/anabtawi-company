---
name: listing-standard
description: Score a listing against the company standard and write a change proposal. Use in the weekly audit.
---
# Listing standard (score each 0–2, 20 max)

1. Title: primary keyword first, brand, size, count, under 200 characters, no ALL CAPS.
2. Bullets: five, benefit-led, each with one secondary keyword, allergen and origin stated.
3. Description or A+: A+ present with comparison chart; brand story module.
4. Images: seven, first on white, one nutrition panel, one lifestyle, one size reference.
5. Attributes: ingredients, allergens, net quantity in marketplace units, expiration type, country of origin, all complete.
6. Search terms: backend field full, no duplicates of title words, no competitor brands.
7. Variations: family correct; no orphan child.
8. Compliance: no prohibited claims; certification claims only with a certificate on file in `products/<sku>.md`.
9. Localisation: correct language, units, and nutrition format for the marketplace.
10. Issues: none open in DataDoe listing issues.

Proposal: an approval file with `action_type: listing_change`, the full patch as JSON against the marketplace product type schema, the score before and expected after, and the 30-day conversion baseline.
