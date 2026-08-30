#!/usr/bin/env python3
"""Rebuild every anchor set after the periodic-report fix.

The prior version keyed prior earnings events on 8-K item 2.02, which some filers
never use. 7 of 40 anchor sets were gapped, the worst by 602 days.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, ticker_cik_map
from anchors import build

draw = json.loads((ROOT / "runs" / "pilot-40" / "draw.json").read_text(encoding="utf-8"))
cm = ticker_cik_map()
changed, failed = [], []
for e in draw["events"]:
    t, ed, sess = e["ticker"], e["event_date"], e["session"]
    d = ROOT / "events" / f"{t}-{ed}"
    if not d.exists():
        continue
    old_n = 0
    ap = d / "anchors.json"
    if ap.exists():
        old = json.loads(ap.read_text(encoding="utf-8"))
        old_n = len(old.get("historical_earnings_moves", []))
        old_dates = {h["event_date"] for h in old.get("historical_earnings_moves", [])}
    else:
        old_dates = set()
    try:
        a = build(t, e.get("cik") or cm.get(t), ed, sess)
    except Exception as ex:
        failed.append((t, f"{type(ex).__name__}: {str(ex)[:60]}"))
        continue
    new_dates = {h["event_date"] for h in a.get("historical_earnings_moves", [])}
    ap.write_text(json.dumps(a, indent=1), encoding="utf-8")
    if new_dates != old_dates:
        changed.append((t, old_n, len(new_dates), sorted(new_dates - old_dates)[-3:]))
    time.sleep(0.3)

print(f"rebuilt {len(draw['events'])} anchor sets; {len(changed)} changed, {len(failed)} failed\n")
for t, o, n, added in changed:
    print(f"  {t:6} {o} -> {n} prior events   newly included: {', '.join(added) or '-'}")
for t, why in failed:
    print(f"  FAILED {t}: {why}")
