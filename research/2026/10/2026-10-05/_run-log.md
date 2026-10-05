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
