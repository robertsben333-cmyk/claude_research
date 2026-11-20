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

## Stage EU — DONE
- Logged at 2026-11-19 15:03 UTC
- 4 of 7 ranked, 0 above floor, panel selects none; PRS handed off at pct 72.6. Everything pushed to origin/main (EARNINGS_DATA_BRANCH=main), last commit 8a1bde6 confirmed with git log origin/main.

## Stage E-P amc exit — 2026-11-20
- Logged at 2026-11-20 14:08 UTC
- 14:08 UTC (09:08 ET). Guards: live and paper both exit 0 (amc -> open as market DAY, matched on placement). Verify: live STEM/OMER/FEAM/RRGB/SNEX ok, paper CURI/CTVA/STEM/OMER/FEAM/RRGB/SNEX ok; nothing UNFILLED, no rescues. Close (--today-only): nothing due on either account, nothing sent, nothing refused. Expected: the 2026-11-19 edge-panel book was empty on both accounts (GRSD not shortable; the no-strong-name top-up landed on main at 18:59 UTC, after that run's 18:49 plan).

## Edge hunt (panel) — 2026-11-20 amc + 2026-11-23 bmo — STARTED
- Logged at 2026-11-20 18:09 UTC
- Fired 18:07 UTC (13:07 ET). Window: 6 confirmed-session names (DLNG amc 11-20; VNET CRGO THCH ADXN BLRX bmo 11-23). Thin day: 40 time-not-supplied rows checked with session_resolve.py (1 killed, 39 carried, 0 announced); the 17 largest carried rows go to the sweep to settle date and session, baselines for any it confirms are sealed before any searcher launches. SEC_USER_AGENT is NOT set in this environment, so www.sec.gov answered 403 and the EDGAR filing checks in session_resolve/priced_in are degraded. Plan: 1 sweep, up to 20 searchers, 4 judges; sell at 3s, buy at 6b, live then paper.

## Edge hunt (panel) — sweep
- Logged at 2026-11-20 18:13 UTC
- Sweep confirmed 5 of 23 (DLNG amc 11-20; VNET CRGO THCH BLRX bmo 11-23). ADXN not confirmed (no company notice; calendar row only). 17 time-not-supplied rows: 0 confirmed (11 positively killed: TCOM 1 Dec, KT/TRON/GDEV already reported, HTT/LOT semi-annual, AIV liquidation, AREC/FSI delayed filings, SOWG, PVL; 6 with no company date). Wave: 5 searchers, all hunted, none shed.

## Edge hunt (panel) — 3s sell
- Logged at 2026-11-20 18:22 UTC
- 18:22 UTC: all 5 searchers finished (hunt_status: 0 unfinished of 5). Live: mode ok (live enabled, kill switch off); flatten: 0 positions held, nothing to sell. Paper: flatten: 0 positions held, nothing to sell. No amc leg was still held.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-20 18:22 UTC
- 5 packs, four judges
