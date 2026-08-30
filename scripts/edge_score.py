#!/usr/bin/env python3
"""One signed number per company, so the day's names can be ranked.

This replaces `edge_confidence.py`, which emitted a direction label, a binary
`called` flag, and a confidence built from three-bucket adversary verdicts and a
three-tier baseline quality. On 2026-08-31 every judged finding fell into one of
two verdict buckets and twelve names collapsed to a single non-zero score and
eleven zeros. There was nothing to rank, and the bucketing did that rather than
the evidence.

Everything here is continuous:

  expected_impact_pct   each finding carries a SIGNED size in percentage points of
                        spot, not an up/down label
  priced_in_pct         the adversary returns 0-100 for how much of that impact is
                        already in the price, not survives/partial/already
  quality               baseline quality is a 0-1 scalar computed from counts and
                        spreads, not full/partial/thin
  edge_pct              the residual the market has not priced, in points of spot
  edge_score            edge_pct squashed to -100..+100 for ranking across names

There is no `called` flag and no threshold. Selection is done afterwards by
sorting on `edge_score` and taking a top-k or a cutoff, which is what makes the
question "can these be ranked?" answerable at every k rather than at one.

    python3 scripts/edge_score.py --run research/2026/08/2026-08-31/edge
    python3 scripts/edge_score.py --run <dir> --legacy   # read old categorical files
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
            findings.append({
                "hunter": f.stem, "key": f"{f.stem}#{i}",
                "finding": item.get("finding"),
                "source": item.get("source"), "source_date": item.get("source_date"),
                "expected_impact_pct": float(imp or 0.0),
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
        # number. Where the two disagree badly the disagreement is information,
        # so the finding is sized on the average rather than on either alone.
        sc = v.get("size_check_pct")
        if sc is not None:
            x["adversary_size_pct"] = float(sc)
            x["size_disagreement_pct"] = round(
                abs(float(sc) - x["expected_impact_pct"]), 3)
            x["expected_impact_pct"] = round(
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

    # Aggregate by source cluster, then discount for correlation between clusters.
    # Within a cluster take the largest residual rather than the sum: two readings
    # of one document are one fact seen twice.
    clusters = {}
    for x in findings:
        c = clusters.setdefault(x["cluster"], [])
        c.append(x["residual_pct"])
    per_cluster = [max(v, key=abs) for v in clusters.values()]
    k = len(per_cluster)
    raw_edge = sum(per_cluster)
    edge_pct = round(raw_edge / math.sqrt(k), 3) if k else 0.0

    # Evidence that merely agrees with what the price already says is not edge.
    tension = None
    if lean is not None and edge_pct:
        agree = (edge_pct > 0) == (lean > 0)
        tension = round(abs(lean), 3)
        edge_pct = round(edge_pct * (0.55 if agree else 1.0), 3)

    edge_pct = round(edge_pct * (0.35 + 0.65 * q), 3)

    # Ranking key. tanh keeps the ordering of edge_pct exactly while bounding the
    # scale, so one outsized finding cannot dominate a sort across names.
    edge_score = round(100.0 * math.tanh(edge_pct / 5.0), 1)

    # Dispersion across hunters, in points. Wide disagreement is a real property
    # of the name and belongs in the uncertainty, not in a gate.
    per_hunter = {}
    for x in findings:
        per_hunter.setdefault(x["hunter"], 0.0)
        per_hunter[x["hunter"]] += x["residual_pct"]
    vals = list(per_hunter.values())
    dispersion = round(statistics.pstdev(vals), 3) if len(vals) > 1 else 0.0

    unpriced_share = ([round(1 - x["priced_in_pct"] / 100.0, 3) for x in findings] or [0.0])
    confidence = round(100.0 * q * min(1.0, k / 3.0) *
                       (1.0 - min(0.5, dispersion / 8.0)) *
                       max(unpriced_share), 1)

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
        "edge_score": edge_score,
        "edge_pct": edge_pct,
        "confidence": confidence,
        "uncertainty_pct": round(max(dispersion, abs(edge_pct) * 0.5), 3),
        "baseline_quality": q,
        "quality_parts": q_parts,
        "priced_lean_pct": lean,
        "agrees_with_price": None if (lean is None or not edge_pct)
                             else ((edge_pct > 0) == (lean > 0)),
        "price_lean_magnitude_pct": tension,
        "independent_clusters": k,
        "cluster_names": sorted(clusters),
        "hunter_dispersion_pct": dispersion,
        "hunters": len(hunts),
        "findings": findings,
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
    rows.sort(key=lambda r: (not r["rankable"], -r["edge_score"]))
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
        "note": "Every name carries a signed edge_score on -100..+100. There is no "
                "call and no threshold: rank on edge_score and cut wherever you "
                "like afterwards, which is what makes the ranking question "
                "answerable at every k.",
        "ranking": rows,
    }
    out = Path(a.out) if a.out else run / "edge-scores.json"
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    nr = sum(1 for r in rows if r["rankable"])
    print(f"{nr} of {len(rows)} names rankable"
          + ("  [LEGACY re-score: synthetic impacts, machinery only]" if a.legacy else ""))
    print(f"\n{'#':>2} {'ticker':8s}{'edge':>7s}{'edge%':>8s}{'conf':>6s}{'unc%':>7s}"
          f"{'qual':>6s}{'clus':>5s}  price lean")
    for r in rows:
        lean = r["priced_lean_pct"]
        ln = f"{lean:+.2f}%" if lean is not None else "  n/a"
        if not r["rankable"]:
            print(f"{'--':>2} {r['ticker']:8s}{'':>7s}{'':>8s}{'':>6s}{'':>7s}"
                  f"{r['baseline_quality']:>6.2f}{'':>5s}  not ranked: {r['not_rankable_because']}")
            continue
        print(f"{r['rank']:>2} {r['ticker']:8s}{r['edge_score']:>7.1f}{r['edge_pct']:>8.2f}"
              f"{r['confidence']:>6.1f}{r['uncertainty_pct']:>7.2f}"
              f"{r['baseline_quality']:>6.2f}{r['independent_clusters']:>5d}  {ln}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
