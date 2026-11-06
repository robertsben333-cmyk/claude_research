# Stage E-P — 2026-11-06 amc + 2026-11-09 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel; the panel's book is traded on the Alpaca PAPER account (step 6b).** All four members ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), one part, no fallback, no retry. One day is an anecdote.

Universe 65 names; sweep confirmed 48; 20 hunted (cap), 19 rankable — TOMZ (the only amc name hunted) moved its Q3 release to 2026-11-12 in a company release at 10:30 ET today, so it has no event in the window. Every ranked name reports Monday 2026-11-09 before the open. No search was cut off (hunt_status: 0 unfinished of 20).

## The panel

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HAIN | bmo | yes | 99 | short | 1 | 99S* | 100S* | 98S* | 100S* | 4 | -3.60 | -6.00 | +5.06% [+3.24, +6.70] | 0.73 | 1.00 | 1.25 |
| 2 | DCTH | bmo | yes | 90 | long | 4 | 90L* | 88L* | 98L* | 86L* | 4 | +1.62 | +2.00 | +4.11% [+2.02, +6.06] | 0.69 | 1.00 | 1.00 |
| 3 | VFF | bmo | yes | 90 | long | 10 | 98L* | 88L* | 98L* | 74L | 3 | +1.94 | +2.00 | +4.02% [+1.92, +5.98] | 0.68 | 1.00 | 0.90 |
| 4 | QTRX | bmo |  | 78 | short | 21 | 49S | 96S* | 98S* | 68S | 2 | -1.61 | -1.20 | +2.35% [+0.51, +4.23] | 0.59 | 0.00 | 0.00 |
| 5 | SOC | bmo |  | 74 | short | 17 | 70S | 84S* | 93S* | 49S | 2 | -1.22 | -0.60 | +1.93% [+0.34, +3.72] | 0.56 | 0.00 | 0.00 |
| 6 | TGTX | bmo |  | 74 | short | 8 | 82S* | 70S | 80S* | 63S | 2 | -1.12 | +0.10 | +1.90% [+0.33, +3.69] | 0.56 | 0.00 | 0.00 |
| 7 | NRXS | bmo |  | 72 | short | 9 | 84S* | 64S | 80S* | 63S | 2 | -1.06 | -1.30 | +1.78% [+0.29, +3.53] | 0.56 | 0.00 | 0.00 |
| 8 | LFMD | bmo |  | 70 | short | 18 | 82S* | 82S* | 76S | 38S | 2 | -1.23 | +0.90 | +1.51% [+0.20, +3.19] | 0.56 | 0.00 | 0.00 |
| 9 | LINC | bmo |  | 56 | short | 19 | 66S | 64S | 72S | 22S | 0 | -0.88 | -1.20 | +0.45% [-0.26, +1.94] | 0.56 | 0.00 | 0.00 |
| 10 | VIA | bmo |  | 52 | short | 28 | 60S | 55S | 9S | 86S* | 1 | -0.74 | -0.80 | +0.34% [-0.35, +1.66] | 0.56 | 0.00 | 0.00 |
| 11 | MNDY | bmo |  | 48 | short | 38 | 90S* | 70S | 44S | 12L | 1 | -0.71 | +0.80 | +0.29% [-0.45, +1.31] | 0.56 | 0.00 | 0.00 |
| 12 | HRTX | bmo |  | 36 | long | 53 | 76L | 48L | 55S | 73L | 0 | +0.85 | +0.70 | +0.29% [-0.54, +0.88] | 0.56 | 0.00 | 0.00 |
| 13 | MPAA | bmo |  | 18 | long | 40 | 55L | 44S | 50L | 12L | 0 | +0.38 | -0.50 | +0.29% [-0.61, +0.82] | 0.56 | 0.00 | 0.00 |
| 14 | PRAX | bmo |  | 18 | long | 8 | 4L | 22L | 24L | 22L | 0 | +0.30 | +0.70 | +0.29% [-0.61, +0.82] | 0.56 | 0.00 | 0.00 |
| 15 | TPB | bmo |  | 18 | short | 32 | 63S | 32S | 9L | 16L | 0 | -0.11 | +0.40 | +0.29% [-0.62, +0.82] | 0.56 | 0.00 | 0.00 |
| 16 | FRVO | bmo |  | 16 | long | 42 | 0- | 50L | 44S | 60L | 0 | +0.30 | +1.30 | +0.29% [-0.64, +0.81] | 0.56 | 0.00 | 0.00 |
| 17 | OCUL | bmo |  | 9 | long | 12 | 25L | 8L | 9S | 11L | 0 | +0.17 | +0.40 | +0.29% [-0.70, +0.79] | 0.56 | 0.00 | 0.00 |
| 18 | TNXP | bmo |  | 4 | short | 27 | 40S | 8L | 16S | 33L | 0 | -0.05 | +0.40 | +0.29% [-0.73, +0.78] | 0.56 | 0.00 | 0.00 |
| 19 | EVGO | bmo |  | 3 | long | 3 | 6L | 4L | 0- | 0- | 0 | +0.03 | +0.00 | +0.29% [-0.75, +0.78] | 0.56 | 0.00 | 0.00 |

Percentiles are each judge's own: the share of that judge's live sizes from runs before today with a smaller |impact_sum| (`*` = in its own top 20%). The expected return is the translation of the percentile — what names at that `panel_pct` have earned on the panel's side, gross, on the scorebord's window, flat at about +0.3% below a percentile of 50 — not a separate forecast.

## Selected names

**HAIN, short, panel_pct 99 (4 of 4 in their own top 20%).** Every judge rests on the same items: on 11 Oct the board put a restructuring banker (Richard Shinder) on its Strategy Committee at $30k a month, in the same 8-K that disclosed the failed lender-consent condition for the Aurelius sale; $557.6m matures 22 Dec against ~$58m cash, the 10-K carries going-concern language, and Bloomberg reported a Chapter 11 being weighed "as soon as next month". The 9 Nov release is the first scheduled update. **Case against:** the equity at $0.14 is an option on an extension (six rounds of lender relief since 2016), the 15 Oct crash already took −51%, and "a restructuring banker means a filing" is the searcher's inference, not a document. **Untradable here:** thin ($0.33m/day) and not lendable at Alpaca, so the book drops it before the split.

**DCTH, long, panel_pct 90 (4 of 4).** Consensus ($25.6m) still models a 12% sequential Q3 dip, while management said on the 6 Aug call it had reduced the assumed seasonal step-down and trained backup REMS teams to avoid last year's capacity loss; a ~$27m print would leave Q4 trivially inside the $104–108m FY guide, i.e. a raise, on a name that paid +22.5% and +23.6% for its last two beat-and-raises; no October pre-release this year (2025's was a warning). **Case against:** the "no softness" comment had two to three weeks of visibility; 340B discounts cut revenue per kit and the margin is flagged below 90%; the fix is management's claim, not data.

**VFF, long, panel_pct 90 (3 of 4; Fable 5.1 at 74).** Aurora (5 Nov) and Canopy (6 Nov) reported the same quarter after VFF last spoke, international medical +44% and +141% on Germany and Poland, into a single-source consensus ($64.4m) flat on Q2, after VFF beat revenue consensus by ~14–15% on its last prints, each bought double digits. **Case against:** the bar is one source; the stock is +16% in five days and ~47% since July on the Organigram–Aurora deal, so part is priced; Aurora's medical gross margin fell to 62% from 69% on competition.

## Where panel and searcher disagree most

- **LFMD**: searcher +0.90 (long lean), panel 70 short — three of four judges weigh the Q4 ramp and the revolver covenant over the Lilly deal.
- **MNDY**: searcher +0.80, panel 48 short (Opus 5 at 90 short on the peer guide sell-offs; Fable 5.1 long).
- **TGTX**: searcher +0.10, panel 74 short (EPS bar needs opex far below Q2).
- **QTRX**: both short; panel 78, just below the cut, with Opus 5 at only 49.

## Stage E comparison

Stage E's `edge/` does not exist for this date (its Routine is stopped), so there is no overlap or Spearman ρ to report.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 names); it is not a forecast to size on. The weights in the table are research; the book uses `execution.panel` (panel_pct − 60, 50% cap). Certainty (`p_up`) is recorded and decides nothing. Nothing checked the findings for factual error (no adversary pass), and the key is not reproducible to better than its own size (four of twelve double-hunted pairs once came back with opposite signs). Sign balance of the searcher: 11 positive, 1 zero, 7 negative; of the panel: 7 long, 12 short. 9 of 19 ranked names had a priced option chain (DCTH, FRVO, LINC, MNDY, PRAX, TGTX, and SOC, TPB, OCUL indicative only on wide spreads); the other 10, including selected HAIN and VFF, fall back to historical medians. The searcher's own `impact_sum` clears the 2.8 floor on one name only (HAIN −6.0). Tradability: HRTX, MPAA and HAIN are thin (<$1m/day); HAIN and HRTX are not lendable at Alpaca (check IBKR).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
