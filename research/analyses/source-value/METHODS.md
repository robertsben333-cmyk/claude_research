# Methods (frozen before any outcome is joined to the new labels)

Written 2026-10-05, committed with codebook v1 and before `scripts/core.py` reads a
single realised move against a v1 label. A change after that point is a new version
(`METHODS-v2.md`) reported beside this one, never an edit of this file.

## Units, outcome and horizons

- **Print**: one company's earnings event. Duplicate hunts of one print (the 09-04/09-07
  twins) count once: the non-duplicate hunt's items are used and the twin's are dropped.
- **Item**: one evidence item in a pack (stratum A and C: a filed finding, an item put
  outside the window, a rejected candidate, or a "searched, found nothing" note; stratum
  B: one cited claim of a dossier).
- **Outcome** `move_n = move / priced_move`, where `priced_move` is the option-implied
  move, else the baseline's expected move, else the median past reaction, floored at 1
  point (as in `../source-types/build.py`). **Winsorised at ±4** for every primary
  statistic (one print with a 30-point move against 3 priced would otherwise decide a
  cell); the raw value is reported beside it.
- **Horizons**. Primary: stratum A the strategy exit (amc at the open, bmo 20:00 CET);
  B close-to-close (the only one PREDICTIONS.csv carries); C the market's own resolver
  window. Secondary (A only): the open (`move_open`) and the close (`move_close`).

## The vote of an item

The labeller's `direction` (−1/0/+1) from two independent runs. Vote = sign of the mean
of the two runs (so a 1 and a 0 vote 1, a 1 and a −1 vote 0). An item with vote 0 enters
prevalence and magnitude, never a directional statistic.

## Usefulness metrics (Phase 2)

For a set of items (a subtype, optionally within a band, a flag or a context):

- **DV** (directional value): mean over voting items of `vote × move_n`. Reported with
  the hit rate (share of voting items with `vote × move > 0`) and n items / n prints.
- **DV\*** (drift-adjusted): mean of `vote × res_n`, where `res_n = move_n − naive_n`.
  `naive_n` is what a vote with no source earns in that name: the mean `move_n` of the
  same stratum and cap band (turnover band in C) plus a linear term in the 20-day run-up,
  both fitted **leaving the print's own day out**. A source that only says "down" in
  names that fall anyway scores zero.
- **MV** (magnitude value), name level: P(|move| / priced > 1 | the subtype is present
  in the name) minus the same probability where it is absent, within the stratum. A
  second form uses the item's `magnitude_claim`: names with a `large` claim against the
  rest.
- **MgV** (marginal value):
  (a) observational: among names where the four-model re-judge median (`median4`) is
      non-zero, the judges' hit rate where the subtype's net vote agrees with the
      judges' sign, minus their hit rate where the subtype is absent or disagrees;
  (b) ablation: below.
- **Prevalence**: share of prints in which the subtype appears (any item, voting or not).

The registry carries all of them; they are never collapsed into one number. **The
usefulness score is DV\*, shrunk**, with its 80% interval.

## Size bands (fixed before outcomes)

Market cap: micro < $300m, small $300m–2bn, mid $2–10bn, large > $10bn. Stratum A
counts (prints, de-duplicated): micro 57, small 37, mid 35, large 29; large has ≥ 15
prints, so the four bands stay separate. Separately: option chain yes / no; median
turnover < $1m / $1–25m / > $25m. Stratum C has no market cap and is banded by
turnover only. Stratum B is 14 large, 14 mid, 2 small.

## Strata

The registry's estimates are **stratum A** (US edge hunts). Stratum B (US dossiers, a
different method, mostly mid and large caps) and stratum C (Europe, Japan, Australia,
no option anchor anywhere) are **replication columns**, never pooled into A's estimate.
A pooled A+B column is reported for information where Cochran's Q between A and B for
that cell has p > 0.10; the verdict never rests on it.

## Statistics (Phase 4)

- **Permutation p**. Realised outcomes (`move_n`, or `res_n` for DV\*) are shuffled
  across prints **within each day** (`perm_day`), keeping every print's items together;
  2,000 shuffles for every question (seeded, `SEED = 20261005`). Two-sided p = share of
  shuffles with |stat − null mean| ≥ |observed − null mean|; z = (observed − null mean)
  / null sd.
- **Contrasts** (A against B inside one question) use the same shuffles on the
  difference.
- **Shrinkage**. Normal-normal empirical Bayes, top-down: group → overall, subtype →
  its (shrunk) group, subtype × band → its (shrunk) subtype. For each level, each child's
  raw estimate `y` has a cluster-robust standard error `s` (items summed within a print,
  prints as clusters); the between-child variance `τ²` is the DerSimonian–Laird moment
  estimate over the siblings (floored at 0). Shrunk = parent + B·(y − parent),
  B = τ²/(τ² + s²); posterior sd = sqrt(B·s² + (1 − B)²·sd_parent²). Cells with fewer
  than 3 voting items take B = 0 (the parent). 80% interval = shrunk ± 1.2816 · post sd.
  Standard library only.
- **Multiplicity**, all three reported: per-question permutation p; family-wise p within
  the batch (max-|z| over the batch, same shuffles); Benjamini–Hochberg q over every
  question answered in the ledger to date (recomputed after every batch, so an earlier
  q can rise). The report states the total number of questions tested.
- **Stability**. Leave-one-day-out for every registry cell: the cell's estimate on each
  day's items alone; the share of days (with ≥ 1 voting item) whose sign matches the
  full-sample sign.
- **Power**. Before each batch, every question carries the number of independent prints
  needed to detect a 10-point hit-rate gap at 80% power (two-sided α 0.05): about 196
  prints for a one-sample hit rate against 50%, about 392 per arm for a two-arm gap,
  inflated by the design effect 1 + (m − 1)·0.3 for m voting items per print. A question
  whose n is below that is marked `underpowered: true` and its p is reported but not read
  as evidence of absence.

## Verdict rules for the registry (frozen)

On stratum A's shrunk DV\* with its 80% interval:

- **works**: shrunk DV\* > 0, the 80% interval above 0, the cell's ledger q < 0.10,
  keeps its sign on ≥ 65% of held-out days, and holds in at least one other stratum
  (same sign of raw DV\* in B or C with ≥ 5 voting items) or on the forward days;
- **probably works**: shrunk DV\* > 0 and the 80% interval above 0, but one of the other
  conditions missing;
- **no evidence either way**: the 80% interval spans 0;
- **probably misleads** / **misleads**: the mirror images (interval below 0; the full set
  of conditions with the sign reversed).

A cell's "ledger q" is the q of the question that tested that exact cell's DV\* (every
registry cell is entered in the ledger as a question before it is computed).

## Ablation (MgV b)

Judge: `../skillopt-judge/seed_skill.md` (the panel-judge brief for one pack), Sonnet 5.5,
isolated. The intact arm is run **twice** over stratum A's packs (this also measures
run-to-run noise); for each ablated subtype, only the packs that contain it are re-judged
once with all its items removed, and unchanged packs reuse the intact calls. Effect =
ablated minus the mean of the two intact runs, on: within-day ρ against `move_n`, hit
rate, and the top-20% book (pooled, per `../judge-lab/judge_lab.py`'s convention). The
noise yardstick is intact run 1 minus intact run 2 on the same packs. Subtypes in order
of prevalence; the arm stops at $120.

## What the labeller may and may not see

Packs with no outcome, anonymised where the context names the company, opaque ids, the
isolated call of `scripts/llm.py`. Outcomes are joined only in `scripts/core.py`.
