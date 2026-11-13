#!/usr/bin/env python3
"""Stage H: the self-revising holistic US earnings researcher.

Subcommands (all paths relative to the repo root):

  pick     --run <RUN>            choose the day's names from stage E-P's sweep, assign the
                                  control arm, freeze both playbooks into the run
  brief    --run <RUN> --ticker T --arm evolving|control
                                  print the exact brief for one researcher
  collect  --run <RUN>            validate the hunts, write recommendations.json and note.md
  resolve  [--offline]            price every closed window on the stage's own window and
                                  freeze it into researcher_holistic/analysis/outcomes.json
  evaluate                        per-version scores, the paired control, stage E-P on the
                                  same names, and the gate; writes evaluation.json / .md
  revise   --proposal <FILE> [--run <RUN>]
                                  apply a reflector proposal if (and only if) the gates
                                  allow it; every proposal is logged, applied or not
  status                          current version, gate, last change
  selftest                        offline checks on synthetic data (used by smoke_test.py)

The window (fixed, never in the playbook): entry at the run day's close; an amc name exits
at the next session's opening print, a bmo name at 13:00 New York on its report day.

Everything the reflector may change lives in researcher_holistic/playbook/current.md.
Everything it may not (the window, the metrics, the gates, the control) lives here and in
config/pipeline.yaml `edge_holistic`, and smoke_test.py checks the control has not moved.
"""
import argparse
import contextlib
import io
import glob
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
# The researchers are blind to their arm: the evolving playbook is "a", the frozen control "b".
ARM_DIR = {"evolving": "a", "control": "b"}
ROOT = Path(__file__).resolve().parents[2]
P = {}  # paths, set by configure()


def configure(root=None, research=None):
    root = Path(root or ROOT)
    h = root / "researcher_holistic"
    P.update(root=root, research=Path(research or root / "research"), h=h,
             pb=h / "playbook", versions=h / "playbook" / "versions",
             current=h / "playbook" / "current.md", control=h / "playbook" / "control.md",
             changes=h / "playbook" / "changes.jsonl", changelog=h / "playbook" / "CHANGELOG.md",
             ana=h / "analysis", outcomes=h / "analysis" / "outcomes.json",
             eval_json=h / "analysis" / "evaluation.json", eval_md=h / "analysis" / "evaluation.md")


configure()


def cfg():
    try:
        import yaml
        c = yaml.safe_load(open(ROOT / "config" / "pipeline.yaml", encoding="utf-8"))
        return c["edge_holistic"]
    except Exception as e:  # pragma: no cover
        sys.exit(f"cannot read config/pipeline.yaml edge_holistic: {e}")


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def dump(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def now_utc():
    return datetime.now(timezone.utc)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- the playbook

HEADER_RE = re.compile(r"^<!-- playbook: (\S+) \| parent: (\S+) \| written: (\S+) \| by: (.*?) -->\s*$", re.M)
SECTION_RE = re.compile(r"^## \[(P\d+)\] (.+)$", re.M)


def parse_playbook(text):
    m = HEADER_RE.search(text)
    if not m:
        raise ValueError("playbook has no header line")
    body = text[m.end():]
    secs = list(SECTION_RE.finditer(body))
    pre = body[:secs[0].start()] if secs else body
    sections = []
    for i, s in enumerate(secs):
        end = secs[i + 1].start() if i + 1 < len(secs) else len(body)
        sections.append({"id": s.group(1), "title": s.group(2).strip(),
                         "text": body[s.end():end].strip("\n")})
    return {"version": m.group(1), "parent": m.group(2), "written": m.group(3),
            "by": m.group(4), "preamble": pre.strip("\n"), "sections": sections}


def render_playbook(pb):
    out = [f"<!-- playbook: {pb['version']} | parent: {pb['parent']} | written: {pb['written']} | by: {pb['by']} -->",
           pb["preamble"], ""]
    for s in pb["sections"]:
        out += [f"## [{s['id']}] {s['title']}", "", s["text"].strip("\n"), ""]
    return "\n".join(out).rstrip("\n") + "\n"


def version_of(path):
    return parse_playbook(Path(path).read_text(encoding="utf-8"))["version"]


def version_num(v):
    m = re.match(r"hp\.v(\d+)$", v or "")
    return int(m.group(1)) if m else 0


def next_version():
    nums = [version_num(Path(f).stem) for f in glob.glob(str(P["versions"] / "hp.v*.md"))]
    return f"hp.v{max(nums or [0]) + 1}"


# ---------------------------------------------------------------- runs

def run_dirs():
    return sorted(Path(p).parent for p in glob.glob(str(P["research"] / "*/*/*/edge-holistic/pick.json")))


def run_date_of(run):
    run = Path(run)
    if run.name == "edge-holistic":
        run = run.parent
    return run.name


def absrun(run):
    run = Path(run)
    return run if run.is_absolute() else (P["root"] / run)


def hdir(run):
    run = absrun(run)
    return run if run.name == "edge-holistic" else run / "edge-holistic"


def et_deadline_utc(run_date, hm):
    h, m = map(int, hm.split(":"))
    d = datetime.fromisoformat(run_date).replace(hour=h, minute=m, tzinfo=ET)
    return d.astimezone(timezone.utc)


def cmd_pick(run, source=None, force=False, max_names=None):
    c = cfg()
    out = hdir(run)
    if (out / "pick.json").exists() and not force:
        pk = load(out / "pick.json")
        print(f"pick.json exists (resume): {len(pk['names'])} names, playbook {pk['playbook_version']}")
        return pk
    src = absrun(source) if source else absrun(run) / c.get("names_from", "edge-panel")
    sweep = load(src / "sweep.json")
    if not sweep:
        print(f"NO SWEEP at {src}/sweep.json: stage E-P's sweep is not on this checkout. "
              "Pull main, or run stage E's steps 0-2 into edge-holistic and pass --source.")
        sys.exit(3)
    if sha(P["control"]) != c["playbook"]["control_sha256"]:
        sys.exit("the frozen control playbook has changed: refuse to run (restore it from git)")
    uni = load(src / "universe.json", {}) or {}
    company = {r.get("ticker"): r.get("company") for r in uni.get("names", [])}
    rows = []
    for n in sweep.get("names", []):
        t = n.get("ticker")
        if not n.get("event_confirmed") or not t:
            continue
        b = load(src / "baselines" / f"{t}.json")
        if not b:
            continue
        rows.append({"ticker": t, "company": company.get(t),
                     "event_date": n.get("actual_event_date") or b.get("event_date") or sweep.get("event_date"),
                     "session": b.get("session") or sweep.get("session"),
                     "hunt_priority": n.get("hunt_priority") or 0,
                     "baseline": str((src / "baselines" / f"{t}.json").relative_to(P["root"])),
                     "sweep": str((src / "sweep.json").relative_to(P["root"]))})
    rows.sort(key=lambda r: (-(r["hunt_priority"] or 0), r["ticker"]))
    cap = int(max_names or c["max_names"])
    shed = [r["ticker"] for r in rows[cap:]]
    rows = rows[:cap]
    rd = run_date_of(run)
    rng = random.Random(f"stage-H-control-{rd}")
    share = float(c["control_share"])
    k = len(rows) if share >= 1 else int(round(share * len(rows)))
    ctl = set(rng.sample(sorted(r["ticker"] for r in rows), k)) if rows else set()
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(P["current"], out / "playbook-a.md")
    shutil.copyfile(P["control"], out / "playbook-b.md")
    for r in rows:
        r["arms"] = ["evolving"] + (["control"] if r["ticker"] in ctl else [])
        for a in r["arms"]:
            (out / "work" / ARM_DIR[a] / r["ticker"]).mkdir(parents=True, exist_ok=True)
    (out / "hunts").mkdir(exist_ok=True)
    (out / "hunts-b").mkdir(exist_ok=True)
    pk = {"run_date": rd, "generated_utc": now_utc().isoformat(timespec="seconds"),
          "source": str(src.relative_to(P["root"])),
          "playbook_version": version_of(P["current"]),
          "control_version": "control:" + version_of(P["control"]),
          "control_seed": f"stage-H-control-{rd}", "control_share": share,
          "control_design": control_design(share), "arm_files": {"evolving": "playbook-a.md, hunts/, work/a/",
                                                                  "control": "playbook-b.md, hunts-b/, work/b/"}, "cap": cap, "shed": shed,
          "research_deadline_utc": et_deadline_utc(rd, c["research_deadline_et"]).isoformat(),
          "names": rows}
    dump(out / "pick.json", pk)
    print(f"{len(rows)} names (cap {cap}, shed {len(shed)}), {k} also on the control; "
          f"playbook {pk['playbook_version']}, control {pk['control_version']}")
    for r in rows:
        print(f"  {r['ticker']:6} {r['session']} {r['event_date']}  prio {r['hunt_priority']}  {'+'.join(r['arms'])}")
    return pk


# Until 2026-11-13 the control ran on a date-seeded random 34% of the names; from then on
# (operator's instruction, to reach a usable paired sample sooner) it runs on every name.
# Runs before the change carry no control_design field and are this legacy value.
LEGACY_CONTROL_DESIGN = "random_share_0.34"


def control_design(share):
    return "all_names" if share >= 1 else f"random_share_{share:g}"


def hunt_path(run, ticker, arm):
    return hdir(run) / ("hunts" if arm == "evolving" else "hunts-b") / f"{ticker}.json"


def cmd_brief(run, ticker, arm):
    pk = load(hdir(run) / "pick.json")
    r = next((x for x in pk["names"] if x["ticker"] == ticker), None)
    if r is None or arm not in r["arms"]:
        sys.exit(f"{ticker} is not in pick.json on the {arm} arm")
    pb = hdir(run) / f"playbook-{ARM_DIR[arm]}.md"
    dl = datetime.fromisoformat(pk["research_deadline_utc"])
    txt = (f"Ticker {ticker} ({r.get('company') or 'company: see the baseline'}), reports "
           f"{r['event_date']} {r['session']}. Run day {pk['run_date']}.\n"
           f"Your playbook: {P['root'] / pb.relative_to(P['root'])} (read it in full first).\n"
           f"Sealed baseline: {P['root'] / r['baseline']}. Your sweep row: the '{ticker}' row of "
           f"{P['root'] / r['sweep']} (read that row only).\n"
           f"Write your JSON to {hunt_path(run, ticker, arm)}.\n"
           f"Your work directory: {hdir(run) / 'work' / ARM_DIR[arm] / ticker}/. Write drafts and downloads "
           "only there; never use /tmp or a shared folder. Apart from the baseline and the sweep row named "
           "above, never read another ticker's files or any other stage's files in this repository.\n"
           f"Your research stops at {dl.strftime('%H:%M')} UTC today (run `date -u`); emit what you have by then.")
    print(txt)
    return txt


# ---------------------------------------------------------------- collect

def check_hunt(h):
    """Returns (status, problems, normalised recommendation)."""
    probs = []
    if h is None:
        return "missing", ["no file"], None
    if h.get("contamination"):
        return "contaminated", [str(h["contamination"])], None
    if h.get("search_complete") is False:
        return "unfinished", [h.get("search_incomplete_reason") or "search_complete false"], None
    try:
        p = float(h["p_up"])
    except Exception:
        return "invalid", ["p_up missing"], None
    if not 0 <= p <= 100:
        return "invalid", ["p_up out of range"], None
    rec = dict(h.get("recommendation") or {})
    act = (rec.get("action") or "none").lower()
    if act not in ("long", "short", "none"):
        probs.append(f"unknown action {act}")
        act = "none"
    want = p if act == "long" else 100 - p if act == "short" else max(p, 100 - p)
    if act == "long" and p <= 50 or act == "short" and p >= 50:
        probs.append(f"{act} contradicts p_up {p}: recommendation dropped")
        act = "none"
        want = max(p, 100 - p)
    try:
        if abs(float(rec.get("confidence_pct")) - want) > 1:
            probs.append(f"confidence_pct {rec.get('confidence_pct')} reset to {want}")
    except Exception:
        probs.append(f"confidence_pct missing, set to {want}")
    rec.update(action=act, confidence_pct=round(want, 1))
    return "ok", probs, rec


def cmd_collect(run):
    out = hdir(run)
    pk = load(out / "pick.json")
    late_at = et_deadline_utc(pk["run_date"], "16:00")
    rows = []
    for r in pk["names"]:
        for arm in r["arms"]:
            hp = hunt_path(run, r["ticker"], arm)
            h = load(hp)
            st, probs, rec = check_hunt(h)
            if st == "ok":
                emitted = h.get("emitted_utc")
                mt = datetime.fromtimestamp(hp.stat().st_mtime, timezone.utc)
                if mt > late_at:
                    st, probs = "late", probs + [f"written {mt.isoformat(timespec='minutes')}, after the 16:00 ET close"]
            row = {"ticker": r["ticker"], "arm": arm, "session": r["session"],
                   "event_date": r["event_date"], "status": st, "problems": probs,
                   "playbook_version": pk["playbook_version"] if arm == "evolving" else pk["control_version"],
                   "control_design": pk.get("control_design", LEGACY_CONTROL_DESIGN),
                   "hunt": str(hp.relative_to(P["root"]))}
            if st == "ok":
                row.update(p_up=float(h["p_up"]), expected_move_pct=h.get("expected_move_pct"),
                           abs_move_pct=h.get("abs_move_pct"), action=rec["action"],
                           confidence_pct=rec["confidence_pct"], reason=rec.get("reason"),
                           what_would_flip_it=rec.get("what_would_flip_it"),
                           unpriced=h.get("unpriced"))
            rows.append(row)
    recs = sorted([x for x in rows if x["arm"] == "evolving" and x.get("action") in ("long", "short")],
                  key=lambda x: -x["confidence_pct"])
    doc = {"run_date": pk["run_date"], "generated_utc": now_utc().isoformat(timespec="seconds"),
           "playbook_version": pk["playbook_version"], "control_version": pk["control_version"],
           "control_design": pk.get("control_design", LEGACY_CONTROL_DESIGN),
           "window": "entry run-day close; amc out at next open, bmo out 13:00 ET report day",
           "recommended": [{k: x.get(k) for k in ("ticker", "session", "event_date", "action",
                                                   "confidence_pct", "p_up", "expected_move_pct",
                                                   "reason", "what_would_flip_it")} for x in recs],
           "names": rows}
    dump(out / "recommendations.json", doc)
    lines = [f"# Stage H, {pk['run_date']}: holistic researcher, playbook {pk['playbook_version']}", "",
             "Stage H is an experiment: one Opus 5.5 researcher per name searches and judges in one "
             "loop and follows a playbook the stage revises from its own resolved days. A frozen copy "
             + ("of the first playbook researches every name as the control. No orders. "
                if pk.get("control_design") == "all_names" else
                "of the first playbook runs on a random third of the names as the control. No orders. ")
             + "One day is an anecdote.", "",
             "Window: entry at today's close; amc out at the next open, bmo out at 13:00 ET on the report day.", "",
             "## Recommendations (evolving playbook)", ""]
    if recs:
        lines += ["| ticker | session | action | confidence | p_up | exp. move | reason | what would flip it |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for x in recs:
            lines.append(f"| {x['ticker']} | {x['session']} | {x['action']} | {x['confidence_pct']:.0f} | "
                         f"{x['p_up']:.0f} | {x.get('expected_move_pct')} | {(x.get('reason') or '').replace('|', '/')} | "
                         f"{(x.get('what_would_flip_it') or '').replace('|', '/')} |")
    else:
        lines.append("None today: no name cleared the playbook's bar.")
    lines += ["", "## Every name", "", "| ticker | arm | status | p_up | action | confidence |",
              "| --- | --- | --- | --- | --- | --- |"]
    for x in rows:
        lines.append(f"| {x['ticker']} | {x['arm']} | {x['status']} | {x.get('p_up', '')} | "
                     f"{x.get('action', '')} | {x.get('confidence_pct', '')} |")
    bad = [x for x in rows if x["status"] != "ok" or x["problems"]]
    if bad:
        lines += ["", "## Problems", ""] + [f"- {x['ticker']} ({x['arm']}): {x['status']}; {'; '.join(x['problems'])}" for x in bad]
    lines += ["", "This is a forecasting exercise over public information, not investment advice.", ""]
    (out / "note.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(recs)} recommendation(s); {sum(1 for x in rows if x['status'] == 'ok')} of {len(rows)} hunts ok")
    for x in recs:
        print(f"  {x['ticker']:6} {x['action']:5} conf {x['confidence_pct']:.0f}  p_up {x['p_up']:.0f}")
    return doc


# ---------------------------------------------------------------- prices

_cache = {}


def _yahoo(sym, rng, interval):
    key = (sym, rng, interval)
    if key in _cache:
        return _cache[key]
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={interval}"
    out = None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            out = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
            break
        except Exception:
            time.sleep(1 + i)
    _cache[key] = out
    return out


class Prices:
    """Daily (open, close) by ET date and 5-minute closes by ET date and minute."""

    def __init__(self, fixture=None):
        self.fixture = fixture

    def daily(self, sym):
        if self.fixture is not None:
            return {d: tuple(v) for d, v in (self.fixture.get(sym, {}).get("daily") or {}).items()}
        r = _yahoo(sym, "3mo", "1d")
        if not r:
            return {}
        q = r["indicators"]["quote"][0]
        out = {}
        for ts, o, c in zip(r.get("timestamp") or [], q["open"], q["close"]):
            out[datetime.fromtimestamp(ts, ET).date().isoformat()] = (o, c)
        return out

    def at(self, sym, day, hm):
        """Last 5-minute close at or before hm (minutes after midnight ET), within an hour."""
        if self.fixture is not None:
            m5 = (self.fixture.get(sym, {}).get("m5") or {}).get(day) or {}
            ok = [(int(k), v) for k, v in m5.items() if hm - 60 <= int(k) <= hm and v]
            return max(ok)[1] if ok else None
        r = _yahoo(sym, "60d", "5m")
        if not r:
            return None
        q, best = r["indicators"]["quote"][0], None
        for ts, c in zip(r.get("timestamp") or [], q["close"]):
            d = datetime.fromtimestamp(ts, ET)
            m = d.hour * 60 + d.minute
            if c is not None and d.date().isoformat() == day and hm - 60 <= m < hm:
                best = c
        return best


def price_window(prices, sym, run_date, event_date, session, today):
    """(entry, exit, entry_day, exit_day, state). state: closed | pending | no_data."""
    bars = prices.daily(sym)
    if not bars:
        return None, None, None, None, "no_data"
    e = bars.get(run_date)
    if not e or not e[1]:
        return None, None, run_date, None, ("pending" if run_date >= today else "no_data")
    entry = e[1]
    after = sorted(d for d, v in bars.items() if d > run_date and v and v[0])
    if session == "amc":
        if not after:
            return entry, None, run_date, None, "pending"
        return entry, bars[after[0]][0], run_date, after[0], "closed"
    xd = event_date if event_date and event_date > run_date else (after[0] if after else None)
    if not xd or xd not in bars:
        return entry, None, run_date, xd, "pending"
    px = prices.at(sym, xd, 13 * 60)
    if not px:
        return entry, None, run_date, xd, "pending"
    return entry, px, run_date, xd, "closed"


def ep_view(run_root, ticker):
    p = load(Path(run_root) / "edge-panel" / "edge-scores-panel.json")
    if not p:
        return None
    bt = p.get("ranking_by_ticker") or {}
    if isinstance(bt, list):  # panel_score.py writes a list of rows
        r = next((x for x in bt if x.get("ticker") == ticker), None)
    else:
        r = bt.get(ticker)
    if r is None:
        r = next((x for x in p.get("ranking", []) if x.get("ticker") == ticker), None)
    if not r:
        return None
    return {"panel_pct_signed": r.get("panel_pct_signed"), "selected": bool(r.get("selected", r.get("panel_selected"))),
            "n_members": r.get("n_members")}


def cmd_resolve(offline=False, prices=None, today=None):
    if offline and prices is None:
        print("offline: nothing priced")
        return load(P["outcomes"], {"rows": {}})
    prices = prices or Prices()
    today = today or datetime.now(ET).date().isoformat()
    oc = load(P["outcomes"], {"rows": {}}) or {"rows": {}}
    added = pending = 0
    for hd in run_dirs():
        rec = load(hd / "recommendations.json")
        if not rec:
            continue
        rd = rec["run_date"]
        for x in rec["names"]:
            if x["status"] != "ok":
                continue
            key = f"{rd}/{x['arm']}/{x['ticker']}"
            if key in oc["rows"]:
                continue
            entry, ex, ed, xd, st = price_window(prices, x["ticker"], rd, x["event_date"], x["session"], today)
            if st != "closed":
                pending += 1
                continue
            mv = (ex / entry - 1) * 100
            sgn = 1 if x["action"] == "long" else -1 if x["action"] == "short" else 0
            oc["rows"][key] = {"run_date": rd, "ticker": x["ticker"], "arm": x["arm"],
                               "playbook_version": x["playbook_version"],
                               "control_design": x.get("control_design") or rec.get("control_design")
                               or LEGACY_CONTROL_DESIGN, "session": x["session"],
                               "event_date": x["event_date"], "p_up": x["p_up"], "action": x["action"],
                               "confidence_pct": x["confidence_pct"],
                               "expected_move_pct": x.get("expected_move_pct"),
                               "entry": round(entry, 4), "exit": round(ex, 4), "entry_day": ed,
                               "exit_day": xd, "move_pct": round(mv, 3),
                               "rec_return_pct": round(sgn * mv, 3) if sgn else None,
                               "ep": ep_view(hd.parent, x["ticker"]), "hunt": x["hunt"],
                               "resolved_utc": now_utc().isoformat(timespec="seconds")}
            added += 1
    oc["updated_utc"] = now_utc().isoformat(timespec="seconds")
    oc["window"] = "entry run-day close; amc exit next open; bmo exit 13:00 ET report day"
    dump(P["outcomes"], oc)
    print(f"resolved {added} new name-arm(s), {pending} still pending, {len(oc['rows'])} in outcomes")
    return oc


# ---------------------------------------------------------------- statistics

def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-30 else 1e-30)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c
        c = c if abs(c) > 1e-30 else 1e-30
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c
        c = c if abs(c) > 1e-30 else 1e-30
        de = d * c
        h *= de
        if abs(de - 1) < 1e-12:
            break
    return h


def _ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * _betacf(a, b, x) / a
    return 1 - math.exp(lb) * _betacf(b, a, 1 - x) / b


def t_p(t, df):
    if df <= 0 or t is None:
        return None
    return _ibeta(df / 2, 0.5, df / (df + t * t))


def binom_p(k, n):
    if n == 0:
        return None
    pk = [math.comb(n, i) * 0.5 ** n for i in range(n + 1)]
    return min(1.0, sum(v for v in pk if v <= pk[k] + 1e-12))


def mean_t(xs):
    n = len(xs)
    if n == 0:
        return {"n": 0}
    m = sum(xs) / n
    if n < 2:
        return {"n": n, "mean": round(m, 3)}
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    t = m / (sd / math.sqrt(n)) if sd > 0 else None
    return {"n": n, "mean": round(m, 3), "sd": round(sd, 3),
            "t": round(t, 2) if t is not None else None,
            "p": round(t_p(t, n - 1), 3) if t is not None else None}


def brier(r):
    up = 1.0 if r["move_pct"] > 0 else 0.0
    return (r["p_up"] / 100 - up) ** 2


def score(rows, cut):
    out = {"names": len(rows), "run_days": len({r["run_date"] for r in rows})}
    if not rows:
        return out
    b = [brier(r) for r in rows]
    out["brier"] = round(sum(b) / len(b), 4)
    out["brier_skill_vs_coin"] = round(1 - out["brier"] / 0.25, 3)
    d = [r for r in rows if r["p_up"] != 50]
    hits = sum(1 for r in d if (r["p_up"] > 50) == (r["move_pct"] > 0))
    out["direction"] = {"n": len(d), "hits": hits, "p": binom_p(hits, len(d)) if d else None}
    rec = [r for r in rows if r.get("rec_return_pct") is not None]
    rh = sum(1 for r in rec if r["rec_return_pct"] > 0)
    out["recommended"] = dict(mean_t([r["rec_return_pct"] for r in rec]), hits=rh,
                              hit_p=binom_p(rh, len(rec)) if rec else None)
    fx = [r for r in rows if abs(r["p_up"] - 50) >= cut - 50]
    fr = [(1 if r["p_up"] > 50 else -1) * r["move_pct"] for r in fx]
    out[f"fixed_cut_{cut}"] = dict(mean_t(fr), hits=sum(1 for v in fr if v > 0))
    # The stage's claim is that SOME events can be called with some certainty, not that
    # the average view beats a coin (operator, 2026-11-11). So the views are also scored
    # by how far they lean: each rung keeps only views at least that far from 50 and
    # prices them on the lean's side. Read the rungs, not only the Brier.
    lad = {}
    for k in LEAN_RUNGS:
        sub = [r for r in rows if abs(r["p_up"] - 50) >= k and r["move_pct"] != 0]
        sv = [(1 if r["p_up"] > 50 else -1) * r["move_pct"] for r in sub]
        h = sum(1 for v in sv if v > 0)
        lad[f">={k}"] = dict(mean_t(sv), hits=h, hit_p=round(binom_p(h, len(sv)), 3) if sv else None)
    out["leaning"] = lad
    return out


LEAN_RUNGS = (5, 7, 10)


def cmd_evaluate(write=True, quiet=False):
    c = cfg()
    g = c["gates"]
    cut = c.get("recommend_cut_fixed", 65)
    oc = load(P["outcomes"], {"rows": {}}) or {"rows": {}}
    rows = list(oc["rows"].values())
    evo = [r for r in rows if r["arm"] == "evolving"]
    ctl = [r for r in rows if r["arm"] == "control"]
    versions = sorted({r["playbook_version"] for r in evo}, key=version_num)
    by_version = {v: score([r for r in evo if r["playbook_version"] == v], cut) for v in versions}
    cidx = {(r["run_date"], r["ticker"]): r for r in ctl}
    pairs = sorted([(r, cidx[(r["run_date"], r["ticker"])]) for r in evo if (r["run_date"], r["ticker"]) in cidx],
                   key=lambda pr: (pr[0]["run_date"], pr[0]["ticker"]))

    def paired(ps):
        d = mean_t([brier(a) - brier(b) for a, b in ps])
        d["meaning"] = "evolving Brier minus control Brier on the same names; below 0 means the evolving playbook was better"
        return d

    paired_by_version = {v: paired([p for p in pairs if p[0]["playbook_version"] == v]) for v in versions}
    lineage = paired(pairs)
    designs = sorted({p[0].get("control_design") or LEGACY_CONTROL_DESIGN for p in pairs})
    paired_by_design = {dz: paired([p for p in pairs if (p[0].get("control_design") or LEGACY_CONTROL_DESIGN) == dz])
                        for dz in designs}
    epsel = [r for r in evo if (r.get("ep") or {}).get("selected")]
    ep_rets = [(1 if r["ep"]["panel_pct_signed"] > 0 else -1) * r["move_pct"] for r in epsel]
    ep_block = dict(mean_t(ep_rets), hits=sum(1 for v in ep_rets if v > 0),
                    note="stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window")
    days = sorted({r["run_date"] for r in rows})
    last5 = days[-5:]
    rolling = {"run_days": last5,
               "evolving": score([r for r in evo if r["run_date"] in last5], cut),
               "control": score([r for r in ctl if r["run_date"] in last5], cut)}
    cur = version_of(P["current"])
    since = [r for r in evo if r["playbook_version"] == cur]
    nd = len({r["run_date"] for r in since})
    gate_open = len(since) >= g["min_resolved_names"] and nd >= g["min_run_days"]
    recent = pairs[-g["drift_window_pairs"]:]
    dr = paired(recent)
    alarm = bool(dr.get("n", 0) >= g["drift_min_pairs"] and dr.get("t") is not None
                 and dr["mean"] > 0 and dr["t"] >= g["drift_t"])
    gate = {"current_version": cur, "resolved_names_on_current": len(since), "run_days_on_current": nd,
            "min_resolved_names": g["min_resolved_names"], "min_run_days": g["min_run_days"],
            "open": gate_open, "drift_alarm": alarm, "drift": dr,
            "rule": (f"revise only with >= {g['min_resolved_names']} resolved names over >= {g['min_run_days']} run days "
                     f"on the current version; at most {g['max_ops']} ops, each citing >= {g['min_evidence_names_per_op']} "
                     "resolved names; on a drift alarm only revert_to")}
    ev = {"generated_utc": now_utc().isoformat(timespec="seconds"), "window": oc.get("window"),
          "resolved_rows": len(rows), "by_version": by_version, "control": score(ctl, cut),
          "paired_vs_control_by_version": paired_by_version, "paired_vs_control_lineage": lineage,
          "paired_vs_control_by_design": paired_by_design,
          "design_note": ("random_share_0.34: before 2026-11-13 the control ran on a date-seeded random third "
                          "of the names; all_names: from 2026-11-13 it runs on every name. Both are paired on "
                          "the same names; read them apart before pooling."),
          "lineage_note": ("The lineage row pools every evolving version on purpose: it tests the PROCESS "
                           "(does self-revision beat a frozen approach on the same names), not any one version. "
                           "Judge a version only on its own row."),
          "stage_ep_same_names": ep_block, "rolling_last_5_days": rolling, "gate": gate,
          "small_sample_warning": "Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing."}
    if write:
        dump(P["eval_json"], ev)
        P["eval_md"].write_text(eval_md(ev), encoding="utf-8")
    if not quiet:
        print(eval_md(ev))
    return ev


def _fmt(s):
    if not s or not s.get("names"):
        return "no resolved names"
    d, r = s["direction"], s["recommended"]
    rec = (f"{r['n']} recs, {r['hits']} right, mean {r.get('mean')}% (t {r.get('t')}, p {r.get('p')})"
           if r.get("n") else "0 recs")
    lean = "; ".join(f"|p_up-50| {k}: {v['hits']}/{v['n']} right, {v.get('mean')}% on the lean's side"
                     f" (t {v.get('t')}, p {v.get('hit_p')})" for k, v in (s.get("leaning") or {}).items() if v.get("n"))
    return (f"{s['names']} names / {s['run_days']} days; Brier {s['brier']} (skill {s['brier_skill_vs_coin']}); "
            f"direction {d['hits']}/{d['n']} (p {d['p']}); {rec}"
            + (f"; leaning views: {lean}" if lean else "; no view leans 5 or more"))


def eval_md(ev):
    L = ["# Stage H evaluation", "", f"Generated {ev['generated_utc']}. Window: {ev['window']}.", "",
         ev["small_sample_warning"], "",
         "Read the leaning views first: the claim under test is that some events can be called with "
         "some certainty, so a version is judged on the views it leans on and on its recommendations, "
         "not on its average Brier alone.", "", "## Per playbook version (evolving arm)", ""]
    for v, s in ev["by_version"].items():
        L.append(f"- **{v}**: {_fmt(s)}; vs control on the same names: "
                 f"{ev['paired_vs_control_by_version'][v].get('n', 0)} pairs, Brier diff "
                 f"{ev['paired_vs_control_by_version'][v].get('mean')} (t {ev['paired_vs_control_by_version'][v].get('t')})")
    if not ev["by_version"]:
        L.append("- nothing resolved yet")
    lg = ev["paired_vs_control_lineage"]
    ep = ev["stage_ep_same_names"]
    g = ev["gate"]
    L += ["", f"- **control (frozen hp.v1)**: {_fmt(ev['control'])}", ""]
    for dz, d in (ev.get("paired_vs_control_by_design") or {}).items():
        L.append(f"- pairs with control design **{dz}**: {d.get('n', 0)}, Brier diff {d.get('mean')} (t {d.get('t')})")
    L += ["",
          "## The process: every evolving version against the frozen control, same names", "",
          f"{lg.get('n', 0)} pairs, mean Brier difference {lg.get('mean')} (t {lg.get('t')}, p {lg.get('p')}). "
          + ev["lineage_note"], "",
          "## Stage E-P on the same names", "",
          f"{ep.get('n', 0)} selected calls, {ep.get('hits', 0)} right, mean {ep.get('mean')}% (t {ep.get('t')}). {ep['note']}.", "",
          "## Last five run days", "",
          f"- evolving: {_fmt(ev['rolling_last_5_days']['evolving'])}",
          f"- control: {_fmt(ev['rolling_last_5_days']['control'])}", "",
          "## Gate", "",
          f"Current version {g['current_version']}: {g['resolved_names_on_current']} resolved names over "
          f"{g['run_days_on_current']} run days (needs {g['min_resolved_names']} over {g['min_run_days']}). "
          f"Gate {'OPEN' if g['open'] else 'closed'}. Drift alarm: {'YES' if g['drift_alarm'] else 'no'} "
          f"({g['drift'].get('n', 0)} recent pairs, diff {g['drift'].get('mean')}, t {g['drift'].get('t')}).", "",
          g["rule"], ""]
    return "\n".join(L)


# ---------------------------------------------------------------- revise

def log_change(entry):
    P["changes"].parent.mkdir(parents=True, exist_ok=True)
    with open(P["changes"], "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def known_tickers(oc):
    return {r["ticker"] for r in oc["rows"].values()}


def cmd_revise(proposal_path, run=None, by="holistic-reflector"):
    c = cfg()
    g = c["gates"]
    prop = load(proposal_path)
    ev = cmd_evaluate(write=True, quiet=True)
    gate = ev["gate"]
    oc = load(P["outcomes"], {"rows": {}}) or {"rows": {}}
    resolved = {f"{r['run_date']}/{r['ticker']}" for r in oc["rows"].values()}
    cur_text = P["current"].read_text(encoding="utf-8")
    pb = parse_playbook(cur_text)
    entry = {"utc": now_utc().isoformat(timespec="seconds"), "run": str(run) if run else None,
             "from_version": pb["version"], "gate": {k: gate[k] for k in ("resolved_names_on_current",
                                                                         "run_days_on_current", "open", "drift_alarm")},
             "proposal": str(proposal_path)}
    if not prop:
        entry.update(status="rejected", reasons=["proposal missing or not JSON"])
        log_change(entry)
        print("REJECTED: proposal missing or not JSON")
        return entry
    entry.update(decision=prop.get("decision"), diagnosis=prop.get("diagnosis"), ops=prop.get("ops") or [],
                 past_changes_review=prop.get("past_changes_review"))
    reasons = []
    ops = prop.get("ops") or []
    if prop.get("decision") != "revise" or not ops:
        entry.update(status="kept", reasons=["reflector chose to keep the approach"])
        log_change(entry)
        print(f"KEPT {pb['version']}: reflector proposed no change")
        return entry
    if not gate["open"] and not gate["drift_alarm"]:
        reasons.append(f"gate closed: {gate['resolved_names_on_current']}/{g['min_resolved_names']} names, "
                       f"{gate['run_days_on_current']}/{g['min_run_days']} days on {pb['version']}")
    if gate["drift_alarm"] and any(o.get("op") != "revert_to" for o in ops):
        reasons.append("drift alarm: only revert_to is allowed")
    if len(ops) > g["max_ops"]:
        reasons.append(f"{len(ops)} ops, max {g['max_ops']}")
    tick = known_tickers(oc)
    new = json.loads(json.dumps(pb))
    for i, o in enumerate(ops):
        ev_names = [n for n in (o.get("evidence_names") or []) if n in resolved]
        if len(ev_names) < g["min_evidence_names_per_op"]:
            reasons.append(f"op {i + 1}: {len(ev_names)} resolved evidence names, needs {g['min_evidence_names_per_op']}")
        for k in ("rationale", "predicted_effect", "revert_if"):
            if not (o.get(k) or "").strip():
                reasons.append(f"op {i + 1}: missing {k}")
        txt = (o.get("text") or "") + " " + (o.get("title") or "")
        named = sorted(t for t in tick if len(t) >= 2 and re.search(rf"(?<![A-Za-z0-9]){re.escape(t)}(?![A-Za-z0-9])", txt))
        if named:
            reasons.append(f"op {i + 1}: names a ticker in playbook text ({', '.join(named)}); write the mechanism, not the company")
        kind = o.get("op")
        ids = [s["id"] for s in new["sections"]]
        if kind == "edit":
            if o.get("id") not in ids or not (o.get("text") or "").strip():
                reasons.append(f"op {i + 1}: edit needs an existing id and text")
            else:
                s = new["sections"][ids.index(o["id"])]
                s["text"] = o["text"].strip("\n")
                if o.get("title"):
                    s["title"] = o["title"].strip()
        elif kind == "add":
            if not (o.get("text") or "").strip() or not (o.get("title") or "").strip():
                reasons.append(f"op {i + 1}: add needs title and text")
            else:
                nid = f"P{max([int(x[1:]) for x in ids] or [0]) + 1}"
                sec = {"id": nid, "title": o["title"].strip(), "text": o["text"].strip("\n")}
                pos = ids.index(o["after"]) + 1 if o.get("after") in ids else len(ids)
                new["sections"].insert(pos, sec)
        elif kind == "remove":
            if o.get("id") not in ids:
                reasons.append(f"op {i + 1}: remove needs an existing id")
            else:
                del new["sections"][ids.index(o["id"])]
        elif kind == "revert_to":
            vf = P["versions"] / f"{o.get('version')}.md"
            if len(ops) != 1:
                reasons.append("revert_to must be the only op")
            elif not vf.exists() or o.get("version") == pb["version"]:
                reasons.append(f"op {i + 1}: unknown or current version {o.get('version')}")
            else:
                old = parse_playbook(vf.read_text(encoding="utf-8"))
                new["preamble"], new["sections"] = old["preamble"], old["sections"]
        else:
            reasons.append(f"op {i + 1}: unknown op {kind}")
    if not new["sections"]:
        reasons.append("the playbook would be empty")
    v = next_version()
    new.update(version=v, parent=pb["version"], written=now_utc().date().isoformat(), by=by)
    text = render_playbook(new)
    if len(text) > c["playbook"]["max_chars"]:
        reasons.append(f"playbook would be {len(text)} chars, max {c['playbook']['max_chars']}")
    if reasons:
        entry.update(status="rejected", reasons=reasons)
        log_change(entry)
        print("REJECTED:\n  " + "\n  ".join(reasons))
        return entry
    (P["versions"] / f"{v}.md").write_text(text, encoding="utf-8")
    P["current"].write_text(text, encoding="utf-8")
    entry.update(status="applied", to_version=v, reasons=[], sha256=hashlib.sha256(text.encode()).hexdigest())
    log_change(entry)
    with open(P["changelog"], "a", encoding="utf-8") as f:
        f.write(f"\n## {v} (from {pb['version']}), {entry['utc']}\n\n{prop.get('diagnosis') or ''}\n\n")
        for o in ops:
            f.write(f"- `{o.get('op')}` {o.get('id') or o.get('version') or o.get('title') or ''}: {o.get('rationale')}\n"
                    f"  - evidence: {', '.join(o.get('evidence_names') or [])}\n"
                    f"  - predicted: {o.get('predicted_effect')}\n  - revert if: {o.get('revert_if')}\n")
    print(f"APPLIED: {pb['version']} -> {v} ({len(ops)} op(s)); next run uses {v}")
    return entry


def cmd_status():
    ev = cmd_evaluate(write=False, quiet=True)
    g = ev["gate"]
    last = None
    if P["changes"].exists():
        lines = [x for x in P["changes"].read_text(encoding="utf-8").splitlines() if x.strip()]
        last = json.loads(lines[-1]) if lines else None
    print(f"current playbook {g['current_version']}; control {version_of(P['control'])}; "
          f"gate {'open' if g['open'] else 'closed'} ({g['resolved_names_on_current']}/{g['min_resolved_names']} names, "
          f"{g['run_days_on_current']}/{g['min_run_days']} days); drift alarm {g['drift_alarm']}")
    if last:
        print(f"last change: {last['utc']} {last['status']} {last.get('from_version')} -> {last.get('to_version', '-')}")


# ---------------------------------------------------------------- selftest

def selftest():
    """Offline checks on a throwaway tree. Returns a list of (label, ok, detail)."""
    res = []
    saved = dict(P)
    tmp = Path(tempfile.mkdtemp(prefix="stageH-"))
    try:
        (tmp / "researcher_holistic" / "playbook" / "versions").mkdir(parents=True)
        for f in ("current.md", "control.md", "versions/hp.v1.md"):
            # The fixture starts a fresh lineage at hp.v1 whatever the live playbook has
            # reached: copying the live current.md broke this test once hp.v2 shipped.
            shutil.copyfile(saved["pb"] / f if f == "control.md" else saved["versions"] / "hp.v1.md",
                            tmp / "researcher_holistic" / "playbook" / f)
        configure(tmp)
        sink = io.StringIO()
        _ctx = contextlib.redirect_stdout(sink)
        _ctx.__enter__()
        pb = parse_playbook(P["current"].read_text(encoding="utf-8"))
        res.append(("playbook parses and renders back identically",
                    render_playbook(pb) == P["current"].read_text(encoding="utf-8") and len(pb["sections"]) >= 5, pb["version"]))
        # a synthetic E-P run with 6 names over 4 days
        fixture = {}
        days = ["2026-08-03", "2026-08-04", "2026-08-05", "2026-08-06", "2026-08-07", "2026-08-10"]
        tickers = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]
        rnd = random.Random(7)
        for t in tickers:
            daily, m5 = {}, {}
            px = 50.0
            for d in days:
                o = px * (1 + rnd.uniform(-0.05, 0.05))
                cl = o * (1 + rnd.uniform(-0.03, 0.03))
                daily[d] = [o, cl]
                m5[d] = {str(13 * 60 - 5): cl * 1.01}
                px = cl
            fixture[t] = {"daily": daily, "m5": m5}
        for d in days[:4]:
            run = tmp / "research" / d[:4] / d[5:7] / d
            ep = run / "edge-panel"
            (ep / "baselines").mkdir(parents=True)
            names = []
            for i, t in enumerate(tickers):
                sess = "amc" if i % 2 == 0 else "bmo"
                nxt = days[days.index(d) + 1]
                ev_d = d if sess == "amc" else nxt
                dump(ep / "baselines" / f"{t}.json", {"ticker": t, "event_date": ev_d, "session": sess})
                names.append({"ticker": t, "event_confirmed": True, "hunt_priority": 100 - i, "actual_event_date": ev_d})
            dump(ep / "sweep.json", {"event_date": d, "session": "amc", "names": names})
            dump(ep / "edge-scores-panel.json", {"ranking_by_ticker": {"AAA": {"panel_pct_signed": 85, "selected": True}}})
            pk = cmd_pick(run, max_names=8)
            for r in pk["names"]:
                for arm in r["arms"]:
                    p = rnd.choice([30, 45, 50, 55, 72])
                    act = "long" if p >= 65 else "short" if p <= 35 else "none"
                    dump(hunt_path(run, r["ticker"], arm),
                         {"ticker": r["ticker"], "p_up": p, "search_complete": True,
                          "recommendation": {"action": act, "confidence_pct": max(p, 100 - p)}})
                    ts = et_deadline_utc(d, "15:30").timestamp()
                    os.utime(hunt_path(run, r["ticker"], arm), (ts, ts))
            cmd_collect(run)
        res.append(("pick takes the sweep's confirmed names by priority and assigns a seeded control",
                    len(pk["names"]) == 8 and pk["names"][0]["ticker"] == "AAA"
                    and sum("control" in r["arms"] for r in pk["names"]) == (8 if cfg()["control_share"] >= 1
                                                                            else round(cfg()["control_share"] * 8))
                    and pk["control_design"] == control_design(float(cfg()["control_share"])), ""))
        pk2 = cmd_pick(run, max_names=8, force=True)
        res.append(("the control draw is reproducible from the date",
                    [r["arms"] for r in pk2["names"]] == [r["arms"] for r in pk["names"]], ""))
        st, probs, rec = check_hunt({"p_up": 40, "recommendation": {"action": "long", "confidence_pct": 60}})
        res.append(("a long against p_up below 50 is dropped, not traded", st == "ok" and rec["action"] == "none", probs))
        st, _, _ = check_hunt({"p_up": 60, "search_complete": False})
        res.append(("an unfinished search is never scored", st == "unfinished", st))
        prop = {"decision": "revise", "diagnosis": "synthetic",
                "ops": [{"op": "edit", "id": "P8", "text": "Spend time on the decisive question.",
                         "rationale": "r", "predicted_effect": "e", "revert_if": "x",
                         "evidence_names": ["2026-08-03/AAA", "2026-08-03/BBB", "2026-08-04/CCC"]}]}
        dump(tmp / "prop.json", prop)
        e0 = cmd_revise(tmp / "prop.json")
        res.append(("with nothing resolved the gate is closed and the proposal is rejected and logged",
                    e0["status"] == "rejected" and any("gate closed" in x for x in e0["reasons"])
                    and P["changes"].exists() and version_of(P["current"]) == "hp.v1", e0.get("reasons")))
        oc = cmd_resolve(prices=Prices(fixture), today="2026-08-11")
        r0 = oc["rows"].get("2026-08-03/evolving/AAA")
        want = (fixture["AAA"]["daily"]["2026-08-04"][0] / fixture["AAA"]["daily"]["2026-08-03"][1] - 1) * 100
        rb = oc["rows"].get("2026-08-03/evolving/BBB")
        want_b = (fixture["BBB"]["m5"]["2026-08-04"][str(13 * 60 - 5)] / fixture["BBB"]["daily"]["2026-08-03"][1] - 1) * 100
        res.append(("amc is priced close to next open, bmo close to 13:00 ET on the report day",
                    bool(r0 and abs(r0["move_pct"] - want) < 1e-2 and rb and abs(rb["move_pct"] - want_b) < 1e-2),
                    (r0 or {}).get("move_pct")))
        ev = cmd_evaluate(quiet=True)
        res.append(("32 resolved names over 4 days open the gate; the E-P comparison is filled",
                    ev["gate"]["resolved_names_on_current"] == 32 and ev["gate"]["open"] is True
                    and ev["stage_ep_same_names"]["n"] == 4, ev["gate"]))
        e1 = cmd_revise(tmp / "prop.json")
        res.append(("a valid proposal is applied as hp.v2 once the gate is open",
                    e1["status"] == "applied" and version_of(P["current"]) == "hp.v2"
                    and (P["versions"] / "hp.v2.md").exists()
                    and "Spend time on the decisive question." in P["current"].read_text(encoding="utf-8"),
                    e1.get("reasons")))
        ev2 = cmd_evaluate(quiet=True)
        res.append(("a new version starts with a closed gate", ev2["gate"]["open"] is False, ev2["gate"]))
        bad = {"decision": "revise", "diagnosis": "d",
               "ops": [{"op": "add", "title": "AAA", "text": "Always buy AAA.", "rationale": "r",
                        "predicted_effect": "e", "revert_if": "x", "evidence_names": ["2026-08-03/AAA"]}]}
        dump(tmp / "bad.json", bad)
        e2 = cmd_revise(tmp / "bad.json")
        res.append(("a proposal naming a ticker or citing too few names is rejected",
                    e2["status"] == "rejected" and any("ticker" in x for x in e2["reasons"])
                    and any("evidence" in x for x in e2["reasons"]), e2["reasons"]))
        res.append(("the control playbook is never written by revise",
                    sha(P["control"]) == sha(saved["control"]), ""))
    except Exception as e:  # pragma: no cover
        import traceback
        res.append(("selftest ran without an exception", False, traceback.format_exc()[-600:]))
    finally:
        try:
            _ctx.__exit__(None, None, None)
        except Exception:
            pass
        P.clear()
        P.update(saved)
        shutil.rmtree(tmp, ignore_errors=True)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("pick")
    s.add_argument("--run", required=True)
    s.add_argument("--source", help="directory holding sweep.json, universe.json and baselines/ (default <RUN>/edge-panel)")
    s.add_argument("--force", action="store_true")
    s = sub.add_parser("brief")
    s.add_argument("--run", required=True)
    s.add_argument("--ticker", required=True)
    s.add_argument("--arm", choices=["evolving", "control"], required=True)
    s = sub.add_parser("collect")
    s.add_argument("--run", required=True)
    s = sub.add_parser("resolve")
    s.add_argument("--offline", action="store_true")
    sub.add_parser("evaluate")
    s = sub.add_parser("revise")
    s.add_argument("--proposal", required=True)
    s.add_argument("--run")
    sub.add_parser("status")
    sub.add_parser("selftest")
    a = ap.parse_args()
    if a.cmd == "pick":
        cmd_pick(a.run, a.source, a.force)
    elif a.cmd == "brief":
        cmd_brief(a.run, a.ticker, a.arm)
    elif a.cmd == "collect":
        cmd_collect(a.run)
    elif a.cmd == "resolve":
        cmd_resolve(a.offline)
    elif a.cmd == "evaluate":
        cmd_evaluate()
    elif a.cmd == "revise":
        cmd_revise(a.proposal, a.run)
    elif a.cmd == "status":
        cmd_status()
    elif a.cmd == "selftest":
        res = selftest()
        for label, ok, detail in res:
            print(f"  {'ok' if ok else 'FAIL':5} {label}" + ("" if ok else f"  {detail}"))
        sys.exit(0 if all(ok for _, ok, _ in res) else 1)


if __name__ == "__main__":
    main()
