---
name: earnings-triage
description: Stage 1 of the daily earnings pipeline. Screens the day's qualified earnings universe down to the handful of names stage 2 can afford to research, scoring each on how much the print could move the stock and on whether deep AI research would add anything. Use when asked to run stage 1, triage the earnings universe, or build the day's shortlist.
---

# Stage 1 — Triage to a shortlist

Stage 0 produced a universe. Stage 2 can afford `triage.shortlist_size` deep dossiers —
currently **3**. This stage picks which ones, on two axes at once:

- **`change_expectation`** — how much could this print move the stock?
- **`ai_edge`** — can careful research actually say something useful about it?

Both must be high. A biotech binary readout scores 95 on the first and 15 on the second:
it will move enormously and nobody can forecast it, so it is a waste of a dossier. Being
willing to say that is the point of this stage.

## 1. Load state

```bash
python3 scripts/run_paths.py --json
```

Read `00-universe.json`. If it is missing, stage 0 did not run or did not publish —
run the `earnings-universe` skill first, then come back.

## 2. Decide whether to run at all

Read `config/pipeline.yaml`. If eligible names ≤ `triage.skip_if_universe_at_or_below`
(default 10), **skip the screen entirely**. Write all eligible names straight to
`01-shortlist.json` with `change_expectation` and `ai_edge` set to `null`,
`"triage_mode": "skipped_small_universe"`, and a `selection_rationale` of
`"universe at or below the triage threshold — all eligible names carried forward"`.
Then jump to step 5. Screening eight names down to eight costs tokens and decides
nothing.

## 3. Scout the universe

Split the eligible names into batches of `triage.batch_size` (default 15) and spawn one
`earnings-triage-scout` subagent per batch, up to `triage.max_scouts`. Run them in
parallel — they are independent.

These scouts are deliberately cheap (Sonnet, medium effort). Do not substitute the
deep researcher here; depth at this stage buys almost nothing, because most of these
names will be discarded within the hour.

Give each scout the tickers, company names, sessions, event dates, and market caps from
the universe file. Nothing else.

If the universe was rebuilt by web search (`status: partial`), tell the scouts so and
ask them to confirm timing more carefully than usual.

## 4. Rank and cut

Collect the scout JSON. For each name:

```
priority_score = weight_change_expectation * change_expectation
               + weight_ai_edge           * ai_edge
```

Then apply, in order:

1. **Drop** anything with `timing_confirmed: false` or `tradeable: false`.
2. **Drop** anything below `min_change_expectation` or below `min_ai_edge`. These are
   hard floors, not tiebreakers — a name that fails either is not worth a dossier
   regardless of how well it scores on the other axis.
3. Sort by `priority_score` descending and take `triage.shortlist_size` (currently 3).

**If fewer names clear the floors than that, take fewer.** Do not backfill from below the
floor to reach a round number. A one-name shortlist of a genuinely researchable setup
beats a three-name list padded with names nobody can call. Record the shortfall and
why.

Prefer a mix of AMC and BMO reporters when the scores are close — a shortlist that is
all after-close names leaves the next morning's window unexamined. Note the tilt if one
session dominates.

## 5. Write the shortlist

`01-shortlist.json`:

```json
{
  "schema_version": 1,
  "run_date": "2026-08-10",
  "window_covered": "<copied from the universe file>",
  "triage_mode": "scouted | skipped_small_universe",
  "universe_total": 61,
  "universe_eligible": 34,
  "scouts_used": 3,
  "floors": {"min_change_expectation": 35, "min_ai_edge": 30},
  "dropped_for_floors": 12,
  "shortlist": [
    {
      "ticker": "TTWO",
      "company": "Take-Two Interactive",
      "session": "amc",
      "event_date": "2026-08-10",
      "market_cap_usd": 41200000000,
      "change_expectation": 78,
      "ai_edge": 64,
      "priority_score": 71.7,
      "expected_move_hint": "9.2%",
      "selection_rationale": "<one line: the catalyst, and why research helps>",
      "evidence": "good"
    }
  ]
}
```

Validate before publishing:

```bash
python3 scripts/validate_stage.py shortlist <run_dir>/01-shortlist.json
```

Fix anything it reports. Do not publish an invalid shortlist — stage 2 reads this file
unattended and will happily research a malformed entry.

Also write `01-shortlist.md`: the window, the funnel counts (universe → eligible →
cleared floors → shortlisted), a table of the shortlist with both scores and the
rationale, and a short list of the most notable names that were *dropped* and why. That
last part is what makes the archive auditable — if the pipeline keeps discarding names
that then move 15%, the dropped list is where you would see it.

## 6. Log and publish

Append to `_run-log.md`:

```markdown
## Stage 1 — triage (<HH:MM> CET)
- Mode: <scouted | skipped (universe <= threshold)>
- Funnel: <n> universe -> <e> eligible -> <f> cleared floors -> <s> shortlisted
- Scouts: <k> subagents (sonnet/medium)
- Session mix: <a> AMC / <b> BMO
- Notable drops: <ticker (reason)>, ...
```

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage 1: shortlist for <YYYY-MM-DD> (<s> names)"
```

## 7. Report

The funnel in one line, the shortlist as a compact table (ticker, session, both scores,
one-line reason), and any warning stage 2 needs — thin evidence, an unbalanced session
mix, or a short list.
