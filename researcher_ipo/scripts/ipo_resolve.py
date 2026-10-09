#!/usr/bin/env python3
"""Resolve stage IPO runs against what the stocks did inside the window.

    python3 researcher_ipo/scripts/ipo_resolve.py --run <RUN> [-o <RUN>/ipo-resolved.json]
    python3 researcher_ipo/scripts/ipo_resolve.py --pool          # every ipo run on disk

Per name, from Yahoo daily bars:
  debut   key: day-1 open (the first trade) -> day-1 close. Beside it, never ranked: the
          pop (offer -> first trade), offer -> day-1 close, day-1 close -> day-2 close.
  lockup  key: open -> close of the event session. Beside it: the same window on the
          expiration-date session (the other date convention), close(D-1) -> close(D).
Every key move is also given net of IWM over the same window (`realised_excess_pct`).

A debut whose first bar is not the event date did not debut that day: it gets
`event_occurred: false` with the date it did trade, and leaves every statistic.

WHY THIS STAGE IS JUDGED POOLED. Phase 0 counts about one event per session, so most
days carry one or two names and a within-day rank correlation does not exist. One day is
an anecdote here even more than elsewhere. `--pool` ranks every resolved name of every
run together on the EXCESS move, so a market-wide day cannot manufacture the result, and
reports the debut and lock-up legs apart, because they are different events on different
scales. Nothing here places an order.
"""
import argparse
import glob
import json
import statistics as st
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ipo_market as IM                                           # noqa: E402
RM = IM.RM


def load(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:                                             # noqa: BLE001
        return None


def realised(b):
    t, day = b["ticker"], date.fromisoformat(b["event_date"])
    bs = IM.bars(t, rg="2y")
    row = {"ticker": t, "event_type": b["event_type"], "event_date": b["event_date"]}
    if not bs:
        row.update({"move_pending": True, "why": "no bars"})
        return row
    if b["event_type"] == "debut":
        b0 = bs[0]
        if b0["date"] < b["event_date"]:
            row.update({"event_occurred": False, "first_bar_date": b0["date"],
                        "event_occurred_note": f"first bar {b0['date']} precedes the event date"})
            return row
        if b0["date"] > b["event_date"]:
            if date.today() <= day:
                row.update({"move_pending": True, "why": "the session has not closed"})
            else:
                row.update({"event_occurred": False, "first_bar_date": b0["date"],
                            "event_occurred_note": f"did not trade on {b['event_date']}; first bar {b0['date']}"})
            return row
        offer = (b.get("deal") or {}).get("offer_price")
        ro = b0["open"] * (b0["raw_close"] / b0["close"]) if b0["close"] else None
        row.update({"realised_move_pct": IM.pct(b0["open"], b0["close"]),
                    "first_trade_price": round(ro, 4) if ro else None,
                    "pop_pct": IM.pct(offer, ro) if offer else None,
                    "offer_to_close_pct": IM.pct(offer, b0["raw_close"]) if offer else None,
                    "d1_to_d2_pct": IM.pct(b0["close"], bs[1]["close"]) if len(bs) > 1 else None,
                    "day1_turnover_usd": round(b0["raw_close"] * b0["volume"], 0)})
        bm = IM.benchmark_window(day, "open_close")
    else:
        bar = IM.bar_on(bs, day)
        if not bar:
            row.update({"move_pending": True, "why": "no bar on the event day yet"})
            return row
        prev = IM.bars_before(bs, day)
        exp = (b.get("lockup") or {}).get("expiration_date")
        bexp = IM.bar_on(bs, exp) if exp else None
        row.update({"realised_move_pct": IM.pct(bar["open"], bar["close"]),
                    "expiry_session_move_pct": IM.pct(bexp["open"], bexp["close"]) if bexp else None,
                    "close_to_close_pct": IM.pct(prev[-1]["close"], bar["close"]) if prev else None,
                    "volume_vs_20d": (round(bar["volume"] / st.mean([x["volume"] for x in prev[-20:]]), 2)
                                      if len(prev) >= 20 and st.mean([x["volume"] for x in prev[-20:]]) else None)})
        bm = IM.benchmark_window(day, "open_close")
    mv = row.get("realised_move_pct")
    row["benchmark_iwm_pct"] = bm
    row["realised_excess_pct"] = round(mv - bm, 3) if mv is not None and bm is not None else None
    return row


def resolve_run(run):
    run = Path(run)
    scores = {r["ticker"]: r for r in (load(run / "edge-scores.json") or {}).get("ranking", [])}
    panel = {r["ticker"]: r for r in (load(run / "edge-scores-panel.json") or {}).get("ranking", [])}
    rows = []
    for f in sorted((run / "baselines").glob("*.json")):
        b = load(f)
        if not b:
            continue
        r = realised(b)
        s = scores.get(b["ticker"]) or {}
        r.update({"rankable": bool(s.get("rankable")) and r.get("event_occurred") is not False,
                  "impact_sum": s.get("impact_sum"),
                  "panel_score": (panel.get(b["ticker"]) or {}).get("panel_score"),
                  "panel_selected": (panel.get(b["ticker"]) or {}).get("selected"),
                  "vs_offer_pct": (b.get("tape") or {}).get("vs_offer_pct"),
                  "run_up_20d_pct": b.get("run_up_20d_pct"),
                  "deal_usd": (b.get("deal") or {}).get("deal_usd")})
        rows.append(r)
    return rows, (load(run / "universe.json") or {}).get("validation_only", False)


def rank_block(rows, key, val):
    pairs = [(r[key], r[val]) for r in rows if r.get(key) is not None and r.get(val) is not None]
    out = {"n": len(pairs)}
    if len(pairs) < 5:
        out["rho_withheld"] = "fewer than five resolved names"
        return out
    xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
    out["spearman"] = RM.spearman(xs, ys)
    # one pooled group: the moves are already net of IWM, which is what stands in for
    # the within-day centring every other stage uses
    out["p"] = RM.permutation_p([pairs], reps=2000)[1]
    return out


def book(rows, floor, val):
    sel = [r for r in rows if r.get("impact_sum") is not None and abs(r["impact_sum"]) >= floor
           and r.get(val) is not None]
    rets = [(1 if r["impact_sum"] > 0 else -1) * r[val] for r in sel]
    if not rets:
        return {"n": 0, "floor": floor}
    return {"n": len(rets), "floor": floor, "hits": sum(x > 0 for x in rets),
            "mean_signed_pct": round(st.mean(rets), 2), "t": RM.tstat(rets)}


def stats(rows, floor):
    ok = [r for r in rows if r.get("rankable") and r.get("realised_move_pct") is not None]
    out = {"resolved": len(ok)}
    for ev in ("all",) + IM.EVENT_TYPES:
        sub = ok if ev == "all" else [r for r in ok if r["event_type"] == ev]
        blk = {"n": len(sub),
               "impact_sum_vs_move": rank_block(sub, "impact_sum", "realised_move_pct"),
               "impact_sum_vs_excess": rank_block(sub, "impact_sum", "realised_excess_pct"),
               "panel_vs_excess": rank_block(sub, "panel_score", "realised_excess_pct"),
               "conviction_book_excess": book(sub, floor, "realised_excess_pct"),
               "sign_hit_rate": (round(sum((r["impact_sum"] > 0) == (r["realised_move_pct"] > 0)
                                           for r in sub if r["impact_sum"]) /
                                       max(1, sum(1 for r in sub if r["impact_sum"])), 3) if sub else None)}
        if ev == "lockup":
            for c in ("vs_offer_pct", "run_up_20d_pct"):
                neg = [dict(r, _c=-r[c]) for r in sub if r.get(c) is not None]
                blk[f"free_control_neg_{c}"] = rank_block(neg, "_c", "realised_excess_pct")
        out[ev] = blk
    return out


def floor_of():
    try:
        import yaml
        c = yaml.safe_load(open(IM.REPO / "config" / "pipeline.yaml"))
        return float((c.get("ipo_hunt") or {}).get("conviction_floor")
                     or (c.get("edge_hunt") or {}).get("conviction_floor") or 2.8)
    except Exception:                                             # noqa: BLE001
        return 2.8


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run")
    ap.add_argument("--pool", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    floor = floor_of()
    if a.pool:
        rows, days = [], 0
        for run in sorted(glob.glob(str(IM.REPO / "research" / "*" / "*" / "*" / "ipo"))):
            got, val_only = resolve_run(run)
            if val_only:
                continue
            days += 1
            rows += [dict(r, run=str(Path(run).relative_to(IM.REPO))) for r in got]
        doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "runs": days, "stats": stats(rows, floor), "rows": rows}
        out = Path(a.out) if a.out else IM.REPO / "researcher_ipo" / "analysis" / "pooled-resolved.json"
    else:
        if not a.run:
            sys.exit("--run or --pool")
        rows, val_only = resolve_run(a.run)
        doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "run": a.run, "validation_only": val_only, "conviction_floor": floor,
               "stats": stats(rows, floor), "rows": rows,
               "note": "One run is an anecdote, and at about one name a day this stage is "
                       "judged pooled: --pool."}
        if rows and all(r.get("move_pending") for r in rows):
            doc["warning"] = "every row is move_pending: resolve again after the session closes"
        out = Path(a.out) if a.out else Path(a.run) / "ipo-resolved.json"
    out.write_text(json.dumps(doc, indent=1, default=str) + "\n")
    print(json.dumps(doc["stats"], indent=1))


if __name__ == "__main__":
    main()
