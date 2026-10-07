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

## Stage EU — Europe researcher — DONE
- Logged at 2026-10-06 13:47 UTC
- Event date sealed for: 2026-10-07. 2 hunters, 2 hunts returned, 0 shed. edge_score ranking_key impact_sum: NET +0.10, INDU_A +0.00; 0 of 2 above floor 2.8. Note: europe-note.md. Publishing with EARNINGS_DATA_BRANCH=main.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-07 01:05 UTC
- 01:05 UTC (10:05 JST) fire. Plan: jp_universe.py -> seal baselines -> provenance stamp -> unpriced-hunter-jp in waves of 5 -> edge_score.py -> note. No orders.

## Stage J — sealed
- Logged at 2026-10-07 01:06 UTC
- JPX sheets as_of 2026-10-01; 9 scheduled, 6 eligible (3 microcaps dropped: 6093, 8166, 9846), 6 hunted, selection: all eligible (under cap 25). 6 baselines sealed; JPX short register as_of 20260929. provenance: jp.v6 / claude-opus-5-5. Wave 1 (2670 2918 3391 428A 5932) spawned.

## Stage J — wave 1 partial
- Logged at 2026-10-07 01:12 UTC
- 2670 (-1.3) and 2918 (0.0) banked; 428A file written; 3391, 5932 and 6255 still hunting.

## Stage J — wave 1 progress
- Logged at 2026-10-07 01:13 UTC
- 428A (-1.7) and 5932 (-0.7) banked. 3391 and 6255 still hunting.

## Stage J — wave 1 complete
- Logged at 2026-10-07 01:14 UTC
- 3391 (+0.2) banked. Wave 1: 5/5 hunts written. Wave 2 (6255) in progress.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-07 01:17 UTC
- 6/6 hunted and scored; none above the 2.8 floor; range +0.20 (3391) to -1.70 (428A). Note: japan/japan-note.md. No orders.

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-07 06:41 UTC
- Fired 06:40 UTC 2026-10-07; sealing for the next ASX session (expected 2026-10-08). Plan: universe -> seal baselines -> provenance -> unpriced-hunter-au waves -> edge_score -> note.

## Stage AU — Australia researcher — EMPTY SESSION
- Logged at 2026-10-07 06:41 UTC
- Event date 2026-10-08 (next ASX session). 1575 vendor rows, 0 scheduled, 0 eligible, 0 hunted. market_open true (basis: 'beyond the tape: a weekday that is not an ASX holiday') — a genuinely thin session outside the Feb/Aug reporting seasons, not a fetch fault. Empty universe published at research/2026/10/2026-10-08/australia/universe.json; no baselines, no hunters, no ranking.

## Close AMC — 2026-10-07 10:11 UTC
- Logged at 2026-10-07 10:17 UTC
- Guard mode --require-exit-tif opg exit 0 (amc_open; amc exit placed as market DAY). verify: 14 legs, none UNFILLED, nothing held. close --submit: no legs due today, nothing sent, no refusals. Fill re-check clean; alpaca-orders.json rewritten with refreshed fill status only.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-07 13:39 UTC
- Fired 13:39 UTC 2026-10-07 (European markets still open; sealed spots are intraday, not closes). Sealing for event date 2026-10-08 (next European session). Plan: eu_universe -> seal baselines -> provenance -> one market hunter per name in waves of 5 -> edge_score -> note. No orders. Note: container's local main was a stale clone; checked out origin/main (275c92d6) before starting.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-07 13:43 UTC
- eu_universe.py --date 2026-10-08: 9 scheduled, 6 eligible at $100k floor, 6 hunted (all eligible, under cap 20): uk TSCO, NFG, FAN; de SZU; fr ALLIX; fi ADMCM. Largest market uk at 50%, 4 markets. No market_closed. Calendar sources: UK RNS calendar read (confirmed NFG/TSCO/FAN), Yahoo read in all ten, issuer calendars read (EQS, Inderes, Nasdaq fincal, Euronext Oslo, bankier). Baselines sealed ~13:43 UTC on intraday prices (not closes). anchor_covered true on 2 (FAN, NFG). provenance stamped (all hunters claude-opus-5-5). Wave 1: TSCO, NFG, FAN, SZU, ALLIX; wave 2: ADMCM.

## Stage EU — wave 1 banked
- Logged at 2026-10-07 13:52 UTC
- 5 of 5 hunts returned: TSCO -1.2, NFG +0.2, FAN +0.3, SZU +0.2, ALLIX -0.4 (impact_sum). SESSION ERROR: ALLIX (Wallix) was sealed bmo/session_unresolved for 2026-10-08, but the issuer's own 16 Jul release plus ABC Bourse's 'Après clôture' listing and prior H1 timestamps (18:30/18:45 Paris) put it AMC on 2026-10-08; the reaction window is 10-08 close -> 10-09 close. Baseline left sealed; hunter's session_check says amc; resolve must use the amc window. Wave 2: ADMCM (fi, nordic hunter).

## Stage EU — Europe researcher — DONE
- Logged at 2026-10-07 13:59 UTC
- Event date sealed for: 2026-10-08. 6 hunters, 6 hunts returned, 0 shed. edge_score ranking_key impact_sum: FAN +0.30, NFG +0.20, SZU +0.20, ADMCM -0.30, ALLIX -0.40, TSCO -1.20; 0 of 6 above floor 2.8. ALLIX is amc (resolve on 10-08 close -> 10-09 close). Note: europe-note.md. Publishing with EARNINGS_DATA_BRANCH=main.

## Stage EU — publish verified
- Logged at 2026-10-07 13:59 UTC
- git log -1 origin/main shows f6f6cae4 'stage EU: Europe ranking for 2026-10-08' — the run is on main.
