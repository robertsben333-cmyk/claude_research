# Run log — 2026-09-11

## Stage 0 — universe (06:40 UTC / 08:40 CEST)
- Logged at 2026-09-11 06:41 UTC
- Window: After the US close on Friday 11 September 2026 through before the US open on Monday 14 September 2026
- Source: nasdaq
- Universe: 4 total (0 AMC, 4 BMO); 1 eligible after qualification
- Excluded: 3 (below_market_cap_floor: CODA, RFIL, HAIN)
- Notes: Weekend roll — Friday close side empty (0 AMC), before-open side rolled correctly to Monday 2026-09-14. CSHR ($0.70B) is the only name above the $500M floor; verified via WebSearch as Nasdaq-listed common (de-SPAC'd 2026-04-01, not a SPAC remnant), with an active listed-options market since 2026-04-16, and BMO timing confirmed by CoinShares' own IR release.

## Stage 1 — triage (06:52 UTC / 08:52 CEST)
- Logged at 2026-09-11 06:42 UTC
- Mode: skipped (universe <= threshold)
- Funnel: 4 universe -> 1 eligible -> 1 cleared floors -> 1 shortlisted
- Scouts: 0 subagents (skip mode)
- Session mix: 0 AMC / 1 BMO
- Notable drops: CODA (below_market_cap_floor), RFIL (below_market_cap_floor), HAIN (below_market_cap_floor) -- all dropped at stage 0, none reached triage

## Close AMC — 2026-09-11
- Logged at 2026-09-11 11:49 UTC
- Config change (operator instruction): orders.exit_mode uniform -> auction_split, flatten_before_entry true -> false in config/pipeline.yaml. Replication risk explicitly acknowledged and accepted by the operator; requirement is amc legs always exit at the opening auction.
- mode --require auction_split: PASS (exit 0) after the config change.
- close --scan 'research/*/*/*/edge' --submit: HOFT (bmo) not sent -- cls unavailable, market closed at 07:49:33 ET (correct, will go in at stage E's own run today). FEIM (amc) SENT opg 5cad5a24-b3f4-401e-8c68-f71b3ab6ca0a. ORCL (amc) SENT opg 58792a00-ceef-4810-8b21-c2ac9dc9c79a. RH (amc) SENT opg d53747ca-36bb-416b-9ea2-5f1323bc3ea8.
- status: all 3 opg exits queued (new, unfilled -- auction has not run yet). No refusals other than the expected HOFT/cls deferral.

## Edge hunt — 2026-09-11 amc + 2026-09-14 bmo — STARTED
- Logged at 2026-09-11 17:07 UTC
- Window resolves 4 names, ALL 2026-09-14 bmo (Monday); zero amc tonight. Universe: CSHR, CODA, RFIL, HAIN. Baselines sealed and committed before any agent launch. Plan: 1 sweep + 1 hunter per confirmed name (<= 4 hunters), well inside the cap of 20.
- Clock: session started 17:05 UTC. The Routine's own prompt still says it fires at 14:04 UTC / 10:04 ET; trig_01CvGQJWoKeNLXWCxiffM3ED reads '4 17 * * 1-5' and it fired at 17:04 UTC = 13:04 ET. Entry deadline (US close, 20:00 UTC) is 2h55m from start, not the 6h the prompt assumes.
- Step 0b (execution.enabled: true, exit_mode: auction_split, flatten_before_entry: false): closed 2026-09-10's book. The 'Close AMC' Routine had already sent the three amc legs into this morning's opening auction at 11:49 UTC — ORCL covered 12 @ 165.43 (short from 155.78, -6.19%); FEIM and RH opg orders EXPIRED UNFILLED and were caught by plain market orders at 13:34 UTC: FEIM covered 31 @ 81.90 (short from 63.42, -29.14%), RH sold 14 @ 137.51 (long from 138.98, -1.06%). This session sent the remaining bmo leg, HOFT 161 sh, into TODAY's closing auction (cls, order ca3f9aca), unrealised -1.18% at submission. Realised on the three closed legs: -709.23 USD. Account equity 9,266.75 from 10,000 at yesterday's entry.
- First-day operational finding on auction_split: two of three opg orders expired unfilled in the paper opening auction. The mode works but is not self-sufficient — the fallback market order is what actually closed FEIM and RH.

## Edge hunt — 2026-09-11 — SWEEP
- Logged at 2026-09-11 17:11 UTC
- 4 of 4 confirmed, 0 phantom, 0 session-unsettled. Every date came off a company press release or IR page, every session off a stated release/call time. hunt_priority: HAIN 82, CSHR 74, RFIL 63, CODA 52.
- RFIL is a session regime change caught by the sweep rather than inherited: all seven prior prints were amc by 8-K item 2.02 acceptance time, this one is company-stated bmo.
- CSHR baseline_history_trustworthy=false — its three recorded 'moves' are corporate-action 6-Ks, one verified as an EGM notice, so the 4.46% expected move and 2.23% deadband are meaningless. CODA's n=0 is genuine absence (it does not file item 2.02 8-Ks at all), so the matcher imported nothing wrong but there is still no base rate.
- Three of four have no usable option chain; RFIL's has a 67%-of-mid ATM spread. The day has essentially no option-implied anchor.

## Edge hunt — 2026-09-11 — HUNTS AND RANKING
- Logged at 2026-09-11 17:23 UTC
- 4 hunters, one per confirmed name, 17 findings total. Subagent spend: 1 sweep + 4 hunters = 5 of the cap of 20. No names shed; the universe was smaller than the budget.
- Ranking on impact_sum (edge-scores.json ranking_key = impact_sum): RFIL +2.50, CODA -4.10, CSHR -5.50, HAIN -5.50. CSHR and HAIN TIE, so the day is three distinct positions over four names, not a strict order. 3 of 4 clear the conviction floor of 3.0; RFIL at 2.50 does not.
- THE CONTROL REPRODUCED THE HUNT. -run_up_20d_pct ranks RFIL, CODA, HAIN, CSHR; the hunt ranks RFIL, CODA, CSHR=HAIN. Spearman between them is +0.95. Four names cannot support a correlation statistic, but this day bought essentially nothing the free control did not already give away.
- Sign balance 3 negative / 1 positive. Option chains: 1 of 4 live (RFIL), and its ATM spread is 67% of mid, so on a strict reading zero of four have a usable priced-move anchor. CSHR's reaction history is unusable (baseline_history_trustworthy false) and CODA's n=0 is genuine absence — both hunters were told so explicitly.
- No adversary pass and no second hunter, so nothing checked these 17 findings for being factually wrong.
