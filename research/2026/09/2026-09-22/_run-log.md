# Run log — 2026-09-22

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-21 13:39 UTC
- Fired 2026-09-21 13:30 UTC (session clock read 13:38 UTC). Sealing for the NEXT European trading day, **2026-09-22** (Tue). Europe reports before the open, so the window is close(2026-09-21) -> close(2026-09-22) for bmo names.
- Sealed spot is an INTRADAY price, not a close: the stage fires ~2h before the 17:30 CET close on the operator's instruction of 2026-09-19. eu_resolve.py takes the realised move from daily bars, never from the sealed spot.
- Plan: eu_universe.py --date 2026-09-22 over ten markets (uk de fr se dk no fi it es pl), $200k/day turnover floor, cap 20, seeded random draw; eu_priced_in.py seals baselines; one isolated hunter per name dispatched on submarket in waves of 5; edge_score.py (the US scorer, unchanged); europe-note.md; publish after every wave.
- Research only. No orders, no broker call. Publishing to main (EARNINGS_DATA_BRANCH pinned explicitly).

## Stage EU — universe and baselines sealed
- Logged at 2026-09-21 13:42 UTC
- Universe: 22 vendor rows scheduled for 2026-09-22, 13 dropped on the $200k/day floor, **9 eligible, 9 hunted** — at/under the cap of 20, so `selection.method` is 'all 9 eligible names' and no random draw was needed.
- by_market: uk 8, fr 1. `market_concentration.largest_market_share` = **0.889 uk**, 2 markets represented. Eight of the ten markets contributed nothing: de/se/dk/no/fi/it/es all had 0 scheduled rows, pl had 1 scheduled and 0 above the floor. No market was flagged `market_closed`. Late September is the UK's month, as SUBMARKET.md predicts.
- Registers: FCA (uk) read, 419 rows as of 2026-09-19; AMF (fr) read, 74 issuers as of 2026-09-17. **7 of 9 names carry `anchor_covered: true`**; FNX and ABCA are `register_read_no_position` (a truncated zero, not an anchor) and take `anchor_quality.direction` 0.15 instead of 0.45.
- Sessions: all 9 bmo. Three carry `session_unresolved: true` — PRTC, SAA, SMIN — defaulted to bmo on the 339/379 measured UK base rate.
- history.basis: 8 UK names `observed_rns` (real dated announcement history); ABCA (fr) is `estimated_from_cadence` — a scale, never evidence a print exists.

## Stage EU — wave 1 banked (5 of 9)
- Logged at 2026-09-21 18:32 UTC
- Hunted: ABCA (fr), KGF, SMIN, OXB, MAB1 (uk). All five wrote a complete hunt file and all five carry a real `pre_local` freeze, a `pre_lessons` freeze and `event_confirmed: true`.
- Finding sums before scoring: OXB +3.20, KGF +2.70, ABCA +2.30, MAB1 +1.40, SMIN −1.40.
- **All five subagents were killed by an account session rate limit (HTTP 429, reset 18:30 UTC) during their wrap-up turn, AFTER writing their JSON.** Nothing was lost: the contract check passes on all five. Only KGF's hand-back reached this session in prose; the other four are read from disk.
- **The run therefore spans a 4.5-hour gap**: baselines sealed 13:39 UTC, wave 1 hunted 13:50–14:00 UTC, wave 2 dispatched after the reset at 18:31 UTC. The baselines are unaffected — sealed once, before any hunter, and nothing downstream revises them. But wave 2's hunters can see the 2026-09-21 European close and wave 1's could not, which is an information asymmetry INSIDE one day's ranking. It is recorded here and in the note rather than smoothed over.
- KGF flagged that it could not reproduce the baseline's short figure: the live FCA aggregated CSV reads 9.31% at position date 2026-08-05 where the cached baseline reads 10.69% at 2026-09-16, and the FCA's own 'current' file is itself ~6 weeks stale. Direction unaffected. Recorded, not corrected — the baseline is sealed.

## Stage EU — wave 2 partial (FNX, SAA banked)
- Logged at 2026-09-21 18:45 UTC
- FNX: emitted −1.0, 3 findings summing −1.3, event confirmed twice from the issuer's own words (23 Jul RNS naming 22 September, plus today's 11:33 RNS setting a 22 Sep 09:00 BST question deadline). `anchor_covered: false` — the FCA register read and does not name Fonix, which is the 0.5% per-holder truncation floor and not a measurement, so its lean is close to the free control.
- SAA: emitted +2.4, 3 findings summing +3.1, event confirmed. Its locality control is the largest on the day — `pre_local` −2.0 flips to `pre_lessons` +2.4.
- Two 89-byte files (`prtcq.json`, `sptxq.json`) were left in the repo root by a hunter's curl — failed Yahoo chart calls returning `Invalid Crumb`. Deleted; they carried nothing. Worth noting that hunters can write scratch to the repo root.
- LUCE and PRTC still hunting.
