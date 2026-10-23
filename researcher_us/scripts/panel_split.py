#!/usr/bin/env python3
"""Stage E-PS: stage E-P's names split over four sessions of at most five, beside E-P.

Built 2026-10-22 on the operator's instruction: "ik heb het gevoel dat bij hoog aantal
tickers het systeem het niet goed doet. dus ik wil even 4 test routines aanmaken, die
ieder max 5 stocks beoordelen, en op de een of andere manier communiceren onderling wie
welk doet". Daily since 2026-10-23, and at the same time as stage E-P ("laat ze
gelijktijdig met e-p lopen zodat ze goed te vergelijken zijn"). The 2026-10-21 run log is
the reason it is worth asking: stage E-P on 30 names left 89 of 118 universe names
unchecked by its one sweep, its searchers reported the session's shared WebSearch budget
running out, and its judges hit a 429 and finished after the close.

Four fresh sessions take stage E-P's names that day from E-P's own sweep, the moment it is
on main, with E-P's sweep rows and sealed baselines copied in. Each session clones MAIN, so
its searcher, judges, scripts and panel history are exactly E-P's, and lays only this
stage's own files over it (`overlay` in config/edge-panel-split.yaml). Each hunts its names
with `unpriced-searcher` while E-P's searchers run, and has its own four blind judges,
scored --dry-run against E-P's history. Places no orders.

  research/<Y>/<M>/<DATE>/edge-split/        plan.json, claims/shard-<k>.json, _run-log.md, summary.{json,md}
  research/<Y>/<M>/<DATE>/edge-split-<k>/    one shard, stage E-P's layout

HOW THE SESSIONS TALK, AND WHERE THEIR OUTPUT GOES: by compare-and-swap commits on
`data_branch` (never main), and only by those. A commit is built on top of the branch's
current tip that adds, replaces or removes exactly the paths in question, and pushed; when
the push is rejected because another session pushed first, the session re-reads the tip
and decides again. Only one of two pushes on the same parent can land, so two sessions can
never hold one shard, and the first plan written is the plan. The session's own checkout
is main and is never committed to, so there is no rebase anywhere and nothing can reach
main through this script.

  python3 researcher_us/scripts/panel_split.py claim   [--shard K --force] [--wait-min 9]
  python3 researcher_us/scripts/panel_split.py log     [--shard K] --heading H --line L [--line L]
  python3 researcher_us/scripts/panel_split.py stamp   --shard K --orchestrator-model M
  python3 researcher_us/scripts/panel_split.py publish --shard K "<commit message>"
  python3 researcher_us/scripts/panel_split.py done    --shard K
  python3 researcher_us/scripts/panel_split.py summary
  python3 researcher_us/scripts/panel_split.py status

`claim` exits 0 with the shard, 3 while stage E-P's sweep is not on main and the start
deadline has not passed (run it again), 2 when the deadline passed without it (stop), 4
when every shard is taken.
"""
import argparse, json, os, random, socket, subprocess, sys, tempfile, time, uuid
from datetime import datetime, time as dtime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[2]
CFG = REPO / "config" / "edge-panel-split.yaml"
ET = ZoneInfo("America/New_York")
PREFIX = "edge-split"
SESSION_ORDER = {"bmo": 0, "amc": 1}
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))


def cfg():
    import yaml
    C = dict((yaml.safe_load(open(CFG)) or {}).get("edge_panel_split") or {})
    if C.get("data_branch") in (None, "", C.get("source_branch", "main"), "main"):
        sys.exit("edge_panel_split.data_branch must name a branch other than main")
    try:
        ep = (yaml.safe_load(open(REPO / "config" / "pipeline.yaml")) or {}).get("edge_panel") or {}
        C.setdefault("ep_hunted_names", int(ep.get("hunted_names")))
    except (OSError, TypeError, ValueError):
        pass
    return C


def now_utc():
    return datetime.now(timezone.utc)


def run_rel(d):
    return f"research/{d:%Y}/{d:%m}/{d.isoformat()}"


def dumps(o):
    return json.dumps(o, indent=1, ensure_ascii=False) + "\n"


def loads(b):
    try:
        return json.loads(b) if b else None
    except ValueError:
        return None


# ---------------------------------------------------------------- git

def git(repo, *a, data=None, env=None, ok=False):
    r = subprocess.run(["git", "-C", str(repo), *a], input=data, capture_output=True, env=env)
    if ok:
        return r
    if r.returncode:
        sys.exit(f"git {' '.join(a)}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout.decode()


def fetch(repo, br):
    """The branch's tip on origin, or None if it does not exist there. Always depth 1: the
    checkout is a shallow clone of main, and nothing here needs history, only tips."""
    a = ["fetch", "-q", "--depth", "1", "origin", f"+refs/heads/{br}:refs/remotes/origin/{br}"]
    for n in range(4):
        r = git(repo, *a, ok=True)
        if r.returncode == 0:
            return git(repo, "rev-parse", f"refs/remotes/origin/{br}").strip()
        if b"couldn't find remote ref" in r.stderr:
            return None
        time.sleep(2 ** n)
    sys.exit(f"git fetch origin {br}: {r.stderr.decode(errors='replace').strip()}")


def show(repo, rev, path):
    if not rev:
        return None
    r = git(repo, "cat-file", "blob", f"{rev}:{path}", ok=True)
    return r.stdout if r.returncode == 0 else None


def ls(repo, rev, path, recursive=False):
    """Names one level under `path` at `rev`, or with recursive=True every file path."""
    if not rev:
        return []
    if recursive:
        r = git(repo, "ls-tree", "-r", "--name-only", rev, "--", path.rstrip("/") + "/", ok=True)
        return r.stdout.decode().split("\n")[:-1] if r.returncode == 0 else []
    r = git(repo, "ls-tree", "--name-only", f"{rev}:{path}", ok=True)
    return r.stdout.decode().split() if r.returncode == 0 else []


def ident(repo):
    env = dict(os.environ)
    name = git(repo, "config", "user.name", ok=True).stdout.decode().strip() or "Earnings Routine"
    mail = git(repo, "config", "user.email", ok=True).stdout.decode().strip() or "earnings-routine@users.noreply.github.com"
    env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=mail, GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=mail)
    return env


def cas(repo, br, decide, message, tries=12):
    """Compare-and-swap on the branch. `decide(tip)` sees the tip (read it with show/ls)
    and returns (changes, value): changes a {path: text | bytes | None} to write on top of
    that tip, None removing the path, or None for the whole thing to write nothing.
    Rejected pushes re-read and decide again, so `decide` must depend on nothing but the
    tip and its own arguments. A change that leaves the tree as it was pushes nothing."""
    for n in range(tries):
        tip = fetch(repo, br)
        if tip is None:
            sys.exit(f"branch {br} does not exist on origin")
        res = decide(tip)
        if res is None:
            return None
        changes, value = res
        if not changes:
            return value
        fd, idx = tempfile.mkstemp(prefix="split-index-", dir=git(repo, "rev-parse", "--absolute-git-dir").strip())
        os.close(fd)
        env = ident(repo)
        env["GIT_INDEX_FILE"] = idx
        try:
            git(repo, "read-tree", tip, env=env)
            for path, data in sorted(changes.items()):
                if data is None:
                    git(repo, "update-index", "--force-remove", "--", path, env=env)
                    continue
                blob = git(repo, "hash-object", "-w", "--stdin",
                           data=data if isinstance(data, bytes) else data.encode("utf-8")).strip()
                git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
            tree = git(repo, "write-tree", env=env).strip()
            if tree == git(repo, "rev-parse", f"{tip}^{{tree}}").strip():
                return value
            commit = git(repo, "commit-tree", tree, "-p", tip, "-m", message, env=env).strip()
        finally:
            os.unlink(idx)
        if git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{br}", ok=True).returncode == 0:
            return value
        time.sleep(1 + random.random() * 2 * (n + 1))
    sys.exit(f"could not push to {br} after {tries} tries: another session keeps moving it")


def session_id(repo, given=None):
    """Stable across calls in one container, so a re-run of `claim` resumes its shard."""
    p = Path(git(repo, "rev-parse", "--absolute-git-dir").strip()) / "panel-split-session"
    if given:
        p.write_text(given)
    if not p.exists():
        p.write_text(f"{socket.gethostname()}-{uuid.uuid4().hex[:8]}")
    return p.read_text().strip()


# ---------------------------------------------------------------- the plan

def assign(names, shards):
    """Round-robin over (event date, session, hunt priority): every shard gets the same
    mix of tonight's and tomorrow's prints and of high and low priority, and within a
    shard the earliest release comes first."""
    order = sorted(names, key=lambda r: (r.get("event_date") or "9999", SESSION_ORDER.get(r.get("session"), 2),
                                         -(r.get("hunt_priority") or 0), r["ticker"]))
    out = {str(k): [] for k in range(1, shards + 1)}
    for i, r in enumerate(order):
        out[str(i % shards + 1)].append(r["ticker"])
    return out


def build_plan(repo, rev, rr, C, me):
    """The day's names, from stage E-P's own run on the source branch at `rev`. Its sweep
    and stage E's degrade order, cut where E-P cuts; E-P's hunts only once its step 5 has
    written edge-scores.json, because a hunts/ directory read mid-wave is a partial list."""
    ep = f"{rr}/{C['names_from']}"
    sweep = loads(show(repo, rev, f"{ep}/sweep.json")) or {}
    rows = {r["ticker"]: r for r in sweep.get("names") or []}
    urow = {n["ticker"]: n for n in (loads(show(repo, rev, f"{ep}/universe.json")) or {}).get("names") or []}
    cap = min(int(C["shards"]) * int(C["hunted_names"]), int(C.get("ep_hunted_names") or 10 ** 6))
    hunted = []
    if show(repo, rev, f"{ep}/edge-scores.json") is not None:
        hunted = sorted({n[:-5].split("-")[0] for n in ls(repo, rev, f"{ep}/hunts") if n.endswith(".json")})
    if hunted:
        basis = f"{C['names_from']}/hunts: the names stage E-P hunted"
        tickers = sorted(hunted, key=lambda t: -(rows.get(t, {}).get("hunt_priority") or 0))
    else:
        basis = (f"{C['names_from']}/sweep.json: confirmed names by hunt_priority, then the rest by "
                 f"hunt_priority, cut at {cap} as budget.edge_degrade_order sheds")
        tickers = [r["ticker"] for r in sorted(rows.values(), key=lambda r: (not r.get("event_confirmed"),
                                                                              -(r.get("hunt_priority") or 0)))]
    names = []
    for t in tickers:
        b = loads(show(repo, rev, f"{ep}/baselines/{t}.json"))
        if b is None:
            continue                   # nothing sealed for it: E-P could not have hunted it either
        r, u = rows.get(t, {}), urow.get(t, {})
        names.append({"ticker": t, "company": u.get("company"),
                      "session": b.get("session") or u.get("session"),
                      "event_date": b.get("event_date") or u.get("event_date"),
                      "hunt_priority": r.get("hunt_priority"), "event_confirmed": r.get("event_confirmed")})
    shed = [n["ticker"] for n in names[cap:]]
    names = names[:cap]
    asg = assign(names, int(C["shards"]))
    for n in names:
        n["shard"] = next(int(k) for k, v in asg.items() if n["ticker"] in v)
    return {"date": rr.rsplit("/", 1)[-1], "stage": "E-PS", "built_utc": now_utc().isoformat(timespec="seconds"),
            "built_by": me, "source": {"branch": C["source_branch"], "commit": rev, "run": ep},
            "names_basis": basis, "shards": int(C["shards"]), "names_per_shard": int(C["hunted_names"]),
            "cap": cap, "names": names, "assignment": asg, "shed_over_cap": shed,
            "note": ("Stage E-P's names, split round-robin over four sessions of at most five and run while "
                     "E-P runs them. Each shard copies E-P's sweep rows and sealed baselines, hunts with its "
                     "own unpriced-searchers and judges with its own four blind judges, scored --dry-run "
                     "against E-P's panel history. Research only, no orders.")}


def ready(repo, C, rr, deadline, now):
    """Whether to start: a plan already exists, or stage E-P's sweep is on the source
    branch (so the shards search while E-P's searchers do), or not yet, or never."""
    if show(repo, fetch(repo, C["data_branch"]), f"{rr}/{PREFIX}/plan.json") is not None:
        return "plan exists", None
    rev = fetch(repo, C["source_branch"])
    if show(repo, rev, f"{rr}/{C['names_from']}/{C['start_when_file']}") is not None:
        return f"stage E-P's {C['start_when_file']} is on {C['source_branch']}", rev
    return ("stop" if now >= deadline else None), rev


def claim(repo, C, me, shard=None, force=False, wait_min=9.0, now=None, sleep=60):
    d = (now or now_utc()).astimezone(ET).date()
    rr = run_rel(d)
    hh, mm = (int(x) for x in C["start_deadline_et"].split(":"))
    deadline = datetime.combine(d, dtime(hh, mm), ET)
    t_end = time.monotonic() + wait_min * 60
    while True:
        why, rev = ready(repo, C, rr, deadline, now or now_utc())
        if why == "stop":
            return 2, {"ready": False, "stop": True, "reason": f"{C['start_deadline_et']} ET passed and no "
                       f"{C['names_from']}/{C['start_when_file']} on {C['source_branch']} for {d}: nothing to split"}
        if why:
            break
        if time.monotonic() >= t_end:
            return 3, {"ready": False, "retry": True, "reason": f"stage E-P's {C['start_when_file']} is not on "
                       f"{C['source_branch']} yet and it is before {C['start_deadline_et']} ET: run claim again"}
        time.sleep(sleep)
    br, n = C["data_branch"], int(C["shards"])
    plan_p = f"{rr}/{PREFIX}/plan.json"
    built = {}

    def decide(tip):
        plan = loads(show(repo, tip, plan_p))
        changes = {}
        if plan is None:
            if rev is None:
                return None
            if "plan" not in built:
                built["plan"] = build_plan(repo, rev, rr, C, me)
            plan = built["plan"]
            changes[plan_p] = dumps(plan)
        claims = {k: loads(show(repo, tip, f"{rr}/{PREFIX}/claims/shard-{k}.json")) for k in range(1, n + 1)}
        mine = [k for k, c in claims.items() if c and c.get("session") == me and c.get("status") != "done"]
        if mine and not shard:
            return changes, (mine[0], plan, True)
        if shard:
            c = claims.get(shard)
            if c and c.get("session") != me and not force:
                return None
            k = shard
        else:
            free = [k for k, c in claims.items() if c is None]
            if not free:
                return None
            k = free[0]
        changes[f"{rr}/{PREFIX}/claims/shard-{k}.json"] = dumps(
            {"shard": k, "of": n, "session": me, "status": "claimed",
             "claimed_utc": now_utc().isoformat(timespec="seconds"), "names": plan["assignment"][str(k)],
             "took_over": claims.get(k) if force else None})
        return changes, (k, plan, False)

    got = cas(repo, br, decide, f"split panel: claim for {d}")
    if got is None:
        tip = fetch(repo, br)
        taken = {k: (loads(show(repo, tip, f"{rr}/{PREFIX}/claims/shard-{k}.json")) or {}).get("session")
                 for k in range(1, n + 1)}
        return 4, {"ready": True, "claimed": False, "reason": (f"shard {shard} is held by another session (pass --force to take it over)"
                                                               if shard else "every shard is taken"), "claims": taken}
    k, plan, resumed = got
    snap = seed(repo, rr, plan, k)
    names = [x for x in plan["names"] if x["ticker"] in plan["assignment"][str(k)]]
    return 0, {"ready": True, "claimed": True, "shard": k, "of": n, "resumed": resumed, "session": me,
               "snap": str(snap), "run": str(Path(repo) / rr), "names": names,
               "names_basis": plan["names_basis"], "source_commit": plan["source"]["commit"],
               "plan_built_by_this_session": plan.get("built_by") == me, "start_reason": why}


def seed(repo, rr, plan, k):
    """Write the shard's universe, sweep, sweep rows and baselines from stage E-P's run at
    the plan's source commit. Once only: a resumed shard keeps what it already has."""
    snap = Path(repo) / rr / f"{PREFIX}-{k}"
    if (snap / "split.json").exists():
        return snap
    rev, ep = plan["source"]["commit"], plan["source"]["run"]
    if git(repo, "cat-file", "-e", rev, ok=True).returncode:
        # another session built the plan; its commit may be behind the branch tip by now
        git(repo, "fetch", "-q", "--depth", "1", "origin", rev, ok=True)
    if git(repo, "cat-file", "-e", rev, ok=True).returncode:
        rev = fetch(repo, plan["source"]["branch"])
    mine = plan["assignment"][str(k)]
    u = loads(show(repo, rev, f"{ep}/universe.json")) or {}
    u = dict(u, names=[x for x in u.get("names") or [] if x["ticker"] in mine], count=len(mine))
    s = loads(show(repo, rev, f"{ep}/sweep.json")) or {}
    rows = [r for r in s.get("names") or [] if r.get("ticker") in mine]
    s = dict(s, names=rows)
    (snap / "baselines").mkdir(parents=True, exist_ok=True)
    (snap / "sweep-rows").mkdir(exist_ok=True)
    (snap / "universe.json").write_text(dumps(u))
    (snap / "sweep.json").write_text(dumps(s))
    for r in rows:
        (snap / "sweep-rows" / f"{r['ticker']}.json").write_text(dumps(r))
    for t in mine:
        b = show(repo, rev, f"{ep}/baselines/{t}.json")
        if b is not None:
            (snap / "baselines" / f"{t}.json").write_bytes(b)
    (snap / "split.json").write_text(dumps({
        "stage": "E-PS", "shard": k, "of": plan["shards"], "names": mine,
        "seeded_utc": now_utc().isoformat(timespec="seconds"),
        "copied_from": {"branch": plan["source"]["branch"], "commit": rev, "run": ep,
                        "files": ["universe.json (filtered)", "sweep.json (filtered)", "baselines/<T>.json"]},
        "note": "Baselines and sweep rows are stage E-P's own, so the searcher's inputs are E-P's."}))
    return snap


# ---------------------------------------------------------------- talking and publishing

def log(repo, C, heading, lines, shard=None, d=None):
    """Append one section to the day's edge-split/_run-log.md on the data branch. Its own
    file, never the day's _run-log.md: that one is main's, and E-P appends to it."""
    import run_log
    d = d or now_utc().astimezone(ET).date()
    p = f"{run_rel(d)}/{PREFIX}/_run-log.md"
    head = f"Split panel {shard}/{C['shards']} — {heading}" if shard else f"Split panel — {heading}"

    def decide(tip):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "_run-log.md"
            cur = show(repo, tip, p)
            if cur is not None:
                f.write_bytes(cur)
            run_log.append_section(str(f), d.isoformat(), head, lines)
            return {p: f.read_bytes()}, p
    return cas(repo, C["data_branch"], decide, f"split panel: log{f' shard {shard}' if shard else ''} for {d}")


def publish(repo, C, shard, msg, d=None):
    """Mirror the shard's directory onto the data branch: every file in it written, every
    path the branch holds under it that is gone here (the release guard moves hunts)
    removed. The only way a shard's output leaves the container."""
    d = d or now_utc().astimezone(ET).date()
    rel = f"{run_rel(d)}/{PREFIX}-{shard}"
    snap = Path(repo) / rel
    local = {f"{rel}/{p.relative_to(snap).as_posix()}": p for p in sorted(snap.rglob("*")) if p.is_file()} if snap.exists() else {}

    def decide(tip):
        changes = {k: p.read_bytes() for k, p in local.items()}
        changes.update({p: None for p in ls(repo, tip, rel, recursive=True) if p not in local})
        return changes, {"published": len(local), "branch": C["data_branch"], "dir": rel}
    return cas(repo, C["data_branch"], decide, msg)


def stamp(repo, C, shard, model=None, d=None):
    """provenance.py stamp for a market main's provenance.py does not know: US-PS is
    registered in memory, its stage version computed by provenance's own rule, and
    nothing on disk but the shard's provenance.json changes."""
    import provenance as P
    market = C.get("provenance_market", "US-PS")
    P.MARKETS.setdefault(market, {"dir": PREFIX, "hunters": ["unpriced-searcher"],
                                  "since_utc": "2026-10-22T00:00:00+00:00",
                                  "lessons": "researcher_us/LESSONS.md",
                                  "skill": ".claude/skills/earnings-edge-panel-split/SKILL.md"})
    P.STAGE_SHORT.setdefault(market, "us-panel-split")
    reg = P.load_registry()
    reg["stages"] = P.stage_versions(reg)
    d = d or now_utc().astimezone(ET).date()
    snap = Path(repo) / run_rel(d) / f"{PREFIX}-{shard}"
    load = P.load_registry
    P.load_registry = lambda: reg
    try:
        doc = P.stamp(snap, market, orchestrator_model=model, force=True)
    finally:
        P.load_registry = load
    doc["budget"] = {"hunted_names_cap": int(C["hunted_names"]), "plan_cap": int(C["shards"]) * int(C["hunted_names"])}
    doc["registered_by"] = "researcher_us/scripts/panel_split.py stamp (main's provenance.py has no US-PS)"
    (snap / "provenance.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return doc


def done(repo, C, shard, d=None):
    d = d or now_utc().astimezone(ET).date()
    rr = run_rel(d)
    snap = Path(repo) / rr / f"{PREFIX}-{shard}"
    sp = loads((snap / "edge-scores-panel.json").read_bytes()) if (snap / "edge-scores-panel.json").exists() else None
    me = session_id(repo)
    cp = f"{rr}/{PREFIX}/claims/shard-{shard}.json"

    def decide(tip):
        c = loads(show(repo, tip, cp)) or {"shard": shard, "session": me}
        c.update(status="done", finished_utc=now_utc().isoformat(timespec="seconds"),
                 panel_scored=sp is not None,
                 members_present=(sp or {}).get("members_present"),
                 selected=[r["ticker"] for r in (sp or {}).get("ranking") or [] if r.get("selected")])
        return {cp: dumps(c)}, c
    return cas(repo, C["data_branch"], decide, f"split panel: shard {shard} done for {d}")


# ---------------------------------------------------------------- the comparison

def _hunt_stats(h):
    if not h:
        return None, None
    src = h.get("sources_used")
    n = len(src) if isinstance(src, (list, dict)) else src if isinstance(src, (int, float)) else None
    return len(h.get("findings") or []), n


def summarise(read_data, read_src, rr, C):
    """Every finished shard beside stage E-P on the same names. Pure function of what the
    two branches hold, so whichever session writes it last writes the complete one."""
    from edge_stats import spearman
    plan = loads(read_data(f"{rr}/{PREFIX}/plan.json"))
    if plan is None:
        return None
    ep = plan["source"]["run"]
    eps = loads(read_src(f"{ep}/edge-scores-panel.json")) or {}
    epk = {r["ticker"]: r for r in (loads(read_src(f"{ep}/edge-scores.json")) or {}).get("ranking") or []}
    epp = {r["ticker"]: r for r in eps.get("ranking") or []}
    shards, rows = {}, []
    for k in range(1, plan["shards"] + 1):
        c = loads(read_data(f"{rr}/{PREFIX}/claims/shard-{k}.json")) or {}
        sd = f"{rr}/{PREFIX}-{k}"
        sp = loads(read_data(f"{sd}/edge-scores-panel.json")) or {}
        sk = {r["ticker"]: r for r in (loads(read_data(f"{sd}/edge-scores.json")) or {}).get("ranking") or []}
        spp = {r["ticker"]: r for r in sp.get("ranking") or []}
        mins = None
        if c.get("claimed_utc") and c.get("finished_utc"):
            mins = round((datetime.fromisoformat(c["finished_utc"]) - datetime.fromisoformat(c["claimed_utc"])).total_seconds() / 60)
        shards[str(k)] = {"status": c.get("status", "unclaimed"), "session": c.get("session"),
                          "names": plan["assignment"][str(k)], "members_present": sp.get("members_present"),
                          "claimed_utc": c.get("claimed_utc"), "finished_utc": c.get("finished_utc"), "minutes": mins}
        for t in plan["assignment"][str(k)]:
            a, b = epp.get(t), spp.get(t)
            fe, se = _hunt_stats(loads(read_src(f"{ep}/hunts/{t}.json")))
            fs, ss = _hunt_stats(loads(read_data(f"{sd}/hunts/{t}.json")))
            rows.append({"ticker": t, "shard": k,
                         "session": next((n["session"] for n in plan["names"] if n["ticker"] == t), None),
                         "ep": ({"panel_pct": a["panel_pct"], "side": a["side"], "selected": a["selected"],
                                 "panel_pct_signed": a["panel_pct_signed"]} if a else None),
                         "split": ({"panel_pct": b["panel_pct"], "side": b["side"], "selected": b["selected"],
                                    "panel_pct_signed": b["panel_pct_signed"]} if b else None),
                         "impact_sum": {"ep": (epk.get(t) or {}).get("impact_sum"), "split": (sk.get(t) or {}).get("impact_sum")},
                         "findings": {"ep": fe, "split": fs}, "sources": {"ep": se, "split": ss}})
    both = [r for r in rows if r["ep"] and r["split"]]
    rho = spearman([r["ep"]["panel_pct_signed"] for r in both], [r["split"]["panel_pct_signed"] for r in both]) if len(both) >= 3 else None
    sel_ep = sorted(r["ticker"] for r in rows if r["ep"] and r["ep"]["selected"])
    sel_sp = sorted(r["ticker"] for r in rows if r["split"] and r["split"]["selected"])
    in_plan = {r["ticker"] for r in rows}

    def mean(key, arm):
        v = [r[key][arm] for r in rows if r[key][arm] is not None]
        return round(sum(v) / len(v), 2) if v else None
    return {"date": plan["date"], "stage": "E-PS", "generated_utc": now_utc().isoformat(timespec="seconds"),
            "names_basis": plan.get("names_basis"),
            "shards": shards, "shards_done": sum(s["status"] == "done" for s in shards.values()),
            "ep_members_present": eps.get("members_present"), "ep_panel_generated_utc": eps.get("generated_utc"),
            "names": len(rows), "names_scored_by_both": len(both),
            "ep_only": sorted(t for t in epp if t not in in_plan),
            "rho_panel_pct_signed": None if rho is None else round(rho, 3),
            "side_agree": sum(r["ep"]["side"] == r["split"]["side"] for r in both),
            "selected": {"ep": sel_ep, "split": sel_sp, "both": sorted(set(sel_ep) & set(sel_sp)),
                         "ep_selected_outside_plan": sorted(t for t, r in epp.items() if r.get("selected") and t not in in_plan)},
            "mean_findings": {"ep": mean("findings", "ep"), "split": mean("findings", "split")},
            "mean_sources": {"ep": mean("sources", "ep"), "split": mean("sources", "split")},
            "mean_abs_panel_pct": {arm: (round(sum(r[arm]["panel_pct"] for r in both) / len(both), 1) if both else None)
                                   for arm in ("ep", "split")},
            "note": ("Stage E-P hunted these names with one sweep and up to twenty searchers in one session; "
                     "the split ran them five to a session in the same half hour, on E-P's own sweep rows and "
                     "baselines and main's searcher, judges and panel history. One day is an anecdote; resolve "
                     "both arms with edge_resolve.py before reading anything into which set paid. Research only, "
                     "no orders."),
            "rows": rows}


def render_md(s):
    def cell(x):
        if not x:
            return "·"
        side = "L" if x["side"] > 0 else "S" if x["side"] < 0 else "-"
        return f"{x['panel_pct']:.0f}{side}{'*' if x['selected'] else ''}"

    def pair(d):
        return f"{'n/a' if d['ep'] is None else d['ep']} / {'n/a' if d['split'] is None else d['split']}"
    L = [f"# Split panel (stage E-PS), {s['date']}", "",
         "Stage E-P's own names, five to a session over four sessions, beside stage E-P's single session. "
         "A cell is `panel_pct` (0-100) with the side, L or S; `*` = selected (80 or more, all four judges); "
         "`·` = not scored in that arm. Findings and sources are counted in each arm's own hunt file.", "",
         f"Names from {s.get('names_basis') or 'n/a'}. Shards done: {s['shards_done']} of {len(s['shards'])}. "
         f"Names scored by both arms: {s['names_scored_by_both']} of {s['names']}. Spearman rho on signed panel_pct: "
         f"{'n/a' if s['rho_panel_pct_signed'] is None else s['rho_panel_pct_signed']}. Same side: "
         f"{s['side_agree']} of {s['names_scored_by_both']}.", "",
         f"Selected by E-P: {', '.join(s['selected']['ep']) or 'none'}. By the split: "
         f"{', '.join(s['selected']['split']) or 'none'}. Both: {', '.join(s['selected']['both']) or 'none'}."
         + (f" E-P also hunted {', '.join(s['ep_only'])}, outside the split's plan"
            + (f", and selected {', '.join(s['selected']['ep_selected_outside_plan'])} of them" if s['selected']['ep_selected_outside_plan'] else "")
            + "." if s.get("ep_only") else ""), "",
         f"Mean findings per name, E-P / split: {pair(s['mean_findings'])}. Mean sources: {pair(s['mean_sources'])}. "
         f"Mean panel_pct on names in both: {pair(s['mean_abs_panel_pct'])}.", "",
         "| ticker | shard | session | E-P | split | impact_sum E-P / split | findings E-P / split | sources E-P / split |",
         "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in sorted(s["rows"], key=lambda r: (r["shard"], r["ticker"])):
        L.append(f"| {r['ticker']} | {r['shard']} | {r['session'] or 'n/a'} | {cell(r['ep'])} | {cell(r['split'])} | "
                 f"{pair(r['impact_sum'])} | {pair(r['findings'])} | {pair(r['sources'])} |")
    L += ["", "| shard | status | names | judges | claimed (UTC) | minutes |", "| ---: | --- | --- | --- | --- | ---: |"]
    for k, v in s["shards"].items():
        L.append(f"| {k} | {v['status']} | {', '.join(v['names'])} | {', '.join(v['members_present'] or []) or 'n/a'} | "
                 f"{(v['claimed_utc'] or 'n/a')[11:16]} | {v['minutes'] if v['minutes'] is not None else 'n/a'} |")
    L += ["", f"E-P's panel was scored {s['ep_panel_generated_utc'] or 'n/a'} with "
          f"{', '.join(s['ep_members_present'] or []) or 'n/a'}.", "", s["note"], ""]
    return "\n".join(L)


def summary(repo, C, d=None):
    d = d or now_utc().astimezone(ET).date()
    rr = run_rel(d)
    src = fetch(repo, C["source_branch"])

    def decide(tip):
        s = summarise(lambda p: show(repo, tip, p), lambda p: show(repo, src, p), rr, C)
        if s is None:
            return None
        return {f"{rr}/{PREFIX}/summary.json": dumps(s), f"{rr}/{PREFIX}/summary.md": render_md(s)}, s
    return cas(repo, C["data_branch"], decide, f"split panel: summary for {d}")


def status(repo, C, d=None):
    d = d or now_utc().astimezone(ET).date()
    rr, tip = run_rel(d), fetch(repo, C["data_branch"])
    plan = loads(show(repo, tip, f"{rr}/{PREFIX}/plan.json"))
    return {"date": d.isoformat(), "plan": None if plan is None else plan["assignment"],
            "names_basis": None if plan is None else plan["names_basis"],
            "claims": {k: loads(show(repo, tip, f"{rr}/{PREFIX}/claims/shard-{k}.json"))
                       for k in range(1, int(C["shards"]) + 1)}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("claim")
    c.add_argument("--shard", type=int)
    c.add_argument("--force", action="store_true", help="take over a shard another session holds")
    c.add_argument("--wait-min", type=float, default=9.0, help="how long one call waits for stage E-P (minutes)")
    c.add_argument("--session", help="name this session (default: a stable id kept in .git)")
    lg = sub.add_parser("log")
    lg.add_argument("--shard", type=int)
    lg.add_argument("--heading", required=True)
    lg.add_argument("--line", action="append", default=[])
    st = sub.add_parser("stamp")
    st.add_argument("--shard", type=int, required=True)
    st.add_argument("--orchestrator-model")
    pb = sub.add_parser("publish")
    pb.add_argument("--shard", type=int, required=True)
    pb.add_argument("message")
    sub.add_parser("done").add_argument("--shard", type=int, required=True)
    sub.add_parser("summary")
    sub.add_parser("status")
    a = ap.parse_args()
    C = cfg()
    if a.cmd == "claim":
        code, out = claim(REPO, C, session_id(REPO, a.session), a.shard, a.force, a.wait_min)
        print(json.dumps(out, indent=1, ensure_ascii=False))
        sys.exit(code)
    elif a.cmd == "log":
        print(log(REPO, C, a.heading, a.line, a.shard))
    elif a.cmd == "stamp":
        doc = stamp(REPO, C, a.shard, a.orchestrator_model)
        print(json.dumps({"market": doc["market"], "stage_version": doc.get("stage_version"),
                          "hunters": {k: v.get("prompt_version") for k, v in doc["hunters"].items()}}, indent=1))
    elif a.cmd == "publish":
        print(json.dumps(publish(REPO, C, a.shard, a.message), indent=1))
    elif a.cmd == "done":
        print(json.dumps(done(REPO, C, a.shard), indent=1, ensure_ascii=False))
    elif a.cmd == "summary":
        s = summary(REPO, C)
        print("no plan for today" if s is None else render_md(s))
    else:
        print(json.dumps(status(REPO, C), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
