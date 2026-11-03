# Run log — 2026-11-03

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-02 15:28 UTC
- Fired 2026-11-02 15:27 UTC (16:27 Amsterdam, ~1h before close; scheduled 14:35 UTC). Sealing for EVENT DATE 2026-11-03 (Tuesday). Plan: universe (10 markets, cap 20), seal, hunters in waves of 5, score, four-judge panel, note.

## Stage EU — universe and baselines sealed
- Logged at 2026-11-02 15:38 UTC
- Event date 2026-11-03 (Tue). 66 scheduled, 43 eligible, 20 drawn (seed eu-2026-11-03): de 7, se 6, no 3, uk 2, fr 1, dk 1; largest market de 35%, 6 markets. All sealed bmo; session_unresolved: ADV FME NOEJ ZAL SOLAR_B COFA ODL SYNACT VSURE DOTD. anchor_covered 9/20. es+pl 0. Yahoo calendar unavailable on every market; bankier (pl) 403. Baselines sealed ~15:50 UTC Mon at intraday spots (not closes). Provenance stamped.
- SHED: COFA — duplicate event. 2026-11-02's run already hunted Coface's 9M-26 release (2 Nov 17:35 Paris, after close; hunt research/2026/11/2026-11-02/europe/hunts/COFA.json); a bmo 11-03 window is the same close(11-02)->close(11-03) window, so hunting it again would count one print twice. Not re-drawn (no second selection). 19 hunters in 4 waves.

## Stage EU — wave 1 banked
- Logged at 2026-11-02 15:48 UTC
- ADV 0.0, BOOZT -0.5, BOSS +0.2, DOTD 0.0, FME -1.4 (impact_sum). All search_complete. Wave 2: HACK MULTI NOBA NOEJ ODL.

## Stage EU — wave 2 banked
- Logged at 2026-11-02 15:55 UTC
- HACK +0.3, MULTI +0.4, NOBA +0.7, NOEJ -0.3, ODL 0.0. All search_complete true. MULTI is a fixed-ratio merger target of REJL_B (0.9725 Rejlers B per share), so MULTI and REJL_B (wave 3) are one correlated exposure. Wave 3: OKEA REJL_B SHA0 SOLAR_B SYNACT.

## Stage EU — wave 3 banked
- Logged at 2026-11-02 16:02 UTC
- OKEA +0.6, REJL_B -0.6, SHA0 0.0, SOLAR_B +0.3, SYNACT -0.5. All search_complete true. MULTI (+0.4) and REJL_B (-0.6) are merger-linked and lean opposite ways on what is effectively one combined share. Wave 4 launched: TMV TUNE VSURE ZAL.

## Stage EU — panel STARTED
- Logged at 2026-11-02 16:11 UTC
- 19/19 hunts banked, all search_complete. Scored: top NOBA +0.70, OKEA +0.60; bottom FME -1.40, REJL_B -0.60; none above floor 2.8. COFA not ranked (shed, duplicate). 19 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-02 16:20 UTC
- Sealed for 2026-11-03 (Tue) at ~15:50 UTC Mon (intraday spots). 66 scheduled, 43 eligible, 20 drawn; COFA shed as duplicate of 11-02's Coface hunt; 19 hunted, all search_complete, 19 ranked. Top NOBA +0.70, OKEA +0.60; bottom FME -1.40, REJL_B -0.60; none above floor 2.8. All bmo (hunters confirmed from issuer notices; BOSS date-only). anchor_covered 9/19; es+pl 0; de 7. MULTI/REJL_B merger-linked (one exposure). Panel 4/4 members, no fallback (sonnet55 did not open the market hunter defs): 1 selected, FME short (3/4, pct 81). Note: europe/europe-note.md. No orders.
- FLAG: no EU run resolved since 2026-10-16; Nordic rows of 10-19..10-23 are past the ~12-day feed window. Resolve this run by ~2026-11-12. Pushing to main (EARNINGS_DATA_BRANCH=main).

## Close AMC — 2026-11-03 11:11 UTC
- Logged at 2026-11-03 11:16 UTC
- Guard mode --require-exit-tif opg: exit 0 (amc open as day). verify: 14 legs, nothing held, no UNFILLED leg. close --submit: no leg due today, nothing sent, no refusals (market closed at 06:11 ET; account reachable). status: no open position.

## Stage M — morning exit review — STARTED
- Logged at 2026-11-03 14:12 UTC
- source research/2026/11/2026-11-02/edge-panel, 09:12 ET

## Stage M — morning exit review — done
- Logged at 2026-11-03 14:15 UTC
- 10 names (source 2026-11-02 edge-panel): LIFE limit 51.00, ICHR open, DOCN close, CHGG limit 0.65, UPST close, IBTA 10:00, VITL limit 8.35, INSP open, HLF 10:00, AEHR open. Previous morning 2026-11-02 has no morning-advice.json, nothing resolved. Pool: 50 names/8 days, review_minus_static -0.065 (t -0.18). HLF and AEHR launched late (8-subagent cap), all 10 in before compile at 09:15 ET.

## Edge hunt (panel) — 2026-11-03 amc + 2026-11-04 bmo — STARTED
- Logged at 2026-11-03 18:21 UTC
- Stage E-P fire; session began 18:08 UTC (13:08 ET). Universe 265 names (135 amc 11-03, 130 bmo 11-04; GEF.B and HVT.A folded), baselines sealed for all 265 in edge-panel/baselines by 18:21 UTC before any agent. Plan: one edge-sweep, up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-03 18:25 UTC
- Sweep finished 18:25 UTC (22 of 265 checked): 21 company-confirmed (amc 11-03: SMCI DUOL NVTS OUST TREE TARS RVLV CRCT MQ FRSH TOST ALAB CAR LIME; bmo 11-04: W HUT RIOT SEDG XPEL DIN CRCL), VRNS unconfirmed, 0 phantoms, 243 unchecked. Sessions unsettled: OUST LIME DIN CRCL. Cap 20: CRCL shed (lowest priority 34, session unsettled), VRNS shed (unconfirmed), 243 unchecked shed. Searchers unpriced-searcher, amc first, at most 8 per turn. Wave 1: SMCI DUOL NVTS OUST TREE TARS RVLV CRCT.

## Edge hunt (panel) — waves 2-3
- Logged at 2026-11-03 18:37 UTC
- Finished, search_complete true per hand-backs: TARS NVTS DUOL CRCT OUST TREE SMCI RVLV. OUST settled amc from the company's own release. Running: MQ FRSH TOST ALAB CAR LIME W HUT (launched 18:40-18:51 UTC). To launch as slots free: RIOT SEDG XPEL DIN. SMCI's searcher left a stray placeholder file at the repo root; removed before publishing.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-11-03 18:48 UTC
- 20/20 searchers returned by 18:47 UTC (unpriced-searcher, native, Opus 5.5). hunt_status check --apply: 0 unfinished of 20. Sessions settled from company releases: OUST amc, LIME amc, DIN bmo. mode: execution enabled, amc_open. flatten --submit at 18:48 UTC (13:48 ET): 8 positions held from 2026-11-02's book (DOCN 18, HLF -79, IBTA -28, ICHR 46, INSP 19, LIFE 42, UPST -70, VITL -155), all closed; flatten reported 'closed'. Note: those legs were dated to exit 11-03 (amc at the open) but were still held at 13:48 ET.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-03 18:48 UTC
- 20 packs, four judges, one part. Account flat after 3s (equity $11,054.21). edge_score and V2 grounded written ~18:50 UTC, before the first print.
