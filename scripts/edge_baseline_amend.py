#!/usr/bin/env python3
"""Amend a sealed baseline's `event_plausibility` from the sweep's company sources.

WHY THIS IS NOT A CONTAMINATED BASELINE
---------------------------------------
The sealing rule exists so that a *finding* cannot revise what the market had
already priced. This touches neither. `event_plausibility` is a data-quality flag
about whether the earnings event exists at all, derived by `priced_in.py` from the
gap between EDGAR filings. Confirming or killing the event is the sweep's stated
job, and this runs BEFORE any hunter is launched, from company press releases and
6-K/8-K filings only.

WHY IT IS NEEDED
----------------
`edge_score.py` computes `rankable = bool(hunts) and confirmed and plaus !=
"suspect"`, and multiplies `baseline_quality` by 0.05 for a suspect verdict. A
name wrongly flagged suspect is therefore arithmetically incapable of ranking
anywhere, regardless of what is found. On 2026-08-31 the cadence heuristic flagged
three names suspect whose dates are confirmed by their own press releases, because
it was matching monthly operational updates (bitcoin production, vehicle
deliveries) as earnings filings. A 16-day or 10-day "earnings cadence" is the
tell.

SYMMETRY
--------
The correction is applied in BOTH directions in the same pass. Where the matcher
inflated confidence -- NIO's `fits_cadence` rests on the same monthly-update
defect -- the verdict is downgraded too. Only correcting the names that would
score better is how a scorer gets quietly tuned toward a result.

The original verdict is never discarded; it is kept in `amended_from`.

    python3 scripts/edge_baseline_amend.py --dir <RUN>/edge/baselines --apply
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

# ticker -> (new verdict, why, the source that establishes it)
AMENDMENTS = {
    "CANG": ("unknown",
             "Date confirmed by Cango's own IR announcement of 2026-08-25 for a "
             "2026-08-31 release. The 'suspect' flag came from a 16-day inferred "
             "cadence, which is the 6-K text matcher catching MONTHLY bitcoin "
             "production updates as earnings filings -- no quarterly reporter has a "
             "16-day cadence. Set to 'unknown' rather than 'fits_cadence' because "
             "the reaction history in this baseline is measuring those monthly "
             "updates and is not an earnings-reaction base rate.",
             "https://ir.cangoonline.com/"),
    "HMR": ("unknown",
            "Date confirmed by Heidmar's press release of 2026-08-26 for a "
            "2026-09-01 pre-open release. The 97-day gap against an inferred "
            "49-day cadence is not a stopped reporter; Q1 2026 was reported "
            "2026-05-26 and the inferred cadence is an artefact of mixed 6-K "
            "matches. 'unknown' not 'fits_cadence': all six prior prints were AMC "
            "and this one is confirmed BMO, so the history measures a different "
            "release convention.",
            "https://www.globenewswire.com/news-release/2026/08/26/3351433/0/en/heidmar-announces-date-for-the-second-quarter-2026-financial-results-conference-call-and-webcast.html"),
    "PXS": ("unknown",
            "Date confirmed by Pyxis Tankers' press release of 2026-08-26 for an "
            "after-close release on 2026-08-31. The 97-day/51-day cadence "
            "mismatch is an artefact of the same 6-K text matching. 'unknown' "
            "because the eight prior prints carry mixed bmo/amc/intraday session "
            "labels, so their 2.33% median reaction is measured inconsistently.",
            "https://www.globenewswire.com/news-release/2026/08/26/3351690/0/en/pyxis-tankers-announces-date-for-the-release-of-the-second-quarter-2026-results.html"),
    "NIO": ("unknown",
            "DOWNGRADE, not an upgrade. The 2026-09-01 date is confirmed by NIO's "
            "6-K of 2026-08-20, but the 'fits_cadence' verdict rests on a 10-day "
            "inferred cadence -- the matcher is catching MONTHLY VEHICLE DELIVERY "
            "updates, not earnings. As a foreign private issuer NIO files no item "
            "2.02. The eight reactions in this baseline are therefore reactions to "
            "delivery reports, and using them as an earnings base rate would "
            "overstate how well this name's print is characterised.",
            "https://ir.nio.com/"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--apply", action="store_true", help="write; otherwise dry run")
    a = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for t, (verdict, why, url) in sorted(AMENDMENTS.items()):
        p = Path(a.dir) / f"{t}.json"
        if not p.exists():
            print(f"{t:5s} SKIP  no baseline at {p}")
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        ep = d.setdefault("event_plausibility", {})
        old = ep.get("verdict")
        if ep.get("amended_from"):
            print(f"{t:5s} SKIP  already amended from {ep['amended_from']['verdict']}")
            continue
        direction = "upgrade" if old == "suspect" else "downgrade"
        print(f"{t:5s} {old:13s} -> {verdict:9s} ({direction})")
        if not a.apply:
            continue
        ep["amended_from"] = {"verdict": old, "reason": ep.get("reason")}
        ep["verdict"] = verdict
        ep["reason"] = why
        ep["amended_utc"] = now
        ep["amended_by"] = "edge sweep, company-sourced; before any hunter launched"
        ep["amended_source"] = url
        p.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")

    print("\nDRY RUN -- pass --apply to write" if not a.apply else "\nwritten")


if __name__ == "__main__":
    main()
