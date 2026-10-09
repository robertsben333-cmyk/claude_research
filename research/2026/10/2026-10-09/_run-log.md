# Run log — 2026-10-09

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-09 01:05 UTC
- 01:05 UTC fire on main 044eb7c. Plan: jp_universe (cap 25, ¥15m floor, seeded draw) → seal baselines → provenance stamp → unpriced-hunter-jp in waves of 5 → edge_score → 4-model panel (step 4p) → note → publish. No orders.

## Stage J — universe and baselines sealed
- Logged at 2026-10-09 01:06 UTC
- 65 scheduled / 31 eligible (34 under ¥15m) / 25 hunted; selection: random sample of 31 eligible, seed jp-2026-10-09. calendar_as_of 2026-10-01. Baselines quality 0.6 (0.45 for 2698, 7603, 7713: no margin ratio). JPX short register as_of 20260929. Provenance jp.v6 · claude-opus-5-5.

## Stage J — resolved earlier run
- Logged at 2026-10-09 01:07 UTC
- jp_resolve.py on 2026-10-07: 6/6 usable, rho -0.087 p 0.86, free control 0.543, lean_vs_free_control_rho 0.029 (well below 1.0; positioning still resolving). 2026-10-08 window closes at today's close, not yet.

## Stage J — first hunt banked
- Logged at 2026-10-09 01:11 UTC
- 2698 +0.20 (rolling 5 concurrent; 2735, 3046, 3048, 3063, 3201 in flight).

## Stage J — wave 1 banked
- Logged at 2026-10-09 01:14 UTC
- 2698 +0.20, 2735 +0.40, 3046 +0.10, 3048 -0.50 (releases 12:00 JST, in session), 3063 -0.25. Rolling 5: 3201, 3222, 3501, 4440, 4443 in flight.

## Stage J — wave 2 banked
- Logged at 2026-10-09 01:21 UTC
- 3201 +0.30, 3222 -0.20, 3501 -0.05, 4440 -0.60 (12:00 JST, in session), 4443 banked. In flight: 4829, 4992, 6264, 6289, 6506, 6814; queued 7603..9974.

## Stage J — wave 3 banked
- Logged at 2026-10-09 01:28 UTC
- 4443 -0.10, 4829 -1.90 (16:00 JST), 4992 +0.25, 6289 +1.10, 6814 +1.20 (H1 pre-released 10-06; FY forecast and dividend deferred to this print), 7603 -0.30. In flight: 6264, 6506, 7713, 7888, 8008; queued 8200, 8244, 9270, 9740, 9974.

## Stage J — wave 4 banked
- Logged at 2026-10-09 01:34 UTC
- 6264 -1.50, 6506 +1.50 (16:00 JST), 7713 +1.60 (15:00 JST, in session), 8008 banked. In flight: 7888, 8200, 8244, 9270, 9740, 9974 (last six).

## Stage J — scored
- Logged at 2026-10-09 01:42 UTC
- 25 of 25 rankable; 0 above the 2.8 floor; top 7713 +1.60, bottom 4829 -1.90; 13 positive / 12 negative (impact_sum).

## Stage J — panel STARTED
- Logged at 2026-10-09 01:42 UTC
- 25 packs, four judges (panel-judge-intl-opus5/-opus55/-sonnet55/-fable51)

## Stage J — Japan researcher — DONE
- Logged at 2026-10-09 01:52 UTC
- 65/31/25 (random draw seed jp-2026-10-09); 25 of 25 rankable, 0 above the 2.8 floor; top 7713 +1.60, bottom 4829 -1.90; 13 positive / 12 negative. Panel: 4 of 4 members, selected 6264 (-1.51, k=4). Note: research/2026/10/2026-10-09/japan/japan-note.md. JPX short register as_of 2026-09-29 (10 days stale).

## Close AMC — 2026-10-09 10:15 UTC
- Logged at 2026-10-09 10:20 UTC
- mode --require-exit-tif opg exit 0 (amc_open, amc->day). verify: 14 legs, none UNFILLED, nothing held. close --submit: no leg due today, no exit orders sent, no refusals. alpaca-orders.json rewritten for 12 runs (fill refresh only).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-09 13:40 UTC
- Fired 13:38 UTC 2026-10-09 (Friday; European markets still open, sealed spots are intraday, not closes). Sealing for event date 2026-10-12 (Monday, next European session). Plan: eu_universe -> seal baselines -> provenance -> one market hunter per name in waves of 5 -> edge_score -> panel -> note. No orders. Note: origin/main was force-rewritten (no merge base with the container's stale local main); working from a branch off origin/main ea9ad133, pushing HEAD:main.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-09 13:43 UTC
- eu_universe.py --date 2026-10-12: 5 scheduled (uk 4, pl 1), 3 eligible at $100k floor, 3 hunted (all eligible, under cap 20): uk FXPO (Ferrexpo, rns), SDG (Sanderson Design, vendor+rns), SWC (Smarter Web Company, rns). Dropped below floor: AREC ($27k/day), pl HPM ($2k/day). Concentration 100% uk, 1 market. No market_closed. Calendar: UK RNS calendar read (added AREC/SWC/FXPO, confirmed SDG), Yahoo read in all ten (0 added), issuer calendars read (EQS, Inderes, Nasdaq fincal, Euronext Oslo, bankier). All three session_unresolved (defaulted bmo). Baselines sealed ~13:45 UTC on intraday prices (not closes); FCA register read as_of 2026-10-08, anchor_covered true on 1 (FXPO 0.38%); history observed_rns on all 3. provenance stamped (uk.v7, claude-opus-5-5). Wave 1 of 1: 3 unpriced-hunter-uk launched.
