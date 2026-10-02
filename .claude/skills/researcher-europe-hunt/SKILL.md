---
name: researcher-europe-hunt
description: The unpriced-information hunt, run over ten European markets pooled - the UK, France, Germany, Sweden, Denmark, Norway, Finland, Italy, Spain and Poland. Seals what the market has priced into each company reporting into the next European session, sends one language-specific hunter per name to find what is not in that price, and sums their signed finding sizes into one number per company so the day's names can be ranked. Research only, no orders. Use when asked to run the Europe researcher, run stage EU, rank the day's European earnings names, or hunt London, Paris, Frankfurt, Stockholm, Copenhagen, Oslo, Helsinki, Milan, Madrid or Warsaw prints.
---

# Stage EU — the European researcher

One signed number per company, so today's European names can be **ranked**. No call, no
threshold, no direction label. Identical question and identical output contract to the US
and Japanese stages, which is the point: if three regions are scored the same way, a
European result means something next to the other two.

**This stage places no orders and reads no broker.** There is no `alpaca_trade.py` step
here and there must not be one. Alpaca carries none of these ten venues anyway, and
execution is a separate decision to be made later on Europe's own resolved numbers.

## Ten markets, one stage, and why

The regulatory spine is genuinely shared — MAR Article 17 ad-hoc disclosure, the
Transparency Directive's annual-plus-half-year floor, the Short Selling Regulation's 0.5%
public threshold — but that is not the reason. The reason is measured: **no European
market is a daily market on its own.** The UK bottoms out at one eligible name on a
Friday; Germany puts 153 of 259 forward events in November and carries one in June;
France is semi-annual with 94 of 161 in February–March. They peak in different months, so
pooling seasonal calendars is what produces one stream. See
`researcher_europe/SUBMARKET.md`.

**Seven markets were added on 2026-09-19** — Stockholm, Copenhagen, Oslo, Helsinki,
Milan, Madrid and Warsaw — and the cap went from 12 to 20 with them. The measurement
that justifies it is seasonal, and the obvious one says the opposite: over the ten
sessions 2026-09-21 → 10-02 the seven add **six names**, because late September is the
UK's month. By month of forward vendor events:

| month | UK+DE+FR | the new seven |
| --- | --- | --- |
| Sep 2026 | 161 | 13 |
| **Oct 2026** | **114** — the existing stage's thinnest | **456** |
| Nov 2026 | 309 | 515 |
| Feb 2027 | 133 | 38 |
| Mar 2027 | 250 | 70 |

And the cadence is better: measured median gaps of 91–98 days across the Nordics and
Poland against the UK's 217 and France's 204, so a Nordic name recurs four times a year
where a UK one recurs twice.

## The ten are NOT equally instrumented, and this is the first thing to say in any note

`eu_market.CAPABILITY` is the measured table and the code reads it rather than assuming.

| markets | short register | day archive | `event_occurred: false` |
| --- | --- | --- | --- |
| **uk** | FCA, with history | Investegate, by date to 1999 | yes |
| **no** | dated event history per issuer | Oslo NewsWeb, true day query, **ticker-keyed** | yes |
| **fr** | AMF, per-holder to 2012 | AMF flux, issuer's own category — **lags the press release** | **no** (since 2026-09-28) |
| **it** | CONSOB xlsx, WAF-retried | eMarket STORAGE, WAF-retried, **not universal** | **no** (since 2026-09-22) |
| **se dk fi** | national, snapshot | Nasdaq Nordic, **paged, no date query** | only inside the feed's ~12-day window |
| **de** | Bundesanzeiger, snapshot | EQS, per issuer only | **no** |
| **es pl** | **none reachable** | **none reachable** | **no** |

**Norway is now the best-instrumented market in this stage after the UK** — it is the
second of the ten whose `history` carries *observed* announcement dates rather than a
cadence estimate.

**Spain and Poland are the weak legs and must be described as such.** A Spanish or
Polish name is hunted with **no positioning anchor**: its `priced_lean_pct` falls back to
the 20-day run-up, which is also the free control the whole stage is measured against, so
that name cannot beat the benchmark with anything that uses it. And it can never be
confirmed or killed after the fact. Both were given the eight-try standard that rescued
France and Italy and failed it. If a pooled ρ is quoted without saying how much of it is
`es`/`pl`, it is being oversold.

## What is different from the other two stages, and it matters

| | US (stage E) | Japan (stage J) | Europe (stage EU) |
| --- | --- | --- | --- |
| Calendar | Nasdaq vendor feed, 20/20 phantom on one day | JPX, the issuer's own notified date | TradingView vendor feed, **2 of 90 phantom** measured against RNS; day archives exist for eight of the ten. **Forward-date coverage is very uneven**: 0.88 of Finnish and 0.81 of Norwegian issuers carry one, against 0.20 Italian, 0.19 Spanish, 0.13 Polish |
| Session | mixed bmo/amc | all amc | **89% bmo** — close(D−1) → close(D) |
| Option anchor | implied move + 25d skew | none; JPX shorts + 信用倍率 | **none**; eight national short registers, **two markets have none at all** |
| Tail | uncapped | 値幅制限 truncates | **uncapped** — maxima 42% / 27% / 52% |
| Names per day | 17–22, all hunted | 8–125, capped at 25 by random draw | 65 eligible on 2026-10-22; capped at **20** |
| Turnover floor | $200k | ¥15m (~$100k) | **$100k** since 2026-10-01 ($200k from 2026-09-19, $1m before); below $1m the register names 12% of issuers, and `anchor_covered` carries that |
| Hunters | one, English | one, Japanese | **seven definitions over ten markets, one bilingual pass each** |

**Europe reports before the open.** 339 of 379 measured UK results announcements landed
before 08:00 London. So the baseline for a `bmo` name must be sealed **the evening
before the print**, and `eu_universe.py --date` defaults to the next calendar day rather
than today. Getting the session backwards roughly halves the move being predicted.

**The option anchor was the hope and it did not materialise.** Yahoo carries zero
single-stock chains for `.L`, `.DE` and `.PA`; Eurex's free reference file has no
settlement prices, no open interest and no underlying map. Europe runs in the same
anchor-less regime as Japan, which is the regime that produced ρ=+0.073, p=0.45 over 104
events on the sealed corpus (`backtest/FINDINGS.md` §33). Say so in every note.

**What Europe does have is a better short register, and eight of the ten read.** The FCA resolves on **89% of the $1–5m turnover band** against 36–44% for
Japan's JPX register, and publishes a per-holder history back to 2012 where JPX's rolls
off. Germany works with a cookie. **France works too** — `www.data.gouv.fr` is
intermittent rather than blocked, so `eu_positioning.load_fr()` retries it for the
resource URL and pulls the file from `object-api.infra.data.gouv.fr`: 40,696 per-holder
rows since 2012, 74 issuers with an open position, and publication end dates that make
the change a measurement. `eu_resolve.py` still reports `lean_vs_free_control_rho` per
market — if it climbs back toward 1.0 for a market that was below it, that register has
stopped resolving. It should read ~1.0 for **Spain and Poland by construction**, because
those two have no register at all.

The seven added in 2026-09 bring five more registers: Finansinspektionen (SE),
Finanstilsynet (DK **at a 0.1% threshold, not 0.5% — a Danish aggregate is not on the
same scale as anyone else's**), Finanstilsynet (NO, a dated event history and the best of
the ten), Finanssivalvonta (FI) and CONSOB (IT, behind a retried WAF). Sweden, Denmark,
Finland and Italy publish the **current position only**, so their `short_change_pct_pts`
is null until two days are cached — and null there means *not known*, never *no change*.

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
session you are sealing against. It reads the vendor calendar for **all ten markets**,
drops anything below **$100k** a day of turnover (normalised to USD off a live FX rate in
six currencies, written into the file — $100k since 2026-10-01, $200k from 2026-09-19, $1m before), and if more than
`cap` survive (**20** since 2026-09-19) takes a **random sample seeded by the date**.
Report `selection.method`, `eligible`, `eligible_by_market`, `hunted` and `by_market` in
the note.

**Read `selection.market_concentration` and put it in the note.** The draw is random and
the calendar is seasonal, so a day can be almost entirely one market — 15 of 20 names
were Swedish on 2026-10-22, because October is Sweden's month. That is a correlated
exposure the scorer cannot see, the same shape as the four US names the IEEPA tariff
refunds ranked together. The draw is deliberately *not* stratified by market, because a
per-market quota is a second selection and this stage has already paid once for a cut the
scorer could not see — so the concentration is reported instead.

The floor matches the US and Japanese stages so all ten markets are cut the same way.
It also means most names now arrive with **no positioning anchor**: below $1m/day the
national short register names 12% of issuers against 89% in the $1–5m band. Every
baseline carries `anchor_covered` and the note must say how many names had one.

The draw is random on purpose: any other cut is a second ranking the scorer cannot see,
and the US run has already paid for that once. It matters twice here — Phase 1 measured
sell-side coverage at 5–7 analysts in the $1–5m turnover band against 16–19 above $25m,
so cutting to the "under-read" band would bake this stage's own thesis into its universe
and make it unfalsifiable. The floor is for capacity and anchor coverage; the thesis is
tested afterwards, by band, in `eu_resolve.py`.

If `scheduled_today` is 0 on every market, check `per_market[*].market_closed` — the ten
holiday calendars differ and are not the same as the national public holidays (XETRA
trades on Fronleichnam; Euronext Paris does not close for every jour férié; Stockholm and
Helsinki shut for Midsummer Eve, which moves). **Only the UK's calendar is fetched live**;
the other nine are hand-entered from each exchange's published trading calendar, so a
wrong entry is possible and shows up as `market_closed` in the universe file rather than
only in the code. Publish the empty universe, say why, and stop.

`per_market[*].off_primary_exchange_filtered` counts rows dropped because the vendor's
country scanner pools venues: `sweden` carries 230 NGM names beside 663 OMXSTO ones, and
`poland` carries 325 NewConnect names beside 384 GPW ones. NGM names do not take Yahoo's
`.ST` at all, so they would be screened on somebody else's tape.

**2. Seal the baselines. Before any hunter.**

```bash
python3 researcher_europe/scripts/eu_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
```

Sealed means sealed. Nothing downstream may revise a baseline.

**2b. Record which prompt and model this run uses. Before any hunter.**

```bash
python3 scripts/provenance.py stamp --run <RUN> --market EU --orchestrator-model "<model>"
```

`<model>` is `session_context.model` from the `get_session` tool when you can call it;
leave the flag out otherwise. It writes `<RUN>/provenance.json`: the version of the
hunter definition the hunters are about to read (for example `jp.v5`), the model its
alias serves, and the blobs of the LESSONS file, the shared hunter core and this skill.
The dashboard groups every number by version and model, so a run without this file is
placed by date and labelled as inferred. If it prints `unregistered-…`, the definition
changed on `main` without `config/prompt-versions.json` being rebuilt; carry on, and say
so in the run log, because the blob still identifies the exact text.

**3. One hunter per name, in the market's own agent.** Dispatch on each baseline's
`submarket` field — the mapping is `MARKETS[<submarket>]["hunter"]`, so read it rather
than remembering it:

| submarket | agent |
| --- | --- |
| `uk` | `unpriced-hunter-uk` |
| `de` | `unpriced-hunter-de` |
| `fr` | `unpriced-hunter-fr` |
| `se` `dk` `no` `fi` | `unpriced-hunter-nordic` — **tell it which one**, it covers four |
| `it` | `unpriced-hunter-it` |
| `es` | `unpriced-hunter-es` |
| `pl` | `unpriced-hunter-pl` |

Run them in waves of `europe_hunt.wave_size` (5), publishing after each wave. Give each
hunter only its own ticker, the window, and the path to its own baseline. Never another
name's baseline, never another hunter's findings, never your own view.

A wave that completes is banked. **If a whole wave returns empty, stop** and write the
`— HALTED` section rather than starting another.

**4. Score.** The scorer is the US one, unchanged and deliberately so:

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
```

The ranking key is whatever `edge-scores.json` reports in `ranking_key`. Read it; do not
carry a remembered contract into the run.

**4b. Report both keys in the chat reply.** `edge_score.py` also writes
`edge-scores-scaled.json`, ranked on `impact_scaled` = (2 × `p_up` / 100 − 1) ×
`abs_move_pct`: the hunter's second, separate measurement (version 3 of the sizing, the
hunter core step 3). `impact_sum` stays the key (version 2: each finding sized on its own,
added up). Print both side by side:

```bash
python3 scripts/score_report.py --run <RUN> --label "Stage EU"
```

and paste its output verbatim at the top of your closing chat reply. Never rank on,
pool or quote `impact_scaled` as the key, and do not apply the conviction floor to it.

**5. Note.** Write `<RUN>/europe-note.md`, answer first: the ranked table with the market
on every row, then the finding and URL driving the top and bottom name, then the names
that could not be ranked and why.

The note must also say, every time:

- `selection.method`, `by_market`, and that the draw was random among the eligible names
- which names carry `session_unresolved`, because their window was assumed rather than
  known and getting it wrong roughly halves the move
- that `options` is null in all ten markets and Europe runs in the anchor-less regime
- which markets' short registers resolved, and **how many names carry
  `anchor_covered: true`** — a name the register was read for but does not name is a
  truncated zero, not an anchor, and under the $100k floor that is most of them
- **how many of the day's names came from Spain or Poland**, which have no positioning
  anchor and no way to be confirmed after the fact, and how many from Germany, which
  cannot reach `event_occurred: false` either
- `selection.market_concentration` — if one market is most of the day, say so before any
  pooled number
- `lean_vs_free_control_rho` per market from the previous resolved run if there is one
- that the lean's weights are priors borrowed from the US runs, measured nowhere in Europe
- which names carry an **estimated** `history.basis` — a scale, not a record of dates.
  Only UK names (`observed_rns`) and Norwegian ones (`observed_newsweb`) are real; the
  other eight markets are cadence estimates, and reading a cadence prior as evidence is
  how TRT got ranked, traded and never reported
- which names sit above `conviction_floor`, and that over the whole US sample the sign
  was a coin flip below it
- per name, the hunter's `abs_move_pct` and `p_up` beside `impact_sum`, and which names
  had **already pre-released the period** (`already_public`) or face a **likely guidance
  change** (`new_in_release`). On the first resolved days those two facts decided the
  size of the move — 3.1% against 7.4%, and 9.0% against 2.3% — while the emitted sizes
  barely differed, so a note that shows them lets a reader see whether the sizing has
  caught up (see the hunters' "Size and certainty" section)
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
the language-pass control — which reports 0 names on any run sealed after 2026-09-22,
because the hunters stopped freezing an English-only draft that day. An empty section
there is the report, not a fault.

**Then pool, because one day is noise.** `eu_resolve.py` now also writes
`stats.size_and_certainty` per run: the hunter's magnitude against the move's
(`abs_move_pct`, `expected_move_pct`, `impact_sum`), the ratio between them, and a Brier
score for `p_up`. None of that means anything on nine names, so read it pooled:

```bash
python3 researcher_europe/scripts/eu_calibration.py
```

It pools every resolved non-validation run and reports SIZE (does the hunter's magnitude
rank the move's, and at what level), DIRECTION (sign, `p_up` against a coin), CERTAINTY
(does anything the hunter emits tell a right sign from a wrong one) and which `lands_on`
lines carry direction.

**And write the post-mortem, because it is the only thing that says WHY.** The rank
correlation cannot tell a hunter that got the number wrong from one that got the number
right and the reaction wrong, and the fix for each is different. Within a week of the
print, for every resolved name, fill `<RUN>/eu-postmortem.json` from the release itself —
one object per ticker with `print_vs_bar_actual_pct` (against the bar the hunter named),
`guidance_change`, `prior_update` (`{"value", "date", "url"}`: had a trading update
already disclosed the period?), `moved_on` (one of the `lands_on` values) with a URL, and
`findings_scored` (`fact_correct` per finding). A general-purpose subagent per five names
does it in about four minutes; the outcome exists, so there is nothing to contaminate.
`eu_calibration.py` reads those files and prints the number-versus-reaction matrix.
The first one, over 2026-09-22 → 09-25, is what `researcher_europe/LESSONS.md`'s
measured section rests on.

**Check the session against the release timestamp while you are there.** Adocia was
sealed `bmo` for 2026-09-24 and released at 18:00 CEST, after the Paris close: the scored
window ended before the release and the 20% fall the next day is in no sample. A vendor
session flag is a guess until a timestamp says otherwise.

**Eight of the ten markets have a day archive** (`eu_archive.py`): the UK on Investegate,
France on the AMF's `info-financiere.gouv.fr` flux, Germany on the EQS-News **search**,
Sweden/Denmark/Finland on the **Nasdaq Nordic disclosure feed**, Norway on **Oslo Børs
NewsWeb** and Italy on **eMarket STORAGE**. France and the Nordics carry the issuer's own
release category, so their results are classified by what was filed rather than by a
headline keyword.

**Three things differ by market and the resolved file states each one per run**
(`confirmation[*].false_reachable`, `archive_kind`, `archive_read`):

- **Germany, Spain, Poland, Italy and — since 2026-09-28 — France can never reach
  `event_occurred: false`.** France's AMF flux carries the regulated filing, which can
  land days after the results press release: ABC arbitrage released at 07:00 CEST on
  2026-09-22 and first appears in the flux on 09-24, so the resolver killed a name that
  reported and rose 11%. The flux still confirms; absence from it is null. And the
  Nordic feed spells some issuers in another word order (`Hennes & Mauritz AB, H & M`),
  which killed H&M's nine-month report until `eu_archive.same_issuer()` matched on the
  words rather than the prefix. **Two of the first four European kills were wrong** —
  a kill removes a name from every sample, so read each one before believing it.
- **Germany, Spain and Poland** in detail: EQS has no
  whole-day query, so a German name is searched by issuer and "not found" cannot be told
  from "the search term missed". Spain and Poland have no archive at all.
- **Sweden, Denmark and Finland can reach it only for a recent print.** The Nasdaq feed's
  `fromDate` is **accepted and ignored** — it returns the most recent rows for any date
  you ask for — so the code never passes it and pages back instead, roughly two days a
  request and about twelve days before it stops being cheap. Beyond that window the
  archive returns `None` and every row resolves null. **So a Nordic run should be
  resolved within about a week.**
- **Italy is behind a WAF** that answers about 7 of 8, and eMarket STORAGE's `data_to` is
  **exclusive** — a naive single-day query returns zero rows and looks exactly like a
  silent day.

`day()` returns **`None`, not `[]`**, where a source could not be read. That distinction
is the only thing between "nobody announced anything" and "I could not look", and only
the first may ever support a kill.

## The language experiment, and why it stopped

**The hunters run ONE pass in English and the local language together, since
2026-09-22.** Until that day each ran an English pass first, froze it as `pre_local`,
and only then searched locally; `edge_score.py` carried
`diagnostics.impact_sum_pre_local` beside the key and `eu_resolve.py` ranked both
against the same realised move, so "searching in German and French earns rank
correlation" was a measured claim rather than a believed one.

**It was retired on the operator's instruction, and the reason is not only tokens.**
Sequencing the two halves forbade them from informing each other — a German filing is
often the reason to run a particular English query, and an English wire item the reason
to go and find the German original — so the control was being paid for out of the
quality of the research it was measuring.

**What that cost is worth stating plainly.** Nothing measures the local half any more.
It cannot be recovered from a run after the fact, because a freeze reconstructed later
is not a freeze. The one thing that softens it: **no European day had resolved while the
control ran**, so `spearman_pre_local` never produced a number against a real outcome.
What was given up is a future measurement, not a result.

**What replaces it is prose.** Every hunter emits `language_note`: one line per thing
the local-language sources carried that the English ones did not, or the single line
'nothing the English sources did not already carry'. Nothing ranks it. The note should
quote it where it is interesting, and should not present it as evidence.

**The UK case was degenerate and the asymmetry survives.** Its local language is
English, so its local half varies *source locality* (RNS, Investegate, the domestic
trade press) rather than language, and a UK `language_note` saying the domestic sources
added nothing is an honest result rather than a lazy hunt.

**The Nordic case is weaker than the others and the hunter is told so.** Nordic issuers
publish in English as a matter of routine — most releases go out in both languages at
once, which is not true in Germany, France or Italy. A Nordic `language_note` that reads
'nothing the English sources did not already carry' is the expected answer there more
often than anywhere else in the stage.

**`eu_resolve.py` still reports the old control and will read 0 names.** That is the
honest report of a control that no longer runs, not a hunter that forgot to freeze. The
runs sealed before 2026-09-22 keep their diagnostics and the dashboard's `Taal` tab
still shows them, labelled as history.

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
