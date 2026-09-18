#!/usr/bin/env python3
"""Tier 1 news retrieval from the Common Crawl monthly index.

The fence is the WARC-Date -- the moment those exact bytes were stored. It is
publisher-independent, survives later edits to the article, and can be re-checked
by anyone afterwards. htmldate's view of the publication date is recorded next to
it as corroboration and never as the fence: htmldate reports the publication date,
not the modified date, which is exactly the failure mode an updated earnings
preview exhibits.

The CDX index is keyed by URL, not by content, so discovery here is: pull a host's
full capture list for the crawl, keep the URLs whose slug names the company, then
range-fetch only those records. No query, no ranking, no top-N -- see FINDINGS.md
section 12 for why that property is the whole point.

For the final run-in to a print the monthly crawl is too stale (it runs a two-week
window); cc_sweep.py over CC-NEWS covers those days.
"""
import argparse, gzip, io, json, re, sys, urllib.parse, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import fetch

UA = {"User-Agent": "claude-research-backtest"}
IDX = "https://index.commoncrawl.org/{coll}-index"
DATA = "https://data.commoncrawl.org/"

# Hosts whose earnings coverage is worth the index pull. Fixed, ticker-agnostic,
# and applied identically to every event -- a per-event host list would be a
# selection decision made with hindsight.
HOSTS = ["fool.com", "benzinga.com", "seekingalpha.com", "investing.com",
         "marketwatch.com", "zacks.com", "tipranks.com", "insidermonkey.com",
         "businesswire.com", "globenewswire.com", "prnewswire.com",
         "stocktitan.net", "simplywall.st", "nasdaq.com"]


def cdx(coll, url_pattern, page=None, timeout=180):
    q = {"url": url_pattern, "output": "json"}
    if page is not None:
        q["page"] = page
    u = IDX.format(coll=coll) + "?" + urllib.parse.urlencode(q)
    try:
        body = fetch(u, timeout=timeout)
    except Exception as e:
        return [], f"{type(e).__name__}: {str(e)[:100]}"
    rows = []
    for line in body.strip().splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows, None


def num_pages(coll, url_pattern):
    u = (IDX.format(coll=coll) + "?"
         + urllib.parse.urlencode({"url": url_pattern, "output": "json",
                                   "showNumPages": "true"}))
    try:
        return json.loads(fetch(u, timeout=120)).get("pages", 1)
    except Exception:
        return 1


def record_text(rec, timeout=180):
    """Range-fetch one WARC record. Returns (warc_date, html) or (None, error)."""
    off, ln = int(rec["offset"]), int(rec["length"])
    req = urllib.request.Request(DATA + rec["filename"],
                                 headers=UA | {"Range": f"bytes={off}-{off + ln - 1}"})
    try:
        raw = urllib.request.urlopen(req, timeout=timeout).read()
        body = gzip.GzipFile(fileobj=io.BytesIO(raw)).read().decode("utf-8", "replace")
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:100]}"
    if "\r\n\r\n" not in body:
        return None, "malformed WARC record"
    warc_hdr, rest = body.split("\r\n\r\n", 1)
    dates = [l.split(": ", 1)[1].strip() for l in warc_hdr.splitlines()
             if l.startswith("WARC-Date:")]
    if not dates:
        return None, "no WARC-Date"
    html = rest.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in rest else rest
    return dates[0], html


def slug_terms(ticker, company):
    """Tokens that identify the company in a URL slug."""
    base = re.sub(r"(?i),?\s+(inc|corp|corporation|company|co|ltd|plc|holdings|"
                  r"technologies|technology|group|sa|nv|ag)\.?$", "", company or "").strip()
    terms = {ticker.lower()}
    if base:
        terms.add(re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-"))
        first = re.sub(r"[^a-z0-9]+", "", base.split()[0].lower())
        if len(first) >= 4:
            terms.add(first)
    return {t for t in terms if len(t) >= 3}


def harvest(ticker, company, cutoff_iso, coll, outdir, hosts=None, max_docs=60,
            max_index_pages=3):
    """cutoff_iso: ISO instant of the print. Only WARC-Dates strictly before it pass."""
    # Deliberately NOT `news/`: corpus_news.py owns that directory. Two
    # harvesters writing to one directory left documents from superseded runs
    # sitting beside current ones with no way to tell them apart.
    outdir = Path(outdir); ad = outdir / "news_archive"
    if ad.exists():
        for old in ad.glob("*.txt"):
            old.unlink()
    ad.mkdir(parents=True, exist_ok=True)
    try:
        import trafilatura
        from htmldate import find_date
    except ImportError:
        sys.exit("pip install trafilatura htmldate")
    terms = slug_terms(ticker, company)
    manifest, seen, index_errors = [], set(), []
    for host in (hosts or HOSTS):
        pattern = f"{host}/*"
        pages = min(num_pages(coll, pattern), max_index_pages)
        cands = []
        for p in range(pages):
            rows, err = cdx(coll, pattern, page=p)
            if err:
                index_errors.append({"host": host, "page": p, "error": err})
                continue
            for r in rows:
                slug = r["url"].lower()
                if r.get("status") == "200" and any(t in slug for t in terms):
                    cands.append(r)
        for r in cands:
            if len(manifest) >= max_docs:
                break
            if r["url"] in seen:
                continue
            seen.add(r["url"])
            warc_date, html = record_text(r)
            if warc_date is None:
                manifest.append({"url": r["url"], "host": host, "tier": 1,
                                 "status": f"fetch failed: {html}"})
                continue
            if warc_date >= cutoff_iso:          # HARD FENCE on stored bytes
                manifest.append({"url": r["url"], "host": host, "tier": 1,
                                 "warc_date": warc_date,
                                 "status": "rejected: captured at or after cutoff"})
                continue
            text = trafilatura.extract(html, include_comments=False,
                                       include_tables=True) or ""
            if len(text) < 400:
                manifest.append({"url": r["url"], "host": host, "tier": 1,
                                 "warc_date": warc_date,
                                 "status": f"rejected: only {len(text)} chars extracted"})
                continue
            try:
                pub = find_date(html, outputformat="%Y-%m-%d", extensive_search=False)
            except Exception:
                pub = None
            name = f"{warc_date[:10].replace('-','')}_{host.split('.')[0]}_{abs(hash(r['url'])) % 10**8}.txt"
            header = (f"SOURCE: {r['url']}\nHOST: {host}\nTIER: 1 (common crawl WARC)\n"
                      f"WARC-DATE: {warc_date}    <- the fence: these bytes existed at this instant\n"
                      f"CLAIMED-PUBLISHED: {pub or 'unknown'}    <- corroboration only\n"
                      f"FENCE: captured strictly before {cutoff_iso}\n{'-' * 72}\n\n")
            (outdir / "news_archive" / name).write_text(header + text, encoding="utf-8")
            manifest.append({"url": r["url"], "host": host, "tier": 1,
                             "warc_date": warc_date, "claimed_published": pub,
                             "file": f"news_archive/{name}", "chars": len(text), "status": "ok"})
    (outdir / "news_archive_manifest.json").write_text(json.dumps(
        {"ticker": ticker, "company": company, "cutoff": cutoff_iso,
         "collection": coll, "hosts": hosts or HOSTS, "slug_terms": sorted(terms),
         "fence": "WARC-Date strictly before cutoff",
         "index_errors": index_errors, "documents": manifest}, indent=1), encoding="utf-8")
    ok = sum(1 for m in manifest if m["status"] == "ok")
    return ok, len(manifest), index_errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--company", default="")
    ap.add_argument("--cutoff", required=True, help="ISO instant of the print, e.g. 2026-08-26T20:00:00Z")
    ap.add_argument("--collection", default="CC-MAIN-2026-34")
    ap.add_argument("--out", required=True)
    ap.add_argument("--hosts", default="")
    ap.add_argument("--max-docs", type=int, default=60)
    ap.add_argument("--max-index-pages", type=int, default=3)
    a = ap.parse_args()
    hosts = [h.strip() for h in a.hosts.split(",") if h.strip()] or None
    ok, tot, errs = harvest(a.ticker.upper(), a.company, a.cutoff, a.collection,
                            a.out, hosts, a.max_docs, a.max_index_pages)
    print(f"{a.ticker}: {ok}/{tot} documents kept -> {a.out}/news/")
    if errs:
        print(f"  WARNING: {len(errs)} index pages failed; coverage is incomplete "
              f"and this event's news layer is thinner than it looks.")
