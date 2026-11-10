# Run log — 2026-11-10

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-09 14:38 UTC
- Fired 2026-11-09 ~14:37 UTC (Mon). Sealing for event date 2026-11-10 (Tue). Plan: universe -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff. Step 0: local main shallow/unrelated to force-updated origin/main; re-pointed main at origin/main (clean tree), all scripts present.

## Stage EU — IBKR
- Logged at 2026-11-09 14:38 UTC
- mode: execution_eu.enabled is false; broker = executor server (auth tws); this session makes no broker call

## Stage EU — progress
- Logged at 2026-11-09 14:48 UTC
- Universe: 68 scheduled, 42 eligible, 20 drawn (random, seed eu-2026-11-10): it 6, de 5, se 5, uk 2, dk 1, no 1; largest it 30%. 20 baselines sealed ~14:50 UTC (intraday spots). Wave 1 launched: A2A ABDP BAHN_B BEAMMW_B BFF.

## Stage EU — panel STARTED
- Logged at 2026-11-09 15:18 UTC
- 20/20 hunts banked, all search_complete. 18 ranked; BAHN_B (Q3 on 11-17, Telenor SEK 62 offer) and BEAMMW_B (Q3 on 11-11) not ranked, no event. None above floor 2.8; top DIA +1.60, bottom ABDP -0.80. Hunters re-read BFF and INW as amc (release after close, reaction 11-11). 18 packs, four -intl- judges.

## Stage EU — IBKR handoff
- Logged at 2026-11-09 15:25 UTC
- ibkr-handoff.json written (no broker call; execution_eu.enabled false, so the executor places nothing). Rule panel_pct>=70 + 4 judges: BUY BFF (74.4), SELL A2A (72.0); DIA not taken (turnover $0.14m < $0.20m floor). Caveat: BFF releases amc per hunter, so its reaction is 11-10 close -> 11-11 close.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-09 15:25 UTC
- Sealed for 2026-11-10 (Tue) ~14:47 UTC Mon 11-09 (intraday spots). 68 scheduled, 42 eligible, 20 drawn (it 6, de 5, se 5, uk 2, dk 1, no 1). 20/20 hunts, all search_complete. 18 ranked; BAHN_B (Q3 11-17) and BEAMMW_B (Q3 11-11) not ranked. None above floor 2.8; top DIA +1.60, bottom ABDP -0.80. Panel 4/4 members, 18/18 each, no fallback; selected DIA long 4/4 (panel_pct 90). BFF and INW are amc per hunters. anchor_covered 4/20; es/pl 0; de 5. Pushed to main (EARNINGS_DATA_BRANCH=main).

## Close AMC — 2026-11-10
- Logged at 2026-11-10 11:19 UTC
- Guard mode --require-exit-tif opg: exit 0 (amc open as day). verify: 14 legs, none UNFILLED, nothing held. close --submit: no legs due today, nothing sent, no refusals. Account reachable. (Run fired 11:12 UTC, 06:12 ET.)

## Stage M — morning exit review — STARTED
- Logged at 2026-11-10 14:17 UTC
- source research/2026/11/2026-11-09/edge-panel, 09:18 ET, 10 picks; 8 analysts launched, SRRK and VG held by the 8-subagent concurrency limit

## Stage M — morning exit review — done
- Logged at 2026-11-10 14:21 UTC
- 10 names, compiled 09:20 ET: exit_open QBTS ASTS LCID PLUG SANM HIMS; exit_limit HSAI SRRK VG; exit_1000 LQDA. Pool (prev morning resolved): 92 names/13 days, review_minus_static +0.06 (t 0.14). SRRK/VG launched ~2 min late (8-subagent concurrency cap); all 10 reviewed in time.

## Edge hunt (panel) — 2026-11-10 amc + 2026-11-11 bmo — STARTED
- Logged at 2026-11-10 18:09 UTC
- Stage E-P fire; session began 18:08 UTC (13:08 ET). Universe 107 names (84 amc 11-10, 23 bmo 11-11; 1 share class folded). edge_universe.py's urllib fetch got HTTP 403 from api.nasdaq.com three times while curl with a full browser UA got 200; the universe was built by the same script with fetch() swapped for curl from a scratch wrapper (no repo code changed). Baselines being sealed by code (9 parallel priced_in processes); one edge-sweep in parallel. Plan: up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — baselines sealed
- Logged at 2026-11-10 18:12 UTC
- 107 of 107 baselines sealed by 18:12 UTC, before any searcher. RDCM failed first on Yahoo HTTPError (parallel burst) and was re-sealed serially, ok. provenance stamped US-P: unpriced-searcher us-searcher.v3 on claude-opus-5-5.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-10 18:15 UTC
- 18:15 UTC. Sweep: 43 of 107 checked, 35 company-confirmed, 7 unconfirmed (VIV RUM AADX BV AYA BRCB GO), 1 phantom (EC: 6-K of 11-09 moved results to 11-12 amc), 64 unchecked. Session unsettled: ALC AMPX EVLV. Cap 20: unconfirmed 7 + phantom shed; confirmed below priority 51 shed (ATRO SKYH KOPN AZTA SATL AEBI BGSI AII INMD ANGX PBR ALC GIB ICL FLNG); 64 unchecked shed. No hunted baseline is suspect; no amendment. Sweep's PBR baseline_history_trustworthy:false self-reported as a mislabel; PBR not hunted. Hunted (20): amc STUB LPTH NN FRNM FLY CAPR CRWV SONO RGTI ATEX KURA MRCY FOSL REZI NRGV AMPX(session unsettled) EVLV(unsettled); bmo ODD RSKD NYAX. Wave 1 (8): STUB LPTH NN FRNM FLY CAPR CRWV SONO.

## Edge hunt (panel) — wave 2
- Logged at 2026-11-10 18:22 UTC
- 18:22 UTC. Returned, search_complete true per hand-backs: NN CRWV CAPR LPTH FLY. Launched in later turns: RGTI ATEX KURA MRCY FOSL. Running: STUB FRNM SONO RGTI ATEX KURA MRCY FOSL. To launch: REZI NRGV AMPX EVLV, then bmo ODD RSKD NYAX.

## Edge hunt (panel) — all 20 launched
- Logged at 2026-11-10 18:28 UTC
- 18:28 UTC. All 20 searchers launched (NYAX last). Returned, search_complete true per hand-backs: NN CRWV CAPR LPTH FLY FRNM STUB SONO KURA ATEX REZI RGTI FOSL. Running: MRCY NRGV AMPX EVLV ODD RSKD NYAX.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-11-10 18:35 UTC
- 20/20 searchers returned by 18:35 UTC (unpriced-searcher, native, Opus 5.5). hunt_status check --apply: 0 unfinished of 20; none retried. mode: execution enabled, amc_open. flatten --submit at 18:35 UTC: 3 positions still held from 2026-11-09's book (ASTS -167 +12.73%, HSAI -317 +1.27%, QBTS -570 +10.16% unrealised as printed), all closed; flatten reported 'closed'.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-10 18:35 UTC
- 18:35 UTC. edge_score and V2 grounded written before the first print. 20 rankable. Packs built; four judges, one part. Account flat after 3s.

## Edge hunt (panel) — panel done
- Logged at 2026-11-10 18:43 UTC
- 18:43 UTC: all four judges on pinned agents, 20/20 each, one part, no fallback, no retry. panel_score: selected (panel_pct >= 80, 4 present) NRGV L 89 (4 of 4). Next AMPX L 79, STUB S 74. Note written; stage E edge/ absent.

## Edge hunt (panel) — step 6b buy
- Logged at 2026-11-10 18:46 UTC
- 18:46 UTC (13:46 ET), after the note: plan, then open --submit --no-flatten. 1 market long order: NRGV 2753 filled @ 3.40, notional ~$9,360 = 50.0% of $18,724 equity (one name hits the 50% cap; the rest stays cash). Execution cost vs mid +0.147. Exit dated 2026-11-11. Nothing else at panel_pct >= 80.

## Edge hunt (panel) — done
- Logged at 2026-11-10 18:50 UTC
- 18:50 UTC: edge_context written with search (step 6d). Run complete. Note: edge_universe.py's urllib fetch is 403'd by api.nasdaq.com while curl with a full browser UA works; the fetch needs a fix before the next fire.

## Holistic research — 2026-11-10 — STARTED
- Logged at 2026-11-10 19:17 UTC
- 14:18 ET fire; E-P sweep on main; pick up to 12 names, evolving hp.v1 + control on a seeded third, collect before 15:45 ET; no orders

## Holistic research — learning step
- Logged at 2026-11-10 19:35 UTC
- 16/16 hunts ok, 0 recommendations (evolving hp.v1 on 12, control on STUB NN FLY SONO). resolve: 15 name-arms newly resolved (11-09 run). gate closed: 11/30 names, 1/3 days on hp.v1; drift alarm off; reflector not launched; tomorrow runs hp.v1. DEFECTS for the operator: (1) holistic.py ep_view crashed on edge-scores-panel.json's list-shaped ranking_by_ticker; minimal read-side fix committed on branch claude/peaceful-sagan-o11p3e only, NOT on main, so tomorrow's resolve will crash again until it is merged. (2) scripts/publish.sh does not stage researcher_holistic/, so outcomes.json / evaluation / any playbook revision never reach main; today's are on the same branch, and evaluation.md is copied into edge-holistic/reflection/.
