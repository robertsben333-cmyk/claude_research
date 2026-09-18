# Outcome — 2026-09-16

**Measurement:** close before the print (2026-09-16) → close after the first full
session following it (2026-09-17).

| Ticker | Call | Signed est. move | Actual move | Direction hit | Magnitude error | Band hit | Implied move broken | Reversal fired | Prelim score | Prelim hit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LEN | Lean Down | −1.4% | **+1.71%** | **No** | +3.11 | No (below 2.3–7.3% band) | No (5.2% implied) | No | −22 | **No** |

## LEN — Lennar Corporation

Reported Q3 FY2026 AMC Tuesday 2026-09-16. A genuine, sourced **double miss**: adjusted
EPS $1.23 vs. $1.30 consensus, revenue $8.05B vs. $8.31B consensus, new orders −9% y/y,
and a second consecutive cut to full-year delivery guidance (80,000–81,000 homes) citing
"deteriorated" market conditions since the last call. This is exactly the kind of print
both the panel (consensus −25.7, Lean Down, certainty High) and the cheap preliminary
read (−22) expected.

**Close 2026-09-16 (pre-print): $78.36** (a -2.14% day on its own, ahead of the AMC
release). **Close 2026-09-17 (post-print): $79.70** — **+1.71%** close-to-close.
Source: stockanalysis.com daily history API, cross-checked against an independent
after-hours report (shares fell a further ~2.6% after hours to ~$76.34, consistent with
a same-session low of $76.07 on 09-17) and an independent article confirming the 09-16
close of $78.36/-2.1%. **Discrepancy flagged:** one AI-generated web-search summary
reported a 09-17 close of $78.54 (+0.22%); this does not match the directly-fetched
stockanalysis.com OHLC table (open $81.00, high $81.00, low $76.07, close $79.70, which
is internally self-consistent with the surrounding days' chained % changes) or the
after-hours/low figures independently reported elsewhere, so the stockanalysis.com
figure is treated as authoritative per the exchange/major-provider preference rule.

**What actually happened, and why the call missed:** the fundamentals broke exactly the
way the panel and the preliminary read both expected — a real, sourced miss and a real
guidance cut, not a mixed or ambiguous print. The stock fell hard after hours (to
roughly −2.6% to −5% below the pre-print close) and again to an intraday low of $76.07
(−2.9% below the pre-print close) during the 09-17 session — so the *initial* reaction
was squarely in line with the bearish call. What reversed it was **2026-09-17 also being
a Fed rate-decision day**: broad market strength on the decision (described in coverage
as a hike, with commentary framing it as inflation-fighting and unanimous) lifted risk
assets generally, and LEN rallied off its intraday low to close net positive on the day.
This is a company-specific miss getting overrun by a same-day macro catalyst that had
nothing to do with Lennar — the single most useful root-cause finding this stage has
produced from a magnitude/direction miss: **the panel's window (close-to-close over the
next full session) has no way to separate a company-specific reaction from a same-day
macro event that happens to land in the same window.** This is a scheduling/measurement
limitation, not evidence the panel's or the dossier's read of Lennar itself was wrong —
both correctly called the print itself bearish.

**Reversal case check:** the red-team's stated bull case (mortgage-rate tailwind making
the margin guide easy, a fresh buyback authorization landing in the release) is **not**
what fired — there was no buyback announcement in this release and no beat; the printed
numbers were a clean miss. The mechanism the red-team named did not happen. The price
reversal that did happen came from an entirely different, exogenous source (the Fed
decision), which no persona and no version of the preliminary read was tasked with
pricing in. `reversal_fired: false` — the named mechanism failed even though the price
technically moved against the panel's direction.

**First directional call in the ledger.** Every one of the prior 15 panelled calls was
Neutral / No Edge; this is the panel's first Lean/Strong Up/Down call, and it is also the
first panelled call with a real signed_estimated_move — so this is also the first
non-null magnitude_error the ledger has ever recorded. It missed direction (called down,
went up) and missed magnitude (predicted −1.4%, got +1.71%, error +3.11pp) and missed
band (predicted 2.3–7.3% unsigned range, got 1.71% — smaller than the pipeline's own
model of Lennar's typical earnings-day move, despite reporting a real miss). The
preliminary read (−22, the dossier's most confident directional read to date) missed in
exactly the same direction, for the same reason: both correctly read the fundamentals
and had no way to see the same-day Fed decision coming.

## 2026-09-17 — nothing to score

`04-advice.json` for 2026-09-17 carries `status: "no_names"`: stage 0's universe for
that window had exactly one candidate (UPXI, $76.0M market cap), which failed the $500M
floor and was never eligible, so stage 1 published an empty shortlist and stages 2/3
correctly produced nothing. Every stage published a heartbeat; this is not a failed
Routine. No calls exist to score for this date.
