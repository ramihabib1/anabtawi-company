# account-health — durable memory

Facts and patterns this department relies on. Each entry: `- since: YYYY-MM-DD · source: <path or export> · <fact>`. Keep under 300 lines; prune monthly.

- since: 2026-09-04 · source: DataDoe sellers_and_vendors_list · CA seller UUID `5692b95f-f3f0-4063-9c1c-40177c54f408`; US seller UUID `822ebf46-c2bc-4350-86d3-dcf1bc8d5469`; same selling-partner id A13QU1H2J81LX0 on both.
- since: 2026-09-04 · source: DataDoe plugins Catalog and Brand Context · Large Inactive CA catalog traces to a 2026-07-13 labeling/compliance deactivation; do not treat historical Inactive alone as a new Amazon enforcement without a fresh issues row.
- since: 2026-09-04 · source: DataDoe exports_sources_get · Org has listing/account notification tables disabled; daily detection relies on Listings + Listings Raw JSON + Seller Account Health Metrics exports.
- since: 2026-09-04 · source: playbooks/us-launch.md · Account-health owns US grocery ungating (due 2026-09-20) and FDA agent/FSVP/supplier-verification open (due 2026-09-20); FDA FFR renewal window Oct 1–Dec 31 2026.
