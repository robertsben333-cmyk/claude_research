#!/usr/bin/env python3
"""Seal what the Toronto market has already priced into each name, before any hunt.

Writes the same shape as `researcher_us/scripts/priced_in.py` and `jp_priced_in.py`, so
`researcher_us/scripts/edge_score.py` scores a Canadian run unchanged and the four
markets' numbers mean the same thing.

CANADA IS THE ONLY MARKET IN THIS REPO THAT RUNS TWO ANCHOR REGIMES AT ONCE, and that
is the whole reason the stage is worth building.

  anchor_covered: "options"   The Montreal Exchange lists this name and the chain is
                              two-sided right now. The baseline carries a real
                              event-implied move and a real ATM spread, so the shared
                              scorer takes its US path and this name is anchored exactly
                              as a US name is. 96% of names above $25m a day, 43% at
                              $1-5m, 10% below $1m.
  anchor_covered: "register"  No chain, or a chain with no live quotes. The baseline
                              supplies its own `priced_lean_pct` and `anchor_quality`
                              from the short register, which covers 87-88% of EVERY
                              turnover band -- the flattest positioning coverage in the
                              repo, against 32% for the FCA below $1m and 9-11 of 25 in
                              Japan.
  anchor_covered: "none"      Neither resolved. Carried, ranked, and reported apart.

`ca_resolve.py` ranks the arms separately. If the anchored arm ranks and the register
arm does not, that is the first direct evidence in this repo about whether the option
anchor is what stage E's result rests on -- `archive/backtest/FINDINGS.md` section 33
priced the anchor-less regime at rho=+0.073, p=0.45 over 104 events and could not
separate the anchor from the market it was measured in. Canada separates them inside one
day's names.

THREE THINGS THIS BASELINE DOES THAT NO OTHER STAGE'S DOES

1. THE OPTION-IMPLIED MOVE IS REFUSED UNLESS IT IS A QUOTE. Outside the Toronto session
   the Montreal chain's bid and ask are zeroes, and pricing an ATM straddle off `last`
   gave a median 12.5% "implied move" on names whose realised moves are nothing like
   that. A number priced off a stale mark is worse than no number, because the scorer
   weights the option term at 0.35 and would treat the noise as the best-known thing
   about the name. So `options.event_implied_move_pct` is written only from two-sided
   quotes; otherwise it is null with the reason and the name falls to the register arm.

2. THE REACTION HISTORY IS OBSERVED, NOT ESTIMATED. Japan has to infer prior
   announcement dates from a cadence because TDnet keeps 31 days. The TMX news archive
   goes back years and is ticker-keyed, so a Canadian history row is a real dated
   release with the realised move around it, carrying `basis: "observed"`. Read that
   difference before comparing `history.n` across the two markets.

3. THE REGISTER IS SNAPSHOTTED SO THE CHANGE EXISTS TOMORROW. `getCompanyShortInterest`
   has no date argument and no history, so the change in short interest -- the component
   Tokyo found most defensible -- cannot be computed on day one. Every run writes the
   day's readings to `researcher_canada/analysis/short-register/<date>.json`, and
   `short_change_pct_pts` resolves as soon as two runs exist. `BUSINESS_DATE` is carried
   into every baseline as well, so the open question of whether that feed refreshes
   daily or restamps CIRO's twice-monthly snapshot is answered by the accumulating files.
"""
import argparse
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_market as M                                   # noqa: E402
import ca_sources as CA                                 # noqa: E402

REPO = Path(__file__).resolve().parents[2]
REGISTER_DIR = REPO / "researcher_canada" / "analysis" / "short-register"


# --- tape -------------------------------------------------------------------------
def tape_rows(ticker, years=3):
    """TMX's own daily bars, oldest first. Preferred over Yahoo deliberately: Yahoo
    answered 429 to every CADUSD request during the 2026-09-22 build, and its European
    closes were measured a session stale, which is what forced `move_pending` on stage
    EU. This is the exchange's own tape for the exchange's own names."""
    end = date.today().isoformat()
    start = (date.today() - timedelta(days=int(365.25 * years))).isoformat()
    rows = CA.bars(ticker, start, end) or []
    out = []
    for r in rows:
        c = r.get("close")
        if c is None:
            continue
        v = r.get("volume")
        out.append({"d": (r.get("dateTime") or "")[:10], "c": c, "o": r.get("open"),
                    "v": v, "tv": (c * v) if v else None})
    out.sort(key=lambda x: x["d"])
    return out


def realised_vol_pct(rows, n=20):
    cl = [r["c"] for r in rows if r["c"]]
    if len(cl) < n + 1:
        return None
    rets = [(cl[i] / cl[i - 1] - 1.0) for i in range(len(cl) - n, len(cl))]
    mu = sum(rets) / len(rets)
    var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
    return round((var ** 0.5) * (252 ** 0.5) * 100, 2)


def move_around(rows, target, window=1):
    """The close-to-close move on the session that reacts to a release on `target`.

    Unlike Japan's `reaction_near` this is not hunting for a date: the date is known
    from the archive. The window exists only because an after-hours release reacts the
    NEXT session and a pre-open one reacts the same session."""
    idx = [i for i, r in enumerate(rows) if r["d"] >= target]
    if not idx or idx[0] == 0:
        return None
    best = None
    for i in range(max(1, idx[0]), min(len(rows), idx[0] + window + 1)):
        prev, cur = rows[i - 1], rows[i]
        if not prev["c"]:
            continue
        mv = (cur["c"] / prev["c"] - 1.0) * 100.0
        if best is None or abs(mv) > abs(best[0]):
            best = (mv, cur["d"])
    if not best:
        return None
    return {"move_pct": round(best[0], 2), "date_used": best[1],
            "announced": target, "basis": "observed"}


# --- the option arm ----------------------------------------------------------------
def option_anchor(ticker, event_date, spot):
    """A real event-implied move, or an honest refusal.

    Returns (options_block, lean_from_options). The lean is the ATM call/put price
    asymmetry rather than 25-delta skew: the Montreal chain publishes prices and open
    interest but no implied volatilities, so a real skew is not computable from it. The
    asymmetry is the same idea one level cruder -- if the ATM put is richer than the
    ATM call at the same strike, the market is paying more for the downside."""
    empty = {"event_implied_move_pct": None, "atm_spread_frac_of_mid": None,
             "skew_25d_vol_points": None}
    try:
        rows = CA.option_chain(ticker)
    except Exception as exc:
        empty["reason"] = f"Montreal Exchange chain not readable: {exc}"
        return empty, None
    if not rows:
        empty["reason"] = ("No listed options at the Montreal Exchange for this "
                           "underlying. 360 of about 2,500 Canadian listings have a "
                           "chain, and coverage falls from 96% above $25m a day to 10% "
                           "below $1m, so an absent chain is the normal case in the band "
                           "this stage is for.")
        return empty, None
    later = sorted({r["expiry"] for r in rows if r["expiry"] > event_date})
    if not later or not spot:
        empty["reason"] = "chain read but no expiry after the event date"
        return empty, None
    exp = later[0]
    ring = [r for r in rows if r["expiry"] == exp]
    atm = min(ring, key=lambda r: abs((r["strike"] or 1e9) - spot))
    cb, ca_, pb, pa = atm["call_bid"], atm["call_ask"], atm["put_bid"], atm["put_ask"]
    two_sided = all(x for x in (cb, ca_, pb, pa))
    if not two_sided:
        empty["reason"] = (
            f"chain found ({len(ring)} strikes on {exp}) but the ATM bid/ask is not "
            f"two-sided, so the only price available is `last`. A straddle priced off a "
            f"stale mark gave a median 12.5% implied move on the 2026-09-22 sample and "
            f"the scorer weights this term at 0.35 -- a wrong anchor is worse than none. "
            f"Seal during the Toronto session (09:30-16:00 ET) to get this number.")
        empty["chain_present"] = True
        empty["expiry"] = exp
        empty["atm_strike"] = atm["strike"]
        empty["atm_open_interest"] = (atm["call_oi"] or 0) + (atm["put_oi"] or 0)
        return empty, None
    cmid, pmid = (cb + ca_) / 2, (pb + pa) / 2
    straddle = cmid + pmid
    spread = ((ca_ - cb) + (pa - pb)) / 2
    lean = round(((cmid - pmid) / spot) * 100.0, 3)
    return {
        "event_implied_move_pct": round(100 * straddle / spot, 2),
        "atm_spread_frac_of_mid": round(spread / straddle, 3) if straddle else None,
        "skew_25d_vol_points": None,
        "expiry": exp, "atm_strike": atm["strike"],
        "atm_open_interest": (atm["call_oi"] or 0) + (atm["put_oi"] or 0),
        "days_past_event": (date.fromisoformat(exp) - date.fromisoformat(event_date)).days,
        "source": f"{CA.MX}/quotes?symbol={ticker}*",
        "basis": ("ATM straddle at the first expiry after the print, off two-sided "
                  "quotes. It spans the option's whole remaining life, so it is an "
                  "UPPER BOUND on the event's share and not a clean earnings implied "
                  "move; de-trending it is unbuilt work. `skew_25d_vol_points` is null "
                  "because the exchange publishes prices and open interest but no "
                  "implied volatilities."),
    }, lean


# --- the register arm ---------------------------------------------------------------
def register_snapshot_path(d):
    return REGISTER_DIR / f"{d}.json"


def previous_register(before):
    """The most recent stored register snapshot before `before`, or (None, None)."""
    if not REGISTER_DIR.exists():
        return None, None
    files = sorted(p for p in REGISTER_DIR.glob("*.json") if p.stem < before)
    if not files:
        return None, None
    try:
        return files[-1].stem, json.loads(files[-1].read_text())
    except Exception:
        return None, None


def lean_components(short_pct, short_change, dtc, analysts, runup, option_lean):
    """What Toronto prices that the run-up does not, each signed, in points.

    NONE OF THESE WEIGHTS IS MEASURED ON CANADIAN DATA. They are priors carried over
    from stage J, where the same argument produced them, and `ca_resolve.py` ranks each
    component separately against the realised move so measurement can replace them. Do
    not defend a weight; replace it.

      option_lean     ATM call richer than ATM put -> POSITIVE. The only component here
                      that is a price rather than a position, so when it resolves it
                      dominates by design.
      short_squeeze   crowded short -> POSITIVE. A crowded short is fuel, not a forecast.
      short_building  shorts ADDING into the print -> NEGATIVE. Null until two runs have
                      stored a register snapshot; see the module docstring.
      days_to_cover   a position that takes many days to cover -> POSITIVE, same idea as
                      short_squeeze but scaled by liquidity rather than by float.
      analyst_gap     a large gap to the consensus price target -> NEGATIVE. This is the
                      weakest prior in the set and the first to drop: it is an argument
                      about sell-side optimism, not an observation of positioning.
      runup           kept so the composite still CONTAINS what the free control
                      contains, which is what makes `lean_vs_free_control_rho` in the
                      resolved file meaningful. If that number climbs back to 1.0 the
                      other components have stopped resolving and the lean has silently
                      become the run-up again.
    """
    out = {}
    out["option_lean"] = round(max(-3.0, min(3.0, 2.0 * option_lean)), 3) \
        if option_lean is not None else None
    out["short_squeeze"] = round(max(-3.0, min(3.0, 0.6 * short_pct)), 3) \
        if short_pct is not None else None
    out["short_building"] = round(max(-2.0, min(2.0, -2.0 * short_change)), 3) \
        if short_change is not None else None
    out["days_to_cover"] = round(max(0.0, min(2.0, 0.25 * math.log10(1 + dtc))), 3) \
        if dtc else None
    up = (analysts or {}).get("priceTarget", {}).get("priceTargetUpside") \
        if analysts else None
    out["analyst_gap"] = round(max(-1.5, min(1.5, -0.02 * up)), 3) if up is not None else None
    out["runup"] = round(-0.05 * runup, 3) if runup is not None else None
    return out


# --- build --------------------------------------------------------------------------
def build(name, universe, register_today, prev_as_of, prev_register):
    t = name["ticker"]
    event_date = name.get("event_date") or universe["event_date"]
    session = name.get("session") or "amc"
    w0, w1 = M.window(event_date, session)

    rows = tape_rows(t)
    closes = [r["c"] for r in rows]
    spot = closes[-1] if closes else None
    turns = sorted(r["tv"] for r in rows[-20:] if r.get("tv")) or []

    doc = {
        "market": "CA",
        "ticker": t,
        "company": name.get("company"),
        "exchange": name.get("exchange"),
        "sector": name.get("sector"),
        "event_date": event_date,
        "session": session,
        "session_unresolved": bool(name.get("session_unresolved")),
        "window": f"close {w0} -> close {w1} ({session})",
        "sealed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {"tape": "getCompanyPriceHistory via app-money.tmx.com",
                    "options": f"{CA.MX}/quotes",
                    "register": "getCompanyShortInterest via app-money.tmx.com",
                    "archive": "getNewsForSymbol via app-money.tmx.com"},
    }

    doc["tape"] = {
        "spot": round(spot, 4) if spot else None,
        "currency": name.get("currency") or "CAD",
        "run_up_20d_pct": round((closes[-1] / closes[-21] - 1) * 100, 2) if len(closes) >= 21 else None,
        "run_up_5d_pct": round((closes[-1] / closes[-6] - 1) * 100, 2) if len(closes) >= 6 else None,
        "median_turnover_cad_20d": int(turns[len(turns) // 2]) if turns else None,
        "turnover_usd_20d": name.get("turnover_usd"),
        "realised_vol_20d_pct": realised_vol_pct(rows, 20),
        "realised_vol_60d_pct": realised_vol_pct(rows, 60),
        "bars": len(rows),
        "last_bar": rows[-1]["d"] if rows else None,
    }

    # --- the option arm
    opts, option_lean = option_anchor(t, event_date, spot)
    doc["options"] = opts

    # --- observed reaction history, off the archive
    try:
        news = CA.news_pages(t, pages=3, limit=100)
    except Exception:
        news = []
    # "AGF Management Limited to Release Third Quarter 2026 Financial Results" is a
    # financial headline and is NOT a print. Counting it as one puts a reaction on the
    # day the company announced its date, which is a day nothing happened.
    fin = [n for n in news
           if M.is_financial_headline(n.get("headline"))
           and not M.ANNOUNCEMENT_HEADLINE.search(n.get("headline") or "")]
    hist, seen = [], set()
    for n in fin:
        d = (n.get("datetime") or "")[:10]
        if not d or d in seen or d >= event_date:
            continue
        seen.add(d)
        mv = move_around(rows, d)
        if mv:
            mv["headline"] = (n.get("headline") or "")[:120]
            mv["source"] = n.get("source")
            hist.append(mv)
        if len(hist) >= 12:
            break
    hist.sort(key=lambda x: x["announced"])
    moves = [abs(h["move_pct"]) for h in hist]
    doc["history"] = {
        "n": len(hist), "basis": "observed", "news_rows_read": len(news),
        "median_abs_move_pct": round(median(moves), 2) if moves else None,
        "events": hist,
        "caveat": ("Dates are REAL: each row is a dated financial-results release from "
                   "the TMX news archive, not a cadence estimate. The move is the larger "
                   "of the release session and the one after it, because an after-hours "
                   "release reacts the next day. The headline classifier excludes drill "
                   "and assay results, which is the single most common false positive on "
                   "the TSXV."),
    }

    # --- the register arm
    si = register_today.get(t)
    prev = (prev_register or {}).get(t)
    short_pct = (si or {}).get("SHORTINTERESTPCT")
    short_pct = round(short_pct * 100, 3) if short_pct is not None else None
    prev_pct = (prev or {}).get("SHORTINTERESTPCT")
    prev_pct = round(prev_pct * 100, 3) if prev_pct is not None else None
    change = round(short_pct - prev_pct, 3) if (short_pct is not None and prev_pct is not None) else None
    try:
        an = CA.analysts(t)
    except Exception:
        an = None
    doc["positioning"] = {
        "short_interest_shares": (si or {}).get("SHORT_INTEREST"),
        "short_ratio_pct": short_pct,
        "days_to_cover_30d": (si or {}).get("DAYSTOCOVER30DAY"),
        "register_business_date": (si or {}).get("BUSINESS_DATE"),
        "short_change_pct_pts": change,
        "short_change_vs": prev_as_of,
        "analysts": an,
        "analyst_band": ("none" if not an or not an.get("totalAnalysts") else
                         "1-2" if an["totalAnalysts"] <= 2 else
                         "3-7" if an["totalAnalysts"] <= 7 else
                         "8-15" if an["totalAnalysts"] <= 15 else "16+"),
        "basis": ("CIRO's consolidated short position, served by TMX because ciro.ca is "
                  "0 of 8 from this container. There is NO history endpoint and no date "
                  "argument, so `short_change_pct_pts` is null until two runs have stored "
                  "a snapshot, and `register_business_date` is carried so the question of "
                  "how often that feed moves is settled by the accumulating files. There "
                  "is also NO EPS consensus anywhere in this API: the bar this print will "
                  "be judged against is not in this baseline and the hunter has to source "
                  "it."),
    }

    # --- expected move
    rv20 = doc["tape"]["realised_vol_20d_pct"]
    hist_med = doc["history"]["median_abs_move_pct"]
    vol_1d = round(rv20 / (252 ** 0.5), 2) if rv20 else None
    im = opts.get("event_implied_move_pct")
    doc["expected_move"] = {
        "event_move_proxy_pct": im or max([x for x in (hist_med, vol_1d) if x is not None],
                                          default=None),
        "from_option_implied_pct": im,
        "from_history_median_pct": hist_med,
        "from_realised_vol_1d_pct": vol_1d,
        "basis": ("the option-implied move where the chain quotes two-sided, otherwise "
                  "the larger of an observed reaction history and a one-session move "
                  "implied by 20-day realised vol. The fallbacks are a SCALE for how far "
                  "this name travels and carry no information about this print."),
    }

    # --- the lean
    comps = lean_components(short_pct, change, doc["positioning"]["days_to_cover_30d"],
                            an, doc["tape"]["run_up_20d_pct"], option_lean)
    vals = [v for v in comps.values() if v is not None]
    doc["lean_components"] = comps
    if im is not None:
        # The chain quoted. Let the shared scorer take its own US path rather than
        # overriding it: `priced_lean_pct` is left unset so edge_score.priced_lean_pct()
        # falls through to its option branch, which is the better-measured code path.
        doc["lean_components_note"] = (
            "Computed and carried for the resolver, but NOT written to priced_lean_pct: "
            "this name has a two-sided chain, so the shared scorer uses its own option "
            "path and the arms stay comparable with stage E.")
    else:
        doc["priced_lean_pct"] = round(sum(vals), 3) if vals else None
        doc["priced_lean_basis"] = (
            "Sum of lean_components. Every weight is a PRIOR carried over from stage J "
            "and none is measured on Canadian data; ca_resolve.py ranks each component "
            "separately so they can be replaced by measurement. What matters today is "
            "that it is not identical to -0.05 * run_up_20d_pct, so the free control is "
            "a real rival rather than the baseline's own number.")

    # --- how anchored is this name
    have_dir = sum(1 for k in ("short_squeeze", "short_building", "days_to_cover",
                               "analyst_gap") if comps.get(k) is not None)
    doc["anchor_covered"] = ("options" if im is not None else
                             "register" if short_pct is not None else "none")
    doc["anchor_quality"] = {
        "magnitude": 0.5 if (rv20 and hist_med) else (0.3 if (rv20 or hist_med) else 0.0),
        "direction": {0: 0.0, 1: 0.2, 2: 0.35, 3: 0.5, 4: 0.6}[have_dir],
        "basis": ("Read by the shared scorer ONLY when there is no option-implied move. "
                  "magnitude is capped at 0.5 because an observed reaction history plus "
                  "realised vol is still not an option price; direction at 0.6 because "
                  "none of the four components is 25-delta skew."),
    }

    # --- how much do we believe the date
    conf = name.get("date_confidence")
    doc["event_plausibility"] = {
        "verdict": {"confirmed": "fits_cadence", "agreed": "fits_cadence",
                    "wsh_only": "unknown", "vendor_only": "unknown",
                    "disputed": "suspect"}.get(conf, "unknown"),
        "date_confidence": conf,
        "vendor_date": name.get("tv_date"),
        "wsh": name.get("wsh"),
        "issuer_announced": name.get("announced"),
        "event_shape": name.get("event_shape"),
        "basis": ("Two calendars that disagree on 172 of 277 forward dates, reconciled "
                  "in ca_universe.py. `confirmed` is Wall Street Horizon's own CON flag, "
                  "which no other calendar in this repo carries."),
    }
    doc["event_occurred"] = None          # settled after the fact by ca_resolve.py
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-register-write", action="store_true",
                    help="do not store today's register snapshot (for replays)")
    a = ap.parse_args()

    u = json.loads(Path(a.universe).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    names = u.get("names", [])
    if not names:
        print("  no names in the universe; nothing to seal")
        return

    today = date.today().isoformat()
    register = {}
    for n in names:
        try:
            si = CA.short_interest(n["ticker"])
        except Exception:
            si = None
        # The endpoint returns a row of nulls rather than nothing for a name it does
        # not cover, so an all-null row has to be treated as absent or 10% of the
        # universe would look anchored when it is not.
        if si and si.get("SHORT_INTEREST") is not None:
            register[n["ticker"]] = si
    print(f"  short register: {len(register)}/{len(names)} names read"
          + (f", business date "
             f"{sorted({v.get('BUSINESS_DATE') or '?' for v in register.values()})}"
             if register else ""))
    prev_as_of, prev = previous_register(today)
    if prev_as_of:
        print(f"  previous snapshot {prev_as_of}: change in short interest is computable")
    else:
        print("  no earlier snapshot: short_change_pct_pts will be null on every name")
    if register and not a.no_register_write:
        REGISTER_DIR.mkdir(parents=True, exist_ok=True)
        register_snapshot_path(today).write_text(
            json.dumps(register, indent=1) + "\n", encoding="utf-8")

    made = 0
    for n in names:
        doc = build(n, u, register, prev_as_of, prev)
        (out / f"{n['ticker']}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        made += 1
        print(f"  sealed {n['ticker']:<9} anchor={doc['anchor_covered']:<9} "
              f"spot={doc['tape']['spot']!s:<9} "
              f"im={doc['options']['event_implied_move_pct']!s:<6} "
              f"short={doc['positioning']['short_ratio_pct']!s:<6} "
              f"lean={doc.get('priced_lean_pct')!s:<7} hist={doc['history']['n']}")
    print(f"{made} baselines -> {out}")


if __name__ == "__main__":
    main()
