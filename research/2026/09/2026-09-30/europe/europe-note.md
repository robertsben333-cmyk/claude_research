# Stage EU — Europe ranking for Wednesday 2026-09-30

Sealed Tue 2026-09-29, 13:40–13:45 UTC, while the European markets were **still trading**.
Every sealed spot and run-up is an **intraday price, not a close**. The realised move is
measured from daily bars by `eu_resolve.py`, never from the sealed spot.

## Answer first

**Nothing clears the conviction floor of 3.0 points, and four of the ten names have no
event in the window at all.** The largest key is SAGA at +1.10. Across the whole US
sample the sign was a coin flip below the floor. The ranking key is `impact_sum`, as
`edge-scores.json` reports it.

| # | name | market | session | `impact_sum` | pre-lessons | `abs_move_pct` | `p_up` | lean | anchor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SAGA Saga | uk | bmo (07:00 pattern, issuer calendar) | **+1.10** | +1.2 | 7.5 | 57 | +0.86 | **FCA 2.72%, +0.40pp building** |
| 2 | GXI Gerresheimer | de | in-session (15:00 CEST call) | **+0.50** | +0.7 | 6.0 | 54 | +3.18 | **BAnz 5.38%, −0.09pp** |
| 3 | AVG Avingtrans | uk | bmo (issuer notice) | **0.00** | 0.0 | 4.5 | 52 | −0.00 | truncated zero |
| 4 | PINE Pinewood | uk | bmo (issuer notice) | **0.00** | 0.0 | 0.4 | 52 | +3.56 | FCA 4.88%, −0.29pp |
| 5 | SPI Spire Healthcare | uk | bmo (07:00 pattern) | **0.00** | 0.0 | 0.3 | 50 | +1.20 | FCA 2.23% |
| 6 | SKIS_B SkiStar | se | bmo (issuer invitation, 07:00 CEST) | **−0.50** | −0.6 | 5.5 | 45 | +0.19 | truncated zero |
| — | ADE Bitcoin Group | de | **released 09-29 09:00 CEST** | not ranked | 0.0 | 2.5 | 50 | −0.26 | truncated zero |
| — | DEBS boohoo / Debenhams | uk | likely no release (interims in Nov) | not ranked | 0.0 | 3.0 | 50 | +0.39 | FCA 1.77% |
| — | DIB Digital Bros | it | **released 09-24 evening** | not ranked | 0.0 | 2.0 | 50 | −0.30 | truncated zero |
| — | KOF Kaufman & Broad | fr | **amc 1 Oct** per issuer | not ranked | 0.0 | 1.5 | 50 | +1.04 | AMF 0.68% |

**Top name, SAGA (+1.10).** The half is only partly pre-released. The 30 Jun AGM update
gave direction but no profit figure, and the FY26/27 outlook is still qualitative
("take a further step forward"). Saga has raised or beaten at each of its last three
scheduled releases: +6.68%, +15.21% and +6.01% on the day.
- **+0.8, guidance:** a firmed or raised outlook, supported independently by Carnival's
  record deposits and raised guide on 09-29
  (<https://www.prnewswire.com/news-releases/carnival-corporation-outperforms-guidance-delivering-best-ever-revenues-net-yields-and-net-income-302892070.html>).
  Base source: <https://www.investegate.co.uk/announcement/rns/saga--saga/agm-trading-update/9642963>.
- **+0.3, fuel hedge:** 100% hedged for FY27, yet the stock fell with unhedged US cruise
  lines on oil days in September. This is an inference.
- **Against it:** a ~5% jump at 10:30 BST on 09-29 with no RNS and no news found, which
  raises the entry price. The bar rests on one broker (Berenberg, +24% FY27 PBT), so
  the sizes are capped.

**Bottom name, SKIS_B (−0.50).** The FactSet dividend consensus of 3.53 SEK (+18%) sits
above the board's record of +0.20 SEK a year. SkiStar fell short of the FactSet dividend
at both of the last two year-ends (2.80 against 3.12, then 3.00 against 3.23), and the
stock fell 3.0% and 4.8% on those days. The bar is FactSet via Börsvärlden, 2026-09-28.
Findings:
- **−0.7, dividend:** the hunter expects 3.20–3.40 SEK.
- **+0.4, group winter bookings:** only Sälen's +10% has been published since June.
- **−0.2, Q4 sales:** the 276 MSEK consensus looks to assume property sales that have
  not happened.

The stock is −7.7% since 26 Aug with no cause found, so part of it may be priced.

**GXI (+0.50) is the one name whose release carries genuinely new numbers into the
window.** The Q1 statement's numbers were pre-released on 27 Aug. The Q2/H1 preliminary
numbers were never disclosed, and the issuer's IR calendar lists them for 30 Sep with a
15:00 CEST call. The sole finding: Active Ownership Opportunities, closely associated
with supervisory board member Röhrig, bought about €12.4m on Xetra between 1 and 11 Sep,
inside the pre-results window. The stock has since fallen below every purchase price.
Source: <https://www.eqs-news.com/news/directors-dealings/gerresheimer-ag-active-ownership-opportunities-scs-buy/70d696e1-ccc2-4f27-975d-15e0b4b56d50_en>.
The finding agrees with the lean, which is short-register driven, so it was trimmed.

## Four names have no event in the window, and three of them need a kill at resolve

- **ADE, Bitcoin Group.** The Halbjahresbericht (half-year report) was published on
  **2026-09-29 at 09:00 CEST**, before the seal.
  Source: <https://www.eqs-news.com/de/news/corporate/bitcoin-group-se-veroeffentlicht-halbjahresbericht-2026-fokus-auf-neustart-von-bitcoin-de-mit-deutlich-erweitertem-produktangebot/7ec15645-32ab-4b1a-9b63-30f38cd47469_de>.
  Germany cannot reach `event_occurred: false` automatically, so **amend the baseline
  by hand at resolve**, with that URL as `event_occurred_note`.
- **DIB, Digital Bros.** FY2026 was released on the **evening of 2026-09-24**, per
  Teleborsa: "ieri sera Digital Bros ha annunciato risultati annuali molto solidi"
  ("last night Digital Bros announced very solid annual results").
  - Source: <https://www.borsaitaliana.it/borsa/notizie/teleborsa/finanza/digital-bros-tp-icap-midcap-alza-target-price-nonostante-taglio-delle-stime-59_2026-09-25_TLB.html?lang=it>
  - The issuer's calendar has nothing on 30 Sep.
  - Italy is `universal: False` and Digital Bros does not appear to file on eMarket
    STORAGE, so this also needs a **hand amendment**.
- **KOF, Kaufman & Broad.** The issuer's H1 release of 2026-07-08 says "jeudi 1er
  octobre 2026 : Publication des résultats des neuf premiers mois 2026 (après Bourse)"
  ("Thursday 1 October 2026: publication of the nine-month 2026 results, after market").
  - Source: <https://newsroom.kaufmanbroad.fr/actualites/resultats-du-1er-semestre-2026-0c62d-72211.html>
  - An older agenda page still says 30 Sep, also after the close.
  - The first reacting session is 2 Oct on the July release, or 1 Oct if the April page
    is right. The sealed bmo window holds neither.
- **DEBS, boohoo / Debenhams Group.** The H1 trading update already went out on 17 Sep:
  <https://www.investegate.co.uk/announcement/rns/boohoo-group--debs/trading-update-for-the-six-months-ended-31-august/9776260>.
  - No Notice of Results has appeared.
  - Fidelity UK lists half-year results for Nov 2026, and last year's interims were
    on 27 Nov.
  - A non-executive director bought shares on 17 Sep. That purchase would fall inside a
    MAR closed period if the interims were on 30 Sep.
  - This is a **probable phantom, not a confirmed one**. The UK archive can confirm or
    kill it at resolve.

So the vendor calendar produced **4 of 10 rows without an event in the window** today,
against the 2 of 90 measured on UK RNS. Three of the four are outside the UK, where the
vendor's forward dates were already known to be sparse and stale.

## Two of the six ranked names are pinned by a cash offer

- **PINE:** a 448p scheme. Approved 99.76% on 25 Sep, court hearing 7 Oct, spot 0.4%
  under the offer.
- **SPI:** a 250p final offer, with Rule 4.2(c) barring a raise. Vote on 30 Oct, and the
  stock has sat at 245.0–246.5p since 7 Sep.

Both keys are 0 with `abs_move_pct` under 0.5%. **Their baseline leans (+3.56 and +1.20)
are short-squeeze terms that cannot operate under a cash cap.** That is a lean defect
worth remembering when `lean_vs_free_control_rho` is read for this day.

The SPI hunter also reports that the baseline dates the 2025 interims to 2025-08-07,
where Investegate shows the Half-year Report at 07:00 on 2025-07-31. One reaction-history
row may therefore be measuring the wrong day. This is unverified here.

## Selection and instrumentation

- **Funnel:** 41 scheduled → 10 eligible above $200k/day → 10 hunted.
  `selection.method`: "all 10 eligible names (at or under the cap)", so no random draw
  was needed (seed `eu-2026-09-30` unused).
  - `by_market`: uk 5, de 2, fr 1, se 1, it 1; dk/no/fi/es/pl 0.
- **`market_concentration`: the UK is 0.50 of the day across 5 markets.** It is 3 of the
  6 ranked names.
- **Options:** `options` is null for all ten names. Europe runs in the anchor-less regime
  that `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events.
- **Short registers:** read for uk (as of 09-28), de (09-28), fr (09-25), it (09-28) and
  se (09-28).
  - **`anchor_covered: true` on 6 of 10:** DEBS, GXI, KOF, PINE, SAGA and SPI.
  - The other four are truncated zeros, not measurements.
- **Spain and Poland: 0 names today.** **Germany: 2 names (ADE, GXI)**, and
  `event_occurred: false` is unreachable for both automatically. Italy and France cannot
  reach it either.
- **`session_unresolved`:** sealed on 8 of 10 (all except PINE and SKIS_B). The hunters
  settled every one, as shown in the table above. GXI releases in-session, so the
  close(09-29) → close(09-30) window holds it.
- **`history.basis`:** it is `observed_rns` for the five UK names. It is an
  **estimated cadence** for ADE, GXI, KOF, DIB and SKIS_B, which is a scale and not a
  record of dates. ADE and DIB are exactly the failure that reading a cadence as evidence
  produces.
- **`lean_vs_free_control_rho`:** the previous resolved runs read 0.69 (09-22), 0.943
  (09-23) and 0.70 (09-24), and 09-25 carries none. No later run has resolved. The
  lean's weights are priors borrowed from the US runs and have been measured nowhere in
  Europe.

## What each release carries (`already_public` / `new_in_release`)

- **Pre-released periods:**
  - **AVG:** FY26 profit "in line" on 24 Jun. Only the first FY27 statement and the
    31 May net debt are new.
  - **GXI:** the Q1 numbers came out on 27 Aug. The Q2/H1 preliminary numbers are new.
  - **SAGA:** direction only, from the 30 Jun AGM update. The profit figure is new.
- **New numbers with a live guide question:**
  - **SAGA:** the FY outlook, and whether it gets firmed or raised.
  - **SKIS_B:** the full-year result, the dividend and the group booking status.
  - **GXI:** whether the FY guide is reiterated.
- **Irrelevant to price:** PINE and SPI, both under cash offers.

## `language_note` highlights (prose, not ranked)

- **GXI:** only the German press (boersennews) noted that the mandatory notice names
  just the Q1 statement while the IR calendar adds Q2/H1 preliminary numbers. The same
  press reads the absence of a Prognose ad-hoc (forecast update) since June as positive.
  It also carried an AI-generated "870 Mio. bis 30. September" (€870m due by
  30 September) refinancing story, which the April ad-hoc shows to be a misreading.
- **DIB:** only the Italian Teleborsa coverage carried the release timing ("ieri sera",
  last night) and the pre-print bar.
- **SKIS_B:** only the Swedish sources carried the Sälen +10% release, the FactSet
  dividend table and the dividend-miss record.
- **KOF:** the French issuer pages settled the date conflict.
- **UK names:** the RNS record settled the dates and the holder changes. The domestic
  trade press added nothing.

## What this is and is not

One day is not a result. It has six ranked names, none above the floor, two of them
pinned by cash offers, and half the day from one market.

**Resolve plan:**
- The bmo names from 2026-10-01.
- GXI and SKIS_B within a week. SkiStar is Nordic, so its print is only confirmable
  inside the feed's ~12-day window.
- Amend ADE and DIB by hand to `event_occurred: false`, with the URLs above.

No orders were placed or considered. This stage reads no broker.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
