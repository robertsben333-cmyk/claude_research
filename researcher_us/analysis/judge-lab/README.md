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

**Pooled, not per day** (changed 2026-10-01 after the first reading, on the operator's
correction: per day, a four-name day always trades one name, which dilutes exactly the
top the book is about). Within each bucket (US or not, before or after the 09-23 scale
change) the names with the largest |score| up to 10, 15 or 20% of the bucket are traded
on the sign. The bucket exists because the hunter's scale moved on 09-23; an absolute
threshold would select one era. The per-day figures are still in the JSON. Reported: picks, hits, mean return gross and net of an assumed cost by
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

## Round 1 of agent judges (2026-10-01)

Three judges written as skills in `judges/`, one shared output contract
(`judges/_contract.md`: direction, certainty 0-100, and the book trades the top ~15% by
certainty):

- **rubric**: a fixed checklist per evidence item (fact, window, line, new, size) and a
  pre-mortem. No outcomes.
- **casebook**: studies ~125 resolved cases from the OTHER two folds of days, with their
  outcomes, then judges by analogy.
- **learned**: a learner agent writes its own SKILL.md from those cases
  (`judges/learned/skill-fold<k>.md`, 9 to 14 counted rules); a fresh judge applies it
  without seeing the cases. The closest thing to training the judge.

`folds.json` puts the 187 development days into three folds, by whole day, no outcome
read; each judge is scored on folds it never learned from. 27 judge agents, Opus, Read
and Write only. `python3 judge_lab.py compare` prints the table; `compare.json` holds it.

Top 15%, all regions, 187 names, net of the assumed cost, p from a within-day shuffle:

| arm | top 10% | top 15% | p | top 20% |
|---|---|---|---|---|
| live `impact_sum` | 12/16 +2.28% | 15/25 +1.59% | 0.09 | 19/34 +1.04% |
| re-judge Sonnet 5.5 (hunter core, other session) | 13/16 +5.92% | **20/25 +6.87%** | 0.00 | 25/34 +4.78% |
| re-judge Opus 5 | 13/16 +6.18% | 18/25 +5.42% | 0.00 | 24/34 +3.63% |
| re-judge Opus 5.5 | 11/16 +2.28% | 17/25 +2.38% | 0.10 | 22/34 +2.71% |
| judge casebook | 13/16 +5.16% | 19/25 +2.83% | 0.12 | 23/34 +1.60% |
| judge rubric | 12/16 +3.49% | 16/25 +2.35% | 0.04 | 21/34 +1.00% |
| judge learned | 10/16 +1.03% | 16/25 +0.88% | 0.12 | 19/34 −1.00% |

Shorting every one of these names returns −0.77% net, so no arm is riding the drift.

**What it says.** Teaching the judge from outcomes did not help on this sample: the
learned skill is the worst arm and the casebook is middling. The two best arms are plain
re-judges under the existing hunter core, on a different model than the one that hunted
(Sonnet 5.5, Opus 5). The agent judges also tilt hard short (learned 20 of 25 picks,
casebook 18), which their skills did not ask for; the learned rules read like a fit to
the cases ("a crowded short points up", "proxies are anti-informative") and did not
transfer.

**What it does not say.** Seven arms on one sample: the best one is chosen after the
fact. Twenty-five picks per arm; a 5-point gap between two arms is about one standard
error. The re-judges and the judges overlap on only 10 to 14 of 25 picks, so they are
picking genuinely different names. Every subagent loads CLAUDE.md, which quotes results
from these same days, for every arm alike. And the casebook leaks across days: a
Europe case on 09-30 mentioned a US name's 09-29 result that one casebook judge was
judging (it flagged it and held that name at certainty 20, outside the top). A
walk-forward casebook (only days before the judged day) closes that, at the cost of
fewer cases for the early days.

**Next.** (1) Run the leading arms forward on the days after 2026-10-01 rather than
adding arms here. (2) If more arms are tested, fold the re-judge prompt into this
contract (a certainty field) so they compete on one footing. (3) Open the test set once,
for at most two arms.
