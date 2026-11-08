#!/usr/bin/env python3
"""A small client for the Interactive Brokers Web API (Client Portal API v1), built for
a cloud Routine that has no desktop, no browser and no always-on gateway.

Two ways in, one set of endpoints:

  oauth    First-party OAuth 1.0a against https://api.ibkr.com/v1/api. The account
           holder registers a consumer key and two RSA key pairs once in IBKR's OAuth
           self-service portal and receives an access token and an (encrypted) access
           token secret. With those, every session mints its own live session token
           (about 24 hours) by a Diffie-Hellman exchange, then opens a brokerage
           session with /iserver/auth/ssodh/init. No gateway, no daily browser login.
  gateway  A Client Portal Gateway (or IBeam) the operator runs and keeps logged in
           somewhere this session can reach. The gateway holds the login, so requests
           go out unsigned.

Written against the standard library plus `requests` and `cryptography`, both already
in the Routine environment, because installing a third-party IBKR package from inside
an auto-mode session is refused and a package that handles a live trading login is a
supply-chain risk this repo does not need.

THE OAUTH SIGNING HAS BEEN TESTED AGAINST A SIMULATED SERVER ONLY (smoke_test.py runs
the whole Diffie-Hellman exchange both ways). It follows IBKR's published first-party
OAuth 1.0a workflow, but the first real proof is `ibkr_trade.py check` against the paper
account. Nothing in this file places an order on its own; ibkr_trade.py does, behind
its guards.

Credentials are read from the environment and never written anywhere:

  IBKR_OAUTH_CONSUMER_KEY         nine characters, chosen in the portal
  IBKR_OAUTH_ACCESS_TOKEN         from the portal
  IBKR_OAUTH_ACCESS_TOKEN_SECRET  from the portal (base64, encrypted to your key)
  IBKR_OAUTH_ENCRYPTION_KEY       private_encryption.pem   (PEM, or base64 of the PEM)
  IBKR_OAUTH_SIGNATURE_KEY        private_signature.pem    (PEM, or base64 of the PEM)
  IBKR_OAUTH_DH_PARAM             dhparam.pem              (PEM, or base64 of the PEM)
  IBKR_OAUTH_REALM                optional, default "limited_poa"
  IBKR_GATEWAY_URL                gateway mode only, e.g. https://host:5000
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import string
import time
from urllib.parse import quote, quote_plus

OAUTH_BASE = "https://api.ibkr.com/v1/api"
USER_AGENT = "claude-research-eu/1.0"
OAUTH_ENV = ("IBKR_OAUTH_CONSUMER_KEY", "IBKR_OAUTH_ACCESS_TOKEN",
             "IBKR_OAUTH_ACCESS_TOKEN_SECRET", "IBKR_OAUTH_ENCRYPTION_KEY",
             "IBKR_OAUTH_SIGNATURE_KEY", "IBKR_OAUTH_DH_PARAM")


class IbkrError(RuntimeError):
    pass


# ------------------------------------------------------------------ helpers

def _pem(value: str) -> bytes:
    """A PEM pasted into an environment variable arrives in one of three shapes: real
    newlines, literal backslash-n, or base64 of the whole file. Accept all three."""
    v = (value or "").strip()
    if not v:
        raise IbkrError("empty PEM")
    if "-----BEGIN" not in v:
        try:
            v = base64.b64decode(v).decode("ascii")
        except Exception as e:
            raise IbkrError(f"value is neither a PEM nor base64 of one: {e}")
    return v.replace("\\n", "\n").encode("ascii")


def to_byte_array(x: int) -> bytes:
    """Big-endian bytes of a positive integer with a leading zero byte when the top bit
    is set: the two's-complement form IBKR's (Java) side uses for the DH secret K."""
    h = format(x, "x")
    if len(h) % 2:
        h = "0" + h
    out = bytes.fromhex(h)
    if x.bit_length() % 8 == 0:
        out = b"\x00" + out
    return out


def nonce(n: int = 16) -> str:
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(n))


def base_string(method: str, url: str, params: dict, prepend: str = "") -> str:
    pairs = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    return f"{prepend}{method.upper()}&{quote_plus(url)}&{quote(pairs)}"


def auth_header(params: dict, realm: str) -> str:
    p = dict(params)
    p["realm"] = realm
    return "OAuth " + ", ".join(f'{k}="{v}"' for k, v in sorted(p.items()))


def live_session_token(dh_secret_K: int, prepend_hex: str) -> str:
    """LST = base64(HMAC-SHA1(key=K as bytes, msg=decrypted access-token secret))."""
    mac = hmac.new(to_byte_array(dh_secret_K), bytes.fromhex(prepend_hex), hashlib.sha1)
    return base64.b64encode(mac.digest()).decode()


def lst_signature(lst: str, consumer_key: str) -> str:
    return hmac.new(base64.b64decode(lst), consumer_key.encode(), hashlib.sha1).hexdigest()


# ------------------------------------------------------------------ OAuth 1.0a

class OAuth1a:
    """The cryptography of IBKR's first-party OAuth, with no network in it, so the
    smoke test can drive it against a simulated server."""

    def __init__(self, consumer_key, access_token, access_token_secret,
                 encryption_pem: bytes, signature_pem: bytes, dh_pem: bytes,
                 realm="limited_poa"):
        from cryptography.hazmat.primitives import serialization
        self.consumer_key = consumer_key
        self.access_token = access_token
        self.realm = realm
        self.enc_key = serialization.load_pem_private_key(encryption_pem, password=None)
        self.sig_key = serialization.load_pem_private_key(signature_pem, password=None)
        import warnings
        with warnings.catch_warnings():     # IBKR's protocol is finite-field DH; not our choice
            warnings.simplefilter("ignore")
            params = serialization.load_pem_parameters(dh_pem)
        nums = params.parameter_numbers()
        self.dh_p, self.dh_g = nums.p, nums.g or 2
        from cryptography.hazmat.primitives.asymmetric import padding
        secret = self.enc_key.decrypt(base64.b64decode(access_token_secret),
                                      padding.PKCS1v15())
        self.prepend = secret.hex()
        self.lst = None
        self.lst_expires_ms = None

    @classmethod
    def from_env(cls, env=os.environ):
        missing = [k for k in OAUTH_ENV if not env.get(k)]
        if missing:
            raise IbkrError("missing environment variables: " + ", ".join(missing))
        return cls(env["IBKR_OAUTH_CONSUMER_KEY"], env["IBKR_OAUTH_ACCESS_TOKEN"],
                   env["IBKR_OAUTH_ACCESS_TOKEN_SECRET"],
                   _pem(env["IBKR_OAUTH_ENCRYPTION_KEY"]),
                   _pem(env["IBKR_OAUTH_SIGNATURE_KEY"]),
                   _pem(env["IBKR_OAUTH_DH_PARAM"]),
                   env.get("IBKR_OAUTH_REALM") or "limited_poa")

    # -- step 1: the live-session-token request, signed RSA-SHA256
    def lst_request(self, url):
        """Returns (headers, dh_random). The caller POSTs to `url` with these headers."""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        a = secrets.randbits(256)
        challenge = format(pow(self.dh_g, a, self.dh_p), "x")
        params = {"oauth_consumer_key": self.consumer_key, "oauth_nonce": nonce(),
                  "oauth_signature_method": "RSA-SHA256",
                  "oauth_timestamp": str(int(time.time())),
                  "oauth_token": self.access_token,
                  "diffie_hellman_challenge": challenge}
        bs = base_string("POST", url, params, prepend=self.prepend)
        sig = self.sig_key.sign(bs.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
        params["oauth_signature"] = quote_plus(base64.b64encode(sig).decode())
        return {"Authorization": auth_header(params, self.realm),
                "User-Agent": USER_AGENT, "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate", "Connection": "keep-alive",
                "Content-Length": "0"}, a

    # -- step 2: turn the server's DH response into the token, and check it
    def accept_lst(self, response: dict, a: int):
        B = int(response["diffie_hellman_response"], 16)
        K = pow(B, a, self.dh_p)
        lst = live_session_token(K, self.prepend)
        if lst_signature(lst, self.consumer_key) != response.get("live_session_token_signature"):
            raise IbkrError("live session token did not validate: the access token "
                            "secret, the encryption key or the DH parameters do not "
                            "belong together")
        self.lst = lst
        self.lst_expires_ms = response.get("live_session_token_expiration")
        return lst

    # -- step 3: every later request, signed HMAC-SHA256 with the token
    def sign(self, method, url, query=None):
        if not self.lst:
            raise IbkrError("no live session token yet")
        params = {"oauth_consumer_key": self.consumer_key, "oauth_nonce": nonce(),
                  "oauth_signature_method": "HMAC-SHA256",
                  "oauth_timestamp": str(int(time.time())),
                  "oauth_token": self.access_token}
        signed = dict(params)
        for k, v in (query or {}).items():
            signed[k] = v
        bs = base_string(method, url, signed)
        mac = hmac.new(base64.b64decode(self.lst), bs.encode("utf-8"), hashlib.sha256)
        params["oauth_signature"] = quote_plus(base64.b64encode(mac.digest()).decode())
        return {"Authorization": auth_header(params, self.realm),
                "User-Agent": USER_AGENT, "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate", "Connection": "keep-alive"}


# ------------------------------------------------------------------ the client

class Ibkr:
    """The Client Portal API v1 endpoints this repo needs, nothing more."""

    def __init__(self, mode="oauth", gateway_url=None, timeout=20, env=os.environ):
        import requests
        self.requests = requests
        self.mode = mode
        self.timeout = timeout
        self.session = requests.Session()
        if mode == "oauth":
            self.base = OAUTH_BASE
            self.oauth = OAuth1a.from_env(env)
        elif mode == "gateway":
            url = gateway_url or env.get("IBKR_GATEWAY_URL")
            if not url:
                raise IbkrError("gateway mode needs execution_eu.gateway_url or IBKR_GATEWAY_URL")
            self.base = url.rstrip("/") + ("" if url.rstrip("/").endswith("/v1/api") else "/v1/api")
            self.oauth = None
        else:
            raise IbkrError(f"unknown auth mode {mode!r}")
        self.authenticated = False

    # -- transport
    def _call(self, method, path, query=None, body=None, retries=2):
        url = self.base + path
        headers = self.oauth.sign(method, url, query) if self.oauth else {"User-Agent": USER_AGENT}
        if body is not None:
            headers["Content-Type"] = "application/json"
        last = None
        for attempt in range(retries + 1):
            try:
                r = self.session.request(method, url, params=query,
                                         data=None if body is None else json.dumps(body),
                                         headers=headers, timeout=self.timeout)
            except self.requests.RequestException as e:
                last = f"{type(e).__name__}: {e}"
                time.sleep(1.5 * (attempt + 1))
                if self.oauth:
                    headers = self.oauth.sign(method, url, query)
                    if body is not None:
                        headers["Content-Type"] = "application/json"
                continue
            if r.status_code in (429, 503) and attempt < retries:
                time.sleep(2.0 * (attempt + 1))
                continue
            if r.status_code >= 400:
                raise IbkrError(f"{method} {path} -> HTTP {r.status_code}: {r.text[:400]}")
            if not r.text.strip():
                return None
            try:
                return r.json()
            except ValueError:
                raise IbkrError(f"{method} {path} returned non-JSON: {r.text[:200]}")
        raise IbkrError(f"{method} {path} failed: {last}")

    def get(self, path, query=None):
        return self._call("GET", path, query=query)

    def post(self, path, body=None, query=None):
        return self._call("POST", path, query=query, body=body if body is not None else {})

    def delete(self, path):
        return self._call("DELETE", path)

    # -- session
    def connect(self):
        if self.oauth:
            url = self.base + "/oauth/live_session_token"
            headers, a = self.oauth.lst_request(url)
            r = self.session.post(url, headers=headers, timeout=self.timeout)
            if r.status_code >= 400:
                raise IbkrError(f"live session token refused: HTTP {r.status_code}: {r.text[:400]}"
                                " (a key registered today only works after IBKR's overnight"
                                " maintenance; a 401 can also mean the wrong realm or user)")
            self.oauth.accept_lst(r.json(), a)
            self.post("/iserver/auth/ssodh/init", {"publish": True, "compete": True})
        status = {}
        for _ in range(10):
            status = self.post("/iserver/auth/status") or {}
            if status.get("authenticated"):
                break
            time.sleep(2)
        if not status.get("authenticated"):
            raise IbkrError(f"brokerage session not authenticated: {status}")
        self.authenticated = True
        self.iserver_accounts = self.get("/iserver/accounts") or {}
        return status

    def tickle(self):
        return self.post("/tickle")

    def logout(self):
        try:
            self.post("/logout")
        except IbkrError:
            pass

    # -- account
    def accounts(self):
        """The accounts this login can trade. /iserver/accounts lists them; the
        portfolio endpoints also need /portfolio/accounts called first."""
        acc = (getattr(self, "iserver_accounts", None) or self.get("/iserver/accounts") or {})
        try:
            self.get("/portfolio/accounts")
        except IbkrError:
            pass
        return list(acc.get("accounts") or [])

    def summary(self, acct):
        return self.get(f"/portfolio/{acct}/summary") or {}

    def positions(self, acct):
        out, page = [], 0
        while page < 20:
            rows = self.get(f"/portfolio/{acct}/positions/{page}") or []
            out.extend(rows)
            if len(rows) < 100:
                break
            page += 1
        return [p for p in out if p.get("position")]

    def live_orders(self):
        r = self.get("/iserver/account/orders", {"force": "true"}) or {}
        time.sleep(1)       # the first call after force=true can return a partial list
        r = self.get("/iserver/account/orders") or r
        return r.get("orders") or []

    def cancel(self, acct, order_id):
        return self.delete(f"/iserver/account/{acct}/order/{order_id}")

    # -- contracts and prices
    def stock_contracts(self, symbol):
        r = self.get("/trsrv/stocks", {"symbols": symbol}) or {}
        out = []
        for entry in r.get(symbol, []) or []:
            for c in entry.get("contracts", []) or []:
                out.append({"conid": c.get("conid"), "exchange": c.get("exchange"),
                            "name": entry.get("name"), "isUS": c.get("isUS")})
        return out

    def contract_info(self, conid):
        return self.get(f"/iserver/contract/{conid}/info") or {}

    def snapshot(self, conids, fields=("31", "84", "86")):
        """Last, bid, ask. The first call for a conid only subscribes, so ask twice."""
        q = {"conids": ",".join(str(c) for c in conids), "fields": ",".join(fields)}
        self.get("/iserver/marketdata/snapshot", q)
        time.sleep(1.5)
        rows = self.get("/iserver/marketdata/snapshot", q) or []
        out = {}
        for row in rows:
            def num(k):
                v = row.get(k)
                if v in (None, ""):
                    return None
                # prefixes: C = prior close, H = halted, D = delayed (no market-data
                # subscription: IBKR then serves its free 15-minute delayed quote)
                s = str(v).lstrip("CHD").replace(",", "")
                try:
                    return float(s)
                except ValueError:
                    return None
            out[int(row.get("conid"))] = {"last": num("31"), "bid": num("84"), "ask": num("86")}
        return out

    # -- orders
    def place(self, acct, order: dict, max_replies=6):
        """Submit one order and answer IBKR's confirmation prompts. Every prompt text
        is returned so the run log shows what was confirmed."""
        r = self.post(f"/iserver/account/{acct}/orders", {"orders": [order]})
        prompts = []
        for _ in range(max_replies):
            item = r[0] if isinstance(r, list) and r else r
            if not isinstance(item, dict):
                raise IbkrError(f"unexpected order response: {r}")
            if item.get("order_id") or item.get("orderId"):
                return {"order_id": str(item.get("order_id") or item.get("orderId")),
                        "status": item.get("order_status"), "prompts": prompts, "raw": item}
            if item.get("error"):
                raise IbkrError(f"order refused: {item.get('error')}")
            if item.get("id") and item.get("message"):
                prompts.append(" | ".join(item.get("message")) if isinstance(item.get("message"), list)
                               else str(item.get("message")))
                r = self.post(f"/iserver/reply/{item['id']}", {"confirmed": True})
                continue
            raise IbkrError(f"unexpected order response: {item}")
        raise IbkrError(f"order still asking for confirmation after {max_replies} replies: {prompts}")
