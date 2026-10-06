# Run log — 2026-10-06

## Stage AU — Australia researcher — DONE (empty session)
- Logged at 2026-10-05 06:42 UTC
- Event date 2026-10-06 (Tue). market_open true (basis: weekday, not an ASX holiday — forward date beyond the index tape). 1574 vendor rows scanned, 0 scheduled on 2026-10-06, 0 eligible, 0 hunted, 0 session_unresolved. Case: a genuinely thin Australian session outside the Feb/Aug reporting seasons, not a shut exchange and not a tape fault. No baselines sealed, no hunters spawned, no orders (stage places none). Universe: research/2026/10/2026-10-06/australia/universe.json.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-05 13:42 UTC
- Fired 2026-10-05 ~13:39 UTC (intraday, European markets open). Sealing for event date 2026-10-06 (Tue), the next European session. Plan: eu_universe (10 markets, cap 20, $100k floor) -> seal baselines -> one bilingual hunter per name in waves of 5 -> edge_score -> note. No orders. Checkout: local branch from origin/main 93d2dd80 (local main clone had diverged after a forced update of origin/main; left untouched), publishing HEAD:main.

## Stage EU — Europe researcher — DONE (empty session)
- Logged at 2026-10-05 13:42 UTC
- Event date 2026-10-06 (Tue), sealed from a 13:39 UTC fire on 2026-10-05 while the European markets were open. No market_closed flag on any of the ten markets.
- Vendor calendar healthy: 4,586 rows scanned across uk/de/fr/se/dk/no/fi/it/es/pl (98 off-primary SE rows filtered). 3 scheduled on 2026-10-06, 0 eligible above the $100k floor, 0 hunted: IHC (uk, $4.1k/day), ALDNE (fr, $1.0k/day), GOP (pl, $3.7k/day). All three session_unresolved (defaulted bmo).
- Case: a genuinely thin early-October session (Nordic Q3 season starts mid-month), not a shut exchange and not a feed fault. No baselines sealed, no hunters spawned, no edge_score run, no note. Floor NOT lowered. Stage places no orders.
- Universe: research/2026/10/2026-10-06/europe/universe.json. Published to main with EARNINGS_DATA_BRANCH=main pinned.

## Stage EU — vendor calendar recall check (operator query)
- Logged at 2026-10-05 15:46 UTC
- Operator reported many UK names on investing.com's calendar for 2026-10-05 that stage EU did not see. Confirmed against Investegate (RNS): 2026-10-05 carried ENSI final results, RMV, SRE and QTX trading updates (>= $100k/day); the 10-02 seal for 10-05 had 0 UK vendor rows.
- Over 2026-09-22 → 10-05 the TradingView scanner MISSED 88 of 135 UK equity results/trading-update RNS above ~$100k/day (rough GBX→USD cut on current 10d volume). Trading updates are never in the vendor feed; but real interims/finals were missed too (e.g. FXPO, AEX, ROCK, ENET, CVSG, MDH, ATOM), and several vendor 'phantoms' reported days later (BILN, HUW, KEFI, RKH), i.e. the vendor dates are estimates. The 2.2% phantom rate in SUBMARKET.md measured PRECISION; RECALL was never measured and is ~35%.
- investing.com: 403 from Cloudflare (not the agent proxy); TLS-impersonating client also 403; a headless-browser load was refused by the session's permission classifier. Not pursued further. Nothing about the 10-06 universe changed.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-06 01:05 UTC
- 01:06 UTC fire: universe for 2026-10-06, seal baselines, one unpriced-hunter-jp per name in waves of 5, score with edge_score.py. No orders.
