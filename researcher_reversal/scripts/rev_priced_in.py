#!/usr/bin/env python3
"""The sealed baseline: what is already known and what is already scheduled.

THE STAGE'S QUESTION IS FORWARD, SO THE BASELINE CARRIES A FORWARD BLOCK
------------------------------------------------------------------------
Stage R asks whether more bad news is coming that the price does not hold, not whether
yesterday's fall was proportionate. That makes `forward` -- built by rev_forward.py from
EDGAR's submissions feed and full-text search, Nasdaq's dated short interest and insider
summary, and ClinicalTrials.gov -- the most important thing in this file. It is sealed
here rather than left to each hunter so that the hunt starts at a document, and so that
two hunts on one name start from the same documents.

THE ANALOGUE, AND WHERE IT BREAKS
---------------------------------
For an earnings print, `researcher_us/scripts/priced_in.py` seals three things: the
option-implied move (how far the market thinks it goes), the skew (which way), and the
history of prior prints (how it usually behaves). For a stock that fell 18% yesterday
the same three exist and two of them are BETTER:

  magnitude   the option chain still works where one is listed, and post-drop implied
              vol is a live statement about whether the market thinks there is more to
              come. Where there is no chain, the name's own realised volatility and the
              size of the drop stand in.
  direction   this is the weak one. There is no scheduled event for skew to be about,
              so the direction anchor is the name's OWN history of comparable falls and
              a cross-sectional prior. Both are close to the free control, which is the
              stage J failure mode -- see `lean_vs_free_control_rho` below.
  history     strictly better than the earnings version. Prior comparable drops are
              OBSERVED, dated, and there are usually more of them than a company has
              quarters. `researcher_japan` had to estimate its cadence and labelled
              every row `estimated`; nothing here is estimated.

THE LEAN IS ENTANGLED WITH ITS OWN BENCHMARK AND THAT IS STATED, NOT FIXED
--------------------------------------------------------------------------
`priced_lean_pct` is built from the name's own history of comparable drops and a
cross-sectional prior conditioned on the bands it falls in. Both move with the size of
the drop, and minus the size of the drop is the free control every ranker is measured
against. Stage J shipped with that entanglement at 1.0 by construction and had to fix
it; here it is reported per run as `lean_vs_free_control_rho` and the components are
kept separate so `rev_resolve.py` can rank each one on its own. If that number reads
near 1.0, the lean IS the control and nothing built on it can beat the control.

THE ONE THING THAT CAN KILL A NAME
----------------------------------
A drop that is a corporate action rather than news. Splits and ordinary dividends are
adjusted out upstream; spin-offs, large special dividends and rights issues often are
not, and they produce a textbook-looking 20% fall with no news and no volume. The check
is cheap: real news brings volume. A drop with no volume spike is marked suspect, which
the shared scorer already multiplies by 0.05 through `event_plausibility`.

    python3 researcher_reversal/scripts/rev_priced_in.py --ticker ABC --date 2026-09-21
"""
import argparse
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))
import rev_market as M                                            # noqa: E402
import rev_forward as F                                           # noqa: E402

try:
    import priced_in as PI                                        # noqa: E402
except Exception:                                                 # noqa: BLE001
    PI = None

PRIOR_PATH = REPO / "researcher_reversal" / "analysis" / "phase0-base-rates.json"


# ------------------------------------------------------------- own history
def comparable_drops(b, i, frac=0.7, lookback=756):
    """Every earlier day this name fell at least `frac` of today's fall.

    Observed and dated, not inferred. The forward leg is the next session's close,
    which is the horizon this stage predicts. Returns the rows and a summary.
    """
    today = (b[i]["close"] / b[i - 1]["close"] - 1) * 100
    thresh = today * frac
    lo = max(1, i - lookback)
    out = []
    for j in range(lo, i):
        if j + 1 >= len(b):
            break
        r = (b[j]["close"] / b[j - 1]["close"] - 1) * 100
        if r <= thresh:
            out.append({
                "date": b[j]["date"],
                "drop_pct": round(r, 2),
                "next_close_pct": round((b[j + 1]["close"] / b[j]["close"] - 1) * 100, 2),
                "next_open_pct": round((b[j + 1]["open"] / b[j]["close"] - 1) * 100, 2),
            })
    nxt = [o["next_close_pct"] for o in out]
    return {
        "basis": f"observed daily closes, drops at or below {round(thresh, 2)}% "
                 f"({frac} of today's), 3-year lookback",
        "n": len(out),
        "median_next_close_pct": round(statistics.median(nxt), 2) if nxt else None,
        "mean_next_close_pct": round(M.mean(nxt), 2) if nxt else None,
        "up_rate_pct": round(100 * sum(1 for x in nxt if x > 0) / len(nxt), 1) if nxt else None,
        "median_abs_next_pct": round(statistics.median([abs(x) for x in nxt]), 2) if nxt else None,
        "events": out[-12:],
    }


# ------------------------------------------------------- cross-section prior
def cross_prior(row, path=PRIOR_PATH):
    """The phase-0 base rate for the bands this name falls in.

    Explicitly a PRIOR and not evidence about this company. It is read from the file
    phase 0 wrote, so a run cannot quote a base rate nobody measured; where that file
    is absent the prior is None and `anchor_quality.direction` falls accordingly.
    """
    if not Path(path).exists():
        return {"status": "no phase0 file", "expected_next_close_pct": None}
    d = json.loads(Path(path).read_text())
    cuts = d.get("cuts") or {}

    def pick(bands, val, edges):
        if val is None:
            return None
        for i in range(len(edges) - 1, -1, -1):
            if val >= edges[i]:
                return bands[i] if i < len(bands) else None
        return bands[0] if bands else None

    size = pick(cuts.get("by_drop_size") or [], row.get("ret_d_pct"),
                [-1e9, -40, -25, -15, -10, -7.5][::-1][::-1])
    turn = pick(cuts.get("by_turnover") or [], row.get("dv_med20"),
                [0, 1e6, 5e6, 25e6, 1e8])
    out = {"built_from": d.get("built_utc"),
           "headline_horizon": "next session close",
           "drop_size_band": (size or {}).get("label"),
           "drop_size_mean_pct": (size or {}).get("mean_pct"),
           "drop_size_n": (size or {}).get("n"),
           "turnover_band": (turn or {}).get("label"),
           "turnover_mean_pct": (turn or {}).get("mean_pct"),
           "turnover_n": (turn or {}).get("n"),
           "all_names_mean_pct": ((d.get("base_rates_gross") or {}).get("d1") or {}).get("mean_pct")}
    parts = [x for x in (out["drop_size_mean_pct"], out["turnover_mean_pct"]) if x is not None]
    out["expected_next_close_pct"] = round(M.mean(parts), 3) if parts else out["all_names_mean_pct"]
    return out


# ------------------------------------------------------------------- build
def build(ticker, drop_date, meta=None, with_options=True, bars=None,
          with_forward=True):
    meta = meta or {}
    b = bars if bars is not None else M.bars(ticker, rg="3y")
    if not b:
        return {"ticker": ticker, "status": "no_bars"}
    idx = {x["date"]: i for i, x in enumerate(b)}
    if drop_date not in idx:
        return {"ticker": ticker, "status": "date_not_traded", "last_bar": b[-1]["date"]}
    i = idx[drop_date]
    if i < 22:
        return {"ticker": ticker, "status": "too_little_history"}
    prev, cur = b[i - 1], b[i]

    def pc(a, c):
        return None if not c else round((a / c - 1) * 100, 3)

    w20 = b[i - 20:i]
    dv = M.median([x["close"] * x["volume"] for x in w20]) or 0.0
    vol20 = M.median([x["volume"] for x in w20]) or 0.0
    ret = pc(cur["close"], prev["close"])
    gap = pc(cur["open"], prev["close"])
    spike = round(cur["volume"] / vol20, 2) if vol20 else None

    w52 = b[max(0, i - 252):i + 1]
    hi52, lo52 = max(x["high"] for x in w52), min(x["low"] for x in w52)
    tr = []
    for j in range(max(1, i - 13), i + 1):
        p, c = b[j - 1], b[j]
        tr.append(max(c["high"] - c["low"], abs(c["high"] - p["close"]),
                      abs(p["close"] - c["low"])))

    row = {"ret_d_pct": ret, "dv_med20": dv}
    hist = comparable_drops(b, i)
    prior = cross_prior(row)

    # A real 15% fall brings volume. One that does not is usually a corporate action
    # the adjustment missed -- a spin-off, a rights issue, a large special dividend --
    # and the shape it makes is specific: the whole fall overnight, on ordinary volume,
    # with no intraday follow-through. That triple is `suspect`, which the shared
    # scorer multiplies by 0.05 and so effectively removes the name.
    #
    # THIN VOLUME ALONE IS NOT THAT. On the 2026-09-21 screen four of fifteen names
    # fell more than 15% on under 1.5x their median volume, which is ordinary in a
    # $2m-a-day stock and not evidence of anything. Those are `unknown`, worth 0.6,
    # and the hunter is asked to name what happened rather than the baseline guessing.
    gs = (gap / ret) if (gap is not None and ret) else None
    suspect = (spike is not None and spike < 1.0 and ret is not None and ret <= -15
               and gs is not None and gs > 0.8)
    verdict = ("suspect" if suspect
               else "fits_cadence" if (spike or 0) >= 2
               else "unknown")

    doc = {
        "ticker": ticker,
        "company": meta.get("company"),
        "sector": meta.get("sector"),
        "exchange": meta.get("exchange"),
        "drop_date": drop_date,
        "predicted_window": "close of drop_date -> close of the next regular session",
        "as_of_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "spot": round(cur["raw_close"], 4),
        "spot_basis": "unadjusted close of the drop day, which is the entry price",
        "drop": {
            "ret_d_pct": ret,
            "gap_pct": gap,
            "intraday_pct": pc(cur["close"], cur["open"]),
            "gap_share": round(gap / ret, 3) if (gap is not None and ret) else None,
            "volume_spike_x": spike,
            "dollar_volume_d": round(cur["close"] * cur["volume"]),
            "dv_med20": round(dv),
        },
        "context": {
            "price": round(cur["raw_close"], 4),
            "market_cap_now": meta.get("market_cap"),
            "pos_52w": round((cur["close"] - lo52) / (hi52 - lo52), 3) if hi52 > lo52 else None,
            "atr14_pct": round(100 * M.mean(tr) / cur["close"], 3) if tr else None,
            "run_up_5d_pct": pc(prev["close"], b[i - 6]["close"]) if i >= 6 else None,
            "run_up_20d_pct": pc(prev["close"], b[i - 21]["close"]) if i >= 21 else None,
            "run_up_60d_pct": pc(prev["close"], b[i - 61]["close"]) if i >= 61 else None,
        },
        "costs": _costs(b, i),
        # The shared scorer's own key name, so researcher_us/scripts/edge_score.py
        # reads this baseline unchanged. `n` is what it scales history quality on.
        "history": hist,
        "cross_section_prior": prior,
        "event_plausibility": {
            "verdict": verdict,
            "why": ("the whole fall happened overnight on below-normal volume with no "
                    "intraday follow-through: the shape of an unadjusted corporate "
                    "action, not of news. Confirm before ranking it" if suspect else
                    "volume confirms something happened" if verdict == "fits_cadence" else
                    "volume is ordinary. The drop is real; what caused it is the "
                    "hunter's first question, not the baseline's guess"),
            "volume_spike_x": spike,
            "gap_share": round(gs, 3) if gs is not None else None,
            "hunter_must_answer": "what caused this fall, with a source and a timestamp",
        },
        "sources": ["yahoo chart v8 daily bars (split and dividend adjusted)",
                    "nasdaq screener (sector, cap)"],
    }

    # THE FORWARD PIPELINE IS THE POINT OF THIS STAGE, so it is sealed with everything
    # else rather than left to each hunter to find. It is every dated thing about this
    # issuer that a source measured to answer can supply: its filing history by form,
    # full-text hits for the phrases that carry a forward risk, dated short interest,
    # insider activity, active trials, and the bid-price rule. The hunter starts at a
    # document instead of a search box, and two hunters on the same name start from the
    # same documents rather than from whatever each happened to find.
    if with_forward:
        try:
            doc["forward"] = F.build(ticker, price=cur["raw_close"])
        except Exception as e:                                    # noqa: BLE001
            doc["forward"] = {"status": "error", "note": str(e)[:200]}
    else:
        doc["forward"] = {"status": "not_requested"}

    if with_options and PI is not None:
        try:
            o = PI.options(ticker, drop_date, cur["raw_close"],
                           realised_vol_pct=doc["context"]["atr14_pct"])
        except Exception as e:                                    # noqa: BLE001
            o = {"status": "error", "note": str(e)[:200]}
        # The straddle here is NOT an event move: there is no scheduled event. It is
        # the market's forward vol over the life of the front expiry, which is the
        # honest reading and the one the note must use.
        if isinstance(o, dict):
            o.pop("event_implied_move_pct", None)
            o["forward_move_basis"] = ("straddle over the front expiry. No scheduled "
                                       "event, so this is forward vol and not an "
                                       "event-implied move")
        doc["options"] = o
    else:
        doc["options"] = {"status": "not_requested"}

    doc.update(_anchors(doc))
    return doc


def _costs(b, i):
    """The estimated round-trip cost, with an honest word for a zero.

    Corwin-Schultz floors a negative estimate at zero, and on a name whose daily range
    is dominated by overnight moves the median of those estimates IS zero. That is the
    estimator failing, not a free trade: on the 2026-09-21 screen four of fifteen names
    came back at 0.00% and one at 4.10%. A reader who takes the zero at face value has
    the cost of this stage exactly backwards, so the status says which case it is.
    """
    hs = M.half_spread_pct(b[i - 21:i])
    hsd = M.half_spread_pct(b[i - 21:i + 1])
    if hs is None:
        st = "not_estimable"
    elif hs == 0.0:
        st = ("estimator_floored_at_zero: more than half the two-day pairs returned a "
              "negative estimate. Read this as UNKNOWN, never as a narrow spread")
    else:
        st = "ok"
    return {
        "half_spread_pct": hs,
        "half_spread_incl_drop_pct": hsd,
        "half_spread_status": st,
        "round_trip_pct": round(2 * hs, 4) if hs else None,
        "basis": "Corwin-Schultz two-day high-low estimate over the 21 sessions BEFORE "
                 "the drop. A FLOOR on the real spread, and blind to the widening the "
                 "drop itself causes",
    }


def _anchors(doc):
    """`anchor_quality` and `priced_lean_pct`, the two keys the shared scorer reads."""
    o = doc.get("options") or {}
    hist = doc.get("history") or {}
    prior = doc.get("cross_section_prior") or {}

    # magnitude: a live chain is the best statement of how far it can still go. Without
    # one, the name's own realised volatility is a real scale and is paid less.
    if o.get("straddle_implied_move_pct") is not None:
        mag = 0.85
    elif doc["context"].get("atr14_pct"):
        mag = 0.45
    else:
        mag = 0.10

    # direction: this is the weak anchor and it is paid like one. Skew is a genuine
    # directional statement; the name's own comparable drops are weaker; a cross-
    # sectional prior is weaker still because it says nothing about THIS company.
    if o.get("skew_25d_vol_points") is not None:
        d = 0.70
    elif (hist.get("n") or 0) >= 6:
        d = 0.45
    elif prior.get("expected_next_close_pct") is not None:
        d = 0.20
    else:
        d = 0.05

    own = hist.get("median_next_close_pct")
    pri = prior.get("expected_next_close_pct")
    skew = o.get("skew_25d_vol_points")
    parts, w = [], []
    if own is not None:
        # WEIGHTED BY HOW MANY COMPARABLE FALLS THERE ACTUALLY WERE. On the 2026-09-11
        # validation day CVV had exactly one, it happened to bounce 14.8%, and an
        # unweighted term put the baseline's lean at +8.3 points before any research --
        # a number the hunt would then have had to argue against. n/6, the same shape
        # edge_score.baseline_quality() already uses for history, so one prior fall
        # contributes a sixth of its face value and six or more contribute all of it.
        w.append(0.45 * min(1.0, (hist.get("n") or 0) / 6.0))
        parts.append(own)
    if pri is not None:
        parts.append(pri); w.append(0.35)
    if skew is not None:
        parts.append(-0.25 * skew); w.append(0.20)
    keep = [(p_, q) for p_, q in zip(parts, w) if q > 0]
    lean = (round(sum(p_ * q for p_, q in keep) / sum(q for _, q in keep), 3)
            if keep else None)

    return {
        "anchor_quality": {"magnitude": mag, "direction": d},
        "priced_lean_pct": lean,
        "lean_components": {
            "own_comparable_drops_median_pct": own,
            "cross_section_prior_pct": pri,
            "minus_quarter_skew": round(-0.25 * skew, 3) if skew is not None else None,
            "warning": "the first two both move with the size of the drop, and minus "
                       "the size of the drop is the free control. rev_resolve.py "
                       "reports lean_vs_free_control_rho; near 1.0 means this lean "
                       "cannot beat the control because it IS the control",
        },
        "free_controls": {
            "neg_ret_d_pct": -doc["drop"]["ret_d_pct"] if doc["drop"]["ret_d_pct"] else None,
            "neg_run_up_20d_pct": (-doc["context"]["run_up_20d_pct"]
                                   if doc["context"].get("run_up_20d_pct") is not None else None),
        },
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--date", required=True, help="the drop date, YYYY-MM-DD")
    ap.add_argument("--no-options", action="store_true")
    ap.add_argument("--no-forward", action="store_true",
                    help="skip the forward pipeline. Only for a plumbing test: it is "
                         "the block this stage exists to hand the hunter")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    doc = build(a.ticker, a.date, with_options=not a.no_options,
                with_forward=not a.no_forward)
    s = json.dumps(doc, indent=1)
    if a.out:
        Path(a.out).write_text(s)
    print(s)


if __name__ == "__main__":
    main()
