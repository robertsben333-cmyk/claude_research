#!/usr/bin/env python3
"""Trade stage EU's panel book at Interactive Brokers: sell everything at the start of
the run, buy the panel's names at the end of it.

Stage EU fires at 15:30 Amsterdam, two hours before the European close, and seals for
the NEXT session, because Europe reports before the open. So the day looks like this:

    step 0s   (15:3x CET)  flatten   sell yesterday's book, whose print came out this
                                     morning, and cancel anything still working
    step 6b   (~16:20 CET) open      buy (or short) today's panel names, which report
                                     before tomorrow's open

The scored window is close(D-1) -> close(D). The trade holds from about two hours
before the close of D-1 to about two hours before the close of D, so it carries the
whole reaction and misses the last two hours of each day. That is the operator's
design (2026-11-08), not something measured.

THE EU PANEL HAS NO MEASURED EDGE YET. The 2026-10-21 study (live, 7 days, 45 names)
put the panel at rho +0.22, p 0.19, with only four names at or above 70. Real money on
it is a decision to find out, not a finding.

The rule is `execution_eu` in config/pipeline.yaml, and it reuses stage E-P's shape:

    entry    panel_pct >= selection.min_panel_pct with all four judges present,
             side from the panel, never at or below zero_weight_pct
    weight   panel_pct - zero_weight_pct, linear, capped per name, what a capped name
             cannot take goes to the rest (alpaca_trade.allocate, the same function)
    budget   gross_pct_of_equity of net liquidation, minus anything still held

and then HARD LIMITS that sit on top of every computed number and are checked again
immediately before each order is sent:

    max_gross_base   most the book may hold, in the account's base currency
    max_name_base    most one name may hold
    max_names        most names in one book
    max_orders_per_run
    max_price_gap_pct  a live price this far from the sealed spot means the contract
                       lookup or the price is wrong, so the name is dropped

Nothing is sent unless ALL of these hold: `execution_eu.enabled` is true, `--submit`
is given, the credentials are in the environment, IBKR_ACCOUNT_ID names an account the
login can see, that account's prefix matches `environment` (DU = paper, U = live), and
the environment variable IBKR_ENVIRONMENT says the same as the config. Two switches
in two places, so neither a config edit nor a pasted variable alone moves real money.

Commands:
    mode                         print the effective settings; exit 1 unless enabled
    check                        connect, show account, equity, positions, open orders
    contracts --run <RUN>        resolve every panel name to an IBKR contract, no orders
    plan --run <RUN> [--offline --equity N --base EUR]
    flatten --run <RUN> [--submit]
    open --run <RUN> [--submit]
    status --run <RUN>
    handoff --run <RUN>          cloud side of the executor route: write the book
                                 request the server's eu_executor.py waits for

Two ways to reach IBKR (`execution_eu.auth`): `tws` (since 2026-11-08 the live route:
IB Gateway + IBC on the operator's own server, driven by eu_executor.py there, because
IBKR gives OAuth to institutional clients only) and `oauth` / `gateway` over the Client
Portal REST API (ibkr_client.py, kept for a future OAuth for individuals).

Every command that touches orders writes `<RUN>/ibkr-orders.json`.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta, date
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO / "researcher_us" / "scripts"))

import eu_market  # noqa: E402

CLIENT_PREFIX = "eu"
OPEN_LOCAL = {"uk": "08:00", "fi": "10:00"}          # everyone else opens 09:00 local
DEFAULT_EXCHANGES = {
    "uk": ["LSE"], "de": ["IBIS", "IBIS2"], "fr": ["SBF"], "se": ["SFB"],
    "dk": ["CPH", "KFB"], "no": ["OSE"], "fi": ["HEX", "HMB"], "it": ["BVME"],
    "es": ["BM"], "pl": ["WSE"],
}


# ------------------------------------------------------------------ config

def config():
    import yaml
    return yaml.safe_load((REPO / "config" / "pipeline.yaml").read_text(encoding="utf-8"))


def eu_config(cfg=None):
    cfg = cfg if cfg is not None else config()
    ex = dict(cfg.get("execution_eu") or {})
    for k in ("selection", "sizing", "limits", "orders"):
        ex[k] = dict(ex.get(k) or {})
    if not isinstance(ex.get("enabled"), bool):
        raise SystemExit("execution_eu.enabled must be an explicit true or false")
    if ex.get("environment") not in ("paper", "live"):
        raise SystemExit("execution_eu.environment must be 'paper' or 'live'")
    return ex


# ------------------------------------------------------------------ the run

def load_run(run):
    run = Path(run)
    p = run / "edge-scores-panel.json"
    if not p.exists():
        raise SystemExit(f"no {p}: the panel has not been scored for this run")
    panel = json.loads(p.read_text(encoding="utf-8"))
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        baselines[b.get("ticker") or f.stem] = b
    uni = {}
    if (run / "universe.json").exists():
        uni = json.loads((run / "universe.json").read_text(encoding="utf-8"))
    return panel, baselines, uni


def spot_local(b):
    """The sealed spot in the trading currency (Yahoo quotes London in pence)."""
    tape = b.get("tape") or {}
    s, ccy = tape.get("spot"), tape.get("currency")
    if not s:
        return None, ccy
    if ccy in ("GBp", "GBX"):
        return s / 100.0, "GBP"
    return float(s), ccy


def select(panel, baselines, ex):
    """Pure: the panel rows this rule buys, and why every other row was not bought."""
    sel = ex["selection"]
    zero = float(sel.get("zero_weight_pct", 60))
    floor = max(float(sel.get("min_panel_pct", 70)), zero)
    min_dv = float(sel.get("min_turnover_usd", 0) or 0)
    sides = set(sel.get("sides") or ["long", "short"])
    allowed = set(sel.get("markets") or DEFAULT_EXCHANGES)
    full = not panel.get("members_missing")
    taken, rejected = [], []
    for row in panel.get("ranking", []):
        t = row.get("ticker")
        pct, side = row.get("panel_pct"), row.get("side")
        b = baselines.get(t) or {}
        px, ccy = spot_local(b)
        dv = (b.get("tape") or {}).get("median_turnover_usd_20d")
        cand = {"ticker": t, "submarket": b.get("submarket"), "company": b.get("company"),
                "panel_pct": pct, "n_members": row.get("n_members"),
                "side": None, "weight_raw": (round(pct - zero, 3) if isinstance(pct, (int, float)) else None),
                "spot_local": px, "currency": ccy, "turnover_usd": dv,
                "event_date": b.get("event_date"), "session": b.get("session"),
                "tv_symbol": b.get("tv_symbol"), "yahoo_symbol": b.get("yahoo_symbol")}

        def drop(why):
            rejected.append({**cand, "reason": why})

        if not isinstance(pct, (int, float)) or side not in (1, -1):
            drop("no panel_pct or side")
        elif sel.get("require_full_panel", True) and (not full or (row.get("n_members") or 0) < 4):
            drop("panel incomplete")
        elif pct <= zero:
            drop(f"panel_pct {pct:.1f} at or below the {zero:.0f} zero point")
        elif pct < floor:
            drop(f"panel_pct {pct:.1f} below the {floor:.0f} entry floor")
        elif (side > 0 and "long" not in sides) or (side < 0 and "short" not in sides):
            drop("side not allowed by execution_eu.selection.sides")
        elif b.get("submarket") not in allowed:
            drop(f"market {b.get('submarket')} not in execution_eu.selection.markets")
        elif b.get("event_occurred") is False:
            drop("event_occurred is false")
        elif not px:
            drop("no sealed spot")
        elif dv is None or dv < min_dv:
            drop(f"turnover {('$%.2fm' % (dv / 1e6)) if dv else 'unknown'} below the ${min_dv/1e6:.2f}m floor")
        else:
            cand["side"] = "BUY" if side > 0 else "SELL"
            taken.append(cand)
    taken.sort(key=lambda c: -c["panel_pct"])
    return taken, rejected


def fx_local_per_base(fx, base, local):
    """`fx` maps currency -> USD per unit (universe.json)."""
    if base == local:
        return 1.0
    if not fx or not fx.get(base) or not fx.get(local):
        return None
    return float(fx[base]) / float(fx[local])


def size(taken, equity_base, held_base, base_ccy, fx, ex):
    """Weights, caps and the hard limits, in the account's base currency. Pure."""
    from alpaca_trade import allocate
    sz, lim = ex["sizing"], ex["limits"]
    max_names = int(lim.get("max_names", 6))
    dropped = [{**c, "reason": f"outside max_names {max_names}"} for c in taken[max_names:]]
    taken = taken[:max_names]
    if not taken:
        return [], dropped, {}
    gross = equity_base * float(sz.get("gross_pct_of_equity", 100)) / 100.0
    gross = min(gross, float(lim.get("max_gross_base", 0) or 0)) - max(0.0, held_base)
    gross = max(0.0, gross)
    cap_name = min(equity_base * float(sz.get("max_name_pct_of_equity", 50)) / 100.0,
                   float(lim.get("max_name_base", 0) or 0))
    adv_pct = sz.get("max_pct_of_turnover")
    caps, usd_per_base = [], fx_local_per_base(fx, base_ccy, "USD")
    for c in taken:
        cap = cap_name
        if adv_pct and c.get("turnover_usd") and usd_per_base:
            cap = min(cap, c["turnover_usd"] * float(adv_pct) / 100.0 / usd_per_base)
        caps.append(cap)
    w = [max(0.0, c["weight_raw"]) for c in taken]
    alloc = allocate(gross, caps, w, True)
    min_pos = float(sz.get("min_position_base", 200))
    sized = []
    for c, target, cap in zip(taken, alloc, caps):
        rate = fx_local_per_base(fx, base_ccy, c["currency"])
        px = c.get("ref_price_local") or c["spot_local"]
        if not rate:
            dropped.append({**c, "reason": f"no FX rate {base_ccy}->{c['currency']}"})
            continue
        qty = int(math.floor(target * rate / px))
        notional_base = qty * px / rate
        row = {**c, "target_base": round(target, 2), "cap_base": round(cap, 2),
               "qty": qty, "price_local": round(px, 4),
               "price_source": c.get("ref_price_source") or "sealed baseline spot",
               "notional_base": round(notional_base, 2),
               "pct_of_equity": round(100 * notional_base / equity_base, 2) if equity_base else None}
        if qty < 1:
            dropped.append({**row, "reason": "sizes to less than one share"})
        elif notional_base < min_pos:
            dropped.append({**row, "reason": f"{notional_base:.0f} {base_ccy} below the {min_pos:.0f} minimum"})
        else:
            sized.append(row)
    meta = {"equity_base": round(equity_base, 2), "held_base": round(held_base, 2),
            "budget_base": round(gross, 2), "cap_name_base": round(cap_name, 2),
            "base_ccy": base_ccy}
    return sized, dropped, meta


def within_limits(sized, held_base, ex):
    """The last word before anything is sent. Returns (ok_rows, refused_rows)."""
    lim = ex["limits"]
    ok, refused, total = [], [], max(0.0, held_base)
    for r in sized:
        n = r["notional_base"]
        if n > float(lim.get("max_name_base", 0)) + 1e-6:
            refused.append({**r, "reason": "hard limit: max_name_base"})
        elif total + n > float(lim.get("max_gross_base", 0)) + 1e-6:
            refused.append({**r, "reason": "hard limit: max_gross_base"})
        elif len(ok) >= int(lim.get("max_names", 6)):
            refused.append({**r, "reason": "hard limit: max_names"})
        else:
            ok.append(r)
            total += n
    return ok, refused


# ------------------------------------------------------------------ the clock

def session_state(submarket, now=None, buffer_min=0):
    """'open' only if the exchange is trading now and closes more than buffer_min
    from now; otherwise a reason."""
    m = eu_market.MARKETS[submarket]
    tz = ZoneInfo(m["tz"])
    now = (now or datetime.now(timezone.utc)).astimezone(tz)
    if now.weekday() >= 5:
        return "weekend"
    if now.date().isoformat() in eu_market.exchange_holidays(submarket, now.year):
        return "exchange holiday"
    oh, om = map(int, OPEN_LOCAL.get(submarket, "09:00").split(":"))
    close = m["close_local"]
    half = eu_market.half_session(submarket, now.date())
    if half:
        close = re.match(r"(\d\d:\d\d)", half).group(1)
    ch, cm = map(int, close.split(":"))
    o = now.replace(hour=oh, minute=om, second=0, microsecond=0)
    c = now.replace(hour=ch, minute=cm, second=0, microsecond=0)
    if now < o:
        return f"not open until {OPEN_LOCAL.get(submarket, '09:00')} local"
    if now >= c - timedelta(minutes=buffer_min):
        return (f"past the {close} local close" if not buffer_min
                else f"within {buffer_min} min of the {close} local close, or past it")
    return "open"


# ------------------------------------------------------------------ guards

def guard(ex, submit):
    """Why nothing may be sent, or None."""
    if not submit:
        return "dry run (no --submit)"
    if not ex.get("enabled"):
        return "execution_eu.enabled is false"
    env_name = os.environ.get("IBKR_ENVIRONMENT")
    if env_name != ex["environment"]:
        return (f"IBKR_ENVIRONMENT is {env_name!r} but execution_eu.environment is "
                f"{ex['environment']!r}: both must say the same")
    if not os.environ.get("IBKR_ACCOUNT_ID"):
        return "IBKR_ACCOUNT_ID is not set"
    return None


def account_prefix_ok(acct, environment):
    return acct.startswith("DU") if environment == "paper" else (acct.startswith("U") and not acct.startswith("DU"))


def connect(ex):
    acct = os.environ.get("IBKR_ACCOUNT_ID") or ""
    if ex.get("auth") == "tws":
        from ibkr_tws import TwsApi
        t = ex.get("tws") or {}
        api = TwsApi(host=t.get("host"), port=(t.get("port") or {}).get(ex["environment"]) if isinstance(t.get("port"), dict) else t.get("port"),
                     client_id=t.get("client_id"), environment=ex["environment"], account=acct,
                     market_data_type=int(t.get("market_data_type", 3)), route=t.get("route", "SMART"))
    else:
        from ibkr_client import Ibkr
        api = Ibkr(mode=ex.get("auth", "oauth"), gateway_url=ex.get("gateway_url"))
    api.connect()
    seen = api.accounts()
    if acct not in seen:
        raise SystemExit(f"IBKR_ACCOUNT_ID {acct!r} is not among the accounts this login sees ({len(seen)} account(s))")
    if len(seen) > 1 and not ex.get("allow_multi_account_login", False):
        raise SystemExit(f"this login sees {len(seen)} accounts; the strategy must run on a login "
                         "that reaches only its own account (execution_eu.allow_multi_account_login)")
    if not account_prefix_ok(acct, ex["environment"]):
        raise SystemExit(f"account {acct} does not look like a {ex['environment']} account")
    return api, acct


def equity_of(api, acct):
    s = api.summary(acct)
    nl = s.get("netliquidation") or {}
    gp = s.get("grosspositionvalue") or {}
    return (float(nl.get("amount") or 0), nl.get("currency") or s.get("currency") or "EUR",
            abs(float(gp.get("amount") or 0)))


# ------------------------------------------------------------------ records

def orders_path(run):
    return Path(run) / "ibkr-orders.json"


def record(run, section, payload):
    p = orders_path(run)
    p.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"runs": []}
    state["runs"].append({"section": section, "at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                          **payload})
    p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cid(run, ticker, leg):
    day = Path(run).parent.name
    return f"{CLIENT_PREFIX}-{day}-{ticker}-{leg}-{int(time.time()) % 100000}"[:40]


# ------------------------------------------------------------------ contracts and prices

def symbol_candidates(b):
    t = (b.get("tv_symbol") or "").split(":")[-1] or b.get("ticker") or ""
    out = [t]
    for a, z in (("_", "."), ("_", " "), ("_", ""), ("-", "."), (".", " ")):
        v = t.replace(a, z)
        if v not in out:
            out.append(v)
    return out


def resolve_contract(api, b, ex):
    over = (ex.get("conid_overrides") or {}).get(b.get("ticker"))
    exchanges = (ex.get("exchanges") or {}).get(b["submarket"]) or DEFAULT_EXCHANGES[b["submarket"]]
    want_ccy = eu_market.MARKETS[b["submarket"]]["currency"]
    tried = []
    conids = [over] if over else []
    if not conids:
        for sym in symbol_candidates(b):
            for c in api.stock_contracts(sym):
                tried.append(f"{sym}@{c['exchange']}")
                if c["exchange"] in exchanges and c["conid"] not in conids:
                    conids.append(c["conid"])
            if conids:
                break
    for conid in conids:
        info = api.contract_info(conid)
        if info.get("currency") == want_ccy:
            return {"conid": int(conid), "symbol": info.get("symbol"), "exchange": info.get("exchange"),
                    "currency": info.get("currency"), "name": info.get("company_name")}
    raise LookupError(f"no {want_ccy} contract on {exchanges} (tried {', '.join(tried) or 'nothing'})")


def tick_increment(api, conid, is_buy, price=None):
    """The increment the exchange accepts at `price` (in the units the order is sent in).
    Over TWS that is the contract's market-rule band for that price, not the contract-wide
    minTick, which let a 101.376p MEGP limit through to an LSE refusal on 2026-11-13."""
    if hasattr(api, "min_tick"):
        try:
            return api.min_tick(conid, price)
        except TypeError:                       # an adapter without the price argument
            return api.min_tick(conid)
    try:
        r = api.get(f"/iserver/contract/{conid}/info-and-rules", {"isBuy": "true" if is_buy else "false"}) or {}
        inc = (r.get("rules") or {}).get("increment")
        return float(inc) if inc else None
    except Exception:
        return None


def round_to(px, inc, up):
    if not inc:
        inc = 10 ** (math.floor(math.log10(px)) - 3) if px > 0 else 0.01
    n = px / inc
    n = math.ceil(n - 1e-9) if up else math.floor(n + 1e-9)
    return round(n * inc, 6)


def yahoo_price(symbol):
    """Yahoo's latest regular-market price (about 15 minutes delayed), in the trading
    currency. Only a fallback for sizing when IBKR returns no quote (no market-data
    subscription); the limit is still collared around it."""
    import requests
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                         params={"range": "1d", "interval": "1m"},
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        meta = r.json()["chart"]["result"][0]["meta"]
        px = float(meta["regularMarketPrice"])
        return px / 100.0 if meta.get("currency") in ("GBp", "GBX") else px
    except Exception:
        return None


def live_price(api, conid, spot_local_px, ex, yahoo_symbol=None):
    """IBKR's price in the trading currency, with a pence check for London; Yahoo when
    IBKR has no quote."""
    q = api.snapshot([conid]).get(int(conid)) or {}
    bid, ask, last = q.get("bid"), q.get("ask"), q.get("last")
    px = (bid + ask) / 2 if bid and ask and ask >= bid else last
    src = "ibkr snapshot mid" if bid and ask else "ibkr last"
    if not px and yahoo_symbol:
        y = yahoo_price(yahoo_symbol)
        if y:
            gap = abs(y / spot_local_px - 1) * 100 if spot_local_px else 0
            if gap > float(ex["limits"].get("max_price_gap_pct", 20)):
                return None, 1.0, f"Yahoo price {y:.4f} is {gap:.0f}% from the sealed spot"
            # IBKR quotes London in pence or pounds; without a quote we cannot tell, so
            # take the unit from the contract's minimum tick later and assume pounds here.
            return y, 1.0, "yahoo (no IBKR quote)"
    if not px:
        return None, 1.0, "no IBKR quote"
    unit = 1.0
    if spot_local_px and 50 < px / spot_local_px < 200:       # IBKR quoting pence
        unit, px = 0.01, px / 100.0
    gap = abs(px / spot_local_px - 1) * 100 if spot_local_px else 0
    if gap > float(ex["limits"].get("max_price_gap_pct", 20)):
        return None, unit, f"IBKR price {px:.4f} is {gap:.0f}% from the sealed spot {spot_local_px:.4f}"
    return px, unit, src


# ------------------------------------------------------------------ orders

def build_order(acct, conid, side, qty, ref_px_local, unit, collar_pct, ex, inc, coid):
    """`inc` is the tick, or a callable taking the limit (in the units sent) and returning
    the tick that applies at that price, because exchanges' ladders are banded by price."""
    otype = ex["orders"].get("type", "limit")
    o = {"acctId": acct, "conid": int(conid), "side": side, "quantity": int(qty),
         "tif": "DAY", "cOID": coid}
    if otype == "market":
        o["orderType"] = "MKT"
    else:
        lim = ref_px_local * (1 + collar_pct / 100.0) if side == "BUY" else ref_px_local * (1 - collar_pct / 100.0)
        lim = lim / unit
        tick = inc(lim) if callable(inc) else inc
        o["orderType"] = "LMT"
        o["price"] = round_to(lim, tick, up=(side == "BUY"))
    return o


def coarse_increment(px):
    """A grid every European price ladder divides: 1% of the price's order of magnitude
    (101p -> 1p, 25.0 -> 0.1). The retry after a tick refusal goes out on it."""
    return 10 ** (math.floor(math.log10(px)) - 2) if px and px > 0 else 0.01


def is_tick_refusal(err):
    m = str(err)
    return "minimum price variation" in m or "Error 110" in m


def place_order(api, acct, order):
    """Place, and if the exchange refuses the limit's tick, re-round it outward (down for a
    sell, up for a buy) onto `coarse_increment` and send it ONCE more. Returns the broker's
    result plus `retried_tick` with the first price when the retry was needed."""
    try:
        return api.place(acct, order)
    except Exception as e:
        if order.get("orderType") != "LMT" or not is_tick_refusal(e):
            raise
        first = order["price"]
        order["price"] = round_to(first, coarse_increment(first), up=(order["side"] == "BUY"))
        if order["price"] == first:
            raise
        order["cOID"] = (order.get("cOID", "") + "-t")[:40]
        res = api.place(acct, order)
        return {**res, "retried_tick": {"first_price": first, "error": str(e)}}


def wait_fills(api, order_ids, seconds):
    deadline = time.time() + seconds
    state = {}
    while True:
        for o in api.live_orders():
            oid = str(o.get("orderId"))
            if oid in order_ids:
                state[oid] = {"status": o.get("status"), "filled": o.get("filledQuantity"),
                              "remaining": o.get("remainingQuantity"), "avg_price": o.get("avgPrice"),
                              "ticker": o.get("ticker")}
        done = [s for s in state.values() if s["status"] in ("Filled", "Cancelled", "Inactive")]
        if len(done) == len(order_ids) or time.time() > deadline:
            return state
        time.sleep(5)


# ------------------------------------------------------------------ commands

def cmd_mode(a, ex):
    print(json.dumps({k: ex.get(k) for k in ("enabled", "environment", "auth", "selection", "sizing", "limits", "orders")},
                     indent=2))
    print(f"IBKR_ENVIRONMENT={os.environ.get('IBKR_ENVIRONMENT')!r}  "
          f"IBKR_ACCOUNT_ID={'set' if os.environ.get('IBKR_ACCOUNT_ID') else 'missing'}  "
          + ("broker=IB Gateway on the executor's server (execution_eu.auth tws); "
             "the cloud Routine only hands the book over (step 6b handoff)" if ex.get("auth") == "tws" else
             f"credentials={'present' if os.environ.get('IBKR_OAUTH_CONSUMER_KEY') or os.environ.get('IBKR_GATEWAY_URL') else 'missing'}"))
    why = guard(ex, True)
    print("ready to submit" if not why else f"would refuse: {why}")
    return 0 if not why else 1


def cmd_check(a, ex):
    api, acct = connect(ex)
    eq, ccy, gross = equity_of(api, acct)
    print(f"connected ({ex.get('auth')}), account {acct} ({ex['environment']}), "
          f"net liquidation {eq:,.2f} {ccy}, gross positions {gross:,.2f} {ccy}")
    for p in api.positions(acct):
        print(f"  holding {p.get('contractDesc') or p.get('ticker')}: {p.get('position')} "
              f"@ {p.get('mktPrice')} {p.get('currency')}")
    for o in api.live_orders():
        print(f"  order {o.get('orderId')} {o.get('ticker')} {o.get('side')} {o.get('status')}")
    return 0


def cmd_contracts(a, ex):
    panel, baselines, _ = load_run(a.run)
    api, _acct = connect(ex)
    for t, b in baselines.items():
        try:
            c = resolve_contract(api, b, ex)
            print(f"  {t:10s} {b['submarket']} -> conid {c['conid']} {c['symbol']} {c['exchange']} {c['currency']} {c['name']}")
        except LookupError as e:
            print(f"  {t:10s} {b['submarket']} -> NOT FOUND: {e}")
    return 0


def plan(a, ex, api=None, acct=None):
    panel, baselines, uni = load_run(a.run)
    taken, rejected = select(panel, baselines, ex)
    if api is None:
        equity, base, held = float(a.equity), a.base, 0.0
    else:
        equity, base, held = equity_of(api, acct)
    sized, dropped, meta = size(taken, equity, held, base, uni.get("fx") or {}, ex)
    return {"taken": taken, "rejected": rejected, "sized": sized, "dropped": dropped, "meta": meta,
            "panel_rule": f"panel_pct >= {ex['selection'].get('min_panel_pct')} with all four judges"}


def print_plan(p):
    m = p["meta"]
    if m:
        print(f"equity {m['equity_base']:,.2f} {m['base_ccy']}, held {m['held_base']:,.2f}, "
              f"budget {m['budget_base']:,.2f}, cap a name {m['cap_name_base']:,.2f}")
    print(f"rule: {p['panel_rule']}")
    for r in p["sized"]:
        print(f"  {r['side']:4s} {r['ticker']:10s} {r['submarket']} pct {r['panel_pct']:5.1f} "
              f"qty {r['qty']:>7d} @ {r['price_local']} {r['currency']} = {r['notional_base']:,.2f} "
              f"({r['pct_of_equity']}%) [{r['price_source']}]")
    for r in p["dropped"]:
        print(f"  --   {r['ticker']:10s} dropped: {r['reason']}")
    near = [r for r in p["rejected"] if isinstance(r.get("panel_pct"), (int, float)) and r["panel_pct"] >= 60]
    for r in near:
        print(f"  --   {r['ticker']:10s} not taken: {r['reason']}")
    if not p["sized"]:
        print("  no name to trade")


def cmd_plan(a, ex):
    if a.offline:
        p = plan(a, ex)
    else:
        api, acct = connect(ex)
        p = plan(a, ex, api, acct)
    print_plan(p)
    return 0


def cmd_flatten(a, ex):
    blocked = guard(ex, a.submit)
    if blocked and a.submit:
        print(f"REFUSED: {blocked}")
        record(a.run, "flatten", {"refused": blocked})
        return 2
    api, acct = connect(ex)
    eq, ccy, gross = equity_of(api, acct)
    working = [o for o in api.live_orders()
               if o.get("status") not in ("Filled", "Cancelled", "Inactive")]
    positions = [p for p in api.positions(acct) if (p.get("assetClass") or "STK") == "STK"]
    print(f"account {acct}: {len(positions)} position(s), {len(working)} working order(s), "
          f"gross {gross:,.2f} {ccy}")
    sent, skipped = [], []
    if not a.submit:
        for p in positions:
            print(f"  would sell {p.get('contractDesc')} {p.get('position')}")
        return 0
    if working and hasattr(api, "cancel_all"):
        api.cancel_all()
        working = []
    for o in working:
        try:
            api.cancel(acct, o.get("orderId"))
        except Exception as e:
            skipped.append({"order": o.get("orderId"), "reason": f"cancel failed: {e}"})
    time.sleep(3)
    collar = float(ex["orders"].get("exit_collar_pct", 2.0))
    for p in positions:
        qty = float(p.get("position"))
        side = "SELL" if qty > 0 else "BUY"
        conid = int(p["conid"])
        name = p.get("contractDesc") or p.get("ticker") or str(conid)
        px = None
        q = api.snapshot([conid]).get(conid) or {}
        px = q.get("bid") if side == "SELL" else q.get("ask")
        px = px or q.get("last") or p.get("mktPrice")
        if not px and ex["orders"].get("type", "limit") != "market":
            skipped.append({"ticker": name, "reason": "no price for a limit exit"})
            continue
        inc = (lambda lim, _c=conid, _b=(side == "BUY"): tick_increment(api, _c, _b, lim))
        order = build_order(acct, conid, side, abs(qty), float(px or 0), 1.0, collar, ex, inc,
                            cid(a.run, name.split()[0], "exit"))
        try:
            res = place_order(api, acct, order)
            sent.append({"ticker": name, "conid": conid, "side": side, "qty": abs(qty),
                         "limit": order.get("price"), **{k: res[k] for k in ("order_id", "status", "prompts")},
                         **({"retried_tick": res["retried_tick"]} if res.get("retried_tick") else {})})
            print(f"  sent {side} {abs(qty)} {name} @ {order.get('price', 'MKT')} -> {res['order_id']}")
        except Exception as e:
            skipped.append({"ticker": name, "reason": str(e)})
            print(f"  FAILED {name}: {e}")
    fills = wait_fills(api, {s["order_id"] for s in sent}, int(ex["orders"].get("fill_wait_seconds", 120))) if sent else {}
    left = [p for p in api.positions(acct)]
    for s in sent:
        s["fill"] = fills.get(s["order_id"])
    record(a.run, "flatten", {"account": acct, "equity": eq, "base": ccy, "sent": sent,
                              "skipped": skipped, "still_held": [p.get("contractDesc") for p in left]})
    print(f"flatten: {len(sent)} sent, {len(skipped)} skipped, {len(left)} position(s) still held")
    return 0 if not left else 3


def cmd_open(a, ex):
    blocked = guard(ex, a.submit)
    if blocked and a.submit:
        print(f"REFUSED: {blocked}")
        record(a.run, "open", {"refused": blocked})
        return 2
    panel, baselines, _ = load_run(a.run)
    today = datetime.now(timezone.utc).date().isoformat()
    sealed = {str(b.get("sealed_utc", ""))[:10] for b in baselines.values()}
    if a.submit and today not in sealed:
        msg = f"the run was sealed on {sorted(sealed)}, not today ({today}): refusing a stale book"
        print(f"REFUSED: {msg}")
        record(a.run, "open", {"refused": msg})
        return 2
    api, acct = connect(ex)
    p = plan(a, ex, api, acct)
    buffer_min = int(ex["orders"].get("close_buffer_min", 0))
    collar = float(ex["orders"].get("entry_collar_pct", 1.0))
    priced, skipped = [], []
    for r in p["taken"][: int(ex["limits"].get("max_names", 6))]:
        b = baselines[r["ticker"]]
        st = session_state(r["submarket"], buffer_min=buffer_min)
        if st != "open":
            skipped.append({**r, "reason": f"market {r['submarket']}: {st}"})
            continue
        try:
            c = resolve_contract(api, b, ex)
        except LookupError as e:
            skipped.append({**r, "reason": str(e)})
            continue
        px, unit, src = live_price(api, c["conid"], r["spot_local"], ex, b.get("yahoo_symbol"))
        if src.startswith("yahoo") and r["submarket"] == "uk":
            skipped.append({**r, "reason": "London name with no IBKR quote: pence or pounds unknown"})
            continue
        if not px:
            skipped.append({**r, "reason": src})
            continue
        priced.append({**r, "conid": c["conid"], "ib_symbol": c["symbol"], "unit": unit,
                       "ref_price_local": px, "ref_price_source": src})
    _, _, uni = load_run(a.run)
    sized, dropped, meta = size(priced, p["meta"]["equity_base"], p["meta"]["held_base"],
                                p["meta"]["base_ccy"], uni.get("fx") or {}, ex)
    ok, refused = within_limits(sized, meta.get("held_base", 0.0), ex)
    p.update({"sized": ok, "dropped": dropped + refused + skipped, "meta": meta})
    print_plan(p)
    if not a.submit:
        return 0
    sent, failed = [], []
    max_orders = int(ex["limits"].get("max_orders_per_run", 20))
    total = meta.get("held_base", 0.0)
    for r in ok:
        if len(sent) >= max_orders:
            failed.append({**r, "reason": "hard limit: max_orders_per_run"})
            continue
        if total + r["notional_base"] > float(ex["limits"]["max_gross_base"]) + 1e-6:
            failed.append({**r, "reason": "hard limit: max_gross_base (final check)"})
            continue
        inc = (lambda lim, _c=r["conid"], _b=(r["side"] == "BUY"): tick_increment(api, _c, _b, lim))
        order = build_order(acct, r["conid"], r["side"], r["qty"], r["ref_price_local"], r["unit"],
                            collar, ex, inc, cid(a.run, r["ticker"], "entry"))
        try:
            res = place_order(api, acct, order)
            total += r["notional_base"]
            sent.append({"ticker": r["ticker"], "conid": r["conid"], "side": r["side"], "qty": r["qty"],
                         "limit": order.get("price"), "notional_base": r["notional_base"],
                         "panel_pct": r["panel_pct"], **{k: res[k] for k in ("order_id", "status", "prompts")},
                         **({"retried_tick": res["retried_tick"]} if res.get("retried_tick") else {})})
            print(f"  sent {r['side']} {r['qty']} {r['ticker']} @ {order.get('price', 'MKT')} -> {res['order_id']}")
        except Exception as e:
            failed.append({**r, "reason": str(e)})
            print(f"  FAILED {r['ticker']}: {e}")
    fills = wait_fills(api, {s["order_id"] for s in sent}, int(ex["orders"].get("fill_wait_seconds", 120))) if sent else {}
    for s in sent:
        s["fill"] = fills.get(s["order_id"])
    record(a.run, "open", {"account": acct, "meta": meta, "rule": p["panel_rule"], "sent": sent,
                           "failed": failed, "not_taken": [{"ticker": d["ticker"], "reason": d["reason"]} for d in p["dropped"]]})
    print(f"open: {len(sent)} sent, {len(failed)} failed")
    return 0


def handoff_path(run):
    return Path(run) / "ibkr-handoff.json"


def cmd_handoff(a, ex):
    """Cloud side of the executor route (execution_eu.auth tws): write the day's book
    request for the server, which waits for this file before it runs `open`. Offline:
    no broker call. The server prices and sizes it against the real account itself."""
    panel, baselines, _ = load_run(a.run)
    p = plan(argparse.Namespace(run=a.run, equity=a.equity, base=a.base), ex)
    now = datetime.now(timezone.utc)
    doc = {"run": str(Path(a.run)), "written_utc": now.isoformat(timespec="seconds"),
           "date_utc": now.date().isoformat(),
           "sealed_utc": sorted({str(b.get("sealed_utc", ""))[:10] for b in baselines.values()}),
           "rule": p["panel_rule"],
           "names": [{"ticker": r["ticker"], "submarket": r["submarket"], "side": r["side"],
                      "panel_pct": r["panel_pct"]} for r in p["taken"]],
           "note": "the executor's server runs `ibkr_trade.py open --run <run> --submit` on this; "
                   "the sizes it sends depend on the account, not on this file"}
    handoff_path(a.run).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"handoff written: {len(doc['names'])} name(s) at or above the rule -> {handoff_path(a.run)}")
    print_plan(p)
    return 0


def cmd_status(a, ex):
    p = orders_path(a.run)
    if p.exists():
        for r in json.loads(p.read_text(encoding="utf-8"))["runs"]:
            print(f"{r['at_utc']} {r['section']}: " + (r.get("refused") or
                  f"{len(r.get('sent', []))} sent, fills {[(s['ticker'], (s.get('fill') or {}).get('status')) for s in r.get('sent', [])]}"))
    else:
        print(f"no {p}")
    if not a.offline:
        api, acct = connect(ex)
        eq, ccy, gross = equity_of(api, acct)
        print(f"account {acct}: net liquidation {eq:,.2f} {ccy}, gross {gross:,.2f}")
        for pos in api.positions(acct):
            print(f"  holding {pos.get('contractDesc')}: {pos.get('position')} @ {pos.get('mktPrice')} {pos.get('currency')}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("mode")
    sub.add_parser("check")
    for name in ("contracts", "plan", "flatten", "open", "status", "handoff"):
        s = sub.add_parser(name)
        s.add_argument("--run", required=True)
        if name in ("flatten", "open"):
            s.add_argument("--submit", action="store_true")
        if name in ("plan", "status"):
            s.add_argument("--offline", action="store_true")
        if name in ("plan", "handoff"):
            s.add_argument("--equity", type=float, default=10000.0)
            s.add_argument("--base", default="EUR")
    a = ap.parse_args(argv)
    ex = eu_config()
    from ibkr_client import IbkrError
    try:
        return {"mode": cmd_mode, "check": cmd_check, "contracts": cmd_contracts, "plan": cmd_plan,
            "flatten": cmd_flatten, "open": cmd_open, "status": cmd_status,
            "handoff": cmd_handoff}[a.cmd](a, ex)
    except IbkrError as e:
        print(f"IBKR error: {e}")
        if getattr(a, "run", None) and a.cmd in ("flatten", "open"):
            record(a.run, a.cmd, {"error": str(e)})
        return 4


if __name__ == "__main__":
    sys.exit(main())
