---
name: run-procedure
description: The standard start and end of every department run on every runtime. Use at the beginning and end of any scheduled or assignment run.
---
# Run procedure

## Start
1. `git pull --rebase` in the company repo. If it fails, stop and write `status: failed` with the error in your state file.
2. Read `AGENTS.md` at the root, then your department `AGENTS.md`, then `memory/MEMORY.md`.
3. List `requests/<your-dept>/inbox/`. Answer each by appending an `## Answer` section, then `git mv` it to `requests/<your-dept>/done/`.
4. Read the state files your charter names, and always `state/calendar.md`.
5. If this is an assignment wake (not your scheduled slot): stop after step 3, commit, push.

## End
1. Write `state/<yours>.md` with today's date, `runtime:` set to the runtime you are, `status:` ok, degraded, or failed, and `tools_failed:` listing any tool that errored.
2. Write `memory/<today>.md` with observations: facts you saw, not conclusions. One line each with its source.
3. Commit: `git add -A && git commit -m "<dept>: <date> run" && git push`. If push is rejected, pull with rebase once and push again; if it fails again, leave the commit and write the failure in your state file next run.
