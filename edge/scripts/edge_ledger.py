#!/usr/bin/env python3
"""Flatten every edge run into one row per finding, and join what the stock did.

The hunt already writes everything this needs. Each run's `edge-scores.json`
carries the hunters' findings verbatim -- the text, the size, the source, the
cluster -- and `edge_resolve.py` knows how to price the outcome window. Nothing
here spawns a subagent or calls a model; it is an extraction over files already
on disk, so it costs a network round trip per unresolved name and nothing else.

The question it exists to make answerable is **what sort of finding was ever
worth anything**: does a `filing_detail` read off a primary document beat an
`inference` off two secondary reports, is a wide `impact_low/high` band a
confession that pays, does a finding sourced two months before the print carry
more than one from yesterday's wire.

## The honesty problem, stated once

**A per-finding outcome does not exist.** You observe one number per company --
what the stock did over the window -- and a name carries three to eight findings
that were never separately priced. So `sign_agreed` on a finding row is not "this
finding was right"; it is "the name this finding belonged to moved the way this
finding pointed", and every finding of that name shares it. Two consequences:

  * A single row means nothing. Group by `kind`, by `evidence`, by source age,
    and compare rates across hundreds of rows.
  * Weight by `share_of_impact`. A finding that was 90% of its name's key
    genuinely was the call; one that was 5% of it is a passenger and its
    agreement is mostly somebody else's.

Both are what `--report` does. `sole_finding` marks the rows where the
attribution problem does not arise at all -- one finding carried the whole name --
and it is the cleanest subgroup in the table, and the smallest.

## Outputs

    edge/ledger/findings.csv     one row per finding, every run, ever
    edge/ledger/names.csv        one row per (date, ticker)
    edge/ledger/edge.sqlite      both, as tables `findings` and `names`
    edge/ledger/outcomes.json    the realised-move cache, so a rebuild is free

Rebuild after every run. It is derived state: safe to delete, cheap to rebuild,
and never hand-edited.

    python3 edge/scripts/edge_ledger.py                 # build everything
    python3 edge/scripts/edge_ledger.py --report        # build, then group it
    python3 edge/scripts/edge_ledger.py --no-network    # cache only, no fetches

`claim`, `kind` and `evidence` are null on every run before 2026-09-10 -- the
hunter contract did not have them. The columns derived from the source URL and
the sizes are populated for all history.
"""
import argparse
import csv
import json
import sqlite3
import statistics
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edge_resolve import realised  # noqa: E402  (the one shared piece of logic)

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "edge" / "ledger"

KINDS = {
    "filing_detail", "guidance_mechanics", "insider_or_ownership",
    "regulatory_or_legal", "competitor_or_peer", "demand_data", "cost_or_input",
    "capital_structure", "management_change", "product_or_contract",
    "accounting", "positioning", "other",
}
EVIDENCE = {"primary", "secondary", "inference"}

FINDING_COLS = [
    "event_date", "run_date", "ticker", "session", "run", "hunter", "key",
    "claim", "kind", "evidence", "finding", "why_not_priced",
    "expected_impact_pct", "impact_low_pct", "impact_high_pct", "band_width_pct",
    "sign", "abs_impact_pct", "share_of_impact", "sole_finding",
    "independence", "source", "source_domain", "cluster",
    "source_date", "source_age_days",
    "priced_in_pct", "priced_in_basis",
    "name_impact_sum", "name_conviction", "name_findings", "above_floor",
    "move_pct", "sign_agreed", "resolved",
]
NAME_COLS = [
    "event_date", "run_date", "ticker", "session", "run",
    "impact_sum", "conviction", "above_floor", "n_findings", "n_clusters",
    "hunters", "priced_lean_pct", "runup_20d_pct", "runup_5d_pct",
    "implied_move_pct", "implied_basis", "deadband_pct",
    "hist_median_abs_move_pct", "hist_n", "baseline_quality",
    "spot", "dollar_vol_20d",
    "entry_date", "exit_date", "move_pct", "move_over_implied",
    "sign_agreed", "abs_error_pts", "resolved",
]


def norm_kind(v):
    v = (v or "").strip().lower().replace(" ", "_").replace("-", "_")
    if not v:
        return None
    return v if v in KINDS else "other"


def norm_evidence(v):
    v = (v or "").strip().lower()
    return v if v in EVIDENCE else (None if not v else "other")


def domain_of(url):
    try:
        h = (urlparse(url or "").hostname or "").lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


def parse_day(s):
    """Hunters write '2026-06-12', '2026-09-02 (report date; filed ...)', junk."""
    if not s:
        return None
    t = str(s).strip()[:10]
    try:
        return date.fromisoformat(t)
    except ValueError:
        return None


DEFAULT_RUNS = "research/*/*/*/edge"


def run_dirs(root, pattern=DEFAULT_RUNS):
    """Any directory shaped like a run: edge-scores.json, baselines/, hunts/.

    `backtest/runs/edge-corpus/*` has that shape too, which is what makes an
    out-of-sample test of a finding-level hypothesis possible at all: 104 resolved
    events whose hunters could not see past the print, scored by the same code.
    """
    return sorted(p for p in root.glob(pattern)
                  if (p / "edge-scores.json").exists())


def event_date_of(run):
    """The run's own day. `research/2026/09/2026-09-10/edge` keeps it in the parent;
    `backtest/runs/edge-corpus/2026-09-09` is the directory itself."""
    name = run.parent.name if run.name == "edge" else run.name
    return name


def baseline_of(run, ticker):
    for p in (run / "baselines" / f"{ticker}.json",
              run / "baselines" / f"{ticker.upper()}.json"):
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return {}
    return {}


def event_of(run, ticker, baseline):
    """The date of the PRINT, not the date of the run.

    They are different for half the rows. A run fires in the European afternoon
    and covers tonight's `amc` prints plus tomorrow morning's `bmo` ones, and the
    09-04 run hunted five names that reported on 09-08. `edge_resolve.py` has
    always taken the date off the baseline; the first version of this script took
    it off the directory name and priced 78 of 153 rows over the wrong window.
    """
    return baseline.get("event_date") or event_date_of(run)


def session_of(run, ticker, baseline):
    s = (baseline.get("session") or "").lower()
    if s in ("amc", "bmo"):
        return s
    try:
        uni = json.loads((run / "universe.json").read_text(encoding="utf-8"))
    except Exception:
        return None
    rows = uni.get("companies") or uni.get("rows") or uni if isinstance(uni, list) else []
    for r in (rows if isinstance(rows, list) else []):
        if (r.get("ticker") or "").upper() == ticker.upper():
            v = (r.get("session") or "").lower()
            return v if v in ("amc", "bmo") else None
    return None


def hunt_index(run):
    """Everything the hunter wrote, keyed the way edge_score keys it.

    `edge-scores.json` does not carry `why_not_priced`, `independence` or the
    impact band, and on runs before 2026-09-10 it does not carry `claim`, `kind`
    or `evidence` either because the contract had no such fields. All of it is
    still in `hunts/<TICKER>.json`, so read that and let the scores file win
    where the two overlap.
    """
    idx = {}
    d = run / "hunts"
    if not d.exists():
        return idx
    for f in sorted(d.glob("*.json")):
        try:
            h = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for i, item in enumerate(h.get("findings") or []):
            idx[f"{f.stem}#{i}"] = item
    return idx


def num(*vals):
    for v in vals:
        if isinstance(v, (int, float)):
            return float(v)
    return None


def build(root, use_network=True, pattern=DEFAULT_RUNS, out=None):
    out_dir = out or LEDGER
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / "outcomes.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    findings, names = [], []
    for run in run_dirs(root, pattern):
        ed = event_date_of(run)
        scores = json.loads((run / "edge-scores.json").read_text(encoding="utf-8"))
        floor = scores.get("conviction_floor") or 3.0
        raw = hunt_index(run)
        for row in scores.get("ranking") or []:
            t = (row.get("ticker") or "").upper()
            fs = row.get("findings") or []
            # Non-rankable rows are calendar noise the sweep killed: no hunter was
            # ever spawned, so there is nothing to learn from them.
            if not t or (not fs and not row.get("rankable")):
                continue
            base = baseline_of(run, t)
            sess = session_of(run, t, base)
            # `impact_sum` became the key on 2026-09-09 and is absent from every
            # file before it. It is a plain sum of the sizes the hunters wrote,
            # so the older runs can be brought onto the same key exactly.
            impact_sum = num(row.get("impact_sum"))
            if impact_sum is None and fs:
                impact_sum = round(
                    sum(num(f.get("expected_impact_pct")) or 0.0 for f in fs), 3)
            conviction = abs(impact_sum) if impact_sum is not None else None

            print_date = event_of(run, t, base)
            ck = f"{print_date}:{t}:{sess}"
            out = cache.get(ck)
            if out is None and use_network and sess:
                try:
                    r, err = realised(t, print_date, sess)
                    out = r if not err else {"error": err}
                except Exception as e:                       # noqa: BLE001
                    out = {"error": f"{type(e).__name__}: {e}"}
                cache[ck] = out
            move = (out or {}).get("move_pct")
            resolved = isinstance(move, (int, float))
            sign_agreed = None
            if resolved and impact_sum not in (None, 0.0) and move != 0:
                sign_agreed = int((impact_sum > 0) == (move > 0))

            tot_abs = sum(abs(num(f.get("expected_impact_pct")) or 0.0) for f in fs)
            clusters = {f.get("cluster") for f in fs if f.get("cluster")}
            hunters = {f.get("hunter") for f in fs if f.get("hunter")}
            above = (int(conviction >= floor)
                     if conviction is not None and floor is not None else None)

            tape = base.get("tape") or {}
            opts = base.get("options") or {}
            hist = base.get("history") or {}
            straddle = opts.get("event_implied_move_pct")
            names.append({
                "event_date": print_date, "run_date": ed,
                "ticker": t, "session": sess,
                "run": str(run.relative_to(root)),
                "impact_sum": impact_sum, "conviction": conviction,
                "above_floor": above, "n_findings": len(fs),
                "n_clusters": len(clusters), "hunters": len(hunters),
                "priced_lean_pct": num(row.get("priced_lean_pct")),
                "runup_20d_pct": num(tape.get("run_up_20d_pct")),
                "runup_5d_pct": num(tape.get("run_up_5d_pct")),
                # Same convention as edge_resolve: the straddle where there was
                # one, the reaction-history proxy where there was not, and a
                # column saying which -- they are not interchangeable.
                "implied_move_pct": num(straddle, base.get("expected_move_pct")),
                "implied_basis": ("straddle" if straddle else
                                  "history_proxy" if base.get("expected_move_pct")
                                  else None),
                "deadband_pct": num(base.get("deadband_pct")),
                "hist_median_abs_move_pct": num(hist.get("median_abs_move_pct")),
                "hist_n": hist.get("n"),
                "baseline_quality": num(base.get("baseline_quality"),
                                        (row.get("diagnostics") or {}).get("baseline_quality")),
                "spot": num(tape.get("spot")),
                "dollar_vol_20d": (round(tape["spot"] * tape["avg_volume_20d"])
                                   if num(tape.get("spot")) and num(tape.get("avg_volume_20d"))
                                   else None),
                # The window that was actually priced. Two runs that hunted the
                # same print on different days share it, which is what makes the
                # repeated events findable at all.
                "entry_date": (out or {}).get("before_date"),
                "exit_date": (out or {}).get("after_date"),
                "move_pct": move if resolved else None,
                "sign_agreed": sign_agreed,
                "move_over_implied": (round(move / num(straddle,
                                       base.get("expected_move_pct")), 3)
                                      if resolved and num(straddle,
                                          base.get("expected_move_pct")) else None),
                "abs_error_pts": (round(abs(impact_sum - move), 3)
                                  if resolved and impact_sum is not None else None),
                "resolved": int(resolved),
            })

            for f in fs:
                src = raw.get(f.get("key")) or {}

                def pick(field, f=f, src=src):
                    v = f.get(field)
                    return src.get(field) if v in (None, "") else v

                imp = num(f.get("expected_impact_pct")) or 0.0
                lo = num(pick("impact_low_pct"))
                hi = num(pick("impact_high_pct"))
                sd = parse_day(f.get("source_date"))
                ev = parse_day(print_date)
                findings.append({
                    "event_date": print_date, "run_date": ed,
                    "ticker": t, "session": sess,
                    "run": str(run.relative_to(root)),
                    "hunter": f.get("hunter"), "key": f.get("key"),
                    "claim": pick("claim"), "kind": norm_kind(pick("kind")),
                    "evidence": norm_evidence(pick("evidence")),
                    "finding": pick("finding"),
                    "why_not_priced": pick("why_not_priced"),
                    "independence": pick("independence"),
                    "expected_impact_pct": imp,
                    "impact_low_pct": lo, "impact_high_pct": hi,
                    "band_width_pct": (round(hi - lo, 3)
                                       if lo is not None and hi is not None else None),
                    "sign": 1 if imp > 0 else (-1 if imp < 0 else 0),
                    "abs_impact_pct": round(abs(imp), 3),
                    "share_of_impact": (round(abs(imp) / tot_abs, 4) if tot_abs else None),
                    "sole_finding": int(len(fs) == 1),
                    "source": f.get("source"),
                    "source_domain": domain_of(f.get("source")),
                    "cluster": f.get("cluster"),
                    "source_date": f.get("source_date"),
                    "source_age_days": ((ev - sd).days if sd and ev else None),
                    "priced_in_pct": num(f.get("priced_in_pct")),
                    "priced_in_basis": f.get("priced_in_basis"),
                    "name_impact_sum": impact_sum, "name_conviction": conviction,
                    "name_findings": len(fs), "above_floor": above,
                    "move_pct": move if resolved else None,
                    # Shared across the name, on purpose. Read the header.
                    "sign_agreed": sign_agreed,
                    "resolved": int(resolved),
                })

    cache_path.write_text(json.dumps(cache, indent=1, sort_keys=True))
    return findings, names


def write_csv(path, cols, rows):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_sqlite(path, findings, names):
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    for table, cols, rows in (("findings", FINDING_COLS, findings),
                              ("names", NAME_COLS, names)):
        con.execute(f"CREATE TABLE {table} ({','.join(cols)})")
        con.executemany(
            f"INSERT INTO {table} VALUES ({','.join('?' * len(cols))})",
            [[r.get(c) for c in cols] for r in rows])
    con.execute("CREATE INDEX f_kind ON findings(kind)")
    con.execute("CREATE INDEX f_event ON findings(event_date, ticker)")
    con.commit()
    con.close()


def group_report(findings):
    """Rates by group, weighted and unweighted, on resolved rows only."""
    rows = [f for f in findings if f["resolved"] and f["sign_agreed"] is not None]
    out = {"resolved_findings": len(rows),
           "names": len({(f["event_date"], f["ticker"]) for f in rows}),
           "days": len({f["event_date"] for f in rows}), "groups": {}}

    def bucket_age(d):
        if d is None:
            return "unknown"
        return "<=7d" if d <= 7 else ("8-30d" if d <= 30 else
                                      ("31-90d" if d <= 90 else ">90d"))

    def bucket_size(a):
        return "<1pt" if a < 1 else ("1-3pt" if a < 3 else ("3-6pt" if a < 6 else ">=6pt"))

    dims = {
        "kind": lambda f: f["kind"] or "unlabelled",
        "evidence": lambda f: f["evidence"] or "unlabelled",
        "source_age": lambda f: bucket_age(f["source_age_days"]),
        "abs_impact": lambda f: bucket_size(f["abs_impact_pct"]),
        "cluster": lambda f: f["cluster"] or "UNSOURCED",
        "sole_finding": lambda f: "sole" if f["sole_finding"] else "one_of_many",
    }
    for dim, keyf in dims.items():
        g = defaultdict(list)
        for f in rows:
            g[keyf(f)].append(f)
        stats = {}
        for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
            w = sum(f["share_of_impact"] or 0.0 for f in v)
            wa = sum((f["share_of_impact"] or 0.0) * f["sign_agreed"] for f in v)
            stats[k] = {
                "n": len(v),
                "names": len({(f["event_date"], f["ticker"]) for f in v}),
                "agree_rate": round(statistics.fmean(f["sign_agreed"] for f in v), 3),
                "agree_rate_weighted": round(wa / w, 3) if w else None,
                "median_abs_impact": round(statistics.median(
                    f["abs_impact_pct"] for f in v), 2),
                "median_move_pct": round(statistics.median(
                    abs(f["move_pct"]) for f in v), 2),
            }
        out["groups"][dim] = stats
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--no-network", action="store_true",
                    help="use the outcome cache only; do not fetch new bars")
    ap.add_argument("--report", action="store_true",
                    help="also write and print edge/ledger/report.json")
    ap.add_argument("--runs", default=DEFAULT_RUNS,
                    help="glob for run directories, relative to --root. Point it at "
                         "backtest/runs/edge-corpus/* to build the sealed corpus as a "
                         "ledger and test a finding-level hypothesis out of sample.")
    ap.add_argument("--out", help="write the ledger here instead of edge/ledger/")
    a = ap.parse_args()

    out_dir = Path(a.out) if a.out else LEDGER
    findings, names = build(Path(a.root), use_network=not a.no_network,
                            pattern=a.runs, out=out_dir)
    write_csv(out_dir / "findings.csv", FINDING_COLS, findings)
    write_csv(out_dir / "names.csv", NAME_COLS, names)
    write_sqlite(out_dir / "edge.sqlite", findings, names)

    res = sum(n["resolved"] for n in names)
    lab = sum(1 for f in findings if f["kind"])
    print(f"findings {len(findings)}  names {len(names)}  resolved names {res}  "
          f"days {len({n['event_date'] for n in names})}  kind-labelled {lab}")
    print(f"-> {out_dir}/findings.csv, names.csv, edge.sqlite")

    if a.report:
        rep = group_report(findings)
        (out_dir / "report.json").write_text(json.dumps(rep, indent=2))
        print(json.dumps(rep, indent=2))
        if rep["days"] < 20:
            print("\nNOTE: too few days to read any of this as a result. It is a "
                  "table to watch as runs pool, not a finding.", file=sys.stderr)


if __name__ == "__main__":
    main()
