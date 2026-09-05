---
name: run-procedure
description: The standard start and end of every department run on every runtime. Use at the beginning and end of any scheduled or assignment run.
---
# Run procedure

## Paths
Every path in the constitution, charters, and skills is relative to the repository root. Your charter is `departments/<your-dept>/AGENTS.md`; your skills are `departments/<your-dept>/skills/<name>/SKILL.md`; shared skills are `shared-skills/<name>/SKILL.md`.

## Start
1. Work only in your own clone of the company repo: `~/anabtawi-company-<your-dept>` (for example `~/anabtawi-company-supply-chain`). Never use another department's clone. If your clone does not exist: `git clone git@github.com:ramihabib1/anabtawi-company.git ~/anabtawi-company-<your-dept>`. Then `cd` into it and run `git pull --rebase --autostash`. If the pull fails, stop and write `status: failed` with the error in your state file.
2. Read `AGENTS.md` at the root, then your department `AGENTS.md`, then `memory/MEMORY.md`.
3. List `requests/<your-dept>/inbox/`. Answer each by appending an `## Answer` section, then `git mv` it to `requests/<your-dept>/done/`.
4. Read the state files your charter names, and always `state/calendar.md`.
5. If this is an assignment wake (not your scheduled slot): stop after step 3, commit, push.

## Sending requests
Before sending a request, check `requests/<to-dept>/inbox/` for an open request from you of the same type about the same SKUs. If one exists, append today's update under a `## Update <date>` heading in that file instead of creating a new one. One open request per type per SKU set.

## End
1. Write `state/<yours>.md` with today's date, `runtime:` set to the runtime you are, `status:` ok, degraded, or failed, and `tools_failed:` listing any tool that errored.
2. Write `memory/<today>.md` with observations: facts you saw, not conclusions. One line each with its source.
3. Commit: `git add -A && git commit -m "<dept>: <date> run" && git push`. If push is rejected, run `git pull --rebase --autostash` once and push again; if it fails again, leave the commit and write the failure in your state file next run. Commit only files you own: your state file, your memory, your inbox answers, requests you send, proposals you write.
