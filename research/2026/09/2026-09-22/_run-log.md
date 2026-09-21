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
