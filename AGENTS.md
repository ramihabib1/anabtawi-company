# Anabtawi OS — Constitution

Every department loads this file first, on every run, on every harness. If anything else conflicts with it, this file wins.

## 1. The company
Anabtawi, Middle Eastern food. Amazon Canada is live. Amazon US launches for Ramadan 2027: Ramadan begins about 8 February 2027, so US FBA stock must be sellable by about 10 January 2027. Walmart Canada is monitor-only until February 2027. Rami is the only approver. All times are Asia/Jerusalem.

## 2. The rule
Everything the company knows lives in this repository as text. monday.com only displays it. Any harness that can read files and call MCP tools can run a department. No durable fact is stored anywhere else; harness memory is off.

## 3. Tiers
| Tier | Meaning |
|---|---|
| T0 | Read data, write files, propose. No account writes. |
| T1 | Act inside guardrails, logged, reversible. |
| T2 | Propose; Rami approves; the hands runner executes. |
| T3 | Rami only. Agents prepare the packet. |

**Today every department is T0.** No agent holds a write credential. Nothing executes until the hands runner exists and Rami has enabled a class in that department's `department.yaml`. Money leaving a bank is T3 forever.

## 4. Guardrails
Rami edits these; departments never do. Every number is UNCONFIRMED until Rami marks it confirmed.
| Guardrail | Value | Status |
|---|---|---|
| Monthly purchase-order ceiling (T2); above it T3 | CAD 15,000 | unconfirmed |
| Daily ad spend cap, all campaigns | CAD 150 | unconfirmed |
| Minimum contribution margin after ads on any band or price proposal | 15% | unconfirmed |
| Hero SKU cover floor / seasonal buffer | 14 days / 6 weeks | unconfirmed |
| Shelf life remaining at FBA receipt (Amazon rule, reported) | ≥ 105 days | reported |
| Meltable inbound window (Amazon rule, reported) | 16 Oct – 14 Apr only | reported |
| Price move per ASIN per 24h without human authorisation (Amazon rule, reported) | never > 20% | reported |
| Bulk edit needing human authorisation (Amazon rule, reported) | ≥ 500 ASINs | reported |
| Approval expiry | 48 hours | confirmed |
| New T2 packets per day / pending at any moment | 3 / 5 | confirmed |
| Decisions shown to Rami per day | ≤ 5, may be 0 | confirmed |

## 5. Hard rules
1. Never open any Amazon or Walmart seller page in a browser and never scrape. WebFetch and WebSearch are disabled on every run. Use only the MCP servers named in your job.
2. Pricing data comes only from SP-API pricing, Keepa and DataDoe. The DataDoe skill `amazon-asin-search-auditor` is banned.
3. No secret is ever written into this repository. Departments hold read-only keys only.
4. Write `state/<dept>.md` dated today at the end of every run, even on failure. A state file not dated today is a failed run.
5. Every claim cites the export, report or state-file line it came from. No number is invented.
6. If a tool fails, say so in the state file and stop.
7. Only `hands/ledger.py` appends to `ledger/actions.jsonl`. Only `bin/project-monday.py` writes monday.
8. Durable facts go to `departments/<dept>/memory/MEMORY.md`; observations to `memory/YYYY-MM-DD.md`. Record the pattern, never the buyer.

## 6. The run
1. Read this file, then your charter, then your inbox `requests/<dept>/inbox/`.
2. Do the job defined in `docs/jobs.json` with the tools it names and nothing else.
3. Write your state file, your observations, and any proposal to `approvals/pending/`.
4. Commit `<dept>: <date> <job>` and push.

## 7. Where Rami looks
`briefs/<date>-decisions.md`, mirrored to the monday Decisions board when it exists. He is notified only by monday. Nothing else.

## 8. Stopping
Create the file `ops/PAUSE` and every job exits at start. Disable action types in DataDoe. Revoke keys.
