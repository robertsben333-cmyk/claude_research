# Stage E — what the edge hunt's output actually measures

One resolved run: `research/2026/08/2026-08-31/edge`, eight rankable names. Run 1 of the
same day (`edge/_run1-bmo/`) contributes nothing measurable — its scores are a `--legacy`
re-score with substituted midpoints, and only 9 of its 28 findings were ever judged.

Nothing here is significant. Every permutation p-value below is above 0.09 and n is eight.
What the numbers do support is an ordering *between candidate rankers* built from the same
run's own files, and that ordering is consistent enough to act on before more days pool.

## The scorer's transformations subtract signal

Spearman against the realised move, same eight names, same day. Permutation p, 20k draws.

| ranking key | ρ | p |
| --- | --- | --- |
| hunt's own `expected_move_pct` (field the scorer never reads) | +0.635 | 0.09 |
| `priced_lean_pct` — baseline only, no hunting | +0.619 | 0.12 |
| minus 20-day run-up — free, no research at all | +0.619 | 0.12 |
| sum of finding residuals, before any multiplier | +0.595 | 0.13 |
| sum of finding impacts, before the adversary | +0.548 | 0.17 |
| cluster-max then ÷√k | +0.452 | 0.27 |
| **`edge_score` as shipped** | **+0.333** | **0.43** |
| `baseline_quality` alone | +0.386 | 0.35 |
| `confidence` | +0.359 | 0.38 |
| number of findings | +0.024 | 0.98 |

Read down the middle of that table: every stage of the aggregation lowers ρ. Residual sum
0.595 → cluster-max and √k discount 0.452 → agreement discount and quality multiplier
0.333. The machinery in `scripts/edge_score.py` is not adding ordering to the raw
evidence; on this day it removed it.

Two of the three best rankers cost nothing. `priced_lean_pct` is computed from the sealed
baseline before a single hunter is spawned, and for six of the eight names it is not a
skew calculation at all — with no option chain it falls back to `-0.05 × run_up_20d_pct`,
so "whatever ran up most in the last month fell hardest" ordered the day better than 51
findings and a full adversary pass. That control belongs in `edge_resolve.py`'s output as
a mandatory column. Until the hunt beats it, the hunt has not been shown to do anything.

## The ordering rests on one name

Leave-one-out on `edge_score`:

| dropped | ρ on remaining 7 |
| --- | --- |
| YEXT | +0.536 |
| HMR | +0.500 |
| NIO | +0.393 |
| MDT / MMED | +0.321 |
| ZEPP | +0.250 |
| CANG | +0.214 |
| **RZLV** | **+0.071** |

Drop RZLV and the ranking is noise. RZLV is the name with the *worst* baseline quality in
the run (0.07) and the lowest confidence (5.0) — the two fields whose job is to tell a
reader which names to trust. A consumer selecting on confidence would have taken MDT
(50.1, the only well-documented name) and discarded the one name carrying the result.

## The adversary judges well and sizes redundantly

Execution was clean: 51 of 51 findings judged, `priced_in_pct` spread from 18 to 92 with a
median of 72 and no bucket pile-up. That is the run-1 category collapse genuinely fixed.

But the adversary also returns `size_check_pct`, and `edge_score.py` averages it with the
hunter's number on the stated grounds that "where the two disagree badly the disagreement
is information". They do not disagree: median gap 0.50pp across 51 findings, one sign flip
in 51. The averaging is a rubber stamp. Whatever the adversary is worth, it is worth it
through `priced_in_pct`, and the size average should be dropped or the disagreement
recorded and left out of the score.

Note also that `priced_in_pct` cannot change a finding's sign, so the finding-level
direction rate is the hunters' alone: **33 of 51 (65%)** match the sign of their company's
realised move, identical before and after the adversary pass.

## Magnitude is signed right and scaled wrong

The `expected_move_pct` the hunters volunteer — a summary forecast the scorer discards —
got the sign right on 8 of 10 hunts and 6 of 8 names, and under-scaled every one of them:

| ticker | hunt forecast | realised | ratio |
| --- | --- | --- | --- |
| YEXT | −3.5% | −3.55% | 1.0× |
| ZEPP | −3.0% | −6.64% | 2.2× |
| RZLV | −4.0 / −4.5% | −17.30% | 4.1× |
| HMR | −2.6% | −10.79% | 4.2× |
| MMED | +1.5 / +2.0% | +10.66% | 6.1× |
| CANG | −3.5% | −23.01% | 6.6× |
| MDT | −0.5% | +1.53% | wrong sign |
| NIO | +1.8% | −4.02% | wrong sign |

Median under-scaling on the correctly-signed names: **4.1×**. This is the same bias
`backtest/RESULTS.md` measured on all three arms and `claude_naive/README.md` warned about
— seven of the eight biggest movers forecast under, several by half. Two independent
experiments now show it, which makes it the most reproducible property of the whole repo.

The shipped `edge_pct` is worse than under-scaled, it is a different unit: +0.04 to −0.58
points of spot against realised moves of 1.5% to 23%. `edge-note.md` says so plainly and
tells the reader not to read −11.5 as a forecast. Fine for a rank-only measure, but the
docstring's "the residual the market has not priced, in points of spot" is not what the
field contains.

## The normalised correlation is mislabelled

`edge_resolve.py` reports `spearman_vs_move_over_implied` and the docstring calls it "the
skill measure … dividing out how much each name was ever going to move". For five of the
eight names there is no option chain, and the divisor falls back to
`baseline.expected_move_pct`, whose own basis field reads `median historical reaction (no
usable option chain)`. So 0.381 is mostly a history-median normalisation, not an implied
one. Rename the field or restrict it to names with a chain.

## What one run costs

20 of 20 subagents (the whole `budget.subagent_caps.edge_hunt`), 227 unique sources across
ten hunts, 187 more in the adversary pass, 3,397 recorded adversary interactions — for
eight ranked names, of which PXS was shed for budget and RGS killed for an unconfirmable
date. The sweep confirmed 9 of 10 names from a company source, which is the part of the
stage that demonstrably works.

## What to change before the next run

1. Score on the sum of finding residuals. Keep `edge_score` as a secondary column until a
   pooled sample says the multipliers earn their place.
2. Carry the hunters' `expected_move_pct` into `edge-scores.json` and resolve it. It is the
   best ranker in the run and it is currently thrown away.
3. Add `-run_up_20d_pct` and `priced_lean_pct` as mandatory control columns in
   `edge_resolve.py`. A run that does not beat them has not established anything.
4. Drop the hunter/adversary size average; record the disagreement separately.
5. Rename `spearman_vs_move_over_implied`, or compute it only where a chain exists.
6. Stop reading `confidence` and `baseline_quality` as reader guidance until they correlate
   with something. On this run they pointed away from the only informative name.
