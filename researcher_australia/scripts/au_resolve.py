#!/usr/bin/env python3
"""Score a finished Australian run against what the stock actually did.

Same job as `researcher_us/scripts/edge_resolve.py` and `jp_resolve.py`: take the
ranking a run emitted, take the realised move over the window the baseline sealed, and
report whether the two are related. Nothing here changes a score; it only measures one.

FOUR THINGS THIS REPORTS THAT THE US RESOLVER DOES NOT
-------------------------------------------------------
1. `lean_vs_free_control_rho`. Australia has no option anchor, so `priced_lean_pct` is
   built out of ASIC's short register plus the run-up. If the register stops resolving,
   the lean quietly becomes `-0.05 * run_up_20d_pct` -- which IS the free control -- and
   the baseline's lean and its own benchmark are one number again. That failure is
   invisible in the ranking itself, so it is reported as a correlation: a value near 1.0
   means the anchor is gone, not that it is working.

2. `by_filer_type`. Half the ASX lodges an Appendix 4C or 5B quarterly activities
   report rather than a 4D or 4E profit result. Those are different events with
   different bars, and pooling them without saying so would hide it. Spearman, sign
   rate and count in each arm.

3. `components`. Every term in the lean is ranked separately against the realised move,
   because the weights in `au_priced_in.lean_components()` are priors carried over from
   Tokyo with no Australian measurement behind them. They are meant to be replaced by
   what this table says, not defended.

4. `by_anchor_covered` is deliberately ABSENT, and that absence is the point. Stage EU
   needs it because a name missing from the FCA register might be at 0.49% or at zero.
   ASIC's register is not truncated, so an absent product is a measured zero and there
   is no second arm to split out.

IT REFUSES TO CONFIRM A FUTURE DATE
------------------------------------
Stage EU shipped a resolver that read the day archives for a date that had not happened,
found nothing from the issuer and wrote `event_occurred: false` -- killing names that
simply had not reported yet, which is the TRT mistake with the sign flipped. This one
refuses to settle `event_occurred` for any date at or after today in Sydney, and says
`pending` instead.

YAHOO'S AUSTRALIAN BARS CAN LAG
--------------------------------
Stage EU measured null closes on `.PA` and `.DE` for sessions that had already happened.
Every row therefore carries `last_bar_date` and `move_pending`, and the summary warns
when every row is pending, so a day that cannot be resolved yet is never read as a day
on which nothing moved.
"""
import argparse
import json
import random
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import au_market as M                                              # noqa: E402
import au_priced_in as PI                                          # noqa: E402


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return round(num / (dx * dy), 4) if dx and dy else None


def perm_p(xs, ys, rho, iters=20000, seed=0):
    if rho is None:
        return None
    rng = random.Random(seed)
    ys = list(ys)
    hit = 0
    for _ in range(iters):
        rng.shuffle(ys)
        r = spearman(xs, ys)
        if r is not None and abs(r) >= abs(rho):
            hit += 1
    return round((hit + 1) / (iters + 1), 4)


def closes(code):
    rows, _, url = PI.bars(code)
    return {r["d"].isoformat(): r["c"] for r in rows}, url


def realised(code, window):
    """The move over the sealed window, off daily closes.

    Never off the sealed spot: the spot is an intraday or close price struck when the
    baseline was written, and using it would mix two price sources in one number.
    """
    by_date, url = closes(code)
    if not by_date:
        return {"move_pct": None, "reason": "no bars", "source": url}
    dates = sorted(by_date)
    a, b = window.get("from_close"), window.get("to_close")
    if a not in by_date:
        prior = [d for d in dates if d <= a]
        if not prior:
            return {"move_pct": None, "reason": f"no bar at or before {a}",
                    "last_bar_date": dates[-1], "source": url}
        a = prior[-1]
    if b not in by_date:
        return {"move_pct": None, "reason": f"no bar for {b}", "move_pending": True,
                "last_bar_date": dates[-1], "source": url}
    c0, c1 = by_date[a], by_date[b]
    return {"move_pct": round((c1 / c0 - 1) * 100, 3), "from_close": a, "to_close": b,
            "from_price": c0, "to_price": c1, "last_bar_date": dates[-1],
            "move_pending": False, "source": url}


def occurred(code, event_date, today_syd):
    """Did a print actually land? Only answerable once the date has passed."""
    ed = date.fromisoformat(event_date)
    if ed >= today_syd:
        return {"event_occurred": None, "state": "pending",
                "note": f"{event_date} is not in the past in Sydney; refusing to "
                        f"confirm or kill a future date."}
    anns, url = PI.announcements(code, ed.year)
    if not anns:
        return {"event_occurred": None, "state": "archive_unreadable",
                "note": "the ASX per-issuer archive returned nothing, which is not the "
                        "same as the issuer lodging nothing", "source": url}
    same = [(d, m, h) for d, m, h in anns if abs((d - ed).days) <= 1]
    hits = [(d, m, h) for d, m, h in same if PI.classify(h)]
    if hits:
        d, m, h = sorted(hits)[0]
        return {"event_occurred": True, "state": "confirmed",
                "confirmed_date": d.isoformat(),
                "confirmed_local": f"{m // 60:02d}:{m % 60:02d}",
                "confirmed_kind": PI.classify(h), "headline": h[:90], "source": url}
    if same:
        return {"event_occurred": None, "state": "announced_unclassified",
                "note": f"{len(same)} announcements within a day of {event_date}, none "
                        f"classified as a print. The UK measurement found six of eight "
                        f"such cases were classifier gaps, so this is NOT a phantom.",
                "headlines": [h[:70] for _, _, h in same[:5]], "source": url}
    return {"event_occurred": False, "state": "no_announcement",
            "note": "the issuer lodged nothing within a day of the scheduled date",
            "source": url}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="a run directory holding "
                                                 "edge-scores.json and baselines/")
    ap.add_argument("-o", "--out")
    ap.add_argument("--no-confirm", action="store_true")
    a = ap.parse_args()

    run = Path(a.run)
    scores = json.loads((run / "edge-scores.json").read_text(encoding="utf-8"))
    today_syd = datetime.now(M.SYD).date()
    # edge-scores.json carries no event_date of its own; the universe does.
    up = run / "universe.json"
    event_date = (json.loads(up.read_text(encoding="utf-8")).get("event_date")
                  if up.exists() else None)

    # `ranking`, not `ranked`. edge_score.py's own key -- reading a remembered
    # contract instead of the file is how a resolver silently reports zero rows.
    ranked = scores.get("ranking") or []
    if not ranked:
        raise SystemExit(f"{run}/edge-scores.json has no `ranking` rows")

    rows = []
    for r in ranked:
        if not r.get("rankable", True):
            continue
        t = r["ticker"]
        bp = run / "baselines" / f"{t}.json"
        b = json.loads(bp.read_text(encoding="utf-8")) if bp.exists() else {}
        w = b.get("window_dates") or {}
        mv = realised(t, w) if w else {"move_pct": None, "reason": "no window"}
        row = {
            "ticker": t,
            "company": b.get("company"),
            "session": b.get("session"),
            "session_unresolved": b.get("session_unresolved"),
            "filer_type": (b.get("history") or {}).get("filer_type"),
            "impact_sum": r.get("impact_sum"),
            "impact_sum_pre_lessons": (r.get("diagnostics") or {}).get("impact_sum_pre_lessons"),
            "conviction": r.get("conviction"),
            "priced_lean_pct": b.get("priced_lean_pct"),
            "lean_components": b.get("lean_components") or {},
            "run_up_20d_pct": (b.get("tape") or {}).get("run_up_20d_pct"),
            "run_up_5d_pct": (b.get("tape") or {}).get("run_up_5d_pct"),
            "short_pct": (b.get("positioning") or {}).get("short_pct"),
            "register_lag_sessions": (b.get("positioning") or {}).get("lag_sessions"),
            "window": w,
            **mv,
        }
        if not a.no_confirm:
            row.update(occurred(t, b.get("event_date") or event_date, today_syd))
        rows.append(row)

    live = [r for r in rows
            if r.get("move_pct") is not None and r.get("event_occurred") is not False]
    pending = [r for r in rows if r.get("move_pending")]

    def rank_against(getter, label, invert=False):
        pairs = [(getter(r), r["move_pct"]) for r in live if getter(r) is not None]
        if len(pairs) < 3:
            return {"label": label, "n": len(pairs), "rho": None, "p": None}
        xs = [(-x if invert else x) for x, _ in pairs]
        ys = [y for _, y in pairs]
        rho = spearman(xs, ys)
        return {"label": label, "n": len(pairs), "rho": rho,
                "p": perm_p(xs, ys, rho)}

    out = {
        "market": "AU",
        "run": str(run),
        "event_date": event_date,
        "resolved_utc": datetime.now(M.UTC).isoformat(timespec="seconds"),
        "n_ranked": len(rows),
        "n_resolved": len(live),
        "n_move_pending": len(pending),
        "n_killed_event_occurred_false": sum(1 for r in rows
                                             if r.get("event_occurred") is False),
        "rankers": {
            "impact_sum": rank_against(lambda r: r["impact_sum"], "the hunt"),
            "impact_sum_pre_lessons": rank_against(
                lambda r: r["impact_sum_pre_lessons"], "the hunt before LESSONS.md"),
            "priced_lean_pct": rank_against(lambda r: r["priced_lean_pct"],
                                            "the sealed lean"),
            "free_control_runup_20d": rank_against(lambda r: r["run_up_20d_pct"],
                                                   "-run_up_20d_pct", invert=True),
            "free_control_runup_5d": rank_against(lambda r: r["run_up_5d_pct"],
                                                  "-run_up_5d_pct", invert=True),
        },
        "components": {
            k: rank_against(lambda r, k=k: r["lean_components"].get(k), k)
            for k in ("short_squeeze", "short_building", "runup")
        },
        "by_filer_type": {
            k: {"n": len([r for r in live if r["filer_type"] == k]),
                "rho": spearman([r["impact_sum"] for r in live
                                 if r["filer_type"] == k and r["impact_sum"] is not None],
                                [r["move_pct"] for r in live
                                 if r["filer_type"] == k and r["impact_sum"] is not None]),
                "sign_right": sum(1 for r in live if r["filer_type"] == k
                                  and r["impact_sum"] and
                                  (r["impact_sum"] > 0) == (r["move_pct"] > 0))}
            for k in ("results", "quarterly_report_only", "none_found")
        },
        "rows": sorted(rows, key=lambda r: -(r.get("impact_sum") or 0)),
    }

    # THE ALARM. If the lean has collapsed back onto the free control, the register
    # stopped resolving and the baseline has no independent directional content --
    # which is invisible in the ranking itself.
    leans = [(r["priced_lean_pct"], -(r["run_up_20d_pct"] or 0)) for r in rows
             if r["priced_lean_pct"] is not None and r["run_up_20d_pct"] is not None]
    # MINIMUM FIVE NAMES, and that is not fussiness. On three names a rank correlation
    # of exactly 1.0 happens by chance one time in six, and the first synthetic AU run
    # duly produced one -- which, read as the alarm below describes, says the register
    # has failed when it resolved for every name. A thin Australian day outside the
    # February and August seasons is NORMAL, so this would have fired regularly and
    # somebody would eventually have written it down as a fact.
    n_lean = len(leans)
    lvc = (spearman([x for x, _ in leans], [y for _, y in leans])
           if n_lean >= 5 else None)
    out["lean_vs_free_control_rho"] = lvc
    out["lean_vs_free_control_n"] = n_lean
    out["lean_vs_free_control_note"] = (
        "Near 1.0 means ASIC's register stopped resolving and priced_lean_pct has "
        "collapsed back onto -run_up_20d_pct, which IS the free control -- a source "
        "failure wearing the costume of a working anchor. Stage J's healthy range "
        "after its positioning anchors shipped was 0.446-0.59; the run-up is a "
        "component of the lean, so some correlation is structural and only a value "
        "near 1.0 is the alarm. Reported as null below five names, because on three "
        "a 1.0 is a coin toss and not a finding."
        if n_lean >= 5 else
        f"Not computed: only {n_lean} name(s) carried both a lean and a run-up, and "
        f"below five a rank correlation of 1.0 arises by chance often enough to be "
        f"meaningless. This is NOT evidence that the register is working or failing. "
        f"Read positioning.covered on the baselines instead.")

    if pending and len(pending) == len(rows):
        out["warning"] = ("EVERY row is move_pending: Yahoo has no bar yet for the "
                          "close that ends the window. This is a data lag, NOT a day "
                          "on which nothing moved. Re-run tomorrow.")

    text = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(text + "\n", encoding="utf-8")
        h = out["rankers"]["impact_sum"]
        print(f"{out['event_date']}: {out['n_resolved']}/{out['n_ranked']} resolved, "
              f"hunt rho={h['rho']} p={h['p']} (n={h['n']}), "
              f"control rho={out['rankers']['free_control_runup_20d']['rho']}, "
              f"lean_vs_control={lvc} -> {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
