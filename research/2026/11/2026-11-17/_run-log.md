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
