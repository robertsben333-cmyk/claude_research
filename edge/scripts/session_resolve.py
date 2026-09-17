#!/usr/bin/env python3
"""Buy back `time-not-supplied` calendar rows by checking them against SEC filings.

Nasdaq's calendar carries a `time` per row. `time-pre-market` and `time-after-hours`
are a schedule; `time-not-supplied` is Nasdaq saying it does not know the session. It
is not a claim that the event is fake, but it correlates hard with rows that are a
vendor projection rather than a schedule -- on 2026-08-31 eight of eight of them had no
earnings event at all -- which is why `edge_universe.py` drops them by default.

The cost of that default shows up on a day like 2026-09-17: 22 calendar rows, 20 not
supplied, one name left to hunt. This script buys some of them back without spending a
hunter, from the one free source that settles it -- the company's own filings.

Per ticker, from `data.sec.gov` only:

  already_reported  a results filing (8-K item 2.02, or a 6-K carrying results
                    language) dated on or just before the event date. The print has
                    happened, the row is stale, and a baseline sealed on it is
                    contaminated. This is a drop, and it is certain.
  session           when a filing in the weeks before the event announces the date in
                    words -- "before market open", "after market close" -- read it off
                    and carry the filing URL as evidence.
  prior             days since the last results filing, against the ~91-day quarterly
                    and ~182-day semi-annual cadence. A weak prior is never a drop on
                    its own: `priced_in.py`'s cadence heuristic once killed four
                    company-confirmed reporters.

What survives is not confirmed, only not yet killed. An unresolved session still has
to be settled by the sweep from a company source before the name can be hunted,
because an unknown session is a coin flip on whether the print is even inside the
window: a `bmo` row dated today already printed this morning, and an `amc` row dated
tomorrow prints a full session after the entry.

    python3 edge/scripts/session_resolve.py --universe <RUN>/edge/universe.json
    python3 edge/scripts/session_resolve.py --universe <RUN>/edge/universe.json --apply
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

UA = "claude_research edge/session_resolve (xavier.friesen@socfin.nl)"
TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
ARCHIVE = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}"
NASDAQ_PR = ("https://api.nasdaq.com/api/news/topic/press_release"
             "?q=symbol:{t}|assetclass:stocks&offset=0&limit={n}")
NASDAQ_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# "Alarum to Release Second Quarter 2025 Results on August 28, 2025" -- the shape of a
# date announcement. A company that has issued these before and has issued none for
# this window is the clearest free evidence that the calendar row is a projection.
ANNOUNCE = re.compile(r"\bto (?:report|announce|release|host|hold)\b|"
                      r"\b(?:date|timing) of\b|\bschedul", re.I)
RESULTS_TITLE = re.compile(r"result|earning|financial|quarter|fiscal|fy ?\d|"
                           r"half[- ]year|full[- ]year", re.I)

# A 6-K carries no item codes and its description is usually just "6-K", so whether
# one is a results release has to be read off the document itself. VinFast files 6-Ks
# for vehicle deliveries; the same defect once gave `priced_in.py` a 10-day "cadence".
RESULTS_TEXT = re.compile(
    r"(financial|operating|unaudited|interim|fourth[- ]quarter|first[- ]quarter|"
    r"second[- ]quarter|third[- ]quarter|full[- ]year|fiscal[- ]year)[^.]{0,80}results|"
    r"results (?:of operations )?for the (?:three|six|nine|twelve)|"
    r"reports? (?:its )?(?:unaudited )?(?:financial|fourth|first|second|third|full)",
    re.I)
# A release that reports numbers carries them. One that announces a date does not, and
# GASS's 6-K of 2026-08-28 -- which announced a 2026-09-02 print -- was read as the
# print itself until this guard existed.
FIGURES = re.compile(r"revenue|net (?:income|loss)|per (?:diluted )?share|gross profit|"
                     r"ebitda|total assets|cash and cash equivalents|operating income",
                     re.I)
FUTURE = re.compile(r"\b(?:will|to|expects? to|plans to|is scheduled to) "
                    r"(?:report|announce|release|publish)\b", re.I)
BMO_WORDS = re.compile(r"before (?:the )?(?:u\.s\. )?(?:market|markets|trading)?"
                       r" ?open|pre-?market|prior to (?:the )?(?:market )?open|"
                       r"before the opening bell", re.I)
AMC_WORDS = re.compile(r"after (?:the )?(?:u\.s\. )?(?:market|markets|trading)?"
                       r" ?close|after-?hours|after the closing bell", re.I)
TAG = re.compile(r"<[^>]+>")


# SEC asks for ten requests a second and answers 429 rather than slowing down.
_last_call = [0.0]
MIN_GAP = 0.13


def http(url, as_json=True, tries=5):
    for n in range(tries):
        gap = MIN_GAP - (time.monotonic() - _last_call[0])
        if gap > 0:
            time.sleep(gap)
        _last_call[0] = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "*/*", "Accept-Encoding": "identity"})
            body = urllib.request.urlopen(req, timeout=30).read()
            return json.loads(body) if as_json else body.decode("utf-8", "ignore")
        except Exception as exc:                                     # noqa: BLE001
            if n == tries - 1:
                return {"_error": str(exc)[:120]} if as_json else ""
            time.sleep((2.5 if "429" in str(exc) else 0.8) * (n + 1))


def nasdaq_press(ticker, n=20):
    """Nasdaq's own press-release feed for the ticker. One call, no key."""
    try:
        req = urllib.request.Request(NASDAQ_PR.format(t=ticker.lower(), n=n),
                                     headers={"User-Agent": NASDAQ_UA,
                                              "Accept": "application/json"})
        body = json.loads(urllib.request.urlopen(req, timeout=25).read())
        return ((body.get("data") or {}).get("rows") or [])
    except Exception:                                                # noqa: BLE001
        return []


def press_evidence(ticker, event_dates, window_days=45):
    """Did the company announce a date for this window, and has it ever announced one?"""
    rows = nasdaq_press(ticker)
    if not rows:
        return {"press_feed": "empty"}
    wanted = set()
    for ev in event_dates:
        wanted |= spellings(ev)
    lo = (date.fromisoformat(min(event_dates)) - timedelta(days=window_days))
    ever, for_window, recent = [], [], []
    for r in rows:
        title = r.get("title") or ""
        try:
            when = datetime.strptime(r.get("created", ""), "%b %d, %Y").date()
        except ValueError:
            when = None
        is_ann = bool(ANNOUNCE.search(title) and RESULTS_TITLE.search(title))
        if is_ann:
            ever.append({"date": r.get("created"), "title": title})
        if when and lo <= when <= date.fromisoformat(max(event_dates)):
            recent.append({"date": r.get("created"), "title": title,
                           "url": "https://www.nasdaq.com" + (r.get("url") or "")})
            if is_ann and any(w in title for w in wanted):
                for_window.append(recent[-1])
    return {"press_feed": "ok", "announces_dates": bool(ever),
            "announcement_examples": ever[:2],
            "announced_for_window": for_window,
            "releases_in_window_days": len(recent),
            "latest_release": recent[0] if recent else None}


def ticker_cik_map():
    doc = http(TICKER_MAP)
    if isinstance(doc, dict) and "_error" in doc:
        sys.exit(f"SEC ticker map unreachable: {doc['_error']}")
    return {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in doc.values()}


def doc_text(cik, filing, budget=2):
    """The filing's own words. The press release is an exhibit, not the wrapper."""
    acc = filing["accession"].replace("-", "")
    base = ARCHIVE.format(cik=int(cik), acc=acc)
    index = http(base + "/index.json")
    names = []
    if isinstance(index, dict) and "_error" not in index:
        names = [f["name"] for f in index.get("directory", {}).get("item", [])
                 if f["name"].lower().endswith((".htm", ".html"))]
        names.sort(key=lambda s: (0 if "ex99" in s.lower().replace("-", "") else 1,
                                  len(s)))
    names = names[:budget] or [filing["doc"]]
    chunks = []
    for name in names:
        text = http(f"{base}/{name}", as_json=False)
        if text:
            chunks.append((f"{base}/{name}",
                           re.sub(r"\s+", " ", TAG.sub(" ", text))))
    return chunks


def results_filings(cik, recent, confirm=5):
    """8-K item 2.02 settles itself. A 6-K has to be opened, and only a few are."""
    n = len(recent["form"])
    items = recent.get("items") or [""] * n
    out, opened = [], 0
    for i in range(n):
        form, item = recent["form"][i], items[i] or ""
        if form.startswith("8-K") and "2.02" in item:
            certain = True
        elif form.startswith("6-K"):
            certain = None                       # unknown until the document is read
        else:
            continue
        out.append({"date": recent["filingDate"][i], "form": form, "items": item,
                    "accession": recent["accessionNumber"][i],
                    "doc": recent["primaryDocument"][i], "certain": certain})
    keep = []
    for f in out:
        if f["certain"] is True:
            keep.append(f)
            continue
        if opened >= confirm:
            break                                 # deeper history is not worth the calls
        opened += 1
        hit = None
        for url, text in doc_text(cik, f):
            head = text[:30000]
            if not RESULTS_TEXT.search(head):
                continue
            if len(FIGURES.findall(head)) < 2 and FUTURE.search(head[:4000]):
                continue                          # a date announcement, not the print
            hit = url
            break
        if hit:
            f["certain"] = False
            f["read_from"] = hit
            keep.append(f)
    keep.sort(key=lambda f: f["date"], reverse=True)
    return keep


def spellings(iso):
    d = date.fromisoformat(iso)
    return {iso, f"{d:%B} {d.day}, {d.year}", f"{d:%b} {d.day}, {d.year}",
            f"{d:%B} {d.day}", f"{d.month}/{d.day}/{d.year}"}


def announcement_scan(cik, recent, event_dates, since, budget=4):
    """Read the session off a date-announcement filing, where one exists."""
    wanted = set()
    for ev in event_dates:
        wanted |= spellings(ev)
    looked = 0
    for i in range(len(recent["form"])):
        if looked >= budget:
            break
        if recent["filingDate"][i] < since:
            continue
        if not recent["form"][i].startswith(("8-K", "6-K")):
            continue
        acc = recent["accessionNumber"][i].replace("-", "")
        base = ARCHIVE.format(cik=int(cik), acc=acc)
        index = http(base + "/index.json")
        if not isinstance(index, dict) or "_error" in index:
            continue
        names = [f["name"] for f in index.get("directory", {}).get("item", [])
                 if f["name"].lower().endswith((".htm", ".html"))]
        # the timing sentence lives in the press-release exhibit, not the 8-K body
        names.sort(key=lambda s: (0 if "ex99" in s.lower().replace("-", "") else 1,
                                  len(s)))
        for name in names[:2]:
            looked += 1
            text = http(f"{base}/{name}", as_json=False)
            if not text:
                continue
            flat = re.sub(r"\s+", " ", TAG.sub(" ", text))
            hit = next((ev for ev in event_dates
                        if any(s in flat for s in spellings(ev))), None)
            if not hit:
                continue
            m = BMO_WORDS.search(flat) or AMC_WORDS.search(flat)
            if not m:
                continue
            sess = "bmo" if BMO_WORDS.match(m.group(0)) else "amc"
            lo, hi = max(0, m.start() - 180), m.end() + 140
            return {"session": sess, "event_date": hit, "url": f"{base}/{name}",
                    "quote": flat[lo:hi].strip(),
                    "filed": recent["filingDate"][i]}
    return None


def classify(ticker, cik, event_dates, today, window, recent_days=10,
             stale_days=200):
    # anchored on the event date, not the clock, so a re-run of a past day agrees
    anchor = date.fromisoformat(min(event_dates))
    # A results filing dated on the anchor is the print itself when the anchor's own
    # session is `bmo` -- SAIC, SY and LX all filed on the morning they reported. When
    # the window takes the anchor as `amc`, the same filing is this morning's bmo print
    # and the row is out of the window by a session.
    same_day_is_event = (anchor.isoformat(), "bmo") in window
    first_kill = 1 if same_day_is_event else 0
    if not cik:
        return {"verdict": "no_cik", "why": "not in the SEC ticker map"}
    doc = http(SUBMISSIONS.format(cik=cik))
    if "_error" in doc:
        return {"verdict": "lookup_failed", "why": doc["_error"]}
    recent = doc["filings"]["recent"]
    res = results_filings(cik, recent)
    last = res[0] if res else None
    since_days = (anchor - date.fromisoformat(last["date"])).days if last else None
    out = {"cik": cik, "entity": doc.get("name"),
           "filer": "foreign" if last and last["form"].startswith("6-K") else "domestic",
           "last_results": last["date"] if last else None,
           "last_results_form": last["form"] if last else None,
           "days_since_results": since_days}

    near = [f for f in res
            if first_kill <= (anchor - date.fromisoformat(f["date"])).days <= recent_days]
    if near:
        f = near[0]
        out.update(verdict="already_reported", prior="n/a",
                   why=f"{f['form']}{' item 2.02' if f['certain'] else ''} filed "
                       f"{f['date']}, {(anchor - date.fromisoformat(f['date'])).days}"
                       " days before the event — no quarterly or semi-annual reporter "
                       "prints twice in ten days, so the row is stale",
                   certain=f["certain"],
                   evidence=ARCHIVE.format(cik=int(cik),
                                           acc=f["accession"].replace("-", ""))
                            + "/" + f["doc"])
        return out

    press = press_evidence(ticker, event_dates)
    out["press"] = press
    if press.get("announced_for_window"):
        hit = press["announced_for_window"][0]
        # Nasdaq serves the release body as a JavaScript shell, so the session is only
        # readable when the headline states it. Usually it does not, and settling it is
        # left to the sweep -- which now gets a shortlist with a citable date instead
        # of a calendar row.
        sess = ("bmo" if BMO_WORDS.search(hit["title"]) else
                "amc" if AMC_WORDS.search(hit["title"]) else None)
        out.update(verdict="announced", prior="strong",
                   why="company press release announces a results date in this window"
                       + (f", session in the headline: {sess}" if sess else
                          "; the headline does not state the session"),
                   evidence=hit["url"], quote=hit["title"])
        if sess:
            out["headline_session"] = sess
        return out

    since = (date.fromisoformat(min(event_dates)) - timedelta(days=45)).isoformat()
    ann = announcement_scan(cik, recent, event_dates, since)
    if ann:
        out.update(verdict="session_resolved", session=ann["session"],
                   session_event_date=ann["event_date"], evidence=ann["url"],
                   why=f"filing of {ann['filed']} names the date and the session",
                   quote=ann["quote"][:400])
        return out

    if press.get("announces_dates") and press.get("press_feed") == "ok":
        out.update(verdict="unresolved", prior="contradicted",
                   why="this company announces its results dates by press release and "
                       "has issued none for this window — the calendar row reads as a "
                       "vendor projection",
                   evidence=(press["announcement_examples"] or [{}])[0].get("title"))
        return out

    if since_days is None:
        prior = "none"
        why = "no periodic results filing on record — either a new registrant or not a filer"
    elif since_days > stale_days:
        prior = "weak"
        why = (f"last results {out['last_results']}, {since_days} days ago — well past "
               "a quarterly or semi-annual cadence")
    elif 60 <= since_days <= 130 or 150 <= since_days <= 215:
        prior = "fits"
        why = f"last results {out['last_results']}, {since_days} days ago — fits a cadence"
    else:
        prior = "early"
        why = f"last results {out['last_results']}, only {since_days} days ago"
    out.update(verdict="unresolved", prior=prior, why=why)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True,
                    help="universe.json built WITH --include-unknown")
    ap.add_argument("--apply", action="store_true",
                    help="rewrite the universe: drop what is killed, set what is "
                         "resolved, mark the rest for the sweep to settle")
    ap.add_argument("--announced-only", action="store_true",
                    help="carry only rows with a company press release naming a date "
                         "in the window. On the one labelled set in the repo — the "
                         "twelve rows of 2026-08-31 — that test kept 4 of 4 real "
                         "reporters and none of the 8 phantoms")
    ap.add_argument("--drop-weak", action="store_true",
                    help="also drop rows with no filing cadence behind them. Off by "
                         "default: the sweep kills phantoms for one agent, and a "
                         "cadence heuristic in priced_in.py once killed four "
                         "company-confirmed reporters")
    ap.add_argument("-o", "--out", help="report path (default beside the universe)")
    a = ap.parse_args()

    path = Path(a.universe)
    uni = json.loads(path.read_text(encoding="utf-8"))
    if not uni.get("unknown_session_included"):
        print("warning: this universe was built without --include-unknown, so the "
              "time-not-supplied rows are not in it and there is nothing to resolve",
              file=sys.stderr)
    window = [(w["date"], w["session"]) for w in (uni.get("window") or [])]
    event_dates = sorted({d for d, _ in window}) or [uni["event_date"]]
    today = date.today()

    unknown = [r for r in uni["names"] if r["session"] == "unknown"]
    if not unknown:
        print("no time-not-supplied rows in this universe")
        return

    cikmap = ticker_cik_map()
    report, keep, drop = [], [], []
    for row in unknown:
        v = classify(row["ticker"], cikmap.get((row["ticker"] or "").upper()),
                     event_dates, today, window)
        v["ticker"], v["company"] = row["ticker"], row["company"]
        v["calendar_date"] = row["event_date"]
        if v["verdict"] == "session_resolved":
            v["in_window"] = (v["session_event_date"], v["session"]) in window
        report.append(v)
        time.sleep(0.25)

    for v in report:
        row = next(r for r in uni["names"] if r["ticker"] == v["ticker"])
        if v["verdict"] == "already_reported":
            drop.append(row)
        elif v["verdict"] == "session_resolved" and not v.get("in_window"):
            drop.append(row)
        elif v["verdict"] == "session_resolved":
            row["session"] = v["session"]
            row["event_date"] = v["session_event_date"]
            row["session_source"] = "sec filing: " + v["evidence"]
            keep.append(row)
        elif v["verdict"] == "announced":
            row["session_source"] = "press release: " + v["evidence"]
            row["session_unresolved"] = True
            keep.append(row)
        elif v["verdict"] == "unresolved" and not a.announced_only and not (
                a.drop_weak and v["prior"] in ("none", "weak", "contradicted")):
            row["session_source"] = "unresolved — sweep must settle or drop"
            row["session_unresolved"] = True
            keep.append(row)
        else:
            drop.append(row)

    doc = {"universe": str(path), "event_date": uni["event_date"], "window": window,
           "resolved_utc": datetime.now().astimezone().isoformat(timespec="seconds"),
           "source": "data.sec.gov submissions + EDGAR archives",
           "unknown_rows": len(unknown),
           "killed": len(drop), "carried": len(keep),
           "announced": sum(1 for v in report if v["verdict"] == "announced"),
           "session_resolved": sum(1 for v in report
                                   if v["verdict"] == "session_resolved"),
           "rows": report}
    out = Path(a.out) if a.out else path.with_name("session-resolve.json")
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    for v in sorted(report, key=lambda x: (x["verdict"], x["ticker"])):
        extra = ""
        if v["verdict"] == "session_resolved":
            extra = f" -> {v['session']} {v['session_event_date']}" \
                    f"{'' if v.get('in_window') else ' (outside the window)'}"
        print(f"  {v['ticker']:8s}{v['verdict']:18s}{extra}")
        print(f"           {v.get('why', '')}")
    print(f"\n{len(unknown)} unresolved rows: {len(drop)} killed, {len(keep)} carried "
          f"({doc['session_resolved']} with a session off a filing). wrote {out}")

    if a.apply:
        killed = {r["ticker"] for r in drop}
        uni["names"] = [r for r in uni["names"] if r["ticker"] not in killed]
        uni["count"] = len(uni["names"])
        uni["unknown_session_count"] = sum(1 for r in uni["names"]
                                           if r["session"] == "unknown")
        uni["session_resolve"] = {"report": str(out), "killed": sorted(killed),
                                  "carried": sorted(r["ticker"] for r in keep)}
        path.write_text(json.dumps(uni, indent=1) + "\n", encoding="utf-8")
        print(f"rewrote {path}: {uni['count']} names, "
              f"{uni['unknown_session_count']} still unresolved")
    else:
        print("dry run — pass --apply to rewrite the universe")


if __name__ == "__main__":
    main()
