#!/usr/bin/env python3
"""What is still coming for this company, from sources that were measured to answer.

THIS IS THE STAGE'S REAL ANCHOR, AND IT REPLACED A WORSE IDEA
--------------------------------------------------------------
The first version of stage R asked its hunter whether yesterday's fall "overshot the
news". That is backward-looking, unfalsifiable until the outcome, and a language model
handed a 25% fall will rationalise either answer fluently. The question that matters is
forward: **is there more bad news coming for this company that the price does not hold,
or is the bad news finished?** A second shoe is a thing with a date and a document. An
over-reaction is an opinion.

So the baseline carries the forward pipeline, from primary sources, and the hunter
starts from documents rather than from a blank search box.

EVERY SOURCE HERE WAS PROBED ON 2026-09-22 AND ANSWERED
--------------------------------------------------------
| source | what it gives | status |
| --- | --- | --- |
| `data.sec.gov/submissions` | every filing this issuer has made, dated, by form | 200 |
| `efts.sec.gov` full-text search | the TEXT of filings, scoped by CIK, form and date | 200 |
| `www.sec.gov` browse-edgar atom | Form 4 and 8-K feeds | 200 |
| `sec.gov/files/company_tickers.json` | ticker to CIK | 200 |
| `api.nasdaq.com/quote/../short-interest` | 24 dated settlements, level and days to cover | 200 |
| `api.nasdaq.com/company/../insider-trades` | Form 4 summary, 3 and 12 month | 200 |
| `api.nasdaq.com/analyst/../earnings-date` | an ALGORITHMIC estimate, see below | 200 |
| `clinicaltrials.gov/api/v2` | trial status and primary completion dates | 200 |
| `api.fda.gov` | recalls and adverse events | 200 |
| `courtlistener.com/api/rest/v4` | federal dockets | 200, **125 requests/day** |

**CourtListener has a daily quota, and spending it looks like a dead source.** 125
requests a day across the whole session. A hunt that exhausts it gets HTTP 429 with
`Rate limit exceeded: 125/day` and, unless it reads the body, will write the docket check
off as unreachable — which happened on 2026-09-22. Re-probed afterwards it returned 200.
Budget it: one or two queries per name, and a 429 means spent, not blocked.

**NOT reachable, so nothing may depend on them:** Nasdaq's Listing Center rulebook and
notices (403), FTSE Russell's index *notices* page (404), Nasdaq's press-release topic
API (301). An index deletion or a delisting notice therefore has to be found through the
company's own 8-K, which is the only route this container has.

**And FTSE Russell's quarterly IPO-additions PDF is a near miss worth stating precisely,
because the obvious diagnosis is wrong.** `final-ipo-additions-3-qtr-r3000.pdf` downloads
at HTTP 200, 419 KB, and it DOES carry a `/ToUnicode` CMap — the 2026-09-22 hunt reported
that it did not, and re-probing showed otherwise. What fails is this container's reader:
`researcher_europe/scripts/eu_pdftext.py` decompresses the streams but does not apply
CMaps, so on a subset-font document it returns font-table bytes rather than text. So the
issuer-level index membership that would confirm an `index_or_flow` cause still rests on
a secondary aggregator plus the volume signature. **The fix is a CMap-aware decoder, not
another source**, and it is not built; until it is, an index-addition finding says so.

THE EARNINGS DATE IS A CADENCE PRIOR AND IS LABELLED AS ONE
------------------------------------------------------------
Nasdaq serves Zacks's *estimated* next report date, "derived from an algorithm based on a
company's historical reporting dates". This repo has already paid for reading a cadence
prior as evidence: TRT read `fits`, cleared the conviction floor, was the day's only
trade, and never reported. The field is `next_earnings_estimated` with
`is_estimate: true` and the vendor's own disclaimer attached, and no finding may rest on
it alone.

    python3 researcher_reversal/scripts/rev_forward.py --ticker CUE
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_market as M                                            # noqa: E402

# The SEC asks for a contact in the UA and rate-limits without one.
SEC_UA = {"User-Agent": "claude_research/1.0 (robertsben333@gmail.com)",
          "Accept": "application/json,text/html"}
NDQ_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
          "Accept": "application/json"}

SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
FTS = "https://efts.sec.gov/LATEST/search-index?q={q}&ciks={cik:010d}"
FTS_WIN = FTS + "&startdt={start}&enddt={end}"
TICKERS = "https://www.sec.gov/files/company_tickers.json"
SHORT = "https://api.nasdaq.com/api/quote/{t}/short-interest?assetclass=stocks"
INSIDER = "https://api.nasdaq.com/api/company/{t}/insider-trades?limit=15&type=ALL"
EARNDATE = "https://api.nasdaq.com/api/analyst/{t}/earnings-date"
CTGOV = ("https://clinicaltrials.gov/api/v2/studies?query.spons={q}"
         "&filter.overallStatus=RECRUITING,ACTIVE_NOT_RECRUITING,ENROLLING_BY_INVITATION"
         "&pageSize=20&fields=NCTId,BriefTitle,OverallStatus,PrimaryCompletionDate,Phase")

# Phrases whose PRESENCE in this issuer's own filings is a dated, forward-looking fact.
# Each is a thing that can produce more selling after a fall, or rule it out.
PROBES = [
    ("shelf_or_atm", '"at-the-market"',
     "an open ATM sells stock into any bounce and is the commonest second leg down"),
    ("going_concern", '"substantial doubt about its ability to continue"',
     "the auditor's language. It reprices the equity and it recurs each filing"),
    ("covenant", '"covenant"',
     "a covenant the fall may have tripped, or a waiver that has an expiry"),
    ("listing_deficiency", '"minimum bid price"',
     "a Nasdaq or NYSE deficiency clock. Not reachable from the exchange here, so the "
     "issuer's own 8-K is the only route"),
    ("lockup", '"lock-up"',
     "a dated supply release"),
    ("reverse_split", '"reverse stock split"',
     "usually a consequence of the fall rather than a cause, and it has a vote date"),
    ("restatement", '"non-reliance"',
     "Item 4.02. The single most reliable predictor of further falls in the record"),
]
_ticker_map = None


def _get(url, headers, tries=3):
    try:
        return M.get(url, headers=headers, tries=tries)
    except Exception:                                             # noqa: BLE001
        return None


def cik_for(ticker):
    """Ticker to CIK from the SEC's own map. None when the issuer is not an SEC filer."""
    global _ticker_map
    if _ticker_map is None:
        raw = _get(TICKERS, SEC_UA)
        _ticker_map = {}
        if raw:
            try:
                for v in json.loads(raw).values():
                    _ticker_map[v["ticker"].upper()] = int(v["cik_str"])
            except Exception:                                     # noqa: BLE001
                pass
    return _ticker_map.get((ticker or "").upper())


def filings(cik, since_days=400, keep=40):
    """This issuer's recent filings, dated, newest first, with a URL each."""
    raw = _get(SUBMISSIONS.format(cik=cik), SEC_UA)
    if not raw:
        return {"status": "unavailable", "filings": []}
    try:
        d = json.loads(raw)
    except Exception:                                             # noqa: BLE001
        return {"status": "unparseable", "filings": []}
    r = (d.get("filings") or {}).get("recent") or {}
    out = []
    today = date.today()
    for i in range(len(r.get("form", []))):
        fd = r["filingDate"][i]
        try:
            age = (today - date.fromisoformat(fd)).days
        except ValueError:
            continue
        if age > since_days:
            continue
        acc = r["accessionNumber"][i].replace("-", "")
        out.append({
            "form": r["form"][i], "filed": fd, "age_days": age,
            "items": r.get("items", [""] * (i + 1))[i] or None,
            "url": (f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/"
                    f"{r['primaryDocument'][i]}"),
        })
        if len(out) >= keep:
            break
    forms = {}
    for f in out:
        forms.setdefault(f["form"], []).append(f["filed"])
    return {
        "status": "ok",
        "company": d.get("name"),
        "sic": d.get("sic"), "sic_description": d.get("sicDescription"),
        "filings": out,
        "form_counts": {k: len(v) for k, v in sorted(forms.items())},
        "latest_by_form": {k: v[0] for k, v in forms.items()},
        "source": SUBMISSIONS.format(cik=cik),
    }


def text_probes(cik, probes=PROBES, window_days=550):
    """Full-text search of THIS issuer's filings for phrases that carry a forward risk.

    EACH PROBE RUNS TWICE, AND THE SECOND RUN IS THE ONE THAT MATTERS. The API returns
    hits by relevance, not by date, so a single query reports whichever five documents
    the index liked -- on the first test that put Cue's newest ATM language at 2021 while
    three S-3s sat in the last year. The windowed query fixes it by asking the index a
    different question: "in the last eighteen months", where every hit is recent by
    construction. `ever` is kept beside it because "this issuer has never used an ATM" is
    itself worth knowing.

    A hit is a dated document, not a hint: the hunter is expected to open it. A miss is
    also information -- no going-concern language anywhere in a microcap that has just
    fallen 30% rules out the commonest second leg down.
    """
    end = date.today().isoformat()
    start = date.fromordinal(date.today().toordinal() - window_days).isoformat()
    out = {}

    def run(url):
        raw = _get(url, SEC_UA, tries=2)
        time.sleep(0.15)                   # the SEC asks for under 10 requests a second
        if not raw:
            return None, []
        try:
            h = json.loads(raw)["hits"]
        except Exception:                                         # noqa: BLE001
            return None, []
        hits = []
        for x in h.get("hits", [])[:6]:
            src = x.get("_source") or {}
            acc, _, doc = x.get("_id", "").partition(":")
            hits.append({
                "filed": src.get("file_date"),
                "forms": src.get("root_forms"),
                "url": (f"https://www.sec.gov/Archives/edgar/data/{cik}/"
                        f"{acc.replace('-', '')}/{doc}") if acc else None,
            })
        hits.sort(key=lambda z: z.get("filed") or "", reverse=True)
        return (h.get("total") or {}).get("value"), hits

    for key, q, why in probes:
        qq = urllib.parse.quote(q)
        ever_total, _ = run(FTS.format(q=qq, cik=cik))
        win_total, win_hits = run(FTS_WIN.format(q=qq, cik=cik, start=start, end=end))
        out[key] = {
            "status": "ok" if ever_total is not None else "unavailable",
            "phrase": q,
            "hits_ever": ever_total,
            "hits_last_%dd" % window_days: win_total,
            "most_recent": win_hits[0]["filed"] if win_hits else None,
            "recent_hits": win_hits[:4],
            "why_it_matters": why,
        }
    return out


def short_interest(ticker):
    """Dated settlements, so the CHANGE into the fall is measurable and not guessed."""
    raw = _get(SHORT.format(t=ticker), NDQ_UA)
    if not raw:
        return {"status": "unavailable"}
    try:
        t = json.loads(raw)["data"]["shortInterestTable"]
        rows = t["rows"]
    except Exception:                                             # noqa: BLE001
        return {"status": "unavailable"}
    def n(s):
        return M.num(s)
    keep = [{"settlement": r.get("settlementDate"),
             "shares_short": n(r.get("interest")),
             "avg_daily_volume": n(r.get("avgDailyShareVolume")),
             "days_to_cover": n(r.get("daysToCover"))} for r in rows[:8]]
    chg = None
    if len(keep) >= 2 and keep[0]["shares_short"] and keep[1]["shares_short"]:
        chg = round(100 * (keep[0]["shares_short"] / keep[1]["shares_short"] - 1), 1)
    return {
        "status": "ok",
        "latest_settlement": keep[0]["settlement"] if keep else None,
        "shares_short": keep[0]["shares_short"] if keep else None,
        "days_to_cover": keep[0]["days_to_cover"] if keep else None,
        "change_vs_prior_settlement_pct": chg,
        "history": keep,
        "lag_warning": ("FINRA settles twice a month and publishes about eight business "
                        "days later, so the position carried INTO the fall is not yet "
                        "observable. Never describe this as current"),
        "source": SHORT.format(t=ticker),
    }


def insiders(ticker):
    raw = _get(INSIDER.format(t=ticker), NDQ_UA)
    if not raw:
        return {"status": "unavailable"}
    try:
        d = json.loads(raw)["data"]
    except Exception:                                             # noqa: BLE001
        return {"status": "unavailable"}
    rows = (d.get("transactionTable") or {}).get("rows") or []
    return {
        "status": "ok",
        "summary_3m_12m": (d.get("numberOfTrades") or {}).get("rows"),
        "recent": [{"insider": r.get("insider"), "date": r.get("lastDate"),
                    "type": r.get("transactionType"), "shares": r.get("sharesTraded"),
                    "price": r.get("lastPrice")} for r in rows[:8]],
        "source": INSIDER.format(t=ticker),
    }


def next_earnings(ticker):
    """Zacks's ALGORITHMIC estimate. A prior, never a schedule. See the module docstring."""
    raw = _get(EARNDATE.format(t=ticker), NDQ_UA)
    if not raw:
        return {"status": "unavailable", "is_estimate": True}
    try:
        txt = json.loads(raw)["data"].get("reportText") or ""
    except Exception:                                             # noqa: BLE001
        return {"status": "unavailable", "is_estimate": True}
    m = re.search(r"(\d{2}/\d{2}/\d{4})", txt)
    iso = None
    if m:
        mm, dd, yy = m.group(1).split("/")
        iso = f"{yy}-{mm}-{dd}"
    return {
        "status": "ok" if iso else "no_date_in_text",
        "date": iso,
        "is_estimate": True,
        "basis": "Zacks algorithm over this company's historical reporting dates, served "
                 "by Nasdaq. NOT a company-announced date",
        "do_not": "No finding may rest on this alone. A cadence prior read as evidence "
                  "is how TRT was ranked, traded, and never reported (2026-09-17)",
        "source": EARNDATE.format(t=ticker),
    }


def trials(company, sic):
    """Active trials and their primary completion dates. Only for pharma/biotech SICs."""
    if not company or not str(sic or "").startswith(("283", "8731", "2834", "2836")):
        return {"status": "not_applicable", "why": f"SIC {sic} is not a drug developer"}
    q = urllib.parse.quote(re.sub(r"[,.]| Inc| Corp| Ltd| plc", "", company).strip())
    raw = _get(CTGOV.format(q=q), SEC_UA, tries=2)
    if not raw:
        return {"status": "unavailable"}
    try:
        st = json.loads(raw).get("studies") or []
    except Exception:                                             # noqa: BLE001
        return {"status": "unavailable"}
    out = []
    for s in st[:12]:
        p = s.get("protocolSection") or {}
        idm = p.get("identificationModule") or {}
        stat = p.get("statusModule") or {}
        des = p.get("designModule") or {}
        out.append({
            "nct": idm.get("nctId"), "title": (idm.get("briefTitle") or "")[:110],
            "status": (stat.get("overallStatus")),
            "primary_completion": ((stat.get("primaryCompletionDateStruct") or {}).get("date")),
            "phase": (des.get("phases") or [None])[0],
            "url": f"https://clinicaltrials.gov/study/{idm.get('nctId')}",
        })
    return {"status": "ok", "n": len(out), "studies": out,
            "why_it_matters": "a primary completion date inside the next few weeks is a "
                              "dated binary the price may not hold"}


def build(ticker, price=None, with_trials=True):
    cik = cik_for(ticker)
    doc = {
        "ticker": ticker,
        "as_of_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "cik": cik,
        "purpose": "what is still coming, from primary sources, so the hunt starts at a "
                   "document rather than a search box",
    }
    if not cik:
        doc["status"] = "not_an_sec_filer_or_ticker_not_mapped"
        doc["filings"] = {"status": "unavailable"}
        doc["text_probes"] = {}
    else:
        f = filings(cik)
        doc["filings"] = f
        doc["text_probes"] = text_probes(cik)
        doc["trials"] = (trials(f.get("company"), f.get("sic"))
                         if with_trials else {"status": "not_requested"})
    doc["short_interest"] = short_interest(ticker)
    doc["insiders"] = insiders(ticker)
    doc["next_earnings_estimated"] = next_earnings(ticker)

    # The one exchange rule this container can check without the Listing Center: a US
    # listing needs a $1 bid. Under $1 starts a 180-day clock that ends in a reverse
    # split or a delisting, and both are supply events.
    if price is not None:
        doc["listing_bid_price"] = {
            "price": price,
            "under_1_dollar": price < 1.0,
            "within_25pct_of_1_dollar": 1.0 <= price < 1.25,
            "rule": "Nasdaq 5450(a)(1) / NYSE 802.01C require a $1 bid. The exchange's "
                    "own notice board is NOT reachable from here (listingcenter 403), so "
                    "a deficiency letter has to be found in the issuer's 8-K",
        }
    doc["unreachable_here"] = {
        "nasdaq_listing_center": "403",
        "ftse_russell_index_notices": "404",
        "nasdaq_press_release_api": "301",
        "consequence": "index deletions and delisting notices are only visible through "
                       "the issuer's own filings from this container. Do not assert one "
                       "without that filing",
    }
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--price", type=float)
    ap.add_argument("--no-trials", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    d = build(a.ticker, price=a.price, with_trials=not a.no_trials)
    s = json.dumps(d, indent=1)
    if a.out:
        Path(a.out).write_text(s)
    print(s)


if __name__ == "__main__":
    main()
