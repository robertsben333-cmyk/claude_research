#!/usr/bin/env python3
"""Is each hunt finished research? Run before edge_score.py on every searcher stage.

A hunt whose search was cut off -- the WebSearch budget ran out, a usage or rate limit
refused the calls -- is not finished research and must never rank, be judged or be
traded beside the hunts that finished (operator, 2026-10-28: five of twenty searchers
hit the shared search budget that day, and two of them, HRTG and CYH, were bought).
The searcher records it itself as `search_complete: false`; this script is the
backstop and the way the orchestrator records what a hand-back said.

  python3 researcher_us/scripts/hunt_status.py check --run <RUN>/edge-panel
  python3 researcher_us/scripts/hunt_status.py check --run <RUN>/edge-panel --apply
  python3 researcher_us/scripts/hunt_status.py mark  --run <RUN>/edge-panel --ticker HRTG \
          --reason "WebSearch budget ran out mid-hunt (hand-back)"
  python3 researcher_us/scripts/hunt_status.py retry --run <RUN>/edge-panel --ticker HRTG

`check` lists every hunt as finished, UNFINISHED or `no flag`, and with `--apply` marks a
hunt whose own text says its search was cut off (the patterns below; they are narrow on
purpose, so "cat budget" or "carrier budgets" do not trip them). `mark` sets the flag by
hand. `retry` moves the unfinished hunt to hunts/_unfinished/ so a fresh searcher can
write hunts/<T>.json again; edge_score.py reads hunts/ non-recursively, so the old file
is kept and ignores itself. edge_score.py makes an unfinished hunt not rankable, which
keeps it out of the panel packs, the panel and the book.
"""
import argparse, json, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

CUT_OFF = re.compile(
    r"(web ?search|search(es)?|tool)[- ](call )?(budget|limit|quota|cap)\b[^.]{0,40}"
    r"(ran out|run out|exhausted|reached|hit|used up|refused)"
    r"|(budget|quota|limit) (for the turn |for this turn )?(ran|run|was) (out|exhausted|reached)"
    r"|usage limit|rate[- ]limit(ed)? (refused|hit)|search was cut (off|short)"
    r"|hunt is (cut short|incomplete)",
    re.I)


def hunts(run):
    return sorted(p for p in (Path(run) / "hunts").glob("*.json"))


def status(h):
    if h.get("search_complete") is False:
        return "UNFINISHED", h.get("search_incomplete_reason") or "flagged by the searcher"
    m = CUT_OFF.search(json.dumps(h, ensure_ascii=False))
    if m:
        return "UNFINISHED?", f"text says: '{m.group(0)}'"
    if h.get("search_complete") is True:
        return "finished", ""
    return "no flag", "searcher did not write search_complete; read its hand-back"


def mark(path, reason):
    h = json.load(open(path))
    h["search_complete"] = False
    h["search_incomplete_reason"] = reason
    h["search_incomplete_marked_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(h, open(path, "w"), ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "mark", "retry"])
    ap.add_argument("--run", required=True)
    ap.add_argument("--ticker")
    ap.add_argument("--reason", default="search cut off (WebSearch budget or usage limit)")
    ap.add_argument("--apply", action="store_true", help="check: mark what the text shows")
    a = ap.parse_args()
    run = Path(a.run)

    if a.cmd in ("mark", "retry"):
        if not a.ticker: sys.exit("--ticker is required")
        p = run / "hunts" / f"{a.ticker}.json"
        if not p.exists(): sys.exit(f"no hunt at {p}")
        if a.cmd == "mark":
            mark(p, a.reason); print(f"{a.ticker}: marked unfinished ({a.reason})")
        else:
            dest = run / "hunts" / "_unfinished"; dest.mkdir(exist_ok=True)
            n = len(list(dest.glob(f"{a.ticker}*.json")))
            target = dest / (f"{a.ticker}.json" if n == 0 else f"{a.ticker}-try{n + 1}.json")
            shutil.move(str(p), target)
            print(f"{a.ticker}: unfinished hunt moved to {target}; relaunch the searcher on {p}")
        return

    unfinished = 0
    for p in hunts(run):
        h = json.load(open(p)); st, why = status(h)
        if st == "UNFINISHED?" and a.apply:
            mark(p, "search cut off, from the hunt's own text: " + why.split("'")[1]); st = "UNFINISHED"
        unfinished += st.startswith("UNFINISHED")
        print(f"{p.stem:8s} {st:12s} {why}")
    print(f"{unfinished} unfinished of {len(hunts(run))}"
          + ("" if a.apply or not unfinished else "; '?' rows are not marked until --apply or mark"))


if __name__ == "__main__":
    main()
