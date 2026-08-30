#!/usr/bin/env python3
"""Turn hunter findings and adversary verdicts into a confidence score per name.

Confidence here is *derived*, never self-reported. On the 33 scored arm calls in
`backtest/runs/pilot-40`, the model's own `evidence_quality` field sorted outcomes
at exactly 50/50 between its top and bottom third -- a self-rated number with no
discriminating power at all. So nothing a hunter says about how sure it feels
enters this calculation. Only these do:

  independent_sources   distinct domains, across surviving findings, pointing the
                        same way. Two hunters citing one press release is one
                        source, not two.
  hunter_agreement      how much the independent hunts agreed on direction
  adversary_survival    what the priced-in adversary could not break
  cuts_against_price    whether the finding contradicts the skew and the run-up.
                        Corroboration of what the price already says earns nothing;
                        a model asked to weigh evidence treats agreement as support,
                        and here agreement means the information is already in.
  baseline_quality      a hard multiplier. A name with no usable option chain and
                        no reaction history has no statement of what was priced, so
                        no finding about it can be confidently called unpriced.

A confidence is emitted for EVERY name in the run, including abstains and names
with nothing found. That is deliberate: selection happens at scoring time by
thresholding this table, never by an agent choosing which names to report. It is
the only way "I only call the ones I am sure about" stays a measurement rather
than a claim.

    python3 scripts/edge_confidence.py --run research/2026/08/2026-08-31/edge
    python3 scripts/edge_confidence.py --run <dir> --threshold 55
"""
import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

SURVIVAL_WEIGHT = {"survives": 1.0, "partially_priced": 0.4, "already_priced": 0.0}
QUALITY_MULTIPLIER = {"full": 1.0, "partial": 0.75, "thin": 0.5}

# Domains that aggregate rather than report. Two findings sourced here are not
# two independent observations, so they collapse to one for the source count.
AGGREGATORS = {"finance.yahoo.com", "stocktwits.com", "seekingalpha.com",
               "benzinga.com", "marketbeat.com", "zacks.com", "fool.com",
               "investing.com", "tipranks.com", "barchart.com", "nasdaq.com",
               "simplywall.st", "gurufocus.com", "stockanalysis.com"}


def domain(url):
    try:
        h = (urlparse(url).hostname or "").lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


def load_dir(p, pattern="*.json"):
    out = []
    d = Path(p)
    if not d.exists():
        return out
    for f in sorted(d.glob(pattern)):
        try:
            out.append((f, json.loads(f.read_text(encoding="utf-8"))))
        except Exception:
            continue
    return out


def score_name(ticker, baseline, hunts, verdicts, threshold):
    """One name: fold its hunts and adversary verdicts into a single call."""
    reasons = []

    # --- what the price already says -------------------------------------
    opts = (baseline or {}).get("options") or {}
    skew = opts.get("skew_25d_vol_points")
    runup = ((baseline or {}).get("tape") or {}).get("run_up_20d_pct")
    priced_lean = None
    if skew is not None and abs(skew) > 2:
        priced_lean = "down" if skew > 0 else "up"
    elif runup is not None and abs(runup) > 8:
        priced_lean = "up" if runup > 0 else "down"

    # --- findings, keyed so an adversary verdict can find its finding -----
    findings = []
    for f, h in hunts:
        for i, item in enumerate(h.get("findings") or []):
            findings.append({
                "hunter": f.stem,
                "key": f"{f.stem}#{i}",
                "direction": (item.get("direction") or "").lower(),
                "finding": item.get("finding"),
                "source": item.get("source"),
                "source_date": item.get("source_date"),
                "why_not_priced": item.get("why_not_priced"),
                "independence": item.get("independence"),
            })
    by_key = {x["key"]: x for x in findings}
    for _, v in verdicts:
        k = v.get("finding_key")
        if k in by_key:
            by_key[k]["verdict"] = v.get("verdict")
            by_key[k]["adversary_confidence"] = v.get("confidence")
            by_key[k]["adversary_argument"] = v.get("strongest_argument")
            by_key[k]["prior_publication"] = v.get("prior_publication") or []
            by_key[k]["materiality"] = v.get("materiality")
            by_key[k]["reaches_this_print"] = v.get("reaches_this_print")

    # A finding nobody challenged is not a survivor. Unjudged findings are
    # weighted as partially priced, so skipping the adversary pass costs
    # confidence instead of granting it for free.
    for x in findings:
        x.setdefault("verdict", "unjudged")
        x["survival_weight"] = SURVIVAL_WEIGHT.get(x["verdict"], 0.4)
        if x.get("materiality") == "immaterial" or x.get("reaches_this_print") is False:
            x["survival_weight"] = 0.0
            x.setdefault("downgrade_note",
                         "immaterial or does not reach this print")

    # --- direction: weighted vote over surviving findings ----------------
    weight = {"up": 0.0, "down": 0.0}
    for x in findings:
        if x["direction"] in weight:
            weight[x["direction"]] += x["survival_weight"]
    total_w = weight["up"] + weight["down"]
    if total_w <= 0:
        direction = "abstain"
    else:
        direction = "up" if weight["up"] > weight["down"] else "down"
        if abs(weight["up"] - weight["down"]) < 0.25 * total_w:
            direction = "abstain"
            reasons.append("surviving findings point both ways with no clear balance")

    live = [x for x in findings
            if x["direction"] == direction and x["survival_weight"] > 0]

    # --- 1. independent sources (0-45) -----------------------------------
    doms = set()
    for x in live:
        d = domain(x.get("source") or "")
        if d:
            doms.add("AGGREGATOR" if d in AGGREGATORS else d)
        ind = x.get("independence") or ""
        for m in re.findall(r"https?://[^\s,)\]]+", ind):
            d2 = domain(m)
            if d2:
                doms.add("AGGREGATOR" if d2 in AGGREGATORS else d2)
    k = len(doms)
    src_pts = {0: 0, 1: 15, 2: 30, 3: 40}.get(k, 45 if k >= 4 else 0)
    if k <= 1:
        reasons.append(f"{k} independent source domain(s) behind the call")

    # --- 2. hunter agreement (0-20) --------------------------------------
    calls = [(h.get("direction") or "").lower() for _, h in hunts]
    voting = [c for c in calls if c in ("up", "down")]
    if not voting:
        agree_pts, agree_frac = 0.0, 0.0
    else:
        agree_frac = Counter(voting).most_common(1)[0][1] / len(voting)
        agree_pts = 20 * max(0.0, (agree_frac - 0.5) / 0.5)
    if len(voting) < 2:
        agree_pts *= 0.5
        reasons.append("only one hunter returned a directional view; agreement unmeasured")

    # --- 3. adversary survival (0-25) ------------------------------------
    if live:
        surv = sum(x["survival_weight"] for x in live) / len(live)
    else:
        surv = 0.0
    surv_pts = 25 * surv
    judged = [x for x in live if x["verdict"] != "unjudged"]
    if live and not judged:
        reasons.append("no adversary pass ran on the surviving findings")

    # --- 4. cuts against what the price says (0 or 10) --------------------
    if direction == "abstain" or priced_lean is None:
        tension_pts, tension = 0, "no directional statement in the price to test against"
    elif direction != priced_lean:
        tension_pts, tension = 10, f"cuts against the price, which leans {priced_lean}"
    else:
        tension_pts, tension = 0, f"agrees with the price, which already leans {priced_lean}"
        reasons.append("finding agrees with what the price already says, so it may be in")

    raw = src_pts + agree_pts + surv_pts + tension_pts

    # --- 5. baseline quality, as a hard multiplier -----------------------
    tier = ((baseline or {}).get("baseline_quality") or {}).get("tier", "thin")
    mult = QUALITY_MULTIPLIER.get(tier, 0.5)
    if mult < 1.0:
        reasons.append(f"baseline quality '{tier}' caps confidence at {int(mult * 100)}%")
    confidence = round(raw * mult, 1)

    called = (direction != "abstain" and confidence >= threshold and k >= 2
              and any(x["verdict"] == "survives" for x in live))
    if not called and direction != "abstain":
        if k < 2:
            reasons.append("held back: fewer than two independent sources")
        elif not any(x["verdict"] == "survives" for x in live):
            reasons.append("held back: no finding survived the adversary outright")
        elif confidence < threshold:
            reasons.append(f"held back: confidence {confidence} below threshold {threshold}")

    return {
        "ticker": ticker,
        "direction": direction,
        "called": called,
        "confidence": confidence,
        "components": {
            "independent_sources": {"n": k, "points": src_pts,
                                    "domains": sorted(doms)},
            "hunter_agreement": {"fraction": round(agree_frac, 2),
                                 "hunters_voting": len(voting),
                                 "points": round(agree_pts, 1)},
            "adversary_survival": {"mean_weight": round(surv, 2),
                                   "points": round(surv_pts, 1)},
            "cuts_against_price": {"points": tension_pts, "note": tension},
            "baseline_quality": {"tier": tier, "multiplier": mult},
            "raw_before_multiplier": round(raw, 1),
        },
        "priced_in": {
            "skew_25d_vol_points": skew,
            "priced_direction_lean": priced_lean,
            "run_up_20d_pct": runup,
            "event_implied_move_pct": opts.get("event_implied_move_pct"),
            "deadband_pct": (baseline or {}).get("deadband_pct"),
        },
        "why": reasons,
        "findings": findings,
        "hunter_calls": calls,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the edge/ directory for the day")
    ap.add_argument("--threshold", type=float, default=55.0)
    ap.add_argument("-o", "--out", help="defaults to <run>/edge-calls.json")
    a = ap.parse_args()

    run = Path(a.run)
    baselines = {f.stem.upper(): d for f, d in load_dir(run / "baselines")}
    hunts, verdicts = {}, {}
    for f, d in load_dir(run / "hunts"):
        hunts.setdefault((d.get("ticker") or f.stem.split("-")[0]).upper(), []).append((f, d))
    for f, d in load_dir(run / "adversary"):
        verdicts.setdefault((d.get("ticker") or f.stem.split("-")[0]).upper(), []).append((f, d))

    tickers = sorted(set(baselines) | set(hunts))
    rows = [score_name(t, baselines.get(t), hunts.get(t, []), verdicts.get(t, []), a.threshold)
            for t in tickers]
    rows.sort(key=lambda r: (-r["confidence"], r["ticker"]))

    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run": str(run),
        "threshold": a.threshold,
        "names_scored": len(rows),
        "names_called": sum(1 for r in rows if r["called"]),
        "coverage_pct": round(100 * sum(1 for r in rows if r["called"]) / len(rows), 1) if rows else 0.0,
        "selection_note": "every name in the run is scored and listed. Calls are selected "
                          "by thresholding this table, not by any agent choosing what to "
                          "report, so the risk-coverage curve can be recomputed at any "
                          "threshold after the fact.",
        "calls": rows,
    }
    out = Path(a.out) if a.out else run / "edge-calls.json"
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    print(f"{doc['names_called']}/{doc['names_scored']} called "
          f"({doc['coverage_pct']}% coverage) at threshold {a.threshold}\n")
    print(f"{'ticker':8s}{'dir':9s}{'conf':>6s}  {'called':7s} why")
    for r in rows:
        print(f"{r['ticker']:8s}{r['direction']:9s}{r['confidence']:6.1f}  "
              f"{'YES' if r['called'] else '-':7s} {'; '.join(r['why'])[:70]}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
