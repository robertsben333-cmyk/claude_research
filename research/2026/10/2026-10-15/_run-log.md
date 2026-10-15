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

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-15 01:05 UTC
- Fired 01:04 UTC (10:04 JST). Plan: jp_universe -> seal baselines -> provenance -> one unpriced-hunter-jp per name in waves of 5 -> edge_score -> four-model panel -> note. No orders.

## Stage J — resolved 2026-10-13 run (from the 10-15 session)
- Logged at 2026-10-15 01:07 UTC
- jp_resolve: 25/25 usable, rho impact_sum 0.27 p 0.199, free control -0.277, sign right 0.56, lean_vs_free_control_rho 0.406. Panel: rho 0.118 p 0.565; 3 selected, 2 hits (+3.37%). One day is not a result.

## Stage J — hunts in progress
- Logged at 2026-10-15 01:13 UTC
- 1418 +4.5, 1430 -0.3, 1407 +3.0 banked. 1407: 決算短信 hit TDnet at 10:00 JST, six minutes BEFORE the 10:06 seal, so its hunter read the release itself (release_preceded_seal: true). Sealed spot 2101 matches pre-10:00 quotes, so the window holds the reaction, but the finding is knowledge of the print, not a forecast; flagged in the note and must not count as evidence for the hunt. Hunters also collided in the shared scratchpad; later hunters are given their own subfolders.

## Stage J — panel STARTED
- Logged at 2026-10-15 01:35 UTC
- 25 hunts banked and scored (edge-scores.json, key impact_sum). Above floor 2.8: 1418 +4.5, 5817 +3.1, 1407 +3.0 (1407 release preceded seal). 25 packs, four judges. Note: two hunters ran over the concurrency cap of 5 briefly (7 at once) at the end.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-15 01:44 UTC
- 129 scheduled / 67 eligible / 25 hunted (seeded random draw). 25/25 hunts, 0 empty. Above floor 2.8: 1418 +4.50, 5817 +3.10, 1407 +3.00 (1407 release at 10:00 JST preceded the 10:06 seal: contaminated). Bottom 3547 -1.00. 12+/10-/3 zero. Panel 4/4 members, no fallback: 7 selected (1418, 1407, 5817, 367A long; 3547, 414A, 6224 short). Register as_of 2026-10-14 (current). Prov jp.v5. Note: japan-note.md. No orders.
