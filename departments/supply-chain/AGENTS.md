# Department: supply-chain

**Mission.** Know the cover days of every active Canadian SKU daily and name the ones under the 14-day floor.
**Judged by.** A stockout that appears in the data before it appears in a state file.
**Thresholds.** Hero cover floor 14 days; seasonal buffer 6 weeks (constitution §4). cover_days = available ÷ (units in the last 28 days ÷ 28). No smoothing and no forecast until a product file exists to forecast against.
**Hard rules.** Propose no purchase order until a supplier file with lead time and price exists. Nothing inbound with under 105 days of shelf life at receipt. Meltable stock inbound only 16 October to 14 April.
**Jobs.** `supply-chain.daily` in `docs/jobs.json`.
