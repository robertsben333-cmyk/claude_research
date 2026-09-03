# Run log — 2026-09-03

## Stage 0 — universe — 07:22 CET
- Logged at 2026-09-03 05:22 UTC
- Window: After the US close on Thursday 03 September 2026 through before the US open on Friday 04 September 2026
- Source: nasdaq (after-close + before-open)
- Universe: 21 total (20 AMC, 1 BMO); 13 eligible after qualification
- Excluded: 8, all below_market_cap_floor ($500M floor) — none excluded for options/timing
- Notes: all 13 above-floor names hand-verified for a real listed options market and single-source-confirmed BMO/AMC session (Nasdaq option-chain listings + company IR press releases for IOT and OXM, cross-checked against TipRanks/StockTitan/Investing.com). No conflicting timing found. Stage 1 (triage) will trigger: 13 eligible > skip_if_universe_at_or_below (10).

## Stage 1 — triage — STARTED
- Logged at 2026-09-03 06:42 UTC
- 13 eligible names, above skip threshold (10); spawning 1 earnings-triage-scout batch (all 13 fit in one batch of 15) to score change_expectation/ai_edge before cutting to shortlist_size=6.

## Stage 1 — triage (06:44 UTC)
- Logged at 2026-09-03 06:45 UTC
- Mode: scouted
- Funnel: 21 universe -> 13 eligible -> 11 cleared timing/tradeability -> 11 cleared floors -> 6 shortlisted
- Scouts: 1 subagent (sonnet/medium), all 13 eligible tickers in one batch
- Session mix: 6 AMC / 0 BMO (all 13 eligible names in today's universe report AMC; no BMO name cleared the market-cap floor)
- Notable drops: MAMA (tradeable: false, illiquid options), SWBI (timing_confirmed: false, one source says 09-04 not 09-03 -- would have ranked top-3 on score, worth a manual re-check before stage 2), DOCU (ranked 8th, already ran +17% into print), ASAN (ranked 7th, closest miss)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-03 08:26 UTC
- Shortlist: 6 names (PATH, PL, AMBA, LULU, ZS, IOT); this batch: PATH, PL, AMBA (positions 1-3 of 6, cap unchanged)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (PATH+PL, then AMBA), publish after each dossier and after each wave

## Stage 2 — deep dive, batch 1 — wave 1 done
- Logged at 2026-09-03 08:47 UTC
- Researched: PATH, PL
- Both event_confirmed; PATH triage rationale corrected (magnitude framing inverted, real catalyst is 09-22 Investor Day); PL triage rationale corrected (not a guidance-validation print, it's about ATM dilution/backlog)

## Stage 2 — deep dive, batch 1 — FINISHED
- Logged at 2026-09-03 09:05 UTC
- Researched: PATH, PL, AMBA
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (PATH+PL, then AMBA), published individually and after each wave
- Median evidence completeness: 84/100 (PATH 84, PL 87, AMBA 82)
- Notable: PATH and PL triage rationales both corrected on further evidence (see wave-1 log entry); AMBA's implied move (12.93%) reads as cheap vs its own 8Q realised-move mean (15.08%), opposite of triage's framing
- Panel-eligible after this batch: n/a — final ranking happens after batch 2

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-03 10:25 UTC
- Shortlist: 6 names (PATH, PL, AMBA, LULU, ZS, IOT); this batch: LULU, ZS, IOT (positions 4-6 of 6, cap unchanged)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (LULU+ZS, then IOT), publish after each dossier and after each wave

## Stage 2 — deep dive, batch 2 — wave 1 done
- Logged at 2026-09-03 10:40 UTC
- Researched: LULU, ZS
- Both event_confirmed; LULU evidence completeness 84 (no IV rank/skew found); ZS evidence completeness 80 (implied move figure six sessions stale, no IV rank found)

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-03 10:59 UTC
- Researched: LULU, ZS, IOT
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (LULU+ZS, then IOT), published individually and after each wave
- Median evidence completeness: 84/100 (LULU 84, ZS 80, IOT 84)
- Panel-eligible after this batch: PATH, PL, LULU, AMBA, IOT, ZS (all 6, rank order) -- panel.names=2 in config so stage 3 takes PATH and PL

## Edge hunt — 2026-09-03 amc + 2026-09-04 bmo — STARTED
- Logged at 2026-09-03 14:10 UTC
- Stage E. Universe: 21 of 68 calendar rows resolved to today's amc (20) plus next-day bmo (1: KNOP). No --include-unknown. Baselines sealed at 14:08 UTC for all 21 — every one returned event_plausibility ok, and 12 of 21 carry a live front-expiry option chain (ZS 13.15%, PL 18.23%, ASAN 18.20%, AMBA 14.44%, NX 14.23%, PATH 13.70%, SWBI 13.61%, GWRE 12.96%, IOT 11.27%, MAMA 11.55%, DOCU 10.62%, LULU 9.42% implied). The 16:04 Amsterdam firing did its job: ZS ATM spread is 9% of mid against 41% on the first run's weekend marks. Budget plan at the edge_hunt cap of 20: 1 sweep + 10 hunters (8 names, double-hunted top 2) + 8 adversaries = 19. 21 names does not fit, so the shed is planned now, not discovered later: shed per budget.edge_degrade_order — unconfirmed names first, then lowest hunt_priority — while deliberately keeping names with a live chain, so 'what the market priced' is measured rather than inferred from a run-up. Shed names sit in the table as rankable:false with a stated reason.
