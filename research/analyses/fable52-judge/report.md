# Fable 5.2 as a panel judge on US E-P evidence

Trial of 9 November 2026. Research only, not investment advice. Trial output: never pool it with live E-P runs.

## The short answer

Fable 5.2 judges the evidence almost the same way the four live judges do, and on 194 resolved names it shows no measurable ranking power. Its largest scores lean positive, as the live panel's do, but nothing reaches significance. There is no case yet for adding it to the panel or for trading on a Fable 5.2 boundary. If you want a provisional line to follow forward, it is a long call at impact_sum of +2.5 or more.

## What was done

- **Sample.** The ten most recent resolved US E-P days, 26 October to 6 November: 199 judged names, 194 resolved. The five withdrawn names of 28 October are out. Versions are kept apart: us-panel.v3 has 139 names over 7 days, us-panel.v2 has 55 names over 3 days.
- **Judge.** One judge run per day, pinned to claude-fable-5-2 at high effort (every run reported that model id). Each run saw only that day's blind pack, the same file the live judges read, plus the judge rules, hunter definition and lessons file as they stood in git on that run day.
- **Returns.** The scorebord's windows: entry 13:30 ET on the run day, amc out at the next open, bmo out at 13:00 ET. Gross, no costs.
- **Tests.** Within-day Spearman with a within-day permutation p, and the return of trading the sign, with a t per name and a t over day means.

## Finding 1: Fable 5.2 is a near copy of the existing judges

| Fable 5.2 against | Spearman | Same sign |
| --- | --- | --- |
| Fable 5.1 | +0.84 | 85% |
| Opus 5.5 | +0.86 | 86% |
| Opus 5 | +0.80 | 82% |
| Sonnet 5.5 | +0.81 | 85% |
| Live panel percentile | +0.89 | 87% |

The live judges agree with each other at about the same level (Fable 5.1 against Opus 5.5 is +0.89). On all 43 live strong calls Fable 5.2 took the panel's side. Its sizes are close to Fable 5.1's: median |impact_sum| 1.00, top 20% from 2.20, top 10% from 3.07. Its p_up ran from 31 to 66.

## Finding 2: no measurable ranking power

Within-day rank correlation of the signed score with the stock's move:

| Judge | v3 (n 139) | v2 (n 55) | Both (n 194) |
| --- | --- | --- | --- |
| Fable 5.2 | +0.02, p 0.82 | +0.05, p 0.70 | +0.03, p 0.68 |
| Fable 5.1 | +0.05, p 0.60 | +0.07, p 0.63 | +0.05, p 0.48 |
| Opus 5.5 | +0.12, p 0.18 | +0.02, p 0.91 | +0.09, p 0.22 |
| Opus 5 | +0.09, p 0.34 | +0.02, p 0.88 | +0.07, p 0.37 |
| Sonnet 5.5 | −0.06, p 0.53 | −0.02, p 0.89 | −0.05, p 0.55 |
| Live panel | +0.08, p 0.36 | +0.01, p 0.92 | +0.06, p 0.40 |

No judge ranks these ten days, and Fable 5.2 is not ahead of the others. Trading every Fable 5.2 sign returned +0.63% a name (n 192, 48% right, t 0.69). The "both" column pools two versions only to show the total; judge each version on its own column.

## Finding 3: the big scores lean positive, not significantly

Side taken from the sign of Fable 5.2's impact_sum, all 194 names:

| Size of score | n | Mean return | Right | t |
| --- | --- | --- | --- | --- |
| below 1 | 94 | −0.55% | 43% | −0.46 |
| 1 to 2 | 49 | +0.61% | 55% | 0.41 |
| 2 to 3 | 26 | +2.37% | 50% | 0.66 |
| 3 or more | 23 | +3.52% | 52% | 1.29 |

The order is right and the hit rate stays near a coin flip, so the mean rests on a few large winners. The direction matters: long calls at +2 or more returned +3.82% (n 35, t 1.54), short calls at −2 or less +0.64% (n 14, 36% right).

## Boundaries

For v3 the threshold was chosen on 29 October to 3 November (80 names) and tested on 4 to 6 November (59 names).

- Development: every threshold below 2.5 lost money; 2.5 or more gave +3.78% (n 12, t 1.37). That is the chosen line.
- Holdout: 2.5 or more gave +5.81% (n 11, 55% right, t 0.86). Names below the line gave +2.57% (n 47), so those three days were good for everything and the gap of about 3 points is not established.
- v2 (3 days, in sample only): 2 or more gave +5.26% (n 17, t 1.65).

Provisional boundaries, to be measured forward and not traded:

| Fable 5.2 impact_sum | Reading |
| --- | --- |
| +2.5 or more | Candidate long call. All ten days: n 24, +5.30%, 62% right, t 1.93. |
| between −2.5 and +2.5 | No call. Returns around zero. |
| −2.5 or less | No call. n 8, 38% right. |

The live rule on the same names, panel 80 or more with four judges: v3 n 25, +1.37%, t 0.55; v2 n 18, +3.54%, t 1.22. Opus 5.5's own top 20% did best in both versions (v3 n 27, +5.53%, t 1.88), which is one of several judges looked at and equally unproven.

## What weakens these numbers

- **Too small.** A 3-point edge on calls with a spread of about 15 points needs roughly 100 strong calls for t 2. There are 24.
- **One judgement per name.** Earlier work found that the same judge model re-run on the same evidence agrees with itself only at ρ 0.54 to 0.69. A single pass cannot separate Fable 5.2 from that noise.
- **Possible leak on a few names.** The judge agents may have had project notes in context that mention seven sample tickers, some with their outcome (LIFE, TREE, CRCT among them, all three large Fable 5.2 long calls and also live strong calls). Without those seven, the 2.5 line gives +3.54% (n 28, t 1.16) and the rank correlation is −0.01.
- **Not point in time on scale.** Fable 5.2 has no history, so "top 20%" is read on this same sample.
- **Gross returns.** Spreads on thin names are not in here.

## Recommendation

1. Do not swap Fable 5.2 into the live panel on this evidence. It adds a fifth opinion that is 0.85 correlated with the other four.
2. If you want to keep measuring, add it as a shadow judge scored on a dry run, so its percentile gets a point-in-time history and the +2.5 long line is tested forward. That costs one extra judge run a day.
3. A cheaper and more telling test first: run Fable 5.2 a second time on these same ten days. If the two passes agree at only 0.6, the judge model matters less than the noise in a single pass, and the next step is averaging passes, not choosing models.

Files: `results.txt` (all tables), `rows.json` (one row per name with every judge's score and the move), `judgements/` (Fable 5.2's raw output per day), `scripts/`.

## Addendum: each judge's own top 20% and top 30% (same 194 names, 10 days)

Side from each judge's sign, gross, t per name. "Own top" means that judge's largest |impact_sum| over this sample (the live panel uses its percentile). Choosing the cut on the same sample is in-sample for every row.

| Judge | Top 20% n | Mean | Right | t | Top 30% n | Mean | Right | t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fable 5.2 | 40 | +2.40% | 48% | 1.01 | 58 | +2.02% | 50% | 1.02 |
| Fable 5.1 | 38 | +2.71% | 53% | 1.22 | 57 | +3.39% | 56% | 1.91 |
| Opus 5.5 | 38 | +5.42% | 55% | 2.32 | 57 | +3.86% | 53% | 2.26 |
| Opus 5 | 41 | +3.22% | 59% | 1.91 | 59 | +3.79% | 61% | 2.23 |
| Sonnet 5.5 | 37 | +4.62% | 54% | 1.93 | 56 | +2.50% | 52% | 1.38 |
| Live panel pct | 39 | +2.76% | 49% | 1.40 | 59 | +3.16% | 54% | 1.80 |

Long side only: Fable 5.2 top 20% +3.32% (n 28, 54% right), top 30% +3.13% (n 40). The others, top 20% / top 30%: Fable 5.1 +7.15% (n 19) / +6.89% (n 31), Opus 5.5 +6.51% (n 25) / +5.00% (n 37), Opus 5 +5.91% / +5.08%, Sonnet 5.5 +5.22% / +2.59%, live panel +5.80% / +5.10%.

Fable 5.2 is the weakest of the six in both cuts. Fable 5.2's top 20% by side: longs +3.32% (n 28), shorts +0.25% (n 12, 33% right). In its top 20% the worst call was MPAA (−25.7%) and the best was a short that rose 53.8% (SOC), so single names move these means a lot. None of the gaps between judges is established: they share the same 194 names and the same ten days.
