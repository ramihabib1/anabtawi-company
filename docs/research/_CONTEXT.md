> Research report produced 2026-09-06 during the founding engagement. Where it mentions files of an earlier repository, treat those as context the researcher had, not as part of this design. The design that governs is docs/ANABTAWI-OS-DESIGN.md.

# Shared context for research agents (2026-09-06)

Client: Rami Anabtawi, AI engineer, solo operator of the Anabtawi brand (Middle Eastern food, ~50-60 SKUs, 10-15 winners).
Amazon Canada ~CAD 8-10k/month today. Walmart Canada set up (monitor-only until Feb 2027). Amazon US launches for Ramadan 2027
(stock in US FBA by mid-January 2027). Targets: Canada CAD 20k/month by March 2027 with 10 newly activated SKUs; US USD 40-60k/month
in year one; seven figures/year; then run other brands on the same system.

Subscriptions: Claude Max, ChatGPT (Codex), SuperGrok, plus API credits. monday.com Pro tier (2 seats). QuickBooks for accounting.
DataDoe (hosted MCP + REST over Seller Central / Vendor Central / Ads data; Skill Hub; scheduled agents; Actions with dry run + approval)
is the Amazon read layer and currently the ONLY Amazon access. No SP-API private developer registration yet.
A Mac mini arrives next week (always-on machine allowed for a local "hands" runner). Rami maintains no servers and babysits nothing.

Goal being designed: an operating system that runs the business as a company of AI departments (finance, supply chain, advertising,
catalog, pricing & market intel, customer, account health & compliance, expansion, CEO/strategy layer), managed on monday.com,
running unattended on any agent harness (Claude Code, Codex CLI, Grok, Claude Cowork, monday agents...), with a knowledge layer that
compounds, an approval/money path where money never moves without Rami's explicit approval, and a daily ranked decision list for Rami.

Non-negotiables: Amazon BSA Section 19 Agent Policy (March 2026): no browser automation or scraping of Seller Central; official APIs
and MCP only. Subscriptions first, API as fallback, legal use only. No lock-in beyond monday as management surface. Secrets only in a vault.
Must instantiate a second brand cheaply. Time zone Asia/Jerusalem.

Report rules: tag EVERY factual claim VERIFIED (you opened the primary source today and it says so; give URL), REPORTED (secondary
source or vendor marketing; give URL), or UNKNOWN (could not confirm; say what you tried). Date-stamp anything that may change (pricing,
terms). Prefer official docs, terms pages, pricing pages, changelogs. Be opinionated: end with "Implications for the design" and
"Open questions". Write in plain markdown, 2,500-5,000 words, tables where they help. No fluff.
