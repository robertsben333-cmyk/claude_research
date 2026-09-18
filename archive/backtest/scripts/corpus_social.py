#!/usr/bin/env python3
"""The informal layer: retail and practitioner chatter, hard-fenced by timestamp.

Filings and wire copy are the cheap half of a pre-earnings corpus and the least
interesting -- consensus EPS and guidance language are already on every terminal
on the street. What an AI researcher is supposed to be good at is aggregating the
informal record at a scale no analyst reads. That is this file.

A source qualifies only if every item carries a hard timestamp:

  stocktwits  cashtag-indexed, exact ISO per message, pages backward via &max=<id>
  hn          Algolia `created_at_i` epoch filter, full comment text

Both are keyless. Neither needs text matching against a ticker -- StockTwits is
indexed by cashtag and HN is queried per company -- so the matching problem that
makes a raw archive sweep painful does not arise.

Notes that cost time to learn:

  * StockTwits paging is ~30 messages per request and roughly 1.5 days per 8
    pages for a liquid name, so a 14-day window is ~75 requests. Unauthenticated
    rate limiting is around 200 requests/hour, i.e. 2-3 tickers an hour.
  * HN Algolia MUST run with typoTolerance=false. Left on, it matches "Okay" for
    "Okta" and returns ~1,450 hits of pure noise against 1 real one.
  * Volume before a print is itself a signal, so the raw per-day message counts
    are written alongside the text rather than being collapsed into a summary.
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

UA = {"User-Agent": "Mozilla/5.0 (compatible; claude-research-backtest)"}
ST = "https://api.stocktwits.com/api/2/streams/symbol/{t}.json?limit=30"
HN = "https://hn.algolia.com/api/v1/search_by_date"


def _get(url, timeout=40, tries=3):
    last = None
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
            return json.loads(r.read()), None
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:70]}"
            if "429" in str(e):
                time.sleep(8 * (i + 1))
            else:
                time.sleep(1.5 * (i + 1))
    return None, last


def stocktwits(ticker, fence_iso, window_start_iso, max_pages=90, sleep=1.5):
    """Page backward from now until the window is covered.

    Only messages between window_start and the fence are kept. Everything after
    the fence is discarded rather than never fetched -- paging backward has to
    walk through the post-print flood to reach the pre-print material, and the
    count of what was discarded is itself worth recording.
    """
    url, kept, discarded, pages, err = ST.format(t=ticker), [], 0, 0, None
    while pages < max_pages:
        d, e = _get(url)
        if e:
            err = e
            break
        msgs = d.get("messages") or []
        if not msgs:
            break
        pages += 1
        for m in msgs:
            ts = m.get("created_at")
            if not ts:
                continue
            if ts >= fence_iso:
                discarded += 1
            elif ts >= window_start_iso:
                sent = ((m.get("entities") or {}).get("sentiment") or {}).get("basic")
                kept.append({"created_at": ts, "body": m.get("body", ""),
                             "user": (m.get("user") or {}).get("username"),
                             "followers": (m.get("user") or {}).get("followers"),
                             "sentiment": sent, "id": m.get("id")})
        if msgs[-1].get("created_at", "") < window_start_iso:
            break
        url = ST.format(t=ticker) + f"&max={msgs[-1]['id']}"
        time.sleep(sleep)
    return kept, {"pages": pages, "discarded_after_fence": discarded, "error": err,
                  "window_fully_covered": err is None and pages < max_pages}


def _base_name(company):
    return re.sub(r"(?i),?\s+(inc|corp|corporation|company|co|ltd|plc|holdings|"
                  r"technologies|group|sa|nv|ag)\.?$", "", company or "").strip()


def _hn_relevant(item, ticker, company):
    """Is this item actually about the company?

    Algolia matches substrings and phrases loosely. Querying "Box" for Box, Inc.
    returned 60 items about "out of the box" and "cat box" -- a whole informal
    layer of noise for any generically named company, and worse than no data
    because it looks like coverage. Require the ticker as a standalone token, or
    the full multi-word company name.
    """
    text = f"{item.get('title') or ''} {item.get('text') or ''}"
    if re.search(rf"\b{re.escape(ticker)}\b", text):
        return True
    base = _base_name(company)
    return bool(base and len(base.split()) >= 2 and base.lower() in text.lower())


def hackernews(company, ticker, fence_epoch, start_epoch, hits=60):
    out, errs, dropped = [], [], 0
    base = _base_name(company)
    queries = {f'"{ticker}"'}
    # a one-word company name is a dictionary word far more often than it is a
    # company, so it is not worth a query on its own
    if base and len(base.split()) >= 2:
        queries.add(f'"{base}"')
    for q in queries:
        u = (f"{HN}?query={urllib.parse.quote(q)}&tags=(story,comment)"
             f"&numericFilters=created_at_i>{start_epoch},created_at_i<{fence_epoch}"
             f"&typoTolerance=false&hitsPerPage={hits}")
        d, e = _get(u, timeout=45)
        if e:
            errs.append({"query": q, "error": e})
            continue
        for h in d.get("hits", []):
            item = {"created_at": h.get("created_at"), "query": q,
                    "title": h.get("title"), "url": h.get("url"),
                    "text": h.get("comment_text") or h.get("story_text") or "",
                    "points": h.get("points"),
                    "hn_url": f"https://news.ycombinator.com/item?id={h.get('objectID')}"}
            if _hn_relevant(item, ticker, company):
                out.append(item)
            else:
                dropped += 1
        time.sleep(1)
    seen, uniq = set(), []
    for h in out:
        if h["hn_url"] not in seen:
            seen.add(h["hn_url"]); uniq.append(h)
    return uniq, errs, dropped


def harvest(ticker, company, cutoff_iso, outdir, window_days=14, margin_hours=1.0):
    outdir = Path(outdir); (outdir / "social").mkdir(parents=True, exist_ok=True)
    cutoff = datetime.fromisoformat(cutoff_iso.replace("Z", "+00:00"))
    fence = cutoff - timedelta(hours=margin_hours)
    start = cutoff - timedelta(days=window_days)
    fence_iso = fence.isoformat().replace("+00:00", "Z")
    start_iso = start.isoformat().replace("+00:00", "Z")

    st, st_meta = stocktwits(ticker, fence_iso, start_iso)
    hn, hn_errs, hn_dropped = hackernews(company, ticker, int(fence.timestamp()),
                                         int(start.timestamp()))

    per_day = Counter(m["created_at"][:10] for m in st)
    if st:
        lines = [f"STOCKTWITS  ${ticker}", f"FENCE: strictly before {fence_iso}",
                 f"WINDOW: {start_iso} .. {fence_iso}",
                 f"MESSAGES: {len(st)}   PAGES PULLED: {st_meta['pages']}",
                 f"DISCARDED AS AFTER-FENCE: {st_meta['discarded_after_fence']}",
                 "", "MESSAGES PER DAY (volume into the print is itself a signal):"]
        for d in sorted(per_day):
            lines.append(f"  {d}  {per_day[d]:4}  {'#' * min(per_day[d], 60)}")
        lines += ["", "-" * 72, ""]
        for m in sorted(st, key=lambda x: x["created_at"]):
            tag = f" [{m['sentiment']}]" if m.get("sentiment") else ""
            lines.append(f"{m['created_at']}  @{m['user']}({m['followers']}){tag}\n"
                         f"  {m['body']}\n")
        (outdir / "social" / "stocktwits.txt").write_text("\n".join(lines), encoding="utf-8")

    if hn:
        lines = [f"HACKER NEWS  {company or ticker}", f"FENCE: strictly before {fence_iso}",
                 f"ITEMS: {len(hn)}", "", "-" * 72, ""]
        for h in sorted(hn, key=lambda x: x["created_at"] or ""):
            lines.append(f"{h['created_at']}  {h.get('title') or '(comment)'}  {h['hn_url']}\n"
                         f"  {(h['text'] or '')[:2000]}\n")
        (outdir / "social" / "hackernews.txt").write_text("\n".join(lines), encoding="utf-8")

    manifest = {
        "ticker": ticker, "company": company, "cutoff": cutoff_iso,
        "fence_utc": fence_iso, "window_start_utc": start_iso,
        "margin_hours": margin_hours,
        "fence_basis": "per-item publisher timestamp; no body inference needed",
        "stocktwits": {"messages": len(st), "per_day": dict(sorted(per_day.items())),
                       **st_meta,
                       "file": "social/stocktwits.txt" if st else None},
        "hackernews": {"items": len(hn), "errors": hn_errs,
                       "dropped_as_irrelevant": hn_dropped,
                       "file": "social/hackernews.txt" if hn else None,
                       "note": "typoTolerance=false; thin for non-developer names"},
        "known_gap": ("Reddit absent: PullPush returns HTTP 429 on nearly every request. "
                      "Arctic Shift untested. This is the largest hole in the informal "
                      "layer for consumer and retail-heavy names."),
    }
    (outdir / "social_manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return len(st), len(hn), st_meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--company", default="")
    ap.add_argument("--cutoff", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--window-days", type=int, default=14)
    ap.add_argument("--margin-hours", type=float, default=1.0)
    a = ap.parse_args()
    n_st, n_hn, meta = harvest(a.ticker.upper(), a.company, a.cutoff, a.out,
                               a.window_days, a.margin_hours)
    print(f"{a.ticker}: stocktwits {n_st} messages over {meta['pages']} pages "
          f"({meta['discarded_after_fence']} discarded as after-fence) | hn {n_hn} items")
    if not meta["window_fully_covered"]:
        print(f"  WARNING: window not fully covered (error={meta['error']}) -- the "
              f"informal layer for this name is partial")
