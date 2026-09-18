# JKS — JinkoSolar Holding Company Limited

**What this print is about.** JinkoSolar reports Q2 2026 before the US open on Wednesday
26 August 2026 [1]. This is not an EPS print. The consensus loss of −$0.75/ADS is
almost exactly what management's own Q1 guidance implies (shipments 14–16 GW, gross
margin "relatively stable" near Q1's 8.3%) [2][30], so the headline number is a low bar
that the company has already pre-described. What is genuinely unresolved is the
**FY2026 module-shipment guidance of 75–85 GW**. Q1 delivered 13.7 GW and Q2 was guided
to 14–16 GW, so H1 lands near 28–30 GW and the full-year range requires 46–56 GW in H2
— versus 44.2 GW actually shipped in H2 2025, in a Chinese market the CPIA says
contracted 66% year-on-year in H1 2026 [12] and will fall for the first time since 2019
[11]. Roth's Philip Shen put exactly this arithmetic to management on the Q1 call [30].
Around that sit three live wildcards the market has not priced: a possible one-time gain
from the May 2026 sale of 75.1% of the Jacksonville US plant for $191.5m [18][19]; the
13-August Hunterbrook investigation alleging the buyer is controlled by the family of
Suntech founder Zhengrong Shi, which puts the 45X/FEOC structure in a "gray zone" [17];
and a Chinese "anti-involution" policy cycle that has already produced one +13% print for
this stock (17 Nov 2025). The stock is at $16.16, −42% YTD, near its 52-week low, with
retail positioning almost unanimously bullish and the listed options market pricing
almost no event premium at all.

---

## 1. Event & anchors

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| **Event confirmed** | **Yes** — `event_confirmed: true` | — | SEC 6-K Ex-99.1, filed 2026-08-14 [1] |
| Event date | 2026-08-26 | — | [1] |
| Session | **bmo** — "before the open of U.S. markets on Wednesday, August 26, 2026" | — | [1] |
| Fiscal quarter | Q2 2026 (quarter ended 30 June 2026) | — | [1] |
| Call time | 08:30 ET / 20:30 Beijing, same day; replay through 2026-09-02 | — | [1] |
| Date changed / pre-announced? | No. Announced 2026-08-14, unchanged. No pre-announcement or profit warning found. | — | [1][25] |
| **Spot** | **$16.16** (close, +1.51% on the day; prev close $15.92) | 2026-08-24 16:00 ET (20:00Z) | Yahoo chart API [8]; CBOE snapshot 2026-08-24 23:43Z [9]; stockanalysis [3] |
| Pre-market check | $16.16, unchanged | 2026-08-25 05:34 ET | Nasdaq quote API [45] |
| **Market cap** | **$846.3m** (52.37m ADS × $16.16; 1 ADS = 4 ordinary shares) | 2026-08-24 | [3][24] |
| Shares / float | 52.37m ADS outstanding; float 30.30m | 2026-08-24 | [4][24] |
| 50-day MA / 200-day MA | $16.45 (own calc from [8]) / $21.36–21.62 | 2026-08-24 | [8][6][7] |
| 52-week range | $14.55 – $31.88 | 2026-08-24 | [3][45] |
| **Event-implied move (own calculation)** | **≈ ±4.6% expected absolute (1σ ≈ 5.7%)** — see method below. **Fragile: sensitivity band ≈ 0–8%.** | 2026-08-24 23:43Z | CBOE delayed option quotes [9] |
| Sep-18 ATM straddle (to expiry, 25 days) | E\|move\| ≈ **14.7%**, 1σ ≈ 18.4%, ATM IV 70.3% | 2026-08-24 23:43Z | own calc from [9] |
| IV30 | **67.04%** (−0.25 pts on the day) | 2026-08-24 23:43Z | [9] |
| IV rank / percentile | **unavailable** (no free historical-IV source reachable). Proxy: RV30 = 43.6%, which is the **9th percentile** of its own trailing-1-year distribution (range 37.4–89.6%, median 60.4%); IV30/RV30 = **1.54** | 2026-08-24 | own calc from [8][9] |
| RV10 / RV20 / RV60 / RV252 | 42.1% / 41.8% / 54.3% / 61.1% | 2026-08-24 | own calc from [8] |

### Implied-move method and its weakness

JKS has **no weekly options**. The nearest expiry is 2026-09-18, 23 days after the print,
so the first-expiry straddle (14.7%) is a 25-day number, not an event number. Because
every listed expiry contains the 26-Aug event, the term structure cannot be used the
usual way; I instead solved for the event variance that reconciles Sep-18 (25d, ATM IV
70.3%) with Oct-16 (53d, ATM IV 68.5%) under a constant diffusive vol. That yields a
diffusive vol of 66.8% and an event 1σ of 5.72% → E|move| 4.56%. Sep-vs-Dec gives
3.40%. **Sensitivity is severe**: moving the Sep ATM IV read by ±3 points swings the
answer from ~0% to ~8%, and Sep-18 bid/ask spreads are 20–60% of premium
(e.g. $15 call 1.45/2.35). Treat ~4.6% as a point estimate with very low confidence.
The honest headline is: **the term structure is essentially flat (Sep 70.3% / Oct 68.5% /
Dec 68.8% / Mar 68.8%) — the options market is pricing close to no earnings kink**, well
below the 6.4% mean absolute move of the last six prints. This is my inference; the most
likely explanation is chain illiquidity rather than a considered market view.

### Realised one-day earnings reactions (all prints are BMO → same-day close-to-close)

| Quarter reported | Date | 1-day move | Open gap | Volume | Date source |
| --- | --- | --- | --- | --- | --- |
| Q1 2024 | 2024-04-29 | **+2.53%** | +4.93% | 1.29m | [42] |
| Q2 2024 | 2024-08-30 | **+5.75%** | −2.98% | 1.53m | [40] |
| Q3 2024 | 2024-10-30 | **+4.93%** | +6.58% | 3.78m | [39] |
| Q4/FY2024 | 2025-03-26 | **−0.82%** | −2.09%* | 2.00m | [41] |
| Q1 2025 | 2025-04-29 | **−3.85%** | −3.91% | 0.88m | [46] *(snippet_only)* |
| Q2+Q3 2025 (combined) | 2025-11-17 | **+13.09%** | +0.63% | 2.72m | [28] |
| Q4/FY2025 | 2026-04-16 | **−11.89%** | −7.76% | 2.85m | [27][20a] |
| Q1 2026 | 2026-04-29 | **−3.67%** | −1.57% | 0.74m | [2][20b] |

\* 2025-03-26 gap shown vs. the prior close; the −2.09% figure in my working refers to the
following session. All price moves computed by me from Yahoo daily OHLC [8].

- **8-quarter stats:** mean |move| **5.82%**, median |move| **4.39%**, max |move| **13.09%**, 4 up / 4 down.
- **Last 6 quarters:** mean |move| **6.38%**, median |move| **4.39%**, max 13.09%, **2 up / 4 down**.
- **Pattern:** the three 2024 prints (when the company was still profitable) were all up
  and modest. The five prints since have been down four times, and the two largest
  absolute moves in the set are the two most recent extremes: −11.89% (Q4/FY2025) and
  +13.09% (the combined Q2+Q3 2025 release). The distribution is fat-tailed, not
  uniformly violent: half the prints moved less than 4.4%.
- **Realised is above implied.** Six-quarter mean |move| of 6.38% vs. my event-implied
  estimate of ~4.6%. That gap is my single most concrete positioning observation.

### Run-up into the print

| Window | Move | Source |
| --- | --- | --- |
| 5 sessions (8/17 → 8/24) | −2.77% | own calc [8] |
| 10 sessions (8/10 → 8/24) | −4.49% | own calc [8] |
| 21 sessions (7/24 → 8/24) | **+9.19%** | own calc [8] |
| 3 months (5/22 → 8/24) | **−29.34%** | own calc [8] |
| Since the Q1 print (4/29 → 8/24) | **−24.94%** | own calc [8] |
| YTD 2026 | **−42.16%** | own calc [8] |
| 52-week | −31.23% | [4] |
| 60-session high / low | $23.31 (5/29) / **$14.58 (7/29)** | own calc [8] |

So: violently down over three months, bounced +10.8% off the 29-July low, then faded
−4.5% over the last two weeks. Sitting essentially on the 50-day MA ($16.45) and 27%
below the 200-day ($21.36). **No run-up to unwind, and no capitulation low being
defended either** — a genuinely neutral technical setup.

---

## 2. The bar

### Consensus

| Metric | Consensus | Source | Note |
| --- | --- | --- | --- |
| Q2 2026 EPS (per ADS) | **−$0.75** | MarketBeat/DailyPolitical [6][7] | The most widely syndicated number |
| Q2 2026 revenue | **$2.166bn** | [6][7] | |
| Alternative consensus | **−$0.62 EPS on ~$3.01bn revenue** | search snippet, provider unidentified [43a] | *snippet_only*; the $3.01bn revenue line is implausible against 14–16 GW of shipments and I do not treat it as the bar |
| Analyst count | 7 (S&P Global via stockanalysis) [5]; MarketBeat counts 7 ratings [6] | | |
| Rating split | stockanalysis: 3 Strong Buy / 0 Buy / 3 Hold / 0 Sell / 1 Strong Sell → "Buy" [5]. MarketBeat: 1 Strong Buy / 1 Buy / 3 Hold / 2 Sell → "Hold" [6] | | Providers disagree on the label; the underlying dispersion is real |
| Avg price target | **$25.44** (range $15.00 – $32.61) [5]; MarketBeat $24.38 [6]; TipRanks-cited most recent single PT $24.00 [26a] | | +51% to +57% above spot |

### What the consensus actually requires

This is my arithmetic, not a sourced figure. Q1 2026 actuals [2]: revenue $1.78bn,
gross profit $147.7m (8.3%), opex $232.9m, operating loss −$85.3m, net loss attributable
to JKS ordinary shareholders −$67.2m (−$1.28/ADS). The gap between the −$85.3m
operating loss and the −$67.2m attributable loss is ~$18m of net below-the-line and
non-controlling-interest relief — JKS Holding owns only **55.59%** of the operating
subsidiary [37], so roughly 44% of the subsidiary's losses are attributed to minorities.

Consensus of −$0.75/ADS × 52.37m ADS = **−$39.3m attributable net loss**. On $2.166bn of
revenue with opex flat and a similar below-the-line/NCI contribution, that implies an
operating loss near −$57m, which implies gross profit of ~$176m, i.e. **gross margin of
roughly 8.1% — essentially flat versus Q1's 8.3%**. That is exactly what the CFO told
the Street on the Q1 call: margins "relatively stable" in Q2 because of "old orders",
with the jump coming in H2 [30].

**Conclusion: the EPS bar is not demanding. It is a restatement of guidance.** The stock
does not clear or fail on this line. This materially reframes the triage hypothesis (see
§11).

### Guidance on the table

| Guidance item | Company guide | Given | Source |
| --- | --- | --- | --- |
| Q2 2026 module shipments | **14.0–16.0 GW** | 2026-04-29 | [2] |
| FY2026 module shipments | **75–85 GW** (>60% high-efficiency) | reaffirmed 2026-04-29 | [2][36] |
| FY2026 ESS shipments | "more than double YoY"; ~**10 GWh** target at ~**15% gross margin** | 2026-04-29 call | [30]; 6 GWh target also reported [36] |
| Year-end 2026 integrated capacity | ~100 GW, incl. 14 GW overseas; >40 GW of >650W capacity | 2026-04-29 | [2] |
| 2026 industry demand | "5–10% decrease vs 2025", stronger H2 | 2026-04-29 call | [30] |
| H2 gross margin | CFO Tan Yi: "gross margin in second half year will jump ... compared to the first half" | 2026-04-29 call | [30] |

### Estimate revisions

**Largely unavailable in numeric form** — this is a real gap. What I could source:
- FY2026 consensus revenue CNY 75.52bn (+15.3% YoY) and FY2026 EPS −CNY 38.11, swinging
  to +CNY 5.13 in FY2027 [5]. Note these are per-ordinary-share RMB figures; the FY2027
  profitability swing is the load-bearing assumption in every bull price target.
- **UBS raised its PT $23 → $24, Neutral, 2026-05-29** [6] — the last major-bank action I
  can date, and it was a token move made when the stock was ~$22.
- **Wall Street Zen upgraded sell → hold, 2026-05-02** [6].
- **Weiss Ratings reissued "sell (D)", 2026-08-03** [26a] — the only August action found.
- Jefferies' widely-quoted "PT raised to $65.43" [26b] carries no retrievable date and is
  inconsistent with every current consensus PT; I do not treat it as live.
- **No 30/60/90-day numeric revision series could be retrieved** (Zacks detailed-estimates
  page not reachable). Directionally, price targets are far above spot ($25.44 avg vs
  $16.16 = +57%), which historically means targets are stale rather than bullish.

### Whisper number

**Unavailable.** No credibly published whisper number for JKS was found. Given seven
covering analysts and a $846m market cap, I would not expect one to exist.

---

## 3. The one metric that matters

> **Whether the FY2026 module-shipment guidance of 75–85 GW survives the print intact —
> and, if it is cut, whether the cut comes with the H2 gross-margin "jump" still attached.**

**Why this and not EPS.** The EPS bar is a restatement of guidance (§2). The shipment
guidance, by contrast, is arithmetically stretched to the point of being the print's only
real information content:

| | GW | Source |
| --- | --- | --- |
| Q1 2026 module shipments (actual) | 13.68 | [2] |
| Q2 2026 module shipments (guided) | 14–16 | [2] |
| **Implied H1 2026** | **27.7–29.7** | own calc |
| FY2026 guidance | 75–85 | [2] |
| **Implied H2 2026 requirement** | **45.3–57.3** | own calc |
| H2 2025 actual (for comparison) | 44.2 (FY 86.06 less H1 41.8) | [27]; H1 2025 = 17.5 Q1 + 24.3 Q2 [2][28] |
| Implied H2 2026 YoY | **+2% to +30%** | own calc |
| …while H1 2026 ran | **−31% YoY** | own calc |

To hold guidance, JinkoSolar has to swing from −31% YoY in H1 to flat-or-better in H2, in
a year when: Chinese H1 installations fell **66%** to 72.07 GW [12]; Chinese module
output fell **35.1%** to 201.3 GW [11]; module export volumes fell 2.5% [11]; the CPIA's
own full-year China forecast is 180–240 GW versus ~315 GW in 2025 [11]; and management
itself guided global demand down 5–10% [30]. **Roth Capital's Philip Shen questioned
precisely this jump on the Q1 call** — from a 14–15 GW quarterly pace to the 25+ GW/quarter
the annual guide implies [30]. Management did not walk it back then.

**Market expectation for it, and how I know.** I could find no published sell-side
shipment forecast for FY2026. My read is that the buy-side already discounts a cut —
the ADS is −42% YTD and trades at 0.38× the FY2025 attributable book value of $2.25bn
[26], and the A-share subsidiary is −15.7% since 22 June [33]. What is *not* discounted,
in my judgement, is a cut **paired with** any softening of the H2 margin-jump language.
The Nov-2025 print (+13.09%) is the template for what happens when JKS delivers a bad
quarter with an intact forward narrative; the Apr-2026 print (−11.89%) is the template
for what happens when the forward narrative cracks.

**Secondary metrics to watch, in order:**
1. **Q2 gross margin** vs. Q1's 8.3%. Anything below ~7% breaks the "inflection" story.
2. **Any gain or loss on the disposal of 75.1% of Jinko Solar (U.S.) Industries** for
   $191.5m, which closed in May 2026 [18][19] — a Q2 event that could scramble headline
   EPS in either direction and against which the −$0.75 consensus is probably not
   calibrated.
3. **ESS shipments and revenue recognition.** Q1 shipped 1.42 GWh but recognised revenue
   on only 520 MWh [2][30]. The FY target is ~10 GWh at ~15% gross margin [30] — roughly
   double module margins. Q2 ESS is the only credible source of positive mix surprise.
4. **Inventory and receivables.** FY2025 inventory rose to RMB14.48bn from RMB12.51bn on
   a 29% revenue decline [26]; receivables were RMB13.77bn at Q1 2026 [2]. A writedown
   is the most likely source of a large negative EPS surprise.

---

## 4. Fundamentals — what changed, what is at stake

### Trajectory (all from company releases)

| | Q2 2025 | Q4 2025 | Q1 2026 | Q2 2026E |
| --- | --- | --- | --- | --- |
| Revenue | RMB17.99bn / $2.51bn [28] | RMB17.51bn / $2.50bn [27] | RMB12.25bn / $1.78bn [2] | $2.166bn cons. [6] |
| Gross margin | 2.9% [28] | 0.3% [27] | **8.3%** [2] | ~8% implied [own calc] |
| Operating margin | n/d | −18.6% [2] | −4.8% [2] | — |
| Net loss attributable | RMB876.4m / $122.3m [28] | RMB1.50bn [2] | RMB463.5m / **$67.2m** [2] | −$39.3m implied [own calc] |
| Loss per ADS | ~$2.34 [own calc from 28] | — | **$1.28** (RMB8.85) [2] | −$0.75 cons. [6] |
| Module shipments | 24.33 GW (26.45 GW incl. cells/wafers) [28] | — | **13.68 GW** (−45.2% QoQ, −21.9% YoY) [2] | 14–16 GW guided [2] |
| ESS shipments | — | — | 1.42 GWh (520 MWh revenue-recognised) [2][30] | — |

The Q1 margin move (0.3% → 8.3%, gross profit +1,749% QoQ [2]) is the whole bull case.
It came from a module price rebound plus a mix shift to overseas (>80% of module
shipments) and high-efficiency product (>640W = ~25% of shipments) [2].

### Full-year 2025 and the balance sheet (SEC XBRL, 20-F FY2025 [26])

| | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| Revenue | — | — | RMB65.50bn / $9.37bn (−29.0%) [27] |
| Gross profit | RMB19.05bn | RMB10.06bn | **RMB1.41bn** [26] |
| Operating income | +RMB6.09bn | −RMB3.34bn | **−RMB8.91bn** [26] |
| Net income | +RMB3.45bn | +RMB0.05bn | **−RMB4.45bn** [26][27] |
| Operating cash flow | RMB13.83bn | RMB16.85bn | **RMB1.08bn** [26] |
| Capex (PP&E) | RMB15.65bn | RMB9.09bn | **RMB3.19bn** [26] |
| **Free cash flow (own calc)** | −RMB1.83bn | **+RMB7.76bn** | **−RMB2.10bn** | 
| Cash & equivalents | RMB16.06bn | RMB25.05bn | RMB20.01bn / $2.86bn [26] |
| Short-term borrowings | RMB13.58bn | RMB6.93bn | **RMB10.66bn** [26] |
| Convertible debt (non-current) | RMB4.79bn | RMB8.61bn | **RMB10.59bn / $1.52bn** [26] |
| Total liabilities | RMB102.3bn | RMB90.6bn | RMB93.5bn [26] |
| Equity attributable to JKS | RMB20.16bn | RMB19.90bn | **RMB15.73bn / $2.25bn** [26] |
| Non-controlling interests | RMB13.38bn | RMB12.80bn | RMB10.30bn [26] |
| R&D | RMB0.91bn | RMB0.92bn | RMB0.90bn [26] |

At Q1 2026 [2]: cash RMB22.81bn ($3.31bn), receivables RMB13.77bn ($2.00bn), inventories
RMB17.71bn ($2.57bn), **total interest-bearing debt RMB47.27bn ($6.85bn)**. stockanalysis
reports total debt $6.29bn against cash $3.31bn and enterprise value $3.83bn [4].

**Read:** the capex collapse (RMB15.65bn → RMB3.19bn in two years) is the clearest
evidence of the anti-involution discipline actually binding, and it is the single most
constructive number in the filings. But operating cash flow fell 94% in 2025 and FCF went
negative, while convertible debt at the holdco has more than doubled since 2023. Equity
attributable to JKS is down 21% in a year. The company is *not* in imminent distress
(RMB22.8bn of cash), but the balance sheet is deteriorating and the converts are a
material dilution overhang at a $846m market cap.

### Dilution and capital return

- **Dividend: $1.50 per ADS ($0.375/ordinary share), ~$78.5m total**, declared 2026-06-12,
  record 2026-06-22, paid ~2026-07-09 [29]. Ex-date 2026-06-22 confirmed in the price
  series [8]. This is now an established annual pattern ($1.50 in 2023, $1.50 in 2024,
  $1.30 in 2025, $1.50 in 2026 [8][29]). At $16.16 that is a **9.3% yield paid by a
  loss-making company** — either a strong signal of holdco cash confidence or an
  unsustainable transfer, depending on your priors.
- **No buyback found.** Share count is essentially static at 52.37m ADS [24].
- **Dilution risk sits in the RMB10.59bn ($1.52bn) of convertible notes** [26], roughly
  1.8× the entire equity market cap.

### Structural change since the last print — this is the big one

1. **Sold 75.1% of Jinko Solar (U.S.) Industries Inc.** (2 GW Jacksonville, Florida module
   plant) to FH JKV Holdings Limited for **~$191.5m**, subject to NAV adjustment.
   Announced 2026-05-08 [19], **closed in May 2026** [18]. JinkoSolar retains 24.9% [16].
   Roughly $94m of the consideration is deferred in tranches [17]. The plant earned
   **$146m of Section 45X credits in 2025 — more than three-quarters of its net profit**
   [17]. The transaction's evident purpose is FEOC compliance under the One Big Beautiful
   Bill Act so the plant can keep claiming 45X [16][17]. **This deconsolidates a US
   manufacturing business from Q2 2026 and may generate a one-time gain or loss that the
   −$0.75 consensus is unlikely to model correctly.**
2. **CEO change at the operating subsidiary.** Kangping Chen — co-founder, CEO of Jiangxi
   Jinko since December 2020 — resigned as CEO effective **2026-03-16**, replaced by
   **Haiyun (Charlie) Cao**, formerly JKS Holding's CFO 2014–2021 [20][31]. Chen stays as
   a director and becomes deputy chairman. This is Q2's first full quarter under the new
   operating CEO.
3. **Sold down the A-share subsidiary.** After a September 2025 inquiry-transfer/placement
   of Jiangxi Jinko A-shares, JKS Holding's stake fell to **~55.59%** [37].

### Customer concentration

**Unavailable / not sourced.** The FY2025 20-F was not read at the concentration level. In
lieu of it: >80% of Q1 2026 module shipments went to overseas markets [2]; recent order
flow is geographically scattered (300 MW Tajikistan, 500 MW South Korea, 1 GW Shenzhen
Energy 2026–28, a 6 GW TOPCon procurement win) [38], which argues against acute single-
customer concentration but is not a substitute for the disclosure.

### Sum-of-the-parts — my inference, arithmetic shown

- Jinko Solar Co., Ltd. (688223.SH): **10.27bn shares** [37] × **CNY 4.34** (2026-08-25
  close) [33] = **CNY 44.57bn**.
- At USDCNY **6.7079** (2026-08-25) [34] → **US$6.64bn**.
- JKS Holding's **55.59%** [37] → **US$3.69bn** look-through.
- Less holdco convertible notes of **$1.52bn** [26] → **~$2.17bn**.
- Versus a JKS ADS market cap of **$846m** [3].

That is a **61–77% discount** to the listed value of the stake, depending on whether you
net the converts. This is a well-known and persistent structural discount (holdco, PRC
capital controls, VIE-adjacent governance, minority leakage), not a new dislocation — but
it is the reason every bull price target sits 50%+ above spot, and it is why this equity
is a high-beta option on sentiment rather than a claim on earnings.

---

## 5. Positioning & options

All option data from the CBOE delayed-quote endpoint, snapshot **2026-08-24 23:43:56**,
underlying $16.16 [9]. All aggregation and Black-Scholes work is mine.

### Term structure — essentially flat

| Expiry | Days | ATM IV | 1σ to expiry | E\|move\| to expiry |
| --- | --- | --- | --- | --- |
| 2026-09-18 (first after event) | 25 | **70.3%** | 18.4% | 14.7% |
| 2026-10-16 | 53 | 68.5% | 26.1% | 20.8% |
| 2026-12-18 | 116 | 68.8% | 38.8% | 30.9% |
| 2027-03-19 | 207 | 68.8% | 51.8% | 41.3% |

A 1.8-point front-month kink is not an earnings bid. For comparison, IV30 is 67.0% while
RV30 is 43.6% — so options are 1.54× recent realised vol in general, but there is no
*incremental* premium for the 26-August event specifically.

### Skew (Sep-18)

| Strike | Moneyness | Call IV | Put IV | Call OI / vol | Put OI / vol |
| --- | --- | --- | --- | --- | --- |
| 10.0 | −38% | 109.1% | 144.1% | 1 / 0 | 226 / 0 |
| 12.5 | −23% | — | 71.5% | 7 / 0 | 514 / 1 |
| 15.0 | −7% | 74.4% | 69.1% | 49 / 3 | 262 / 21 |
| 17.5 | +8% | 72.4% | 64.3% | 243 / **56** | 270 / 2 |
| 20.0 | +24% | 66.9% | 78.6% | 610 / **338** | 458 / 0 |
| 22.5 | +39% | 84.2% | 85.9% | 267 / **101** | 132 / 0 |
| 25.0 | +55% | 87.2% | 95.0% | 723 / **500** | 46 / 0 |

Near the money there is a **mild call skew** (17.5 call 72.4% vs 15 put 69.1%) — the
opposite of the usual pre-earnings put bid. Deep downside (12.5 put, 71.5%) is only ~1
point above ATM. There is a pronounced upside-wing smile at 22.5/25 that looks like
lottery-ticket demand rather than a hedging structure.

### Unusual options activity — the clearest positioning signal in this name

Total 2026-08-24 CBOE-reported option volume: **1,041 calls vs 29 puts — a put/call
volume ratio of 0.03**. It is concentrated in far-OTM September upside:

- **Sep 25 calls: 500 contracts traded** (+55% OTM, 25 days, quoted 0.00 bid / 0.10 ask),
  standing OI 723.
- **Sep 20 calls: 338 traded** (+24% OTM, 0.10/0.25), standing OI 610.
- **Sep 22.5 calls: 101 traded**; **Sep 17.5 calls: 56 traded**.

Total open interest across all expiries: **6,649 calls vs 3,400 puts (P/C OI 0.51)**.
Sep-18 has large legacy call OI at strikes far above spot (30-strike OI 1,189; 42.5-strike
OI 411; 45-strike OI 237) — residue from when the stock traded above $30.

**Interpretation (mine):** someone — most plausibly retail, given the strikes and the
penny prices — is buying a very one-sided upside lottery into this print. The absence of
any put activity means there is no hedged long base that has to be unwound on bad news,
but it also means there is no cushion of short-put or protective flow to absorb a drop.
Options positioning is crowded long and cheap, which is exactly the configuration that
produces a violent gap when the underlying assumption fails.

### Short interest and borrow

| Metric | Value | As of | Source |
| --- | --- | --- | --- |
| Short interest | **2.85m shares** | date not shown | stockanalysis [4] |
| Short % of shares outstanding | **7.36%** | date not shown | [4] |
| Short % of float (own calc: 2.85m / 30.30m) | **~9.4%** | — | [4] |
| Days to cover / short ratio | **4.50** | date not shown | [4] |
| 20-day average volume | 575,218 | 2026-08-24 | [4] |
| **Borrow fee / cost to borrow** | **unavailable** — Fintel Cloudflare-blocked, iBorrowDesk returned an empty reply, ORTEX paywalled | — | — |
| Conflicting figures found | 2.51m / 6.61%; 5.83m / 15.65%; 1.90m / 3.68% | undated | search snippets [35a] — *snippet_only*, mutually inconsistent, not used |

I use the stockanalysis figures because they are internally consistent (2.85m / 52.37m =
7.36%; 2.85m / 575k ≈ 4.96 days, close to the quoted 4.50 on a slightly longer volume
window). **The settlement date is not shown anywhere I could reach, which is a real
weakness** — NYSE-listed names are not covered by Nasdaq's short-interest API.

### How crowded is the trade?

**Moderately crowded long, in an unusual way.** Institutional ownership is only 34–36%
[4][6], insider ownership 19.8–42.2% depending on provider [4][6] (the spread reflects
whether the founding Li family's holdings are counted). Free float is 30.3m ADS —
~$490m. On 575k shares/day of average volume, that is a thin, retail-heavy, low-
institutional name where a 9%-of-float short base and a one-sided call book can both move
the price a long way. Short interest at 4.5 days to cover is meaningful but not a
squeeze setup on its own.

---

## 6. Sentiment & alt-data

### Retail / social — near-unanimous bullishness on rising volume

Pulled directly from the Stocktwits public API, 240 messages spanning **2026-08-03 to
2026-08-25** [32]:

| Window | Messages | Bullish | Bearish | Untagged | % bullish of tagged |
| --- | --- | --- | --- | --- | --- |
| 0–7 days | 87 | 83 | **1** | 3 | 98.8% |
| 8–14 days | 86 | 80 | **1** | 5 | 98.8% |
| 15–30 days | 67 | 60 | **0** | 7 | 100% |
| **Total** | **240** | **223** | **2** | 15 | **99.1%** |

Watchlist count: **10,701** [32]. Message volume is **rising into the print** (87 in the
last 7 days vs 67 in the 15–30-day window). Daily spikes: 66 messages on 2026-08-21 (the
day the stock closed at $15.92), 41 on 2026-08-13 (the Hunterbrook publication date), 40
on 2026-08-03.

**Two bearish messages out of 225 tagged, over three weeks, into an earnings print, in a
stock down 42% YTD.** Taken with the 0.03 put/call volume ratio, this is the most
one-sided retail configuration I found in this name. It is supporting colour, not a
load-bearing claim, but the direction of the bias is unambiguous and it is a contrarian
negative.

### Analyst rating changes and price-target drift

| Date | Firm | Action | Source |
| --- | --- | --- | --- |
| 2026-08-03 | Weiss Ratings | Reissued **Sell (D)** | [26a] |
| 2026-05-29 | UBS Group | PT $23 → **$24**, **Neutral** | [6] |
| 2026-05-02 | Wall Street Zen | Upgrade **Sell → Hold** | [6] |
| undated | Jefferies (Alan Lau) | PT to $65.43 from $36.69, Buy | [26b] — *stale/unverifiable, disregarded* |

Price-target drift is the story: consensus PT $24.38–$25.44 [5][6] against a $16.16 spot
and a 200-day MA of $21.36. Targets have not been marked down alongside the −42% YTD
move — **the sell side has gone quiet rather than turned negative**, which historically
means the next revision cycle is downward.

TipRanks' AI analyst ("Spark") rates JKS **Neutral**, citing margin collapse, net loss,
high leverage, volatile/negative free cash flow and a bearish technical setup [26a].

### Alt-data

- **Google Trends: unavailable.** The Trends API returned HTTP 429 from this environment.
  This matters less for a B2B module manufacturer than it would for a consumer name.
- **Order-flow proxy (public announcements, a genuinely usable alt-signal for this
  business):** 2026-08-13 — 300 MW Tiger Neo 3.0 utility project in Tajikistan; 500 MW
  Tiger Neo 3.0 order in South Korea; 1 GW Shenzhen Energy 2026–28 procurement; ranked
  first in an N-type TOPCon segment with a 6 GW module procurement win; 10 Tiger Neo 3.0
  orders signed at SNEC 2026 [38]. Announced order flow is healthy and skews to
  non-China markets — consistent with the >80% overseas mix [2] and mildly supportive of
  the H2 shipment case.
- **Product spec (relevant because guidance rests on >60% high-efficiency mix):** Tiger
  Neo 3.0 at 670W max output, 24.8% module efficiency [38]; Q1 average output 655–660W
  with >640W products at ~25% of shipments [2]. The mix shift is real but was only a
  quarter of Q1 volume — getting to >60% by year-end is a second stretch target sitting
  alongside the shipment target.
- **App ranks / web traffic / job postings / reviews: not applicable or unavailable** for
  a Chinese industrial manufacturer; no attempt is recorded as a success.

---

## 7. Forensics

### A reporting-regime change that is itself the finding

JinkoSolar filed **seven Form 3 initial ownership statements on 17–18 March 2026** — the
first Section 16 filings in the company's history — followed by **nine Form 4s and six
Form 144s** in 2026 [25]. Prior to March 2026 the CIK shows only 6-Ks, 20-Fs, 13D/Gs and
144s. Yet the company **continues to file 6-Ks captioned "Report of Foreign Private
Issuer"**, including on 2026-08-14 [1][18][19].

I could not source an explanation for this (no 6-K, press release or news item found
announcing a change in FPI status). The observable fact stands on its own and is
useful either way: **as of March 2026 JinkoSolar insiders are reporting transactions on
Form 4 in near-real time, which they never had to do before.** That is why the following
is knowable at all.

### Form 4 activity — all discretionary, all sales, no buys

Every sale below carries `aff10b5One = 0` — i.e. **not made under a Rule 10b5-1 plan**
[21][22][23].

| Date | Insider | Role | Transaction | Price | Post-transaction | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-05-01 | **Li Xiande** | CEO & director, co-founder | **+1,777,142** ordinary shares — PSU vest (2023 plan) | $0 | 4,550,062 ord. | [23a] |
| 2026-05-01 | Li Xianhua | Director, co-founder | +771,428 ordinary — PSU vest | $0 | 11,629,612 ord. | [23b] |
| 2026-05-01 | Cao Haiyun | Director (now CEO of Jiangxi Jinko) | +354,285 ordinary — PSU vest | $0 | 354,285 ord. | [23c] |
| 2026-05-01 | Li Mengmeng | **CFO** | +2,856 ordinary — PSU vest | $0 | 2,856 ord. | [23d] |
| **2026-05-13** | **Li Xianhua** | Director, co-founder | **SELL 1,280,000 ordinary (= 320,000 ADS)** | **$25.53/ADS** wtd avg (range $24.76–26.00) | 10,349,612 ord. | [21] |
| **2026-05-13** | Siew Wing Keong | Independent director | **SELL 16,000 ADS** | **$26.11** wtd avg ($26.00–26.29) | 186,000 ord. | [22a] |
| **2026-05-13** | Stephen Markscheid | Independent director | **SELL 2,000 ADS** | **$25.00** | 20,000 ADS | [23e] (Form 4/A, 2026-05-20) |
| **2026-06-30** | Siew Wing Keong | Independent director | **SELL 16,000 ADS** | **$16.49** | 170,000 ord. | [22b] |
| 2026-07-01 | Siew Wing Keong | Independent director | +10,000 ordinary — RSU vest | $0 | 10,000 ord. | [22b] |
| 2026-07-01 | Stephen Markscheid | Independent director | +10,000 ordinary — RSU vest | $0 | 10,000 ord. | [23f] |

**Six Form 144 notices of proposed sale** were filed in 2026: 2026-05-05, 2026-05-13 (×2),
2026-05-19 [25]. The 2026-05-19 notice (Siew Wing Keong) proposes 6,000 ADS,
aggregate market value $150,000, approximate sale date 05/19/2026, broker The Core
Securities Company Limited, Hong Kong; it also confirms **52,370,188 ADS outstanding**
[24].

**Reading it:**
- **Three of the company's directors, including a co-founder, sold on the same day
  (2026-05-13) at $25.00–$26.11, discretionarily, five days after announcing the sale of
  the US subsidiary and two weeks after a large PSU vest.** The stock is now $16.16 —
  **36% below where they sold.**
- Li Xianhua's sale alone was ~$8.2m.
- Siew sold the identical 16,000-ADS block again on 30 June at $16.49, a 37% lower
  price — that repetition looks mechanical/liquidity-driven rather than informed.
- **There is not a single insider purchase on the record.** The one apparent buy
  (Markscheid, code P) was corrected by a Form 4/A on 2026-05-20 to a sale [23e].
- **No insider transactions at all since 2026-07-02** — an eight-week quiet period
  consistent with a closed window into the print. Nothing has been signalled by
  transactions in the run-up.

### Executive / director departures

**Kangping Chen resigned as CEO of Jiangxi Jinko effective 2026-03-16** after five years
in the role and as a co-founder of the group; replaced by Haiyun (Charlie) Cao, formerly
JKS Holding CFO 2014–2021 [20][31]. Chen remains a director, joins the strategy and
sustainability committee, and is appointed deputy chairman subject to shareholder
approval. Framed as a promotion-plus-succession rather than a departure, and Chen has
not exited the group.

### Auditor, restatements, filing language

- **FY2025 Form 20-F filed 2026-04-29** [25], within the four-month deadline. No
  delinquency.
- **No auditor change, restatement, material-weakness disclosure or SEC comment-letter
  activity found in 2026.** (28 CORRESP and 15 UPLOAD filings exist on the CIK but none
  are dated 2026 in the recent block [25]. I did not read the 20-F's ICFR section — see
  coverage gaps.)
- **One correction notice exists on the FY2025 results release** — the PR Newswire item
  is headed "/C O R R E C T I O N — JinkoSolar Holding Co., Ltd./" [27]. I could not
  determine what was corrected.

### Reporting-cadence red flags (the real pattern)

| Quarter | Reported | Gap from quarter end |
| --- | --- | --- |
| Q2 2025 + Q3 2025 | **2025-11-17, combined into a single release** [28] | 140 days / 48 days |
| Q4/FY2025 | **2026-04-16** [27] | 106 days |
| Q1 2026 | 2026-04-29 [2] | 29 days |

**JinkoSolar skipped a standalone Q2 2025 report entirely and folded it into the Q3
release four and a half months after quarter end, then reported FY2025 in mid-April
rather than March, then reported Q1 2026 thirteen days later.** The current print, at 57
days after quarter end, is the most timely release in over a year. There is no filed
explanation for the Q2 2025 delay that I could find. Two observations follow: (a) the
company has demonstrated it will withhold a quarter when the numbers are bad — the
combined release covered the two worst-margin quarters of the cycle; (b) the fact that
this print is *on time and on the originally announced date* is, in itself, mildly
reassuring.

### 8-K / 6-K cadence

18 6-Ks since June 2025, 8 of them in 2026 [25]. The 2026 sequence is unusually
event-dense for this issuer: subsidiary CEO change (03-16), FY results notice (03-24),
Q1 results notice (04-20), FY2025 results (04-16), Q1 results + 20-F (04-29), US
subsidiary disposal announced (05-08), disposal closed (06-01), dividend (06-12),
Q2 date (08-14). **Nothing filed between 2026-06-12 and 2026-08-14** — a two-month
silence immediately preceding the print, with no pre-announcement, no guidance update
and no 6-K.

### Third-party investigation — live headline risk

**2026-08-13, Hunterbrook Media** published an investigation alleging that FH JKV
Holdings — the buyer of 75.1% of Jinko's Jacksonville plant — is ultimately controlled by
**Zhang Wei, wife of Suntech founder Zhengrong Shi**, with their sons Dennis and Mitchell
Shi as directors, through a Hong Kong entity (Fortune Harmony Investments) and a BVI
parent (Prosper Bright Ventures) [17]. The article identifies three unresolved FEOC/OBBBA
questions: whether Treasury will treat Hong Kong as China; whether Jinko's continued
ownership of the US trademarks constitutes "effective control" via IP licensing; and
whether the ~$94m deferred purchase price counts as debt under the control test [17].
JinkoSolar did not respond to a request for comment. FH Capital says it acted only as an
investment adviser and that Shi and Zhang are Australian citizens [17]. Hunterbrook
disclosed no position [17].

**The stock did not react:** 2026-08-13 closed −0.79% at $16.29 on 268,000 shares — the
lightest volume in the sample — and rose +2.82% the next day [8]. **This risk is
unpriced.** If it surfaces in Wednesday's Q&A, or if the disposal accounting is
questioned, it is a tail. If it does not, it is nothing.

---

## 8. Macro & peer read-through

### Sector and factor regime — hostile

| | Level | 3-month | 1-month | As of |
| --- | --- | --- | --- | --- |
| TAN (Invesco Solar ETF) | 48.32 | **−29.9%** | −5.8% | 2026-08-24 [8] |
| FSLR | 208.31 | **−22.8%** | +2.7% | 2026-08-24 [8] |
| CSIQ | 14.32 | — | +4.8% (1mo) | 2026-08-24 [8] |
| DQ | 14.43 | — | +21.8% (1mo) | 2026-08-24 [8] |
| S&P 500 | 7,652.86 | +1.8% | +3.2% | 2026-08-24 [8] |
| US 10-year | 4.70% | +4.7% (in yield) | +0.5% | 2026-08-24 [8] |
| USDCNY | 6.7079 | — | — | 2026-08-25 [34] |

Solar has underperformed the S&P by ~32 points over three months while rates rose. This
is a factor-hostile tape for a levered, loss-making, long-duration renewable name. Note,
though, that the last month has been a *bottoming* tape — DQ +21.8%, CSIQ +4.8%, FSLR
+2.7%, JKS +9.2% over 21 sessions [8] — driven by the two policy events below.

### Peers that have already reported

**Daqo New Energy (DQ), polysilicon, reported 2026-08-20 BMO** [10]:
- EPS **−$1.20 vs −$0.57 consensus — a large miss** [43a]; revenue $62.7m (beat, but on a
  tiny base) [10][43a].
- **Polysilicon ASP $4.04/kg vs $5.96/kg in Q1 — down 32% sequentially**, and below the
  $5.95/kg production cost [10]. Gross margin −132.0% [10].
- Prices fell from RMB35–37/kg in Q1 to **RMB31–34/kg in Q2** [10].
- Industry polysilicon output **−9.8% YoY in H1 2026**; Daqo ran at **57% of nameplate**
  [10]. Net loss $81.2m; cash $555.3m, no debt [10].
- **But management said "polysilicon prices are beginning to show signs of a recovery,
  with spot prices stabilizing and forward prices rebounding by more than 10%"** [10].
- Price action: **DQ closed +6.62% on the print day** despite the miss, then −9.35% the
  next session and +6.26% on 8/24 [8]. Reporting suggests it fell as much as 14.6%
  intraday before recovering [43b]. **The market bought the policy narrative and sold the
  quarter.** That is the single most instructive peer datum for JKS.

**Read-through to JKS, two directions:**
- *Negative:* Daqo confirms Q2 was a weak-demand, high-inventory, falling-price quarter
  across the chain [10]. A 32% QoQ fall in poly ASP is not consistent with a firm module
  market, and JKS's own Q1 claim that prices would "remain relatively stable" [2] looks
  optimistic.
- *Positive:* falling polysilicon is an **input-cost tailwind** for a module maker. JKS
  explicitly blamed Q4 2025's margin collapse on "rising costs of raw materials such as
  polysilicon and silver" [27]. That headwind reversed in Q2. Combined with module prices
  that InfoLink puts at RMB0.65–0.73/W for ground-mount in early August versus
  RMB0.68–0.73/W in mid-June [13], the module-vs-poly spread should have widened. **This
  is the strongest quantitative argument that JKS's Q2 gross margin holds or beats 8.3%.**

**Canadian Solar (CSIQ) reports 2026-08-27 — the day after JKS**, with revenue expected
$1.17bn, −31.2% YoY [43c]. It is not a read-in, but it means JKS's print will be traded
as a read-through for CSIQ, which can amplify the move in either direction.

### China policy — the anti-involution cycle

- **China H1 2026 solar installations 72.07 GW, −66% YoY** from 212.21 GW (distorted by a
  2025 pull-forward ahead of Document No. 136 market-based pricing) [12]. Wafer output
  −7.3%, cell −21.9%, **module output −35.1% to 201.3 GW** [11]. CPIA full-year forecast
  180–240 GW versus ~315 GW in 2025 — **China's first annual decline since 2019** [11].
- Exports: module volumes −2.5%, cell exports +36.8%, total wafer/cell/module export value
  $17.18bn, +24.3% YoY [11].
- **Policy stack tightening** [10]: energy-consumption standards effective 2027-01-01 with
  shutdown risk above 6.3 kgce/kg (tightened from the proposed 6.4); CPIA cost-accounting
  guidelines issued 2026-07-27; SAMR price-compliance guidance 2026-07-31 to "curb
  irrational low-price competition"; and an **industry pledge signed 2026-08-06 by Daqo
  and seven competitors to eliminate below-cost sales**.
- Pricing: TOPCon cells peaked ~RMB0.45/W in February on high silver costs, fell to the
  cash-cost band of RMB0.26–0.27/W by July [13]. Modules RMB0.68–0.73/W (ground) and
  RMB0.73–0.82/W (distributed) in mid-June; RMB0.65–0.73/W and RMB0.70–0.76/W in early
  August [13]. **Module prices drifted down slightly through Q2 into August.**

### US trade policy — a large, recent, two-sided shock

**On 2026-08-06 President Trump signed a Section 232 proclamation** on polysilicon and
downstream derivatives [14][15]:
- **Minimum import prices, effective 2026-12-04: $21/kg polysilicon, $100/kg ingots and
  wafers, $0.22/W cells, $0.38/W modules.**
- A separate **15% ad valorem duty** (10% for the UK).
- CBP will require importer certification of compliant US sale prices, with a carve-out
  for fixed-term contracts entered before 2026-08-06.

A **$0.38/W module floor against Chinese modules currently quoted around $0.09–0.12/W FOB
[35b]** is a price floor roughly 3–4× the world price. This all but eliminates the
US as an addressable import market for Chinese modules — but that market was already
largely closed to JinkoSolar by AD/CVD and UFLPA, and JinkoSolar has just sold 75.1% of
its US manufacturing base. The solar complex **rallied** on the news (JKS +2.53% on 8/6
and +5.13% on 8/7; DQ +8.63% on 8/7; TAN +2.93% on 8/7 [8]), reading global price floors
as margin-supportive. My read: **modestly positive for JKS globally, and now largely
irrelevant to its own US operations**, but it raises input costs for the 24.9%-owned
Jacksonville plant, which imports cells.

**Retroactive AD/CVD:** the Court of International Trade ordered retroactive collection on
Southeast Asian solar imports from April 2022 – June 2024, and the government decided in
February 2026 not to appeal [35c]. Commerce **preliminarily determined that the mandatory
Vietnamese respondents, JA Solar and JinkoSolar, did not have critical circumstances —
i.e. JinkoSolar was excluded from the retroactive duties** [35c]. A search snippet
asserting JinkoSolar faces "a substantial cash liability due to retroactive tariffs on its
Southeast Asian imports" [26a] contradicts that primary finding; I do not treat the
liability claim as established, but it is a residual uncertainty worth listening for on
the call.

### Customer / supplier read-throughs

- **Supplier (Daqo):** 57% utilisation, ASP below cash cost, forward prices up >10% [10] →
  supports a Q2 cost tailwind and an H2 cost headwind for JKS.
- **Downstream (First Solar):** −22.8% over three months [8] despite being the primary
  beneficiary of Section 232 — the market is not paying up for solar policy wins.
- **A-share sibling:** Jinko Solar Co. (688223.SH) closed CNY 4.34 on 2026-08-25, −15.7%
  since 22 June, −55% from its 52-week high of CNY 9.66, and traded 47.0m shares [33].
  **The A-share market has NOT pre-announced the H1 result** — I found no 业绩预告 for
  688223 (the pre-announcements retrieved belong to 晶科科技/JinkoPower, 601778, a
  different company) [44]. Chinese semi-annual reports are due by 31 August, so 688223's
  H1 filing is due within days *after* the ADS print. Note the sequencing: JKS reports at
  08:30 ET on 26 August = 20:30 Beijing, i.e. **after** the A-share close that day, so the
  A-share reacts on 27 August rather than pre-signalling.

---

## 9. Bull case / bear case / base case

### Bull case

The Q2 print confirms the margin inflection and the FY guide survives. The evidence:
gross margin already went 0.3% → 8.3% in one quarter [2]; polysilicon — JKS's largest
input and the thing it blamed for Q4 2025's collapse [27] — fell 32% sequentially in Q2
[10] while module prices barely moved (RMB0.68–0.73/W in June to RMB0.65–0.73/W in
August [13]), so the spread widened; the EPS bar of −$0.75 requires only ~8% gross margin,
which is what management already guided [own calc; 6][30]; ESS is ramping toward ~10 GWh
at ~15% margin, roughly double module margins, with Q1's 1.42 GWh shipped but only 520 MWh
recognised, i.e. a revenue backlog that lands later [2][30]; announced order flow is
healthy and geographically diversified [38]; the $191.5m US disposal may drop a one-time
gain into Q2 that consensus does not model [18][19]; Section 232 puts a $0.38/W floor
under US module prices from December [14][15]; and the anti-involution stack — the 6 August
below-cost-sales pledge, the 2027 energy-consumption standards, SAMR pricing guidance —
is the same policy narrative that produced a **+13.09%** print on 17 November 2025 [10][28].
Against a $846m market cap holding a 55.59% stake in a listed subsidiary worth ~$3.69bn
[3][33][34][37], with 9.4% of the float short and 4.5 days to cover [4], a 9.3% dividend
[29], and options pricing essentially no event premium [9], the upside convexity is real.

### Bear case

The FY2026 shipment guidance of 75–85 GW is arithmetically indefensible and gets cut. H1
lands at 27.7–29.7 GW [2], meaning H2 must deliver 45.3–57.3 GW against 44.2 GW in H2
2025 [27][28] — a swing from −31% YoY to flat-or-better — in a year when Chinese
installations fell 66% in H1 [12], Chinese module output fell 35.1% [11], the CPIA sees
the first annual decline since 2019 [11], and management's own demand forecast is −5 to
−10% [30]. Roth already flagged the gap on the Q1 call and got no satisfactory answer
[30]. The peer print says Q2 was a weak-demand, high-inventory, falling-price quarter
across the chain, with Daqo missing EPS by more than 100% and running at 57% utilisation
[10]. FY2025 free cash flow was −RMB2.1bn with operating cash flow down 94% [26];
inventory rose on a 29% revenue decline [26]; convertible debt is $1.52bn against an
$846m market cap [26]. Three directors including a co-founder sold discretionarily —
**not** under 10b5-1 — at $25–26 in May, 36% above today's price, and nobody has bought
anything, ever [21][22][23]. The company has already demonstrated it will withhold a bad
quarter (Q2 2025 was never reported standalone) [28]. And the positioning is the wrong
way round: 223 bullish to 2 bearish Stocktwits messages over three weeks [32], a 0.03
put/call volume ratio with 500 far-OTM Sep-25 calls bought on the last session [9], and
a sell side whose $25 price targets have not been marked down at all through a 42% decline
[5][6]. When the guidance cut lands, there is no hedged base to absorb it.

### Base case

A quarter that is fine on the numbers and unresolved on the guidance. Q2 revenue lands
near $2.1–2.3bn with gross margin roughly flat at 7.5–9% and an attributable loss around
−$0.60 to −$0.90/ADS — i.e. a print that neither clears nor fails the low bar consensus
has set [own calc; 2][6][30]. FY2026 shipment guidance is trimmed rather than abandoned
— my central expectation is a move to something like 65–75 GW, presented alongside
unchanged H2 margin-jump language and a louder ESS story, because that is the pattern
management used in Q1 (bad volumes, good margins, intact narrative) and it produced only
a −3.67% reaction [2][8]. Base rates support a modest move: the median absolute one-day
reaction over the last eight prints is 4.39%, and half of them moved less than that [8].
The disposal accounting and the Hunterbrook questions are the two things most likely to
turn a modest move into a violent one, in either direction. **I lean modestly negative**
— the concrete, near-certain catalyst (a guidance cut) is negative, the peer read is
negative, the positioning is one-sidedly long, and four of the last six prints were down
— but conviction is capped by how washed out the stock already is (−42% YTD, 0.38× book,
a 61–77% SOTP discount) and by the genuine possibility of a disposal gain.

---

## 10. What would flip the consensus view

**The most credible reversal is a reaffirmed 75–85 GW FY2026 shipment guide backed by a
specific, quantified H2 order book.** Concretely: management holds the range, states an
H2 contracted/order-book coverage figure above ~70%, reports Q2 gross margin at or above
9%, raises or reaffirms the ~10 GWh ESS target with Q2 recognised ESS revenue materially
above Q1's 520 MWh, and books a clean gain on the Jacksonville disposal. That combination
would (a) invalidate the arithmetic that is the entire bear case, (b) validate the
polysilicon-spread margin story that Daqo's ASP collapse implies, and (c) leave a stock
at 0.38× book, 9.4% of float short, 4.5 days to cover, with a call book already
positioned for it and no put hedges to sell into a rally. On the November 2025 template
that is a +10% to +15% day, and the options market — pricing under 5% for the event — is
not set up for it.

The mirror-image reversal of the *bull* case is narrower and more specific: a
**writedown**. FY2025 inventory rose to RMB14.48bn on a 29% revenue decline and Q1 2026
receivables stood at RMB13.77bn [2][26]. An inventory or receivable impairment large
enough to push the attributable loss past ~−$1.50/ADS would break the margin-inflection
narrative outright, and on the April 2026 template that is a −10% to −12% day.

A third, lower-probability flip: **management is asked on the call about the Hunterbrook
allegations and gives an unsatisfactory answer**, or discloses that Treasury FEOC guidance
puts the Jacksonville 45X credits at risk. That is worth $146m/year of credits to an
asset JKS now owns 24.9% of [17] — small in cash terms, large in narrative terms for a
company whose entire equity value is a governance discount.

---

## 11. Note on the triage rationale

Triage selected JKS as "a Chinese solar manufacturer in an overcapacity/pricing-pressure
cycle with a history of violent prints; peer solar reports already out and module-pricing
data give a genuine read-through edge." **Two of the three legs hold; one does not.**

- **Overcapacity/pricing cycle: confirmed and then some** — China H1 installs −66%,
  module output −35.1%, first annual decline since 2019 [11][12].
- **Peer read-through edge: confirmed** — Daqo's 20 August print gives a hard, dated,
  quantified read on Q2 supply-chain pricing (poly ASP −32% QoQ) plus a traded reaction
  pattern (+6.6% on a big miss) [10][8].
- **"History of violent prints": overstated.** The median absolute one-day reaction over
  the last eight prints is **4.39%**, and four of eight were under 4% [8]. Only two of
  eight exceeded 10%. JKS is a fat-tailed but not reliably violent earnings stock, and
  the options market's flat term structure [9] is, on this evidence, closer to right than
  the triage framing implies. The correct expectation is a modest move with real tail
  risk, not a guaranteed large move.

One thing triage could not have known and which I would flag as the more interesting edge:
**the EPS bar is a restatement of guidance, so this print resolves on the FY shipment
guide and on the accounting for a $191.5m US disposal that consensus almost certainly
has not modelled.**

---

## 12. Coverage gaps

1. **No published event-implied move exists for JKS.** No weekly options; earnings-watcher
   does not cover it; Market Chameleon and OptionSlam are paywalled. My ~4.6% figure is
   computed from CBOE delayed quotes with a ±3-point IV sensitivity that swings the answer
   from ~0% to ~8%. *Matters enormously* — the panel's entire risk frame depends on this
   number, and it should be treated as a wide prior, not an anchor.
2. **IV rank / IV percentile: unavailable.** No free historical-implied-vol source
   reachable. I substituted an RV30 percentile (9th percentile of trailing year) and the
   IV30/RV30 ratio (1.54). *Matters* — I cannot say whether 67% IV30 is cheap or dear for
   this name specifically.
3. **Borrow fee / cost to borrow: unavailable.** Fintel Cloudflare-blocked, iBorrowDesk
   empty reply, ORTEX paywalled. *Matters* — 9.4% of float is short and the borrow rate
   is the best available proxy for how hard-conviction that short base is.
4. **Short-interest settlement date: unavailable.** stockanalysis shows 2.85m / 7.36% /
   4.50 days-to-cover with no as-of date, and NYSE names are not in Nasdaq's short-interest
   API. Three other providers give mutually inconsistent figures (1.90m, 2.51m, 5.83m).
   *Matters* — a stale short-interest number is a stale positioning read.
5. **30/60/90-day estimate revision series: unavailable in numeric form.** Zacks detailed
   estimates not reachable. Only three dated rating actions found, the most recent
   substantive one from 29 May. *Matters* — I cannot tell whether the −$0.75 has been
   drifting down into the print.
6. **Consensus providers disagree.** MarketBeat says −$0.75 / $2.166bn; an unidentified
   provider says −$0.62 / $3.01bn. *Matters* — a $0.13 EPS spread on a −$0.75 base is 17%
   of the number.
7. **Whisper number: none published.** Expected for a 7-analyst, $846m ADS.
8. **Google Trends: HTTP 429 from this environment.** Low materiality for a B2B name.
9. **Customer concentration: not sourced.** The FY2025 20-F was accessed via XBRL only,
   not read narratively. *Matters moderately* — a large single customer would change the
   shipment-guidance risk profile.
10. **The FY2025 20-F ICFR / material-weakness section was not read.** I confirmed timely
    filing and found no auditor change, but I did not verify the internal-control opinion.
    *Matters* — given the Q2 2025 reporting delay, an ICFR qualification would be
    material and I cannot rule one out.
11. **The "/CORRECTION/" on the FY2025 results release is unexplained.** I could not
    determine what was corrected.
12. **No explanation found for the March 2026 onset of Section 16 (Form 3/4) filing**
    while the company still files as a foreign private issuer. *Matters* — the mechanism
    might imply a change in the company's US reporting obligations that I have not
    identified.
13. **Q2 2026 disposal accounting is unknowable pre-print.** Whether the $191.5m
    Jacksonville sale produces a gain, a loss, or is treated as an equity-method
    remeasurement will materially move headline EPS and no consensus I found models it.
14. **Q1 2025 earnings date (2025-04-29) is snippet-only** (MarketBeat), unlike the other
    seven dates which are primary-sourced. The associated −3.85% reaction is therefore
    the weakest row in the historical-move table.
15. **688223 shares outstanding (10.27bn) is snippet-only** (Simply Wall St), which flows
    into the SOTP arithmetic. The conclusion (a very large discount) is robust to a
    ±20% error in that figure; the precise 61–77% range is not.
16. **The A-share subsidiary's H1 2026 result is not yet public** and is due by 31 August.
    A pre-announcement in the next 24 hours would be a live pre-signal I cannot see.
17. **ir.jinkosolar.com returned HTTP 503** throughout; all company material came via SEC
    EDGAR and PR Newswire instead. **fintel.io** and **marketchameleon.com** were
    blocked/paywalled. **trends.google.com** rate-limited.

---

## 13. Sources

1. SEC Form 6-K Ex-99.1, filed 2026-08-14 — earnings date, BMO session, 08:30 ET call, Q2 2026 quarter end. https://www.sec.gov/Archives/edgar/data/0001481513/000110465926097046/tm2623266d1_ex99-1.htm
2. PR Newswire — JinkoSolar Announces First Quarter 2026 Financial Results (2026-04-29): revenue, gross margin, opex, net loss, loss per ADS, shipments, ESS, balance sheet, Q2 and FY2026 guidance, CEO commentary. https://www.prnewswire.com/news-releases/jinkosolar-announces-first-quarter-2026-financial-results-302757116.html
3. stockanalysis.com/stocks/jks — spot $16.16 (2026-08-24 16:00 EDT), market cap $846.30m, shares 52.37m, 52-week range, TTM revenue/EPS, dividend, analyst consensus. https://stockanalysis.com/stocks/jks/
4. stockanalysis.com/stocks/jks/statistics — short interest 2.85m / 7.36% / 4.50 days to cover, float 30.30m, beta 0.50, 20-day avg volume, EV, total debt, cash, book value, 52-week change. https://stockanalysis.com/stocks/jks/statistics/
5. stockanalysis.com/stocks/jks/forecast — 7 analysts, $25.44 avg PT ($15.00–$32.61), rating split, FY2026/FY2027 revenue and EPS forecasts. https://stockanalysis.com/stocks/jks/forecast/
6. DailyPolitical (MarketBeat syndicate), 2026-08-24 — consensus EPS −$0.75, revenue $2.166bn, market cap, 50/200-day MAs, rating breakdown, PT $24.38, UBS and Wall Street Zen actions, institutional/insider ownership, leverage ratios. https://www.dailypolitical.com/2026/08/24/jinkosolar-jks-projected-to-release-earnings-on-wednesday.html
7. MarketBeat instant alert, 2026-08-19 — consensus, MAs, PT, Siew Wing Keong 2026-06-30 sale, ownership. https://www.marketbeat.com/instant-alerts/jinkosolar-jks-to-announce-earnings-on-wednesday-2026-08-19/
8. Yahoo Finance chart API (JKS, DQ, CSIQ, FSLR, TAN, ^GSPC, ^TNX, 688223.SS) — all daily OHLC, all earnings-day reaction calculations, run-up windows, realised vol, dividend ex-dates. https://query1.finance.yahoo.com/v8/finance/chart/JKS
9. CBOE delayed option quotes, snapshot 2026-08-24 23:43:56 — full JKS chain, IV30 67.04%, spot $16.16, all implied-move / term-structure / skew / OI / volume analysis. https://cdn.cboe.com/api/global/delayed_quotes/options/JKS.json
10. PR Newswire — Daqo New Energy Q2 2026 results (2026-08-20): revenue, poly ASP $4.04/kg, cost $5.95/kg, gross margin, net loss, cash, industry output, 57% utilisation, anti-involution policy stack, Q3/FY guidance, price-recovery commentary. https://www.prnewswire.com/news-releases/daqo-new-energy-announces-unaudited-second-quarter-2026-financial-results-302856319.html
11. pv magazine, 2026-07-29 — China's first annual solar contraction since 2019; H1 wafer/cell/module output; export data; CPIA 180–240 GW forecast; Document No. 136. https://www.pv-magazine.com/2026/07/29/chinas-solar-market-heads-for-first-annual-contraction-since-2019/
12. TaiyangNews / CPIA — China H1 2026 PV installations 72.07 GW, −66% YoY. https://taiyangnews.info/markets/cpia-china-h1-2026-solar-pv-istallations-drop-66-percent-yoy
13. InfoLink Consulting PV spot price commentary, 2026-08-05 — TOPCon module RMB0.65–0.73/W (ground) and RMB0.70–0.76/W (distributed) in early August; mid-June levels; cell price path from RMB0.45/W to RMB0.26–0.27/W. https://www.infolink-group.com/energy-article/pv-spot-price-20260805
14. pv magazine USA, 2026-08-07 — Section 232 proclamation signed 2026-08-06, minimum import prices on polysilicon and modules. https://pv-magazine-usa.com/2026/08/07/us-announces-tariffs-minimum-import-price-on-polysilicon-imports/
15. White & Case — Section 232 tariffs and price floors: $21/kg polysilicon, $100/kg ingots/wafers, $0.22/W cells, $0.38/W modules; 15% ad valorem; effective 2026-12-04; CBP certification. https://www.whitecase.com/insight-alert/president-trump-orders-tariffs-and-price-floors-polysilicon-section-232-action
16. PV Tech, 2026-05-11 — JinkoSolar sells 75.1% of its US manufacturing business; 2 GW Jacksonville plant; retains 24.9%; FEOC context; peer behaviour (Trina, JA Solar). https://www.pv-tech.org/jinkosolar-sells-majority-stake-in-us-manufacturing-business/
17. Hunterbrook Media, 2026-08-13 — investigation into FH JKV Holdings' ultimate control (Zhang Wei / Zhengrong Shi family), $146m of 2025 45X credits, ~$94m deferred consideration, three unresolved FEOC/OBBBA questions, FH Capital and JinkoSolar responses, no-position disclosure. https://newsletter.hntrbrk.com/p/the-entity-that-bought-jinkos-florida
18. SEC Form 6-K filed 2026-06-01 — closing of the disposal of 75.1% of Jinko Solar (U.S.) Industries Inc. https://www.sec.gov/Archives/edgar/data/1481513/000110465926068540/tm2616503d1_6k.htm
19. SEC Form 6-K filed 2026-05-08 — definitive agreement to sell 75.1% of Jinko Solar (U.S.) Industries Inc. to FH JKV Holdings Limited for ~US$191.5m subject to NAV adjustment. https://www.sec.gov/Archives/edgar/data/1481513/000110465926057541/tm2614056d1_6k.htm
20. SEC Form 6-K filed 2026-03-16 — Jiangxi Jinko senior management changes; Kangping Chen resigns as CEO, becomes deputy chairman. https://www.sec.gov/Archives/edgar/data/1481513/000110465926028076/tm268902d1_6k.htm
   - 20a. SEC Form 6-K filed 2026-03-24 — notice to report FY2025 results on 2026-04-16. https://www.sec.gov/Archives/edgar/data/1481513/000110465926033612/tm269685d1_6k.htm
   - 20b. SEC Form 6-K filed 2026-04-20 — notice to report Q1 2026 results on 2026-04-29. https://www.sec.gov/Archives/edgar/data/1481513/000110465926045252/tm2612226d1_6k.htm
21. SEC Form 4, Li Xianhua, filed 2026-05-15 — sale of 1,280,000 ordinary shares (320,000 ADS) on 2026-05-13 at $25.53 wtd avg; aff10b5One = 0. https://www.sec.gov/Archives/edgar/data/1481513/000110465926061816/xslF345X06/tm2614761-1_4seq1.xml
22. SEC Forms 4, Siew Wing Keong — (a) filed 2026-05-15, sale of 16,000 ADS on 2026-05-13 at $26.11; (b) filed 2026-07-02, sale of 16,000 ADS on 2026-06-30 at $16.49 plus 10,000-share RSU vest 2026-07-01; both aff10b5One = 0. https://www.sec.gov/Archives/edgar/data/1481513/000110465926061818/xslF345X06/tm2614765-1_4seq1.xml and https://www.sec.gov/Archives/edgar/data/1481513/000110465926080105/xslF345X06/tm2619656-2_4seq1.xml
23. SEC Forms 4 filed 2026-05-04 (PSU vestings, 2023 Equity Incentive Plan, vested 2026-05-01) and related: (a) Li Xiande, CEO, +1,777,142 ordinary — https://www.sec.gov/Archives/edgar/data/1481513/000110465926054450/xslF345X06/tm2613204-2_4seq1.xml ; (b) Li Xianhua +771,428 — .../000110465926054454/... ; (c) Cao Haiyun +354,285 — .../000110465926054456/... ; (d) Li Mengmeng, CFO, +2,856 — .../000110465926054463/... ; (e) Form 4/A, Stephen Markscheid, filed 2026-05-20, sale of 2,000 ADS at $25.00 on 2026-05-13, aff10b5One = 0 — https://www.sec.gov/Archives/edgar/data/1481513/000149497126000003/xslF345X06/primary_doc.xml ; (f) Form 4, Markscheid, filed 2026-07-02, 10,000-share RSU vest — .../000110465926080103/...
24. SEC Form 144, Siew Wing Keong, filed 2026-05-19 — 6,000 ADS proposed, $150,000 aggregate, broker The Core Securities Company Limited (Hong Kong); confirms 52,370,188 ADS outstanding and 1 ADS = 4 ordinary shares. https://www.sec.gov/Archives/edgar/data/1481513/000110465926063565/primary_doc.xml
25. SEC EDGAR submissions index, CIK 0001481513 — complete filing history: 6-K cadence, first-ever Form 3s on 2026-03-17/18, nine Form 4s, six Form 144s in 2026, FY2025 20-F filed 2026-04-29. https://data.sec.gov/submissions/CIK0001481513.json
26. SEC XBRL company facts, CIK 0001481513 — FY2022–FY2025 gross profit, operating income, net income, operating cash flow, capex, cash, inventory, short-term borrowings, convertible debt, equity, NCI, R&D, total assets/liabilities. https://data.sec.gov/api/xbrl/companyfacts/CIK0001481513.json
   - 26a. TipRanks JKS page — Weiss Ratings Sell (D) reissued 2026-08-03; most recent single PT $24.00; Spark AI "Neutral"; retroactive-tariff claim (unverified). https://www.tipranks.com/stocks/jks
   - 26b. TipRanks/The Fly — Jefferies PT raised to $65.43 (undated, disregarded). https://www.tipranks.com/news/the-fly/jinkosolar-price-target-raised-to-65-43-from-36-69-at-jefferies
27. PR Newswire — JinkoSolar Announces Fourth Quarter and Full Year 2025 Financial Results (2026-04-16, carries a "/CORRECTION/" header): FY2025 net loss RMB4.45bn, 86.06 GW shipments, revenue RMB65.50bn, Q4 revenue and margin commentary on polysilicon and silver costs. https://www.prnewswire.com/news-releases/jinkosolar-announces-fourth-quarter-and-full-year-2025-financial-results-302744662.html
28. PR Newswire — JinkoSolar Announces Second and Third Quarter 2025 Financial Results (2025-11-17, combined release): Q2 2025 revenue RMB17.99bn/$2.51bn, 26,446 MW total shipments (24,334 MW modules), 2.9% gross margin, RMB876.4m/$122.3m net loss. https://www.prnewswire.com/news-releases/jinkosolar-announces-second-and-third-quarter-2025-financial-results-302617065.html
29. PR Newswire — JinkoSolar Announces Cash Dividend (2026-06-12): $0.375/ordinary share, $1.50/ADS, ~$78.5m, record 2026-06-22, payable ~2026-07-09. https://www.prnewswire.com/news-releases/jinkosolar-announces-cash-dividend-302798902.html
30. Investing.com — JinkoSolar Q1 2026 earnings call transcript: CFO Tan Yi on Q2 margins "relatively stable" and the H2 "jump"; ~10 GWh ESS target at ~15% gross margin; 2026 demand −5 to −10%; US JV commentary; Philip Shen's question on the 14–15 GW pace versus the 75–85 GW annual guide. https://www.investing.com/news/transcripts/earnings-call-transcript-jinkosolar-q1-2026-shows-eps-beat-stock-dips-93CH-4645395
31. pv magazine, 2026-03-20 — JinkoSolar appoints new CEO (Haiyun/Charlie Cao at Jiangxi Jinko). https://www.pv-magazine.com/2026/03/20/chinese-pv-industry-brief-jinkosolar-appoints-new-ceo/
32. Stocktwits public API, JKS stream, 240 messages 2026-08-03 → 2026-08-25 — sentiment tagging by bucket, message-volume trend, watchlist count 10,701. https://api.stocktwits.com/api/2/streams/symbol/JKS.json
33. Yahoo Finance — Jinko Solar Co., Ltd. (688223.SS): CNY 4.34 close 2026-08-25, 52-week range CNY 3.92–9.66, volume 47.0m, daily series since 2026-06-22. https://finance.yahoo.com/quote/688223.SS/
34. Yahoo Finance — USDCNY 6.7079 as of 2026-08-25. https://query1.finance.yahoo.com/v8/finance/chart/CNY=X
35. Trade-policy and price sources: (a) short-interest snippet aggregation across Fintel/Benzinga/GuruFocus (mutually inconsistent, unused) https://fintel.io/ss/us/jks ; (b) module price levels ~$0.085–0.12/W FOB https://www.openpr.com/news/4607627/solar-module-prices-2026-tracker-report-shows-china-floor ; (c) Solar Power World — CIT retroactive duties, government declines to appeal (Feb 2026), JinkoSolar and JA Solar excluded as mandatory Vietnamese respondents without critical circumstances. https://www.solarpowerworldonline.com/2026/02/government-decides-to-not-appeal-cit-ruling-on-retroactive-solar-panel-tariffs/
36. EnergyTrend, 2026-04-17 — JinkoSolar FY2026 75–85 GW module guidance, ESS as growth engine, 6 GWh ESS target, April 2026 full-stack ESS product launch. https://www.energytrend.com/news/20260417-51258.html
37. Simply Wall St / search aggregation — JinkoSolar owns ~55.59% of Jiangxi Jinko after the September 2025 A-share inquiry transfer and placement; 688223 shares outstanding 10.27bn as of August 2026. *snippet_only.* https://simplywall.st/stocks/cn/semiconductors/xssc-688223/jinko-solar-shares/ownership
38. PV Tech / SolarQuarter / pv magazine order-flow items: 300 MW Tajikistan Tiger Neo 3.0 (2026-08-13); 500 MW South Korea; 1 GW Shenzhen Energy 2026–28; 6 GW TOPCon procurement win; 10 Tiger Neo 3.0 orders at SNEC 2026; Tiger Neo 3.0 at 670W / 24.8%. https://solarquarter.com/2026/08/13/jinkosolar-secures-300-mw-utility-scale-solar-project-in-tajikistan-featuring-tiger-neo-3-0/ and https://www.pv-tech.org/industry-updates/jinkosolar-signs-10-tiger-neo-3-0-orders-during-snec-2026/
39. PR Newswire — JinkoSolar Announces Third Quarter 2024 Financial Results (2024-10-30). https://www.prnewswire.com/news-releases/jinkosolar-announces-third-quarter-2024-financial-results-302291448.html
40. PR Newswire — JinkoSolar Announces Second Quarter 2024 Financial Results (2024-08-30). https://www.prnewswire.com/news-releases/jinkosolar-announces-second-quarter-2024-financial-results-302234929.html
41. Manila Times / PR Newswire — JinkoSolar Announces Fourth Quarter and Full Year 2024 Financial Results (2025-03-26). https://www.manilatimes.net/2025/03/26/tmt-newswire/pr-newswire/jinkosolar-announces-fourth-quarter-and-full-year-2024-financial-results/2080357
42. PR Newswire / Nasdaq — JinkoSolar Announces First Quarter 2024 Financial Results (2024-04-29). https://www.prnewswire.com/news-releases/jinkosolar-announces-first-quarter-2024-financial-results-302129947.html
43. Peer-print context: (a) Financial Modeling Prep — Daqo Q2 2026 EPS −$1.20 vs −$0.57 estimate, revenue beat https://site.financialmodelingprep.com/market-news/daqo-new-energy-dq-q2-2026-earnings-revenue-beat-eps-miss ; (b) Yahoo Finance — "Daqo New Energy shares tumble after Q2 earnings miss and weak polysilicon market" https://finance.yahoo.com/markets/stocks/articles/daqo-energy-shares-tumble-q2-104913637.html ; (c) MarketBeat — Canadian Solar Q2 2026 due 2026-08-27, revenue expected $1.17bn, −31.2% YoY https://www.marketbeat.com/instant-alerts/canadian-solar-csiq-expected-to-release-quarterly-earnings-on-thursday-2026-08-20/
44. Chinese-language A-share disclosure search (晶科能源 688223 半年度业绩预告) — no H1 2026 pre-announcement located for 688223; the results retrieved belong to 晶科科技 (601778, JinkoPower), a different listed company. https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_AchievementNotice/stockid/688223.phtml
45. Nasdaq quote API — JKS pre-market $16.16 at 2026-08-25 05:34 ET; prior close $16.16 (+1.51%) at 2026-08-24 16:00 ET; 52-week range; earnings date 2026-08-26. https://api.nasdaq.com/api/quote/JKS/info?assetclass=stocks
46. MarketBeat earnings report page — Q1 2025 reported 2025-04-29, EPS −$2.85 vs −$1.45 consensus, revenue $1.91bn. *snippet_only.* https://www.marketbeat.com/earnings/reports/2026-4-29-jinkosolar-holding-co-ltd-stock/

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.*
