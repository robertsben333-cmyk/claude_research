---
name: researcher-ipo-hunt
description: Stage IPO. The unpriced-information hunt pointed at two dated events in the life of a new US listing (NYSE, NYSE American and Nasdaq) - the debut, scored from the first trade to that day's close, and the lock-up expiry, scored from that session's open to its close. Seals what is known about each event before the open, sends one IPO hunter per name, sums the signed finding sizes into one number per company, then a blind four-model panel (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sizes the hunters' evidence and ranks beside it, as stage E-P does. Research only, no orders. Use when asked to run stage IPO, the IPO researcher, rank today's IPO debuts or lock-up expiries, or hunt IPOs.
---

# Stage IPO — the IPO researcher

One signed number per company, so the day's IPO events can be **ranked**. No call, no
threshold, no direction label. Same finding contract and same scorer as every other
stage, plus stage E-P's four-model panel on the hunters' evidence.

Read `CLAUDE.md` first, then `researcher_ipo/README.md`, then come back here.

## The two events and their one window shape

| event | the session | window | what is NOT scored |
| --- | --- | --- | --- |
| `debut` | the first session the IPO trades | **first trade (the opening cross) → that session's close** | the pop from the offer price to the first trade: nobody here gets an allocation |
| `lockup` | the first session after Nasdaq's lock-up expiration date | **that session's open → its close** | the run-in before the date and the overnight gap into the open |

The quiet-period expiry was left out on the operator's choice. Both windows open after
the Routine fires (08:35 New York) and close the same afternoon, so **the outcome does
not exist anywhere while the hunters run**. A hand-run later in the day is different:
the hunter definition says what to do then.

## What phase 0 established, before any agent existed

`researcher_ipo/analysis/phase0-base-rates.json`, built by
`researcher_ipo/scripts/ipo_backtest.py` over 26 months of priced deals. Read
`researcher_ipo/README.md` for the table and its biases. The base rates travel into
every baseline under `phase0`, so the hunters and judges size against measured numbers.

## Steps

Resolve paths with `python3 scripts/run_paths.py --json`. `<RUN>` is
`research/<YYYY>/<MM>/<DATE>/ipo/`. Re-read the clock with `date -u`; do not trust the
date you were told at startup. `<DATE>` is today in New York.

**0. Heartbeat, before you spend anything.**

```bash
python3 scripts/run_log.py --heading "Stage IPO — IPO researcher — STARTED" --line "<the plan>"
scripts/publish.sh "stage IPO: started for <YYYY-MM-DD>"
```

**1. Universe.**

```bash
python3 researcher_ipo/scripts/ipo_universe.py -o <RUN>/universe.json
```

Debuts first-trading today and lock-ups whose first free session is today, SPACs out,
debuts under `ipo_hunt.min_deal_usd` out, lock-ups under the $200k turnover floor out,
a date-seeded random draw above `cap`. Report the `funnel` in the note.

**An empty day is the normal day.** About one event a session over a year, and most
sessions carry none. `market_closed` set means NYSE is shut. Either way: publish the
universe, append one line to the run log saying which case it is, and stop.

**2. Seal the baselines. Before any hunter.**

```bash
python3 researcher_ipo/scripts/ipo_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
```

Sealed means sealed: nothing downstream revises a baseline, except the retrospective
`event_occurred: false`, added after the window with its source. A debut sealed with
`offer_price_final: false` has not been flipped to priced on Nasdaq's calendar yet; the
hunter confirms the pricing press release, and the note says which names were sealed on
a range.

**2b. Record which prompt and model this run uses. Before any hunter.**

```bash
python3 scripts/provenance.py stamp --run <RUN> --market IPO --orchestrator-model "<model>"
```

`<model>` is `session_context.model` from the `get_session` tool when you can call it;
leave the flag out otherwise.

**3. One hunter per name.** Spawn `unpriced-hunter-ipo`, in waves of
`ipo_hunt.wave_size`, publishing after each wave. Give each hunter only its own ticker,
its event type, the window, the path to its own baseline and its output path
`<RUN>/hunts/<TICKER>.json`. Never another name's baseline, never another hunter's
findings, never your own view.

If `unpriced-hunter-ipo` comes back "not found", launch `general-purpose` with the body
of `.claude/agents/unpriced-hunter-ipo.md` pasted in and `model: opus`, and record which
form ran. A wave that comes back entirely empty: stop, and write a `— HALTED` section.

**4. Score.** The shared scorer, unchanged:

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
python3 scripts/score_report.py --run <RUN> --label "Stage IPO"
```

The ranking key is whatever `edge-scores.json` reports in `ranking_key`. A hunter that
returned `event_confirmed: false` (a debut postponed, a lock-up already released) is not
ranked; that is the scorer's rule, not yours to override.

**4p. The four-model panel.** Follow `config/market-panel-step.md` exactly, with
`--market IPO`, run-log heading `Stage IPO — panel STARTED`, publish prefix
`stage IPO:`, and **the IPO judges**, not the `-intl-` ones:

```bash
python3 scripts/market_panel.py packs --market IPO --run <RUN>
# heartbeat + publish, then the four judges in ONE message:
#   panel-judge-ipo-opus5, -opus55, -sonnet55, -fable51, each given only the packs file
python3 scripts/market_panel.py check --market IPO --run <RUN>
python3 scripts/market_panel.py score --market IPO --run <RUN>
```

| member | agent | fallback if the agent or its model is refused |
| --- | --- | --- |
| `opus5` | `panel-judge-ipo-opus5` (`claude-opus-5`) | **none**: run without it and record it missing |
| `opus55` | `panel-judge-ipo-opus55` (`claude-opus-5-5`) | `general-purpose`, `model: opus`, body of `config/panel-judge-ipo.md` pasted in |
| `sonnet55` | `panel-judge-ipo-sonnet55` (`claude-sonnet-5-5`) | `general-purpose`, `model: sonnet`, same |
| `fable51` | `panel-judge-ipo-fable51` (`claude-fable-5-1`) | `general-purpose`, `model: fable`, same |

Each judge gets this prompt and nothing else: *"Follow your definition. Your packs file is
`<RUN>/panel/packs.json`. Write your JSON array to `<RUN>/panel/<member>.json`. Use only
Read and Write."* Never give a judge the hunts, the scores, another judge's file or your
own view.

**The first IPO panel run seeds the history.** If `score` stops on a missing
`researcher_ipo/analysis/panel-history.json`, run
`python3 scripts/market_panel.py seed --market IPO` once and score again. The seed is
stage E-P's earnings-scale history; this stage reads only the last 60 names, so its own
sizes replace the seed within a few months. Until then "own top 20%" is measured against
earnings prints and the selection will be sparse. Say so in the note.

**5. Note.** `<RUN>/ipo-note.md`, answer first:

1. Three lines at the top: **this is stage IPO: debuts scored from the first trade to the
   close, lock-ups from the open to the close, a blind four-model panel, no orders**;
   which judges ran; that one day is an anecdote and this stage is judged pooled.
2. The ranked table: rank, ticker, event type, `impact_sum`, `impact_scaled`, the panel's
   `selected`, `consensus_k` and `panel_score`.
3. The panel section from `config/market-panel-step.md` ("In the note").
4. Per name, the finding and URL driving its number, and the strongest case against.
5. Per debut: the offer price or range it was sealed on, the deal size, and the recent
   debuts' first-trade-to-close median from the baseline. Per lock-up: the expiration
   date, `early_release_checked` as the hunter left it, price versus offer and the
   share of the company that unlocks.
6. The `funnel`, and every name that could not be ranked and why.
7. What the numbers are not: the 2.8 conviction floor was measured on earnings prints;
   the panel's member scales are still the borrowed E-P seed; nothing has resolved.

Keep the disclaimer from `config/pipeline.yaml` on the note.

**6. Publish.**

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage IPO: IPO ranking for <YYYY-MM-DD>"
```

The closing chat reply pastes the `score_report.py` output verbatim, then the panel
table from `market_panel.py score`, then the funnel in one line.

## Resolving, after the close

```bash
python3 researcher_ipo/scripts/ipo_resolve.py --run <RUN>
python3 scripts/market_panel.py resolve --market IPO --run <RUN>
python3 researcher_ipo/scripts/ipo_resolve.py --pool
```

The first writes `<RUN>/ipo-resolved.json` (key moves, moves net of IWM, the pop and the
other convention beside them, `event_occurred: false` for a debut that did not trade
that day). The third pools every resolved run, debuts and lock-ups apart. **Read the
pooled file, never a single day.**

## Budget

`config/pipeline.yaml`, `ipo_hunt`: up to 12 hunters in waves of 6, then one wave of four
judges. Shed names before the panel, never a judge.

## The rule that outranks the rest

Never fabricate a number. Every company-specific figure carries a source URL or is
marked `unavailable`/`null`. An IPO's coverage is thin and its press is promotional, so
this matters more here than in the earnings stages: a book that is "multiple times
oversubscribed" with no named source is not a finding.

This is research, not investment advice.
