#!/usr/bin/env python3
"""Phase 0's answer: does a big one-day faller bounce, continue, or do neither?

Reads what rev_harvest.py collected and asks the only questions worth asking before
a single agent is spawned:

  1. base rates       what the worst K names of a day do over seven horizons, gross
  2. net of cost      the same, minus an estimated round-trip spread. This is the
                      table that decides whether the stage can exist, because the
                      screen selects on a realised extreme move and extreme movers
                      are thin. A reversal edge smaller than the spread is not an edge
  3. cuts             by size of drop, by turnover, by price, by how much of the drop
                      was the overnight gap, by volume spike, by sector
  4. free rankers     within-day rank correlation against the forward return for every
                      variable available for nothing, with a within-day permutation p
                      and a max-statistic family-wise correction over the whole family.
                      A hunt that cannot beat these has established nothing, which is
                      the lesson stage E paid thirteen days to learn
  5. the book         long the worst K equally each day and hold one session, plus the
                      short side, priced per day with days as the unit

EVERY NUMBER IN HERE CARRIES TWO BIASES AND BOTH FAVOUR REVERSAL
----------------------------------------------------------------
Survivorship: the universe is today's listings, so a name that dropped 40% and then
delisted is absent. That removes the worst continuations only.
Spread: Corwin-Schultz is a floor on the real cost and is estimated from the days
BEFORE the drop, so it does not see the widening the drop itself causes.
A reversal result that survives both is interesting. One that needs either of them
to be ignored is not.

    python3 researcher_reversal/scripts/rev_backtest.py --drops <dir> --k 15
"""
import argparse
import gzip
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rev_market as M                                            # noqa: E402

REPO = Path(__file__).resolve().parents[2]
HORIZONS = ["open1", "d1", "d2", "d3", "d5", "d10", "d21"]
HEADLINE = "d1"

# Every variable that costs nothing: no agent, no search, no judgement. The hunt has
# to beat the best of these AFTER the correction below, not the average of them.
RANKERS = [
    ("neg_ret_d", lambda r: -r["ret_d_pct"], "how far it fell (the reversal control)"),
    ("ret_d", lambda r: r["ret_d_pct"], "continuation control"),
    ("dv_med20", lambda r: r["dv_med20"], "how much it normally trades"),
    ("price", lambda r: r["price"], "price level"),
    ("vol_spike", lambda r: r["vol_spike"], "volume against its own 20-day median"),
    ("gap_share", lambda r: r["gap_share"], "share of the drop that was the gap"),
    ("gap_pct", lambda r: r["gap_pct"], "the overnight gap itself"),
    ("intraday_pct", lambda r: r["intraday_pct"], "the intraday leg itself"),
    ("neg_runup_20d", lambda r: -(r["runup_20d_pct"] or 0), "minus the 20-day run-up"),
    ("runup_5d", lambda r: r["runup_5d_pct"], "the 5-day run-up"),
    ("pos_52w", lambda r: r["pos_52w"], "position in the 52-week range"),
    ("atr14", lambda r: r["atr14_pct"], "its own realised volatility"),
    ("neg_half_spread", lambda r: -(r["half_spread_pct"] or 0), "minus the spread"),
]


# ------------------------------------------------------------------- loading
def load(drops_dir, ret_max, dv_min, px_min):
    rows = []
    with gzip.open(Path(drops_dir) / "drops.jsonl.gz", "rt") as fh:
        for line in fh:
            r = json.loads(line)
            if (r["ret_d_pct"] <= ret_max and r["dv_med20"] >= dv_min
                    and r["price"] >= px_min and r.get("fwd_" + HEADLINE) is not None):
                rows.append(r)
    return rows


def market(rg="3y"):
    """SPY forward returns by date, so every result can also be shown market-excess."""
    b = M.bars("SPY", rg=rg)
    idx = {x["date"]: i for i, x in enumerate(b)}
    out = {}
    for d, i in idx.items():
        e = {}
        for key, field, k in (("open1", "open", 1), ("d1", "close", 1),
                              ("d2", "close", 2), ("d3", "close", 3),
                              ("d5", "close", 5), ("d10", "close", 10),
                              ("d21", "close", 21)):
            j = i + k
            e[key] = (round((b[j][field] / b[i]["close"] - 1) * 100, 4)
                      if j < len(b) else None)
        out[d] = e
    return out


def select(rows, k):
    """The worst k names of each session. The screen, and nothing else."""
    by_day = defaultdict(list)
    for r in rows:
        by_day[r["date"]].append(r)
    out = {}
    for d, rs in by_day.items():
        rs.sort(key=lambda r: r["ret_d_pct"])
        out[d] = rs[:k]
    return dict(sorted(out.items()))


# ------------------------------------------------------------------ reporting
def describe(vals, label=""):
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"label": label, "n": 0}
    lo, hi = M.bootstrap_ci(vals)
    up = sum(1 for v in vals if v > 0)
    return {
        "label": label, "n": len(vals),
        "mean_pct": round(M.mean(vals), 3),
        "median_pct": round(statistics.median(vals), 3),
        "up_rate_pct": round(100 * up / len(vals), 1),
        "sign_p": M.sign_test_p(up, len(vals)),
        "t": M.tstat(vals),
        "ci95": [lo, hi],
    }


def band(rows, fn, edges, labels, horizon, excess=None):
    out = []
    for i, lab in enumerate(labels):
        lo = edges[i]
        hi = edges[i + 1] if i + 1 < len(edges) else None
        sub = [r for r in rows
               if fn(r) is not None and fn(r) >= lo and (hi is None or fn(r) < hi)]
        d = describe([_fwd(r, horizon, excess) for r in sub], lab)
        d["median_drop_pct"] = (round(statistics.median([r["ret_d_pct"] for r in sub]), 2)
                                if sub else None)
        d["median_half_spread_pct"] = (M.median([r["half_spread_pct"] for r in sub])
                                       if sub else None)
        out.append(d)
    return out


def _fwd(r, horizon, excess=None):
    v = r.get("fwd_" + horizon)
    if v is None:
        return None
    if excess is not None:
        m = (excess.get(r["date"]) or {}).get(horizon)
        if m is None:
            return None
        return round(v - m, 4)
    return v


def net_of_cost(rows, horizon, mult, excess=None, side=+1):
    """Gross return minus a round trip at `mult` times the estimated half-spread.

    Two half-spreads: one in, one out. `mult=1` prices the estimate as if it were
    right, `mult=2` as if the real cost is twice the estimate, which for a name that
    has just fallen 30% is the conservative reading rather than the pessimistic one.
    """
    out = []
    for r in rows:
        g = _fwd(r, horizon, excess)
        hs = r.get("half_spread_pct")
        if g is None or hs is None:
            continue
        out.append(side * g - 2 * mult * hs)
    return out


def rankers(sel, horizon, excess, reps):
    """Every free variable, ranked within day against the forward return."""
    res = []
    for name, fn, why in RANKERS:
        groups = []
        for d, rs in sel.items():
            g = [(fn(r), _fwd(r, horizon, excess)) for r in rs]
            g = [(a, b) for a, b in g if a is not None and b is not None]
            if len(g) >= 3:
                groups.append(g)
        rho, p = M.permutation_p(groups, None, None, reps=reps)
        res.append({"ranker": name, "what": why, "rho": rho, "perm_p": p,
                    "days": len(groups)})
    res.sort(key=lambda x: -(abs(x["rho"]) if x["rho"] is not None else 0))
    return res


def family_wise(sel, horizon, excess, reps, seed=3):
    """Max-statistic correction over the whole ranker family.

    The best of thirteen candidates is not a p-value. Under the null the statistic to
    beat is the LARGEST |rho| ANY of the thirteen reaches on the same shuffled data, so
    that is what each shuffle records. Same construction as the repo's own
    thirteen-candidate correction in researcher_us/EDGE_ANALYSIS.md.

    ONE SHUFFLE PER DAY, SHARED BY EVERY CANDIDATE. Shuffling separately per candidate
    would break the correlation between them and make the correction too lenient
    precisely where the candidates are near-duplicates, which here they are: gap_pct,
    gap_share and intraday_pct are three views of one decomposition.
    """
    import random
    rng = random.Random(seed)
    names = [n for n, _, _ in RANKERS]
    xs = {n: [] for n in names}
    ys, spans = [], []
    for d, rs in sorted(sel.items()):
        y = [_fwd(r, horizon, excess) for r in rs]
        keep = [i for i, v in enumerate(y) if v is not None]
        if len(keep) < 3:
            continue
        yy = M._centred([y[i] for i in keep])
        start = len(ys)
        ys += yy
        spans.append((start, start + len(yy)))
        for n, fn, _ in RANKERS:
            col = [fn(rs[i]) for i in keep]
            col = [c if c is not None else 0.0 for c in col]
            xs[n] += M._centred(col)
    n_tot = len(ys)
    if n_tot < 10:
        return {"best_abs_rho": None, "family_p": None}

    my = sum(ys) / n_tot
    dy = [v - my for v in ys]
    sy = math.sqrt(sum(v * v for v in dy)) or 1.0
    prep = {}
    for n in names:
        col = xs[n]
        m = sum(col) / n_tot
        d = [v - m for v in col]
        sx = math.sqrt(sum(v * v for v in d)) or 1.0
        prep[n] = (d, sx)

    def best(vec):
        return max(abs(sum(a * b for a, b in zip(d, vec)) / (sx * sy))
                   for d, sx in prep.values())

    obs = best(dy)
    buf = list(dy)
    hits = 0
    for _ in range(reps):
        for lo, hi in spans:
            seg = buf[lo:hi]
            rng.shuffle(seg)
            buf[lo:hi] = seg
        if best(buf) >= obs:
            hits += 1
    return {"best_abs_rho": round(obs, 4),
            "family_p": round((hits + 1) / (reps + 1), 5),
            "candidates": len(RANKERS), "reps": reps,
            "note": "one shuffle per day shared by every candidate, so near-duplicate "
                    "candidates cannot make the correction lenient"}


def book(sel, horizon, excess, mult, side):
    """Equal-weight the day's worst K, hold one horizon. Days are the unit."""
    per_day = []
    for d, rs in sel.items():
        legs = net_of_cost(rs, horizon, mult, excess, side)
        if legs:
            per_day.append({"date": d, "n": len(legs), "ret_pct": round(M.mean(legs), 4)})
    vals = [p["ret_pct"] for p in per_day]
    out = describe(vals, f"{'long' if side > 0 else 'short'} worst-K, "
                          f"{horizon}, cost x{mult}")
    out["days"] = len(per_day)
    out["names_per_day"] = round(M.mean([p["n"] for p in per_day]), 1) if per_day else 0
    out["cumulative_pct"] = round(sum(vals), 2)
    return out, per_day


def book_sweep(sel, ex):
    """The same book at every horizon, both sides, two cost levels, three liquidity cuts.

    ONE ENTRY COST BUYS EVERY HORIZON, WHICH IS THE WHOLE ARGUMENT FOR HOLDING LONGER.
    The spread is paid once whatever the holding period, so a drift of 0.3% a session is
    worthless at one session and worth having at ten. That is a statement about cost, not
    about skill, and it is the reason this table exists separately from the base rates.

    The liquidity cuts matter more here than anywhere else in the repo: this screen
    selects on a realised extreme move, and extreme movers are thin. A result that lives
    only under $1m a day is a result nobody can trade.
    """
    cuts = {"all": lambda r: True,
            "dv>=$1m": lambda r: r["dv_med20"] >= 1e6,
            "dv>=$5m": lambda r: r["dv_med20"] >= 5e6}
    out = {}
    for cut, keep in cuts.items():
        out[cut] = {}
        for h in HORIZONS:
            out[cut][h] = {}
            for side, tag in ((-1, "short"), (+1, "long")):
                for m in (0, 1):
                    per_day = []
                    for d, rs in sel.items():
                        rs2 = [r for r in rs if keep(r)]
                        legs = net_of_cost(rs2, h, m, ex, side)
                        if legs:
                            per_day.append(M.mean(legs))
                    if len(per_day) < 30:
                        continue
                    lo, hi = M.bootstrap_ci(per_day)
                    out[cut][h][f"{tag}_x{m}"] = {
                        "days": len(per_day),
                        "mean_per_day_pct": round(M.mean(per_day), 3),
                        "t": M.tstat(per_day),
                        "ci95": [lo, hi],
                        "up_days_pct": round(100 * sum(1 for v in per_day if v > 0)
                                             / len(per_day), 1),
                    }
    out["borrow_warning"] = (
        "the short side assumes the name can be borrowed and charges no borrow fee. "
        "On this screen the hardest-falling names are the hardest to borrow, and a "
        "hard-to-borrow rate of 20-100% annualised is 1.2-6.0 points over a 21-session "
        "hold -- of the same order as the drift being measured. Nothing here nets it off")
    return out


def overlap_check(sel, ex, horizons=("d5", "d10", "d21")):
    """The same book on NON-OVERLAPPING days, because t on overlapping ones is inflated.

    Holding 15 names for 21 sessions and starting a new book every session means 21
    books are open at once and consecutive day-returns share 20/21 of their window.
    They are not 728 independent observations and a t computed as if they were is the
    single easiest way to oversell this stage.

    EVERY STARTING OFFSET IS RUN, NOT ONE. Thinning to every Nth session leaves one
    arbitrary subsample of about 34 books at N=21, and which 34 moves the mean by
    several points -- the first offset tried gave +10.6% where the full overlapping
    sample gives +5.4%. So all N offsets are run and the spread across them is
    reported. The number to quote is the median offset's t, with the worst offset
    beside it.
    """
    days = sorted(sel)
    out = {}
    for h in horizons:
        n = int(h[1:])
        for side, tag in ((-1, "short"), (+1, "long")):
            per_offset = []
            for off in range(n):
                vals = []
                for i in range(off, len(days), n):
                    legs = net_of_cost(sel[days[i]], h, 1, ex, side)
                    if legs:
                        vals.append(M.mean(legs))
                if len(vals) >= 8:
                    per_offset.append({"offset": off, "books": len(vals),
                                       "mean_pct": round(M.mean(vals), 3),
                                       "t": M.tstat(vals),
                                       "up_books_pct": round(100 * sum(
                                           1 for v in vals if v > 0) / len(vals), 1)})
            if not per_offset:
                continue
            ts = sorted(x["t"] for x in per_offset if x["t"] is not None)
            ms = sorted(x["mean_pct"] for x in per_offset)
            out[f"{h}_{tag}_x1"] = {
                "offsets": len(per_offset),
                "books_per_offset": per_offset[0]["books"],
                "median_mean_pct": ms[len(ms) // 2],
                "min_mean_pct": ms[0], "max_mean_pct": ms[-1],
                "median_t": ts[len(ts) // 2] if ts else None,
                "min_t": ts[0] if ts else None, "max_t": ts[-1] if ts else None,
                "offsets_with_t_over_2": sum(1 for t in ts if t > 2),
            }
    out["note"] = ("every Nth session only, N = the holding period, so no two books in "
                   "one offset share a day. All N offsets are run; quote the median t "
                   "and the min. Compare these with book_sweep's t, never the reverse")
    return out


def entry_next_open(sel, ex, horizons=("d1", "d2", "d3", "d5", "d10", "d21")):
    """The same book entered at the NEXT OPEN instead of the drop-day close.

    Phase 0's own base rates say the overnight leg runs the other way: +0.93% to the
    next open on average, against a negative drift from there on. A short put on at the
    close therefore pays for that bounce before it earns anything. This derives the
    open-entry return from the two legs already harvested rather than refetching, and
    it is the cheapest improvement available to this stage if the drift is real.
    """
    out = {}
    for h in horizons:
        for side, tag in ((-1, "short"), (+1, "long")):
            vals = []
            for d, rs in sel.items():
                legs = []
                for r in rs:
                    a, b = r.get("fwd_open1"), r.get("fwd_" + h)
                    hs = r.get("half_spread_pct")
                    if a is None or b is None or hs is None:
                        continue
                    g = ((1 + b / 100) / (1 + a / 100) - 1) * 100
                    legs.append(side * g - 2 * hs)
                if legs:
                    vals.append(M.mean(legs))
            if len(vals) < 30:
                continue
            lo, hi = M.bootstrap_ci(vals)
            out[f"{h}_{tag}_x1"] = {"days": len(vals),
                                    "mean_per_day_pct": round(M.mean(vals), 3),
                                    "t": M.tstat(vals), "ci95": [lo, hi]}
    out["note"] = ("entry at the open after the drop, exit at the same horizon's close. "
                   "Derived from the harvested legs, so it costs no extra fetch")
    return out


# ----------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drops", required=True, help="dir holding drops.jsonl.gz")
    ap.add_argument("--k", type=int, default=15, help="names taken per session")
    ap.add_argument("--ret", type=float, default=-5.0, help="max drop kept, percent")
    ap.add_argument("--dv", type=float, default=200_000, help="median 20d dollar volume floor")
    ap.add_argument("--price", type=float, default=1.0)
    ap.add_argument("--reps", type=int, default=1500, help="permutation reps")
    ap.add_argument("--range", default="3y")
    ap.add_argument("--out", default=str(REPO / "researcher_reversal" / "analysis"))
    a = ap.parse_args()

    rows = load(a.drops, a.ret, a.dv, a.price)
    sel = select(rows, a.k)
    flat = [r for rs in sel.values() for r in rs]
    ex = market(a.range)
    print(f"{len(rows)} rows pass the floors, {len(flat)} selected over "
          f"{len(sel)} sessions", file=sys.stderr)

    rep = {
        "built_utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                                 __import__("time").gmtime()),
        "screen": {"worst_per_session": a.k, "max_ret_pct": a.ret,
                   "dv_med20_min": a.dv, "price_min": a.price},
        "sample": {"rows_passing_floors": len(rows), "selected": len(flat),
                   "sessions": len(sel),
                   "first": min(sel) if sel else None, "last": max(sel) if sel else None,
                   "median_drop_pct": round(statistics.median(
                       [r["ret_d_pct"] for r in flat]), 2) if flat else None,
                   "median_dv_med20": M.median([r["dv_med20"] for r in flat]),
                   "median_half_spread_pct": M.median(
                       [r["half_spread_pct"] for r in flat])},
        "known_biases": {
            "survivorship": "the universe is today's listings, so drops followed by a "
                            "delisting are absent. Removes the worst continuations only, "
                            "so every reversal number here is an upper bound",
            "spread_estimated": "Corwin-Schultz from the 21 days before the drop. A floor "
                                "on the real cost, and blind to the widening the drop causes",
            "no_borrow_check": "the short side assumes every name is shortable. On this "
                               "screen many are not, and the ones that are not are the "
                               "ones that fell hardest",
            "adjusted_prices": "returns are split and dividend adjusted, so a corporate "
                               "action cannot masquerade as a drop",
        },
        "base_rates_gross": {h: describe([_fwd(r, h) for r in flat], h)
                             for h in HORIZONS},
        "base_rates_excess": {h: describe([_fwd(r, h, ex) for r in flat], h)
                              for h in HORIZONS},
        "net_of_cost": {
            f"x{m}": {h: describe(net_of_cost(flat, h, m), f"{h} net x{m}")
                      for h in HORIZONS} for m in (0, 1, 2)},
    }

    rep["cuts"] = {
        "by_drop_size": band(flat, lambda r: r["ret_d_pct"],
                             [-1e9, -40, -25, -15, -10, -7.5],
                             ["<=-40%", "-40..-25", "-25..-15", "-15..-10",
                              "-10..-7.5", "-7.5..-5"], HEADLINE),
        "by_turnover": band(flat, lambda r: r["dv_med20"],
                            [0, 1e6, 5e6, 25e6, 1e8],
                            ["<$1m", "$1-5m", "$5-25m", "$25-100m", ">$100m"], HEADLINE),
        "by_price": band(flat, lambda r: r["price"], [0, 3, 10, 30],
                         ["$1-3", "$3-10", "$10-30", ">$30"], HEADLINE),
        "by_gap_share": band(flat, lambda r: r["gap_share"], [-1e9, 0, 0.5, 0.9],
                             ["gap up / drift down", "mostly intraday",
                              "mostly gap", "almost all gap"], HEADLINE),
        "by_vol_spike": band(flat, lambda r: r["vol_spike"], [0, 2, 5, 15],
                             ["<2x", "2-5x", "5-15x", ">15x"], HEADLINE),
        "by_half_spread": band(flat, lambda r: r["half_spread_pct"],
                               [0, 0.25, 0.75, 2.0],
                               ["<0.25%", "0.25-0.75%", "0.75-2%", ">2%"], HEADLINE),
    }
    sectors = sorted({r["sector"] for r in flat if r["sector"]})
    rep["cuts"]["by_sector"] = sorted(
        [describe([_fwd(r, HEADLINE) for r in flat if r["sector"] == s], s)
         for s in sectors], key=lambda d: -d["n"])

    rep["rankers"] = {h: rankers(sel, h, ex, a.reps) for h in ("d1", "d5")}
    rep["family_wise_d1"] = family_wise(sel, "d1", ex, min(a.reps, 600))

    rep["book_sweep"] = book_sweep(sel, ex)
    rep["overlap_check"] = overlap_check(sel, ex)
    rep["entry_next_open"] = entry_next_open(sel, ex)
    rep["book"] = {}
    for side, tag in ((+1, "long"), (-1, "short")):
        for m in (0, 1):
            k = f"{tag}_cost_x{m}"
            b, per_day = book(sel, HEADLINE, ex, m, side)
            rep["book"][k] = b
            if side > 0 and m == 1:
                rep["book"]["long_cost_x1_per_day"] = per_day[-20:]

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "phase0-base-rates.json").write_text(json.dumps(rep, indent=1))

    # The selected rows travel with the report. The full harvest is 284k rows and 29MB
    # and belongs in a scratch directory; these 11k are what every number above was
    # computed on, so checking them in is what makes the report auditable rather than
    # asserted. Rebuild the harvest with rev_harvest.py to sweep the floors again.
    with gzip.open(out / "phase0-selected.jsonl.gz", "wt") as fh:
        for d in sorted(sel):
            for r in sel[d]:
                fh.write(json.dumps(r, separators=(",", ":")) + "\n")
    print(json.dumps({k: rep[k] for k in
                      ("sample", "base_rates_gross", "net_of_cost")}, indent=1))
    print(f"\nwrote {out / 'phase0-base-rates.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
