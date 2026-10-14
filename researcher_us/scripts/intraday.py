#!/usr/bin/env python3
"""Stage E-PI: stage E-P's panel, re-run from scratch at fixed times through the US session.

Built 2026-10-14 on the operator's instruction: "a routine for the US that does the same
as US-panel, but runs it independently every 1,5 hours starting from 10.00, and saves
these so we can see the development". Each fire is a fresh session that seals its own
baselines, launches its own searchers and its own four judges, and writes one SNAPSHOT
directory. The day's name set is frozen by the first snapshot (universe + sweep) so every
snapshot answers about the same names and only the evidence and the clock move.

Layout, beside stage E-P's own directory, with the date still the parent so every
per-run script (edge_score, panel_packs, panel_score, edge_resolve) works unchanged:

  research/<Y>/<M>/<DATE>/edge-intraday/            the day: names.json, timeline.{json,md}
  research/<Y>/<M>/<DATE>/edge-intraday-1000/       one snapshot per slot, E-P's layout
  research/<Y>/<M>/<DATE>/edge-intraday-1130/ ...

Nothing pools these with stage E-P: the directory names match no `edge-panel` glob, the
provenance market is `US-PI`, the panel is scored with --dry-run so the panel history
(the reference every judge's percentile is read against) never sees an intraday size.

  python3 researcher_us/scripts/intraday.py slot  [--now ISO]          which snapshot this fire is
  python3 researcher_us/scripts/intraday.py freeze --snap <SNAP>       first snapshot: freeze the names
  python3 researcher_us/scripts/intraday.py prefilter --snap <SNAP>    no frozen set and 16:00: bmo only, before the sweep
  python3 researcher_us/scripts/intraday.py seed   --snap <SNAP>       later snapshots: copy them in
  python3 researcher_us/scripts/intraday.py guard  --snap <SNAP>       drop amc hunts that ran past the release
  python3 researcher_us/scripts/intraday.py timeline --run <RUN>       the day's development, per name

THE ONE LEAK THIS STAGE HAS AND STAGE E-P DOES NOT. Stage E-P starts at 13:06 ET and is
done long before an amc release. A snapshot started at 14:30 or 16:00 ET is not: its
searchers can still be searching when tonight's amc names publish results, and a searcher
that reads the release is reporting the outcome. Two rules close it, both mechanical:
`seed`/`freeze` leave every amc name out of a snapshot whose slot is at or after
`amc_last_slot_et` (16:00: that snapshot is bmo only), and `guard` moves any amc hunt
written at or after `amc_release_cutoff_et` (16:00 ET on the event date) out of the
scored set, with its baseline, before edge_score.py reads them. A guarded name is
`rankable: false` for that snapshot, never a zero.
"""
import argparse, json, os, shutil, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[2]
ET = ZoneInfo("America/New_York")
PREFIX = "edge-intraday"


def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml"))
    return c.get("edge_panel_intraday") or {}


def hm(s):
    h, m = str(s).split(":")
    return int(h) * 60 + int(m)


def run_dir(d):
    return REPO / "research" / f"{d:%Y}" / f"{d:%m}" / d.isoformat()


def slot_for(now_utc, C):
    """The snapshot this fire is. The nearest configured slot within the tolerance gives
    the label (`1130`); a fire outside every slot keeps its own clock (`1347`) and says
    so, rather than being filed under a slot it did not run at."""
    et = now_utc.astimezone(ET)
    mins = et.hour * 60 + et.minute
    slots = [hm(s) for s in C.get("slots_et", ["10:00", "11:30", "13:00", "14:30", "16:00"])]
    tol = int(C.get("slot_tolerance_min", 45))
    best = min(slots, key=lambda s: abs(s - mins))
    on_slot = abs(best - mins) <= tol
    label_min = best if on_slot else mins
    label = f"{label_min // 60:02d}{label_min % 60:02d}"
    lo, hi = hm(C.get("earliest_et", "09:15")), hm(C.get("latest_et", "16:45"))
    d = et.date()
    run = run_dir(d)
    snap = run / f"{PREFIX}-{label}"
    amc_out = label_min >= hm(C.get("amc_last_slot_et", "16:00"))
    status = "new"
    if (snap / "edge-scores-panel.json").exists():
        status = "complete"
    elif snap.exists():
        status = "partial"
    return {"date": d.isoformat(), "now_et": et.isoformat(timespec="minutes"),
            "weekday": et.weekday() < 5, "inside_hours": lo <= mins <= hi,
            "slot": label, "on_slot": on_slot, "run": str(run), "snap": str(snap),
            "day_dir": str(run / PREFIX), "names_frozen": (run / PREFIX / "names.json").exists(),
            "amc_excluded": amc_out, "status": status}


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _slot_min(snap):
    lab = Path(snap).name.rsplit("-", 1)[-1]
    return int(lab[:2]) * 60 + int(lab[2:]) if lab.isdigit() and len(lab) == 4 else None


def _filter(snap, C, universe, sweep):
    """Write the snapshot's universe.json / sweep.json and intraday.json. amc names are
    left out of a snapshot at or after amc_last_slot_et."""
    snap = Path(snap)
    sm = _slot_min(snap)
    amc_out = sm is not None and sm >= hm(C.get("amc_last_slot_et", "16:00"))
    excluded = {}
    names = []
    for n in universe.get("names") or []:
        if amc_out and n.get("session") == "amc":
            excluded[n["ticker"]] = "amc name: this snapshot starts at or after the amc release"
        else:
            names.append(n)
    u = dict(universe, names=names, count=len(names))
    s = dict(sweep or {})
    if s.get("names"):
        s["names"] = [r for r in s["names"] if r.get("ticker") not in excluded]
    snap.mkdir(parents=True, exist_ok=True)
    (snap / "universe.json").write_text(json.dumps(u, indent=1) + "\n")
    if sweep is not None:
        (snap / "sweep.json").write_text(json.dumps(s, indent=1) + "\n")
    meta = {"stage": "E-PI", "slot": snap.name.rsplit("-", 1)[-1],
            "seeded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "names_from": f"{PREFIX}/names.json",
            "hunt": [n["ticker"] for n in names
                     if not sweep or any(r.get("ticker") == n["ticker"] and r.get("event_confirmed")
                                         for r in (sweep.get("names") or []))],
            "excluded": excluded}
    old = _load(snap / "intraday.json") or {}
    if old.get("guard"):
        meta["guard"] = old["guard"]
    (snap / "intraday.json").write_text(json.dumps(meta, indent=1) + "\n")
    return meta


def freeze(snap, C):
    """First snapshot of the day, after its own universe and sweep: the name set every
    later snapshot uses. First writer wins; a second call never overwrites it."""
    snap = Path(snap)
    day = snap.parent / PREFIX
    out = day / "names.json"
    if out.exists():
        return {"frozen": False, "reason": "already frozen", "path": str(out)}
    sm = _slot_min(snap)
    if sm is not None and sm >= hm(C.get("amc_last_slot_et", "16:00")):
        return {"frozen": False, "reason": "a snapshot that excludes amc names never freezes the day's set"}
    u, s = _load(snap / "universe.json"), _load(snap / "sweep.json")
    if u is None:
        sys.exit(f"no universe.json in {snap}: run edge_universe.py into the snapshot first")
    day.mkdir(parents=True, exist_ok=True)
    doc = {"date": snap.parent.name, "frozen_by": snap.name,
           "frozen_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "universe": u, "sweep": s}
    out.write_text(json.dumps(doc, indent=1) + "\n")
    _filter(snap, C, u, s)
    return {"frozen": True, "path": str(out), "names": len(u.get("names") or [])}


def prefilter(snap, C):
    """Only when names are not frozen yet: drop amc rows from the snapshot's own
    universe.json BEFORE its sweep, when the snapshot starts at or after the amc release,
    so not even the sweep reads tonight's releases."""
    snap = Path(snap)
    u = _load(snap / "universe.json")
    if u is None:
        sys.exit(f"no universe.json in {snap}")
    meta = _filter(snap, C, u, None)
    return {"names": len(u.get("names") or []) - len(meta["excluded"]), "excluded": meta["excluded"]}


def seed(snap, C):
    snap = Path(snap)
    doc = _load(snap.parent / PREFIX / "names.json")
    if doc is None:
        return {"seeded": False, "reason": "no names.json yet: this snapshot builds and freezes them"}
    meta = _filter(snap, C, doc["universe"], doc.get("sweep"))
    return {"seeded": True, "hunt": meta["hunt"], "excluded": meta["excluded"]}


def guard(snap, C, now=None):
    """Move any amc hunt written at or after the release cutoff on its event date (and
    its baseline) into _after_release/, which edge_score.py does not read."""
    snap = Path(snap)
    cut = C.get("amc_release_cutoff_et", "16:00")
    moved = {}
    sessions = {}
    for b in (snap / "baselines").glob("*.json"):
        d = _load(b) or {}
        sessions[b.stem] = (d.get("session"), d.get("event_date") or d.get("date"))
    for h in sorted((snap / "hunts").glob("*.json")):
        t = h.stem.split("-")[0]
        sess, ev = sessions.get(t, (None, None))
        if sess != "amc" or not ev:
            continue
        h_, m_ = (int(x) for x in cut.split(":"))
        cutoff = datetime.fromisoformat(ev).replace(hour=h_, minute=m_, tzinfo=ET)
        written = datetime.fromtimestamp(h.stat().st_mtime, tz=timezone.utc)
        if written >= cutoff:
            dest = snap / "_after_release"
            (dest / "hunts").mkdir(parents=True, exist_ok=True)
            (dest / "baselines").mkdir(parents=True, exist_ok=True)
            shutil.move(str(h), dest / "hunts" / h.name)
            b = snap / "baselines" / f"{t}.json"
            if b.exists():
                shutil.move(str(b), dest / "baselines" / b.name)
            moved[t] = {"hunt_written_utc": written.isoformat(timespec="seconds"),
                        "cutoff_et": cutoff.isoformat(timespec="minutes")}
    meta = _load(snap / "intraday.json") or {}
    meta["guard"] = {"ran_utc": (now or datetime.now(timezone.utc)).isoformat(timespec="seconds"),
                     "cutoff_et": cut, "moved": moved}
    (snap / "intraday.json").write_text(json.dumps(meta, indent=1) + "\n")
    return meta["guard"]


def timeline(run):
    """Per name, the panel's call in every snapshot of the day, oldest first, with stage
    E-P's 13:06 run beside it as a reference column (not a snapshot)."""
    run = Path(run)
    snaps = sorted(p for p in run.glob(f"{PREFIX}-*") if p.is_dir() and _slot_min(p) is not None)
    cols = []
    for p in snaps:
        j = _load(p / "edge-scores-panel.json")
        if j:
            cols.append((p.name.rsplit("-", 1)[-1], j))
    ep = _load(run / "edge-panel" / "edge-scores-panel.json")
    sess = {}
    for p in snaps + [run / "edge-panel"]:
        for b in (p / "baselines").glob("*.json"):
            sess.setdefault(b.stem, (_load(b) or {}).get("session"))
    names = sorted({r["ticker"] for _, j in cols for r in j["ranking"]}
                   | ({r["ticker"] for r in ep["ranking"]} if ep else set()))
    rows = []
    for t in names:
        cells = {}
        for lab, j in cols:
            r = next((x for x in j["ranking"] if x["ticker"] == t), None)
            if r:
                cells[lab] = {"panel_pct": r.get("panel_pct"), "side": r.get("side"),
                              "selected": r.get("selected"),
                              "expected_return_pct": r.get("expected_return_pct"),
                              "members": {m: {"pct": x.get("pct"), "side": x.get("side")}
                                          for m, x in (r.get("members") or {}).items()}}
        seq = [c for c in cells.values()]
        sides = [c["side"] for c in seq if c.get("side")]
        er = next((x for x in ep["ranking"] if x["ticker"] == t), None) if ep else None
        rows.append({"ticker": t, "session": sess.get(t), "snapshots": cells,
                     "side_flips": sum(a != b for a, b in zip(sides, sides[1:])),
                     "times_selected": sum(bool(c.get("selected")) for c in seq),
                     "pct_first": seq[0]["panel_pct"] if seq else None,
                     "pct_last": seq[-1]["panel_pct"] if seq else None,
                     "edge_panel_1306": ({"panel_pct": er.get("panel_pct"), "side": er.get("side"),
                                          "selected": er.get("selected")} if er else None)})
    out = {"date": run.name, "stage": "E-PI", "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "slots": [lab for lab, _ in cols],
           "members_present": {lab: j.get("members_present") for lab, j in cols},
           "note": ("Each snapshot is an independent stage E-P run (own baselines, searchers and judges). "
                    "Cells are panel_pct 0-100 with the side, * = selected (panel_pct >= 80, all members). "
                    "edge_panel_1306 is stage E-P's own run, shown for reference and never pooled. "
                    "Research only, no orders."),
           "names": rows}
    day = run / PREFIX
    day.mkdir(parents=True, exist_ok=True)
    (day / "timeline.json").write_text(json.dumps(out, indent=1) + "\n")
    (day / "timeline.md").write_text(render_md(out))
    return out


def _cell(c):
    if not c or c.get("panel_pct") is None:
        return "·"
    s = "L" if (c.get("side") or 0) > 0 else "S" if (c.get("side") or 0) < 0 else "-"
    return f"{c['panel_pct']:.0f}{s}{'*' if c.get('selected') else ''}"


def render_md(out):
    slots = out["slots"]
    L = [f"# Intraday panel (stage E-PI), {out['date']}", "",
         "Each column is an independent stage E-P run at that New York time: fresh baselines, fresh "
         "searchers, a fresh blind four-model panel. A cell is `panel_pct` (0-100, the mean of the four "
         "judges' own percentiles) with the side, L or S; `*` marks a selected name (80 or more, all four "
         "judges present); `·` means the name was not in that snapshot (an amc name after 16:00, or a hunt "
         "the release guard removed). `E-P 13:06` is stage E-P's own run, for reference only.", "",
         "| ticker | session | " + " | ".join(f"{s[:2]}:{s[2:]}" for s in slots) + " | E-P 13:06 | flips | selected |",
         "| --- | --- | " + " | ".join("---:" for _ in slots) + " | ---: | ---: | ---: |"]
    for r in sorted(out["names"], key=lambda r: (-(r["pct_last"] or 0), r["ticker"])):
        L.append(f"| {r['ticker']} | {r['session'] or 'n/a'} | "
                 + " | ".join(_cell(r["snapshots"].get(s)) for s in slots)
                 + f" | {_cell(r['edge_panel_1306'])} | {r['side_flips']} | {r['times_selected']}/{len(r['snapshots'])} |")
    missing = {s: [m for m in ("opus5", "opus55", "sonnet55", "fable51") if m not in (out["members_present"].get(s) or [])]
               for s in slots}
    gaps = [f"{s[:2]}:{s[2:]} without {', '.join(v)}" for s, v in missing.items() if v]
    L += ["", "Judges missing: " + ("; ".join(gaps) if gaps else "none") + ".", "",
          "One day is an anecdote; the snapshots share a name set and a market, so they are not "
          "independent evidence of anything. Research only, not investment advice.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("slot"); s.add_argument("--now", help="ISO time with zone (default: the clock)")
    for name in ("freeze", "prefilter", "seed", "guard"):
        sub.add_parser(name).add_argument("--snap", required=True)
    sub.add_parser("timeline").add_argument("--run", required=True)
    a = ap.parse_args()
    C = cfg()
    if a.cmd == "slot":
        now = datetime.fromisoformat(a.now) if a.now else datetime.now(timezone.utc)
        print(json.dumps(slot_for(now, C), indent=1))
    elif a.cmd == "freeze":
        print(json.dumps(freeze(a.snap, C), indent=1))
    elif a.cmd == "prefilter":
        print(json.dumps(prefilter(a.snap, C), indent=1))
    elif a.cmd == "seed":
        print(json.dumps(seed(a.snap, C), indent=1))
    elif a.cmd == "guard":
        print(json.dumps(guard(a.snap, C), indent=1))
    else:
        out = timeline(a.run)
        print((Path(a.run) / PREFIX / "timeline.md").read_text())


if __name__ == "__main__":
    main()
