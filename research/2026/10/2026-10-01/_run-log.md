# Run log — 2026-10-01

## Stage AU — Australia researcher — EMPTY UNIVERSE
- Logged at 2026-09-30 06:40 UTC
- Fired 06:40 UTC 2026-09-30, sealing for the next ASX session 2026-10-01 (Thu).
- Funnel: 1579 vendor scanner rows / 0 scheduled / 0 eligible / 0 hunted. selection.method: 'all 0 eligible names (at or under the cap)', seed au-2026-10-01, session_unresolved 0.
- Case: market_open true (basis: 'beyond the tape: a weekday that is not an ASX holiday') with zero names — a genuinely thin Australian session, outside the Feb/Aug reporting seasons. Not a shut exchange, not a tape fault.
- No baselines sealed, no hunters spawned, nothing scored. Universe file published: research/2026/10/2026-10-01/australia/universe.json.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-30 13:42 UTC
- Fired Wed 2026-09-30 13:38 UTC (15:38 Amsterdam, markets open) on main (fdce24c8); sealing for next European session Thu 2026-10-01. Plan: eu_universe -> eu_priced_in seal -> one market hunter per name in waves of 5 -> edge_score -> europe-note. No orders. Pushing to main (EARNINGS_DATA_BRANCH=main pinned). Note: origin/main had been force-pushed since the container clone (no common history); local main re-pointed at origin/main, old local kept as branch backup-local-main-preforce (not pushed).

## Stage EU — universe and seal
- Logged at 2026-09-30 13:43 UTC
- 6 scheduled (uk 3, fr 2, no 1) / 2 eligible above $200k / 2 hunted; selection.method: all 2 eligible (under cap 20), seed eu-2026-10-01 unused. by_market uk 1 (JHD James Halstead, $0.73m/day), no 1 (SNI Stolt-Nielsen, $1.09m/day). market_concentration: uk 0.50, 2 markets. No market_closed. Off-primary filtered: se 231, pl 326.
- Registers read: uk (09-29, 420 rows), no (09-29, 96 rows). anchor_covered 1 of 2 (JHD disclosed; SNI register read, no position = truncated zero). session_unresolved 0 of 2 (both bmo, vendor flag). history.basis observed_rns (JHD, 13) and observed_newsweb (SNI, 27) — both observed, no cadence estimates. es/pl 0, de 0. One wave of 2 hunters.

## Stage EU — JHD hunter returned
- Logged at 2026-09-30 13:45 UTC
- JHD event_confirmed false: FY26 results delayed from 1 Oct to Wed 14 Oct 2026 by RNS 28 Sep 07:00 (BDO needs more audit time) https://www.investegate.co.uk/announcement/rns/james-halstead--jhd/delay-in-publication-of-fy26-audited-results/9792824. Vendor calendar had not picked it up. UK archive can reach event_occurred: false at resolve. SNI hunter still running.

## Stage EU — Europe researcher — DONE
- Logged at 2026-09-30 13:51 UTC
- 2 hunted / 1 rankable / 0 above floor 3.0. SNI -1.00 (Q4 tanker-rate guidance line; abs 6.5, p_up 42). JHD not ranked: results delayed to 14 Oct (RNS 28 Sep), kill reachable automatically via UK archive at resolve.
- Note: research/2026/10/2026-10-01/europe/europe-note.md. No orders. Published to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-01 01:05 UTC
- Tokyo window after 15:00 JST 2026-10-01. Universe via jp_universe.py, seal baselines, one unpriced-hunter-jp per name in waves of 5, score with edge_score.py. No orders.

## Stage J — Japan researcher — universe sealed
- Logged at 2026-10-01 01:06 UTC
- 6 scheduled / 4 eligible / 4 hunted (all eligible, no draw). Dropped on turnover: 2493, 5942. 4 baselines sealed on short register 20260929; all four truncated zeros on the register, 信用倍率 resolved on all four. Also resolved the 2026-09-29 run: 4/4 usable, lean_vs_free_control_rho -0.4.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-01 01:16 UTC
- 4/4 hunted, 4/4 rankable, 0 above floor. Ranking: 7545 +1.6, 7447 -1.0, 8276 -1.6, 3549 -2.0, the exact reverse of -run_up_20d. 8276 may release intraday at 13:30 JST (prints 2024-10 to 2026-04 did), which would put part of the reaction outside the window. No orders: research only.

## Close AMC (stage E exit Routine) 10:10 UTC
- Logged at 2026-10-01 10:16 UTC
- Guard exit 0 (amc open as day). verify: 14 legs, none UNFILLED, 0 held. close --submit: no new exit legs due today (none sent), no refusals. Account reachable.
