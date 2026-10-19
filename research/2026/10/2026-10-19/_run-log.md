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
