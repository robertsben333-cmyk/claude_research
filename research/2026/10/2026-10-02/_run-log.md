# Run log — 2026-10-02

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-01 06:41 UTC
- Fired 06:41Z 2026-10-01; sealing for the next ASX session (2026-10-02). Plan: universe -> seal -> one unpriced-hunter-au per name in waves -> edge_score -> note. No orders.

## Stage AU — Australia researcher — EMPTY UNIVERSE
- Logged at 2026-10-01 06:41 UTC
- Case: market_open true with zero names (basis: 'beyond the tape: a weekday that is not an ASX holiday'). Vendor scan read 1577 rows, 0 scheduled for 2026-10-02 after the Sydney-date shift, 0 eligible, 0 hunted, 0 session_unresolved. Genuinely thin session outside the Feb/Aug reporting seasons.
- No baselines sealed, no hunters spawned, no scores. No orders (this stage never places any).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-01 13:38 UTC
- Fired Thu 2026-10-01 13:38 UTC (15:38 Amsterdam, markets open) on main (8f333bcd); sealing for next European session Fri 2026-10-02. Plan: eu_universe -> eu_priced_in seal -> one market hunter per name in waves of 5 -> edge_score -> europe-note. No orders. Pushing to main (EARNINGS_DATA_BRANCH=main pinned).

## Stage EU — universe and seal
- Logged at 2026-10-01 13:39 UTC
- 3 scheduled (uk 1, fr 1, pl 1) / 1 eligible above $200k / 1 hunted; selection.method: all 1 eligible (under cap 20), seed eu-2026-10-02 unused. by_market uk 1 (JDW J D Wetherspoon, $1.12m/day). market_concentration: uk 1.00, 1 market. Dropped below floor: ALBPK (fr, $8.8k/day), KER (pl, $41k/day). No market_closed. Off-primary filtered: se 231, pl 325.
- Register read: uk (2026-09-29, 420 rows). anchor_covered 1 of 1 (JDW disclosed 4.57%, change -0.01pp). session_unresolved 0 (bmo, vendor flag). history.basis observed_rns (n 8, median |move| 4.91%). es/pl 0, de 0. One wave of 1 hunter (unpriced-hunter-uk).

## Stage EU — Europe researcher — DONE
- Logged at 2026-10-01 13:46 UTC
- 1 hunted / 1 rankable / 0 above floor 3.0. JDW -0.91 (FY27 outlook line after +13.5% rally from July warning; abs 6.5, p_up 43; pre_lessons -0.88). Event confirmed by issuer's 22 Jul RNS.
- Note: research/2026/10/2026-10-02/europe/europe-note.md. No orders. Published to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-02 01:05 UTC
- Fired 01:05Z 2026-10-02 (10:05 JST) on main (4b54850). Plan: jp_universe -> jp_priced_in seal -> provenance stamp -> one unpriced-hunter-jp per name in waves of 5 -> edge_score -> japan-note. No orders.

## Stage J — universe and seal
- Logged at 2026-10-02 01:06 UTC
- 9 scheduled / 5 eligible (4 dropped below ¥15m turnover floor) / 5 hunted; selection.method: all 5 eligible names (at or under the cap 25), seed jp-2026-10-02 unused. market_closed null. Sheets kessan07_0904 (as_of 09-03), kessan08_0918 (as_of 09-17). Short register 20260929 read (598 codes); margin ratio resolved 4 of 5 (4394 None). baseline_quality direction 0.6 x4, 0.45 x1. One wave of 5 unpriced-hunter-jp.
