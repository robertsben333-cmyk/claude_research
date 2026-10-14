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
