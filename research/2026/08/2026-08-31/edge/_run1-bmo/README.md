# Run 1 — 2026-08-31 bmo — archived

This is the **first** edge hunt of 2026-08-31, moved here intact by the second run of the
same day. Nothing was deleted; every file is the one that was committed at
`4a186ea edge hunt: complete for 2026-08-31 bmo, 0 of 12 called`.

## Why it was moved

Two edge hunts ran on 2026-08-31 over **different windows**:

| | window | universe |
| --- | --- | --- |
| run 1 (here) | 2026-08-31 bmo, `--include-unknown` | SAIC SY LX BLRX GASS GRFS SSL AIV CBAT CHRN CURR FRGT |
| run 2 (`../`) | 2026-08-31 amc + 2026-09-01 bmo, the `--window` default | MDT NIO MMED RZLV YEXT CANG HMR ZEPP RGS PXS |

`edge_score.py --run <dir>` reads every `*.json` in `<dir>/baselines`, `<dir>/hunts` and
`<dir>/adversary` non-recursively. Left in place, run 1's twelve names would have been
pooled into run 2's ranking — two different windows sorted as one day. Worse, run 1's
findings were recorded under the **old categorical contract** (`direction`, no
`expected_impact_pct`), which the current scorer reads as `0.0` unless `--legacy` is
passed. All twelve would have entered the table as zeros and sorted above every genuinely
negative name.

Moving them into a subdirectory is enough, because `load_dir` does not recurse.

## What this costs

`edge_resolve.py --pool 'research/2026/*/*/edge'` no longer sees these names. That pool
loses nothing measurable: run 1 called 0 of 12, eight of its rows were phantom calendar
entries with no earnings event, and it produced no ranking. Its value is the
methodological record — it is the run that caused the categories to be removed — and that
record is what is preserved here.

To re-score it deliberately, on its own and never merged into another day:

```bash
python3 scripts/edge_score.py --run research/2026/08/2026-08-31/edge/_run1-bmo --legacy
```

`--legacy` substitutes midpoints for the missing continuous fields. Those midpoints are a
demonstration of the machinery, never evidence about the day.
