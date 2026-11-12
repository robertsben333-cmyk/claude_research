# Run log — 2026-11-12

## Close AMC — stage E pre-market exit
- Logged at 2026-11-12 11:19 UTC
- Fired 11:12 UTC (06:12 ET). Guard `mode --require-exit-tif opg` exit 0 (amc_open; amc -> open as market DAY, auction_orders false). verify over 12 edge runs / 14 exit legs: none UNFILLED, nothing held. close --submit: 0 legs due today, NO orders sent, no refusals (stage E's Routine is stopped, so no new edge book exists; stage E-P's amc legs are not in this scan). Post-wait verify: all 14 ok.

## Stage E-P amc exit — 2026-11-12
- Logged at 2026-11-12 14:08 UTC
- 14:08 UTC (09:08 ET). Guard mode --require-exit-tif opg: exit 0 (amc -> open as market DAY, matched on placement). verify --fix --submit over 18 edge-panel runs: 0 exit legs to check, nothing UNFILLED, no rescue. close --today-only --submit: 2 amc legs of the 2026-11-11 book SENT as market DAY orders queued for the open: CURI (order a02c6084-d77f-4a12-b951-a1ca28612d15) and CTVA buy-to-cover 839 sh (order cfbc3a00-ad2e-47fa-ab48-e4c8e7fd56cc), both pending_new. No refusals printed; no bmo legs due today.

## Stage M — morning exit review — STARTED
- Logged at 2026-11-12 14:15 UTC
- source research/2026/11/2026-11-11/edge-panel, 09:15 ET, 3 picks (CURI, CAE, CTVA), analysts launched

## Stage M — previous morning scored
- Logged at 2026-11-12 14:15 UTC
- pool: 109 names over 15 days; review +2.40% (t 2.01) vs static +2.42% (t 2.17); review_minus_static −0.02pp (t −0.04); Brier review−prior p_open_lags −0.016 (t −1.32), p_fade −0.007 (t −0.76)

## Stage M — morning exit review — done
- Logged at 2026-11-12 14:17 UTC
- 3 names: CURI exit_1000, CTVA exit_open, CAE exit_open; compiled 09:17 ET; all 3 analysts ran (morning-reaction-analyst)

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-12 14:37 UTC
- Fired 14:36 UTC (15:36 Amsterdam, markets open). Sealing for event date 2026-11-13 (Fri), RUN research/2026/11/2026-11-13/europe. Plan: universe (cap 20), seal, provenance, one hunter per name (up to 8 concurrent), edge_score, four-model panel, note, IBKR handoff. Local main was a stale shallow checkout diverged from a force-updated origin; main re-pointed at origin/main 95ec29fb0.
