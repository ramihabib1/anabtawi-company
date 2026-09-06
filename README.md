# Anabtawi OS

The operating system that runs the Anabtawi brand as a company of AI departments, with Rami as the board. Designed from a blank page in September 2026; nothing here descends from an earlier design.

- `docs/ANABTAWI-OS-DESIGN.md` — the design: architecture, alternatives beaten, monday workspace to the schema, SKU profile, departments, CEO loop, knowledge, money path, human interface, tools and cost, multi-brand, build order.
- `docs/monday-schema.yaml` — the monday workspace as data; `bin/project-monday.py --init` builds it (after approval).
- `docs/anabtawi-os.html` — the rendered design.
- `docs/schemas/` — approval packet and ledger entry JSON Schemas.
- `docs/research/` — the ten research reports the design rests on, every claim tagged VERIFIED / REPORTED / UNKNOWN.
- `AGENTS.md` — the constitution every department loads first. `CLAUDE.md` and `GEMINI.md` include it.
- `departments/<dept>/` — nine departments: charter, `department.yaml`, skills, memory.
- `strategy/`, `patterns/`, `playbooks/`, `products/`, `state/`, `work/`, `projects/`, `requests/`, `approvals/`, `ledger/` — the company's memory and record.
- `hands/`, `bin/`, `ops/` — the runner, the adapters, the machine.

Status: design awaiting Rami's approval. Nothing has been built in monday. Build order is §13 of the design.
