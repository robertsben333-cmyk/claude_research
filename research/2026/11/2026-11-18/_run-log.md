# Run log — 2026-11-18

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-17 14:37 UTC
- Fired 14:37 UTC 2026-11-17 (15:36 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-18 (Wed). Plan: universe (cap 20), baselines, provenance, one hunter per name in waves of 5, score, four-judge panel, note, IBKR handoff. Local main was stale after an origin force-update; checked out origin/main 187a5553f.

## Stage EU — IBKR
- Logged at 2026-11-17 14:37 UTC
- mode: broker=IB Gateway on the executor's server (execution_eu.auth tws); this session only hands over. Last line: would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is 'live' (expected here — no credentials in this session).

## Stage EU — universe sealed
- Logged at 2026-11-17 14:47 UTC
- Event date 2026-11-18 (Wed). 47 scheduled, 27 eligible above $100k, random draw of 20 (seed eu-2026-11-18): uk 8, no 5, pl 3, se 2, de 1, it 1 (fr/dk/fi/es 0). Largest market uk 40%, 6 markets. No market closed. 20 baselines sealed ~14:45 UTC (intraday spots, not closes). Provenance stamped (orchestrator claude-opus-5-5). Wave 1 launched: PFS0 TISG CLN CPS KGH.

## Stage EU — hunts
- Logged at 2026-11-17 14:50 UTC
- TISG banked: no event (shares suspended by Borsa Italiana since 2026-11-03 under concordato preventivo; issuer calendar has no 18 Nov date) -> phantom, impact 0. ELON launched in its slot.

## Stage EU — hunts
- Logged at 2026-11-17 14:54 UTC
- CLN banked: impact_sum -0.2, abs 5.5, p_up 46. Hunter set session_check amc (6 of last 7 periodic reports released after the 17:00 Warsaw close). SVEAF_B launched.
