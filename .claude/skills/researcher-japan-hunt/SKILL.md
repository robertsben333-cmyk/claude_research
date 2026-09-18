---
name: researcher-japan-hunt
description: The unpriced-information hunt, run over the Japanese market. Seals what the market has priced into each company reporting after today's Tokyo close, sends one hunter per name to find what is not in that price, and sums their signed finding sizes into one number per company so the day's names can be ranked. Research only, no orders. Use when asked to run the Japan researcher, run stage J, rank the day's Japanese earnings names, or hunt Tokyo prints.
---

# Stage J — the Japanese researcher

One signed number per company, so today's Japanese names can be **ranked**. No call,
no threshold, no direction label. Identical question and identical output contract to
the US stage, which is the point: if the two markets are scored the same way, the
Japanese result means something next to the American one.

**This stage places no orders and reads no broker.** There is no `alpaca_trade.py`
step here and there must not be one. It is research.

## What is different from the US stage, and it matters

| | US (stage E) | Japan (stage J) |
| --- | --- | --- |
| Calendar | Nasdaq vendor feed, `time-not-supplied` 20/20 phantom on one day | JPX `決算発表予定日`, the issuer's own notified date |
| Event window | after US close → before next open | after 15:00 JST → before 09:00 JST next session |
| Option anchor | implied move + 25d skew | none; substituted by JPX short register + 信用倍率 |
| The bar | sell-side consensus EPS | the company's own 会社予想 and the 進捗率 against it |
| Names per day | 17–22, all hunted | 8–125 scheduled; microcaps cut, then **capped at 25 by random draw** |
| Tail | uncapped | daily 値幅制限 price limit truncates large moves |

**The missing option anchor is substituted, not ignored (since 2026-09-18).** Japan has
no single-stock option chain, so there is no implied move and no skew. The baseline
instead carries `positioning` — JPX's daily disclosed short register (level and change)
and 信用倍率 — and supplies its own `priced_lean_pct` and `anchor_quality` to the shared
scorer. What that bought, measured on the 2026-09-11 universe: the lean's rank
correlation with the free control fell from **1.0 by construction to 0.446–0.59**, and
`baseline_quality` rose from a hard ceiling of **0.40 to 0.725**.

Two things still belong in every note. The weights in `lean_components()` are priors
with no Japanese measurement behind them, which is why `jp_resolve.py` ranks each
component separately. And none of it says what the market expects from *this* print —
positioning is stock, not flow — so the sealed-corpus result for anchor-less hunting
(ρ=+0.073, p=0.45 over 104 events) has been made testable, not refuted.

## Steps

Resolve paths with `python3 scripts/run_paths.py --json`. Re-read the clock with
`date -u`; do not trust the date you were told at startup.

**0. Heartbeat, before you spend anything.**

```bash
python3 scripts/run_log.py --heading "Stage J — Japan researcher — STARTED" --line "<the plan>"
scripts/publish.sh "stage J: started for <YYYY-MM-DD>"
```

One cheap commit, and the only thing that distinguishes a Routine that never fired
from a session killed on its first subagent.

**1. Universe.** `<RUN>` is `research/<YYYY>/<MM>/<DATE>/japan/`.

```bash
python3 researcher_japan/scripts/jp_universe.py -o <RUN>/universe.json
```

It reads every `kessan*.xlsx` JPX currently publishes, takes the rows scheduled for
today, drops microcaps on median 20-day turnover, and if more than 25 survive takes a
**random sample seeded by the date**. Report `selection.method`, `eligible` and
`hunted` in the note. The draw is random on purpose: any other cut is a second ranking
the scorer cannot see, and the US run has already paid for that once.

If `scheduled_today` is 0, that is a normal outcome and usually means the relevant
fiscal cohort's sheet is not up yet rather than that nobody reports. Publish the empty
universe, say which sheets were read and their `as_of`, and stop.

**2. Seal the baselines. Before any hunter.**

```bash
python3 researcher_japan/scripts/jp_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
```

Sealed means sealed. Nothing downstream may revise a baseline.

**3. One hunter per name.** Spawn `unpriced-hunter-jp`, in waves of
`japan_hunt.wave_size`, publishing after each wave. Give each hunter only its own
securities code, the window, and the path to its own baseline. Never another name's
baseline, never another hunter's findings, never your own view.

A wave that completes is banked. **If a whole wave returns empty, stop** and write the
`— HALTED` section rather than starting another.

**4. Score.** The scorer is the US one, unchanged and deliberately so:

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
```

The ranking key is whatever `edge-scores.json` reports in `ranking_key`. Read it; do
not carry a remembered contract into the run.

**5. Note.** Write `<RUN>/japan-note.md`, answer first: the ranked table, then the
finding and URL driving the top and bottom name, then the names that could not be
ranked and why.

The note must also say, every time:

- `selection.method`, and that the draw was random among the eligible names
- `lean_vs_free_control_rho` from the previous resolved run if there is one, because
  it is the check that the lean has not collapsed back into the free control
- that the lean's weights are priors, and which positioning components resolved
- the `history` basis is an estimated cadence, a scale and not a record of dates
- which names sit above `conviction_floor`, and that over the whole US sample the
  sign was a coin flip below it
- that one day is not a result

**6. Publish.**

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage J: Japan ranking for <YYYY-MM-DD>"
```

## Resolving, the next day

```bash
python3 researcher_japan/scripts/jp_resolve.py --run <RUN>
```

Confirms each release against TDnet, measures close-to-next-close, and reports
Spearman against the realised move with a permutation p and three controls. A name
TDnet cannot confirm gets `event_occurred: false` and leaves every ranking. TDnet keeps
about 31 days, so resolve promptly or the confirmation is lost.

## Budget

`config/pipeline.yaml`, `japan_hunt`. When the day would exceed the cap, shed by
`japan_hunt.degrade_order` and record what you shed in the run log. Half a run that
finishes beats a full one that gets cut off.

## The rule that outranks the rest

Never fabricate a number. Every company-specific figure carries a source URL or is
marked `unavailable`/`null`. A missing anchor correctly lowers confidence downstream;
an invented one corrupts everything after it.

This is research, not investment advice. Keep the disclaimer from
`config/pipeline.yaml` on the note.
