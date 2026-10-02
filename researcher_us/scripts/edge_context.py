#!/usr/bin/env python3
"""Three context labels per name, for the reader: retail tilt, search attention and
recent volatility.

INFORMATION ONLY (operator's instruction, 2026-10-02). Nothing ranks, selects, sizes or
trades on this file. `alpaca_trade.py`, `edge_score.py`, the dashboard and every
resolver ignore it; `scripts/score_report.py` prints it as two columns beside the key so
a reader sees, for every name and whatever its score, whether the two conditions the
hypothesis register found the hunt doing better under are present.

  retail   `retail_tilt` >= 50, the dashboard's definition (dashboard/scripts/
           build_ledger.py): the mean of four percentiles, churn (20-day dollar volume
           over market cap), small market cap, low share price and 20-day realised
           volatility. The percentiles are taken against the names already in
           `dashboard/data/ledger.json`, which is the reference the dashboard ranks
           against, so the label can differ slightly from the one the dashboard prints
           once it has rebuilt with today's names in it.
  search   Google Trends spike below 1.0x, `weighting.SEARCH_SPLIT`: the day's interest
           over the name's own 90-day median (+1). Same query rule as
           edge_search_volume.py: the company name minus its legal suffix, never the
           ticker. `sparse` and `silent` mean Google reports too little for a baseline;
           that is no label at all, not a quiet name.
  vol      20-day realised volatility, annualised, at or above VOL_SPLIT = 58%, from
           the sealed baseline's tape. Added 2026-10-02 on the operator's instruction and
           FROZEN at that value: the only measured indicator that tracked the hit rate
           (research/analyses/signal-vs-noise/: the book's top volatility third, which
           starts near 58%, was right 82% of the time against 45-50%), but in the live
           sample it did not raise the return per name. The split was read off those
           days, so it is a forward test, never a filter. Do not re-tune it.

TODAY IS STILL BEING COUNTED. At run time Google flags the entry day as partial, and a
partial day reads low, which would call every name quiet. So the spike is taken on the
LAST COMPLETE day (normally the day before entry) and `search.basis` says which day.
The dashboard's own `search_spike` is computed later on the full entry day and can
disagree. This script never writes `researcher_us/analysis/trends-cache.json`: a partial
day cached under that key would corrupt the after-the-fact measurement.

What the two labels rest on, so nobody reads more into them than is there: above the
conviction floor, 13-22 days in sample, retail 71.8% against 39.1% right and quiet
search 71.4% against 50.0%, neither clearing |t| = 2; below the floor neither turns the
sign usable (research/analyses/below-floor-factors/).

    python3 researcher_us/scripts/edge_context.py --run <RUN>/edge
    python3 researcher_us/scripts/edge_context.py --run <RUN>/edge --no-search

Writes <RUN>/edge-context.json. Exits 0 when the retail half worked, whatever search did.
"""
import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "dashboard" / "scripts"))

import edge_search_volume as SV   # noqa: E402
import weighting as W             # noqa: E402

LEDGER = REPO / "dashboard" / "data" / "ledger.json"
VOL_SPLIT = 58.0      # frozen 2026-10-02, see the docstring
OUT = "edge-context.json"


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def tape_of(run, ticker):
    b = load(Path(run) / "baselines" / f"{ticker}.json") or {}
    t = b.get("tape") or {}
    spot = t.get("spot") or b.get("spot")
    vol = next((t[k] for k in ("avg_volume_20d", "adv_20d", "avg_vol_20d") if t.get(k)), None)
    return {"spot": spot, "realised_vol_20d": t.get("realised_vol_20d_annualised_pct"),
            "dollar_vol": (spot * vol) if spot and vol else None}


def reference(run):
    """The ledger's names, minus this run's own rows: the same population the dashboard
    takes its percentiles over."""
    d = load(LEDGER) or {}
    here = str(Path(run).resolve().relative_to(REPO)) if Path(run).resolve().is_relative_to(REPO) else None
    ref = {"churn_pct": [], "market_cap_usd": [], "spot": [], "realised_vol_20d": []}
    for r in d.get("names") or []:
        if r.get("duplicate_event") or (here and r.get("run") == here):
            continue
        for k in ref:
            if r.get(k) is not None:
                ref[k].append(r[k])
    return ref


def pct(x, vals, invert=False):
    if x is None or not vals:
        return None
    p = 100 * sum(1 for v in vals if v < x) / len(vals)
    return round(100 - p if invert else p, 1)


def retail(row, ref):
    churn = (100 * row["dollar_vol"] / row["market_cap_usd"]
             if row.get("dollar_vol") and row.get("market_cap_usd") else None)
    parts = {"churn": pct(churn, ref["churn_pct"]),
             "small_cap": pct(row.get("market_cap_usd"), ref["market_cap_usd"], True),
             "low_price": pct(row.get("spot"), ref["spot"], True),
             "volatility": pct(row.get("realised_vol_20d"), ref["realised_vol_20d"])}
    vals = [v for v in parts.values() if v is not None]
    tilt = round(sum(vals) / len(vals), 1) if len(vals) >= 2 else None
    return {"retail_tilt": tilt, "parts": parts,
            "favourable": None if tilt is None else tilt >= W.RETAIL_SPLIT}


def search(company, ticker, day):
    q = SV.query_for(company, ticker)
    end = datetime.fromisoformat(day).date()
    pts, err = SV.fetch_series(q, (end - timedelta(days=89)).isoformat(), end.isoformat(),
                               tries=2, partial=True)
    if err or not pts:
        return {"query": q, "state": "failed", "favourable": None, "why": err}
    done = [(dt, v) for dt, v, part in pts if not part]
    partial_today = next((v for dt, v, part in pts if part), None)
    m = SV.measures(done)
    if m.get("unusable"):
        return {"query": q, "state": m["unusable"], "favourable": None}
    try:
        basis = datetime.strptime(done[-1][0], "%b %d, %Y").date().isoformat()
    except (ValueError, TypeError):
        basis = str(done[-1][0])
    return {"query": q, "state": "measured", "spike": m["spike_day"], "basis": basis,
            "median_90d": m["level_median_90d"], "partial_today": partial_today,
            "favourable": m["spike_day"] < W.SEARCH_SPLIT}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--no-search", action="store_true", help="retail only, no network")
    ap.add_argument("--budget-seconds", type=float, default=240,
                    help="stop querying Google after this long; the rest read `budget`")
    a = ap.parse_args()

    run = Path(a.run)
    uni = load(run / "universe.json") or {}
    rows = uni.get("names") or uni.get("rows") or []
    key = load(run / "edge-scores.json") or {}
    ranked = [r["ticker"] for r in key.get("ranking", [])]
    if ranked:                       # the names the table prints, in its order
        byt = {r["ticker"]: r for r in rows}
        rows = [byt.get(t, {"ticker": t}) for t in ranked]
    if not rows:
        print(f"no names in {run}", file=sys.stderr)
        sys.exit(1)

    day = run.parent.name
    ref = reference(run)
    t0 = time.monotonic()
    out = []
    for r in rows:
        t = r["ticker"]
        row = {"ticker": t, "company": r.get("company"),
               "market_cap_usd": r.get("market_cap_usd"), **tape_of(run, t)}
        row["retail"] = retail(row, ref)
        rv = row.get("realised_vol_20d")
        row["vol"] = {"realised_vol_20d": rv,
                      "high": None if rv is None else rv >= VOL_SPLIT}
        if a.no_search:
            row["search"] = {"state": "not_run", "favourable": None}
        elif time.monotonic() - t0 > a.budget_seconds:
            row["search"] = {"state": "budget", "favourable": None}
        else:
            row["search"] = search(r.get("company"), t, day)
            time.sleep(2.5)          # Trends rate-limits hard
        out.append(row)
        rt, s = row["retail"], row["search"]
        print(f"  {t:7s} retail {rt['retail_tilt'] if rt['retail_tilt'] is not None else 'n/a':>5}"
              f" {'yes' if rt['favourable'] else ('no' if rt['favourable'] is False else '?'):3s}"
              f"   vol {row['vol']['realised_vol_20d'] if row['vol']['realised_vol_20d'] is not None else 'n/a':>5}"
              f"   search {s['state']:9s}"
              + (f" {s['spike']:.2f}x on {s['basis']}" if s.get("spike") is not None else ""))

    res = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "run": str(run), "use": "information only: nothing ranks, selects, sizes or "
                                   "trades on this file",
           "spec": {"retail_split": W.RETAIL_SPLIT, "search_split": W.SEARCH_SPLIT,
                    "vol_split": VOL_SPLIT,
                    "retail_reference_n": {k: len(v) for k, v in ref.items()},
                    "search_basis": "last complete Google Trends day before the run"},
           "names": out}
    (run / OUT).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {run / OUT}")


if __name__ == "__main__":
    main()
