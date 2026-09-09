#!/usr/bin/env python3
"""The brief for one day's corpus hunter, and for one day's corpus adversary.

One agent per day rather than one per ticker. The live edge hunt spends a hunter
per name; over 109 events that is 109 opus/high agents and the point of the
backtest is to find out whether the method carries information at all, not to
reproduce its cost. A day-level agent reads the same sealed corpus and emits the
same per-name JSON contract.

What that costs, stated so it is not discovered later: the hunters stop being
independent of each other within a day. A per-ticker hunter cannot be influenced
by what it found on another name; a day hunter ranks its own names implicitly
while sizing them. Between days nothing leaks. `hunter_dispersion_pct` in
`edge_score.py` also goes to zero, since there is only ever one hunter per name.

The adversary stays a separate agent, because its whole function is not having
seen the hunter's numbers. Merging the two would leave `priced_in_pct` set by the
same context that produced `expected_impact_pct`, which is not a check.

    python3 backtest/scripts/edge_corpus_brief.py --day 2026-09-01
    python3 backtest/scripts/edge_corpus_brief.py --day 2026-09-01 --adversary
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs" / "edge-corpus"
REPO = ROOT.parent


def hunter_brief(day):
    run = RUNS / day
    man = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    lines = [
        f"Hunt for unpriced information on the {man['names']} companies below, all of "
        f"which reported earnings on {day}.",
        "",
        "This print has already happened. You have no web tools by design: a search "
        "today returns the outcome. Everything you use must come out of the capture "
        "directory named for each company, and nothing may come from what you know or "
        "can infer about how these prints went.",
        "",
        f"Repository root: {REPO}",
        f"Run directory:   {run}",
        "",
        "For each company:",
        "",
    ]
    for e in man["events"]:
        cap = REPO / e["capture"]
        lines.append(
            f"- **{e['ticker']}** ({e['company']}) — {e['session']} on {e['event_date']}\n"
            f"  baseline: {run / 'baselines' / (e['ticker'] + '.json')}\n"
            f"  capture:  {cap}\n"
            f"  corpus holds {e['items']} captured items, {e['docs']} stored doc bodies"
        )
    lines += [
        "",
        "Read each company's baseline first. None of them carries an option-implied "
        "move or a skew: the chain is not readable as of a past date, so "
        "`options.status` is `not_recoverable_retrospectively` and both fields are "
        "null. Your anchor for how far this name moves on a print is "
        "`expected_move_pct`, which here is the median of its own prior reactions. "
        "Do not manufacture a directional read out of the run-up to replace the skew.",
        "",
        "Work the companies in the order given. Write each one's JSON to "
        f"`{run / 'hunts'}/<TICKER>.json` with `Write` as you finish it, rather than "
        "holding them all to the end — a run that dies partway keeps what is on disk.",
        "",
        "Where a company's corpus is thin, the honest output is a small number or "
        "zero. Every name here is ranked against every other name in the sample, so "
        "a manufactured finding on a thin name does more damage than an empty one: it "
        "displaces a real ordering. An empty `findings` list with "
        "`expected_move_pct: 0` is a complete and correct answer.",
        "",
        "Emit one JSON object per company in the shape your definition specifies. "
        "When you are done, reply with one line per ticker: the ticker, its "
        "`expected_move_pct`, and the number of findings.",
    ]
    return "\n".join(lines)


def adversary_brief(day):
    run = RUNS / day
    man = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    hunts = sorted((run / "hunts").glob("*.json"))
    claims = {}
    for f in hunts:
        d = json.loads(f.read_text(encoding="utf-8"))
        t = (d.get("ticker") or f.stem).upper()
        rows = []
        for i, item in enumerate(d.get("findings") or []):
            rows.append({
                "finding_key": f"{f.stem}#{i}",
                "finding": item.get("finding"),
                "source": item.get("source"),
                "source_date": item.get("source_date"),
                "corpus_ref": item.get("corpus_ref"),
                "body_available": item.get("body_available"),
                "why_not_priced": item.get("why_not_priced"),
                "independence": item.get("independence"),
            })
        if rows:
            claims[t] = rows
    (run / "adversary-briefs").mkdir(exist_ok=True)
    for t, rows in claims.items():
        (run / "adversary-briefs" / f"{t}.json").write_text(
            json.dumps({"ticker": t, "claims": rows}, indent=1) + "\n", encoding="utf-8")

    by_t = {e["ticker"]: e for e in man["events"]}
    lines = [
        f"Judge how much of each claim below is already in the price. "
        f"{len(claims)} companies from the {day} earnings date carry findings.",
        "",
        "You have not seen the hunter's own impact numbers or reasoning and you must "
        "not ask for them. You have the claims, the sealed baseline, and the same "
        "capture directory the hunter read.",
        "",
        f"Repository root: {REPO}",
        f"Run directory:   {run}",
        "",
    ]
    for t in sorted(claims):
        e = by_t.get(t, {})
        lines.append(
            f"- **{t}** — {len(claims[t])} claim(s)\n"
            f"  claims:   {run / 'adversary-briefs' / (t + '.json')}\n"
            f"  baseline: {run / 'baselines' / (t + '.json')}\n"
            f"  capture:  {REPO / e.get('capture', '')}"
        )
    lines += [
        "",
        "No baseline here carries a skew or an implied move, so `the options already "
        "say it` is not available to you. `quote.json` is the strongest tool you do "
        "have and it needs no search: if the stock moved or volume built around the "
        "date a fact became available, it is in the price. Do the arithmetic on the "
        "bars.",
        "",
        "`corpus_coverage` is required on every verdict. A capture ran a bounded set "
        "of queries, so its silence about a fact is not evidence the fact was "
        "unpublished, and a number resting on silence has to be readable as such.",
        "",
        f"Write each company's verdicts to `{run / 'adversary'}/<TICKER>.json` with "
        "`Write` as you finish it. Copy every `finding_key` back exactly.",
        "",
        "When you are done, reply with one line per ticker: the ticker and the "
        "priced_in_pct values you assigned, in order.",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--day", required=True)
    ap.add_argument("--adversary", action="store_true")
    a = ap.parse_args()
    print(adversary_brief(a.day) if a.adversary else hunter_brief(a.day))


if __name__ == "__main__":
    main()
