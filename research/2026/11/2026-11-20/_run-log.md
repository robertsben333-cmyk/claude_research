# Run log — 2026-11-20

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-19 14:37 UTC
- Fired 14:37Z 2026-11-19 (Thu); sealing for event date 2026-11-20 (Fri), next European session. Plan: universe -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff. Publishing to main (EARNINGS_DATA_BRANCH=main).

## Stage EU — IBKR
- Logged at 2026-11-19 14:38 UTC
- mode (no broker call): IBKR_ENVIRONMENT=None IBKR_ACCOUNT_ID=missing; broker=IB Gateway on executor's server (auth tws); 'would refuse: IBKR_ENVIRONMENT None vs execution_eu.environment live' — expected in this session, which only hands off.

## Stage EU — universe + baselines
- Logged at 2026-11-19 14:48 UTC
- 28 scheduled, 7 eligible above $100k, 7 hunted (all, under cap 20): no 3 (JACK, PNOR, PRS), pl 2 (BMC, CMP), se 1 (PAX), uk 1 (TRI). Largest market no 43%. Registers: no/se/uk read, pl none. session_unresolved: JACK, BMC, CMP, TRI. provenance stamped (nordic.v5, pl.v5, uk; orchestrator claude-opus-5-5).
- Wave 1 launched: JACK PNOR PRS PAX TRI. Wave 2: BMC CMP.

## Stage EU — hunts
- Logged at 2026-11-19 14:50 UTC
- TRI: hunter reports NO event on 2026-11-20 (event_confirmed false). Half-year report was 2026-11-17 07:00 RNS (-19.82%), the date the 20 Oct trading update named; the RNS-calendar row is stale. Findings empty.

## Stage EU — hunts
- Logged at 2026-11-19 14:50 UTC
- JACK: phantom (event_confirmed false). Issuer calendar (NewsWeb 2026-05-03) and MFN put Q3 on 2026-11-25; the vendor's 11-20 is an estimate. Findings empty.

## Stage EU — hunts
- Logged at 2026-11-19 14:50 UTC
- BMC: no event in window. ESPI 68/2026 (2026-11-17) moved the Q3/9M report to 2026-11-30; findings empty. Third phantom of three hunts so far.

## Stage EU — hunts
- Logged at 2026-11-19 14:51 UTC
- PNOR: confirmed bmo (06:30 CET, NewsWeb 13 Nov). impact_sum +0.1, scaled -0.4 (abs 3.3, p_up 44). Baseline history row 2026-05-29 (-27.5%) is mostly an ex-distribution, not a results reaction.

## Stage EU — hunts
- Logged at 2026-11-19 14:55 UTC
- PRS: confirmed bmo (07:00 CET). impact_sum +0.1 (guide +0.6, cash +0.2, recontracting -0.4, Caius selling -0.3), abs 6.5, p_up 52. Unexplained -9.9% on 7x volume 17 Nov.

## Stage EU — hunts
- Logged at 2026-11-19 14:56 UTC
- PAX: confirmed bmo (07:00 CET, MFN). impact_sum +0.2, abs 7.5, p_up 51. Bar: DNB Carnegie commissioned preview (sales SEK105m).

## Stage EU — hunts
- Logged at 2026-11-19 14:58 UTC
- CMP: event confirmed (RB 1/2026). Hunter says session is AMC (H1 at 20:15, FY at 17:12), not the sealed bmo. impact_sum +0.2, abs 5.0, p_up 52. Two scraped PAX scratch pages (cmsreg.html, fc.html) removed: GitHub push protection flagged an embedded third-party Mapbox token.

## Stage EU — panel STARTED
- Logged at 2026-11-19 14:59 UTC
- 4 packs (CMP PAX PNOR PRS), four judges. Scored: 4 of 7 rankable, 0 above floor 2.8; BMC JACK TRI not ranked (no event).

## Stage EU — IBKR handoff
- Logged at 2026-11-19 15:02 UTC
- ibkr-handoff.json written 15:02Z: 1 name, PRS long (no, panel_pct 72.6, all four judges), offline plan 12,770 sh @ 4.175 NOK ≈ 50% cap. No broker call from this session.
