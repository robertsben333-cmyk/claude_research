#!/usr/bin/env python3
"""Shared helpers: HTTP with SEC-compliant UA and rate limiting, ticker->CIK."""
import json, os, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
CACHE.mkdir(exist_ok=True)

def _load_keys():
    """Keys live in backtest/.keys.env (gitignored), so they stay out of shell
    history and out of the repo. Environment variables still win if both exist."""
    f = ROOT / ".keys.env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_keys()

SEC_UA = os.environ.get("SEC_UA", "claude-research-backtest xavier.friesen@socfin.nl")
_last = {"sec": 0.0}


def fetch(url, ua=None, timeout=40, retries=2, sec=False, binary=False):
    # The SEC blocks generic user agents. Callers used to have to remember
    # sec=True; when they forgot, the request came back blocked and was recorded
    # as though the document did not exist. Detect the host instead of trusting
    # every call site to get it right.
    if not sec and (".sec.gov/" in url or url.startswith("https://sec.gov")):
        sec = True
    if sec:
        gap = time.time() - _last["sec"]
        if gap < 0.12:
            time.sleep(0.12 - gap)
        _last["sec"] = time.time()
    hdr = {"User-Agent": ua or (SEC_UA if sec else "Mozilla/5.0"),
           "Accept-Encoding": "gzip, deflate"}
    last = None
    for _ in range(retries + 1):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=timeout)
            b = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                import gzip
                b = gzip.decompress(b)
            return b if binary else b.decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(1.0)
    raise last


def cached(name, builder, ttl_hours=24):
    p = CACHE / name
    if p.exists() and (time.time() - p.stat().st_mtime) < ttl_hours * 3600:
        return json.loads(p.read_text(encoding="utf-8"))
    v = builder()
    p.write_text(json.dumps(v), encoding="utf-8")
    return v


def ticker_cik_map():
    def build():
        d = json.loads(fetch("https://www.sec.gov/files/company_tickers.json", sec=True))
        return {v["ticker"]: str(v["cik_str"]).zfill(10) for v in d.values()}
    return cached("ticker_cik.json", build, ttl_hours=168)


def submissions(cik):
    return cached(f"sub_{cik}.json",
                  lambda: json.loads(fetch(f"https://data.sec.gov/submissions/CIK{cik}.json", sec=True)),
                  ttl_hours=12)
