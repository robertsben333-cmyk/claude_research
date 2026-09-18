#!/usr/bin/env python3
"""Tier 2/3 news corpus: ticker-indexed discovery, date-fenced, then verified.

The ticker-matching problem that makes a raw archive sweep painful does not exist
here: news APIs tag articles with the ticker at ingestion, so discovery is a
single ranged query per event rather than a text match over the whole web.

    provider(ticker, from, to) -> [{url, published_utc, headline, source}]

Three providers, tried in order, all ticker-tagged and all date-ranged:

  finnhub       /company-news?symbol=&from=&to=      free key, ~1y history
  alphavantage  NEWS_SENTIMENT&tickers=&time_from=   free key, sentiment included
  firecrawl     /v2/search with tbs=cdr:1,...        paid; backfill for thin names

Discovery date fences are necessary but never sufficient, so every candidate is
verified independently before it enters the corpus:

  1. provider's published_utc  <  cutoff
  2. htmldate on the fetched body  <  cutoff        (claimed publication date)
  3. body scan finds no post-cutoff tells
  4. if Wayback holds a snapshot before the cutoff, that body is used instead of
     the live one -- which upgrades the document from tier 3 to tier 2 for free

A document that fails 1-3 is rejected and recorded. A document that passes but
could only be fetched live is kept as tier 3 and counted, because the honest
number to publish is the tier-3 share, not a claim that there is none.
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore, Lock
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import fetch

UA = {"User-Agent": "Mozilla/5.0 (compatible; claude-research-backtest)"}

# Finnhub's news `datetime` is a unix timestamp whose wall-clock is EASTERN, not
# UTC. Measured against EDGAR 8-K acceptance times, which are authoritative:
#
#   OKTA 2026-08-26   8-K 20:03:06Z   "Q2 Adj. EPS $1.05 Beats" 16:02:00Z   -4.02h
#   BILL 2026-08-19   8-K 20:02:15Z   "Q4 Adj. EPS $0.84 Beats" 16:01:53Z   -4.01h
#   WOLF 2026-08-19   8-K 20:40:15Z   "Reports Mixed Q4"        16:21:03Z   -4.32h
#
# Left uncorrected this puts every article from the four hours after an AMC print
# on the safe side of the fence -- the entire post-release flood. Reinterpret the
# wall-clock as ET and convert properly.
ET = ZoneInfo("America/New_York")

# archive.org needs its own, much tighter budget than the rest of the pipeline.
# Raising the worker pool from 1 to 10 cut the wall clock from 15 minutes to two
# -- and pushed failed archive lookups from 2 to 25, because every worker hit
# web.archive.org at once. Those failures do not raise; they quietly demote
# documents to tier 3 and degrade the exact number this project publishes as its
# quality measure. Concurrency here is a per-host question, not a global one.
_WB_SLOTS = BoundedSemaphore(2)
_WB_LOCK = Lock()
_WB_LAST = [0.0]
_WB_MIN_GAP = 0.8


class _ArchiveThrottle:
    def __enter__(self):
        _WB_SLOTS.acquire()
        with _WB_LOCK:
            gap = time.time() - _WB_LAST[0]
            if gap < _WB_MIN_GAP:
                time.sleep(_WB_MIN_GAP - gap)
            _WB_LAST[0] = time.time()
        return self

    def __exit__(self, *exc):
        _WB_SLOTS.release()
        return False


def et_wallclock_to_utc(ts):
    naive = datetime.fromtimestamp(ts, timezone.utc).replace(tzinfo=None)
    return naive.replace(tzinfo=ET).astimezone(timezone.utc)

# Phrases that only exist in a body written after the print. Deliberately blunt:
# a false rejection costs one article, a false acceptance corrupts an experiment.
TELLS = [
    r"\bbeat(?:s|ing)?\s+(?:the\s+)?(?:consensus|estimates?|expectations?)",
    r"\bmiss(?:es|ed|ing)?\s+(?:the\s+)?(?:consensus|estimates?|expectations?)",
    r"\bshares?\s+(?:rose|fell|jumped|plunged|surged|sank|tumbled|soared|slid)",
    r"\bstock\s+(?:rose|fell|jumped|plunged|surged|sank|tumbled|soared|slid)",
    r"\breported\s+(?:quarterly\s+)?(?:earnings|revenue|results)\s+of",
    r"\bafter\s+(?:the\s+)?(?:company\s+)?reported\b",
    r"\bpost[- ]earnings\b", r"\bearnings\s+call\s+transcript\b",
    r"\braised\s+(?:its\s+)?(?:full[- ]year\s+)?(?:guidance|outlook)\s+(?:after|following)\b",
]
TELL_RX = [re.compile(p, re.I) for p in TELLS]


# ---------------------------------------------------------------- providers

def provider_finnhub(ticker, dfrom, dto):
    key = os.environ.get("FINNHUB_KEY")
    if not key:
        return None, "FINNHUB_KEY not set"
    u = (f"https://finnhub.io/api/v1/company-news?symbol={ticker}"
         f"&from={dfrom}&to={dto}&token={key}")
    try:
        rows = json.loads(fetch(u, timeout=45))
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:110]}"
    return [{"url": r.get("url"), "headline": r.get("headline"),
             "source": r.get("source"),
             "published_utc": et_wallclock_to_utc(r.get("datetime", 0))
             .isoformat().replace("+00:00", "Z")}
            for r in rows if r.get("url")], None


def provider_alphavantage(ticker, dfrom, dto):
    key = os.environ.get("ALPHAVANTAGE_KEY")
    if not key:
        return None, "ALPHAVANTAGE_KEY not set"
    u = ("https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
         f"&tickers={ticker}&time_from={dfrom.replace('-','')}T0000"
         f"&time_to={dto.replace('-','')}T2359&limit=200&apikey={key}")
    try:
        d = json.loads(fetch(u, timeout=60))
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:110]}"
    if "feed" not in d:
        return None, f"no feed in response: {str(d)[:120]}"
    out = []
    for r in d["feed"]:
        t = r.get("time_published", "")          # YYYYMMDDTHHMMSS
        iso = (f"{t[:4]}-{t[4:6]}-{t[6:8]}T{t[9:11]}:{t[11:13]}:{t[13:15]}Z"
               if len(t) >= 15 else None)
        out.append({"url": r.get("url"), "headline": r.get("title"),
                    "source": r.get("source"), "published_utc": iso})
    return [x for x in out if x["url"] and x["published_utc"]], None


def provider_firecrawl(ticker, dfrom, dto, company=""):
    key = os.environ.get("FIRECRAWL_KEY")
    if not key:
        return None, "FIRECRAWL_KEY not set"
    def g(d):
        y, m, dd = d.split("-")
        return f"{int(m)}/{int(dd)}/{y}"
    payload = json.dumps({
        "query": f"{company or ticker} ({ticker}) earnings preview analyst",
        "limit": 20,
        "tbs": f"cdr:1,cd_min:{g(dfrom)},cd_max:{g(dto)}",
    }).encode()
    req = urllib.request.Request("https://api.firecrawl.dev/v2/search", data=payload,
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=90).read())
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:110]}"
    web = (d.get("data") or {}).get("web") or d.get("data") or []
    # Google's tbs filters on ITS crawl date, not the publication date, and
    # third-party pass-through is imprecise -- so these carry no timestamp we
    # trust. They go forward with published_utc unknown and must earn their
    # place from htmldate alone.
    return [{"url": r.get("url"), "headline": r.get("title"),
             "source": "firecrawl/google", "published_utc": None} for r in web
            if r.get("url")], None


PROVIDERS = [("finnhub", provider_finnhub),
             ("alphavantage", provider_alphavantage),
             ("firecrawl", provider_firecrawl)]


# ---------------------------------------------------------------- content

def wayback_before(url, cutoff_iso, tries=3):
    """Snapshot strictly before the cutoff.

    Returns (snapshot_url, timestamp, status). CDX with an explicit `to` bound --
    never the availability API, which returns the closest snapshot in EITHER
    direction and will hand back post-event content.

    The status matters as much as the result. An earlier version returned None
    both when no snapshot existed and when archive.org simply refused the query,
    and archive.org refuses often. That silently downgraded documents to tier 3
    and inflated the one number this project publishes as its honesty check.
    """
    to = cutoff_iso.replace("-", "").replace(":", "").replace("T", "")[:14]
    q = ("http://web.archive.org/cdx/search/cdx?output=json&limit=-3&filter=statuscode:200"
         f"&to={to}&url={urllib.parse.quote(url, safe='')}")
    last = None
    for i in range(tries):
        try:
            with _ArchiveThrottle():
                rows = json.loads(fetch(q, timeout=30, retries=0))
            break
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:60]}"
            time.sleep(2.0 * (i + 1))
    else:
        return None, None, f"lookup_failed ({last})"
    if len(rows) < 2:
        return None, None, "no_snapshot"
    ts = rows[-1][1]
    if ts >= to:
        return None, None, "no_snapshot_before_cutoff"
    return f"http://web.archive.org/web/{ts}id_/{url}", ts, "ok"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        raise urllib.error.HTTPError(req.full_url, code, newurl, hdrs, None)


_OPENER = urllib.request.build_opener(_NoRedirect)


def resolve_url(url, hops=4, timeout=25):
    """Follow redirects to the canonical publisher URL.

    Finnhub returns its own `finnhub.io/api/news?id=...` redirect URLs rather
    than publisher URLs. Used as-is they break the corpus twice over: archive.org
    can never hold a snapshot of a per-request redirect, so every document is
    forced to tier 3, and the redirect itself often refuses a plain fetch, which
    showed up as 19 of 24 documents 'body unavailable'. Resolving first restores
    both the archive lookup and the fetch.
    """
    cur = url
    for _ in range(hops):
        try:
            _OPENER.open(urllib.request.Request(cur, headers=UA), timeout=timeout)
            return cur, None
        except urllib.error.HTTPError as e:
            if 300 <= e.code < 400 and isinstance(e.msg, str) and e.msg.startswith("http"):
                cur = e.msg
                continue
            return cur, (None if e.code < 400 else f"HTTP {e.code}")
        except Exception as e:
            return cur, f"{type(e).__name__}: {str(e)[:50]}"
    return cur, "too many redirects"


META_DATE_RX = [
    re.compile(r"""<meta[^>]+property=["']article:published_time["'][^>]+content=["']([^"']+)""", re.I),
    re.compile(r"""<meta[^>]+name=["'](?:pubdate|publish-date|date)["'][^>]+content=["']([^"']+)""", re.I),
    re.compile(r'"datePublished"\s*:\s*"([^"]+)"', re.I),
]


def published_date(html):
    """Publication date, publisher metadata first, htmldate second.

    htmldate reads the page-render date on SPA-ish sites -- a TradingView-hosted
    Zacks preview whose body says "is set to release second-quarter results on
    Aug. 26" was dated two days AFTER the print and thrown away. Explicit
    publisher metadata is both more reliable and cheaper when it is present.
    """
    for rx in META_DATE_RX:
        m = rx.search(html or "")
        if m and len(m.group(1)) >= 10:
            return m.group(1)[:10], "meta"
    try:
        from htmldate import find_date
        d = find_date(html, outputformat="%Y-%m-%d", extensive_search=False)
        return (d, "htmldate") if d else (None, "none")
    except Exception:
        return None, "none"


def body_of(url, timeout=45):
    try:
        return fetch(url, timeout=timeout)
    except Exception:
        return None


def scan_tells(text):
    return [p.pattern for p, m in ((p, p.search(text)) for p in TELL_RX) if m]


# ---------------------------------------------------------------- harvest

def harvest(ticker, company, cutoff_iso, outdir, window_days=14, max_docs=40,
            providers=None, margin_hours=1.0, workers=8):
    try:
        import trafilatura
    except ImportError:
        sys.exit("pip install trafilatura htmldate")
    outdir = Path(outdir); nd = outdir / "news"
    # Purge before writing. Successive runs used different fence semantics -- an
    # uncorrected clock, unresolved redirect URLs -- and their output stayed on
    # disk. 55 files accumulated in a directory where one run had kept 14, and a
    # sealed reader would have read all 55 as though they were current. Derived
    # state must be rebuilt, never appended to.
    if nd.exists():
        for old in nd.glob("*.txt"):
            old.unlink()
    nd.mkdir(parents=True, exist_ok=True)
    cutoff = datetime.fromisoformat(cutoff_iso.replace("Z", "+00:00"))
    fence = cutoff - timedelta(hours=margin_hours)
    fence_iso = fence.isoformat().replace("+00:00", "Z")
    dto = cutoff.date().isoformat()
    dfrom = (cutoff - timedelta(days=window_days)).date().isoformat()

    candidates, prov_log, seen = [], [], set()
    for name, fn in PROVIDERS:
        if providers and name not in providers:
            continue
        rows, err = (fn(ticker, dfrom, dto, company) if name == "firecrawl"
                     else fn(ticker, dfrom, dto))
        prov_log.append({"provider": name, "error": err,
                         "returned": None if rows is None else len(rows)})
        for r in (rows or []):
            if r["url"] not in seen:
                seen.add(r["url"]); r["provider"] = name; candidates.append(r)

    # Each document costs a redirect resolve, an archive lookup and a fetch --
    # all network-bound and all independent. Run serially, 52 candidates blew a
    # 900s wall clock twice. A thread pool is the whole difference between one
    # ticker and forty.
    def _process(c):
        rec = {"url": c["url"], "provider": c["provider"], "source": c.get("source"),
               "provider_published_utc": c.get("published_utc")}
        # check 1 -- provider timestamp, clock-corrected, with a safety margin.
        # The margin exists because a provider clock that was wrong once can be
        # wrong again in a way no calibration caught.
        if c.get("published_utc") and c["published_utc"] >= fence_iso:
            return rec | {"status": f"rejected: provider timestamp at/after fence {fence_iso}"}, None
        # resolve provider redirect -> canonical publisher URL before any archive
        # lookup, or the lookup is guaranteed to miss
        canon, rerr = resolve_url(c["url"])
        rec["canonical_url"] = canon if canon != c["url"] else None
        if rerr:
            rec["resolve_error"] = rerr
        target = canon
        # content: archive first (tier 2), live second (tier 3)
        wb_url, wb_ts, wb_status = wayback_before(target, cutoff_iso)
        rec["wayback_status"] = wb_status
        if wb_url:
            html, tier, note = body_of(wb_url), 2, f"wayback snapshot {wb_ts}"
            if html is None:
                html, tier, note = body_of(target), 3, "live fetch (snapshot fetch failed)"
        else:
            html, tier, note = body_of(target), 3, f"live fetch ({wb_status})"
        if not html:
            return rec | {"status": "rejected: body unavailable"}, None
        # check 2 -- publication date, publisher metadata before htmldate
        pub, pub_src = published_date(html)
        rec["date_source"] = pub_src
        if pub and pub > cutoff.date().isoformat():
            return rec | {"tier": tier, "claimed_published": pub,
                          "status": "rejected: published date after cutoff"}, None
        text = trafilatura.extract(html, include_comments=False, include_tables=True) or ""
        if len(text) < 400:
            return rec | {"tier": tier,
                          "status": f"rejected: only {len(text)} chars extracted"}, None
        # check 3 -- post-cutoff tells in the body.
        # A tell in a tier-3 body is disqualifying: those bytes are today's, so a
        # results phrase may well be leakage. The same tell in a TIER-2 body
        # cannot be -- the archive proves the bytes predate the fence, so the
        # phrase is forward-looking ("expect post-earnings IV crush" in a
        # preview) and the document stands. Quarantined rather than deleted, so
        # the false-rejection rate is measurable instead of invisible.
        tells = scan_tells(text)
        if tells and tier == 3:
            return rec | {"tier": tier, "claimed_published": pub, "tells": tells[:4],
                          "status": "quarantined: tells in unarchived body"}, None
        host = urllib.parse.urlparse(target).netloc.replace("www.", "")
        stamp = (c.get("published_utc") or pub or "unknown")[:10].replace("-", "")
        fname = f"{stamp}_{host.split('.')[0]}_{abs(hash(c['url'])) % 10**8}.txt"
        head = [
            f"SOURCE: {target}",
            f"PROVIDER-URL: {c['url']}",
            f"HOST: {host}",
            f"TIER: {tier} ({note})",
            f"PROVIDER: {c['provider']}  PROVIDER-PUBLISHED: {c.get('published_utc')}",
            f"CLAIMED-PUBLISHED: {pub or 'unknown'} (via {pub_src})",
            f"FENCE: verified before {fence_iso}",
        ]
        if tier == 3:
            head.append("WARNING: tier 3 - live body, content may have "
                        "changed since publication")
        head += ["-" * 72, "", ""]
        header = chr(10).join(head)
        return (rec | {"tier": tier, "claimed_published": pub, "note": note,
                       "file": f"news/{fname}", "chars": len(text),
                       "tells_in_body": tells[:4], "status": "ok"},
                (fname, header + text))

    manifest, writable = [], []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for rec, payload in pool.map(_process, candidates):
            manifest.append(rec)
            if payload:
                writable.append((rec, payload))

    # newest first, so a max_docs cap keeps the material closest to the print
    writable.sort(key=lambda x: x[0].get("provider_published_utc") or "", reverse=True)
    for rec, (fname, body) in writable[:max_docs]:
        (nd / fname).write_text(body, encoding="utf-8")
    for rec, _ in writable[max_docs:]:
        rec["status"] = "dropped: over max_docs"
        rec.pop("file", None)

    t2 = sum(1 for m in manifest if m.get("status") == "ok" and m.get("tier") == 2)
    t3 = sum(1 for m in manifest if m.get("status") == "ok" and m.get("tier") == 3)
    wb_failed = sum(1 for m in manifest
                    if str(m.get("wayback_status", "")).startswith("lookup_failed"))
    # every file on disk must be accounted for in the manifest
    on_disk = {f"news/{f.name}" for f in (outdir / "news").glob("*.txt")}
    listed = {m["file"] for m in manifest if m.get("file")}
    orphans = sorted(on_disk - listed)
    (outdir / "news_manifest.json").write_text(json.dumps(
        {"ticker": ticker, "company": company, "cutoff": cutoff_iso,
         "window_days": window_days, "from": dfrom, "to": dto,
         "fence_utc": fence_iso, "margin_hours": margin_hours,
         "provider_clock_note": "finnhub timestamps corrected ET->UTC; see et_wallclock_to_utc",
         "providers": prov_log, "candidates": len(candidates),
         "kept_tier2": t2, "kept_tier3": t3,
         "quarantined": sum(1 for m in manifest
                            if str(m.get("status", "")).startswith("quarantined")),
         "tier3_share": round(t3 / max(t2 + t3, 1), 3),
         "wayback_lookups_failed": wb_failed,
         "tier3_share_caveat": ("some tier-3 documents may only be tier 3 because the "
                                "archive lookup failed, not because no snapshot exists"
                                if wb_failed else "all archive lookups succeeded"),
         "fence": "clock-corrected provider timestamp AND published date AND body scan, all before fence",
         "orphan_files": orphans,
         "documents": manifest}, indent=1), encoding="utf-8")
    return t2, t3, len(candidates), prov_log, wb_failed


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--company", default="")
    ap.add_argument("--cutoff", required=True, help="ISO instant of the print")
    ap.add_argument("--out", required=True)
    ap.add_argument("--window-days", type=int, default=14)
    ap.add_argument("--max-docs", type=int, default=40)
    ap.add_argument("--providers", default="", help="comma list; default all configured")
    ap.add_argument("--margin-hours", type=float, default=1.0,
                    help="safety margin subtracted from the cutoff")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    provs = [p.strip() for p in a.providers.split(",") if p.strip()] or None
    t2, t3, n, log, wbf = harvest(a.ticker.upper(), a.company, a.cutoff, a.out,
                                  a.window_days, a.max_docs, provs, a.margin_hours,
                                  a.workers)
    print(f"{a.ticker}: {n} candidates -> {t2} tier-2, {t3} tier-3 "
          f"(tier-3 share {t3 / max(t2 + t3, 1):.0%})")
    if wbf:
        print(f"  NOTE: {wbf} archive lookups FAILED -- that tier-3 share is an upper "
              f"bound, not a measurement")
    for p in log:
        print(f"  {p['provider']:14} returned={p['returned']} error={p['error']}")
