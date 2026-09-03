---
name: brief
description: Compile the morning brief from state files, approvals, requests, and yesterday's numbers. Use in the 07:00 run.
---
# The morning brief

File: `briefs/<YYYY-MM-DD>.md`. Under 400 words unless a critical exception justifies more. Every number cites its source. No adjectives.

```
# Brief — <date>

## Did not run
<department>: state file dated <date>. (omit section if all ran)

## Critical
- <one line per item, with the number and the threshold, and the file it came from>

## Decisions (reply "approve 1,3 reject 2 hold 4")
1. <dept> · <action> · <sku> · <cost/impact> · approvals/pending/<file>
2. ...

## Yesterday (<marketplace>)
revenue <n> CAD (7d avg <n>) · units <n> · ad spend <n> · ACOS <n>% · TACoS <n>% · margin <n>%
source: DataDoe export <id>

## Conflicts
- <dept A> wants X; <dept B> wants Y; rule applied: <constitution section>; proposed resolution.

## Learned
- <one line per durable observation added to any MEMORY.md this week>

## Pending
<n> approvals · <n> requests past needed-by
```

Chat delivery (Grok Bot `#company` now, Telegram on the Paperclip runtime later): split at headings so no message exceeds 4,000 characters; the first message is "Did not run" and "Critical" only.
