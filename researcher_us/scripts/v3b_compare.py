#!/usr/bin/env python3
"""Stage E-P v3b against stage E-P, pooled, on the names both ranked the same day.

The question (operator, 2026-11-14): does the v3b searcher and judge brief predict the
earnings reaction better than the current stage E-P? The pre-registration is
research/analyses/us-panel-v3-information/PREREGISTRATION.md; this script computes
exactly what it names and nothing chosen after seeing the data.

Per stage, on the COMMON names of every day both stages ran (a name only one stage
ranked is reported as a count and left out of every comparison):

  primary    rho_scaled: within-day pooled Spearman of panel_pct_signed against the
             realised move divided by the sealed expected move (day fixed effect:
             each day's ranks are centred, as edge_resolve.pooled_within_days does).
             Paired difference v3b - E-P with a day bootstrap (resample days).
  secondary  rho_raw (the same on the raw move); the book at panel_pct >= 80 (all four
             judges) and the band at >= 60: n, hit rate, mean side return, and the
             same on the scaled move; the judges' mean p_up: Brier score and its
             spread across names (resolution), against the sign of the move.
  v3b only   the judges' three-part forecast: the mean over judges of
             p x move_if_clears + (1 - p) x move_if_misses, ranked like the primary;
             and the share of evidence items per evidence_type.

The window is edge_resolve.realised(): the close before the print to the close after
the first full session following it. Gross of costs. Moves are cached in
research/analyses/us-panel-v3-information/moves-cache.json so a rerun does not refetch.

  python3 researcher_us/scripts/v3b_compare.py            # every day both ran
  python3 researcher_us/scripts/v3b_compare.py --offline  # cache only, no fetch
"""
import argparse
import glob
import json
import random
import statistics as st
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import edge_resolve as ER  # noqa: E402

OUT = ROOT / "research" / "analyses" / "us-panel-v3-information"
CACHE = OUT / "moves-cache.json"
STAGES = {"E-P": "edge-panel", "E-P v3b": "edge-panel-v3b"}
BOOK, BAND = 80.0, 60.0


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sgn(x):
    return (x > 0) - (x < 0)


def rows_of(run):
    """ticker -> panel row of a run's edge-scores-panel.json."""
    d = load(Path(run) / "edge-scores-panel.json") or {}
    return {r["ticker"]: r for r in d.get("ranking") or []}


def judge_files(run):
    out = {}
    for f in sorted((Path(run) / "panel").glob("*.json")):
        if f.name.startswith("packs"):
            continue
        try:
            for o in json.loads(f.read_text(encoding="utf-8")):
                out.setdefault(o["id"].split("/")[-1], []).append(o)
        except (ValueError, TypeError, KeyError):
            continue
    return out


def day_runs():
    days = []
    for v3b in sorted(glob.glob(str(ROOT / "research/*/*/*/edge-panel-v3b"))):
        ep = Path(v3b).parent / "edge-panel"
        if (Path(v3b) / "edge-scores-panel.json").exists() and (ep / "edge-scores-panel.json").exists():
            days.append((Path(v3b).parent.name, ep, Path(v3b)))
    return days


def move_for(cache, run, t, offline):
    b = load(Path(run) / "baselines" / f"{t}.json") or {}
    key = f"{b.get('event_date')}|{b.get('session')}|{t}"
    if key in cache:
        return cache[key], b
    if offline or not b.get("event_date"):
        return None, b
    try:
        res, _ = ER.realised(t, b["event_date"], b.get("session", "bmo"))
    except Exception:
        res = None
    if res:
        cache[key] = res["move_pct"]
    return (res or {}).get("move_pct"), b


def pooled(days, key, target):
    """Within-day pooled Spearman: centred ranks per day, then one correlation."""
    A, B = [], []
    for rows in days:
        v = [r for r in rows if r.get(key) is not None and r.get(target) is not None]
        if len(v) < 3:
            continue
        A += ER.centred_ranks([r[key] for r in v])
        B += ER.centred_ranks([r[target] for r in v])
    if len(A) < 3:
        return None
    mx, my = st.fmean(A), st.fmean(B)
    num = sum((a - mx) * (b - my) for a, b in zip(A, B))
    dx = sum((a - mx) ** 2 for a in A) ** .5
    dy = sum((b - my) ** 2 for b in B) ** .5
    return round(num / (dx * dy), 3) if dx and dy else None


def book(rows, stage, floor):
    picked = [r for r in rows if r[stage]["full"] and r[stage]["pct"] >= floor and r[stage]["side"]]
    rets = [r[stage]["side"] * r["move"] for r in picked]
    sc = [r[stage]["side"] * r["scaled"] for r in picked if r["scaled"] is not None]
    if not rets:
        return {"n": 0}
    return {"n": len(rets), "hit": round(sum(x > 0 for x in rets) / len(rets), 3),
            "mean_ret_pct": round(st.fmean(rets), 2),
            "t": round(st.fmean(rets) / (st.stdev(rets) / len(rets) ** .5), 2) if len(rets) > 2 and st.stdev(rets) else None,
            "mean_scaled": round(st.fmean(sc), 3) if sc else None}


def brier(rows, stage):
    xs = [(r[stage]["p_up"] / 100.0, 1.0 if r["move"] > 0 else 0.0) for r in rows
          if r[stage]["p_up"] is not None and r["move"] != 0]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "brier": round(st.fmean((p - y) ** 2 for p, y in xs), 4),
            "p_up_sd": round(st.pstdev([p * 100 for p, _ in xs]), 2)}


def bootstrap_delta(by_day, key_a, key_b, target, n=2000, seed=7):
    days = list(by_day)
    if len(days) < 2:
        return None
    rnd = random.Random(seed)
    ds = []
    for _ in range(n):
        smp = [by_day[rnd.choice(days)] for _ in days]
        a, b = pooled(smp, key_b, target), pooled(smp, key_a, target)
        if a is not None and b is not None:
            ds.append(a - b)
    if not ds:
        return None
    ds.sort()
    return {"mean": round(st.fmean(ds), 3), "lo90": round(ds[int(.05 * len(ds))], 3),
            "hi90": round(ds[int(.95 * len(ds)) - 1], 3), "p_gt0": round(sum(d > 0 for d in ds) / len(ds), 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="read moves from the cache only")
    a = ap.parse_args()
    cache = load(CACHE) or {}
    by_day, only, types = {}, Counter(), Counter()
    for day, ep, v3 in day_runs():
        R = {"E-P": rows_of(ep), "E-P v3b": rows_of(v3)}
        J = judge_files(v3)
        for h in v3.glob("hunts/*.json"):
            d = load(h) or {}
            for f in (d.get("findings") or []) + (d.get("outside_window") or []) + (d.get("rejected_candidates") or []):
                if isinstance(f, dict):
                    types[f.get("evidence_type") or "untagged"] += 1
        common = sorted(set(R["E-P"]) & set(R["E-P v3b"]))
        only["E-P only"] += len(set(R["E-P"]) - set(common))
        only["v3b only"] += len(set(R["E-P v3b"]) - set(common))
        rows = []
        for t in common:
            mv, b = move_for(cache, v3, t, a.offline)
            if mv is None:
                only["unresolved common"] += 1
                continue
            em = b.get("expected_move_pct")
            row = {"day": day, "ticker": t, "move": mv,
                   "scaled": round(mv / em, 3) if em else None}
            for s in STAGES:
                r = R[s][t]
                mem = r.get("members") or {}
                pu = [m.get("p_up") for m in mem.values() if m.get("p_up") is not None]
                row[s] = {"pct_signed": r.get("panel_pct_signed"), "pct": r.get("panel_pct") or 0.0,
                          "side": r.get("side") or 0, "full": r.get("n_members") == 4,
                          "p_up": st.fmean(pu) if pu else None}
                row[f"key {s}"] = r.get("panel_pct_signed")
            ev = []
            for o in J.get(t, []):
                p = o.get("parts") or {}
                try:
                    q = float(p["p_clears_real_bar"]) / 100
                    ev.append(q * float(p["move_if_clears_pct"]) + (1 - q) * float(p["move_if_misses_pct"]))
                except (KeyError, TypeError, ValueError):
                    pass
            row["key v3b parts"] = st.fmean(ev) if ev else None
            rows.append(row)
        if rows:
            by_day[day] = rows
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    allrows = [r for v in by_day.values() for r in v]
    days = list(by_day.values())
    res = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "days": sorted(by_day), "common_names_resolved": len(allrows), "counts": dict(only),
           "stages": {}}
    for s in STAGES:
        res["stages"][s] = {
            "rho_scaled": pooled(days, f"key {s}", "scaled"),
            "rho_raw": pooled(days, f"key {s}", "move"),
            "book_80": book(allrows, s, BOOK), "band_60": book(allrows, s, BAND),
            "p_up": brier(allrows, s)}
    res["stages"]["E-P v3b"]["parts_rho_scaled"] = pooled(days, "key v3b parts", "scaled")
    res["primary_delta_rho_scaled"] = bootstrap_delta(by_day, "key E-P", "key E-P v3b", "scaled")
    res["delta_rho_raw"] = bootstrap_delta(by_day, "key E-P", "key E-P v3b", "move")
    tot = sum(types.values()) or 1
    res["v3b_evidence_types"] = {k: round(v / tot, 3) for k, v in types.most_common()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "v3b-compare.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(f"{len(by_day)} days, {len(allrows)} common resolved names; {dict(only)}")
    for s, v in res["stages"].items():
        print(f"  {s:8s} rho_scaled {v['rho_scaled']}  rho_raw {v['rho_raw']}  "
              f"book>=80 {v['book_80']}  band>=60 {v['band_60']}  p_up {v['p_up']}")
    print(f"  v3b three-part forecast rho_scaled {res['stages']['E-P v3b']['parts_rho_scaled']}")
    print(f"  primary: delta rho_scaled (v3b - E-P), day bootstrap {res['primary_delta_rho_scaled']}")
    if len(by_day) < 20:
        print("  fewer than 20 run days: the pre-registration reads nothing before 20.")


if __name__ == "__main__":
    main()
