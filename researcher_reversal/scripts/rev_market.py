#!/usr/bin/env python3
"""Market primitives for the reversal stage: the listed universe, daily bars, costs.

WHY THIS IS NOT researcher_us/scripts/edge_bars.py
--------------------------------------------------
`edge_bars.py` caches FIFTEEN-MINUTE bars for a few dozen names inside a sliding
60-day window, because the questions it serves are intraday. This stage asks a
cross-sectional question over the whole listed market and several years, so it
needs daily bars for thousands of names and none of the intraday resolution. The
two caches would fight over the same file for no gain.

THREE THINGS IN HERE THAT ARE EASY TO GET WRONG
-----------------------------------------------
1. EVERY OHLC IS ADJUSTED. A 2-for-1 split shows up in raw closes as a 50% fall,
   which is precisely the event this stage screens for, so a raw-close screen would
   fill with corporate actions and nothing else. Each day's open/high/low/close is
   multiplied by adjclose/close for that day, so returns, the high-low range and the
   spread estimate all sit on one basis.
2. THE SPREAD IS ESTIMATED, NOT OBSERVED. Yahoo serves no historical quotes, and
   spread is the cost that decides whether this stage can exist at all (a 25% faller
   at $170k a day is not a 25% faller you can trade). `corwin_schultz` is the
   standard two-day high-low estimator; it is a floor on the real cost, not the real
   cost, and it is biased low for exactly the thin names this screen selects.
3. THE UNIVERSE IS TODAY'S LISTINGS. Anything that delisted between a past drop and
   today is absent from every historical sample built from it. That removes the worst
   continuations (bankruptcy, going-dark) and therefore biases a backtest TOWARD
   reversal. It cannot be fixed from this source. It is reported rather than hidden:
   see `known_biases` in rev_backtest.py.
"""
import gzip
import json
import math
import re
import statistics
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
      "Accept": "application/json"}
SCREENER = ("https://api.nasdaq.com/api/screener/stocks"
            "?tableonly=false&limit=25000&download=true&exchange={ex}")
CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/{t}"
         "?interval=1d&range={rg}&events=div%2Csplit")
EXCHANGES = ("nasdaq", "nyse", "amex")

# Instruments that are not the thing this stage studies. A warrant or a unit can
# fall 40% on no news at all, and a preferred does not have an equity reaction.
NOT_COMMON = re.compile(
    r"\b(warrant|unit[s]?|right[s]?|preferred|debenture|subordinated)\b"
    r"|%\s*(note|bond|deb)|\bnotes\s+due\b", re.I)
BAD_SYMBOL = re.compile(r"[\^/]|\.(W|U|R|WS|UN|RT)$", re.I)


# ----------------------------------------------------------------- utilities
def num(s):
    """A number out of Nasdaq's money/percent strings, or None."""
    if s is None:
        return None
    t = re.sub(r"[^0-9.\-]", "", str(s))
    if t in ("", "-", ".", "-."):
        return None
    try:
        return float(t)
    except ValueError:
        return None


def median(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def stdev(xs):
    xs = [x for x in xs if x is not None]
    return statistics.stdev(xs) if len(xs) > 1 else None


def get(url, headers=UA, timeout=45, tries=4, backoff=2.0):
    """One GET with the repo's standard backoff. Raises on final failure."""
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:                      # noqa: BLE001
            last = e
            if k < tries - 1:
                time.sleep(backoff ** k)
    raise last


# ------------------------------------------------------------------ universe
def screener(exchanges=EXCHANGES, common_only=True):
    """Every listed name Nasdaq's screener knows, with sector, cap and volume.

    This is the population the daily screen ranks. It is NOT filtered on
    liquidity here: the floor belongs to the screen, so that a run can report how
    many names it removed and a backtest can sweep the floor rather than assume it.
    """
    out, seen = [], set()
    for ex in exchanges:
        d = json.loads(get(SCREENER.format(ex=ex)))
        for r in (d.get("data") or {}).get("rows") or []:
            sym = (r.get("symbol") or "").strip().upper()
            name = (r.get("name") or "").strip()
            if not sym or sym in seen:
                continue
            if common_only and (BAD_SYMBOL.search(sym) or NOT_COMMON.search(name)):
                continue
            seen.add(sym)
            out.append({
                "ticker": sym,
                "company": name,
                "exchange": ex,
                "sector": (r.get("sector") or "").strip() or None,
                "industry": (r.get("industry") or "").strip() or None,
                "country": (r.get("country") or "").strip() or None,
                "ipo_year": num(r.get("ipoyear")),
                "last_sale": num(r.get("lastsale")),
                "pct_change": num(r.get("pctchange")),
                "volume": num(r.get("volume")),
                "market_cap": num(r.get("marketCap")),
            })
    return out


def yahoo_symbol(t):
    """Nasdaq writes class shares BRK.A; Yahoo wants BRK-A."""
    return t.replace(".", "-")


# ---------------------------------------------------------------------- bars
def bars(ticker, rg="2y", raw=False):
    """Adjusted daily OHLCV, oldest first. [] when the chart is empty.

    `raw=True` returns unadjusted prices, which is what a live baseline wants to
    quote as the price a person would have seen. Everything computed here uses the
    adjusted series.
    """
    try:
        d = json.loads(get(CHART.format(t=yahoo_symbol(ticker), rg=rg), tries=3))
    except Exception:                               # noqa: BLE001
        return []
    res = ((d.get("chart") or {}).get("result") or [None])[0]
    if not res:
        return []
    ts = res.get("timestamp") or []
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    adj = ((res.get("indicators") or {}).get("adjclose") or [{}])
    adj = (adj[0] if adj else {}).get("adjclose") or [None] * len(ts)
    tz = (res.get("meta") or {}).get("exchangeTimezoneName") or "America/New_York"
    from datetime import datetime
    from zoneinfo import ZoneInfo
    zone = ZoneInfo(tz)
    out = []
    for i, t in enumerate(ts):
        o, h, l, c = (q.get("open") or [])[i:i + 1], (q.get("high") or [])[i:i + 1], \
                     (q.get("low") or [])[i:i + 1], (q.get("close") or [])[i:i + 1]
        o, h, l, c = (x[0] if x else None for x in (o, h, l, c))
        v = (q.get("volume") or [None] * len(ts))[i]
        a = adj[i] if i < len(adj) else None
        if None in (o, h, l, c) or not c:
            continue
        f = 1.0 if (raw or not a) else (a / c)
        out.append({
            "date": datetime.fromtimestamp(t, zone).date().isoformat(),
            "open": o * f, "high": h * f, "low": l * f, "close": c * f,
            "raw_close": c, "volume": float(v or 0),
        })
    out.sort(key=lambda b: b["date"])
    return out


def bars_many(tickers, rg="2y", workers=8, pause=0.05, on_done=None):
    """Bars for many names, threaded. Returns {ticker: bars}. Failures give []."""
    res, lock = {}, threading.Lock()
    q = list(tickers)
    idx = [0]

    def work():
        while True:
            with lock:
                if idx[0] >= len(q):
                    return
                t = q[idx[0]]
                idx[0] += 1
            b = bars(t, rg=rg)
            time.sleep(pause)
            with lock:
                res[t] = b
                if on_done:
                    on_done(len(res), len(q), t, b)

    ths = [threading.Thread(target=work, daemon=True) for _ in range(workers)]
    for th in ths:
        th.start()
    for th in ths:
        th.join()
    return res


# --------------------------------------------------------------------- costs
def corwin_schultz(win):
    """Two-day high-low bid-ask spread estimate, as a FRACTION of price.

    Corwin & Schultz (2012). `win` is a list of consecutive daily bars; the estimate
    is the median of the per-pair estimates, negatives floored at zero as the paper
    prescribes. Returns None when there is nothing to estimate from.

    Read it as a floor. It assumes continuous trading and no overnight price change,
    both of which fail hardest in thin names and on gap days, and it is estimated
    from the days BEFORE a drop, not the drop day itself, so it does not see the
    widening that the drop causes.
    """
    k = 3 - 2 * math.sqrt(2)
    est = []
    for i in range(1, len(win)):
        a, b = win[i - 1], win[i]
        if min(a["low"], b["low"]) <= 0:
            continue
        b1 = math.log(a["high"] / a["low"]) ** 2 + math.log(b["high"] / b["low"]) ** 2
        hi, lo = max(a["high"], b["high"]), min(a["low"], b["low"])
        g = math.log(hi / lo) ** 2
        alpha = (math.sqrt(2 * b1) - math.sqrt(b1)) / k - math.sqrt(g / k)
        s = 2 * (math.exp(alpha) - 1) / (1 + math.exp(alpha))
        est.append(max(s, 0.0))
    return median(est)


def half_spread_pct(win):
    """Half the estimated spread, in percent. One side of a round trip."""
    s = corwin_schultz(win)
    return None if s is None else round(s * 100 / 2, 4)


# ------------------------------------------------------------------ statistics
def spearman(xs, ys):
    """Rank correlation with average ranks for ties. None when undefined."""
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    n = len(pairs)
    mx, my = sum(rx) / n, sum(ry) / n
    num_ = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return None if den == 0 else round(num_ / den, 4)


def tstat(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return None
    sd = statistics.stdev(xs)
    return None if sd == 0 else round(mean(xs) / (sd / math.sqrt(len(xs))), 3)


def sign_test_p(wins, n):
    """Two-sided binomial p against 50%, exact. For hit rates."""
    if not n:
        return None
    def c(a, b):
        return math.comb(a, b)
    tail = sum(c(n, k) for k in range(0, min(wins, n - wins) + 1))
    return round(min(1.0, 2 * tail / (2 ** n)), 5)


def permutation_p(groups, key=None, val=None, reps=2000, seed=11):
    """Within-group permutation p for a rank correlation.

    `groups` is a list of lists of (x, y) pairs, one list per day. The statistic is the
    pooled within-day centred-rank correlation; the null shuffles y WITHIN each day, so
    market-wide drift on a given day cannot manufacture it. Same construction as
    researcher_us/scripts/edge_resolve.py, for the same reason.

    THE SHUFFLE IS DONE ON THE RANKS, NOT THE VALUES, AND THAT IS NOT A SHORTCUT.
    Permuting y inside a day permutes its centred ranks and nothing else, so the ranks
    can be computed once. Both pooled sums of squares are then invariant across reps and
    only the cross-product moves, which turns each rep from a re-rank of every day into
    one pass of multiply-add. The naive version needed hours on 750 days; this needs
    seconds and returns the same statistic.
    """
    import random
    rng = random.Random(seed)
    xs, ys, spans = [], [], []
    for g in groups:
        if len(g) < 2:
            continue
        rx = _centred([p[0] for p in g])
        ry = _centred([p[1] for p in g])
        spans.append((len(xs), len(xs) + len(rx)))
        xs += rx
        ys += ry
    n = len(xs)
    if n < 3:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    sx = math.sqrt(sum(v * v for v in dx))
    sy = math.sqrt(sum(v * v for v in dy))
    if sx == 0 or sy == 0:
        return None, None
    obs = sum(a * b for a, b in zip(dx, dy)) / (sx * sy)

    # sy is invariant under a within-day shuffle only if every day's mean rank is the
    # same, which centring guarantees (each day centres to zero). Recomputed per rep
    # anyway would cost nothing here, but it is provably unchanged, so it is not.
    hits = 0
    buf = list(dy)
    for _ in range(reps):
        for lo, hi in spans:
            seg = buf[lo:hi]
            rng.shuffle(seg)
            buf[lo:hi] = seg
        r = sum(a * b for a, b in zip(dx, buf)) / (sx * sy)
        if abs(r) >= abs(obs):
            hits += 1
    return round(obs, 4), round((hits + 1) / (reps + 1), 5)


def _centred(v):
    n = len(v)
    order = sorted(range(n), key=lambda i: v[i])
    r = [0.0] * n
    i = 0
    while i < len(order):
        j = i
        while j + 1 < n and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    m = (n + 1) / 2
    return [x - m for x in r]


def bootstrap_ci(xs, reps=4000, seed=7, lo=2.5, hi=97.5):
    """Percentile CI of the mean.

    `random.choices` and `sum` rather than a Python resampling loop: on a sample of
    eleven thousand names this function is called eighty times by one backtest, and the
    loop version turned a two-minute run into a forty-minute one for an identical
    interval. Reps are trimmed on very large samples, where the interval is already
    stable to the third decimal.
    """
    import random
    xs = [x for x in xs if x is not None]
    n = len(xs)
    if n < 3:
        return None, None
    if n > 5000:
        reps = min(reps, 1200)
    rng = random.Random(seed)
    ch = rng.choices
    ms = sorted(sum(ch(xs, k=n)) / n for _ in range(reps))
    return (round(ms[int(len(ms) * lo / 100)], 4),
            round(ms[min(len(ms) - 1, int(len(ms) * hi / 100))], 4))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "screener":
        u = screener()
        print(json.dumps({"n": len(u), "sample": u[:3]}, indent=2))
    elif len(sys.argv) > 2 and sys.argv[1] == "bars":
        b = bars(sys.argv[2], rg=sys.argv[3] if len(sys.argv) > 3 else "1mo")
        print(json.dumps(b[-5:], indent=2))
    else:
        print(__doc__)
