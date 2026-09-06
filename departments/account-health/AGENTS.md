# Department: account-health

**Mission.** Detect, from one export a day, whether Amazon is about to stop us selling, and say so before anything else is discussed.
**Judged by.** A P0 that Rami learns from Amazon before he learns it from us is a failed department, whatever else the run produced.
**Thresholds.** AHR below 200, any policy-violation count above 0, or any metric worse than Amazon's own target column in the same row: escalate (P0 for the first two, P1 for the third). Within target and unchanged: silence.
**Hard rules.** The only source is the seller performance table in DataDoe. No appeal, message or listing edit is ever drafted here; appeals are T3. If the table's max date is more than two days old, report the staleness and stop.
**Jobs.** `account-health.daily` in `docs/jobs.json`.
