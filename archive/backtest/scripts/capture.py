#!/usr/bin/env python3
"""Track B: forward capture. Sweep the run-in to a print, before the print exists.

Everything in `corpus_news.py` -- the Wayback tiering, htmldate, the tells regex,
the safety margin -- exists for one reason: retrospective capture cannot prove
when bytes existed. Capture forward and that proof is free. We fetched it, we
stamped it, and the print has not happened yet. There is one tier, and it needs
no audit.

## The split

Discovery is the agent's. Fetching is this script's.

The live pipeline researches with `WebSearch` and `WebFetch` across nine areas
(see `.claude/agents/earnings-deep-researcher.md`). A corpus swept by a script
with its own source list would test reasoning over a document set the production
policy never chose, which is a different experiment. So the agent runs the same
nine-area search program it always runs -- forward, before the print -- and hands
this script a plan: the queries it issued, the results each returned, and the
URLs worth a body.

That is also why the plan records queries and their result lists verbatim, not
just the URLs kept. The (query -> results) mapping IS the frozen search index a
backtest arm searches against at replay, and the fraction of an arm's queries
that miss it is the honest measure of how wide the capture was.

No news APIs. Finnhub and Alpha Vantage are deliberately absent: their coverage,
their ranking and their clocks are not what production uses, and section 19 is a
standing reminder that a vendor timestamp is a claim rather than a clock.

## Three properties that make a daily sweep affordable

  * **Capture is session-agnostic.** Nasdaq supplies a session for well under
    half of future rows (`time-not-supplied` on 8 of 14 for 2026-08-31), and
    guessing it up front would be a needless dependency. We do not need it. Every
    document carries the instant WE fetched it, so the fence is applied after the
    print by `seal.py`, using the EDGAR 8-K acceptance time that FINDINGS.md
    section 3 established as exact. Capture wide, seal precisely, later.

  * **Content-addressed storage makes the daily re-sweep nearly free.** A
    document refetched unchanged costs one manifest line, not a copy. A document
    that CHANGED gets a new hash, and the pair is the narrative moving into the
    print -- an updated preview, a revised estimate, a headline rewritten after a
    pre-announcement. No retrospective corpus can reconstruct that at any price.

  * **The script spends no model tokens.** HTTP and text extraction only. The
    agent layer sits on top and is the only part that costs anything, which is
    what lets the sweep run every day without touching the budget the research
    stages live on.

## Deterministic layers

Two sources the researcher relies on but cannot get from a search engine, plus
one that serves area 7 directly. All keyless:

  edgar       submissions API; immutable, SEC-timestamped, needs no fence
  quote       daily bars, for the price and run-up anchors of area 2
  stocktwits  cashtag-indexed, exact ISO per message, so no ticker matching

The tells regex is kept, but as a TRIPWIRE rather than a filter. A body captured
before a print should never contain post-earnings language. If one does, the
event date is wrong or the calendar is stale -- that is a bug report, not a
document to discard, so it is recorded and the run warns.
"""
import argparse, hashlib, json, re, sys, time
import urllib.parse, urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import fetch, ticker_cik_map, submissions, ROOT

try:
    import trafilatura
except ImportError:
    trafilatura = None

UA = {"User-Agent": "Mozilla/5.0 (compatible; claude-research-capture)"}
NASDAQ = "https://api.nasdaq.com/api/calendar/earnings?date={d}"
YQ = "https://query1.finance.yahoo.com"
ST = "https://api.stocktwits.com/api/2/streams/symbol/{t}.json?limit=30"

# Post-event language. Forward, this can only fire on a bug -- see the tripwire
# note above. Same patterns as corpus_news.TELLS, deliberately blunt.
TELLS = [
    r"\bbeat(?:s|ing)?\s+(?:the\s+)?(?:consensus|estimates?|expectations?)",
    r"\bmiss(?:es|ed|ing)?\s+(?:the\s+)?(?:consensus|estimates?|expectations?)",
    r"\bshares?\s+(?:rose|fell|jumped|plunged|surged|sank|tumbled|soared|slid)",
    r"\bstock\s+(?:rose|fell|jumped|plunged|surged|sank|tumbled|soared|slid)",
    r"\breported\s+(?:quarterly\s+)?(?:earnings|revenue|results)\s+of",
    r"\bafter\s+(?:the\s+)?(?:company\s+)?reported\b",
    r"\bpost[- ]earnings\b",
]
# NOT included forward: `earnings call transcript`. corpus_news.py carries it
# because retrospectively it marks a document that can only exist after a print.
# Forward it is navigation chrome -- every aggregator quote page links to one --
# and it tripped on stockanalysis.com's SAIC page, which is a perfectly ordinary
# pre-event quote page that also names the upcoming date. A tripwire that fires
# on a nav link is a tripwire nobody reads.
TELL_RX = [re.compile(p, re.I) for p in TELLS]

# Post-event fields on the calendar row. FINDINGS.md section 2: the historical
# calendar contains the answer, so these never reach disk.
DROP = {"eps", "surprise", "lastYearEPS", "lastYearRptDt"}


def now_utc():
    return datetime.now(timezone.utc)


def stamp(dt=None):
    return (dt or now_utc()).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get(url, timeout=30, tries=2, headers=None):
    last = None
    for _ in range(tries):
        try:
            r = urllib.request.urlopen(
                urllib.request.Request(url, headers=headers or UA), timeout=timeout)
            return json.loads(r.read()), None
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:70]}"
            time.sleep(0.6)
    return None, last


def parse_cap(s):
    try:
        return float(str(s).replace("$", "").replace(",", ""))
    except Exception:
        return 0.0


# ------------------------------------------------------------------ universe

def forward_universe(dfrom, dto, min_cap=0.0):
    """Every US earnings event scheduled in [dfrom, dto], deduped by ticker+date.

    Deliberately unfiltered by session. Nasdaq's `time` field is absent for most
    future rows and is not needed -- see the module docstring.
    """
    out, seen = [], set()
    d = dfrom
    while d <= dto:
        if d.weekday() < 5:
            j, _ = _get(NASDAQ.format(d=d.isoformat()), timeout=25, tries=3)
            for r in ((j or {}).get("data") or {}).get("rows") or []:
                tk = (r.get("symbol") or "").strip().upper()
                if not tk or (tk, d.isoformat()) in seen:
                    continue
                cap = parse_cap(r.get("marketCap"))
                if cap < min_cap:
                    continue
                seen.add((tk, d.isoformat()))
                out.append({
                    "ticker": tk,
                    "company": r.get("name") or "",
                    "event_date": d.isoformat(),
                    "market_cap_usd_today": cap,
                    "consensus_eps_forecast": r.get("epsForecast") or None,
                    "n_estimates": r.get("noOfEsts") or None,
                    "fiscal_quarter_ending": r.get("fiscalQuarterEnding") or None,
                    "calendar_time_hint": r.get("time") or None,
                    "session": None,          # resolved by seal.py, from EDGAR
                    "first_seen_utc": stamp(),
                })
        d += timedelta(days=1)
    return out


# ------------------------------------------------------- content-addressed store

def store_doc(evdir, text, meta):
    """Write `text` under its own sha1. Returns (sha, is_new).

    The dedup is the whole economy of a daily sweep: an article that has not
    changed since yesterday costs one manifest reference. An article that HAS
    changed lands under a new hash next to the old one, which is the signal.
    """
    body = text or ""
    sha = hashlib.sha1(body.encode("utf-8", "replace")).hexdigest()
    docs = evdir / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    p = docs / f"{sha}.txt"
    new = not p.exists()
    if new:
        head = "\n".join(f"{k.upper()}: {v}" for k, v in meta.items() if v not in (None, ""))
        p.write_text(head + "\n\n" + body, encoding="utf-8")
    return sha, new


def extract(html):
    if not html:
        return ""
    if trafilatura is None:
        return re.sub(r"<[^>]+>", " ", html)[:200000]
    return trafilatura.extract(html, include_comments=False, include_tables=True) or ""


MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def _event_date_forms(event_date):
    """The ways a document might name this event's date."""
    d = date.fromisoformat(event_date)
    m, mon = MONTHS[d.month - 1], MONTHS[d.month - 1][:3]
    return [event_date, f"{m} {d.day}, {d.year}", f"{mon} {d.day}, {d.year}",
            f"{mon}. {d.day}, {d.year}", f"{d.day} {m} {d.year}"]


def scan_tells(text, event_date=None):
    """Post-earnings language that refers to THIS print.

    The naive version of this check -- any tell, anywhere -- fires on every
    prior-quarter recap in the corpus, and those are legitimate: FINDINGS.md
    section 5 makes the point that the previous quarter's release carries the
    guidance this print will be judged against. A tripwire that fires on normal
    operation gets ignored, which is the section 20 failure in a new place.

    So a tell only counts when the body also names this event's date. A recap of
    last September's quarter passes silently; a recap of a print that has not
    happened yet does not, and that is the only case worth waking someone for.
    """
    t = text or ""
    hits = [p.pattern for p in TELL_RX if p.search(t)]
    if not hits or not event_date:
        return []
    return hits if any(f in t for f in _event_date_forms(event_date)) else []


# ------------------------------------------------------- agent-planned fetching

def _snippet_fallback(evdir, it, url, why, seen_urls, event_date):
    """Store the search snippet when the body cannot be had.

    Measured on the SAIC test run: 6 of 11 planned URLs failed -- three timeouts
    on wire sites, three HTTP errors from domains behind bot protection
    (tipranks, simplywall.st). That is the same wall the live researcher hits,
    and its environment note already prescribes the answer: cite the source and
    mark the datum `snippet_only` so downstream knows its confidence level.

    Losing the datum entirely would be worse and quieter. A snippet with correct
    provenance is a weaker document, not a missing one, and the distinction is
    recoverable later because it is written into the record.
    """
    snip = (it.get("snippet") or "").strip()
    if not snip:
        return None, {"url": url, "status": why + "; no snippet in plan"}
    body = f"[SNIPPET ONLY - body unreachable: {why}]\n\n{it.get('title') or ''}\n\n{snip}"
    sha, new = store_doc(evdir, body, {
        "source": url, "provider": "agent-websearch", "snippet_only": True,
        "unreachable_reason": why, "area": it.get("area"),
        "headline": it.get("title"), "query": it.get("query"),
        "fetched_utc": stamp()})
    seen_urls.add(url)
    return ({"kind": "news", "url": url, "sha": sha, "new": new,
             "snippet_only": True, "area": it.get("area"),
             "query": it.get("query"), "headline": it.get("title"),
             "chars": len(body),
             "tripwire_tells": scan_tells(body, event_date)[:3] or None},
            {"url": url, "status": why + "; stored as snippet_only"})


def fetch_planned(evdir, plan_urls, seen_urls, max_docs, log, event_date=None):
    """Fetch every URL the agent's search program surfaced.

    The script does not choose these. That is the point of the split: the
    production policy picks the documents, so the captured corpus is the corpus
    production would have read.
    """
    rows = []
    for it in plan_urls:
        if len(rows) >= max_docs:
            log.append({"url": it.get("url"), "status": "over max_docs"})
            continue
        u = (it.get("url") or "").strip()
        if not u or u in seen_urls:
            continue
        try:
            html = fetch(u, timeout=50, retries=2)
        except Exception as e:
            rec = _snippet_fallback(evdir, it, u, f"fetch failed: {type(e).__name__}",
                                    seen_urls, event_date)
            log.append(rec[1])
            if rec[0]:
                rows.append(rec[0])
            continue
        text = extract(html)
        if len(text) < 300:
            rec = _snippet_fallback(evdir, it, u, f"thin: {len(text)} chars",
                                    seen_urls, event_date)
            log.append(rec[1])
            if rec[0]:
                rows.append(rec[0])
            continue
        meta = {"source": u, "provider": "agent-websearch",
                "area": it.get("area"), "headline": it.get("title"),
                "why": it.get("why"), "query": it.get("query"),
                "fetched_utc": stamp()}
        sha, new = store_doc(evdir, text, meta)
        tells = scan_tells(text, event_date)
        rows.append({"kind": "news", "url": u, "sha": sha, "new": new,
                     "area": it.get("area"), "query": it.get("query"),
                     "headline": it.get("title"), "chars": len(text),
                     "tripwire_tells": tells[:3] or None})
        seen_urls.add(u)
    return rows


def store_search_trace(evdir, searches):
    """The frozen search index: every query the agent issued and what came back.

    Stored even for queries whose results were never fetched. A replayed arm that
    issues a query we never issued should be able to find that out, and a miss
    rate is only meaningful against a record of what WAS asked.
    """
    if not searches:
        return None
    payload = {"captured_utc": stamp(), "n_queries": len(searches),
               "searches": searches}
    p = evdir / "search_trace"
    p.mkdir(exist_ok=True)
    f = p / f"{stamp().replace(':', '').replace('-', '')}.json"
    f.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return f.name


# --------------------------------------------------------------- social layer

def social_stocktwits(evdir, ticker, since_id, max_pages=3):
    """Delta since the last message we saw. The daily-increment argument in one
    call: FINDINGS.md section 21 measured ~75 pages to backfill 14 days; run
    daily and an active name is 3-6 pages, a quiet one is 1."""
    msgs, cursor, pages, err = [], None, 0, None
    while pages < max_pages:
        u = ST.format(t=ticker) + (f"&max={cursor}" if cursor else "")
        j, e = _get(u, timeout=30)
        if e:
            err = e
            break
        batch = (j or {}).get("messages") or []
        if not batch:
            break
        stop = False
        for m in batch:
            if since_id and m.get("id") and m["id"] <= since_id:
                stop = True
                break
            msgs.append({"id": m.get("id"), "created_at": m.get("created_at"),
                         "body": m.get("body"),
                         "sentiment": ((m.get("entities") or {}).get("sentiment") or {}).get("basic")})
        if stop or len(batch) < 30:
            break
        cursor = batch[-1].get("id")
        pages += 1
        time.sleep(0.4)
    if not msgs:
        return None, err, since_id
    text = "\n".join(f"[{m['created_at']}] ({m.get('sentiment') or '-'}) {m['body']}"
                     for m in msgs if m.get("body"))
    sha, new = store_doc(evdir, text, {"source": f"stocktwits ${ticker}",
                                       "provider": "stocktwits",
                                       "n_messages": len(msgs),
                                       "fetched_utc": stamp()})
    top = max((m["id"] for m in msgs if m.get("id")), default=since_id)
    return {"kind": "social", "sha": sha, "new": new, "provider": "stocktwits",
            "n_messages": len(msgs), "chars": len(text)}, err, top


# -------------------------------------------------------------- filings layer

def filings_edgar(evdir, cik, seen_accessions, lookback_days=400, max_new=200):
    """Index EDGAR filings. Records pointers, never bodies.

    Measured on the first two captures: filing bodies were 98.9% of AIV's bytes
    and 89.4% of SAIC's. They are also the one layer that does not need storing.
    EDGAR is immutable and permanently addressable by accession, so the pointer
    IS the document -- `rehydrate.py` fetches it back byte-identical whenever a
    reader actually needs the text.

    Dropping them takes an event from ~1.1MB to roughly 50KB, which is the whole
    difference between a corpus this repository can hold for a year and one it
    cannot hold for a month. It also removes 46 HTTP round trips per first
    capture, which was most of the wall clock.
    """
    if not cik:
        return [], "no cik"
    try:
        sub = submissions(cik)
    except Exception as e:
        return [], f"{type(e).__name__}: {str(e)[:60]}"
    rec = ((sub or {}).get("filings") or {}).get("recent") or {}
    forms = rec.get("form") or []
    floor = (now_utc().date() - timedelta(days=lookback_days)).isoformat()
    col = lambda k: rec.get(k) or [None] * len(forms)
    rows = []
    for i, form in enumerate(forms):
        if len(rows) >= max_new:
            break
        acc, fdate = col("accessionNumber")[i], col("filingDate")[i] or ""
        doc = col("primaryDocument")[i]
        if not acc or not doc or acc in seen_accessions or fdate < floor:
            continue
        rows.append({
            "kind": "filing", "new": True, "form": form,
            "filing_date": fdate, "accession": acc,
            "accepted_utc": col("acceptanceDateTime")[i],
            "primary_document": doc, "items": col("items")[i] or None,
            "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
                   f"{acc.replace('-', '')}/{doc}",
            "indexed_utc": stamp()})
        seen_accessions.add(acc)
    if rows:
        (evdir / "filings.json").write_text(json.dumps(
            {"cik": cik, "lookback_days": lookback_days,
             "filings": sorted(_load_filings(evdir) + rows,
                               key=lambda r: r["filing_date"], reverse=True)},
            indent=1), encoding="utf-8")
    return rows, None


def _load_filings(evdir):
    p = evdir / "filings.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("filings") or []


# ---------------------------------------------------------------- price layer

def quote_bar(ticker):
    u = f"{YQ}/v8/finance/chart/{ticker}?range=3mo&interval=1d"
    j, err = _get(u, timeout=25)
    if err:
        return None, err
    try:
        res = j["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        bars = [{"date": datetime.fromtimestamp(t, timezone.utc).date().isoformat(),
                 "close": c, "volume": v}
                for t, c, v in zip(res["timestamp"], q["close"], q["volume"])
                if c is not None]
        return {"bars": bars[-63:], "fetched_utc": stamp()}, None
    except Exception as e:
        return None, f"parse: {type(e).__name__}"


# -------------------------------------------------------------------- capture

def days_to_event(ev):
    try:
        return (date.fromisoformat(ev["event_date"]) - now_utc().date()).days
    except Exception:
        return 999


def capture_event(ev, root, plan=None, max_docs=40, skip_social=False):
    """One daily snapshot for one event. Idempotent: re-running the same day adds
    only what changed."""
    evdir = Path(root) / "events" / f"{ev['ticker']}-{ev['event_date']}"
    evdir.mkdir(parents=True, exist_ok=True)

    epath = evdir / "event.json"
    if not epath.exists():
        epath.write_text(json.dumps({k: v for k, v in ev.items() if k not in DROP},
                                    indent=1), encoding="utf-8")

    spath = evdir / "state.json"
    state = json.loads(spath.read_text()) if spath.exists() else {}
    seen_urls = set(state.get("seen_urls") or [])
    seen_acc = set(state.get("seen_accessions") or [])

    started = stamp()
    rows, errs, log = [], {}, []
    plan = plan or {}

    trace_file = store_search_trace(evdir, plan.get("searches"))
    rows += fetch_planned(evdir, plan.get("fetch") or [], seen_urls, max_docs, log,
                          ev["event_date"])

    if not skip_social:
        srow, e3, top_id = social_stocktwits(evdir, ev["ticker"], state.get("stocktwits_max_id"))
        if e3:
            errs["stocktwits"] = e3
        if srow:
            rows.append(srow)
    else:
        top_id = state.get("stocktwits_max_id")

    cik = ev.get("cik") or state.get("cik") or ticker_cik_map().get(ev["ticker"])
    # No per-run cap any more. Indexing costs one submissions call, so the whole
    # lookback lands on first sight; a flat 12 used to walk backwards through the
    # catalogue and would have reached the prior-year 10-K a week after the print.
    frows, e4 = filings_edgar(evdir, cik, seen_acc)
    if e4:
        errs["edgar"] = e4
    rows += frows

    qb, e5 = quote_bar(ev["ticker"])
    if e5:
        errs["quote"] = e5
    if qb:
        (evdir / "quote.json").write_text(json.dumps(qb, indent=1), encoding="utf-8")

    snapdir = evdir / "snapshots"
    snapdir.mkdir(exist_ok=True)
    tripwires = [r for r in rows if r.get("tripwire_tells")]
    snap = {"ticker": ev["ticker"], "event_date": ev["event_date"],
            "capture_started_utc": started, "capture_finished_utc": stamp(),
            "search_trace": trace_file,
            "n_queries": len((plan.get("searches") or [])),
            "n_items": len(rows), "n_new": sum(1 for r in rows if r.get("new")),
            "n_snippet_only": sum(1 for r in rows if r.get("snippet_only")),
            "n_filings_indexed": sum(1 for r in rows if r["kind"] == "filing"),
            "n_bodies_stored": sum(1 for r in rows if r.get("sha")),
            "tripwires": tripwires or None, "errors": errs or None,
            "skipped": log or None, "items": rows}
    (snapdir / f"{started.replace(':', '').replace('-', '')}.json").write_text(
        json.dumps(snap, indent=1), encoding="utf-8")

    state.update({"seen_urls": sorted(seen_urls), "seen_accessions": sorted(seen_acc),
                  "stocktwits_max_id": top_id, "cik": cik,
                  "last_capture_utc": stamp()})
    spath.write_text(json.dumps(state, indent=1), encoding="utf-8")
    return snap


def main():
    ap = argparse.ArgumentParser(description="Track B forward capture.")
    ap.add_argument("--root", default=str(ROOT / "captures"))
    ap.add_argument("--from-date", help="ISO. default: today")
    ap.add_argument("--to-date", help="ISO. default: from-date + horizon")
    ap.add_argument("--horizon-days", type=int, default=15)
    ap.add_argument("--min-cap", type=float, default=0.0,
                    help="market-cap floor in USD. 0 = every scheduled name")
    ap.add_argument("--tickers", help="comma list; capture only these")
    ap.add_argument("--plan", help="capture plan JSON written by the agent")
    ap.add_argument("--max-docs", type=int, default=40)
    ap.add_argument("--skip-social", action="store_true")
    ap.add_argument("--social-within-days", type=int, default=2,
                    help="only capture StockTwits for events this close. The "
                         "universe is tracked far wider than social is captured "
                         "-- see the note in main().")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--universe-only", action="store_true")
    a = ap.parse_args()

    root = Path(a.root)
    root.mkdir(parents=True, exist_ok=True)
    dfrom = date.fromisoformat(a.from_date) if a.from_date else now_utc().date()
    dto = date.fromisoformat(a.to_date) if a.to_date else dfrom + timedelta(days=a.horizon_days)

    uni = forward_universe(dfrom, dto, a.min_cap)
    if a.tickers:
        want = {t.strip().upper() for t in a.tickers.split(",")}
        uni = [e for e in uni if e["ticker"] in want]
    if a.limit:
        uni = uni[:a.limit]

    upath = root / "universe.json"
    prev = json.loads(upath.read_text()) if upath.exists() else []
    known = {(e["ticker"], e["event_date"]) for e in prev}
    merged = prev + [e for e in uni if (e["ticker"], e["event_date"]) not in known]
    upath.write_text(json.dumps(merged, indent=1), encoding="utf-8")

    print(f"universe {dfrom} -> {dto}: {len(uni)} events "
          f"({len(merged) - len(prev)} new, {len(merged)} tracked)")
    if a.universe_only:
        return 0

    plan = json.loads(Path(a.plan).read_text(encoding="utf-8")) if a.plan else {}
    if plan and not a.tickers:
        print("  note: --plan given without --tickers; the plan applies to every "
              "event in the sweep, which is almost never what you want")

    tot_new = 0
    for i, ev in enumerate(uni, 1):
        p = plan if (not plan or plan.get("ticker", ev["ticker"]) == ev["ticker"]) else {}
        # StockTwits is the only rate-limited layer and it decides the wall clock.
        # Measured on the 2026-08-30 sweep: 3.5s per event with social, 1.0s
        # without, over a 229-event 15-day window. FINDINGS.md section 21 puts
        # unauthenticated limiting near 200 requests/hour, and the window sizes
        # out like this:
        #
        #     <=1d   14 near   42 reqs   4.4 min
        #     <=2d   42 near  126 reqs   5.6 min     <- default
        #     <=3d   83 near  249 reqs   7.3 min     over the ceiling
        #     <=5d  147 near  441 reqs   9.9 min     cannot finish
        #
        # Two days costs nothing real. The sweep runs daily, so a name is still
        # captured at D-2 and D-1, and an AMC name again on D because 17:03 CEST
        # is 11:03 ET, before the close. Chatter two weeks out is thin anyway.
        # Track the universe wide, capture social near.
        near = days_to_event(ev) <= a.social_within_days
        skip_social = a.skip_social or not near
        try:
            s = capture_event(ev, root, p, a.max_docs, skip_social)
        except Exception as e:
            print(f"  [{i}/{len(uni)}] {ev['ticker']:<6} FAILED {type(e).__name__}: {str(e)[:60]}")
            continue
        tot_new += s["n_new"]
        flag = "  TRIPWIRE" if s.get("tripwires") else ""
        errs = ",".join(s["errors"]) if s.get("errors") else "-"
        print(f"  [{i}/{len(uni)}] {ev['ticker']:<6} d{days_to_event(ev):<3} "
              f"q={s['n_queries']:<3} items={s['n_items']:<3} new={s['n_new']:<3} "
              f"soc={'-' if skip_social else 'y'} err={errs}{flag}", flush=True)
    print(f"done: {tot_new} new documents under {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
