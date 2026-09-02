# VSXY — Victoria's Secret & Co.

**Event confirmed: YES** — Q2 FY2026 (quarter ended 1 Aug 2026), Thursday 3 September 2026, **BMO**. Press release ~07:30 ET, call 08:30 ET, confirmed from the company's own 13-Aug-2026 announcement [1][2] and corroborated by the exchange calendar feed with `isEarningsDateEstimate: false` [3].

**What this print is about.** VSXY is up **+271% over the last 252 sessions** [3] on a genuine operational turnaround — four consecutive quarters of positive comps, four consecutive large EPS beats, and a Q1 print (2 Jun 2026) that moved the stock **+47.4% in one session**, its largest gain ever [4][5]. The question on 3 September is not whether Q2 was good; the UBS Evidence Lab web-traffic read (+45% YoY in Q2, accelerating) and the company's own beat-every-guide record make a Q2 beat the base case [6]. The question is **whether management raises the full-year guide enough**. Sell-side consensus now sits *above the top end of both the Q2 and the FY2026 company guidance ranges* — FY26 revenue consensus $7.141B vs a $7.030–7.130B guide, FY26 EPS consensus $4.667 vs a $4.35–4.60 guide [3][7]. A beat-and-reiterate is therefore a de-facto guide-down against the Street. Meanwhile the second-largest holder, activist BBRC/Brett Blundy, has sold **exactly 2,500,000 shares** into the post-Q1 rally at $80.03–$90.60, cutting from 13.0% to 9.8% [8][9][10][11], and the closest structural comp, Bath & Body Works, just printed −2.3% sales with a Q3 EPS guide of $0.07–0.12 against a $0.26 consensus [12]. The market is pricing a ~14–15% event move into a stock that is already **−15.8% from its 10-Aug record close** [3].

**A note on the triage rationale.** The starting hint called this a "post-spinoff momentum name (up ~300% over a year)… genuinely binary." The *magnitude* framing is right — up 271% over a year, an implied move near 14.5%, and a realised 47.4% single-session move one quarter ago. The *"post-spinoff"* framing is wrong: VS&Co separated from L Brands in **2021**, five years ago; the ticker change VSCO→VSXY on 2 June 2026 was a branding exercise, not a corporate action [13][14]. And "momentum name into a binary print" understates the setup — the stock has *already given back 16%* into the event, so this is a de-risked momentum name, not an extended one. That materially changes the asymmetry and is reflected below.

---

## 1. Event & anchors

| Item | Value | As-of | Source |
| --- | --- | --- | --- |
| Event date | 2026-09-03 | confirmed | [1][2][3] |
| Session | **bmo** — release ~07:30 ET, call 08:30 ET | confirmed | [1][2] |
| Fiscal period | Q2 FY2026, quarter ended 2026-08-01 | — | [1][3] |
| Date changed / pre-announced? | No. No pre-announcement 8-K as of 2026-09-02; last 8-K (20 Aug, event 18 Aug) was a board appointment | 2026-09-02 | [15][16] |
| Spot | **$84.17** (close) | 2026-09-01 20:00Z | [3][17] |
| Pre-market | $84.50 | 2026-09-02 10:03Z | [3] |
| Market cap | **$6.691bn** (79,491,720 sh × $84.17) | 2026-09-01 | [3][17] |
| Enterprise value | $9.39bn | 2026-09-01 | [3] |
| Event-implied move | **≈14.5%** (range 13.8–15.1%, derived — see method) | 2026-09-01 close | [18], own calc |
| Front-expiry ATM straddle | $13.69 (Sep-18 K=85) = **16.26% of spot**; BS IV **94.2%** | 2026-09-01 close | [18], own calc |
| Second expiry | Oct-16 ATM straddle $17.97, BS IV **76.2%** → term structure **inverted** | 2026-09-01 close | [18], own calc |
| IV rank / percentile | **unavailable** — no IV history source reachable | — | — |
| 21d realised vol | 49.9% · 10d 45.7% · 63d 91.7% (inflated by the 2-Jun +47%) | 2026-09-01 | own calc from [3] |
| Beta | 2.07 | 2026-09-01 | [3] |
| 52-week range | $22.02 – $102.46 | 2026-09-01 | [3][17] |

**Implied-move method (mine, stated so the panel can discount it).** VSXY has **no weekly options** — Yahoo returns only monthly expiries, the first after the event being **2026-09-18**, 16 days out [18]. So the raw front straddle overstates the event. Three estimates:
1. Raw front-expiry ATM straddle / spot = **16.26%**.
2. Conventional 85%-of-straddle heuristic = **13.82%**.
3. Two-expiry variance decomposition (`IV₁²T₁ = σ_base²T₁ + J²`; `IV₂²T₂ = σ_base²T₂ + J²`, Sep-18 vs Oct-16): base vol 62.9%, **event jump J = 15.13%**. Re-running with a put-call-parity-corrected October put (the Oct put last-traded an hour before the close) gives base 68.1%, **J = 14.03%**.

I take **14.5%** as the point estimate. Confidence check: the Sep-18 ATM call and put both last traded at **19:59Z**, i.e. simultaneously at the close, and satisfy put-call parity to within $0.04 (C−P = −0.71 vs theoretical −0.67), so the front straddle is a clean, contemporaneous quote, not stale. Bid/ask and open interest come back as zeros in this feed and are marked unavailable.

### Realised one-day earnings reactions

Reaction sessions derived by matching company-confirmed release dates to close-to-close price history [3]. VS&Co released **AMC with a next-morning 08:00 ET call through FY2024**, then switched to **BMO with an 08:30 ET call from Q1 FY2025 onward** — so the reaction session differs by regime and is noted.

| Quarter | Release | Reaction session | Move | Note |
| --- | --- | --- | --- | --- |
| Q2 FY24 | 2024-08-28 AMC [19] | 2024-08-29 | **−3.70%** | |
| Q3 FY24 | 2024-12-05 AMC [20] | 2024-12-06 | **+11.62%** | |
| Q4 FY24 | 2025-03-05 AMC *(inferred)* | 2025-03-06 | **−8.24%** | contaminated: tariff-shock week, VSCO fell 6 straight sessions |
| Q1 FY25 | 2025-06-11 BMO [21] | 2025-06-11 | **−5.41%** | delayed print after May-2025 cyber incident |
| Q2 FY25 | 2025-08-28 BMO [22] | 2025-08-28 | **−0.48%** | **opened +9.7% at $24.99, closed −0.48%** — documented gap-and-fade at this same seasonal print |
| Q3 FY25 | 2025-12-05 BMO *(inferred)* | 2025-12-05 | **+17.99%** | 12.1m shares, ~3× normal volume; press coverage cites "surged nearly 17%" [23] |
| Q4 FY25 | 2026-03-05 BMO [24] | 2026-03-05 | **−12.16%** | beat on both lines, fell on FY26 guide + tariffs + Adore Me charge [24][25] |
| Q1 FY26 | 2026-06-02 BMO [4] | 2026-06-02 | **+47.44%** | closed $80.06, biggest gain ever, record high [5] |

- **Last 6 quarters:** −8.24, −5.41, −0.48, +17.99, −12.16, +47.44. Mean abs **15.29%**, median abs **10.20%**, max abs **47.44%**. Up/down **2 up / 4 down**.
- **Last 8 quarters:** mean abs **13.38%**, median abs **9.93%**. Up/down **3 up / 5 down**.
- **Read:** the implied 14.5% is *above* the 6-quarter median (10.2%) but *below* the 6-quarter mean (15.3%) — the mean is entirely a function of one +47% observation. Stripping that single print, the last five average 8.9%. Options are pricing something close to a repeat of June. That is a demanding thing to pay for.

---

## 2. The bar

| Metric | Consensus | n | Range | Company guide | Gap |
| --- | --- | --- | --- | --- | --- |
| Q2 FY26 EPS (adj) | **$0.774** | 11 | $0.748 – $0.820 | ~$0.65–0.75 *(from the call, secondary)* [7][26] | Street **above** the top of guide |
| Q2 FY26 revenue | **$1.6198bn** (+11.0% YoY) | 9 | $1.612 – $1.628bn | **$1.590–1.615bn** (+9.0% to +10.7%) [4] | Street **above** the top of guide |
| Q2 FY26 operating income | — | — | — | **$90–100m** vs $55m adj LY [4] | |
| Q3 FY26 EPS | **$0.056** | 11 | −$0.02 – $0.184 | none | fragile, near-breakeven quarter |
| Q3 FY26 revenue | $1.566bn (+6.4%) | 9 | $1.545 – $1.589bn | none | |
| FY26 EPS (adj) | **$4.667** | 11 | $4.50 – $4.899 | **$4.35–4.60** *(from the call, secondary)* [26] | Street **~1.5% above** the top |
| FY26 revenue | **$7.141bn** (+9.0%) | 10 | $7.087 – $7.175bn | **$7.030–7.130bn** [4] | Street **above** the top |
| FY27 EPS | $5.603 | 11 | $5.23 – $6.15 | — | |

All consensus figures: exchange analyst-estimate feed as of 2026-09-01 [3]; Zacks independently marks the Q2 consensus at **$0.77** and revenue **$1.6bn (+11.2%)** [27].

**Estimate revisions (Q2 FY26 EPS):** $0.4122 (90d) → $0.7613 (60d) → $0.7668 (30d) → $0.7716 (7d) → **$0.7743 (now)**. The 90-day jump is the post-Q1 reset, not new information. The genuinely current signal is small and one-directional: **+0.8% over 30d, 1 up-revision, 0 down** [3].

**The more informative revision is Q3, not Q2:** Q3 FY26 EPS has **9 upward revisions and 0 downward in the last 30 days** [3]. The Street has been marking up the *forward* quarter into the print. That is the raised bar.

**What VSXY has to deliver just to hold the stock flat (my inference):**
1. Q2 revenue ≥ ~$1.62bn and adjusted EPS ≥ ~$0.78 — i.e. beat the *Street*, which is already above the top of the company's own guide.
2. Raise FY26 net sales guidance to **at least ~$7.15bn** at the low-to-mid point, since consensus $7.141bn already exceeds the current $7.130bn top end.
3. Raise FY26 adjusted operating income above the current $550–580m so the FY EPS guide clears the $4.667 consensus.
4. Guide Q3 in a way that does not break the $0.056 consensus — a quarter with essentially no margin for error and Fashion Show costs (18 Oct, Los Angeles) landing inside it [28].

**Whisper number: unavailable.** EarningsWhispers returns 404 under both VSCO and VSXY. No credibly published whisper found. Zacks reports an **Earnings ESP of +5.20% with a Zacks Rank #1**, which is a model output rather than a whisper, and is `snippet_only` [27].

**The structural argument that the bar is beatable.** FY guide $7.030–7.130bn minus H1 ($1.560bn actual + $1.590–1.615bn guided = $3.150–3.175bn) implies **H2 net sales of $3.855–3.980bn vs $3.741bn in H2 FY25 = +3.0% to +6.4%** (FY25 revenue $6.553bn, H1 FY25 $2.812bn, both from the XBRL filings [29]). Against Q1 at +15% and a Q2 guide at +9–11%, management's own H2 embeds a sharp deceleration. That is either conservatism to be harvested or a genuine view that the comp gets hard. My inference: mostly conservatism, given they raised the FY guide by $180m of sales and $120m of operating income at the Q1 print [4].

---

## 3. The one metric that matters

**It is not EPS. It is the size of the FY2026 guidance raise — specifically FY net sales and adjusted operating income — with the Q3 revenue/EPS guide as the trap door.**

Justification: consensus FY26 revenue ($7.141bn) and EPS ($4.667) both sit *above the top end* of the guidance management issued on 2 June [3][4]. Arithmetically, reiterating the guide lowers the Street. This company's own history is unambiguous on which line the stock trades: on 5 March 2026 VS&Co **beat** Q4 on both the top and bottom line — adjusted EPS $2.77 vs $2.47–2.51 expected, revenue $2.27bn vs $2.22bn — and the stock fell **−12.16%** on the forward guide, tariffs and the Adore Me charge [24][25]. On 2 June 2026 it beat *and* raised the FY guide by $180m/$120m, and the stock rose **+47.44%** [4][5]. Same company, same CEO, two quarters apart, opposite outcomes, and the discriminating variable was the guide.

**What the market expects for it (my read, from the revision pattern):** the 9 upward Q3 revisions in 30 days and a FY consensus above the guide top imply the Street is already modelling a raise of roughly $30–60m to the FY sales range and a proportionate operating-income raise. To surprise positively, management needs a raise materially larger than that — plausibly FY sales to ~$7.20bn+ — of the kind they delivered in June. To disappoint, they need only reiterate.

**Secondary metric to watch:** Q2 comparable sales. Q1 was **+13%**, the fourth consecutive positive comp [4]. A fifth consecutive positive comp is expected; the debate is double-digit versus high-single-digit. Third: gross margin, where a pre-print estimate of ~38.5% vs 35.6% LY (≈290bps expansion) has been published [30] — Q1 delivered 37.5% (GP $585m on $1,560m [29]).

---

## 4. Fundamentals — what changed, what is at stake

**Q1 FY2026 (quarter ended 2026-05-02), reported 2 June 2026** [4][29]:

| | Q1 FY26 | Q1 FY25 | Δ |
| --- | --- | --- | --- |
| Net sales | $1,560m | $1,353m | **+15%** (guide was $1,490–1,525m) |
| Total comparable sales | +13% | — | 4th consecutive positive quarter |
| Gross profit | $585m (37.5%) | — | driven by regular-price selling, less promotion |
| Operating income | $76m | $20m | |
| Adjusted operating income | **$80m** | $32m | guide was **$32–42m** — beat by ~$40m |
| Net income | $48m | −$2m | |
| Diluted EPS | $0.56 | −$0.02 | |
| Adjusted EPS | **$0.60** | $0.09 | guide was **$0.20–0.30** |

**Channel mix, Q1 FY26** [4]: Stores–North America $802.8m (+11.3%); Direct $469.4m (+8.4%); **International $287.4m (+44.9%)**. International is the fastest-growing leg — management attributes it largely to China, with partner-operated locations guided to 604–622 stores by year-end and 67 China stores currently [31]. Note the asymmetry: Direct (+8.4%) grew *slowest* despite UBS measuring website visits +45% YoY — traffic is not converting one-for-one into digital revenue, which is the single most important caveat on the bullish alt-data read.

**Balance sheet and cash (from XBRL, 10-Q for period ended 2026-05-02)** [29]:
- Cash **$207m** (vs $518m at FY25 year-end, $138m a year earlier).
- Inventory **$1,098m** vs $1,043m LY = **+5.3% YoY against +15% sales growth**. Management guided inventory up high-single-digits and came in at +5% [32]. This is the cleanest fundamental signal in the file: inventory is growing at a third the rate of sales, which is what makes the gross-margin expansion durable rather than borrowed.
- Long-term debt $986m; non-current operating lease liability $1,597m; total debt (incl. leases) $2.851bn; equity $790m; debt/equity 337% [3][29].
- Q1 operating cash flow **−$137m** (vs −$150m LY) — Q1 is seasonally negative. TTM operating cash flow $512m, FCF $242m [3].
- Capex $54m in Q1; FY25 capex $187m [29].

**Capital return:** repurchased **2.2m shares for $100m at an average $45.27** during Q1 FY26 — the first buyback since FY23 ($0 repurchased in FY24 and FY25) [4][29]. **$150m remains** on the March-2024 $250m authorisation [4]. At $84.17 that residual buys only ~1.8m shares. My inference: the $45.27 average is now 46% below spot, which is a good look for management but also means the remaining authorisation has far less support value, and an authorisation *increase* is a plausible sweetener on this call.

**Tariffs:** FY26 assumes ~$160m gross incremental tariff cost mitigated to ~**$40m net**, via vendor cost work, sourcing diversification, freight mix and pricing [24]. Q1 carried ~175bps of tariff pressure in gross margin, with a lesser impact expected in Q2 and less again in H2 as the company laps [32]. Of the ~$40m Q1 operating-income beat, management attributed ~$25m to the business and ~$14–15m to tariffs coming in better than assumed; of the $120m FY operating-income raise, ~$55m was base business and ~$65m the tariff assumption change [32]. **This is a meaningful quality-of-beat caveat**: over half the FY raise was a tariff-assumption revision, not demand.

**Portfolio cleanup:** Adore Me's subscription offering was ended and converted to a loyalty model, with a **$120m pre-tax impairment** on Adore Me assets; DailyLook (acquired with Adore Me) is under strategic review as a non-core asset [33][34]. Adore Me has been a drag on operating income [34].

**Footprint:** ~1,420 retail stores in ~70 countries, 30,000+ associates [4].

**What changed since the last print:** BBRC cut its stake by 2.5m shares; the proxy fight ended in a decisive company win; a tenth director was added effective 14 Sep; the Fashion Show was scheduled for 18 Oct in Los Angeles with Gigi Hadid; the stock made a record high at $102.46 on 10 Aug and then fell 16% over six sessions; five sell-side firms raised price targets in August.

---

## 5. Positioning & options

*(All as of 2026-09-01 close unless stated.)*

**Implied vol and term structure** — derived by me from option last prices [18]:
- Sep-18 ATM (K=85): **94.2%** IV, straddle $13.69.
- Oct-16 ATM (K=85): **76.2%** IV, straddle $17.97.
- **Inverted by ~18 vol points** — a clean event bid in the front month.
- Front IV (94%) sits roughly at 63-day realised (91.7%) but at **1.9× the 21-day realised (49.9%)**. My inference: options are priced for a June repeat, and the post-event vol crush is likely to be severe regardless of direction.

**Skew — essentially flat, which is the most interesting single observation in this section.** Sep-18 IVs from my own Black-Scholes on last prices [18]: P60 94.2%, P65 93.8%, P70 96.1%, P75 94.7%, P80 95.4%, C85 93.9%, C90 93.6%, C95 89.9%, C100 92.6%, C105 92.1%, C110 93.5%. There is a marginal put premium (P80 95.4% vs C95 89.9%) and **no meaningful smirk in either direction**. Read: the market is pricing a large, roughly *symmetric* binary. It is not positioned for a crash and it is not positioned for a squeeze. That is unusual for a name up 271% in a year, and it argues that the consensus view genuinely is "coin flip, big move."

**Volume-based put/call (2026-09-01)** [18]: Sep-18 353 calls / 491 puts = **1.39**; Oct-16 88/131 = 1.49; Dec-18 98/90 = 0.92; Jan-27 201/97 = 0.48. **Total across expiries 740 calls / 809 puts = 1.09.** Near-dated flow is put-heavy (hedging into the event); longer-dated flow is call-heavy. Open interest is **unavailable** — the feed returns zeros across every strike.

**Short interest** [3][35]:

| Settlement | Shares short | Change | % float | Days to cover |
| --- | --- | --- | --- | --- |
| **2026-08-14** | **10,170,180** | −7.2% | **12.9%** | **6.48** |
| 2026-07-31 | 10,959,867 | −0.2% | 13.9% | 6.14 |
| 2026-07-15 | 10,980,127 | −0.6% | 13.9% | 7.30 |
| 2026-06-30 | 11,041,019 | −6.1% | 14.0% | 4.96 |
| 2026-06-15 | 11,762,359 | −12.6% | 14.9% | 3.28 |

The exchange statistics feed independently confirms 10,170,180 shares short at the 2026-08-14 settlement, prior month 10,980,127, short ratio **6.06**, but computes **17.58% of float** [3] against MarketBeat's 12.9% [35] — the two use different float definitions. Float is 70,695,166 shares [3], which gives 14.4% on a straight division. **Whichever denominator you take, this is a heavily shorted stock with ~6 days to cover into a 14.5%-implied event.**

**Ownership crowding:** institutions hold **109.8%** of shares outstanding across 581 holders (>100% is the signature of heavy short-driven rehypothecation), insiders 10.49% [3]. BBRC still holds 7,810,631 shares (9.8%) [11].

**Borrow fee / hard-to-borrow status: unavailable.** No source reachable. This matters — a 12.9–17.6% short interest that is *cheap* to borrow is a different animal from one that is expensive, and the distinction bears directly on squeeze risk.

**Run-in to the print** [3]:
- −1.45% (1 session) · −3.39% (5) · +0.08% (10) · **−5.09% (21)** · +55.01% (63) · **+271.28% (252)**.
- Record close **$99.97 on 2026-08-10**; spot is **−15.8%** from that. Intraday 52-week high $102.46, same day.
- Six consecutive down sessions through 17 Aug cumulatively −16%, erasing ~$1.3bn of market value, with no company-specific news identified as the cause; contemporaneous coverage attributed it to profit-taking and softer apparel-retail sentiment rather than a fundamental break [36].
- Reversal on 26 Aug: **+3.79%** ($87.36 → $90.79) alongside the whole apparel group on Abercrombie's strong print [37].

**How crowded is the trade?** My read: **less crowded than the triage rationale assumes.** The name is retail-favoured and momentum-owned, but it has already surrendered 16% into the event, short interest is large and only slowly declining, skew is flat, and the largest informed holder has been the marginal seller for three months. This is not a stock sitting on its highs with everybody long. The right characterisation is "a crowded *narrative* that has already been partially de-risked in price."

---

## 6. Sentiment & alt-data

**Alt-data — UBS Evidence Lab, published 18 Aug 2026 with the PT raise to $95 (Neutral maintained)** [6]. This is the highest-quality forward read available on the actual quarter:
- **Total visits to the Victoria's Secret website grew +45% YoY in Q2 FY2026**, an acceleration of **675bps QoQ**.
- **Discount factor fell 85bps YoY** — corroborating less promotional intensity, which is the mechanism behind the gross-margin story.
- **US Google searches +2% YoY in Q2, decelerating from +13% in Q1.**
- UBS **raised FY2026–2028 EPS estimates 5–7% and explicitly forecasts a Q2 beat**, while keeping Neutral on valuation.

My inference: this is a genuinely mixed alt-data signal that is being read too bullishly. Web visits and discounting point to a strong quarter *already delivered*. The search deceleration from +13% to +2% is a top-of-funnel measure and points to the *forward* quarters — precisely the line (Q3/H2 guide) the print will trade on. Note also that Q1's +45%-type traffic strength coincided with Direct revenue up only +8.4% [4], so traffic-to-revenue conversion is weak.

**Analyst ratings and drift** [3]:

| Period | Strong Buy | Buy | Hold | Sell |
| --- | --- | --- | --- | --- |
| Now (0m) | 3 | 3 | **5** | 0 |
| −1m | 3 | 3 | 5 | 0 |
| −2m | 2 | 3 | 5 | 0 |
| −3m | 2 | **5** | 3 | 0 |

The Street has drifted **toward Hold** over three months — the Q1 blowout triggered *downgrades* on valuation (**UBS Buy→Neutral and Jefferies Buy→Hold, both 3 June 2026**) rather than upgrades [3][38]. Recommendation mean 2.18 ("buy" bucket, but weakly).

**Price-target drift is strongly upward and is running ahead of ratings:**
- Mean **$94.60**, median **$97.00**, high **$110**, low **$73** (n=10) [3].
- TD Cowen $75 → **$80**, Hold (18 Aug) [39]
- UBS $90 → **$95**, Neutral (18 Aug) [6]
- Telsey Advisory $90 → **$100**, Outperform (27 Aug) [40]
- BofA $95 → **$107**, Buy (Aug) [41]
- JPMorgan $88 → **$110**, Overweight (Aug/28 Jul) [3][41]

Mean PT $94.60 is **+12.4% above spot** — the sell-side is, on average, positioned for the stock to be higher after this print.

**Retail and social:** Stocktwits sentiment ran **bullish with "extremely high" message volume** around the June print, with retail traders framing the name as "war proof, tariff proof, recession proof" [42]. A GLP-1 narrative — weight-loss drugs driving bra re-fits and replacement demand — has become part of the retail bull case [43]. **This colour is from June 2026 and I could not source a current 7/14/30-day social trend**; treat it as stale context, not as positioning evidence. Retail tone was demonstrably euphoric at the highs; whether it survived the 16% August drawdown is unknown.

**Catalyst calendar beyond the print:** the 2026 Victoria's Secret Fashion Show is confirmed for **Sunday 18 October, in Los Angeles, with Gigi Hadid returning** [28]. The 2025 show was explicitly credited by management with driving brand awareness (streaming views +60%, +9m social followers) and preceded the +17.99% Q3 FY25 reaction [23]. Its costs land in Q3 — relevant to a quarter with a $0.056 consensus.

---

## 7. Forensics

**The dominant fact: the activist is selling into strength, and has been for three months.** From the Schedule 13D/A chain and the corresponding Form 4s [8][9][10][11][44][45][46]:

| Date | Shares sold | Price | Holding after | % out |
| --- | --- | --- | --- | --- |
| — (baseline 2026-05-04) | — | — | 10,310,631 | **13.0%** |
| 2026-06-02 | 1,107,672 | $80.11 wtd avg ($80.00–80.69) | | |
| 2026-06-04 | 27,758 | $80.03 wtd avg ($80.00–80.19) | 9,175,201 | **11.6%** |
| 2026-06-26 | 276,171 | $88.50 | 8,899,030 | |
| 2026-07-22 | 289,479 | $88.89 | 8,609,551 | |
| 2026-07-28 | 718,007 / 79,122 / 1,791 | $89.08 / $89.76 / $90.60 | 7,810,631 | **9.8%** |
| **Total** | **2,500,000** | $80.03–$90.60 | | **−320bps** |

Observations that matter:
- The very first tranche was sold **on the day of the +47% Q1 print**, into the spike, at $80.11 — 1.1m shares.
- The Form 4s carry **no 10b5-1 plan designation** in the ownership XML; the disposals are reported as open-market sales (code S) by a 10%+ beneficial owner. Treat as **discretionary**, not scheduled [44][45][46].
- BBRC has now crossed **below the 10% Section 16 threshold**. Its future dispositions will surface via 13D/A amendments rather than prompt Form 4s, so the *granularity* of the disclosure degrades from here. My inference: this raises, not lowers, the residual overhang risk on 7.81m remaining shares (≈9.8%, or roughly 5 days of average volume).
- Timing context: BBRC ran a "vote no" campaign against Chair Donna James and director Mariam Naficy, **lost decisively** at the 11 June annual meeting (James 54,925,752 for vs 10,800,993 against — ~83.5% of votes cast, and reported as >99% excluding BBRC's own shares), with all nine nominees elected, say-on-pay approved 54,394,913 to 11,238,067, and Ernst & Young ratified 66,826,966 to 80,677 [15][47][48]. The selling accelerated *after* the loss. The plainest reading is an activist monetising a won trade after losing a governance fight — not a fundamental signal. But it is the most informed seller in the register, and it is selling.

**Company insiders:** no discretionary open-market selling found. The only insider Form 4 in the window is CMO **Elizabeth Preis, 5,614 shares on 2026-06-02 at $80.06 under transaction code F** — shares withheld for tax on vesting, not a sale [49]. Director **Mariam Naficy** filed a Form 144 on 2026-06-17 for **1,317 shares** through a revocable trust — de minimis, and she was not renominated to the board [50]. Eight Form 4s dated 2026-06-11 are the annual director equity grants following the meeting [15].

**Departures:** Mariam Naficy left the board (not renominated) amid the proxy contest [51]. No CEO/CFO/auditor turnover. Hillary Super has been CEO since September 2024; Scott Sekella has been CFOO since August 2025 [52]. **Ernst & Young ratified 2026-06-11 with 99.8% of votes cast** — no auditor issue, no restatement found [15].

**8-K cadence: normal and uneventful.** Since April 2026: 2026-05-11 (proxy-related), 2026-05-21 (ticker change), 2026-06-02 (Q1 results), 2026-06-11 (annual meeting results), 2026-08-20 (**board expanded from nine to ten, Gerri Martin-Flickinger appointed independent director and Audit Committee member effective 2026-09-14**) [15][16]. **No pre-announcement, no preliminary-results 8-K, no guidance update between 2 June and 2 September.** Worth noting because this company *does* pre-announce when it has to — it issued preliminary Q1 FY25 results during the May-2025 cyber incident [21]. Its silence here is mildly informative: nothing has gone materially wrong enough to require disclosure.

**Filing-language / tone:** the Q1 FY26 release headline leads with three affirmative bullets (sales +15% exceeding guidance; operating income increase; FY guidance raised) and the CEO quote is unusually declarative — "very strong start," "remain confident" [4]. That is a confident-tone filing. There is no hedging language shift I can identify between the Q4 FY25 and Q1 FY26 releases beyond the tariff paragraph.

---

## 8. Macro & peer read-through

**Peers that have already reported this Q2 cycle:**

| Peer | Result | Stock reaction | Read for VSXY |
| --- | --- | --- | --- |
| **Abercrombie & Fitch** (26 Aug) | Record Q2 net sales **$1.27bn**, EPS **$4.17**, op margin ~20%, **raised FY outlook**, 15th consecutive quarter of top-line growth [37][53] | Lifted the entire apparel group; **VSXY +3.79% that session** [3][37] | **Positive.** Brand-led specialty apparel with pricing power is working. Closest analogue to VSXY's own thesis. |
| **Urban Outfitters** (26 Aug) | Record Q2 net sales **$1.66bn (+10.4%)**, net income $240.7m; but **EPS $1.72 vs $1.73 consensus — a 1c miss** [54][55] | Sharp regular-session gain, then **after-hours pullback** on profit-taking [37] | **Cautionary.** A record quarter with a one-cent miss still got sold. The market is not paying for "good" this cycle. |
| **Bath & Body Works** (26 Aug) | Net sales **$1,514m, −2.3% YoY**; adj EPS $0.62 but only **$0.31 excluding ~$80m of tariff refunds**; FY sales guided **−4% to −2.5%**; **Q3 adj EPS guide $0.07–0.12 vs $0.26 consensus** [12][56] | — | **Most negative read in the file.** BBWI is VSXY's structural sibling — same L Brands lineage, same mall footprint, overlapping beauty category, similar customer. It is shrinking while VSXY compounds, and it just guided Q3 60%+ below consensus. Either VSXY is taking genuine share (bullish, and consistent with its comps) or the mall/beauty channel is deteriorating in a way VSXY has yet to show (bearish). |
| **Gap** | −16% YTD, trading 27.3% below its Feb-2026 52-week high of $29.13 [37] | — | Negative for the mid-market mall cohort. |
| **PVH** | Reports **2026-09-02 AMC** — same window as this dossier | — | Wholesale apparel read-through lands hours before VSXY's release. Watch it. |
| **American Eagle / Aerie** | Reports **2026-09-09 AMC**, i.e. *after* VSXY [57][58]. Q1 FY26: record revenue $1.2bn, **Aerie comps +25%** [59] | — | Aerie is the direct intimates share-taker. Its +25% Q1 comp says the *category* is strong, not just VSXY. Supports the bull case; also means VSXY's comp is not uncontested. |

**Sector/factor regime (my read):** the August tape rewarded brand-led specialty apparel with margin expansion (ANF) and punished anything with a blemish (URBN's 1c miss) or structural decline (BBWI, GAP). VSXY sits in the first bucket on fundamentals and the second on valuation. Factor-wise this is a high-beta (2.07), high-momentum, heavily-shorted small/mid-cap — the kind of exposure that moves violently on both idiosyncratic news and any momentum-factor unwind.

**Rate / FX / commodity sensitivity:** the material sensitivity is **tariffs**, not rates or FX — ~$160m gross / ~$40m net FY26 incremental cost, with the headwind decaying through H2 as the company laps [24][32]. FX matters increasingly given International grew 44.9% and is the fastest leg [4]. Debt is $986m long-term against $207m cash [29], so rates matter modestly to interest expense but the company is not levered in a way that makes rates the swing factor.

**Consumer backdrop:** the read is mixed and I am flagging it as the weakest-sourced part of this section. Coresight's August 2026 outlook forecasts US retail sales growth above 4% through year-end [60]; apparel has been among the leading contributing categories in recent back-to-school months, while tariff-driven price increases and a softening labour market are cited as constraints on real volumes [60][61]. I could not cleanly separate 2025 from 2026 data points in the available sources and have therefore leaned on this only lightly.

---

## 9. Bull case / bear case / base case

**Bull case (my estimate ~35% likelihood).** VS&Co has beaten its own operating-income guidance by ~$40m in the most recent quarter and has beaten consensus EPS four quarters running by +164%, +54%, +10% and +90% [3][4]. UBS Evidence Lab measured website visits **+45% YoY in Q2, accelerating 675bps QoQ**, with discounting down 85bps — a direct, independent read on the quarter that has just closed, and UBS raised FY26–28 EPS 5–7% and explicitly forecast a beat [6]. Inventory up only 5% against sales up 15% means the margin expansion is real, not borrowed from future markdowns [4][32]. Management's own FY guide embeds only **+3.0% to +6.4% H2 growth** against +15% Q1 and a +9–11% Q2 guide (my arithmetic from [4][29]) — a conservatism reservoir they have twice chosen to release. Positioning is favourable in a way the narrative does not reflect: the stock is **−15.8% from its 10 Aug record close** [3], short interest is **10.17m shares / ~6 days to cover** at the 14 Aug settlement [3][35], and skew is flat with no crash bid [18]. Sell-side mean PT $94.60 is 12.4% above spot [3]. A June-style beat-and-raise into that setup produces a violent upside move; the base rate for this company's raises is +17.99% (Dec-25) and +47.44% (Jun-26).

**Bear case (my estimate ~40% likelihood).** The Street is already **above the top end of both the Q2 and the FY26 guidance ranges** — consensus revenue $1.6198bn vs a $1.590–1.615bn Q2 guide, FY consensus $7.141bn vs a $7.030–7.130bn guide, FY EPS $4.667 vs a $4.35–4.60 guide [3][4][26]. Arithmetically, a beat-and-reiterate *lowers* numbers, and **9 upward Q3 revisions in the last 30 days** [3] mean the forward quarter's bar has been raised into the print on a quarter whose consensus EPS is only **$0.056 with a low estimate of −$0.02**. This company has already demonstrated it will fall hard on exactly that mechanism: on 5 March 2026 it beat Q4 on both lines and fell **−12.16%** on the guide [24][25]. And on 28 August 2025 — the equivalent seasonal print — it opened **+9.7% at $24.99 and closed −0.48%** [3], a documented gap-and-fade. The most informed holder is a seller: BBRC has disposed of **exactly 2,500,000 shares** at $80.03–$90.60 across four discretionary tranches since the Q1 print, cutting 13.0% → 9.8%, and retains 7.81m shares of overhang with degraded disclosure now that it is below the Section 16 threshold [8][9][10][11][44][45][46]. Sibling **Bath & Body Works** just printed −2.3% sales and guided Q3 EPS **$0.07–0.12 against a $0.26 consensus** [12]. UBS's own search data shows top-of-funnel demand decelerating from +13% to +2% YoY [6]. The Street has been drifting to Hold (5 of 11) with the two most recent rating changes both **downgrades** on valuation [3]. At 18× FY26 consensus EPS and ~14× EV/EBITDA after +271% in a year, there is no valuation cushion.

**Base case (my estimate ~25% likelihood, and the modal single outcome).** Q2 comes in modestly above the Street on revenue and EPS — call it $1.63–1.65bn and $0.82–0.90 — a fifth consecutive positive comp in the high single digits to low teens, and gross margin near or above the ~38.5% pre-print estimate [30]. Management raises the FY sales guide to roughly $7.15–7.22bn and adjusted operating income to roughly $580–620m — a real raise, but one the Street has largely pre-empted. Q3 is guided conservatively because the Fashion Show cost lands there. The stock moves less than the 14.5% implied, vol collapses from 94% to the 50s, and both straddle buyers and the "binary" framing lose. This is the outcome the flat skew is quietly pricing and it is the one nobody writes a thesis about.

**My preliminary read: direction score +12, probability of an up move 55%, conviction Low.** The fundamental momentum, the de-risked 16% drawdown into the event, the ~6-day-to-cover short base and the conservatism in the H2 guide tilt me modestly long. The "Street above guidance" bar, the BBRC overhang, the BBWI read-across and this stock's own 2-up/4-down record over the last six prints keep the tilt small. Note explicitly that the *historical base rate is against me*: 2 of the last 6 and 3 of the last 8 reactions were positive. I am overriding that base rate on the strength of the Evidence Lab traffic read and the H2 guidance arithmetic, and if the panel disagrees with either of those two inputs, the correct answer is closer to neutral or negative.

---

## 10. What would flip the consensus view

The consensus view — held by the sell-side (mean PT $94.60, 12.4% above spot), by retail, and implicitly by me — is **"the turnaround is real, they beat, they raise, the stock works."** The single most credible reversal is not a Q2 miss. It is this:

> **Management delivers a strong Q2 and then reiterates rather than raises the FY26 guide, citing H2 caution — promotional environment, tariff timing, Fashion Show costs, or a tougher lap — and guides Q3 revenue at or below the $1.566bn consensus with EPS below $0.056.**

That is credible because: (a) the FY guide as it stands already implies only +3.0–6.4% H2 growth, so management has *already told you* they are cautious on H2 [4][29]; (b) they raised the FY guide only three months ago by $180m/$120m, of which ~$65m of the operating-income raise was a tariff-assumption change rather than demand [32] — a second raise of similar size requires genuine demand upside, not another assumption revision; (c) the closest structural comp just guided its own Q3 EPS ~60% below consensus [12]; (d) this exact mechanism produced −12.16% on 5 March 2026 after a clean beat [24][25]; and (e) the Street has raised Q3 nine times in 30 days into the print [3], so there is no cushion. If that happens, the flat skew means put buyers have not paid up for it, and the downside gap could exceed the 14.5% implied.

**The mirror-image flip:** a **buyback authorisation increase** announced alongside the print. The current $250m authorisation has only $150m left, the company has $207m cash and just resumed repurchasing after two years of zero [4][29], and an activist holding 9.8% has been the marginal seller — a larger authorisation would absorb exactly that overhang. It is not in any estimate I can find, and it would reframe the BBRC sales from "smart money leaving" to "company buying its float back at a discount."

**Two lower-probability flips worth naming:** (1) BBRC files a 13D/A disclosing either a further large sale or, conversely, a settlement/standstill — either would move the stock independent of results; (2) evidence in the Direct channel that the +45% web traffic did *not* convert (Direct grew only +8.4% in Q1 despite similar traffic strength [4][6]), which would discredit the single best piece of alt-data underpinning the bull case.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **IV rank / IV percentile** | No IV-history source reachable. I can say the front IV is 94.2% and 1.9× 21-day realised, but not where 94% sits in VSXY's own distribution. Without it, "is the 14.5% implied move rich or cheap versus this name's own history" is only answerable against *realised* moves, not against *implied* ones. |
| **Options open interest** | The feed returns zeros at every strike. I have volume-based put/call (1.09 total, 1.39 front) but no positioning stock. Cannot assess dealer gamma, pin risk, or whether the put-heavy front-month flow is new or closing. |
| **Bid/ask spreads on the option chain** | All zeros. The straddle is built from last prices. They pass a put-call-parity check to $0.04 and both legs traded at 19:59Z, so I believe them — but the implied move carries execution-cost uncertainty I cannot size. |
| **No weekly options exist on VSXY** | The first expiry after the event is 16 days out. Every implied-move figure here is a *decomposition*, not a direct read. My three methods span 13.8–15.1%; a weekly straddle would have collapsed that range. |
| **Borrow fee / hard-to-borrow status** | Unavailable. With 12.9–17.6% of float short and ~6 days to cover, whether the borrow is cheap or expensive materially changes the squeeze probability and the character of any upside move. |
| **Whisper number** | EarningsWhispers 404s under both VSCO and VSXY. No credible published whisper. The Zacks ESP (+5.20%) and Rank (#1) are model outputs, not whispers, and are snippet-sourced. |
| **Current (7/14/30-day) social sentiment trend** | The Stocktwits colour I have is from **June 2026** and predates the 16% August drawdown. I cannot say whether retail tone survived it. Flagged as stale, not current. |
| **Q2 FY26 adjusted-EPS guidance ($0.65–0.75) and FY26 adjusted-EPS guidance ($4.35–4.60)** | **Neither appears in the 8-K press release**, which guides only on net sales and operating income [4]. Both figures come from the earnings call via secondary reporting. They are internally consistent with the operating-income guide (my check: $95m OI − ~$15m interest, 25% tax, 85m shares ≈ $0.71), but they are `snippet_only` and the "Street is above guidance" conclusion on EPS rests on them. The *revenue* version of that conclusion rests on the primary filing and is solid. |
| **Q4 FY24 and Q3 FY25 release dates** | Inferred from the price/volume signature and press coverage, not confirmed from a company source. The Q4 FY24 reaction (−8.24% on 2025-03-06) is additionally contaminated by a six-session macro selloff that week. Both are included in the historical-move series with that caveat. |
| **Institutional 13F positioning changes into the print** | Not sourced beyond the aggregate (109.8% of shares out, 581 holders). Cannot tell whether long-only money added or trimmed during the August drawdown. |
| **Segment-level Q2 expectations** | No published consensus by channel (Stores NA / Direct / International). Given International grew 44.9% in Q1 and Direct only 8.4%, the mix is likely to matter to the reaction, and I have no Street benchmark for it. |
| **Consumer macro data vintage** | The retail-sales sources returned a mix of 2025 and 2026 datapoints that I could not cleanly separate. Section 8's consumer paragraph is deliberately hedged as a result. |
| **Unusual options activity reports** | No provider-sourced UOA found for the run-in. The volume figures in Section 5 are my own aggregation from the raw chain. |

**Domains not reachable in this environment:** `victoriassecretandco.com` (503), `globenewswire.com` (503), `benzinga.com` (403), `stockstory.org` (403), `earningswhispers.com` (404 on both tickers), `easternprogress.com` (429), `marketchameleon.com` (503), `barchart.com` (dynamic content did not render), `stooq.com` (connection reset). SEC EDGAR, the Yahoo Finance JSON APIs, MarketBeat, Investing.com, StockTitan, Trefis and StockAnalysis were all reachable.

---

## 12. Sources

1. Victoria's Secret & Co., "Invites You to Listen to the Second Quarter 2026 Earnings Call" — earnings date 3 Sep 2026, call 08:30 ET, release ~1 hour prior. https://www.victoriassecretandco.com/news-releases/news-release-details/victorias-secret-co-invites-you-listen-second-quarter-2026 *(page 503; content confirmed via [2])*
2. StockTitan mirror of the same company release — verbatim confirmation of date, time and BMO release timing. https://www.stocktitan.net/news/VSXY/victoria-s-secret-co-invites-you-to-listen-to-the-second-quarter-hd1yzbwa19h0.html
3. Yahoo Finance JSON APIs (chart, options, quoteSummary: earningsTrend, recommendationTrend, financialData, defaultKeyStatistics, earningsHistory, calendarEvents, upgradeDowngradeHistory, majorHoldersBreakdown) — spot, market cap, shares, float, price history and all derived returns/realised vol, consensus EPS/revenue and revision trends, analyst counts and ratings, price targets, short interest, institutional/insider ownership, earnings-date confirmation. https://query1.finance.yahoo.com/v8/finance/chart/VSXY?range=3y&interval=1d and https://query1.finance.yahoo.com/v10/finance/quoteSummary/VSXY
4. SEC Form 8-K Ex-99.1, Q1 FY2026 earnings release (2 Jun 2026) — Q1 results, channel detail, buyback, Q2 and FY26 guidance. https://www.sec.gov/Archives/edgar/data/0001856437/000185643726000011/ex991vsxyq12026earningsrel.htm
5. Bloomberg via Yahoo Finance, "Victoria's Secret Climbs to Record High as Chain Outperforms" — +47.44% close at $80.06 on 2 Jun 2026, biggest gain ever. https://finance.yahoo.com/markets/stocks/articles/victoria-secret-climbs-record-high-135153679.html
6. Investing.com, "UBS raises Victoria's Secret stock price target to $95 on strong web traffic" (18 Aug 2026) — UBS Evidence Lab web visits +45% YoY / +675bps QoQ, discount factor −85bps, US Google searches +2% YoY vs +13% in Q1, FY26–28 EPS raised 5–7%, Q2 beat forecast. https://www.investing.com/news/analyst-ratings/ubs-raises-victorias-secret-stock-price-target-to-95-on-strong-web-traffic-93CH-4865135
7. Search snippet aggregation of Q2 consensus (Benzinga $0.75; TipRanks $0.60/$1.62bn; StockStory +11% revenue) — corroborating range only; primary consensus taken from [3]. https://www.benzinga.com/quote/VSXY/earnings *(403)*
8. SEC Schedule 13D/A Amendment No. 5, BBRC International (filed 2026-05-04) — 10,310,631 shares, 13.0%; launch of the "vote no" campaign. https://www.sec.gov/Archives/edgar/data/1856437/000121390026051617/primary_doc.xml
9. SEC Schedule 13D/A Amendment No. 6 (filed 2026-06-04) — 9,175,201 shares, 11.6%. https://www.sec.gov/Archives/edgar/data/1856437/000121390026065438/primary_doc.xml
10. SEC Schedule 13D/A Amendment No. 7 (filed 2026-07-29) — 7,810,631 shares, 9.8%. https://www.sec.gov/Archives/edgar/data/1856437/000121390026082834/primary_doc.xml
11. SEC EDGAR submissions index for CIK 0001856437 — full filing cadence, 8-K/Form 4/13D dates. https://data.sec.gov/submissions/CIK0001856437.json
12. Bath & Body Works Q2 2026 results and Q3 guidance (26 Aug 2026) — net sales $1,514m (−2.3%), adj EPS $0.62 incl. ~$80m tariff refunds ($0.31 ex-refund), FY sales −4% to −2.5%, Q3 adj EPS $0.07–0.12 vs $0.26 consensus. https://www.bbwinc.com/media/newsroom/n-bath-body-works-reports-second-quarter-results-exceeding-guidance-and-continued-progress-on-transformation-2026-08-26-065530
13. Victoria's Secret & Co., ticker change VSCO → VSXY effective 2 June 2026, NYSE listing unchanged, same CUSIP. https://www.marketscreener.com/news/victoria-s-secret-co-will-change-its-ticker-to-vsxy-from-vsco-ce7f5dd9df8df327
14. Fortune, "Why Victoria's Secret changed its stock ticker to 'VSXY'" — branding rationale, activist context. https://fortune.com/2026/05/21/victorias-secret-changed-stock-ticker-vsxy-nyse-activists-hillary-super/
15. SEC Form 8-K (filed 2026-06-15, event 2026-06-11), Item 5.07 — full annual-meeting vote tallies for all nine directors, say-on-pay and E&Y ratification. https://www.sec.gov/Archives/edgar/data/1856437/000185643726000015/vsco-20260611.htm
16. SEC Form 8-K (filed 2026-08-20, event 2026-08-18), Item 5.02 — board expanded nine → ten, Gerri Martin-Flickinger appointed independent director / Audit Committee, effective 2026-09-14. https://www.sec.gov/Archives/edgar/data/1856437/000185643726000017/vsco-20260818.htm
17. StockAnalysis.com VSXY overview — $84.17 close as of 1 Sep 2026 16:00 EDT, $6.69bn market cap, 79.49m shares, 52-week range, forward P/E, next earnings date. https://stockanalysis.com/stocks/vsxy/
18. Yahoo Finance options chain, VSXY, expiries 2026-09-18 / 2026-10-16 / 2026-12-18 / 2027-01-15 — ATM straddles, last-trade timestamps, strike-level prices used for my own Black-Scholes IV, skew and put/call volume calculations. https://query1.finance.yahoo.com/v7/finance/options/VSXY?date=1789689600
19. SEC Form 8-K Ex-99.1 / company release, Q2 2024 results (28 Aug 2024, call 08:00 ET 29 Aug 2024) — establishes the AMC-release regime. https://www.victoriassecretandco.com/news-releases/news-release-details/victorias-secret-co-reports-second-quarter-2024-results
20. Nasdaq / company release, Q3 2024 results (5 Dec 2024, call 08:00 ET 6 Dec 2024). https://www.nasdaq.com/press-release/victorias-secret-co-reports-third-quarter-2024-results-2024-12-05
21. Victoria's Secret & Co., preliminary Q1 2025 results and security-incident update; rescheduled Q1 2025 release to 11 June 2025 before market open with an 08:30 ET call — establishes the BMO regime and the pre-announcement precedent. https://www.sec.gov/Archives/edgar/data/0001856437/000185643725000026/ex991vsco632025.htm
22. SEC Form 8-K Ex-99.1, Q2 2025 earnings release (28 Aug 2025) — net sales $1.459bn (+3%), comps +4%, adjusted net income $27m / $0.33 per diluted share. https://www.sec.gov/Archives/edgar/data/1856437/000185643725000037/ex991vscoq22025earningsrel.htm
23. Company release and coverage, Q3 2025 results and FY guidance raise (Dec 2025) — net sales $1.472bn (+9%), FY adj OI raised to $350–375m, stock "surged nearly 17%". https://www.victoriassecretandco.com/news-releases/news-release-details/victorias-secret-co-reports-third-quarter-2025-results-and/
24. SEC Form 8-K Ex-99.1, Q4/FY2025 earnings release (5 Mar 2026) — beat on both lines, initial FY26 guide $6.85–6.95bn / EPS $3.20–3.45, ~$160m gross / ~$40m net tariff assumption. https://www.sec.gov/Archives/edgar/data/1856437/000185643726000002/ex991vscoq42025earningsrel.htm
25. Investing.com, "Victoria's Secret Q4 2025 slides: strong beats, stock slides on outlook" — adj EPS $2.77 vs $2.47 forecast, revenue $2.27bn vs $2.22bn, shares −14.29% premarket to $56.24 on the FY26 guide, asset charges and DailyLook review. https://www.investing.com/news/company-news/victorias-secrets-q4-2025-slides-strong-beats-stock-slides-on-outlook-93CH-4544679
26. Secondary reporting of the Q1 FY26 call guidance not present in the 8-K: Q2 adjusted EPS ~$0.65–0.75 and FY26 adjusted EPS $4.35–4.60 (raised from $3.20–3.45). **`snippet_only`.** https://finance.yahoo.com/markets/stocks/articles/victorias-secret-q1-2026-earnings-113704350.html
27. Zacks via Yahoo Finance — Q2 consensus $0.77 (up 1c in 30 days, +133% YoY), revenue $1.6bn (+11.2%), Earnings ESP +5.20%, Zacks Rank #1. **`snippet_only`.** https://finance.yahoo.com/markets/stocks/articles/vsxy-stock-still-worth-buying-132500137.html
28. Victoria's Secret Fashion Show 2026 — Sunday 18 October, Los Angeles, Gigi Hadid returning. https://www.victoriassecret.com/us/vs/vsinsider/fashion-show/2026-show-location
29. SEC XBRL company facts, CIK 0001856437 — Q1 FY26 and historical revenue, gross profit, operating income, net income, EPS, diluted shares, cash, inventory, long-term debt, lease liabilities, equity, operating cash flow, capex, buybacks. https://data.sec.gov/api/xbrl/companyfacts/CIK0001856437.json
30. Pre-print estimate of Q2 gross margin ~38.5% vs 35.6% LY (≈290bps expansion). **`snippet_only`.** https://www.easternprogress.com/is-vsxy-stock-still-worth-buying-after-its-sharp-rally-in-2026/article_8d3d499b-a970-55e3-a3ad-ab07157e29c3.html
31. International/China detail — Q1 FY26 international sales +45%, mid-teens retail comps, 67 China stores, partner-operated network guided to 604–622 by year-end. https://finance.yahoo.com/markets/stocks/articles/international-expansion-key-victorias-secrets-135700056.html
32. Q1 FY2026 earnings call detail — tariff quantification (~175bps Q1 headwind, $14–15m of the OI beat and ~$65m of the FY raise from tariff assumptions), inventory +5% vs high-single-digit guide, "back half launches" commentary. https://www.marketbeat.com/earnings/reports/2026-6-2-victorias-secret-stock/
33. Customer Experience Dive — Adore Me subscription ended and converted to loyalty; DailyLook strategic review as a non-core asset. https://www.customerexperiencedive.com/news/victorias-secret-ends-adore-me-subscription-strategic-review-daily-look/813985/
34. Retail Dive — "Adore Me weighs on Victoria's Secret operating income"; $120m pre-tax impairment on Adore Me assets. https://www.retaildive.com/news/adore-me-weighs-victorias-secret-operating-income/819450/
35. MarketBeat VSXY short interest history — settlements 2026-06-15 through 2026-08-14, shares short, % float, days to cover. https://www.marketbeat.com/stocks/NYSE/VSXY/short-interest/
36. Trefis, "A 6-Day Losing Streak Has Victoria's Secret Stock Down 16%" (19 Aug 2026) — ~$1.3bn of market value erased, no stated cause, P/E 32.2, YTD +54.9%, TTM +275.7%. https://www.trefis.com/stock/vsxy/articles-v3/611973/a-6-day-losing-streak-has-victorias-secret-stock-down-16/2026-08-19
37. StockStory via FinancialContent, "American Eagle, Dick's, Gap, Victoria's Secret, and Urban Outfitters Stocks Trade Up" (26 Aug 2026) — ANF record Q2 $1.27bn / EPS $4.17 / ~20% op margin / raised FY outlook lifting the group; URBN after-hours pullback; Gap −16% YTD. **`snippet_only`.** https://markets.financialcontent.com/stocks/article/stockstory-2026-8-26-american-eagle-dicks-gap-victorias-secret-and-urban-outfitters-stocks-trade-up-what-you-need-to-know
38. Stocktwits, "Victoria's Secret's 47% Surge Has Wall Street Hitting The Brakes — Here's Why UBS Downgraded VSXY Stock" — UBS Buy→Neutral on valuation post-Q1. https://stocktwits.com/news-articles/markets/equity/victorias-secret-rally-post-q1-earnings-ubs-downgrades-vsxy/cZ0jPUzRex1
39. TD Cowen price target $75 → $80, Hold, 18 Aug 2026. **`snippet_only`.** https://www.cnn.com/markets/stocks/VSXY
40. MarketBeat — Telsey Advisory Group price target $90 → $100, Outperform, 27 Aug 2026. https://www.marketbeat.com/instant-alerts/analyst-victorias-secret-co-nyse-vsxy-stock-price-expected-to-rise-telsey-advisory-group-analyst-says-2026-08-27/
41. GuruFocus — August 2026 analyst actions including BofA $95 → $107 (Buy) and JPMorgan $88 → $110 (Overweight). **`snippet_only`.** https://www.gurufocus.com/news/9041139/vsxy-maintained-by-ubs-price-target-raised-to-9500
42. Stocktwits, "VSXY Stock Eyes Best Week Ever: Retail Traders Brand Victoria's Secret As 'War Proof, Tariff Proof'" — bullish retail tone, "extremely high" message volume (June 2026, **stale**). https://stocktwits.com/news-articles/markets/equity/vsxy-stock-eyes-best-week-ever-retail-traders-brand-victoria-secret-war-proof-tariff-proof/cZ0SDRsReDU
43. Coverage of the GLP-1 tailwind narrative in the VSXY bull case. **`snippet_only`.** https://finance.yahoo.com/markets/stocks/articles/vsxy-stock-track-biggest-percentage-gain-175128727.html
44. SEC Form 4, BBRC International, transaction date 2026-07-28 — 718,007 @ $89.08, 79,122 @ $89.76, 1,791 @ $90.60; holding to 7,810,631. https://www.sec.gov/Archives/edgar/data/1856437/000121390026082832/0001213900-26-082832.txt
45. SEC Form 4, BBRC International, transaction date 2026-07-22 — 289,479 @ $88.89; and 2026-06-26 — 276,171 @ $88.50. https://www.sec.gov/Archives/edgar/data/1856437/000121390026081457/0001213900-26-081457.txt and https://www.sec.gov/Archives/edgar/data/1856437/000121390026073870/0001213900-26-073870.txt
46. SEC Form 4, BBRC International, transaction dates 2026-06-02 and 2026-06-04 — 1,107,672 @ $80.11 and 27,758 @ $80.03; holding to 9,175,201. https://www.sec.gov/Archives/edgar/data/1856437/000121390026065437/0001213900-26-065437.txt
47. Victoria's Secret & Co. via Nasdaq, "Shareholders Decisively Re-Elect All Nine Company Director Nominees" — Donna James >83% of votes cast, >99% excluding BBRC. https://www.nasdaq.com/press-release/victorias-secret-co-shareholders-decisively-re-elect-all-nine-company-director
48. Kirkland & Ellis, "Kirkland Represents Victoria's Secret & Co. in Successful Defense of 'Vote No' Proxy Fight". https://www.kirkland.com/news/press-release/2026/06/kirkland-represents-victorias-secret--co-in-successful-defense-of-vote-no-proxy-fight
49. SEC Form 4, Elizabeth Preis (Chief Marketing & Customer Officer), 2026-06-02 — 5,614 shares at $80.06, transaction code F (tax withholding on vesting), not a discretionary sale. https://www.sec.gov/Archives/edgar/data/1856437/000122520826005795/0001225208-26-005795.txt
50. SEC Form 144, Mariam Naficy (Director), filed 2026-06-17 — 1,317 shares via the Mader Naficy Revocable Trust. https://www.sec.gov/Archives/edgar/data/1856437/000196858226000627/0001968582-26-000627.txt
51. Retail Dive, "Victoria's Secret unveils allegations against activist investor, loses board director" — Naficy departure and the company's stated objections to Blundy's board candidacy. https://www.retaildive.com/news/victorias-secret-intimates-proxy-activist-investor-board-director/819981/
52. SEC Form 10-K FY2026 (year ended 2026-01-31) — executive tenure (Hillary Super CEO since Sep 2024; Scott Sekella CFOO since Aug 2025), business description, risk factors. https://www.sec.gov/Archives/edgar/data/1856437/000185643726000004/vsco-20260131.htm
53. Abercrombie & Fitch Q2 FY2026 press release (SEC Ex-99.1). https://www.sec.gov/Archives/edgar/data/1018840/000101884026000041/q22026pressrelease.htm
54. Urban Outfitters Q2 FY2026 results — record net sales $1.66bn (+10.4%), net income $240.7m, EPS $2.78 (GAAP diluted). https://www.globenewswire.com/news-release/2026/08/26/3351678/4732/en/urbn-reports-record-q2-sales-and-profits.html
55. Investing.com earnings-call coverage, "Urban Outfitters posts record Q2 2026 sales, shares retreat". https://in.investing.com/news/stock-market-news/earnings-call-transcript-urban-outfitters-posts-record-q2-2026-sales-shares-retreat-93CH-5572983
56. Quartz, "Bath & Body Works Q2 2026 earnings: profit outlook raised, sales weak" — Q3 guidance detail vs consensus. https://qz.com/bath-body-works-earnings-profit-outlook-sales-forecast-082626
57. AEO Inc. — Q2 FY2026 results to be reported 9 September 2026 after market close. https://www.businesswire.com/news/home/20260825313920/en/AEO-Inc.-to-Report-Second-Quarter-Fiscal-2026-Results-on-September-9-2026
58. Barchart mirror of the AEO scheduling release. https://www.barchart.com/story/news/4029832/aeo-inc-to-report-second-quarter-fiscal-2026-results-on-september-9-2026
59. American Eagle Outfitters Q1 FY2026 results — record Q1 revenue $1.2bn (+10%), Aerie comps +25%. https://investors.ae.com/press-releases/news-details/2026/AEO-Inc--Reports-First-Quarter-Fiscal-2026-Results/default.aspx
60. Coresight Research, "August 2026 US Retail Sales Outlook: Forecasting Retail Sales Growth Above 4% Through Year-End". **`snippet_only`, vintage uncertain.** https://coresight.com/research/august-2026-us-retail-sales-outlook-forecasting-retail-sales-growth-above-4-through-year-end/
61. EY US retail sales macro commentary — tariff pass-through, real volume constraints, apparel category contribution. **`snippet_only`, vintage uncertain.** https://www.ey.com/en_us/insights/strategy/macroeconomics/us-retail-sales

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such. Every company-specific figure above is either sourced to a URL or explicitly marked unavailable; figures labelled "own calc" are my derivations from the cited underlying data, and figures labelled `snippet_only` come from search-result snippets rather than a retrieved page.*
