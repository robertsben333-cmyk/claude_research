#!/usr/bin/env python3
"""Stage E-P shadow juror: SubQ Snap, a non-Anthropic model, asked about the panel's packs.

    python3 researcher_us/scripts/snap_juror.py --run <RUN>/edge-panel [--dry-run]
                                                 [--out <DIR>] [--repeat | --no-repeat]

Why it exists (researcher_us/SNAP_JUROR_HANDOFF.md): the E-P panel counts agreement
between four members as independent confirmation, and all four are Anthropic models
whose errors are probably correlated. Snap is a decision model from another lab on
another architecture. It answers declared questions over declared answers and returns a
probability for every answer.

IT IS A SHADOW COLUMN, NOT A MEMBER. It writes `edge-scores-snap.json`, which
`edge_resolve.py` ranks beside the panel as `spearman_snap`. Nothing that selects, sizes
or trades reads it: `alpaca_trade.py`, `edge_score.py` and `panel_score.py` must not
mention this file and the smoke test checks that. Promotion is the operator's call,
after it has pooled.

Per pack, one request with three questions:

- `move` (choice): where the move over the window lands, 24 bins from
  `snap_juror.bin_edges_inner` in config/pipeline.yaml. Derived: `snap_impact` = E[move]
  (bin midpoints, tails at `tail_values`), `snap_p_up` = 100 x P(move > 0), `snap_abs` =
  E[|move|]. `snap_impact` is the one pre-registered number; it is on the footing of a
  judge's impact_sum, (2 p_up/100 - 1) x abs_move_pct.
- `up` (noul): closes the window above the entry. A cross-check on `move`; logged only.
- `vs_implied` (score): |move| against the sealed implied move, five levels. Logged only.

NEVER FATAL. No key, host denied, a 4xx, a pack over the limit: the files are still
written, with `status` and `reason` per name, and the exit code is 0, so the stage run
carries on. The key is read from SUBQ_API_KEY and never written anywhere; without it
nothing is sent and every name is `no_key`. The first auth, credit, permission or
egress failure stops the remaining calls, because every pack would fail the same way.

FORWARD ONLY. A run sealed before `release_date` (2026-10-12, the model's public
release) is refused: the model's training may hold those outcomes. A run scored after
its seal day, but sealed on or after the release, is `basis: retro_post_release`; one
scored on its seal day is `forward`. Never pool the two.

The model id `subq-snap-preview` is a preview alias and can move underneath us, as
`opus` did on 2026-09-22. The `model` string the API returns is recorded on every call;
two different strings are two versions and are never pooled.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# Bump with any change to the preamble, the questions or the derivation: it is the
# version of what Snap is asked, and runs on two versions are not pooled.
SCRIPT_VERSION = "snap.v1"

PREAMBLE = (
    "You are judging one US-listed company that reports quarterly earnings in the window "
    "below. The pack holds a sealed baseline (prices, the option-implied move, the "
    "company's past earnings reactions) and research evidence collected before the "
    "print. The window: entry at the regular-session close before the earnings release, "
    "exit at the regular-session close after the first full trading session that follows "
    "the release. For a 'bmo' release (before the open on event_date) that is the close "
    "of the session before event_date to the close of event_date; for an 'amc' release "
    "(after the close on event_date) it is the close of event_date to the close of the "
    "next session. Moves are in percent of the entry price. Answer only from the pack.")

# Keys of a pack that name files Snap cannot open.
DROP_KEYS = ("hunter_definition", "lessons_file")

VS_IMPLIED_LEVELS = [
    "well under half of the implied move (|move| < 0.5x implied)",
    "under the implied move (0.5x to 0.8x)",
    "about the implied move (0.8x to 1.2x)",
    "over the implied move (1.2x to 1.5x)",
    "well over the implied move (|move| > 1.5x implied)",
]

FATAL_FOR_ALL = {"no_key", "bad_key", "no_credits", "model_forbidden", "host_denied"}


# ---------------------------------------------------------------------------- config
def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / "config" / "pipeline.yaml", encoding="utf-8"))
    s = c.get("snap_juror") or {}
    if not s:
        raise RuntimeError("config/pipeline.yaml has no snap_juror block")
    return s


def bins(c):
    """The 24 bins as (name, description, lo, hi, representative value)."""
    inner = [float(x) for x in c["bin_edges_inner"]]
    lo_tail, hi_tail = (float(x) for x in c["tail_values"])
    edges = [float("-inf")] + inner + [float("inf")]
    out = []

    def f(x):
        return f"{abs(x):g}"

    for lo, hi in zip(edges, edges[1:]):
        if lo == float("-inf"):
            name, desc, mid = f"falls_more_than_{f(hi)}pct", f"falls more than {f(hi)}%", lo_tail
        elif hi == float("inf"):
            name, desc, mid = f"rises_more_than_{f(lo)}pct", f"rises more than {f(lo)}%", hi_tail
        elif hi <= 0:
            name = f"falls_{f(hi)}_to_{f(lo)}pct"
            desc = f"falls between {f(hi)}% and {f(lo)}%"
            mid = (lo + hi) / 2
        else:
            name = f"rises_{f(lo)}_to_{f(hi)}pct"
            desc = f"rises between {f(lo)}% and {f(hi)}%"
            mid = (lo + hi) / 2
        out.append({"name": name, "description": desc, "lo": lo, "hi": hi, "value": mid})
    return out


# --------------------------------------------------------------------------- request
def state_of(pack):
    return {"instructions_for_reading": PREAMBLE,
            "pack": {k: v for k, v in pack.items() if k not in DROP_KEYS}}


def questions(b):
    return {
        "move": {
            "type": "choice",
            "instructions": ("Where does the stock's move over the window land? Choose the "
                             "range that holds the close-to-close move in percent."),
            "criteria": {x["name"]: x["description"] for x in b},
        },
        "up": {
            "type": "noul",
            "instructions": ("Will the stock close the window above the entry price "
                             "(a positive close-to-close move)?"),
        },
        "vs_implied": {
            "type": "score",
            "instructions": ("How large is the absolute move over the window against the "
                             "sealed option-implied move (baseline.options."
                             "event_implied_move_pct, or baseline.expected_move_pct when "
                             "there is no straddle)?"),
            "criteria": VS_IMPLIED_LEVELS,
        },
    }


def body_of(pack, c, b):
    return {"model": c["model"], "state": state_of(pack), "questions": questions(b)}


def sha(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest()


def classify(code, raw):
    """(status, reason) for an HTTP failure. A 403 carrying JSON `detail` is the key;
    a 403 with an HTML body is the egress policy refusing the host."""
    detail = None
    try:
        detail = (json.loads(raw) or {}).get("detail")
    except Exception:
        pass
    msg = (detail.get("message") if isinstance(detail, dict) else detail) or raw[:200]
    etype = detail.get("error_type") if isinstance(detail, dict) else None
    if code == 401:
        return "bad_key", f"401 {etype or ''}: {msg}"[:300]
    if code == 402:
        return "no_credits", f"402: {msg}"[:300]
    if code == 403:
        if detail is None:
            return "host_denied", f"403 without a JSON detail (egress policy): {raw[:120]}"
        return "model_forbidden", f"403 {etype or ''}: {msg}"[:300]
    if code == 400:
        return "rejected", f"400 {etype or ''}: {msg}"[:300]
    if code == 422:
        return "invalid_request", f"422 {etype or ''}: {msg}"[:300]
    if code == 429:
        return "rate_limited", f"429: {msg}"[:300]
    return "api_error", f"HTTP {code}: {msg}"[:300]


def post(body, c, key, opener=None):
    """One call with the configured retries. Returns (response or None, status, reason,
    attempts). Retries only 429, 5xx and network errors; never another 4xx."""
    url = f"https://{c['host']}{c['path']}"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    backoff = [float(x) for x in c.get("backoff_s", [2, 4])]
    tries = int(c.get("retries", 2)) + 1
    status, reason = "api_error", "not attempted"
    for i in range(tries):
        req = urllib.request.Request(url, data=data, method="POST", headers=headers)
        try:
            with (opener or urllib.request.urlopen)(req, timeout=float(c["timeout_s"])) as r:
                return json.loads(r.read().decode("utf-8")), "ok", None, i + 1
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace")
            status, reason = classify(e.code, raw)
            if not (e.code == 429 or e.code >= 500):
                return None, status, reason, i + 1
        except urllib.error.URLError as e:
            text = str(getattr(e, "reason", e))
            if "403" in text or "407" in text:                 # proxy refused the CONNECT
                return None, "host_denied", f"egress policy: {text[:200]}", i + 1
            status, reason = "unreachable", f"{type(e).__name__}: {text[:200]}"
        except Exception as e:                                  # TLS, timeout, bad JSON
            status, reason = "unreachable", f"{type(e).__name__}: {str(e)[:200]}"
        if i + 1 < tries:
            time.sleep(backoff[min(i, len(backoff) - 1)])
    return None, status, reason, tries


# ------------------------------------------------------------------------- the answer
def _probs(ans, names):
    """A choice/score answer's probabilities as a list aligned with `names`, whether the
    API returns them keyed by name or as a list."""
    p = (ans or {}).get("probabilities")
    if isinstance(p, dict):
        v = [float(p.get(n, 0.0) or 0.0) for n in names]
    elif isinstance(p, list) and len(p) == len(names):
        v = [float(x or 0.0) for x in p]
    else:
        return None
    s = sum(v)
    return [x / s for x in v] if s > 0 else None


def derive(resp, b):
    """The per-name numbers from one response. Raises ValueError if `move` is unusable."""
    answers = (resp or {}).get("answers") or {}
    mv = answers.get("move") or {}
    p = _probs(mv, [x["name"] for x in b])
    if p is None:
        raise ValueError("no usable probabilities on `move`")
    impact = sum(pi * x["value"] for pi, x in zip(p, b))
    p_up = 100.0 * sum(pi for pi, x in zip(p, b) if x["lo"] >= 0)
    absm = sum(pi * abs(x["value"]) for pi, x in zip(p, b))
    up = answers.get("up")
    p_up_noul = (up.get("noul") if isinstance(up, dict) else up)
    p_up_noul = None if p_up_noul is None else 100.0 * float(p_up_noul)
    vi = answers.get("vs_implied") or {}
    return {
        "snap_impact": round(impact, 3),
        "snap_p_up": round(p_up, 2),
        "snap_abs": round(absm, 3),
        "snap_vs_implied": vi.get("score"),
        "confidence_move": mv.get("confidence"),
        "move_choice": mv.get("choice"),
        "p_up_noul": None if p_up_noul is None else round(p_up_noul, 2),
        "p_up_disagreement": (None if p_up_noul is None
                              else round(p_up_noul - p_up, 2)),
    }


# ---------------------------------------------------------------------------- the run
def run_date(run, packs):
    for p in packs:
        parts = str(p.get("id", "")).split("/")
        if len(parts) >= 3:
            return parts[1]
    for part in reversed(Path(run).resolve().parts):
        if len(part) == 10 and part[4] == "-" and part[7] == "-":
            return part
    return None


def first_live_day(run_dir, date):
    """True when no earlier E-P run carries a Snap file with a live answer, so this is the
    day to call every pack twice and record whether the answers repeat."""
    for f in (REPO / "research").glob("*/*/*/edge-panel/edge-scores-snap.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("date") and d["date"] < date and d.get("n_ok", 0) > 0:
            return False
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", required=True, help="<RUN>/edge-panel")
    ap.add_argument("--out", help="write here instead of the run directory (plumbing runs)")
    ap.add_argument("--dry-run", action="store_true", help="build the requests, call nothing")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--repeat", dest="repeat", action="store_true", default=None,
                   help="call each pack twice (default: only on the first live day)")
    g.add_argument("--no-repeat", dest="repeat", action="store_false")
    a = ap.parse_args()

    c = cfg()
    b = bins(c)
    run = Path(a.run)
    out = Path(a.out) if a.out else run
    (out / "panel").mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    packs_path = run / "panel" / "packs.json"
    packs = json.loads(packs_path.read_text(encoding="utf-8")) if packs_path.exists() else []
    date = run_date(run, packs)
    release = str(c["release_date"])
    # Forward means asked no later than the seal day, before any outcome exists.
    basis = ("refused_pre_release" if date and date < release
             else "retro_post_release" if date and date < now[:10]
             else "forward")
    key = os.environ.get("SUBQ_API_KEY") or None

    stop = None
    if not c.get("enabled", False):
        stop = ("disabled", "snap_juror.enabled is false in config/pipeline.yaml")
    elif not packs:
        stop = ("no_packs", f"{packs_path} missing or empty")
    elif basis == "refused_pre_release":
        stop = ("refused_pre_release",
                f"run dated {date} is before the model's release {release}; its training "
                "may hold the outcome")
    elif a.dry_run:
        stop = ("dry_run", "--dry-run: requests built, nothing sent")
    elif not key:
        stop = ("no_key", "SUBQ_API_KEY is not set in this session's environment")
    repeat = (a.repeat if a.repeat is not None
              else (stop is None and basis == "forward" and first_live_day(run, date)))

    raw, rows, models, tokens = [], [], set(), 0
    for p in packs:
        t = (p.get("baseline") or {}).get("ticker") or str(p.get("id", "")).split("/")[-1]
        body = body_of(p, c, b)
        rec = {"id": p.get("id"), "ticker": t, "request_sha256": sha(body),
               "request_bytes": len(json.dumps(body, ensure_ascii=False).encode("utf-8"))}
        row = {"ticker": t, "status": None, "reason": None, "snap_impact": None,
               "snap_p_up": None, "snap_abs": None, "snap_vs_implied": None,
               "confidence_move": None, "p_up_noul": None}
        if stop:
            row["status"], row["reason"] = stop
        else:
            resp, st, why, n = post(body, c, key)
            rec.update({"called_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "attempts": n, "status": st, "reason": why, "response": resp})
            row["status"], row["reason"] = st, why
            if resp is not None:
                models.add(resp.get("model"))
                tokens += int(((resp.get("usage") or {}).get("input_tokens")) or 0)
                row["model_returned"] = resp.get("model")
                try:
                    row.update(derive(resp, b))
                except ValueError as e:
                    row["status"], row["reason"] = "unparsed", str(e)
                if repeat and row["status"] == "ok":
                    resp2, st2, why2, _ = post(body, c, key)
                    rec["repeat"] = {"status": st2, "reason": why2, "response": resp2}
                    if resp2 is not None:
                        tokens += int(((resp2.get("usage") or {}).get("input_tokens")) or 0)
                        a1 = (resp or {}).get("answers")
                        a2 = (resp2 or {}).get("answers")
                        row["repeat_identical"] = a1 == a2
                        try:
                            row["repeat_snap_impact"] = derive(resp2, b)["snap_impact"]
                        except ValueError:
                            pass
            if st in FATAL_FOR_ALL:
                stop = (st, f"stopped after the first call: {why}")
        raw.append(rec)
        rows.append(row)

    ok = [r for r in rows if r["status"] == "ok"]
    status = ("ok" if ok and len(ok) == len(rows) else "partial" if ok
              else (rows[0]["status"] if rows else (stop or ("no_packs",))[0]))
    reason = None if status == "ok" else next((r["reason"] for r in rows if r["reason"]),
                                              stop[1] if stop else None)
    head = {"generated_utc": now, "date": date, "run": str(run),
            "script_version": SCRIPT_VERSION, "model_requested": c["model"],
            "models_returned": sorted(m for m in models if m),
            "basis": basis, "status": status, "reason": reason,
            "key_in_env": bool(key), "repeat_called": bool(repeat),
            "input_tokens": tokens,
            "cost_usd": round(tokens * float(c["usd_per_m_input_tokens"]) / 1e6, 6),
            "places_orders": False, "reads_into_selection": False}
    (out / "panel" / "snap.json").write_text(
        json.dumps({**head, "preamble": PREAMBLE, "bins": b, "calls": raw},
                   indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    ranked = sorted(ok, key=lambda r: -r["snap_impact"])
    scores = {**head, "ranking_key": "snap_impact", "n": len(rows), "n_ok": len(ok),
              "note": ("Shadow column. Ranked beside the panel by edge_resolve.py as "
                       "spearman_snap; nothing that selects, sizes or trades reads it."),
              "ranking_by_ticker": rows}
    (out / "edge-scores-snap.json").write_text(
        json.dumps(scores, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    prov = out / "provenance.json"
    if prov.exists():
        d = json.loads(prov.read_text(encoding="utf-8"))
        d.setdefault("panel", {})["snap"] = {
            "role": "shadow juror, not a member", "model_requested": c["model"],
            "models_returned": head["models_returned"], "script_version": SCRIPT_VERSION,
            "status": status, "reason": reason, "basis": basis, "n_ok": len(ok),
            "n": len(rows), "recorded_utc": now}
        prov.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # One line for the note, under the panel table.
    if ranked:
        top, bot = ranked[0], ranked[-1]
        line = (f"Snap (shadow juror, {', '.join(head['models_returned']) or c['model']}, "
                f"not in the panel): top {top['ticker']} {top['snap_impact']:+.2f}, "
                f"bottom {bot['ticker']} {bot['snap_impact']:+.2f} "
                f"({len(ok)} of {len(rows)} names answered).")
    else:
        line = f"Snap (shadow juror) did not run: {status} - {reason}."
    print(line)
    print(f"wrote {out / 'edge-scores-snap.json'} and {out / 'panel' / 'snap.json'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:                       # never fatal to the stage run
        print(f"snap_juror: {type(e).__name__}: {e} (stage carries on)", file=sys.stderr)
        sys.exit(0)
