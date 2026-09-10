#!/usr/bin/env python3
"""What KIND of information did the right calls rest on, and what did the wrong ones?

This is not a scorecard for the stage. `edge_calibration.py` asks whether the number
is any good. This asks the question you would ask to make the *hunter* better: of the
things it found, which sorts of thing were worth finding.

The unit is a finding. Its attributes are what the hunter wrote and what can be read
off the source for free -- what kind of document it came from, how old it was on the
day of the print, whether anything independent corroborated it, how wide the hunter's
own uncertainty band was, and how much of its company's call it carried.

    python3 edge/scripts/edge_evidence.py
    python3 edge/scripts/edge_evidence.py --json edge/analysis/edge-evidence.json
    python3 edge/scripts/edge_evidence.py --examples     # the biggest hits and misses

## Three views, because attribution is the whole difficulty

You observe one move per company and a name carries three to eight findings. So no
row can be scored on its own. The three views trade coverage against cleanliness:

  ALL           every resolved finding, its name's outcome attached, additionally
                weighted by `share_of_impact`. Most data, weakest attribution
  DECISIVE      only findings that were at least half of their name's key. When one
                finding carried the call, its name's outcome IS its outcome
  BY LEAD       one row per company, classified by the SINGLE LARGEST finding behind
                it. This is the "what did we mostly bet on" view and the one to read
                first, because the unit and the outcome finally match

A category that looks good in ALL and bad in BY LEAD is a category that shows up as
supporting detail on names that were called from something else.

## The one cut that separates: a series bridged to the company

Fourteen of the 303 resolved findings rest on a **third-party series** -- an EIA diesel
price, a BLS airline-fare CPI, a NOAA temperature record, a Semrush traffic estimate, a
count of federal contract actions -- which the hunter then connects to this company's
quarter **by its own reasoning**. Those fourteen were right **2 times out of 14** (14%,
binomial p = 0.013), across 11 distinct companies and 5 days, and they are not small:
median size 2.38 points against 1.40 for everything else. Everything else was right 167
of 289 (58%).

The mechanism is legible, which is why it is worth acting on rather than filing as a
coincidence. A public series is available to everyone and says nothing about this
company until someone supplies the bridge. The bridge is the hunter's own inference,
it is untested, and it is exactly the sort of argument that feels like proprietary
insight while resting on the weakest link in the chain. NAVN carried two of them on one
theme (+3.0 and +1.5 off the same airline-fare CPI) and fell 21.9%.

This category was found by looking, on 67 names, after several other cuts were tried.
Treat it as a hypothesis with a mechanism, not a result -- it is written into
`.claude/agents/unpriced-hunter.md` so that the next months of runs test it.

## What the source classes mean

  filing        SEC/EDGAR and other statutory registers. The company had to say it
  company_pr    the company's own wire release or IR page. It chose to say it
  regulator     a non-filing government or agency source: tariff dockets, BLS, courts
  trade         industry bodies, trade press, specialist data nobody aggregates
  media         general financial press and market-commentary sites
  aggregator    Yahoo/MarketBeat/stockanalysis-type pages that restate someone else
  social        forums and retail chatter
  none          no URL

`independence` is recorded as corroborated only when the hunter actually put a URL in
it. It says "none" 21 times out of 399, and the free-text "corroborated" answers are
not evidence of anything until that field is checked against its own content.
"""
import argparse
import csv
import json
import math
import re
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "edge" / "ledger"

FILING = {"sec.gov", "data.sec.gov", "efts.sec.gov", "sedar.com", "sedarplus.ca",
          "find-and-update.company-information.service.gov.uk", "hkexnews.hk"}
PR = {"globenewswire.com", "prnewswire.com", "businesswire.com", "stocktitan.net",
      "accesswire.com", "newsfilecorp.com"}
AGG = {"stockanalysis.com", "finance.yahoo.com", "marketbeat.com", "investing.com",
       "tipranks.com", "benzinga.com", "dailypolitical.com", "nasdaq.com",
       "wallstreetzen.com", "gurufocus.com", "barchart.com", "zacks.com"}
MEDIA = {"fool.com", "theglobeandmail.com", "reuters.com", "bloomberg.com",
         "cnbc.com", "wsj.com", "ft.com", "seekingalpha.com", "barrons.com",
         "aljazeera.com", "forbes.com", "businessinsider.com", "cnevpost.com",
         "eeo.com.cn", "cfodive.com", "techcrunch.com", "theinformation.com"}
SOCIAL = {"reddit.com", "twitter.com", "x.com", "stocktwits.com", "youtube.com"}
GOVISH = re.compile(r"(^|\.)(gov|gov\.uk|europa\.eu|govinfo\.gov)$")

# A third-party series -- a price index, a weather record, a traffic estimate, a
# government statistic -- that the hunter connects to this company's quarter by its
# own reasoning. The connection is the hunter's, not the company's, and that is what
# distinguishes it from a company disclosure that happens to mention fuel costs.
SERIES = re.compile(
    r"\b(CPI|PPI|EIA|BLS|NOAA|FRED|diesel|fuel price|weather|temperature|"
    r"commodity price|registrations|foot traffic|web traffic|app downloads?|"
    r"job postings?|contract actions|FPDS|semrush|similarweb|indexbox)\b", re.I)


def bridges_a_series(finding, why_not_priced, src_class):
    """Does this finding rest on a third-party series bridged to the company?"""
    return bool(SERIES.search(f"{finding or ''} {why_not_priced or ''}")) \
        or src_class == "regulator"


def source_class(domain):
    d = (domain or "").lower()
    if not d:
        return "none"
    if d in FILING:
        return "filing"
    if d in PR:
        return "company_pr"
    if d in AGG:
        return "aggregator"
    if d in MEDIA:
        return "media"
    if d in SOCIAL:
        return "social"
    if GOVISH.search(d) or d.endswith(".gov"):
        return "regulator"
    if d == "AGGREGATOR":
        return "aggregator"
    return "trade"


def age_bucket(d):
    if d is None:
        return "unknown"
    if d < 0:
        return "future_dated"
    return "<=3d" if d <= 3 else ("4-14d" if d <= 14 else
                                  ("15-60d" if d <= 60 else ">60d"))


def size_bucket(a):
    return "<1pt" if a < 1 else ("1-3pt" if a < 3 else ("3-6pt" if a < 6 else ">=6pt"))


def band_bucket(w, size):
    if w is None or not size:
        return "no_band"
    r = w / abs(size)
    return "tight(<1x)" if r < 1 else ("2x" if r < 2.5 else "wide(>2.5x)")


def load(path=LEDGER / "findings.csv"):
    """Resolved findings, one hunt per event.

    ABM, UNFI, WDH, CAN and GMHS were hunted on both 09-04 and 09-07 for the same
    09-08 prints. Keeping both would count one outcome twice and weight those five
    events double in every table here, so the later hunt of an event is dropped
    wholesale -- the earlier one is kept, as `edge_direction.py` does.
    """
    raw = [r for r in csv.DictReader(open(path, encoding="utf-8"))
           if r["resolved"] == "1" and r["sign_agreed"] != ""]
    first_run = {}
    for r in raw:
        ev = (r["ticker"], r["event_date"], r["session"])
        if ev not in first_run or r["run_date"] < first_run[ev]:
            first_run[ev] = r["run_date"]
    out = []
    for r in raw:
        ev = (r["ticker"], r["event_date"], r["session"])
        if r["run_date"] != first_run[ev]:
            continue
        f = dict(r)
        f["imp"] = float(r["expected_impact_pct"] or 0)
        f["absimp"] = abs(f["imp"])
        f["share"] = float(r["share_of_impact"] or 0)
        f["ok"] = int(r["sign_agreed"])
        f["move"] = float(r["move_pct"])
        f["age"] = int(r["source_age_days"]) if r["source_age_days"] else None
        f["band"] = float(r["band_width_pct"]) if r["band_width_pct"] else None
        f["src"] = source_class(r["source_domain"])
        f["corrob"] = bool(re.search(r"https?://", r["independence"] or ""))
        f["bridge"] = bridges_a_series(r["finding"], r["why_not_priced"], f["src"])
        out.append(f)
    return out


def binom_p(k, n):
    if not n:
        return None
    c = [math.comb(n, i) * 0.5 ** n for i in range(n + 1)]
    return round(min(1.0, sum(x for x in c if x <= c[k] * 1.0000001)), 4)


def tabulate(rows, keyf, min_n=4):
    g = defaultdict(list)
    for r in rows:
        g[keyf(r)].append(r)
    out = {}
    for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
        if len(v) < min_n:
            continue
        w = sum(x["share"] for x in v)
        out[k] = {
            "n": len(v),
            "names": len({(x["event_date"], x["ticker"]) for x in v}),
            "right": round(st.fmean(x["ok"] for x in v), 3),
            "right_weighted": (round(sum(x["share"] * x["ok"] for x in v) / w, 3)
                               if w else None),
            "binom_p": binom_p(sum(x["ok"] for x in v), len(v)),
            "median_size": round(st.median(x["absimp"] for x in v), 2),
            "median_move": round(st.median(abs(x["move"]) for x in v), 2),
        }
    return out


def by_lead(rows):
    """One row per company, classified by the single largest finding behind it."""
    names = defaultdict(list)
    for r in rows:
        names[(r["event_date"], r["ticker"])].append(r)
    leads = []
    for _, v in names.items():
        lead = max(v, key=lambda x: x["absimp"])
        lead = dict(lead)
        lead["lead_share"] = lead["share"]
        lead["n_findings_name"] = len(v)
        leads.append(lead)
    return leads


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json")
    ap.add_argument("--examples", action="store_true")
    a = ap.parse_args()

    rows = load()
    decisive = [r for r in rows if r["share"] >= 0.5]
    leads = by_lead(rows)

    dims = {
        "source_class": lambda r: r["src"],
        "source_age": lambda r: age_bucket(r["age"]),
        "corroborated_with_url": lambda r: "yes" if r["corrob"] else "no",
        "finding_size": lambda r: size_bucket(r["absimp"]),
        "band_width_vs_size": lambda r: band_bucket(r["band"], r["imp"]),
        "direction_of_finding": lambda r: "up" if r["imp"] > 0 else "down",
        # The one cut that separates cleanly. See the docstring section below.
        "third_party_series_bridge": lambda r: "yes" if r["bridge"] else "no",
    }
    doc = {
        "counts": {"findings": len(rows), "decisive_findings": len(decisive),
                   "names": len(leads),
                   "days": len({r["event_date"] for r in rows})},
        "all_findings": {k: tabulate(rows, f) for k, f in dims.items()},
        "decisive_findings": {k: tabulate(decisive, f, min_n=3)
                              for k, f in dims.items()},
        "by_lead_finding": {k: tabulate(leads, f, min_n=3) for k, f in dims.items()},
        "reading": (
            "`right` is whether the NAME moved the way the finding pointed. In "
            "all_findings that is shared by every finding of a name; in "
            "by_lead_finding the unit and the outcome match. Compare the two."),
    }

    if a.examples:
        s = sorted(leads, key=lambda r: -r["absimp"])
        doc["examples"] = {
            "largest_calls": [
                {"ticker": r["ticker"], "date": r["event_date"], "right": r["ok"],
                 "size": r["imp"], "move": r["move"], "src": r["src"],
                 "age_days": r["age"], "share": round(r["share"], 2),
                 "finding": (r["finding"] or "")[:400]}
                for r in s[:12]],
        }

    print(json.dumps(doc, indent=2))
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(doc, indent=2))


if __name__ == "__main__":
    main()
