#!/usr/bin/env python3
"""Shadow News Grounding Engine: Quantifying market response to wire news across liquid horizons.

Tracks both raw return and beta-adjusted excess return against SPY across:
  - 5m, 15m, 60m (intraday algorithmic / initial price discovery)
  - session_close (closing auction of the news session)
  - next_open (opening cross following the news)
  - next_close (24h benchmark)
  - 1d (24 hours from announcement)
  - 5d (1-week institutional rebalancing)
  - 1m (1-month structural repricing)

Generates empirical response multipliers (kappa_tau,line) for grounding unpriced findings.
"""
import argparse
import gzip
import json
import math
import os
import statistics as st
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
REPO = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
YQ = "https://query1.finance.yahoo.com"
CHART_URL = f"{YQ}/v8/finance/chart/{{t}}?interval={{iv}}&range={{rg}}"
SHADOW_LEDGER_PATH = REPO / "researcher_us" / "analysis" / "shadow-ledger.json"

TIMEFRAMES = [
    "5m", "15m", "60m", "session_close", "next_open", "next_close", "1d", "5d", "1m"
]

def yahoo_symbol(ticker):
    return ticker.upper().replace(".", "-")

def get_json(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last = e
            time.sleep(1.0 + i)
    return None

def fetch_daily_bars(ticker, days=400):
    """Daily bars for macro horizons (1d, 5d, 1m) and beta calculation."""
    sym = yahoo_symbol(ticker)
    url = f"{YQ}/v8/finance/chart/{sym}?range={days}d&interval=1d"
    j = get_json(url)
    if not j or "chart" not in j or not j["chart"]["result"]:
        return []
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(res["timestamp"]):
        c = q["close"][i]
        o = q["open"][i]
        if c is None:
            continue
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(ET)
        out.append({
            "timestamp": ts,
            "date": dt.date().isoformat(),
            "open": o,
            "close": c,
            "volume": q["volume"][i] or 0
        })
    return out

def fetch_intraday_bars(ticker, interval="5m", rng="60d"):
    """Intraday bars for high-frequency horizons (5m, 15m, 60m)."""
    sym = yahoo_symbol(ticker)
    url = f"{YQ}/v8/finance/chart/{sym}?range={rng}&interval={interval}&includePrePost=true"
    j = get_json(url)
    if not j or "chart" not in j or not j["chart"]["result"]:
        return []
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(res["timestamp"]):
        c = q["close"][i]
        o = q["open"][i]
        if c is None:
            continue
        dt = datetime.fromtimestamp(ts, timezone.utc).astimezone(ET)
        out.append({
            "timestamp": ts,
            "datetime": dt.isoformat(),
            "date": dt.date().isoformat(),
            "minute_of_day": dt.hour * 60 + dt.minute,
            "open": o,
            "close": c,
            "volume": q["volume"][i] or 0
        })
    return out

def calculate_beta(stock_daily, spy_daily, lookback=60):
    """Calculates rolling 60-day beta of the stock against SPY."""
    stock_map = {r["date"]: r["close"] for r in stock_daily}
    spy_map = {r["date"]: r["close"] for r in spy_daily}
    common = sorted(set(stock_map) & set(spy_map))
    if len(common) < 20:
        return 1.0  # fallback to market-neutral 1.0
    common = common[-lookback:]
    s_ret = [stock_map[common[i]] / stock_map[common[i - 1]] - 1 for i in range(1, len(common))]
    m_ret = [spy_map[common[i]] / spy_map[common[i - 1]] - 1 for i in range(1, len(common))]
    
    var_m = st.pvariance(m_ret) if len(m_ret) > 1 else 0
    if var_m == 0:
        return 1.0
    mean_s, mean_m = st.fmean(s_ret), st.fmean(m_ret)
    cov = sum((s_ret[i] - mean_s) * (m_ret[i] - mean_m) for i in range(len(s_ret))) / len(s_ret)
    return round(cov / var_m, 3)

def compute_multi_horizon_moves(stock_intra, stock_daily, spy_intra, spy_daily, news_ts_utc, beta=1.0):
    """Computes raw and excess return across all 9 liquid horizons for news landing at news_ts_utc."""
    # Find baseline price at t0
    news_dt = datetime.fromisoformat(news_ts_utc.replace("Z", "+00:00")).astimezone(ET)
    news_epoch = int(news_dt.timestamp())
    news_date = news_dt.date().isoformat()
    
    def price_at_ts(bars, target_epoch, mode="at_or_after"):
        if not bars:
            return None
        if mode == "at_or_after":
            valid = [b for b in bars if b["timestamp"] >= target_epoch]
            return valid[0]["open"] if valid else None
        elif mode == "at_or_before":
            valid = [b for b in bars if b["timestamp"] <= target_epoch]
            return valid[-1]["close"] if valid else None
        return None

    p0 = price_at_ts(stock_intra, news_epoch, mode="at_or_before")
    spy0 = price_at_ts(spy_intra, news_epoch, mode="at_or_before")
    
    # If intraday bar before t0 not found, try open of bar at_or_after
    if p0 is None:
        p0 = price_at_ts(stock_intra, news_epoch, mode="at_or_after")
    if spy0 is None:
        spy0 = price_at_ts(spy_intra, news_epoch, mode="at_or_after")
        
    # If still not found in intraday (e.g. historical aging), fallback to daily close before
    if p0 is None:
        prior = [r for r in stock_daily if r["date"] <= news_date]
        p0 = prior[-1]["close"] if prior else None
    if spy0 is None:
        prior_s = [r for r in spy_daily if r["date"] <= news_date]
        spy0 = prior_s[-1]["close"] if prior_s else None

    if p0 is None or p0 <= 0:
        return {}

    # Map daily bars by date
    s_day_map = {r["date"]: r for r in stock_daily}
    spy_day_map = {r["date"]: r for r in spy_daily}
    sorted_dates = sorted(s_day_map.keys())

    moves = {}
    
    # 1. High frequency intraday: 5m, 15m, 60m
    for tf, delta_sec in [("5m", 300), ("15m", 900), ("60m", 3600)]:
        t_target = news_epoch + delta_sec
        p_target = price_at_ts(stock_intra, t_target, mode="at_or_before")
        spy_target = price_at_ts(spy_intra, t_target, mode="at_or_before")
        if p_target and p0:
            raw = (p_target / p0 - 1) * 100.0
            excess = raw - (beta * ((spy_target / spy0 - 1) * 100.0) if (spy_target and spy0) else 0.0)
            moves[tf] = {"raw_pct": round(raw, 3), "excess_pct": round(excess, 3), "status": "ok"}
        else:
            moves[tf] = {"raw_pct": None, "excess_pct": None, "status": "no_intraday_data"}

    # 2. Session cross: session_close, next_open, next_close
    curr_idx = sorted_dates.index(news_date) if news_date in sorted_dates else -1
    
    # session_close
    if curr_idx >= 0:
        p_close = s_day_map[sorted_dates[curr_idx]]["close"]
        spy_close = spy_day_map.get(sorted_dates[curr_idx], {}).get("close")
        raw = (p_close / p0 - 1) * 100.0
        excess = raw - (beta * ((spy_close / spy0 - 1) * 100.0) if (spy_close and spy0) else 0.0)
        moves["session_close"] = {"raw_pct": round(raw, 3), "excess_pct": round(excess, 3), "status": "ok"}
    else:
        moves["session_close"] = {"raw_pct": None, "excess_pct": None, "status": "missing_daily"}

    # next_open & next_close
    if curr_idx >= 0 and curr_idx + 1 < len(sorted_dates):
        next_d = sorted_dates[curr_idx + 1]
        p_next_open = s_day_map[next_d]["open"]
        p_next_close = s_day_map[next_d]["close"]
        spy_next_open = spy_day_map.get(next_d, {}).get("open")
        spy_next_close = spy_day_map.get(next_d, {}).get("close")

        # next_open
        if p_next_open:
            raw_no = (p_next_open / p0 - 1) * 100.0
            excess_no = raw_no - (beta * ((spy_next_open / spy0 - 1) * 100.0) if (spy_next_open and spy0) else 0.0)
            moves["next_open"] = {"raw_pct": round(raw_no, 3), "excess_pct": round(excess_no, 3), "status": "ok"}
        
        # next_close
        if p_next_close:
            raw_nc = (p_next_close / p0 - 1) * 100.0
            excess_nc = raw_nc - (beta * ((spy_next_close / spy0 - 1) * 100.0) if (spy_next_close and spy0) else 0.0)
            moves["next_close"] = {"raw_pct": round(raw_nc, 3), "excess_pct": round(excess_nc, 3), "status": "ok"}
    else:
        moves["next_open"] = {"raw_pct": None, "excess_pct": None, "status": "unresolved"}
        moves["next_close"] = {"raw_pct": None, "excess_pct": None, "status": "unresolved"}

    # 3. Macro horizons: 1d, 5d, 1m (21 trading days)
    for tf, day_offset in [("1d", 1), ("5d", 5), ("1m", 21)]:
        target_idx = curr_idx + day_offset
        if curr_idx >= 0 and target_idx < len(sorted_dates):
            t_date = sorted_dates[target_idx]
            p_macro = s_day_map[t_date]["close"]
            spy_macro = spy_day_map.get(t_date, {}).get("close")
            raw_m = (p_macro / p0 - 1) * 100.0
            excess_m = raw_m - (beta * ((spy_macro / spy0 - 1) * 100.0) if (spy_macro and spy0) else 0.0)
            moves[tf] = {"raw_pct": round(raw_m, 3), "excess_pct": round(excess_m, 3), "status": "ok"}
        else:
            moves[tf] = {"raw_pct": None, "excess_pct": None, "status": "unresolved_or_outside"}

    return moves

class ShadowLedger:
    def __init__(self, path=SHADOW_LEDGER_PATH):
        self.path = Path(path)
        self.records = self._load()

    def _load(self):
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return {"items": [], "response_matrix": {}}
        return {"items": [], "response_matrix": {}}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.records, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def add_shadow_observation(self, item):
        """Item: {ticker, timestamp_utc, headline, line_item, llm_impact_score, moves, beta, event_iv_pct}"""
        self.records["items"].append(item)
        self.recompute_matrix()

    def recompute_matrix(self):
        """Symmetric Normalization:
        Calculates kappa_{tau, line} = sum(alpha_tilde * Score) / sum(Score^2)
        where alpha_tilde = alpha_excess / event_iv_pct.
        kappa represents standardized return per unit of volatility per score point.
        """
        by_line = {}
        for it in self.records["items"]:
            line = it.get("line_item", "other")
            score = it.get("llm_impact_score", 0.0)
            iv = it.get("event_iv_pct")
            moves = it.get("moves", {})
            if not score or not iv or iv <= 0:
                continue
            by_line.setdefault(line, []).append((score, moves, iv))

        matrix = {}
        for line, observations in by_line.items():
            matrix[line] = {}
            for tf in TIMEFRAMES:
                valid = [
                    (s, obs[tf]["excess_pct"] / iv)
                    for s, obs, iv in observations
                    if tf in obs and obs[tf]["excess_pct"] is not None
                ]
                if not valid:
                    matrix[line][tf] = {"kappa": 0.0, "sample_size": 0, "correlation": 0.0}
                    continue
                sum_xy = sum(x * y for x, y in valid)
                sum_xx = sum(x * x for x, y in valid)
                kappa = round(sum_xy / sum_xx, 5) if sum_xx > 0 else 0.0
                
                xs, ys = [v[0] for v in valid], [v[1] for v in valid]
                r = 0.0
                if len(xs) > 2 and st.pvariance(xs) > 0 and st.pvariance(ys) > 0:
                    r = round(st.correlation(xs, ys), 3)
                matrix[line][tf] = {
                    "kappa": kappa,
                    "sample_size": len(valid),
                    "correlation": r
                }
        self.records["response_matrix"] = matrix

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-ticker", default="AAPL", help="Test ticker for bar verification")
    args = ap.parse_args()

    print(f"Testing market data and multi-timeframe engine for {args.test_ticker} and SPY...")
    spy_daily = fetch_daily_bars("SPY")
    stock_daily = fetch_daily_bars(args.test_ticker)
    spy_intra = fetch_intraday_bars("SPY", interval="5m", rng="5d")
    stock_intra = fetch_intraday_bars(args.test_ticker, interval="5m", rng="5d")

    beta = calculate_beta(stock_daily, spy_daily)
    print(f"{args.test_ticker} 60-day beta against SPY: {beta}")

    if stock_intra:
        test_ts = stock_intra[len(stock_intra) // 2]["datetime"]
        print(f"Calculating multi-horizon moves for test timestamp {test_ts}...")
        moves = compute_multi_horizon_moves(stock_intra, stock_daily, spy_intra, spy_daily, test_ts, beta=beta)
        print(json.dumps(moves, indent=2))

if __name__ == "__main__":
    main()
