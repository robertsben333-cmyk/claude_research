# Run log — 2026-10-05

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-02 13:39 UTC
- Fired 13:38Z 2026-10-02 (Fri), sealing for event date 2026-10-05 (Mon, next European trading day). Working tree = origin/main d1db8e7 on local branch eu-run (local main had diverged from a force-updated origin; not used). Plan: eu_universe -> eu_priced_in seal -> provenance stamp -> one market hunter per name in waves of 5 -> edge_score -> europe-note. No orders. Publishing to main (EARNINGS_DATA_BRANCH=main).

## Stage EU — Europe researcher — DONE (empty day)
- Logged at 2026-10-02 13:39 UTC
- Event date 2026-10-05. All ten calendars read, none market_closed. 1 scheduled (BON.PA, fr), 0 eligible: dropped below the $100k floor at $84,308/day. Floor not lowered. 0 hunted, no baselines, no scoring, nothing to resolve. Universe and note in research/2026/10/2026-10-05/europe/. No orders. Pushed to main (EARNINGS_DATA_BRANCH=main).

## Stage AU — Australia researcher — EMPTY DAY
- Logged at 2026-10-04 06:40 UTC
- Fired 2026-10-04 06:40 UTC (Sunday), sealing for ASX session 2026-10-05. Repo: existing checkout, reset local main to origin/main (force-updated remote).
- Universe: 1575 vendor rows scanned, 0 scheduled, 0 eligible, 0 hunted. market_open true (basis: weekday not an ASX holiday, beyond the tape) — a genuinely thin off-season Australian session, not a fault. No hunters spawned, no baselines sealed.
- Universe file: research/2026/10/2026-10-05/australia/universe.json

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-05 01:05 UTC
- Fired 01:05Z on main @ 119187b. Plan: jp_universe -> seal baselines -> provenance stamp -> unpriced-hunter-jp in waves of 5 -> edge_score -> note. Research only, no orders.

## Stage J — sealed
- Logged at 2026-10-05 01:06 UTC
- universe: 15 scheduled / 11 eligible (4 dropped on ¥15m turnover) / 11 hunted, selection 'all 11 eligible names (at or under the cap)', calendar_as_of 2026-10-01. 11 baselines sealed 01:05Z, short register file 20260929. provenance jp.v6 · claude-opus-5-5 (alias_timeline). Wave 1 (1376 2753 3148 3186 3498) spawned.

## Stage J — wave 1 banked
- Logged at 2026-10-05 01:13 UTC
- 4 of 5 back (1376 2753 3148 3498); 3186 still running. Wave 2 spawned: 3612 6474 7630 7679. Note: 2753 released 09:00 JST, BEFORE the 10:05 seal, so its sealed-spot entry is post-release (residual drift only).

## Stage J — hunt 7679 banked, scratch collision
- Logged at 2026-10-05 01:20 UTC
- 7679 hunter reports a parallel hunter (7630) wrote a same-named file in the shared scratch directory and overwrote its Q1 短信 text copy; it re-read from a private subdirectory and logged the wrong reading under rejected_candidates. 7630's hunt may carry the same risk — check its sources before trusting it. Defect: hunters share scratch filenames.

## Stage J — hunt 7630 banked
- Logged at 2026-10-05 01:22 UTC
- 7630 hunter confirms it wrote q1.txt etc. into shared /tmp/claude-0/ instead of its scratchpad; it was the overwriter, not the overwritten — its findings cite its own Ichibanya documents (eir-parts 月次, kabutan 短信 PDFs). 7679 already caught and rejected the contaminated reading.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-05 01:27 UTC
- 11/11 hunted and rankable; 0 above the 2.8 floor; top 3498 +1.70, bottom 7679 -1.20; 7 positive / 4 negative; 2753 released 09:00 before the seal (residual-drift window). Note: research/2026/10/2026-10-05/japan/japan-note.md. No orders.

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-05 06:41 UTC
- 06:42 UTC fire: universe for next ASX session, seal baselines, one unpriced-hunter-au per name in waves of 5, score with edge_score.py, note. No orders.

## Stage AU — Australia researcher — DONE (empty session)
- Logged at 2026-10-05 06:42 UTC
- Sealed for 2026-10-06: 0 scheduled / 0 eligible / 0 hunted, thin open session. See research/2026/10/2026-10-06/_run-log.md.

## Stage X — Close AMC — 2026-10-05 10:10 UTC
- Logged at 2026-10-05 10:16 UTC
- Guard mode --require-exit-tif opg exit 0 (amc_open; amc -> day). verify: 14 legs, none UNFILLED, nothing held. close --submit: no leg with exit date today, 0 orders sent, 0 refusals. Account reachable. Unfilled-at-expiry legs (FEIM, RH, VRA, FPS, RLGT, LUXE, ALMU, LEN) are historical and show 0 still held.

## Edge hunt (panel) — 2026-10-05 amc + 2026-10-06 bmo — STARTED
- Logged at 2026-10-05 17:08 UTC
- 17:10 UTC fire. Window: 3 confirmed-session names (RPM, LW, APOG, all 2026-10-06 bmo). Thin day, so time-not-supplied rows checked with session_resolve.py: 5 carried unresolved (AEHR, VLGEA, ARTW, NCPL, MSS), 0 killed, 0 confirmed — not hunted (no announced date; base-universe kept comparable with stage E). 3 baselines sealed 17:12Z, all with option chains. Plan: 1 edge-sweep, up to 3 unpriced-searchers, then 4 blind judges. No orders.

## Edge hunt (panel) — sweep
- Logged at 2026-10-05 17:12 UTC
- edge-sweep: 3 of 3 confirmed from company releases, all 2026-10-06 bmo (APOG 63, LW 47, RPM 29), 0 phantom. AEHR (time-not-supplied, calendar 10-05) checked by hand: no company date announcement found, not hunted; its baseline moved to edge-panel/_not-hunted/. provenance: us-searcher.v1 · claude-opus-5-5.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-10-05 17:21 UTC
- 3 searchers back (APOG +3.40 above floor, RPM +0.30, LW -0.10). edge_score + V2 grounded written 17:21Z, before the first print (V2 3/3 grounded on 180 obs). LW: hunter's prose said impact_sum -0.4 but its findings sum to -0.1; scorer uses the findings. Packs built; launching four judges.

## Edge hunt (panel) — DONE
- Logged at 2026-10-05 17:26 UTC
- 4 of 4 judges ran (opus5, opus55, sonnet55, fable51; pinned agents, no fallback), 3/3 ids covered each. Panel selected APOG (k 4/4, panel_score +1.65, expected_edge 3.35); RPM +0.67, LW +0.18 not selected. Searcher key: APOG +3.40 (floor), RPM +0.30, LW -0.10. Stage E edge/ not on main at note time: no comparison. No alpaca_trade.py call, no shadow ledger. Note: research/2026/10/2026-10-05/edge-panel/edge-note.md.

## Stage CA — Canada researcher — STARTED
- Logged at 2026-10-05 18:33 UTC
- 18:34 UTC (14:34 ET, Toronto open). Plan: ca_universe -> seal baselines before 16:00 ET -> provenance stamp -> unpriced-hunter-ca one per name in waves -> edge_score -> note. No orders.

## Stage CA — Canada researcher — EMPTY UNIVERSE
- Logged at 2026-10-05 18:33 UTC
- TSX open (market_closed null); scheduled_today 1 of 2510 scanner rows (7 candidates in window). Calendar: confirmed 0 / agreed 0 / wsh_only 0 / vendor_only 1 / disputed 0; moved_off_target_by_wsh none. Dropped: YAY (THS Maple, TSXV) below the $100k turnover floor at $666/day. filing_only drops: 0. Eligible 0, hunted 0. No baselines sealed, so no short-register snapshot stored today and no anchor-arm split (0 options / 0 register). Normal off-peak outcome, not a fault; TMX stack answered (WSH + news archive read). FX from Bank of Canada because Yahoo did not answer.

## Stage R — reversal researcher — STARTED
- Logged at 2026-10-05 19:04 UTC
- Fired 19:04 UTC = 15:04 ET, inside 13:30–16:05 ET. Repo was present in the working directory (no clone). Plan: --intraday screen K=15, seal baselines, one reversal-hunter per name, edge_score.py, resolve 2026-10-02, note before 16:00 ET.

## Stage R — reversal researcher — DONE
- Logged at 2026-10-05 19:12 UTC
- rev_universe --intraday at 15:04 EDT for drop date 2026-10-05: 5977 screened, 36 passed floors, 15 hunted, 15 rankable. Largest sector Health Care 6/15 (40%), no concentration warning. SPY +0.83% at screen. Five names repeat from the 10-02 run (WHLR WCT HOST GCTK GRML).
- Provenance: reversal-hunter rev.v7, claude-opus-5-5. Hunters ran 8 at a time (concurrency cap); all 15 written by 19:11 UTC. Nothing shed.
- Floor-clearer (|impact_sum|>=2.8): WHLR -3.00 (Series D holder redemption 10-05, settled in stock; 8-K expected before 10-06 open). Range -3.00..+0.50. Zero repricing (leg 1) findings; every overshoot_pct 0. 5 hunts returned zero findings.
- Defect (repeat of 10-02): overshoot_has_mechanism=true on 8 hunts with no repricing finding (VOGX HOST GRML BGS NNNN CRDL GCTK WCT); by_overshoot_mechanism will mis-bucket them. Constant/brief not changed.
- Resolve: 2026-10-01 run resolved at d1 (resolve-2026-10-01.json): impact_sum rho +0.324 (p 0.24) vs neg_atr14 +0.196, neg_vol_spike +0.296, neg_ret_d -0.614 (p 0.018); lean_vs_free_control_rho 0.029; book ONEN short +2.60% gross. 2026-10-02 run all 15 move_pending (window closes today); resolve-2026-10-02.json written as pending.
- Nasdaq short-interest API returned 503 to PAAI and BGS hunters. No orders, no broker step. Note: research/2026/10/2026-10-05/reversal/reversal-note.md

## Edge hunt — 2026-10-05 amc + 2026-10-06 bmo — STARTED (LATE)
- Logged at 2026-10-06 06:55 UTC
- Routine fired 17:04 UTC 10-05; step 0b verify/close --submit DENIED by auto-mode classifier (real-world transactions), and the session then stalled ~14h on a second denial (edge_universe.py). Resumed 06:55 UTC 10-06. Close AMC 10:16 UTC 10-05 found 0 held, so no exit was owed. 10-05 amc half: 0 confirmed rows (AEHR company-announced 10-05 amc but time-not-supplied, already printed, not hunted). 10-06 bmo half still ahead of its prints: RPM, LW, APOG; baselines sealed 06:57 UTC 10-06 pre-market, implied move None on all three (no two-sided chain pre-market) so the baseline takes the historical-median fallback. Plan: 1 sweep + 3 hunters, must finish before ~10:30 UTC (06:30 ET) bmo releases.

## Edge hunt — sweep (late)
- Logged at 2026-10-06 06:58 UTC
- edge-sweep: 3 of 3 confirmed from company releases, all 2026-10-06 bmo (APOG 66, LW 52, RPM 31), 0 phantom, 0 session unsettled; no release out at ~07:00 UTC. provenance us.v9 · claude-opus-5-5. 3 unpriced-hunters launched ~06:59 UTC.
