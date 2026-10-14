# Run log — 2026-10-15

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-14 06:42 UTC
- Sealing for the next ASX session (2026-10-15). Plan: universe -> seal baselines -> one unpriced-hunter-au per name in waves of 5 -> edge_score -> four-model panel -> note.

## Stage AU — panel STARTED
- Logged at 2026-10-14 06:49 UTC
- 1 pack (BOQ), four judges

## Stage AU — Australia researcher — DONE
- Logged at 2026-10-14 06:51 UTC
- Funnel 1/1/1 (BOQ, FY results, bmo). impact_sum +0.40 (p32), below the 2.8 floor; impact_scaled +0.33. Panel 4/4 members ran, BOQ not selected (k=0, sign 4/4 +, panel_score +0.34). ASIC register as of 2026-10-08, lag 4 sessions. Provenance au.v4 · claude-opus-5-5. No orders (this stage has none).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-14 13:39 UTC
- Fired 13:38 UTC 2026-10-14 (European markets still open; sealed spot is intraday). Sealing for EVENT DATE 2026-10-15 (Thu), the next European trading day.
- Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model panel -> note. No orders.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-14 13:42 UTC
- 28 scheduled, 18 eligible (uk 6, se 8, no 2, de 1, fi 1), all 18 hunted (under cap 20). Largest market se 44%. Calendar adds: RNS added 7 UK names (all session_unresolved), Yahoo added EQT, Inderes added PCOM_B (not eligible). All five registers read (uk de se no fi). Provenance stamped (orchestrator model flag omitted). Waves: [2GB NDA_FI ENTRA NEL AQ] [CARA EMIL_B EQT ERIC_A OEM_B] [SLP_B WALL_B AVCT CAML] [DNLM ENT WTB XPS].

## Stage EU — panel STARTED
- Logged at 2026-10-14 14:01 UTC
- 18 hunts done; 15 ranked, 0 above 2.8. Not ranked (no event on 10-15): AVCT (investor presentation of 09-30 interims), CAML (date is Cygnus scheme Effective Date — uk_rns_calendar misparsed it as results), WTB (interims brought forward to 10-13). OEM_B hunter says release is in-session on 10-15 (vendor said amc). NEL hunter: NO register lists issuer as 'NEL' at 0.59% (Tages), baseline read 0.0 — eu_positioning NO join likely needs ISIN match. 15 packs, four judges next.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-14 14:09 UTC
- Event date 2026-10-15. 15 ranked (top CARA/XPS +0.70, bottom NEL -1.60), 0 above floor 2.8. Not ranked: AVCT, CAML, WTB (no event on 10-15; all three from uk_rns_calendar; CAML = parser read a scheme Effective Date as results). Amend event_occurred:false after the window.
- Panel: 4/4 members, no fallback, 0 selected (NEL closest, k=1... panel_pct 68 short). Note: europe-note.md. Resolve within ~a week (se/fi Nordic feed window). Published with EARNINGS_DATA_BRANCH=main.
