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
