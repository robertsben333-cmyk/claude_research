#!/usr/bin/env python3
"""
Check that a stage wrote what the next stage expects.

Each stage runs this on its own output before publishing. A stage that writes a
malformed file silently poisons every later stage of the day, so this fails
loudly instead.

    python3 scripts/validate_stage.py shortlist research/2026/08/2026-08-10/01-shortlist.json
    python3 scripts/validate_stage.py panel     research/2026/08/2026-08-10/03-panel/TTWO.json
    python3 scripts/validate_stage.py advice    research/2026/08/2026-08-10/04-advice.json

Exit 0 = valid, 1 = invalid (problems printed to stderr).
"""

import argparse
import json
import sys

CALLS = {"Strong Up", "Lean Up", "Neutral / No Edge", "Lean Down", "Strong Down"}
CERTAINTY = {"High", "Med", "Low"}


def _num(problems, obj, key, lo, hi, where, required=True):
    if key not in obj or obj[key] is None:
        if required:
            problems.append(f"{where}: missing '{key}'")
        return
    v = obj[key]
    if not isinstance(v, (int, float)):
        problems.append(f"{where}: '{key}' must be a number, got {type(v).__name__}")
    elif not (lo <= v <= hi):
        problems.append(f"{where}: '{key}' = {v} outside [{lo}, {hi}]")


def validate_shortlist(doc, problems):
    names = doc.get("shortlist")
    if not isinstance(names, list) or not names:
        problems.append("root: 'shortlist' must be a non-empty list")
        return
    seen = set()
    for i, n in enumerate(names):
        w = f"shortlist[{i}]"
        for key in ("ticker", "company", "session", "event_date", "selection_rationale"):
            if not n.get(key):
                problems.append(f"{w}: missing '{key}'")
        t = n.get("ticker")
        if t in seen:
            problems.append(f"{w}: duplicate ticker '{t}'")
        seen.add(t)
        _num(problems, n, "change_expectation", 0, 100, w)
        _num(problems, n, "ai_edge", 0, 100, w)
        _num(problems, n, "priority_score", 0, 100, w)
        if n.get("session") not in ("amc", "bmo"):
            problems.append(f"{w}: 'session' must be 'amc' or 'bmo'")


def validate_panel(doc, problems):
    if not doc.get("ticker"):
        problems.append("root: missing 'ticker'")
    verdicts = doc.get("panel_verdicts")
    if not isinstance(verdicts, list):
        problems.append("root: 'panel_verdicts' must be a list")
        return
    if len(verdicts) != 7:
        problems.append(f"root: expected 7 panel verdicts, got {len(verdicts)}")
    personas = set()
    for i, v in enumerate(verdicts):
        w = f"panel_verdicts[{i}]"
        p = v.get("persona")
        if not p:
            problems.append(f"{w}: missing 'persona'")
        elif p in personas:
            problems.append(f"{w}: duplicate persona '{p}'")
        personas.add(p)
        _num(problems, v, "direction_score", -100, 100, w)
        _num(problems, v, "prob_up", 0, 100, w)
        _num(problems, v, "reversal_risk", 0, 100, w)
        if v.get("confidence") not in CERTAINTY:
            problems.append(f"{w}: 'confidence' must be one of {sorted(CERTAINTY)}")
        if len(v.get("key_sources") or []) < 2:
            problems.append(f"{w}: needs at least 2 entries in 'key_sources'")
        if not (v.get("key_drivers") or []):
            problems.append(f"{w}: 'key_drivers' is empty")
        if not v.get("top_risk_to_my_call"):
            problems.append(f"{w}: missing 'top_risk_to_my_call'")

    s = doc.get("synthesis")
    if not isinstance(s, dict):
        problems.append("root: missing 'synthesis' object")
        return
    _num(problems, s, "consensus_score", -100, 100, "synthesis")
    _num(problems, s, "prob_up", 0, 100, "synthesis")
    _num(problems, s, "disparity", 0, 100, "synthesis")
    _num(problems, s, "consensus_reversal_risk", 0, 100, "synthesis")
    _num(problems, s, "unsigned_expected_move", 0, 200, "synthesis")
    if s.get("call") not in CALLS:
        problems.append(f"synthesis: 'call' must be one of {sorted(CALLS)}")
    if s.get("certainty_tier") not in CERTAINTY:
        problems.append(f"synthesis: 'certainty_tier' must be one of {sorted(CERTAINTY)}")

    # The conviction gate: Neutral must not carry a signed point estimate.
    signed = s.get("signed_estimated_move")
    if s.get("call") == "Neutral / No Edge" and signed is not None:
        problems.append("synthesis: Neutral / No Edge must have 'signed_estimated_move': null")
    if s.get("call") in CALLS - {"Neutral / No Edge"} and signed is None:
        problems.append(f"synthesis: '{s.get('call')}' requires a signed_estimated_move")

    # Direction must agree with the call.
    if isinstance(signed, (int, float)):
        if "Up" in (s.get("call") or "") and signed < 0:
            problems.append("synthesis: Up call with a negative signed_estimated_move")
        if "Down" in (s.get("call") or "") and signed > 0:
            problems.append("synthesis: Down call with a positive signed_estimated_move")

    band = s.get("move_band_low_high")
    if not (isinstance(band, list) and len(band) == 2):
        problems.append("synthesis: 'move_band_low_high' must be [low, high]")
    elif band[0] > band[1]:
        problems.append("synthesis: move band low is above high")

    # Magnitude discipline: the point estimate is a fraction of the expected move.
    em = s.get("unsigned_expected_move")
    if isinstance(signed, (int, float)) and isinstance(em, (int, float)) and em > 0:
        ratio = abs(signed) / em
        if ratio > 0.85:
            problems.append(
                f"synthesis: |signed_estimated_move| is {ratio:.0%} of the expected move "
                "(cap is ~0.8x even for a high-certainty Strong call)"
            )


def validate_advice(doc, problems):
    ranked = doc.get("ranked_names")
    if not isinstance(ranked, list) or not ranked:
        problems.append("root: 'ranked_names' must be a non-empty list")
        return
    for i, n in enumerate(ranked):
        w = f"ranked_names[{i}]"
        if not n.get("ticker"):
            problems.append(f"{w}: missing 'ticker'")
        if n.get("panelled") and n.get("call") not in CALLS:
            problems.append(f"{w}: panelled name needs a valid 'call'")
    if not doc.get("run_date"):
        problems.append("root: missing 'run_date'")


VALIDATORS = {
    "shortlist": validate_shortlist,
    "panel": validate_panel,
    "advice": validate_advice,
}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("kind", choices=sorted(VALIDATORS))
    p.add_argument("path")
    args = p.parse_args()

    try:
        with open(args.path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except OSError as exc:
        sys.exit(f"cannot read {args.path}: {exc}")
    except ValueError as exc:
        sys.exit(f"{args.path} is not valid JSON: {exc}")

    problems = []
    VALIDATORS[args.kind](doc, problems)

    if problems:
        print(f"INVALID {args.kind}: {args.path}", file=sys.stderr)
        for prob in problems:
            print(f"  - {prob}", file=sys.stderr)
        sys.exit(1)

    print(f"valid {args.kind}: {args.path}")


if __name__ == "__main__":
    main()
