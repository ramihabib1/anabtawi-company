# Running a department with Claude Code headless (Max subscription)

```bash
export CLAUDE_CODE_OAUTH_TOKEN=...   # from `claude setup-token`, one-year token; never set ANTHROPIC_API_KEY alongside it
cd ~/anabtawi-company/departments/supply-chain
claude -p "Run this department's scheduled heartbeat per AGENTS.md and shared-skills/run-procedure/SKILL.md." \
  --output-format json --permission-mode acceptEdits \
  --mcp-config .mcp.json \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(git:*),mcp__datadoe__*,mcp__freightos__*"
```
Meetings: add `--agents` with one subagent per department, or let the Chief of Staff charter spawn them via the Task tool. Weekly limits are shared with your interactive use; watch `/status`.
