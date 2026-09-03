# Group chat protocol (pinned in every chat)

Chats are for meetings and alerts. They are never the record. The record is the repo: state files, inbox requests, approval files, minutes.

## Who may post, and when
- `anabtawi-chief-of-staff` opens and closes every meeting and posts the daily brief.
- A department bot posts only: (a) when asked by name in the current meeting round, (b) once to report a failed run, (c) once to acknowledge an assignment. Never otherwise. Never reply to another bot's message unless the Chief of Staff asked for a second round.
- Rami may post anything, any time. A message from Rami that says "approve", "reject", or "hold" about a numbered decision is a decision; the Chief of Staff records it in the approval file and the ledger.

## Meeting rounds
1. The Chief of Staff posts the question, the decision needed, and the files to read, and names the departments to answer.
2. Each named department replies exactly once with this template, under 120 words:
   `POSITION: ... · EVIDENCE: <file or export> · RISK: ... · RECOMMENDATION: ...`
3. The Chief of Staff may open one second round with a specific follow-up to specific departments.
4. The Chief of Staff closes: decision, rule applied from the constitution, actions as inbox requests, anything Tier 2 or above as an approval file for Rami, and commits `meetings/<date>-<name>.md`. Then posts "closed, minutes committed".

## Alerts
A bot that fails a run posts one line: `FAILED <dept> <date>: <error>` and stops. The Chief of Staff decides what to do.

## What is not allowed in chat
No numbers without a source. No decisions by bots. No instructions to another bot except by the Chief of Staff during a meeting or as an assignment. No secrets, keys, or logins, ever. Nothing said in chat overrides a file in the repo.
