#!/usr/bin/env python3
"""Did the release happen, what did the stock do, and did the ranking predict it.

Three jobs in that order, because the first gates the other two. Same shape as
`jp_resolve.py` and `edge_resolve.py` so the four markets' numbers mean the same thing,
with four Canadian additions that exist because of what SOURCES.md measured.

1. CONFIRM, AND NEVER CONFIRM A FUTURE DATE. Two archives, both ticker-keyed: a
   financial-results headline on the TMX news feed, or an interim/annual financial
   statement filed on SEDAR+ within three days. Either confirms. Neither, on a date
   that has passed, sets `event_occurred: false` -- the retrospective kill the US stage
   added after TRT was ranked, traded and never reported. On a date that has NOT passed
   nothing is written at all, because stage EU shipped the mirror-image bug: it resolved
   a forward run, found nothing from the issuer for a day that had not happened and
   killed the name.

2. MEASURE. close(D) -> close(D+1) for amc, close(D-1) -> close(D) for bmo, off TMX's
   own tape. The window is stage E's, deliberately, although nobody chose it on evidence
   in any market.

3. RANK, AND RANK THE ARMS APART. This is the part Canada is for. Every other stage
   reports one Spearman; this one reports it for the option-anchored names and the
   register-anchored names separately, because Canada is the only market in the repo
   where both regimes run inside one day's names. `archive/backtest/FINDINGS.md`
   section 33 priced the anchor-less regime at rho=+0.073 over 104 events and could not
   tell the anchor from the market. Here the market is held fixed.

   It also reports by `date_confidence`, which turns the open question "which of the two
   calendars is right" into a measurement that accumulates on its own: if `confirmed`
   and `agreed` rows resolve and `vendor_only` rows do not, the vendor half of the
   universe is noise and the floor should move.

   And it reports `lean_vs_free_control_rho`. Stage J carries the same number for the
   same reason: if it climbs to 1.0 the positioning components have stopped resolving
   and `priced_lean_pct` has silently become the free control again, which is the defect
   that makes Spain and Poland unable to beat their own benchmark.
"""
import argparse
import json
import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_market as M                                   # noqa: E402
import ca_sources as CA                                 # noqa: E402

FIN_FILING = ("financial statement", "interim", "annual report", "md&a",
              "management's discussion", "52-109", "results")


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
    return round(num / (dx * dy), 3) if dx and dy else None


def perm_p(xs, ys, rho, iters=10000, seed=7):
    if rho is None:
        return None
    rng = random.Random(seed)
    ys = list(ys)
    hits = 0
    for _ in range(iters):
        rng.shuffle(ys)
        r = spearman(xs, ys)
        if r is not None and abs(r) >= abs(rho):
            hits += 1
    return round((hits + 1) / (iters + 1), 4)


def closes(ticker, start, end):
    """{date: close} off TMX's own tape, padded either side so a holiday cannot make a
    window unmeasurable."""
    lo = (date.fromisoformat(start) - timedelta(days=12)).isoformat()
    hi = (date.fromisoformat(end) + timedelta(days=12)).isoformat()
    try:
        rows = CA.bars(ticker, lo, hi)
    except Exception:
        return {}
    return {(r.get("dateTime") or "")[:10]: r.get("close")
            for r in rows if r.get("close") is not None}


def on_or_before(cl, d):
    ks = sorted(k for k in cl if k <= d)
    return (ks[-1], cl[ks[-1]]) if ks else (None, None)


def confirm(ticker, event_date):
    """(event_occurred, note). None means "not settled", never "did not happen"."""
    today = datetime.now(timezone.utc).date().isoformat()
    if event_date >= today:
        return None, (f"{event_date} has not passed; nothing is checked. Resolving a "
                      f"forward date is how stage EU killed two names that had not "
                      f"reported yet.")
    try:
        news = CA.news_pages(ticker, pages=2, limit=100)
    except Exception as exc:
        return None, f"archive unreadable: {exc}"
    for n in news:
        d = (n.get("datetime") or "")[:10]
        h = n.get("headline") or ""
        if d in (event_date, M.next_session(event_date).isoformat()) \
           and M.is_financial_headline(h) and not M.ANNOUNCEMENT_HEADLINE.search(h):
            return True, f"wire: {h[:110]} ({n.get('source')}, {n.get('datetime')})"
    d0 = (date.fromisoformat(event_date) - timedelta(days=3)).isoformat()
    d1 = (date.fromisoformat(event_date) + timedelta(days=3)).isoformat()
    try:
        fil = CA.filings(ticker, d0, d1, 40)
    except Exception:
        fil = []
    for f in fil:
        txt = f"{f.get('description') or ''} {f.get('name') or ''}".lower()
        if any(k in txt for k in FIN_FILING):
            return True, (f"SEDAR+ filing {f.get('filingDate')}: "
                          f"{f.get('description')} / {f.get('name')}")
    if news or fil:
        return False, ("no financial-results release on the wire and no interim or "
                       "annual financial filing on SEDAR+ within three days. Both "
                       "archives answered, so this is an absence and not a failed fetch.")
    return None, "both archives returned nothing at all; treat as unsettled, not absent"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the day's run directory")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    run = Path(a.run)
    scores = json.loads((run / "edge-scores.json").read_text())
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        baselines[f.stem.upper()] = json.loads(f.read_text())

    rows = []
    # `names` in edge-scores.json is a COUNT, not a list. The rows are under `ranking`.
    ranking = scores.get("ranking") or scores.get("rows") or []
    for r in ranking:
        if not isinstance(r, dict):
            continue
        t = (r.get("ticker") or "").upper()
        b = baselines.get(t) or {}
        ed = b.get("event_date") or scores.get("event_date")
        sess = b.get("session") or "amc"
        if not ed:
            continue
        w0, w1 = M.window(ed, sess)
        cl = closes(t, w0, w1)
        d0, c0 = on_or_before(cl, w0)
        d1, c1 = on_or_before(cl, w1)
        move = round((c1 / c0 - 1) * 100, 3) if (c0 and c1 and d1 != d0) else None
        occurred, note = confirm(t, ed)
        rows.append({
            "ticker": t, "company": b.get("company"), "event_date": ed, "session": sess,
            "impact_sum": r.get("impact_sum"), "conviction": r.get("conviction"),
            "rankable": r.get("rankable"),
            "impact_sum_pre_lessons": (r.get("diagnostics") or {}).get("impact_sum_pre_lessons"),
            "anchor_covered": b.get("anchor_covered"),
            "date_confidence": (b.get("event_plausibility") or {}).get("date_confidence"),
            "event_shape": (b.get("event_plausibility") or {}).get("event_shape"),
            "priced_lean_pct": b.get("priced_lean_pct"),
            "lean_components": b.get("lean_components"),
            "run_up_20d_pct": (b.get("tape") or {}).get("run_up_20d_pct"),
            "implied_move_pct": (b.get("options") or {}).get("event_implied_move_pct"),
            "entry_date": d0, "entry": c0, "exit_date": d1, "exit": c1,
            "realised_move_pct": move,
            "move_pending": move is None,
            "event_occurred": occurred, "event_occurred_note": note,
        })

    ok = [r for r in rows if r["realised_move_pct"] is not None
          and r["impact_sum"] is not None and r["rankable"]
          and r["event_occurred"] is not False]

    def rank_block(sample, key=lambda r: r["impact_sum"], label="impact_sum"):
        xs = [key(r) for r in sample if key(r) is not None]
        ys = [r["realised_move_pct"] for r in sample if key(r) is not None]
        if len(xs) < 3:
            return {"n": len(xs), "spearman": None, "note": "fewer than 3 resolved names"}
        rho = spearman(xs, ys)
        signs = sum(1 for x, y in zip(xs, ys) if x * y > 0)
        return {"n": len(xs), "key": label, "spearman": rho,
                "permutation_p": perm_p(xs, ys, rho),
                "sign_right": signs, "sign_rate": round(signs / len(xs), 3),
                "mean_signed_return_pct": round(
                    sum((y if x > 0 else -y) for x, y in zip(xs, ys)) / len(xs), 3)}

    out = {
        "market": "CA",
        "run": str(run),
        "resolved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "names": len(rows),
        "resolved": len(ok),
        "pending": sum(1 for r in rows if r["move_pending"]),
        "killed_event_occurred_false": sum(1 for r in rows if r["event_occurred"] is False),
        "median_abs_move_pct": round(median([abs(r["realised_move_pct"]) for r in ok]), 2)
                               if ok else None,
        "overall": rank_block(ok),
        "pre_lessons": rank_block(ok, lambda r: r.get("impact_sum_pre_lessons"),
                                  "impact_sum_pre_lessons"),
        "free_control": rank_block(
            ok, lambda r: (-r["run_up_20d_pct"] if r["run_up_20d_pct"] is not None else None),
            "-run_up_20d_pct"),
        "priced_lean": rank_block(ok, lambda r: r.get("priced_lean_pct"), "priced_lean_pct"),
        "by_anchor_covered": {
            k: rank_block([r for r in ok if r["anchor_covered"] == k])
            for k in ("options", "register", "none")},
        "by_date_confidence": {
            k: rank_block([r for r in ok if r["date_confidence"] == k])
            for k in ("confirmed", "agreed", "wsh_only", "vendor_only", "disputed")},
        "by_session": {k: rank_block([r for r in ok if r["session"] == k])
                       for k in ("amc", "bmo")},
        "rows": rows,
    }

    # Is the lean still a real rival to the free control, or has it silently become it?
    lean = [(r["priced_lean_pct"], -r["run_up_20d_pct"]) for r in ok
            if r.get("priced_lean_pct") is not None and r["run_up_20d_pct"] is not None]
    out["lean_vs_free_control_rho"] = (
        spearman([x for x, _ in lean], [y for _, y in lean]) if len(lean) >= 3 else None)
    out["lean_vs_free_control_note"] = (
        "1.0 means priced_lean_pct IS -run_up_20d_pct, so the baseline's direction and "
        "its own benchmark are one number and the hunt cannot beat the control with "
        "anything built on it. That is the state Spain and Poland are in permanently.")

    # Each lean component ranked on its own, so the priors can be replaced by measurement.
    comps = {}
    for k in ("option_lean", "short_squeeze", "short_building", "days_to_cover",
              "analyst_gap", "runup"):
        s = [r for r in ok if (r.get("lean_components") or {}).get(k) is not None]
        comps[k] = rank_block(s, lambda r, k=k: r["lean_components"][k], k)
    out["lean_components"] = comps

    text = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text[:4000])
    o = out["overall"]
    print(f"{out['resolved']} resolved of {out['names']} "
          f"({out['pending']} pending, {out['killed_event_occurred_false']} killed) | "
          f"rho={o.get('spearman')} p={o.get('permutation_p')} "
          f"vs free control {out['free_control'].get('spearman')} | "
          f"options arm {out['by_anchor_covered']['options'].get('spearman')} "
          f"register arm {out['by_anchor_covered']['register'].get('spearman')}")
    if a.out:
        print(f"-> {a.out}")


if __name__ == "__main__":
    main()
