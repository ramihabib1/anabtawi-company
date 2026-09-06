# Anabtawi OS

The operating system that runs the Anabtawi brand as a company of AI departments, with Rami as the board.

Read `SPEC.md` (three pages). Then `docs/PLAN.md` for what is built tonight and each day after.

- `AGENTS.md` — the constitution, one page. `CLAUDE.md` and `GEMINI.md` include it.
- `docs/jobs.json` — every scheduled job: reads, tools, steps, writes, timeout, done conditions. `bin/run-job.py <id>` runs one.
- `docs/mcp-servers.json` — every MCP server, variable names only.
- `docs/monday-schema.yaml` — the monday workspace as data; `bin/build-monday.py --init` creates it.
- `docs/record-schemas.yaml`, `docs/schemas/` — record formats; `bin/validate-records.py` checks them.
- `departments/<dept>/` — charter, `department.yaml` (jobs, servers, tier table), skills, memory.
- `state/`, `briefs/`, `approvals/`, `ledger/`, `requests/`, `work/`, `projects/`, `patterns/`, `products/`, `suppliers/`, `strategy/` — the company's record.
- `bin/project-monday.py` — the only process that writes monday. `hands/observe.py` — the runner; tonight it has no write path.
- `docs/audit/` — six independent audits of this design. `docs/research/` — the ten research reports. `docs/archive/` — the long design document and its reasoning.
