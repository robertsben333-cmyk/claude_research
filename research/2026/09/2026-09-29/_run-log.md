# Run log — 2026-09-29

## Stage AU — Australia researcher — empty session
- Logged at 2026-09-28 06:41 UTC
- Fired 2026-09-28 06:40 UTC (16:40 Sydney), sealing for the next ASX session 2026-09-29.
- Funnel: 1578 vendor calendar rows / 0 scheduled / 0 eligible / 0 hunted. market_open=true (weekday, not an ASX holiday; calendar read cleanly).
- Case: market open with zero names — a genuinely thin Australian session outside the Feb/Aug reporting seasons. No baselines sealed, no hunters spawned, nothing to rank. No orders (research only).
- Housekeeping: local checkout's main had diverged from a force-updated origin/main; reset to origin/main (stale local tip kept as branch backup/local-main-stale-20260928, not pushed).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-28 13:39 UTC
- Fired 2026-09-28 13:39 UTC on main, sealing for event date 2026-09-29 (Tue). Markets intraday; sealed spot is not a close.
- Plan: eu_universe -> eu_priced_in -> one bilingual hunter per name in waves of 5 -> edge_score -> europe-note. No orders.

## Stage EU — universe and seal
- Logged at 2026-09-28 13:45 UTC
- 31 scheduled (uk 13, fr 7, pl 6, de 2, it 2, es 1; se/dk/no/fi 0), 10 eligible above $200k, 10 hunted, no draw (under cap 20). uk 5 (BAG CARD CBG MTEC MTL), de 2 (2GB HBH), fr 1 (GNFT), it 1 (SERI), es 1 (ADX). market_concentration: uk 0.50 over 5 markets.
- session_unresolved (defaulted bmo): 2GB ADX CBG GNFT MTL SERI.
- Registers: uk FCA 2026-09-25 read, de Bundesanzeiger read, it CONSOB read, fr AMF UNREADABLE today (no cache), es none by design. anchor_covered 2 of 10: CARD (2.48%), CBG (4.11%). history observed_rns for 5 UK, estimated_from_cadence for the other 5.

## Stage EU — wave 1 complete
- Logged at 2026-09-28 13:56 UTC
- 5 of 5 UK hunters returned: CARD -1.1 (guide restatement after weak May-Jul high street), CBG -0.3 (CET1 +0.3, dividend timetable -0.6), MTEC -0.7 (reiteration after +48% run), BAG 0 (H1 pre-released 4 Aug), MTL 0 (H1 pre-released; date UNCONFIRMED, AIM deadline 30 Sep so 29 or 30 Sep). All bmo 07:00 by issuer RNS pattern. Wave 2: 2GB HBH GNFT SERI launched, ADX now.

## Stage EU — Europe researcher — DONE
- Logged at 2026-09-28 14:08 UTC
- Event date 2026-09-29 (sealed Mon 09-28 intraday). 31 scheduled / 10 eligible / 10 hunted / 9 rankable / 0 above floor 3.0. 2GB +0.70, BAG 0, GNFT 0, HBH -0.10, ADX -0.25, SERI -0.25, CBG -0.30, MTEC -0.70, CARD -1.10; MTL not ranked (date unconfirmed, AIM deadline 30 Sep).
- GNFT and SERI are AMC per hunters (evening releases) though sealed bmo: read the amc window at resolve. AMF register unreadable today (GNFT no anchor). ADX hunter reports CNMV resultado-oir/resultado-ip listing pages returned 200 -- unverified in code. SERI hunter reports eu_pdftext.py garbled the issuer PDF. Note: research/2026/09/2026-09-29/europe/europe-note.md. Publishing with EARNINGS_DATA_BRANCH=main pinned.

## Stage EU — publish check
- Logged at 2026-09-28 14:08 UTC
- git log -1 origin/main after publish: de6ac0d4 'stage EU: Europe ranking for 2026-09-29' — the ranking is on main.

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-29 01:05 UTC
- Plan: jp_universe -> jp_priced_in seal -> one unpriced-hunter-jp per name in waves of 5 -> edge_score -> japan-note. No orders. Fired 01:04 UTC 2026-09-29 (10:04 JST).

## Stage J — universe + baselines sealed
- Logged at 2026-09-29 01:05 UTC
- 8 scheduled / 4 eligible / 4 hunted (2792 ハニーズ, 3050 DCM, 7921 TAKARA & CO, 8217 オークワ); method: all 4 eligible at or under cap 25, no draw. calendar_as_of 2026-09-03. Short register file 20260918 (11 days stale); all four absent from it (truncated zero). One wave of 4 hunters.

## Stage J — wave 1 complete
- Logged at 2026-09-29 01:14 UTC
- 4 of 4 hunters returned: 2792 -1.5 (Q1 月次 93.3% vs plan 99.1% -> OP progress ~20%), 3050 +0.5 (Q1 cushion > Q2 月次 shortfall), 7921 +1.0 (FY-end backlog +23%), 8217 0 (H1 pre-revised 09-25, no findings).

## Stage J — Japan researcher — DONE
- Logged at 2026-09-29 01:14 UTC
- 4 ranked, 0 above floor: 7921 +1.00, 3050 +0.50, 8217 0.00, 2792 -1.50. Register 20260918 (11 days stale). 8217 release time unconfirmed (last H1 at 13:00 JST, intraday). Note: japan/japan-note.md. No orders.

## Close AMC (stage X) — 2026-09-29 10:10 UTC
- Logged at 2026-09-29 10:16 UTC
- Guard mode --require-exit-tif opg: exit 0 (amc open as day). verify: 14 legs, all ok, none held, no UNFILLED. close --submit: no legs due today, nothing sent, no refusals. status: no open positions in scanned books.

## Edge hunt — 2026-09-29 amc + 2026-09-30 bmo — STARTED
- Logged at 2026-09-29 17:09 UTC
- Fired 17:05 UTC. Window: 6 of 33 calendar rows (CNXC amc 09-29; JBL, FDS, CAG, CALM, YRD bmo 09-30). session_resolve over the 21 time-not-supplied rows: 1 killed, 20 carried unresolved, 0 confirmed by press release — none added. Baselines sealed for all 6 (YRD has no option chain). Plan: 1 sweep + 6 hunters.
- STEP 0b NOT RUN: the session's permission classifier refused the broker call (alpaca_trade.py verify/close --submit) as a real-world transaction. No order was placed, cancelled or re-sent by this session. Any bmo leg due to exit today is still held unless sold elsewhere; step 7 (the entry) will be refused the same way. The operator must run the exit/entry by hand or grant the permission.
