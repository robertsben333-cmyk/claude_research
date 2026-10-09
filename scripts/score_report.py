#!/usr/bin/env python3
"""The table every hunt stage pastes, verbatim, into its closing chat reply.

Since 2026-10-01 every hunter answers twice, and the reply carries both answers side
by side so nobody has to open a file to see them:

  impact_sum     version 2, THE KEY. Each finding sized on its own, added up. This is
                 what ranks the day, what the 3.0 conviction floor was measured on and,
                 for stage E only, what trades. From edge-scores.json.
  impact_scaled  version 3. (2 * p_up / 100 - 1) * abs_move_pct, the hunter's second,
                 separate measurement of the whole print. From edge-scores-scaled.json,
                 its own file. Not ranked on, not traded, never pooled with the key.
  V2             US only (stages E, E-S and E-P): the grounded score from
                 edge-scores-grounded.json, at its primary horizon. Shown as
                 "not run" when the file is absent, never left out silently.
  retail, search, vol
                 US only, since 2026-10-02: CONTEXT, NOT A SCORE. Whether the name has
                 a retail tilt >= 50, a quiet Google search spike (< 1.0x) and a 20-day
                 realised volatility >= 58% (frozen), from
                 researcher_us/scripts/edge_context.py's edge-context.json, for every
                 name whatever its score. Nothing ranks, selects, sizes or trades on
                 them (operator's instruction). "not run" when the file is absent.

Each of the two numbers carries a percentile in brackets, e.g. `+3.40 (p87)`: the share
of reference names sized by the SAME model whose |value| sits below this one's (ties
count half). Under 20 reference names the bracket reads `n<20`. It describes SIZE against
that model's own habit, not rank within the day and not a probability. The reference set
per model has two parts:

  live runs     every rankable name in research/<date>/<stage>/ up to this run's date,
                model from provenance.for_row, every stage pooled, synthetic validation
                runs and the run itself left out. impact_scaled from
                edge-scores-scaled.json once live runs write it.
  evaluations   the blind re-judges already run over resolved names (EVALUATIONS):
                Opus 5.5 under the two-measurement core (rejudge-opus55-v2-sizing, both
                numbers) and Opus 5, Sonnet 5.5 and Fable 5.1 from rejudge-four-models
                (impact_scaled only: that brief made findings sum to the scaled number,
                so its impact_sum is not version 2). impact_scaled is recomputed as
                (2·p_up/100 − 1)·abs_move_pct, as edge_score.scaled_view does.

THE SEPTEMBER OPUS 5.5 HUNTS ARE LEFT OUT, from both parts (operator's instruction,
2026-10-01). Between the alias switch on 2026-09-22 and the shared hunter core, Opus 5.5
filed a third of what it surfaced and sized near zero; that prompt was a mistake, not a
habit to measure against. A live run counts as one when its hunter model is Opus 5.5 and
its provenance carries no `hunter_core` blob; an evaluation row is dropped when the live
hunt whose evidence it judged was one. The re-judges judge evidence only and ran below
live scale even on Opus 5 (rejudge-opus55-v2-sizing README), so a bracket read off them
is conservative about how large a live number is.

    python3 scripts/score_report.py --run research/2026/10/2026-10-02/edge
    python3 scripts/score_report.py --run <RUN>/europe --label "Stage EU"

Reads only; writes nothing. Exits 1 when the run has no edge-scores.json, so a
reply cannot quote a table that was never scored.
"""
import argparse
import json
import sys
from bisect import bisect_left, bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import provenance  # noqa: E402

US_DIRS = {"edge", "edge-sonnet", "edge-panel", "edge-deep"}
DIR_MARKET = {v["dir"]: k for k, v in provenance.MARKETS.items()}
MIN_HISTORY = 20


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def f(v, fmt="{:+.2f}"):
    return "n/a" if v is None else fmt.format(v)


def run_model(run, reg):
    """The hunter model that sized a run's names, or None. An alias whose served model
    nothing has observed (stage E-S's `sonnet`) is its own group, labelled `sonnet?`;
    an alias caught mid-switch (`opus` on 2026-09-22) is left out rather than guessed."""
    market = DIR_MARKET.get(Path(run).name)
    if not market:
        return None
    try:
        row = provenance.for_row(run, market, reg=reg)
    except Exception:  # a provenance hiccup must not cost the table
        return None
    if row.get("model"):
        return row["model"]
    return row.get("model_short") if row.get("model_basis") == "not_recorded" else None


def context_cells(ctx, ticker):
    """The two context columns for one name. `ctx` is edge-context.json or None."""
    if ctx is None:
        return ["not run", "not run", "not run"]
    c = next((n for n in ctx.get("names", []) if n.get("ticker") == ticker), None)
    if c is None:
        return ["n/a", "n/a", "n/a"]
    yn = {True: "yes", False: "no", None: "?"}
    rt = c.get("retail") or {}
    retail = (f"{yn[rt.get('favourable')]} ({rt['retail_tilt']:.0f})"
              if rt.get("retail_tilt") is not None else "n/a")
    se = c.get("search") or {}
    search = (f"{yn[se.get('favourable')]} ({se['spike']:.2f}x)"
              if se.get("spike") is not None else f"n/a ({se.get('state', '?')})")
    vo = c.get("vol") or {}
    vol = (f"{yn[vo.get('high')]} ({vo['realised_vol_20d']:.0f})"
           if vo.get("realised_vol_20d") is not None else "n/a")
    return [retail, search, vol]


def session_labels(run):
    """{ticker: 'amc' | 'bmo' | 'bmo?'} for one run. The sealed baseline carries the
    session; `?` marks one the sweep could not confirm (session_unresolved). A ticker
    with none (stage R screens fallers, not prints) is absent and reads `n/a`."""
    run = Path(run)
    out = {}
    for b in sorted((run / "baselines").glob("*.json")):
        d = load(b) or {}
        if d.get("session"):
            out[b.stem] = d["session"] + ("?" if d.get("session_unresolved") else "")
    u = load(run / "universe.json") or {}
    names = u.get("names") if isinstance(u.get("names"), list) else []
    for n in names:
        t = n.get("ticker") or n.get("symbol") or n.get("code")
        sess = n.get("session") or u.get("session")
        if t and sess and str(t) not in out:
            out[str(t)] = sess + ("?" if n.get("session_unresolved") else "")
    return out


def impact_of(r):
    """impact_sum; before 2026-09-09 it was not a top-level field and is the sum of the
    findings' sizes by definition, exactly as edge_sample.py re-derives it."""
    if r.get("impact_sum") is not None:
        return r["impact_sum"]
    fs = r.get("findings")
    return sum(x.get("expected_impact_pct") or 0 for x in fs) if fs else None


SEPT_OPUS55 = provenance.SEPT_OPUS55

# Blind re-judges of resolved names: (glob, model, which numbers count as reference).
EVALUATIONS = [
    ("research/analyses/rejudge-opus55-v2-sizing/out-*.json", "claude-opus-5-5",
     ("impact_sum", "impact_scaled")),
    ("research/analyses/rejudge-four-models/out-*-opus5.json", "claude-opus-5",
     ("impact_scaled",)),
    ("research/analyses/rejudge-four-models/out-*-sonnet.json", "claude-sonnet-5-5",
     ("impact_scaled",)),
    ("research/analyses/rejudge-four-models/out-*-fable.json", "claude-fable-5-1",
     ("impact_scaled",)),
]
EVAL_KEY = "research/analyses/rejudge-four-models/key.json"


# One definition, shared with the dashboard's "zonder sept. Opus 5.5" switch.
september_opus55 = provenance.september_opus55


def scaled_of(r):
    p, m = r.get("p_up"), r.get("abs_move_pct")
    if p is None or m is None:
        return None
    return (2 * p / 100 - 1) * m


def model_history(run, reg, everything=False):
    """{model: {"impact_sum": sorted |values|, "impact_scaled": sorted |values|}} over
    the live runs up to this one and the blind evaluations, September Opus 5.5 out.
    `everything` keeps every live run, this one and later ones included: the fixed
    reference the dashboard's top-X% filter reads beside the point-in-time one."""
    run = Path(run).resolve()
    day = "9999-12-31" if everything else run.parent.name
    hist = {}
    models, tainted = {}, set()

    def slot(m):
        return hist.setdefault(m, {"impact_sum": [], "impact_scaled": []})

    for d in sorted((ROOT / "research").glob("[0-9]*/[0-9]*/[0-9]*-*-*/*/")):
        # edge-panel's searcher sizes for breadth and is never ranked on its own
        # sizes (config/searcher-addendum.md), so it is not a reference for the hunters.
        # edge-deep (stage D) sizes three names with twice the depth and is kept out
        # until its scale has been compared with the hunters' on resolved names.
        # ipo (stage IPO) sizes an INTRADAY window on a different event, so its sizes
        # are not a reference for an earnings hunt's, nor theirs for it.
        if d.name not in DIR_MARKET or d.name in ("edge-panel", "edge-deep", "ipo"):
            continue
        model = run_model(d, reg)
        models[d.resolve()] = model
        if september_opus55(d, model):
            tainted.add(str(d.relative_to(ROOT)).rstrip("/"))
            continue
        if (d.resolve() == run and not everything) or d.parent.name > day or not model:
            continue
        key = load(d / "edge-scores.json")
        if not key or key.get("legacy_rescore"):
            continue
        if (load(d / "universe.json") or {}).get("validation_only"):
            continue
        for r in key.get("ranking", []):
            v = impact_of(r) if r.get("rankable") else None
            if v is not None:
                slot(model)["impact_sum"].append(abs(v))
        for r in (load(d / "edge-scores-scaled.json") or {}).get("ranking", []):
            if r.get("impact_scaled") is not None:
                slot(model)["impact_scaled"].append(abs(r["impact_scaled"]))

    # Each evaluation row judged the evidence of one live hunt; key.json says which.
    # Anonymised packs carry `pid` (anon/us/007) in place of the id. Corpus names are
    # in no key and drop out, as score_full.py drops them.
    origin = {}
    for k in load(ROOT / EVAL_KEY) or []:
        for i in (k.get("id"), k.get("pid")):
            if i:
                origin[i] = k.get("run")
    here = (str(run.relative_to(ROOT)) if run.is_relative_to(ROOT) and not everything
            else None)
    for pattern, model, numbers in EVALUATIONS:
        for f in sorted(ROOT.glob(pattern)):
            for r in load(f) or []:
                src = origin.get(r.get("id"))
                if src is None or src in tainted or src == here:
                    continue
                if "impact_sum" in numbers and r.get("impact_sum") is not None:
                    slot(model)["impact_sum"].append(abs(r["impact_sum"]))
                v = scaled_of(r) if "impact_scaled" in numbers else None
                if v is not None:
                    slot(model)["impact_scaled"].append(abs(v))
    for h in hist.values():
        for v in h.values():
            v.sort()
    return hist


def percentile(value, ref):
    """Mid-rank percentile of |value| in a sorted list of |values|; None when there is
    no value or fewer than MIN_HISTORY reference names."""
    if value is None or len(ref) < MIN_HISTORY:
        return None
    x = abs(value)
    below, upto = bisect_left(ref, x), bisect_right(ref, x)
    return 100 * (below + 0.5 * (upto - below)) / len(ref)


def pct(value, ref):
    """The same percentile as a bracket for the table."""
    if value is None:
        return ""
    if len(ref) < MIN_HISTORY:
        return " (n<20)"
    return f" (p{round(percentile(value, ref))})"


class Percentiles:
    """|impact_sum| percentile of a name against the reference names sized by the SAME
    model, for the dashboard: `pit` against what existed before its run (what
    score_report printed that day), `all` against the whole reference. Cached per run."""

    def __init__(self, reg=None):
        self.reg = reg or provenance.load_registry()
        self._pit, self._all = {}, None

    def of(self, run, model, value):
        if not model or value is None:
            return None, None
        key = str(Path(run).resolve())
        if key not in self._pit:
            self._pit[key] = model_history(run, self.reg)
        if self._all is None:
            self._all = model_history(run, self.reg, everything=True)
        ref = lambda h: (h.get(model) or {}).get("impact_sum") or []
        p, a = percentile(value, ref(self._pit[key])), percentile(value, ref(self._all))
        return (None if p is None else round(p, 1)), (None if a is None else round(a, 1))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the directory holding edge-scores.json")
    ap.add_argument("--label", help="stage name for the heading, e.g. 'Stage E'")
    ap.add_argument("--us", action="store_true",
                    help="show the V2 column (automatic for edge/ and edge-sonnet/)")
    a = ap.parse_args()

    run = Path(a.run)
    key = load(run / "edge-scores.json")
    if not key:
        print(f"no edge-scores.json in {run}: nothing has been scored", file=sys.stderr)
        sys.exit(1)
    scaled = load(run / "edge-scores-scaled.json")
    sc = {r["ticker"]: r for r in (scaled or {}).get("ranking", [])}
    us = a.us or run.name in US_DIRS
    grounded = load(run / "edge-scores-grounded.json") if us else None
    # stage E-P runs edge_context.py on its own directory; stage E's is the fallback,
    # since both rank the same day's names
    ctx = (load(run / "edge-context.json") or load(run.parent / "edge" / "edge-context.json")
           if us else None)
    gr = {r["ticker"]: r for r in (grounded or {}).get("ranking", [])}
    floor = key.get("conviction_floor", 3.0)
    reg = provenance.load_registry()
    model = run_model(run, reg)
    hist = model_history(run, reg).get(model, {"impact_sum": [], "impact_scaled": []})

    label = a.label or run.name
    print(f"**{label}, {run.parent.name}**: ranked on `{key.get('ranking_key')}` "
          f"(version 2, each finding sized on its own); conviction floor {floor:.1f} "
          f"applies to it only.")
    if not scaled:
        print("`edge-scores-scaled.json` is missing: impact_scaled not computed "
              "(re-run edge_score.py).")
    if us:
        if grounded is None:
            v2_state = "V2 not run: no edge-scores-grounded.json in this run."
        elif grounded.get("status") != "calibrated":
            v2_state = f"V2 {grounded.get('status')}: no grounded values."
        else:
            v2_state = (f"V2 at `{grounded.get('primary_horizon')}`, matrix as of "
                        f"{grounded.get('matrix_as_of')}.")
        print(v2_state)
    short = provenance.SHORT_MODEL.get(model, model) if model else None
    if short:
        print(f"Brackets: percentile of |value| among reference names sized by {short} "
              f"(impact_sum n={len(hist['impact_sum'])}, impact_scaled "
              f"n={len(hist['impact_scaled'])}): live runs to date plus the blind "
              f"re-judges, September Opus 5.5 hunts left out. Scale, not rank.")
    else:
        print("Brackets: no percentile, the hunter model of this run is not recorded.")
    print()

    sess = session_labels(run)
    head = ["#", "ticker", "session", "impact_sum (key)", "floor", "impact_scaled (v3)",
            "abs_move", "p_up"]
    if us:
        head += ["V2 grounded", "retail ≥50", "search quiet", "vol ≥58"]
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join(" --- " for _ in head) + "|")
    dropped = []
    for r in key.get("ranking", []):
        if not r.get("rankable"):
            dropped.append(r)
            continue
        s = sc.get(r["ticker"], {})
        cells = [str(r.get("rank")), r["ticker"], sess.get(r["ticker"], "n/a"),
                 f"**{f(r['impact_sum'])}**" + (pct(r["impact_sum"], hist["impact_sum"])
                                                 if model else ""),
                 "yes" if r.get("conviction", 0) >= floor else "no",
                 f(s.get("impact_scaled")) + (pct(s.get("impact_scaled"),
                                                  hist["impact_scaled"]) if model else ""),
                 f(s.get("abs_move_pct"), "{:.1f}"),
                 f(s.get("p_up"), "{:.0f}")]
        if us:
            g = gr.get(r["ticker"], {})
            if grounded is None or grounded.get("status") != "calibrated":
                cells.append("not run")
            elif g.get("impact_sum_grounded") is None:
                cells.append("n/a" + (f" ({g['not_grounded_because']})"
                                      if g.get("not_grounded_because") else ""))
            else:
                cells.append(f(g["impact_sum_grounded"]))
            cells += context_cells(ctx, r["ticker"])
        print("| " + " | ".join(cells) + " |")
    if not key.get("ranking"):
        print("| | no names | | | | | | |" + (" | | | |" if us else ""))
    for r in dropped:
        print(f"\nNot ranked: {r['ticker']}: {r.get('not_rankable_because')}")
    print("\n`session` is when the print lands: `amc` after the close, `bmo` before the "
          "open; `?` = not confirmed by the sweep, `n/a` = no print (stage R).")
    print("`impact_scaled` is the hunter's second, separate measurement, "
          "(2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.")
    if us:
        print("`retail`, `search` and `vol` are context for the reader, shown for every "
              "name whatever its score: retail tilt ≥ 50, a Google search spike under "
              "1.0x on the last complete day, and 20-day realised volatility ≥ 58% "
              "annualised. Nothing ranks, selects, sizes or trades on them.")


if __name__ == "__main__":
    main()
