# Run log — 2026-10-07

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-06 06:41 UTC
- 06:4x UTC fire (Sydney 17:4x AEDT): universe for next ASX session 2026-10-07, seal baselines, one unpriced-hunter-au per name in waves, score with edge_score.py. No orders.

## Stage AU — Australia researcher — DONE (empty session)
- Logged at 2026-10-06 06:41 UTC
- au_universe.py: 1572 scanner rows, 0 scheduled / 0 eligible / 0 hunted for 2026-10-07; market_open true (weekday, not an ASX holiday). Thin off-season session, not a fault. No baselines sealed, no hunters spawned.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-06 13:38 UTC
- Fired 13:38 UTC 2026-10-06 (European markets still open). Sealing for event date 2026-10-07 (next European session). Plan: eu_universe -> seal baselines -> provenance -> one market hunter per name in waves of 5 -> edge_score -> note. No orders.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-06 13:41 UTC
- eu_universe.py --date 2026-10-07: 7 scheduled, 2 eligible at $100k floor, 2 hunted (all eligible, under cap 20): uk NET (Netcall, session_unresolved, RNS-confirmed date), se INDU_A (Industrivärden A). Concentration 50/50, 2 markets. All ten market calendars read; none market_closed.
- Baselines sealed ~13:50 UTC on intraday prices (not closes). anchor_covered false on both (registers read: se 337 rows, uk 424 rows; neither names the issuer -> truncated zero). History: NET observed_rns, INDU_A estimated_from_cadence. provenance stamped (uk/nordic hunters on claude-opus-5-5). Wave 1 of 1: 2 hunters launched.
