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

## Stage EU — hunts
- Logged at 2026-11-17 15:07 UTC
- SVT banked: impact_sum +0.1, abs 2.5, p_up 52; interims bmo confirmed (9 Jul trading update). Remaining: MSLH SDY WKP.

## Stage EU — hunts
- Logged at 2026-11-17 15:08 UTC
- MSLH banked: impact_sum -1.4, abs 5.5, p_up 45; 10-month trading update confirmed (notice 3 Nov), bmo 07:00 by precedent. Remaining: SDY WKP.

## Stage EU — hunts
- Logged at 2026-11-17 15:08 UTC
- SDY banked: impact_sum -0.7, abs 8.0, p_up 46; H1 bmo 07:00 confirmed (issuer calendar). Remaining: WKP.

## Stage EU — panel STARTED
- Logged at 2026-11-17 15:09 UTC
- 20 of 20 hunted; 18 ranked, ENH and TISG not ranked (no event on 18 Nov: ENH Q3 is 27 Nov per issuer calendar; TISG suspended under concordato). No name above the 2.8 floor; top ITH +0.90, bottom MSLH -1.40. 18 packs, four judges launching.

## Stage EU — IBKR handoff
- Logged at 2026-11-17 15:17 UTC
- ibkr-handoff.json written (no broker call): SELL PFS0 (de, pct 97.5, 66 sh @ 60.5 EUR, 39.9%), SELL MSLH (uk, 95.6, 1857 sh @ 1.7063 GBP, 38.0%), SELL SDY (uk, 85.4, 13219 sh @ 0.138 GBP, 21.9%) on a 10,000 EUR offline plan. Not taken: ARR (turnover $0.13m < $0.20m floor), ELON ($0.16m < floor), CTEC (65.8), ITH (66.9).

## Stage EU — DONE
- Logged at 2026-11-17 15:17 UTC
- 20 hunted, 18 ranked (ENH phantom: issuer dates Q3 27 Nov; TISG suspended, no event). No name above the 2.8 floor; key top ITH +0.90, bottom MSLH -1.40. Panel (4 of 4 members, no fallback) selects PFS0, ARR, MSLH, SDY short. Handoff: PFS0, MSLH, SDY short. Published to origin/main (EARNINGS_DATA_BRANCH=main; publish.sh's rebase raced hunters writing eu-short-cache.json, so most pushes were plain git rebase + push HEAD:main). Ran 6-7 hunters concurrently rather than strict waves of 5 to reach the handoff before the close. CLN/CPS/KGH hunters set session amc against the vendor's bmo default.

## Stage E-P amc exit — 2026-11-18
- Logged at 2026-11-18 14:09 UTC
- 09:09 ET. Guards: live exit 0, paper exit 0 (amc -> open as day). verify: live STEM/OMER ok, paper CURI/CTVA/STEM/OMER ok, nothing UNFILLED, no rescue. close --today-only: LIVE FEAM amc SELL market DAY queued for open, order efdf3245-d2dc-4103-ad36-81daababd0d9; PAPER FEAM amc SELL market DAY, order 9fa3d307-b1b9-487f-a62c-cde1e8ebbc72. Refused on both: JMIA bmo (market placement, market closed; left for stage E-P's own run).

## Edge hunt (panel) — 2026-11-18 amc + 2026-11-19 bmo — STARTED
- Logged at 2026-11-18 18:08 UTC
- Fired 18:07 UTC (13:07 ET). Universe 38 names (17 amc 11-18, 21 bmo 11-19); 38 baselines sealed in edge-panel/baselines. Plan: one edge-sweep, up to 20 unpriced-searchers by hunt_priority amc first, four judges.

## Edge hunt (panel) — sweep and waves
- Logged at 2026-11-18 18:14 UTC
- 18:15Z: Sweep: 34 confirmed of 38 (unconfirmed BEEM, LQDT, WMG, BORR; sweep file's top-level count says 35, the agent reports 34 correct); session unsettled WMT HP MMS CCIF EVAX WMG. Cap 20 by hunt_priority: hunted RRGB ARBE PCYO EVAX MAGN KLIC FUTU RERE SNEX DAO YMM BBWI P JOYY WWD UTI CPA MMS PDD VVV; shed (lowest priority) WSM SBLK NTES HP BABA EVGN TEN PANW MANU UGI WMT NJR ROAD CCIF. Only RRGB's baseline carries a live option chain. CPA baseline_history_trustworthy=false. Wave 1 (amc): RRGB PCYO KLIC SNEX P JOYY WWD UTI.
## Edge hunt (panel v3b) — 2026-11-18 amc + 2026-11-19 bmo — STARTED
- Logged at 2026-11-18 18:16 UTC
- 38 names in window (17 amc 11-18, 21 bmo 11-19), 38 baselines sealed in edge-panel-v3b/baselines before any agent. Plan: 1 edge-sweep, up to 20 unpriced-searcher-v3b (<=6 per turn, amc first), 4 panel-judge-v3b judges. No orders. Fired 18:11 UTC.

## Edge hunt (panel v3b) — sweep and waves
- Logged at 2026-11-18 18:25 UTC
- 18:27Z sweep: 36 confirmed of 38 (unconfirmed WMG, BEEM); session unsettled WMG EVAX BEEM. Cap 20 by hunt_priority: hunted BORR UTI RRGB FUTU BBWI KLIC HP P MMS SBLK WSM RERE LQDT JOYY MAGN TEN VVV DAO BABA WWD; shed YMM SNEX PDD CPA PCYO UGI MANU ROAD PANW ARBE NTES EVAX NJR EVGN WMT CCIF WMG BEEM. Wave 1 (amc): BORR UTI RRGB KLIC HP P.

## Edge hunt (panel) — baselines amended
- Logged at 2026-11-18 18:32 UTC
- 18:32Z: 19 of 20 searchers returned, 0 unfinished (hunt_status). Amended RRGB and MMS suspect -> unknown from company sources (RRGB rescheduled release; MMS's 10-20 8-K was an acquisition, not a print). HP and ROAD also read suspect but were not hunted. VVV still running.

## Edge hunt (panel) — step 3s flatten
- Logged at 2026-11-18 18:32 UTC
- 18:33Z: all 20 searchers returned, hunt_status 0 unfinished of 20. LIVE: held JMIA -295 sh (short, +38.1% unrealised as reported), closed at market. PAPER: held JMIA -2187 sh (short), closed at market. FEAM (amc) was already sold by the 09:00 ET amc-exit Routine on both accounts; no amc leg was still held here. Both accounts report closed.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-18 18:33 UTC
- 20 packs, four judges
## Edge hunt (panel v3b) — sweep and waves
- Logged at 2026-11-18 18:33 UTC
- 18:34Z HP, P returned (v3b fields present, search complete). Wave 2 launched: SBLK JOYY WWD FUTU.

## Edge hunt (panel v3b) — sweep and waves
- Logged at 2026-11-18 18:35 UTC
- 18:45Z BORR, UTI returned (v3b fields present, complete). Wave 3: BBWI MMS.

## Edge hunt (panel v3b) — sweep and waves
- Logged at 2026-11-18 18:43 UTC
- 18:43Z all 20 searchers launched (last BABA). Returned so far, all with v3b fields and search_complete true: HP P BORR UTI RRGB KLIC JOYY FUTU SBLK WWD BBWI MMS.
