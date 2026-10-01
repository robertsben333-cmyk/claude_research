# researcher_japan — stage J

The unpriced-information hunt, run over the Tokyo market. One signed number per
company (`impact_sum`, points of spot, unbounded) so the day's names can be **ranked**.
No call, no threshold, no direction label. Research only: **this stage places no
orders and reads no broker.**

It exists to ask whether the result the US stage is chasing is a property of the
method or a property of the US market. Because it uses the same scorer, the same key
and the same measurement window, the two are directly comparable.

## Status

**Four days have resolved, eight names, and it is not a result.** On the corrected
window three of seven signs were right; the stage has not yet beaten anything.
Built and validated end to end on 2026-09-18 against a real past date (2026-09-11:
76 scheduled, 34 eligible, 25 drawn, 24 of 25 confirmed on TDnet, one correctly killed
as `event_occurred: false`, median realised move 2.87%). That run used synthetic
findings to exercise the plumbing and ranked at ρ=0.154, p=0.47, which is what random
findings should do and is not a result about anything.

## What changed on 2026-10-01, and why (`jp.v5`)

The first resolved days read as one sign right in seven. Two causes were found, and
only one of them was the hunter.

**The measurement was wrong for a third of the names.** The TSE has closed at 15:30
since 2024-11-05, not at 15:00 as every file here said, and Japanese companies release
at fixed times that are often INSIDE the session: 13:00 and 13:30 for retailers, 15:00
widely. `jp_resolve.py` entered every name at the event-day close, so a 13:00 release
was scored from a price that already held its reaction. Of the first seventeen hunted
names four released before the close, three of them on resolved days. TAKARA & CO
(7921), +1.0 on a 15:00 release, rose 3.3% into the close and was scored on the next
day's −1.9%. The resolver now reads the release time off TDnet and enters an
in-session release at the sealed 10:05 JST spot (only if it was sealed that same
morning, else the previous close). `entry_basis`, `release_time_jst` and
`move_close_to_close_pct` say which window was used and keep the old one beside it.
Re-resolved, the record is three of seven.

**The hunter was sizing against the wrong bar.** The definition told it the company
plan is the bar and the 進捗率 is where the edge is. Five of seven calls came back
negative, four on "the 月次 show the quarter missing the company's own plan", and two
of those four stocks fell. The monthly series is public; the miss was priced before
anyone found it, and a known bad number often lifts a Japanese stock when it lands
(悪材料出尽くし). The definition now ranks what a release ADDS: a forecast revision
against 四季報 or IFIS rather than against the plan, shareholder returns (増配, 自社株買い,
優待), the new year's guide, and only then the quarter, read against the company's own
progress-rate history. It asks for the release time, gives the hunter a Japanese scale
and treats a visible miss as priced unless the release adds to it.
`LESSONS.md` holds the two measured rules, with their counts, so the `pre_lessons`
control still measures them separately from the definition.

**What this does not establish.** Eight names over four days. The change is a
hypothesis about this market and is compared forward: every run since carries its
prompt version in `provenance.json`, and the dashboard's **Versies** tab puts `jp.v5`
beside `jp.v3`. Do not pool the two when judging either.

## The pieces

| | |
| --- | --- |
| `scripts/jp_universe.py` | JPX `決算発表予定日` → today's names, microcap cut, cap-25 random draw |
| `scripts/jp_priced_in.py` | the sealed baseline, in the shape `edge_score.py` reads |
| `scripts/jp_resolve.py` | TDnet confirmation and release TIME, realised move from before the release, Spearman + permutation p |
| `scripts/jp_positioning.py` | JPX disclosed short register + 信用倍率, the substitute anchors |
| `researcher_us/scripts/edge_score.py` | **shared** — same scorer for both markets, so the numbers are comparable |
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

## The anchor problem, and how it was solved

Japan has no liquid single-stock options, so `options` is all `null`: no event-implied
move, no 25-delta skew. Until 2026-09-18 that left `priced_lean_pct` as
`-0.05 * run_up_20d_pct`, which is **also the free control every ranker is measured
against** -- the baseline's lean and its own benchmark were the same number, so the
control could not be beaten by anything that used it, and `baseline_quality` was capped
at 0.40.

Three substitutes now carry that load, built from what Tokyo does publish:

| | what it is | coverage | independent of the run-up? |
| --- | --- | --- | --- |
| `short_ratio_pct` | JPX's daily disclosed short register, summed over sellers | non-zero on 9-11 of 25 names; a real 0 otherwise | yes, rho 0.07 |
| `short_change_pct_pts` | the same register's current vs previous ratio: shorts building or covering | same | largely |
| `margin_ratio` | 信用倍率, margin longs / margin shorts | 25 of 25 | largely, rho -0.39 |

Measured on the 2026-09-11 universe, the composite lean now ranks against the free
control at **rho 0.446-0.59, where it was 1.0 by construction**, and `baseline_quality`
reaches **0.725** where it was capped at 0.40. `jp_resolve.py` reports
`lean_vs_free_control_rho` on every run: if it climbs back toward 1.0 the positioning
sources have stopped resolving and the lean has collapsed into the control again.

**The weights are priors and nothing about them is measured in Tokyo.** A crowded short
is treated as a positive lean because the US run watched two shorts into 18%- and
23%-of-float names both squeeze more than 20%; shorts building into a print is treated
as negative because disclosed sellers who must file their names are the closest thing
this market has to visible informed flow; a high 信用倍率 is treated as negative because
leveraged retail longs have to be sold eventually. `jp_resolve.py` ranks each component
separately against the realised move for exactly this reason. **Replace the weights with
measurement; do not defend them.**

What is still missing, and it is not small: none of this says what the market expects
from *this print*. Skew is a price someone paid for one tail on one date. A short
register and a margin ratio are stock, not flow, and they say how crowded the trade
already is, not what the crowd thinks the number will be. `expected_move` is likewise a
scale, from realised vol and an estimated-cadence history, and **nothing is paying for
it**. The sealed-corpus result that runs on this kind of anchor -- rho +0.073, p 0.45
over 104 events (`backtest/FINDINGS.md` §33) -- has not been refuted by any of this. It
has been made testable.

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

## The hunters need `curl`, and that was found the hard way

On the 2026-09-18 verification run a hunter hit HTTP 403 from `WebFetch` on **every URL
it tried**, including the TDnet 月次 PDFs that were the single highest-value series for
its name, and fell back to search snippets it could not confirm. Re-checked from the
same container seconds later: `curl` returned **200** on TDnet's list *and* its PDFs, on
kabutan, on irbank and on Nikkei — the same URLs `WebFetch` refused. A company's own IR
host and minkabu refuse both.

`WebFetch` is blocked on this egress path where `curl` is not, and this market's evidence
lives in documents rather than in search results. `unpriced-hunter-jp` therefore carries
`Bash`, which the US hunter does not, and its definition documents the fallback. Without
it the stage reads Japan through search snippets and cannot verify a single figure in its
source, which is the condition this repo's "never fabricate a number" rule exists to
prevent.

## The selection is random on purpose

In season the calendar carries up to 125 names on one date and TDnet saw 456 releases
in a day. One hunter per name means the day has to be cut, so: drop microcaps on median
20-day turnover (default ¥15m ≈ $100k/day since 2026-10-01, the non-US bar and half the US one; it was ¥30m ≈ $200k/day, the same capacity bar the US run screens
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
