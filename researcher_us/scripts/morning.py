#!/usr/bin/env python3
"""Stage M — the morning-after exit review, half an hour before the US open.

Built 2026-10-18 on the operator's instruction: *"a routine that runs one hour before
the open and, for the names that scored 60 or higher the day before (US only), judges
the earnings release, the public reaction and the stock's move, and from that the
expected price reaction and the recommended action at the open: sell, limit, or wait
until the end of the day."* Moved the same day to 08:56 ET, so the bmo releases of
08:00-08:30 are out before it reads them, and on 2026-10-20 to 09:10 ET (operator's
instruction): the whole stage measured about four minutes end to end on its first two
fires, and the last twenty minutes of pre-market are what decide the open (HAS read
+0.1% at 08:56 and +4.0% at 09:25 on 2026-10-20).

WHAT IT READS. Stage E-P's run of the previous trading day,
`research/<prev>/edge-panel/edge-scores-panel.json`. A name is picked when its
`panel_pct` (0-100, the size of the mean of the four judges' own-range percentiles) is
at or above `morning_exit.min_panel_pct` (60) and its print falls in this morning's
window: an amc name that reported after yesterday's close, or a bmo name reporting this
morning. The POSITION is the panel's side, entered at 13:30 ET on the entry day: the
scorebord's window, which is the operator's.

THE FOUR ACTIONS, from the position's point of view (a short's "sell" is a cover):

    exit_open    sell at the opening print, market order
    exit_1000    sell at market at 10:00 ET (added 2026-10-20, see below)
    exit_limit   a day limit at a stated price beyond the pre-market price (a sell
                 above it for a long, a cover below it for a short); unfilled at the
                 close, it goes at the close
    exit_close   hold through the session, sell at the close

THE OPENING QUESTION (2026-10-20, `researcher_us/analysis/open-lag.md`). Over 231 US
earnings events with a pre-market gap of 2% or more, the open held a median 98% of the
pre-market move, and from there the gap FADED: a position on the side of the move gave
back about 1.0-1.4 points by 10:00 when the pre-market traded actively. When the
pre-market was stale (last print 31+ minutes before the open, or fewer than six 5m
bars) the open lagged, and what followed was a coin flip once the pre-market reference
was made robust. So the brief carries the pre-market at 1-minute resolution, a robust
reference (the median of the last five 1m prints) and the stale flag, the analyst gets
the findings as principles without numbers or cases (operator, 2026-10-20: numbers
lead), and every review answers three scorable questions: `p_open_lags`, `px_1000_pct`
and `p_fade_by_1000`. `compile` attaches the measured base rate per name and `resolve`
scores the forecasts against it on the same names; it never reaches a brief.

THE CONTROL. Every advice row also carries what the scorebord's own rule does with no
morning review at all: amc out at the open, bmo out at 13:00 ET. The review has added
something only where it beats that rule on the same names, pooled over many mornings
(`pool`). One morning is an anecdote.

IT PLACES NO ORDERS, and there is no code path that could.

    python3 researcher_us/scripts/morning.py slot
    python3 researcher_us/scripts/morning.py pick      [--date D]
    python3 researcher_us/scripts/morning.py snapshot  [--date D] [--final]
    python3 researcher_us/scripts/morning.py compile   [--date D]
    python3 researcher_us/scripts/morning.py resolve   [--date D]
    python3 researcher_us/scripts/morning.py pool
"""
import argparse
import glob
import json
import math
import statistics as st
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))
sys.path.insert(0, str(REPO / "scripts"))
import edge_exit as EX                      # noqa: E402  Yahoo plumbing, one price source
from get_earnings import is_trading_day     # noqa: E402  NYSE calendar, holidays included

ET = ZoneInfo("America/New_York")
ACTIONS = ("exit_open", "exit_1000", "exit_limit", "exit_close")
TICK = 0.01        # a limit counts as filled only when the tape traded THROUGH it
MIN_GAP_PCT = 2.0  # below this the open-lag questions are a ratio of two noises
STALE_MINUTES = 31  # open_lag.py's definition, so the prior and the flag agree
STALE_BARS = 6
OPEN_LAG_FILE = REPO / "researcher_us" / "analysis" / "open-lag.json"


def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml"))
    out = dict(c.get("morning_exit") or {})
    out.setdefault("disclaimer", (c.get("output") or {}).get("disclaimer"))
    return out


def hm(s):
    h, m = str(s).split(":")
    return int(h) * 60 + int(m)


def run_dir(d):
    return REPO / "research" / f"{d:%Y}" / f"{d:%m}" / d.isoformat()


def prev_trading_day(d):
    p = d - timedelta(days=1)
    while not is_trading_day(p):
        p -= timedelta(days=1)
    return p


def paths(d, C):
    prev = prev_trading_day(d)
    src = run_dir(prev) / C.get("source_dir", "edge-panel")
    out = run_dir(d) / C.get("output_dir", "morning")
    return prev, src, out


def _load(p):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return None


def _write(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def _rel(p):
    p = Path(p)
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def _now_utc():
    return datetime.now(timezone.utc)


def _date_arg(a):
    return date.fromisoformat(a) if a else _now_utc().astimezone(ET).date()


# ------------------------------------------------------------------------ slot

def slot(C, now=None):
    now = now or _now_utc()
    et = now.astimezone(ET)
    d = et.date()
    prev, src, out = paths(d, C)
    mins = et.hour * 60 + et.minute
    status = ("complete" if (out / "morning-advice.json").exists()
              else "partial" if (out / "picks.json").exists() else "new")
    return {"now_utc": now.isoformat(timespec="seconds"),
            "now_et": et.strftime("%Y-%m-%d %H:%M %Z"),
            "date": d.isoformat(), "trading_day": is_trading_day(d),
            "inside_hours": hm(C.get("earliest_et", "06:30")) <= mins
            <= hm(C.get("latest_et", "09:29")),
            "minutes_to_open": 9 * 60 + 30 - mins,
            "source_run_date": prev.isoformat(), "source_run": _rel(src),
            "source_exists": (src / "edge-scores-panel.json").exists(),
            "out": _rel(out), "status": status}


# ------------------------------------------------------------------------ pick

def pick(d, C):
    prev, src, out = paths(d, C)
    panel = _load(src / "edge-scores-panel.json")
    if panel is None:
        return {"date": d.isoformat(), "source_run": _rel(src),
                "error": "no edge-scores-panel.json in the source run", "picks": [],
                "excluded": []}
    uni = {r["ticker"]: r for r in (_load(src / "universe.json") or {}).get("names", [])}
    floor = float(C.get("min_panel_pct", 60))
    min_members = int(C.get("min_members", 3))
    picks, excluded = [], []
    for r in panel.get("ranking", []):
        t = r["ticker"]
        b = _load(src / "baselines" / f"{t}.json") or {}
        ev, ses = b.get("event_date"), b.get("session")
        pct = r.get("panel_pct")
        why = None
        if pct is None or pct < floor:
            why = f"panel_pct {pct} below {floor:g}"
        elif (r.get("n_members") or 0) < min_members:
            why = f"{r.get('n_members')} judges, fewer than {min_members}"
        elif not r.get("side"):
            why = "panel has no side"
        elif b.get("event_occurred") is False:
            why = "baseline amended: event did not occur"
        elif not (ses == "amc" and ev == prev.isoformat()
                  or ses == "bmo" and ev == d.isoformat()):
            why = f"print {ev} {ses} is not in this morning's window"
        if why:
            excluded.append({"ticker": t, "panel_pct": pct, "reason": why})
            continue
        u = uni.get(t, {})
        tape = b.get("tape") or {}
        picks.append({
            "ticker": t, "company": u.get("company"), "session": ses, "event_date": ev,
            "entry_date": prev.isoformat(),
            "side": int(r["side"]), "position": "long" if r["side"] > 0 else "short",
            "panel_pct": pct, "panel_pct_sd": r.get("panel_pct_sd"),
            "n_members": r.get("n_members"), "selected_by_panel": bool(r.get("selected")),
            "expected_return_pct": r.get("expected_return_pct"),
            "p_right": r.get("p_right"),
            "judge_notes": {m: (v or {}).get("note") for m, v in
                            (r.get("members") or {}).items()},
            "eps_forecast_nasdaq": u.get("eps_forecast"),
            "n_estimates_nasdaq": u.get("n_estimates"),
            "baseline": {"spot": tape.get("spot"), "as_of_utc": b.get("as_of_utc"),
                         "expected_move_pct": b.get("expected_move_pct"),
                         "expected_move_basis": b.get("expected_move_basis"),
                         "deadband_pct": b.get("deadband_pct"),
                         "history": (b.get("history") or {}).get("moves", [])[:8]},
            "source_files": {
                "baseline": _rel(src / "baselines" / f"{t}.json"),
                "hunt": _rel(src / "hunts" / f"{t}.json")},
        })
    picks.sort(key=lambda p: -p["panel_pct"])
    cap = int(C.get("max_names", 10))
    for p in picks[cap:]:
        excluded.append({"ticker": p["ticker"], "panel_pct": p["panel_pct"],
                         "reason": f"over the cap of {cap} names"})
    res = {"generated_utc": _now_utc().isoformat(timespec="seconds"),
           "date": d.isoformat(), "source_run": _rel(src),
           "source_stage": C.get("source_stage", "E-P"),
           "rule": f"panel_pct >= {floor:g}, >= {min_members} judges, print in this "
                   f"morning's window (amc {prev} or bmo {d}); top {cap} by panel_pct",
           "picks": picks[:cap], "excluded": excluded}
    _write(out / "picks.json", res)
    return res


# -------------------------------------------------------------------- prices

def bars5(ticker, rng="5d"):
    """5-minute bars with pre- and post-market, keyed by ET date. High and low are
    kept because a limit order is decided by them."""
    j = EX._get(f"{EX.YQ}/v8/finance/chart/{EX.yahoo_symbol(ticker)}"
                f"?range={rng}&interval=5m&includePrePost=true")
    res = ((j or {}).get("chart") or {}).get("result")
    if not res or not res[0].get("timestamp"):
        return {}
    r = res[0]
    q = (r.get("indicators") or {}).get("quote", [{}])[0]
    out = {}
    for i, ts in enumerate(r["timestamp"]):
        c = q.get("close", [None])[i]
        if c is None:
            continue
        t = datetime.fromtimestamp(ts, timezone.utc).astimezone(ET)
        out.setdefault(t.date().isoformat(), []).append({
            "hm": t.hour * 60 + t.minute, "open": q["open"][i], "high": q["high"][i],
            "low": q["low"][i], "close": c, "volume": q["volume"][i] or 0})
    return out


def _last(day, lo, hi):
    v = [b for b in day if lo <= b["hm"] <= hi]
    return v[-1] if v else None


def _pct(a, b):
    return None if a is None or not b else round((a / b - 1) * 100, 3)


def bars1(ticker):
    """Today's 1-minute bars with the pre-market, keyed by ET date."""
    j = EX._get(f"{EX.YQ}/v8/finance/chart/{EX.yahoo_symbol(ticker)}"
                f"?range=1d&interval=1m&includePrePost=true")
    res = ((j or {}).get("chart") or {}).get("result")
    if not res or not res[0].get("timestamp"):
        return {}
    r = res[0]
    q = (r.get("indicators") or {}).get("quote", [{}])[0]
    out = {}
    for i, ts in enumerate(r["timestamp"]):
        c = q.get("close", [None])[i]
        if c is None:
            continue
        t = datetime.fromtimestamp(ts, timezone.utc).astimezone(ET)
        out.setdefault(t.date().isoformat(), []).append(
            {"hm": t.hour * 60 + t.minute, "close": c})
    return out


def _hhmm(m):
    return None if m is None else f"{m // 60:02d}:{m % 60:02d}"


def premarket_detail(ticker, today, mins, pm_bars5, prev_close):
    """How alive the pre-market is, and a reference that one stray print cannot move.

    EFX on 2026-10-20 printed once at yesterday's close at 09:10 between prints of
    166-170, so the last print alone is not a reference. `stale_at_open` assumes no
    further print before 09:30, so it can only turn false later, never true."""
    try:
        m1 = [b for b in bars1(ticker).get(today, [])
              if 4 * 60 <= b["hm"] < min(mins + 1, 9 * 60 + 30)]
    except Exception:
        m1 = []
    basis = "1m"
    prints = m1
    if not prints:
        basis = "5m"
        prints = [{"hm": b["hm"], "close": b["close"]} for b in pm_bars5]
    last_hm = prints[-1]["hm"] if prints else None
    ref = st.median(b["close"] for b in prints[-5:]) if prints else None
    stale = (last_hm is None or 9 * 60 + 30 - last_hm >= STALE_MINUTES
             or len(pm_bars5) < STALE_BARS)
    return {
        "basis": basis,
        "prints": len(prints),
        "prints_last_30m": len([b for b in prints if b["hm"] >= mins - 30]),
        "bars_5m": len(pm_bars5),
        "last_print_et": _hhmm(last_hm),
        "minutes_since_last_print": None if last_hm is None else mins - last_hm,
        "reference_median_last5": ref,
        "reference_pct_vs_prev_close": _pct(ref, prev_close),
        "stale_at_open": stale,
        "stale_rule": f"last print {STALE_MINUTES}+ minutes before 09:30 (assuming no "
                      f"further print) or fewer than {STALE_BARS} five-minute bars",
    }


def open_lag_prior(stale):
    """The measured base rates for this name's group, from open_lag.py's report.

    p_open_lags: the open holds less than half of the pre-market move.
    p_fade_by_1000: from the open to 10:00 the price moves back toward yesterday's
    close (against the pre-market move). Both on events with |pre-market gap| >= 2%."""
    rep_ = _load(OPEN_LAG_FILE) or {}
    g = rep_.get("stale_pm" if stale else "fresh_pm") or {}
    w = (g.get("wait_minus_open") or {}).get("1000") or {}
    if not g.get("n_big_gap"):
        return {"available": False, "source": _rel(OPEN_LAG_FILE)}
    return {
        "available": True, "group": "stale" if stale else "fresh",
        "n_events": g["n_big_gap"],
        "p_open_lags": round(100 * g["open_short_rate"], 1),
        "p_fade_by_1000": None if w.get("share_better") is None
        else round(100 * (1 - w["share_better"]), 1),
        "median_open_capture": round(g["median_capture_open"], 2),
        "gapside_1000_minus_open_pp": None if w.get("mean") is None
        else round(w["mean"], 2),
        "caveat": ("measured on the last pre-market print; with a robust reference the "
                   "fresh-group fade holds (-1.39pp, t -3.4) and the stale group is a "
                   "coin flip (+0.99pp, t 1.45, 2 lags against 6 fades): a stale "
                   "pre-market is uncertainty, not a signal"),
        "source": _rel(OPEN_LAG_FILE),
    }


def price_snapshot(p, now_et):
    """What the tape says at decision time. Every number is Yahoo's; none is typed."""
    dd = EX.daily(p["ticker"]) or {}
    m5 = bars5(p["ticker"])
    today = now_et.date().isoformat()
    closes = sorted(k for k in dd if k < today)
    prev_close = dd[closes[-1]]["close"] if closes else None
    entry_bar = _last(m5.get(p["entry_date"], []), 13 * 60, 13 * 60 + 30)
    entry_px, entry_basis = (entry_bar["close"], "13:30 ET 5m bar") if entry_bar else (
        p["baseline"].get("spot"), "sealed baseline spot (no 13:30 bar)")
    ah = (_last(m5.get(p["event_date"], []), 16 * 60 + 5, 20 * 60)
          if p["session"] == "amc" else None)
    mins = now_et.hour * 60 + now_et.minute
    pm_day = m5.get(today, [])
    pm = _last(pm_day, 4 * 60, min(mins, 9 * 60 + 25))
    pm_bars = [b for b in pm_day if 4 * 60 <= b["hm"] < 9 * 60 + 30]
    reg = _last(pm_day, 9 * 60 + 30, min(mins, 16 * 60)) if mins >= 9 * 60 + 30 else None
    last = (reg or pm or {}).get("close")
    side = p["side"]
    detail = premarket_detail(p["ticker"], today, mins, pm_bars, prev_close)
    return {
        "as_of_et": now_et.strftime("%Y-%m-%d %H:%M %Z"),
        "prev_close": prev_close, "prev_close_date": closes[-1] if closes else None,
        "entry_px": entry_px, "entry_basis": entry_basis,
        "after_hours_last": ah and ah["close"],
        "after_hours_pct_vs_prev_close": _pct(ah and ah["close"], prev_close),
        "premarket_last": pm and pm["close"],
        "premarket_time_et": pm and f"{pm['hm'] // 60:02d}:{pm['hm'] % 60:02d}",
        "premarket_high": max((b["high"] for b in pm_bars if b["high"]), default=None),
        "premarket_low": min((b["low"] for b in pm_bars if b["low"]), default=None),
        "premarket_volume": sum(b["volume"] for b in pm_bars),
        "premarket_pct_vs_prev_close": _pct(pm and pm["close"], prev_close),
        "premarket_detail": detail,
        "after_open": reg is not None,
        "last": last,
        "position_return_so_far_pct": (None if _pct(last, entry_px) is None
                                       else round(side * _pct(last, entry_px), 3)),
        "volume_note": "Yahoo's extended-hours bars often carry no volume; a zero is "
                       "not evidence that nothing traded.",
    }


def market_snapshot(now_et):
    out = {}
    for sym in ("SPY", "QQQ", "IWM"):
        dd = EX.daily(sym) or {}
        m5 = bars5(sym, "2d")
        today = now_et.date().isoformat()
        closes = sorted(k for k in dd if k < today)
        pc = dd[closes[-1]]["close"] if closes else None
        mins = now_et.hour * 60 + now_et.minute
        b = _last(m5.get(today, []), 4 * 60, min(mins, 16 * 60))
        out[sym] = {"prev_close": pc, "last": b and b["close"],
                    "pct_vs_prev_close": _pct(b and b["close"], pc)}
    return out


def snapshot(d, C, final=False, now=None):
    _, _, out = paths(d, C)
    picks = _load(out / "picks.json")
    if not picks:
        raise SystemExit("no picks.json: run `pick` first")
    now_et = (now or _now_utc()).astimezone(ET)
    snap = {"generated_utc": _now_utc().isoformat(timespec="seconds"),
            "as_of_et": now_et.strftime("%Y-%m-%d %H:%M %Z"),
            "market": market_snapshot(now_et), "names": {}}
    for p in picks["picks"]:
        s = price_snapshot(p, now_et)
        snap["names"][p["ticker"]] = s
        if not final:
            _write(out / "briefs" / f"{p['ticker']}.json", {
                "stage": "M", "date": d.isoformat(), "pick": p, "tape": s,
                "market": snap["market"],
                "output_path": _rel(out / "reviews" / f"{p['ticker']}.json"),
                "actions": {
                    "exit_open": "sell (cover a short) at the opening print, market",
                    "exit_1000": "sell (cover a short) at market at 10:00 ET",
                    "exit_limit": "day limit beyond the pre-market price; unfilled -> "
                                  "out at the close",
                    "exit_close": "hold through the session, out at the close"},
                "static_rule": static_rule(p["session"], C),
                "compiled_at_et": C.get("advice_deadline_et", "09:24")})
    _write(out / ("snapshot-final.json" if final else "snapshot.json"), snap)
    return snap


def static_rule(session, C):
    return (C.get("static_rule") or {"amc": "exit_open", "bmo": "exit_1300"})[session]


# --------------------------------------------------------------------- compile

def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def check_review(rv, p, tape):
    """Problems with one review, as strings. An empty list is a usable review."""
    probs = []
    rec = (rv or {}).get("recommendation") or {}
    act = rec.get("action")
    released = ((rv or {}).get("release") or {}).get("found")
    if act not in ACTIONS + ("none",):
        probs.append(f"action {act!r} is not one of {ACTIONS + ('none',)}")
    if act == "none" and released:
        probs.append("action none although the release was found")
    if act == "exit_limit":
        lp = rec.get("limit_price")
        ref = tape.get("last")
        if not _num(lp):
            probs.append("exit_limit without a numeric limit_price")
        elif ref and (lp - ref) * p["side"] <= 0:
            probs.append(f"limit {lp} is not beyond the pre-market price {ref} on the "
                         f"position's side, so it is a market order at the open")
    exp = (rv or {}).get("expected") or {}
    if act in ACTIONS:
        for k in ("open_pct_vs_prev_close", "open_to_close_pct", "px_1000_pct_vs_prev_close"):
            if not _num(exp.get(k)):
                probs.append(f"expected.{k} missing")
        for k in ("p_open_lags", "p_fade_by_1000"):
            if not _num(exp.get(k)) or not 0 <= exp[k] <= 100:
                probs.append(f"expected.{k} missing or outside 0-100")
    rel = (rv or {}).get("release") or {}
    if released and not str(rel.get("source_url", "")).startswith("http"):
        probs.append("release found but no source_url")
    return probs


def compile_advice(d, C):
    prev, src, out = paths(d, C)
    picks = _load(out / "picks.json") or {"picks": []}
    snap = _load(out / "snapshot.json") or {"names": {}}
    try:
        final = snapshot(d, C, final=True)
    except Exception as e:                  # a dead feed must not cost the advice
        final = {"names": {}, "error": f"{type(e).__name__}: {e}"}
    rows = []
    for p in picks["picks"]:
        t = p["ticker"]
        rv = _load(out / "reviews" / f"{t}.json")
        tape = snap["names"].get(t, {})
        tape_f = final["names"].get(t, {})
        probs = ["review missing"] if rv is None else check_review(rv, p, tape)
        rec = (rv or {}).get("recommendation") or {}
        exp = (rv or {}).get("expected") or {}
        usable = not probs
        rows.append({
            "ticker": t, "company": p.get("company"), "session": p["session"],
            "event_date": p["event_date"], "position": p["position"], "side": p["side"],
            "panel_pct": p["panel_pct"], "selected_by_panel": p["selected_by_panel"],
            "entry_px": tape.get("entry_px"), "entry_basis": tape.get("entry_basis"),
            "prev_close": tape.get("prev_close"),
            "premarket_at_review": tape.get("premarket_last"),
            "premarket_pct_at_review": tape.get("premarket_pct_vs_prev_close"),
            "premarket_at_compile": tape_f.get("premarket_last"),
            "premarket_pct_at_compile": tape_f.get("premarket_pct_vs_prev_close"),
            "premarket_ref_at_compile": (tape_f.get("premarket_detail") or {}).get(
                "reference_median_last5"),
            "premarket_ref_pct_at_compile": (tape_f.get("premarket_detail") or {}).get(
                "reference_pct_vs_prev_close"),
            "premarket_stale_at_compile": (tape_f.get("premarket_detail") or {}).get(
                "stale_at_open"),
            # The base rate is the scoring control and is never put in a brief: the
            # operator's instruction of 2026-10-20 is principles for the analyst, not
            # numbers or cases, because numbers lead.
            "open_lag_prior": open_lag_prior(next(
                (x for x in ((tape_f.get("premarket_detail") or {}).get("stale_at_open"),
                             (tape.get("premarket_detail") or {}).get("stale_at_open"))
                 if x is not None), False)),
            "position_return_so_far_pct": next(
                (x for x in (tape_f.get("position_return_so_far_pct"),
                             tape.get("position_return_so_far_pct")) if x is not None), None),
            "release_found": ((rv or {}).get("release") or {}).get("found"),
            "thesis": ((rv or {}).get("thesis_check") or {}).get("verdict"),
            "expected_open_pct": exp.get("open_pct_vs_prev_close"),
            "expected_open_to_close_pct": exp.get("open_to_close_pct"),
            "p_open_to_close_up": exp.get("p_open_to_close_up"),
            "expected_1000_pct": exp.get("px_1000_pct_vs_prev_close"),
            "p_open_lags": exp.get("p_open_lags"),
            "p_fade_by_1000": exp.get("p_fade_by_1000"),
            "confidence": exp.get("confidence"),
            "action": rec.get("action") if usable else "none",
            "limit_price": rec.get("limit_price") if usable else None,
            "reason": rec.get("reason"),
            "what_would_change_it": rec.get("what_would_change_it"),
            "static_rule": static_rule(p["session"], C),
            "problems": probs,
        })
    res = {"generated_utc": _now_utc().isoformat(timespec="seconds"),
           "date": d.isoformat(), "stage": "M", "source_run": picks.get("source_run"),
           "rule": picks.get("rule"),
           "market": (final.get("market") if any(
               (v or {}).get("last") for v in (final.get("market") or {}).values())
               else snap.get("market")),
           "places_orders": False, "rows": rows, "excluded": picks.get("excluded", [])}
    _write(out / "morning-advice.json", res)
    (out / "morning-note.md").write_text(render_note(res, C))
    return res


ACTION_NL = {"exit_open": "Verkopen bij opening", "exit_limit": "Limietorder",
             "exit_close": "Wachten tot slot", "none": "Geen advies",
             "exit_1000": "Verkopen om 10:00",
             "exit_1300": "Uit om 13:00 ET"}


def _f(x, nd=2, sign=True):
    if not _num(x):
        return "—"
    return f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"


def render_note(res, C):
    L = [f"# Ochtendadvies {res['date']} — stage M", "",
         f"Bron: `{res['source_run']}` (stage E-P). Regel: {res['rule']}. "
         "Positie = de kant van het panel, instap 13:30 ET op de instapdag. "
         "**Er worden geen orders geplaatst.**", ""]
    mk = res.get("market") or {}
    if mk:
        L.append("Markt premarket: " + ", ".join(
            f"{k} {_f(v.get('pct_vs_prev_close'))}%" for k, v in mk.items()))
        L.append("")
    if not res["rows"]:
        L += ["Geen namen met panel_pct ≥ "
              f"{C.get('min_panel_pct', 60)} in het venster van vanochtend.", ""]
    else:
        L += ["| Naam | Sessie | Positie | panel_pct | Premarket vs slot | Positie tot nu "
              "| Voorbeurs stil | Verwacht open | Verwacht 10:00 | Verwacht open→slot "
              "| **Advies** | Limiet | Vaste regel |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in res["rows"]:
            L.append(
                f"| {r['ticker']} | {r['session']} | {r['position']} | "
                f"{_f(r['panel_pct'], 1, False)}{'*' if r['selected_by_panel'] else ''} | "
                f"{_f(next((x for x in (r.get('premarket_ref_pct_at_compile'), r['premarket_pct_at_compile'], r['premarket_pct_at_review']) if x is not None), None))}% | "
                f"{_f(r['position_return_so_far_pct'])}% | "
                f"{'ja' if r.get('premarket_stale_at_compile') else 'nee' if r.get('premarket_stale_at_compile') is False else '—'} | "
                f"{_f(r['expected_open_pct'])}% | {_f(r.get('expected_1000_pct'))}% | "
                f"{_f(r['expected_open_to_close_pct'])}% | **{ACTION_NL[r['action']]}** | "
                f"{_f(r['limit_price'], 2, False)} | {ACTION_NL.get(r['static_rule'])} |")
        L += ["", "`*` = door het panel geselecteerd (top 20%). Premarket = de mediaan van de "
              "laatste vijf voorbeurstransacties om 09:24. Rendementen in % vanaf "
              "de kant van de positie; verwachtingen zijn ten opzichte van het slot van "
              "gisteren.", ""]
        for r in res["rows"]:
            L.append(f"## {r['ticker']} — {ACTION_NL[r['action']]}")
            L.append("")
            if r["reason"]:
                L.append(r["reason"])
                L.append("")
            if r["what_would_change_it"]:
                L.append(f"*Wat dit advies verandert:* {r['what_would_change_it']}")
                L.append("")
            if r["problems"]:
                L.append("Niet bruikbaar: " + "; ".join(r["problems"]))
                L.append("")
    if res["excluded"]:
        L += ["## Niet meegenomen", ""]
        L += [f"- {e['ticker']}: {e['reason']}" for e in res["excluded"]]
        L.append("")
    L += ["## Hoe dit te lezen", "",
          "Elk advies wordt na het slot gescoord tegen de vaste regel (amc uit bij "
          "opening, bmo uit om 13:00 ET) op dezelfde namen (`morning.py resolve`, "
          "`pool`). Eén ochtend is een anekdote: pas over veel ochtenden blijkt of de "
          "beoordeling iets toevoegt aan de vaste regel.", "",
          "*Voorbeurs stil* = de laatste voorbeurstransactie ligt 31 minuten of meer "
          "voor de opening, of er waren minder dan zes 5-minutenbars. Gemeten over 231 "
          "earnings-events houdt de opening meestal de hele voorbeursbeweging vast en "
          "zakt de koers daarna tot 10:00 terug; bij een stille voorbeurs is de "
          "opening onbetrouwbaar en is de richting daarna onzeker "
          "(`researcher_us/analysis/open-lag.md`).", "",
          (C.get("disclaimer") or "This is a forecasting exercise over public "
           "information. It is not investment advice."), ""]
    return "\n".join(L)


# --------------------------------------------------------------------- resolve

def exit_prices_today(ticker, d):
    """Regular-session prices on D: open, 13:00, close, high, low. None until the
    close exists, so nothing that has not happened is ever scored."""
    dd = EX.daily(ticker) or {}
    m5 = bars5(ticker, "5d").get(d.isoformat(), [])
    reg = [b for b in m5 if 9 * 60 + 30 <= b["hm"] < 16 * 60]
    if d.isoformat() not in dd or not reg:
        return None
    now = _now_utc().astimezone(ET)
    if d == now.date() and now.hour * 60 + now.minute < 16 * 60 + 10:
        return None
    b13 = _last(reg, 12 * 60 + 55, 12 * 60 + 55) or _last(reg, 9 * 60 + 30, 12 * 60 + 55)
    b10 = _last(reg, 9 * 60 + 55, 9 * 60 + 55) or _last(reg, 9 * 60 + 30, 9 * 60 + 55)
    return {"open": dd[d.isoformat()]["open"], "close": dd[d.isoformat()]["close"],
            "px_1300": b13 and b13["close"], "px_1000": b10 and b10["close"],
            "high": max(b["high"] for b in reg if b["high"]),
            "low": min(b["low"] for b in reg if b["low"]),
            "high_after_open": max((b["high"] for b in reg if b["hm"] >= 9 * 60 + 35
                                    and b["high"]), default=None),
            "low_after_open": min((b["low"] for b in reg if b["hm"] >= 9 * 60 + 35
                                   and b["low"]), default=None)}


def limit_exit(side, lp, px):
    """Where a day limit leaves the position. Through at the open -> the open; traded
    through during the session -> the limit; else the close."""
    o = px["open"]
    if (o - lp) * side >= 0:
        return o, "filled_at_open"
    hi, lo = px["high"], px["low"]
    if side > 0 and hi is not None and hi >= lp + TICK:
        return lp, "filled_intraday"
    if side < 0 and lo is not None and lo <= lp - TICK:
        return lp, "filled_intraday"
    return px["close"], "unfilled_out_at_close"


def open_lag_outcome(r, px):
    """Did the open lag the pre-market, and did the price fade back by 10:00?

    The reference is the pre-market at the compile (the robust median when present).
    Unscored (None) when the gap is under MIN_GAP_PCT or a price is missing. Brier
    scores sit beside the base rate's, so the review is judged against the prior."""
    pc = r.get("prev_close")
    ref = r.get("premarket_ref_at_compile") or r.get("premarket_at_compile") \
        or r.get("premarket_at_review")
    out = {"open_lag_reference": ref, "realised_open_lags": None,
           "realised_fade_by_1000": None}
    if not (pc and ref and px.get("open")) or abs(ref / pc - 1) * 100 < MIN_GAP_PCT:
        return out
    g = ref - pc
    out["realised_open_lags"] = (px["open"] - pc) / g < 0.5
    if px.get("px_1000") is not None:
        out["realised_fade_by_1000"] = (px["px_1000"] - px["open"]) * (1 if g > 0 else -1) < 0
    prior = r.get("open_lag_prior") or {}
    for k, real in (("p_open_lags", out["realised_open_lags"]),
                    ("p_fade_by_1000", out["realised_fade_by_1000"])):
        if real is None:
            continue
        y = 1.0 if real else 0.0
        if _num(r.get(k)):
            out[f"brier_{k}"] = round((r[k] / 100 - y) ** 2, 4)
        if _num(prior.get(k)):
            out[f"brier_{k}_prior"] = round((prior[k] / 100 - y) ** 2, 4)
    return out


def resolve(d, C):
    _, _, out = paths(d, C)
    adv = _load(out / "morning-advice.json")
    if not adv:
        raise SystemExit("no morning-advice.json for this date")
    rows = []
    for r in adv["rows"]:
        px = exit_prices_today(r["ticker"], d)
        entry = r.get("entry_px")
        if px is None or not entry:
            rows.append({"ticker": r["ticker"], "pending": True})
            continue
        s = r["side"]

        def ret(x):
            return None if x is None else round(s * (x / entry - 1) * 100, 3)
        rets = {"exit_open": ret(px["open"]), "exit_close": ret(px["close"]),
                "exit_1300": ret(px["px_1300"]), "exit_1000": ret(px.get("px_1000"))}
        fill = None
        if _num(r.get("limit_price")):
            lx, fill = limit_exit(s, r["limit_price"], px)
            rets["exit_limit"] = ret(lx)
        rec = r["action"] if r["action"] in rets else r["static_rule"]
        rows.append({
            "ticker": r["ticker"], "session": r["session"], "position": r["position"],
            "panel_pct": r["panel_pct"], "pending": False,
            "action": r["action"], "scored_as": rec, "static_rule": r["static_rule"],
            "limit_fill": fill, "px": px, "entry_px": entry, "returns": rets,
            "recommended_return": rets.get(rec),
            "static_return": rets.get(r["static_rule"]),
            "review_minus_static": (None if rets.get(rec) is None
                                    or rets.get(r["static_rule"]) is None
                                    else round(rets[rec] - rets[r["static_rule"]], 3)),
            "best_action": max(("exit_open", "exit_1000", "exit_close", "exit_1300"),
                               key=lambda k: rets[k] if rets[k] is not None else -1e9),
            "expected_open_pct": r.get("expected_open_pct"),
            "realised_open_pct": _pct(px["open"], r.get("prev_close")),
            "expected_open_to_close_pct": r.get("expected_open_to_close_pct"),
            "realised_open_to_close_pct": _pct(px["close"], px["open"]),
            "expected_1000_pct": r.get("expected_1000_pct"),
            "realised_1000_pct": _pct(px.get("px_1000"), r.get("prev_close")),
            **open_lag_outcome(r, px),
        })
    res = {"generated_utc": _now_utc().isoformat(timespec="seconds"),
           "date": d.isoformat(), "rows": rows,
           "note": "Returns in % on the position's side from the 13:30 ET entry, "
                   "gross. A limit counts as filled only if the session traded a cent "
                   "through it; a touch at the limit is not a fill. action 'none' is "
                   "scored as the static rule."}
    _write(out / "morning-resolved.json", res)
    return res


def _mean_t(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    m = st.mean(xs)
    if len(xs) < 2:
        return {"n": 1, "mean": round(m, 3)}
    se = st.stdev(xs) / math.sqrt(len(xs))
    return {"n": len(xs), "mean": round(m, 3), "t": round(m / se, 2) if se else None}


def _rho(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if _num(x) and _num(y)]
    if len(pairs) < 5:
        return None
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for k, i in enumerate(o):
            r[i] = float(k)
        return r
    x, y = rk([p[0] for p in pairs]), rk([p[1] for p in pairs])
    mx, my = st.mean(x), st.mean(y)
    num = sum((i - mx) * (j - my) for i, j in zip(x, y))
    den = math.sqrt(sum((i - mx) ** 2 for i in x) * sum((j - my) ** 2 for j in y))
    return round(num / den, 3) if den else None


def pool(C):
    rows = []
    for f in sorted(glob.glob(str(REPO / "research" / "*" / "*" / "*" /
                                  C.get("output_dir", "morning") / "morning-resolved.json"))):
        for r in (_load(f) or {}).get("rows", []):
            if not r.get("pending"):
                rows.append(dict(r, date=Path(f).parent.parent.name))
    days = sorted({r["date"] for r in rows})
    res = {"generated_utc": _now_utc().isoformat(timespec="seconds"),
           "names": len(rows), "days": len(days),
           "review": _mean_t([r["recommended_return"] for r in rows]),
           "static_rule": _mean_t([r["static_return"] for r in rows]),
           "review_minus_static": _mean_t([r["review_minus_static"] for r in rows]),
           "always": {k: _mean_t([r["returns"].get(k) for r in rows])
                      for k in ("exit_open", "exit_1000", "exit_1300", "exit_close")},
           "by_action": {a: _mean_t([r["review_minus_static"] for r in rows
                                     if r["action"] == a])
                         for a in ACTIONS + ("none",)},
           "rho_expected_vs_realised_open": _rho(
               [r["expected_open_pct"] for r in rows], [r["realised_open_pct"] for r in rows]),
           "rho_expected_vs_realised_1000": _rho(
               [r.get("expected_1000_pct") for r in rows],
               [r.get("realised_1000_pct") for r in rows]),
           "brier_review_minus_prior": {
               k: _mean_t([r[f"brier_{k}"] - r[f"brier_{k}_prior"] for r in rows
                           if r.get(f"brier_{k}") is not None
                           and r.get(f"brier_{k}_prior") is not None])
               for k in ("p_open_lags", "p_fade_by_1000")},
           "rho_expected_vs_realised_open_to_close": _rho(
               [r["expected_open_to_close_pct"] for r in rows],
               [r["realised_open_to_close_pct"] for r in rows]),
           "note": "The review adds something only where review_minus_static is "
                   "positive with t >= 2 over many mornings. Names on one morning share "
                   "a market and are not independent. brier_review_minus_prior below "
                   "zero means the analysts' open-lag probabilities beat the measured "
                   "base rate."}
    _write(REPO / "researcher_us" / "analysis" / "morning-pool.json", res)
    return res


# ------------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("slot")
    for name in ("pick", "snapshot", "compile", "resolve"):
        sp = sub.add_parser(name)
        sp.add_argument("--date")
        if name == "snapshot":
            sp.add_argument("--final", action="store_true")
    sub.add_parser("pool")
    a = ap.parse_args()
    C = cfg()
    if a.cmd == "slot":
        res = slot(C)
    elif a.cmd == "pick":
        res = pick(_date_arg(a.date), C)
        for p in res["picks"]:
            print(f"  pick  {p['ticker']:<6} {p['session']} {p['position']:<5} "
                  f"panel_pct {p['panel_pct']:.1f}")
        for e in res["excluded"]:
            print(f"  skip  {e['ticker']:<6} {e['reason']}")
    elif a.cmd == "snapshot":
        res = snapshot(_date_arg(a.date), C, final=a.final)
        for t, s in res["names"].items():
            print(f"  {t:<6} prev {s['prev_close']}  pm {s['premarket_last']} "
                  f"({s['premarket_pct_vs_prev_close']}%) at {s['premarket_time_et']}  "
                  f"entry {s['entry_px']}  position {s['position_return_so_far_pct']}%")
        res = {"as_of_et": res["as_of_et"], "market": res["market"]}
    elif a.cmd == "compile":
        res = compile_advice(_date_arg(a.date), C)
        print((REPO / paths(_date_arg(a.date), C)[2] / "morning-note.md").read_text())
        return 0
    elif a.cmd == "resolve":
        res = resolve(_date_arg(a.date), C)
    else:
        res = pool(C)
    print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
