# Run log — 2026-10-26

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-23 13:37 UTC
- Fired 13:36 UTC Fri 2026-10-23; sealing for event date 2026-10-26 (Mon, next European session). Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model intl panel -> note. No orders.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-23 13:49 UTC
- Event date 2026-10-26 (Mon). 12 scheduled, 7 eligible, all 7 hunted (under cap 20): uk 2 (AMC, BVXP), pl 2 (KTY, OPL), se 1 (ALLEI), fi 1 (KREATE), it 1 (SGF). Largest market uk 29%, 5 markets. Yahoo calendar quote endpoint unavailable on all ten markets. Registers read se/fi/it/uk; pl none. anchor_covered: ALLEI only (1 of 7). History observed_rns for AMC/BVXP, estimated for 5. session_unresolved: AMC BVXP KTY SGF. OPL amc. One wave of 5 + one of 2: [KREATE SGF KTY OPL ALLEI] then [AMC BVXP].

## Stage EU — wave 1 done
- Logged at 2026-10-23 13:58 UTC
- KREATE -0.2, SGF +0.7, KTY +0.3, OPL +0.5, ALLEI written. KTY and SGF hunters report amc from issuer timestamps (sealed bmo?, both session_unresolved so the resolver measures both windows). AMC and BVXP running.

## Stage EU — panel STARTED
- Logged at 2026-10-23 14:05 UTC
- 7 hunts done; 7 ranked, 0 above 2.8 (ALLEI +1.00, SGF +0.70, AMC +0.60, OPL +0.50, KTY +0.30, BVXP -0.20, KREATE -0.20). 7 packs, four judges (intl).

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-23 14:11 UTC
- Event date 2026-10-26. 7 ranked (uk 2, pl 2, se 1, fi 1, it 1): ALLEI +1.00, SGF +0.70, AMC +0.60, OPL +0.50, KTY +0.30, BVXP -0.20, KREATE -0.20; 0 above floor 2.8. KTY and SGF sealed bmo? but report amc per issuer timestamps (resolver measures both windows; read the amc one). ALLEI releases 11:30 CET in session. Yahoo calendar unavailable on all ten markets.
- Panel: 4/4 members, no fallback; 1 selected: BVXP short (k=4, panel_pct 96) against hunter -0.20. Note: europe-note.md. No orders. Published with EARNINGS_DATA_BRANCH=main.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-26 01:06 UTC
- Fired 01:04 UTC 2026-10-26 (10:04 JST). Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp in waves of 5 (cap 25) -> edge_score -> four-model intl panel -> note. No orders.

## Stage J — wave 1 launched
- Logged at 2026-10-26 01:07 UTC
- Universe: 8 scheduled, 5 eligible (3 dropped on turnover), 5 hunted, method 'all 5 eligible names (at or under the cap)'. Baselines sealed 01:06 UTC; provenance jp.v5 / claude-opus-5-5. All five short-register levels read 0.0% (register 20261023, 610 codes) and baseline_quality 0.6. One wave of 5 hunters.

## Stage J — hunt banked
- Logged at 2026-10-26 01:12 UTC
- 2211 hunt returned (impact_sum 0.0); four still running.

## Stage J — panel STARTED
- Logged at 2026-10-26 01:18 UTC
- 5 hunts banked and scored (impact_sum 7970 +1.90, 6923 +1.00, 8060 +0.50, 2211 0.00, 3635 -0.50; none above 2.8). 5 packs, four judges.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-26 01:21 UTC
- 5 ranked: 7970 +1.90, 6923 +1.00, 8060 +0.50, 2211 0.00, 3635 -0.50; none above floor 2.8. Panel 4/4 members, no fallback, 0 selected (7970 k=2, panel_pct 77). Also resolved 10-21 and 10-22 (3 names each). Note: japan/japan-note.md. No orders.

## Close AMC — 2026-10-26 10:13 UTC
- Logged at 2026-10-26 10:19 UTC
- Guard mode --require-exit-tif opg exit 0 (amc_open, amc -> day order queued for open). verify: 14 exit legs, none UNFILLED, nothing held. close --submit: no leg due today, nothing sent, no refusals. Account reachable. Note: stage E-P now trades the account (since 2026-10-19); this scan covers research/*/*/*/edge only, so E-P legs under edge-panel/ are not seen by this Routine.

## Stage M — morning exit review — STARTED
- Logged at 2026-10-26 13:17 UTC
- source research/2026/10/2026-10-23/edge-panel, 09:17 ET, picks MED BMRC DEA

## Stage M — morning exit review — done
- Logged at 2026-10-26 13:19 UTC
- 3 names: MED exit_close, BMRC exit_limit 28.05, DEA exit_close; compiled 09:19 ET; pool 29 names/5 days review_minus_static +0.073 (t 0.13)

## Edge hunt (panel) — 2026-10-26 amc + 2026-10-27 bmo — STARTED
- Logged at 2026-10-26 17:15 UTC
- Stage E-P fire 17:06 UTC (session start 17:07). Universe 105 names (40 amc 10-26, 65 bmo 10-27), baselines sealed for all 105 in edge-panel/baselines before any agent. Plan: one edge-sweep, up to 20 unpriced-searchers, step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-10-26 17:20 UTC
- Sweep finished ~17:20 UTC (12-min budget, 24 of 105 checked): 11 company-confirmed (CLS WHR RMBS AEYE ZDGE PSMT BLX amc 10-26; GLXY DQ CBC SNDL bmo 10-27; CBC via QuiverQuant relay), 0 phantoms proven, 9 checked-unconfirmed likely projections (PHAR VLRS GGB KOF CLW FLXS TZOO INIO NVS), 81 unchecked. Cap 20: the 11 confirmed plus the 9 highest-priority unchecked (AMKR SOFI JBLU KNSA AGYS CNC PII CVLT GLW; searchers told to settle event and session themselves). Shed: the 9 checked-unconfirmed and 72 lower-priority unchecked by edge_degrade_order. baseline_history_trustworthy=false for DQ SNDL CBC. Searchers unpriced-searcher, amc first.

## Edge hunt (panel) — searcher progress
- Logged at 2026-10-26 17:34 UTC
- 11 of 20 searchers returned by 17:35 UTC (CLS WHR RMBS AEYE ZDGE PSMT BLX AMKR AGYS GLXY CBC; AMKR and AGYS settled amc 10-26 from company sources, CBC 10-27 bmo from two copies of the company notice). Running: DQ SNDL SOFI JBLU KNSA CNC PII CVLT; GLW queued for the next free slot.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-10-26 17:46 UTC
- 20/20 searchers returned by ~17:45 UTC (unpriced-searcher, native, Opus 5.5; all 20 events company-confirmed, incl. the 9 the sweep left unchecked). mode: execution enabled. flatten --submit at 17:46 UTC: held MED 438 sh (+4.58% unrealised, 2026-10-23 book), closed at market; account flat, equity $10,524.11.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-10-26 17:46 UTC
- 20 packs, four judges, one part. edge_score and V2 grounded written ~17:47 UTC, before the first print.
