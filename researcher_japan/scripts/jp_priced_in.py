#!/usr/bin/env python3
"""Seal what the market has already priced into each Japanese name, before any hunt.

Same job as `researcher_us/scripts/priced_in.py`, and it writes the same shape, so
`researcher_us/scripts/edge_score.py` scores a Japanese run unchanged and the two
markets stay directly comparable. What differs is what this market will tell you.

THE OPTION ANCHOR DOES NOT EXIST HERE, AND THAT IS THE BIGGEST SINGLE CAVEAT
---------------------------------------------------------------------------
The US baseline's strongest number is the option-implied move for the event, with the
ATM spread as its quality measure and 25-delta skew as a direction lean. Japan has
listed single-stock options on a small set of names and they are not liquid; KRX and
JPX both concentrate their option volume in the index. So `options` is written with
every field `null` and a `reason`, honestly rather than by omission.

That is not cosmetic. `edge_score.baseline_quality` weights options at 0.35 and skew
at 0.25, so a Japanese name can score at most 0.40 on quality, and `priced_lean_pct`
falls through to its `-0.05 * run_up_20d_pct` branch for every name. Two things follow
and both belong in every note this stage writes:

  1. The control IS the lean. In the US sample `-run_up_20d_pct` ranked six days at
     rho=0.335 and the hunt's own evidence led it by 0.080 with a CI spanning zero.
     Here the control is not a rival sitting beside the key, it is literally the
     baseline's only directional content. If the Japanese hunt does not beat it,
     the hunt has added nothing at all.
  2. This is the regime that produced the worst number in the repo. On the sealed
     backtest corpus, where the option anchor was unrecoverable and every event ran
     on the historical-reaction proxy, the hunt ranked at rho=+0.073, p=0.45 over 104
     events. Japan runs in that regime permanently and by construction. Read
     `backtest/FINDINGS.md` section 33 before treating an early Japanese result as
     evidence of anything.

THE HISTORY ANCHOR IS A PROXY AND IS LABELLED AS ONE
----------------------------------------------------
TDnet keeps about 31 days online and JPX publishes only the near cohorts, so prior
announcement DATES are not retrievable from a free source. What is retrievable is
each prior period END, from Yahoo's `earningsHistory`, plus the lag between period end
and announcement implied by the date the issuer has notified for THIS quarter. Applying
that lag backwards gives an estimated prior announcement date; the reaction is then
read off the largest absolute move in a +/-2 trading day window around it.

That is a cadence prior, and this repo has already been burned by reading a cadence
prior as evidence: `session_resolve.py`'s cadence test read `fits` on TRT, a human
took it as confirmation, 33% of equity went behind it and the company never reported.
So every history row carries `basis: "estimated"`, the estimated date, the date
actually used and the gap between them. A row whose window move is not clearly the
largest nearby is not evidence that a print happened there. Treat `median_abs_move_pct`
as a scale, never as a fact about a specific past date.

WHAT IS REAL AND SOURCED
------------------------
Spot, the 20-day run-up and turnover are off the tape. EPS actual, EPS estimate and
the surprise percentage are Yahoo's own consensus records and are carried through
unmodified with their source URL. Those are the numbers a hunter should lean on.
"""
import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
UTC = ZoneInfo("UTC")
REPO = Path(__file__).resolve().parents[2]
YQ = "https://query1.finance.yahoo.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
_crumb = {"v": None}


QUARTER_N = {"第１四半期": 1, "第1四半期": 1, "第２四半期": 2, "第2四半期": 2,
             "第３四半期": 3, "第3四半期": 3, "本決算": 4, "通期": 4, "第４四半期": 4}


def shift_months(d, months):
    """Month arithmetic that lands on the last day of the target month.

    Fiscal period ends are month-ends, so stepping back a quarter from 2026-08-31
    has to give 2026-05-31 and not 2026-05-28 or an error.
    """
    y, m = d.year, d.month - months
    while m <= 0:
        m += 12
        y -= 1
    while m > 12:
        m -= 12
        y += 1
    nxt = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return nxt - timedelta(days=1)


def period_end_for(fiscal_year_end, quarter_label):
    """The period this release covers, from the fiscal year-end and the quarter.

    Taken from JPX's own two columns rather than from a vendor's quarter list. The
    first version of this read the lag off Yahoo's `earningsHistory`, whose most
    recent period end for a small Japanese name is often a quarter or two stale: DCM
    Holdings came out with a 121-day lag where the true lag was 29, and every
    estimated prior date was then three months wrong.
    """
    try:
        fye = date.fromisoformat(fiscal_year_end)
    except Exception:
        return None
    q = QUARTER_N.get((quarter_label or "").strip())
    if not q:
        return None
    return shift_months(fye, 3 * (4 - q))


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def crumb():
    if _crumb["v"] is None:
        sh(f"curl -sS --max-time 20 -c /tmp/jpyc.txt -H 'User-Agent: {UA}' -o /dev/null https://fc.yahoo.com")
        _crumb["v"] = sh(f"curl -sS --max-time 20 -b /tmp/jpyc.txt -H 'User-Agent: {UA}' '{YQ}/v1/test/getcrumb'").strip()
    return _crumb["v"]


def get_json(url, with_crumb=False):
    c = f"curl -sS --max-time 35 -H 'User-Agent: {UA}'"
    if with_crumb:
        c += " -b /tmp/jpyc.txt"
    out = sh(f"{c} '{url}'")
    try:
        return json.loads(out)
    except Exception:
        return None


def bars(code):
    d = get_json(f"{YQ}/v8/finance/chart/{code}.T?range=3y&interval=1d")
    try:
        r = d["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        ts = r["timestamp"]
        rows = []
        for i, t in enumerate(ts):
            c, o, v = q["close"][i], q["open"][i], (q.get("volume") or [None] * len(ts))[i]
            if c is None:
                continue
            rows.append({"d": datetime.fromtimestamp(t, JST).date(), "c": c, "o": o, "v": v})
        return rows, r["meta"]
    except Exception:
        return [], {}


def reaction_near(rows, target, window=2):
    """Largest one-day close-to-close move within +/-`window` trading days of `target`.

    Returns the move and the date it was taken from, plus how far that is from the
    estimate, so a reader can see when the proxy is reaching.
    """
    idx = [i for i, r in enumerate(rows) if r["d"] >= target]
    if not idx or idx[0] == 0:
        return None
    i0 = idx[0]
    best = None
    for i in range(max(1, i0 - window), min(len(rows), i0 + window + 1)):
        prev, cur = rows[i - 1], rows[i]
        if not prev["c"]:
            continue
        mv = (cur["c"] / prev["c"] - 1.0) * 100.0
        if best is None or abs(mv) > abs(best[0]):
            best = (mv, cur["d"], i)
    if best is None:
        return None
    mv, used, _ = best
    return {"move_pct": round(mv, 2), "date_used": used.isoformat(),
            "date_estimated": target.isoformat(),
            "days_from_estimate": (used - target).days}


def build(name, event_date):
    code = name["code"]
    rows, meta = bars(code)
    src_chart = f"{YQ}/v8/finance/chart/{code}.T?range=3y&interval=1d"
    doc = {
        "market": "JP",
        "ticker": code,
        "yahoo_symbol": f"{code}.T",
        "company": name.get("name_en") or name.get("name_ja"),
        "company_ja": name.get("name_ja"),
        "industry": name.get("industry_en"),
        "event_date": event_date,
        "session": "amc",
        "window": f"{event_date} 15:00 JST -> next open 09:00 JST",
        "quarter": name.get("quarter"),
        "fiscal_year_end": name.get("fiscal_year_end"),
        "sealed_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "sources": {"tape": src_chart,
                    "calendar": "https://www.jpx.co.jp/listing/event-schedules/"
                                "financial-announcement/index.html"},
    }

    closes = [r["c"] for r in rows]
    spot = closes[-1] if closes else None
    win = closes[-21:]
    doc["tape"] = {
        "spot": round(spot, 2) if spot else None,
        "currency": meta.get("currency"),
        "run_up_20d_pct": round((win[-1] / win[0] - 1) * 100, 2) if len(win) >= 2 else None,
        "median_turnover_jpy_20d": name.get("tape", {}).get("median_turnover_jpy_20d"),
        "bars_3y": len(rows),
    }

    # Explicitly null, with the reason, rather than absent. edge_score reads these
    # keys and an absent `options` block and an empty one must not look different.
    doc["options"] = {
        "event_implied_move_pct": None,
        "atm_spread_frac_of_mid": None,
        "skew_25d_vol_points": None,
        "reason": "No liquid single-stock option market in Japan for this name. JPX "
                  "option volume is concentrated in the index, so there is no "
                  "event-implied move and no skew to read a direction lean from. "
                  "priced_lean_pct therefore falls back to -0.05 * run_up_20d_pct "
                  "for every Japanese name, which makes the free control and the "
                  "baseline's only directional content the same number.",
    }

    # Consensus: real, sourced, unmodified.
    qs = f"{YQ}/v10/finance/quoteSummary/{code}.T?modules=earningsHistory&crumb={crumb()}"
    eh = get_json(qs, with_crumb=True)
    hist_rows, cons = [], []
    try:
        items = eh["quoteSummary"]["result"][0]["earningsHistory"]["history"]
    except Exception:
        items = []
    for it in items:
        qend = (it.get("quarter") or {}).get("fmt")
        cons.append({
            "period_end": qend,
            "eps_actual": (it.get("epsActual") or {}).get("raw"),
            "eps_estimate": (it.get("epsEstimate") or {}).get("raw"),
            "surprise_pct": (it.get("surprisePercent") or {}).get("raw"),
        })
    doc["consensus"] = {"source": qs.split("&crumb=")[0], "quarters": cons}

    # The cadence proxy, built off JPX's own fiscal columns.
    pe0 = period_end_for(name.get("fiscal_year_end"), name.get("quarter"))
    lag = None
    if pe0:
        try:
            lag = (date.fromisoformat(event_date) - pe0).days
        except Exception:
            lag = None
        if lag is not None and not (0 < lag < 150):
            lag = None                      # a lag outside this is a parse error

    if lag and rows:
        first_bar, ed = rows[0]["d"], date.fromisoformat(event_date)
        for k in range(1, 13):              # three years back, one row per quarter
            prior_end = shift_months(pe0, 3 * k)
            est = prior_end + timedelta(days=lag)
            if est >= ed or est <= first_bar:
                continue
            r = reaction_near(rows, est)
            if r:
                r["period_end"] = prior_end.isoformat()
                r["basis"] = "estimated"
                hist_rows.append(r)
        hist_rows.sort(key=lambda x: x["date_used"])

    moves = [abs(r["move_pct"]) for r in hist_rows]
    doc["history"] = {
        "n": len(hist_rows),
        "basis": "estimated_from_cadence",
        "lag_days_used": lag,
        "period_end_this_quarter": pe0.isoformat() if pe0 else None,
        "median_abs_move_pct": round(median(moves), 2) if moves else None,
        "events": hist_rows,
        "caveat": "Announcement DATES are estimated by applying this quarter's "
                  "notified lag backwards to prior period ends; the move is the "
                  "largest within +/-2 trading days of that estimate. This is a "
                  "cadence prior, not a record that a print happened on that date. "
                  "Use it as a scale for how much this name moves, never as "
                  "evidence about a particular past date.",
    }

    # JPX carries the date the ISSUER notified to the exchange. That is stronger
    # confirmation than anything the US calendar offers -- the Nasdaq feed's
    # `time-not-supplied` was 20 of 20 phantom on 2026-09-17 -- so a row present
    # here is treated as a confirmed event rather than an unknown one.
    doc["event_plausibility"] = {
        "verdict": "fits_cadence",
        "basis": "issuer-notified date carried by JPX on the 決算発表予定日 sheet",
        "calendar_as_of": name.get("_calendar_as_of"),
    }
    doc["event_occurred"] = None      # settled after the fact by jp_resolve
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()

    u = json.loads(Path(a.universe).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    made = 0
    for n in u.get("names", []):
        n = dict(n)
        n["_calendar_as_of"] = u.get("calendar_as_of")
        doc = build(n, u["event_date"])
        p = out / f"{n['code']}.json"
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made += 1
        print(f"  sealed {n['code']:<6} {(doc['company'] or '')[:34]:<34} "
              f"spot={doc['tape']['spot']} runup={doc['tape']['run_up_20d_pct']} "
              f"hist_n={doc['history']['n']}")
    print(f"{made} baselines -> {out}")


if __name__ == "__main__":
    main()
