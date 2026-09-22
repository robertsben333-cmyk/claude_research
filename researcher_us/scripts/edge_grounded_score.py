#!/usr/bin/env python3
"""Grounded Edge Scorer: Applying Symmetric Unit-Volatility Calibration to Runtime Unpriced Findings.

Reads the unpriced findings emitted by unpriced-hunter (hunts/*.json), loads the
calibrated response matrix from the shadow ledger, and computes:

    Grounded_Impact_{tau}(j) = S_j * kappa_{tau, line_j} * IV_{live}

Where:
    - S_j is Claude's raw proposed finding score
    - kappa_{tau, line_j} is the unit-volatility response factor from the shadow ledger
    - IV_{live} is the target equity's live event implied volatility from its sealed baseline
    - Beta is strictly excluded from this mapping (market beta was already stripped in the shadow ledger)

Emits multi-horizon grounded ranking keys (impact_sum_5m, impact_sum_15m, ..., impact_sum_next_close, impact_sum_1m)
into edge-scores-grounded.json alongside raw diagnostics.
"""
import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SHADOW_LEDGER_PATH = REPO / "researcher_us" / "analysis" / "shadow-ledger.json"

TIMEFRAMES = [
    "5m", "15m", "60m", "session_close", "next_open", "next_close", "1d", "5d", "1m"
]

def load_json(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def get_live_event_iv(baseline):
    """Extracts event implied volatility from the sealed baseline file."""
    if not baseline:
        return 1.0
    opts = baseline.get("options") or {}
    em = opts.get("event_implied_move_pct") or opts.get("straddle_implied_move_pct")
    if em and em > 0:
        return float(em)
    hist = baseline.get("history") or {}
    med = hist.get("median_abs_move_pct")
    if med and med > 0:
        return float(med)
    rv = (baseline.get("tape") or {}).get("realised_vol_20d_annualised_pct")
    if rv and rv > 0:
        return round(float(rv) / math.sqrt(252), 2)
    return 3.0  # default floor if no data

def ground_run(run_dir, ledger_path=SHADOW_LEDGER_PATH):
    run_dir = Path(run_dir)
    scores_file = run_dir / "edge-scores.json"
    if not scores_file.exists():
        print(f"Error: {scores_file} does not exist.")
        return None

    scores = load_json(scores_file)
    ledger = load_json(ledger_path) or {"response_matrix": {}}
    resp_matrix = ledger.get("response_matrix", {})

    baselines = {}
    for bp in (run_dir / "baselines").glob("*.json"):
        d = load_json(bp)
        if d and d.get("ticker"):
            baselines[d["ticker"]] = d

    grounded_ranking = []

    for name_row in scores.get("ranking", []):
        t = name_row["ticker"]
        b = baselines.get(t, {})
        live_iv = get_live_event_iv(b)
        findings = name_row.get("findings", [])

        row_out = dict(name_row)
        row_out["live_event_iv_pct"] = live_iv
        row_out["grounded_impacts"] = {}

        # For each timeframe, calculate the grounded impact sum
        for tf in TIMEFRAMES:
            tf_findings = []
            tf_sum = 0.0

            for f in findings:
                raw_score = float(f.get("expected_impact_pct") or 0.0)
                line = f.get("lands_on") or "other"
                
                # Get kappa for this line & timeframe
                line_params = resp_matrix.get(line, {}).get(tf, {})
                kappa = line_params.get("kappa", 0.0)

                # SYMMETRIC FORMULA: Grounded = S_j * kappa * IV_live
                # If kappa is 0 (unobserved in shadow ledger), fall back to raw score
                if kappa != 0.0:
                    grounded_f = round(raw_score * kappa * live_iv, 3)
                    calibrated = True
                else:
                    grounded_f = raw_score
                    calibrated = False

                tf_findings.append({
                    "finding_key": f.get("key"),
                    "raw_score": raw_score,
                    "lands_on": line,
                    "kappa": kappa,
                    "grounded_impact": grounded_f,
                    "calibrated": calibrated
                })
                tf_sum += grounded_f

            row_out["grounded_impacts"][tf] = {
                "impact_sum": round(tf_sum, 3),
                "conviction": round(abs(tf_sum), 3),
                "findings": tf_findings
            }

        grounded_ranking.append(row_out)

    out = {
        "run": str(run_dir),
        "grounded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "timeframes_tracked": TIMEFRAMES,
        "ranking": grounded_ranking
    }

    out_file = run_dir / "edge-scores-grounded.json"
    out_file.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Successfully wrote grounded scores across 9 timeframes to {out_file}")
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True, help="Path to edge run directory (e.g. research/2026/09/2026-09-09/edge)")
    ap.add_argument("--ledger", default=str(SHADOW_LEDGER_PATH), help="Path to shadow ledger JSON")
    args = ap.parse_args()

    ground_run(args.run, args.ledger)

if __name__ == "__main__":
    main()
