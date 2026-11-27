# Run log — 2026-11-27

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-26 14:38 UTC
- Fired 14:36 UTC 2026-11-26 (Thu). Sealing for event date 2026-11-27 (Fri). RUN=research/2026/11/2026-11-27/europe. Plan: universe (cap 20), seal, one hunter per name, score, 4-judge panel, note, IBKR handoff. Local main was a stale pre-force-push copy (diverged 52/58); worked from a detached checkout of origin/main, local branch left untouched.

## Stage EU — IBKR
- Logged at 2026-11-26 14:38 UTC
- mode: auth tws, executor server trades; cloud has no broker env (expected). Last line: would refuse: IBKR_ENVIRONMENT None vs execution_eu.environment 'live' (cloud only; no call made).

## Stage EU — universe sealed
- Logged at 2026-11-26 14:43 UTC
- 42 scheduled, 11 eligible, 11 hunted (all, under cap 20): no 5 (DDRIL ENH NORAM PLSV VTURA), pl 4 (MDV NTT PLW VGO), de 1 (GXI), se 1 (RVRC). bankier (pl issuer calendar) 403. 11 baselines sealed.

## Stage EU — hunters launched
- Logged at 2026-11-26 14:44 UTC
- 8 running (concurrency limit 8): DDRIL ENH NORAM PLSV VTURA RVRC GXI MDV. Queued: NTT PLW VGO.

## Stage EU — hunts banked (1)
- Logged at 2026-11-26 14:45 UTC
- NORAM back: phantom (Q3 released 2026-11-24 17:13 UTC on NewsWeb 687324; 11-27 is only a distribution payment date), event_confirmed false. NTT launched in the freed slot.

## Stage EU — hunts banked (2)
- Logged at 2026-11-26 14:45 UTC
- RVRC back: phantom (Q1 released 2026-11-19 07:30 CET; 11-27 is the SEK 1.50 ex-dividend day, ~-2.8% mechanical on unadjusted close — resolver must not score it). PLW launched.

## Stage EU — hunts banked (3)
- Logged at 2026-11-26 14:49 UTC
- VTURA back: real release 11-27 before Oslo open; target of ENH all-share bid (5.50 ENH/VTURA, LOI 2026-09-11) — ENH also in today's set, so VTURA and ENH are one correlated exposure. impact_sum +0.1. VGO launched (last).

## Stage EU — hunts banked (4)
- Logged at 2026-11-26 14:49 UTC
- GXI back: real (delayed final H1 report, H1 pre-released 30 Sep), impact_sum -0.3.

## Stage EU — hunts banked (5)
- Logged at 2026-11-26 14:49 UTC
- PLSV back: confirmed bmo ~07:00 CET, impact_sum +0.4.

## Stage EU — hunts banked (6)
- Logged at 2026-11-26 14:49 UTC
- DDRIL back: confirmed 07:30 CET bmo, impact_sum -1.5 (Borgland Dolphin still moored Las Palmas vs 'on contract from November' guide). Running: ENH MDV NTT PLW VGO.

## Stage EU — hunts banked (7)
- Logged at 2026-11-26 14:50 UTC
- ENH back: confirmed 06:00 CET bmo, impact_sum -0.4. Running: MDV NTT PLW VGO.

## Stage EU — hunts banked (8)
- Logged at 2026-11-26 14:50 UTC
- MDV back: date confirmed 27 Nov but session amc (Modivo publishes after close; Q1 17:55, H1 ~22:00) — real window close(11-27)->close(11-30). impact_sum +0.4. Running: NTT PLW VGO.

## Stage EU — hunts banked (9)
- Logged at 2026-11-26 14:52 UTC
- PLW back: date confirmed (snippet), session likely amc on issuer pattern (no timestamp for this release), impact_sum +0.1. bankier.pl 403 to curl and WebFetch. Running: NTT VGO.

## Stage EU — hunts banked (10)
- Logged at 2026-11-26 14:53 UTC
- NTT back: date confirmed (RB 1/2026), session likely amc on pattern (H1 20:46), impact_sum -0.3, impact_scaled +0.72 (sign disagrees). Running: VGO.

## Stage EU — hunts
- Logged at 2026-11-26 14:54 UTC
- 11/11 hunted. Phantoms (no event in window): NORAM (Q3 out 11-24), RVRC (Q1 out 11-19; 11-27 ex-div). Hunters settle MDV, NTT, PLW, VGO as amc on 11-27 (window close(11-27)->close(11-30)). VGO impact_sum +0.4.

## Stage EU — panel STARTED
- Logged at 2026-11-26 14:55 UTC
- 9 packs, four judges

## Stage EU — panel
- Logged at 2026-11-26 14:58 UTC
- 4/4 judges, no fallback. Selected (3 of 4 in own top 20%): DDRIL 92 short (4/4), NTT 89 long (4/4), MDV 82 long (3/4). VGO 65 long, ENH 60 short not selected.

## Stage EU — IBKR handoff
- Logged at 2026-11-26 14:58 UTC
- handoff written (before the note, 14:58 UTC): 3 names, offline plan at sealed spots on EUR 10,000: SELL DDRIL 27.9%, BUY NTT 40.7%, BUY MDV 31.3%. Not taken (<70): VGO 65.0, ENH 60.4. Caveat for the operator: hunters settle NTT and MDV as amc on 27 Nov (after the Warsaw close; issuer pattern, MDV H1 at ~22:00, NTT H1 at 20:46), so a position held only to the 15:35 Amsterdam flatten on 27 Nov exits BEFORE the print. DDRIL is a confirmed 07:30 CET bmo release.

## Stage EU — done
- Logged at 2026-11-26 14:59 UTC
- Note published. Handoff went out before the note. Pushed to main (EARNINGS_DATA_BRANCH=main). Calendar defect again: NORAM and RVRC dated on a distribution/ex-dividend day, not a results day. 4 of 9 ranked names (all Polish) release amc on 11-27, outside the sealed bmo window; two are panel selections.

## Stage E-P amc exit — 2026-11-27
- Logged at 2026-11-27 14:08 UTC
- Fired 14:07 UTC (09:07 ET). Guards: live and paper both exit 0 (amc -> open as day, matched on placement). verify --fix: live 9 exit legs all ok, paper 11 all ok; nothing UNFILLED, no rescue. close --today-only: one leg due on each account, FINV short (2026-11-25 amc, panel_pct -79.2): live buy 484 and paper buy 3360 NOT SENT, HTTP 403 insufficient qty available (available 0). Cause, read from the broker: a market DAY buy-to-cover for the full position was already open on each account, placed outside this repo with a random client_order_id (live 700936da-6422-4226-979b-6bbe99babd1b at 12:00:04 UTC, 3 rows down. paper d9a1ac75-09d1-41d1-8126-9f10a1fd2c56 at 09:00:30 UTC), status new, so FINV goes at the open either way. No bmo legs due; no other refusals.

## Edge hunt (panel) — 2026-11-27 amc + 2026-11-30 bmo — STARTED
- Logged at 2026-11-27 18:09 UTC
- Fired 18:07 UTC (13:07 ET), the day after Thanksgiving: the US session closed early at 13:00 ET, so it was already shut when this run fired. Window 11-27 amc + 11-30 bmo: 4 of 28 calendar rows have a session (CHA HMR BOSC PWRL, all 11-30 bmo); baselines sealed. Thin day: 19 time-not-supplied rows checked with session_resolve.py (2 killed by EDGAR: KT filed 2.02 today, PVL 11-18; 17 carried, 0 announced). The 17 carried rows go to the sweep to settle date and session; baselines for any it confirms are sealed before any searcher launches. Plan: 1 sweep, up to 20 searchers, 4 judges. Step 6b buy WILL be refused (market closed, and every name prints Monday bmo); step 3s flatten can only queue for Monday's open.

## Edge hunt (panel v3b) — 2026-11-27 amc + 2026-11-30 bmo — STARTED
- Logged at 2026-11-27 18:14 UTC
- Fired 18:07 UTC (13:10 ET slot); session already shut (Thanksgiving half-day, close 13:00 ET). Own universe: 4 of 28 rows with a session (CHA HMR BOSC PWRL, all 11-30 bmo), baselines sealed. Thin day: session_resolve.py on 19 time-not-supplied rows killed 4 by EDGAR, carried 15 (0 announced); sweep settles date/session, baselines for its confirmations sealed before any searcher. Plan: 1 sweep, up to 20 unpriced-searcher-v3b (max 6 per turn), 4 v3b judges. No orders, no shadow ledger.

## Edge hunt (panel v3b) — sweep
- Logged at 2026-11-27 18:20 UTC
- Sweep: 4 confirmed, all 2026-11-30 bmo (HMR 71, CHA 63, BOSC 54, NAT 42; NAT's 11-27 calendar date wrong, baseline sealed 11-30 bmo after the sweep, before any searcher). 15 phantom incl. PWRL (sealed, no date: N-2 fund, not hunted). Nothing confirmed in today's amc. Baseline histories for HMR/CHA/BOSC flagged untrustworthy (6-K rows). 4 searchers, one wave, nothing shed.
