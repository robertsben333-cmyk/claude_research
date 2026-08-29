#!/usr/bin/env python3
"""Layer 1 of the sealed corpus: SEC filings, hard-fenced by filing date.

This is the only layer that is provably clean. Filings are immutable and
timestamped by the SEC, so `filingDate < cutoff` cannot admit post-event
content -- there is no revision to worry about and no search ranking to bias.

8-K item 2.02 keeps the actual numbers and the guidance in EX-99.1, not in the
cover page, so exhibits are followed. Without that the corpus contains the
filing but not the bar the next print will be judged against.

Writes plain text into <event>/filings/ plus a manifest recording form, filing
date, acceptance time and the canonical URL of every document, so the leak
audit can re-verify the fence afterwards.
"""
import argparse, html, json, re, sys
from datetime import date, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import fetch, submissions, ticker_cik_map

KEEP = {"10-Q", "10-K", "8-K", "4", "DEF 14A", "SC 13D", "SC 13D/A",
        "SCHEDULE 13G", "SCHEDULE 13G/A", "424B5", "S-3ASR"}
MAX_BYTES = 900_000
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t\r\f\v]+")
NL = re.compile(r"\n{3,}")
EX = re.compile(r"(?i)ex[-_]?99")


def to_text(raw_html):
    h = re.sub(r"(?is)<(script|style|ix:header)[^>]*>.*?</\1>", " ", raw_html)
    h = re.sub(r"(?i)</(p|div|tr|h[1-6]|li|table)>", "\n", h)
    t = html.unescape(TAG.sub(" ", h)).replace("•", "-").replace("◦", "-")
    t = WS.sub(" ", t)
    return NL.sub("\n\n", "\n".join(l.strip() for l in t.split("\n"))).strip()


def exhibits(cik, acc_nodash):
    """Returns (names, error). A swallowed failure here is indistinguishable from
    'this filing had no exhibits', which would silently drop the earnings release
    itself from the corpus -- so the error is returned and recorded, not hidden."""
    try:
        d = json.loads(fetch(
            f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}/index.json",
            sec=True, timeout=40))
    except Exception as e:
        return [], f"{type(e).__name__}: {str(e)[:120]}"
    return ([it["name"] for it in d["directory"]["item"]
             if EX.search(it["name"]) and it["name"].lower().endswith((".htm", ".html", ".txt"))],
            None)


def _write_doc(cik, acc, doc, di, meta, outdir, cutoff_date, manifest):
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"
    try:
        raw = fetch(url, sec=True, timeout=60)
    except Exception as e:
        manifest.append(meta | {"url": url, "status": f"fetch failed: {type(e).__name__}"})
        return
    txt = to_text(raw)[:MAX_BYTES]
    suffix = "" if di == 0 else f"_ex{di}"
    form = meta["form"].replace("/", "-").replace(" ", "")
    safe = f"{meta['filing_date']}_{form}_{acc[-6:]}{suffix}.txt"
    header = (f"SOURCE: {url}\nFORM: {meta['form']}\nFILED: {meta['filing_date']}\n"
              f"ACCEPTED: {meta['accepted']}\nITEMS: {meta['items']}\n"
              f"FENCE: filed strictly before {cutoff_date}\n{'-' * 72}\n\n")
    (outdir / "filings" / safe).write_text(header + txt, encoding="utf-8")
    manifest.append(meta | {"url": url, "file": f"filings/{safe}",
                            "chars": len(txt), "status": "ok"})


def build(ticker, cik, cutoff_date, outdir, lookback_days=400, max_filings=40):
    outdir = Path(outdir)
    (outdir / "filings").mkdir(parents=True, exist_ok=True)
    floor = (date.fromisoformat(cutoff_date) - timedelta(days=lookback_days)).isoformat()
    r = submissions(cik)["filings"]["recent"]
    rows = []
    for i, form in enumerate(r["form"]):
        fd = r["filingDate"][i]
        if not (floor <= fd < cutoff_date):      # HARD FENCE: strictly before the print
            continue
        if form not in KEEP:
            continue
        rows.append({"form": form, "filing_date": fd,
                     "accepted": r["acceptanceDateTime"][i],
                     "items": r["items"][i], "accession": r["accessionNumber"][i],
                     "primary": r["primaryDocument"][i]})
    rows.sort(key=lambda x: x["filing_date"], reverse=True)
    rows = rows[:max_filings]
    manifest, exhibit_errors = [], []
    for x in rows:
        acc = x["accession"].replace("-", "")
        docs = [x["primary"]]
        if x["form"] == "8-K":
            names, err = exhibits(cik, acc)
            if err:
                exhibit_errors.append({"accession": x["accession"], "filing_date":
                                       x["filing_date"], "error": err})
            docs += [e for e in names if e != x["primary"]]
        for di, doc in enumerate(docs):
            _write_doc(cik, acc, doc, di, x, outdir, cutoff_date, manifest)
    (outdir / "filings_manifest.json").write_text(
        json.dumps({"ticker": ticker, "cik": cik, "cutoff_date": cutoff_date,
                    "lookback_days": lookback_days,
                    "fence": "every document filed strictly before cutoff_date",
                    "exhibit_index_errors": exhibit_errors,
                    "documents": manifest}, indent=1), encoding="utf-8")
    ok = sum(1 for m in manifest if m.get("status") == "ok")
    return ok, len(manifest), len(rows), exhibit_errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--cutoff", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cik")
    ap.add_argument("--lookback", type=int, default=400)
    a = ap.parse_args()
    cik = a.cik or ticker_cik_map().get(a.ticker.upper())
    ok, tot, filings, errs = build(a.ticker.upper(), cik, a.cutoff, a.out, a.lookback)
    print(f"{a.ticker}: {filings} filings -> {ok}/{tot} documents written to {a.out}/filings/")
    if errs:
        print(f"  WARNING: {len(errs)} exhibit index lookups failed - the earnings "
              f"release may be missing from the corpus. Re-run before using this event.")
        for e in errs:
            print(f"    {e['filing_date']} {e['accession']}: {e['error']}")
