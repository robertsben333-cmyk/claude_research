# Stage E-P — 2026-11-20 amc + 2026-11-23 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel. It trades the panel's book on a live and a paper Alpaca account.**
All four judges ran on their pinned models: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. None was missing.
One day is an anecdote. This is a thin Friday with five names, and **no name was selected**.

## Panel table

The window held 6 calendar names with a confirmed session. The sweep confirmed 5 of them; ADXN had no company notice and was not hunted. All 5 confirmed names were searched, and every search finished.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | THCH | bmo 11-23 | no | 59 | short | 13 | 72 S | 64 S | 60 S | 38 S | 0 | -0.81 | -0.25 | +0.70% [-0.17, +2.17] | 0.56 |
| 2 | BLRX | bmo 11-23 | no | 53 | long | 9 | 56 L | 57 L | 60 L | 38 L | 0 | +0.74 | +1.20 | +0.34% [-0.34, +1.70] | 0.56 |
| 3 | DLNG | amc 11-20 | no | 35 | long | 8 | 46 L | 34 L | 24 L | 38 L | 0 | +0.44 | +0.40 | +0.29% [-0.54, +0.87] | 0.56 |
| 4 | CRGO | bmo 11-23 | no | 34 | short | 53 | 89 S* | 12 L | 24 L | 84 S* | 2 | -0.60 | -0.70 | +0.29% [-0.55, +0.87] | 0.56 |
| 5 | VNET | bmo 11-23 | no | 6 | short | 52 | 84 L* | 32 S | 32 S | 43 S | 1 | -0.38 | -0.20 | +0.29% [-0.72, +0.79] | 0.56 |

`*` marks a judge's own top 20%. Each judge is shown as its own percentile, never as a raw size.

`E[return]` is what names at that percentile have earned on the panel's side, gross, over the scorebord window. Below a percentile of 50 it is flat at about +0.3%, so it translates the percentile and is not a separate forecast.

Weights (`weight_equal`, `weight_precision_tilt`) are zero for every name, because nothing was selected.

## Selected names

None. No name reached panel_pct 80, and none fell in the 70-79 top-up band, so the book is empty on both accounts.

## Where the panel and the searcher disagree most

- **CRGO:** Opus 5 (89, short) and Fable 5.1 (84, short) both put it in their own top 20%. They read the street consensus sitting at the top of the guide as forcing Solutions to hold its level, and they lean on the Q3 2025 precedent, when a KPI beat and a revenue lag gave −13.9%. Opus 5.5 and Sonnet 5.5 lean slightly long. The spread is 53 and the mean is 34.
- **VNET:** Opus 5 is at 84 long, on the crowded short (about 26% of float) and the event move it thinks the market underprices. The other three judges lean mildly short on the revenue arithmetic. The mean nets to 6.

## Stage E comparison

Stage E wrote no `edge/` directory today; its Routine is stopped. There is no overlap and no ρ.

## What the numbers are not

- **`expected_return_pct`:** what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 over 148 names). It is not a forecast to size on.
- **`p_up`:** recorded and decides nothing.
- **Unchecked findings:** nothing checked them for factual errors.
- **The searcher's key:** cannot be reproduced to better than its own size.
- **Reaction histories:** every baseline's history is empty, because `SEC_USER_AGENT` is unset and www.sec.gov answered 403.
- **Option chain:** only VNET has a live one.
- **Liquidity:** all five names are thin. Turnover runs from about $14k to $165k a day, except VNET.

## Context: retail, search and volatility (not used for selection)

These labels are context only.

- **Retail tilt:** 50 or above on all five names.
- **Search:** sparse, or failed for DLNG.
- **Volatility at 58% or above:** VNET (128), THCH (92) and CRGO (74).

This is a forecasting exercise over public information. It is not investment advice.
