#!/usr/bin/env python3
"""Does the edge hunt predict anything once you only keep the big calls?

The rank question (section 41) came back null. This asks a different one: take
only names where the prediction clears some size, treat the sign as a directional
call, and score it as a call rather than as an ordering.

Two predictors, because they are not the same claim:

  hunter    `expected_move_pct` from the hunt file -- what the hunter thought the
            stock would do, before the adversary discounted anything
  edge      `edge_pct` from the scorer -- what survives the adversary's priced-in
            estimate. Much smaller: the adversary put the median finding at 78%
            already priced, so a 5% hunter call becomes a ~1% edge

Reported against floors, never alone. FINDINGS.md section 1 and `baselines.py`
both make the point that a hit rate with nothing beside it is unreadable:

  coin           50%, and at these n the interval is wide
  always_up      the sign of equity drift on this sample
  always_down    its mirror
  base           the majority direction actually realised in the subset, which is
                 the number a constant call would have scored on exactly the names
                 the threshold selected. This is the honest floor for a filter:
                 a filter that only picks names that went up looks skilful and is
                 not.

**The whole threshold curve is printed, not one cut.** Picking a threshold after
seeing the outcomes is how a null becomes a finding, and the only defence is to
show every cut so a reader can see whether one is special or was chosen. Nothing
here carries a corrected p-value and none should be read as significant: this is
the ninth-odd subset tested on the same 104 names.

    python3 backtest/scripts/edge_corpus_threshold.py
"""
import argparse
import json
import random
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs" / "edge-corpus"
SHARE_CLASS_DROP = {"BF.A", "WLYB"}


def rows():
    out = []
    for outp in sorted(RUNS.glob("*/edge-outcome.json")):
        day = outp.parent.name
        doc = json.loads(outp.read_text(encoding="utf-8"))
        scores = {r["ticker"]: r for r in json.loads(
            (outp.parent / "edge-scores.json").read_text(encoding="utf-8"))["ranking"]}
        for d in doc.get("per_day", []):
            for r in (d.get("rows") or []):
                if r.get("outcome") != "resolved" or r["ticker"] in SHARE_CLASS_DROP:
                    continue
                h = outp.parent / "hunts" / f"{r['ticker']}.json"
                hunter = None
                if h.exists():
                    hunter = json.loads(h.read_text(encoding="utf-8")).get(
                        "expected_move_pct")
                sc = scores.get(r["ticker"], {})
                man = json.loads((outp.parent / "manifest.json").read_text(
                    encoding="utf-8"))
                ev = next((e for e in man["events"]
                           if e["ticker"] == r["ticker"]), {})
                out.append({
                    "day": day, "ticker": r["ticker"],
                    "hunter_pct": hunter, "edge_pct": sc.get("edge_pct"),
                    "move_pct": r["move_pct"],
                    "deadband_pct": r.get("deadband_pct"),
                    "corpus_type": corpus_type(ROOT.parent / ev["capture"])
                    if ev.get("capture") else "unknown",
                })
    return out


def corpus_type(cap):
    """A capture that ran no news query holds an EDGAR index and retail chatter.

    95 of the 109 names are like that (section 36), and a hunt over one of them is
    not the same experiment as a hunt over a capture with a news channel.
    """
    for s in (cap / "snapshots").glob("*.json"):
        try:
            for it in (json.loads(s.read_text(encoding="utf-8")).get("items") or []):
                if it.get("kind") == "news":
                    return "news_bearing"
        except Exception:
            continue
    return "filings_only"


def binom_p(hits, n, p0=0.5, seed=11, draws=20000):
    """Two-sided, by simulation, so no scipy and no normal approximation at n=9."""
    rng = random.Random(seed)
    obs = abs(hits - n * p0)
    ge = sum(1 for _ in range(draws)
             if abs(sum(1 for _ in range(n) if rng.random() < p0) - n * p0) >= obs)
    return round((ge + 1) / (draws + 1), 4)


def score(sel, label):
    if not sel:
        return {"label": label, "n": 0}
    hits = sum(1 for r in sel if (r["pred"] > 0) == (r["move_pct"] > 0))
    ups = sum(1 for r in sel if r["move_pct"] > 0)
    base = max(ups, len(sel) - ups) / len(sel)
    ret = [r["move_pct"] if r["pred"] > 0 else -r["move_pct"] for r in sel]
    # Outside the deadband only: a move the baseline calls no-direction is not a
    # direction the call can have got right.
    live = [r for r in sel
            if r.get("deadband_pct") is None
            or abs(r["move_pct"]) >= r["deadband_pct"]]
    lh = sum(1 for r in live if (r["pred"] > 0) == (r["move_pct"] > 0))
    return {
        "label": label, "n": len(sel),
        "hit": hits, "hit_rate": round(hits / len(sel), 3),
        "p_vs_coin": binom_p(hits, len(sel)),
        "base_rate": round(base, 3),
        "always_up": round(ups / len(sel), 3),
        "ret_per_trade": round(st.mean(ret), 2),
        "ret_total": round(sum(ret), 1),
        "ret_sd": round(st.pstdev(ret), 2) if len(ret) > 1 else None,
        "n_outside_deadband": len(live),
        "hit_outside_deadband": (round(lh / len(live), 3) if live else None),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--corpus", choices=["news_bearing", "filings_only"],
                    help="restrict to captures of this type")
    a = ap.parse_args()

    data = rows()
    if a.corpus:
        data = [r for r in data if r["corpus_type"] == a.corpus]
    out = {"names": len(data), "predictors": {}}

    for key, name in [("hunter_pct", "hunter expected_move_pct"),
                      ("edge_pct", "edge_pct (after adversary discount)")]:
        blocks = []
        vals = [abs(r[key]) for r in data if r.get(key) is not None]
        cuts = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]
        if vals:
            cuts = [c for c in cuts if c <= max(vals)]
        for c in cuts:
            sel = [{**r, "pred": r[key]} for r in data
                   if r.get(key) is not None and abs(r[key]) >= c and r[key] != 0]
            blocks.append(score(sel, f"|pred| >= {c:.1f}%"))
        out["predictors"][name] = blocks

    out["corpus_filter"] = a.corpus or "all"
    name = f"threshold-report{'-' + a.corpus if a.corpus else ''}.json"
    (RUNS / name).write_text(
        json.dumps(out, indent=1) + "\n", encoding="utf-8")

    if a.json:
        print(json.dumps(out, indent=1))
        return

    print(f"=== directional value of the edge hunt's own size estimates, "
          f"{len(data)} resolved names ===")
    for name, blocks in out["predictors"].items():
        print(f"\n--- {name}")
        print(f"{'cut':>12s} {'n':>4s} {'hit':>5s} {'rate':>6s} {'p':>7s} "
              f"{'base':>6s} {'up%':>6s} {'ret/trade':>10s} {'sd':>7s} "
              f"{'n>dead':>7s} {'hit>dead':>9s}")
        for b in blocks:
            if not b["n"]:
                continue
            hd = f"{b['hit_outside_deadband']:.3f}" if b["hit_outside_deadband"] is not None else "--"
            print(f"{b['label']:>12s} {b['n']:4d} {b['hit']:5d} {b['hit_rate']:6.3f} "
                  f"{b['p_vs_coin']:7.4f} {b['base_rate']:6.3f} {b['always_up']:6.3f} "
                  f"{b['ret_per_trade']:+10.2f} {str(b['ret_sd']):>7s} "
                  f"{b['n_outside_deadband']:7d} {hd:>9s}")
    print("\nNo p-value here is corrected for the number of cuts shown, and the "
          "whole curve is printed precisely so no single cut can be read as a "
          "result on its own.")


if __name__ == "__main__":
    main()
