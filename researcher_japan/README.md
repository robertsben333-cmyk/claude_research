# researcher_japan — stage J

The unpriced-information hunt, run over the Tokyo market. One signed number per
company (`impact_sum`, points of spot, unbounded) so the day's names can be **ranked**.
No call, no threshold, no direction label. Research only: **this stage places no
orders and reads no broker.**

It exists to ask whether the result the US stage is chasing is a property of the
method or a property of the US market. Because it uses the same scorer, the same key
and the same measurement window, the two are directly comparable.

## Status

**Nothing has resolved. There is no Japanese result, good or bad.**
Built and validated end to end on 2026-09-18 against a real past date (2026-09-11:
76 scheduled, 34 eligible, 25 drawn, 24 of 25 confirmed on TDnet, one correctly killed
as `event_occurred: false`, median realised move 2.87%). That run used synthetic
findings to exercise the plumbing and ranked at ρ=0.154, p=0.47, which is what random
findings should do and is not a result about anything.

## The pieces

| | |
| --- | --- |
| `scripts/jp_universe.py` | JPX `決算発表予定日` → today's names, microcap cut, cap-25 random draw |
| `scripts/jp_priced_in.py` | the sealed baseline, in the shape `edge_score.py` reads |
| `scripts/jp_resolve.py` | TDnet confirmation, realised move, Spearman + permutation p |
| `researcher_us/scripts/edge_score.py` | **shared, unchanged** — the scorer is deliberately the same one |
| `.claude/agents/unpriced-hunter-jp.md` | the hunter; same output contract as the US one |
| `.claude/skills/researcher-japan-hunt/SKILL.md` | the run |

## Why Japan and not Korea

Korea was the original target and was rejected on measurement. Querying DART directly:
Korean periodic filings arrive in four spikes a year of roughly 3,000 each (Nov 3,077
quarterly; Mar 2,880 annual; May 3,059; Aug 3,121) and the weeks between them carry
almost nothing — the 14–18 September 2026 window had zero quarterly or semi-annual
reports. Korean issuers are near-universally December fiscal year-end, so they all
report together. Korea also has no mandatory forward earnings-date notice, no liquid
single-stock options, and KIND returns 403 from this environment.

Japan's fiscal year-ends are staggered, so the flow never stops. Counting 決算短信 on
TDnet across all pages: 456 on 2026-08-14 at the season peak, but still 79 on 09-11,
39 on 09-18, 24 on 09-01 and 11 on 09-17 in the off-season. The quietest day sampled
matched half the US stage's daily universe.

## What this market will not give you

**No option anchor.** JPX concentrates option volume in the index; single-stock options
are not liquid. `options` is written all-`null` with a reason rather than omitted.
Consequences, which belong in every note:

- `baseline_quality` tops out at **0.40** for any Japanese name.
- `priced_lean_pct` falls to `-0.05 * run_up_20d_pct` for every name, so the free
  control and the baseline's only directional content are **the same number**. The
  hunt has to beat the run-up to have added anything at all.
- This is the regime that produced the worst number in this repo: on the sealed
  backtest corpus, where the option anchor was likewise unrecoverable, the hunt ranked
  ρ=+0.073, p=0.45 over 104 events (`backtest/FINDINGS.md` §33).

**No retrievable history of announcement dates.** TDnet keeps ~31 days and JPX
publishes only near cohorts. `history` is therefore built by applying this quarter's
notified lag backwards to prior period ends and taking the largest move within ±2
trading days. Every row carries `basis: "estimated"`, the estimated date, the date used
and the gap. It is a **scale**, not a record. This repo has already been burned reading
a cadence prior as evidence — TRT was ranked, traded and never reported.

**A truncated tail.** Tokyo's daily 値幅制限 caps how far a name can move, which biases
every correlation toward zero on exactly the events the hunt most wants credit for.
Limit-locked sessions are flagged by the resolver, never corrected.

**A near-horizon calendar.** JPX posts one sheet per fiscal-month cohort and only the
near ones are up at a time, so a day with no rows usually means that cohort's sheet is
not published yet, not that nobody reports. `calendar_sheets` and `calendar_as_of` are
carried into every universe file for exactly this reason.

## The selection is random on purpose

In season the calendar carries up to 125 names on one date and TDnet saw 456 releases
in a day. One hunter per name means the day has to be cut, so: drop microcaps on median
20-day turnover (default ¥30m ≈ $200k/day, the same capacity bar the US run screens
on), then if more than 25 remain take a **random sample seeded by the date**.

Random, because any other cut is a second ranking the scorer cannot see. The US run has
already paid for this: its two highest-`hunt_priority` names got two hunters each, and
because the key is a sum those names carried the largest conviction by construction —
`edge_hunter_control.py` had to rebuild all 38 events to find out how much of the
headline was selection rather than finding. The seed is the date and `eligible_codes`
carries the whole population, so the draw is checkable.

Note what the microcap cut costs: on the 62 names scheduled for 2026-10-09 the median
turnover was ¥7.4m a day, about $49k, and the floor kept 40%. The ranked universe is
explicitly the liquid half of the day and is **not** a sample of Japanese listed
companies.

## This is research, not advice

A forecasting exercise over public information. Keep the disclaimer from
`config/pipeline.yaml` on every deliverable.
