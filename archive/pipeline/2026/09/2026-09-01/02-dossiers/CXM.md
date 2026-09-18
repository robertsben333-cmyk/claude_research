# CXM — Sprinklr, Inc.

**Event confirmed: YES.** Q2 FY2027 (quarter ended 31 July 2026), released **before market open Wednesday 2 September 2026**, call at 8:30am ET. Confirmed by the company's own dated release ("Sprinklr Announces Date of Second Quarter Financial Results", 12 Aug 2026) [S1][S2]. No date change and no pre-announcement found.

**What this print is about.** Sprinklr guided its own Q2 to roughly **+1% total revenue growth and a year-over-year decline in EPS and margin** ($214–215M vs $212.0M LY; ~$0.10 vs $0.13 LY; ~14% non-GAAP operating margin vs 18% LY) [S3][S4]. Into that, the stock has run **+49% off its 23 July low and +29% in one month** to $8.21, above the sell-side average price target, with a 14-day RSI of 81 [S5][S6][S7]. Almost none of that move is Sprinklr-specific: over the identical window IGV is +26%, FRSH +42%, FIVN +59% and CRM +64% — an application-software AI re-rating triggered by Salesforce's 26 August blowout [own calculation from S8; S9]. So the question is not whether Sprinklr beats a $0.104 consensus — it has beaten in each of the last four-plus quarters — but whether a company guiding to ~1% revenue growth can produce enough forward evidence (FY27 subscription and operating-income guidance, cRPO, AI-native ARR) to justify a multiple that has just been marked up 50% on someone else's numbers. Sprinklr also retired its longest-running demand disclosure (the $1M+ customer count) at the last print, after it fell from 149 to 141 — which is directly relevant to the triage thesis and is discussed in §4.

---

## 1. Event & anchors

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Event date | 2026-09-02 | — | [S1][S2] |
| Session | **bmo** (release before open; call 8:30am ET) | — | [S1][S2] |
| Fiscal period | Q2 FY2027, quarter ended 2026-07-31 | — | [S3] |
| Date announced | 2026-08-12 (3 weeks' notice, same cadence as prior years) | — | [S2] |
| Spot | **$8.21** (+0.61%) | 2026-08-31 16:00 ET close | [S5], cross-checked [S8] |
| Prior close (Fri 28 Aug) | $8.16 (+2.77%) — `snippet_only`; Yahoo's daily series is missing the 28 Aug bar | 2026-08-28 | [S10] |
| Market cap | **$1.92B** | 2026-08-31 | [S5] |
| Enterprise value | $1.52B | 2026-08-31 | [S6] |
| Shares outstanding (A+B) | 234.23M | 2026-08-31 | [S6] |
| Float | 115.14M | 2026-08-31 | [S6] |
| 52-week range | $4.72 – $8.69 | 2026-08-31 | [S5][S8] |
| Event-implied move | **unavailable** — see below | — | — |
| IV rank / percentile | **unavailable** | — | — |
| 20-day realised vol (annualised) | 38.2% (my calculation from Yahoo daily closes) | 2026-08-31 | own calc from [S8] |
| 6-month realised vol (annualised) | 42.6% (my calculation) | 2026-08-31 | own calc from [S8] |
| 20-day avg volume | 2.85M sh (60-day: 3.31M) | 2026-08-31 | own calc from [S8] |
| RSI(14) | 81.15 | ~2026-08-31/09-01 | [S7] |
| Beta | 0.61 (5Y) / 0.58 | 2026-08-31 | [S6][S11] |

### Why there is no implied move

**CXM's listed options are effectively non-functional and I could not source a published implied move for this event.** Pulling the full Yahoo chain on 31 Aug: there are **no weekly expiries** — the first expiry after the print is **18 September 2026, 17 days out** — strikes are $2.50 apart (5.0 / 7.5 / 10.0), Yahoo reports **zero open interest on every line**, and total daily contract volume across the front expiry was ~200 contracts. Bids/asks were all zero in the post-close snapshot. There is therefore no ATM straddle to read and no usable options positioning signal [own pull, Yahoo options API].

Two weak, clearly-labelled reference points instead of an implied move:
- **My inference, low confidence:** last-trade marks on the 18 Sep chain back-solve to implied vols of ~52% (7.5 put), ~75% (7.5 call) and ~77% (10 call). At 70% IV a 17-day ATM straddle is ~12% of spot — but these are stale last-trade prints on zero-OI lines and should not be treated as a market-clearing implied move.
- **Historical, from a data provider, but stale:** Market Chameleon's figure quoted on 2 June 2026 was an expected move of **13.71%** through the 18 June expiry against an **average Day-0 move of 5.98%** [S12]. That is the *June* event, not this one.

### Realised one-day earnings reactions (eight quarters)

Reaction day = the session in which the report was digested, derived from the 8-K Item 2.02 filing date cross-referenced with the price gap. **Sprinklr switched from AMC to BMO reporting between December 2024 and March 2025** — the two 2024 events below are AMC (reaction next day), the six since are BMO (reaction same day) [S13][S14][S15].

| Fiscal Q | Release | Session | Reaction day | Gap % | Close-to-close % |
| --- | --- | --- | --- | --- | --- |
| Q2 FY25 | 2024-09-04 | amc | 2024-09-05 | −3.73% | **−9.31%** |
| Q3 FY25 | 2024-12-04 | amc | 2024-12-05 | +2.89% | **+0.35%** |
| Q4 FY25 | 2025-03-12 | bmo | 2025-03-12 | +10.52% | **+16.58%** |
| Q1 FY26 | 2025-06-04 | bmo | 2025-06-04 | +5.26% | **+5.96%** |
| Q2 FY26 | 2025-09-03 | bmo | 2025-09-03 | −4.65% | **−10.00%** |
| Q3 FY26 | 2025-12-03 | bmo | 2025-12-03 | +3.98% | **+3.05%** |
| Q4 FY26 | 2026-03-11 | bmo | 2026-03-11 | +4.98% | **+6.05%** |
| Q1 FY27 | 2026-06-03 | bmo | 2026-06-03 | −8.36% | **−3.02%** |

All prices from Yahoo daily OHLCV [S8]; 8-K dates from EDGAR [S13][S14]; the Dec-2024 AMC attribution is confirmed by the release itself [S15].

- **Last 8:** mean |move| **6.79%**, median |move| **6.01%**, max **16.58%**; 5 up / 3 down.
- **Last 6 (all BMO):** mean |move| **7.44%**, median |move| **6.01%**, max **16.58%**; 4 up / 2 down.
- **Pattern worth flagging:** both prior *September* (fiscal Q2) prints fell hard — −9.31% and −10.00%. n=2, so treat as colour, not evidence.
- **Secondary pattern:** the two down-gap BMO prints behaved differently. Sept-2025 gapped −4.65% and *kept selling* to −10.0%. June-2026 gapped −8.36% and was *bought back* to −3.0%. Dip-buying was present as recently as the last print.

---

## 2. The bar

**Consensus for Q2 FY27 (quarter ended 31 July 2026):**

| Metric | Consensus | Company guidance (given 3 Jun 2026) | Q2 FY26 actual |
| --- | --- | --- | --- |
| Non-GAAP EPS | **$0.104** [S16][S17] | ~$0.10 [S3] | $0.13 [S4] |
| Total revenue | **$214.449M** [S16][S17] | $214.0–215.0M [S3] | $212.04M [S4] |
| Subscription revenue | not sourced | $193.5–194.5M [S3] | $188.5M [S4] |
| Non-GAAP operating income | not sourced | $29.5–30.5M [S3] | $38.2M (18% margin) [S4] |

**What that arithmetic means.** Consensus revenue sits at the *midpoint* of guidance. The guide implies **+0.9% to +1.4% total revenue growth** and **+2.7% to +3.2% subscription growth** year over year, with non-GAAP operating income **down ~22% YoY** and margin compressing from 18% to ~14%. Subscription revenue is guided *below* the $194.8M printed in Q1 FY27 — i.e. a **sequential decline in subscription revenue**, which for a SaaS business is a poor optic regardless of the explanation.

**Analyst count:** 8–9 covering (stockanalysis.com: 9; MarketBeat-sourced: 8) [S18][S19]. Consensus rating **Hold**; distribution 2 Strong Buy / 1 Buy / 5 Hold / 1 Sell [S18] or 2 Buy / 4 Hold / 2 Sell [S19].

**Price targets — the stock has outrun the sell side.** Average PT **$7.88** [S18] / **$7.786** [S19] versus a spot of $8.21. Range $6.00–$12.00 [S18]. CXM currently trades **~5% above the consensus target**.

**Revisions.** I could not source a clean 30/60/90-day revision table.
- As of **25 June 2026**: over the trailing 60 days, *no* analysts raised current-quarter estimates and *two* revised down, taking the consensus from $0.13 to $0.11 [S20]. `snippet_only`.
- As of **early June 2026**: EPS estimates down 2.5% over 60 days but "recently stabilised" [S21]. `snippet_only`.
- FY27 consensus is now **$867.44M revenue (+1.20%) and $0.49 EPS** — precisely inside the company's $866.5–868.5M / $0.48–0.49 guide, i.e. the Street is modelling guidance and nothing more [S18][S3].
- Directionally this is a **negative-to-flat revision regime**: estimates were cut into the June print and have not been rebuilt.

**Prior guidance versus Street, and the FY27 setup — this is the important part.**

| FY27 guidance item | Initial (11 Mar 2026) | Revised (3 Jun 2026) | Change |
| --- | --- | --- | --- |
| Subscription revenue | $778–780M | $779.5–781.5M | **+$1.5M** |
| Total revenue | $869–871M | $866.5–868.5M | **−$2.5M** |
| Non-GAAP operating income | $144–146M | $139–141M | **−$5.0M** |
| Non-GAAP EPS | $0.47–0.48 | $0.48–0.49 | **+$0.01** |

[S22][S3]. Management cut the operating-income line by $5M at the last print and the stock gapped −8.4%. Against FY26 actuals (total $857.2M, subscription $756.3M, non-GAAP op income $146.2M, FCF $141.9M) [S22], FY27 guidance is **+1.2% total revenue, +3.2% subscription, and operating income down ~4% YoY**. FY27 FCF is guided at ~$150M [S23].

**Implied H2 (my calculation):** Q1 subscription $194.8M + Q2 guide midpoint $194.0M = $388.8M. FY guide midpoint $780.5M ⇒ **H2 subscription ≈ $391.7M**, versus H2 FY26 subscription of $383.7M (= $756.3M − $184.1M − $188.5M) ⇒ **+2.1% YoY**. So the guide is not demanding in absolute terms, but it does require Q3 and Q4 to step back up from a Q2 that steps *down*, and management has explicitly staked its case on "sequential subscription revenue buildup beginning Q3" [S24].

**What is needed to hold the stock flat (my inference).** A $0.01–0.02 EPS beat with revenue at the top of the range and FY27 guidance merely *reaffirmed* is, on this run-up, a fade. To hold flat I think Sprinklr needs (a) FY27 subscription revenue raised, not reiterated, (b) the $139–141M operating-income line defended or raised, and (c) an accelerating, quantified AI number that maps onto the CRM/FIVN narrative that caused the re-rating.

**Whisper number:** **unavailable.** No credibly published whisper found.

---

## 3. The one metric that matters

**It is not EPS.** Sprinklr has beaten the EPS consensus in each of the last four-plus quarters (Q1 FY27 $0.11 vs $0.10; Q2 FY26 $0.13 vs $0.10; Q4 FY26 reportedly 44% above consensus) [S17][S25][S21]. A headline beat is the base case and is priced.

**The metric is the FY27 guidance package — specifically the non-GAAP operating income line ($139–141M) and the subscription revenue line ($779.5–781.5M) — read alongside cRPO growth.**

Why cRPO and not customer count: **at the Q1 FY27 call Sprinklr retired the $1M+ customer count disclosure.** Management's stated reason was the shift to a pod-based go-to-market structure that changed "how accounts are owned, expanded and measured", while noting the $1M+ cohort's net dollar retention was 115% [S24]. The count had been falling — **147 at Q3 FY25 (up 20% YoY), 149 at Q2 FY26, 141 at Q4 FY26** [S15][S4][S22]. **This partially invalidates the triage rationale for this name:** the customer-count series the triage note wanted edge on no longer exists. NRR does, and it is improving.

What is left as forward demand evidence, with the trend:

| Metric | Q2 FY26 | Q3 FY26 | Q4 FY26 | Q1 FY27 |
| --- | --- | --- | --- | --- |
| Net dollar expansion (subscription basis) | 102% [S26] | n/s | 103% [S26] | **104%** [S24] |
| cRPO growth YoY | +7% [S4] | n/s | **+1%** [S22] | **+5%** [S24] |
| Total RPO growth YoY | +4% [S4] | n/s | flat [S22] | **+10%** [S24] |
| $1M+ customers | 149 [S4] | n/s | 141 [S22] | **discontinued** [S24] |
| AI-native SKU ARR growth YoY | n/s | n/s | n/s | **+47%** [S24] |

**My read on the expectation:** the market is looking for cRPO growth to hold at or above +5% and for the AI-native ARR growth number (+47% in Q1) to be repeated and ideally higher — because that is the only line item that connects Sprinklr to the Agentforce/Five9-AI story that moved the multiple. Absent a quantified consensus for cRPO (none sourced), I treat "cRPO ≥ +5% YoY and FY27 operating income guidance held" as the flat-line bar. `Inference — mine.`

---

## 4. Fundamentals — what changed, what is at stake

**Segment mix and growth.** Subscription is ~89% of revenue and growing ~5–6%; professional services is the swing factor and is shrinking fast. FY26 services ≈ $100.9M ($857.2M − $756.3M); FY27 guided services ≈ $87M ($867.5M − $780.5M), i.e. **−14% YoY** (my calculation from [S22][S3]). Q1 FY27 services was $24.7M and the Q2 guide implies ~$20.5M — **that ~$4M sequential services decline is most of why total revenue is guided down QoQ.** This is a mix-quality *positive* being read as a growth *negative*.

**Quarterly revenue series** [S27]:

| Quarter | Ended | Revenue | YoY |
| --- | --- | --- | --- |
| Q1 FY26 | 2025-04-30 | $205.50M | +4.9% |
| Q2 FY26 | 2025-07-31 | $212.04M | +7.5% |
| Q3 FY26 | 2025-10-31 | $219.07M | +9.2% |
| Q4 FY26 | 2026-01-31 | $220.59M | +8.9% |
| Q1 FY27 | 2026-04-30 | $219.48M | +6.8% |
| Q2 FY27 (guide) | 2026-07-31 | $214.0–215.0M | **+0.9–1.4%** |

**Margins.** Q1 FY27 non-GAAP operating margin was **14%, down from 18%** a year earlier; GAAP operating income turned positive at $10.6M / 5% margin (from −$1.8M) [S3]. Management attributes the non-GAAP compression to deliberate investment in "AI and R&D talent, particularly forward-deployed engineers", with headcount-reduction productivity expected to support H2 margin recovery [S24]. FY26 non-GAAP operating margin was 17% [S22]; FY27 guidance implies ~16%.

**Free cash flow and balance sheet.** Q1 FY27 FCF **$65.8M (30% margin)**; FY26 FCF $141.9M; FY27 guided ~$150M [S3][S22][S23]. Cash & equivalents $163.3M plus marketable securities $279.5M = **~$443M**, no meaningful debt implied by EV $1.52B vs market cap $1.92B [S28][S6]. **FCF yield on EV ≈ 9.9%** (my calculation) — for a company still growing subscription revenue mid-single-digit, that is the crux of the value case.

**Buyback / dilution.** $200M authorisation approved 11 Mar 2026 (expires 15 Mar 2027). A **$125M accelerated share repurchase** was executed 16 Mar 2026 with an initial delivery of **17.1M shares at $5.84** (80% of the notional); final settlement was still pending as of the Q1 10-Q, with ~$75M of authorisation remaining [S28][S24]. Share count fell to 234.23M [S6]. `Inference — mine:` because ASR final share delivery depends on the VWAP over the pricing period, the stock's move from $5.84 to $8.21 materially reduces (and could eliminate) any incremental share delivery at settlement; that is a small headwind to the share-count story, not a thesis.

**Customer concentration — new and material.** The Q1 FY27 10-Q discloses that **one large multinational customer represented 10.4% of Q1 FY27 subscription revenue** due to timing; no other customer exceeded 10% [S28]. This is plausibly connected to the "largest software deal in company history" with an unnamed global consumer-electronics customer disclosed around the Summer '26 release [S29]. A single 10%+ customer in a business with 5% growth is both the upside (it can ramp) and the risk (renewal/timing lumpiness).

**Geography.** Q1 FY27: Americas $112.9M (51%), EMEA $77.0M (35%), other $29.6M (14%); US alone $104.3M [S28]. Management flagged **$3–4M of Middle East deal slippage** and geopolitical timing risk on "several very large deals over the next 2, 3 quarters" [S24] — EMEA at 35% of revenue makes that a live variable this quarter.

**What changed since the last print (3 June 2026):**
1. **Summer '26 release, 15 July 2026** — agentic Voice AI agents, MCP support, ViralMoment video analytics; 16 AI features shipped. Largest software deal in company history disclosed [S29][S30].
2. **New CRO Thomas Addis effective 1 July 2026** [S31] — he was in seat for one of the three months in this quarter; granted 810,372 RSUs on 15 Aug 2026 [S32].
3. **Jordi Ribas** (President of Search & AI at Microsoft) joined the board effective 17 Aug 2026, on the Nominating & Governance and **Strategy** committees; board expanded 7→8 [S33][S34].
4. **Sector re-rating**: CRM +23% on 26 Aug on Agentforce ARR of $1.5B (+240% YoY) and a large FY27 guidance raise [S9].
5. ViralMoment (AI social-video intelligence) acquired in May 2026 [S29][S35].

---

## 5. Positioning & options

**Options: no signal available, and that is itself the finding.** No weekly expiries; first post-event expiry 18 Sep 2026 (17 days); strikes $2.50 apart; zero reported open interest on every line in the front four expiries; front-expiry volume ~200 contracts on 31 Aug. **IV term structure, skew and put/call ratio are all `unavailable`.** There is no dealer hedging flow, no straddle, and no unusual-options-activity read to be had in this name (own pull, Yahoo options API, 2026-08-31 20:00 UTC). The one observable: 133 contracts traded in the 18 Sep **$10 calls** (22% OTM, $0.09) and 52 in the $7.5 puts on 31 Aug — trivial size, but the call side was the busier line.

**Short interest — conflicting sources, flagged.**

| Source | Shares short | % of float | Days to cover | As of |
| --- | --- | --- | --- | --- |
| stockanalysis.com | 9.13M | 7.93% | 3.18 | 2026-09-01 [S6] |
| Finviz | 9.13M | 8.86% | 2.65 | ~2026-08-31 [S7] |
| Unattributed aggregator snippet | 20.96M (from 20.44M) | 20.31% | 5.49 | date unknown [S36] |

The two independent providers agree on **9.13M shares**; I treat the 20.96M figure as unreliable and `snippet_only`, but it is worth flagging because a 20% short float would change the squeeze arithmetic entirely. On the 9.13M basis the position is **moderate, not crowded short, and 2.6–3.2 days to cover is not squeeze fuel.**

**Borrow fee:** **unavailable.**

**Run-up into the print — this is the dominant positioning fact.**

| Window | CXM | IGV | CRM | FIVN | FRSH |
| --- | --- | --- | --- | --- | --- |
| 23 Jul → 31 Aug 2026 | **+49.3%** ($5.50→$8.21) | +26.3% | +64.1% | +58.9% | +42.5% |
| 26 Aug → 31 Aug 2026 | +9.9% | +7.4% | +25.3% | +8.0% | +7.8% |

(my calculation from Yahoo daily closes [S8]). Finviz corroborates: CXM +10.5% week, **+29.1% month**, +36.6% quarter, +42.3% half-year, **−5.0% year** [S7]. The 50-day MA was $5.93 and the 200-day $5.69 as of ~24 Aug [S19] — the stock is roughly 40% above its 200-day.

**How crowded does it look?** `Inference — mine:` not crowded in the derivatives or short-interest sense, because neither market is functional or extreme here. Crowded in the **momentum/beta** sense: RSI 81, price above the consensus PT, volume in the last three sessions (4.9M, ~n/a, 4.7M) running ~1.6x the 20-day average, and a move that is almost exactly the small-cap-SaaS beta of a sector melt-up rather than anything Sprinklr did. That is the fragile part: the marginal buyer of the last 49% did not buy Sprinklr's fundamentals, and has no anchor to defend if the guide is merely reiterated.

---

## 6. Sentiment & alt-data

**Analyst ratings and PT drift.** Consensus **Hold**, average PT $7.79–7.88 vs spot $8.21 [S18][S19]. Actions on record:

| Firm | Date | Action | PT |
| --- | --- | --- | --- |
| Citigroup | 2026-06-04 | Neutral, PT cut | $7 → $6 [S19] |
| Rosenblatt | 2026-06-04 | Buy, PT cut | $12 → $8.50 [S19] |
| DA Davidson | 2026-06-04 | Neutral, PT cut | $6.25 → $6.00 [S19] |
| Weiss Ratings | 2026-08-05 | Upgrade within Sell band | "sell (d)" → "sell (d+)" [S19] |
| Citizens | 2026-01-29 | Market Outperform | $17 [S37] |

**Conflict flagged:** a separate aggregator snippet reports Morgan Stanley raising $8→$10 (Equal-Weight), DA Davidson $8→$9 (Neutral) and Wells Fargo $6→$7 (Underweight) "on 5 June 2026" [S38]. Those PT levels are inconsistent with a $5.45 stock and with the same-week cuts above; I believe they are misdated (most likely June 2025) and mark them `snippet_only, low confidence`. Either way, **no post-run-up (August 2026) sell-side upgrade or PT raise was found** — the sell side has not chased this move, which is why the stock sits above its own consensus target.

**Retail/social.** Stocktwits maintains sentiment/message-volume series for CXM but I could not retrieve the numeric 7/14/30-day trend [S39]. One low-quality third-party note described "positive sentiment prevailing" in early August 2026 [S40]. **Quantified retail sentiment trend: `unavailable`.** Treat as no signal rather than a positive.

**Alt-data proxies.**
- Google Trends: **unavailable** (not retrievable in this environment).
- Web traffic / app ranks: **unavailable** and largely irrelevant — Sprinklr is a B2B enterprise platform with no consumer app.
- **Glassdoor:** 3.5/5 across 2,559 reviews, rating **up 6% over the last twelve months**; 55% would recommend, 48% positive business outlook; work-life balance 3.0, culture 3.2, career opportunities 3.3, comp 3.7 [S41]. Mildly improving from a low base — consistent with a turnaround that is landing internally but not yet in revenue. Undated as to the snapshot; `snippet_only`.
- **Job postings:** **unavailable.** Management said it is adding "forward-deployed engineers" while continuing headcount reductions elsewhere [S24] — a hiring-mix shift I could not independently verify.
- Layoff trackers reference cuts in March 2026 (~70) and an August 2026 entry, but the sourcing conflates these with the February 2025 15%/500-person action and I could not verify an August 2026 reduction independently. **Treat as unverified** [S42][S43].

---

## 7. Forensics

**Form 4 activity (pulled directly from EDGAR, full-text submissions):**

| Date | Person | Role | Code | Shares | Price | Character |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-08-17 | Jordi Ribas | Director | A | 29,850 | $0 | New-director RSU grant [S44] |
| 2026-08-15 | Thomas Addis | CRO | A | 810,372 | $0 | New-hire RSU grant, 3-yr vest from Sep 2027 [S32] |
| 2026-08-10 | Jacob Scott | General Counsel | S | 71,585 | $6.97 | **10b5-1** (plan adopted 2025-10-15) [S45] |
| 2026-06-22 | Jacob Scott | General Counsel | S | 2,724 | $4.97 | **10b5-1** (same plan) [S46] |
| 2026-06-17 | Karthik Suri | Officer | S | 41,852 | $5.14 | per aggregator [S17] |
| 2026-06-16 | Joy Corso | Officer | S | 33,635 | $5.30 | per aggregator [S19] |
| 2026-06-01 | Amitabh Misra | CTO | S | 45,127 | $5.92 | **10b5-1** (plan adopted 2025-12-22) [S47] |
| 2026-03-24 | Amitabh Misra | CTO | S | 41,667 | $5.82 | **10b5-1** (same plan) [S48] |
| 2026-03-16 | Rory Read | CEO | S | 45,001 | $5.85 | **Sell-to-cover** RSU tax withholding [S49] |
| 2026-03-15 | Rory Read | CEO | A | 2,101,575 | $0 | Annual RSU grant [S49] |
| 2026-03-16 | Ragy Thomas | Founder/Chairman | S | 16,668 | $5.85 | **Sell-to-cover** [S50] |
| 2026-02-05/06 | Rory Read | CEO | S | 78,043 + 87,795 | $6.02 / $6.00 | **10b5-1** (plan adopted 2025-10-15) [S51] |

**Read:** every disposition in the last twelve months is either a Rule 10b5-1 plan sale or a sell-to-cover for RSU tax withholding. **There is no discretionary insider selling and, more notably, no open-market insider buying — not even at the $4.72 April low.** Aggregators put three-month insider sales at 395,880 shares / ~$2.21M [S17][S19] and CEO Read at 631,230 shares / ~$4.45M over six months [S52]; both are consistent with plan sales. `Inference — mine:` neutral-to-mildly-negative. Plan sales carry no information, but a management team with a stock at 0.6x its January analyst target and no one buying is not sending a confidence signal. **No Form 4 has been filed since 19 August 2026** — no insider has transacted during the 20% rally into the print.

**Executive and director churn — heavy, and worth weighting.**
- CFO **Manish Sarin stepped down 19 Sep 2025**; **Anthony Coletta** (ex-SAP Chief IR Officer) appointed CFO effective **7 Oct 2025** [S53]. This will be Coletta's **fourth** print. `Inference — mine:` a CFO in his first year, whose predecessor left abruptly, has strong incentives to set guidance conservatively — which cuts *against* a big guidance raise but *for* a beat on the quarter.
- CMO Arun Pattabhiraman departed effective 16 Mar 2026 [S54].
- Two directors — **Yvette Kanouff and Neeraj Agrawal** — declined re-election at the 2026 annual meeting (8-K filed 29 Apr 2026); board shrank 9→7, both explicitly with "no disagreement" language [S55].
- CRO **Thomas Addis** joined 1 Jul 2026 [S31].
- **Jordi Ribas** added 17 Aug 2026; **Eileen Schloss removed from the Strategy Committee** the same day [S34].
- That is CFO, CMO, CRO and three board seats turned over in eleven months. Elevated but coherent with a declared turnaround under CEO Rory Read.

**Auditor / restatement / litigation.** No restatement, no auditor change, no going-concern language found. The **securities class action (Boshart / In re Sprinklr) was dismissed with prejudice on 31 Mar 2026**, and the consolidated derivative actions were dismissed without prejudice on 6 May 2026; no material litigation provisions as of 30 Apr 2026 [S28]. **Clean.**

**8-K cadence.** 20 8-Ks over roughly 19 months, dominated by Item 5.02 personnel filings and quarterly Item 2.02 results — no unusual clustering and, critically, **no Item 2.02 or 8.01 filing between 3 June 2026 and 1 September 2026**, i.e. **no pre-announcement and no guidance update** ahead of this print [S13][S14].

**Filing-language / disclosure shift.** The single most important forensic item is the **retirement of the $1M+ customer count** at the Q1 FY27 call, after the number had declined from 149 (Q2 FY26) to 141 (Q4 FY26) [S4][S22][S24]. Management framed it as a go-to-market restructuring artefact and offered the $1M+ cohort NDR of 115% in its place. `Inference — mine:` companies retire metrics that have stopped flattering them. The substitute metric (cohort NDR) is genuinely better on the merits, but the timing is unhelpful and it removes the cleanest way for an outsider to verify enterprise land-and-expand.

**Ownership / control.** **Hellman & Friedman controlled ~49.5% of combined Class A + Class B voting power as of 30 April 2026**, with the 10-Q noting future transfers or Class B conversions could take H&F above 50%; H&F reports on Schedule 13D (not 13G) following its purchase of additional Class A shares, with a 13D/A amendment filed 9 Dec 2025 [S56]. Founder/Chairman Ragy Thomas retains Class B holdings directly and through family trusts [S50]. Insider ownership is reported at 21.75% [S6] / 25.18% [S19] / 56.03% on a Class-A-only basis [S7]; institutional 40–52% [S6][S19].

---

## 8. Macro & peer read-through

**Regime.** The dominant fact of the last six weeks is a violent re-rating of application software on AI-monetisation evidence. **IGV +26.3% from 23 July to 31 August 2026**, with the acceleration concentrated after 26 August (own calculation, [S8]). Sprinklr's low beta (0.58–0.61) [S6][S11] did not stop it participating at 49%.

**The catalyst: Salesforce, 26 August 2026.** Q2 FY27 revenue $11.35B vs $11.32B expected, diluted EPS $4.29 vs $3.27, net income +87%, FY27 revenue guidance raised to $46.1–46.4B and EPS to $10.21–10.25; **Agentforce annualised revenue passed $1.5B, +240% YoY**; a $2.6B gain on the Anthropic stake. Shares +23% [S9][S57]. This is what re-rated the group — and it sets an implicit bar: the market now wants a *quantified, accelerating* AI revenue line from every CX vendor.

**The closest and most instructive comp: Five9, 6 August 2026.** Adjusted EPS $0.70 vs $0.68, revenue $312.4M vs $306.4M (+10%; subscription +14%), **AI revenue +78% to a $150M+ run rate**, full-year AI growth outlook raised from >40% to ≥60%, and a Fortune 100 win worth ~$100M TCV. **The stock still fell 4.3%** on the day, because adjusted EBITDA margin compressed to 22% from 24% and FCF fell 30% YoY [S58][S59]. **This is Sprinklr's exact profile** — margin compression (18%→14%) and only modest FCF growth ($141.9M→~$150M guided) — with a far weaker growth rate. It is the single most relevant precedent in this dossier. (Note the sequel: FIVN is +8% from 26 Aug to 31 Aug and +59% from 23 July, so the sector bid *did* overwhelm the bad day within three weeks — which is the bull's rebuttal.)

**Freshworks** — the nearest small-cap CX comp — reported Q2 2026 revenue of $237.4M, **+16% YoY** [S60], roughly ten points faster than Sprinklr, and is +42% over the same window. Sprinklr is the slowest-growing name in its own comp set and has been re-rated alongside them.

**Rate / FX / commodity sensitivity.** Minimal direct commodity exposure. FX matters at the margin — 49% of revenue is non-Americas [S28] — and a weaker dollar would be a modest tailwind, but I found no company quantification and mark it `unavailable`. The real macro sensitivity is **enterprise software budget cycles and multiple compression risk**: at 2.2x P/S [S7] on ~1% growth, the equity is a duration asset re-rated on sentiment.

**Customer/supplier read-throughs.** The Middle East deal slippage management flagged ($3–4M, plus "several very large deals over the next 2, 3 quarters" with geopolitical timing risk) [S24] is the one identifiable idiosyncratic macro exposure and is unresolved going into this print.

---

## 9. Bull case / bear case / base case

**Bull.** Sprinklr is the cheapest genuine AI-CX asset in a group that just got repriced: EV $1.52B on ~$150M of guided FY27 free cash flow is a ~10% FCF yield [S6][S23], against Freshworks at +16% growth and Five9 at +10% both trading far richer. The operating turnaround is real in the retention data — NDR has stepped 102% → 103% → 104%, the $1M+ cohort NDR is 115%, renewal rates are the best in over two years, "Project Bear Hug" is producing double-digit renewal improvements in the cohorts where it has been applied, and total RPO growth re-accelerated to +10% with cRPO to +5% [S24]. AI-native SKU ARR grew 47% with 180+ active customer projects, and the company signed the largest software deal in its history [S24][S29] — visible in the 10-Q as a customer at 10.4% of subscription revenue [S28]. A new CFO has set guidance conservatively enough that the company has beaten four straight quarters, and the strategic file is open in a way it has not been before: H&F holds ~49.5% of the voting power [S56], the board has a **Strategy Committee**, and Microsoft's President of Search & AI just joined it [S34] — the exact configuration Citizens described when it argued for an acquisition exit at a $17 target [S37]. In a regime where Five9 fell 4% on its print and is up 8% since, any FY27 raise gets bought hard.

**Bear.** The company itself has guided this quarter to **~1% revenue growth, a 22% YoY decline in non-GAAP operating income, EPS down from $0.13 to ~$0.10, and a sequential decline in subscription revenue** [S3][S4]. Into that, the stock is +49% in six weeks, +29% in a month, RSI 81, trading **above** its $7.79–7.88 consensus price target with no August upgrade or PT raise on record [S7][S18][S19]. The entire move is sector beta (IGV +26%, FRSH +42%, FIVN +59% over the identical window) — the marginal buyer bought the AI-software trade, not Sprinklr, and has nothing to defend if the guide is merely reiterated. Management cut FY27 operating income by $5M at the last print and the stock gapped −8.4% [S22][S3]. The most relevant precedent, Five9, beat both lines, *raised* its AI outlook and still fell 4.3% because margins and FCF compressed — Sprinklr has the same margin compression and a third of the growth [S58]. The company retired its $1M+ customer-count disclosure right after it fell from 149 to 141 [S4][S22][S24]. Both prior fiscal-Q2 (September) prints fell 9–10% [S8]. And no insider has bought a share on the open market, at any price, including the $4.72 low.

**Base case (mine).** Sprinklr delivers Q2 revenue at or slightly above the top of its $214–215M guide and EPS of $0.11–0.13 against a $0.104 consensus — a real but unremarkable beat, consistent with four straight quarters of sandbagging by a first-year CFO. NDR holds at 104% or ticks to 105%, cRPO growth is in the +4–7% band, and management **reaffirms** rather than raises FY27 subscription revenue and the $139–141M operating income line, pointing again to the H2 ramp and to lumpy large-deal and Middle East timing. On any other setup that print is a modest positive. Sitting on a +29% one-month move, above the consensus PT, at RSI 81, with the September seasonal and the Five9 template in front of it, I think it is more likely to be sold than bought — a fade of roughly the historical 6–7% median magnitude, skewed by the fact that the sector bid is strong enough to truncate the downside within days. I put roughly 40% odds on an up day and expect a realised absolute move in the 5–9% range.

---

## 10. What would flip the consensus view

The single most credible reversal, stated concretely: **Sprinklr raises FY27 subscription revenue guidance above $781.5M and defends or raises the $139–141M non-GAAP operating income range, while quantifying AI-native ARR growth at or above the 47% it printed in Q1 — ideally with an explicit ARR dollar figure.** That combination would convert the last six weeks from a beta trade into a fundamental one: it would confirm that the H2 subscription reacceleration is contracted rather than hoped for, it would neutralise the Five9 "margin compression punishes AI growth" template, and it would give the sell side — which has not raised a target since June and sits below spot — a reason to chase. cRPO growth accelerating to double digits would be the corroborating tell, because it is the only forward-demand number left after the $1M+ customer count was retired.

A second, lower-probability reversal that is nonetheless live in this specific name: **any disclosure touching strategic alternatives.** With H&F at ~49.5% of the voting power, a standing Strategy Committee, and Microsoft's President of Search & AI newly seated on it, a process — or a bid — would make the operating numbers irrelevant. I have found **no evidence that a process exists**; this is optionality, not a forecast.

Conversely, the view flips the other way — from "fade" to "rout" — if FY27 operating income is cut a second consecutive quarter, or if cRPO growth decelerates back toward the +1% printed at Q4 FY26.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **Event-implied move: no ATM straddle and no published implied move.** CXM has no weeklies, $2.50 strike spacing, zero reported OI, ~200 contracts of front-expiry volume. | The single most useful anchor for sizing an earnings trade is simply absent. Everything downstream must lean on realised-move history (mean \|6.79%\|, median \|6.01%\|) instead of a market-clearing expectation. |
| **IV rank / percentile, IV term structure, skew, put/call ratio: all unavailable.** | No read on whether volatility is rich or cheap into the event, and no way to detect directional options positioning. |
| **Borrow fee / short-borrow availability: unavailable.** | Cannot assess cost-to-carry for the short side or detect hard-to-borrow stress. |
| **Short interest conflict:** two providers say 9.13M shares / ~8% of float; one unattributed snippet says 20.96M / 20.31% / 5.49 days. | A 20% short float would make this a squeeze candidate rather than a fade. I used the 9.13M figure; the panel should know the alternative exists. |
| **Whisper number: none found.** | Cannot distinguish "beats consensus" from "beats what the buy side actually expects" — the gap that most often determines the reaction. |
| **Clean 30/60/90-day estimate revision table: not sourced.** Only two dated, snippet-level data points (2 downward revisions over 60 days as of 25 June; −2.5% over 60 days as of early June). | The revision *trend* through August — after the sector re-rated — is unknown and could cut either way. |
| **Consensus for subscription revenue, cRPO, NDR and non-GAAP operating income: not sourced.** | These are the metrics the print actually trades on (§3) and I have the company's guide but not the Street's number for them. |
| **Quantified retail/social sentiment with 7/14/30-day trend: unavailable.** Stocktwits page not retrievable. | Cannot corroborate or contradict the momentum read with a positioning-independent sentiment series. |
| **Google Trends, web traffic, job-posting counts: unavailable.** | No independent demand nowcast. Partially mitigated by the fact that B2B enterprise software has weak consumer alt-data signal anyway. |
| **August 2026 layoff: unverified.** Trackers reference it but conflate it with February 2025. | A pre-print workforce action would be a meaningful cost/tone signal. |
| **Analyst PT actions dated "5 June 2026" (MS $8→$10, DAVA $8→$9, WFC $6→$7) conflict with same-week cuts and are probably misdated.** | The direction of sell-side PT drift is ambiguous as a result; I relied on the current $7.79–7.88 averages, which are consistent across two providers. |
| **28 August 2026 daily bar missing from Yahoo's series;** close of $8.16 taken from a search snippet and cross-checked against stockanalysis.com's +$0.05 / +0.61% for 31 Aug. | Minor, but one of the three most recent sessions rests on a snippet. |
| **FX sensitivity not quantified by the company.** | 49% of revenue is non-Americas; a currency swing could move reported subscription revenue by more than the width of the guidance range. |

---

## 12. Sources

1. **[S1]** https://www.stocktitan.net/news/CXM/sprinklr-announces-date-of-second-quarter-financial-ceac3ffvvh0e.html — Q2 FY27 results released **before market open 2 Sep 2026**, call 8:30am ET. Event confirmation.
2. **[S2]** https://www.nasdaq.com/press-release/sprinklr-announces-date-second-quarter-financial-results-2026-08-12 — same announcement, dated 12 Aug 2026; establishes 3 weeks' notice and no date change.
3. **[S3]** https://www.sprinklr.com/newsroom/sprinklr-announces-first-quarter-fiscal-2027-results/ — Q1 FY27 results and Q2/FY27 guidance (revenue, subscription, operating income, EPS, FCF, cash, RPO).
4. **[S4]** https://investors.sprinklr.com/news/press-releases/detail/234/sprinklr-announces-second-quarter-fiscal-2026-results — Q2 FY26 actuals: $212.0M total, $188.5M subscription, 18% non-GAAP margin, $0.13 EPS, 149 $1M+ customers. The YoY comparison base.
5. **[S5]** https://stockanalysis.com/stocks/cxm/ — spot $8.21 as of 31 Aug 2026 16:00 EDT, market cap $1.92B, shares 234.23M, 52-week range, next earnings date.
6. **[S6]** https://stockanalysis.com/stocks/cxm/statistics/ — short interest 9.13M / 7.93% of float / 3.18 days to cover, float 115.14M, EV $1.52B, beta 0.61, insider 21.75% / institutional 52.18%.
7. **[S7]** https://finviz.com/quote.ashx?t=cxm — short float 8.86%, short ratio 2.65, RSI(14) 81.15, performance week/month/quarter/half/year, P/S 2.21, target price $7.88.
8. **[S8]** https://query1.finance.yahoo.com/v8/finance/chart/CXM — daily OHLCV used for all historical earnings-day moves, run-up calculations, realised volatility and peer/IGV comparisons. (Same endpoint for IGV, CRM, FIVN, FRSH.)
9. **[S9]** https://www.salesforce.com/news/press-releases/2026/08/26/fy27-q2-earnings/ — Salesforce Q2 FY27 results, guidance raise, Agentforce $1.5B ARR +240%. The sector catalyst.
10. **[S10]** https://www.investing.com/equities/sprinklr — CXM closed $8.16 on 28 Aug 2026 (+2.77%). `snippet_only`.
11. **[S11]** https://www.dailypolitical.com/2026/08/24/sprinklr-inc-nysecxm-given-consensus-rating-of-hold-by-brokerages.html — beta 0.58, 50-day MA $5.93, 200-day MA $5.69.
12. **[S12]** https://www.barchart.com/story/news/2268675/sprinklr-s-enterprise-customer-retention-the-metric-that-could-rewrite-the-bull-case — 2 Jun 2026: Market Chameleon average Day-0 move 5.98%, expected move 13.71% through 18 Jun expiry. Historical/stale reference only.
13. **[S13]** https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001569345&type=8-K — 8-K filing dates and item numbers used to date every earnings release and confirm the AMC→BMO switch; also establishes 8-K cadence and the absence of a pre-announcement.
14. **[S14]** EDGAR atom feed, same CIK, `dateb=20250201` — earlier 8-K dates (2024-09-04 and 2024-12-04 Item 2.02).
15. **[S15]** https://www.businesswire.com/news/home/20241204028277/en/Sprinklr-Announces-Third-Quarter-Fiscal-2025-Results — Q3 FY25 released **after market close** 4 Dec 2024; 147 $1M+ customers (+20% YoY); resolves the session attribution for the 2024 events.
16. **[S16]** https://www.nasdaq.com/articles/insights-sprinklr-cxm-q2-wall-street-projections-key-metrics — Q2 FY27 consensus EPS $0.1040, revenue $214.449M.
17. **[S17]** https://www.dailypolitical.com/2026/08/30/sprinklr-cxm-expected-to-release-quarterly-earnings-on-wednesday.html — consensus EPS/revenue, Q1 FY27 actual vs estimate, analyst actions, insider sales totals, ownership.
18. **[S18]** https://stockanalysis.com/stocks/cxm/forecast/ — 9 analysts, Hold, average PT $7.88, range $6–$12, rating distribution, FY26/FY27 revenue and EPS estimates.
19. **[S19]** https://www.dailypolitical.com/2026/08/24/sprinklr-inc-nysecxm-given-consensus-rating-of-hold-by-brokerages.html — 8 brokerages, average PT $7.7857, Citigroup/Rosenblatt/DA Davidson/Weiss actions with dates, Joy Corso and Jacob Scott insider sales, moving averages, ownership.
20. **[S20]** https://finance.yahoo.com/markets/options/articles/implied-volatility-surging-sprinklr-stock-123600840.html — 25 Jun 2026: two downward current-quarter revisions over 60 days, consensus $0.13 → $0.11; Zacks Rank #2. `snippet_only`.
21. **[S21]** https://www.msn.com/en-us/money/topstocks/sprinklr-q1-2027-earnings-preview/ar-AA24EFU2 (via Investing.com preview) — EPS estimates −2.5% over 60 days then stabilising; Q4 beat 44% above consensus; nine analysts, mean PT $8.47. `snippet_only`.
22. **[S22]** https://www.sec.gov/Archives/edgar/data/1569345/000156934526000011/live10kearningsrelease.htm — Q4/FY26 results: FY26 total $857.2M, subscription $756.3M, non-GAAP op income $146.2M, FCF $141.9M, 141 $1M+ customers, RPO flat / cRPO +1%; initial FY27 guidance; $200M buyback authorisation with $125M ASR.
23. **[S23]** https://www.chartmill.com/news/CXM/Chartmill-49384-Sprinklr-NYSECXM-Falls-on-Soft-Guidance-Despite-Q1-Beat (via search snippet; page returns 403) — FY27 FCF ~$150M. `snippet_only`.
24. **[S24]** https://www.fool.com/earnings/call-transcripts/2026/06/04/sprinklr-cxm-q1-2027-earnings-transcript/ — Q1 FY27 call: NDR 104% (103% prior), $1M+ cohort NDR 115%, cRPO $627.1M +5%, RPO $1.04B +10%, AI-native SKU ARR +47%, 180+ AI projects, 17.1M shares repurchased, $75M authorisation left, $3–4M Middle East slippage, rationale for retiring the $1M+ customer disclosure, H2 ramp commentary, forward-deployed engineer hiring.
25. **[S25]** https://www.zacks.com/stock/news/2746466/sprinklr-cxm-beats-q2-earnings-and-revenue-estimates — Q2 FY26 $0.13 vs $0.10 consensus; the stock still fell 10% that day.
26. **[S26]** https://finance.yahoo.com/quote/CXM/earnings/CXM-Q4-2026-earnings_call-418900.html — NDR 103% in Q4 FY26, 102% in Q1/Q2 FY26. `snippet_only`.
27. **[S27]** https://stockanalysis.com/stocks/cxm/financials/?p=quarterly and .../cash-flow-statement/?p=quarterly — quarterly revenue/operating income/EPS series and quarterly operating cash flow, capex, FCF and buyback outlays.
28. **[S28]** https://www.sec.gov/Archives/edgar/data/0001569345/000156934526000028/cxm-20260430.htm — Q1 FY27 10-Q: deferred revenue $414.2M, RPO $1,038.3M, cRPO $627.1M, SBC $20.7M, ASR terms (17.1M shares at $5.84, ~$75M remaining), cash $163.3M + securities $279.5M, **one customer at 10.4% of subscription revenue**, geographic revenue split, securities class action dismissed with prejudice 31 Mar 2026.
29. **[S29]** https://www.cmswire.com/customer-experience/sprinklr-ships-16-ai-features-for-realtime-cx/ — Summer '26 release (15 Jul 2026), agentic Voice AI, MCP, ViralMoment video analytics, and the largest software deal in company history with a global consumer-electronics customer.
30. **[S30]** https://www.sprinklr.com/newsroom/sprinklr-introduces-new-ai-capabilities-to-help-brands-move-from-insights-to-real-time-customer-action/ — company announcement of the Summer '26 release.
31. **[S31]** https://www.sec.gov/Archives/edgar/data/0001569345/000119312526291553/d106582dex991.htm — Thomas Addis appointed Chief Revenue Officer effective 1 Jul 2026.
32. **[S32]** https://www.sec.gov/Archives/edgar/data/1569345/000214446826000004/0002144468-26-000004.txt — Form 4, Thomas Addis, 810,372 RSUs granted 15 Aug 2026.
33. **[S33]** https://www.sec.gov/Archives/edgar/data/0001569345/000119312526347899/d40248dex991.htm — Jordi Ribas board appointment press release.
34. **[S34]** https://www.sec.gov/Archives/edgar/data/0001569345/000119312526347899/d40248d8k.htm — 8-K filed 13 Aug 2026: Ribas appointed Class II director effective 17 Aug, board 7→8, Nominating & Governance + **Strategy Committee**; Eileen Schloss removed from the Strategy Committee; director compensation terms.
35. **[S35]** https://www.investing.com/news/company-news/sprinklr-acquires-viralmoments-video-intelligence-assets-93CH-4714138 — ViralMoment acquisition (May 2026).
36. **[S36]** https://www.marketbeat.com/stocks/NYSE/CXM/short-interest — conflicting short interest 20.44M → 20.96M, 20.31% of float, 5.49 days to cover, date not established. `snippet_only`, low confidence.
37. **[S37]** https://finance.yahoo.com/news/citizens-analyst-report-says-sprinklr-154546995.html — 29 Jan 2026 Citizens Market Outperform, PT $17, acquisition-exit thesis, named potential acquirers, and H&F at 45% of voting rights / 69M shares as of May 2025.
38. **[S38]** https://www.marketbeat.com/instant-alerts/... (via search) — Morgan Stanley $8→$10, DA Davidson $8→$9, Wells Fargo $6→$7 "5 Jun 2026". `snippet_only`, probably misdated; flagged as a conflict.
39. **[S39]** https://stocktwits.com/symbol/CXM/sentiment — sentiment/message-volume series exists; numeric values not retrievable.
40. **[S40]** https://news.stocktradersdaily.com/news_release/1/Responsive_Playbooks_and_the_CXM_Inflection_080926072402_1786317842.html — early-Aug 2026 "positive sentiment prevailing". Low-quality; colour only.
41. **[S41]** https://www.glassdoor.com/Reviews/Sprinklr-Reviews-E427532.htm — 3.5/5 across 2,559 reviews, +6% over twelve months, 55% recommend, 48% positive outlook, sub-scores. `snippet_only`.
42. **[S42]** https://layoffs.fyi/company/sprinklr/ — layoff tracker entries including an August 2026 reference. Unverified.
43. **[S43]** https://www.cxtoday.com/contact-center/sprinklr-initiates-project-bear-hug-to-prioritize-enterprise-customers-opens-up-on-its-layoffs/ — Project Bear Hug (top 500 enterprise customers), Rule of 40 focus, layoff history.
44. **[S44]** https://www.sec.gov/Archives/edgar/data/1569345/000215112126000004/0002151121-26-000004.txt — Form 4, Jordi Ribas, 29,850 RSUs granted 17 Aug 2026.
45. **[S45]** https://www.sec.gov/Archives/edgar/data/1569345/000196757526000010/0001967575-26-000010.txt — Form 4, Jacob Scott (GC), sold 71,585 at $6.97 on 10 Aug 2026 under a 10b5-1 plan adopted 15 Oct 2025.
46. **[S46]** https://www.sec.gov/Archives/edgar/data/1569345/000196757526000008/0001967575-26-000008.txt — Form 4, Jacob Scott, sold 2,724 at $4.97 on 22 Jun 2026, same 10b5-1 plan.
47. **[S47]** https://www.sec.gov/Archives/edgar/data/1569345/000201805026000006/0002018050-26-000006.txt — Form 4, Amitabh Misra (CTO), sold 45,127 at $5.92 on 1 Jun 2026 under a 10b5-1 plan adopted 22 Dec 2025.
48. **[S48]** https://www.sec.gov/Archives/edgar/data/1569345/000201805026000004/0002018050-26-000004.txt — Form 4, Misra, sold 41,667 at $5.82 on 24 Mar 2026, same plan.
49. **[S49]** https://www.sec.gov/Archives/edgar/data/1569345/000152859726000006/0001528597-26-000006.txt — Form 4, Rory Read (CEO), 2,101,575 RSUs granted 15 Mar 2026; 45,001 sold 16 Mar 2026 as sell-to-cover.
50. **[S50]** https://www.sec.gov/Archives/edgar/data/1569345/000186680226000004/0001866802-26-000004.txt — Form 4, Ragy Thomas, 16,668 sold 16 Mar 2026 as sell-to-cover; Class B and family-trust holdings.
51. **[S51]** https://www.sec.gov/Archives/edgar/data/1569345/000152859726000004/0001528597-26-000004.txt — Form 4, Rory Read, 78,043 and 87,795 sold 5–6 Feb 2026 at ~$6.00 under a 10b5-1 plan adopted 15 Oct 2025; also a 20-share open-market purchase in Nov 2024.
52. **[S52]** https://www.gurufocus.com/news/8599811/insider-selling-rory-read-sells-165858-shares-of-sprinklr-inc-cxm — CEO six-month sales aggregate (631,230 shares / ~$4.45M) and Ragy Thomas transaction history. `snippet_only`.
53. **[S53]** https://www.tipranks.com/news/company-announcements/sprinklr-appoints-anthony-coletta-as-new-cfo and https://www.sahmcapital.com/news/content/sprinklr-appoints-anthony-coletta-cfo-effective-immediately-2025-10-07 — CFO transition: Manish Sarin stepped down 19 Sep 2025; Anthony Coletta (ex-SAP Chief IR Officer) effective 7 Oct 2025.
54. **[S54]** https://www.sec.gov/Archives/edgar/data/1569345/000156934526000004/cxm-20260120.htm — 8-K, CMO Arun Pattabhiraman departing effective 16 Mar 2026.
55. **[S55]** https://www.sec.gov/Archives/edgar/data/0001569345/000156934526000017/cxm-20260423.htm — 8-K, directors Yvette Kanouff and Neeraj Agrawal declining re-election; board 9→7; committee reassignments; "no disagreement" language.
56. **[S56]** https://www.sec.gov/Archives/edgar/data/0001569345/000156934526000028/cxm-20260430.htm (10-Q ownership disclosure) and https://investors.sprinklr.com/financial-information/all-sec-filings/content/0001193125-25-313023/0001193125-25-313023.pdf (Schedule 13D/A, 9 Dec 2025) — Hellman & Friedman at ~49.5% of combined voting power as of 30 Apr 2026, with potential to exceed 50%.
57. **[S57]** https://www.cnbc.com/2026/08/26/salesforce-crm-q2-earnings-report-2027.html — Salesforce Q2 FY27 coverage and stock reaction.
58. **[S58]** https://www.investing.com/news/transcripts/earnings-call-transcript-five9-tops-q2-2026-estimates-but-shares-fall-93CH-4844484 — Five9 Q2 2026: beat on EPS and revenue, AI revenue +78% to $150M+ run rate, guidance raised, **shares fell 4.29%** on EBITDA margin compression (24%→22%) and FCF −30%.
59. **[S59]** https://www.investing.com/news/company-news/five9-q2-2026-slides-show-ai-growth-amid-margin-pressure-93CH-4844544 — Five9 Q2 2026 slide detail.
60. **[S60]** https://www.investing.com/news/company-news/freshworks-q2-2026-slides-enterprise-growth-drives-16-revenue-gain-93CH-4836215 — Freshworks Q2 2026 revenue $237.4M, +16% YoY.

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented or relied upon as such. Figures are sourced or explicitly marked unavailable; inferences are labelled as the analyst's own.*
