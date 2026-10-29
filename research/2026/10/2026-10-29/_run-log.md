# Run log — 2026-10-29

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-28 13:47 UTC
- Fired 13:46 UTC 2026-10-28 (scheduled 13:35), sealing for event date 2026-10-29 (Thu). Plan: universe (cap 20, $100k floor), seal, stamp, hunters in waves of 5, score, four-judge panel, note. Local main had diverged from origin (stale container copy, 52/52); work done on a fresh branch off origin/main, published with publish.sh to main.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-28 14:00 UTC
- Event date 2026-10-29. 115 scheduled, 78 eligible (uk 5, de 11, fr 6, se 11, dk 4, no 18, fi 12, it 3, es 6, pl 2), 20 drawn (random, seed eu-2026-10-29): no 6, fi 3, es 3, fr 2, se 2, it 2, uk 1, de 1. Largest market no 30%, 8 markets. Baselines sealed ~14:15 UTC at intraday spots. session_unresolved: RDC, AL2SI, AMP, IG, BOHUS, DVD, KOG, PPH. anchor_covered 6/20 (AMP, IG, DVD, PPH, RDC + see note). es 3 names (no anchor, no archive). Provenance stamped. Wave 1: AKRBP AL2SI AMP BOHUS DNO.

## Stage EU — 14 of 20 hunts banked
- Logged at 2026-10-28 14:26 UTC
- Banked: BOHUS +1.4, FDR +1.2, IG +0.9, PDX +0.8, DNO +0.7, ENENTO +0.6, NESTE +0.3, AMP +0.2, ENGCON_B +0.1, KOG -0.1, DVD -0.3, AKRBP -0.4, EPR -0.7, AL2SI -4.5. Session corrections by hunters: AL2SI and AMP report amc (issuer pattern / 18:30 CET call), so the sealed bmo window may hold no release; ENENTO and IG release in session (inside the bmo window). Running: IDR NTGY POSTI PPH RDC STMPA (six concurrent for a few minutes, one over max_concurrent 5). Hunters run rolling, not in fixed waves; each banked hunt published on arrival.

## Stage EU — panel STARTED
- Logged at 2026-10-28 14:34 UTC
- All 20 hunts banked and scored; 20 ranked. AL2SI -4.50 the only name above floor 2.8. 20 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-28 14:42 UTC
- 20 ranked: BOHUS +1.40 top ... AL2SI -4.50 (only floor-clearer; hunter dates release amc, so sealed bmo window likely holds no release). Panel 4/4 members, no fallback, 4 selected: FDR long (4/4, pct 83), AL2SI short (3/4, 93), EPR short (3/4, 81), NESTE long (3/4, 80). anchor_covered 5/20; es 3 names, pl 0; 5 se/fi names need resolving within ~a week. AMP also amc per hunter. Note: europe/europe-note.md. No orders. Published to main (EARNINGS_DATA_BRANCH=main) from a fresh branch off origin/main, because local main had diverged.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-29 01:05 UTC
- Routine fire 01:05 UTC 2026-10-29 (10:05 JST). Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp in waves of 5 (cap 25) -> edge_score -> four-model intl panel -> note. No orders.

## Stage J — wave 1 launched
- Logged at 2026-10-29 01:07 UTC
- Universe: 127 scheduled, 106 eligible (21 dropped on turnover), 25 hunted, random sample seed 'jp-2026-10-29'. calendar_as_of 2026-10-01. provenance jp.v5 / claude-opus-5-5. Wave 1: 1946 2594 3116 3199 4347.

## Stage J — resolved 2026-10-27
- Logged at 2026-10-29 01:07 UTC
- jp_resolve: 25/25 usable, impact_sum rho -0.313 (p 0.125), free control 0.055, lean_vs_free_control_rho 0.435. Panel: rho panel_pct -0.483 (p 0.01), selected 6 names 1 right, mean signed -6.22%. One day is not a result.
