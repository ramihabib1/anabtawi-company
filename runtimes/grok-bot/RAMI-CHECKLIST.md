# Rami's part (about 20 minutes)

1. Push this repo to GitHub as `anabtawi-company` (see PUSH-INSTRUCTIONS). Create a deploy key with write access on that repo only. Keep the private key to paste into the Chief of Staff bot's git setup; nothing else ever sees it.
2. In DataDoe: create a separate MCP key for the bots. Confirm every action type is disabled in Settings → Actions. You can revoke this key at any time; that is the kill switch for the data side.
3. In Grok Bot: hire `anabtawi-chief-of-staff`. Paste `runtimes/grok-bot/bots/chief-of-staff.md` as its system prompt. Add the DataDoe MCP connector with the bot key. Create the `#company` group chat in Grok Bot with the bot and yourself; that chat is where the brief, approvals, and failures arrive on this runtime.
4. Send it its first message: "Build the company. Follow runtimes/grok-bot/BOOTSTRAP.md from the repo at <repo URL>. Deploy key follows in the next message." Then paste the deploy key.
5. Watch `#company`. Answer its questions. Grade the first brief the next morning.

What you do not give any bot: Seller Central login, Ads API token, Keepa key, QuickBooks, SP-API, your personal DataDoe key.
