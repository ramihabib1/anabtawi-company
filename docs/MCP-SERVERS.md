# MCP servers and secrets

Department `.mcp.json` files reference secrets by `${NAME}`. The runtime injects them from the vault; they are never written to the repo.

| Server | Used by | Secret names | Notes |
|---|---|---|---|
| DataDoe | all | `DATADOE_MCP_KEY` | Hosted, HTTP streamable. Read-only key for the Grok Bot pilot; actions stay disabled in DataDoe settings. |
| Amazon Ads MCP (official) | advertising | `AMAZON_ADS_MCP_URL`, `AMAZON_ADS_MCP_TOKEN` | Needs Ads API (LWA) credentials approved for the profile. Fill the URL and token from Amazon's connection page once approved. |
| Keepa | pricing-intel | `KEEPA_API_KEY` | Entry tier, 20 tokens/minute. The `keepa-mcp` package name is a placeholder until verified; swap for the chosen server. |
| QuickBooks Online MCP | finance | `QBO_CLIENT_ID`, `QBO_CLIENT_SECRET`, `QBO_REALM_ID` | Intuit's official open-source server. Read use only; A2X posts. |
| Freightos | supply-chain | `FREIGHTOS_MCP_URL` | Placeholder until the landed-cost API wrapper is chosen. Until then the skill calls the public calculator by hand. |

Never in any `.mcp.json`: SP-API credentials, Seller Central logins, Telegram tokens. Those live only with the hands runner and the approval bot.
