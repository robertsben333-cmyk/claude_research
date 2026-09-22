---
name: researcher-australia-hunt
description: The unpriced-information hunt, run over the Australian market. Seals what the market has priced into each ASX company reporting into the next Sydney session, sends one English-language hunter per name to find what is not in that price, and sums their signed finding sizes into one number per company so the day's names can be ranked. Research only, no orders. Use when asked to run the Australia researcher, run stage AU, rank the day's ASX earnings names, or hunt Sydney prints.
---

# Stage AU — the Australian researcher

One signed number per company, so the day's ASX names can be **ranked**. No call, no
threshold, no direction label. Identical question and identical output contract to the
US, Japanese and European stages, which is the point: scored the same way, the
Australian result means something next to the others.

**This stage places no orders and reads no broker.** There is no `alpaca_trade.py` step
here and there must not be one. Alpaca does not carry the ASX. It is research.

## What is different, and all of it matters

| | US (stage E) | Australia (stage AU) |
| --- | --- | --- |
| Calendar | Nasdaq vendor feed | TradingView vendor feed, **dates shifted to Sydney time** |
| Event window | after US close → before next open | **close(D−1) → close(D)**, because 91% report pre-open |
| Sealed | on the day | **the evening before**, after the Sydney close |
| Option anchor | implied move + 25d skew | none; substituted by ASIC's short register |
| Short register | — | **daily, untruncated, back to 2010** — the best in the repo |
| Reaction history | real dates | **real dates**, from the ASX archive |
| Hunter passes | one | **one** — no local-language pass, deliberately |
| Tail | uncapped | **uncapped**; no daily price limit, unlike Tokyo |

**The seal happens the evening before the print.** Measured 2026-09-22 against the ASX
announcement record, 67 of 74 results announcements (91%) landed before the 10:00 Sydney
open. So `au_universe.py --date` defaults to the **next** ASX session and the Routine
fires at 06:30 UTC, after the 16:00 Sydney close. Sealing on the morning of the print
would seal after the event.

**The vendor's date is wrong by one day for 85% of Australian rows, and the code fixes
it.** The vendor stamps the UTC instant and Sydney is ten or eleven hours ahead of it, so
BHP's 08:31 Sydney lodgement on 18 August reads as 17 August. `au_market.sydney_event_date()`
converts the instant rather than adding a constant, so it survives the daylight-saving
change on 2026-10-04. Every row carries `event_date_basis`. Do not "correct" it back.

**The missing option anchor is substituted, and the substitute is better than Tokyo's or
Europe's.** No ASX single-stock chain is retrievable here (AAPL 22 expiries, `BHP.AX`
zero, measured 2026-09-22), so `options` is all null. In its place the baseline carries
ASIC's aggregated daily short position — and unlike every other register in this repo it
is **not a 0.5% disclosure threshold**: 430 of the 755 rows on 2026-09-16 were below
0.5%, minimum 0.000000%. So the level is a real number at every size and there is no
`anchor_covered` arm to split out, because there are no truncated zeros. What it costs is
the **lag**: ASIC publishes about four business days in arrears, carried as
`positioning.lag_sessions` and never to be treated as zero.

**Half the ASX lodges a cash-flow report, not a profit result.** `history.filer_type` is
`results` (Appendix 4D/4E), `quarterly_report_only` (Appendix 4C/5B under Listing Rule
4.7B) or `none_found`. These are different events with different bars and the note must
report the mix. `none_found` on an issuer whose three years of archive read cleanly is a
reason to doubt the print exists at all.

**The hunters run one English pass and there is no second language to search.** There is
no Australian-language press the wires do not read, and the entire regulated disclosure
channel is one English feed everybody reads. **`unpriced-hunter-au` has no `pre_local`
field and no `language_note`. Do not add either.** The `pre_lessons` freeze still runs.

Stage EU and stage CA dropped their own `pre_local` freeze on 2026-09-22 and now run one
bilingual pass each, so this is no longer the exception it was. The difference that
remains is that they have a second language to search and Australia does not: they carry
a prose `language_note` and this stage carries none. A field that would be structurally
empty on every Australian name is worse than absent — somebody would eventually pool it.

## Steps

Resolve paths with `python3 scripts/run_paths.py --json`. Re-read the clock with
`date -u`; do not trust the date you were told at startup.

**0. Heartbeat, before you spend anything.**

```bash
python3 scripts/run_log.py --heading "Stage AU — Australia researcher — STARTED" --line "<the plan>"
scripts/publish.sh "stage AU: started for <YYYY-MM-DD>"
```

One cheap commit, and the only thing that distinguishes a Routine that never fired from
a session killed on its first subagent.

**1. Universe.** `<RUN>` is `research/<YYYY>/<MM>/<DATE>/australia/`, where `<DATE>` is
the **event date**, which is the next Sydney session, not today.

```bash
python3 researcher_australia/scripts/au_universe.py -o <RUN>/universe.json
```

It scans the vendor calendar, shifts every date to Sydney time, keeps the rows landing
on the target session, drops names below $200k/day of turnover, folds second share
classes into their issuer, and if more than `cap` survive takes a **random sample seeded
by the date**. Report `selection.method`, `eligible` and `hunted` in the note. The draw
is random on purpose: any other cut is a second ranking the scorer cannot see, and the US
run has already paid for that once.

**Read the reason for an empty universe rather than guessing it.** `market_open` false
means the ASX is shut and there is nothing to wait for. `market_open` null with the note
about the index tape means the fetch failed, which is a container fault and not a quiet
market — do not hunt on that file. `scheduled_today` 0 on an open day is a normal thin
Australian session, most likely outside the February and August reporting seasons.
Publish the empty universe, say which case it is in one line, and stop.

**2. Seal the baselines. Before any hunter.**

```bash
python3 researcher_australia/scripts/au_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
```

Sealed means sealed. Nothing downstream may revise a baseline. If the ASIC register
could not be read the script says so loudly: `priced_lean_pct` then falls back to the
run-up alone, which **is** the free control, and the baseline has no independent
directional content. That belongs in the note, not in a log line.

**3. One hunter per name.** Spawn `unpriced-hunter-au`, in waves of
`australia_hunt.wave_size`, publishing after each wave. Give each hunter only its own ASX
code, the window, and the path to its own baseline. Never another name's baseline, never
another hunter's findings, never your own view.

A wave that completes is banked. **If a whole wave returns empty, stop** and write the
`— HALTED` section rather than starting another.

**4. Score.** The scorer is the US one, unchanged and deliberately so:

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
```

The ranking key is whatever `edge-scores.json` reports in `ranking_key`. Read it; do not
carry a remembered contract into the run.

**5. Note.** Write `<RUN>/australia-note.md`, answer first: the ranked table, then the
finding and URL driving the top and bottom name, then the names that could not be ranked
and why.

The note must also say, every time:

- `selection.method`, and that the draw was random among the eligible names
- the **filer-type mix**: how many names lodge a 4D/4E and how many a 4C/5B, because
  those are different events and a pooled ranking spans both
- the **register lag** in sessions, and that a "shorts are building" reading may be
  describing history on a name that has already moved
- `lean_vs_free_control_rho` from the previous resolved run if there is one, because it
  is the check that the lean has not collapsed back into the free control
- that the lean's weights are **priors carried over from stage J** with no Australian
  measurement behind them
- how many names carried `session_unresolved`
- which names sit above `conviction_floor`, and that over the whole US sample the sign
  was a coin flip below it
- that **nothing has resolved in Australia**, that this stage runs anchor-less in the
  regime `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073 over 104 events, and that
  one day is not a result

**6. Publish.**

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage AU: Australia ranking for <YYYY-MM-DD>"
```

## Resolving, after the print

```bash
python3 researcher_australia/scripts/au_resolve.py --run <RUN> -o <RUN>/resolved.json
```

Confirms each print against the ASX per-issuer archive, measures the move over the sealed
window off daily closes, and reports Spearman against the realised move with a
permutation p, the two free controls, every lean component separately, and a split by
filer type. It **refuses to settle `event_occurred` for a date that has not passed** —
stage EU shipped a resolver that killed names which simply had not reported yet.

Yahoo's non-US daily closes can lag, so every row carries `move_pending` and the summary
warns when all of them are. That is a data lag, never a day on which nothing moved.

Unlike Tokyo, the confirmation source does not expire: the ASX archive is queryable by
year and goes back years, so a late resolve loses nothing.

## Budget

`config/pipeline.yaml`, `australia_hunt`. When the day would exceed the cap, shed by
`australia_hunt.degrade_order` and record what you shed in the run log. Half a run that
finishes beats a full one that gets cut off.

## The rule that outranks the rest

Never fabricate a number. Every company-specific figure carries a source URL or is marked
`unavailable`/`null`. A missing anchor correctly lowers confidence downstream; an
invented one corrupts everything after it.

This is research, not investment advice. Keep the disclaimer from `config/pipeline.yaml`
on the note.
