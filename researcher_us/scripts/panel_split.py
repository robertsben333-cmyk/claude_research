#!/usr/bin/env python3
"""Stage E-PS: stage E-P's names split over four sessions of at most five, one day's test.

Built 2026-10-22 on the operator's instruction: "ik heb het gevoel dat bij hoog aantal
tickers het systeem het niet goed doet. dus ik wil even 4 test routines aanmaken, die
ieder max 5 stocks beoordelen, en op de een of andere manier communiceren onderling wie
welk doet". The 2026-10-21 run log is the reason it is worth a day: stage E-P on 30 names
left 89 of 118 universe names unchecked by its one sweep, its searchers reported the
session's shared WebSearch budget running out, and its eight judge instances hit a 429
and finished after the close, so no book was bought.

Four fresh sessions take stage E-P's OWN names that day (its hunts, or its sweep if the
hunts are not there yet), with E-P's sweep rows and sealed baselines copied in, so the
only thing that differs from E-P is how many names one session carries (and that it runs
about an hour later). Each session hunts its names with `unpriced-searcher` and has its
own four blind judges, scored --dry-run against stage E-P's history. Places no orders.

  research/<Y>/<M>/<DATE>/edge-split/        plan.json, claims/shard-<k>.json, summary.{json,md}
  research/<Y>/<M>/<DATE>/edge-split-<k>/    one shard, stage E-P's layout

HOW THE SESSIONS TALK: through git, on `edge_panel_split.data_branch` (never main). Every
write to edge-split/ and to the day's _run-log.md is a compare-and-swap: a commit built on
top of the branch's current tip that adds or replaces exactly those files, pushed; when
the push is rejected because another session pushed first, the session re-reads the tip
and decides again. Only one of two pushes on the same parent can land, so two sessions can
never hold one shard, and the first plan written is the plan. Those commits never need a
merge, so they cannot conflict with publish.sh's rebases of the shard directories.

  python3 researcher_us/scripts/panel_split.py claim  [--shard K --force] [--wait-min 9]
  python3 researcher_us/scripts/panel_split.py log    --shard K --heading H --line L [--line L]
  python3 researcher_us/scripts/panel_split.py publish "<commit message>"
  python3 researcher_us/scripts/panel_split.py done   --shard K
  python3 researcher_us/scripts/panel_split.py summary
  python3 researcher_us/scripts/panel_split.py status

`claim` exits 0 with the shard, 3 while stage E-P has not reached its buy and the start
deadline has not passed (run it again), 2 when the deadline passed with no E-P sweep on
the source branch (stop), 4 when every shard is taken.
"""
import argparse, json, os, random, socket, subprocess, sys, tempfile, time, uuid
from datetime import datetime, time as dtime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[2]
ET = ZoneInfo("America/New_York")
PREFIX = "edge-split"
SESSION_ORDER = {"bmo": 0, "amc": 1}
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))


def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml"))
    C = dict(c.get("edge_panel_split") or {})
    if C.get("data_branch") in (None, "", C.get("source_branch", "main")):
        sys.exit("edge_panel_split.data_branch must name a branch other than the source branch")
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


def fetch(repo, br, depth=None):
    """The branch's tip on origin, or None if it does not exist there."""
    a = ["fetch", "-q"] + (["--depth", str(depth)] if depth else []) + ["origin", f"+refs/heads/{br}:refs/remotes/origin/{br}"]
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


def ls(repo, rev, path):
    if not rev:
        return []
    r = git(repo, "ls-tree", "--name-only", f"{rev}:{path}", ok=True)
    return r.stdout.decode().split() if r.returncode == 0 else []


def ident(repo):
    env = dict(os.environ)
    name = git(repo, "config", "user.name", ok=True).stdout.decode().strip() or "Earnings Routine"
    mail = git(repo, "config", "user.email", ok=True).stdout.decode().strip() or "earnings-routine@users.noreply.github.com"
    env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=mail, GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=mail)
    return env


def cas(repo, br, decide, message, tries=12):
    """Compare-and-swap on the branch. `decide(read)` sees the tip through `read(path)`
    and returns (changes, value), changes a {path: text} to write on top of that tip, or
    None to write nothing. Rejected pushes re-read and decide again, so `decide` must
    depend on nothing but what it reads."""
    for n in range(tries):
        tip = fetch(repo, br)
        if tip is None:
            sys.exit(f"branch {br} does not exist on origin")
        res = decide(lambda p: show(repo, tip, p))
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
            for path, text in sorted(changes.items()):
                blob = git(repo, "hash-object", "-w", "--stdin", data=text.encode("utf-8")).strip()
                git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
            tree = git(repo, "write-tree", env=env).strip()
            commit = git(repo, "commit-tree", tree, "-p", tip, "-m", message, env=env).strip()
        finally:
            os.unlink(idx)
        if git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{br}", ok=True).returncode == 0:
            sync(repo, br)
            return value
        time.sleep(1 + random.random() * 2 * (n + 1))
    sys.exit(f"could not push to {br} after {tries} tries: another session keeps moving it")


def sync(repo, br):
    """Bring the working tree up to the tip when that is a fast-forward. Not needed for
    correctness (every read goes through the tip, never the working tree), so a refusal
    only warns: publish.sh reconciles the next time it runs."""
    fetch(repo, br)
    if git(repo, "merge", "--ff-only", "-q", f"refs/remotes/origin/{br}", ok=True).returncode:
        print(f"note: working tree not fast-forwarded to origin/{br}; publish.sh will reconcile", file=sys.stderr)


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
    """The day's names, from stage E-P's own run on the source branch at `rev`."""
    ep = f"{rr}/{C['names_from']}"
    sweep = loads(show(repo, rev, f"{ep}/sweep.json")) or {}
    rows = {r["ticker"]: r for r in sweep.get("names") or []}
    urow = {n["ticker"]: n for n in (loads(show(repo, rev, f"{ep}/universe.json")) or {}).get("names") or []}
    hunted = sorted({n[:-5].split("-")[0] for n in ls(repo, rev, f"{ep}/hunts") if n.endswith(".json")})
    cap = int(C["shards"]) * int(C["hunted_names"])
    if hunted:
        basis = f"{C['names_from']}/hunts: the names stage E-P hunted"
        tickers = sorted(hunted, key=lambda t: -(rows.get(t, {}).get("hunt_priority") or 0))
    else:
        basis = (f"{C['names_from']}/sweep.json (E-P's hunts not on {C['source_branch']} yet): confirmed names by "
                 "hunt_priority, then the rest by hunt_priority, as budget.edge_degrade_order sheds")
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
            "names": names, "assignment": asg, "shed_over_cap": shed,
            "note": ("Stage E-P's own names, split round-robin over four sessions of at most five. Each shard "
                     "copies E-P's sweep rows and sealed baselines, hunts with its own unpriced-searchers and "
                     "judges with its own four blind judges, scored --dry-run. Research only, no orders.")}


def ready(repo, C, rr, deadline, now):
    """Whether to start: a plan already exists, or stage E-P has reached its buy (so these
    sessions cannot push it into the usage limit before its book is placed), or the start
    deadline has passed and E-P's sweep exists."""
    br, src = C["data_branch"], C["source_branch"]
    if show(repo, fetch(repo, br), f"{rr}/{PREFIX}/plan.json") is not None:
        return "plan exists", None
    rev = fetch(repo, src, depth=1)
    ep = f"{rr}/{C['names_from']}"
    if show(repo, rev, f"{ep}/{C['start_when_file']}") is not None:
        return f"stage E-P wrote {C['start_when_file']}", rev
    if now >= deadline:
        if show(repo, rev, f"{ep}/sweep.json") is not None:
            return "start deadline passed; E-P's sweep exists", rev
        return "stop", rev
    return None, rev


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
                       f"{C['names_from']}/sweep.json on {C['source_branch']} for {d}: nothing to split"}
        if why:
            break
        if time.monotonic() >= t_end:
            return 3, {"ready": False, "retry": True, "reason": f"stage E-P has not written {C['start_when_file']} "
                       f"and it is before {C['start_deadline_et']} ET: run claim again"}
        time.sleep(sleep)
    br, n = C["data_branch"], int(C["shards"])
    plan_p = f"{rr}/{PREFIX}/plan.json"
    built = {}

    def decide(read):
        plan = loads(read(plan_p))
        changes = {}
        if plan is None:
            if rev is None:
                return None
            if "plan" not in built:
                built["plan"] = build_plan(repo, rev, rr, C, me)
            plan = built["plan"]
            changes[plan_p] = dumps(plan)
        claims = {k: loads(read(f"{rr}/{PREFIX}/claims/shard-{k}.json")) for k in range(1, n + 1)}
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
    snap = seed(repo, C, rr, plan, k)
    names = [x for x in plan["names"] if x["ticker"] in plan["assignment"][str(k)]]
    return 0, {"ready": True, "claimed": True, "shard": k, "of": n, "resumed": resumed, "session": me,
               "snap": str(snap), "run": str(Path(repo) / rr),
               "names": names, "names_basis": plan["names_basis"], "source_commit": plan["source"]["commit"],
               "plan_built_by_this_session": plan.get("built_by") == me, "start_reason": why}


def seed(repo, C, rr, plan, k):
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
        rev = fetch(repo, plan["source"]["branch"], depth=1)
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


# ---------------------------------------------------------------- talking

def log(repo, C, heading, lines, shard=None, d=None):
    """Append one section to the day's _run-log.md on the data branch, by compare-and-swap,
    so four sessions appending at once never meet in a rebase."""
    import run_log
    d = d or now_utc().astimezone(ET).date()
    p = f"{run_rel(d)}/_run-log.md"
    head = f"Split panel {shard}/{C['shards']} — {heading}" if shard else f"Split panel — {heading}"

    def decide(read):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "_run-log.md"
            cur = read(p)
            if cur is not None:
                f.write_bytes(cur)
            run_log.append_section(str(f), d.isoformat(), head, lines)
            return {p: f.read_text(encoding="utf-8")}, p
    return cas(repo, C["data_branch"], decide, f"split panel: log{f' shard {shard}' if shard else ''} for {d}")


def done(repo, C, shard, d=None):
    d = d or now_utc().astimezone(ET).date()
    rr = run_rel(d)
    snap = Path(repo) / rr / f"{PREFIX}-{shard}"
    sp = loads((snap / "edge-scores-panel.json").read_bytes()) if (snap / "edge-scores-panel.json").exists() else None
    me = session_id(repo)
    cp = f"{rr}/{PREFIX}/claims/shard-{shard}.json"

    def decide(read):
        c = loads(read(cp)) or {"shard": shard, "session": me}
        c.update(status="done", finished_utc=now_utc().isoformat(timespec="seconds"),
                 panel_scored=sp is not None,
                 members_present=(sp or {}).get("members_present"),
                 selected=[r["ticker"] for r in (sp or {}).get("ranking") or [] if r.get("selected")])
        return {cp: dumps(c)}, c
    return cas(repo, C["data_branch"], decide, f"split panel: shard {shard} done for {d}")


def publish(repo, C, msg):
    subprocess.run([sys.executable, str(REPO / "scripts" / "update_index.py")], cwd=repo, capture_output=True)
    env = dict(os.environ, EARNINGS_DATA_BRANCH=C["data_branch"])
    return subprocess.run([str(REPO / "scripts" / "publish.sh"), msg], cwd=repo, env=env).returncode


# ---------------------------------------------------------------- the comparison

def _hunt_stats(h):
    if not h:
        return None, None
    src = h.get("sources_used")
    return len(h.get("findings") or []), (len(src) if isinstance(src, list) else None)


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

    def mean(key, arm):
        v = [r[key][arm] for r in rows if r[key][arm] is not None]
        return round(sum(v) / len(v), 2) if v else None
    return {"date": plan["date"], "stage": "E-PS", "generated_utc": now_utc().isoformat(timespec="seconds"),
            "shards": shards, "shards_done": sum(s["status"] == "done" for s in shards.values()),
            "ep_members_present": eps.get("members_present"), "ep_panel_generated_utc": eps.get("generated_utc"),
            "names": len(rows), "names_scored_by_both": len(both),
            "rho_panel_pct_signed": None if rho is None else round(rho, 3),
            "side_agree": sum(r["ep"]["side"] == r["split"]["side"] for r in both),
            "selected": {"ep": sel_ep, "split": sel_sp, "both": sorted(set(sel_ep) & set(sel_sp))},
            "mean_findings": {"ep": mean("findings", "ep"), "split": mean("findings", "split")},
            "mean_sources": {"ep": mean("sources", "ep"), "split": mean("sources", "split")},
            "mean_abs_panel_pct": {arm: (round(sum(r[arm]["panel_pct"] for r in both) / len(both), 1) if both else None)
                                   for arm in ("ep", "split")},
            "note": ("Stage E-P hunted these names with one sweep and up to twenty searchers in one session; "
                     "the split ran them five to a session about an hour later, on E-P's own sweep rows and "
                     "baselines. One day is an anecdote; resolve both arms with edge_resolve.py before reading "
                     "anything into which set paid. Research only, no orders."),
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
         f"Shards done: {s['shards_done']} of {len(s['shards'])}. Names scored by both arms: "
         f"{s['names_scored_by_both']} of {s['names']}. Spearman rho on signed panel_pct: "
         f"{'n/a' if s['rho_panel_pct_signed'] is None else s['rho_panel_pct_signed']}. Same side: "
         f"{s['side_agree']} of {s['names_scored_by_both']}.", "",
         f"Selected by E-P: {', '.join(s['selected']['ep']) or 'none'}. By the split: "
         f"{', '.join(s['selected']['split']) or 'none'}. Both: {', '.join(s['selected']['both']) or 'none'}.", "",
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
    src = fetch(repo, C["source_branch"], depth=1)

    def decide(read):
        s = summarise(read, lambda p: show(repo, src, p), rr, C)
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
    sub.add_parser("publish").add_argument("message")
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
    elif a.cmd == "publish":
        sys.exit(publish(REPO, C, a.message))
    elif a.cmd == "done":
        print(json.dumps(done(REPO, C, a.shard), indent=1, ensure_ascii=False))
    elif a.cmd == "summary":
        s = summary(REPO, C)
        print("no plan for today" if s is None else render_md(s))
    else:
        print(json.dumps(status(REPO, C), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
