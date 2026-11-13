"""Rows for the 'where does the US edge work' analysis: one row per resolved stage E-P
name, from dashboard/data/ledger.json (names_panel) plus each name's sealed baseline.
Return = the operator's window (in 13:30 ET, amc out at next open, bmo out 13:00 ET),
gross, on the panel's side. Run: python3 research/analyses/us-edge-where/build.py"""
import json, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
src = sys.argv[1] if len(sys.argv) > 1 else ROOT / "dashboard/data/ledger.json"
L = json.load(open(src))
names = L.get("names_panel") or [r for r in L["names"] if r.get("stage") == "E-P"]
rows = []
for r in names:
    if r.get("duplicate_event") or r.get("ret_strategy") is None:
        continue
    b = {}
    bf = ROOT / r["run"] / "baselines" / f"{r['ticker']}.json"
    if bf.exists():
        b = json.load(open(bf))
    tape, opt = b.get("tape") or {}, b.get("options") or {}
    hist = b.get("history") or {}
    side = 1 if r["impact_sum"] > 0 else -1
    lean = r.get("priced_lean_pct")
    rows.append({
        "version": r["prompt_version"], "run_date": r["run_date"], "ticker": r["ticker"],
        "session": r["session"], "event_date": r["event_date"],
        "weekday": datetime.date.fromisoformat(r["run_date"]).strftime("%a"),
        "pct": r["panel_pct"], "side": side, "signed": r["impact_sum"],
        "sd": r.get("panel_pct_sd"), "members": r.get("panel_members_pct"),
        "searcher_sum": r.get("searcher_impact_sum"), "n_findings": r.get("n_findings"),
        "move": r["mv_strategy"], "ret": r["ret_strategy"], "ret_close": r.get("ret_close"),
        "sector": r.get("sector"), "industry": r.get("industry"),
        "mcap": r.get("market_cap_usd"), "adv": r.get("dollar_vol"),
        "spot": r.get("spot") or tape.get("spot"),
        "retail_tilt": r.get("retail_tilt"), "vol20": r.get("realised_vol_20d"),
        "runup_20d": tape.get("run_up_20d_pct"), "runup_5d": tape.get("run_up_5d_pct"),
        "from_high": tape.get("pct_from_52w_high"),
        "lean": lean, "lean_agree": (None if not lean else (lean > 0) == (side > 0)),
        "opt_ok": opt.get("status") == "ok", "implied": opt.get("event_implied_move_pct"),
        "skew": opt.get("skew_25d_vol_points"),
        "expected_move": b.get("expected_move_pct"),
        "hist_med": hist.get("median_abs_move_pct"), "hist_n": hist.get("n"),
        "hist_up": (hist.get("up_count") / hist["n"] if hist.get("n") else None),
        "shortable": r.get("shortable"), "search_state": r.get("search_state")})
out = Path(__file__).with_name("rows.json")
out.write_text(json.dumps(rows, indent=0))
import collections
print(len(rows), collections.Counter(x["version"] for x in rows))
