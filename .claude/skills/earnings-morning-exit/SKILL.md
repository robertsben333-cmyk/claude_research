---
name: earnings-morning-exit
description: Stage M. Half an hour before the US open, takes every name stage E-P scored at panel_pct 60 or higher on the previous trading day whose earnings are now out (amc yesterday, bmo this morning), and has one morning-reaction-analyst per name judge the release, the public reaction and the pre-market move, estimate the open and the open-to-close move, and recommend one exit for a position on the panel's side - sell at the open, a day limit, or wait until the close. Scores yesterday's advice against the static exit rule first. Writes research/<date>/morning/ and places no orders. Use when asked to run stage M, the morning exit review, or the pre-open earnings advice.
---

# Stage M — the morning-after exit review

Built 2026-10-18 on the operator's instruction: *"a routine that runs one hour before
the open and, for the names that had a score of 60 or higher the day before (US only),
judges the earnings release, the public reaction and the stock's move, and from that the
expected price reaction and the recommended action at the open: sell, limit, or wait
until the end of the day."* It fires at **08:56 ET** since the same day (moved from 08:26
on the operator's instruction, so the 08:00-08:30 bmo releases are out), which leaves the
analysts about 25 minutes. Launch them the moment the briefs exist.

Read `CLAUDE.md` first. Everything this stage computes is in
`researcher_us/scripts/morning.py`; its docstring defines the three actions, the
position and the control. Config is `morning_exit` in `config/pipeline.yaml`.

**What a "score of 60" is.** Stage E-P's `panel_pct` (0-100): the size of the mean of
the four judges' own-range percentiles, with the direction in `side`. 60 is the
operator's threshold and sits below E-P's own selection (80), so most names this stage
reads are names E-P did not select. The calibration in
`researcher_us/analysis/panel-calibration.json` reads about +0.3% up to 50, +1.6% at 70
and +2.6% at 80: below 80 the expected edge of the position itself is small, which is a
reason to read this stage's numbers per band.

**The position** is the panel's side, entered at 13:30 ET on the entry day (the
scorebord's window). **The control** is the scorebord's static exit: amc out at the open,
bmo out at 13:00 ET. Every advice row carries both, and `resolve` scores both.

**YOU PLACE NO ORDERS.** No `alpaca_trade.py` call of any kind. Never write into
`<prev>/edge-panel/` or any other stage's directory.

## 0. Clock and status

```bash
python3 researcher_us/scripts/morning.py slot
```

- `trading_day` false: append one line to today's run log saying the exchange is shut,
  publish, stop.
- `inside_hours` false (before 06:30 or after 09:29 ET): log one line with the New York
  time, publish, stop. An exit review after the open answers a question that has gone.
- `status: complete`: a re-fire. Log one line, publish, stop.
- `status: partial`: a killed earlier attempt. Keep `picks.json` and every review that
  exists; re-run `snapshot` and launch only the analysts whose review is missing.
- `source_exists` false: stage E-P did not publish yesterday. Log it, write the empty
  note with `compile`, publish, stop.

Heartbeat before anything is spent:

```bash
python3 scripts/run_log.py --heading "Stage M — morning exit review — STARTED" --line "<source run, now ET>"
scripts/publish.sh "stage M: started for <D>"
```

## 1. Score the previous morning first

```bash
python3 researcher_us/scripts/morning.py resolve --date <previous trading day>
python3 researcher_us/scripts/morning.py pool
```

Only when that morning has a `morning-advice.json`. Its close exists now, so this is
final. A missing day is not an error. Print the `pool` line in the run log: names, days,
`review_minus_static` with its t.

## 2. Pick

```bash
python3 researcher_us/scripts/morning.py pick
```

Writes `<D>/morning/picks.json`. Zero picks is a real answer: run `compile`, publish, and
say "no names at panel_pct >= 60 in this morning's window".

## 3. Snapshot

```bash
python3 researcher_us/scripts/morning.py snapshot
```

Writes the tape for every pick and one brief per name in `<D>/morning/briefs/`. Publish.

## 4. The analysts, one message

Launch one `morning-reaction-analyst` per pick, **all in ONE message**, each given only:

> Stage M review. Brief: `<D>/morning/briefs/<TICKER>.json`. Write your review to the
> `output_path` in the brief. It is now <HH:MM> New York; the advice is compiled at 09:24.

If the agent type is not found (a definition new on `main` that the harness has not
loaded), use `general-purpose` with model `opus` and tell it to read
`.claude/agents/morning-reaction-analyst.md` first and follow it exactly. Log the
fallback.

Do not give an analyst your own view, another analyst's review, or anything about
yesterday beyond what its brief names.

## 5. Compile by 09:24 ET

When every analyst has returned, or at 09:24 ET, whichever is first:

```bash
python3 researcher_us/scripts/morning.py compile
```

It re-reads the tape, checks every review (an action outside the three, a limit on the
wrong side of the pre-market price, a release with no URL, missing expectations) and
writes `morning-advice.json` and `morning-note.md`. A review with problems is shown as
`Geen advies` with the problem; it is not repaired by hand. A review that arrives after
the compile is not added.

Then:

```bash
python3 scripts/run_log.py --heading "Stage M — morning exit review — done" --line "<n> names, <actions>"
python3 scripts/update_index.py
export EARNINGS_DATA_BRANCH=main
scripts/publish.sh "stage M: exit review for <D>"
git fetch origin main && git log --oneline -1 origin/main
```

## 6. The closing reply

Paste `morning-note.md`'s table, then per name the one-line reason, then the `pool` line
from step 1, which analysts ran, and anything that failed. One morning is an anecdote.
This is a forecasting exercise over public information, not investment advice.
