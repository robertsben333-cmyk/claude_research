#!/usr/bin/env python3
"""What is reporting over the next week, and how much of it stage E could hunt.

A forward calendar, not a research output. It answers the planning question the
dashboard cannot answer from the archive: how many names are coming, on which
sessions, and how many of them would survive the two gates that decide whether the
edge hunt sees a name at all.

THE TWO GATES, BOTH APPLIED HERE SO THE COUNT IS HONEST

  SESSION. Nasdaq's `time` field is a schedule for `time-pre-market` and
  `time-after-hours` and an admission of ignorance for `time-not-supplied`. Stage 0
  drops the third case. That is usually the LARGER half of the calendar -- 20 of 22
  rows on 2026-09-17 -- and the measured phantom rate on it is 20 of 20 for that
  window and 8 of 8 for 2026-08-31, so dropping them is right on cost and is not
  free. Both counts are printed; neither is hidden inside the other.

  LIQUIDITY. `execution.benchmark.min_dollar_volume_usd` in config/pipeline.yaml,
  $200k a day. Names below it are dropped outright rather than sized down, so a
  calendar that counts them overstates what is tradeable. Turnover is spot times
  20-day average volume, from the same bars the rest of the analysis uses.

WHAT THIS IS NOT. It carries no prediction, no ranking and no score -- those come
from a hunt that has not happened. A name on this list is a candidate, and the
archive says most candidates never clear the conviction floor: 55 of 106 resolved
events did, and on the four thinnest days the count was zero.

    python3 edge/scripts/edge_calendar.py
    python3 edge/scripts/edge_calendar.py --days 7 --out edge/analysis/edge-calendar.json
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts"))

import edge_bars as EB                                        # noqa: E402
from get_earnings import fetch_nasdaq, is_trading_day         # noqa: E402

try:
    import yaml
except ImportError:                                           # pragma: no cover
    yaml = None


def min_dollar_volume():
    if yaml is None:
        return 200_000
    cfg = yaml.safe_load((REPO / "config" / "pipeline.yaml").read_text())
    return float(((cfg.get("execution") or {}).get("benchmark") or {})
                 .get("min_dollar_volume_usd") or 200_000)


def turnover(ticker):
    """spot * 20-session average volume, from the shared bar cache."""
    rows, err = EB.bars(ticker)
    if err or not rows:
        return None, None, err or "no bars"
    days = EB.by_day(rows)
    ds = sorted(days)[-20:]
    if not ds:
        return None, None, "no sessions"
    spot = EB.day_close(days[ds[-1]])
    vols = []
    for d in ds:
        v = sum(b[4] or 0 for b in days[d])
        if v:
            vols.append(v)
    if not vols or not spot:
        return spot, None, "no volume"
    return spot, round(spot * (sum(vols) / len(vols))), None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7, help="calendar days ahead to cover")
    ap.add_argument("--from", dest="start", default=None, help="YYYY-MM-DD, default today")
    ap.add_argument("--no-turnover", action="store_true",
                    help="skip the liquidity gate (no price fetches)")
    ap.add_argument("--out", default="edge/analysis/edge-calendar.json")
    a = ap.parse_args()

    start = datetime.fromisoformat(a.start).date() if a.start else date.today()
    floor = min_dollar_volume()
    print(f"Earnings calendar from {start} for {a.days} days. "
          f"Liquidity floor ${floor:,.0f}/day.\n")

    out, errors = {}, []
    for i in range(a.days + 1):
        d = start + timedelta(days=i)
        if not is_trading_day(d):
            continue
        try:
            rows = fetch_nasdaq(d)
        except Exception as e:                                # noqa: BLE001
            errors.append({"date": d.isoformat(), "error": f"{type(e).__name__}: {str(e)[:100]}"})
            print(f"  {d}  FETCH FAILED  {type(e).__name__}: {str(e)[:70]}")
            continue
        names = []
        for r in rows:
            names.append({"ticker": r["symbol"], "company": r["name"],
                          "session": r["session"], "market_cap_usd": r["market_cap_usd"],
                          "eps_estimate": r["eps_estimate"],
                          "fiscal_quarter_ending": r["fiscal_quarter_ending"],
                          "analyst_count": r["analyst_count"]})
        out[d.isoformat()] = names
        conf = [n for n in names if n["session"] in ("amc", "bmo")]
        print(f"  {d}  {len(names):3d} rows   {len(conf):3d} with a confirmed session   "
              f"{len(names) - len(conf):3d} time-not-supplied")

    # liquidity, on the confirmed-session names only -- the others are not candidates
    if not a.no_turnover:
        print("\nPricing the confirmed-session names for the liquidity gate...")
        seen = {}
        for d, names in out.items():
            for n in names:
                if n["session"] not in ("amc", "bmo"):
                    continue
                t = n["ticker"]
                if t not in seen:
                    seen[t] = turnover(t)
                spot, dv, err = seen[t]
                n["spot"], n["dollar_vol"], n["price_error"] = spot, dv, err
                n["clears_liquidity"] = bool(dv and dv >= floor)

    total = sum(len(v) for v in out.values())
    confirmed = sum(1 for v in out.values() for n in v if n["session"] in ("amc", "bmo"))
    tradeable = sum(1 for v in out.values() for n in v if n.get("clears_liquidity"))

    print(f"\n{total} calendar rows over {len(out)} trading days")
    print(f"{confirmed} carry a confirmed session -- the only ones stage 0 keeps")
    if not a.no_turnover:
        print(f"{tradeable} of those also clear the ${floor:,.0f}/day liquidity floor")

    print("\nBY SESSION AND DAY (confirmed sessions only)\n")
    print(f"  {'date':12s}{'amc':>6s}{'bmo':>6s}{'tradeable':>11s}   largest names by turnover")
    for d in sorted(out):
        conf = [n for n in out[d] if n["session"] in ("amc", "bmo")]
        amc = sum(1 for n in conf if n["session"] == "amc")
        bmo = len(conf) - amc
        tr = [n for n in conf if n.get("clears_liquidity")]
        top = sorted(tr, key=lambda n: -(n.get("dollar_vol") or 0))[:4]
        s = ", ".join(f"{n['ticker']} ({n['session']})" for n in top)
        print(f"  {d:12s}{amc:>6d}{bmo:>6d}{len(tr):>11d}   {s}")

    res = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "from": start.isoformat(), "days": a.days,
           "liquidity_floor_usd": floor,
           "totals": {"rows": total, "confirmed_session": confirmed,
                      "clears_liquidity": tradeable},
           "source": "api.nasdaq.com/api/calendar/earnings",
           "errors": errors, "by_date": out}
    Path(REPO / a.out).write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
