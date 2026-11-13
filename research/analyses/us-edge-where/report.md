# Where does the US panel work? (stage E-P, 14 Oct to 12 Nov 2026)

Built 2026-11-13. Rows: `rows.json` (from `build.py`), all cuts: `results.txt`
(`analyse.py`), difference tests: `tests.txt` (`tests.py`).

## Sample and rules

- 400 resolved stage E-P names with all four judges. **us-panel.v2**: 186 names, 11 run
  days (14 to 28 Oct). **us-panel.v3**: 214 names, 11 run days (29 Oct to 12 Nov). The two
  versions are never pooled; every number below is per version.
- Return = the operator's window on the panel's side, gross: in at 13:30 ET, amc out at
  the next open, bmo out at 13:00 ET. No spread, no costs.
- p-values are two-sided sign-flip or permutation tests. About 60 cuts at three score
  levels were looked at, so a single p near 0.05 is expected by chance several times
  over. Nothing here survives a multiplicity correction.
- "In-sample" below means the cut was read off these same 400 names. Because both
  versions were on the table at once, a cut that holds in both is a replication across
  two disjoint periods, not a clean out-of-sample test. The clean test is the runs
  from 13 Nov onward.

## The base picture

| | v2 | v3 |
|---|---|---|
| ranking, within-day rho of signed panel_pct vs move | -0.14 (p 0.10, n 186) | +0.08 (p 0.27, n 214) |
| all names, per name | -0.80% (t -1.40, p 0.17) | +1.40% (t 1.76, p 0.09) |
| panel_pct >= 60, per name | +0.08% (n 75, p 0.94) | +3.45% (n 79, t 2.42, p 0.016) |
| panel_pct >= 80 (the live book), per name | -0.64% (n 39, p 0.74) | +2.84% (n 34, t 1.34, p 0.17) |
| panel_pct >= 80, per day | +0.78% (11 days, t 0.35) | +3.41% (11 days, t 1.59) |
| short everything | -0.35% | -0.29% |

The panel does not rank the day in either version. v3 earns on its higher scores, v2
did not. The 60-80 band is positive in both versions (+0.86% n 36, +3.92% n 45) and is
no worse than the 80+ band the book buys (difference +1.5 and +1.1 points, p 0.51 and
0.72).

## Hypotheses from this sample (all in-sample)

**H1. Size: the panel works on small and mid caps ($0.3bn to $10bn) and not on large
caps.** At panel_pct >= 60: v2 +3.46% (n 39) against -3.58% for the rest (n 36),
difference +7.0, t 3.37, p 0.002; v3 +4.48% (n 62) against -0.29% (n 17), difference
+4.8, t 1.66, p 0.17. On all names: v2 +1.9 points (p 0.09), v3 +4.2 points (t 2.54,
p 0.02). Large caps above $10bn lose in both versions on all names (-1.78% n 70,
-2.10% n 43). Micro caps under $300m are negative in both, n 21 and 12, too few to say.
Same sign in both versions; the strongest candidate here. Checked on the old stage E
hunter sample (us.v4, us.v9): not confirmed there (n 9 to 31 per cell, signs mixed), so
it is a claim about the panel, not about the method in general.

**H2. Share price $10 to $50.** At >= 60: v2 +3.81% (n 25) against -1.78%, p 0.014; v3
+4.56% (n 33) against +2.90%, p 0.59. At >= 80 it is +6.7% in both (n 10 and 16).
Overlaps heavily with H1 (large caps are mostly above $50); treat as the same effect.

**H3. The panel's side agrees with the last five days' move.** With the 5-day move:
v2 +0.09% against -1.68% (all names, p 0.12), v3 +2.79% against +0.56% (p 0.17); at
>= 60 the gap is +2.9 and +2.8 points (p 0.21, 0.34). Same sign four times, never
significant. Too small to tell.

**H4. Strong shorts do not pay.** panel_pct >= 80 shorts: v2 -2.18% (n 14), v3 -0.62%
(n 17); longs +0.22% (n 25) and +6.30% (n 17). Long minus short +2.4 (p 0.54) and +6.9
(p 0.11). At >= 60 the v3 shorts are fine (+3.84%, n 37), so this is about the top
band only. Too small to tell; same direction as the Fable 5.2 judge trial.

**H5. A liquid option market helps.** Names with a usable chain: v2 -0.59% against
-1.27% without (p 0.59); v3 +2.14% against -0.65% (p 0.12). At >= 60 with an implied
move of 10% or more: v2 +3.44% (n 28) against -3.07% (p 0.023), v3 +4.39% (n 51)
against +2.39% (n 12, p 0.65). Same sign, one significant cell.

**H6. Technology is the weak sector.** All names: v2 -1.32% (n 31) against -0.70%,
p 0.68; v3 -1.15% (n 58) against +2.34%, p 0.05. See the out-of-sample section: this
one was stated before.

Things that looked like something in one version and were absent or reversed in the
other, so no hypothesis: bmo shorts (v2 -5.33% at >= 60, n 13, p 0.008; v3 +5.63%),
Wednesday (v2 -2.99%, p 0.004, which is the 21 Oct run; v3 -0.31%), session (amc
against bmo flips sign), realised volatility above 58, weekday in general.

## Earlier hypotheses, tested on runs they were not fitted on

These were written down on stage E's September runs (the dashboard's Hypotheses tab,
CLAUDE.md) or in a later trial. Stage E-P and its key are different, so this asks
whether the pattern carries over, per version.

| earlier claim | v2 | v3 | verdict |
|---|---|---|---|
| A higher score is right more often (rho of score vs sign right; was +0.51) | +0.03, p 0.74 | +0.04, p 0.56 | not replicated |
| The floor separates: at or above it against below (panel_pct 80) | +0.2 points, p 0.89 | +1.7 points, p 0.43 | not replicated |
| The free control, minus the 20-day run-up, ranks the day (was +0.34) | -0.06, p 0.49 | 0.00, p 0.95 | dead |
| Shorting everything pays (was +1.6% a name) | -0.35% | -0.29% | dead |
| Pays more where the side agrees with the sealed price lean | >= 60: +3.6 points, p 0.10; >= 80: +9.9, p 0.007 | >= 60: -1.1, p 0.71; >= 80: -2.3, p 0.59 | replicated in v2, reversed in v3 |
| High retail tilt pays above the floor | >= 60: +3.2 points, p 0.16; >= 80: +4.0, p 0.29 | >= 60: +0.7, p 0.85; >= 80: n 4 | right sign, too small |
| Technology is the weak sector | -0.6 points, p 0.68 | -3.5 points, p 0.05 | same sign in both; also -6.9 points (p 0.035) on stage E us.v4. The one earlier claim that keeps showing up |
| Consumer Cyclical carries the result | -0.7 points, p 0.72 | +0.5 points, p 0.83 | not replicated |
| bmo beats amc | -2.5 points, p 0.27 | +0.7 points, p 0.81 | not replicated |
| Raising the threshold lifts bmo and lowers amc | no | no (both rise) | not replicated |
| Volatility >= 58 raises the hit rate (frozen forward test) | 44% vs 47% | 56% vs 51% | too small |
| Longs work, shorts do not (Fable 5.2 trial) | >= 80: +2.4 points, p 0.54 | >= 80: +6.9 points, p 0.11 | same sign, too small |
| Search attention (Google Trends spike) hurts | not testable: 73 names measured, feeder stale | | open |

## What to do with it

1. Nothing in the live rule should move on this. The one thing with weight is H1, and
   it was found by looking.
2. Pre-register H1 now and score it forward on runs from 13 Nov: "at panel_pct >= 60,
   names with a market cap between $0.3bn and $10bn return more than the rest". At the
   current rate (about 5 such names a day) 20 trading days give roughly 100 names in
   the group, enough to see a 4-point gap at t near 2.
3. Per day, the candidate book "panel_pct >= 60 and $0.3bn to $10bn" made +2.42% a day
   in v2 (39 names, 10 days, t 0.93, 7 of 10 days up) and +5.78% in v3 (62 names, 11
   days, t 2.90, 9 of 11 up), against +0.78% and +3.41% for the live >= 80 book. In
   sample, gross, and the thin end of that band has wide spreads.
4. Costs are not in any number here.
