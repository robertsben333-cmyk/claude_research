#!/usr/bin/env python3
"""Which captures hold material fetched after the print they are supposed to precede.

The first contamination check in this repo compared each snapshot's timestamp
against the capture's directory date -- the date the earnings *calendar* claimed
-- and found zero violations across 205 captures. That check was answering the
wrong question. `seal.py` moves an event to its 8-K or 6-K acceptance date, and
where that lands *earlier* than the calendar date the capture went on sweeping
past the print it had already missed.

The GAUZ hunter found this by itself and said so: capture filed under
GAUZ-2026-09-02, seal puts the print at 2026-08-31T13:10Z, so `quote.json`
carries the 08-31 and 09-01 closes and two of three stored bodies were fetched
after the print. It declared the leak, refused to read the post-print bodies, and
asked to be treated as compromised. That is the honest-agent path from
FINDINGS.md section 32 working exactly as intended -- and it is not a substitute
for the harness knowing.

Compared against the sealed acceptance instant, not a date, because a bmo print
at 13:10Z and a snapshot at 15:07Z the same day are hours apart in the wrong
direction.

    python3 backtest/scripts/edge_corpus_audit.py
    python3 backtest/scripts/edge_corpus_audit.py --json
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs" / "edge-corpus"


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def audit_one(cap, accepted_utc, session):
    """Snapshots, stored bodies and price bars taken after the print.

    The bar test is session-dependent and the first version of it was wrong in the
    direction that manufactures alarm: it counted the event day's own close as
    post-print for every name, which flagged 83 of 109. For an `amc` print that
    close is the *pre*-print close -- the left-hand side of the repo's own
    close-to-close convention -- so only later bars leak. For a `bmo` print the
    event day's close is the reaction itself.
    """
    cut = parse(accepted_utc)
    late_snaps, late_items, late_bars = [], 0, []
    for s in sorted((cap / "snapshots").glob("*.json")):
        raw = s.name.replace(".json", "")   # e.g. 20260902T150755Z
        stamp = datetime.strptime(raw, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        if stamp > cut:
            late_snaps.append(raw)
            try:
                late_items += json.loads(s.read_text(encoding="utf-8")).get("n_items", 0) or 0
            except Exception:
                pass
    q = cap / "quote.json"
    if q.exists():
        try:
            bars = json.loads(q.read_text(encoding="utf-8")).get("bars") or []
            ed = cut.date().isoformat()
            late_bars = [b["date"] for b in bars if b["date"] > ed]
            if session == "bmo":
                late_bars += [b["date"] for b in bars if b["date"] == ed]
        except Exception:
            pass
    return {"late_snapshots": late_snaps, "late_snapshot_items": late_items,
            "late_bars": sorted(set(late_bars))}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = []
    for man in sorted(RUNS.glob("*/manifest.json")):
        m = json.loads(man.read_text(encoding="utf-8"))
        for e in m["events"]:
            cap = ROOT.parent / e["capture"]
            seal = json.loads((cap / "seal.json").read_text(encoding="utf-8"))
            r = audit_one(cap, seal["accepted_utc"], e["session"])
            r.update(ticker=e["ticker"], event_date=e["event_date"],
                     session=e["session"], calendar_date=e["calendar_date"],
                     capture=e["capture"], accepted_utc=seal["accepted_utc"])
            r["contaminated"] = bool(r["late_snapshots"]) or bool(r["late_bars"])
            rows.append(r)

    bad = [r for r in rows if r["contaminated"]]
    out = RUNS / "contamination.json"
    out.write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "basis": "every snapshot, stored body and price bar compared against the sealed "
                 "8-K/6-K acceptance instant, not the calendar date the capture was "
                 "filed under",
        "names": len(rows), "contaminated": len(bad),
        "rows": sorted(rows, key=lambda r: (not r["contaminated"], r["ticker"])),
    }, indent=1) + "\n", encoding="utf-8")

    # A non-destructive clean view per contaminated name. The capture corpus is the
    # archive and is not rewritten; instead each affected event gets an explicit list
    # of the snapshots an agent may read and the last bar it may look at, and the
    # brief passes that on. Dropping these names instead would cost 31 of 109.
    for r in rows:
        if not r["contaminated"]:
            continue
        cap = ROOT.parent / r["capture"]
        allowed = sorted(s.name.replace(".json", "")
                         for s in (cap / "snapshots").glob("*.json")
                         if s.name.replace(".json", "") not in r["late_snapshots"])
        ed = r["event_date"]
        last_bar = ed if r["session"] == "amc" else "the last bar strictly before " + ed
        (RUNS / r["event_date"] / "clean-view").mkdir(parents=True, exist_ok=True)
        (RUNS / r["event_date"] / "clean-view" / f"{r['ticker']}.json").write_text(
            json.dumps({
                "ticker": r["ticker"], "event_date": ed, "session": r["session"],
                "accepted_utc": r["accepted_utc"],
                "reason": "this capture kept sweeping after the print; the snapshots and "
                          "bars named below are the only admissible ones",
                "allowed_snapshots": allowed,
                "excluded_snapshots": r["late_snapshots"],
                "excluded_bars": r["late_bars"],
                "last_admissible_bar": last_bar,
            }, indent=1) + "\n", encoding="utf-8")

    if a.json:
        print(json.dumps(bad, indent=1))
        return
    for r in bad:
        print(f"{r['ticker']:7s} {r['event_date']} {r['session']}  "
              f"cal={r['calendar_date']}  "
              f"late_snaps={len(r['late_snapshots'])} ({r['late_snapshot_items']} items)  "
              f"late_bars={len(r['late_bars'])}")
    print(f"\n{len(bad)} of {len(rows)} names hold post-print material")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
