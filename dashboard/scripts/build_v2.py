#!/usr/bin/env python3
"""Stage E V2 into dashboard/data/v2.json, for the V2 tab.

Two things, both read and neither computed here beyond counting:

  ledger   researcher_us/analysis/shadow-ledger.json: how many 8-Ks are collected,
           scored and measured, and the kappa matrix refitted from them as it stands
           now (edge_shadow_engine.fit_matrix, the same code the scorer uses)
  names    every edge-scores-grounded.json on disk, keyed `run|ticker` so the page
           can join V2 onto the ledger's names and rank pre-lessons, post-lessons
           and V2 against the same exit horizon and the same filters as every
           other tab

The realised moves are NOT here: the page takes them from ledger.json, so all three
scores are ranked against one price source.

    python3 dashboard/scripts/build_v2.py
"""
import glob
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "researcher_us" / "scripts"))
import edge_shadow_engine as shadow  # noqa: E402

OUT = ROOT / "dashboard" / "data" / "v2.json"


def main():
    led = shadow.load_ledger()
    items = led.get("items", [])
    by_status = {}
    for it in items:
        by_status[it["status"]] = by_status.get(it["status"], 0) + 1
    matrix, n_obs = shadow.fit_matrix(items)
    lines = {}
    for it in items:
        if it.get("llm_impact_score") is not None:
            lines[it.get("line_item", "other")] = lines.get(it.get("line_item", "other"), 0) + 1

    names, runs = {}, []
    for gp in sorted(glob.glob(str(ROOT / "research/*/*/*/edge/edge-scores-grounded.json"))):
        g = json.loads(Path(gp).read_text(encoding="utf-8"))
        if g.get("forward") is not True:
            continue                    # forward only: a regrounded old run is a backtest
        run = str(Path(gp).parent.relative_to(ROOT))
        runs.append({"run": run, "status": g.get("status"),
                     "matrix_as_of": g.get("matrix_as_of"),
                     "observations": g.get("ledger_observations_used"),
                     "n_grounded": sum(1 for r in g.get("ranking", [])
                                       if r.get("impact_sum_grounded") is not None)})
        for r in g.get("ranking", []):
            names[f"{run}|{r['ticker']}"] = {
                "v2": r.get("impact_sum_grounded"),
                "vol_only": r.get("control_vol_only"),
                "sigma": r.get("sigma_daily_pct"),
                "status": g.get("status"),
                "why": r.get("not_grounded_because")}

    doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "min_n": int(shadow.cfg("min_n", 30)),
           "primary_horizon": shadow.cfg("primary_horizon", "session_close"),
           "min_event_date": str(shadow.cfg("min_event_date", "2026-07-01")),
           "ledger": {"items": len(items), "by_status": by_status,
                      "observations": n_obs, "scored_by_line": lines,
                      "matrix": matrix, "timeframes": shadow.TIMEFRAMES},
           "runs": runs, "names": names}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT}  ({len(items)} ledger items, {n_obs} observations, "
          f"{len(runs)} grounded runs)")


if __name__ == "__main__":
    main()
