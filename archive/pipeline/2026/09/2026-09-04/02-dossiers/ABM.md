# ABM — ABM Industries Incorporated

**What this print is about.** ABM is not going to be judged on the $1.01–$1.04 headline EPS line — it has missed sell-side EPS in four consecutive quarters and the stock still rose on two of them [12][13]. This print is about one arithmetic problem: management has promised a fiscal-2026 segment operating margin of 7.8–8.0% and adjusted EPS of $3.85–$4.15, but delivered only 7.2% segment margin and $1.72 of adjusted EPS in the first half [3]. That leaves the back half needing roughly 8.4% segment margin and $2.13–$2.43 of EPS — a 25–43% year-on-year step-up in H2 profitability (my arithmetic on sourced inputs). Q3 (quarter ended 31 Jul 2026) is the quarter where that promise either shows up in the numbers or gets walked back. ABM walked back exactly this kind of promise at the equivalent quarter a year ago, guiding to "the low end" on 5 Sep 2025 [4]. Set against that: revenue has beaten consensus for eight straight quarters [12], Q3 estimates have been revised *up* (3 up, 0 down, $0.98 → $1.01 over 60 days) [16][18], the Technical Solutions/AI-data-centre/microgrid story is corroborated by very strong peer prints from EMCOR and Aramark [27][28], and the office leasing backdrop is at a post-pandemic high [29]. The stock enters +18.4% over three months and 5.8% below its 52-week high [9] — a materially less forgiving setup than June, when it printed off a multi-year low.

**Event confirmed: YES** (company press release, GlobeNewswire, 25 Aug 2026) [1]. Note one data-vendor conflict: TipRanks labels the 8 Sep event "After Close, Confirmed" [11] and a MarketBeat URL slug carries 2026-09-03 [—]. The company source is authoritative and unambiguous: **Tuesday 8 September 2026, before market open, call at 8:30 AM ET** [1].

---

## 1. Event & anchors

| Item | Value | As of | Source / note |
| --- | --- | --- | --- |
| Earnings date | 2026-09-08 | confirmed 2026-08-25 | Company PR [1] |
| Session | **bmo** — release before open, call 8:30 AM ET | | Company PR [1] |
| Fiscal period | Fiscal Q3 2026, quarter ended 31 Jul 2026 | | Company PR [1] |
| Date changed / pre-announced? | No. No 8-K filed with SEC since 2026-06-05 | 2026-09-04 | EDGAR submissions [19] |
| Spot | **$47.23** (close) | 2026-09-03 16:00 ET / 20:00Z | stockanalysis [6], Yahoo chart API [9], Nasdaq API "LAST TRADE $47.23" [10] |
| Prior close / day range | $46.46 / $46.50–$47.27 | 2026-09-03 | Yahoo chart API [9] |
| Market cap | **$2.77B** (58.58M shares × $47.23) | 2026-09-03 | stockanalysis [6] |
| 52-week range | $36.96 – $50.12 | 2026-09-03 | stockanalysis [6]; confirmed in OHLC [9] |
| Position vs 52w | −5.8% from high, +27.8% from low | 2026-09-03 | derived from [9] |
| Fwd P/E · EV/EBITDA · Div yield | 11.47x · 10.53x · 2.46% ($1.16) | 2026-09-03 | stockanalysis [6][7] |
| Beta (5y) | 0.68 | | stockanalysis [7] |
| **Event-implied move** | **≈ ±7.0%** (see derivation below) | 2026-09-04 pre-open quotes | **Derived by me** from Nasdaq option chain [10]. No published implied move found. |
| Sep-18 ATM straddle | ≈ 7.3–7.7% of spot; implied vol ≈ 47–49% | 2026-09-04 | Derived from [10] |
| IV rank / percentile | **unavailable** (current). Only stale reference: IV 39.24%, IV Rank 54.76% on 2025-09-11 [15] | — | see Coverage gaps |
| Realised vol 20d / 30d / 60d | 15.1% / 18.8% / 22.0% (annualised) | 2026-09-03 | derived from [9] |

### Implied-move derivation (my work — read the caveat)

ABM's listed options are **extremely thin**. In the window 2026-09-04 → 2026-12-31 the Nasdaq chain returns exactly **two expiries** (18 Sep 2026 and 16 Oct 2026), $5.00 strike increments, and total Sep-18 open interest across every strike of roughly **88 contracts** [10]. There are no weeklies. Quotes are wide (Sep-18 $45 call 2.35/3.80).

Using the Sep-18 $45 strike — the only internally consistent pair (call mid $3.075, put mid $0.85; put-call parity implies a forward of $47.23, matching spot) — implied vol solves to **46.7% (call) / 49.1% (put)**, and a synthetic ATM straddle at $47.23 is worth **7.3–7.7% of spot** for the 14 calendar days to expiry. Stripping out non-event diffusion at the recent 19% realised vol leaves a **one-sigma event move of ~8.6%, or ~6.9% on a straddle-price basis**. I use **±7.0%** as the headline number and flag it as low confidence.

*Sanity check:* ±7.0% sits slightly above the 5.81% mean absolute realised D0 move of the last six quarters and slightly below the 6.47% mean of the last eight — a normal, modest event premium. **This is a plausible number, not a market-observed one.**

### Realised one-day earnings reactions (close-to-close, D0)

Computed from Yahoo daily OHLC [9]; the four most recent match TipRanks' published reaction column exactly (+6.67 / −4.62 / +5.49 / +0.33) [11], which validates the method.

| Report date | Quarter | Prev close | Gap at open | **D0 close-to-close** | D+1 | D0+D+1 | Intraday low vs prev close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-05 | Q2 FY26 | 39.88 | +4.66% | **+6.67%** | −0.26% | +6.39% | +4.26% |
| 2026-03-10 | Q1 FY26 | 43.28 | −3.37% | **−4.62%** | −0.99% | −5.57% | **−9.61%** |
| 2025-12-17 | Q4 FY25 | 45.74 | +4.46% | **+5.49%** | **−9.91%** | −4.96% | +1.88% |
| 2025-09-05 | Q3 FY25 | 48.10 | −0.69% | **+0.33%** | −2.90% | −2.58% | **−8.40%** |
| 2025-06-06 | Q2 FY25 | 51.26 | −5.46% | **−9.07%** | +3.52% | −5.87% | −15.33% |
| 2025-03-12 | Q1 FY25 | 49.83 | +4.37% | **−8.67%** | +3.41% | −5.56% | −10.86% |
| 2024-12-18 | Q4 FY24 | 54.91 | −9.43% | **−8.36%** | +1.63% | −6.87% | −10.38% |
| 2024-09-06 | Q3 FY24 | 56.10 | +6.56% | **−8.57%** | −2.63% | −10.98% | −8.59% |

**Last 6 quarters:** mean |move| **5.81%**, median |move| **6.08%**, max |move| **9.07%**, **3 up / 3 down**, signed mean −1.65%.
**Last 8 quarters:** mean |move| **6.47%**, median |move| **7.51%**, max **9.07%**, **3 up / 5 down**, signed mean **−3.35%**, signed median **−6.49%**.

Three patterns I regard as material:

1. **The two-day move has been negative in 7 of the last 8 prints** (only Q2 FY26 was positive). Mean D0+D+1 = −4.50%. The Dec-2025 print is the cleanest example: +5.49% on the day, then **−9.91%** the next session on 2.6M shares.
2. **The open is a terrible guide.** Q1 FY25 gapped +4.37% and closed −8.67% (a 13-point reversal); Q3 FY24 gapped +6.56% and closed −8.57% (15 points). Q3 FY25 gapped −0.69%, traded −8.40% intraday, and closed **+0.33%**. This happens *despite* the call being pre-open.
3. **Intraday ranges are far wider than close-to-close.** Any strategy keyed to the open or to an intraday stop faces roughly double the headline volatility.

*My inference, labelled as such:* the 2024–2025 portion of this sample coincides with a $56 → $37 downtrend, so the negative signed base rate is partly a trend artefact and should be discounted — but not to zero.

---

## 2. The bar

| Metric | Consensus | Source |
| --- | --- | --- |
| Q3 FY26 adjusted EPS | **$1.01** (Zacks) / **$1.04** (Investing.com) | [12][16][18]; Nasdaq/stage-0 also $1.01 |
| Q3 FY26 revenue | **$2.32B** (Investing.com) / ~$2.332B (snippet) | [12] |
| Analyst count | 8 covering (stockanalysis); 3 EPS estimators (Nasdaq/stage-0) | [8] |
| Consensus price target | **$52.43** avg / $52 median; range $45–$68 | [8] |
| Consensus rating | Buy (stockanalysis, 8 analysts) | [8]; Zacks Rank **#3 Hold** [13] |
| FY26 adjusted EPS consensus | **$3.94** (Zacks) / $3.98 (stockanalysis) | [14][8] |
| FY26 revenue consensus | $9.23B (+5.5%) | [8] |

**Year-ago comparison (fiscal Q3 2025, quarter ended 31 Jul 2025), from the company's own 8-K exhibit [4]:**
revenue **$2,224.0M** (+6.2%, organic +5.0%); GAAP EPS $0.67; **adjusted EPS $0.82**; adjusted EBITDA $125.8M (5.9% margin); FCF $150.2M; segment revenue B&I $1,038.7M / M&D $408.9M / Aviation $291.8M / Education $235.1M / ATS $249.5M; segment operating profit $73.8 / $36.4 / $19.7 / $21.1 / $19.4M.

So consensus requires **+23% to +27% YoY adjusted EPS growth** on **+4.3% revenue growth**. That gap is entirely margin and share count.

**Estimate revisions.** Direction is **positive and unambiguous**: over the trailing 60 days three analysts raised Q3 estimates and none cut, moving the Zacks consensus from **$0.98 to $1.01** [16][18]; Zacks Research specifically raised its Q3 number to $1.00 on 26 June 2026 [17]. I could not source a clean 30/60/90-day revision grid — see Coverage gaps.

**Guidance versus Street.** FY26 guide is $3.85–$4.15 [3][5]; the **midpoint ($4.00) sits above the $3.94 consensus** [14]. That is unusual and means the Street does not fully believe the guide. At Q2 the company also (a) tightened organic revenue growth to "toward the upper end of 3–4%", (b) tightened segment operating margin to the **lower end** of 7.8–8.0%, and (c) **raised** the FY26 interest-expense assumption to **~$110M** from the original $95–105M [3][5] — a quiet ~$0.06–0.09 of EPS headwind absorbed inside an unchanged range.

**What ABM has to deliver just to hold the stock flat (my construction from sourced inputs):**

- **Adjusted EPS ≥ ~$1.01–$1.04.** Nothing about a beat here is routine: on Investing.com's consensus series ABM has missed EPS for four straight quarters (−13.7%, −19.3%, −4.6%, −2.2%) [12] — though the miss is shrinking each quarter.
- **Revenue ≥ ~$2.35B.** Consensus at $2.32B implies only +4.3% growth. Q2 grew +8.4% (6.1% organic + 2.3% acquisition) [3] and Q3 carries a full quarter of WGNSTAR. On a 6% organic + 2% acquisition run-rate the print would be ~$2.40B. **I think the revenue bar is low and a beat is close to the base case.**
- **Segment operating margin ≈ 8.0%+.** This is the real bar — see next section.
- **Reaffirm $3.85–$4.15 without narrowing to the low end.** Narrowing to "the low end" would put the implied FY number at/below $3.85 versus $3.94 consensus, a ~2%+ FY cut. That is precisely what happened on 5 Sep 2025 [4].

**Whisper number: unavailable.** No credibly published whisper found.

---

## 3. The one metric that matters

> **Segment operating margin for fiscal Q3 2026, and whether management reaffirms the full $3.85–$4.15 range rather than narrowing to the low end.**

Not EPS. The evidence that the market trades ABM on margin trajectory and outlook rather than the EPS line is direct: on 5 Jun 2026 ABM **missed** the Zacks EPS consensus ($0.90 vs $0.92) and the stock **rose 6.67%** on a revenue beat, record bookings and a reaffirmed range [13][11][32]; on 17 Dec 2025 it missed by 19.3% and still closed **+5.49%** before reversing [12][9]. Conversely on 10 Mar 2026 the stock fell despite a revenue beat, because Technical Solutions margin disappointed on project timing and mix [31].

**The arithmetic (my derivation; every input sourced).** ABM defines segment operating margin as the sum of the five segments' operating profit over total revenue — I verified this reproduces the company's own reported figure for Q2 FY26 ($166.8M / $2,290M = 7.28% ≈ the reported 7.3% [3]).

| | Segment operating margin |
| --- | --- |
| Q3 FY25 (actual) | **7.66%** (derived from [4]: $170.4M / $2,224.0M) |
| H1 FY25 (actual) | 7.8% [3] |
| FY25 (actual) | 7.9% [5] |
| Q2 FY26 (actual) | 7.3% [3] |
| H1 FY26 (actual) | **7.2%** [3] |
| FY26 guide | 7.8–8.0%, **"lower end"** [3] |
| **H2 FY26 required to reach 7.8%** | **≈ 8.4%** (on $9.23B FY revenue [8]) |
| **H2 FY26 required to reach 8.0%** | ≈ 8.8% |

Q4 is seasonally ABM's strongest quarter (Q4 FY25 segment margin backs out to ~8.4%). Even crediting that, **Q3 FY26 needs roughly 8.0–8.2%** — a ~70–90bp sequential step-up from Q2's 7.3%, of which only ~40bp is seasonal (Q2 FY25 → Q3 FY25 was +38bp).

**The EPS bridge says the same thing.** H1 FY26 adjusted EPS $1.72 vs guide $3.85–$4.15 leaves **$2.13–$2.43 for H2**, against H2 FY25 actual of $1.70 ($0.82 + $0.88) [3][4][5] — **+25% to +43% YoY**. If Q3 lands at consensus $1.01, **Q4 must then be $1.12–$1.42 versus $0.88 last year (+27% to +61%)**. If Q3 comes in at, say, $0.95, the Q4 requirement becomes arithmetically implausible and the FY guide has to move.

**What the market expects for it, and how I know:** management explicitly told the Street on the Q2 call that margin expansion would be **"weighted to the second half," driven by service mix in Technical Solutions, strategic contract exits, price escalation and cost actions** [13][3]. The $35M annual run-rate restructuring programme launched in Aug 2025 should be fully in the run-rate by now [4]. Three analysts raised Q3 numbers on the back of that [16][18]. So the Street has, at the margin, chosen to believe it.

**Secondary metric to watch:** nine-month new sales bookings. ABM led its Q3 FY25 release with ">$1.5B through three quarters, +15% YoY" [4] and reported a record $1.2B first-half in FY26 [3]. A 9M FY26 bookings number above ~$1.8B would be the cleanest forward-looking positive.

---

## 4. Fundamentals — what changed, what is at stake

**Q2 FY26 (last reported, quarter ended 30 Apr 2026) [3]:**

| Segment | Revenue | YoY | Op profit | Margin |
| --- | --- | --- | --- | --- |
| Business & Industry | $1,015.8M | flat | $76.7M | 7.6% |
| Manufacturing & Distribution | $463.8M | +16.5% | $40.6M | 8.8% |
| Aviation | $310.8M | +19.5% | $16.3M | 5.2% |
| Education | $232.2M | +1.9% | $16.4M | 7.1% |
| Technical Solutions (ATS) | $267.3M | +27.2% | $16.8M | 6.3% |
| **Total** | **$2,290M** | **+8.4%** (6.1% organic, 2.3% acq.) | $166.8M | **7.3%** |

Adjusted EPS $0.90 (vs $0.86); GAAP $0.73; adjusted EBITDA $131.7M (5.8% margin); operating cash flow $66.2M, FCF $22.4M; capex $43.8M; total debt $1.9B, **total leverage 3.2x with a stated target of below 3.0x by fiscal year-end**; liquidity $613.8M; **record H1 bookings $1.2B** [3].

**What changed since the last print:**

- **Mix is shifting toward lower-margin, faster-growing work.** ATS grew +27% but at only 6.3% operating margin, and management said the battery-energy-storage projects are "heavy on equipment, heavy on infrastructure and the margins are a little less" [—transcript coverage, 3]. Aviation grew +19.5% at 5.2% margin. Meanwhile the highest-margin legacy business (B&I at 7.6%, M&D at 8.8%) is the slow-growth part. **This is a structural headwind to the 8.0% segment-margin target that volume alone does not fix** — my inference.
- **B&I revenue went flat**, on strategic client exits and pricing discipline [3][13]. Management frames this as deliberate margin repair.
- **WGNSTAR** closed 4 Feb 2026 for ~$275M cash, funded by a $255M incremental term loan; semiconductor/high-tech technical services; **modestly dilutive to FY26 adjusted EPS** (intangible amortisation + interest), guided $0.05–$0.07 accretive in FY27 [24][26]. Q3 FY26 is its first full clean quarter.
- **Buybacks were switched off.** Q1 FY26: 2.07M shares at $44.13 for $91.1M. **Q2 FY26: just $3.0M** [3][25]. $89.0M of authorisation remained at 30 Apr 2026 [24]. The company is deleveraging from 3.2x toward <3.0x, so **there is no buyback bid supporting the shares into or immediately after this print** — my inference from [3][24].
- **Interest expense guide raised** to ~$110M from $95–105M [3][5].
- **Self-insurance is the recurring landmine.** Reserves stood at **$679.0M** at 30 Apr 2026; the Q2 interim actuarial review concluded **no prior-year adjustment was required** [24]. That is good news for Q2 but note that ABM **changed its definition in FY25 to stop excluding prior-year self-insurance adjustments from adjusted metrics** [4] — so any Q3 actuarial swing flows *straight into adjusted EPS*. A $(0.26) prior-year self-insurance charge is exactly what blew up Q4 FY25 [5]. This is a genuine two-sided tail on the EPS line.
- **No goodwill impairment; goodwill $2,738.4M** (up from $2,591.1M on the $146.0M WGNSTAR addition). Litigation accrual $8.3M, reasonably-possible range $0–$15.1M; "not a party to any material legal proceedings." No customer-concentration disclosure. In compliance with all covenants (max total net leverage 5.00x, secured 4.00x, interest coverage 1.50x) [24].
- **New business colour:** LaGuardia Terminal B autonomous robotics pilot announced 28 Jul 2026 (inspection quadruped with Skild.ai, autonomous scrubbers/vacuums with CenoBots) [35]. Small financially; useful as evidence the labour-productivity story is real.

**What's at stake:** with the guide midpoint above consensus and 75% of the year gone after this print, Q3 is the last quarter in which ABM can plausibly "make it up in Q4." A reaffirmation backed by an 8%+ segment margin re-rates a stock trading at 11.5x forward earnings. A narrowing to the low end, or another self-insurance charge, breaks the FY26 story and re-opens the 2024–25 credibility problem.

---

## 5. Positioning & options

**The headline finding: this is not a crowded trade in either direction, and the options market carries almost no information.**

- **Options are near-unusable.** Two expiries only in the next four months (18 Sep, 16 Oct), $5 strikes, **~88 total contracts of open interest across the entire Sep-18 chain**, most strikes showing no volume at all [10]. There is **no term structure to measure and no reliable skew** — the Sep-18 $50 put quotes 2.80/5.60 against $2.77 of intrinsic value, i.e. the bid is essentially intrinsic. Any "unusual options activity" read on this name would be noise. *Practical consequence: institutional holders cannot hedge this print cheaply, so realised moves can overshoot with no dealer flow to dampen them* — my inference.
- **Derived implied move ~±7.0%** (see §1), implied vol ~47–49% on the 14-day Sep-18 straddle against **realised vol of 15.1% (20d) / 18.8% (30d)** [9]. The entire premium is event premium.
- **IV rank / percentile: unavailable.** Only stale data point: IV 39.24%, IV Rank 54.76% as of 11 Sep 2025 [15]. A Zacks note in late July 2026 flagged the **Oct-16 $60.00 call** as carrying some of the highest implied volatility in the equity universe [15] — on that chain, with 2 contracts of open interest, I would not treat it as a signal.
- **Short interest:** **1.88M shares, 3.26% of float, 3.22% of shares out, 4.63 days to cover**, float 57.89M [7]. A second provider shows **2.51M shares / 4.17% of float / 4.4 days to cover, +5.46% month-on-month** [38]. Either way: **modest, not a squeeze setup, not a crowded short.** Historical context: short interest peaked around 2.90M shares / 6.78% of float / 6.26 days to cover in Dec 2025 [37], so the short base has been reduced substantially over 2026.
- **Borrow fee / cost to borrow: unavailable** (Fintel returned HTTP 403).
- **Put/call ratio: unavailable.**
- **Ownership:** ~91.6% institutional [—see 34-adjacent coverage]; stockanalysis reports institutional ownership >100% (a normal artefact of lending) and insider ownership 1.14% [7]. Q2-2026 13F season showed net institutional buying, with Pzena adding >351k shares [—13F coverage].
- **Run-up into the print:** +18.4% over 3 months, +6.8% over 6 months, but **−3.5% over the last month and only +0.2% over the last five sessions** [9]. The stock topped at $49.36 (29 Jul) / $49.18 (4 Aug) and has drifted sideways-to-lower since, closing at $47.23 on 3 Sep. **Interpretation (mine): the momentum trade was put on in June–July and has been quietly bleeding for a month. It is neither a fresh breakout nor a capitulated bottom — the least informative possible position.**
- **Technicals:** 50-day SMA $46.92, 200-day SMA $43.48 [7]; a golden cross printed in late July [16]. Price sits just above both. 20-day average volume 337.8k [7] versus a 60-day average of 496k [9] — **volume has dried up into the event**, consistent with low participation.
- **Liquidity risk note:** average daily volume of ~340k shares on a $2.77B market cap means the post-print reaction is likely to be made by a small number of participants. Past prints traded 1.4–3.2M shares [9] — 4–9x normal.

---

## 6. Sentiment & alt-data

- **Analyst ratings/targets:** consensus "Buy" across 8 analysts, average target **$52.43**, median $52, range **$45–$68** [8]. But the two named recent actions are both **non-constructive**: Baird (Andrew Wittmann) raised its target to **$48 from $45 while keeping Neutral**, and Truist cut to **$45 from $47, Hold** [33]. Both sit at or below the current $47.23 spot. **My read: the "Buy" consensus is carried by a small number of high targets ($68 top of range) while the actively-updating analysts are neutral-to-negative on valuation.** Zacks Rank is **#3 (Hold)**, with Value A / Growth B / **Momentum D** / VGM A [13].
- **Price-target drift:** modestly upward — one aggregator shows the average moving from $51.43 to $51.86, another from $53.33 to $57.50 [—drift coverage]. I could not source a clean dated PT time series; treat drift as "flat to slightly up."
- **Estimate-revision sentiment is the clearest positive signal in the file:** 3 up / 0 down over 60 days, consensus $0.98 → $1.01 [16][18].
- **Retail/social tone:** essentially absent. TipRanks classifies retail investor sentiment as **"Very Negative"**, with **fewer than 0.1% of its retail users holding ABM**; 1.5% of holders changed position in 7 days and 10.7% in 30 days [34]. **This is a stock retail does not own or discuss.** I found no meaningful StockTwits/Reddit/WSB signal, which is itself the finding — social sentiment carries no information here and should be given zero weight.
- **Alt-data proxies:**
  - *Air travel (Aviation segment, 13.6% of Q2 revenue):* TSA screened a record ~18.7M travellers over the 2026 July 4 window and multiple all-time single-day records were set through summer 2026 [30]. **Directly supportive of Aviation volumes in the May–July quarter.**
  - *Office occupancy / leasing (B&I, 44% of Q2 revenue):* US office **leasing hit a new post-pandemic high in Q2 2026**, up 27% versus the 5-year average; overall availability fell to 23.1% in Q1 2026 from 24.8% a year prior, with 88% of markets improving; overall vacancy 18.6%, prime vacancy down 80bp to 12.7% [29]. Recovery is uneven — Manhattan and San Francisco at/above pre-pandemic, while Chicago, Houston and DC lag by 35–40% [29]. ABM named the **West Coast, Midwest and Mid-Atlantic** as its slow-recovery problem markets a year ago [4]; the macro data says two of those three are still the laggards.
  - *AI/data-centre infrastructure (ATS, 11.7% of Q2 revenue):* corroborated by EMCOR and Comfort Systems (§8).
  - *Google Trends / app ranks / web traffic / job postings:* **unavailable** — not applicable or not sourced for a B2B facility-services contractor.

---

## 7. Forensics

- **8-K cadence: silent.** ABM has filed **no 8-K since 2026-06-05** (the Q2 earnings 8-K) [19]. The 2026 8-K record is: 5 Feb (WGNSTAR close), 10 Mar (Q1 earnings), 25 Mar (annual meeting results), 5 Jun (Q2 earnings). **No pre-announcement, no guidance update, no management change, no financing event, no acquisition in the three months before this print.** For a company whose FY guide requires a large H2 ramp, three months of silence is neutral-to-mildly-reassuring: there has been no negative pre-release, but equally no positive one. *My inference.*
- **Form 4 activity — three sales, one of them notable:**

| Date | Insider | Role | Code | Shares | Price | Held after | Plan? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-12 | Scott B. Salmirs | President & CEO | S | 50,000 (39,576 @ $46.2492 + 10,424 @ $46.6859) | ~$46.34 | **434,861** | **10b5-1**, plan dated 2025-12-24 [20] |
| 2026-07-01 | David M. Orr | EVP & CFO | **F** (tax withholding, not a sale) | 539 | $44.54 | 36,034 | n/a [23] |
| 2026-07-13 | **Dean A. Chin** | **SVP & Chief Accounting Officer** | **S** | **3,958** @ $45.30–$45.36 | $45.3123 | 16,993 | **NO — discretionary open-market sale, 10b5-1 flag = 0** [21] |
| 2026-07-16 | Raul J. Valentin | EVP & CHRO | S | 1,639 | $48.00 | 49,036 | **10b5-1**, plan dated 2026-04-15 [22] |

  **The one that matters is Chin.** A **discretionary** (non-plan) open-market sale by the **Chief Accounting Officer** of ~**19% of his direct holdings** ($179k), seven weeks before the Q3 print, is the single most adverse insider datum in this file. I want to be careful: $179k is small in absolute terms, it was executed in an open window shortly after the Q2 10-Q, and the CAO's holdings are modest. It is a **yellow flag, not a red one**, and I would not build a thesis on it. The CEO's much larger sale was plan-driven and left him with 434,861 shares — no signal.
  **No insider buying at any point in 2026** [19][20-23].
- **Executive/director departures:** none found. Salmirs remains President & CEO; Orr remains CFO; Paul Goldberg remains IR contact [1]. New CIO and Chief Strategy Officer roles were *added* alongside the WGNSTAR deal in early 2026 [26] — expansion, not attrition.
- **Auditor / restatement:** none found. No goodwill impairment; no impairment indicators disclosed [24]. FY25 10-K filed on schedule 2025-12-19 [19].
- **Filing-language / accounting-policy shift — this is the important one.** In FY25 ABM made a **definitional change to stop excluding prior-year self-insurance adjustments from its adjusted metrics** [4]. That change removes a management lever but also removes a shock absorber: the $679.0M self-insurance reserve now transmits actuarial revisions **directly into adjusted EPS** [24]. The Q2 FY26 interim review required no adjustment [24]; whether a Q3 review does is unknowable from outside and is a live two-sided tail.
- **Capital-allocation signalling:** buybacks were $91.1M in Q1 FY26 and then **$3.0M in Q2** [3][25] with $89.0M still authorised [24]. Management is prioritising the sub-3.0x leverage target over the share count. *My read: a company confident in a large H2 earnings ramp with the stock at 11.5x forward would ordinarily be buying; it isn't. That is a mildly negative tell, though the stated deleveraging commitment is a sufficient benign explanation.*

---

## 8. Macro & peer read-through

**Regime.** ABM is a low-beta (0.68 [7]), labour-intensive, contract-based services roll-up — a defensive, value-factor, rate-insensitive name with negligible FX or commodity exposure. Its economics are wage inflation versus contractual price escalation. The one clean rate linkage is its floating-rate debt: $1.82B net long-term debt against ~$110M of FY26 interest expense [3][24], so the interest line is a modest headwind if short rates stay elevated.

**Peers who already reported, and how they traded:**

- **Aramark (ARMK), Q3 FY26 reported 2026-08-11** — adjusted EPS $0.52 vs $0.48 consensus, revenue $5.1B (+3.7% vs forecast), organic revenue +9%, client retention ~98%, both FSS US and FSS International with double-digit operating income growth, **outlook raised**, and a new multi-year data-centre/colocation workforce services engagement. **Shares +8.2%** [27]. *Read-through: the outsourced-facility-services demand environment and the pricing/retention backdrop are strong, and the data-centre adjacency is monetising. Positive for ABM's B&I and M&D volumes.*
- **EMCOR (EME), Q2 2026 reported 2026-07-30** — revenue +20% to $5.15B, record profitability, **remaining performance obligations $17.1B, +44% YoY with ~95% of the growth organic**, guidance raised; stock has since traded from ~$672 to ~$828 [28]. **Comfort Systems (FIX)** posted its first >$3B revenue quarter and closed the Hunt Electric acquisition [28]. *Read-through: the AI/data-centre electrical-and-mechanical build cycle is running hot. This is the direct comparable for ABM's Technical Solutions segment (microgrids, battery energy storage, EV infrastructure), which grew +27.2% in Q2 [3][36]. **Strongly supportive of an ATS revenue beat.** It does not, however, say anything reassuring about ATS **margin**, which is exactly where ABM disappointed in Q1 FY26 [31] and where the low-margin equipment content is a structural drag.*
- **Vestis (VSTS)** — the weak comparable: FY26 revenue guided **flat to down 2%**, and a 19-day Teamsters strike in Indianapolis was settled in early August 2026 with wage increases [—Vestis coverage]. *Read-through: uniform rental is a different end-market, but the labour-cost datapoint is relevant to any US route-and-labour services business.*
- **Sector framing:** RSM's review of facility-services Q4 calls found the group uniformly focused on growth initiatives, operational efficiency and technology investment [—RSM]. ABM's own AI/robotics push [35] fits that pattern.

**Customer/supplier read-throughs:**
- *Airlines/airports (Aviation):* record TSA throughput through summer 2026 [30]. ABM flagged one watch-item at Q2 — the potential impact of **rising fuel costs on airline clients** [—Q2 call coverage].
- *Commercial landlords (B&I):* leasing at post-pandemic highs, availability falling for eight consecutive quarters, but recovery concentrated in trophy assets and in Manhattan/SF rather than ABM's named soft markets [29][4].
- *Semiconductor fabs (M&D + WGNSTAR):* ABM has deliberately priced aggressively to win semiconductor and e-commerce work, which it acknowledged pressured M&D margin [4]. WGNSTAR deepens that exposure [26].

**Net macro assessment (mine):** the demand backdrop for every one of ABM's five segments is neutral-to-positive right now, and better than it was a year ago. **The macro supports the revenue line and says nothing supportive about the margin line** — and the margin line is what this print is about.

---

## 9. Bull case / bear case / base case

**Bull case (~35%).** Revenue beats comfortably — consensus at $2.32B implies only +4.3% growth against +8.4% in Q2 and a full quarter of WGNSTAR; a 6% organic + 2% acquisition run-rate produces ~$2.40B [3][12]. Q3 FY25 is an easy comp ($0.82 adjusted EPS, depressed by deliberate rebid pricing and pre-restructuring cost) [4], the $35M restructuring is fully in the run-rate [4], and Q3 is seasonally a ~40bp margin step-up from Q2. Peers are corroborating the demand story emphatically — Aramark +8.2% on a beat-and-raise [27], EMCOR RPO +44% [28] — while ABM's ATS grew +27% into that same cycle [3][36]. Estimates have been revised **up** with zero cuts [16][18], the office leasing backdrop is at a post-pandemic high [29], air traffic is at records [30], short interest is modest and falling [7][37], and the stock trades at 11.5x forward earnings and 10.5x EV/EBITDA versus a $52.43 consensus target [6][7][8]. If Q3 segment margin prints 8.0%+ and the range is reaffirmed, the credibility discount that has capped this stock since 2024 starts to close. The June 2026 print is the template: a headline EPS *miss* plus a revenue beat plus record bookings produced **+6.67%** [11][13].

**Bear case (~45%).** The back-half margin promise is the largest ABM has made in years and the company's track record on exactly this promise is poor. H1 delivered 7.2% against a full-year guide of 7.8–8.0%, requiring ~8.4% in H2 — and management has already conceded the **lower end** of the range [3]. On 5 Sep 2025, at the equivalent quarter, ABM cut FY25 to "the low end" of $3.65–$3.80 citing higher interest expense and near-term margin pressure [4] — and then still landed FY25 at $3.44 [5]. The FY26 guide midpoint of $4.00 sits **above** the $3.94 consensus [14], meaning any narrowing is a cut versus the Street. Mix is working against the target: the fastest-growing segments (ATS 6.3%, Aviation 5.2%) carry the lowest margins while the highest-margin B&I is flat [3]. Interest expense has already been marked up to ~$110M [3]. The $679M self-insurance reserve now flows straight into adjusted EPS after the definitional change [4][24], and a prior-year charge is exactly what broke Q4 FY25 [5]. ABM has missed EPS consensus four quarters running [12]. The buyback is switched off while the company deleverages from 3.2x [3][24]. The CAO made a discretionary sale of ~19% of his stake in July [21]. And positioning is unhelpful: the stock is +18.4% in three months, 5.8% from its 52-week high, above both moving averages [9][7], with Baird at $48 Neutral and Truist at $45 Hold [33] — no valuation cushion and no capitulated base. The base rate is genuinely ugly: **3 up / 5 down over the last eight prints, signed median −6.49%, and the two-day move negative in 7 of 8** [9][11].

**Base case (~50% of outcome mass, my central expectation).** ABM beats on revenue (~$2.36–2.42B) and lands adjusted EPS close to but probably a touch short of the $1.01–$1.04 consensus — extending the four-quarter miss streak but with the miss magnitude continuing to shrink (−13.7% → −19.3% → −4.6% → −2.2% [12]). Segment margin improves sequentially from 7.3% to roughly 7.8–8.1%, better than Q2 but likely at the bottom of what the full-year bridge requires. Management reaffirms $3.85–$4.15 but leans verbally toward the lower half, and the call becomes an argument about whether Q4 can carry $1.15+. The stock's realised move lands inside the ~±7% implied cone, skewed slightly negative — call it −2% to −4% — with materially wider intraday range than close-to-close range, per the pattern in §1. **The key asymmetry: a clean 8%+ segment margin plus an unqualified reaffirmation is worth more upside than an in-line print is worth downside, but the probability-weighted centre of the distribution sits just below zero because the bar is set by the company's own guide rather than by the Street's estimate.**

**My preliminary read: direction score −18, probability of an up move 43%, conviction Medium.** The negative tilt rests on (i) the H2 margin bar and ABM's own precedent of narrowing guidance at this exact quarter [3][4], (ii) an unfavourable run-up and the absence of a buyback bid [9][24], (iii) a 3-up/5-down historical base rate with a −6.49% signed median [9], and (iv) four consecutive EPS misses [12]. It is tempered — and the conviction held to Medium rather than High — by genuinely positive estimate revisions [16][18], a very supportive peer set [27][28], an easy year-ago comp [4], and an undemanding 11.5x forward multiple [6].

---

## 10. What would flip the consensus view

**The single most credible reversal: ABM prints a Q3 segment operating margin of 8.2% or better, raises the floor of the FY26 adjusted EPS range (e.g. to $3.95–$4.15), and reports nine-month new sales bookings above ~$1.9B.**

That combination would be concrete, checkable within minutes of the 8:30 AM ET call, and would do three specific things: it would prove the back-half margin bridge is real rather than aspirational, it would move the FY guide floor **above** the $3.94 Street number [14] rather than down toward it, and — with WGNSTAR turning $0.05–$0.07 accretive in FY27 [26] and ATS compounding into the data-centre cycle that EMCOR and Comfort Systems have just validated [28] — it would give the Street a credible >$4.40 FY27 EPS anchor. At 11.5x forward [6], that is a $50–55 stock rather than a $47 one, and it would justify the $52.43 consensus target [8]. Concretely, I would expect a same-day move of **+7% to +10%**, i.e. at or beyond the top of the implied cone, because the thin options market means no dealer flow to absorb it (§5).

The mirror-image flip that would confirm the bear case: **any narrowing to "the low end" of $3.85–$4.15, a Q3 segment margin below 7.6% (i.e. no year-on-year improvement over Q3 FY25's 7.66%), or a prior-year self-insurance charge.** Any one of those would rerun the 5 Sep 2025 script [4] and I would expect −6% to −9%.

**The lower-probability third path worth naming:** an in-line print with a reaffirmed guide could still produce the D0-up / D+1-down pattern seen in December 2025 (+5.49%, then −9.91% [9]). Anyone reading only the first day's close would draw the wrong conclusion.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **No published event-implied move from any provider.** TipRanks' daily "Options Volatility and Implied Earnings Moves" series does not cover 8 Sep 2026 or list ABM [—]; SpotGamma/MarketChameleon/Barchart/OptionSlam pages returned no numeric values via WebFetch. | My ±7.0% is a derivation from a chain with ~88 contracts of open interest. It could easily be wrong by ±2pp. The panel should treat the implied move as an estimate, not an anchor. |
| **IV rank / IV percentile: current value unavailable.** Only a stale 11 Sep 2025 reading (IV 39.24%, IV Rank 54.76%) [15]. | Cannot say whether options are rich or cheap versus ABM's own history. |
| **Options skew and term structure: unmeasurable.** Only two expiries exist in the next four months and quotes are wider than the values being measured [10]. | Removes the usual read on directional option positioning entirely. |
| **Put/call ratio and unusual options activity: unavailable.** | Would normally be a directional tell; here it would be noise even if I had it. |
| **Borrow fee / cost to borrow: unavailable** (Fintel HTTP 403). | Cannot confirm whether the modest short interest is cheap or constrained. Low importance given 3.3% of float. |
| **Clean 30/60/90-day estimate-revision grid: unavailable.** I have the 60-day direction ($0.98 → $1.01, 3 up / 0 down) [16][18] but not a dated series, and no revenue-estimate revision history. | The 60-day figure is the strongest positive signal in the file; I would like to know whether the momentum is accelerating or stalled. |
| **Whisper number: unavailable.** | Cannot tell whether the buy-side bar sits above the $1.01–$1.04 published bar. |
| **Q3 FY26 revenue consensus is provider-dependent** ($2.32B Investing.com [12]; ~$2.332B via snippet). | ~0.5% dispersion; low impact. |
| **Consensus dispersion / high-low EPS range: unavailable.** Providers disagree on the point estimate ($1.01 Zacks/Nasdaq vs $1.04 Investing.com) without publishing the range. | With only 3–8 estimators, the "consensus" is fragile and a "beat" is definition-dependent. |
| **Session conflict not fully resolved by a second high-quality source.** Company PR says BMO with an 8:30 AM ET call [1]; TipRanks labels it "After Close, Confirmed" [11]. | I am confident the company is right — every ABM print in this dossier's history was BMO — but the panel should know a major vendor disagrees. |
| **Google Trends, app ranks, web traffic, job postings, review data: not sourced.** | Mostly not applicable to a B2B contractor, but a job-postings series would have been a genuine proxy for ABM's headcount and margin plans. |
| **Segment-level Q3 FY26 consensus: unavailable.** | The one metric is a segment-margin figure and I have no published Street estimate for it — my ~8.0–8.2% requirement is derived arithmetic, not a surveyed number. |
| **Q4 FY25 segment operating margin is my back-calculation** (~8.4%) rather than a directly quoted figure. | Used only to argue Q4 seasonality; the direction is safe, the decimal is not. |
| **Domains unreachable this session:** fintel.io (403), zacks.com (bot wall), barchart.com (empty), marketchameleon.com (values behind interactive charts), investor.abm.com/news-releases index (timeout), stooq.com (connection reset). SEC EDGAR, Nasdaq API, Yahoo chart API and stockanalysis.com all worked. | Recorded per pipeline convention. |

---

## 12. Sources

1. ABM Industries — "ABM to Announce Third Quarter 2026 Financial Results", GlobeNewswire, 2026-08-25 — **event date 2026-09-08, before market open, call 8:30 AM ET, webcast + supplemental presentation, replay through 2026-09-22.** https://www.globenewswire.com/news-release/2026/08/25/3350870/799/en/abm-to-announce-third-quarter-2026-financial-results.html
2. Manila Times mirror of [1] — corroborating the event date/session. https://www.manilatimes.net/2026/08/26/tmt-newswire/globenewswire/abm-to-announce-third-quarter-2026-financial-results/2412116
3. ABM — "ABM Reports Fiscal Second Quarter 2026 Results and Reaffirms Fiscal 2026 Adjusted EPS Outlook", GlobeNewswire, 2026-06-05 — **Q2 FY26 revenue $2.29B (+8.4%, 6.1% organic), full segment revenue/operating-profit table, segment margin 7.3% Q2 / 7.2% H1, adjusted EPS $0.90 (H1 $1.72), GAAP $0.73, adjusted EBITDA $131.7M, OCF $66.2M, FCF $22.4M, debt $1.9B, leverage 3.2x vs <3.0x target, liquidity $613.8M, buybacks $3.0M Q2 / $94.7M H1, dividend $0.29, record H1 bookings $1.2B, FY26 guide (EPS $3.85–$4.15, organic upper end of 3–4%, segment margin lower end of 7.8–8.0%, interest ~$110M, tax 29–30%).** https://www.globenewswire.com/news-release/2026/06/05/3307288/799/en/ABM-Reports-Fiscal-Second-Quarter-2026-Results-and-Reaffirms-Fiscal-2026-Adjusted-EPS-Outlook.html
4. SEC EDGAR — ABM Form 8-K Exhibit 99.1, 2025-09-05 (Q3 FY25 press release) — **the year-ago comparison: revenue $2,224.0M (+6.2%, organic +5.0%), GAAP EPS $0.67, adjusted EPS $0.82, adjusted EBITDA $125.8M, FCF $150.2M, full segment revenue and operating-profit table (used to derive Q3 FY25 segment margin of 7.66%), $150M buyback authorisation increase, restructuring programme, FY25 guided "toward the low end" of $3.65–$3.80, definitional change on prior-year self-insurance adjustments, slow-recovery West Coast / Midwest / Mid-Atlantic office markets.** https://www.sec.gov/Archives/edgar/data/771497/000077149725000020/abm-ex99_1.htm
5. ABM — "ABM Reports Fourth Quarter and Full Fiscal 2025 Results and Provides Fiscal 2026 Outlook", GlobeNewswire, 2025-12-17 — **FY25 adjusted EPS $3.44, FY25 segment operating margin 7.9%, FY25 FCF $155.1M, leverage 2.7x, Q4 FY25 adjusted EPS $0.88 with a $(0.26) prior-year self-insurance impact, Q4 revenue $2.3B (+5.4%), original FY26 guidance ($3.85–$4.15, organic 3–4%, segment margin 7.8–8.0%, interest $95–105M, tax 29–30%).** https://www.globenewswire.com/news-release/2025/12/17/3206839/799/en/ABM-Reports-Fourth-Quarter-and-Full-Fiscal-2025-Results-and-Provides-Fiscal-2026-Outlook.html
6. StockAnalysis.com — ABM overview — **spot $47.23 as of 2026-09-03 16:00 EDT, market cap $2.77B, 58.58M shares out, PE 18.19, forward PE 11.47, dividend $1.16 / 2.46%, 52-week range $36.96–$50.12, beta 0.68, next earnings 2026-09-08, revenue TTM $9.05B.** https://stockanalysis.com/stocks/abm/
7. StockAnalysis.com — ABM statistics — **short interest 1.88M shares, 3.26% of float, 3.22% of shares out, 4.63 days to cover, float 57.89M, institutional ownership 100.78%, insider 1.14%, 50d SMA $46.92, 200d SMA $43.48, 20d avg volume 337,796, EV/EBITDA 10.53.** https://stockanalysis.com/stocks/abm/statistics/
8. StockAnalysis.com — ABM forecast — **8 analysts, consensus Buy, avg PT $52.43, median $52, range $45–$68, FY26 revenue $9.23B and EPS $3.98.** https://stockanalysis.com/stocks/abm/forecast/
9. Yahoo Finance chart API (`query1.finance.yahoo.com/v8/finance/chart/ABM?range=5y&interval=1d`) — **daily OHLCV used to compute every realised earnings reaction, gap, D+1, intraday range, run-up, realised volatility and moving-average figure in this dossier.** Last bar 2026-09-03, regularMarketPrice 47.23, regularMarketTime 2026-09-03 20:00:03Z. https://query1.finance.yahoo.com/v8/finance/chart/ABM?range=5y&interval=1d
10. Nasdaq options-chain API (`api.nasdaq.com/api/quote/ABM/option-chain`) — **"LAST TRADE: $47.23 (AS OF SEP 4, 2026)"; only two expiries (2026-09-18, 2026-10-16) in the 2026-09-04 → 2026-12-31 window; $5 strike increments; full bid/ask/volume/OI grid used to derive implied volatility and the ATM straddle.** https://api.nasdaq.com/api/quote/ABM/option-chain?assetclass=stocks&limit=500&fromdate=2026-09-04&todate=2026-12-31&excode=oprac&callput=callput&money=all&type=all
11. TipRanks — ABM earnings — **published price reactions +6.67% (Jun-05-26), −4.62% (Mar-10-26), +5.49% (Dec-17-25), +0.33% (Sep-05-25), which independently validate my computed series; Q3 2026 forecast $1.01; historical report-date list. Also labels the 8 Sep event "After Close, Confirmed" — conflicts with the company PR [1].** https://www.tipranks.com/stocks/abm/earnings
12. Investing.com — ABM earnings — **Q3 FY26 EPS forecast $1.04 and revenue forecast $2.32B; eight-quarter actual-vs-forecast table showing EPS misses of −2.17%, −4.6%, −19.27%, −13.68%, −1.15% and revenue beats in all eight quarters.** https://www.investing.com/equities/abm-industries-inc-earnings
13. Zacks (via Yahoo/TradingView) — "ABM Q2 Earnings Call Flags Strong Back-Half Margin Push" — **Zacks Q2 consensus was $0.92 (so $0.90 was a Zacks miss) against a $2.22B revenue consensus that was beaten by 2.95%; management's back-half margin-expansion language; organic growth now toward the high end of 3–4%; Zacks Rank #3 (Hold), Value A / Growth B / Momentum D / VGM A.** https://finance.yahoo.com/markets/stocks/articles/abm-q2-earnings-call-flags-085100598.html
14. Zacks (via Yahoo) — "ABM Stock Price Increases 11% Since Reporting Q2 Earnings Miss" — **FY26 Zacks consensus $3.94 versus a guided midpoint of $4.00; stock rallied 10.9% after the 5 Jun release despite the EPS miss.** https://finance.yahoo.com/markets/stocks/articles/abm-stock-price-increases-11-133500111.html
15. Zacks — "Do Options Traders Know Something About ABM Industries Stock We Don't?" — **Oct-16-2026 $60.00 call flagged for very high implied volatility; the only IV Rank datapoint found anywhere (39.24% IV / 54.76% IV Rank, dated 2025-09-11 — stale).** https://finance.yahoo.com/markets/options/articles/options-traders-know-something-abm-123000441.html
16. Zacks — "ABM Industries (ABM) Just Flashed Golden Cross Signal: Do You Buy?" — **50-day SMA crossed above the 200-day; no Q3 estimate cuts against 3 revisions higher in 60 days; stock +7.7% over four weeks and +23.7% over 90 days at time of writing; Zacks Rank #3.** https://finance.yahoo.com/markets/stocks/articles/abm-industries-abm-just-flashed-135501285.html
17. MarketBeat — "Q3 EPS Estimates for ABM Industries Raised by Zacks Research", 2026-06-29 — **Zacks Research raised its Q3 FY26 estimate to $1.00 in a note dated 26 June 2026.** https://www.marketbeat.com/instant-alerts/q3-eps-estimates-for-abm-industries-raised-by-zacks-research-2026-06-29/
18. Zacks estimate-revision data (via search snippet, `snippet_only`) — **Zacks Q3 consensus moved from 98 cents to $1.01 over 60 days on three upward revisions and zero cuts.** https://www.zacks.com/stock/quote/ABM/detailed-earning-estimates
19. SEC EDGAR — ABM submissions JSON (CIK 0000771497) — **complete filing cadence; confirms no 8-K since 2026-06-05, 10-Q filed 2026-06-05 for the period ended 2026-04-30, 10-K filed 2025-12-19, and the full 2026 Form 4 record.** https://data.sec.gov/submissions/CIK0000771497.json
20. SEC Form 4 — Scott B. Salmirs (President & CEO), filed 2026-06-12 — **50,000 shares sold (39,576 @ $46.2492; 10,424 @ $46.6859) under a Rule 10b5-1 plan adopted 2025-12-24; 434,861 shares held after.** https://www.sec.gov/Archives/edgar/data/771497/000122520826005990/doc4.xml
21. SEC Form 4 — **Dean A. Chin (SVP & Chief Accounting Officer)**, filed 2026-07-15 — **3,958 shares sold 2026-07-13 at a weighted-average $45.3123 ($45.30–$45.36); `aff10b5One` flag = 0, i.e. a discretionary open-market sale, not a plan trade; 16,993 shares held after.** https://www.sec.gov/Archives/edgar/data/771497/000122520826006611/doc4.xml
22. SEC Form 4 — Raul J. Valentin (EVP & CHRO), filed 2026-07-17 — **1,639 shares sold 2026-07-16 at $48.00 under a Rule 10b5-1 plan adopted 2026-04-15; 49,036 held after.** https://www.sec.gov/Archives/edgar/data/771497/000122520826006655/doc4.xml
23. SEC Form 4 — David M. Orr (EVP & CFO), filed 2026-07-06 — **539 shares disposed 2026-07-01 at $44.54 under transaction code F (tax withholding), not an open-market sale; 36,034 held after.** https://www.sec.gov/Archives/edgar/data/771497/000122520826006482/doc4.xml
24. SEC EDGAR — ABM Form 10-Q for the quarter ended 2026-04-30 — **$89.0M of buyback authorisation remaining; 2.13M shares repurchased in H1 FY26 at an average $44.17; term loan $821.9M, revolver $1,045.0M, net long-term debt $1,821.6M, $518.9M borrowing capacity; covenants (5.00x total net leverage, 4.00x secured, 1.50x interest coverage) in compliance; self-insured claims reserves $679.0M with no prior-year adjustment required in the H1 interim review; goodwill $2,738.4M including $146.0M from WGNSTAR, no impairment; litigation accrual $8.3M, reasonably-possible range $0–$15.1M, no material legal proceedings; WGNSTAR funded by a $255.0M incremental term loan.** https://www.sec.gov/Archives/edgar/data/771497/000077149726000007/abm-20260430.htm
25. SEC EDGAR — ABM Form 10-Q for the quarter ended 2026-01-31 — **Q1 FY26 buyback of 2.07M shares at an average $44.13 for $91.1M; $92.0M authorisation remaining at 31 Jan 2026; the Sep-2025 $150.0M authorisation expansion.** https://www.sec.gov/Archives/edgar/data/771497/000077149726000001/abm-20260131.htm
26. Seeking Alpha / ABM — WGNSTAR acquisition — **completed 2026-02-04, ~$275M cash, semiconductor and high-technology technical services; modestly dilutive to FY26 adjusted EPS on intangible amortisation and interest, guided $0.05–$0.07 accretive in FY27; new CIO and Chief Strategy Officer roles announced alongside; FY26 EPS guidance of $3.85–$4.15 maintained.** https://seekingalpha.com/news/4562815-abm-industries-maintains-2026-eps-guidance-of-3_85-4_15-as-wgnstar-acquisition-strengthens
27. Aramark Q3 FY2026 (peer, reported 2026-08-11) — **adjusted EPS $0.52 vs $0.48 consensus, revenue $5.1B beating by 3.66%, organic revenue +9%, ~98% client retention, double-digit operating income growth in FSS US and FSS International, outlook raised, new multi-year data-centre/colocation Nexus engagement; shares +8.22% to $60.29.** https://www.investing.com/news/company-news/aramark-q3-fy2026-slides-revenue-outlook-raised-on-nexus-momentum-93CH-4851976
28. EMCOR Q2 2026 and Comfort Systems Q2 2026 (peers, reported late July 2026) — **EMCOR revenue +20% to $5.15B, record profitability, RPO $17.1B (+44% YoY, ~95% organic), guidance raised, stock from ~$672 to ~$828; Comfort Systems first >$3B revenue quarter and Hunt Electric acquisition; data-centre and AI-infrastructure investment named as the driver.** https://www.fool.com/earnings/call-transcripts/2026/07/30/emcor-eme-q2-2026-earnings-call-transcript/
29. US office market Q1–Q2 2026 (Newmark / CBRE / JLL / Savills) — **leasing at a new post-pandemic high in Q2 2026, +27% versus the trailing 5-year average; availability 23.1% in Q1 2026 versus 24.8% a year earlier with 88% of markets improving; overall vacancy 18.6%, prime vacancy down 80bp to 12.7%; recovery concentrated in Manhattan and San Francisco while Chicago, Houston and DC lag by 35–40%.** https://www.nmrk.com/insights/market-report/1q26-u-s-office-market-conditions-trends
30. TSA passenger throughput 2026 — **record ~18.7M travellers projected for the 2026 Independence Day window; multiple all-time single-day screening records through summer 2026.** https://www.tsa.gov/sites/default/files/foia-readingroom/tsa-throughput-data-to-august-9-2026-to-august-15-2026.pdf
31. Investing.com — "ABM Q1 2026 slides: revenue beats offset by margin pressure", 2026-03-10 — **Q1 FY26 adjusted EPS $0.83 vs $0.87 consensus, revenue $2.2B beat, +6.1% total / +5.5% organic growth; Technical Solutions margin below expectations on project timing and mix; FY26 guidance of $3.85–$4.15 maintained; stock fell as much as 9.14% intraday to $39.33.** https://www.investing.com/news/company-news/abm-q1-2026-slides-revenue-beats-offset-by-margin-pressure-93CH-4552358
32. Investing.com — "Why is ABM Industries stock ripping 7% higher today?", 2026-06-05 — **the Q2 FY26 reaction: +7.4% mid-day, gap from ~$41.74 to a high of $43.39, settling near $42.54.** https://www.investing.com/news/stock-market-news/why-is-abm-industries-stock-ripping-7-higher-today-93CH-4728941
33. Analyst actions (TipRanks "The Fly" / MarketBeat) — **Baird (Andrew Wittmann) raised its ABM price target to $48 from $45, Neutral; Truist lowered to $45 from $47, Hold.** https://www.tipranks.com/news/the-fly/abm-price-target-lowered-to-48-from-49-at-baird
34. TipRanks — ABM stock investors — **retail investor sentiment "Very Negative"; fewer than 0.1% of TipRanks retail investors hold ABM; 1.5% changed their holding in 7 days and 10.7% in 30 days; average holder age 35–55.** https://www.tipranks.com/stocks/abm/stock-investors
35. ABM — "ABM and LaGuardia Gateway Partners Launch Autonomous Robotics Pilot at Terminal B", GlobeNewswire, 2026-07-28 — **autonomous inspection quadruped with Skild.ai and autonomous scrubbers/vacuums with CenoBots at LaGuardia Terminal B.** https://www.globenewswire.com/news-release/2026/07/28/3334377/799/en/ABM-and-LaGuardia-Gateway-Partners-Launch-Autonomous-Robotics-Pilot-at-Terminal-B-Setting-a-New-Standard-for-Airport-Guest-Experience.html
36. Benzinga — "ABM Rides AI Data Center Boom To Fastest Growth In Nearly Four Years", 2026-06-05 — **Technical Solutions revenue +27% on battery storage, AI infrastructure and microgrid demand; microgrid win with a major big-box retailer; management describes a multi-year growth cycle with data-centre construction expanding at a double-digit pace globally; watch-item on rising fuel costs for airline clients.** https://www.benzinga.com/markets/earnings/26/06/53040082/abm-rides-ai-data-center-boom-to-fastest-growth-in-nearly-four-years
37. CapEdge / ShortSqueeze — ABM short interest history — **short interest rose from 2.86M to 2.90M shares over the 2025-11-28 → 2025-12-09 settlement period, 6.78% of float, 6.26 days to cover on 462.85k average volume; 2025 days-to-cover ranged 2.24–6.71.** https://capedge.com/company/771497/ABM/short-interest
38. MarketBeat — ABM short interest (second provider, `snippet_only`) — **2.51M shares short, 4.17% of float, +5.46% month-on-month, short interest ratio 4.4 days.** https://www.marketbeat.com/stocks/NYSE/ABM/short-interest
39. ABM — "ABM Reports Fiscal First Quarter 2026 Results and Reaffirms Fiscal 2026 Outlook", GlobeNewswire, 2026-03-10 — **confirms the Q1 FY26 report date and time (BMO, 8:30 AM ET call) used to date the −4.62% realised reaction.** https://www.globenewswire.com/news-release/2026/03/10/3252596/799/en/abm-reports-fiscal-first-quarter-2026-results-and-reaffirms-fiscal-2026-outlook.html
40. ABM — "ABM to Announce First Quarter 2025 Financial Results" — **confirms the Q1 FY25 report date of Wednesday 12 March 2025, before market open, 8:30 AM ET call, used to date the −8.67% realised reaction.** https://investor.abm.com/news-releases/news-release-details/abm-announce-first-quarter-2025-financial-results

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such. Every company-specific figure above is either sourced to a URL or explicitly marked unavailable; figures labelled "derived" are my own arithmetic on sourced inputs and are identified as such at the point of use.*
