# Run log — 2026-10-13

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-12 06:41 UTC
- Fired 06:40 UTC Mon 2026-10-12; sealing for the next ASX session (2026-10-13). Plan: au_universe -> seal baselines -> provenance -> unpriced-hunter-au waves -> edge_score -> four-model panel -> note. No orders.

## Stage AU — Australia researcher — EMPTY UNIVERSE
- Logged at 2026-10-12 06:41 UTC
- au_universe.py: 1575 vendor rows, 0 scheduled for 2026-10-13, 0 eligible, 0 hunted. market_open=true (basis: weekday, not an ASX holiday; the index tape read cleanly, so this is not a fetch fault). A thin Australian session outside the Feb/Aug reporting seasons. No baselines sealed, no hunters, no panel. Published universe.json and stopped.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-12 13:40 UTC
- Fired 13:39 UTC 2026-10-12. Sealing for event date 2026-10-13 (next European session). Plan: universe -> baselines -> provenance -> hunters in waves of 5 -> score -> 4-model panel -> note. Local main was a stale divergent snapshot; worked from origin/main on a local branch, publish pushes HEAD:main.

## Stage EU — universe sealed
- Logged at 2026-10-12 13:50 UTC
- 11 scheduled, 6 eligible (uk 5, no 1), all 6 hunted (under cap 20). Concentration: uk 83%. Baselines sealed for ABG, BWY, BYIT, ENSI, GNC, YOU. Yahoo quote calendar unavailable on every batch. Wave 1 = 5 UK hunters; wave 2 = ABG (nordic/no).

## Stage EU — wave 1 done
- Logged at 2026-10-12 13:57 UTC
- 5 UK hunters returned: BWY -1.0, BYIT -0.85, GNC +0.9, YOU +0.4, ENSI event_confirmed false (results were 2026-10-05; 13 Oct is an IMC presentation). ABG (no) running.

## Stage EU — panel STARTED
- Logged at 2026-10-12 13:58 UTC
- 5 packs, four judges

## Stage EU — Europe ranking for 2026-10-13 — DONE
- Logged at 2026-10-12 14:03 UTC
- Sealed for 2026-10-13 (next European session). 6 eligible (uk 5, no 1), 5 ranked, 0 above floor 2.8. Top GNC +0.90, bottom BWY -1.00. ENSI phantom (results 2026-10-05; rns calendar read an IMC presentation date). Panel: 4/4 members, 0 selected. Pushed to main via publish.sh (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-13 01:05 UTC
- Fired 01:05 UTC 2026-10-13 (10:05 JST). Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp waves -> edge_score -> four-model panel -> note. Research only, no orders.

## Stage J — universe sealed
- Logged at 2026-10-13 01:07 UTC
- 51 scheduled, 30 eligible above ¥15m turnover, 25 hunted by random draw seed jp-2026-10-13. 25 baselines sealed. Provenance jp.v5 · claude-opus-5-5. JPX short register as_of 20260929 (stale vs run date). Wave 1 (1401 1419 2379 2653 2791) launched 01:11 UTC.

## Stage J — wave 1 banked
- Logged at 2026-10-13 01:18 UTC
- 1401 1419 2379 2653 2791 hunted (5/5 non-empty). Running rolling at wave_size 5 concurrency.

## Stage J — hunts complete
- Logged at 2026-10-13 01:44 UTC
- 25/25 hunted, 0 empty. Scoring.

## Stage J — panel STARTED
- Logged at 2026-10-13 01:44 UTC
- 25 packs, four judges (panel-judge-intl-*)

## Stage J — Japan researcher — DONE
- Logged at 2026-10-13 01:54 UTC
- 51 scheduled / 30 eligible / 25 hunted (seeded draw). 25/25 rankable, none above floor 2.8; top 9278 +2.20, bottom 2791 -1.30. Panel 4/4 members, selected 6432, 9278, 2791. JPX short register as_of 2026-09-29 (stale). Note: japan/japan-note.md. No orders.

## Close AMC — 10:00 UTC routine
- Logged at 2026-10-13 10:16 UTC
- mode --require-exit-tif opg: exit 0 (amc_open, amc exit queued as DAY market for the open). verify: 14 legs, none UNFILLED, nothing still held. close --submit: no leg due today, nothing sent, no refusals. alpaca-orders.json files rewritten by the fill re-read.

## Stage IPO — IPO researcher — STARTED
- Logged at 2026-10-13 12:37 UTC
- Routine fire 12:36 UTC; universe for 2026-10-13, seal, hunt up to 12 names in waves of 6, score, four-model IPO panel. No orders.

## Stage IPO — IPO researcher — EMPTY DAY
- Logged at 2026-10-13 12:49 UTC
- NYSE open (market_closed null); eligible 0: no debut first-trades today and no lock-up's first free session is today. Funnel all zeros (debut_scheduled 0, lockup_scheduled 0). Nasdaq calendar fetched OK at 12:37 UTC (Oct: 5 priced, 2 upcoming — IAM expected 10/15, CTY 10/16), so this is a real empty day, not a fetch failure. No hunters, no panel, no orders. Note: the container lacked the 'requests' module; installed with pip before ipo_universe.py would run.

## Edge hunt — 2026-10-13 amc + 2026-10-14 bmo — STARTED
- Logged at 2026-10-13 17:09 UTC
- 17:05 UTC fire. 9 of 26 calendar rows in window (AZZ amc; ASML BAC MS BLK PGR FAST STT SOTK bmo). Baselines sealed (8 with option chains, SOTK none). Plan: 1 sweep + up to 9 hunters.
- Step 0b: execution.enabled true, exit_mode amc_open. 'alpaca_trade.py verify --fix --submit' was DENIED by the auto-mode classifier [Real-World Transactions] - the narrow allow rules did not hold. Read-only 'status' worked: equity $11,200.86 = cash, no open positions, so nothing was due to sell and the denial cost nothing today.
## Edge hunt (panel) — 2026-10-13 amc + 2026-10-14 bmo — STARTED
- Logged at 2026-10-13 17:09 UTC
- Stage E-P, 17:09Z. 9 names in window (ASML BAC MS BLK PGR FAST STT AZZ SOTK); 13 with --include-unknown, session_resolve killed UNTY (8-K 2.02 filed 10-13), carried BMRA/FNGR/NXTT unresolved, none confirmed, so they stay out. Baselines sealed into edge-panel/baselines (8 with option chain, SOTK none). Plan: 1 edge-sweep, up to 9 unpriced-searcher, 4 blind judges. No orders.

## Edge hunt — sweep
- Logged at 2026-10-13 17:14 UTC
- Sweep confirmed 9 of 9 from company sources, 0 phantom, 0 session unsettled. Unknown-session check (session_resolve.py): 4 time-not-supplied rows, UNTY killed (8-K 2.02 filed 2026-10-13), BMRA/FNGR/NXTT carried unresolved with no announcement - not added. 9 hunters, one per name; 8 launched at once, BAC queued on the 8-concurrent ceiling.

## Edge hunt — 2026-10-13 amc + 2026-10-14 bmo — DONE
- Logged at 2026-10-13 17:25 UTC
- 9 hunters returned, all with pre_lessons and print_vs_bar_pct (us.v9, claude-opus-5-5). edge_score.py: 9/9 rankable, ranking_key impact_sum, 0 clear the 2.8 floor. Top ASML/MS +1.60, bottom SOTK -0.70. V2 grounded written (9/9, 186 ledger obs). Spearman vs -run_up_20d +0.23.
- Step 7: execution.enabled true, but 'plan' found NO name meeting |impact_scaled| >= 1.76 (max 0.65 SOTK), so 'open --submit' was not called - nothing to place. Step 0b sold nothing (the account held no positions; the verify/close --submit call was denied by the auto-mode classifier). Orders accepted 0, gross 0% of equity ($11,201). All 9 refused: below the conviction floor.
- Step 6c (shadow ledger) skipped this run. Step 6d context written (search failed for MS and SOTK). Operator notified that broker submit calls are denied again in auto mode despite the narrow allow rules in .claude/settings.json.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-10-13 17:31 UTC
- 9 of 9 searchers returned (unpriced-searcher, native agent). edge_score: 9/9 rankable, 0 clear the 2.8 floor (max |impact_sum| 0.97 BAC). V2 grounded written 17:31Z, 9/9 calibrated. 9 packs, four judges launching.

## Edge hunt (panel) — DONE
- Logged at 2026-10-13 17:39 UTC
- Four judges ran on pinned agents (opus5, opus55, sonnet55, fable51), 9/9 ids each, no retries. panel_score: 0 selected (SOTK k=2, PGR k=1). rho stage E impact_sum vs panel_score +0.745 (n=9). Searcher: 0 over 2.8 floor. No alpaca_trade.py call, no shadow ledger. Note at edge-panel/edge-note.md.
