# Stage E-P — 2026-11-25 amc + 2026-11-27 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel.** It trades the panel's book on the live and paper Alpaca accounts at step 6b; the orders are in the run log and in `alpaca-orders*.json`. All four judges ran on their pinned models: Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1. No fallback was used. **One day is an anecdote, and this is a three-name day.**

The window was thin because of Thanksgiving. Thursday 11-26 is a market holiday, so all three prints react in Friday 11-27's half-day session, which closes at 13:00 ET.
- **Confirmed sessions:** the calendar gave 2 names with a confirmed session.
- **Unknown-session rows:** 33 rows had `time-not-supplied`. `session_resolve.py` killed 1 (PVL) and carried 32.
- **Sweep:** of the 35 rows, the sweep confirmed 3, all on company sources: FINV (amc 11-25), BMA (amc 11-25, from the Banco Macro IR page) and XYF (bmo 11-27). The other 32 were dropped.
- **Hunting:** all 3 were hunted and none was shed. All three searches completed.

## The panel

| rank | ticker | session | selected (mean ≥ 80) | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | consensus_k | panel_score | searcher impact_sum | E[return] (80% band) | p_right |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FINV | amc 11-25 | no (top-up band 70-79) | 79 | short | 13 | 58 S | 92 S* | 80 S | 88 S* | 3 | -1.39 | -0.30 | +2.51% [+0.58, +4.43] | 0.60 |
| 2 | BMA | amc 11-25 | no | 61 | short | 9 | 54 S | 64 S | 74 S | 53 S | 0 | -0.81 | -0.80 | +0.90% [-0.09, +2.39] | 0.56 |
| 3 | XYF | bmo 11-27 | no | 57 | short | 10 | 41 S | 59 S | 66 S | 63 S | 0 | -0.80 | -2.00 | +0.56% [-0.22, +2.05] | 0.56 |

How to read the table:
- **Member columns:** each is that judge's own percentile against its live range, 0–100. L or S gives the side, and `*` marks a judge's own top 20%.
- **`weight_equal` and `weight_precision_tilt`:** both are 0 for every name, because nothing cleared the mean-percentile selection.
- **E[return]:** what names at that percentile have earned on the panel's side. It is one number per percentile, gross, measured on the scorebord window. Below a percentile of 50 it is flat at about +0.3%. It translates the percentile; it is not a separate forecast.

**No name reached `panel_pct` 80, so the mean-percentile rule selected nothing.**
- **FINV at 79.2:** it misses 80 by under a point. Three of four judges put it in their own top 20% on the short side, so the old 3-of-4 consensus rule would have selected it.
- **Top-up:** `execution.panel.top_up` puts 70–79 names in the book on a day with no strong name, at equal weight and at most 33% each. FINV is the only name in that band, so the book is FINV short. What was actually placed is in step 6b of the run log.

## FINV, the only name near the line

The case is a peer read-through.
- **Qfin's Q3, reported 11-24:**
  - Volume fell 40.6% YoY.
  - It guided Q4 non-GAAP net income to RMB250–350m, which is −67 to −77% YoY, and Q4 volume to about −20% QoQ.
  - Management said "a 3% take rate is impossible to maintain". FINV's China take rate is about 3.2%.
  - Source: https://uk.investing.com/news/stock-market-news/earnings-call-transcript-qfin-holdings-posts-weak-q3-2026-results-as-growth-slows-93CH-5002961
- **Why it matters for FINV:** the stock trades on its guide. Its FY revenue guide of RMB11.5–12.9bn was steered to the low end on 2026-08-27, conditional on the environment holding (https://www.financialcontent.com/article/gnwcq-2026-8-27-finvolution-group-reports-second-quarter-2026-unaudited-financial-results).

**The strongest case against:**
- **Already public and already sold:** Qfin's print is a day old. FINV fell 5.4% on 11-25 and 17.6% over 20 days, to its 52-week low.
- **The low end may still hold:** the FY low end needs only about RMB4.89bn in H2.
- **Buyback headroom:** US$946m of cash and short-term investments against a US$150m buyback with about US$123m unused.
- **Judges split on size:** Opus 5 put it at only its 58th percentile.

The option-implied event move is about 13.4%, indicative only, from a wide chain. The reaction session is a thin Friday half day.

## Where panel and searcher disagree most

- **XYF:** the searcher's sum is −2.00, the largest of the day. The panel puts it at 57, the lowest. The judges discounted a peer proxy on a name with no sourced bar, no consensus and no option chain.
- **FINV:** the searcher's sum is −0.30, nearly flat. The panel puts it at 79, the highest. The judges weighted the Qfin guide read-through more heavily than the searcher's offsetting low-end arithmetic did.

## Stage E

Stage E wrote no `edge/` today, because its Routine has been stopped since 2026-10-19. There is no overlap and no Spearman ρ.

## Searcher table and context

| ticker | impact_sum | pre-lessons | impact_scaled | V2 | floor 2.8 | tradable | -run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FINV | -0.30 | -0.70 | -1.30 | -0.44 | - | yes, $2.22m/day, borrow ok | +17.6 |
| BMA | -0.80 | -1.50 | -0.63 | -0.43 | - | yes, $15.75m/day, borrow ok | +17 |
| XYF | -2.00 | -2.80 | -0.70 | -4.81 | - | thin, $0.52m/day, borrow ok | -6.6 |

**Signs:** all three hunts leaned negative, and so did all twelve judge verdicts. Two of the three names are at 52-week lows after sector selloffs, so this may be the run-up talking rather than information. On this day the control (−run-up) points long on FINV and BMA.

### Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing selects or sizes on them.
- **FINV:** retail 62.2, so ≥50 yes. 20-day volatility 52.6%. Search data too sparse to read.
- **BMA:** retail 43.6, no. Volatility 38.3%. Search spike 0.86x, quiet.
- **XYF:** retail 62.9, yes. Volatility 86.3%, so ≥58 yes. Search spike 0.73x, quiet.

## What the numbers are not

- **`expected_return_pct`:** this is what names at that percentile have earned. Out of sample it has a weak record, correlating +0.12 with the realised return over 148 names. It is not a forecast to size on.
- **`p_up`:** recorded, and it decides nothing.
- **No fact-checking:** nothing checked the findings, so a factually wrong finding enters at full size.
- **Reproducibility:** the key is not reproducible to better than its own size.
- **No sourced consensus bar:**
  - XYF and FINV have none at the quarter level.
  - BMA's bar is disputed. Bloomberg's consensus is ARS219.5bn and Citi's estimate is ARS188.5bn.
- **Baseline histories:** these are empty for all three, because SEC_USER_AGENT is unset in this environment and www.sec.gov returned 403.

This is a forecasting exercise over public information. It is not investment advice.
