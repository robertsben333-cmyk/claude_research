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
