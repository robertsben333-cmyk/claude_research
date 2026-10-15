# Stage E-P — 2026-10-15 amc + 2026-10-16 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel. It places no orders.**
All four judges ran on their pinned agents with no fallback: Opus 5 (`claude-opus-5`, accepted), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each covered all 13 packs.
One day is an anecdote. The panel is judged pooled over many days, never on one.

Window: 13 names, 8 amc on 10-15 and 5 bmo on 10-16. The sweep confirmed all 13 from company sources, with 0 phantoms and 0 unsettled sessions.

## The panel

`panel_pct` is the size of the mean of the four judges' signed percentiles, each against that judge's own live range (n=60 live sizes per member). A name is selected when all four judges are present and `panel_pct` is 80 or higher.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | old score | searcher impact_sum | E[return] (80% band) | P(right) | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LOOP | amc 10-15 | **yes** | 96 | short | 2 | 98S* | 95S* | 93S* | 98S* | 4 | −2.93 | −3.00 | +4.83% [+2.89, +6.55] | 0.72 | 0.5 | see json |
| 2 | JBHT | amc 10-15 | **yes** | 86 | long | 1 | 87L* | 85L* | 85L* | 87L* | 4 | +1.49 | +1.40 | +3.46% [+1.36, +5.46] | 0.65 | 0.5 | see json |
| 3 | CTW | amc 10-15 | | 75 | short | 10 | 78S | 60S | 88S* | 72S | 2 | −1.10 | −0.20 | +1.97% [+0.36, +3.78] | 0.57 | | |
| 4 | AA | amc 10-15 | | 66 | long | 7 | 55L | 68L | 70L | 72L | 0 | +0.79 | +0.50 | +1.27% [+0.08, +2.89] | 0.56 | | |
| 5 | CFG | bmo 10-16 | | 54 | long | 6 | 55L | 60L | 45L | 57L | 0 | +0.67 | +0.50 | +0.37% [−0.30, +1.81] | 0.56 | | |
| 6 | IBKR | amc 10-15 | | 35 | long | 16 | 27L | 43L | 15L | 57L | 0 | +0.36 | +0.15 | +0.29% | 0.56 | | |
| 7 | MTB | bmo 10-16 | | 32 | long | 12 | 28L | 37L | 15L | 48L | 0 | +0.33 | +0.20 | +0.29% | 0.56 | | |
| 8 | RF | bmo 10-16 | | 23 | short | 6 | 18S | 20S | 22S | 33S | 0 | −0.26 | −0.65 | +0.29% | 0.56 | | |
| 9 | SFNC | amc 10-15 | | 23 | long | 8 | 27L | 20L | 12L | 33L | 0 | +0.26 | +0.30 | +0.29% | 0.56 | | |
| 10 | CNS | amc 10-15 | | 20 | short | 16 | 13S | 7S | 47S | 15S | 0 | −0.22 | −0.40 | +0.29% | 0.56 | | |
| 11 | INDB | amc 10-15 | | 15 | short | 6 | 25S | 15S | 15S | 7S | 0 | −0.19 | −0.20 | +0.29% | 0.56 | | |
| 12 | TRV | bmo 10-16 | | 15 | long | 10 | 28L | 18L | 8L | 3L | 0 | +0.13 | −0.20 | +0.29% | 0.56 | | |
| 13 | TFC | bmo 10-16 | | 5 | long | 17 | 5L | 15L | 22S | 23L | 0 | +0.11 | −0.20 | +0.29% | 0.56 | | |

`*` marks a judge's own top 20%. The judges are reported as percentiles, not raw sizes. `weight_precision_tilt` is in `edge-scores-panel.json`.

**What the E[return] column is.** It is the expected return at that percentile, a translation of `panel_pct` and not a separate forecast: every name at the same percentile gets the same number. It is gross, measured on the scorebord's window, and fitted on 148 resolved panel names. It is flat at about +0.3% below a percentile of 50, and out of sample it correlates only +0.12 with the realised return. Do not size on it.

## The selected names

**LOOP, short, panel_pct 96 (4 of 4, every judge in its own top 3–7%).** All four judges named the same line: liquidity.

- **The case for the short.** At 31 May, Loop had $1.06M of cash plus a CAD 3.5M undrawn facility, against about $1.2M a quarter of operating burn and $599K of FY27 loan repayments ([FQ1 10-Q](https://www.sec.gov/Archives/edgar/data/1504678/000143774926023542/loop20260531_10q.htm)). That arithmetic puts 31 August liquidity near $2M. The going-concern doubt is still in the filings, and EDGAR shows no financing since. The India JV project debt was still "term sheets under review" in the 1 October deck ([slide 8](https://www.sec.gov/Archives/edgar/data/1504678/000143774926031737/slide08.jpg)), against the "fall 2026" close given on the July call, and Loop's roughly $25M equity share is unfunded. The stock fell on 5 or 6 of its last 7 prints, depending on the judge's count.
- **The strongest case against.**
  - The stock is already −34% over 20 days and at its 52-week low.
  - A strategic-alternatives committee was formed on 17 September ([8-K](https://www.sec.gov/Archives/edgar/data/1504678/000143774926030685/ex_1017371.htm)), and the chairman's fund bought at $0.64–0.73.
  - A financing or India debt close announced with the print would flip the sign. The searcher put the range at up to +4 for the India finding and +10 for the strategic review.
- **Untradeable at size.** The stock turns over about $45k a day (128.6k shares at $0.351), far under stage E's $200k floor. It has no usable option chain and no skew.
- **Our verdict:** a research result, not a trade. If it were a trade, it would carry a named reservation for the strategic-review tail.

**JBHT, long, panel_pct 86 (4 of 4, every judge at its 85th–87th percentile).**

- **The case for the long.**
  - The quarter was pre-announced on 15 September (Q3 EPS guided to $1.72–1.81), so the stock trades on the call.
  - Diesel peaked at $6.51 on 21 September and has since fallen to about $6.25–6.31. Management said the surcharge lag turns into a tailwind when fuel falls. The searcher's October diesel figure is a secondhand quote of GasBuddy.
  - Intermodal bid season opens in October, with truck spot rates up about 50% year on year, tender rejections at 13.8%, and rail intermodal volume up 6–7% year on year in late September.
- **The strongest case against.**
  - Consensus of $1.81 sits at the top of the guide, while September diesel and purchased-transport costs point to the lower half, so a headline miss is likely.
  - Put skew is +4.15.
  - The three supporting findings are industry series, not company numbers.
- **Tradable:** about $231M a day.
- **Our verdict:** a research result, with a named reservation for the likely headline miss.

## Where the panel and the searcher disagree most

- **CTW:** the searcher has −0.20 (near zero), while the panel has 75 short and Sonnet 5.5 puts it in its own top 20%. The judges weighted the roughly 7% weaker yen against a +41% comparison more heavily than the searcher did. Turnover is about $35k a day.
- **TRV and TFC:** the searcher leans slightly negative (−0.20 each), and the panel leans slightly long (15 and 5). Both are near-nulls either way.
- **RF:** the searcher's second-largest negative (−0.65) is only 23 on the panel.

## Stage E comparison

Stage E's `research/2026/10/2026-10-15/edge/edge-scores.json` did not exist when this note was written (about 17:45 UTC). Stage E had published no directory and no run-log heartbeat today, so no overlap or Spearman ρ can be computed. Stage E's Routine lives on another account and cannot be inspected from here (see CLAUDE.md), so it is not established whether it fired late or did not fire.

## Searcher table (the comparison arm)

The searcher's own `impact_sum`, `impact_scaled` and V2 are in `score_report.py`'s table and the run reply. V2 was calibrated and written before the first print, with 13 of 13 names grounded at `session_close` on 186 ledger observations. Only LOOP (−3.00) clears the 2.8 floor.

- **Sign balance:** the searcher's sum is positive on 6 names and negative on 7.
- **Control `-run_up_20d_pct`, per name:**

  | Name | Control |
  |---|---|
  | LOOP | +34.15 |
  | AA | +14.73 |
  | CNS | +7.49 |
  | INDB | +6.21 |
  | CTW | +5.58 |
  | CFG | +5.56 |
  | IBKR | +4.69 |
  | RF | +4.04 |
  | TFC | +3.96 |
  | MTB | +3.13 |
  | SFNC | +2.40 |
  | JBHT | +1.23 |
  | TRV | +0.48 |

  The panel's top short, LOOP, is the control's strongest long. The two disagree on the day's largest name.
- **Option coverage:** 8 of 13 names have a usable option chain. The other 5 have a historical-median baseline: INDB, CNS, SFNC, CTW and LOOP.
- **One correlated exposure:** six regional banks (TFC, MTB, CFG, RF, INDB, SFNC) share deposit-cost and NII drivers. The searchers for those names relied on the same PNC, First Horizon and FB Financial read-throughs.

## What the numbers are not

- `expected_return_pct` and `expected_edge_pct` are what names at that percentile have earned, not a forecast to size on. The weights are research, and nothing trades them.
- `p_up` is recorded and decides nothing.
- Nothing checked the findings: a factually wrong one enters at full size.
- The key is not reproducible to better than its own size. When names were hunted twice, the two hunts' sums differed by a median 2.40 points, and 4 of 12 pairs had opposite signs.
- Below the floor, the sign of `impact_sum` is a coin flip on the evidence so far.

## Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing ranks, selects or sizes on them.

| Name | Retail tilt | Search spike | Realised vol |
|---|---|---|---|
| LOOP | 75 (≥50) | sparse | 64 (≥58) |
| CTW | 67 (≥50) | 0.94x (quiet) | 102 (≥58) |
| JBHT | 29 | failed | 25 |
| AA | 44 | 0.93x (quiet) | 28 |
| CFG | 29 | 1.03x | 18 |
| SFNC | 40 | failed | 16 |
| MTB | 18 | 1.08x | 14 |
| IBKR | 31 | 0.88x (quiet) | 30 |
| INDB | 32 | 0.91x (quiet) | 17 |
| TFC | 24 | 0.88x (quiet) | 18 |
| TRV | 15 | 0.96x (quiet) | 18 |
| CNS | 29 | sparse | 20 |
| RF | 36 | sparse | 17 |

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
