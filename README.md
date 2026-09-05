# Anabtawi Company

The operating system of the Anabtawi brand's e-commerce business, as a company of AI departments.
Everything here is text. Any agent runtime that can read a folder, call MCP servers, and push to git can run a department.

- `AGENTS.md` — the constitution. Every department loads it first. `CLAUDE.md` imports it for Claude Code.
- `departments/<dept>/` — one folder per department: `AGENTS.md` charter, `.mcp.json` tools, `skills/`, `memory/`.
- `state/` — one dated state file per department; the shared blackboard.
- `requests/<dept>/inbox/` — typed requests between departments. Schema in `docs/CONVENTIONS.md`.
- `approvals/` — durable approval files. Only Rami's approval flips a file to `approved/`; only the hands runner executes it.
- `products/`, `suppliers/`, `markets/`, `playbooks/` — the company's knowledge.
- `ledger/` — `actions.jsonl` (every account write), `decisions.md`, `kpis.csv`.
- `briefs/`, `meetings/` — the company's diary.
- `runtimes/` — how to run the departments on each runtime: Grok Bot (interim), Paperclip on the Mac mini (target), Claude Code and Codex headless.
- `docs/` — conventions, schemas, and the design document.

Design and research: `docs/DECISION-CONTROL-PLANE.md` (why Paperclip runs the company and what we build ourselves), `docs/research/` (the four surveys behind it), and the anabtawi-os repository for the v3 design and the 12 earlier surveys.
