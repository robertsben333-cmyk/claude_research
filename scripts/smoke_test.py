#!/usr/bin/env python3
"""
End-to-end plumbing check, with fabricated data and no model calls.

The pipeline's stages hand files to each other unattended, hours apart, across
separate sessions. A shape mismatch between two stages surfaces at 17:37 on a
Tuesday otherwise. This runs the whole chain against synthetic data in a temp
directory in about a second.

It checks the plumbing, not the research: agent definitions parse, path
resolution works, every stage's file shape passes its own validator, the
synthesis maths is self-consistent, and the conviction gate actually fires.

    python3 scripts/smoke_test.py

Exit 0 = the chain is intact.
"""

import glob
import json
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
failures = []


def check(label, condition, detail=""):
    if condition:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label}" + (f" — {detail}" if detail else ""))
        failures.append(label)


def run(args, expect=0):
    p = subprocess.run([PY] + args, capture_output=True, text=True, cwd=REPO)
    ok = p.returncode == expect
    return ok, (p.stdout + p.stderr).strip()


PERSONAS = [
    "Fundamental / KPI Analyst",
    "Options & Positioning Strategist",
    "Behavioural / Sentiment Reader",
    "Outside-View Base-Rate Statistician",
    "Macro / Cross-Asset & Peer Read-through",
    "Red-Team Skeptic",
    "Insider, Communication & Alt-Data Forensics",
]


def verdicts(scores, confidence="Med"):
    out = []
    for name, s in zip(PERSONAS, scores):
        v = {
            "persona": name,
            "direction_score": s,
            "prob_up": max(1, min(99, 50 + s * 0.35)),
            "confidence": confidence,
            "expected_move_view": "±9%, roughly priced",
            "reversal_risk": 40,
            "key_drivers": ["driver a", "driver b"],
            "top_risk_to_my_call": "guidance reset",
            "key_sources": ["https://example.com/a", "https://example.com/b"],
        }
        if name == "Red-Team Skeptic":
            v["strongest_reversal_case"] = "priced-in beat into a 20% run-up"
        out.append(v)
    return out


ANCHORS = {
    "event_confirmed": True,
    "event_implied_move_pct": 9.2,
    "historical_move_mean_abs": 7.7,
    "historical_move_max_abs": 12.4,
    "historical_sample_size": 8,
}


def synth(tmp, scores, anchors=None, confidence="Med"):
    src = os.path.join(tmp, "in.json")
    with open(src, "w") as fh:
        json.dump({"ticker": "TEST", "anchors": anchors or ANCHORS,
                   "panel_verdicts": verdicts(scores, confidence)}, fh)
    p = subprocess.run([PY, "scripts/synthesize.py", src],
                       capture_output=True, text=True, cwd=REPO)
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout), ""


def main():
    print("Definitions")
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required: pip install pyyaml")

    for path in sorted(glob.glob(os.path.join(REPO, ".claude/agents/*.md")) +
                       glob.glob(os.path.join(REPO, ".claude/skills/*/SKILL.md"))):
        rel = os.path.relpath(path, REPO)
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            check(rel, False, "no frontmatter")
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except yaml.YAMLError as exc:
            check(rel, False, str(exc).splitlines()[0])
            continue
        expected = (os.path.basename(os.path.dirname(path)) if path.endswith("SKILL.md")
                    else os.path.basename(path)[:-3])
        check(rel, bool(fm.get("name") == expected and fm.get("description")),
              f"name/description mismatch (name={fm.get('name')!r})")

    check("config/pipeline.yaml parses",
          bool(yaml.safe_load(open(os.path.join(REPO, "config/pipeline.yaml")))))

    print("\nPath resolution")
    ok, out = run(["scripts/run_paths.py", "2026-08-10", "--json", "--no-create"])
    check("run_paths.py --json", ok, out)
    if ok:
        pp = json.loads(out)
        check("run_dir uses research/<Y>/<M>/<date>",
              pp["run_dir"].endswith("research/2026/08/2026-08-10"), pp["run_dir"])

    print("\nCalendar logic")
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    from get_earnings import next_trading_day, is_trading_day  # noqa: E402
    from datetime import date  # noqa: E402
    check("Friday rolls to Monday",
          next_trading_day(date(2026, 8, 7)) == date(2026, 8, 10))
    check("Christmas is not a trading day", not is_trading_day(date(2026, 12, 25)))
    check("Thanksgiving is not a trading day", not is_trading_day(date(2026, 11, 26)))
    check("day before a holiday rolls past it",
          next_trading_day(date(2026, 12, 24)) == date(2026, 12, 28))

    with tempfile.TemporaryDirectory() as tmp:
        print("\nSynthesis maths")

        s, err = synth(tmp, [62, 55, 70, 48, 58, 40, 66], confidence="High")
        check("aligned bullish panel -> Lean Up", s and s["call"] == "Lean Up",
              err or (s and s["call"]))
        if s:
            check("signed move is a fraction of expected move",
                  0 < s["signed_estimated_move"] < 0.85 * s["unsigned_expected_move"],
                  f"{s['signed_estimated_move']} vs {s['unsigned_expected_move']}")
            check("Up call carries a positive signed move", s["signed_estimated_move"] > 0)
            check("band is right-skewed around the expected move",
                  s["move_band_low_high"][1] - s["unsigned_expected_move"]
                  > s["unsigned_expected_move"] - s["move_band_low_high"][0])

        s, _ = synth(tmp, [-70, -62, -58, -66, -68, -64, -60], confidence="High")
        check("aligned bearish panel -> Strong Down", s and s["call"] == "Strong Down",
              s and s["call"])
        check("Down call carries a negative signed move",
              s and s["signed_estimated_move"] < 0)

        s, _ = synth(tmp, [90, -85, 75, -70, 60, -80, 40])
        check("split panel -> gate fires", s and s["conviction_gate_applied"] is True)
        check("gated call is Neutral / No Edge", s and s["call"] == "Neutral / No Edge")
        check("gated call has no signed move", s and s["signed_estimated_move"] is None)
        check("split panel is labelled split", s and s["panel_alignment"] == "split")

        s, _ = synth(tmp, [55, 50, 60, 45, 52, 48, 58],
                     anchors={"event_confirmed": False})
        check("unconfirmed timing -> gate fires", s and s["conviction_gate_applied"])

        s, _ = synth(tmp, [55, 50, 60, 45, 52, 48, 58],
                     anchors={"event_confirmed": True})
        check("no move anchor -> gate fires", s and s["conviction_gate_applied"])

        hi, _ = synth(tmp, [45, 42, 48, 40, 44, 41, 46], confidence="High")
        lo, _ = synth(tmp, [45, 42, 48, 40, 44, 41, 46], confidence="Low")
        check("Low confidence shrinks the signed move versus High",
              hi and lo and abs(lo["signed_estimated_move"]) < abs(hi["signed_estimated_move"]),
              f"low={lo and lo['signed_estimated_move']} high={hi and hi['signed_estimated_move']}")
        check("a weak-but-coherent lean survives as a call",
              lo and lo["call"] == "Lean Up", lo and lo["call"])

        print("\nStage file contracts")

        shortlist = {
            "schema_version": 1, "run_date": "2026-08-10",
            "window_covered": "after close 10 Aug through before open 11 Aug",
            "triage_mode": "scouted", "shortlist": [{
                "ticker": "TEST", "company": "Test Corp", "session": "amc",
                "event_date": "2026-08-10", "change_expectation": 78,
                "ai_edge": 64, "priority_score": 71.7,
                "selection_rationale": "binary guidance event with rich public data",
            }],
        }
        p1 = os.path.join(tmp, "01-shortlist.json")
        json.dump(shortlist, open(p1, "w"))
        ok, out = run(["scripts/validate_stage.py", "shortlist", p1])
        check("valid shortlist passes", ok, out)

        shortlist["shortlist"][0]["ai_edge"] = 140
        json.dump(shortlist, open(p1, "w"))
        ok, out = run(["scripts/validate_stage.py", "shortlist", p1], expect=1)
        check("out-of-range ai_edge is rejected", ok, out)

        good, _ = synth(tmp, [62, 55, 70, 48, 58, 40, 66], confidence="High")
        panel = {"ticker": "TEST", "company": "Test Corp",
                 "panel_verdicts": verdicts([62, 55, 70, 48, 58, 40, 66], "High"),
                 "synthesis": good}
        p3 = os.path.join(tmp, "TEST.json")
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3])
        check("synthesize.py output passes the panel validator", ok, out)

        panel["synthesis"] = dict(good, signed_estimated_move=-4.0)
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3], expect=1)
        check("Up call with a negative move is rejected", ok, out)

        panel["synthesis"] = dict(good, signed_estimated_move=good["unsigned_expected_move"])
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3], expect=1)
        check("claiming the full expected move is rejected", ok, out)

        panel["synthesis"] = good
        panel["panel_verdicts"] = panel["panel_verdicts"][:6]
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3], expect=1)
        check("a missing panel seat is flagged", ok, out)

        advice = {"schema_version": 1, "run_date": "2026-08-10", "ranked_names": [
            {"ticker": "TEST", "panelled": True, "call": "Lean Up",
             "signed_estimated_move": 4.2, "certainty_tier": "Med"}]}
        p4 = os.path.join(tmp, "04-advice.json")
        json.dump(advice, open(p4, "w"))
        ok, out = run(["scripts/validate_stage.py", "advice", p4])
        check("valid advice passes", ok, out)

    print("\nConsolidated predictions table")
    with tempfile.TemporaryDirectory() as tmp:
        # A synthetic run day whose files are spread across four stages, which is
        # exactly the join build_predictions.py has to get right.
        day_dir = os.path.join(tmp, "2026", "08", "2026-08-10")
        os.makedirs(os.path.join(day_dir, "02-dossiers"))
        os.makedirs(os.path.join(day_dir, "03-panel"))
        good, _ = synth(tmp, [62, 55, 70, 48, 58, 40, 66], confidence="High")

        json.dump({"run_date": "2026-08-10", "shortlist": [
            {"ticker": "TEST", "session": "amc", "change_expectation": 78, "ai_edge": 64}]},
            open(os.path.join(day_dir, "01-shortlist.json"), "w"))
        json.dump({"ticker": "TEST", "company": "Test Corp", "session": "amc",
                   "event_date": "2026-08-10", "preliminary_direction_score": 25,
                   "evidence_completeness": 82, "event_implied_move_pct": 9.2},
                  open(os.path.join(day_dir, "02-dossiers", "TEST.json"), "w"))
        json.dump({"ticker": "TEST", "synthesis": good},
                  open(os.path.join(day_dir, "03-panel", "TEST.json"), "w"))
        json.dump({"run_date": "2026-08-10", "ranked_names": [
            {"ticker": "TEST", "panelled": True, "call": "Lean Up"}]},
            open(os.path.join(day_dir, "04-advice.json"), "w"))
        json.dump({"run_date": "2026-08-10", "names": [
            {"ticker": "TEST", "actual_move": 6.8, "direction_hit": True,
             "magnitude_error": 2.6, "band_hit": True}]},
            open(os.path.join(day_dir, "05-outcome.json"), "w"))

        sys.path.insert(0, os.path.join(REPO, "scripts"))
        import build_predictions  # noqa: E402
        build_predictions.RESEARCH = tmp
        pred = build_predictions.collect()

        check("one row per prediction", len(pred) == 1, f"got {len(pred)}")
        if pred:
            r = pred[0]
            check("pulls the call from the advice file", r["call"] == "Lean Up", r["call"])
            check("pulls triage scores from the shortlist",
                  r["change_expectation"] == 78 and r["ai_edge"] == 64)
            check("pulls the preliminary read from the dossier",
                  r["preliminary_direction_score"] == 25)
            check("pulls synthesis numbers from the panel file",
                  r["disparity"] == good["disparity"]
                  and r["signed_estimated_move"] == good["signed_estimated_move"])
            check("pulls the realised move from the outcome file",
                  r["actual_move"] == 6.8 and r["direction_hit"] is True)
            check("flattens the move band into two columns",
                  r["band_low"] == good["move_band_low_high"][0]
                  and r["band_high"] == good["move_band_low_high"][1])
        s = build_predictions.summarise(pred)
        check("summary counts a scored panelled call",
              s["predictions_scored"] == 1 and s["panelled_direction_hit_rate"] == 1.0, str(s))

        # An unscored day must read as pending, not as a miss.
        os.remove(os.path.join(day_dir, "05-outcome.json"))
        pend = build_predictions.collect()
        check("unscored prediction reads as pending",
              pend[0]["outcome_status"] == "pending" and pend[0]["direction_hit"] is None)
        check("pending rows are excluded from the hit rate",
              build_predictions.summarise(pend)["panelled_direction_hit_rate"] is None)

    print("\nData fetch")
    ok, out = run(["scripts/get_earnings.py", "--probe"])
    if ok:
        print("  ok    at least one earnings source is reachable")
    else:
        print("  WARN  no earnings source reachable from this environment")
        print("        The pipeline will fall back to WebSearch and produce weaker")
        print("        dossiers. Point the Routines at an environment with full")
        print("        network access. See docs/ROUTINES.md.")
        for line in out.splitlines():
            print(f"        {line}")

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All plumbing checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
