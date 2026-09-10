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
    "CSBR": ("fits_cadence",
             "UPGRADE off 'suspect', and it is the ONLY amendment in today's pass "
             "that changes anything ranked: edge_score.py sets rankable=False on a "
             "suspect verdict and multiplies baseline_quality by 0.05, so Champions "
             "Oncology would have been arithmetically incapable of ranking anywhere "
             "despite a company-confirmed event. Every other verdict on this run "
             "feeds only event_q (1.0 / 0.6 / 0.05) into baseline_quality, which "
             "lives in diagnostics and decides nothing. The 'suspect' verdict is a "
             "false positive off the fiscal calendar, not off a matcher defect: "
             "Champions has an APRIL 30 year end, so FY results land in late July "
             "and Q1 follows only ~45 days later, which the cadence heuristic reads "
             "as a sub-quarterly gap. The same 45-day pattern produced the "
             "2025-09-15 print already sitting in the baseline's own history. The "
             "company's press release confirms Q1 (quarter ended 2026-07-31) after "
             "the close on 2026-09-10 with a 4:30 p.m. EDT call. Domestic item-2.02 "
             "filer and the sweep rates the seven recorded reactions trustworthy, "
             "so unlike the FPI names below there is no history defect to forgive "
             "and fits_cadence is the honest verdict rather than 'unknown'.",
             "https://www.biospace.com/press-releases/champions-oncology-to-announce-first-quarter-financial-results-on-thursday-september-10-2026"),
    "ZUMZ": ("fits_cadence",
             "UPGRADE off 'unknown'. Zumiez is a long-listed domestic retailer and "
             "the 'unknown' rests on history.n=0, which is a COLLECTION FAILURE and "
             "not a cadence problem -- the same records artefact as PANW, CXM and "
             "MEI on earlier runs. The event itself is confirmed by the company's "
             "own GlobeNewswire release of 2026-08-27: fiscal 2026 Q2 results "
             "'following the closing of regular stock market trading hours' on "
             "2026-09-10, call 5:00 p.m. ET. The thin history is NOT forgiven by "
             "this: hist_n stays 0 and the name still pays for it in "
             "baseline_quality, and its hunter is told explicitly that the baseline "
             "carries NO earnings base rate and that the absence is an artefact, so "
             "it must not read the silence as a quiet history.",
             "https://www.globenewswire.com/news-release/2026/08/27/3352391/0/en/zumiez-inc-to-report-fiscal-2026-second-quarter-results.html"),
    "CMCM": ("unknown",
             "DOWNGRADE off 'fits_cadence' -- the symmetric half of this pass, and "
             "the reason it exists. Cheetah Mobile's 2026-09-11 pre-open date is "
             "confirmed by its own PR Newswire release of 2026-09-04, so the EVENT "
             "is real; but the 'fits_cadence' verdict rests on the foreign private "
             "issuer 6-K text-matching defect, exactly the NIO / YSG failure mode. "
             "CMCM files no item 2.02, so the matcher takes any 6-K whose text "
             "resembles a results announcement, and the sweep rates the eight "
             "recorded reactions untrustworthy as an earnings base rate. "
             "'fits_cadence' would hand the name a 1.0 event multiplier its history "
             "has not earned. 'unknown' is the correct middle for 'the event exists "
             "but its history does not characterise it', and it does not bar the "
             "name from ranking. Correcting only CSBR and ZUMZ, which both score "
             "better for it, is how a scorer gets quietly tuned toward a result.",
             "https://www.morningstar.com/news/pr-newswire/20260904cn40886/cheetah-mobile-to-report-second-quarter-2026-financial-results-on-september-11-2026"),
}

# DELIBERATELY NOT AMENDED on 2026-09-10, and this is the judgement, not an
# oversight. The sweep confirmed all 17 of 17 names from company sources with zero
# phantoms, so nothing needs killing; three flagged names nevertheless keep their
# pessimistic verdict.
#   DSGX: carries cadence_implausible with verdict 'unknown', and the event IS
#         company-confirmed (GlobeNewswire 2026-08-04, Q2 FY2027 after the close
#         2026-09-10, call 5:30 p.m. ET) -- so the instinct is to upgrade. It stays
#         at 'unknown' for the DOO / PSNY / ZGN reason: Descartes is a foreign
#         private issuer, the 6-K text matcher caught non-earnings filings, and the
#         sweep rates the eight recorded reactions untrustworthy. Upgrading would
#         forgive a history defect and hand it a 1.0 multiplier it has not earned.
#   MNY:  identical case. MoneyHero's own 6-K exhibit on CIK 0001974044 announces
#         Q2 2026 pre-open on 2026-09-11 with an 8:00 a.m. EDT call, which is the
#         strongest kind of confirmation there is, and the cadence_implausible flag
#         is a matcher artefact. But the same matcher is what produced its eight
#         "reactions", the sweep rates them untrustworthy, and 'unknown' is what
#         that state actually is.
#   REF:  stays at 'unknown' on the OPPOSITE reasoning -- not a history defect but
#         thin confirmation. Reformation IPO'd on the NYSE on 2026-07-30 at $15 and
#         this is its first report as a public company, so history.n=0 is a fact
#         about the company rather than an artefact. The date comes from wire copy
#         dated 2026-08-27 mirrored on StockTitan and EDGAR CIK 0001787117 carries
#         NO 8-K naming it, so unlike CSBR and ZUMZ there is no filing behind the
#         confirmation. 'unknown' states exactly what is known. The cost is
#         cosmetic: only 'suspect' blocks rankability.
# The remaining 11 names are untouched -- all rated history-trustworthy by the
# sweep, all already at fits_cadence.
#
# Net effect of this pass: CSBR becomes rankable at a 1.0 event multiplier instead
# of being zeroed at 0.05, ZUMZ's records-bug thinness stops being scored as an
# event-existence doubt, and CMCM's FPI matcher history stops carrying a 1.0
# multiplier it had not earned. Per-name history warnings go to the hunters.
_RETIRED_2026_09_08 = {
    "YQ": ("unknown",
           "UPGRADE off 'suspect', which is the amendment that matters today: "
           "edge_score.py sets rankable=False on a suspect verdict and multiplies "
           "baseline_quality by 0.05, so 17 Education would have been "
           "arithmetically incapable of ranking anywhere despite a "
           "company-confirmed event. The event is real: the company's own "
           "GlobeNewswire release of 2026-09-02 states Q2 2026 unaudited results "
           "after the close of US markets on 2026-09-08 with a 9:00pm ET call. "
           "The 'suspect' verdict rests on a 5-day gap against a 78-day median, "
           "and that 5-day gap is the 2026-09-03 6-K announcing a US$10m share "
           "repurchase authorisation -- not an earnings print. As a foreign "
           "private issuer YQ files no item 2.02, so the text matcher takes "
           "buyback and corporate 6-Ks as prints. 'unknown' and NOT "
           "'fits_cadence': the sweep rated the reaction history untrustworthy "
           "for exactly the same reason, and the +74% 5-day / +42.5% 20-day "
           "run-up in the baseline's tape is the market reacting to that buyback "
           "6-K. Upgrading to fits_cadence would forgive a history defect and "
           "hand the name a 1.0 event multiplier it has not earned; the event is "
           "established, its recorded history simply does not characterise it.",
           "https://www.globenewswire.com/news-release/2026/09/02/3354907/0/en/17-education-technology-group-inc-to-report-second-quarter-2026-unaudited-financial-results-on-september-8-2026.html"),
    "SUNB": ("fits_cadence",
             "UPGRADE off 'unknown'. Sunbelt Rentals Holdings is a brand-new SEC "
             "registrant (CIK 0002083785) -- the former Ashtead Group, "
             "redomiciled and renamed, now dual-listed NYSE/LSE as SUNB -- so the "
             "baseline has only two prints on record and returned 'unknown' with "
             "no median_gap_days at all. That zero-cadence is a consequence of "
             "the registrant's age, NOT of the 6-K/text-matcher defect that keeps "
             "ODD, NNOX and CGNT at 'unknown' below: SUNB is a domestic filer, "
             "both recorded rows (2026-03-12 and 2026-06-23) are genuine 8-K item "
             "2.02 prints on exact acceptance times, and the sweep rated the "
             "history trustworthy. The event itself is confirmed with the hour by "
             "the company's own IR release: Q1 FY2027 results posted to IR before "
             "an 8:30am ET call on 2026-09-09. The thinness of two events stays "
             "recorded in baseline_quality (tier=partial, history_events=2), so "
             "correcting the event flag does not overstate the history.",
             "https://ir.sunbeltrentals.com/news-events/press-releases/detail/151/sunbelt-rentals-to-announce-first-quarter-fiscal-year-2027-results-on-september-9-2026"),
    "CRMT": ("suspect",
             "DOWNGRADE off 'fits_cadence', and it is here to keep this pass "
             "symmetric: two names gain and one loses. America's Car-Mart is the "
             "one name of 24 the sweep could NOT confirm. Car-Mart pre-announces "
             "every print with a GlobeNewswire 'Schedules ... Results and "
             "Conference Call' release 7-14 days ahead (Q4 FY2026: released "
             "2026-07-07 for a 2026-07-14 print), and as of 2026-09-08 no such "
             "release exists for Q1 FY2027 and EDGAR carries no scheduling 8-K. "
             "Vendors disagree with each other and with themselves -- MarketBeat "
             "carries 2026-09-09 bmo, others the same date amc, TipRanks "
             "2026-09-17 -- which is the classic signature of a vendor projection "
             "rather than a schedule. The 'fits_cadence' verdict rests on a "
             "57-day gap against a 91-day median (ratio 0.63), i.e. the baseline "
             "itself is describing a sub-quarterly gap and calling it a fit. "
             "'suspect' is the honest verdict: the cadence disagrees with the "
             "calendar and no company source names the date. CRMT is dropped from "
             "the hunt under budget.edge_degrade_order step 1, and this verdict is "
             "what makes that loss visible in edge-scores.json rather than silent.",
             "https://www.globenewswire.com/news-release/2026/07/07/3323618/0/en/america-s-car-mart-inc-schedules-fourth-quarter-fiscal-year-2026-results-and-conference-call.html"),
}

# DELIBERATELY NOT AMENDED on 2026-09-08, and this is the judgement, not an
# oversight. ODD, NNOX and CGNT all carry cadence_implausible with verdict
# 'unknown', and all three events are confirmed by the company's own press release
# WITH the hour -- so the instinct is to upgrade them to fits_cadence. They stay at
# 'unknown' (event_q 0.6) for the CAN/DLNG/GMHS reason: in every one the 6-K text
# matcher caught NON-EARNINGS filings, so the recorded reactions are not earnings
# base rates, and upgrading would forgive a history defect and hand each name a 1.0
# multiplier it has not earned. All three are Israeli foreign private issuers that
# file no item 2.02.
#   ODD:  8 filings at a 21-day median gap. ODDITY 6-Ks frequently; the two
#         reactions that are almost certainly real earnings are -49.21% on
#         2026-02-25 and -29.61% on 2026-06-02, and the option chain is pricing a
#         third leg at ~20.7% event-implied on a 3-day expiry. The other six rows
#         are not earnings and the 6.25% median is not an earnings base rate.
#   NNOX: 8 filings at a 6-day median gap -- the densest 6-K stream on the list.
#         The -44.0% on 2026-06-25 and -24.4% on 2026-04-20 are in there but so is
#         everything else Nanox announces. No quarterly reporter has a 6-day
#         cadence.
#   CGNT: 8 filings at a 13-day median gap, including a 1-day gap that produced the
#         'unknown'. The -20.57% on 2026-06-03 is probably the real Q1 FYE27
#         print; the rows dated 2026-09-01 and 2026-09-08 are the date-announcement
#         6-K and other corporate filings, not prints.
# JMKE is not amended because there is nothing to amend: Jersey Mike's IPO'd in
# 2026 and priced_in.py produced no baseline at all (28 usable bars, no options, no
# reaction history), so it has no verdict, no spot and no priced-in measurement.
# The event IS company-confirmed (2026-09-09, 8:30am ET call) and its hunt_priority
# is 79.4, but "is this already priced" is unanswerable for it, so it is dropped
# from the hunt as a visible loss rather than hunted against a baseline that does
# not exist.
# The remaining 19 names are untouched: all domestic, all on 8-K item 2.02
# acceptance times, all rated history-trustworthy by the sweep.
#
# Net effect of this pass: YQ becomes rankable at a 0.6 event multiplier instead of
# being zeroed at 0.05, SUNB's new-registrant thinness stops being scored as an
# event-existence doubt, and CRMT's unconfirmed row stops carrying a 1.0 multiplier
# it had not earned. Per-name history warnings go to the hunters instead.
_RETIRED_2026_09_04 = {
    "WDH": ("unknown",
            "Superseded by the 2026-09-07 entry above, which covers the same name "
            "over the same 2026-09-08 event and adds the duplicate-row defect. Kept "
            "only to record that the 2026-09-04 pass reached the same verdict from "
            "the same company source independently.",
            "https://en.prnasia.com/releases/global/waterdrop-inc-to-report-second-quarter-2026-financial-results-on-september-8-2026-545126.shtml"),
}

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
