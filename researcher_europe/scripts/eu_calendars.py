#!/usr/bin/env python3
"""Issuer-sourced forward calendars for the continental markets, joined to the vendor
universe. Built 2026-10-06 after the vendor's UK recall measured 45 of 126 and a probe
found it skips Q1/Q3 statements for many continental issuers
(`research/analyses/eu-calendar-sources/`).

| source                                   | markets     | join      | session from      |
|------------------------------------------|-------------|-----------|-------------------|
| EQS-News events search                   | de (+AT/CH) | ISIN      | none              |
| Euronext Oslo financial-events           | no          | name      | none              |
| bankier.pl kalendarium (results filter)  | pl          | ISIN, via bankier's company page (cached) | none |
| Inderes calendar (.fi / .se / .dk)       | fi, se, dk  | name      | webcast time      |
| Nasdaq Nordic "Financial Calendar" releases | se, dk, fi | name   | none              |

Every source returns events in one shape -- {market, date, kind, title, source,
source_url, isin|None, issuer|None, symbol|None, time_utc|None} -- and `scheduled()`
joins them to the vendor rows. Each source is wrapped so a failure costs that source
only and is reported, never raised: an unreachable calendar must leave the universe
exactly as the other sources built it, and say so.

Two caches persist across sessions in `researcher_europe/analysis/calendars/`
(publish.sh pushes the folder): the Nasdaq Nordic release table, because the category
feed is a year deep and its bodies are free text worth parsing once, and bankier's
symbol -> ISIN map.

    python3 researcher_europe/scripts/eu_calendars.py 2026-10-22      # what each source dates
"""
import html as htmlmod
import json
import re
import subprocess
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eu_archive as A          # noqa: E402
import uk_rns_calendar as RC    # noqa: E402  (forward_dates: the shared date parser)

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "researcher_europe" / "analysis" / "calendars"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
UTC = timezone.utc


def get(url, timeout=40):
    p = subprocess.run(["curl", "-sSL", "--max-time", str(timeout), "-A", UA,
                        "-w", "\n%{http_code}", url],
                       capture_output=True, text=True, errors="replace",
                       timeout=timeout + 10)
    body, _, code = p.stdout.rpartition("\n")
    return int(code or 0), body


def get_ok(url, tries=3):
    for i in range(tries):
        code, body = get(url)
        if code == 200 and body:
            return body
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"HTTP {code} from {url}")


def text_of(h):
    h = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", h or "")
    return htmlmod.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))).strip()


def _ev(market, d, kind, title, source, url, isin=None, issuer=None, symbol=None,
        time_utc=None):
    return {"market": market, "date": d, "kind": kind, "title": title, "source": source,
            "source_url": url, "isin": isin, "issuer": issuer, "symbol": symbol,
            "time_utc": time_utc}


# --- Germany: EQS-News events search ------------------------------------------------
EQS = ("https://www.eqs-news.com/search-results/{page}?searchtype=events&searchword={w}"
       "&pageLimit=100")
EQS_MON = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov "
                                          "Dec".split())}
# Issuer-entered categories. Kept: anything that is a periodic report or statement.
EQS_REPORT = re.compile(r"quarter|half|annual (financial )?report|interim|statement|"
                        r"results|financial report", re.I)
EQS_NOT = re.compile(r"general meeting|AGM|roadshow|conference|capital markets|dividend|"
                     r"press release", re.I)


def eqs_events(max_pages=12):
    """Every forward EQS event, both search words, de-duplicated. The search ANDs over
    words and needs one, so 'a' and 'e' together cover the list (753 unique of 802 and
    801 on 2026-10-06)."""
    seen, out = set(), []
    for w in ("a", "e"):
        for n in range(1, max_pages + 1):
            t = get_ok(EQS.format(page=f"page/{n}/" if n > 1 else "", w=w))
            blocks = t.split('data-api-type="events"')[1:]
            for blk in blocks:
                isin = re.search(r'data-events-isin="([^"]*)"', blk)
                cat = re.search(r"data-events-category='([^']*)'", blk)
                dd = re.search(r'event__date[^"]*">\s*(\d+)\s*<', blk)
                my = re.search(r'event__month-year">\s*(\w+) (\d+)\s*<', blk)
                comp = re.search(r'event__company">([^<]*)<', blk)
                tit = re.search(r'event__title">([^<]*)<', blk)
                if not (dd and my and my.group(1)[:3] in EQS_MON):
                    continue
                d = date(2000 + int(my.group(2)), EQS_MON[my.group(1)[:3]],
                         int(dd.group(1))).isoformat()
                c = htmlmod.unescape(cat.group(1)) if cat else ""
                ttl = htmlmod.unescape(tit.group(1).strip()) if tit else ""
                if EQS_NOT.search(c) or not EQS_REPORT.search(c + " " + ttl):
                    continue
                key = (d, isin.group(1) if isin else None, ttl)
                if key in seen:
                    continue
                seen.add(key)
                out.append(_ev("de", d, c or ttl, ttl, "eqs_events",
                               "https://www.eqs-news.com/search-results/?searchtype=events",
                               isin=isin.group(1) if isin else None,
                               issuer=htmlmod.unescape(comp.group(1).strip()) if comp else None))
            tot = re.search(r"out of&nbsp;(\d+)", t)
            if not blocks or not tot or n * 100 >= int(tot.group(1)):
                break
    return out


# --- Norway: Euronext Oslo financial events -----------------------------------------
OSLO = ("https://live.euronext.com/en/markets/oslo/equities/financial-events"
        "?field_ofe_event_from_date_value=2&page={page}")
OSLO_REPORT = re.compile(r"quarterly report|half[- ]year|annual report|interim|"
                         r"q[1-4]|results|financial statements", re.I)


def oslo_events(max_pages=40, until=None):
    out, seen = [], set()
    for page in range(max_pages):
        t = get_ok(OSLO.format(page=page))
        i = t.find('<table class="table cols-3">')
        if i < 0:
            break
        rows = re.findall(r"<tr.*?</tr>", t[i:t.find("</table>", i)], re.S)
        new = 0
        for r in rows:
            tds = re.findall(r"<td.*?</td>", r, re.S)
            if len(tds) != 3:
                continue
            dt = re.search(r'datetime="(\d{4}-\d\d-\d\d)', tds[0])
            link = re.search(r'href="([^"]+)"', tds[2])
            issuer, ev = text_of(tds[1]), text_of(tds[2])
            if not dt or (dt.group(1), issuer, ev) in seen:
                continue
            seen.add((dt.group(1), issuer, ev))
            new += 1
            if OSLO_REPORT.search(ev):
                out.append(_ev("no", dt.group(1), ev, ev, "euronext_oslo",
                               link.group(1) if link else OSLO.format(page=page),
                               issuer=issuer))
        if not new or (until and out and max(e["date"] for e in out) > until):
            break
    return out


# --- Poland: bankier.pl kalendarium -------------------------------------------------
BANKIER = ("https://www.bankier.pl/gielda/kalendarium/?eventType=10"
           "&navigation_type=week&navigation_start={ts}")
PL_MON = {"stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5,
          "czerwca": 6, "lipca": 7, "sierpnia": 8, "września": 9, "października": 10,
          "listopada": 11, "grudnia": 12}
BANKIER_MAP = DIR / "bankier-isin.json"


def bankier_events(start, end):
    """Results events ("Wyniki spółek") for every week touching [start, end]. The dates
    are the issuers' own: Polish issuers must publish their periodic-report schedule in
    January."""
    out = []
    monday = start - timedelta(days=start.weekday())
    while monday <= end:
        ts = int(datetime(monday.year, monday.month, monday.day, 12, tzinfo=UTC).timestamp())
        url = BANKIER.format(ts=ts)
        t = get_ok(url)
        for blk in re.split(r'class="m-quotes-calendar-list__date">', t)[1:]:
            m = re.match(r"(\d+) (\S+) (\d{4})", blk)
            if not m or m.group(2).lower() not in PL_MON:
                continue
            d = date(int(m.group(3)), PL_MON[m.group(2).lower()], int(m.group(1))).isoformat()
            for sym, info in re.findall(
                    r'akcje/([^/]+)/kalendarium" class="m-quotes-calendar-list__symbol">'
                    r'[^<]*</a><div class="m-quotes-calendar-list__info">([^<]*)', blk):
                out.append(_ev("pl", d, "results", htmlmod.unescape(info).strip(),
                               "bankier", url, symbol=sym))
        monday += timedelta(days=7)
    return out


def bankier_isins(symbols):
    """bankier symbol -> ISIN, read off each company's own bankier page once and cached."""
    cache = json.loads(BANKIER_MAP.read_text()) if BANKIER_MAP.exists() else {}
    todo = [s for s in set(symbols) if s not in cache]

    def one(s):
        try:
            t = get_ok(f"https://www.bankier.pl/gielda/notowania/akcje/{s}/kalendarium", 2)
        except Exception:
            return s, None
        found = re.findall(r"\b(PL[A-Z0-9]{9}\d)\b", t)
        return s, (max(set(found), key=found.count) if found else None)

    with ThreadPoolExecutor(6) as ex:
        for s, isin in ex.map(one, todo):
            if isin:
                cache[s] = isin
    if todo:
        DIR.mkdir(parents=True, exist_ok=True)
        BANKIER_MAP.write_text(json.dumps(cache, indent=0, sort_keys=True) + "\n")
    return cache


# --- Finland, Sweden, Denmark: Inderes ----------------------------------------------
INDERES = {"fi": "https://www.inderes.fi/en/markets/calendar",
           "se": "https://www.inderes.se/en/markets/calendar",
           "dk": "https://www.inderes.dk/en/markets/calendar"}
INDERES_KEEP = {"INTERIM_REPORT", "BUSINESS_REVIEW", "ANNUAL_REPORT"}


def inderes_events(market):
    """The first 200 events from today on the market's Inderes site. That reaches past
    the next session on every day measured (Sweden's busiest page on 2026-10-06 ran to
    10-22), which is all a seal needs; `horizon` says how far it reached."""
    t = get_ok(INDERES[market])
    j = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S).group(1))
    recs = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("__typename") == "CalendarEvent":
                recs.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(j)
    out = []
    for r in recs:
        if r.get("type") not in INDERES_KEEP:
            continue
        comp = ((r.get("instrument") or {}).get("company") or {})
        live = next((c.get("liveTime") for c in (r.get("content") or [])
                     if isinstance(c, dict) and c.get("liveTime")), None)
        out.append(_ev(market, r["date"], r["type"].lower(),
                       f'{comp.get("name")} {r.get("period") or ""} {r["type"]}',
                       "inderes", INDERES[market].split("/en/")[0] + (comp.get("pageUrl") or ""),
                       issuer=comp.get("name"), time_utc=live))
    horizon = max((r["date"] for r in recs), default=None)
    return out, horizon


# --- Sweden, Denmark, Finland: Nasdaq Nordic "Financial Calendar" releases ----------
NQ_FINCAL = ("https://api.news.eu.nasdaq.com/news/query.action?type=json&showCompany=true"
             "&limit=200&start={start}&cnscategory=Financial%20Calendar")
NQ_TABLE = DIR / "nasdaq-nordic-fincal.json"
NQ_MKT = {lab: m for m, labs in A.NASDAQ_MARKETS.items() for lab in labs}


def nasdaq_fincal_update(max_pages=4):
    """Fold every English 'Financial Calendar' release not yet parsed into the table.
    Unlike the main feed, this category pages back about eight months per 200 rows, so a
    first build reads a year in a few requests; later runs stop at the first page whose
    releases are all already parsed."""
    tab = json.loads(NQ_TABLE.read_text()) if NQ_TABLE.exists() else {"done": [], "events": []}
    done = set(tab["done"])
    todo = []
    for page in range(max_pages):
        items = json.loads(get_ok(NQ_FINCAL.format(start=page * 200)))["results"]["item"]
        if not items:
            break
        fresh = [x for x in items if x.get("messageUrl") not in done]
        todo += [x for x in fresh if "lang=en" in (x.get("messageUrl") or "")
                 and x.get("market") in NQ_MKT]
        done.update(x.get("messageUrl") for x in items if "lang=en" not in (x.get("messageUrl") or ""))
        if not fresh:
            break

    def one(x):
        url = x["messageUrl"]
        try:
            body = text_of(get_ok(url, 2))
        except Exception:
            return url, None
        ref = date.fromisoformat(x["published"][:10])
        return url, [_ev(NQ_MKT[x["market"]], d.isoformat(), kind, q, "nasdaq_fincal", url,
                         issuer=x.get("company")) | {"published": x["published"]}
                     for d, kind, q in RC.forward_dates(body, ref, horizon_days=460)]

    with ThreadPoolExecutor(6) as ex:
        for url, evs in ex.map(one, todo):
            if evs is None:
                continue                        # not marked done: retried next run
            done.add(url)
            tab["events"].extend(evs)
    tab["done"] = sorted(done)
    tab["updated_utc"] = datetime.now(UTC).isoformat(timespec="seconds")
    DIR.mkdir(parents=True, exist_ok=True)
    NQ_TABLE.write_text(json.dumps(tab, indent=1, ensure_ascii=False) + "\n")
    return tab


def nasdaq_fincal_on(target, tab):
    """Events dated `target`, dropping any the SAME issuer has since re-dated: a later
    release about the same kind of report within 45 days of it supersedes it."""
    per = {}
    for e in tab["events"]:
        per.setdefault(A.norm(e["issuer"]), []).append(e)
    out = []
    for evs in per.values():
        for e in [x for x in evs if x["date"] == target]:
            later = [x for x in evs if x["published"] > e["published"]
                     and x["kind"] == e["kind"] and x["date"] != target
                     and abs((date.fromisoformat(x["date"]) - date.fromisoformat(target)).days) < 45]
            if not later:
                out.append(e)
    return out


# --- the join ------------------------------------------------------------------------
# eu_archive.norm strips the legal forms the registers use; the calendars add the Nordic
# and share-class ones. Measured 2026-10-22: without these, Nokia ("Nokia" against the
# vendor's "Nokia Oyj"), Gränges and Lindex did not join.
EXTRA_FORMS = re.compile(r"\b(OYJ|ABP|AB|PUBL|ASA|AS|A S|AKTIESELSKAB|CORPORATION|CORP|"
                         r"SER|SERIES|CLASS|SHS|SHARES|[AB])\b")


def key(name):
    # accents off first: norm() turns "Gränges" into "GR NGES" against "Granges AB"
    plain = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", EXTRA_FORMS.sub(" ", A.norm(plain))).strip()


def _turnover(r):
    return (r.get("average_volume_10d_calc") or 0) * (r.get("close") or 0)

def collect(market, target):
    """(events dated `target` for `market`, per-source status)."""
    t = date.fromisoformat(target)
    jobs = {"de": [("eqs_events", lambda: eqs_events())],
            "no": [("euronext_oslo", lambda: oslo_events(until=target))],
            "pl": [("bankier", lambda: bankier_events(t, t))],
            "fi": [("inderes", lambda: inderes_events("fi")),
                   ("nasdaq_fincal", lambda: nasdaq_fincal_on(target, nasdaq_fincal_update()))],
            "se": [("inderes", lambda: inderes_events("se")),
                   ("nasdaq_fincal", lambda: nasdaq_fincal_on(target, nasdaq_fincal_update()))],
            "dk": [("inderes", lambda: inderes_events("dk")),
                   ("nasdaq_fincal", lambda: nasdaq_fincal_on(target, nasdaq_fincal_update()))],
            }.get(market, [])
    events, status = [], {}
    for name, fn in jobs:
        try:
            got = fn()
            horizon = None
            if isinstance(got, tuple):
                got, horizon = got
            got = [e for e in got if e["date"] == target and e["market"] == market]
            events += got
            status[name] = {"state": "read", "dated_for_target": len(got)}
            if horizon:
                status[name]["reaches_to"] = horizon
                if horizon <= target:
                    # the page ended ON or before the target, so the target day itself
                    # may be cut off part-way: a busy Swedish day fills 200 rows
                    status[name]["state"] = "read_short"
        except Exception as exc:
            status[name] = {"state": "unavailable", "error": str(exc)[:300]}
    return events, status


def match(market, rows, events):
    """[(event, vendor_row)] for every event that joins a vendor-universe row. ISIN where
    the source carries one (EQS; bankier via its company page), else the issuer name
    under eu_archive.same_issuer (word-order-insensitive, legal forms off)."""
    by_isin = {r.get("isin"): r for r in rows if r.get("isin")}
    names = [(key(r.get("description")), r) for r in rows]
    if market == "pl":
        m = bankier_isins([e["symbol"] for e in events if e.get("symbol")])
        for e in events:
            e["isin"] = e.get("isin") or m.get(e.get("symbol"))
    out = []
    for e in events:
        r = by_isin.get(e.get("isin")) if e.get("isin") else None
        if r is None and e.get("issuer"):
            k = key(e["issuer"])
            # exact first: same_issuer() is lenient by design (it was built for kills
            # that must not miss), and "NOKIA" also matches "NOKIAN RENKAAT"
            hits = [r2 for n, r2 in names if n and n == k] or \
                   [r2 for n, r2 in names if n and len(k) >= 3 and A.same_issuer(k, n)]
            # Several hits that are ONE issuer's share classes (Sagax A/B/D) resolve to
            # the most traded line; hits that are different issuers stay unjoined.
            if len({n for n, r2 in names if r2 in hits}) == 1 and hits:
                r = max(hits, key=_turnover)
            else:
                r = None
        if r is not None:
            out.append((e, r))
    return out


if __name__ == "__main__":
    tgt = sys.argv[1]
    for mk in ("de", "no", "pl", "fi", "se", "dk"):
        evs, st = collect(mk, tgt)
        print(mk, st, [(e["issuer"] or e["symbol"], e["title"][:40]) for e in evs][:12])
