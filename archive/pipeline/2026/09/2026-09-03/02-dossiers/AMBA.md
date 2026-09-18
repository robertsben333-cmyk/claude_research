# AMBA — Ambarella, Inc.

**What this print is about.** Ambarella reports FQ2 2027 (quarter ended 31 July 2026) after the close on Thursday 3 September 2026. This is not a headline-EPS print. Ambarella has beaten its own guidance and Street EPS in essentially every recent quarter and the stock has still fallen on five of the last six reactions — including −21.4% on the last one. The print therefore trades on the **FQ3 2027 revenue and opex guide**, and specifically on whether the DRAM/NAND cost shock that management itself pre-flagged in May as a second-half risk to *its customers* has begun to show up in orders. Two things make this quarter unusually messy: (1) a one-time **$9.0M reduction of R&D expense** lands in the July quarter from a terminated customer development project, flattering FQ2 opex and creating a mechanical ~$9M step-up into FQ3; and (2) the **NXP takeover premium has completely deflated** — the stock at $67.14 is 9.4% *below* the $74.09 pre-rumour close of 30 July and 21.9% below the $86.00 post-rumour close of 31 July, so the market is currently ascribing roughly zero probability-weighted value to a deal. Options price ~12.6–12.9%; the eight-quarter mean absolute D+1 move is 15.1%. Triage called this "a beat-and-raise setup"; the evidence says the beat is close to certain and largely irrelevant, and I disagree that the setup is directionally favourable — see §11.

---

## 1. Event & anchors

| Item | Value | As of | Source |
|---|---|---|---|
| `event_confirmed` | **true** | — | Company press release [1][2] |
| Report date | **2026-09-03**, earnings release after market close | — | [1][2] |
| Session | **amc** | — | [1] |
| Call time | 1:30 p.m. Pacific / 20:30 UTC, 2026-09-03 | — | [1][2] |
| Fiscal period | FQ2 FY2027, quarter ended **2026-07-31** | — | [1][3] |
| Date changed / pre-announcement? | No. Date announced 2026-08-12 and unchanged. No 8-K filed since 2026-07-01; no pre-announcement, no guidance revision | 2026-09-03 | EDGAR filing index [4] |
| Spot | **$67.14** (close, −1.02% on the day) | 2026-09-02 20:00Z | Yahoo chart API [5]; stockanalysis [6] |
| Market cap | **$2.95B** (43,861,484 shares × $67.14 = $2.945B) | 2026-09-02 | [6]; share count from 10-Q [3] |
| Shares out / float | 43.87M / 41.86M | 2026-04-30 (10-Q) / 2026-09-03 (float) | [3][7] |
| Event implied move | **12.93%** (weekly, expiry 2026-09-04) · 16.23% (monthly, 2026-09-18) | 2026-09-03 | OptionSlam [8] |
| Alternate implied move | 12.64% expected move; "~14%" cited by Investing.com | ~2026-09-01/02 | Barchart preview [9] `snippet_only`; Investing.com via search [10] `snippet_only` |
| IV / IV rank / IV percentile | IV 73.81%, HV 74.68%, **IV rank 54.14**, IV percentile 59 | ~2026-09-02 | Barchart [11] `snippet_only` |
| IV 1-yr high / low | 106.28% (2026-07-29) / 35.47% (2025-09-11) | — | Barchart [11] `snippet_only` |
| 20d / 60d / 252d realised vol | 41.5% / 91.8% / 74.6% | 2026-09-02 | Computed from [5] |
| 50-DMA / 200-DMA / RSI(14) | $73.92 / $69.46 (my calc) · $74.02 / $69.37 / RSI 37.63 | 2026-09-02 / 2026-09-03 | Computed from [5]; [7] |
| 52-week range | $48.30–$96.69 (intraday) · $48.65–$95.51 (closing) | 2026-09-02 | [6]; computed from [5] |

### Realised one-day (D+1, close-to-close) earnings moves — eight quarters

Computed by me from Yahoo daily closes [5]; report dates independently confirmed from company releases [12][13][14][15][16][17][18][3].

| Quarter | Report date (AMC) | D+1 date | Pre close | D+1 close | **D+1 move** | 20-session run-in | % of 52wk high at print |
|---|---|---|---|---|---|---|---|
| Q1 FY27 | 2026-05-28 | 2026-05-29 | $91.84 | $72.18 | **−21.41%** | +39.3% | 96.2% |
| Q4 FY26 | 2026-02-26 | 2026-02-27 | $70.90 | $60.34 | **−14.89%** | +6.3% | 74.2% |
| Q3 FY26 | 2025-11-25 | 2025-11-26 | $90.97 | $73.89 | **−18.78%** | +5.4% | 95.2% |
| Q2 FY26 | 2025-08-28 | 2025-08-29 | $70.63 | $82.48 | **+16.78%** | +6.9% | 85.2% |
| Q1 FY26 | 2025-05-29 | 2025-05-30 | $62.00 | $52.64 | **−15.10%** | +29.2% | 74.8% |
| Q4 FY25 | 2025-02-26 | 2025-02-27 | $75.81 | $62.83 | **−17.12%** | +3.1% | 91.4% |
| Q3 FY25 | 2024-11-26 | 2024-11-27 | $68.41 | $72.44 | **+5.89%** | +11.2% | 100.0% |
| Q2 FY25 | 2024-08-27 | 2024-08-28 | $52.79 | $58.40 | **+10.63%** | +3.6% | 69.7% |
| **Q2 FY27 (this print)** | 2026-09-03 | 2026-09-04 | $67.14 | — | — | **−18.4%** | **70.3%** |

- **Mean |move| (8q): 15.08% · Median |move|: 15.94% · Max |move|: 21.41%**
- Mean |move| (last 6q): 17.35% · Median: 16.95%
- Up/down pattern, most recent first: **D, D, D, U, D, D, U, U** → 3 up / 5 down over 8; **1 up / 5 down over 6**
- Independent corroboration of the pattern: Barchart's preview states six of the past eight D+1 moves exceeded 10%, four exceeded 15%, the average D+1 move is 14.97%, and the stock exceeded the options-implied move in five of the past eight [9] `snippet_only`. TipRanks independently reports the last reaction as −21.41% [19], matching my computation exactly — a useful check on the whole series.
- **My inference:** the D+1 move of −20.2% quoted by Quiver for May 2026 [20] and −21.4% by Simply Wall St/TipRanks [19][21] are the same event; I use the computed −21.41%.

---

## 2. The bar

**Consensus (FQ2 FY27, quarter ended 2026-07-31)**

| Metric | Consensus | Source |
|---|---|---|
| Non-GAAP EPS | **$0.17** (vs $0.15 in FQ2 FY26) | TipRanks [19]; Simply Wall St [22] `snippet_only` |
| Revenue | **$109.91M** | Simply Wall St [22] `snippet_only` |
| Revenue (Zacks) | **$108.3M**, +13.4% y/y | Zacks via search [23] `snippet_only` |
| Analyst count | 14 (S&P Global, per stockanalysis) — other aggregators show 14–22; TipRanks shows only 3 "recent" | [6][24][19] |
| FY27 revenue consensus | $440.61M–$441.47M | Seeking Alpha [24] `snippet_only`; stockanalysis [6] |
| FY27 EPS consensus | $0.75–$0.79 | [24][6] |

**Company guidance given 2026-05-28 for FQ2 FY27** [3][25]:
- Revenue **$105.0M–$111.0M** (midpoint $108.0M, +13.1% y/y vs $95.5M)
- Non-GAAP gross margin **59.0%–60.5%**
- Non-GAAP opex **$56.0M–$59.0M**
- Sequential growth expected in **both** auto and IoT
- FY27 total revenue growth reaffirmed at **10%–15%** (midpoint ~12.5%) [26]

**Guidance vs Street.** The Street sits at or just above the guidance midpoint ($108.3M–$109.9M vs $108.0M). Backing out the guide mechanically: $108M × 59.75% GM = $64.5M gross profit − $57.5M opex = $7.0M non-GAAP operating income; + ~$2.0M other income − ~$0.8M tax ≈ $8.2M ÷ ~44.2M diluted ≈ **$0.185**. So the $0.17 consensus is *below* the arithmetic midpoint of company guidance — a low bar on the quarter itself. (This is my calculation from [3].)

**Revisions.** Over the last three months, EPS estimates saw **12 upward revisions and 0 downward**, revenue **12 up and 1 down** [24] `snippet_only`. Consensus price target has drifted up ~9.13% over three months [27] `snippet_only`. I could not source a clean 30/60/90-day estimate-change series — see coverage gaps.

**Whisper number.** `unavailable`. I found no credibly published whisper for AMBA FQ2 FY27. Rosenblatt (2026-08-31) says only that it expects "a beat-and-raise" [28]; it does not publish a figure in the accessible note.

**What the company has to deliver to hold the stock flat (my inference).** Given the guidance-implied ~$0.185 vs $0.17 consensus, a small beat on the reported quarter is near-automatic and is already discounted. To hold flat, Ambarella needs an FQ3 revenue guide with a midpoint at or above roughly **$118–122M** (my back-out from the $440.6M FY27 consensus less $100.4M actual Q1 and ~$110M Q2, allocated using FY26 seasonality) **and** an FQ3 non-GAAP opex guide that does not step up by the full $9.0M R&D credit, **and** management language that does not extend the DRAM/flash customer-demand caveat. Miss any one of those and the last four downside reactions are the template.

---

## 3. The one metric that matters

**The FQ3 FY2027 revenue guide, read against management's own May warning that customers face "much higher DRAM price and the flash price as well as potential shortage in the second half."** [29]

Why this and not EPS:
- Ambarella beat EPS in each of the last several quarters and the stock fell anyway four of five times [19][5]. Headline EPS carries no information here.
- Management explicitly located the risk in H2 FY27 — the quarter it is about to guide. Q1 non-GAAP GM guidance of 59.0–60.5% was described as stable "despite the DRAM pricing pressures mentioned for the second half of fiscal 2027" [29].
- The macro fact has not improved: conventional DRAM contract prices are projected up **13–18% q/q** in Q3 2026 and NAND up **10–15% q/q**, after DRAM/NAND surged 90–95% q/q in Q1 2026 [30]. Security-camera makers are publicly raising prices on DRAM shortage [31]. Ambarella's largest end customer is a consumer camera brand (below), the segment most exposed to BOM inflation.
- Ambarella has already responded operationally: inventory days went **99 → 145** in one quarter, explicitly "to support upcoming ramps and offset anticipated supply chain constraints," with Samsung having told them supply is tightening [29]. Inventory rose from $52.2M to $80.4M q/q (+53.8%) [3].

**Secondary metric that matters almost as much: the FQ3 non-GAAP opex guide.** The 10-Q discloses that on 2026-05-12 Ambarella terminated a customer development project, refunded $4.5M of a $13.5M deposit, and that "the remaining $9.0 million of the deposit is expected to be recognized as a **reduction of research and development expense in the second quarter ending July 31, 2026**" [3]. That $9.0M credit is worth roughly **$0.20 per diluted share**. It sits inside the July quarter only. **My inference (flagged as inference, and the single most uncertain judgement in this dossier):** because the guide was issued on 2026-05-28, after the 2026-05-12 termination, the $56–59M non-GAAP opex guide most likely already embeds the credit — meaning underlying opex is ~$65–68M and FQ3 opex will step up ~$9M q/q even before growth spending. If instead Ambarella excludes the credit from non-GAAP, FQ2 non-GAAP EPS is clean and there is no step-up. I could not resolve which, and it materially changes how the FQ3 EPS guide will read. This item appears in no sell-side commentary I could find, which is consistent with the thin-coverage thesis in triage.

**Third: any management language on strategic alternatives.** Rosenblatt explicitly expects management **not** to comment on the NXP talks or any strategic alternatives on the call [28]. If they do comment either way, that dominates the print.

---

## 4. Fundamentals — what changed, what is at stake

All figures below are from the FQ1 FY2027 Form 10-Q (period ended 2026-04-30, filed 2026-06-02) via SEC XBRL/EDGAR [3][32] unless noted.

**Income statement (FQ1 FY27, GAAP)**
- Revenue **$100.357M**, +16.9% y/y (from $85.872M)
- Cost of revenue $41.768M → gross profit **$58.589M**, GAAP GM **58.4%** (vs 60.0% y/y) [25]
- R&D **$58.140M** (−1.2% y/y); SG&A $19.865M (+6.9% y/y); total opex $78.005M
- **Operating loss −$19.416M**; net loss **−$18.093M** (−$0.41/sh GAAP)
- Non-GAAP net profit $5.0M, **non-GAAP EPS $0.11**; non-GAAP GM 59.9% (vs 62.0% y/y) [25]
- Stock-based comp **$21.893M = 21.8% of revenue** — the entire gap between GAAP and non-GAAP

**Cash flow and balance sheet**
- Operating cash flow **−$25.626M** in FQ1 FY27, vs **+$14.801M** in FQ1 FY26. A $40M y/y swing.
- Capex $3.957M → FCF ≈ **−$29.6M** for the quarter (my calculation)
- Cash & equivalents $114.443M + marketable debt securities $163.357M = **$277.8M**, no debt. Down $34.8M q/q, per management driven by the inventory build [33]
- Inventory **$80.355M** (from $52.246M q/q, $33.808M a year earlier) — inventory days 99 → 145 [29]
- Total assets $794.838M including **$303.625M goodwill**; total liabilities $189.020M; equity $605.818M
- Deferred revenue, current: $22.393M → **$17.036M** (−23.9% q/q)
- **Manufacturing purchase commitments: $80.4M (1/31/26) → $53.9M (4/30/26), −33% q/q** [3]. Read alongside a 54% inventory build, this is the pairing to watch: they took delivery and cut forward commitments.

**Buyback / dilution**
- FQ1 FY27 repurchases: 47,798 shares for **$2.441M**. New **$50.0M** programme authorised 2026-05-27, running 2026-07-01 → 2027-06-30 [3]
- Shares outstanding 43,305,592 (1/31/26) → **43,861,484** (4/30/26) = +1.28% in one quarter. The buyback ($50M ≈ 1.7% of cap over a year) does not offset SBC-driven dilution (~$88M annualised). **Net dilutive.**

**Mix and concentration**
- IoT ≈ **75%** of FQ1 revenue; automotive ≈ 25% and at an **all-time record**, with "very strong double digit" sequential growth [33]
- Edge AI ≈ **80%** of revenue in FY26, +~50% y/y [26][34]; cumulative >46M edge-AI SoCs shipped, 12 products in production [33]
- Distributor **WT Microelectronics = 61% of FQ1 FY27 revenue** (63% prior year). Top-10 end customers = **67%** of revenue [3]
- **Largest end customer FY27-to-date: Arashi Vision (Insta360)**, supplied indirectly through WT to multiple ODMs [3]
- Geography (bill-to, FQ1 FY27): Taiwan $60.98M, APAC ex-TW $23.25M, Europe **$6.31M (down from $8.74M y/y)**, North America ex-US $7.90M, US $1.92M [3]

**Growth drivers management is selling**
- **Hanwha long-term agreement** signed 2026-05-28: ">$800M potential revenue over a period exceeding 10 years," multi-generational co-development across video security, robotics, industrial automation, life sciences [35][36]
- **Robotics: 15+ design wins, >$100M lifetime revenue potential, 30+ customers** across drones and AMRs [33]
- **Edge infrastructure:** N1-655 SoC, first design win announced, first products expected H2 CY2026, "couple of hundred million dollar SAM" [33][37]
- 5nm Gen-3 SoCs ramping into higher volume, lifting ASPs; 4nm and 2nm in design [28]

**What changed since the last print (2026-05-28)**
1. Hanwha LTA announced same day (already in the price)
2. NXP takeover talks reported by the FT on 2026-07-31 [38][39]; stock +16.08% that day on 9.21M shares, then a full round-trip
3. Stock made a separate +28.04% single-day move on 2026-06-30 on Rosenblatt naming it a top H2 pick / "pure play on physical AI" [40] — also fully round-tripped
4. New $50M buyback commenced 2026-07-01 [3]
5. Multiple discretionary insider sales in June/July (see §8)
6. Sector: SOX fell 21% in July 2026, its worst month since October 2008, then recovered double digits in early August [41][42]

**What is at stake.** At $67.14 the enterprise value is ~$2.67B (my calc: $2.945B cap − $277.8M net cash) = **~6.1x FY27 consensus revenue of $440.6M**, for a business with a GAAP operating loss, SBC at 22% of revenue, negative FQ1 free cash flow, and 10–15% guided growth. That multiple only holds if the edge-AI/robotics/auto narrative keeps compounding. A guide that acknowledges memory-driven customer softness would force a growth-rate debate the multiple cannot absorb.

---

## 5. Positioning & options

| Metric | Value | As of | Source |
|---|---|---|---|
| Event implied move (weekly, 2026-09-04 expiry) | **12.93%** | 2026-09-03 | OptionSlam [8] |
| Implied move (monthly, 2026-09-18) | 16.23% | 2026-09-03 | [8] |
| Alternate expected move | 12.64% | ~2026-09-01 | Barchart preview [9] `snippet_only` |
| IV / HV | 73.81% / 74.68% | ~2026-09-02 | Barchart [11] `snippet_only` |
| IV rank / IV percentile | **54.14** / 59 | ~2026-09-02 | [11] `snippet_only` |
| Put/call **volume** ratio | 0.78 (30-day avg volume 4,413 contracts) | ~2026-09-02 | [11] `snippet_only` |
| Put/call **open interest** ratio | **0.56** (32,457 OI) | ~2026-09-02 | [11] `snippet_only` |
| Short interest | **4.07M shares = 9.72% of float** | 2026-09-03 | stockanalysis [7] |
| Days to cover | **2.22** | 2026-09-03 | [7] |
| Short interest (alt) | 9.28% | 2026-09-03 | OptionSlam [8] |
| Short interest (stale — do not use) | 2.38M / 6.57% / 2.34 days | ~Jan 2026 | Benzinga [43] |
| Borrow fee | **unavailable** | — | Fintel/Benzinga pages not reachable |
| Skew (put vs call IV by strike) | **unavailable** | — | — |
| Beta (5Y) | 2.08 | 2026-09-03 | [7] |
| 20-day avg volume | 972,665 shares | 2026-09-02 | Computed from [5] |

**Run-in / drawdown into the print** (computed from [5], as of 2026-09-02 close):

| Window | Change |
|---|---|
| 5 sessions (from 2026-08-26) | **−3.59%** |
| 10 sessions (from 2026-08-19) | **−9.99%** |
| From post-NXP-rumour peak close $86.00 (2026-07-31) | **−21.93%** |
| From pre-rumour close $74.09 (2026-07-30) | **−9.38%** |
| From last print's pre-close $91.84 (2026-05-28) | **−26.89%** |
| 3 months (from 2026-06-02) | −14.34% |
| 12 months (from 2025-09-03) | −15.36% |

**Reading of the positioning.**
- **The trade does not look crowded long. It looks abandoned.** The 20-session run-in of **−18.4%** is negative for the first time in the eight-quarter sample; every prior print was entered with a positive 20-day run (+3.1% to +39.3%). RSI 37.6, below both the 50-DMA ($73.92) and roughly at the 200-DMA ($69.46).
- **The M&A premium is gone and then some.** $67.14 is 9.4% below the pre-rumour $74.09. Whatever probability the market assigned to an NXP deal on 31 July, it now assigns approximately none — and has also marked down the standalone business. NXP's own stock fell >20% over the following month on the rumour plus a UBS downgrade citing Chinese auto inventory [44] `snippet_only`, which is a coherent reason for the deflation and my best explanation for the 17–24 August slide ($82.04 → $70.00, −14.7% in six sessions on rising volume [5]).
- **Short interest at 9.72% of float with 2.22 days to cover** is elevated for a $3B semi but not squeeze-critical; a beat plus a clean guide has fuel behind it.
- **Options are not maximally braced.** 12.6–12.9% implied against a 15.08% eight-quarter mean absolute realised move, with the stock having exceeded the implied move in five of the last eight [9]. IV rank of 54 is *middling*, not extreme, despite an event with a documented 15% average move. My inference: the straddle is, if anything, cheap relative to base rates.
- **Put/call OI of 0.56 is call-heavy**, consistent with residual takeover-lottery-ticket buying rather than downside hedging.
- **One forensic oddity:** Barchart records the trailing-year IV high of 106.28% on **2026-07-29** [11]. The stock then rose +7.08% on 1.51M shares on **7/30**, the session *before* the FT report on 7/31. Volatility and price both moved ahead of publication. I am not alleging anything; I note it as evidence that this name has leaked before.

---

## 6. Sentiment & alt-data

- **Analyst ratings.** Consensus "Buy." stockanalysis/S&P Global: 14 analysts, average PT **$95** (range $80–$120), implying 41.5% upside from $67.14 [6]. Breakdown 5 Strong Buy / 2 Buy / 7 Hold / 0 Sell [6]. ChartMill shows a median PT of $100 (range $80–$115) across 22 analysts, 9 Buy / 5 Hold / 0 Sell [24] `snippet_only`.
- **Price-target drift: upward.** Average PT +9.13% over three months [27] `snippet_only`. Recent named actions: **Rosenblatt reiterated Buy, $120 PT, on 2026-08-31**, explicitly expecting a beat-and-raise and citing 5nm Gen-3 ramping and 4nm/2nm performance-per-watt leadership [28]. **Stifel (Tore Svanberg) reiterated Buy, $106 PT, 2026-08-24** [6]. Rosenblatt raised $115 → $120 following the Q1 print [45].
- **The tell:** the average PT is $95–$100 and the stock is $67.14. That is a ~40% gap. Either the sell-side is far behind the tape, or the tape is wrong. Historically on this name the tape has led — the Street held ~$95–$100 PTs through the −21% May reaction too.
- **A downgrade did land after Q1**, "highlighting second-half 2026 demand risk," per Quiver [20] `snippet_only`. I could not identify the firm — see coverage gaps.
- **Zacks Rank: #3 (Hold)** currently, having been #2 (Buy) in March 2026 [46] `snippet_only`.
- **Retail/social.** Stocktwits sentiment flipped to "bullish" from "bearish" with "high" message volume around the +28%/+32% move on 2026-06-30, when AMBA was a top-10 trending ticker [40] `snippet_only`. I could **not** source a current 7/14/30-day social-sentiment trend line as of early September — this is a real gap and I am not going to guess at it. Treat retail tone as **unknown**, not bullish.
- **Institutional flow (Q2 2026 13Fs, filed mid-August).** Mixed and not decisive: State Street +586,269 shares (+29.7%); Handelsbanken Fonder −262,293 (−66.1% of its position); EverSource +362.2% [47][48] `snippet_only`.
- **Alt-data on the largest end customer (Insta360 / Arashi Vision) — the most useful proxy I found.** Arashi Q1 CY2026 sales CNY 2,481.23M vs CNY 1,355.03M a year earlier (+83%); TTM revenue $1.66B as of 2026-06-30; global 360-camera shipments +55% y/y to 500k units in Q1 CY2026 with Arashi holding >68% share [49][50] `snippet_only`. **But:** Caixin reported on 2026-08-14 that DJI and Arashi Vision are escalating a battle for the 360-camera market [49]. Strong volume growth at Ambarella's largest end customer is a genuine positive for the July quarter; intensifying price competition plus NAND inflation is a genuine negative for the guide.
- **Hiring.** ~22 open Ambarella roles on ZipRecruiter, skewed to algorithm/verification engineering for autonomous driving and edge AI [51] `snippet_only`. Directionally consistent with continued R&D investment; too coarse to be a signal.
- **Google Trends / web traffic / app ranks:** `unavailable` — not applicable or not sourceable for a fabless component supplier.

---

## 7. Forensics

Primary source: SEC EDGAR submissions index and individual filings, parsed directly [4][32].

**Form 4 activity — every filing since 2026-06-12, with the `aff10b5One` flag read from the XML:**

| Date | Insider | Title | Txn | Shares | Price | 10b5-1? | Shares after |
|---|---|---|---|---|---|---|---|
| 2026-07-09 | Chen Yun-Lung | VP, Business Dev. & Marketing | S | 5,958 | $78.66 | **No** | 60,557 |
| 2026-07-01 | Ju Chi-Hong | SVP, Systems & GM | S | 10,000 | $88.84 | **No** | 155,924 |
| 2026-07-01 | Wang Feng-Ming | CEO | S | 16,250 | $90.08 | Yes | 773,607 |
| 2026-06-26 | Paisley, Christopher B. | Director | S | 250 | $62.01 | Yes | 41,029 |
| 2026-06-17 | Young, John Alexander | CFO | S | 3,186 + 1,847 | $67.87 / $66.98 | Yes | 112,590 |
| 2026-06-17 | Lee, Chan W. | COO | S | 2,951 | $67.87 | **No** | 157,098 |
| 2026-06-17 | Ju Chi-Hong | SVP, Systems & GM | S | 2,017 | $67.87 | **No** | 165,924 |
| 2026-06-17 | Wang Feng-Ming | CEO | S | 6,204 | $67.87 | **No** | 799,857 |
| 2026-06-17 | Wang Feng-Ming | CEO | G (gift) | 10,000 | — | — | 789,857 |
| 2026-06-12 | Chen Yun-Lung | VP, Business Dev. & Marketing | S | 9,856 | $67.06 | **No** | 66,515 |

Also reported: the CEO sold 32,500 shares at $90.04–$92.05 on 2026-05-26 under a 10b5-1 plan adopted 2025-10-08 [52].

**Reading.**
- **Zero insider buying** anywhere in the window.
- The 2026-06-17 cluster at $67.87 across four officers on the same day has the signature of sell-to-cover on an RSU vest, and I would not read it as a view — but note it was filed as code S without the 10b5-1 flag.
- The two that do read as views: **Ju Chi-Hong sold 10,000 shares at $88.84 on 2026-07-01 with no 10b5-1 flag**, one session after the +28% Rosenblatt-driven pop and a month before the NXP leak; and **Chen Yun-Lung sold 5,958 at $78.66 on 2026-07-09**, also discretionary. Both sold into strength that has since fully reversed. Small in dollars (~$0.9M and ~$0.5M) but directionally unhelpful.
- **No Form 4 since 2026-07-10** — a ~7½ week gap consistent with a closed trading window into the print. Nothing anomalous.

**8-K cadence and content.** Only two 8-Ks since the February earnings 8-K, and both are routine:
- 2026-02-27 (event 2026-02-23): Item 5.02, Compensation Committee approval of the FY2027 Annual Bonus Plan [53]
- 2026-07-01 (event 2026-06-26): Items 5.02/5.07, 2026 Annual Meeting results and the amended 2021 Equity Incentive Plan [54]

**No 8-K has been filed in August 2026 at all.** That is the single cleanest fact about the NXP situation: **as of the market close before this print there is no merger agreement, no Item 1.01, no Item 8.01 acknowledgement, and no pre-announcement of results.** Other August filings are third-party 13Gs and an S-8 (2026-08-03) [4].

**Departures, auditor, restatement.** No Item 5.02 departures. No auditor change, no Item 4.02 non-reliance, no restatement, no material weakness disclosed. Filings are on a normal DFIN/Donnelley cadence.

**Filing-language / tone shifts worth flagging in the FQ1 FY27 10-Q** [3]:
- New/elevated supply-chain language: "constant changes in the macro-economic environment, including potential retaliatory tariffs and restrictions on exports to foreign locations due to the recent imposition of tariffs by the U.S. Government on imports."
- Customer-concentration risk language sharpened: "The loss of a significant customer, or substantial reduction in purchases by a significant customer, **could happen again** at any time and without notice."
- The subsequent-event note discloses a **terminated customer development project** (2026-05-12), a $4.5M refund of a $13.5M deposit, and the $9.0M R&D credit landing in the July quarter. A cancelled custom-silicon programme is a negative datapoint that has attracted essentially no commentary.
- Adverse purchase commitment loss liabilities of **$1.2M** recorded at 2026-04-30, where there were none material at 2026-01-31.

---

## 8. Macro & peer read-through

**Sector regime.** The SOX rallied 106% YTD into a late-June 2026 all-time high, then **fell 21% in July 2026 — its worst month since October 2008** — before recovering double digits in early August [41][42]. Chip stocks shed more than $1 trillion in the July selloff [55]. Characterised as "a repricing of expectations after an exceptionally strong rally" rather than AI-demand deterioration [41].

**The most recent sector catalyst was decisively positive — and AMBA did not participate.** Nvidia reported after the close on 2026-08-26, beat, and guided well above; NVDA rose **8.7%** on 2026-08-27, its largest daily gain since April 2025, with Broadcom +4.5%, Marvell +5.8%, Micron +4.5%, SMH +3.5% [56][57]. AMBA rose only **+2.14%** that day ($69.64 → $71.16) and then fell in each of the next three sessions to $67.14 [5]. **My inference: this is idiosyncratic distribution, not sector beta.** It is the single most bearish tape fact in this dossier.

**Peers who already reported.**
- **NXP (the putative acquirer), Q2 2026 reported ~2026-07-27:** revenue $3,496M +19.5% y/y; non-GAAP EPS $3.61; auto $1,938M +12.1% (+17% ex-divestitures); Q3 guide $3.65–3.85B (+15–21% y/y), non-GAAP GM 58.0–59.0% [58]. Beat, but **shares fell** on the print [59]. NXP subsequently fell >20% in a month on the Ambarella rumour, a UBS downgrade citing Chinese auto inventory, and sector weakness [44] `snippet_only`. **Read-through:** the automotive end market NXP describes is healthy and SDV-driven — supportive of Ambarella's record auto quarter — but NXP's own de-rating and the Chinese-auto-inventory flag are the mechanism by which the AMBA takeover premium evaporated.
- **Mobileye, Q2 2026 (2026-07-23):** revenue $508M, roughly flat y/y; adjusted operating income $155M, +46%; **raised** FY26 revenue guidance midpoint by $20M to $1.97–2.02B; new Cloud-Enhanced ADAS design win with Stellantis; closed a $591M acquisition of Mentee Robotics to push into physical AI/humanoids [60][61]. **Read-through:** ADAS design-win momentum is real, and the physical-AI/robotics narrative Ambarella sells is being validated and simultaneously contested by a better-capitalised competitor.

**Customer / supply-chain read-throughs.**
- **Memory is the binding constraint.** Q3 CY2026 conventional DRAM contract prices +13–18% q/q; NAND +10–15% q/q; NAND contract prices across categories up 33–38%; supply staying tight as makers shift capacity to server product [30]. Security-camera manufacturers are publicly raising prices citing DRAM shortage [31]. Ambarella's SoC is a small share of a camera BOM, but memory inflation compresses its customers' ability to buy.
- **Insta360/Arashi (largest end customer)** is growing very fast (+83% y/y Q1 CY26 sales) but now faces an escalating DJI assault on the 360-camera segment [49][50] `snippet_only`.

**Rate/FX/commodity sensitivity.** Ambarella is Cayman-domiciled, invoices in USD, with 61% of bill-to revenue in Taiwan and ~85% in Asia [3]. No debt, so no rate sensitivity on the liability side; ~$277.8M of cash/securities earning interest (other income $2.083M in FQ1). The company flags US–China trade tension and retaliatory tariffs as a named forward risk [3]. **Its real commodity exposure is memory pricing, indirectly, through customers.**

---

## 9. Bull case / bear case / base case

**Bull case (stock up 10%+).** Ambarella has beaten its guidance midpoint effectively every recent quarter, the Street sits at $0.17 against a guidance-implied ~$0.185, and Rosenblatt on 2026-08-31 publicly expects a beat-and-raise on 5nm Gen-3 volume ramps and rising ASPs [28]. Estimate revisions are 12-up/0-down over three months [24]. Positioning is the most washed out in the sample: the 20-session run-in is **−18.4%**, negative for the first time in eight quarters, RSI 37.6, and short interest is **9.72% of float at 2.22 days to cover** [7] — squeeze fuel. The last time AMBA entered a print beaten down near the bottom of its range (Q2 FY25, 69.7% of the 52-week high, −9.4% 60-day momentum) it rose **+10.63%**; the time before that with a modest run-in (Q2 FY26 at $70.63) it rose **+16.78%** [5]. Auto is at a record, the Hanwha LTA adds >$800M of visibility, robotics has 15+ design wins worth >$100M lifetime, and N1-655 edge-infrastructure products ship in H2 [33][35]. And there is a free option: the FT-reported NXP talks were never denied, no 8-K has ended them, and at $67.14 the stock trades **below** its pre-rumour price, so any confirmation is pure upside [38][4].

**Bear case (stock down 10%+).** The base rate is brutal and consistent: **five of the last six D+1 reactions were negative, averaging −17.4% in absolute terms, every one of them on a quarter where the company beat** [5][19]. The mechanism is always the same — the print is fine, the guide or the margin is not. This quarter has two specific loaded barrels. First, management itself pre-flagged that customers face "much higher DRAM price and the flash price as well as potential shortage in the second half" [29], and memory prices have kept climbing (DRAM +13–18% q/q in Q3 CY26) [30] — that lands squarely on the FQ3 guide, into a consumer-camera-heavy customer base (Insta360 is the largest end customer, WT is 61% of revenue) [3]. Second, the **$9.0M R&D credit** recognised in the July quarter [3] most likely flatters FQ2 opex and creates a ~$9M / ~$0.20-per-share step-up into FQ3 that few models capture. The operating data already lean the wrong way: operating cash flow −$25.6M vs +$14.8M a year ago, inventory days 99→145, manufacturing purchase commitments −33% q/q, deferred revenue −24% q/q, and a **cancelled customer development programme** [3][29]. Insiders sold discretionarily into July strength with zero buying [4]. And the tape has already voted: AMBA fell in three of the four sessions after Nvidia's blowout lifted the whole sector, and has given back 100%+ of the takeover pop [5].

**Base case (my read).** A modest revenue and EPS beat on the July quarter — probably $109–112M and $0.18–0.21 — is close to a formality, and will not be what the stock trades on. The move is decided in the FQ3 guide and in how management frames memory-driven customer behaviour. I lean modestly negative because the specific catalyst management pre-announced (memory-driven H2 customer pressure) has, on the external evidence, gotten worse rather than better, because the FQ3 opex step-up is a real and under-modelled risk, and because the base rate on this name says beats do not save the stock. I hold that lean **loosely**, for three honest reasons: the −18.4% run-in is unprecedented in the sample and most of the historical damage occurred from elevated entry prices; a 9.72% short base with 2.2 days to cover can invert a modest positive surprise into a large up move; and there is a live, unresolved takeover file with a floor under it. Expect a large move either way — 12.6–12.9% implied against a 15.08% eight-quarter mean absolute realised move, exceeded five of the last eight times [8][9].

---

## 10. What would flip the consensus view

The most credible reversal, stated concretely: **an FQ3 FY2027 revenue guide with a midpoint at or above ~$122M — roughly +13% sequential — combined with management explicitly de-risking the memory issue** ("we have secured supply / customers have absorbed the cost / no order pushouts observed"), **and** an FQ3 non-GAAP opex guide of $60M or below that shows the $9.0M credit was not carrying FQ2. That combination would (a) validate the 10–15% FY27 growth reaffirmation with the hardest quarter de-risked, (b) reframe the 145-day inventory build as pre-positioning for a ramp rather than a demand air-pocket, and (c) force a 9.7%-of-float short base to cover into a stock 30% off its 52-week high with a $95–100 Street target. Given the 12.9% implied move and the +16.78% precedent from the August 2025 print, that path is worth +15% to +20%, and it is the reason my conviction here is medium rather than high.

The second, non-fundamental reversal: **any confirmation of an NXP transaction, or of a competing bid.** The stock at $67.14 sits below its $74.09 pre-rumour level, so a deal at even a modest premium to the FT-implied ">$3B" is a 20%+ event with no earnings content at all. Rosenblatt expects management to say nothing [28]; if they say something, the print is irrelevant.

The reversal that would deepen my bearishness instead: management withdrawing or trimming the 10–15% FY27 growth frame.

---

## 11. Where I disagree with triage

Triage's rationale was: *"Options price a ~14% move into a beat-and-raise setup with a complex edge-AI/auto/security product mix that gets thinner sell-side coverage than mega-cap semis."*

- **The ~14% implied move is right in spirit, slightly high in fact.** The first expiry after the report (2026-09-04) prices **12.93%** [8]; a preview source puts the expected move at **12.64%** [9]. Both are *below* the eight-quarter mean absolute realised move of 15.08%. Triage under-stated the case: the interesting fact is not that the move is big, it is that the implied move is arguably **cheap** relative to base rates.
- **"Beat-and-raise setup" is the framing I most disagree with.** It is Rosenblatt's phrase [28] and it may well describe the *results*. It does not describe the *trade*. Ambarella beat on 26 Feb 2025, 29 May 2025, 25 Nov 2025, 26 Feb 2026 and 28 May 2026 and the stock fell 17.1%, 15.1%, 18.8%, 14.9% and 21.4% [5][19]. Treating "they will beat" as a bullish input on this specific name is the error the tape has punished five times in six quarters.
- **"Thinner sell-side coverage" is correct and is the most useful part of the hint.** Fourteen covering analysts [6], and the two most consequential facts I found — the $9.0M R&D credit landing in FQ2 with a step-up into FQ3, and the 33% q/q drop in manufacturing purchase commitments alongside a 54% inventory build — appear in the 10-Q and in no commentary I could locate.
- Triage did not know about the **NXP takeover file**, which is the largest single swing factor in the name and materially raises reversal risk in both directions.

---

## 12. Coverage gaps

| Gap | Why it matters |
|---|---|
| **Borrow fee / stock-loan rate** — Fintel and Benzinga short-interest pages unreachable | With 9.72% of float short, the cost of carry tells you whether the short base is conviction or hedge. Without it I cannot size the squeeze risk properly. |
| **Options skew (put vs call IV by strike) and full IV term structure** | I have IV level, IV rank, and P/C ratios but not the shape. Skew would tell me whether the 12.9% straddle is symmetric or whether downside is being bid — directly relevant given the base rate. |
| **FQ3 FY2027 consensus revenue** | This is the single most important number in the dossier and I could only *infer* ~$118–122M by backing it out of the $440.6M FY27 consensus. The bar for the guide is therefore approximate. Biggest gap by far. |
| Whether the **$9.0M R&D credit** is inside or outside non-GAAP opex | Determines whether FQ2 EPS quality is poor and whether FQ3 opex steps up ~$0.20/share. I flagged it as an unresolved inference; a transcript or model would settle it. |
| **Whisper number** | No credible published whisper found. |
| **Identity of the post-Q1 downgrading firm** | Quiver referenced a downgrade citing H2 demand risk [20] but named no firm; that thesis is the same one I am underwriting and I would like to see it. |
| **Current 7/14/30-day retail/social sentiment trend** | Only a June 2026 Stocktwits datapoint found. Retail tone into this print is genuinely unknown; I have deliberately not characterised it. |
| **Precise 30/60/90-day estimate revision magnitudes** | I have direction and count (12 up / 0 down over 3 months, snippet_only) but not the dollar drift. |
| **Google Trends / web-traffic / app-rank proxies** | Not meaningful for a fabless component supplier; noted for completeness. |
| Barchart's "4-DTE expected move 3.53 (5.04%)" [11] conflicts with the 12.6–12.9% event move | Almost certainly a stale or non-event cached field. I have used OptionSlam's 12.93% and flagged the conflict rather than reconciling it silently. |
| **Marketchameleon and several finance domains blocked** (403 / access-denied / 503) | Forced reliance on search snippets for some options and revision data. I computed all historical moves myself from raw OHLC to avoid this dependence. |

**Domains I could not reach:** marketchameleon.com (access denied), investor.ambarella.com static-files and news-release pages (503 / HTTP2 stream error), barchart.com story and volatility pages via WebFetch (empty body — search snippet used), stooq.com (JS challenge). `data.sec.gov`, `www.sec.gov` and the Yahoo chart API were all reachable via curl and carry most of the load in this dossier.

---

## 13. Sources

1. Ambarella IR — "Ambarella Announces Second Quarter Fiscal Year 2027 Earnings Conference Call to be Held September 3, 2026" — https://investor.ambarella.com/news-releases/news-release-details/ambarella-announces-second-quarter-fiscal-year-2027-earnings — event date, AMC session, 1:30pm PT call time
2. GlobeNewswire, 2026-08-12, same release — https://www.globenewswire.com/news-release/2026/08/12/3343332/23306/en/ambarella-announces-second-quarter-fiscal-year-2027-earnings-conference-call-to-be-held-september-3-2026.html — independent confirmation of the event
3. SEC EDGAR — Ambarella Form 10-Q, period ended 2026-04-30, filed 2026-06-02 — https://www.sec.gov/Archives/edgar/data/1280263/000119312526253198/amba-20260430.htm — balance sheet, cash flow, inventory, WT 61% concentration, Arashi Vision as largest end customer, geographic revenue, $50M buyback, $9.0M R&D credit subsequent event, purchase commitments, risk language
4. SEC EDGAR — Ambarella submissions index (CIK 0001280263) — https://data.sec.gov/submissions/CIK0001280263.json — filing cadence, Form 4 list, absence of any August 8-K
5. Yahoo Finance chart API, AMBA 5-year daily OHLC — https://query1.finance.yahoo.com/v8/finance/chart/AMBA?range=5y&interval=1d — spot $67.14 at 2026-09-02 20:00Z, all computed earnings-day moves, run-in, realised vol, moving averages
6. stockanalysis.com — AMBA overview and forecast — https://stockanalysis.com/stocks/amba/ and https://stockanalysis.com/stocks/amba/forecast/ — spot, market cap, shares, 52-week range, 14 analysts, $95 average PT, rating breakdown, Stifel $106
7. stockanalysis.com — AMBA statistics — https://stockanalysis.com/stocks/amba/statistics/ — short interest 4.07M / 9.72% of float / 2.22 days to cover, float, beta 2.08, RSI, 50/200-DMA
8. OptionSlam — AMBA earnings — https://www.optionslam.com/earnings/stocks/AMBA — weekly implied move 12.93% (2026-09-04 expiry), monthly 16.23%, short interest 9.28%, EVR 7.1
9. Barchart — "Ambarella's AI Edge Vision Story Needs More Than Design Wins This Quarter" — https://www.barchart.com/story/news/2161673/ambarella-s-ai-edge-vision-story-needs-more-than-design-wins-this-quarter — expected move 12.64%, average D+1 move 14.97%, exceeded implied in 5 of 8, 6 of 8 moves >10% (`snippet_only`)
10. Investing.com AMBA equity page — https://www.investing.com/equities/ambarella-inc — "~14%" implied move (`snippet_only`)
11. Barchart — AMBA volatility & greeks — https://www.barchart.com/stocks/quotes/AMBA/volatility-greeks — IV 73.81%, HV 74.68%, IV rank 54.14, IV percentile 59, IV high 106.28% on 2026-07-29, P/C volume 0.78, P/C OI 0.56 (`snippet_only`)
12. GlobeNewswire — Ambarella Q1 FY2027 results, 2026-05-28 — https://www.globenewswire.com/news-release/2026/05/28/3303255/23306/en/ambarella-inc-announces-first-quarter-fiscal-year-2027-financial-results.html — report date confirmation
13. GlobeNewswire — Ambarella Q4/FY2026 results, 2026-02-26 — https://www.globenewswire.com/news-release/2026/02/26/3246085/23306/en/ambarella-inc-announces-fourth-quarter-and-fiscal-year-2026-financial-results.html — report date; Q4 revenue $100.9M
14. Motley Fool — Ambarella Q3 FY2026 earnings call transcript, 2025-11-25 — https://www.fool.com/earnings/call-transcripts/2025/11/25/ambarella-amba-q3-2026-earnings-call-transcript/ — report date confirmation
15. GlobeNewswire — Ambarella Q2 FY2026 results, 2025-08-28 — https://www.globenewswire.com/news-release/2025/08/28/3141112/23306/en/Ambarella-Inc-Announces-Second-Quarter-Fiscal-Year-2026-Financial-Results.html — report date; Q2 FY26 revenue $95.5M
16. GlobeNewswire — Ambarella Q1 FY2026 results, 2025-05-29 — https://www.globenewswire.com/news-release/2025/05/29/3090699/23306/en/Ambarella-Inc-Announces-First-Quarter-Fiscal-Year-2026-Financial-Results.html — report date
17. GlobeNewswire — Ambarella Q4/FY2025 results, 2025-02-26 — https://www.globenewswire.com/news-release/2025/02/26/3033351/23306/en/Ambarella-Inc-Announces-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results.html — report date; Q4 FY25 revenue $84.0M
18. GlobeNewswire — Ambarella Q3 FY2025 results, 2024-11-26 — https://www.globenewswire.com/news-release/2024/11/26/2987813/23306/en/Ambarella-Inc-Announces-Third-Quarter-Fiscal-Year-2025-Financial-Results.html — report date
19. TipRanks — AMBA earnings — https://www.tipranks.com/stocks/amba/earnings — FQ2 FY27 EPS consensus $0.17, prior-year $0.15, Q1 FY27 actual $0.11 vs $0.10, −21.41% D+1 reaction (independent match to my computation)
20. Quiver Quantitative — "Ambarella slides as investors digest cautious outlook and fresh downgrade after Q1 results" — https://www.quiverquant.com/news/Ambarella+slides+as+investors+digest+cautious+outlook+and+fresh+downgrade+after+Q1+results — unnamed downgrade citing H2 demand risk; memory/supply commentary (`snippet_only`)
21. TIKR — "Ambarella Fell 21% Today" — https://www.tikr.com/blog/ambarella-fell-21-today-heres-how-much-the-stock-could-rise-in-2026 — May 2026 reaction context, prior proximity to 52-week high
22. Simply Wall St — AMBA future/forecast — https://simplywall.st/stocks/us/semiconductors/nasdaq-amba/ambarella/future — next-quarter consensus EPS $0.17 and revenue $109.91M (`snippet_only`)
23. Zacks via search — Q2 FY27 revenue consensus $108.3M (+13.4% y/y), non-GAAP EPS consensus $0.17 — https://finance.yahoo.com/markets/stocks/articles/ambarellas-q1-earnings-meet-estimates-140700679.html (`snippet_only`)
24. ChartMill — AMBA analyst ratings — https://www.chartmill.com/stock/quote/AMBA/analyst-ratings — 22-analyst median PT $100, range $80–$115, 9 Buy / 5 Hold / 0 Sell (`snippet_only`); Seeking Alpha estimates page — https://seekingalpha.com/symbol/AMBA/earnings/estimates — FY27 consensus EPS $0.75 / revenue $440.61M, 12 up / 0 down EPS revisions in 3 months (`snippet_only`)
25. Ambarella IR — Q1 FY2027 financial results release — https://investor.ambarella.com/news-releases/news-release-details/ambarella-inc-announces-first-quarter-fiscal-year-2027-financial — Q1 revenue $100.4M, GAAP GM 58.4%, non-GAAP GM 59.9%, non-GAAP EPS $0.11, full Q2 guidance
26. Seeking Alpha — "Ambarella targets 10%-15% revenue growth in fiscal 2027 as edge AI adoption accelerates" — https://seekingalpha.com/news/4558382-ambarella-targets-10-percentminus-15-percent-revenue-growth-in-fiscal-2027-as-edge-ai — FY27 growth frame, edge AI ~80% of revenue
27. tickernerd — AMBA forecast — https://tickernerd.com/stock/amba-forecast/ — average PT revised up 9.13% over 3 months (`snippet_only`)
28. Investing.com — "Rosenblatt reiterates Buy rating on Ambarella stock ahead of earnings", 2026-08-31 — https://www.investing.com/news/analyst-ratings/rosenblatt-reiterates-buy-rating-on-ambarella-stock-ahead-of-earnings-93CH-4882601 — Buy, $120 PT, explicit beat-and-raise expectation, 5nm Gen-3 ramp, expectation that management will not comment on strategic alternatives
29. Investing.com — Ambarella Q1 FY2027 earnings call transcript — https://www.investing.com/news/transcripts/earnings-call-transcript-ambarella-q1-2027-beats-eps-expectations-but-stock-dips-93CH-4715652 — DRAM/flash customer pressure quote, inventory days 99→145, Samsung supply tightening
30. Tom's Hardware — memory price outlook — https://www.tomshardware.com/pc-components/ram/memory-price-surge-begins-to-cool-as-consumers-hit-affordability-limit-ai-demand-still-keeps-dram-and-nand-prices-climbing-through-q3-2026 — Q3 2026 DRAM contract +13–18% q/q, NAND +10–15% q/q; wccftech — https://wccftech.com/memory-nand-prices-surged-90-percent-in-q1-2026/ — Q1 2026 +90–95% q/q
31. Bokysee — "Security Camera Price Increase 2026: DRAM Shortage and AI Demand" — https://bokysee.com/security-camera-price-increase-dram-shortage-and-ai-demand-driving-global-cost-surge/ — downstream camera-OEM cost pass-through (trade source, supporting colour only)
32. SEC XBRL company facts, CIK 0001280263 — https://data.sec.gov/api/xbrl/companyfacts/CIK0001280263.json — revenue, gross profit, R&D, operating loss, net loss, cash, inventory, operating cash flow, SBC, shares outstanding, buyback, equity, liabilities across quarters
33. Motley Fool — Ambarella Q1 FY2027 earnings call transcript, 2026-05-28 — https://www.fool.com/earnings/call-transcripts/2026/05/28/ambarella-amba-q1-2027-earnings-transcript/ — IoT ~75% of revenue, record auto, 46M cumulative edge-AI SoCs, 15+ robotics design wins >$100M lifetime, edge infrastructure SAM, cash/marketable securities $278M, inventory rationale
34. Nasdaq — "Ambarella Q3 Earnings Beat Estimates, Revenues Jump More Than 31% Y/Y" — https://www.nasdaq.com/articles/ambarella-q3-earnings-beat-estimates-revenues-jump-more-31-y-y — Q3 FY26 revenue $108.5M vs $104.07M consensus, EPS $0.27 vs $0.21, edge AI ~80% of revenue
35. Ambarella IR — "Hanwha and Ambarella Enter Into Long-Term Edge AI Agreement" — https://investor.ambarella.com/news-releases/news-release-details/hanwha-and-ambarella-enter-long-term-edge-ai-agreement — >$800M over 10+ years, scope
36. Seeking Alpha — "Ambarella outlines $105M-$111M Q2 revenue while Hanwha agreement targets $800M+ over 10+ years" — https://seekingalpha.com/news/4598204-ambarella-outlines-105m-111m-q2-revenue-while-hanwha-agreement-targets-800m-over-10-plus — guidance and Hanwha in one place
37. SEC EDGAR — Ambarella Form 10-K FY2026, filed 2026-03-23 — https://www.sec.gov/Archives/edgar/data/1280263/000119312526119321/amba-20260131.htm — N1/N1-655 product positioning, FY26 revenue $390.7M
38. Yahoo Finance — "Ambarella reportedly in talks to be acquired by NXP Semiconductors, shares spike" — https://finance.yahoo.com/markets/stocks/articles/ambarella-reportedly-talks-acquired-nxp-173701702.html — FT report 2026-07-31, deal potentially >$3B, talks not certain
39. SiliconANGLE, 2026-07-31 — https://siliconangle.com/2026/07/31/nxp-reportedly-talks-acquire-vehicle-chip-supplier-ambarella/ — independent confirmation of the FT report and its date
40. Yahoo Finance / Stocktwits — "AMBA Stock Rockets 32% — Why Rosenblatt Sees Ambarella As A Pure Play On Physical AI" — https://finance.yahoo.com/technology/ai/articles/amba-stock-rockets-32-why-190927059.html — the 2026-06-30 move (+28.04% close-to-close per [5]); Stocktwits sentiment flip to bullish (`snippet_only`)
41. TradingView / Leverage Shares — "The 2026 Semiconductor Selloff Creates an Opportunity" — https://www.tradingview.com/news/leverage_shares:c8d519c05094b:0-the-2026-semiconductor-selloff-creates-an-opportunity/ — SOX +106% YTD into late-June high, −21% in July 2026 (worst month since Oct 2008), double-digit August recovery
42. Fortune — "Wall Street's favorite bet comes undone as chips whipsaw market" — https://fortune.com/2026/08/02/wall-street-ai-trade-chip-stocks-volatility-sox-selloff/ — July 2026 SOX drawdown context
43. Benzinga — AMBA short interest — https://www.benzinga.com/quote/AMBA/short-interest — 2.38M shares / 6.57% of float / 2.34 days to cover (stale, ~Jan 2026; cited only to document the trend into today's 4.07M)
44. Pluang — "NXP stock drops 20% amid Ambarella rumors and UBS downgrade" — https://pluang.com/en/news-feed/argumen-kuat-untuk-keuntungan-70-persen-pada-nxp-semikonduktor — NXP −20% in a month on the Ambarella rumour, UBS downgrade on Chinese auto inventory (`snippet_only`, low-tier source, used only for the deflation mechanism)
45. Rosenblatt press mentions — "Ambarella price target raised to $120 from $115" — https://www.rblt.com/news/ambarella-price-target-raised-to-120-from-115-at-rosenblatt — PT history
46. TradingView / Zacks — "Do Options Traders Know Something About Ambarella Stock We Don't?" — https://www.tradingview.com/news/zacks:a1598f13f094b:0-do-options-traders-know-something-about-ambarella-stock-we-don-t/ — Zacks Rank #3 (Hold) currently, #2 in March 2026 (`snippet_only`)
47. MarketBeat — Handelsbanken Fonder AB sells 262,293 shares of AMBA, filed 2026-08-14 — https://www.marketbeat.com/instant-alerts/filing-handelsbanken-fonder-ab-sells-262293-shares-of-ambarella-inc-amba-2026-08-14/ — Q2 2026 13F position cut of 66.1% (`snippet_only`)
48. HedgeFollow — AMBA 13F institutional ownership — https://hedgefollow.com/stocks/AMBA — State Street +586,269 shares (+29.7%) in Q2 2026 (`snippet_only`)
49. Caixin Global, 2026-08-14 — "China's DJI and Arashi Vision Escalate Battle for 360-Camera Market" — https://www.caixinglobal.com/2026-08-14/chinas-dji-and-arashi-vision-escalate-battle-for-360-camera-market-102474326.html — competitive pressure on Ambarella's largest end customer (`snippet_only`)
50. PitchBook — Arashi Vision company profile — https://pitchbook.com/profiles/company/139895-38 — Q1 CY2026 sales CNY 2,481.23M vs CNY 1,355.03M; TTM revenue $1.66B as of 2026-06-30; >68% 360-camera share (`snippet_only`)
51. ZipRecruiter — Ambarella job listings — https://www.ziprecruiter.com/co/Ambarella/Jobs — ~22 open roles, engineering-weighted (`snippet_only`)
52. StockTitan — Ambarella Form 4 filings — https://www.stocktitan.net/sec-filings/AMBA/form-4-ambarella-inc-insider-trading-activity-837a18a1600c.html and .../c81ff69e0ee5.html and .../727ecb1de8f2.html — CEO 32,500-share sale 2026-05-26 at $90.04–$92.05 under a 10b5-1 plan adopted 2025-10-08; corroborates the EDGAR-parsed table
53. SEC EDGAR — Ambarella Form 8-K filed 2026-02-27 (event 2026-02-23) — https://www.sec.gov/Archives/edgar/data/1280263/000119312526083175/d116451d8k.htm — Item 5.02, FY2027 Annual Bonus Plan (routine)
54. SEC EDGAR — Ambarella Form 8-K filed 2026-07-01 (event 2026-06-26) — https://www.sec.gov/Archives/edgar/data/1280263/000119312526292824/d139114d8k.htm — Items 5.02/5.07, annual meeting results, amended 2021 Equity Incentive Plan (routine)
55. CNBC, 2026-07-29 — "Chip stocks shed more than $1 trillion as selloff hits companies powering AI boom" — https://www.cnbc.com/2026/07/29/chip-selloff-sk-hynix-samsung-softbank.html — July 2026 sector drawdown magnitude
56. CNBC market wrap, 2026-08-27 — https://www.cnbc.com/2026/08/26/stock-market-today-live-updates.html — Nvidia +8.7% post-earnings, Broadcom +4.5%, sector rally
57. Kiplinger — Nvidia earnings live coverage, August 2026 — https://www.kiplinger.com/investing/live/nvidia-earnings-live-updates-and-commentary-august-2026 — NVDA beat and guide, sector read-through
58. Investing.com — "NXP Q2 2026 slides: record results, ambitious 2030 targets" — https://www.investing.com/news/company-news/nxp-q2-2026-slides-record-results-ambitious-2030-targets-93CH-4818254 — NXP Q2 revenue $3,496M, auto $1,938M, Q3 guide $3.65–3.85B
59. Investing.com — "NXP Semiconductors tops Q2 2026 estimates, shares fall" — https://www.investing.com/news/transcripts/earnings-call-transcript-nxp-semiconductors-tops-q2-2026-estimates-shares-fall-93CH-4818239 — beat-but-fell precedent in the same end market
60. Mobileye IR — Q2 2026 results — https://ir.mobileye.com/news-releases/news-release-details/mobileye-releases-second-quarter-2026-results-updates-guidance — revenue $508M, adjusted operating income $155M, raised FY26 guidance
61. Automotive World — "Mobileye reports Q2 2026 robotaxi and ADAS momentum" — https://www.automotiveworld.com/news/mobileye-reports-q2-2026-robotaxi-and-adas-momentum/ — Stellantis Cloud-Enhanced ADAS win, Mentee Robotics acquisition ($591M)

---

*This is research, not investment advice. It is a forecasting exercise over public information and must not be presented or relied upon as investment advice.*
