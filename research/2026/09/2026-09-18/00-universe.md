# Earnings universe — 2026-09-18

**Window:** After the US close on Friday 18 September 2026 through before the US open on Monday 21 September 2026
**Generated:** 2026-09-18T05:13:48+00:00 UTC
**Status:** `ok`
**Source:** after-close `nasdaq` · before-open `nasdaq`

**Counts:** 0 after-close + 0 before-open = **0** total; 0 above the $500,000,000 market-cap floor; **0 eligible** after qualification.

No company in the raw feed carried a confirmed `amc` (18th) or `bmo` (21st) session tag.
Nasdaq returned 7 rows for 2026-09-18 and 8 rows for 2026-09-21, but every one of them
came back `time-not-supplied` (`session: "unknown"`) except `ABVX` on 2026-09-21, which
is tagged `amc` and therefore does not fill the before-open slot this window needs. Per
the stage-0 qualification rule ("conflicting or unconfirmed BMO/AMC timing — drop
these"), none of the unconfirmed rows are carried into the universe below. This is the
same pattern seen on 2026-09-17 (1 of 16 raw rows had a confirmed session) and is a
known Nasdaq feed characteristic, not a fetch failure — see `CLAUDE.md`,
"`time-not-supplied` rows are checkable" and `edge/scripts/session_resolve.py`, which
stage E may use later today to recover any of these that are genuinely reporting.
