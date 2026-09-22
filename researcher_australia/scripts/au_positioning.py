#!/usr/bin/env python3
"""Disclosed short positioning per ASX name, from ASIC's own daily file.

THIS IS THE BEST POSITIONING SERIES IN THE REPO, AND IT IS WHY THIS MARKET WAS BUILT
------------------------------------------------------------------------------------
Every other register this repo uses is a DISCLOSURE register with a threshold. The FCA,
the Bundesanzeiger, the AMF and JPX all publish positions at or above 0.5% of shares
outstanding, one row per holder. Below the line a name reads 0.0 whether it is at 0.49%
or at nothing, which is why `edge_score` pays a truncated zero 0.15 where a real
disclosure earns 0.45.

ASIC does not work that way. Under the Corporations Act short sellers report their
positions to ASIC daily, and ASIC publishes the AGGREGATE for every product: shares
short, shares on issue, and the percentage. Measured on the 2026-09-16 file:

    755 products, minimum 0.000000%, median 0.309%, p90 4.57%, maximum 17.30%
    430 of 755 rows are BELOW 0.5%

So more than half the register is made of rows every other market in this repo would
have truncated to zero. Three consequences, and all three belong in any note that
quotes an Australian lean:

  1. The level is a real number, not a floor. A name at 0.3% is distinguishable from
     a name at nothing, which is the distinction `anchor_covered` exists to paper over
     everywhere else.
  2. The change is measurable without a disclosure event. The European and Japanese
     changes move when a holder crosses a threshold; this one moves when the position
     moves.
  3. It is BACKTESTABLE. ASIC's index carries 4,113 dated files back to 2010-06-16,
     against JPX's rolling ~30-day window. Nothing in this repo has yet tested a
     positioning anchor against outcomes on a long history. This is the series that
     can carry that test.

THE FILE IS PUBLISHED LATE, AND THE LAG IS CARRIED RATHER THAN HIDDEN
---------------------------------------------------------------------
ASIC publishes roughly four business days in arrears: on 2026-09-22 the newest file was
2026-09-16. So the register a baseline seals is never today's, and `lag_sessions` says
how stale it is. A hunter reading "shorts are building" needs to know the observation
is four sessions old, because on a name that has already run, four sessions is the whole
move. Nothing downstream may treat the lag as zero.

ABSENCE, AND WHAT IT MEANS HERE
--------------------------------
An absent product has no reported short position at all. Because the register is not
truncated, that is a stronger statement than the same absence in London or Tokyo: it is
a measured zero rather than "below the line". It is still not a guarantee -- a product
whose reporting brokers filed nothing that day is also absent -- so `covered` records
that the file was read, and a failed download is never a register of zeros.

THE SIGN OF THE EFFECT IS A PRIOR AND IS NOT MEASURED HERE
-----------------------------------------------------------
Nothing in this repo has measured what a crowded Australian short does into a print.
The weights in `au_priced_in.lean_components()` are the Japanese priors carried over,
and `au_resolve.py` ranks every component separately so measurement can replace them.
Do not defend the weights. Replace them.
"""
import argparse
import csv
import io
import json
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "researcher_australia" / "analysis" / "short-positions-cache.json"
INDEX = "https://download.asic.gov.au/short-selling/short-selling-data.json"
DAILY = ("https://download.asic.gov.au/short-selling/"
         "RR{day}-{version}-SSDailyAggShortPos.csv")
PAGE = ("https://www.asic.gov.au/regulatory-resources/markets/short-selling/"
        "short-position-reports-table/")

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from au_market import fetch, trading_days                      # noqa: E402


def available_files(refresh=False):
    """[(YYYYMMDD, version)] newest first, from ASIC's own index."""
    try:
        rows = json.loads(fetch(INDEX, timeout=30).decode("utf-8", "replace"))
    except Exception:
        return []
    out = [(str(r["date"]), str(r.get("version") or "001")) for r in rows
           if str(r.get("date", "")).isdigit()]
    return sorted(set(out), reverse=True)


def parse(blob):
    """One row per ASX product code, from the aggregated daily CSV."""
    txt = blob.decode("utf-8-sig", "replace")
    out = {}
    for r in csv.DictReader(io.StringIO(txt)):
        code = (r.get("Product Code") or "").strip().upper()
        if not code or len(code) > 6:
            continue
        try:
            pct = float(r.get("% of Total Product in Issue "
                              "Reported as Short Positions") or 0.0)
        except ValueError:
            continue
        try:
            shares = int(float(r.get("Reported Short Positions") or 0))
        except ValueError:
            shares = None
        out[code] = {"short_pct": round(pct, 4),
                     "short_shares": shares,
                     "product": (r.get("Product") or "").strip()}
    return out


def _cache_read():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _cache_write(cache):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache), encoding="utf-8")


def load_day(day, version="001", cache=None, refresh=False):
    """One register by YYYYMMDD. Cached, because ASIC's own index is long but a run
    that re-downloads 750KB per name is how stage EU spent twelve minutes before
    sealing a single baseline."""
    cache = _cache_read() if cache is None else cache
    if day in cache and not refresh:
        return cache[day]
    blob = fetch(DAILY.format(day=day, version=version), timeout=60, referer=PAGE)
    if len(blob) < 5000 or b"," not in blob[:200]:
        return None
    rows = parse(blob)
    if not rows:
        return None
    cache[day] = rows
    _cache_write(cache)
    return rows


def load(on_or_before=None, lookback=5, refresh=False):
    """The newest register at or before `on_or_before`, plus one `lookback` register
    days earlier so the CHANGE can be computed.

    Returns (as_of, rows, prev_as_of, prev_rows, lag_sessions). Every one of those can
    be None, and a caller that fills a None with a zero has invented data.
    """
    want = (on_or_before or date.today().isoformat()).replace("-", "")
    files = available_files()
    if not files:
        return None, {}, None, {}, None
    usable = [f for f in files if f[0] <= want]
    if not usable:
        return None, {}, None, {}, None

    cache = _cache_read()
    as_of = rows = None
    for i, (day, ver) in enumerate(usable):
        rows = load_day(day, ver, cache, refresh)
        if rows:
            as_of, idx = day, i
            break
    if not rows:
        return None, {}, None, {}, None

    prev_as_of, prev_rows = None, {}
    for day, ver in usable[idx + lookback:]:
        p = load_day(day, ver, cache, refresh)
        if p:
            prev_as_of, prev_rows = day, p
            break

    # How stale the register is, in ASX sessions, off the tape rather than in calendar
    # days -- a Friday file read on a Tuesday is two sessions old, not four days.
    lag = None
    days = trading_days()
    if days:
        a = date(int(as_of[:4]), int(as_of[4:6]), int(as_of[6:]))
        t = date.fromisoformat(on_or_before) if on_or_before else date.today()
        lag = sum(1 for d in days if a < d <= t)
    return as_of, rows, prev_as_of, prev_rows, lag


def for_code(code, rows, prev_rows, as_of, prev_as_of, lag):
    """One name's positioning. An absent product is a measured zero, not a gap."""
    code = code.upper()
    hit = rows.get(code)
    prev = (prev_rows or {}).get(code)
    now_pct = hit["short_pct"] if hit else (0.0 if rows else None)
    prev_pct = prev["short_pct"] if prev else (0.0 if prev_rows else None)
    change = (round(now_pct - prev_pct, 4)
              if (now_pct is not None and prev_pct is not None) else None)
    return {
        "short_pct": now_pct,
        "short_shares": hit["short_shares"] if hit else (0 if rows else None),
        "short_prev_pct": prev_pct,
        "short_change_pct_pts": change,
        "in_register": bool(hit),
        "covered": bool(rows),
        "as_of": as_of,
        "prev_as_of": prev_as_of,
        "lag_sessions": lag,
        "basis": ("ASIC's aggregated daily short position report. NOT a 0.5% "
                  "disclosure register: every product with a reported position "
                  "appears, and 430 of 755 rows on 2026-09-16 were below 0.5%. An "
                  "absent product therefore has no reported short position at all, "
                  "which is a measured zero rather than a truncation. The file is "
                  "published about four business days in arrears -- see lag_sessions."
                  if hit or rows else
                  "the register could not be read; this is missing data, not a zero"),
        "source": PAGE,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="newest register at or before this date")
    ap.add_argument("--lookback", type=int, default=5,
                    help="register days back for the change (default 5)")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--code", action="append")
    a = ap.parse_args()
    as_of, rows, prev_as_of, prev_rows, lag = load(a.date, a.lookback, a.refresh)
    if not rows:
        raise SystemExit("no ASIC short-position file could be read")
    print(f"register {as_of} ({len(rows)} products), previous {prev_as_of} "
          f"({len(prev_rows)}), lag {lag} sessions")
    if a.code:
        for c in a.code:
            print(f"  {c}: {json.dumps(for_code(c, rows, prev_rows, as_of, prev_as_of, lag))}")
    else:
        top = sorted(rows.items(), key=lambda x: -x[1]["short_pct"])[:10]
        for c, v in top:
            p = (prev_rows.get(c) or {}).get("short_pct")
            ch = f"{v['short_pct'] - p:+.2f}pp" if p is not None else "     -"
            print(f"  {c:<6} {v['product'][:36]:<36} {v['short_pct']:>6.2f}%  {ch}")


if __name__ == "__main__":
    main()
