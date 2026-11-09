# Run log — 2026-11-09

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-06 14:37 UTC
- Fired Fri 2026-11-06 14:36 UTC (15:36 Amsterdam, markets open; spots intraday). Sealing for next European session Mon 2026-11-09. Plan: universe (cap 20) -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note. Local main was a stale shallow clone diverged from force-updated origin/main; re-pointed to origin/main 1415d26e5.

## Stage EU — progress
- Logged at 2026-11-06 14:40 UTC
- Universe: 22 scheduled, 16 eligible, all 16 hunted (at/under cap 20). by_market uk2 de4 fr1 dk1 it6 es1 pl1; largest it 37.5%. Baselines sealed 16/16 (intraday spots Fri 14:4x UTC). Provenance stamped. Wave 1 launched: G1A HNR1 HYQ PAT NTG.

## Stage EU — progress
- Logged at 2026-11-06 14:49 UTC
- Wave 1 banked 5/5, all search_complete: G1A 0.0, HNR1 +1.0, HYQ -0.6, PAT +1.8 (session amc per issuer timestamps), NTG +0.55 (session amc per issuer). Wave 2 launched: ALM ALCLS DOV EGLA IOT. Note: publish.sh push was refused non-fast-forward while CI moved main (shallow clone); recovered with pull --rebase + push.

## Stage EU — progress
- Logged at 2026-11-06 14:54 UTC
- Wave 2: ALM -0.7, ALCLS 0 (no release in window, event_confirmed false; Cellectis releases amc and has not announced a Q3 date), DOV -0.1 (session amc per issuer timestamps), EGLA 0 (PHANTOM: board 2026-11-16 per issuer calendar). IOT running. Rolling into wave 3 at 5 concurrent: NWL PHN UCG TEN launched; KNOS REC queued.

## Stage EU — panel STARTED
- Logged at 2026-11-06 15:02 UTC
- 16/16 hunts banked, all search_complete. 13 ranked; ALCLS/EGLA/REC not ranked (no event in window: ALCLS no Q3 date announced, EGLA board 11-16, REC printed 11-06). None above floor 2.8. Top IOT +2.10, bottom TEN -0.90. Hunters re-read session as amc for PAT NTG DOV PHN NWL. 13 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-06 15:09 UTC
- Sealed for 2026-11-09 (Mon) at ~14:45 UTC Fri 11-06 (intraday spots). 22 scheduled, 16 eligible, all 16 hunted (no draw; it 6 largest, 37.5%), all search_complete. 13 ranked; ALCLS (no Q3 date), EGLA (phantom, board 11-16), REC (duplicate of 11-06 interims) not ranked. Top IOT +2.10, bottom TEN -0.90; none above floor 2.8.
- Panel: 4/4 members, 13/13 each, no fallback. Selected IOT long 3/4 (panel_pct 88).
- Six names re-sessioned amc by hunters (PAT NTG DOV PHN NWL[10-11 08:05] TEN); resolve after 11-10. anchor_covered 4/16; es 1, pl 1, de 4. publish.sh's own push failed non-fast-forward twice (CI moving main); recovered with pull --rebase. Pushing to main (EARNINGS_DATA_BRANCH=main).

## Stage M — morning exit review — STARTED
- Logged at 2026-11-09 14:19 UTC
- source research/2026/11/2026-11-06/edge-panel; fired late, now 09:19 ET (scheduled 09:10)

## Stage M — previous morning scored
- Logged at 2026-11-09 14:19 UTC
- 2026-11-06 resolved. Pool: 84 names / 12 days, review mean +0.829% (t 0.68), review_minus_static -0.274pp (t -0.65); Brier review-minus-prior p_open_lags -0.021 (t -1.73), p_fade_by_1000 -0.013 (t -1.06)

## Stage M — morning exit review — done
- Logged at 2026-11-09 14:20 UTC
- 8 names: exit_open HAIN VFF QTRX SOC TGTX; exit_limit DCTH 18.89; exit_close NRXS; none LFMD (release not found). Fired 09:18 ET (8 min late); compiled ~09:21 ET; HAIN review provisional at compile

## Stage M — recompiled
- Logged at 2026-11-09 14:21 UTC
- HAIN final review in; recompiled before 09:24 ET

## Edge hunt (panel) — 2026-11-09 amc + 2026-11-10 bmo — STARTED
- Logged at 2026-11-09 18:10 UTC
- Stage E-P fire; session began 18:07 UTC (13:07 ET). Universe 168 names (119 amc 11-09, 49 bmo 11-10; UONE/UONEK both on calendar). Baselines being sealed by code into edge-panel/baselines (9 parallel priced_in processes); one edge-sweep launched in parallel with sealing. Plan: up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — baselines sealed
- Logged at 2026-11-09 18:12 UTC
- 168 of 168 baselines sealed by 18:12 UTC, before any searcher. BAP and LINE failed first time on Yahoo HTTPError (parallel burst) and were re-sealed serially, both ok. provenance stamped US-P: unpriced-searcher us-searcher.v3 on claude-opus-5-5.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-09 18:17 UTC
- 18:17 UTC. Sweep: 28 of 168 checked, 22 company-confirmed, 6 unconfirmed (ONTO ZETA SE HRB JBS WIX), 0 phantoms, 140 unchecked. ASTS and VOD session unsettled. Cap 20: unconfirmed 6 shed, lowest hunt_priority confirmed shed: TDG (27) VOD (17); 140 unchecked shed. PLUG baseline amended suspect->unknown before any searcher (matcher took the 15 Oct preliminary 8-K as a print; company release sets 11-09 amc, call 16:30 ET); no other hunted name suspect. ASTS LCID BAP LEGN HSAI ONON VG cadence_implausible and/or history untrustworthy (SKYD too): searchers told. Hunted (20): amc ASTS HIMS RKLB TTD ACHR PLUG LCID SANM QLYS SKYD TTWO BAP OXY; bmo SRRK LQDA QBTS LEGN HSAI ONON VG. Wave 1 (8): ASTS HIMS RKLB TTD ACHR PLUG LCID SANM.
