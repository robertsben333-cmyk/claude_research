# researcher_canada — an access measurement, not a stage

There is no stage CA. Nothing here seals a baseline, spawns a hunter, ranks a day or
places an order, and nothing downstream reads it. This directory holds one thing: the
measured answer to whether Canada can be read from this container at all.

**It can.** The two official surfaces are shut and stay shut: `sedarplus.ca` answers a
Radware 403 eight times out of eight and `ciro.ca` a Cloudflare interstitial eight times
out of eight, on the same retry protocol that rescued France. Both are reachable through
TMX Group's own portal instead. `app-money.tmx.com/graphql` is unauthenticated and serves
the SEDAR+ filing index with a PDF per filing, a consolidated newswire archive with
timestamps, the short-interest register, Wall Street Horizon's calendar with a
confirmed/unconfirmed flag, and TMX's own daily tape. `m-x.ca` serves the listed option
chain for 360 underlyings.

Read `SOURCES.md` before using any of it. The short version of what it establishes:

- The **short register covers 87 to 88% of every turnover band**, including the $1–5m
  band this repo's thesis is about. That matches the FCA register there (89%) and beats
  it badly below $1m, where the UK covers 32% of the names the $200k floor adds against
  Canada's 88%. Japan's register names 9 to 11 of 25 at any size.
- The **vendor calendar's phantom rate is 1 in 140**, against 20 of 20 for the US
  `time-not-supplied` rows. 68% of past events are confirmed by a results release on the
  wire and almost all the rest by a financial-statement filing on SEDAR+.
- The **release timestamp settles the session**, agreeing with the vendor flag on 90 of
  92 confirmed prints.
- The **option chain covers 43% of the $1–5m band and 96% above $25m**, which would make
  Canada the only market outside the US where the anchored and anchor-less regimes can be
  run side by side and compared within one day's names.

And the short version of what it does not establish:

- Everything except the option chain comes from **one vendor stack**. Europe's ten markets
  fail independently; Canada would fail all at once.
- The register has **no history and an ununderstood date stamp**, so the level is usable
  and the change is not, until the field has been recorded daily for a fortnight.
- The **implied move is unverified** — every fetch here ran with Toronto shut, so the
  straddle was priced off `last`.
- The calendar's two sources **disagree on 172 of 277 forward dates** and nothing here
  says which is right.
- Roughly a third of the eligible universe reports by **filing rather than by press
  release**. That is a different event shape from the one this method assumes, and it is
  concentrated in junior mining at the bottom of the band.

## Files

```
SOURCES.md                      the measurement, with every number and its caveat
scripts/ca_sources.py           the client: GraphQL + Montreal Exchange, plus CAPABILITY
scripts/ca_measure.py           reproduces every number in SOURCES.md
analysis/ca-source-measurement.json   what the last run wrote
```

```bash
python3 researcher_canada/scripts/ca_sources.py     # self-test on one name
python3 researcher_canada/scripts/ca_measure.py     # the whole battery, ~7 minutes
```

## If a stage is ever built here

Three things would have to be settled first, in this order, and all three are cheap:

1. **Record `getCompanyShortInterest` daily for two weeks** and find out whether
   `BUSINESS_DATE` moves. Everything about a positioning anchor depends on the answer and
   nothing else can be built on it until it is known.
2. **Score Wall Street Horizon against TradingView** on the forward fortnight, using the
   news archive of section 4 as the judge. One of them is the calendar; today neither is.
3. **Run one chain fetch during the Toronto session** and see whether bid and ask
   populate. That is the difference between an option anchor and a stale print.

Until those three are done, a Canadian stage would be built on an anchor of unknown
freshness, a calendar of unknown provenance and an implied move of unknown quality. None
of that is visible from a ranking, which is exactly how TRT happened.
