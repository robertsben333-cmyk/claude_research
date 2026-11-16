# Run log — 2026-11-17

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-16 14:37 UTC
- Fired 14:36 UTC 2026-11-16 (15:36 Amsterdam, markets open). Sealing for event date 2026-11-17 (next European session). Plan: universe (cap 20, $100k floor) -> seal -> one bilingual hunter per name in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff. Note: local main in this container had diverged from a force-updated origin/main; the run works on a fresh branch off origin/main and publishes HEAD:main.

## Stage EU — IBKR
- Logged at 2026-11-16 14:38 UTC
- mode (no broker call from this session): broker = IB Gateway on executor's server (auth tws); this session only hands over. Last line: 'would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is live' — expected here, no IBKR env in the Routine.

## Stage EU — universe and seal
- Logged at 2026-11-16 14:41 UTC
- Event date 2026-11-17 (Tue). 38 scheduled, 21 eligible above $100k, random draw of 20 (seed eu-2026-11-17): uk 5, se 3, dk 3, pl 3, de 2, es 2, fr 1, no 1. Largest market uk 25%, 8 markets. 20 baselines sealed ~14:45 UTC (intraday spots, not closes). Provenance stamped. Wave 1 launched: DPLM IMB ZEG ALO NIBE_B.

## Stage EU — hunts
- Logged at 2026-11-16 14:49 UTC
- Banked so far: DPLM +0.5, IMB -1.7, ALO -0.2 (amc 18:00 CET confirmed), NIBE_B +0.9. Running at 5 concurrent rather than strict waves, to reach the IBKR handoff before the 17:30 CET close. DEFECT for a building session: NIBE_B baseline seals short 0.0 but FI shows 5.27% aggregate (LEI 549300ZQH0FIF1P0MX67); looks like a register name-join miss in eu_positioning for se. Baseline left sealed as is.

## Stage EU — register defect
- Logged at 2026-11-16 14:54 UTC
- Second Swedish short-register miss: SEYE baseline 0.0 / anchor_covered false, FI aggregate lists 'Smart Eye Aktiebolag (publ)' at 4.47% (2026-11-13). With NIBE_B (5.27%) this is a systematic se name-join failure in eu_positioning; baselines left sealed. Fix in a building session.

## Stage EU — Spain register lead
- Logged at 2026-11-16 14:58 UTC
- EDR hunter: CNMV per-issuer short page (posicionescortas?nif=A02850956, and per-holder posicionescortascomunicaciones.aspx?nif=…&idDecl=<LEI>) answers from this container where the grid the baseline uses does not; EDR disclosed shorts 3.15% (Citadel 1.46, CFM 0.89, ActusRay 0.80). Possible Spanish positioning anchor for a building session to verify; baselines unchanged.

## Stage EU — panel STARTED
- Logged at 2026-11-16 15:12 UTC
- 20 of 20 hunted; 19 ranked, PXM not ranked (issuer's own date is 2026-11-23: a phantom). No name above the 2.8 floor; top NIBE_B/REACH +0.90, bottom OHLA -2.20. Packs built, four judges launching.
