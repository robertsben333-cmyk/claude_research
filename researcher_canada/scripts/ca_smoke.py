#!/usr/bin/env python3
"""Stage CA plumbing checks, with no network and no model calls.

Covers the four pieces of logic that decide what gets hunted and what gets anchored,
because each of them fails as a WRONG RESULT rather than as an error:

  - the session window (a bmo name measured over an amc window is simply the wrong move)
  - the event-shape classifier (a junior's drill results read as an earnings history)
  - the option-anchor refusal (a straddle priced off a stale `last` becomes the best-
    weighted term in the scorer)
  - the calendar reconciliation (a disputed date hunted is how TRT happened)

Run it after touching ca_market.py, ca_priced_in.py or ca_universe.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_market as M          # noqa: E402
import ca_priced_in as P       # noqa: E402
import ca_universe as U        # noqa: E402

FAILED = []


def check(name, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + ("" if ok else f"   got {got!r} want {want!r}"))
    if not ok:
        FAILED.append(name)


def chain(call_bid, call_ask, put_bid, put_ask, last=5.0):
    return [{"expiry": "2026-10-16", "weekly": False, "strike": 100.0,
             "call_bid": call_bid, "call_ask": call_ask, "call_last": last,
             "call_oi": 10, "put_bid": put_bid, "put_ask": put_ask,
             "put_last": last, "put_oi": 10}]


print("Calendar and sessions")
check("a weekend is closed", M.market_closed("2026-09-26"), "weekend")
check("Thanksgiving is closed", M.market_closed("2026-10-12"), "Thanksgiving")
check("an ordinary Tuesday is open", M.market_closed("2026-09-22"), None)
check("amc window is D -> D+1", M.window("2026-09-22", "amc"), ("2026-09-22", "2026-09-23"))
check("bmo window is D-1 -> D", M.window("2026-09-22", "bmo"), ("2026-09-21", "2026-09-22"))
check("the window steps over a holiday",
      M.window("2026-10-09", "amc"), ("2026-10-09", "2026-10-13"))

print("Event shape")
check("a results release counts",
      M.is_financial_headline("Dollarama Reports Fiscal 2027 Second Quarter Results"), True)
check("drill results do NOT count",
      M.is_financial_headline("Reports High-Grade Drill Results at Eagle Zone"), False)
check("a French release counts",
      M.is_financial_headline("Quebecor publie ses résultats financiers du T2"), True)
check("two financial headlines make a wire reporter",
      M.event_shape(["Q1 2026 Financial Results", "Reports Second Quarter 2026 Results",
                     "Announces Drill Results"])[0], "release")
check("a driller is filing_only",
      M.event_shape(["Announces Drill Results", "Reports High-Grade Assay Results",
                     "Closes Private Placement"])[0], "filing_only")
check("an announcement of a future release is not a print",
      bool(M.ANNOUNCEMENT_HEADLINE.search("AGF Management Limited to Release Third "
                                          "Quarter 2026 Financial Results")), True)

print("Option anchor")
orig = P.CA.option_chain
try:
    P.CA.option_chain = lambda t: chain(4.0, 4.2, 3.8, 4.0)
    blk, lean = P.option_anchor("X", "2026-09-22", 100.0)
    check("a two-sided chain gives an implied move", blk["event_implied_move_pct"], 8.0)
    check("and an ATM spread", blk["atm_spread_frac_of_mid"], 0.025)
    check("and a lean from the call/put asymmetry", lean, 0.2)

    P.CA.option_chain = lambda t: chain(0.0, 0.0, 0.0, 0.0, last=9.0)
    blk, lean = P.option_anchor("X", "2026-09-22", 100.0)
    check("a chain with no quotes is REFUSED", blk["event_implied_move_pct"], None)
    check("and says the chain was there", blk.get("chain_present"), True)
    check("and gives no lean", lean, None)

    P.CA.option_chain = lambda t: []
    blk, lean = P.option_anchor("X", "2026-09-22", 100.0)
    check("no chain at all is refused too", blk["event_implied_move_pct"], None)
    check("and does not claim a chain was present", blk.get("chain_present"), None)

    P.CA.option_chain = lambda t: chain(4.0, 4.2, 3.8, 4.0)
    blk, lean = P.option_anchor("X", "2026-12-01", 100.0)
    check("an expiry before the print is not an anchor",
          blk["event_implied_move_pct"], None)
finally:
    P.CA.option_chain = orig

print("Calendar reconciliation")
CON = {"date": "2026-10-22", "confirmed": True, "status": "CON", "session": "amc"}
UNC = {"date": "2026-10-22", "confirmed": False, "status": "UNC", "session": "bmo"}
check("a CON flag wins outright",
      U.reconcile("2026-10-29", CON), ("confirmed", "2026-10-22", "amc"))
check("two vendors agreeing is good enough",
      U.reconcile("2026-10-22", UNC), ("agreed", "2026-10-22", "bmo"))
check("WSH alone is wsh_only",
      U.reconcile(None, UNC), ("wsh_only", "2026-10-22", "bmo"))
check("a contradiction is disputed",
      U.reconcile("2026-10-29", UNC), ("disputed", "2026-10-22", "bmo"))
check("no WSH row is vendor_only",
      U.reconcile("2026-10-29", None), ("vendor_only", "2026-10-29", None))

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {', '.join(FAILED)}")
    sys.exit(1)
print("All stage CA plumbing checks passed.")
