#!/usr/bin/env python3
"""Score a resolved edge-hunt run finding by finding: fact right? reaction right?

`edge_resolve.py` answers whether the day RANKED. It cannot say why a row was right or
wrong, and the resolved days of 2026-09-08 through 09-14 showed the two coming apart
constantly: the hunter proves a fact, the print confirms it, and the stock moves the
other way on the guide or on positioning. That failure is invisible to a rank
correlation and it is the one the hunters most need to learn from.

So this scores each finding on three things a person fills in from the release and the
tape, in `<RUN>/edge/finding-verdicts.json`:

  fact_correct      did the thing the hunter said would be in the print appear
                    (true / false / null when the company did not disclose it)
  reaction_correct  did the stock move the way the finding's sign said, over the
                    window edge_resolve scores. Filled automatically from the
                    realised move when left null; override it when the window is
                    wrong for the name
  moved_on          which line the move actually landed on, in the hunter's own
                    `lands_on` vocabulary: reported_quarter, guidance, one_off,
                    financing, capital_return, positioning, other

and, per name, `print_vs_bar_actual_pct` -- what the number actually did against the
bar the hunter named -- so the hunter's two answers (`print_vs_bar_pct` and
`expected_move_pct`) can be resolved separately. The gap between "predicted the
number" and "predicted the stock" is the cheapest measurement this stage has of
whether it forecasts the reaction or only the print.

    python3 edge/scripts/edge_postmortem.py --run <RUN>/edge --template   # write the file to fill
    python3 edge/scripts/edge_postmortem.py --run <RUN>/edge              # score it
    python3 edge/scripts/edge_postmortem.py --pool 'research/2026/*/*/edge'

Pooled, it reports: the fact x reaction confusion matrix; reaction hit rate by
`lands_on` and by `moved_on`; the resolution of the hunter's two numbers; and the
sign split. When a pattern in those tables recurs, it belongs in edge/LESSONS.md --
that file is how the next hunter learns it, and nothing else is.

Nothing here changes the key, the floor or the book. It is measurement.
"""
import argparse
import glob
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edge_resolve import realised  # noqa: E402

LANDS = ("reported_quarter", "guidance", "one_off", "financing", "capital_return",
         "positioning", "other")


def load_json(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def realised_moves(run, scores):
    """{ticker: move_pct}. Prefer edge-outcome.json; fetch what it lacks."""
    out = {}
    oc = load_json(Path(run) / "edge-outcome.json")
    if oc:
        for day in oc.get("per_day") or []:
            for r in day.get("rows") or []:
                if r.get("outcome") == "resolved" and r.get("move_pct") is not None:
                    out[r["ticker"]] = r["move_pct"]
    baselines = {}
    for f in sorted((Path(run) / "baselines").glob("*.json")):
        d = load_json(f)
        if d:
            baselines[d["ticker"]] = d
    for r in scores.get("ranking", []):
        t = r["ticker"]
        if t in out or not r.get("rankable"):
            continue
        b = baselines.get(t) or {}
        if not b.get("event_date"):
            continue
        try:
            res, err = realised(t, b["event_date"], b.get("session", "bmo"))
        except Exception:
            res, err = None, "fetch failed"
        if res and not err:
            out[t] = res["move_pct"]
    return out


def template(run, scores, moves):
    names = []
    for r in scores.get("ranking", []):
        hv = r.get("hunter_view") or {}
        entry = {
            "ticker": r["ticker"],
            "impact_sum": r.get("impact_sum"),
            "expected_move_pct": hv.get("expected_move_pct"),
            "print_vs_bar_pct": hv.get("print_vs_bar_pct"),
            "bar": hv.get("bar"),
            "realised_move_pct": moves.get(r["ticker"]),
            "print_vs_bar_actual_pct": None,
            "moved_on": None,
            "note": "",
            "findings": [],
        }
        for x in r.get("findings") or []:
            entry["findings"].append({
                "key": x["key"],
                "finding": x.get("finding"),
                "expected_impact_pct": x.get("expected_impact_pct"),
                "lands_on": x.get("lands_on"),
                "fact_correct": None,
                "reaction_correct": None,
                "note": "",
            })
        names.append(entry)
    return {
        "run": str(run),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "how_to_fill": {
            "fact_correct": "true if the thing the finding said would be in the print was; "
                            "false if it was not; null if the company did not disclose it",
            "reaction_correct": "leave null to fill from the realised move; set it only when "
                                "the scored window is wrong for this name",
            "moved_on": "one of " + " | ".join(LANDS) + ", from the release and the coverage",
            "print_vs_bar_actual_pct": "what the number did against the bar the hunter named, "
                                       "in percent of the bar; null if the hunter named none",
        },
        "names": names,
    }


def score(verdicts, moves):
    """Per-run tallies. Returns a dict of counters that pool by addition."""
    conf = {"fact_right_reaction_right": 0, "fact_right_reaction_wrong": 0,
            "fact_wrong_reaction_right": 0, "fact_wrong_reaction_wrong": 0,
            "fact_unknown": 0, "reaction_unresolved": 0}
    by_lands = {}
    by_moved = {}
    two_numbers = {"n": 0, "stock_sign_right": 0, "number_sign_right": 0,
                   "number_right_stock_wrong": 0, "number_wrong_stock_right": 0,
                   "abs_err_move": [], "abs_err_sum": []}
    sign = {"long_n": 0, "long_hits": 0, "long_pay": [],
            "short_n": 0, "short_hits": 0, "short_pay": []}
    filled = 0
    for nm in verdicts.get("names") or []:
        mv = nm.get("realised_move_pct")
        if mv is None:
            mv = moves.get(nm["ticker"])
        for f in nm.get("findings") or []:
            rc = f.get("reaction_correct")
            imp = f.get("expected_impact_pct") or 0.0
            if rc is None and mv is not None and imp:
                rc = (imp > 0) == (mv > 0)
            fc = f.get("fact_correct")
            if fc is not None:
                filled += 1
            if rc is None:
                conf["reaction_unresolved"] += 1
            elif fc is None:
                conf["fact_unknown"] += 1
            else:
                conf[f"fact_{'right' if fc else 'wrong'}_reaction_{'right' if rc else 'wrong'}"] += 1
            lo = f.get("lands_on") or "unlabelled"
            d = by_lands.setdefault(lo, {"n": 0, "reaction_hits": 0, "size": 0.0})
            if rc is not None:
                d["n"] += 1
                d["reaction_hits"] += int(rc)
                d["size"] += abs(imp)
        mo = nm.get("moved_on")
        if mo:
            by_moved[mo] = by_moved.get(mo, 0) + 1
        em, pv, pa = nm.get("expected_move_pct"), nm.get("print_vs_bar_pct"), \
            nm.get("print_vs_bar_actual_pct")
        if mv is not None and isinstance(em, (int, float)) and em:
            two_numbers["n"] += 1
            sr = (em > 0) == (mv > 0)
            two_numbers["stock_sign_right"] += int(sr)
            two_numbers["abs_err_move"].append(abs(em - mv))
            if isinstance(nm.get("impact_sum"), (int, float)):
                two_numbers["abs_err_sum"].append(abs(nm["impact_sum"] - mv))
            if isinstance(pv, (int, float)) and isinstance(pa, (int, float)) and pv and pa:
                nr = (pv > 0) == (pa > 0)
                two_numbers["number_sign_right"] += int(nr)
                two_numbers["number_right_stock_wrong"] += int(nr and not sr)
                two_numbers["number_wrong_stock_right"] += int((not nr) and sr)
            side = "long" if em > 0 else "short"
            sign[f"{side}_n"] += 1
            sign[f"{side}_hits"] += int(sr)
            sign[f"{side}_pay"].append(mv if em > 0 else -mv)
    return {"confusion": conf, "by_lands_on": by_lands, "moved_on": by_moved,
            "two_numbers": two_numbers, "by_sign": sign, "facts_filled": filled}


def merge(a, b):
    if a is None:
        return b
    out = json.loads(json.dumps(a))
    for k, v in b["confusion"].items():
        out["confusion"][k] += v
    for k, v in b["by_lands_on"].items():
        d = out["by_lands_on"].setdefault(k, {"n": 0, "reaction_hits": 0, "size": 0.0})
        for kk in d:
            d[kk] += v[kk]
    for k, v in b["moved_on"].items():
        out["moved_on"][k] = out["moved_on"].get(k, 0) + v
    for k, v in b["two_numbers"].items():
        out["two_numbers"][k] = out["two_numbers"][k] + v
    for k, v in b["by_sign"].items():
        out["by_sign"][k] = out["by_sign"][k] + v
    out["facts_filled"] += b["facts_filled"]
    return out


def report(t, label):
    c = t["confusion"]
    print(f"\n=== {label} ===")
    judged = sum(v for k, v in c.items() if k.startswith("fact_") and "unknown" not in k)
    print(f"findings with a fact verdict: {judged}  (fact unknown: {c['fact_unknown']}, "
          f"reaction unresolved: {c['reaction_unresolved']})")
    print(f"  fact right & reaction right   {c['fact_right_reaction_right']:>4}")
    print(f"  fact right & reaction WRONG   {c['fact_right_reaction_wrong']:>4}   <- the failure LESSONS.md #1 is about")
    print(f"  fact wrong & reaction right   {c['fact_wrong_reaction_right']:>4}   <- unearned; discount these")
    print(f"  fact wrong & reaction wrong   {c['fact_wrong_reaction_wrong']:>4}")
    if t["by_lands_on"]:
        print("reaction hit rate by the line the finding lands on:")
        for k, v in sorted(t["by_lands_on"].items(), key=lambda kv: -kv[1]["n"]):
            if v["n"]:
                print(f"  {k:18s} {v['reaction_hits']:>3}/{v['n']:<3} "
                      f"{100*v['reaction_hits']/v['n']:5.0f}%   total |size| {v['size']:.1f}")
    if t["moved_on"]:
        print("what the move actually landed on: " +
              ", ".join(f"{k} {v}" for k, v in sorted(t["moved_on"].items(), key=lambda kv: -kv[1])))
    tn = t["two_numbers"]
    if tn["n"]:
        print(f"the hunter's two numbers, n={tn['n']}:")
        print(f"  stock sign right (expected_move_pct)   {tn['stock_sign_right']}/{tn['n']}")
        print(f"  number sign right (print_vs_bar_pct)   {tn['number_sign_right']}/{tn['n']}"
              "   (needs print_vs_bar_actual_pct filled)")
        print(f"  number right, stock wrong              {tn['number_right_stock_wrong']}")
        print(f"  number wrong, stock right              {tn['number_wrong_stock_right']}")
        if tn["abs_err_move"]:
            print(f"  median |error| expected_move_pct       {statistics.median(tn['abs_err_move']):.2f}"
                  + (f"   impact_sum {statistics.median(tn['abs_err_sum']):.2f}"
                     if tn["abs_err_sum"] else ""))
    s = t["by_sign"]
    for side in ("long", "short"):
        if s[f"{side}_n"]:
            print(f"  {side:5s} {s[f'{side}_hits']}/{s[f'{side}_n']}  "
                  f"mean payoff {statistics.fmean(s[f'{side}_pay']):+.2f}%")
    if t["facts_filled"] == 0:
        print("no fact_correct filled yet: run with --template, fill finding-verdicts.json "
              "from the release, then re-run")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run")
    ap.add_argument("--pool", help="glob of run dirs")
    ap.add_argument("--template", action="store_true",
                    help="write finding-verdicts.json (never overwrites a filled one)")
    a = ap.parse_args()
    if not a.run and not a.pool:
        ap.error("--run or --pool")

    runs = [a.run] if a.run else sorted(glob.glob(a.pool))
    total = None
    for run in runs:
        run = Path(run)
        scores = load_json(run / "edge-scores.json")
        if not scores:
            continue
        vpath = run / "finding-verdicts.json"
        moves = realised_moves(run, scores)
        if a.template:
            if vpath.exists():
                ex = load_json(vpath)
                if any(f.get("fact_correct") is not None
                       for nm in ex.get("names", []) for f in nm.get("findings", [])):
                    print(f"{vpath} already carries verdicts; not overwritten")
                    continue
            vpath.write_text(json.dumps(template(run, scores, moves), indent=1) + "\n",
                             encoding="utf-8")
            print(f"wrote {vpath}  ({sum(len(n['findings']) for n in template(run, scores, moves)['names'])} findings, "
                  f"{len(moves)} names with a realised move)")
            continue
        verdicts = load_json(vpath)
        if not verdicts:
            if a.run:
                print(f"no {vpath}; run with --template first")
            continue
        t = score(verdicts, moves)
        if a.run:
            report(t, str(run))
        total = merge(total, t)
    if a.pool and total:
        report(total, f"POOLED over {len(runs)} run dirs")


if __name__ == "__main__":
    main()
