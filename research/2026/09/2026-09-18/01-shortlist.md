# Stage 1 — Triage shortlist — 2026-09-18

**Window:** After the US close on Friday 18 September 2026 through before the US open on
Monday 21 September 2026

**Mode:** skipped (universe at or below threshold — 0 eligible ≤ 10)

## Funnel

0 universe → 0 eligible → 0 cleared floors → 0 shortlisted

## Shortlist

None. Stage 0 qualified zero names for this window: Nasdaq returned rows (7 for the
09-18 after-close slot, 8 for the 09-21 before-open slot) but all but one carried
`time-not-supplied`/unknown session, and the qualification rule drops unconfirmed-session
rows rather than guessing. The one confirmed row (ABVX, amc on 09-21) falls outside this
window's before-open slot. See `00-universe.json` and its run-log entry.

Per `earnings-triage`, an eligible universe at or below `triage.skip_if_universe_at_or_below`
(10) skips the screen entirely and carries every eligible name forward — here that is
zero names, not a screening failure. No scouts were spawned.

## Dropped names

None to report — the drop happened upstream in stage 0's qualification step, not in
triage.

## Note for stage 2

Nothing to research today. Stage 2 should find `01-shortlist.json` with an empty
`shortlist` and `triage_mode: skipped_small_universe`, and skip rather than treat this as
a missing/failed stage 1. Same underlying cause as 2026-09-17: Nasdaq's `time-not-supplied`
labeling is starving the window of confirmed rows. `edge/scripts/session_resolve.py` may
recover a real name from these rows later, independent of this pipeline (see stage E).

---
*This is a research/forecasting exercise over public information, not investment advice.*
