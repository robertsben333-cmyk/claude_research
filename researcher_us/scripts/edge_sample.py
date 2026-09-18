#!/usr/bin/env python3
"""The resolved edge-hunt sample, every run, both score schemas.

WHY NOT edge_decompose.py
-------------------------
`edge_decompose.py` reads `edge_score`, `edge_pct`, `confidence` and
`baseline_quality` off each ranked row. Those fields left the top level of
`edge-scores.json` on 2026-09-09 when `impact_sum` became the ranking key, so it
raises `KeyError: 'edge_score'` on every run from 09-09 onward and the analysis in
`researcher_us/EDGE_ANALYSIS.md` has been stuck on the first six days ever since -- 43 names,
38 after de-duplication. Seven more runs were on disk and in no sample.

This reads the fields that exist in BOTH schemas, so the whole archive loads:

    impact_sum   the ranking key, present throughout
    conviction   abs(impact_sum), the only cut that survived a correction
    priced_lean_pct, run_up_20d_pct, event_implied_move_pct, spot, adv    baseline

ONE NUMBER IS RE-DERIVED, AND ONLY ONE. Before 2026-09-09 `impact_sum` was not a
top-level field: the key was `edge_score` and the hunters' sizes lived inside
`findings`. Summing them is the definition of `impact_sum` -- `edge_score.py` and
`edge_decompose.py` both write exactly that sum -- so 47 of the 106 events carry a
derived value, flagged `impact_sum_derived: true`. Nothing else is reconstructed.
If a number was not written by the run that made it, this module does not invent it.

DE-DUPLICATION IS NOT OPTIONAL
------------------------------
09-07 re-hunts five of 09-04's prints and 09-09/09-10 overlap too. `--pool` in
`edge_resolve.py` double-counts those, which is how `edge_score`'s trading return
came out positive: `researcher_us/EDGE_ANALYSIS.md` records that de-duplicated it falls to
+0.09%/day. Events here are keyed on (ticker, event_date, session) and the EARLIER
hunt is kept, because that is the one that was made without seeing the later day.

WHAT IS EXCLUDED, AND WHY EACH
------------------------------
  not rankable        no hunt, no event, a phantom row, or a second share class.
                      Includes `event_occurred: false` -- TRT 2026-09-17, which the
                      calendar promised and EDGAR never delivered
  unresolved          the event window has not closed yet. An event is resolved
                      once the first full session after the print has ended
"""
import glob
import json
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _company_names(run):
    """ticker -> company, from whichever universe file the run wrote."""
    out = {}
    for name in ("universe-with-unknown.json", "universe.json"):
        p = Path(run) / name
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:                                    # noqa: BLE001
            continue
        for n in d.get("names") or []:
            if n.get("ticker") and n.get("company"):
                out.setdefault(n["ticker"], n["company"])
    return out


def load(pattern="research/2026/*/*/edge", resolved_before=None):
    """Every rankable, resolved event across the archive, de-duplicated.

    `resolved_before` is a date; an event whose exit session is not strictly before
    it is dropped as unresolved. Defaults to today, so a print from last night --
    whose first full session is still running -- never enters a sample.
    """
    cutoff = resolved_before or date.today()
    runs = sorted(p for p in glob.glob(str(REPO / pattern)) if Path(p).is_dir())
    seen, events = {}, []
    for run in runs:
        run = str(Path(run).relative_to(REPO))
        sf = REPO / run / "edge-scores.json"
        if not sf.exists():
            continue
        sc = json.loads(sf.read_text())
        if sc.get("legacy_rescore"):
            continue                    # midpoints assigned after the fact, not evidence
        names = _company_names(REPO / run)
        for n in sc.get("ranking") or []:
            if not n.get("rankable"):
                continue
            t = n["ticker"]
            bp = REPO / run / "baselines" / f"{t}.json"
            if not bp.exists():
                continue
            b = json.loads(bp.read_text())
            ed, sess = b.get("event_date"), (b.get("session") or "bmo")
            if not ed:
                continue
            # the first full session after the print: the event date for bmo,
            # the day after for amc. Resolved once that session is behind us.
            settle = datetime.fromisoformat(ed).date()
            if sess == "amc":
                settle += timedelta(days=1)
            if settle >= cutoff:
                continue
            key = (t, ed, sess)
            if key in seen:
                continue
            tape, opt = b.get("tape") or {}, b.get("options") or {}
            fs = n.get("findings") or []
            # THE ONE THING THIS MODULE RECOMPUTES, AND ONLY BECAUSE IT HAS TO.
            # Runs before 2026-09-09 predate `impact_sum` as a top-level field: the
            # key was `edge_score` and the hunters' raw sizes lived only inside
            # `findings`. The sum is the definition -- edge_score.py and
            # edge_decompose.py both write exactly this -- so summing it here
            # reproduces the number rather than inventing one. Without it, 47 of 105
            # events carry no prediction at all and every hit rate is deflated by
            # counting them as misses.
            impact = n.get("impact_sum")
            if impact is None:
                impact = round(sum(x.get("expected_impact_pct") or 0 for x in fs), 6)
                derived = True
            else:
                derived = False
            ev = {
                "run": run, "run_date": run.split("/")[3], "ticker": t,
                "company": names.get(t), "event_date": ed, "session": sess,
                "impact_sum": impact,
                "impact_sum_derived": derived,
                "conviction": n.get("conviction", abs(impact)),
                "priced_lean_pct": n.get("priced_lean_pct"),
                "run_up_20d_pct": tape.get("run_up_20d_pct"),
                "implied_move_pct": opt.get("event_implied_move_pct"),
                "expected_move_pct": b.get("expected_move_pct"),
                "spot": tape.get("spot"),
                "adv_20d": tape.get("avg_volume_20d"),
                "n_findings": len(fs),
                "hunters": (n.get("diagnostics") or {}).get("hunters"),
            }
            ev["dollar_vol"] = round((ev["spot"] or 0) * (ev["adv_20d"] or 0))
            seen[key] = True
            events.append(ev)
    return events


if __name__ == "__main__":
    import argparse
    import collections
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", default="research/2026/*/*/edge")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    ev = load(a.pool)
    if a.json:
        print(json.dumps(ev, indent=1))
    else:
        per = collections.Counter(e["run_date"] for e in ev)
        for d in sorted(per):
            print(f"  {d}  {per[d]:3d}")
        print(f"\n{len(ev)} resolved, de-duplicated events over {len(per)} run days")
        print(f"{sum(1 for e in ev if abs(e['impact_sum'] or 0) >= 3)} at or above "
              f"the 3.0 conviction floor")
