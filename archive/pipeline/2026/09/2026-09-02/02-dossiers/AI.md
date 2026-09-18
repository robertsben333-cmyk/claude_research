# AI — C3.ai, Inc.

**Event confirmed: TRUE.** C3.ai's own press release (Businesswire, 2026-08-20) states results for the fiscal
first quarter ended **July 31, 2026** will be issued **following the close of U.S. markets on Wednesday,
September 2, 2026**, with the call at 2:00 p.m. PT / 5:00 p.m. ET [1]. Directly fetched from the primary
source. Note a live vendor discrepancy: TipRanks and several aggregators still list **September 9, 2026** as
the expected date [12][30] — that is an algorithmic estimate contradicted by the company's own filing-grade
announcement, and it should be disregarded.

**What this print is about.** This is the first full quarter (May–July 2026) run entirely under Tom Siebel's
restored leadership and his rebuilt go-to-market, after FY26 collapsed — revenue −35.7% to $250.3M, a GAAP
operating loss of $498.5M, and RPO down 13.6% to $203.1M [7][26]. Siebel's diagnosis was explicit and
falsifiable: the collapse was *sales execution*, not product, churn or demand, and the fix was widening the
target account list from 100–150 per region to roughly 1,000 [17][19]. Q1 FY27 is the first data point on
whether that fix is working. Crucially, the last print showed that beating EPS and revenue is not enough:
Q4 FY26 beat on both and the stock still closed −1.21%, because **bookings came in light** and DA Davidson
reiterated Underperform the next morning [24][23]. So this trades on bookings/RPO and on whether the
$210–240M FY27 revenue frame survives — not on the headline loss per share. Meanwhile the setup is unusually
tense: 34.65% of the float is short with 9.65 days to cover [10], options price a ~13.6% move [3], and the
consensus price target ($8.82) sits **14.7% below** the current $10.34 spot [21].

---

## 1. Event & anchors

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Event date | 2026-09-02 | confirmed 2026-08-20 | [1] |
| Session | **amc** ("following the close of the U.S. markets") | — | [1] |
| Call time | 2:00 p.m. PT / 5:00 p.m. ET | — | [1] |
| Fiscal period | Q1 FY2027, quarter ended 2026-07-31 | — | [1] |
| Pre-announcement this quarter? | **No.** The 2026-08-20 release was date-only, no preliminary figures | 2026-08-20 | [1] |
| Spot | **$10.34** (close, −4.44% on the day) | 2026-09-01T20:00:02Z | [2][21] |
| Market cap | **$1.61B** (155.45M shares out) | 2026-09-01 | [21][10] |
| Enterprise value | $1.09B | 2026-09-01 | [10] |
| 52-week range | $7.68 – $20.22 | 2026-09-01 | [21] |
| **Event-implied move** | **±13.64%** (weekly, Sep-04-2026 expiry — first expiry after the print) | fetched 2026-09-02 | [3] |
| Implied move (corroboration) | ~13.49% cited 2026-08-31 · `snippet_only` | 2026-08-31 | [4] |
| Implied move (monthly) | ±16.25% (Sep-18-2026 expiry) | fetched 2026-09-02 | [3] |
| Sep-04 weekly call IV | **179** | 2026-09-01 | [5] |
| Sep cycle IV | **100**, vs 52-week IV range 51–108 | 2026-09-01 | [5] |
| **IV rank (derived)** | **≈86** — my calculation: (100−51)/(108−51) | 2026-09-01 | derived from [5] |
| 20-day realised vol (ann.) | 49.9% — my calculation from daily closes | to 2026-09-01 | derived from [2] |
| Beta (5Y) | 2.09 | 2026-09-01 | [21] |
| Avg 30-day volume | 4.74M shares — my calculation | to 2026-09-01 | derived from [2] |

**Cross-check on the implied move (my own arithmetic, stated as inference):** a 179 IV on the Sep-04 weekly
with ~2 calendar days to expiry implies √(2/365) × 1.79 ≈ **13.2%** — which independently reconciles with
OptionSlam's 13.64% straddle read [3][5]. Two methods and two vendors agree, so I treat ~13.5% as a solid
anchor rather than a snippet artefact.

### Realised one-day earnings moves (close before → close after)

Computed by me from Yahoo Finance daily closes pulled via the chart API on 2026-09-02 [2]. The 2026-06-03
figure independently matches OptionSlam's own record ($10.71 → $10.58, −1.21%) [3], which validates the method.

| Report date (amc) | Quarter | Close before | Close after | Move |
| --- | --- | --- | --- | --- |
| 2024-12-09 | Q2 FY25 | 41.68 | 41.73 | **+0.12%** |
| 2025-02-26 | Q3 FY25 | 26.44 | 23.88 | **−9.68%** |
| 2025-05-28 | Q4 FY25 | 23.02 | 27.80 | **+20.76%** |
| 2025-09-03 | Q1 FY26 | 16.68 | 15.46 | **−7.31%** |
| 2025-12-03 | Q2 FY26 | 15.01 | 15.32 | **+2.07%** |
| 2026-02-25 | Q3 FY26 | 10.31 | 8.40 | **−18.53%** |
| 2026-06-03 | Q4 FY26 | 10.71 | 10.58 | **−1.21%** |

- **Up/down pattern: 3 up / 4 down over 7 quarters** (2 up / 4 down over the last 6).
- Mean |move| = **8.53%** · Median |move| = **7.31%** · Max |move| = **20.76%** (7 quarters).
- Last 6 only: mean |move| = 9.93%, median = 8.50%.
- **My inference:** the 13.6% implied move is priced ~1.6× the 7-quarter mean realised move and ~1.4× the
  6-quarter mean. Options look *rich versus the central tendency* but not versus the tails (−18.5%, +20.8%),
  which is exactly what you would expect for a name where the distribution is bimodal rather than fat-normal.
  The vol premium is also stark against 49.9% realised: the Sep cycle is marked at 100.

**Corroborating narrative on the two tail events:** the −18.53% on 2026-02-26 was the quarter C3 AI cut 26%
of its workforce and guided down [25]; the +20.76% on 2025-05-29 followed the Q4 FY25 report. Both prove the
name is capable of a 2× implied-move day in either direction.

---

## 2. The bar

| Metric | Consensus | Company guidance | Gap |
| --- | --- | --- | --- |
| Q1 FY27 revenue | **$51.46M** (−26.8% YoY) [6][20] | **$50.0–54.0M** (mid $52.0M) [7][8] | Street sits ~1% *below* the guide midpoint |
| Q1 FY27 non-GAAP EPS | **−$0.26** (loss widens 29.7% YoY) [6][20] | not guided on EPS | — |
| Q1 FY27 subscription revenue | $48.28M (−19.9% YoY) [6] | — | 94% of total |
| Q1 FY27 professional services revenue | $3.07M (−69.2% YoY) [6] | — | — |
| Q1 FY27 subscription gross margin | 27.9% (vs 31.0% LY) [6] | — | Street models further compression |
| Q1 FY27 non-GAAP operating loss | — | **$(40.5)–(48.5)M** [7][8] | — |
| FY27 revenue | $224.31M (−10.4% YoY) [21] | **$210–240M** [7][8] | Street essentially at the midpoint |
| FY27 non-GAAP EPS | −$0.79 [21] | non-GAAP op loss $(128)–(160)M [7][8] | — |

**Revisions.** The Zacks consensus EPS estimate for the quarter is **unchanged over the past 30 days**,
reported consistently across multiple dated Zacks/Yahoo pieces [6][20][29]. Zacks Rank **#3 (Hold)** [6].
60-day and 90-day revision detail could not be sourced — see coverage gaps. My inference: unchanged estimates
into a print for a company whose revenue has fallen 35.7% is not a sign of stability so much as a sign that
the sell side has stopped modelling upside and is simply parroting the guide.

**Ratings and price-target setup — this is the sharpest single fact in the dossier.**
- 14 analysts. Consensus rating **Sell**. Average price target **$8.82**, i.e. **14.7% below the $10.34
  spot** [21]. Breakdown: 1 Strong Buy / 0 Buy / 7 Hold / 3 Sell / 3 Strong Sell [21]. Target range $6–$15 [22].
- Most recent actions: **D.A. Davidson (Lucky Schreiner), Sell, $7 — dated 2026-09-01, the day before the
  print** [21]. Bank of America (Koji Ikeda), Sell, $8, 2026-07-22 [21]. Wedbush (Daniel Ives), Buy, $15,
  2026-06-04 [21]. An earlier cut of the consensus on 2026-08-11 showed a Hold consensus and a $10.78 target
  across 9 analysts (`snippet_only`) [22] — the drift from ~$10.78 to $8.82 in three weeks is downward.

**Whisper number.** No credibly published whisper number found. Marked `unavailable`.

**What the company has to deliver just to hold the stock flat — my inference.** Given the Street is *below*
the guide midpoint on revenue, an in-line revenue print is close to free. The bar that matters is therefore
not the P&L: it is (a) RPO that stops falling, ideally up sequentially from $203.1M, (b) bookings commentary
that is at minimum not "lighter than expected," which is precisely what sank the last print [24], and
(c) reaffirmation of the FY27 $210–240M revenue frame. Fail any of those three and the run-up of the last
five weeks (+12.6% off the 2026-07-31 close of $9.18 [2]) is the first thing to go.

---

## 3. The one metric that matters

**Bookings, and behind it RPO.** Not EPS, not revenue.

The evidence that this is the trading metric, not my guess:

1. **The last print is a controlled experiment.** Q4 FY26 (2026-06-03) beat on EPS (−$0.33 vs −$0.38) *and*
   on revenue ($51.6M vs $50.13M) and *also* beat its own non-GAAP operating loss guidance [7][14]. The stock
   still closed down 1.21% [2][3]. The next morning D.A. Davidson reiterated Underperform with a $7 target
   citing specifically that "bookings for the quarter came in lighter than analysts anticipated" and "an
   elongated timeline for business trends to improve" [24]. One contemporaneous summary described the quarter
   as "an impressive beat of analysts' adjusted operating income estimates but a significant miss of analysts'
   billings estimates" [30].
2. **Management framed the whole turnaround in these terms.** Siebel on the Q4 call: the fix "fixes revenue
   growth. It fixes RPO. It fixes… cash generation," and the cause was "basically sales execution" [17].
   The company attributed the RPO deterioration to sales execution rather than product, churn or demand [26].
3. **RPO is disclosed and is falling.** RPO was **$203.1M at 2026-04-30, down 13.6% YoY**, comprising $36.4M
   of deferred revenue and $166.7M of non-cancellable contract commitments [26].

**What the market expects for it.** No published consensus RPO or bookings estimate could be sourced — this
is a genuine gap and it matters, because it means the bar is set by narrative rather than a number. What is
sourceable about the shape of the expectation:
- Q4 FY26 activity level: **28 agreements signed**, including 9 new Initial Production Deployments and 7 IPD
  conversions; **417 cumulative IPDs signed, 251 still active** [26][17].
- FY26 Federal/Defense/Aerospace bookings were **+17% YoY and 41% of total bookings** [26]; in Q2 FY26
  federal bookings were **+89% YoY** [16]. Federal is the one part of the book that has been growing, so the
  federal bookings line is where a positive surprise would have to come from.
- **My inference on the specific bar:** RPO needs to print above roughly $203M — i.e. flat-to-up sequentially
  — for the bull case to survive contact with the release. A third consecutive double-digit YoY RPO decline
  makes the "sales execution is fixed" thesis untestable for another quarter, and that is the scenario where
  the 13.6% implied move gets used to the downside.

---

## 4. Fundamentals — what changed, what is at stake

**FY26 (ended 2026-04-30), the year that broke the model** [7][14][27]:
- Total revenue **$250.3M**, down from $389.1M — **−35.7%**. Subscription $227.1M (91% of total).
- GAAP operating loss **$(498.5)M**; GAAP net loss **$(470.4)M**; GAAP EPS **−$3.35**; non-GAAP EPS **−$1.35**.
- GAAP gross margin **31%**, non-GAAP **46%**.
- **Free cash flow −$192.1M** for the year.

**Q4 FY26 specifically** [7][14][17]:
- Revenue $51.6M (−53% YoY [26]); subscription $48.4M = **94% of total**.
- GAAP gross margin collapsed to **22%**, non-GAAP 37%. (Q3 FY26 GAAP gross margin had already fallen to 17%
  from 59% a year earlier on surging subscription cost of revenue [25].)
- Non-GAAP operating loss $(54.4)M — *better* than the guided $(56)–(64)M range.
- Q4 free cash flow **−$54.8M** [17].

**What changed since the last print:**
- **Cost base.** Headcount cut ~35%, from ~1,070–1,075 in January 2026 to **~700**; roughly **$130M of the
  $135M** targeted annual savings already realised, with the balance landing in **2H FY27** [17][7][19].
  Restructuring charges of $10.8M (severance and WARN Act) were taken [7].
- **Go-to-market.** Target account universe widened from 100–150 per region to ~1,000 [17][19].
- **Leadership.** Siebel resumed CEO effective 2026-05-08 and remains Chairman; Stephen Ehikian, CEO from
  2025-09-01, moved to President [13][9]. The CEO successor search announced 2025-07-24 [9] has had no public
  update since Siebel's return, and succession was not discussed on the Q4 call [17].
- **Commercial proof points.** Shell expanded its C3 AI Reliability deployment on **2026-06-04** across a
  program monitoring 13,000+ pieces of equipment, adding agent-based root-cause analysis [18]. On
  **2026-08-10** Forrester named C3 AI a Leader in *The Forrester Wave: AI Platforms, Q3 2026*, with the
  **highest score in current offering of all 15 providers evaluated** [15]. The stock closed +1.76% on the
  Forrester news (2026-08-07 close $10.22 → 2026-08-10 close $10.40, my calculation [2]).

**Balance sheet — this is the bull case's floor** [7][10]:
- **Cash and investments $673M as of 2026-06-03**, which includes **$68.7M of net proceeds from Siebel
  personally purchasing 6,170,000 shares at $11.16** [7]. Separately reported: cash and equivalents $575.45M,
  total debt $58.68M, EV $1.09B [10].
- **My inference:** against FY27 guided non-GAAP operating loss of $(128)–(160)M, that cash implies roughly
  four years of runway on the non-GAAP measure and comfortably more than two years even on FY26's much
  heavier $192M GAAP-basis free cash burn. There is no financing cliff in the next several quarters. The
  market cap of $1.61B against $673M of cash and investments means roughly 42% of the equity value is cash,
  and EV/FY27-revenue-guide-midpoint ($1.09B / $225M) ≈ 4.8×.

**Customer concentration.** The FY26 10-K explicitly flags reliance on a limited number of customers for a
substantial portion of revenue as a material risk, alongside risks from the CEO transition, the workforce
reduction and the restructuring plan [27]. Baker Hughes has historically been the anchor joint-venture
relationship, renewed and amended four times since 2019 [28].

**Buyback/dilution.** No share repurchase programme found. Shares outstanding 155.45M [21]; the FY26 GAAP net
loss included substantial stock-based compensation implied by the $3.35 GAAP vs $1.35 non-GAAP EPS gap [7] —
i.e. ongoing dilution rather than buyback. Precise SBC dollar figure not sourced.

---

## 5. Positioning & options

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Shares short | **48.14M** | latest settlement per vendor | [10] |
| % of float | **34.65%** | " | [10] |
| % of shares outstanding | 30.97% | " | [10] |
| **Days to cover** | **9.65** | " | [10] |
| Prior-month short interest | 44.42M shares — **short interest rising +8.4%** | " | [10] |
| Alternate SI read | 32.43% of float as of the 2026-08-03 close · `snippet_only` | 2026-08-03 | [11] |
| Borrow fee | **0.3658% annualised**, 1.0M shares available (Interactive Brokers) · no timestamp published | undated | [31] |
| OI put/call ratio | **0.45** · `snippet_only` | recent | [32] |
| Call:put *volume* into the print | **1.6 : 1** | 2026-09-01 | [5] |
| Sep-04 weekly IV / Sep cycle IV | **179 / 100** (52-wk IV range 51–108) | 2026-09-01 | [5] |

**Term structure.** The front weekly at 179 against a Sep cycle at 100 and 20-day realised at 49.9% is a
textbook single-event vol kink: essentially all of the front-week premium is the September 2 print. There is
no meaningful vol bid past the event.

**Skew.** 25-delta put/call skew could not be sourced — MarketChameleon returned HTTP 503 and Fintel returned
HTTP 403. This is a real gap; see coverage gaps.

**Run-up into the print** (my calculations from daily closes [2], all measured to the 2026-09-01 close of
$10.34):

| Window | From | Change |
| --- | --- | --- |
| 5 sessions | 2026-08-25 $9.79 | **+5.62%** |
| 1 month | 2026-08-03 $9.73 | +6.27% |
| From the July low area | 2026-07-31 $9.18 | **+12.64%** |
| From mid-July | 2026-07-15 $9.14 | +13.13% |
| 3 months | 2026-06-02 $11.18 | **−7.51%** |
| 6 months | 2026-03-02 $8.65 | +19.54% |

Last twelve sessions of closes: 9.93, 9.70, 9.87, 10.38, 10.31, 10.30, 10.11, 9.79, 9.70, 10.33, 10.82,
10.34 [2]. Note the **−4.44% on 2026-09-01**, the session immediately before the print, which coincides with
D.A. Davidson's Sell/$7 reiteration dated the same day [21].

**How crowded does the trade look — my read.** Genuinely two-sided and unusually so. The short side is very
crowded in *size* (34.65% of float, 9.65 days to cover) but not *stressed*: borrow at 37bp with a million
shares available is not a squeeze-primed setup, it is a cheap, comfortable short that funds can hold through
an event [10][31]. Simultaneously the options tape is tilted long — 1.6:1 call volume into the print and an
OI put/call of 0.45 [5][32]. So the equity book is short and the derivatives book is long, which mechanically
widens the outcome distribution and is a decent explanation for why the implied move is priced 1.6× the mean
realised move. It also means a positive surprise has two accelerants (short cover plus dealer call hedging)
while a negative surprise has to fight short-covering profit-taking — a mild asymmetry in favour of the
upside *tail*, sitting inside a distribution whose *centre* I read as lower.

---

## 6. Sentiment & alt-data

- **Sell-side tone is the most negative it has been.** Consensus Sell, average target **$8.82 — 14.7% below
  spot** [21]. The stock is trading materially *above* where the Street thinks it belongs, which is unusual
  and is itself a bearish positioning fact. Target drift over three weeks: ~$10.78 (9 analysts, 2026-08-11,
  `snippet_only`) [22] → $8.82 (14 analysts, 2026-09-01) [21].
- **Freshest analyst action is negative and one day old:** D.A. Davidson Sell, $7, 2026-09-01 [21].
- **Zacks:** Rank #3 (Hold); consensus EPS unchanged over 30 days [6][20][29].
- **Retail/social.** Stocktwits has a documented pattern with this name of flipping *bullish on bad news* —
  after the quarter in which the company cut 26% of staff and shares fell 22% after hours, retail sentiment
  moved from neutral to bullish [33]. That is colour, not a load-bearing claim. A quantified 7/14/30-day
  Stocktwits sentiment trend with dates could not be sourced — gap.
- **Positive third-party validation in the window:** Forrester Wave Leader, highest current-offering score of
  15 providers, 2026-08-10 [15]. Customer commentary quoted in the Wave describes "white glove"
  implementation and enthusiasm about realised business value [15]. This is the single strongest recent piece
  of evidence for Siebel's "the product is not the problem" claim.
- **Alt-data.** Headcount from Revelio Labs shows 1,095 employees as of December 2025 and 253 active job
  postings in 2025 [34] — but that predates the restructuring that took headcount to ~700 [17], so it is
  stale and I am not treating it as a signal. Google Trends, web traffic, app ranks and current job-posting
  counts could not be sourced — gap.

---

## 7. Forensics

**Form 4 activity — all identified insider *sales* are 10b5-1, and there is a very large discretionary buy
on the other side.**
- **2026-08-11:** Thomas M. Siebel (CEO and Chairman) exercised options for 453,314 Class A shares at $3.90
  and disposed of 453,314 shares at $10.51 [35][36].
- **2026-07-14 / 2026-07-15:** Siebel sold 462,565 Class A shares, reported at ~$4.2M–$4.76M [35][37][38].
- Both sets of dispositions were executed under a **pre-established Rule 10b5-1 plan dated 2024-09-20**, i.e.
  **non-discretionary** [35]. My read: these are mechanical and carry near-zero information about the quarter.
- **Offsetting and far more informative:** Siebel personally bought **6,170,000 shares at $11.16** in the open
  market, generating **$68.7M of net proceeds to the company**, disclosed with the preliminary Q4 results in
  May 2026 [7][17]. That purchase price is **8% above** the current $10.34 spot. A discretionary $69M buy
  outweighs ~$9M of plan-driven sales as a signal.

**Governance and filings.**
- **8-K filed 2026-08-27 (event 2026-08-25), Item 5.02:** **John C. Dwyer appointed to the board** as a Class
  III director, term through the 2026 annual meeting; standard non-employee package including an initial
  option award with grant-date fair value of $900,000 vesting over five years. Signed by Siebel as CEO and
  Chairman [39].
- **DEF 14A filed 2026-08-27:** 2026 annual meeting **2026-10-26**, virtual, 10:00 a.m. PT; **record date
  2026-09-04** (two days after this print); three Class III directors up for election; advisory say-on-pay
  vote [40].
- **8-K cadence in FY26:** 2026-02-24, 2026-03-24, 2026-06-03, 2026-07-14, 2026-08-25 [39][41]. Routine —
  no unusual clustering or off-cycle filing ahead of this print.

**Pre-announcement signalling.**
- The company **has form here**: on **2026-05-12** it pre-announced preliminary Q4 and FY26 results *together
  with* Siebel's resumption of the CEO role [13][9]. The stock closed **−7.28%** that day (2026-05-11 $9.48 →
  2026-05-12 $8.79, my calculation [2]).
- For Q1 FY27 there has been **no pre-announcement**. The 2026-08-20 release contained the date and nothing
  else [1]. My inference: given the demonstrated willingness to pre-announce, the *absence* of a warning
  is mildly reassuring on the tail-disaster scenario — it argues against a repeat of the February 2026
  −18.5% type event — but it says nothing about whether bookings inflected, since the May pre-announcement
  was itself for an in-line quarter.

**Executive departures, auditor, restatement.** No CFO or CRO departure could be found for 2026; the only
confirmed leadership change is Ehikian CEO → President and Siebel's return [13][9]. No auditor change,
restatement or material weakness was found in searching the FY26 10-K coverage, but I could not read the
audit-opinion and ICFR sections of the 10-K directly, so I am recording this as **not confirmed either way**
rather than clean [27].

**Filing-language tone shift.** The FY26 10-K adds explicit risk-factor language around the CEO transition,
the global workforce reduction and the restructuring plan and their potential effect on future performance
and *investor confidence* [27] — new relative to prior years and consistent with management acknowledging
execution risk rather than concealing it.

---

## 8. Macro & peer read-through

**The sector backdrop is the bear case's best argument.** Enterprise-AI demand is demonstrably not the
constraint:
- **Palantir, Q2 reported 2026-08-04:** revenue **+93% to $1.94B**, commercial revenue **+149% to $764M**,
  government **+90% to $809M**, beating LSEG estimates of $1.8B; the stock rose **~29%** [42].
- **SoundHound, Q2 2026:** revenue **$61.9M, +45% YoY**, ~18% above the ~$52.4M consensus; loss narrowed to
  $(0.02) vs $(0.05) expected; FY26 revenue guidance **raised to $230–260M** [42].
- Peer data/analytics names cited in a C3-specific preview: Elastic +16% revenue growth (beat by 0.9%),
  Teradata +6.2% (beat by 3.4%) [43].

**My inference:** C3.ai is guiding to **−26% YoY** in a quarter where its closest thematic comparables are
growing 45–93% and raising guidance. That is not a demand problem; it is a share and execution problem, which
is exactly Siebel's own diagnosis [17]. The market has been rewarding "proof over promise" in enterprise
software this cycle, and C3.ai is arriving with promise.

**Same-session crowding.** Per this run's stage-1 shortlist, **Snowflake, Broadcom, NetApp and PVH all report
after the close on 2026-09-02** as well. My inference: AI is a $1.6B market cap reporting into the same tape
as AVGO and SNOW. On a night when a mega-cap AI-capex print and a high-multiple data-software print land
simultaneously, a small-cap's own numbers can be swamped by sector beta in the after-hours and the following
open. With a beta of 2.09 [21], AI is unusually exposed to that spillover in both directions.

**Rate / FX / commodity sensitivity.** Minimal direct commodity or FX exposure; the meaningful macro linkages
are (a) high-beta, long-duration equity sensitivity to rates and risk appetite (β 2.09 [21]), and (b) federal
budget flow, since Federal/Defense/Aerospace was 41% of FY26 bookings and the growth engine [26]. C3 AI holds
substantial federal contract vehicles including a U.S. Air Force Rapid Sustainment Office award whose ceiling
was raised to $450M and a $500M five-year DoD Production Other Transaction Agreement covering Air Force,
Space Command, F-35 JPO and DISA [44] — I could not confirm the announcement dates of these vehicles within
the last twelve months, so treat them as existing capacity rather than fresh catalysts.

**Customer/supplier read-through.** Shell's 2026-06-04 expansion of its C3 AI Reliability deployment across
13,000+ monitored assets, adding agent-based root-cause analysis, is the most recent large-customer datapoint
and is a renewal/expansion rather than a loss [18]. Baker Hughes remains the anchor JV, renewed and amended
four times since 2019 [28].

---

## 9. Bull case / bear case / base case

**Bull case.** The Street is positioned for failure and the setup is mechanically explosive. 34.65% of the
float is short with 9.65 days to cover [10], the consensus target of $8.82 is 14.7% *below* spot [21], and
the options tape is already 1.6:1 calls [5] — so a single credible bookings/RPO inflection forces both a
short scramble and dealer delta buying at once, and the +20.76% precedent from 2025-05-29 [2] proves the
mechanism is live. The fundamentals supporting that inflection are real and sourced: ~$130M of the $135M cost
programme is already banked with the rest landing in 2H FY27 [17], the Street sits *below* the guide midpoint
on revenue so an in-line quarter is a technical beat [6][7], Forrester ranked the product highest in current
offering of 15 evaluated platforms on 2026-08-10 [15], Shell expanded rather than churned on 2026-06-04 [18],
federal bookings grew 17% in FY26 and are 41% of the book [26], and Siebel put $68.7M of his own money in at
$11.16 — 8% above today's price [7]. With $673M of cash against a $1.61B market cap [7][10] there is no
financing risk to discount.

**Bear case.** The last print is the template and it was bearish: Q4 FY26 beat on EPS *and* revenue *and*
its own operating-loss guide, and still closed down 1.21%, because bookings were light [7][2][24]. Nothing
in the evidence says that changed. RPO is down 13.6% to $203.1M [26], GAAP gross margin has collapsed from
59% to 17% to 22% across three quarters [25][7], FY26 free cash flow was −$192.1M [7], and the company is
guiding Q1 revenue down 26% YoY [7] in a quarter when Palantir grew 93% and SoundHound raised guidance [42].
Estimates have not moved in 30 days [6], the freshest analyst action is a Sell at $7 dated the day before the
print [21], and the stock has already rallied 12.6% off its 2026-07-31 close into the event [2] — so there
is run-up to surrender. Five of the last seven reports closed lower [2], and the two big up-moves came with
positive guidance changes that are not plausibly on the table for a company that just set a $210–240M FY27
frame it has every incentive to defend rather than raise one quarter in.

**Base case (my read).** The quarter itself prints roughly in line — revenue somewhere in the $50–54M guided
band, non-GAAP operating loss at or better than the guided $(40.5)–(48.5)M given the cost cuts are already
banked — and FY27 guidance is reaffirmed rather than raised, because one quarter into a rebuilt sales motion
management has no basis to raise. The stock then trades on bookings/RPO commentary. My weight of evidence
says that commentary is more likely to be "improving but early" than "inflected," which the market has
already shown it will sell (Q4 FY26, −1.21% on a double beat). Combined with the +12.6% five-week run-up,
the consensus target 14.7% below spot, and a fresh Sell reiteration on 2026-09-01, I lean modestly **down** —
but with genuinely low conviction, because a 34.65% short base at a 37bp borrow cost and a 1.6:1 call skew is
the definition of a setup where a single good number produces a violent move the other way. I expect a move
of meaningful size in either direction: the 13.6% implied move is above the 8.5% mean realised move, so I
would not be a buyer of the straddle, but I would not fade the wings either.

**Preliminary direction score: −22 · Preliminary probability of an up move: 42% · Conviction: Medium.**

---

## 10. What would flip the consensus view

The single most credible reversal is **RPO printing flat-to-up sequentially against the $203.1M base at
2026-04-30, accompanied by a specific, quantified bookings figure showing YoY growth** [26]. That would
convert Siebel's "it is basically sales execution" [17] from an assertion into a measured fact, and it is the
one disclosure that the bears' entire thesis — "an elongated timeline for business trends to improve" [24] —
cannot survive. The second-order version, almost as powerful: **raising the FY27 revenue guide above the
$240M top end** [7], which management would only do with visible backlog. Either event lands into 34.65%
short interest with 9.65 days to cover [10] and a call-heavy options book [5][32], and the 2025-05-29
precedent of +20.76% [2] shows the resulting move can be roughly 1.5× the implied move.

The mirror-image flip — the thing that would make me materially *more* bearish than my −22 — would be a cut
to the FY27 $210–240M frame, or a third consecutive double-digit YoY RPO decline. Given the February 2026
precedent of −18.53% on a guide-down plus layoffs [2][25], that scenario is worth more than the implied move
to the downside.

A quieter flip worth naming: **any announcement naming a successor CEO**. The search initiated 2025-07-24 [9]
has been publicly silent since Siebel's return [17], and Siebel is 73 and returned from a serious health
episode [13]. An announcement in either direction — a named successor, or a formal abandonment of the search
— is a discrete, plausible, un-priced headline that could arrive on this call.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **Whisper number** — none credibly published found | Without it I cannot tell whether the buy side is positioned above or below the −$0.26 / $51.46M sell-side consensus, which is the difference between an in-line print rallying and selling off. |
| **60-day and 90-day estimate revisions** — only the 30-day (unchanged) datum sourced [6] | 30 days of stability could be masking a large 90-day cut. The direction of the three-month revision trend is a standard drift predictor and I am flying without it. |
| **Options skew (25-delta put/call)** — MarketChameleon returned HTTP 503, Fintel HTTP 403 | With a 1.6:1 call *volume* ratio and a 0.45 OI put/call, skew is the missing piece that would tell me whether the upside is being bought or the downside sold. Directly affects the asymmetry read in §5. |
| **Borrow fee carries no published as-of date** [31] | A 0.3658% borrow is the crux of my "crowded but not stressed" read. If that figure is stale and borrow has tightened, the squeeze risk is materially higher than I have assumed. |
| **Consensus RPO / bookings estimate** — none published found | This is *the* metric the print trades on (§3) and there is no number to beat. The bar is narrative, which widens the outcome distribution and lowers my conviction. |
| **Q4 FY26 absolute bookings dollar figure** — company does not disclose it; D.A. Davidson said only "lighter than anticipated" [24] | I can establish that bookings missed but not by how much, so I cannot size the sequential comparison. |
| **Google Trends, web traffic, app ranks, current job-postings count** | No independent real-time read on demand. The only headcount alt-data found (Revelio, 1,095 employees, Dec 2025 [34]) predates the cut to ~700 and is unusable. |
| **Quantified Stocktwits 7/14/30-day sentiment trend with dates** | Only qualitative colour sourced [33]. Retail flow matters more than usual in a 34%-short small cap. |
| **Auditor identity, ICFR/material-weakness status, going-concern language** — not directly read from the 10-K [27] | Recorded as *not confirmed*, not as clean. For a company with a $498.5M operating loss this is a real forensic blind spot. |
| **Stock-based compensation dollar figure** | The $3.35 GAAP vs $1.35 non-GAAP EPS gap [7] implies it is very large, but I could not source the number, so I cannot quantify ongoing dilution. |
| **Domains unreachable:** fintel.io (403), marketchameleon.com (503), stooq.com (connection reset), unusualwhales.com (no data returned), marketrebellion.com (empty body — used via search snippet instead) | Recorded per the environment note. |

**Two vendor-data traps I found and avoided, flagged for the panel:**
1. **The Sep 9 date is wrong.** TipRanks and several aggregators list 2026-09-09 [12][30]; the company's own
   release says 2026-09-02 [1]. Any downstream figure sourced to a "next earnings" page may be misdated.
2. **Several search snippets returned stale articles as if current** — a TipRanks "what to expect from Q1"
   page that is actually from September 2024 (consensus −$0.13 on $86.94M revenue, $35 price target), and a
   Barchart preview quoting a $11.75 spot and a −53.5% YoY revenue expectation that belongs to the Q4 FY26
   report, not this one. Neither is used anywhere above. Analyst actions attributed to "August 2026" in one
   snippet (Morgan Stanley $22→$11, UBS $23→$16, Northland downgrade) are in fact from September 2025 and are
   likewise excluded.

---

## 12. Sources

1. [C3 AI to Announce Financial Results for Fiscal First Quarter 2027 on September 2, 2026 — Businesswire, 2026-08-20](https://www.businesswire.com/news/home/20260820849223/en/C3-AI-to-Announce-Financial-Results-for-Fiscal-First-Quarter-2027-on-September-2-2026) — **event confirmation**: date, AMC session, quarter ended 2026-07-31, 2:00pm PT call time; no preliminary figures.
2. [Yahoo Finance chart API, ticker AI, 2-year daily closes (fetched 2026-09-02)](https://query2.finance.yahoo.com/v8/finance/chart/AI?range=2y&interval=1d) — spot $10.34 at 2026-09-01T20:00:02Z; all seven historical earnings-day close-to-close moves; run-up windows; realised vol; average volume; catalyst-day moves.
3. [OptionSlam — C3.ai (AI) earnings history and implied moves](https://www.optionslam.com/earnings/stocks/AI) — **implied move ±13.64% (Sep-04 weekly), ±16.25% (Sep-18 monthly)**; next earnings 2026-09-02; 2026-06-03 pre-close $10.71 / one-day close $10.58 (−1.21%).
4. [TipRanks — C3 AI options imply move post-earnings (via search snippet, 2026-08-31)](https://www.tipranks.com/news/the-fly/c3-ai-options-imply-13-2-move-in-share-price-post-earnings-thefly-news) — ~13.49% implied move corroboration. `snippet_only`.
5. [Market Rebellion — Mid-session IV Report, September 1, 2026](https://marketrebellion.com/news/daily-iv-report/mid-session-iv-report-september-1-2026/) — Sep-04 weekly call IV 179; Sep cycle IV 100 vs 52-wk range 51–108; call:put volume 1.6:1 into results "after the bell on September 2". `snippet_only` (page body returned empty on direct fetch).
6. [Zacks/Yahoo — Seeking Clues to C3.ai (AI) Q1 Earnings: Wall Street Projections for Key Metrics](https://finance.yahoo.com/markets/stocks/articles/seeking-clues-c3-ai-ai-131503319.html) — consensus EPS −$0.26, revenue $51.46M (−26.8%), subscription $48.28M, professional services $3.07M, subscription GM 27.9%, PS GM 51.7%, 30-day revision unchanged, Zacks Rank #3.
7. [C3.ai Form 8-K Exhibit 99.1 — Q4 and FY2026 results (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000056/ex991-fy26xq4earnings.htm) — Q4 revenue $51.6M, subscription $48.4M, GAAP GM 22% / non-GAAP 37%, GAAP EPS −$0.79 / non-GAAP −$0.33; FY26 revenue $250.3M, GAAP operating loss $(498.5)M, GAAP EPS −$3.35, non-GAAP EPS −$1.35, FCF $(192.1)M; cash and investments $673M incl. $68.7M Siebel purchase of 6.17M shares at $11.16; restructuring charge $10.8M; **Q1 FY27 guidance $50–54M revenue, $(40.5)–(48.5)M non-GAAP operating loss; FY27 guidance $210–240M revenue, $(128)–(160)M non-GAAP operating loss**.
8. [C3 AI Announces Fiscal Fourth Quarter and Full Fiscal Year 2026 Results — Businesswire, 2026-06-03](https://www.businesswire.com/news/home/20260603380058/en/C3-AI-Announces-Fiscal-Fourth-Quarter-and-Full-Fiscal-Year-2026-Results) — guidance corroboration.
9. [Tom Siebel and the Board Initiate Search for Successor CEO at C3 AI — Businesswire, 2025-07-24](https://www.businesswire.com/news/home/20250724662139/en/Tom-Siebel-and-the-Board-Initiate-Search-for-Successor-CEO-at-C3-AI) — succession search initiation and terms.
10. [stockanalysis.com — C3.ai statistics and valuation](https://stockanalysis.com/stocks/ai/statistics/) — **short interest 48.14M shares, 34.65% of float, 30.97% of shares out, days to cover 9.65, prior month 44.42M**; shares out 155.45M; float 138.94M; beta 2.09; market cap $1.61B; EV $1.09B; cash $575.45M; total debt $58.68M.
11. [Investing.com — C3.ai's Options Anomaly: A Squeeze in the Making?](https://www.investing.com/analysis/c3ais-options-anomaly-a-squeeze-in-the-making-200677935) — short interest 32.43% of float as of the 2026-08-03 close. `snippet_only`.
12. [TipRanks — C3.Ai, Inc. (AI) Earnings Dates](https://www.tipranks.com/stocks/ai/earnings) — vendor listing 2026-09-09 as next earnings; **cited only to document the discrepancy**.
13. [C3 AI Announces Preliminary Q4/FY2026 Results; Thomas M. Siebel Resumes Role of CEO — C3.ai IR, 2026-05-12](https://ir.c3.ai/news-releases/news-release-details/c3-ai-announces-preliminary-fourth-quarter-and-full-fiscal-year) — pre-announcement precedent; Siebel resumes CEO effective 2026-05-08; Ehikian to President.
14. [Investing.com — Earnings call transcript: C3.ai beats Q4 2026 estimates but stock dips](https://www.investing.com/news/transcripts/earnings-call-transcript-c3ai-beats-q4-2026-estimates-but-stock-dips-93CH-4725379) — Q4 EPS −$0.33 vs −$0.38 estimate; revenue $51.6M vs $50.13M estimate.
15. [C3 AI Named Leader in AI Platforms — Businesswire, 2026-08-10](https://www.businesswire.com/news/home/20260810156989/en/C3-AI-Named-Leader-in-AI-Platforms) — Forrester Wave AI Platforms Q3 2026 Leader, highest current-offering score of 15 providers.
16. [C3 AI Q2 FY2026 Results — c3.ai](https://c3.ai/news/c3-ai-announces-fiscal-second-quarter-2026-results) — federal bookings +89% YoY; total bookings +49% QoQ; 17 agreements >$1M, six >$5M.
17. [C3.ai (AI) Q4 2026 Earnings Call Transcript — The Motley Fool, 2026-06-03](https://www.fool.com/earnings/call-transcripts/2026/06/03/c3ai-ai-q4-2026-earnings-transcript/) — Siebel on sales execution; 100–150 → ~1,000 accounts; 417 cumulative IPDs, 251 active; headcount ~1,070 → ~700; ~$130M of $135M savings realised; Q4 FCF −$54.8M; cash $673M; no succession discussion.
18. [C3 AI and Shell Expand Collaboration, Scaling Reliability AI Deployment — c3.ai, 2026-06-04](https://c3.ai/c3-ai-and-shell-expand-collaboration-scaling-reliability-ai-deployment-across-global-asset-operations/) — multi-year expansion, 13,000+ monitored assets, agent-based root cause analysis.
19. [Investing.com — C3.ai Q4 FY26 analysis: restructuring and go-to-market](https://uk.investing.com/news/stock-market-news/earnings-call-transcript-c3ai-beats-q4-2026-estimates-but-stock-dips-93CH-4712739) — 35% headcount reduction, $135M cost reduction, FY27 guidance framing.
20. [Zacks/Yahoo — C3.ai, Inc. (AI) Registers a Bigger Fall Than the Market](https://finance.yahoo.com/markets/stocks/articles/c3-ai-inc-ai-registers-215002066.html) — earnings 2026-09-02, EPS −$0.26, revenue $51.46M (−26.76%), Zacks Rank #3, estimate unchanged over the month.
21. [stockanalysis.com — C3.ai stock forecast and analyst price targets](https://stockanalysis.com/stocks/ai/forecast/) — **14 analysts, Sell consensus, $8.82 average target (14.70% downside), 1/0/7/3/3 breakdown; D.A. Davidson Sell $7 dated 2026-09-01; BofA Sell $8 dated 2026-07-22; Wedbush Buy $15 dated 2026-06-04; FY27 forecast revenue $224.31M, EPS −$0.79**; spot $10.34, market cap $1.61B, 52-wk range $7.68–$20.22, beta 2.09.
22. [public.com — C3.ai stock forecast, analyst ratings and price target](https://public.com/stocks/ai/forecast-price-target) — 2026-08-11 cut: Hold consensus, $10.78 target across 9 analysts; target range $6–$15. `snippet_only`.
23. [Daily Political — C3.ai's Underperform Rating Reaffirmed at D.A. Davidson, 2026-09-01](https://www.dailypolitical.com/2026/09/01/c3-ais-ai-underperform-rating-reaffirmed-at-da-davidson.html) — reiteration one day before the print.
24. [Investing.com — DA Davidson reiterates C3.ai Underperform on bookings miss, 2026-06-04](https://www.investing.com/news/analyst-ratings/da-davidson-reiterates-c3ai-stock-underperform-on-bookings-miss-93CH-4726935) — **bookings lighter than anticipated despite EPS and revenue beats; $7 target; "elongated timeline for business trends to improve"**.
25. [CNBC — C3 AI shares plummet as company cuts 26% of workforce, posts wider loss than expected, 2026-02-26](https://www.cnbc.com/2026/02/26/c3-ai-stock-layoffs-loss.html) — context for the −18.53% reaction; Q3 FY26 GAAP gross margin 17% vs 59%.
26. [C3 AI Announces Fiscal Third Quarter 2026 Results / FY26 metrics — c3.ai](https://c3.ai/news/c3-ai-announces-fiscal-third-quarter-2026-results) and associated FY26 disclosure — **RPO $203.1M at 2026-04-30, −13.6% YoY ($36.4M deferred revenue + $166.7M non-cancellable commitments); 28 agreements, 9 new IPDs, 7 IPD conversions in Q4; FY26 Federal/Defense/Aerospace bookings +17% YoY = 41% of total bookings; Q4 revenue −53% YoY**.
27. [C3.ai Form 10-K FY2026 (SEC EDGAR, filed 2026-06-24)](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000078/ai-20260430.htm) — FY26 revenue $250.3M, net loss $470.4M; risk factors on customer concentration, CEO transition, workforce reduction and restructuring.
28. [C3 AI and Baker Hughes Renew and Expand Joint Venture Agreement — c3.ai](https://c3.ai/c3-ai-and-baker-hughes-renew-and-expand-joint-venture-agreement/) — anchor JV renewed/amended four times since 2019; deployments at Shell, Eni, QatarEnergy LNG, Petronas, ExxonMobil and others.
29. [Zacks/Yahoo — C3.ai, Inc. (AI) Is a Trending Stock](https://finance.yahoo.com/markets/stocks/articles/c3-ai-inc-ai-trending-130004643.html) — 30-day consensus EPS estimate unchanged.
30. [StockStory / Yahoo — C3.ai (AI) Reports: Everything You Need To Know Ahead Of Earnings](https://finance.yahoo.com/markets/stocks/articles/c3-ai-ai-reports-q2-041257561.html) — "beat of adjusted operating income estimates but a significant miss of billings estimates"; average target $8.82 vs then-spot; also carries the erroneous Sep-09 date.
31. [companiesmarketcap.com — C3 AI cost to borrow (Interactive Brokers)](https://companiesmarketcap.com/c3-ai/cost-to-borrow/) — **borrow fee 0.3658% annualised, 1,000,000 shares available; no as-of date published**.
32. [Fintel — AI put/call ratio and options sentiment](https://fintel.io/sopt/us/ai) — OI put/call 0.45. `snippet_only` (page returned HTTP 403 on direct fetch).
33. [Stocktwits — C3.AI stock crashes after alarming results: retail investors see worst-case scenario](https://stocktwits.com/news-articles/markets/equity/c3-ai-stock-crashes-after-alarming-results-forecast-retail-investors-see-worst-case-scenario-speculate-buyout/cZR66LDRIbd) — retail sentiment moved neutral → bullish after the −22% after-hours reaction and 26% workforce cut. Supporting colour only.
34. [Revelio Labs — C3 ai employee count and job postings](https://www.reveliolabs.com/companies/c3-ai/employees/) — 1,095 employees as of December 2025, 253 active job postings in 2025. **Stale — predates the cut to ~700.**
35. [Investing.com — C3.ai CEO Thomas Siebel sells $4.76M company stock](https://www.investing.com/news/insider-trading-news/c3ai-ceo-thomas-siebel-sells-476m-company-stock-93CH-4859508) — 2026-08-11 option exercise 453,314 at $3.90 and disposal at $10.51; sales under a **Rule 10b5-1 plan dated 2024-09-20**, non-discretionary.
36. [C3.ai Form 4 (SEC EDGAR, accession 000157752626000098)](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000098/wk-form4_1786656439.xml) — Form 4 primary filing.
37. [C3.ai Form 4 (SEC EDGAR, accession 000157752626000094)](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000094/wk-form4_1785891723.xml) — Form 4 primary filing.
38. [Motley Fool — What Does the C3.ai CEO's Sale of Company Shares Worth $4.2 Million Mean for Investors? (2026-07-18)](https://www.fool.com/coverage/filings/2026/07/18/what-does-the-c3-ai-ceo-s-sale-of-company-shares-worth-usd4-2-million-mean-for-investors/) — 462,565 shares sold 2026-07-14/15.
39. [C3.ai Form 8-K, filed 2026-08-27 (event 2026-08-25) — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000103/ai-20260825.htm) — Item 5.02: John C. Dwyer appointed Class III director; $900,000 grant-date-fair-value initial option award vesting over five years.
40. [C3.ai Form DEF 14A, filed 2026-08-27 — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000110/ai-20260827.htm) — annual meeting 2026-10-26 virtual, record date 2026-09-04, three Class III directors, advisory say-on-pay.
41. [C3.ai Form 8-K, 2026-07-14 — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0001577526/000157752626000092/ai-20260714.htm) — 8-K cadence reference.
42. [CNBC — Palantir stock rises 29% on soaring commercial revenue, AI sovereignty (2026-08-04)](https://www.cnbc.com/2026/08/04/palantir-2q-earnings-ai-sovereign-tools.html) — PLTR revenue +93% to $1.94B, commercial +149% to $764M, government +90% to $809M, stock +29%; and [Motley Fool / Yahoo peer coverage](https://finance.yahoo.com/technology/ai/articles/not-palantir-not-soundhound-ai-144301496.html) — SoundHound Q2 revenue $61.9M +45%, loss $(0.02) vs $(0.05), FY26 guide raised to $230–260M.
43. [Barchart — C3.ai (AI) Q1 Earnings Report Preview: What To Look For](https://www.barchart.com/story/news/2247875/c3-ai-ai-q1-earnings-report-preview-what-to-look-for) — peer growth reference (Elastic +16%, Teradata +6.2%). **Note: this article's spot price and YoY figures are stale and are not used elsewhere in this dossier.**
44. [C3 AI — US Air Force Rapid Sustainment Office contract award increased to $450M](https://c3.ai/news/c3-ai-us-air-force-rapid-sustainment-office-contract-award-increased) and [FedScoop — DoD awards C3.AI $500M Other Transaction Agreement](https://fedscoop.com/department-of-defense-awards-c3-ai-500m-other-transaction-agreement/) — federal contract vehicles. **Announcement dates not confirmed to be within the last twelve months.**

---

*This is research, not investment advice. It is a forecasting exercise over public information and must not
be presented or relied upon as investment advice.*
