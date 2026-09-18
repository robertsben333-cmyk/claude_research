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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jp_positioning as POS               # noqa: E402

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


def realised_vol_pct(rows, n=20):
    """Annualised close-to-close volatility over the last `n` sessions, in percent.

    The magnitude anchor the option chain would have given. It is not an implied move
    and must not be called one: it says how much this stock HAS been moving, not how
    much the market is paying for it to move through this print. Its virtue over the
    historical-reaction proxy is that it is current -- a name whose vol has doubled in
    the last month shows up here and does not show up in a median of twelve estimated
    reactions from the last three years.
    """
    cl = [r["c"] for r in rows if r["c"]]
    if len(cl) < n + 1:
        return None
    rets = [(cl[i] / cl[i - 1] - 1.0) for i in range(len(cl) - n, len(cl))]
    if len(rets) < 2:
        return None
    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
    return round((var ** 0.5) * (252 ** 0.5) * 100, 2)


def lean_components(positioning, margin, runup):
    """The four things Tokyo prices that the run-up does not, each signed, in points.

    NONE OF THESE WEIGHTS IS MEASURED ON JAPANESE DATA. They are priors, and they are
    kept as separate named components precisely so that `jp_resolve.py` can rank each
    one against the realised move and replace the priors with measurement. Do not
    defend the weights; replace them.

    Signs, and where each prior comes from:

      short_squeeze   crowded disclosed short -> POSITIVE. The US run saw two shorts
                      into names with 18% and 23% of float short both squeeze more
                      than 20%. A crowded short is fuel, not a forecast.
      short_building  shorts ADDING into the print -> NEGATIVE. Disclosed sellers
                      increasing a position days before results is positioning by
                      people who must file their names; it is the closest thing this
                      market has to informed flow you can see.
      margin_overhang high 信用倍率 (margin longs >> margin shorts) -> NEGATIVE.
                      Leveraged retail longs have to be sold eventually and a
                      disappointing print is when. Below 1 the margin short side is
                      larger, which is the setup that squeezes, so the sign flips.
                      Log-scaled because the raw ratio runs from 2 to 2,395.
      runup           the US fallback, kept so the composite still contains what the
                      free control contains -- but no longer ONLY that.
    """
    import math
    out = {}
    sr = (positioning or {}).get("short_ratio_pct")
    sc = (positioning or {}).get("short_change_pct_pts")
    out["short_squeeze"] = round(max(-3.0, min(3.0, 0.6 * sr)), 3) if sr is not None else None
    out["short_building"] = round(max(-2.0, min(2.0, -2.0 * sc)), 3) if sc is not None else None
    if margin and margin > 0:
        out["margin_overhang"] = round(max(-2.0, min(2.0, -0.5 * math.log10(margin))), 3)
    else:
        out["margin_overhang"] = None
    out["runup"] = round(-0.05 * runup, 3) if runup is not None else None
    return out


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
        # The 5-day run-in, added 2026-09-18 after the first live run found the 20-day
        # window hiding the thing that mattered. On 4716 the 20-day read -0.42%, which
        # says "no directional content", while the five sessions into the print were
        # +4.4% on a US-parent read-through -- the hunter had to source the move itself
        # off raw bars because the baseline netted an early-September drawdown against
        # a late bounce. A run-in the market has to justify at the print is exactly what
        # a lean is for, so it is now sealed rather than left to be rediscovered.
        # NOTE: it is NOT in priced_lean_pct. Adding it would be a second helping of the
        # run-up in a composite that already carries the 20-day one, and no Japanese
        # measurement says which window belongs there. jp_resolve.py ranks it separately.
        "run_up_5d_pct": round((closes[-6:][-1] / closes[-6:][0] - 1) * 100, 2)
                         if len(closes) >= 6 else None,
        "median_turnover_jpy_20d": name.get("tape", {}).get("median_turnover_jpy_20d"),
        "realised_vol_20d_pct": realised_vol_pct(rows, 20),
        "realised_vol_60d_pct": realised_vol_pct(rows, 60),
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
                  "event-implied move and no skew. Until 2026-09-18 that left "
                  "priced_lean_pct as -0.05 * run_up_20d_pct, which is ALSO the free "
                  "control, so the baseline's lean and its own benchmark were the same "
                  "number. They are no longer: `positioning` and `expected_move` below "
                  "carry substitutes built from what Tokyo does publish, and this "
                  "baseline supplies its own `priced_lean_pct` and `anchor_quality`.",
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
    # --- what Tokyo prices, in place of an option chain -------------------------
    pos = POS.for_code(code, name.get("_short_rows") or {}, name.get("_short_as_of"))
    margin = name.get("_margin_ratio")
    doc["positioning"] = dict(pos)
    doc["positioning"]["margin_ratio"] = margin
    doc["positioning"]["margin_ratio_basis"] = (
        "信用倍率, margin long balance / margin short balance, scraped from a broker "
        "portal rather than published by the exchange. Null is a normal outcome."
    )

    rv20 = doc["tape"]["realised_vol_20d_pct"]
    hist_med = doc["history"]["median_abs_move_pct"]
    # A one-session move implied by current vol. Not an implied move -- there is no
    # option paying for this -- so it is named for what it is.
    vol_1d = round(rv20 / (252 ** 0.5), 2) if rv20 else None
    doc["expected_move"] = {
        "event_move_proxy_pct": max([x for x in (hist_med, vol_1d) if x is not None],
                                    default=None),
        "from_realised_vol_1d_pct": vol_1d,
        "from_history_median_pct": hist_med,
        "basis": "the larger of (a) the median of twelve ESTIMATED prior reactions and "
                 "(b) a one-session move implied by 20-day realised volatility. It is "
                 "NOT an option-implied move: nothing is paying for it, and it carries "
                 "no information about what the market expects from THIS print. It is "
                 "a scale for how far this name travels.",
    }

    comps = lean_components(pos, margin, doc["tape"]["run_up_20d_pct"])
    vals = [v for v in comps.values() if v is not None]
    doc["lean_components"] = comps
    doc["priced_lean_pct"] = round(sum(vals), 3) if vals else None
    doc["priced_lean_basis"] = (
        "Sum of the components above. Read researcher_japan/scripts/jp_priced_in.py, "
        "lean_components(): every weight is a PRIOR, none is measured on Japanese "
        "data, and jp_resolve.py ranks each component separately so measurement can "
        "replace them. What matters today is only that this is no longer identical to "
        "-0.05 * run_up_20d_pct, so the free control is a real rival again."
    )

    # How well anchored is this name, for a market with no option chain. Read by the
    # shared scorer's baseline_quality(). Neither term reaches 1.0 on purpose: an
    # option-implied move with a tight two-sided chain is better than any of this.
    have_dir = sum(1 for k in ("short_squeeze", "short_building", "margin_overhang")
                   if comps.get(k) is not None)
    doc["anchor_quality"] = {
        "magnitude": 0.5 if (rv20 and hist_med) else (0.3 if (rv20 or hist_med) else 0.0),
        "direction": {0: 0.0, 1: 0.25, 2: 0.45, 3: 0.60}[have_dir],
        "basis": "magnitude: realised vol plus an estimated-cadence reaction history, "
                 "capped at 0.5 because neither is an option-implied move. direction: "
                 "how many of the three positioning components resolved, capped at "
                 "0.60 because none of them is 25-delta skew.",
    }

    doc["event_occurred"] = None      # settled after the fact by jp_resolve
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-margin", action="store_true",
                    help="skip the scraped 信用倍率 lookup (one request per name)")
    a = ap.parse_args()

    u = json.loads(Path(a.universe).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # One download for the whole day rather than one per name.
    short_as_of, short_rows = POS.load(u.get("event_date"))
    if not short_rows:
        print("  WARNING: no JPX short register could be read; positioning will be "
              "empty and the lean falls back to the run-up alone")
    else:
        print(f"  short register {short_as_of}: {len(short_rows)} codes")

    made = 0
    for n in u.get("names", []):
        n = dict(n)
        n["_calendar_as_of"] = u.get("calendar_as_of")
        n["_short_rows"] = short_rows
        n["_short_as_of"] = short_as_of
        n["_margin_ratio"] = POS.margin_ratio(n["code"]) if not a.no_margin else None
        doc = build(n, u["event_date"])
        p = out / f"{n['code']}.json"
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made += 1
        print(f"  sealed {n['code']:<6} {(doc['company'] or '')[:30]:<30} "
              f"spot={doc['tape']['spot']!s:<9} lean={doc['priced_lean_pct']!s:<7} "
              f"short={doc['positioning']['short_ratio_pct']}% "
              f"margin={doc['positioning']['margin_ratio']} "
              f"q={doc['anchor_quality']['direction']}")
    print(f"{made} baselines -> {out}")


if __name__ == "__main__":
    main()
