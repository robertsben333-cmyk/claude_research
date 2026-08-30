#!/usr/bin/env python3
"""What the market has already priced into an imminent earnings print.

This is the baseline the edge hunt is measured against, and it is deliberately
computed by code rather than by an agent. An agent that decides for itself what
was "already priced" after it has found something will always conclude the
finding is new. So the baseline is snapshotted first, written to disk, and the
hunters never get to revise it.

Three layers, cheapest first:

  tape      spot, run-up, distance from 52w extremes, realised vol, volume
  history   the last eight reactions to this company's own prints, from EDGAR
            8-K item 2.02 acceptance times -- exact, not scraped
  options   the front expiry covering the event: ATM implied vol, the straddle
            implied move, and the 25-delta skew

The skew is the part that does not exist anywhere else in this repo, and it is
the only thing here that carries *direction*. A straddle says how far the market
thinks the stock moves; the risk reversal says which side it is paying to be
protected on. `event_implied_move_pct` has been null in every anchors.json ever
written because option chains are not recoverable retrospectively. Run forward,
it is free.

    python3 scripts/priced_in.py --ticker SAIC --date 2026-08-31 --session bmo
    python3 scripts/priced_in.py --tickers SAIC,SY,LX --date 2026-08-31 -o baselines/
"""
import argparse
import http.cookiejar
import json
import math
import statistics
import sys
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SEC_UA = "claude-research-edge-hunt xavier.friesen@socfin.nl"
YQ = "https://query1.finance.yahoo.com"
RISK_FREE = 0.04

_session = {"opener": None, "crumb": None}


def _yahoo():
    """Yahoo's options endpoint returns 401 bare. It wants a cookie and a crumb.

    The chart endpoint does not, which is why the rest of the repo never had to
    do this. Cached for the life of the process; the crumb is good for hours.
    """
    if _session["opener"] is not None:
        return _session["opener"], _session["crumb"]
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    try:
        op.open(urllib.request.Request("https://fc.yahoo.com",
                                       headers={"User-Agent": UA}), timeout=20)
    except Exception:
        pass  # expected to 404; we only want the Set-Cookie it carries
    crumb = op.open(
        urllib.request.Request(f"{YQ}/v1/test/getcrumb", headers={"User-Agent": UA}),
        timeout=20).read().decode().strip()
    _session["opener"], _session["crumb"] = op, crumb
    return op, crumb


def get_json(url, sec=False, tries=3):
    hdr = {"User-Agent": SEC_UA if sec else UA, "Accept": "application/json"}
    last = None
    for i in range(tries):
        try:
            if sec:
                time.sleep(0.15)
                r = urllib.request.urlopen(urllib.request.Request(url, headers=hdr),
                                           timeout=30)
            else:
                op, _ = _yahoo()
                r = op.open(urllib.request.Request(url, headers=hdr), timeout=30)
            return json.loads(r.read())
        except Exception as e:
            last = e
            time.sleep(1.0 + i)
    raise last


# ---------------------------------------------------------------- tape

def bars(ticker, days=460):
    j = get_json(f"{YQ}/v8/finance/chart/{ticker}?range={days}d&interval=1d")
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(res["timestamp"]):
        c = q["close"][i]
        if c is None:
            continue
        out.append({"date": datetime.fromtimestamp(ts, timezone.utc).date().isoformat(),
                    "close": c, "volume": q["volume"][i] or 0})
    return out


def tape(rows, event_date, session):
    """Bars strictly usable before the print. For bmo the event day has not traded."""
    pre = [r for r in rows
           if r["date"] < event_date or (session == "amc" and r["date"] == event_date)]
    if len(pre) < 30:
        return None, f"only {len(pre)} usable bars"
    closes = [r["close"] for r in pre]
    rets = [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes))]
    yr = closes[-252:] if len(closes) >= 252 else closes
    return {
        "last_close_date": pre[-1]["date"],
        "spot": round(closes[-1], 4),
        "run_up_5d_pct": round((closes[-1] / closes[-6] - 1) * 100, 2) if len(closes) > 6 else None,
        "run_up_20d_pct": round((closes[-1] / closes[-21] - 1) * 100, 2) if len(closes) > 21 else None,
        "pct_from_52w_high": round((closes[-1] / max(yr) - 1) * 100, 2),
        "pct_from_52w_low": round((closes[-1] / min(yr) - 1) * 100, 2),
        "realised_vol_20d_annualised_pct": round(statistics.pstdev(rets[-20:]) * (252 ** .5) * 100, 1),
        "avg_volume_20d": int(sum(r["volume"] for r in pre[-20:]) / 20),
    }, None


# ---------------------------------------------------------------- history

def cik_for(ticker):
    j = get_json("https://www.sec.gov/files/company_tickers.json", sec=True)
    for row in j.values():
        if row["ticker"].upper() == ticker.upper():
            return str(row["cik_str"]).zfill(10)
    return None


def prior_prints(cik, before, n=8):
    """Past earnings filings with their session, from EDGAR acceptance time.

    Domestic filers announce on an 8-K carrying item 2.02. The item code is exact,
    the acceptance time is authoritative, and FINDINGS.md §3 already established
    that it recovers the session reliably.

    Foreign private issuers file a 6-K instead, and 6-K has no item codes. Probed
    on LX, SY and SSL: `primaryDocDescription` is empty or the literal string
    "6-K", and the filing-index document names are opaque accession numbers and
    image files. Neither can distinguish a results release from a press release
    about anything else, so no history is returned rather than a guessed one. The
    deadband falls back to realised vol and `baseline_quality` drops to thin,
    which is the correct downstream consequence: for these names there is no
    defensible statement of what the market has priced.
    """
    from zoneinfo import ZoneInfo
    j = get_json(f"https://data.sec.gov/submissions/CIK{cik}.json", sec=True)
    r = j["filings"]["recent"]

    # A CIK outlives the company attached to it. CHRN, first live run: seven prior
    # reactions returned, all of them prints by Ekso Bionics Holdings, which held
    # this CIK from 2014 until a reverse merger on 2026-05-05 issued 138.2m new
    # shares to a different business. Different company, different capital
    # structure, different investor base -- and the history read as ChronoScale's
    # own. `formerNames` says exactly when the identity changed and is free to
    # check, so prints from before the change are excluded rather than pooled.
    identity_since = None
    for fn in (j.get("formerNames") or []):
        to = (fn.get("to") or "")[:10]
        if to and (identity_since is None or to > identity_since):
            identity_since = to

    out, saw_6k, dropped = [], False, 0
    for i, form in enumerate(r["form"]):
        if form == "6-K":
            saw_6k = True
            continue
        if form != "8-K" or "2.02" not in (r["items"][i] or ""):
            continue
        dt = datetime.fromisoformat(r["acceptanceDateTime"][i].replace("Z", "+00:00")) \
            .astimezone(ZoneInfo("America/New_York"))
        if dt.date().isoformat() >= before:
            continue
        ed = dt.date().isoformat()
        if identity_since and ed < identity_since:
            dropped += 1
            continue
        hhmm = dt.hour * 60 + dt.minute
        out.append({"event_date": ed,
                    "session": "amc" if hhmm >= 960 else ("bmo" if hhmm <= 570 else "intraday")})
        if len(out) >= n:
            break
    if out:
        basis = "8-K item 2.02 acceptance times (exact)"
        if dropped:
            basis += (f"; {dropped} earlier print(s) excluded as filed under a former "
                      f"name on this CIK before {identity_since}")
        return out, basis
    if dropped:
        return [], (f"all {dropped} prior print(s) on this CIK were filed under a former "
                    f"name before {identity_since}, so they belong to a predecessor "
                    "entity and are not this company's reaction history")
    if saw_6k:
        return [], ("foreign private issuer: files 6-K, which carries no item codes and "
                    "no usable document description, so earnings dates are not "
                    "recoverable from EDGAR metadata")
    return [], "no 8-K item 2.02 filings found before the cutoff"


def reaction(rows, event_date, session):
    """Close before the print to close after the first full session following it.

    The same convention LEDGER.md uses, so a historical move computed here is
    comparable to a scored one.
    """
    idx = {r["date"]: i for i, r in enumerate(rows)}
    dates = [r["date"] for r in rows]
    if session == "amc":
        before = [d for d in dates if d <= event_date]
        after = [d for d in dates if d > event_date]
    else:
        before = [d for d in dates if d < event_date]
        after = [d for d in dates if d >= event_date]
    if not before or not after:
        return None
    b, a = rows[idx[before[-1]]]["close"], rows[idx[after[0]]]["close"]
    return round((a / b - 1) * 100, 2)


def plausibility(hist, event_date):
    """Does an event on this date fit the company's own filing cadence?

    A calendar row is a claim, not a schedule. Aggregators project the last known
    cadence forward, so a company that changed how it reports -- or stopped
    reporting altogether -- keeps generating future "earnings dates" that nobody
    has confirmed. The check is cheap: compare the gap since the last real
    earnings filing against the median gap between the ones before it.
    """
    if len(hist) < 3:
        return {"verdict": "unknown", "reason": "fewer than 3 prior prints to infer a cadence from"}
    ds = [date.fromisoformat(h["event_date"]) for h in hist]     # newest first
    gaps = [(ds[i] - ds[i + 1]).days for i in range(len(ds) - 1)]
    typical = statistics.median(gaps)
    since = (date.fromisoformat(event_date) - ds[0]).days
    out = {"days_since_last_print": since,
           "median_gap_days": round(typical, 1),
           "ratio": round(since / typical, 2) if typical else None,
           "last_print": hist[0]["event_date"]}
    if not typical:
        out["verdict"] = "unknown"
        out["reason"] = "cannot infer a cadence"
    elif since < 0.5 * typical:
        out["verdict"] = "suspect"
        out["reason"] = (f"an event {since} days after the last print does not fit a "
                         f"{typical:.0f}-day cadence; the calendar row may be stale")
    elif since > 1.8 * typical:
        out["verdict"] = "suspect"
        out["reason"] = (f"{since} days since the last earnings filing against a "
                         f"{typical:.0f}-day cadence; the company may have changed or "
                         "stopped its reporting, which would also make the reaction "
                         "history above describe a regime that no longer exists")
    else:
        out["verdict"] = "fits_cadence"
        out["reason"] = f"{since} days since the last print against a {typical:.0f}-day cadence"
    return out


# ---------------------------------------------------------------- options

def _ncdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _delta(spot, strike, iv, t, kind):
    if iv <= 0 or t <= 0 or spot <= 0 or strike <= 0:
        return None
    d1 = (math.log(spot / strike) + (RISK_FREE + iv * iv / 2) * t) / (iv * math.sqrt(t))
    return _ncdf(d1) if kind == "call" else _ncdf(d1) - 1.0


def _mid(o):
    b, a = o.get("bid") or 0, o.get("ask") or 0
    if b > 0 and a > 0:
        return (b + a) / 2
    return o.get("lastPrice") or 0


def _interp_iv(legs, target_delta):
    """IV at a target delta, linearly interpolated between the straddling strikes."""
    pts = sorted((l for l in legs if l["delta"] is not None), key=lambda l: l["delta"])
    for i in range(len(pts) - 1):
        lo, hi = pts[i], pts[i + 1]
        if lo["delta"] <= target_delta <= hi["delta"]:
            span = hi["delta"] - lo["delta"]
            if span == 0:
                return lo["iv"]
            w = (target_delta - lo["delta"]) / span
            return lo["iv"] + w * (hi["iv"] - lo["iv"])
    return None


def options(ticker, event_date, spot, realised_vol_pct=None):
    """Front expiry that covers the event: ATM vol, straddle move, 25-delta skew."""
    try:
        op, crumb = _yahoo()
    except Exception as e:
        return {"status": f"crumb_failed: {type(e).__name__}"}
    try:
        j = get_json(f"{YQ}/v7/finance/options/{ticker}?crumb={crumb}")
        res = j["optionChain"]["result"]
        if not res:
            return {"status": "no_options_market"}
        exps = res[0].get("expirationDates") or []
        if not exps:
            return {"status": "no_options_market"}
        ed = date.fromisoformat(event_date)
        covering = [e for e in exps
                    if datetime.fromtimestamp(e, timezone.utc).date() > ed]
        if not covering:
            return {"status": "no_expiry_after_event"}
        target = covering[0]
        j = get_json(f"{YQ}/v7/finance/options/{ticker}?date={target}&crumb={crumb}")
        chain = j["optionChain"]["result"][0]["options"][0]
    except Exception as e:
        return {"status": f"chain_failed: {type(e).__name__}: {str(e)[:80]}"}

    exp_date = datetime.fromtimestamp(target, timezone.utc).date()
    t = max((exp_date - date.today()).days, 1) / 365.0
    calls, puts = chain.get("calls") or [], chain.get("puts") or []
    if not calls or not puts:
        return {"status": "empty_chain", "expiry": exp_date.isoformat()}

    sc = {c["strike"]: c for c in calls}
    sp = {p["strike"]: p for p in puts}
    both = sorted(set(sc) & set(sp))
    if not both:
        return {"status": "no_paired_strikes", "expiry": exp_date.isoformat()}
    atm = min(both, key=lambda k: abs(k - spot))
    warn = []

    # Liquidity guard. An illiquid chain still returns numbers, and they are
    # garbage rather than missing: the first run produced a 135.69% implied move
    # for AIV and a -124 vol-point skew for GASS, both from one-sided quotes and
    # stale lastPrice. Numbers that wrong reaching a hunter would anchor it hard.
    def two_sided(o):
        return (o.get("bid") or 0) > 0 and (o.get("ask") or 0) > 0

    def spread_frac(o):
        b, a = o.get("bid") or 0, o.get("ask") or 0
        m = (b + a) / 2
        return (a - b) / m if m > 0 else 9.9

    quoted = two_sided(sc[atm]) and two_sided(sp[atm])
    worst_spread = max(spread_frac(sc[atm]), spread_frac(sp[atm]))
    straddle = _mid(sc[atm]) + _mid(sp[atm])
    implied = round(straddle / spot * 100, 2) if spot else None
    atm_iv = statistics.fmean([sc[atm].get("impliedVolatility") or 0,
                               sp[atm].get("impliedVolatility") or 0])

    # Reject only what is unusable; flag the rest. The first version nulled any
    # straddle wider than 40% of mid and threw away SAIC -- a $5.4bn name whose
    # only listed expiry is monthly, quoted over a weekend, at 41%. A wide spread
    # makes a number noisy; it does not make it a leak. So the number survives
    # with its spread attached and `confidence_penalty` carries the cost.
    if not quoted:
        warn.append("ATM legs not two-sided; no live bid/ask to price a straddle from")
        implied = None
    elif worst_spread > 0.80:
        warn.append(f"ATM bid-ask spread {worst_spread:.0%} of mid; too wide to mean anything")
        implied = None
    elif worst_spread > 0.35:
        warn.append(f"ATM bid-ask spread {worst_spread:.0%} of mid; implied move is indicative only")
    if implied is not None and implied > 60:
        warn.append(f"implied move {implied}% is implausible for a single print; rejected")
        implied = None

    def legs(side, kind):
        out = []
        for o in side:
            iv = o.get("impliedVolatility") or 0
            if not (0.05 <= iv <= 3.0):          # outside this the IV is a solver artefact
                continue
            if not two_sided(o) or (o.get("openInterest") or 0) < 1:
                continue
            out.append({"strike": o["strike"], "iv": iv,
                        "delta": _delta(spot, o["strike"], iv, t, kind)})
        return out

    iv_c25 = _interp_iv(legs(calls, "call"), 0.25)
    iv_p25 = _interp_iv(legs(puts, "put"), -0.25)
    skew = round((iv_p25 - iv_c25) * 100, 2) if (iv_c25 and iv_p25) else None
    if skew is not None and abs(skew) > 40:
        warn.append(f"25-delta skew {skew} vol points is outside any plausible range; rejected")
        skew = None

    oi_c = sum(c.get("openInterest") or 0 for c in calls)
    oi_p = sum(p.get("openInterest") or 0 for p in puts)
    dte = (exp_date - date.today()).days

    # Strip the non-event vol out of the straddle. A straddle expiring 18 days
    # after the print prices 18 days of ordinary movement plus the earnings jump;
    # read raw, it says SAIC has a 10.3% earnings move when most of that is just
    # time. Subtract the ordinary component in variance and what is left is the
    # jump the market is actually paying for.
    event_implied = implied
    decomp = None
    if implied is not None and realised_vol_pct and dte > 1:
        trading_days = max(1.0, dte * 5.0 / 7.0)
        sigma_period = (realised_vol_pct / 100.0) * (trading_days / 252.0) ** 0.5
        sigma_total = (implied / 100.0) / 0.7979          # ATM straddle ~ 0.7979*sigma
        if sigma_total > 0:
            frac = max(0.0, 1.0 - (sigma_period / sigma_total) ** 2) ** 0.5
            event_implied = round(implied * frac, 2)
            decomp = (f"{implied}% straddle over {dte} calendar days less "
                      f"{round(sigma_period * 100, 2)}% of ordinary 20d-realised movement, "
                      "subtracted in variance")

    out = {
        "status": "ok" if (implied is not None or skew is not None) else "unusable_chain",
        "expiry": exp_date.isoformat(),
        "days_to_expiry": dte,
        "atm_strike": atm,
        "atm_iv_pct": round(atm_iv * 100, 1) if quoted else None,
        "straddle_implied_move_pct": implied,
        "event_implied_move_pct": event_implied,
        "event_implied_move_basis": decomp or "straddle taken as-is (no vol anchor to net off)",
        "skew_25d_vol_points": skew,
        "skew_note": "IV(25d put) - IV(25d call). Positive = the market is paying more "
                     "for downside protection than for upside.",
        "put_call_open_interest_ratio": round(oi_p / oi_c, 2) if oi_c else None,
        "total_open_interest": oi_c + oi_p,
        "atm_spread_frac_of_mid": round(worst_spread, 3) if quoted else None,
        "warnings": warn,
    }
    if skew is not None:
        out["priced_direction_lean"] = ("downside paid" if skew > 2
                                        else "upside paid" if skew < -2 else "balanced")
    return out


# ---------------------------------------------------------------- assembly

def build(ticker, event_date, session):
    ticker = ticker.upper()
    doc = {
        "ticker": ticker,
        "event_date": event_date,
        "session": session,
        "as_of_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": ["yahoo chart v8 daily bars",
                    "yahoo options v7 front expiry (cookie+crumb)",
                    "sec edgar submissions api, 8-K item 2.02 acceptance times"],
    }
    try:
        rows = bars(ticker)
    except Exception as e:
        doc["status"] = f"bars_failed: {type(e).__name__}"
        return doc
    tp, err = tape(rows, event_date, session)
    if err:
        doc["status"] = err
        return doc
    doc["tape"] = tp
    spot = tp["spot"]

    hist, cik, basis = [], None, "not attempted"
    try:
        cik = cik_for(ticker)
        if cik:
            prints, basis = prior_prints(cik, event_date)
            for e in prints:
                m = reaction(rows, e["event_date"], e["session"])
                if m is not None:
                    hist.append({**e, "move_pct": m})
        else:
            basis = "no CIK on EDGAR for this ticker"
    except Exception as e:
        basis = f"edgar lookup failed: {type(e).__name__}"
    absm = [abs(h["move_pct"]) for h in hist]
    doc["cik"] = cik
    doc["history"] = {
        "moves": hist,
        "n": len(hist),
        "basis": basis,
        "median_abs_move_pct": round(statistics.median(absm), 2) if absm else None,
        "max_abs_move_pct": round(max(absm), 2) if absm else None,
        "up_count": sum(1 for h in hist if h["move_pct"] > 0),
    }

    # Does an event on this date fit the company's own filing cadence?
    #
    # AIV, first live run: the calendar said 2026-08-31, the baseline reported six
    # prior reactions and tier `partial`, and all of it was wrong. Aimco has been in
    # liquidation since a shareholder vote on 2026-02-06, filed its Q2 10-Q on
    # 2026-08-07 with no accompanying item 2.02 8-K, and has issued no earnings
    # release since 2026-03-02. The six reactions came from a reporting regime the
    # company had abandoned, and the date was an aggregator projecting the old
    # cadence forward. It cost an opus/high hunter to discover that, and it should
    # have cost a subtraction.
    doc["event_plausibility"] = plausibility(hist, event_date)

    doc["options"] = options(ticker, event_date, spot,
                             tp.get("realised_vol_20d_annualised_pct"))

    # The deadband: below this, the reaction had no direction in it and the event
    # is not scored. Preferred basis is the name's own reaction history; where
    # EDGAR yields none, a one-day move of one realised standard deviation stands
    # in, because a 2% default would call a routine day on a 90%-vol microcap a
    # directional hit.
    med = doc["history"]["median_abs_move_pct"]
    rv = tp["realised_vol_20d_annualised_pct"]
    if med:
        doc["deadband_pct"] = round(max(1.5, 0.5 * med), 2)
        doc["deadband_basis"] = f"half the median of {len(absm)} prior reactions, floored at 1.5%"
    else:
        daily = (rv / 100.0) / (252 ** 0.5) * 100 if rv else None
        doc["deadband_pct"] = round(max(1.5, daily), 2) if daily else 2.0
        doc["deadband_basis"] = ("one day at 20d realised vol (no earnings history on EDGAR)"
                                 if daily else "default 2.0% (no history, no vol)")
    doc["deadband_note"] = ("A realised move inside this band is scored as no-direction "
                            "rather than as a miss.")

    im = doc["options"].get("event_implied_move_pct")
    doc["expected_move_pct"] = im if im else med
    doc["expected_move_basis"] = ("option straddle net of ordinary vol, front expiry"
                                  if im else "median historical reaction (no usable option chain)")

    # One place downstream can look to decide whether this name is researchable.
    have = doc["options"].get("status") == "ok"
    suspect = doc["event_plausibility"].get("verdict") == "suspect"
    usable_hist = 0 if suspect else len(absm)
    tier = ("full" if have and usable_hist >= 4
            else "partial" if (have or usable_hist >= 4)
            else "thin")
    doc["baseline_quality"] = {
        "options_usable": have,
        "history_events": len(absm),
        "history_usable": usable_hist,
        "event_plausibility": doc["event_plausibility"].get("verdict"),
        "priced_direction_available": doc["options"].get("skew_25d_vol_points") is not None,
        "tier": tier,
        "note": "thin means there is no reliable statement of what the market priced, so "
                "a confident call on this name cannot be justified by the baseline.",
    }
    if suspect:
        doc["baseline_quality"]["history_discount_note"] = (
            "reaction history is present but not counted toward the tier: the event date "
            "does not fit this company's own filing cadence, so the history may describe "
            "a reporting regime it no longer follows")
    doc["status"] = "ok"
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker")
    ap.add_argument("--tickers", help="comma-separated list")
    ap.add_argument("--date", required=True, help="event date YYYY-MM-DD")
    ap.add_argument("--session", default="bmo", choices=["bmo", "amc"])
    ap.add_argument("-o", "--out", help="directory to write <TICKER>.json into")
    a = ap.parse_args()

    names = [a.ticker] if a.ticker else [t.strip() for t in (a.tickers or "").split(",") if t.strip()]
    if not names:
        sys.exit("give --ticker or --tickers")

    outdir = Path(a.out) if a.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    for t in names:
        doc = build(t, a.date, a.session)
        if outdir:
            (outdir / f"{t.upper()}.json").write_text(
                json.dumps(doc, indent=1) + "\n", encoding="utf-8")
            o = doc.get("options", {})
            print(f"{t.upper():6s} {str(doc.get('status'))[:22]:22s} "
                  f"spot={doc.get('tape', {}).get('spot')} "
                  f"impl={o.get('straddle_implied_move_pct')}% "
                  f"skew={o.get('skew_25d_vol_points')} "
                  f"hist_n={doc.get('history', {}).get('n')} "
                  f"deadband={doc.get('deadband_pct')}")
        else:
            print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    main()
