#!/usr/bin/env python3
"""The User-Agent this repo sends to SEC EDGAR, and the one lookup that needs no contact.

SEC asks automated clients to name themselves and give a contact address. A contact
address is personal data, so it does not live in this repo. The environment a Routine
runs in sets it:

    SEC_USER_AGENT="claude-research earnings-pipeline <contact address>"

Until 2026-11-16 three scripts here hard-coded a personal address. A session whose
privacy hook refuses to run a script holding the account's own address could not run
them, and that stopped stage E-P v3b before its sweep on its first fire.

What SEC answers to a plain client name with no address, measured 2026-11-16 from a
Routine container:

    data.sec.gov/submissions                  200
    efts.sec.gov full-text search             200
    efts.sec.gov company lookup (keysTyped)   200
    www.sec.gov/files/company_tickers.json    403
    www.sec.gov/Archives/edgar/data/...       403
    www.sec.gov/cgi-bin/browse-edgar          403

So without the variable a ticker still maps to its CIK through `lookup_cik()` and the
8-K item 2.02 history still reads, while everything under www.sec.gov fails. Each caller
says so in what it writes, because a refused request read as an empty filing record is a
plausible wrong answer, which is the failure this repo keeps paying for.

    python3 researcher_us/scripts/sec_contact.py     # is it set, does it carry a contact

The value itself is never printed, so it cannot end up in a run log.
"""
import json
import os
import urllib.parse
import urllib.request

ENV = "SEC_USER_AGENT"
GENERIC = "claude-research earnings-pipeline"
EFTS_LOOKUP = "https://efts.sec.gov/LATEST/search-index?keysTyped={q}"
NO_CONTACT = (f"{ENV} is not set to a User-Agent with a contact address, and "
              "www.sec.gov refuses requests without one (403)")


def user_agent():
    """The configured User-Agent, or a plain client name when none is set."""
    return (os.environ.get(ENV) or "").strip() or GENERIC


def has_contact():
    """www.sec.gov answers only a User-Agent that carries an address."""
    return "@" in user_agent()


def lookup_cik(ticker, timeout=25):
    """Ticker to 10-digit CIK from EDGAR's company lookup, which needs no contact.

    Exact match on the listed tickers only: the lookup is a prefix search, so `LX`
    also returns LXU and LXSPY. EDGAR writes share classes with a hyphen (BF-B), and
    the same query with a dot returns nothing, so the hyphen form is asked.
    """
    t = (ticker or "").upper().strip()
    if not t:
        return None
    forms = {t, t.replace(".", "-"), t.replace("-", ".")}
    req = urllib.request.Request(
        EFTS_LOOKUP.format(q=urllib.parse.quote(t.replace(".", "-"))),
        headers={"User-Agent": user_agent(), "Accept": "application/json"})
    doc = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    for hit in (doc.get("hits") or {}).get("hits") or []:
        listed = (hit.get("_source") or {}).get("tickers") or ""
        if {x.strip().upper() for x in listed.split(",")} & forms:
            return str(hit["_id"]).zfill(10)
    return None


if __name__ == "__main__":
    raw = (os.environ.get(ENV) or "").strip()
    print(f"{ENV} set: {'yes' if raw else 'no'}")
    print(f"carries a contact address: {'yes' if has_contact() else 'no'}")
    if not has_contact():
        print(f"www.sec.gov will refuse: {NO_CONTACT}. Ticker lookups fall back to the "
              "EDGAR company search; 6-K exhibits and filing text are not read.")
