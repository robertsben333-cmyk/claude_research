# Stage E-P — edge hunt with a blind four-model panel, 2026-11-16 window

**This is stage E-P: Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel.** Stage E-P trades the book through `alpaca_trade.py` (step 6b, live then paper). The panel rule sets the book; nothing in this note sizes it.
**All four judges ran on their pinned models**: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each covered 20 of 20 ids, none was missing, and no fallback was used.
**One day is an anecdote.** The panel is judged only pooled over many days.

**Window:** amc 2026-11-16 plus bmo 2026-11-17.
- **Universe:** 70 names (43 amc, 27 bmo).
- **Sweep:** 34 company-confirmed, 7 phantoms (RSSS, WKHS, CEPL, SUPV, GLBS, SMWB, GFUZ), 29 unconfirmed.
- **Hunted:** 20 names by `hunt_priority` after the unconfirmed were shed: 17 amc and 3 bmo (OPRA, KLAR, ELTK).
- **Shed though confirmed (on priority):** MNSO, BRFH, AS, HUYA, ENR, TME, ESLT, WB, VIK, JD, DIS, OCSL, HD, SR.
- **Searchers:** all 20 finished (`hunt_status`: 0 unfinished); none was retried.
- **Baseline amended:** STEM, from `suspect` to `unknown`. The company itself moved Q3 to Nov 16, and the matcher had missed the 08-12 print.

## Panel table

How to read the table:
- `panel_pct` is the mean of the four judges' own percentiles, 0-100, with the direction in `side`. A `*` marks a judge that put the name in its own top 20%.
- **Selection rule:** `panel_pct` >= 80 with all four judges present.
- **Expected return:** gross, on the scorebord window, on the panel's side. There is one number per percentile, so it translates the percentile and is not a separate forecast. It is flat at about +0.3% below a percentile of 50.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_prec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | STEM | amc 11-16 | **yes** | 95 | short | 3 | 90S* | 97S* | 99S* | 94S* | 4 | -1.99 | -4.30 | +4.75% [+2.77, +6.50] | 0.72 | 1.0 | 0.95 |
| 2 | IMDX | amc 11-16 | **yes** | 89 | short | 6 | 80S* | 97S* | 87S* | 93S* | 4 | -1.57 | -4.50 | +3.98% [+1.88, +5.94] | 0.68 | 1.0 | 1.10 |
| 3 | NXB | amc 11-16 | **yes** | 85 | short | 6 | 88S* | 83S* | 77S | 93S* | 3 | -1.50 | -1.90 | +3.40% [+1.29, +5.41] | 0.65 | 1.0 | 1.17 |
| 4 | OMER | amc 11-16 | **yes** | 85 | long | 5 | 80L | 90L* | 90L* | 82L* | 3 | +1.43 | +2.80 | +3.40% [+1.29, +5.41] | 0.65 | 1.0 | 1.25 |
| 5 | TMS | amc 11-16 | **yes** | 82 | short | 7 | 90S* | 83S* | 72S | 85S* | 3 | -1.40 | -3.30 | +2.98% [+0.93, +4.95] | 0.62 | 1.0 | 1.00 |
| 6 | RCAT | amc 11-16 | **yes** | 82 | short | 16 | 58S | 97S* | 78S | 95S* | 2 | -1.58 | -0.50 | +2.90% [+0.87, +4.87] | 0.62 | 1.0 | 0.75 |
| 7 | KLAR | bmo 11-17 | **yes** | 81 | short | 9 | 88S* | 74S | 71S | 91S* | 2 | -1.31 | -1.30 | +2.76% [+0.75, +4.71] | 0.61 | 1.0 | 0.92 |
| 8 | POWL | amc 11-16 |  | 77 | short | 23 | 92S* | 88S* | 38S | 91S* | 3 | -1.54 | -0.60 | +2.26% [+0.48, +4.13] | 0.58 | 0.0 | 0.00 |
| 9 | XBP | amc 11-16 |  | 59 | short | 6 | 50S | 61S | 66S | 58S | 0 | -0.84 | -1.10 | +0.74% [-0.15, +2.21] | 0.56 | 0.0 | 0.00 |
| 10 | WRAP | amc 11-16 |  | 50 | short | 8 | 37S | 58S | 50S | 54S | 0 | -0.65 | -0.10 | +0.29% [-0.43, +1.43] | 0.56 | 0.0 | 0.00 |
| 11 | API | amc 11-16 |  | 46 | long | 6 | 39L | 48L | 55L | 41L | 0 | +0.57 | +1.30 | +0.29% [-0.47, +1.17] | 0.56 | 0.0 | 0.00 |
| 12 | INFQ | amc 11-16 |  | 46 | short | 34 | 86S* | 56S | 8L | 49S | 1 | -0.70 | +0.10 | +0.29% [-0.47, +1.16] | 0.56 | 0.0 | 0.00 |
| 13 | FTLF | amc 11-16 |  | 44 | short | 5 | 50S | 38S | 47S | 41S | 0 | -0.55 | -0.90 | +0.29% [-0.49, +1.07] | 0.56 | 0.0 | 0.00 |
| 14 | YALA | amc 11-16 |  | 42 | long | 6 | 39L | 46L | 50L | 36L | 0 | +0.54 | +1.00 | +0.29% [-0.50, +1.01] | 0.56 | 0.0 | 0.00 |
| 15 | GLAS | amc 11-16 |  | 42 | short | 49 | 46S | 73S | 87S* | 39L | 1 | -0.88 | -1.40 | +0.29% [-0.50, +0.99] | 0.56 | 0.0 | 0.00 |
| 16 | DUOT | amc 11-16 |  | 31 | long | 45 | 46S | 48L | 55L | 66L | 0 | +0.61 | +0.50 | +0.29% [-0.56, +0.85] | 0.56 | 0.0 | 0.00 |
| 17 | POCI | amc 11-16 |  | 15 | long | 21 | 5S | 25L | 44L | 6S | 0 | +0.08 | -0.00 | +0.29% [-0.66, +0.81] | 0.56 | 0.0 | 0.00 |
| 18 | OPRA | bmo 11-17 |  | 14 | short | 19 | 39S | 18S | 14L | 14S | 0 | -0.25 | -0.60 | +0.29% [-0.66, +0.81] | 0.56 | 0.0 | 0.00 |
| 19 | ELTK | bmo 11-17 |  | 8 | long | 18 | 9L | 28L | 22S | 14L | 0 | +0.23 | +1.90 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.00 |
| 20 | AYTU | amc 11-16 |  | 6 | long | 16 | 9S | 11L | 30L | 8S | 0 | -0.00 | -0.10 | +0.29% [-0.72, +0.79] | 0.56 | 0.0 | 0.00 |

**Selected (7):**
- **Short:** STEM, IMDX, NXB, TMS, RCAT, KLAR.
- **Long:** OMER.
- **Sessions:** all amc 11-16 except KLAR (bmo 11-17).
- **Just outside:** POWL at 77 short. Three judges had it in their own top 20%; Sonnet 5.5 had it at 38.

### The selected names

**STEM (95, short; 4 of 4, spread 3).**
- **Judges' case:** a roughly $19m equity stub sits under $118.7m of convertibles and about $160m of 11% notes, with no PIK capacity left. The operating-cash-flow guide needs +$8-18m in H2 after -$8.0m in H1. The print was moved to the last legal 10-Q day, three weeks into a Guggenheim recapitalisation review.
- **Strongest case against:** about 12% of float is short. The stock is -42% over 20 days, so much of this is already priced, and four of its six prior prints rose.
- **Tradable:** yes, short, borrow available at Alpaca. It is thin ($0.58m a day), so paper sizing is capped by capacity.

**IMDX (89, short; 4 of 4).**
- **Judges' case:** $18.7m of cash at 30 June against a guided burn of about $8m a quarter leaves roughly one quarter of runway, and a raise is likely. The FDA timeline has quietly moved into 2027, while the Street still carries Buy ratings.
- **Strongest case against:** the stock is -30% over 20 days and at its 52-week low.
- **Tradable:** elsewhere. Alpaca does not lend it on this snapshot, so check borrow at IBKR.

**NXB (85, short; 3 of 4).**
- **Judges' case:** a 90-day 15% bridge loan with a boat-sale sweep, and a revolver secured on the founder's pledged shares. This is the first print under an all-new management team, with the CFO seat vacant.
- **Strongest case against:** revenue is likely above the run rate the guide implies, and there is no sourced bar.
- **Tradable:** no. Turnover is $0.05m a day, below the floor.

**OMER (85, long; 3 of 4, Opus 5 at 80).**
- **Judges' case:** on 16 Oct, after the quarter closed, the company said US demand for YARTEMLEA is "rising" (https://www.webull.com/news/15757402736043008). Shorts added 1.4M shares after that, to 17.7% of shares at 9.6 days to cover, and the calls are bid.
- **Strongest case against:** the Q3 revenue bar is disputed, from $30.9m to $38.0m, and FY consensus implies a steep H2 ramp.
- **Tradable:** yes, long.

**TMS (82, short; 3 of 4).**
- **Judges' case:** the aggregator consensus of $177.5-178.7m needs acquired revenue that the company says is Q4-weighted and has not yet reported closing in any 8-K. The $60m pro-forma EBITDA guide needs $40m from acquisitions, and only $2.6m has closed.
- **Strongest case against:** the Sound Point refinancing should lift the going-concern language, and the stock has already slid 26% with no news.
- **Tradable:** elsewhere. It is not lendable at Alpaca and thin at $0.36m a day.

**RCAT (82, short; 2 of 4, spread 16).**
- **Judges' case:** Teal was absent from both Gauntlet II leaderboards, so the $14-28m of Q3 Drone Dominance revenue the CEO pointed to is likely near zero. Consensus still needs Q3 revenue near double Q2's, and there has been no order release since July.
- **Strongest case against:** 25.5% of shares are short at 6.3 days to cover, the skew is call-bid, and the stock rose +6.2% on its last revenue miss. Opus 5 sits only at 58 for that reason.
- **Tradable:** elsewhere. It is not lendable at Alpaca.

**KLAR (81, short; 2 of 4).**
- **Judges' case:** the FY adjusted operating income guide needs a record Q4 of $106-136m. The dollar has risen about 3% since the August guide, and every real print on this name has turned on the guide.
- **Strongest case against:** revenue has come in at the top of guidance three quarters running, and about 9.7% of float is short.
- **Tradable:** yes, short, borrow available.

**What this means for the book:**
- Of the seven selected, three are tradable at Alpaca: STEM short, OMER long and KLAR short.
- IMDX, TMS and RCAT are not shortable at Alpaca, and NXB is below the turnover floor.
- With three strong tradable names the top-up does not apply.
- Step 6b's plan decides the book, and the run log records it.

### Where the panel and the searcher disagree most

- **RCAT:** the searcher has -0.50 (p46); the panel has 82 short. The searcher's lessons shrank a -2.7 draft for the crowded short, while three judges kept the Gauntlet miss large.
- **POWL:** the searcher has -0.60; the panel has 77 short, with three judges in their own top 20% on the CFO's "not double-digit" against a +11-15% consensus.
- **ELTK:** the searcher has +1.90 (p89); the panel has 8. The judges treated the peer and FX items as proxies on an uncovered name.
- **GLAS:** spread 49. Sonnet 5.5 is at 87 short; Fable 5.1 leans long on the on-time-filing relief path.
- **INFQ:** spread 34. Opus 5 is at 86 short; Sonnet 5.5 leans long.

### Stage E comparison

Stage E has no files today: its Routine has been stopped since 2026-10-19, and `<RUN>/edge/` does not exist. Within this stage, Spearman ρ between the searcher's `impact_sum` and the signed `panel_pct` over the 20 names is **+0.86**.

### What the numbers are not

- **`expected_return_pct`** (and `expected_edge_pct` on selected names) is what names at that percentile have earned. Its out-of-sample record is weak: a correlation of +0.12 with the realised return over 148 names. It is not a forecast to size on.
- **The weights** (`w_equal`, `w_prec`) are research; nothing trades them.
- **`p_up`** is recorded and decides nothing.
- **Standing caveats:**
  - Nothing checked the findings for factual error.
  - The searchers' key is not reproducible to better than its own size.
  - The sign is lopsided: 13 of 20 searcher sums are negative, and 16 of 20 for Opus 5. The judges attribute that to a universe of distressed microcaps; LESSONS calls it a known artefact of the question.
- **Pre-announced quarters:** FTLF's Q3 10-Q was on EDGAR at 07:30 ET today, and the stock traded down on it intraday. OPRA pre-released Q3 on 11-03, and GLAS pre-released revenue on 10-19. The prints themselves are therefore partly stale.

### Searcher keys (score_report, verbatim)

**Stage E-P (searcher), 2026-11-16**: ranked on `impact_sum` (version 2, each finding sized on its own); conviction floor 2.8 applies to it only.
V2 at `session_close`, matrix as of 2026-11-16T18:08:30+00:00.
Brackets: percentile of |value| among reference names sized by Opus 5.5 (impact_sum n=938, impact_scaled n=954): live runs to date plus the blind re-judges, September Opus 5.5 hunts left out. Scale, not rank.

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up | V2 grounded | retail ≥50 | search quiet | vol ≥58 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | OMER | amc | **+2.80** (p96) | yes | +1.60 (p94) | 16.0 | 55 | +3.81 | yes (64) | n/a (sparse) | no (54) |
| 2 | ELTK | bmo | **+1.90** (p89) | no | +0.64 (p73) | 8.0 | 54 | +1.94 | yes (58) | n/a (sparse) | no (42) |
| 3 | API | amc | **+1.30** (p80) | no | +0.84 (p81) | 7.0 | 56 | +0.88 | yes (51) | yes (0.87x) | no (36) |
| 4 | YALA | amc | **+1.00** (p72) | no | +0.40 (p56) | 5.0 | 54 | +0.21 | no (38) | no (1.35x) | no (16) |
| 5 | DUOT | amc | **+0.50** (p46) | no | +0.88 (p82) | 11.0 | 54 | +3.01 | yes (85) | n/a (sparse) | yes (95) |
| 6 | INFQ | amc | **+0.10** (p14) | no | -0.20 (p33) | 10.0 | 49 | +2.14 | yes (77) | n/a (sparse) | yes (117) |
| 7 | POCI | amc | **-0.00** (p4) | no | +0.14 (p25) | 7.0 | 51 | +0.31 | yes (59) | n/a (sparse) | no (39) |
| 8 | AYTU | amc | **-0.10** (p14) | no | -0.42 (p57) | 7.0 | 47 | -0.12 | yes (62) | n/a (sparse) | no (35) |
| 9 | WRAP | amc | **-0.10** (p14) | no | -0.80 (p80) | 8.0 | 45 | -1.80 | yes (79) | n/a (sparse) | yes (99) |
| 10 | RCAT | amc | **-0.50** (p46) | no | -1.30 (p91) | 13.0 | 45 | -0.40 | yes (85) | yes (0.93x) | yes (122) |
| 11 | OPRA | bmo | **-0.60** (p53) | no | -0.12 (p22) | 6.0 | 49 | -0.34 | yes (57) | no (1.18x) | yes (62) |
| 12 | POWL | amc | **-0.60** (p53) | no | -0.72 (p77) | 12.0 | 47 | -2.03 | yes (59) | n/a (sparse) | yes (98) |
| 13 | FTLF | amc | **-0.90** (p67) | no | -0.30 (p45) | 5.0 | 47 | -0.84 | yes (64) | n/a (sparse) | yes (64) |
| 14 | XBP | amc | **-1.10** (p76) | no | -0.70 (p76) | 7.0 | 45 | -1.71 | yes (66) | n/a (sparse) | yes (60) |
| 15 | KLAR | bmo | **-1.30** (p80) | no | -1.40 (p93) | 14.0 | 45 | -2.03 | yes (51) | no (1.11x) | no (50) |
| 16 | GLAS | amc | **-1.40** (p82) | no | -1.80 (p95) | 18.0 | 45 | -8.34 | yes (90) | n/a (sparse) | yes (144) |
| 17 | NXB | amc | **-1.90** (p89) | no | -1.30 (p91) | 13.0 | 45 | -3.84 | yes (73) | n/a (failed) | yes (98) |
| 18 | TMS | amc | **-3.30** (p97) | yes | -1.30 (p91) | 13.0 | 45 | -6.80 | yes (62) | n/a (sparse) | yes (107) |
| 19 | STEM | amc | **-4.30** (p99) | yes | -2.64 (p98) | 22.0 | 44 | -16.00 | yes (94) | yes (0.75x) | yes (163) |
| 20 | IMDX | amc | **-4.50** (p99) | yes | -1.92 (p96) | 12.0 | 42 | -7.23 | yes (72) | n/a (failed) | yes (64) |

Not ranked: ACM: no hunt

Not ranked: AGPU: no hunt

Pre-lessons, scaled and V2 are measured beside the key, not traded. Control: `-run_up_20d_pct` in `edge-scores.json`.

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._
