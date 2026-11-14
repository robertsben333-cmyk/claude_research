#!/usr/bin/env python3
"""Stage EU's IBKR client over the TWS API: IB Gateway, kept logged in by IBC, on a
machine the operator controls.

Why this exists (2026-11-08): IBKR's OAuth is for institutional clients only ("OAuth1.0a
is only available to institutional clients"; OAuth 2.0 "is not available to Individual
account structures"). An individual account reaches the API only through a logged-in
gateway. The cloud Routine cannot hold one, so a small always-on server runs IB Gateway
with IBC (it restarts nightly without a second factor; the operator confirms a login on
the phone about once a week) and `eu_executor.py` on that server trades the book the
Routine publishes. Nothing connects in to that server.

`TwsApi` has the same methods, returning the same shapes, as `ibkr_client.Ibkr`, so
`ibkr_trade.py` runs unchanged on either. It needs `ib_async` (the maintained fork of
ib_insync), which the server's install script puts in its virtualenv. The cloud never
imports this file.

Settings: `execution_eu.tws` in config/pipeline.yaml, overridden by IBKR_TWS_HOST,
IBKR_TWS_PORT and IBKR_TWS_CLIENT_ID. IB Gateway listens on 4001 for live and 4002 for
paper by default.
"""
from __future__ import annotations

import math
import os

from ibkr_client import IbkrError

DEFAULT_PORT = {"live": 4001, "paper": 4002}


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or f <= 0:
        return None
    return f


def _band_increment(bands, price):
    """The increment of the highest band whose lowEdge is at or below `price`."""
    best = None
    for b in bands or []:
        try:
            lo, inc = float(getattr(b, "lowEdge")), float(getattr(b, "increment"))
        except (TypeError, ValueError, AttributeError):
            continue
        if math.isnan(lo) or math.isnan(inc) or inc <= 0 or lo > price + 1e-12:
            continue
        if best is None or lo >= best[0]:
            best = (lo, inc)
    return best[1] if best else None


class TwsApi:
    """The `Ibkr` interface over ib_async. `ib` may be injected (the smoke test does)."""

    def __init__(self, host=None, port=None, client_id=None, environment="paper", account=None, ib=None,
                 market_data_type=3, route="SMART"):
        self.host = os.environ.get("IBKR_TWS_HOST") or host or "127.0.0.1"
        self.port = int(os.environ.get("IBKR_TWS_PORT") or port or DEFAULT_PORT.get(environment, 4002))
        self.client_id = int(os.environ.get("IBKR_TWS_CLIENT_ID") or client_id or 17)
        self.account = account
        self.market_data_type = market_data_type     # 3 = delayed when not subscribed
        self.route = route
        self.ib = ib
        self._details = {}
        self._rules = {}

    # -------------------------------------------------------------- session

    def connect(self):
        if self.ib is None:
            try:
                from ib_async import IB
            except ImportError as e:  # pragma: no cover - server only
                raise IbkrError("ib_async is not installed (run the executor's install script)") from e
            self.ib = IB()
        if self.ib.isConnected():
            return self
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id, timeout=20,
                            account=self.account or "")
        except Exception as e:
            raise IbkrError(f"cannot reach IB Gateway at {self.host}:{self.port}: {e}. "
                            "Is the gateway running and logged in?") from e
        self.ib.reqMarketDataType(self.market_data_type)
        return self

    def pump(self, seconds=0.5):
        self.ib.sleep(seconds)

    # -------------------------------------------------------------- account

    def accounts(self):
        return [a for a in (self.ib.managedAccounts() or []) if a]

    def summary(self, acct):
        out = {}
        for v in self.ib.accountSummary(acct):
            tag = {"NetLiquidation": "netliquidation", "GrossPositionValue": "grosspositionvalue"}.get(v.tag)
            if tag and v.currency and v.currency != "BASE":
                out[tag] = {"amount": float(v.value), "currency": v.currency}
        if "netliquidation" in out:
            out["currency"] = out["netliquidation"]["currency"]
        return out

    def positions(self, acct):
        prices = {p.contract.conId: p.marketPrice for p in self.ib.portfolio(acct)} if hasattr(self.ib, "portfolio") else {}
        rows = []
        for p in self.ib.positions(acct):
            if not p.position:
                continue
            c = p.contract
            rows.append({"conid": c.conId, "position": float(p.position), "ticker": c.symbol,
                         "contractDesc": f"{c.symbol} {c.primaryExchange or c.exchange or ''}".strip(),
                         "mktPrice": _num(prices.get(c.conId)), "currency": c.currency,
                         "assetClass": c.secType or "STK"})
        return rows

    # -------------------------------------------------------------- orders

    def _trades(self):
        try:
            self.ib.reqAllOpenOrders()
        except Exception:
            pass
        self.pump()
        seen, out = set(), []
        for t in list(self.ib.trades()):
            oid = t.order.orderId or t.order.permId
            if oid in seen:
                continue
            seen.add(oid)
            out.append(t)
        return out

    def live_orders(self):
        rows = []
        for t in self._trades():
            s = t.orderStatus
            rows.append({"orderId": str(t.order.orderId or t.order.permId), "status": s.status,
                         "filledQuantity": s.filled, "remainingQuantity": s.remaining,
                         "avgPrice": _num(s.avgFillPrice), "ticker": t.contract.symbol,
                         "side": t.order.action, "account": t.order.account, "orderRef": t.order.orderRef})
        return rows

    def cancel(self, acct, order_id):
        for t in self._trades():
            if str(t.order.orderId or t.order.permId) == str(order_id):
                self.ib.cancelOrder(t.order)
                return True
        return False

    def cancel_all(self):
        """Every working order on the account, whichever client sent it."""
        self.ib.reqGlobalCancel()
        self.pump(2)

    # -------------------------------------------------------------- contracts

    def stock_contracts(self, symbol):
        from ib_async import Contract
        out, seen = [], set()
        for cd in self.ib.reqContractDetails(Contract(secType="STK", symbol=symbol)) or []:
            c = cd.contract
            self._details[c.conId] = cd
            key = (c.conId, c.primaryExchange or c.exchange)
            if key in seen:
                continue
            seen.add(key)
            out.append({"conid": c.conId, "exchange": c.primaryExchange or c.exchange, "currency": c.currency})
        return out

    def _detail(self, conid):
        conid = int(conid)
        if conid not in self._details:
            from ib_async import Contract
            got = self.ib.reqContractDetails(Contract(conId=conid)) or []
            if not got:
                raise IbkrError(f"no contract details for conid {conid}")
            self._details[conid] = got[0]
        return self._details[conid]

    def contract_info(self, conid):
        cd = self._detail(conid)
        c = cd.contract
        return {"conid": c.conId, "symbol": c.symbol, "exchange": c.primaryExchange or c.exchange,
                "currency": c.currency, "company_name": cd.longName}

    def min_tick(self, conid, price=None):
        """The price increment the exchange accepts AT `price`.

        `contractDetails.minTick` is one contract-wide number and is finer than most
        exchanges' price ladders: on 2026-11-13 the LSE refused a MEGP sell at 101.376p
        (Error 110, "does not conform to the minimum price variation") because minTick
        let three decimals through. The real ladder is the contract's market rule
        (`marketRuleIds`, one per valid exchange, read with `reqMarketRule`): a list of
        (lowEdge, increment) bands. With a price, use the band it falls in on the rule of
        the primary listing; if the primary's rule cannot be picked out, the coarsest
        increment any listed venue imposes (valid on all of them). Without a price, or if
        no rule can be read, fall back to minTick."""
        try:
            cd = self._detail(conid)
        except Exception:
            return None
        if price is not None and price > 0:
            inc = self._rule_increment(cd, float(price))
            if inc:
                return inc
        return _num(getattr(cd, "minTick", None))

    def _rule_increment(self, cd, price):
        ids = [x.strip() for x in str(getattr(cd, "marketRuleIds", "") or "").split(",")]
        exs = [x.strip() for x in str(getattr(cd, "validExchanges", "") or "").split(",")]
        if not any(ids):
            return None
        prim = getattr(cd.contract, "primaryExchange", "") or ""
        pick = ids[exs.index(prim)] if prim and len(ids) == len(exs) and prim in exs else None
        if pick:
            inc = _band_increment(self._market_rule(pick), price)
            if inc:
                return inc
        incs = [_band_increment(self._market_rule(r), price) for r in dict.fromkeys(i for i in ids if i)]
        incs = [i for i in incs if i]
        return max(incs) if incs else None

    def _market_rule(self, rid):
        if rid not in self._rules:
            try:
                self._rules[rid] = list(self.ib.reqMarketRule(int(rid)) or [])
            except Exception:
                self._rules[rid] = []
        return self._rules[rid]

    def _contract(self, conid):
        from ib_async import Contract
        c = self._detail(conid).contract
        return Contract(conId=c.conId, exchange=self.route or c.primaryExchange,
                        primaryExchange=c.primaryExchange, currency=c.currency, symbol=c.symbol, secType="STK")

    # -------------------------------------------------------------- prices

    def snapshot(self, conids, wait=4.0):
        """Bid, ask, last per conid, delayed when the account has no market-data
        subscription (reqMarketDataType 3)."""
        tickers = {}
        for conid in conids:
            try:
                tickers[int(conid)] = self.ib.reqMktData(self._contract(conid), "", True, False)
            except Exception:
                continue
        self.pump(wait)
        out = {}
        for conid, t in tickers.items():
            last = _num(getattr(t, "last", None)) or _num(getattr(t, "close", None))
            out[conid] = {"bid": _num(getattr(t, "bid", None)), "ask": _num(getattr(t, "ask", None)), "last": last}
        return out

    # -------------------------------------------------------------- placing

    def place(self, acct, order: dict):
        from ib_async import LimitOrder, MarketOrder
        kw = {"account": acct, "tif": order.get("tif", "DAY"), "orderRef": order.get("cOID", "")}
        if order.get("orderType") == "MKT":
            o = MarketOrder(order["side"], order["quantity"], **kw)
        else:
            o = LimitOrder(order["side"], order["quantity"], float(order["price"]), **kw)
        trade = self.ib.placeOrder(self._contract(order["conid"]), o)
        self.pump(2)
        errors = [e.message for e in trade.log if getattr(e, "errorCode", 0) and e.errorCode not in (399, 2104, 2106, 2158)]
        if trade.orderStatus.status in ("Cancelled", "Inactive", "ApiCancelled") and errors:
            raise IbkrError("; ".join(errors))
        return {"order_id": str(trade.order.orderId), "status": trade.orderStatus.status,
                "prompts": errors, "raw": None}

    def get(self, path, params=None):  # the REST client's escape hatch; not available here
        raise IbkrError(f"not available over the TWS API: {path}")
