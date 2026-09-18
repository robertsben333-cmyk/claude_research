#!/usr/bin/env python3
"""Place stage E's benchmark names as real orders at Alpaca, and close them again.

The stage emits one signed number per company, `impact_sum`, and no call. This
script is the only place in the repo that turns that number into a position, and
it does so through exactly one rule -- the one thing in `researcher_us/EDGE_ANALYSIS.md`
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

The event window is the one `edge_resolve.py` scores:

    amc print   the last close before the print is the event date's close
    bmo print   it is the close of the session before

Both trading steps run inside stage E's own session, four hours apart. Step 0b
sells yesterday's book at market before the sweep launches; step 7 buys today's
at market as soon as the note is published. Neither waits for the closing
auction, and the difference that makes was measured on the same 18 traded events:
market-on-close gave 15/18 and +5.86% a trade, a market order at 14:00 ET gave
14/18 and +5.82% -- four hundredths of a point. `researcher_us/scripts/edge_entry_timing.py`
regenerates that. What it cannot see is the spread: the closing auction is the
deepest liquidity of the day, and in a $200k-a-day name that is where a fill is
cheapest. Set `orders.entry: market_on_close` to go back to the auction.

Nothing is submitted unless all four of these hold: `execution.enabled: true` in
config/pipeline.yaml, `--submit` on the command line, credentials in the
environment, and a paper endpoint (a live endpoint additionally needs
--live-account-i-understand). Without --submit every subcommand is a dry run that
prints and writes the plan and touches no order.

    export ALPACA_API_KEY_ID=... ALPACA_API_SECRET_KEY=...
    python3 researcher_us/scripts/alpaca_trade.py flatten --submit                    # step 0b
    python3 researcher_us/scripts/alpaca_trade.py plan  --run research/2026/09/2026-09-09/edge
    python3 researcher_us/scripts/alpaca_trade.py open  --run <same> --submit --no-flatten   # step 7
    python3 researcher_us/scripts/alpaca_trade.py status --run research/2026/09/2026-09-09/edge
    python3 researcher_us/scripts/alpaca_trade.py verify --scan 'research/*/*/*/edge' --fix --submit

A submitted sell is not a sold position. `close` re-reads every exit it sent after
`orders.fill_check_seconds` (300 by default) and says, per leg, whether the account
has actually let go of the shares; `verify` does the same check on demand. That
check exists because `cls` and `opg` are auction orders -- each crosses once and
takes whatever size the contra side brings, which on a $200k-a-day name has been 17
of 161 (HOFT), 39 of 183 (CODA) and 0 of 224 (RLGT). Nothing re-read the status, so
the record said `submitted: true` while the position stayed open for another day.
"""
import argparse
import glob
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

PAPER = "https://paper-api.alpaca.markets"
DATA = "https://data.alpaca.markets"   # market data lives on its own host
CLIENT_PREFIX = "edge"          # every client_order_id this repo ever creates
MOC_CUTOFF_MIN = 10             # minutes before the close that MOC stops being accepted
# How old a last trade may be before the quote mid is preferred for sizing. Ten
# minutes is loose enough for a $200k-a-day name that prints a few times an hour
# and tight enough that a halted or overnight tape falls through to the quote.
MAX_TRADE_AGE_S = 600
# How wide a quote may be before its mid stops being a price. The free IEX feed
# serves plenty of junk: FEIM quoted 54.24 / 72.79 at 18:12 UTC on 2026-09-10, a
# 29% spread, while the stock was trading near 63.4. A mid taken off that is not
# an estimate of anything, so a stale trade is preferred to it.
MAX_QUOTE_SPREAD_PCT = 2.0


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

    # -- market data. A different host from the trading API, same credentials.

    def data_call(self, path, timeout=30):
        url = f"{DATA}{path}"
        req = urllib.request.Request(url, method="GET", headers={
            "APCA-API-KEY-ID": self.key,
            "APCA-API-SECRET-KEY": self.secret,
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
        except Exception as e:
            return None, f"{type(e).__name__}: {str(e)[:300]}"

    def latest_quotes(self, symbols):
        if not symbols:
            return {}, None
        q = urllib.parse.quote(",".join(sorted(symbols)))
        d, err = self.data_call(f"/v2/stocks/quotes/latest?symbols={q}")
        return ((d or {}).get("quotes") or {}), err

    def latest_trades(self, symbols):
        if not symbols:
            return {}, None
        q = urllib.parse.quote(",".join(sorted(symbols)))
        d, err = self.data_call(f"/v2/stocks/trades/latest?symbols={q}")
        return ((d or {}).get("trades") or {}), err


def quote_snapshot(q):
    """Normalise one Alpaca quote into bid/ask/mid/spread, or None if unusable.

    A one-sided or crossed quote is not a price. The free IEX feed serves plenty
    of both, and a mid taken off `ap 163.86 / bp 155.76` -- a real ORCL quote from
    2026-09-10 -- is 5% away from where the stock was actually trading.
    """
    if not q:
        return None
    bid, ask = q.get("bp"), q.get("ap")
    try:
        bid, ask = float(bid or 0), float(ask or 0)
    except (TypeError, ValueError):
        return None
    if bid <= 0 or ask <= 0 or ask < bid:
        return None
    mid = (bid + ask) / 2.0
    return {"bid": bid, "ask": ask, "mid": round(mid, 4),
            "spread_pct": round(100 * (ask - bid) / mid, 3),
            "utc": q.get("t"), "bid_size": q.get("bs"), "ask_size": q.get("as")}


def _age_seconds(ts):
    """Seconds between an Alpaca RFC3339 timestamp and now, or None if unparseable."""
    if not ts:
        return None
    # Alpaca sends nanoseconds; fromisoformat takes at most microseconds.
    s = re.sub(r"\.(\d{6})\d+", r".\1", str(ts).strip()).replace("Z", "+00:00")
    try:
        t = datetime.fromisoformat(s)
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).total_seconds()


def reference_prices(api, tickers, max_trade_age_s=MAX_TRADE_AGE_S):
    """A live, sourced price per ticker for sizing. Never invents one.

    Sizing used to divide the budget by the SEALED BASELINE spot, and the old
    docstring called that deliberate on the grounds that the alternative was "an
    unsourced live quote". An Alpaca last trade is not unsourced -- it carries a
    venue and an exchange timestamp, both recorded here -- and the baseline is
    captured when the run starts, which on 2026-09-10 was 14:08 UTC against orders
    that went in at 17:59. Four hours. HOFT was sized off 12.42 and filled at
    12.6186, so a 20.0%-of-equity position was really 20.3%, and every "fill versus
    plan" number in the run log was drift rather than execution.

    Preference order, and each name records which one it got:
      last trade   fresh, the best single estimate of where the next share prints
      quote mid    trade stale or missing, and the quote is two-sided AND tight
      last trade   stale, but still a price something actually traded at
      None         caller falls back to the baseline spot and SAYS SO

    The tightness test is not decoration. On the first live run FEIM's trade was
    stale and its quote was 54.24 / 72.79 -- 29% wide on the free IEX feed -- and
    the first version of this function sized off that mid. A wide mid is not a
    price; a stale print is.

    Returns {ticker: {price, source, utc, age_s, quote}}. A ticker absent from the
    result has no live price and must be sized off the baseline with that recorded.
    """
    out = {}
    if not api.usable or not tickers:
        return out, "no credentials" if not api.usable else None
    trades, terr = api.latest_trades(tickers)
    quotes, qerr = api.latest_quotes(tickers)
    for t in tickers:
        snap = quote_snapshot(quotes.get(t))
        tr = trades.get(t) or {}
        price, source, utc, age = None, None, None, None
        try:
            tp = float(tr.get("p") or 0)
        except (TypeError, ValueError):
            tp = 0.0
        tage = _age_seconds(tr.get("t"))
        tight = snap and snap["spread_pct"] <= MAX_QUOTE_SPREAD_PCT
        if tp > 0 and (tage is None or tage <= max_trade_age_s):
            price, source, utc, age = tp, "alpaca last trade", tr.get("t"), tage
        elif tight:
            price, source, utc = snap["mid"], "alpaca quote mid", snap["utc"]
            age = _age_seconds(snap["utc"])
        elif tp > 0:
            price, source, utc, age = (
                tp, f"alpaca last trade (stale {tage:.0f}s)"
                    + (f", quote {snap['spread_pct']:.1f}% wide" if snap else ""),
                tr.get("t"), tage)
        elif snap:
            price, source, utc = (snap["mid"],
                                  f"alpaca quote mid ({snap['spread_pct']:.1f}% wide, "
                                  f"no trade)", snap["utc"])
            age = _age_seconds(snap["utc"])
        if price:
            out[t] = {"price": round(price, 4), "source": source, "utc": utc,
                      "age_s": round(age) if age is not None else None,
                      "quote": snap}
    return out, (terr or qerr)


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

    Share counts come off `ref_price` -- a live, sourced Alpaca last trade or quote
    mid, set by `reference_prices()` at plan time. Until 2026-09-10 they came off the
    SEALED BASELINE spot instead, which is captured when the run starts: on that day
    the baseline was 14:08 UTC and the orders went in at 17:59, so HOFT was sized off
    12.42, filled at 12.6186, and a 20.0%-of-equity cap produced a 20.3% position.
    The caps are percentages of equity and of ADV, so applying them to a stale price
    makes them the wrong percentages, and the error grows with the gap.

    A name with no live price keeps `spot` and records `price_source` as the
    baseline, because sizing off a stale number knowingly beats not trading, and
    both beat sizing off a stale number silently.
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
        px = c.get("ref_price") or c["spot"]
        qty = int(math.floor(target / px))
        notional = qty * px
        cap_adv = (c["dollar_volume_usd"] * float(adv_pct) / 100.0 if adv_pct else None)
        row = {**c, "target_notional_usd": round(target, 2), "qty": qty,
               "price_used_usd": round(px, 4),
               "price_source": c.get("ref_price_source") or "sealed baseline spot",
               "notional_usd": round(notional, 2),
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

    # A live price per name, fetched AFTER the tradable set is final so no quote is
    # pulled for a name that cannot be placed. Sizing divides the budget by this;
    # anything without one falls back to the baseline spot and says so in the row.
    refs, ref_err = reference_prices(api, [c["ticker"] for c in tradable])
    for c in tradable:
        r = refs.get(c["ticker"])
        if r:
            c["ref_price"] = r["price"]
            c["ref_price_source"] = r["source"]
            c["ref_price_utc"] = r["utc"]
            c["ref_price_age_s"] = r["age_s"]
            c["quote_at_plan"] = r["quote"]
            c["baseline_drift_pct"] = (round(100 * (r["price"] - c["spot"]) / c["spot"], 3)
                                       if c.get("spot") else None)

    keep, undersized = size(tradable, float(equity), sizing)
    rejected += undersized

    return {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "run": str(run), "broker": "alpaca", "endpoint": api.base,
            "account_kind": "paper" if api.is_paper else "live",
            "ranking_key": scores.get("ranking_key"),
            "benchmark": bench, "sizing": sizing, "orders": ex["orders"],
            "calendar_source": cal_src, "today": today, "today_source": today_src,
            "reference_price_error": ref_err,
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
    """Replace the row carrying this client_order_id, or append it.

    Replace, not merge. The merge left a failed attempt's `reason` sitting beside
    the successful attempt's `submitted: true` -- VRA and FPS on 2026-09-15 both
    read "cls unavailable (market closed)" next to a live order id, which is the
    opposite of what happened. alpaca-orders.json is the file a person opens to
    answer "did the sell go", so each order says one thing. The attempts that were
    never sent are kept, as history, where they cannot be read as the outcome.
    """
    for i, r in enumerate(rows):
        if r.get("client_order_id") == row.get("client_order_id"):
            hist = list(r.get("previous_attempts") or [])
            if r.get("reason") and not r.get("submitted"):
                hist.append({"utc": r.get("utc"), "reason": r.get("reason")})
            rows[i] = {**row, **({"previous_attempts": hist} if hist else {})}
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


def entry_window(api, moc=True):
    """Can an order go in right now? Returns (ok, note).

    A plain market order needs only an open session. A market-on-close order needs
    the session to be open AND more than MOC_CUTOFF_MIN left, because Alpaca stops
    accepting them near the bell; taking the cutoff off the calendar's own close
    handles early-close days rather than hardcoding 15:50.
    """
    clk, err = api.clock()
    if not clk:
        return False, f"clock unreachable: {err}"
    now = datetime.fromisoformat(clk["timestamp"].replace("Z", "+00:00"))
    if not clk.get("is_open"):
        return False, f"market closed at {now.isoformat(timespec='seconds')}"
    nc = datetime.fromisoformat(clk["next_close"].replace("Z", "+00:00"))
    left = (nc - now).total_seconds() / 60.0
    if moc and left < MOC_CUTOFF_MIN:
        return False, f"{left:.0f} min to the close, inside the MOC cutoff"
    return True, f"{left:.0f} min to the close"


def overdue_legs(today, scan="research/*/*/*/edge", held=None):
    """Entries whose exit date has passed with no exit ever submitted.

    The safety property the whole operation rests on: a new book is never entered on
    top of an old one nobody sold. `flatten_before_entry` used to guarantee that by
    selling everything, but the per-session exit turns the flatten off, and then the
    guarantee has to come from checking rather than from sweeping.

    `held` is the set of symbols Alpaca actually still holds, and passing it is what
    keeps this honest. `flatten` closes positions without writing a per-leg exit into
    `alpaca-orders.json`, so the ledger alone reports a flattened position as unsold
    forever. Filtering on what the account holds means only a position that is really
    still open counts.
    """
    out = []
    for run in sorted(glob.glob(str(REPO / scan))):
        p = orders_path(run)
        if not p.exists():
            continue
        state = json.loads(p.read_text(encoding="utf-8"))
        done = {x.get("closes") for x in state.get("exits", []) if x.get("submitted")}
        # ... but only for a symbol the account has actually let go of. A partially
        # filled exit that then expired leaves the record submitted and the shares
        # held, and reading `done` alone turned that into a position no run would
        # sell and no `open` would refuse to trade over — a silent leak, which is
        # worse than the loud refusal this function exists to raise. When `held` is
        # known it outranks the ledger: still held means still unsold.
        if held is not None:
            done = {c for c in done
                    if not any(e.get("client_order_id") == c and e["symbol"] in held
                               for e in state.get("entries", []))}
        for e in state.get("entries", []):
            xd = e.get("exit_date")
            if (e.get("submitted") and xd and xd < today
                    and e.get("client_order_id") not in done
                    and (held is None or e["symbol"] in held)):
                out.append({"run": run, "symbol": e["symbol"], "exit_date": xd,
                            "side": e["side"], "qty": e.get("qty")})
    return out


# Alpaca order states in which an order can still trade. Anything else — filled,
# expired, canceled, rejected, done_for_day — can never fill another share, so a
# position still open behind one of those is a leg nothing is selling.
LIVE_ORDER_STATUSES = {
    "new", "accepted", "pending_new", "partially_filled", "held",
    "accepted_for_bidding", "pending_replace", "replaced", "calculated",
    "stopped", "suspended", "pending_cancel",
}


def order_live(api, rec):
    """Is this recorded order still capable of filling, per the broker right now?

    Unknown counts as live. A failed lookup must not be the reason a position gets
    sold a second time; the cost of being wrong that way is a real duplicate trade,
    while the cost of the other way is one more overdue line in the next run's log.
    """
    cid = rec.get("client_order_id")
    if not api.usable or not cid:
        return True
    o, err = api.call("GET", f"/v2/orders:by_client_order_id?client_order_id={cid}")
    if not o:
        return False if err and "404" in str(err) else True
    return str(o.get("status", "")).lower() in LIVE_ORDER_STATUSES


# Where an auction order can only ever fill. `cls` crosses once at 16:00 ET and
# `opg` once at 09:30 ET, so neither is verifiable five minutes after submission --
# it is still `new`, correctly, for hours.
AUCTION_TIFS = {"cls": "the 16:00 ET closing auction",
                "opg": "the 09:30 ET opening auction"}


def held_qty(api, sym):
    """How many shares of this symbol the account still holds, unsigned."""
    if not api.usable:
        return None
    pos, _ = api.position(sym)
    return abs(float(pos.get("qty", 0))) if pos else 0.0


def fill_state(api, rec):
    """Re-read one submitted order at the broker: status, and how much it filled."""
    cid = rec.get("client_order_id")
    if not api.usable or not cid:
        return None
    o, err = api.call("GET", f"/v2/orders:by_client_order_id?client_order_id={cid}")
    if not o:
        # Unknown counts as live, for the reason order_live() counts it live: a
        # failed lookup must never be the reason a position gets sold twice.
        return {"status": f"lookup failed: {err}", "live": True,
                "filled_qty": 0.0, "filled_avg_price": None, "order_qty": None}
    st = str(o.get("status", "")).lower()
    return {"status": st, "live": st in LIVE_ORDER_STATUSES,
            "filled_qty": float(o.get("filled_qty") or 0),
            "filled_avg_price": o.get("filled_avg_price"),
            "order_qty": float(o.get("qty") or 0)}


def verify_exits(api, runs, ex, submit, blocked, wait_s=0, fix=True, quiet=False):
    """Did the sells actually SELL? Re-read every submitted exit at the broker.

    Submission is not a fill, and until 2026-09-15 nothing here ever looked again.
    `send` stored the status Alpaca returns at submission -- always `pending_new`
    or `accepted` -- and the session ended. The only thing that ever noticed an
    exit which had not sold was the NEXT run's held-position check, 17 to 24 hours
    later, and that check could not always act (see the market fallback in
    cmd_close).

    What was being missed is that `cls` and `opg` are not market orders. Each
    participates in ONE auction cross and takes whatever size the contra side
    brings, which in a $200k-a-day name is often almost none:

        HOFT  2026-09-11  cls    17 of 161 filled, then expired
        CODA  2026-09-14  cls    39 of 183 filled, then expired
        RLGT  2026-09-15  opg     0 of 224 filled

    Three verdicts per leg, and only one of them is a problem:

        closed     the account no longer holds it. Done, whatever the order says.
        working    an order that can still fill is out. Expected for hours on an
                   auction TIF -- this is not a failure and nothing is re-sent.
        UNFILLED   shares still held and every order for the leg is dead at the
                   broker. Nothing will ever sell this leg on its own.

    With `fix`, an UNFILLED leg is re-sent at plain market, sized to what Alpaca
    reports is still held, under the same invariant cmd_close keeps: only when
    every prior order is dead AND the position is really still there.
    """
    if wait_s:
        if not quiet:
            print(f"\nwaiting {wait_s}s for fills, then verifying")
        time.sleep(wait_s)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    mkt_tif = ex["orders"].get("time_in_force", "day")
    mkt = None                       # one clock call for the whole sweep, not per leg
    clk, _ = api.clock() if api.usable else (None, None)
    market_open = clk.get("is_open") if clk else None
    rows = []
    for run in runs:
        state = load_orders(run)
        touched = False
        for en in state.get("entries", []):
            if not en.get("submitted"):
                continue
            sent = [x for x in state.get("exits", [])
                    if x.get("closes") == en["client_order_id"] and x.get("submitted")]
            if not sent:
                continue
            reports = [(x, fill_state(api, x)) for x in sent]
            residual = held_qty(api, en["symbol"])
            live = [x for x, r in reports if r is None or r.get("live")]
            filled = sum((r or {}).get("filled_qty") or 0 for _, r in reports)
            if residual is None:
                verdict = "unknown"
            elif residual == 0:
                verdict = "closed"
            elif live:
                verdict = "working"
            else:
                verdict = "unfilled"
            row = {"run": run, "symbol": en["symbol"], "session": en.get("session"),
                   "exit_date": en.get("exit_date"), "entry_qty": float(en["qty"]),
                   "filled_qty": filled, "residual_qty": residual,
                   "verdict": verdict, "checked_utc": now,
                   "orders": [{"client_order_id": x["client_order_id"],
                               "time_in_force": x.get("time_in_force"),
                               **(r or {"status": "not checked"})}
                              for x, r in reports]}
            if verdict == "working":
                waiting = {x.get("time_in_force") for x in live
                           if x.get("time_in_force") in AUCTION_TIFS}
                if waiting:
                    row["note"] = ("waiting on " + ", ".join(
                        sorted(AUCTION_TIFS[t] for t in waiting)) +
                        "; not verifiable until it has crossed")
                elif market_open is False:
                    # A plain DAY order sent in the pre-market is accepted and held by
                    # Alpaca until the regular session opens, so `new` here is correct
                    # and not a failure. It is the same shape of "cannot be verified
                    # yet" as an auction order, and saying so keeps a pre-market run
                    # from reporting a working exit as if it were a problem.
                    row["note"] = ("queued while the market is closed; Alpaca routes "
                                   "it at the next open, so it is not verifiable "
                                   "until the session starts")
            if verdict == "unfilled" and fix:
                if blocked or not submit:
                    row["rescue"] = {"submitted": False,
                                     "reason": blocked or "dry run: --submit not given"}
                else:
                    if mkt is None:
                        mkt = auction_window(api, mkt_tif)
                    if not mkt[0]:
                        row["rescue"] = {"submitted": False,
                                         "reason": f"market unavailable ({mkt[1]})"}
                    else:
                        cid = f"{client_id(run, en['symbol'], 'exit')}-v{len(sent) + 1}"
                        side = "sell" if en["side"] == "buy" else "buy"
                        body = order_body(en["symbol"], int(residual), side, ex,
                                          moc=False, tif=mkt_tif)
                        rec = send(api, body, cid, True, None)
                        rec.update({"leg": "exit", "closes": en["client_order_id"],
                                    "exit_date": en.get("exit_date"),
                                    "position_qty_at_close": residual,
                                    "note": "rescue: every earlier exit for this leg "
                                            "was dead at the broker with shares still "
                                            "held"})
                        upsert(state["exits"], rec)
                        row["rescue"] = {k: rec.get(k) for k in
                                         ("client_order_id", "submitted", "order_id",
                                          "status", "reason", "qty")}
                        touched = True
            vs = state.setdefault("verifications", [])
            for i, v in enumerate(vs):
                if (v.get("symbol") == row["symbol"]
                        and v.get("exit_date") == row["exit_date"]):
                    vs[i] = row
                    break
            else:
                vs.append(row)
            touched = True
            rows.append(row)
        if touched and api.usable:
            state["log"].append({"utc": now, "action": "verify", "fix": bool(fix)})
            save_orders(run, state)
    if not quiet:
        print(f"\nfill check over {len(runs)} run(s), {len(rows)} exit leg(s)")
        for r in rows:
            mark = {"closed": "ok", "working": "work", "unfilled": "UNFILLED",
                    "unknown": "?"}[r["verdict"]]
            print(f"  {r['symbol']:8s}{(r['session'] or '?'):4s}{mark:9s}"
                  f"filled {r['filled_qty']:g}/{r['entry_qty']:g}"
                  f"  still held {r['residual_qty']}"
                  + (f"  -> {r['note']}" if r.get("note") else "")
                  + (f"  -> rescue {r['rescue'].get('order_id') or r['rescue'].get('reason')}"
                     if r.get("rescue") else ""))
        bad = [r for r in rows if r["verdict"] == "unfilled"]
        if bad:
            print(f"  {len(bad)} leg(s) NOT SOLD and no order working. Say so in the "
                  f"run log: an unsold leg blocks the next `open`.")
    return rows


EXIT_MODES = ("uniform", "bmo_close", "auction_split", "amc_open")


def exit_mode(ex):
    """Which of the four exit schemes is configured.

    `exit_by_session: true` is kept as an alias for `auction_split`; it was the first
    shape of this setting and turning it on already meant that scheme.
    """
    m = ex["orders"].get("exit_mode")
    if m is None:
        m = "auction_split" if ex["orders"].get("exit_by_session") else "uniform"
    if m not in EXIT_MODES:
        raise SystemExit(f"execution.orders.exit_mode is {m!r}; expected one of "
                         + ", ".join(EXIT_MODES))
    # A non-uniform mode with the flatten still on is not a preference, it is a
    # contradiction: the flatten sells every amc name at market when the run starts,
    # hours before the auction the mode exists to reach, so the configured exit can
    # never happen. It was documented in three places and enforced in none, which is
    # the shape of defect this repo keeps paying for -- a setting that reads as on
    # and is silently overridden. Refuse rather than run the wrong exit quietly.
    if m != "uniform" and ex["orders"].get("flatten_before_entry", True):
        raise SystemExit(
            f"execution.orders.exit_mode is {m!r} but flatten_before_entry is true. "
            "The flatten sells the whole book at market at the start of the next run, "
            "before any auction the mode would use, so the mode cannot take effect. "
            "Set flatten_before_entry: false, or set exit_mode: uniform.")
    return m


def exit_tif_for(session, ex):
    """Which instrument closes a position, per session, per mode.

    The two sessions were measured separately and want opposite exits
    (`researcher_us/EDGE_ANALYSIS.md`, "amc and bmo want opposite exits"). Per trade over the
    38 de-duplicated events, on the conviction book:

        amc   opening auction +8.91%   ~10:00 ET +6.08%   closing auction +5.23%
        bmo   opening auction +2.96%   ~10:00 ET +2.58%   closing auction +6.48%

    An amc print gets a whole overnight of processing, so the opening auction is
    already the informed price and the session that follows takes about three points
    back off the book. A bmo print gets two thin hours of pre-market and keeps
    repricing all day.

    WHAT EACH MODE COSTS AND WHAT IT NEEDS, on the same 22 trades:

      uniform         +4.49% (t=2.52)  the shipped scheme: flatten everything at
                      market when the next run starts, about 10:00 ET
      bmo_close       +6.27% (t=3.34)  amc at market on the run, bmo into today's
                      closing auction. ONE run — reachable from stage E's own
                      Routine, needs `flatten_before_entry: false` and nothing else
      auction_split   +7.81% (t=4.01)  amc into the opening auction, bmo into the
                      closing auction. Needs a SECOND Routine at 14:00 Amsterdam,
                      because Alpaca rejects `opg` between 09:28 and 19:00 ET

      amc_open        +6.49% (t=3.42)  amc into the opening auction, bmo at plain
                      market on the run at 13:00 ET. Same second Routine as
                      auction_split; gives up 1.31pp against it, and is the only mode
                      whose bmo leg is CERTAIN to be gone before the same afternoon
                      buys the next book

    So `bmo_close` buys +1.77pp of the +3.32pp on offer and costs no new machinery;
    `auction_split` buys the remaining +1.54pp and costs a second daily firing that
    only a person can create. None of it is established: on 09-08 and 09-09 every exit
    hour available on both days paid between −1.42% and −0.05% per trade, and
    `backtest/RESULTS.md` puts the close ahead of the open on its own 37 sealed events
    for all three arms.

    WHY `amc_open` EXISTS, given that it is measurably worse than `auction_split`.
    Two reasons the +7.81% cannot see, and both are about the bmo leg:

    The +6.48% for a bmo closing auction assumes the `cls` order FILLS. On this book
    it has filled 39 of 183 (CODA) and 17 of 161 (HOFT) and then expired, because an
    auction order crosses once and takes whatever size the contra side brings. The
    rest was sold at market one to three days later with the overnight exposure that
    implies. A return that expires in the auction is not a return.

    And a bmo leg still open at 13:05 ET is still open when step 7 buys at 13:24 ET.
    The sizing divides a gross budget over the new names without knowing the old book
    is still there, so gross stacks: on 2026-09-15 VRA and FPS were held through
    LUXE's entry. `open` does not refuse it either, because a leg whose exit order is
    working is not past its exit date. A plain market sell at 13:05 ET is verifiable
    within the same session -- which is what the fill check is for -- so the budget
    the entry divides is known to be free.

    The cost is measured and is not zero: 1.31pp per trade over the same 22 trades,
    ρ 0.391 against 0.461, and 16 of 22 right instead of 17. Against `uniform_close`
    (+5.80%) it is still ahead by +0.57pp, on a paired day bootstrap of [−2.86, +3.18]
    -- which is to say, not established either. `researcher_us/scripts/edge_exit.py` scores it as
    the `amc_open_bmo_1300` policy; re-run it as days pool.
    """
    placement = exit_placement(session, ex)
    plain = ex["orders"].get("time_in_force", "day")
    if not auction_orders(ex):
        return plain
    if placement == "open":
        return "opg"
    if placement == "close":
        return "cls"
    return plain


def exit_placement(session, ex):
    """WHERE this session's exit is aimed, independent of which instrument gets it
    there: `open`, `close` or `market` (whenever the run that sends it fires).

    Placement and instrument were the same thing until 2026-09-18, and conflating
    them is what made the amc exit fail silently for a week. The mode says where the
    exit belongs; `auction_orders` says whether an auction order is the way to get it
    there. On this account it is not.
    """
    mode = exit_mode(ex)
    if mode == "uniform":
        return "close" if ex["orders"].get("exit", "market_on_close") == \
            "market_on_close" else "market"
    if mode == "bmo_close":
        return "market" if session == "amc" else "close"
    if mode == "amc_open":
        return "open" if session == "amc" else "market"
    return "open" if session == "amc" else "close"


def defer_to_session_run(placement, overdue, session_open):
    """Should THIS run leave this leg to the one that fires inside the session?

    `close` takes every leg whose exit date is today, and two runs a day call it:
    "Close AMC" at 06:05 ET and stage E at 13:05 ET. Under `auction_split` that was
    harmless -- the bmo leg wanted `cls`, and `window_for("cls")` refuses a closed
    market, so the early run could not take it even by accident. Once the instrument
    became a plain DAY order nothing refused it any more: on 2026-09-18 the 06:05 ET
    run sent TRT's bmo exit as a market DAY order, which Alpaca queues for the OPEN.
    The book was then running amc at the open AND bmo at the open, where the
    configured policy is bmo at 13:05 ET -- and bmo is the session that measured
    WORST at the open (+2.96% against +6.48% at the close, +2.58% around 10:00 ET).

    The placement is the whole of the rule. A leg aimed at the `open` is exactly what
    a pre-market run exists to place. A leg aimed at `market` means "at market, on
    the run that fires inside the session", and a closed market is the one condition
    under which this run is not that run.

    An OVERDUE leg is never deferred: its event is over, and queueing it for the open
    beats holding it another seven hours on the chance the later run fires. Nor is a
    leg deferred when the clock could not be read (`session_open is None`) -- an
    unknown clock must not become a reason a position goes unsold.

    What this costs: if stage E's own run then dies, the bmo leg is held overnight
    rather than having been sold at the open by accident. The overdue rule is the
    net -- it goes at market on the next run either way, and `open` refuses to buy a
    new book over it.
    """
    return bool(placement and placement != "open" and not overdue
                and session_open is False)


def auction_orders(ex):
    """May this account use `opg`/`cls` at all? Default NO, since 2026-09-18.

    THE AUCTION ORDERS WERE NEVER REACHING AN AUCTION. Ten auction exit legs have
    been sent from this book. One filled in full (ORCL, 12 of 12), two part-filled
    and expired (HOFT 17 of 161, CODA 39 of 183), and seven filled nothing at all --
    including LEN on 2026-09-17, a buy-to-cover of 28 shares of a $20bn homebuilder,
    which expired at 09:30:52 ET with zero. Twenty-eight shares of Lennar is not a
    liquidity problem in the opening cross of its primary listing. The instrument was.

    Two documented causes, and either is sufficient:

      * `opg` and `cls` are Elite Smart Router order types. Alpaca's own order-types
        page states it flatly -- "OPG and CLS orders are only available to Elite
        Smart Router users" -- and this is an $11.5k paper account, not an Elite one.
        The API accepts the order and it simply never reaches an auction.
      * Paper fills are simulated against the NBBO quote stream, not against a real
        auction cross, and the simulator "will receive partial fills for a random
        size 10% of the time". That is an exact description of the 17-of-161 and
        39-of-183 records, and of the zeros.

    So the mode still decides WHERE the exit is aimed (`exit_placement`) and this
    decides HOW it gets there. With auction orders off, an exit aimed at the open is
    a plain market DAY order submitted in the pre-market: Alpaca accepts it while the
    market is closed and routes it at the next open, so it fills in the first seconds
    of the regular session instead of in the 09:30 cross. That is a few basis points
    away from the auction price and about 10 points of per-trade return away from an
    order that does not sell at all.

    Set to `true` only on an account that is actually on the Elite Smart Router, and
    only after `verify` shows an auction leg filling in full.
    """
    return bool(ex["orders"].get("auction_orders", False))


def auction_window(api, tif):
    """Can an auction order of this kind go in right now? Returns (ok, note).

    Alpaca REJECTS rather than queues these inside two ET windows -- `cls` from 15:50
    to 19:00, `opg` from 09:28 to 19:00 -- so an `opg` exit cannot be placed by the
    same run that places the entries. It has to go in during the pre-market of the
    exit date, or after 19:00 ET the evening before.
    """
    if tif == "cls":
        return entry_window(api, True)
    if tif != "opg":
        # A plain DAY order is not an auction order and Alpaca no longer rejects
        # submissions while the market is closed -- it queues them and routes the
        # order once the regular session opens (confirmed against Alpaca's current
        # docs, 2026-09-16: "order-submission API calls while the market was closed
        # were [once] rejected, but now those API calls are accepted ... and the
        # orders are routed to the marketplace at the next available time"). So this
        # always says yes; the note just records whether it goes in immediately or
        # sits queued for the open.
        clk, err = api.clock()
        if not clk:
            return False, f"clock unreachable: {err}"
        return True, ("market order" if clk.get("is_open")
                      else "queued for the next open (DAY orders are accepted "
                           "and routed by Alpaca while the market is closed)")
    clk, err = api.clock()
    if not clk:
        return False, f"clock unreachable: {err}"
    # The clock's own timestamp carries the exchange offset, so read the local wall
    # clock off it rather than assuming an offset here.
    now = datetime.fromisoformat(clk["timestamp"].replace("Z", "+00:00"))
    local = now.astimezone(timezone(timedelta(hours=-4)))
    mins = local.hour * 60 + local.minute
    if 9 * 60 + 28 <= mins < 19 * 60:
        return False, (f"{local:%H:%M} ET is inside Alpaca's opg rejection window "
                       "(09:28-19:00 ET); submit in the pre-market of the exit date")
    return True, f"opg accepted at {local:%H:%M} ET"


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


def order_body(ticker, qty, side, ex, moc=True, tif=None):
    o = {"symbol": ticker, "qty": str(int(qty)), "side": side,
         "type": "market", "extended_hours": False}
    if tif:
        o["time_in_force"] = tif                   # cls, opg, or day, chosen by caller
    elif moc:
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
                  f"{c['notional_usd']:>11,.0f}"
                  f"{c.get('pct_of_equity') or 0:>7.1f}"
                  f"{c.get('pct_of_adv') or 0:>7.2f}"
                  f"{c['dollar_volume_usd']/1e6:>9.1f}m{c['binding_cap']:>13s}"
                  f"  {c['entry_date']} -> {c['exit_date']}")
        # Where the share counts came from. A name sized off the baseline is sized
        # off a price captured when the run started, which can be hours old.
        stale_px = [c for c in plan["positions"]
                    if c.get("price_source", "").startswith("sealed baseline")]
        drift = [c for c in plan["positions"] if c.get("baseline_drift_pct") is not None]
        if drift:
            worst = max(drift, key=lambda c: abs(c["baseline_drift_pct"]))
            print(f"sized on live prices; the baseline has drifted a median "
                  f"{statistics.median(abs(c['baseline_drift_pct']) for c in drift):.2f}% "
                  f"since the run sealed it, worst {worst['ticker']} "
                  f"{worst['baseline_drift_pct']:+.2f}%")
        if stale_px:
            print(f"! {', '.join(c['ticker'] for c in stale_px)} sized off the SEALED "
                  f"BASELINE spot, not a live price"
                  + (f" ({plan['reference_price_error']})"
                     if plan.get("reference_price_error") else "")
                  + " — the %eq and %adv caps are against a stale price for these.")
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
        gross = sum(c["notional_usd"] for c in plan["positions"])
        net = sum(c["notional_usd"] * (1 if c["side"] == "buy" else -1)
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

    # Never stack a new book on an unsold one. With `flatten_before_entry` on, the
    # flatten below makes this impossible; with the per-session exit it is off, and
    # then a missed exit run is the failure that has to be loud.
    today = None
    if api.usable:
        clk, _ = api.clock()
        today = clk["timestamp"][:10] if clk else None
    if today:
        pos, _ = api.call("GET", "/v2/positions")
        held = {p["symbol"] for p in pos} if isinstance(pos, list) else None
        stale = overdue_legs(today, held=held)
        if stale and not a.allow_stale:
            for s in stale:
                print(f"  ! {s['symbol']:8s}{s['side']:5s}due {s['exit_date']}  "
                      f"{s['run']}")
            raise SystemExit(
                f"refusing: {len(stale)} position(s) are past their exit date with no "
                f"exit submitted. Close them first:\n"
                f"  python3 researcher_us/scripts/alpaca_trade.py close "
                f"--scan 'research/*/*/*/edge' --submit\n"
                f"(--allow-stale to enter anyway, which stacks a second book on top)")

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
    use_moc = ex["orders"].get("entry", "market") == "market_on_close"
    open_ok, open_note = (entry_window(api, use_moc) if (a.submit and not blocked)
                          else (False, "dry run"))
    print(f"\nsubmit: {'blocked — ' + blocked if blocked else open_note}"
          f" ({'market-on-close' if use_moc else 'market'})")

    today = None
    if api.usable:
        clk, _ = api.clock()
        today = clk["timestamp"][:10] if clk else None
    state = load_orders(a.run)
    if flat is not None and flat.get("submitted"):
        state["log"].append(flat)

    # The quote at submission, for every name, in one call immediately before the
    # orders go out. Without this there is no way to tell execution cost from the
    # day's drift: on 2026-09-10 the fills looked 0.83% adverse against the plan,
    # but the plan's reference was four hours old, so the run log could only say
    # "this number is not slippage". `orders.entry` (market vs market_on_close) is
    # supposed to be decided on fill quality, and that decision needs this.
    submit_quotes, sq_err = ({}, None)
    if api.usable:
        raw_q, sq_err = api.latest_quotes([c["ticker"] for c in plan["positions"]])
        submit_quotes = {t: quote_snapshot(q) for t, q in raw_q.items()}
        if sq_err:
            print(f"  ! quotes at submit unavailable ({sq_err}); fills will not be "
                  f"measurable against the spread")

    for c in plan["positions"]:
        reason = blocked
        if not reason and today and c["entry_date"] != today and not a.force_date:
            reason = f"entry date is {c['entry_date']}, today is {today} (--force-date)"
        entry_moc = use_moc
        if not reason and not open_ok:
            if use_moc and a.allow_market_fallback:
                entry_moc = False                # a market order still works
            elif use_moc:
                reason = (f"MOC unavailable ({open_note}); --allow-market-fallback to "
                          "send a plain market order instead")
            else:
                reason = (f"cannot send a market order: {open_note}. A market order "
                          "outside the session does not fill at a price this stage "
                          "has measured.")
        body = order_body(c["ticker"], c["qty"], c["side"], ex, moc=entry_moc)
        cid = client_id(a.run, c["ticker"], "entry")
        rec = send(api, body, cid, a.submit, reason)
        rec.update({"leg": "entry", "entry_date": c["entry_date"],
                    "exit_date": c["exit_date"], "event_date": c["event_date"],
                    "session": c["session"], "key": c["key"], "value": c["value"],
                    "spot_at_plan": c["spot"],
                    "price_at_plan": c.get("price_used_usd"),
                    "price_source_at_plan": c.get("price_source"),
                    "quote_at_submit": submit_quotes.get(c["ticker"]),
                    "quote_at_submit_error": sq_err})
        upsert(state["entries"], rec)
        print(f"  {c['ticker']:8s}{'SENT' if rec['submitted'] else 'not sent'}"
              f"  {rec.get('order_id') or rec.get('reason')}")
    if blocked:
        print(f"\nnothing submitted, so {orders_path(a.run).name} was not touched — "
              f"the plan is in alpaca-plan.json")
        return
    state["log"].append({"utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "action": "open", "window": open_note,
                         "entry": ("market_on_close" if use_moc else "market"),
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
    mode = exit_mode(ex)
    by_session = mode != "uniform" and not a.now
    use_moc = ex["orders"].get("exit", "market_on_close") == "market_on_close" and not a.now
    moc, moc_note = ((entry_window(api, True) if use_moc else (True, "market order"))
                     if (a.submit and not blocked) else (False, "dry run"))
    # One clock call per instrument, not per position.
    win = {}

    def window_for(tif):
        if tif not in win:
            win[tif] = (auction_window(api, tif) if (a.submit and not blocked)
                        else (False, "dry run"))
        return win[tif]
    today = None
    session_open = None
    if api.usable:
        clk, _ = api.clock()
        today = clk["timestamp"][:10] if clk else None
        session_open = clk.get("is_open") if clk else None
    print(f"closing across {len(runs)} run(s), today {today}, "
          f"{'blocked — ' + blocked if blocked else moc_note}"
          + (f"  [exit_mode {mode}: amc -> {exit_tif_for('amc', ex)}, "
             f"bmo -> {exit_tif_for('bmo', ex)}]" if by_session else ""))

    for run in runs:
        state = load_orders(run)
        for e in state["entries"]:
            if a.submit and not e.get("submitted"):
                continue                    # in a dry run, show them all instead
            cid = client_id(run, e["symbol"], "exit")
            # A submitted exit is not a closed position. HOFT's exit on 2026-09-11 went
            # in as `cls`, filled 17 of 161 and expired; the record said submitted, so
            # every later run skipped it here and 144 shares sat open with nothing in
            # the repo that would ever sell them. Submission is an intention — the only
            # evidence a leg is finished is that the account no longer holds it. So the
            # skip stands only while the position is really gone, and the re-send below
            # is sized to what Alpaca reports it still holds, never to the entry qty.
            prior = [x for x in state["exits"]
                     if x.get("closes") == e["client_order_id"] and x.get("submitted")]
            if prior:
                still_held = None
                if api.usable:
                    pos, _ = api.position(e["symbol"])
                    still_held = abs(float(pos.get("qty", 0))) if pos else 0.0
                if still_held is None or still_held == 0.0:
                    continue
                # Held shares are not enough on their own: a `cls` order sent earlier
                # in this same session sits at `new` until the auction, and the
                # position stays open the whole time. Re-sending then would sell the
                # position twice, which is the other half of the invariant. So a leg
                # is only retried once every prior exit order is *dead* at the broker
                # — the stored status is the status at submission and cannot say that,
                # so it is re-read here.
                if any(order_live(api, x) for x in prior):
                    print(f"  {run} {e['symbol']:8s} exit already working at the "
                          f"broker; leaving it alone")
                    continue
                # Alpaca rejects a duplicate client_order_id, so a retry needs its own.
                # Suffixing keeps the original record intact and makes the retry legible
                # in alpaca-orders.json rather than overwriting the history of the leg.
                cid = f"{cid}-r{len(prior) + 1}"
                print(f"  {run} {e['symbol']:8s} exit submitted {len(prior)}x but "
                      f"{still_held:g} still held; re-sending as {cid}")
            # A leg whose exit date has PASSED is overdue, not finished. The old rule
            # closed only `exit_date == today`, so one missed run left a position that
            # no later run would ever sell. Overdue legs go at plain market: their
            # auction is gone, and holding on for the next one is not a decision
            # anything here measured.
            xd = e.get("exit_date")
            overdue = bool(today and xd and xd < today)
            due = a.all or overdue or (today and xd == today)
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
            tif = exit_tif_for(e.get("session"), ex) if by_session else None
            place = exit_placement(e.get("session"), ex) if by_session else None
            if overdue:
                tif = ex["orders"].get("time_in_force", "day")
                place = "market"
                print(f"  {run} {e['symbol']:8s} overdue since {xd}; going at market")
            elif (not reason
                  and defer_to_session_run(place, overdue, session_open)):
                reason = ("market placement, and the market is closed: this leg exits "
                          "at market on the run that fires inside the session, not "
                          "queued for the open by this one")
            if tif:
                ok, note = window_for(tif)
                if not ok and prior and not overdue:
                    # The auction this leg wanted is gone AND the order sent to it is
                    # dead with the shares still held. RLGT on 2026-09-15: the 06:05
                    # ET `opg` filled none of 224, and the 13:05 ET retry asked for
                    # `opg` again inside Alpaca's 09:28-19:00 rejection window, so
                    # nothing was sent and the position sat another full day. Holding
                    # for tomorrow's auction is not a decision anything here measured;
                    # it is one more night of exposure on a leg whose event is over.
                    mkt = ex["orders"].get("time_in_force", "day")
                    ok2, note2 = window_for(mkt)
                    if ok2:
                        print(f"  {run} {e['symbol']:8s} {tif} unavailable ({note}) and "
                              f"the earlier exit died unfilled; going at market")
                        tif, ok, note = mkt, ok2, note2
                if not reason and not ok:
                    reason = f"{tif} unavailable ({note})"
            elif not reason and use_moc and not moc:
                reason = f"MOC unavailable ({moc_note}); rerun with --now for a " \
                         "market order or before the cutoff"
            side = "sell" if e["side"] == "buy" else "buy"
            body = order_body(e["symbol"], qty or e["qty"], side, ex,
                              moc=use_moc, tif=tif)
            rec = send(api, body, cid, a.submit, reason)
            rec.update({"leg": "exit", "closes": e["client_order_id"],
                        "exit_date": e.get("exit_date"), "position_qty_at_close": held,
                        # WHERE this exit was aimed, beside the instrument that got
                        # it there. Without it the record cannot distinguish an exit
                        # meant for the open from one that merely went at market,
                        # which is the whole of what changed on 2026-09-18.
                        "placement": place or "market"})
            upsert(state["exits"], rec)
            rec["time_in_force"] = body["time_in_force"]
            print(f"  {run} {e['symbol']:8s}{(e.get('session') or '?'):4s}"
                  f"{body['time_in_force']:4s}"
                  f"{'SENT' if rec['submitted'] else 'not sent'}"
                  f"  {rec.get('order_id') or rec.get('reason')}")
        if blocked:
            continue                        # a dry run records nothing
        state["log"].append({"utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                             "action": "close", "all": bool(a.all), "moc": moc_note,
                             "exit_mode": mode,
                             "windows": {k: v[1] for k, v in win.items()}})
        save_orders(run, state)
        print(f"  wrote {orders_path(run)}")

    # A submitted sell is not a sold position, and the session is about to end. Wait
    # out `orders.fill_check_seconds` and look. An auction TIF will still read
    # `working` here and that is correct -- what this catches now is the order that
    # was rejected, expired or never left the gate, which used to survive as
    # `submitted: true` until the next run 17 to 24 hours later.
    wait = (a.verify_after if getattr(a, "verify_after", None) is not None
            else int(ex["orders"].get("fill_check_seconds", 300)))
    if not blocked and a.submit and wait >= 0:
        verify_exits(api, runs, ex, a.submit, blocked, wait_s=wait,
                     fix=bool(ex["orders"].get("fill_check_fix", True)))


def cmd_verify(a, api, ex):
    if not api.usable:
        sys.exit("verify needs ALPACA_API_KEY_ID / ALPACA_API_SECRET_KEY")
    runs = [a.run] if a.run else sorted(
        p for pat in a.scan for p in glob.glob(pat) if orders_path(p).exists())
    if not runs:
        print("no run with an alpaca-orders.json to verify")
        return
    blocked = (guard(api, ex, a.submit, a.live_account_i_understand) if a.fix
               else "--fix not given")
    verify_exits(api, runs, ex, a.submit, blocked, wait_s=a.wait, fix=a.fix)


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
            # Fill against the quote captured at submission. This is the only
            # comparison here that is execution cost rather than the day's drift:
            # both prices are from the same instant. Positive = paid away from the
            # mid, in the direction that costs money on the side actually traded.
            fap = (o or {}).get("filled_avg_price")
            q = e.get("quote_at_submit") or {}
            slip = half = None
            if fap and q.get("mid"):
                sgn = 1 if e["side"] == "buy" else -1
                slip = round(100 * (float(fap) - q["mid"]) / q["mid"] * sgn, 3)
                half = round((q.get("spread_pct") or 0) / 2.0, 3)
            rows.append({"client_order_id": e["client_order_id"], "leg": e.get("leg"),
                         "symbol": e["symbol"], "side": e["side"],
                         "status": (o or {}).get("status") or oerr,
                         "filled_qty": (o or {}).get("filled_qty"),
                         "filled_avg_price": fap,
                         "mid_at_submit": q.get("mid"),
                         "spread_pct_at_submit": q.get("spread_pct"),
                         "slippage_vs_mid_pct": slip,
                         "half_spread_pct": half,
                         "price_at_plan": e.get("price_at_plan"),
                         "drift_since_plan_pct": (
                             round(100 * (float(fap) - e["price_at_plan"])
                                   / e["price_at_plan"], 3)
                             if fap and e.get("price_at_plan") else None),
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
        measured = [r for r in rows if r.get("slippage_vs_mid_pct") is not None]
        if measured:
            print(f"\n  {'':6s}{'sym':8s}{'vs mid':>9s}{'½spread':>9s}{'drift':>9s}")
            for r in measured:
                dr = r["drift_since_plan_pct"]
                print(f"  {'':6s}{r['symbol']:8s}"
                      f"{r['slippage_vs_mid_pct']:>+9.3f}"
                      f"{r['half_spread_pct']:>9.3f}"
                      + (f"{dr:>+9.3f}" if dr is not None else f"{'—':>9s}"))
            avg = statistics.mean(r["slippage_vs_mid_pct"] for r in measured)
            print(f"  {'':6s}{'mean':8s}{avg:>+9.3f}   <- execution cost against the "
                  f"mid at submission. `drift` is the day moving between plan and "
                  f"fill and is NOT execution cost.")
            print(f"  {'':6s}orders.entry is '{ex['orders'].get('entry','market')}'; "
                  f"switch to market_on_close if this mean stays above the half-spread.")
        elif rows:
            print(f"  (no quote captured at submission, so fill quality against the "
                  f"spread cannot be measured for these — orders placed before "
                  f"2026-09-10 predate that capture)")
        for p in open_pos:
            print(f"  OPEN  {p['symbol']:8s}{p['qty']:>8s} @ {p['avg_entry_price']}  "
                  f"{float(p['unrealized_plpc'])*100:+.2f}%")
        out["runs"].append({"run": run, "orders": rows, "open_positions": open_pos})
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {a.out}")


# ---------------------------------------------------------------- cli

def cmd_assets(a, api, ex):
    """Per-name session and tradability for EVERY name in a run, floor or no floor.

    The note has to state, for each name it ranks, which session carries the print
    and whether the name could be traded at all. `plan` cannot answer the second
    question for the whole table: it checks borrow only for names that already
    cleared the conviction floor, because that is the only set it is about to size.
    So a below-floor name has never been asked, and a note that filled the column in
    anyway would be inventing the answer for exactly the rows nobody checked.

    Tradability here is deliberately INDEPENDENT of the conviction floor. The floor
    is a selection decision about whether the sign means anything; capacity and
    borrow are facts about the name. Keeping them in separate columns is what lets a
    reader see that a name was skipped for conviction rather than because it could
    not be traded -- and, on 2026-09-14, that every one of the four floor-clearing
    NEGATIVES was untradeable while the traded book was long-only.

    Read-only: it places nothing and it is not gated on --submit. With no usable
    credentials the borrow column reports `unknown` rather than a guess.

    Since 2026-09-15 the verdict separates LIQUIDITY from BORROW. Liquidity is a
    property of the name (`ok`, `thin` under `thin_dollar_volume_usd`, `below floor`)
    and holds at every broker; borrow is one broker's answer on one day, and a short
    Alpaca will not lend is routinely borrowable at IBKR. So a short that clears the
    turnover floor but is not lendable here reads `elsewhere`, never `no`. The
    operator's rule is not to trade into a limited-liquidity warning, which is what
    `thin` stands in for; nothing in this script drops a name on it.

    BORROW IS A SNAPSHOT, so this prefers the run's own `alpaca-plan.json` over a
    live lookup whenever one exists. Alpaca re-checks shortability daily: COE was
    recorded `shortable: false` by the 2026-09-14 plan at 17:35 UTC and read
    borrowable the next morning. A note regenerated a day later against a live
    lookup would therefore say the book could have shorted a name the run had
    already refused, and would contradict the run log sitting beside it. `--live`
    forces the current answer when the question really is "can I borrow it now".
    """
    run = Path(a.run)
    scores, baselines = load_run(run)
    # {ticker: (shortable, reason)} as the plan recorded it, for names it examined.
    planned, plan_utc = {}, None
    ppath = run / "alpaca-plan.json"
    if not getattr(a, "live", False) and ppath.exists():
        try:
            pj = json.loads(ppath.read_text(encoding="utf-8"))
            plan_utc = pj.get("generated_utc") or pj.get("as_of_utc")
            # `positions` is the taken set and `rejected` the refused one. NOT
            # `orders` -- that key holds the order settings dict, and listing it
            # yields its keys as strings, which then raise inside this try and
            # silently emptied `planned` so every row fell through to a live
            # lookup. Only dicts, and only names the plan actually examined.
            for r in (pj.get("positions") or []) + (pj.get("rejected") or []):
                if isinstance(r, dict) and r.get("asset_checked"):
                    planned[r["ticker"]] = (r.get("shortable"), r.get("reason"))
        except Exception:
            planned = {}
    bench = ex.get("benchmark") or {}
    floor = float(bench.get("min_conviction") or 0)
    min_dv = float(bench.get("min_dollar_volume_usd") or 0)
    # Below this the note calls the name THIN. It is not a floor and nothing is
    # dropped on it: it is the proxy for the "limited liquidity" warning a broker
    # shows, and the operator's rule is not to trade into one. $1m/day unless
    # config says otherwise -- six of the first 22 long/short positions sat under
    # it, and the headline returns on such names are upper bounds (VRA printed
    # +23% at the open and was +12% within the same five-minute bar on $288k/day).
    thin_dv = float(bench.get("thin_dollar_volume_usd") or 1_000_000)
    key = bench.get("key", "impact_sum")

    print(f"{run}   {'paper' if api.is_paper else 'live'} {api.base}"
          if api.usable else f"{run}   no credentials: borrow is unknown")
    print(f"floor |{key}| >= {floor}, turnover floor ${min_dv/1e6:.1f}m, "
          f"thin below ${thin_dv/1e6:.1f}m\n")
    print(f"{'ticker':8}{'session':9}{'event':12}{key:>10}{'floor':>7}"
          f"{'turnover':>11}{'liquidity':>12}{'Alpaca':>8}  tradable")

    rows = []
    for row in scores.get("ranking", []):
        t = row.get("ticker")
        b = baselines.get(t) or {}
        tape = b.get("tape") or {}
        spot, vol = tape.get("spot"), tape.get("avg_volume_20d")
        dv = (spot * vol) if (spot and vol) else None
        val = row.get(key)
        signed = isinstance(val, (int, float))
        short_side = signed and val < 0

        tradable = shortable = None
        source = "live"
        if t in planned:
            shortable = planned[t][0]
            tradable = shortable if short_side else True
            source = "plan"
        elif api.usable:
            asset, _ = api.asset(t)
            if asset:
                tradable = asset.get("shortable") if short_side else asset.get("tradable")
                shortable = asset.get("shortable")

        # Two facts, kept apart because they answer different questions and were
        # once merged into one "no". Liquidity is a property of the NAME and holds at
        # every broker. Borrow is a property of ONE broker on one day: a short Alpaca
        # will not lend is routinely borrowable at IBKR, so "not shortable at Alpaca"
        # is a check to make elsewhere, not a verdict that the name is untradeable.
        # The reason column answers "could this be traded", never "should it be".
        liquidity = ("unknown" if dv is None else
                     "below floor" if dv < min_dv else
                     "thin" if dv < thin_dv else "ok")
        if dv is None:
            verdict, why = "no", "no 20-day volume, so capacity is unknown"
        elif dv < min_dv:
            verdict, why = "no", f"turnover ${dv/1e6:.2f}m below the ${min_dv/1e6:.1f}m floor"
        elif tradable is None:
            # No answer from the plan and none from a lookup. A long needs no
            # borrow, so it is tradable on turnover alone; a short is unknown.
            verdict, why = (("unknown", "borrow not checked (no credentials)"
                             if not api.usable else "asset lookup failed")
                            if short_side else ("yes", "long side, turnover clears"))
        elif not tradable and short_side:
            verdict, why = "elsewhere", ("not lendable at Alpaca on this snapshot; "
                                         "check borrow at IBKR before calling it untradeable")
        elif not tradable:
            verdict, why = "no", "not tradable at Alpaca"
        else:
            verdict, why = "yes", ("short side, Alpaca borrow available" if short_side
                                   else "long side, turnover clears")
        if liquidity == "thin" and verdict in ("yes", "elsewhere"):
            why += f"; THIN at ${dv/1e6:.2f}m/day — expect a limited-liquidity warning"

        borrow = ("n/a" if not short_side else
                  "unknown" if shortable is None else
                  "yes" if shortable else "no")
        print(f"{t:8}{str(b.get('session') or '?'):9}"
              f"{str(b.get('event_date') or '?'):12}"
              f"{(f'{val:+.2f}' if signed else '?'):>10}"
              f"{('yes' if signed and abs(val) >= floor else '-'):>7}"
              f"{(f'${dv/1e6:.2f}m' if dv else '?'):>11}{liquidity:>12}{borrow:>8}"
              f"  {verdict} — {why}")
        rows.append({"ticker": t, "session": b.get("session"),
                     "event_date": b.get("event_date"), key: val,
                     "clears_floor": bool(signed and abs(val) >= floor),
                     "dollar_volume_usd": round(dv) if dv else None,
                     "liquidity": liquidity, "thin_dollar_volume_usd": thin_dv,
                     "shortable_alpaca": shortable, "shortable": shortable,
                     "borrow_source": source,
                     "tradable": verdict, "reason": why})

    # Say which rows are the run's own answer and which were asked just now, so a
    # reader can tell a reconstructed cell from a recorded one.
    live_short = [r["ticker"] for r in rows
                  if r["borrow_source"] == "live" and r["shortable"] is not None]
    if planned:
        print(f"\nborrow as the run recorded it at {plan_utc}"
              + (f"; asked live just now for {', '.join(live_short)} "
                 "(the plan never checked them -- they were below the floor)"
                 if live_short else ""))
    elif live_short:
        print("\nborrow asked live just now; no alpaca-plan.json to read it from")

    out = Path(a.out) if a.out else run / "alpaca-assets.json"
    out.write_text(json.dumps({"run": str(run), "key": key,
                               "conviction_floor": floor,
                               "min_dollar_volume_usd": min_dv,
                               "thin_dollar_volume_usd": thin_dv,
                               "tradable_values": {
                                   "yes": "turnover clears and, for a short, Alpaca lends it",
                                   "elsewhere": "turnover clears; Alpaca will not lend it on "
                                                "this snapshot -- check IBKR",
                                   "no": "turnover below the floor, or not tradable at all",
                                   "unknown": "not checked"},
                               "credentials": bool(api.usable),
                               "borrow_as_of": plan_utc or "live lookup",
                               "names": rows}, indent=1) + "\n", encoding="utf-8")
    print(f"\nwrote {out}")
    return rows


def cmd_mode(a, api, ex):
    """Print the effective execution settings, and optionally assert one.

    This exists so a Routine prompt can GUARD on the configuration instead of
    describing it. The second exit Routine's step 1 used to read "if
    `orders.exit_mode` is not `auction_split`, do nothing" -- a config key read by
    eye, by a session, from a YAML file whose keys have already been renamed once.
    Read by eye it can be read wrong in both directions: a missing key looks like a
    guard that was clearly meant to pass, and a renamed key looks like a guard that
    can never pass. Neither failure says anything in the run log.

    `--require <mode>[,<mode>...]` exits 0 when one of those modes is configured and 1
    when none is, so the guard becomes one command whose answer is in the exit status:

        python3 researcher_us/scripts/alpaca_trade.py mode --require auction_split,amc_open || exit 0

    `--require-exit-tif <tif>` is the better guard for the second exit Routine, and it
    is the one its prompt should use. That Routine exists for exactly one reason: some
    session's exit is an `opg` order, and only a pre-market firing can place one. Ask
    that question directly and the guard keeps working when a mode is renamed or added
    -- which has now happened twice. A guard naming `auction_split` alone silently
    stopped doing anything the moment `amc_open` shipped, while still reporting a tidy
    no-op every morning.

        python3 researcher_us/scripts/alpaca_trade.py mode --require-exit-tif opg || exit 0
    """
    enabled = bool(ex.get("enabled"))
    mode = exit_mode(ex)
    orders = ex["orders"]
    print(f"execution.enabled      {str(enabled).lower()}")
    print(f"orders.exit_mode       {mode}")
    print(f"orders.flatten_before_entry  {orders.get('flatten_before_entry', True)}")
    print(f"orders.entry           {orders.get('entry', 'market')}")
    print(f"orders.exit            {orders.get('exit', 'market_on_close')}")
    print(f"orders.auction_orders  {auction_orders(ex)}"
          + ("" if auction_orders(ex) else
             "   <- opg/cls are Elite Smart Router order types and did not fill on "
             "this account (1 of 10 legs); an exit aimed at the open goes as a "
             "market DAY order queued in the pre-market instead"))
    print(f"exit placement         amc -> {exit_placement('amc', ex)}, "
          f"bmo -> {exit_placement('bmo', ex)}")
    print(f"exit instrument        amc -> {exit_tif_for('amc', ex)}, "
          f"bmo -> {exit_tif_for('bmo', ex)}")
    if not auction_orders(ex) and "close" in (exit_placement('amc', ex),
                                              exit_placement('bmo', ex)):
        print("  WARNING: a session is aimed at the CLOSING auction and auction "
              "orders are off, so its exit goes at plain market whenever the run "
              "that sends it fires -- which is not the close. That is a different "
              "exit from the measured one.")
    print(f"orders.fill_check_seconds    {orders.get('fill_check_seconds', 300)}")
    print(f"orders.fill_check_fix        {orders.get('fill_check_fix', True)}")
    if a.require:
        want = [m.strip() for m in a.require.split(",") if m.strip()]
        bad = [m for m in want if m not in EXIT_MODES]
        if bad:
            raise SystemExit(f"--require {', '.join(bad)}; expected one of "
                             + ", ".join(EXIT_MODES))
        if not enabled:
            print(f"\nrequire {a.require}: NO -- execution.enabled is false")
            raise SystemExit(1)
        if mode not in want:
            print(f"\nrequire {a.require}: NO -- the configured mode is {mode}")
            raise SystemExit(1)
        print(f"\nrequire {a.require}: yes")
    if a.require_exit_tif:
        want = a.require_exit_tif
        tifs = {s: exit_tif_for(s, ex) for s in ("amc", "bmo")}
        places = {s: exit_placement(s, ex) for s in ("amc", "bmo")}
        # `opg` and `cls` are asked for as a PLACEMENT and not as a literal
        # instrument. The Routine that pastes `--require-exit-tif opg` is asking one
        # question -- is there an exit here that has to go in before the open, which
        # only a pre-market firing can place -- and the answer did not change when
        # the instrument stopped being an auction order on 2026-09-18. A guard that
        # matched the literal string would have failed shut that day and reported a
        # tidy no-op every morning while the amc legs went unsold, which is exactly
        # the failure this guard replaced.
        family = {"opg": "open", "cls": "close"}.get(want)
        hit = [s for s in ("amc", "bmo")
               if tifs[s] == want or (family and places[s] == family)]
        if not enabled:
            print(f"\nrequire-exit-tif {want}: NO -- execution.enabled is false")
            raise SystemExit(1)
        if not hit:
            print(f"\nrequire-exit-tif {want}: NO -- no session exits there "
                  f"(amc -> {places['amc']}/{tifs['amc']}, "
                  f"bmo -> {places['bmo']}/{tifs['bmo']})")
            raise SystemExit(1)
        how = ", ".join(f"{s} {places[s]} as {tifs[s]}" for s in hit)
        print(f"\nrequire-exit-tif {want}: yes ({how})")
        if family and not any(tifs[s] == want for s in hit):
            print(f"  NOTE: matched on placement, not on the literal tif. "
                  f"orders.auction_orders is {auction_orders(ex)}, so the exit aimed "
                  f"at the {family} goes as a plain market order queued for it. The "
                  f"question this Routine exists to ask -- is there an exit that must "
                  f"be placed before the open -- is still yes.")


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
    p.add_argument("--allow-stale", action="store_true",
                   help="enter even though positions are past their exit date unsold")

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
    p.add_argument("--verify-after", type=int, metavar="SECONDS",
                   help="seconds to wait before re-reading the exits at the broker "
                        "(default orders.fill_check_seconds, 300)")
    p.add_argument("--no-verify", dest="verify_after", action="store_const", const=-1,
                   help="submit and exit without checking whether the sells filled")

    p = sub.add_parser("verify", help="re-read submitted exits at the broker and "
                                      "report what actually filled")
    common(p, run_required=False)
    p.add_argument("--scan", action="append", default=[])
    p.add_argument("--wait", type=int, default=0,
                   help="seconds to wait before looking (default 0)")
    p.add_argument("--fix", action="store_true",
                   help="re-send at plain market any leg still held behind a dead "
                        "order (needs --submit)")

    p = sub.add_parser("status", help="reconcile orders and positions against a run")
    common(p, run_required=False)
    p.add_argument("--scan", action="append", default=[])
    p.add_argument("--out")

    p = sub.add_parser("assets", help="per-name session and tradability for every "
                                      "name in a run (read-only; places nothing)")
    common(p)
    p.add_argument("--out")
    p.add_argument("--live", action="store_true",
                   help="ask the broker now instead of using the borrow state the "
                        "run's own alpaca-plan.json recorded")

    p = sub.add_parser("mode", help="print the effective execution settings; "
                                    "--require asserts one and sets the exit status")
    p.add_argument("--require", help="comma-separated exit modes; exit 1 unless one "
                                     "of them is configured and execution is enabled")
    p.add_argument("--require-exit-tif", metavar="TIF",
                   help="exit 1 unless some session's exit uses this instrument "
                        "(opg, cls, day) and execution is enabled. Survives a mode "
                        "being renamed; use it in the second exit Routine's guard")
    p.add_argument("--base", help=argparse.SUPPRESS)

    a = ap.parse_args()
    if getattr(a, "scan", None) == []:
        a.scan = ["research/*/*/*/edge"]
    cfg = config()
    ex = execution_config(cfg)
    api = Alpaca(base=a.base)
    {"plan": cmd_plan, "open": cmd_open, "close": cmd_close,
     "flatten": cmd_flatten, "status": cmd_status, "mode": cmd_mode,
     "assets": cmd_assets, "verify": cmd_verify}[a.cmd](a, api, ex)


if __name__ == "__main__":
    main()
