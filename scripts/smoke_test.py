#!/usr/bin/env python3
"""
End-to-end plumbing check, with fabricated data and no model calls.

The pipeline's stages hand files to each other unattended, hours apart, across
separate sessions. A shape mismatch between two stages surfaces at 17:37 on a
Tuesday otherwise. This runs the whole chain against synthetic data in a temp
directory in about a second.

It checks the plumbing, not the research: agent definitions parse, path
resolution works, every stage's file shape passes its own validator, the
synthesis maths is self-consistent, and the conviction gate actually fires.

    python3 scripts/smoke_test.py

Exit 0 = the chain is intact.
"""

import glob
import json
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
failures = []


def check(label, condition, detail=""):
    if condition:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label}" + (f" — {detail}" if detail else ""))
        failures.append(label)


def run(args, expect=0):
    p = subprocess.run([PY] + args, capture_output=True, text=True, cwd=REPO)
    ok = p.returncode == expect
    return ok, (p.stdout + p.stderr).strip()


PERSONAS = [
    "Fundamental / KPI Analyst",
    "Options & Positioning Strategist",
    "Behavioural / Sentiment Reader",
    "Outside-View Base-Rate Statistician",
    "Macro / Cross-Asset & Peer Read-through",
    "Red-Team Skeptic",
    "Insider, Communication & Alt-Data Forensics",
]


def verdicts(scores, confidence="Med"):
    out = []
    for name, s in zip(PERSONAS, scores):
        v = {
            "persona": name,
            "direction_score": s,
            "prob_up": max(1, min(99, 50 + s * 0.35)),
            "confidence": confidence,
            "expected_move_view": "±9%, roughly priced",
            "reversal_risk": 40,
            "key_drivers": ["driver a", "driver b"],
            "top_risk_to_my_call": "guidance reset",
            "key_sources": ["https://example.com/a", "https://example.com/b"],
        }
        if name == "Red-Team Skeptic":
            v["strongest_reversal_case"] = "priced-in beat into a 20% run-up"
        out.append(v)
    return out


ANCHORS = {
    "event_confirmed": True,
    "event_implied_move_pct": 9.2,
    "historical_move_mean_abs": 7.7,
    "historical_move_max_abs": 12.4,
    "historical_sample_size": 8,
}


def synth(tmp, scores, anchors=None, confidence="Med"):
    src = os.path.join(tmp, "in.json")
    with open(src, "w") as fh:
        json.dump({"ticker": "TEST", "anchors": anchors or ANCHORS,
                   "panel_verdicts": verdicts(scores, confidence)}, fh)
    p = subprocess.run([PY, "scripts/synthesize.py", src],
                       capture_output=True, text=True, cwd=REPO)
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout), ""


def main():
    print("Definitions")
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required: pip install pyyaml")

    for path in sorted(glob.glob(os.path.join(REPO, ".claude/agents/*.md")) +
                       glob.glob(os.path.join(REPO, ".claude/skills/*/SKILL.md"))):
        rel = os.path.relpath(path, REPO)
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            check(rel, False, "no frontmatter")
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except yaml.YAMLError as exc:
            check(rel, False, str(exc).splitlines()[0])
            continue
        expected = (os.path.basename(os.path.dirname(path)) if path.endswith("SKILL.md")
                    else os.path.basename(path)[:-3])
        check(rel, bool(fm.get("name") == expected and fm.get("description")),
              f"name/description mismatch (name={fm.get('name')!r})")

    check("config/pipeline.yaml parses",
          bool(yaml.safe_load(open(os.path.join(REPO, "config/pipeline.yaml")))))

    print("\nPath resolution")
    ok, out = run(["scripts/run_paths.py", "2026-08-10", "--json", "--no-create"])
    check("run_paths.py --json", ok, out)
    if ok:
        pp = json.loads(out)
        check("run_dir uses research/<Y>/<M>/<date>",
              pp["run_dir"].endswith("research/2026/08/2026-08-10"), pp["run_dir"])

    print("\nCalendar logic")
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    from get_earnings import next_trading_day, is_trading_day  # noqa: E402
    from datetime import date  # noqa: E402
    check("Friday rolls to Monday",
          next_trading_day(date(2026, 8, 7)) == date(2026, 8, 10))
    check("Christmas is not a trading day", not is_trading_day(date(2026, 12, 25)))
    check("Thanksgiving is not a trading day", not is_trading_day(date(2026, 11, 26)))
    check("day before a holiday rolls past it",
          next_trading_day(date(2026, 12, 24)) == date(2026, 12, 28))

    with tempfile.TemporaryDirectory() as tmp:
        print("\nSynthesis maths")

        s, err = synth(tmp, [62, 55, 70, 48, 58, 40, 66], confidence="High")
        check("aligned bullish panel -> Lean Up", s and s["call"] == "Lean Up",
              err or (s and s["call"]))
        if s:
            check("signed move is a fraction of expected move",
                  0 < s["signed_estimated_move"] < 0.85 * s["unsigned_expected_move"],
                  f"{s['signed_estimated_move']} vs {s['unsigned_expected_move']}")
            check("Up call carries a positive signed move", s["signed_estimated_move"] > 0)
            check("band is right-skewed around the expected move",
                  s["move_band_low_high"][1] - s["unsigned_expected_move"]
                  > s["unsigned_expected_move"] - s["move_band_low_high"][0])

        s, _ = synth(tmp, [-70, -62, -58, -66, -68, -64, -60], confidence="High")
        check("aligned bearish panel -> Strong Down", s and s["call"] == "Strong Down",
              s and s["call"])
        check("Down call carries a negative signed move",
              s and s["signed_estimated_move"] < 0)

        s, _ = synth(tmp, [90, -85, 75, -70, 60, -80, 40])
        check("split panel -> gate fires", s and s["conviction_gate_applied"] is True)
        check("gated call is Neutral / No Edge", s and s["call"] == "Neutral / No Edge")
        check("gated call has no signed move", s and s["signed_estimated_move"] is None)
        check("split panel is labelled split", s and s["panel_alignment"] == "split")

        s, _ = synth(tmp, [55, 50, 60, 45, 52, 48, 58],
                     anchors={"event_confirmed": False})
        check("unconfirmed timing -> gate fires", s and s["conviction_gate_applied"])

        s, _ = synth(tmp, [55, 50, 60, 45, 52, 48, 58],
                     anchors={"event_confirmed": True})
        check("no move anchor -> gate fires", s and s["conviction_gate_applied"])

        hi, _ = synth(tmp, [45, 42, 48, 40, 44, 41, 46], confidence="High")
        lo, _ = synth(tmp, [45, 42, 48, 40, 44, 41, 46], confidence="Low")
        check("Low confidence shrinks the signed move versus High",
              hi and lo and abs(lo["signed_estimated_move"]) < abs(hi["signed_estimated_move"]),
              f"low={lo and lo['signed_estimated_move']} high={hi and hi['signed_estimated_move']}")
        check("a weak-but-coherent lean survives as a call",
              lo and lo["call"] == "Lean Up", lo and lo["call"])

        print("\nStage file contracts")

        shortlist = {
            "schema_version": 1, "run_date": "2026-08-10",
            "window_covered": "after close 10 Aug through before open 11 Aug",
            "triage_mode": "scouted", "shortlist": [{
                "ticker": "TEST", "company": "Test Corp", "session": "amc",
                "event_date": "2026-08-10", "change_expectation": 78,
                "ai_edge": 64, "priority_score": 71.7,
                "selection_rationale": "binary guidance event with rich public data",
            }],
        }
        p1 = os.path.join(tmp, "01-shortlist.json")
        json.dump(shortlist, open(p1, "w"))
        ok, out = run(["scripts/validate_stage.py", "shortlist", p1])
        check("valid shortlist passes", ok, out)

        shortlist["shortlist"][0]["ai_edge"] = 140
        json.dump(shortlist, open(p1, "w"))
        ok, out = run(["scripts/validate_stage.py", "shortlist", p1], expect=1)
        check("out-of-range ai_edge is rejected", ok, out)

        good, _ = synth(tmp, [62, 55, 70, 48, 58, 40, 66], confidence="High")
        panel = {"ticker": "TEST", "company": "Test Corp",
                 "panel_verdicts": verdicts([62, 55, 70, 48, 58, 40, 66], "High"),
                 "synthesis": good}
        p3 = os.path.join(tmp, "TEST.json")
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3])
        check("synthesize.py output passes the panel validator", ok, out)

        panel["synthesis"] = dict(good, signed_estimated_move=-4.0)
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3], expect=1)
        check("Up call with a negative move is rejected", ok, out)

        panel["synthesis"] = dict(good, signed_estimated_move=good["unsigned_expected_move"])
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3], expect=1)
        check("claiming the full expected move is rejected", ok, out)

        panel["synthesis"] = good
        panel["panel_verdicts"] = panel["panel_verdicts"][:6]
        json.dump(panel, open(p3, "w"))
        ok, out = run(["scripts/validate_stage.py", "panel", p3], expect=1)
        check("a missing panel seat is flagged", ok, out)

        advice = {"schema_version": 1, "run_date": "2026-08-10", "ranked_names": [
            {"ticker": "TEST", "panelled": True, "call": "Lean Up",
             "signed_estimated_move": 4.2, "certainty_tier": "Med"}]}
        p4 = os.path.join(tmp, "04-advice.json")
        json.dump(advice, open(p4, "w"))
        ok, out = run(["scripts/validate_stage.py", "advice", p4])
        check("valid advice passes", ok, out)

        # A day where stage 2 died has nothing to rank, but must still publish a
        # deliverable rather than fabricate rows to satisfy the validator.
        blocked = {"schema_version": 1, "run_date": "2026-08-10", "status": "blocked",
                   "status_reason": "stage 2 published no dossiers",
                   "ranked_names": []}
        p4b = os.path.join(tmp, "04-advice-blocked.json")
        json.dump(blocked, open(p4b, "w"))
        ok, out = run(["scripts/validate_stage.py", "advice", p4b])
        check("a blocked day can publish an empty advice note", ok, out)

        json.dump({k: v for k, v in blocked.items() if k != "status_reason"},
                  open(p4b, "w"))
        ok, out = run(["scripts/validate_stage.py", "advice", p4b], expect=1)
        check("a blocked day without a reason is rejected", ok, out)

        json.dump({"schema_version": 1, "run_date": "2026-08-10", "ranked_names": []},
                  open(p4b, "w"))
        ok, out = run(["scripts/validate_stage.py", "advice", p4b], expect=1)
        check("an empty advice note still needs a status", ok, out)

    print("\nRun-log heartbeat")
    with tempfile.TemporaryDirectory() as tmp:
        log = os.path.join(tmp, "_run-log.md")
        sys.path.insert(0, os.path.join(REPO, "scripts"))
        from run_log import append_section

        append_section(log, "2026-08-10", "Stage 2 — batch 1 — STARTED",
                       ["Tickers: AAA, BBB"])
        first = open(log, encoding="utf-8").read()
        check("heartbeat creates the log with its date header",
              first.startswith("# Run log — 2026-08-10"), first[:60])
        check("heartbeat records the plan", "Tickers: AAA, BBB" in first, first)

        append_section(log, "2026-08-10", "Stage 2 — batch 1 — FINISHED",
                       ["Researched: AAA"])
        second = open(log, encoding="utf-8").read()
        check("appending never drops the earlier section",
              "STARTED" in second and "FINISHED" in second, second)
        check("only one date header after two appends",
              second.count("# Run log —") == 1, second)

    print("\nConsolidated predictions table")
    with tempfile.TemporaryDirectory() as tmp:
        # A synthetic run day whose files are spread across four stages, which is
        # exactly the join build_predictions.py has to get right.
        day_dir = os.path.join(tmp, "2026", "08", "2026-08-10")
        os.makedirs(os.path.join(day_dir, "02-dossiers"))
        os.makedirs(os.path.join(day_dir, "03-panel"))
        good, _ = synth(tmp, [62, 55, 70, 48, 58, 40, 66], confidence="High")

        json.dump({"run_date": "2026-08-10", "shortlist": [
            {"ticker": "TEST", "session": "amc", "change_expectation": 78, "ai_edge": 64}]},
            open(os.path.join(day_dir, "01-shortlist.json"), "w"))
        json.dump({"ticker": "TEST", "company": "Test Corp", "session": "amc",
                   "event_date": "2026-08-10", "preliminary_direction_score": 25,
                   "evidence_completeness": 82, "event_implied_move_pct": 9.2},
                  open(os.path.join(day_dir, "02-dossiers", "TEST.json"), "w"))
        json.dump({"ticker": "TEST", "synthesis": good},
                  open(os.path.join(day_dir, "03-panel", "TEST.json"), "w"))
        json.dump({"run_date": "2026-08-10", "ranked_names": [
            {"ticker": "TEST", "panelled": True, "call": "Lean Up"}]},
            open(os.path.join(day_dir, "04-advice.json"), "w"))
        json.dump({"run_date": "2026-08-10", "names": [
            {"ticker": "TEST", "actual_move": 6.8, "direction_hit": True,
             "magnitude_error": 2.6, "band_hit": True}]},
            open(os.path.join(day_dir, "05-outcome.json"), "w"))

        sys.path.insert(0, os.path.join(REPO, "scripts"))
        import build_predictions  # noqa: E402
        build_predictions.RESEARCH = tmp
        pred = build_predictions.collect()

        check("one row per prediction", len(pred) == 1, f"got {len(pred)}")
        if pred:
            r = pred[0]
            check("pulls the call from the advice file", r["call"] == "Lean Up", r["call"])
            check("pulls triage scores from the shortlist",
                  r["change_expectation"] == 78 and r["ai_edge"] == 64)
            check("pulls the preliminary read from the dossier",
                  r["preliminary_direction_score"] == 25)
            check("pulls synthesis numbers from the panel file",
                  r["disparity"] == good["disparity"]
                  and r["signed_estimated_move"] == good["signed_estimated_move"])
            check("pulls the realised move from the outcome file",
                  r["actual_move"] == 6.8 and r["direction_hit"] is True)
            check("flattens the move band into two columns",
                  r["band_low"] == good["move_band_low_high"][0]
                  and r["band_high"] == good["move_band_low_high"][1])
        s = build_predictions.summarise(pred)
        check("summary counts a scored panelled call",
              s["predictions_scored"] == 1 and s["panelled_direction_hit_rate"] == 1.0, str(s))

        # An unscored day must read as pending, not as a miss.
        os.remove(os.path.join(day_dir, "05-outcome.json"))
        pend = build_predictions.collect()
        check("unscored prediction reads as pending",
              pend[0]["outcome_status"] == "pending" and pend[0]["direction_hit"] is None)
        check("pending rows are excluded from the hit rate",
              build_predictions.summarise(pend)["panelled_direction_hit_rate"] is None)

    print("\nPublishing under a moving remote")
    # Reproduces the failure that lost a whole stage-2 batch: the remote branch
    # moves while a stage is running, and the stage still has to land its work.
    with tempfile.TemporaryDirectory() as tmp:
        def git(cwd, *args, check=True):
            return subprocess.run(["git", "-C", cwd, *args],
                                  capture_output=True, text=True, check=check)

        bare = os.path.join(tmp, "origin.git")
        stage = os.path.join(tmp, "stage")     # the Routine session
        other = os.path.join(tmp, "other")     # someone else pushing meanwhile
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", bare], check=True)

        subprocess.run(["git", "clone", "-q", bare, stage], check=True)
        os.makedirs(os.path.join(stage, "scripts"))
        os.makedirs(os.path.join(stage, "research"))
        for f in ("INDEX.md", "LEDGER.md"):
            open(os.path.join(stage, f), "w").write("seed\n")
        subprocess.run(["cp", os.path.join(REPO, "scripts", "publish.sh"),
                        os.path.join(stage, "scripts")], check=True)
        git(stage, "config", "user.email", "t@example.com")
        git(stage, "config", "user.name", "T")
        git(stage, "add", "-A")
        git(stage, "commit", "-qm", "seed")
        git(stage, "push", "-q", "origin", "main")

        # Someone else pushes to main, touching a tracked file the stage also writes.
        subprocess.run(["git", "clone", "-q", bare, other], check=True)
        git(other, "config", "user.email", "o@example.com")
        git(other, "config", "user.name", "O")
        open(os.path.join(other, "INDEX.md"), "w").write("rebuilt by someone else\n")
        open(os.path.join(other, "OTHER.md"), "w").write("their work\n")
        git(other, "add", "-A")
        git(other, "commit", "-qm", "concurrent change")
        git(other, "push", "-q", "origin", "main")

        # The stage finishes: it wrote research output and regenerated INDEX.md.
        os.makedirs(os.path.join(stage, "research", "2026", "08", "2026-08-10"))
        open(os.path.join(stage, "research", "2026", "08", "2026-08-10",
                          "02-dossiers.md"), "w").write("expensive research\n")
        open(os.path.join(stage, "INDEX.md"), "w").write("rebuilt by the stage\n")

        p = subprocess.run(["bash", os.path.join(stage, "scripts", "publish.sh"),
                            "stage 2 batch 1: dossiers"],
                           capture_output=True, text=True)
        check("publish.sh succeeds when the remote moved mid-run",
              p.returncode == 0, (p.stdout + p.stderr).strip()[-300:])

        files = git(stage, "ls-tree", "-r", "--name-only", "origin/main").stdout.split()
        check("the stage's research reached the remote",
              "research/2026/08/2026-08-10/02-dossiers.md" in files, str(files))
        check("the concurrent change was not clobbered",
              "OTHER.md" in files, str(files))

    print("\nOrder placement (researcher_us/scripts/alpaca_trade.py, no network, no orders)")
    # The real module lives in researcher_us/scripts; scripts/alpaca_trade.py is a forwarding
    # shim for the Routine prompt's frozen path and is not importable as the module.
    sys.path.insert(0, os.path.join(REPO, "researcher_us", "scripts"))
    import alpaca_trade as at                                     # noqa: E402

    ex = at.execution_config(yaml.safe_load(
        open(os.path.join(REPO, "config/pipeline.yaml"), encoding="utf-8")))
    # This asserted `enabled is False` until 2026-09-10, when the operator turned
    # the switch on deliberately for the paper account and the check started failing
    # on every run. A permanently red check is worse than no check: it trains the
    # next session to skip the output. What the switch must still be is an explicit
    # bool -- a None or a stray string would sail through `if ex["enabled"]` in
    # guard() -- and the three gates that actually stop an accident are tested
    # separately below and still hold: --submit is required, a disabled config
    # blocks --submit, and a live endpoint needs its own flag.
    check("the execution switch is an explicit bool",
          isinstance(ex.get("enabled"), bool),
          f"enabled={ex.get('enabled')!r} — guard() treats anything truthy as on")
    if ex.get("enabled"):
        print("        note: execution is ON. Orders go out on `--submit`; the "
              "endpoint gate still requires paper unless overridden.")
    check("the conviction floor is inherited from stage E",
          ex["benchmark"]["min_conviction"] == 3.0,
          str(ex["benchmark"]["min_conviction"]))

    # -- the price the budget is divided by (added 2026-09-10)
    #
    # Sizing used to divide by the sealed baseline spot, which is captured when the
    # run starts: on the first live run that was 14:08 UTC against orders at 17:59,
    # so a 20.0%-of-equity cap produced a 20.3% position. It now divides by a live
    # Alpaca price. These checks cover the branch that got it wrong first time --
    # a stale trade next to a 29%-wide quote, where the mid is not a price.
    check("a two-sided quote gives a mid and a spread",
          (at.quote_snapshot({"bp": 10.0, "ap": 10.1}) or {}).get("mid") == 10.05)
    check("a one-sided or crossed quote is not a price",
          at.quote_snapshot({"bp": 0, "ap": 10.1}) is None
          and at.quote_snapshot({"bp": 11.0, "ap": 10.0}) is None
          and at.quote_snapshot(None) is None)
    check("a nanosecond timestamp parses",
          at._age_seconds("2026-09-10T18:00:00.123456789Z") is not None
          and at._age_seconds("not-a-date") is None)

    now = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z")

    class _FakeApi:
        usable = True
        def __init__(self, trades, quotes):
            self._t, self._q = trades, quotes
        def latest_trades(self, syms):
            return {k: v for k, v in self._t.items() if k in syms}, None
        def latest_quotes(self, syms):
            return {k: v for k, v in self._q.items() if k in syms}, None

    refs, _ = at.reference_prices(_FakeApi(
        trades={"FRESH": {"p": 100.0, "t": now},
                "STALE": {"p": 63.96, "t": "2026-01-01T00:00:00Z"},
                "OLDTIGHT": {"p": 20.0, "t": "2026-01-01T00:00:00Z"}},
        quotes={"FRESH": {"bp": 99.0, "ap": 99.1},
                "STALE": {"bp": 54.24, "ap": 72.79},      # 29% wide, the FEIM case
                "OLDTIGHT": {"bp": 21.0, "ap": 21.02},
                "QUOTEONLY": {"bp": 5.0, "ap": 5.01}}),
        ["FRESH", "STALE", "OLDTIGHT", "QUOTEONLY", "NOTHING"])
    check("a fresh trade wins over the quote",
          refs["FRESH"]["price"] == 100.0, str(refs.get("FRESH")))
    check("a stale trade beats a 29%-wide mid",
          refs["STALE"]["price"] == 63.96 and "stale" in refs["STALE"]["source"],
          str(refs.get("STALE")))
    check("a tight mid beats a stale trade",
          refs["OLDTIGHT"]["price"] == 21.01, str(refs.get("OLDTIGHT")))
    check("a quote with no trade is still usable",
          refs["QUOTEONLY"]["price"] == 5.005, str(refs.get("QUOTEONLY")))
    check("a name with neither is absent, so the caller falls back and says so",
          "NOTHING" not in refs, str(list(refs)))
    # Note Alpaca(key="") is NOT credential-less: the constructor reads the
    # environment when an argument is falsy, so this stubs `usable` directly.
    class _NoCreds:
        usable = False
    _none, _why = at.reference_prices(_NoCreds(), ["X"])
    check("no credentials means no live prices and no guessing",
          _none == {} and _why == "no credentials", f"{_none} {_why!r}")
    check("no tickers is not an error",
          at.reference_prices(_FakeApi({}, {}), [])[0] == {})

    _sized, _ = at.size([{"ticker": "X", "spot": 100.0, "ref_price": 110.0,
                          "ref_price_source": "alpaca last trade",
                          "dollar_volume_usd": 10**9}], 10_000.0,
                        {"gross_exposure_pct_of_equity": 100,
                         "max_position_pct_of_equity": 20})
    check("sizing divides by the live price, not the sealed spot",
          _sized[0]["qty"] == 18 and _sized[0]["price_used_usd"] == 110.0,
          str(_sized[0]["qty"]))
    _fb, _ = at.size([{"ticker": "X", "spot": 100.0, "dollar_volume_usd": 10**9}],
                     10_000.0, {"gross_exposure_pct_of_equity": 100,
                                "max_position_pct_of_equity": 20})
    check("with no live price it falls back to the spot and records that",
          _fb[0]["qty"] == 20 and _fb[0]["price_source"] == "sealed baseline spot",
          str(_fb[0]["price_source"]))

    scores = {"ranking_key": "impact_sum", "ranking": [
        {"ticker": "BIGL", "rankable": True, "impact_sum": 9.0},     # long, liquid
        {"ticker": "BIGS", "rankable": True, "impact_sum": -6.0},    # short, liquid
        {"ticker": "TINY", "rankable": True, "impact_sum": 12.0},    # illiquid
        {"ticker": "WEAK", "rankable": True, "impact_sum": 2.9},     # under the floor
        {"ticker": "NOEV", "rankable": False, "impact_sum": 8.0,
         "not_rankable_because": "event unconfirmed"}]}
    base = {t: {"ticker": t, "event_date": "2026-09-09", "session": s,
                "as_of_utc": "2026-09-09T14:00:00+00:00",
                "tape": {"spot": 50.0, "avg_volume_20d": v}}
            for t, s, v in [("BIGL", "amc", 1_000_000), ("BIGS", "bmo", 1_000_000),
                            ("TINY", "amc", 1_000), ("WEAK", "amc", 1_000_000),
                            ("NOEV", "amc", 1_000_000)]}
    taken, rejected = at.select(scores, base, ex["benchmark"])
    reasons = {r["ticker"]: r["reason"] for r in rejected}
    check("the benchmark takes only the liquid names above the floor",
          [c["ticker"] for c in taken] == ["BIGL", "BIGS"],
          str([c["ticker"] for c in taken]))
    check("a name under the conviction floor is refused",
          "conviction floor" in reasons.get("WEAK", ""), str(reasons))
    check("an untradeably thin name is refused on capacity",
          "turnover" in reasons.get("TINY", ""), str(reasons))
    check("an unconfirmed event is refused", "not rankable" in reasons.get("NOEV", ""),
          str(reasons))
    check("the sign sets the side",
          [c["side"] for c in taken] == ["buy", "sell"], str(taken))

    eq_cap = 100_000 * float(ex["sizing"]["max_position_pct_of_equity"]) / 100
    gross_budget = 100_000 * float(ex["sizing"]["gross_exposure_pct_of_equity"]) / 100
    sized, _ = at.size(taken, 100_000.0, ex["sizing"])
    check("no position exceeds max_position_pct_of_equity",
          all(s["notional_usd"] <= eq_cap + 1e-6 for s in sized),
          str([s["notional_usd"] for s in sized]))
    check("no position exceeds max_position_pct_of_adv",
          all(s["cap_capacity_usd"] is None
              or s["notional_usd"] <= s["cap_capacity_usd"] + 1e-6
              for s in sized),
          str([(s["notional_usd"], s["cap_capacity_usd"]) for s in sized]))
    check("the book never exceeds the gross budget",
          sum(s["notional_usd"] for s in sized) <= gross_budget + 1e-6)
    check("share counts are whole", all(float(s["qty"]).is_integer() for s in sized))

    # Equal weight, and the leftover of a capped name redistributed rather than lost.
    wide = [{"ticker": t, "key": "impact_sum", "value": v, "conviction": abs(v),
             "side": "buy" if v > 0 else "sell", "spot": 10.0,
             "dollar_volume_usd": dv, "event_date": "2026-09-09", "session": "amc"}
            for t, v, dv in [("A", 9.0, 1e9), ("B", -8.0, 1e9), ("C", 7.0, 1e9),
                             ("D", 6.0, 1e9), ("E", 5.0, 1e9), ("F", 4.0, 1e9)]]
    six, _ = at.size(wide, 100_000.0, ex["sizing"])
    notionals = [s["notional_usd"] for s in six]
    check("six equal weights, no cap binding",
          max(notionals) - min(notionals) <= 10.0 and
          abs(sum(notionals) - gross_budget) < 100, str(notionals))
    check("the biggest score gets no more money than the smallest",
          abs(six[0]["notional_usd"] - six[-1]["notional_usd"]) <= 10.0,
          f"{six[0]['ticker']} {six[0]['notional_usd']} vs "
          f"{six[-1]['ticker']} {six[-1]['notional_usd']}")

    thin = [dict(w) for w in wide]
    thin[0]["dollar_volume_usd"] = 300_000            # 1% of ADV = $3,000
    redis, _ = at.size(thin, 100_000.0, ex["sizing"])
    capped = [s for s in redis if s["ticker"] == "A"][0]
    others = [s["notional_usd"] for s in redis if s["ticker"] != "A"]
    check("a capacity-capped name is cut to its cap",
          capped["notional_usd"] <= 3000 + 1e-6 and
          capped["binding_cap"] == "capacity", str(capped["notional_usd"]))
    check("its leftover is redistributed, not lost",
          abs(sum(others) + capped["notional_usd"] - gross_budget) < 100 and
          max(others) - min(others) <= 10.0, str(others))

    # How few names it takes to under-deploy moves with the cap: five at 20%, three at
    # 33%. Two names is under-deployed at any cap the config can sanely carry, so the
    # check reads the shipped numbers rather than restating one of them.
    few, _ = at.size(wide[:2], 100_000.0, ex["sizing"])
    check("a book smaller than the cap allows under-deploys on purpose",
          all(abs(s["notional_usd"] - eq_cap) < 10.0 for s in few)
          and sum(s["notional_usd"] for s in few) < gross_budget - 1.0,
          str([s["notional_usd"] for s in few]))
    check("the per-name cap is the binding one there",
          all(s["binding_cap"] == "per-name %" for s in few),
          str([s["binding_cap"] for s in few]))

    # The flatten and the exit mode are one setting in two keys: a non-uniform mode
    # with the flatten on sells every auction leg at market before its auction, and
    # exit_mode() refuses that pairing outright. Assert the pairing, not either value
    # -- both have been changed by the operator once and will be again.
    check("the flatten and the exit mode agree",
          (ex["orders"].get("flatten_before_entry") is True)
          == (at.exit_mode(ex) == "uniform"),
          f"flatten={ex['orders'].get('flatten_before_entry')} "
          f"exit_mode={at.exit_mode(ex)}")

    # The two trading steps live in two hand-maintained files and drift silently.
    skill = open(os.path.join(REPO, ".claude/skills/earnings-edge-hunt/SKILL.md"),
                 encoding="utf-8").read()
    rprompt = open(os.path.join(REPO, "researcher_us/routine-prompts/edge-hunt.md"),
                   encoding="utf-8").read()
    for label, text in (("the skill", skill), ("the stage E Routine prompt", rprompt)):
        # Either shape is a sell before the hunt, and which one is right depends on
        # orders.exit_mode: the flatten is wrong whenever a position wants an auction.
        check(f"{label} sells before the hunt",
              "flatten --submit" in text or "close --scan" in text)
        check(f"{label} checks that the sells filled", "verify --scan" in text)
        check(f"{label} buys with --no-flatten", "--no-flatten" in text)
        check(f"{label} gates both steps on execution.enabled",
              text.count("execution.enabled") >= 2 or text.count("enabled` is true") >= 2
              or text.count("execution.enabled` is `true") >= 1)
    check("a flatten without --submit closes nothing",
          at.flatten(at.Alpaca(key="", secret=""), False,
                     "dry run")["submitted"] is False)

    days = at.trading_days_offline("2026-09-09")
    check("an amc print enters on the event date and exits the next session",
          at.window(days, "2026-09-09", "amc") == ("2026-09-09", "2026-09-10"),
          str(at.window(days, "2026-09-09", "amc")))
    check("a bmo print enters the session before and exits on the event date",
          at.window(days, "2026-09-09", "bmo") == ("2026-09-08", "2026-09-09"),
          str(at.window(days, "2026-09-09", "bmo")))
    check("a Monday bmo print enters on the Friday",
          at.window(at.trading_days_offline("2026-09-14"), "2026-09-14", "bmo")
          == ("2026-09-11", "2026-09-14"),
          str(at.window(at.trading_days_offline("2026-09-14"), "2026-09-14", "bmo")))

    moc_body = at.order_body("BIGL", 10, "buy", ex, moc=True)
    mkt_body = at.order_body("BIGL", 10, "buy", ex, moc=False)
    check("market-on-close is type market, tif cls",
          (moc_body["type"], moc_body["time_in_force"]) == ("market", "cls"),
          str(moc_body))
    check("a plain market entry is type market, tif day",
          (mkt_body["type"], mkt_body["time_in_force"]) == ("market", "day"),
          str(mkt_body))
    check("the shipped entry is an immediate market order",
          ex["orders"].get("entry") == "market", str(ex["orders"].get("entry")))
    check("nothing is sent to extended hours",
          moc_body["extended_hours"] is False and mkt_body["extended_hours"] is False)
    check("the exit inverts the entry side",
          at.order_body("BIGL", 10, "sell" if mkt_body["side"] == "buy" else "buy",
                        ex)["side"] == "sell")
    blocked = at.guard(at.Alpaca(key="", secret=""), ex, submit=False, live_ok=False)
    check("a run without --submit is blocked before any order", bool(blocked), str(blocked))
    check("a disabled config blocks --submit",
          bool(at.guard(at.Alpaca(key="k", secret="s"), {**ex, "enabled": False},
                        submit=True, live_ok=False)))
    check("a live endpoint is blocked without the explicit flag",
          "paper" in (at.guard(at.Alpaca(base="https://api.alpaca.markets",
                                         key="k", secret="s"),
                               {**ex, "enabled": True}, submit=True, live_ok=False) or ""))

    # Per-session exits. Off in the shipped config, so the first check is that it is
    # off: turning it on also needs flatten_before_entry off and a second run a day,
    # and the two would silently cancel each other out.
    # A non-uniform mode is REFUSED while the flatten is on, so every probe below
    # sets both together -- which is also the only combination that is coherent.
    def _mode(m, flatten=False):
        return {**ex, "orders": {**ex["orders"], "exit_mode": m,
                                 "flatten_before_entry": flatten}}

    check("the shipped config names a known exit mode",
          at.exit_mode(ex) in at.EXIT_MODES, at.exit_mode(ex))
    # WHERE the exit is aimed is the mode's decision; WHICH INSTRUMENT gets it there
    # is orders.auction_orders. They were the same thing until 2026-09-18, when ten
    # auction legs had produced one full fill and the account turned out not to be on
    # the Elite Smart Router that `opg`/`cls` require. So the placement checks below
    # are the ones that must hold in every configuration; the instrument checks are
    # conditional on auction orders being available.
    def _auc(m, on):
        d = _mode(m)
        return {**d, "orders": {**d["orders"], "auction_orders": on}}

    check("uniform aims both sessions at the same exit",
          at.exit_placement("amc", _mode("uniform"))
          == at.exit_placement("bmo", _mode("uniform")) == "close")
    # bmo_close is the one reachable from stage E's single Routine: the amc leg is
    # the plain market sell the flatten already did, the bmo leg goes to the close.
    check("bmo_close sells amc at market and aims bmo at the close",
          (at.exit_placement("amc", _mode("bmo_close")) == "market"
           and at.exit_placement("bmo", _mode("bmo_close")) == "close"),
          f'amc={at.exit_placement("amc", _mode("bmo_close"))} '
          f'bmo={at.exit_placement("bmo", _mode("bmo_close"))}')
    check("auction_split aims amc at the open and bmo at the close",
          (at.exit_placement("amc", _mode("auction_split")) == "open"
           and at.exit_placement("bmo", _mode("auction_split")) == "close"))
    # amc_open is auction_split with the bmo leg brought forward to the run itself,
    # so the position is certainly gone before the same afternoon buys the next book.
    check("amc_open aims amc at the open and sells bmo at market",
          (at.exit_placement("amc", _mode("amc_open")) == "open"
           and at.exit_placement("bmo", _mode("amc_open")) == "market"),
          f'amc={at.exit_placement("amc", _mode("amc_open"))} '
          f'bmo={at.exit_placement("bmo", _mode("amc_open"))}')
    check("an unknown session falls back to the closing exit",
          at.exit_placement(None, _mode("auction_split")) == "close")

    check("with auction orders ON the opening modes use opg and the closing cls",
          all(at.exit_tif_for("amc", _auc(m, True)) == "opg"
              for m in ("auction_split", "amc_open"))
          and at.exit_tif_for("bmo", _auc("auction_split", True)) == "cls")
    # The instrument that replaced them. A plain DAY order submitted in the
    # pre-market is accepted while the market is closed and routed at the next open,
    # so the amc leg still leaves at the open -- it just leaves.
    check("with auction orders OFF every exit is a plain day order",
          all(at.exit_tif_for(sess, _auc(m, False)) == "day"
              for m in at.EXIT_MODES for sess in ("amc", "bmo")),
          str({m: {s: at.exit_tif_for(s, _auc(m, False)) for s in ("amc", "bmo")}
               for m in at.EXIT_MODES}))
    check("the shipped config has auction orders off",
          at.auction_orders(ex) is False, str(at.auction_orders(ex)))
    # The second exit Routine exists to place the exit that must go in BEFORE the
    # open, whichever instrument does it. Its pasted guard says `--require-exit-tif
    # opg`, a session cannot edit a Routine, and the guard failing shut would mean a
    # correct-looking no-op every morning while the amc legs went unsold -- the exact
    # failure it was written to replace. So it matches on placement.
    # WHICH RUN SELLS A LEG. `close` takes every leg due today and two runs a day
    # call it. On 2026-09-18 the 06:05 ET Routine sent TRT's bmo exit as a market DAY
    # order, which Alpaca queues for the OPEN, although `amc_open` puts bmo at market
    # on stage E's 13:05 ET run -- and bmo measured worst at the open of the three.
    check("a market-placement leg is left to the run inside the session",
          at.defer_to_session_run("market", overdue=False, session_open=False))
    check("an open-placement leg is exactly what the pre-market run is for",
          not at.defer_to_session_run("open", overdue=False, session_open=False))
    check("an overdue leg is never deferred",
          not at.defer_to_session_run("market", overdue=True, session_open=False))
    check("nothing is deferred while the session is open",
          not at.defer_to_session_run("market", overdue=False, session_open=True))
    check("an unreadable clock never becomes a reason a leg goes unsold",
          not at.defer_to_session_run("market", overdue=False, session_open=None))

    check("both opening modes are reachable by the opg guard, auction orders or not",
          all(at.exit_placement("amc", _auc(m, on)) == "open"
              for m in ("auction_split", "amc_open") for on in (True, False)))
    check("exit_by_session: true still means auction_split",
          at.exit_mode({**ex, "orders": {**{k: v for k, v in ex["orders"].items()
                                            if k != "exit_mode"},
                                         "flatten_before_entry": False,
                                         "exit_by_session": True}})
          == "auction_split")
    # The contradiction that was documented in three places and enforced in none:
    # the flatten sells the amc names at market hours before the auction the mode
    # exists to reach, so the configured exit could never happen and nothing said so.
    for _m in ("bmo_close", "auction_split", "amc_open"):
        try:
            at.exit_mode(_mode(_m, flatten=True))
            check(f"{_m} with the flatten still on is refused", False,
                  "it was accepted")
        except SystemExit as e:
            check(f"{_m} with the flatten still on is refused",
                  "flatten_before_entry" in str(e), str(e)[:60])
    try:
        at.exit_mode(_mode("whatever"))
        check("an unknown exit_mode is refused", False, "it was accepted")
    except SystemExit as e:
        check("an unknown exit_mode is refused", "exit_mode" in str(e), str(e)[:80])
    check("an explicit tif overrides the moc flag",
          at.order_body("X", 1, "sell", ex, moc=True, tif="opg")["time_in_force"]
          == "opg")
    check("an opg order is still a plain market order",
          at.order_body("X", 1, "sell", ex, tif="opg")["type"] == "market")

    # The safety property: a new book is never entered on top of an unsold one. With
    # flatten_before_entry on, the flatten guarantees it. With the per-session exit
    # that flatten is off, so the guarantee has to come from this check instead.
    import json as _json
    import tempfile as _tf
    from pathlib import Path as _Path
    _tmp = _Path(_tf.mkdtemp())
    _run = _tmp / "research" / "2026" / "09" / "2026-09-08" / "edge"
    _run.mkdir(parents=True)
    (_run / "alpaca-orders.json").write_text(_json.dumps({
        "entries": [
            {"symbol": "AAA", "side": "buy", "qty": 10, "exit_date": "2026-09-09",
             "submitted": True, "client_order_id": "edge-2026-09-08-AAA-entry"},
            {"symbol": "BBB", "side": "sell", "qty": 20, "exit_date": "2026-09-09",
             "submitted": True, "client_order_id": "edge-2026-09-08-BBB-entry"},
            {"symbol": "CCC", "side": "buy", "qty": 5, "exit_date": "2026-09-10",
             "submitted": True, "client_order_id": "edge-2026-09-08-CCC-entry"},
            {"symbol": "DDD", "side": "buy", "qty": 5, "exit_date": "2026-09-09",
             "submitted": False, "client_order_id": "edge-2026-09-08-DDD-entry"},
        ],
        "exits": [{"closes": "edge-2026-09-08-BBB-entry", "submitted": True}],
        "log": []}))
    _repo = at.REPO
    at.REPO = _tmp
    try:
        _late = [g["symbol"] for g in at.overdue_legs("2026-09-10")]
        check("an unsold position past its exit date is flagged overdue",
              _late == ["AAA"], f"flagged {_late}")
        check("a position whose exit was already sent is not flagged",
              "BBB" not in _late)
        check("a position due today is not flagged overdue",
              "CCC" not in _late)
        check("an entry that never filled is not flagged as an open position",
              "DDD" not in _late)
        check("nothing is overdue on its own exit date",
              at.overdue_legs("2026-09-09") == [])
        # `flatten` closes positions without writing a per-leg exit, so the ledger on
        # its own calls a flattened position unsold forever. Only what the account
        # actually holds counts.
        check("a flattened position is not flagged once the account no longer holds it",
              at.overdue_legs("2026-09-10", held=set()) == [])
        check("it is still flagged while the account does hold it",
              [g["symbol"] for g in at.overdue_legs("2026-09-10", held={"AAA"})]
              == ["AAA"])
    finally:
        at.REPO = _repo

    print("\nOne issuer, one event (researcher_us/scripts/share_class.py, edge_score.py)")
    sys.path.insert(0, os.path.join(REPO, "researcher_us", "scripts"))
    import share_class as sc                                       # noqa: E402
    check("a dotted class suffix resolves to its issuer",
          sc.base_of("LEN.B") == "LEN" and sc.base_of("GEF-B") == "GEF")
    check("an ordinary ticker is not a share class",
          sc.base_of("LEN") is None and sc.base_of("ALMU") is None)
    day = [{"ticker": "LEN", "event_date": "2026-09-16"},
           {"ticker": "LEN.B", "event_date": "2026-09-16"},
           {"ticker": "BRK.B", "event_date": "2026-09-16"},
           {"ticker": "ALMU", "event_date": "2026-09-16"}]
    kept, folded = sc.collapse(day)
    check("the second class is folded into its issuer",
          [x["ticker"] for x in folded] == ["LEN.B"]
          and folded[0]["share_class_of"] == "LEN")
    check("a class with no issuer in the day is kept",
          "BRK.B" in [x["ticker"] for x in kept])
    check("a class reporting on another date is not folded",
          sc.collapse([{"ticker": "X", "event_date": "d1"},
                       {"ticker": "X.A", "event_date": "d2"}])[1] == [])

    print("\nTen European markets (researcher_europe/scripts/*, config europe_hunt)")
    sys.path.insert(0, os.path.join(REPO, "researcher_europe", "scripts"))
    import eu_market as em                                         # noqa: E402
    import eu_sheet as esheet                                      # noqa: E402
    import eu_archive as earch                                     # noqa: E402
    import eu_priced_in as epi                                     # noqa: E402
    import eu_pdftext as epdf                                      # noqa: E402
    import eu_resolve as eres                                      # noqa: E402
    import inspect                                                 # noqa: E402

    # THE YAML BOOLEAN TRAP. Unquoted `no` in a YAML list is the boolean False, so
    # `markets: [uk, de, fr, se, dk, no, fi, it, es, pl]` silently drops Norway -- the
    # best-instrumented of the seven markets added on 2026-09-19. It fails as a wrong
    # RESULT, not as an error, which is exactly the class of bug this file exists for.
    import yaml                                                    # noqa: E402
    cfg = yaml.safe_load(open(os.path.join(REPO, "config", "pipeline.yaml"),
                              encoding="utf-8"))
    mk = cfg["europe_hunt"]["markets"]
    check("every configured European market is a string, not a YAML boolean",
          all(isinstance(x, str) for x in mk), repr(mk))
    check("Norway survives the YAML load", "no" in mk, repr(mk))
    check("every configured market is known to eu_market",
          all(x in em.MARKETS for x in mk),
          repr([x for x in mk if x not in em.MARKETS]))
    check("every market has a hunter agent definition",
          all(os.path.exists(os.path.join(REPO, ".claude", "agents",
                                          em.MARKETS[x]["hunter"] + ".md"))
              for x in mk),
          repr(sorted({em.MARKETS[x]["hunter"] for x in mk})))

    # The Nordic share-class translation. Yahoo answers an empty chart for the wrong
    # symbol rather than erroring, so a broken rule here drops the day's largest Nordic
    # names -- the ones with two share classes -- as "no tape".
    check("a Nordic share class is hyphenated for Yahoo",
          em.yahoo_symbol("se", "OMXSTO:INVE_A") == "INVE-A.ST"
          and em.yahoo_symbol("fi", "OMXHEX:NDA_FI") == "NDA-FI.HE")
    check("a non-Nordic ticker is left alone",
          em.yahoo_symbol("de", "XETR:SAP") == "SAP.DE"
          and em.yahoo_symbol("fr", "EURONEXT:MC") == "MC.PA")

    # `event_occurred: false` is reachable in some markets and not others, and treating
    # an unreachable archive as an empty one is the TRT mistake in mirror image.
    check("event_occurred: false is unreachable where no archive exists",
          not em.false_reachable("es") and not em.false_reachable("pl")
          and not em.false_reachable("de"))
    check("event_occurred: false is reachable where a UNIVERSAL day archive exists",
          all(em.false_reachable(m) for m in ("uk", "fr", "no", "se")))
    # ITALY IS THE EXCEPTION AND IT WAS MEASURED, not assumed. This assertion used to
    # include "it", on the belief that a day archive implies a kill is reachable. On
    # 2026-09-22 PHILOGEN was found absent from eMarket STORAGE's issuer dropdown and
    # from day queries on three dates it is known to have filed, while the archive read
    # fine each time -- so eMarket STORAGE is not universal across Italian issuers and
    # "carries the day and not this issuer" is not evidence of silence there. A day
    # archive is necessary for a kill and not sufficient; `universal` is the rest.
    check("Italy cannot kill on absence: its day archive is not universal",
          em.capability("it", "archive") == "day"
          and em.capability("it", "universal") is False
          and not em.false_reachable("it"))
    check("every other market is universal unless measured otherwise",
          all(em.capability(m, "universal") for m in
              ("uk", "de", "fr", "se", "dk", "no", "fi", "es", "pl")))
    check("a market with no archive returns None, not an empty day",
          earch.day("es", "2026-09-17") is None
          and earch.day("pl", "2026-09-17") is None)

    # --- the four defects the 2026-09-23 run surfaced, fixed 2026-09-22 --------------

    # 1. The PDF extractor used to read only `(literal)` strings, so an issuer's
    #    headline figures -- set in a bold SUBSET font and emitted as `<hex>` -- came
    #    back blank inside fluent prose. A blank where a number belongs is worse than a
    #    failure, because nothing downstream can tell them apart.
    import zlib as _zlib
    _digits = "229,681"
    _cmap = ("/CIDInit /ProcSet findresource begin 12 dict begin begincmap\n"
             f"{len(_digits)} beginbfchar\n"
             + "".join(f"<{i+1:04X}> <{ord(c):04X}>\n"
                       for i, c in enumerate(_digits))
             + "endbfchar\nendcmap end end")
    _codes = "".join(f"{i+1:04X}" for i in range(len(_digits)))
    _body = ("1 0 obj << /Font << /F1 2 0 R >> >> endobj\n"
             "2 0 obj << /ToUnicode 3 0 R >> endobj\n")
    _content = f"BT /F1 12 Tf (Net Profit of ) Tj <{_codes}> Tj ( thousand) Tj ET"

    def _stream(txt):
        return b"stream\n" + _zlib.compress(txt.encode("latin-1")) + b"\nendstream\n"

    _pdf = (b"%PDF-1.4\n" + _body.encode() + b"3 0 obj "
            + _stream(_cmap) + b"endobj\n" + _stream(_content) + b"%%EOF\n")
    _txt = epdf.squeeze(epdf.extract(_pdf))
    check("a hex-encoded subset-font number survives PDF extraction",
          _digits in _txt and "Net Profit of" in _txt)
    check("an ordinary literal-string PDF still extracts unchanged",
          "Ordinary 1,234 text" in epdf.squeeze(epdf.extract(
              b"%PDF-1.4\n" + _stream("BT (Ordinary 1,234 text) Tj ET") + b"%%EOF")))
    check("per-font CMaps are resolved rather than merged",
          b"F1" in epdf._font_cmaps(_pdf))

    # 2. The AMF flux answers a `where=` on a field that does not exist with HTTP 200,
    #    `results: []` and `total_count: null`. An empty list is the one answer that can
    #    support `event_occurred: false`, so a vendor field rename would have made
    #    France start killing names that did report.
    check("fr_day checks total_count before believing an empty day",
          "total_count" in inspect.getsource(earch.fr_day))

    # 3. An ESTIMATED reaction history is a measurably biased scale, not merely a
    #    thinner one, so it must not earn an observed history's magnitude score.
    check("an estimated history is worth less than an observed one",
          "scale_is_lower_bound" in inspect.getsource(epi)
          and "0.35" in inspect.getsource(epi))
    check("eu_resolve splits the ranking by history basis",
          "by_history_basis" in inspect.getsource(eres))

    # 4. The 20- and 5-day run-ups share a blind spot: a move OLDER than twenty
    #    sessions reads flat in both. Sealed as its own control, never in the lean.
    check("a 60-day control is sealed beside the other two",
          "run_up_60d_pct" in inspect.getsource(epi))
    check("the 60-day control is ranked separately",
          "spearman_free_control_neg_runup_60d" in inspect.getsource(eres))
    check("the 60-day run-up is NOT folded into the lean",
          "run_up_60d_pct" not in inspect.getsource(epi.lean_components))

    # Holiday arithmetic, the part most likely to be wrong and least likely to raise.
    check("Midsummer Eve is the Friday between 19 and 25 June",
          em.midsummer_eve(2026).isoformat() == "2026-06-19"
          and em.midsummer_eve(2027).isoformat() == "2027-06-25")
    check("the Nordic and southern exchange calendars are populated",
          all(len(em.exchange_holidays(m, 2026)) >= 9
              for m in ("se", "dk", "no", "fi", "pl", "it", "es")))

    # A results announcement and an announcement ABOUT one are different events. 12 of
    # Nordic Semiconductor's 25 matched history rows were invitations before this.
    for head, want in (("NOD: Results for the first quarter 2026", True),
                       ("Interim report January-June 2026", True),
                       ("NOD: Invitation to first quarter results for 2026", False),
                       ("Notice of Interim Results", False),
                       ("Fortum's financial calendar in 2027", False)):
        got = bool(epi.RESULTS_RE.search(head)) and not bool(epi.NOTICE_RE.search(head))
        check(f"history keeps/drops correctly: {head[:44]}", got == want)

    # The local-language classifier. `bokslutskommunike` has no English cognate, so an
    # English-only classifier misses every Nordic Q4.
    for head, want in (("Delårsrapport kvartal 1, maj - juli 2026", True),
                       ("Bokslutskommuniké 2026", True),
                       ("Osavuosikatsaus tammi-kesäkuu 2026", True),
                       ("Risultati consolidati al 30 giugno 2026", True),
                       ("Raport kwartalny za III kwartał 2026", True),
                       ("Mandatory notification of trade", False)):
        check(f"archive classifier: {head[:44]}",
              earch.looks_like_results(head) == want)

    # The two spreadsheet registers are parsed with the standard library, because this
    # container has no openpyxl and no odfpy.
    import zipfile                                                 # noqa: E402
    import io as _io                                               # noqa: E402
    buf = _io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        # The SpreadsheetML namespace is not decoration: eu_sheet matches on the
        # namespaced local name, because that is what a real .xlsx carries.
        ns = ('xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"')
        z.writestr("xl/sharedStrings.xml",
                   f'<sst {ns}><si><t>Issuer</t></si><si><t>ACME SPA</t></si></sst>')
        z.writestr("xl/worksheets/sheet1.xml",
                   f'<worksheet {ns}><sheetData>'
                   '<row><c r="A1" t="s"><v>0</v></c></row>'
                   '<row><c r="A2" t="s"><v>1</v></c><c r="C2"><v>1.25</v></c></row>'
                   '</sheetData></worksheet>')
    rows = esheet.read(buf.getvalue())
    check("xlsx shared strings resolve and sparse cells keep their column",
          rows[0][0] == "Issuer" and rows[1][0] == "ACME SPA"
          and len(rows[1]) == 3 and rows[1][1] == "" and rows[1][2] == "1.25",
          repr(rows))
    buf = _io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("mimetype", "application/vnd.oasis.opendocument.spreadsheet")
        # Real ODS puts cell text in <text:p>, namespaced, and eu_sheet matches the
        # namespaced local name. A bare <p> is not what the format produces.
        z.writestr("content.xml",
                   '<o xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"'
                   '   xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">'
                   '<table:table>'
                   '<table:table-row>'
                   '<table:table-cell><text:p>A</text:p></table:table-cell>'
                   '<table:table-cell table:number-columns-repeated="3"/>'
                   '<table:table-cell><text:p>B</text:p></table:table-cell>'
                   '</table:table-row></table:table></o>')
    rows = esheet.read(buf.getvalue())
    check("an ods repeated-cell run expands to the right column count",
          rows and rows[0][0] == "A" and rows[0][4] == "B" and len(rows[0]) == 5,
          repr(rows))

    # ---------------------------------------------------------------- stage AU
    print("\nStage AU — Australia")
    sys.path.insert(0, os.path.join(REPO, "researcher_australia", "scripts"))
    import au_market as am                                          # noqa: E402
    import au_priced_in as api                                      # noqa: E402
    import au_positioning as apos                                   # noqa: E402

    # THE ONE-DAY SHIFT. The vendor stamps the UTC instant and Sydney is ten or eleven
    # hours ahead, so 85% of Australian rows sit one Sydney day later than the vendor
    # says. This is the defect most likely to produce a plausible wrong answer: it does
    # not throw, it hunts a name whose print was yesterday.
    import datetime as _dt                                          # noqa: E402
    midnight = int(_dt.datetime(2026, 8, 17, 0, 0, tzinfo=am.UTC).timestamp())
    d, _ = am.sydney_event_date(midnight, "bmo")
    check("a bare UTC midnight on a bmo row moves to the next Sydney day",
          d.isoformat() == "2026-08-18", d)
    d, _ = am.sydney_event_date(midnight, "amc")
    check("a bare UTC midnight on an amc row keeps its date",
          d.isoformat() == "2026-08-17", d)
    # BHP lodged its Appendix 4E at 08:31 on 18 August Sydney time.
    bhp = int(_dt.datetime(2026, 8, 17, 22, 31, tzinfo=am.UTC).timestamp())
    d, basis = am.sydney_event_date(bhp, "bmo")
    check("a real pre-open instant converts to the Sydney date, not vendor + 1",
          d.isoformat() == "2026-08-18" and "Sydney" in basis, f"{d} {basis}")
    # And it survives the daylight-saving change on 2026-10-04, which a constant +1
    # would not: 22:31 UTC is 09:31 AEDT the next day, still pre-open.
    dst = int(_dt.datetime(2026, 10, 15, 22, 31, tzinfo=am.UTC).timestamp())
    d, _ = am.sydney_event_date(dst, "bmo")
    check("the shift survives the AEDT changeover", d.isoformat() == "2026-10-16", d)
    check("a missing vendor date returns None rather than today",
          am.sydney_event_date(None, "bmo")[0] is None)

    # The window. A bmo print is close(D-1) -> close(D); an amc print is the US shape.
    w = am.window_for("bmo", _dt.date(2026, 9, 23), [_dt.date(2026, 9, 22),
                                                     _dt.date(2026, 9, 23),
                                                     _dt.date(2026, 9, 24)])
    check("a bmo window ends on the event date, not after it",
          w["from_close"] == "2026-09-22" and w["to_close"] == "2026-09-23", w)
    w = am.window_for("amc", _dt.date(2026, 9, 23), [_dt.date(2026, 9, 22),
                                                     _dt.date(2026, 9, 23),
                                                     _dt.date(2026, 9, 24)])
    check("an amc window starts on the event date",
          w["from_close"] == "2026-09-23" and w["to_close"] == "2026-09-24", w)

    # THE HOLIDAY CALENDAR. `trading_days()` only knows the PAST -- the tape can say a
    # session happened, never that a future one will -- and this stage always seals for
    # a date beyond the tape. Without a holiday rule the fallback read "weekday means
    # open", so an ASX holiday Monday would have come back as a quiet session, which is
    # the two-causes-look-identical failure that jp_universe.market_closed exists for.
    # The Routine fires on Sundays, so a holiday Monday is not a corner case.
    check("Easter is computed correctly",
          [am.easter(y).isoformat() for y in (2026, 2027, 2028)]
          == ["2026-04-05", "2027-03-28", "2028-04-16"])
    h2026, h2027, h2028 = (am.exchange_holidays(y) for y in (2026, 2027, 2028))
    check("Good Friday and Easter Monday are ASX holidays",
          h2027.get(_dt.date(2027, 3, 26)) == "Good Friday"
          and h2027.get(_dt.date(2027, 3, 29)) == "Easter Monday")
    # Christmas 2027 is a Saturday and Boxing Day a Sunday; both want the Monday. The
    # dict-literal version silently overwrote Christmas and the year came back with two
    # Boxing Days -- right dates, wrong names.
    check("a Christmas/Boxing collision keeps both names and both days",
          h2027.get(_dt.date(2027, 12, 27)) == "Christmas Day"
          and h2027.get(_dt.date(2027, 12, 28)) == "Boxing Day")
    check("Boxing Day 2026 moves to the Monday",
          h2026.get(_dt.date(2026, 12, 28)) == "Boxing Day")
    # ANZAC Day is not substituted when it falls on a weekend, unlike the others.
    check("ANZAC Day is dropped on a weekend and kept on a weekday",
          _dt.date(2026, 4, 25) not in h2026
          and h2028.get(_dt.date(2028, 4, 25)) == "ANZAC Day")
    check("market_open_on names which instrument answered",
          am.market_open_on(_dt.date(2027, 12, 27), [])[1].startswith("ASX holiday")
          and am.market_open_on(_dt.date(2027, 9, 26), [])[1] == "weekend"
          and am.market_open_on(_dt.date(2027, 9, 23), [])[0] is None)

    # THREE CLASSES, NOT ONE. A 4D/4E is a profit result; a 4C/5B is a cash-flow report
    # with a completely different bar; a notice of a results date is neither. Each of
    # the False rows below was a real false positive in the 2026-09-22 build: Myer's
    # "FY24 Results Release Date" scored as a -3.53% reaction, TUA's two "Details"
    # notices as -2.09% and +0.32%, and an S&P index rebalance as -4.88%.
    for head, want in (
            ("BHP Appendix 4E and 2026 Annual Report", "results"),
            ("Appendix 4D and Interim Financial Report", "results"),
            ("2026 Full Year Results Presentation", "results"),
            ("June 2026 Quarterly Report", "quarterly_report"),
            ("Appendix 4C Quarterly Cashflow Report", "quarterly_report"),
            ("Quarterly Activities Report", "quarterly_report"),
            ("FY24 Results Release Date", None),
            ("HY25 Results Presentation Details", None),
            ("Details for FY24 Full Year Results Investor Presentation", None),
            ("S&amp;P DJI Announces September 2026 Quarterly Rebalance", None),
            ("Notice of Annual General Meeting", None),
            ("BHP Group Limited Appendix 4G", None),
            ("Change of Director's Interest Notice", None)):
        check(f"AU classifier: {head[:46]}", api.classify(head) == want,
              f"got {api.classify(head)!r}, want {want!r}")

    # ABSENCE IS A MEASURED ZERO ONLY WHEN THE FILE WAS READ. ASIC's register is not
    # truncated at 0.5%, so an absent product really has no reported position -- but an
    # unreadable file is missing data, and confusing the two invents a zero.
    reg = {"BHP": {"short_pct": 1.5, "short_shares": 100, "product": "BHP"}}
    prev = {"BHP": {"short_pct": 1.0, "short_shares": 90, "product": "BHP"}}
    hit = apos.for_code("BHP", reg, prev, "20260916", "20260909", 4)
    check("a listed product carries its level, change and lag",
          hit["short_pct"] == 1.5 and hit["short_change_pct_pts"] == 0.5
          and hit["in_register"] and hit["lag_sessions"] == 4, hit)
    absent = apos.for_code("ZZZ", reg, prev, "20260916", "20260909", 4)
    check("an absent product is a measured zero when the register was read",
          absent["short_pct"] == 0.0 and absent["covered"] and not absent["in_register"])
    broken = apos.for_code("BHP", {}, {}, None, None, None)
    check("an unreadable register is None, never a zero",
          broken["short_pct"] is None and not broken["covered"]
          and "missing data" in broken["basis"], broken)

    # The stage places no orders, and the skill and hunter must not acquire one.
    au_skill = open(os.path.join(REPO, ".claude", "skills",
                              "researcher-australia-hunt", "SKILL.md"),
                 encoding="utf-8").read()
    au_agent = open(os.path.join(REPO, ".claude", "agents",
                              "unpriced-hunter-au.md"),
                 encoding="utf-8").read()
    check("stage AU's skill places no orders",
          "alpaca_trade.py" not in au_skill.replace(
              "There is no `alpaca_trade.py` step", ""))
    # ONE ENGLISH PASS. A later edit that reintroduces pre_local would emit a
    # structurally zero delta that somebody would pool with the German and French ones.
    check("the AU hunter has no pre_local freeze",
          '"pre_local"' not in au_agent and "local_pass_note" not in au_agent.replace(
              "No `local_pass_note`.", "").replace(
              "`local_pass_note`", "").replace("and `local_pass_note` in this", ""))
    check("the AU hunter still carries the pre_lessons control",
          '"pre_lessons"' in au_agent and "lessons_applied" in au_agent)
    check("config says language_pass is off for Australia",
          cfg["australia_hunt"]["language_pass"] is False)
    check("config gives Australia the same turnover floor as the other stages",
          cfg["australia_hunt"]["min_turnover_usd"] == 200000)
    check("stage AU has no execution block",
          "execution" not in cfg["australia_hunt"])
    check("researcher_australia/LESSONS.md carries no rules yet",
          "Add the first rule when" in
          open(os.path.join(REPO, "researcher_australia", "LESSONS.md"),
               encoding="utf-8").read())

    print("\nData fetch")
    ok, out = run(["scripts/get_earnings.py", "--probe"])
    if ok:
        print("  ok    at least one earnings source is reachable")
    else:
        print("  WARN  no earnings source reachable from this environment")
        print("        The pipeline will fall back to WebSearch and produce weaker")
        print("        dossiers. Point the Routines at an environment with full")
        print("        network access. See docs/ROUTINES.md.")
        for line in out.splitlines():
            print(f"        {line}")

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All plumbing checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
