#!/usr/bin/env python3
"""Draw the event sample, and commit it before anything is harvested.

Order matters. Enumerate the complete universe first, apply filters that are
written down in advance, then draw with a fixed seed and write the manifest. A
sample chosen after looking at results is not a sample, and the temptation to
quietly drop an awkward name is much easier to resist when the draw is already
on disk with its seed next to it.

Exclusions, all decided before seeing any outcome:

  * session unresolved, or 'intraday' -- the measurement window is undefined
  * no bar on the event date, or the window runs past available data
  * a corporate action inside the measurement window (truth.py flags it)
  * fewer than 4 prior earnings reactions -- nothing to size a move against

Stratification is on session and market-cap band only. Retail interest almost
certainly matters more -- the informal layer is thin for enterprise names and
presumably rich for consumer ones (FINDINGS section 21) -- but every cheap proxy
for it costs an API call per candidate, and spending the budget on screening
rather than harvesting is the wrong trade at this size. Instead the StockTwits
message count is recorded per event during the build, so the sample can be split
on it afterwards. That is weaker than stratifying, and it is stated here rather
than hidden.
"""
import argparse, json, random, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT
import truth

CAP_BANDS = [(2e9, 10e9, "small"), (10e9, 50e9, "mid"), (50e9, 1e15, "large")]


def band(cap):
    for lo, hi, name in CAP_BANDS:
        if lo <= cap < hi:
            return name
    return "micro"


def eligible(ev, verify_prices=True):
    """Return (ok, reason). Reason is recorded for every exclusion."""
    if ev.get("session") not in ("amc", "bmo"):
        return False, f"session {ev.get('session')!r}"
    if not ev.get("event_date"):
        return False, "no event date"
    if ev.get("market_cap_usd_today", 0) < 2e9:
        return False, "below cap floor"
    if not ev.get("cik"):
        return False, "no CIK"
    if not verify_prices:
        return True, None
    t = truth.move(ev["ticker"], ev["event_date"], ev["session"])
    if "error" in t:
        return False, f"price: {t['error']}"
    if t.get("corporate_action_in_window"):
        return False, "corporate action inside measurement window"
    return True, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True, help="output of events.py")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--exclude", default="", help="comma list of tickers already done")
    ap.add_argument("--out", default=str(ROOT / "runs"))
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--no-verify-prices", action="store_true")
    a = ap.parse_args()

    allev = json.load(open(a.events, encoding="utf-8"))
    already = {t.strip().upper() for t in a.exclude.split(",") if t.strip()}

    kept, dropped, seen = [], [], set()
    for ev in allev:
        key = (ev["ticker"], ev.get("event_date"))
        if ev["ticker"] in already:
            dropped.append({**{k: ev[k] for k in ("ticker", "event_date")},
                            "reason": "already harvested"}); continue
        if key in seen:
            dropped.append({"ticker": ev["ticker"], "event_date": ev.get("event_date"),
                            "reason": "duplicate"}); continue
        seen.add(key)
        ok, why = eligible(ev, not a.no_verify_prices)
        (kept if ok else dropped).append(ev if ok else
                                         {"ticker": ev["ticker"],
                                          "event_date": ev.get("event_date"),
                                          "reason": why})

    strata = defaultdict(list)
    for ev in kept:
        strata[(ev["session"], band(ev["market_cap_usd_today"]))].append(ev)

    rng = random.Random(a.seed)
    for v in strata.values():
        v.sort(key=lambda e: (e["ticker"], e["event_date"] or ""))
        rng.shuffle(v)

    # proportional allocation, then round-robin the remainder so a thin stratum
    # is not silently zeroed out
    total = sum(len(v) for v in strata.values())
    draw, keys = [], sorted(strata, key=lambda k: (-len(strata[k]), k))
    quota = {k: min(len(strata[k]), int(a.n * len(strata[k]) / max(total, 1))) for k in keys}
    for k in keys:
        draw += strata[k][:quota[k]]
    i = 0
    while len(draw) < a.n and any(len(strata[k]) > quota[k] for k in keys):
        k = keys[i % len(keys)]
        if len(strata[k]) > quota[k]:
            draw.append(strata[k][quota[k]]); quota[k] += 1
        i += 1
    draw = draw[:a.n]

    outdir = Path(a.out) / a.run_id
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_id": a.run_id, "seed": a.seed, "n_requested": a.n, "n_drawn": len(draw),
        "source_events": a.events, "universe_size": len(allev),
        "eligible": len(kept), "excluded": len(dropped),
        "exclusion_reasons": dict(Counter(d["reason"] for d in dropped).most_common()),
        "strata_available": {f"{k[0]}/{k[1]}": len(v) for k, v in sorted(strata.items())},
        "strata_drawn": dict(Counter(f"{e['session']}/{band(e['market_cap_usd_today'])}"
                                     for e in draw).most_common()),
        "stratified_on": ["session", "market_cap_band"],
        "not_stratified_on": ["retail_interest -- recorded per event during build, "
                              "see draw.py docstring"],
        "already_harvested": sorted(already),
        "events": draw,
        "excluded_detail": dropped,
    }
    (outdir / "draw.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"universe {len(allev)} -> eligible {len(kept)} -> drawn {len(draw)}")
    print(f"strata drawn: {manifest['strata_drawn']}")
    print(f"top exclusions: {list(manifest['exclusion_reasons'].items())[:6]}")
    print(f"-> {outdir / 'draw.json'}")


if __name__ == "__main__":
    main()
