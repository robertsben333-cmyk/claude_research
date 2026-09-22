#!/usr/bin/env python3
"""Reproduce every number in researcher_canada/SOURCES.md.

Five measurements, all against the live web, none of them cached:

  1. UNIVERSE      -- TradingView's Canada scanner, turnover in USD, the $200k floor
                      stages E, J and EU all screen on, and the forward 60 days.
  2. ANCHORS       -- what fraction of that universe carries a listed option chain
                      (Montreal Exchange) and a short-interest reading (TMX), by
                      turnover band. The band split is the whole point: an anchor that
                      only covers the names the thesis says are already well read is
                      not an anchor for this stage.
  3. CALENDAR      -- Wall Street Horizon coverage, its CONFIRMED / UNCONFIRMED split,
                      and how often it disagrees with the vendor calendar.
  4. CONFIRMATION  -- the phantom test. Take the vendor's LAST release date for names
                      that reported in the past 45 days and ask the two archives whether
                      anything happened: a same-day results release on the wire, or a
                      financial-statement filing on SEDAR+ within three days. This is
                      the same test the UK leg ran against Investegate (2.2% phantom)
                      and the US one against EDGAR (20 of 20 phantom).
  5. RELIABILITY   -- eight tries per host with a 2-4s backoff, including a retest of
                      sedarplus.ca and ciro.ca, because the France leg was written off
                      on four resets against a host that answers one request in three.

Usage:  python3 researcher_canada/scripts/ca_measure.py [--sample N] [--quick]
"""
import argparse
import json
import random
import re
import statistics as st
import subprocess
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_sources as ca  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "researcher_canada" / "analysis" / "ca-source-measurement.json"
TV = "https://scanner.tradingview.com/canada/scan"
TV_COLUMNS = ["name", "description", "close", "currency", "market_cap_basic",
              "average_volume_10d_calc", "earnings_release_date",
              "earnings_release_time", "earnings_release_next_date",
              "earnings_release_next_time", "exchange", "sector"]
SESSION_FLAG = {-1: "bmo", 1: "amc", 0: None}
FLOOR_USD = 200_000
BANDS = ["0.2-1m", "1-5m", "5-25m", ">25m"]
RESULTS_RE = re.compile(
    r"\b(results?|résultats?|earnings|financial|fiscal|quarter|Q[1-4]|annual|interim|reports?)\b",
    re.I)
FIN_FILING_RE = re.compile(
    r"financial statement|interim|annual report|MD&A|management.s discussion|52-109|results",
    re.I)


def band(t):
    if t is None:
        return "n/a"
    return ("<0.2m" if t < 0.2e6 else "0.2-1m" if t < 1e6 else
            "1-5m" if t < 5e6 else "5-25m" if t < 25e6 else ">25m")


def fx_cadusd():
    """Live, never a constant, for the reason eu_universe.py gives: the floor is the
    only non-random selection the stage makes, so the number it is applied against has
    to be reproducible from the file."""
    for i in range(6):
        p = subprocess.run(
            ["curl", "-sS", "--max-time", "25", "-H", f"User-Agent: {ca.UA}",
             "https://query1.finance.yahoo.com/v8/finance/chart/CADUSD=X"
             "?range=5d&interval=1d"], capture_output=True)
        try:
            d = json.loads(p.stdout)
            c = [x for x in d["chart"]["result"][0]["indicators"]["quote"][0]["close"] if x]
            return round(c[-1], 5)
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def scan():
    body = {"filter": [{"left": "is_primary", "operation": "equal", "right": True},
                       {"left": "type", "operation": "equal", "right": "stock"}],
            "options": {"lang": "en"}, "columns": TV_COLUMNS,
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
            "range": [0, 8000]}
    p = subprocess.run(["curl", "-sSL", "--max-time", "90", "-H", f"User-Agent: {ca.UA}",
                        "-X", "POST", "-H", "Content-Type: application/json",
                        "--data-binary", "@-", TV],
                       input=json.dumps(body).encode(), capture_output=True)
    d = json.loads(p.stdout)
    return [dict(zip(TV_COLUMNS, x["d"]), tv_symbol=x["s"]) for x in d.get("data", [])]


def by_band(rows, pred):
    out = {}
    for b in BANDS:
        s = [r for r in rows if r["band"] == b]
        if s:
            k = sum(1 for r in s if pred(r))
            out[b] = {"n": len(s), "covered": k, "pct": round(100 * k / len(s))}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=140,
                    help="past-event sample for the confirmation test")
    ap.add_argument("--chains", type=int, default=26,
                    help="option chains to fetch (SERIAL, ~3s each)")
    ap.add_argument("--quick", action="store_true", help="skip the reliability battery")
    a = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    res = {"measured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "floor_usd": FLOOR_USD}

    # 1 -- universe -----------------------------------------------------------------
    fx = fx_cadusd()
    # A SILENT FALLBACK IS THE THING THIS REPO KEEPS PAYING FOR. Yahoo answered 429 on
    # all six tries during the 2026-09-22 run, so the floor was applied at a constant.
    # That is carried in the output rather than left to be inferred from a null.
    res["cadusd"] = fx
    res["fx_source"] = ("query1.finance.yahoo.com CADUSD=X" if fx
                        else "FALLBACK CONSTANT 0.71 -- yahoo did not answer")
    rows = scan()
    res["universe"] = {"scanner_rows": len(rows),
                       "exchanges": dict(Counter(r["exchange"] for r in rows))}
    opt = set(ca.optionable())
    res["optionable_underlyings"] = len(opt)

    fwd = []
    for r in rows:
        ts = r.get("earnings_release_next_date")
        if not ts:
            continue
        d = datetime.fromtimestamp(ts, timezone.utc).date()
        if not (today <= d <= today + timedelta(days=60)):
            continue
        px, vol = r.get("close"), r.get("average_volume_10d_calc")
        t = px * vol * (fx or 0.71) if (px and vol) else None
        if not t or t < FLOOR_USD:
            continue
        sym = r["tv_symbol"].split(":")[-1]
        fwd.append({"sym": sym, "date": d.isoformat(), "turnover_usd": t,
                    "band": band(t), "exchange": r["exchange"], "close": px,
                    "tv_session": SESSION_FLAG.get(r.get("earnings_release_next_time")),
                    "optionable": sym in opt or sym.split(".")[0] in opt})
    res["eligible_next_60d"] = len(fwd)
    print(f"universe {len(rows)} rows | optionable {len(opt)} | "
          f"eligible >=${FLOOR_USD:,}/day over 60d: {len(fwd)}")

    # 2/3 -- anchors and calendar -----------------------------------------------------
    def probe(r):
        try:
            si = ca.short_interest(r["sym"])
        except Exception:
            si = None
        try:
            ev = ca.earnings_event(r["sym"], today.isoformat())
        except Exception:
            ev = []
        return {**r, "si": si, "wsh": ev[0] if ev else None}

    with ThreadPoolExecutor(max_workers=8) as ex:
        probed = list(ex.map(probe, fwd))

    has_si = lambda r: bool(r["si"] and r["si"].get("SHORT_INTEREST") is not None)
    has_wsh = lambda r: bool(r["wsh"])
    res["coverage"] = {
        "short_interest": {"all": round(100 * sum(map(has_si, probed)) / len(probed)),
                           "by_band": by_band(probed, has_si)},
        "option_chain": {"all": round(100 * sum(1 for r in probed if r["optionable"]) / len(probed)),
                         "by_band": by_band(probed, lambda r: r["optionable"])},
        "wsh_calendar": {"all": round(100 * sum(map(has_wsh, probed)) / len(probed)),
                         "by_band": by_band(probed, has_wsh)},
    }
    sid = Counter(r["si"]["BUSINESS_DATE"] for r in probed if has_si(r))
    res["short_interest_business_dates"] = dict(sid.most_common(5))
    w = [r for r in probed if r["wsh"]]
    res["calendar"] = {
        "wsh_rows": len(w),
        "confirmed": sum(1 for r in w if r["wsh"]["confirmed"]),
        "session_encoded": sum(1 for r in w if r["wsh"]["session"]),
        "agrees_with_vendor_date": sum(1 for r in w if r["wsh"]["date"] == r["date"]),
        "sample_disagreements": [[r["sym"], r["date"], r["wsh"]["date"]] for r in w
                                 if r["wsh"]["date"] != r["date"]][:10],
    }
    print("coverage:", json.dumps(res["coverage"], indent=None))

    # 4 -- confirmation ---------------------------------------------------------------
    past = []
    for r in rows:
        ts = r.get("earnings_release_date")
        if not ts:
            continue
        d = datetime.fromtimestamp(ts, timezone.utc).date()
        if not (today - timedelta(days=45) <= d < today):
            continue
        px, vol = r.get("close"), r.get("average_volume_10d_calc")
        t = px * vol * (fx or 0.71) if (px and vol) else None
        if not t or t < FLOOR_USD:
            continue
        past.append({"sym": r["tv_symbol"].split(":")[-1], "date": d.isoformat(),
                     "band": band(t),
                     "tv_session": SESSION_FLAG.get(r.get("earnings_release_time"))})
    random.seed(20260922)
    random.shuffle(past)
    sample = past[:a.sample]

    def confirm(c):
        try:
            n = ca.news(c["sym"], limit=60)
        except Exception:
            n = []
        oldest = n[-1]["datetime"][:10] if n else None
        same = [x for x in n if (x.get("datetime") or "")[:10] == c["date"]]
        hit = [x for x in same if RESULTS_RE.search(x.get("headline", ""))]
        out = {**c, "archive_reaches": bool(oldest and oldest <= c["date"]),
               "same_day_release": len(same), "results_headline": len(hit),
               "release_ts": (hit or same)[0]["datetime"] if (hit or same) else None}
        if not same:                       # second route: the filing itself
            d0 = (date.fromisoformat(c["date"]) - timedelta(days=3)).isoformat()
            d1 = (date.fromisoformat(c["date"]) + timedelta(days=3)).isoformat()
            try:
                f = ca.filings(c["sym"], d0, d1, 40)
            except Exception:
                f = []
            out["financial_filing"] = sum(
                1 for x in f
                if FIN_FILING_RE.search((x.get("description") or "") + " " + (x.get("name") or "")))
        else:
            out["financial_filing"] = None
        return out

    with ThreadPoolExecutor(max_workers=8) as ex:
        conf = list(ex.map(confirm, sample))
    reach = [r for r in conf if r["archive_reaches"]]
    wire = [r for r in reach if r["results_headline"]]
    anyrel = [r for r in reach if r["same_day_release"]]
    filed = [r for r in reach if not r["same_day_release"] and r["financial_filing"]]
    res["confirmation"] = {
        "sample": len(conf), "archive_reaches_event_date": len(reach),
        "same_day_results_headline": len(wire),
        "any_same_day_release": len(anyrel),
        "no_release_but_financial_filing": len(filed),
        "unconfirmed_by_either": len(reach) - len(anyrel) - len(filed),
        "by_band_wire": by_band(reach, lambda r: bool(r["results_headline"])),
    }

    def sess_of(ts):
        if not ts:
            return None
        h, m = int(ts[11:13]), int(ts[14:16])
        return "bmo" if (h, m) < (9, 30) else "amc" if h >= 16 else "intraday"
    agree = Counter()
    for r in wire:
        if r["tv_session"]:
            agree[f"{r['tv_session']}->{sess_of(r['release_ts'])}"] += 1
    res["confirmation"]["vendor_session_vs_release_timestamp"] = dict(agree)
    print("confirmation:", json.dumps(res["confirmation"], indent=None))

    # option chains (serial) ---------------------------------------------------------
    # Sample the chains ACROSS the bands. The scanner sorts by market cap, so taking the
    # first N optionable names measures the option chain on mega-caps only and says
    # nothing about the band this stage is for.
    optnames = [r for r in probed if r["optionable"]]
    random.seed(20260922)
    random.shuffle(optnames)
    chains = optnames[:a.chains]
    got = []
    for r in chains:
        try:
            im = ca.implied_move_pct(r["sym"], r["date"], r["close"])
        except Exception:
            im = None
        if im:
            got.append({**im, "sym": r["sym"], "band": r["band"]})
        time.sleep(0.5)
    res["option_chain_sample"] = {
        "tried": len(chains), "priced": len(got),
        "priced_off_quote": sum(1 for g in got if g["priced_off"] == "quote"),
        "atm_open_interest_nonzero": sum(1 for g in got if g["atm_open_interest"]),
        "median_implied_move_pct": round(st.median([g["implied_move_pct"] for g in got]), 2) if got else None,
        "median_days_past_event": st.median([g["days_past_event"] for g in got]) if got else None,
        "rows": got[:15],
    }
    print("option chains:", res["option_chain_sample"]["priced"], "of",
          res["option_chain_sample"]["tried"], "priced")

    # 5 -- reliability -----------------------------------------------------------------
    if not a.quick:
        tests = [
            ("app-money.tmx.com/graphql",
             ["-X", "POST", "-H", "Content-Type: application/json", "--data-binary",
              '{"query":"query($s:String){getQuoteBySymbol(symbol:$s){symbol price}}",'
              '"variables":{"s":"AEM"}}', ca.GQL], 40),
            ("www.m-x.ca (chain)", [f"{ca.MX}/quotes?symbol=AEM*"], 5000),
            ("scanner.tradingview.com",
             ["-X", "POST", "-H", "Content-Type: application/json", "--data-binary",
              '{"filter":[{"left":"type","operation":"equal","right":"stock"}],'
              '"columns":["name"],"range":[0,5]}', TV], 40),
            ("www.sedarplus.ca", ["https://www.sedarplus.ca/"], 1000),
            ("www.ciro.ca", ["https://www.ciro.ca/"], 1000),
            ("www.sedi.ca", ["https://www.sedi.ca/"], 1000),
        ]
        rel = {}
        for name, args, minbytes in tests:
            ok, codes = 0, []
            for i in range(8):
                p = subprocess.run(["curl", "-sS", "-o", "/dev/null",
                                    "-w", "%{http_code} %{size_download}",
                                    "--max-time", "40", "-H", f"User-Agent: {ca.UA}"] + args,
                                   capture_output=True)
                t = p.stdout.decode().split()
                code = t[0] if t else "ERR"
                size = int(t[1]) if len(t) > 1 else 0
                codes.append(code)
                ok += 1 if (code == "200" and size >= minbytes) else 0
                time.sleep(2 if i < 2 else 3)
            rel[name] = {"ok_of_8": ok, "codes": codes}
            print(f"  {name:<30}{ok}/8")
        res["reliability"] = rel

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))
    print("wrote", OUT.relative_to(REPO))


if __name__ == "__main__":
    main()
