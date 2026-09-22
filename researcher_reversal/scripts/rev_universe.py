#!/usr/bin/env python3
"""The day's universe: the worst fallers of the last completed US session.

THE SCREEN IS THE EVENT DEFINITION, NOT A RANKING
-------------------------------------------------
Stage E draws its day at random once a turnover floor has cut it, because any other
cut is a second ranking the scorer cannot see. Here the cut IS the event definition:
"the biggest losers" is what the stage studies, so ranking by the fall and taking the
worst K is the population, not a selection inside it. What must NOT happen is a
second cut underneath: every name that survives the floors and makes the worst K is
hunted, with one hunter each. K equals the hunter cap for that reason. Hunting the
"most interesting" ten of fifteen would be exactly the double-hunt mistake one level
up -- a score assigned before any hunting, invisible to everything downstream.

TWO FLOORS AND A FOLD
---------------------
  turnover   median 20-day dollar volume >= $200k, the same floor stages E, J, EU and
             AU screen on, so a pooled comparison across stages is not comparing cuts
  price      close >= $1.00. Sub-dollar names are tick-constrained, frequently in
             delisting proceedings, and their "30% fall" is often two ticks
  fold       one issuer is one event; researcher_us/scripts/share_class.py, unchanged

THE PRE-RANK IS THE SCREENER AND THE DECISION IS THE BARS
---------------------------------------------------------
Nasdaq's screener carries an unadjusted percent change for every listed name in one
request, which is the cheap way to find the candidates. It is NOT the decision: a
2-for-1 split reads as -50% there. Every candidate's fall is recomputed from split
and dividend adjusted closes before it is kept, and the difference between the two is
carried per row as `screener_vs_adjusted_gap_pp` so a corporate action is visible
rather than silently traded.

    python3 researcher_reversal/scripts/rev_universe.py --date 2026-09-21 --k 15
"""
import argparse
import json
import sys
import time
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))
sys.path.insert(0, str(REPO / "scripts"))
import rev_market as M                                            # noqa: E402
from share_class import collapse                                  # noqa: E402

try:
    from get_earnings import next_trading_day                     # NYSE calendar
except Exception:                                                 # noqa: BLE001
    next_trading_day = None

DV_FLOOR = 200_000.0
PRICE_FLOOR = 1.00
CANDIDATES = 200          # deepest the screener pre-rank is trusted to go
ET = ZoneInfo("America/New_York")
# The intraday screen is only meaningful in the last part of the session: early enough
# that the position can still go on, late enough that the day's fall is mostly made.
# 21:00 CET is 15:00 ET, which is the hour this was measured on.
CUT_OPEN_ET, CUT_CLOSE_ET = (13, 30), (16, 5)


def last_session(bars_spy):
    return bars_spy[-1]["date"] if bars_spy else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="the drop date. Default: last completed session")
    ap.add_argument("--k", type=int, default=15, help="names hunted; equals the hunter cap")
    ap.add_argument("--dv", type=float, default=DV_FLOOR)
    ap.add_argument("--price", type=float, default=PRICE_FLOOR)
    ap.add_argument("--candidates", type=int, default=CANDIDATES)
    ap.add_argument("--intraday", action="store_true",
                    help="screen TODAY's incomplete session off the live partial bar, "
                         "so the names can still be bought before the close. Measured "
                         "cost against the close screen: 86.4%% of the worst 15 survive "
                         "to the close and the last hour is a coin flip "
                         "(researcher_reversal/analysis/intraday-cut.json)")
    ap.add_argument("--from-drops", metavar="DIR",
                    help="rebuild a PAST session from rev_harvest.py's drops.jsonl.gz "
                         "instead of the live screener. The screener's percent change "
                         "is today's, so it cannot pre-rank a historical day; this is "
                         "what makes a past day reconstructable for validation")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    spy = M.bars("SPY", rg="1mo")
    now_et = datetime.now(ET)
    if a.intraday:
        # Yahoo's daily chart carries TODAY as a partial bar whose close is the live
        # price, so the same code path screens an unfinished session. What it must not
        # do is pretend the bar is final.
        drop_date = a.date or now_et.date().isoformat()
        hhmm = (now_et.hour, now_et.minute)
        if not (CUT_OPEN_ET <= hhmm <= CUT_CLOSE_ET) and not a.date:
            print(f"intraday screen refused at {now_et:%H:%M} ET: the window is "
                  f"{CUT_OPEN_ET[0]:02d}:{CUT_OPEN_ET[1]:02d}-"
                  f"{CUT_CLOSE_ET[0]:02d}:{CUT_CLOSE_ET[1]:02d} ET. Before it the day's "
                  f"fall is not made yet; after it, screen the completed session "
                  f"instead of a partial bar.", file=sys.stderr)
            return 2
        if now_et.weekday() >= 5 and not a.date:
            print("intraday screen refused: US market shut", file=sys.stderr)
            return 2
    else:
        drop_date = a.date or last_session(spy)
    if not drop_date:
        print("cannot establish the last completed session", file=sys.stderr)
        return 2
    spy_by = {x["date"]: x for x in spy}
    spy_ret = None
    if drop_date in spy_by:
        i = [x["date"] for x in spy].index(drop_date)
        if i:
            spy_ret = round((spy[i]["close"] / spy[i - 1]["close"] - 1) * 100, 3)

    nxt = None
    if a.from_drops:
        spy2 = M.bars("SPY", rg="2y")
        ds = [x["date"] for x in spy2]
        if drop_date in ds:
            i2 = ds.index(drop_date)
            if i2 + 1 < len(ds):
                nxt = ds[i2 + 1]
            j = i2
            if j:
                spy_ret = round((spy2[j]["close"] / spy2[j - 1]["close"] - 1) * 100, 3)
    if nxt is None and next_trading_day:
        try:
            nxt = next_trading_day(date.fromisoformat(drop_date)).isoformat()
        except Exception:                                         # noqa: BLE001
            nxt = None

    uni = M.screener()
    meta = {u["ticker"]: u for u in uni}
    if a.from_drops:
        import gzip
        seen = {}
        with gzip.open(Path(a.from_drops) / "drops.jsonl.gz", "rt") as fh:
            for line in fh:
                r = json.loads(line)
                if r["date"] == drop_date:
                    seen[r["ticker"]] = r["ret_d_pct"]
        pre = sorted([{**(meta.get(t) or {"ticker": t, "company": None, "sector": None,
                                          "exchange": None, "market_cap": None}),
                       "pct_change": v} for t, v in seen.items()],
                     key=lambda u: u["pct_change"])[:a.candidates]
        print(f"harvest {len(seen)} candidate falls on {drop_date}", file=sys.stderr)
    else:
        pre = sorted([u for u in uni if u.get("pct_change") is not None],
                     key=lambda u: u["pct_change"])[:a.candidates]
        print(f"screener {len(uni)} names, {len(pre)} candidates pre-ranked, "
              f"worst {pre[0]['ticker']} {pre[0]['pct_change']}%", file=sys.stderr)
    if not pre:
        print(f"no candidates for {drop_date}", file=sys.stderr)
        return 2

    rg = "2y" if a.from_drops else "6mo"
    bars = M.bars_many([u["ticker"] for u in pre], rg=rg, workers=8)

    rows, rejected = [], []
    for u in pre:
        t = u["ticker"]
        b = bars.get(t) or []
        dates = [x["date"] for x in b]
        if drop_date not in dates:
            rejected.append({"ticker": t, "why": "no bar on the drop date"})
            continue
        i = dates.index(drop_date)
        if i < 21:
            rejected.append({"ticker": t, "why": "under 21 sessions of history"})
            continue
        prev, cur = b[i - 1], b[i]
        ret = round((cur["close"] / prev["close"] - 1) * 100, 3)
        w20 = b[i - 20:i]
        dv = M.median([x["close"] * x["volume"] for x in w20]) or 0.0
        vol20 = M.median([x["volume"] for x in w20]) or 0.0
        row = {
            "ticker": t, "company": u["company"], "sector": u["sector"],
            "exchange": u["exchange"], "market_cap": u["market_cap"],
            "event_date": drop_date,            # share_class.collapse reads this key
            "drop_date": drop_date,
            "next_session": nxt,
            "ret_d_pct": ret,
            "screener_pct_change": u["pct_change"],
            "screener_vs_adjusted_gap_pp": round(u["pct_change"] - ret, 2),
            "price": round(cur["raw_close"], 4),
            "dv_med20": round(dv),
            "dollar_volume_d": round(cur["close"] * cur["volume"]),
            "volume_spike_x": round(cur["volume"] / vol20, 2) if vol20 else None,
            "gap_pct": round((cur["open"] / prev["close"] - 1) * 100, 3),
            "spy_ret_d_pct": spy_ret,
        }
        row["idio_ret_pct"] = (round(ret - spy_ret, 3) if spy_ret is not None else None)
        if dv < a.dv:
            rejected.append({**row, "why": f"turnover {round(dv)} below {int(a.dv)}"})
            continue
        if row["price"] < a.price:
            rejected.append({**row, "why": f"price {row['price']} below {a.price}"})
            continue
        if ret >= 0:
            rejected.append({**row, "why": "adjusted close did not fall; the screener's "
                                           "percent change was a corporate action"})
            continue
        rows.append(row)

    kept, folded = collapse(rows, key=lambda x: x)
    kept.sort(key=lambda r: r["ret_d_pct"])
    hunted = kept[:a.k]
    for n, r in enumerate(hunted, 1):
        r["rank_by_fall"] = n

    doc = {
        "built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "drop_date": drop_date,
        "next_session": nxt,
        "predicted_window": "close of drop_date -> close of next_session",
        "spy_ret_d_pct": spy_ret,
        "screen_basis": ("live partial bar, session still open" if a.intraday
                         else "completed session, final daily bars"),
        "screen_time_et": now_et.strftime("%Y-%m-%d %H:%M %Z"),
        "bars_are_final": not a.intraday,
        "intraday_caveat": (
            "The fall is measured to the screen instant, not to the close. Measured "
            "over 45 sessions: 86.4% of the worst 15 at 15:00 ET are still the worst 15 "
            "at the close (min 11 of 15), and the 15:00-to-close move on those names is "
            "a coin flip -- mean -0.24%, median 0.00%, sd 4.54%, 49.8% falling further. "
            "So the screen is cheap and the entry is near-free in expectation, but "
            "phase 0's base rates are CLOSE-to-close and this is not."
            if a.intraday else None),
        "screen": {"candidates_pre_ranked": len(pre),
                   "dv_med20_min": a.dv, "price_min": a.price,
                   "worst_per_session": a.k,
                   "note": "the worst K by adjusted fall, every one of them hunted. "
                           "No second cut: K equals the hunter cap by design"},
        "counts": {"screener": len(uni), "passed_floors": len(rows),
                   "share_classes_folded": len(folded), "hunted": len(hunted),
                   "rejected": len(rejected)},
        "market_concentration": _concentration(hunted),
        "hunted": hunted,
        "not_hunted_above_floor": kept[a.k:],
        "folded": folded,
        "rejected": rejected[:80],
    }
    s = json.dumps(doc, indent=1)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(s)
        print(f"wrote {a.out}", file=sys.stderr)
    else:
        print(s)
    return 0


def _concentration(rows):
    """One sector filling the day is a correlated exposure the scorer cannot see.

    Stage EU carries the same field because 15 of 20 names came back Swedish on one
    day; stage E ranked four US names on one tariff ruling. A losers screen is MORE
    exposed to this than an earnings calendar, because a sector selling off is the
    most ordinary way for fifteen names to fall at once.
    """
    from collections import Counter
    c = Counter(r.get("sector") or "unknown" for r in rows)
    top = c.most_common(1)[0] if c else ("none", 0)
    return {"by_sector": dict(c.most_common()),
            "largest_sector": top[0],
            "largest_sector_share": round(top[1] / len(rows), 2) if rows else None,
            "warning": ("more than half the day is one sector: treat the day's ranking "
                        "as one bet, not as K" if rows and top[1] / len(rows) > 0.5 else None)}


if __name__ == "__main__":
    sys.exit(main())
