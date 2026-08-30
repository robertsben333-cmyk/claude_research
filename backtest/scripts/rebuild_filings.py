#!/usr/bin/env python3
"""Rebuild every filings corpus after the form-priority fix.

Selecting by recency alone let Form 4s eat the budget -- a median 29 of 41
documents per event -- and left BEN and UCTT with no 10-Q or 10-K at all, while
the document count still looked healthy.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, ticker_cik_map
from corpus_edgar import build as harvest

draw = json.loads((ROOT / "runs" / "pilot-40" / "draw.json").read_text(encoding="utf-8"))
cm = ticker_cik_map()
rows = []
for e in draw["events"]:
    t, ed = e["ticker"], e["event_date"]
    d = ROOT / "events" / f"{t}-{ed}"
    if not d.exists():
        continue
    for old in (d / "filings").glob("*.txt"):
        old.unlink()
    try:
        res = harvest(t, e.get("cik") or cm.get(t), ed, str(d)); ok = res[0] if isinstance(res, tuple) else res
    except Exception as ex:
        rows.append((t, "FAILED", str(ex)[:50], 0, 0)); continue
    m = json.loads((d / "filings_manifest.json").read_text(encoding="utf-8"))
    from collections import Counter
    c = Counter((x.get("form") or "?") for x in m["documents"])
    per = c.get("10-Q", 0) + c.get("10-K", 0)
    rows.append((t, ok, c.get("4", 0), c.get("8-K", 0), per))
    time.sleep(0.4)

print(f"{'tick':6}{'docs':>6}{'F4':>5}{'8-K':>6}{'periodic':>10}  flag")
noper = 0
for t, ok, f4, k8, per in rows:
    flag = "" if per else "STILL NO PERIODIC REPORT"
    if not per:
        noper += 1
    print(f"{t:6}{str(ok):>6}{str(f4):>5}{str(k8):>6}{str(per):>10}  {flag}")
print(f"\nevents with no 10-Q/10-K: {noper}")
