#!/usr/bin/env python3
"""
Collapse the whole archive into one flat table of every prediction ever made.

The per-day files are the record, but they are scattered across
research/<Y>/<M>/<date>/ and split between advice, panel and outcome files. This
walks all of it and emits one row per (run date, ticker) — the file you open to
ask "what did we call, and what happened", or to load into a spreadsheet.

Derived state: safe to delete and rebuild at any time.

    python3 scripts/build_predictions.py
    python3 scripts/build_predictions.py --since 2026-08-01
"""

import argparse
import csv
import glob
import json
import os
import re
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(REPO_ROOT, "research")

COLUMNS = [
    "run_date", "ticker", "company", "session", "event_date",
    "panelled", "call", "certainty_tier", "prob_direction",
    "signed_estimated_move", "unsigned_expected_move",
    "band_low", "band_high", "event_implied_move",
    "consensus_score", "disparity", "panel_alignment",
    "reversal_risk", "reversal_risk_tier",
    "preliminary_direction_score", "evidence_completeness",
    "change_expectation", "ai_edge",
    "actual_move", "direction_hit", "magnitude_error", "band_hit",
    "implied_move_broken", "reversal_fired", "outcome_status",
]


def _read_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _get(d, *keys, default=None):
    """First present, non-None key from a dict."""
    if not isinstance(d, dict):
        return default
    for k in keys:
        if d.get(k) is not None:
            return d[k]
    return default


def collect(since=None):
    rows = []
    for run_dir in sorted(glob.glob(os.path.join(RESEARCH, "*", "*", "*"))):
        day = os.path.basename(run_dir)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
            continue
        if since and day < since:
            continue

        advice = _read_json(os.path.join(run_dir, "04-advice.json"))
        if not advice:
            continue  # no calls made that day

        shortlist = _read_json(os.path.join(run_dir, "01-shortlist.json")) or {}
        triage = {n.get("ticker"): n for n in shortlist.get("shortlist", []) or []}

        outcome = _read_json(os.path.join(run_dir, "05-outcome.json")) or {}
        outcomes = {n.get("ticker"): n for n in outcome.get("names", []) or []}

        for name in advice.get("ranked_names", []) or []:
            ticker = name.get("ticker")
            if not ticker:
                continue

            # The panel file carries the richest version of the numbers.
            panel = _read_json(os.path.join(run_dir, "03-panel", f"{ticker}.json")) or {}
            syn = panel.get("synthesis") or {}
            dossier = _read_json(
                os.path.join(run_dir, "02-dossiers", f"{ticker}.json")) or {}
            t = triage.get(ticker, {})
            o = outcomes.get(ticker, {})
            band = syn.get("move_band_low_high") or [None, None]

            rows.append({
                "run_date": advice.get("run_date", day),
                "ticker": ticker,
                "company": _get(name, "company") or dossier.get("company"),
                "session": _get(name, "session") or dossier.get("session") or t.get("session"),
                "event_date": _get(name, "event_date") or dossier.get("event_date"),
                "panelled": bool(name.get("panelled")),
                "call": _get(name, "call", default=syn.get("call")),
                "certainty_tier": _get(name, "certainty_tier", default=syn.get("certainty_tier")),
                "prob_direction": _get(name, "prob_direction", default=syn.get("prob_direction")),
                "signed_estimated_move": _get(name, "signed_estimated_move",
                                              default=syn.get("signed_estimated_move")),
                "unsigned_expected_move": _get(name, "unsigned_expected_move",
                                               default=syn.get("unsigned_expected_move")),
                "band_low": band[0],
                "band_high": band[1],
                "event_implied_move": _get(syn, "event_implied_reference",
                                           default=dossier.get("event_implied_move_pct")),
                "consensus_score": syn.get("consensus_score"),
                "disparity": syn.get("disparity"),
                "panel_alignment": syn.get("panel_alignment"),
                "reversal_risk": syn.get("consensus_reversal_risk"),
                "reversal_risk_tier": _get(name, "reversal_risk_tier",
                                           default=syn.get("reversal_risk_tier")),
                "preliminary_direction_score": dossier.get("preliminary_direction_score"),
                "evidence_completeness": _get(name, "evidence_completeness",
                                              default=dossier.get("evidence_completeness")),
                "change_expectation": t.get("change_expectation"),
                "ai_edge": t.get("ai_edge"),
                "actual_move": o.get("actual_move"),
                "direction_hit": o.get("direction_hit"),
                "magnitude_error": o.get("magnitude_error"),
                "band_hit": o.get("band_hit"),
                "implied_move_broken": o.get("implied_move_broken"),
                "reversal_fired": o.get("reversal_fired"),
                # Distinguishes "not scored yet" from "scored, and here is the result".
                "outcome_status": (o.get("outcome") or ("scored" if o else "pending")),
            })
    return rows


def summarise(rows):
    scored = [r for r in rows if r["direction_hit"] is not None]
    panelled = [r for r in scored if r["panelled"]]
    hits = sum(1 for r in panelled if r["direction_hit"])
    errs = [abs(r["magnitude_error"]) for r in panelled
            if isinstance(r.get("magnitude_error"), (int, float))]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_days": len({r["run_date"] for r in rows}),
        "predictions_total": len(rows),
        "predictions_panelled": sum(1 for r in rows if r["panelled"]),
        "predictions_scored": len(scored),
        "panelled_direction_hit_rate": round(hits / len(panelled), 3) if panelled else None,
        "panelled_mean_abs_magnitude_error": round(sum(errs) / len(errs), 2) if errs else None,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--since", metavar="YYYY-MM-DD", help="Only runs on or after this date")
    p.add_argument("--out-csv", default=os.path.join(REPO_ROOT, "PREDICTIONS.csv"))
    p.add_argument("--out-json", default=os.path.join(REPO_ROOT, "PREDICTIONS.json"))
    args = p.parse_args()

    rows = collect(args.since)
    rows.sort(key=lambda r: (r["run_date"], r["ticker"]), reverse=True)
    summary = summarise(rows)

    with open(args.out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    with open(args.out_json, "w", encoding="utf-8") as fh:
        json.dump({"summary": summary, "predictions": rows}, fh, indent=2)
        fh.write("\n")

    print(f"{summary['predictions_total']} prediction(s) across "
          f"{summary['run_days']} run day(s); "
          f"{summary['predictions_scored']} scored")
    if summary["panelled_direction_hit_rate"] is not None:
        print(f"panelled direction hit rate: "
              f"{summary['panelled_direction_hit_rate']:.0%}")
    print(f"wrote {args.out_csv}")
    print(f"wrote {args.out_json}")


if __name__ == "__main__":
    main()
