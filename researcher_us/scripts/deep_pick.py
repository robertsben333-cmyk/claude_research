#!/usr/bin/env python3
"""Stage D: draw the day's three names for the deep researcher, at random, seeded by date.

The pool is what stage E would hunt: the sweep's confirmed names, ordered by
`hunt_priority` and cut at `edge_hunt.hunted_names`, minus a name whose sealed baseline
says `event_plausibility: suspect`. From that pool `edge_deep.names_per_day` names are
drawn with a seed derived from the run date, so a re-run draws the same names and nobody
chooses them.

Random rather than "the most researchable names", because any other cut is a second
ranking nobody measures, and it would bias the one comparison this stage exists for:
deep against stage E and E-P on the SAME names. Stage J and EU draw the same way.

    python3 researcher_us/scripts/deep_pick.py --run <RUN>/edge-deep
    python3 researcher_us/scripts/deep_pick.py --run <RUN>/edge-deep --no-amc   # late fire

`--no-amc` drops tonight's amc names from the pool before the draw, for a fire too late
to finish a deep hunt before a 16:00 ET release. It is recorded in pick.json, because it
changes the pool.
"""
import argparse
import hashlib
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def config():
    try:
        import yaml
        c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml"))
    except Exception:
        c = {}
    deep = c.get("edge_deep") or {}
    hunt = c.get("edge_hunt") or {}
    return int(deep.get("names_per_day", 3)), int(hunt.get("hunted_names", 19))


def seed_for(day):
    return int(hashlib.sha256(("stage-D:" + day).encode()).hexdigest()[:12], 16)


def pool_from(sweep, baselines, cap, no_amc):
    names = sweep.get("names") or []
    out, dropped = [], []
    for n in names:
        t = (n.get("ticker") or "").upper()
        if not t:
            continue
        if n.get("event_confirmed") is False:
            dropped.append({"ticker": t, "why": "sweep: event not confirmed"})
            continue
        b = baselines.get(t) or {}
        if b.get("event_plausibility") == "suspect":
            dropped.append({"ticker": t, "why": "baseline: event_plausibility suspect"})
            continue
        out.append(n)
    out.sort(key=lambda n: -(n.get("hunt_priority") or 0))
    for n in out[cap:]:
        dropped.append({"ticker": n["ticker"].upper(), "why": "below stage E's hunted_names cut"})
    out = out[:cap]
    if no_amc:
        keep = []
        for n in out:
            s = (baselines.get(n["ticker"].upper()) or {}).get("session") or n.get("session")
            if s == "amc":
                dropped.append({"ticker": n["ticker"].upper(), "why": "--no-amc: fire too late"})
            else:
                keep.append(n)
        out = keep
    return out, dropped


def draw(pool, k, seed):
    tickers = sorted(n["ticker"].upper() for n in pool)
    rng = random.Random(seed)
    return sorted(rng.sample(tickers, min(k, len(tickers))))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True, help="<RUN>/edge-deep")
    ap.add_argument("--no-amc", action="store_true")
    ap.add_argument("-k", type=int, help="names to draw (default edge_deep.names_per_day)")
    a = ap.parse_args()
    run = Path(a.run)
    k_cfg, cap = config()
    k = a.k or k_cfg
    sweep_path = run / "sweep.json"
    if not sweep_path.exists():
        sys.exit(f"no sweep.json in {run}: run the sweep first")
    sweep = json.loads(sweep_path.read_text())
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        try:
            baselines[f.stem.upper()] = json.loads(f.read_text())
        except Exception:
            pass
    day = run.parent.name
    seed = seed_for(day)
    pool, dropped = pool_from(sweep, baselines, cap, a.no_amc)
    picked = draw(pool, k, seed)
    rows = {n["ticker"].upper(): n for n in pool}
    doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "run": str(run), "date": day, "method": "date_seeded_random_draw",
           "seed": seed, "k": k, "hunted_names_cap": cap, "no_amc": a.no_amc,
           "pool": sorted(rows), "pool_size": len(rows), "dropped": dropped,
           "picked": [{"ticker": t,
                       "session": (baselines.get(t) or {}).get("session") or rows[t].get("session"),
                       "event_date": (baselines.get(t) or {}).get("event_date")
                       or rows[t].get("actual_event_date"),
                       "hunt_priority": rows[t].get("hunt_priority")} for t in picked],
           "note": ("Drawn at random from the names stage E would hunt, so every pick also "
                    "carries a stage E and an E-P score. Nobody chose these names.")}
    (run / "pick.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(f"pool {len(rows)} confirmed names, drew {len(picked)}: {', '.join(picked) or 'none'}"
          f"  (seed {seed}{', no amc' if a.no_amc else ''})")


if __name__ == "__main__":
    main()
