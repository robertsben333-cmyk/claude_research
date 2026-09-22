#!/usr/bin/env python3
"""Seal what the market has already priced into each ASX name, before any hunt.

Same job as `researcher_us/scripts/priced_in.py`, and it writes the same shape, so
`researcher_us/scripts/edge_score.py` scores an Australian run unchanged and the four
markets stay directly comparable. What differs is what this market will tell you.

THERE IS NO OPTION ANCHOR, AND THAT IS THE BIGGEST SINGLE CAVEAT
-----------------------------------------------------------------
Measured 2026-09-22 through the repo's own authenticated Yahoo path: AAPL returns 22
expiries, TSM 19, ITUB 8. `BHP.AX` and `CBA.AX` return ZERO, as do every Canadian,
Hong Kong, Japanese, Swiss and Indian symbol tried. ASX single-stock options exist and
are not retrievable free from this container, so `options` is written with every field
null and a reason, honestly rather than by omission.

That puts stage AU in the same regime as stages J and EU, which is the regime the
sealed backtest priced at rho=+0.073, p=0.45 over 104 events
(`archive/backtest/FINDINGS.md` section 33). Nothing about Australia refutes that, and
every note this stage writes has to say so.

WHAT IS BETTER HERE THAN IN TOKYO OR EUROPE, AND IT IS TWO THINGS
-------------------------------------------------------------------
1. THE SHORT REGISTER IS NOT TRUNCATED. ASIC publishes the aggregate short position for
   every product, not the positions above a 0.5% disclosure threshold: 430 of the 755
   rows on 2026-09-16 were below 0.5%, minimum 0.000000%. So the level is a real number
   and the change moves when the position moves rather than when a holder crosses a
   line. Everywhere else in this repo a below-threshold name reads 0.0 and
   `anchor_covered` exists to record that the zero is not real. Here it is real.
   The cost is the LAG: ASIC publishes about four business days in arrears, carried as
   `positioning.lag_sessions` and never treated as zero.

2. THE REACTION HISTORY IS OBSERVED, NOT ESTIMATED. The ASX per-issuer announcement
   archive is queryable by year and goes back years, so prior results announcements
   carry their real dates and their real timestamps. Japan cannot do this -- TDnet
   keeps about 31 days, so `jp_priced_in` applies this quarter's lag backwards and
   labels every history row `estimated`. Reading a cadence prior as evidence is how
   TRT was ranked, traded and never reported. Australian history rows carry
   `basis: "observed"` and the announcement's own timestamp, so they are evidence
   about a date and may be cited as such.

WHAT IS REAL AND SOURCED
------------------------
Spot, the run-ups, turnover and realised vol are off the tape. EPS actual, estimate and
surprise are Yahoo's own consensus records, carried through unmodified with their source
URL. The short register is ASIC's own publication. The history dates are ASX's own
announcement record. Nothing in this file is inferred except the lean weights, which are
priors and are labelled as priors.
"""
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
import au_market as M                                              # noqa: E402
import au_positioning as POS                                       # noqa: E402

_crumb = {"v": None}


def crumb():
    """Yahoo's quoteSummary wants a cookie and a crumb; the chart endpoint does not."""
    if _crumb["v"] is None:
        M.sh(["curl", "-sSL", "--max-time", "25", "-c", "/tmp/au_yq_cookies",
              "-H", f"User-Agent: {M.UA}", "https://fc.yahoo.com"])
        out = M.sh(["curl", "-sSL", "--max-time", "25", "-b", "/tmp/au_yq_cookies",
                    "-H", f"User-Agent: {M.UA}",
                    f"{M.YQ}/v1/test/getcrumb"]).stdout.decode("utf-8", "replace")
        _crumb["v"] = out.strip()
    return _crumb["v"]


def get_json(url, with_crumb=False):
    cmd = ["curl", "-sSL", "--max-time", "40", "-H", f"User-Agent: {M.UA}"]
    if with_crumb:
        cmd += ["-b", "/tmp/au_yq_cookies"]
    cmd.append(url)
    try:
        return json.loads(M.sh(cmd).stdout.decode("utf-8", "replace"))
    except Exception:
        return {}


def bars(code):
    sym = M.yahoo_symbol(code)
    url = f"{M.YQ}/v8/finance/chart/{sym}?range=3y&interval=1d"
    d = get_json(url)
    try:
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        rows = [{"d": datetime.fromtimestamp(t, M.SYD).date(), "c": c, "v": v}
                for t, c, v in zip(res["timestamp"], q["close"], q["volume"])
                if c is not None]
        return rows, res.get("meta", {}), url
    except Exception:
        return [], {}, url


def realised_vol_pct(rows, n=20):
    closes = [r["c"] for r in rows][-(n + 1):]
    if len(closes) < 3:
        return None
    rets = [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes))]
    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / max(1, len(rets) - 1)
    return round((var ** 0.5) * (252 ** 0.5) * 100, 2)


RESULTS_RE = re.compile("|".join(M.RESULTS_PATTERNS), re.I)
QUARTERLY_RE = re.compile("|".join(M.QUARTERLY_PATTERNS), re.I)
NOT_RESULTS_RE = re.compile("|".join(M.NOT_RESULTS_PATTERNS), re.I)


def classify(headline):
    """`results`, `quarterly_report`, or None. The exclusion is checked FIRST.

    A notice of a results date is not a result -- see M.NOT_RESULTS_PATTERNS for the
    two measured cases this rule exists for.
    """
    if NOT_RESULTS_RE.search(headline):
        return None
    if RESULTS_RE.search(headline):
        return "results"
    if QUARTERLY_RE.search(headline):
        return "quarterly_report"
    return None
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
STAMP_RE = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(\d{1,2}):(\d{2})\s*(am|pm)", re.I)


def announcements(code, year):
    """Every announcement the ASX holds for one issuer in one year.

    Returns [(date, minutes_since_midnight, headline)]. Empty means the fetch failed OR
    the issuer lodged nothing, and those are NOT the same -- the caller records which.
    """
    url = M.MARKET["confirm_issuer"].format(code=code, year=year)
    html = M.fetch(url, timeout=45).decode("utf-8", "replace")
    out = []
    for tr in ROW_RE.findall(html):
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip()
                 for c in CELL_RE.findall(tr)]
        if len(cells) < 3:
            continue
        m = STAMP_RE.match(cells[0])
        if not m:
            continue
        d = datetime.strptime(m.group(1), "%d/%m/%Y").date()
        hh, mm = int(m.group(2)), int(m.group(3))
        if m.group(4).lower() == "pm" and hh != 12:
            hh += 12
        if m.group(4).lower() == "am" and hh == 12:
            hh = 0
        out.append((d, hh * 60 + mm, cells[2]))
    return out, url


def session_of(minutes):
    if minutes < 600:
        return "bmo"
    if minutes < 960:
        return "in_session"
    return "amc"


def move_over(rows, sess, day):
    """The realised move over the window this announcement's session implies."""
    by_date = {r["d"]: r["c"] for r in rows}
    dates = sorted(by_date)
    if day not in by_date:
        nxt = [d for d in dates if d >= day]
        if not nxt:
            return None
        day = nxt[0]
    i = dates.index(day)
    if sess == "amc":
        a, b = i, i + 1
    else:
        a, b = i - 1, i
    if a < 0 or b >= len(dates):
        return None
    c0, c1 = by_date[dates[a]], by_date[dates[b]]
    if not c0:
        return None
    return {"date": day.isoformat(), "session": sess,
            "from_close": dates[a].isoformat(), "to_close": dates[b].isoformat(),
            "move_pct": round((c1 / c0 - 1) * 100, 2)}


def history(code, rows, event_date, years=3):
    """Prior results reactions, from the ASX's OWN announcement record.

    This is the thing Japan cannot have. Every row is a real lodgement with a real
    timestamp, so the session is measured rather than assumed and the window is the
    right one. A row is only kept when the narrow results classifier matches, so an
    Appendix 4G or a bare annual report lodged days after the numbers is not counted
    as a print.
    """
    ed = date.fromisoformat(event_date)
    events, sources, failures = [], [], []
    seen = set()
    for y in range(ed.year, ed.year - years, -1):
        anns, url = announcements(code, y)
        sources.append(url)
        if not anns:
            failures.append(y)
            continue
        for d, mins, head in anns:
            if d >= ed:
                continue
            kind = classify(head)
            if kind is None:
                continue
            # One print lodges several documents in the same few minutes; keep the
            # earliest per day, which is the one the market traded on.
            if d in seen:
                continue
            seen.add(d)
            mv = move_over(rows, session_of(mins), d)
            if not mv:
                continue
            mv.update({"announced_local": f"{mins // 60:02d}:{mins % 60:02d}",
                       "headline": head[:90], "basis": "observed", "kind": kind})
            events.append(mv)
    events.sort(key=lambda x: x["date"])
    moves = [abs(e["move_pct"]) for e in events]
    kinds = {k: sum(1 for e in events if e["kind"] == k)
             for k in ("results", "quarterly_report")}
    res_moves = [abs(e["move_pct"]) for e in events if e["kind"] == "results"]
    return {
        "n": len(events),
        "basis": "observed_announcement_dates",
        "years_searched": years,
        "years_that_returned_nothing": failures,
        "kinds": kinds,
        "filer_type": ("results" if kinds["results"] else
                       "quarterly_report_only" if kinds["quarterly_report"] else
                       "none_found"),
        "median_abs_move_pct": round(median(moves), 2) if moves else None,
        "median_abs_move_results_only_pct": (round(median(res_moves), 2)
                                             if res_moves else None),
        "events": events,
        "sources": sources,
        "caveat": ("Dates and timestamps are the ASX's own announcement record, so "
                   "these are real prints and may be cited as facts about a date -- "
                   "unlike researcher_japan, whose history is a cadence estimate. What "
                   "is still inferred is the CLASSIFIER: a results release whose "
                   "headline carries no results vocabulary is missed, which is the "
                   "Trustpilot failure mode stage EU measured. A year in "
                   "years_that_returned_nothing was not read, not a quiet year. "
                   "`filer_type` of quarterly_report_only means this issuer lodges an "
                   "Appendix 4C or 5B rather than a 4D or 4E -- a cash-flow statement, "
                   "not a profit result -- which is a different bar and is not a "
                   "missing print. `none_found` with no failed years is a reason to "
                   "doubt that a print is scheduled at all."),
    }


def lean_components(pos, runup):
    """What Australia prices that the run-up does not, each signed, in points.

    NONE OF THESE WEIGHTS IS MEASURED ON AUSTRALIAN DATA. They are the Japanese priors
    carried over, and they are kept as separate named components precisely so
    `au_resolve.py` can rank each one against the realised move and replace the priors
    with measurement. Do not defend the weights; replace them.

      short_squeeze   crowded short -> POSITIVE. The US run saw two shorts into names
                      with 18% and 23% of float short both squeeze more than 20%. A
                      crowded short is fuel, not a forecast.
      short_building  shorts ADDING into the print -> NEGATIVE. The closest thing this
                      market has to visible informed flow. It is four sessions stale,
                      so on a name that has already moved it may be describing history.
      runup           the US fallback, kept so the composite still contains what the
                      free control contains, but no longer ONLY that.

    The Japanese third component, 信用倍率, has no Australian equivalent and is absent
    rather than substituted. What compensates is that both components here come off an
    UNTRUNCATED register, so neither is a floor.
    """
    out = {}
    sr = (pos or {}).get("short_pct")
    sc = (pos or {}).get("short_change_pct_pts")
    out["short_squeeze"] = round(max(-3.0, min(3.0, 0.6 * sr)), 3) if sr is not None else None
    out["short_building"] = round(max(-2.0, min(2.0, -2.0 * sc)), 3) if sc is not None else None
    out["runup"] = round(-0.05 * runup, 3) if runup is not None else None
    return out


def build(name, event_date, short):
    code = name["ticker"]
    rows, meta, src_chart = bars(code)
    sess = name.get("session") or "bmo"
    doc = {
        "market": "AU",
        "ticker": code,
        "yahoo_symbol": M.yahoo_symbol(code),
        "company": name.get("company"),
        "sector": name.get("sector"),
        "event_date": event_date,
        "session": sess,
        "session_unresolved": bool(name.get("session_unresolved")),
        "session_source": name.get("session_source"),
        "window": name.get("window", {}).get("text"),
        "window_dates": name.get("window"),
        "vendor_date_kind": name.get("vendor_date_kind"),
        "event_date_basis": name.get("event_date_basis"),
        "sealed_utc": datetime.now(M.UTC).isoformat(timespec="seconds"),
        "sources": {"tape": src_chart,
                    "calendar": "TradingView public scanner, Sydney-shifted",
                    "announcements": M.MARKET["confirm_issuer"].format(code=code,
                                                                       year=event_date[:4]),
                    "short_register": POS.PAGE},
    }

    closes = [r["c"] for r in rows]
    spot = closes[-1] if closes else None
    win20, win5 = closes[-21:], closes[-6:]
    doc["tape"] = {
        "spot": round(spot, 4) if spot else None,
        "currency": meta.get("currency") or "AUD",
        "last_bar_date": rows[-1]["d"].isoformat() if rows else None,
        "run_up_20d_pct": round((win20[-1] / win20[0] - 1) * 100, 2) if len(win20) >= 2 else None,
        # Sealed for the same reason stage J seals it: on 4716 the 20-day window read
        # -0.42% while the five sessions into the print were +4.38%, and the hunter had
        # to rediscover the move off raw bars. It is deliberately NOT in
        # priced_lean_pct -- that would be a second helping of the run-up, and no
        # Australian measurement says which window belongs there. au_resolve.py ranks
        # it separately, as its own free control.
        "run_up_5d_pct": round((win5[-1] / win5[0] - 1) * 100, 2) if len(win5) >= 6 else None,
        "median_turnover_aud_20d": (name.get("tape") or {}).get("median_turnover_aud_20d"),
        "median_turnover_usd_20d": name.get("median_turnover_usd_20d"),
        "realised_vol_20d_pct": realised_vol_pct(rows, 20),
        "realised_vol_60d_pct": realised_vol_pct(rows, 60),
        "bars_3y": len(rows),
    }

    doc["options"] = {
        "event_implied_move_pct": None,
        "atm_spread_frac_of_mid": None,
        "skew_25d_vol_points": None,
        "reason": ("No ASX single-stock option chain is retrievable free from this "
                   "container. Measured 2026-09-22 on the repo's own authenticated "
                   "Yahoo path: AAPL 22 expiries, BHP.AX and CBA.AX zero. So there is "
                   "no event-implied move and no 25-delta skew, and `positioning` "
                   "below carries the substitute. This stage runs in the regime "
                   "archive/backtest/FINDINGS.md section 33 priced at rho=+0.073, "
                   "p=0.45 over 104 events."),
    }

    qs = (f"{M.YQ}/v10/finance/quoteSummary/{M.yahoo_symbol(code)}"
          f"?modules=earningsHistory&crumb={crumb()}")
    eh = get_json(qs, with_crumb=True)
    cons = []
    try:
        items = eh["quoteSummary"]["result"][0]["earningsHistory"]["history"]
    except Exception:
        items = []
    for it in items:
        cons.append({"period_end": (it.get("quarter") or {}).get("fmt"),
                     "eps_actual": (it.get("epsActual") or {}).get("raw"),
                     "eps_estimate": (it.get("epsEstimate") or {}).get("raw"),
                     "surprise_pct": (it.get("surprisePercent") or {}).get("raw")})
    doc["consensus"] = {"source": qs.split("&crumb=")[0], "quarters": cons,
                        "caveat": ("Australian sell-side coverage is thin below the "
                                   "ASX 200 and an empty list is common. It is not a "
                                   "signal.")}

    doc["history"] = history(code, rows, event_date)

    as_of, rows_reg, prev_as_of, prev_rows, lag = short
    pos = POS.for_code(code, rows_reg, prev_rows, as_of, prev_as_of, lag)
    doc["positioning"] = pos

    rv20 = doc["tape"]["realised_vol_20d_pct"]
    hist_med = doc["history"]["median_abs_move_pct"]
    vol_1d = round(rv20 / (252 ** 0.5), 2) if rv20 else None
    doc["expected_move"] = {
        "event_move_proxy_pct": max([x for x in (hist_med, vol_1d) if x is not None],
                                    default=None),
        "from_realised_vol_1d_pct": vol_1d,
        "from_history_median_pct": hist_med,
        "basis": ("the larger of (a) the median of OBSERVED prior reactions and (b) a "
                  "one-session move implied by 20-day realised volatility. It is NOT "
                  "an option-implied move: nothing is paying for it and it says "
                  "nothing about what the market expects from THIS print. It is a "
                  "scale for how far this name travels. Unlike stage J's, the history "
                  "half rests on real announcement dates."),
    }

    comps = lean_components(pos, doc["tape"]["run_up_20d_pct"])
    vals = [v for v in comps.values() if v is not None]
    doc["lean_components"] = comps
    doc["priced_lean_pct"] = round(sum(vals), 3) if vals else None
    doc["priced_lean_basis"] = (
        "Sum of the components above. Read au_priced_in.lean_components(): every "
        "weight is a PRIOR carried over from stage J, none is measured on Australian "
        "data, and au_resolve.py ranks each component separately so measurement can "
        "replace them. What matters today is only that this is not identical to "
        "-0.05 * run_up_20d_pct, so the free control is a real rival rather than the "
        "same number wearing two hats.")

    have_dir = sum(1 for k in ("short_squeeze", "short_building")
                   if comps.get(k) is not None)
    observed = doc["history"]["basis"] == "observed_announcement_dates" and doc["history"]["n"] > 0
    doc["anchor_quality"] = {
        # 0.55 where stage J pays 0.5 for the same two ingredients, because this
        # history is observed rather than estimated. Still capped well below 1.0: an
        # option-implied move off a tight two-sided chain beats all of it.
        "magnitude": (0.55 if (rv20 and observed) else
                      0.40 if (rv20 and hist_med) else
                      0.30 if (rv20 or hist_med) else 0.0),
        # Two components here earn nearly what three earn in Tokyo, because ASIC's
        # register is not truncated at 0.5% and Tokyo's third component is a scraped
        # broker number. Capped at 0.55 because neither is 25-delta skew.
        "direction": {0: 0.0, 1: 0.30, 2: 0.55}[have_dir],
        "basis": ("magnitude: realised vol plus an OBSERVED reaction history, capped "
                  "because neither is an option-implied move. direction: how many of "
                  "the two positioning components resolved off ASIC's untruncated "
                  "daily register, capped because neither is skew. The register is "
                  f"{pos.get('lag_sessions')} sessions stale and that is not "
                  "discounted here -- read it off positioning.lag_sessions."),
    }

    doc["event_occurred"] = None          # settled after the fact by au_resolve.py
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-history", action="store_true",
                    help="skip the ASX announcement archive (3 requests per name)")
    a = ap.parse_args()

    u = json.loads(Path(a.universe).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    short = POS.load(u.get("event_date"))
    if not short[1]:
        print("  WARNING: no ASIC short register could be read. positioning will be "
              "EMPTY, not zero, and the lean falls back to the run-up alone -- which "
              "is the free control, so the baseline would have no independent "
              "directional content at all. Say so in the note.")
    else:
        print(f"  ASIC register {short[0]}: {len(short[1])} products, "
              f"previous {short[2]}, lag {short[4]} sessions")

    made = 0
    for n in u.get("names", []):
        if a.no_history:
            doc = build(dict(n, _skip=True), u["event_date"], short)
            doc["history"] = {"n": 0, "basis": "skipped", "events": [],
                              "median_abs_move_pct": None}
        else:
            doc = build(n, u["event_date"], short)
        (out / f"{n['ticker']}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made += 1
        print(f"  sealed {n['ticker']:<6} {(doc['company'] or '')[:28]:<28} "
              f"spot={doc['tape']['spot']!s:<9} lean={doc['priced_lean_pct']!s:<7} "
              f"short={doc['positioning']['short_pct']}% "
              f"hist={doc['history']['n']} q={doc['anchor_quality']['direction']}")
    print(f"{made} baselines -> {out}")


if __name__ == "__main__":
    main()
