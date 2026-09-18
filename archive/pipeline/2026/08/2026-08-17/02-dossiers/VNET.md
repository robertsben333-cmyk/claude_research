# VNET — VNET Group, Inc.

**Event confirmed: YES** — Q2 2026 (June quarter) results, **Tuesday 18 August 2026, before the open of U.S. markets**, earnings call 8:00 AM ET / 8:00 PM Beijing [1][2][3][8]. No date change or pre-announcement found; the scheduling release went out 4 August 2026 [19].

**What this print is about.** VNET is no longer a Chinese colocation story — it is a levered, capital-hungry AI-data-centre developer whose equity trades on delivered megawatts and order backlog, not on EPS. Q1 2026 was the setup quarter: only 18MW delivered as planned, wholesale revenue overtaking retail for the first time (+58.1% YoY), 517MW of new orders booked year-to-date of which ~510MW came from a *single* internet customer, and FY26 guidance held flat despite the order haul [16][18]. Management told the Street the ramp is back-half loaded: ~250MW across Q2–Q3 2026 and 266MW across Q4 2026–Q1 2027, against a stated annual delivery target of 450–500MW and RMB10–12bn of capex [18]. So this is the first print where the delivery machine has to actually show up in the operating metrics. Two things frame it: the closest comparable, GDS, reported eight sessions earlier, *raised* capex and revenue guidance and rallied +6.2% on the day — but its adjusted EBITDA margin fell 180bp YoY on higher utility costs [24][34]; and Tencent's Q2 capex tripled QoQ-adjusted (+176% YoY to RMB52.8bn) with a pledge of "substantial increase" weighted to H2 [25]. The stock, meanwhile, is $7.60 — down 24.7% in 60 sessions and near the bottom of a $6.17–$14.48 52-week range [4][7] — with 15.5% of float short [10] and a violently call-skewed option book [6]. The market is paying ~12% for the move; the last six prints averaged 6.8%.

---

## 1. Event & anchors

| Item | Value | As-of | Source |
|---|---|---|---|
| Report date | 2026-08-18 | confirmed | [1][2][3] |
| Session | **bmo** (before U.S. open); call 8:00 AM ET | confirmed | [1][2][8] |
| Fiscal period | Q2 2026 (quarter ended 2026-06-30) | — | [1][19] |
| Scheduling release | 2026-08-04 | — | [19] |
| Spot (last close) | **$7.60** | 2026-08-14 16:00 ET | [4][7] |
| Indicative pre-open | $7.70 (+1.32%) — Cboe file stamped 2026-08-17 10:05 ET but `last_trade_time` = 2026-08-14 15:59 ET, so treat as stale/indicative | 2026-08-17 | [6] |
| Market cap | **$2.16bn** (284.69M ADSs out) | 2026-08-14 | [4] |
| 52-week range | $6.17 – $14.48 | 2026-08-14 | [4] |
| **Event implied move (my calc)** | **±12.2%** = 85% × ATM straddle, 2026-08-21 expiry (first expiry after the print), interpolated to spot $7.70. Straddle K=7.0 → $1.08; K=8.0 → $1.12; interpolated $1.108 = 14.39% of spot | 2026-08-17 file | [6] |
| Published implied move | **±14.8%** (raw-straddle convention) | 2026-08-16 | [5] |
| Published avg historical move (same source) | ±12.2% | 2026-08-16 | [5] |
| IV30 | 89.69 (down 2.52 pts, −2.7% d/d) | 2026-08-17 file | [6] |
| IV / HV / **IV Rank** | IV 84.86% / HV 67.88% / **IV Rank 46.80%** (no as-of printed on page — low confidence) | fetched 2026-08-17 | [8] |
| IV30 vs 52-wk IV range | 89 vs range 55–112 → ≈60th percentile (snippet_only) | 2026-08-11 | [30] |
| 30-day realised vol (my calc from daily closes) | 69.1% annualised | to 2026-08-14 | [7] |

**Do not use** the Investing.com headline "may move 2% on earnings release" [28]. Its historical table interleaves 2024 and 2026 dates and its "actual move" figures (−5.7% for 26 May 2026, −0.9% for 16 Mar 2026) do not reconcile with raw price data. I computed the reactions myself.

### Realised one-day earnings reactions (close-to-close, computed from daily OHLC; earnings dates and sessions confirmed from company releases)

| Quarter | Report date | Session | Reaction day | Prev close | Close | **1-day move** | Gap at open | Volume |
|---|---|---|---|---|---|---|---|---|
| Q3 2024 | 2024-11-20 | amc [7th qtr, for context] | 2024-11-21 | 3.76 | 4.33 | **+15.16%** | +7.71% | 4.84M |
| Q4 2024 | 2025-03-12 | bmo | 2025-03-12 | 11.91 | 11.00 | **−7.64%** | −2.02% | 14.5M |
| Q1 2025 | 2025-05-28 | bmo | 2025-05-28 | 6.04 | 5.39 | **−10.76%** | −6.95% | 9.91M |
| Q2 2025 | 2025-08-21 | bmo | 2025-08-21 | 7.98 | 7.34 | **−8.02%** | −6.64% | 7.37M |
| Q3 2025 | 2025-11-20 | bmo | 2025-11-20 | 8.32 | 8.22 | **−1.20%** | **+5.77%** | 7.20M |
| Q4 2025 | 2026-03-16 | bmo | 2026-03-16 | 10.51 | 9.53 | **−9.32%** | −0.10% | 12.1M |
| Q1 2026 | 2026-05-26 | bmo | 2026-05-26 | 9.54 | 9.92 | **+3.98%** | −0.63% | 16.1M |

Sources: prices [7]; dates/sessions [2][3] and company scheduling releases [39] and search-confirmed PRs.

**Last six quarters (Q4'24 → Q1'26): `[−7.64, −10.76, −8.02, −1.20, −9.32, +3.98]`**
- mean |move| **6.82%** · median |move| **7.83%** · max |move| **10.76%**
- pattern: **1 up / 5 down**. Including Q3'24 → 2 up / 5 down, mean |move| 8.01%.
- Intraday reversal is a recurring feature: Q3'25 gapped **+5.8%** and closed **−1.2%**; Q4'25 opened flat and closed **−9.3%**; Q4'24 gapped −2% and closed −7.6%. The open is a poor guide to the close in this name.
- **My inference:** the option market's ±12.2% is ~1.8× the realised mean and ~1.6× the realised median of the last six. Either the market is paying for a guidance-raise binary, or the event vol is simply rich.

---

## 2. The bar

**Consensus**
- Q2 2026 EPS: **−$0.06 per ADS** [12]. Analyst count on the EPS line: **unavailable**.
- Q2 2026 revenue: **$405.75M** [13]. At USD/CNY 6.7377 [33] that is ≈RMB2.73bn (+12.5% YoY); at the ~7.15–7.18 rate prevailing in Q2 2025 it is ≈RMB2.90bn (+19% YoY). **The FX basis of the published USD estimate is not disclosed, so treat the RMB-equivalent as a range, not a number.**
- Coverage: **14 analysts**, consensus "Buy" [4][13]; rating split 9 Strong Buy / 4 Buy / 0 Hold / 1 Sell [14].
- Consensus price target is wildly dispersed: $15.07 avg, range $7.55–$24.97 (14 analysts, S&P Global / TipRanks, updated 2026-08-07) [14]; $15.08 (14 analysts) [also Investing.com consensus page]; $14.00 (14 analysts) [13]; $17.40 (6 analysts) [15]. Against a $7.60 spot that is 84–129% implied upside — **the sell side is far more bullish than the tape.**

**Company guidance (reiterated at Q1, unchanged twice this year)** [16]
- FY2026 net revenue **RMB11.5–11.8bn** (+15.6% to +18.6% vs RMB9.95bn FY2025 [36])
- FY2026 adjusted EBITDA **RMB3,550–3,750M** (+19.2% to +25.9% vs RMB2.98bn FY2025 [36])
- FY2026 capex **RMB10–12bn**, sized against a "450 to 500 megawatts" annual delivery target [18]

**What the company has to deliver just to hold the stock flat — my inference, arithmetic from [16]**
- Revenue: FY midpoint RMB11.65bn less Q1's RMB2.69bn leaves RMB8.96bn over three quarters = RMB2.99bn/qtr. Straight-line, Q2 needs roughly **RMB2.85–2.95bn (+17% to +21% YoY** vs RMB2.43bn in Q2 2025 [35]).
- Adjusted EBITDA: FY midpoint RMB3.65bn less Q1's RMB891.5M leaves RMB2.76bn = RMB920M/qtr. Q2 needs roughly **RMB900–950M (+23% to +30% YoY** vs RMB732.5M [35]), i.e. a **~31–33% margin** vs 30.1% in Q2 2025.
- Capacity: from 907MW in service at 31 Mar [16], with ~250MW guided across Q2+Q3 [18], a "clean" Q2 delivers roughly **100–130MW**, taking capacity in service to **~1,010–1,040MW** with utilised capacity above 687MW. Anything at the Q1-style 18MW pace reads as slippage.
- Guidance: GDS *raised* both capex and revenue guidance on 13 August [24]. **A reiteration from VNET now reads as a relative negative**, because it is the third consecutive hold against 517MW of booked orders.

**Estimate revisions**
- I could not source a clean 30/60/90-day consensus EPS/revenue revision series — the free surfaces (Nasdaq, Seeking Alpha, TipRanks) were empty, paywalled or 403'd. **Marked as a coverage gap.**
- What I could source is price-target drift, which has turned down: **Bank of America cut its target to $13.20 from $16.30 on ~7–10 August 2026 while keeping Buy** [14][snippet 30-class search result]; Deutsche Bank initiated Buy $12.50 on 7 July 2026; Weiss reiterated Sell (D+) on 15 July; Morgan Stanley reiterated OW $16.00 and Jefferies Buy $24.79, both on 26–27 May [15]. Net: the only *change* in the last ten weeks was a 19% target cut from a Buy-rated house.
- FY26 EPS consensus is not a usable anchor: published figures range from +$0.20 to −$8.79 for the same year across providers [4][14], which tells you the sell side models the REIT/tax/derivative line, not operations.

**Whisper number: unavailable.** EarningsWhispers gates it behind login [ref in sources]. Given EPS is dominated by non-operating tax and derivative items (Q1's RMB531.8M net loss was driven by RMB486.2M of *capital-transaction* income tax from the REIT listings [17]), the EPS line is close to information-free here anyway.

---

## 3. The one metric that matters

**Delivered and utilised wholesale megawatts, and whether the FY26 delivery/capex/EBITDA guidance is finally raised.** Not EPS, not even revenue.

Why, and how I know:
- Q1 2026's revenue beat ($390.32M vs $388.47M) and EBITDA beat (RMB891.5M vs RMB881M consensus) coincided with a **$1.17 EPS miss**, and the stock went **up 3.98%** [11][7]. The market explicitly looked through EPS.
- Management framed the whole 2026 story in delivery terms on the Q1 call: 519MW of orders YTD, the 500MW anchor order phased 2026–2028, "250 megawatts targeted for Q2–Q3 2026 and 266 megawatts for Q4 2026–Q1 2027," capex "based on annual delivery target of 450 to 500 megawatts," unit capex "around RMB20,000 per kilowatt" [18].
- The Q1 press release leads with the operating stack, not the P&L: capacity in service 907MW, utilised 687MW, utilisation 75.7% (mature 93.8% / ramp-up 45.0%), committed capacity 869MW = **95.7% commitment rate**, **516MW under construction** [16].

**The expectation I would hold management to (my inference, from [16][18]):**
1. Capacity in service ≈**1,010–1,040MW** (Q1: 907MW). Below ~975MW = slippage.
2. Utilised capacity meaningfully above 687MW; utilisation rate holding ≥73–75% *despite* new ramp-up capacity landing (mechanically dilutive to the ratio — a small utilisation dip on big deliveries is good news, and the market may misread it).
3. **New orders YTD > 517MW.** VNET press-releases material order wins (e.g. the 40MW win, the 517MW YTD tally) — and there has been **no order press release and no 6-K at all between 26 May and 17 August 2026** [19]. Either they have been saved for the print, or Q2 booked nothing. This is the single most under-appreciated binary in the setup.
4. Adjusted EBITDA margin ≥31% with an explicit answer on utility costs — because that is exactly what compressed GDS [24].
5. Any raise to FY revenue / EBITDA / capex guidance, or an increase to the 450–500MW annual delivery target.

---

## 4. Fundamentals — what changed, what is at stake

**Segment mix inverted.** Q1 2026: wholesale IDC RMB1.06bn (+58.1% YoY) overtook retail IDC RMB1.02bn (+5.4%) **for the first time**; non-IDC RMB606.6M (+0.3%) [16]. Total RMB2.69bn (+19.8%). The growth engine is one segment, and increasingly one customer.

**Margin trajectory is two-faced.** Adjusted EBITDA RMB891.5M, +30.6% YoY, margin **33.1% vs 30.4%** — expanding. But GAAP gross profit only +8.9% to RMB615.9M and **gross margin fell to 22.9% from 25.2%** [16][17]. Depreciation on newly delivered, still-ramping capacity is the wedge. Both narratives are true and both will be quoted on 18 August.

**Unit economics.** Retail MRR/cabinet RMB9,448, 50,170 cabinets in service, 32,165 utilised, 64.1% utilisation (mature 68.5%, ramp-up 24.2%) [16] — retail is a slowly melting annuity. Wholesale unit capex "around RMB20,000/kW" [18], which on 450–500MW/yr is RMB9–10bn, consistent with the RMB10–12bn capex guide.

**Cash flow and balance sheet — the actual risk.** Operating cash flow was only **RMB173.7M** in Q1 2026 (vs RMB195.7M in Q1 2025) against **RMB1.75bn of quarterly capex** [16][17]. Liquidity RMB8.80bn (cash RMB7.77bn + ST investments RMB718.2M + restricted RMB307.9M). Debt: **ST RMB5.18bn + LT borrowings RMB12.93bn + converts RMB4.83bn ≈ RMB22.9bn** [16]. The company raised **RMB8.14bn** of new/refinanced debt, equity and other financing in Q1 alone [16]. FCF is structurally deeply negative by design; the equity is a call option on financing access.

**Financing channels actually working:** two private REITs listed on the Shanghai Stock Exchange in March 2026, combined offering ~**RMB6.36bn**, targeting ~RMB2bn of cash proceeds and a repeatable capital-recycling model [17][18]; ABS issuance (2 in Q1); a **$137.7M private placement** of 81.0M Class A shares at $1.70/share ($10.20/ADS) closing ~3 March 2026 [38] — i.e. real, recent dilution done ~34% above today's price; and management "actively exploring the feasibility" of a Hong Kong listing [18].

**Ownership change, not a capital raise.** CATL affiliates (PJ Millennium I/II) agreed on ~13 May 2026 to buy **~650.4M Class A shares (38.08%) at $1.4486/share, ~$942M, from Shandong Hi-Speed Holdings**, closing expected Q4 2026, subject to SDHG shareholder approval; buyers committed to vote with the founder so control is unchanged [31]. **No new money reaches VNET.** The $1.4486/share price equals **$8.69/ADS — 14% above today's $7.60**, which is a useful reference for what a strategic paid four months ago.

**Customer concentration is the elephant.** Of 517MW booked YTD 2026, **~510MW (110MW + 400MW) came from one internet customer** in the Greater Beijing Area; a 7MW local-services order made up the rest [18]. Concentration of this degree is a genuine multiple-compressor and any commentary on customer diversification will be read closely.

---

## 5. Positioning & options

All option data below from the Cboe delayed-quote file for VNET, file timestamp **2026-08-17 10:05:05 ET** [6]; corroborated on put/call by Barchart [9].

**Term structure — a textbook event kink**

| Expiry | DTE | ATM (K=8) call IV | ATM put IV |
|---|---|---|---|
| 2026-08-21 | 4 | **127.7%** | 121.9% |
| 2026-09-18 | 32 | 85.2% | 64.7% |
| 2026-12-18 | 123 | 77.5% | 83.6% |
| 2027-01-15 | 151 | 77.7% | 74.2% |

Front expiry trades ~43 vol points over the next month — all of it is the print. IV30 is 89.69 and **falling** (−2.52 pts, −2.7% d/d) into the event [6], which is unusual; event IV is normally bid in the last two sessions.

**Skew is inverted — the market is paying up for upside, not downside.**

| Expiry | 25Δ call IV | 25Δ put IV | Skew (put − call) |
|---|---|---|---|
| 2026-08-21 | 141.5% (K=9) | 115.3% (K=7) | **−26.2 pts** |
| 2026-09-18 | 98.8% (K=10) | 92.1% (K=7) | −6.6 pts |
| 2026-12-18 | 88.7% (K=13) | 81.5% (K=6) | −7.2 pts |
| 2027-01-15 | 87.7% (K=14) | 86.3% (K=6) | −1.4 pts |

**Put/call — extremely call-heavy**
- Total open interest: **89,752 calls vs 26,147 puts → P/C OI 0.291** [6]; Barchart shows 88,444 / 26,096 → 0.30 [9].
- Session volume: **2,243 calls vs 168 puts → P/C volume 0.075** [6][9].
- By expiry, P/C OI: Aug-21 0.23, Sep-18 0.24, Dec-18 0.20, **Mar-2027 0.01**, Jan-2027 0.93 (the only put-heavy tenor).

**Where the crowd is**
- **2026-08-21 $9.00 call: OI 12,172, session volume 1,263** — the single most-traded contract, ~17% OTM, 141.5% IV, delta 0.22. This is the event lottery ticket.
- 2027-03-19 $12.00 call: OI **12,995** (largest OI on the board), delta 0.38.
- 2026-09-18 $10.00 call OI 9,052; 2026-09-18 $9.00 call OI 3,673 with 405 traded.
- Downside interest is concentrated far out: 2027-01-15 $8.00 put OI 5,839 and $7.00 put OI 4,694 — hedges, not event bets. Nearest event put with size: Aug-21 $7.00, OI 3,805.
- **Barchart flagged VNET among names with unusual *call* volume on 10 August 2026** (snippet_only) [30].

**Short interest** [10]

| Settlement | Shares short | % float | Days to cover | Δ |
|---|---|---|---|---|
| 2026-07-31 | **36,843,771** | **15.50%** | **8.74** | −13.5% |
| 2026-07-15 | 42,577,426 | 17.90% | 9.30 | +12.4% |
| 2026-06-30 | 37,874,609 | 15.90% | 8.16 | −1.2% |
| 2026-06-15 | 38,342,506 | 16.10% | 5.69 | −5.3% |

15.5% of float with 8.7 days to cover on 3.85M ADS/day average volume [10] is genuine squeeze fuel, and shorts *reduced* 13.5% into the print — they are not adding. Nasdaq's own short-interest surface is empty for VNET [Nasdaq short-interest page].

**Borrow fee / utilisation: unavailable.** iBorrowDesk returned no data for VNET.

**Run-up (computed from daily closes to 2026-08-14 [7])**
- 5 sessions **+3.7%** · 10 sessions **+6.0%** · 20 sessions **+2.8%** · 60 sessions **−24.7%** (from $10.09 on 2026-05-19) · YTD **−16.6%** (from $9.11 on 2026-01-02)
- 20-day average volume 3.85M ADS; last 30 sessions ranged $6.29–$8.33 — the stock bottomed at $6.29 in late July and has rebuilt ~21% off that low into the print.

**Institutional flow.** Point72 Asset Management / Steven A. Cohen filed a 13G/A on **2026-08-14** reporting **18,331,561 ADSs = 6.6%** of Class A as of 30 June 2026 (including 40,800 ADSs' worth of call options) [21], up from **12,742,392 ADSs = 4.8%** as of 8 January 2026 [22] — a **+43.9%** increase in ADS terms over H1. A multi-manager building to 6.6% is consistent with the call-heavy book above.

**How crowded does the trade look? My read:** crowded on *both* sides, which is why the straddle is 1.8× realised. Long side is expressed in short-dated OTM calls (Aug-21 $9) and a growing Point72 stake; short side is 15.5% of float that is actively trimming. That is a configuration that produces violent moves in either direction and, historically in this name, an unreliable open (see the gap-vs-close column in §1).

---

## 6. Sentiment & alt-data

**Sell side** [14][15]
- 14 analysts, consensus "Buy": 9 Strong Buy / 4 Buy / 0 Hold / 1 Sell. Avg PT **$15.07**, low $7.55, high $24.97 (updated 2026-08-07).
- Rating/PT actions, most recent first: BofA **cut $16.30 → $13.20**, keeps Buy (~7–10 Aug 2026, snippet_only); Weiss reiterated Sell D+ (15 Jul); Deutsche Bank **initiated Buy, $12.50** (7 Jul, Peter Milliken); Morgan Stanley reiterated OW $16.00 (27 May); Zacks upgraded Strong Sell → Hold (27 May); Jefferies reiterated Buy $24.79 (26 May, Edison Lee).
- One unverified but directionally relevant claim: a secondary outlet reports **Goldman Sachs removed VNET from its APAC Conviction List** during the June–July drawdown [37]. Goldman *added* VNET to that list in October 2025. I could not corroborate the removal from a primary or tier-1 source — **treat as unconfirmed colour, not evidence.**

**Attention / retail (thin, and I am flagging it as thin)**
- MarketBeat trends page, as-of **2026-08-17**: media mentions **6 → 4 week-over-week (−33.3%)**; page views **2,235 → 1,921 (−14.0%)**; internal search volume 0 → 2 [29]. Attention is *falling* into a print with a 12% implied move, which is itself notable — this is not a retail-hyped setup.
- Stocktwits message-volume and bull/bear percentages: **could not retrieve numerically.** A search-snippet characterisation of the Stocktwits stream describes it as "mixed" — bullish on wholesale IDC growth (+58.1%), bearish on the RMB531.8M net loss, 22.9% gross margin and declining retail capacity [Stocktwits/search]. **This is colour only; no 7/14/30-day sentiment series is sourced.**

**Alt-data proxies — largely unavailable.** No Google Trends series, no app-rank data (not applicable), no web-traffic estimate, no job-posting count, no China IDC channel-check note could be sourced within this run. The nearest usable proxies are macro/industry:
- **China business electricity price ≈11.6 US¢/kWh (April 2026) vs 8.7 US¢/kWh (June 2024)** [32] — a ~33% rise in the key input cost, and precisely the line item that cut GDS's Q2 EBITDA margin by 180bp [24].
- No VNET order press release or 6-K filed between **2026-05-26 and 2026-08-17** [19] — a ~12-week communication silence in a company that had filed nine 6-Ks between 13 February and 26 May 2026.

---

## 7. Forensics

**A structural change worth knowing: VNET insiders now file Form 4s.** The Holding Foreign Insiders Accountable Act (in the FY2026 NDAA, enacted 18 December 2025) extended Section 16(a) to directors and officers of foreign private issuers **effective 18 March 2026** [23]. VNET duly filed **seven Form 3s on 2026-03-17** [19]. VNET remains an FPI (20-F / 6-K), but insider transaction data exists for this name for the first time — and it is genuinely under-used.

**Every 2026 Form 4, read from the filings themselves** [20]:

| Filed | Insider | Role | Code | Shares (Class A ord.) | Price | Post-txn |
|---|---|---|---|---|---|---|
| 2026-03-25 | David Lifeng Chen | Director | **S** | 83,544 | $1.5055 (≈$9.03/ADS) | 334,164 |
| 2026-05-19 | Zhihua Zhang | SVP, Operational Finance | M then **S** | +42,996 / −9,072 | $1.6946 (≈$10.17/ADS) | 33,924 |
| 2026-06-03 | Sean Shao | Director | **S** | 60,000 | $1.7133 (≈$10.28/ADS) | 983,820 |
| 2026-05-01 | David Lifeng Chen | Director | M (RSU vest) | +83,544 | — | 417,708 |
| 2026-08-04 | David Lifeng Chen | Director | M (RSU vest) | +83,544 (vested 2026-07-31) | — | 501,252 RSUs |

Readings:
- **No 10b5-1 checkbox is marked on any of these filings** [20] — on their face all sales are **discretionary**, not plan sales. That said, all three sales are small, RSU-vest-adjacent and consistent with sell-to-cover behaviour; I would not over-read them.
- **Zero open-market purchases by any insider in 2026.** No insider is buying a stock the sell side thinks is worth ~2×.
- **No insider sale since 1 June 2026.** The only filing in the pre-earnings window (2026-08-04) is an RSU vesting with no disposal — i.e. **no pre-earnings distribution signal.**
- Two Form 144s were filed 2026-03-19 and 2026-03-20 [19], consistent with the Chen sale.

**Management and board churn — the real forensic flag.**
- **CFO Qiyu Wang resigned effective 2026-04-30**, stated for personal reasons and explicitly "not due to any disagreement with VNET or its accounting practices" [26]. **Peter Zhihua Zhang** had been appointed SVP, Operational Finance and **principal accounting officer** on 2026-02-13 — two and a half months *before* the CFO departure was announced [27]. I found **no announcement of a permanent CFO**. VNET therefore goes into a capital-markets-critical print (RMB10–12bn capex, HK listing under study, RMB22.9bn of debt, a 38% control transfer pending) **without a named CFO**, with the accounting function under an SVP who himself sold stock in May [20][26][27]. This is the item I would push hardest on.
- Director **Jianbiao Zhu resigned 2026-03-09**, described as amicable with no disagreement [search-sourced].

**Filings hygiene.** FY2025 20-F filed **2026-04-16** (FY2024's was filed 2025-04-25 — no delay) [19]. **No restatement, NT filing, auditor change or disclosed material weakness surfaced** in my searches — but I could not read the 20-F itself, so this is **absence of evidence, not evidence of absence.** Marked as a gap.

**8-K/6-K cadence.** 2026 6-Ks: 13 Feb, 17 Feb (×2), 27 Feb, 10 Mar, 16 Mar, 20 Apr, 13 May, 26 May — then **nothing** through 17 August [19]. In 2025 the equivalent summer window also went quiet (27 Jun ×2, then 21 Aug), so this is not unprecedented; but 2026 H1 was unusually loud and the silence follows a period of monthly order/financing news.

**Pre-announcement signalling: none found.** No guidance update, no pre-release, no date change.

---

## 8. Macro & peer read-through

**The demand signal is unambiguously strong and it is fresh.**
- **Tencent (Q2 2026, reported 12 Aug):** capex **RMB52.8bn, +176% YoY and +65% QoQ**, pushing free cash flow to **−RMB13.8bn**; CSO James Mitchell pledged "a substantial increase" in 2026 capex **especially in the second half**, as China-designed AI chips become available [25]. Tencent going FCF-negative to buy compute is the single best leading indicator for Greater-Beijing wholesale IDC absorption — which is exactly where VNET's 510MW anchor order sits [18].
- **Alibaba:** CEO Eddie Wu signalled the company will **overshoot** its RMB380bn three-year AI capex pledge, with the spend concentrated in cloud [25-adjacent SCMP coverage].
- Combined ByteDance/Tencent/Alibaba/Baidu capex is tracked as **+80%+ YoY in 2026** [25-adjacent].

**The closest peer just told us both halves of the story.** GDS Holdings, Q2 2026, **BMO 13 August 2026** [24]:
- Revenue RMB3,088.0M **+6.5% YoY**; adjusted EBITDA RMB1,406.0M **+2.5%**; net income RMB837.6M vs a RMB70.6M loss.
- **Adjusted EBITDA margin 45.5% vs 47.3% YoY — explicitly attributed to higher utility costs.**
- Utilisation 79.2% (from 77.5%); **area under construction +43.9% QoQ**; pre-commitment on construction 89.2%; committed + pre-committed area +18.2% YoY.
- **Capex guidance raised to ~RMB10,000M from ~RMB9,000M**; FY revenue guide raised to RMB12,700–13,000M.
- **Stock reaction: +6.20% on the day (32.74 → 34.77), then −1.04% the next session** [34].

**My read-throughs, labelled as inference:**
1. **Positive for VNET's demand/backlog narrative** — a peer accelerating construction 44% QoQ and raising capex is confirming the order cycle VNET is levered to.
2. **Negative for VNET's margin line** — utility-cost inflation [32] hit the peer's EBITDA margin by 180bp. VNET needs a *rising* margin (~31–33%) to stay on FY guidance (§2). This is the most likely place for a bad surprise.
3. **The bar on guidance has been reset upward by GDS.** A reiteration from VNET after 517MW of orders will look conservative by comparison.
4. **Sentiment tailwind is real but stale-ish.** BABA rallied ~+11% from 30 Jul to 10 Aug then gave back ~4.5% into 13 Aug, closing +1.35% on 14 Aug [34-adjacent]. China ADRs are firm, not euphoric.

**FX.** USD/CNY **6.7377** on 2026-08-17 [33], vs ~7.15–7.18 a year earlier. VNET reports in RMB; a ~6% stronger RMB **flatters every USD-translated headline** by roughly that amount. Any USD-based "beat" against a USD consensus struck on an older FX assumption may be partly currency. Conversely, RMB appreciation modestly eases the USD-denominated convertible/offshore debt burden.

**Rates/commodities.** VNET is a long-duration, heavily levered, negative-FCF asset — the most rate- and risk-appetite-sensitive profile in the China IDC complex. Power tariffs [32] are the operating commodity exposure.

---

## 9. Bull case / bear case / base case

**Bull.** Q2 is the quarter the H2-loaded ramp becomes visible: capacity in service jumps from 907MW toward ~1,030MW against a 95.7% commitment rate and 516MW under construction [16], utilised capacity climbs off 687MW, and management raises FY revenue/EBITDA guidance the way GDS just did [24] — plus discloses new orders taking the YTD tally above 517MW, which the 12-week press-release silence [19] makes plausible as saved news. The demand evidence behind that is not speculative: Tencent's capex tripled and is explicitly H2-weighted [25]. Into that, positioning is combustible in VNET's favour — 15.5% of float short with 8.7 days to cover [10], Point72 up 44% to 6.6% [21][22], and CATL agreeing to pay $8.69/ADS-equivalent four months ago [31] versus $7.60 today. The stock is 24.7% below its May level and 47% below its 52-week high [4][7], so the price embeds very little.

**Bear.** The base rate is the bear case: **five of the last six prints closed down**, mean |move| 6.8%, and the two worst gaps came after operationally fine quarters [7]. The mechanism is consistent — VNET beats on revenue/EBITDA and then discloses something on margin, tax or funding that resets the model. Q1 gave you the template: gross margin **22.9% vs 25.2%**, a RMB531.8M net loss, operating cash flow of RMB173.7M against RMB1.75bn of capex, and RMB22.9bn of debt [16][17]. Now add a confirmed, sector-wide utility-cost squeeze that just cost the closest peer 180bp of EBITDA margin [24][32], while VNET needs margin to *rise* to ~31–33% to hold guidance (§2). Add ~510MW of the 517MW order book sitting with **one** customer [18], no permanent CFO into a print that is fundamentally about financing capacity [26][27], no insider buying all year [20], and a Buy-rated broker cutting its target 19% two weeks ago [14]. And the upside is pre-paid: the Aug-21 $9 call has 12,172 OI at 141.5% IV with 25Δ calls 26 vol points *over* 25Δ puts [6] — a good print can be sold into that.

**Base case.** Revenue and adjusted EBITDA land in or slightly above the RMB2.85–2.95bn / RMB900–950M straight-line band, capacity in service prints roughly 990–1,040MW, **FY26 guidance is reiterated rather than raised**, and margin commentary is hedged on power costs. That is a "fine, not thrilling" quarter into a ±12.2% straddle, and the option market loses. Directionally the tape then splits: the short base [10] and the depressed price argue up, the base rate and the sell-into-strength call overhang argue down, and the historical gap-versus-close divergence [§1] argues that whatever happens at 9:30 is not what happens at 16:00. I lean marginally negative on the close, with low conviction, and I think the highest-probability *trade* observation in this dossier is that **realised will come in inside the implied** — 6.8% mean realised versus 12.2% priced.

---

## 10. What would flip the consensus view

**The single most credible reversal is a raised FY2026 guide accompanied by a new order disclosure.** Concretely: net revenue guidance lifted from RMB11.5–11.8bn to ~RMB12.0bn+, adjusted EBITDA lifted above RMB3.75bn, capex lifted above RMB12bn, and new orders YTD disclosed above ~700MW with at least one named *new* customer diluting the 510MW single-customer concentration [16][18]. That combination would do three things at once: validate the 450–500MW delivery target as a floor rather than a cap, break the "guidance is always reiterated" pattern that has framed three straight prints, and remove the concentration discount. Against 15.5% short float with 8.7 days to cover [10] and 12,172 contracts of Aug-21 $9 calls already open [6], that print does not produce a 4% day — it produces a gap through $9 and a squeeze, and it would invert the 5-of-6-down base rate in one session.

The mirror-image flip: **capacity in service below ~975MW plus adjusted EBITDA margin below 30%.** That says the H2 ramp has slipped *and* power costs are eating the incremental economics, which forces the FY EBITDA guide to be de-facto abandoned in Q3 and puts the RMB10–12bn capex programme in tension with RMB173.7M-per-quarter operating cash flow [16]. In that world the $15 average price target [14] is stale by 40%+ and the 4/5 of the option book that is long calls unwinds into the same exit.

A third, lower-probability flip that nobody is positioned for: **any negative development on the CATL/SDHG transaction** (it still requires SDHG shareholder approval [31]). The market treats a Q4 close as done. It is not.

---

## 11. Coverage gaps

| Gap | Why it matters |
|---|---|
| **30/60/90-day consensus estimate revisions** (EPS and revenue). Nasdaq, Seeking Alpha and TipRanks surfaces were empty, paywalled or 403. | Revision direction is the cleanest read on whether the buy side has already marked the H2 ramp. Without it I substituted price-target drift, which is a weaker proxy. |
| **Whisper number** — EarningsWhispers gated behind login. | Less damaging than usual here, since EPS is dominated by non-operating tax/derivative items. |
| **Analyst count on the Q2 EPS line**, and the Q2 revenue estimate from a second independent provider. Only one source each (−$0.06 [12]; $405.75M [13]). | A single-sourced consensus is a fragile bar. The FX basis of the USD revenue estimate is also undisclosed, which is material given RMB moved ~6% YoY. |
| **Q2 2026 adjusted EBITDA consensus** — not sourced anywhere. | This is the line the stock actually reacts to; I had to derive the required range arithmetically from guidance instead. |
| **IV rank / percentile with a stated as-of.** Barchart printed 46.80% with no timestamp [8]; Market Rebellion's IV30 = 89 vs a 55–112 52-week range implies ~60th percentile [30] and is snippet-only. My IV30 of 89.69 [6] has no history attached. | Two credible readings ~13 points apart. It changes whether you call event vol "average" or "elevated". |
| **Borrow fee and utilisation** — iBorrowDesk returned nothing; Nasdaq's short-interest page for VNET is empty. | With 15.5% of float short [10], the cost of that short is the difference between conviction shorts and lazy hedges. |
| **Retail/social sentiment as a 7/14/30-day series.** Only MarketBeat's week-over-week mentions/page-views [29] and a qualitative Stocktwits characterisation. | Weakest section of the dossier. Treat all sentiment here as colour. |
| **All conventional alt-data**: Google Trends, web traffic, job postings, China IDC channel checks, regional power-quota news. | For a capacity-delivery story, a job-postings or construction-permit proxy would have been the highest-value independent check on the 250MW Q2–Q3 claim. |
| **FY2025 20-F contents** — could not read the filing; no independent confirmation of auditor identity, ICFR conclusion, or absence of a material weakness. | I report "no issues found", which is not the same as "no issues". |
| **Whether any new orders were signed in Q2 2026.** No press release, no 6-K, 26 May → 17 August [19]. | This is the biggest single unknown in the print and I could not resolve it either way. |
| **Goldman APAC Conviction List removal** — single secondary source [37], uncorroborated. | If true it partly explains the June–July drawdown; I have not treated it as evidence. |
| **Spot freshness.** Last confirmed close is 2026-08-14 ($7.60). The Cboe file was timestamped 2026-08-17 10:05 ET showing $7.70 but with a 2026-08-14 15:59 last-trade time [6]. | If VNET moved materially on 17 August, every percentage in §5 shifts. |

---

## 12. Sources

1. VNET Group Investor Relations — https://ir.vnet.com/ — Q2 2026 date/time (page returned HTTP 503 on direct fetch; date/time confirmed via indexed content of this domain and [2][19]).
2. Market Chameleon, VNET earnings dates — https://marketchameleon.com/Overview/VNET/Earnings/Earnings-Dates/ — "expected to release earnings on August 18, 2026 before the market opens (BMO)"; last report 26 May 2026 BMO, +4.0% to close 9.92; −23.4% drift since.
3. Barchart / PR Newswire, VNET Q4 FY2025 scheduling release — https://www.barchart.com/story/news/555433/vnet-to-announce-unaudited-fourth-quarter-and-full-year-2025-financial-results-on-march-16-2026 — verbatim "before the open of U.S. markets", call 8:00 AM ET; establishes VNET's BMO/8:00 ET pattern.
4. StockAnalysis, VNET overview — https://stockanalysis.com/stocks/vnet/ — spot $7.60 as of 2026-08-14 16:00 ET; market cap $2.16bn; 284.69M shares; 52-wk $6.17–$14.48; TTM revenue $1.51bn; next earnings 2026-08-18.
5. EarningsWatcher, week of 17–21 Aug 2026 — https://earnings-watcher.com/earnings-this-week — VNET implied move ±14.8%, average historical ±12.2%, last report −10.5%, report 2026-08-18 before open, data as-of 2026-08-16.
6. Cboe delayed option quotes, VNET — https://cdn.cboe.com/api/global/delayed_quotes/options/VNET.json — file timestamp 2026-08-17 10:05:05; underlying $7.70 (last trade 2026-08-14 15:59); IV30 89.692 (−2.52); full chain used for the ATM straddle (±12.2%), term structure, 25Δ skew, put/call OI and volume, and top OI/volume contracts.
7. Yahoo Finance chart API, VNET daily OHLCV 2024-01-02 → 2026-08-14 — https://query1.finance.yahoo.com/v8/finance/chart/VNET — all historical earnings-day reactions, gaps, volumes, run-up windows and 30-day realised vol computed from this series.
8. Barchart, VNET expected move — https://www.barchart.com/stocks/quotes/VNET/expected-move — IV 84.86%, HV 67.88%, IV Rank 46.80%, "Latest Earnings: 08/18/26 [BMO]" (expected-move table itself was JS-loaded and unavailable).
9. Barchart, VNET put/call ratios — https://www.barchart.com/stocks/quotes/VNET/put-call-ratios — put vol 168 / call vol 2,243 (0.07); put OI 26,096 / call OI 88,444 (0.30).
10. MarketBeat, VNET short interest — https://www.marketbeat.com/stocks/NASDAQ/VNET/short-interest/ — 36,843,771 shares short, 15.50% of float, 8.74 days to cover at 2026-07-31, −13.5% vs prior; prior periods 2026-07-15 / 06-30 / 06-15.
11. MarketBeat, VNET earnings — https://www.marketbeat.com/stocks/NASDAQ/VNET/earnings/ — 2026-08-18 BMO, call 8:00 AM ET; Q1 2026 EPS −$1.20 vs −$0.03 est; revenue $390.32M vs $388.47M est; FY26 revenue guide $1.7bn.
12. CoinCodex, VNET earnings — https://coincodex.com/stock/VNET/earnings/ — Q2 2026 consensus EPS −$0.06; EPS forecast-vs-actual history for 2025-03-12, 2025-08-21, 2025-11-20, 2026-03-16, 2026-05-26.
13. TradingKey, VNET forecast — https://www.tradingkey.com/markets/stocks/vnet/forecast — next-quarter revenue estimate $405.75M; 14 analysts; consensus PT $14.00 (high $27.22, low $10.84).
14. StockAnalysis, VNET forecast — https://stockanalysis.com/stocks/vnet/forecast/ — 14 analysts, Buy; avg PT $15.07, range $7.55–$24.97; 9 Strong Buy / 4 Buy / 0 Hold / 1 Sell; BofA cut $16 → $13 on 2026-08-07; data updated 2026-08-07 (S&P Global / TipRanks).
15. MarketBeat, VNET price targets — https://www.marketbeat.com/stocks/NASDAQ/VNET/price-target/ — Weiss Sell D+ 2026-07-15; Deutsche Bank initiate Buy $12.50 2026-07-07; Morgan Stanley OW $16.00 and Zacks upgrade 2026-05-27; Jefferies Buy $24.79 and BofA Buy $16.30 2026-05-26; consensus $17.40 on 6 analysts.
16. SEC / VNET Q1 2026 earnings press release (6-K exhibit 99.1, filed 2026-05-26) — https://www.sec.gov/Archives/edgar/data/1508475/000110465926065937/tm2615608d1_ex99-1.htm — **primary source** for: revenue RMB2.69bn +19.8%; wholesale RMB1.06bn +58.1%; retail RMB1.02bn +5.4%; non-IDC RMB606.6M +0.3%; gross profit RMB615.9M, margin 22.9% vs 25.2%; adjusted EBITDA RMB891.5M +30.6%, margin 33.1% vs 30.4%; capacity in service 907MW, utilised 687MW, utilisation 75.7% (mature 93.8% / ramp 45.0%), committed 869MW / 95.7%, under construction 516MW; retail 50,170 cabinets, 32,165 utilised, 64.1%, MRR/cabinet RMB9,448; cash+ST inv+restricted RMB8.80bn; ST debt RMB5.18bn, LT borrowings RMB12.93bn, converts RMB4.83bn; operating cash flow RMB173.7M; Q1 capex RMB1.75bn; RMB8.14bn of financing raised; FY26 guidance RMB11.5–11.8bn revenue / RMB3,550–3,750M adjusted EBITDA / RMB10–12bn capex, "unchanged".
17. StockTitan, VNET Q1 2026 — https://www.stocktitan.net/news/VNET/vnet-reports-unaudited-first-quarter-2026-financial-estmglgnyvnq.html — net loss RMB531.8M driven by RMB486.2M of capital-transaction income tax; two Shanghai-listed private REITs, ~RMB6.36bn combined offering; loss/ADS RMB8.16 (US$1.20); FY26 capex guide.
18. Motley Fool, VNET Q1 2026 earnings call transcript (2026-05-26) — https://www.fool.com/earnings/call-transcripts/2026/05/26/vnet-q1-2026-earnings-call-transcript/ — 519MW orders YTD incl. 400MW + 110MW from one internet customer; 500MW order phased 2026–2028; 18MW delivered in Q1 as planned; ~250MW targeted Q2–Q3 2026, 266MW Q4 2026–Q1 2027; 450–500MW annual delivery target; unit capex ~RMB20,000/kW; REIT target ~RMB2bn cash; CATL synergies and 1.5GW wholesale footprint; Hong Kong listing "actively exploring the feasibility"; retail MRR/cabinet and 64.1% utilisation.
19. SEC EDGAR submissions, VNET Group (CIK 0001508475) — https://data.sec.gov/submissions/CIK0001508475.json — complete filing history: 6-K cadence (13 Feb → 26 May 2026, then none through 17 Aug); seven Form 3s on 2026-03-17; Form 4s on 2026-03-25, 05-01, 05-15 ×3, 05-19, 06-03, 08-04; Forms 144 on 2026-03-19/20; 20-F filed 2026-04-16 (FY2024's on 2025-04-25); 13G/A on 2026-08-14.
20. VNET Form 4 filings (parsed from the SEC XML) — https://www.sec.gov/Archives/edgar/data/1508475/000110465926089994/tm2622150-1_4seq1.xml (Chen, RSU vest 83,544 on 2026-07-31) · https://www.sec.gov/Archives/edgar/data/1508475/000110465926069766/tm2616764-1_4seq1.xml (Shao, sale 60,000 @ $1.7133 on 2026-06-01) · plus the 2026-03-25, 2026-05-01 and 2026-05-19 filings under the same EDGAR path — transaction codes, prices, post-transaction holdings, and the absence of any 10b5-1 designation.
21. SEC, Point72 Asset Management / Steven A. Cohen SC 13G/A on VNET, filed 2026-08-14 — https://www.sec.gov/Archives/edgar/data/1508475/000091957426005501/primary_doc.xml — 109,989,366 Class A shares = 18,331,561 ADSs = **6.6%**, as of 2026-06-30, incl. 40,800 ADSs from call options.
22. SEC, Point72 SC 13G on VNET, filed 2026-01-09 (event date 2026-01-08) — https://www.sec.gov/Archives/edgar/data/1508475/000090266426000144/primary_doc.xml — 76,454,352 shares = 12,742,392 ADSs = **4.8%**; the baseline for the +43.9% build.
23. Morrison Foerster, "Section 16 Reporting Required for Foreign Private Issuers in 2026" — https://www.mofo.com/resources/insights/251224-section-16-reporting-required-for-foreign-private-issuers-in-2026 — HFIAA in the FY2026 NDAA (enacted 2025-12-18) extends Section 16(a) to FPI insiders effective 2026-03-18; Form 3s due that date. Explains why VNET Form 4 data now exists.
24. GlobeNewswire, GDS Holdings Q2 2026 results (2026-08-13) — https://www.globenewswire.com/news-release/2026/08/13/3344406/0/en/gds-holdings-limited-reports-second-quarter-2026-results.html — revenue RMB3,088.0M +6.5%; adjusted EBITDA RMB1,406.0M +2.5%, margin 45.5% vs 47.3% on higher utility costs; utilisation 79.2%; area under construction +43.9% QoQ; capex guide raised to ~RMB10bn from ~RMB9bn; FY revenue guide RMB12.7–13.0bn.
25. CNBC, "Chinese tech giant Tencent sees spending surge…" (2026-08-12) — https://www.cnbc.com/2026/08/12/china-tencent-earnings-q2-2026-gaming-ai-advertising.html — Q2 capex RMB52.8bn (+176% YoY, +65% QoQ), FCF −RMB13.8bn, "substantial increase" in 2026 capex weighted to H2.
26. StockTitan, VNET leadership change — https://www.stocktitan.net/news/VNET/vnet-announces-changes-to-leadership-qjxlj977kluh.html — CFO Qiyu Wang resigned effective 2026-04-30 for personal reasons, stated not related to operations, policies, accounting or internal practices.
27. PR Newswire, "VNET Appoints New Officer to Finance Leadership Team" (2026-02-13) — https://www.prnewswire.com/news-releases/vnet-appoints-new-officer-to-finance-leadership-team-302687596.html — Peter Zhihua Zhang appointed SVP, Operational Finance and principal accounting officer.
28. Investing.com, "Vnet Group stock may move 2% on earnings release" (2026-08-11) — https://www.investing.com/news/stock-market-news/vnet-group-stock-may-move-2-on-earnings-release-93CH-4852043 — cited **only** to record that its "2%" implied move and its historical implied-vs-actual table are internally inconsistent and should not be used.
29. MarketBeat, VNET trends and sentiment (as-of 2026-08-17) — https://www.marketbeat.com/stocks/NASDAQ/VNET/trends-and-sentiment/ — media mentions 6 → 4 (−33.3%); page views 2,235 → 1,921 (−14.0%); internal search 0 → 2.
30. Market Rebellion pre-market IV report, 2026-08-11 — https://marketrebellion.com/news/daily-iv-report/pre-market-iv-report-august-11-2026/ — VNET 30-day option IV 89 vs 52-week range 55–112 (**snippet_only**; page body did not render on fetch). Same search surfaced Barchart's unusual-call-volume flag for VNET on 2026-08-10 (**snippet_only**).
31. Telecompaper, "CATL affiliates to acquire 38% stake in Vnet for USD 940 million" — https://www.telecompaper.com/news/catl-affiliates-to-acquire-38-stake-in-vnet-for-usd-940-million--1571102 — PJ Millennium I/II to buy ~650.4M Class A shares (38.08%) at $1.4486/share, ~$942M, from Shandong Hi-Speed Holdings; close expected Q4 2026 subject to SDHG shareholder approval; buyers vote with founder.
32. Statista, business electricity prices in China — https://www.statista.com/statistics/1373596/business-electricity-price-china — ~11.6 US¢/kWh in April 2026 vs 8.7 US¢/kWh in June 2024.
33. Yahoo Finance chart API, USD/CNY — https://query1.finance.yahoo.com/v8/finance/chart/CNY=X — 6.7377 on 2026-08-17 (6.7428 on 2026-08-13).
34. Yahoo Finance chart API, GDS and BABA daily bars — https://query1.finance.yahoo.com/v8/finance/chart/GDS — GDS 2026-08-13 open 33.05, close 34.77 vs 32.74 prior close = **+6.20%**; 2026-08-14 close 34.41 = −1.04%. BABA series used for the China-ADR risk-appetite read.
35. PR Newswire, VNET Q2 2025 results (2025-08-21) — https://www.prnewswire.com/news-releases/vnet-reports-unaudited-second-quarter-2025-financial-results-302535608.html — Q2 2025 revenue RMB2.43bn +22.1%; wholesale +112.5%; adjusted EBITDA RMB732.5M +27.7%, margin 30.1% vs 28.8%; wholesale capacity in service 674MW (+101MW QoQ), utilised 511MW (+74MW QoQ). **snippet_only** (figures from the indexed release, page not fetched). These are the YoY comparables for the print.
36. StockTitan, VNET FY2025 results — https://www.stocktitan.net/news/VNET/vnet-reports-unaudited-fourth-quarter-and-full-year-2025-financial-c8a73pyze5uv.html — FY2025 revenue RMB9.95bn +20.5%; adjusted EBITDA RMB2.98bn +22.6%; year-end wholesale 889MW in service at 70.1% utilisation, 452MW under construction. **snippet_only.**
37. Kalkine, "Why VNET Group (NASDAQ: VNET) Stock Is Down lower Today" — https://kalkine.com/news/general-news/why-vnet-group-nasdaq-vnet-stock-is-down-lower-today — sole source for the claim that Goldman Sachs removed VNET from its APAC Conviction List, alongside debt-load and negative-retained-earnings bear points. **Uncorroborated; treated as colour only.**
38. Investing.com, "VNET raises $138 million through private share placement" — https://www.investing.com/news/company-news/vnet-raises-138-million-through-private-share-placement-93CH-4531730 — 81.0M new Class A shares at $1.70/share ($10.20/ADS), $137.7M, closing ~2026-03-03. **snippet_only.**
39. VNET IR, Q2 2025 scheduling release — https://ir.vnet.com/news-releases/news-release-details/vnet-announce-unaudited-second-quarter-2025-financial-results — establishes the 2025-08-21 report date used in the historical reaction table. Companion releases for the 2025-05-28, 2025-03-12 and 2024-11-20 dates were confirmed via the same IR path and indexed PR Newswire copies; the 2024-11-20 release specifies **after** the U.S. close with a call at 8:00 PM ET, which is why the Q3 2024 reaction is measured on 2024-11-21.
40. Nasdaq, VNET short interest and earnings pages — https://www.nasdaq.com/market-activity/stocks/vnet/short-interest and https://www.nasdaq.com/market-activity/stocks/vnet/earnings — both returned "Data is currently not available"; cited to document the gap.

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such.*
