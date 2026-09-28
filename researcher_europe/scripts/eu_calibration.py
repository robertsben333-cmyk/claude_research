#!/usr/bin/env python3
"""Pool every resolved European run and score the hunters on SIZE and CERTAINTY.

    python3 researcher_europe/scripts/eu_calibration.py
    python3 researcher_europe/scripts/eu_calibration.py --json out.json

`eu_resolve.py` answers one day at a time, and on four to fourteen names a day every
number it prints is noise. This pools the resolved days (validation runs excluded, a
killed name excluded) and asks three questions the signed rank correlation cannot
separate:

  SIZE       does the hunter's magnitude rank the magnitude of the move, and at what
             level -- `median_ratio_realised_to_predicted` above 1 is under-sizing
  DIRECTION  does the sign come out right, and does `p_up` beat a coin (Brier < 0.25)
  CERTAINTY  does anything the hunter emits tell a right sign from a wrong one --
             `p_up` distance from 50, finding count, range width, `|impact_sum|`

and, where a run carries `eu-postmortem.json` (per-name verdicts filled from the
release: the actual print against the hunter's bar, what the move landed on, whether
a prior trading update had already disclosed the numbers), the split that decides
where to improve: **was the hunter wrong about the NUMBER or about the REACTION?**

It changes nothing. It is measurement, and nothing it prints should move a constant
until many more days have pooled -- the same rule that froze `w1`.
"""
import argparse
import glob
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_resolve import spearman  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def hunts_of(run):
    out = {}
    for f in sorted(Path(run, "hunts").glob("*.json")):
        h = load(f)
        if isinstance(h, dict) and h.get("ticker"):
            out.setdefault(h["ticker"], h)
    return out


def collect(pattern):
    rows = []
    for rf in sorted(glob.glob(pattern)):
        run = Path(rf).parent
        uni = load(run / "universe.json") or {}
        if uni.get("validation_only"):
            continue
        res = load(rf) or {}
        hunts = hunts_of(run)
        pm = {x.get("ticker"): x for x in (load(run / "eu-postmortem.json") or [])
              if isinstance(x, dict)}
        for r in res.get("rows", []):
            mv = r.get("realised_move_pct")
            if mv is None or r.get("move_pending") or not r.get("rankable"):
                continue
            if r.get("event_occurred") is False:
                continue
            h = hunts.get(r["ticker"]) or {}
            if h.get("event_confirmed") is False:
                continue
            f = h.get("findings") or []
            rows.append({
                "date": res.get("event_date"), "ticker": r["ticker"],
                "market": r.get("submarket"), "move": mv,
                "impact_sum": r.get("impact_sum") or 0.0,
                "expected_move": h.get("expected_move_pct") or 0.0,
                "abs_move": h.get("abs_move_pct"),
                "p_up": h.get("p_up"),
                "print_vs_bar": h.get("print_vs_bar_pct"),
                "proxy": r.get("history_median_abs_move_pct"),
                "n_findings": len(f),
                "width": sum((x.get("impact_high_pct") or 0) - (x.get("impact_low_pct") or 0)
                             for x in f),
                "by_line": {k: sum(x.get("expected_impact_pct") or 0 for x in f
                                   if x.get("lands_on") == k)
                            for k in {x.get("lands_on") for x in f}},
                "pm": pm.get(r["ticker"]),
            })
    return rows


def rho(a, b):
    return spearman(a, b) if len(a) >= 3 else None


def size_block(rows):
    out = {}
    for k in ("abs_move", "expected_move", "impact_sum", "proxy"):
        p = [(abs(r[k]), abs(r["move"])) for r in rows
             if isinstance(r.get(k), (int, float)) and r[k]]
        if len(p) < 3:
            out[k] = {"n": len(p)}
            continue
        out[k] = {"n": len(p),
                  "rho_abs_vs_abs_move": rho([a for a, _ in p], [b for _, b in p]),
                  "median_predicted": round(median(a for a, _ in p), 2),
                  "median_realised": round(median(b for _, b in p), 2),
                  "median_ratio": round(median(b / a for a, b in p), 2),
                  "frac_realised_larger": round(sum(b > a for a, b in p) / len(p), 3)}
    return out


def direction_block(rows):
    out = {}
    for k in ("impact_sum", "expected_move", "print_vs_bar"):
        p = [(r[k], r["move"]) for r in rows
             if isinstance(r.get(k), (int, float)) and r[k] and r["move"]]
        if len(p) < 3:
            out[k] = {"n": len(p)}
            continue
        right = [1 if (a > 0) == (b > 0) else 0 for a, b in p]
        out[k] = {"n": len(p), "rho": rho([a for a, _ in p], [b for _, b in p]),
                  "sign_right": f"{sum(right)}/{len(right)}",
                  "book_mean_pct": round(sum(math.copysign(1, a) * b for a, b in p)
                                         / len(p), 2)}
    # The ranker the two new answers imply, beside the key it may one day replace:
    # (2 p_up - 1) x abs_move. Hunts before 2026-09-28 carry neither field.
    se = [((2 * r["p_up"] / 100.0 - 1) * r["abs_move"], r["move"]) for r in rows
          if isinstance(r.get("p_up"), (int, float))
          and isinstance(r.get("abs_move"), (int, float))]
    out["signed_expectation"] = ({"n": len(se), "rho": rho([a for a, _ in se],
                                                           [b for _, b in se])}
                                 if len(se) >= 3 else {"n": len(se)})
    pr = [(r["p_up"] / 100.0, 1.0 if r["move"] > 0 else 0.0) for r in rows
          if isinstance(r.get("p_up"), (int, float)) and r["move"]]
    if len(pr) >= 3:
        out["p_up"] = {"n": len(pr),
                       "brier": round(sum((p - o) ** 2 for p, o in pr) / len(pr), 4),
                       "brier_coin_flip": 0.25,
                       "buckets": bucket(pr)}
    else:
        out["p_up"] = {"n": len(pr), "note": "hunts before 2026-09-28 carry no p_up"}
    return out


def bucket(pr):
    b = defaultdict(list)
    for p, o in pr:
        conf = abs(p - 0.5)
        lab = "50-55" if conf < 0.05 else "55-65" if conf < 0.15 else "65-80" if conf < 0.3 else ">80"
        b[lab].append(1.0 if (p > 0.5) == (o == 1.0) else 0.0)
    return {k: {"n": len(v), "sign_right": round(sum(v) / len(v), 3)}
            for k, v in sorted(b.items())}


def certainty_block(rows):
    nz = [r for r in rows if r["impact_sum"] and r["move"]]
    right = [1.0 if (r["impact_sum"] > 0) == (r["move"] > 0) else 0.0 for r in nz]
    out = {"n": len(nz)}
    for k in ("n_findings", "width"):
        out[f"rho_{k}_vs_sign_right"] = rho([r[k] for r in nz], right)
    out["rho_abs_impact_vs_sign_right"] = rho([abs(r["impact_sum"]) for r in nz], right)
    return out


def line_block(rows):
    """Signed findings per line against the move: which lines carry direction."""
    by = defaultdict(list)
    for r in rows:
        for k, v in r["by_line"].items():
            if v:
                by[k].append((v, r["move"]))
    return {k: {"n": len(v),
                "sign_right": f"{sum((a > 0) == (b > 0) for a, b in v)}/{len(v)}",
                "rho": rho([a for a, _ in v], [b for _, b in v])}
            for k, v in sorted(by.items())}


def postmortem_block(rows):
    """Number vs reaction, from eu-postmortem.json where a run carries one."""
    pm = [r for r in rows if r["pm"]]
    if not pm:
        return {"n": 0, "note": "no run carries eu-postmortem.json"}
    cells = Counter()
    moved_on = Counter()
    prior = Counter()
    for r in pm:
        a = r["pm"].get("print_vs_bar_actual_pct")
        mo = r["pm"].get("moved_on")
        moved_on[(mo or {}).get("line") if isinstance(mo, dict) else mo] += 1
        pu = r["pm"].get("prior_update")
        prior[bool(pu.get("value") if isinstance(pu, dict) else pu)] += 1
        if not isinstance(a, (int, float)) or not r["print_vs_bar"] or not r["expected_move"]:
            continue
        number_right = (a > 0) == (r["print_vs_bar"] > 0)
        reaction_right = (r["expected_move"] > 0) == (r["move"] > 0)
        cells[("number " + ("right" if number_right else "wrong"),
               "reaction " + ("right" if reaction_right else "wrong"))] += 1
    beat = [(r["pm"]["print_vs_bar_actual_pct"], r["move"]) for r in pm
            if isinstance(r["pm"].get("print_vs_bar_actual_pct"), (int, float))]
    return {"n": len(pm),
            "number_x_reaction": {f"{a} / {b}": n for (a, b), n in sorted(cells.items())},
            "rho_actual_surprise_vs_move": rho([a for a, _ in beat], [b for _, b in beat]),
            "sign_actual_surprise_vs_move": (f"{sum((a > 0) == (b > 0) for a, b in beat if a)}"
                                             f"/{sum(1 for a, _ in beat if a)}"),
            "moved_on": dict(moved_on.most_common()),
            "numbers_pre_released": dict(prior)}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default=str(REPO / "research/*/*/*/europe/eu-resolved.json"))
    ap.add_argument("--json", help="also write the report here")
    a = ap.parse_args()
    rows = collect(a.runs)
    rep = {"n_names": len(rows), "n_days": len({r["date"] for r in rows}),
           "size": size_block(rows), "direction": direction_block(rows),
           "certainty": certainty_block(rows), "by_line": line_block(rows),
           "postmortem": postmortem_block(rows),
           "note": ("Pooled over resolved non-validation runs; killed and unconfirmed "
                    "names excluded. Measurement only: nothing here moves a constant "
                    "until many more days have pooled.")}
    text = json.dumps(rep, indent=2, ensure_ascii=False)
    print(text)
    if a.json:
        Path(a.json).write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
