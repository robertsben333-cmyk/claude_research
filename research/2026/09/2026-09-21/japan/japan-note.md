# Stage J — Japan researcher — 2026-09-21

**Tokyo was shut. No names were hunted and there is no ranking.**

2026-09-21 is 敬老の日 (Respect for the Aged Day). `universe.json` carries
`market_closed: "public holiday: 敬老の日"`, so the empty calendar is the exchange
being closed — **not** a fiscal cohort's sheet that has yet to be published. Those two
produce an identical `scheduled_today: 0` and mean opposite things; this one is
settled, and there is nothing to wait for.

## Funnel

| | |
| --- | --- |
| Calendar rows read | 680 |
| Scheduled today | 0 |
| Eligible | 0 |
| Hunted | 0 |
| `selection.method` | not reached — no candidates to draw from |

Both cohort sheets parsed and are carried in `calendar_sheets`:

- `kessan07_0904.xlsx` — `as_of` 2026-09-03, 236 rows
- `kessan08_0918.xlsx` — `as_of` 2026-09-17, 444 rows

`calendar_as_of` is the older of the two, **2026-09-03**. The calendar was read in
full; it simply contains nobody scheduled for a day the exchange is closed.

## A defect this run found, and fixed

The container this stage fires into **does not ship `openpyxl`**. On the first pass
both sheets failed with `No module named 'openpyxl'`, `calendar_rows_total` came back
**0**, and every per-sheet row carried an `error`. Today the holiday short-circuited
that before it could matter. **On a trading day it would not have.** The output would
have read `scheduled_today: 0` with a null `market_closed`, and this stage's own skill
instructs a session to read exactly that as "the relevant fiscal cohort's sheet is
most likely not published yet" — so a session would have reported a quiet morning and
published an empty universe while 680 rows sat unread.

Two things changed:

- `openpyxl` was installed and the universe regenerated, which is why the published
  file reads 680 rows rather than 0.
- `jp_universe.py` now emits **`calendar_readable`**, and writes an explicit note when
  every cohort sheet failed to parse, so "nothing was read" can never again be read as
  "nobody reports". The holiday note still wins where a holiday is the settled cause.

This is the same failure shape the repo has paid for before — two causes that look
identical in the output and mean opposite things. It is now visible in the file itself
rather than only in a per-sheet `error` field nobody is told to check.

## The four things that belong in every stage J note

**There is no option anchor, and since 2026-09-18 it is substituted rather than merely
disclosed.** Japan has no liquid single-stock options, so `options` is all null. The
baseline supplies its own `priced_lean_pct` and `anchor_quality` from `positioning`:
JPX's daily disclosed short register (level, and whether shorts are building or
covering) and 信用倍率, the margin long/short ratio. Measured on the 2026-09-11
universe that moved the lean's rank correlation with the free control from **1.0 by
construction to 0.446–0.59**, and `baseline_quality` from a hard ceiling of **0.40 to
0.725**. **No baseline was sealed today**, so none of it was exercised on this date.

**`lean_vs_free_control_rho` from the last resolved run: there is none.** Nothing has
resolved in Japan yet. The only stage J runs on disk are the 2026-09-18 forward hunts
for 2026-09-24 and 2026-09-25, which have not reached their windows. So the check that
the lean has not collapsed back into the free control **cannot be performed today**,
and its absence is not reassurance. The weights behind the lean's components are
**priors with no Japanese measurement behind them**; `jp_resolve.py` ranks each
component separately so measurement can eventually replace them.

**The universe is cut and the cut is random** — microcaps drop on median 20-day
turnover (¥30m), then a date-seeded random draw picks at most 25. Not reached today.
The draw is random on purpose: any other cut is a second ranking the scorer cannot
see.

**`history` is an estimated cadence, not a record of dates.** TDnet keeps about 31
days, so prior dates are inferred by applying this quarter's notified lag backwards.
It is a scale for how much a name moves, never evidence that a print exists. Reading a
cadence prior as evidence is how the US stage ranked, traded and never got a print out
of TRT.

**Daily 値幅制限 price limits truncate the tail**, so a large finding can be right and
still not get paid in full.

## Ranking

None. `impact_sum` is the ranking key and no company produced one, because no company
reports into a window that does not exist. No name sits above the `conviction_floor`
of 3.0 for the same reason. Over the whole US sample the sign of `impact_sum` below
that floor is a coin flip (53%), which is why the floor is the finding rather than the
ranking.

## What this day does not establish

Nothing whatsoever about the method. A closed exchange is not evidence for or against
the hunt; it is an absence of evidence. **The next two scheduled fires are also
holidays** — 2026-09-22 (休日) and 2026-09-23 (秋分の日) — so the first stage J fire
that can produce a ranking is **2026-09-24**, for which a hunted run from 2026-09-18
already exists and should be resolved rather than re-hunted.

---

This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.
