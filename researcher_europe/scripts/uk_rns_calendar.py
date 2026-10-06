#!/usr/bin/env python3
"""A forward UK results calendar built from the RNS record itself.

WHY THIS EXISTS. The vendor calendar stage EU was built on (TradingView's scanner,
`earnings_release_next_date`) was measured on 2026-10-05 against Investegate's RNS
mirror over the ten sessions 2026-09-22 -> 10-05, and it carried only 47 of 135 UK
equity results and trading-update announcements above ~$100k a day. The 2.2% phantom
rate in SUBMARKET.md measured PRECISION; nobody had measured RECALL, and it is ~35%.
Several of its "phantoms" reported days later, i.e. its dates are estimates.

UK issuers tell the market when they will report, in their own announcements:

  * a dated NOTICE ("Notice of Half Year Results ... on the morning of Thursday
    5 November 2026"), usually two to five weeks ahead;
  * a FINANCIAL CALENDAR inside a results or trading-update announcement ("the Group
    will issue a trading update on 22 January 2027").

This module reads both off Investegate, which mirrors every RNS by date back to 1999,
and keeps a rolling table of every forward date it has seen:
`researcher_europe/analysis/uk-rns-calendar.json`. Each entry carries the source
announcement's URL and timestamp, so a date is always a quotation from the issuer and
never an estimate. Nothing here is a cadence prior.

    python3 researcher_europe/scripts/uk_rns_calendar.py update            # crawl new days
    python3 researcher_europe/scripts/uk_rns_calendar.py on 2026-10-08     # rows for a date
    python3 researcher_europe/scripts/uk_rns_calendar.py measure --from 2026-09-22 --to 2026-10-05

`eu_universe.py` merges `on(<date>, known_by=<seal instant>)` into the UK leg, so a row
is used only if the announcement that dated it was public when the baseline is sealed.

WHAT IT DOES NOT CATCH: an issuer that announces nothing ahead (common on AIM for
trading updates), and a date given only in a PDF annual report. Those are the residual
`measure` reports.
"""
import argparse
import html as htmlmod
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eu_archive as A  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "researcher_europe" / "analysis" / "uk-rns-calendar.json"
CACHE = Path(os.environ.get("UK_RNS_CACHE", "/tmp/uk-rns-cache"))
UTC = timezone.utc

ROW = re.compile(
    r'<td>(\d\d \w\w\w \d{4} \d\d:\d\d [AP]M)</td>.*?/company/([A-Z0-9\.]+)">([^<]*)'
    r'</a></div></div>.*?announcement-link" href="([^"]+)">([^<]*)<', re.S)

MONTHS = ("January February March April May June July August September October "
          "November December").split()
MON = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}
MON.update({m[:3].lower(): i + 1 for i, m in enumerate(MONTHS)})
MON["sept"] = 9
_M = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
# "5 November 2026", "5th November", "Thursday, 5 Nov 2026"  |  "November 5, 2026"
DATE_DMY = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?" + _M + r"\.?(?:,?\s+(20\d\d))?\b", re.I)
DATE_MDY = re.compile(r"\b" + _M + r"\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s+(20\d\d))?\b", re.I)

# Headlines whose whole point is a forward date.
NOTICE_HEAD = re.compile(
    r"(notice|notification|date|timing|release date|announcement date|calendar)"
    r".{0,40}(result|trading|statement|update|report|interim|half|final|q[1-4])"
    r"|(result|trading update|trading statement).{0,30}(notice|date|timing)", re.I)
NOT_EVENT_HEAD = re.compile(
    r"\b(AGM|GM|EGM|general meeting|redemption|noteholder|stabili[sz]ation|dividend|"
    r"court hearing|tender|meeting of|scheme)\b", re.I)
# Announcements likely to carry a financial calendar for the NEXT event.
CARRIER_HEAD = re.compile(
    r"result|trading update|trading statement|pre-close|half.year|interim|annual report"
    r"|quarter|q[1-4]\b|operational update|business update|investor presentation", re.I)

# The event a date belongs to, read from the words just before it.
EVENT_CTX = re.compile(
    r"(interim|half[- ]year(ly)?|full[- ]year|final|preliminary|annual|quarter(ly)?|"
    r"q[1-4]|nine[- ]month|first[- ]half|h[12]|year[- ]end)?\s*"
    r"(results?|trading (update|statement)|pre-close (trading )?(update|statement)|"
    r"(business|operational|operating) update|interim management statement|"
    r"financial (report|statements|results))", re.I)
ANNOUNCE_VERB = re.compile(
    r"(announce|publish|release|report|issue|present|expect|intend|schedul|due|will be"
    r"|on|date|calendar)", re.I)
NOT_EVENT_CTX = re.compile(
    r"(AGM|annual general meeting|general meeting|dividend|record date|ex-dividend|"
    r"paid|payment|webinar|capital markets day|investor day|conference|deadline|expir|"
    r"maturity|completion|closing date|long-?stop)", re.I)
CAL_HEADING = re.compile(r"financial (calendar|diary)|key dates|forthcoming (dates|events)"
                         r"|reporting (calendar|dates)|dates for (the )?diary", re.I)
# A date that ENDS a period ("six months ending 30 September") is not the event date.
PERIOD_END = re.compile(
    r"(ended|ending|end(ed)? on|to|as at|as of|since|until|through|period end(ed|ing)?)"
    r"\s*(\w+day,?\s*)?(the\s*)?$", re.I)


def _key(url):
    return CACHE / (re.sub(r"[^A-Za-z0-9]+", "_", url)[-180:] + ".html")


def get(url):
    """Cached GET. Investegate pages for a past day never change, so caching them is
    what makes a 60-day backfill cheap and a daily update a few requests. A body is
    cached only when it carries announcement content, so an error page never sticks."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = _key(url)
    if key.exists():
        return key.read_text(encoding="utf-8", errors="replace")
    body = A.get(url)
    if body and ("announcement-link" in body or "Disclaimer*" in body):
        key.write_text(body, encoding="utf-8")
    return body


def store(url, body):
    CACHE.mkdir(parents=True, exist_ok=True)
    _key(url).write_text(body, encoding="utf-8")


def day_rows(d, today=None):
    """Every RNS on Investegate for `d`: time, EPIC, issuer, url, headline."""
    out, seen = [], set()
    live = today and d >= today          # today's page is still growing: never cache
    # Page through to the highest page any page links to. Stopping at the first empty
    # page is NOT safe: Investegate intermittently answers a page with nothing, and on
    # the first backfill that truncated 2026-10-02 to 50 of 330 rows and 09-10 to zero.
    last, pg = 1, 0
    while pg < min(last, 40):
        pg += 1
        url = A.IG_DAY.format(d=d) + (f"?page={pg}" if pg > 1 else "")
        h, found = "", []
        for attempt in range(4):
            h = A.get(url) if (live or attempt) else get(url)
            found = ROW.findall(h or "")
            if found:
                if not live:
                    store(url, h)
                break
            time.sleep(2 * (attempt + 1))
        last = max([last] + [int(x) for x in re.findall(r"[?&]page=(\d+)", h or "")])
        new = [r for r in found if r[3] not in seen]
        if not found:
            raise RuntimeError(f"Investegate returned no rows for {url} after 4 tries")
        for ts, epic, issuer, link, head in new:
            seen.add(link)
            t = datetime.strptime(ts, "%d %b %Y %I:%M %p")   # Investegate shows London time
            out.append({"ts_london": t.isoformat(timespec="minutes"), "epic": epic.upper(),
                        "issuer": htmlmod.unescape(issuer).strip(), "url": link,
                        "headline": htmlmod.unescape(head).strip()})
    return out


def body_text(url):
    h = get(url) or ""
    h = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", h)
    t = htmlmod.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))
    # Investegate prepends an AI summary; the issuer's own text starts after it.
    i = t.find("Disclaimer*")
    return t[i + 11:] if i >= 0 else t


def _mk(day, mon, year, ref):
    k = mon.lower().rstrip(".")
    m = MON.get(k) or MON.get(k[:3])
    if not m:
        return None
    y = int(year) if year else ref.year
    try:
        d = date(y, m, int(day))
    except ValueError:
        return None
    if not year and d < ref:                 # "5 November" in December means next year
        try:
            d = date(y + 1, m, int(day))
        except ValueError:
            return None
    return d


def forward_dates(text, ref, horizon_days=200):
    """(date, kind, snippet) for every date after `ref` that the text ties to a results
    or trading-update event. A date is kept only when an event phrase sits in the 160
    characters before it and no exclusion word (AGM, dividend, period end...) sits
    between the two -- 'six months ending 30 September' is the period, not the event."""
    found = []
    for rx, order in ((DATE_DMY, "dmy"), (DATE_MDY, "mdy")):
        for m in rx.finditer(text):
            if order == "dmy":
                d = _mk(m.group(1), m.group(2), m.group(3), ref)
            else:
                d = _mk(m.group(2), m.group(1), m.group(3), ref)
            if not d or d <= ref or d > ref + timedelta(days=horizon_days):
                continue
            if d.weekday() >= 5:
                continue
            pre = text[max(0, m.start() - 160):m.start()]
            ev = list(EVENT_CTX.finditer(pre))
            if not ev:
                continue
            last = ev[-1]
            between = pre[last.end():]
            # A "Financial calendar" / "Key dates" table lists "Interim results  24
            # November 2026" with no verb; the table heading is the context instead.
            in_table = CAL_HEADING.search(text[max(0, m.start() - 700):m.start()])
            if (NOT_EVENT_CTX.search(between) or PERIOD_END.search(pre[-30:])
                    or not (in_table or ANNOUNCE_VERB.search(pre[last.start():]))):
                continue
            kind = ("trading_update" if re.search(r"trading|update|statement", last.group(0), re.I)
                    else "results")
            found.append((d, kind, (pre[last.start():] + m.group(0))[-200:].strip()))
    return found


def harvest(rows, d):
    """Forward-dated events from one day's announcements."""
    ref = date.fromisoformat(d)
    picks = []
    for r in rows:
        h = r["headline"]
        notice = bool(NOTICE_HEAD.search(h)) and not NOT_EVENT_HEAD.search(h)
        carrier = bool(CARRIER_HEAD.search(h)) and not NOT_EVENT_HEAD.search(h)
        if notice or carrier:
            picks.append((r, "notice" if notice else "financial_calendar"))

    def one(p):
        r, basis = p
        try:
            fd = forward_dates(body_text(r["url"]), ref)
        except Exception:
            return []
        if basis == "financial_calendar":
            # A results announcement mentions many dates; only the earliest per kind is
            # the next event, later ones belong to the event after it.
            best = {}
            for x in fd:
                if x[1] not in best or x[0] < best[x[1]][0]:
                    best[x[1]] = x
            fd = list(best.values())
        return [{"epic": r["epic"], "issuer": r["issuer"], "event_date": x[0].isoformat(),
                 "kind": x[1], "basis": basis, "quote": x[2], "source_url": r["url"],
                 "source_headline": r["headline"], "source_ts_london": r["ts_london"]}
                for x in fd]

    out = []
    with ThreadPoolExecutor(6) as ex:
        for got in ex.map(one, picks):
            out.extend(got)
    return out


def load():
    if CAL.exists():
        return json.loads(CAL.read_text(encoding="utf-8"))
    return {"crawled_days": [], "events": []}


def save(cal):
    CAL.parent.mkdir(parents=True, exist_ok=True)
    cal["crawled_days"] = sorted(set(cal["crawled_days"]))
    cal["events"].sort(key=lambda e: (e["event_date"], e["epic"], e["source_ts_london"]))
    cal["updated_utc"] = datetime.now(UTC).isoformat(timespec="seconds")
    CAL.write_text(json.dumps(cal, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def update(start=None, end=None, lookback=45):
    """Crawl every weekday from `start` (default: the day after the last crawled day,
    or `lookback` days ago) to `end` (default today). Today is re-crawled each time,
    since its page grows; past days are crawled once."""
    cal = load()
    today = datetime.now(UTC).date()
    end = end or today
    done = set(cal["crawled_days"])
    if start is None:
        start = (max(date.fromisoformat(x) for x in done) if done
                 else today - timedelta(days=lookback))
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    days = [x.isoformat() for x in days if x.weekday() < 5]
    for d in days:
        rows = day_rows(d, today=today.isoformat())
        if not rows:
            continue
        got = harvest(rows, d)
        cal["events"] = [e for e in cal["events"] if not e["source_ts_london"].startswith(d)]
        cal["events"].extend(got)
        if d < today.isoformat():
            cal["crawled_days"].append(d)
        print(f"{d}: {len(rows)} RNS, {len(got)} forward dates", file=sys.stderr)
    save(cal)
    return cal


def on(target, known_by=None, cal=None):
    """Rows dated for `target`, one per EPIC, using only announcements published before
    `known_by` (a naive London datetime; default: no cut). When an issuer gave two
    dates for the same event the LATEST announcement wins -- issuers move dates."""
    cal = cal or load()
    per = {}
    for e in cal["events"]:
        if known_by and datetime.fromisoformat(e["source_ts_london"]) > known_by:
            continue
        per.setdefault(e["epic"], []).append(e)
    out = []
    for epic, evs in per.items():
        # the latest statement about each upcoming event decides its date
        latest = max(evs, key=lambda e: e["source_ts_london"])
        hits = [e for e in evs if e["event_date"] == target]
        if not hits:
            continue
        superseded = (latest["event_date"] != target and latest["kind"] == hits[-1]["kind"]
                      and latest["source_ts_london"] > max(h["source_ts_london"] for h in hits)
                      and abs((date.fromisoformat(latest["event_date"]) -
                               date.fromisoformat(target)).days) < 45)
        if superseded:
            continue
        pick = sorted(hits, key=lambda e: (e["basis"] != "notice", e["source_ts_london"]))[0]
        out.append(pick)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("update")
    u.add_argument("--from", dest="start")
    u.add_argument("--to", dest="end")
    o = sub.add_parser("on")
    o.add_argument("date")
    m = sub.add_parser("measure")
    m.add_argument("--from", dest="start", required=True)
    m.add_argument("--to", dest="end", required=True)
    a = ap.parse_args()
    if a.cmd == "update":
        update(date.fromisoformat(a.start) if a.start else None,
               date.fromisoformat(a.end) if a.end else None)
    elif a.cmd == "on":
        print(json.dumps(on(a.date), indent=1, ensure_ascii=False))
    elif a.cmd == "measure":
        r = measure(date.fromisoformat(a.start), date.fromisoformat(a.end))
        for x in r["per_day"]:
            print(x["date"], {k: v for k, v in x.items() if k not in ("date", "missed")},
                  "missed:", " ".join(x["missed"]))
        print("TOTAL", r["total"])



# --- measurement -------------------------------------------------------------------
def measure(start, end, floor_usd=100_000):
    """Forward recall of the vendor, of this calendar, and of both, against the UK
    equity results and trading updates Investegate actually carried on each day.

    Every date this calendar contributes must have been PUBLIC at the seal: the stage
    fires at 13:30 UTC the business day before, so only announcements stamped before
    14:30 London that day count. Turnover is a rough cut off the vendor's 10-day average
    volume at today's price, so it is for this measurement only."""
    import glob
    import eu_universe as U
    rows, _, _ = U.scan("uk")
    fx = U.fx_rates()
    vend = {r["name"].upper(): r for r in rows}

    def usd(r):
        v = (r.get("average_volume_10d_calc") or 0) * (r.get("close") or 0)
        return U.to_usd(v / 100 if r.get("currency") == "GBX" else v,
                        "GBP", fx) or 0

    not_result = re.compile(r"^(notice|presentation|date of|release date|posting|"
                            r"publication of annual|result of|annual financial report)",
                            re.I)
    cal = load()
    tot = {"truth": 0, "vendor": 0, "rns": 0, "either": 0, "rns_rows": 0, "rns_hit": 0}
    per_day = []
    d = start
    while d <= end:
        if d.weekday() < 5:
            ds = d.isoformat()
            prev = d - timedelta(days=1)
            while prev.weekday() >= 5:
                prev -= timedelta(days=1)
            cut = datetime.combine(prev, datetime.min.time()).replace(hour=14, minute=30)
            try:
                rns = day_rows(ds)
            except Exception:
                rns = None
            if rns:
                said = {r["epic"] for r in rns}
                truth = {r["epic"]: r["headline"] for r in rns
                         if A.looks_like_results(r["headline"])
                         and not not_result.search(r["headline"])
                         and r["epic"] in vend and usd(vend[r["epic"]]) >= floor_usd}
                f = glob.glob(str(ROOT / f"research/2026/*/{ds}/europe/universe.json"))
                vs = set()
                if f:
                    u = json.loads(Path(f[0]).read_text(encoding="utf-8"))
                    vs = {(x.get("tv_symbol") or "").split(":")[-1].upper()
                          for x in u.get("names", []) + u.get("dropped", [])
                          if (x.get("_market") or x.get("submarket")) == "uk"}
                cs = {e["epic"] for e in on(ds, known_by=cut, cal=cal) if e["epic"] in vend}
                cs_big = {e for e in cs if usd(vend[e]) >= floor_usd}
                t = set(truth)
                row = {"date": ds, "truth": len(t), "vendor": len(t & vs),
                       "rns": len(t & cs), "either": len(t & (vs | cs)),
                       "rns_rows": len(cs_big), "rns_hit": len(cs_big & said),
                       "missed": sorted(t - vs - cs)}
                per_day.append(row)
                for k in tot:
                    tot[k] += row[k]
        d += timedelta(days=1)
    return {"per_day": per_day, "total": tot}


if __name__ == "__main__":
    main()
