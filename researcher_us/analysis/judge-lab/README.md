# Judge lab: which way of scoring the findings gets the top 20% right

Started 2026-10-01. Question: given the findings a hunter has collected, is there a way
of turning them into a score that picks the right names for the **top ~20% of each
day** better than the live `impact_sum`? The other 80% is not the target, because the
book only ever trades the top.

`judge_lab.py` is the harness. It does not hunt and calls no model.

## Data and split

- 231 resolved, hunted names (US 154, Europe 48, Australia 16, Japan 13), taken from
  `../rejudge-full-2026-10-01/key.json`: the live hunter's findings with its own
  sizes, the sealed baseline and the realised move (US: the strategy exit, $200k
  turnover floor; elsewhere the market's resolver window).
- **Split by whole days, frozen in `split.json`**: train 141, validation 46, test 44
  names. Days that a LESSONS file was written from (US 09-08 to 09-14, Europe 09-16,
  09-19, 09-22, 09-28, Japan 09-11 and 09-18) are forced into train, because the hunter
  has already learned from them. The rest was assigned by a seeded shuffle balanced on
  name count, without reading any outcome. `split` refuses to redraw it.
- **The test set is sealed.** `score` only prints it with `--unseal <variants>`, and
  every unseal is appended to `TEST-LOG.md`. It is meant to be opened once, for the
  variants chosen on train and validation. It has not been opened.

## The metric

Per day, the `max(1, round(0.2 x n))` names with the largest |score| are traded on the
sign of the score. Per day and not on one absolute threshold, because the hunter's scale
moved twice (Opus 5.5 on 09-23, the shared core on 10-01) and a pooled threshold would
select one era. Reported: picks, hits, mean return gross and net of an assumed cost by
turnover band, t, and for the leave-one-day-out column a permutation p (the share of
within-day shuffles of the scores whose top 20% does at least as well).

## Variants tested so far

| variant | what it is | fitted? |
|---|---|---|
| `live` | the `impact_sum` the hunt emitted (the book today) | no |
| `signed_max` | only the largest finding, signed | no |
| `net_count` | findings up minus findings down | no |
| `sum_ge1` | `impact_sum` over findings of at least 1 point | no |
| `no_positioning` | `impact_sum` without positioning/short-interest findings | no |
| `per_implied` | `impact_sum` over the move the market expects | no |
| `agree_runup` | x1.5 where the sign agrees with minus the 20-day run-up, x0.5 where not | no |
| `cat_weights` | a weight per finding category from its train hit rate | yes |
| `ridge_signed` | ridge regression of the move on signed features | yes |
| `selector` | keeps the hunt's sign, learns which names to trust (logistic) | yes |
| `rejudge_opus`, `rejudge_sonnet` | the blinded re-judges on the same evidence | no |
| `ctrl_runup`, `ctrl_short` | free controls | no |

## First reading (all regions, leave-one-day-out over train + validation, 33 picks)

| variant | hits | net per pick | p |
|---|---|---|---|
| `signed_max` | 20/33 | +2.33% | 0.04 |
| `sum_ge1` | 19/27 | +2.14% | 0.08 |
| `no_positioning` | 19/33 | +1.68% | 0.09 |
| `agree_runup` | 19/33 | +1.37% | 0.08 |
| `selector` | 19/33 | +0.49% | 0.11 |
| `live` | 18/33 | −0.10% | 0.31 |
| `ridge_signed` | 17/34 | −2.21% | 0.60 |
| `ctrl_runup` | 16/34 | −2.88% | 0.89 |

US only and outside the US separately: `results-us.json`, `results-ex_us.json`.

## What this does and does not say

**Nothing here is a result.** The best p is 0.04 out of fourteen variants, so after
paying for the choice it is not significant. The validation set holds eight picks.

**The fitted models overfit, visibly.** `selector` scores 20/25 in train and +0.49% out
of sample; `ridge_signed` goes from +2.39% in train to −2.21%. With about 190 names,
anything with more than one or two free parameters learns the sample.

**The simple rules lean one way, and that way is a hypothesis worth carrying forward.**
The three that do best all throw information away: keep only the largest finding, drop
the small ones, drop the positioning findings. That fits what the repo already measured
(the scorer's aggregation was subtractive in September), but it was chosen on these
same days.

**The data is the bottleneck, not the method.** The US move has a standard deviation
of 10.6 points. Telling a +3 point edge per pick from zero takes about 77 top picks at
80% power, which at 20% is about 385 tradable US names: three times what exists.
Telling two variants apart takes more. Outside the US it is about 33 picks, but those
days are few and partly validation days.

## Next steps

1. **Freeze a short list and run it forward**, as the real test: `live`, `signed_max`,
   `sum_ge1`, `no_positioning`. Fixed rules, no parameters, computable from any new
   hunt. Every resolved day after 2026-10-01 counts toward it.
2. **Model judges with different prompts** can be tested on the same split:
   `judge_lab.py packs --split val --out <file>` writes the blinded packs for one split,
   a judge session writes `out-<pack>-<variant>.json` in the re-judge format, and the
   harness scores it like any other variant. A judge that is given the train days
   with their outcomes as worked examples is the direct form of "training the judge".
   Expect validation to be too small to decide it; the comparison has to pool forward.
3. Open the test set once, when the short list is final.
