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

## Stage EU — hunts
- Logged at 2026-11-17 14:56 UTC
- PFS0 banked: impact_sum -1.3, abs 9.0, p_up 46; Q3 confirmed (EQS 2026-11-11), bmo 08:00 CET from issuer timestamps. ARR launched.

## Stage EU — hunts
- Logged at 2026-11-17 14:56 UTC
- ELON banked: impact_sum +0.7, abs 10, p_up 52; Q3 confirmed (issuer calendar, MFN est. 08:30 CET). ENH launched.

## Stage EU — hunts
- Logged at 2026-11-17 14:57 UTC
- CPS banked: impact_sum +0.1, abs 6.0, p_up 53; session_check amc (files after Warsaw close; H1 stamped 17:47) so the bmo window likely holds no release. HAFNI launched.

## Stage EU — hunts
- Logged at 2026-11-17 14:58 UTC
- KGH banked: impact_sum -0.2, abs 4.5, p_up 47; session_check amc (last three releases 17:30-17:49 Warsaw). ENH banked: phantom — issuer calendar (NewsWeb 685636) dates Q3 to 2026-11-27, event_confirmed false. PEN and VOW launched.

## Stage EU — hunts
- Logged at 2026-11-17 15:00 UTC
- ARR banked: impact_sum -0.5, abs 8.0, p_up 44; bmo 07:30 Oslo confirmed. BLND launched.

## Stage EU — hunts
- Logged at 2026-11-17 15:01 UTC
- SVEAF_B banked: impact_sum 0.0, abs 5.5, p_up 47; bmo 07:30 CET confirmed. CTEC and ITH launched (6 concurrent from here, to reach the handoff before the 17:30 CET close).

## Stage EU — hunts
- Logged at 2026-11-17 15:02 UTC
- HAFNI banked: impact_sum +0.2, abs 4.5, p_up 52; bmo ~07:30 CET (NewsWeb 686176). MSLH launched.

## Stage EU — hunts
- Logged at 2026-11-17 15:03 UTC
- VOW banked: impact_sum -0.9, abs 8.0, p_up 46; bmo confirmed (NewsWeb 686196). SDY launched.

## Stage EU — hunts
- Logged at 2026-11-17 15:03 UTC
- PEN banked: impact_sum -0.1, abs 4.0, p_up 50; bmo 07:00 CET (NewsWeb 686174). SSE and SVT launched.

## Stage EU — hunts
- Logged at 2026-11-17 15:03 UTC
- BLND banked: impact_sum +0.3, abs 2.6, p_up 50; bmo 07:00, H1 pre-released in 15 Oct trading statement. WKP launched (last name).

## Stage EU — hunts
- Logged at 2026-11-17 15:07 UTC
- SSE banked: impact_sum +0.6, abs 3.0, p_up 53; bmo 07:00, H1 EPS pre-released 1 Oct.

## Stage EU — hunts
- Logged at 2026-11-17 15:07 UTC
- CTEC banked: impact_sum -1.2, abs 7.5, p_up 45; 10-month trading update confirmed (H1 scheduled events), bmo 07:00 by precedent.

## Stage EU — hunts
- Logged at 2026-11-17 15:07 UTC
- ITH banked: impact_sum +0.9, abs 5.5, p_up 52; Q3 bmo confirmed (issuer calendar). Rosebank consent risk filed outside window.
