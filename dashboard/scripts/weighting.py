#!/usr/bin/env python3
"""Pre-registered weightings of the edge-hunt score. Frozen 2026-09-18.

TWO SPECS LIVE HERE AND w2 IS THE ONE BEING CARRIED FORWARD.

    w1 / w1_filter   the first attempt: the factor multiplies the score, so it changes
                     which names clear the conviction floor. Superseded, kept frozen
                     and still computed, because deleting a spec after seeing it lose
                     is how a record stops being a record.
    w2               the operator's design: the floor stays the gate and the factors
                     set the SIZE. See the w2 block at the bottom of this file.

Everything below this line describes w1.

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
# date. A median recomputed on every rebuild would drift with the sample and
# quietly re-fit the spec without anyone editing it.
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


# =============================================================================
# w2 — THE FLOOR STAYS THE GATE; THE VARIABLES SET THE SIZE
# =============================================================================
"""
w1 let a tilt push a name over the conviction floor, and that is where it lost: the
four names it promoted returned -11.01% and the floor is the only rule in this repo
that ever cleared a family-wise correction. w2 takes the other road, on the operator's
instruction:

    SELECTION   unchanged. |impact_sum| >= conviction_floor, and nothing else.
                No tilt adds a name and no tilt removes one.
    SIZING      asymmetric. The four factors set a strength per name, strength sets
                a share of the gross budget, and a single name may take up to 50% of
                equity instead of the flat 33% the stage uses now.

So a wrong tilt can now cost size on a good name or buy size on a bad one, but it can
never buy a name the hunt did not conviction-rank in the first place. That is a smaller
surface for a rule chosen on 13 days.

WHAT THE HIGHER CAP COSTS, STATED PLAINLY. `config/pipeline.yaml` calls the per-name
cap the only risk control in the stage. Raising it from 33% to 50% means one print can
move the account by half the gap it opens: the 23% single-name gap that moved the
account 4.5% at a 20% cap and about 7.5% at 33% moves it about 11.5% at 50%. Nothing
else changed to offset that, and w2 is not switched on anywhere -- it is computed
beside the live rule so the two can be compared.

FOUR FACTORS, EACH -1 / 0 / +1, all four named by the operator:

    evidence      more findings behind the score
    retail        the consumer/retail character of the name
    lean_agree    the sealed price lean points the same way
    search_quiet  less search traffic into the print

`evidence` is in here on instruction and carries a caveat the others do not: H7 measured
`n_findings` on its own as `geen effect`. It is the one factor with no support behind it
in the register, and if w2 underperforms it is the first to drop.
"""
SPEC_W2 = {
    "version": "w2",
    "frozen": "2026-09-18",
    "gate": "|impact_sum| >= conviction_floor, unchanged",
    "g": 0.125,                    # strength -> weight slope; +-4 spans 0.5 .. 1.5
    "weight_clamp": [0.5, 1.5],
    "max_pct_per_name": 50.0,      # up from the live 33
    "gross_pct": 100.0,
    "note": "sizing only; no tilt adds or removes a name. Chosen on 13 days; "
            "only a forward sample tests it.",
}
G = SPEC_W2["g"]
W_LO, W_HI = SPEC_W2["weight_clamp"]
MAX_PCT = SPEC_W2["max_pct_per_name"]
GROSS_PCT = SPEC_W2["gross_pct"]

FINDINGS_MANY, FINDINGS_FEW = 4, 2


def strength(row):
    """The four factors, each -1 / 0 / +1. Missing input is 0, never a guess."""
    t = tilts(row)                      # lean_agree, search_quiet, retail  (sector drops)
    nf = row.get("n_findings")
    out = {
        "evidence": 0 if nf is None else (1 if nf >= FINDINGS_MANY
                                          else (-1 if nf <= FINDINGS_FEW else 0)),
        "retail": t["retail"],
        "lean_agree": t["lean_agree"],
        "search_quiet": t["search_quiet"],
    }
    return out


def weight(row):
    """Per-name relative weight before the budget is divided. Never negative."""
    st = strength(row)
    return max(W_LO, min(W_HI, 1 + G * sum(st.values()))), st


def allocate(rows, gross_pct=None, max_pct=None):
    """Shares of equity for one day's book, weighted and capped.

    Same shape as the live sizer -- a capped name's leftover is redistributed over the
    rest -- so the only differences from the live rule are WHICH weight each name gets
    and WHERE the cap sits. Returns {id: pct_of_equity}; the sum is the deployed gross,
    which is below `gross_pct` only when too few names can absorb it.
    """
    gross = GROSS_PCT if gross_pct is None else gross_pct
    cap = MAX_PCT if max_pct is None else max_pct
    if not rows:
        return {}
    ws = {id(r): weight(r)[0] for r in rows}
    share = {}
    live = list(rows)
    budget = gross
    # iterate: hand out pro rata, cap, redistribute what the cap refused
    for _ in range(len(rows) + 1):
        tot = sum(ws[id(r)] for r in live)
        if not live or tot <= 0 or budget <= 1e-9:
            break
        capped = []
        for r in live:
            want = budget * ws[id(r)] / tot
            if want >= cap - 1e-9:
                share[id(r)] = cap
                capped.append(r)
        if not capped:
            for r in live:
                share[id(r)] = budget * ws[id(r)] / tot
            break
        budget -= cap * len(capped)
        live = [r for r in live if id(r) not in {id(x) for x in capped}]
    return share


def equal_allocate(rows, gross_pct=100.0, max_pct=33.0):
    """The live rule: equal weight, whole budget, capped per name."""
    if not rows:
        return {}
    per = min(max_pct, gross_pct / len(rows))
    return {id(r): per for r in rows}


def attach_w2(names, floor):
    """`w2_strength` / `w2_weight` per name. Shares are per DAY, so they are computed
    where a day exists -- in the dashboard and in the day table below -- not here."""
    n = 0
    for r in names:
        imp = r.get("impact_sum")
        if imp is None:
            r["w2_weight"], r["w2_strength"] = None, {}
            continue
        w, st = weight(r)
        r["w2_weight"] = round(w, 4)
        r["w2_strength"] = st
        r["w2_in_book"] = bool(abs(imp) >= floor)     # the plain gate, unchanged
        n += 1
    return n
