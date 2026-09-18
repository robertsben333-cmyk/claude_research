#!/usr/bin/env python3
"""Pool the edge-corpus days, split by what the capture actually held.

`edge/scripts/edge_resolve.py` pools a run's names into one rank correlation. That is
right for the live pipeline, where every name got the same treatment. It is wrong
here, and section 36 is why: of the 109 names in this backtest only 14 captures
hold a single news item. The other 95 are an EDGAR index and a Stocktwits dump.

Those are two experiments:

  news_bearing   can the method rank a name given news, filings and social
  filings_only   can it rank one given filings and retail chatter alone

Pooling them produces a number that answers neither, which is the anchor-mix
mistake of section 34 in a new place. Both are reported, and `filings_only` is the
more interesting half: a hunt that finds nothing in an EDGAR index has told us
something about the method, while one that finds nothing because nobody searched
has told us about the capture.

Three further splits, each recording a known defect rather than a hypothesis:

  contaminated     the capture kept sweeping past the print (section 35). Their
                   hunts ran under a clean-view restriction, so they are reported
                   apart until that restriction is shown not to matter.
  seal_6k          session inferred from a 6-K acceptance time, which is not a
                   release time (section 37). RZLV shows how wrong that can be.
  share_class      two classes of one company reporting one print. One event, so
                   the second copy is excluded from the pooled figure rather than
                   counted as independent evidence.

    python3 backtest/scripts/edge_corpus_report.py
"""
import argparse
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs" / "edge-corpus"

# Two share classes of one company reporting one print. The class kept is the one
# whose corpus is richer; the other is one event counted twice.
SHARE_CLASS_DROP = {"BF.A", "WLYB"}

# Names whose hunt was written while a document naming post-print moves was in the
# hunter's context. The 2026-09-03 hunter opened a pre-market movers list before
# checking its fetch timestamp, disclosed it, and excluded it from the six names it
# had not yet written -- but CPB and CIEN were already on disk. Their numbers may be
# sound; they cannot be shown to be, which is the whole point of a sealed corpus.
# Reported apart rather than deleted, because a disclosed breach is data about the
# harness and a silently kept one is not.
BREACH_EXPOSED = {("2026-09-03", "CPB"), ("2026-09-03", "CIEN")}


def spearman(x, y):
    n = len(x)
    if n < 3:
        return None

    def rank(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return None if dx == 0 or dy == 0 else num / (dx * dy)


def perm_p(x, y, seed=7, n=20000):
    s = spearman(x, y)
    if s is None:
        return None, None
    rng = random.Random(seed)
    yy = list(y)
    hits = 0
    for _ in range(n):
        rng.shuffle(yy)
        t = spearman(x, yy)
        if t is not None and abs(t) >= abs(s):
            hits += 1
    return round(s, 3), round((hits + 1) / (n + 1), 4)


def corpus_type(cap):
    for s in (cap / "snapshots").glob("*.json"):
        try:
            for it in (json.loads(s.read_text(encoding="utf-8")).get("items") or []):
                if it.get("kind") == "news":
                    return "news_bearing"
        except Exception:
            continue
    return "filings_only"


def collect():
    contam = {}
    cf = RUNS / "contamination.json"
    if cf.exists():
        for r in json.loads(cf.read_text(encoding="utf-8"))["rows"]:
            contam[(r["event_date"], r["ticker"])] = r["contaminated"]

    rows = []
    for out in sorted(RUNS.glob("*/edge-outcome.json")):
        day = out.parent.name
        doc = json.loads(out.read_text(encoding="utf-8"))
        man = json.loads((out.parent / "manifest.json").read_text(encoding="utf-8"))
        by_t = {e["ticker"]: e for e in man["events"]}
        per_day = doc.get("per_day") or []
        rows_in = [x for d in per_day for x in (d.get("rows") or [])]
        for r in rows_in:
            if r.get("outcome") != "resolved":
                continue
            e = by_t.get(r["ticker"], {})
            cap = ROOT.parent / e.get("capture", "")
            seal = {}
            if (cap / "seal.json").exists():
                seal = json.loads((cap / "seal.json").read_text(encoding="utf-8"))
            rows.append({
                "day": day, "ticker": r["ticker"],
                "edge_score": r["edge_score"], "move_pct": r["move_pct"],
                "move_over_implied": r.get("move_over_implied"),
                "implied_basis": r.get("implied_basis"),
                "corpus_type": corpus_type(cap) if cap.exists() else "unknown",
                "contaminated": bool(contam.get((day, r["ticker"]))),
                "seal_6k": "6-K" in (seal.get("basis") or ""),
                "share_class_dup": r["ticker"] in SHARE_CLASS_DROP,
                "breach_exposed": (day, r["ticker"]) in BREACH_EXPOSED,
                "items": e.get("items"), "docs": e.get("docs"),
            })
    return rows


def stat_block(rows, label):
    rows = [r for r in rows if not r["share_class_dup"]]
    if len(rows) < 3:
        return {"label": label, "n": len(rows),
                "note": "fewer than 3 names; rank correlation not computed"}
    e = [r["edge_score"] for r in rows]
    s_raw, p_raw = perm_p(e, [r["move_pct"] for r in rows])
    out = {"label": label, "n": len(rows),
           "spearman_vs_raw_move": s_raw, "p_raw": p_raw}
    norm = [r for r in rows if r["move_over_implied"] is not None]
    if len(norm) >= 3:
        s_n, p_n = perm_p([r["edge_score"] for r in norm],
                          [r["move_over_implied"] for r in norm])
        out.update(spearman_vs_move_over_implied=s_n, p_normalised=p_n,
                   n_normalised=len(norm),
                   anchor_mix=dict(Counter(r["implied_basis"] for r in norm)))
    nz = [r for r in rows if r["edge_score"] != 0]
    out["nonzero_scores"] = len(nz)
    out["distinct_scores"] = len({r["edge_score"] for r in rows})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = collect()
    blocks = [stat_block(rows, "ALL resolved names")]
    for key, val, label in [
        ("corpus_type", "news_bearing", "corpus held news items"),
        ("corpus_type", "filings_only", "corpus was filings + social only"),
        ("contaminated", False, "capture clean against the seal"),
        ("contaminated", True, "capture kept sweeping past the print"),
        ("seal_6k", False, "session from an 8-K item 2.02 (measured)"),
        ("seal_6k", True, "session from a 6-K acceptance time (inferred)"),
        ("breach_exposed", False, "no disclosed sight of a post-print document"),
    ]:
        blocks.append(stat_block([r for r in rows if r[key] == val], label))

    doc = {"names_resolved": len(rows),
           "share_class_duplicates_excluded": sorted(SHARE_CLASS_DROP),
           "breach_exposed": sorted(f"{d}/{t}" for d, t in BREACH_EXPOSED),
           "days": sorted({r["day"] for r in rows}),
           "blocks": blocks, "rows": rows}
    outp = RUNS / "corpus-report.json"
    outp.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    if a.json:
        print(json.dumps(doc["blocks"], indent=1))
        return

    print(f"=== edge-corpus, {len(rows)} resolved names over "
          f"{len(doc['days'])} days ===\n")
    hdr = f"{'':46s} {'n':>4s} {'rho(raw)':>9s} {'p':>7s} {'rho(norm)':>10s} {'p':>7s}"
    print(hdr)
    print("-" * len(hdr))
    for b in blocks:
        if b.get("note"):
            print(f"{b['label']:46s} {b['n']:4d}   {b['note']}")
            continue
        print(f"{b['label']:46s} {b['n']:4d} "
              f"{b['spearman_vs_raw_move']:+9.3f} {b['p_raw']:7.4f} "
              + (f"{b['spearman_vs_move_over_implied']:+10.3f} {b['p_normalised']:7.4f}"
                 if b.get("spearman_vs_move_over_implied") is not None else
                 f"{'--':>10s} {'--':>7s}"))
    print(f"\nwrote {outp}")


if __name__ == "__main__":
    main()
