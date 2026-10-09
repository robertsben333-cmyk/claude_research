#!/usr/bin/env python3
"""Market primitives for stage IPO: the US IPO calendar, deal pages, the event rules.

Every other stage here hunts an earnings print or a fall. This one hunts two dated
events in the life of a new listing, on NYSE, NYSE American and Nasdaq alike:

  debut      the first session a newly priced IPO trades. Window: the FIRST TRADE (the
             opening cross, Yahoo's day-1 open) to that same session's close. The offer
             price is context, never the anchor: nobody using this repo gets an
             allocation, so the pop from offer to open is measured and ranks nothing.
  lockup     the first session on which the pre-IPO holders' lock-up has expired.
             Window: that session's open to its close, the same intraday shape.

WHERE THE DATA COMES FROM, measured 2026-10-09 from this container
-------------------------------------------------------------------
- `api.nasdaq.com/api/ipo/calendar?date=YYYY-MM` (browser User-Agent): one month of
  priced, upcoming, filed and withdrawn deals, ALL US exchanges, not only Nasdaq. Over
  2025-10..2026-10 it listed 371 priced rows: 274 on Nasdaq tiers, 97 on NYSE and NYSE
  American. `pricedDate` is the FIRST TRADING DAY on 5 of 6 deals checked against Yahoo;
  the sixth (ACCV, priced 9/30, first bar 10/06) is why `first_bar_date` is always read
  from the tape and never assumed.
- `api.nasdaq.com/api/ipo/overview/?dealId=...`: one deal. Carries
  `LockupPeriodNumberofDays`, `LockupPeriodExpirationDate`, `QuietPeriodExpirationDate`,
  `SharesOutstanding`, `ShareholderSharesOffered` (secondary), `SECCIK`, the price, the
  shares offered and the over-allotment. That is what makes the lock-up event cheap to
  date. It does NOT carry early-release provisions (staged unlocks tied to an earnings
  release or a price trigger), so the nominal date can be wrong by weeks: the hunter
  checks the prospectus, and a baseline says `early_release_checked: false` until it has.
- EDGAR (`efts.sec.gov` full-text search, `data.sec.gov/submissions`) for the 424B4
  final prospectus and any 8-K waiving or amending a lock-up.

THE LOCK-UP DATE RULE
---------------------
Nasdaq's expiration date is the LAST restricted day (ACCV: priced 2026-09-30, 180 days,
expires 2027-03-29 = 09-30 + 180). The event session is therefore the first NYSE trading
day STRICTLY AFTER it. The resolver also measures the expiration-date session itself, so
the other convention can be checked rather than argued.

SPACS ARE NOT IPOS FOR THIS STAGE. A blank-check unit priced at $10.00 has no operating
business to be mispriced and trades at trust value. 186 of the 371 priced rows were one.
"""
import json
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "researcher_reversal" / "scripts"))
from get_earnings import is_trading_day, next_trading_day          # noqa: E402
import rev_market as RM                                            # noqa: E402

CACHE = REPO / "researcher_ipo" / "analysis" / "cache"
NASDAQ_UA = {"User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/124 Safari/537.36"),
             "Accept": "application/json", "Referer": "https://www.nasdaq.com/"}
CAL = "https://api.nasdaq.com/api/ipo/calendar?date={ym}"
OVERVIEW = "https://api.nasdaq.com/api/ipo/overview/?dealId={d}"

SPAC_NAME = re.compile(r"\b(acquisition|merger)\b|\bspac\b|blank check", re.I)
EVENT_TYPES = ("debut", "lockup")


def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml"))
    return c.get("ipo_hunt") or {}


# ------------------------------------------------------------------ parsing
def money(s):
    if s in (None, "", "--"):
        return None
    try:
        return float(re.sub(r"[$,\s]", "", str(s)))
    except ValueError:
        return None


def mdy(s):
    """'9/30/2026' or '09/30/2026' -> date. None for anything else."""
    if not s:
        return None
    try:
        return datetime.strptime(str(s).strip(), "%m/%d/%Y").date()
    except ValueError:
        return None


def price_range(s):
    """'15.00-17.00' -> (15.0, 17.0); '18.00' -> (18.0, 18.0)."""
    if not s:
        return None, None
    xs = [money(x) for x in str(s).split("-")]
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None
    return min(xs), max(xs)


def is_spac(row):
    name = row.get("companyName") or row.get("company") or ""
    tick = (row.get("proposedTickerSymbol") or row.get("ticker") or "").upper()
    lo, hi = price_range(row.get("proposedSharePrice"))
    unit = tick.endswith("U") and lo == 10.0
    return bool(SPAC_NAME.search(name)) or unit


# ------------------------------------------------------------------ fetching
def _read_cache(p, max_age_h):
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(d["fetched_utc"])).total_seconds() / 3600
    return d if max_age_h is None or age <= max_age_h else None


def _write_cache(p, payload):
    p.parent.mkdir(parents=True, exist_ok=True)
    doc = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "data": payload}
    p.write_text(json.dumps(doc, separators=(",", ":"), sort_keys=True) + "\n")
    return doc


def calendar_month(ym, refresh=False):
    """{'priced': [...], 'upcoming': [...], 'filed': [...], 'withdrawn': [...]} for YYYY-MM.

    A month that ended more than 10 days ago is cached for good; the current and the
    last month are refetched after six hours, because deals move from upcoming to priced.
    """
    p = CACHE / "calendar" / f"{ym}.json"
    y, m = map(int, ym.split("-"))
    closed = date(y, m, 28) + timedelta(days=14) < date.today()
    if not refresh:
        c = _read_cache(p, None if closed else 6)
        if c:
            return c["data"]
    raw = json.loads(RM.get(CAL.format(ym=ym), headers=NASDAQ_UA, tries=4))
    d = raw.get("data") or {}
    out = {}
    for k in ("priced", "upcoming", "filed", "withdrawn"):
        v = d.get(k) or {}
        rows = v.get("rows") or (v.get("upcomingTable") or {}).get("rows") or []
        out[k] = rows
    _write_cache(p, out)
    return out


def overview(deal_id, max_age_h=24 * 7, refresh=False):
    """The flattened poOverview of one deal: {'LockupPeriodExpirationDate': '03/29/2027', ...}."""
    p = CACHE / "deals" / f"{deal_id}.json"
    if not refresh:
        c = _read_cache(p, max_age_h)
        if c:
            return c["data"]
    try:
        raw = json.loads(RM.get(OVERVIEW.format(d=deal_id), headers=NASDAQ_UA, tries=3))
    except Exception as e:                                          # noqa: BLE001
        return {"_error": str(e)[:200]}
    po = ((raw.get("data") or {}).get("poOverview")) or {}
    flat = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in po.items()}
    info = (raw.get("data") or {}).get("companyInformation") or {}
    flat["_description"] = (info.get("companyDescription") or "")[:1500]
    _write_cache(p, flat)
    time.sleep(0.25)
    return flat


def months_back(n, today=None):
    t = today or date.today()
    y, m = t.year, t.month
    out = []
    for _ in range(n):
        out.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return out[::-1]


def deal_row(r, status):
    """One calendar row in this stage's own words."""
    lo, hi = price_range(r.get("proposedSharePrice"))
    return {
        "deal_id": r.get("dealID"),
        "ticker": (r.get("proposedTickerSymbol") or "").strip().upper() or None,
        "company": (r.get("companyName") or "").strip(),
        "exchange": r.get("proposedExchange"),
        "status": status,
        "price_low": lo, "price_high": hi,
        "shares_offered": money(r.get("sharesOffered")),
        "deal_usd": money(r.get("dollarValueOfSharesOffered")),
        "priced_date": (mdy(r.get("pricedDate")) or mdy(r.get("expectedPriceDate")) or None),
        "spac": is_spac(r),
    }


def priced_deals(months):
    """Every PRICED deal in the given months, de-duplicated on dealID."""
    seen, out = set(), []
    for ym in months:
        for r in calendar_month(ym).get("priced") or []:
            if r.get("dealID") in seen:
                continue
            seen.add(r.get("dealID"))
            d = deal_row(r, "priced")
            if d["priced_date"]:
                out.append(d)
    return out


# ------------------------------------------------------------------ the lock-up rule
def lockup_terms(ov, priced):
    """(expiration_date, days, basis) from a deal overview, or an assumed 180 days."""
    days = None
    try:
        days = int(float(str(ov.get("LockupPeriodNumberofDays") or "").replace(",", "")))
    except ValueError:
        pass
    exp = mdy(ov.get("LockupPeriodExpirationDate"))
    if exp:
        return exp, days, "nasdaq_overview_date"
    if days and priced:
        return priced + timedelta(days=days), days, "nasdaq_overview_days"
    if priced:
        return priced + timedelta(days=180), 180, "assumed_180"
    return None, None, "unknown"


def lockup_event_day(expiration):
    """First NYSE session strictly after the last restricted day."""
    return next_trading_day(expiration)


def prev_trading_day(d):
    p = d - timedelta(days=1)
    while not is_trading_day(p):
        p -= timedelta(days=1)
    return p


# ------------------------------------------------------------------ the tape
def bars(ticker, rg="2y"):
    return RM.bars(ticker, rg=rg)


def bar_on(bs, day):
    s = day.isoformat() if isinstance(day, date) else day
    return next((b for b in bs if b["date"] == s), None)


def bars_before(bs, day):
    s = day.isoformat() if isinstance(day, date) else day
    return [b for b in bs if b["date"] < s]


def pct(a, b):
    return None if a in (None, 0) or b is None else round((b / a - 1) * 100, 3)


def benchmark_window(day, kind="open_close", sym="IWM", _memo={}):
    """The small-cap benchmark's move over the same window: open->close of `day`, or
    close(prev)->close(day). IWM because nearly every name here is a small or mid cap."""
    if sym not in _memo:
        _memo[sym] = RM.bars(sym, rg="5y")
    b = bar_on(_memo[sym], day)
    if not b:
        return None
    if kind == "open_close":
        return pct(b["open"], b["close"])
    prev = bars_before(_memo[sym], day)
    return pct(prev[-1]["close"], b["close"]) if prev else None
