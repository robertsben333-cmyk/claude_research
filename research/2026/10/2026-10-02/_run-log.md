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
