# Audit brief (2026-09-06, evening)

You are auditing one part of "Anabtawi OS", a design for running a solo-operator Amazon food brand as a company of AI departments.
Repository under audit: /home/user/anabtawi-os (branch anabtawi-os). Read-only for you: do NOT edit any file except your own report.
The owner, Rami, has rejected the current state as "nothing is clear, I keep finding flaws in five seconds". He wants a minimal core built TONIGHT
on his MacBook (Mac mini arrives next week), using: Claude Code on a Max subscription, the DataDoe MCP (Amazon read layer, key in his hands),
the monday.com MCP (Pro tier, 2 seats; workspace not yet built), QuickBooks. No Telegram, no Slack: monday notifications only.

Your job: find every flaw in your part. Be brutal and specific. For each finding give: severity (BLOCKER = wrong or contradictory, would break
or mislead; MAJOR = unclear, incomplete, or unverifiable in a way that matters; MINOR), file and line or section, what is wrong, and the exact fix
(text or structure). Check consistency ACROSS files: constitution (AGENTS.md), design (docs/ANABTAWI-OS-DESIGN.md), monday schema
(docs/monday-schema.yaml), record schemas (docs/record-schemas.yaml), JSON schemas (docs/schemas/), department.yaml files, README.
Then answer: "What is the minimum of this part needed for a first working core tonight, and what can wait?"
Write your report to /home/user/anabtawi-os/docs/audit/<your-part>.md. Findings first, sorted by severity. Then the tonight-minimum. Under 2,500 words.
Do not praise. Do not summarise the design back. Do not invent facts about vendors; if you rely on a claim, say whether the research reports in docs/research/ support it.
