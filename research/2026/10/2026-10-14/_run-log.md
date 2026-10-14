# Run log — 2026-10-14

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-13 06:41 UTC
- Sealing for the next ASX session (2026-10-14). Plan: universe -> seal baselines -> one unpriced-hunter-au per name in waves of 5 -> edge_score -> four-model panel -> note.

## Stage AU — Australia researcher — EMPTY UNIVERSE
- Logged at 2026-10-13 06:41 UTC
- Funnel 0 / 0 / 0: 1575 vendor rows scanned, none dated 2026-10-14 after the Sydney shift. market_open true (basis: 'beyond the tape: a weekday that is not an ASX holiday'), so this is a genuinely thin ASX session outside the Feb/Aug seasons, not a shut exchange and not a tape fault. No baselines sealed, no hunters, no panel, no orders (this stage has none).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-13 13:39 UTC
- Fired 13:38 UTC 2026-10-13 (European markets still open; sealed spot is intraday). Sealing for EVENT DATE 2026-10-14 (Wed), the next European trading day.
- Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model panel -> note. No orders.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-13 13:49 UTC
- 10 scheduled, 7 eligible (uk 4, se 2, dk 1), all 7 hunted (under cap 20). Dropped below $100k: RWA, ALSMA, DUST. Largest market uk 57%. Yahoo quote calendar unavailable on every market. Provenance stamped (orchestrator model flag omitted: get_session not callable here). Wave 1: BOOM JHD SCT VTU DEMANT; wave 2: AVARDA CRED_A.

## Stage EU — panel STARTED
- Logged at 2026-10-13 13:59 UTC
- 7 hunts done (DEMANT phantom: Q3 IMS is 2026-11-03; 14 Oct is the start of its quiet period). 6 ranked, 0 above 2.8. Packs built; four judges next.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-13 14:05 UTC
- Event date 2026-10-14. 6 ranked (AVARDA +1.60, VTU +1.60, BOOM +1.20, CRED_A +0.10, SCT +0.10, JHD -0.60), 0 above floor 2.8. DEMANT not ranked: phantom row (Q3 IMS is 2026-11-03; amend event_occurred:false after the window).
- Panel: 4/4 members, no fallback, 0 selected (AVARDA k=2). Note: europe-note.md. Resolve within ~a week (SE/DK Nordic feed window). Published with EARNINGS_DATA_BRANCH=main.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-14 01:05 UTC
- 2026-10-14T01:05:20Z: universe (JPX kessan, ¥15m floor, cap 25 random draw) -> seal baselines -> one unpriced-hunter-jp per name in waves of 5 -> edge_score -> four-model panel -> note. No orders.

## Stage J — resolved 2026-10-09 run (from the 10-14 session)
- Logged at 2026-10-14 01:07 UTC
- jp_resolve: 25/25 usable, rho impact_sum 0.535 p 0.0073, free control -0.112, sign right 0.72, lean_vs_free_control_rho 0.367. Panel: rho 0.471 p 0.018; 1 selected, 0 hits (-1.43%). One day is not a result.

## Stage J — panel STARTED
- Logged at 2026-10-14 01:41 UTC
- 25 hunts banked and scored (edge-scores.json, key impact_sum). 25 packs, four judges.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-14 01:52 UTC
- 90 scheduled / 50 eligible / 25 hunted (seeded random draw). 25/25 hunts, 0 empty. Top 9168 +1.50, bottom 6086 -1.00, none above floor 2.8; 16+/8-/1 zero. Panel 4/4 members, no fallback: 1 selected, 1434 JESCO 4/4. Register as_of 2026-09-29 (stale). Prov jp.v5. Note: japan-note.md. No orders.

## Close AMC — 2026-10-14 10:10 UTC
- Logged at 2026-10-14 10:15 UTC
- Guard mode --require-exit-tif opg exit 0 (amc_open, amc->day queued for open). verify: 14 legs, none still held, none UNFILLED with shares held. close --submit: 12 runs scanned, no leg due today, 0 orders sent, 0 refusals. Account reachable.

## Stage IPO — IPO researcher — STARTED
- Logged at 2026-10-14 12:36 UTC
- Fired 12:36 UTC (08:36 ET). Plan: universe → seal → hunters (waves of 6) → score → four-model IPO panel → note. No orders.

## Stage IPO — panel STARTED
- Logged at 2026-10-14 12:47 UTC
- 1 pack (MAIR), four IPO judges. ARXS not ranked: hunter found lock-up lapsed 2026-10-13 (424B4 dated 2026-04-15, 180 days → 10-12); Nasdaq date one day late.

## Stage IPO — IPO researcher — DONE
- Logged at 2026-10-14 12:49 UTC
- 2 lock-ups hunted (ARXS, MAIR), 0 debuts (1 SPAC dropped). MAIR ranked: impact_sum +0.45, panel_pct 10, not selected; all four judges ran. ARXS not ranked: the hunter dates its first free session to 2026-10-13. Possible off-by-one in the lock-up event date in ipo_universe.py, flagged in the note and not fixed. No price from inside the window was seen.

## Intraday panel 10:00 — STARTED
- Logged at 2026-10-14 13:58 UTC
- First snapshot of the day: build universe (--window), one edge-sweep, freeze names, seal baselines, one unpriced-searcher per name, guard, score, four judges, panel_score --dry-run --stage E-PI. No orders.

## Intraday panel 10:00 — panel STARTED
- Logged at 2026-10-14 14:24 UTC
- 17 searchers done (unpriced-searcher, Opus 5.5), guard moved nothing (ran 14:24 UTC), 17 packs, four judges.

## Intraday panel 10:00 — done
- Logged at 2026-10-14 14:31 UTC
- 17/17 hunted (unpriced-searcher, Opus 5.5), guard moved nothing, all four judges 17/17, panel scored --dry-run --stage E-PI (history untouched). Selected: CMTL short (panel_pct 96, 4/4 own top 20%). No orders. Timeline at edge-intraday/timeline.md.

## Intraday panel 12:00 — STARTED
- Logged at 2026-10-14 15:58 UTC
- Fired 15:58 UTC (11:58 ET). Names frozen by 10:00: seed, re-seal baselines, one unpriced-searcher per name (amc first), guard, score, four judges, panel_score --dry-run --stage E-PI. No orders.

## Edge hunt — 2026-10-14 amc + 2026-10-15 bmo — STARTED
- Logged at 2026-10-14 17:07 UTC
- Fired 17:04 UTC. Universe 17 of 40 calendar rows (4 amc 10-14: HOMB EQBK CMTL EDUC; 13 bmo 10-15). Baselines sealed for all 17 (9 with option-implied move). Plan: 1 sweep + up to 17 hunters (cap 19).
- Step 0b: execution.enabled true, exit_mode amc_open. 'alpaca_trade.py verify --scan ... --fix --submit' DENIED by the auto-mode classifier [Real-World Transactions], twice, including the exact narrow form. Read-only status: equity $11,200.86 = cash, no open positions, so nothing was due and the denial cost nothing.

## Edge hunt (panel) — 2026-10-14 amc + 2026-10-15 bmo — STARTED
- Logged at 2026-10-14 17:09 UTC
- Fired 17:06 UTC (13:06 ET). Universe 17 of 40 rows (4 amc 10-14, 13 bmo 10-15); own baselines sealed for all 17 in edge-panel/. Plan: 1 edge-sweep + up to 17 unpriced-searcher (Opus 5.5), then 4 blind judges. No orders.

## Edge hunt (panel, Fable) — 2026-10-14 amc + 2026-10-15 bmo — STARTED
- Logged at 2026-10-14 17:11 UTC
- Stage E-PF: 17 names in window (4 amc 10-14, 13 bmo 10-15), baselines sealed 17:11Z in edge-panel-fable/baselines. Plan: one edge-sweep, one unpriced-searcher-fable (claude-fable-5-1) per confirmed name, four blind judges, panel_score --dry-run --stage E-PF. No orders.

## Edge hunt — 2026-10-14 amc + 2026-10-15 bmo — DONE
- Logged at 2026-10-14 17:31 UTC
- Sweep: 17 of 17 confirmed, 0 phantom, 0 session unsettled. 17 hunters, one per name, all returned under the current contract (pre_lessons, print_vs_bar_pct, abs_move_pct/p_up present). Correction to the STARTED line: 10 of 17 baselines had a live option chain, not 9.
- Scored: ranking_key impact_sum. 17/17 rankable, 0 clear the 2.8 floor (max BNY +1.85). impact_scaled max |CMTL -1.50| < 1.76. V2 calibrated on 186 obs. Sign balance 9+/1 zero/7-. Spearman(key, -run_up_20d) = +0.10.
- Step 7: execution.enabled true; 'plan' found NO name meeting |impact_scaled| >= 1.76, so 'open --submit' was not called. Orders accepted 0, gross 0% of equity ($11,200.86). All 17 refused: below the conviction floor. Step 0b sold nothing (account flat); its verify/close --submit call was DENIED by the auto-mode classifier [Real-World Transactions], same as 10-13 - the narrow allow rules in .claude/settings.json are still not holding for --submit calls.
- Step 6c (shadow ledger) skipped. Step 6d context written (search failed for BNY, SCHW, PNC, HOMB, EQBK).

## Edge hunt (panel) — panel STARTED
- Logged at 2026-10-14 18:17 UTC
- Resumed 18:2x UTC from a second session after the first hit a usage limit. 16 of 17 searchers done; PNC's searcher did not finish and is shed (not ranked: no hunt). Scored 16/16 rankable, 0 clear 2.8. V2 written before the first print. 16 packs, four judges.

## Intraday panel 12:00 — RESUMED
- Logged at 2026-10-14 18:20 UTC
- Resumed 18:3x UTC (14:3x ET) from a second session after the first hit a usage limit; status partial: 7 of 17 hunts, baselines kept (sealed at the 12:00 slot). Relaunching the 10 missing unpriced-searchers (CMTL amc first). These 10 hunts search at ~14:30 ET, not 12:00, so this snapshot is a 12:00 seal with mixed search times; recorded, not corrected.

## Edge hunt (panel, Fable) — RESUMED
- Logged at 2026-10-14 18:20 UTC
- Resumed 18:3x UTC from a second session after the first hit a usage limit: 8 of 17 hunts on disk, baselines kept. Relaunching the 9 missing unpriced-searcher-fable (all bmo 10-15).

## Intraday panel 12:00 — panel STARTED
- Logged at 2026-10-14 18:22 UTC
- The 10 relaunched searchers were stopped on the operator's instruction; the snapshot is scored on the 7 hunts the first session wrote (CMC EDUC EQBK ERIC HOMB MAN WIT); the other 10 names are not ranked (no hunt). Guard run. 7 packs, four judges.

## Edge hunt (panel, Fable) — panel STARTED
- Logged at 2026-10-14 18:24 UTC
- On the operator's instruction no further searchers were run, so the hunted set matches what the first session had: 8 of 17 hunts (CMC CMTL EDUC EQBK ERIC HOMB MAN WIT); the other 9 are not ranked (no hunt). 8 packs, four judges.

## Edge hunt (panel) — 2026-10-14 amc + 2026-10-15 bmo — DONE
- Logged at 2026-10-14 18:27 UTC
- 16/17 hunted (unpriced-searcher, Opus 5.5); PNC shed, its searcher unfinished when the first session hit a usage limit. Resumed and finished by a second session from 18:17 UTC. All four judges 16/16 (pinned agents). panel_score: selected CMTL short (panel_pct 93, 4/4 own top 20%, E[return] +4.44%). Searcher: 0 over the 2.8 floor. rho stage E vs panel +0.355 (n=16). No orders. Panel history +64 sizes.

## Intraday panel 12:00 — done
- Logged at 2026-10-14 18:28 UTC
- 7/17 hunted (unpriced-searcher, Opus 5.5; the 10 missing searchers stopped on the operator's instruction, so only slot-time searches count), guard moved nothing, all four judges 7/7, panel scored --dry-run --stage E-PI (history untouched). Selected: none (ERIC 74 long closest). No orders. Timeline rebuilt.
