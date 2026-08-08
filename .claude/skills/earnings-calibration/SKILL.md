---
name: earnings-calibration
description: Stage 4 of the daily earnings pipeline. The morning after, records what the previously called stocks actually did, scores the panel's calls, and maintains the rolling accuracy ledger. Use when asked to run stage 4, check yesterday's earnings calls, or update the calibration ledger.
---

# Stage 4 — Outcome check and calibration

Cheap, fast, and the only stage that tells you whether any of the others work.

A forecasting pipeline with no outcome ledger drifts indefinitely: it feels insightful
every single day and there is no evidence either way. This stage closes the loop. It
runs the next morning, after the calls have resolved.

## 1. Find the run to score

```bash
python3 scripts/run_paths.py --json
```

The run to score is the **previous trading day**, not today. Take the most recent
`research/*/*/*` directory that has an `04-advice.json` and no `05-outcome.md`. If there
are several unscored runs — a weekend, a holiday, a failed routine — score all of them,
oldest first.

If there is nothing unscored, say so in one line and stop. Do not manufacture work.

## 2. Get what actually happened

For each name in `ranked_names`, find via `WebSearch`/`WebFetch`:

- the reported EPS and revenue versus consensus
- the guidance the company gave, if any
- **the actual post-earnings price move**: close before the print → close after the
  first full session following it, as a percent
- the intraday reversal, if the stock gapped one way and closed the other — that detail
  matters and a single close-to-close number hides it

Use the same close-to-close convention every day. An inconsistent measurement window
makes the ledger meaningless. If a source disagrees with another, prefer the exchange or
a major provider and note the discrepancy.

If a company delayed or moved its report, record `"outcome": "not_reported"` and exclude
it from scoring — do not score it as a miss.

## 3. Score the calls

For each **panelled** name:

- **Direction hit**: did the stock move the way the call said? A `Neutral / No Edge`
  call is scored separately — it is a hit when the realised absolute move came in below
  the expected move, a miss when the stock moved hard and the panel had no view.
- **Magnitude error**: `actual_move − signed_estimated_move`, signed.
- **Band hit**: did `|actual_move|` land inside `move_band_low_high`?
- **Implied-move break**: did the stock move more than the event-implied move?
- **Reversal fired**: did the specific red-team reversal case actually play out? This is
  the most informative single field in the ledger, because it is the one thing the panel
  explicitly predicted *against*.

For non-panelled deep-dive names, score direction against
`preliminary_direction_score` only. That comparison is the evidence for whether the
seven-persona panel earns its cost over a single deep researcher — if the panel is not
beating the preliminary read over a few dozen names, the expensive stage is not paying
for itself and should be cut.

## 4. Write the outcome file

`05-outcome.md` in that run's directory: a table of every name with the call, the
realised move, the direction hit, the magnitude error, and one line on what the call
got right or wrong. Then a short honest paragraph — where the process failed, not just
where the number missed. "The implied move was stale" is a fixable finding; "the market
was irrational" is not.

Also `05-outcome.json`:

```json
{
  "run_date": "2026-08-10",
  "scored_at": "2026-08-11",
  "measurement": "close before print to close after first full session",
  "names": [
    {"ticker": "TTWO", "panelled": true, "call": "Lean Up",
     "signed_estimated_move": 4.2, "actual_move": 6.8,
     "direction_hit": true, "magnitude_error": 2.6, "band_hit": true,
     "implied_move_broken": false, "reversal_fired": false,
     "preliminary_direction_score": 25, "preliminary_hit": true}
  ]
}
```

## 5. Update the rolling ledger

Append to `LEDGER.md` at the repo root, one row per run day, and refresh the summary
block at the top:

- calls scored to date, split panelled versus preliminary-only
- direction hit rate, overall and for panelled names only
- mean and median absolute magnitude error
- band hit rate
- calibration by certainty tier: **do High-certainty calls actually hit more often than
  Low-certainty ones?** If they do not, the certainty tiering is decorative and the
  synthesis needs fixing.
- how often the red-team reversal case fired

Report these plainly whether or not they flatter the pipeline. A ledger that only gets
updated after good days is worse than no ledger.

## 6. Publish

```bash
python3 scripts/update_index.py
python3 scripts/build_predictions.py
scripts/publish.sh "stage 4: outcomes for <YYYY-MM-DD>"
```

`build_predictions.py` rewrites `PREDICTIONS.csv`/`.json`, flipping the rows you just
scored from `pending` to their realised numbers. Its printed summary — total
predictions, how many are scored, the panelled direction hit rate — is a useful
cross-check against the figures you wrote into `LEDGER.md`. If the two disagree, the
ledger is wrong, because the table is derived straight from the per-day files.

## 7. Report

Which run was scored, the hit rate for that day, the running hit rate, and — most
usefully — any pattern showing up across several days: a persona that is consistently
wrong, a systematic magnitude bias, certainty tiers that do not separate. Those are the
findings that justify changing `scripts/synthesize.py` or a persona definition.
