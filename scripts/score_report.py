#!/usr/bin/env python3
"""The table every hunt stage pastes, verbatim, into its closing chat reply.

Since 2026-10-01 every hunter answers twice, and the reply carries both answers side
by side so nobody has to open a file to see them:

  impact_sum     version 2, THE KEY. Each finding sized on its own, added up. This is
                 what ranks the day, what the 3.0 conviction floor was measured on and,
                 for stage E only, what trades. From edge-scores.json.
  impact_scaled  version 3. (2 * p_up / 100 - 1) * abs_move_pct, the hunter's second,
                 separate measurement of the whole print. From edge-scores-scaled.json,
                 its own file. Not ranked on, not traded, never pooled with the key.
  V2             US only (stage E and stage E-S): the grounded score from
                 edge-scores-grounded.json, at its primary horizon. Shown as
                 "not run" when the file is absent, never left out silently.

Each of the two numbers carries a percentile in brackets, e.g. `+3.40 (p87)`: the share
of earlier rankable names, sized by the SAME hunter model, whose |value| sits below this
one's (ties count half). Model per run from its provenance.json (provenance.for_row,
which infers by date where a run has none). Every stage is pooled per model, synthetic
validation runs and the run itself are left out, and only run dates up to this one's
count, so re-running the report on an old day gives the same brackets. Under 20 earlier
names the bracket reads `n<20` rather than a percentile. It describes SIZE against the
model's own habit, not rank within the day and not a probability, and it pools prompt
versions, which CLAUDE.md forbids for judging a version: read it as scale, nothing more.

    python3 scripts/score_report.py --run research/2026/10/2026-10-02/edge
    python3 scripts/score_report.py --run <RUN>/europe --label "Stage EU"

Reads only; writes nothing. Exits 1 when the run has no edge-scores.json, so a
reply cannot quote a table that was never scored.
"""
import argparse
import json
import sys
from bisect import bisect_left, bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import provenance  # noqa: E402

US_DIRS = {"edge", "edge-sonnet"}
DIR_MARKET = {v["dir"]: k for k, v in provenance.MARKETS.items()}
MIN_HISTORY = 20


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def f(v, fmt="{:+.2f}"):
    return "n/a" if v is None else fmt.format(v)


def run_model(run, reg):
    """The hunter model that sized a run's names, or None. An alias whose served model
    nothing has observed (stage E-S's `sonnet`) is its own group, labelled `sonnet?`;
    an alias caught mid-switch (`opus` on 2026-09-22) is left out rather than guessed."""
    market = DIR_MARKET.get(Path(run).name)
    if not market:
        return None
    try:
        row = provenance.for_row(run, market, reg=reg)
    except Exception:  # a provenance hiccup must not cost the table
        return None
    if row.get("model"):
        return row["model"]
    return row.get("model_short") if row.get("model_basis") == "not_recorded" else None


def impact_of(r):
    """impact_sum; before 2026-09-09 it was not a top-level field and is the sum of the
    findings' sizes by definition, exactly as edge_sample.py re-derives it."""
    if r.get("impact_sum") is not None:
        return r["impact_sum"]
    fs = r.get("findings")
    return sum(x.get("expected_impact_pct") or 0 for x in fs) if fs else None


def model_history(run, reg):
    """{model: {"impact_sum": sorted |values|, "impact_scaled": sorted |values|}} over
    every earlier run on disk, this one excluded."""
    run = Path(run).resolve()
    day = run.parent.name
    hist = {}
    for d in sorted((ROOT / "research").glob("[0-9]*/[0-9]*/[0-9]*-*-*/*/")):
        if d.resolve() == run or d.parent.name > day or d.name not in DIR_MARKET:
            continue
        key = load(d / "edge-scores.json")
        if not key or key.get("legacy_rescore"):
            continue
        if (load(d / "universe.json") or {}).get("validation_only"):
            continue
        model = run_model(d, reg)
        if not model:
            continue
        h = hist.setdefault(model, {"impact_sum": [], "impact_scaled": []})
        for r in key.get("ranking", []):
            v = impact_of(r) if r.get("rankable") else None
            if v is not None:
                h["impact_sum"].append(abs(v))
        for r in (load(d / "edge-scores-scaled.json") or {}).get("ranking", []):
            if r.get("impact_scaled") is not None:
                h["impact_scaled"].append(abs(r["impact_scaled"]))
    for h in hist.values():
        for v in h.values():
            v.sort()
    return hist


def pct(value, ref):
    """Mid-rank percentile of |value| in a sorted list of |values|, as a bracket."""
    if value is None:
        return ""
    if len(ref) < MIN_HISTORY:
        return " (n<20)"
    x = abs(value)
    below, upto = bisect_left(ref, x), bisect_right(ref, x)
    return f" (p{round(100 * (below + 0.5 * (upto - below)) / len(ref))})"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the directory holding edge-scores.json")
    ap.add_argument("--label", help="stage name for the heading, e.g. 'Stage E'")
    ap.add_argument("--us", action="store_true",
                    help="show the V2 column (automatic for edge/ and edge-sonnet/)")
    a = ap.parse_args()

    run = Path(a.run)
    key = load(run / "edge-scores.json")
    if not key:
        print(f"no edge-scores.json in {run}: nothing has been scored", file=sys.stderr)
        sys.exit(1)
    scaled = load(run / "edge-scores-scaled.json")
    sc = {r["ticker"]: r for r in (scaled or {}).get("ranking", [])}
    us = a.us or run.name in US_DIRS
    grounded = load(run / "edge-scores-grounded.json") if us else None
    gr = {r["ticker"]: r for r in (grounded or {}).get("ranking", [])}
    floor = key.get("conviction_floor", 3.0)
    reg = provenance.load_registry()
    model = run_model(run, reg)
    hist = model_history(run, reg).get(model, {"impact_sum": [], "impact_scaled": []})

    label = a.label or run.name
    print(f"**{label}, {run.parent.name}**: ranked on `{key.get('ranking_key')}` "
          f"(version 2, each finding sized on its own); conviction floor {floor:.1f} "
          f"applies to it only.")
    if not scaled:
        print("`edge-scores-scaled.json` is missing: impact_scaled not computed "
              "(re-run edge_score.py).")
    if us:
        if grounded is None:
            v2_state = "V2 not run: no edge-scores-grounded.json in this run."
        elif grounded.get("status") != "calibrated":
            v2_state = f"V2 {grounded.get('status')}: no grounded values."
        else:
            v2_state = (f"V2 at `{grounded.get('primary_horizon')}`, matrix as of "
                        f"{grounded.get('matrix_as_of')}.")
        print(v2_state)
    short = provenance.SHORT_MODEL.get(model, model) if model else None
    if short:
        print(f"Brackets: percentile of |value| among earlier rankable names sized by "
              f"{short} (impact_sum n={len(hist['impact_sum'])}, impact_scaled "
              f"n={len(hist['impact_scaled'])}; all stages pooled). Scale, not rank.")
    else:
        print("Brackets: no percentile, the hunter model of this run is not recorded.")
    print()

    head = ["#", "ticker", "impact_sum (key)", "floor", "impact_scaled (v3)",
            "abs_move", "p_up"]
    if us:
        head.append("V2 grounded")
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join(" --- " for _ in head) + "|")
    dropped = []
    for r in key.get("ranking", []):
        if not r.get("rankable"):
            dropped.append(r)
            continue
        s = sc.get(r["ticker"], {})
        cells = [str(r.get("rank")), r["ticker"],
                 f"**{f(r['impact_sum'])}**" + (pct(r["impact_sum"], hist["impact_sum"])
                                                 if model else ""),
                 "yes" if r.get("conviction", 0) >= floor else "no",
                 f(s.get("impact_scaled")) + (pct(s.get("impact_scaled"),
                                                  hist["impact_scaled"]) if model else ""),
                 f(s.get("abs_move_pct"), "{:.1f}"),
                 f(s.get("p_up"), "{:.0f}")]
        if us:
            g = gr.get(r["ticker"], {})
            if grounded is None or grounded.get("status") != "calibrated":
                cells.append("not run")
            elif g.get("impact_sum_grounded") is None:
                cells.append("n/a" + (f" ({g['not_grounded_because']})"
                                      if g.get("not_grounded_because") else ""))
            else:
                cells.append(f(g["impact_sum_grounded"]))
        print("| " + " | ".join(cells) + " |")
    if not key.get("ranking"):
        print("| | no names | | | | | |" + (" |" if us else ""))
    for r in dropped:
        print(f"\nNot ranked: {r['ticker']}: {r.get('not_rankable_because')}")
    print("\n`impact_scaled` is the hunter's second, separate measurement, "
          "(2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.")


if __name__ == "__main__":
    main()
