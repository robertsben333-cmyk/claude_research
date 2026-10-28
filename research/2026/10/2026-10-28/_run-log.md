# Run log — 2026-10-28

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-27 14:01 UTC
- Fired 13:59 UTC 2026-10-27 (scheduled 13:35), sealing for event date 2026-10-28 (Wed), markets still open so sealed spots are intraday.
- Plan: eu_universe (cap 20, $100k floor) -> seal baselines -> provenance -> hunters in waves of 5 -> edge_score -> four-model panel -> note. Publishing to main (EARNINGS_DATA_BRANCH=main).

## Stage EU — universe and baselines sealed
- Logged at 2026-10-27 14:11 UTC
- Event date 2026-10-28. 88 scheduled, 53 eligible (uk 6, de 7, fr 5, se 7, dk 4, no 8, fi 11, it 1, es 3, pl 1), 20 drawn (random, seed eu-2026-10-28): fi 5, no 4, uk 3, fr 2, se 2, dk 2, de 1, es 1. Largest market fi 25%, 8 markets. Yahoo calendar unavailable on all ten; bankier (PL) unavailable. Baselines sealed ~14:10 UTC at intraday spots. amc: AIR, DBV, AOJ_B. session_unresolved: CGEO, JYSK, SRT. Registers: es none; others read. Provenance stamped, orchestrator claude-opus-5-5. Wave 1: 8TRA ACAST AIR AOJ_B BNOR.

## Stage EU — wave 1 mostly banked, wave 2 launched
- Logged at 2026-10-27 14:21 UTC
- Banked: BNOR +0.3 (merger target of VAR, pinned), ACAST +0.8, AOJ_B +0.5 (amc confirmed), AIR +0.1 (amc confirmed; Dutch issuer, not on AMF flux). 8TRA still running. Launched CGEO, DBV, ELE, GSK.

## Stage EU — wave 2 banked
- Logged at 2026-10-27 14:32 UTC
- Banked: 8TRA +1.1, CGEO +0.5 (bmo confirmed 07:00 RNS), JYSK 0.0 (Q3 pre-released 12 Oct; bmo by pattern), GSK +0.3, ELE +0.7, LASTIK -0.3, DBV -3.4 (date NOT confirmed by issuer; Earnings Whispers says 11-04 — possible phantom, amc). Running: ORNAV PEAB_B PHO SALME SANOMA.

## Stage EU — panel STARTED
- Logged at 2026-10-27 14:48 UTC
- All 20 hunts banked; 19 ranked (SRT: no event). DBV -3.40 the only name above floor 2.8 (date unconfirmed by issuer). Packs built, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-27 14:56 UTC
- 19 ranked: 8TRA +1.10 ... DBV -3.40 (only floor-clearer; date not confirmed by issuer, possible phantom). SRT not ranked (no event). Panel 4/4 members, no fallback, 3 selected: DBV short (4/4, pct 96), SALME short (4/4, 86), 8TRA long (3/4, 81). anchor_covered 5/20; es 1 name; 9 se/dk/fi names need resolving within ~a week. Note: europe/europe-note.md. No orders. Pushed to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-28 01:06 UTC
- Fired 01:04 UTC (10:04 JST) 2026-10-28. Plan: jp_universe (cap 25, seeded draw) → seal baselines → provenance → unpriced-hunter-jp in waves of 5 → edge_score → four-model intl panel → note. No orders.

## Stage J — wave 1 launched
- Logged at 2026-10-28 01:07 UTC
- Universe: 46 scheduled, 39 eligible (7 dropped on turnover), 25 hunted, method "random sample of 39 eligible, seed 'jp-2026-10-28'". calendar_as_of 2026-10-01. Short register 20261027 (626 codes). provenance jp.v5 / claude-opus-5-5. Five waves of 5. Wave 1: 1930 2002 2664 2760 3003.

## Stage J — resolved 2026-10-26
- Logged at 2026-10-28 01:08 UTC
- jp_resolve: 5/5 usable, impact_sum rho 0.0 (p 1.0), free control 0.4, sign right 1/5, lean_vs_free_control_rho 0.70 (5 names; short_squeeze/short_building unresolvable, no register positions). Panel resolved too. One day is not a result.
