#!/usr/bin/env python3
"""Disclosed short positioning per European name, from the national registers.

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

The Short Selling Regulation is what stands in its place. Most of these markets publish
name-level net short positions at the 0.5% public threshold, which gives two things the
run-up cannot: how crowded the short side already is, and whether it is being built or
covered into the print.

EIGHT OF TEN READ. Measured 2026-09-19, when the Nordics, Warsaw, Milan and Madrid were
added: UK, DE, FR, SE, DK, NO, FI and IT all download; **ES and PL do not** -- see
UNREACHABLE, and note that both were given the eight-try standard that rescued France
and Italy and failed it. A market with no register produces a lean equal to the free
control, which is a measurement that cannot beat its own benchmark; that is a real cost
of including Spain and Poland and it is carried, not hidden.

FOUR CAN MEASURE THEIR OWN CHANGE and the rest need the cache. The UK (historic file),
France (publication end dates) and Norway (dated events per issuer) carry history;
Germany, Denmark, Finland, Italy and Sweden publish only the current position and are
diffed against yesterday's cached file. `SELF_HISTORIED` and `CACHE_DIFFED` are the
lists, and getting a market into the wrong one either double-counts or leaves
`short_building` null forever.

AND DENMARK IS NOT ON THE SAME SCALE. Finanstilsynet publishes from 0.1% where the SSR
threshold is 0.5%, so a Danish aggregate sums positions no other register shows. It is
deliberately not rescaled: `threshold_pct` rides in the row and eu_resolve.py ranks the
lean components per market.

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

  FR / AMF        **SOLVED ON 2026-09-19, AND THE DIAGNOSIS THAT CLOSED IT WAS WRONG.**
                  Phase 1 recorded www.data.gouv.fr as unreachable: every curl request
                  including the site root died with `Recv failure: Connection reset by
                  peer` and the agent proxy logged `ws_closed_mid_exchange`. Re-tested
                  eighteen times on 2026-09-19, the host answers **intermittently, not
                  never**: `/` returned 200 on 2 of 3 tries, `/api/1/site/` on 4 of 9,
                  and the dataset endpoint on 2 of 6. The tunnel fails at TLS -- 517 B
                  sent, 39 B received, closed after 7s -- so it looks identical to a
                  block and is not one. Four attempts were enough to conclude "blocked"
                  and eight are enough to get the file.

                  So the register comes in two hops, and the second one is the reliable
                  one: retry the dataset endpoint until it answers, read the resource's
                  direct URL out of it, and pull the CSV from
                  `object-api.infra.data.gouv.fr`, which has answered 200 on every
                  request made to it. 5.1 MB, **40,696 per-holder rows back to 2012**,
                  with a position start date, a publication start date and a publication
                  END date -- so it is the AMF's whole history, the analogue of the FCA's
                  per-holder xlsx and better than Bundesanzeiger's current-only snapshot.

                  Two consequences worth stating. The change is **measured, not
                  approximated**: a position is open exactly while its end date is empty,
                  so the aggregate can be reconstructed as of any past date and
                  `short_change_pct_pts` is a real delta over a stated window, which is
                  more than the UK file supports. And it is **backtestable**, like the
                  FCA's and unlike JPX's. What it does not fix is coverage: 74 French
                  issuers carry an open position against 419 UK and 124 German.

ABSENCE IS A ZERO ONLY WHERE THE FILE WAS READ
----------------------------------------------
A name absent from a register that downloaded successfully has no disclosed position at
or above 0.5%, which is information. A name whose register could not be read at all is
not a zero. The two are different objects, `covered` is the field that separates them,
and nothing downstream may treat them alike. Since 2026-09-19 all three registers
normally read, so the second case is a transient rather than a market -- and a register
that fails today but was read within five days is used from the cache with
`stale_cache_days` set, which is a third state and is labelled as one.

THE TRUNCATED ZERO IS NOT AN ANCHOR, AND THE TURNOVER FLOOR MADE THAT MATTER
-----------------------------------------------------------------------------
The floor dropped from $1m to $200k on 2026-09-19. On the ten sessions measured that
day the FCA register names 80% of the UK issuers above $1m and 32% of those between
$200k and $1m, so most of what the lower floor buys reads a truncated 0.0 here. That is
a real zero and it is NOT a measurement of this issuer: `eu_priced_in.py` seals
`anchor_covered` (true only where the register names the issuer), pays that state 0.15
of `anchor_quality.direction` where a disclosure earns 0.45, and `eu_resolve.py` reports
the rank correlation split by it.

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
import time
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# Before the sibling import, not after: eu_positioning is imported by eu_priced_in from
# a different working directory, and a bare `import eu_sheet` would raise there.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import eu_sheet                                                       # noqa: E402

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
# The stable resource id. It 302s to the dated object-storage file; the redirect target
# changes every day (the filename carries an export timestamp), so it cannot be
# hard-coded, and this id is the only fixed handle on it.
AMF_RESOURCE = ("https://www.data.gouv.fr/api/1/datasets/r/"
                "c2539d1c-8531-4937-9cba-3bd8e9786cc5")
AMF_DATASET_API = ("https://www.data.gouv.fr/api/1/datasets/historique-des-positions-"
                   "courtes-nettes-sur-actions-rendues-publiques-depuis-le-1er-"
                   "novembre-2012/")
# How far back the French change is measured. Ten calendar days rather than one trading
# day: the register is a disclosure stream, not a daily snapshot, so a holder who has
# not re-filed since Tuesday has not changed position, and a one-day window would read
# almost every name as unchanged.
FR_CHANGE_WINDOW_DAYS = 10
# The same window for every register that carries its own dated history, so the
# `short_change_pct_pts` field means one thing across markets rather than ten.
CHANGE_WINDOW_DAYS = 10

# --- the seven registers added on 2026-09-19 --------------------------------------
# Every URL below was fetched from this container on that date and the result is in the
# comment beside it. Four work outright, one works with a retry, two do not work at all.
SE_ODS = ("https://www.fi.se/sv/vara-register/blankningsregistret/"
          "GetBlankningsregisterAggregat/")            # 609 kB ODS, dated history
DK_PAGE = ("https://www.dfsa.dk/financial-themes/capital-market/"
           "company-announcements/aggregated-net-short-positions")   # inline HTML table
NO_API = "https://ssr.finanstilsynet.no/api/v2/instruments"          # 1.5 MB JSON
FI_API = "https://www.finanssivalvonta.fi/api/shortselling/datatable/current"
FI_REFERER = ("https://www.finanssivalvonta.fi/en/financial-market-participants/"
              "capital-markets/issuers-and-investors/short-positions/"
              "Current-net-short-positions/")
IT_XLSX = ("https://www.consob.it/documents/11973/395154/PncPubbl.xlsx/"
           "fbefe0a2-795b-bad3-9369-beccbeb14f27")     # 746 kB xlsx behind a WAF

# WHAT DOES NOT RESOLVE, AND WHY IT IS RECORDED HERE RATHER THAN DISCOVERED AGAIN.
# Both were given the EIGHT-TRY STANDARD that rescued France and Italy -- this repo has
# twice written a host off as blocked after four attempts and been wrong both times --
# and both failed it, on the same sweep where emarketstorage passed 7 of 8.
UNREACHABLE = {
    "es": ("The CNMV publishes net short positions through an ASP.NET postback "
           "(`/portal/consultas/ee/posicionescortas`) behind a cookie gate. Driven from "
           "here the page returns 8 of 8 HTTP 200 and ZERO table rows and zero ES ISINs, "
           "before and after posting the cookie-consent form with a valid __VIEWSTATE. "
           "Every `Consulta-OIR` / `InformacionRelevante` path returns 403. So a Spanish "
           "name has NO positioning anchor: its lean is the run-up, which is also the "
           "free control it is measured against."),
    "pl": ("The KNF register is a DataTables POST to "
           "`rss.knf.gov.pl/RssOuterView/JSCRIPT`, which answers 302 without a cookie "
           "and 403 with one, on every attempt and with browser headers. This is a HARD "
           "failure, not the intermittent kind: on the same sweep `www.gpw.pl` and "
           "`espi.pap.pl` each scored 0 of 8 while `emarketstorage.com` scored 7 of 8. "
           "So a Polish name has NO positioning anchor."),
}


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


# --- FR ----------------------------------------------------------------------------
def _curl_retry(url, tries=10, timeout=120, follow=True):
    """www.data.gouv.fr answers intermittently from this container. Retry it.

    Phase 1 tried four times, got four connection resets and wrote the host off as
    blocked. It is not blocked: the same requests succeed roughly a third of the time,
    and the failure is a TLS exchange that dies after 7 seconds, which looks exactly
    like a policy block and is not one. Returns b"" when every try fails, so the caller
    reports an uncovered register rather than raising.
    """
    cmd = ["curl", "-sS", "--max-time", str(timeout), "-H", f"User-Agent: {UA}"]
    if follow:
        cmd.append("-L")
    for i in range(tries):
        p = subprocess.run(cmd + [url], capture_output=True)
        if p.returncode == 0 and p.stdout:
            return p.stdout
        # Back off. Hammering the host without a pause was measured at 0 successes in
        # 12 where a 2-4s gap gets one in three; whatever resets the tunnel does not
        # like a tight loop.
        time.sleep(2 + 2 * (i % 3))
    return b""


def _is_amf_csv(raw):
    """The file is served with a UTF-8 BOM, so a byte-exact startswith misses it.

    This cost a run: the fetch worked, the header check did not, and the register was
    reported unreachable with the direct URL printed beside it. Check the header inside
    the first line instead.
    """
    return bool(raw) and b"Detenteur de la position" in raw[:200]


def _fr_rows():
    """The AMF per-holder CSV, by whichever of the two paths answers.

    Path 1 is the stable resource id, followed through its 302. Path 2 asks the dataset
    API for the resource's current direct URL and pulls that from
    `object-api.infra.data.gouv.fr`, which is the host that actually serves the bytes
    and which has not failed a request here. Path 2 exists because path 1 has to get
    the flaky host right on the first hop AND the redirect in one go.
    """
    raw = _curl_retry(AMF_RESOURCE, tries=8, timeout=90)
    if not _is_amf_csv(raw):
        meta = _curl_retry(AMF_DATASET_API, tries=15, timeout=25)
        try:
            res = (json.loads(meta.decode("utf-8", "replace")).get("resources") or [])
            direct = next((r.get("url") for r in res
                           if (r.get("format") or "").lower() == "csv"), None)
        except Exception:
            direct = None
        if not direct:
            return None, "the data.gouv.fr dataset endpoint did not answer in 15 tries"
        raw = _curl_retry(direct, tries=4, timeout=180)
        if not _is_amf_csv(raw):
            return None, (f"resource URL {direct} did not deliver the CSV "
                          f"({len(raw)} bytes, starts {raw[:40]!r})")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig", "replace")),
                               delimiter=";"))
    return (rows, None) if rows else (None, "the AMF CSV parsed to zero rows")


def _fr_aggregate(rows, as_of=None):
    """Aggregate disclosed net short per issuer, point in time.

    A row is one holder's declared position with a start date, a publication start date
    and a publication END date that is filled in when the position falls back below the
    0.5% threshold. So a position is open exactly while its end date is empty, and the
    register as of any past date D is: every row published on or before D whose end date
    is empty or after D, taking each holder's most recent such row. That is what makes
    the French change a MEASUREMENT rather than the UK file's best effort.
    """
    cur = defaultdict(dict)
    for r in rows:
        end = (r.get("Date de fin de publication position") or "").strip()
        pub = (r.get("Date de debut de publication position") or "").strip()
        start = (r.get("Date de debut position") or "").strip()
        if as_of is not None:
            if pub and pub > as_of:
                continue
            if end and end <= as_of:
                continue
        elif end:
            continue
        try:
            pct = float(str(r.get("Ratio")).replace(",", "."))
        except (TypeError, ValueError):
            continue
        k = norm(r.get("Emetteur / issuer"))
        h = r.get("Detenteur de la position courte nette") or ""
        prev = cur[k].get(h)
        if prev is None or start > prev[0]:
            cur[k][h] = (start, pct, r.get("code ISIN"),
                         r.get("Emetteur / issuer"))
    return {k: {"pct": round(sum(v[1] for v in hs.values()), 4),
                "sellers": len(hs),
                "isin": next(iter(hs.values()))[2],
                "name": next(iter(hs.values()))[3],
                "date": max(v[0] for v in hs.values())}
            for k, hs in cur.items() if hs}


def load_fr():
    rows, err = _fr_rows()
    if rows is None:
        raise RuntimeError(err)
    now = _fr_aggregate(rows)
    then_day = (datetime.utcnow().date()
                - timedelta(days=FR_CHANGE_WINDOW_DAYS)).isoformat()
    then = _fr_aggregate(rows, as_of=then_day)
    out = {}
    for k, v in now.items():
        prev = then.get(k)
        out[k] = {
            "short_ratio_pct": v["pct"],
            "short_ratio_prev_pct": prev["pct"] if prev else 0.0,
            "short_change_pct_pts": round(v["pct"] - (prev["pct"] if prev else 0.0), 4),
            "change_window_days": FR_CHANGE_WINDOW_DAYS,
            "change_reference_date": then_day,
            "disclosed_sellers": v["sellers"],
            "isin": v["isin"],
            "position_date": v["date"],
            "issuer_as_published": v["name"],
        }
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


# --- SE ----------------------------------------------------------------------------
def _num(x):
    """A register percentage, however its locale writes it. `7,99` and `7.99` both."""
    try:
        return float(str(x).strip().replace("\u00a0", "").replace(" ", "").replace(",", "."))
    except (TypeError, ValueError):
        return None


def load_se():
    """Finansinspektionen's aggregated register: a SNAPSHOT, one row per issuer.

    THIS WAS READ WRONG ONCE AND THE CORRECTION IS THE REASON FOR THIS PARAGRAPH. The
    sheet is 1,784 rows, of which all but 342 are blank padding, and the 342 real rows
    are 342 DISTINCT issuers -- one each. It looked like a dated history because the
    position dates span 2019-12-19 to 2026-09-18 across 96 distinct values, but that
    spread is not history: `Positionsdatum senaste position` is the date THIS issuer's
    aggregate last changed, so a name nobody has traded against since 2019 carries a
    2019 date. Read as a history it produced a `short_change_pct_pts` equal to the full
    level for every one of the 342 names, because no row was ever older than the
    reference date.

    So Sweden is snapshot-only, like Germany, Denmark, Finland and Italy, and its change
    is a cache diff. What the date field does buy, which no other snapshot register
    gives, is STALENESS: `position_date` says how long this level has stood, and a
    disclosed short unchanged since 2019 is a different object from one that moved
    yesterday. It rides in the row as `position_date` and is worth reading before a
    negative finding.
    """
    raw = _curl_retry(SE_ODS, tries=4, timeout=120)
    if not raw:
        raise RuntimeError("Finansinspektionen's ODS did not download in 4 tries")
    rows = eu_sheet.read(raw)
    hdr = next((i for i, r in enumerate(rows)
                if r and "emittent" in (r[0] or "").lower()), None)
    if hdr is None:
        raise RuntimeError("the Swedish ODS has no issuer header row; layout changed")
    hist = defaultdict(list)                     # issuer -> [(date, pct, lei, name)]
    # Keyed by issuer so a duplicate row cannot silently become two issuers, and so the
    # `max` below is well defined if the file's shape ever changes.
    for r in rows[hdr + 1:]:
        if len(r) < 4 or not (r[0] or "").strip():
            continue
        pct, d = _num(r[2]), (r[3] or "").strip()[:10]
        if pct is None or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            continue
        hist[norm(r[0])].append((d, pct, (r[1] or "").strip(), r[0].strip()))
    out = {}
    for k, evs in hist.items():
        # One row per issuer in practice; `max` rather than `[0]` so a future file that
        # did carry several rows would take the newest instead of an arbitrary one.
        d, pct, lei, name = max(evs)
        out[k] = {"short_ratio_pct": round(pct, 4),
                  # Null, never 0: this file cannot say what the level was last week,
                  # and 0 would read as "unchanged". Filled from the cache from the
                  # second day on, like the other three snapshot registers.
                  "short_ratio_prev_pct": None,
                  "short_change_pct_pts": None,
                  "disclosed_sellers": None,     # the file is aggregated, not per holder
                  "isin": None, "lei": lei,
                  "position_date": d, "issuer_as_published": name}
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


# --- DK ----------------------------------------------------------------------------
_DK_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_DK_CELL = re.compile(r"<td[^>]*>(.*?)</td>", re.S)


def load_dk():
    """Finanstilsynet's aggregated table, parsed out of the page itself.

    The only one of the ten served as HTML rather than as a file, and the only one whose
    PUBLICATION THRESHOLD IS 0.1% rather than the SSR's 0.5% -- the rows run down to
    0.10 when measured. So a Danish zero is a stronger statement than a British one: it
    rules out five times less short interest. `threshold_pct` rides in every row so
    nothing downstream compares a Danish zero with a Swedish one as if they were the
    same object.

    Current position only, so the change is a cache diff, as for Germany.
    """
    html = _curl([DK_PAGE], timeout=60).decode("utf-8", "replace")
    out = {}
    for r in _DK_ROW.findall(html):
        cells = [re.sub(r"<[^>]+>", "", c).replace("&nbsp;", " ").strip()
                 for c in _DK_CELL.findall(r)]
        if len(cells) < 4 or not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", cells[1] or ""):
            continue
        pct = _num(cells[3])
        if pct is None:
            continue
        out[norm(cells[2])] = {
            "short_ratio_pct": round(pct, 4),
            "short_ratio_prev_pct": None, "short_change_pct_pts": None,
            "disclosed_sellers": None, "isin": cells[1],
            "threshold_pct": 0.1,
            "position_date": (cells[4][:10] if len(cells) > 4 else ""),
            "issuer_as_published": cells[2]}
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


# --- NO ----------------------------------------------------------------------------
def load_no():
    """The Norwegian SSR register: the cleanest of the ten.

    One JSON document, no key and no cookie, carrying every issuer that has ever had a
    disclosed position together with its FULL DATED EVENT HISTORY -- each event an
    aggregate percentage plus the per-holder positions behind it. So the current level
    and the change over any window are both exact, and the anchor is backtestable, like
    the FCA's and the AMF's and unlike Bundesanzeiger's.

    An event with `shortPercent` 0 is a real close-out, not a gap, so a name whose latest
    event is 0 has a disclosed history and no current position. That is deliberately
    kept as a row rather than dropped: it is the one state that distinguishes "shorts
    were here and have gone" from "nobody has ever been short", and the second is what a
    name absent from the register means.
    """
    raw = _curl_retry(NO_API, tries=4, timeout=120)
    if not raw:
        raise RuntimeError("the Norwegian SSR API did not answer in 4 tries")
    data = json.loads(raw.decode("utf-8", "replace"))
    ref = (datetime.utcnow().date() - timedelta(days=CHANGE_WINDOW_DAYS)).isoformat()
    out = {}
    for it in data:
        evs = sorted((e for e in (it.get("events") or []) if e.get("date")),
                     key=lambda e: e["date"])
        if not evs:
            continue
        last = evs[-1]
        prev = next((e for e in reversed(evs) if e["date"][:10] <= ref), None)
        pct = float(last.get("shortPercent") or 0.0)
        pv = float(prev.get("shortPercent") or 0.0) if prev else 0.0
        out[norm(it.get("issuerName"))] = {
            "short_ratio_pct": round(pct, 4),
            "short_ratio_prev_pct": round(pv, 4),
            "short_change_pct_pts": round(pct - pv, 4),
            "change_window_days": CHANGE_WINDOW_DAYS,
            "change_reference_date": ref,
            "disclosed_sellers": len(last.get("activePositions") or []),
            "isin": it.get("isin"),
            "position_date": last["date"][:10],
            "issuer_as_published": it.get("issuerName")}
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


# --- FI ----------------------------------------------------------------------------
def load_fi():
    """FIN-FSA's current register, through the DataTables endpoint its own page calls.

    A POST, not a GET, and the GET returns a 404 page that looks exactly like a dead
    URL -- which is why the endpoint is recorded here with the form body that works
    rather than left to be rediscovered. Per-holder rows, so the aggregate is a sum and
    `disclosed_sellers` is real. Current positions only; the change is a cache diff.
    """
    body = ("draw=1&start=0&length=1000&lang=en"
            "&search%5Bvalue%5D=&search%5Bregex%5D=false")
    raw = _curl(["-X", "POST", "--data", body,
                 "-H", "X-Requested-With: XMLHttpRequest",
                 "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
                 FI_API], referer=FI_REFERER, timeout=60)
    data = json.loads(raw.decode("utf-8", "replace"))
    agg = defaultdict(lambda: {"pct": 0.0, "sellers": 0, "isin": None, "name": None,
                               "date": ""})
    for r in data.get("data") or []:
        pct = _num(r.get("netShortPositionInPercent"))
        if pct is None:
            continue
        a = agg[norm(r.get("issuerName"))]
        a["pct"] += pct
        a["sellers"] += 1
        a["isin"] = a["isin"] or r.get("isinCode")
        a["name"] = a["name"] or r.get("issuerName")
        a["date"] = max(a["date"], (r.get("positionDate") or "")[:10])
    out = {k: {"short_ratio_pct": round(v["pct"], 4),
               "short_ratio_prev_pct": None, "short_change_pct_pts": None,
               "disclosed_sellers": v["sellers"], "isin": v["isin"],
               "position_date": v["date"], "issuer_as_published": v["name"]}
           for k, v in agg.items()}
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


# --- IT ----------------------------------------------------------------------------
def _excel_date(v):
    """CONSOB writes the position date as an Excel serial, so 46259 is 2026-08-25.

    Left as a number it sorts and compares as a number, which reads as a plausible date
    to nothing and silently breaks `as_of`. The epoch is 1899-12-30, which is Excel's
    own off-by-one for 1900 and is correct for every date this register carries.
    """
    try:
        n = float(str(v).strip().replace(",", "."))
    except (TypeError, ValueError):
        return (str(v) or "")[:10]
    if n < 20000 or n > 80000:
        return (str(v) or "")[:10]
    return (datetime(1899, 12, 30) + timedelta(days=int(n))).date().isoformat()


def load_it():
    """CONSOB's per-holder register, from an xlsx behind an intermittent WAF.

    Measured 2026-09-19: the short-selling landing page served the real document on 2 of
    5 tries and a Radware captcha page on the other 3, and the xlsx itself came on the
    second attempt. Retried, not believed on one failure -- the France lesson.

    The download URL is not guessable. It is built by a `downloadShortselling()` function
    inlined in the landing page, and the filename is `PncPubbl.xlsx` with two Ls, which
    is why the obvious `PncPubb.xlsx` returns 404 and looks like a dead register.
    """
    raw = _curl_retry(IT_XLSX, tries=8, timeout=120)
    if not raw or raw[:2] != b"PK":
        raise RuntimeError("CONSOB's PncPubbl.xlsx did not download in 8 tries "
                           "(the WAF serves a captcha page instead)")
    rows = eu_sheet.read(raw)
    agg = defaultdict(lambda: {"pct": 0.0, "sellers": 0, "isin": None, "name": None,
                               "date": ""})
    for r in rows:
        # Two header rows, Italian then English, then the data. Keyed off a real ISIN in
        # column 5 rather than off a row index, so an added preamble row cannot shift it.
        if len(r) < 7 or not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", (r[4] or "").strip()):
            continue
        pct = _num(r[5])
        if pct is None:
            continue
        a = agg[norm(r[2])]
        a["pct"] += pct
        a["sellers"] += 1
        a["isin"] = a["isin"] or r[4].strip()
        a["name"] = a["name"] or r[2].strip()
        a["date"] = max(a["date"], _excel_date(r[6]))
    out = {k: {"short_ratio_pct": round(v["pct"], 4),
               "short_ratio_prev_pct": None, "short_change_pct_pts": None,
               "disclosed_sellers": v["sellers"], "isin": v["isin"],
               "position_date": v["date"], "issuer_as_published": v["name"]}
           for k, v in agg.items()}
    dates = [v["position_date"] for v in out.values() if v["position_date"]]
    return (max(dates) if dates else None), out


# Which markets publish their own dated history, and which need two days of cache before
# `short_change_pct_pts` is anything but null. Getting this wrong in either direction is
# expensive: a cache diff applied to a file that already carries history double-counts,
# and a missing diff leaves the `short_building` lean component null forever.
SELF_HISTORIED = {"uk", "fr", "no"}
CACHE_DIFFED = {"de", "dk", "fi", "it", "se"}
LOADERS = {"uk": load_uk, "de": load_de, "fr": load_fr, "se": load_se,
           "dk": load_dk, "no": load_no, "fi": load_fi, "it": load_it}
SOURCES = {"uk": FCA_CURRENT, "de": BANZ_CSV, "fr": AMF_RESOURCE, "se": SE_ODS,
           "dk": DK_PAGE, "no": NO_API, "fi": FI_API, "it": IT_XLSX,
           "es": None, "pl": None}


def load(markets=("uk", "de", "fr", "se", "dk", "no", "fi", "it", "es", "pl"),
         refresh=False):
    """Every register once for the whole day, cached.

    Cached because four of the eight readable registers publish only the current
    snapshot -- Germany, Denmark, Finland and Italy -- so once a day's file is replaced
    it cannot be re-fetched, and the cache is the only way `short_change_pct_pts` ever
    becomes computable for them. The other four carry their own dated history and are
    never diffed against the cache; see SELF_HISTORIED.

    Spain and Poland have no reachable register at all and short-circuit here rather
    than being attempted, retried and timed out on every run. That is not a judgement
    about those markets, it is the measurement in UNREACHABLE, and it is re-testable:
    delete the entry and add a loader when one of them starts answering.
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
        # TODAY'S FILE IS ALREADY ON DISK: USE IT. Without this the stage re-fetches
        # every register on every invocation, which for France means up to 27 retries
        # against an intermittent host -- measured at twelve minutes before a single
        # baseline was sealed. A register is published once a day; re-reading it twice
        # in one session cannot say anything new. `--refresh` forces the fetch.
        cached_today = (cache.get(m) or {}).get(today)
        if cached_today and not refresh:
            dates = [v.get("position_date") for v in cached_today.values()
                     if v.get("position_date")]
            out[m] = {"as_of": max(dates) if dates else None, "rows": cached_today,
                      "covered": True, "error": None, "stale_cache_days": 0,
                      "from_cache": True, "source": SOURCES.get(m)}
            continue
        if m in UNREACHABLE:
            out[m] = {"as_of": None, "rows": {}, "covered": False, "error": None,
                      "stale_cache_days": None, "source": None,
                      "reason": UNREACHABLE[m]}
            continue
        loader = LOADERS[m]
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
            if m in CACHE_DIFFED and prev_day:   # the four snapshot-only registers
                for k, v in rows.items():
                    p = snap[prev_day].get(k)
                    if p and p.get("short_ratio_pct") is not None:
                        v["short_ratio_prev_pct"] = p["short_ratio_pct"]
                        v["short_change_pct_pts"] = round(
                            v["short_ratio_pct"] - p["short_ratio_pct"], 4)
            snap[today] = rows
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        stale = None
        if not rows:
            # A register that failed TODAY but was read within the last few days is
            # better than nothing AND worse than a fresh read, so it is used and
            # labelled. Disclosure registers move slowly -- a French holder who has not
            # re-filed since Tuesday has not changed position -- but `stale` and
            # `cache_age_days` ride in every name's positioning block so no reader
            # mistakes a five-day-old file for today's. Five days is the limit; beyond
            # it the register is simply uncovered.
            snap = (cache.get(m) or {})
            prev_day = max(snap, default=None)
            if prev_day:
                age = (datetime.fromisoformat(today).date()
                       - datetime.fromisoformat(prev_day).date()).days
                if age <= 5 and snap[prev_day]:
                    rows, as_of, stale = snap[prev_day], prev_day, age
        out[m] = {"as_of": as_of, "rows": rows, "covered": bool(rows), "error": err,
                  "stale_cache_days": stale, "source": SOURCES.get(m)}
        if m == "fr" and not rows:
            out[m]["reason"] = (
                "The AMF register is hosted on www.data.gouv.fr, which answers this "
                "container INTERMITTENTLY -- roughly one request in three, the rest "
                "dying in the TLS exchange (`ws_closed_mid_exchange`). It is retried "
                "up to eighteen times across two paths and this run got nothing. That "
                "is a transient, not a market with no short sellers: re-run before "
                "concluding anything. " + (f"Last error: {err}" if err else ""))
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
    out["stale_cache_days"] = reg.get("stale_cache_days")
    out.update({"covered": True, "as_of": reg.get("as_of"), "source": src,
                "basis": "sum of disclosed net short positions at or above 0.5% of "
                         "shares outstanding, as published by the national regulator"})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--markets", default="uk,de,fr,se,dk,no,fi,it,es,pl")
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
