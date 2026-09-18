# Backtesting the preliminary research read

A research project sitting beside the daily pipeline, not inside it. Nothing here writes
to `research/`, `LEDGER.md` or `PREDICTIONS.*`, and no Routine fires it.

**The question.** Does the stage-2 preliminary read carry information about the direction
of a post-earnings move, and — more usefully — *which kinds of moves can be seen ahead of
time from the public record and which cannot*.

Read `FINDINGS.md` first. Everything below follows from probes that were actually run,
and the second round of them overturned the first round's central conclusion.

## The shape of the problem

A backtest of this skill lives or dies on one property: the research agent must see the
world as it stood before the print, and nothing after it. Three things have to be true at
once.

1. **The content is as of a date we choose** — not merely published before it. An
   earnings preview updated the morning after is still "published" beforehand.
2. **The selection is not hindsight.** A search engine queried today ranks by what turned
   out to matter. Filtering that list by date does not undo the ranking.
3. **The fence is verifiable after the fact**, by something other than the agent's word.

Search-and-filter fails all three (`FINDINGS.md` §6). Reading a web archive that stores
bodies satisfies all three (§7, §12).

## The corpus, in three tiers of provenance

Every document carries the tier it came from, and results are reported by tier. A tier is
a claim about how strongly the fence holds, and the weakest tier in a dossier bounds what
the dossier can be used to conclude.

**Tier 1 — proof. Common Crawl WARC records.** The stored bytes with a `WARC-Date` earlier
than the cutoff. Unforgeable, publisher-independent, and unaffected by later edits. Two
sources with complementary weaknesses:

- *CC-MAIN* (monthly). Cheap and targeted: a CDX index and a Parquet columnar index mean
  you fetch only the records you want. It is a **back-catalogue**, though, not a news
  feed — it re-crawls old pages and samples a publisher's recent output thinly (§13:
  4 transcripts and 64 articles from all of August 2026 on fool.com). Valuable for
  history and old call transcripts. Not the run-in.
- *CC-NEWS* (continuous). Covers every day, 454 WARCs for August. No index at all, so it
  must be swept — and the sweep is shared across the entire universe. Since §13 this is
  **the** news layer rather than a supplement, which makes the sweep load-bearing.

**Tier 2 — strong. Wayback snapshots with a timestamp before the cutoff.** Same property
as Tier 1, far sparser for financial pages in a narrow window (§6). Use where it happens
to have a capture; never plan around it. Always bound the timestamp explicitly — the
availability API returns the *closest* snapshot in either direction and will hand back
post-event content if asked carelessly.

**Tier 3 — probabilistic. A live fetch of a page whose publication date precedes the
cutoff**, established with `htmldate` and corroborated by a scan of the body for
post-cutoff content. Admits the updated-article failure mode by construction. Permitted
only when a name would otherwise have no news at all, always flagged, and its share of
each dossier is reported.

**Filings and market anchors** sit alongside all three and are clean by construction
(§1, §3, §5): SEC filings are immutable and date-stamped, price bars are price bars.

## The informal layer

Filings and wire copy are the cheap half of this corpus and the least interesting half.
Consensus EPS and guidance language are on every terminal on the street; an AI researcher
that reads them well has matched the baseline, not beaten it. The forecasting value is
supposed to come from aggregating the informal record at a scale no analyst reads — retail
positioning and its turn, developer and customer sentiment, product complaints, hiring,
chatter volume into the print.

That layer earns its own tier logic, and it is simpler: every item carries a publisher
timestamp, so the fence needs no body inference at all. No htmldate, no tells scan, no
updated-article failure mode. `scripts/corpus_social.py` implements it (§21):

- **StockTwits** — the backbone. Cashtag-indexed, exact ISO timestamp per message, pages
  backward with `&max=<id>`. ~75 requests covers a 14-day window, ~2 minutes a ticker,
  rate-limited to 2-3 tickers an hour unauthenticated.
- **Hacker News** via Algolia — hard epoch filter, full comment text, and thin: one OKTA
  hit in fourteen days. Real for developer-tools and infrastructure names, empty for most
  of the universe. Must run `typoTolerance=false` or it matches "Okay" for "Okta".
- **Reddit — the open gap.** PullPush 429s on nearly every request. Arctic Shift is the
  next thing to try and it matters more than the rest of the table for consumer names.

Message volume per day is written alongside the text rather than collapsed, because the
shape of chatter into a print is itself one of the few informal signals that is cleanly
quantifiable.

## Route chosen: ticker-indexed discovery, archive-first content

The CC-NEWS sweep below remains the most rigorous option and the most expensive. The
route now being built is cheaper and nearly as strong, because the two hard parts turn
out to be separable (§14–§18):

- **Discovery** by ticker-tagged news API with a date range — Finnhub or Alpha Vantage,
  both free — so there is no text matching at all. Firecrawl `tbs=cdr` backfills thin
  names, entering with no trusted timestamp (§15).
- **Content** from a Wayback snapshot before the cutoff wherever one exists, which makes
  the document tier 2. Live fetch only as fallback, marked tier 3 and counted (§18).
- **Verification** on every document independently of discovery: provider timestamp,
  htmldate, and a body scan for post-cutoff tells. Demonstrated catching a real
  post-earnings recap while passing a real preview (§17).

`scripts/corpus_news.py` implements this. Every run reports its **tier-3 share**, which is
the number that bounds what the run can be used to conclude.

## The sweep, if the cheap route proves too thin

The single insight that makes this affordable: **CC-NEWS is swept once for a date window,
not once per event.** All 1,667 August events share the same three weeks of news. One
pass reads the window, matches every record against the full ticker list, and writes each
match into per-ticker directories.

Sizing, measured rather than assumed: ~41,000 records per 1.07GB WARC, 19 WARCs per day,
so roughly 20GB and 780,000 records a day, ~485GB for a full month. Records must be
streamed to be read — there is no index to skip with — so bandwidth is the binding cost
and it is fixed.

Two ways to pay it. Stream it from here, which is hours rather than minutes but needs no
account and no setup. Or run the sweep on an EC2 instance in `us-east-1`, where
`data.commoncrawl.org` is S3-local and the transfer is fast and free; the output is a few
GB of matched articles rather than half a terabyte. Prefer the second if a month of
history is wanted; the first is fine to prove the sweep on a few days.

Matching is deliberately dumb: company name or `$TICKER` in the extracted text, no model
in the loop, no scoring, no top-N. Everything that matches and predates the fence is
kept. Dumb is the point — it is what makes §12 hold.

## Two tracks

**Track A — retrospective.** The month already on disk. Filings and anchors from the
first round; news from the CC sweep. Addressable now, no waiting.

**Track B — prospective.** A nightly harvest over the full qualified universe, capturing
the pre-print web while the outcome does not yet exist. Its advantages over Track A are
narrow but real: it can capture the option-implied move, and it catches sources Common
Crawl never visits. It is no longer the only way to get text, which is what §7 changed —
so it is now a refinement rather than the main event. Still worth switching on early,
since its value is a function of when it starts.

## Arms

Every arm receives the **same harness-computed anchor block**, so what varies is the
research and not who managed to find a price.

| Arm | Corpus | Tools | Purpose |
| --- | --- | --- | --- |
| **A1 — filings only** | filings + anchors | `Read`, `Grep`, `Glob` | what the primary record alone supports |
| **A2 — + formal news** | A1 + tier 1/2 news | same | the conventional read |
| **A3 — + informal** | A2 + StockTwits/HN/Reddit | same | the hypothesis worth testing |
| **C — open** | live web, unrestricted | `WebSearch`, `WebFetch` | contaminated ceiling, never a result |
| **floor** | anchors only, no model | — | always-Neutral; coin flip; sign-of-drift |

The arms are nested deliberately, so each step isolates one layer's contribution.

A1→A2 measures what wire copy and analyst commentary are worth on top of the primary
record. A2→A3 is **the question this project exists to answer**: does the informal record
carry signal the formal record does not? If A3 beats A2, the live pipeline is currently
spending its budget on the wrong half of the input, because stage 2 reads formal sources
almost exclusively. If A3 does not beat A2, that is worth knowing before building more
scraping.

A3 against C bounds leakage: if they score alike, A3 leaked. Every rate is read between
the floor and C, never alone. `LEDGER.md`'s n=3 problem is what happens when a number is
reported without either bound.

Enforcement is the tool allowlist on a dedicated agent definition, never an instruction in
a prompt. The pipeline already relies on this — the persona agents have no file-reading
tools precisely so independence is not left to good intentions.

## Blinding

The sealed reader runs in a scrubbed worktree with `research/`, `LEDGER.md`,
`PREDICTIONS.*` and `INDEX.md` absent. `PREDICTIONS.csv` has an `actual_move` column and
`earnings-deep-researcher` currently holds `Bash`, `Read`, `Glob` and `Grep` — in this
checkout it can simply grep the answer.

## Anchors

`scripts/anchors.py`, from bars strictly before the print and from EDGAR filing dates:
spot, distance from 52-week high and low, 20-day realised vol, 5- and 20-day run-up,
average volume, and the last eight earnings reactions with their dates.

One deliberate gap: the **option-implied move is not recoverable retrospectively** and is
marked `unavailable`. In its place the block carries `expected_move_proxy_pct` — the
median absolute move over the last eight prints — explicitly labelled a proxy. For OKTA
that proxy is ±8.24% against a realised +28.63%, on a name whose recent reactions include
+30%, +24% and −16%; the proxy is a weak centre for exactly the names that matter most.
This is the one place where the backtested skill is not the live skill. Only Track B
closes it, and only for events after it starts.

## Sampling

Enumerate the complete universe first, then draw from it — never sample and then
enumerate.

1. `scripts/events.py` over the target window at a $2B cap floor.
2. Drop: unresolved session, `intraday` prints, foreign private issuers, dual-class
   duplicates, corporate action inside the measurement window, fewer than 60 pre-cutoff
   bars, fewer than 4 prior earnings reactions.
3. Stratify on session, cap band and sector; draw with a fixed seed.
4. **Commit the draw before running anything**, with seed, window and filters, so the
   sample cannot drift toward names that turned out to be interesting.

On size, honestly: estimating one hit rate to ±10pp needs about n=100; separating 60% from
50% at 80% power needs roughly n=400. Under n≈30 the result is a debugging exercise and a
source of failure cases, not a measurement — a legitimate first milestone as long as it is
called that.

The budget knob is model tier, not ticker supply. n≈120 sealed reads on a mid tier and
n≈30 on Opus cost about the same; running both on the same events measures the tier effect
for free.

## Scoring

`scripts/truth.py` for the realised move, then per event: direction hit, signed and
absolute magnitude error, band hit, whether the proxy expected move was broken. Same
conventions and the same five call labels as the live ledger, so results are comparable to
`LEDGER.md` rather than a parallel dialect.

## Leak audit — reported, not assumed

Runs after every dossier, on every arm including the sealed ones:

- re-verify the fence on every corpus document from its recorded `WARC-Date` or filing date
- resolve the publication date of every cited URL; flag anything at or after the cutoff
- scan dossier prose for outcome tells — reported figures, "shares rose/fell", post-cutoff dates
- an auditor pass that *is* given the outcome and asked one question: does this dossier
  contain anything unknowable before the cutoff

A flagged dossier is **void, not corrected**. Void rate and Tier-3 share are published next
to the hit rate. A backtest that does not report its own contamination rate is not evidence.

## The output that is actually wanted

The headline hit rate is close to a byproduct. Three artefacts carry the value:

**Knowability cross-tab.** A labeller reading only the pre-cutoff corpus, blind to every
dossier, marks each event *ex-ante knowable* or *not knowable*. Hit rate crossed with that
label is the direct answer to what an AI can and cannot see.

**Failure taxonomy.** Every miss classified: missing anchor, misread bar, guidance
surprise, macro shock, sentiment misread, correct read and the market disagreed.

**A1 versus A2.** What the news layer is actually worth, in hit rate and in calibration.
If it is worth little, the live pipeline is spending most of its budget on the wrong half
of the input.

## Layout

```
backtest/
  PLAN.md  FINDINGS.md  README.md
  scripts/  common.py  truth.py  events.py  anchors.py  corpus_edgar.py
            cc_sweep.py  cc_fetch.py  corpus_news.py  audit.py  score.py  draw.py
  corpus/news/<TICKER>/<warc-date>_<host>_<hash>.txt      shared across all events
  runs/<run-id>/manifest.json          seed, window, filters, the committed draw
  events/<TICKER>-<YYYY-MM-DD>/
    anchors.json  filings/  filings_manifest.json  news/  news_manifest.json
    arm-a1/dossier.md|.json  arm-a2/…  arm-c/…
    truth.json  audit.json
  RESULTS.md
```

## Build order

1. ~~`truth.py` — validated against all eight scored outcomes~~ **done**
2. ~~`events.py` — exact session from EDGAR 8-K item 2.02 acceptance time~~ **done**
3. ~~`anchors.py`~~ **done**
4. ~~`corpus_edgar.py` — exhibits followed, silent failures surfaced~~ **done**
5. ~~`cc_fetch.py`~~ **done** — history and old transcripts, tier 1. Not the run-in (§13).
5b. ~~`corpus_news.py`~~ **done** — finnhub live, clock bug found and fixed (§19),
   archive-status conflation fixed (§20).
5c. ~~`corpus_social.py`~~ **built** — StockTwits + HN, timestamp-fenced (§21).
   Reddit still open.
6. Measure the tier-2 share and articles-per-ticker on a 10-name draw. Only if that comes
   back thin does `cc_sweep.py` over CC-NEWS become worth its bandwidth.
7. `draw.py` — enumerate, filter, stratify, commit the manifest
8. `earnings-deep-researcher-sealed` — `Read`/`Grep`/`Glob` only
9. One event end to end, dossier read by hand before anything scales
10. `audit.py`, `score.py`, pilot at n≈30
11. Track B nightly harvest

Step 6 is the one with real cost attached and the one to decide deliberately: three days
of sweep is a few tens of GB and answers whether the match rate per ticker is high enough
to bother with the month.

## What this cannot answer

The implied move is a proxy, so anything the live skill derives from real option pricing is
absent. Sources Common Crawl never visits are absent, and paywalled analyst research is
absent for everyone. A Track A result is a **lower bound** on the live skill rather than a
measurement of it — narrower than the first round's version of that caveat, but still true.
