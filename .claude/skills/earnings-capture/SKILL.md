---
name: earnings-capture
description: Track B forward capture. Sweeps the run-in to upcoming earnings prints and stores the pre-event record — agent-run WebSearch across the nine research areas, plus filings, retail chatter and price bars — while the outcome still does not exist. Use when asked to run the capture sweep, build the forward corpus, capture upcoming earnings, or grow the backtest training database.
---

# Forward capture — building the corpus before the answer exists

Every fence in `backtest/scripts/corpus_news.py` — the Wayback tiering, htmldate, the
tells regex, the safety margin — exists because retrospective capture cannot prove when
bytes existed. This stage makes that proof free. You fetch today, the print is days
away, and the timestamp is yours rather than a vendor's claim.

Three things follow, and they are the whole reason this stage is cheap:

- **You are the discovery layer, the script is the executor.** The corpus has to be the
  corpus production would have read, so you run the same nine-area search program
  `earnings-deep-researcher` runs. A script with its own source list would build a
  different corpus and test a different thing.
- **Do not fetch pages yourself.** Hand URLs to `capture.py`. It stores content-addressed,
  stamps the fetch instant, deduplicates against every prior day, and keeps a changed
  article next to its earlier version — which is the narrative moving into the print, and
  the most valuable thing here.
- **Never resolve the session.** Nasdaq leaves `time-not-supplied` on most future rows.
  You do not need it. `seal.py` sets the fence after the print from the EDGAR 8-K
  acceptance time, which `backtest/FINDINGS.md` §3 established as exact.

## 0. Two script directories, and they are not the same one

This trips every fresh session, so read it once here rather than working it out:

- `scripts/` at the **repo root** — `run_log.py`, `publish.sh`, `run_paths.py`. Shared
  with the daily pipeline. Run these from the repo root.
- `backtest/scripts/` — `capture.py`, `rehydrate.py`, and the rest of the backtest.
  Run these from `backtest/`.

`run_log.py` writes into `research/<Y>/<M>/<date>/_run-log.md` like every other stage, so
the capture leaves its trace where you would look for it.

## 1. Resolve the working set

```bash
cd backtest && python3 scripts/capture.py --from-date <YYYY-MM-DD> --horizon-days 15 --universe-only
```

Writes `captures/universe.json`, merging new events into what is already tracked.
Re-running never loses a name. Every scheduled US name is taken by default — there is no
cap floor, because a thin corpus for a small name is a real observation about that name,
not a gap.

If the sweep is large, capture in cap order and say in the run log where you stopped. A
partial day recorded honestly is worth more than a full day that dies halfway.

## 2. Search, as the researcher searches

For each name, work the nine areas from `.claude/agents/earnings-deep-researcher.md`
§"What to research". Run independent searches in parallel.

Two deliberate departures from the live stage:

- **Over-search.** Issue more queries than a dossier needs, including angles you doubt
  will pay. Capture is one-shot — a query you skip today can never be run against this
  day again — and breadth now is what keeps replay honest later.
- **Do not analyse.** No dossier, no view, no ranking. Judging the setup is what the
  backtest arms are for, and a stored opinion of yours would contaminate them.

Skip areas 2 and 8 where the script already covers them: price, run-up and volume come
from `quote.json`, Form 4s and 8-Ks from the EDGAR layer.

## 3. Write the capture plan

One file per ticker, in the scratch directory, not the repo:

```json
{
  "ticker": "SAIC",
  "company": "Science Applications International",
  "event_date": "2026-08-31",
  "searches": [
    {"area": 3, "query": "SAIC fiscal Q2 2027 consensus EPS estimate",
     "results": [{"title": "...", "url": "https://...", "snippet": "..."}]}
  ],
  "fetch": [
    {"url": "https://...", "area": 3, "title": "...", "query": "SAIC fiscal Q2 2027 consensus EPS estimate",
     "why": "carries the consensus figure and the revision trend"}
  ]
}
```

`searches` records every query and its full result list, including results you chose not
to fetch. That mapping is the frozen search index a backtest arm searches against at
replay, and the share of an arm's queries that miss it is the honest measure of how wide
this capture was. Dropping the misses would make that number flattering and meaningless.

`fetch` is the subset worth a body. Keep it under about 40 per name per day.

## 4. Capture

```bash
cd backtest && python3 scripts/capture.py --from-date <YYYY-MM-DD> --to-date <YYYY-MM-DD> --tickers <TICKER> --plan <scratch>/plan-<TICKER>.json
```

Per name the script adds: the planned URLs, new EDGAR filings since the last sweep,
the StockTwits delta, and a refreshed 63-day price bar series.

**Check `tripwires` in the snapshot it prints.** Post-earnings language in a body
captured before a print is impossible unless something upstream is wrong — a stale
calendar row, a wrong event date, a company that already pre-announced. It is a bug
report, not a document to discard. Investigate before continuing, and record what you
found.

Capture each name as you finish it. Do not batch to the end of the run: this stage is one
pass over a day that never comes back.

## 5. Run log

From the repo root, not from `backtest/`:

```bash
python3 scripts/run_log.py --heading "Capture — <YYYY-MM-DD> — DONE" --line "<n> events swept, <q> queries, <d> documents, <t> tripwires"
```

Leave the `— STARTED` heartbeat before the first search, as every stage does. A capture
session killed on its first name and a capture that never fired need completely
different fixes, and without a heartbeat they look identical.

## 6. Publish

Also from the repo root. It stages `backtest/captures` and pushes to `main`:

```bash
scripts/publish.sh "capture: <YYYY-MM-DD>, <n> events, <d> documents"
```

The session is ephemeral. Anything not pushed is gone, and unlike the research stages
this work cannot be redone tomorrow — the day will have moved.

## 7. Report

The window, events swept, queries issued, documents stored and how many were new, any
tripwires, and any name you skipped with the reason. If a name came back with almost
nothing, say so plainly. That is a finding about coverage, not a failure of the run.
