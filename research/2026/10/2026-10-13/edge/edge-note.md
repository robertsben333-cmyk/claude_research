# Edge hunt — 2026-10-13 amc + 2026-10-14 bmo

**No name clears either floor today, so the book is empty.** The highest |`impact_sum`| is 1.60 (ASML, MS) against a floor of 2.8. The highest |`impact_scaled`| is 0.65 (SOTK) against the book's floor of 1.76. Below the floor the sign has been a coin flip (53% over 38 events), so what follows is a ranking and not a set of views. Eight of nine names are large caps reporting into a week where the peer banks (JPM, GS, C, WFC) printed on 2026-10-13. Most findings are peer read-throughs that land inside guidance, and the hunters sized them small, as they should.

Ranking key: `impact_sum` (as named in `edge-scores.json`), signed points of spot.

| # | ticker | session | pre-lessons | post-lessons (key) | scaled | V2 | floor | tradable | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ASML | bmo 10-14 | +2.50 | **+1.60** | +0.60 | +1.18 | no | yes — $2,331m/day, ok | −6.69 |
| 2 | MS | bmo 10-14 | +2.10 | **+1.60** | +0.63 | +0.37 | no | yes — $1,024m/day, ok | +8.93 |
| 3 | AZZ | amc 10-13 | +1.40 | **+1.05** | +0.52 | +0.31 | no | yes — $34m/day, ok | −3.76 |
| 4 | BAC | bmo 10-14 | +1.30 | **+0.90** | +0.36 | +0.38 | no | yes — $1,997m/day, ok | +9.39 |
| 5 | BLK | bmo 10-14 | +0.40 | **+0.60** | +0.48 | +0.09 | no | yes — $549m/day, ok | −1.58 |
| 6 | PGR | bmo 10-14 | +0.70 | **+0.30** | +0.15 | +0.10 | no | yes — $674m/day, ok | −1.07 |
| 7 | STT | bmo 10-14 | +0.50 | **+0.20** | +0.08 | +0.08 | no | yes — $370m/day, ok | +6.80 |
| 8 | FAST | bmo 10-14 | +0.00 | **−0.20** | −0.29 | −0.07 | no | yes — short, Alpaca lends, $346m/day | −2.99 |
| 9 | SOTK | bmo 10-14 | −1.40 | **−0.70** | −0.65 | −1.16 | no | yes — short, Alpaca lends, $1.0m/day (borderline thin) | −56.22 |

Pre-lessons, scaled and V2 are measured beside the key and are not traded. Since 2026-10-02 the book selects on |scaled| ≥ 1.76; nothing reached it.

## What drives the top and the bottom

- **ASML +1.60.** The largest finding (+0.7) is a customer proxy. Since ASML's July call, Samsung's Q3 preliminary operating profit came in at KRW 107.4tn, TSMC's Q3 revenue rose 50.9% y/y and Micron raised its FY27 capex. The second (+0.6) is ASML's own July capacity plan, about +45% effective EUV output, which sits above the ~28% 2027 sales growth the street models. Sources are in `hunts/ASML.json` (https://investor.asml.com/news-releases/news-release-details/q2-2026-financial-results). The price says: skew −7.1 (calls bid), −7.4% over five days on sector de-risking. The baseline's reaction history is contaminated by non-earnings 6-K dates, so the hunter rebuilt it: 2 of 6 confirmed prints closed up, and beats have been sold.
- **MS +1.60.** One finding carries it (+1.5). The 10-13 peer prints show GS equities +72% y/y and JPM equities +49%, while the published MS equities estimates ($4.5–4.9bn) predate them. That points to an EPS beat of roughly 8% on a ~$3.08 bar (https://247wallst.com/investing/2026/10/13/goldman-sachs-rises-on-equities-led-earnings-beat-jpmorgan-chase-treads-water-wells-fargo-declines-3/). The price says: MS fell 1.2% on 10-13 while GS rose, and its July record-equities beat closed only +0.39%. This is a peer proxy, not a company number.
- **SOTK −0.70 (bottom).** The stock is +56% in 20 days on two order PRs whose deliveries fall mainly in FY2028. The FY2027 guide (flat to modestly higher) has no path to rise on them (https://finviz.com/news/396901/sono-tek-announces-record-719-million-in-orders-from-advanced-clean-energy-sector-customer). The CEO also flagged that Q1's 57% gross margin is not representative, and the one-analyst EPS bar is disputed ($0.04 against $0.05). There is no option chain, so the baseline is inferred from history, and the baseline's own history is untrustworthy (implausible cadence).
- **FAST −0.20.** The findings net to about zero. Two months of public sales imply a revenue beat against a stale bar, but a gross margin down 80–100bp is the line this stock was sold on in Q1 and Q2.

## Names that could not be ranked

None. All 9 are rankable, and the sweep confirmed 9 of 9 from company sources with 0 phantoms. Four `time-not-supplied` rows were checked and left out. `session_resolve.py` killed UNTY (8-K item 2.02 filed 2026-10-13). BMRA, FNGR and NXTT had no announced date and were not added.

## Critical read of the floor-clearers

There are none. One sentence on the two closest: **ASML and MS are not recommended**. Both sit at 1.60, about 57% of the floor. Both rest mainly on peer or customer proxies that land inside guidance on a name whose recent beats have been sold. MS also nets 3 positive against 2 negative findings, which the scorer flags.

## What the note must also say

- **Order versus sign.** This is a ranking only. Below the floor the sign is a coin flip on the evidence so far (53% over 38 events); above it the rank of conviction predicted sign-correctness at ρ=+0.514 on that sample (+0.361 once the double hunt is controlled for). Nothing is above it today. `impact_sum` is not a forecast of the move. It sums findings that can rest on the same document.
- **Control.** −run_up_20d ranks BAC, MS, STT at the top and SOTK at the bottom. The hunt's order correlates with it at Spearman +0.23 today: the same bottom name, a different top. Over the resolved sample the free control has not been beaten durably, and over 105 events it returned −0.42% a trade.
- **Sign balance.** 7 of 9 names lean positive and 2 negative. That is the reverse of the early negative tilt, and most of it is the 10-13 peer prints read across. It is a correlated exposure (five financials on one peer read) that the scorer cannot see.
- **Nothing checked the findings.** There is no adversary and no second hunter, so a factually wrong finding enters at full size. Several hunters relied on search snippets where fetches returned 403 or 503 (ASML finding 4, PGR's consensus, BAC's JPM trading split).
- **Reproducibility.** When two hunters sized the same name, the median gap was 2.40 points, and 4 of 12 pairs had opposite signs. Every key today is smaller than that gap.
- **Baseline measured or inferred.** 8 of 9 names have a live option chain. SOTK has none, so its expected move is a historical median and its lean is −0.05 × run-up.
- **Cost to trade.** All nine clear the $200k turnover floor. SOTK sits right at the $1m thin line ($1.01m/day), so its extreme is the least tradeable row.
- **One day is an anecdote.** Nine names cannot produce a meaningful rank correlation, and the stage has not yet beaten a free control on the pooled sample.

## Context: retail, search and volatility (not used for selection)

These labels are context only; nothing ranks, selects or trades on them.

- ASML: retail no (14), search not quiet (1.03x), vol no (30)
- MS: retail no (11), search failed, vol no (19)
- AZZ: retail no (25), search quiet (0.97x), vol no (20)
- BAC: retail no (16), search quiet (0.98x), vol no (19)
- BLK: retail no (9), search quiet (0.80x), vol no (19)
- PGR: retail no (15), search sparse, vol no (22)
- STT: retail no (16), search quiet (0.91x), vol no (13)
- FAST: retail no (18), search not quiet (1.02x), vol no (16)
- SOTK: retail **yes** (72), search failed, vol **yes** (77)

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
