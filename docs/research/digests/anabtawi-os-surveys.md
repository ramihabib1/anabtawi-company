# Digest: anabtawi-os research corpus (13 surveys + V2 design), extracted 2026-09-05

Source root: /home/user/ramihabib1/anabtawi-os/docs/research/ and /home/user/ramihabib1/anabtawi-os/docs/ANABTAWI-OS-V2-DESIGN.md
Surveys dated 2026-09-02/03. Tags are copied from the originals (VERIFIED / REPORTED / UNKNOWN). "V-adj" = the source wrote "VERIFIED-adjacent/-ish/-by-consensus".
Corpus caveat (README.md): several agents framed recommendations around the retired v1 stack (Supabase, Hetzner executor, Mem0, python Telegram bot) because the old CLAUDE.md was in context. Egress-blocked during research: datadoe.com, x.ai/docs.x.ai, developer-docs.amazon.com, sellercentral.amazon.com, advertising.amazon.com, helium10.com, keepa.com, support.anthropic.com, developers.openai.com, help.openai.com, glama/smithery/lobehub. Anything from those is REPORTED even when quoting the vendor.

---

## 1. VERIFIED facts that constrain the design (one line each; file; URL)

### 1.1 Amazon policy (BSA Section 19 Agent Policy, DPP/AUP, SP-API)
- BSA Agent Policy = new Section 19, announced ~Feb 17 2026, effective Mar 4 2026, no opt-out; 90-day transition to early June 2026, then enforcement without warning. REPORTED-high-confidence (spapi-writes.md §3; catalog-intel.md §4.0 calls it VERIFIED via 5+ secondary sources). https://sellercentral.amazon.com/seller-forums/discussions/t/84e3f6b1-42f7-4cf3-a189-a5cc8d78d838 ; https://ppc.land/amazons-new-ai-agent-rules-shake-up-sellers-before-march-4-deadline/ ; https://www.digitalapplied.com/blog/amazon-ai-agent-policy-march-2026-automated-seller-rules
- "Agent" = any automated software/AI acting on a seller account or accessing Amazon Services on the seller's behalf; explicitly names repricers, PPC automation, listing tools, browser extensions, fulfillment scripts. REPORTED (spapi-writes.md §3.2).
- Three obligations: (1) identify as automated: `Agent/[agent name]` in User-Agent on all HTTP requests, no simulating human behaviour, no CAPTCHA bypass; (2) comply continuously; (3) cease on Amazon's request; Amazon may restrict access "through technical or other measures". REPORTED near-verbatim (spapi-writes.md §3.3). https://sellercentral.amazon.com/mws/static/agreement
- All automated seller actions must flow through registered SP-API applications with an app ID tied to a verified developer account; browser automation, screen scraping, undocumented endpoints explicitly prohibited. REPORTED (spapi-writes.md §3.4).
- Vendor due-diligence test circulating: ask any third-party tool for (a) SP-API application ID, (b) sample audit-log export, (c) written Agent Policy compliance statement; no answer in 48h = presumed non-compliant. REPORTED (spapi-writes.md §3.4).
- Logging: every automated action logged with timestamp, action type, inputs, outputs; retrievable; retained >= 12 months. REPORTED (spapi-writes.md §3.5).
- Human-authorization floor ("Tier 3"): bulk edits >= 500 ASINs in one batch; price changes > 20% in any rolling 24h (per ASIN); account configuration changes; must be "a real human approval in the workflow, not an automated approval gate that mimics human confirmation". REPORTED (spapi-writes.md §3.6; catalog-intel.md §4.0).
- Pricing-specific: automated repricing via SP-API permitted within rate/update limits, but agents may NOT use scraped competitor data obtained outside Product Advertising API / SP-API to drive pricing decisions. REPORTED (catalog-intel.md §4.0). https://ecomclips.com/blog/amazon-bsa-agent-policy-2026-what-every-seller-must-do-before-march-4-to-protect-rankings-sales/
- Same BSA update: separate BSA for Mexico; new restrictions on using Amazon materials to train AI models; dispute-resolution updates. REPORTED (spapi-writes.md §3.1). https://myamazonguy.com/news/amazon-services-business-solutions-agreement/
- Consequences of non-compliance not itemized for Section 19 in any reachable source; do not assume graduated warnings. UNKNOWN (spapi-writes.md §3.7).
- DPP/AUP update effective Nov 25 2025: "Developer" renamed "Solution Provider"; existing integrations "may require changes to security controls". REPORTED (spapi-writes.md §2.4). https://developer-docs.amazon.com/sp-api/changelog/updates-to-the-data-protection-policy-and-acceptable-use-policy
- SP-API developer fees ($1,400/yr + overage, Jan-Apr 2026) were cancelled entirely May 12 2026. REPORTED (supply-finance.md §3). https://novadata.io/resources/news/amazon-cancels-sp-api-fees-may-2026
- Private/self-authorized SP-API app: Professional account, Primary User, register in Solution Provider Portal (~20 min identity verification), add client, pick roles, self-authorize -> refresh token (new token each repeat); app stays draft forever; ordinary roles approved "within a few working days". REPORTED (spapi-writes.md §2.1). https://developer-docs.amazon.com/sp-api/docs/self-authorization
- Non-restricted roles: Pricing, Product Listing, Inventory & Order Tracking, Finance & Accounting, Brand Analytics -> no DPP Section 2 pentest/architecture review. REPORTED (spapi-writes.md §2.2-2.3). Amazon Fulfillment role restricted-status UNKNOWN; Buyer-Seller Messaging likely restricted; Direct-to-Consumer Shipping explicitly restricted (VERIFIED via https://github.com/amzn/selling-partner-api-docs/issues/2390 : role denied 6-7 times over 5 months).
- SP-API Guard: free self-assessment scanner vs DPP controls, 24h report; not a mandatory gate. REPORTED. https://developer.amazonservices.com/tools/selling-partner-api-guard
- Amazon Seller Assistant (agentic) runs on Bedrock with "a mix of Amazon Nova and Anthropic Claude models"; live for all US 3P sellers free; Canvas live US/UK; Canada availability UNKNOWN; NO API/MCP surface (VERIFIED-by-absence). (spapi-writes.md §4). https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-agentic-ai ; auto-approve mode for routine tasks slated Q2 2026 (advertising.md §2, REPORTED).

### 1.2 SP-API capabilities (first-party, free)
- Notifications API model (VERIFIED from raw.githubusercontent.com/amzn/selling-partner-api-models/main/models/notifications-api-model/notifications.json): exactly two destination types, `sqs` (needs ARN) or `eventBridge` (accountId, name, region); `createSubscription` per notificationType; `sendTestNotification` exists; `EventFilter.eventFilterType` enum = ANY_OFFER_CHANGED, ORDER_CHANGE, SHIPMENT_TRACKING_MILESTONE_CHANGED; ORDER_CHANGE sub-filter enum = BuyerRequestedChange, DeliveryTipChange, OrderStatusChange. (spapi-writes.md §5.1)
- Neither notification destination is "no AWS account"; push notifications require an AWS account either way. VERIFIED mechanics (spapi-writes.md §5.3).
- ANY_OFFER_CHANGED: `processingDirective` throttles to 5- or 10-minute cadence, filter by marketplace; this is the hijacker/Buy Box signal. VERIFIED (catalog-intel.md §2, §3.3). https://docs.developer.amazonservices.com/en_UK/notifications/Notifications_AnyOfferChangedNotification.html
- LISTINGS_ITEM_ISSUES_CHANGE: v1.0 payload sunset (no new subs after Aug 14 2026; existing stop Aug 26 2026); use payload version 2023-12-13; flags LISTING_SUPPRESSED / ATTRIBUTE_SUPPRESSED / CATALOG_ITEM_REMOVED. VERIFIED via changelog excerpt (catalog-intel.md §2).
- ACCOUNT_STATUS_CHANGED (NORMAL/AT_RISK/DEACTIVATED) and PRICING_HEALTH (offer loses Featured Offer eligibility on price) notification types. REPORTED (customer-health-runtime.md B5). No SP-API field reads the Account Health Rating itself. UNKNOWN.
- Brand Analytics via SP-API Reports (Brand Registry + Brand Analytics role): Search Query Performance + Search Catalog Performance programmatic since Feb 26 2025; Top Search Terms; Market Basket; Repeat Purchase; GET_BRAND_ANALYTICS_SEARCH_TERMS_REPORT (schema update Mar 15 2023). VERIFIED via changelog (catalog-intel.md §2; advertising.md §5). https://developer-docs.amazon.com/sp-api/changelog/update-added-new-search-query-performance-and-search-catalog-performance-analytics-report-types
- Product Pricing API v2022-05-01: `getFeaturedOfferExpectedPriceBatch` (FOEP = price at/below which own SKU expected to win Buy Box), up to 40 SKUs/call, all marketplaces except Japan; `getCompetitiveSummary` expanded Jan 2025; dynamic usage plan. VERIFIED (catalog-intel.md §3.2). https://developer-docs.amazon.com/sp-api/changelog/update-product-pricing-api-v2022-05-01-now-supports-the-getfeaturedofferexpectedpricebatch-operation-in-all-marketplaces-except-japan
- SP-API "Manage Automated Pricing Rules": associate SKU to strategy (featured-offer-matching, lowest-price, external-price, sales-based, custom) with `minimum_seller_allowed_price`/`maximum_seller_allowed_price` in the same PATCH; Amazon executes 24/7; one rule per SKU; no B2B. VERIFIED (catalog-intel.md §4.1). https://developer-docs.amazon.com/sp-api/changelog/new-automated-pricing-rules-for-sp-api
- Listings Items API: JSON Patch (add/replace/delete whole attributes only; no intra-attribute patch); payload must match Product Type Definitions JSON Schema per product type + marketplace + seller; preview-errors endpoint exists. VERIFIED (catalog-intel.md §5.2). https://developer-docs.amazon.com/sp-api/docs/partially-update-a-listing
- Product Type Definitions are per marketplace; CA = A2EUQ1WTGCTBG2, US = ATVPDKIKX0DER; food attributes ingredients / allergen_information / expiration_type / country_of_origin. VERIFIED (catalog-intel.md §5.2-5.3).
- Catalog Items API (no Brand Registry gate), A+ Content Management API (A+ role). VERIFIED (catalog-intel.md §2). https://developer-docs.amazon.com/sp-api/docs/catalog-items-api
- No SP-API "submit reimbursement claim" write endpoint; reimbursement events read-only via Finances API; case creation is Seller Central UI only. UNKNOWN/likely absent (spapi-writes.md §1.3; supply-finance.md §3).
- No SP-API endpoint for Manage Your Experiments, Listing Quality Dashboard score, Enhance My Listing, Creative Studio, Project Zero, Transparency, Vine enrollment. UNKNOWN/likely none (catalog-intel.md §4.3, §5.1, §6.1, §6.4).
- Messaging API v1: order-tied, allowed message types restricted; Solicitations API: one fixed-template review+feedback request per order, no custom copy. REPORTED (customer-health-runtime.md A2).
- Returns report GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA with detailed-disposition and reason codes; `listReturnReasonCodes` endpoint. REPORTED (customer-health-runtime.md A3).
- No official Amazon review-text API has ever existed; since Nov 5 2024 full review history behind login wall; since Feb 26 2025 even "8 most recent" needs a session cookie; only 3-8 featured reviews + aggregates scrapable; scraping violates Conditions of Use (civil). VERIFIED (catalog-intel.md §3.6). https://tracefuse.ai/blog/is-there-an-amazon-api-to-retrieve-product-reviews/
- Listing Quality Dashboard updated Jul 1 2026: six components (image quality, title compliance, bullet completeness, A+ presence, review-velocity health, attribute completeness); now affects organic rank; no API. VERIFIED direction (catalog-intel.md §6.1). https://novadata.io/resources/news/amazon-listing-quality-dashboard-rollout-july-2026

### 1.3 Amazon Ads
- Amazon Ads MCP Server open beta since Feb 2 2026, Amazon-hosted, translates prompts into Ads API calls. VERIFIED via multiple press (advertising.md §1). https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta
- 50+ tools with prefixes cp_/sp_/dsp_/amc_/ac_; complete tool manifest UNKNOWN. REPORTED (advertising.md §1).
- Requires an existing Ads API LWA credential set (approval 1-3 business days); no separate MCP gate; DSP tools need DSP API approval (~$50K+/yr spend, 1-2 weeks); AMC tools need a provisioned AMC instance. REPORTED (advertising.md §1).
- Canada implicitly covered (NA region; Amazon's example expands a US+CA campaign); explicit marketplace allow-list UNKNOWN. REPORTED.
- Rate limits for hosted MCP: UNKNOWN. Report generation can take 10-15 min. REPORTED.
- MCP sees only ad data: no inventory, no landed cost/fees, no Buy Box. REPORTED (advertising.md §1). https://sentrykit.com/blog/amazon-ads-mcp-server-sellers/
- Amazon internal testing: agents pulled excessive AMC data and called deprecated endpoints. REPORTED.
- Third-party wrappers (marketplaceadpros/amazon-ads-mcp-server, VERIFIED repo; ppcprophet, KuudoAI, adspirer, Imsamiullah09 REPORTED) proxy through their own SaaS credentials; not the official server.
- Ads Agent (unBoxed Nov 2025) and Creative Agent are in-console UI features, not callable. REPORTED (advertising.md §2).
- Amazon Marketing Stream: hourly push via SQS/Firehose, needs AWS; not an MCP tool. REPORTED (advertising.md §3).
- Walmart Connect Ads API restricted to Walmart Connect Partner Network (WCPN) members; no official Walmart MCP; Vinkius (8 tools, proxied creds) and Intentwise Walmart MCP are third-party. REPORTED (advertising.md §7).
- Pacvue is the only PPC platform with an official MCP (May 14 2026), priced for $100K+/mo. REPORTED (advertising.md §4).

### 1.4 Anthropic (legal/product) — see §4 for full text
- Legal-and-compliance page VERIFIED (code.claude.com/docs/en/legal-and-compliance): Agent SDK developers "should use API key authentication"; Anthropic "does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, or Max plan credentials on behalf of their users"; does NOT "prevent an end user from signing in to the unmodified Claude Code binary with their own Claude subscription". (subscription-clis.md §1.2-1.3)
- `claude setup-token` mints a one-year OAuth token -> `CLAUDE_CODE_OAUTH_TOKEN`; Pro/Max/Team/Enterprise; "can only make model requests... can't establish Remote Control sessions or fetch claude.ai connectors. MCP servers you configure locally still work." VERIFIED. https://code.claude.com/docs/en/authentication
- Auth precedence: cloud creds > ANTHROPIC_AUTH_TOKEN > ANTHROPIC_API_KEY > apiKeyHelper > CLAUDE_CODE_OAUTH_TOKEN > profile > /login. A stray ANTHROPIC_API_KEY silently overrides the subscription token. VERIFIED (subscription-clis.md §1.3). `--bare` mode ignores CLAUDE_CODE_OAUTH_TOKEN.
- Usage Policy: "Advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK"; Anthropic may enforce without notice. VERIFIED wording; whether 8 daily cron departments count as "ordinary" is UNKNOWN.
- Routines (research preview) VERIFIED at https://code.claude.com/docs/en/routines : Pro/Max/Team/Enterprise; triggers Scheduled (1-hour minimum), API (per-routine /fire bearer endpoint; fired text arrives as untrusted `<routine-fire-payload>`), GitHub events; run on Anthropic cloud (or self-hosted env); "no permission-mode picker and no approval prompts"; "draw down subscription usage the same way interactive sessions do" + separate daily run-start cap; requires claude.ai subscription login (Console API keys cannot use /schedule); all connected MCP connectors included by default; overage needs "usage credits". (subscription-clis.md §1.4; customer-health-runtime.md C7)
- Claude Code on the web: cloud sessions persist, steerable from Claude mobile app. VERIFIED. https://code.claude.com/docs/en/claude-code-on-the-web
- Claude Code mobile push approvals since v2.1.110 (Apr 16 2026). VERIFIED (interface-knowledge.md §1). https://code.claude.com/docs/en/mobile
- Claude Code auto memory since v2.1.59 (Feb 26 2026) at ~/.claude/projects/<project>/memory/MEMORY.md; local, Claude-Code-specific, not synced. VERIFIED. https://code.claude.com/docs/en/memory
- Claude Code reads CLAUDE.md, not AGENTS.md natively; import via `@AGENTS.md`. REPORTED (interface-knowledge.md §4).
- Claude Code `/sandbox`: Seatbelt on macOS, bubblewrap on Linux, kernel-enforced FS/exec/network allow-lists. VERIFIED via write-ups; CVE-2026-25725 exists against @anthropic-ai/claude-code (hosting-ops.md §4.2). https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2026-25725
- Claude Code native/npm installs auto-update by default; pin with `claude install <version>` AND `DISABLE_AUTOUPDATER=1`; v2.1.113 (Apr 17 2026) switched to native binary. VERIFIED (hosting-ops.md §6.1).
- No RFC 8628 device-code flow for Pro/Max (issues #22992, #42965 open). REPORTED (hosting-ops.md §1.0).
- Managed Agents VERIFIED (platform.claude.com/docs/en/managed-agents/overview, multiagent-orchestration): beta header `managed-agents-2026-04-01`; scheduled deployments; vaults (session-scoped env vars; mcp_oauth background refresh); file-based memory stores + "Dreaming"; multiagent: up to 20 unique roster agents, one level deep, max 25 concurrent threads, typed thread_message events, session budgets, one advisor. Pricing REPORTED: tokens + $0.08/active session-hour. (customer-health-runtime.md C9)
- Claude Agent SDK subagents: fresh isolated context, only final message returns. REPORTED (customer-health-runtime.md C10).
- Anthropic engineering guidance VERIFIED: "Building Effective Agents" (5 workflow patterns; simple composable patterns win) https://www.anthropic.com/engineering/building-effective-agents ; multi-agent research system: orchestrator-workers, 90.2% gain, ~15x token cost, token usage explains ~80% of variance https://www.anthropic.com/research/multiagent-systems ; shared-state vs message coordination, Claude Code Agent Teams use a shared file https://claude.com/blog/multi-agent-coordination-patterns (frameworks-standards.md §7).
- Anthropic pricing VERIFIED (claude-api skill): Sonnet 5 $2/$10 per MTok (until Aug 31 2026; REPORTED $3/$15 from Sept 2026 in grok.md), Opus 5 $5/$25. (subscription-clis.md §7.2)
- Agent Skills SKILL.md opened Dec 18 2025 as vendor-neutral standard (agentskills.io); 32 tools by Mar 2026, ~40 by Jun 2026. VERIFIED (frameworks-standards.md §3; subscription-clis.md §6.2). https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md
- MCP spec 2026-07-28: stateless core, removed initialize/initialized handshake and Mcp-Session-Id (SEP-2567), OAuth 2.1, RFC 9207, DCR deprecated for CIMD. VERIFIED. https://modelcontextprotocol.io/specification/2026-07-28 (frameworks-standards.md §3; hosting-ops.md §6.1)

### 1.5 OpenAI, xAI, Google — see §4 for full text
- Codex CLI Apache-2.0, `codex exec --json` JSONL events, `codex login --device-auth`, MCP + AGENTS.md ("untrusted projects no longer supply project-level AGENTS.md"). VERIFIED repo / REPORTED docs (subscription-clis.md §2).
- OpenAI reinstated 5-hour Codex limit for Plus on Aug 25 2026. REPORTED (9to5mac). Pro tiers ~5x/20x Plus. REPORTED.
- Grok Build: beta May 14 2026 (SuperGrok Heavy), GA ~Aug 7 2026, open-sourced Apache-2.0 Jul 15 2026 after the exfiltration incident; `grok -p --output-format streaming-json`; `grok login --device-auth` VERIFIED (github.com/xai-org/grok-build auth docs, hosting-ops.md §7.1).
- Grok Build exfiltration (Jul 2026, researcher "cereblab", mitmproxy): 192 KB task -> 5.10 GiB uploaded to GCS bucket `grok-code-session-traces`, full git history incl. `.env`, privacy toggle ineffective; fix is a server-side flag, code path still present. REPORTED high-confidence, 6+ outlets (subscription-clis.md §3.4).
- Gemini CLI stopped serving free / Google AI Pro / Ultra individual accounts on Jun 18 2026 (announced I/O May 19 2026); Code Assist Standard/Enterprise unaffected; successor Antigravity CLI (`agy`) closed-source. VERIFIED quota doc + REPORTED shutdown (subscription-clis.md §4). https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/quota-and-pricing.md
- Google banned proxying Gemini CLI OAuth via third-party tools Feb 2026, enforced Mar 25 2026 with mass account suspensions incl. paying Ultra subscribers. VERIFIED via multiple 2026 reports (orchestrators.md §6).

### 1.6 Third-party tool facts
- DataDoe: see §3.
- Helium 10 official MCP (2026): OAuth, read-only, on-demand, bundled with Diamond plan; REST API Enterprise-only. VERIFIED via excerpts (catalog-intel.md §1.1). https://github.com/helium10/Helium10-MCP ; https://kb.helium10.com/hc/en-us/articles/51580564409883-Getting-Started-with-Helium-10-MCP
- Helium 10 prices rose Apr 2026: Platinum $129/mo; Diamond $279/mo annual (customer-health-runtime.md says Diamond $359/mo, 200 ASINs); Starter discontinued. REPORTED.
- Keepa domain code `ca: 6` (full amazon.ca coverage). VERIFIED. https://keepa.com/api-docs/ ; entry EUR 49/mo for 20 tokens/min, no free tier. REPORTED. https://revenuegeeks.com/software/keepa/api
- Jungle Scout API only on Growth Accelerator / Brand Owner+CI plans, $29-199/mo add-on, $0.05/request overage, 10 marketplaces incl. CA. VERIFIED vendor page. https://www.junglescout.com/products/jungle-scout-api/
- Nova Analytics (novadata.io): read-only MCP for Claude/ChatGPT/Gemini, 21 marketplaces, hourly refresh; from $29/mo annual, 14-day trial. VERIFIED vendor (supply-finance.md §1). https://novadata.io/amazon-mcp-tools
- Sellerboard: no public API; scheduled CSV/Excel email exports ("Automation" page); Walmart dashboard live; ~$15-19/mo. V-adj/REPORTED (supply-finance.md §1). https://sellerboard.com/walmart
- Intuit official open-source QuickBooks Online MCP server (Oct 2025): 29 entities CRUD, 11 reports. VERIFIED. https://github.com/intuit/quickbooks-online-mcp-server ; Xero has no official MCP as of Apr 2026.
- A2X: Amazon plan from $29/mo, Walmart plan from $79/mo; posts to QBO/Xero/NetSuite/Sage. VERIFIED (supply-finance.md §4).
- Threecolts Seller 365: reimbursements cover FBA and Walmart WFS; from $69/mo. VERIFIED vendor page. https://www.threecolts.com/seller-365
- Getida: 25% commission, no monthly fee, audits trailing 18 months. VERIFIED-by-multiple. https://revenuegeeks.com/software/getida
- Amazon reimbursement basis = manufacturing cost since Mar 31 2025; auto-reimbursement since Jan 15 2025; 60-day claim window for FC lost/damaged. VERIFIED-by-multiple / REPORTED (supply-finance.md §3). https://www.carbon6.io/blog/amazon-reimbursement-policy/
- SellerSonar REST API + webhooks, Enterprise-only. VERIFIED via excerpts. https://sellersonar.com/api/
- FeedbackWhiz, Sellerise, Helium 10 Alerts, Jungle Scout Review Automation, SageMailer, AMZAlert: no public API (REPORTED); FeedbackFive UNKNOWN. (customer-health-runtime.md A1)
- Vine: Pro plan + Brand Registry + FBA + <30 reviews; cap 30 units; $0 enrollment for products under $100 from Mar 2026. REPORTED (customer-health-runtime.md A4).
- Flexport AI agents manage 40% of forwarding ops (Mar 2026); Freightos free landed-cost calculator + developer API. VERIFIED vendor (supply-finance.md §5). https://developers.freightos.com/freight-tools
- FDA Food Facility Registration biennial renewal Oct 1-Dec 31 2026; missing it cancels registration. VERIFIED. https://www.registrarcorp.com/blog/food-beverage/food-facility-registration/must-fsvp-food-importers-register-fda/ ; Prior Notice 2-8h before arrival; FSVP ongoing. V-adj.
- CFIA SFC licence required before border presentation; manufactured foods sector since Jul 15 2020; apply via My CFIA. VERIFIED. https://www.cbsa-asfc.gc.ca/publications/cn-ad/cn24-03-eng.html
- GST/HST: Amazon collects for non-registered sellers since Jul 1 2021; CAD 30,000 threshold is worldwide sales over 4 rolling quarters. VERIFIED-multiple (supply-finance.md §4; customer-health-runtime.md B6).
- US sales tax: Amazon marketplace facilitator in ~45 states; income/franchise tax nexus from FBA inventory is separate; consider protective Form 1120-F + Form 8833. REPORTED (customer-health-runtime.md B6).
- CA bilingual (EN/FR) food labelling legally required; Quebec Charter may require French prominence; metric units; separate NFT format vs US. VERIFIED direction (catalog-intel.md §5.3).
- Expiration-dated FBA inventory pulled 50 days before expiry (US policy). REPORTED.
- Walmart: luke-nielsen/walmart-mcp VERIFIED (mp_update_inventory, mp_update_price, mp_acknowledge_order; no WFS, no Connect; 0 stars). https://github.com/luke-nielsen/walmart-mcp
- Telegram Bot API: inline keyboards + CallbackQuery; getUpdates long-polling vs HTTPS webhook; 4096-char message limit counted after entity parsing. VERIFIED. https://core.telegram.org/bots/api
- WhatsApp Cloud API per-message billing since Jul 1 2025; from Oct 1 2026 service replies inside the 24h window billed too. VERIFIED/REPORTED. Baileys: bans in 2-8 weeks, `lotusbail` npm exfiltrated sessions (Apr 2026). VERIFIED (interface-knowledge.md §1).
- Cloudflare Access free for up to 50 users; cannot protect default *.pages.dev (custom domain needed). VERIFIED. Tailscale personal free tier 6 accounts. VERIFIED (interface-knowledge.md §3).
- healthchecks.io free: 20 checks, 3 months history. VERIFIED. https://healthchecks.io/docs/
- Backblaze B2 $6.95/TB/mo, first 3x stored volume egress free. VERIFIED (hosting-ops.md §5.2).
- Hetzner CX22 ~EUR 4.35-4.59/mo after Apr 2026 increase; DigitalOcean from $4/mo per-second billing since Jan 1 2026. VERIFIED-ish (hosting-ops.md §1.2).
- Mac mini M4 idle 4-6W VERIFIED (Jeff Geerling); base price $799 Jun 2026 then $899 with M5 Pro/M6 refresh announced Aug 25 2026, ships Sep 22 2026. REPORTED.
- Paperclip: MIT, Node>=24.11, pnpm>=9.15, Postgres, S3-compatible storage; ~79.9k stars; `claude_local` honours CLAUDE_CODE_OAUTH_TOKEN; `codex_local` inherits host ChatGPT login. VERIFIED (orchestrators.md §1). https://github.com/paperclipai/paperclip
- OpenClaw: MIT, ~389k stars; CVE-2026-25253 CVSS 8.8 one-click RCE even on localhost (patched v2026.1.29); 30k+ then 258,305 exposed instances (Censys, Mar 2026); ClawHavoc 341 -> 824+ malicious skills. VERIFIED/REPORTED (orchestrators.md §2; hosting-ops.md §4.3).
- Hermes Agent: MIT, ~240.5k stars, native MCP, cron, Telegram; claude-code subprocess provider in open issues #48320/#78563/#47199. VERIFIED (orchestrators.md §3).
- NanoClaw: container per context; ANTHROPIC_AUTH_TOKEN API key only. VERIFIED. https://github.com/dh7/NanoClaw
- n8n: Sustainable Use License; native MCP node; "Send and Wait for Approval" Telegram/Slack node since ~v2.6 (Jan 2026). VERIFIED/REPORTED (orchestrators.md §4).
- LiteLLM documented Claude Max OAuth forwarding tutorial VERIFIED https://docs.litellm.ai/docs/tutorials/claude_code_max_subscription (but conflicts with Anthropic policy above).
- Langfuse MIT core, acquired by ClickHouse Jan 16 2026. VERIFIED. DBOS MIT library over Postgres. VERIFIED. Temporal self-host ~$3,200/mo + ~0.4 FTE. REPORTED.
- A2A v1.0 Apr 2026, 150+ orgs, Linux Foundation -> Agentic AI Foundation. VERIFIED. AGENTS.md donated to Agentic AI Foundation Dec 2025, 60k+ repos. VERIFIED.
- 12-Factor Agents (HumanLayer) factors 5/6/7/12 VERIFIED. https://github.com/humanlayer/12-factor-agents
- GitHub Agentic Workflows (gh-aw) technical preview Feb 2026: never merges automatically. VERIFIED. https://github.com/github/gh-aw
- Memory provenance research: arXiv 2606.04990 (source type, timestamp, authoring agent, evidence, confidence, update history). VERIFIED. Mem0 confidence-score / decay guidance. VERIFIED (interface-knowledge.md §6).

---

## 2. Tool decisions already made per department (buy/skip, why, price)

### Advertising (advertising.md)
- BUY: official Amazon Ads MCP Server (free; needs Ads API LWA creds) as the only ads execution MCP. Do not use third-party credential-proxying wrappers.
- BUY (free): weekly SP-API Brand Analytics sync (SQP, Search Catalog Performance, Search Terms).
- DEFER: Amazon Marketing Stream (AWS SQS/Firehose); DSP/AMC tools (>$50K/yr gate).
- SKIP: Pacvue ($100K+/mo scale, MCP May 2026), Quartile ($895-2,000+/mo), Intentwise (~$1,000/mo), Adbrew (~$799), Teikametrics (~$599+3%), Xnurta (~$750), Perpetua ($250-550), Scale Insights (~1%), m19 ($59/$479+3%), Ad Badger — all "second closed brain" risk. Helium 10 Adtomic ($229 + 2% over $5K) noted as good fit but not bought.
- SKIP as agent sources: Helium 10 Enterprise API, Jungle Scout, DataDive ($149 Standard) — API is upper-tier priced; use as manual launch research at most. SKIP ZonGuru/Nozzle rank trackers.
- NO Walmart Connect MCP yet; when needed route via a WCPN partner (Perpetua/Teikametrics/Pacvue) rather than Vinkius/Intentwise proxies.
- Playbook to encode: 4-campaign-per-hero-SKU structure (Auto+Broad discovery, Phrase, Exact rank, Branded defense, ASIN conquest); branded/non-branded never share a campaign; negatives only above statistical threshold; 10-day history before dayparting/rules; per-SKU target ACOS from contribution margin; budget split ~20-25/25-30/45-55; bid/budget change caps (+25-30% per action), one change per target per 24-48h.

### Supply Chain (supply-finance.md)
- BUY: Sellerboard $15-19/mo (profit cross-check; Walmart-ready; ingest via scheduled email CSV).
- TRIAL: Nova Analytics MCP (free promo / $29/mo) as agent-native cross-check.
- BUY: Getida or Refunds Manager (0 fixed, 25% of recovered). Seller Investigators same terms.
- BUY/INTEGRATE: Freightos landed-cost API (free calculator) for live tariff-adjusted landed cost.
- BUY (free): Google Sheet + Sheets MCP as human-editable supplier directory.
- MANDATORY: CFIA SFC licence; FDA FFR (renew Oct-Dec 2026), Prior Notice, FSVP.
- SKIP NOW: SoStocked (~$250/mo), Inventory Planner ($300-500), Cin7 ($349-599+), Flieber ($299), Fabrikatör, Prediko (Amazon connector "coming soon"), SkuVault (WMS), Helium 10 Inventory (needs $129-279 suite). WATCHLIST: RestockPro (~$99/mo) once SKU x marketplace pairs exceed ~100-150 (about US launch).
- SKIP: Anvyl, Sourcify, Zoho Inventory; Airtable/Notion as new paid infra.
- WATCH: Flexport (fit for small volume UNKNOWN); Threecolts Seller 365 ($69-79) at Walmart launch.

### Finance (supply-finance.md)
- BUY: QuickBooks Online Plus $99/mo + Intuit official MCP (first-party MCP outweighs Xero's better multi-currency/GST fit). Alternative: Xero Growing $47/mo + community MCP.
- BUY: A2X Amazon $29/mo (+$79/mo Walmart plan later). WATCHLIST: Taxomate Multi (unlimited channels; Basic $52, Essential $92, Pro $220). Synder pricier ($65/$115/$275). Link My Books: CAD not listed in calculator, verify.
- MANDATORY: GST/HST registration (worldwide threshold already passed); confirm number on file in Seller Central.
- SKIP: Float ($49-179), Fathom, Pulse ($29) — build cash forecast from own data + QBO MCP.
- FX handling: UNKNOWN, needs cross-border CPA.

### Catalog & Brand (catalog-intel.md)
- BUY (free, mandatory): SP-API Catalog Items, A+ Content Mgmt, Product Type Definitions, Listings Items; Brand Analytics reports; LISTINGS_ITEM_ISSUES_CHANGE + ANY_OFFER_CHANGED notifications.
- BUY: Helium 10 Diamond with MCP (~$200-280/mo REPORTED; confirm) — only keyword tool with official agent-native MCP.
- SKIP: Jungle Scout, DataDive (repackages Keepa+JS), SmartScout ($29 base + Enterprise API), ZonGuru, Merchant Words, Scale Insights, SellerApp (unknown).
- SKIP as agent input: Enhance My Listing, Creative Studio (UI only). Manage Your Experiments: manual quarterly on top 3-5 SKUs.
- SKIP for now: SellerSonar (Enterprise API duplicates free notifications).

### Pricing & Market Intel (catalog-intel.md)
- BUY (free): Product Pricing API FOEP + getCompetitiveSummary; SP-API Automated Pricing Rules for the pre-approved band; ANY_OFFER_CHANGED.
- BUY: Keepa API entry ~EUR 49/mo (20 tokens/min); community MCP purahmanian/keepa-mcp exists (REPORTED).
- SKIP: repricers Aura (~$55+), Informed.co ($99/$147), Feedvisor ($100-1,500+), RepricerExpress/BQool/Seller Snap; Amazon dashboard Automate Pricing (limited logic).
- DEFER: Helium 10 Market Tracker (MCP exposure UNKNOWN).
- SKIP: review scraping (login wall + ToS), FeedbackWhiz, Sellerise.
- Estimated incremental spend Catalog+Pricing: ~$65-350/mo.

### Customer & Reputation (customer-health-runtime.md)
- SKIP third-party review/alert tools as agent dependencies (no APIs). Use first-party data + PRICING_HEALTH.
- USE Solicitations API directly or cheapest wrapper (SageMailer $10-25/mo, FeedbackFive $24-199); never Messaging API for marketing.
- Gate buyer_message / review_solicitation / vine_enrollment behind approval.
- BUILD returns_daily sync joined to supplier shipments for quality loop.

### Account Health & Compliance (customer-health-runtime.md)
- SUBSCRIBE ACCOUNT_STATUS_CHANGED as critical alert. AHR itself manual.
- Never auto-submit appeals/POA/IP responses; agent drafts, human submits.
- Engage cross-border accountant before Jan 2027 (1120-F decision). TaxJar (~$19/mo) / Avalara only for non-marketplace nexus gap.

### Runtime (customer-health-runtime.md C7-C11, V2 design)
- V2 design (Sep 2 2026): Claude Code on the web + Routines as runtime v1; Managed Agents as graduation path; Amazon Ads MCP, DataDoe reads, a vetted SP-API write MCP with vault credential, Walmart MCP later, Gmail, web; data bought = Sellerboard, Helium 10, Keepa; no warehouse; weekly KPI CSV in repo. Cost ~$350-800/mo (Claude Max $200, API $0-300, Sellerboard $19-39, Helium 10 $99-229, Keepa ~$20, DataDoe/write MCP TBD).
- V2 open decisions for Rami: Routines-first vs Managed Agents day one; which MCP holds SP-API write creds; TZ/brief time; account facts (NA unified, Brand Registry CA/US, Walmart CA/US, Pro plan); guardrail numbers; repo name.

---

## 3. DataDoe (datadoe.md; corroborated in spapi-writes.md §1.2, grok.md §5, frameworks-standards.md §3)

Identity
- Built by Deltologic (Poland, founded 2020, ~30 engineers); founders Kris Krokos, Jakob Wolitzki. REPORTED.
- Started 2025 as chat "AI Copilot/Sidekick", pivoted 2026 to "Amazon data and action layer for AI" (press release NatLawReview/MarTechSeries). REPORTED.
- Claims Amazon-audited SP-API developer, SOC 2 Type II, cleared Amazon DPP assessment. REPORTED (compare page dated Jun 18 2026).
- No independent reviews (Reddit/G2/Trustpilot/PH) found. UNKNOWN. Name collisions: Dataddo, Datadog, DataDome.

MCP tool contract (VERIFIED from https://github.com/Deltologic/datadoe-mcp — a No-Op schema stub, `MCP_SERVER_VERSION = '0.4.0'`, MIT, 1060-line src/index.ts, "exposing the schema of DataDoe MCP to registries")
- Endpoint `https://mcp.datadoe.com/mcp/v1`, HTTP Streamable, static key header `datadoe-mcp-key` (created at app.datadoe.com/integrations/mcp). Hosted only; DataDoe owns SP-API registration/OAuth/refresh tokens/rate limits. Not self-hostable.
- Setup: `claude mcp add datadoe --transport http --url https://mcp.datadoe.com/mcp/v1 --header "datadoe-mcp-key: <KEY>"`; guides for Cursor, VS Code/Copilot, Codex CLI, Gemini CLI, ChatGPT, n8n, NanoClaw, CrewAI, OpenAI Agents SDK, Claude Agent SDK, OpenClaw, Gumloop, Hermes, Office+Claude (datadoe.com/hub/docs).
- Account: `sellers_and_vendors_list` (filter by name/marketplace), `organization_and_subscription_details_get`.
- Data (async export-job model, not per-entity tools): `exports_sources_get` (search templates: orders, sales & traffic, ads, inventory, listings, settlements, returns, brand analytics), `exports_create` (SQL-like filter groups, GROUP BY, sum/avg/count/countDistinct/min/max, DAY/WEEK/MONTH intervals, CSV/JSON), `exports_get` (poll), `exports_list`, `exports_raw_url_get` (one-time URL), `exports_raw_download` (inline), `exports_delete`.
- Files: `files_create` (base64; listing images, A+), `files_list`, `files_get`, `files_download_url_get`, `files_delete`.
- Docs: `datadoe_user_docs_table_of_contents_get`, `datadoe_user_docs_page_get`.
- COGS: `cogs_upsert`, `cogs_delete` (feeds P&L). Vendor codes: `vendor_code_upsert`, `vendor_code_delete`.
- Plugins: `plugins_get`, `plugins_memories_create`, `plugins_memories_edit`, `plugins_skills_get`, `plugins_files_get` — "Memories" (user/org notes), "Skills" (SKILL.md bundles from Skill Hub), "Files".
- Actions: `actions_details_schema_get`, `actions_start` (supports `dryRun=true`), `actions_get` (poll), `actions_list` (audit history).

Write capabilities (VERIFIED README)
- `AMAZON_LISTINGS_UPDATE` (title, bullets, description, price, generic keyword, item-type keyword); `AMAZON_ORDERS_CANCEL`; `AMAZON_ORDERS_CONFIRM_SHIPMENT` (tracking); Ads actions add/update/remove/find campaigns, ad groups, targets, ads across SP/SB/SD/TV/DSP. Marketing adds: reprice, edit images, publish A+, negatives, bids, launch SP campaigns (REPORTED).
- Safety: every action type disabled by default, enabled per type in Settings > Actions; disabled types allow dry-run, reject live; audit via `actions_list`. "Every change is dry-run first, nothing goes through without your approval" (REPORTED marketing).
- Token cost: 2 AI tokens per <=100 entities, +1 per extra 100 (VERIFIED).
- NOT found: FBA inbound shipment creation, feed uploads, reimbursement cases, Vendor PO ack, review requests. UNKNOWN/likely absent.

Data coverage
- VERIFIED: Seller Central SP-API (FBA+FBM), Vendor Central (Retail Analytics, Sales Diagnostic, Demand Forecast, EDI), Ads API (SP/SB/SD/Sponsored TV/DSP incl. search terms), Brand Analytics (SQP, search terms, market basket, repeat purchase, demographics). Marketplaces US, UK, DE, FR, IT, ES, CA, AU, JP, MX "and more" (pricing page says 23, enterprise page 21 — inconsistent).
- Entities: orders/line items, order performance, sales & traffic (sessions, page views, CVR), refunds; ads with ACoS/ROAS/impression share; FBA inventory, restock recs, stranded, inventory age, units at risk; ASIN catalog, attributes, Buy Box ownership, variations; settlements, fees, reserves, reimbursements, deposits; returns + reasons; Brand Analytics. Changelog adds FBA Inbound Shipments, Subscribe & Save, Promotion & Coupon Performance, raw Ads and DSP tables. "100+ tables" incl. gated PII tables. REPORTED. Schema: datadoe.com/hub/data-scheme.
- REPORTED: DSP raw reports; Amazon Marketing Stream + SP-API order notifications; buyer-seller messages and review velocity (Deltologic's own comparison). UNKNOWN: AMC; Walmart/Shopify/TikTok Shop (marketing pages only, not in README).

Non-MCP features (all REPORTED)
- BigQuery: dedicated dataset in your own GCP project, retained from connection day, refreshed daily.
- REST API + typed npm SDK.
- Built-in KPI/P&L dashboards ("true margin after fees, ads and COGS"); PowerBI/Tableau/Looker/Sheets/Excel connectors; recurring exports.
- Scheduled AI prompts on Home; async agents for anomaly alerts, daily revenue digests, restock alerts, Buy Box loss pings; Slack alerts.
- Reorder/restock forecaster (lead times, seasonality, MOQs); fee+COGS-aware repricer; FBA reimbursement audit agent — read like Skill Hub workflows; depth UNKNOWN.
- Skill Hub: 47 pre-built skills/workflows with preview, dry-run, audit-log defaults (frameworks-standards.md could not find "DataDoe Skill Hub" in any source and flagged UNKNOWN; datadoe.md verified `plugins_skills_get` exists).
- Enterprise tier: no rate limits, SLA, account manager, multi-seat, 21 marketplaces.

Freshness / limits (REPORTED)
- "Continuous sync on most feeds"; DataDoe polls and caches in its warehouse; sub-second query on pre-synced data; initial backfill up to 735 days; freshness/sync-failure alerts. No independent lag benchmark.
- Ad data retention (Deltologic comparison, single source): SP keyword-level ~95 days, SB/SD ~60 days.
- Standard plan throttled by token/row caps, not RPS; Amazon 429s absorbed by DataDoe.

Pricing (REPORTED https://www.datadoe.com/pricing)
- Standard $97/mo flat, 14-day trial no card, cancel anytime: MCP + REST + BigQuery, 100+ tables, 2,000 AI action tokens/mo, 10,000,000 data rows, 1 seat. Enterprise custom. Overage past 10M rows / 2,000 tokens: UNKNOWN. Whether exports consume the token pool: UNKNOWN. Per-marketplace/per-account fee: none found.

Architectural notes recorded
- Approval loop lives inside DataDoe's action model (per-type enable + dryRun), audit trail in DataDoe not in the repo; datadoe.md's verdict (v1 framing) was "read-only"; spapi-writes.md called it "most credible hosted write option" but lacking inbound/reimbursements; V2 design uses it for Seller/Vendor/Ads reads.
- grok.md: DataDoe is protocol-level so BYO-MCP from Grok plausible but not named by DataDoe.
- Competitors: AgentCentral ($39/$69/$99/$199 by order volume; implied no Vendor Central/BigQuery), Seller Labs MCP (free under $2K/mo revenue; can edit campaigns/bids with approval), TMR MCP (read-only, free for TMR users), Windsor.ai (read-only), Adzviser (read-only), Apideck (Items only; you register own SP-API app), Zapier MCP (2 tasks per call; Pro plan NA), Vinkius (10-tool proxied SP-API server), Amazon's own `@amazon-sp-api-release/sp-api-dev-mcp` (developer explorer, not data).

---

## 4. Orchestrators and subscription CLIs: verdicts and exact policy findings

### 4.1 Verdicts (orchestrators.md, subscription-clis.md, hosting-ops.md, frameworks-standards.md)
- No surveyed orchestrator satisfies org-chart + typed requests + markdown-git state + Telegram approvals + MCP action + legitimate subscription billing + per-department credential isolation at once.
- Paperclip: only purpose-built org-chart/budget/approval orchestrator; best-evidenced subscription-CLI adapters (`claude_local`, `codex_local`); Postgres-native state (markdown-git must be bolted on); typed requests not first-class (issue tickets); 6 months old, single pseudonymous maintainer (@dotta), 153 open issues snapshot (43 bugs, 5 security), Reddit "worse than plain Claude Code"; heavy for CX22. hosting-ops: run only as a read-only dashboard/control-plane if at all.
- OpenClaw: native markdown-git memory (USER.md, MEMORY.md, memory/YYYY-MM-DD.md), native Telegram/Signal/WhatsApp channels with pairing allowlists, multi-provider incl. Grok; but CVE-2026-25253, 258k exposed instances, ClawHavoc supply chain, Anthropic policy reversed three times on it — never bind beyond Tailscale, no ClawHub skills. memsearch (extracted memory search) reusable standalone.
- Hermes Agent: native MCP/cron/Telegram, self-generated skills; claude-code subprocess provider only in open issues; no org-chart.
- NanoClaw: best isolation (container per context, Docker Sandboxes/Firecracker), API-key only (no subscription).
- n8n: best turnkey approval UX (Send-and-Wait Telegram buttons) + native MCP node + single container; no department concept; AI Agent node defaults to API keys; self-host is one more server (its own DB/auth/updates).
- Temporal: ~0.4 FTE ops, disqualified. DBOS: MIT library over existing Postgres, recommended if durability needed. Windmill: AGPLv3, native approval steps, heavier. Inngest self-host: contradictory sources, UNKNOWN. Trigger.dev: Apache/MIT (conflicting), Postgres + containers.
- Frameworks: LangGraph library MIT but `langgraph-api` Elastic License (REPORTED); CrewAI MIT; AutoGen frozen (Microsoft Agent Framework 1.0 GA Apr 3 2026) = framework-vendor-risk cautionary tale; Pydantic AI (MIT, durable execution on Temporal/DBOS/Prefect) best vendor-agnostic pick; Agno only one with native scheduler + HITL; Claude Agent SDK explicitly single-vendor. Recommendation: no framework, or Pydantic AI thin.
- Router: LiteLLM proxy self-hosted (per-department model groups, fallbacks, pre-call budget caps, OTel). Portkey Apache-2.0 since Mar 2026 (acquired by Palo Alto Apr 2026). OpenRouter/Vercel/Cloudflare hosted-only.
- Observability: Langfuse (MIT core) first, Opik runner-up; instrument via OpenLLMetry/OTel GenAI (agent spans still experimental).
- Memory: markdown-in-git as ground truth; Mem0 as derived index only; Zep hosted-only (avoid); Cognee self-host graph later; Anthropic memory tool / Claude auto-memory are patterns, not mechanisms.
- hosting-ops verdict: local Mac mini, launchd LaunchAgents (tokens live in user home), Docker `compose run --rm` per agent, 1Password Service Accounts (`op run`) or self-hosted Infisical, healthchecks.io off-box dead-man switch, Tailscale, GitHub free, restic -> B2, pin versions + weekly ops-check report. Contract: ~6-10h setup, ~1-3h/month; irreducible manual step = periodic browser OAuth re-auth (interval undocumented). "Leverage subscriptions" and "zero maintenance" are in direct tension.
- subscription-clis allocation: 2-3 sensitive approval-producing departments on Claude Code CLI/Max; 2-3 analysis departments on Codex/ChatGPT; 1-2 credential-free read-only on Grok Build; cross-department consolidation on Anthropic API key (Agent-SDK-shaped code must be API-billed). Keep a funded ANTHROPIC_API_KEY (~$15-40/mo floor) plus small OpenAI/xAI keys as overflow.
- Capacity: 8 departments x 30-60 min agentic ≈ 150K-500K tokens/run, 1.2-4M/day, 8-28M/week (own estimate); Sonnet 5 API ≈ $90-300/mo; Claude Max 20x "very likely insufficient" for all 8 daily; comfortable for 2-4 lighter departments. ChatGPT Pro possibly most elastic (REPORTED). Max 5x $100, Max 20x $200 (5-hour window + weekly cap + Sonnet sub-cap REPORTED; ~225 / ~900 messages per 5h REPORTED).
- Multi-agent pattern: shared state (blackboard) + typed request files + read-only coordinator synthesis is consistent with Anthropic guidance; "typed request inbox" and "coordinator meeting" are the operator's own extension, not directly validated by Anthropic production write-ups (frameworks-standards.md §7).

### 4.2 Anthropic — exact findings
- VERIFIED text (code.claude.com/docs/en/legal-and-compliance): "Developers building products or services that interact with Claude's capabilities, including those using the Agent SDK, should use API key authentication through Claude Console or a supported cloud provider. Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, or Max plan credentials on behalf of their users." / "Nor does it prevent an end user from signing in to the unmodified Claude Code binary with their own Claude subscription..." / API keys may be provisioned in secrets managers/machine images "provided the resulting usage is billed to the key owner". / "Advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK" and Anthropic "may [enforce] without prior notice."
- Timeline (REPORTED, cross-corroborated): Jan 9 2026 server-side block, error "This credential is only authorized for use with Claude Code and cannot be used for other API requests."; Feb 19-20 2026 ToS/docs codified; Mar 19 2026 OpenCode maintainers removed Anthropic OAuth code ("anthropic legal requests" PR); Apr 4 2026 full enforcement (Boris Cherny announcement; same day OpenAI made Codex free on all paid tiers); May 13 2026 "Agent SDK credits" tier (Pro $20, Max 5x $100, Max 20x $200 credits; OpenClaw re-authorized by name); Jun 15 2026 separate credit pool paused — subscription-authenticated SDK/`claude -p`/third-party use draws from the same plan limits. Net Sept 2026: third-party harnesses on Max OAuth "permitted but policy-volatile" per orchestrators.md vs "cannot" per subscription-clis.md (the two surveys disagree; subscription-clis.md quotes the live page, which still forbids third-party routing). Unmodified `claude` binary subprocess on own subscription was never blocked.
- Community feature request anthropics/claude-agent-sdk-python#559 (Max billing in SDK) closed without grant. VERIFIED issue exists.
- Headless `claude -p` requires `--dangerously-skip-permissions`/`--permission-mode bypassPermissions`; tool calls via CLI subprocess are text, not JSON-RPC (Hermes issue detail). REPORTED.
- OAuth token lifetime: setup-token = one year (VERIFIED docs) vs community "weeks-months, needs re-auth" (REPORTED, hosting-ops). No device-code flow (issues #22992, #42965).
- Routines rules: see §1.4. Routines cannot be used from API accounts; run with no approval prompts; count against subscription + daily run cap.
- Cowork `/schedule` scheduled tasks: server-side, any paid plan, knowledge-work surface. REPORTED (customer-health-runtime.md C8).

### 4.3 OpenAI — exact findings
- Codex CLI Apache-2.0, open source, 101K+ stars. VERIFIED repo.
- Service Terms (REPORTED via snippet): prohibit "automatically or programmatically extracting data", sharing account credentials, reselling access or "using ChatGPT to power third-party services". No clause found against cron use of own account; no explicit blessing either ("documented-but-unendorsed middle ground"). help.openai.com/en/articles/11369540: Codex sign-in shares ChatGPT ToS; guardrails "may occasionally involve a temporary restriction".
- Never revoked ChatGPT-subscription use in third-party harnesses; Codex free on all paid tiers Apr 4 2026. REPORTED.
- Limits: 5-hour rolling window + weekly cap; Jul 12 2026 5-hour window suspended (weekly only); Aug 25 2026 5-hour limit reinstated for Plus; Pro tiers ~5x/20x with looser gate "for the upcoming months". REPORTED. `/status` shows quota. Models GPT-5.5/5.6 (Luna/Terra/Sol tiers) REPORTED; exact current default UNKNOWN.
- Device auth: `codex login --device-auth` documented; some reports it needs workspace admin enablement; fallback SSH-forward localhost:1455 or copy auth.json (issues #9253, #3820). REPORTED.
- API pricing REPORTED: GPT-5.6 Luna $0.20/$1.20, Terra $2/$12, Sol $5/$30 per MTok.

### 4.4 xAI — exact findings
- Products: Grok Tasks (Jun 12 2025) -> Automations (Jul 16 2026; schedule-based free, email-trigger SuperGrok $30); Grok 4 Heavy/SuperGrok Heavy $300 (internal parallel agents, not developer-exposed); Grok Build (May 2026); Grok Bot beta Aug 11 2026 (persistent cloud computer, logs into user's tools with user's own credentials; all Bots share one cloud computer per account; no API for create/schedule/monitor; tier gating in flux; users report "nearly unusable"); Grok 4.6 Aug 12 2026 (500K ctx). All REPORTED (x.ai blocked).
- API `api.x.ai/v1` OpenAI-SDK-compatible; Agent Tools API (web search, X search, code exec, collections, MCP); Remote MCP tools; Responses API state capped at 30 days; no hosted scheduler/vault/budget/multi-agent primitive found. REPORTED. Rate-limit tiers by cumulative spend since Jan 1 2026; no public enterprise SLA.
- Pricing REPORTED: Grok 4.1 Fast $0.20/$0.50 (status disputed), 4.20/4.3 $1.25/$2.50, Grok Build 0.1 $1/$2, 4.5/4.6 $2/$6 ($4/$12 above 200K).
- Grok Build: SuperGrok $30 / X Premium+ $40 reported sufficient by some, SuperGrok Heavy $299 (promo $99 x6 months) by others — minimum tier UNKNOWN; headless via `GROK_CODE_XAI_API_KEY` + `-p`; claims zero-config Claude Code compatibility (reads CLAUDE.md/.claude/, skills, MCP, hooks) REPORTED; ACP support claimed (which ACP unclear); hang bug on "Waiting/Responding" REPORTED.
- Exfiltration incident Jul 2026: see §1.5. subscription-clis verdict: "hard blocker for trust" for anything with credentials; usable only for a credential-free read-only department with `.env` excluded.
- No evidence of xAI restricting third-party/automated subscription use (REPORTED-permissive, thin).
- Safety/regulatory: IWF-confirmed CSAM imagery Jan 2026; UK ICO, Ireland DPC, Canada's Privacy Commissioner, Ofcom investigations by Mar 2026 (relevant to a Canadian operator handing credentials to Grok Bot). REPORTED.
- Benchmarks REPORTED: τ²-Bench Grok 4.1 Fast 82.71% vs Opus 4.5 81.99%; SWE-bench Verified Grok 4.5 86.6% vs Claude Opus 5 96%. Tool-call hallucination reports (vercel/ai #11263).
- grok.md verdict: Claude for platform layer; Grok at most a model swap behind an abstraction; Grok Bot not for a real business today.

### 4.5 Google — exact findings
- Gemini CLI quota doc VERIFIED: personal account 1,000 req/day; unpaid API key 250/day Flash only; Code Assist Standard 1,500; Enterprise 2,000.
- Feb 2026 ban on proxying Gemini CLI OAuth via third-party tools; Mar 25 2026 detection + mass suspensions incl. Ultra subscribers; Jun 2026 OAuth login flow deprecated for AI Pro/Ultra/individual Code Assist. VERIFIED via multiple reports.
- Jun 18 2026 Gemini CLI stopped serving free/AI Pro/AI Ultra individuals, no grace period; Code Assist Standard/Enterprise (Workspace/Cloud-billed) unaffected. REPORTED (The Register, others).
- Antigravity CLI (`agy`): closed source, headless mode, MCP, 5-hour windows; AI Pro $19.99 "too constrained", AI Ultra $100 "realistic threshold"; automation terms UNKNOWN. REPORTED.
- Verdict: Gemini/Antigravity excluded (not in Rami's subscription stack; would be API-key or a fourth subscription).

### 4.6 Other harnesses (subscription-clis.md §5)
- OpenCode: cannot use Claude Pro/Max (policy + maintainers removed code); API key only; live 429/OAuth issues (anomalyco/opencode #18362, #18329).
- Goose (Linux Foundation AAIF, Apache-2.0, 53.7k stars): BYOK only, MCP-native, Recipes with approval gates.
- Crush (Charm; own "Hyper" subscription), Aider, Cline (own credits; free Kimi K2.5), Qwen Code, Kimi CLI (backend for other harnesses), Amp ($20/$200 own plans): none spend Claude Max/ChatGPT/SuperGrok. "Pi" CLI: UNKNOWN, not found.
- Load-bearing finding: only first-party CLIs (Claude Code, Codex, Grok Build) can spend the existing subscriptions.

---

## 5. Interface and knowledge survey findings (interface-knowledge.md, hosting-ops.md, frameworks-standards.md)

Approval channel
- Telegram via python-telegram-bot, long polling, single hard-coded chat-ID allowlist: free, inline buttons, no public endpoint, no template review, no ban risk. Signal fallback (no buttons; keyword replies). Slack team-oriented (HumanLayer is Slack/email-first; Telegram unconfirmed). Discord needs a bot process for button clicks. WhatsApp Cloud API: template pre-approval + per-message billing rising Oct 2026; Baileys never.
- Approval mechanics: 12-Factor Agents factors 5/6/7/12 (unified event log, pause/resume, contact humans as tool calls, stateless reducer); only durable external state survives restart; defense in depth = allowlisted chat ID + executor only executes `status='approved'`; two-tap "maker-checker" confirm above a dollar threshold; `expires_at` so stale approvals never fire; TOTP in reply as pragmatic non-repudiation upgrade; nobody in OSS signs messages cryptographically.
- File/git-based approval queue (markdown + YAML frontmatter `status: pending` -> `approved`; PR review as gate; gh-aw precedent) suits content/knowledge/prompt changes; poor for time-sensitive money (no push, no one-tap). Hybrid recommended: chat for $, git-PR for content.
- Claude Code mobile push approvals (v2.1.110) and `claude-push` (ntfy.sh) exist.

Brief delivery
- Telegram 4096 chars post-parsing; chunk on section boundaries; HTML parse_mode over MarkdownV2; headline in chat, link to full page.
- Wiki: MkDocs Material (Python, most popular, one-line GH Actions deploy) over Docusaurus, Quartz (Obsidian wikilinks/backlinks; closest to interlinked dossiers), Obsidian Publish (paid SaaS), mdBook.
- Private access: Cloudflare Pages + Cloudflare Access (free <=50 users, email OTP, custom domain required) for non-technical family; Tailscale/Headscale (6 free accounts) if zero public exposure wanted.

Repo as wiki and memory
- AGENTS.md is foundation-governed (AAIF, Dec 2025), 60k+ repos, 20+ tools; Claude Code needs `@AGENTS.md` import. Put portable rules in AGENTS.md, make CLAUDE.md a pointer.
- OpenClaw layout as reference: USER.md, MEMORY.md, memory/YYYY-MM-DD.md; "the model only remembers what has been written to those files"; memsearch standalone.
- Suggested layout: AGENTS.md, L1_RULES.md (<1 page), inbox/ (raw run outputs), ledgers/, dossiers/ (one file per product/competitor), playbooks/, briefs/, memory/MEMORY.md + dated daily files. Zettelkasten atomic notes + Johnny Decimal + AI librarian; `.brain/` folder pattern.
- Context limits: CLAUDE.md loaded fully every session; keep ~200 lines; everything else on-demand.
- Search: ripgrep until a few hundred files; then sqlite-vec (single file, brute force) before LanceDB; sqlite-memory (sqliteai) as Mem0 alternative.

Ledgers without a database
- JSONL append logs (git-diffable, no schema ceremony) + periodic CSV snapshots (family-readable; bad for appends/merges); SQLite in git is binary-opaque (gitsqlite/textconv workarounds, merges fragile) — generate on demand with sqlite-utils, don't commit; DuckDB queries CSV/Parquet directly (`FROM 'ledgers/sales/*.csv'`); Datasette/Datasette Lite for browsing.
- Real Postgres only when concurrent writers, RLS, FK integrity across many tables, or real-time subscriptions. Free tiers: Supabase 500MB/2 projects/pauses; Neon 0.5GB/100 projects; Turso 100 DBs/5GB/500M reads.

Compounding knowledge
- Provenance fields per memory write (source type, timestamp, agent, evidence, transformation, confidence, update history) — arXiv 2606.04990; tag playbooks "activated" when cited in a real decision.
- Weekly consolidation = classify new / reinforced / decaying; automatic confidence decay when unreinforced N weeks; monthly adversarial falsification of each playbook against last 30 days of outcomes; store the validation verdict as its own provenance-linked record; always re-ground in raw outcome data (model-collapse analogue); 20-30 "golden path" domain eval cases instead of public memory benchmarks (BEAM/LoCoMo/LongMemEval).
- Mem0 confidence-score, "confidently wrong" stale memories; 90-day unreinforced -> demote/archive.

Multi-brand
- Hub-and-spoke: canonical "standards" repo (skills, subagents, MCP configs, AGENTS.md fragments) pulled into each brand repo as a pinned git submodule; fine to ~2-5 brands, then a skill registry.
- Isolation: one data project / one memory namespace / one `.env` (vault scope) / one Telegram bot per brand; shared compute OK if each process reads only its own secrets; mandatory tenant filter if anything is shared.

Hosting/ops details worth carrying
- systemd timers > cron (journald, Persistent=true catch-up, TimeoutStartSec, Restart=on-failure, After=network-online). launchd: LaunchAgents not LaunchDaemons for OAuth tokens; StartCalendarInterval fires after wake; disable sleep.
- Secrets: 1Password Service Accounts / Infisical / Doppler CLI injection (`op run` / `infisical run` / `doppler run`); sops+age weakest rotation; macOS Keychain Mac-only.
- Monitoring: healthchecks.io off-box (20 free checks) + optional Uptime Kuma push monitors; alerts through the existing Telegram bot; ntfy.sh/Pushover alternatives.
- Drift: pin CLI + MCP versions; MCP 2026-07-28 breaking change could silently break older servers (DataDoe, Ads MCP, Keepa, QBO); weekly ops-check job reports without applying.
- Backup: GitHub free > self-hosted Gitea/Forgejo; restic -> B2 (~$0.70/mo for 100GB); recovery <1h except manual re-auth.
- Self-hosted PaaS (Coolify ~57k stars, Dokploy, CapRover) cut VPS ops to 1-2h/mo but do not solve auth; CX32 realistic floor with PaaS + 8 agents.

---

## 6. Comms-design draft summary (comms-design.md, pre-research)

- Principle: departments do not chat; free-form agent-to-agent conversation is expensive, non-auditable, drifts. Three channels.
- Channel 1, shared state (blackboard), always on: `state/inventory.md` (Supply Chain, daily: cover/SKU/market, inbound ETAs, capacity), `state/cash.md` (Finance, weekly: cash, 8-week forecast, PO ceiling remaining), `state/ads.md` (Advertising, daily: launches, pacing, ACOS by SKU, ramps), `state/prices.md` (Pricing, daily: price, floor, competitors, tests), `state/catalog.md` (Catalog, weekly: changes in flight, experiments, suppressed), `state/health.md` (Account Health, daily), `state/calendar.md` (Chief of Staff: launches, deals, seasonal windows, blackout dates — no price/listing changes during Vine, deals, ranking pushes). Rule: read every touching state file before proposing; Chief of Staff rejects proposals that ignore state.
- Channel 2, typed requests (inbox), async: `requests/<dept>/inbox/<id>.md` with fixed schema (from, to, type, SKU(s), ask, needed-by, context links). Enumerated types: need-forecast (Ads -> Supply), need-cash-check (Supply -> Finance), need-margin-floor (Pricing -> Finance), need-launch-plan (Supply -> Ads/Catalog), quality-issue (Customer -> Supply/Catalog), blackout (Ads/Catalog -> Pricing), competitor-oos (Pricing -> Ads), stockout-risk (Supply -> Ads). Check inbox at run start, answer before own work, append answer to same file; unanswered by needed-by escalates to Chief of Staff.
- Channel 3, meetings, scheduled and event-driven: one Managed Agents multiagent session (or one Claude Code session spawning subagents); Chief of Staff coordinates, departments are roster threads; coordinator poses decision, collects positions, resolves via constitution, writes ledger, queues T2+ for Rami. Standing: Monday WBR (all), monthly S&OP (Supply, Finance, Ads, Catalog, Expansion: demand -> supply -> cash -> launch calendar; POs sized here), launch review per new SKU/market (Catalog, Ads, Supply, Pricing). Event meetings: hero stockout imminent (Supply+Ads+Pricing), competitor OOS (Pricing+Ads), health drop (Health+Catalog+CoS).
- Why coordinator not peer-to-peer: Managed Agents supports coordinator<->roster only, one level, no peer messaging — single audit trail, single constitution point, single escalation to Rami; departments still talk async via inbox without coordinator.
- Rami sees: unresolved cross-department conflicts as decisions in the brief (two lines per position); one-page minutes at `meetings/YYYY-MM-DD-<name>.md`; can join live or read later.
- frameworks-standards.md §7 note: the inbox and meeting refinements are the operator's extension of the blackboard pattern; recommends the meeting be a read-only synthesis pass, not live negotiation.

---

## 7. Open questions the surveys left unanswered (targets for new research)

Amazon policy and SP-API
1. Live BSA Section 19 text: exact wording of identification, logging (12-month), and the 20%/500-ASIN human-authorization thresholds; itemized consequences. Never fetched (spapi-writes §3, §3.7).
2. Whether "Amazon Fulfillment" (inbound) and "Buyer-Seller Messaging" roles are restricted; approval timelines for a private app in 2026 (spapi-writes §2.2).
3. Full SP-API notification-type catalog (notification-type-values page) incl. any account-health push type; FBA inventory availability notification exact name (spapi-writes §5.2).
4. Whether Amazon shipped an official SP-API data MCP (press mentions "SP-API MCP released by Amazon late 2025"); status of `@amazon-sp-api-release/sp-api-dev-mcp` (catalog-intel §2; spapi-writes §1.1).
5. Seller Assistant / Canvas availability in Canada; Seller Assistant auto-approve mode status (spapi-writes §4; advertising §2).

Amazon Ads
6. Full 50+ tool manifest of the official Ads MCP; whether Brand Metrics and search-term reports are exposed; official rate limits; explicit marketplace list; any Managed Agents / Routines guidance (advertising §1, §3).
7. Whether an ads account at CAD ~150/day qualifies for Ads API developer access (the ">$50K/month" gate claim) (advertising §1).

DataDoe
8. Actual sync lag vs Seller Central; whether exports consume the 2,000-token pool; overage pricing past 10M rows/2,000 tokens; per-account limits (datadoe §5-6).
9. Whether Walmart/Shopify/TikTok, AMC, buyer messages, reviews are reachable through the MCP (vs BI layer only) (datadoe §2).
10. Skill Hub contents (47 skills), Memories/Files semantics, scheduled agents/alerts: are they MCP-addressable or app-only; can a scheduled DataDoe agent push to a webhook/Slack/Telegram (datadoe §4; frameworks-standards §3 could not find Skill Hub).
11. Whether DataDoe Actions can be restricted per API key / per marketplace; whether `actions_list` audit export satisfies the Section 19 vendor test (app ID, audit log, compliance statement) (datadoe §7; spapi-writes §3.4).
12. Ad-data retention windows (95/60 days) — independent confirmation (datadoe §5).
13. Whether DataDoe has updated to MCP spec 2026-07-28 (hosting-ops §6.1).

Subscriptions and CLIs (as of Sept 2026)
14. Anthropic: current status of third-party-harness use on Max after the Jun 15 2026 pool change (orchestrators.md and subscription-clis.md disagree); whether daily multi-department `claude -p` cron on one Max account counts as "ordinary, individual usage"; Routines daily run-start cap number; exact Max 5x/20x token ceilings; Sonnet-specific weekly sub-cap; setup-token real lifetime vs re-auth reports; Routines self-hosted environment option details; whether Routines can prune MCP connectors per routine (subscription-clis §1; hosting-ops §1.0).
15. Anthropic: Managed Agents pricing/webhooks/memory-store detail (only REPORTED); Cowork scheduled tasks terms (customer-health-runtime C8-C9).
16. OpenAI: official numeric Codex weekly/5-hour limits per plan; whether personal Plus supports device-code auth; current default Codex model; whether OpenAI Service Terms permit unattended scheduled Codex use of one's own account (subscription-clis §2).
17. xAI: minimum tier for Grok Build headless; Grok Bot tier gating and run limits; whether the exfiltration path was structurally removed and a post-mortem published; Grok Build hang bug status; whether "ACP" means Zed or IBM; xAI ToS on automated subscription use; Automations run limits (grok §1-2; subscription-clis §3).
18. Google: Antigravity CLI automation terms; whether a Workspace Code Assist seat is worth a fourth subscription (subscription-clis §4).
19. Paperclip: official Docker-per-agent mode; Telegram notification adapter; gemini_local OAuth; whether it can act as MCP client itself (orchestrators §1, §5).
20. HumanLayer Telegram channel support (orchestrators §5).
21. Hatchet license/stars; Inngest self-host reality; Trigger.dev license; LangGraph license file (frameworks-standards §1, §5).

Data tools
22. Helium 10 Diamond current price and whether Market Tracker / rank tracking data is exposed via the MCP; MCP tool list (catalog-intel §1.1, §3.4).
23. Keepa current EUR pricing and token math for ~60 SKUs + competitor set daily (catalog-intel §3.1).
24. Nova Analytics: Walmart support, current pricing, whether "free for life" promo still applies, write capability (supply-finance §1).
25. Sellerboard: any official API in 2026; Link My Books CAD support; Taxomate vs A2X Multi head-to-head at CA+US+Walmart (supply-finance §1, §4).
26. FeedbackFive API; SellerSonar Enterprise price (customer-health-runtime A1; catalog-intel §6.3).
27. Walmart Marketplace API 2026 shape, WFS inbound API, "130-tool lobehub" and Apideck Walmart MCP existence; WCPN application path for a solo brand (spapi-writes §6; advertising §7).

Compliance and category (flagged as highest-priority gaps)
28. Grocery & Gourmet ungating process for US (docs, timelines, scrutiny for Middle Eastern foods); meltables policy and seasonal holds; cold-chain FBA rules (catalog-intel §7).
29. US nutrition-label format requirements; Halal/Kosher/Organic certification equivalence CA->US; country-of-origin enforcement (catalog-intel §7; supply-finance §5).
30. End-to-end FDA/CFIA compliance consultants and customs brokers for small food brands, with costs (supply-finance §5).
31. Flexport minimum volume / small-importer pricing (supply-finance §5).
32. USD/CAD FX bookkeeping mechanics; 1120-F protective filing decision (supply-finance §4; customer-health-runtime B6).
33. Vine 2026 fee change confirmation ($0 under $100) and CA applicability (customer-health-runtime A4).
34. Whether CA FBA follows the same 50-day expiry pull rule (catalog-intel §7.1).

Interface/knowledge
35. Tailscale current free-tier device/user caps; Cloudflare Access current free-user cap (interface-knowledge §3 cites 2026 figures, not re-verified).
36. sqlite-memory and memsearch maturity for a markdown repo of a few hundred files (interface-knowledge §4).
37. No production case study found for the "typed request inbox + coordinator meeting" pattern; validation still needed (frameworks-standards §7).

Design-level (from V2 design §10 and README)
38. Which component holds SP-API write credentials in the zero-server design (V2 §10.2) — the surveys' write-path recommendation assumed a self-hosted Executor that v2 retired.
39. Routines-first vs Managed Agents day one; where the approval gate lives given Routines run with no prompts (V2 §10.1; subscription-clis §1.4).
40. Guardrail numbers (PO ceiling, daily ad cap, margin floor) and account facts (NA unified, Brand Registry CA/US, Walmart CA/US) (V2 §10.4-10.5).
