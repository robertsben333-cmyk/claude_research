#!/usr/bin/env python3
"""Seal what the market has already priced into each European name, before any hunt.

Same job as `researcher_us/scripts/priced_in.py` and `researcher_japan/scripts/
jp_priced_in.py`, and it writes the same shape, so `researcher_us/scripts/edge_score.py`
scores a European run unchanged and the three markets stay directly comparable. What
differs is what these markets will tell you.

THE OPTION ANCHOR DOES NOT EXIST HERE EITHER, AND THAT WAS THE HOPE
-------------------------------------------------------------------
Europe was expected to fix Japan's biggest hole. It does not. Measured in Phase 1:
Yahoo returns 21 expiries and 196 contracts for AAPL with a valid crumb and **zero
expiries and zero contracts** for SAP.DE, ADS.DE, BARC.L, MC.PA and BNP.PA. Eurex's
daily product-and-instrument reference file downloads cleanly (4.06 MB, HTTP 200) and
contains trading parameters, order profiles and price-range tables -- no settlement
prices, no open interest, no underlying ISIN map -- so no implied move can be computed
from it, and its market-statistics page is JavaScript with no JSON endpoint. Euronext's
derivatives pages return the SPA shell.

So `options` is written with every field `null` and a reason, and Europe runs in the
same anchor-less regime as Japan -- which is the regime that produced the worst number
in this repo: rho=+0.073, p=0.45 over 104 events on the sealed backtest corpus
(`backtest/FINDINGS.md` section 33). Nothing here refutes that. It makes it testable in
a third market, on a tail that is not truncated.

WHAT STANDS IN ITS PLACE, AND WHERE IT WORKS
--------------------------------------------
The Short Selling Regulation's 0.5% public threshold. The FCA register resolved on 89%
of the UK $1-5m-turnover cohort against 12% below $1m and 36-44% for Japan's JPX
register, so the substitute anchor is materially better here than in Tokyo -- in the UK
and Germany. **It is empty for France**, because www.data.gouv.fr is unreachable from
this container; see `eu_positioning.py`. A French name's `priced_lean_pct` therefore
falls back to the run-up, which is also the free control, and `eu_resolve.py` reports
`lean_vs_free_control_rho` PER MARKET so that reads as the near-1.0 it is instead of
being averaged away.

THE HISTORY ANCHOR IS REAL FOR THE UK AND ESTIMATED FOR THE OTHER TWO
----------------------------------------------------------------------
Japan has no retrievable history of announcement dates, so `jp_priced_in.py` applies
this quarter's notified lag backwards and labels every row `estimated`. The UK does not
have that problem: Investegate's per-company page lists real dated RNS announcements
going back years, so a UK name's `history` carries **observed** dates and the reaction
is read off the correct window around a date that is known to have carried a release.

Germany and France have no equivalent free archive -- EQS-News serves a non-paginating
snapshot of the live feed, and the Boerse Frankfurt `company_calendar` endpoint returns
`{}` for every ISIN tried -- so those two fall back to the Japanese method: step the
measured cadence gap backwards from the vendor's last release date and take the largest
move within +/-2 trading days. Every such row carries `basis: "estimated"`, the estimated
date, the date used and the gap between them. **It is a scale, not a record.** This repo
has already been burned reading a cadence prior as evidence -- TRT was ranked, traded
and never reported.

THE SESSION IS SEALED AND ITS UNCERTAINTY IS SEALED WITH IT
------------------------------------------------------------
339 of 379 measured UK results announcements landed before 08:00 London, so a European
name is `bmo` unless something says otherwise, and the window is close(D-1) -> close(D).
The vendor calls the session unknown for 150 of 318 German and 238 of 346 French rows;
windowing an unknown row as pre-market understates the move by roughly half, which is
what produced a spurious German maximum of 15.4% in Phase 1 where the correct window
gives 27.5%. `session_unresolved` rides in the baseline and the resolver measures both
windows for such a row rather than choosing one silently.

WHAT IS REAL AND SOURCED
------------------------
Spot, the run-ups, realised volatility and turnover are off the tape. EPS actual, EPS
estimate, the surprise percentage and the analyst count are Yahoo's own consensus
records, carried through unmodified with their source URL. The analyst count is in here
for a second reason: it is the measurable proxy for this stage's entire thesis, and
`eu_resolve.py` ranks the hunt's performance by coverage band so the thesis is tested
rather than assumed.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eu_positioning as POS                      # noqa: E402
from eu_market import MARKETS                     # noqa: E402

UTC = ZoneInfo("UTC")
YQ = "https://query1.finance.yahoo.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
IG_COMPANY = "https://www.investegate.co.uk/company/{code}"
_crumb = {"v": None}

# Same classifier the Phase 1 measurement used. It is deliberately loose: UK issuers
# headline results in marketing language often enough that a strict list misses them --
# Trustpilot's 2026 interims went out as "AI, Enterprise and US momentum fuel strong
# growth", with no results vocabulary at all. Six of the eight apparent calendar misses
# in Phase 1 were this classifier and not the calendar.
RESULTS_RE = re.compile(r"""(?ix)\b(
   interim\s+(results|report|accounts|management\s+statement)
  |half[-\s]?year(ly)?\s*(financial)?\s*(results|report|statement)
  |half[-\s]?yearly
  |final\s+(audited\s+)?results
  |preliminary\s+(results|announcement)
  |annual\s+(results|financial\s+report)
  |full[-\s]?year\s*(20\d\d\s*)?results
  |audited\s+results
  |(first|second|third|fourth|q[1-4]|1st|2nd|3rd|4th)[-\s]*quarter(ly)?\s*
      (results|report|update|statement|trading)
  |quarterly\s+(results|report|statement|update)
  |trading\s+(statement|update)
  |results\s+for\s+the\s+(year|period|half|six|three|nine|twelve)
 )\b""")
NOTICE_RE = re.compile(r"(?i)\bnotice\s+of\s+(results|interim|final|half)")


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def crumb():
    if _crumb["v"] is None:
        sh(f"curl -sS --max-time 20 -c /tmp/euyc.txt -H 'User-Agent: {UA}' "
           f"-o /dev/null https://fc.yahoo.com")
        _crumb["v"] = sh(f"curl -sS --max-time 20 -b /tmp/euyc.txt "
                         f"-H 'User-Agent: {UA}' '{YQ}/v1/test/getcrumb'").strip()
    return _crumb["v"]


def get_json(url, with_crumb=False, timeout=35):
    c = f"curl -sS --max-time {timeout} -H 'User-Agent: {UA}'"
    if with_crumb:
        c += " -b /tmp/euyc.txt"
    try:
        return json.loads(sh(f"{c} '{url}'"))
    except Exception:
        return None


def bars(symbol, rng="3y"):
    d = get_json(f"{YQ}/v8/finance/chart/{symbol}?range={rng}&interval=1d")
    try:
        r = d["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        out = []
        for i, t in enumerate(r["timestamp"]):
            c = q["close"][i]
            if c is None:
                continue
            out.append({"d": datetime.fromtimestamp(t, UTC).date(), "c": c,
                        "v": (q.get("volume") or [None] * len(r["timestamp"]))[i]})
        return out, r["meta"]
    except Exception:
        return [], {}


def move_for(rows, day, session):
    """The realised move over the window this stage ranks, for one known date.

    `bmo` is close(D-1) -> close(D) because the release lands before the open; `amc`
    is close(D) -> close(D+1). Getting this backwards roughly halves the number, which
    is why it is one function used by the baseline and the resolver alike.
    """
    ds = [r["d"] for r in rows]
    if day not in ds:
        return None
    i = ds.index(day)
    if session == "amc":
        if i + 1 >= len(rows):
            return None
        a, b = rows[i]["c"], rows[i + 1]["c"]
    else:
        if i < 1:
            return None
        a, b = rows[i - 1]["c"], rows[i]["c"]
    return round((b / a - 1) * 100, 2) if a else None


def reaction_near(rows, target, window=2):
    """Largest one-session move within +/-`window` trading days of an ESTIMATED date."""
    idx = [i for i, r in enumerate(rows) if r["d"] >= target]
    if not idx or idx[0] == 0:
        return None
    i0, best = idx[0], None
    for i in range(max(1, i0 - window), min(len(rows), i0 + window + 1)):
        if not rows[i - 1]["c"]:
            continue
        mv = (rows[i]["c"] / rows[i - 1]["c"] - 1) * 100
        if best is None or abs(mv) > abs(best[0]):
            best = (mv, rows[i]["d"])
    if best is None:
        return None
    return {"move_pct": round(best[0], 2), "date_used": best[1].isoformat(),
            "date_estimated": target.isoformat(),
            "days_from_estimate": (best[1] - target).days, "basis": "estimated"}


def uk_history(epic, rows, session, before, max_pages=4):
    """Real, dated past results announcements for a UK name, off Investegate.

    This is the one place Europe is better anchored than Tokyo. Japan cannot retrieve
    prior announcement dates at all; the UK publishes them and keeps them. A row here
    is a date on which a results announcement demonstrably went out, so the reaction is
    measured over the correct window around a known event rather than over a cadence
    guess.
    """
    out, seen = [], set()
    for pg in range(1, max_pages + 1):
        url = IG_COMPANY.format(code=epic) + (f"?page={pg}" if pg > 1 else "")
        html = sh(f"curl -sSL --max-time 30 -H 'User-Agent: {UA}' '{url}'")
        found = re.findall(
            r"<td>\s*(\d{1,2}\s+\w{3}\s+\d{4})[^<]*</td>.*?announcement-link\"[^>]*>"
            r"([^<]*)</a>", html, re.S)
        if not found:
            break
        for dtxt, head in found:
            if not RESULTS_RE.search(head) or NOTICE_RE.search(head):
                continue
            try:
                d = datetime.strptime(dtxt.strip(), "%d %b %Y").date()
            except ValueError:
                continue
            if d >= before or d in seen:
                continue
            seen.add(d)
            mv = move_for(rows, d, session)
            if mv is not None:
                out.append({"move_pct": mv, "date_used": d.isoformat(),
                            "headline": head.strip()[:80], "basis": "observed_rns"})
    out.sort(key=lambda x: x["date_used"])
    return out


def realised_vol_pct(rows, n=20):
    cl = [r["c"] for r in rows if r["c"]]
    if len(cl) < n + 1:
        return None
    rets = [cl[i] / cl[i - 1] - 1 for i in range(len(cl) - n, len(cl))]
    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
    return round((var ** 0.5) * (252 ** 0.5) * 100, 2)


def lean_components(positioning, runup):
    """The three things these markets price that the run-up does not, signed, in points.

    NONE OF THESE WEIGHTS IS MEASURED ON EUROPEAN DATA. They are the Japanese priors,
    which are themselves the US priors, and they are kept as separate named components
    precisely so `eu_resolve.py` can rank each one against the realised move and replace
    them with measurement. Do not defend the weights; replace them.

      short_squeeze   crowded disclosed short -> POSITIVE. The US run watched two shorts
                      into 18%- and 23%-of-float names both squeeze more than 20%.
      short_building  shorts ADDING into the print -> NEGATIVE. Sellers who must file
                      their names increasing a position days before results are the
                      closest thing to visible informed flow in these markets.
      runup           the fallback the US stage uses, kept so the composite still
                      contains what the free control contains -- but no longer only
                      that, except in France, where it IS only that.

    Japan's third component, 信用倍率, has no European analogue: there is no published
    margin long/short balance per name in any of the three. So Europe's lean rests on
    two independent components against Japan's three, and on ONE in France.
    """
    out = {}
    sr = (positioning or {}).get("short_ratio_pct")
    sc = (positioning or {}).get("short_change_pct_pts")
    out["short_squeeze"] = round(max(-3.0, min(3.0, 0.6 * sr)), 3) if sr is not None else None
    out["short_building"] = round(max(-2.0, min(2.0, -2.0 * sc)), 3) if sc is not None else None
    out["runup"] = round(-0.05 * runup, 3) if runup is not None else None
    return out


def build(name, event_date, registers):
    m = name["_market"]
    cfg = MARKETS[m]
    sym = name["yahoo_symbol"]
    session = name.get("session") or "bmo"
    rows, meta = bars(sym)
    src_chart = f"{YQ}/v8/finance/chart/{sym}?range=3y&interval=1d"
    ed = date.fromisoformat(event_date)

    doc = {
        "market": "EU",
        "submarket": m,
        "submarket_name": cfg["name"],
        "language": cfg["language"],
        "ticker": name["name"],
        "yahoo_symbol": sym,
        "tv_symbol": name.get("tv_symbol"),
        "company": name.get("description"),
        "industry": name.get("sector"),
        "event_date": event_date,
        "session": session,
        "session_unresolved": bool(name.get("session_unresolved")),
        "session_basis": name.get("session_basis"),
        "window": (f"close of the session before {event_date} -> {event_date} close"
                   if session == "bmo" else
                   f"{event_date} close -> next close"),
        "sealed_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "sources": {"tape": src_chart, "calendar": "TradingView public scanner",
                    "confirmation": cfg["confirm_name"]},
    }

    closes = [r["c"] for r in rows]
    w20, w5 = closes[-21:], closes[-6:]
    doc["tape"] = {
        "spot": round(closes[-1], 4) if closes else None,
        "currency": meta.get("currency"),
        "run_up_20d_pct": round((w20[-1] / w20[0] - 1) * 100, 2) if len(w20) >= 2 else None,
        "run_up_5d_pct": round((w5[-1] / w5[0] - 1) * 100, 2) if len(w5) >= 2 else None,
        "median_turnover_usd_20d": name.get("median_turnover_usd_20d"),
        "realised_vol_20d_pct": realised_vol_pct(rows, 20),
        "realised_vol_60d_pct": realised_vol_pct(rows, 60),
        "bars_3y": len(rows),
    }

    doc["options"] = {
        "event_implied_move_pct": None,
        "atm_spread_frac_of_mid": None,
        "skew_25d_vol_points": None,
        "reason": "No European single-stock option chain is retrievable from a free "
                  "source. Yahoo returns 0 expiries and 0 contracts for .L, .DE and .PA "
                  "symbols against 21 and 196 for AAPL on the same crumb; Eurex's daily "
                  "reference file carries trading parameters but no settlement prices, "
                  "no open interest and no underlying ISIN map, and its statistics page "
                  "is JavaScript with no JSON endpoint. So there is no event-implied "
                  "move and no skew, and this baseline supplies its own priced_lean_pct "
                  "and anchor_quality from the national short registers instead.",
    }

    qs = (f"{YQ}/v10/finance/quoteSummary/{sym}"
          f"?modules=earningsHistory%2CfinancialData&crumb={crumb()}")
    eh = get_json(qs, with_crumb=True)
    cons, analysts = [], None
    try:
        res = eh["quoteSummary"]["result"][0]
        for it in (res.get("earningsHistory") or {}).get("history") or []:
            cons.append({"period_end": (it.get("quarter") or {}).get("fmt"),
                         "eps_actual": (it.get("epsActual") or {}).get("raw"),
                         "eps_estimate": (it.get("epsEstimate") or {}).get("raw"),
                         "surprise_pct": (it.get("surprisePercent") or {}).get("raw")})
        analysts = ((res.get("financialData") or {})
                    .get("numberOfAnalystOpinions") or {}).get("raw")
    except Exception:
        pass
    band = ("unknown" if analysts is None else
            "<=2" if analysts <= 2 else "3-7" if analysts <= 7 else
            "8-13" if analysts <= 13 else ">13")
    doc["consensus"] = {
        "source": qs.split("&crumb=")[0], "quarters": cons,
        "analyst_count": analysts, "analyst_band": band,
        "basis": "Sell-side coverage, carried because it is the measurable proxy for "
                 "this stage's thesis. Phase 1 measured 1-2 analysts below $1m/day of "
                 "turnover, 5-7 at $1-5m, 11-13 at $5-25m and 16-19 above, consistently "
                 "across all three markets. eu_resolve.py ranks the hunt BY this band so "
                 "the thesis is tested rather than selected on.",
    }

    # --- history ------------------------------------------------------------------
    hist, hbasis, hsrc = [], None, None
    if m == "uk":
        hist = uk_history(name["name"], rows, session, ed)
        hbasis, hsrc = "observed_rns", IG_COMPANY.format(code=name["name"])
    if not hist:
        last, nxt = name.get("earnings_release_date"), name.get("earnings_release_next_date")
        gap = None
        if last and nxt and nxt > last:
            gap = (nxt - last) / 86400
        if last and gap and 60 <= gap <= 400 and rows:
            last_d = datetime.fromtimestamp(last, UTC).date()
            first_bar = rows[0]["d"]
            for k in range(0, 13):
                est = last_d - timedelta(days=int(round(gap * k)))
                if est >= ed or est <= first_bar:
                    continue
                r = reaction_near(rows, est)
                if r:
                    hist.append(r)
            hist.sort(key=lambda x: x["date_used"])
        hbasis = hbasis or "estimated_from_cadence"
        hsrc = hsrc or "TradingView last/next release dates, stepped backwards"
    moves = [abs(r["move_pct"]) for r in hist]
    doc["history"] = {
        "n": len(hist), "basis": hbasis, "source": hsrc,
        "median_abs_move_pct": round(median(moves), 2) if moves else None,
        "events": hist,
        "caveat": ("Dates are REAL: each row is a results announcement Investegate "
                   "records on that date, and the move is over this stage's own window."
                   if hbasis == "observed_rns" else
                   "Dates are ESTIMATED by stepping the measured cadence gap backwards "
                   "from the vendor's last release date; the move is the largest within "
                   "+/-2 trading days of that estimate. A cadence prior, not a record "
                   "that a print happened on that date. Use it as a SCALE for how far "
                   "this name travels, never as evidence about a particular past date -- "
                   "TRT was ranked, traded and never reported on exactly this mistake."),
    }

    doc["event_plausibility"] = {
        # Not "confirmed". The vendor calendar's measured phantom rate on the UK was
        # 2 of 90 rows over 20 sampled days -- far better than the US feed's 20 of 20
        # on one day, and not zero. One phantom every five days on a ten-name day.
        "verdict": "fits_cadence",
        "basis": "vendor forward calendar (TradingView), measured at a 2.2% phantom "
                 "rate on 90 UK rows against the RNS record. Confirmation against "
                 f"{cfg['confirm_name']} is eu_resolve.py's job, after the fact.",
        "calendar_source": "TradingView public scanner",
    }

    pos = POS.for_name(m, name.get("description"), registers)
    doc["positioning"] = pos

    rv20 = doc["tape"]["realised_vol_20d_pct"]
    hist_med = doc["history"]["median_abs_move_pct"]
    vol_1d = round(rv20 / (252 ** 0.5), 2) if rv20 else None
    doc["expected_move"] = {
        "event_move_proxy_pct": max([x for x in (hist_med, vol_1d) if x is not None],
                                    default=None),
        "from_realised_vol_1d_pct": vol_1d,
        "from_history_median_pct": hist_med,
        "basis": "the larger of (a) the median of this name's prior reactions and (b) a "
                 "one-session move implied by 20-day realised volatility. It is NOT an "
                 "option-implied move: nothing is paying for it and it carries no "
                 "information about what the market expects from THIS print. It is a "
                 "scale for how far this name travels. Phase 1 median realised move was "
                 "2.81% (UK), 3.12% (DE), 4.19% (FR) against Japan's 2.87%, with the "
                 "tail intact in all three -- 42%, 27% and 52% maxima and no price "
                 "limit to truncate them.",
    }

    comps = lean_components(pos, doc["tape"]["run_up_20d_pct"])
    vals = [v for v in comps.values() if v is not None]
    doc["lean_components"] = comps
    doc["priced_lean_pct"] = round(sum(vals), 3) if vals else None
    doc["priced_lean_basis"] = (
        "Sum of the components above. Read eu_priced_in.lean_components(): every weight "
        "is a PRIOR borrowed from the US runs, none is measured on European data, and "
        "eu_resolve.py ranks each component separately so measurement can replace them. "
        + ("FOR THIS NAME THE LEAN IS THE RUN-UP ALONE, because the national short "
           "register could not be read -- so the baseline's lean and the free control "
           "are the same number and the control cannot be beaten by anything using it."
           if not pos.get("covered") else
           "What matters is only that this is no longer identical to "
           "-0.05 * run_up_20d_pct, so the free control is a real rival again."))

    have_dir = sum(1 for k in ("short_squeeze", "short_building")
                   if comps.get(k) is not None)
    doc["anchor_quality"] = {
        "magnitude": 0.5 if (rv20 and hist_med) else (0.3 if (rv20 or hist_med) else 0.0),
        # Two components rather than Japan's three, because there is no European
        # 信用倍率 analogue, so the ceiling is lower: 0.45 against 0.60.
        "direction": {0: 0.0, 1: 0.25, 2: 0.45}[have_dir],
        "basis": "magnitude: realised vol plus a reaction history, capped at 0.5 because "
                 "neither is an option-implied move. direction: how many of the two "
                 "positioning components resolved, capped at 0.45 because neither is "
                 "25-delta skew and Europe has no margin-balance component to add.",
    }

    doc["event_occurred"] = None      # settled after the fact by eu_resolve
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-positioning", action="store_true",
                    help="skip the short registers entirely (the lean falls back to "
                         "the run-up for every name, which is also the free control)")
    a = ap.parse_args()

    u = json.loads(Path(a.universe).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    markets = sorted({n["_market"] for n in u.get("names", [])}) or u.get("markets", [])
    registers = {} if a.no_positioning else POS.load(tuple(markets))
    for m, r in registers.items():
        print(f"  register {m}: covered={r['covered']} as_of={r['as_of']} "
              f"rows={len(r.get('rows') or {})}")

    made = 0
    for n in u.get("names", []):
        doc = build(n, u["event_date"], registers)
        (out / f"{doc['submarket']}-{doc['ticker']}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made += 1
        print(f"  sealed {doc['submarket']}:{doc['ticker']:<8} "
              f"{(doc['company'] or '')[:26]:<26} spot={doc['tape']['spot']!s:<9} "
              f"sess={doc['session']}{'?' if doc['session_unresolved'] else ' '} "
              f"lean={doc['priced_lean_pct']!s:<7} "
              f"short={doc['positioning'].get('short_ratio_pct')} "
              f"hist={doc['history']['n']}({doc['history']['basis'][:8]}) "
              f"analysts={doc['consensus']['analyst_count']}")
    print(f"{made} baselines -> {out}")


if __name__ == "__main__":
    main()
