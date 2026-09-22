---
name: researcher-canada-hunt
description: The unpriced-information hunt, run over the Canadian market — TSX, TSX Venture, CSE and NEO. Seals what the market has priced into each company reporting into the next Toronto session, sends one hunter per name to find what is not in that price, and sums their signed finding sizes into one number per company so the day's names can be ranked. Research only, no orders. Use when asked to run the Canada researcher, run stage CA, rank the day's Canadian earnings names, or hunt Toronto, TSX or TSXV prints.
---

# Stage CA — the Canadian researcher

One signed number per company, so today's Canadian names can be **ranked**. No call, no
threshold, no direction label. Identical question and identical output contract to the
US, Japanese and European stages, scored by the same scorer, because that is the only
way the four markets' numbers mean the same thing.

**This stage places no orders and reads no broker.** There is no `alpaca_trade.py` step
here and there must not be one. It is research.

## Why Canada is worth a stage, and it is not the calendar

Canada is the only market in this repo where the **option-anchored and anchor-less
regimes run inside one day's names**. The Montreal Exchange lists options on 360
underlyings, covering 96% of names above $25m a day and 10% below $1m, while the short
register covers 87–88% of *every* band. So a Canadian day splits into an arm anchored
exactly as the US stage is and an arm anchored as Japan and Europe are, in the same
market, on the same dates, scored by the same scorer.

`archive/backtest/FINDINGS.md` §33 priced the anchor-less regime at ρ=+0.073, p=0.45
over 104 events and could not separate the anchor from the market it was measured in.
`ca_resolve.py`'s `by_anchor_covered` separates them. That is the point of this stage;
the ranking is the by-product.

## What is different from the other stages

| | US (E) | Japan (J) | Canada (CA) |
| --- | --- | --- | --- |
| Calendar | Nasdaq feed, 20/20 phantom on one day | JPX issuer-notified date | **two vendors reconciled**, one carrying a CONFIRMED flag |
| Option anchor | implied move + 25d skew | none | **implied move for ~half the names, none for the rest** |
| Positioning | short interest | JPX register + 信用倍率 | CIRO register via TMX, 87–88% of every band, **no history** |
| The bar | sell-side consensus EPS | the company's own 会社予想 | **absent from the baseline — the hunter sources it** |
| Reaction history | real dates | estimated cadence | **real dates, off the TMX archive** |
| Event shape | a release | a release | a release **or a bare SEDAR+ filing**; filing-only issuers are screened out |
| Second language | none | Japanese | **French, for Québec issuers only — inside the one pass, not a second one** |

Four things must appear in every note this stage writes, because each is a live
uncertainty rather than a caveat that has been retired:

1. **The two calendars disagree on 172 of 277 forward dates.** The universe file grades
   every name `confirmed` / `agreed` / `wsh_only` / `vendor_only` / `disputed`, and
   `ca_resolve.py` ranks by that grade. Report the split. Disputed names are not hunted
   unless the issuer itself announced the date.
2. **The short register has no history.** `short_change_pct_pts` is null until two runs
   have stored a snapshot in `researcher_canada/analysis/short-register/`. Report the
   `register_business_date` you sealed — whether that feed refreshes daily or restamps
   CIRO's twice-monthly snapshot is still unknown, and the accumulating files are what
   will answer it.
3. **The implied move is refused unless the chain quotes two-sided.** Outside the
   Toronto session the Montreal chain's bid and ask are zeroes, and a straddle priced
   off `last` gave a median 12.5% "implied move" on the 2026-09-22 sample. Report how
   many names came back `anchor_covered: "options"`; if it is zero on a weekday run, the
   run was sealed outside 09:30–16:00 ET and the whole day is on the register arm.
4. **Everything except the option chain comes from one vendor stack.** TMX/QuoteMedia
   serves the register, the filings, the archive, the calendar and the tape. Europe's
   ten markets fail independently; Canada fails all at once, and there is no second
   source for the register anywhere.


## One bilingual pass, and the control that went with it

**`unpriced-hunter-ca` runs ONE pass in English and, for a Québec issuer, French,
since 2026-09-22.** Until that day the English half was frozen as `pre_local` before the
French half ran, and `impact_sum_pre_local` measured whether French search earned rank
correlation. It was retired on the operator's instruction: sequencing the two halves
forbade them from informing each other, which is most of what a bilingual reader is for.

**Nothing measures the French half any more.** No Canadian day had resolved while the
freeze existed, so the control never produced a number — what was given up is a future
measurement, not a result. What replaces it is `language_note`: prose, one line per
thing the French sources carried that the English ones did not, or 'not a Québec issuer,
English sources only'. Nothing ranks it. Quote it in the note where it is interesting
and do not present it as evidence. The `pre_lessons` control is untouched and still runs.

## Steps

Resolve paths with `python3 scripts/run_paths.py --json`. Re-read the clock with
`date -u`; do not trust the date you were told at startup.

**0. Heartbeat, before you spend anything.**

```bash
python3 scripts/run_log.py --heading "Stage CA — Canada researcher — STARTED" --line "<the plan>"
scripts/publish.sh "stage CA: started for <YYYY-MM-DD>"
```

**1. Universe.** `<RUN>` is `research/<YYYY>/<MM>/<DATE>/canada/`.

```bash
python3 researcher_canada/scripts/ca_universe.py -o <RUN>/universe.json
```

It scans TradingView's Canada universe, reconciles every candidate against Wall Street
Horizon through TMX, drops names below $200k a day of turnover, drops **filing-only
issuers** and **disputed dates**, folds second share classes, and if more than `cap`
survive takes a **random sample seeded by the date**. Report `selection.method`,
`calendar_reconciliation` and `moved_off_target_by_wsh` in the note.

`scheduled_today: 0` is a normal outcome in Canada — late September ran one name a day
and late October runs twelve. Publish the empty universe and stop. `market_closed` is
the exchange being shut, which is a different thing and says so.

**2. Seal the baselines. Before any hunter.**

```bash
python3 researcher_canada/scripts/ca_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
```

Sealed means sealed. Nothing downstream may revise a baseline. This step also writes the
day's short-register snapshot, which is what makes tomorrow's change computable.

**3. One hunter per name.** Spawn `unpriced-hunter-ca`, in waves of
`canada_hunt.wave_size`, publishing after each wave. Give each hunter only its own
ticker, the window, and the path to its own baseline. Never another name's baseline,
never another hunter's findings, never your own view.

A wave that completes is banked. **If a whole wave returns empty, stop** and write the
`— HALTED` section rather than starting another.

**4. Score.** The scorer is the US one, unchanged and deliberately so:

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
```

The ranking key is whatever `edge-scores.json` reports in `ranking_key`. Read it; do not
carry a remembered contract into the run.

**5. Note.** Write `<RUN>/canada-note.md`, answer first: the ranked table, then the
finding and URL driving the top and bottom name, then the names that could not be ranked
and why.

Besides the four live uncertainties above, the note must say every time:

- `selection.method`, and that the draw was random among the eligible names
- how many names are on each anchor arm, and that the two are ranked apart
- the `analyst_band` spread, because coverage is this stage's own thesis
- which names sit above `conviction_floor`, and that over the whole US sample the sign
  was a coin flip below it
- that nothing has resolved in Canada yet and one day is not a result

**6. Publish.**

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage CA: Canada ranking for <YYYY-MM-DD>"
```

## Resolving, the next day

```bash
python3 researcher_canada/scripts/ca_resolve.py --run <RUN> -o <RUN>/canada-resolved.json
```

Confirms each release two ways — a financial-results headline on the TMX archive, or an
interim/annual filing on SEDAR+ within three days — measures close-to-close over the
session window, and reports Spearman with a permutation p, the free control, the lean,
and the breakdowns by anchor arm and by date confidence.

**It will not confirm a date that has not passed.** Stage EU shipped that bug and killed
two names that had simply not reported yet. A name neither archive can confirm on a past
date gets `event_occurred: false` and leaves every ranking, which is the retrospective
kill the US stage added after TRT.

## Budget

`config/pipeline.yaml`, `canada_hunt`. When the day would exceed the cap, shed by
`canada_hunt.degrade_order` and record what you shed in the run log.

## The rule that outranks the rest

Never fabricate a number. Every company-specific figure carries a source URL or is
marked `unavailable`/`null`. **This matters more in Canada than anywhere else in this
repo, because the baseline has no consensus EPS in it at all**: the bar is not sealed,
the hunter has to source it, and a size against an invented bar is the worst thing this
stage can emit.

This is research, not investment advice. Keep the disclaimer from
`config/pipeline.yaml` on the note.
