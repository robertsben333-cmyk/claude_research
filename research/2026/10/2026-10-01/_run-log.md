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
