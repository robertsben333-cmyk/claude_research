# Run log — 2026-10-20

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-19 13:41 UTC
- Fired 13:38 UTC Mon 2026-10-19; sealing for event date 2026-10-20 (Tue, next European session). Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model intl panel -> note. No orders.
- Local main in the container was a stale 2026-10-14 snapshot with no common history with the force-updated origin/main; it was kept as branch stale-local-main-2026-10-14 and the run works on a branch cut from origin/main (ca8771a45). publish.sh pushes HEAD:main.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-19 13:55 UTC
- Event date 2026-10-20. 23 scheduled, 11 eligible, all 11 hunted (under cap 20): se 5 (BMAX EXS LIME SCST UPSALE), de 2 (DB1 MUM), uk 1 (BPM), fr 1 (OVH), dk 1 (EMBLA), es 1 (ENG). Largest market se 45.5%, 6 markets. Registers: uk 2026-10-16, de 2026-10-16, fr 2026-10-15, se 2026-10-19, dk as_of 27-08-2026 (STALE, ~7 weeks), es none. anchor_covered: BMAX only (1 of 11). history observed_rns for BPM only; 10 estimated. session_unresolved: BPM, DB1, MUM. Provenance stamped (claude-opus-5-5).

## Stage EU — wave 1 done
- Logged at 2026-10-19 14:06 UTC
- BPM -0.35, OVH -0.5, MUM 0.0, ENG +0.2, DB1 +0.2. DB1: issuer calendar says release ~19:00 CEST 2026-10-20 (amc), so the sealed bmo window ends before the release; session_check says amc. Wave 2: BMAX EXS LIME SCST UPSALE (se, unpriced-hunter-nordic).

## Stage EU — wave 2 done
- Logged at 2026-10-19 14:18 UTC
- EXS +0.9, LIME +0.9, UPSALE 0.0, SCST -0.5, BMAX -0.7. Wave 3: EMBLA (dk, unpriced-hunter-nordic).

## Stage EU — panel STARTED
- Logged at 2026-10-19 14:28 UTC
- 11 hunts done; 11 ranked, 0 above 2.8 (EXS +0.90, LIME +0.90, DB1 +0.20, ENG +0.20, MUM 0.00, UPSALE 0.00, BPM -0.35, EMBLA -0.40, OVH -0.50, SCST -0.50, BMAX -0.70). 11 packs, four judges (intl).

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-19 14:36 UTC
- Event date 2026-10-20. 11 ranked (se 5, de 2, uk/fr/dk/es 1): EXS +0.90, LIME +0.90, DB1 +0.20, ENG +0.20, MUM 0.00, UPSALE 0.00, BPM -0.35, EMBLA -0.40, OVH -0.50, SCST -0.50, BMAX -0.70; 0 above floor 2.8. DB1 is amc per issuer calendar (~19:00 CEST) — sealed bmo window is wrong; check eu_resolve's row. Yahoo calendar unavailable on all ten markets.
- Panel: 4/4 members, no fallback; 1 selected: BMAX short (k=3, panel_pct 73). OVH widest split (sd 50). Note: europe-note.md. Resolve the 5 SE names + EMBLA within ~a week (Nordic feed window). Published with EARNINGS_DATA_BRANCH=main; panel-history.json and eu-short-cache.json committed by hand (not in publish.sh paths).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-20 01:05 UTC
- 01:06 UTC: universe (JPX kessan, turnover floor 15m JPY, seeded draw cap 25), seal baselines, one unpriced-hunter-jp per name in waves of 5, edge_score, four-model panel, note. No orders.

## Stage J — universe and baselines
- Logged at 2026-10-20 01:06 UTC
- 5 scheduled, 4 eligible (1 dropped on turnover), 4 hunted (all, under cap). Three are J-REITs (3226, 3466, 8968, FY Aug) and 5933 Alinco Q2. Baselines sealed 10:05 JST.

## Stage J — wave 1 launched; prior runs resolved
- Logged at 2026-10-20 01:07 UTC
- 4 unpriced-hunter-jp launched (3226, 3466, 5933, 8968). Resolved while waiting: 10-14 rho -0.067 (25 names, lean_vs_free_control_rho 0.789), 10-15 rho +0.085 (25, lean_vs 0.531), 10-16 (2 names, rho withheld); panel-resolved written for each.

## Stage J — panel STARTED
- Logged at 2026-10-20 01:12 UTC
- 4 hunts in, scored (impact_sum 5933 +0.70, 8968 +0.45, 3466 +0.40, 3226 0.00; none above floor 2.8). 4 packs, four judges.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-20 01:16 UTC
- 4/4 hunted and scored; panel 4/4 members, 0 selected. impact_sum: 5933 +0.70, 8968 +0.45, 3466 +0.40, 3226 0.00; none above floor. Note: japan/japan-note.md. No orders.

## Stage M — morning exit review — STARTED
- Logged at 2026-10-20 12:58 UTC
- source research/2026/10/2026-10-19/edge-panel, 08:59 ET; 5 picks (EFX, VICR, AERO, HAS, NOC), 5 analysts launched

## Stage M — previous morning scored
- Logged at 2026-10-20 12:59 UTC
- 2026-10-19 resolved: CLF exit_close +15.76% vs static exit_1300 +15.72% (review_minus_static +0.04). Pool: 1 name, 1 day, review_minus_static mean +0.04, no t on n=1.

## Stage M — morning exit review — done
- Logged at 2026-10-20 13:01 UTC
- 5 names compiled 13:00 UTC: EFX exit_open, VICR exit_limit 202.00, AERO exit_open, HAS exit_limit 97.38, NOC exit_open. 5/5 morning-reaction-analysts ran, no fallback, no compile problems. No orders placed.

## Stage M — late edit
- Logged at 2026-10-20 13:01 UTC
- HAS analyst rewrote its review after the compile (prose/sources only; action and limit unchanged). Kept for the record; not recompiled, per skill.

## Intraday panel 12:00 — STARTED
- Logged at 2026-10-20 15:59 UTC
- First snapshot of the day (names not frozen): universe + sweep, freeze, seal, Opus 5.5 searchers, guard, four judges, panel --dry-run --stage E-PI. No orders.

## Intraday panel 12:00 — names frozen
- Logged at 2026-10-20 16:11 UTC
- Universe 45 (22 amc 10-20, 23 bmo 10-21); sweep confirmed 43, ISRG and HCSG unconfirmed (vendor-only). Names frozen to edge-intraday/names.json. Cap 19: hunting PEGA IART LRN WGO NP ALK LAD MHO UAL WFRD ABT ELV TMO NFLX OZK COF WAB DHR CB; shed by lowest hunt_priority (recorded in intraday.json): NTRS NPB TDY MCB OFG SF BKU EWBC QCRH HWC ORRF ONB AMX BWB MCO NLY NEE CME FCCO T ELS PM ADC UNF. amc first.

## Intraday panel 12:00 — baselines amended
- Logged at 2026-10-20 16:11 UTC
- Before any searcher: NP suspect -> fits_cadence (matcher miss, Q2 printed 07-21), IART suspect -> unknown (10-02 row is a guidance cut, not a print); both company-confirmed by the sweep. No downgrades among hunted names. Table in edge_baseline_amend.py rewritten for this run.

## Intraday panel 12:00 — wave 1
- Logged at 2026-10-20 16:14 UTC
- 8 unpriced-searcher (Opus 5.5) launched ~16:15 UTC with an explicit read restriction: PEGA LRN NP ALK UAL WFRD NFLX OZK (amc). COF, CB (amc) and 9 bmo queued behind the platform cap of 8.

## Intraday panel 12:00 — all searchers launched
- Logged at 2026-10-20 16:26 UTC
- All 19 unpriced-searcher (Opus 5.5, native agent) launched by 16:27 UTC; 11 hunts in (all amc but COF, plus IART, MHO). Last launched: DHR.

## Intraday panel 12:00 — panel STARTED
- Logged at 2026-10-20 16:33 UTC
- 19/19 hunted (unpriced-searcher, Opus 5.5, native). Guard at 16:33 UTC moved nothing (all amc hunts written before 16:00 ET). edge_score 19 rankable. 19 packs, four judges.

## Intraday panel 12:00 — done
- Logged at 2026-10-20 16:41 UTC
- 19/19 hunted (unpriced-searcher, Opus 5.5, native), guard moved nothing, all four judges 19/19 on pinned ids, panel scored --dry-run --stage E-PI (history untouched). Selected: ALK short (82), NP long (81); PEGA short 79 misses. 24 confirmed names shed for budget, ISRG/HCSG unconfirmed. No orders. Timeline at edge-intraday/timeline.md.

## Edge hunt (panel) — 2026-10-20 amc + 2026-10-21 bmo — STARTED
- Logged at 2026-10-20 17:09 UTC
- Stage E-P fire 17:06 UTC. Universe 45 names (22 amc 10-20, 23 bmo 10-21), baselines sealed for all 45 in edge-panel/baselines. Next: one edge-sweep, then up to 19 unpriced-searchers, step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-10-20 17:15 UTC
- Sweep: 39 of 45 confirmed, 0 phantoms; unconfirmed ISRG PEGA TDY OFG NPB HCSG (not hunted). Budget 19 by hunt_priority: LRN NP IART WGO ALK UAL NFLX MHO LAD ELV CB WFRD WAB DHR COF MCB OZK ABT PM. Shed (lowest priority, strict order): QCRH TMO BWB SF ORRF EWBC HWC BKU AMX ONB NEE NTRS NLY T CME FCCO ELS MCO ADC UNF. Searchers unpriced-searcher, amc first.
