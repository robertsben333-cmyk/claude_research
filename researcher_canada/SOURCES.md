# Canada: what is reachable, measured 2026-09-22

## 1. The verdict that changes

The first pass over Canada was right about both hosts and wrong about the market.
`sedarplus.ca` and `ciro.ca` are shut from this container and stay shut when retested
properly. Neither is the only route to what sits behind it.

TMX Group's own retail portal runs on an **unauthenticated GraphQL endpoint**,
`app-money.tmx.com/graphql`, which serves the SEDAR+ filing index with a downloadable
PDF per filing, a consolidated newswire archive with timestamps, the short-interest
register, Wall Street Horizon's earnings calendar with a confirmed/unconfirmed flag,
analyst counts, insider transactions and TMX's own daily tape. The Montréal Exchange
serves the full listed option chain for 360 underlyings, free, from `m-x.ca`.

On coverage of the earnings universe Canada is the **best-instrumented non-US market in
this repo**, and on two axes it is better instrumented than the US stage: the calendar
carries its own confirmation flag, and the option chain is published by the exchange
rather than inferred.

## 2. The sources, with the eight-try protocol applied

Eight attempts, 2 to 4 second backoff, the protocol the France leg earned after four
resets were read as a dead host.

| Host | Role | Result |
| --- | --- | --- |
| `app-money.tmx.com/graphql` | filings, news, short register, calendar, tape | **8/8**, no auth |
| `app.quotemedia.com` | the SEDAR+ filing PDF itself | **8/8**, 134 KB retrieved |
| `www.m-x.ca` | listed option chain, 360 underlyings | **8/8 serial**, 0/26 at 5 concurrent |
| `scanner.tradingview.com` | forward calendar and turnover | **8/8** |
| `www.sedarplus.ca` | the official filing archive | **0/8**, Radware 403 |
| `www.ciro.ca` | the official short register | **0/8**, Cloudflare interstitial |
| `www.sedi.ca` | insider filings | **0/8**, same Radware 403 |

Rate limits were not hit. The coverage sweep in section 3 made 748 GraphQL calls at
eight concurrent and the confirmation sweep in section 4 another 179, with no throttling
response and no failure. The Montréal Exchange is the opposite: 26 chains at five
concurrent returned 26 truncated pages, and the same 26 fetched one at a time all
returned in full. Fetch it serially.

The two blocks are different failures and neither is France's. SEDAR+ returns a hard 403
with a Radware transaction id and no challenge to solve; CIRO returns a Cloudflare
interstitial. A backoff does not rescue either, and nothing here tries to defeat them.

## 3. Coverage of the universe that matters

TradingView's Canada scanner returns 2,507 primary listings (TSX 623, TSXV 1,301,
CSE 562, NEO 21). Screened the way stages E, J and EU screen, at $200k a day of
turnover, with a scheduled release in the next 60 days: **374 names**.

| Turnover band | names | option chain | short interest | WSH calendar |
| --- | ---: | ---: | ---: | ---: |
| $0.2–1m | 112 | 10% | **88%** | 46% |
| $1–5m | 84 | 43% | **87%** | 70% |
| $5–25m | 104 | 79% | **88%** | 90% |
| above $25m | 74 | 96% | **97%** | 97% |
| all | 374 | 53% | **90%** | 74% |

Against the earlier EDGAR cross-filing measurement on the same market, which came in at
36% overall, 31% at $0.2–1m, 26% at $1–5m and 59% above $25m.

EDGAR rescued the large caps and nothing else. The short register does the
opposite: it is **flat across the bands**, covering 87% of the $1–5m names this stage's whole thesis is about. Compared like for
like: the FCA register covers 89% of the UK cohort in the $1–5m band, so Canada matches
the best register in the repo there, and **32% of the UK names the $200k floor adds
below $1m against Canada's 88%**, which is where the gap is. JPX names 9 to 11 of 25
Japanese names at any size.

The option chain is the mirror image, strong at the top and thin at the bottom. That is
not a reason to skip it. It means Canada can run **two regimes side by side in one
market**: an anchored one on the optionable half, which is the only non-US test of the
regime `archive/backtest/FINDINGS.md` §33 measured at ρ=+0.073 anchor-less, and an
anchor-less one below it, carried apart in the data exactly as `anchor_covered` is in
Europe.

## 4. Confirmation: the phantom rate is about 1 in 139

The test the UK leg ran against Investegate and the US one against EDGAR. Take the
vendor's **last** release date for names that reported in the past 45 days, sample 140,
and ask the archives whether anything happened. All 140 had an archive reaching back past
the event date.

- **95 of 140 (68%)** carry a same-day results headline on the wire.
- **101 of 140 (72%)** carry a same-day release of any kind.
- Of the 39 with no release at all, **38 have an interim-financials or 52-109 filing on
  SEDAR+ within three days** of the vendor's date.
- **1 of 140 is unconfirmed by either route.**

So the vendor calendar is not the US calendar. But the 68% is the number to carry, not
the 99.3%, because those two routes are not the same event. A Dollarama results release at
07:00 ET is a print a hunt can be run into. A junior explorer filing interim statements
on SEDAR+ at some hour with no press release is a **different event shape**, and the
whole method here assumes a release that a market reprices against. The gap is almost
entirely the $0.2–1m band (60% wire-confirmed, against 93% above $25m) and almost entirely junior mining.

The archive also settles the session. On 91 confirmed prints where the vendor supplied a
session flag, the release timestamp agrees **90 times**. Canada can read the session off
the event itself, which the US stage cannot.

## 5. The calendar carries its own confirmation flag

`getWSHEventData` returns Wall Street Horizon events with `event_status` of `CON` or
`UNC` and the session written into `event_name` ("Before Mkt" / "After Mkt"). Over the
374 eligible names, 277 carry an earnings event, 50 of them confirmed, 271 with a session
encoded.

**It disagrees with TradingView on 172 of 277 next-release dates**, among them Enbridge
(10-30 against 11-06), Canadian Natural (10-29 against 11-05) and Barrick (10-29 against
11-09). Both cannot be right
and nothing here establishes which is. That is the first thing to settle before a stage
is built, and it is cheap to settle: record both forward for a fortnight and score them
against the archive, which is the same instrument section 4 already validates.

A confirmation flag is worth naming plainly. TRT was ranked, traded at 33% of equity and
never reported, because a cadence prior was read as evidence a print existed. `CON` is
not a cadence prior. It does not remove the need for the archive check; it removes the
class of mistake that made the check necessary after the fact.

## 6. What is not solved

1. **One vendor.** Short interest, filings, news, calendar and tape all arrive through
   the TMX/QuoteMedia stack. Europe's ten markets fail independently. Canada fails all at
   once. A second source for the register was looked for and not found: `tsx.com` has no
   short-position page (404), Fintel is behind Cloudflare, and Barchart, MarketBeat and
   stockanalysis.com render the number client-side, so none of them answers from here.
2. **No history on the register.** One snapshot, no date argument, no history field. The
   FCA's per-holder history makes the UK anchor backtestable; Canada's cannot be. A
   change-in-short-interest variable has to be accumulated forward or not used.
3. **The register's date is not understood.** All 336 readings came back stamped
   `BUSINESS_DATE 2026-09-21`. CIRO publishes twice a month, as of the 15th and
   month-end, so this is either a daily refresh of a modelled number or a publication
   date pasted onto the 09-15 snapshot. Those mean opposite things. Record the field
   daily for two weeks before anything reads the change; the level is usable now.
4. **The implied move is unverified, and today's number is not usable.** Everything here
   ran with Toronto shut, so bid and ask are zeroes and **0 of 26 sampled chains could be
   priced off a quote**. 25 of 26 produced a number off `last` and 20 carried open
   interest at the money, but the median came out at **12.5% over a median 15 days past
   the print** — a whole-life straddle off possibly stale marks, not an earnings implied
   move. Two separate pieces of work: one live-session fetch settles whether quotes
   populate, and de-trending the event's share out of the straddle is unbuilt.
5. **Terms of use.** money.tmx.com is a retail portal, not a published data product. This
   is read-only research traffic at single-name rates and should stay that way. m-x.ca
   refuses at 5 concurrent and answers 8 of 8 serially.
6. **Nothing here is a result about Canadian prints.** No baseline has been sealed, no
   hunt has run, nothing has resolved. This is an access measurement and only that.

## 7. Reproduce it

```bash
python3 researcher_canada/scripts/ca_sources.py            # self-test, one name
python3 researcher_canada/scripts/ca_measure.py            # every number above
```

`ca_measure.py` writes `researcher_canada/analysis/ca-source-measurement.json`. The
committed run is 2026-09-22T08:05Z. One thing in it is degraded and says so in the file:
Yahoo answered 429 to all six tries for CADUSD, so the turnover floor was applied at a
constant 0.71 rather than a live rate (`fx_source` records which). At the band
boundaries that moves a handful of names either way and changes nothing in the table.
