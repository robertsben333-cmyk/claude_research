#!/usr/bin/env python3
"""A pre-registered weighting of the edge-hunt score. Frozen 2026-09-18.

WHAT THIS IS
------------
`impact_sum` ranks the day and its absolute value decides what gets bought. This
multiplies that score by a factor built from variables the hypothesis register found
something in, keeping the sign, so both the ranking AND the selection change:

    w_score = impact_sum * clamp(1 + K * sum(tilts), 0.5, 1.5)

It does NOT replace the live rule. `edge_score.py` is untouched and the book is still
placed on `impact_sum`. This runs beside it so the two can be compared on days that do
not exist yet.

WHY IT IS FROZEN, AND WHAT THAT COSTS
-------------------------------------
Every tilt below was chosen after looking at 13 days of outcomes. Scored on those same
13 days it will beat the plain rule, and that number is worth nothing -- it is the
definition of fitting. The only honest test is forward, which is why the spec carries a
freeze date and a version, and why NOTHING HERE MAY BE RE-TUNED. If a tilt turns out
wrong, the answer is `w2` with its own freeze date beside `w1`, not a quietly edited
constant. A constant that moves when the data moves is not a hypothesis.

ONE FREE PARAMETER, ON PURPOSE
------------------------------
K is the only magnitude in the spec and every tilt is +1, 0 or -1. Letting each tilt
carry its own fitted weight would be four more parameters fitted on 56 traded names,
which is how a weighting scheme memorises its sample. K = 0.15 means a name with every
tilt against it keeps half its score and a name with everything for it gains half.

WHAT IS DELIBERATELY LEFT OUT, AND WHY
--------------------------------------
  session          H1 came back `geen effect`. The exit split (H2a/H2b) leans, but that
                   is an exit rule, not a score: it belongs in `exit_mode`, not here.
  n_findings       H7, `geen effect`. It measures how much there was to write.
  dollar_vol       H8 leans, but acting on it means tilting TOWARD names the $200k
                   turnover floor and the borrow check then refuse. That is a capacity
                   trap, not an edge.
  realised_vol,
  retail_tilt as
  a size proxy     these rank how far the stock MOVED, not whether the hunt was right.
                   `retail_tilt` is in the spec for the accuracy split it showed on the
                   traded book, not for the move-size correlation.
"""
from datetime import date

SPEC = {
    "version": "w1",
    "frozen": "2026-09-18",
    "k": 0.15,
    "clamp": [0.5, 1.5],
    "basis": "13 resolved hunt days, 56 names above the conviction floor",
    "note": "chosen after seeing those days; only a forward sample tests it",
}

# TWO VARIANTS, BOTH FROZEN TODAY, BOTH CARRIED FORWARD.
#
#   w1          symmetric. The factor can pull a name over the floor as well as under it.
#   w1_filter   one-sided. The factor may only REMOVE a name from the book; a name the
#               plain floor rejected can never be promoted by a tilt.
#
# The second exists because of what the first did in sample, and the reasoning is worth
# keeping rather than hiding in a constant. Run symmetric over the 13 days: the names it
# DROPS were correctly dropped (+0.22% against +3.69% for the book), the names it KEEPS
# do better than the book (+4.27%), and the four names it PROMOTES return -11.01% --
# which is the whole of its underperformance. That is not surprising after the fact: the
# conviction floor is the only rule in this repo that ever cleared a family-wise
# correction, so a tilt chosen on 13 days overruling it is the weakest link in the chain
# doing the most consequential thing.
#
# Shipping both rather than picking the better one is the point. The one-sided variant
# was designed after seeing those four names, so choosing it on this sample would be the
# same fitting error one level up. Let the forward days choose.
VARIANTS = ("w1", "w1_filter")
K = SPEC["k"]
LO, HI = SPEC["clamp"]

# The retail-tilt split point, frozen at the median of the traded book on the freeze
# date. A median recomputed每 rebuild would move with the sample and quietly re-fit.
RETAIL_SPLIT = 50.0
SEARCH_SPLIT = 1.0
SECTOR_UP = {"Consumer Cyclical"}
SECTOR_DOWN = {"Technology"}


def tilts(row):
    """Each tilt is -1, 0 or +1. A missing input is 0, never a guess."""
    out = {}

    # H5, `steun`. The hunt earned most where the sealed baseline's own price lean
    # already pointed the same way. Uncomfortable for a stage whose premise is that
    # it finds what the price has missed, which is exactly why it is worth carrying
    # forward rather than explaining away.
    lean, imp = row.get("priced_lean_pct"), row.get("impact_sum")
    if lean is None or not imp:
        out["lean_agree"] = 0
    else:
        out["lean_agree"] = 1 if (lean > 0) == (imp > 0) else -1

    # H9, `steun` on the traded book. More search attention, worse outcome -- a print
    # everyone is already looking at is a print that has been chewed over.
    if row.get("search_state") != "measured" or row.get("search_spike") is None:
        out["search_quiet"] = 0
    else:
        out["search_quiet"] = 1 if row["search_spike"] < SEARCH_SPLIT else -1

    # H3, `mogelijk`. Retail-held names react to what a reader can find.
    rt = row.get("retail_tilt")
    out["retail"] = 0 if rt is None else (1 if rt >= RETAIL_SPLIT else -1)

    # H4, `mogelijk`, AND THE WEAKEST LINK IN THIS SPEC. With nine sectors the best one
    # is good by construction. It is included because the gap was large and the
    # mechanism has to be testable; it is the first tilt to drop if w1 underperforms.
    sec = row.get("sector")
    out["sector"] = 1 if sec in SECTOR_UP else (-1 if sec in SECTOR_DOWN else 0)
    return out


def factor(row):
    t = tilts(row)
    return max(LO, min(HI, 1 + K * sum(t.values()))), t


def weighted(row):
    """The re-weighted score, sign preserved. None when there is no score to weight."""
    imp = row.get("impact_sum")
    if imp is None:
        return None, 1.0, {}
    f, t = factor(row)
    return round(imp * f, 4), round(f, 4), t


def attach(names, floor):
    """Add the weighted score and BOTH variants' book membership to every row.

        w_score / w_conviction / w_factor / w_tilts   the re-weighted score
        w_above_floor                                 w1, symmetric
        wf_above_floor                                w1_filter, demote-only

    The plain rule is untouched and stays the one the book is placed on.
    """
    n = 0
    for r in names:
        ws, f, t = weighted(r)
        imp = r.get("impact_sum")
        plain_in = imp is not None and abs(imp) >= floor
        r["w_score"] = ws
        r["w_factor"] = f
        r["w_tilts"] = t
        r["w_conviction"] = None if ws is None else round(abs(ws), 4)
        r["w_above_floor"] = None if ws is None else bool(abs(ws) >= floor)
        # demote-only: must be in the plain book AND survive the re-weighting
        r["wf_above_floor"] = (None if ws is None
                               else bool(plain_in and abs(ws) >= floor))
        if ws is not None:
            n += 1
    return n


if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path
    led = Path(__file__).resolve().parents[2] / "dashboard" / "data" / "ledger.json"
    d = json.loads(led.read_text())
    floor = d.get("conviction_floor", 3.0)
    rows = [r for r in d["names"] if not r.get("duplicate_event")
            and r.get("mv_strategy") is not None and (r.get("impact_sum") or 0) != 0]
    attach(rows, floor)
    print(f"spec {SPEC['version']} frozen {SPEC['frozen']}  K={K}  clamp={LO}-{HI}")
    print(f"{len(rows)} scored names\n")

    def book(rs, key):
        v = [(r["mv_strategy"] if (r[key] or 0) > 0 else -r["mv_strategy"]) for r in rs]
        if not v:
            return None
        m = sum(v) / len(v)
        hits = sum(1 for x in v if x > 0)
        return len(v), hits, m

    plain = [r for r in rows if abs(r["impact_sum"]) >= floor]
    wgt = [r for r in rows if r["w_above_floor"]]
    wfl = [r for r in rows if r["wf_above_floor"]]
    for label, rs, key in (("plain      |impact_sum| >= floor", plain, "impact_sum"),
                           ("w1         |w_score| >= floor", wgt, "w_score"),
                           ("w1_filter  demote-only", wfl, "w_score")):
        n, h, m = book(rs, key)
        print(f"  {label:34s} n={n:3d}  raak {h}/{n} ({100*h/n:.0f}%)  {m:+.2f}% per naam")
    ins = {r["ticker"] + r["event_date"] for r in plain}
    outs = {r["ticker"] + r["event_date"] for r in wgt}
    print(f"\n  w1 selection: {len(outs - ins)} names enter the book, "
          f"{len(ins - outs)} leave")
    print(f"  w1_filter:    0 enter by construction, "
          f"{len(ins) - len(wfl)} leave")
    print("\n  IN SAMPLE AND THEREFORE WORTH NOTHING as evidence: every tilt was chosen")
    print("  after seeing these days. The forward comparison is the test.")
    sys.exit(0)
