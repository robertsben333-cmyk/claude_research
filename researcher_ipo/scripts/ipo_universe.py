#!/usr/bin/env python3
"""Stage IPO's universe for one US session: the debuts and the lock-up expiries.

    python3 researcher_ipo/scripts/ipo_universe.py -o <RUN>/universe.json [--date YYYY-MM-DD]

Default date is today in New York. The Routine fires at 08:35 ET, before the open, so
every name here is an event in a session that has not started yet.

DEBUTS. A priced deal whose `pricedDate` is the session, or an upcoming deal expected to
price the evening before or on the day that Nasdaq has not flipped to priced yet
(`offer_price_final: false`). SPACs are dropped. A floor on the deal size
(`ipo_hunt.min_deal_usd`) stands in for a turnover floor, because a debut has no tape.
A deal that already has a bar before the session is not a debut and is dropped.

LOCK-UPS. A deal priced in the last `lockup_lookback_months` whose first session after
Nasdaq's lock-up expiration date is the session. Only deals whose pricing date plus a
standard lock-up length (90, 120, 150, 180, 270 or 365 days, plus or minus ten) lands
near the session have their deal page fetched, so a lock-up of a non-standard length
outside those bands is missed; that is stated in the output rather than discovered.
A lock-up name must clear stage E's turnover floor (`ipo_hunt.min_turnover_usd`, median
of the last twenty sessions) and still be listed.

If more than `cap` names survive, a DATE-SEEDED random draw picks them, the same rule as
stages J, EU, AU and CA: any other cut is a second ranking the scorer cannot see.
Research only; nothing here places an order.
"""
import argparse
import json
import random
import statistics as st
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ipo_market as IM                                           # noqa: E402

ET = ZoneInfo("America/New_York")
STANDARD_LOCKUPS = (90, 120, 150, 180, 270, 365)


def debuts(day, cfg, funnel):
    months = sorted({(day - timedelta(days=3)).strftime("%Y-%m"), day.strftime("%Y-%m")})
    rows, seen = [], set()
    for ym in months:
        cal = IM.calendar_month(ym, refresh=True)
        for status in ("priced", "upcoming"):
            for r in cal.get(status) or []:
                d = IM.deal_row(r, status)
                if d["deal_id"] in seen:
                    continue
                pd = d["priced_date"]
                hit = (pd == day) if status == "priced" else (pd in (day, IM.prev_trading_day(day)))
                if not hit:
                    continue
                seen.add(d["deal_id"])
                funnel["debut_scheduled"] += 1
                if d["spac"]:
                    funnel["debut_spac"] += 1
                    continue
                if not d["ticker"]:
                    funnel["debut_no_ticker"] += 1
                    continue
                rows.append(d)
    out = []
    for d in rows:
        if (d["deal_usd"] or 0) < float(cfg.get("min_deal_usd", 25e6)):
            funnel["debut_below_min_deal"] += 1
            continue
        bs = IM.bars(d["ticker"], rg="1mo")
        if IM.bars_before(bs, day):
            funnel["debut_already_trading"] += 1
            continue
        ov = IM.overview(d["deal_id"], max_age_h=6)
        final = d["status"] == "priced" and d["price_low"] == d["price_high"]
        out.append({
            "ticker": d["ticker"], "company": d["company"], "event_type": "debut",
            "session": "debut", "event_date": day.isoformat(), "exchange": d["exchange"],
            "deal_id": d["deal_id"], "cik": ov.get("SECCIK"),
            "calendar_status": d["status"], "offer_price_final": final,
            "offer_price": d["price_high"] if final else None,
            "price_range": None if final else [d["price_low"], d["price_high"]],
            "shares_offered": d["shares_offered"], "deal_usd": d["deal_usd"],
        })
    return out


def lockups(day, cfg, funnel):
    lb = int(cfg.get("lockup_lookback_months", 15))
    deals = IM.priced_deals(IM.months_back(lb, day))
    out = []
    for d in deals:
        if d["spac"] or not d["ticker"]:
            continue
        age = (day - d["priced_date"]).days
        if not any(abs(age - n) <= 10 for n in STANDARD_LOCKUPS):
            continue
        ov = IM.overview(d["deal_id"])
        exp, days, basis = IM.lockup_terms(ov, d["priced_date"])
        if not exp or IM.lockup_event_day(exp) != day:
            continue
        funnel["lockup_scheduled"] += 1
        if (d["deal_usd"] or 0) < float(cfg.get("min_deal_usd", 25e6)):
            funnel["lockup_below_min_deal"] += 1
            continue
        bs = IM.bars(d["ticker"], rg="3mo")
        prev = IM.bars_before(bs, day)
        if len(prev) < 5:
            funnel["lockup_no_tape"] += 1
            continue
        to = st.median([b["raw_close"] * b["volume"] for b in prev[-20:]])
        if to < float(cfg.get("min_turnover_usd", 200_000)):
            funnel["lockup_below_turnover"] += 1
            continue
        out.append({
            "ticker": d["ticker"], "company": d["company"], "event_type": "lockup",
            "session": "lockup", "event_date": day.isoformat(), "exchange": d["exchange"],
            "deal_id": d["deal_id"], "cik": ov.get("SECCIK"),
            "priced_date": d["priced_date"].isoformat(),
            "offer_price": d["price_high"] if d["price_high"] == d["price_low"] else None,
            "lockup_days": days, "lockup_basis": basis,
            "expiration_date": exp.isoformat(), "early_release_checked": False,
            "turnover_20d_usd": round(to, 0), "deal_usd": d["deal_usd"],
        })
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--date", help="the session, YYYY-MM-DD (default: today in New York)")
    ap.add_argument("--validation-only", action="store_true",
                    help="mark the file so no pooled number or reference set reads it")
    a = ap.parse_args()
    cfg = IM.cfg()
    day = date.fromisoformat(a.date) if a.date else datetime.now(ET).date()
    funnel = {k: 0 for k in ("debut_scheduled", "debut_spac", "debut_no_ticker", "debut_below_min_deal",
                             "debut_already_trading", "lockup_scheduled", "lockup_below_min_deal",
                             "lockup_no_tape", "lockup_below_turnover")}
    doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "run_date": day.isoformat(), "market": "IPO",
           "window": {"debut": "first trade (day-1 opening cross) -> day-1 close",
                      "lockup": "open -> close of the first session after the lock-up expiration date"},
           "market_closed": None if IM.is_trading_day(day) else "NYSE holiday or weekend",
           "validation_only": bool(a.validation_only),
           "floors": {"min_deal_usd": float(cfg.get("min_deal_usd", 25e6)),
                      "min_turnover_usd_lockup": float(cfg.get("min_turnover_usd", 200_000))},
           "lockup_search": {"standard_lengths_days": list(STANDARD_LOCKUPS), "band_days": 10,
                             "note": "Deals whose age is not within 10 days of a standard lock-up "
                                     "length are not checked; a non-standard lock-up is missed."}}
    names = []
    if not doc["market_closed"]:
        names = debuts(day, cfg, funnel) + lockups(day, cfg, funnel)
    eligible = len(names)
    cap = int(cfg.get("cap", 12))
    method = "all eligible"
    if eligible > cap:
        rnd = random.Random(f"ipo-{day.isoformat()}")
        names = sorted(rnd.sample(names, cap), key=lambda n: n["ticker"])
        method = f"date-seeded random draw of {cap} from {eligible}"
    doc.update({"funnel": funnel, "eligible": eligible, "scheduled_today": eligible,
                "selection": {"method": method, "seed": f"ipo-{day.isoformat()}",
                              "by_event_type": {e: sum(1 for n in names if n["event_type"] == e)
                                                for e in IM.EVENT_TYPES}},
                "names": names})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n")
    print(f"{day}: {eligible} eligible ({doc['selection']['by_event_type']}), {len(names)} kept; "
          f"funnel {json.dumps(funnel)}" + (f"; MARKET CLOSED: {doc['market_closed']}" if doc["market_closed"] else ""))


if __name__ == "__main__":
    main()
