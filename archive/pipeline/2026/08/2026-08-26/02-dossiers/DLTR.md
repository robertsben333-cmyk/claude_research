# DLTR — Dollar Tree, Inc.

**What this print is about.** Dollar Tree reports Q2 FY2026 (quarter ended 1 August 2026) before the open on Thursday 27 August 2026 [1]. This is not an EPS-line print — it is a *guidance-versus-positioning* print. The company beat hugely last quarter (adj. EPS $1.74 vs ~$1.53–1.56 Street, stock +17.87% on the day [2][3][20]) and the shares have since run **+43.5% in three months** to $134.48, which is **above** the Street's average price target of $131.68 and against a consensus rating of *Hold* (14 of 27 analysts) [4][20]. The Street's FY2026 adjusted EPS number of **$7.04** already sits near the top of management's own $6.70–$7.10 guide [4][5], so a simple in-line quarter plus a reiterated guide is, arithmetically, a disappointment. Three things can break that stalemate: (a) whether the July traffic inflection that Placer.ai and Jefferies flagged (+4.5% rolling three-month visits) actually shows up in the comp [6]; (b) whether management finally quantifies and books **IEEPA tariff refunds**, which are explicitly *excluded* from guidance and which Walmart just monetised to the tune of ~$3bn [7][8]; and (c) whether the **new Section 301 tariffs (10–12.5% across 60 economies, ~$20m/month or ~$70m/quarter of COGS pre-mitigation for DLTR)** force a second-half margin caveat [9]. Options price a ~9.2% move; the last two times DLTR went into a print on a >20% three-month run-up it fell ~8.4% both times [own calc, 2].

---

## 1. Event & anchors

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| **event_confirmed** | **true** | — | Company 8-K exhibit 99.1, filed 2026-08-06 [1] |
| Earnings date | 2026-08-27 (Thursday) | — | [1] |
| Session | **bmo** — "before the stock market opens" | — | [1] |
| Call time | 08:00 ET, hosted by CEO Mike Creedon & CFO Stewart Glendinning | — | [1] |
| Fiscal period | Q2 FY2026, quarter ended 2026-08-01 | — | [1] |
| Date changed / pre-announced? | **No.** Date announced 2026-08-06 and unchanged. No 8-K since 2026-08-06; no Item 2.02/7.01 pre-announcement, no Item 4.02, no Item 5.02 in 2026 | 2026-08-26 | SEC submissions feed [10] |
| Spot | **$134.48** (close; day range $132.28–$136.17, vol 2,623,971; prior close $136.75) | 2026-08-25 20:00Z | Yahoo chart API [2]; corroborated by StockAnalysis [4] |
| Spot (intraday 8/26 reference) | $134.48 "last trade as of Aug 26, 2026" (Nasdaq); $134.73 quoted by StockStory 8/26 | 2026-08-26 | [11][12] |
| Market cap | **$25.84bn** (192.17m shares out × $134.48) | 2026-08-26 | [4]; share count corroborated at 192,174,588 as of 2026-05-26 in Mantle Ridge 13D/A [13] |
| 52-week range | $84.71 – $142.40 intraday; highest *close* in trailing 252 sessions $141.21 | 2026-08-25 | [2][4] |
| **Event-implied move (my calculation)** | **±9.2%** — Aug-28 ATM straddle: $134 strike C mid 6.325 + P mid 5.975 = **$12.30** = 9.15% of spot; $133/$135/$136 strikes all give 9.18% | 2026-08-26 chain snapshot | Nasdaq options API [11] |
| Implied move (published, cross-check) | 9.26% weekly (Aug-28 expiry); 11.12% monthly (Sep-18) | 2026-08-26 | OptionSlam [14] |
| Implied move (published, older) | 10.51% | 2026-08-24 (spot $131.70) | ad-hoc-news [15] — `snippet_only`-grade secondary; **triage's 10.51% hint is 2 days stale and 1.3pts rich vs the live chain** |
| Straddle breakevens (Aug-28) | ≈ $122.2 down / $146.8 up | 2026-08-26 | own calc from [11] |
| **IV / IV rank** | IV 51.13%, **IV Rank 71.19%** | Barchart page, as-of not stamped | [16] |
| Realised vol (own calc) | 20-day 23.8% annualised; 60-day 35.9% | 2026-08-25 | own calc from [2] |
| Put/call — volume | **1.77** (3,854 puts / 2,175 calls) | Barchart current session | [16] |
| Put/call — open interest | **0.62** (31,722 puts / 51,479 calls) | Barchart | [16] |

### Historical one-day earnings reactions

Every date below is the **actual SEC filing date of the corresponding 10-Q/10-K** (all DLTR reports are BMO, so the reaction is same-day close vs prior close). Moves computed by me from daily closes [2][10].

| Report date | Quarter | Prior close | Close | **1-day move** |
| --- | --- | --- | --- | --- |
| 2024-09-04 | Q2 FY24 | $81.65 | $63.56 | **−22.16%** |
| 2024-12-04 | Q3 FY24 | $72.48 | $73.83 | **+1.86%** |
| 2025-03-26 | Q4 FY24 | $67.14 | $69.21 | **+3.08%** |
| 2025-06-04 | Q1 FY25 | $96.72 | $88.62 | **−8.37%** |
| 2025-09-03 | Q2 FY25 | $111.35 | $102.03 | **−8.37%** |
| 2025-12-03 | Q3 FY25 | $108.99 | $112.92 | **+3.61%** |
| 2026-03-16 | Q4 FY25 | $107.46 | $114.36 | **+6.42%** |
| 2026-05-28 | Q1 FY26 | $95.87 | $113.00 | **+17.87%** |

- **Last 6 quarters:** mean |move| **7.95%**, median |move| **7.39%**, max |move| **17.87%**. Pattern: **+ − − + + +** (4 up / 2 down).
- **Last 8 quarters:** mean |move| **8.97%**, median |move| **7.39%**, max |move| **22.16%**. 5 up / 3 down.
- **Implied vs realised:** the 9.2% live implied sits just above the 6-quarter mean absolute (7.95%) and well above the median (7.39%). Options are **modestly rich, not egregiously so** — the tail (2024-09-04's −22%) is what pays for it.

**My inference (labelled as mine, small-sample, fragile):** reaction is negatively related to the three-month pre-print run-up. Run-ups and subsequent moves: −32.5%→−22.16%; +14.0%→+1.86%; −2.8%→+3.08%; **+45.1%→−8.37%**; **+22.0%→−8.37%**; +6.8%→+3.61%; −13.5%→+6.42%; −24.9%→+17.87%. Spearman ρ = −0.31 on all eight; excluding the Sep-2024 guidance-collapse outlier, Pearson r = **−0.92** on the remaining seven. **The current three-month run-up is +43.5% — the largest in the sample.** Its nearest analogue (2025-06-04, +45.1%) produced −8.37% *on a beat*. n=7 with a discretionary exclusion; treat as suggestive, not load-bearing.

---

## 2. The bar

| Metric | Company guidance (issued 2026-05-28) | Consensus | Source |
| --- | --- | --- | --- |
| Q2 net sales | **$4.8–4.9bn** | **$4.85bn** (+6.3% y/y) | [5][17][12] |
| Q2 comparable store sales | **+2.5% to +3.5%** | Sell-side modelling ~**4.0%** (vs 3.0% for DG) | [5][18] |
| Q2 adjusted diluted EPS (cont. ops) | **$1.00–$1.15** | **$1.11** (Zacks); +44.2% y/y | [5][17] |
| FY2026 net sales | $20.5–20.7bn | $20.67bn | [5][4] |
| FY2026 comps | +3% to +4% | — | [5] |
| FY2026 adjusted EPS | **$6.70–$7.10** (raised from $6.50–6.90 at Q4) | **$7.04** (21 analysts) | [5][4][19] |

**Estimate revisions.** Zacks reports the Q2 consensus mark **unchanged over the past 30 days**; StockStory likewise says analysts "generally reconfirmed their estimates over the last 30 days" [17][12]. Directionally the FY number has drifted up over the quarter: consensus was **$6.67** at the time of the May guide-raise and is now **$7.04** [19][4]. I could **not** source a precise 30/60/90-day consensus revision series — see coverage gaps.

**Individual sell-side marks above consensus.** Jefferies Q2 EPS **$1.15** (top of the guide band), comp **+3.4%** decomposed as traffic +0.8% / ticket +2.6% [6]. Oppenheimer Q2 **$1.13**, FY **$7.05**, and explicitly flags the FY midpoint could be raised **$0.10–$0.20** [19].

**Prior guidance vs Street, and the comparison base.** Q2 FY25 (the base) was net sales $4,566.8m, GAAP op income $231.0m (5.06% margin), GAAP diluted EPS $0.91, **adjusted EPS $0.77 — which the company disclosed "included $0.20 of positive impact, relative to expectations, related to tariff timing"** [20][21]. So the +44% y/y growth headline is measured against an *inflated* base; that makes the optical bar harder, not easier. Offsetting it: diluted share count was 207.8m in Q2 FY25 and 197.4m in Q1 FY26 [21], so a ~7% share-count tailwind does roughly a sixth of the work on its own.

**What has to happen just to hold the stock flat (my inference).** Given spot is 2.1% *above* the average target and the Street's FY number is already $7.04 against a $6.70–7.10 guide, the neutral outcome is roughly: Q2 adj. EPS **≥ $1.15** (top of guide), comp **≥ 3.5%** (top of guide) with traffic at least flat-to-positive, **and** an FY adjusted EPS guide raised to at least **~$7.15–$7.25** with the tariff-refund question addressed constructively. A $1.11–1.13 print with a reiterated $6.70–7.10 FY range is, in my read, a down day.

**Whisper number.** Earnings Whispers' DLTR page returned no populated whisper figure when fetched [22]. **Unavailable.** The nearest usable proxies are the two named analyst marks above consensus (Jefferies $1.15, Oppenheimer $1.13) and the ~4.0% comp expectation [6][18][19].

---

## 3. The one metric that matters

**The FY2026 adjusted-EPS guidance revision, and specifically whether it is funded by tariff refunds.** Not headline EPS, and not even the comp.

Why:
1. **Guidance is the binding constraint on the stock, not the quarter.** The Street is at $7.04 inside a $6.70–$7.10 guide [4][5]. There is no room for a reiterate. Oppenheimer's published expectation is a **$0.10–$0.20 midpoint raise** [19], so the market-implied bar is roughly FY **$6.80–$7.30**, midpoint ~$7.05, i.e. a raise is already in the price.
2. **The refund is the single largest unbaked variable.** On the Q1 call management stated plainly that **"no tariff refunds are assumed in either recent results or forward outlook due to timing and amount uncertainty,"** and said any refund would likely be **reinvested in customer value** rather than dropped to EPS [23][17]. Since then the mechanism has become concrete: SCOTUS struck down the IEEPA tariffs 6–3 on 2026-02-20; the CIT ordered ~$165bn of refunds; CBP reported **~$128.68bn accepted for processing** in its CAPE system as of 2026-07-31 [24][25]. **Walmart booked nearly $3bn of tariff refunds in its 2026-08-20 quarter and redeployed it into 11,000+ rollbacks (up from ~7,200)** [7][8]. Dollar Tree imports ~40% of merchandise, the vast majority from China [26]. The market will read Walmart's precedent straight across.
3. **The offset is now identifiable.** New Section 301 tariffs of **10–12.5% across 60 economies** are estimated at **~$20m/month, ~$70m/quarter of COGS for DLTR pre-mitigation** [9]. On $4.85bn of quarterly revenue that is ~1.4% of sales, or roughly **$0.27/share pre-tax** on ~193m shares — material against a $1.11 consensus, and it lands mostly in H2 (the quarter being reported ended 2026-08-01).

**What the market expects for it, and how I know:** a raise of $0.10–$0.20 at the midpoint (Oppenheimer, published [19]); Street already at $7.04 (21 analysts, StockAnalysis [4]); Raymond James and Goldman both named **tariff reimbursements** explicitly in their July upgrade theses [27]. The asymmetric outcome nobody has modelled is management quantifying a refund receivable *and* saying most of it goes back into price — good for the multi-year comp story, neutral-to-bad for the FY EPS line the stock is priced off.

**Secondary metric to watch:** **traffic**. Q1 traffic was **−1.0%** with ticket **+4.5%** [5]; Q4 FY25 was traffic −1.2% / ticket +6.3% [28]. Jefferies' Placer.ai read has Q2 visits **+1.4%** and **July +4.5%**, modelled as a **+0.8% traffic comp** [6]. A positive traffic comp would be the first in three quarters and is the cleanest evidence that multi-price is additive rather than just mix.

---

## 4. Fundamentals — what changed, what is at stake

**Segment mix / structure.** Dollar Tree is now a single-banner business. Family Dollar was sold on 2025-07-05; Q1 FY26 still carried **$21.1m of transition-services-agreement income** in corporate SG&A, and the company said it will move to **consolidated SG&A reporting from fiscal 2027**, eliminating the separate corporate segment [5][23]. Corporate SG&A fell **15% y/y** and levered **70bps to 2.4% of total revenue** in Q1 [23]. TSA runoff is a modest, known headwind to that line.

**Q1 FY2026 (reported 2026-05-28), the most recent datapoint** [5][21][23]:

| | Q1 FY26 | Q1 FY25 | Δ |
| --- | --- | --- | --- |
| Net sales | $4,970.5m | $4,636.5m | **+7.2%** |
| Comparable store sales | +3.5% (traffic −1.0%, ticket +4.5%) | — | — |
| Gross margin | — | — | **+120bps** |
| SG&A % of revenue | 27.8% | 27.3% | +50bps (marketing, general liability) |
| GAAP operating income | $473.3m (9.52%) | $384.1m (8.28%) | **+124bps** |
| GAAP diluted EPS (cont. ops) | $1.76 | $1.61 | +9.3% |
| **Adjusted diluted EPS** | **$1.74** | $1.26 | **+38%** |
| Diluted shares | 197.4m | 213.9m | **−7.7%** |
| Merchandise inventory | $2,470.8m | $2,704.0m | **−8.6%** |

Gross-margin drivers in Q1: higher merchandise margin, freight favourability and lower shrink, partly offset by **higher tariffs and markdowns** [5][23]. Management said shrink "improved year-over-year as our strategies are gaining real traction" [23].

**Unit economics / format.** 9,382 stores at Q1-end (113 opened in the quarter); **~5,900 multi-price stores**, with ~630 converted or opened as multi-price in Q1 alone [5][29]. FY26 plan: **~400 openings, 75 closures** [5][29]. Critically, **~85% of sales remain at $2 and below** — the multi-price expansion is a ticket lever layered on an intact opening price point, not a repositioning [23].

**Free cash flow and balance sheet** (quarter ended 2026-05-02) [21][23]:
- Operating cash flow (continuing ops) **$644.0m** in Q1; **$2,190.7m** in FY25.
- **Free cash flow $392m** in Q1 [23].
- Cash **$1,007.3m**; long-term debt **$2,932.6m**; shareholders' equity **$3,507.0m**; non-current operating lease liability $3,655.5m.
- Long-term debt rose **$500m** in Q1 because the company drew a new **$500m term loan on 2026-03-19** (SOFR + 1.00%, matures 2029, no amortisation) [30]. Net debt ~$1.93bn against $2.19bn of FY25 operating cash flow — under 1× — but this is explicitly **debt-funded buyback capacity**, which is a modest quality caveat.

**Buyback / dilution.** This is the loudest capital-allocation signal in the name:
- Q1 FY26: **5.5m shares for $595m** ($585.8m cash) [5][21].
- Trailing twelve months: share count down **~8%**; **$1.7bn returned** [23]. FY25 repurchases $1,548.0m [21].
- June 2026: **$500m block repurchase** from selling stockholders including Mantle Ridge funds [31].
- **2026-07-01: Board replenished the authorisation to $2.5bn** (8-K Item 8.01) — **~9.7% of the current market cap** [32][31].
- **Guidance assumes no future repurchases** [23]. Every dollar spent is therefore incremental to the guided EPS.

**Working capital.** Inventory down 9% on sales up 7.2% — a ~16pt favourable spread — which management framed as fresher assortments and ~$425m of avoided carrying cost [23]. This is a real margin-of-safety item: it lowers markdown risk into the holiday build.

**Freight.** Management moved freight contracts to **shorter-term arrangements** to track spot rates, keeping favourable base rates but wearing higher **fuel surcharges**; elevated fuel was assumed for all of 2026 in the guide [23][19].

**What changed since the last print:** the $2.5bn buyback replenishment (July 1) [32]; the Mantle Ridge exit (June 24) [13][33]; the new Section 301 tariff regime (~$70m/quarter pre-mitigation) [9]; the tariff-refund machinery becoming operational with Walmart's ~$3bn precedent [7][24]; and a sell-side capitulation wave (Goldman off Sell, Jefferies off Underperform) [27][34].

---

## 5. Positioning & options

**Term structure (my calculation, raw ATM straddle ÷ spot, from the live Nasdaq chain [11]):**

| Expiry | ATM straddle | % of spot |
| --- | --- | --- |
| **2026-08-28** (first post-event) | $12.30–12.35 | **9.16%** |
| 2026-09-04 | $13.40–13.48 | 9.98% |
| 2026-09-11 | $13.40–14.05 | ~10.2% |
| 2026-09-18 | $14.95–15.05 | **11.12%** |

The Aug-28 contract has **two calendar days** of life and prices 9.16%; the Sep-18 contract has 23 days and prices 11.12%. Nearly the entire front-month variance is the event. My Sep-18 figure of 11.12% matches OptionSlam's published 11.12% exactly [14], which is a good validation of the chain snapshot.

**Skew — this is where I disagree with triage.** Triage's rationale cited "elevated bearish put/call skew." On *price*, the Aug-28 wings are close to symmetric [11]:
- $124 put (−7.8% OTM) mid **$2.33** vs $145 call (+7.8% OTM) mid **$2.43** — calls very slightly richer.
- $120 put (−10.8%) mid **$1.15** vs $150 call (+11.5%) mid **$1.05** — roughly balanced.

On *flow*, however, the put bias is real and fresh: Barchart shows session **put/call volume 1.77** (3,854 puts vs 2,175 calls) [16], and the single largest line in the front expiry is **1,524 contracts of the Aug-28 $124 put against open interest of only 85** — brand-new downside protection struck ~7.8% below spot [11]. Meanwhile **open interest is call-heavy: P/C OI 0.62** (31,722 puts vs 51,479 calls) [16], and the biggest OI concentrations in the chain are all upside calls: Sep-18 **$145 calls OI 6,377**, Sep-18 **$140 calls OI 3,018**, Sep-18 **$130 calls OI 3,004** [11].

**My read:** the book is *structurally long via calls* and is *buying puts into the print*. That is hedging on top of a crowded long, not a bearish skew regime. Corrected characterisation: **crowded-long with fresh downside insurance**, which is a worse setup for a beat than a genuinely bearish book would be — there is no short base to squeeze.

**Short interest.** 7,772,719 shares short, **4.35% of float**, **days-to-cover 4.3** on 1.91m average daily volume, settlement date **2026-08-14**, and **down 21.75% versus the prior report** [35]. Shorts have been covering into the run. Low and falling short interest removes the squeeze mechanism from the bull case.

**Borrow fee:** **unavailable** — Fintel's securities-lending page returned HTTP 403 and no other provider surfaced a rate [36]. Given 4.35% short interest on a $25.8bn Nasdaq large cap, general-collateral borrow is the overwhelmingly likely state, but I am not asserting a number.

**Run-up / drawdown into the print (own calc from [2]):**

| Window | Move to 2026-08-25 close |
| --- | --- |
| 5 sessions | **+3.07%** |
| 10 sessions | +5.01% |
| 1 month | **+7.12%** |
| 3 months | **+43.52%** |
| 6 months | +2.10% |
| 12 months | +18.67% |

Last five closes: 08-19 $131.84 · 08-20 $128.45 · 08-21 $131.48 · **08-24 $136.75 (+4.01%)** · 08-25 $134.48 (−1.66%) [2]. The 8/24 jump was attributed to pre-earnings positioning, improving sell-side sentiment, and a reported new institutional stake of 398,171 shares [37].

**Crowding.** Institutional ownership is reported at ~97.4%, with 406 institutional buyers vs 487 sellers in Q2 2026 [37][38]. BlackRock is reported at 8.29% [38]. Retail sentiment on Stocktwits is described as "bullish" [27]. Sell-side has upgraded four times in seven weeks. Every constituency is on the same side.

---

## 6. Sentiment & alt-data

**Analyst actions (chronological, all 2026):**

| Date | Firm | Action | PT |
| --- | --- | --- | --- |
| 07-09 | Raymond James | Market Perform → **Outperform** | $140 [27] |
| 07-09 | Goldman Sachs | **Sell → Neutral** | $105 → $125 [27] |
| 07-31 | Bernstein | Market Perform (maintained) | $124 → $127 [34] |
| 08-06 | BMO Capital (Bania) | Underperform (maintained) | $90 → $98 [34] |
| 08-11 | Wells Fargo | Overweight (maintained) | $145 → **$155** [34] |
| 08-18/19 | Jefferies (Tarlowe) | **Underperform → Hold** | $85 → **$135** [6][34] |
| 08-22 | Wall Street Zen | Hold → **Buy** | — [19] |

**Price-target drift is up but still below spot.** Reported consensus targets, all within the last week: **$131.68** (StockAnalysis, 27 analysts, 2026-08-26) [4]; **$130.25** (Barchart) [3]; **$129.64** (public.com, 27 analysts) [34]; **$127.32** (MarketScreener, 27 analysts, range $85–$170) [39]; **$123.41** (ad-hoc-news, 2026-08-22) [19]; median **$130.00** across 17 analysts over six months (Quiver) [37]. **Spot $134.48 is above every one of them.** Rating distribution: 6 Strong Buy / 4 Buy / **14 Hold** / 2 Sell / 1 Strong Sell; range $98–$170 [4].

**Alt-data — the strongest single piece of evidence in this dossier.** Jefferies' upgrade was built on **Placer.ai rolling three-month visit data**: Q2 customer traffic **+1.4%**, accelerating to **+4.5% in July**, which its model converts to a **+0.8% traffic comp** and a **+3.4% total comp** (ticket +2.6%) [6]. This matters because traffic was **−1.0% in Q1** and **−1.2% in Q4 FY25** [5][28] — a positive traffic comp would be a genuine inflection, and it is the metric Goldman and BMO both cite as the reason for their remaining caution [27][34].

**Retail / social tone.** Stocktwits sentiment was described as **"bullish"** as of July 2026 and moved to **"extremely bullish" with message volume +1,100% in 24 hours** — but that surge datapoint is from the **post-Q1 (late May 2026)** reaction, not this week [27][40]. I have **no clean 7/14/30-day social trend series** for the current window; treat retail tone as directionally bullish and non-load-bearing. Message volume is reported up ~50% y/y with watchers +1.8% [27].

**Google Trends:** **unavailable** — no sourced search-interest series for "Dollar Tree" for August 2026 could be retrieved [41].

**Job postings / reviews / web traffic:** not sourced. See coverage gaps.

---

## 7. Forensics

**Form 4 activity.** Recent officer/director filings are **entirely routine and non-discretionary** [10]:
- **2026-08-03** (txn 2026-08-01): Stephanie Stahl, Director — code **C** (conversion of deferred/restricted units), 1,185 shares acquired, holding 5,274. No sale.
- **2026-08-03** (txn 2026-08-02): Aditya Maheshwari, **Chief Accounting Officer** — code **F** (shares withheld for tax), 127 shares at $127.21, holding 5,896.
- **2026-07-06/07** and **2026-04-02/03**: clusters of Form 4s on the 07-01 and 04-01/03-31 annual grant/vest dates — mechanical equity-compensation activity, not signal.
- Reported publicly: CEO Creedon's 2026 transactions were a tax-withholding disposition of 10,224 shares plus a 44,158-RSU grant (April), and 1,929 shares from three-year PRSU settlement with 1,687 auto-surrendered at $109.51 (2026-03-31) [42].
- **No discretionary open-market officer purchase or sale in the last two months.** Quiver counts **1 insider trade in six months: the Mantle Ridge sale, 0 purchases** [37]. A third-party aggregator reports a Glendinning net purchase of 20,500 shares, but I could not verify it against a specific Form 4 and am **not treating it as sourced** [42].
- 10b5-1 status: the August filings are C and F codes, which do not require a plan; no 10b5-1 checkbox assertion is being made here.

**The activist exit — the most important forensic item.** Mantle Ridge LP (a **"director by deputization"** filer, i.e. Paul Hilal sits on the board) reported on Form 4 for **2026-06-24** [13]:
- Conversion (code C) of 602,170 shares, taking beneficial ownership to 12,706,663;
- **Sale (code S) of 2,230,455 shares at $111.31** (~$248m);
- **In-kind distribution (code J, $0) of 10,266,164 shares** to limited partners, leaving **210,044 shares**.

The accompanying 13D/A (filed 2026-06-25) records Mantle Ridge, MR Cobalt Advisor and Paul Hilal each at **~0.1%** of 192,174,588 shares outstanding and states they have **ceased to be beneficial owners of more than 5%** — while **Hilal remains on the board** [13][33]. Two readings, both defensible: (i) the overhang is now cleared and the block sale was absorbed at $111 with the company itself buying $500m of it [31]; (ii) the activist who drove the Family Dollar separation and the turnaround thesis has monetised at ~$111 into a stock now at $134.48. The in-kind distribution also means ~10.3m shares sit with LPs who may sell on their own schedule — a diffuse, unquantifiable supply overhang.

**Auditor / restatement.** No Item 4.02 filing and no restatement disclosure in the 2026 filing record [10]. Nothing sourced suggesting an auditor issue.

**Executive / director departures.** No Item 5.02 8-K in 2026 [10]. The CEO/CFO pair hosting this call (Creedon/Glendinning) is unchanged from Q1 [1][23]. No CFO change found [29].

**8-K cadence.** 2026 year-to-date: 02-23, 03-16, 03-23, 05-07, 05-28, 06-23, 07-02, 08-06 — **eight filings**, versus roughly sixteen in calendar 2025 [10]. Cadence is *lower*, not elevated, and every 2026 filing is explicable (earnings-call announcements, earnings results, the term loan, annual-meeting results, the buyback authorisation). **No 8-K since 2026-08-06** means no pre-announcement and no guidance revision in the three weeks into the print.

**Filing-language / tone.** Q1 disclosure language was notably *pre-committed to conservatism*: "no tariff refunds are assumed," "several variables that remain dynamic today, including tariffs, fuel, freight and just some broader consumer pressure," and elevated fuel assumed for all of 2026 [23]. Management has deliberately built a low bar for itself and has beaten it — trailing four-quarter average earnings surprise **+32.1%**, last quarter **+13.7%** [17].

---

## 8. Macro & peer read-through

**Tariff regime — the defining macro variable.** SCOTUS ruled **6–3 on 2026-02-20** that IEEPA does not authorise the president to impose tariffs; the CIT ordered CBP to refund **~$165bn** (estimates up to $175bn) of unlawfully collected duties, with statutory interest at 6% for corporates [24][25]. As of **2026-07-31**, ~**$128.68bn** of potential and certified refunds had been accepted for processing in CBP's CAPE system; **refunds are not automatic — importers must file** [24]. Separately, **new Section 301 tariffs of 10–12.5% on imports from 60 economies** are now in force; DLTR's estimated exposure is **~$20m/month, ~$70m/quarter of COGS pre-mitigation** [9]. China's effective rate is reported around 37.5% all-in [26]. Dollar Tree imports ~**40%** of merchandise, mostly from China [26], and in prior tariff rounds mitigated **>90%** of incremental cost via sourcing shifts, pack-size/spec changes, item deletion and multi-price flexibility [26].

**Peers who already reported (all August 2026):**

| Company | Date | Result | Stock reaction |
| --- | --- | --- | --- |
| **TJX** | 08-19 | Comps **+4%**, pre-tax margin **13.3% (+190bps)**, above plan | "ticks up" [43] |
| **Walmart** | 08-20 | US comps **+2.6% vs +3.8% est — slowest in six years**; ~**$3bn tariff refunds** redeployed into 11,000+ rollbacks (from ~7,200) | — [7][8] |
| **Ross Stores** | ~08-20 | Revenue **+13%**, comps **+10%**, EPS **$2.66 vs $1.95**; FY guide raised to $8.61–8.77 from $7.50–7.74 | **+8%** [43][44] |
| **Target** | ~08-19 | Revenue **+5.3%**, beat by 1.5%; FY sales guide raised to ~+4% from ~+2%; traffic up, spend per trip flat | **+3.8%** [12][45] |
| **BJ's** | Aug | Revenue **+15.7%**, beat by 4.7% | **+7.9%** [12] |
| **Dollar General** | **08-27, same morning**, call 09:00 ET (after DLTR's 08:00 call) | Consensus EPS **$2.00**, revenue **$11.17bn** (+4.2%) | pending [46] |

**Read-through, my synthesis.** Value and off-price retail is running hot (Ross +10% comps, TJX +4%, BJ's +15.7%); the one weak print is **Walmart's low-income-exposed US comp**, which is precisely DLTR's customer overlap. Bank of America Institute reports the "K-shaped" pattern has largely disappeared in 2026, that **lower-income households' spending at discount apparel stores has grown five times faster than higher-income households**, and that larger tax refunds plus an improving labour market are supporting the low end — but also that the top 10% of households now account for roughly half of all consumer spending, the highest share on record back to 1989 [45][47]. Fuel is the swing factor management flagged: gasoline was **$3.27/gal on 2026-08-25** on the futures/commodity series, though a separate retail series reports drivers paying **$4/gal in the second week of August for the first time**, and the commodity series is ~53% higher y/y [48][49]. **These two fuel figures conflict; I am reporting both rather than picking one.** Walmart's CFO framing — "$4 gas has a psychological impact" — is the relevant channel [7].

**Same-day correlation risk.** DG reports the same morning and its call starts an hour after DLTR's. A strong DLTR / weak DG (or vice versa) sets up an intraday pairs unwind that can amplify or mute DLTR's move independent of its own numbers. Sell-side is already modelling **DLTR comp ~4.0% vs DG ~3.0%** [18].

**Rate / FX / commodity sensitivity.** Beta 0.67 [4]. Minimal direct FX exposure (US/Canada operations); the real FX channel is USD-denominated China sourcing cost. Rate sensitivity is modest and mostly on the floating $500m term loan at SOFR+1.00% [30]. Diesel/fuel is the live commodity input via freight surcharges [23].

---

## 9. Bull case / bear case / base case

**Bull case.** The alt-data says the comp inflects. Placer.ai three-month rolling visits accelerated to **+4.5% in July** and Jefferies converts that to a **+0.8% traffic comp / +3.4% total comp**, above the 2.5–3.5% guide, with Q2 EPS at **$1.15** — the top of the band [6]. That would be the first positive traffic quarter in three, precisely the objection Goldman and BMO have been holding out on [27][34]. The peer tape is supportive: Ross +10% comps and a big guidance raise, TJX +4% comps with 190bps of margin, BJ's +15.7%, Target raising its FY sales guide [43][44][12]. Management guided conservatively on purpose — no tariff refunds, elevated fuel all year, **no future buybacks assumed** — and then replenished a **$2.5bn authorisation equal to ~9.7% of the market cap** on 2026-07-01, on top of an ~8% trailing-twelve-month share-count reduction [23][32][31]. Trailing four-quarter average surprise is **+32.1%** [17]. If they beat to ~$1.20 and take the FY guide to $7.20+ while quantifying a refund receivable, the 9.2% implied move is cheap to the upside and the last three reactions (+3.61%, +6.42%, +17.87%) show the market will pay for it.

**Bear case.** Everything good is already in the price and then some. The stock is **+43.5% in three months**, trading **above every published consensus target** ($123.41–$131.68) with **14 of 27 analysts at Hold** and three at Sell [2][4][19][39]. The Street's FY number, **$7.04**, is already at the top of the $6.70–$7.10 guide, so a reiterate is a de-facto cut [4][5]. The comparison base is contaminated upward: Q2 FY25 adjusted EPS of $0.77 **included $0.20 of tariff-timing benefit** [20]. New Section 301 tariffs at **~$70m/quarter pre-mitigation** land mostly in H2 and give management every reason to hedge the back half [9]. Walmart just told the market that the low-income US consumer produced the slowest comp in six years, and fuel is the pressure point management itself flagged [7][23]. Positioning is one-sided: short interest is only **4.35% of float and fell 21.75%** into the print, so there is no squeeze fuel; OI is call-heavy (P/C OI 0.62) while today's flow is defensive (P/C volume 1.77, with 1,524 fresh Aug-28 $124 puts against 85 OI) [35][16][11]. And the activist who built the thesis **distributed and sold out at ~$111** in June, leaving ~10.3m shares in LP hands [13][33]. My run-up regression — fragile, n=7, but the two prior >20% three-month run-ups produced **−8.37% both times, one of them on a beat** — points the same way.

**Base case.** Dollar Tree beats the quarter and raises the year modestly, and the stock does not reward it. I expect Q2 adjusted EPS in the **$1.14–$1.22** range (guide top to a normal-sized beat) on comps of **3.5–4.5%** with traffic roughly flat to slightly positive, and an FY adjusted EPS guide moved to something like **$6.95–$7.30** — a $0.10–$0.20 midpoint raise, exactly what Oppenheimer has already published as the expectation [19]. Tariff refunds get discussed and probably framed as reinvestment in price rather than an EPS windfall, consistent with Q1 language and Walmart's playbook [23][7][8]. That is a good quarter into a stock priced above every target with a Hold-consensus book positioned long. I put roughly **55% probability on a negative one-day reaction**, with the distribution wide and fat on both sides: the realised 6-quarter mean absolute move is 7.95% against a 9.2% implied, so I do not think the straddle is meaningfully mispriced — the edge, such as it is, is in direction, and it is thin.

---

## 10. What would flip the consensus view

**The most credible reversal: management puts a hard dollar number on the IEEPA tariff refund and flows a majority of it to the FY guide rather than to price investment.**

Concretely: if the release or the 08:00 ET call discloses a refund receivable of, say, **$150–400m** (a plausible scale for an importer of ~40% of $20bn of merchandise, against Walmart's ~$3bn on ~6× the revenue base [7][26]) and management raises FY2026 adjusted EPS to **$7.40+** rather than the ~$7.05–7.15 the Street has pencilled in, then every bear pillar collapses at once: the "above target" objection dies because targets reset upward within hours; the "Street at the top of the guide" objection inverts; and the $2.5bn authorisation gets read as accretive to a materially higher base. On that path I would expect the stock through $145 and the 9.2% implied move to be exceeded to the upside, exactly as it was in May (+17.87% [2]).

The mirror-image reversal, less likely but cleaner to falsify: **a positive traffic comp with a reiterated FY guide.** If traffic prints positive (validating Placer) but management holds $6.70–$7.10 citing the new Section 301 cost of ~$70m/quarter [9], the market will conclude the tariff offset is bigger than modelled and sell the beat. That specific combination — good comp, unchanged year — is my single highest-probability path to a −8% day.

**What would make me wrong about the run-up fade:** a positive traffic comp *and* an FY raise to $7.20+. Two conditions, both observable within the first ten minutes of the release.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **Whisper number** — EarningsWhispers page returned unpopulated fields [22] | The published consensus ($1.11) is demonstrably below where named analysts sit ($1.13–$1.15). Without a whisper I am inferring the real bar from two sell-side marks and one modelled comp (~4.0%), which is thinner evidence than I would like on the single most important calibration input. |
| **Precise 30/60/90-day consensus revision series** — only "unchanged over 30 days" (Zacks/StockStory) and a $6.67→$7.04 FY drift [17][12][19][4] | Cannot distinguish a quietly-rising bar from a genuinely static one; revision momentum is normally a first-order input to post-print drift. |
| **Borrow fee / cost-to-borrow** — Fintel 403, no alternative provider [36] | With short interest down 21.75% and DTC 4.3, borrow is almost certainly general collateral, but I cannot confirm there is no stress in the lending market. |
| **Implied volatility skew in vol terms (25-delta put vs call IV)** — AlphaQuery 503, Barchart volatility page JS-rendered [16][50] | I inferred skew from option *prices* rather than fitted IVs. My conclusion that near-dated skew is roughly symmetric (contradicting triage) rests on mid-price symmetry, which is a reasonable but not airtight proxy. |
| **IV rank as-of timestamp** — Barchart shows IV Rank 71.19% with no date stamp [16] | An IV rank without a date is exactly the sort of stale figure the brief warns about. Cross-checked against my own realised-vol calc (20d 23.8%, 60d 35.9%) which is consistent with elevated but not extreme IV. |
| **Google Trends / web traffic / app data / job postings / reviews** [41] | Placer.ai (via Jefferies) is my only alt-data source and it is second-hand through a sell-side note. A second independent alt-data read on July/August traffic would materially raise confidence in the single most important secondary metric. |
| **Current-week social sentiment trend (7/14/30-day)** [27][40] | The "extremely bullish, +1,100% messages" datapoint is from late May, not this week. I have direction (bullish) but no trend. |
| **DLTR-specific tariff refund quantification** [25] | The industry-wide numbers are well sourced ($165bn ordered, $128.68bn in processing) but no company-specific DLTR figure exists in the public record. This is the largest unquantified swing factor in the print. |
| **Q2 FY26 diluted share count** | I used ~193m as an interpolation between the reported 197.4m (Q1 FY26) and continued buyback. This is my estimate, not a sourced figure, and it feeds my EPS bridge. |
| **Realised-move dataset provenance** | Prices come from the Yahoo chart API [2]; the eight earnings dates are independently confirmed against SEC 10-Q/10-K filing dates [10], so the mapping is solid, but I could not obtain a vendor-published earnings-move table to cross-check my arithmetic. |
| **Domains unreachable** | OptionSlam full history (paywalled beyond one quarter) [14]; Zacks detailed-estimates (bot wall) [51]; AlphaQuery (503); MarketChameleon (503); OpenInsider (503); StocksEarning (403); Fintel (403); Yahoo options endpoint (crumb-protected). Yahoo's *chart* endpoint and the **Nasdaq options-chain API** were reachable and did most of the quantitative work. |

---

## 12. Sources

1. [Dollar Tree 8-K Ex-99.1, "Dollar Tree, Inc. to Host Second Quarter Earnings Conference Call," filed 2026-08-06](https://www.sec.gov/Archives/edgar/data/0000935703/000093570326000101/ex991q2-26earningscallanno.htm) — **event confirmation**: date 2026-08-27, before market open, quarter ended 2026-08-01, 08:00 ET call, Creedon/Glendinning.
2. [Yahoo Finance chart API, DLTR daily closes, 3-year range](https://query1.finance.yahoo.com/v8/finance/chart/DLTR?range=3y&interval=1d) — spot $134.48 at 2026-08-25 20:00Z, prior close $136.75, day range, volume, 52-week range, and all historical closes used to compute earnings-day moves, run-ups and realised volatility.
3. [Barchart, "Dear Dollar Tree Stock Fans, Mark Your Calendars for August 27"](https://www.barchart.com/story/news/4030075/dear-dollar-tree-stock-fans-mark-your-calendars-for-august-27) — price $134.48 (−1.66%), market cap $26.28bn, YTD +8.4%, 1yr +19.3%, consensus target $130.25, street high $170, Q1 beat detail.
4. [StockAnalysis.com — DLTR overview and forecast pages](https://stockanalysis.com/stocks/dltr/forecast/) — 192.17m shares out, market cap $25.84bn, P/E 21.61, forward P/E 18.56, beta 0.67, rating split 6/4/14/2/1 across 27 analysts, consensus target $131.68 (range $98–$170), forward revenue $20.67bn and adjusted EPS $7.04 for the fiscal year ending Jan-2027 (21 analysts).
5. [Dollar Tree 8-K Ex-99.1, Q1 FY2026 earnings press release, filed 2026-05-28](https://www.sec.gov/Archives/edgar/data/0000935703/000093570326000064/ex991q1-26earningspressrel.htm) — Q1 net sales $5.0bn (+7.2%), comps +3.5% (traffic −1.0%, ticket +4.5%), GM +120bps, SG&A 27.8%, op margin 9.5%, GAAP EPS $1.76, adj EPS $1.74, 197.4m diluted shares, $595m/5.5m shares repurchased, cash $1.0bn, 9,382 stores, ~5,900 multi-price, Q2 guide ($4.8–4.9bn, +2.5–3.5% comps, $1.00–1.15 adj EPS), FY26 guide ($20.5–20.7bn, +3–4% comps, $6.70–7.10 adj EPS, ~400 openings / 75 closings), tariff and Family Dollar TSA references.
6. [Blockonomi / Investing.com — Jefferies upgrade on Placer.ai traffic data, 2026-08-18/19](https://blockonomi.com/dollar-tree-dltr-stock-climbs-on-jefferies-upgrade-as-july-traffic-surges-4-5/) — Underperform→Hold, PT $85→$135; Q2 traffic +1.4%, **July +4.5%** on Placer rolling three-month visits; modelled +0.8% traffic comp, +3.4% total comp (ticket +2.6%); Q2 EPS estimate $1.15 vs Street $1.12.
7. [NBC News — "At Walmart, billions in tariff refunds soften the blow from slower sales growth," 2026-08-20](https://www.nbcnews.com/business/consumer/walmart-earnings-tariffs-sales-growth-rcna593450) — Walmart US comps +2.6% vs +3.8% expected, slowest in six years; ~$3bn tariff refunds; $4 gas psychological threshold.
8. [Fortune — "Facing weary customers, Walmart will use its nearly $3 billion in tariff refunds to lower prices," 2026-08-20](https://fortune.com/2026/08/20/walmart-tariff-refunds-prices/) — 11,000+ rollbacks vs ~7,200 prior quarter.
9. [Simply Wall St — "Dollar Tree Stock And 2 Consumer Names Facing New Section 301 Tariff Pressure," 2026-07-28](https://simplywall.st/stocks/us/consumer-retailing/nasdaq-dltr/dollar-tree/news/dollar-tree-stock-and-2-consumer-names-facing-new-section-30) — new Section 301 tariffs 10–12.5% on 60 economies; **DLTR ~$20m/month, ~$70m/quarter COGS exposure pre-mitigation**; mitigation levers cited.
10. [SEC EDGAR submissions feed, CIK 0000935703](https://data.sec.gov/submissions/CIK0000935703.json) — full filing history used to (a) confirm the eight historical earnings dates via 10-Q/10-K filing dates, (b) establish 8-K cadence (8 filings YTD 2026, none since 2026-08-06), (c) confirm absence of Item 4.02/5.02, (d) enumerate Form 4 activity.
11. [Nasdaq options-chain API, DLTR, expiries 2026-08-28 through 2026-09-18](https://api.nasdaq.com/api/quote/DLTR/option-chain?assetclass=stocks&limit=500&fromdate=2026-08-26&todate=2026-09-20&excode=oprac&callput=callput&money=all&type=all) — full bid/ask/volume/OI by strike; source of my ATM straddle implied move (9.16%), term structure, skew symmetry check, the 1,524-lot Aug-28 $124 put print, and Sep-18 call OI concentrations.
12. [StockStory via FinancialContent / Yahoo — "Dollar Tree (DLTR) Q2 Earnings: What To Expect," 2026-08-26](https://finance.yahoo.com/markets/stocks/articles/dollar-tree-dltr-q2-earnings-035649469.html) — consensus revenue growth +6.3%, prior-quarter $4.98bn (+7.2%) with gross-margin beat, share price $134.73, average target $131.68, +7.3% one-month move, Target (+5.3% revenue, +3.8% stock) and BJ's (+15.7% revenue, +7.9% stock) read-throughs, "estimates reconfirmed over last 30 days."
13. [SEC Form 4 — Mantle Ridge LP, DLTR, transaction date 2026-06-24, filed 2026-06-25](https://www.sec.gov/Archives/edgar/data/935703/000110465926077658/xslF345X06/tm2618973-2_4seq1.xml) — "Director by deputization"; code C 602,170 shares; **code S 2,230,455 shares at $111.31**; **code J in-kind distribution 10,266,164 shares at $0**; residual holding 210,044.
14. [OptionSlam — DLTR earnings and implied move page](https://www.optionslam.com/earnings/stocks/DLTR) — implied move weekly 9.26% (expiry 2026-08-28), monthly 11.12% (expiry 2026-09-18), 2026-05-28 realised move +17.86% (pre $95.87 → post $113.00, intraday max 19.57%), EVR 3.9/10.
15. [ad-hoc-news — "Dollar Tree stock faces volatile week ahead of August 27 earnings," 2026-08-24](https://www.ad-hoc-news.de/boerse/news/corporate-news/dollar-tree-stock-faces-volatile-week-ahead-of-august-27-earnings/69993085) — published implied move 10.51%, price $131.70 as of 2026-08-24. `snippet_only`-grade secondary; superseded by my live chain calculation.
16. [Barchart — DLTR put/call ratios page](https://www.barchart.com/stocks/quotes/DLTR/put-call-ratios) — put/call volume 1.77 (3,854/2,175), put/call OI 0.62 (31,722/51,479), **IV 51.13%, IV Rank 71.19%**, next earnings 08/27/26 BMO. No as-of stamp on the volatility figures.
17. [Zacks via Yahoo Finance — "Dollar Tree Q2 Earnings Around the Corner"](https://finance.yahoo.com/markets/stocks/articles/dollar-tree-q2-earnings-around-140700360.html) — consensus EPS $1.11 (+44.2% y/y), revenue $4.85bn (+6.3%), consensus unchanged over 30 days, trailing four-quarter average surprise +32.1%, last-quarter surprise +13.7%, BMO reporting confirmation.
18. [ad-hoc-news — "Dollar Tree stock holds above consensus as investors eye Q2 earnings boost"](https://www.ad-hoc-news.de/boerse/news/corporate-news/dollar-tree-stock-holds-above-consensus-as-investors-eye-q2-earnings-boost/69983014) — sell-side same-store-sales expectation raised to **4.0% for DLTR vs 3.0% for DG**.
19. [ad-hoc-news — "Dollar Tree stock gets a fresh analyst upgrade as buyback and earnings expectations build," 2026-08-22](https://www.ad-hoc-news.de/boerse/news/corporate-news/dollar-tree-stock-gets-a-fresh-analyst-upgrade-as-buyback-and-earnings/69985077) — Wall Street Zen Hold→Buy 2026-08-22; consensus target $123.41 vs price $131.48; **Oppenheimer Q2 $1.13 / FY $7.05**; FY midpoint raise of **$0.10–$0.20** expected; $2.5bn authorisation = 10.7% of shares; prior consensus $6.67 vs guide midpoint $6.90.
20. [Dollar Tree 8-K Ex-99.1, Q2 FY2025 earnings press release, filed 2025-09-03](https://www.sec.gov/Archives/edgar/data/935703/000093570325000060/ex991q2-25earningspressrel.htm) — Q2 FY25 comps **+6.5% on traffic +3.0% / ticket +3.4%**; **adjusted diluted EPS $0.77 "including $0.20 of positive impact, relative to expectations, related to tariff timing"**; net sales +12.3%; FY25 outlook.
21. [SEC XBRL companyfacts, CIK 0000935703](https://data.sec.gov/api/xbrl/companyfacts/CIK0000935703.json) — audited/reviewed line items: Q2 FY25 revenue $4,566.8m, gross profit $1,570.1m, operating income $231.0m, GAAP diluted EPS $0.91, diluted shares 207.8m; Q1 FY26 revenue $4,970.5m, operating income $473.3m, GAAP diluted EPS $1.76, diluted shares 197.4m, merchandise inventory $2,470.8m (vs $2,704.0m), cash $1,007.3m, LT debt $2,932.6m, equity $3,507.0m, OCF (continuing) $644.0m, repurchases $585.8m; FY25 revenue $19,395.7m, gross profit $7,050.7m, operating income $1,653.1m, GAAP diluted EPS $6.22, OCF $2,190.7m, repurchases $1,548.0m.
22. [EarningsWhispers — DLTR](https://www.earningswhispers.com/stocks/DLTR) — whisper number fields unpopulated on fetch; **no whisper sourced**.
23. [The Motley Fool — Dollar Tree (DLTR) Q1 2026 Earnings Call Transcript, 2026-05-29](https://www.fool.com/earnings/call-transcripts/2026/05/29/dollar-tree-dltr-q1-2026-earnings-transcript/) — "no tariff refunds are assumed"; refunds to be reinvested in customer value; ~85% of sales at $2 and below; traffic −1.0% (20bps sequential improvement, ~200bps two-year improvement vs Q4); all income cohorts positive comps; corporate SG&A −15% and 70bps leverage to 2.4%; consolidated SG&A reporting from FY2027; FCF $392m; $595m repurchased plus $98m post-quarter; ~8% TTM share reduction, $1.7bn returned; **no future repurchases assumed in guidance**; inventory −9% on sales +7.2%, ~$425m avoided carrying cost; freight moved to shorter-term contracts with higher fuel surcharges; elevated fuel assumed for all of 2026; Glendinning on "tariffs, fuel, freight and just some broader consumer pressure."
24. [Skadden — "Tariff Refund Mechanism Takes Shape After Supreme Court's IEEPA Ruling," 2026](https://www.skadden.com/insights/publications/2026/03/tariff-refund-mechanism-takes-shape) and [Norton Rose Fulbright — "Potential refunds: US Supreme Court overturns IEEPA tariffs"](https://www.nortonrosefulbright.com/en/knowledge/publications/20f2de87/potential-refunds-us-supreme-court-overturns-ieepa-tariffs) — SCOTUS 6–3 ruling 2026-02-20; CIT order to refund ~$165bn; CBP CAPE system; ~$128.68bn accepted for processing as of 2026-07-31; refunds require affirmative filing.
25. [Penn Wharton Budget Model — "Supreme Court Tariff Ruling: IEEPA Revenue and Potential Refunds," 2026-02-20](https://budgetmodel.wharton.upenn.edu/p/2026-02-20-supreme-court-tariff-ruling/) — refund magnitude ~$166bn, ~63% of 2025 customs-duty receipts; 330,000+ importers; statutory interest 6% for corporates.
26. [Fox Business — "Dollar Tree may drop some products if tariffs are implemented"](https://www.foxbusiness.com/economy/dollar-tree-could-drop-some-products-tariffs-enacted) and [Supply Chain Dive — "Dollar Tree prepped for multiple tariff scenarios, CEO says"](https://www.supplychaindive.com/news/dollar-tree-outlines-tariff-contingency-plan/744169/) — ~40% of merchandise imported, vast majority from China (2024 annual report); >90% of first-round tariff cost mitigated; sourcing shifts, spec/size changes, item deletion; multi-price flexibility. China effective rate ~37.5% per [TariffsTool](https://www.tariffstool.com/tariffs-from-china).
27. [Stocktwits / Yahoo Finance — "DLTR Stock: Dollar Tree Wins Dual Wall Street Upgrades As Analysts See Earnings Upside," 2026-07-09](https://finance.yahoo.com/markets/stocks/articles/dltr-stock-dollar-tree-wins-073659647.html) — Raymond James Market Perform→Outperform PT $140; Goldman Sachs Sell→Neutral PT $105→$125; both cite tariff reimbursements, conservative guidance, buybacks; both flag soft traffic as the residual concern; retail sentiment "bullish" on Stocktwits.
28. [Dollar Tree Q4 FY2025 results, reported 2026-03-16](https://corporate.dollartree.com/_assets/_dfdbb82ef530754a17c5b7aea22ca90c/dollartreeinfo/news/2026-03-16_Dollar_Tree_Inc_Reports_Fourth_Quarter_and_Full_303.pdf) — Q4 comps +5.0% (ticket +6.3%, traffic −1.2%), adjusted diluted EPS $2.56 (+21%), revenue $5.5bn (+9%), initial FY2026 guide $6.50–6.90 adj EPS and +3–4% comps.
29. [Yahoo Finance — "Dollar Tree Announces New Change at 630 Stores Throughout the U.S. — And Closes 75"](https://finance.yahoo.com/markets/stocks/articles/dollar-tree-announces-change-630-035447964.html) — ~630 stores converted to or opened as multi-price in Q1, chainwide ~5,900; ~400 openings / 75 closures in FY26; 9,382 stores at Q1-end; no CFO change found.
30. [Dollar Tree 8-K, Item 1.01, term loan credit agreement dated 2026-03-19](https://www.sec.gov/Archives/edgar/data/935703/000093570326000027/dltr-20260319.htm) — $500m term loan facility with Bank of America as agent, SOFR + 1.00%, matures 2029-03-19, no required amortisation.
31. [Dollar Tree press release — "$2.5 Billion Share Repurchase Authorization," 2026-07-02](https://corporate.dollartree.com/news-media/press-releases/detail/308/dollar-tree-inc-announces-2-5-billion-share-repurchase) / [8-K exhibit](https://www.sec.gov/Archives/edgar/data/0000935703/000093570326000075/ex991sharebuybackreplenish.htm) — authorisation replenished to $2.5bn, no expiration; **$500m repurchased in June 2026 in a block trade involving selling stockholders including Mantle Ridge funds**; ~$700m remained before replenishment.
32. [Dollar Tree 8-K, Item 8.01, dated 2026-07-01](https://www.sec.gov/Archives/edgar/data/935703/000093570326000075/dltr-20260701.htm) — Board approved a $2.5bn aggregate share repurchase authorisation.
33. [StockTitan — DLTR Schedule 13D/A, Mantle Ridge, filed 2026-06-25](https://www.stocktitan.net/sec-filings/DLTR/schedule-13d-a-dollar-tree-inc-amended-major-shareholder-report-0d3aa59004d2.html) — Mantle Ridge, MR Cobalt Advisor and Paul C. Hilal each ~0.1% of 192,174,588 shares outstanding as of 2026-05-26; ceased to be >5% beneficial owners; **Hilal remains on the board**; 10,476,108 shares distributed in kind.
34. [ad-hoc-news / TipRanks-sourced analyst action summaries, July–August 2026](https://www.ad-hoc-news.de/boerse/news/corporate-news/dollar-tree-stock-firms-ahead-of-q2-2026-earnings-after-analyst-upgrade/69975639) — Jefferies Underperform→Hold PT $85→$135 (08-18/19); Wells Fargo Overweight PT $145→$155 (08-11); BMO Underperform PT $90→$98 (08-06); Bernstein Market Perform PT $124→$127 (07-31); 27-analyst consensus Hold, target $129.64.
35. [MarketBeat — DLTR short interest](https://www.marketbeat.com/stocks/NASDAQ/DLTR/short-interest) — 7,772,719 shares short at the **2026-08-14 settlement**, **4.35% of float**, **days-to-cover 4.3**, average daily volume 1.91m, **−21.75% vs prior report**.
36. [Fintel — DLTR short-squeeze / borrow rate page](https://fintel.io/ss/us/dltr) — **HTTP 403, unreachable**. Borrow fee recorded as unavailable.
37. [Quiver Quantitative — "Dollar Tree (DLTR) gains as investors position for earnings," 2026-08-24](https://www.quiverquant.com/news/Dollar+Tree+(DLTR)+gains+as+investors+position+for+earnings+and+improving+Wall+Street+sentiment) — +4.1% on 2026-08-24; new institutional stake of 398,171 shares reported; insider trades last 6 months = 1 (Mantle Ridge sale ~$248.3m), 0 purchases; 406 institutional buyers vs 487 sellers in Q2 2026; median target $130.00 across 17 analysts, range $98–$170.
38. [DefenseWorld — "BlackRock Inc. Invests $1.93 Billion in Dollar Tree," 2026-08-20](https://www.defenseworld.net/2026/08/20/blackrock-inc-invests-1-93-billion-in-dollar-tree-inc-dltr.html) — BlackRock 15,926,906 shares / ~$1.926bn / 8.29% ownership; institutional ownership reported ~97.4%.
39. [MarketScreener — DLTR consensus](https://www.marketscreener.com/quote/stock/DOLLAR-TREE-INC-16256753/consensus/) — 27 analysts, consensus Hold, average target $127.32, range $85–$170.
40. [Stocktwits — "DLTR Stock Eyes Best Week In 4 Years"](https://stocktwits.com/news-articles/markets/equity/dltr-stock-eyes-best-week-four-years-price-target-dollar-tree-discount-retailer-earnings/cZgSIITRetg) — retail sentiment moved to "extremely bullish," message volume +1,100% in 24 hours (**late-May 2026 context, not the current week**); message volume +50% y/y, watchers +1.8%.
41. Google Trends for "Dollar Tree", August 2026 — **no sourced series obtained**; recorded as a coverage gap.
42. [GuruFocus — Michael C. Creedon Jr. insider activity](https://www.gurufocus.com/insider/169186/creedon-michael-c-jr) and [StockTitan DLTR Form 4 summaries](https://www.stocktitan.net/sec-filings/DLTR/form-4-dollar-tree-inc-insider-trading-activity-483b57a7c7d5.html) — CEO April 2026 tax-withholding disposition of 10,224 shares plus 44,158 RSU grant; 2026-03-31 PRSU settlement 1,929 shares with 1,687 surrendered at $109.51. A reported Glendinning net purchase of 20,500 shares could **not** be tied to a specific Form 4 and is not relied on.
43. [24/7 Wall St. — "Ross Jumps 8% on 10% Comp Growth, TJX Ticks Up, Macy's Edges Higher," 2026-08-21](https://247wallst.com/investing/2026/08/21/ross-jumps-8-on-10-comp-growth-tjx-ticks-up-macys-edges-higher/) and [TJX 8-K Q2 FY27 press release](https://www.sec.gov/Archives/edgar/data/0000109198/000010919826000045/tjxq2fy27earningspressrele.htm) — TJX comps +4%, pre-tax margin 13.3% (+190bps), above plan; Ross +8% on the day.
44. [Benzinga — "Ross Stores Posts Double Beat in Q2, Raises 2026 Earnings Guidance"](https://www.benzinga.com/markets/earnings/26/08/61344730/ross-stores-posts-double-beat-in-q2-raises-2026-earnings-guidance) — revenue +13%, comps +10%, EPS $2.66 vs $1.95 consensus; FY guide raised to $8.61–8.77 from $7.50–7.74; Q3 comps guided +6–7%.
45. [Invezz — "What do Walmart's and Target's results say about the US consumer?", 2026-08-22](https://invezz.com/news/2026/08/22/what-do-walmarts-and-targets-results-say-about-the-us-consumer/) — Target FY sales guide raised to ~+4% from ~+2%; Walmart traffic up / spend per trip down; Target traffic up / spend per trip flat; growth concentrated in essentials and value retail.
46. [StockTitan — "Dollar General Q2 2026 Earnings Call Set for Aug. 27"](https://www.stocktitan.net/news/DG/dollar-general-corporation-announces-webcast-of-its-second-quarter-bipz3jdcgxs4.html) and [Zacks via Yahoo — DG Q2 preview](https://finance.yahoo.com/markets/stocks/articles/unlocking-q2-potential-dollar-general-131504479.html) — DG reports 2026-08-27, call 09:00 ET; consensus EPS $2.00 (+7.5%), revenue $11.17bn (+4.2%); DG trading mid-$120s on 2026-08-24, consensus Hold, target $130.42.
47. [Bank of America Institute — "The rise of value," 2026-07-15](https://institute.bankofamerica.com/content/dam/economic-insights/consumer-search-for-value.pdf) — K-shaped pattern largely disappeared in 2026; lower-income spending at discount apparel stores growing ~5× faster than higher-income; larger tax refunds and improving labour market supporting the low end; top 10% of households ≈ half of consumer spending, highest on record since 1989.
48. [TradingEconomics — gasoline price](https://tradingeconomics.com/commodity/gasoline) — $3.27/gal on 2026-08-25, −1.63% over the past month, +53.11% y/y.
49. [Finder — US gas prices, 2018 to August 2026](https://www.finder.com/economics/gas-prices) — retail average reported at $4/gal in the second week of August 2026 for the first time. **Conflicts with [48]; both reported.**
50. [AlphaQuery — DLTR 30-day implied volatility](https://www.alphaquery.com/stock/DLTR/volatility-option-statistics/30-day/iv-mean) — **HTTP 503, unreachable.** Recorded as a coverage gap for fitted-IV skew.
51. [Zacks — DLTR detailed earnings estimates](https://www.zacks.com/stock/quote/DLTR/detailed-earning-estimates) — **bot wall, unreachable.** Recorded as a coverage gap for the 7/30/60/90-day consensus revision series.

---

*This is a forecasting exercise over public information. It is research, not investment advice, and must not be presented or relied upon as such. Figures are sourced or explicitly marked unavailable; inferences are labelled as the analyst's own.*
