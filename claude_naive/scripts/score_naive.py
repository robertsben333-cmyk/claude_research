#!/usr/bin/env python3
"""Score claude_naive forecasts against the realised move, under the backtest's scheme.

Buy 14:00 ET (20:00 CET) on the last session before the print -- the event date for
`amc`, the prior trading day for `bmo`. Exit next open (primary) or next close.
Long on Up, short on Down, flat on Neutral.

Every rate is reported beside its floor. A hit rate alone is the mistake the main
LEDGER.md made: 58% over 31 calls with nothing to compare it to, so nobody could say
whether the pipeline knew anything.

Floors carried over from the pilot-40 backtest:

    always_down      55%       (that sample skewed down; recomputed here per batch)
    last_reaction    62%       free, reads nothing -- the real bar
    coin             50%, and the interval is wide at these sample sizes
    proxy magnitude  3.64pp median error over the same 37 events

Both magnitude numbers are scored. `expected_abs_move_pct` is the model's honest
estimate; `expected_abs_move_pct_scaled` applies the backtest's under-scaling
correction. Scoring both is the only way to learn whether that correction generalises
or was an artefact of 37 events -- seven of whose eight largest moves came in
under-forecast, several by half.
"""
import argparse, json, statistics, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "backtest" / "scripts"))

CALL_SIGN = {"Strong Up": 1, "Lean Up": 1, "Neutral / No Edge": 0,
             "Lean Down": -1, "Strong Down": -1}


def load_truth(ticker, event_date, session):
    from truth import move
    return move(ticker, event_date, session)


def load_trade(ticker, event_date, session):
    from trade_prices import compute
    r = compute(ticker, event_date, session)
    if r.get("error"):
        r2 = compute(ticker, event_date, session, "60m", "3mo")
        if not r2.get("error"):
            r2["fallback_reason"] = r["error"]
            return r2
    return r


def score_day(date):
    d = ROOT / date
    fp = d / "forecasts.json"
    if not fp.exists():
        sys.exit(f"no forecasts at {fp}")
    rows = json.loads(fp.read_text(encoding="utf-8"))
    scored = []
    for r in rows:
        t, ed, sess = r["ticker"], r.get("event_date"), r.get("session")
        if not (ed and sess):
            scored.append(r | {"outcome_status": "skipped: no event_date/session"})
            continue
        tr = load_truth(t, ed, sess)
        px = load_trade(t, ed, sess)
        time.sleep(0.3)
        if tr.get("error"):
            scored.append(r | {"outcome_status": f"pending: {tr['error']}"})
            continue
        mv = tr["actual_move_pct"]
        s = CALL_SIGN.get(r.get("call"))
        rec = r | {
            "actual_move_pct": mv,
            "direction_hit": None if s in (None, 0) else ((s > 0) == (mv > 0)),
            "abs_error_raw": abs((r.get("expected_abs_move_pct") or 0) - abs(mv)),
            "abs_error_scaled": abs((r.get("expected_abs_move_pct_scaled")
                                     or r.get("expected_abs_move_pct") or 0) - abs(mv)),
            "outcome_status": "scored",
        }
        if not px.get("error"):
            rec |= {"ret_to_open_pct": px["ret_to_open_pct"],
                    "ret_to_close_pct": px["ret_to_close_pct"],
                    "entry_1400et": px["entry_1400et"],
                    "trade_ret_open": None if not s else s * px["ret_to_open_pct"],
                    "trade_ret_close": None if not s else s * px["ret_to_close_pct"]}
        else:
            rec["trade_price_error"] = px["error"]
        scored.append(rec)
    (d / "scored.json").write_text(json.dumps(scored, indent=1), encoding="utf-8")
    return scored


def report(scored, date):
    done = [r for r in scored if r.get("outcome_status") == "scored"]
    if not done:
        print("nothing scored yet")
        return ""
    dirs = [r for r in done if r["direction_hit"] is not None]
    hits = sum(1 for r in dirs if r["direction_hit"])
    ups = sum(1 for r in done if r["actual_move_pct"] > 0)
    rets = [r["trade_ret_open"] for r in done if r.get("trade_ret_open") is not None]
    retc = [r["trade_ret_close"] for r in done if r.get("trade_ret_close") is not None]
    # floors on THIS batch, not borrowed from the backtest
    ad = statistics.mean(-r["ret_to_open_pct"] for r in done if "ret_to_open_pct" in r) \
        if any("ret_to_open_pct" in r for r in done) else None
    raw = statistics.median(r["abs_error_raw"] for r in done)
    sca = statistics.median(r["abs_error_scaled"] for r in done)

    L = []
    L.append(f"\n## {date}\n")
    L.append(f"- events forecast: {len(scored)}, scored: {len(done)}, "
             f"directional: {len(dirs)}, neutral: {len(done)-len(dirs)}")
    L.append(f"- realised: {ups}/{len(done)} up, median |move| "
             f"{statistics.median(abs(r['actual_move_pct']) for r in done):.2f}%")
    if dirs:
        L.append(f"- **direction {hits}/{len(dirs)} ({hits/len(dirs):.0%})** "
                 f"— floor: the free last-reaction rule scored 62% over the backtest's 37")
    if rets:
        L.append(f"- **return per trade, exit open: {statistics.mean(rets):+.2f}%** "
                 f"(total {sum(rets):+.1f}%)"
                 + (f" — always_down on the same events: {ad:+.2f}%" if ad is not None else ""))
    if retc:
        L.append(f"- return per trade, exit close: {statistics.mean(retc):+.2f}% "
                 f"(total {sum(retc):+.1f}%)")
    L.append(f"- magnitude median error: **raw {raw:.2f}pp vs scaled {sca:.2f}pp** "
             f"— the backtest's proxy floor was 3.64pp")
    better = "scaled" if sca < raw else "raw"
    L.append(f"  - the {better} number is closer on this batch"
             + ("; the under-scaling correction is holding so far"
                if better == "scaled" else
                "; the correction is not helping here"))
    L.append("")
    L.append(f"| ticker | call | pred | scaled | actual | dir | open | close |")
    L.append(f"| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(done, key=lambda x: -abs(x["actual_move_pct"])):
        h = "-" if r["direction_hit"] is None else ("hit" if r["direction_hit"] else "miss")
        ro = r.get("trade_ret_open")
        rc = r.get("trade_ret_close")
        L.append(f"| {r['ticker']} | {r['call'].replace(' / No Edge','')} | "
                 f"{r.get('expected_abs_move_pct',0):.1f} | "
                 f"{r.get('expected_abs_move_pct_scaled', r.get('expected_abs_move_pct',0)):.1f} | "
                 f"{r['actual_move_pct']:+.2f} | {h} | "
                 f"{('' if ro is None else f'{ro:+.2f}')} | "
                 f"{('' if rc is None else f'{rc:+.2f}')} |")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    a = ap.parse_args()
    scored = score_day(a.date)
    block = report(scored, a.date)
    print(block)
    led = ROOT / "LEDGER.md"
    head = ("# claude_naive — forecast ledger\n\n"
            "Arm A of the pilot-40 backtest, run live. Every rate carries its floor.\n\n"
            "Scheme: buy 14:00 ET (20:00 CET) the last session before the print, "
            "exit next open (primary) or next close. Long on Up, short on Down, "
            "flat on Neutral.\n\n"
            "Backtest reference points, over 37 events: direction 72%, "
            "+0.90%/trade at the open, +2.16% at the close, magnitude median error "
            "3.35pp against a 3.64pp proxy. Those had 18 directional calls behind them "
            "and were called a lead, not a finding.\n")
    if not led.exists():
        led.write_text(head, encoding="utf-8")
    with led.open("a", encoding="utf-8") as f:
        f.write(block + "\n")
    print(f"\nappended to {led}")


if __name__ == "__main__":
    main()
