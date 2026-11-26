# Run log — 2026-11-26

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-25 14:38 UTC
- Fired 14:37 UTC 2026-11-25 (15:37 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-26 (Thu). Plan: universe -> baselines -> hunters in waves of 5 -> score -> 4-model panel -> note -> IBKR handoff. Local main had diverged from a rewritten origin/main (no merge base); working on a fresh branch at origin/main 2250fb921 and publishing to main.

## Stage EU — universe and baselines
- Logged at 2026-11-25 14:42 UTC
- 49 scheduled, 20 eligible (>= $100k), all 20 hunted (at the cap, no draw needed): uk 10, pl 6, no 2, se 1, dk 1. Concentration: UK 50%, 5 markets. 20 baselines sealed (intraday spots, ~14:45 UTC). Provenance stamped.
- IBKR mode: auth tws, executor server trades; cloud has no broker env (expected).
- Hunters: first 8 launched (concurrency limit 8): ACP CIG DIA ENT MDG VOX (pl) DFENS HUNT (no). Queued: PARKEN SANION CBOX CMCX FSG HFD IGP LTHM MAB PCIP SAFE SREI.

## Stage EU — hunts banked (1)
- Logged at 2026-11-25 14:47 UTC
- Back: HUNT (phantom: Q3 out 11-20, event_confirmed false), DFENS, ACP (hunter settles amc), CIG, DIA (amc), ENT (amc), VOX (date moved to 11-25 after close: window-equivalent bmo), MDG (amc likely), CBOX (released 11-25 07:00, a day before the vendor date; event_confirmed false). Running: PARKEN SANION CMCX FSG HFD IGP LTHM MAB. Queued: PCIP SAFE SREI.

## Stage EU — hunts
- Logged at 2026-11-25 14:54 UTC
- 20/20 hunted. 4 not ranked (no event in window): CBOX, IGP, PCIP (results released 24-25 Nov; 26 Nov is only an Investor Meet presentation), HUNT (Q3 out 20 Nov). Hunters settle ACP, DIA, ENT, MDG as amc (window close(11-26)->close(11-27)); VOX moved to 11-25 after close (window unchanged). 16 ranked, none above the 2.8 floor; top CMCX +1.20, bottom FSG -1.40.

## Stage EU — panel STARTED
- Logged at 2026-11-25 14:54 UTC
- 16 packs, four judges

## Stage EU — panel
- Logged at 2026-11-25 14:59 UTC
- 4/4 judges, no fallback. Selected (3 of 4 in own top 20%): CMCX 98 long (4/4), FSG 80 short (3/4). DIA 74 short (2/4).

## Stage EU — IBKR handoff
- Logged at 2026-11-25 14:59 UTC
- handoff written (before the note): 3 names, offline plan at sealed spots on EUR 10,000: BUY CMCX 50.0%, SELL FSG 29.2%, SELL DIA 20.8%. Not taken (< 70): ACP 68.0, DFENS 67.2, VOX 60.1. Caveat for the operator: DIA's hunter settles its release as amc on 26 Nov (after the Warsaw close), so a position held only to the 15:35 Amsterdam flatten on 26 Nov exits before the print.

## Stage EU — done
- Logged at 2026-11-25 15:02 UTC
- Note published. Handoff went out before the note (15:01 UTC). Pushed to main (EARNINGS_DATA_BRANCH=main). Calendar defect for a dev session: CBOX, IGP and PCIP were dated on their Investor Meet Company presentation day, not their results day; the baselines' own RNS history already held the release.

## Stage E-P amc exit — 2026-11-26
- Logged at 2026-11-26 14:08 UTC
- Fired 14:07 UTC (09:07 ET), Thanksgiving: US market closed. Guards passed on both accounts (live, paper: amc -> open as day). verify --fix: live 9 exit legs all ok, paper 11 exit legs all ok, nothing UNFILLED, no rescue sent. close --today-only: live 9 runs, paper 28 runs, no leg due today, nothing sent, nothing refused.

## Edge hunt (panel) — 2026-11-26 window — STARTED
- Logged at 2026-11-26 18:09 UTC
- Fired 18:07 UTC (13:07 ET), Thanksgiving: NYSE/Nasdaq closed today, Fri 11-27 is a half day (close 13:00 ET). Window 11-26 amc + 11-27 bmo: 1 of 26 calendar rows has a session (XYF 11-27 bmo). Thin-day check with --include-unknown + session_resolve: 25 unresolved rows, 3 killed by EDGAR, 22 carried, 0 confirmed by press release, so not hunted (holiday amc rows). Plan: baseline sealed for XYF, 1 sweep, up to 1 searcher, 4 judges. Step 6b buy will be refused (market closed); step 3s flatten would only queue for Friday's open.

## Edge hunt (panel v3b) — 2026-11-26 window — STARTED
- Logged at 2026-11-26 18:13 UTC
- Fired 18:10 UTC (13:10 ET), Thanksgiving: market closed, Fri 11-27 half day. Own universe: 1 of 26 rows with a session (XYF 11-27 bmo). Thin-day check (--include-unknown + session_resolve): 25 unresolved, 4 killed by EDGAR, 21 carried, 0 confirmed by press release, not hunted. Baseline sealed for XYF (spot 5.25, no implied move, hist_n 8). Plan: 1 sweep, 1 unpriced-searcher-v3b, 4 panel-judge-v3b judges. No orders.
## Edge hunt (panel) — sweep, search, step 3s
- Logged at 2026-11-26 18:19 UTC
- Sweep: 1 of 1 confirmed (XYF 11-27 bmo, company release). 1 searcher (unpriced-searcher, Opus 5.5), search_complete true, 0 unfinished. impact_sum -0.40 (pre-lessons -0.50), V2 -0.52. Main finding: going-private bid at US$6.03/ADS (11-06) from the ~93% holder; stock trades the deal spread.
- Step 3s at ~18:20 UTC with the market CLOSED (Thanksgiving): live held FINV -484 (-2.86%), paper held FINV -3360 (-2.97%). Both close-alls accepted and queued; FINV still held on both, cover executes at Friday 11-27 open. Defect for a dev session: flatten without --submit printed '0 position(s) held' on both accounts minutes earlier, because the guard returns before positions are read, so a dry run cannot be used to see what is held.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-26 18:20 UTC
- 1 packs, four judges

## Edge hunt (panel) — panel
- Logged at 2026-11-26 18:23 UTC
- 4/4 judges on pinned models, no fallback. XYF panel_pct 39 short (opus5 49S, opus55 11S, sonnet55 56S, fable51 38S), not selected. 0 selected. Note published.

## Edge hunt (panel) — step 6b
- Logged at 2026-11-26 18:24 UTC
- Plan live and paper: no name at panel_pct >= 80 or 70-79 (XYF 38.6), nothing to trade. open refused on both accounts anyway: market closed (Thanksgiving). Nothing sent. FINV cover still queued on both accounts for Friday's open (live held $1,176, paper $8,165 short). Note for the operator: Friday 11-27 closes 13:00 ET, before E-P's 13:06 fire, so Friday's step 6b will also find the market closed.

## Edge hunt (panel v3b) — panel STARTED
- Logged at 2026-11-26 18:22 UTC
- Sweep: 1 confirmed (XYF 11-27 bmo, company release), 0 phantom. 1 unpriced-searcher-v3b (native agent), search_complete true, v3b fields present (expectations, next_guide, evidence_type on 10/10 items). impact_sum -0.90, V2 -1.70 (written before the print). 1 pack, four judges.
## Edge hunt (panel) — done
- Logged at 2026-11-26 18:24 UTC
- Duplicate event: the 11-25 E-P run already hunted XYF for this same 11-27 bmo print (its next trading day skipped Thanksgiving): 57.1 short then, 38.6 short now. Both are now in panel-history.json, and edge_resolve --pool would count one print twice. De-duplicate when pooling. panel-history.json was committed separately because publish.sh did not stage it.

## Edge hunt (panel v3b) — panel
- Logged at 2026-11-26 18:27 UTC
- 4/4 v3b judges on pinned models, no fallback. XYF panel_pct 41 short (own history; 38 on E-P scale; E-P's panel 38.6 short), not selected. 0 selected. 4 sizes appended to panel-history-v3b.json; E-P history untouched. No orders, no alpaca_trade.py call. Note published.

## Edge hunt (panel v3b) — done
- Logged at 2026-11-26 18:28 UTC
- Duplicate event, same as E-P: the 11-25 v3b run already hunted XYF for this 11-27 bmo print (panel_pct_signed +3.2 then, -41.0 now). Both are now in panel-history-v3b.json. De-duplicate when pooling and in v3b_compare.py.
