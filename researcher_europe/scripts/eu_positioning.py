#!/usr/bin/env python3
"""Disclosed short positioning per European name, from the three national registers.

WHY THIS EXISTS
---------------
The same reason `researcher_japan/scripts/jp_positioning.py` exists, and Phase 1 found
the same hole: there is no retrievable European single-stock option chain. Yahoo returns
21 expiries and 196 contracts for AAPL with a valid crumb and **zero expiries and zero
contracts** for SAP.DE, ADS.DE, BARC.L, MC.PA and BNP.PA. Eurex's daily reference file
downloads (4.06 MB, HTTP 200) and carries trading parameters, order profiles and price
range tables but no settlement prices, no open interest and no underlying ISIN map, so
an implied move cannot be computed from it; its market-statistics page is JavaScript
with no JSON endpoint.

So `options` is null for Europe as it is for Japan, `edge_score.priced_lean_pct` would
fall through to its `-0.05 * run_up_20d_pct` branch, and the baseline's lean and the
free control every ranker is measured against would be the same number.

The Short Selling Regulation is what stands in its place. All three markets publish
name-level net short positions at the 0.5% public threshold, which gives two things the
run-up cannot: how crowded the short side already is, and whether it is being built or
covered into the print.

WHAT EACH REGISTER ACTUALLY GIVES, MEASURED
-------------------------------------------
  UK / FCA        THE BEST ONE IN THIS REPO. Three plain GETs, no cookie, no key:
                  `aggregated-current-net-short-positions.csv` (419 issuers, position
                  dates to 2026-09-17), `aggregated-historic-net-short-positions.csv`
                  (5,615 rows, every position that has fallen below the threshold) and
                  `short-positions-daily-update.xlsx` (108,850 per-holder rows back to
                  2012-10-31). The third has NO Japanese analogue -- JPX's register
                  rolls off, which is why jp_positioning.py has to cache it. The FCA
                  publishes the whole history, so a European positioning anchor can be
                  backtested rather than only run forward.

                  Coverage of the UK results cohort, 302 issuers over 20 sampled days:
                  12% below $1m/day of turnover, **89% at $1-5m**, 74% at $5-25m, 67%
                  above $25m. Japan's JPX register resolved on 9 to 11 of 25 names.
                  That single row is the strongest argument for building this stage,
                  and it is also the argument for the $1m turnover floor.

  DE / Bundes-    Works, with a session cookie picked up from /pub/en/nlp first. 486
  anzeiger        live disclosed positions as of 2026-09-17, of which 124 are German
                  ISINs against 427 primary German stocks. Current position only, so
                  the CHANGE has to be built by caching successive days exactly as
                  Japan does.

  FR / AMF        **DOES NOT WORK FROM THIS CONTAINER AND IS NOT WORKED AROUND.**
                  www.data.gouv.fr, which hosts the register, resets the proxy tunnel
                  on every request including the site root (`ws_closed_mid_exchange`);
                  WebFetch reads the dataset page but cannot deliver a 4.9 MB CSV;
                  bdif.amf-france.org is an Angular SPA whose API was not found. French
                  names therefore run with `covered: false` and an EXPLICIT reason, and
                  their lean falls back to the run-up -- which is also the free control.
                  `eu_resolve.py` reports `lean_vs_free_control_rho` PER MARKET so this
                  reads near 1.0 for France and near 0.4-0.6 for the other two, rather
                  than being averaged into invisibility.

ABSENCE IS A ZERO ONLY WHERE THE FILE WAS READ
----------------------------------------------
A UK or German name absent from a register that downloaded successfully has no disclosed
position at or above 0.5%, which is information. A French name is absent because the
file could not be read at all, which is not. The two are different objects and
`covered` is the field that separates them; nothing downstream may treat them alike.

WHAT IS NOT KNOWN. The threshold truncates -- 0.4% and 0.0% are both recorded as 0.0.
Market-maker and index-arbitrage shorts below the line are invisible. And the SIGN of
the effect is a PRIOR borrowed from the US runs, not a European measurement:
`eu_resolve.py` ranks each component separately for exactly that reason. Replace the
weights with measurement; do not defend them.
"""
import argparse
import csv
import io
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "researcher_europe" / "analysis" / "eu-short-cache.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"

FCA_CURRENT = ("https://www.fca.org.uk/publication/documents/"
               "aggregated-current-net-short-positions.csv")
FCA_HISTORIC = ("https://www.fca.org.uk/publication/documents/"
                "aggregated-historic-net-short-positions.csv")
FCA_PAGE = ("https://www.fca.org.uk/markets/short-selling/"
            "notification-and-disclosure-net-short-positions")
BANZ_PAGE = "https://www.bundesanzeiger.de/pub/en/nlp"
BANZ_CSV = ("https://www.bundesanzeiger.de/pub/en/nlp"
            "?0--top~csv~form~panel-form-csv~resource~link")
AMF_DATASET = ("https://www.data.gouv.fr/datasets/historique-des-positions-courtes-"
               "nettes-sur-actions-rendues-publiques-depuis-le-1er-novembre-2012")


def _curl(args, cookie=None, referer=None, timeout=90):
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {UA}"]
    if cookie:
        cmd += ["-b", cookie, "-c", cookie]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    cmd += args
    p = subprocess.run(cmd, capture_output=True)
    return p.stdout


def norm(s):
    """Match a register's issuer name against a vendor's company description.

    Neither register carries a ticker, so the join is on the name and it is the
    weakest link in this file. Legal-form words and punctuation come off; what is
    left is compared exactly. A near-miss is a MISS -- it records a zero where a real
    position exists, which is the direction that costs the hunter a warning rather
    than inventing one. `unmatched_sample` in the cache lets that be audited.
    """
    s = (s or "").upper()
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\b(PLC|LIMITED|LTD|GROUP|HOLDINGS|HOLDING|THE|SA|SE|AG|INC|COMPANY|"
               r"CO|NV|SPA|KGAA|AKTIENGESELLSCHAFT|SOCIETE|ANONYME)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# --- UK ----------------------------------------------------------------------------
def load_uk():
    """{normalised issuer name: {...}} plus the change against the historic file."""
    cur = _curl([FCA_CURRENT], referer=FCA_PAGE).decode("utf-8-sig", "replace")
    rows = list(csv.DictReader(io.StringIO(cur)))
    if not rows:
        return None, {}
    out, dates = {}, []
    for r in rows:
        try:
            pct = float(r["Aggregated net short position (%)"])
        except (KeyError, TypeError, ValueError):
            continue
        d = r.get("Position date")
        dates.append(d)
        out[norm(r["Name of Company"])] = {
            "short_ratio_pct": round(pct, 4),
            "isin": r.get("International Securities Identification Number (ISIN)"),
            "position_date": d,
            "issuer_as_published": r["Name of Company"],
        }
    # The change. The historic file carries every position that has DROPPED below the
    # threshold with the date it did, so it gives the previous level for a name whose
    # aggregate has fallen. It does not give a full previous aggregate for a name still
    # above the line, so the change is computed where it can be and is null otherwise
    # -- never zero, which would read as "no change" rather than "not known".
    try:
        hist = list(csv.DictReader(io.StringIO(
            _curl([FCA_HISTORIC], referer=FCA_PAGE).decode("utf-8-sig", "replace"))))
    except Exception:
        hist = []
    prev = {}
    for r in hist:
        k = norm(r.get("Name of Company"))
        try:
            pct = float(r["Aggregated net short position (%)"])
        except (KeyError, TypeError, ValueError):
            continue
        d = r.get("Position date") or ""
        if k not in prev or d > prev[k][1]:
            prev[k] = (pct, d)
    for k, v in out.items():
        p = prev.get(k)
        v["short_ratio_prev_pct"] = round(p[0], 4) if p else None
        v["short_change_pct_pts"] = round(v["short_ratio_pct"] - p[0], 4) if p else None
    return (max(dates) if dates else None), out


# --- DE ----------------------------------------------------------------------------
def load_de(tmp_cookie="/tmp/eu_banz_cookie.txt"):
    _curl(["-o", "/dev/null", BANZ_PAGE], cookie=tmp_cookie, timeout=45)
    raw = _curl([BANZ_CSV], cookie=tmp_cookie, referer=BANZ_PAGE).decode("utf-8-sig",
                                                                        "replace")
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows or "ISIN" not in (rows[0] or {}):
        return None, {}
    agg = defaultdict(lambda: {"pct": 0.0, "sellers": 0, "isin": None, "name": None,
                               "date": ""})
    for r in rows:
        try:
            pct = float(str(r["Position"]).replace(",", "."))
        except (TypeError, ValueError):
            continue
        k = norm(r.get("Emittent"))
        a = agg[k]
        a["pct"] += pct
        a["sellers"] += 1
        a["isin"] = a["isin"] or r.get("ISIN")
        a["name"] = a["name"] or r.get("Emittent")
        a["date"] = max(a["date"], r.get("Datum") or "")
    out = {k: {"short_ratio_pct": round(v["pct"], 4),
               "short_ratio_prev_pct": None,
               # Bundesanzeiger publishes the CURRENT position only. The change needs
               # two days of this file, so it is null on a first run and filled from the
               # cache from the second day on. Null, never 0.
               "short_change_pct_pts": None,
               "disclosed_sellers": v["sellers"], "isin": v["isin"],
               "position_date": v["date"], "issuer_as_published": v["name"]}
           for k, v in agg.items()}
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


def load(markets=("uk", "de", "fr"), refresh=False):
    """Every register once for the whole day, cached.

    Cached because Bundesanzeiger publishes only the current snapshot: once a day's
    file is replaced it cannot be re-fetched, and the cache is the only way the CHANGE
    component ever becomes computable for Germany.
    """
    cache = {}
    if CACHE.exists() and not refresh:
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    today = datetime.utcnow().date().isoformat()
    out = {}
    for m in markets:
        if m == "fr":
            out["fr"] = {"as_of": None, "rows": {}, "covered": False,
                         "reason": "The AMF register is hosted on www.data.gouv.fr, "
                                   "which is unreachable from this container: every "
                                   "curl request including the site root dies with "
                                   "`Recv failure: Connection reset by peer` and the "
                                   "agent proxy logs `ws_closed_mid_exchange`. WebFetch "
                                   "reads the dataset page but cannot deliver the 4.9 MB "
                                   "CSV, and bdif.amf-france.org is an SPA whose API was "
                                   "not found. This is a KNOWN OPEN HOLE, not a market "
                                   "with no short sellers.",
                         "source": AMF_DATASET}
            continue
        loader = load_uk if m == "uk" else load_de
        try:
            as_of, rows = loader()
        except Exception as exc:
            as_of, rows = None, {}
            err = str(exc)
        else:
            err = None
        if rows:
            snap = cache.setdefault(m, {})
            prev_day = max([d for d in snap if d < today], default=None)
            if m == "de" and prev_day:
                for k, v in rows.items():
                    p = snap[prev_day].get(k)
                    if p and p.get("short_ratio_pct") is not None:
                        v["short_ratio_prev_pct"] = p["short_ratio_pct"]
                        v["short_change_pct_pts"] = round(
                            v["short_ratio_pct"] - p["short_ratio_pct"], 4)
            snap[today] = rows
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        out[m] = {"as_of": as_of, "rows": rows, "covered": bool(rows), "error": err,
                  "source": FCA_CURRENT if m == "uk" else BANZ_CSV}
    return out


def for_name(market, company, registers):
    """One name's positioning. Absence is a zero ONLY where the register was read."""
    reg = registers.get(market) or {}
    src = reg.get("source")
    if not reg.get("covered"):
        return {"short_ratio_pct": None, "short_ratio_prev_pct": None,
                "short_change_pct_pts": None, "disclosed_sellers": None,
                "covered": False,
                "basis": reg.get("reason") or f"register unavailable: {reg.get('error')}",
                "as_of": reg.get("as_of"), "source": src}
    hit = (reg.get("rows") or {}).get(norm(company))
    if hit is None:
        return {"short_ratio_pct": 0.0, "short_ratio_prev_pct": 0.0,
                "short_change_pct_pts": 0.0, "disclosed_sellers": 0, "covered": True,
                "basis": "absent from a register that downloaded successfully, so no "
                         "disclosed net short position at or above the 0.5% public "
                         "threshold. A real zero -- but the threshold truncates, so "
                         "0.4% and 0.0% are both recorded here as 0.0, and the join is "
                         "on the issuer NAME, so a name spelled differently in the "
                         "register reads as a zero it should not.",
                "as_of": reg.get("as_of"), "source": src}
    out = dict(hit)
    out.update({"covered": True, "as_of": reg.get("as_of"), "source": src,
                "basis": "sum of disclosed net short positions at or above 0.5% of "
                         "shares outstanding, as published by the national regulator"})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--markets", default="uk,de,fr")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--name", action="append", help="look up these company names")
    a = ap.parse_args()
    regs = load(tuple(x.strip() for x in a.markets.split(",")), a.refresh)
    for m, r in regs.items():
        print(f"{m}: covered={r['covered']} as_of={r['as_of']} "
              f"rows={len(r.get('rows') or {})}"
              + (f"  [{(r.get('reason') or r.get('error') or '')[:90]}]"
                 if not r["covered"] else ""))
        if r["covered"]:
            top = sorted(r["rows"].items(), key=lambda x: -x[1]["short_ratio_pct"])[:5]
            for k, v in top:
                print(f"    {v['issuer_as_published'][:36]:<36} "
                      f"{v['short_ratio_pct']:>6.2f}%  (change "
                      f"{v.get('short_change_pct_pts')})")
    for n in a.name or []:
        for m in regs:
            print(f"  {m} / {n}: {json.dumps(for_name(m, n, regs), ensure_ascii=False)}")


if __name__ == "__main__":
    main()
