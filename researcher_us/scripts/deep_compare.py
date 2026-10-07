#!/usr/bin/env python3
"""Stage D against stage E and E-P, on the same names, pooled over every resolved day.

Stage D researches three names a day, drawn at random from what stage E hunts, so each
pick also carries a stage E `impact_sum` and an E-P `panel_score`. Three names cannot be
ranked within a day, so this script pools NAMES across days and asks per arm:

- sign: of the names the arm gave a non-zero sign, how many moved that way (one-sided
  binomial p against a coin);
- book: the mean of sign(score) x realised move, the return of trading the sign, with t;
- rank: Spearman rho of the score against the realised move over all pooled names, with a
  permutation p. Pooled across days, not within them, so a market day moves it.

And, paired on the same names, whether deep beats each other arm on sign (exact McNemar on
the names where they disagree). The arms:

    deep          stage D's impact_sum, the key (sum of its findings)
    deep_scaled   stage D's (2 x p_up/100 - 1) x abs_move_pct
    deep_quick    stage D's frozen quick first read (pre_research.impact_sum_pct): the
                  depth control, same model and name with the depth taken away
    stage_e       stage E's impact_sum on the same name, same day
    ep_panel      stage E-P's panel_score on the same name, same day
    neg_runup20   minus the 20-day run-up from stage D's own sealed baseline, the free control

The realised move is edge_resolve.realised(): close before the print to close after the
first full session. Fetched moves are cached in <RUN>/edge-deep/deep-outcome.json.

    python3 researcher_us/scripts/deep_compare.py                       # every edge-deep run
    python3 researcher_us/scripts/deep_compare.py --offline             # cache only
    python3 researcher_us/scripts/deep_compare.py --questions-template --run <RUN>/edge-deep

`--questions-template` writes <RUN>/edge-deep/question-verdicts.json with one row per
frozen question, to be filled after the print (from the release and the reaction, never
before): `was_the_line` (did the reaction turn on this question), `answered_right` (did
the release answer it the way stage D said) and, per name, `missed_line` (what the stock
did trade on, if no question named it). The pooled report reads every filled file.

Research only. At three names a day this is too small to tell anything for weeks; the
script says so rather than printing a verdict.
"""
import argparse
import glob
import json
import math
import sys
from datetime import datetime, timezone
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from edge_stats import spearman_perm, tstat, binom_ge  # noqa: E402

ARMS = ("deep", "deep_scaled", "deep_quick", "stage_e", "ep_panel", "neg_runup20")
MIN_N = 20  # below this, print the counts and say the sample is too small


def load(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return None


def by_ticker(rows, key):
    out = {}
    for r in rows or []:
        t = (r.get("ticker") or "").upper()
        if t and r.get("rankable", True) is not False and isinstance(r.get(key), (int, float)):
            out[t] = r[key]
    return out


def collect_run(deep_dir, fetch):
    deep_dir = Path(deep_dir)
    day = deep_dir.parent
    scores = load(deep_dir / "edge-scores.json") or {}
    deep = by_ticker(scores.get("ranking"), "impact_sum")
    e = by_ticker((load(day / "edge" / "edge-scores.json") or {}).get("ranking"), "impact_sum")
    ep = by_ticker((load(day / "edge-panel" / "edge-scores-panel.json") or {}).get("ranking"),
                   "panel_score")
    cache_path = deep_dir / "deep-outcome.json"
    cache = load(cache_path) or {}
    rows, changed = [], False
    for t in sorted(deep):
        hunt = load(deep_dir / "hunts" / f"{t}.json") or {}
        base = load(deep_dir / "baselines" / f"{t}.json") or {}
        pre = hunt.get("pre_research") or {}
        p_up, absm = hunt.get("p_up"), hunt.get("abs_move_pct")
        row = {"day": day.name, "ticker": t,
               "deep": deep[t],
               "deep_scaled": ((2 * p_up / 100 - 1) * absm
                               if isinstance(p_up, (int, float)) and isinstance(absm, (int, float))
                               else None),
               "deep_quick": pre.get("impact_sum_pct"),
               "stage_e": e.get(t), "ep_panel": ep.get(t),
               "neg_runup20": (-(base.get("tape") or {}).get("run_up_20d_pct")
                               if isinstance((base.get("tape") or {}).get("run_up_20d_pct"),
                                             (int, float)) else None),
               "abs_move_pct": absm}
        res = cache.get(t)
        if res is None and fetch and base.get("event_date"):
            try:
                from edge_resolve import realised
                res, err = realised(t, base["event_date"], base.get("session", "bmo"))
            except Exception as exc:
                res, err = None, f"price fetch failed: {type(exc).__name__}"
            if res:
                cache[t] = res
                changed = True
            else:
                row["pending"] = err
        if res:
            row["move_pct"] = res["move_pct"]
        rows.append(row)
    if changed:
        cache_path.write_text(json.dumps(cache, indent=1) + "\n", encoding="utf-8")
    verdicts = load(deep_dir / "question-verdicts.json")
    return rows, verdicts


def sgn(x):
    return (x > 0) - (x < 0)


def arm_stats(rows, arm):
    live = [r for r in rows if r.get("move_pct") is not None and r.get(arm) is not None]
    signed = [r for r in live if sgn(r[arm]) != 0]
    hits = sum(1 for r in signed if sgn(r[arm]) == sgn(r["move_pct"]))
    book = [sgn(r[arm]) * r["move_pct"] for r in signed]
    out = {"n": len(live), "n_signed": len(signed), "sign_hits": hits,
           "sign_p_one_sided": round(binom_ge(hits, len(signed)), 4) if signed else None,
           "book_mean_pct": round(sum(book) / len(book), 2) if book else None,
           "book_t": round(tstat(book), 2) if len(book) > 1 and not math.isnan(tstat(book)) else None}
    if len(live) >= 3:
        rho, p = spearman_perm([r[arm] for r in live], [r["move_pct"] for r in live])
        out["rho"] = None if math.isnan(rho) else round(rho, 3)
        out["rho_p"] = None if math.isnan(p) else round(p, 4)
    return out


def mcnemar(rows, a, b):
    """Exact two-sided McNemar on the names both arms signed: does `a` get the sign right
    where `b` gets it wrong more often than the reverse?"""
    both = [r for r in rows if r.get("move_pct") is not None and r.get(a) is not None
            and r.get(b) is not None and sgn(r[a]) and sgn(r[b])]
    ra = [sgn(r[a]) == sgn(r["move_pct"]) for r in both]
    rb = [sgn(r[b]) == sgn(r["move_pct"]) for r in both]
    a_only = sum(1 for x, y in zip(ra, rb) if x and not y)
    b_only = sum(1 for x, y in zip(ra, rb) if y and not x)
    d = a_only + b_only
    p = (min(1.0, 2 * sum(comb(d, i) for i in range(0, min(a_only, b_only) + 1)) * 0.5 ** d)
         if d else None)
    return {"n_both_signed": len(both), "agree_sign": sum(1 for r in both if sgn(r[a]) == sgn(r[b])),
            f"{a}_right_{b}_wrong": a_only, f"{b}_right_{a}_wrong": b_only,
            "p_two_sided": round(p, 4) if p is not None else None}


def question_stats(all_verdicts):
    qs, names, line_named = [], 0, 0
    for v in all_verdicts:
        for name in (v or {}).get("names", []):
            filled = [q for q in name.get("questions", []) if q.get("was_the_line") is not None]
            if not filled:
                continue
            names += 1
            if any(q.get("was_the_line") for q in filled):
                line_named += 1
            qs.extend(filled)
    ans = [q for q in qs if q.get("answered_right") is not None]
    return {"names_scored": names, "names_where_a_frozen_question_was_the_line": line_named,
            "questions_scored": len(qs),
            "questions_answered_right": sum(1 for q in ans if q["answered_right"]),
            "questions_with_answer_scored": len(ans),
            "line_questions_answered_right": sum(1 for q in ans if q.get("was_the_line")
                                                 and q["answered_right"]),
            "line_questions_scored": sum(1 for q in ans if q.get("was_the_line"))}


def template(deep_dir):
    deep_dir = Path(deep_dir)
    names = []
    for f in sorted((deep_dir / "hunts").glob("*.json")):
        h = load(f) or {}
        frozen = h.get("questions_frozen") or []
        answers = {q.get("id"): q for q in h.get("key_questions") or []}
        names.append({"ticker": (h.get("ticker") or f.stem).upper(),
                      "missed_line": None,
                      "questions": [{"id": q.get("id"), "question": q.get("question"),
                                     "answer_given": (answers.get(q.get("id")) or {}).get("answer"),
                                     "was_the_line": None, "answered_right": None,
                                     "evidence_after_print": None}
                                    for q in frozen]})
    out = deep_dir / "question-verdicts.json"
    if out.exists():
        sys.exit(f"{out} exists; not overwriting a filled verdict file")
    out.write_text(json.dumps({"filled_utc": None, "names": names}, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out}: {sum(len(n['questions']) for n in names)} questions on {len(names)} names")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pool", default="research/2026/*/*/edge-deep")
    ap.add_argument("--run", help="one edge-deep dir (for --questions-template)")
    ap.add_argument("--offline", action="store_true", help="read cached moves only")
    ap.add_argument("--questions-template", action="store_true")
    ap.add_argument("-o", help="write the report JSON here")
    a = ap.parse_args()
    if a.questions_template:
        if not a.run:
            sys.exit("--questions-template needs --run")
        return template(a.run)

    runs = [a.run] if a.run else sorted(glob.glob(a.pool))
    rows, verdicts = [], []
    for r in runs:
        rr, v = collect_run(r, not a.offline)
        rows += rr
        verdicts.append(v)
    live = [r for r in rows if r.get("move_pct") is not None]
    report = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "runs": runs, "names": len(rows), "resolved": len(live),
              "days": len({r["day"] for r in live}),
              "arms": {arm: arm_stats(rows, arm) for arm in ARMS},
              "paired_sign": {f"deep_vs_{b}": mcnemar(rows, "deep", b)
                              for b in ("deep_quick", "stage_e", "ep_panel")},
              "questions": question_stats(verdicts),
              "too_small": len(live) < MIN_N,
              "rows": rows}

    print(f"stage D: {len(rows)} names over {len(runs)} runs, {len(live)} resolved "
          f"on {report['days']} days")
    if report["too_small"]:
        print(f"  n={len(live)} < {MIN_N}: too small to tell anything; counts only")
    print(f"  {'arm':12s}{'n':>4s}{'sign':>9s}{'p':>8s}{'book':>8s}{'t':>7s}{'rho':>8s}{'p':>8s}")
    for arm, s in report["arms"].items():
        sign = f"{s['sign_hits']}/{s['n_signed']}" if s["n_signed"] else "--"
        f = lambda v, fmt: (fmt % v) if v is not None else "--"
        print(f"  {arm:12s}{s['n']:>4d}{sign:>9s}{f(s['sign_p_one_sided'], '%.3f'):>8s}"
              f"{f(s['book_mean_pct'], '%+.2f'):>8s}{f(s['book_t'], '%.2f'):>7s}"
              f"{f(s.get('rho'), '%+.3f'):>8s}{f(s.get('rho_p'), '%.3f'):>8s}")
    for k, m in report["paired_sign"].items():
        other = k.split("_vs_", 1)[1]
        print(f"  {k}: both signed {m['n_both_signed']}, agree {m['agree_sign']}, "
              f"deep-only right {m['deep_right_' + other + '_wrong']}, "
              f"{other}-only right {m[other + '_right_deep_wrong']}, McNemar p {m['p_two_sided']}")
    q = report["questions"]
    if q["names_scored"]:
        print(f"  questions: a frozen question was the line on {q['names_where_a_frozen_question_was_the_line']}"
              f"/{q['names_scored']} names; answered right {q['questions_answered_right']}"
              f"/{q['questions_with_answer_scored']} (on the line: {q['line_questions_answered_right']}"
              f"/{q['line_questions_scored']})")
    else:
        print("  questions: no question-verdicts.json filled yet")
    if a.o:
        Path(a.o).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
