# Run log — 2026-11-13

## Close AMC (stage E amc exit) — 2026-11-13
- Logged at 2026-11-13 11:17 UTC
- Fired 11:11 UTC (06:11 ET). Guard `mode --require-exit-tif opg` exit 0 (amc_open; amc -> open as market DAY, auction_orders false). verify over 12 stage E runs / 14 exit legs: all ok, nothing UNFILLED, nothing still held. close --submit: no leg due today, NO orders sent, no refusals (stage E's Routine stopped 2026-10-19, so no new stage E legs exist; E-P's amc exits belong to E-PX). status: unchanged. Account reachable.

## Stage M — morning exit review — NOT RUN
- Logged at 2026-11-13 14:37 UTC
- Routine fired at 14:37 UTC (09:37 New York), 27 minutes after its scheduled 14:10 UTC and 7 minutes after the open; slot reports inside_hours false, so per the skill no review was made (an exit review after the open answers a question that has gone). Source run research/2026/11/2026-11-12/edge-panel exists. No orders placed.

## Stage E-P amc exit — 2026-11-13
- Logged at 2026-11-13 15:29 UTC
- Fired 15:27 UTC = 10:27 ET, about 1h22m after its 14:05 UTC schedule and AFTER the 09:30 open. Clone on main 5b77b86.
- LIVE: guard mode --account live --require-exit-tif opg exit 0 (amc -> open as day) but prints 'live credentials MISSING': the environment carries ALPACA_LIVE_API_KEY_ID and ALPACA_LIVE_SECRET_KEY, while alpaca_trade.py reads ALPACA_LIVE_API_SECRET_KEY. verify --account live refused (exit 1, credentials); close --account live: 'No run with an alpaca-orders.json to close' (no alpaca-orders-live.json exists; E-P's 11-12 live buy was refused for the same missing secret, so there is no live book to sell). Nothing sent on live. Not routed around (no env-var aliasing).
- PAPER: guard exit 0. verify --fix --submit over 19 runs: 2 exit legs, CURI amc ok 4303/4303, CTVA amc ok 839/839, nothing UNFILLED, no rescue. close --today-only dry run first (fire was in-session): only the three amc legs of 2026-11-12 due (HTFL S131, LFTO L349, STNE S735), no bmo legs. close --today-only --submit --no-verify: all three NOT SENT, 'no open position at Alpaca (HTTP 404)'. status: paper account flat, equity = cash $22,470.95, no positions, so the three were closed before 15:29 UTC by something outside this Routine (no record in this repo). No orders placed by this fire.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-13 15:33 UTC
- Fired 15:31 UTC (16:31 Amsterdam, about an hour before the European close; scheduled 14:35, fired ~56 min late). Sealing for event date 2026-11-16 (Mon), RUN research/2026/11/2026-11-16/europe. Plan: universe (cap 20), seal, provenance, one hunter per name, edge_score, four-model panel, note, IBKR handoff. Local main was a stale shallow checkout diverged from a force-updated origin; resetting it was refused in auto mode, so the run works on local branch eu-run-2026-11-13 at origin/main e4162afea and publishes HEAD:main.

## Stage EU — universe and seal
- Logged at 2026-11-13 15:36 UTC
- Event date 2026-11-16 (Mon). 19 scheduled, 9 eligible above $100k, all 9 hunted (at or under cap 20): uk 6, pl 2, es 1. Largest market uk at 67%. 9 baselines sealed ~15:40 UTC (intraday spots, not closes). session_unresolved: CBF LGEN MEGP SLR SRE. BYG sealed amc. Provenance stamped. IBKR mode: execution_eu.environment live; no IBKR env in this session (expected), handoff file only.
- Wave 1 (5): APN BYG LGEN MEGP N91. Wave 2 (4): SRE CBF GPW SLR.

## Stage EU — panel STARTED
- Logged at 2026-11-13 15:46 UTC
- 9 of 9 hunted; 8 ranked, SLR not ranked (hunter: no CNMV date notice, 9M likely at the 19 Nov CMD). No name above the 2.8 floor; top N91 +0.60, bottom APN -1.30. Hunters put CBF (17:16/17:57 history) and BYG (issuer RNS 'at the close') after the 16 Nov close (amc). 8 packs, four judges.

## Stage EU — IBKR handoff
- Logged at 2026-11-13 15:50 UTC
- Handoff written (no broker call): 1 name at panel_pct >= 70 with four judges — SELL MEGP (81.4, uk). Offline plan sized on a 10,000 EUR placeholder equity at the sealed spot; the executor sizes on the real account. Written ~15:50 UTC, later than usual because the Routine fired ~56 min late.

## Stage EU — ranking
- Logged at 2026-11-13 15:50 UTC
- 8 ranked, SLR not ranked (no CNMV date notice; 9M likely at the 19 Nov CMD). No name above the 2.8 floor; top N91 +0.60, bottom APN -1.30. Panel (4 of 4 members, no fallback) selects MEGP short (3 of 4, panel_pct 81). UK 67% of the day. CBF and BYG amc per hunters/issuer.
- Published to main via EARNINGS_DATA_BRANCH=main from local branch eu-run-2026-11-13 (local main stale and diverged; reset refused in auto mode).

## Edge hunt (panel) — 2026-11-13 window — STARTED
- Logged at 2026-11-13 18:16 UTC
- Fired 18:07 UTC = 13:07 New York (EST). Universe --window: 39 names (amc 11-13: ROLR, BBGI; bmo 11-16: 37). 39 baselines sealed into edge-panel/baselines before any agent. Plan: one edge-sweep, up to 20 unpriced-searchers by hunt_priority (amc first, max 8 per turn), step 3s flatten live then paper, edge_score, grounded V2, four blind judges, panel_score, note, step 6b buy live then paper.
