# Stage E-P, October: do the highest average panel sizes pay?

**Question (operator, 2026-10-14).** Drop the 3-of-4 rule for this read. Put the four
judges on one scale, average them per name, and ask the usual question: if we trade every
name whose average is at or above a threshold, what does it return, and how many names is
that?

**Method.** `panel_mean_pct.py`. Only stage E-P runs from October (the September Opus 5.5
hunts are left out on the operator's instruction, so `panel-history.json`, which was seeded
from re-judges of those hunts, is not used). Each model's `impact_sum` is multiplied by a
factor that brings its median |size| over the 44 October names to the mean of the four
medians: Opus 5 x0.64, Opus 5.5 x1.33, Sonnet 5.5 x1.53, Fable 5.1 x0.97. No outcome is used
to set the scale. The four rescaled sizes are averaged into `avg_pct`. For every threshold,
the resolved names at or above it are traded on the sign, equal weight, gross, at two exits
from `dashboard/data/ledger.json`: close to close and the strategy exit.
`build_chart.py` renders `panel-mean-pct.html`.

**Result, 35 resolved names over six days (10-05 to 10-12).**

| threshold on \|avg\| | names | close to close | se | right |
|---|---|---|---|---|
| 0 (every name) | 35 | +1.84% | 1.24 | 57% |
| 0.5 | 23 | +3.38% | 1.45 | 61% |
| 1.0 | 13 | +2.82% | 2.15 | 54% |
| 1.5 | 9 | +5.56% | 2.36 | 67% |
| 2.0 | 5 | +4.29% | 3.42 | 40% |

Shorting every name with no research: +1.17%. The current 3-of-4 rule: 5 names, +5.93%.

**What it does not show.** Six days and 35 names; every point above 1.5 rests on nine
names or fewer and its band includes the short-everything line. The curve was read across
every threshold, so the best point on it is the optimistic one. Gross of costs. The 10-13
run (9 names) was unresolved when this ran.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
  python3 research/analyses/panel-mean-pct/build_chart.py
