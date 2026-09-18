# SMTC — Semtech Corporation

**Event confirmed: YES.** Semtech reports Q2 FY2027 (quarter ended ~26 July 2026) **after the close on Tuesday, 25 August 2026**, with a conference call at 1:30 p.m. PT / 4:30 p.m. ET the same day. Confirmed from the company's own conference-call press release dated 11 August 2026 [1] and corroborated by the Nasdaq/StockStory/Barchart earnings calendars [2][3][4]. No date change and no pre-announcement have been filed — the last 8-K was the 13 August cellular-module divestiture [5].

**What this print is about.** This is not an EPS print. Semtech has already told the market what the July quarter looks like: it guided $328.0M ±$5.0M revenue and $0.61 ±$0.02 adjusted EPS at the Q1 call on 26 May, both far above the then-consensus ($300.7M / $0.51), and the Street has simply adopted the guide ($328.4M / $0.62) [6][7][8]. The reported quarter is therefore close to pre-announced. What is genuinely at stake is (a) whether **data-center revenue hit the ~$96–97M implied by management's "35% sequential growth" target**, and (b) whether the **October-quarter guide confirms the promised second-half 1.6T CopperEdge/FiberEdge acceleration**. The complication is the tape: SMTC has round-tripped a 300%+ AI-connectivity melt-up, sitting **-30.8% below its 22 June closing high of $174.73** and **-21.6% in the five sessions to 24 August**, with 20-day realised volatility of 110% annualised. The last two prints were both sold — including a -4.41% reaction to a large beat-and-raise in May — and August's AI-optics peers (Coherent, Astera Labs) beat and still fell. Meanwhile front-expiry options positioning is aggressively, one-sidedly long calls. That is the tension this dossier is about.

---

## 1. Event & anchors

| Item | Value | As-of | Source |
| --- | --- | --- | --- |
| Event date | 2026-08-25 | confirmed | [1][2][3] |
| Session | **amc** (call 1:30pm PT / 4:30pm ET) | confirmed | [1] |
| Fiscal period | Q2 FY2027 (quarter ended ~2026-07-26) | — | [1][6] |
| Date changed / pre-announced? | No. No 8-K since 2026-08-13 (divestiture) | 2026-08-25 | [5][9] |
| Spot (last official close) | **$120.91** (-2.56%) | 2026-08-24 20:00Z | [10][11] |
| Pre-market, event day | **$126.00** (+4.46%), bid 125.00 / ask 126.49 | 2026-08-25 ~10:01Z | [12] |
| Pre-market cross-check | $125.92 (+4.14%) | 2026-08-25 | [10] |
| Market cap | **$11.26B** (93.15M shares o/s) | 2026-08-24 | [10] |
| 52-week range (intraday) | $50.42 – $177.35 | 2026-08-24 | [10] |
| 52-week closing high | $174.73 (2026-06-22) → **-30.8% drawdown** | computed [11] | [11] |
| **Event-implied move (derived)** | **≈13.3% expected absolute move; ≈16.6% 1σ jump** | 2026-08-25 ~10:01Z | [12], my calc |
| Front-expiry ATM straddle | **21.71% of spot** (Sep-18-26, 24 DTE, K=125) | 2026-08-25 | [12] |
| Cboe IV30 | **102.06%** (-0.25 pt d/d) | 2026-08-25 | [12] |
| 20d / 60d realised vol (ann.) | **110.6% / 99.8%** | computed [11] | [11] |
| IV rank / IV percentile | **unavailable** — no free source reachable | — | — |

### Important structural note on the implied move

**SMTC has no weekly options.** Nasdaq's option-chain expiry list and the full Cboe delayed chain both show the first available expiry after the print is the **standard monthly, 18 September 2026 (24 DTE)** [12][13]. There is therefore no clean event straddle to read off, and no published implied-move figure for this print that I could source. I derived one from the Cboe chain:

- Sep-18 (24d) ATM IV 106.1%; Oct-16 (52d) 94.4%; Nov-20 (87d) 90.6%; Dec-18 (115d) 90.0%.
- Decomposing front variance into a diffusive component plus an earnings jump, across three expiry pairs:
  - Sep/Oct → diffusive 83.0%, **jump σ = 16.97%**, E|move| = 13.54%
  - Sep/Nov → diffusive 83.9%, **jump σ = 16.66%**, E|move| = 13.30%
  - Sep/Dec → diffusive 85.2%, **jump σ = 16.23%**, E|move| = 12.95%
- I use **13.3%** as the headline event-implied move (mid of the E|move| estimates). *This is my inference from sourced option prices, not a published number.*

Sanity check: 13.3% implied vs an **11.00% mean absolute** realised move over the last eight quarters. Options are pricing the event ~20% richer than the historical average move — but the base (non-event) vol is so extreme (83–85% diffusive; 110% realised over 20 days) that the earnings premium is a smaller share of total vol than usual for a name like this.

### Realised one-day earnings reactions (earnings-day close → next-day close)

Computed by me from Nasdaq daily closes [11]. Method validated: it reproduces Trefis's published figures **exactly on all 7 overlapping quarters** [14].

| Fiscal quarter | Report date (amc) | Reaction date | Close before | Close after | 1-day move |
| --- | --- | --- | --- | --- | --- |
| Q1 FY27 | 2026-05-26 | 2026-05-27 | $164.46 | $157.20 | **-4.41%** |
| Q4 FY26 | 2026-03-16 | 2026-03-17 | $89.00 | $79.21 | **-11.00%** |
| Q3 FY26 | 2025-11-24 | 2025-11-25 | $70.01 | $71.78 | **+2.53%** |
| Q2 FY26 | 2025-08-25 | 2025-08-26 | $51.00 | $58.72 | **+15.14%** |
| Q1 FY26 | 2025-05-27 | 2025-05-28 | $38.78 | $37.01 | **-4.56%** |
| Q4 FY25 | 2025-03-13 | 2025-03-14 | $32.71 | $39.60 | **+21.06%** |
| Q3 FY25 | 2024-11-25 | 2024-11-26 | $53.44 | $63.11 | **+18.10%** |
| Q2 FY25 | 2024-08-27 | 2024-08-28 | $38.16 | $42.43 | **+11.19%** |

- **Pattern: 5 up / 3 down (62.5% up).** Mean absolute **11.00%**, median absolute **11.09%**, max absolute **21.06%**.
- **Regime shift is the key observation.** The four prints from Aug-2024 to Aug-2025 averaged **+16.4%** (all positive). The three since Nov-2025 average **-4.3%** (two negative). The change coincides with the multiple expanding to 45–50x forward.
- Longer history (Trefis, 19 events back to Jun-2021): 13 of 19 positive (68%), median positive +10.1%, median negative -7.8%, worst -27.1% (Aug-2022) [14].
- **A separate, non-earnings tail event:** on 10 February 2025 SMTC fell **over 30%** intraday after disclosing on 7 February that CopperEdge sales would not ramp in FY26 and would fall below the previously disclosed $50M floor case — ~$1.4B of market cap in one session [15]. That episode is the origin of the still-live securities class action (below) and is the reason CopperEdge credibility is load-bearing for this name.

---

## 2. The bar

| Metric | Company guide (26 May 2026) | Consensus | Source |
| --- | --- | --- | --- |
| Revenue | **$328.0M ±$5.0M** | **$328.4M** (Zacks) / $328.67M (alt) — +27.5% YoY | [6][7][8] |
| Adj. diluted EPS | **$0.61 ±$0.02** | **$0.62** (Zacks) / $0.614 (alt) — +51% YoY | [6][7][8] |
| Adj. gross margin | 54.0% ±50bps | 54.0% | [6][4] |
| Total semi products GM | 62.1% ±50bps | — | [6] |
| Adj. opex, net | $105.2M ±$2.0M (vs $95.1M in Q1 — **+10.6% q/q**) | — | [6] |
| Adj. operating margin | 21.9% ±40bps | 21.9% | [6][4] |
| Adj. EBITDA | $79.2M ±$2.3M (24.2% margin) | — | [6] |
| Non-GAAP diluted share count | 97.7M | — | [6] |
| Adj. normalised tax rate | 17% | — | [6] |

**Segment-level consensus** (Zacks, published 2026-08-2x) [7]:

| Reportable segment | Estimate | YoY |
| --- | --- | --- |
| Signal Integrity (the data-center engine) | **$125.46M** | **+63.4%** |
| Analog Mixed Signal & Wireless | $109.99M | +19.6% |
| IoT Systems & Connectivity | $92.71M | +4.4% |

| End market | Estimate | YoY |
| --- | --- | --- |
| Infrastructure | $118.29M | +61.3% |
| Industrial | $170.55M | +19.2% |
| High-End Consumer | $39.96M | -3.0% |

**Revisions.** EPS consensus **unchanged over the past 60 days**, and up **+0.3% over 30 days** [7][8]. Zacks Rank #2 (Buy) [7]. This is unusually flat drift — no negative pre-print estimate erosion, but also no upward chase. Note the 90-day picture is different: the Q2 numbers were *stepped up wholesale* on 26 May when the guide landed 9% above the revenue consensus and 20% above the EPS consensus [6][16].

**Guidance vs Street history.** Semtech has beaten EPS for 7–8 consecutive quarters [8][17]. Q1 FY27 itself: $291.0M vs $283.44M consensus, $0.51 adj. EPS vs $0.45 [16][6]. The company's demonstrated pattern is to beat modestly on the quarter and to guide well above Street.

**Whisper number: unavailable.** No credibly published whisper for this print was reachable. My inference on the *effective* buy-side bar, given the company's guide is the consensus and the company beats its own guide routinely: revenue near **$333–338M** (i.e. at/above the top of the guided band) and EPS **$0.64–0.67**. *Labelled inference — not sourced.*

**What is needed just to hold the stock flat.** In-line with guidance will not do it, because guidance *is* the consensus and the guide was set nearly three months ago when the stock was $164. My read: the print must (1) show data centre at or above ~$96–97M, (2) guide October revenue with a sequential step-up consistent with "acceleration in H2" — I read that as roughly **$360M+**, and (3) keep adjusted gross margin at or above the 54% guided despite the $10M opex step-up. Missing any one of the three, on a name at 46x forward earnings [4], is likely to be sold.

---

## 3. The one metric that matters

**Data-centre net sales, and specifically whether the number is ≈$96–97M and whether the October guide implies further acceleration.**

Why this and not EPS:
- Q1 FY27 data-centre revenue was a record **$71.6M**, +14% sequentially and +39% YoY [16][18].
- At the Q1 call management explicitly targeted **~35% sequential data-centre growth in Q2, "representing 85% growth over the same period last year"** [18][19].
- The year-ago base is **$52.2M** (Q2 FY26 data-centre net sales, +92% YoY at the time) [20].
- 35% on $71.6M = **$96.7M**. 85% on $52.2M = **$96.6M**. The two paths agree. **~$96.5–97M is the number.** This is the single most precisely specified expectation management has put on the table, and it is why the Signal Integrity segment consensus is $125.46M (+63.4% YoY) versus $102.0M actual in Q1 [7][16].
- CEO Hong Hou at Q1: *"As FiberEdge and CopperEdge 1.6T revenues layer onto our strong growth base, we expect data center growth to accelerate throughout the year"*, citing *"exceptionally strong bookings and backlog to support module ramps in the second half"* and *"accelerating demand throughout fiscal year 2027 and beyond"* [6][21].
- Benchmark's pre-print note frames the same thing from the sell side: watch **"October data center mix, margin quality, and backlog conversion"** rather than the headline [4].

Secondary metric with real weight: **LoRa**. Q1 LoRa-enabled revenue was $44.5M (+12% q/q, +14% YoY) and management targeted **>15% sequential growth** in Q2 → ~$51M+ [21]. LoRa is the second leg of the story and the reason the cellular-module business was divested.

**Why CopperEdge specifically carries asymmetric risk.** This is the product Semtech told the market in Feb-2025 would *not* ramp, after guiding a $50M floor case — a disclosure that cost 30%+ in a session and produced a still-pending securities class action [15]. The market has forgiven it (the stock is up ~145% over 252 sessions [11]), but any qualitative softening of 1.6T CopperEdge language will be read against that history, not on its own terms.

---

## 4. Fundamentals — what changed, what is at stake

**Q1 FY27 actuals (quarter ended 2026-04-26)** [6][16]:

| | Q1'27 | Q4'26 | Q1'26 |
| --- | --- | --- | --- |
| Net sales | **$291.0M** (+6% q/q, +16% YoY) | $274.4M | $251.1M |
| GAAP gross margin | 52.0% | 50.4% | 52.3% |
| Adj. gross margin | **53.0%** | 51.6% | 53.5% |
| GAAP operating margin | 8.9% | (6.7)% | 14.3% |
| Adj. operating margin | **20.4%** | 18.2% | 19.0% |
| GAAP diluted EPS | $0.27 | $(0.32) | $0.22 |
| Adj. diluted EPS | **$0.51** (+34% YoY) | $0.44 | $0.38 |
| Adj. EBITDA | $66.4M (22.8%) | $57.4M (20.9%) | $55.4M (22.1%) |

**Segment mix, Q1 FY27** [16]: Signal Integrity $102.0M · Analog Mixed Signal & Wireless $100.8M · IoT Systems & Connectivity $88.3M. Within that: data centre $71.6M, LoRa-enabled $44.5M, Industrial end-market $153.9M [16][21].

**FY26 full year**: record net sales **$1.05B**, +15%, on data-centre and LoRa strength; Q4 FY26 carried a **$44.6M goodwill/intangible impairment** which is what produced the GAAP operating loss that quarter [22][6].

**Cash flow and balance sheet** [16]:
- Q1 FY27 operating cash flow **$36.2M**; capex $8.2M; **free cash flow $28.0M** (9.6% of sales — thin for a 20% operating-margin business, and a fair question given the guided opex ramp).
- Cash and equivalents **$163.3M**, down from $195.2M at Q4 FY26.
- Long-term debt **$492.0M**.

**Capital structure — the convertible overhang** [23]:
- **$402.5M of 0.00% convertible senior notes due 2030**, priced 7 Oct 2025 ($350M + $52.5M greenshoe). Conversion rate 9.8964 shares/$1,000 → **conversion price $101.05** (42.5% premium at issue). Proceeds were used to exchange out of the 1.625% 2027s and 4.00% 2028s and repay term loans.
- **Capped call cap: $141.82** (100% premium at issue).
- At $120.91 the notes are **in the money** (~4.0M shares of underlying). The capped calls neutralise dilution up to $141.82; above that, dilution is unhedged. In the Q1 10-Q the 2030 notes were still *excluded* from diluted share count because the conversion price exceeded the average market price for that period [24] — that will not remain true. Guided non-GAAP diluted share count is already 97.7M vs 93.15M basic shares outstanding [6][10].
- Sizeable long-dated put open interest is consistent with convertible-arbitrage hedging: **Jan-2027 put OI 11,536 (P/C OI 1.16)** and **Jan-2028 put OI 19,848 (P/C OI 6.64)** [12]. *That is my interpretation of the OI pattern, not a sourced attribution.*

**What changed since the last print:**
1. **Cellular module divestiture (13 Aug 2026).** Definitive agreement to sell the cellular module business to Compal Electronics (TWSE: 2324) for **$62M cash**, expected to close in **Q4 FY27**. UBS advised. CEO Hou: *"This divestiture sharpens our focus on the product portfolio where we have the strongest conviction in growth and industry leadership: data center and LoRa connectivity."* [5] Modules are a low-margin hardware business; removing them is structurally gross-margin accretive but revenue-dilutive from Q4 FY27. **The call will need to quantify the revenue and margin restatement — this is a live source of guidance confusion.**
2. **New $360M revolving credit facility (6 Jul 2026)**, Morgan Stanley Senior Funding as agent, **undrawn at closing**, plus an uncommitted incremental term loan facility [25]. Liquidity flexibility ahead of a capacity-constrained ramp — read as prudent, not distressed.
3. **Executive Severance Plan amended and restated (2 Jun 2026)** to add severance for terminations *not* in connection with a change of control [26]. Neutral-to-mildly-notable governance change.
4. **No buyback disclosed.** I found no share-repurchase authorisation or activity in FY27 to date. Capital return is not part of this story; capital structure is going the other way (converts + revolver).

**Customer concentration: unavailable.** I could not source a current top-customer concentration figure. For a company whose data-centre ramp depends on a small number of hyperscaler/optical-module programmes, this is a material gap.

---

## 5. Positioning & options

All options data below computed by me from the Cboe delayed chain snapshot, file timestamp **2026-08-25 10:01:10Z** [12]. Underlying reference $126.00 (pre-market).

**IV term structure — backwardated, but on an extreme base:**

| Expiry | DTE | ATM IV | ATM straddle (% of spot) |
| --- | --- | --- | --- |
| 2026-09-18 | 24 | **106.1%** | 21.71% |
| 2026-10-16 | 52 | 94.4% | 27.94% |
| 2026-11-20 | 87 | 90.6% | 34.40% |
| 2026-12-18 | 115 | 90.0% | 39.05% |
| 2027-01-15 | 143 | 87.4% | 42.14% |
| 2027-03-19 | 206 | 87.2% | 50.00% |
| 2028-01-21 | 514 | 85.7% | 74.68% |

Front-to-back spread is only ~20 vol points, and the **long end never comes below ~85%**. The market is not treating this as a stable business with an event bump; it is treating it as a permanently high-variance asset. Cboe IV30 of 102.06% is *below* trailing 20-day realised vol of 110.6% [11][12] — by that measure front options are not obviously expensive.

**Skew — positive, i.e. calls bid over puts. This is the standout:**

| Expiry | ATM IV | 25Δ call IV | 25Δ put IV | 25Δ risk reversal (C−P) |
| --- | --- | --- | --- | --- |
| 2026-09-18 | 106.1% | 107.9% (K=155) | 105.0% (K=105) | **+2.9 vols** |
| 2026-10-16 | 94.4% | 94.7% (K=165) | 94.2% (K=100) | +0.5 vols |
| 2026-11-20 | 90.6% | 93.1% (K=185) | 89.8% (K=100) | +3.3 vols |

Equities almost always show negative skew (puts over calls). SMTC shows the opposite in the event expiry. That is a speculative-upside signature, not a hedging one.

**Put/call — heavily call-tilted in the event expiry:**

| Expiry | Call OI | Put OI | P/C OI | Call vol | Put vol | P/C vol |
| --- | --- | --- | --- | --- | --- | --- |
| **2026-09-18** | **22,875** | **6,201** | **0.27** | 4,105 | 983 | **0.24** |
| 2026-10-16 | 7,124 | 1,785 | 0.25 | 941 | 129 | 0.14 |
| 2026-11-20 | 4,538 | 1,154 | 0.25 | 136 | 50 | 0.37 |
| 2026-12-18 | 5,550 | 1,991 | 0.36 | 370 | 52 | 0.14 |
| All expiries | 55,286 | 43,938 | 0.79 | 5,740 | 1,261 | 0.22 |

The all-expiry P/C of 0.79 is distorted by the long-dated convert-hedge puts; the **tradeable near-term book is roughly 4:1 calls**. Largest Sep-18 call open interest sits at **$140 (3,885), $145 (2,963), $180 (2,112), $130 (1,861), $155 (1,665)** — i.e. concentrated **15–50% above spot** [12].

**My read on positioning (inference).** The near-dated options book is crowded long-upside into a print, on a stock that has just fallen 21.6% in five sessions. Long-call crowding into an event is a negative-skew configuration: it means much of the marginal upside demand has already been expressed and is decaying, and a "good but not spectacular" print leaves a wall of OTM calls to be monetised into any pop. Conversely there is very little downside hedging in place, so a genuine disappointment has less pre-existing protection to cushion it.

**Short interest** (snippet_only) [27]:
- **6.5M shares short**, up **17.1%** on the prior period, **7.0% of float**.
- **Days to cover 2.2**, up 118% period-on-period.
- 7% of float with only 2.2 days to cover is a modest, easily-covered short base. There is no meaningful squeeze fuel here, though the sharp *increase* suggests some fresh bearish positioning arrived during the August drawdown.
- **Settlement date for this reading: unavailable.**

**Borrow fee / cost to borrow: unavailable.** No free source reachable.

**Institutional ownership** (snippet_only) [28]: ~72.0% institutional, ~0.47% insider. A second source reported total institution-held shares +0.35% over three months. Sources conflict on methodology; treat as directional only.

**Run-up / drawdown into the print** (computed from [11]):

| Window to 2026-08-24 close | Change |
| --- | --- |
| 1 session | -2.56% |
| 3 sessions | -3.55% |
| **5 sessions** | **-21.60%** (from $154.22 on 8/17) |
| 10 sessions | -7.89% |
| 21 sessions | -3.98% |
| 63 sessions | -22.88% |
| 126 sessions | +39.27% |
| 252 sessions | **+144.81%** |
| From 52w closing high ($174.73, 6/22) | **-30.80%** |

**Recent session detail** [11]: 8/12 +6.72 · 8/13 -4.59 · 8/14 +5.07 · **8/17 +9.88** · **8/18 -12.31** · **8/19 -7.30** · 8/20 -0.38 · 8/21 -0.63 · 8/24 -2.56. The 17 August spike was the Compal divestiture plus a Needham reiteration and a broad semi rally (peers MTSI +3.3%, SITM +4.7%, LSCC +4.0%) [29][30]. The 18–19 August collapse has **no company-specific catalyst I could identify**; it coincides with a broad chip selloff on elevated bond yields in which the Nasdaq-100 fell 1.7% and semis fell ~5%, with Micron -7.0%, ARM -6.7%, Intel -6.6% [31]. SMTC fell roughly three times the sector — high-beta unwind, not news.

**How crowded does the trade look?** Very crowded on the long side by every measure I can observe: 13 of 16 analysts at Strong Buy [4], mean price target **$198–$201 versus a $121 spot** (a 64–67% gap) [32][4], Reddit sentiment 88/100 bullish [33], near-dated options 4:1 calls with positive skew [12], and 72% institutional ownership [28]. The only non-consensus positioning is a modest 7%-of-float short base [27].

---

## 6. Sentiment & alt-data

**Analyst ratings and targets:**

| Source | Rating | Analysts | Mean PT | High | Low | As-of |
| --- | --- | --- | --- | --- | --- | --- |
| StockAnalysis [32] | Strong Buy (12 SB / 1 B / 2 H / 0 S) | 15 | **$201.38** (+66.6%) | $230 | $155 | 2026-08-24 |
| Barchart [4] | Strong Buy (13 of 16) | 16 | $198.36 (+68.3%) | $230 | — | 2026-08-24 |
| TipRanks (snippet) [34] | — | 22 | $209.30 | — | — | Aug 2026 |
| S&P Global (snippet) [35] | Strong Buy | 14 | $205.25 | — | — | Aug 2026 |
| Public.com (snippet) [36] | Buy (57% SB / 36% B / 7% H) | 14 | — | — | — | 2026-08-10 |

Forward P/E **45.7–46.9x** on non-GAAP FY27 EPS of ~$2.65; P/S **8.48x** [32][4]. FY28 consensus EPS $3.89 (+47%) [32].

**Price-target drift.** All the visible PT action ran *up* on the Q1 beat and then stopped:
- Benchmark **$230 from $120** (Buy) [37]
- UBS (Timothy Arcuri) **$225 from $165** (Buy) [38]
- Craig-Hallum (Anthony Stoss) **$205 from $105** (Buy) [37]
- Fair-value estimate raised **$110.47 → $230.00** on stronger long-term data-centre assumptions [35]

The only downgrade I could source: **Northland (Gus Richard) cut to Market Perform from Outperform on ~26 May 2026** on valuation, noting SMTC traded at **53x FY28 consensus** — part of a sector-wide action that also downgraded Astera Labs and Intel with the framing that semis are *"priced for perfection and face elevated risks over the next two quarters"* [39][40]. On 17 August a Needham analyst reiterated a positive rating citing data-centre demand trends [29].

**Critical caveat:** targets clustering at $198–$209 against a $121 spot means **the sell side has not marked to market a 31% drawdown.** I read the target set as stale, not as forward-looking signal. Post-print PT cuts are a live risk regardless of what the numbers say.

**Retail and social:**
- Reddit sentiment **88/100 bullish** but with **0 mentions/day, down 100% versus its recent average** — bullish tone, collapsed engagement [33].
- StockTwits retail sentiment was **"extremely bullish" 84/100 with "extremely high" message volume** as of March 2026 [33].
- **7/14/30-day social trend: unavailable.** I could not source a dated sentiment time series. The 88/100-with-zero-mentions datapoint is directionally consistent with a de-crowding retail base but is a single snapshot.
- Press tone in June was already skeptical: TipRanks ran *"Semtech Stock Sags As AI Euphoria Meets Reality"* (15 Jun 2026), citing profit-taking after a 300% year, insider selling by the CEO/CFO/COO, and valuation reassessment [41].

**Alt-data: largely unavailable.** No Google Trends series, app ranks, or web-traffic proxies were reachable for this name (Semtech is a component supplier with no consumer surface, so these proxies have limited signal value anyway). Job postings: **25 open roles**, actively hiring, from a search snippet — too thin and undated to be usable [42]. **This is a real coverage gap, though a lower-value one for a B2B semiconductor supplier.**

**A caution on media reports of the last print.** Several outlets described SMTC as gaining "more than 15%" after the Q1 FY27 report. The close-to-close tape does not support this: SMTC closed **$164.46 on 26 May and $157.20 on 27 May, -4.41%** [11]. The stock rose 4.90% on 26 May *into* the print and gapped up after hours (~+4% [43]), then closed lower the next day. **Anyone anchoring on "SMTC popped 15% last quarter" has the sign wrong.**

---

## 7. Forensics

**Insider activity — Form 4s filed 2026-05-25 → 2026-08-21, aggregated by me from EDGAR primary filings** [9][44]. 32 Form 4s. Open-market sales (code S, disposal):

| Insider | Title | Shares | Value | Dates | 10b5-1? |
| --- | --- | --- | --- | --- | --- |
| Asaf Silberstein | EVP & COO | 18,500 | $2,599,439 | 6/03–8/17 | Mixed (2,000 on 6/03 discretionary) |
| **Hong Q. Hou** | **President & CEO** | 15,605 | $2,335,608 | 6/05–8/07 | **Mixed (9,605 on 6/29 discretionary)** |
| **John Michael Wilson** | **Chief Quality Officer & CTO** | 5,500 | $935,000 | 6/22 | **No — discretionary** |
| Li Ye Jane | (officer) | 5,285 | $881,758 | 5/28 | **No — discretionary** |
| Gregory Michael Fischer | (officer) | 2,500 | $399,045 | 5/28–6/30 | Mixed (1,000 on 5/28 discretionary) |
| Jason Elliot Green | EVP & CCO | 2,264 | $294,086 | 7/07 | Yes |
| Mark Lin | EVP & CFO | 1,653 | $251,867 | 6/10–7/01 | Yes |
| Paul V. Walsh Jr. | Director | 1,500 | $216,770 | 6/24–8/19 | Yes |
| **TOTAL** | | **52,807** | **$7,913,572** | | |

**Insider purchases in the window: zero.**

**The discretionary subset is the signal.** Filings where the `aff10b5One` flag is **0** (i.e. *not* under a pre-arranged plan), verified individually against the XML [44]:

| Date | Insider | Shares | Price |
| --- | --- | --- | --- |
| 2026-06-29 | **Hong Q. Hou (CEO)** | 9,605 | $152.43 / $152.99 |
| 2026-06-22 | **J. Michael Wilson (CQO/CTO)** | 5,500 | **$170.00** |
| 2026-06-03 | Asaf Silberstein (COO) | 2,000 | $164.00 |
| 2026-05-28 | Li Ye Jane | 5,285 | $166.84 |
| 2026-05-28 | Gregory M. Fischer | 1,000 | $164.69 |
| **Total discretionary** | | **23,390** | **≈$3.86M** |

That is **~$3.9M of discretionary, non-plan selling by five insiders including the CEO and the CTO, clustered in a $152–$170 band between 28 May and 29 June** — and Wilson's 5,500 shares at exactly $170.00 on 22 June was the session of the 52-week *closing high* ($174.73). Separately, COO Silberstein sold 5,000 at exactly $150 on 17 August — the local top — but that one **was** under a 10b5-1 plan (adopted 8 April 2026) [45].

**How to weight this.** Most of the dollar volume was plan-based and mechanical, so the popular "insiders are dumping" framing overstates it. But the *discretionary* cluster is real, is concentrated in the top 15% of the stock's 52-week range, includes the CEO, and is unaccompanied by a single purchase. My read: consistent with executives who think the shares got ahead of the business — not evidence of knowledge about this specific quarter, since all of it predates the July quarter-end by weeks. **Note also that plan-adoption dates are recent for two sellers** (Silberstein 8 Apr 2026; Fischer 30 Mar 2026), i.e. plans adopted *after* the stock had already multiplied.

**Litigation.** *Kleovoulos v. Semtech Corporation et al.*, No. 2:25-cv-01474 (C.D. Cal.) — securities fraud class action on behalf of purchasers **27 Aug 2024 – 7 Feb 2025**, alleging Semtech misrepresented the suitability and ramp schedule of CopperEdge for its server-rack customer. Trigger: the 7 Feb 2025 disclosure that CopperEdge would not ramp in FY26 and would come in below the previously disclosed $50M floor case; the stock fell 30%+ on 10 Feb 2025. Lead-plaintiff deadline 22 Apr 2025 [15][46]. **Current procedural status: unavailable.** Note that Semtech's non-GAAP reconciliation explicitly excludes *"litigation costs or dispute settlement charges or recoveries"* [6].

**Auditor / restatement:** no restatement, auditor change, or material weakness disclosure found in the filing record [9]. Q4 FY26 carried a **$44.6M goodwill and intangible impairment** — a real write-down, disclosed, and the cause of the GAAP operating loss that quarter [6].

**Executive departures:** no departures found in FY27 to date. The relevant history is older: CEO Paul Pickle departed abruptly in 2024 over board differences and Dr. Hong Hou was appointed effective 6 June 2024 [47]. The 2 Jun 2026 8-K under Item 5.02 was a **compensation matter only** — amendment and restatement of the Executive Severance Plan to extend severance to non-change-of-control terminations — not a departure [26].

**8-K cadence.** Sparse and unremarkable: 2026-05-26 (Q1 earnings), 2026-06-08 (severance plan), 2026-07-06 (revolver), 2026-08-13 (divestiture) [9]. **No pre-announcement, no negative pre-signalling, and no filing in the 12 days before this print.** Given that Semtech's own history includes a mid-quarter negative pre-announcement in Feb 2025 [15], the *absence* of one this time is mildly reassuring — the company has demonstrated it will pre-announce when things break.

**Form 144 cadence** is heavy (roughly weekly through June–August) [9], consistent with the ongoing plan sales above rather than anything new.

**Filing-language / tone shift:** none detected. The Q1 FY27 release language is unambiguously confident ("record", "exceptional start", "strong conviction in our growth trajectory", "exceptionally strong bookings and backlog") [6]. I could not obtain the Q2 10-Q for a risk-factor diff — it will not exist until the print.

---

## 8. Macro & peer read-through

**Regime.** August 2026 has been a two-way tape for AI semis. Global semiconductor sales hit a record $120.6B in May 2026, the 15th consecutive monthly record, and the PHLX Semiconductor Index reached new highs in August [42][48]. But there have been repeated violent unwinds: a July selloff in which chip stocks shed more than $1 trillion on AI-spending and cost fears [49], an early-July Intel-led drawdown [50], and the 18–19 August episode where rising yields and inflation anxiety knocked semis ~5% and the Nasdaq-100 -1.7% in a session [31]. High-multiple, high-beta AI derivatives like SMTC have been the whipping boys of each unwind — SMTC fell 12.31% on 18 August against a ~5% sector move [11][31].

**Rate sensitivity is the dominant macro factor here.** SMTC is a long-duration equity: negative GAAP trailing earnings [10], 46x forward non-GAAP, valuation entirely dependent on out-year data-centre growth. The 18–19 August selloff was explicitly yield-driven [31]. FX and commodity sensitivity are second-order; wafer and materials cost inflation is a live margin input, with ~20 semiconductor peers having pushed through price increases from 1 July 2026 [51].

**The single biggest scheduling fact: NVIDIA reports Q2 FY27 after the close on Wednesday 26 August 2026** — the very session in which SMTC's reaction plays out [52][53]. Consensus is ~$91.85B revenue / $2.08 EPS across 40 analysts, with hyperscaler 2026 capex commitments estimated at $775–800B [52]. **SMTC's post-print day is therefore also the day the entire AI complex de-risks into the sector's defining print.** My inference: this compresses the amount of directional conviction anyone will express in SMTC on 26 August and raises the odds that even a well-received print is only partially monetised before the close — and it materially raises reversal risk on 27 August.

**Peers who have already reported — the read-through is "beat and fade":**

| Peer | Date | Result | Reaction |
| --- | --- | --- | --- |
| **Coherent (COHR)** | 2026-08-12 | Q4 rev $2.045B (+33.7%); Datacom & Comms $1.615B (79% of sales, +59% pro forma); non-GAAP EPS $1.74 (+7.6% beat); Q1 guide $2.2–2.4B vs $2.14B Street | **Shares slipped ~4% after hours** despite the beat-and-raise; stock had been +93% YTD [54][55] |
| **Lumentum (LITE)** | 2026-08-11 | Q4 adj EPS $3.23 vs $2.95; rev $1.01B vs $984.6M; sales +109% YoY; 8th straight growth quarter; non-GAAP GM >50% first time | **+1.51% after hours** — beat rewarded, but only modestly [54][55] |
| **Astera Labs (ALAB)** | 2026-08-04 | Q2 guided $355–365M (+85–90% YoY); Scorpio X-Series in volume production, moved up to largest product family in Q3 | **-12% since reporting**, on higher opex [56] |
| Sector, pre-earnings | mid-Aug | — | *"Coherent Falls 12%, Lumentum Drops 7% as AI Optics Stocks Cool Ahead of Earnings"* [54] |

**This is the most important comparable evidence in the dossier.** Three AI-optics/connectivity suppliers reported strong numbers in August 2026. Two of the three traded down afterwards, and the explanation given for Coherent was explicitly that a large YTD run "left little room for anything short of a clean beat." SMTC's setup rhymes: +144.8% over 252 sessions [11], 46x forward, and a guided opex step-up of exactly the kind that punished Astera Labs.

**The mitigant that distinguishes SMTC from Coherent.** Coherent went into its print near its highs. SMTC goes in **-30.8% from its closing high and -21.6% over five sessions** [11]. The de-rating that punished the peers has, for SMTC, largely already happened before the event rather than after it.

**Supply-chain / customer read-through:** Semtech demonstrated 1.6T ACCs running live traffic against NVIDIA's 224G SerDes and is a co-founding member of the ACC MSA alongside AMD, Dell and NVIDIA [57]. The company sits directly downstream of hyperscaler rack architecture decisions, which makes NVDA's 26 August commentary a genuine fundamental read-through, not just a beta event. Management has also scheduled a **Data Center teach-in for 15 October 2026 in San Jose** with the CEO, CFO and the SVP/GM of Signal Integrity presenting long-term financial objectives [58] — a forum that gives management a reason to keep some of its best disclosure in reserve on 25 August, which historically dampens print-day upside.

---

## 9. Bull case / bear case / base case

**Bull case.** The de-risking already happened. SMTC enters this print 30.8% below its June closing high and 21.6% below where it traded five sessions ago [11], with the entire decline attributable to a sector-wide, yield-driven unwind rather than anything company-specific [31] — no negative pre-announcement, no 8-K, no estimate cuts (consensus EPS unchanged over 60 days, +0.3% over 30) [7][8][9]. Underneath, the business is inflecting hard: data centre going from $52.2M a year ago to a targeted ~$96.7M this quarter [16][20][18], LoRa guided >15% sequentially [21], "exceptionally strong bookings and backlog" for H2 module ramps [6][21], 1.6T design wins with major optical module makers [21], and a portfolio cleanup that just removed the lowest-margin business for $62M cash [5]. The company has beaten EPS 7–8 quarters running and has a demonstrated habit of guiding materially above Street — last quarter's guide was 9% above consensus revenue and 20% above consensus EPS [6][16][8]. If October guidance repeats that pattern, a stock trading at $121 against a $198–$201 mean sell-side target [32][4] with only 7% of float short [27] has a long way to travel on very little supply.

**Bear case.** The bar has been pre-set at a level that leaves no room. Guidance *is* consensus ($328M / $0.61–0.62) [6][7], so an in-line quarter is worth nothing, and management publicly committed to a specific, checkable ~35% sequential data-centre number [18][19] that becomes a stick if missed by a dollar. The August peer tape is unambiguous: Coherent beat and raised and fell ~4%; Astera Labs is -12% since its print; the stated reason was that big YTD runs leave "little room for anything short of a clean beat" [54][55][56]. The guided opex step-up from $95.1M to $105.2M (+10.6% q/q) [6] is exactly the line item that broke Astera Labs. Positioning is one-sidedly long: front-expiry P/C open interest of 0.27, 4:1 call volume, and a **positive** 25-delta risk reversal (+2.9 vols) with call OI stacked at $140–$180 [12] — a decaying wall of upside bets and almost no downside hedging. Insiders sold $7.9M since late May with zero purchases, including ~$3.9M of *discretionary* non-plan sales by the CEO and CTO at $152–$170 [44]. Sell-side targets clustered at $198–$209 [32][34] have not been marked to a 31% drawdown, making post-print PT cuts a distinct second-day risk. And the reaction day is 26 August — the day the whole AI complex de-risks into NVIDIA's print after the close [52][53]. Finally, this is the company that pre-announced a CopperEdge ramp failure in February 2025 and lost 30% in a session, and is still defending a class action over it [15]; the market's tolerance for soft 1.6T language is asymmetrically low.

**Base case (mine).** The July quarter prints fine — at or modestly above the $328M/$0.61 guide, with data centre at or near $96–97M — because Semtech's guide was set with the quarter already two-thirds visible and the company beats its own guide as a matter of routine. The October guide is the coin flip, and the honest answer is that I **could not source a Q3 FY27 consensus revenue figure**, so I cannot tell you where the guidance bar actually sits. Absent that, I weight the two structural facts I *can* observe: the peer base rate in August 2026 has been beat-and-fade, and near-dated positioning is crowded long. Against that, the -21.6% five-session drawdown genuinely de-risks this setup in a way that Coherent's did not. I land marginally negative with low conviction, and I expect a wide distribution — the implied 13.3% expected move [12] against an 11.0% historical mean absolute move [11] is, if anything, roughly fair. The distribution is fat on both tails: 21% up and 11% down are both in the recent sample [11].

---

## 10. What would flip the consensus view

**The most credible reversal, stated concretely: an October revenue guide of $370M or better with data-centre revenue guided above ~$130M and adjusted gross margin held at or above 55%.**

That combination would do three things at once. It would prove the 1.6T CopperEdge/FiberEdge ramp is real and on schedule rather than a promise — settling the exact question the February-2025 disclosure and the pending class action put in doubt [15]. It would demonstrate that the $105.2M opex step-up bought revenue rather than just cost, which is the specific failure mode that took Astera Labs down 12% [56] and that Benchmark flagged as the thing to watch ("October data center mix, margin quality, and backlog conversion") [4]. And mechanically, it would repeat the Q1 pattern of guiding ~9–20% above Street [6][16], which is the setup that historically produces SMTC's +15% to +21% reaction days [11]. With only 7% of float short [27], 13 of 16 analysts already at Strong Buy [4], and mean targets at $198–$201 against a $121 spot [32], the flip would come not from short covering but from the sell side being handed a reason not to cut those targets — and from the ~$140/$145 September call strikes with ~6,800 contracts of open interest [12] coming into play.

**The mirror-image flip (bear direction):** any language that defers the 1.6T CopperEdge ramp — "second half weighted", "customer qualification timing", a revised floor case — combined with an October guide below ~$345M. The Feb-2025 precedent says the market will not wait for the next data point to reprice that.

**A structural wildcard for the guide itself:** the Compal cellular-module divestiture closes in Q4 FY27 [5]. If management guides October on a continuing-operations basis without clearly bridging the removed revenue, a mechanically lower headline number could be misread on the tape in the first minutes. That is a source of noise, not signal, but it is a real path to a bad initial print reaction that reverses.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **Q3 FY27 (October quarter) consensus revenue/EPS** | The single most important missing number. The whole print turns on the guide, and I cannot say what the guide has to clear. This is the largest hole in the dossier and the main reason my conviction is Low. |
| **Published event-implied move** | No weekly options exist on SMTC [13]; first expiry after the print is 24 DTE. My 13.3% figure is *derived* from a sourced Cboe chain [12], not published. Treat it as an estimate with ±2pt uncertainty. |
| **IV rank / IV percentile** | Cannot say whether IV30 of 102% is high or low *for this name*. Given 20d realised of 110.6%, it may not be elevated at all — which would change how one reads the "options are pricing a big move" framing. |
| **Borrow fee / cost to borrow** | No free source reachable. 7% of float short with 2.2 days to cover suggests easy borrow, but unconfirmed. |
| **Short-interest settlement date** | The 6.5M-share figure [27] is snippet-only and undated; the +17.1% change could be from any period during the August drawdown. |
| **Whisper number** | None credibly published. My $333–338M / $0.64–0.67 estimate is inference only. |
| **Customer concentration** | Not sourced. For a company whose thesis is a hyperscaler-driven data-centre ramp, the identity and concentration of the customer base is material to how a guide should be read. |
| **7/14/30-day social sentiment trend** | Only a single undated snapshot (Reddit 88/100 with zero daily mentions [33]). No trend, so I cannot tell whether retail is capitulating or accumulating into the print. |
| **Alt-data (Google Trends, web traffic, job postings, review data)** | Effectively absent. Lower value for a B2B component supplier, but it means there is no independent check on the demand narrative. |
| **Class-action procedural status** | Unknown whether *Kleovoulos* survived a motion to dismiss. A ruling would be a discrete headline risk of unknown timing. |
| **Segment gross margins / data-centre gross margin** | Only total and "semiconductor products" GM (62.1% guided) are disclosed [6]. Cannot assess whether the data-centre mix shift is margin-accretive or dilutive at the segment level. |
| **Buyback authorisation** | Found none in FY27; I am reporting absence of evidence, not evidence of absence. |
| **Unreachable domains (WebFetch blocked/403/401)** | tipranks.com (403), marketchameleon.com (access denied), barchart.com options page (template only), optioncharts.io (paywalled), thestreet.com (403), query1/query2.finance.yahoo.com (401, crumb required), ca.finance.yahoo.com options chain (503), financialcontent.com (redirect loop), stooq.com (JS challenge). **Reachable and used directly:** sec.gov/data.sec.gov, cdn.cboe.com, api.nasdaq.com, stockanalysis.com, businesswire.com, trefis.com, stocktitan.net. |

---

## 12. Sources

1. StockTitan — Semtech Q2 FY2027 conference call announcement, BUSINESS WIRE dateline 2026-08-11: "after the close of the market on Tuesday, August 25, 2026", call "1:30 p.m. PT (4:30 p.m. ET)". *Event date, session, call time (primary IR release).* https://www.stocktitan.net/news/SMTC/semtech-announces-second-quarter-of-fiscal-year-2027-conference-zagjhuxtt4pg.html
2. MarketBeat — Semtech expected to announce quarterly earnings Tuesday (2026-08-18). *Event date corroboration.* https://www.marketbeat.com/instant-alerts/semtech-smtc-expected-to-announce-quarterly-earnings-on-tuesday-2026-08-18/
3. Daily Political — Semtech expected to release earnings Tuesday (2026-08-22). *Event date corroboration; consensus $0.6140 EPS / $328.67M revenue.* https://www.dailypolitical.com/2026/08/22/semtech-smtc-expected-to-release-earnings-on-tuesday.html
4. Barchart — "Dear Semtech Stock Fans, Mark Your Calendars for August 25" (2026-08-24). *Event date/session; consensus GM 54% and op margin 21.9%; forward P/E 46.85x; P/S 8.48x; RSI 43.22; Strong Buy 13 of 16; mean PT $198.36, high $230; -33.5% from June peak, -23.1% over 5 days; Benchmark's "October data center mix, margin quality, backlog conversion".* https://www.barchart.com/story/news/4006858/dear-semtech-stock-fans-mark-your-calendars-for-august-25
5. SEC EDGAR — Semtech 8-K exhibit 99.1, 2026-08-13. *Cellular module divestiture to Compal Electronics for $62M cash; closing expected Q4 FY27; CEO quote; UBS advised.* https://www.sec.gov/Archives/edgar/data/0000088941/000119312526347716/d123711dex991.htm
6. SEC EDGAR — Semtech 8-K exhibit 99.1, Q1 FY2027 results, dated 2026-05-26. *All Q1 FY27 GAAP/non-GAAP financials; full Q2 FY27 guidance table (revenue $328.0M ±$5.0M, adj GM 54.0%, semi products GM 62.1%, adj opex $105.2M, adj op margin 21.9%, adj EPS $0.61 ±$0.02, adj EBITDA $79.2M, diluted share count 97.7M, tax 17%); CEO/CFO quotes; non-GAAP exclusion list incl. litigation costs; Q4'26 $44.6M impairment.* https://www.sec.gov/Archives/edgar/data/88941/000008894126000009/smtc-04262026x8k991.htm
7. Yahoo Finance / Zacks — "Countdown to Semtech (SMTC) Q2 Earnings: A Look at Estimates Beyond Revenue and EPS". *Consensus EPS $0.62 (+51.2% YoY), revenue $328.37M (+27.5%); 30-day EPS revision +0.3%; 30-day stock -8.5% vs S&P +3.5%; Zacks Rank #2; segment and end-market estimates.* https://ca.finance.yahoo.com/news/countdown-semtech-smtc-q2-earnings-131502717.html
8. Yahoo Finance / Zacks — "SMTC Set to Report Q2 Earnings: What's in the Cards for the Stock?". *Consensus $328.4M revenue / $0.62 EPS, unchanged over past 60 days; guidance restated; growth drivers.* https://finance.yahoo.com/markets/stocks/articles/smtc-set-report-q2-earnings-134200063.html
9. SEC EDGAR — Semtech Corp (CIK 0000088941) submissions feed. *Complete filing cadence: 8-Ks 2026-05-26, 2026-06-08, 2026-07-06, 2026-08-13; 32 Form 4s since 2026-05-25; Form 144 cadence; 10-Q 2026-05-27; no restatement/auditor filings; FYE 01-31.* https://data.sec.gov/submissions/CIK0000088941.json
10. StockAnalysis — SMTC overview. *Close $120.91 (-2.56%) on 2026-08-24 16:00 EDT; market cap $11.26B; 93.15M shares outstanding; 52-week range $50.42–$177.35; negative GAAP earnings (no P/E); pre-market 2026-08-25 $125.92 (+4.14%); daily close table used for cross-check.* https://stockanalysis.com/stocks/smtc/
11. Nasdaq historical price API — SMTC daily OHLCV, 2024-06-03 to 2026-08-24 (558 sessions). *All computed figures: eight quarters of one-day post-earnings reactions; mean/median/max absolute move; run-up and drawdown windows; 52-week closing high $174.73 (2026-06-22); 20d realised vol 110.6%, 60d 99.8%; daily session detail 8/12–8/24.* https://api.nasdaq.com/api/quote/SMTC/historical?assetclass=stocks&fromdate=2024-06-01&todate=2026-08-25&limit=600
12. Cboe delayed options quotes — SMTC full chain, file timestamp 2026-08-25 10:01:10Z. *Underlying $126.00 (+4.46%), bid 125.00/ask 126.49, prev close $120.91, IV30 102.06%; complete expiry list (first post-event expiry = 2026-09-18); all ATM straddles, IV term structure, 25-delta skew/risk reversals, put/call OI and volume by expiry, strike-level open interest; inputs to my earnings-jump decomposition.* https://cdn.cboe.com/api/global/delayed_quotes/options/SMTC.json
13. Nasdaq option-chain API — SMTC. *Confirms zero records for expiries 2026-08-25 to 2026-09-05 and that the earliest listed expiration is September 2026 (2026-09-18); i.e. no weekly options.* https://api.nasdaq.com/api/quote/SMTC/option-chain?assetclass=stocks&fromdate=2026-08-25&todate=2026-09-05
14. Trefis — "How Will Semtech Stock React To Its Upcoming Earnings?" (2026-05-22). *19-event history of one-day post-earnings returns back to Jun-2021; 13 of 19 positive (68%, rising to 82% over last 3 years); median positive +10.1%, median negative -7.8%, max +21.1%, min -27.1%. Used to validate my computed reaction series (7/7 overlapping quarters match).* https://www.trefis.com/articles/600175/how-will-semtech-stock-react-to-its-upcoming-earnings/2026-05-22
15. Hagens Berman / Kessler Topaz — Semtech securities class action. *Kleovoulos v. Semtech Corporation et al., No. 2:25-cv-01474 (C.D. Cal.); class period 2024-08-27 to 2025-02-07; CopperEdge suitability and ramp allegations; 2025-02-07 disclosure that CopperEdge would fall below the $50M floor case; 2025-02-10 stock -30%+, ~$1.4B market cap; lead plaintiff deadline 2025-04-22.* https://www.prnewswire.com/news-releases/semtech-corporation-smtc-faces-class-action-suit-over-alleged-copperedge-misrepresentations--hagens-berman-302384876.html
16. BusinessWire — "Semtech Announces First Quarter of Fiscal Year 2027 Results". *Q1 FY27 detail: net sales $291.0M; segments Signal Integrity $102.0M / AMS&W $100.8M / IoT S&C $88.3M; GAAP and adj. margins; operating cash flow $36.2M, capex $8.2M, FCF $28.0M; cash $163.3M (from $195.2M); long-term debt $492.0M; Q2 guidance. Beat vs consensus $283.44M / $0.45.* https://www.businesswire.com/news/home/20260525414093/en/Semtech-Announces-First-Quarter-of-Fiscal-Year-2027-Results
17. Benzinga — Semtech earnings estimates. *EPS beats in 7 consecutive quarters.* https://www.benzinga.com/quote/SMTC/earnings
18. Seeking Alpha — "Semtech forecasts $328M Q2 revenue as it targets 35% sequential data center growth". *The ~35% sequential data-centre growth target and all-time-high LoRa sales.* https://seekingalpha.com/news/4597199-semtech-forecasts-328m-q2-revenue-as-it-targets-35-percent-sequential-data-center-growth
19. Investing.com — "Earnings call transcript: Semtech beats Q1 2027 forecasts, stock rises". *Q1 FY27 call: ninth consecutive quarter of net sales growth; data centre record $71.6M, +14% q/q, +39% YoY; Q2 data-centre target +35% sequential = +85% YoY; capacity-constrained environment commentary.* https://www.investing.com/news/transcripts/earnings-call-transcript-semtech-beats-q1-2027-forecasts-stock-rises-93CH-4710949
20. Semtech IR — Q2 FY2026 results (2025-08-25). *Q2 FY26 net sales $257.6M (+20% YoY); data-centre net sales record $52.2M, +1% q/q, +92% YoY — the year-ago base for this quarter's data-centre comparison.* https://www.semtech.com/company/press/semtech-announces-second-quarter-of-fiscal-year-2026-results
21. Briefing.com / Motley Fool — Semtech Q1 FY27 call coverage and transcript. *Industrial revenue $153.9M (+8% YoY); LoRa-enabled revenue $44.5M (+12% q/q, +14% YoY) with >15% sequential growth targeted; 1.6T optical design wins with major module makers; "exceptionally strong bookings and backlog" for H2 ramps; CEO Hou "accelerating demand throughout fiscal year 2027 and beyond".* https://www.briefing.com/story-stocks/archive/2026/5/27/semtech-delivers-record-q1-as-data-center-demand-powers-upside-q2-guidance-(smtc) · https://www.fool.com/earnings/call-transcripts/2026/05/26/semtech-smtc-q1-2027-earnings-transcript/
22. BusinessWire — "Semtech Announces Fourth Quarter and Fiscal Year 2026 Results" (2026-03-16). *Q4 FY26 net sales $274.4M (+3% q/q, +9% YoY), adj EPS $0.44; FY26 record net sales $1.05B, +15%; eighth consecutive quarter of growth.* https://www.businesswire.com/news/home/20260316127252/en/Semtech-Announces-Fourth-Quarter-and-Fiscal-Year-2026-Results
23. BusinessWire / Investing.com — Semtech convertible notes pricing (2025-10-07). *$350M + $52.5M greenshoe = $402.5M of 0.00% convertible senior notes due 2030; conversion rate 9.8964 sh/$1,000 = $101.05 conversion price (42.5% premium); capped call cap $141.82 (100% premium); proceeds used to exchange 1.625% 2027s and 4.00% 2028s and repay term loans.* https://www.investing.com/news/company-news/semtech-prices-350-million-convertible-notes-offering-due-2030-93CH-4276918
24. StockTitan — Semtech Q1 FY27 10-Q summary. *2030 Notes excluded from diluted share count for the quarter ended 2026-04-26 because conversion price exceeded average market price; cash $163.3M; principal debt $492–503M; net interest income position.* https://www.stocktitan.net/sec-filings/SMTC/10-q-semtech-corp-quarterly-earnings-report-63b8c4818a5e.html
25. SEC EDGAR — Semtech 8-K, 2026-07-06, Item 1.01. *New Credit Agreement with Morgan Stanley Senior Funding as administrative agent: $360M revolving credit facility, undrawn at closing, plus uncommitted incremental term loan facility.* https://www.sec.gov/Archives/edgar/data/88941/000008894126000022/smtc-20260706.htm
26. SEC EDGAR — Semtech 8-K, 2026-06-02, Item 5.02. *Human Capital and Compensation Committee approved amendment and restatement of the Executive Severance Plan to add non-change-of-control severance. Compensation matter only — no executive departure.* https://www.sec.gov/Archives/edgar/data/88941/000008894126000019/smtc-20260602.htm
27. Nasdaq / TradingDay — SMTC short interest (snippet_only, settlement date not stated). *6.5M shares short, +17.1% period-on-period, 7.0% of float; days to cover 2.2, +118%.* https://www.nasdaq.com/market-activity/stocks/smtc/short-interest · https://www.tradingday.com/stocks/smtc/short-interest.html
28. TipRanks / TradingKey — SMTC ownership (snippet_only). *~72.04% institutional, ~0.47% insider, ~27.49% public/other; institutional shares +0.35% over three months.* https://www.tipranks.com/stocks/smtc/ownership
29. StockStory / AlphaStreet — "Why Semtech (SMTC) Stock Is Trading Up Today" (2026-08-17). *SMTC +9.0–9.9% on the Compal divestiture plus a Needham positive reiteration on data-centre demand; peers MTSI +3.3%, SITM +4.7%, LSCC +4.0%.* https://stockstory.org/us/stocks/nasdaq/smtc/news/why-up-down/why-semtech-smtc-stock-is-trading-up-today-3 · https://news.alphastreet.com/semtech-jumps-9-0-amid-sector-wide-rally/
30. Simply Wall St (via Yahoo Finance) — "Semtech (SMTC) Dropped, So What Is Behind The Latest Attention?" (2026-08-19). *Confirms 12.31% single-day decline; price $135.23; 79.68% YTD return; 429.69% 3-year TSR; P/S 11.6x vs industry 7.2x and peers 6.2x; fair-value estimate $204.83.* https://finance.yahoo.com/markets/stocks/articles/semtech-smtc-dropped-behind-latest-161223531.html
31. Bloomberg / StartupHub — market wrap, 2026-08-18. *Chip selloff on inflation and government-debt anxiety with elevated bond yields; semis -5%, Nasdaq-100 -1.7%; Micron -7.02%, ARM -6.67%, Intel -6.58%.* https://www.bloomberg.com/news/articles/2026-08-17/stock-market-today-dow-s-p-live-updates · https://www.startuphub.ai/ai-news/ai-stocks-daily/2026/ai-stocks-2026-08-18
32. StockAnalysis — SMTC analyst forecast page. *15 analysts, Strong Buy (12 SB / 1 B / 2 H); mean PT $201.38 (+66.55%), high $230, low $155; FY27 revenue $1.36B (+29.8%), FY27 EPS $2.65, FY28 EPS $3.89 (+47.06%); forward P/E 45.65x.* https://stockanalysis.com/stocks/smtc/forecast/
33. AltIndex — SMTC Reddit mentions and sentiment (snippet_only, undated). *Reddit sentiment 88/100 bullish with 0 mentions/day, -100% vs recent average; peers AMD 131/day, Intel 605/day; March 2026 StockTwits sentiment "extremely bullish" 84/100 on "extremely high" volume.* https://altindex.com/ticker/smtc/reddit-mentions
34. TipRanks — SMTC forecast (snippet_only). *22 analysts, average 12-month PT $209.30.* https://www.tipranks.com/stocks/smtc/forecast
35. S&P Global via CNN Markets (snippet_only). *14 analysts, consensus Strong Buy, average PT $205.25; fair-value estimate raised $110.47 → $230.00 on stronger long-term data-centre demand assumptions.* https://www.cnn.com/markets/stocks/SMTC
36. Public.com — SMTC forecast (snippet_only, as of 2026-08-10). *14 analysts: 57% Strong Buy, 36% Buy, 7% Hold.* https://public.com/stocks/smtc/forecast-price-target
37. Benzinga — SMTC analyst ratings. *Benchmark raised PT to $230 from $120 (Buy); Craig-Hallum (Anthony Stoss) raised PT to $205 from $105 (Buy).* https://www.benzinga.com/quote/SMTC/analyst-ratings
38. Sahm Capital — "Semtech Stock Gains After Q1 Results Beat Estimates, Analysts Raise Price Targets" (2026-05-27). *UBS (Timothy Arcuri) raised PT to $225 from $165, Buy.* https://www.sahmcapital.com/news/content/semtech-stock-gains-after-q1-results-beat-estimates-analysts-raise-price-targets-2026-05-27
39. Investing.com — "Northland downgrades Semtech stock rating on valuation concerns". *Gus Richard cut SMTC to Market Perform from Outperform ~2026-05-26 on valuation; cited 53x FY28 consensus.* https://www.investing.com/news/analyst-ratings/northland-downgrades-semtech-stock-rating-on-valuation-concerns-93CH-4709488
40. Investing.com — "Northland downgrades chip stocks on AI spending, supply concerns". *Sector-wide downgrade of ALAB, INTC and SMTC to Market Perform; semis "priced for perfection", elevated risk over next two quarters.* https://www.investing.com/news/stock-market-news/northland-downgrades-chip-stocks-on-ai-spending-supply-concerns-93CH-4709280
41. TipRanks — "Semtech Stock Sags As AI Euphoria Meets Reality" (2026-06-15). *Profit-taking after a 300% year; insider selling by CEO, CFO and COO amplifying overvaluation concerns; PTs lifted toward $230; design-win/backlog offset.* https://www.tipranks.com/news/catalyst/semtech-stock-sags-as-ai-euphoria-meets-reality
42. Semtech careers / LinkedIn (snippet_only, undated). *~25 open roles, actively hiring. Also: global semiconductor sales record $120.6B in May 2026, +104.1% YoY, 15th consecutive monthly record.* https://www.semtech.com/careers
43. Investing.com — "Semtech jumps 4% on strong guidance after Q1 earnings, revenue beat". *After-hours reaction to the Q1 FY27 print (+~4%), which did not hold into the 2026-05-27 close (-4.41% per [11]).* https://www.investing.com/news/earnings/semtech-jumps-4-on-strong-guidance-after-q1-earnings-revenue-beat-93CH-4710728
44. SEC EDGAR — all Semtech Form 4 filings 2026-05-25 to 2026-08-21 (32 filings, parsed individually from primary XML). *Insider-by-insider open-market sale totals; per-transaction dates, share counts and prices; `aff10b5One` flag and plan-adoption footnotes used to separate 10b5-1 from discretionary sales; zero purchases.* https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000088941&type=4&dateb=&owner=include&count=40
45. SEC EDGAR — Form 4, Asaf Silberstein (EVP & COO), transaction 2026-08-17. *5,000 shares sold at $150.00; footnote: pursuant to a Rule 10b5-1 plan adopted 2026-04-08; 88,862 shares held after.* https://www.sec.gov/Archives/edgar/data/88941/000151495426000031/wk-form4_1787169685.xml
46. Kessler Topaz — Semtech Corporation securities fraud class action case page. *Case caption, class period and allegation detail.* https://www.ktmc.com/semtech-corporation/
47. Semtech IR / LA Business Journal. *CEO transition: Paul Pickle departed; Dr. Hong Q. Hou appointed President and CEO effective 2024-06-06 following board differences.* https://www.semtech.com/company/press/semtech-appoints-semiconductor-industry-leader-hong-q-hou-as-president-and-ceo · https://labusinessjournal.com/featured/semtech-adjusting-to-abrupt-ceo-change/
48. Intellectia — NVIDIA August 2026 earnings preview. *PHLX Semiconductor Index at new highs in August 2026; sector sentiment context.* https://intellectia.ai/blog/nvidia-earnings-august-2026
49. CNBC — "Chip stocks shed more than $1 trillion as selloff hits companies powering AI boom" (2026-07-29). *July 2026 AI-semis drawdown context.* https://www.cnbc.com/2026/07/29/chip-selloff-sk-hynix-samsung-softbank.html
50. Forbes — "Semiconductor Selloff Deepens As AI Spending Fears Hit Intel" (2026-07-08). *Early-July 2026 semiconductor drawdown context.* https://www.forbes.com/sites/petercohan/2026/07/08/intel-stock-down-21-inside-the-july-2026-semiconductor-selloff/
51. Tickeron — "Semtech Corporation (SMTC) Falls -20% in 30 Days After Semiconductor Sector Selloff" (snippet_only). *Wafer and materials cost inflation; ~20 semiconductor peers implementing price increases from 2026-07-01; TSMC capex/margin warning as a sector catalyst.* https://tickeron.com/blogs/semtech-corporation-smtc-falls-20-in-30-days-after-semiconductor-sector-selloff-15060/
52. Intellectia — "Nvidia Earnings August 26 2026: AI Chip Leader Q2 Preview". *NVDA reports Q2 FY27 after the close Wednesday 2026-08-26; 40 analysts at ~$91.85B revenue / $2.08 EPS; hyperscaler 2026 capex commitments estimated $775–800B.* https://intellectia.ai/blog/nvidia-earnings-august-26-2026-preview
53. TipRanks — "Options Volatility and Implied Earnings Moves This Week, August 24 – August 27, 2026" (snippet_only; page 403 to direct fetch). *Confirms NVDA, CRM, CRWD and MRVL all report in the same window as SMTC; SMTC consensus $0.61 EPS vs prior-year $0.41, revenue +27.6% to $328.67M.* https://www.tipranks.com/news/options-volatility-and-implied-earnings-moves-this-week-august-24-august-27-2026
54. Yahoo Finance — "Coherent (COHR) & Lumentum Holdings (LITE): Two AI Optics Suppliers Just Beat Earnings. Why Did Investors Punish One of Them?" and "Coherent Falls 12%, Lumentum Drops 7% as AI Optics Stocks Cool Ahead of Earnings". *Peer beat-and-fade dynamic; COHR +93% YTD into the print left "little room for anything short of a clean beat".* https://finance.yahoo.com/markets/stocks/articles/coherent-cohr-lumentum-holdings-lite-180139462.html · https://finance.yahoo.com/markets/stocks/articles/coherent-falls-12-lumentum-drops-162541572.html
55. SEC EDGAR / Investing.com — Coherent 8-K (2026-08-12) and Lumentum Q4 FY26 transcript (2026-08-11). *COHR: revenue $2.045B (+33.7%), Datacenter & Comms $1.615B (79% of sales, +59% pro forma), non-GAAP EPS $1.74 (7.6% beat), Q1 guide $2.2–2.4B vs $2.14B Street, shares -4% AH; industrial segment -16%. LITE: adj EPS $3.23 vs $2.95, revenue $1.01B vs $984.57M, sales +109% YoY, 8th straight growth quarter, non-GAAP GM >50% first time, +1.51% AH.* https://www.sec.gov/Archives/edgar/data/0000820318/000119312526346860/d128030dex991.htm · https://www.investing.com/news/transcripts/earnings-call-transcript-lumentum-tops-q4-2026-forecasts-as-ai-demand-lifts-outlook-93CH-4852933
56. Yahoo Finance / Simply Wall St — Astera Labs Q2 2026 (reported 2026-08-04). *Guided Q2 revenue $355–365M (+85–90% YoY), GAAP diluted EPS $0.44–0.46; Scorpio X-Series in volume production, expected largest product family in Q3 (a quarter early); shares -12% since reporting on higher operating expenses.* https://finance.yahoo.com/markets/stocks/articles/investors-hold-astera-labs-stock-175100478.html
57. Semtech blog / Q4 FY26 transcript — DesignCon 2026 and ACC MSA. *1.6T ACCs demonstrated running live traffic to NVIDIA 224G SerDes; CopperEdge shipping for 1.6T ACC hyperscaler deployment; co-founding member of the ACC MSA with AMD, Dell and NVIDIA.* https://blog.semtech.com/designcon-2026-semtech-leads-the-charge-toward-200g-and-the-linear-interconnect-future
58. BusinessWire — "Semtech Corporation to Host Data Center Teach-in Event on Oct. 15, 2026" (2026-08-14). *Teach-in in San Jose, 9 a.m. PT, with CEO Hong Hou, SVP/GM Signal Integrity Imran Sherazi and CFO Mark Lin presenting strategy, technology portfolio, growth opportunities and long-term financial objectives.* https://www.businesswire.com/news/home/20260814576040/en/Semtech-Corporation-to-Host-Data-Center-Teach-in-Event-on-Oct.-15-2026

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
