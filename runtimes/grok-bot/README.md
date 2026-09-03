# Grok Bot pilot (interim, until Paperclip runs on the Mac)

Scope: Tier 0 only. Read-only DataDoe key. A deploy key with write access to this repo only. No Seller Central login, no Ads MCP, no SP-API, no QuickBooks, no Keepa key.

Why the limits: all bots on a Grok account share one cloud computer, and xAI's Grok Build client was found in July 2026 uploading repositories including secret files. Nothing a bot holds may be a secret that matters.

## Order
1. `account-health` first (reads only, easy to grade), then `chief-of-staff` (the brief). Two bots for two days.
2. If both fire on schedule, read DataDoe through MCP, write their state files, commit and push, add `supply-chain`, `pricing-intel`, `customer`. Never `advertising` on this runtime (it has T1 writes).

## Per bot, in the Grok Bot app
1. Hire a new bot. Name it `anabtawi-<dept>`.
2. Paste the system prompt from `bots/<dept>.md`.
3. Connectors: add the DataDoe MCP with the read-only key (Bring-Your-Own-MCP). No other connectors.
4. On the bot's computer, once: `git clone <deploy-key URL> ~/anabtawi-company`. The system prompt tells the bot to pull and push.
5. Routine: schedule the bot at its calendar time (`docs/CALENDAR.md`), daily.
6. Channel: connect the Telegram channel for the Chief of Staff bot only, so the brief reaches your phone. Other bots have no channel.

## Pass criteria (three consecutive days)
- Fires within 15 minutes of schedule without you touching it.
- Pulls, writes `state/<dept>.md` dated today, commits, pushes.
- Never opens Seller Central or any Amazon page in its browser (check the activity screen).
- Findings match what you see in Seller Central.
- Touches only its department folder, its state file, and its inbox.
Two failures on any item and the pilot fails; wait for the Mac.
