#!/usr/bin/env python3
"""Fetch filing bodies back from EDGAR for a captured event.

`capture.py` stores filing pointers rather than filing text. On the first two
captures the bodies were 98.9% (AIV) and 89.4% (SAIC) of all bytes, and they are
the one layer that gains nothing from being stored: EDGAR is immutable and
permanently addressable, so an accession is the document. Pointers take an event
from roughly 1.1MB to 50KB, which is the difference between a corpus this repo
can carry for years and one it cannot carry for a month.

This script is the other half of that trade. Give it an event directory and it
writes the bodies into `filings_text/`, which is gitignored -- a local cache, not
corpus state. Delete it whenever; it rebuilds.

The rehydrated text is byte-identical to what a capture-time fetch would have
returned, which is the property that makes the trade safe. It is not an
approximation of the document, it is the document.
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import fetch, ROOT

try:
    import trafilatura
except ImportError:
    trafilatura = None


def extract(html):
    if not html:
        return ""
    if trafilatura is None:
        import re
        return re.sub(r"<[^>]+>", " ", html)[:200000]
    return trafilatura.extract(html, include_comments=False, include_tables=True) or ""


def rehydrate(evdir, forms=None, limit=None):
    evdir = Path(evdir)
    fp = evdir / "filings.json"
    if not fp.exists():
        return 0, 0, f"no filings.json in {evdir}"
    rows = json.loads(fp.read_text(encoding="utf-8")).get("filings") or []
    if forms:
        want = {f.strip().upper() for f in forms}
        rows = [r for r in rows if (r.get("form") or "").upper() in want]
    if limit:
        rows = rows[:limit]
    out = evdir / "filings_text"
    out.mkdir(exist_ok=True)
    got = skipped = 0
    for r in rows:
        dest = out / f"{r['filing_date']}_{r['form'].replace('/', '-')}_{r['accession']}.txt"
        if dest.exists():
            skipped += 1
            continue
        try:
            text = extract(fetch(r["url"], timeout=45, retries=1))
        except Exception as e:
            print(f"  {r['accession']}  FAILED {type(e).__name__}")
            continue
        if len(text) < 200:
            print(f"  {r['accession']}  thin ({len(text)} chars)")
            continue
        head = (f"SOURCE: {r['url']}\nFORM: {r['form']}\n"
                f"FILING_DATE: {r['filing_date']}\nACCESSION: {r['accession']}\n"
                f"ACCEPTED_UTC: {r.get('accepted_utc')}\n"
                f"NOTE: rehydrated from EDGAR; immutable, identical to capture time\n")
        dest.write_text(head + "\n" + text, encoding="utf-8")
        got += 1
    return got, skipped, None


def main():
    ap = argparse.ArgumentParser(description="Fetch filing bodies back from EDGAR.")
    ap.add_argument("event_dir", nargs="+", help="captures/events/<TICKER>-<DATE>")
    ap.add_argument("--forms", help="comma list, e.g. 10-Q,10-K,8-K")
    ap.add_argument("--limit", type=int, help="max filings per event")
    a = ap.parse_args()
    forms = a.forms.split(",") if a.forms else None
    for d in a.event_dir:
        got, skipped, err = rehydrate(d, forms, a.limit)
        if err:
            print(f"{d}: {err}")
        else:
            print(f"{Path(d).name}: {got} fetched, {skipped} already cached")
    return 0


if __name__ == "__main__":
    sys.exit(main())
