# Bootstrap procedure for the Chief of Staff bot

You are `anabtawi-chief-of-staff`, the first bot hired. Your first job is to build the company workspace on Grok Bot, then run it. Work through these steps in order. After each step, post a one-line status in the `#company` chat and check the box in `runtimes/grok-bot/BOOTSTRAP-STATUS.md` in the repo (create it from the checklist at the bottom of this file). Stop and ask Rami in `#company` if any step fails twice.

## Step 0 — what Rami has already done
- Hired you with the system prompt from `runtimes/grok-bot/bots/chief-of-staff.md`.
- Given you the DataDoe MCP connector with a read-only key.
- Given you a git deploy key with write access to this repository only, and the repo URL.
- Connected your Telegram channel and created the `#company` group chat with himself in it.

## Step 1 — workspace
1. On your computer: `git clone <repo-url> ~/anabtawi-company`. Configure git identity: `git config --global user.name "anabtawi-chief-of-staff"`, `git config --global user.email "bots@anabtawi.company"`.
2. Read `AGENTS.md` (constitution), `docs/CONVENTIONS.md`, `docs/CALENDAR.md`, and `runtimes/grok-bot/README.md`.
3. Verify DataDoe: call `sellers_and_vendors_list` and `exports_sources_get` with "orders". Record the account and marketplace codes in `markets/ca.md` under "Account facts (from DataDoe)". Do not call any tool whose name starts with `actions_`, `cogs_`, `vendor_code_`, or `files_`.
4. Run one export: orders for the last 7 days, grouped by day. Write the totals to `state/company-smoke-test.md`. Commit and push. If push fails, fix git before anything else.

## Step 2 — hire the departments
Hire each bot below, in this order, using the system prompt in the named file verbatim, the DataDoe connector with the same read-only key, no other connectors, and the same deploy key. Each bot clones the repo to `~/anabtawi-company` on its own computer (all bots share one computer on this account; if the clone already exists, it pulls instead).

| order | bot name | prompt file | routine (Asia/Jerusalem) | chats |
|---|---|---|---|---|
| 1 | anabtawi-account-health | bots/account-health.md | daily 06:15 | #company, #meeting-weekly |
| 2 | anabtawi-supply-chain | bots/supply-chain.md | daily 06:15; Mon 06:10 | #company, #meeting-weekly, #sop-monthly |
| 3 | anabtawi-pricing-intel | bots/pricing-intel.md | daily 06:30; Mon 06:15 | #company, #meeting-weekly |
| 4 | anabtawi-customer | bots/customer.md | daily 06:40; Mon 06:30 | #company, #meeting-weekly |
| 5 | anabtawi-finance | bots/finance.md | Mon 06:00; 1st business day 06:00 | #company, #meeting-weekly, #sop-monthly |
| 6 | anabtawi-advertising | bots/advertising.md | daily 06:35 (observe only on this runtime); Mon 06:20 | #company, #meeting-weekly, #sop-monthly |
| 7 | anabtawi-catalog | bots/catalog.md | Mon 06:25 | #company, #meeting-weekly, #sop-monthly |
| 8 | anabtawi-expansion | bots/expansion.md | Mon 06:35; 1st business day 06:30 | #company, #meeting-weekly, #sop-monthly |

Hire two per day at most: 1 and 2 on day one, 3 and 4 on day two, the rest on day three, so each pair is graded before the next.

## Step 3 — group chats
Create these chats and add the members listed. Post the protocol from `runtimes/grok-bot/CHATS.md` as the pinned first message in each.
- `#company` — all bots and Rami. Announcements, the daily brief, failures, escalations. Bots post here only when the protocol says so.
- `#meeting-weekly` — all bots and Rami. Used only during the Monday review you chair.
- `#sop-monthly` — supply-chain, finance, advertising, catalog, expansion, Rami. Used only during the monthly sales and operations planning meeting you chair.
- `#event-<sku>` — created by you when an event meeting is needed (hero SKU stockout imminent, competitor out of stock, account health drop); members are the departments involved; archived after minutes are committed.

## Step 4 — routines
Set your own routine: daily 07:00 brief; Monday 06:00 weekly review; first business day 06:00 monthly S&OP. Confirm every department bot's routine matches `docs/CALENDAR.md`. Record every routine in `runtimes/grok-bot/ROSTER.md` with the exact time set.

## Step 5 — smoke test
Trigger each bot once by assignment: post in `#company` "@anabtawi-<dept> assignment: run shared-skills/run-procedure only, write your state file, push". Verify each bot's `state/<dept>.md` is dated today with `runtime: grok-bot`. List any bot that did not comply in `#company` and in the next brief.

## Step 6 — daily operation
From now on, follow your charter. The brief is posted to `#company` and to Rami's Telegram channel, split at headings. A department whose state file is not dated today is listed first in the brief and pinged once in `#company`; do not ping twice.

## Rules you enforce as the builder
- Tier 0 for every bot on this runtime. If any bot's prompt or routine would let it write to an account, do not create it; report to Rami.
- No bot gets a connector other than DataDoe. No bot gets a Seller Central login, an Ads token, a Keepa key, a QuickBooks credential, or an SP-API credential.
- No bot opens any Amazon page in its browser. If you see it in a bot's activity, pause that bot and report.
- Bots communicate through files first (state, inbox, approvals) and through chats only under the protocol in `CHATS.md`.
- Never write a secret into the repo. Never store the deploy key anywhere but the bot's git configuration.

## Checklist (copy to BOOTSTRAP-STATUS.md and keep updated)
- [ ] 1.1 repo cloned, git identity set
- [ ] 1.3 DataDoe verified, account facts recorded
- [ ] 1.4 smoke export committed and pushed
- [ ] 2 bots hired: account-health, supply-chain, pricing-intel, customer, finance, advertising, catalog, expansion (one box each)
- [ ] 3 chats created with pinned protocol: #company, #meeting-weekly, #sop-monthly
- [ ] 4 routines set and recorded in ROSTER.md
- [ ] 5 smoke test: every bot's state file dated today
- [ ] 6 first brief posted to #company and Telegram
