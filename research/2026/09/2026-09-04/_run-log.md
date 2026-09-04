# Run log — 2026-09-04

## Stage 0 — universe (07:19 CEST)
- Logged at 2026-09-04 05:18 UTC
- Window: After the US close on Friday 04 September 2026 through before the US open on Tuesday 08 September 2026 (Monday 07 Sep is Labor Day; roll to Tuesday handled by get_earnings.py)
- Source: nasdaq (after-close + before-open)
- Universe: 5 total (0 AMC, 5 BMO); 2 eligible after qualification
- Excluded: 3 (below_market_cap_floor: WDH $0.35B, CAN $0.24B, GMHS $0.05B)
- Eligible: ABM, UNFI — both NYSE-listed, real listed-options markets, BMO timing cross-checked via WebSearch against a second independent source (investing.com for ABM, company press release for UNFI)
- Notes: three-day trading gap ahead of the window (Labor Day) means the before-open side rolls all the way to Tuesday 08 Sep; nothing else odd.

## Stage 1 — triage (10:31 CEST, run by stage 2 session — stage 1 Routine had not published)
- Logged at 2026-09-04 08:29 UTC
- Mode: skipped (universe 2 <= threshold 10)
- Funnel: 5 universe -> 2 eligible -> 2 cleared floors -> 2 shortlisted
- Scouts: 0 (screen skipped)
- Session mix: 0 AMC / 2 BMO
- Notable drops: none (stage 0 already excluded WDH, CAN, GMHS below market-cap floor)
- Note: 01-shortlist.json was absent when this session started (~2h after stage 1's scheduled 08:38 CEST fire); ran earnings-triage inline per earnings-deep-dive step 1's guidance rather than block stage 2

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-04 08:29 UTC
- Shortlist: 2 names (ABM, UNFI); this batch: ABM
- Already on disk, skipping: none
- Plan: 1 wave of 1 opus/high researcher (ABM), publish after the wave

## Stage 2 — deep dive, batch 1 — FINISHED (08:50 UTC)
- Logged at 2026-09-04 08:51 UTC
- Researched: ABM
- Skipped (already done): none
- Failed: none
- Subagents: 1 opus/high, in 1 wave of 1
- Median evidence completeness: 80/100
- Panel-eligible after this batch: N/A (ranking runs after the final batch)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-04 10:26 UTC
- Shortlist: 2 names (ABM, UNFI); this batch: UNFI
- Already on disk, skipping: ABM (batch 1 completed)
- Plan: 1 wave of 1 opus/high researcher (UNFI), publish after the wave

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-04 10:43 UTC
- Researched: UNFI
- Skipped (already done): ABM (batch 1)
- Failed: none
- Subagents: 1 opus/high, in 1 wave of 1
- Median evidence completeness: 80/100
- Ranking: 02-ranking.json written from both dossiers (ABM, UNFI); shortlist change_expectation was null for both (triage_mode skipped_small_universe), so the panel_priority formula's 0.20 change_expectation weight was dropped and the remaining two renormalized -- documented in the ranking file's note
- Panel-eligible after this batch: ABM (45.13), UNFI (39.5) -- both eligible, both go to panel (panel.names=2, only 2 dossiers exist)

## Stage E — edge hunt — 2026-09-04 amc + 2026-09-08 bmo — STARTED
- Logged at 2026-09-04 14:11 UTC
- Window resolved to 5 confirmed names, all 2026-09-08 bmo: ABM, UNFI, WDH, CAN, GMHS. Today's Friday amc contributed nothing — all 12 calendar rows were time-not-supplied and were dropped per the phantom-rate rule (--include-unknown withheld).
- BUG FIXED FIRST: edge_universe.py --window skipped weekends but not NYSE holidays, so it resolved the Friday before Labor Day to Monday 2026-09-07 (market closed) and returned 0 of 19 rows. It now uses next_trading_day() from get_earnings.py, which already knew the calendar. Window is now 09-04 amc + 09-08 bmo.
- Baselines sealed and committed before any agent launches. All 5 fits_cadence, all with 7-8 exact 8-K item 2.02 reaction histories, no cadence_implausible, no suspect verdicts — no amend pass needed.
- Only 1 of 5 has a usable option chain (UNFI, event-implied 12.02%, but ATM spread 39% of mid = indicative only). ABM's chain exists but spread is 188% of mid = unusable. WDH/CAN/GMHS no chain. So 4 of 5 baselines infer what is priced from a 20d run-up rather than measuring it.
- Plan: 1 edge-sweep over all 5, then 7 unpriced-hunters (2 each on top 2 by hunt_priority, 1 on the other 3), then 5 priced-in-adversaries, 1 per ticker judging all findings on both sides. Total 13 subagents against the edge_hunt cap of 20 — no shed needed.

## Stage E — sweep + baseline amend — 2026-09-04
- Logged at 2026-09-04 14:16 UTC
- CORRECTION to the STARTED entry above: it claimed all 5 baselines were fits_cadence. They were not. CAN and GMHS carry verdict 'unknown' with cadence_implausible true; I read the console 'status: ok' column instead of event_plausibility.verdict. The sweep caught this.
- Sweep: 5 of 5 confirmed, ZERO phantom calendar rows, and every one of the five was pre-announced by the company's own press release WITH the hour, so session_unsettled is 0 too. All five are 2026-09-08 bmo. Second consecutive run with a zero phantom rate under the no---include-unknown rule.
- hunt_priority: UNFI 78, CAN 66, ABM 61, WDH 47, GMHS 33.
- Baseline history trustworthy on only 2 of 5. ABM and UNFI are domestic filers on exact 8-K item 2.02 acceptance times. CAN (13-day median gap, monthly bitcoin-production 6-Ks), GMHS (55-day median, 3 of 8 rows outside any reporting quarter, one tagged intraday) and WDH (three 6-Ks inside one quarter) are all the 6-K text-matcher defect.
- AMEND PASS, applied before any hunter launched: exactly ONE amendment, WDH fits_cadence -> unknown. A pass whose only entry is a downgrade. CAN and GMHS were deliberately NOT upgraded despite company-confirmed dates, per the DOO/PSNY/VBNK/ZGN precedent: the event is real but the history does not characterise it, and upgrading would forgive the history defect and hand each a 1.0 event multiplier it has not earned. Net: one name loses a multiplier, none gains one.
- Option-chain reality: 1 of 5 measured, 4 of 5 inferred. Only UNFI has a usable chain (event-implied 12.02%, ATM spread 39% of mid = indicative only). ABM's chain exists but the ATM spread is 188% of mid on 93 total OI. WDH and GMHS have no options market at all; CAN's legs are not two-sided. The 16:04 Amsterdam firing time did tighten UNFI's spread from the 41% seen on stale weekend marks, but only to 39% — the binding constraint is 1,765 contracts of front-expiry OI, not the hour.
