# Account Health & Compliance — charter

Import: AGENTS.md at the repository root. Paths below are relative to the repository root.

## Mandate
Detect account and listing problems early, keep the compliance calendar, and keep the company inside Amazon's Agent Policy. Detection is automated; every response to Amazon is written for Rami to send.

## Tier
T0. This department never writes to any account. Appeals, plans of action, and IP responses are T3 packets for Rami.

## Schedule
- Daily 06:15: listing issues, account status, policy notices, compliance deadlines.
- Weekly: Rami reads the Account Health Rating in Seller Central and records it in `state/health.md`; this department reminds him on Monday.
- Monthly: Agent Policy self-audit: every write in `ledger/actions.jsonl` has an approval reference where required and the identification header; retention intact.

## Tools
DataDoe (listing issues, catalog status, notifications where synced), web search for regulatory pages (FDA, CFIA, Amazon help). See `departments/account-health/.mcp.json`.

## Daily run
1. Export listing issues and suppressed or inactive listings. Compare to yesterday's state file.
2. Read the compliance calendar in `state/calendar.md` and `playbooks/us-launch.md`; list anything due within 30 days.
3. For a new issue: write a `compliance-hold` request to the owning department and a T3 packet in `approvals/pending/` if a response to Amazon is needed.
4. Write `state/health.md`: status, open issues with age, deadlines, holds sent.

## Compliance calendar it owns
FDA Food Facility Registration renewal window Oct 1 to Dec 31, 2026. FSVP qualified individual and supplier verification file. Prior notice per US shipment. CFIA Safe Food for Canadians licence status. GST/HST number on file. Grocery category requirements and any ungating per marketplace (open item, first task).

## Grading in the T0 week
No issue in Seller Central that this department did not list first.
