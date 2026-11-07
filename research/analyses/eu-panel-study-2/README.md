# EU panel study, round 2

As of 5 November 2026. This builds on the first study (21 October, PR #42, `/mnt/project-files/eu-panel-study/rapport.md`). Returns are signed by the panel's side (long when the panel says up, short when it says down). Unless a line says otherwise, the window is close(R−1) to close(R), where R is the reaction session: the event day for bmo names, the next day for amc names. Everything below the headline is exploratory.

## Short answer

**The panel now ranks Europe measurably.** Across 19 live panel days (event days 12 October to 5 November, 244 names), the panel's within-day ranking correlates with the move at ρ +0.20 (permutation p 0.003). On the 198 names the first study never saw (event days from 21 October), it is ρ +0.21 (p 0.006). The first study measured +0.22 with p 0.19 on 45 names, so the sign held and the sample grew enough to settle it. The free control (−run_up_20d) ranks at −0.04 (p 0.53), so the panel is not repeating it.

**The strong calls carry most of the return, but only just clear costs.** At the standing benchmark of panel ≥ 70 there are 44 calls: +3.03% gross per call, 66% right, t 2.41, p 0.020. Net of an estimated spread (Corwin-Schultz plus 0.10%) that drops to +2.00%, t 1.61, p 0.12. Grouped by day, which accounts for names on the same day moving together, the ≥ 70 book gives t 1.73, p 0.105 over 15 days. At ≥ 80 it is stronger: 26 calls, +4.13% gross, +2.98% net, and 12 of 13 days positive (day-clustered t 3.25, p 0.007). Treat ≥ 80 with care, because I picked it from four thresholds after looking at the data.

**Timing: close to close is still the right window, and the exit matters more than the entry.** Entering at panel time, in the last hour, or at the close changes the result by less than 0.2 points (paired difference +0.04, t 0.61). Exiting at the open gives up part of the move: on all names, holding to the close adds +0.54 points over selling at the open (t 1.90, p 0.058). For high scores the move seems to carry on into the next days (≥ 80: close R to close R+5 +4.47%, n 16, t 2.71), but that is a small sample and not yet a rule.

**Best strategy, said honestly.** Keep the rule fixed in advance and keep measuring it: panel ≥ 70 (or ≥ 80), enter at the close before the print, exit at the close of the reaction day. The out-of-sample test supports nothing beyond that. When I chose among 135 rule variants on the first half of the days, the ranking of variants did not carry into the second half (ρ −0.07). The first half's winner, "long only", earned nothing in the second half.

## What was measured

| | |
|---|---|
| Days | 19 live panel days, event days 2026-10-12 to 2026-11-05. 2026-11-06 is not out yet |
| Names | 268 panel-scored; 244 usable (4 neutral, 19 not priced or pending, 1 killed by the resolver: INISS_B, an amc name from today, which is pending anyway) |
| Prompt version | One: stage eu.v8, hunters uk.v7 / de.v7 / fr.v7 / nordic.v5 / it.v5 / es.v5 / pl.v5 on Opus 5.5 with the shared core, the same hunter, core and lessons blobs on every day. No pooling across versions |
| Left out | September Opus 5.5 runs and the 1 October uk.v5 run (house rule). 7 and 8 October are the same version but had no panel run |
| Panel | Live `edge-scores-panel.json`. For 10-12 to 10-14 the live files had no `panel_pct`, so the first study's dry-run rescore is used (12 names) |
| Prices | Yahoo 1d and 5m bars. Market control: STOXX 600 |
| Costs | Corwin-Schultz spread from the 20 sessions before the print (median 0.64% round trip, 0.74% under $1m a day, 0.44% above $25m), plus 0.10% fees. UK stamp duty on longs was tried too and changes almost nothing |

Sessions are bmo for 223 names and amc for 21. The resolver takes the hunter's session over the vendor's when the hunter cites a timestamp, which changed the session for 18 names.

## The resolver bug (ERIC_A, NDA_FI): fixed

The bug had two causes. Both are fixed in `researcher_europe/scripts/eu_archive.py` and covered in the smoke test.

1. **Nordea files under the Stockholm label.** NDA_FI is a Helsinki name, but its Q3 report of 15 October sits in the Nasdaq Nordic feed under "Main Market, Stockholm". The resolver only read the listing country's rows. A Nordic day now keeps all three Nordic markets; the Baltics and Iceland stay out.
2. **The feed writes names its own way.** Ericsson appears as `Ericsson, Telefonab. L M` and Industrivärden as `Industrivärden, AB`. The name normaliser turned the ä into a space. Confirmation now strips accents first and accepts abbreviations (`TELEFONAB` matches `TELEFONAKTIEBOLAGET`). If a day only carries a near-namesake (for example Nordea Hypotek), the result is "not a kill" instead of a kill.

I checked this against the real feed: ERIC_A and NDA_FI on 10-15, and INDU_A on 10-07, now resolve as reported. That 10-07 INDU_A kill was a third victim nobody had noticed. Every panel day was re-resolved with the fix (`resolved/`, kept here and not in the live run folders). After the fix the only panel name killed is INISS_B. Of the other kills in the resolver output, none is a panel name. I have not checked them by hand: DEMANT 10-14, REJL_B 10-22, SOLAR_B 11-04, and several UK names.

## 1. Where it seems to work

### Score bands (gross, close to close)

| panel_pct | n | mean | median | right | t | p | median abs move |
|---|---|---|---|---|---|---|---|
| control: everything long | 244 | −0.07% | +0.35% | 52% | −0.17 | 0.87 | |
| all names, panel side | 244 | +1.22% | +1.31% | 59% | 2.99 | 0.003 | |
| 0–30 | 100 | +0.58% | +0.83% | 56% | 0.89 | 0.38 | 3.1% |
| 30–50 | 41 | +1.90% | +2.36% | 63% | 2.59 | 0.013 | 2.9% |
| 50–60 | 33 | +0.52% | +0.45% | 52% | 0.52 | 0.61 | 3.6% |
| 60–70 | 26 | +0.47% | +0.79% | 58% | 0.49 | 0.63 | 3.4% |
| 70–80 | 18 | +1.43% | +2.02% | 56% | 0.67 | 0.51 | 5.8% |
| **80–100** | **26** | **+4.13%** | +3.15% | **73%** | 2.71 | 0.012 | 4.5% |
| ≥ 70 | 44 | +3.03% | +2.50% | 66% | 2.41 | 0.020 | |
| ≥ 70 minus STOXX | 44 | +2.88% | | 68% | 2.28 | 0.028 | |

Below 70 the bands are roughly flat at +0.5% per name. The 30–50 bump is most likely noise. The return sits at the top. The curve is not smooth: across all names the score's correlation with the signed return is only +0.10. High scores also find larger movers (median abs move 4.5% to 5.8% against about 3%).

The ≥ 70 result does not rest on one name or one day. Without its three best names it is still +1.81%. Leaving out any single day keeps it between +2.27% and +3.45%. The tails are wide in both directions: best PREV_B +20.6% and KNOW +20.0%, worst BHG −15.1% and ALLEI −13.0%.

### Long or short, session, period

| cut | all names | ≥ 70 |
|---|---|---|
| long | n 124, +1.14%, t 2.24 | n 19, +3.55%, t 1.66 |
| short | n 120, +1.31%, t 2.03 | n 25, +2.63%, t 1.73 |
| bmo | n 223, +1.13%, t 2.63 | n 39, +2.76%, t 2.04 |
| amc | n 21, +2.18%, t 1.69 | n 5, +5.13% (too small) |
| first half, event days 10-12 to 10-23 | n 103, +0.37%, t 0.56 | n 14, +2.51%, t 0.93 |
| second half, 10-26 to 11-05 | n 141, +1.84%, t 3.61 | n 30, +3.27%, t 2.39 |

Long and short both earn, while "everything long" earned nothing in this period. So the result is not a market tilt. The second half is clearly better than the first. Part of the reason: on the first days each judge had little European history to measure its own percentile against, so the scale was still settling.

### Country, sector, liquidity

Read every cell here as exploratory. With roughly 40 comparisons, two or three "p < 0.05" results are what chance alone would produce.

| country (all names) | n | mean | right | t |
|---|---|---|---|---|
| Sweden | 80 | +1.23% | 60% | 1.51 |
| Norway | 35 | +0.61% | 51% | 0.74 |
| UK | 34 | +0.63% | 53% | 0.65 |
| Germany | 26 | +2.30% | 62% | 1.61 |
| Finland | 22 | +2.73% | 64% | 1.83 |
| Spain / France / Italy / Denmark / Poland | 13 / 12 / 9 / 7 / 6 | +0.86 / +1.47 / −0.61 / +0.13 / +2.22% | | under 1.4 |

No country stands out significantly. Only Italy is negative, on 9 names. The ≥ 70 calls spread across Sweden (14), Norway (7), Germany (7), France (4) and Finland (4), with only 8 others. Sector shows no pattern either: the largest group, Finance (48 names), earns +0.76%. Groups that look good, such as Commercial Services (+3.85%, n 13) and Industrial Services (+3.94%, n 10), are too small to call.

By liquidity, the thinnest names (under $1m a day) do best gross (≥ 70: +4.14%, n 20). They also cost the most to trade (CS median 0.74%), so net the gap shrinks.

### The first study's leads, tested on the days it never saw (event days 10-21 to 11-05, 198 names)

| lead (from 21 Oct) | then (n 45) | now, new days only | verdict |
|---|---|---|---|
| volatile names (20d vol ≥ 40%) do better | +5.2%, n 6 | +2.78% (n 34) vs +1.27% below 40% | held, but the gap is not significant |
| low judge spread is better | +1.17% vs −1.38% | +1.52% vs +1.54% | did not hold |
| 4 of 4 judges agree is better | +0.58% vs −2.37% | +1.42% vs +1.89% | did not hold |
| short register (anchor) does not help | −1.18% vs +0.42% | anchor +0.65% (n 56) vs none +1.87% (n 142) | held, and the direction is the opposite of the design |
| 0–2 analysts weak | −4.6%, n 6 | +1.94%, n 12 | did not hold |

The anchor result is the most persistent finding across both studies. On all days, names whose short register reports a position earn +0.28% (n 70); names without one earn +1.60% (n 174). Among strong calls it is −1.00% (n 17) against +5.57% (n 27). It is not just volatility: with 20d vol under 40% it is −0.18% (anchor) against +1.19% (no anchor). But anchor coverage is tied to country (the UK and Germany have it far more often than Norway, Finland or Spain), so country and anchor cannot be separated yet. I would not act on this. It is the first thing to test as a pre-registered hypothesis.

## 2. How much do entry and exit times matter?

Entries are on the day before the print: the 5-minute bar at the moment the panel finished (about 14:00 to 16:20 UTC), 60 or 30 minutes before the close, and the close itself. Exits are on the reaction day: the open, then +15 minutes, +30 minutes, +1, +2, +4 and +6 hours after the official open, the close, and the closes of R+1, R+2 and R+5.

**Strong calls (≥ 70), mean signed gross %, intraday columns on the 40 of 44 names with a full 5-minute tape**

| entry \ exit | open R | +30m | +1h | +2h | +4h | +6h | close R |
|---|---|---|---|---|---|---|---|
| panel time D−1 | +2.02 | +2.13 | +2.10 | +2.28 | +2.20 | +2.33 | **+2.82** |
| last 60m D−1 | +2.02 | +2.12 | +2.09 | +2.27 | +2.20 | +2.32 | +2.81 |
| close D−1 | +1.85 | +1.97 | +1.94 | +2.12 | +2.04 | +2.17 | +2.65 |
| open R (enter after the gap) | | −0.03 | −0.12 | +0.10 | +0.05 | +0.12 | +0.64 |

**≥ 80 (25 of 26 names)**

| entry \ exit | open R | +30m | +1h | +2h | +4h | +6h | close R |
|---|---|---|---|---|---|---|---|
| panel time D−1 | +2.87 | +3.52 | +3.33 | +3.57 | +3.59 | +3.47 | **+4.01** |
| close D−1 | +2.49 | +3.15 | +2.97 | +3.21 | +3.22 | +3.10 | +3.64 |
| open R | | +0.42 | +0.14 | +0.46 | +0.50 | +0.31 | +0.90 |

**The move split into legs (signed, entry close R−1)**

| leg | all (n 244) | ≥ 70 (n 44) | ≥ 80 (n 26) |
|---|---|---|---|
| gap: close R−1 → open R | +0.68%, t 2.52 | +2.25%, t 2.42 | +2.68%, t 1.99 |
| session: open R → close R | +0.54%, t 1.88 | +0.66%, t 0.69 | +1.25%, t 0.93 |
| day 2: close R → close R+1 | +0.10% (n 225) | +1.65%, t 1.47 (n 38) | +2.84%, t 1.60 (n 23) |
| close R → close R+5 | +0.06% (n 166) | +2.33%, t 1.80 (n 29) | **+4.47%, t 2.71 (n 16)** |

What this means:

- **Entry barely matters.** Panel time, the last hour and the close sit within about 0.2 points of each other. Entering at panel time is slightly better for ≥ 80 (+0.42 points, t 1.83, p 0.08). That gain comes on top of an extra spread you may pay intraday, so a closing auction is the sensible default for these thin names.
- **Entering after the gap gives up most of the edge.** About three quarters of the strong calls' return arrives in the opening gap. Waiting for the open and then following the panel leaves only +0.6% to +0.9%, less than the spread.
- **Exiting at the open is the weakest choice, though no longer by a significant margin.** Across all names, holding to the close adds +0.54 points (t 1.90, p 0.058). The session leg is positive for bmo names (+0.57%, t 1.89). That is the same pattern as in the first study and in the US: a morning print keeps being priced through the day. For ≥ 70 the session leg is positive but noisy (t 0.69).
- **Holding longer is the open question.** For all names, day 2 adds nothing (+0.10%). For high scores the move keeps going (≥ 80 to R+5: +4.47%, 13 of 16 positive). It goes the other way from the first study's backtest, where day 2 reversed. That rests on 16 names, and the R+5 sample can only include events up to 29 October. Each extra day held also adds overnight risk and, for shorts, borrow cost. Measure it forward; do not switch yet.
- **amc names** (n 21) look different: most of their move is in the gap, plus a strong day 2 (+3.15%, n 20, t 1.61). They are too few to give them their own rule.

## 3. Costs

| book | gross | net CS + 0.10% | net flat 0.40% |
|---|---|---|---|
| all names (244) | +1.22%, t 2.99 | +0.36%, t 0.88 | +0.82%, t 2.01 |
| ≥ 60 (70) | +2.08%, t 2.38 | +1.14%, t 1.32 | +1.68%, t 1.92 |
| ≥ 70 (44) | +3.03%, t 2.41 | +2.00%, t 1.61 | +2.63%, t 2.10 |
| ≥ 80 (26) | +4.13%, t 2.71 | +2.98%, t 1.98 | +3.73%, t 2.44 |

Trading every name the panel scores does not pay after costs: the edge per name below 70 is smaller than the spread. Corwin-Schultz is an estimate from highs and lows on volatile days, not a quoted spread, and for the thinnest names it is probably too low rather than too high. No real fill has been measured in Europe. Stages EU, J, AU and CA place no orders, so every number here is a paper number.

## 4. The best strategy, with an out-of-sample check

I split the days in two: period A (event days 10-12 to 10-23, 103 names, 10 days) and period B (10-26 to 11-05, 141 names, 9 days). I built 135 rule variants (threshold 50/60/70/80 × filter: none, 4 of 4 agree, low spread, turnover above $1m, long only, short only, hunter agrees × exit: open, +1h, close R, close R+1, open→close), all net of costs, chose on A, and tested on B.

- **The in-sample choice did not carry.** The rank correlation between a variant's result in A and in B is −0.07. A's best, "≥ 70, long only, exit R+1" (+7.24%, t 3.04), earned +1.65% with 44% right in B. Every "long only" variant that topped A failed in B.
- **The only thing that holds in both halves is the plain threshold.** ≥ 70, close to close, net: A +1.35% (n 14), B +2.30% (n 30). ≥ 80 with exit at close R+1 did well in both (A +4.22%, n 9; B +6.74%, n 14, t 1.79), but that is one cell among 135.
- **Day-level book** (equal weight within a day, net, compounded, fully invested, not a feasible risk level): ≥ 70 exit close R +19.1% over 15 days with a call (t 0.93); ≥ 80 exit close R +56.5% over 13 days (t 2.33, p 0.038); ≥ 80 exit at the open +21.1%.

**My recommendation:**

1. **Keep the rule fixed and pre-registered:** panel ≥ 70, entry at the close before the print, exit at the close of the reaction day. Do not optimise filters yet. The out-of-sample test shows that the filters are where overfitting creeps in.
2. **Report ≥ 80 alongside it as the second line.** It is the US threshold, so it was not invented here, but it is the cell that looks best on this data. Treat it as a hypothesis for the coming weeks.
3. **Pre-register two hypotheses now so the next round tests them cleanly:** (a) names without a short-register position beat names with one, within the ≥ 70 calls; (b) for ≥ 80, holding to close R+5 beats close R.
4. **Before any real money:** measure real spreads on a few names (one paper fill or quote snapshot per name at the close), because costs decide whether ≥ 70 is worth trading.

## What this study cannot tell

- 19 days and one prompt version. Days are not independent of each other, and day-clustered tests are weaker than per-name tests (≥ 70: day t 1.73, p 0.105).
- The panel's percentile scale settled in the first week, so early days are not quite comparable with later ones.
- European pre-market does not exist as a usable tape; "open R" is Yahoo's first 5-minute bar. Spreads are estimated, not quoted.
- R+2 and R+5 are only available for the earlier part of the period.

## Files

- `collect.py` builds `dataset.json` (prices in `cache/`, not committed). `resolve_all.py` re-runs the resolver into `resolved/`. `analyse.py` writes `report.txt` (every table above, and more) and `results.json`. `extra.py` writes the robustness checks in `extra.txt`.
- Nothing in a live run, a panel history or the scorebord was written.

This is research, not investment advice.
