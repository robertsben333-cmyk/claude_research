# Pre-registration: do "is it reliable" and "is it enough" pick the right names?

Written 2026-10-05, before any rated judgement exists. Committed before the run, so the
git history shows these tests were fixed first.

## The question

Should the panel judge rate two things beside its sizing:

- `evidence_reliability` (0-100): is what the pack says true and correctly read?
- `evidence_sufficiency` (0-100): is there enough here to form a view on this print at all?

They are asked AFTER sizing, with an instruction not to revise the numbers
(`seed_skill_rated.md`), so `impact_sum` stays the ranking key and the ratings can only
be used as a filter. Folding them into `p_up` would double-count: the shared core
already sends all sign uncertainty there.

The closest thing tried before: judge-lab's `rubric` judge asked per item whether it
was a fact or an inference and turned that into a certainty that REPLACED the ranking.
It did not beat the plain re-judges (16/25 against 20/25 in the top 15%). This tests the
other use: keep the ranking, filter it.

## Sample and runs

All 134 US names in `data/` (60 train + 49 gate + 25 readout from the SkillOpt runs; the
judge-lab TEST days stay sealed and are not in `data/`). Sonnet 5.5, isolated as before,
two runs (A and B). Primary numbers use the MEAN over the two runs of `impact_sum` and of
each rating. Nothing is fitted. Thresholds are the median of each rating over all 134
names, taken before any outcome is joined.

## Primary tests (three, so Bonferroni: |t| >= 2.4 to count)

- **H1 (sufficiency filters the book).** In the top 20% by |impact_sum| (judge-lab's
  pooled `top_metrics`, tradable names, per bucket), picks with sufficiency at or above
  the median earn more per pick, net, than picks below it.
- **H2 (reliability filters the book).** The same, for reliability.
- **H3 (sufficiency tells when the sign is right).** Among all names with a view, the
  sign is right more often at or above the sufficiency median than below it.

Verdict per test: the gap has the predicted sign and |t| >= 2.4 → **supported**; predicted
sign and |gap| >= 3pp (H1, H2) or >= 10 points of hit rate (H3) with |t| < 2.4 →
**possible, more data**; otherwise **not supported**.

**Power, stated now:** about 23 top-20% picks split in two, with a per-pick sd near 10,
puts the standard error of the H1/H2 gap near 4 points. Only a gap of about 10 points
would be supported. A null here does not rule out a small effect.

## Secondary (reported, no verdict)

- **Reproducibility:** Spearman of each rating between run A and run B. Below 0.5 means
  the rating is mostly noise and should not be used whatever the tests say.
- **Redundancy:** Spearman of each rating with |impact_sum|, |p_up − 50|, the number of
  evidence items, the share of items sourced to sec.gov, 20-day realised volatility and
  log turnover. A rating that is |impact_sum| again adds nothing.
- **Does asking change the sizing?** On the 74 gate + readout names where seed runs
  exist: Spearman of rated `impact_sum` against seed `impact_sum`, and the top-20% book
  of each.
- The combined filter (top 20% AND both ratings at or above the median), and the H1-H3
  numbers split into train days, gate days and readout days.
