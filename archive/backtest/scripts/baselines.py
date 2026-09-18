#!/usr/bin/env python3
"""Model-free baselines. Every arm is read against these, never alone.

LEDGER.md reports a 58% direction hit rate over 31 calls with no floor beside it,
which is why nobody can say whether the pipeline knows anything. A hit rate is
meaningless without the number a coin would have scored on the same events, and on
a 40-event sample the coin is noisy enough to beat 58% about a third of the time.

Baselines:

  always_up        every event called up. Equities drift up; this is the one a
                   naive model accidentally implements and then feels clever about.
  always_down      the mirror, included so the drift is visible rather than assumed.
  always_neutral   scored under the ledger's own convention: a Neutral call hits
                   when the realised move came in below the expected move.
  coin             fair coin, 20,000 draws, reported as mean and 5-95 interval --
                   the interval is the part that matters.
  momentum         sign of the 20-day run-up into the print.
  reversal         the opposite. Included because if momentum works, this must fail
                   by the same margin, and if both look good the metric is broken.
  last_reaction    sign of the previous quarter's reaction to the same company.
  proxy_size       size-only: was the realised move above or below the median of the
                   last eight reactions? Direction is not attempted.

The size baseline exists because the archive already says direction is the weakest
thing this pipeline produces and size is the answerable question. An arm that beats
the coin on direction but cannot beat proxy_size on magnitude has not earned much.
"""
import json, random, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT


def _band(cap):
    return "large" if cap >= 50e9 else "mid" if cap >= 10e9 else "small"


def load(run="pilot-40"):
    draw = json.loads((ROOT / "runs" / run / "draw.json").read_text(encoding="utf-8"))
    out = []
    for e in draw["events"]:
        key = f"{e['ticker']}-{e['event_date']}"
        tp, ap = ROOT / "truth" / f"{key}.json", ROOT / "events" / key / "anchors.json"
        if not (tp.exists() and ap.exists()):
            continue
        t, a = json.loads(tp.read_text(encoding="utf-8")), json.loads(ap.read_text(encoding="utf-8"))
        mv = t.get("actual_move_pct")
        if mv is None:
            continue
        hist = [h["move_pct"] for h in a.get("historical_earnings_moves", [])]
        out.append({
            "ticker": e["ticker"], "key": key, "move": mv, "abs": abs(mv),
            "run_up_20d": a.get("run_up_20d_pct"), "run_up_5d": a.get("run_up_5d_pct"),
            "last_reaction": hist[0] if hist else None,
            "median_hist_abs": statistics.median([abs(h) for h in hist]) if hist else None,
            # the draw records the cap, not the band; derive it here so the
            # stratified view cannot silently come back empty
            "cap_band": e.get("cap_band") or _band(e.get("market_cap_usd_today") or 0),
        })
    return out


def rate(hits, n):
    return None if not n else hits / n


def directional(evs, pick):
    """pick(e) -> +1 / -1 / None. None abstains and is excluded from the rate."""
    n = hits = 0
    for e in evs:
        s = pick(e)
        if s is None or e["move"] == 0:
            continue
        n += 1
        hits += (s > 0) == (e["move"] > 0)
    return hits, n


def report(evs):
    print(f"n = {len(evs)} events with a realised move\n")
    up = sum(1 for e in evs if e["move"] > 0)
    print(f"base rate: {up}/{len(evs)} moved up ({up/len(evs):.0%}), "
          f"median |move| {statistics.median(e['abs'] for e in evs):.2f}%, "
          f"mean move {statistics.mean(e['move'] for e in evs):+.2f}%\n")

    rows = []
    for name, fn in [
        ("always_up", lambda e: 1),
        ("always_down", lambda e: -1),
        ("momentum_20d", lambda e: None if e["run_up_20d"] is None else (1 if e["run_up_20d"] > 0 else -1)),
        ("reversal_20d", lambda e: None if e["run_up_20d"] is None else (-1 if e["run_up_20d"] > 0 else 1)),
        ("momentum_5d", lambda e: None if e["run_up_5d"] is None else (1 if e["run_up_5d"] > 0 else -1)),
        ("last_reaction", lambda e: None if e["last_reaction"] is None else (1 if e["last_reaction"] > 0 else -1)),
    ]:
        h, n = directional(evs, fn)
        rows.append((name, h, n, rate(h, n)))

    random.seed(7)
    trials = [sum(random.choice([True, False]) for _ in evs) / len(evs) for _ in range(20000)]
    trials.sort()
    coin_lo, coin_hi = trials[int(0.05 * len(trials))], trials[int(0.95 * len(trials))]

    print(f"{'DIRECTION baseline':<18}{'hits':>6}{'n':>5}{'rate':>8}")
    print("-" * 37)
    for name, h, n, r in rows:
        print(f"{name:<18}{h:6}{n:5}{(f'{r:.0%}' if r is not None else '  n/a'):>8}")
    print(f"{'coin (20k draws)':<18}{'':6}{len(evs):5}{statistics.mean(trials):8.0%}")
    print(f"\ncoin 5-95 interval on n={len(evs)}: {coin_lo:.0%} - {coin_hi:.0%}")
    print(f"-> a direction rate inside that band is indistinguishable from chance.")
    print(f"   the live ledger's 58% would sit {'INSIDE' if coin_lo <= 0.58 <= coin_hi else 'outside'} it.\n")

    # Neutral under the ledger's convention, and the size question
    withhist = [e for e in evs if e["median_hist_abs"]]
    neutral_hits = sum(1 for e in withhist if e["abs"] < e["median_hist_abs"])
    print(f"{'SIZE baseline':<34}{'n':>5}{'rate':>8}")
    print("-" * 47)
    print(f"{'always_neutral (move < proxy)':<34}{len(withhist):5}{neutral_hits/len(withhist):8.0%}")
    print(f"{'move exceeded proxy expected size':<34}{len(withhist):5}"
          f"{1 - neutral_hits/len(withhist):8.0%}")
    err = [abs(e["abs"] - e["median_hist_abs"]) for e in withhist]
    print(f"\nproxy_size as a magnitude forecast: median abs error "
          f"{statistics.median(err):.2f}pp, mean {statistics.mean(err):.2f}pp")
    print(f"-> any arm's expected_abs_move_pct must beat {statistics.median(err):.2f}pp "
          f"median error to have added anything.\n")

    print("BY CAP BAND (results must be read within band, never pooled)")
    print(f"{'band':<8}{'n':>4}{'up%':>7}{'med |move|':>12}{'coin-beating room':>20}")
    for b in ("small", "mid", "large"):
        g = [e for e in evs if e["cap_band"] == b]
        if not g:
            continue
        u = sum(1 for e in g if e["move"] > 0)
        print(f"{b:<8}{len(g):4}{u/len(g):7.0%}{statistics.median(e['abs'] for e in g):11.2f}%"
              f"{'wide' if len(g) >= 20 else 'too small to resolve':>20}")


if __name__ == "__main__":
    evs = load(sys.argv[1] if len(sys.argv) > 1 else "pilot-40")
    report(evs)
    (ROOT / "runs" / "pilot-40" / "baselines.json").write_text(
        json.dumps({"n": len(evs), "events": evs}, indent=1), encoding="utf-8")
