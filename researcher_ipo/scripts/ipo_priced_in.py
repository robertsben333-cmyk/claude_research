#!/usr/bin/env python3
"""Seal what is already known about each of the day's IPO events, before any hunter.

    python3 researcher_ipo/scripts/ipo_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines

One JSON per name. Code writes it and nothing downstream may revise it, except the
retrospective `event_occurred: false` (a debut that did not trade that day, a lock-up
that had already been released early), which the resolver or a person adds with its
source in `event_occurred_note`.

WHAT A DEBUT BASELINE CARRIES
  the deal (offer price or range, shares, secondary share, size, exchange, lock-up and
  quiet-period dates, CIK), the regime of RECENT DEBUTS measured on the same window
  (first trade -> day-1 close, and the pop to the open beside it), the issuer's filings
  and a set of full-text probes into its own prospectus. There is no option chain, no
  short interest and no tape: the scale is the recent-debut distribution, and the
  baseline says so in `anchor_quality`.

WHAT A LOCK-UP BASELINE CARRIES
  the deal and the lock-up terms, the tape (spot, price versus offer, 5/20-day run-up,
  20-day turnover, the open-to-close standard deviation that sizes this window), the
  overhang (shares outstanding against shares sold), short interest with its lag,
  insider trades, the filings since the IPO (a follow-on or an 8-K before the date is
  usually an early release) and probes for early-release and waiver language.

Nothing here is a forecast. Nothing here places an order.
"""
import argparse
import json
import statistics as st
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ipo_market as IM                                           # noqa: E402
sys.path.insert(0, str(IM.REPO / "researcher_reversal" / "scripts"))
import rev_forward as RF                                          # noqa: E402

DEBUT_PROBES = [
    ("cornerstone", '"indicated an interest in purchasing"',
     "named investors who asked for an allocation before pricing: demand the book already "
     "had, and often a sign the deal was covered before the roadshow ended"),
    ("directed_share_program", '"directed share program"',
     "shares reserved for employees and friends; small, and they are not locked up the same way"),
    ("controlled_company", '"controlled company"',
     "the founder or sponsor keeps control; governance discount and a large future supply"),
    ("dual_class", '"Class B common stock"',
     "a second voting class; the free float may be a small slice of the company"),
    ("material_weakness", '"material weakness"',
     "the auditor found a control failure; common in small IPOs, it shows up in the first 10-Q"),
    ("going_concern", '"substantial doubt about its ability to continue"',
     "the IPO money is what keeps the company alive"),
]
LOCKUP_PROBES = [
    ("early_release", '"early release"',
     "a staged release tied to an earnings date or a price trigger moves the real date"),
    ("lockup", '"lock-up"',
     "where the terms live: the 424B4, a follow-on prospectus, an 8-K amending them"),
    ("waiver", '"waive"',
     "the underwriters waived the lock-up for some holders, usually to run a follow-on"),
    ("registration_rights", '"registration rights"',
     "holders who can force a registered sale once the lock-up ends"),
]


def debut_regime(day, lookback_days=90):
    """The recent debuts on the same window, from the calendar and the tape."""
    start = day - timedelta(days=lookback_days)
    months = sorted({(start + timedelta(days=i)).strftime("%Y-%m") for i in range(0, lookback_days + 1, 10)}
                    | {day.strftime("%Y-%m")})
    rows = []
    for d in IM.priced_deals(months):
        if d["spac"] or not d["ticker"] or not (start <= d["priced_date"] < day):
            continue
        if (d["deal_usd"] or 0) < float(IM.cfg().get("min_deal_usd", 25e6)):
            continue
        bs = IM.bars(d["ticker"], rg="6mo")
        if not bs:
            continue
        b0 = bs[0]
        lag = (date.fromisoformat(b0["date"]) - d["priced_date"]).days
        if not (0 <= lag <= 7) or b0["date"] >= day.isoformat():
            continue
        offer = d["price_high"] if d["price_high"] == d["price_low"] else None
        ro = b0["open"] * (b0["raw_close"] / b0["close"]) if b0["close"] else None
        rows.append({"ticker": d["ticker"], "first_trade": b0["date"], "deal_usd": d["deal_usd"],
                     "key_move_pct": IM.pct(b0["open"], b0["close"]),
                     "pop_pct": IM.pct(offer, ro) if offer else None})

    def summ(xs):
        xs = [x for x in xs if x is not None]
        if not xs:
            return {"n": 0}
        return {"n": len(xs), "median": round(st.median(xs), 2), "mean": round(st.mean(xs), 2),
                "median_abs": round(st.median([abs(x) for x in xs]), 2),
                "sd": round(st.stdev(xs), 2) if len(xs) > 1 else None,
                "share_up": round(sum(x > 0 for x in xs) / len(xs), 2)}
    last30 = (day - timedelta(days=30)).isoformat()
    return {"lookback_days": lookback_days,
            "window": "first trade (day-1 open) -> day-1 close",
            "key_move_pct": summ([r["key_move_pct"] for r in rows]),
            "key_move_pct_last_30d": summ([r["key_move_pct"] for r in rows if r["first_trade"] >= last30]),
            "pop_pct": summ([r["pop_pct"] for r in rows]),
            "debuts": sorted(rows, key=lambda r: r["first_trade"], reverse=True)[:15],
            "source": "api.nasdaq.com/api/ipo/calendar + Yahoo daily bars"}


def phase0():
    p = IM.REPO / "researcher_ipo" / "analysis" / "phase0-base-rates.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    keep = {}
    for ev in ("debut", "lockup"):
        b = d.get(ev) or {}
        keep[ev] = {k: b.get(k) for k in ("window", "key_move_pct", "key_excess_pct", "pop_pct",
                                          "by_pop", "by_vs_offer", "by_deal_size", "by_locked_share",
                                          "free_rankers_vs_key") if b.get(k) is not None}
    keep["generated_utc"] = d.get("generated_utc")
    keep["source"] = "researcher_ipo/analysis/phase0-base-rates.json"
    return keep


def deal_block(n, ov):
    so = IM.money(ov.get("SharesOutstanding"))
    sh = n.get("shares_offered") or IM.money(ov.get("SharesOffered"))
    sec = IM.money(ov.get("ShareholderSharesOffered"))
    return {"deal_id": n["deal_id"], "exchange": n["exchange"], "cik": ov.get("SECCIK"),
            "offer_price": n.get("offer_price"), "price_range": n.get("price_range"),
            "offer_price_final": n.get("offer_price_final", True),
            "shares_offered": sh, "secondary_shares_offered": sec,
            "secondary_share_of_deal": round(sec / sh, 3) if sec and sh else None,
            "over_allotment": ov.get("SharesOverAllotment"),
            "deal_usd": n.get("deal_usd"),
            "shares_outstanding_after": so,
            "float_share_at_ipo": round(sh / so, 3) if so and sh and so > sh else None,
            "lockup_days": ov.get("LockupPeriodNumberofDays"),
            "lockup_expiration": ov.get("LockupPeriodExpirationDate"),
            "quiet_period_expiration": ov.get("QuietPeriodExpirationDate"),
            "employees": ov.get("NumberOfEmployees"),
            "state_of_incorporation": ov.get("StateOfInc"),
            "description": (ov.get("_description") or "")[:900],
            "source": IM.OVERVIEW.format(d=n["deal_id"])}


def edgar_block(cik, probes, window_days, day):
    """Filings and probes, CUT AT THE EVENT DATE. A live run seals before the session so
    the cut removes nothing; a validation or backfill run on a past date would otherwise
    hand the hunter filings made after the event. The probes' `hits_ever` counts come
    from the index and cannot be cut, so a past-date run says so."""
    try:
        c = int(str(cik).lstrip("0") or 0) if cik else None
    except ValueError:
        c = None
    if not c:
        return {"status": "no_cik"}
    cut = day.isoformat()
    since = window_days + max(0, (date.today() - day).days)
    f = RF.filings(c, since_days=since, keep=80)
    fl = [x for x in (f.get("filings") or []) if x["filed"] < cut]
    counts, latest = {}, {}
    for x in fl:
        counts[x["form"]] = counts.get(x["form"], 0) + 1
        latest.setdefault(x["form"], x["filed"])
    pr = RF.text_probes(c, probes=probes, window_days=since)
    for v in pr.values():
        hits = [h for h in v.get("recent_hits") or [] if (h.get("filed") or "") < cut]
        v["recent_hits"] = hits
        v["most_recent"] = hits[0]["filed"] if hits else None
    out = {"status": f.get("status"), "cik": c, "sic_description": f.get("sic_description"),
           "cut_at": cut, "form_counts": counts, "latest_by_form": latest,
           "filings": fl[:20], "probes": pr, "source": f.get("source")}
    if day < date.today():
        out["past_date_note"] = ("sealed after the event date: filings and probe hits are cut at "
                                 "it, but each probe's hit COUNTS come from today's index")
    return out


def seal_debut(n, day, regime, p0):
    ov = IM.overview(n["deal_id"], max_age_h=1)
    b = {"ticker": n["ticker"], "company": n["company"], "event_type": "debut", "session": "debut",
         "event_date": day.isoformat(),
         "window": {"from": "first trade on " + day.isoformat() + " (the opening cross)",
                    "to": "close of " + day.isoformat()},
         "spot": None, "spot_note": "no tape before the first trade; the window starts at it",
         "deal": deal_block(n, ov),
         "recent_debuts": regime,
         "phase0": p0,
         "edgar": edgar_block(ov.get("SECCIK") or n.get("cik"), DEBUT_PROBES, 400, day),
         # The scale is the recent-debut distribution, not this name's own: magnitude is
         # thin and direction is close to absent. edge_score reads this into diagnostics.
         "anchor_quality": {"magnitude": 0.35, "direction": 0.0},
         "history": {"n": 0, "basis": "a debut has no reaction history"}}
    return b


def seal_lockup(n, day, p0):
    ov = IM.overview(n["deal_id"], max_age_h=24)
    bs = IM.bars(n["ticker"], rg="1y")
    prev = IM.bars_before(bs, day)
    last = prev[-1] if prev else None
    oc = [IM.pct(x["open"], x["close"]) for x in prev[-20:]]
    oc = [x for x in oc if x is not None]
    si = RF.short_interest(n["ticker"])
    ins = RF.insiders(n["ticker"])
    b = {"ticker": n["ticker"], "company": n["company"], "event_type": "lockup", "session": "lockup",
         "event_date": day.isoformat(),
         "window": {"from": "open of " + day.isoformat(), "to": "close of " + day.isoformat()},
         "spot": round(last["raw_close"], 4) if last else None,
         "spot_date": last["date"] if last else None,
         "spot_note": "the last close; the window opens at the next open, so the gap is not scored",
         "deal": deal_block(n, ov),
         "lockup": {"priced_date": n["priced_date"], "days": n["lockup_days"],
                    "expiration_date": n["expiration_date"], "basis": n["lockup_basis"],
                    "event_day_rule": "first NYSE session strictly after the expiration date",
                    "early_release_checked": False,
                    "note": "Nasdaq's nominal date. Staged early releases, a waiver for a follow-on "
                            "or an earnings-linked release can have freed the shares earlier; the "
                            "hunter checks the 424B4 and the filings since."},
         "tape": {"first_trade": bs[0]["date"] if bs else None,
                  "sessions_listed": len(prev),
                  "vs_offer_pct": IM.pct(n.get("offer_price"), last["raw_close"]) if last else None,
                  "run_up_5d_pct": IM.pct(prev[-6]["close"], last["close"]) if len(prev) > 6 else None,
                  "run_up_20d_pct": IM.pct(prev[-21]["close"], last["close"]) if len(prev) > 21 else None,
                  "turnover_20d_usd": n.get("turnover_20d_usd"),
                  "open_close_sd_20d_pct": round(st.stdev(oc), 2) if len(oc) > 2 else None,
                  "open_close_median_abs_20d_pct": round(st.median([abs(x) for x in oc]), 2) if oc else None,
                  "volume_5d_vs_20d": (round(st.mean([x["volume"] for x in prev[-5:]]) /
                                             st.mean([x["volume"] for x in prev[-20:]]), 2)
                                       if len(prev) >= 20 and st.mean([x["volume"] for x in prev[-20:]]) else None),
                  "source": "Yahoo daily bars, adjusted"},
         "short_interest": si, "insiders": ins,
         "phase0": p0,
         "edgar": edgar_block(ov.get("SECCIK") or n.get("cik"), LOCKUP_PROBES, 400, day),
         "anchor_quality": {"magnitude": 0.5 if len(oc) >= 10 else 0.3,
                            "direction": 0.3 if si.get("status") == "ok" else 0.1},
         "history": {"n": 0, "basis": "one lock-up per IPO: there is no own history of this event"},
         # stage E's run-up control, sealed under the name every resolver reads
         "run_up_20d_pct": IM.pct(prev[-21]["close"], last["close"]) if len(prev) > 21 else None}
    return b


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    u = json.loads(Path(a.universe).read_text())
    day = date.fromisoformat(u["run_date"])
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    p0 = phase0()
    regime = debut_regime(day) if any(n["event_type"] == "debut" for n in u["names"]) else None
    for n in u["names"]:
        f = out / f"{n['ticker']}.json"
        if f.exists():
            print(f"{n['ticker']}: sealed already, left alone")
            continue
        b = seal_debut(n, day, regime, p0) if n["event_type"] == "debut" else seal_lockup(n, day, p0)
        b["sealed_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        b["validation_only"] = u.get("validation_only", False)
        f.write_text(json.dumps(b, indent=1, default=str) + "\n")
        print(f"{n['ticker']}: {n['event_type']} sealed")


if __name__ == "__main__":
    main()
