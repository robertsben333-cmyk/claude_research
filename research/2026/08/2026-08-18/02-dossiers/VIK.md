# VIK — Viking Holdings Ltd

**Event confirmed: YES.** Viking's own IR press release states results are released **before the US market opens on Wednesday, 19 August 2026**, with the call at **08:00 ET** [1].

**What this print is about.** Viking is not a normal earnings event because the quarter is already effectively sold: as of 3 May 2026 the company had **92% of 2026 Capacity PCDs booked** against **$6,225M of advance bookings** [4][5]. Q2 revenue and EPS are therefore close to arithmetic, and the historical evidence is that Viking "rarely misses Wall Street's revenue estimates" [23]. What is *not* pre-determined is (a) the **2027 season booking update as of early August 2026** — the direct analogue to last year's "55% of 2026 sold / $3,883M / $866 per PCD" disclosure [12] — set against a **15% increase in 2027 core-product capacity** [4][16]; and (b) how management characterises the **record-low European river water levels** that have disrupted Rhine and Danube sailings through July and August 2026 [24][25][26][27], a Q3 event that sits entirely outside the Q2 numbers and lands squarely on Viking as the world's largest river operator. The stock arrives at the print having fallen **7.65% on Friday 14 August** on a weak US July retail-sales print [8][9][28] and **6.2% over ten sessions** (my calculation from daily closes [3]) — a setup that in each of the last three quarters preceded an *up* move.

**A note on the triage hint.** The triage rationale framed this as a "booking-curve/capacity-growth debate not fully consensus-priced." I think that is directionally right but incomplete: the more differentiated, dateable, and under-discussed variable I found is the **European river low-water crisis**, which is Viking-specific in a way the booking-curve debate is not. I have weighted it accordingly.

---

## 1. Event & anchors

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Event date | 2026-08-19 | — | Company IR [1] |
| Session | **bmo** (release before open; call 08:00 ET) | — | Company IR [1] |
| Fiscal period | Q2 2026 (calendar Apr–Jun) | — | Company IR [1] |
| Date changed / pre-announced? | No. Scheduling PR only; no 6-K pre-release found | — | SEC filing list [20] |
| Spot | **$99.86** | 2026-08-17 20:00:02Z (16:00 EDT close) | Yahoo chart API [3]; corroborated by stockanalysis.com [2] |
| Prior session | $97.99 (−7.65%) on 2026-08-14 | 2026-08-14 | [3], [9] |
| Market cap | **$44.55B** (446.16M shares out) | 2026-08-17 | stockanalysis.com [2] |
| Trailing P/E | 37.2x | 2026-08-17 | stockanalysis.com [2] |
| Beta | 1.50 | 2026-08-17 | stockanalysis.com [2] |
| 52-week range | $56.06 – $110.09 | 2026-08-17 | stockanalysis.com [2] |
| **Event-implied move (ATM straddle, 21-Aug expiry — first expiry after report)** | **7.6% of spot** ($100 strike: call $3.70 + put $3.88 = $7.58) | 2026-08-17 20:00Z | My calculation from Yahoo option chain [30] |
| De-vol'd single-day event move (my inference) | **≈6.5%** after stripping 3 non-event days at ~45% diffusive vol | 2026-08-17 | My calculation [30] |
| Published implied move (cross-check) | 10.41% "monthly" — this maps to the **September** expiry (Sept ATM straddle = 10.63%), **not** the event-specific move | 2026-08-17 (T−2) | OptionSlam [7]; `snippet_only: false` but premium-gated table |
| IV (30-day) | 44.78% | last session (no explicit stamp on page) | Barchart [19] · `snippet_only: true` |
| **IV rank** | **62.50%** (IV percentile 67%) | last session | Barchart [19] · `snippet_only: true` |
| HV30 | 34.16% | last session | Barchart [19] |
| Realised vol (my calc) | RV10 46.7% · RV20 38.3% · RV60 33.3% · RV252 38.9% | 2026-08-17 | My calculation [3] |

### Historical one-day realised earnings reactions (close-to-close on report day)

All eight prints since the May 2024 IPO. Computed by me from Yahoo daily OHLC [3]; the May-2026 figure cross-checks against OptionSlam's independently published 5.53% [7] and Market Chameleon's "+5.5% … to close at 86.72" [6], validating the method.

| Report date | Quarter | Session | Prev close | Open (gap) | Close | **1-day move** |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-08-22 | Q2 2024 | bmo | 36.44 | 34.70 (−4.77%) | 33.22 | **−8.84%** |
| 2024-11-19 | Q3 2024 | bmo | 45.39 | 43.53 (−4.10%) | 45.09 | **−0.66%** |
| 2025-03-11 | Q4 2024 | bmo | 42.74 | 40.95 (−4.19%) | 40.15 | **−6.06%** |
| 2025-05-20 | Q1 2025 | bmo | 47.08 | 44.10 (−6.33%) | 44.73 | **−4.99%** |
| 2025-08-19 | Q2 2025 | bmo | 60.20 | 56.45 (−6.23%) | 59.22 | **−1.63%** |
| 2025-11-19 | Q3 2025 | bmo | 58.27 | 58.13 (−0.24%) | 61.21 | **+5.05%** |
| 2026-03-03 | Q4 2025 | bmo | 74.04 | 72.61 (−1.93%) | 76.42 | **+3.21%** |
| 2026-05-14 | Q1 2026 | bmo | 82.17 | 89.90 (+9.41%) | 86.72 | **+5.54%** |

- **Mean absolute: 4.50% · Median absolute: 5.02% · Max absolute: 8.84%**
- **Up/down pattern: 3 up / 5 down**, but strictly clustered — the **first five prints were all negative, the last three all positive**. The regime flipped at Q3 2025.
- **Intraday reversal is the dominant micro-pattern.** Seven of eight prints gapped in one direction and then reverted materially: five of the eight gapped **down** and three of those closed far better than the gap (2024-11-19: −4.10% → −0.66%; 2025-08-19: −6.23% → −1.63%; 2026-03-03: −1.93% → +3.21%). The one large up-gap (2026-05-14, +9.41%) **faded to +5.54%**. Opening prints have consistently been a poor guide to the close.
- **Implied is rich to realised.** The ~6.5–7.6% event pricing sits ~1.4–1.7x the 4.50% mean absolute realised move. Options have over-priced this event in each of the last two quarters: implied 13.19% vs actual 5.53% in May 2026 [7]; implied 6.05% vs actual 3.21% in March 2026 [17].

### Run-up into the print vs the reaction (my calculation, [3])

| Report date | 5-day run-up into print | Reaction |
| --- | --- | --- |
| 2024-08-22 | +6.52% | −8.84% |
| 2024-11-19 | +2.14% | −0.66% |
| 2025-03-11 | −9.96% | −6.06% |
| 2025-05-20 | +3.31% | −4.99% |
| 2025-08-19 | +4.15% | −1.63% |
| 2025-11-19 | −2.96% | **+5.05%** |
| 2026-03-03 | −3.14% | **+3.21%** |
| 2026-05-14 | −4.51% | **+5.54%** |
| **2026-08-19 (now)** | **−3.80%** (10-day: −6.21%) | ? |

**My inference:** 4 of 4 prints preceded by a positive 5-day run-up fell; 3 of 4 preceded by a negative run-up rose (the exception being March 2025, where the run-up was an outlier −9.96%). The current −3.80% run-up sits almost exactly on top of the three most recent, all of which produced +3% to +5.5% reactions. This is an n=8 pattern with obvious overfitting risk and I treat it as a tilt, not a thesis.

---

## 2. The bar

**Consensus (note the dispersion across vendors — none of these are the company's own guidance):**

| Metric | Estimate | Source |
| --- | --- | --- |
| Adjusted EPS | **$1.25** (+26.3% YoY) | Zacks via Yahoo Finance [10] |
| Adjusted EPS (alt) | $1.27 | TipRanks [22] · `snippet_only: true` |
| Revenue | **$2.13B** (+13% YoY) | Zacks via Yahoo Finance [10] |
| Revenue (alt) | $2.17B / $2.14B / "+14.1% YoY" | TipRanks [22] / TIKR [9] / StockStory [23] |
| Analyst count | 20–21 (16 buy, 2 outperform, 2 hold, 1 sell); 25 per MarketScreener | TIKR [9]; stockanalysis [2]; MarketScreener [21] |
| Mean price target | **$109.15** (+9.3% vs spot); alt $101.22 (MarketScreener), $107.29 (TradingKey) | [2][9]; [21]; [8] |

**Comparison base — Q2 2025 actuals** [12]: revenue $1,880.4M (+18.5%), adjusted EBITDA $632.9M (+28.5%), adjusted net income $439.0M, **adjusted EPS $0.99**, occupancy 95.6%, net yield $607 (+8.0%), capacity PCDs 2,131,907 (+8.8%).

**Consensus for the operating line items** (Zacks, [10]) — this is the level at which the print is actually judged:

| Metric | Q2 2026 estimate | Implied YoY |
| --- | --- | --- |
| Capacity PCDs | 2,293,559 | +7.6% |
| PCDs | 2,199,290 | +7.9% |
| Occupancy | 95.9% | +0.3 pts |
| Net yield | $638.03 | +5.1% |
| Cruise & land revenue | $1.97B | +12.5% |
| Onboard & other revenue | $147.23M | +17.6% |
| Viking Ocean net yield | $631.74 | +14.6% |
| Viking River net yield | $640.87 | +5.6% |

**Revisions.** Mildly positive and, more importantly, *stable*: Q2 EPS consensus revised **+0.2% over 30 days** [10]; next-quarter revenue estimate revised **+0.23% over 3 months** (ChartMill, July 2026 [11] · `snippet_only: true`); StockStory notes analysts "have generally reconfirmed their estimates over the last 30 days" [23]. **60-day and 90-day EPS revision figures: unavailable.**

**Guidance setup.** Viking does **not** issue formal quarterly EPS/revenue guidance. What it gives instead is (i) the advance-bookings table for the current and following season, and (ii) qualitative targets. The standing qualitative target is **mid-single-digit net yield growth for Core Products, conditional on stable macro** [16]. Capacity guidance: **+7% Core Product operating capacity in 2026** (cut from an original ~10% river growth after eight Longship delivery delays [13]) and **+15% in 2027** [16].

**Whisper number: unavailable** — I could not find a credibly published whisper for VIK.

**What the company has to deliver just to hold the stock flat (my inference).** Three things simultaneously: (1) adjusted EPS at or modestly above $1.25 — a low bar given the pre-sold revenue and a 12.46% average beat over the last two quarters [22]; (2) a 2027 booking update that shows **at least ~55% of 2027 capacity sold** with per-PCD pricing still up year-over-year, which on 15% more capacity requires ~15% more PCDs sold than the same point last year; and (3) a Q3 river-disruption commentary that is framed as an operational inconvenience with contained cost rather than a yield or cancellation event. Miss on (3) alone and I think the print trades down despite (1) and (2).

---

## 3. The one metric that matters

**The 2027 season advance-booking disclosure as of early August 2026 — specifically the percentage of 2027 Capacity PCDs sold and advance bookings per PCD — read against 15% capacity growth.** Secondarily and nearly as important this quarter: **management's quantification of the European river low-water impact on Q3.**

**Why this and not EPS.** Viking's revenue for the reported quarter is locked long before the quarter starts (92% of 2026 sold as of 3 May [4]), so the Q2 P&L carries almost no information. Every incremental piece of information in the release is forward-looking, and the disclosure the market re-rates on is the booking table. The 14 August Barchart headline on this name is literally *"Viking Holdings Reports Earnings While Everyone Waits to Hear What Bookings Actually Look Like"* [17].

**What the market expects, and how I know:**

| Season | Disclosure point | % capacity sold | Advance bookings | Per PCD | vs prior year |
| --- | --- | --- | --- | --- | --- |
| 2026 | as of 2025-08-10 [12] | **55%** | $3,883M | $866 (+4%) | +13% |
| 2026 | as of 2026-02-15 [13] | 86% | $5,960M | $859 (+6%) | +13% |
| 2026 | as of 2026-05-03 [4][5] | 92% | $6,225M | $842 | +13% |
| **2027** | as of 2026-05-03 [4][5] | **38%** | $3,403M | **$986** | **+31%** |
| **2027** | **as of ~2026-08-09 (this print)** | **base rate ≈55%** | **?** | **?** | **?** |

The direct analogue is the 55% figure. Because 2027 core capacity is **+15%** [16], holding 55% booked requires selling ~15% more passenger-cruise-days than a year ago. The pricing signal to watch is per-PCD: 2027 stood at **$986** at the May checkpoint versus **$842** for the 2026 season at the same reporting date, and management explicitly flagged that this partly reflects **mix** — high-yield Egypt and India itineraries sold earlier in the cycle — rather than pure rate [16]. CEO Leah Talactac's May framing: *"The season is already 38% booked with the capacity for our core product increasing by 15% over 2026"* [16].

**Why the river commentary is the swing factor this specific quarter.** Europe's rivers hit record lows in July–August 2026. Hungary's Paks plant recorded the Danube's **lowest-ever level on 27 July**; the Romanian Danube fell to a **30-year low**; the Rhine, Main and Upper Danube ran below seasonal norms [27]. **Viking itself issued a 30 July update describing water levels on sections of the Rhine and Danube as "exceptionally low,"** warning of itinerary modifications and ship swaps [25]; the **Viking Ullur ran aground on a Danube sandbank** [25]; Forbes on 11 August named Viking River Cruises among the affected operators, with ship swaps, coach transfers around unnavigable stretches, and hotel nights the standard remediation [24]. Viking's mitigation model — identical sister ships positioned either side of a shallow bottleneck with guests bussed between them [25] — means it avoids outright cancellation, so the hit is **cost and guest-goodwill, not lost revenue**. But it lands in **Q3, Viking's largest quarter and the heart of the April–October core river season** [29], and it is not in any consensus line item I could source. I could find **no published estimate of the dollar impact** — see coverage gaps.

---

## 4. Fundamentals — what changed, what is at stake

**Scale and mix.** FY2025 revenue **$6,501.4M (+21.9%)**, adjusted EBITDA **$1,872.1M (+38.8%)**, adjusted net income **$1,165.1M (+43.9%)**, adjusted EPS **$2.61**, net yield **$583 (+7.4%)**, occupancy 95.4%, capacity PCDs 7,709,620 [13]. Segment FY2025: **Viking River** net yield $578, adjusted gross margin $1,897.9M; **Viking Ocean** net yield $572, adjusted gross margin $1,985.6M [13]. The two core segments are near-equal contributors — which is exactly why a river-specific shock matters at the group level.

**Most recent quarter (Q1 2026, reported 14 May)** [4][5]: revenue **$1,053.7M (+17.5%)**, adjusted EBITDA **$104.8M (+43.9%)**, net loss **$54.2M** (vs −$105.5M), diluted EPS **−$0.12** / adjusted **−$0.11**, net yield **$596 (+9.5%)**, occupancy **94.7%**, capacity PCDs 1,270,701 (+6.6%), 92 vessels operated, 119,757 passengers. Segment detail [16]: **River** capacity PCDs −8.4% (deliberate shift to high-yield Egypt/Vietnam itineraries) but net yield **+28.3% to $761**; **Ocean** capacity PCDs +10%, occupancy 95%, net yield **+5.6% to $527**. Management cautioned Q1 river data has little predictive value given the April–October season [29].

**Margin trajectory.** Q1 2026 operating margin improved to **+1.1%** from **−1.0%** a year earlier [14]. FY2025 adjusted EBITDA margin ≈28.8% on FY2025 revenue [13] (my calculation). The FY2025 EBITDA growth rate (+38.8%) ran roughly 1.8x the revenue growth rate (+21.9%) [13] — operating leverage on a fixed-cost fleet, which is the core of the bull case and also what makes any yield disappointment amplified.

**Cash flow and balance sheet.** FY2025 operating cash flow **$2,560.3M**, capex **$1,026.9M**, implying **~$1,533M free cash flow** [13]. At 31 Mar 2026: cash **$4.0B**, undrawn revolver **$1.0B**, deferred revenue **$5.4B** (up from $4.6B at 31 Dec 2025 [13]), net debt **$1,941.9M**, **net leverage 1.0x** — down from 1.1x at year-end and 2.4x at end-2024 [4][13][18]. The deleveraging over 18 months is one of the cleanest facts in the file. My inference: at $44.55B market cap plus $1.94B net debt, EV ≈ **$46.5B**, or roughly **24x** TTM adjusted EBITDA of ~$1.90B — full, but not indefensible against ~30%+ EBITDA growth.

**What is at stake on capital intensity.** Committed ship capex is **~$1.9B in 2026 and ~$1.0B in 2027**, with **$4,418.4M of total future shipbuilding commitments** running to the early 2030s [18]. The orderbook is **20 additional river ships by 2028, nine ocean ships by 2031, two expedition ships by 2031** [15]. Capacity growth is contractually committed; demand is not. That asymmetry is the structural bear case.

**Buyback / dividend: none.** VIK pays **no dividend** (TTM payout $0.00 as of 27 Jul 2026) [31], and management on the Q1 call named reinvestment in the orderbook as the top capital-allocation priority, with **no buyback discussed** [16][29]. There is no capital-return lever to defend the stock into a soft print.

**Customer concentration:** not applicable — direct-to-consumer, ~120k passengers in a seasonally weak quarter [4].

**Cost exposure.** Fuel is only **~4% of adjusted gross margin (2025)**, river fuel is largely on fixed-price contracts locked in 2025, and the ocean fleet is fuel-efficient with closed-loop scrubbers [16][32]. **EUR 500M is hedged for 2026 at ~$1.10/EUR**, structured to offset euro-denominated loans so FX does not flow to adjusted EPS [32]. Viking is materially *less* fuel- and FX-exposed than the mass-market operators — a point UBS has cited in reiterating Buy [32].

**What changed since the last print:** (i) CEO transition executed — **Leah Talactac** from President/CFO to **CEO**, **Torstein Hagen** to **Executive Chairman**, **Linh Banh** to **CFO**, all announced alongside Q1 on 14 May [4][33]; (ii) **2028–2029 ocean bookings opened 6 August** — 700+ departures, 80 voyages, 301 ports, 84 countries [15]; (iii) fleet additions **Viking Ptah** (Nile, 82 guests) and **Viking Dagur** (Europe) delivered [15]; (iv) the **European low-water event** [24][25][26][27].

---

## 5. Positioning & options

*All as of the 2026-08-17 close unless noted.*

- **Event-implied move:** ATM (K=$100) straddle expiring **2026-08-21** — the first expiry after the report — priced at **$7.58 (7.59% of the $99.86 spot)** on same-session traded prices (call volume 91, put volume 216). My de-vol'd estimate of the pure single-day event move is **≈6.5%**. Source: my calculation from the Yahoo option chain [30].
- **Term structure is steeply inverted.** Solving Black-Scholes off traded marks: **~90% ATM IV for the 21-Aug expiry vs ~45% for 18-Sep** [30] (my calculation). Barchart's 30-day IV of **44.78%** [19] independently corroborates the ~45% back-month level. This is a textbook event-vol hump; the front expiry is almost entirely earnings premium.
- **Skew is meaningfully to the downside.** Front expiry: the $90 put trades at **104.9% IV** and the $85 put at **107.4%**, against **96.0%** for the $110 call [30]. September: $90 put **48.4%** vs $110 call **42.5%** — roughly **6 vol points** of put-over-call [30] (my calculation). Downside protection is being bid, not upside.
- **Put/call:** Barchart shows **OI put/call 1.58** (21,509 puts vs 13,632 calls) and **volume put/call 1.43** (934 vs 652) [19]. My own front-expiry volume tally from the chain gives put/call **1.66** (837 vs 503) [30]. All three readings agree: put-skewed.
- **Unusual options activity:** front-expiry downside put volume clustered at $90 (100), $85 (142) and $80 (113) contracts against near-zero prior open interest [30]. That is small in absolute terms but is fresh, one-directional, and far out of the money for a 4-day option — consistent with tail hedging into the print rather than directional speculation. **No third-party UOA scanner data obtained.**
- **Short interest:** **conflicting sources.** Fintel reports **7,324,491 shares short, 3.54% of float, 2.75 days to cover** (NYSE data, settlement date not shown on the free page) [34]. A second source reports **7.5M shares, 2.4% of float, 3.4 days to cover, down 15.7% from the prior period** [35] (`snippet_only: true`). Either way, this is **not a crowded short** — low single-digit percent of float and under 3.5 days to cover.
- **Borrow fee / utilisation: unavailable** (Fintel gates it behind premium) [34].
- **Run-up / drawdown into the print:** **−3.80% over 5 sessions, −6.21% over 10**, driven by a **−7.65% day on 14 August** on **5.29M shares** versus a 30-day average of **~2.08M** — the heaviest volume day in the window [3] (my calculation). The stock closed **7.8% below its 52-week high of $110.09** [2][3]. Longer-horizon momentum remains strongly positive: **+19.3% over 63 sessions, +32.8% over 126, +66.4% over 252, +39.8% YTD** [3].
- **How crowded is the trade?** Institutional ownership is reported at **98.84% across 512 filers** [36] (`snippet_only: true`), with **FMR at 5.3% (16.99M shares, as of 30 Jun 2026, filed 6 Aug)** [37] and **CPPIB down to 3.5% (11.24M shares)** [37]. My read: the *long* side is the crowded side. Pre-IPO sponsor overhang has largely cleared — TPG fully exited in the May 2025 secondary at $44.20 and CPPIB has been steadily reducing [38][39] — which removes a historic supply drag but also means the remaining register is conviction long-only money with limited incremental buying power at 37x.

---

## 6. Sentiment & alt-data

**Analyst ratings and price-target drift — uniformly positive, and that is itself a risk.** Rating mix per TIKR as of 14 August: **16 buy, 2 outperform, 2 hold, 1 sell** among 20 analysts [9]; stockanalysis shows a "Strong Buy" consensus with a **$109.15** mean target [2]. Recent target raises, all in the 30 days before the print:

| Firm | Action | Date | Source |
| --- | --- | --- | --- |
| Goldman Sachs | $108 → **$120**, Buy | 2026-07-31 | [40] |
| Citi (James Hardiman) | $101 → **$113**, Buy | Aug 2026 | [41] |
| Stifel | $105 → **$125** | Aug 2026 | [41] |
| Morgan Stanley | $86 → **$93**, **Equal Weight** | Aug 2026 | [40] |
| Barclays | $88 → **$93**, **Equal Weight** | Aug 2026 | [40] |
| UBS (Robin Farley) | Buy reiterated, **$100** target, citing fuel hedging | 2026 | [32][41] |
| J.P. Morgan | Buy maintained | 2026-08-13 | [41] |

**My inference:** the dispersion matters more than the mean. Goldman/Citi/Stifel sit at $113–$125 while **Morgan Stanley and Barclays are Equal Weight with $93 targets — below the current $99.86 spot**. TIKR's own note observed analysts "stayed put while the price moved," treating the 14 August drop as a reset rather than a change of view [9]. That is a bull-crowded book with a soft floor: the stock is already trading through two major banks' targets, and MarketScreener's alternative $101.22 mean implies barely 1% upside [21].

**Retail / social tone: substantially unavailable.** Stocktwits' public sentiment page returned **N/A across all timeframes** without login [42], so I have **no 7/14/30-day retail trend**. The only sourced datapoint is from **August 2025** — "extremely bullish" with "extremely high" chatter [43] — which is a year stale and I do not treat it as evidence for this print. StockInvest.us rated VIK **Hold/Accumulate with a technical score of 0.00** on data through 13 August 2026 [44].

**Alt-data proxies — thin, and I want to be explicit that most of what follows is industry-level, not Viking-level:**
- **Travel-advisor survey data (positive):** Virtuoso reported **2026 sales +21% with cruise +22%**; in its July survey of ~800 advisors, **63% cited premium and luxury ocean cruising** as what clients want more of; bookings of **$50K+ for sailings 1–2 years out are +49% in 2026 vs 2025** [45]. Viking's segment is where the money is going.
- **Brand consideration (positive):** in a Cruiseline.com/Shipmate survey, **Viking was the top river brand under consideration at 62.3%**, and **92.8% of respondents had at least one 2026-or-later voyage booked** [46].
- **Booking-window behaviour (positive):** ANZ travellers reported booking Viking **380 days in advance** [46].
- **Google Trends:** **no hard index values obtained** — see coverage gaps.
- **App ranks, web traffic, job postings, review scores:** **none sourced.**
- **Negative alt-data (the real one):** the Forbes / Cruise Critic / Travel Weekly / CNN reporting on record-low Rhine and Danube levels is itself high-quality contemporaneous alt-data about Q3 operations, and it points the wrong way [24][25][26][27].

---

## 7. Forensics

- **Insider transactions — all sales, but all mechanical.** The verified Form 4s are **Anton Hofmann (EVP, Group Operations)**: 94,276 shares sold 15 June 2026 at weighted averages of $96.04 (1,606) and $95.32 (92,670), ~$8.99M, **explicitly pursuant to a Rule 10b5-1 plan adopted 9 March 2026**, leaving 292,819 shares including 109,904 unvested RSUs [47]. Additional Hofmann sales: **5,956 shares on 10 June 2026 at $91.00**, same plan [48]; a separate 185,283-share sale under a trading plan [49]; and **4,610 shares sold purely to cover RSU tax withholding** [50], plus a CEO sale to cover taxes [51]. **Quiver reports 27 insider transactions over the trailing six months, 100% sales, zero purchases** [8] (`snippet_only: true`).
  - **My read:** headline-ugly, substantively benign. Every transaction I could verify individually is either 10b5-1 or tax withholding, the plan was adopted in **March**, well ahead of the Q2 window, and there is **no verified discretionary open-market selling and no Hagen-family selling** — one source explicitly notes **Karine Hagen made no insider transaction over the trailing 18 months** [52]. I do not treat this as a signal.
- **Form 144 cadence:** multiple filings clustered **19 May – 15 June 2026** [20], consistent with the Hofmann plan schedule rather than opportunistic distribution. Nothing filed since mid-June.
- **Executive changes — the significant one.** The **CEO transition was announced simultaneously with Q1 results on 14 May 2026**: founder **Torstein Hagen** (CEO for ~three decades) moved to **Executive Chairman**; **Leah Talactac** (President & CFO, who led the 2024 IPO) became **CEO**; **Linh Banh** (EVP Finance) became **CFO** [4][33]. Bundling a founder-CEO transition into an earnings release is the kind of thing that normally reads as burying news — but the stock **rose 5.54% that day** [3], and there is no evidence of an involuntary departure. **This will be Talactac's first Q2 print as CEO and Banh's second as CFO.** My inference: modest incremental risk of a communication misstep on a call where the river question is unavoidable, and no established track record of how this pair handles a bad-news question.
- **Auditor / restatement issues:** **none found.**
- **8-K / 6-K cadence:** Viking is a foreign private issuer filing 6-Ks. 2026 filings to date: **3 March** (Q4/FY2025), **31 March**, **14 May** (two, including Q1 results), **15 May** [20]. That is a normal, sparse cadence with **no off-cycle 6-K since 15 May** — i.e. **no pre-announcement, no guidance revision, and no 8-K-equivalent disclosure of the river disruption**. Given the severity of the low-water event, management's choice *not* to pre-announce is itself mildly reassuring on magnitude, though foreign private issuers face a lower continuous-disclosure bar than domestic filers, so I would not lean hard on it.
- **Filing-language / tone shifts:** I did not obtain a diff of the risk-factor or MD&A language between the FY2025 and Q1 2026 filings. **Unassessed** — see coverage gaps.
- **13G activity:** **FMR LLC filed a new 13G on 6 August 2026** disclosing **5.3% (16,993,566 shares) as of 30 June** [37]; **CPPIB filed 13G/A Amendment No. 5 on 14 August** showing **3.5% (11,244,744 shares)** [37][20]. Fidelity building to a 5%+ position while the last sponsor trims is, on my read, a mildly constructive rotation of the register.

---

## 8. Macro & peer read-through

**Sector/factor regime.** The 14 August drawdown was macro, not idiosyncratic: **US July retail sales fell 0.6% m/m** against expectations of a modest gain, and the S&P 500 slipped from a record high, hitting consumer-facing names [9][28]. Year-over-year retail sales were still **+5.2%** [28], and Deloitte's consumer pulse shows discretionary spending intent cooling with the sharpest pullback in **big-ticket goods** — accessories, jewellery, home décor, furniture — rather than in experiences [28]. **My inference:** the macro tape sold Viking as a consumer-discretionary beta name (beta 1.50 [2]), but Viking's actual customer — affluent, 55+, booking 12+ months ahead, having already paid a deposit — has close to zero exposure to a one-month retail-sales wobble. The 7.65% drawdown therefore looks more like a de-risking than a re-rating, which is the single best thing about the entry setup.

**Rate / FX / commodity sensitivity.** Low relative to peers. Fuel ≈**4% of adjusted gross margin**, river fuel largely fixed-price for 2026, ocean fleet fuel-efficient with scrubbers [16][32]. **EUR 500M hedged for 2026 at ~$1.10**, structured against euro loans so FX does not reach adjusted EPS [32]. Net leverage **1.0x** with **$4.0B cash** means rate sensitivity on the balance sheet is modest and cash interest income is a tailwind [4]. The Fed had cut 175bp cumulatively since September 2024 to 3.50–3.75% by December 2025 [28].

**Peers who already reported this cycle — a genuinely split tape:**

| Peer | Date | Result | Stock reaction |
| --- | --- | --- | --- |
| **Carnival (CCL)** | 2026-06-23 | Record Q2: revenue $6.7B, net income $569M, **$100M above own March guidance**; **93% of H2 capacity booked at record prices**; **record customer deposits $9.0B (+$450M)**; **2027 European bookings up mid-teens % at higher prices**; flagged Middle East geopolitical drag on some Med deployments but called it transitory | Fell ~6% on the day [54] |
| **Royal Caribbean (RCL)** | 2026-07-28 | **Beat and raised.** Adjusted EPS **$4.21** vs ~$4.02 consensus (fifth straight beat); net yields **+1.9%**; FY guidance raised to **$17.73–$17.87** (~14% growth); FY revenue +9% | **+5.7%** [53] |
| **Norwegian (NCLH)** | 2026-07-30 | Beat Q2 (adj EPS $0.48, EBITDA $666M, revenue +4.9% to $2.6B, all above own guidance) but **cut FY**: net yield now **~−5%**, adjusted EPS **~$1.50**, EBITDA ~$2.5B; Q3 net yield guided **−8.9%**. Blamed Middle East disruption, higher fuel, **softer European summer demand**, and self-described **"self-inflicted marketing and revenue management issues"** | Dropped [55][56] |

**My read-through.** Three signals, and they do not point the same way:
1. **Forward demand for premium/long-booking-window product is intact.** Carnival's record deposits and mid-teens 2027 European booking growth at higher prices [54], plus RCL's raise [53], are the closest available proxies for what Viking should say about 2027. This is the strongest single argument for the bull case.
2. **European summer 2026 was soft for someone.** NCLH's guidance cut explicitly cites softer European summer demand [55]. Viking's European exposure is overwhelmingly river, not Med ocean, and NCLH itself attributed much of the shortfall to internal execution — so I discount but do not dismiss this.
3. **Beating is not sufficient.** Carnival beat and fell 6%; NCLH beat the quarter and fell on the guide. In this sector, in this tape, the reported quarter has not been the driver — the forward statement has. That is precisely the structure of the VIK setup.

**Customer/supplier read-through.** Supply side is the live constraint: shipyard production delays already forced **eight Longship delivery reschedules**, cutting Viking's own 2026 river capacity growth from 10% to 6% [13]. A further slip would trim 2027's +15% capacity plan — mechanically bad for revenue growth, arguably good for yields.

---

## 9. Bull case / bear case / base case

**Bull case.** Viking prints adjusted EPS comfortably above $1.25 on a quarter that was 92% pre-sold [4][10], and — the part that matters — discloses 2027 at or above ~55% of capacity booked with per-PCD pricing still rising, sustaining the +31% advance-bookings trajectory shown at the May checkpoint on 15% more capacity [4][16]. Carnival's record $9.0B deposits and mid-teens 2027 European booking growth at higher prices [54] and RCL's beat-and-raise [53] say that forward demand for exactly this product is intact. Management frames the river low-water event as an operational cost absorbed through sister-ship swaps and coach transfers with no cancellations and no yield concession [24][25]. On this path the stock recovers the 14 August air pocket: the −3.80% five-day run-up matches the setup that preceded +5.05%, +3.21% and +5.54% reactions in the last three quarters [3], the implied move is rich to a 4.50% mean-absolute realised [3][7], and the balance sheet — 1.0x net leverage, $4.0B cash, $1.5B FY2025 FCF [4][13] — gives the multiple something to stand on.

**Bear case.** The stock enters at **37x trailing earnings** after **+66% in twelve months** [2][3], with the mean target only 9% above spot and **Morgan Stanley and Barclays already below spot at $93** [21][40]. Into that, management has to address a river season disrupted by the worst European water levels in three decades — Danube record lows at Paks on 27 July, a 30-year low in Romania, Viking's own 30 July "exceptionally low" advisory, and the Viking Ullur aground [24][25][27] — in Viking's largest quarter and the core of its April–October river season [29]. If the July heatwave also slowed *river bookings* in the weeks before the ~9 August measurement date, the 2027 disclosure disappoints on the very metric the print trades on. Options are positioned for this: put/call OI 1.58 [19], ~9 vol points of front-expiry put-over-call skew, and fresh downside put volume at $80–$90 [30]. There is **no buyback** to defend the tape [16][31], the orderbook commits **$4.4B** of capex regardless of demand [18], and Carnival's 6% drop on record results [54] shows that in this group a good quarter buys nothing. A first-time CEO fielding the river question badly is enough on its own.

**Base case.** Viking beats a low, pre-sold EPS bar (adjusted EPS $1.25–$1.35 against $1.25 consensus [10], given a 12.46% average beat over two quarters [22]) and reports a 2027 booking position broadly in line with the ~55% base rate at healthy per-PCD pricing [12][16]. Management acknowledges the European river disruption, quantifies it as a Q3 cost headwind rather than a demand event, and reiterates mid-single-digit yield growth [16]. The stock gaps somewhere between −4% and +6%, and — consistent with seven of eight prior prints [3] — the close is materially closer to flat than the open. **I lean modestly positive**, weighted by the run-up pattern, the pre-sold revenue base, the RCL/CCL read-through, and the fact that 7.65% of downside was already taken out on Friday for reasons that have nothing to do with Viking's customer. **I hold that lean loosely**, because the river variable is real, dateable, and genuinely two-sided, and because implied vol is pricing ~1.4x the historical realised move — the option market is not offering this cheaply.

**My preliminary read: direction_score +15, prob_up 55, conviction Med.** Reversal risk is high and separate from direction: the intraday-reversal pattern is the most robust thing in the price history, and I would not trust the opening print in either direction.

---

## 10. What would flip the consensus view

The most credible reversal is **a river-driven cut to the second-half yield outlook.** Concretely: if management on the 08:00 ET call quantifies the European low-water disruption as a **Q3 net yield headwind** — say, guiding river net yield growth below the mid-single-digit Core Product target [16], or disclosing that guest compensation and ship-swap logistics costs will compress Q3 adjusted EBITDA — then the entire premise of the stock's 66% twelve-month re-rating [3] is challenged. That premise is that Viking's booking model makes it structurally immune to the demand and disruption problems that hit NCLH [55]. A river yield cut says the immunity is to *demand* shocks, not *operational* ones, and that Viking has a recurring climate-linked exposure in its highest-margin, largest-capacity-growth segment — 20 more river ships arrive by 2028 [15]. At 37x earnings [2] with two bulge-bracket targets already below spot [40], that is worth well more than the 6.5–7.6% the options are pricing.

The mirror-image reversal, which I consider somewhat less likely but not remote: **2027 booked at 60%+ with per-PCD pricing up double digits and an explicit statement that low water cost nothing material.** That would confirm both pricing power and operational resilience simultaneously, and would likely force the Equal Weight desks at Morgan Stanley and Barclays [40] to move — the classic squeeze on a bull-crowded name where the marginal bear is a valuation bear rather than a fundamental one.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **Borrow fee / short utilisation** | Gated behind Fintel premium [34]. Without it I cannot judge whether the modest 3.54% short interest is expensive or free to carry — relevant to squeeze potential on an upside surprise. |
| **Short interest is internally inconsistent** | Fintel: 7.32M shares / 3.54% float / 2.75 DTC [34]. Second source: 7.5M / 2.4% float / 3.4 DTC [35]. Neither states a settlement date. The float denominators clearly differ. Both agree the short is small, so the disagreement is low-stakes, but I cannot state a precise figure. |
| **Whisper number** | Not found anywhere credible. Given VIK's 12.46% average two-quarter beat [22], the buyside bar is plainly above the $1.25 sell-side print, but I cannot say by how much — which is exactly the number that determines whether an EPS beat is actually a beat. |
| **60- and 90-day EPS revision breadth** | I sourced only the 30-day (+0.2% [10]) and a 3-month revenue figure (+0.23% [11]). Without the fuller revision path I cannot tell whether the Street has been quietly creeping up all summer or is flat. |
| **No dollar estimate of the river low-water impact** | This is my biggest gap and the biggest single swing factor in the dossier. I established the event is severe, ongoing, and Viking-specific [24][25][26][27], but found **no sell-side or company quantification** of the Q3 cost or yield effect. I therefore cannot size the bear case, only name it. |
| **IV rank/percentile has no explicit timestamp** | Barchart's 62.50% / 67% [19] almost certainly reflects the 17 August session (its 30-day IV of 44.78% matches my independent September-expiry calculation of ~45% [30]), but the page carries no as-of stamp. Marked `snippet_only`. |
| **Option bid/ask spreads unavailable** | The post-close chain returned zero bids and asks [30], so the 7.59% straddle is built from **last traded prices**, not mid-market. Volumes (91 calls, 216 puts at the ATM strike) confirm same-session trading, but the implied move could be off by a few tenths. |
| **Retail/social sentiment 7/14/30-day trend** | Stocktwits returned N/A without login [42]. The only sourced retail datapoint is from **August 2025** [43] and I have deliberately excluded it from my read. Per the source hierarchy this is colour rather than a load-bearing input, so the practical cost is low. |
| **Google Trends index values; app ranks; web traffic; job postings; review scores** | None obtained at the Viking-brand level. My alt-data is therefore industry survey data [45][46] rather than a real-time proxy for Viking's own booking velocity — a meaningful weakness given the whole thesis turns on booking velocity. |
| **Filing-language / tone diff between FY2025 and Q1 2026 filings** | Not performed. A risk-factor addition on climate/water navigability would have been a strong tell. |
| **Exact analyst count** | Ranges from 20 [9] to 21 [2] to 25 [21] depending on vendor, with mean targets from $101.22 to $109.15. I report the range rather than pick one. |
| **WebFetch blocked domains** | `optioncharts.io` was blocked by the environment's egress policy. Market Chameleon [6], WallStreetZen and Fintel [34] returned partial data behind paywalls. Yahoo Finance's chart and option-chain APIs, SEC EDGAR, and Viking's own IR site were all fully reachable. |

**Evidence completeness: 82/100.** Areas 1, 2, 3, 4, 5, 6, 8 and 9 are well sourced, much of it from primary company filings and directly computed market data. Area 7 (sentiment/alt-data) is the weakest at roughly half-covered, and the missing river-impact quantification is a material hole in an otherwise strong file.

---

## 12. Sources

1. [Viking IR — Viking Schedules Conference Call on Second Quarter 2026 Financial Results](https://ir.viking.com/news-events/press-releases/detail/239/viking-schedules-conference-call-on-second-quarter-2026-financial-results) — event date 2026-08-19, 08:00 ET call, release before market open, Q2 2026.
2. [stockanalysis.com — VIK overview](https://stockanalysis.com/stocks/vik/) — spot $99.86 at 2026-08-17 16:00 EDT, market cap $44.55B, 446.16M shares, P/E 37.21, beta 1.50, 52-week range, next earnings 2026-08-19, mean target $109.15.
3. Yahoo Finance chart API, `https://query1.finance.yahoo.com/v8/finance/chart/VIK?range=3y&interval=1d` — daily OHLCV used for all eight earnings-day reactions, run-up calculations, realised vol, YTD/trailing performance, volume, and the 2026-08-14 (−7.65%, 5.29M shares) and 2026-08-17 ($99.86) sessions. All derived figures are my calculations.
4. [Viking IR — Viking Announces CEO Transition and Reports First Quarter 2026 Financial Results](https://ir.viking.com/news-events/press-releases/detail/231/viking-announces-ceo-transition-and-reports-first-quarter-2026-financial-results) — Q1 2026 revenue $1,053.7M, adj EBITDA $104.8M, net loss $54.2M, EPS −$0.12/−$0.11, net yield $596, occupancy 94.7%, capacity PCDs 1,270,701, 2026/2027 advance bookings, cash $4.0B, net leverage 1.0x, deferred revenue $5.4B, CEO transition.
5. [StockTitan — Viking Holdings 6-K, boosts Q1 revenue, books 92% of 2026 capacity](https://www.stocktitan.net/sec-filings/VIK/6-k-viking-holdings-ltd-current-report-foreign-issuer-f67e945f30ae.html) — corroborates Q1 2026 booking figures.
6. [Market Chameleon — VIK earnings](https://marketchameleon.com/Overview/VIK/Earnings/) — "+5.5% the day following the earnings announcement to close at 86.72"; next earnings 2026-08-19 BMO; +15.2% drift since May print. Used to validate my computed reaction series.
7. [OptionSlam — VIK straddle history](https://www.optionslam.com/earnings/straddle/VIK) — upcoming 2026-08-19 implied move 10.41% (monthly); 2026-05-14 implied 13.19% vs actual 5.53%; earnings date list back to 2024-08-22.
8. [Quiver Quantitative — Viking Holdings Slides Ahead of Earnings as Cruise-Sector Caution Lingers](https://www.quiverquant.com/news/Viking+Holdings+Slides+Ahead+of+Earnings+as+Cruise-Sector+Caution+Lingers) — pre-earnings slide framing, median target $95, target range $93–$120, 27 insider transactions in six months all sales.
9. [TIKR — Viking Holdings Stock Fell 8% Last Friday. The Street's Targets Say It Overshot.](https://www.tikr.com/blog/viking-holdings-stock-fell-8-last-friday-the-streets-targets-say-it-overshot) — 2026-08-14 close $97.99 (−7.65%), weak US retail sales as driver, 16/2/2/1 rating split among 20 analysts, mean target $109.15, Q2 revenue consensus $2.14B.
10. [Yahoo Finance / Zacks — Viking (VIK) Q2 Earnings on the Horizon: Analysts' Insights on Key Performance Measures](https://finance.yahoo.com/markets/stocks/articles/viking-vik-q2-earnings-horizon-131504409.html) — EPS $1.25 (+26.3%), revenue $2.13B (+13%), +0.2% 30-day revision, and the full operating-metric consensus table (capacity PCDs, occupancy, net yield, segment yields).
11. [ChartMill — VIK analyst ratings](https://www.chartmill.com/stock/quote/VIK/analyst-ratings) — next-quarter revenue estimate revised +0.23% over three months (July 2026).
12. [Viking IR — Viking Reports Second Quarter 2025 Financial Results](https://ir.viking.com/news-events/press-releases/detail/202/viking-reports-second-quarter-2025-financial-results) — the Q2 2025 comparison base and, critically, the 2026-season booking disclosure as of 2025-08-10 (55% sold, $3,883M, $866/PCD, +13% YoY).
13. [Viking 6-K exhibit, Q4/FY2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1745201/000174520126000004/vik-ex99_1.htm) — FY2025 revenue $6,501.4M, adj EBITDA $1,872.1M, adj net income $1,165.1M, adj EPS $2.61, net yield $583, segment yields, FY2025 OCF $2,560.3M and capex $1,026.9M, year-end cash/deferred revenue/net leverage, 2026 booking position as of 2026-02-15, Longship delivery delays cutting 2026 river capacity growth 10%→6%.
14. [FinancialContent / StockStory — Viking (VIK) Stock Trades Up, Here Is Why (2026-05-14)](https://markets.financialcontent.com/stocks/article/stockstory-2026-5-14-viking-vik-stock-trades-up-here-is-why) — Q1 2026 revenue beat, adj EBITDA $104.8M vs $100.8M consensus, operating margin 1.1% vs −1.0%.
15. [Viking press — Viking Opens Bookings for 2028–2029 Ocean Voyages (2026-08-06)](https://www.vikingcruises.com/press/press-releases/2026-08-06-viking-opens-bookings-for-2028-2029-ocean-voyages.html) — 700+ departures, 80 voyages, 301 ports, 84 countries; orderbook of 20 river ships by 2028, nine ocean by 2031, two expedition by 2031.
16. [The Motley Fool — Viking (VIK) Q1 2026 Earnings Call Transcript](https://www.fool.com/earnings/call-transcripts/2026/05/14/viking-vik-q1-2026-earnings-call-transcript/) — mid-single-digit yield target, 2027 capacity +15%, Talactac quote on 38% booked, Ocean/River 2027 rates ($882 vs $786; $1,108 vs $992) and the mix caveat, segment Q1 detail, fuel at 4% of adjusted gross margin, cancellation rates, capital-allocation priorities with no buyback.
17. [Barchart — Viking Holdings Reports Earnings While Everyone Waits to Hear What Bookings Actually Look Like (2026-05-13)](https://www.barchart.com/story/news/1915650/viking-holdings-reports-earnings-while-everyone-waits-to-hear-what-bookings-actually-look-like) — Q1 implied move 6.05%, historical average day-0 move 4.17%, year-end 2025 customer deposits $2.7B (+15%), Egypt pause detail, framing of bookings as the market-moving disclosure.
18. [StockTitan — Viking Holdings 6-K, lifts Q1 2026 revenue with strong bookings but stays in loss](https://www.stocktitan.net/sec-filings/VIK/6-k-viking-holdings-ltd-current-report-foreign-issuer-939018577e36.html) — committed ship capex ~$1.9B (2026) and ~$1.0B (2027), $4,418.4M future shipbuilding commitments, net debt $1,941.9M, net leverage 1.0x.
19. [Barchart — VIK put/call ratios](https://www.barchart.com/stocks/quotes/VIK/put-call-ratios) — put OI 21,509 / call OI 13,632 (P/C 1.58), put vol 934 / call vol 652 (P/C 1.43), IV 44.78%, IV rank 62.50%, IV percentile 67%, HV30 34.16%.
20. [SEC EDGAR — Viking Holdings Ltd filing index (CIK 0001745201)](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001745201&type=&dateb=&owner=include&count=60) — 2026 6-K cadence (3 Mar, 31 Mar, 14 May ×2, 15 May), Form 4 dates, Form 144 cluster May–June, 13G filings 6 Aug and 14 Aug.
21. [MarketScreener — VIK target price consensus](https://www.marketscreener.com/quote/stock/VIKING-HOLDINGS-LTD-169452709/consensus/) — 25 analysts, mean target $101.22, 82% buy.
22. [TipRanks — VIK earnings](https://www.tipranks.com/stocks/vik/earnings) — consensus EPS $1.27, revenue $2.17B; average beat of 12.46% over the last two quarters. Note: this page also displays a stale "Aug 26, 2026" next-earnings date, contradicted by the company's own release [1].
23. [Yahoo Finance / StockStory — What To Expect From Viking's (VIK) Q2 Earnings (2026-08-17)](https://finance.yahoo.com/markets/stocks/articles/expect-viking-vik-q2-earnings-034050817.html) — revenue expected +14.1% vs +18.5% prior-year, estimates reconfirmed over 30 days, "Viking rarely misses Wall Street's revenue estimates," peer context.
24. [Forbes — Low Water Levels Are Still Disrupting European River Cruises, From Ship Swaps To Evacuation (2026-08-11)](https://www.forbes.com/sites/emesemaczko/2026/08/11/low-water-levels-are-still-disrupting-european-river-cruises-from-ship-swaps-to-evacuation/) — Rhine/Main/Danube stretches affected, Viking River Cruises named, Viking's 30 July update, August departures most impacted, ship swaps and coach transfers.
25. [Cruise Critic — European River Cruises Hit by Low Water Levels](https://www.cruisecritic.com/news/low-water-disrupts-danube-and-rhine-river-cruises) — Viking's 30 July "exceptionally low" advisory, Viking Ullur aground on the Danube, sister-ship swap mitigation model, Romanian Danube at a 30-year low.
26. [Travel Weekly — Viking ship runs aground amid low water levels](https://www.travelweekly.com/River-Cruising/Viking-ship-runs-aground-in-Europe-due-to-low-water-levels) — the grounding incident.
27. [CNN — Extreme weather is drying up Europe's rivers in a crisis so dire it can be seen from space (2026-08-05)](https://www.cnn.com/2026/08/05/climate/europe-rivers-record-lows-satellite-space-rhine-danube) — July heatwave timeline, Paks record-low Danube reading on 27 July, Romanian 30-year low, ships stranded north of Budapest.
28. [Deloitte — State of the US Consumer, July–August 2026](https://www.deloitte.com/us/en/insights/topics/economy/consumer-pulse/state-of-the-us-consumer.html) — July retail sales −0.6% m/m and +5.2% y/y, discretionary spending intent by category, Fed easing path.
29. [Yahoo Finance — Viking Holdings Ltd Q1 2026 Earnings Call Summary](https://finance.yahoo.com/markets/stocks/articles/viking-holdings-ltd-q1-2026-210124508.html) — April–October core river season, $4.0B cash and $1.0B undrawn revolver, capital-allocation commentary, no buyback discussion.
30. Yahoo Finance option chain API, `https://query2.finance.yahoo.com/v7/finance/options/VIK?date=1787270400` and `?date=1789689600` — 2026-08-21 and 2026-09-18 chains as of 2026-08-17 20:00Z. Source for the ATM straddle (7.59%), the de-vol'd 6.5% event move, the ~90% vs ~45% term structure, the put skew, front-expiry put/call volume, and the $80–$90 downside put activity. All Black-Scholes inversions are my calculations.
31. [MacroTrends — VIK dividend history](https://www.macrotrends.net/stocks/charts/VIK/viking-holdings/dividend-yield-history) — TTM dividend $0.00, yield 0.00% as of 2026-07-27.
32. [Investing.com — UBS reiterates Buy on Viking Holdings stock citing fuel hedging](https://www.investing.com/news/analyst-ratings/ubs-reiterates-buy-on-viking-holdings-stock-citing-fuel-hedging-93CH-4568615) — EUR 500M hedged for 2026 at ~$1.10, fuel ~4% of adjusted gross margin, river fixed-price contracts, UBS Buy.
33. [Maritime Executive — Viking Transitions Management as Torstein Hagen Becomes Executive Chairman](https://maritime-executive.com/article/viking-transitions-management-as-torstein-hagen-becomes-executive-chairman) — Talactac to CEO, Hagen to Executive Chairman, Banh to CFO, announced 2026-05-14.
34. [Fintel — VIK short interest](https://fintel.io/ss/us/vik) — 7,324,491 shares short, 3.54% of float, 2.75 days to cover; borrow fee and utilisation gated.
35. [StockTitan — VIK overview](https://www.stocktitan.net/overview/VIK/) — alternative short interest: 7.5M shares, 2.4% of float, days-to-cover 3.4 (+19.7% period-over-period). `snippet_only`.
36. [Fintel — VIK institutional ownership](https://fintel.io/so/us/vik) — 98.84% institutional ownership, 512 filers, 205,174,371 shares. `snippet_only`.
37. [StockTitan — FMR LLC discloses 5.3% stake in Viking Holdings](https://www.stocktitan.net/sec-filings/VIK/schedule-13g-viking-holdings-ltd-passive-investment-disclosure-5-92f764e4e59d.html) and [CPPIB 13G/A, 3.5% stake](https://www.stocktitan.net/sec-filings/VIK/schedule-13g-a-viking-holdings-ltd-amended-passive-investment-disclos-718bc3b2541c.html) — FMR 16,993,566 shares / 5.3% as of 2026-06-30, filed 2026-08-06; CPPIB 11,244,744 shares / 3.5%, Amendment No. 5.
38. [Ropes & Gray — Viking Holdings Closes on $1.3 Billion Secondary Public Offering](https://www.ropesgray.com/en/news-and-events/news/2025/06/viking-holdings-closes-on-secondary-public-offering) — TPG/CPPIB secondary priced 27 May 2025.
39. [Seatrade Cruise — CPP, TPG launch secondary offering of 30.5m Viking shares](https://www.seatrade-cruise.com/finance-legal-regulatory/cpp-tpg-launch-secondary-offering-of-30-5m-viking-shares) — 30,531,917 shares at $44.20; TPG fully exited, CPPIB retained 31,344,744.
40. [TipRanks / TheFly — Viking Holdings price target changes](https://www.tipranks.com/news/the-fly/viking-holdings-price-target-raised-to-75-from-50-at-stifel-thefly) — Goldman $108→$120 Buy (2026-07-31), Morgan Stanley $86→$93 Equal Weight, Barclays $88→$93 Equal Weight.
41. [Yahoo Finance — VIK analyst insights](https://finance.yahoo.com/quote/VIK/analyst-insights/) — Citi $101→$113 Buy, Stifel $105→$125, UBS Buy $100, J.P. Morgan Buy maintained 2026-08-13.
42. [Stocktwits — VIK sentiment](https://stocktwits.com/symbol/VIK/sentiment) — sentiment score, message volume and participation all N/A without login. Recorded as a gap.
43. [Stocktwits news — Viking CFO Sees Consistent Consumer Trends](https://stocktwits.com/news-articles/markets/equity/viking-cfo-sees-consistent-consumer-trends/chsgN88RdWc) — "extremely bullish" retail sentiment, August 2025. Stale; excluded from my read.
44. [StockInvest.us — VIK](https://stockinvest.us/stock/VIK) — Hold/Accumulate, technical score 0.00, data through 2026-08-13.
45. [Seatrade Cruise — Virtuoso sales rise 21% in 2026 with cruise growth up 22%](https://www.seatrade-cruise.com/resources/virtuoso-sales-rise-21-in-2026-with-cruise-growth-up-22-) — advisor-channel alt-data: 63% of ~800 advisors citing premium/luxury ocean demand, $50K+ bookings 1–2 years out +49%.
46. [PR Newswire — Survey from Cruiseline.com and Shipmate Uncovers Shifting Cruise Trends for 2026](https://www.prnewswire.com/news-releases/survey-from-cruiselinecom-and-shipmate-uncovers-shifting-cruise-trends-for-2026-302831009.html) — Viking top river brand under consideration at 62.3%, 92.8% with a 2026+ voyage booked, 380-day ANZ booking window.
47. [StockTitan — Viking Holdings (VIK) EVP sells 94,276 shares under Rule 10b5-1 plan](https://www.stocktitan.net/sec-filings/VIK/form-4-viking-holdings-ltd-insider-trading-activity-d8ff8cadb2a9.html) — Anton Hofmann, 2026-06-15, $96.04/$95.32 weighted averages, plan adopted 2026-03-09, 292,819 shares remaining incl. 109,904 unvested RSUs.
48. [StockTitan — Viking EVP sells 5,956 shares in planned trade](https://www.stocktitan.net/sec-filings/VIK/form-4-viking-holdings-ltd-insider-trading-activity-2d6df4e5192a.html) — Hofmann, 2026-06-10, $91.00, same 10b5-1 plan.
49. [StockTitan — Viking EVP sells 185,283 shares under trading plan](https://www.stocktitan.net/sec-filings/VIK/form-4-viking-holdings-ltd-insider-trading-activity-e17a8d462900.html) — additional planned sale.
50. [StockTitan — Viking Holdings (VIK) EVP executes 4,610-share sale to cover RSU tax obligations](https://www.stocktitan.net/sec-filings/VIK/form-4-viking-holdings-ltd-insider-trading-activity-c3cc36965c0a.html) — tax-withholding sale, not discretionary.
51. [StockTitan — Viking Holdings CEO sells shares to cover taxes](https://www.stocktitan.net/sec-filings/VIK/form-4-viking-holdings-ltd-insider-trading-activity-46a1fcf0a9a7.html) — CEO tax-withholding sale.
52. [GuruFocus — Karine Hagen insider trading](https://www.gurufocus.com/insider/287723/karine-hagen) — no insider transaction over the trailing 18 months.
53. [StockTitan — Royal Caribbean Q2 2026: Adjusted EPS $4.21; Outlook Up](https://www.stocktitan.net/news/RCL/royal-caribbean-group-reports-second-quarter-results-above-q8hwz22c13o3.html) and [TIKR — Royal Caribbean Stock Moves Higher After Topping Q2](https://www.tikr.com/blog/royal-caribbean-nyse-stock-moves-higher-after-topping-second-quarter-earnings-and-revenue-expectations) — 2026-07-28 beat and raise, net yields +1.9%, FY guidance $17.73–$17.87, stock +5.7%.
54. [PR Newswire — Carnival Corporation Delivers Record Second Quarter Revenues, Net Yields and Adjusted Net Income](https://www.prnewswire.com/news-releases/carnival-corporation-delivers-record-second-quarter-revenues-net-yields-and-adjusted-net-income-302807056.html) and [24/7 Wall St. — Carnival Plunges 6% While Royal Caribbean and Norwegian Tread Water](https://247wallst.com/investing/2026/06/23/carnival-plunges-6-while-royal-caribbean-and-norwegian-tread-water-heres-why/) — 2026-06-23 record Q2, 93% of H2 booked at record prices, record customer deposits $9.0B, 2027 European bookings up mid-teens at higher prices, stock −6%.
55. [Norwegian Cruise Line Holdings IR — Second Quarter 2026 Financial Results](https://www.nclhltd.com/investors/news-events/press-releases/detail/812/norwegian-cruise-line-holdings-reports-second-quarter-2026) — 2026-07-30 Q2 beat (revenue +4.9% to $2.6B, adj EPS $0.48, adj EBITDA $666M) with FY guidance cut to ~$1.50 adj EPS, net yield ~−5%, Q3 net yield −8.9%.
56. [StockStory — Norwegian Cruise Line Posts Q2 CY2026 Sales In Line With Estimates But Stock Drops](https://stockstory.org/us/stocks/nyse/nclh/news/earnings/norwegian-cruise-line-nysenclh-posts-q2-cy2026-sales-in-line-with-estimates-but-stock-drops) — drivers of the NCLH cut: Middle East disruption, higher fuel, softer European summer demand, self-inflicted marketing/revenue-management issues.

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such.*
