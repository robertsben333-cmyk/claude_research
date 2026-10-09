#!/usr/bin/env python3
"""Which hunter prompt, and which model, produced a prediction.

    python3 scripts/provenance.py registry            # rebuild config/prompt-versions.json
    python3 scripts/provenance.py check               # every live hunter is registered
    python3 scripts/provenance.py stamp --run <RUN> --market JP [--orchestrator-model M]
    python3 scripts/provenance.py backfill [--force]  # past runs, from git history
    python3 scripts/provenance.py show --run <RUN>

WHY THIS EXISTS. Every market's hunter definition has been rewritten several times and
the model behind the `opus` alias changed underneath all of them on 2026-09-22. A
dashboard that pools every day as if one method produced it cannot say whether a change
helped. So each run carries `provenance.json`: for every hunter agent the run used, the
prompt VERSION (`jp.v4`), the exact definition blob, the model alias in its frontmatter
and the model that alias served, plus the LESSONS file, the shared hunter core and the
skill as blobs.

VERSIONS ARE DERIVED, NOT TYPED. A version is a distinct content of the agent file as it
stood on origin/main's first-parent history, numbered in order of first appearance, and
`from_utc` is when that content reached main -- which is what a Routine clones. A
definition edited on a branch and not yet merged is registered with `from_utc: null`
(`pending_merge`), so a run stamped from the branch is still identified, and date-based
inference never assigns it to a run that cloned main. `label` is the one hand-written
field and survives regeneration, keyed by blob.

THE MODEL IS INFERRED UNLESS RECORDED. A hunter subagent cannot report which model served
it, and its frontmatter says an ALIAS (`opus`, `sonnet`). `MODEL_TIMELINE` maps the alias
to what it served by date; the `opus` switch from claude-opus-5 to claude-opus-5-5 was
observed between 18:56 and 19:09 UTC on 2026-09-22 (CLAUDE.md, "The hunters moved to
Opus 5.5"). `model_basis` says `alias_timeline` for that, and `recorded` only where a
session passed the model it actually saw. The orchestrating session's model is separate
and is only ever recorded, never inferred.

BACKFILL IS GIT-DERIVED. For a past run, the version is the blob of the definition on
origin/main at the moment the run sealed its universe. That needs full history
(`git fetch --unshallow`), which a Routine's depth-1 clone does not have -- so backfill
is run once from a development session and its files are committed, and the build
scripts never need git.
"""
import argparse
import glob
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "prompt-versions.json"

# Every hunter this repo has run live, with the short prefix its version ids carry.
HUNTERS = {
    "unpriced-hunter": "us",
    "unpriced-hunter-sonnet": "us-sonnet",
    "unpriced-searcher": "us-searcher",
    "deep-question-researcher": "us-deep",
    "unpriced-hunter-jp": "jp",
    "unpriced-hunter-uk": "uk",
    "unpriced-hunter-de": "de",
    "unpriced-hunter-fr": "fr",
    "unpriced-hunter-nordic": "nordic",
    "unpriced-hunter-it": "it",
    "unpriced-hunter-es": "es",
    "unpriced-hunter-pl": "pl",
    "unpriced-hunter-au": "au",
    "unpriced-hunter-ca": "ca",
    "reversal-hunter": "rev",
}

# Run directory name -> market code, the hunters it uses, and the files that shape a
# prediction besides the hunter definition.
MARKETS = {
    "US": {"dir": "edge", "hunters": ["unpriced-hunter"],
           "lessons": "researcher_us/LESSONS.md",
           "skill": ".claude/skills/earnings-edge-hunt/SKILL.md"},
    "US-S": {"dir": "edge-sonnet", "hunters": ["unpriced-hunter-sonnet"],
             "lessons": "researcher_us/LESSONS.md",
             "skill": ".claude/skills/earnings-edge-hunt-sonnet/SKILL.md"},
    # Stage E-P (2026-10-01): the searcher is the only hunter; the four panel judges are
    # not hunters and are recorded by the stage in provenance.json's `panel` block.
    "US-P": {"dir": "edge-panel", "hunters": ["unpriced-searcher"],
             "lessons": "researcher_us/LESSONS.md",
             "skill": ".claude/skills/earnings-edge-panel/SKILL.md"},
    # Stage D (2026-10-07): three names a day, one deep researcher each, frozen key
    # questions and a frozen quick first read. Research only.
    "US-D": {"dir": "edge-deep", "hunters": ["deep-question-researcher"],
             "lessons": "researcher_us/LESSONS.md",
             "skill": ".claude/skills/earnings-deep-research/SKILL.md"},
    "JP": {"dir": "japan", "hunters": ["unpriced-hunter-jp"],
           "lessons": "researcher_japan/LESSONS.md",
           "skill": ".claude/skills/researcher-japan-hunt/SKILL.md"},
    "EU": {"dir": "europe",
           "hunters": ["unpriced-hunter-uk", "unpriced-hunter-de", "unpriced-hunter-fr",
                       "unpriced-hunter-nordic", "unpriced-hunter-it",
                       "unpriced-hunter-es", "unpriced-hunter-pl"],
           "lessons": "researcher_europe/LESSONS.md",
           "skill": ".claude/skills/researcher-europe-hunt/SKILL.md"},
    "AU": {"dir": "australia", "hunters": ["unpriced-hunter-au"],
           "lessons": "researcher_australia/LESSONS.md",
           "skill": ".claude/skills/researcher-australia-hunt/SKILL.md"},
    "CA": {"dir": "canada", "hunters": ["unpriced-hunter-ca"],
           "lessons": "researcher_canada/LESSONS.md",
           "skill": ".claude/skills/researcher-canada-hunt/SKILL.md"},
    "R": {"dir": "reversal", "hunters": ["reversal-hunter"],
          "lessons": "researcher_reversal/LESSONS.md",
          "skill": ".claude/skills/researcher-reversal-hunt/SKILL.md"},
}
DIR_TO_MARKET = {v["dir"]: k for k, v in MARKETS.items()}
CORE = "config/hunter-core.md"

# Stage EU's submarket -> the hunter that hunts it (the skill's own table).
EU_SUBMARKET_HUNTER = {"uk": "unpriced-hunter-uk", "de": "unpriced-hunter-de",
                       "fr": "unpriced-hunter-fr", "se": "unpriced-hunter-nordic",
                       "dk": "unpriced-hunter-nordic", "no": "unpriced-hunter-nordic",
                       "fi": "unpriced-hunter-nordic", "it": "unpriced-hunter-it",
                       "es": "unpriced-hunter-es", "pl": "unpriced-hunter-pl"}

# What an alias served, by time. Boundaries are UTC and come from observation, not from
# an announcement; between `until` of one entry and `from` of the next the model is
# ambiguous and is reported as such.
MODEL_TIMELINE = {
    "opus": [
        {"until_utc": "2026-09-22T18:56:00+00:00", "model": "claude-opus-5"},
        {"from_utc": "2026-09-22T19:09:00+00:00", "model": "claude-opus-5-5"},
    ],
    # Stage E-S is the only Sonnet hunter and started 2026-10-01. Nothing in this repo
    # has observed which Sonnet the alias serves to a subagent, so it is not guessed.
    "sonnet": [],
}
SHORT_MODEL = {"claude-opus-5": "Opus 5", "claude-opus-5-5": "Opus 5.5",
               "claude-sonnet-5": "Sonnet 5", "claude-sonnet-5-5": "Sonnet 5.5",
               "claude-fable-5-1": "Fable 5.1"}


def git(*args, check=True):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()


def blob_of_file(path):
    """The git blob id of a file on disk, which needs no history: `git hash-object`."""
    f = ROOT / path
    if not f.exists():
        return None
    data = f.read_bytes()
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    return h


def blob_at(commit, path):
    out = subprocess.run(["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT,
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else None


def frontmatter_model(text):
    m = re.search(r"^model:\s*(\S+)", text or "", re.M)
    return m.group(1) if m else None


def parse_utc(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def served_model(alias, at):
    """(model, basis) for an alias at a moment. basis: alias_timeline / ambiguous /
    not_recorded."""
    # A frontmatter that pins a full model id (stage E-P, 2026-10-01) names its model;
    # nothing has to be inferred from a timeline.
    if (alias or "").startswith("claude-"):
        return alias, "pinned_in_frontmatter"
    tl = MODEL_TIMELINE.get(alias or "")
    if not tl or at is None:
        return None, "not_recorded"
    for e in tl:
        lo, hi = parse_utc(e.get("from_utc")), parse_utc(e.get("until_utc"))
        if (lo is None or at >= lo) and (hi is None or at < hi):
            return e["model"], "alias_timeline"
    return None, "ambiguous"


# ----------------------------------------------------------------- the registry
def build_registry(ref="origin/main"):
    if git("rev-parse", "--is-shallow-repository") == "true":
        raise SystemExit("shallow clone: run `git fetch --unshallow origin` first; "
                         "versions are derived from the full history of main")
    old = load_registry()
    labels = {}
    for h in (old.get("hunters") or {}).values():
        for v in h.get("versions") or []:
            if v.get("label"):
                labels[v["blob"]] = v["label"]
    out = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "source": f"first-parent history of {ref}, plus the working tree",
           "model_timeline": MODEL_TIMELINE, "hunters": {}}
    for agent, short in HUNTERS.items():
        path = f".claude/agents/{agent}.md"
        commits = git("rev-list", "--first-parent", "--reverse",
                      "--format=%H %cI", ref, "--", path).splitlines()
        seen, versions, prev = {}, [], None
        for line in commits:
            if line.startswith("commit "):
                continue
            sha, when = line.split(" ", 1)
            b = blob_at(sha, path)
            if b is None or b == prev:
                prev = b
                continue
            prev = b
            if b not in seen:      # a revert to an earlier text keeps its old id
                seen[b] = len(seen) + 1
            text = git("show", f"{sha}:{path}")
            versions.append({
                "id": f"{short}.v{seen[b]}", "blob": b,
                "from_utc": parse_utc(when).astimezone(timezone.utc).isoformat(),
                "commit": sha[:10],
                "subject": git("log", "-1", "--format=%s", sha),
                "model_alias": frontmatter_model(text),
            })
        cur = blob_of_file(path)
        if cur and cur not in seen:
            text = (ROOT / path).read_text(encoding="utf-8")
            versions.append({"id": f"{short}.v{len(seen) + 1}", "blob": cur,
                             "from_utc": None, "commit": None,
                             "subject": "working tree, not yet on main",
                             "pending_merge": True,
                             "model_alias": frontmatter_model(text)})
        for v in versions:
            if v["blob"] in labels:
                v["label"] = labels[v["blob"]]
        out["hunters"][agent] = {"file": path, "short": short, "versions": versions}
    out["stages"] = stage_versions(out)
    return out


STAGE_SHORT = {"US": "us", "US-S": "us-sonnet", "US-P": "us-panel", "US-D": "us-deep", "JP": "jp", "EU": "eu", "AU": "au",
               "CA": "ca", "R": "rev"}


def stage_versions(reg):
    """A stage gets a new version whenever ANY of its hunters changes. For a stage with
    one hunter this is that hunter's numbering; for stage EU it folds seven language
    hunters, which change together, into one sequence the dashboard can filter on."""
    out = {}
    for market, spec in MARKETS.items():
        times = sorted({v["from_utc"] for a in spec["hunters"]
                        for v in reg["hunters"][a]["versions"] if v.get("from_utc")})
        epochs, last = [], None
        for t in times:
            at = parse_utc(t)
            hmap = {a: (version_at(a, at, reg) or {}).get("id") for a in spec["hunters"]}
            if hmap == last:
                continue
            last = hmap
            new = [v for a in spec["hunters"] for v in reg["hunters"][a]["versions"]
                   if v.get("from_utc") == t]
            epochs.append({"id": f"{STAGE_SHORT[market]}.v{len(epochs) + 1}",
                           "from_utc": t, "hunters": hmap,
                           "label": next((v["label"] for v in new if v.get("label")), None),
                           "subject": new[0]["subject"] if new else None})
        pend = {a: next((v["id"] for v in reg["hunters"][a]["versions"]
                         if v.get("pending_merge")), None) for a in spec["hunters"]}
        if any(pend.values()):
            hmap = dict(last or {})
            hmap.update({a: i for a, i in pend.items() if i})
            new = [v for a in spec["hunters"] for v in reg["hunters"][a]["versions"]
                   if v.get("pending_merge")]
            epochs.append({"id": f"{STAGE_SHORT[market]}.v{len(epochs) + 1}",
                           "from_utc": None, "pending_merge": True, "hunters": hmap,
                           "label": next((v["label"] for v in new if v.get("label")), None),
                           "subject": "working tree, not yet on main"})
        out[market] = epochs
    return out


def stage_version_for(market, hunter_ids, reg=None):
    """The stage version whose hunter map equals the versions a run used."""
    reg = reg or load_registry()
    for e in reversed((reg.get("stages") or {}).get(market) or []):
        if all(e["hunters"].get(a) == i for a, i in hunter_ids.items() if i):
            return e
    return None


def load_registry():
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return {}


def version_of(agent, blob, reg=None):
    reg = reg or load_registry()
    for v in ((reg.get("hunters") or {}).get(agent) or {}).get("versions") or []:
        if v["blob"] == blob:
            return v
    return None


def version_at(agent, at, reg=None):
    """The version that was on main at `at`: the last one whose from_utc <= at."""
    reg = reg or load_registry()
    best = None
    for v in ((reg.get("hunters") or {}).get(agent) or {}).get("versions") or []:
        f = parse_utc(v.get("from_utc"))
        if f is not None and at is not None and f <= at:
            best = v
    return best


def check():
    reg, bad = load_registry(), []
    for agent in HUNTERS:
        b = blob_of_file(f".claude/agents/{agent}.md")
        if b and not version_of(agent, b, reg):
            bad.append(agent)
    return bad


# -------------------------------------------------------------- a run's record
def seal_time(run):
    """When the run read its tree: the earliest timestamp its own files carry, else the
    first commit that added the directory."""
    rp = Path(run)
    cands = []
    for name in ("universe.json", "edge-universe.json"):
        d = _load(rp / name) or {}
        for k in ("generated_utc", "built_utc", "resolved_utc", "sealed_utc"):
            if d.get(k):
                cands.append(parse_utc(d[k]))
    for f in sorted((rp / "baselines").glob("*.json"))[:3]:
        d = _load(f) or {}
        for k in ("sealed_utc", "as_of_utc"):
            if d.get(k):
                cands.append(parse_utc(d[k]))
    cands = [c for c in cands if c]
    if cands:
        return min(cands), "run_files"
    rel = str(rp.relative_to(ROOT)) if str(rp).startswith(str(ROOT)) else str(rp)
    first = git("log", "--diff-filter=A", "--reverse", "--format=%cI", "--", rel,
                check=False).splitlines()
    if first:
        return parse_utc(first[0]), "first_commit"
    return None, "unknown"


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def hunter_record(agent, blob, at, reg, basis, hunter_model=None):
    v = version_of(agent, blob, reg) if blob else None
    alias = (v or {}).get("model_alias")
    if alias is None and blob and blob == blob_of_file(f".claude/agents/{agent}.md"):
        alias = frontmatter_model((ROOT / f".claude/agents/{agent}.md").read_text())
    if hunter_model:
        model, mbasis = hunter_model, "recorded"
    else:
        model, mbasis = served_model(alias, at)
    return {"agent": agent,
            "prompt_version": (v or {}).get("id") or (f"unregistered-{blob[:8]}"
                                                      if blob else None),
            "prompt_label": (v or {}).get("label"),
            "prompt_subject": (v or {}).get("subject"),
            "prompt_from_utc": (v or {}).get("from_utc"),
            "definition_blob": blob,
            "model_alias": alias, "model": model, "model_basis": mbasis,
            "basis": basis}


def stamp(run, market, orchestrator_model=None, hunter_model=None, force=False):
    """Record what is in the tree NOW. Call it from the session that runs the stage,
    before the hunters are spawned, so it records the definitions they will read."""
    rp = Path(run)
    out = rp / "provenance.json"
    if out.exists() and not force:
        return _load(out)
    spec = MARKETS[market]
    reg = load_registry()
    now = datetime.now(timezone.utc)
    doc = {"market": market, "run": _rel(rp),
           "stamped_utc": now.isoformat(timespec="seconds"),
           "basis": "recorded_at_run",
           "orchestrator_model": orchestrator_model,
           "orchestrator_model_basis": "recorded" if orchestrator_model else "not_recorded",
           "hunters": {a: hunter_record(a, blob_of_file(f".claude/agents/{a}.md"), now,
                                        reg, "recorded_at_run", hunter_model)
                       for a in spec["hunters"]},
           "files": {k: blob_of_file(p) for k, p in
                     (("lessons", spec["lessons"]), ("skill", spec["skill"]),
                      ("hunter_core", CORE))}}
    doc["stage_version"] = _stage_block(market, doc, reg)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return doc


def backfill_one(run, market, reg, ref="origin/main", force=False):
    rp = Path(run)
    out = rp / "provenance.json"
    if out.exists():
        prev = _load(out) or {}
        if prev.get("basis") == "recorded_at_run":
            return "kept (recorded at run; never overwritten)"
        if not force:
            return "kept"
    at, tbasis = seal_time(rp)
    if at is None:
        return "no seal time"
    commit = git("rev-list", "-1", "--first-parent", f"--before={at.isoformat()}", ref,
                 check=False)
    if not commit:
        return "no commit on main before the seal"
    spec = MARKETS[market]
    doc = {"market": market, "run": _rel(rp),
           "stamped_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "basis": "backfilled_from_git",
           "basis_note": ("the tree on main when the run sealed; a run made from a "
                          "development branch would have read a different tree"),
           "seal_utc": at.isoformat(), "seal_time_basis": tbasis,
           "main_commit": commit[:10],
           "orchestrator_model": None, "orchestrator_model_basis": "not_recorded",
           "hunters": {a: hunter_record(a, blob_at(commit, f".claude/agents/{a}.md"), at,
                                        reg, "backfilled_from_git")
                       for a in spec["hunters"]},
           "files": {k: blob_at(commit, p) for k, p in
                     (("lessons", spec["lessons"]), ("skill", spec["skill"]),
                      ("hunter_core", CORE))}}
    doc["stage_version"] = _stage_block(market, doc, reg)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return f"{list(doc['hunters'].values())[0]['prompt_version']} @ {at:%Y-%m-%d %H:%M}"


def _stage_block(market, doc, reg):
    ids = {a: h.get("prompt_version") for a, h in doc["hunters"].items()
           if h.get("prompt_version") and not str(h["prompt_version"]).startswith("unreg")}
    e = stage_version_for(market, ids, reg) if ids else None
    return ({"id": e["id"], "label": e.get("label") or e.get("subject"),
             "from_utc": e.get("from_utc")} if e else None)


def _rel(p):
    s = str(Path(p).resolve())
    return s[len(str(ROOT)) + 1:] if s.startswith(str(ROOT)) else str(p)


# ------------------------------------------------------- what a build reads
SEPT_OPUS55 = "claude-opus-5-5"
HUNTER_CORE_FROM = "2026-10-01"  # config/hunter-core.md reached main this day


def september_opus55(run, model):
    """An Opus 5.5 hunt from before the shared hunter core: the too-strict prompt.

    Between the alias switch on 2026-09-22 and `config/hunter-core.md`, Opus 5.5 filed a
    third of what it surfaced and sized near zero; the operator ruled that prompt a
    mistake, not a habit to measure against (2026-10-01). A run counts as one when its
    hunter model is Opus 5.5 and its provenance.json carries no `hunter_core` blob. The
    one definition: `score_report.py` leaves these runs out of its reference set and the
    dashboard offers to leave them out of every number, both through this function."""
    if model != SEPT_OPUS55:
        return False
    prov = _load(Path(run) / "provenance.json")
    if prov is None:
        # No stamp at all (the 2026-10-05 run never wrote one): the absence of a
        # `hunter_core` blob proves nothing, so decide by date. The core was on main
        # from HUNTER_CORE_FROM; a run sealed before it is the September prompt.
        return Path(run).resolve().parent.name < HUNTER_CORE_FROM
    return not (prov.get("files") or {}).get("hunter_core")


def for_row(run, market, submarket=None, reg=None):
    """Flat provenance for one ranked name, for the dashboard. Reads the run's
    provenance.json; without one, infers from the registry by seal time and says so.
    Never calls git."""
    reg = reg or load_registry()
    spec = MARKETS.get(market)
    if not spec:
        return {}
    agent = spec["hunters"][0]
    if market == "EU":
        agent = EU_SUBMARKET_HUNTER.get((submarket or "").lower(), agent)
    doc = _load(Path(run) / "provenance.json")
    h = ((doc or {}).get("hunters") or {}).get(agent)
    if h is None:
        at = None
        for name in ("universe.json",):
            d = _load(Path(run) / name) or {}
            at = parse_utc(d.get("generated_utc") or d.get("built_utc")
                           or d.get("resolved_utc"))
        v = version_at(agent, at, reg) if at else None
        model, mbasis = served_model((v or {}).get("model_alias"), at)
        h = {"agent": agent, "prompt_version": (v or {}).get("id"),
             "prompt_label": (v or {}).get("label"),
             "prompt_subject": (v or {}).get("subject"),
             "prompt_from_utc": (v or {}).get("from_utc"),
             "model_alias": (v or {}).get("model_alias"), "model": model,
             "model_basis": mbasis,
             "basis": "inferred_by_date" if v else "unknown"}
    sv = (doc or {}).get("stage_version")
    if sv is None and h.get("prompt_version"):
        e = stage_version_for(market, {agent: h["prompt_version"]}, reg)
        sv = ({"id": e["id"], "label": e.get("label") or e.get("subject"),
               "from_utc": e.get("from_utc")} if e else None)
    ver, model = (sv or {}).get("id") or h.get("prompt_version"), h.get("model")
    return {
        "prompt_version": ver,
        "prompt_label": ((sv or {}).get("label") or h.get("prompt_label")
                         or h.get("prompt_subject")),
        "prompt_from_utc": (sv or {}).get("from_utc") or h.get("prompt_from_utc"),
        "hunter_version": h.get("prompt_version"),
        "hunter_agent": agent,
        "model": model,
        "model_short": SHORT_MODEL.get(model, model) if model else (
            f"{h.get('model_alias')}?" if h.get("model_alias") else None),
        "model_basis": h.get("model_basis"),
        "orchestrator_model": (doc or {}).get("orchestrator_model"),
        "prov_basis": h.get("basis"),
        "sept_opus55": september_opus55(run, model),
        "prov_key": ("onbekend" if not ver else f"{ver} · " + (
            SHORT_MODEL.get(model, model) if model else
            f"{h.get('model_alias')} (model niet vastgelegd)" if h.get("model_alias")
            else "model onbekend")),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("registry")
    sub.add_parser("check")
    s = sub.add_parser("stamp")
    s.add_argument("--run", required=True)
    s.add_argument("--market", required=True, choices=sorted(MARKETS))
    s.add_argument("--orchestrator-model", default=None,
                   help="session_context.model from get_session, if the session can read it")
    s.add_argument("--hunter-model", default=None,
                   help="only if the session KNOWS what served the hunters")
    s.add_argument("--force", action="store_true")
    b = sub.add_parser("backfill")
    b.add_argument("--force", action="store_true")
    b.add_argument("--ref", default="origin/main")
    sh = sub.add_parser("show")
    sh.add_argument("--run", required=True)
    a = ap.parse_args()

    if a.cmd == "registry":
        reg = build_registry()
        REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")
        for agent, h in reg["hunters"].items():
            print(f"{agent:26s} " + "  ".join(
                v["id"] + ("*" if v.get("pending_merge") else "") for v in h["versions"]))
        print(f"-> {REGISTRY.relative_to(ROOT)}   (* = not yet on main)")
    elif a.cmd == "check":
        bad = check()
        if bad:
            print("unregistered hunter definitions: " + ", ".join(bad) +
                  "\nrun `python3 scripts/provenance.py registry` (needs full history)")
            sys.exit(1)
        print("every live hunter definition is registered")
    elif a.cmd == "stamp":
        d = stamp(a.run, a.market, a.orchestrator_model, a.hunter_model, a.force)
        for h in d["hunters"].values():
            print(f"{h['agent']}: {h['prompt_version']} · {h['model'] or h['model_alias']}"
                  f" ({h['model_basis']})")
    elif a.cmd == "backfill":
        if git("rev-parse", "--is-shallow-repository") == "true":
            raise SystemExit("shallow clone: run `git fetch --unshallow origin` first")
        reg = load_registry()
        for market, spec in MARKETS.items():
            for run in sorted(glob.glob(str(ROOT / f"research/*/*/*/{spec['dir']}"))):
                if Path(run).name != spec["dir"]:
                    continue
                print(f"{market:4s} {_rel(run)}: {backfill_one(run, market, reg, a.ref, a.force)}")
    elif a.cmd == "show":
        print(json.dumps(_load(Path(a.run) / "provenance.json"), ensure_ascii=False,
                         indent=1))


if __name__ == "__main__":
    main()
