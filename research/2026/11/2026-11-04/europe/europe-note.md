# Stage EU — Europe ranking for 2026-11-04 (Wed)

Sealed Tue 2026-11-03 ~14:45 UTC, about three hours before the European close (15:45
Amsterdam; Europe is on winter time). Every sealed spot and `run_up_20d_pct` is an
**intraday price, not a close**. The ranking key is `impact_sum`, read from
`edge-scores.json`'s `ranking_key`. The conviction floor is 2.8.

**No name clears the floor.** The largest are BUR and SOFF at +1.30 and TRN at −1.90.
Nineteen names were hunted and all finished their search (`search_complete`). **Four of
the nineteen had no release in the window** (EVK, BPE, TEN, TIT): the vendor date was
stale or wrong. They are not ranked. The four-model panel selected two names: **BUR long
(4 of 4 judges) and BSL short (3 of 4)**. This stage places no orders and reads no broker.

## Ranked

| # | ticker | market | session | impact_sum (key) | abs_move | p_up | impact_scaled | anchor | history | pre-released? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BUR | uk | sealed amc; **actually in-session**, 13:00 GMT 4 Nov | +1.30 | 7.0 | 54 | +0.56 | no | observed_rns | no |
| 2 | SOFF | no | bmo (07:00) | +1.30 | 5.0 | 57 | +0.70 | no | observed_newsweb | no |
| 3 | BOUV | no | bmo? → bmo (06:00) | +1.20 | 6.0 | 53 | +0.36 | no | observed_newsweb | no |
| 4 | ODF | no | amc (20:00 Oslo) | +0.60 | 5.0 | 55 | +0.50 | no | observed_newsweb | no |
| 5 | AKER | no | bmo? → bmo (07:00) | +0.55 | 3.5 | 54 | +0.28 | no | observed_newsweb | no (NAV computable from public prices) |
| 6 | PNDORA | dk | bmo? (calendar 11:00 CET) | +0.50 | 9.0 | 52 | +0.36 | yes | estimated | no |
| 7 | SAMPO | fi | bmo (08:30 EET) | +0.45 | 3.5 | 55 | +0.35 | no | estimated | no |
| 8 | LRE | uk | bmo (07:00) | +0.10 | 5.5 | 55 | +0.55 | yes | observed_rns | no |
| 9 | FRA | de | bmo (07:00) | −0.20 | 3.3 | 53 | +0.20 | no | estimated | **yes**, 26 Oct ad-hoc |
| 10 | BMW | de | bmo (~07:30) | −0.35 | 5.0 | 51 | +0.10 | yes | estimated | partly (Q3 deliveries 13 Oct) |
| 11 | CHEF | se | bmo (07:45) | −0.50 | 9.0 | 50 | +0.00 | no | estimated | **yes**, sales in the 7 Oct trading update |
| 12 | BSL | de | bmo? → bmo (~06:50) | −0.80 | 4.0 | 45 | −0.40 | no | estimated | **yes**, 29 Oct ad-hoc with a guide raise |
| 13 | BTRW | uk | bmo? → bmo (07:00) | −1.20 | 5.5 | 48 | −0.22 | yes | observed_rns | no |
| 14 | SNWS | uk | bmo (07:00) | −1.40 | 7.5 | 47 | −0.45 | yes | observed_rns | **yes**, FY "ahead" on 29 Sep |
| 15 | TRN | uk | bmo (07:00) | −1.90 | 6.0 | 46 | −0.48 | yes | observed_rns | **yes**, H1 trading 11 Sep |

`bmo?` marks a name sealed with `session_unresolved`. The hunter's `session_check` then
settled it from the issuer's own notice or release-time history. **BUR is the one session
error.** The baseline was sealed `amc` (close 11-04 → close 11-05). Burford's own notice
(RNS, 26 Oct, https://www.investegate.co.uk/announcement/rns/burford-capital-npv-di---bur/notice-of-3q26-results-results-call-details/9841689)
puts the release at 8:00am EST, which is 13:00 GMT and inside the London session. Its
`session_check` opens `bmo`, so `eu_resolve.py` will read close 11-03 → close 11-04. The
baseline was not revised.

Names likely to carry a guidance change (`new_in_release`): PNDORA (first 2027 margin
direction plus a strategic update), SNWS (first cost of going national), CHEF (it gives
a Q4 outlook every quarter), TRN (first results under the new CEO, plus a promised
regulatory update), BTRW (first update under the new CEO, against a FY27 completions
guide). Already pre-released: FRA, BSL, SNWS, TRN, and CHEF's sales. On the first
resolved European days those two facts decided the size of the move while the emitted
sizes barely differed.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their own `-intl-` agents, with no fallback, and each covered 15 of 15 names. One
caveat: the Sonnet 5.5 judge reported that it did not open the three hunter definitions
the packs name and read only the first 120 lines of `LESSONS.md`. Its sizes are scored as
returned.

The selection rule is `consensus_k` ≥ 3 of 4, each judge in its own top 20%. A judge's
top 20% starts at: Opus 5 |1.35|, Opus 5.5 |0.80|, Sonnet 5.5 |0.66|, Fable 5.1 |0.96|.
Each threshold comes from that judge's last 200 live sizes in this market.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BUR | amc (really in-session) | **yes** | 85 | long | 3 | 89L* | 80L* | 82L* | 86L* | 4 | +1.40 | +1.30 |
| 2 | BSL | bmo | **yes** | 85 | short | 4 | 88S* | 88S* | 84S* | 78S | 3 | −1.53 | −0.80 |
| 3 | BOUV | bmo | | 83 | long | 5 | 87L* | 77L | 88L* | 78L | 2 | +1.33 | +1.20 |
| 4 | SNWS | bmo | | 59 | short | 23 | 84S* | 58S | 22S | 72S | 1 | −0.90 | −1.40 |
| 5 | LRE | bmo | | 31 | long | 39 | 22S | 82L* | 50L | 13L | 1 | +0.42 | +0.10 |
| 6 | SOFF | bmo | | 60 | long | 15 | 78L | 64L | 37L | 62L | 0 | +0.83 | +1.30 |
| 7 | TRN | bmo | | 34 | short | 27 | 54S | 42S | 12L | 51S | 0 | −0.59 | −1.90 |
| 8 | ODF | amc | | 40 | long | 5 | 44L | 32L | 37L | 45L | 0 | +0.54 | +0.60 |
| 9 | AKER | bmo | | 41 | long | 15 | 65L | 41L | 28L | 28L | 0 | +0.46 | +0.55 |
| 10 | CHEF | bmo | | 23 | short | 36 | 52S | 32L | 15S | 58S | 0 | −0.43 | −0.50 |
| 11 | SAMPO | bmo | | 24 | long | 10 | 10L | 32L | 20L | 32L | 0 | +0.37 | +0.45 |
| 12 | BMW | bmo | | 8 | long | 21 | 27S | 25L | 15L | 20L | 0 | +0.27 | −0.35 |
| 13 | PNDORA | bmo | | 13 | short | 51 | 80S | 16S | 64L | 22S | 0 | −0.26 | +0.50 |
| 14 | BTRW | bmo | | 6 | long | 22 | 37L | 20S | 6S | 15L | 0 | +0.03 | −1.20 |
| 15 | FRA | bmo | | 0 | long | 26 | 3L | 4S | 37L | 37S | 0 | −0.02 | −0.20 |

**BUR (selected, long, 4 of 4).** Burford's fair-value policy requires it to mark up Q3's
two milestones: the ICC Cameroon award (24 Jul) and the Taction v Apple $5.7bn verdict
(25 Sep, about $700m on balance sheet). The 2Q26 10-Q's own milestone factors (5–40%
before trial judgment, 25–60% at a judgment or award) imply an unrealized gain of tens to
low hundreds of $m. The bar is $0.09 EPS (about $20m), seen only in search snippets and
probably stale
(https://www.sec.gov/Archives/edgar/data/1714174/000171417426000097/bur-20260630.htm).
**The strongest case against:** the gain is non-cash and every input is public. The stock
rose 13.6% in the five sessions to the seal. Burford's results days have mostly been sold:
5 of the last 7 two-day windows were negative, including −10.45% on the 2025 results. All
four judges and the hunter sized it on the in-session window, not the sealed amc one.

**BSL (selected, short, 3 of 4; Fable 5.1 was just outside its own top 20% at 78).**
Basler's 9-month numbers and a third guide raise went out in the 29 Oct ad-hoc
(https://www.eqs-news.com/news/ad-hoc/basler-ag-preliminary-9-month-result-again-increase-of-forecast-2026-after-continued-high-incoming-orders-and-strong-results/24df783a-623e-4ad0-8689-110bd3ecf6b5_en).
That leaves two things for 4 Nov. The first is the unquantified "positive one-time
effects" inside the 22.5% margin. The second is a pattern: all three earlier
confirmation days after a pre-release closed lower (−3.07%, −2.11%, −1.08%). The stock is
also +14.25% over five sessions. **The strongest case against:** a backlog €51m ahead of
sales and the sensor plant back to full output could point the call toward the top of the
range. The hunter itself was only −0.80, below the panel's read. And this is a confirmation
report, so a 4.0% move may be generous.

**Where the panel and the hunter disagree most:**
- **PNDORA**: the hunter is +0.50, the panel −0.26 short. Opus 5 is at 80S on the 2027
  margin floor, and Sonnet 5.5 is 64L. This is the widest spread of the day (sd 51).
- **BTRW**: the hunter is −1.20, the panel +0.03. The judges let the crowded, building
  9.13% short and four straight up-days on updates offset the weak fundamentals.
- **TRN**: the hunter's most negative name (−1.90) gets a panel_pct of only 34. Sonnet 5.5
  even reads it as long.
- **BMW**: the hunter is −0.35, the panel +0.27. Both are near zero.

No name is above the floor, so there is no "above the floor but not selected" case.

**What the numbers are not.** `panel_score` ranks; it does not forecast. There is no
`expected_edge_pct` off the US. Certainty (`p_up`) is recorded and decides nothing. In the
four-model re-judge the judges ranked Europe better than the live hunt (ρ +0.33/+0.34 on
48 names) but Japan and Australia worse, so nothing about this market's panel is
established.

## Top and bottom of the key

- **Top, BUR / SOFF +1.30.** BUR is as above. SOFF's largest finding (+0.6, capital return)
  is the rising dividend path (USD 0.05, 0.05, 0.10, 0.15) with the cash constraint removed
  (https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=678191). The finding
  behind its +0.4: neither SOFF nor its 27.3% associate SOMA has issued the guidance cut
  both filed before last year's Q3.
- **Bottom, TRN −1.90.** These are the first results under the new CEO, Ian Brown. FY28
  consensus still grows on every line, while the company says UK headwinds run into H2
  (−1.2,
  https://trainlinegroup.com/investors/shareholder-centre/analyst-consensus). The company
  has also promised a "fuller update on the regulatory landscape" against a GBR Retail Code
  it says "requires further strengthening" (−0.8,
  https://www.investegate.co.uk/announcement/rns/trainline--trn/statement-regarding-draft-retail-code-of-practice/9815600).
  A 4.98% short that is still building pulls the other way (+0.4).

## Not ranked

- **EVK**: Evonik published Q3 on **2026-11-03** before the open
  (https://www.evonik.com/en/news/press-releases/2026/11/Q3-2026.html). The vendor's
  11-04 date is last year's date carried forward.
- **TIT**: TIM moved its Q3 board meeting from 4 Nov to **10 Nov** on 2026-10-06
  (https://www.borsaitaliana.it/borsa/notizie/teleborsa/finanza/tim-sposta-cda-su-trimestrale-al-10-novembre-227_2026-10-06_TLB.html?lang=it).
- **TEN**: Tenaris releases **after the close** on 4 Nov
  (https://ir.tenaris.com/events-and-presentations), so the reaction is 11-05, outside the
  sealed bmo window.
- **BPE**: BPER's board meets 4 Nov and the release follows on **5 Nov ~07:00 CET**
  (calendar,
  https://www.emarketstorage.it/sites/default/files/comunicati/2026-08/20260806_187988.pdf;
  call invitation, 27 Oct).
- **SOLAR_B**: shed before hunting. Solar's own calendar dates its Q3 to 3 Nov, and the
  2026-11-03 run already hunted it. Today's row came from one source with no time.

**Five of the twenty drawn names were not 4-Nov bmo/amc events as the calendar said.**
Three of the five are Italian. Italy's `event_occurred: false` is unreachable, so the
resolver could never have caught these. The hunters caught them.

## The day, and what it is not

- **Selection**: `random sample of 64 eligible, seed 'eu-2026-11-04'`. 102 scheduled, 64
  eligible above the **$100k/day** floor, 20 drawn at random. By market: uk 5, de 4, no 4,
  it 3, dk 2, se 1, fi 1. Eligible by market: uk 11, de 10, se 14, dk 5, no 12, fi 4,
  it 6, es 2. **`market_concentration`**: the largest market is the UK at 25%, with 7
  markets represented. That is a spread day, not a one-market day.
- **Calendar sources**: TradingView, plus the UK RNS calendar (read; it added LRE among
  others), the EQS events calendar for DE, Euronext Oslo for NO, and Inderes and the Nasdaq
  Nordic financial calendar for FI/SE/DK. **Yahoo's calendar was unavailable for all ten
  markets**, and bankier (PL) returned 403.
- **Options are null in all ten markets.** Europe runs in the anchor-less regime that
  produced ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
- **Short registers**: de, dk, fi, it, no, se and uk all read (es and pl have none). **7 of
  the 20 sealed names carry `anchor_covered: true`** (BMW, BTRW, EVK, LRE, PNDORA, SNWS,
  TRN), and **6 of the 15 ranked names do**. Every other zero is the 0.5% truncation (0.1%
  in Denmark), not a measurement. Correction: the run log's "8/20" was a miscount.
- **Spain and Poland: 0 names.** Germany: 4 names (BMW, BSL, EVK, FRA), for which
  `event_occurred: false` can never be reached. Italy's three can't reach it either, and
  all three turned out to have no event in the window.
- **`lean_vs_free_control_rho`**: no European run has resolved since 2026-10-16. Its only
  per-market reading is se 0.60. **The Nordic rows of 10-19 → 10-23 are past the ~12-day
  feed window.** Resolve this run by ~2026-11-12.
- **The lean's weights are priors borrowed from the US runs**, measured nowhere in Europe.
- **Estimated `history.basis`** (a scale, not a record of dates) applies to BMW, BSL, FRA,
  PNDORA, SAMPO and CHEF among the ranked names. Only UK (`observed_rns`) and Norwegian
  (`observed_newsweb`) histories are real. The SAMPO hunter found that several of its
  estimated dates were not print days: the median absolute move on real report dates is
  2.7%, against the baseline's 1.45%.
- **Conviction floor**: none above 2.8. Over the whole US sample the sign was a coin flip
  below it.
- **`language_note`, where it mattered**: TIM's date change was only in the Italian
  Teleborsa item. BPER's release time came only from the Italian archive timestamps.
  Knowit's "Norge utvecklas starkt" (BOUV's peer read) was only in Swedish. BMW's CFO line
  "Unsere aktuelle Planung ist eher konservativ" and the early close of its severance
  programme were only in German. Fraport's underlying EBITDA miss was stated outright only
  by dpa-AFX in German. Elsewhere the notes read "nothing the English sources did not
  already carry", which is the expected Nordic answer.
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
