# Run log — 2026-09-22

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-21 13:39 UTC
- Fired 2026-09-21 13:30 UTC (session clock read 13:38 UTC). Sealing for the NEXT European trading day, **2026-09-22** (Tue). Europe reports before the open, so the window is close(2026-09-21) -> close(2026-09-22) for bmo names.
- Sealed spot is an INTRADAY price, not a close: the stage fires ~2h before the 17:30 CET close on the operator's instruction of 2026-09-19. eu_resolve.py takes the realised move from daily bars, never from the sealed spot.
- Plan: eu_universe.py --date 2026-09-22 over ten markets (uk de fr se dk no fi it es pl), $200k/day turnover floor, cap 20, seeded random draw; eu_priced_in.py seals baselines; one isolated hunter per name dispatched on submarket in waves of 5; edge_score.py (the US scorer, unchanged); europe-note.md; publish after every wave.
- Research only. No orders, no broker call. Publishing to main (EARNINGS_DATA_BRANCH pinned explicitly).
