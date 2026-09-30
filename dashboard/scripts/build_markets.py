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
import re
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
           "resolved": "eu-resolved.json",
           "skill": ".claude/skills/researcher-europe-hunt/SKILL.md",
           "lessons": "researcher_europe/LESSONS.md"},
    "JP": {"dir": "japan", "label": "Japan", "stage": "J",
           "resolver": "researcher_japan/scripts/jp_resolve.py",
           "resolved": "jp-resolved.json",
           "skill": ".claude/skills/researcher-japan-hunt/SKILL.md",
           "lessons": "researcher_japan/LESSONS.md"},
    "AU": {"dir": "australia", "label": "Australië", "stage": "AU",
           "resolver": "researcher_australia/scripts/au_resolve.py",
           "resolved": "au-resolved.json",
           "skill": ".claude/skills/researcher-australia-hunt/SKILL.md",
           "lessons": "researcher_australia/LESSONS.md"},
    "CA": {"dir": "canada", "label": "Canada", "stage": "CA",
           "resolver": "researcher_canada/scripts/ca_resolve.py",
           "resolved": "canada-resolved.json",
           "skill": ".claude/skills/researcher-canada-hunt/SKILL.md",
           "lessons": "researcher_canada/LESSONS.md"},
}

# Which agent definition hunted a name. Europe has seven, keyed on the
# submarket, exactly as the stage EU skill's dispatch table says; the other
# three markets have one each.
EU_HUNTER = {"uk": "uk", "de": "de", "fr": "fr", "it": "it", "es": "es",
             "pl": "pl", "se": "nordic", "dk": "nordic", "no": "nordic",
             "fi": "nordic"}
ONE_HUNTER = {"EU": None, "JP": "jp", "AU": "au", "CA": "ca"}


def hunter_of(code, submarket):
    h = ONE_HUNTER[code] or EU_HUNTER.get((submarket or "").lower())
    return f"unpriced-hunter-{h}" if h else None


def agent_path(hunter):
    return f".claude/agents/{hunter}.md" if hunter else None


# ------------------------------------------------------------------ prompts
#
# "Is the prompt working" is only answerable if every hunt carries the prompt it
# ran under. The hunters do not write that down, so it is recovered from git:
# the version of an agent definition (or skill, or LESSONS.md) that sat in the
# tree of the commit that first ADDED the hunt file. That is the closest commit
# to the moment the hunter was spawned, and the session that spawned it had that
# tree checked out, give or take a prompt change merged mid-run.
#
# A version is a distinct blob on the first-parent history of HEAD, so a merge
# counts on the day it landed on main and not on the day its branch was
# written. Its id is the commit that introduced it, which is shared across the
# seven European hunters when one commit changed all seven -- that is what makes
# "before and after 2026-09-28" one comparison and not seven.
#
# A shallow clone cannot do any of this: every file looks added in the one
# commit it has, which would attribute every hunt to today's prompt. So a
# shallow clone carries the attribution over from the previous markets.json and
# marks what it cannot attribute, rather than inventing it.

def git(*args, inp=None):
    try:
        p = subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True,
                           text=True, input=inp, timeout=120)
    except Exception:
        return None
    return p.stdout if p.returncode == 0 else None


def is_shallow():
    out = git("rev-parse", "--is-shallow-repository")
    return out is None or out.strip() != "false"


def blobs(specs):
    """{'<commit>:<path>': blob or None}, in one git call."""
    specs = sorted(set(specs))
    if not specs:
        return {}
    out = git("cat-file", "--batch-check", inp="\n".join(specs) + "\n") or ""
    res = {}
    for spec, line in zip(specs, out.splitlines()):
        parts = line.split()
        res[spec] = parts[0] if len(parts) >= 2 and parts[1] == "blob" else None
    return res


def history(path):
    """Distinct versions of one file on the first-parent history of HEAD,
    oldest first: [{id, commit, date, subject, blob}]."""
    out = git("log", "--first-parent", "--reverse",
              "--format=%H%x09%cI%x09%s", "--", path) or ""
    commits = [l.split("\t", 2) for l in out.splitlines() if l.count("\t") >= 2]
    bl = blobs(f"{c[0]}:{path}" for c in commits)
    vers, last = [], None
    for h, when, subj in commits:
        b = bl.get(f"{h}:{path}")
        if not b or b == last:
            continue
        last = b
        vers.append({"id": h[:8], "commit": h[:8], "date": when[:16].replace("T", " "),
                     "subject": subj[:140], "blob": b})
    return vers


def added_commits(globs_):
    """{repo-relative path: commit that first added it}."""
    out = git("log", "--diff-filter=A", "--format=@@%H", "--name-only", "--",
              *globs_) or ""
    first, cur = {}, None
    for line in out.splitlines():
        if line.startswith("@@"):
            cur = line[2:]
        elif line.strip() and cur:
            first[line.strip()] = cur          # log is newest first: keep oldest
    return first


class Prompts:
    """Attributes each hunt to the prompt versions it ran under."""

    def __init__(self, previous):
        self.shallow = is_shallow()
        self.previous = previous or {}
        self.hist = {}
        self.added = {}
        self.pending = []

    def versions(self, path):
        if path not in self.hist:
            self.hist[path] = [] if self.shallow else history(path)
        return self.hist[path]

    def index(self, code, dirname):
        if not self.shallow:
            self.added.update(added_commits(
                [f"research/*/*/*/{dirname}/hunts/*.json"]))

    def attribute(self, hunt_rel, paths, prev_key):
        """{'hunter': id, 'skill': id, 'lessons': id} for one hunt file."""
        if self.shallow:
            return (self.previous.get(prev_key) or {}).get("prompt") or {
                k: None for k in paths}
        commit = self.added.get(hunt_rel)
        if not commit:
            return {k: None for k in paths}
        specs = {k: f"{commit}:{p}" for k, p in paths.items() if p}
        bl = blobs(specs.values())
        out = {}
        for k, p in paths.items():
            b = bl.get(specs.get(k))
            if not p or not b:
                out[k] = None
                continue
            v = next((v for v in self.versions(p) if v["blob"] == b), None)
            # A blob that never sat on main: the hunt ran from a branch whose
            # prompt was later changed again before merging. Named, not guessed.
            out[k] = v["id"] if v else f"tak:{b[:7]}"
        return out


# Hunter prose -> did the local-language sources add anything. A heuristic and
# labelled as one on the page: language_note is free text by design, and the
# control that measured this with a number was retired on 2026-09-22.
NOTHING = re.compile(
    r"\bnothing\b|\bno (additional|new|extra|further)\b|identical|same content|"
    r"did not (add|carry)|confirmation rather than|added no\b|not add", re.I)


def lang_added(note):
    if not note:
        return None
    items = note if isinstance(note, list) else [note]
    items = [str(x) for x in items if str(x).strip()]
    if not items:
        return None
    return any(not NOTHING.search(x) for x in items)


def days_between(a, b):
    try:
        return (date.fromisoformat(str(a)[:10]) - date.fromisoformat(str(b)[:10])).days
    except Exception:
        return None


def hunt_summary(h, event_date):
    """The parts of one hunt file that say whether the prompt was followed and
    what it predicted beside the ranked number."""
    if not h:
        return None
    fs = h.get("findings") or []
    pre = h.get("pre_lessons") or {}
    final_sum = sum((f.get("expected_impact_pct") or 0) for f in fs)
    pre_sum = pre.get("impact_sum_pct")
    lessons_changed = None
    if pre_sum is not None:
        lessons_changed = (abs((pre_sum or 0) - final_sum) > 1e-9
                           or (pre.get("findings_count") is not None
                               and pre.get("findings_count") != len(fs)))
    finds = []
    for f in fs:
        lang = (f.get("source_language") or "").lower() or None
        finds.append({
            "x": f.get("expected_impact_pct"),
            "lo": f.get("impact_low_pct"),
            "hi": f.get("impact_high_pct"),
            "on": f.get("lands_on"),
            "dt": days_between(f.get("resolves_by"), event_date),
            "lang": lang,
            "pass": f.get("found_in_pass"),
            "src": bool(str(f.get("source") or "").startswith("http")),
            "quote": bool(f.get("original_quote")),
            "ind": f.get("independence"),
        })
    return {
        "synthetic": bool(h.get("SYNTHETIC")),
        "event_confirmed": h.get("event_confirmed"),
        "expected_move_pct": h.get("expected_move_pct"),
        "abs_move_pct": h.get("abs_move_pct"),
        "p_up": h.get("p_up"),
        "print_vs_bar_pct": h.get("print_vs_bar_pct"),
        "already_public": h.get("already_public"),
        "new_in_release": h.get("new_in_release"),
        "sources_used": h.get("sources_used"),
        "n_outside": len(h.get("outside_window") or []),
        "n_nothing": len(h.get("searched_and_found_nothing") or []),
        "lessons_changed": lessons_changed,
        "has_language_note": h.get("language_note") is not None,
        "lang_added": lang_added(h.get("language_note")),
        "findings": finds,
    }


def postmortem_of(p):
    if not p:
        return None
    fsc = p.get("findings_scored") or []
    right = [x.get("fact_correct") for x in fsc if x.get("fact_correct") is not None]
    prior = p.get("prior_update")
    return {
        "release_found": p.get("release_found"),
        "release_in_window": p.get("release_in_window"),
        "print_vs_bar_actual_pct": p.get("print_vs_bar_actual_pct"),
        "guidance_change": p.get("guidance_change"),
        "prior_update": (prior.get("value") if isinstance(prior, dict) else prior),
        "moved_on": p.get("moved_on"),
        "facts_n": len(right),
        "facts_right": sum(1 for x in right if x),
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


def collect_run(run, spec, problems, code=None, prompts=None):
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
    # One hunt per name under the current contract; the first file wins if a
    # name was hunted twice, which is the h1 by sort order.
    hunt_by = {}
    for hp in hunts:
        hd = load(hp)
        tk = (hd or {}).get("ticker") or hp.stem.rsplit("-h", 1)[0]
        hunt_by.setdefault(str(tk), (hp, hd))
    pms = {}
    for pp in sorted(rp.glob("*-postmortem.json")):
        doc = load(pp)
        for p in (doc if isinstance(doc, list) else (doc or {}).get("rows") or []):
            if isinstance(p, dict) and p.get("ticker"):
                pms[str(p["ticker"])] = p
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
        hp, hd = hunt_by.get(str(tk), (None, None))
        row["hunter"] = hunter_of(code, row["submarket"]) if code else None
        row["hunt"] = hunt_summary(hd, row["event_date"])
        row["pm"] = postmortem_of(pms.get(str(tk)))
        row["prompt"] = None
        if prompts is not None and hp is not None:
            hrel = str(hp.relative_to(ROOT))
            row["prompt"] = prompts.attribute(
                hrel, {"hunter": agent_path(row["hunter"]),
                       "skill": spec.get("skill"), "lessons": spec.get("lessons")},
                f"{rel}|{tk}")
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


def prompt_catalogue(code, spec, rows, prompts, prev_doc):
    """Every version of every prompt file this market's hunts ran under, with
    the commit subject that says what changed. The page groups by `id`."""
    if prompts.shallow:
        return ((prev_doc.get("markets") or {}).get(code) or {}).get("prompts") or {}
    hunters = sorted({r["hunter"] for r in rows if r.get("hunter")})
    if code != "EU" and ONE_HUNTER[code]:
        hunters = [f"unpriced-hunter-{ONE_HUNTER[code]}"]
    cat = {"hunter": {}, "skill": {}, "lessons": {}}
    for h in hunters:
        cat["hunter"][h] = [{k: v for k, v in x.items() if k != "blob"}
                            for x in prompts.versions(agent_path(h))]
    for k in ("skill", "lessons"):
        cat[k][spec[k]] = [{kk: v for kk, v in x.items() if kk != "blob"}
                           for x in prompts.versions(spec[k])]
    return cat


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
    prev_doc = load(a.out) or {}
    previous = {f"{r.get('run')}|{r.get('ticker')}": r
                for m in (prev_doc.get("markets") or {}).values()
                for r in (m.get("names") or [])}
    prompts = Prompts(previous)
    if prompts.shallow:
        problems.append("shallow git clone: promptversies overgenomen uit de vorige "
                        "markets.json; nieuwe hunts staan als onbekend. CI moet "
                        "met fetch-depth: 0 uitchecken.")
    for code, spec in STAGES.items():
        prompts.index(code, spec["dir"])
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
            m, rs = collect_run(run, spec, problems, code, prompts)
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
            "prompts": prompt_catalogue(code, spec, rows, prompts, prev_doc),
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
