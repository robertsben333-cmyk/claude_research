#!/usr/bin/env python3
"""Today's ASX earnings universe, qualified, cut and drawn.

Same job as `jp_universe.py` and `eu_universe.py`, and it writes the same shape, so
`researcher_us/scripts/edge_score.py` scores an Australian run unchanged and the four
markets stay directly comparable.

THE STAGE SEALS FOR THE NEXT SESSION, BECAUSE AUSTRALIA REPORTS BEFORE THE OPEN
-------------------------------------------------------------------------------
91% of ASX results announcements land before the 10:00 Sydney open (67 of 74 measured,
see `au_market.py`). So the window is `close(D-1) -> close(D)`, the baseline has to be
sealed on the evening before the print, and `--date` therefore defaults to the NEXT ASX
session rather than to today. The Routine fires at 06:30 UTC, after the 16:00 Sydney
close, which is the evening before.

THE VENDOR DATE IS SHIFTED BEFORE ANYTHING IS DONE WITH IT
-----------------------------------------------------------
85% of Australian vendor rows sit one Sydney day later than the vendor says, because
the vendor stamps the UTC instant and Sydney is ten or eleven hours ahead of it. That
correction happens in `au_market.sydney_event_date()` and every row carries
`vendor_date`, `event_date` and `event_date_basis` so the shift is auditable rather
than invisible. Getting it wrong does not throw; it hunts a name whose print happened
yesterday.

THE CALENDAR IS A VENDOR CALENDAR AND ITS ERROR RATE IS ONLY PARTLY MEASURED
-----------------------------------------------------------------------------
Of 80 vendor rows checked against the ASX announcement record on 2026-09-22, 74 had a
results announcement within three days of the shifted date and 6 did not. That is an
UPPER BOUND on the phantom rate, not the rate: the UK measurement found six of its
eight apparent misses were gaps in the headline classifier rather than missing prints,
and this classifier is deliberately narrower still. Confirmation is not optional and
`event_occurred: false` stays reachable, per-issuer, through `au_resolve.py`.

SELECTION, AND WHY IT IS RANDOM
--------------------------------
A turnover floor for capacity, then a seeded random draw if more than `--cap` survive.
Random because any other cut is a second ranking the scorer cannot see, and this repo
has already paid for one of those twice: the double hunt inflated the US conviction
number by construction, and stage EU refuses to stratify its draw by market for the
same reason. `selection.seed` is in the output so the draw is reproducible and nobody
has to trust it was not re-rolled until it looked good.
"""
import argparse
import json
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "researcher_us" / "scripts"))
import au_market as M                                              # noqa: E402
from share_class import collapse                                   # noqa: E402

TV = "https://scanner.tradingview.com/{scanner}/scan"
TV_COLUMNS = ["name", "description", "close", "currency", "market_cap_basic",
              "average_volume_10d_calc", "earnings_release_date",
              "earnings_release_time", "earnings_release_next_date",
              "earnings_release_next_time", "exchange", "sector", "country"]


def post(url, body, timeout=90):
    import subprocess
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {M.UA}",
           "-X", "POST", "-H", "Content-Type: application/json", "--data-binary", "@-",
           url]
    p = subprocess.run(cmd, capture_output=True, input=json.dumps(body).encode())
    return p.stdout.decode("utf-8", "replace")


def audusd():
    """Live, not a constant. The turnover floor is the only selection this stage makes
    that is not random, so the number it is applied against has to be reproducible from
    the output file."""
    try:
        d = json.loads(M.fetch(f"{M.YQ}/v8/finance/chart/AUDUSD=X?range=5d&interval=1d",
                               timeout=25).decode("utf-8", "replace"))
        c = [x for x in d["chart"]["result"][0]["indicators"]["quote"][0]["close"] if x]
        return round(c[-1], 5)
    except Exception:
        return None


def scan():
    body = {"filter": [{"left": "is_primary", "operation": "equal", "right": True},
                       {"left": "type", "operation": "equal", "right": "stock"}],
            "options": {"lang": "en"}, "columns": TV_COLUMNS,
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
            "range": [0, 6000]}
    d = json.loads(post(TV.format(scanner=M.MARKET["scanner"]), body))
    rows, off_exchange = [], 0
    for x in d.get("data", []):
        r = dict(zip(TV_COLUMNS, x["d"]))
        r["tv_symbol"] = x["s"]
        # The country scanner is not one exchange: it also carries ASXCEN and CHIXAU,
        # which are not the primary listing and would be screened on the wrong tape.
        if r.get("exchange") not in M.MARKET["exchange_allow"]:
            off_exchange += 1
            continue
        rows.append(r)
    return rows, d.get("totalCount"), off_exchange


def tape(code):
    """Spot, 20-day median turnover and the bar count, off Yahoo."""
    sym = M.yahoo_symbol(code)
    url = f"{M.YQ}/v8/finance/chart/{sym}?range=3mo&interval=1d"
    try:
        d = json.loads(M.fetch(url, timeout=30).decode("utf-8", "replace"))
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        rows = [(c, v) for c, v in zip(q["close"], q["volume"])
                if c is not None and v is not None]
    except Exception as exc:
        return {"error": f"{type(exc).__name__}", "source": url}
    if not rows:
        # A WRONG SYMBOL RETURNS AN EMPTY CHART, NOT AN ERROR. That is how stage EU
        # nearly lost its largest Nordic names, so an empty tape is named as such.
        return {"error": "empty chart (wrong symbol, or no bars)", "source": url}
    turn = sorted(c * v for c, v in rows[-20:])
    return {"spot": round(rows[-1][0], 4),
            "median_turnover_aud_20d": round(median(turn)),
            "bars": len(rows), "source": url}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="event date, Sydney. Default: the NEXT ASX session, "
                                   "because this stage seals the evening before.")
    ap.add_argument("--cap", type=int, default=20,
                    help="most names to hunt in a day (default 20)")
    ap.add_argument("--min-turnover-usd", type=int, default=200_000,
                    help="median 20-day turnover floor in USD (default 200000, the "
                         "same capacity bar stages E, J and EU screen on)")
    ap.add_argument("--no-tape", action="store_true",
                    help="emit the shifted calendar with no screen and no draw")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    days = M.trading_days()
    today_syd = datetime.now(M.SYD).date()
    target = a.date or M.next_session(today_syd, days).isoformat()
    tdate = date.fromisoformat(target)
    is_open, open_basis = M.market_open_on(tdate, days)

    rows, total, off_exchange = scan()
    fx = audusd()

    carried = []
    for r in rows:
        sess = M.SESSION_FLAG.get(r.get("earnings_release_time"))
        for field, kind in (("earnings_release_next_date", "next"),
                            ("earnings_release_date", "last")):
            ed, basis = M.sydney_event_date(r.get(field), sess)
            if ed is None or ed.isoformat() != target:
                continue
            carried.append({
                "ticker": r["name"],
                "company": r.get("description"),
                "sector": r.get("sector"),
                "session": sess or "bmo",
                "session_unresolved": sess is None,
                "session_source": ("TradingView earnings_release_time flag "
                                   f"{r.get('earnings_release_time')}"),
                "event_date": target,
                "vendor_date_field": field,
                "vendor_date_kind": kind,
                "event_date_basis": basis,
                "window": M.window_for(sess or "bmo", tdate, days),
                "close": r.get("close"),
                "currency": r.get("currency"),
                "market_cap": r.get("market_cap_basic"),
                "tv_symbol": r.get("tv_symbol"),
                "yahoo_symbol": M.yahoo_symbol(r["name"]),
            })
            break

    out = {
        "market": "AU",
        "event_date": target,
        "market_open": is_open,
        "market_open_basis": open_basis,
        "session_majority": "bmo",
        "window_note": ("91% of ASX results land before the 10:00 Sydney open, so a "
                        "bmo window is close(D-1) -> close(D) and this universe is "
                        "sealed the evening before D."),
        "calendar_source": ("TradingView public scanner (vendor), dates shifted to "
                            "Sydney time -- see au_market.sydney_event_date()"),
        "calendar_rows_total": total,
        "calendar_rows_off_primary_exchange": off_exchange,
        "scheduled_today": len(carried),
        "cap": a.cap,
        "min_turnover_usd": a.min_turnover_usd,
        "fx_audusd": fx,
        "fx_source": f"{M.YQ}/v8/finance/chart/AUDUSD=X",
        "generated_utc": datetime.now(M.UTC).isoformat(timespec="seconds"),
    }

    if is_open is False and not carried:
        out["names"] = []
        out["note"] = (f"The ASX is closed on {target} ({open_basis}). An empty "
                       f"universe here is the "
                       f"exchange being shut, NOT a calendar that failed to load. "
                       f"Nothing to wait for and nothing to hunt.")
    elif not days:
        out["names"] = []
        out["note"] = ("The ASX index tape could not be read, so trading days, "
                       "windows and the register lag are all unreliable. This is a "
                       "container or network fault, not a quiet market. Do not hunt "
                       "on this file.")
    elif a.no_tape:
        out["names"] = carried
        out["note"] = "--no-tape: no screen, no draw"
    else:
        if fx is None:
            out["names"] = []
            out["note"] = ("AUDUSD did not resolve, so every name would be screened "
                           "against a USD floor in the wrong currency. Nothing is "
                           "drawn rather than cut at roughly two thirds of the "
                           "intended bar.")
        else:
            eligible, dropped = [], []
            for r in carried:
                r = dict(r)
                r["tape"] = tape(r["ticker"])
                t = r["tape"]
                turn = t.get("median_turnover_aud_20d")
                if t.get("error") or turn is None:
                    r["drop_reason"] = f"no tape ({t.get('error', 'missing')})"
                    dropped.append(r)
                    continue
                usd = turn * fx
                r["median_turnover_usd_20d"] = round(usd)
                if usd < a.min_turnover_usd:
                    r["drop_reason"] = (f"below the floor: ${usd:,.0f}/day "
                                        f"< ${a.min_turnover_usd:,}")
                    dropped.append(r)
                else:
                    eligible.append(r)

            # One issuer is one event, however many lines it lists.
            eligible, folded = collapse(eligible)

            seed = f"au-{target}"
            rng = random.Random(seed)
            if len(eligible) > a.cap:
                picked = sorted(rng.sample(eligible, a.cap), key=lambda x: x["ticker"])
                method = f"random sample of {len(eligible)} eligible, seed '{seed}'"
            else:
                picked = sorted(eligible, key=lambda x: x["ticker"])
                method = f"all {len(eligible)} eligible names (at or under the cap)"

            unresolved = sum(1 for x in picked if x["session_unresolved"])
            out["selection"] = {"method": method, "seed": seed,
                                "eligible": len(eligible), "dropped": len(dropped),
                                "folded_share_classes": len(folded),
                                "hunted": len(picked),
                                "session_unresolved": unresolved}
            out["eligible_tickers"] = sorted(x["ticker"] for x in eligible)
            out["names"] = picked
            out["dropped"] = dropped
            out["folded"] = folded

    text = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text + "\n", encoding="utf-8")
        s = out.get("selection", {})
        print(f"{target}: {total} scanner rows, {len(carried)} scheduled, "
              f"{s.get('eligible', '-')} eligible, {s.get('hunted', '-')} hunted "
              f"-> {a.out}")
        if out.get("note"):
            print(f"  note: {out['note']}")
    else:
        print(text)


if __name__ == "__main__":
    main()
