---
name: researcher-europe-hunt
description: The unpriced-information hunt, run over the UK, French and German markets pooled. Seals what the market has priced into each company reporting into the next European session, sends one language-specific hunter per name to find what is not in that price, and sums their signed finding sizes into one number per company so the day's names can be ranked. Research only, no orders. Use when asked to run the Europe researcher, run stage EU, rank the day's European earnings names, or hunt London, Paris or Frankfurt prints.
---

# Stage EU — the European researcher

One signed number per company, so today's European names can be **ranked**. No call, no
threshold, no direction label. Identical question and identical output contract to the US
and Japanese stages, which is the point: if three markets are scored the same way, a
European result means something next to the other two.

**This stage places no orders and reads no broker.** There is no `alpaca_trade.py` step
here and there must not be one. Alpaca does not carry LSE, Euronext or XETRA anyway, and
execution is a separate decision to be made later on Europe's own resolved numbers.

## Three markets, one stage, and why

The regulatory spine is genuinely shared — MAR Article 17 ad-hoc disclosure, the
Transparency Directive's annual-plus-half-year floor, the Short Selling Regulation's 0.5%
public threshold — but that is not the reason. The reason is measured: **none of the three
is a daily market on its own.** The UK bottoms out at one eligible name on a Friday;
Germany puts 153 of 259 forward events in November and carries one in June; France is
semi-annual with 94 of 161 in February–March. They peak in different months, so pooling
three seasonal calendars is what produces one stream. See `researcher_europe/SUBMARKET.md`.

## What is different from the other two stages, and it matters

| | US (stage E) | Japan (stage J) | Europe (stage EU) |
| --- | --- | --- | --- |
| Calendar | Nasdaq vendor feed, 20/20 phantom on one day | JPX, the issuer's own notified date | TradingView vendor feed, **2 of 90 phantom** measured against RNS; day archives now exist for all three markets |
| Session | mixed bmo/amc | all amc | **89% bmo** — close(D−1) → close(D) |
| Option anchor | implied move + 25d skew | none; JPX shorts + 信用倍率 | **none**; FCA / Bundesanzeiger short registers |
| Tail | uncapped | 値幅制限 truncates | **uncapped** — maxima 42% / 27% / 52% |
| Names per day | 17–22, all hunted | 8–125, capped at 25 by random draw | median 6.5 above $200k, 2.5 above $1m, capped at 12 |
| Turnover floor | $200k | ¥30m (~$200k) | **$200k** since 2026-09-19 (was $1m); below $1m the register names 12% of issuers, and `anchor_covered` carries that |
| Hunters | one, English | one, Japanese | **three, one per market, English pass then local pass** |

**Europe reports before the open.** 339 of 379 measured UK results announcements landed
before 08:00 London. So the baseline for a `bmo` name must be sealed **the evening
before the print**, and `eu_universe.py --date` defaults to the next calendar day rather
than today. Getting the session backwards roughly halves the move being predicted.

**The option anchor was the hope and it did not materialise.** Yahoo carries zero
single-stock chains for `.L`, `.DE` and `.PA`; Eurex's free reference file has no
settlement prices, no open interest and no underlying map. Europe runs in the same
anchor-less regime as Japan, which is the regime that produced ρ=+0.073, p=0.45 over 104
events on the sealed corpus (`backtest/FINDINGS.md` §33). Say so in every note.

**What Europe does have is a better short register, and since 2026-09-19 all three
read.** The FCA resolves on **89% of the $1–5m turnover band** against 36–44% for
Japan's JPX register, and publishes a per-holder history back to 2012 where JPX's rolls
off. Germany works with a cookie. **France works too** — `www.data.gouv.fr` is
intermittent rather than blocked, so `eu_positioning.load_fr()` retries it for the
resource URL and pulls the file from `object-api.infra.data.gouv.fr`: 40,696 per-holder
rows since 2012, 74 issuers with an open position, and publication end dates that make
the change a measurement. `eu_resolve.py` still reports `lean_vs_free_control_rho` per
market — if it climbs back toward 1.0 for any market, that register has stopped
resolving.

## Steps

Resolve paths with `python3 scripts/run_paths.py --json`. Re-read the clock with
`date -u`; do not trust the date you were told at startup.

**0. Heartbeat, before you spend anything.**

```bash
python3 scripts/run_log.py --heading "Stage EU — Europe researcher — STARTED" --line "<the plan>"
scripts/publish.sh "stage EU: started for <YYYY-MM-DD>"
```

One cheap commit, and the only thing that distinguishes a Routine that never fired from
a session killed on its first subagent.

**1. Universe.** `<RUN>` is `research/<YYYY>/<MM>/<DATE>/europe/`.

```bash
python3 researcher_europe/scripts/eu_universe.py --date <EVENT-DATE> -o <RUN>/universe.json
```

`<EVENT-DATE>` is the day the print lands, which for a `bmo` name is the day AFTER the
session you are sealing against. It reads the vendor calendar for all three markets,
drops anything below **$200k** a day of turnover (normalised to USD off a live FX rate
written into the file — it was $1m until 2026-09-19), and if more than `cap` survive
takes a **random sample seeded by the date**. Report `selection.method`, `eligible`,
`hunted` and `by_market` in the note.

The floor matches the US and Japanese stages so all three markets are cut the same way.
It also means most names now arrive with **no positioning anchor**: below $1m/day the
national short register names 12% of issuers against 89% in the $1–5m band. Every
baseline carries `anchor_covered` and the note must say how many names had one.

The draw is random on purpose: any other cut is a second ranking the scorer cannot see,
and the US run has already paid for that once. It matters twice here — Phase 1 measured
sell-side coverage at 5–7 analysts in the $1–5m turnover band against 16–19 above $25m,
so cutting to the "under-read" band would bake this stage's own thesis into its universe
and make it unfalsifiable. The floor is for capacity and anchor coverage; the thesis is
tested afterwards, by band, in `eu_resolve.py`.

If `scheduled_today` is 0 on every market, check `per_market[*].market_closed` — the
three holiday calendars differ and are not the same as the national public holidays
(XETRA trades on Fronteichnam; Euronext Paris does not close for every jour férié).
Publish the empty universe, say why, and stop.

**2. Seal the baselines. Before any hunter.**

```bash
python3 researcher_europe/scripts/eu_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
```

Sealed means sealed. Nothing downstream may revise a baseline.

**3. One hunter per name, in the market's own agent.** Spawn `unpriced-hunter-uk`,
`unpriced-hunter-fr` or `unpriced-hunter-de` according to each baseline's `submarket`
field, in waves of `europe_hunt.wave_size`, publishing after each wave. Give each hunter
only its own ticker, the window, and the path to its own baseline. Never another name's
baseline, never another hunter's findings, never your own view.

A wave that completes is banked. **If a whole wave returns empty, stop** and write the
`— HALTED` section rather than starting another.

**4. Score.** The scorer is the US one, unchanged and deliberately so:

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
```

The ranking key is whatever `edge-scores.json` reports in `ranking_key`. Read it; do not
carry a remembered contract into the run.

**5. Note.** Write `<RUN>/europe-note.md`, answer first: the ranked table with the market
on every row, then the finding and URL driving the top and bottom name, then the names
that could not be ranked and why.

The note must also say, every time:

- `selection.method`, `by_market`, and that the draw was random among the eligible names
- which names carry `session_unresolved`, because their window was assumed rather than
  known and getting it wrong roughly halves the move
- that `options` is null in all three markets and Europe runs in the anchor-less regime
- which markets' short registers resolved, and **how many names carry
  `anchor_covered: true`** — a name the register was read for but does not name is a
  truncated zero, not an anchor, and under the $200k floor that is most of them
- `lean_vs_free_control_rho` per market from the previous resolved run if there is one
- that the lean's weights are priors borrowed from the US runs, measured nowhere in Europe
- for a German or French name, that `history.basis` is an estimated cadence — a scale and
  not a record of dates; UK names carry `observed_rns` and are the exception
- which names sit above `conviction_floor`, and that over the whole US sample the sign
  was a coin flip below it
- that one day is not a result

**6. Publish.**

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage EU: Europe ranking for <YYYY-MM-DD>"
```

## Resolving, the next session

```bash
python3 researcher_europe/scripts/eu_resolve.py --run <RUN>
```

Confirms each release, measures the correct window per session (and BOTH windows where
the session was unresolved), and reports Spearman against the realised move with a
permutation p, the controls, every lean component separately, per-market statistics and
the language-pass control.

**All three markets have a day archive since 2026-09-19** (`eu_archive.py`): the UK on
Investegate, France on the AMF's own `info-financiere.gouv.fr` flux — which carries the
issuer's declared filing category, so French results are classified by what was filed
and not by a headline keyword — and Germany on the EQS-News **search**, which paginates
back years where its front page does not.

So none of the three expires, and **resolving late is no longer a data-loss risk**. What
does differ: EQS has no whole-day query, so the German archive is assembled issuer by
issuer and a German name that is not found resolves **`event_occurred: null`, never
`false`**. The UK and France can reach `false`, because their archives were read in full
for that date and do not carry the issuer.

## The language experiment

Each hunter runs an **English pass first**, freezes it as `pre_local`, then runs the
local pass and revises. `edge_score.py` carries `diagnostics.impact_sum_pre_local` beside
the key and `eu_resolve.py` ranks both against the same realised move, so "searching in
German and French earns rank correlation" is measured rather than believed.

**The ordering is load-bearing.** English first, then local. Running local first tests a
different question and the two are not interchangeable.

**The UK case is degenerate and is reported apart.** Its local language is English, so its
second pass varies *source locality* (RNS, Investegate, the domestic trade press) rather
than language. `pre_local.variable` says which, and `eu_resolve.py` refuses to pool the UK
delta with the German and French ones. Averaging them would report the mean of two
different experiments.

**Nothing pools on one day.** A delta on four to twelve names is noise. Say so in the note.

## Budget

`config/pipeline.yaml`, `europe_hunt`. When the day would exceed the cap, shed by
`europe_hunt.degrade_order` and record what you shed in the run log. Half a run that
finishes beats a full one that gets cut off.

## The rule that outranks the rest

Never fabricate a number. Every company-specific figure carries a source URL or is marked
`unavailable`/`null`. **This matters more, not less, when the source is in a language the
reviewer may not read** — a translated paraphrase with no original string is
indistinguishable from an invented one, so every non-English finding quotes the original
beside the translation.

This is research, not investment advice. Keep the disclaimer from `config/pipeline.yaml`
on the note.
