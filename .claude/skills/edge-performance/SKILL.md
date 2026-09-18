---
name: edge-performance
description: Folds every newly closed position and every newly resolved edge-hunt run into the performance ledger, rebuilds the dashboard, and writes down what changed. Use when asked to update the performance dashboard, check what the edge hunt is earning, score the closed trades, or analyse stage E's results over time.
---

# Edge performance — fold in what closed, then say what it now reads

Stage E scores companies daily and the account trades a slice of them. Neither of
those measures itself. This does, over every run and every position at once, and it
is the only place in the repo where the trading record and the research record meet.

It is a **read-only** stage. It never submits, cancels or modifies an order, never
re-scores a run, and never edits a hunt. If you find an exit that did not fill or a
position past its exit date, you report it — `researcher_us/scripts/alpaca_trade.py` and a
person decide what to do about it.

Run it after the US close, when the day's positions have either closed or visibly
failed to. Running it earlier is harmless: an unclosed window is reported as pending
and re-prices itself on the next update.

## 1. Read the clock and the previous state

```bash
date -u
python3 dashboard/scripts/build_ledger.py --help >/dev/null   # imports resolve
```

A session's own sense of the date goes stale; `date -u` is the only clock to trust.
Then note what the ledger says *before* you touch it — the comparison is the whole
point of the update:

```bash
python3 - <<'PY'
import json
d = json.load(open('dashboard/data/ledger.json'))
s = d['stats']
print(d['generated_utc'], '| names', s['ranking']['n'], 'days', s['ranking']['days'],
      '| rho', s['ranking'].get('rho_impact_sum'),
      '| closed', s['trading']['n_closed'],
      '| pnl', s['trading'].get('total_pnl_usd'))
PY
```

If `data/ledger.json` does not exist yet, this is the first build; skip the
comparison and say so.

## 2. Rebuild

```bash
./dashboard/update.sh
```

`--offline` skips the broker and keeps the previous build's trades; `--serve` serves
the page afterwards so its own refresh button works. A person can run the same button
from the page; you run the script.

It fetches the account's whole fill history, matches it into round trips, re-prices
every run at eight exit horizons, recomputes every statistic and re-renders
`dashboard.html`. Without network to the broker use `--offline`, which keeps the
previous build's trades and flags that it did so.

Read what it prints. Three lines matter:

- `names priced: N   problems: M` — a rising `M` with a falling `N` means runs
  stopped resolving, not that the stage got worse.
- `round trips: X closed, Y open` — `Y` should be the positions entered today and
  nothing older. An older name in the open list is an exit that never filled.
- the pooled `rho` and `control` line — the research verdict, before any money.

## 3. Find what changed, and check it is real

Compare against the numbers from step 1 and establish, for each:

- **New closed positions.** For each one: the ticker, the entry and exit price, the
  return, and whether stage E or a person closed it (`exit_source` in
  `data/trades.csv`). A position closed by hand is not evidence about the exit
  policy, so never pool the two without saying which is which.
- **Newly resolved names.** A run whose outcome window has closed since the last
  build now carries a move. Check whether the day's `rho` in the Score tab is
  plausible against the names — one day of eight names swings between +0.9 and −0.3
  on noise alone.
- **A run still in flight.** The newest run resolves against tonight's close, so its
  names carry `pending: true` and no return at the `close` horizon. That is expected, not
  a failure — but check that yesterday's run has *left* that state. A pending row that is
  two days old means the reaction session came and went without a daily bar, which is a
  data problem, not a market one.
- **Positions open longer than a day.** Cross-check `data/trades.csv` `hold_hours`
  and the planned `exit_date` in `research/<date>/edge/alpaca-orders.json`. An
  `opg`/`cls` order that never crossed leaves a position open and the ledger shows
  it as a long hold, not as a failure. Report it; do not fix it here.
- **A number that moved more than the new data can explain.** If two new trades move
  the pooled `rho` by 0.2, something re-priced. Say so rather than reporting the new
  figure as a finding.

## 4. Read the tabs that only a filter can answer

Three questions are worth asking on every update, because each one has already moved
once in this sample and none of them is visible in the unfiltered numbers.

- **Does the threshold still do the same thing to both sessions?** The **Drempel** tab
  sweeps fifteen cuts. On the first build, raising it lifted bmo monotonically (+2.5%
  at ≥0 to +12.0% at ≥7) while amc fell with it (−0.7% to −2.9%). If that split holds
  as days pool it is an argument for a per-session floor; if it flips, it was noise and
  the note has to say so.
- **Is the edge in the thin names?** The same tab splits thin against thick turnover at
  the median. If only the thin half rises with the threshold, the cut buys illiquidity
  rather than information, and the **Capaciteit** tab says what the position size would
  have to be.
- **What did execution cost?** The **Handel** tab prices every closed position against
  the same name's board return. Report the policy gap and the exec gap separately —
  the first includes the entry timing, the second does not.
- **What does the position cap cost?** The **positiecap** control recomputes every day's
  return under the sizing rule — gross budget split over the day's names, capped per
  name. On the first build, 33% per name over the whole sample compounds to less than
  equal weight does, because a four-name day leaves capital idle. Report the total under
  the live cap, not the equal-weighted one, whenever the question is about the account.

Always report which of the three returns you mean. Per name or position, per day, and
compounded over the period are three different numbers, and on this sample the spread
around the first is more than ten times its mean.

Set the filters back to the defaults before quoting a headline number, and say in the
log which filters a number was taken under. A ρ measured above the threshold is a
different statistic from the pooled one and the two must never be reported as if they
were the same.

## 5. Write it down

Append one dated section to `dashboard/LOG.md` — append, never rewrite, the
same rule as `_run-log.md`. Keep it short and keep it honest:

```markdown
## 2026-09-17 — update

Closed since the last build: LUXE +25.4% ($534, closed by hand), ...
Newly resolved: 2026-09-15 (4 names, rho +0.80).

Pooled, 102 names over 11 days: rho -0.145 against -0.137 for the free control.
Account: +17.1% over 8 sessions, 9 closed positions, 5 up.

Read: the ranking still does not beat the free control, and the account result is
one leg — six longs at +17.7%, three shorts at -13.9%.
```

Three things belong in every entry and nothing else has to:

1. what closed and what resolved since the last build,
2. the pooled ranking figure **next to its free control**, because the first without
   the second means nothing,
3. one sentence of critical read — what the new data would have to look like before
   any of this is a finding.

Add a fourth line whenever a *slice* moved: the session split on the threshold curve,
a sector that has gone from three names to eight, an execution gap that widened, or a
cost per name that doubled. Those are the numbers that change what the stage does
next, and they are invisible in the pooled figure.

Never write a conclusion the sample cannot carry. At this n, the honest sentence is
usually "still nothing established"; write that rather than dressing up a good week.

## 6. Publish

```bash
scripts/publish.sh "performance: ledger and dashboard through <YYYY-MM-DD>"
```

The ledger, the CSVs and `dashboard.html` are generated but they are **not**
reproducible later: the broker's fill history is not in this repo and the oldest
orders age out of the API. A session that does not push them loses the only copy.

## 7. Report

Lead with what changed, not with the level. Then the pooled figure and its control,
then anything that needs a person: an exit that never filled, a position two days
overdue, a run that stopped resolving, a `problems` list that grew.

If the stage's own conclusions have moved — the ranking crossing zero, the free
control overtaking it, a session split reversing — that belongs in
`researcher_us/EDGE_ANALYSIS.md` and in `CLAUDE.md`, in the same commit. Do not leave the
headline paragraph of CLAUDE.md describing a result this ledger has since contradicted.
