#!/usr/bin/env python3
"""The four-model judging panel for the non-US researcher stages (EU, J, AU, CA).

Stage E-P's method, applied to the hunts each regional stage already runs (2026-10-08,
operator's instruction): the day's hunter evidence goes into blind packs with every size
removed, four judges on four different models size it independently, and
researcher_us/scripts/panel_score.py combines them with stage E-P's frozen rules
(`edge_panel` in config/pipeline.yaml): each member read against its OWN recent history,
a name `selected` when 3 of 4 put it in their own top 20% on the panel's side.

What differs from stage E-P, and why:

- The hunters stay the stage's own (`unpriced-hunter-<market>`), not a searcher variant,
  so each stage's `impact_sum`, its prompt version and its resolved series carry on
  unbroken. The four-model re-judge that the panel rules were measured on judged exactly
  this: ordinary hunter evidence, including 48 European, 13 Japanese and 16 Australian
  names (research/analyses/rejudge-four-models/).
- Each pack names its own hunter definition and lessons file, so the judges are a second
  set, `panel-judge-intl-*`, generated from config/panel-judge-intl.md. The E-P judges
  are untouched.
- One history file per market (`researcher_<market>/analysis/panel-history.json`),
  seeded once with a frozen copy of stage E-P's history, because a member's "top 20%"
  needs at least 20 sizes before the first day. The market's own sizes push the seed out
  of the 200-name window as they accumulate. Nothing here writes stage E-P's history.
- `expected_edge_pct` is null: stage E-P's +6.7% prior was measured on development names
  that were mostly American, and there is no prior for a selected name in these markets.

    python3 scripts/market_panel.py packs   --market EU --run <RUN>
    python3 scripts/market_panel.py check   --market EU --run <RUN>
    python3 scripts/market_panel.py score   --market EU --run <RUN> [--fallback opus55=general-purpose:opus]
    python3 scripts/market_panel.py resolve --market EU --run <RUN>
    python3 scripts/market_panel.py pool    [--market EU]
    python3 scripts/market_panel.py seed    --market EU       # once; refuses to overwrite

Research only. Nothing here places, reads or sizes an order.
"""
import argparse
import glob
import json
import math
import random
import re
import statistics as st
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))
sys.path.insert(0, str(REPO / "scripts"))
import panel_packs as PP                                             # noqa: E402
import panel_score as PS                                             # noqa: E402
import score_report                                                  # noqa: E402

MARKETS = {
    "EU": {"dir": "europe", "id": "eu", "hunter": None,
           "lessons": "researcher_europe/LESSONS.md", "resolved": "eu-resolved.json",
           "history": "researcher_europe/analysis/panel-history.json"},
    "JP": {"dir": "japan", "id": "jp", "hunter": "unpriced-hunter-jp",
           "lessons": "researcher_japan/LESSONS.md", "resolved": "jp-resolved.json",
           "history": "researcher_japan/analysis/panel-history.json"},
    "AU": {"dir": "australia", "id": "au", "hunter": "unpriced-hunter-au",
           "lessons": "researcher_australia/LESSONS.md", "resolved": "au-resolved.json",
           "history": "researcher_australia/analysis/panel-history.json"},
    "CA": {"dir": "canada", "id": "ca", "hunter": "unpriced-hunter-ca",
           "lessons": "researcher_canada/LESSONS.md", "resolved": "canada-resolved.json",
           "history": "researcher_canada/analysis/panel-history.json"},
}
JUDGES = {"opus5": ("panel-judge-intl-opus5", "claude-opus-5"),
          "opus55": ("panel-judge-intl-opus55", "claude-opus-5-5"),
          "sonnet55": ("panel-judge-intl-sonnet55", "claude-sonnet-5-5"),
          "fable51": ("panel-judge-intl-fable51", "claude-fable-5-1")}
STAGE = {"EU": "EU-P", "JP": "J-P", "AU": "AU-P", "CA": "CA-P"}


def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml"))
    rules = dict(c.get("edge_panel") or {})
    rules.update({k: v for k, v in (c.get("market_panel") or {}).items()
                  if k in ("member_top_share", "history_window", "consensus_fraction")})
    return rules


def eu_hunter(submarket):
    from provenance import EU_SUBMARKET_HUNTER
    return EU_SUBMARKET_HUNTER.get(submarket)


def run_date(run):
    return next((p for p in Path(run).parts if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p)), None)


def hunts_for(run, t):
    pat = re.compile(r"^%s(-h\d+)?\.json$" % re.escape(t))
    return sorted(p for p in (Path(run) / "hunts").glob("*.json") if pat.match(p.name))


# ---------------------------------------------------------------- packs

def build_packs(market, run):
    spec, run = MARKETS[market], Path(run)
    day = run_date(run)
    if not day:
        sys.exit(f"cannot read the run date from {run}")
    sf = run / "edge-scores.json"
    if not sf.exists():
        sys.exit(f"{sf} is missing: score the run before building packs")
    rankable = {r["ticker"] for r in json.load(open(sf)).get("ranking", []) if r.get("rankable")}
    packs, unmapped = [], []
    for b in sorted((run / "baselines").glob("*.json")):
        base = json.load(open(b))
        t = base.get("ticker") or b.stem
        if t not in rankable:
            continue
        hs = hunts_for(run, t)
        if not hs:
            continue
        hunter = spec["hunter"] or eu_hunter(base.get("submarket"))
        if not hunter:
            unmapped.append(t)
            continue
        packs.append({"id": f"{spec['id']}/{day}/{t}",
                      "hunter_definition": f".claude/agents/{hunter}.md",
                      "lessons_file": spec["lessons"],
                      "baseline": PP.trim(base),
                      "first_hunter_context": PP.context(hs[0]),
                      "evidence": PP.evidence(hs)})
    if unmapped:
        print(f"no hunter mapped for submarket of {', '.join(unmapped)}: left out", file=sys.stderr)
    return packs


def cmd_packs(a):
    packs = build_packs(a.market, a.run)
    out = Path(a.run) / "panel"
    out.mkdir(exist_ok=True)
    json.dump(packs, open(out / "packs.json", "w"), ensure_ascii=False, indent=1)
    lines = (out / "packs.json").read_text().count("\n")
    defs = sorted({p["hunter_definition"] for p in packs})
    print(f"{len(packs)} packs -> {out / 'packs.json'} ({lines} lines); "
          f"hunter definitions: {', '.join(defs) or 'none'}")


# ---------------------------------------------------------------- check

def cmd_check(a):
    run = Path(a.run)
    ids = {p["id"] for p in json.load(open(run / "panel" / "packs.json"))}
    bad = 0
    for m in PS.MEMBERS:
        f = run / "panel" / f"{m}.json"
        if not f.exists():
            print(f"{m}: MISSING (no {f.name})")
            bad += 1
            continue
        try:
            got = {o.get("id") for o in json.load(open(f))}
        except Exception as e:                                       # noqa: BLE001
            print(f"{m}: UNREADABLE ({e})")
            bad += 1
            continue
        miss, extra = sorted(ids - got), sorted(got - ids)
        print(f"{m}: {len(ids & got)}/{len(ids)}"
              + (f"  missing {', '.join(miss)}" if miss else "")
              + (f"  unknown ids {', '.join(map(str, extra))}" if extra else ""))
        bad += bool(miss or extra)
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- score

def cmd_score(a):
    spec, run = MARKETS[a.market], Path(a.run)
    hist = REPO / spec["history"]
    if not hist.exists():
        sys.exit(f"{hist} does not exist: run `market_panel.py seed --market {a.market}` once")
    out, added = PS.score(run, cfg(), dry_run=a.dry_run, history=hist, stage=STAGE[a.market])
    for r in out["ranking"]:
        r["expected_edge_pct"] = None
    out["market"] = a.market
    out["rules_from"] = "edge_panel"
    out["history_file"] = spec["history"]
    out["note"] += (" Non-US stage: the hunters are the stage's own, the judges are "
                    "panel-judge-intl-*, and expected_edge_pct is null because stage E-P's "
                    "development prior was measured mostly on US names.")
    json.dump(out, open(run / "edge-scores-panel.json", "w"), indent=1)
    if not a.dry_run:
        stamp_provenance(run, out, a.fallback or [])
    print(f"members {', '.join(out['members_present'])}"
          + (f" (MISSING {', '.join(out['members_missing'])})" if out["members_missing"] else "")
          + f"; selection {out['selection']}; {added} sizes added to {spec['history']}")
    sess = score_report.session_labels(run)
    print(f"{'rank':>4s} {'ticker':8s} {'session':7s} {'sel':3s} {'k':>2s} {'agree':>5s} {'score':>6s} {'sd':>5s}  members (z)")
    for r in out["ranking"]:
        zz = " ".join(f"{m}:{x['z']:+.2f}{'*' if x['in_own_top'] else ''}" for m, x in r["members"].items())
        print(f"{r['rank']:4d} {r['ticker']:8s} {sess.get(r['ticker'], 'n/a'):7s} {'yes' if r['selected'] else '':3s} {r['consensus_k']:2d} "
              f"{r['sign_agree']:2d}/{r['n_members']}  {r['panel_score']:+6.2f} {r['panel_sd_z']:5.2f}  {zz}")


def stamp_provenance(run, out, fallbacks):
    """Write the panel block into <RUN>/provenance.json: per member, the agent that ran,
    the model pinned in its frontmatter, or `missing`. --fallback member=agent[:model]
    records a member that ran through stage E-P's general-purpose fallback."""
    fb = {}
    for f in fallbacks:
        m, _, rest = f.partition("=")
        agent, _, model = rest.partition(":")
        fb[m] = {"agent": agent, "model_alias": model or None, "fallback": True,
                 "model_pinned": None}
    p = run / "provenance.json"
    prov = json.load(open(p)) if p.exists() else {}
    block = {"stamped_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "rules_from": "edge_panel", "history_file": out["history_file"],
             "selection": out["selection"], "members": {}}
    for m, (agent, model) in JUDGES.items():
        if m not in out["members_present"]:
            block["members"][m] = {"status": "missing", "agent": agent, "model_pinned": model}
        else:
            block["members"][m] = dict({"status": "ran", "agent": agent, "model_pinned": model,
                                        "fallback": False}, **fb.get(m, {}))
    prov["panel"] = block
    json.dump(prov, open(p, "w"), indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- resolve

def move_of(row):
    for k in ("realised_move_pct", "move_pct", "realised_move"):
        if row.get(k) is not None:
            return row[k]
    return None


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    rx, ry = ranks(xs), ranks(ys)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def perm_p(xs, ys, n=2000, seed=7):
    rho = spearman(xs, ys)
    if rho is None:
        return None
    rnd, ys2, hit = random.Random(seed), list(ys), 0
    for _ in range(n):
        rnd.shuffle(ys2)
        r = spearman(xs, ys2)
        hit += r is not None and abs(r) >= abs(rho) - 1e-12
    return (hit + 1) / (n + 1)


def book(pairs):
    """pairs: (side, move). Hit rate and mean signed return of a book, gross."""
    rets = [s * m for s, m in pairs if s]
    if not rets:
        return {"n": 0}
    return {"n": len(rets), "hits": sum(r > 0 for r in rets),
            "mean_signed_move_pct": round(st.mean(rets), 2),
            "t": (round(st.mean(rets) / (st.stdev(rets) / math.sqrt(len(rets))), 2)
                  if len(rets) > 1 and st.stdev(rets) > 0 else None)}


def resolve_rows(market, run):
    spec, run = MARKETS[market], Path(run)
    res = run / spec["resolved"]
    pan = run / "edge-scores-panel.json"
    if not res.exists() or not pan.exists():
        return None, f"needs both {spec['resolved']} and edge-scores-panel.json"
    resolved = json.load(open(res))
    panel = {r["ticker"]: r for r in json.load(open(pan)).get("ranking", [])}
    scores = json.load(open(run / "edge-scores.json"))
    key = {r["ticker"]: r for r in scores.get("ranking", [])}
    floor = scores.get("conviction_floor")
    rows = []
    for r in resolved.get("rows") or []:
        t, mv = r.get("ticker"), move_of(r)
        if t not in panel or mv is None or r.get("move_pending") or r.get("event_occurred") is False \
                or r.get("rankable") is False:
            continue
        p, k = panel[t], key.get(t) or {}
        rows.append({"ticker": t, "move_pct": mv, "panel_score": p["panel_score"],
                     "panel_selected": p["selected"], "consensus_k": p["consensus_k"],
                     "side": p["side"], "impact_sum": k.get("impact_sum") or 0.0,
                     "above_floor": floor is not None and abs(k.get("impact_sum") or 0.0) >= floor})
    return {"rows": rows, "conviction_floor": floor,
            "validation_only": (json.load(open(run / "universe.json")).get("validation_only")
                                if (run / "universe.json").exists() else None)}, None


def stats_of(rows, floor):
    out = {"n": len(rows)}
    if len(rows) >= 5:
        mv = [r["move_pct"] for r in rows]
        ps, ks = [r["panel_score"] for r in rows], [r["impact_sum"] for r in rows]
        r3 = lambda x: None if x is None else round(x, 3)              # noqa: E731
        out.update({"spearman_panel": r3(spearman(ps, mv)), "p_panel": r3(perm_p(ps, mv)),
                    "spearman_impact_sum": r3(spearman(ks, mv)), "p_impact_sum": r3(perm_p(ks, mv))})
    else:
        out["rho_withheld"] = "fewer than five resolved names"
    out["panel_selected"] = book([(r["side"], r["move_pct"]) for r in rows if r["panel_selected"]])
    out["hunter_above_floor"] = book([((r["impact_sum"] > 0) - (r["impact_sum"] < 0), r["move_pct"])
                                      for r in rows if r["above_floor"]])
    out["conviction_floor"] = floor
    return out


def cmd_resolve(a):
    got, err = resolve_rows(a.market, a.run)
    if err:
        sys.exit(f"{a.run}: {err}")
    s = stats_of(got["rows"], got["conviction_floor"])
    doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "market": a.market, "run": str(a.run), "stats": s, "rows": got["rows"],
           "note": "Gross, the market resolver's own window. One run is an anecdote: pool with "
                   "`market_panel.py pool` before reading anything."}
    json.dump(doc, open(Path(a.run) / "panel-resolved.json", "w"), indent=1)
    print(json.dumps(s, indent=1))


def cmd_pool(a):
    out = {}
    for m in ([a.market] if a.market else MARKETS):
        spec, rows, days = MARKETS[m], [], []
        for run in sorted(glob.glob(str(REPO / "research" / "*" / "*" / "*" / spec["dir"]))):
            got, err = resolve_rows(m, run)
            if err or got["validation_only"] or not got["rows"]:
                continue
            days.append({"run": str(Path(run).relative_to(REPO)), **stats_of(got["rows"], got["conviction_floor"])})
            rows.extend(got["rows"])
        out[m] = {"days": len(days), "names": len(rows),
                  "panel_selected": book([(r["side"], r["move_pct"]) for r in rows if r["panel_selected"]]),
                  "hunter_above_floor": book([((r["impact_sum"] > 0) - (r["impact_sum"] < 0), r["move_pct"])
                                              for r in rows if r["above_floor"]]),
                  "per_day": days}
    print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- seed

def cmd_seed(a):
    dest = REPO / MARKETS[a.market]["history"]
    if dest.exists():
        sys.exit(f"{dest} exists; the seed is written once and never refreshed")
    us = json.load(open(PS.HISTORY))
    doc = {"_seed": {"from": str(PS.HISTORY.relative_to(REPO)),
                     "copied_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "note": ("Frozen copy of stage E-P's member history, so each member has a "
                              "scale before this market's first panel day. This market's own "
                              "sizes are appended after it and push it out of the window.")}}
    for m in PS.MEMBERS:
        doc[m] = list(us.get(m, []))
    dest.parent.mkdir(parents=True, exist_ok=True)
    json.dump(doc, open(dest, "w"), indent=1)
    print(f"{dest.relative_to(REPO)}: seeded {', '.join(f'{m} {len(doc[m])}' for m in PS.MEMBERS)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("packs", "check", "score", "resolve", "pool", "seed"):
        p = sub.add_parser(name)
        p.add_argument("--market", choices=sorted(MARKETS), required=name != "pool")
        if name not in ("pool", "seed"):
            p.add_argument("--run", required=True)
        if name == "score":
            p.add_argument("--dry-run", action="store_true",
                           help="score without appending to the history or stamping provenance")
            p.add_argument("--fallback", action="append",
                           help="member=agent[:model] for a member that ran through a fallback")
    a = ap.parse_args()
    {"packs": cmd_packs, "check": cmd_check, "score": cmd_score, "resolve": cmd_resolve,
     "pool": cmd_pool, "seed": cmd_seed}[a.cmd](a)


if __name__ == "__main__":
    main()
