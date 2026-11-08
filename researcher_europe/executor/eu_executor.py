#!/usr/bin/env python3
"""Stage EU's executor: runs on the operator's own always-on server, next to IB Gateway,
and trades the book the cloud Routine publishes. Nothing connects in to the server;
it only fetches from GitHub and talks to the gateway on localhost.

Two systemd timers call it on weekdays (install.sh sets them up):

    15:35 Amsterdam  flatten  git pull, `ibkr_trade.py check`, then
                              `ibkr_trade.py flatten --run <yesterday's run> --submit`
    16:00 Amsterdam  open     git pull every two minutes until the cloud Routine's step
                              6b has published `<RUN>/ibkr-handoff.json` for today,
                              then `ibkr_trade.py open --run <RUN> --submit`, once;
                              gives up at 17:30 Amsterdam

Every rule, limit and switch is `ibkr_trade.py`'s, unchanged: nothing is sent unless
`execution_eu.enabled` is true on main, IBKR_ENVIRONMENT here equals
`execution_eu.environment`, IBKR_ACCOUNT_ID names the only account the login sees, and
its prefix matches (DU paper, U live). So turning trading off is still one line on main.

Logs go to ~/eu-executor/logs/<date>.log. With EXECUTOR_PUSH_LOG=1 (and a GitHub token
allowed to write this repository) each day's log and `ibkr-orders.json` are pushed to
the branch `eu-ibkr-log`, never to main, so a session can read what happened.

    python3 eu_executor.py flatten | open | check | status [--repo DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

AMS = ZoneInfo("Europe/Amsterdam")
HOME = Path(os.environ.get("EXECUTOR_HOME") or Path.home() / "eu-executor")
LOG_BRANCH = "eu-ibkr-log"
OPEN_GIVE_UP_LOCAL = "17:30"
POLL_SECONDS = 120


def now_ams():
    return datetime.now(timezone.utc).astimezone(AMS)


class Log:
    def __init__(self):
        (HOME / "logs").mkdir(parents=True, exist_ok=True)
        self.path = HOME / "logs" / f"{now_ams().date().isoformat()}.log"

    def __call__(self, msg):
        line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}"
        print(line, flush=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def pull(repo, log):
    """Make the checkout equal to origin/main. Untracked files (the order records this
    server writes) are left alone."""
    try:
        git(repo, "fetch", "-q", "origin", "main")
        git(repo, "checkout", "-q", "-B", "main", "origin/main")
        return git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
    except subprocess.CalledProcessError as e:
        log(f"git pull failed: {e.stderr.strip()}")
        return None


def europe_runs(repo):
    return sorted((repo / "research").glob("*/*/*/europe"), key=lambda p: p.parent.name)


def run_to_flatten(repo, today):
    """The run whose book is being sold: the newest Europe run for a session on or
    before today (its names reported this morning)."""
    runs = [r for r in europe_runs(repo) if r.parent.name <= today]
    return runs[-1] if runs else None


def todays_handoff(repo, today_utc):
    for r in reversed(europe_runs(repo)):
        h = r / "ibkr-handoff.json"
        if h.exists():
            try:
                if json.loads(h.read_text(encoding="utf-8")).get("date_utc") == today_utc:
                    return r
            except Exception:
                continue
    return None


def trade(repo, log, *args):
    cmd = [sys.executable, str(repo / "researcher_europe" / "scripts" / "ibkr_trade.py"), *args]
    log("$ " + " ".join(cmd[1:]))
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=repo)
    for line in (p.stdout + p.stderr).splitlines():
        log("  " + line)
    log(f"  exit {p.returncode}")
    return p.returncode


def state_path():
    return HOME / "state.json"


def load_state():
    try:
        return json.loads(state_path().read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(s):
    state_path().write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")


def push_log(repo, log, runs):
    """Copy today's log and the order records to the eu-ibkr-log branch and push it."""
    if os.environ.get("EXECUTOR_PUSH_LOG") != "1":
        return
    work = HOME / "log-branch"
    try:
        if not (work / ".git").exists():
            url = git(repo, "remote", "get-url", "origin").stdout.strip()
            subprocess.run(["git", "clone", "-q", url, str(work)], check=True, capture_output=True, text=True)
            if git(work, "ls-remote", "--heads", "origin", LOG_BRANCH).stdout.strip():
                git(work, "checkout", "-q", LOG_BRANCH)
            else:
                git(work, "checkout", "-q", "--orphan", LOG_BRANCH)
                git(work, "rm", "-rq", "--cached", ".", check=False)
                for p in work.iterdir():
                    if p.name != ".git":
                        shutil.rmtree(p) if p.is_dir() else p.unlink()
        else:
            git(work, "pull", "-q", "--ff-only", "origin", LOG_BRANCH, check=False)
        day = now_ams().date().isoformat()
        (work / "logs").mkdir(exist_ok=True)
        shutil.copy(log.path, work / "logs" / f"{day}.log")
        for r in runs:
            if r and (r / "ibkr-orders.json").exists():
                dest = work / "orders" / f"{r.parent.name}-ibkr-orders.json"
                dest.parent.mkdir(exist_ok=True)
                shutil.copy(r / "ibkr-orders.json", dest)
        git(work, "add", "-A")
        if git(work, "diff", "--cached", "--quiet", check=False).returncode != 0:
            git(work, "-c", "user.name=eu-executor", "-c", "user.email=eu-executor@localhost",
                "commit", "-qm", f"eu-executor: {day} {datetime.now(timezone.utc).strftime('%H:%MZ')}")
            git(work, "push", "-q", "origin", f"HEAD:{LOG_BRANCH}")
            log(f"log pushed to {LOG_BRANCH}")
    except subprocess.CalledProcessError as e:
        log(f"log push failed: {(e.stderr or '').strip()}")


def cmd_check(repo, log):
    pull(repo, log)
    return trade(repo, log, "check")


def cmd_flatten(repo, log):
    head = pull(repo, log)
    log(f"flatten at {now_ams():%Y-%m-%d %H:%M} Amsterdam, main at {head}")
    trade(repo, log, "mode")
    rc = trade(repo, log, "check")
    today = now_ams().date().isoformat()
    run = run_to_flatten(repo, today)
    if rc != 0:
        log("check failed: not flattening (the gateway is not reachable or not logged in)")
        push_log(repo, log, [run])
        return rc
    if run is None:
        log("no Europe run on disk to record against; nothing to do")
        return 0
    rc = trade(repo, log, "flatten", "--run", str(run), "--submit")
    push_log(repo, log, [run])
    return rc


def cmd_open(repo, log, give_up_local=OPEN_GIVE_UP_LOCAL):
    today_utc = datetime.now(timezone.utc).date().isoformat()
    state = load_state()
    if state.get("opened_utc_date") == today_utc:
        log(f"open already ran today for {state.get('opened_run')}; not again")
        return 0
    hh, mm = (int(x) for x in give_up_local.split(":"))
    deadline = now_ams().replace(hour=hh, minute=mm, second=0, microsecond=0)
    log(f"waiting for today's handoff until {give_up_local} Amsterdam")
    while True:
        head = pull(repo, log)
        run = todays_handoff(repo, today_utc)
        if run is not None:
            log(f"handoff found in {run.relative_to(repo)} (main at {head})")
            rc = trade(repo, log, "open", "--run", str(run), "--submit")
            state.update({"opened_utc_date": today_utc, "opened_run": str(run.relative_to(repo)), "exit": rc})
            save_state(state)
            push_log(repo, log, [run])
            return rc
        if now_ams() >= deadline:
            log("no handoff today before the deadline: the Routine did not reach step 6b "
                "(or was late); nothing bought")
            push_log(repo, log, [])
            return 0
        time.sleep(POLL_SECONDS)


def cmd_status(repo, log):
    run = run_to_flatten(repo, now_ams().date().isoformat())
    return trade(repo, log, "status", "--run", str(run)) if run else trade(repo, log, "check")


def load_env_file(path="/etc/eu-executor.env"):
    """Run by hand, the settings systemd passes are not in the environment: read them."""
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except OSError:
        pass


def main(argv=None):
    load_env_file()
    global HOME
    HOME = Path(os.environ.get("EXECUTOR_HOME") or HOME)
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("cmd", choices=["flatten", "open", "check", "status"])
    ap.add_argument("--repo", default=os.environ.get("EXECUTOR_REPO") or str(HOME / "claude_research"))
    ap.add_argument("--give-up", default=OPEN_GIVE_UP_LOCAL, help="open: last Amsterdam time to wait")
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    log = Log()
    if a.cmd == "open":
        return cmd_open(repo, log, a.give_up)
    return {"flatten": cmd_flatten, "check": cmd_check, "status": cmd_status}[a.cmd](repo, log)


if __name__ == "__main__":
    sys.exit(main())
