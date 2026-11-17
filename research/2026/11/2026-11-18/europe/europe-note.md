# Stage EU — Europe researcher, event date 2026-11-18

**Answer first.** No name clears the 2.8 conviction floor on `impact_sum`. The four-model panel selects **four shorts, 4 of 4 judges each: PFS0 (panel_pct 98), ARR (97), MSLH (96), SDY (85)**. The hunters' key points the same way on all four (−1.30, −0.50, −1.40, −0.70). Top of the key is ITH (+0.90), bottom MSLH (−1.40). Two vendor rows were phantoms (ENH, TISG). One day is not a result.

Sealed 2026-11-17 ~14:45 UTC while the European markets were still trading, so every sealed spot is an intraday price, not a close. Scored window close(17 Nov) → close(18 Nov) for bmo names. Three Polish names (CLN, CPS, KGH) were defaulted to bmo by the vendor, but their hunters set `session_check` to **amc** from the issuers' own filing timestamps (the reaction window would then be close 18 Nov → close 19 Nov; the resolver measures both).

## Ranked table (`ranking_key` = `impact_sum`)

| # | ticker | mkt | session | impact_sum | abs_move | p_up | impact_scaled | anchor | pre-released / new |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ITH | uk | bmo (issuer calendar, webcast 09:00 GMT) | +0.90 | 5.5 | 52 | +0.22 | no (truncated zero) | Q3 new; production/price public |
| 2 | ELON | se | bmo (MFN est. 08:30 CET) | +0.70 | 10.0 | 52 | +0.40 | no (truncated zero) | Q3 new; no consensus at all |
| 3 | SSE | uk | bmo (07:00) | +0.60 | 3.0 | 53 | +0.18 | yes (1.3%, covering) | **H1 EPS pre-released 1 Oct** |
| 4 | BLND | uk | bmo (07:00) | +0.30 | 2.6 | 50 | 0.00 | no (truncated zero) | **H1 pre-released 15 Oct**; first results under new CEO |
| 5 | HAFNI | no | bmo (07:30 CET, NewsWeb 686176) | +0.20 | 4.5 | 52 | +0.18 | no (truncated zero) | 80% of Q3 days pre-covered; Q4 cover new |
| 6 | CPS | pl | **amc per hunter** (vendor bmo) | +0.10 | 6.0 | 53 | +0.36 | no (pl) | Q3 new; strategy and guide given 29 Oct |
| 7 | SVT | uk | bmo (07:00) | +0.10 | 2.5 | 52 | +0.10 | yes (2.69%, building) | Q1 pre-released 9 Jul |
| 8 | SVEAF_B | se | bmo (07:30 CET, issuer) | 0.00 | 5.5 | 47 | −0.33 | no (truncated zero) | first report after KlaraBo merger |
| 9 | PEN | no | bmo (07:00 CET, NewsWeb 686174) | −0.10 | 4.0 | 50 | 0.00 | no (truncated zero) | **Q3 pre-released 4 Nov**; 2026 guide re-base new |
| 10 | CLN | pl | **amc per hunter** (vendor bmo) | −0.20 | 5.5 | 46 | −0.44 | no (pl) | Q3 new; no szacunkowe wyniki |
| 11 | KGH | pl | **amc per hunter** (vendor bmo) | −0.20 | 4.5 | 47 | −0.27 | no (pl) | Q3 volumes/prices public monthly |
| 12 | ARR | no | bmo (07:30 Oslo) | −0.50 | 8.0 | 44 | −0.96 | no (truncated zero) | Q3 new; company flagged headwinds in Q2 |
| 13 | SDY | uk | bmo (07:00) | −0.70 | 8.0 | 46 | −0.64 | yes (0.21%) | H1 new beyond Jul revenue; covenant test |
| 14 | VOW | no | bmo (NewsWeb 686196) | −0.90 | 8.0 | 46 | −0.64 | no (truncated zero) | Q3 new; refinancing open |
| 15 | WKP | uk | bmo (07:00) | −0.90 | 5.0 | 46 | −0.40 | yes (6.76%) | Q2 KPIs pre-released 15 Oct |
| 16 | CTEC | uk | bmo (07:00 by precedent) | −1.20 | 7.5 | 45 | −0.75 | yes (4.26%) | 10-month update; **first FY27 outlook** likely new |
| 17 | PFS0 | de | bmo (08:00 CET, issuer) | −1.30 | 9.0 | 46 | −0.72 | yes (0.54%) | Q3 new; no pre-release |
| 18 | MSLH | uk | bmo (07:00 by precedent) | −1.40 | 5.5 | 45 | −0.55 | yes (4.17%, building) | 10-month update; peers warned in period |

`impact_scaled` is the hunter's second measurement, (2·p_up/100 − 1)·abs_move. It is not the key and the floor does not apply to it.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing. All four members ran on their pinned `-intl-` agents, no fallback, 18 of 18 packs each. Selection is `consensus` (3 of 4 in their own top 20%); each member is read against its own last 200 live sizes.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PFS0 | **yes** | 98 | short | 2 | 100S* | 97S* | 99S* | 94S* | 4 | −2.91 | −1.30 |
| 2 | ARR | **yes** | 97 | short | 3 | 100S* | 93S* | 99S* | 96S* | 4 | −2.70 | −0.50 |
| 3 | MSLH | **yes** | 96 | short | 3 | 99S* | 93S* | 93S* | 98S* | 4 | −2.24 | −1.40 |
| 4 | SDY | **yes** | 85 | short | 8 | 90S* | 80S* | 95S* | 76S | 4 | −1.39 | −0.70 |
| 5 | ELON | | 73 | long | 18 | 86L* | 52L | 58L | 96L* | 2 | +1.11 | +0.70 |
| 6 | CTEC | | 66 | short | 20 | 81S* | 82S* | 68S | 32S | 2 | −1.08 | −1.20 |
| 7 | VOW | | 28 | short | 56 | 50L | 87S* | 74S | 0 | 1 | −0.54 | −0.90 |
| 8 | ITH | | 67 | long | 8 | 76L | 67L | 55L | 70L | 0 | +0.91 | +0.90 |
| 9 | KGH | | 45 | short | 5 | 37S | 50S | 42S | 50S | 0 | −0.52 | −0.20 |
| 10–18 | WKP, SSE, HAFNI, CPS, PEN, BLND, CLN, SVT, SVEAF_B | | ≤25 | | | | | | | 0 | | |

(SDY's `k` is printed 4 by the scorer though fable51 reads 76; it is selected either way, 3 of 4.)

**PFS0 short (98).** Every member names the order-intake line: the FY order target (~EUR 549m) is out of reach after H1 intake fell 9.4%, Q3-25 is a tough EUR 141.1m comparison, the H1 outlook dropped the numeric guide, and order intake decided both 2026 prints (−12.3%, −12.0%) despite earnings beats ([EQS H1](https://www.eqs-news.com/news/corporate/pfisterer-holding-se-continues-successful-growth-trajectory-significant-increase-in-revenue-and-earnings/6f2f72cf-05bb-429b-84fe-f0a99dc4cd8a_en)). Case against: the stock is already ~26% below the H1-day close and 46% below its May high, Bernstein initiated Outperform at 102, and Nexans' grid accessories grew strongly in Q3.

**ARR short (97).** The company's own Q2 report flagged Q3 Cloud headwinds (hardware costs, seasonality, a client bankruptcy), the bar is one analyst and snippet-only, and the +9.7% move on the UK DE&S contract (10 Nov) runs into the print while the signing falls after the window. Case against: insiders (chair, an EVP) bought inside the quarter, the DE&S win is real, and at ~$0.13m a day this is a micro-cap whose bar is essentially unknown.

**MSLH short (96).** Both listed UK brick peers cut guidance inside Marshalls' period — Ibstock 2 Nov ("materially below", [RNS](https://www.investegate.co.uk/announcement/rns/ibstock--ibst/q3-trading-update-/9851713)) and Forterra 11 Nov, which also called home-improvement demand as weak as new-build — Travis Perkins merchanting volume was −9.0%, and Marshalls' own broker consensus page (£49.7m PBT) is dated 10 Aug. Case against: 4.17% disclosed short (building), the £11m Landscaping self-help, and the likeliest outcome is an "in line" statement with a relief move.

**SDY short (85).** H1 results with nothing pre-released beyond revenue to July, full-year profit already pushed "towards the lower end" in September, the first covenant test at the original leverage limit and a going-concern flag in the FY26 accounts, against a construction PMI of 43.6. Case against: the stock has already fallen ~27% since late August, and ProService (a direct counterparty) said it was ahead of expectations.

**Where panel and key disagree most.** ARR: the key reads only −0.50 while all four judges put it in their top 7%. VOW: the key reads −0.90 but the judges split (Opus 5 long, Opus 5.5 and Sonnet short, Fable flat). CTEC: the key's second-most negative name (−1.20) is not selected because Fable reads it small. ELON: two judges in their top 20% long, two not.

**What the numbers are not.** `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing; the EU member scales still lean on the frozen E-P seed until this market has ~200 panel names of its own; in the four-model re-judge the judges ranked Europe better than the live hunt, but nothing about this market's panel is established (2026-10-21: ρ +0.22, p 0.19 on 45 names).

## Top and bottom, and what drives them

- **Top, ITH +0.90:** a dividend-guide raise is plausible because the FY26 guide is a fixed 30% of post-tax operating cash flow and Q3 realisations ran well above H1 (peer Harbour's 9M pre-hedge $92/bbl and raised FCF outlook, [RNS](https://www.investegate.co.uk/announcement/rns/harbour-energy--hbr/trading-and-operations-update/9859148)). Cut by its 58.8 mmboe hedge book. The Rosebank consent risk (−5.0) is outside the window.
- **Bottom, MSLH −1.40:** the peer guidance cuts above ([Ibstock RNS](https://www.investegate.co.uk/announcement/rns/ibstock--ibst/q3-trading-update-/9851713)).

## Not ranked

- **TISG (it):** no event. Shares suspended by Borsa Italiana since 3 Nov "fino a nuova comunicazione" (until further notice) under a concordato preventivo that gives shareholders nothing; issuer calendar has no 18 Nov date (next board 23 Nov, H1 report 10 Dec). [eMarket STORAGE 2378-123-2026](https://www.emarketstorage.com/sites/default/files/comunicati/2026-11/20261116_192043.pdf).
- **ENH (no):** phantom. Issuer's own financial calendar on NewsWeb puts Q3 on **27.11.2026** ([message 685636](https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=685636)).

## The day, and what to discount

- **Selection:** random sample of 27 eligible above $100k/day, seed `eu-2026-11-18`; 47 scheduled; hunted 20: uk 8, no 5, pl 3, se 2, de 1, it 1 (fr, dk, fi, es 0). Eligible by market: uk 11, no 5, pl 4, de 2, se 2, fr 1, dk 1, it 1.
- **Market concentration:** largest market uk at 40%, 6 markets represented. Not one market's day, but the four panel shorts are three UK names plus one German, and three of them (MSLH, SDY, PFS0) share a construction/infrastructure capex exposure — a correlated bet the scorer cannot see.
- **`session_unresolved`:** PFS0, TISG, VOW, CLN, CPS, KGH, ELON, CTEC, ITH, MSLH, SDY were vendor-defaulted to bmo. The hunters settled PFS0, VOW, ELON, CTEC, ITH, MSLH, SDY as bmo from issuer timestamps, and CLN, CPS, KGH as **amc**.
- **Options:** null in all ten markets; Europe runs in the anchor-less regime (backtest ρ=+0.073, p=0.45 over 104 events).
- **Short registers:** the FCA, Bundesanzeiger, FI, Finanstilsynet (NO) and CONSOB registers read. **7 of 20 names carry `anchor_covered: true`** (CTEC, MSLH, SDY, SSE, SVT, WKP, PFS0); every other name read is a truncated zero, not a measured zero.
- **Spain/Poland:** 3 Polish names (CLN, CPS, KGH), 0 Spanish — no positioning anchor and no way to confirm or kill after the fact; their lean is the run-up, i.e. the free control. **Germany:** 1 name (PFS0), which also cannot reach `event_occurred: false`. Italy (TISG) cannot either.
- **`lean_vs_free_control_rho`:** the latest resolved Europe run on disk is 2026-10-16 (se 0.60 only); nothing resolved since, so no fresher per-market reading exists. The lean's weights are priors borrowed from the US runs, measured nowhere in Europe.
- **Estimated `history.basis`:** CLN, CPS, KGH, ELON, SVEAF_B, PFS0, TISG carry a cadence estimate — a scale, not a record of dates. Observed: the eight UK names (`observed_rns`) and five Norwegian (`observed_newsweb`).
- **Conviction floor:** no name is above 2.8. Over the whole US sample the sign was a coin flip below the floor.
- **Already public / new in release:** SSE, BLND, PEN pre-released the period (expect smaller moves); CTEC (first FY27 outlook), MSLH, PEN (2026 guide re-base), ITH (dividend guide) and WKP face a possible guidance change.
- **Language:** the Swedish and Polish passes carried load-bearing facts (ELON/SVEAF_B insider registers, Polish consensus and release timestamps, Italian suspension terms); the Norwegian and UK domestic passes added nothing beyond English.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
