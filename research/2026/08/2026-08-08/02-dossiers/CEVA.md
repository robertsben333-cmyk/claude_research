# CEVA — CEVA, Inc.

**What this print is about.** Ceva is a ~$1.1bn semiconductor IP licensor (DSP, NPU, Wi-Fi/Bluetooth/UWB/5G connectivity IP) whose stock has been re-rated as an edge-AI proxy: +72.9% YTD and +79.9% over 52 weeks [4][5]. The Q2 print itself is unlikely to be the story — management guided Q2 revenue to $26–30m on the May call and Street consensus ($28.15m / $0.073) sits almost exactly on the guidance midpoint [12][31]. What the print actually trades on is whether management **reiterates the "top end of 8–12%" FY26 revenue guide**, which arithmetically requires a very large second-half royalty ramp (my calc: ~$68m of H2 revenue vs ~$55m in H1), and whether they can put commercial substance behind the July 6 "landmark" NeuPro-M AI licensing deal with an unnamed major U.S. software/AI platform company [22][23]. Two things make the setup uncomfortable: Q2 revenue estimates were cut ~9.4% over the prior three months [15], and the stock has run +16.2% in the five sessions into the report (my calc from sourced closes: $33.27 on Aug 3 → $38.67 on Aug 7) [5][26]. The last print is the tell — Ceva gapped +14.4% pre-market on a clean beat and closed **down 1.37%** [16][26][32]. Note also the triage premise that CEVA "surged 14% on its last beat" is **wrong on a closing basis**; that was an intraday premarket print that fully faded.

---

## 1. Event & anchors

`event_confirmed: true`

| Item | Value | As-of / source |
| --- | --- | --- |
| Earnings date | **Monday, 2026-08-10** | Company-scheduled release [2][3] |
| Session | **BMO** — release before NASDAQ open, call 8:30 a.m. ET | [2][3] |
| Fiscal period | Q2 2026 (quarter ended 2026-06-30) | [2] |
| Date changed / pre-announced? | No evidence of a date change or pre-announcement found | — |
| Spot | **$38.67** (close) | 2026-08-07 16:00 ET [5] |
| Prior close / 1-day move | $35.59 → $38.67, **+8.65%** | 2026-08-07 [5][26] |
| Market cap | **$1.08bn** | 2026-08-07 [5] |
| Shares outstanding | 27.86m (float 24.69m) | [5][6] |
| 52-week range | $17.02 – $51.60 | [5] |
| 50-DMA / 200-DMA | $41.87 / $28.48 | 2026-08-07 [6] |
| Beta (5Y) | 2.01 | [6] |
| Avg volume | 1,385,788 sh | [5] |
| **Event implied move** | **unavailable** — see caveat below | — |
| IV rank / IV percentile | **unavailable** | — |

**Implied-move caveat (important).** The only options datum I could source is OptionSlam's "Implied Move (Monthly): **20.56%**, expires August 21, 2026", 3 days to earnings, as of 2026-08-07 [32]. That is the straddle-implied move to the **Aug-21 monthly expiry** (CEVA appears not to have weeklies), i.e. it covers the earnings event *plus* nine subsequent sessions of a beta-2.0 small cap. It is an **upper bound**, not a clean event move, and is wildly above the realised earnings-day history below. I have therefore set `event_implied_move_pct: null` rather than pass a number that would corrupt downstream sizing. Treat 20.56% as "options are expensive into this print," not as the expected gap.

### Realised earnings-day moves (last 8 prints)

Ceva reports BMO, so the reaction day is the release day itself. Provenance is mixed and is labelled per row.

| Quarter | Release date | Session | Reaction | Basis / source |
| --- | --- | --- | --- | --- |
| Q1 2026 | 2026-05-11 | bmo | **−1.37%** ($36.97 → $36.46) | close-to-close, OptionSlam [32]; closes confirmed [26] |
| Q4 2025 | 2026-02-17 | bmo | **−9.79%** | 24-hour, Simply Wall St [11]; −11.38% on 48h basis [30] |
| Q3 2025 | 2025-11-10 | bmo | **−0.31%** | day-of [10][30] |
| Q2 2025 | 2025-08-11 | bmo | **+9.2%** | close, MarketBeat headline [33]; +8.61% on 48h basis [30] |
| Q1 2025 | 2025-05-07 | bmo | **−20.17%** | 24-hour, Simply Wall St [11]; −23.45% 48h [30]; investing.com cited −14.9% intraday [8] |
| Q4 2024 | 2025-02-13 | bmo | **+8.27%** | 48-hour, CoinCodex [30] |
| Q3 2024 | 2024-11-07 | bmo | +11.90% | 48-hour [30] |
| Q2 2024 | 2024-08-07 | bmo | +26.20% | 48-hour [30] |

**Last six (used in JSON):** −1.37, −9.79, −0.31, +9.2, −20.17, +8.27.
- Mean |move| **8.19%** · Median |move| **8.74%** · Max |move| **20.17%** (my calc from the rows above)
- Up/down pattern: **D, D, D, U, D, U → 2 up / 4 down**. Simply Wall St independently states "four of the last five earnings events from Feb 13, 2025 through Feb 17, 2026 produced negative 24-hour price reactions" [11], which corroborates the skew.
- Intraday behaviour matters more than the close here: on 2026-05-11 the stock was indicated **+14.4% pre-market**, traded −6.3% by mid-morning, printed a max adverse excursion of −10.73%, and closed −1.37% [16][32]. This is a name that gaps on headlines and gives it back.

---

## 2. The bar

**Consensus (Q2 2026)**
| Metric | Consensus | Source |
| --- | --- | --- |
| EPS (non-GAAP) | **$0.073** | Investing.com earnings table, as-of 2026-08-08 [31] |
| EPS (alt. print) | $0.08 | [15] `snippet_only` |
| Revenue | **$28.15m** | Investing.com [31] |
| Revenue (alt. prints) | $28.50m; $28.633m on 10 analysts | [15] `snippet_only` |
| Analyst count (ratings) | 9 analysts, "Buy" consensus, avg PT $50.00 | stockanalysis, 2026-08-07/08 [5] |
| FY2026 consensus | Revenue $123.16m, EPS $0.51 | [15] `snippet_only` |

**Company guidance given on the May 11 call (this is the actual bar):** [12]
- Q2 revenue **$26–30m**
- Gross margin 87% GAAP / **88% non-GAAP**
- Opex: GAAP $27.7–28.7m / **non-GAAP $22.2–23.2m**
- Net interest income ~$1.7m; taxes ~$1.5m; non-GAAP share count 29.7m
- FY26: revenue growth at the **top end of 8–12%**; non-GAAP operating margin and net income **+40–50% YoY**; combined COGS+opex up ~8% vs 2025

**My bridge (inference, arithmetic from [12]):** at the $28m guidance midpoint, 88% GM → $24.6m gross profit, less $22.7m non-GAAP opex = $1.9m op income, +$1.7m interest, −$1.5m tax = $2.1m ÷ 29.7m shares ≈ **$0.072**. Consensus $0.073 is therefore *exactly* the guidance midpoint. At the $30m top end the same bridge yields ~$0.13; at the $26m low end, ~$0.01. **EPS leverage to the revenue line is brutal** — a $2m revenue miss roughly halves EPS. That is the single most important structural fact about this print.

**FY arithmetic (my calc).** FY25 revenue was $109.6m [9]. Top end of 8–12% = ~$122.8m. Less Q1 $27.0m [1] and ~$28m for Q2 implies **~$67.8m of H2 revenue, ~$34m per quarter** — versus a record Q4'25 of $31.3m [9]. Management explicitly leans on a historical ~40% H1→H2 sequential ramp [12], but the required run-rate is above anything Ceva has printed. Reiterating "top end" on Monday is therefore a genuinely load-bearing statement, not boilerplate.

**Revisions.** Q2 revenue estimate revised **down 9.44% over the trailing 3 months** [15] `snippet_only`. As of the May print, Ceva had "0 positive EPS revisions and 3 negative EPS revisions in the last 90 days" [16]. I could not source clean 30/60/90-day EPS revision breadth from a primary estimate provider — see coverage gaps. Direction of drift is unambiguously **negative on revenue, into a stock that has re-rated hard.**

**Whisper number.** No credibly published whisper found. `unavailable`.

**What has to be delivered to hold the stock flat (my inference):** revenue at or above ~$28.5m (upper half of guide), non-GAAP EPS ≥ $0.08, **an explicit reiteration of the "top end of 8–12%" FY guide**, a Q3 revenue guide with a ≥$32m midpoint, and royalty revenue materially above Q1's $9.2m. Anything less than a Q3 guide starting with a 3 and the H2 ramp thesis breaks.

---

## 3. The one metric that matters

**Royalty revenue and the implied H2 royalty ramp — not headline EPS.**

Why: licensing is already at a three-year high ($17.8m in Q1, +18% YoY) and the big licensing headline (the NeuPro-M deal) was pre-announced on July 6 [22][23], so it is in the price and, being a Q3 event, is almost certainly not in Q2 revenue. Royalties are where the surprise lives. Q1'26 royalties were **$9.2m, flat YoY** [1], versus Q4'25 royalties of **$13.8m — the strongest in four years** [9]. Management's entire FY bridge rests on royalties re-accelerating in H2 [12].

**What the market expects for it and how I know:** I could not source a published Q2 royalty consensus (`unavailable`). But management's own drivers, stated on the May call [12], set the expectation: non-mobile/smart-edge royalties +8% YoY; industrial IoT revenue +19% on higher-ASP mix; cellular IoT units +38% YoY; Wi-Fi at a record 91m units (+158%); Bluetooth/Wi-Fi combos doubling in volume at higher ASPs; automotive AI entering production in the 2026 Toyota RAV4 via Renesas R-Car V4H; and "stronger high-end smartphone royalties in the second half." The offset management named is smartphone softness and memory-pricing/inventory constraints [1][12].

**The tell to watch on the 8:30 call:** whether royalty dollars are ≥ ~$11m (sequential recovery toward the Q4'25 run-rate) and whether management repeats the ~40% H1→H2 language. Note Ceva does **not** put guidance in the press release — the Q1 release contained none [1] — so the 8:30 a.m. call, not the 8:00 a.m. headline, is where the move gets made. The May 11 open was a trap for exactly this reason.

---

## 4. Fundamentals — what changed, what is at stake

**Q1 2026 actuals (most recent reported quarter)** [1][17]
- Revenue **$27.0m, +11% YoY**; licensing & related **$17.8m, +18% YoY** (3-year high); royalties **$9.2m, ~flat**
- GAAP GM 86% / non-GAAP GM 87%
- GAAP operating loss **$5.1m** (vs −$4.4m); non-GAAP operating income **$0.5m** (vs $0.3m)
- GAAP diluted EPS **−$0.16** (vs −$0.14); non-GAAP diluted EPS **$0.04** (vs $0.06 — *down* YoY)
- 14 licence agreements signed, incl. 2 OEM and 3 multi-technology deals
- 458m Ceva-powered devices shipped, incl. record 91m Wi-Fi units
- AI >20% of licensing & related revenue

**FY2025 baseline** [9]: revenue $109.6m; Q4'25 record $31.3m (+7% YoY) with licensing $17.5m (+11%) and royalties $13.8m (+2%, best in 4 years); 18 licence deals in Q4; 10 NPU deals signed in 2025; 2.1bn devices shipped in the year; Q4'25 non-GAAP GM 89%, non-GAAP net income $4.9m (+86%).

**Balance sheet & cash** [1][12][19]
- Cash & equivalents $21.4m; marketable securities + deposits $194.3m; **~$216m total cash & investments**
- Total assets $388.2m; stockholders' equity $338.2m; no debt disclosed in the sourced materials
- **Q1'26 operating cash flow −$4.885m**; capex $2.3m; **FCF negative** [19]
- TTM revenue $112.38m; TTM net loss $11.77m [5]
- DSO 59 days; D&A $0.9m/qtr; headcount 430 (348 engineers) [12]

**Dilution.** Shares outstanding +6.74% YoY and **+8.29% QoQ** [6]. Equity comp is ~$5.3m/qtr embedded in the GAAP-to-non-GAAP bridge [12]. The last disclosed buyback action I could source is the **November 2024** expansion (+700k shares, ~1,056k total available) [21]; management gave **no buyback commentary on the Q1'26 call** [12]. Net: the company is diluting, not shrinking, the share count — a real negative for a business that generates no GAAP profit.

**Customer concentration.** Not sourced at the named-customer level. Structurally, Ceva's royalty base is broad (Wi-Fi/BT combos across many SoC vendors), but licensing is lumpy and the July NeuPro-M deal is a single-customer concentration event by construction. Marked `unavailable` — see gaps.

**What changed since the last print (Q1, May 11):**
1. **2026-07-06** — Landmark AI licensing deal, NeuPro-M selected by a major unnamed U.S. software/AI platform company for a custom AI silicon programme. Stock +13.3% to $45.81 that day [22][23][24].
2. **2026-07-13** — 8-K, Item 5.02: **COO Michael Boukaya resigns effective 2026-08-01**, remaining through 2026-12-31 for transition [27][28].
3. **2026-08-04** — Actions Technology launches ATS296X Bluetooth audio chips on Ceva-Waves Bluetooth HDT — the earliest commercial HDT deployment; throughput 2 Mbps → ~7.5 Mbps [25].
4. Stock round-tripped: 52-week high **$51.59/$51.60** in early-to-mid July [5][29], down to $33.27 on Aug 3, back to $38.67 on Aug 7 [26].

---

## 5. Positioning & options

| Metric | Value | As-of / source |
| --- | --- | --- |
| Short interest | 1.98m shares | stockanalysis, latest settlement [6] |
| Short % shares out / % float | 7.12% / **8.03%** | [6] |
| Days to cover (short ratio) | **2.56** | [6] |
| SI trend | up from 1.77m prior month | [6] |
| Institutional ownership | 84.2% (stockanalysis) / 85.4%, 386 holders, 25.6m sh (Fintel) | [6][34] |
| Insider ownership | 2.90% | [6] |
| OI put/call ratio | 0.14 (bullish-skewed) | Fintel, `snippet_only`, undated [18] |
| IV term structure / skew | **unavailable** | — |
| Borrow fee | **unavailable** | — |
| Unusual options activity | **unavailable** | — |
| Monthly straddle implied move (Aug-21) | 20.56% | OptionSlam, 2026-08-07 [32] |
| Earnings Volatility Rating (OptionSlam) | 5.3 | [32] |

**Run-up into the print (my calc from sourced closes [26]):** Aug 3 $33.27 → Aug 4 $36.22 (+8.87%) → Aug 5 $34.24 (−5.47%) → Aug 6 $35.59 (+3.94%) → Aug 7 $38.67 (+8.65%). That is **+16.2% over five sessions**, on two >8% up days, into a BMO print. Volatility of daily returns in that window is itself extreme.

**Crowding read (my inference).** The name looks *moderately* crowded long and lightly crowded short. 8% of float short with only 2.6 days to cover is not a squeeze setup — the float turns over fast enough that shorts can exit. A 0.14 OI put/call skews the option book heavily to calls, which is consistent with a retail/momentum long tilt and means dealer positioning is unlikely to cushion a downside gap. Institutions own ~85%, so the marginal buyer into the pre-earnings ramp is more likely fast money than a new long-term holder. The combination I dislike most: a +16% five-session run-up, a call-heavy option book, and a stock that has closed *down* on four of its last six prints.

---

## 6. Sentiment & alt-data

**Analyst rating and PT drift (chronological):**
- 2026-05-11/12 (post-Q1): TD Cowen $24→$45; Rosenblatt $40→$45; UBS $42→$48; Oppenheimer $30→$42; Stifel $30→$42; JPMorgan $30→$36 [14]. Separately, investing.com reported JPMorgan **initiating at Neutral, $30** around the same print [16] — I could not reconcile these two accounts; treat the JPM datapoint as uncertain.
- 2026-06-15: **Needham initiates Buy, $55**, citing "Physical AI potential" [20].
- 2026-07-10: **Stifel (Ruben Roy) $42→$50**, Buy reiterated [20][24].
- ~mid/late July 2026: **Benchmark initiates Hold, no price target, on valuation** — noted the stock had "more than doubled from its 52-week low" [20]. Exact date `unavailable`.
- Consensus prints, conflicting across vendors: stockanalysis 9 analysts, Buy, avg PT **$50.00** (2026-08-07) [5]; TipRanks "Strong Buy", median PT **$45.00** as of 2026-07-12 [14]; Danelfin avg PT $43.12 [13]; Benzinga-cited avg forecast $40.80 [24]; WallStreetZen 1Y PT $30.33 [17]. Spread of $30–$55 on a $38.67 stock is itself a signal of low analyst conviction.

**Drift direction (my read):** price targets rose steeply from May through July 10, then **stopped rising** — the most recent initiation (Benchmark) is a valuation-driven Hold. PT drift has flattened right as the stock corrected from $51.60 to $33 and back. That is a late-cycle pattern for a re-rating.

**Retail/social (supporting colour only, low weight):** StockTwits shows bullish posting including a widely-followed account with a $53 target [13] `snippet_only`. Danelfin AI Score 6/10 ("Hold"), probability advantage +3.71% over 3 months, sentiment component +14.13% [13]. I could not source a quantified 7/14/30-day social-tone trend series — see gaps.

**Alt-data proxies:** I could not source Google Trends, app ranks, web traffic, job postings, or channel checks for Ceva. This is expected — Ceva sells IP to ~a few hundred SoC customers, so consumer alt-data is structurally uninformative. The nearest real proxies are (a) partner product launches, where the Aug 4 Actions Technology ATS296X HDT launch is a genuine commercialisation datapoint [25], and (b) the NeuPro-Nano AI award at embedded world 2026 (110+ submissions) [35], which is reputational rather than financial.

---

## 7. Forensics

**Form 4 activity** [7][27][36]
| Date | Insider | Role | Action | Shares | Price | Value |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-02-20 | Yaniv Arieli | CFO | **Open-market buy** | 2,500 | $19.34 | $48,350 |
| 2026-02-19 | Yaniv Arieli | CFO | RSU acquisition | 17,793 | — | — |
| 2026-02-23 (rep.) | Amir Panush | CEO | **Open-market buy** | 5,100 | ~$19.70 | $100,470 |
| 2026-05-15 | Michael Boukaya | COO | Disposition | 20,500 | $36.13 | $740,665 |
| 2026-05-20 | Gweltaz Toquet | CCO | Disposition | 20,922 | $37.50 | $784,575 |
| 2026-06-02 | 6 directors | Board | Option/RSU awards | 3,325 ea. | — | $0 |
| 2026-06-09 | Louis Silver | Director | Option exercise + withholding | 13,000 @ $27.17 / 7,736 @ $45.66 | — | $353,210 |
| 2026-06-09 | Peter McManamon | Director | Option exercise + withholding | 14,000 @ $27.17 / 8,331 @ $45.66 | — | $380,380 |

**Reading it (my inference, with a caveat).** The February cluster is a genuine bullish signal: CEO *and* CFO buying on the open market within days of each other, at ~$19.34–19.70, with the stock near its 52-week low [7]. That trade is now up ~100%. The May dispositions are the ambiguous piece: secform4 classifies Boukaya's 20,500 shares as a sale [36], but StockTitan's headline for the same filing reads "COO **returns** 20,500 shares to issuer at $36.13" [28] — language consistent with a **Code-F tax withholding**, not a discretionary sale. I could not open the underlying Form 4 to confirm the transaction code, so **treat the May dispositions as unclassified**. I found **no evidence** of 10b5-1 plan adoption disclosures either way. `10b5-1 vs discretionary: unavailable.`

**Departures.**
- **2026-07-13, 8-K Item 5.02:** EVP & COO **Michael Boukaya resigns the COO role effective 2026-08-01**, remaining with the company through 2026-12-31 [27][28]. A COO exit six weeks after the company's biggest-ever licensing announcement, with the incumbent selling/withholding ~$740k of stock in May, is the sharpest negative forensic in this file. Sell-side framing calls it "uncertainty around operational follow-through" on the edge-AI/wireless IP execution strategy [28].
- **2026-04-20:** Director Sven-Christer Nilsson retired from the board effective immediately prior to the 2026 annual meeting [27].

**Auditor / restatement.** Kost Forer Gabbay & Kasierer (EY Israel) ratified as auditor for FY2026 at the 2026-06-02 annual meeting [8-K Item 5.07, 2026-06-03] [27][37]. **No restatement, material weakness, or auditor change found.** FY2025 10-K filed 2026-02-27 [37].

**8-K cadence.** EDGAR's 8-K browse returned only two non-earnings 8-Ks in 2026: 2026-06-03 (Item 5.07, annual meeting) and 2026-07-13 (Item 5.02, COO) [27]. Earnings 8-Ks exist separately [1][9]. Cadence is normal-to-quiet; the July 5.02 filing is the outlier.

**Pre-announcement signalling.** None for Q2 results. The July 6 NeuPro-M press release is a **business** pre-announcement, not a financial one — no deal value, no revenue timing, no customer name disclosed [22][23]. My inference: the absence of any quantification means the Street cannot model it, so Monday's call commentary on the deal's revenue recognition is a live catalyst in both directions.

**Filing-language / tone.** Q1'26 release contained **no forward guidance at all** [1] — a change investing.com explicitly flagged as removing a bullish catalyst [16]. If the Q2 release again withholds guidance, expect the same open-then-fade mechanic.

---

## 8. Macro & peer read-through

**Sector regime.** Semis are the leadership trade of 2026: the Invesco PHLX Semiconductor ETF (SOXQ) is +99% YTD and +58% over three months, versus broader tech +21.5% [38]. Global semiconductor sales hit $403.3bn in Q2 2026, +35.1% QoQ, with SIA looking for >$1.5tn for the full year [39]. But there is a crack: "some air has come out of the semiconductor bubble" in late July, with leveraged bearish semi ETFs up ~58% in a month [38]. Ceva's own July round-trip ($51.60 → $33.27) fits that sector de-rating far better than it fits anything company-specific.

**IP-licensing peers who already reported.**
- **Arm (FY Q2 2026):** revenue $1.1bn +34% YoY; **licensing +56%**, **royalty +21%**, driven by Armv9 mix, Neoverse and CSS [40]. Strong read-through for the *licensing* line and for the "IP vendors capture more value per design" thesis Ceva articulates.
- **Rambus (Q2 2026, reported 2026-07-27):** first-ever >$200m quarter at $207.4m; **royalties $84.2m, +22% YoY** on AI/data-centre memory demand [41][42].
Both confirm that IP royalties tied to **AI/datacentre** are inflecting. Ceva's royalty base, however, is **edge/consumer/IoT/automotive**, not datacentre — so the peer read is directionally supportive of licensing but only weakly supportive of Ceva's specific royalty pool. That distinction is the main reason I discount the "peers are ripping, so CEVA rips" argument.

**Supply-chain / input read-throughs.**
- **Memory pricing and availability** is the named headwind: management cited memory constraints hitting Q1 IoT unit volumes and flagged "near-term memory pricing uncertainty" for the rest of 2026 [12]. Rising DRAM/NAND cost inflates consumer-device BOMs and can suppress the unit shipments Ceva earns per-unit royalties on. Nasdaq's own SOX research frames 2026 as "AI tailwinds and **memory shortages**" [43].
- **Smartphones** remain the drag: Q1 royalties were held flat by smartphone softness [1][12], and management is banking on "stronger high-end smartphone royalties in the second half."
- **Automotive:** Renesas R-Car V4H with Ceva AI DSP in production in the **2026 Toyota RAV4** — Ceva's first mass-volume automotive AI royalty stream [1][12]. NXP and Renesas are the named automotive AI royalty contributors [12].

**Rate/FX/commodity sensitivity (my inference).** Ceva is a high-beta (2.01 [6]), long-duration, unprofitable-on-GAAP small cap: it is a rates-sensitive *multiple* story, not a rates-sensitive *earnings* story. R&D is predominantly Israel-based, so a stronger shekel raises opex; I could not source FX-sensitivity disclosure or hedging detail (`unavailable`). ~$216m of cash generates ~$1.7m/qtr of interest income [12] — roughly 80% of the entire non-GAAP EPS bridge at the guidance midpoint, which means **falling short rates mechanically compress EPS**.

---

## 9. Bull case / bear case / base case

**Bull.** The Q2 bar is low and has been *lowered further*: Street revenue was cut 9.4% in three months [15], and consensus EPS of $0.073 sits precisely at the midpoint of a guide management themselves set only three months ago [12][31]. Licensing momentum is real and accelerating — $17.8m in Q1 was a three-year high, 14 deals signed, AI >20% of licensing [1] — and the July 6 NeuPro-M win with a major U.S. software/AI platform company genuinely broadens the TAM from chipmakers to hyperscaler-adjacent custom silicon [22][23]. The Aug 4 Actions Technology ATS296X launch proves Bluetooth HDT is shipping commercially, not just licensed [25]. Peers confirm the regime: Arm licensing +56%, Rambus royalties +22% [40][41]. Operating leverage is extreme in both directions — a $30m top-end quarter mathematically produces ~$0.13 non-GAAP EPS (my bridge from [12]), an ~80% beat. CEO and CFO both bought stock on the open market in February at ~$19 [7]. And the stock is still 25% below its $51.60 July high [5], so this is not a name at its highs going into the print.

**Bear.** Ceva gaps on headlines and gives it back: the last print was a 100% EPS beat with a +14.4% pre-market indication that closed **−1.37%**, with a −10.73% max adverse excursion intraday [16][32][26]. Four of the last six prints closed lower [11]. The stock has just run **+16.2% in five sessions** into a BMO report [26], on a call-heavy option book (OI put/call 0.14 [18]) with only 2.6 days-to-cover of shorts to squeeze [6] — i.e. the fuel is on the long side, not the short side. The FY "top end" guide requires ~$68m of H2 revenue versus ~$55m in H1 (my calc from [1][9][12]), a step-up above any half Ceva has printed, and it depends on a smartphone royalty recovery management has been promising while royalties printed **flat YoY in Q1** [1]. Non-GAAP EPS *declined* YoY in Q1 ($0.04 vs $0.06) [1], operating cash flow was **−$4.9m** [19], share count is up 8.3% QoQ [6], and the company has no GAAP profit. The COO resigned effective Aug 1 [27][28] weeks after the flagship deal. Benchmark initiated **Hold on valuation** [20], and PT drift has flattened. Sector-wide, semis wobbled hard in late July [38] and memory-cost inflation is a live headwind management themselves named [12][43].

**Base case (my read).** An in-line-to-modestly-better Q2 — revenue $28–29m, non-GAAP EPS $0.08–0.10 — with FY guidance reiterated at "top end of 8–12%" but *without* the specificity the market now needs on H2 royalties or on NeuPro-M revenue timing. The press release again carries no guidance [1], so the 8:00 a.m. headline is ambiguous and the move is decided on the 8:30 call. Given a +16% five-session run-up, a call-heavy book, and a company whose only lever for a positive surprise (royalties) printed flat last quarter, I think the modal outcome is a small-to-moderate negative close, with a fat right tail if royalties come in near $12m+ and Q3 is guided above $32m. Expected magnitude ~7–9% in absolute terms (in line with the 8.19% mean / 8.74% median realised), skewed down.

---

## 10. What would flip the consensus view

The single most credible reversal is **royalty revenue printing ≥ ~$12m with a Q3 revenue guide midpoint ≥ $33m**, explicitly attributed to (a) Bluetooth/Wi-Fi combo ASP uplift, (b) the Renesas/Toyota RAV4 automotive AI ramp, and (c) a *quantified* contribution from the NeuPro-M platform deal. That combination would do three things at once: validate the H2 arithmetic that currently only exists as a management assertion, convert the July 6 press release from a narrative event into a modelled revenue line, and re-rate royalties from "flat and smartphone-hostage" to "the growth line." Under that outcome I would expect the fade pattern to break and the stock to hold a double-digit gain, because the bear case here is almost entirely "the H2 ramp is unmodellable" rather than "the business is bad."

The mirror-image flip: if management *softens* the FY language from "top end of 8–12%" to plain "8–12%", or declines to guide Q3 at all, the stock should trade to the low $30s regardless of the Q2 beat, because the entire $38.67 price rests on the H2 ramp being real.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **Event-implied move (clean ATM straddle for first post-earnings expiry)** | The core sizing anchor. Only a full-cycle Aug-21 monthly implied move (20.56%) was sourceable [32], which conflates the event with 9 days of beta-2.0 drift. Without it, the panel cannot judge whether the option market is pricing the print rich or cheap versus the 8.19% mean realised. |
| **IV rank / IV percentile / IV term structure / skew** | No vol-surface data reachable (Barchart, MarketChameleon, Fintel all blocked or paywalled). Cannot assess IV-crush risk or whether puts are bid. |
| **Borrow fee / hard-to-borrow status** | Short % of float is 8.03% with 2.56 days to cover [6]; without borrow cost I cannot tell whether that short base is conviction or cheap hedging. |
| **Unusual options activity / pre-earnings flow** | Would materially sharpen the crowding read given the 0.14 OI put/call. |
| **Q2 royalty and licensing consensus (segment-level)** | The one metric that matters has no published expectation I could source. The panel is judging the key line without a bar. |
| **Clean 30/60/90-day EPS revision breadth from a primary provider** | Only a 3-month revenue revision (−9.44%) [15] and a May-dated 0-up/3-down count [16]. Cannot date the estimate drift precisely. |
| **Whisper number** | None credibly published. |
| **Transaction codes on the May 2026 COO/CCO Form 4 dispositions** | Sources conflict between "sale" [36] and "returned to issuer" [28]. Changes the forensic sign from bearish to neutral. |
| **10b5-1 plan status for all insider transactions** | Not disclosed in any source reached. |
| **Named customer concentration (% of revenue from top customers)** | 10-K/10-Q concentration table not extractable; matters because licensing is lumpy and single-deal-driven. |
| **Exact Feb 2026 daily closes (Feb 13/17/18)** | The Q4'25 reaction is taken from a secondary 24-hour figure (−9.79%) [11] rather than verified closes. |
| **FX/shekel exposure and hedging** | Israel-based R&D cost base; unquantified. |
| **Current buyback activity / remaining authorisation as of Q2'26** | Last sourced action is Nov-2024 [21]; no Q1'26 call commentary [12]. Share count is rising 8.3% QoQ [6] — the panel should know whether buybacks are dormant. |
| **Google Trends / job postings / web-traffic alt-data** | Not sourced; structurally low-signal for a B2B IP licensor, but the absence is noted. |
| **Blocked/unreachable domains** | chartmill.com (403), tipranks.com (403), simplywall.st direct page (403), macrotrends.net (403), fintel.io (403), wsj.com (blocked), nasdaq.com short interest (data not published), marketchameleon/optionsearnings (paywalled), openinsider (503). |

---

## 12. Sources

1. Ceva Q1 2026 financial results (press release) — Q1 revenue/segments/margins/EPS/balance sheet/units; confirms no guidance in release — https://www.prnewswire.com/news-releases/ceva-inc-announces-first-quarter-2026-financial-results-302767706.html and https://www.ceva-ip.com/press/ceva-inc-announces-first-quarter-2026-financial-results/
2. Ceva schedules Q2 2026 earnings release and conference call — date, BMO, 8:30 a.m. ET call — https://www.stocktitan.net/news/CEVA/ceva-inc-schedules-second-quarter-2026-earnings-release-and-xz1m0xyej9pr.html
3. Ceva Q2 2026 earnings date confirmation (secondary) — https://www.barchart.com/story/news/3180821/ceva-inc-schedules-second-quarter-2026-earnings-release-and-conference-call
4. Simply Wall St — CEVA +72.9% YTD, valuation after rally — https://simplywall.st/stocks/us/semiconductors/nasdaq-ceva/ceva/news/is-ceva-ceva-above-fair-value-after-a-73-rally
5. StockAnalysis CEVA overview — spot $38.67 (2026-08-07 16:00 EDT, +8.65%), market cap $1.08bn, 27.86m shares, 52-wk range, avg volume, TTM revenue/net loss, 9 analysts / Buy / $50 avg PT — https://stockanalysis.com/stocks/ceva/
6. StockAnalysis CEVA statistics — short interest 1.98m, 7.12% of shares out, 8.03% of float, 2.56 days to cover, float 24.69m, shares +8.29% QoQ, beta 2.01, 50/200-DMA, institutional 84.22%, insider 2.90% — https://stockanalysis.com/stocks/ceva/statistics/
7. Insider cluster buying Feb 2026 — CFO Arieli 2,500 sh @ $19.34; CEO Panush 5,100 sh / $100,470 — https://www.investing.com/news/insider-trading-news/arieli-ceva-cfo-buys-48k-of-ceva-stock-93CH-4520483 and https://www.tipranks.com/news/insider-trading/top-ceva-executives-quietly-place-a-big-bet-on-their-own-company-insider-trading-news
8. CEVA Q1 2025 earnings reaction (stock −14.9%) — https://www.investing.com/news/transcripts/earnings-call-transcript-ceva-q1-2025-misses-forecasts-stock-falls-149-93CH-4028851
9. Ceva Q4 & FY2025 results — Q4 revenue $31.3m, licensing $17.5m, royalties $13.8m (4-yr high), FY25 $109.6m, 18 deals, 2026 guide 8–12% — https://www.prnewswire.com/news-releases/ceva-inc-announces-fourth-quarter-and-full-year-2025-financial-results-302688881.html
10. CEVA Q3 2025 earnings and −0.31% day-of reaction — https://www.investing.com/news/transcripts/earnings-call-transcript-ceva-q3-2025-revenue-rise-but-eps-misses-forecast-93CH-4346422
11. Simply Wall St CEVA analysis — "four of the last five earnings events … produced negative 24-hour price reactions", −20.17% on Q1'25, −9.79% after Q4'25 — https://simplywall.st/stocks/us/semiconductors/nasdaq-ceva/ceva
12. Ceva Q1 2026 earnings call transcript — full Q2 and FY26 guidance, opex/tax/share count, royalty drivers by end market, H1→H2 ramp, cash $216m, OCF −$4.9m, capex $2.3m, headcount 430/348 — https://www.fool.com/earnings/call-transcripts/2026/05/12/ceva-ceva-q1-2026-earnings-transcript/
13. Danelfin CEVA AI stock analysis — AI Score 6/10 Hold, +3.71% probability advantage, sentiment +14.13%, $43.12 avg PT; StockTwits $53 bullish call — https://danelfin.com/stock/CEVA
14. MarketBeat CEVA forecast — May 12 2026 PT raises (TD Cowen, Rosenblatt, UBS, JPMorgan, Oppenheimer, Stifel); TipRanks Strong Buy / $45 median as of 2026-07-12 — https://www.marketbeat.com/stocks/NASDAQ/CEVA/forecast/ and https://www.tipranks.com/stocks/ceva/forecast
15. Trefis / consensus aggregation — Q2'26 EPS $0.08, revenue $28.50m and $28.633m (10 analysts), revenue estimate −9.44% over 3 months, FY26 $123.16m / $0.51 — https://www.trefis.com/data/companies/ceva
16. "Why is CEVA stock sliding today?" — +14.4% pre-market indication, −6.3% mid-morning, no guidance in release, 0 up / 3 down EPS revisions in 90 days, JPMorgan Neutral $30 — https://www.investing.com/news/stock-market-news/why-is-ceva-stock-sliding-today-93CH-4676925
17. CEVA Q1 2026 10-Q — revenue detail, 14 licences, 458m units / 91m Wi-Fi, cash and balance sheet — https://www.sec.gov/Archives/edgar/data/0001173489/000143774926016119/ceva20260331_10q.htm ; WallStreetZen 1Y PT $30.33 — https://www.wallstreetzen.com/stocks/us/nasdaq/ceva/stock-forecast
18. Fintel CEVA options — OI put/call ratio 0.14 — https://fintel.io/sopt/us/ceva
19. Finimize / StockTitan 10-Q summary — Q1'26 operating cash flow −$4.885m, negative FCF — https://finimize.com/content/ceva-asset-snapshot and https://www.stocktitan.net/sec-filings/CEVA/10-q-ceva-inc-quarterly-earnings-report-3de345f1f249.html
20. Analyst actions — Needham initiates Buy $55 (2026-06-15, "Physical AI"); Stifel $42→$50 (2026-07-10); Benchmark initiates Hold, no PT, on valuation — https://www.investing.com/news/analyst-ratings/needham-initiates-ceva-stock-with-buy-rating-on-ai-potential-93CH-4741807 , https://za.investing.com/news/stock-market-news/stifel-raises-ceva-stock-price-target-to-50-on-ai-positioning-93CH-4364313 , https://www.investing.com/news/analyst-ratings/benchmark-initiates-hold-rating-on-ceva-stock-citing-valuation-93CH-4795164
21. Ceva share repurchase program expansion (Nov 2024, +700k shares, ~1,056k available) — https://www.prnewswire.com/news-releases/ceva-inc-announces-expansion-of-existing-share-repurchase-program-302298414.html
22. Ceva wins landmark AI licensing deal — NeuPro-M selected by major U.S. software/AI platform company for custom AI silicon (2026-07-06) — https://www.prnewswire.com/news-releases/ceva-wins-landmark-ai-licensing-deal-with-major-us-software-and-ai-platform-company-302818112.html
23. Same deal, StockTitan coverage — https://www.stocktitan.net/news/CEVA/ceva-wins-landmark-ai-licensing-deal-with-major-u-s-software-and-ai-k1xqp0x16cc4.html
24. Benzinga — CEVA +13.3% to $45.81 on 2026-07-06 on the AI deal; Stifel PT $50; avg forecast $40.80 — https://www.benzinga.com/trading-ideas/movers/26/07/60277836/why-is-ceva-stock-gaining-monday
25. Ceva + Actions Technology ATS296X Bluetooth HDT audio chips (2026-08-04) — throughput 2 → ~7.5 Mbps, earliest commercial HDT implementation — https://www.prnewswire.com/news-releases/ceva-and-actions-technology-collaborate-to-bring-bluetooth-hdt-audio-chips-to-market-302839955.html
26. Daily closes — May 8 $36.97, May 11 $36.46, May 12 $37.08; Aug 3 $33.27, Aug 4 $36.22, Aug 5 $34.24, Aug 6 $35.59, Aug 7 $38.67 — https://www.financialcontent.com/quote/NQ:CEVA/historical and https://stockanalysis.com/stocks/ceva/history/
27. SEC EDGAR CEVA 8-K list 2026 — 2026-07-13 Item 5.02 (COO), 2026-06-03 Item 5.07 (annual meeting); director Nilsson retirement 8-K 2026-04-20 — https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001173489&type=8-K&dateb=&owner=include&count=40 and https://www.otcmarkets.com/filing/html?id=19353910&guid=XLj-kqh88tkGdth
28. Simply Wall St — COO Michael Boukaya resigns COO role effective 2026-08-01, stays through 2026-12-31; execution-risk commentary — https://simplywall.st/stocks/us/semiconductors/nasdaq-ceva/ceva/news/how-does-cevas-ceva-coo-transition-shape-its-edge-ai-executi ; StockTitan Form 4 "COO returns 20,500 shares to issuer at $36.13" — https://www.stocktitan.net/sec-filings/CEVA/form-4-ceva-inc-insider-trading-activity-7efc8e192a57.html
29. Ceva stock hits 52-week high at $51.59 (July 2026), +133.76% over prior year — https://ca.investing.com/news/stock-market-news/ceva-stock-hits-52week-high-at-5159-usd-93CH-4701081
30. CoinCodex CEVA earnings history — 8 quarters of EPS est/actual and 48-hour post-earnings price change — https://coincodex.com/stock/CEVA/earnings/
31. Investing.com CEVA earnings table — Q2'26 consensus EPS $0.073 / revenue $28.15m; 10-quarter history of dates and estimates — https://www.investing.com/equities/ceva-earnings
32. OptionSlam CEVA — next earnings 2026-08-10, 3 days to earnings, Implied Move (Monthly, Aug-21 expiry) 20.56%, EVR 5.3; May 11 2026 row: pre-close $36.97, post-open −2.56%, one-day close change −1.37%, max movement −10.73% — https://www.optionslam.com/earnings/stocks/CEVA
33. MarketBeat — CEVA stock price up 9.2% following strong earnings (2025-08-12, on the 2025-08-11 Q2'25 print) — https://www.marketbeat.com/instant-alerts/ceva-nasdaqceva-stock-price-up-92-following-strong-earnings-2025-08-12
34. Fintel CEVA institutional ownership — 386 institutional holders, 25,598,293 shares, 85.37% institutional, 90 buyers / 64 sellers TTM — https://fintel.io/so/us/ceva
35. Ceva NeuPro-Nano NPU wins AI category, embedded award 2026 (110+ submissions) — https://www.prnewswire.com/news-releases/cevas-neupro-nano-npu-wins-artificial-intelligence-award-at-embedded-world-2026-302711611.html
36. SECForm4 CEVA insider transaction list 2026 — May/June Form 4 detail — https://www.secform4.com/insider-trading/1173489.htm
37. Ceva 2026 annual meeting / auditor ratification (Kost Forer Gabbay & Kasierer, EY Israel); FY2025 10-K filed 2026-02-27 — https://www.stocktitan.net/sec-filings/CEVA/8-k-ceva-inc-reports-material-event-fd960b8f4947.html and https://www.ceva-ip.com/wp-content/uploads/Ceva_10-K_2025.pdf
38. Semiconductor sector regime — SOXQ +99% YTD, +58% 3-month; late-July semi weakness and leveraged bearish ETF gains — https://www.nerdwallet.com/investing/learn/best-semiconductor-stocks and https://www.etftrends.com/leveraged-inverse-content-hub/semiconductor-outlook-bodes-well-for-this-etf/
39. Global semiconductor sales Q2 2026 $403.3bn, +35.1% QoQ; SIA >$1.5tn 2026 — https://www.benzinga.com/markets/tech/26/08/61047954/whats-going-on-with-taiwan-semiconductor-stock-friday-4
40. Arm FY Q2 2026 — revenue $1.1bn +34%, licensing $515.0m +56%, royalty $620.0m +21% — https://futurumgroup.com/insights/arm-q2-fy-2026-earnings-highlight-ai-driven-royalty-momentum/
41. Rambus Q2 2026 — record revenue $207.4m, royalties $84.2m — https://www.investing.com/news/company-news/rambus-q2-2026-slides-record-revenue-tops-200m-on-ai-demand-93CH-4815211
42. Rambus Q2 royalty revenue +22% YoY — https://www.iam-media.com/article/rambus-q2-royalty-revenue-rises-22-yoy-amid-ai-boom
43. Nasdaq SOX research: "AI Tailwinds and Memory Shortages" — https://indexes.nasdaqomx.com/docs/202601%20Semiconductor%20Research%20-%20SOX.pdf

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such.*
