#!/usr/bin/env python3
"""Place stage E's benchmark names as real orders at Alpaca, and close them again.

The stage emits one signed number per company, `impact_sum`, and no call. This
script is the only place in the repo that turns that number into a position, and
it does so through exactly one rule -- the one thing in `docs/EDGE_ANALYSIS.md`
that survived a family-wise correction:

    |impact_sum| >= conviction_floor   ->  long if positive, short if negative

Everything else here is plumbing and safety. The rule is 21 trades over 5
independent days (16/21 correct, +6.37% per trade, best-of-seven-thresholds
p=0.034). That is a lead, not an edge. Below the floor the sign of impact_sum is
a coin flip (53% over 38 events) and those names are never traded.

Two screens sit on top of the rule and both exist because the analysis found the
result would not have been reachable without them:

  capacity     six of the first 22 long/short positions traded under $1m a day and
               the best single trade in the sample turns over $170k. Names under
               `execution.benchmark.min_dollar_volume_usd` are dropped, not sized down.
  shortability Alpaca will reject a short in a name that is not `shortable`, and a
               rejected leg turns a market-neutral book into a naked long.

The window is the one `edge_resolve.py` scores, so the traded return and the
measured return are the same number:

    amc print   enter at the close ON the event date,     exit at the next close
    bmo print   enter at the close BEFORE the event date, exit at the event close

Entry and exit are both market-on-close, which is why this needs two invocations
on two different days. `open` runs on the entry date, `close` on the exit date;
both must land before Alpaca's 15:50 ET cutoff for MOC orders.

Nothing is submitted unless all four of these hold: `execution.enabled: true` in
config/pipeline.yaml, `--submit` on the command line, credentials in the
environment, and a paper endpoint (a live endpoint additionally needs
--live-account-i-understand). Without --submit every subcommand is a dry run that
prints and writes the plan and touches no order.

    export ALPACA_API_KEY_ID=... ALPACA_API_SECRET_KEY=...
    python3 scripts/alpaca_trade.py plan  --run research/2026/09/2026-09-09/edge
    python3 scripts/alpaca_trade.py open  --run research/2026/09/2026-09-09/edge --submit
    python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit
    python3 scripts/alpaca_trade.py status --run research/2026/09/2026-09-09/edge
"""
import argparse
import glob
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

PAPER = "https://paper-api.alpaca.markets"
CLIENT_PREFIX = "edge"          # every client_order_id this repo ever creates
MOC_CUTOFF_MIN = 10             # minutes before the close that MOC stops being accepted


# ---------------------------------------------------------------- config

def config():
    import yaml
    return yaml.safe_load((REPO / "config" / "pipeline.yaml").read_text(encoding="utf-8"))


def execution_config(cfg):
    """The `execution:` block, with the conviction floor inherited from stage E."""
    ex = dict(cfg.get("execution") or {})
    bench = dict(ex.get("benchmark") or {})
    if bench.get("min_conviction") is None:
        bench["min_conviction"] = float((cfg.get("edge_hunt") or {}).get("conviction_floor", 3.0))
    ex["benchmark"] = bench
    ex["sizing"] = dict(ex.get("sizing") or {})
    ex["orders"] = dict(ex.get("orders") or {})
    return ex


# ---------------------------------------------------------------- http

class Alpaca:
    """Thin REST client. Reads credentials from the environment, never from a file."""

    def __init__(self, base=None, key=None, secret=None):
        self.base = (base or os.environ.get("ALPACA_BASE_URL") or PAPER).rstrip("/")
        self.key = key or os.environ.get("ALPACA_API_KEY_ID") or ""
        self.secret = secret or os.environ.get("ALPACA_API_SECRET_KEY") or ""

    @property
    def usable(self):
        return bool(self.key and self.secret)

    @property
    def is_paper(self):
        return "paper-api" in self.base

    def call(self, method, path, body=None, timeout=30):
        url = f"{self.base}{path}"
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "APCA-API-KEY-ID": self.key,
            "APCA-API-SECRET-KEY": self.secret,
            "Content-Type": "application/json",
            "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode()
                return (json.loads(raw) if raw.strip() else {}), None
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace")
            try:
                msg = json.loads(raw).get("message", raw)
            except Exception:
                msg = raw
            return None, f"HTTP {e.code}: {str(msg)[:300]}"
        except Exception as e:                                    # network, TLS, timeout
            return None, f"{type(e).__name__}: {str(e)[:300]}"

    def account(self):
        return self.call("GET", "/v2/account")

    def clock(self):
        return self.call("GET", "/v2/clock")

    def calendar(self, start, end):
        return self.call("GET", f"/v2/calendar?start={start}&end={end}")

    def asset(self, sym):
        return self.call("GET", f"/v2/assets/{sym}")

    def position(self, sym):
        return self.call("GET", f"/v2/positions/{sym}")

    def orders(self, status="all", limit=200):
        return self.call("GET", f"/v2/orders?status={status}&limit={limit}&nested=false")

    def submit(self, order):
        return self.call("POST", "/v2/orders", order)


# ---------------------------------------------------------------- calendar

def trading_days_offline(around, span=20):
    """Fallback when there are no credentials: the pipeline's own calendar."""
    from get_earnings import is_trading_day
    d0 = date.fromisoformat(around) - timedelta(days=span)
    return [(d0 + timedelta(days=i)).isoformat()
            for i in range(2 * span) if is_trading_day(d0 + timedelta(days=i))]


def trading_days(api, around, span=20):
    """Sessions around a date, from Alpaca's calendar where possible.

    Returns (days, source). The offline fallback is US-holiday arithmetic and is
    marked as such in the plan, because a wrong session boundary moves the entry
    to the wrong close and silently changes what is being traded.
    """
    if api and api.usable:
        d = date.fromisoformat(around)
        cal, err = api.calendar((d - timedelta(days=span)).isoformat(),
                                (d + timedelta(days=span)).isoformat())
        if cal and not err:
            return [r["date"] for r in cal], "alpaca /v2/calendar"
    return trading_days_offline(around, span), "offline: get_earnings.is_trading_day"


def window(days, event_date, session):
    """The window edge_resolve.py scores: last close before the print, first after."""
    if session == "amc":
        before = [d for d in days if d <= event_date]
        after = [d for d in days if d > event_date]
    else:
        before = [d for d in days if d < event_date]
        after = [d for d in days if d >= event_date]
    if not before or not after:
        return None, None
    return before[-1], after[0]


# ---------------------------------------------------------------- selection

def load_run(run):
    run = Path(run)
    scores = json.loads((run / "edge-scores.json").read_text(encoding="utf-8"))
    baselines = {}
    for p in sorted((run / "baselines").glob("*.json")):
        try:
            baselines[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return scores, baselines


def select(scores, baselines, bench):
    """Apply the benchmark. Returns (taken, rejected), each a list of dicts.

    Pure: no network, no clock, no account. This is the function to test.
    """
    floor = float(bench["min_conviction"])
    min_dv = float(bench.get("min_dollar_volume_usd") or 0)
    key = bench.get("key", "impact_sum")
    taken, rejected = [], []

    for row in scores.get("ranking", []):
        t = row.get("ticker")
        val = row.get(key)
        b = baselines.get(t) or {}
        tape = b.get("tape") or {}
        spot, vol = tape.get("spot"), tape.get("avg_volume_20d")
        dv = (spot * vol) if (spot and vol) else None
        cand = {"ticker": t, "key": key, "value": val,
                "conviction": abs(val) if isinstance(val, (int, float)) else None,
                "side": None,
                "event_date": b.get("event_date") or scores.get("event_date"),
                "session": b.get("session"),
                "spot": spot, "spot_as_of": b.get("as_of_utc"),
                "avg_volume_20d": vol,
                "dollar_volume_usd": round(dv) if dv else None,
                "run_up_20d_pct": tape.get("run_up_20d_pct")}

        def drop(reason):
            rejected.append({**cand, "reason": reason})

        if bench.get("require_rankable", True) and not row.get("rankable", False):
            drop(f"not rankable: {row.get('not_rankable_because') or 'unstated'}")
        elif not isinstance(val, (int, float)):
            drop(f"no {key} on the row")
        elif abs(val) < floor:
            drop(f"below the conviction floor ({abs(val):.2f} < {floor:.2f})")
        elif not spot:
            drop("no spot in the sealed baseline")
        elif not b.get("session"):
            drop("no session in the sealed baseline")
        elif dv is None:
            drop("no 20-day volume, so capacity is unknown")
        elif dv < min_dv:
            drop(f"turnover ${dv/1e6:.2f}m below the ${min_dv/1e6:.1f}m floor")
        else:
            cand["side"] = "buy" if val > 0 else "sell"
            taken.append(cand)

    taken.sort(key=lambda c: -c["conviction"])
    cap = bench.get("max_positions")
    if cap and len(taken) > int(cap):
        for c in taken[int(cap):]:
            rejected.append({**c, "reason": f"outside the top {cap} by conviction"})
        taken = taken[:int(cap)]
    return taken, rejected


def size(taken, equity, sizing):
    """Equal weight, capped per name, with the leftover redistributed equally.

    Every name gets the same target: the gross budget split N ways. Nothing here
    reads the score -- a name with a `impact_sum` of 12 gets the same dollars as one
    at 3.1, because the key ranks and does not size (median absolute error 6-7 points
    against a realised standard deviation near 11).

    Two caps can cut a name below the equal share: `max_position_pct_of_equity`, and
    `max_position_pct_of_adv` if it is set. Whatever a capped name cannot take is
    redistributed equally over the names that are not yet capped, and the pass
    repeats until nothing moves. So the book deploys as much of the budget as the
    caps allow, and every uncapped name still holds the same amount as every other
    uncapped name. When every name is capped the budget is deliberately
    under-deployed -- at a 20% cap that is any day with fewer than five names.

    Share counts come off the sealed baseline's spot, taken hours before the close
    the order fills at, so the notional drifts with the day's move. That is
    deliberate: the alternative is an unsourced live quote.
    """
    if not taken:
        return [], []
    gross = equity * float(sizing.get("gross_exposure_pct_of_equity", 20)) / 100.0
    max_eq = equity * float(sizing.get("max_position_pct_of_equity", 4)) / 100.0
    adv_pct = sizing.get("max_position_pct_of_adv")
    min_usd = float(sizing.get("min_position_usd", 200))

    caps = [min(max_eq, (c["dollar_volume_usd"] * float(adv_pct) / 100.0
                         if adv_pct else float("inf")))
            for c in taken]
    alloc = [0.0] * len(taken)
    remaining, open_idx = gross, list(range(len(taken)))
    while open_idx:
        share = remaining / len(open_idx)
        hit = [i for i in open_idx if caps[i] <= share + 1e-9]
        if not hit:                     # nobody is capped: this split is final
            for i in open_idx:
                alloc[i] = share
            remaining = 0.0
            break
        for i in hit:
            alloc[i] = caps[i]
            remaining -= caps[i]
        open_idx = [i for i in open_idx if i not in hit]

    sized, dropped = [], []
    for i, c in enumerate(taken):
        target = alloc[i]
        qty = int(math.floor(target / c["spot"]))
        notional = qty * c["spot"]
        cap_adv = (c["dollar_volume_usd"] * float(adv_pct) / 100.0 if adv_pct else None)
        row = {**c, "target_notional_usd": round(target, 2), "qty": qty,
               "notional_at_spot_usd": round(notional, 2),
               "pct_of_equity": round(100 * notional / equity, 2) if equity else None,
               "pct_of_adv": (round(100 * notional / c["dollar_volume_usd"], 3)
                              if c["dollar_volume_usd"] else None),
               "cap_equity_usd": round(max_eq, 2),
               "cap_capacity_usd": (round(cap_adv, 2) if cap_adv else None),
               "binding_cap": ("equal share" if target < caps[i] - 1e-6 else
                               "capacity" if cap_adv is not None and cap_adv < max_eq
                               else "per-name %")}
        if qty < 1:
            dropped.append({**row, "reason": "sizes to less than one share"})
        elif notional < min_usd:
            dropped.append({**row, "reason": f"position ${notional:.0f} below the "
                                             f"${min_usd:.0f} minimum"})
        else:
            sized.append(row)
    return sized, dropped


# ---------------------------------------------------------------- plan

def build_plan(run, api, ex, equity_override=None):
    scores, baselines = load_run(run)
    bench, sizing = ex["benchmark"], ex["sizing"]
    taken, rejected = select(scores, baselines, bench)

    equity, equity_src, acct = None, None, None
    if equity_override:
        equity, equity_src = float(equity_override), "--equity"
    if api.usable:
        acct, err = api.account()
        if acct and equity is None:
            equity, equity_src = float(acct["equity"]), "alpaca /v2/account"
        elif not acct:
            print(f"  ! /v2/account: {err}", file=sys.stderr)
    if equity is None:
        equity = ex.get("assumed_equity_usd")
        equity_src = "config execution.assumed_equity_usd"
    if not equity:
        sys.exit("no equity: give --equity, set execution.assumed_equity_usd, or "
                 "export ALPACA_API_KEY_ID / ALPACA_API_SECRET_KEY")

    # Dates, and the asset checks that decide whether a leg can be placed at all.
    cal_src, cal_cache = None, {}
    for c in taken:
        if c["event_date"] not in cal_cache:
            cal_cache[c["event_date"]] = trading_days(api, c["event_date"])
        days, cal_src = cal_cache[c["event_date"]]
        c["entry_date"], c["exit_date"] = window(days, c["event_date"], c["session"])
        c["asset_checked"] = False
        c["shortable"] = None
        if api.usable:
            a, err = api.asset(c["ticker"])
            if a:
                c["asset_checked"] = True
                c["tradable"] = a.get("tradable")
                c["shortable"] = a.get("shortable")
                c["easy_to_borrow"] = a.get("easy_to_borrow")
            else:
                c["asset_error"] = err

    # Whether the entry close is still ahead. Every name in a run shares it: an amc
    # print carries the run's own date, a bmo print carries the next day's, and both
    # enter at the run date's close. A plan built after that close can no longer be
    # entered at the price the measurement uses, and saying so here beats finding out
    # per-order at submit time.
    today, today_src = None, "container clock (UTC)"
    if api.usable:
        clk, _ = api.clock()
        if clk:
            today, today_src = clk["timestamp"][:10], "alpaca /v2/clock (ET)"
    if today is None:
        today = datetime.now(timezone.utc).date().isoformat()
    for c in taken:
        if c.get("entry_date"):
            c["entry_window"] = ("today" if c["entry_date"] == today else
                                 "past" if c["entry_date"] < today else "future")

    # Everything that cannot be placed goes before the budget is split, so a name
    # Alpaca will not lend does not take an equal share of the money with it.
    tradable = []
    for c in taken:
        if not c["entry_date"] or not c["exit_date"]:
            rejected.append({**c, "reason": "could not place the event in the calendar"})
        elif c.get("asset_checked") and not c.get("tradable"):
            rejected.append({**c, "reason": "not tradable at Alpaca"})
        elif c["side"] == "sell" and not ex["orders"].get("allow_shorts", True):
            rejected.append({**c, "reason": "shorts disabled in config"})
        elif c["side"] == "sell" and c.get("asset_checked") and not c.get("shortable"):
            rejected.append({**c, "reason": "not shortable at Alpaca"})
        else:
            tradable.append(c)

    keep, undersized = size(tradable, float(equity), sizing)
    rejected += undersized

    return {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "run": str(run), "broker": "alpaca", "endpoint": api.base,
            "account_kind": "paper" if api.is_paper else "live",
            "ranking_key": scores.get("ranking_key"),
            "benchmark": bench, "sizing": sizing, "orders": ex["orders"],
            "calendar_source": cal_src, "today": today, "today_source": today_src,
            "equity_usd": round(float(equity), 2), "equity_source": equity_src,
            "buying_power_usd": (round(float(acct["buying_power"]), 2)
                                 if acct else None),
            "regt_buying_power_usd": (round(float(acct["regt_buying_power"]), 2)
                                      if acct and acct.get("regt_buying_power")
                                      else None),
            "shorting_enabled": (acct.get("shorting_enabled") if acct else None),
            "names_in_run": scores.get("names"),
            "note": ("Selection is |impact_sum| >= conviction_floor, sign for side, "
                     "plus a turnover floor and a shortability check. The rule is 21 "
                     "trades over 5 independent days; treat it as a lead. This is "
                     "research, not investment advice."),
            "positions": keep, "rejected": rejected}


# ---------------------------------------------------------------- order state

def orders_path(run):
    return Path(run) / "alpaca-orders.json"


def load_orders(run):
    p = orders_path(run)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"run": str(run), "entries": [], "exits": [], "log": []}


def save_orders(run, state):
    state["updated_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    orders_path(run).write_text(json.dumps(state, indent=1) + "\n", encoding="utf-8")


def upsert(rows, row):
    for i, r in enumerate(rows):
        if r.get("client_order_id") == row.get("client_order_id"):
            rows[i] = {**r, **row}
            return
    rows.append(row)


def client_id(run, ticker, leg):
    return f"{CLIENT_PREFIX}-{Path(run).parent.name}-{ticker}-{leg}"


# ---------------------------------------------------------------- guards

def guard(api, ex, submit, live_ok):
    """Every reason not to send an order, checked before the first one is sent."""
    if not submit:
        return "dry run: --submit not given"
    if not ex.get("enabled"):
        return "execution.enabled is false in config/pipeline.yaml"
    if not api.usable:
        return "no ALPACA_API_KEY_ID / ALPACA_API_SECRET_KEY in the environment"
    if not api.is_paper and not live_ok:
        return (f"endpoint {api.base} is not a paper endpoint; pass "
                "--live-account-i-understand to trade a live account")
    acct, err = api.account()
    if not acct:
        return f"account unreachable: {err}"
    if acct.get("trading_blocked") or acct.get("account_blocked"):
        return "the Alpaca account is blocked for trading"
    return None


def moc_ok(api):
    """Is it inside the window where Alpaca still accepts market-on-close?

    Returns (ok, note). The cutoff is the session close less MOC_CUTOFF_MIN, so
    early-close days are handled by the calendar rather than a hardcoded 15:50.
    """
    clk, err = api.clock()
    if not clk:
        return False, f"clock unreachable: {err}"
    now = datetime.fromisoformat(clk["timestamp"].replace("Z", "+00:00"))
    if not clk.get("is_open"):
        return False, f"market closed at {now.isoformat(timespec='seconds')}"
    nc = datetime.fromisoformat(clk["next_close"].replace("Z", "+00:00"))
    left = (nc - now).total_seconds() / 60.0
    if left < MOC_CUTOFF_MIN:
        return False, f"{left:.0f} min to the close, inside the MOC cutoff"
    return True, f"{left:.0f} min to the close"


def flatten(api, submit, reason_blocked, timeout=60):
    """Cancel every open order and close every position, at market, now.

    This is the start-of-run clean slate: the book is rebuilt from scratch every
    day, so whatever is still open is yesterday's and goes. It is safe at that
    moment for one reason worth stating -- at the time the edge hunt runs, every
    position in the account has already been through its print, so nothing is cut
    short of its event. It is not a free swap for the market-on-close exit: it sells
    around the open rather than at the close, and to the next open the direction
    result is ρ=+0.331, p=0.046 against ρ=+0.514, p=0.0015 to the next close.

    Returns a record. Waits for flat, because an open opposing order in a symbol
    that is also in today's book gets the entry rejected as a potential wash trade.
    """
    rec = {"action": "flatten", "utc": datetime.now(timezone.utc).isoformat(
        timespec="seconds"), "submitted": False}
    if reason_blocked:
        return {**rec, "reason": reason_blocked}
    before, err = api.call("GET", "/v2/positions")
    if before is None:
        return {**rec, "reason": f"could not read positions: {err}"}
    rec["positions_before"] = [{"symbol": p["symbol"], "qty": p["qty"],
                                "unrealized_plpc": p.get("unrealized_plpc")}
                               for p in before]
    if not submit:
        return {**rec, "reason": "dry run"}
    api.call("DELETE", "/v2/orders")                    # stale MOC exits included
    resp, err = api.call("DELETE", "/v2/positions?cancel_orders=true")
    if resp is None and err:
        return {**rec, "reason": f"close-all refused: {err}"}
    rec["close_all_response"] = resp
    waited = 0
    while waited < timeout:
        left, _ = api.call("GET", "/v2/positions")
        if left == []:
            break
        time.sleep(3)
        waited += 3
    left, _ = api.call("GET", "/v2/positions")
    rec.update({"submitted": True, "waited_s": waited,
                "positions_after": [p["symbol"] for p in (left or [])]})
    if left:
        rec["reason"] = ("still holding " + ", ".join(p["symbol"] for p in left) +
                         " after the close-all; entries in those names would be "
                         "rejected as a wash trade")
    return rec


def order_body(ticker, qty, side, ex, moc=True):
    o = {"symbol": ticker, "qty": str(int(qty)), "side": side,
         "type": "market", "extended_hours": False}
    if moc:
        o["time_in_force"] = "cls"                 # market-on-close
    else:
        o["time_in_force"] = ex["orders"].get("time_in_force", "day")
    return o


def send(api, body, cid, submit, reason_blocked):
    """One order. Returns a record, submitted or not, always with a stated reason."""
    rec = {"client_order_id": cid, **{k: body[k] for k in
           ("symbol", "qty", "side", "type", "time_in_force")},
           "utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if reason_blocked:
        return {**rec, "submitted": False, "reason": reason_blocked}
    resp, err = api.submit({**body, "client_order_id": cid})
    if resp:
        return {**rec, "submitted": True, "order_id": resp.get("id"),
                "status": resp.get("status")}
    if err and "client_order_id" in err.lower():
        return {**rec, "submitted": False, "reason": "already placed (duplicate "
                                                     "client_order_id)"}
    return {**rec, "submitted": False, "reason": err}


# ---------------------------------------------------------------- commands

def cmd_plan(a, api, ex):
    plan = build_plan(a.run, api, ex, a.equity)
    out = Path(a.out) if a.out else Path(a.run) / "alpaca-plan.json"
    out.write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    print_plan(plan)
    print(f"\nwrote {out}")
    return plan


def print_plan(plan):
    print(f"{plan['run']}   {plan['account_kind']} {plan['endpoint']}")
    print(f"equity ${plan['equity_usd']:,.0f} ({plan['equity_source']}), "
          f"calendar {plan['calendar_source']}")
    b = plan["benchmark"]
    print(f"benchmark: |{b.get('key')}| >= {b['min_conviction']}, turnover >= "
          f"${float(b.get('min_dollar_volume_usd') or 0)/1e6:.1f}m, "
          f"max {b.get('max_positions')} names\n")
    if not plan["positions"]:
        print("no name meets the benchmark — nothing to trade")
    else:
        print(f"{'ticker':8s}{'side':6s}{'key':>8s}{'-runup':>8s}{'qty':>7s}"
              f"{'notional':>11s}{'%eq':>7s}{'%adv':>7s}{'turnover':>10s}"
              f"{'size from':>13s}  entry -> exit")
        for c in plan["positions"]:
            ru = c.get("run_up_20d_pct")
            print(f"{c['ticker']:8s}{'long' if c['side']=='buy' else 'short':6s}"
                  f"{c['value']:>+8.2f}"
                  f"{(f'{-ru:+.1f}' if ru is not None else '—'):>8s}"
                  f"{c['qty']:>7d}"
                  f"{c['notional_at_spot_usd']:>11,.0f}"
                  f"{c.get('pct_of_equity') or 0:>7.1f}"
                  f"{c.get('pct_of_adv') or 0:>7.2f}"
                  f"{c['dollar_volume_usd']/1e6:>9.1f}m{c['binding_cap']:>13s}"
                  f"  {c['entry_date']} -> {c['exit_date']}")
        agree = [c for c in plan["positions"] if c.get("run_up_20d_pct") is not None
                 and (c["value"] > 0) == (c["run_up_20d_pct"] < 0)]
        print(f"the free control: -run_up_20d_pct agrees with the side on "
              f"{len(agree)} of {len(plan['positions'])} names. It ranked the six "
              f"resolved days at rho=0.335 against the hunt's 0.407.")
        stale = [c["ticker"] for c in plan["positions"]
                 if c.get("entry_window") == "past"]
        if stale:
            print(f"\n! the entry close has already passed for {', '.join(stale)} "
                  f"(today {plan['today']}, {plan['today_source']}). `open` will "
                  f"refuse these unless --force-date, and a forced fill is not the "
                  f"price edge_resolve.py scores.")
        gross = sum(c["notional_at_spot_usd"] for c in plan["positions"])
        net = sum(c["notional_at_spot_usd"] * (1 if c["side"] == "buy" else -1)
                  for c in plan["positions"])
        print(f"\ngross ${gross:,.0f} ({gross/plan['equity_usd']*100:.1f}% of equity), "
              f"net ${net:+,.0f}")
        bp = plan.get("regt_buying_power_usd") or plan.get("buying_power_usd")
        if bp and gross > bp:
            print(f"! gross ${gross:,.0f} exceeds ${bp:,.0f} of buying power. The "
                  f"orders that do not fit will be rejected by Alpaca, not by this "
                  f"script — lower gross_exposure_pct_of_equity.")
        short = [c for c in plan["positions"] if c["side"] == "sell"]
        if short and plan.get("shorting_enabled") is False:
            print(f"! {len(short)} short leg(s) on an account with shorting disabled. "
                  f"They will all be rejected and the book becomes long-only, which "
                  f"is a different strategy from the measured one.")
    if plan["rejected"]:
        print(f"\n{len(plan['rejected'])} name(s) not traded")
        for c in plan["rejected"]:
            print(f"  {c['ticker']:8s}{c['reason']}")


def cmd_open(a, api, ex):
    blocked = guard(api, ex, a.submit, a.live_account_i_understand)

    # Clean slate first, and sizing after it, so the plan is drawn against the
    # equity and buying power the flatten actually leaves behind.
    flat = None
    if ex["orders"].get("flatten_before_entry", True) and not a.no_flatten:
        flat = flatten(api, a.submit, blocked)
        held = flat.get("positions_before") or []
        print(f"flatten: {len(held)} position(s) held"
              + (f" — {', '.join(p['symbol'] for p in held)}" if held else "")
              + (f" — {'closed' if flat['submitted'] else flat.get('reason')}"))
        if flat.get("submitted") and flat.get("positions_after"):
            print(f"  ! still holding {', '.join(flat['positions_after'])}")

    plan = build_plan(a.run, api, ex, a.equity)
    if flat is not None:
        plan["flatten"] = flat
        same = {p["symbol"] for p in (flat.get("positions_before") or [])} & \
               {c["ticker"] for c in plan["positions"]}
        if same:
            print(f"  ! {', '.join(sorted(same))} was sold and is bought back today, "
                  f"which is a day trade. Under $25k of equity FINRA allows three in "
                  f"five business days before the account is restricted.")
    Path(a.run, "alpaca-plan.json").write_text(json.dumps(plan, indent=1) + "\n",
                                               encoding="utf-8")
    print_plan(plan)
    moc, moc_note = (moc_ok(api) if (a.submit and not blocked) else (False, "dry run"))
    print(f"\nsubmit: {'blocked — ' + blocked if blocked else moc_note}")

    today = None
    if api.usable:
        clk, _ = api.clock()
        today = clk["timestamp"][:10] if clk else None
    state = load_orders(a.run)
    if flat is not None and flat.get("submitted"):
        state["log"].append(flat)
    use_moc = ex["orders"].get("entry", "market_on_close") == "market_on_close"

    for c in plan["positions"]:
        reason = blocked
        if not reason and today and c["entry_date"] != today and not a.force_date:
            reason = f"entry date is {c['entry_date']}, today is {today} (--force-date)"
        entry_moc = use_moc
        if not reason and use_moc and not moc:
            if a.allow_market_fallback:
                entry_moc = False
            else:
                reason = (f"MOC unavailable ({moc_note}); --allow-market-fallback to "
                          "send a plain market order instead")
        body = order_body(c["ticker"], c["qty"], c["side"], ex, moc=entry_moc)
        cid = client_id(a.run, c["ticker"], "entry")
        rec = send(api, body, cid, a.submit, reason)
        rec.update({"leg": "entry", "entry_date": c["entry_date"],
                    "exit_date": c["exit_date"], "event_date": c["event_date"],
                    "session": c["session"], "key": c["key"], "value": c["value"],
                    "spot_at_plan": c["spot"]})
        upsert(state["entries"], rec)
        print(f"  {c['ticker']:8s}{'SENT' if rec['submitted'] else 'not sent'}"
              f"  {rec.get('order_id') or rec.get('reason')}")
    if blocked:
        print(f"\nnothing submitted, so {orders_path(a.run).name} was not touched — "
              f"the plan is in alpaca-plan.json")
        return
    state["log"].append({"utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "action": "open", "moc": moc_note,
                         "positions": len(plan["positions"])})
    save_orders(a.run, state)
    print(f"\nwrote {orders_path(a.run)}")


def cmd_close(a, api, ex):
    runs = [a.run] if a.run else sorted(
        p for pat in a.scan for p in glob.glob(pat) if orders_path(p).exists())
    if not runs:
        print("no run with an alpaca-orders.json to close")
        return
    blocked = guard(api, ex, a.submit, a.live_account_i_understand)
    use_moc = ex["orders"].get("exit", "market_on_close") == "market_on_close" and not a.now
    moc, moc_note = ((moc_ok(api) if use_moc else (True, "market order"))
                     if (a.submit and not blocked) else (False, "dry run"))
    today = None
    if api.usable:
        clk, _ = api.clock()
        today = clk["timestamp"][:10] if clk else None
    print(f"closing across {len(runs)} run(s), today {today}, "
          f"{'blocked — ' + blocked if blocked else moc_note}")

    for run in runs:
        state = load_orders(run)
        for e in state["entries"]:
            if a.submit and not e.get("submitted"):
                continue                    # in a dry run, show them all instead
            cid = client_id(run, e["symbol"], "exit")
            if any(x.get("client_order_id") == cid and x.get("submitted")
                   for x in state["exits"]):
                continue
            due = a.all or (today and e.get("exit_date") == today)
            if not due:
                continue
            reason = blocked
            qty, held = None, None
            if api.usable:
                pos, err = api.position(e["symbol"])
                if pos:
                    held = float(pos.get("qty", 0))
                    qty = abs(int(float(pos["qty"])))
                elif not reason:
                    reason = f"no open position at Alpaca ({err})"
            if qty is None and not reason:
                qty = int(e["qty"])
            if not reason and use_moc and not moc:
                reason = f"MOC unavailable ({moc_note}); rerun with --now for a " \
                         "market order or before the cutoff"
            side = "sell" if e["side"] == "buy" else "buy"
            body = order_body(e["symbol"], qty or e["qty"], side, ex, moc=use_moc)
            rec = send(api, body, cid, a.submit, reason)
            rec.update({"leg": "exit", "closes": e["client_order_id"],
                        "exit_date": e.get("exit_date"), "position_qty_at_close": held})
            upsert(state["exits"], rec)
            print(f"  {run} {e['symbol']:8s}"
                  f"{'SENT' if rec['submitted'] else 'not sent'}"
                  f"  {rec.get('order_id') or rec.get('reason')}")
        if blocked:
            continue                        # a dry run records nothing
        state["log"].append({"utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                             "action": "close", "all": bool(a.all), "moc": moc_note})
        save_orders(run, state)
        print(f"  wrote {orders_path(run)}")


def cmd_flatten(a, api, ex):
    blocked = guard(api, ex, a.submit, a.live_account_i_understand)
    rec = flatten(api, a.submit, blocked)
    held = rec.get("positions_before") or []
    print(f"{len(held)} position(s) held")
    for p in held:
        pl = p.get("unrealized_plpc")
        print(f"  {p['symbol']:8s}{p['qty']:>10s}"
              + (f"  {float(pl)*100:+.2f}%" if pl is not None else ""))
    print("closed" if rec.get("submitted") else f"not closed — {rec.get('reason')}")
    if rec.get("positions_after"):
        print(f"! still holding {', '.join(rec['positions_after'])}")
    if a.run and rec.get("submitted"):
        state = load_orders(a.run)
        state["log"].append(rec)
        save_orders(a.run, state)


def cmd_status(a, api, ex):
    if not api.usable:
        sys.exit("status needs ALPACA_API_KEY_ID / ALPACA_API_SECRET_KEY")
    acct, err = api.account()
    if not acct:
        sys.exit(f"account unreachable: {err}")
    print(f"{'paper' if api.is_paper else 'LIVE'} {api.base}")
    print(f"equity ${float(acct['equity']):,.2f}  cash ${float(acct['cash']):,.2f}  "
          f"buying power ${float(acct['buying_power']):,.2f}")
    runs = [a.run] if a.run else sorted(
        p for pat in a.scan for p in glob.glob(pat) if orders_path(p).exists())
    out = {"checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "equity_usd": round(float(acct["equity"]), 2), "runs": []}
    for run in runs:
        state = load_orders(run)
        rows = []
        for e in state["entries"] + state["exits"]:
            if not e.get("submitted"):
                continue
            o, oerr = api.call("GET", f"/v2/orders:by_client_order_id?"
                                      f"client_order_id={e['client_order_id']}")
            rows.append({"client_order_id": e["client_order_id"], "leg": e.get("leg"),
                         "symbol": e["symbol"], "side": e["side"],
                         "status": (o or {}).get("status") or oerr,
                         "filled_qty": (o or {}).get("filled_qty"),
                         "filled_avg_price": (o or {}).get("filled_avg_price"),
                         "exit_date": e.get("exit_date")})
        open_pos = []
        for sym in {e["symbol"] for e in state["entries"] if e.get("submitted")}:
            p, _ = api.position(sym)
            if p:
                open_pos.append({"symbol": sym, "qty": p["qty"],
                                 "avg_entry_price": p["avg_entry_price"],
                                 "unrealized_plpc": p["unrealized_plpc"]})
        print(f"\n{run}")
        for r in rows:
            print(f"  {r['leg'] or '?':6s}{r['symbol']:8s}{r['side']:6s}"
                  f"{str(r['status']):12s}filled {r['filled_qty']} @ "
                  f"{r['filled_avg_price']}  exit {r['exit_date']}")
        for p in open_pos:
            print(f"  OPEN  {p['symbol']:8s}{p['qty']:>8s} @ {p['avg_entry_price']}  "
                  f"{float(p['unrealized_plpc'])*100:+.2f}%")
        out["runs"].append({"run": run, "orders": rows, "open_positions": open_pos})
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {a.out}")


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, run_required=True):
        p.add_argument("--run", required=run_required,
                       help="an edge run directory, e.g. research/2026/09/2026-09-09/edge")
        p.add_argument("--base", help="Alpaca endpoint (default $ALPACA_BASE_URL or paper)")
        p.add_argument("--equity", type=float,
                       help="override account equity for sizing (dry runs)")
        p.add_argument("--submit", action="store_true",
                       help="actually place orders; without it everything is a dry run")
        p.add_argument("--live-account-i-understand", action="store_true",
                       help="permit a non-paper endpoint")

    p = sub.add_parser("plan", help="apply the benchmark and write alpaca-plan.json")
    common(p)
    p.add_argument("--out")

    p = sub.add_parser("open", help="flatten, then place the entry orders "
                                    "(run on the entry date)")
    common(p)
    p.add_argument("--force-date", action="store_true",
                   help="place even when today is not the planned entry date")
    p.add_argument("--allow-market-fallback", action="store_true",
                   help="if the MOC window has passed, send a plain market order")
    p.add_argument("--no-flatten", action="store_true",
                   help="keep the existing positions instead of selling them first")

    p = sub.add_parser("flatten", help="cancel every order and close every position, "
                                       "at market, now")
    common(p, run_required=False)

    p = sub.add_parser("close", help="close what is due (run on the exit date)")
    common(p, run_required=False)
    p.add_argument("--scan", action="append", default=[],
                   help="glob of run dirs to scan instead of --run")
    p.add_argument("--all", action="store_true",
                   help="close every open leg regardless of its exit date")
    p.add_argument("--now", action="store_true",
                   help="market order immediately instead of market-on-close")

    p = sub.add_parser("status", help="reconcile orders and positions against a run")
    common(p, run_required=False)
    p.add_argument("--scan", action="append", default=[])
    p.add_argument("--out")

    a = ap.parse_args()
    if getattr(a, "scan", None) == []:
        a.scan = ["research/*/*/*/edge"]
    cfg = config()
    ex = execution_config(cfg)
    api = Alpaca(base=a.base)
    {"plan": cmd_plan, "open": cmd_open, "close": cmd_close,
     "flatten": cmd_flatten, "status": cmd_status}[a.cmd](a, api, ex)


if __name__ == "__main__":
    main()
