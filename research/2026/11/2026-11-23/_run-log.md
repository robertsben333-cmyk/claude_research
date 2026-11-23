# Run log — 2026-11-23

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-20 14:38 UTC
- Fired 14:36Z 2026-11-20 (Fri); sealing for event date 2026-11-23 (Mon), next European session. Plan: universe -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff. Publishing to main (EARNINGS_DATA_BRANCH=main). Note: local main in this container had diverged from a force-rewritten origin/main; worked on a fresh branch from origin/main (db07cde10), publish.sh pushes HEAD:main.

## Stage EU — IBKR
- Logged at 2026-11-20 14:38 UTC
- mode (no broker call): IBKR_ENVIRONMENT=None IBKR_ACCOUNT_ID=missing; broker=IB Gateway on executor's server (auth tws); 'would refuse: IBKR_ENVIRONMENT None vs execution_eu.environment live' — expected in this session, which only hands off.

## Stage EU — universe + baselines
- Logged at 2026-11-20 14:40 UTC
- 10 scheduled, 3 eligible above $100k, 3 hunted (all, under cap 20): no 1 (NYKD), se 1 (VER), uk 1 (CER). Largest market uk 33% (3 markets, one name each). Registers no/se/uk read. session_unresolved: all three (bmo assumed). bankier (pl issuer calendar) HTTP 403. provenance stamped (orchestrator claude-opus-5-5). One wave: NYKD VER CER.

## Stage EU — hunts
- Logged at 2026-11-20 14:44 UTC
- NYKD: confirmed bmo (company invitation NewsWeb 686560, 'before the opening'). impact_sum +0.3, abs 5.5, p_up 50. No bar sourceable; runway restatement after placement + tax ruling is the only new line, sign uncallable.

## Stage EU — hunts
- Logged at 2026-11-20 14:44 UTC
- CER: confirmed bmo (07:00 RNS pattern; issuer notice 9875780). impact_sum +0.2, abs 7.0, p_up 49. FY26 already pre-released 14 Sep (warning, -12.5%); move is FY27 outlook + order book; one broker bar (Canaccord ~+10% rev).

## Stage EU — hunts
- Logged at 2026-11-20 14:48 UTC
- VER: event confirmed (company calendar 23 Nov); bmo by pattern (06:00 CET every prior report). impact_sum -2.6, abs 12.0, p_up 44. Lead: FY26 revenue guide (EUR 680-720m) needs Q4 +14% y/y on 3.5% organic growth; new CFO since 3 Nov; securitisation unannounced; offset by CEO buys and peer beats.

## Stage EU — panel STARTED
- Logged at 2026-11-20 14:48 UTC
- 3 packs, four judges

## Stage EU — panel
- Logged at 2026-11-20 14:51 UTC
- 4/4 judges, no fallback. VER selected 4/4, panel_pct 100 short. NYKD 3, CER 4.

## Stage EU — IBKR handoff
- Logged at 2026-11-20 14:52 UTC
- handoff written: 0 names. VER (panel_pct 100 short, 4/4) not taken: median turnover $0.19m below execution_eu.selection.min_turnover_usd $0.20m. Server will buy nothing. Published to main.

## Stage E-P amc exit — 2026-11-23
- Logged at 2026-11-23 14:10 UTC
- Fired 14:09 UTC (09:09 ET). Guards: live and paper both exit 0 (amc -> open as market DAY, matched on placement). verify --fix: live 5 legs all ok, paper 7 legs all ok, nothing UNFILLED, no rescue sent. close --today-only: live 6 runs and paper 25 runs scanned, NO leg due today on either account, nothing sent, nothing refused. Reason: the 2026-11-20 E-P run entered no positions (alpaca-orders.json and alpaca-orders-live.json: entries [], positions 0).

## Edge hunt (panel) — 2026-11-23 amc + 2026-11-24 bmo — STARTED
- Logged at 2026-11-23 18:09 UTC
- Fired 18:07 UTC (13:07 ET). Universe 43 (18 amc 11-23, 25 bmo 11-24); CENT/CENTA not folded by share_class.py, CENTA will not be hunted. Baselines sealed for all 43. Plan: one edge-sweep, up to 20 unpriced-searchers (<=8 per turn), four judges, then 3s flatten and 6b buy (live then paper).

## Edge hunt (panel) — sweep
- Logged at 2026-11-23 18:15 UTC
- Sweep confirmed 40 of 43 (CENTA folded into CENT, not hunted); unconfirmed FLNC, KSS, BBY (calendar only); 0 phantoms. Session unsettled: HPE (amc very likely), AMTM (after today's close either way), MOV. Wave plan: 20 hunted by hunt_priority — SYM SMTC ANF DY KC CMP MMED HPE DKS TUYA TIGR DLTR EMBC ZM TITN BURL CENT BZUN AMTM VALN; shed (below cap): EPSN CMBT MOV ALCO SJM J BILI A DAC ITRN BWLP ADI VIPS FLX ZH PFLT PNNT MDT FSCO + the 3 unconfirmed. Option-chain names among the shed (SJM, J, A, ADI, MDT, BILI, VIPS) were not kept back in: the hunted 20 are mostly optioned already. Wave 1 (amc first): SYM SMTC CMP HPE TUYA ZM CENT AMTM. SEC_USER_AGENT unset: FPI histories empty.
