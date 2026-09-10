#!/usr/bin/env python3
"""Eight pre-registered hypotheses about stage E, and the code that scores them.

Everything in `EDGE_ANALYSIS.md` was found by looking at the data that produced it.
That is how hypotheses are made, and it is not how they are tested. This file fixes
the tests **before** the data that will settle them exists, so that a year from now
nobody has to wonder whether the cut was chosen after the fact.

Each hypothesis carries: what it claims, why it might be true, the exact statistic,
the estimate it was born from (marked `discovery`, never evidence for itself), an
independent reading on the sealed corpus where one is available, and the rule that
decides it. Nothing here changes the hunter, the scorer or the book.

    python3 edge/scripts/edge_hypotheses.py                    # score all three samples
    python3 edge/scripts/edge_hypotheses.py --since 2026-09-11 # the forward test only
    python3 edge/scripts/edge_hypotheses.py --json edge/analysis/edge-hypotheses.json

## The three samples, and why they are not interchangeable

  DISCOVERY   `edge/ledger/` up to and including 2026-09-10. Every hypothesis below
              was read off it. Its numbers are stated so the forward test can be
              compared against something, and for no other purpose.
  CORPUS      `edge/ledger/corpus/`, built from `backtest/runs/edge-corpus/*` — 107
              resolved events whose hunters saw a sealed point-in-time capture and
              could not search past the print. Genuinely out of sample for anything
              read off the live runs. Its own limits are in `backtest/FINDINGS.md`
              §33: every event runs on the historical-reaction anchor because the
              option chain is unrecoverable retrospectively, 30 captures kept
              sweeping past the print, and hunters averaged 1.8 findings a name
              against 4.5 live — so a category that needs the open web is thin or
              absent there, and absence is not disconfirmation.
  FORWARD     everything from `--since` onward. Empty today. This is the test.

## Reading the verdicts

`pending` means not enough events yet, and the row says how many the test needs at
80% power. `supported` and `rejected` mean the decision rule fired. A hypothesis can
be `rejected` and still be worth knowing; the point of writing it down is that the
answer counts either way.
"""
import argparse
import csv
import json
import math
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import edge_evidence as E                                    # noqa: E402
from edge_calibration import within_day_perm, ols            # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "edge" / "ledger"
CORPUS = ROOT / "edge" / "ledger" / "corpus"
DISCOVERY_ENDS = "2026-09-10"


# ------------------------------------------------------------------ statistics

def binom_p(k, n):
    if not n:
        return None
    c = [math.comb(n, i) * 0.5 ** n for i in range(n + 1)]
    return round(min(1.0, sum(x for x in c if x <= c[k] * 1.0000001)), 4)


def events_for_power(true_rate, base=0.5, power=0.8, alpha=0.05, cap=2000):
    """How many events before a rate this far from `base` is detectable.

    Exact binomial, two-sided, computed rather than quoted: the answer is the
    difference between 'run it for a fortnight' and 'run it for a year', and it is
    the single most useful number for deciding whether a hypothesis is worth
    keeping on the list at all.
    """
    if true_rate == base:
        return None
    for n in range(5, cap + 1):
        crit = [k for k in range(n + 1) if binom_p(k, n) <= alpha]
        if not crit:
            continue
        pw = sum(math.comb(n, k) * true_rate ** k * (1 - true_rate) ** (n - k)
                 for k in crit)
        if pw >= power:
            return n
    return None


# ------------------------------------------------------------------ the samples

def sample(ledger, since=None, until=None):
    path = ledger / "findings.csv"
    if not path.exists():
        return None
    rows = [r for r in E.load(path)
            if (since is None or r["event_date"] >= since)
            and (until is None or r["event_date"] <= until)]
    if not rows:
        return None
    names = {}
    npath = ledger / "names.csv"
    if npath.exists():
        for r in csv.DictReader(open(npath, encoding="utf-8")):
            names[(r["ticker"], r["event_date"], r["session"])] = r
    leads = E.by_lead(rows)
    for lead in leads:
        n = names.get((lead["ticker"], lead["event_date"], lead["session"]), {})
        lead["key"] = float(n.get("impact_sum") or lead["name_impact_sum"] or 0)
        lead["implied"] = float(n["implied_move_pct"]) if n.get("implied_move_pct") else None
        lead["basis"] = n.get("implied_basis")
        lead["runup"] = float(n["runup_20d_pct"]) if n.get("runup_20d_pct") else None
        lead["ratio"] = abs(lead["key"]) / lead["implied"] if lead["implied"] else None
    return {"findings": rows, "leads": leads,
            "days": sorted({r["event_date"] for r in rows})}


# ------------------------------------------------------------------ the metrics

def rate_metric(rows, select, base_rows=None):
    sel = [r for r in rows if select(r)]
    if not sel:
        return {"n": 0}
    k = sum(r["ok"] for r in sel)
    out = {"n": len(sel), "right": k, "rate": round(k / len(sel), 3),
           "binom_p": binom_p(k, len(sel))}
    if base_rows:
        b = [r for r in base_rows]
        out["sample_base_rate"] = round(st.fmean(r["ok"] for r in b), 3) if b else None
        if out["sample_base_rate"] is not None:
            out["lift_vs_base"] = round(out["rate"] - out["sample_base_rate"], 3)
    return out


def rank_metric(rows, xf, yf=lambda r: r["ok"], need=(lambda r: True)):
    sel = [r for r in rows if need(r)]
    rho, p, n = within_day_perm(sel, xf, yf)
    return {"spearman": rho, "perm_p": p, "n": n}


def slope_metric(leads):
    xs = [r["key"] for r in leads]
    ys = [r["move"] for r in leads]
    f = ols(xs, ys) or {}
    return {k: f.get(k) for k in ("slope", "slope_t", "r2", "n")}


# ------------------------------------------------------------------ the registry

HYPOTHESES = [
    {
        "id": "H1-series-bridge",
        "claim": "A finding that rests on a third-party series the hunter connects "
                 "to the company by its own reasoning is right less than half the "
                 "time — worse than a coin, not merely unhelpful.",
        "mechanism": "A public series is available to everyone and says nothing "
                     "about one company until someone supplies the bridge. The "
                     "bridge is the hunter's, untested, and it feels like insight "
                     "precisely because it was built rather than found.",
        "scope": "findings",
        "metric": ("rate", lambda r: r["bridge"]),
        "decides": "Rejected if 25+ bridged findings accumulate at or above 50%. "
                   "Supported at 25+ below 40%.",
        "target_rate": 0.30,
        "caveat": "The hunter was instructed against this on 2026-09-10, so the "
                  "forward sample is deliberately starved. That was the right call "
                  "for the book and it costs the experiment; if the category "
                  "disappears entirely the hypothesis simply stops being testable, "
                  "and the instruction stands on the discovery sample alone.",
    },
    {
        "id": "H2-filing-lead",
        "claim": "A call led by a statutory filing beats the sample's own base rate "
                 "by at least 10 points.",
        "mechanism": "The company had to file it, so it is complete and dull; being "
                     "dull is what leaves it unread. Nothing in a 10-Q is news, "
                     "which is exactly why the price may not hold it.",
        "scope": "leads",
        "metric": ("rate", lambda r: r["src"] == "filing"),
        "decides": "Supported at 60+ filing-led calls with a lift above +0.10 and "
                   "a binomial p under 0.05. Rejected if the lift is under +0.02.",
        "target_rate": 0.65,
    },
    {
        "id": "H3-aggregator-lead",
        "claim": "A call led by an aggregator page — Yahoo, MarketBeat, "
                 "stockanalysis, Investing.com — is below the base rate.",
        "mechanism": "An aggregator restates someone else's number. Anything "
                     "reachable there has been reachable to everyone for as long as "
                     "the page has existed, so it is the least likely place for "
                     "something unpriced to sit.",
        "scope": "leads",
        "metric": ("rate", lambda r: r["src"] == "aggregator"),
        "decides": "Supported at 40+ aggregator-led calls below 40%. Rejected at or "
                   "above the base rate.",
        "target_rate": 0.30,
    },
    {
        "id": "H4-old-beats-fresh",
        "claim": "A lead finding whose source is more than 60 days old beats one "
                 "under 3 days old.",
        "mechanism": "The stage's own premise. Yesterday's wire is in the price by "
                     "construction; page 47 of a June filing may never have been "
                     "read by anyone who trades the name.",
        "scope": "leads",
        "metric": ("split", lambda r: E.age_bucket(r["age"]) == ">60d",
                   lambda r: E.age_bucket(r["age"]) == "<=3d"),
        "decides": "Supported when both arms exceed 40 events and the gap holds "
                   "above +0.10. Rejected if the gap turns negative at that size.",
        "target_rate": 0.60,
    },
    {
        "id": "H5-conviction-over-implied",
        "claim": "Conviction divided by the implied move ranks the sign better than "
                 "raw conviction AND better than the implied move on its own. The "
                 "second half is the whole hypothesis: without it the result is free.",
        "mechanism": "Three points of edge on a name the market has priced to move "
                     "4% is a large claim; the same three points on a name priced to "
                     "move 18% is noise. The raw key cannot tell those apart, and "
                     "the ranking is run within a day across names of very different "
                     "volatility. BUT a quiet name is easier to call for reasons that "
                     "have nothing to do with the hunt, so `1/implied` has to be "
                     "beaten, not merely mentioned — it was added as a control after "
                     "the first version of this hypothesis looked strong, and it "
                     "immediately explained most of the effect.",
        "scope": "leads",
        "metric": ("rank_pair",
                   lambda r: r["ratio"], lambda r: abs(r["key"]),
                   lambda r: r["ratio"] is not None),
        "decides": "Supported when 120+ anchored events give the ratio a "
                   "correlation above BOTH the raw key and `1/implied`, by at least "
                   "0.08 over the latter. Rejected if `1/implied` matches it — which "
                   "is what both current samples say, so this starts life leaning "
                   "rejected. Straddle-anchored names are reported separately; the "
                   "corpus anchor is 100% history proxy, so there `1/implied` is a "
                   "pure volatility ranking.",
        "target_rate": 0.65,
    },
    {
        "id": "H6-conviction-gate",
        "claim": "The gate the book is placed on — |impact_sum| at or above the "
                 "conviction floor of 3 — is right more than half the time.",
        "mechanism": "A hunter that found something says so with a bigger number. "
                     "The claim is only that the size orders the confidence, which "
                     "is all H8 leaves standing.",
        "scope": "leads",
        "metric": ("rate", lambda r: abs(r["key"]) >= 3.0),
        "decides": "Supported at 50+ gated events above 50% with p under 0.05. "
                   "Rejected at 50+ events at or below 50%. This is the one the "
                   "money rides on, so it is also the one to stop on.",
        "target_rate": 0.68,
    },
    {
        "id": "H7-beats-the-free-control",
        "claim": "Where the hunt and minus-the-20-day-run-up point in opposite "
                 "directions, the hunt is right more often than the control.",
        "mechanism": "The control is the thing to beat and it costs nothing. If the "
                     "hunt only agrees with it, the hunt is an expensive way to read "
                     "a price chart. The disagreements are the entire question.",
        "scope": "leads",
        "metric": ("head_to_head",),
        "decides": "Supported at 60+ disagreements where the hunt leads by 10 points "
                   "or more. Rejected if the control leads at that size.",
        "target_rate": 0.62,
    },
    {
        "id": "H9-quiet-names-are-callable",
        "claim": "A free number available before any subagent is spawned — minus the "
                 "implied move, i.e. prefer the quiet names — predicts whether the "
                 "day's calls come out right.",
        "mechanism": "A name the market has priced to move 4% has less room to "
                     "surprise in either direction than one priced to move 18%, so "
                     "whatever lean exists is likelier to survive the print. If this "
                     "holds it is not an edge; it is a reason to distrust every "
                     "accuracy number that has not been conditioned on it.",
        "scope": "leads",
        "metric": ("rank_pair",
                   lambda r: -r["implied"], lambda r: abs(r["key"]),
                   lambda r: r["implied"] is not None),
        "decides": "Supported at 120+ anchored events with a correlation clear of "
                   "zero. If supported, every rate in H2, H3, H4 and H6 has to be "
                   "re-read conditioned on it before any of them means anything.",
        "target_rate": 0.62,
    },
    {
        "id": "H8-magnitude-is-noise",
        "claim": "The NULL, asserted rather than hoped for: the regression of the "
                 "realised move on impact_sum has a slope indistinguishable from "
                 "zero. The number orders; it does not measure.",
        "mechanism": "Sizes are elicited from a model with no feedback loop and no "
                     "units it has ever been scored on. There is no reason for them "
                     "to be calibrated and, on 68 events, they are not.",
        "scope": "leads",
        "metric": ("slope",),
        "decides": "This one is REJECTED — meaning the number does carry magnitude — "
                   "if 150+ events give a slope whose t exceeds 2 and whose sign is "
                   "positive. Until then the number must not size a position.",
        "target_rate": None,
    },
]

DISCOVERY_NOTE = {
    "H1-series-bridge": "3/15 findings, 1/8 as lead (live, p=0.035)",
    "H2-filing-lead": "15/22 = 0.682 against a 0.537 base (live)",
    "H3-aggregator-lead": "2/4 live and 1/8 corpus; pooled 3/12",
    "H4-old-beats-fresh": "0.586 vs 0.400 live; 0.588 vs 0.455 corpus",
    "H5-conviction-over-implied": "rho 0.273 vs 0.209 raw, 62 anchored events",
    "H6-conviction-gate": "24/35 live all-hunters, 17/24 single-hunted, 16/28 corpus",
    "H7-beats-the-free-control": "15/24 against 9/24 on the disagreements (live)",
    "H8-magnitude-is-noise": "slope -0.021, t=-0.09, R2=0.000 over 68 events",
    "H9-quiet-names-are-callable": ("rho 0.227 (p=0.117) live, 0.264 (p=0.020) "
                                    "corpus — found while controlling H5"),
}


def score(h, s):
    if s is None:
        return {"n": 0, "note": "no events in this sample"}
    leads, findings = s["leads"], s["findings"]
    m = h["metric"]
    kind = m[0]
    if kind == "rate":
        rows = findings if h["scope"] == "findings" else leads
        return rate_metric(rows, m[1], base_rows=rows)
    if kind == "split":
        rows = leads
        a, b = rate_metric(rows, m[1], rows), rate_metric(rows, m[2], rows)
        gap = (round(a["rate"] - b["rate"], 3)
               if a.get("rate") is not None and b.get("rate") is not None else None)
        return {"old": a, "fresh": b, "gap": gap}
    if kind == "rank_pair":
        anchored = [r for r in leads if m[3](r)]
        out = {"n_anchored": len(anchored),
               "ratio": rank_metric(anchored, m[1]),
               "raw": rank_metric(anchored, m[2]),
               # The control that decides it. A quiet name is easier to call whether
               # or not anybody hunted it.
               "one_over_implied": rank_metric(anchored, lambda r: -r["implied"]),
               "neg_run_up": rank_metric(
                   anchored, lambda r: -(r["runup"] or 0.0))}
        strad = [r for r in anchored if r["basis"] == "straddle"]
        if len(strad) >= 5:
            out["straddle_only"] = {"n": len(strad),
                                    "ratio": rank_metric(strad, m[1]),
                                    "raw": rank_metric(strad, m[2])}
        return out
    if kind == "head_to_head":
        dis = [r for r in leads if r["runup"] is not None
               and (r["key"] > 0) != (-r["runup"] > 0)]
        if not dis:
            return {"n": 0}
        hunt = sum(r["ok"] for r in dis)
        ctrl = sum(int((-r["runup"] > 0) == (r["move"] > 0)) for r in dis)
        return {"n": len(dis), "hunt": hunt, "control": ctrl,
                "hunt_rate": round(hunt / len(dis), 3),
                "control_rate": round(ctrl / len(dis), 3),
                "binom_p": binom_p(hunt, len(dis))}
    if kind == "slope":
        return slope_metric(leads)
    return {}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", default=None,
                    help=f"first FORWARD day (default: the day after {DISCOVERY_ENDS})")
    ap.add_argument("--json")
    a = ap.parse_args()

    since = a.since or "2026-09-11"
    samples = {
        "discovery": sample(LIVE, until=DISCOVERY_ENDS),
        "corpus_out_of_sample": sample(CORPUS),
        "forward": sample(LIVE, since=since),
    }
    doc = {"discovery_ends": DISCOVERY_ENDS, "forward_starts": since,
           "samples": {k: ({"events": len(v["leads"]), "findings": len(v["findings"]),
                            "days": len(v["days"])} if v else {"events": 0})
                       for k, v in samples.items()},
           "hypotheses": []}
    for h in HYPOTHESES:
        row = {"id": h["id"], "claim": h["claim"], "mechanism": h["mechanism"],
               "decides": h["decides"],
               "discovery_estimate": DISCOVERY_NOTE.get(h["id"]),
               "events_needed_for_80pct_power": (
                   events_for_power(h["target_rate"]) if h.get("target_rate") else None),
               "results": {k: score(h, v) for k, v in samples.items()}}
        if h.get("caveat"):
            row["caveat"] = h["caveat"]
        doc["hypotheses"].append(row)

    print(json.dumps(doc, indent=2))
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(doc, indent=2))
    fwd = samples["forward"]
    if not fwd:
        print(f"\nFORWARD SAMPLE IS EMPTY. Nothing is decided until runs from "
              f"{since} resolve.", file=sys.stderr)


if __name__ == "__main__":
    main()
