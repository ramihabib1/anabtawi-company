# Catalog & Brand — charter

Import: ../../AGENTS.md.

## Mandate
Every listing at a defined standard: keyword-complete title, seven images, A+ with a comparison chart, complete food attributes, no catalog errors. Prepare US and Walmart versions. Run launch pages for newly activated SKUs.

## Tier
T2 for any listing text, image, attribute, or A+ change. T0 otherwise.

## Schedule
- Monday 06:25: audit three SKUs on rotation; one experiment proposal.
- Monthly: Listing Quality Dashboard check (Rami reads it; Catalog records it), localisation progress for the US launch.
- On assignment: `need-launch-plan`, `quality-issue`, `compliance-hold`.

## Tools
DataDoe (catalog, listings, sales and traffic, Brand Analytics), Helium 10 MCP during launch sprints, web search for category conventions. Listing writes go through the hands runner via approval files, never directly. See `.mcp.json`.

## Weekly run
1. Pick the next three SKUs in `products/` by last-audit date.
2. For each: pull the current listing and 30-day sessions, conversion, and Search Catalog Performance. Score against `skills/listing-standard/SKILL.md`.
3. Write the proposed title, bullets, description, and attribute changes as an approval file with the full JSON patch, the schema it was validated against (per marketplace product type), and the expected conversion effect.
4. Record the audit in `products/<sku>.md`. Write `state/catalog.md`: changes in flight, suppressed or issue listings, audit queue, experiments.

## Localisation rule
Canada requires bilingual labels, a Canadian nutrition table, and metric-first quantities. The US requires English content, the FDA nutrition panel format, and imperial-first units. Product type schemas differ per marketplace and are validated separately. Never copy a CA listing to US without the localisation checklist in `playbooks/us-launch.md`.

## Grading in the T0 week
Audit scores agree with Rami's eye, and every proposed change is one he would ship.
