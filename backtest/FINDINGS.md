# Feasibility probes — 2026-08-28

Everything below was run, not reasoned about. Each finding names the endpoint so it can
be re-checked when it breaks.

## 1. Ground truth is deterministic and exact

Yahoo's chart API (`query1.finance.yahoo.com/v8/finance/chart/<T>`, no key) serves daily
bars. Applying the ledger's own convention — close before the print, close after the
first full session following it — reproduces **all eight scored outcomes in
`PREDICTIONS.csv` to the cent**:

| | STDN | OKTA | NTNX | DLTR | WOLF | HOV | BILL | BABA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| computed | 4.45 | 28.63 | 6.81 | −3.92 | −9.42 | −7.47 | −0.65 | 1.26 |
| ledger | 4.45 | 28.63 | 6.81 | −3.92 | −9.42 | −7.47 | −0.65 | 1.26 |

Scoring never needs an agent again. `scripts/truth.py` also reports the
split/dividend-adjusted move alongside the raw one; a gap above 0.5pp means a corporate
action inside the window and the event is dropped from the sample.

## 2. The historical calendar contains the answer

`api.nasdaq.com/api/calendar/earnings?date=<past date>` returns, for every row, the
**reported** `eps` and the `surprise` percentage. The universe source is itself a leak.
`epsForecast` and `noOfEsts` are legitimate pre-event consensus and are kept; `eps` and
`surprise` are dropped at ingestion and never written to disk.

`marketCap` on that endpoint is *today's* cap, not the cap as of the event — a stock
that halved shows a smaller number. It is used for the liquidity floor only and is
never exposed to a research agent.

## 3. Nasdaq drops the session for past dates; EDGAR restores it exactly

Past-date rows all carry `time: "time-not-supplied"`, which is why
`scripts/get_earnings.py --date 2026-08-05` returns 475 raw rows and zero qualified ones.

The fix is better than the thing it replaces. The earnings 8-K carries item **2.02**
and an `acceptanceDateTime` in the submissions API, and that timestamp converted to ET
settles the session with no guessing and without looking at price action:

```
OKTA  2026-08-26T16:03:06 ET  -> amc     INTU  2026-08-25T16:02:29 ET -> amc
DKS   2026-08-25T07:01:39 ET  -> bmo     MRVL  2026-08-27T16:05:59 ET -> amc
```

Rule: `>= 16:00 ET` → amc, `<= 09:30 ET` → bmo, anything between → `intraday`, excluded.

Over 2026-08-24…27 the resolver settled 18 of 26 candidates. The eight failures are all
one of two known classes: foreign private issuers file 6-K rather than 8-K (PDD, XPEV,
BMO, BNS, RY) and dual-class tickers share a CIK (HEI.A). Both are mechanical — extend
to 6-K, dedupe by CIK — or exclude the class and say so.

## 4. Universe supply is not the constraint

Earnings events at or above a $2B cap floor, 2026-07-27 → 2026-08-27: **1,667**. Peak
season runs 200+ a day (2026-08-05: 251). Sampling is a budget question, never an
availability one.

## 5. EDGAR is a provably clean corpus layer

Filings are immutable and SEC-timestamped, so `filingDate < cutoff` cannot admit
post-event content. There is no revision to worry about and no ranking to bias. For
OKTA at a 2026-08-26 cutoff, a 400-day lookback yields **41 documents, 660KB**: the
prior-quarter 10-Q, the prior-quarter earnings 8-K with the guidance the coming print
will be judged against, the proxy, 20+ Form 4 insider transactions and several 13G/A
ownership changes.

Two things this probe caught that a design on paper would not have:

- **8-K item 2.02 keeps the numbers in EX-99.1, not the primary document.** The cover
  page is 4.7KB of boilerplate; the release is 244KB. Without following exhibits the
  corpus contains the filing but not the bar.
- **A swallowed exhibit-index failure is indistinguishable from "no exhibits".** One
  transient SEC timeout silently dropped the single most important document and the run
  still reported success. Exhibit errors are now recorded in the manifest and the run
  warns.

## 6. The retrospective news layer is not salvageable

Two independent probes, both negative.

**Wayback.** The CDX API works (`web.archive.org/cdx/search/cdx`) and honours `from`/`to`.
It returns genuinely empty for `finance.yahoo.com/quote/OKTA` across 2026-08-01…25 — the
nearest capture is 2026-08-27, *after* the print. The availability API returns the
closest snapshot in either direction, so it will happily hand back post-event content
unless the timestamp is checked explicitly. Coverage of financial pages in a specific
pre-earnings window is too sparse to build a corpus from.

**Search.** `WebSearch` exposes no date parameter — only `allowed_domains` /
`blocked_domains` — and a `before:2026-08-26` operator in the query string is ignored.
Searching the OKTA event as a harvester would returns, in the **link list itself**:

- *"OKTA Q2 Earnings Beat on Subscription Growth, FY27 View Raised"* (title)
- `qz.com/okta-stock-surged-after-the-identity-security-company-beat-earnings-expectations` (URL slug)

The outcome leaks in titles and URLs, not merely in snippets. A discovery step that
passes nothing but URLs to the sealed reader is *still* contaminated.

This is the finding that decides the architecture: for past events, a research agent
with any web tool is contaminated by construction, and the news layer cannot be
reconstructed retrospectively at all. It has to be captured forward, before the outcome
exists.

---

# Second round — 2026-08-28, after "the text is essential"

§6 concluded the news layer was unrecoverable. That conclusion was **wrong**, and wrong
because it tested the two worst sources. Searching for URLs and pulling them from
Wayback is the fragile path. Reading an archive that already stores the bodies is not.

## 7. Common Crawl serves full article text with an unforgeable capture time

`index.commoncrawl.org/CC-MAIN-2026-34-index` → capture record → HTTP `Range` request
against the WARC on `data.commoncrawl.org` → one gzip member → the complete stored page.

Probed end to end: 109KB range-fetched out of a ~1GB WARC, yielding **60,115 characters**
of article text and this header:

```
WARC-Date: 2026-08-09T10:51:50Z
WARC-Target-URI: https://www.fool.com/earnings/call-transcripts/...
```

The `WARC-Date` is the fence, and it is the right kind of fence: it records when those
exact bytes provably existed. It cannot be edited by the publisher, cannot drift when an
article is updated, and does not depend on any date the page claims about itself.

## 8. The monthly crawl is a two-week window, not a month

Capture spans sampled from CC-MAIN-2026-34 ("August 2026 Index"):

| host | captures | span |
| --- | --- | --- |
| fool.com | 300 | 2026-08-07 … 2026-08-20 |
| benzinga.com | 107 | 2026-08-07 … 2026-08-19 |
| seekingalpha.com | 127 | 2026-08-07 … 2026-08-19 |
| investing.com | 16 | 2026-08-07 … 2026-08-19 |

For a print on 2026-08-26 the freshest main-crawl content is six days stale. The main
crawl gives the persistent background; it does not give the last-week flow, which is the
most decision-relevant window there is.

## 9. CC-NEWS closes the recency gap, and has no index

The continuous news crawl covers **every single day**: 454 WARC files for 2026-08-01…28,
353 for July. Sampled by streaming 12MB of one file and walking the gzip members with
`zlib.decompressobj(wbits=31)`:

- 462 records parsed from 12MB → roughly **41,000 records per 1.07GB file**
- 19 files stamped 2026-08-25 → about **20GB and ~780,000 news records per day**
- `WARC-Date` span inside that 12MB slice: 95 seconds
- 43 distinct hosts in the slice; finance and newswire share around 4% (PR Newswire present)

And the constraint: **CC-NEWS ships no index.** Both
`index.commoncrawl.org/CC-NEWS-2026-08-index` and `CC-NEWS/2026/08/cc-index.paths.gz`
return 404. CC-MAIN has a 103MB CDX cluster index *and* a Parquet columnar index queryable
by host; CC-NEWS has neither. It has to be swept.

The sweep is not per-event, which changes the economics completely. One pass over a date
window extracts articles for **every ticker in the universe at once** — 1,667 August
events share the same three weeks of news. That is the "build the universe beforehand"
step, done exactly once.

## 10. The extraction stack installs locally — no plugin required

`pip install htmldate trafilatura` succeeds (htmldate 1.10.0). Validated against real
CC records:

```
url       : fool.com/investing/2016/05/31/intel-corporation-has-a-new-key-ingredient...
WARC-Date : 2026-08-12T02:28:21Z    <- capture time, the fence
htmldate  : 2016-05-31              <- claimed publication date, corroboration only
text      : 3,930 chars via trafilatura
```

The two dates answer different questions and must not be conflated. `WARC-Date` is when
the bytes existed. `htmldate` is when the page says it was published — useful for
ordering and for catching a page that back-dates itself, never sufficient on its own.
htmldate's own documentation notes it measures the publication date and not the modified
date, which is precisely the failure mode that matters for an updated earnings preview.

## 11. Commercial APIs solve discovery, not point-in-time content

Exa supports `startPublishedDate` / `endPublishedDate` in ISO 8601, plus `startCrawlDate`
/ `endCrawlDate`, which is a genuinely good discovery filter. But its `contents` endpoint
serves **the most recent crawl** — `maxAgeHours: -1` means "always cache", not "cache as
of a date I choose". A preview article updated after the print returns updated. Same
shape for every commercial news API: the date filter applies to the article's metadata,
the body is whatever was last fetched.

Useful as a discovery aid or a third-tier fallback. Not a substitute for a WARC.

## 12. An exhaustive sweep has no hindsight selection at all

This is the part that matters most and is easy to miss. §6's leak was not only that
snippets carry outcomes — it was that *search ranking is hindsight*. Today's engine
surfaces the articles that turned out to matter.

Sweeping an archive removes that problem rather than mitigating it. There is no query, no
ranking and no top-N. Every record captured before the fence that mentions the company is
taken, in whatever proportion it actually existed. The selection bias that made the
search-plus-filter design unfixable simply does not arise.

## 13. The monthly crawl is a back-catalogue, not a news feed

`cc_fetch.py` was built and run against the real OKTA event (cutoff
`2026-08-26T20:03:06Z`, four hosts, two index pages each). It kept **18 of 18 candidate
documents**, every one captured between 2026-08-09 and 2026-08-19 — the fence held
cleanly, no rejections, no index errors.

But look at what came back:

| claimed published | captured | chars | what it is |
| --- | --- | --- | --- |
| 2018-09-06 | 2026-08-14 | 49,107 | Q2 FY19 earnings call transcript |
| 2019-08-28 | 2026-08-15 | 59,238 | Q2 FY20 earnings call transcript |
| 2021-11-28 | 2026-08-09 | 2,978 | an earnings preview from five years ago |
| … 14 more, all 2018–2025 | | | |
| 2026-08-14 | 2026-08-17 | 3,809 | the quote page — the only recent document |

CC-MAIN re-crawls the archive. URL-slug discovery therefore surfaces a publisher's
**back-catalogue**, not its current output. Two direct counts confirm it: the entire
August index holds **4** fool.com call transcripts from all of 2026, and **64** fool.com
articles published in August 2026. That is a thin sample of one publisher's month, not
coverage of it.

So CC-MAIN earns its place for history — old transcripts and prior-cycle commentary are
genuinely useful to a base-rate read, and they are Tier 1 clean — but it does not supply
the run-in to a print. **CC-NEWS is the news layer, not a supplement to it**, which makes
the sweep the load-bearing step of the whole design rather than an optimisation.

---

# Third round — the API route

## 14. Ticker matching is a solved problem, and not by crawling

The objection to the sweep was matching raw text to tickers. The answer is not a better
matcher — it is to stop matching. News APIs tag articles with the ticker at ingestion, so
discovery becomes one ranged query per event:

| provider | endpoint | fence | history | key |
| --- | --- | --- | --- | --- |
| Finnhub | `/company-news?symbol=&from=&to=` | exact unix ts | ~1 year | free |
| Alpha Vantage | `NEWS_SENTIMENT&tickers=&time_from=&time_to=` | `YYYYMMDDTHHMM` | ~2022→ | free |
| Firecrawl | `/v2/search` + `tbs=cdr:1,cd_min:…,cd_max:…` | Google crawl date | broad | paid |

Yahoo's keyless `v1/finance/search?q=<TICKER>` also returns ticker-tagged news with exact
UTC timestamps — but only the latest ten, with no range parameter. A complete free nightly
layer for Track B; useless retrospectively.

## 15. Firecrawl's date filter is real, and is the weakest of the three

`tbs` is supported and does accept `cdr:1,cd_min:MM/DD/YYYY,cd_max:MM/DD/YYYY`. Two
caveats that keep it as backfill rather than the primary:

- Google's `cdr` filters on **its own crawl date**, not the article's publication date.
- Third-party pass-through of `tbs` is imprecise — reported accuracy 62–78% against 99.4%
  for native Google. Firecrawl is a third party here.

So Firecrawl results enter with `published_utc: null` and have to earn their place from
htmldate and the body scan alone. Useful for names the ticker-tagged providers cover
thinly; never trusted on its own.

## 16. X is out for retrospective, viable for prospective

Full-archive search moved to Enterprise-only at **$42,000+/month** (the $5,000 Pro tier
that used to carry it is closed to new signups). Pay-per-use since February 2026 at
~$0.005 per post read, with the free tier closed to new developers.

Reaching back to an August print therefore costs enterprise money. But the 7-day recent
search is cheap and perfectly adequate for a **nightly** capture, so X belongs to Track B
and nowhere else.

## 17. The verification stack catches a real leak — demonstrated

Run against a genuine pre/post pair for the OKTA event (cutoff `2026-08-26T20:03:06Z`):

| | pre-earnings preview | post-earnings recap |
| --- | --- | --- |
| Wayback snapshot before cutoff | **20260824164903** | none |
| htmldate | 2026-08-24 | 2026-08-26 |
| extracted text | 3,172 chars | 2,671 chars |
| post-cutoff tells in body | none | `shares (rose\|fell\|surged\|…)` |
| verdict | **accept, tier 2** | **reject** |

Three independent checks, and the recap fails two of them.

## 18. Wayback is far better on articles than on quote pages

§6 concluded Wayback coverage was too sparse to plan around. That was measured on a
**quote page**, which archives rarely. The article probe above found a snapshot from two
days before the print on the first URL tried.

The consequence is worth more than it looks: a document with a pre-cutoff Wayback snapshot
is served from the snapshot, so it is **tier 2 — archived bytes — not tier 3**. Discovery
through a ticker-tagged API and content through Wayback gets much of the corpus to tier 2
without a WARC sweep at all. One sample is not a coverage rate; measuring the tier-2 share
across a real draw is the first thing the pilot should report.

## 19. Finnhub timestamps are Eastern wall-clock, not UTC

Finnhub's `company-news` returns `datetime` as a unix timestamp. Read as UTC, it places
articles **four hours earlier than they were published**. Measured against EDGAR 8-K
acceptance times, which are authoritative:

| ticker | 8-K accepted | finnhub ts on the results headline | offset |
| --- | --- | --- | --- |
| OKTA | 2026-08-26T20:03:06Z | 2026-08-26T16:02:00Z | −4.02h |
| BILL | 2026-08-19T20:02:15Z | 2026-08-19T16:01:53Z | −4.01h |
| WOLF | 2026-08-19T20:40:15Z | 2026-08-19T16:21:03Z | −4.32h |

Three events, three times −4h: EDT wall-clock stored as if it were UTC. (WOLF's extra 19
minutes is ordinary reporting lag, not clock drift.)

Uncontrolled, this puts **the entire post-release news flood on the safe side of the
fence** for every AMC print — "Q2 Adj. EPS $1.05 Beats $0.97 Estimate", "Okta Stock
Rallies After Q2 Earnings Beat Estimates", the full call transcript. A backtest built on
it would have been measuring the skill's ability to read a results wire.

Fixed by reinterpreting the wall-clock as `America/New_York`. After the fix everything
from 20:03:06Z onward is blocked. One item still passes at 20:02:00Z — the earnings press
release itself, which crossed the wire a minute before EDGAR accepted the 8-K. That is
the true event boundary, and it is why the fence carries a **safety margin** (default one
hour) rather than sitting exactly on the filing timestamp.

Two lessons that generalise past Finnhub. A vendor timestamp is a claim, not a clock. And
the only reason this was catchable is that EDGAR acceptance times gave an independent
clock to check it against — every provider added later must be calibrated the same way
before it is trusted.

## 20. "No snapshot" and "the archive refused" are not the same thing

The first full run reported **0 tier-2 and 12 tier-3 — a 100% tier-3 share** — for a
ticker where a pre-cutoff snapshot had already been confirmed by hand. The cause was in
`wayback_before`, which returned `None` both when no snapshot existed and when
archive.org failed the query, and archive.org fails often.

The effect ran in the dangerous direction: it silently degraded documents to tier 3 and
inflated the exact number this project publishes as its honesty check. A pessimistic bias
is still a bias, and one that would have been reported as a measurement.

Now returns an explicit status — `ok`, `no_snapshot`, `no_snapshot_before_cutoff`, or
`lookup_failed(<error>)` — with retries and backoff. Failed lookups are counted, and when
any occur the run states that its tier-3 share is an upper bound rather than a
measurement.

## 21. The informal layer, which is where the edge actually is

Everything above builds a corpus of filings and wire copy. That is the cheapest half to
fence and the least interesting: consensus EPS and guidance language are already in every
terminal on the street. The forecasting value of an AI researcher is supposed to be in
aggregating the informal record — retail positioning, developer and customer sentiment,
product chatter, hiring, complaint volume — which no analyst reads at scale.

A source is only usable here if it carries a hard timestamp. Surveyed:

| source | fence | text | retrospective | verdict |
| --- | --- | --- | --- | --- |
| **StockTwits** | exact ISO per message, cashtag-indexed | full | yes, by cursor paging | **primary** |
| **HN Algolia** | `created_at_i` epoch filter | full | yes | niche |
| Reddit (PullPush) | `created_utc` epoch | full | HTTP 429 throttled | blocked, retry Arctic Shift |
| Google Trends | date-ranged | signal only | yes | untested |
| YouTube Data API | `publishedBefore/After` | transcripts | yes, free quota | untested |
| X / Twitter | — | — | Enterprise $42k/mo | out (§16) |

**StockTwits** is the find. Keyless, cashtag-indexed so no matching problem, exact ISO
timestamps, and it pages backward with `&max=<id>`. Measured: 8 pages of 30 covered
2026-08-28T15:44 back to 2026-08-27T02:23, about 1.5 days — so a 14-day window is roughly
75 pages, about two minutes per ticker. Unauthenticated rate limiting (~200 requests/hour)
caps throughput near 2-3 tickers an hour, which is slow but entirely workable for n=30.

**HN Algolia** has a hard epoch fence and full comment text, but is thin: exactly **one**
OKTA hit in the 14 days before the print, with typo tolerance disabled. (Left on, Algolia
matches "Okay" for "Okta" and returns 1,453 hits of noise — a trap worth naming.) Keep it
for developer-tools and infrastructure names; it will be empty for most of the universe.

**Reddit is the significant gap.** PullPush returns 429 on nearly every request. Arctic
Shift is the next thing to try, and it matters more than the rest of this table combined
for consumer and meme-adjacent names.

## 22. Finnhub returns redirect URLs, which silently forced every document to tier 3

`company-news` does not return publisher URLs. It returns its own redirect
endpoints — `https://finnhub.io/api/news?id=<hash>` — which resolve to the real
article:

```
finnhub.io/api/news?id=30bc9685...  ->  finance.yahoo.com/markets/stocks/articles/okta-okta-stock-above-fair-191102716.html
finnhub.io/api/news?id=e8abdfda...  ->  247wallst.com/investing/2026/08/21/ai-is-now-attacking-at-machine-speed...
finnhub.io/api/news?id=76547bac...  ->  marketbeat.com/articles/marketbeat-week-in-review-08-17-08-21/
```

Used as-is they break the corpus in two places at once, and neither failure
announces itself:

1. **Archive lookups can never hit.** No web archive holds a snapshot of a
   per-request redirect endpoint. Every document was therefore forced to tier 3
   — the 100% tier-3 share in §20 was only *partly* the status-conflation bug.
2. **Fetches fail.** 19 of 24 rejections in that run were `body unavailable`,
   which read like publisher paywalls and was actually the redirect refusing a
   plain request.

Fixed by resolving to the canonical URL before any archive lookup or fetch.
Immediately after the fix, one of the first three resolved URLs came back with a
genuine pre-fence snapshot (`247wallst.com`, captured 20260822144707), so tier 2
is reachable after all.

The pattern worth carrying forward: **three separate bugs (§19, §20, §22) all
biased the corpus in the same direction** — fewer documents, weaker provenance,
and a fence that looked tighter than it was. None of them raised an error. Every
one was found by checking a number against an independent source rather than by
reading the code. Budget for that in the pilot: assume the first run of any new
provider is wrong in a way that flatters it.

## 23. Google-with-a-date-fence: measured, and it fails on both sides

Tested properly across three events (OKTA, BILL, WOLF), four queries each, every
returned URL kept and run through the fence. 91 distinct URLs.

| | N | tier2 | tier3 | leaked | unusable | leak rate |
| --- | --- | --- | --- | --- | --- | --- |
| OKTA | 29 | 4 | 5 | 13 | 7 | 45% |
| BILL | 27 | 2 | 3 | 8 | 14 | 30% |
| WOLF | 35 | 1 | 0 | 10 | 24 | 29% |
| **all** | **91** | **7** | **8** | **31** | **45** | **34%** |

34% of everything Google returns is leaked. But the number that matters is
narrower: of the URLs that produced a **readable body** — the only ones that
could ever reach a research agent — **67% (31/46) is post-cutoff**. Two of every
three documents the route successfully delivers contain the answer. `cnbc.com/
2026/08/26/okta-okta-earnings-q2-2027` comes back on a query phrased entirely as
a preview.

The date fence does nothing at discovery time, and this is structural rather than
fixable: Google ranks by relevance, and for "what to expect from X's earnings"
the most relevant document is always the one written afterwards. `tbs=cdr:`
filters on Google's crawl date (§15), so Firecrawl does not change the ranking —
it would raise the readable-body count, and since leaked documents are the
majority of readable bodies, it would most likely raise the absolute leak count
too.

**Yield fails at the same time.** Raw clean counts overstate badly: 6 of 7
tier-2 survivors pass only because they are *stale* — archived quote-page widgets
from 2021, 2025, months before the event, clean and worthless. Clean documents
actually dated inside the 14-day window: **OKTA 6, BILL 3, WOLF 0.** Zero for
WOLF, which is exactly the small, distressed, thinly-covered name where discovery
help is most needed.

Unusable was 49% (45/91), dominated by blocked fetches (37). Paid scraping fixes
those. It fixes neither leakage nor staleness.

### The false rejections matter more than the false accepts

Hunting for pre-earnings titles hiding post-earnings bodies turned up the opposite
problem:

- *"Okta Gears Up to Report Q2 Earnings: What's in Store for the Stock?"* —
  rejected on `htmldate = 2026-08-28`. The body reads *"is set to release
  second-quarter fiscal 2027 results on Aug. 26"* and *"the to-be-reported
  quarter."* htmldate had read TradingView's page-render date. Fixed in §24.
- *"WOLF: 47% Short Interest, 932% Borrow Fee"*, dated four days pre-cutoff and
  the single best pre-earnings document in WOLF's set — rejected because
  *"expect post-earnings IV crush"* trips `\bpost[- ]earnings\b`. Confirmed
  against the live regex. Forward-looking options language, read as a results
  recap. It is why WOLF's in-window clean count is zero.

And the genuinely dangerous inverse: **stale-looking URLs serving live content.**
`marketbeat.com/instant-alerts/...-nasdaqokta-2025-09-01` returned
`htmldate = 2026-08-26`. Any heuristic trusting a date in the URL admits it.
Live-updating pages have no stable publication date; their content is always now.

**Verdict: not viable as a primary discovery route, and weak as backfill.** The
fix is not to loosen verification — the asymmetry in CLAUDE.md holds, a false
rejection costs one article and a false acceptance corrupts the experiment. The
fix is to stop discovering through a relevance-ranked engine. Ticker-tagged,
natively date-ranged providers return a *time-ordered* list where the fence is a
real filter rather than a post-hoc rescue.

Keep Google as last-resort backfill for names the tagged providers return nothing
on, admitting only tier-2 with an in-window snapshot. And treat a WOLF-shaped
result — zero in-window clean documents — as a reason to drop the name from the
sample rather than to write a dossier on thin sourcing.

## 24. Three fixes that came straight out of §23

- **`fetch()` now detects SEC hosts itself.** 9 of the 37 blocked fetches were
  self-inflicted: a `sec.gov` URL reaching the generic path gets `Mozilla/5.0`,
  the SEC blocks it, and the document is recorded as though it did not exist.
  Host detection beats trusting every call site to pass `sec=True`.
- **Publisher metadata before htmldate.** `article:published_time`,
  `datePublished` and friends are checked first; htmldate is the fallback. The
  source of the date is recorded per document, so render-date failures stay
  visible.
- **Tells quarantine rather than delete, and only at tier 3.** A results phrase
  in a tier-3 body may be leakage. The same phrase in a **tier-2** body cannot
  be — the archive proves those bytes predate the fence — so it is forward-looking
  and the document stands. Quarantined items are counted, which turns the
  false-rejection rate from invisible into measurable.

## 25. First clean corpus, and the hygiene bug that nearly spoiled it

With the clock (§19), archive-status (§20) and redirect (§22) fixes in, the OKTA
harvest went from **0 tier-2 / 12 tier-3** to **7 tier-2 / 7 tier-3** out of 52
candidates. Two archive lookups timed out, so the 50% tier-3 share is correctly
reported as an upper bound rather than a measurement.

The kept documents are the right kind: analyst price-target notes, a Wells Fargo
initiation, a Zscaler-vs-Okta comparison, peer read-through on Palo Alto and
MongoDB, and two dated previews. That is a corpus a research agent can actually
reason from.

Then a count that did not add up. The manifest kept 14 documents; the directory
held **55**. Neither `cc_fetch.py` nor `corpus_news.py` purged before writing, and
both wrote into the same `news/` folder — so output from three runs with three
different fence semantics (an uncorrected clock, unresolved redirect URLs, and the
fixed version) sat side by side, indistinguishable, and a sealed reader would have
read all 55 as current.

This is the most dangerous class of bug in the project so far. It produces no
error, degrades silently, and *reintroduces exactly the leakage the whole design
exists to prevent* — through the back door of stale derived state rather than
through the fence.

Three changes:

- each harvester **purges its own output before writing** — derived state is
  rebuilt, never appended to
- `cc_fetch.py` writes to `news_archive/`, so the two harvesters cannot collide
- the manifest records **`orphan_files`**: anything on disk not accounted for in
  the manifest, which makes the failure loud next time

Also fixed here: the header wrote `SOURCE:` as the Finnhub redirect URL while
`HOST:` showed the resolved publisher — an earlier patch that silently missed its
match. Now both come from the resolved URL, with the provider's redirect recorded
separately as `PROVIDER-URL`.

The running tally is worth stating plainly: **five bugs so far (§19, §20, §22,
§25 ×2), every one silent, every one biasing the corpus toward looking cleaner or
thinner than it was.** None surfaced from reading code. All five surfaced from
checking a number against something independent — EDGAR timestamps, a manual
archive lookup, a file count. That ratio is the argument for the pilot being
instrumented before it is scaled.

## 26. Scaling to 40, and two sampling faults caught before the run

**Wall clock.** Serial harvesting blew a 900s limit twice. A thread pool cut one
ticker from >15 minutes to 2m16s — and pushed failed archive lookups from 2 to
25, because ten workers hit web.archive.org simultaneously. Those failures are
silent and demote documents to tier 3, degrading the very number published as the
quality measure. Concurrency here is a **per-host** question: archive.org now has
its own semaphore (2 slots, 0.8s minimum gap) while fetches stay at 8 workers.

| configuration | tier2/tier3 | archive failures | wall clock |
| --- | --- | --- | --- |
| serial | 7 / 7 | 2 | >15 min (killed) |
| 10 workers, no throttle | 8 / 12 | 25 | 2m16s |
| 8 workers + archive throttle | **11 / 9** | **1** | 7m21s |

**Sampling fault 1: the universe was mega-caps.** `events.py --limit-per-day`
sorts by market cap and takes the top N, so a 12-per-day universe drew 24
large-cap, 14 mid and 2 small out of 40. That is not the population this pipeline
researches — stage 1 shortlists on change expectation, which skews smaller and
more volatile, and small retail-heavy names are where the informal layer is
expected to carry signal. Added `--sample-per-day`, which draws at random with the
seed. The redraw came back **24 small, 12 mid, 4 large**, spanning binary-event
biotechs, a crypto miner, utilities and two mega-caps.

**Sampling fault 2: HN noise on generic company names.** Querying Algolia for
`"Box"` on behalf of Box, Inc. returned 60 items about "out of the box" and "cat
box". Worse than no data, because it looks like coverage. Two guards: a one-word
company name gets no name-query at all, and every item must contain the ticker as
a standalone token or the full multi-word company name. Items dropped this way
are counted in the manifest.

Of the first three events harvested, one (**UCTT**) came back with **zero** news
documents — the WOLF-shaped starvation case from §23, now confirmed as recurring
rather than a WOLF peculiarity. How often it happens across 40 is one of the
numbers this pilot exists to produce.

## 27. The 40-event corpus: coverage tracks market cap, and that is the problem

40 events, 4.7 hours, all five stages on every one. Aggregate:

| | |
| --- | --- |
| filings documents | **1,644** (~41 per event, uniform) |
| news documents | 154 tier-2 + 181 tier-3 (tier-3 share 54%, 17 archive failures) |
| StockTwits messages | 1,738 |
| news starved (0 docs) | **8 events (20%)** — all small-cap |
| news thin (<5 docs) | 9 events (22%) |
| news usable (≥5 docs) | 23 events (57%) |

**Coverage is a near-monotonic function of market cap:**

| band | n | news docs (median) | StockTwits (median) | zero chatter |
| --- | --- | --- | --- | --- |
| small | 24 | **1** | 3 | 8 of 24 |
| mid | 12 | 10 | 15 | 1 of 12 |
| large | 4 | 25 | 46 | 0 of 4 |

This is the finding that shapes the whole experiment, and it runs against us. The
population the live pipeline actually researches is small and mid-cap names with
high change expectation — and that is exactly where the corpus is thinnest. Test
only on well-covered names and the answer describes mega-caps, which stage 1 rarely
shortlists.

The sharpest illustration is **AAP**, whose realised move was **−24.55%**, the
largest in the sample. It has **one** news document. The single most informative
event in the draw is the one we know least about.

**But the filings layer is uniformly rich** — ~41 documents per event with no
relationship to size, because every filer files. That reshapes the arms:

- **A1 (filings + anchors) is viable on all 40 events.**
- A2 and A3 are viable on 23, and unevenly.

So A1 becomes the backbone rather than a floor, and the A1→A2→A3 comparisons must
be run **only on the subset where all three corpora exist**, with the coverage
distribution reported alongside. Comparing an A3 hit rate computed on 23 well-covered
names against an A1 rate computed on 40 would be measuring market cap, not method.

Two consequences to build in:

- **Report every result stratified by coverage**, never pooled. A pooled number here
  is a market-cap average wearing a method's name.
- **The starvation rate is itself a finding.** 20% of a randomly drawn universe cannot
  be researched from public news at all. That is worth knowing about the live
  pipeline, which currently writes a dossier regardless.
