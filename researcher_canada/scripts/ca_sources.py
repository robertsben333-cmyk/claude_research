#!/usr/bin/env python3
"""What Canada can be read from, measured rather than assumed (2026-09-22).

THE PROBLEM THIS FILE ANSWERS. A first pass over Canada wrote the market off: the
confirmation archive (sedarplus.ca) answers 403 behind Radware, and the short register
(ciro.ca) answers a Cloudflare interstitial. Both were re-tested here with the protocol
the France leg earned -- eight tries with a 2-4s backoff, not a tight loop -- and both
are still 0 of 8. That verdict about those two hosts stands.

It is the wrong conclusion about the market, because neither host is the only way to the
data behind it. TMX Group's own retail portal (money.tmx.com) runs on an UNAUTHENTICATED
GraphQL endpoint, app-money.tmx.com/graphql, which serves, ticker-keyed and
date-queryable: the SEDAR+ filing index with a downloadable PDF per filing, a
consolidated newswire archive (Canada Newswire, PR Newswire, GlobeNewswire, Newsfile)
with timestamps, the short-interest register, Wall Street Horizon's earnings calendar
with a CONFIRMED / UNCONFIRMED flag and the session encoded in the event name, analyst
counts, insider transactions, and TMX's own daily price history. The Montreal Exchange
(m-x.ca) serves the full listed option chain -- strikes, bid, ask, last, open interest,
weeklies -- for 360 underlyings, free, from the exchange.

So Canada is not Spain-and-Poland. On coverage of the earnings universe it is the
BEST-instrumented non-US market in this repo, and on two axes (a confirmed/unconfirmed
calendar flag, and a listed option chain) it is better instrumented than the US stage.

WHAT IS NOT SOLVED, AND MUST BE READ BEFORE ANY OF IT IS BELIEVED:

1. ONE VENDOR. Short interest, filings, news, calendar and tape all arrive through the
   TMX/QuoteMedia stack. Europe's ten markets fail independently; Canada fails all at
   once. There is no second source for the short register at all -- CIRO is the only
   publisher and it is shut.
2. NO HISTORY ON THE SHORT REGISTER. `getCompanyShortInterest` returns one snapshot with
   no date argument, and there is no history field (the schema's own error message lists
   `getRawShortInterestData`, which is the site's top-10 widget, not the register). The
   FCA's per-holder history makes the UK anchor BACKTESTABLE; Canada's cannot be, and a
   change-in-short-interest variable has to be accumulated forward, day by day, or not
   used.
3. THE SHORT-INTEREST DATE IS NOT UNDERSTOOD. Every one of 336 names came back stamped
   BUSINESS_DATE 2026-09-21, a Monday. CIRO publishes the consolidated report twice a
   month, as of the 15th and month-end, so a 09-21 stamp is either a daily refresh of a
   modelled number or a publication date pasted onto the 09-15 snapshot. Those mean
   opposite things for a change variable. Settle it by recording the field daily for two
   weeks before anything reads it; until then use the LEVEL and not the change.
4. THE IMPLIED MOVE IS UNVERIFIED. Every measurement here ran with Toronto shut, so the
   chain's bid and ask columns are zeroes and the straddle had to be priced off `last`,
   which can be days stale. The chain is structurally complete; whether a usable
   earnings implied move comes out of it must be measured once during a live session.
5. TERMS OF USE. money.tmx.com is a retail portal, not a published data product. This is
   read-only research traffic at single-name rates, and it should stay that way.
   m-x.ca refuses at 5 concurrent fetches and answers 8 of 8 serially -- fetch it one at
   a time.
"""
import html
import json
import re
import subprocess
import time
from datetime import date, datetime

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
GQL = "https://app-money.tmx.com/graphql"
MX = "https://www.m-x.ca/en/trading/data"

# Measured 2026-09-22 from this container. `tries` is the France protocol: eight
# attempts with a 2-4s backoff, because a host that answers one request in three looks
# exactly like a host that is down when it is asked four times in a row.
CAPABILITY = {
    "app-money.tmx.com/graphql": {
        "role": "filings index, news archive, short register, calendar, tape",
        "tries": "8/8", "auth": None,
        "serves": ["getCompanyFilings", "getNewsForSymbol", "getNewsForSymbols",
                   "getNewsStoryById", "getCompanyShortInterest", "getWSHEventData",
                   "getCompanyPriceHistory", "getCompanyAnalysts",
                   "getInsiderTransactions", "getCompanyMostRecentTrades"],
    },
    "app.quotemedia.com": {
        "role": "the SEDAR+ filing PDF itself, linked from getCompanyFilings",
        "tries": "8/8", "auth": None, "note": "134 KB PDF retrieved; read it with "
                                              "researcher_europe/scripts/eu_pdftext.py",
    },
    "www.m-x.ca": {
        "role": "listed option chain, 360 underlyings: strike, bid, ask, last, OI, weeklies",
        "tries": "8/8", "auth": None,
        "note": "SERIAL ONLY -- 0 of 26 at 5 concurrent, 8 of 8 one at a time.",
    },
    "scanner.tradingview.com": {
        "role": "forward earnings calendar and turnover, same vendor as stage EU",
        "tries": "8/8", "auth": None,
        "note": "disagrees with Wall Street Horizon on 172 of 278 next-release dates.",
    },
    "www.sedarplus.ca": {
        "role": "the official filing archive", "tries": "0/8", "auth": None,
        "note": "Radware AppWall, hard 403 with a transaction id, no JS challenge. "
                "Not a flaky handshake -- the France retest protocol does not rescue it. "
                "Reached instead through getCompanyFilings + app.quotemedia.com.",
    },
    "www.ciro.ca": {
        "role": "the official short register (CSPR, twice monthly)", "tries": "0/8",
        "auth": None, "note": "Cloudflare interstitial, 8 of 8. Reached instead through "
                              "getCompanyShortInterest -- level only, no history.",
    },
    "www.sedi.ca": {
        "role": "insider filings", "tries": "0/8", "auth": None,
        "note": "same Radware 403 as SEDAR+. Reached instead through "
                "getInsiderTransactions.",
    },
}


# --- transport -------------------------------------------------------------------
def _curl(args, timeout=45):
    """curl, not urllib, for the reason jp_universe.py and eu_universe.py both give:
    this container reaches the internet through a proxy urllib does not pick up, and a
    silent URLError reads as an empty day rather than a broken fetch."""
    p = subprocess.run(["curl", "-sS", "--max-time", str(timeout),
                        "-H", f"User-Agent: {UA}"] + args, capture_output=True)
    return p.stdout


def gql(query, variables=None, timeout=45, retries=3):
    """One GraphQL call. Retries on a transport failure, never on a GraphQL error --
    a bad field name is a bug in this file and retrying it just hides it."""
    body = json.dumps({"query": query, "variables": variables or {}})
    last = None
    for i in range(retries):
        out = _curl(["-X", "POST", "-H", "Content-Type: application/json",
                     "-H", "Origin: https://money.tmx.com",
                     "-H", "Referer: https://money.tmx.com/",
                     "--data-binary", body, GQL], timeout=timeout)
        try:
            d = json.loads(out)
        except Exception as exc:
            last = f"unparseable: {exc}: {out[:200]!r}"
            time.sleep(2 * (i + 1))
            continue
        if "errors" in d:
            raise RuntimeError(f"graphql: {d['errors'][0].get('message')}")
        return d.get("data") or {}
    raise RuntimeError(last or "no response")


# --- the five things a stage would need ------------------------------------------
Q_SHORT = ("query($symbol: String!){getCompanyShortInterest(symbol:$symbol){"
           "BUSINESS_DATE TICKER SHORT_INTEREST SHORTINTERESTPCT DAYSTOCOVER30DAY}}")
Q_FILINGS = ("query($symbol: String!,$fromDate:String,$toDate:String,$limit:Int){"
             "filings:getCompanyFilings(symbol:$symbol,fromDate:$fromDate,"
             "toDate:$toDate,limit:$limit){filingDate description name urlToPdf}}")
Q_NEWS = ("query($symbol:String!,$page:Int!,$limit:Int!,$locale:String!){"
          "news:getNewsForSymbol(symbol:$symbol,page:$page,limit:$limit,locale:$locale)"
          "{headline datetime source newsid summary}}")
Q_NEWS_MANY = ("query($symbols:[String!],$page:Int!,$limit:Int!,$locale:String!){"
               "news:getNewsForSymbols(symbols:$symbols,page:$page,limit:$limit,"
               "locale:$locale){headline datetime source newsid topic}}")
Q_STORY = ("query($newsid:String!){newsArticle:getNewsStoryById(newsid:$newsid){"
           "headline story datetime source}}")
Q_WSH = "query($symbols:[String]){quote:getWSHEventData(symbols:$symbols){data}}"
# getCompanyPriceHistory SILENTLY CAPS AT 25 ROWS whatever `limit` and `start` say --
# measured on AGF.B, where a three-year request returned five weeks. It is the charting
# endpoint that carries the tape: 766 daily rows over the same three years. A truncation
# that returns a valid-looking short series is exactly the failure this repo keeps
# paying for, so the capped endpoint is not used at all.
Q_BARS = ("query($symbol:String!,$fromDate:String,$toDate:String,$freq:String){"
          "getChartDataBySymbol(symbol:$symbol,fromDate:$fromDate,toDate:$toDate,"
          "freq:$freq){dateTime open high low close volume}}")


def short_interest(symbol):
    """The positioning anchor. LEVEL ONLY -- see caveat 3 in the module docstring."""
    return gql(Q_SHORT, {"symbol": symbol}).get("getCompanyShortInterest")


def filings(symbol, from_date, to_date, limit=40):
    """The SEDAR+ index for one issuer between two dates, with a PDF URL per filing.

    This is the half of the confirmation problem the news archive does not solve. On the
    2026-09-22 measurement, 38 of the 39 vendor rows with NO same-day press release had
    an interim-financials or 52-109 certificate filing within three days of the vendor's
    date -- which is a real reporting event with no wire release, and the shape most of
    the Canadian small-cap calendar takes."""
    return gql(Q_FILINGS, {"symbol": symbol, "fromDate": from_date,
                           "toDate": to_date, "limit": limit}).get("filings") or []


def news(symbol, limit=60, page=1, locale="en"):
    """One issuer's consolidated wire feed, newest first, with an ISO timestamp carrying
    the Eastern offset -- so the SESSION is readable off the release itself. Measured
    against the vendor's session flag on 89 confirmed prints: 89 agree, 2 do not."""
    rows = gql(Q_NEWS, {"symbol": symbol, "page": page, "limit": limit,
                        "locale": locale}).get("news") or []
    # The feed carries raw HTML entities ("AGF&#xA0;Management Limited Reports ...").
    # Left in, they break every headline classifier on a word boundary.
    for r in rows:
        for k in ("headline", "summary"):
            if r.get(k):
                r[k] = html.unescape(r[k])
    return rows


def news_pages(symbol, pages=3, limit=100, locale="en"):
    """Several pages of one issuer's feed, oldest-reaching first call last.

    100 items reaches back about six months for a chatty issuer -- AGF publishes monthly
    AUM releases and its last 100 headlines contained ONE results release. A reaction
    history two prints long is not a history, so anything that needs one pages."""
    out, seen = [], set()
    for p in range(1, pages + 1):
        try:
            rows = news(symbol, limit=limit, page=p, locale=locale)
        except Exception:
            break
        if not rows:
            break
        for r in rows:
            k = r.get("newsid")
            if k in seen:
                continue
            seen.add(k)
            out.append(r)
    return out


def news_for(symbols, limit=100, page=1, locale="en"):
    """The whole-day archive Germany's EQS leg never had: one call over a LIST of
    tickers. This is what makes `event_occurred: false` reachable across a universe
    rather than one issuer at a time."""
    return gql(Q_NEWS_MANY, {"symbols": list(symbols), "page": page, "limit": limit,
                             "locale": locale}, timeout=60).get("news") or []


def story(newsid):
    return gql(Q_STORY, {"newsid": str(newsid)}).get("newsArticle")


def wsh_events(symbol):
    """Wall Street Horizon's event list. `event_status` is CON or UNC and `event_name`
    ends in 'Before Mkt' or 'After Mkt', so the calendar carries its own confirmation
    flag AND its own session -- neither of which Nasdaq's US feed has, and the absence
    of the first is what put 33% of equity behind TRT on 2026-09-17."""
    d = gql(Q_WSH, {"symbols": [symbol]}).get("quote") or {}
    ev = d.get("data")
    if not isinstance(ev, list):          # {"error": "No matching companies found"}
        return []
    return [e for e in ev if isinstance(e, dict)]


def earnings_event(symbol, on_or_after=None):
    """The next scheduled earnings announcement, normalised."""
    on_or_after = on_or_after or date.today().isoformat()
    out = []
    for e in wsh_events(symbol):
        if e.get("event_type") != "EAD":
            continue
        m = re.match(r"(\d\d)/(\d\d)/(\d{4})", e.get("event_date") or "")
        if not m:
            continue
        d = f"{m.group(3)}-{m.group(1)}-{m.group(2)}"
        if d < on_or_after:
            continue
        name = e.get("event_name") or ""
        out.append({"date": d, "confirmed": e.get("event_status") == "CON",
                    "status": e.get("event_status"),
                    "session": "amc" if "After Mkt" in name else
                               "bmo" if "Before Mkt" in name else None,
                    "name": name, "isin": e.get("isin")})
    return sorted(out, key=lambda x: x["date"])[:1]


Q_ANALYSTS = ("query($symbol:String!){getCompanyAnalysts(symbol:$symbol){totalAnalysts "
              "priceTarget{lowPriceTarget highPriceTarget priceTarget priceTargetUpside} "
              "consensusAnalysts{consensus buy sell hold}}}")


def analysts(symbol):
    """Analyst count, price target and the buy/sell/hold split.

    The count is the `analyst_band` variable stage EU carries, and it is the one number
    that speaks directly to this repo's thesis about under-read names. There is NO EPS
    consensus anywhere in this API, which is a real gap: the bar a Canadian print is
    judged against has to be sourced by the hunter, and the baseline says so rather than
    leaving a reader to assume it was checked."""
    return gql(Q_ANALYSTS, {"symbol": symbol}).get("getCompanyAnalysts")


def bars(symbol, start, end, freq="day"):
    """TMX's own daily tape, OLDEST ROW FIRST, as {dateTime, open, high, low, close,
    volume}. Preferred over Yahoo deliberately: Yahoo answered 429 to every request
    during the 2026-09-22 build, and its European closes were measured a session stale,
    which is what forced `move_pending` on stage EU. This is the exchange's own tape."""
    return gql(Q_BARS, {"symbol": symbol, "fromDate": start, "toDate": end,
                        "freq": freq}, timeout=60).get("getChartDataBySymbol") or []


# --- Montreal Exchange ------------------------------------------------------------
_MONTH = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"])}


def optionable():
    """The 360 underlyings with listed options, from the exchange's own list."""
    s = _curl([f"{MX}/options-list"], timeout=45).decode("utf-8", "replace")
    out = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S):
        c = [re.sub("<[^>]+>", "", x).strip()
             for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        if len(c) >= 3 and c[1] != "Option Symbol":
            out[c[2]] = c[1]
    return out


def option_chain(symbol):
    """One underlying's whole chain. SERIAL ONLY -- see CAPABILITY.

    Columns are (expiry, call bid/ask/last/chg/OI/vol, strike, put bid/ask/last/chg/
    OI/vol). Outside the Toronto session bid and ask are zeroes, so anything computed
    from this before 09:30 ET is priced off a possibly stale `last`.

    A dotted Toronto ticker (GIB.A, GRT.UN, CHP.UN) is listed at the Montreal Exchange
    under its root, and the wrong symbol returns a full-sized page with no chain in it
    rather than an error -- so the fallback has to key off zero PARSED ROWS, not off the
    response size. Without it a whole class of names reads as "no options" when it has a
    chain, which is the same silent failure the Nordic share classes produced in Europe.
    """
    rows = _parse_chain(_curl([f"{MX}/quotes?symbol={symbol}*"], timeout=60))
    if not rows and "." in symbol:
        root = symbol.split(".")[0]
        rows = _parse_chain(_curl([f"{MX}/quotes?symbol={root}*"], timeout=60))
    return rows


def _parse_chain(raw):
    s = raw.decode("utf-8", "replace")
    if len(s) < 2000:
        return []
    def f(x):
        try:
            return float(x.replace(",", ""))
        except ValueError:
            return None
    rows = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S):
        c = [re.sub("<[^>]+>", "", x).strip()
             for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        if len(c) != 14:
            continue
        m = re.match(r"([A-Z][a-z]+) (\d+),? (\d{4})", c[0])
        if not m:
            continue
        exp = date(int(m.group(3)), _MONTH[m.group(1)], int(m.group(2)))
        rows.append({"expiry": exp.isoformat(), "weekly": "Weekly" in c[0],
                     "call_bid": f(c[1]), "call_ask": f(c[2]), "call_last": f(c[3]),
                     "call_oi": f(c[5]), "strike": f(c[7]),
                     "put_bid": f(c[8]), "put_ask": f(c[9]), "put_last": f(c[10]),
                     "put_oi": f(c[12])})
    return rows


def implied_move_pct(symbol, event_date, spot):
    """The ATM straddle over the first expiry after the print, as a percent of spot.

    UNVERIFIED IN A LIVE SESSION -- caveat 4. It is also NOT a clean earnings implied
    move: the straddle spans the option's whole remaining life (median 15 days past the
    print on the sample measured), so it is an upper bound on the event's share, and
    de-trending it is a piece of work nobody has done here yet."""
    rows = option_chain(symbol)
    if not rows or not spot:
        return None
    later = sorted({r["expiry"] for r in rows if r["expiry"] > event_date})
    if not later:
        return None
    ring = [r for r in rows if r["expiry"] == later[0]]
    atm = min(ring, key=lambda r: abs((r["strike"] or 1e9) - spot))
    def mid(b, a, last):
        return (b + a) / 2 if (b and a) else last
    c = mid(atm["call_bid"], atm["call_ask"], atm["call_last"]) or 0
    p = mid(atm["put_bid"], atm["put_ask"], atm["put_last"]) or 0
    if not (c or p):
        return None
    return {"expiry": later[0], "strike": atm["strike"], "straddle": round(c + p, 4),
            "implied_move_pct": round(100 * (c + p) / spot, 2),
            "atm_open_interest": (atm["call_oi"] or 0) + (atm["put_oi"] or 0),
            "priced_off": "quote" if (atm["call_bid"] and atm["call_ask"]) else "last",
            "days_past_event": (date.fromisoformat(later[0])
                                - date.fromisoformat(event_date)).days}


if __name__ == "__main__":
    sym = "DOL"
    print(f"--- self-test on {sym}, {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print("short interest :", short_interest(sym))
    print("next earnings  :", earnings_event(sym))
    f = filings(sym, "2026-09-01", "2026-09-22", 5)
    print(f"filings        : {len(f)} rows, first {f[0]['filingDate'] if f else None} "
          f"{f[0]['description'] if f else ''}")
    n = news(sym, limit=3)
    print(f"news           : {len(n)} rows, first {n[0]['datetime'] if n else None} "
          f"{n[0]['headline'][:60] if n else ''}")
    b = bars(sym, "2026-09-10", "2026-09-19")
    print(f"bars           : {len(b)} rows, last {b[-1] if b else None}")
    print(f"optionable     : {len(optionable())} underlyings")
