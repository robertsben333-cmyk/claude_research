#!/usr/bin/env python3
"""The day's Japanese earnings universe, from the exchange's own forward calendar.

WHY THIS IS NOT A PORT OF edge_universe.py
------------------------------------------
The US stage reads a vendor calendar (Nasdaq) whose `time` field is a schedule for
two of its three values and an admission of ignorance for the third, so most of
`session_resolve.py` exists to tell a real reporter from a phantom row. Japan does
not have that problem: JPX itself publishes `決算発表予定日 / Scheduled Date` as a
spreadsheet per fiscal-month cohort, with the code, both names, the fiscal year-end
and the quarter. It is the issuer's own notified date, carried by the exchange, with
a stated as-of date on the sheet. A row here is a company that has told the exchange
when it will report.

WHAT IT STILL DOES NOT GUARANTEE
--------------------------------
A notified date can move, and the sheet is a snapshot: `as_of` is read off the file
and carried into the output so a later reader can see how stale the calendar was
when the run sealed. Confirmation that the release actually landed is `jp_resolve`'s
job, after the fact, against TDnet. Nothing here predicts.

THE SESSION
-----------
Tokyo trades 09:00-11:30 and 12:30-15:00 JST. Earnings land overwhelmingly after the
15:00 close: on 2026-08-14, 386 of 456 `決算短信` were timestamped 15:00 or later, and
on 2026-09-01 all 24 were. So a name scheduled for date D is an `amc` event on D, and
the window this stage ranks is D 15:00 JST to D+1 09:00 JST. There is no US-style
BMO cohort to speak of, and `session` is written anyway so the scorer and the
resolver read the same field name they read for the US run.

SELECTION, AND WHY IT IS RANDOM
-------------------------------
In season this calendar carries up to 125 companies on one date, and the season peak
on TDnet was 456 releases in a day. The stage hunts one company per hunter, so the
day has to be cut. The cut is two steps and the second one is deliberately not a
judgement:

  1. Drop the microcaps, on median 20-day turnover. Capacity is real and the US
     analysis found the turnover floor helped monotonically. The default is
     30,000,000 JPY, which at 150 JPY to the dollar is the same ~$200k a day the US
     run screens on, so the two markets' universes are cut on a comparable bar
     rather than on two numbers chosen separately. It bites much harder here: the
     Japanese tail is far thinner than the US one. On the 62 names scheduled for
     2026-10-09 the median was 7,367,800 JPY a day, about $49k, and this floor kept
     40% of them. That is the intended effect -- it is the "deselect microcaps"
     step -- but it means the ranked universe is explicitly the liquid half of the
     day and is not a sample of Japanese listed companies.
  2. If more than `cap` survive, take a RANDOM sample of them, seeded by the date.

Random, because every selection rule that is not random is a second ranking the
scorer cannot see. The US run has already paid for this once: its two highest
`hunt_priority` names got two hunters each, and because the key is a sum, those
names carried the largest conviction by construction -- `edge_hunter_control.py` had
to rebuild all 38 events to find out how much of the headline was the selection
rather than the finding. A seeded random draw cannot do that. The seed is the date,
so the draw is reproducible, and `eligible` carries every name that could have been
drawn, so anyone can check the draw against the population it came from.
"""
import argparse
import io
import json
import random
import re
import subprocess
import sys
import urllib.parse
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

SHUKUJITSU = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
HOLIDAY_CACHE = REPO / "researcher_japan" / "analysis" / "jp-holidays.json"
JPX_INDEX = ("https://www.jpx.co.jp/listing/event-schedules/"
             "financial-announcement/index.html")
JPX_HOST = "https://www.jpx.co.jp"
YQ = "https://query1.finance.yahoo.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def fetch(url, binary=False, referer=None, timeout=45):
    """curl, not urllib: this container reaches the internet through a proxy that
    urllib does not pick up, and a silent URLError here would look like an empty
    calendar rather than a broken fetch."""
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {UA}"]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    cmd += ["-w", "\n%{http_code}", url]
    p = subprocess.run(cmd, capture_output=True)
    out = p.stdout
    tail = out[-4:].decode("ascii", "replace").strip()
    body = out[: -len(tail) - 1] if tail.isdigit() else out
    code = int(tail) if tail.isdigit() else 0
    if code != 200:
        raise RuntimeError(f"HTTP {code} for {url}")
    return body if binary else body.decode("utf-8", "replace")


def market_closed(day):
    """Is Tokyo shut on `day` (a date)? Returns a reason string, or None if open.

    WHY THIS IS NOT COSMETIC. An empty calendar has two completely different causes and
    they need opposite responses: the fiscal cohort's sheet is not published yet (wait),
    or the exchange is shut (nothing to wait for). Without this the run records the first
    reason for both, and next week is the worked example -- Tokyo is closed 2026-09-21,
    09-22 and 09-23 for 敬老の日, a 国民の休日 and 秋分の日, so the Routine fires into
    three consecutive shut days and would have logged a misleading explanation each
    time. This repo has already paid for a wrong reason recorded confidently.

    Source is the Cabinet Office's own 国民の祝日 CSV, which is the authoritative list.
    TSE additionally closes 31 December to 3 January, which no holiday list carries
    because they are not public holidays.
    """
    if day.weekday() >= 5:
        return "weekend"
    if (day.month, day.day) in ((12, 31), (1, 1), (1, 2), (1, 3)):
        return "year-end / new-year exchange holiday (31 Dec - 3 Jan)"

    holidays = {}
    if HOLIDAY_CACHE.exists():
        try:
            holidays = json.loads(HOLIDAY_CACHE.read_text(encoding="utf-8"))
        except Exception:
            holidays = {}
    if day.isoformat() not in holidays:
        try:
            raw = fetch(SHUKUJITSU, binary=True)
            text = None
            for enc in ("cp932", "utf-8-sig", "utf-8"):
                try:
                    text = raw.decode(enc)
                    break
                except Exception:
                    continue
            if text:
                import csv as _csv
                import io as _io
                fresh = {}
                for row in _csv.reader(_io.StringIO(text)):
                    if len(row) < 2 or "/" not in row[0]:
                        continue
                    try:
                        y, m, d = (int(x) for x in row[0].split("/"))
                    except ValueError:
                        continue
                    fresh[date(y, m, d).isoformat()] = row[1]
                if fresh:
                    holidays = fresh
                    HOLIDAY_CACHE.parent.mkdir(parents=True, exist_ok=True)
                    HOLIDAY_CACHE.write_text(
                        json.dumps(holidays, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass                      # an unreachable list is not a reason to stop
    name = holidays.get(day.isoformat())
    return f"public holiday: {name}" if name else None


def cohort_files():
    """Every `kessan*.xlsx` JPX currently publishes.

    There is one per fiscal-month cohort and only the near ones are up at any time:
    in September 2026 the page carried July and August only, because the March
    cohort -- about 90% of the market -- does not publish its sheet until its own
    season nears. So this is a NEAR-HORIZON calendar by construction, and a day
    with no rows is more often "that cohort's sheet is not up yet" than "nobody
    reports". The count of sheets read is written into the output for that reason.
    """
    html = fetch(JPX_INDEX)
    hrefs = sorted(set(re.findall(r'href="([^"]*kessan[^"]*\.xlsx)"', html)))
    return [h if h.startswith("http") else JPX_HOST + h for h in hrefs]


def parse_cohort(blob):
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(blob), data_only=True, read_only=True)
    ws = wb.worksheets[0]
    as_of, header_seen, rows = None, False, []
    for r in ws.iter_rows(values_only=True):
        if not r:
            continue
        first = str(r[0]) if r[0] is not None else ""
        if not header_seen:
            m = re.search(r"As of (\d{4})/(\d{1,2})/(\d{1,2})", first)
            if m:
                as_of = date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
            if "決算発表予定日" in first:
                header_seen = True
            continue
        if r[0] is None or r[1] is None:
            continue
        d = r[0].date() if isinstance(r[0], datetime) else None
        if d is None:
            continue
        fy = r[4].date().isoformat() if isinstance(r[4], datetime) else None
        rows.append({
            "scheduled_date": d.isoformat(),
            "code": str(r[1]).strip(),
            "name_ja": str(r[2]).strip() if r[2] else None,
            "name_en": str(r[3]).strip() if r[3] else None,
            "fiscal_year_end": fy,
            "industry_ja": str(r[5]).strip() if len(r) > 5 and r[5] else None,
            "industry_en": str(r[6]).strip() if len(r) > 6 and r[6] else None,
            "quarter": str(r[7]).strip() if len(r) > 7 and r[7] else None,
        })
    return as_of, rows


def calendar():
    seen, rows, as_ofs, files = set(), [], [], []
    for url in cohort_files():
        try:
            as_of, got = parse_cohort(fetch(url, binary=True, referer=JPX_INDEX))
        except Exception as exc:                      # one bad sheet is not the day
            files.append({"url": url, "error": str(exc)})
            continue
        files.append({"url": url, "as_of": as_of, "rows": len(got)})
        if as_of:
            as_ofs.append(as_of)
        for x in got:
            key = (x["scheduled_date"], x["code"])
            if key in seen:
                continue
            seen.add(key)
            rows.append(x)
    return rows, (min(as_ofs) if as_ofs else None), files


def tape(code, days=40):
    """Spot, 20-day run-up and median turnover, off Yahoo's `<code>.T` bars.

    Turnover rather than market cap is the microcap screen, for the same reason the
    US run screens on dollar volume: what binds is what can be traded in a day, and
    a 2,000-yen stock with no volume is not made tradeable by a large float. Median,
    not mean, because one earnings day in the window would otherwise set the level.
    """
    url = f"{YQ}/v8/finance/chart/{code}.T?range={days}d&interval=1d"
    try:
        d = json.loads(fetch(url, timeout=30))
    except Exception as exc:
        return {"error": str(exc)}
    try:
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        closes = [c for c in q["close"] if c is not None]
        vols = [v for v in (q.get("volume") or []) if v is not None]
        if len(closes) < 5:
            return {"error": "too few bars"}
        pairs = [(c, v) for c, v in zip(q["close"], q.get("volume") or [])
                 if c is not None and v is not None]
        turn = sorted(c * v for c, v in pairs[-20:]) or [0]
        med = turn[len(turn) // 2]
        window = closes[-21:]
        runup = ((window[-1] / window[0] - 1.0) * 100.0) if len(window) >= 2 else None
        return {
            "spot": round(closes[-1], 2),
            "currency": res["meta"].get("currency"),
            "run_up_20d_pct": round(runup, 2) if runup is not None else None,
            "median_turnover_jpy_20d": int(med),
            "bars": len(closes),
            "as_of": datetime.now(JST).isoformat(timespec="seconds"),
        }
    except Exception as exc:
        return {"error": f"parse: {exc}"}


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="event date, JST. Default: today in Tokyo.")
    ap.add_argument("--cap", type=int, default=25,
                    help="most names to hunt in a day (default 25)")
    ap.add_argument("--min-turnover-jpy", type=int, default=30_000_000,
                    help="median 20-day turnover floor; below it is a microcap and "
                         "is dropped before the draw (default 3e7 JPY, ~$200k/day, "
                         "the same capacity bar the US run screens on)")
    ap.add_argument("--no-tape", action="store_true",
                    help="skip Yahoo entirely; emits the calendar with no screen "
                         "and no draw, for inspecting what JPX is publishing")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    target = a.date or datetime.now(JST).date().isoformat()
    closed = market_closed(date.fromisoformat(target))
    rows, as_of, files = calendar()
    todays = [r for r in rows if r["scheduled_date"] == target]

    out = {
        "market": "JP",
        "event_date": target,
        "window": f"{target} 15:00 JST -> next open 09:00 JST",
        "session": "amc",
        "calendar_as_of": as_of,
        "calendar_sheets": files,
        "calendar_rows_total": len(rows),
        "scheduled_today": len(todays),
        "market_closed": closed,
        "cap": a.cap,
        "min_turnover_jpy": a.min_turnover_jpy,
        "generated_utc": datetime.now(ZoneInfo("UTC")).isoformat(timespec="seconds"),
    }

    if closed and not todays:
        out["names"] = []
        out["note"] = (f"Tokyo is closed on {target} ({closed}). An empty calendar here "
                       f"is the exchange being shut, NOT a cohort sheet that has yet to "
                       f"be published. Nothing to wait for and nothing to hunt.")
        text = json.dumps(out, ensure_ascii=False, indent=2)
        if a.out:
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_text(text + "\n", encoding="utf-8")
            print(f"{target}: market closed ({closed}); empty universe -> {a.out}")
        else:
            print(text)
        return

    if a.no_tape:
        out["names"] = todays
        out["note"] = "--no-tape: no screen, no draw"
    else:
        eligible, dropped = [], []
        for r in todays:
            r = dict(r)
            r["tape"] = tape(r["code"])
            t = r["tape"]
            turn = t.get("median_turnover_jpy_20d")
            if t.get("error") or turn is None:
                r["drop_reason"] = f"no tape ({t.get('error', 'missing')})"
                dropped.append(r)
            elif turn < a.min_turnover_jpy:
                r["drop_reason"] = f"microcap: turnover {turn:,} < {a.min_turnover_jpy:,}"
                dropped.append(r)
            else:
                eligible.append(r)

        # Seeded by the date, so the draw is reproducible from the output alone and
        # nobody has to trust that it was not re-rolled until it looked good.
        seed = f"jp-{target}"
        rng = random.Random(seed)
        if len(eligible) > a.cap:
            picked = sorted(rng.sample(eligible, a.cap), key=lambda x: x["code"])
            method = f"random sample of {len(eligible)} eligible, seed '{seed}'"
        else:
            picked = sorted(eligible, key=lambda x: x["code"])
            method = f"all {len(eligible)} eligible names (at or under the cap)"

        out["selection"] = {"method": method, "seed": seed,
                            "eligible": len(eligible), "dropped": len(dropped),
                            "hunted": len(picked)}
        out["eligible_codes"] = sorted(x["code"] for x in eligible)
        out["names"] = picked
        out["dropped"] = dropped

    text = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text + "\n", encoding="utf-8")
        s = out.get("selection", {})
        print(f"{target}: {len(rows)} calendar rows, {len(todays)} scheduled today, "
              f"{s.get('eligible', '-')} eligible, {s.get('hunted', '-')} hunted "
              f"-> {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
