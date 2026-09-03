# Paperclip on the MacBook (moves to the Mac mini unchanged)

Verified from the Paperclip README on 2026-09-03. Requirements: Node.js 24.11+, pnpm 9.15+. Postgres is embedded by default.

## Install
```bash
# one-off, no permanent install
npx --registry https://registry.npmjs.org paperclipai onboard --yes
# or managed install
curl -fsSL https://paperclip.ing/install.sh | bash -s -- --no-prompt --no-onboard
paperclipai onboard --yes --bind tailnet   # never --bind lan on a laptop that leaves the house
```
UI and API: http://localhost:3100. `paperclipai configure` to change settings later.

## Before hiring anyone
1. Clone this repo to `~/anabtawi-company`. Every agent's `cwd` is `~/anabtawi-company/departments/<dept>`.
2. Sign in on the host: `claude` (Max login) and `codex login`. Paperclip's `claude_local` adapter inherits the host login; `codex_local` links the host ChatGPT login into each agent's managed home automatically. Do not set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in the environment unless you want that agent API-billed.
3. Export secrets for MCP servers from your vault before starting Paperclip (`op run --env-file=runtimes/paperclip/secrets.env -- paperclipai ...`, or Infisical equivalent). Names are in `docs/MCP-SERVERS.md`.

## Hire the departments
Create one company "Anabtawi". Hire agents from `runtimes/paperclip/agents/*.json` (adapter config per department). Reporting lines: every department reports to Chief of Staff; Chief of Staff reports to the board (Rami).

Adapter keys (verified from the adapter docs):
- `claude_local`: `cwd`, `model`, `promptTemplate`, `engine` (auto | acp | cli), `maxTurnsPerRun` (default 300), `timeoutSec`, `graceSec`, `dangerouslySkipPermissions` (default true in headless), `env`.
- `codex_local`: `cwd`, `model` (unset = CLI default), `modelReasoningEffort`, `instructionsFilePath`, `promptTemplate`, `search`, `dangerouslyBypassApprovalsAndSandbox`, `timeoutSec`, `graceSec`, `outputInactivityTimeoutMs` (default 7 min), `env`.

## Heartbeats and budgets
Set each agent's heartbeat to its calendar slot in `../../AGENTS.md` and `docs/CALENDAR.md` (Asia/Jerusalem). Set a monthly budget per agent (Paperclip pauses the agent on overspend; subscription runs report zero cost, so budgets bite only on API-billed agents). Turn on the audit log export to `ledger/paperclip-audit/` if the version supports it.

## First week
All departments at T0. Grade state files and proposals daily. Advertising moves to T1 only after Rami edits its charter.

## Moving to the Mac mini
Clone the repo, restore Paperclip's data directory (or re-hire from the JSON files, five minutes), sign in to both CLIs, export secrets, start.
