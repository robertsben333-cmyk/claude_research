# ABM — ABM Industries Incorporated

**Event confirmed: YES.** ABM reports **fiscal Q3 2026 (quarter ended 31 July 2026) before the open on Tuesday 8 September 2026**, with a conference call at **8:30 AM ET**, per the company's own 25 August 2026 announcement [1].

**Two corrections to the framing this name arrived with.** First, stage 0 described this as "Q4" in one search path — it is **Q3 FY2026**; ABM's fiscal year ends 31 October [1][6]. Second, the plain-language window given ("after the US close on Monday 07 September") is technically void: **Monday 7 September 2026 is Labor Day and US equity markets are closed** [30]. The last traded price is Friday 4 September's close, and this print lands into a re-opening market after a three-day weekend, with no Monday session to pre-position in. Every price, IV and positioning figure below is therefore as-of 4 September 2026 by construction, not by staleness.

**What this print is about, in one paragraph.** It is not about revenue, and it is not really about the $1.01 headline. ABM's first half of FY2026 delivered adjusted EPS of **$1.73 — exactly flat against the $1.73 it did in H1 FY2025** ($0.83 vs $0.87 in Q1, $0.90 vs $0.86 in Q2) [7][6]. Management has nonetheless reaffirmed full-year adjusted EPS of **$3.85–$4.15** [6], which requires an H2 of **$2.12–$2.42 against a prior-year H2 of $1.70 — a 25% to 42% year-on-year step-up, built entirely on a promised back-half margin inflection in Technical Solutions**. The Street has largely taken the guide at face value (FY26 consensus $3.98 on 8 analysts [21]; Q3 consensus $1.01, revised *up* from $0.98 over 60 days [24]), which means the burden of proof on 8 September is: show one quarter of the inflection, or the whole guide breaks. Complicating it, ABM's $871.8M of cheap interest-rate swaps (1.72%–3.81%) were disclosed as "mostly maturing June 28, 2026" — i.e. inside the very quarter being reported [11] — and the FY26 EPS guide is stated "before any impact from prior-year self-insurance adjustments" while *reported* adjusted EPS, after an SEC-driven definitional change, now **includes** them [7][16][12]. That asymmetry produced a 19% headline "miss" last December that the market correctly ignored. It could produce another one here.

---

## 1. Event & anchors

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Event date | **2026-09-08** | confirmed | [1] |
| Session | **bmo**, call 8:30 AM ET | confirmed | [1] |
| Fiscal period | Q3 FY2026, quarter ended 2026-07-31 | — | [1][6] |
| Date changed / pre-announced? | No. Last 8-K of any kind was the 5 June Q2 release; **no 8-K, no press release and no Form 4 since 17 July** | 2026-09-07 | [2] |
| Spot | **$47.05** (Fri close; Mon 7 Sep is a market holiday) | 2026-09-04T20:00Z | [3][4][30] |
| Market cap | **$2.76B** | 2026-09-04 | [3] |
| Enterprise value | $4.63B | 2026-09-04 | [3] |
| Shares outstanding | 58.58M | 2026-09-04 | [3] |
| Forward P/E | 11.43 (stockanalysis) / 10.80 (finviz) | 2026-09-04 | [3][19] |
| EV/EBITDA | 10.51 | 2026-09-04 | [3] |
| Beta (5Y) | 0.67 / 0.64 | 2026-09-04 | [3][19] |
| Dividend yield | 2.47% ($0.29/qtr declared) | 2026-09-04 | [3][6] |
| **Event-implied move (ATM straddle, first expiry after report — 18 Sep 2026)** | **≈ 7.5% of spot** ($3.51 straddle; ATM IV 47.7%, 14 calendar days) | 2026-09-04 close snapshot | [5], my calculation |
| **Isolated earnings-jump (two-expiry decomposition)** | **σ_jump ≈ 6.8%; expected absolute move ≈ 5.4%** | same | [5], my calculation |
| IV30 (CBOE) | 36.43% | 2026-09-04 | [5] |
| IV rank / percentile | **unavailable** — no historical IV series reachable | — | see §12 |
| Realised 21d vol | **14.9%, 4th percentile of the last 2 years** (2y range 9.9 / 24.2 median / 51.9) | 2026-09-04 | [4], my calculation |
| Realised 63d / 252d vol | 22.9% / 27.6% | 2026-09-04 | [4], my calculation |
| 52-week range | $36.96 – $50.12 (intraday, finviz); closing high $49.36 on 2026-07-29 | 2026-09-04 | [19][4] |
| Avg daily volume | 340k (20d) / 500k (90d) | 2026-09-04 | [4] |

### Realised one-day earnings reactions

Computed by me from stockanalysis daily closes [4], with report dates taken from **SEC 8-K Item 2.02 filing dates** [2] rather than a vendor calendar. All ABM releases are BMO, so the reaction day is the filing date itself.

| Quarter | Report date | Prev close | Open | Close | **Close-to-close** | Gap | Intraday (open→close) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q2 FY26 | 2026-06-05 | 39.88 | 41.74 | 42.54 | **+6.67%** | +4.66% | +1.92% |
| Q1 FY26 | 2026-03-10 | 43.28 | 41.82 | 41.28 | **−4.62%** | −3.37% | −1.29% |
| Q4 FY25 | 2025-12-17 | 45.74 | 47.78 | 48.25 | **+5.49%** | +4.46% | +0.98% |
| Q3 FY25 | 2025-09-05 | 48.10 | 47.77 | 48.26 | **+0.33%** | −0.69% | +1.03% |
| Q2 FY25 | 2025-06-06 | 51.26 | 48.46 | 46.61 | **−9.07%** | −5.46% | −3.82% |
| Q1 FY25 | 2025-03-12 | 49.83 | 52.01 | 45.51 | **−8.67%** | **+4.37%** | **−12.50%** |
| Q4 FY24 | 2024-12-18 | 54.91 | 49.73 | 50.32 | **−8.36%** | −9.43% | +1.19% |
| Q3 FY24 | 2024-09-06 | 56.10 | 59.78 | 51.29 | **−8.57%** | **+6.56%** | **−14.20%** |
| Q2 FY24 | 2024-06-06 | 47.76 | 49.00 | 48.40 | **+1.34%** | +2.60% | −1.22% |
| Q1 FY24 | 2024-03-07 | 40.79 | 43.99 | 43.35 | **+6.28%** | +7.85% | −1.45% |
| Q4 FY23 | 2023-12-13 | 44.36 | 48.30 | 52.30 | **+17.90%** | +8.88% | +8.28% |
| Q3 FY23 | 2023-09-07 | 44.81 | 40.46 | 38.70 | **−13.64%** | −9.71% | −4.35% |

- **Last 6 quarters:** `[+6.67, −4.62, +5.49, +0.33, −9.07, −8.67]` · mean |move| **5.81%** · median |move| **6.08%** · max |move| **9.07%** · **3 up / 3 down**
- **Last 12 quarters:** mean |move| **7.58%** · median |move| **7.51%** · max |move| **17.90%** · **6 up / 6 down**
- **September prints specifically are the worst of the four:** 2023-09-07 −13.64%, 2024-09-06 −8.57%, 2025-09-05 +0.33%. Mean of the three September reactions is −7.3% versus +2.9% for the other nine. n=3 — colour, not a signal, but it is not nothing.
- **Fade risk is documented, not theoretical.** Twice in twelve prints ABM gapped *up* materially and closed *sharply down*: 2025-03-12 (+4.37% gap → −8.67% close, −12.50% intraday) and 2024-09-06 (+6.56% gap → −8.57% close, −14.20% intraday). Both were quarters where the release read fine and the *call* broke it. Anyone reading the 8-K headline at 07:00 ET has historically had a materially different picture from the 16:00 ET close.
- **Run-in matters here.** Across those 12 events, the 10-session return into the print correlates **+0.68** with the reaction (5-session: +0.67). My computation [4]. Today's run-in is essentially nil (see §6), which by that relationship argues for a muted, unbiased reaction — and is the single strongest piece of evidence *against* a large directional move.

---

## 2. The bar

| Metric | Consensus | Source |
| --- | --- | --- |
| Q3 FY26 adjusted EPS | **$1.01** | [19][20][24] |
| Q3 FY26 EPS, 60-day revision | **$0.98 → $1.01; 3 analysts up, 0 down** (as of ~2026-07-23) | [24] |
| Q3 FY26 revenue | **≈ $2.332B** (+~4% YoY) — `snippet_only` | [22][25] |
| Prior-year comparable (Q3 FY25) | Adjusted EPS **$0.82**; revenue **$2.224B**, organic +5.0% | [9] |
| Implied YoY on consensus | **EPS +23.2%**, revenue +4.9% | my calculation |
| FY26 consensus EPS | **$3.98** (8 analysts) | [21] |
| FY26 company guidance | **Adj. EPS $3.85–$4.15**; organic rev +3–4%, total +4–5%, segment op margin 7.8–8.0% (Q2: "low end"); interest ~$110M; tax 29–30% | [6][7][15] |
| Analyst count / rating | 8 analysts, consensus "Buy", avg PT **$52.43** (stockanalysis) — vs MarketBeat's 5-analyst "Hold" at **$47.00** | [21][17] |
| Zacks Rank | **#3 (Hold)**; industry in bottom 19% of Zacks industry ranks | [24] |
| Whisper number | **None found** — no credibly published whisper | — |

### What ABM has to deliver just to hold the stock flat

This is the arithmetic that dominates the print.

| | FY25 actual | FY26 |
| --- | --- | --- |
| Q1 adj EPS | $0.87 | $0.83 (−4.6%) |
| Q2 adj EPS | $0.86 | $0.90 (+4.7%) |
| **H1 adj EPS** | **$1.73** | **$1.73 (0.0%)** |
| H2 adj EPS | $1.70 (Q3 $0.82 + Q4 $0.88) | **required $2.12–$2.42** |
| **Implied H2 YoY growth required** | — | **+24.7% to +42.4%** |
| Full year | **$3.44** | guide $3.85–$4.15; consensus $3.98 |

Sources for every figure in that table: Q1 FY26 and Q1 FY25 adjusted EPS and the explicit prior-year restatement from the Q1 FY26 8-K [7]; Q2 FY26 from the Q2 8-K [6]; Q3 FY25 from the Q3 FY25 8-K [9]; Q4 FY25 and FY25 full-year $3.44 from the Q4 FY25 8-K [8]. My arithmetic on top.

At the **guide midpoint of $4.00**, the implied Q4 is $4.00 − $1.73 − $1.01 = **$1.26, or +43% on Q4 FY25's $0.88**. At the **low end of $3.85**, Q4 would still need $1.11, or +26%. There is no version of the reaffirmed guide that does not require a violent H2 acceleration from a company whose H1 was flat.

**The credibility overhang.** ABM guided FY2025 to $3.65–$3.80 (a range whose *lower end it raised* in March 2025 [10]), told the market in September 2025 it would land "toward the lower end" [9], and delivered **$3.44** [8] — roughly 6% below the bottom of its own reiterated range. It has now guided FY2026 to a range whose achievement requires a bigger H2 inflection than the one it failed to deliver in FY2025. Whatever the Street's $1.01 says, that history is the reason the stock trades at 11.4x forward earnings [3].

**But there is a real offset the bears under-weight.** The FY26 guidance is stated "adjusted EPS is expected to be in the range of $3.85 to $4.15, **before any impact from prior-year self-insurance adjustments**" [7], whereas *reported* adjusted EPS after the SEC-driven definitional change now **includes** those adjustments [16][12]. Consensus is a reported-basis number. In Q4 FY25, reported adjusted EPS of $0.88 carried a **$(0.26) prior-year self-insurance impact** [8] and printed against a $1.09 consensus — a 19% "miss" — **and the stock closed +5.49%** [4][20]. A mechanically identical event can happen again. This is the single largest source of headline/reality divergence in this name.

---

## 3. The one metric that matters

**Technical Solutions (ATS) segment operating margin, and whether management reaffirms $3.85–$4.15 without narrowing it.**

Not EPS, and not revenue. Revenue is the part nobody doubts — organic growth was 5.5% in Q1 and 6.1% in Q2, H1 new sales bookings were a record $1.2B, and ATS revenue grew 27.2% in Q2 [6][15]. The problem is that ATS grew revenue while *destroying* margin: ATS operating margin was **3.7% in Q1 FY26** [7], against **7.8% in Q3 FY25** ($19.4M on $249.5M [9]). Management's explanation is mix — Q2 was "heavy on equipment and infrastructure with lower margins" from large battery-energy-storage projects, and the fix is a shift toward "designing and engineering work versus turning the wrenches" in H2 [15].

**What the market expects for it, and how I know.** Management said on the Q2 call, verbatim: *"We expect healthy sequential margin improvement in the third and fourth quarters, driven by improved mix in ATS and our ongoing price escalation and cost actions"*, and framed H2 as *"a significant step up in both earnings and margin"* [15]. Simultaneously they moved consolidated segment operating margin guidance to the **low end** of the 7.8–8.0% range [6] — i.e. they had already begun walking the profitability guide down while holding the EPS guide. The Street's $1.01 for Q3 is the numerical expression of believing the ATS mix shift starts landing in the July quarter.

**Concretely, what to watch in the 07:00 ET release:** ATS segment operating profit in dollars. Q3 FY25 was $19.4M on $249.5M revenue [9]. With ATS revenue plausibly near $300M+ (Q2 was $267M, +27% YoY [6]), a Q3 ATS operating profit **below roughly $22M** says the mix shift has not started and the FY guide is arithmetically finished. Above ~$28M and the hockey stick is live. That number, not EPS, is the print.

Second-order tell in the same release: consolidated **segment operating margin**. Q2 was 7.3% versus 7.9% a year earlier [6]. Anything still below 7.8% in a seasonally-strong Education quarter [15] is a problem.

---

## 4. Fundamentals — what changed, what is at stake

**Segment mix (Q2 FY26, quarter ended 30 Apr 2026)** [6]:

| Segment | Revenue | YoY | Note |
| --- | --- | --- | --- |
| Business & Industry | $1,016M | flat | ~44% of revenue; the legacy office-cleaning core |
| Manufacturing & Distribution | $464M | +16.5% | |
| Aviation | $311M | +19.5% | |
| Education | $232M | +1.9% | seasonally strongest in fiscal Q3 |
| Technical Solutions (ATS) | $267M | +27.2% | the margin swing factor |
| **Total** | **$2,290M** | **+8.4%** (organic +6.1%, acquisitions +2.3%) | record Q2 |

**What changed since the last print (5 June 2026):**

1. **The interest-rate swaps rolled off inside the reported quarter.** The Q2 10-Q discloses seven swaps totalling **$871.8M notional at fixed rates of 1.72%–3.81%, "mostly maturing June 28, 2026"**, against a weighted-average borrowing rate excluding swaps of **5.66%** [11]. Fiscal Q3 ran 1 May – 31 July 2026, so roughly one third of the quarter — and all of Q4 — carries un-hedged pricing on that notional. *My inference, clearly labelled as mine:* repricing ~$872M from a ~2.8% blended fixed rate to ~5.66% is on the order of **$25M annualised pre-tax, ~$6M per quarter, ~$0.07/share after tax** on ~59M shares. That is 7% of the $1.01 consensus. Management raised the FY26 interest-expense guide from $95–105M to **~$110M** at Q2 [6][15], so this is partly contemplated — but it is contemplated inside the same guide that also requires a 25–42% H2 earnings acceleration.
2. **No news flow at all.** No 8-K, no press release and no Form 4 since 17 July 2026 [2]. For a company mid-way through a promised inflection, silence is neutral-to-mildly-negative: there has been no positive pre-announcement, and no negative one either.
3. **Nothing in the tape.** The stock is −3.09% over 21 sessions and +0.51% over 10, versus +10.60% since the Q2 print [4]. The post-Q2 enthusiasm peaked at $49.36 on 29 July and has bled since.

**Unit economics and margin trajectory.** Consolidated segment operating margin 7.3% in Q2 vs 7.9% prior year [6]; ATS margin 3.7% in Q1 [7]. Adjusted EBITDA $131.7M in Q2 (5.75% of revenue) vs $125.9M [6]; $117.8M in Q1 [7]. FY25 adjusted EBITDA margin was 5.9% [8], against an FY25 guide of 6.3–6.5% [9] — another guide missed.

**Free cash flow.** H1 FY26 FCF was **$71.3M** (Q1 $48.9M + Q2 $22.4M) [7][6]. FY26 guidance is **~$250M before transformation and integration costs**, with those excluded items running ~$65M annually including ~$20M of remaining ELEVATE transformation cost [26]. So H2 must produce roughly $180M of the guided FCF — the same hockey stick as EPS, on the cash line. Note that FY25 FCF was $155.1M [8] and that Q3 FY25 alone delivered $150.2M of FCF [9], so Q3 is seasonally the cash quarter; a weak Q3 FCF print would be a loud signal.

**Balance sheet and capital allocation.** Total debt $1,863.4M ($821.9M term loan + $1,045.0M revolver drawn), $518.9M revolver capacity available, weighted-average rate 5.66% ex-swaps [11]. Leverage **3.2x** at Q2, against a stated intention to be **below 3.0x by fiscal year-end**, with management calling debt repayment "our near-term priority" [6][15]. Goodwill $2,738.4M, up from $2,591.1M, on WGNSTAR ($146.0M) and LMC ($14.1M) — no impairment taken [11]. Buyback: 2.13M shares for $94.1M in H1 at an average $44.17, with **$89.0M remaining** of the $150M authorisation expanded 3 September 2025 [11]. Diluted share count fell to 60.7M in Q1 FY26 from 63.2M [7] and 59.9M for the H1 average from 63.1M [11] — roughly a **5% share-count tailwind** that is doing meaningful work inside the required 23% Q3 EPS growth.

**M&A.** WGNSTAR closed February 2026 for ~$275M, adding semiconductor fab services — 60+ clients, 300+ sites, presence in 75% of US/European fab capacity [15][27]. Combined with the 2024 Quality Uptime data-centre acquisition and RavenVolt microgrids, **~7% of ABM revenue now comes from semiconductors and data centres** [15]. This is the strategic bull case and the reason ATS revenue is compounding at 20–27%.

**Customer concentration:** **not disclosed** in the Q2 FY26 10-Q [11]. See §12.

---

## 5. Positioning & options

Options data below is computed by me from the **CBOE delayed-quote chain snapshot timestamped 2026-09-06 00:55 UTC**, which reflects the Friday 4 September close (spot $47.05 matches) [5].

**IV term structure — clean earnings backwardation:**

| Expiry | Days | ATM IV | ATM straddle (% of spot) |
| --- | --- | --- | --- |
| **2026-09-18** (first after event) | 14 | **47.7%** | **7.46%** |
| 2026-10-16 | 42 | 38.5% | 10.42% |
| 2027-01-15 | 133 | 32.8% | 15.81% |

Two-expiry decomposition of the front and second month gives a **non-event base vol of ~32.9%** and an **isolated earnings-jump σ of 6.77%**, i.e. an expected absolute event-day move of **~5.4%**. The headline 7.46% straddle number overstates the event because ABM has **no weekly options** — the nearest expiry is ten trading days *after* the print, so it prices the event plus two weeks of ordinary vol.

**The options market here is thin to the point of being barely informative, and this matters.** The stage-0 note that ABM has an "active listed options market" is an overstatement. The 18 September expiry has **$5 strike spacing, total open interest of 93 contracts across all strikes, and Friday volume of 378 contracts** [5]. Quotes are wide to absurd — the 18 Sep $50 call was 0.15 bid / 1.15 offered. Across *all eight* listed expiries, total open interest is 2,776 calls and 381 puts. **Treat the implied move as a derived estimate with wide error bars, not as a market consensus.**

**Skew:** essentially flat at the front. 18 Sep: $45 call IV 48.7% vs $45 put IV 49.2%; $50 call 44.9% vs $50 put 46.9%; $55 call 47.8% [5]. No pronounced put bid, no crash-hedging.

**Put/call:** all-expiry OI ratio 0.14 (call-heavy, but that is two stale Jan-27 call lines of 467 and 392 contracts, not a live signal). Friday volume: 234 calls / 191 puts, ratio 0.82 [5]. Ortex independently reports the put/call ratio at 0.14, "slightly above its 20-day average, not extreme" [23].

**Short interest** — settlement date **14 August 2026** [18]:
- 1,884,396 shares short (**3.25% of float**), **−3.03% vs the prior report** (1,943,345)
- **Days to cover 5.6** [18]. Note vendors disagree: finviz shows short ratio 3.54 [19], stockanalysis 4.63 [3]. All three are consistent with "a few days" — nothing squeezable.
- Peak was ~3.0M shares (5.2% of float) in **May 2026**; the position has been cut by roughly a third since [18]
- Ortex: short interest 3.2% of free float, **down ~25% over the past month**, **borrow cost recently below 0.35%** [23]. (Ortex also prints a "utilisation >1,500%" figure that is not a coherent number; I am disregarding it.)

**Ownership:** institutional 102.47% (float-based artefact), insider 1.59%, insider transactions −5.63% over the trailing window [19].

**Run-in / crowding:**

| Window | Return |
| --- | --- |
| 1 session | −0.38% |
| 5 sessions | −0.32% |
| 10 sessions | +0.51% |
| 21 sessions | −3.09% |
| Since Q2 print (3 mo) | +10.60% |
| 6 months | +7.32% |
| 12 months | −2.18% |

Computed from [4]. RSI(14) 49.2, price −0.55% vs SMA20, +0.19% vs SMA50, +8.14% vs SMA200 [19]. **The stock is sitting on its 50-day, un-extended, with no directional run-in.** Realised 21-day vol at **14.9% is the 4th percentile of the last two years** [4] — the tape has gone completely quiet into an event with a 12-quarter mean absolute reaction of 7.6%.

**How crowded is the trade? It is not.** Short interest falling and modest, borrow essentially free, options open interest trivial, no options skew, no run-in, retail attention nil (§6), 20-day volume (340k) running a third below the 90-day average (500k) [4]. There is no consensus position to squeeze in either direction. That is a genuine reason to expect a *smaller* move than history suggests, and it cuts against my own directional lean.

---

## 6. Sentiment & alt-data

**Retail / social: effectively zero.** ABM's Stocktwits symbol page has **686 watchers**. The 30 most recent messages span **20 February to 5 August 2026** — over five months — and only **three carry a sentiment tag (all Bullish)**. **There has been no message at all in the last month**, and the last three before that were unrelated options-pump posts [28]. There is no 7/14/30-day retail sentiment *trend* to report because there is no retail sentiment. For a $2.8B NYSE name reporting tomorrow, this is the cleanest possible evidence of an uncrowded, un-narrativised print. Treat as supporting colour only.

**Analyst rating changes and price-target drift** [17]:

| Date | Firm | Analyst | Action | Old → New |
| --- | --- | --- | --- | --- |
| 2026-08-11 | Weiss Ratings | — | Upgrade | Hold (C) → Hold (C+) |
| 2026-06-08 | Robert W. Baird | Andrew Wittmann | Raise target, **Neutral** maintained | $45 → $48 |
| 2026-03-11 | UBS | Joshua Chan | Lower target | $51 → $45 |
| 2026-03-11 | Truist | Jasper Bibb | Lower target | $47 → $45 |
| 2026-03-11 | Maxim Group | Tate Sullivan | **Upgrade Hold → Buy** | → $50 |

MarketBeat's consensus PT is **$47.00 — unchanged at 1 month, 3 months, and versus $56.00 a year ago** [17]; stockanalysis puts the 8-analyst average at **$52.43** (low $45, high $68) [21]. The two disagree because they cover different analyst sets; the honest summary is **the sell side has done nothing since June, and what it did in March was cut**. There is no target-raising cycle into this print.

**Estimate revisions:** the only granular series I could source is Zacks via [24] — over the 60 days to ~23 July 2026, **three analysts raised the current-quarter estimate and none lowered it, taking consensus $0.98 → $1.01**. StockStory's preview characterises analysts as having "generally reconfirmed their estimates over the last 30 days" [22]. So: **mildly positive revisions, entirely stale (six weeks old), and no 7/30/90-day breakdown obtainable** — the Zacks detailed-estimates page is bot-blocked (§12).

**Alt-data:** Google Trends returned HTTP 429 (rate-limited) and I could not source a trend series [29]. App-rank, web-traffic and review proxies are not meaningful for a B2B outsourced-services contractor. Job postings were not sourced. The relevant "alt-data" for ABM is office occupancy, and Kastle-derived data has weekly office occupancy at **56.3%, the highest since early 2020**, with Q1 2026 office net absorption of 6.9M sq ft — the eighth consecutive quarter of positive demand and the best Q1 since 2020 [31] (`snippet_only`). That is a slow tailwind for Business & Industry, but management explicitly flagged **West Coast vacancy running "2 or 3x worse than New York City"** [15], so the national average flatters ABM's actual mix.

---

## 7. Forensics

**Form 4 activity — all sales, no purchases, mostly planned** [2] and the underlying XML filings [13]:

| Filed | Insider | Role | Date | Code | Shares | Price | Held after | 10b5-1? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-17 | Raul Valentin | EVP & CHRO | 2026-07-16 | S | 1,639 | $48.00 | 49,036 | **Yes** — plan dated 2026-04-15 |
| 2026-07-15 | **Dean A. Chin** | **SVP & Chief Accounting Officer** | 2026-07-13 | S | 3,958 | $45.31 | 16,993 | **No 10b5-1 footnote** |
| 2026-07-06 | David M. Orr | EVP & CFO | 2026-07-01 | **F** (tax withholding) | 539 | $44.54 | 36,034 | n/a — not a discretionary sale |
| 2026-06-12 | Scott B. Salmirs | President & CEO | 2026-06-12 | S | **50,000** (two lots) | $46.25 / $46.69 | 395,285 | **Yes** — plan dated 2025-12-24 |
| 2026-02-10 | Rene Jacobsen | EVP & COO | 2026-02-09 | S | 9,339 | $47.23 | 41,626 | **Yes** |

Two observations. **(a) The CEO's 50,000-share, ~$2.3M June sale was under a plan entered 24 December 2025** — before the Q1 miss and well before any Q3 visibility. It is not a signal. **(b) The Chief Accounting Officer's 13 July sale of 3,958 shares at $45.31 carries no Rule 10b5-1 footnote** — the only footnotes are the weighted-average-price undertaking and the standard dividend-reinvestment note [13]. Every other selling insider's Form 4 explicitly names a plan. This is a small sale (~$179k, and he retained 16,993 shares), it was five weeks after the Q2 print and roughly two weeks before quarter-end, and it is entirely consistent with routine tax/diversification behaviour — but a *discretionary* sale by the **Chief Accounting Officer** is the one Form 4 in this set worth flagging. **My read: weak negative, low confidence.** There were also 144 filings on 2026-06-12, 2026-07-13 and 2026-07-16 matching those sales [2]. **No insider has made an open-market purchase** in the period reviewed [23].

**Auditor / restatement / SEC issues — resolved but instructive.** EDGAR shows a full SEC comment-letter cycle on ABM's non-GAAP presentation: **UPLOAD 2025-03-06 → CORRESP 2025-03-28 → UPLOAD 2025-04-25 → CORRESP 2025-05-01 → UPLOAD 2025-05-07** [2]. The 1 May 2025 letter, signed by then-CFO **Earl R. Ellis**, states the Staff's comment concerned "our non-GAAP reconciliation presented in the Form 8-K filed on December 18, 2024, specifically related to the adjustment for 'Prior year self-insurance adjustment'", and commits ABM to "revise our presentation in future filings and earnings materials to exclude the Prior year self-insurance adjustment from our calculation of non-GAAP financial measures" [12]. ABM implemented this in the **17 December 2025** Q4 FY25 release: *"After communications with the staff of the Securities and Exchange Commission, we have revised the definition of our non-GAAP financial measures… This definitional change has been applied to our fourth quarter 2025 results and retroactively to all presented periods"* [16]. **No restatement of GAAP figures; no auditor change; no 10-K/A or 10-Q/A on file** [2].

**The live consequence of that history:** ABM's FY26 *guidance* is expressed "before any impact from prior-year self-insurance adjustments" [7] while its *reported* adjusted EPS includes them. **Consensus is a reported-basis number and guidance is not.** Any adverse actuarial development on prior accident years flows straight into the headline miss. Precedent: FY24 saw prior-period self-insurance claims increase by **$20.3M** [32], and Q4 FY25's adjusted EPS carried a **$(0.26)** hit from the same source [8].

**Executive and director changes.** CFO transition: on 6 June 2025 the board appointed **David Orr** EVP & CFO, succeeding **Earl Ellis** (CFO since November 2020), with Ellis serving as senior advisor until no later than 5 September 2025 and receiving **severance for a termination without cause** [14]. The 8-K carrying it is the 2025-06-10 Item 5.02 [2]. *My inference, labelled as mine:* the CFO change came roughly five weeks after ABM conceded the SEC's non-GAAP point, and the severance treatment ("without cause") is not the language of a voluntary retirement. I have found **no evidence** connecting the two, and internal-promotion succession is the ordinary reading — but the sequencing is worth the panel knowing. On 29 October 2025 the board **added** Barry A. Hytinen as a director, expanding the board from eleven to twelve [33] — an addition, not a departure, and the only 5.02 since. **No auditor change, no director resignation, no restatement.**

**8-K cadence and filing-language shifts.** The cadence is metronomic: four earnings 8-Ks a year plus credit-agreement and governance items [2]. The 2026-02-05 8-K (Items 1.01/2.03) was the term loan for the WGNSTAR acquisition [2][23]. **There has been no 8-K since 5 June 2026** — no pre-announcement, no guidance update, no negative signalling of any kind. **Legal:** accrued probable litigation losses $8.3M, reasonably-possible range zero to $15.1M, "we are currently not a party to any material legal proceedings"; **no risk-factor updates** beyond the FY25 10-K [11]. **ELEVATE transformation** charges were $6.8M in H1 FY26, $20.1M cumulative, expected to complete in 2026 [11].

**One data-quality trap for the panel.** A TradingView headline circulating in search results reads *"ABM Industries 3Q 2026: Revenue $2.29B, EPS $0.73 — 10-Q Summary"* [34]. Those figures are **Q2 FY26** ($2.29B revenue, $0.73 GAAP EPS [6]) mislabelled as Q3. **ABM has not reported Q3 FY2026.** Any downstream reader encountering that headline should discard it.

---

## 8. Macro & peer read-through

**Regime: hawkish, and unhelpfully so for this name.** The 4 September August payrolls print came in at **+162,000 against a ~53–55k consensus** with unemployment steady at 4.1%; short-end Treasury yields rose sharply and CME FedWatch odds of a **quarter-point rate _hike_** at the 15–16 September FOMC jumped to **~58%** (Bloomberg ~63%) [35][36] (`snippet_only`). Average hourly earnings rose 0.3% m/m and **+3.1% y/y** [36]. CPI and PPI land the week *after* ABM reports, so ABM prints into an unresolved hawkish overhang, on the first session after a holiday.

**Why that matters specifically for ABM.** (i) It is a **levered small cap** — $1.86B of debt, 3.2x leverage, and $871.8M of hedges that just expired [11] — so a hike repricing is a direct earnings headwind, not an abstraction. Commentary in the same coverage flags that small caps "contend with a much higher cost of capital than large-cap peers" and may face turbulence until Q3 earnings [35]. (ii) It is **labour-intensive**; wage growth of 3.1% running *below* PCE inflation [36] is actually a mild positive for the cost line, and ABM management claims "really good visibility on our cost basis" and AI-generated price-escalation letters to recapture wage inflation [15]. (iii) Beta is only 0.64–0.67 [19][3], so the macro is a valuation and interest-expense channel more than a sentiment channel.

**Peers who have already reported — demand is confirmed, margin is not.**

| Peer | Reported | Result | Reaction |
| --- | --- | --- | --- |
| **Aramark (ARMK)** | 2026-08-11 | Adj. EPS $0.52 vs $0.48; revenue $5.1B, +9%, vs $4.92B est.; **raised** FY26 organic revenue growth to 9–10% from 7–9%; data-centre hospitality business ramping faster than expected | **+6% to +8.9%** on the day (`snippet_only`) [37] |
| **Cintas (CTAS)** | 2026-07-15 | FQ4 revenue $2.91B, +8.9%, organic +8.4%; adj. EPS $1.29, +18.3%; gross margin 51.0%, an all-time high; FY27 adj. EPS guide $5.36–$5.50 | not sourced [38] |
| **Healthcare Services Group (HCSG)** | FQ1 2026 | Revenue $462.8M, +3.4%; Environmental Services $208.3M at 12.1% margin; reiterated mid-single-digit growth | not sourced [39] |

**The read-through is asymmetric and it is the most useful thing in this section.** Aramark and Cintas both confirm that **outsourced facility-services demand is strong and that data-centre-adjacent service revenue is a genuine 2026 growth vector** — which supports ABM's top line and the ATS revenue trajectory, and makes a *revenue* miss on 8 September unlikely. Neither peer, however, says anything about ABM's actual problem: **the margin on equipment-heavy energy and infrastructure projects.** Cintas beat on gross margin at an all-time high; ABM's consolidated segment margin went the other way in Q2 (7.3% vs 7.9% [6]). If ABM misses, it will not be because the end market is soft — it will be because ABM converted the demand at a bad margin. Peer strength therefore raises, not lowers, the bar for an in-line print to be rewarded.

**Customer/supplier read-throughs.** ABM's ATS demand cited on the Q2 call ties to nationwide battery-storage installations up 52% in 2025, double-digit global data-centre construction growth, and continued double-digit semiconductor revenue growth via WGNSTAR [15]. Aviation ties to TSA throughput near 3M passengers/day [15]. Both are corroborative but neither is a quarter-specific tell.

---

## 9. Bull case / bear case / base case

**Bull case.** The demand side is unambiguous and externally corroborated: ABM has posted 5.5% and 6.1% organic growth in the two reported FY26 quarters, record H1 bookings of $1.2B, and ATS revenue +27% [6][7][15], while Aramark raised its organic revenue guide on data-centre-driven strength and Cintas printed 8.4% organic with record gross margin [37][38]. The margin problem is mix, not price — Q2's ATS drag came from equipment-heavy battery-storage projects, and management has said explicitly that H2 shifts toward "designing and engineering work" [15]. Meanwhile a ~5% year-on-year diluted share reduction (60.7M from 63.2M; 59.9M H1 average from 63.1M) does a quarter of the work in the required EPS step-up for free [7][11], Education is seasonally strongest in fiscal Q3 [15], and the WGNSTAR/LMC quarters are now full ones. Positioning offers no resistance: short interest is 3.25% of float and falling, borrow is under 0.35%, options open interest at the front expiry is 93 contracts, there is no put skew, retail watchers number 686 with no post in a month, and the stock has not run (−0.32% over five sessions) [18][23][5][28][4]. At 11.4x forward against FY26 EPS growth of ~16% [3][21], very little is priced. And there is a live precedent for the market looking straight through a bad headline: Q4 FY25 printed adjusted EPS of $0.88 versus $1.09 consensus — a 19% miss — carrying $(0.26) of prior-year self-insurance, **and the stock closed +5.49%** [8][20][4].

**Bear case.** The bar is not $1.01 — it is the arithmetic behind it, and the arithmetic is brutal. H1 FY26 adjusted EPS was $1.73, **identical to H1 FY25's $1.73** [7][6], yet the reaffirmed $3.85–$4.15 guide requires H2 of $2.12–$2.42 against a prior-year H2 of $1.70: **+25% to +42%** [8]. Consensus $1.01 for Q3 is +23% year-on-year off a base ($0.82 [9]) that ABM has not grown past in six months. This company already failed exactly this test one year ago: it guided FY25 to $3.65–$3.80, *raised the lower end* in March [10], said "toward the lower end" in September [9], and delivered **$3.44** [8]; its FY25 adjusted EBITDA margin came in at 5.9% against a 6.3–6.5% guide [8][9]. The erosion has already restarted — Q1 FY26 missed at $0.83 versus $0.87 consensus with ATS margin at 3.7% [7][20], and at Q2 management quietly moved segment operating margin to the **low end** of 7.8–8.0% while holding EPS [6]. Into that, three concrete H2 headwinds land: the **$871.8M of 1.72–3.81% swaps "mostly maturing June 28, 2026"** repricing against a 5.66% ex-swap rate, inside the reported quarter [11]; the **Transport for London exit worth ~300bp of B&I growth in the back half** plus West Coast CRE vacancy running 2–3x New York's [15]; and leverage at 3.2x against a sub-3.0x year-end target that constrains the buyback to $89M remaining [6][11]. Free cash flow tells the same story — $71.3M in H1 against a ~$250M guide [7][6][26]. Because the guide is stated "before any impact from prior-year self-insurance adjustments" while reported adjusted EPS now includes them [7][16], the *reported* number carries one-way downside risk with a $(0.26) precedent [8]. And ABM has a documented habit of gapping up on the release and closing sharply lower once the call happens — twice in twelve prints, including −12.5% and −14.2% intraday reversals [4].

**Base case.** Revenue comes in fine — probably at or slightly above the ~$2.33B consensus, given 6%+ organic momentum, full quarters of WGNSTAR/LMC, and peer confirmation [22][6][37][38]. ATS margin improves *sequentially* from the Q1/Q2 trough but not enough to make the full-year arithmetic work, and management responds the way it has each of the last three quarters: it narrows rather than abandons, guiding to the low end of $3.85–$4.15 or trimming the top of the range while pointing at Q4. That is precisely the Q1 FY26 setup, which produced −4.62% [4]. Offsetting that, the market has almost nothing at risk here — no run-in, no crowding, realised vol at the 4th percentile of two years, and a 10-session run-in of +0.51% that, on the +0.68 historical relationship, argues for a muted reaction [4]. So I expect a **modest down day rather than a violent one**, with the isolated event-implied move of ~5.4% [5] looking roughly fair-to-slightly-rich given how uncrowded the name is. The genuine tail risk in both directions is the call, not the release.

---

## 10. What would flip the consensus view

**The most credible reversal is a clean, quantified ATS margin inflection in the 07:00 ET release.** Specifically: Technical Solutions segment operating profit of roughly **$28M or better** on ~$300M of revenue — i.e. ATS margin back near 9%, versus 3.7% in Q1 and 7.8% in Q3 FY25 [7][9] — accompanied by consolidated segment operating margin at or above 7.8% and an *unnarrowed* reaffirmation of $3.85–$4.15. That combination would validate the "design and engineering versus turning the wrenches" mix thesis in the one quarter where the bears have said it cannot happen [15], make the $1.26 implied Q4 credible rather than heroic, and re-rate a stock trading at 11.4x with a 2.5% yield and a shrinking share count [3]. Given how uncrowded the setup is — 3.25% short and falling, front-expiry open interest of 93 contracts, 686 retail watchers, no run-in [18][5][28][4] — there is no positioning to absorb that, and the Q2 FY26 print (+6.67%) and Q4 FY23 print (+17.90%) show what ABM does when it clears a bar nobody expected it to clear [4].

**The mirror-image flip for the bulls** is narrower but equally concrete: a prior-year **self-insurance charge** in the release. Because guidance excludes it and consensus includes it [7][16], a $(0.20)+ development would manufacture a headline "miss" of ~20% that says nothing about the operating business. If the panel sees a big EPS miss on 8 September, the first thing to check is the self-insurance line — Q4 FY25 is the template, and the market got that one right by rallying 5.49% [8][4].

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **IV rank / IV percentile — unavailable.** No historical IV30 series reachable; CBOE gives a point-in-time IV30 only [5]. | Cannot say whether 47.7% front IV is cheap or rich *for ABM*. Partially mitigated: realised 21d vol is at the 4th percentile of two years [4], so the vol risk premium is unusually wide in absolute terms. |
| **No published third-party implied move.** TipRanks' 3 Sep implied-move list does not include ABM [25]; SpotGamma's free tool renders client-side [40]. Both my figures (7.46% straddle, 5.4% isolated jump) are **my own derivation** from a delayed CBOE chain with 93 contracts of front open interest [5]. | The panel should treat the implied move as an estimate with wide error bars, not a market consensus. This is the weakest anchor in the dossier. |
| **Q3 FY26 consensus revenue ($2.332B) is `snippet_only`** [22][25]. | Sets the revenue bar; not independently confirmed from a fetched page. |
| **No 7/30/90-day estimate-revision breakdown.** Zacks detailed-estimates and StockStory pages are bot-blocked (403 / "Pardon Our Interruption"); SimplyWallSt returned 403. Only the 60-day $0.98→$1.01 figure, as of ~23 July, was obtainable [24]. | Six-week-old revision data cannot tell us whether the Street has moved *since* the summer. |
| **No whisper number found.** | Removes one read on the true bar. |
| **Customer concentration not disclosed** in the Q2 FY26 10-Q [11]. | Cannot size single-client risk beyond the TfL exit management volunteered [15]. |
| **Days-to-cover disagreement:** 5.6 [18], 4.63 [3], 3.54 [19]. | All say "not squeezable"; the spread does not change the conclusion. |
| **Borrow fee (<0.35%) and short-interest trend (−25% m/m) come from Ortex commentary** [23], a lower-tier source; the same page prints an incoherent "utilisation >1,500%". Not corroborated by a primary lender source. | Borrow economics are a supporting, not load-bearing, claim. |
| **Google Trends unavailable** — HTTP 429 rate-limit [29]. No web-traffic, app-rank or job-posting proxy sourced. | Low cost: none of these are meaningful for a B2B outsourced-services contractor. |
| **Cintas and HCSG day-of stock reactions not sourced**; Aramark's +6–8.9% is `snippet_only` [37]. | Weakens the "how peers traded" half of the peer read-through; the *fundamental* read-through is well sourced. |
| **FY26 free-cash-flow guidance ($250M before transformation costs) is `snippet_only`** [26] and does not reconcile cleanly with a transcript remark about "$100M through H1" versus the $71.3M I compute from the two 8-Ks [7][6]. | I have used the primary-source $71.3M. The $250M target should be verified against the release on the day. |
| **Domains unreachable this session:** `investor.abm.com` (repeated 60s timeouts), `nasdaq.com` (503), `zacks.com` (bot wall), `stockstory.org` (403), `simplywall.st` (403), `trends.google.com` (429), Yahoo options API (crumb auth). | Recorded per the network policy. All materially affected figures are flagged above. |

**Interest-expense arithmetic in §4 is my own inference**, not a sourced figure: the $871.8M notional, the 1.72–3.81% fixed rates, the "mostly maturing June 28, 2026" language and the 5.66% ex-swap rate are all sourced [11]; the ~$0.07/share quarterly impact is my calculation and depends on assumptions about the blended swap rate and refinancing that ABM has not disclosed.

---

## 12. Sources

1. [ABM to Announce Third Quarter 2026 Financial Results — GlobeNewswire, 2026-08-25](https://www.globenewswire.com/news-release/2026/08/25/3350870/799/en/abm-to-announce-third-quarter-2026-financial-results.html) — event date, BMO session, 8:30 AM ET call, fiscal Q3 2026.
2. [SEC EDGAR submissions, CIK 0000771497](https://data.sec.gov/submissions/CIK0000771497.json) — authoritative 8-K Item 2.02 earnings dates back to 2019, Form 4 and 144 list, comment-letter cycle, absence of any 8-K since 2026-06-05, absence of 10-K/A or 10-Q/A.
3. [ABM Industries statistics — stockanalysis.com](https://stockanalysis.com/stocks/abm/statistics/) — spot $47.05 as of 2026-09-04 16:00 EDT, market cap $2.76B, EV $4.63B, 58.58M shares, forward P/E 11.43, EV/EBITDA 10.51, cash $95.9M, debt $1.97B, beta 0.67, dividend yield 2.47%, short data.
4. [stockanalysis.com daily price history API, 5Y](https://stockanalysis.com/api/symbol/s/abm/history?range=5Y&period=Daily) — all twelve earnings-day close-to-close/gap/intraday moves, run-in windows, realised-vol percentiles, 52-week closing range, volume trend. All derived figures are my calculations on this series.
5. [CBOE delayed option quotes, ABM](https://cdn.cboe.com/api/global/delayed_quotes/options/ABM.json) — 2026-09-06 00:55 UTC snapshot of the 2026-09-04 close: IV30 36.43%, full chain by expiry, ATM IVs (47.7 / 38.5 / 32.8), strike spacing, open interest, volume, skew. Straddle and two-expiry earnings-jump decomposition are my calculations.
6. [ABM Q2 FY2026 8-K exhibit 99.1 (SEC), filed 2026-06-05](https://www.sec.gov/Archives/edgar/data/0000771497/000119312526258367/abm-ex99_1.htm) — Q2 revenue $2,290M +8.4% (organic 6.1%), adj. EPS $0.90 vs $0.86, GAAP $0.73, adj. EBITDA $131.7M, all five segments, segment margin 7.3% vs 7.9%, OCF $66.2M, FCF $22.4M, leverage 3.2x, $0.29 dividend, reaffirmed $3.85–$4.15, segment margin to "low end", interest ~$110M.
7. [ABM Q1 FY2026 8-K exhibit 99.1 (SEC), filed 2026-03-10](https://www.sec.gov/Archives/edgar/data/771497/000119312526099334/abm-ex99_1.htm) — revenue $2,243M +6.1% (organic 5.5%), adj. EPS **$0.83 vs $0.87 prior year**, GAAP $0.64 vs $0.69, diluted shares 60.7M vs 63.2M, ATS margin 3.7%, all segments, FCF $48.9M, leverage 2.9x, $91.1M buyback, and the guidance language "**before any impact from prior-year self-insurance adjustments**".
8. [ABM Q4 & FY2025 8-K exhibit 99.1 (SEC), filed 2025-12-17](https://www.sec.gov/Archives/edgar/data/771497/000119312525321680/abm-ex99_1.htm) — Q4 revenue $2.3B +5.4%, adj. EPS $0.88 including a **$(0.26)** prior-year self-insurance impact, adj. EBITDA $124.2M / 5.6%, **FY25 adj. EPS $3.44**, FY25 EBITDA margin 5.9%, FY25 FCF $155.1M, and the original FY2026 guidance.
9. [ABM Q3 FY2025 8-K exhibit 99.1 (SEC), filed 2025-09-05](https://www.sec.gov/Archives/edgar/data/771497/000077149725000020/abm-ex99_1.htm) — the year-ago comparable: revenue $2,224M +6.2% (organic 5.0%), **adj. EPS $0.82**, GAAP $0.67, adj. EBITDA $125.8M / 5.9%, ATS $249.5M revenue / $19.4M operating profit, FCF $150.2M, and "toward the lower end" of $3.65–$3.80.
10. [ABM Q1 FY2025 8-K exhibit 99.1 (SEC), filed 2025-03-12](https://www.sec.gov/Archives/edgar/data/771497/000095017025037617/abm-ex99_1.htm) — Q1 FY25 adj. EPS $0.87, and confirmation ABM **raised the lower end** of its FY25 EPS guide to $3.65–$3.80 before missing it.
11. [ABM Form 10-Q for the quarter ended 2026-04-30 (SEC)](https://www.sec.gov/Archives/edgar/data/771497/000077149726000007/abm-20260430.htm) — **$871.8M of interest-rate swaps at 1.72%–3.81% "mostly maturing June 28, 2026"**, 5.66% weighted-average rate ex-swaps, total debt $1,863.4M, $518.9M revolver capacity, buyback 2.13M shares for $94.1M with **$89.0M remaining**, 59.9M H1 diluted shares vs 63.1M, goodwill $2,738.4M with no impairment, $8.3M accrued litigation (range 0–$15.1M), ELEVATE charges $6.8M H1 / $20.1M cumulative, tax rate 27.9% Q2, **no customer-concentration disclosure**.
12. [ABM CORRESP to SEC Division of Corporation Finance, 2025-05-01 (SEC)](https://www.sec.gov/Archives/edgar/data/771497/000077149725000011/filename1.htm) — the SEC comment concerned the "Prior year self-insurance adjustment" in the 2024-12-18 8-K non-GAAP reconciliation; ABM, over CFO Earl R. Ellis's signature, agreed to change its presentation.
13. ABM Form 4 filings (SEC XML): [Valentin 2026-07-17](https://www.sec.gov/Archives/edgar/data/771497/000122520826006655/doc4.xml) · [**Chin 2026-07-15**](https://www.sec.gov/Archives/edgar/data/771497/000122520826006611/doc4.xml) · [Orr 2026-07-06](https://www.sec.gov/Archives/edgar/data/771497/000122520826006482/doc4.xml) · [Salmirs 2026-06-12](https://www.sec.gov/Archives/edgar/data/771497/000122520826005990/doc4.xml) · [Jacobsen 2026-02-10](https://www.sec.gov/Archives/edgar/data/771497/000122520826001587/doc4.xml) — transaction codes, share counts, prices, holdings after, and the 10b5-1 footnotes (present on all but Chin's).
14. [ABM Names David Orr as Chief Financial Officer — GlobeNewswire / ABM IR, 2025-06-10](https://www.globenewswire.com/news-release/2025/06/10/3096631/799/en/ABM-Names-David-Orr-as-Chief-Financial-Officer.html) — CFO transition effective 6 June 2025, Ellis as senior advisor to no later than 5 September 2025 with severance for termination without cause.
15. [ABM Q2 FY2026 earnings call transcript — The Motley Fool, 2026-06-08](https://www.fool.com/earnings/call-transcripts/2026/06/08/abm-abm-q2-2026-earnings-call-transcript/) — the H2 margin-ramp quotes, ATS mix ("designing and engineering" vs "turning the wrenches"), **TfL exit ≈300bp of B&I back-half growth**, West Coast vacancy 2–3x NYC, record $1.2B H1 bookings, ~7% of revenue from semis + data centres, WGNSTAR scale, battery storage +52% in 2025, sub-3.0x leverage target and "$89 million remains" buyback, Education seasonality and the $85B K-12 funding gap, Aviation/TSA ~3M pax/day, wage-escalation commentary.
16. [ABM Reports Fourth Quarter and Full Fiscal 2025 Results — GlobeNewswire, 2025-12-17](https://www.globenewswire.com/news-release/2025/12/17/3206839/799/en/ABM-Reports-Fourth-Quarter-and-Full-Fiscal-2025-Results-and-Provides-Fiscal-2026-Outlook.html) — the verbatim non-GAAP definitional-change language and its retroactive application.
17. [ABM analyst forecast — MarketBeat](https://www.marketbeat.com/stocks/NYSE/ABM/forecast/) — 5-analyst Hold consensus, $47.00 PT unchanged at 1m/3m and down from $56.00 a year ago, and the dated list of analyst actions (Weiss 8/11/26, Baird 6/8/26, UBS and Truist 3/11/26, Maxim 3/11/26).
18. [ABM short interest — MarketBeat](https://www.marketbeat.com/stocks/NYSE/ABM/short-interest/) — **2026-08-14 settlement: 1,884,396 shares, 3.25% of float, 5.6 days to cover, −3.03% vs prior**, and the ~3.0M / 5.2% May 2026 peak.
19. [ABM quote — Finviz](https://finviz.com/quote?t=ABM) — EPS next quarter $1.01, next-year EPS $4.35, short float 3.27% / short ratio 3.54 / 1.88M shares, institutional 102.47%, insider 1.59%, insider transactions −5.63%, beta 0.64, RSI 49.2, SMA20/50/200 relatives, 52-week range, "Sep 08 BMO".
20. [ABM earnings history — TipRanks](https://www.tipranks.com/stocks/abm/earnings) — the eight-quarter actual-vs-consensus surprise history used to establish the Q4 FY25 $0.88-vs-$1.09 and Q1 FY26 $0.83-vs-$0.87 gaps, and the $1.01 Q3 FY26 forecast. (Note: the fetched table's two columns are actual-then-consensus, which I verified against primary 8-K figures before use.)
21. [ABM forecast — stockanalysis.com](https://stockanalysis.com/stocks/abm/forecast/) — 8 analysts, "Buy", average PT $52.43 (low $45 / high $68), FY26 revenue $9.23B and **FY26 EPS $3.98**, FY26 EPS growth +15.62%.
22. [ABM (ABM) Reports Earnings Tomorrow: What To Expect — StockStory via FinancialContent, 2026-09-07](https://markets.financialcontent.com/stocks/article/stockstory-2026-9-7-abm-abm-reports-earnings-tomorrow-what-to-expect) — Q3 revenue consensus ≈$2.332B, ~4% expected YoY growth, "analysts generally reconfirmed estimates over the last 30 days", and the "market still unconvinced the ERP rollout is behind it" framing. `snippet_only`.
23. [ABM Industries: ERP scars meet a critical print — Ortex, 2026-09-05](https://ortex.news/articles/158535/abm-industries-erp-scars-meet-a-critical-print) — short interest 3.2% of free float and −25% m/m, **borrow cost recently below 0.35%**, put/call 0.14 vs 20-day average, ELEVATE/ERP history, CEO's $2.3M June sale under a pre-arranged plan and the absence of open-market insider purchases.
24. [Do Options Traders Know Something About ABM Industries Stock We Don't? — Zacks via Yahoo Finance, 2026-07-23](https://finance.yahoo.com/markets/options/articles/options-traders-know-something-abm-123000441.html) — **Zacks Rank #3 (Hold)**, industry in the bottom 19%, and the 60-day revision: three analysts up, none down, consensus **$0.98 → $1.01**.
25. [Options Volatility and Implied Earnings Moves Today, September 03, 2026 — TipRanks](https://www.tipranks.com/news/options-volatility-and-implied-earnings-moves-today-september-03-2026) — checked and **does not list ABM**; establishes that no published implied move was available from this source.
26. [ABM Q2 FY2026 earnings call coverage — Investing.com](https://www.investing.com/news/transcripts/earnings-call-transcript-abm-industries-q2-2026-reports-record-revenue-stock-rises-93CH-4728726) — FY26 FCF ~$250M before transformation/integration costs, ~$65M of excluded items including ~$20M remaining transformation cost. `snippet_only`.
27. [ABM Expands Position in Data Center Industry with Acquisition of Quality Uptime Services — GlobeNewswire, 2024-06-24](https://www.globenewswire.com/news-release/2024/06/24/2902940/799/en/ABM-Expands-Position-and-Capabilities-in-Fast-Growing-Data-Center-Industry-with-Acquisition-of-Quality-Uptime-Services.html) — the data-centre/mission-critical acquisition history behind the ATS growth story.
28. [Stocktwits ABM stream API](https://api.stocktwits.com/api/2/streams/symbol/ABM.json?limit=30) — 686 watchers; 30 most recent messages spanning 2026-02-20 to 2026-08-05; three sentiment-tagged (all Bullish); zero posts in the last month.
29. Google Trends explore endpoint — returned **HTTP 429 (Too Many Requests)**; no search-interest series obtained.
30. [Is the stock market open on Labor Day? 2026 holiday trading schedule — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/is-the-stock-market-open-on-labor-day-heres-the-holiday-trading-schedule-for-2026-210239142.html) and [NYSE Group 2026–2028 holiday calendar](https://s2.q4cdn.com/154085107/files/doc_news/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar-2025.pdf) — NYSE and Nasdaq closed Monday 2026-09-07, reopening 09:30 ET Tuesday 2026-09-08.
31. [Office occupancy trends and insights — Propmodo](https://propmodo.com/office-occupancy-trends-and-insights/) and [US Real Estate Market Outlook 2026: Office — CBRE](https://www.cbre.com/insights/books/us-real-estate-market-outlook-2026/office) — Kastle-derived weekly office occupancy 56.3% (highest since early 2020), Q1 2026 net absorption 6.9M sq ft, eighth consecutive quarter of positive demand. `snippet_only`.
32. [ABM FY2025 Annual Report (SEC Form ARS)](https://www.sec.gov/Archives/edgar/data/771497/000119312526050329/fy2025_ars.pdf) — self-insurance methodology and the FY2024 $20.3M increase in prior-period-accident-year claims. `snippet_only`.
33. [ABM 8-K, Item 5.02, filed 2025-10-30 (SEC)](https://www.sec.gov/Archives/edgar/data/771497/000119312525257546/abm-20251030.htm) — election of Barry A. Hytinen as director on 2025-10-29, board expanded from eleven to twelve.
34. [ABM Industries 3Q 2026: Revenue $2.29B, EPS $0.73 — 10-Q Summary, TradingView](https://www.tradingview.com/news/tradingview:0aaf6ebee21fa:0-abm-industries-3q-2026-revenue-2-29b-eps-0-73-10-q-summary/) — cited only to flag it as **mislabelled**: those are Q2 FY26 figures.
35. [Stock Market Today (Sept. 4, 2026): Yields jump, stocks fall after jobs report surprises to upside — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-sept-04-2026) — the 4 September market reaction, short-end yield move, and small-cap cost-of-capital framing. `snippet_only`.
36. [Jobs report August 2026 — CNBC, 2026-09-04](https://www.cnbc.com/2026/09/04/jobs-report-august-2026.html) and [Hot Jobs Report Hurts Stocks, Lifts Rate Hike Odds — Charles Schwab](https://www.schwab.com/learn/story/stock-market-update-open) — +162k payrolls vs ~53–55k consensus, unemployment 4.1%, average hourly earnings +0.3% m/m and +3.1% y/y, CME FedWatch ~58% odds of a 25bp **hike** at the 15–16 September FOMC. `snippet_only`.
37. [Aramark Q3 FY2026 8-K exhibit 99.1 (SEC), 2026-08-11](https://www.sec.gov/Archives/edgar/data/0001584509/000158450926000118/ex991armkq3fy2026.htm) and [Aramark jumps after Q3 earnings beat and higher 2026 revenue outlook — QuiverQuant](https://www.quiverquant.com/news/Aramark+jumps+after+Q3+earnings+beat+and+higher+2026+revenue+outlook) — adj. EPS $0.52 vs $0.48, revenue $5.1B +9% vs $4.92B est., FY26 organic growth raised to 9–10%, data-centre hospitality ramp; day-of move +6% to +8.9% is `snippet_only`.
38. [Cintas Corporation Announces Fiscal 2026 Fourth Quarter and Full Year Results, 2026-07-15](https://www.cintas.com/about/newsroom/details/news/2026/07/15/cintas-corporation-announces-fiscal-2026-fourth-quarter-and-full-year-results/) — FQ4 revenue $2.91B +8.9%, organic +8.4%, adj. EPS $1.29 +18.3%, 51.0% record gross margin, FY27 adj. EPS guide $5.36–$5.50.
39. [Healthcare Services Group Q1 FY2026 8-K exhibit (SEC)](https://www.sec.gov/Archives/edgar/data/0000731012/000073101226000025/ex99-2026xq1xpressrelease.htm) — revenue $462.8M +3.4%, Environmental Services $208.3M at 12.1% margin, mid-single-digit growth reiterated.
40. [Implied Earnings Moves Chart — SpotGamma](https://spotgamma.com/free-tools/implied-earnings-moves/) — methodology reference ("at-the-money straddle for the first expiration date after a stock's scheduled earnings date"); the tool renders client-side and returned no ABM figure.

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such.*
