# Stage J — Japan researcher — 2026-09-22

## Answer: no ranking today. Tokyo is closed.

**Funnel: scheduled 0 / eligible 0 / hunted 0.** No baselines were sealed and no
hunter was spawned, because there is nothing to hunt.

The Tokyo Stock Exchange is shut on 2026-09-22 for a public holiday
(敬老の日 / Respect-for-the-Aged Day, a 国民の祝日). `jp_universe.py` reads this from
the Cabinet Office's own 国民の祝日 list and wrote `market_closed: "public holiday: 休日"`
into `universe.json`.

## Which of the two empty-universe cases this is — the one that matters

There are two ways the universe comes back empty and they mean opposite things:

1. **The exchange is shut** — nothing to wait for. **This is today's case.**
2. The relevant fiscal cohort's schedule sheet is not published yet — a real print
   could still be coming.

They are distinguished by whether the calendar was readable. Today it was:
`calendar_readable: true`, **680 rows** across two JPX 決算発表予定日 sheets —
`kessan07_0904.xlsx` (as_of 2026-09-03, 236 rows) and `kessan08_0918.xlsx`
(as_of 2026-09-17, 444 rows). `scheduled_today` is 0 not because the sheets are
missing but because the exchange is closed, so no release lands in the
15:00 JST → 09:00 JST-next-session window. `calendar_as_of` is 2026-09-03.

Per CLAUDE.md, 2026-09-21 (敬老の日 observed), 2026-09-22 (国民の休日) and 2026-09-23
(秋分の日) all fall on a shut exchange — the first three scheduled fires after stage J
was built. Today is the middle one. Tokyo reopens Thursday 2026-09-24.

## Standing caveats that belong in every note

- **Selection.** N/A today — the random, date-seeded draw over eligible names only
  runs when names survive the turnover cut. Zero survived because zero were scheduled.
- **Positioning / option anchor.** Japan has no liquid single-stock options, so the
  baseline substitutes JPX's disclosed short register (level + change) and 信用倍率.
  Its `lean_components()` weights are **priors with no Japanese measurement behind
  them**; `jp_resolve.py` ranks each component separately so measurement can replace
  them. No baseline was sealed today, so none of this was exercised.
- **`lean_vs_free_control_rho`** — the check that the lean has not collapsed back into
  the free control (run-up) — has **no value to report**: nothing has resolved in Japan
  yet, so there is no previous resolved run.
- **`history` is an estimated cadence**, inferred by carrying this quarter's notified
  lag backwards over TDnet's ~31-day window. It is a scale for how much a name moves,
  **never a record of announcement dates**. Not used today.
- **conviction_floor** is `null` in config; no names to place above or below it. Over
  the whole US sample the sign below the floor was a coin flip — irrelevant today.
- Daily 値幅制限 price limits truncate the tail — irrelevant today.

## What this day does NOT establish

Nothing. A closed exchange produces no observation about the method, the market, or
the ranking. It is not a quiet feed, not a failed fetch, and not a null result — it is
a holiday. The next live Tokyo session is 2026-09-24.

---
*This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.*
