#!/usr/bin/env python3
"""Build the adversary brief for each ticker, and verify the verdicts joined back.

The adversary must judge each claim WITHOUT seeing the hunter's own size or its
argument for why the claim is unpriced -- that is the question being asked
independently. So the brief carries the claim, its source and its date, and nothing
else. Doing this by hand in the shell invites two failure modes that this script
exists to remove.

FAILURE MODE 1 -- a leaked hunter number. If `expected_impact_pct` or
`why_not_priced` reaches the adversary, the adversary is no longer independent and
`size_disagreement_pct` downstream becomes meaningless. This script whitelists the
fields that go out rather than blacklisting the ones that must not, so a new field
added to the hunter contract cannot leak by default.

FAILURE MODE 2 -- a broken join key. `edge_score.py` joins verdicts to findings on
`finding_key`, computed there as f"{hunt_file.stem}#{index}". A key that does not
match is dropped SILENTLY: the finding keeps `priced_in_pct = None`, defaults to
"unjudged, mostly priced", and quietly costs that name edge. Nothing errors. This
script generates the keys with the same rule as the scorer, and `--check` re-reads
the adversary directory afterwards and reports any finding that never got a verdict.

    python3 scripts/edge_brief.py --run <RUN>/edge              # write the briefs
    python3 scripts/edge_brief.py --run <RUN>/edge --check      # verify the join
"""
import argparse
import json
import sys
from pathlib import Path

# Exactly what the adversary is allowed to see about a claim. Whitelist, not
# blacklist: anything the hunter invents beyond this stays out by construction.
BRIEF_FIELDS = ("finding", "source", "source_date")


def load_hunts(run):
    """Findings per ticker, keyed exactly as edge_score.py keys them."""
    out = {}
    d = run / "hunts"
    if not d.exists():
        sys.exit(f"no hunts directory at {d}")
    for f in sorted(d.glob("*.json")):
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! {f.name}: unreadable ({e})", file=sys.stderr)
            continue
        ticker = (doc.get("ticker") or f.stem.split("-")[0]).upper()
        for i, item in enumerate(doc.get("findings") or []):
            claim = {"finding_key": f"{f.stem}#{i}"}          # same rule as the scorer
            for k in BRIEF_FIELDS:
                claim[k] = item.get(k)
            if not claim["source"]:
                claim["source"] = "UNSOURCED -- the hunter gave no URL for this claim"
            out.setdefault(ticker, []).append(claim)
    return out


def write_briefs(run, hunts):
    outdir = run / "adversary-briefs"
    outdir.mkdir(parents=True, exist_ok=True)
    for ticker, claims in sorted(hunts.items()):
        hunters = sorted({c["finding_key"].split("#")[0] for c in claims})
        doc = {
            "ticker": ticker,
            "hunters": hunters,
            "findings_to_judge": claims,
            "instructions": (
                "Judge EVERY finding, on both sides. Return priced_in_pct 0-100 and "
                "your own signed size_check_pct for each. Copy finding_key verbatim -- "
                "it is the join key and a typo silently drops the verdict. You have not "
                "been shown the hunters' own sizes or their reasoning, and must not try "
                "to infer them."),
        }
        (outdir / f"{ticker}.json").write_text(
            json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        n_pos = sum(1 for c in claims if c["source"].startswith("UNSOURCED"))
        flag = f"  ({n_pos} unsourced)" if n_pos else ""
        print(f"  {ticker:6s} {len(claims):3d} claims from {len(hunters)} hunter(s){flag}")
    print(f"\nwrote {len(hunts)} briefs to {outdir}")


def check(run, hunts):
    """Did every finding actually get a verdict? Silent drops are the danger."""
    judged, dupes = {}, []
    d = run / "adversary"
    if not d.exists():
        sys.exit(f"no adversary directory at {d} -- nothing to check")
    for f in sorted(d.glob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        for v in (doc.get("verdicts") or [doc]):
            k = v.get("finding_key")
            if k is None:
                continue
            if k in judged:
                dupes.append(k)
            judged[k] = (f.name, v.get("priced_in_pct"), v.get("size_check_pct"))

    all_keys = {c["finding_key"] for cs in hunts.values() for c in cs}
    missing = sorted(all_keys - set(judged))
    orphans = sorted(set(judged) - all_keys)
    nulls = sorted(k for k, (_, p, _) in judged.items() if p is None)

    print(f"findings:        {len(all_keys)}")
    print(f"verdicts joined: {len(all_keys & set(judged))}")
    for label, items, why in (
        ("UNJUDGED", missing,
         "will default to mostly-priced and silently cost that name edge"),
        ("ORPHAN VERDICT", orphans,
         "key matches no finding -- a typo, or a hunt file changed after the brief"),
        ("NULL priced_in_pct", nulls,
         "verdict present but carries no number, treated as unjudged"),
        ("DUPLICATE", sorted(set(dupes)),
         "judged twice; the later one wins, which may not be the one you want"),
    ):
        if items:
            print(f"\n{label} ({len(items)}) -- {why}")
            for k in items:
                print(f"  {k}")

    bad = bool(missing or orphans or nulls or dupes)
    print("\nJOIN CLEAN -- every finding carries an adversary number" if not bad
          else "\nJOIN INCOMPLETE -- fix before trusting edge_score.py output")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the <RUN>/edge directory")
    ap.add_argument("--check", action="store_true",
                    help="verify verdicts joined back, instead of writing briefs")
    a = ap.parse_args()

    run = Path(a.run)
    hunts = load_hunts(run)
    if not hunts:
        sys.exit("no findings in any hunt file")
    if a.check:
        sys.exit(check(run, hunts))
    write_briefs(run, hunts)


if __name__ == "__main__":
    main()
