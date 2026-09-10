#!/usr/bin/env python3
"""Does the edge hunt call direction, or only rank?

`edge_resolve.py` measures rank correlation, which is the right test for a ranking
and says nothing about whether the sign of a score predicts the sign of the move.
This scores the sign, under the trading scheme `claude_naive` uses so the two
experiments are comparable: buy at 20:00 CET (14:00 ET) on the last session before
the print -- the event date for `amc`, the prior session for `bmo` -- and exit at
the next open (primary) or the next close.

Every rate sits beside its floor. `always_short` is the free rule on the same
events, and this sample skewed down, so a hit rate alone would flatter.

Rows repeated across runs are de-duplicated by (ticker, event_date, session),
keeping the earlier hunt: 09-07 re-hunts five of 09-04's prints and pooling them
would count those events twice.

    python3 edge/scripts/edge_direction.py
    python3 edge/scripts/edge_direction.py --key escore
"""
import argparse
import json
import math
import statistics as st
import sys
import time
from math import comb
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backtest" / "scripts"))


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def ranks(x):
    s = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and x[s[j + 1]] == x[s[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for m in range(i, j + 1):
            r[s[m]] = avg
        i = j + 1
    return r


def pearson(a, b):
    n = len(a)
    ma, mb = st.mean(a), st.mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b))
    return num / den if den else 0.0


def binom_ge(k, n):
    return sum(comb(n, i) * 0.5 ** n for i in range(k, n + 1))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", default="edge/analysis/edge-rows.json")
    ap.add_argument("--key", default="impact_sum",
                    help="the predictor to score: impact_sum, escore, hunter_move")
    ap.add_argument("--cache", default=".edge_direction_cache.json")
    ap.add_argument("--out", default="edge/analysis/edge-direction.json")
    a = ap.parse_args()

    from trade_prices import compute
    cache = json.loads(Path(a.cache).read_text()) if Path(a.cache).exists() else {}
    days = json.loads(Path(a.rows).read_text())

    seen, rows = set(), []
    for d in sorted(days, key=lambda d: d[0]["run"]):
        for r in d:
            b = json.loads((Path(r["run"]) / "baselines" / f"{r['t']}.json").read_text())
            ed, sess = b.get("event_date"), b.get("session", "bmo")
            key = f"{r['t']}|{ed}|{sess}"
            if key in seen:
                continue
            seen.add(key)
            if key not in cache:
                px = compute(r["t"], ed, sess)
                if px.get("error"):
                    alt = compute(r["t"], ed, sess, "60m", "3mo")
                    if not alt.get("error"):
                        alt["fallback_reason"] = px["error"]
                        px = alt
                cache[key] = px
                Path(a.cache).write_text(json.dumps(cache))
                time.sleep(0.3)
            px = cache[key]
            if px.get("error") or r.get(a.key) is None:
                continue
            rows.append({
                "t": r["t"], "day": r["run"].split("/")[-2], "event": ed, "sess": sess,
                "pred": round(r[a.key], 2), "escore": r["escore"],
                "entry": px["entry_1400et"], "open": px["exit_open"],
                "close": px["exit_close"], "ro": px["ret_to_open_pct"],
                "rc": px["ret_to_close_pct"], "drift": px["pre_print_drift_pct"],
                "hit_o": None if r[a.key] == 0 else sign(r[a.key]) == sign(px["ret_to_open_pct"]),
                "hit_c": None if r[a.key] == 0 else sign(r[a.key]) == sign(px["ret_to_close_pct"]),
                "dv": r.get("dollar_vol"),
            })
    rows.sort(key=lambda r: -r["pred"])

    def block(rk, hk):
        v = [r for r in rows if r["pred"] != 0]
        hits = sum(1 for r in v if r[hk])
        tr = [(1 if r["pred"] > 0 else -1) * r[rk] for r in v]
        m, sd = st.mean(tr), st.stdev(tr)
        act = [r[rk] for r in rows]
        pred = [r["pred"] for r in rows]
        return {"n": len(v), "hits": hits, "pct": round(100 * hits / len(v), 1),
                "binom_p": round(binom_ge(hits, len(v)), 3),
                "ret": round(m, 2), "sd": round(sd, 2),
                "t": round(m / (sd / math.sqrt(len(tr))), 2),
                "always_short": round(-st.mean(act), 2),
                "always_long": round(st.mean(act), 2),
                "down": sum(1 for x in act if x < 0),
                "pearson_pred_vs_actual": round(pearson(pred, act), 3),
                "spearman_pred_vs_actual": round(pearson(ranks(pred), ranks(act)), 3),
                "median_abs_error_pp": round(st.median(
                    [abs(p - x) for p, x in zip(pred, act)]), 2)}

    doc = {"predictor": a.key, "n_events": len(rows), "rows": rows,
           "scheme": "buy 14:00 ET the last session before the print; exit next "
                     "open or next close",
           "open": block("ro", "hit_o"), "close": block("rc", "hit_c")}
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n")

    print(f"predictor {a.key}, {len(rows)} de-duplicated events\n")
    print(f"{'exit':12s}{'direction':>14s}{'binom p':>9s}{'ret/trade':>11s}"
          f"{'sd':>7s}{'t':>6s}{'always-short':>14s}")
    for lab, k in (("next open", "open"), ("next close", "close")):
        s = doc[k]
        cell = "{}/{} = {:.0f}%".format(s["hits"], s["n"], s["pct"])
        print(f"{lab:12s}{cell:>14s}"
              f"{s['binom_p']:>9.3f}{s['ret']:>+11.2f}{s['sd']:>7.2f}{s['t']:>6.2f}"
              f"{s['always_short']:>+14.2f}")
    print("\nsize, not sign:")
    for lab, k in (("next open", "open"), ("next close", "close")):
        s = doc[k]
        print(f"  {lab:12s} pearson {s['pearson_pred_vs_actual']:+.3f}  "
              f"spearman {s['spearman_pred_vs_actual']:+.3f}  "
              f"median |error| {s['median_abs_error_pp']:.2f}pp")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
