# Run log — 2026-10-16

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-15 13:39 UTC
- Fired 13:38 UTC 2026-10-15 (European markets still open; sealed spot is intraday). Sealing for EVENT DATE 2026-10-16 (Fri), the next European trading day.
- Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model panel -> note. No orders.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-15 13:52 UTC
- 7 scheduled, 5 eligible (se 5), all 5 hunted (under cap 20). Largest market se 100%. First universe build hit a truncated-JSON error on the German vendor read (de per_market error); one retry read DE cleanly (428 rows, 0 scheduled), same 5 names. DE Yahoo calendar unavailable on the retry. SE register read as of 2026-10-15 (335 rows); anchor_covered: AZA, NP3 (2 of 5). history.basis estimated for all 5; ITECH hist=0. Provenance nordic.v5 · claude-opus-5-5. One wave: [AZA INVE_A ITECH NP3 PLAZ_B].

## Stage EU — panel STARTED
- Logged at 2026-10-15 14:02 UTC
- 5 hunts done; 5 ranked, 0 above 2.8 (top AZA +0.80, bottom INVE_A/ITECH 0.00). 5 packs, four judges.
