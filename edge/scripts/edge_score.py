#!/usr/bin/env python3
"""One signed number per company, so the day's names can be ranked.

**The ranking key is `impact_sum`: the hunters' signed per-finding sizes, added up.**
Nothing else. It is measured, not designed: `docs/EDGA` -- see
`edge/EDGE_ANALYSIS.md` -- decomposed six resolved runs and found that every
transformation this script used to apply lowered the rank correlation against the
realised move.

    impact sum, as it comes from the hunters        rho = 0.453  p = 0.006
      sized on the hunter/adversary mean instead         0.407  p = 0.014
      x (1 - priced_in/100)                              0.376  p = 0.027
      cluster-max                                        0.284
      / sqrt(k)                                          0.279
      x agreement discount x quality multiplier          0.243  p = 0.156   <- shipped
                                                                              until
                                                                              2026-09-09

A paired bootstrap over days puts the gap between the first line and the last at
+0.165, 95% CI [+0.082, +0.244]. The machinery was subtractive, so it no longer
decides anything. The demoted numbers are still computed, into `diagnostics`, for
two reasons: `residual_sum` is a genuinely open question (the priced-in haircut
costing ordering is the most counter-intuitive result in the file and rests on six
days), and `edge_score_legacy` keeps every earlier run comparable.

Two things ride alongside the key:

  conviction        abs(impact_sum). Direction skill is conditional on it. The rank
                    of conviction predicts whether the sign was right at rho=+0.514
                    (permutation p=0.0015) to the next close; over ALL events the
                    sign is a coin flip at 53%. Above the median prediction it is
                    74%. `conviction_floor` in config/pipeline.yaml is where a
                    reader should start believing the sign -- it is a floor on
                    EMPHASIS, never a filter on this file.
  priced_lean_pct   the control. One number off the sealed baseline, available
                    before a single subagent is spawned, that ranked the same six
                    days at rho=0.335. Until the hunt beats it the hunt has not been
                    shown to add anything, so it travels beside the key rather than
                    multiplying into it.

No call, no direction label, no threshold in the output. Selection is the reader's,
made afterwards on the complete table, which is what keeps "can these be ranked?"
answerable at every k.

    python3 edge/scripts/edge_score.py --run research/2026/09/2026-09-09/edge
    python3 edge/scripts/edge_score.py --run <dir> --legacy   # old categorical files
"""
import argparse
import json
import math
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# Only used with --legacy, to read runs recorded before the contract changed.
# Midpoints, not measurements: a re-score of old data is a demonstration of the
# machinery and never evidence about the day.
LEGACY_PRICED_IN = {"survives": 15.0, "partially_priced": 60.0,
                    "already_priced": 95.0, "unjudged": 65.0}
LEGACY_IMPACT_PCT = 4.0

def conviction_floor(default=3.0):
    """Where a reader should start believing the sign. Config, not arithmetic."""
    p = Path(__file__).resolve().parents[2] / "config" / "pipeline.yaml"
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*conviction_floor:\s*([0-9.]+)", line)
            if m:
                return float(m.group(1))
    except Exception:
        pass
    return default


FLOOR = conviction_floor()

AGGREGATORS = {"finance.yahoo.com", "stocktwits.com", "seekingalpha.com",
               "benzinga.com", "marketbeat.com", "zacks.com", "fool.com",
               "investing.com", "cn.investing.com", "uk.investing.com",
               "ca.investing.com", "tipranks.com", "barchart.com", "nasdaq.com",
               "simplywall.st", "gurufocus.com", "stockanalysis.com",
               "stocktitan.net", "prnewswire.com", "globenewswire.com"}


def domain(url):
    try:
        h = (urlparse(url or "").hostname or "").lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


def cluster_of(x):
    """Two hunters citing one press release are one observation, not two."""
    d = domain(x.get("source"))
    return "AGGREGATOR" if d in AGGREGATORS else (d or "UNSOURCED")


def load_dir(p):
    out = []
    d = Path(p)
    if not d.exists():
        return out
    for f in sorted(d.glob("*.json")):
        try:
            out.append((f, json.loads(f.read_text(encoding="utf-8"))))
        except Exception:
            continue
    return out


def baseline_quality(baseline):
    """0-1 scalar. How well do we actually know what this name has priced in?

    Continuous because the three-tier version made a name with 3 prior prints and
    a wide chain identical to one with none, and because a hard 0.5 multiplier on
    `thin` made those names arithmetically incapable of ranking anywhere but the
    bottom regardless of what was found.
    """
    b = baseline or {}
    opts = b.get("options") or {}
    hist = b.get("history") or {}

    n = hist.get("n") or 0
    hist_q = min(1.0, n / 6.0)

    spread = opts.get("atm_spread_frac_of_mid")
    if opts.get("event_implied_move_pct") is None:
        opt_q = 0.0
    elif spread is None:
        opt_q = 0.5
    else:
        opt_q = max(0.0, min(1.0, 1.0 - spread / 0.6))

    dir_q = 1.0 if opts.get("skew_25d_vol_points") is not None else 0.0

    plaus = (b.get("event_plausibility") or {}).get("verdict")
    event_q = {"fits_cadence": 1.0, "unknown": 0.6, "suspect": 0.05}.get(plaus, 0.6)

    q = 0.40 * hist_q + 0.35 * opt_q + 0.25 * dir_q
    return round(q * event_q, 3), {
        "history": round(hist_q, 3), "options": round(opt_q, 3),
        "priced_direction": dir_q, "event_plausibility": event_q,
        "history_events": n, "atm_spread_frac": spread,
    }


def priced_lean_pct(baseline):
    """What the price itself says about direction, in points, signed.

    Skew is the market paying for one tail. Positive skew (puts bid) is a
    negative lean. Scaled so a large skew on a large implied move matters more
    than the same skew on a quiet name.
    """
    b = baseline or {}
    opts = b.get("options") or {}
    skew = opts.get("skew_25d_vol_points")
    em = opts.get("event_implied_move_pct")
    if skew is None or not em:
        runup = (b.get("tape") or {}).get("run_up_20d_pct")
        if runup is None:
            return None
        return round(-0.05 * runup, 3)      # a big run-in is itself an expectation
    return round(-(skew / 20.0) * em, 3)


def score_name(ticker, baseline, hunts, verdicts, legacy=False):
    q, q_parts = baseline_quality(baseline)
    lean = priced_lean_pct(baseline)

    findings = []
    for f, h in hunts:
        for i, item in enumerate(h.get("findings") or []):
            imp = item.get("expected_impact_pct")
            if imp is None and legacy:
                d = (item.get("direction") or "").lower()
                imp = LEGACY_IMPACT_PCT * (1 if d == "up" else -1 if d == "down" else 0)
            lo, hi = item.get("impact_low_pct"), item.get("impact_high_pct")
            findings.append({
                "hunter": f.stem, "key": f"{f.stem}#{i}",
                "finding": item.get("finding"),
                # The three ledger fields. They decide nothing here and are carried
                # through verbatim so `edge_ledger.py` reads one file per run
                # instead of re-opening every hunt. Null on runs before 2026-09-10.
                "claim": item.get("claim"),
                "kind": item.get("kind"),
                "evidence": item.get("evidence"),
                "source": item.get("source"), "source_date": item.get("source_date"),
                "expected_impact_pct": float(imp or 0.0),
                # The hunter's own band. Discarded until 2026-09-10, which threw
                # away the one thing it says about its own uncertainty.
                "impact_low_pct": None if lo is None else float(lo),
                "impact_high_pct": None if hi is None else float(hi),
                "cluster": cluster_of(item),
            })

    # The adversary now returns one file per ticker carrying a verdicts[] array,
    # instead of one file per finding. Both shapes are read so a run recorded
    # under the old contract still scores.
    by_key = {x["key"]: x for x in findings}
    flat = []
    for _, v in verdicts:
        flat.extend(v.get("verdicts") or [v])
    for v in flat:
        x = by_key.get(v.get("finding_key"))
        if not x:
            continue
        p = v.get("priced_in_pct")
        if p is None and legacy:
            p = LEGACY_PRICED_IN.get(v.get("verdict"), 65.0)
        x["priced_in_pct"] = None if p is None else float(p)
        x["adversary_note"] = v.get("strongest_argument")
        # The adversary sizes each claim itself, without seeing the hunter's
        # number. Until 2026-09-09 the finding was then sized on the MEAN of the
        # two, on the reasoning that a disagreement is information. It is, but
        # averaging is not how to use it: over 43 resolved names the mean ranks at
        # rho=0.407 (p=0.014) and the hunter's own number at rho=0.453 (p=0.006).
        # So the key sums the hunter's number and the adversary's estimate is kept
        # beside it, where a large disagreement stays visible instead of being
        # split down the middle. On 2026-09-09 KEQU-h1#0 had the hunter at -4.0
        # against the adversary at -15.0, and that name's rank turned on it.
        sc = v.get("size_check_pct")
        if sc is not None:
            x["adversary_size_pct"] = float(sc)
            x["size_disagreement_pct"] = round(
                abs(float(sc) - x["expected_impact_pct"]), 3)
            # Only `edge_score_legacy` reads this, so the old key still
            # reproduces exactly.
            x["sized_mean_pct"] = round(
                (x["expected_impact_pct"] + float(sc)) / 2.0, 3)

    # An unjudged finding is not a survivor. Default it to mostly-priced so that
    # skipping the adversary pass costs edge rather than granting it free.
    for x in findings:
        if x.get("priced_in_pct") is None:
            x["priced_in_pct"] = LEGACY_PRICED_IN["unjudged"]
            x["priced_in_basis"] = "unjudged; defaulted"
        else:
            x["priced_in_basis"] = "adversary"
        x["residual_pct"] = round(
            x["expected_impact_pct"] * (1.0 - x["priced_in_pct"] / 100.0), 3)
        # The pre-2026-09-09 arithmetic, kept only so edge_score_legacy is exact.
        x["_legacy_residual_pct"] = round(
            x.get("sized_mean_pct", x["expected_impact_pct"])
            * (1.0 - x["priced_in_pct"] / 100.0), 3)

    # THE RANKING KEY. The hunters' signed sizes, added up, and nothing else.
    impact_sum = round(sum(x["expected_impact_pct"] for x in findings), 3)
    conviction = round(abs(impact_sum), 3)

    # Everything below is a diagnostic. None of it enters the key.
    #
    # residual_sum is the open question: every way of letting priced_in touch the
    # ranking lowered it (the haircut 0.453 -> 0.325, and dropping high-priced_in
    # findings is monotonically worse the more it drops). Measured, never applied.
    #
    # None of it means anything on a day with no adversary pass, so say null rather
    # than computing a number off the "unjudged" default of 65.
    judged = [x for x in findings if x.get("priced_in_basis") == "adversary"]
    residual_sum = (round(sum(x["residual_pct"] for x in findings), 3)
                    if judged and len(judged) == len(findings) else None)

    # edge_score_legacy reproduces the pre-2026-09-09 key exactly, so every earlier
    # run stays comparable and the demotion stays checkable.
    clusters = {}
    for x in findings:
        clusters.setdefault(x["cluster"], []).append(x["_legacy_residual_pct"])
    per_cluster = [max(v, key=abs) for v in clusters.values()]
    k = len(per_cluster)
    legacy_pct = round(sum(per_cluster) / math.sqrt(k), 3) if k else 0.0
    if lean is not None and legacy_pct:
        legacy_pct = round(legacy_pct * (0.55 if (legacy_pct > 0) == (lean > 0) else 1.0), 3)
    legacy_pct = round(legacy_pct * (0.35 + 0.65 * q), 3)
    edge_score_legacy = round(100.0 * math.tanh(legacy_pct / 5.0), 1)

    # Dispersion across hunters, in points. A real property of the name, kept as
    # metadata: two isolated hunters disagreeing is the most informative thing the
    # stage produces and it should be visible, not folded into a number.
    per_hunter = {}
    for x in findings:
        per_hunter.setdefault(x["hunter"], 0.0)
        per_hunter[x["hunter"]] += x["expected_impact_pct"]
    vals = list(per_hunter.values())
    dispersion = round(statistics.pstdev(vals), 3) if len(vals) > 1 else 0.0

    # A name with no event, or with no evidence either way, sits at 0.0 and would
    # sort above every mildly negative name. Arithmetically right, and useless for
    # the question being asked. Rankable is carried separately so the correlation
    # test runs on names that actually reported.
    plaus = ((baseline or {}).get("event_plausibility") or {}).get("verdict")
    confirmed = any((h.get("event_confirmed") is not False) for _, h in hunts) if hunts else True
    rankable = bool(hunts) and confirmed and plaus != "suspect"
    why_not = None
    if not rankable:
        why_not = ("no hunt" if not hunts
                   else "hunter found no event on this date" if not confirmed
                   else "event date does not fit the filing cadence")

    return {
        "ticker": ticker,
        "rankable": rankable,
        "not_rankable_because": why_not,
        "impact_sum": impact_sum,
        "conviction": conviction,
        "priced_lean_pct": lean,
        "findings": findings,
        "diagnostics": {
            "residual_sum": residual_sum,
            "adversary_judged": f"{len(judged)}/{len(findings)}" if findings else "0/0",
            "edge_score_legacy": edge_score_legacy,
            "baseline_quality": q,
            "quality_parts": q_parts,
            "independent_clusters": k,
            "cluster_names": sorted(clusters),
            "hunter_dispersion_pct": dispersion,
            "hunters": len(hunts),
            "note": "diagnostics only. None of these enters the ranking key -- "
                    "edge/EDGE_ANALYSIS.md measured every one of them as neutral or "
                    "subtractive against the realised move.",
        },
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--legacy", action="store_true",
                    help="read runs recorded under the old categorical contract")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    run = Path(a.run)
    baselines = {f.stem.upper(): d for f, d in load_dir(run / "baselines")}
    hunts, verdicts = {}, {}
    for f, d in load_dir(run / "hunts"):
        hunts.setdefault((d.get("ticker") or f.stem.split("-")[0]).upper(), []).append((f, d))
    for f, d in load_dir(run / "adversary"):
        verdicts.setdefault((d.get("ticker") or f.stem.split("-")[0]).upper(), []).append((f, d))

    rows = [score_name(t, baselines.get(t), hunts.get(t, []), verdicts.get(t, []), a.legacy)
            for t in sorted(set(baselines) | set(hunts))]
    rows.sort(key=lambda r: (not r["rankable"], -r["impact_sum"]))
    rank = 0
    for r in rows:
        if r["rankable"]:
            rank += 1
            r["rank"] = rank
        else:
            r["rank"] = None

    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run": str(run),
        "legacy_rescore": a.legacy,
        "names": len(rows),
        "rankable": sum(1 for r in rows if r["rankable"]),
        "ranking_key": "impact_sum",
        "conviction_floor": FLOOR,
        "note": "Ranked on impact_sum: the hunters' signed per-finding sizes, added "
                "up, in points of spot. No call and no threshold -- cut wherever you "
                "like afterwards, which is what keeps the ranking question answerable "
                "at every k. `conviction` (abs of the key) is where the direction "
                "skill lives: over all events the sign is a coin flip, above the "
                "median conviction it is 74%. conviction_floor is a floor on emphasis "
                "in the note, never a filter on this file. Everything under "
                "`diagnostics` was measured as neutral or subtractive and decides "
                "nothing -- see edge/EDGE_ANALYSIS.md.",
        "ranking": rows,
    }
    out = Path(a.out) if a.out else run / "edge-scores.json"
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    nr = sum(1 for r in rows if r["rankable"])
    print(f"{nr} of {len(rows)} names rankable"
          + ("  [LEGACY re-score: synthetic impacts, machinery only]" if a.legacy else ""))
    above = sum(1 for r in rows if r["rankable"] and r["conviction"] >= FLOOR)
    print(f"{above} of {nr} clear the conviction floor of {FLOOR:.1f} points\n")
    print(f"{'#':>2} {'ticker':8s}{'impact':>9s}{'convict':>9s}{'floor':>7s}"
          f"{'lean':>9s}{'resid':>8s}{'legacy':>8s}")
    for r in rows:
        lean = r["priced_lean_pct"]
        ln = f"{lean:+.2f}%" if lean is not None else "n/a"
        d = r["diagnostics"]
        if not r["rankable"]:
            print(f"{'--':>2} {r['ticker']:8s}{'':>9s}{'':>9s}{'':>7s}{ln:>9s}"
                  f"{'':>8s}{'':>8s}  not ranked: {r['not_rankable_because']}")
            continue
        # residual_sum and edge_score_legacy are both None when a name carries no
        # adversary verdicts. Since the adversary became a weekly audit that is the
        # normal case on four days in five, so these must be formatted defensively
        # or the summary crashes on every non-audit day.
        rs = d.get("residual_sum")
        lg = d.get("edge_score_legacy")
        rs_s = f"{rs:+.2f}" if rs is not None else "n/a"
        lg_s = f"{lg:+.1f}" if lg is not None else "n/a"
        print(f"{r['rank']:>2} {r['ticker']:8s}{r['impact_sum']:>+9.2f}"
              f"{r['conviction']:>9.2f}{('yes' if r['conviction'] >= FLOOR else '-'):>7s}"
              f"{ln:>9s}{rs_s:>8s}{lg_s:>8s}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
