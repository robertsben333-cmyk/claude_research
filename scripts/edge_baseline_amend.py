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
#
# THIS TABLE IS PER-RUN AND MUST BE REWRITTEN FROM EACH DAY'S SWEEP.
# It is not a growing registry: the tickers below are the ones the CURRENT run's
# sweep found defective. A stale table silently prints "SKIP no baseline" for
# every entry and then "DRY RUN", which reads exactly like "nothing to amend" --
# on 2026-09-01 the 2026-08-31 table was still in place and did that. The guard
# in main() now makes a fully stale table exit non-zero instead of looking clean.
AMENDMENTS = {
    "WDH": ("unknown",
            "DOWNGRADE, and on 2026-09-04 it is the ONLY amendment -- a pass whose "
            "sole entry lowers a verdict, which is worth stating plainly because the "
            "symmetry rule is usually invoked the other way round. Waterdrop's "
            "2026-09-08 pre-open date IS confirmed by its own PR Newswire release of "
            "2026-08-25 (call 8:00 a.m. ET), so the event is real. But the "
            "'fits_cadence' verdict is an artefact: it rests on a median gap of 85 "
            "days computed over a filing set that contains THREE 6-Ks inside one "
            "quarter -- 2026-06-17, 2026-06-23 and 2026-07-24 -- where at most one "
            "earnings release can exist. As a foreign private issuer Waterdrop files "
            "no item 2.02, and it 6-Ks its buybacks, special dividends and AGM "
            "material, all of which carry results-shaped language the text matcher "
            "accepts. The verdict also reads 'last print 2026-07-24', 46 days ago, "
            "which would make the 2026-09-08 event a second print inside the same "
            "quarter. Only the five older entries (2025-03-12, 2025-06-05, "
            "2025-09-04, 2025-12-03, 2026-03-25) form a clean quarterly chain, so "
            "the 2.29% median and the 1.5% deadband derived from it rest on eight "
            "rows of which at most six are earnings reactions. 'unknown' not "
            "'suspect': the event is established, its history simply does not "
            "characterise it.",
            "https://en.prnasia.com/releases/global/waterdrop-inc-to-report-second-quarter-2026-financial-results-on-september-8-2026-545126.shtml"),
}

# DELIBERATELY NOT AMENDED on 2026-09-04, and this is the judgement, not an
# oversight. CAN and GMHS both carry cadence_implausible with verdict 'unknown',
# and both events are confirmed by the company's own press release with the hour
# -- so the instinct is to upgrade them to fits_cadence. They stay at 'unknown'
# (event_q 0.6) for exactly the DOO/PSNY/VBNK/ZGN reason below: in both names the
# 6-K text matcher caught NON-EARNINGS filings, so the recorded reactions are not
# earnings base rates and upgrading would forgive a history defect and hand each
# name a 1.0 multiplier it has not earned.
#   CAN: 8 filings at a 13-day median gap, including a 2026-07-14/07-15 pair one
#        day apart. Canaan 6-Ks its monthly bitcoin-production and mining-fleet
#        updates. No quarterly reporter has a 13-day cadence.
#   GMHS: 8 filings at a 55-day median. On a 2026-06-30 fiscal year end the real
#        prints are 2025-09-09, 2025-11-25, 2026-03-23 and 2026-06-24; the other
#        three (2026-07-13, 07-14, 08-28) sit outside any reporting quarter. The
#        2026-06-24 row is also tagged session 'intraday', so its +9.84% is not a
#        clean overnight reaction. Usable base rate is 4 events, not 8.
# ABM and UNFI are untouched: both domestic, both on exact 8-K item 2.02
# acceptance times, both rated history-trustworthy by the sweep.
#
# Net effect of this pass: WDH loses the 1.0 event multiplier it had not earned,
# and no name gains one. Per-name history warnings go to the hunters instead.
_RETIRED_2026_09_02 = {
    "MEI": ("fits_cadence",
            "UPGRADE. Date and session confirmed by Methode Electronics' own "
            "GlobeNewswire release of 2026-08-26: Q1 FY2027 (period ended "
            "2026-08-01) issued after the close on 2026-09-02, call the next "
            "morning at 08:00 ET. The 'unknown' verdict came from history.n=0, and "
            "that zero is the SAME RECORDS BUG as PANW and CXM: priced_in.py "
            "discarded all 68 prior item 2.02 prints on CIK 0000065270 as 'filed "
            "under a former name', and EDGAR's submissions API lists no former "
            "name for Methode -- it has been METHODE ELECTRONICS INC since 1994. "
            "Three registrants producing this artefact across three runs is a bug "
            "in the former-name filter, not three records events. The thin history "
            "is NOT forgiven here: hist_n stays 0, hist_q stays 0, and the name "
            "still pays for it in baseline_quality. Hunters are told explicitly "
            "that this baseline carries NO earnings base rate and that the absence "
            "is an artefact, so they must not read it as a quiet history.",
            "https://www.globenewswire.com/news-release/2026/08/26/3351719/0/en/methode-electronics-announces-first-quarter-fiscal-2027-results-conference-call.html"),
    "GOLD": ("fits_cadence",
             "UPGRADE. Date and session confirmed by the company's own "
             "GlobeNewswire release of 2026-08-19: fiscal Q4 and full-year FY2026 "
             "(year ended 2026-06-30) call on 2026-09-02 at 16:30 ET, results "
             "issued before the call. Unlike MEI this was NOT a records bug -- the "
             "history was correctly truncated to 2 prints because A-Mark Precious "
             "Metals really did rename to Gold.com, Inc. on 2025-12-01 (former-name "
             "record on CIK 0001591588). So the two surviving reactions are genuine "
             "earnings reactions to this registrant and the sweep rates the history "
             "trustworthy; there are simply only two of them, which hist_q already "
             "prices. The event-existence flag was the only thing wrong.",
             "https://www.globenewswire.com/news-release/2026/08/19/3347585/31746/en/gold-com-sets-fiscal-fourth-quarter-and-full-year-2026-earnings-call-for-wednesday-september-2-at-4-30-p-m-et.html"),
    "WLYB": ("unknown",
             "DOWNGRADE -- one of the two symmetric halves of this pass. WLYB is "
             "John Wiley & Sons CLASS B and WLY is class A: one company, one CIK "
             "(0000107140), one 8-K, one earnings event on 2026-09-03 bmo. The "
             "calendar carries them as two rows with an identical market cap and an "
             "identical year-ago EPS, which is the tell. 'fits_cadence' is therefore "
             "true of the underlying company but false of this row as an independent "
             "event, and the seven recorded 'reactions' are measured on a line that "
             "trades 247 shares a day -- two of them are exactly 0.00%, i.e. an "
             "unchanged last trade rather than a reaction. Downgraded to 'unknown' "
             "rather than 'suspect': the event is real, this row just is not a "
             "separate one and its history is not a price series.",
             "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000107140&type=8-K"),
    "AMBR": ("unknown",
             "DOWNGRADE -- the other symmetric half. 'fits_cadence' rests on a "
             "77-day median gap in 6-K text matches, but the only evidence for a "
             "2026-09-03 print is the calendar row itself. Amber has always "
             "pre-announced by 6-K (the 2026-05-21 6-K set the 2026-05-28 Q1 call), "
             "and every 6-K on CIK 0001697818 since July -- 2026-07-28, 2026-08-10 "
             "(leadership changes) and 2026-08-31 (the AMBR agentic-AI rebrand) -- "
             "contains no results date, with the supposed print one day away. Last "
             "year's comparable half-year report landed 2025-09-10, a week later "
             "than the calendar's date. Not set to 'suspect', which would bar the "
             "name from ranking on absence of evidence alone; 'unknown' states "
             "exactly what is known, which is that the event is unestablished.",
             "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001697818&type=6-K"),
}

# DELIBERATELY NOT AMENDED, and this is the judgement, not an oversight:
# DOO, PSNY, VBNK and ZGN all carry cadence_implausible and all four are real,
# company-confirmed events -- so the instinct is to upgrade them to fits_cadence.
# They stay at 'unknown' (event_q 0.6) because in every one of the four the 6-K
# text matcher caught NON-EARNINGS filings, exactly the CANG/NIO failure mode:
# DOO's 7 matches are monthly 6-K wrappers, PSNY's 8 are monthly delivery updates
# (one of them the scheduling release itself), VBNK's 8 are near-daily regulatory
# and capital-ratio filings, and ZGN's 8 are quarterly revenue announcements plus
# a 20-F notice. Their recorded medians are therefore not earnings base rates.
# 'unknown' is the correct middle for "the event exists but its history does not
# characterise it"; upgrading to fits_cadence would forgive the history defect and
# hand each name a 1.0 multiplier it has not earned. Per-name history warnings go
# to the hunters instead.
_RETIRED_2026_09_01 = {
    "PANW": ("fits_cadence",
             "UPGRADE. Date and session confirmed by Palo Alto Networks' own press "
             "release for a 2026-09-01 after-close release (webcast 4:30 p.m. ET). "
             "The 'unknown' verdict came from history.n=0, and that zero is a "
             "RECORDS BUG, not a cadence problem: priced_in.py discarded all 28 "
             "prior prints on CIK 0001327567 as 'filed under a former name before "
             "2026-08-27'. PANW has not changed its name. A company-issued "
             "scheduling release is stronger evidence the event exists than any "
             "cadence inference, so the event-existence flag goes to fits_cadence. "
             "The thin history is NOT forgiven by this: hist_q stays 0 and still "
             "costs the name 40% of baseline_quality in the right term.",
             "https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-to-announce-fiscal-fourth-quarter-and-fiscal-year-2026-financial-results-on-tuesday--september-1--2026"),
    "CXM": ("fits_cadence",
            "UPGRADE. Date and session confirmed by Sprinklr's own press release of "
            "2026-08-12 for a pre-open 2026-09-02 release (call 8:30 a.m. ET), "
            "consistent with Q2 FY26 released pre-open 2025-09-03. Identical "
            "records bug to PANW: all 21 prints on CIK 0001569345 discarded as "
            "'former name before 2026-08-19'. Sprinklr has not changed its name. "
            "Two registrants producing the same artefact two weeks apart is a bug "
            "in the former-name filter, not two records events.",
            "https://www.nasdaq.com/press-release/sprinklr-announces-date-second-quarter-financial-results-2026-08-12"),
    "GASS": ("unknown",
             "UPGRADE from suspect. StealthGas' own press release of 2026-08-28 "
             "confirms Q2 2026 results before the New York open on 2026-09-02. The "
             "'suspect' flag is a FALSE POSITIVE: the 6-K text matcher counted that "
             "very SCHEDULING RELEASE as an earnings print, producing an impossible "
             "'event 5 days after the last print' against an 88-day cadence. The "
             "same artefact appears a year earlier (2025-08-25 and 2025-08-29, four "
             "days apart, one of them a scheduling notice). Set to 'unknown' and "
             "NOT fits_cadence, because at least two of the eight recorded "
             "reactions are reactions to a date announcement, so the 1.19% median "
             "is diluted and is not an earnings-reaction base rate.",
             "https://www.globenewswire.com/news-release/2026/08/28/3352793/9952/en/stealthgas-inc-announces-the-date-for-the-release-of-the-second-quarter-2026-financial-and-operating-results-conference-call-and-webcast.html"),
    "YSG": ("unknown",
            "DOWNGRADE, not an upgrade -- the symmetric half of this pass. Yatsen's "
            "2026-09-02 pre-open date is confirmed by its own IR page, so the event "
            "is real; but the 'fits_cadence' verdict rests on the same foreign "
            "private issuer 6-K text-matching defect. The history contains a "
            "literal DUPLICATE (2026-03-02 twice with an identical -8.99%) and two "
            "entries five days apart (2026-05-21 and 2026-05-26) where the "
            "company's own release puts the Q1 print on 2026-05-26 -- so 2026-05-21 "
            "is a different 6-K, not an earnings print. At least three of eight rows "
            "are not distinct earnings reactions, so the 8.99% median and the 4.5% "
            "deadband derived from it are both overstated.",
            "https://ir.yatsenglobal.com/2026-08-26-Yatsen-to-Announce-Second-Quarter-2026-Financial-Results-on-September-2,-2026"),
}

_RETIRED_2026_08_31 = {
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

    # A stale per-run table prints only "SKIP no baseline" lines and then "DRY
    # RUN", which is indistinguishable from "this run needed no amendments".
    # Refuse to look clean: if not one entry matches a baseline in this dir, the
    # table belongs to another run and has not been rewritten.
    present = [t for t in AMENDMENTS if (Path(a.dir) / f"{t}.json").exists()]
    if AMENDMENTS and not present:
        raise SystemExit(
            f"STALE AMENDMENTS TABLE: none of {sorted(AMENDMENTS)} has a baseline "
            f"in {a.dir}. This table is per-run -- rewrite it from THIS run's sweep "
            f"before applying. Exiting non-zero rather than reporting 'nothing to "
            f"amend', which is how a stale table hides."
        )

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
        # Rank by the event_q multiplier edge_score.py actually applies, so the
        # printed direction matches the arithmetic effect. The old rule called
        # every non-suspect change a "downgrade", which mislabelled
        # unknown -> fits_cadence and hid whether a pass was really symmetric.
        rank = {"suspect": 0, "unknown": 1, "fits_cadence": 2}
        lo, hi = rank.get(old, 1), rank.get(verdict, 1)
        direction = "upgrade" if hi > lo else "downgrade" if hi < lo else "no change"
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
