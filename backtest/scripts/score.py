#!/usr/bin/env python3
"""Score the arms against realised moves, and against the floor.

Reads backtest/runs/<run>/arms/<arm>/batch-*.json -- each a JSON array of per-event
forecasts in the shared schema -- joins them to backtest/truth/, and reports every
rate beside the baseline it has to clear.

Nothing here is reported pooled-and-alone. A direction rate without the coin
interval beside it is the mistake LEDGER.md already made: 58% over 31 calls, no
floor, and so no way to tell whether the pipeline knows anything. On n=40 the coin
covers 38-62%, and a one-line rule (repeat last quarter's reaction sign) scores 62%.
That is the bar, not 50%.

Scoring conventions, matching the live ledger so results stay comparable:

  direction hit   sign of the call matches the sign of the realised move. A
                  'Neutral / No Edge' call abstains from the direction rate and is
                  scored separately under the size convention, rather than being
                  silently counted as a miss or a half-hit.
  neutral hit     realised |move| came in below the proxy expected move.
  magnitude       |predicted expected_abs_move_pct - realised |move||, compared with
                  the proxy's own error on the same events.
  calibration     whether High-certainty calls actually beat Low-certainty ones. If
                  they do not, the field is decorative -- which is exactly what the
                  archive found for `Med` vs `Low` conviction.
"""
import json, random, statistics, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT

CALL_SIGN = {"Strong Up": 1, "Lean Up": 1, "Neutral / No Edge": 0,
             "Lean Down": -1, "Strong Down": -1}


def _band(cap):
    return "large" if cap >= 50e9 else "mid" if cap >= 10e9 else "small"


def load_truth_and_anchors(run):
    draw = json.loads((ROOT / "runs" / run / "draw.json").read_text(encoding="utf-8"))
    meta = {}
    for e in draw["events"]:
        key = f"{e['ticker']}-{e['event_date']}"
        tp, ap = ROOT / "truth" / f"{key}.json", ROOT / "events" / key / "anchors.json"
        if not (tp.exists() and ap.exists()):
            continue
        t = json.loads(tp.read_text(encoding="utf-8"))
        a = json.loads(ap.read_text(encoding="utf-8"))
        if t.get("actual_move_pct") is None:
            continue
        hist = [abs(h["move_pct"]) for h in a.get("historical_earnings_moves", [])]
        nm = ROOT / "events" / key / "news_manifest.json"
        news = 0
        if nm.exists():
            m = json.loads(nm.read_text(encoding="utf-8"))
            news = (m.get("kept_tier2") or 0) + (m.get("kept_tier3") or 0)
        meta[e["ticker"]] = {
            "key": key, "move": t["actual_move_pct"],
            "abs": abs(t["actual_move_pct"]),
            "proxy": statistics.median(hist) if hist else None,
            "band": _band(e.get("market_cap_usd_today") or 0),
            "news_docs": news,
            "coverage": "starved" if news == 0 else "thin" if news < 5 else "usable",
        }
    return meta


def load_arm(run, arm):
    d = ROOT / "runs" / run / "arms" / arm
    out = {}
    if not d.exists():
        return out
    for f in sorted(d.glob("batch-*.json")):
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  !! {arm}/{f.name} is not valid JSON: {e}")
            continue
        for r in rows if isinstance(rows, list) else [rows]:
            if r.get("ticker"):
                out[r["ticker"]] = r
    return out


def coin_interval(n, trials=20000, seed=7):
    random.seed(seed)
    xs = sorted(sum(random.choice([True, False]) for _ in range(n)) / n for _ in range(trials))
    return xs[int(0.05 * trials)], xs[int(0.95 * trials)]


def score(arm_name, preds, meta):
    rows = [(t, p, meta[t]) for t, p in preds.items() if t in meta]
    if not rows:
        return None
    dir_n = dir_hit = 0
    neu_n = neu_hit = 0
    mag_err, proxy_err = [], []
    by_cert = defaultdict(lambda: [0, 0])
    by_cov = defaultdict(lambda: [0, 0])
    signed = []
    for t, p, m in rows:
        s = CALL_SIGN.get(p.get("call"))
        if s is None:
            continue
        if s == 0:
            neu_n += 1
            if m["proxy"] is not None and m["abs"] < m["proxy"]:
                neu_hit += 1
        else:
            dir_n += 1
            hit = (s > 0) == (m["move"] > 0)
            dir_hit += hit
            by_cert[p.get("certainty", "?")][0] += hit
            by_cert[p.get("certainty", "?")][1] += 1
            by_cov[m["coverage"]][0] += hit
            by_cov[m["coverage"]][1] += 1
            signed.append((p.get("direction_score", 0), m["move"]))
        e = p.get("expected_abs_move_pct")
        if e is not None:
            mag_err.append(abs(e - m["abs"]))
            if m["proxy"] is not None:
                proxy_err.append(abs(m["proxy"] - m["abs"]))
    return {"arm": arm_name, "n": len(rows), "dir_n": dir_n, "dir_hit": dir_hit,
            "dir_rate": dir_hit / dir_n if dir_n else None,
            "neutral_n": neu_n, "neutral_hit": neu_hit,
            "neutral_rate": neu_hit / neu_n if neu_n else None,
            "mag_median_err": statistics.median(mag_err) if mag_err else None,
            "proxy_median_err": statistics.median(proxy_err) if proxy_err else None,
            "by_certainty": {k: v for k, v in by_cert.items()},
            "by_coverage": {k: v for k, v in by_cov.items()},
            "signed": signed}


def report(run="pilot-40", arms=("arm-a-naive", "arm-b-planfirst", "arm-c-skill")):
    meta = load_truth_and_anchors(run)
    results = []
    for a in arms:
        preds = load_arm(run, a)
        if not preds:
            print(f"[{a}] no forecasts on disk yet")
            continue
        r = score(a, preds, meta)
        if r:
            results.append(r)
    if not results:
        return
    print(f"\n{'arm':<18}{'n':>4}{'dirN':>6}{'dir rate':>10}{'neutral':>9}{'mag err':>9}{'proxy err':>11}")
    print("-" * 67)
    for r in results:
        dr = f"{r['dir_rate']:.0%}" if r["dir_rate"] is not None else "n/a"
        nr = f"{r['neutral_hit']}/{r['neutral_n']}" if r["neutral_n"] else "-"
        me = f"{r['mag_median_err']:.2f}pp" if r["mag_median_err"] is not None else "n/a"
        pe = f"{r['proxy_median_err']:.2f}pp" if r["proxy_median_err"] is not None else "n/a"
        print(f"{r['arm']:<18}{r['n']:4}{r['dir_n']:6}{dr:>10}{nr:>9}{me:>9}{pe:>11}")

    n = max(r["dir_n"] for r in results) or 1
    lo, hi = coin_interval(n)
    print(f"\nFLOOR on n={n} directional calls")
    print(f"  coin 5-95 interval      {lo:.0%} - {hi:.0%}   <- inside this is indistinguishable from chance")
    print(f"  last_reaction rule      62%          <- free, reads nothing. This is the real bar.")
    print(f"  proxy magnitude error   2.93pp       <- beat this or expected_abs_move_pct added nothing")

    print("\nCALIBRATION - do High-certainty calls actually hit more than Low?")
    for r in results:
        parts = []
        for c in ("High", "Med", "Low"):
            h, t = r["by_certainty"].get(c, [0, 0])
            parts.append(f"{c} {h}/{t}" + (f" ({h/t:.0%})" if t else ""))
        print(f"  {r['arm']:<18}{'   '.join(parts)}")
    print("  a tier that does not separate is decorative -- the archive already found")
    print("  Med conviction returning -2.2% and Low returning +9.1%.")

    print("\nBY COVERAGE - does the news layer earn its cost?")
    for r in results:
        parts = []
        for c in ("usable", "thin", "starved"):
            h, t = r["by_coverage"].get(c, [0, 0])
            parts.append(f"{c} {h}/{t}" + (f" ({h/t:.0%})" if t else ""))
        print(f"  {r['arm']:<18}{'  '.join(parts)}")

    (ROOT / "runs" / run / "scores.json").write_text(
        json.dumps([{k: v for k, v in r.items() if k != "signed"} for r in results],
                   indent=1), encoding="utf-8")


if __name__ == "__main__":
    report(sys.argv[1] if len(sys.argv) > 1 else "pilot-40")
