#!/usr/bin/env python3
"""Self-test for stage E-PS (panel_split.py), against throwaway git repositories only.

Stage E-PS lives on its own branch and a fired session runs on main with the stage's
files laid over it, so its checks cannot sit in scripts/smoke_test.py (main's file) and
live here instead. No network and no model calls. Run it after any change to
panel_split.py, its skill or config/edge-panel-split.yaml:

  python3 researcher_us/scripts/panel_split_check.py
"""
import json, os, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import panel_split as ps  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + ("" if ok else f"\n        {detail}"))
    if not ok:
        FAILS.append(name)


def g(c, *a):
    return subprocess.run(["git", "-C", c, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                          check=True, capture_output=True)


def main():
    C0 = ps.cfg()
    skill = (REPO / ".claude" / "skills" / "earnings-edge-panel-split" / "SKILL.md").read_text(encoding="utf-8")
    check("stage E-PS places no orders, never writes E-P's history and never publishes to main",
          C0.get("places_orders") is False and C0.get("writes_panel_history") is False
          and C0.get("data_branch") not in (None, "", "main")
          and "no `alpaca_trade.py` call of any kind" in skill and "panel_split.py stamp" in skill
          and "--dry-run --stage E-PS" in skill and "intraday.py guard" in skill
          and "never the two scripts directly" in skill)
    check("every overlay file exists, so a session on main can lay them over its checkout",
          all((REPO / f).exists() for f in C0.get("overlay") or []) and len(C0.get("overlay") or []) == 3,
          str(C0.get("overlay")))

    nm = ([{"ticker": f"A{i}", "session": "amc", "event_date": "2026-10-22", "hunt_priority": 90 - i} for i in range(9)]
          + [{"ticker": f"B{i}", "session": "bmo", "event_date": "2026-10-23", "hunt_priority": 99 - i} for i in range(11)])
    asg = ps.assign(nm, 4)
    check("twenty names go into four shards of five, tonight's prints first in each",
          sorted(len(v) for v in asg.values()) == [5, 5, 5, 5] and all(v[0].startswith("A") for v in asg.values())
          and sorted(sum(asg.values(), [])) == sorted(n["ticker"] for n in nm), str(asg))

    with tempfile.TemporaryDirectory() as td:
        bare, src = os.path.join(td, "o.git"), os.path.join(td, "src")
        subprocess.run(["git", "init", "-q", "--bare", bare], check=True)
        subprocess.run(["git", "clone", "-q", bare, src], check=True, capture_output=True)
        rr = "research/2026/10/2026-10-22"
        ep = os.path.join(src, rr, "edge-panel")
        for t in ("X1", "X2", "X3", "X4"):
            for d_ in ("baselines", "hunts"):
                os.makedirs(os.path.join(ep, d_), exist_ok=True)
            json.dump({"ticker": t, "session": "amc", "event_date": "2026-10-22"}, open(os.path.join(ep, "baselines", t + ".json"), "w"))
        # E-P is mid-wave: two hunts written, no edge-scores.json yet
        for t in ("X1", "X2"):
            json.dump({"ticker": t, "findings": [{}], "sources_used": 3}, open(os.path.join(ep, "hunts", t + ".json"), "w"))
        json.dump({"names": [{"ticker": t, "event_confirmed": t != "X4", "hunt_priority": p}
                             for t, p in (("X1", 90), ("X2", 80), ("X3", 70), ("X4", 95))]},
                  open(os.path.join(ep, "sweep.json"), "w"))
        json.dump({"names": [{"ticker": t, "company": t} for t in ("X1", "X2", "X3", "X4")]}, open(os.path.join(ep, "universe.json"), "w"))
        g(src, "add", "-A"); g(src, "commit", "-qm", "e-p"); g(src, "push", "-q", "origin", "HEAD:refs/heads/main")
        g(src, "push", "-q", "origin", "HEAD:refs/heads/test")
        cl = {}
        for who in ("a", "b", "c"):
            cl[who] = os.path.join(td, who)
            subprocess.run(["git", "clone", "-q", "--depth", "1", "-b", "main", "file://" + bare, cl[who]],
                           check=True, capture_output=True)
        C = dict(C0, shards=2, hunted_names=5, data_branch="test", source_branch="main", ep_hunted_names=3)
        at = datetime(2026, 10, 22, 17, 25, tzinfo=timezone.utc)
        real_build = ps.build_plan

        def racing_build(*a, **k):                     # b decides on a stale tip: a pushes first
            ps.build_plan = real_build
            cl["a_got"] = ps.claim(cl["a"], C, "sess-a", now=at, wait_min=0)
            return real_build(*a, **k)
        ps.build_plan = racing_build
        rb = ps.claim(cl["b"], C, "sess-b", now=at, wait_min=0)
        ps.build_plan = real_build
        ra = cl["a_got"]
        tip = ps.fetch(cl["c"], "test")
        plan = json.loads(ps.show(cl["c"], tip, f"{rr}/edge-split/plan.json"))
        check("two sessions racing for a shard get different ones, and the first plan pushed is the plan",
              ra[0] == 0 and rb[0] == 0 and ra[1]["shard"] == 1 and rb[1]["shard"] == 2
              and plan["built_by"] == "sess-a" and not rb[1]["plan_built_by_this_session"]
              and os.path.exists(os.path.join(rb[1]["snap"], "baselines", plan["assignment"]["2"][0] + ".json")),
              f"{ra} {rb}")
        check("mid-wave, the plan comes from E-P's sweep (confirmed first, E-P's cap), not its partial hunts",
              "sweep.json" in plan["names_basis"] and [n["ticker"] for n in plan["names"]] == ["X1", "X2", "X3"]
              and plan["shed_over_cap"] == ["X4"], json.dumps(plan["names"]))
        again = ps.claim(cl["a"], C, "sess-a", now=at, wait_min=0)
        third = ps.claim(cl["c"], C, "sess-c", now=at, wait_min=0)
        check("a session that re-runs claim resumes its own shard; a third finds none free",
              again[0] == 0 and again[1]["shard"] == 1 and again[1]["resumed"] and third[0] == 4, f"{again} {third}")
        none_yet = ps.claim(cl["c"], dict(C, names_from="edge-nothing"), "sess-x",
                            now=datetime(2026, 10, 23, 17, 25, tzinfo=timezone.utc), wait_min=0)
        too_late = ps.claim(cl["c"], dict(C, names_from="edge-nothing"), "sess-x",
                            now=datetime(2026, 10, 23, 19, 0, tzinfo=timezone.utc), wait_min=0)
        check("before E-P's sweep it says wait, after the deadline without one it says stop",
              none_yet[0] == 3 and too_late[0] == 2, f"{none_yet} {too_late}")

        ps.log(cl["a"], C, "STARTED", ["a"], shard=1, d=at.date())
        ps.log(cl["b"], C, "STARTED", ["b"], shard=2, d=at.date())
        tip = ps.fetch(cl["c"], "test")
        rl = ps.show(cl["c"], tip, f"{rr}/edge-split/_run-log.md").decode()
        check("two sessions append to the stage's own run log, never the day's",
              "Split panel 1/2 — STARTED" in rl and "Split panel 2/2 — STARTED" in rl
              and ps.show(cl["c"], tip, f"{rr}/_run-log.md") is None, rl)

        s1 = Path(ra[1]["snap"])
        (s1 / "hunts").mkdir(exist_ok=True)
        for t in plan["assignment"]["1"]:
            json.dump({"ticker": t, "findings": [{}, {}], "sources_used": 5}, open(s1 / "hunts" / f"{t}.json", "w"))
        ps.publish(cl["a"], C, 1, "shard 1 hunts", d=at.date())
        moved = plan["assignment"]["1"][0]
        (s1 / "_after_release" / "hunts").mkdir(parents=True)
        os.replace(s1 / "hunts" / f"{moved}.json", s1 / "_after_release" / "hunts" / f"{moved}.json")
        ps.publish(cl["a"], C, 1, "shard 1 guard", d=at.date())
        t2 = ps.fetch(cl["c"], "test")
        ps.publish(cl["a"], C, 1, "shard 1 again, nothing changed", d=at.date())
        tip = ps.fetch(cl["c"], "test")
        files = ps.ls(cl["c"], tip, f"{rr}/edge-split-1", recursive=True)
        check("publish mirrors the shard: a guarded hunt moves, an unchanged tree pushes nothing",
              f"{rr}/edge-split-1/hunts/{moved}.json" not in files
              and f"{rr}/edge-split-1/_after_release/hunts/{moved}.json" in files
              and f"{rr}/edge-split-1/baselines/{moved}.json" in files and tip == t2
              and ps.fetch(cl["c"], "main") == subprocess.run(["git", "-C", src, "rev-parse", "HEAD"],
                                                               capture_output=True, text=True).stdout.strip(),
              f"{files} {t2} {tip}")

        doc = ps.stamp(cl["a"], C, 1, "claude-opus-5-5", d=at.date())
        check("stamp registers US-PS at run time with its own stage version",
              doc["market"] == "US-PS" and (doc.get("stage_version") or {}).get("id", "").startswith("us-panel-split.v")
              and (s1 / "provenance.json").exists(), json.dumps(doc.get("stage_version")))

        for k, snap in ((1, s1), (2, Path(rb[1]["snap"]))):
            mine = plan["assignment"][str(k)]
            json.dump({"members_present": ["opus5", "opus55", "sonnet55", "fable51"], "ranking": [
                {"ticker": t, "panel_pct": 85.0, "side": 1, "selected": True, "panel_pct_signed": 85.0} for t in mine]},
                open(snap / "edge-scores-panel.json", "w"))
            ps.publish(cl["a" if k == 1 else "b"], C, k, f"shard {k} panel", d=at.date())
            ps.done(cl["a" if k == 1 else "b"], C, k, d=at.date())
        s = ps.summary(cl["b"], C, d=at.date())
        md = ps.show(cl["c"], ps.fetch(cl["c"], "test"), f"{rr}/edge-split/summary.md").decode()
        check("the summary counts both shards, reads sources as a number, and lists E-P's names outside the plan",
              s["shards_done"] == 2 and s["names"] == 3 and s["mean_sources"]["split"] == 5.0
              and "Split panel (stage E-PS)" in md, json.dumps({k: s[k] for k in ("shards_done", "names", "mean_sources")}))

    print("\nAll split-panel checks passed." if not FAILS else f"\n{len(FAILS)} check(s) FAILED.")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
