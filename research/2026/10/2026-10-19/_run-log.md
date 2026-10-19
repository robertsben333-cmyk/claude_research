# Run log — 2026-10-19

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-16 13:41 UTC
- Fired 13:41 UTC Fri 2026-10-16; sealing for event date 2026-10-19 (Mon, next European session). Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model intl panel -> note. No orders.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-16 13:50 UTC
- Event date 2026-10-19. 8 scheduled, 4 eligible (uk 3, se 1), all 4 hunted (under cap 20). Largest market uk 75%. Yahoo calendar quote endpoint unavailable on all ten markets this run (calendar rests on vendor + RNS + issuer calendars). UK register as of 2026-10-15, SE as of 2026-10-16; anchor_covered: ITM only (1 of 4). history observed_rns for BKS/ITM/TSTL, estimated (hist=0) for AIRA. session_unresolved: AIRA, ITM. Provenance stamped (uk/nordic hunters, claude-opus-5-5). One wave: [AIRA(se) BKS ITM TSTL].

## Stage EU — panel STARTED
- Logged at 2026-10-16 14:02 UTC
- 4 hunts done; 4 ranked, 0 above 2.8 (BKS -0.60, TSTL -0.60, ITM -1.10, AIRA -1.20). 4 packs, four judges (intl).

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-16 14:06 UTC
- Event date 2026-10-19. 4 ranked (uk 3, se 1): BKS -0.60, TSTL -0.60, ITM -1.10, AIRA -1.20; 0 above floor 2.8. AIRA and ITM sealed bmo? and both confirmed bmo by the issuer. Yahoo calendar unavailable on all ten markets.
- Panel: 4/4 members, no fallback; 1 selected: ITM short (k=3, panel_pct 80). AIRA panel_pct 82 at k=2. Note: europe-note.md. Resolve AIRA within ~a week (Nordic feed window; issuer publishes via MFN). Published with EARNINGS_DATA_BRANCH=main.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-19 01:05 UTC
- Fired 01:04 UTC 2026-10-19 (10:04 JST). Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp in waves of 5 (cap 25) -> edge_score -> four-model intl panel -> japan-note. Research only, no orders.

## Stage J — wave 1 STARTED
- Logged at 2026-10-19 01:06 UTC
- 4 scheduled / 4 eligible / 4 hunted (all, under cap 25): 3295 3481 3488 8984, all J-REIT Aug-period results. Baselines sealed, provenance jp.v5. Previous resolved run (2026-10-13) lean_vs_free_control_rho 0.406.

## Stage J — wave 1 done
- Logged at 2026-10-19 01:14 UTC
- 4 of 4 hunts returned. Note: hunter 3295 reported a shared scratch-file collision (a y.json overwritten with 3481.T bars); it re-fetched its own data into a per-ticker folder before using it.

## Stage J — panel STARTED
- Logged at 2026-10-19 01:14 UTC
- 4 packs, four judges

## Stage J — Japan researcher — DONE
- Logged at 2026-10-19 01:17 UTC
- 4/4/4 hunted, all J-REIT amc. impact_sum: 3295 +0.40, 8984 +0.30, 3481 +0.10, 3488 -0.40; none above 2.8. Panel 4 of 4 members, none selected; panel's largest is 3481 short (pct 25). Note: japan/japan-note.md.

## Close AMC — 2026-10-19 10:10 UTC
- Logged at 2026-10-19 10:16 UTC
- Guard mode --require-exit-tif opg: exit 0 (amc_open, amc->day, matched on placement). verify: 14 legs, none UNFILLED, nothing still held. close --submit: no leg due today, nothing sent, no refusals. Fill check re-read the 14 legs; alpaca-orders.json files rewritten by the fill check only. status printed no output.

## Stage M — morning exit review — STARTED
- Logged at 2026-10-19 12:57 UTC
- source research/2026/10/2026-10-16/edge-panel, now 08:57 EDT

## Stage M — morning exit review — done
- Logged at 2026-10-19 13:00 UTC
- 1 name: CLF exit_close (Wachten tot slot). Pool: no prior morning (first fire, n=0).

## Intraday panel 10:00 — STARTED
- Logged at 2026-10-19 14:00 UTC
- Stage E-PI snapshot 1000 (first of day, names not frozen): universe --window, one edge-sweep, freeze, seal, one unpriced-searcher per name, guard, score, four blind judges, panel_score --dry-run --stage E-PI. No orders.

## Intraday panel 10:00 — names frozen
- Logged at 2026-10-19 14:12 UTC
- Universe 38 (17 amc 10-19, 21 bmo 10-20); sweep confirmed 37, CBSH unconfirmed (aggregators disagree, no 8-K). Names frozen to edge-intraday/names.json. Budget cap 19 hunted: shed by lowest hunt_priority GE RTX GM NOC STLD WRB HAL KEY CCK AGNC WTFC ZION BOKF FNB AUB UCB PEBO MBWM (recorded in intraday.json 'shed'; their baselines stay so they appear unrankable). Hunting: VICR KARO WASH HAS EFX RBB CCBG AERO SFBS HBCP WAL MSCI SMBK RLI VMI SYF ALLY GPC MMM, amc first.

## Intraday panel 10:00 — panel STARTED
- Logged at 2026-10-19 14:35 UTC
- 19/19 hunted (unpriced-searcher, Opus 5.5); guard at 14:35 UTC moved nothing; edge_score 19 rankable, 0 clear 2.8. Packs built, four judges.

## Intraday panel 10:00 — done
- Logged at 2026-10-19 14:41 UTC
- 19/19 hunted (unpriced-searcher, Opus 5.5), guard moved nothing, all four judges 19/19 (opus5, opus55, sonnet55, fable51 on their pinned ids), panel scored --dry-run --stage E-PI (history untouched). Selected: EFX short (90), AERO short (89). 18 confirmed names shed for budget, CBSH unconfirmed. No orders. Timeline at edge-intraday/timeline.md.

## Intraday panel 12:00 — STARTED
- Logged at 2026-10-19 15:59 UTC
- Stage E-PI snapshot 1200, names frozen by 1000: seed, re-seal, one unpriced-searcher (Opus 5.5) per hunt name, amc first, guard, score, four blind judges, panel_score --dry-run --stage E-PI. No orders.

## Intraday panel 12:00 — wave 1
- Logged at 2026-10-19 16:02 UTC
- Seeded from names.json (frozen by 1000). Same 19 hunt names as 1000 (frozen sweep, same priorities); 18 shed for budget, recorded in intraday.json. 37 baselines sealed 16:01-16:03 UTC. 8 searchers launched (platform cap 8): KARO WASH RBB AERO SFBS HBCP WAL SMBK; RLI and 10 bmo names queued.

## Intraday panel 12:00 — independence breach, VICR
- Logged at 2026-10-19 16:11 UTC
- VICR searcher reported it read edge-intraday-1000/hunts/VICR.json before searching (it found it on disk; the brief did not point to it). Hunt moved to edge-intraday-1200/_contaminated/VICR.json, unscored. VICR re-run with an explicit read restriction (20th subagent, inside the cap). Later launches (GPC, MMM, VICR rerun) carry the same restriction; none of the 9 finished hunts names an earlier snapshot path in its file. All 9 amc hunts done by 16:11 UTC. Searchers disagree on whether the Fed hiked on 2026-09-16 (most say yes, HBCP says held since Dec 2025): left as filed, judges see both.

## Intraday panel 12:00 — panel STARTED
- Logged at 2026-10-19 16:20 UTC
- 19/19 hunted (unpriced-searcher, Opus 5.5; VICR re-run after the independence breach). Guard at 16:20 UTC moved nothing. edge_score 19 rankable, 0 clear 2.8. 19 packs, four judges.

## Intraday panel 12:00 — done
- Logged at 2026-10-19 16:27 UTC
- 19/19 hunted (unpriced-searcher, Opus 5.5; VICR re-run after independence breach, first attempt in _contaminated/), guard moved nothing, all four judges 19/19 on pinned ids, panel scored --dry-run --stage E-PI (history untouched). Selected: EFX short (94), AERO short (87). No orders. Timeline rebuilt.

## Edge hunt (panel) — 2026-10-19 amc + 2026-10-20 bmo — STARTED
- Logged at 2026-10-19 17:19 UTC
- Stage E-P. Universe 38 (17 amc 10-19, 21 bmo 10-20), 38 baselines sealed in edge-panel/baselines before any search. Plan: one edge-sweep, up to 19 unpriced-searcher (Opus 5.5), then four blind judges. No orders.
## Edge hunt (panel, Fable) — 2026-10-19 amc + 2026-10-20 bmo — STARTED
- Logged at 2026-10-19 17:11 UTC
- Stage E-PF. Universe 38 (17 amc 10-19, 21 bmo 10-20), 38 baselines sealed 17:10-17:11 UTC into edge-panel-fable/. Plan: one edge-sweep, up to 19 unpriced-searcher-fable (claude-fable-5-1) searchers by hunt_priority, then four blind judges, panel_score --dry-run --stage E-PF. No orders.

## Edge hunt (panel, Fable) — sweep
- Logged at 2026-10-19 17:21 UTC
- Sweep confirmed 36 of 38 (WAL, CBSH unconfirmed, 0 phantoms). Cap 19 hunted by hunt_priority: VICR KARO AERO HAS STLD VMI RBB GPC WASH RLI EFX SMBK CCK SFBS MSCI CCBG ALLY ZION MBWM. Shed for budget (lowest priority): SYF HBCP AGNC GM PEBO HAL WTFC MMM AUB NOC BOKF GE FNB RTX UCB KEY WRB. Searchers: unpriced-searcher-fable, amc first, 8 concurrent. Each brief forbids reading any other stage's directory (after the E-PI VICR breach).
