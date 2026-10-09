#!/usr/bin/env python3
"""Phase 0 for stage IPO: what the two windows do, measured before any agent exists.

Over every operating-company IPO Nasdaq's calendar lists as priced in the lookback
(SPACs out), this measures:

  debut   first trade (day-1 open) -> day-1 close        the stage's key window
          offer -> first trade (the pop, not capturable)  recorded, ranks nothing
          offer -> day-1 close, day-1 close -> day-2 close
  lockup  open -> close on the first session after the expiration date   key window
          the same window on the expiration-date session itself (the other convention)
          close(D-1) -> close(D), close(D-5) -> close(D-1) (the run-in)

each raw and net of IWM over the same window, then splits them on the things a hunter
would be told: deal size, exchange, the pop, price versus offer at the unlock, the size
of the overhang. It also ranks the free variables a hunt has to beat.

    python3 researcher_ipo/scripts/ipo_backtest.py [--months 26] [--min-deal 25e6]

Writes researcher_ipo/analysis/phase0-base-rates.json and the per-event rows beside it.
Three biases, all reported in the output: the universe is Nasdaq's calendar as served
today (a deal it dropped is absent); Yahoo serves today's listings, so an IPO that
delisted since has no bars and falls out (biases the lock-up sample toward survivors);
and the lock-up date is Nasdaq's nominal one, blind to staged early releases.
"""
import argparse
import json
import statistics as st
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ipo_market as IM                                           # noqa: E402
RM = IM.RM

OUT = IM.REPO / "researcher_ipo" / "analysis"


def summary(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "mean": round(st.mean(xs), 2), "median": round(st.median(xs), 2),
            "sd": round(st.stdev(xs), 2) if len(xs) > 1 else None,
            "share_up": round(sum(x > 0 for x in xs) / len(xs), 3),
            "t": RM.tstat(xs),
            "median_abs": round(st.median([abs(x) for x in xs]), 2)}


def split(rows, key, buckets, val):
    out = {}
    for name, test in buckets:
        out[name] = summary([r[val] for r in rows if r.get(key) is not None and test(r[key])])
    return out


def raw_open(b):
    return b["open"] * (b["raw_close"] / b["close"]) if b and b["close"] else None


def debut_rows(deals, min_deal):
    rows = []
    for d in deals:
        if d["spac"] or not d["ticker"] or (d["deal_usd"] or 0) < min_deal:
            continue
        bs = IM.bars(d["ticker"])
        if not bs:
            rows.append({**d, "priced_date": d["priced_date"].isoformat(), "no_bars": True})
            continue
        b0 = bs[0]
        first = date.fromisoformat(b0["date"])
        lag = (first - d["priced_date"]).days
        offer = d["price_high"] if d["price_high"] == d["price_low"] else None
        ro = raw_open(b0)
        r = {**d, "priced_date": d["priced_date"].isoformat(), "first_bar_date": b0["date"],
             "first_bar_lag_days": lag, "offer": offer,
             # the first bar Yahoo has is not always the debut: a listing older than the
             # 2y range, or a deal that never printed until much later
             "debut_on_tape": 0 <= lag <= 7,
             "key_move_pct": IM.pct(b0["open"], b0["close"]),
             "pop_pct": IM.pct(offer, ro) if offer else None,
             "offer_to_close_pct": IM.pct(offer, b0["raw_close"]) if offer else None,
             "d1_to_d2_pct": IM.pct(b0["close"], bs[1]["close"]) if len(bs) > 1 else None,
             "day1_turnover_usd": round(b0["raw_close"] * b0["volume"], 0)}
        bm = IM.benchmark_window(b0["date"], "open_close")
        r["key_excess_pct"] = (round(r["key_move_pct"] - bm, 3)
                               if r["key_move_pct"] is not None and bm is not None else None)
        rows.append(r)
    return rows


def lockup_rows(deals, min_deal, today):
    rows = []
    for d in deals:
        if d["spac"] or not d["ticker"] or (d["deal_usd"] or 0) < min_deal:
            continue
        ov = IM.overview(d["deal_id"], max_age_h=None)
        exp, days, basis = IM.lockup_terms(ov, d["priced_date"])
        if not exp:
            continue
        ev = IM.lockup_event_day(exp)
        if ev >= today:
            continue
        bs = IM.bars(d["ticker"])
        b = IM.bar_on(bs, ev)
        r = {**d, "priced_date": d["priced_date"].isoformat(), "lockup_days": days,
             "lockup_basis": basis, "expiration_date": exp.isoformat(),
             "event_date": ev.isoformat(),
             "shares_outstanding": IM.money(ov.get("SharesOutstanding")),
             "secondary_shares": IM.money(ov.get("ShareholderSharesOffered"))}
        if not b:
            r["no_bar_on_event_day"] = True
            rows.append(r)
            continue
        prev = IM.bars_before(bs, ev)
        bexp = IM.bar_on(bs, exp)
        offer = d["price_high"] if d["price_high"] == d["price_low"] else None
        r.update({
            "key_move_pct": IM.pct(b["open"], b["close"]),
            "expiry_session_move_pct": IM.pct(bexp["open"], bexp["close"]) if bexp else None,
            "close_to_close_pct": IM.pct(prev[-1]["close"], b["close"]) if prev else None,
            "run_in_5d_pct": IM.pct(prev[-6]["close"], prev[-1]["close"]) if len(prev) > 6 else None,
            "run_up_20d_pct": IM.pct(prev[-21]["close"], prev[-1]["close"]) if len(prev) > 21 else None,
            "vs_offer_pct": IM.pct(offer, prev[-1]["raw_close"]) if offer and prev else None,
            "volume_ratio": (round(b["volume"] / st.median([x["volume"] for x in prev[-20:]]), 2)
                             if len(prev) >= 20 and st.median([x["volume"] for x in prev[-20:]]) else None),
            "turnover_20d_usd": (round(st.median([x["raw_close"] * x["volume"] for x in prev[-20:]]), 0)
                                 if len(prev) >= 20 else None),
        })
        so, sh = r["shares_outstanding"], d["shares_offered"]
        r["locked_share_of_outstanding"] = (round(1 - sh / so, 3) if so and sh and so > sh else None)
        bm = IM.benchmark_window(ev, "open_close")
        r["key_excess_pct"] = (round(r["key_move_pct"] - bm, 3)
                               if r["key_move_pct"] is not None and bm is not None else None)
        rows.append(r)
    return rows


def free_rankers(rows, cands, val="key_move_pct"):
    out = {}
    for c in cands:
        pairs = [(r[c], r[val]) for r in rows if r.get(c) is not None and r.get(val) is not None]
        if len(pairs) >= 10:
            out[c] = {"n": len(pairs), "spearman": RM.spearman([p[0] for p in pairs], [p[1] for p in pairs])}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--months", type=int, default=26)
    ap.add_argument("--min-deal", type=float, default=None)
    a = ap.parse_args()
    c = IM.cfg()
    min_deal = a.min_deal if a.min_deal is not None else float(c.get("min_deal_usd", 25e6))
    today = date.today()
    months = IM.months_back(a.months, today)
    deals = IM.priced_deals(months)
    n_spac = sum(d["spac"] for d in deals)
    print(f"{len(deals)} priced deals over {months[0]}..{months[-1]}, {n_spac} SPACs", file=sys.stderr)

    deb = [r for r in debut_rows([d for d in deals if d["priced_date"] < today], min_deal)]
    deb_ok = [r for r in deb if r.get("debut_on_tape") and r.get("key_move_pct") is not None]
    print(f"debuts: {len(deb)} candidates, {len(deb_ok)} on the tape", file=sys.stderr)
    lk = lockup_rows(deals, min_deal, today)
    lk_ok = [r for r in lk if r.get("key_move_pct") is not None]
    print(f"lock-ups: {len(lk)} expired, {len(lk_ok)} with a bar on the event day", file=sys.stderr)

    size_b = [("<$50m", lambda x: x < 50e6), ("$50-200m", lambda x: 50e6 <= x < 200e6),
              ("$200m-1bn", lambda x: 200e6 <= x < 1e9), (">=$1bn", lambda x: x >= 1e9)]
    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lookback_months": months,
        "min_deal_usd": min_deal,
        "priced_deals": len(deals), "spacs_excluded": n_spac,
        "debut": {
            "window": "first trade (day-1 open) -> day-1 close",
            "n_candidates": len(deb), "n_on_tape": len(deb_ok),
            "no_bars": sum(1 for r in deb if r.get("no_bars")),
            "first_bar_not_debut": sum(1 for r in deb if r.get("first_bar_date") and not r.get("debut_on_tape")),
            "key_move_pct": summary([r["key_move_pct"] for r in deb_ok]),
            "key_excess_pct": summary([r["key_excess_pct"] for r in deb_ok]),
            "pop_pct": summary([r["pop_pct"] for r in deb_ok]),
            "offer_to_close_pct": summary([r["offer_to_close_pct"] for r in deb_ok]),
            "d1_to_d2_pct": summary([r["d1_to_d2_pct"] for r in deb_ok]),
            "by_deal_size": split(deb_ok, "deal_usd", size_b, "key_move_pct"),
            "by_exchange": {ex: summary([r["key_move_pct"] for r in deb_ok if (r["exchange"] or "").startswith(ex)])
                            for ex in ("NASDAQ", "NYSE")},
            "by_pop": split(deb_ok, "pop_pct", [("broke issue (<0)", lambda x: x < 0),
                                                ("0 to 15", lambda x: 0 <= x < 15),
                                                ("15 to 50", lambda x: 15 <= x < 50),
                                                (">=50", lambda x: x >= 50)], "key_move_pct"),
            "free_rankers_vs_key": free_rankers(deb_ok, ["pop_pct", "deal_usd", "day1_turnover_usd"]),
        },
        "lockup": {
            "window": "open -> close of the first session after Nasdaq's expiration date",
            "n_expired": len(lk), "n_with_bar": len(lk_ok),
            "no_bar_on_event_day": sum(1 for r in lk if r.get("no_bar_on_event_day")),
            "basis": {b: sum(1 for r in lk if r["lockup_basis"] == b) for b in
                      ("nasdaq_overview_date", "nasdaq_overview_days", "assumed_180")},
            "lockup_days": {str(k): sum(1 for r in lk if r.get("lockup_days") == k)
                            for k in sorted({r.get("lockup_days") for r in lk if r.get("lockup_days")})},
            "key_move_pct": summary([r["key_move_pct"] for r in lk_ok]),
            "key_excess_pct": summary([r["key_excess_pct"] for r in lk_ok]),
            "expiry_session_move_pct": summary([r["expiry_session_move_pct"] for r in lk_ok]),
            "close_to_close_pct": summary([r["close_to_close_pct"] for r in lk_ok]),
            "run_in_5d_pct": summary([r["run_in_5d_pct"] for r in lk_ok]),
            "volume_ratio": summary([r["volume_ratio"] for r in lk_ok]),
            "by_vs_offer": split(lk_ok, "vs_offer_pct", [("below offer", lambda x: x < 0),
                                                         ("0 to 50 over", lambda x: 0 <= x < 50),
                                                         (">=50 over", lambda x: x >= 50)], "key_move_pct"),
            "by_locked_share": split(lk_ok, "locked_share_of_outstanding",
                                     [("<70% locked", lambda x: x < 0.7), ("70-85%", lambda x: 0.7 <= x < 0.85),
                                      (">=85%", lambda x: x >= 0.85)], "key_move_pct"),
            "by_turnover": split(lk_ok, "turnover_20d_usd", [("<$1m/day", lambda x: x < 1e6),
                                                             ("$1-10m", lambda x: 1e6 <= x < 1e7),
                                                             (">=$10m", lambda x: x >= 1e7)], "key_move_pct"),
            "free_rankers_vs_key": free_rankers(lk_ok, ["vs_offer_pct", "run_up_20d_pct", "run_in_5d_pct",
                                                        "locked_share_of_outstanding", "turnover_20d_usd"]),
        },
        "events_per_trading_day": None,
        "known_biases": [
            "Nasdaq's calendar as served today; deals it no longer lists are absent.",
            "Yahoo serves today's listings: an IPO that delisted has no bars and drops out, which "
            "removes the worst outcomes from the lock-up sample.",
            "Lock-up dates are Nasdaq's nominal ones; staged early releases are not visible here.",
            "Day-1 open is the opening cross as Yahoo reports it; a market order sent after it fills "
            "at the NBBO a moment later, and day-1 spreads in a new listing are wide.",
        ],
    }
    sessions = sum(1 for i in range(365) if IM.is_trading_day(date.fromordinal(today.toordinal() - i)))
    yr = date.fromordinal(today.toordinal() - 365).isoformat()
    n_deb_yr = sum(1 for r in deb_ok if r["first_bar_date"] >= yr)
    n_lk_yr = sum(1 for r in lk_ok if r["event_date"] >= yr)
    doc["events_per_trading_day"] = {"last_365_days_sessions": sessions, "debuts": n_deb_yr,
                                     "lockups": n_lk_yr,
                                     "per_session": round((n_deb_yr + n_lk_yr) / sessions, 2)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "phase0-base-rates.json").write_text(json.dumps(doc, indent=1) + "\n")
    (OUT / "phase0-rows.json").write_text(json.dumps({"debut": deb, "lockup": lk}, indent=1, default=str) + "\n")
    print(json.dumps({k: doc[k] for k in ("priced_deals", "spacs_excluded", "events_per_trading_day")}, indent=1))
    for ev in ("debut", "lockup"):
        print(ev, json.dumps(doc[ev]["key_move_pct"]), json.dumps(doc[ev]["key_excess_pct"]))


if __name__ == "__main__":
    main()
