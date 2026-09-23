#!/usr/bin/env python3
"""Stage E V2: the day's findings in the shadow ledger's units, beside V1.

    grounded(j, tau) = S_j * kappa(tau, line_j) * sigma_live

S_j is the hunter's own `expected_impact_pct`, kappa comes from
`edge_shadow_engine.py` (beta-stripped move over sigma, per score point), and
sigma_live is the name's 20-session realised daily sigma off the sealed baseline --
the same quantity, computed the same way, that divided every shadow move. The
result is in percent of spot, per horizon.

THREE SCORES PER NAME, ALWAYS TOGETHER. Every row carries the hunters' sum before
they read LESSONS.md (`impact_sum_pre_lessons`), V1's key after it (`impact_sum_v1`)
and V2 (`impact_sum_grounded`). The CLI prints them as one table, which is the table
the note carries, and `edge_resolve.py` ranks all three against the same move.

V1 IS STILL THE KEY THAT TRADES. This writes `edge-scores-grounded.json` beside
`edge-scores.json` and changes nothing in it; `alpaca_trade.py` never reads this
file. V2 has to earn its place in `edge_resolve.py`, which ranks both against the
same realised move, plus a third ranker that is V1 times sigma and no kappa at all.
If V2 only matches that control, kappa added nothing and the reorder is volatility.

THREE RULES THAT PR #9 DID NOT HAVE, each against a way a plausible number misleads:

  - One scale per sum. A finding whose line has no kappa takes the pooled kappa for
    its horizon; if the pooled fit is itself below `edge_v2.min_n`, the whole day is
    `uncalibrated` and every grounded value is null. Nothing falls back to the raw
    score, because a raw 5 beside a grounded 1.8 is two units added together.
  - No invented denominators. A name with no realised sigma is not grounded and says
    why; there is no default of 1.0 or 3.0.
  - The matrix is rebuilt as of the run. kappa is refitted in memory from ledger items
    with t0 before the run's baselines were sealed, so re-grounding an old run later
    cannot use that run's own prints.

    python3 researcher_us/scripts/edge_grounded_score.py --run research/2026/09/2026-09-22/edge
"""
import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import edge_shadow_engine as shadow  # noqa: E402

TIMEFRAMES = shadow.TIMEFRAMES


def load_json(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def sigma_live(baseline):
    """Daily realised sigma in percent, from the sealed tape. None if absent."""
    rv = ((baseline or {}).get("tape") or {}).get("realised_vol_20d_annualised_pct")
    return round(float(rv) / math.sqrt(252), 4) if rv and rv > 0 else None


def usable(entry, min_n):
    return bool(entry and entry.get("kappa") is not None and entry["n"] >= min_n)


def pick_kappa(matrix, line, tf, min_n):
    """(kappa, source) for one finding, or (None, reason)."""
    own = (matrix.get(line) or {}).get(tf)
    if usable(own, min_n):
        return own["kappa"], "line"
    pooled = (matrix.get("_pooled") or {}).get(tf)
    if usable(pooled, min_n):
        return pooled["kappa"], "pooled"
    return None, "uncalibrated"


def seal_time(run_dir):
    """The earliest baseline seal: nothing the ledger learned after it may be used."""
    stamps = []
    for bp in (Path(run_dir) / "baselines").glob("*.json"):
        b = load_json(bp) or {}
        if b.get("as_of_utc"):
            stamps.append(b["as_of_utc"])
    return min(stamps) if stamps else None


def ground_run(run_dir, ledger_path=shadow.LEDGER, min_n=None, primary=None):
    run_dir = Path(run_dir)
    scores = load_json(run_dir / "edge-scores.json")
    if not scores:
        raise SystemExit(f"{run_dir}/edge-scores.json does not exist; run edge_score.py first")
    min_n = int(min_n or shadow.cfg("min_n", 30))
    primary = primary or shadow.cfg("primary_horizon", "session_close")
    as_of = seal_time(run_dir)
    ledger = shadow.load_ledger(ledger_path)
    matrix, n_obs = shadow.fit_matrix(ledger.get("items", []), as_of)

    baselines = {}
    for bp in (run_dir / "baselines").glob("*.json"):
        d = load_json(bp)
        if d and d.get("ticker"):
            baselines[d["ticker"]] = d

    day_calibrated = usable((matrix["_pooled"]).get(primary), min_n)
    rows = []
    for r in scores.get("ranking", []):
        t = r["ticker"]
        sig = sigma_live(baselines.get(t))
        row = {"ticker": t, "rankable": r.get("rankable"),
               "rank_v1": r.get("rank"),
               "impact_sum_pre_lessons": (r.get("diagnostics") or {}).get(
                   "impact_sum_pre_lessons"),
               "impact_sum_v1": r.get("impact_sum"),
               "sigma_daily_pct": sig,
               # The control V2 must beat: V1 in percent-of-sigma units, no kappa.
               "control_vol_only": (None if sig is None or r.get("impact_sum") is None
                                    else round(r["impact_sum"] * sig, 3)),
               "grounded": {}, "impact_sum_grounded": None}
        why = None
        if not r.get("rankable"):
            why = "not rankable in V1: " + str(r.get("not_rankable_because"))
        elif sig is None:
            why = "no realised sigma in the sealed baseline"
        for tf in TIMEFRAMES:
            if why:
                break
            total, used, missing = 0.0, {"line": 0, "pooled": 0}, 0
            for f in r.get("findings", []):
                s = f.get("expected_impact_pct")
                if s is None:
                    continue
                k, src = pick_kappa(matrix, f.get("lands_on") or "other", tf, min_n)
                if k is None:
                    missing += 1
                    continue
                total += float(s) * k * sig
                used[src] += 1
            row["grounded"][tf] = (None if missing else
                                   {"impact_sum": round(total, 3), "kappa_from": used})
        if why:
            row["not_grounded_because"] = why
        elif not day_calibrated:
            row["not_grounded_because"] = (f"pooled kappa at {primary} rests on fewer "
                                           f"than min_n={min_n} observations")
        else:
            g = row["grounded"].get(primary)
            row["impact_sum_grounded"] = g["impact_sum"] if g else None
        rows.append(row)

    live = [x for x in rows if x["impact_sum_grounded"] is not None]
    for i, x in enumerate(sorted(live, key=lambda x: -x["impact_sum_grounded"]), 1):
        x["rank_v2"] = i
    out = {
        "run": str(run_dir),
        "grounded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "v2",
        "status": "calibrated" if day_calibrated else "uncalibrated",
        "ranking_key": "impact_sum_grounded",
        "primary_horizon": primary,
        "trades_on": "V1 (edge-scores.json, impact_sum). alpaca_trade.py never reads this file.",
        "min_n": min_n,
        "matrix_as_of": as_of,
        "ledger_observations_used": n_obs,
        "kappa_used": {k: v for k, v in matrix.items()},
        "timeframes_tracked": TIMEFRAMES,
        "ranking": sorted(rows, key=lambda x: (x.get("rank_v2") is None,
                                                x.get("rank_v2") or 0,
                                                x.get("rank_v1") or 999)),
    }
    (run_dir / "edge-scores-grounded.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return out


def three_score_table(out):
    """pre-lessons | post-lessons (V1, trades) | V2, one line per name."""
    def f(v):
        return "--" if v is None else f"{v:+.2f}"
    status = out["status"]
    lines = [f"{'ticker':8s}{'pre-lessons':>13s}{'post-lessons':>14s}{'V2':>9s}  note",
             f"{'':8s}{'':>13s}{'(V1, trades)':>14s}{'':>9s}"]
    for r in sorted(out["ranking"], key=lambda r: (r.get("rank_v1") or 999)):
        v2 = f(r["impact_sum_grounded"]) if status == "calibrated" else "uncal."
        note = r.get("not_grounded_because", "") if status == "calibrated" else ""
        lines.append(f"{r['ticker']:8s}{f(r.get('impact_sum_pre_lessons')):>13s}"
                     f"{f(r.get('impact_sum_v1')):>14s}{v2:>9s}  {note}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--ledger", default=str(shadow.LEDGER))
    a = ap.parse_args()
    out = ground_run(a.run, a.ledger)
    n = sum(1 for r in out["ranking"] if r.get("rank_v2"))
    print(f"V2 {out['status']}: {n} of {len(out['ranking'])} names grounded at "
          f"{out['primary_horizon']}, matrix as of {out['matrix_as_of']} on "
          f"{out['ledger_observations_used']} ledger observations")
    print(three_score_table(out))
    print(f"wrote {Path(a.run) / 'edge-scores-grounded.json'}  (V1 untouched; V1 trades)")


if __name__ == "__main__":
    main()
