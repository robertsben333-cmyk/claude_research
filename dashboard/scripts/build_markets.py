#!/usr/bin/env python3
"""Collect the researchers that place no orders into one dataset, for the
per-market tabs on the dashboard: Europe, Japan, Australia and Canada.

    python3 dashboard/scripts/build_markets.py
    python3 dashboard/scripts/build_markets.py --resolve     # also fill in moves

This is the RESEARCH record for the stages that place no orders. There is no
money level here and there must not be one: stages EU, J, AU and CA have no
broker, so `dashboard/data/ledger.json`'s trades and equity curve say nothing
about them and are not extended to them.

What it does NOT do is own the outcome window. Each market's window is different
-- Europe and Australia report before the open, so theirs is close(D-1) ->
close(D), Japan's is the Tokyo close to the next one -- and that logic lives in
eu_resolve.py, jp_resolve.py, au_resolve.py and ca_resolve.py. This script reads
the file those write (`eu-resolved.json`, `jp-resolved.json`, `au-resolved.json`,
`canada-resolved.json`) and, with
--resolve, runs the market's own resolver for a past run that has none yet. A
realised move that appears here was computed by the market's resolver or it does
not appear at all.

The statistics are deliberately absent. The page recomputes rho, the sign rate
and the book return client-side from these rows under its own threshold, the
same way every other tab on the dashboard works -- a frozen summary is a
threshold you cannot move. Each run's own resolver stats ride along verbatim
under `resolver_stats` so the two can be compared.
"""
import argparse
import glob
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dashboard" / "data"

# stage -> (directory name, market code, resolver, its default output file)
STAGES = {
    "EU": {"dir": "europe", "label": "Europa", "stage": "EU",
           "resolver": "researcher_europe/scripts/eu_resolve.py",
           "resolved": "eu-resolved.json"},
    "JP": {"dir": "japan", "label": "Japan", "stage": "J",
           "resolver": "researcher_japan/scripts/jp_resolve.py",
           "resolved": "jp-resolved.json"},
    "AU": {"dir": "australia", "label": "Australië", "stage": "AU",
           "resolver": "researcher_australia/scripts/au_resolve.py",
           "resolved": "au-resolved.json"},
    "CA": {"dir": "canada", "label": "Canada", "stage": "CA",
           "resolver": "researcher_canada/scripts/ca_resolve.py",
           "resolved": "canada-resolved.json"},
}


def rd(x, n=3):
    return None if x is None else round(x, n)


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def move_of(row):
    """The realised move, whatever the market's resolver called the field.

    Europe and Japan write `realised_move_pct`; Australia writes `move_pct`.
    Keep reading both rather than renaming a field three resolved runs already
    carry."""
    for k in ("realised_move_pct", "move_pct", "realised_move"):
        if row.get(k) is not None:
            return row[k]
    return None


def needs_resolving(path):
    """Is there still an outcome to fetch for this run?

    Not simply "is the file missing". Yahoo's European daily closes lag by a
    session or two, so a run resolved the morning after its print writes a file
    in which every row is `move_pending` and no move was ever recorded. Treating
    that file as done freezes the day at nothing, permanently, which is a worse
    failure than the one it saves: it looks exactly like a day on which the hunt
    had no outcome. So a file with no realised move and at least one row still
    live is resolved again, and a file that carries even one move is left alone
    -- the window it priced has closed and will not change."""
    if not path.exists():
        return True
    doc = load(path)
    if doc is None:
        return True
    rows = doc.get("rows") or []
    if not rows:
        return True
    if any(move_of(r) is not None for r in rows):
        return False
    return any(r.get("event_occurred") is not False for r in rows)


def resolve_run(run, spec, timeout=300):
    """Run the market's own resolver over a run that has no resolved file.

    Only ever called for a run whose event date has passed, and never for one
    that already has a file -- a resolver call costs network and the window it
    prices does not change once it has closed."""
    out = Path(run) / spec["resolved"]
    cmd = [sys.executable, str(ROOT / spec["resolver"]), "--run", str(run),
           "-o", str(out)]
    try:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"{run}: resolver timed out after {timeout}s"
    if p.returncode != 0:
        tail = (p.stderr or p.stdout or "").strip().splitlines()
        return f"{run}: resolver exited {p.returncode}: {tail[-1] if tail else ''}"
    return None


def collect_run(run, spec, problems):
    """One run directory -> (meta, rows). Rows exist with or without an outcome."""
    rp = Path(run)
    rel = str(rp.relative_to(ROOT)) if str(rp).startswith(str(ROOT)) else str(rp)
    scores = load(rp / "edge-scores.json") or {}
    universe = load(rp / "universe.json") or {}
    resolved = load(rp / spec["resolved"])

    run_date = rel.rstrip("/").split("/")[-2]
    event_date = (scores.get("event_date") or universe.get("event_date")
                  or (resolved or {}).get("event_date") or run_date)

    # The resolver's rows, keyed by ticker, for the outcome and for the fields it
    # adds that the scorer does not carry.
    res_rows = {r.get("ticker"): r for r in ((resolved or {}).get("rows") or [])}

    ranking = scores.get("ranking") or []
    hunts = sorted(rp.glob("hunts/*.json"))
    rows = []
    for r in ranking:
        tk = r.get("ticker")
        bl = load(rp / "baselines" / f"{tk}.json") or {}
        tape = bl.get("tape") or {}
        pos = bl.get("positioning") or {}
        diag = r.get("diagnostics") or {}
        rr = res_rows.get(tk) or {}
        move = move_of(rr)
        impact = r.get("impact_sum")

        row = {
            "market": spec["stage"],
            "submarket": (bl.get("submarket") or rr.get("submarket")
                          or spec["stage"].lower()),
            "run": rel,
            "run_date": run_date,
            "event_date": bl.get("event_date") or event_date,
            "ticker": tk,
            "company": bl.get("company") or rr.get("company"),
            "industry": bl.get("industry"),
            "session": bl.get("session") or rr.get("session"),
            "session_unresolved": bl.get("session_unresolved"),
            "rank": r.get("rank"),
            "rankable": r.get("rankable", True),
            "not_rankable_because": r.get("not_rankable_because"),
            "impact_sum": impact,
            "conviction": None if impact is None else abs(impact),
            "n_findings": len(r.get("findings") or []),
            "impact_sum_pre_lessons": diag.get("impact_sum_pre_lessons"),
            "impact_sum_pre_local": diag.get("impact_sum_pre_local"),
            "pre_local_variable": diag.get("pre_local_variable"),
            "priced_lean_pct": r.get("priced_lean_pct", bl.get("priced_lean_pct")),
            "baseline_quality": diag.get("baseline_quality"),
            "lean_components": bl.get("lean_components") or {},
            "run_up_20d_pct": tape.get("run_up_20d_pct"),
            "run_up_5d_pct": tape.get("run_up_5d_pct"),
            "spot": tape.get("spot"),
            "currency": tape.get("currency"),
            "turnover_usd": tape.get("median_turnover_usd_20d"),
            "realised_vol_20d_pct": tape.get("realised_vol_20d_pct"),
            "analyst_count": (bl.get("consensus") or {}).get("analyst_count"),
            "analyst_band": (bl.get("consensus") or {}).get("analyst_band"),
            "anchor_covered": bl.get("anchor_covered", rr.get("anchor_covered")),
            "anchor_state": rr.get("anchor_state"),
            "positioning_covered": pos.get("covered"),
            "short_ratio_pct": pos.get("short_ratio_pct", pos.get("short_pct")),
            "filer_type": (bl.get("history") or {}).get("filer_type",
                                                        rr.get("filer_type")),
            "event_occurred": rr.get("event_occurred", bl.get("event_occurred")),
            "move_pending": rr.get("move_pending"),
            "realised_move_pct": rd(move, 3),
        }
        # The board return: what the hunt's own sign earned. Short a negative
        # prediction, long a positive one -- the same convention the US ledger
        # uses, so the two are read the same way.
        row["ret"] = (None if move is None or not impact
                      else rd(move if impact > 0 else -move, 3))
        row["sign_right"] = (None if move is None or not impact
                             else (impact > 0) == (move > 0))
        rows.append(row)

    meta = {
        "market": spec["stage"],
        "run": rel,
        "run_date": run_date,
        "event_date": event_date,
        "names": scores.get("names", len(ranking)),
        "rankable": scores.get("rankable"),
        "ranking_key": scores.get("ranking_key"),
        "conviction_floor": scores.get("conviction_floor"),
        "n_rows": len(rows),
        "n_hunts": len(hunts),
        "n_findings": sum(r["n_findings"] for r in rows),
        "n_resolved": sum(1 for r in rows if r["realised_move_pct"] is not None),
        "n_killed": sum(1 for r in rows if r["event_occurred"] is False),
        "scored_utc": scores.get("generated_utc"),
        "sealed_utc": universe.get("generated_utc"),
        "resolved_utc": (resolved or {}).get("resolved_utc"),
        "has_resolved_file": resolved is not None,
        "validation_only": universe.get("validation_only"),
        "market_closed": universe.get("market_closed"),
        "cap": universe.get("cap"),
        "min_turnover_usd": universe.get("min_turnover_usd"),
        "selection": universe.get("selection") or {},
        "resolver_stats": {k: v for k, v in (resolved or {}).items()
                           if k in ("stats", "rankers", "components",
                                    "by_anchor_covered", "by_filer_type",
                                    "per_market", "lean_vs_free_control_rho",
                                    "lean_vs_free_control_n", "confirmation",
                                    "n_usable", "n_resolved", "warning")},
    }
    # A day with no names has two causes that look identical and mean opposite
    # things, which is the whole reason jp_universe.py writes `market_closed`:
    # the exchange was shut, or the scoring failed. Only the second is a problem.
    meta["scored"] = (rp / "edge-scores.json").exists()
    if not ranking:
        if meta["market_closed"]:
            meta["quiet_reason"] = f"beurs dicht: {meta['market_closed']}"
        elif not meta["scored"]:
            # Hunts on disk and no edge-scores.json is a run that is still going,
            # not a day that produced nothing. The live stage EU run of 09-23 sat
            # in exactly that state -- four hunts written, scoring not reached --
            # and the two read identically from here unless the hunts are counted.
            meta["quiet_reason"] = (
                f"gejaagd ({len(hunts)} hunts), nog niet gescoord" if hunts
                else "geen edge-scores.json: geen naam gehaald deze dag")
        else:
            meta["quiet_reason"] = "edge-scores.json zonder ranking-rijen"
            problems.append(f"{rel}: edge-scores.json has no ranking rows")
    return meta, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="*", default=None,
                    help="run directory globs; default is every europe/japan/"
                         "australia/canada run under research/")
    ap.add_argument("--resolve", action="store_true",
                    help="for a run whose event date has passed and which has no "
                         "resolved file, call the market's own resolver. Costs "
                         "network; a run is only ever resolved once.")
    ap.add_argument("--timeout", type=int, default=300,
                    help="seconds per resolver call (default 300)")
    ap.add_argument("--out", default=str(DATA / "markets.json"))
    a = ap.parse_args()

    today = date.today().isoformat()
    problems, markets = [], {}
    for code, spec in STAGES.items():
        pats = a.runs or [f"research/*/*/*/{spec['dir']}"]
        runs = []
        for pat in pats:
            runs.extend(sorted(glob.glob(str(ROOT / pat))))
        runs = [r for r in runs if Path(r).name == spec["dir"]]

        if a.resolve:
            for run in runs:
                rp = Path(run)
                if rp.parent.name >= today:
                    continue                      # the window has not closed yet
                if not (rp / "edge-scores.json").exists():
                    continue                      # nothing was scored: a shut
                                                  # exchange, or a day with no
                                                  # eligible name. Not a failure,
                                                  # and every resolver refuses it.
                if not needs_resolving(rp / spec["resolved"]):
                    continue
                err = resolve_run(run, spec, a.timeout)
                if err:
                    problems.append(err)

        metas, rows = [], []
        for run in runs:
            m, rs = collect_run(run, spec, problems)
            metas.append(m)
            rows.extend(rs)
        metas.sort(key=lambda m: m["run_date"])
        rows.sort(key=lambda r: (r["run_date"], -(r["conviction"] or 0)))
        markets[code] = {
            "market": code,
            "label": spec["label"],
            "stage": spec["stage"],
            "dir": spec["dir"],
            "resolved_file": spec["resolved"],
            "resolver": spec["resolver"],
            "runs": metas,
            "names": rows,
            "n_runs": len(metas),
            "n_names": len(rows),
            "n_resolved": sum(1 for r in rows if r["realised_move_pct"] is not None),
        }
        print(f"{code}: {len(metas)} runs, {len(rows)} names, "
              f"{markets[code]['n_resolved']} with a realised move")

    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "markets": markets,
        "problems": problems,
        "note": ("Research record only. Stages EU, J and AU place no orders, so "
                 "there is no money level here and no equity curve. A realised "
                 "move comes from the market's own resolver and from nowhere "
                 "else."),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False,
                                      separators=(",", ":")) + "\n",
                           encoding="utf-8")
    for p in problems:
        print(f"  problem: {p}")
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
