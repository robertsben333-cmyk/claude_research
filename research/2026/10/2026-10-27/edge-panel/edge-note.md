# Stage E-P — 2026-10-27 amc + 2026-10-28 bmo

**This is stage E-P: Opus 5.5 searchers, then a blind four-model panel.** It is also the stage that places the Alpaca paper book (step 6b, after this note).
All four judges ran on their pinned models, with no fallback: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each judge covered all 20 names in one part.
**One day is an anecdote.** Only pooled days can say whether the panel selects.

Universe: 168 names on the calendar (82 amc 10-27, 86 bmo 10-28), all baselines sealed before any agent ran. The sweep checked 27 names and confirmed 22 from company sources, with no phantom proven. 20 names were hunted. NHTC and CTO were confirmed but shed on hunt_priority, and every unchecked row was shed with them.

## The panel

Columns:
- **pct**: `panel_pct` on a 0-100 scale. Its side is in the next column.
- **Judge columns**: each judge's own percentile against its live range, with L or S for its side. `*` marks a judge's own top 20%.
- **E[ret]**: the expected return at that percentile, gross, on the scorebord window. Its 80% band and P(right) follow.
- **w**: the weight in the book, which is `panel_pct − 60`.

| # | ticker | session | sel | pct | side | sd | Opus 5 | Opus 5.5 | Sonnet 5.5 | Fable 5.1 | k | score | searcher impact_sum | E[ret] (80% band) | P(right) | w |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BOOM | amc 10-27 | **yes** | 96 | long | 2 | 94L* | 97L* | 98L* | 93L* | 4 | +2.13 | +1.65 | +4.80% (+2.85, +6.53) | 0.72 | 35.8 |
| 2 | OI | amc 10-27 | **yes** | 94 | short | 4 | 94S* | 99S* | 89S* | 94S* | 4 | −1.96 | −1.20 | +4.64% (+2.64, +6.43) | 0.71 | 34.2 |
| 3 | RBBN | amc 10-27 | **yes** | 90 | short | 9 | 74S | 97S* | 95S* | 95S* | 3 | −2.04 | −1.70 | +4.15% (+2.06, +6.08) | 0.69 | 30.4 |
| 4 | ENPH | amc 10-27 | **yes** | 86 | short | 11 | 82S* | 99S* | 92S* | 69S | 3 | −1.58 | −0.90 | +3.43% (+1.33, +5.43) | 0.65 | 25.6 |
| 5 | LUNG | amc 10-27 | **yes** | 85 | short | 8 | 87S* | 88S* | 72S | 93S* | 3 | −1.58 | −2.00 | +3.34% (+1.23, +5.35) | 0.64 | 25.0 |
| 6 | KIDS | amc 10-27 | **yes** | 84 | long | 9 | 83L* | 90L* | 92L* | 69L | 3 | +1.56 | +0.20 | +3.15% (+1.08, +5.14) | 0.63 | 23.7 |
| 7 | AMRN | bmo 10-28 | | 71 | short | 22 | 39S | 85S* | 95S* | 64S | 2 | −1.09 | −1.50 | +1.61% | 0.56 | — |
| 8 | JMKE | bmo 10-28 | | 62 | long | 16 | 52L | 80L | 74L | 40L | 0 | +0.74 | +1.00 | +0.93% | 0.56 | — |
| 9 | DMC | bmo 10-28 | | 55 | short | 20 | 31S | 80S* | 67S | 40S | 1 | −0.63 | −0.90 | +0.37% | 0.56 | — |
| 10 | OPFI | bmo 10-28 | | 54 | short | 12 | 58S | 72S | 47S | 40S | 0 | −0.65 | +0.60 | +0.37% | 0.56 | — |
| 11 | OTLY | bmo 10-28 | | 53 | long | 40 | 83L* | 50L | 90L* | 11S | 2 | +0.99 | +2.20 | +0.35% | 0.56 | — |
| 12 | UCTT | amc 10-27 | | 50 | short | 26 | 66S | 45S | 79S | 9S | 0 | −0.70 | +0.20 | +0.29% | 0.56 | — |
| 13 | FSP | amc 10-27 | | 48 | short | 11 | 29S | 52S | 57S | 54S | 0 | −0.58 | −1.00 | +0.29% | 0.56 | — |
| 14 | BRSP | amc 10-27 | | 32 | long | 20 | 15L | 35L | 63L | 16L | 0 | +0.33 | +0.50 | +0.29% | 0.56 | — |
| 15 | INTA | amc 10-27 | | 28 | short | 46 | 39S | 42S | 47L | 78S | 0 | −0.45 | −0.50 | +0.29% | 0.56 | — |
| 16 | SEVN | amc 10-27 | | 23 | short | 19 | 42S | 42S | 4S | 4S | 0 | −0.28 | −0.50 | +0.29% | 0.56 | — |
| 17 | LU | amc 10-27 | | 16 | short | 14 | 31S | 0 | 30S | 4S | 0 | −0.23 | −0.20 | +0.29% | 0.56 | — |
| 18 | SLDE | amc 10-27 | | 10 | short | 34 | 63S | 21L | 17L | 16S | 0 | −0.03 | −0.50 | +0.29% | 0.56 | — |
| 19 | REPL | bmo 10-28 | | 2 | short | 20 | 17L | 35S | 9L | 0 | 0 | +0.09 | +0.00 | +0.29% | 0.56 | — |
| 20 | BBNX | amc 10-27 | | 0 | long | 56 | 63S | 42S | 80L* | 25L | 1 | −0.05 | +0.70 | +0.29% | 0.56 | — |

`weight_equal` and `weight_precision_tilt` are in `edge-scores-panel.json`. The book uses the live linear rule (panel_pct − 60, at most 50% of equity a name).

How to read the expected return:
- It is the translation of the percentile, not a separate forecast: every name at the same percentile gets the same number.
- It is gross, on the scorebord window, and flat at about +0.3% below a percentile of 50.

All six selected names are amc tonight. The book is therefore one overnight gap: two longs and four shorts.

## Selected names

**BOOM (long, 96, all four judges in their top 20%).**
- Case for: the company guided Q3 sales to $158-168M, while Street revenue consensus sits below that floor ($154.3M at Earnings Whispers, $156.4M at Investing.com). Frac spread counts rose quarter on quarter. Q2 beat a ~$146M consensus with $157M, and the stock rose 15.5%.
- Strongest case against: the partner's put on the remaining 40% of Arcadia has been exercisable since 2026-09-06, and nobody has said whether it was used. Its value is ~$187M of carried minority interest against $28.6M of cash, settled 20% in cash and 80% in preferred. This release or the 10-Q is the first place an exercise would show.
- Thin: about $0.6m of turnover a day.

**OI (short, 94, all four in their top 20%).**
- Case for: TTF European gas went from a €45 June average to about €89-91 on Oct 22, after O-I last guided. O-I has hedged 75-80% of its 2026 European gas, and the guide was already cut twice on this exact driver. Each of the last two prints fell about 15%.
- Strongest case against: the stock is up 13% over 20 days off its low, and the +9.9 put skew already leans the same way. Ardagh's European furnace closures help O-I's pricing. The bar is unsourced: EPS guidance was withdrawn and aggregators disagree.

**RBBN (short, 90, three of four in their top 20%; Opus 5 at 74).**
- Case for: Rosenblatt downgraded the stock on 2026-09-14 on another delay to Verizon's voice-modernization project. The full-year guide needs a record Q4, and Q3 is the first leverage-covenant test after the May waiver.
- Strongest case against: the stock is down 24% in 20 days, about 3% above its 52-week low, so much of the delay is priced. Record IP Optical bookings support the quarter.

**ENPH (short, 86).**
- Case for: the company's own safe-harbor figures suggest about $75M of Q4 revenue falls away, while Q4 consensus is flat at about $305M. The same setup drew −15% a year ago.
- Strongest case against: short interest is 21.9% of float, put skew is +28.7 vol points, and the stock is down 22% since July. The February print squeezed +38.6%. Opus 5 judged the cliff substantially priced; Fable 5.1 sat outside its own top 20%.

**LUNG (short, 85).**
- Case for: the FY26 $90-92M guide needs H2 growth of +6-10% year on year after H1 fell 6.7%, with China shipments at zero. That implies a record Q4. Guidance moves on this name have run −42% to +29%.
- Strongest case against: the Street already sits at the low end of the guide, simply holding the guide in July drew +28.8%, and short interest is low (about 1.6% of shares).
- Thin: about $0.6m of turnover a day.

**KIDS (long, 84).**
- Case for: the run-rate points to a third beat-and-raise. H1 grew +14%, Trauma & Deformity +26%, and most of the year's ~$10M of instrument-set deployment falls in Q3. The last two raises rose +3.8% and +6.9%.
- Strongest case against: there is no Q3 consensus, so the bar is the searcher's own arithmetic. The largest holder (Squadron, ~24%) sold mid-quarter. The EBITDA guide needs a record H2. Last year's Q3 pre-announced a miss at −9.2%.

## Where the panel and the searcher disagree most

- **OTLY**: the searcher's largest number (+2.20) became a panel_pct of 53. Fable 5.1 went the other way (11S), and the spread of 40 is the day's second widest.
- **KIDS**: the searcher's sum was +0.20, but three judges put the name in their top 20% long.
- **OPFI**: the searcher's sum was +0.60, yet all four judges lean short.
- **UCTT**: the searcher's sum was +0.20 and the panel leans short at 50.
- **BBNX**: the searcher's sum was +0.70 and the panel reads it as a non-result (0, spread 56).

## Stage E

`research/2026/10/2026-10-27/edge/` does not exist: stage E's Routine is stopped. There is no comparison and no Spearman ρ today.

## What the numbers are not

- **The expected return.** `expected_return_pct` (and `expected_edge_pct` on a selected name) is what names at that percentile have earned in the past. Its out-of-sample record is weak: a correlation of +0.12 with the realised return over 148 names. It is not a forecast to size on.
- **The weights.** They are research. Only the linear `panel_pct − 60` rule in `execution.panel` trades.
- **Certainty.** `p_up` is recorded and decides nothing; it did not predict on the development names.
- **Fact-checking.** Nothing checked the searchers' findings for factual errors.
- **Reproducibility.** The key is not reproducible to better than its own size.
- **The searcher's key.** No name clears the 2.8 floor; OTLY +2.20 is the largest. Below the floor the sign is a coin flip on the evidence so far.
- **Sign balance.** The searchers leaned 8 positive and 11 negative, with REPL at zero.
- **Option chains.** Most chains were thin. ENPH, OI, INTA and UCTT had usable implied moves, and the others fall back on historical medians.

## Context: retail, search and volatility (not used for selection)

These labels are context only: nothing ranks, selects or sizes on them. They are the last three columns of the searcher table in the closing reply, from `edge-context.json`. Among the selected names:
- BOOM, OI, ENPH, LUNG and KIDS are retail ≥ 50.
- RBBN is retail ≥ 50 and vol ≥ 58.
- Search attention was too sparse to read for all six.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
