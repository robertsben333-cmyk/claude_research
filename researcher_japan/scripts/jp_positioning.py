#!/usr/bin/env python3
"""Disclosed short positioning per Japanese name, from JPX's own daily file.

WHY THIS EXISTS
---------------
The Japanese baseline had no directional content. With no liquid single-stock options
there is no implied move and no 25-delta skew, so `edge_score.priced_lean_pct` fell
through to its `-0.05 * run_up_20d_pct` branch for every name. That made the baseline's
lean and the *free control* the same number, which means the control could never be
beaten by the baseline and the hunt was being asked to beat a rival it also depended on.

JPX publishes `<YYYYMMDD>_Short_Positions.xls` every trading day: one row per
(stock, short seller) for every disclosed position at or above 0.5% of shares
outstanding, carrying the current ratio, the share count, the previous calculation date
and **the previous ratio**. That gives two things the run-up cannot:

  level   how crowded the short side already is
  change  whether shorts are being built or covered into the print

Both are name-specific, market-based, published daily by the exchange, and arithmetically
independent of the 20-day run-up.

ABSENCE IS A ZERO, NOT A GAP
----------------------------
566 codes appeared in the 2026-09-18 file against roughly 3,900 listed companies. That is
not 14% coverage. The file is a disclosure register with a 0.5% threshold, so a name that
does not appear has **no disclosed short position above 0.5%** — which is information,
not missing data. `short_ratio_pct` is therefore 0.0 for an absent name and
`covered: true` says the file was read successfully, so a real zero is never confused
with a failed download.

WHAT IS NOT KNOWN
-----------------
The threshold truncates: a name at 0.4% and a name at 0.0% are both recorded as 0.0. The
register covers disclosed positions only, so market-maker and index-arbitrage shorts that
sit below the line are invisible. And the sign of the effect is a PRIOR, not a Japanese
measurement: the US run saw two crowded shorts (18% and 23% of float) squeeze more than
20%, which is why a crowded short is treated as a positive lean here. Nothing in this
repo has yet measured that in Tokyo. `jp_resolve.py` ranks each component separately for
exactly that reason -- the weights are meant to be replaced by measurement, not defended.
"""
import argparse
import json
import re
import subprocess
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "researcher_japan" / "analysis" / "short-positions-cache.json"
INDEX = "https://www.jpx.co.jp/markets/public/short-selling/index.html"
KABUTAN = "https://kabutan.jp/stock/kabuka?code={code}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Column indices in the JPX sheet, read off the header row rather than guessed.
COL_CODE, COL_NAME_EN, COL_RATIO, COL_PREV_RATIO = 2, 4, 10, 14


def _sh(cmd):
    return subprocess.run(cmd, capture_output=True)


def _fetch(url, referer=None):
    cmd = ["curl", "-sSL", "--max-time", "45", "-H", f"User-Agent: {UA}"]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    cmd.append(url)
    return _sh(cmd).stdout


def available_files():
    """Every short-position file JPX currently links, newest first.

    Returns [(YYYYMMDD, url)]. JPX keeps a rolling window, so an older run cannot be
    rebuilt from this source -- which is why the parsed result is cached.
    """
    html = _fetch(INDEX).decode("utf-8", "replace")
    out = []
    for href in re.findall(r'href="([^"]*(\d{8})_Short_Positions\.xls)"', html):
        path, day = href
        url = path if path.startswith("http") else "https://www.jpx.co.jp" + path
        out.append((day, url))
    return sorted(set(out), reverse=True)


def parse(blob):
    """Aggregate the per-seller rows into one row per securities code."""
    import xlrd
    wb = xlrd.open_workbook(file_contents=blob)
    ws = wb.sheet_by_index(0)
    agg = defaultdict(lambda: {"ratio": 0.0, "prev": 0.0, "sellers": 0, "name_en": None})
    for i in range(ws.nrows):
        row = ws.row_values(i)
        if len(row) <= COL_PREV_RATIO:
            continue
        raw = str(row[COL_CODE]).strip()
        if not raw or raw.lower().startswith("code"):
            continue
        # JPX writes numeric codes as floats ("4716.0") and alphanumeric ones as text.
        code = raw[:-2] if raw.endswith(".0") else raw
        if not re.fullmatch(r"\d{4}|\d{3}[A-Z]", code):
            continue
        try:
            ratio = float(row[COL_RATIO])
        except (TypeError, ValueError):
            continue
        try:
            prev = float(row[COL_PREV_RATIO])
        except (TypeError, ValueError):
            prev = 0.0
        a = agg[code]
        a["ratio"] += ratio
        a["prev"] += prev
        a["sellers"] += 1
        a["name_en"] = a["name_en"] or str(row[COL_NAME_EN]).strip() or None
    # JPX stores the ratio as a fraction (0.006 = 0.6%); percent is what everything
    # downstream talks in.
    return {c: {"short_ratio_pct": round(v["ratio"] * 100, 4),
                "short_ratio_prev_pct": round(v["prev"] * 100, 4),
                "short_change_pct_pts": round((v["ratio"] - v["prev"]) * 100, 4),
                "disclosed_sellers": v["sellers"],
                "name_en": v["name_en"]}
            for c, v in agg.items()}


def load(on_or_before=None, refresh=False):
    """The most recent short register at or before `on_or_before` (YYYY-MM-DD).

    Cached to `analysis/short-positions-cache.json`: JPX's window rolls, so once a day
    drops off the index it cannot be re-fetched and the cache is the only record.
    """
    cache = {}
    if CACHE.exists() and not refresh:
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    want = (on_or_before or date.today().isoformat()).replace("-", "")
    have = sorted([d for d in cache if d <= want], reverse=True)
    if have and not refresh:
        return have[0], cache[have[0]]

    for day, url in available_files():
        if day > want:
            continue
        blob = _fetch(url, referer=INDEX)
        if len(blob) < 10000:
            continue
        try:
            rows = parse(blob)
        except Exception:
            continue
        cache[day] = rows
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        return day, rows
    return None, {}


def for_code(code, rows, as_of):
    """One name's positioning. An absent code is a real zero, not a gap."""
    hit = rows.get(code)
    if hit is None:
        return {
            "short_ratio_pct": 0.0,
            "short_ratio_prev_pct": 0.0,
            "short_change_pct_pts": 0.0,
            "disclosed_sellers": 0,
            "covered": bool(rows),
            "basis": "absent from the JPX register, so no disclosed position at or "
                     "above the 0.5% threshold. A real zero, not missing data -- but "
                     "the threshold truncates, so 0.4% and 0.0% are both recorded here "
                     "as 0.0.",
            "as_of": as_of,
            "source": INDEX,
        }
    out = dict(hit)
    out.pop("name_en", None)
    out.update({"covered": True,
                "basis": "sum of disclosed positions at or above 0.5% of shares "
                         "outstanding, aggregated over sellers",
                "as_of": as_of, "source": INDEX})
    return out


def margin_ratio(code):
    """信用倍率 -- margin long balance divided by margin short balance.

    The number Japanese retail and the domestic desks actually watch, and the reason
    it is here is coverage: the JPX short register only carries positions at or above
    0.5%, which is 11 of 25 names on a real day, while 信用倍率 exists for essentially
    every margin-eligible name. High means leveraged longs are crowded and have to be
    sold eventually; below 1 means the margin short side is larger, which is the setup
    that squeezes.

    SCRAPED, not official. The JPX file above is an exchange publication with a stated
    calculation date; this is a number lifted out of a broker-portal page whose layout
    can change without notice. It is returned with `basis: "scraped"` and a null is a
    normal outcome, never an error -- nothing downstream may treat its absence as a
    failure.
    """
    out = _sh(["curl", "-sSL", "--max-time", "25", "-H", f"User-Agent: {UA}",
               KABUTAN.format(code=code)]).stdout.decode("utf-8", "replace")
    txt = " ".join(re.sub(r"<[^>]+>", " ", out).split())
    m = re.search(r"PER\s*PBR\s*利回り\s*信用倍率\s*(.*?)時価総額", txt)
    if not m:
        return None
    # The four values follow the four labels in order: PER, PBR, yield, margin ratio.
    vals = re.findall(r"(－|[\d,\.]+)\s*(?:倍|％)", m.group(1))
    if len(vals) < 4 or vals[3] == "－":
        return None
    try:
        return float(vals[3].replace(",", ""))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="most recent register at or before this date")
    ap.add_argument("--refresh", action="store_true", help="ignore the cache")
    ap.add_argument("--code", action="append", help="print these codes only")
    ap.add_argument("--margin", action="store_true",
                    help="also fetch the scraped 信用倍率 for each --code")
    a = ap.parse_args()
    day, rows = load(a.date, a.refresh)
    if not rows:
        raise SystemExit("no short-position file could be read")
    print(f"register {day}: {len(rows)} codes with a disclosed short position")
    if a.code:
        for c in a.code:
            rec = for_code(c, rows, day)
            if a.margin:
                rec["margin_ratio"] = margin_ratio(c)
            print(f"  {c}: {json.dumps(rec, ensure_ascii=False)}")
    else:
        top = sorted(rows.items(), key=lambda x: -x[1]["short_ratio_pct"])[:10]
        for c, v in top:
            print(f"  {c:<6} {(v['name_en'] or '')[:30]:<30} "
                  f"{v['short_ratio_pct']:>6.2f}%  "
                  f"(was {v['short_ratio_prev_pct']:.2f}, "
                  f"{v['short_change_pct_pts']:+.2f}pp, {v['disclosed_sellers']} sellers)")


if __name__ == "__main__":
    main()
