---
name: datadoe-export
description: How to pull a dataset from DataDoe's MCP using its export-job model. Use whenever a charter says "export from DataDoe".
---
# DataDoe export

DataDoe does not expose per-entity tools. Data comes from an export job.

1. `exports_sources_get` with a search phrase (for example "fba inventory", "orders", "search query performance", "returns", "settlements") to find the template and its columns.
2. `exports_create` with: the source id, a date range in ISO dates, filters (marketplace country code, SKU list), group-by and aggregates if you need totals, format `json` for under 10,000 rows, else `csv`.
3. Poll `exports_get` until status is complete. Reports can take minutes; do not create a second identical job.
4. `exports_raw_download` for inline data under a few MB; otherwise `exports_raw_url_get` and fetch once.
5. Cite the export in your state file as `DataDoe export <source> <date range> <job id>`.

Never call `actions_start`. Actions are disabled for every department; writes go through the hands runner.
