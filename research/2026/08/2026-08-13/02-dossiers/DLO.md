# DLO — DLocal Limited

**What this print is about.** dLocal is no longer a "does the volume grow" story — total payment volume has compounded above 50% year-on-year for six straight quarters and grew 73% in Q1 2026 [1]. This print is about whether the *dollars* follow the volume. Gross profit over TPV has fallen from 1.05% (Q1'25) to 0.88% (Q4'25) to 0.84% (Q1'26) [1][2], and operating expenses grew 58% year-on-year in Q1 [1]. Management's FY26 guide requires operating profit of roughly $280–291M off a Q1 base of $52.8M — an arithmetic that only closes if the promised second-half operating-leverage inflection is real [1][2]. Q2 is, by management's own framing, the last quarter of elevated H1 opex, which makes it the structurally worst quarter of the year for the exact metric this stock trades on. The last two prints where record TPV was paired with soft unit economics were sold hard (-6.8% and -13.0%); the one print where operating profit grew 48% and capital returns were announced rallied +9.4% [computed, 3]. Triage's framing — "violent reactions to take-rate and FX commentary" — is directionally right on take rate; I found less evidence that FX per se is the trigger, and would re-centre it on **operating profit and opex**.

---

## 1. Event & anchors

`event_confirmed: true`

| Item | Value | As-of / source |
| --- | --- | --- |
| Earnings date | **Thursday 13 August 2026** | Company press release, 5 Jun 2026 [4] |
| Session | **AMC** (after US market close) | Company press release [4] |
| Call time | 17:00 ET, conference call + video webcast, investor.dlocal.com | Company press release [4] |
| Fiscal period | Q2 2026, quarter ended 30 June 2026 | Company press release [4] |
| Date changed / pre-announced? | No. Date set 5 Jun 2026 and unchanged; no pre-announcement or 6-K guidance update found between 14 May and 13 Aug 2026 [5][6] | — |
| Spot | **$14.28** (close) | 2026-08-12 16:00 ET [7] |
| Spot (pre-market) | $14.50 | 2026-08-13 07:48 ET [7] |
| Market cap | **$4.19B** | 2026-08-12 [7] |
| Shares outstanding | 293.47M (float 79.64M; insider ownership 49.01%) | [7] |
| Enterprise value | $3.39B; net cash $803.95M ($2.74/sh) | [7] |
| Forward P/E | 15.37 (trailing 22.31) | [7] |
| **Event implied move** | **≈11.9%** — ATM straddle, 21 Aug 2026 expiry, $14 strike, mid $1.70 vs $14.28 close. Forward-interpolated ATM straddle ≈$1.76 ≈ 12.3% (parity forward $14.30–14.35) | CBOE delayed chain, 2026-08-12/13 [8], my computation |
| Implied move (published) | **11%** ("options data compiled by Bloomberg") | Investing.com, 6 Aug 2026 [9] |
| IV rank / percentile | **unavailable** (Market Chameleon, OptionCharts, OptionSlam all gated) | — |
| Front-expiry IV | ~95% (21 Aug ATM call 94.7 / put 95.1) | [8] |
| 30-day IV (iv30) | 60.86 | CBOE [8] |
| 20d / 60d realised vol | 31.0% / 43.2% | computed from Yahoo daily closes [3] |

### Realised one-day earnings reactions (close-to-close, report date → next session)

All computed by me from Yahoo Finance daily closes [3]; earnings dates cross-checked against Investing.com's earnings table [10].

| Report date | Quarter | Close before | Close after | Move |
| --- | --- | --- | --- | --- |
| 2024-05-15 | Q1'24 | 10.00 | 9.75 | **−2.50%** |
| 2024-08-14 | Q2'24 | 7.76 | 8.03 | **+3.48%** |
| 2024-11-13 | Q3'24 | 9.04 | 10.20 | **+12.83%** |
| 2025-03-11 | Q4'24 | 8.58 | 8.52 | **−0.70%** |
| 2025-05-14 | Q1'25 | 10.19 | 11.24 | **+10.30%** |
| 2025-08-13 | Q2'25 | 11.69 | 15.35 | **+31.31%** |
| 2025-11-12 | Q3'25 | 14.86 | 13.85 | **−6.80%** |
| 2026-03-18 | Q4'25 | 11.45 | 12.53 | **+9.43%** |
| 2026-05-14 | Q1'26 | 12.66 | 11.01 | **−13.03%** |

- **Last 6 quarters:** [−0.70, +10.30, +31.31, −6.80, +9.43, −13.03]; mean |move| **11.93%**, median |move| **9.87%**, max |move| **31.31%**. Up/down: 3 up / 3 down.
- **Last 8 quarters:** mean |move| 10.99%, median 9.87%, 5 up / 3 down.
- **Implied (11.9%) sits almost exactly on the 6-quarter mean absolute move (11.9%) and ~2pts above the median (9.9%).** My read: options are fairly priced to slightly rich versus the median outcome, but the fat right tail (Aug'25 +31%) justifies the premium.

**Discrepancy flag.** Press-reported reaction figures do not reconcile with the close-to-close series. Investing.com/Bloomberg cite "actual price changes from −28.7% to +49.4%" over the past eight, a median move of 15.2%, a +22.4% move on 13 Nov 2024 and +11.7% on 14 Aug 2024 [9]. My computed close-to-close figures for those two dates are +12.83% and +3.48%. Benzinga separately reported DLO "+15.48% at $13.50 in extended trading" on 13 Aug 2025 [11] against a next-day close-to-close of +31.31%. I have used close-to-close throughout and flag that Bloomberg's methodology is evidently different (likely multi-session or intraday-extreme). Do not mix the two series.

---

## 2. The bar

| Metric | Consensus | Source |
| --- | --- | --- |
| Q2'26 EPS | **$0.191** | Investing.com earnings table [10] |
| Q2'26 EPS (alt) | $0.18 | TradingKey / Investing.com summary [12], `snippet_only` |
| Q2'26 EPS (alt) | $0.20 | WallStreetZen [13], `snippet_only` |
| Q2'26 revenue | **$364.65M** (+42.2% YoY vs $256.5M) | Investing.com earnings table [10] |
| FY26 revenue | $1.54B (+40.65%) | stockanalysis.com, 10 analysts [14] |
| FY26 EPS | $0.85 (+5.79%) | stockanalysis.com [14] |
| Analyst count | 10 (stockanalysis) / 8 with ratings in last 12m (MarketBeat) | [14][15] |
| Consensus PT | $18.25 (range $14.50–$21.00) / $17.75 (range $15–$21) | [14][15] |
| Rating split | 6 Strong Buy / 3 Buy / 1 Hold (stockanalysis, Jul 2026); 1 SB / 6 Buy / 1 Hold (MarketBeat) | [14][15] |
| Whisper number | **unavailable** — no credibly published whisper found | — |

**Estimate revisions.** Partial. Seeking Alpha's revisions page (via snippet) shows **0 up / 1 down EPS revision in the last 90 days** for the near quarter, but **2 up / 0 down** for the current fiscal year [16], `snippet_only`. The FY26 EPS consensus is quoted at $0.85 by stockanalysis [14] and $0.84 by WallStreetZen (range $0.74–$0.94) [13]; Simply Wall St reported the FY26 EPS estimate falling from $0.828 to $0.72 at an unstated date [17], which I could not date or reconcile and therefore do not rely on. **30/60-day revision detail is a coverage gap.**

**Surprise history (Investing.com basis — reported diluted EPS vs forecast) [10]:**

| Date | EPS act/est | Surprise | Rev act/est | Rev surprise |
| --- | --- | --- | --- | --- |
| 2026-05-14 | 0.140 / 0.170 | −17.65% | 335.9 / 334.4 | **+0.45%** |
| 2026-03-18 | 0.180 / 0.180 | 0.00% | 337.9 / 293.6 | +15.09% |
| 2025-11-12 | 0.170 / 0.160 | +6.25% | 282.5 / 256.4 | +10.18% |
| 2025-08-13 | 0.172 / 0.130 | +32.31% | 256.5 / 232.2 | +10.48% |
| 2025-05-14 | 0.175 / 0.120 | +46.00% | 216.8 / 205.9 | +5.26% |
| 2025-02-27 | 0.100 / 0.140 | −28.57% | 204.5 / 204.9 | −0.19% |

**The single most important line in that table is the last revenue-surprise column.** DLO beat revenue by 5–15% for four consecutive quarters, then beat by **0.45%** in Q1'26. The Street has caught up to the TPV ramp. The mechanism that produced the +31% reaction in August 2025 — a $24M revenue beat — is no longer available at the same magnitude.

**Guidance setup (FY2026, reaffirmed unchanged at Q1 on 14 May 2026) [1][2]:**

| Line | FY25 base | FY26 guide | Implied FY26 | Q1'26 actual | Q2–Q4 required | Required quarterly avg |
| --- | --- | --- | --- | --- | --- | --- |
| TPV | $40.8B | +50–60% | $61.2–65.3B | $14.1B | $47.1–51.2B | $15.7–17.1B |
| Gross profit | $402.8M | +22.5–27.5% | $493.4–513.6M | $118.7M | $374.7–394.9M | $124.9–131.6M |
| Operating profit | $219.9M | +27.5–32.5% | $280.4–291.4M | $52.8M (rep) / $57.2M (ex-item) | $227.6–238.6M | **$75.9–79.5M** |

*(Guidance and FY25 bases from the Q4'25 release [2]; Q1'26 actuals from the Q1 release [1]. Required-run-rate arithmetic is mine.)*

**What the company has to deliver just to hold the stock flat (my inference):**
1. Revenue ≥ ~$365M and gross profit ≥ **~$125M** (implies ≥+26% YoY off $98.9M in Q2'25 [18]).
2. Gross profit / TPV **≥ ~0.80%**. Below that and the compression narrative reasserts.
3. Reported diluted EPS ≥ **$0.19**, which requires net income of ~$56M vs $51.6M ex-item in Q1 [1] — a ~9% sequential step on an adjusted basis, achievable only if opex is genuinely flat.
4. Opex growth decelerating hard from Q1's **+58% YoY** [1].
5. FY26 guidance reaffirmed, ideally with the TPV range raised (Q1 ran at +73% against a +50–60% guide — a raise is arithmetically easy and, in my view, likely).

---

## 3. The one metric that matters

**Gross profit dollars and the operating-profit run-rate — not EPS, not TPV.**

The evidence that TPV is *not* the driver is unusually clean. Q3'25: record $10.4B TPV, +59% YoY, first quarter above $100M gross profit — stock **−6.80%**. Q1'26: record $14.1B TPV, +73% YoY, record $118.7M gross profit — stock **−13.03%** [1][3]. Q4'25: TPV +70% *and* operating profit +48% *and* a $300M buyback plus a new dividend policy — stock **+9.43%** [2][3]. The market pays for operating profit and capital returns and discounts volume records entirely.

The specific number to watch is **operating profit**. Guidance requires an average of $75.9–79.5M per quarter across Q2–Q4 against $52.8M reported in Q1 and $62.7M in Q4'25 [1][2]. Management pre-committed to the mechanism: H2 benefit from "(i) the end of the investment cycle, (ii) acceleration of our automation agenda driving headcount reductions; (iii) corrective OPEX actions; and (iv) lower share-based payments expense," plus **no net new hiring for the remainder of 2026** [1]. Q2 is the first quarter in which the mid-May hiring freeze can appear, but management explicitly framed the leverage as an **H2** event.

**Expectation (my inference, not sourced):** Q2 operating profit of ~$58–66M. If it prints at or above ~$66M with opex growth under ~35% YoY, the H2 bridge is credible and the guide is safe. If it prints below ~$58M, the implied Q3+Q4 requirement rises to roughly $85–90M per quarter and the market will conclude the operating-profit guide is unreachable. **Second watch item: gross profit / TPV.** Q1 was 0.84%; at a plausible ~$16B Q2 TPV and ~$125M gross profit the ratio lands near 0.78%. A print in the 0.80–0.85% band is neutral; below 0.78% reopens the wound.

---

## 4. Fundamentals — what changed, what is at stake

**Q1 2026 actuals (reported 14 May 2026) [1]:**
- TPV **$14.1B**, +73% YoY (+63% cc), +7% QoQ. Pay-ins $10.1B (72%, +86%); pay-outs $3.9B (28%, +101%). Local-to-local $7.7B (55%, +101%); cross-border $6.3B (45%, +49%).
- Revenue **$335.9M**, +55% YoY (+52% cc), flat QoQ. LatAm $262.5M (78%, +61%) — Brazil $57.8M, Argentina $61.2M, Mexico $55.7M, other LatAm $87.8M. Africa & Asia $73.4M (22%, +36%).
- Gross profit **$118.7M**, +40% YoY, +2% QoQ. Margin 35% (vs 39% Q1'25, 34% Q4'25). LatAm $84.7M (71%); Africa & Asia $34.0M (29%). **GP/TPV 0.84%** vs 1.05% Q1'25.
- Operating profit **$52.8M** (+15%) / $57.2M ex prior-period tax adjustment (+25%). Opex $62M ex-item, **+58% YoY**, described by management as "slightly above" expectations.
- Net income **$41.9M** (−10%) / $51.6M ex-item (+11%). Diluted EPS **$0.14** reported / $0.17 adjusted.
- Adjusted FCF **$14.7M**, −63% YoY, −77% QoQ — ~$11M tax-credit timing and ~$24M advancement-operation receivables (mostly Argentine installments) routed through a dedicated SPV expected to unwind [1][19].
- Cash $815.6M total; corporate cash $451.8M (+$27.3M QoQ). Buyback: only **$10.1M** repurchased in Q1 against a $300M authorisation running to March 2027 [1][2].

**Unit economics and concentration.** Net revenue retention **152%** in Q1, above 140% for four consecutive quarters; $329M of revenue from existing merchants versus $6.8M from new [20]. Top-10 merchants **62%** of revenue in Q1 [20], consistent with 61% for FY25 in the 20-F (62% in 2024, 60% in 2023) [21]. **This is the structural fragility.** Growth is almost entirely land-and-expand inside a concentrated book, which is why take rate compresses — large merchants step into lower unit-rate volume tiers. Management calls take rate an output metric managed to TPV [22]; that framing is correct on the economics and is also exactly what a company losing pricing power would say. Either way, one renegotiation with a top-5 merchant can move a quarter.

**Balance sheet / capital returns.** Net cash $803.95M, $2.74/share, ~19% of market cap [7]. Total debt $109.71M [7]. Dividend policy set at 30% of prior-year FCF — $57.2M ($0.1939/share) paid for 2026 [2]. $300M buyback with ~$290M unspent against a **79.6M-share float** [2][7] — my inference: a materially accelerated repurchase disclosed on this call would be a genuine surprise lever given how small the float is.

**What changed since the last print:** launch of "Stablecoin Full" across 44+ emerging markets (21 Apr 2026) [23]; addition to the Russell 2000 and Russell 3000 indexes effective 29 Jun 2026 [24]; three sell-side target raises including a UBS upgrade [15]. No merchant-win press release, no guidance update, no 6-K between 14 May and 13 Aug [5][6].

---

## 5. Positioning & options

All options figures computed by me from the CBOE delayed chain snapshot, spot reference $14.28–14.49, 2026-08-12/13 [8].

**Term structure — a large, clean earnings kink:**

| Expiry | ATM straddle (K=14) | % of spot | ATM IV |
| --- | --- | --- | --- |
| 2026-08-21 | $1.70 | 11.73–11.90% | ~0.95 |
| 2026-09-18 | $2.10 | 14.49% | ~0.58 |
| 2026-10-16 | $2.45 | 16.91% | ~0.50 |
| 2026-11-20 | $3.15 | 21.74% | ~0.53 |
| 2026-12-18 | $3.50 | 24.15% | ~0.52 |

Front expiry carries ~38 vol points over the next serial — a normal-to-large event premium. Front IV of ~95% versus 20-day realised of 31.0% and 60-day of 43.2% [3][8] means a straddle buyer needs roughly the historical mean move to break even.

**Skew — upside, not downside.** 21 Aug: $16 calls (Δ +0.267) IV 1.024 versus $13 puts (Δ ≈ −0.24) IV 0.991 — calls ~3 vol points *over* equidistant puts. ATM call 0.947 / ATM put 0.951, essentially flat. **This is the opposite of typical equity skew and says the marginal options buyer is paying up for upside.**

**Put/call.** 21 Aug expiry: volume P/C **0.45**, open-interest P/C **0.41**. Whole chain: volume P/C 0.44, open-interest P/C **0.16** (265,844 calls vs 42,512 puts). Front-expiry call OI is stacked at $14 (9,957), $15 (7,642), $16 (14,777), $17 (5,319) and $20 (7,022). The largest single lines in the whole chain are Dec-2026 $17 calls (74,479 OI) and Dec-2026 $13 calls (60,145 OI) — the pairing looks like a single large structured call spread rather than directional retail flow; I could not confirm its origin.

**Day-of flow (as captured, partial session).** 21 Aug $14 calls led with 894 contracts; the next four most-active lines were $14 puts (218), $13 puts (160), $17 calls (137) and $12 puts (109) — i.e. active two-way but call-led. Market Chameleon reported DLO total option open interest at 117,490 contracts against a 52-week average of 60,806, an OI percentile rank of **95.6%** [25], `snippet_only`, undated.

**Short interest — sources conflict; treat with care.**

| Source | Shares short | % float | % shares out | Days to cover | As-of |
| --- | --- | --- | --- | --- | --- |
| stockanalysis.com [7] | 16.54M | 20.77% | 5.64% | 6.60 | undated |
| MarketBeat (via snippet) [26] | 14.10M | 17.04% | — | 5.8 | undated |
| Finviz/other (via snippet) [26] | 14.96M | 19.82% | — | 11.25 | undated |
| StatMuse (via snippet) [27] | 13.31M | — | 4.54% | — | undated |

**Settlement date is a coverage gap** — Nasdaq's DLO short-interest page returned "Data is currently not available" [28]. The consistent reading is 13–17M shares short, high as a percentage of the small 79.6M free float but modest (4.5–5.6%) against 293M shares outstanding, with days-to-cover in the 5.8–6.6 range on the mainstream sources. **Borrow fee 0.29% APR with 2.3M shares available** per shortinteresttracker.com [26], `snippet_only` — a trivially cheap borrow, which argues against any squeeze mechanic.

**Run-up / drawdown into the print** (computed from [3]): $14.08 on 23 Jul → $15.31 on 3 Aug (+8.7%) → **$14.28 on 12 Aug (−6.7% off the high)**. 30-day change −3.8%. Year-to-date +1.0% ($14.14 at 2025-12-31). 52-week range $10.97–$15.83.

**My read on crowding:** long-biased and moderately crowded in options (OI percentile ~96th, chain P/C OI 0.16, positive call skew, three sell-side target raises in six weeks), but *not* crowded in the cash equity — the stock has bled 6.7% off its August high and is flat YTD. The equity has partially de-risked; the option book has not.

---

## 6. Sentiment & alt-data

**Analyst actions in the last six weeks — uniformly positive:**
- 1 Jul 2026: **UBS upgrade Neutral → Buy**, PT $16 → $20 (analyst Kaio Prato, citing "strong growth path" with improving operating leverage) [15][29].
- 24 Jul 2026: **Truist**, PT $15 → $17, Buy maintained [15].
- 31 Jul 2026: **Goldman Sachs**, PT $17 → $19, Buy maintained [15].
- Consensus PT drift is clearly upward: $17.75–$18.25 now [14][15], versus a low-$16s complex before July. One counter-datapoint surfaced in a snippet — an unnamed analyst cutting a target $0.30 to $17.35 citing opex caution [30], undated, `snippet_only`.

**Retail / social.** Stocktwits sentiment on DLO has been "bullish" to "extremely bullish" through 2026: "extremely bullish" with "extremely high" message volume in March 2026 after Q4 results, and again in May 2026 immediately after the Q1 miss, when retail flipped from neutral to extremely bullish within 24 hours on an "undervalued" framing; most recently described as "bullish" on "normal" message volume [31]. **A quantified 7/14/30-day sentiment series is a coverage gap** — Stocktwits' sentiment endpoint is auth-gated. Note the pattern: retail bought the last two selloffs, which is supporting colour only.

**Alt-data.** Weak by nature — dLocal is B2B infrastructure with no app, no consumer web funnel, and no reviewable storefront, so consumer alt-data proxies carry near-zero signal here. The one usable proxy is hiring: Revelio Labs reports **523 active job postings in 2026, +37.5% versus 2025**, new postings per month rising from 85 (2023) to 239 (2026), and headcount of ~1,345 as of March 2026 versus 871 in 2023 (+54.3%) [32], `snippet_only`. **This sits in direct tension with management's mid-May commitment to "no net new hiring for the rest of the year"** [1]. The Revelio data appears to predate or straddle that decision (headcount is dated March 2026), so it does not disprove the freeze — but it does mean I have no independent confirmation that the freeze is being executed, and the opex line is the single most important number in the print. Google Trends and web-traffic proxies were not sourced.

---

## 7. Forensics

**Form 4 activity — heavy, ongoing, but plan-based [33]:**
- **Sebastian Kanovich** (co-founder, director): converted 1,000,000 Class B into Class A and sold **1,000,000 Class A at $14.63 on 1 Jul 2026**; sold **25,700 at $15.50 on 7 Jul 2026**; sold **4,700 at $15.50 on 4 Aug 2026** [33][34][35]. All executed under a **Rule 10b5-1 plan adopted 26 Nov 2025** — i.e. pre-committed, non-discretionary, and adopted well before the current quarter. A Form 144 for a further 72,753 shares was filed [33].
- **William Rodney Pruett** (director): **bought 20,000 Class A shares at $11.85 on 29 May 2026** — an open-market, discretionary purchase two weeks after the −13% Q1 selloff [33]. This is the only discretionary insider transaction I found, and it is a buy.
- Two bona fide gift transfers of 884,249 shares each between the Hyman K Bielsky and Marietta Austin Bielsky revocable trusts on 27 May 2026 at $0.00 [33] — estate planning, no informational content.

**My read:** the Kanovich selling is large in share count but is mechanical 10b5-1 execution from a founder with a very large stake, running through both strength ($15.50) and the pre-earnings window. It is not a signal about this quarter. The Pruett buy is the only discretionary datapoint and it is directionally positive, though small and 11 weeks stale.

**Governance / audit.** Auditor is **Price Waterhouse & Co. S.R.L.** (PwC network member), audit report dated 24 Apr 2025 for the FY2025 20-F [21]. No restatement, no auditor change, no material-weakness disclosure found. Dual-class share structure with 49% insider ownership is a standing governance risk factor [7][21].

**Management changes.** Last CFO transition was March 2025 (Mark Ortiz stepped down for health reasons; Jeffrey Brown appointed interim) [36]. **I could not confirm whether a permanent CFO has since been appointed** — a coverage gap, and relevant because a still-interim CFO delivering a guidance defence carries less weight.

**8-K/6-K cadence.** Three 6-K filings in 2026: 18 Mar (Q4'25 results), 20 Apr (AGM/administrative), 14 May (Q1'26 results) [5]. Entirely routine; **no filing between 14 May and 13 Aug**, which rules out any pre-announcement, guidance revision or material-event signalling into the print.

**Legacy overhangs.** A 2023 Argentine government investigation into alleged improper FX transfers and a related US securities class action (IPO 2 Jun 2021 through 5 Jun 2023 class period) [37][38]. I found no 2026 developments on either. Not live for this print, but it is why the market is unusually sensitive to Argentina-related disclosure from this issuer.

**Filing-language shift.** One notable change: at Q1, management moved from generic optimism to specifying four named opex levers and an explicit hiring freeze [1]. That is a company putting a checkable commitment on the record. Q2 is the first checkpoint.

---

## 8. Macro & peer read-through

**Same-night crowding.** **Nu Holdings (NU) and StoneCo (STNE) both report AMC on 13 August 2026** [39][40]. Three LatAm fintechs printing into the same after-hours session means DLO's move can be amplified or contaminated by sector-level read-across, particularly from NU, which is far more widely held. NU's Q2 consensus is $0.20 EPS (+42.9% YoY) on $5.45B revenue (+48.7%) [39]. This materially raises the variance of DLO's reaction independent of DLO's own numbers.

**Peers that have already reported:**
- **MercadoLibre (5 Aug)** — revenue above $10B, +49.8% YoY, but operating margin **6.7% versus 6.9% expected**, down 550bp YoY; shares fell after hours on Brazil and Mexico cost pressure [41]. **This is the closest possible analogue to DLO's setup: LatAm volume is excellent, LatAm margin is not, and the market punished the margin.**
- **PagSeguro / PagBank (11 Aug)** — non-GAAP net income R$576M, non-GAAP diluted EPS +~10% YoY; credit portfolio +30.7% to R$5.1B; NPL 90+ up to 3.4%; deposits +15.1% to R$42.8B [42]. Brazilian consumer/SMB payments demand is intact.
- **Payoneer (6 Aug)** — revenue $274.3M, +5% YoY; GAAP net loss $(2.4)M versus $19.5M profit a year earlier; volume +15% to $23.7B with B2B +48%; company being acquired by Nuvei [43]. Cross-border volume growth is real but interest-income-dependent monetisation is deteriorating.
- **Adyen (H1 2026)** — net revenue €1,302.9M, +19% (+21% cc); **raised FY26 net revenue growth outlook to 21–23% from 20–22%** [44]. The premium global acquirer is accelerating, which supports the argument that the enterprise cross-border spend environment is healthy.

**Read-through, my inference:** the peer set says volume is strong and margins are the battleground, everywhere. That is precisely the axis on which DLO is most exposed, and MELI's post-print reaction is the cautionary template.

**FX and rates.** Argentina was **18% of DLO Q1'26 revenue** ($61.2M, its largest single-country line) [1] and was called out as the sequential swing factor with "funding costs declining materially" after Q4'25 election-related volatility [22]. Q2 2026 Argentine macro was benign: the crawling band is widening at lagged inflation rather than via discrete devaluation, consensus peso forecast ~1,700/USD by December (~17.4% annual depreciation), June inflation seen below 2% m/m, IMF projecting ~3.5% GDP growth [45][46]. Brazil (17% of revenue) is stable — the Fed held at 3.50–3.75% on 29 July (9-3 vote) and BRL firmed toward 5.10 [45]. My inference: **FX is a mild tailwind or neutral for Q2, not the headwind it was in Q4'25.** Note that constant-currency growth ran *below* reported in Q1 (63% cc vs 73% reported TPV) [1], meaning FX had been additive — a reversal would flatter the cc line but hurt the headline.

**Factor regime.** DLO joined the Russell 2000 on 29 June 2026 [24], adding passive small-cap ownership. 5-year beta 0.87 [7]. Institutional ownership only 22.55% against 49.01% insider ownership [7] — a thin, retail-and-index-heavy register on a 79.6M float, which mechanically amplifies post-earnings gaps.

---

## 9. Bull case / bear case / base case

**Bull.** dLocal is a compounding volume machine trading at 15.4x forward earnings with $2.74/share of net cash — 19% of the market cap — and a $300M buyback that is 97% unspent against a 79.6M float [7][2][1]. TPV has run above 50% growth for six straight quarters and grew 73% in Q1 against a guide of 50–60%, so a **TPV guidance raise is arithmetically easy** [1][2]. Net revenue retention of 152% and four straight quarters above 140% mean the revenue base is self-expanding [20]. Argentina — the largest revenue country at 18% and the Q4'25 problem child — normalised in Q1 and faced a benign Q2 macro [1][22][45]. The working-capital drag that crushed Q1 FCF (~$11M tax credits, ~$24M advancement receivables in an SPV) is designed to unwind, so a large FCF snap-back is a live headline surprise [19]. UBS, Truist and Goldman all raised targets in the six weeks *before* this print [15] — analysts do not raise into an expected blow-up. And the stock has already surrendered 6.7% from its 3 August high [3], so some disappointment is pre-paid. Positive call skew and 96th-percentile option open interest [8][25] mean an upside surprise gets amplified by dealer hedging into a very small float.

**Bear.** The two most recent quarters in which record TPV was paired with soft unit economics were sold −6.8% and −13.0%; volume records earn nothing from this market [1][3]. Gross profit over TPV has fallen 21bp year-on-year to 0.84% and the Q1 gross margin was 35% versus 39% [1]. The FY26 operating-profit guide requires **$75.9–79.5M per quarter across Q2–Q4 against $52.8M in Q1 and $62.7M in Q4'25** — and management explicitly located the leverage in the *second half*, meaning Q2 is structurally the weakest quarter for exactly the metric that decides the reaction [1][2]. Opex grew 58% YoY in Q1 and came in above management's own expectation [1]; Revelio shows job postings up 37.5% year-on-year with no independent confirmation that the mid-May hiring freeze is executing [32]. The revenue-beat magnitude has collapsed from +15%/+10%/+10%/+5% to **+0.45%** [10] — the Street has caught up, so the mechanism that produced the +31% August 2025 move is gone. Top-10 merchant concentration is 62% and effectively all growth is expansion inside that book [20][21], so pricing power sits with the customer, which is what the take-rate chart shows. MELI, the closest analogue, was sold last week on precisely a 20bp operating-margin miss [41]. And options positioning is one-sided long — chain-wide put/call OI of 0.16 with positive call skew [8] — so there is no protective bid to cushion a miss.

**Base case (my read).** dLocal beats or meets on revenue and TPV — likely $365M+ and $15–16.5B — reports gross profit near $122–128M with take rate around 0.78–0.82%, and reaffirms FY26 guidance while probably raising the TPV range. Operating profit lands around $58–66M: better than Q1, but short of the $76–80M run-rate the FY guide demands, leaving the H2 bridge steep. The call then decides the reaction, and specifically whether management can show a hard opex number — flat or down sequentially — proving the freeze is real. I put slightly better than even odds on the print itself being fine and slightly worse than even odds on the *reaction*, because the market has punished this precise "great volume, leverage next half" combination twice in the last three quarters. Wide dispersion: implied 11.9% is roughly the right magnitude and I would not fade it in either direction on conviction.

---

## 10. What would flip the consensus view

The most credible reversal is **an operating-profit and opex print that arrives a quarter early.** Concretely: Q2 operating profit at or above **~$70M** with opex growth decelerating from +58% to under ~30% year-on-year, accompanied by an explicit *raise* to the FY26 operating-profit growth range (from 27.5–32.5% to something starting with a 3), and a disclosed acceleration of the buyback — say $50M+ repurchased in Q2 against the ~$290M remaining authorisation on a 79.6M float [1][2][7]. That combination would demolish the bear thesis in one move, because it converts the H2 leverage story from a promise into evidence, and it is exactly the configuration that produced the +9.4% Q4'25 reaction. It is not the likeliest outcome — management guided the leverage to H2 — but it is entirely within reach if the mid-May cost actions bit faster than modelled, and the market is not positioned for it in the cash equity.

The mirror-image flip: gross profit / TPV printing below **0.76%** with any softening of the FY26 gross-profit or operating-profit ranges. That would be read as the concentrated top-10 merchant book repricing dLocal rather than dLocal choosing to scale, and given 62% concentration and 152% NRR there is no offsetting new-logo story to point at [20][21]. In that scenario the −13% Q1 reaction is the template, not the floor.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **IV rank / IV percentile unavailable** | Market Chameleon, OptionCharts and OptionSlam are all member-gated. I can show front-month IV (~95%) versus 20d/60d realised (31%/43%) and the term-structure kink, but cannot say where current IV sits in its own 52-week distribution — so I cannot judge whether the event premium is historically rich or cheap for this name. |
| **Short-interest settlement date unknown; four sources disagree** | Nasdaq's DLO short-interest page returns "Data is currently not available" [28]. Estimates span 13.31M–16.54M shares and 17.0%–20.8% of float, with days-to-cover from 5.8 to 11.25. Recency is load-bearing for positioning and I have none of it. |
| **30/60-day estimate revision detail** | Only a 90-day count (0 up / 1 down near-quarter, 2 up / 0 down FY26) from a Seeking Alpha snippet [16]. Whether the Street trimmed Q2 in the last month is directly relevant to how beatable $0.191 is. |
| **No published whisper number** | Cannot quantify the buy-side bar above the $0.18–$0.20 sell-side range. Given three target raises in six weeks, the buy-side bar is plausibly above consensus, but I have no evidence for it. |
| **Consensus EPS conflicts across providers** | $0.191 (Investing.com), $0.18 (TradingKey), $0.20 (WallStreetZen). On a $14 stock a 2c spread is the difference between a beat and a miss headline. |
| **Q2'26 gross-profit and operating-profit consensus not sourced** | This is the most important gap in the dossier. The metric that decides the reaction has no sourced Street number — my $125M gross profit / $58–66M operating profit expectations are inference from the guidance arithmetic, not consensus. |
| **Permanent CFO status unconfirmed** | Last confirmed datapoint is Jeffrey Brown as *interim* CFO from March 2025 [36]. An interim CFO defending a steep H2 guidance bridge is a weaker signal than a permanent one. |
| **Whether the mid-May hiring freeze is executing** | Revelio shows postings +37.5% YoY and headcount dated March 2026 [32] — pre-freeze. No independent read on Q2 headcount. Opex is the swing variable and I cannot triangulate it. |
| **Quantified Stocktwits sentiment score and 7/14/30-day trend** | Auth-gated; only qualitative tone sourced [31]. |
| **Google Trends, web traffic, app ranks** | Not sourced. Low signal value for B2B payments infrastructure, but the gap is real. |
| **Origin of the Dec-26 $17c / $13c open-interest block (74,479 / 60,145)** | Largest lines in the chain by a wide margin; could be a hedge, a structured note, or a directional position. Unidentified. |
| **Q2'26 buyback execution to date** | Only $10.1M of $300M used in Q1 [1]. Q2 usage is unknown and would change both the EPS math and the float. |
| **Press-reported earnings reactions irreconcilable with the price series** | Bloomberg/Investing.com cite a −28.7%/+49.4% range and a 15.2% median [9] against my computed 8-quarter range of −13.0%/+31.3% and 9.87% median [3]. Methodologies differ; I used close-to-close throughout. |
| **Fetch-blocked / unavailable domains** | tipranks.com (403), sec.gov EDGAR full-text browse for the Q4'25 exhibit at one URL (403), zacks.com (bot-detection), finance.yahoo.com/quote/DLO/analysis (503), optioncharts.io and marketchameleon.com (JS-gated), nasdaq.com short-interest (no data), fintel.io and shortinteresttracker.com (snippet only). Yahoo v7 options endpoint required a crumb — substituted the CBOE delayed chain. |

---

## 12. Sources

1. [dLocal Reports First Quarter 2026 Financial Results — GlobeNewswire, 14 May 2026](https://www.globenewswire.com/news-release/2026/05/14/3295379/0/en/dlocal-reports-first-quarter-2026-financial-results.html) and [the same release as SEC Form 6-K exhibit](https://www.sec.gov/Archives/edgar/data/0001846832/000184683226000019/ex993dlocal1q26er.htm) — Q1'26 TPV, revenue by geography, gross profit, take rate, operating profit, net income, EPS, FCF, cash, buyback, opex, FY26 guidance reaffirmation, H2 opex levers, hiring freeze.
2. [dLocal Reports 2025 Fourth Quarter Financial Results — SEC Form 6-K exhibit, 18 Mar 2026](https://www.sec.gov/Archives/edgar/data/1846832/000207097926000110/a991dlocal4q25_earningsres.htm) — FY25 and Q4'25 TPV/revenue/gross profit/operating profit/net income/EPS/FCF, FY25 bases, $300M buyback authorisation, dividend policy and amount, verbatim FY26 guidance.
3. [Yahoo Finance chart API, DLO daily OHLCV, 3-year history](https://query1.finance.yahoo.com/v8/finance/chart/DLO?range=3y&interval=1d) — all historical earnings-reaction moves, spot, run-up/drawdown, realised vol, 52-week range, YTD. Retrieved 2026-08-13.
4. [dLocal to Report Second Quarter 2026 Financial Results — GlobeNewswire, 5 Jun 2026](https://www.globenewswire.com/news-release/2026/06/05/3307624/0/en/dLocal-to-Report-Second-Quarter-2026-Financial-Results.html) — event date, AMC session, 17:00 ET call time, fiscal period. Primary event confirmation.
5. [SEC EDGAR filing list, dLocal Ltd (CIK 0001846832)](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001846832&type=6-K&dateb=&owner=include&count=40) — 6-K cadence in 2026 (18 Mar, 20 Apr, 14 May); absence of filings 14 May–13 Aug.
6. [dLocal Investor Relations, News & Events](https://dlocal.gcs-web.com/news-and-events/) — company news list May–Aug 2026; no pre-announcement.
7. [stockanalysis.com — DLO statistics](https://stockanalysis.com/stocks/dlo/statistics/) — spot $14.28 (2026-08-12 close), pre-market $14.50 (2026-08-13 07:48 ET), market cap, shares outstanding, float, insider/institutional ownership, short interest, days to cover, cash, debt, net cash, beta, P/E.
8. [CBOE delayed options quotes, DLO](https://cdn.cboe.com/api/global/delayed_quotes/options/DLO.json) — full chain used to compute ATM straddle/implied move, IV term structure, skew, put/call volume and OI, largest OI lines, iv30. Retrieved 2026-08-13.
9. [Dlocal options signal 11% move on upcoming earnings release — Investing.com, 6 Aug 2026](https://www.investing.com/news/stock-market-news/dlocal-options-signal-11-move-on-upcoming-earnings-release-93CH-4842973) — published 11% Bloomberg-derived implied move; historical implied-vs-actual statistics (flagged as methodologically inconsistent with my close-to-close series).
10. [Dlocal (DLO) Earnings Date & Report — Investing.com](https://www.investing.com/equities/dlocal-earnings) — Q2'26 consensus EPS $0.191 and revenue $364.65M; eight-quarter actual-vs-forecast EPS and revenue table with dates.
11. [dLocal Stock Rallies After Q2 Earnings Report — Benzinga, Aug 2025](https://www.benzinga.com/markets/earnings/25/08/47109043/dlocal-stock-rallies-after-q2-earnings-report-heres-why) — reported +15.48% extended-hours move on 13 Aug 2025; used only to flag the methodology discrepancy.
12. [Dlocal Ltd (DLO) Earnings Forecast — TradingKey](https://www.tradingkey.com/markets/stocks/nasdaq-dlo/earnings) — alternative Q2'26 EPS estimate $0.18; quarterly EPS surprise percentages. `snippet_only`.
13. [Dlocal Stock Forecast & Predictions — WallStreetZen](https://www.wallstreetzen.com/stocks/us/nasdaq/dlo/stock-forecast) — alternative Q2'26 EPS estimate $0.20; FY26 EPS $0.84 range $0.74–$0.94; 1Y PT $18.00. `snippet_only`.
14. [DLocal (DLO) Stock Forecast & Analyst Price Targets — stockanalysis.com](https://stockanalysis.com/stocks/dlo/forecast/) — consensus PT $18.25, range $14.50–$21.00, 10 analysts, rating breakdown, FY26/FY27 revenue and EPS forecasts.
15. [DLocal (DLO) Stock Forecast and Price Target — MarketBeat](https://www.marketbeat.com/stocks/NASDAQ/DLO/forecast/) — consensus PT $17.75, 8 analysts, rating breakdown, and the dated 90-day rating/target change table (Goldman 31 Jul, Truist 24 Jul, UBS 1 Jul).
16. [DLO estimate revisions — Seeking Alpha](https://seekingalpha.com/symbol/DLO/earnings/revisions) — 90-day EPS revision counts (0 up / 1 down near quarter; 2 up / 0 down FY26); FY26 consensus $0.85 on $1.5B. `snippet_only`.
17. [DLocal (NasdaqGS:DLO) Stock Forecast & Analyst Predictions — Simply Wall St](https://simplywall.st/stocks/us/diversified-financials/nasdaq-dlo/dlocal/future) — FY26 EPS estimate reported falling $0.828 → $0.72; undated, not relied upon. `snippet_only`.
18. [dLocal Reports 2025 Second Quarter Financial Results — GlobeNewswire, 13 Aug 2025](https://www.globenewswire.com/news-release/2025/08/13/3132983/0/en/dLocal-Reports-2025-Second-Quarter-Financial-Results.html) — Q2'25 base: TPV $9.2B, revenue $256.5M, gross profit $98.9M, FCF $48M.
19. [DLocal (DLO): Q1 2026 Earnings Review — MVC Investing](https://mvcinvesting.substack.com/p/dlocal-dlo-q1-2026-earnings-review) — working-capital detail (~$11M tax credits, ~$24M advancement receivables via SPV), take-rate driver (installment mix / volume tiers), opex corrective actions, H2 leverage framing.
20. [DLocal Q1 2026 Earnings Call Transcript — Benzinga](https://www.benzinga.com/insights/news/26/05/52586148/dlocal-q1-2026-earnings-call-transcript) — NRR 152%, four consecutive quarters above 140%, $329M existing-merchant vs $6.8M new-merchant revenue, top-10 merchants 62% of revenue / $209M.
21. [dLocal Ltd Form 20-F, FY2025](https://www.sec.gov/Archives/edgar/data/1846832/000207097926000113/dlo-20251231.htm) — auditor Price Waterhouse & Co. S.R.L. (PwC network), top-10 merchant concentration 61% (2025) / 62% (2024) / 60% (2023), risk factors.
22. [DLocal (DLO) Q1 2026 Earnings Transcript — The Motley Fool, 15 May 2026](https://www.fool.com/earnings/call-transcripts/2026/05/15/dlocal-dlo-q1-2026-earnings-transcript/) — take rate as an "output metric", Argentina recovery and funding costs, Brazil seasonality, merchant-expansion examples, $300M buyback commentary, opex $62M ex-item.
23. [dLocal launches Stablecoin Full — dLocal press release, 21 Apr 2026](https://www.dlocal.com/press-releases/dlocal-launches-the-most-seamless-stablecoin-integration-for-payments-in-emerging-markets/) — product launch across 44+ emerging markets; change since last print.
24. [dLocal added to membership of US small-cap Russell 2000 Index — GlobeNewswire, 26 Jun 2026](https://www.globenewswire.com/news-release/2026/06/26/3318486/0/en/dlocal-added-to-membership-of-us-small-cap-russell-2000-index.html) — index inclusion effective 29 Jun 2026.
25. [DLO Open Interest Trends — Market Chameleon](https://marketchameleon.com/Overview/DLO/OpenInterestTrends/) — total option OI 117,490 vs 52-week average 60,806, OI percentile rank 95.6%. `snippet_only`, undated.
26. [DLOCAL LTD (DLO) Short Interest — shortinteresttracker.com](https://shortinteresttracker.com/stock/DLO) and [MarketBeat short interest](https://www.marketbeat.com/stocks/NASDAQ/DLO/short-interest/) — borrow fee 0.29% APR, 2.3M shares available to borrow; alternative short-interest and days-to-cover figures. `snippet_only`, undated.
27. [What Is The Short Interest In Dlocal — StatMuse](https://www.statmuse.com/money/ask/what-is-the-short-interest-in-dlocal) — 13.31M shares short, 4.54% of outstanding. `snippet_only`, undated.
28. [DLocal Limited Class A Short Interest — Nasdaq](https://www.nasdaq.com/market-activity/stocks/dlo/short-interest) — returned "Short interest is currently not available"; documents the settlement-date gap.
29. [UBS upgrades DLocal stock rating to Buy on growth outlook — Investing.com, 1 Jul 2026](https://www.investing.com/news/analyst-ratings/ubs-upgrades-dlocal-stock-rating-to-buy-on-growth-outlook-93CH-4769554) — upgrade Neutral → Buy, PT $16 → $20, analyst Kaio Prato, rationale.
30. [dLocal (NASDAQ: DLO) delivers record 2025 growth, cash returns and 2026 outlook — StockTitan](https://www.stocktitan.net/sec-filings/DLO/6-k-d-local-ltd-current-report-foreign-issuer-1b0ba8df5db3.html) — FY26 guidance summary and a reported $0.30 price-target cut to $17.35 on opex caution. `snippet_only`, undated for the PT cut.
31. [DLO Stock Tumbles On Q1 Profit Miss: Retail Turns Bullish On 'Undervalued' Stock — Stocktwits](https://stocktwits.com/news-articles/markets/equity/dlo-stock-tumbles-on-q1-profit-miss-retail-turns-bullish-on-undervalued-stock/cZXlYOOReSC) and [DLO sentiment page](https://stocktwits.com/symbol/DLO/sentiment) — qualitative retail tone March/May 2026 and most recent "bullish on normal volume". `snippet_only`; quantitative series auth-gated.
32. [DLocal Number of Employees 2026 — Revelio Labs](https://www.reveliolabs.com/companies/dlocal/employees) — 523 active job postings in 2026 (+37.5% YoY), 239 new postings/month, headcount ~1,345 as of March 2026 (+54.3% from 2023). `snippet_only`.
33. [dLocal Form 4 insider filings — StockTitan](https://www.stocktitan.net/sec-filings/DLO/form-4-d-local-ltd-insider-trading-activity-b17e6c31a3cc.html) — Kanovich 1,000,000-share conversion and sale at $14.63 (1 Jul 2026) under a 10b5-1 plan adopted 26 Nov 2025; [director purchase 20,000 shares at $11.85, 29 May 2026](https://www.stocktitan.net/sec-filings/DLO/form-4-d-local-ltd-insider-trading-activity-67059acca752.html); [884,249-share trust gifts, 27 May 2026](https://www.stocktitan.net/sec-filings/DLO/form-4-d-local-ltd-insider-trading-activity-e068d9f992f3.html); [Form 144 for 72,753 shares](https://www.stocktitan.net/sec-filings/DLO/144-d-local-ltd-sec-filing-efc041f48beb.html).
34. [DLocal Director Sebastian Kanovich Sells 25,700 Shares for $398,350 — The Motley Fool, 14 Jul 2026](https://www.fool.com/coverage/filings/2026/07/14/dlocal-director-sebastian-kanovich-sells-25-700-shares-for-usd398-350-is-the-stock-a-sell-too/) — 7 Jul 2026 sale at $15.50 under the 10b5-1 plan.
35. [Insider Selling: DLocal (NASDAQ:DLO) Director Sells 4,700 Shares — Daily Political, 11 Aug 2026](https://www.dailypolitical.com/2026/08/11/insider-selling-dlocal-nasdaqdlo-director-sells-4700-shares-of-stock.html) — 4 Aug 2026 sale of 4,700 shares at $15.50.
36. [dLocal Announces CFO Transition due to Health Reasons — GlobeNewswire, 25 Mar 2025](https://www.globenewswire.com/news-release/2025/03/25/3049160/0/en/dLocal-Announces-CFO-Transition-due-to-Health-Reasons.html) — Mark Ortiz departure, Jeffrey Brown appointed interim CFO.
37. [DLocal Limited (DLO) Faces Government Investigation and Lawsuit Over Foreign Exchange Regulations — GlobeNewswire, 6 Nov 2023](https://www.globenewswire.com/news-release/2023/11/06/2774309/32716/en/DLocal-Limited-DLO-Faces-Government-Investigation-and-Lawsuit-Over-Foreign-Exchange-Regulations.html) — 2023 Argentine investigation background.
38. [DLocal Limited securities fraud class action — Kessler Topaz](https://www.ktmc.com/new-cases/dlocal-limited/) — class period 2 Jun 2021 – 5 Jun 2023, allegations.
39. [Should You Buy, Hold or Sell Nu Holdings Stock Before Q2 Earnings? — Yahoo Finance](https://sg.finance.yahoo.com/news/buy-hold-sell-nu-holdings-143500870.html) and [NU Q2 2026 Earnings Report — MarketBeat](https://www.marketbeat.com/earnings/reports/2026-8-13-nu-holdings-ltd-stock/) — NU reports AMC 13 Aug 2026; consensus $0.20 EPS on $5.45B revenue.
40. [StoneCo Ltd. to Announce Second Quarter 2026 Financial Results on August 13th, 2026 — StockTitan](https://www.stocktitan.net/news/STNE/stone-co-ltd-to-announce-second-quarter-2026-financial-results-on-kqzc2qyy71u9.html) — STNE reports AMC 13 Aug 2026.
41. [MercadoLibre, Inc. Reports Second Quarter 2026 Financial Results — Business Wire, 5 Aug 2026](https://www.businesswire.com/news/home/20260805925866/en/MercadoLibre-Inc.-Reports-Second-Quarter-2026-Financial-Results) and [MercadoLibre Q2: Revenue Tops US$10 Billion, Shares Slip — Rio Times](https://www.riotimesonline.com/mercadolibre-q2-2026-revenue-tops-10-billion/) — revenue +49.8%, operating margin 6.7% vs 6.9% expected, shares fell after hours on Brazil/Mexico cost pressure.
42. [PagSeguro Digital Posts Strong Q2 2026 Profit on Banking and Credit Growth — TipRanks, 11 Aug 2026](https://www.tipranks.com/news/company-announcements/pagseguro-digital-posts-strong-q2-2026-profit-on-banking-and-credit-growth) — non-GAAP net income R$576M, EPS +~10%, credit +30.7%, NPL 90+ 3.4%, deposits +15.1%.
43. [Payoneer Reports Second Quarter 2026 Financial Results — PR Newswire, 6 Aug 2026](https://www.prnewswire.com/news-releases/payoneer-reports-second-quarter-2026-financial-results-302844544.html) — revenue $274.3M +5%, net loss $(2.4)M, volume +23.7B +15%, B2B +48%, Nuvei acquisition.
44. [Adyen publishes H1 2026 financial results — Adyen](https://www.adyen.com/press-and-media/adyen-publishes-h1-2026-financial-results-3wjne) and [Adyen Raises 2026 Revenue Outlook After Strong H1 Results](https://www.globalbankingandfinance.com/adyen-lifts-2026-revenue-outlook-strong-first-half/) — net revenue €1,302.9M +19% (+21% cc), FY26 growth outlook raised to 21–23%.
45. [Argentina's fragile monetary framework risks renewed volatility — PIIE, 2026](https://www.piie.com/blogs/realtime-economics/2026/argentinas-fragile-monetary-framework-risks-renewed-volatility) and [BRL to USD guide — Rio Times](https://www.riotimesonline.com/brl-to-usd-understanding-the-brazilian-real-exchange-rate-2026-guide/) — Argentine crawling-band mechanics, peso ~1,700/USD December forecast (~17.4% depreciation), Fed hold at 3.50–3.75% on 29 Jul, BRL toward 5.10.
46. [Argentina's June Inflation Seen Dipping Below 2% for First Time — Rio Times](https://www.riotimesonline.com/argentina-june-inflation-below-2-percent-2026/) and [Argentina Inflation Forecast 2026: REM Raises Outlook to 29.1%](https://www.riotimesonline.com/argentina-inflation-forecast-29-percent-rem-2026/) — Q2'26 Argentine inflation and macro backdrop.

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such.*
