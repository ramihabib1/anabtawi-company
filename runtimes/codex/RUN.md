# Running a department with Codex CLI headless (ChatGPT plan)

```bash
codex login --device-auth           # once, on the box
cd ~/anabtawi-company/departments/advertising
codex exec --json --cd . \
  "Run this department's scheduled heartbeat per AGENTS.md and shared-skills/run-procedure/SKILL.md." \
  < AGENTS.md
```
Configure MCP servers in Codex's config for this directory from `.mcp.json` (Codex reads `mcpServers` in its config). Codex honours `AGENTS.md`; untrusted directories do not load project instructions, so mark the repo trusted once.
