# SAIC — Science Applications International Corporation

**What this print is about.** SAIC reports Q2 FY2027 (quarter ended ~31 July 2026) before the open on Monday 31 August 2026 [1][2]. This is not an EPS-beat question — SAIC has beaten consensus EPS by 24–62% in each of its last four prints [3] and its guidance is structurally conservative. It is a *positioning* question. The stock closed at $128.96 on 27 Aug, 96.8% of the way up its 52-week range and +56.8% off its 11 Feb 2026 low of $82.22, a low created when management pre-announced a $350M cut to FY27 revenue guidance and the stock fell 16.0% in a day [4][5]. Since then the market has re-rated SAIC from a broken-growth story to a margin-and-buyback compounder: FY27 adj-EPS guidance has been walked from $9.50–$9.70 (Mar) to $9.90–$10.10 (Jun) [6][7], EBITDA margin guidance from 9.9–10.1% to 10.1–10.3%, and the company is retiring ~7.8% of its market cap a year in stock [8]. The sell-side has not kept up — the average price target ($116.89–$121.50 across three aggregators) sits *below* spot, with 8 Holds and 1 Sell against 2 Buys [9][10][11]. So the bar is no longer "beat"; the bar is "beat, raise again, and show the organic-revenue trough is real before the RITS contract rolls off in Q3 and takes $200M out of H2" [12]. Options price a ~8.9–9.2% event move [13], consistent with a 6-print realised mean absolute move of 9.2% [own calc, 14].

---

## 1. Event & anchors

| Item | Value | As-of | Source |
| --- | --- | --- | --- |
| `event_confirmed` | **true** | — | Company press release 13 Aug 2026 [1][2] |
| Event date | **2026-08-31 (Monday)** | — | [1][2] |
| Session | **bmo** — "before market open on Monday, August 31, 2026" | — | [1][2] |
| Call time | 10:00 a.m. EDT, webcast-only (no dial-in) | — | [1][2] |
| Fiscal period | Q2 FY2027, quarter ended ~31 Jul 2026 (FY ends 29 Jan 2027) | — | [1][15] |
| Date changed / pre-announced? | No change. No pre-announcement this cycle. Last 8-K was 19 Aug (MARPA amendment) [16]; last 2.02 8-K was 1 Jun [7] | 28 Aug 2026 | EDGAR submissions index [17] |
| Spot | **$128.96** (close); $129.30 after-hours 19:53 ET | 2026-08-27T20:00Z | [8][18] |
| Prior close / day change | $127.58 / +1.08% | 2026-08-27 | [18] |
| Market cap | **$5.45B** (42.28M sh × $128.96) | 2026-08-27 | [8] |
| 52-week range | $81.08 – $130.53 (spot = 96.8% of range) | 2026-08-27 | [18], own calc |
| Front expiry | **2026-09-18** (22 dte) — no weeklies listed | 2026-08-27 close | Cboe delayed quotes [13] |
| ATM straddle (K=130) | $11.80 = **9.15% of spot** | 2026-08-27 close | [13], own calc |
| **Event-implied move (1σ)** | **~8.9%** (two-expiry event-vol decomposition) | 2026-08-27 close | [13], own calc — method below |
| ATM IV, front (18 Sep) | 46.4% | 2026-08-27 close | [13] |
| ATM IV, 2nd (16 Oct) | 37.8% | 2026-08-27 close | [13] |
| ATM IV, 3rd (20 Nov) | 37.4% | 2026-08-27 close | [13] |
| IV30 | 41.88% (−0.20% d/d) | 2026-08-27 close | [13] |
| Implied base (non-event) vol | 29.2% | derived | own calc |
| Realised vol 20d / 60d / 120d | 21.5% / 32.9% / 33.9% | to 2026-08-27 | own calc from [19] |
| IV rank / percentile | **unavailable** — no historical IV series sourced | — | — |
| Beta (5Y) | 0.29 | 2026-08-28 | [8] |

**Implied-move method (mine, transparent).** SAIC lists no weekly options, so the nearest expiry after the print is 18 Sep — 22 days out. The raw ATM straddle (9.15%) therefore overstates the one-day event move. Both the 18 Sep and 16 Oct expiries contain the event, so I solved the two-equation system `σ_front²·T₁ = σ_base²·T₁ + E²` and `σ_2nd²·T₂ = σ_base²·T₂ + E²` using ATM IVs of 46.4% (T₁=22d) and 37.8% (T₂=50d). That gives base vol 29.2% and an event jump **E = 8.87%**. I report the implied move as **8.9%**, with a defensible range of 8.9–9.2%. No third-party published implied move for SAIC was findable; MarketChameleon and Barchart were access-denied.

### Historical realised one-day earnings moves

All SAIC releases are BMO, so the reaction day equals the 8-K Item 2.02 filing date. Dates confirmed from EDGAR [17]; moves computed from daily closes [19].

| Report date | Quarter | 1-day move |
| --- | --- | --- |
| 2026-06-01 | Q1 FY27 | **+10.44%** |
| 2026-03-16 | Q4 FY26 | **+1.24%** |
| 2025-12-04 | Q3 FY26 | **+16.29%** |
| 2025-09-04 | Q2 FY26 | **−6.91%** |
| 2025-06-02 | Q1 FY26 | **−13.26%** |
| 2025-03-17 | Q4 FY25 | **+7.15%** |
| 2024-12-05 | Q3 FY25 | −2.53% |
| 2024-09-05 | Q2 FY25 | +4.70% |
| 2024-06-03 | Q1 FY25 | −11.77% |
| 2024-03-18 | Q4 FY24 | −9.98% |
| 2023-12-04 | Q3 FY24 | +13.41% |
| 2023-09-07 | Q2 FY24 | −4.86% |

- **Last 6:** mean |move| **9.21%**, median **8.79%**, max **16.29%**, pattern **U, U, U, D, D, U** (4 up / 2 down).
- **Last 8:** mean |move| 7.81%, median 7.03%.
- **Last 12:** mean |move| 8.54%, median 8.57%, 6 up / 6 down.
- **Non-quarterly event, worth flagging:** 2026-02-11, a standalone Item 2.02/7.01 8-K with preliminary FY26 results plus a cut to FY27 revenue guidance, produced a **−16.03%** day [4][5][19]. SAIC has demonstrated willingness to reset guidance off-cycle.

**Own inference:** the ~8.9% implied is *fairly* priced against a 9.2% six-quarter realised mean — this is not an obviously cheap or obviously rich straddle. There is no volatility edge here; the edge, if any, has to be directional.

### Run-up / de-risking into the print

| Window to 2026-08-27 | Change |
| --- | --- |
| 1 day | +1.08% |
| 5 days | +2.11% |
| 21 days | **+10.21%** |
| 63 days (~3m) | **+24.36%** |
| 126 days (~6m) | **+40.63%** |
| Since 2026-02-11 close ($82.22) | **+56.80%** |
| 252 days (1y) | +7.84% |

All computed from [19]. Average daily volume 20d 394,942 vs 90d 509,483 — volume is *below* trend into the print, i.e. no visible institutional repositioning in the tape. The stock made its 52-week intraday high ($130.53) on the last session before the report.

---

## 2. The bar

**Consensus — sources disagree; I report the spread rather than pick one.**

| Metric | Value | Source |
| --- | --- | --- |
| Q2 FY27 EPS consensus | **$2.15** | MarketBeat [10] |
| Q2 FY27 EPS consensus | **$2.25** (4 analysts) | Nasdaq, via stage-0 universe file [20] |
| Q2 FY27 EPS consensus | **$2.31** | Investing.com [3]; TradingKey [21] |
| Q2 FY27 revenue consensus | **$1.76B** | Investing.com [3] |
| Q2 FY27 revenue consensus | **$1.77B** | TradingKey [21] |
| Q2 FY27 revenue expectation | "revenue to decline 2.4% y/y" (≈$1.727B off a $1.769B base) | StockStory [22] |
| FY27 EPS consensus (Zacks) | **$9.61** — *below* the low end of company guidance | Zacks via search snippet [23] `snippet_only` |
| Analyst count | 11 [9] / 12 [21] |
| Consensus rating | Hold — 2 Buy, 8 Hold, 1 Sell | TipRanks [11] |
| Average price target | **$121.50** [9] · $120.50 [11] · $116.89 [24] — **all below spot $128.96** |
| PT high / low | $137 (Stifel) / $95–$96 (BNP Exane, Goldman) | [9][11] |

**Prior-year comparable (the actual base):** Q2 FY26 (ended 1 Aug 2025) revenue **$1.769B** (−3% organic), operating income $139M (7.9%), adj EBITDA **$185M (10.5%)**, GAAP diluted EPS $2.71, **adjusted diluted EPS $3.63**, FCF $150M, net bookings $2.6B, book-to-bill 1.5 (TTM 1.0), backlog $23.2B ($3.6B funded), buybacks $106M [25].

**Company guidance in force (raised 1 Jun 2026)** [7]:

| FY27 metric | Current guide | Prior guide (16 Mar) |
| --- | --- | --- |
| Revenue | $7.0–$7.2B | $7.0–$7.2B |
| Organic growth | (4)% – (2)% | (4)% – (2)% |
| Adj EBITDA | $720–$730M | $705–$715M |
| Adj EBITDA margin | 10.1% – 10.3% | 9.9% – 10.1% |
| **Adj diluted EPS** | **$9.90 – $10.10** | $9.50 – $9.70 |
| Free cash flow | >$600M | >$600M |

**FY26 actuals for reference:** revenue $7.26B (−3%), adj EBITDA $708M (9.7%), GAAP EPS $7.70, **adj EPS $10.75**, FCF $577M, buybacks $422M / ~4.0M shares, backlog $22.6B [6].

**Estimate revisions.** I could not source a clean 30/60/90-day revision table — Zacks' detailed-estimates page is bot-blocked and Nasdaq's estimate module returned "data not available". Two qualitative, conflicting reads: StockStory says "the majority of analysts covering the company have reconfirmed their estimates over the last 30 days" [22]; a Zacks snippet says estimates "have been broadly trending downward" over the past month [23] — but the same snippet quotes a FY27 consensus of $9.61, *below* company guidance of $9.90–$10.10, which suggests that figure is stale rather than a fresh cut. Investing.com reports three upward EPS revisions for the upcoming period [26] `snippet_only`. **Treat revisions as an unresolved gap.**

**Whisper number:** unavailable. No credibly published SAIC whisper found.

**What SAIC has to deliver just to hold the stock flat (my inference, not sourced):** given a +24% three-month run and an average PT below spot, an in-line-to-modest beat with FY27 guidance merely reaffirmed is, in my view, a fade. Flat probably requires (a) adj EPS materially above ~$2.31, (b) FY27 adj EPS guidance raised again toward ~$10.30–$10.50, and (c) a Q2 book-to-bill ≥1.0 with commentary that the H2 organic trough is the trough.

---

## 3. The one metric that matters

**Not EPS. It is the FY2027 revenue/organic-growth commentary around the RITS roll-off, paired with whether the FY27 adjusted-EPS guide gets raised a second time.**

Why: on the Q1 call, CEO Jim Reagan said "RITS will likely now roll off in Q3," creating a **$200 million headwind** across H2, with management modelling **~(3)% organic contraction in each of Q3 and Q4** and expecting to finish "at or slightly above the midpoint" of sales guidance [12]. Q2 is therefore the *last clean quarter* — the revenue comp is against a weak $1.769B prior-year quarter [25], and consensus of $1.73–$1.77B [3][21][22] implies roughly flat to −2.4% y/y. The market has already paid for the margin story: EBITDA margin guidance is up 60bp since February and Civilian hit a record 15% segment margin, which CFO Prabu Natarajan said should "operate consistently at 15% or so" [12]. What is *not* yet in the price is evidence that revenue stops shrinking. So the trade keys off: (i) does management hold or improve the (4)%–(2)% organic band; (ii) Q2 net bookings / book-to-bill and TTM book-to-bill (Q4 FY26 was a very weak 0.3, Q1 FY27 recovered to 1.1, TTM 1.0) [6][7]; (iii) any first framing of FY28.

**Secondary tell:** management said recompete win rates are "stabilizing and expected to return to the 90% range" and new-business win rates are "well above 30%" [12]. SAIC has already banked >$1.6B of Intel/Space awards in H1 FY27 including a $400M intelligence recompete announced 5 Aug [27] — the day after which the stock rose +3.31% [19]. A strong bookings headline is the most likely positive catalyst.

**How I know what's expected:** consensus revenue $1.76–$1.77B [3][21] vs the $1.769B prior-year base, and the company's own guided H2 shape [12]. There is no published buy-side bookings expectation I could source.

---

## 4. Fundamentals — what changed, what is at stake

**Segments (Q1 FY27, 10-Q)** [15]:
- Defense and Intelligence: revenue $1,466M (+2% y/y), adj operating income $146M (+27%), margin **10.0%** vs 8.0%.
- Civilian: revenue $440M (−1% y/y), adj operating income $68M (+31%), margin **15.5%** vs 11.7%.
- Consolidated: $1,906M (+2%; +0.5% organic ex-SilverEdge), net income $115M (+69%).

**Margin trajectory.** Q1 FY27 adj EBITDA $222M / **11.65%** — a record — but management explicitly warned Q1's "mid-to-upper 10%" adjusted operating margins exceed the full-year implied "mid-to-upper 9%", and that Q1 benefited from a **$12M venture-investment IPO gain worth ~60bp** [12]. That is the single most important quality caveat on the Q1 print, and it means Q2 margin should mechanically be lower than Q1. FY26 full year was 9.7% adj EBITDA margin [6]; FY27 guided 10.1–10.3% [7].

**Portfolio reshaping.** Since February SAIC has been deliberately exiting commoditised Enterprise IT — the segment shrinks from 17% to ~10% of revenue by FY27 following losses on the Army RITS and Air Force Cloud One recompetes, which drove the $350M FY27 revenue cut [4]. The qualified pipeline is down ~25% y/y, "the vast majority" of that in enterprise IT [12]. Management launched "Project Orbit," an enterprise transformation programme built from ~3,500 employee ideas, to free up investment capacity [12]. Business groups were consolidated from five to three effective 31 Jan 2026 [28].

**Cash and capital returns — the real EPS engine.**
- TTM FCF $603M [8]; FY26 FCF $577M [6]; FY27 guide >$600M [7]. Q1 FY27 FCF was only $118M — heavily H2-weighted [7].
- Buybacks: $422M / ~4.0M shares in FY26 [6]; $175M / 1.9M shares in Q1 FY27 alone; ~$1.2B remaining under the Dec-2024 authorisation; management targets ~$400M for FY27 and called repurchases "opportunistic" given the price dislocation [7][12][15].
- **Buyback yield 7.84%**, dividend yield 1.15% [8]. Shares outstanding 42.28M and falling [8][15]. On a $5.45B cap, retiring ~$400M/yr of stock is ~7% of shares — this is why EPS can grow while revenue shrinks.

**Balance sheet.** Total debt $2.68B, cash $109M, net debt ~$2.57B, EV $8.02B, EV/EBITDA 10.9x [8]. Principal $2.5B: TLA $1.1B (2030), TLB3 $500M (2031), 2028 notes $400M, 2033 notes $500M; $1.0B revolver undrawn [15]. On 14 Aug 2026 SAIC upsized its MUFG Master Accounts Receivable Purchase Agreement from $300M to **$400M** [16] — more liquidity headroom, but it is also a receivables-sale facility, so watch whether reported FCF is flattered by drawing on it (Q1 had $814M sold, $116M outstanding sold receivables) [15].

**Valuation.** PE 14.5x TTM, forward PE **13.34x**, EV/EBITDA 10.88x [8]. Cheap versus CACI or Leidos, but SAIC is the only one of the three guiding to negative organic growth.

**Customer concentration.** ~all revenue is US federal; the practical concentration risk is programme-level (RITS, Cloud One) rather than customer-level. Backlog $22.9B total / $3.7B funded at Q1 FY27 [7]. Funded backlog covers roughly half a year of revenue — normal for the sector, but it means appropriations timing moves quarters.

---

## 5. Positioning & options

**Term structure (2026-08-27 close, Cboe delayed quotes)** [13]:

| Expiry | DTE | ATM straddle (K=130) | % of spot | ATM IV | Put OI | Call OI | P/C OI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-09-18 | 22 | $11.80 | 9.15% | **46.4%** | **3,469** | 146 | **23.8** |
| 2026-10-16 | 50 | $14.50 | 11.24% | 37.8% | 0 | 9 | 0.00 |
| 2026-11-20 | 85 | $18.60 | 14.42% | 37.4% | 14 | 101 | 0.14 |
| 2026-12-18 | 113 | $22.25 | 17.25% | 38.8% | 120 | 213 | 0.56 |
| 2027-02-19 | 176 | $26.05 | 20.20% | 36.7% | 5 | 61 | 0.08 |

- **Steeply inverted front end**: 46.4% front vs 37.4–37.8% for the next two expiries. Classic event pricing; ~8.6 vol points of event premium.
- IV30 41.88% versus realised 20d 21.5% — the options market is paying a large premium to very quiet recent tape.
- **Skew is essentially flat to slightly call-favoured** at the wings for the front expiry: 25-delta-ish put (K=120, Δ−0.26) IV 48.2% vs 25-delta-ish call (K=140, Δ+0.26) IV 45.4% — only ~2.8 vol of put skew; and at ~35 delta the call (K=135, 47.6%) is actually *above* the put (K=125, 46.0%) [13]. For a stock at 52-week highs with a 9% implied move, that is not a fearful chain.
- **But open interest is overwhelmingly puts in the event expiry**: 3,469 puts vs 146 calls, concentrated at **Sep $120 (2,056 OI)** and **Sep $115 (1,328 OI)** — both well below spot. Total chain P/C OI 6.81. My inference: this looks like pre-existing downside protection or a financed hedge on a long position rather than fresh directional bearishness (the strikes are ~7–11% OTM, i.e. right at the implied move). Absolute size is small — 3,469 contracts ≈ 347k shares ≈ 0.8% of shares out — so do not over-read it.
- **Traded volume is negligible** across the chain (single- and low-double-digit contracts per strike on 27 Aug) [13]. SAIC options are illiquid; there is no meaningful "unusual options activity" signal to extract, positive or negative.

**Short interest.** 2.71M shares short, **up from 2.37M the prior period (+14.3%)**, = 6.42% of shares outstanding, 6.49% of float, **6.61 days to cover** [8]. A second aggregator reports 3.0M shares / 7.0% of float, +6.7% period-on-period and **+51.7% since July 2025** [29] `snippet_only`. The settlement date is not stated on either source; the most recent Nasdaq mid-month settlement was 2026-08-14 [30]. Either way: short interest is elevated for a low-beta defence-IT name and has been *rising into a 52-week high*.

**Borrow fee / shares available to borrow:** **unavailable** — Fintel returned HTTP 403.

**Crowding read (mine).** The trade looks moderately crowded long on momentum and moderately hedged with puts, with a rising short base leaning against it. Institutional ownership 76% [24]. The tell I weight most is that the sell-side average target sits ~6% *below* spot with 8 Holds and 1 Sell [9][11] — the marginal upgrade buyer is thin, and price targets are being raised reactively after the fact (Jefferies $115→$130 on 19 Aug, five sessions before the print, and still Hold [24][31]).

---

## 6. Sentiment & alt-data

- **Retail/social:** Stocktwits sentiment **62% bullish** on 1,356 messages, as of 2026-08-28 [32]. I could not source a 7/14/30-day sentiment trend series — the gauge is a point-in-time reading only. Treat as weak supporting colour.
- **Analyst rating changes and PT drift (dated):**
  - 2026-08-19 — Jefferies (Sheila Kahyaoglu): PT $115 → **$130**, keeps **Hold**, explicitly ahead of the 31 Aug print [24][31].
  - 2026-07-07 — TD Cowen (Gautam Khanna): PT $130 → **$125**, **Hold** [24]. (TipRanks shows a separate TD Cowen raise to $130 from $115 [11]; the two aggregators disagree on the sequence — flagged.)
  - 2026-06-03 — UBS: $113 → **$119**, **Neutral** [24].
  - 2026-06-02 — Citigroup (John Godyn): $120 → **$132**, **Buy** [24][11].
  - 2026-06-02 — JPMorgan: $110 → **$125**, **Neutral** [24].
  - 2026-06-09 — Goldman Sachs (Noah Poponak): $85 → **$96**, **Sell** [33].
  - 2026-05-27 — BNP Paribas Exane: initiation, **$95**, Neutral [24].
  - Stifel (Jonathan Siegmann): **$137 Buy** — the Street high; raised from $120 [11][34].
  - **Pattern:** targets are drifting up steadily but ratings are not. Every raise since June has been a Hold/Neutral except Citi and Stifel. Nine of eleven targets are at or below $132 while the stock is $128.96.
- **Alt-data proxies:** **none sourced.** SAIC is a pure business-to-government services firm — app ranks, web traffic and consumer reviews have no read-through, and I could not source a SAIC-specific job-postings or Google-Trends time series. Broad federal-contractor labour-market data exists but is not company-specific [35]. Recorded as a coverage gap.
- **News flow into the print:** $400M intelligence-agency recompete win announced 5 Aug (stock +3.31% on 6 Aug) [27][19]; $118.4M VA award 6 Aug [27]; two new directors (David Benson, David Cush) effective 20 Aug [36][37]. Nothing negative in the last three weeks that I could find.

---

## 7. Forensics

- **Insider transactions — the cleanest finding in this dossier.** I pulled and parsed every Form 4 SAIC has filed since 1 Sep 2025 — **41 filings** — directly from EDGAR. **There is not a single open-market sale (code S) or purchase (code P) in any of them.** Every non-derivative transaction is code A (grant), F (shares withheld for tax), M (option exercise) or G (gift) [17, own parse]. Representative recent filings: Vincent DiFronzo (EVP Air Force & Space, Intel) — 2,682 shares gifted 2 Jul 2026 [38]; Kathleen McCarthy (EVP, CHRO) — 1,233 shares withheld at $114.35 on 6 Jun [39]; Steven Shane (director) — option exercise 2,876 @ $77.65 plus 1,941 withheld at $115.08 on 2 Jun [40]; David Urban (director) — 1,886-share grant 3 Jun [41]. **No 10b5-1 plan is referenced in any of them, because there are no discretionary dispositions to explain.** My read: insiders have not sold a share into a 57% rally to 52-week highs. That is a mildly constructive absence-of-signal, and it is inconsistent with the one search headline I saw claiming "SAIC insider buying" [42] — I found no purchases either, so treat that headline as unreliable.
- **Executive and director changes.** Toni Townes-Whitley separated as CEO "without cause" announced after the close on 23 Oct 2025; Jim Reagan (board member since Jan 2023, ex-Leidos CFO) was named interim CEO [43][44], then permanent CEO on 17 Feb 2026 [45][46] — six days after the −16% guidance-cut day. This print is Reagan's second as permanent CEO. Board expanded from ten to twelve on 20 Aug 2026 with Benson and Cush, both to the Audit Committee [36][37]; corresponding Form 3s filed 20 Aug [17]. Additional Item 5.02 8-Ks were filed 9 Apr 2026 (plus an amendment) and 1 Jun 2026 [17] — I did not retrieve their contents (gap).
- **Auditor / restatement.** Ernst & Young LLP, ratified at the 3 Jun 2026 annual meeting (35,670,199 for / 306,713 against). FY26 audit fees $5,003,000 vs FY25 $5,005,000 — flat; total fees $5,299,888 vs $5,253,202 [47]. **No restatement and no material weakness found.** Fee stability and a clean ratification are the opposite of a red flag.
- **Legal.** SAIC received federal grand jury subpoenas in **April 2022 and October 2023** in connection with a criminal investigation by the DOJ Antitrust Division; the company is cooperating and states it cannot estimate any fines or penalties [15][48]. This is long-standing, unchanged boilerplate — background risk, not a fresh catalyst, but it is a live tail.
- **8-K cadence.** Normal and low. Since April 2026: 29 May (8.01), 1 Jun (2.02 earnings + 5.02), 8 Jun (5.07 vote results), 10 Aug (5.02 directors), 19 Aug (1.01/2.03 MARPA upsize) [17]. **No 7.01/8.01 pre-announcement 8-K in the run-up to this print** — which matters, because SAIC *did* use exactly that mechanism on 11 Feb 2026 to warn [4]. Its absence this time is a modest negative-surprise-risk reducer.
- **Filing-language / tone shift.** Q1 FY27 10-Q notes the DHS funding disruption (Feb–Apr 2026) resolved with full-year funding through 30 Sep 2026, and cites the July 2025 "One Big Beautiful Bill Act" restoring immediate R&D expensing (a cash-tax tailwind) [15]. Effective tax rate 20.9% vs 20.6% prior year [15]. Nothing I would call a tone shift.

---

## 8. Macro & peer read-through

**Regime.** Government-services is currently a two-tier market: national-security demand accelerating, civil agencies at a funding trough. SAIC's own CFO said civil funding is "at a trough" and unlikely to "materially deteriorate from here," while management expects "another large appropriation for FY 2027" with FY26 money now "starting to flow… albeit unevenly" [12].

**Budget/shutdown.** FY2027 begins 1 October 2026. The Senate passed a continuing resolution (H.R. 6500) 90–6 on 8 Aug funding the government at FY2026 levels through 11 December 2026; House passage was still pending as of late August [49][50] `snippet_only`. A CR is the base case; a shutdown is a live but secondary tail. Relevant to SAIC because the 2025 shutdown was named by management as one cause of the FY26 revenue shortfall [4]. Expect this to be an analyst-question topic on the call, not a headline number.

**Rates / FX / commodities.** Minimal direct exposure — no material FX or commodity sensitivity; ~$2.5B of debt with roughly $1.6B floating (TLA + TLB3) makes SAIC modestly rate-sensitive on interest expense [15], but this is second-order.

**Peers that already reported, with their reaction-day moves** (own calc from daily closes [19]; earnings dates from the cited coverage):

| Peer | Report date | 1-day move | What they said |
| --- | --- | --- | --- |
| **Leidos (LDOS)** | 2026-08-04 | **+10.01%** | Record Q2 revenue $4.6B (+7%), adj EBITDA margin 13.8%, defence book-to-bill 2.2x, **raised FY guidance** [51][52] |
| **Booz Allen (BAH)** | 2026-07-24 | **+10.11%** | Revenue **−4.2% to $2.8B**, adj EBITDA +7.4% with margin +130bp to 11.9%, adj EPS +22.3%, FCF $261M vs $96M, guidance reaffirmed; national security accelerating, civil challenged [53][54] |
| **CACI** | 2026-08-05 | −1.18% | FY26 revenue $9.6B (+10.9%), diluted EPS $24.16 (+8.2%); large PT raises followed [55] |
| **Parsons (PSN)** | 2026-08-05 | −1.67% | Q2 revenue $1.6B, book-to-bill 1.2x [51] |
| **ICF International** | 2026-08-04 | +2.50% | — |
| **KBR** | 2026-07-29 | −3.93% | — |
| **V2X** | 2026-08-05 | −1.04% | — |
| **L3Harris** | 2026-07-24 | +0.18% | — |

**The read-through that matters.** Booz Allen is the near-perfect analogue for SAIC's setup: revenue *declining* mid-single-digit, margins expanding, EPS up sharply, guidance reaffirmed — and the stock went **+10.1%**. Leidos, on a margin-and-raise print, went **+10.0%**. That is direct evidence that in this tape the market will pay up for margin-and-cash quality even with a shrinking top line. **The counter-evidence:** BAH was down 32% over the prior year and PSN down 39% [19] — both were *washed out* going in. SAIC is not washed out; it is +24% in three months and at the top of its range. CACI, which *was* extended (+21% 3m, +30% 1y) and beat, went **−1.2%** [19][55]. The peer cohort's message is therefore conditional: margin beats get paid when positioning is clean, and get sold when it is not.

---

## 9. Bull case / bear case / base case

**Bull.** SAIC beats big again and raises FY27 EPS guidance a second time, and the stock gaps toward $140. The evidence: four consecutive EPS beats of +24%, +32%, +42% and +62% [3]; guidance raised from $9.50–$9.70 to $9.90–$10.10 in one step in June [6][7]; a ~7.8% buyback yield mechanically compounding EPS on a 42.3M-share base with $1.2B of authorisation left [8][15]; Q2 laps a genuinely weak $1.769B prior-year quarter *before* the RITS roll-off hits in Q3 [12][25]; >$1.6B of Intel/Space awards already banked in H1 FY27 including the $400M recompete announced 5 Aug [27], which sets up a strong bookings headline; Civilian margins at a record 15% that the CFO says are structural [12]; short interest up 14% into the print with 6.6 days to cover as squeeze fuel [8]; zero insider selling across 41 Form 4s [17, own parse]; and the direct BAH/LDOS precedent of +10% moves on exactly this template [51][53].

**Bear.** SAIC delivers a fine quarter and the stock sells off 6–10% because everything good is already in the price. The evidence: spot $128.96 sits at **96.8% of the 52-week range** after +56.8% off the February low and +24.4% in three months [19]; the consensus price target is **$116.89–$121.50, below spot**, with 8 Holds and 1 Sell against 2 Buys [9][11][24]; forward PE has re-rated from crisis levels to 13.3x for a company guiding organic revenue **down 2–4%** [7][8]; management itself flagged that Q1's record 11.65% margin included a **$12M one-off IPO gain worth 60bp** and that full-year margins run "mid-to-upper 9%" versus Q1's "mid-to-upper 10%" [12]; the qualified pipeline is down ~25% y/y [12] and Q4 FY26 book-to-bill was 0.3 [6]; the $200M RITS headwind lands in Q3–Q4 with ~(3)% organic contraction guided for both [12]; front-expiry put OI outnumbers call OI 24-to-1 at strikes right at the implied move [13]; and SAIC's own history is unkind here — in the four prints where it entered in the top quartile of its 52-week range, it went **1-for-4 with a −3.3% average move** (2024-03-18 −9.98%, 2024-06-03 −11.77%, 2023-09-07 −4.86%, 2023-12-04 +13.41%) [19, own calc].

**Base case (mine).** High probability of an EPS beat, moderate probability of a second FY27 guidance raise, and a genuinely two-sided price reaction because positioning has already discounted a good quarter. I expect Q2 adj EPS above the $2.15–$2.31 consensus band and revenue near $1.76–$1.80B, with FY27 EPS guidance nudged toward $10.10–$10.40 and the organic band held. On that outcome the stock probably trades up but by less than the ~8.9% implied — call it +2% to +5% — because the average sell-side target is below spot and the marginal upgrade is thin. The fat left tail is any softening of the organic-revenue band or a book-to-bill below 1.0, either of which, from 96.8% of the range with a 9% implied move, plausibly produces a −8% to −12% day. **Net: a slight lean up on fundamentals, almost entirely offset by positioning. Direction score +8, prob-up 54, reversal risk high.** I do not think this name carries real directional edge; the implied move is close to fair against a 9.2% six-quarter realised mean.

---

## 10. What would flip the consensus view

The most credible reversal is **management widening or lowering the FY27 organic-growth band, or guiding Q3 revenue below ~$1.70B, while explicitly framing the RITS/Cloud One roll-off as larger or earlier than the $200M/H2 they described in June** [12]. SAIC has done exactly this before — off-cycle, on 11 Feb 2026, with a $350M revenue cut that took the stock down 16.0% in a session [4][19]. Concretely: if the FY27 revenue guide moves from $7.0–$7.2B to anything with a $6-handle at the low end, or if Q2 net bookings come in below ~$1.5B (book-to-bill <0.9), the "margin compounder at 13x" thesis that has driven a 57% rally reverts to "shrinking asset with a good buyback," and the appropriate multiple is closer to the $95–$96 Goldman/BNP targets than to Stifel's $137 [9][11][33]. The mirror-image flip on the upside is a raise of FY27 adj EPS guidance to $10.40+ *combined* with an organic band improved to (2)%–0% — that would be the first credible evidence of a growth trough and would justify the sell-side chasing targets above $140.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **IV rank / IV percentile — null.** MarketChameleon (403 access-denied for automated clients) and AlphaQuery (503) unreachable; Cboe's delayed-quote endpoint gives only current IV30 (41.88%). | Without an IV history I cannot say whether a 9% implied is rich or cheap *relative to SAIC's own option history*. I substituted the 46.4% front vs 37.4% three-month term-structure inversion and IV30-vs-realised (41.9% vs 20d 21.5%) as partial proxies, but this is the largest single anchor missing. |
| **Estimate revision breadth (30/60/90-day) — unavailable.** Zacks detailed-estimates bot-blocked; Nasdaq estimate module returned "data not available". | Revision direction is one of the better short-horizon predictors of post-print drift. Two search snippets conflict outright (StockStory: reconfirmed; Zacks: trending down). Unresolved. |
| **Consensus EPS spread of $2.15 / $2.25 / $2.31** across three providers, and revenue $1.73B / $1.76B / $1.77B. | A 7% spread on the EPS bar makes "beat or miss" ambiguous at the margin. I could not obtain a single primary-source consensus with analyst count and standard deviation. |
| **Whisper number — unavailable.** | With four consecutive 24–62% beats, the buy-side bar is almost certainly far above published consensus, and I cannot quantify by how much. This is the reason my conviction is Low rather than Medium. |
| **Borrow fee and shares available to borrow — unavailable** (Fintel 403). | Determines whether the +14% rise in short interest reflects genuine bearish conviction or cheap, plentiful hedging. |
| **Short-interest settlement date not stated** on either source; two sources disagree (2.71M / 6.42% [8] vs 3.0M / 7.0% [29]). | Days-to-cover of 6.6 vs a competing 3.7 changes the squeeze read materially. |
| **Alt-data — none.** No SAIC-specific Google Trends, job-postings, or federal-award-run-rate time series sourced. | For a B2G services company the only genuinely predictive alt-data would be USASpending obligation run-rates; I could not retrieve a time series. |
| **Sentiment trend (7/14/30d) — unavailable.** Stocktwits gives a point-in-time 62% bullish only. | A level without a trend is close to useless. |
| **Contents of the 9 Apr 2026 and 1 Jun 2026 Item 5.02 8-Ks not retrieved.** | Could contain a CFO or segment-president change I have not accounted for. |
| **globenewswire.com and investors.saic.com returned HTTP 503**; benzinga.com, fintel.io, marketchameleon.com returned 403; zacks.com bot-blocked; wsj.com blocked by tooling. | Primary IR sourcing was routed through the Manila Times GlobeNewswire mirror and SEC EDGAR instead. EDGAR was fully reachable, so all filing-based facts are primary-sourced. |

---

## 12. Sources

1. https://www.globenewswire.com/news-release/2026/08/13/3344501/0/en/saic-schedules-second-quarter-fiscal-year-2027-earnings-conference-call-for-august-31-at-10-a-m-edt.html — earnings date/session/time announcement (page returned 503; used via search snippet + mirror [2]) `snippet_only`
2. https://www.manilatimes.net/2026/08/13/tmt-newswire/globenewswire/saic-schedules-second-quarter-fiscal-year-2027-earnings-conference-call-for-august-31-at-10-am-edt/2404898 — full GlobeNewswire text mirror: "before market open on Monday, August 31, 2026", 10:00 a.m. EDT, webcast-only
3. https://www.investing.com/equities/scnc-app-in-earnings — earnings surprise history (Q1 FY27 +41.67%, Q4 FY26 +32.32%, Q3 +24.04%, Q2 +62.05%, Q1 FY26 −11.11%); next-quarter EPS forecast $2.31, revenue $1.76B
4. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000008/saic8k02112026exhibit992.htm — 11 Feb 2026 8-K: preliminary FY26 results, FY27 revenue cut $7.35–7.55B → $7.00–7.20B, RITS/Cloud One losses, Enterprise IT 17%→10%
5. https://www.investing.com/news/stock-market-news/saic-stock-tumbles-after-lowering-revenue-guidance-for-fiscal-2027-93CH-4500851 — market reaction to the 11 Feb guidance cut
6. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000025/saic031620268kexhibit991.htm — Q4/FY26 results 8-K: FY26 revenue $7.26B, adj EBITDA $708M/9.7%, adj EPS $10.75, FCF $577M, buybacks $422M, backlog $22.6B; initial FY27 guide $9.50–$9.70
7. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000077/saic06012026ex991earningsr.htm — Q1 FY27 results 8-K: revenue $1.906B, adj EBITDA $222M/11.6%, GAAP EPS $2.61, adj EPS $3.23, FCF $118M, bookings $2.1B, B2B 1.1, backlog $22.9B/$3.7B funded, buybacks $175M; FY27 guide raised to $9.90–$10.10 and 10.1–10.3% margin
8. https://stockanalysis.com/stocks/saic/statistics/ — market cap $5.45B, EV $8.02B, 42.28M shares, short interest 2.71M (prior 2.37M), 6.42% of shares out, 6.49% float, 6.61 days to cover, beta 0.29, PE 14.5, fwd PE 13.34, EV/EBITDA 10.88, TTM revenue $7.29B, FCF $603M, debt $2.68B, cash $109M, buyback yield 7.84%
9. https://stockanalysis.com/stocks/saic/forecast/ — 11 analysts, Hold, average PT $121.50, high $137, low $93
10. https://www.marketbeat.com/stocks/NASDAQ/SAIC/earnings/ — Q2 FY27 consensus EPS $2.15; historical beat table
11. https://www.tipranks.com/stocks/saic/forecast — 2 Buy / 8 Hold / 1 Sell, average PT $120.50, high $137 (Stifel), low $95; recent analyst actions
12. https://www.fool.com/earnings/call-transcripts/2026/06/01/saic-q1-2027-earnings-call-transcript/ — Q1 FY27 call: RITS rolls off in Q3, $200M H2 headwind, ~(3)% organic in Q3 and Q4, "at or slightly above the midpoint" of sales guidance, $12M IPO gain = 60bp, Civilian ~15% margin structural, pipeline −25% y/y, recompete win rates returning to ~90%, ~$400M FY27 buyback target, Project Orbit, civil funding "at a trough"
13. https://cdn.cboe.com/api/global/delayed_quotes/options/SAIC.json — full delayed option chain, timestamp 2026-08-28 05:40:21 (27 Aug close): spot $128.96, IV30 41.879%, all expiries/strikes/IVs/OI used for straddle, term structure, skew and put/call OI
14. Own calculation from [13] and [19] — implied-move decomposition and realised-move statistics
15. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000079/saic-20260501.htm — Q1 FY27 10-Q: segment revenue/margins, $2.5B debt principal and maturities, $1.0B undrawn revolver, MARPA receivables sold, $1.2B remaining buyback authorisation, 42.3M shares outstanding, 20.9% tax rate, DOJ Antitrust grand jury subpoenas, DHS funding disruption
16. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000123/saic-20260814.htm — 19 Aug 2026 8-K: MUFG MARPA Amendment No. 6, facility limit $300M → $400M
17. https://data.sec.gov/submissions/CIK0001571123.json — complete SAIC filing index: all Item 2.02 8-K dates (earnings-day identification), 8-K cadence, Form 3/4 list; source for the 41-Form-4 open-market-transaction scan
18. https://stockanalysis.com/api/quotes/s/SAIC — spot $128.96 close 27 Aug 2026 4:00 PM EDT, +1.08%, after-hours $129.30 at 7:53 PM EDT, 52-week $81.08–$130.53
19. https://stockanalysis.com/api/symbol/s/SAIC/history?range=5Y&period=Daily — daily OHLC history used for every earnings-day move, run-up windows, realised vol, and 52-week-range position (also used for LDOS, CACI, BAH, PSN, KBR, VVX, ICFI, LHX peer reaction days)
20. /home/user/claude_research/research/2026/08/2026-08-28/00-universe.json — Nasdaq-sourced stage-0 record: EPS estimate $2.25, 4 analysts, fiscal quarter ending Jul/2026, market cap $5,393,676,568
21. https://www.tradingkey.com/markets/stocks/saic/forecast — next-quarter revenue $1.77B, EPS $2.31, 12 analysts, Hold, average PT $119.00 (range $91–$142.11)
22. https://stockstory.org/us/stocks/nasdaq/saic/news/earnings/saic-earnings-what-to-look-for-from-saic-2 — market expects revenue −2.4% y/y; "majority of analysts… reconfirmed their estimates over the last 30 days"
23. https://zacks.com/stock/quote/SAIC/detailed-estimates — Zacks FY27 consensus $9.61; "estimates broadly trending downward" (page bot-blocked; used via search snippet) `snippet_only`
24. https://www.thestockobserver.com/2026/08/19/jefferies-financial-group-raises-science-applications-international-nasdaqsaic-price-target-to-130-00.html — dated analyst actions (Jefferies 19 Aug $115→$130 Hold; TD Cowen 7 Jul $130→$125; UBS 3 Jun $113→$119; Citi 2 Jun $120→$132 Buy; JPMorgan 2 Jun $110→$125; BNP Exane 27 May init $95), average PT $116.89, institutional ownership 76%
25. https://www.sec.gov/Archives/edgar/data/1571123/000157112325000164/saic090420258-kexhibit991.htm — Q2 FY26 (prior-year comparable): revenue $1.769B, −3% organic, op income $139M/7.9%, adj EBITDA $185M/10.5%, GAAP EPS $2.71, adj EPS $3.63, FCF $150M, bookings $2.6B, B2B 1.5, backlog $23.2B, buybacks $106M
26. https://finance.yahoo.com/markets/stocks/articles/science-applications-international-corporation-saic-131504915.html — 52-week high commentary, three upward EPS revisions, P/E 13.8 `snippet_only`
27. https://www.globenewswire.com/news-release/2026/08/05/3339286/0/en/saic-wins-400-million-recompete-contract-with-u-s-intelligence-agency.html — $400M intelligence recompete, >$1.6B Intel/Space awards in H1 FY27; plus $118.4M VA award 6 Aug `snippet_only`
28. https://www.quiverquant.com/news/SAIC+Announces+Strategic+Restructuring:+Consolidation+of+Business+Groups+to+Enhance+Growth+and+Efficiency — five business groups consolidated to three effective 31 Jan 2026 `snippet_only`
29. https://benzinga.com/quote/SAIC/short-interest — alternative short-interest read: 3.0M shares, +6.7% period-on-period, 7.0% of float, +51.7% since July 2025 (page 403; used via search snippet) `snippet_only`
30. https://www.globenewswire.com/news-release/2026/08/25/3350873/6948/en/nasdaq-announces-mid-month-open-short-interest-positions-in-nasdaq-stocks-as-of-settlement-date-august-14-2026.html — most recent Nasdaq short-interest settlement date (2026-08-14), published 25 Aug
31. https://www.tipranks.com/news/the-fly/saic-price-target-raised-to-130-from-120-at-jefferies — Jefferies PT raise ahead of the 31 Aug fiscal Q2 report `snippet_only`
32. https://stocktwits.com/symbol/SAIC — 62% bullish, 1,356 messages, as of 28 Aug 2026
33. https://www.gurufocus.com/news/8893407/saic-raises-revenue-and-ebitda-forecasts-for-fy27 — Goldman Sachs PT $85 → $96 (9 Jun 2026) `snippet_only`
34. https://www.tipranks.com/news/the-fly/saic-price-target-raised-to-155-from-145-at-td-cowen — TipRanks/TheFly analyst-action feed for SAIC `snippet_only`
35. https://hiringlab.indeed.com/2025/11/20/indeed-2026-us-jobs-hiring-trends-report/ — federal-contractor labour-market context (not SAIC-specific)
36. https://www.sec.gov/Archives/edgar/data/1571123/000119312526341188/d104119d8k.htm — 10 Aug 2026 8-K Item 5.02: David C. Benson and David Cush appointed effective 20 Aug 2026, board expanded 10 → 12, both to Audit Committee
37. https://www.tipranks.com/news/company-announcements/science-applications-expands-board-with-two-new-directors — corroboration of the board expansion `snippet_only`
38. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000120/xslF345X06/wk-form4_1783368387.xml — Form 4, Vincent P. DiFronzo (EVP Air Force & Space, Intel), 2 Jul 2026, code G gift, no open-market sale
39. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000115/xslF345X06/wk-form4_1781035299.xml — Form 4, Kathleen T. McCarthy (EVP, CHRO), 6 Jun 2026, code F tax withholding at $114.35
40. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000081/xslF345X06/wk-form4_1780517031.xml — Form 4, Steven R. Shane (director), 2 Jun 2026, code M exercise at $77.65 + code F at $115.08
41. https://www.sec.gov/Archives/edgar/data/1571123/000157112326000111/xslF345X06/wk-form4_1780604173.xml — Form 4, David Urban (director), 3 Jun 2026, code A grant
42. https://finance.yahoo.com/news/investors-may-respond-saic-saic-231350814.html — headline claiming SAIC insider buying; **contradicted** by my full Form 4 scan [17], which found no code-P purchases since Sep 2025 `snippet_only`
43. https://www.globenewswire.com/news-release/2025/10/23/3172467/0/en/SAIC-Announces-CEO-Transition.html — 23 Oct 2025 CEO transition, Townes-Whitley out, Reagan interim `snippet_only`
44. https://virginiabusiness.com/townes-whitley-out-as-saics-ceo-after-two-years/ — separation "without cause", no reason given `snippet_only`
45. https://washingtonexec.com/2026/02/saic-names-jim-reagan-ceo-after-interim-tenure/ — Reagan named permanent CEO Feb 2026 `snippet_only`
46. https://www.washingtontechnology.com/companies/2026/02/saics-board-stays-reagan-names-him-full-time-ceo/411456/ — corroboration, effective 17 Feb 2026 `snippet_only`
47. https://www.sec.gov/Archives/edgar/data/0001571123/000157112326000069/saic-20260422.htm — DEF 14A: Ernst & Young LLP retained for FY ending 29 Jan 2027; FY26 audit fees $5,003,000 vs FY25 $5,005,000; total $5,299,888 vs $5,253,202; ratification vote 35,670,199 for / 306,713 against `snippet_only`
48. https://www.sec.gov/Archives/edgar/data/1571123/000157112325000107/saic-20250502.htm — prior-year 10-Q with the same DOJ Antitrust Division grand jury subpoena disclosure (April 2022 and October 2023), establishing it as unchanged language
49. https://www.fedtools.com/blog/government-shutdown-october-2026 — Senate passed CR 90–6 (H.R. 6500) funding to 11 Dec 2026; House vote pending `snippet_only`
50. https://www.americanactionforum.org/insight/a-fy-2027-appropriations-progress-report/ — FY2027 appropriations progress, CR most likely path `snippet_only`
51. https://www.govconwire.com/articles/leidos-q2-2026-earnings-results — Leidos Q2 2026: revenue $4.6B +7%, adj EBITDA margin 13.8%, defence book-to-bill 2.2x, raised FY guidance; Parsons Q2 revenue $1.6B, B2B 1.2x `snippet_only`
52. https://finance.biggo.com/news/US_LDOS_2026-08-04 — Leidos Q2 2026 call detail `snippet_only`
53. https://www.sec.gov/Archives/edgar/data/0001443646/000162828026049494/q1fy2027exhibit991_final.htm — Booz Allen Q1 FY2027 8-K exhibit: revenue $2.8B (−4.2%), adj EBITDA $334M (+7.4%), margin 11.9% (+130bp), adj EPS $1.81 (+22.3%), FCF $261M, backlog $39B, B2B 1.5x, guidance reaffirmed
54. https://www.govconwire.com/articles/booz-allen-2-8b-q1-fy2027-revenue-financial-results — corroboration of BAH Q1 FY27 `snippet_only`
55. https://www.sec.gov/Archives/edgar/data/0000016058/000162828026053448/fy26-q4caci20260805ex991.htm — CACI FY26 Q4 8-K exhibit (revenue $9.6B +10.9%, diluted EPS $24.16 +8.2%)

---

*This is a forecasting exercise over public information. It is research, not investment advice, and must not be relied upon as such. Figures are sourced or marked unavailable; anchors marked `snippet_only` were obtained from search-result snippets rather than a fetched page and carry lower confidence.*
