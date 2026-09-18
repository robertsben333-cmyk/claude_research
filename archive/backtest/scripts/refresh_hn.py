#!/usr/bin/env python3
"""Re-run only the Hacker News half of the informal layer.

The relevance filter (FINDINGS section 26) landed mid-run, so events harvested
before it carry unfiltered noise -- 60 items about "cat box" for Box, Inc.

StockTwits is deliberately NOT re-run. It pages backward from today, so every day
that passes makes an older event more expensive to reach and eventually
unreachable. Re-paging to fix an unrelated bug would trade real coverage for
tidiness.
"""
import json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT
from corpus_social import hackernews

draw = json.load(open(ROOT / "runs" / "pilot-40" / "draw.json", encoding="utf-8"))
changed = 0
for ev in draw["events"]:
    d = ROOT / "events" / f"{ev['ticker']}-{ev['event_date']}"
    mp = d / "social_manifest.json"
    if not mp.exists():
        continue
    m = json.loads(mp.read_text(encoding="utf-8"))
    if m.get("hackernews", {}).get("dropped_as_irrelevant") is not None:
        continue                                    # already filtered
    cutoff = datetime.fromisoformat(m["cutoff"].replace("Z", "+00:00"))
    fence = datetime.fromisoformat(m["fence_utc"].replace("Z", "+00:00"))
    start = datetime.fromisoformat(m["window_start_utc"].replace("Z", "+00:00"))
    before = m["hackernews"]["items"]
    hn, errs, dropped = hackernews(ev.get("company", ""), ev["ticker"],
                                   int(fence.timestamp()), int(start.timestamp()))
    f = d / "social" / "hackernews.txt"
    if hn:
        lines = [f"HACKER NEWS  {ev.get('company') or ev['ticker']}",
                 f"FENCE: strictly before {m['fence_utc']}", f"ITEMS: {len(hn)}",
                 "", "-" * 72, ""]
        for h in sorted(hn, key=lambda x: x["created_at"] or ""):
            lines.append(f"{h['created_at']}  {h.get('title') or '(comment)'}  "
                         f"{h['hn_url']}\n  {(h['text'] or '')[:2000]}\n")
        f.write_text("\n".join(lines), encoding="utf-8")
    elif f.exists():
        f.unlink()
    m["hackernews"] = {"items": len(hn), "errors": errs,
                       "dropped_as_irrelevant": dropped,
                       "file": "social/hackernews.txt" if hn else None,
                       "note": "typoTolerance=false; relevance-filtered; "
                               "thin for non-developer names"}
    mp.write_text(json.dumps(m, indent=1), encoding="utf-8")
    if before != len(hn):
        changed += 1
        print(f"  {ev['ticker']:6} {before:3} -> {len(hn):3} items ({dropped} dropped as irrelevant)")
print(f"\n{changed} events corrected")
