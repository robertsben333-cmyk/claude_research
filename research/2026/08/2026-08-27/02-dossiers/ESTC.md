# ESTC — Elastic N.V.

**What this print is about.** Elastic reports Q1 FY2027 (quarter ended 31 July 2026) after the close on Thursday 27 August 2026, with the call at 17:00 ET [1]. Management set the bar itself on 28 May 2026: Q1 revenue of $469–470M (+13.1% y/y at the midpoint, the *lowest* growth quarter of FY27 by design) and non-GAAP EPS of $0.57–0.59, which is *down* ~3% y/y [2]. The Street sits exactly on that midpoint — consensus revenue $469.49M and EPS $0.58 [7] — so there is no cushion in the number and no scepticism discount either. The whole print therefore turns on one thing: whether Elastic Cloud re-accelerates sequentially after posting its **first-ever quarter-over-quarter decline** in Q4 FY26 ($217.4M vs $218.0M in Q3) [2][10], and whether cRPO growth supports management's "back-half weighted FY27" story. Complicating everything is the setup: the stock is up **+35.1% since 22 July 2026** ($58.68 → $79.25) [3], has already given back ~9.3% from its 19 Aug close of $87.34 [3], and trades ~6% below the stockanalysis.com consensus target of $84.41 [6] and *above* two other published consensus targets ($77.41 [46], $71.40 [47]). Three months ago Elastic also announced a 7% workforce cut *after* it set this guidance [18][19] — un-guided cost savings that make an EPS beat more likely but tell you nothing about demand. Triage's framing ("small/mid-cap growth SaaS with a history of sharp double-digit post-earnings moves on billings/cloud-growth surprises") is **correct and if anything understated** — realised one-day moves have averaged 14.2% absolute over eight quarters, with a −26.5% and two +14.8% prints in the set [3].

---

## 1. Event & anchors

`event_confirmed: true`

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Earnings date | Thursday **2026-08-27** | press release dated 2026-08-13 | [1] |
| Session | **amc** — after the U.S. market close | — | [1] |
| Call time | 14:00 PT / **17:00 ET** | — | [1] |
| Fiscal period | **Q1 FY2027**, quarter ended 2026-07-31 | — | [1] |
| Date changed / pre-announced? | No. No 8-K filed since 2026-06-24; no pre-announcement | EDGAR index pulled 2026-08-27 | [13] |
| Spot | **$79.25** (regular-session close) | 2026-08-26T20:00Z | [3]; corroborated by Nasdaq "LAST TRADE $79.25 (AS OF AUG 27, 2026)" [44] |
| Prior close | $80.40 (2026-08-25); day move −1.43% | 2026-08-26 | [3] |
| Market cap | **$8.24B** | 2026-08-26 | [5] |
| Shares outstanding | 103.95M (stockanalysis); 104,751,470 on the FY26 10-K cover (2026-04-30) | 2026-08-26 / 2026-04-30 | [5] / [16] |
| Enterprise value | $7.46B (net cash $778.7M: $1.37B cash vs $591.6M debt) | 2026-08-26 | [5] |
| Forward P/E | 24.43 | 2026-08-26 | [5] |
| Beta (5Y) | 0.97 | 2026-08-26 | [5] |
| 52-week high / low | $96.07 / $42.05 | 2026-08-26 | [3] |
| **Event-implied one-day move (derived)** | **≈12.9%** (range 12–14.5% on bid/ask; 1SD ≈16.2%) | CBOE quotes as of 2026-08-26T19:59:59 ET-close | [4], my calculation — see method below |
| Front ATM straddle (Sep-18 $80) | $13.70 mid = **17.29% of spot** (bid-side 16.5%, ask-side 18.0%) | 2026-08-26 close | [4] |
| ATM IV term structure | Sep-18 **85.8%** → Oct-16 70.2% → Nov-20 66.8% → Jan-27 65.3% | 2026-08-26 | [4] |
| CBOE 30-day IV (iv30) | **79.85%** (iv30 change 0.0) | 2026-08-26 | [4] |
| IV rank / percentile | **unavailable** — see coverage gaps | — | — |

**Implied-move method (my calculation, not a quoted figure).** Elastic has **no weekly options** in the CBOE delayed-quote chain; the nearest listed expiry after the event is the 2026-09-18 monthly, 22 calendar days out [4]. A raw straddle/spot of 17.29% therefore badly overstates the one-day event move. Using the standard two-expiry variance decomposition — σ₁²T₁ = σ_d²T₁ + E² and σ₂²T₂ = σ_d²T₂ + E², with σ₁ = 85.8% (Sep-18 ATM), σ₂ = 70.2% (Oct-16 ATM), T₁ = 22/365, T₂ = 50/365 — gives an event 1-standard-deviation jump **E ≈ 16.2%** and an implied residual diffusive vol of ~54.9%. The straddle-equivalent expected absolute move (0.798 × E) is **≈12.9%**. Cross-check: stripping 22 days of 54.9% diffusive vol out of the $13.70 straddle in variance terms gives ≈13.5%. I am publishing **12.9%** as the headline with a 12–14.5% band. This is derived, not quoted — treat it as ±1.5pt.

*(I found a published "ESTC options imply 10.7%" note but it is dated **29 August 2024** and references an $11.02 move on a ~$103 stock [not current]; I discarded it rather than pass it off as live. Same for a Yahoo/Zacks "options traders" piece dated 5 June 2024.)*

### Realised one-day earnings moves (close-to-close, day after the AMC print)

Computed from Yahoo daily closes [3]; independently corroborated for the last four quarters by TipRanks' reaction column [40].

| Report date | Quarter | Prior close | Reaction close | **1-day move** | Open→close behaviour |
| --- | --- | --- | --- | --- | --- |
| 2024-08-29 | Q1 FY25 | $103.64 | $76.19 | **−26.49%** | — |
| 2024-11-21 | Q2 FY25 | $94.13 | $108.03 | **+14.77%** | — |
| 2025-02-27 | Q3 FY25 | $101.28 | $116.36 | **+14.89%** | — |
| 2025-05-29 | Q4 FY25 | $92.03 | $80.87 | **−12.13%** | — |
| 2025-08-28 | Q1 FY26 | $87.79 | $85.06 | **−3.11%** | **opened +7.5% at $94.37, closed −3.11% — full gap reversal** |
| 2025-11-20 | Q2 FY26 | $82.08 | $70.04 | **−14.67%** | opened −11.6%, closed −14.7% (extended) |
| 2026-02-26 | Q3 FY26 | $61.58 | $52.07 | **−15.44%** | opened −10.5%, closed −15.4% (extended) |
| 2026-05-28 | Q4 FY26 | $57.61 | $64.70 | **+12.31%** | **opened −6.4% at $53.91 on the weak Q1 guide, closed +12.31% — ~+20% open-to-close reversal** |

- **Mean |move| (8q): 14.23%. Median |move| (8q): 14.72%. Max |move|: 26.49%.**
- Last 6 quarters: mean |move| 12.09%, median |move| 13.49%, max 15.44%.
- **Up/down pattern (8q, oldest→newest): D, U, U, D, D, D, D, U — 3 up / 5 down.** Last 6: 2 up / 4 down.
- **Gap-fade risk is real and documented.** In two of the last four prints the initial after-hours/opening reaction fully reversed by the close. On 28 May 2026 Investing.com reported shares "fell 8.8%" after hours on the light Q1 guide [8]; the stock closed the next day **+12.31%** [3]. On 28 Aug 2025 the stock gapped up 7.5% and closed down 3.1% [3]. **Anyone trading the after-hours print in this name has been wrong half the time.**

---

## 2. The bar

**Consensus for Q1 FY27** (Zacks-sourced, article dated 2026-08-24) [7]:

| Metric | Consensus | y/y | Company guidance (2026-05-28) [2] |
| --- | --- | --- | --- |
| Non-GAAP EPS | **$0.58** | **−3.3%** | $0.57–0.59 |
| Total revenue | **$469.49M** | +13.1% | $469–470M (+13.1% mid) |
| Subscription revenue | $442.32M | +13.8% | — |
| **Elastic Cloud (subscription)** | **$229.23M** | **+17.1%** | not separately guided |
| Other subscription | $213.08M | +10.5% | — |
| Professional services | $27.18M | +1.8% | — |
| Sales-led subscription revenue | — | — | $392–393M (+15.9% mid, +15.6% cc) |
| Non-GAAP operating margin | — | — | ~14.0% (vs 15.7% in Q1 FY26 [11]) |
| Diluted shares assumed | — | — | 106.0–107.0M |

**The Street is sitting exactly on guidance, at every line.** Revenue consensus $469.49M vs guidance midpoint $469.5M. EPS consensus $0.58 vs guidance midpoint $0.58. FY27 consensus revenue $1.99B and EPS $3.24 (29 analysts) vs guidance $1.985–2.000B and $3.21–3.29 [6][2]. There is **no embedded beat and no embedded haircut**. That is unusual and important: it means the sell-side has done no independent work above the guide, and the buy-side bar is therefore whatever the whisper is, not the printed consensus.

**Revisions.** Zacks reports the Q1 consensus EPS "adjusted upward by 18.2% over the past 30 days" to $0.58 [7]. **I do not read this as genuine revision momentum.** Guidance of $0.57–0.59 was issued on 28 May 2026, three months before the 30-day window opened; a +18.2% move from ~$0.49 to $0.58 inside the last month is far more consistent with a stale consensus mechanically catching up to a long-published guide than with analysts marking up their models. I could not source clean 60/90-day revision series — see coverage gaps. *(Inference, mine.)*

**Guidance vs Street history (revenue beat vs own guidance midpoint):**

| Quarter | Guide midpoint | Actual | Beat | Next-day move |
| --- | --- | --- | --- | --- |
| Q3 FY26 | $438M [12] | $450M [10] | **+2.7%** | −15.44% |
| Q4 FY26 | $446M [10] | $451M [2] | **+1.1%** | +12.31% |

Rosenblatt, previewing on 26 Aug 2026, expects "an in-line to marginal beat for the quarter ending July 31, compared to a 1% beat in the fourth quarter" [23]. Management said on the Q4 call that it beat guidance "across every key metric" for a seventh consecutive quarter [2].

**Whisper number: unavailable.** EarningsWhispers is gated and returned no figure [not sourced]. Working from the beat pattern above, a 1–2.7% revenue beat implies **~$474–482M**, and the layoff savings (below) plausibly support **$0.62–0.68** on EPS. That is my arithmetic on sourced inputs, not a published whisper.

**What Elastic has to deliver just to hold the stock flat (my read).** After a +35% run, in-line is not enough. The flat-line bar is, in my judgement: (a) Q1 revenue ≥ ~$476M (≈1.5% beat), (b) **Elastic Cloud ≥ ~$230M**, i.e. a clean sequential rebound off $217.4M, (c) cRPO growth held at ≥18–20% y/y (Q1 FY26 cRPO was $956.5M, +18% [11]; Q4 FY26 cRPO $1.203B, +20% [2]), and (d) **an explicit raise to the FY27 revenue range**, not merely "reiterate." Absent (d), the stock has to justify a 35% re-rating on a quarter management already told the market would be its weakest.

---

## 3. The one metric that matters

**Elastic Cloud revenue and, specifically, its sequential trajectory.**

Not EPS. EPS is guided to *decline* y/y and is the line most likely to be flattered by the June restructuring, so a beat there carries almost no information.

The cloud sequence, all from primary 8-K/press-release sources:

| Quarter | Elastic Cloud revenue | y/y | q/q |
| --- | --- | --- | --- |
| Q1 FY26 (Jul-25) | $195.8M [11] | +24% | — |
| Q2 FY26 (Oct-25) | $205.7M [12] | +22% | +5.1% |
| Q3 FY26 (Jan-26) | $218.0M [10] | +21% | +6.0% |
| Q4 FY26 (Apr-26) | **$217.4M** [2] | +20% | **−0.3%** ← first sequential decline |
| **Q1 FY27 (Jul-26) consensus** | **$229.23M** [7] | **+17.1%** | **+5.4%** |

Stifel flagged exactly this in its 18 Aug note: "Q4 cloud revenue declin[ed] quarter-over-quarter for the first time" [22]. Rosenblatt models **+19%** cloud growth in Q1, decelerating from 20% [23] — that is ~$233M, above the $229M consensus.

Management's own decomposition on the Q4 call: annual (committed) cloud grew 26% while **monthly self-serve cloud grew just 3%** and was described as "a flattish business" and not a strategic priority [9]. So the honest read is that the headline cloud line is being dragged by a stagnant self-serve tail while the committed book compounds in the mid-20s. **If cloud prints ≥$232M with committed cloud still ~25%+, the deceleration narrative that drove Morgan Stanley's July downgrade breaks and the stock has room. If cloud prints ≤$225M — a second soft sequential — the "AI search isn't showing up in Elastic's numbers" thesis [20] is confirmed and the 35% run unwinds violently.**

**Secondary signal, close behind: the FY27 revenue guide.** Management framed FY27 as back-half weighted, with growth driven by "CRPO … which turns into recognised revenue through the year, as well as increasing ramp sales capacity" [9]. A reiterate-only FY27 after a Q1 beat will be read as the beat being one-off/FX; a raise to the top half or above $2.00B is the bull trigger. Note that FY27 guidance explicitly assumed **no contribution from unannounced products or acquisitions** [9] — and Elastic has since closed Deductive AI ($85M, 24 Aug 2026) [30][31], which gives management a clean, non-demand reason to nudge numbers.

---

## 4. Fundamentals — what changed, what is at stake

**FY26 exit (year ended 2026-04-30)** [2]:
- Total revenue $1.739B, +17% (+16% cc). Subscription $1.634B, +18%. Elastic Cloud $837.3M, +22%. Sales-led subscription $1.438B, +20%.
- Non-GAAP operating margin **16.4%**; GAAP operating margin −2%.
- Adjusted FCF $346M, **20% margin**; operating cash flow $327M. Rule of 40 = 37%.
- Non-GAAP diluted EPS $2.57. GAAP diluted EPS $3.43 — **inflated by a large one-off tax benefit** ($435M benefit recognised in Q4, producing GAAP Q4 EPS of $4.14) [2]. Do not read the GAAP line as earnings power.
- Cash + marketable securities $1.370B.

**Q4 FY26 (quarter)** [2]: revenue $451M +16% (+14% cc); subscription $422M +17%; sales-led subscription $375M +19% (+16% cc); non-GAAP op margin 14.8%; non-GAAP EPS $0.61; adjusted FCF $150M.

**Backlog and customers — the genuinely strong part of the story** [2][10][12][11]:
- **Total RPO $1.982B, +28% y/y — the highest y/y growth in four years.** Current RPO $1.203B, +20%.
- **Non-current RPO +43% y/y**, achieved "without any material change in our discount practices" per management [9] — i.e. longer multi-year commitments rather than bought duration.
- Net expansion rate **~112%**, flat for four straight quarters (Q1 FY26 112%, Q2 112%, Q3 ~112%, Q4 ~112%) [11][12][10][2]. Stable, not accelerating.
- Customers >$100k ACV: 1,510 (Q4 FY25) → 1,550 (Q1 FY26) → 1,600 (Q2) → 1,660 (Q3) → **1,720+ (Q4 FY26)** [11][12][10][2]. Consistent +50–60/quarter cadence — Q1 FY27 should print ~1,770–1,780 to stay on trend.
- **240+ customers at >$1M ACV**, a record quarter for $1M deals; >30 net adds to that cohort in FY26; >$5M customers grew 30% [36].
- **600+ customers with $100k+ ACV now use Elastic's AI capabilities, and that cohort grows ~500bp faster than non-AI customers** [9] — management repeated this on the Q4 call and it is the single most cited bull datapoint.

**What changed since the last print (all after 28 May 2026 guidance was set):**
1. **7% workforce reduction announced 24 June 2026** (plan committed 23 June), ~250 roles, **$22–25M one-time severance and related charges, most recognised in Q1 FY27** [18][19]. Management said it still expects net headcount growth this year and will keep hiring in customer-facing GTM [18]. **This is not in the Q1 or FY27 non-GAAP margin guidance.** It is a live source of upside to the ~14.0% Q1 op-margin guide and to the ~19.0% FY27 guide.
2. **Chief Product Officer Ken Exner resigned** — notified 18 June 2026, last day 17 July 2026. Engineering leadership (Elasticsearch & Platform Group; Observability & Security Group) now reports directly to CEO Kulkarni [17].
3. **Deductive AI acquired for $85.0M, closed 24 August 2026** [30][31] — AI-driven production-incident investigation, folded into Elastic Observability. Announced July 2026.
4. **Morgan Stanley downgrade to Equal-weight, PT $73 → $66, on 21 July 2026** (stock −4.4% that session) [20][21] on the view that Elastic's AI-driven search business is taking longer to grow than rival data-infrastructure names.

**Capital structure and returns** [15][16][33][34]:
- $500M repurchase authorisation, announced October 2025 alongside an Analyst Day at which targets were raised (stock +8% that day) [33][34]. Stated policy: return ~50% of FCF via buyback absent better acquisition uses [34].
- FY26 repurchases **$340.1M** of the $500M — but the cadence is telling: $109.2M through H1, **$190.9M in Q3 alone** (the quarter the stock crashed to the $50s), then **only $40.0M in Q4** [15]. ~$160M authorisation remains. *(Inference, mine: management bought aggressively at $52–70 and stepped back as the stock recovered; that is a mild valuation signal from insiders-with-a-cheque-book, and it cuts against buying here at $79.)*
- Shares outstanding 105.53M (2025-04-30) → 104.75M (2026-04-30) [16] — **net share count down ~0.7%, so the buyback is more than absorbing SBC dilution.** Q1 FY27 guidance nonetheless assumes 106.0–107.0M diluted shares [2].
- Gross margin ~76% (trailing) [22][23]. Net cash $778.7M [5].

**Customer concentration.** One customer — **a channel partner — was 11% of total revenue in FY26** (11% in FY24, 12% in FY25) [36]. Material and stable; worth flagging because a marketplace/distributor concentration of that size can shift quarterly revenue timing.

**Headcount / capacity.** Revelio Labs reports ~3,890 employees as of March 2026, up 35.2% from 2,877 in 2023, with 1,115 active job postings in 2026 (+84.3% vs 2025) [45]. AltIndex shows 340 currently open roles, +6.6% over the quarter [26]. The GTM-capacity ramp management is leaning on for FY27 acceleration is at least visible in postings.

---

## 5. Positioning & options

All options data below is derived from the CBOE delayed-quote chain snapshot for ESTC, timestamped **2026-08-26T15:59:59 (ET close)** [4]. It is one session stale and pre-dates today's session; treat levels, not decimals.

**Term structure — a textbook earnings kink.** ATM ($80 strike) IV: **Sep-18 85.8% → Oct-16 70.2% → Nov-20 66.8% → Dec-18 66.5% → Jan-27 65.3% → Feb-27 61.8% → Jun-27 61.1%** [4]. The front month carries ~15.6 vol points over the second month, which is the entire event premium. CBOE's headline iv30 is 79.85% with a zero one-day change [4].

**Skew — call-favoured, not put-protected.** On the Sep-18 expiry: the ~25-delta put ($70 strike, δ −0.24) marks IV 87.4%, while the ~25-delta call ($95 strike, δ +0.25) marks IV 90.9%; the $90 call (δ +0.33) marks 86.7% vs the $70 put's 87.4% [4]. Wings are essentially flat with a mild **call** bid. For a name that has fallen on five of its last eight prints, the absence of a downside skew premium is notable — **the options market is not paying up for crash protection here.** *(Inference, mine.)*

**Open interest and put/call.**
- Sep-18 expiry: 3,259 call OI vs 1,784 put OI → **P/C OI 0.55** [4].
- All listed expiries: ~37,997 call OI vs ~9,551 put OI → **P/C OI ~0.25** [4]. Fintel separately reports an OI put/call ratio of **0.36** for ESTC [25] (snippet only).
- Longer-dated positioning is extremely call-heavy: **Nov-20 11,955 call OI vs 1,153 put OI (P/C 0.10)** and **Jun-27 10,409 call OI vs 394 put OI (P/C 0.04)** [4]. Jan-28 is the only expiry that is put-heavy (P/C 2.01) [4].

**Unusual activity.**
- MarketBeat flagged **4,771 calls traded on Friday 14 Aug 2026, +101% vs the 2,375 average** [24].
- In the 26 Aug snapshot, the **Sep-18 $100 call** (26% out of the money) traded **344 contracts on 956 OI** — by far the largest single-strike volume in the chain and more than the entire ATM strike's call volume (25) [4]. Someone is buying far-OTM upside into the print. That is speculative, cheap, and consistent with the momentum crowd rather than with institutional hedging.

**Short interest.** Two sources disagree slightly and I am reporting both:
- stockanalysis.com: **5.68M shares short, 5.47% of shares outstanding, 6.71% of float, short ratio 3.57 days to cover**, as of 2026-08-26 page state [5].
- A search snippet citing the settlement **dated 2026-08-04** puts it at **7.08M shares, 6.81% of shares outstanding**, with days-to-cover ~2.15 on 1.90M average volume [snippet only, see 5's search context].
Either way: **mid-single-digit short interest and 2–4 days to cover — not a squeeze setup, not a crowded short.** There is no meaningful short base to force a covering rally.

**Borrow fee: unavailable.** Fintel's short-squeeze page returned HTTP 403 [see coverage gaps].

**Run-up and drawdown into the print** [3]:

| Window | ESTC | IGV (software ETF) | Relative |
| --- | --- | --- | --- |
| 2026-07-22 → 2026-08-26 | **+35.06%** ($58.68 → $79.25) | +15.02% | **+20.0pts** |
| 2026-07-24 → 2026-08-24 (1 month) | **+41.9%** | — | — |
| 2026-08-19 → 2026-08-26 (5 sessions) | **−9.26%** ($87.34 → $79.25) | −0.41% | **−8.9pts** |

Two big single-session gains built the move: **+7.38% on 7 Aug 2026** [3][37] and **+11.50% on 13 Aug 2026** [3]. The 13 Aug move was partly sector — MongoDB +7.9%, monday.com +9.7%, Cloudflare +6.2% on a soft PPI print that took the S&P to a record close [29] — and partly company-specific AI-security narrative ahead of Black Hat USA 2026, plus an AV-Comparatives 100%-malware-protection result and a new AWS Security Competency AI distinction [28]. **None of it was a fundamental datapoint about the July quarter.**

**How crowded does this look? (my read.)** Crowded long on the options tape and the momentum tape; *not* crowded on the short side; and the last five sessions have already vented ~9% of the run while the sector barely moved. That combination — a 35% one-month rally, call-skewed options, zero short base, no put protection bid, and a Street sitting exactly on guidance — is the classic configuration in which an in-line print gets sold. It is also the configuration in which a genuine cloud re-acceleration produces a violent squeeze higher, because nothing is positioned against it.

---

## 6. Sentiment & alt-data

**Analyst ratings and targets — three published consensuses that do not agree.** Report all three; the dispersion itself is the datum.

| Source | Consensus rating | n | Average PT | Range | As of |
| --- | --- | --- | --- | --- | --- |
| stockanalysis.com [6] | Buy | 31 | **$84.41** (+6.5% vs spot) | $53 – $120 | 2026-08-26 |
| Investing.com [46] | 18 buy / 12 hold / 1 sell | 27 | **$77.41** (−2.3%) | $53 – $120 | Aug 2026 (snippet only) |
| S&P Global via Barchart [47] | Buy | 30 | **$71.40** (−9.9%) | — | Aug 2026 (snippet only) |

**The stock has run through the middle of its own target distribution.** On the two lower consensus marks it is already *above* the average target.

**Rating and target actions, dated:**
- **21 Jul 2026 — Morgan Stanley: Overweight → Equal-weight, PT $73 → $66**; less confident a growth inflection materialises near/medium term; AI-driven search "taking longer than expected to grow" while rival data-infrastructure names already show AI benefit. Stock −4.4% that session [20][21].
- **18 Aug 2026 — Stifel: Buy maintained, PT $65 → $90** on valuation (~13× CY27 EV/FCF), noting Q4 cloud's first sequential decline but a "positive bias … based on the valuation" as SaaS comps ease through FY27 [22].
- **25 Aug 2026 — Wells Fargo: Equal-weight maintained, PT $60 → $80** [snippet only, see 6's search context].
- **26 Aug 2026 — Rosenblatt: Buy reiterated, PT $83**; expects an in-line-to-marginal beat, models cloud +19% in Q1 vs 20% in Q4; cites log-management tool consolidation, legacy-SIEM modernisation and agentic AI apps on Elasticsearch Relevance Engine [23].
- Rosenblatt had earlier cut its target to $83 from $90 following the restructuring and leadership departure [snippet only].
- Search snippets also reference BofA raising to $90 from $70 and TD Cowen to $70 from $65 in August [snippet only, undated in the snippet].

**Price-target drift is chasing price, not leading it.** Stifel +$25, Wells Fargo +$20 and Rosenblatt's cut-then-hold all land *after* the 35% rally. That is momentum-following coverage, and it is why the average target now sits only ~6% above spot on the most generous count.

**Retail / social (supporting colour only, never load-bearing):**
- Stocktwits followers **5,977, roughly flat over three months** as of mid-August 2026; ESTC ranks in the 1st percentile of its industry for Stocktwits following [27]. **Retail is not crowding this name.**
- AltIndex (as of 2026-08-27) [26]: **AI Score 38/100 ("Sell")**, but **sentiment score 91/100** with "negative pressure over 90 days." Reddit mentions ~2/day; X mentions 3 (+92.1%); Stocktwits mentions 2 (+96.1%); news mentions 50 (+92.3%). The percentage jumps are off tiny bases — the absolute chatter volume is negligible.
- Retail tone in August has been positive on the AI-security/agentic-SOC narrative [28], and Stocktwits characterised sentiment around July's target cut as "divided" [27-adjacent].
- **7/14/30-day quantified sentiment trend: not sourced** — I could only get a 90-day directional characterisation and a 3-month follower trend. See coverage gaps.

**Alt-data proxies** [26][45]:
- **Web traffic: ~1.2M monthly visits, −7.4% over three months.** A negative, though elastic.co traffic is a weak proxy for a sales-led enterprise business whose growth is explicitly coming from committed multi-year deals rather than self-serve.
- **Job postings: 340 open roles, +6.6% over the quarter** [26]; 1,115 postings across 2026, +84.3% vs 2025 [45]. Consistent with management's "add more sales capacity" commitment [9] despite the 7% cut.
- Employee "business outlook" 45% positive, **−27.4%** [26] — plausibly the June layoff showing up in Glassdoor-type data.
- Elastic named a Leader in the 2026 Gartner Magic Quadrant for Observability Platforms, third consecutive year [snippet only].
- **Google Trends: not sourced.** No app-rank data applies (enterprise infrastructure).

---

## 7. Forensics

**Form 4 / insider activity** [13]:
- **No Form 4 has been filed since 2026-06-10.** The insider tape has been silent for ~11 weeks going into this print — consistent with a standard blackout, and notably free of discretionary selling into a 35% rally.
- Filings cluster tightly on RSU vesting dates: seven Form 4s on 2026-06-10 (transaction date 2026-06-08), seven on 2026-03-10 (2026-03-09), one on 2026-01-12 (2026-01-09), each preceded by a batch of Form 144s [13].
- **CEO Ashutosh Kulkarni**: on 2026-06-08 received 148,857 PRSU-linked shares and 111,123 RSUs; on 2026-06-09 sold **40,373 shares at $60.61 to satisfy tax withholding** — an employer-mandated "sell to cover", not a discretionary disposal [38]. A CPO filing shows the same RSU-vest/tax-sale pattern [38].
- **Read: the insider activity in this name is mechanical.** I found no evidence of a discretionary open-market sale by an officer or director in 2026. That is a mild positive, or at minimum the absence of a negative. *(Inference, mine.)*

**13D — Pictet has been distributing into the rally.** Pictet Asset Management SA filed an original Schedule 13D on ESTC on 2026-01-26 and has amended it repeatedly (2026-03-03, 2026-05-15, 2026-08-04, 2026-08-19, 2026-08-20) [13][14]. Amendment No. 2 (event date 2026-08-19, filed 2026-08-20) discloses:
- **5,393,567 shares, 5.18% of the class**; sole voting power 5,377,364; aggregate cost ~$400.8M [14].
- Item 4 is an **engagement, not control**, mandate: Pictet "may seek to influence the Issuer's policies and practices through discussions with the Boards and management" but "does not currently have any plans or proposals that would result in a change in control" [14].
- **The transaction schedule is the interesting part.** Across 23 Jun – 19 Aug 2026 Pictet reports **527,565 shares sold against 83,640 bought — net −443,925 shares.** Specifically: sells of 15,180 @ $59.23 (23 Jun), 9,704 @ $67.37 (6 Aug), 16,465 @ $83.44 (17 Aug) and **152,158 @ $85.96 on 19 Aug 2026 — the exact local high close of $87.34's session cluster** [14][3].
- *(Inference, mine: a 5%+ holder was a heavy net seller into the entire August rally, and its single largest sale landed within a day of the top. That is real supply, and it is disclosed supply — meaning the panel can treat it as fact rather than as flow speculation.)*
- A separate 13G/A was filed on 2026-08-13 by CIK 1167557 [13]; I did not resolve the holder.

**Executive departures.** CPO **Ken Exner** notified the company on **18 June 2026** and departed **17 July 2026**, "not a result of any disagreement with the Company or its board … or any matter relating to the Company's operations, policies, or practices"; engineering leadership consolidated under the CEO [17]. CFO Navam Welihinda has been in seat since 28 Feb 2025 [17-adjacent]. **A CPO exit at a company whose entire equity story is product-led AI differentiation is a genuine negative signal, and it is why Rosenblatt trimmed its target** [snippet only].

**Restructuring.** 8-K filed 2026-06-24 (plan committed 2026-06-23): ~7% workforce reduction, ~250 roles, **$22–25M one-time severance charges, most in Q1 FY27**, framed as AI-driven efficiency with continued hiring in GTM and expected net headcount growth for the year [18][19].

**Auditor / restatement.** PricewaterhouseCoopers LLP; the FY26 Exhibit 23.1 consent references PwC's report **dated 8 June 2026** on both the financial statements and **the effectiveness of internal control over financial reporting** [35]. The 10-K was filed on time on 2026-06-08 [13]. **No Item 4.01 (auditor change) or Item 4.02 (non-reliance) 8-K appears in the EDGAR index** [13]. No restatement or material-weakness disclosure found.

**8-K cadence.** Only three 8-Ks in calendar 2026: 2026-02-26 (Q3 results), 2026-05-28 (Q4 results), 2026-06-24 (restructuring/CPO) [13]. **Nothing since 24 June — no pre-announcement, no negative pre-release, no guidance update.** For a company that has beaten its guide seven straight quarters, silence is the base case, not a signal.

**Filing-language / tone.** I did not do a systematic 10-K/10-Q diff — flagged in coverage gaps. The one tonal item I can source is from the Q4 call: CFO Welihinda framed FY27 guidance as "a credible projection" carrying "appropriate risk adjustment … related to consumption, related to FX, related to timing of large deals and mix" and excluding any contribution from unannounced products or acquisitions [9]. That is conservative framing, consistent with a beat-and-raise cadence.

---

## 8. Macro & peer read-through

**Regime.** Software is in a violent, high-dispersion, AI-differentiated tape. In the last three months daily ±5%+ moves have been routine across the complex: DDOG has had ten such sessions, MDB eleven, NOW seventeen, CRWD eleven [3]. Whatever ESTC does on Friday will be amplified by a market that is repricing "who actually monetises AI" almost daily. On 13 Aug a soft PPI print took the S&P 500 to a record close of 7,798.99 and lifted the whole AI-software cohort [29].

**Sector performance since the 22 July low** [3]: ESTC **+35.1%**, MDB +33.2%, NOW +31.8%, SNOW +17.8%, IGV +15.0%, S +12.6%, PANW +1.2%, CRWD +0.4%, DDOG −7.4%. **The entire AI-data-infrastructure cohort has re-rated; ESTC is at the top of it.** In the last five sessions the cohort has faded together (MDB −7.8%, CRWD −6.2%, PANW −5.7% since 19 Aug) with ESTC the worst at −9.3% [3].

**The peer that matters most this quarter: Datadog.** DDOG reported Q2 2026 on 5/6 August — **$1.12B revenue (+36%), adjusted EPS $0.65, both above consensus, and it raised full-year guidance — and the stock fell 19.03% on 6 Aug, a record single-day drop** [3][32]. The cause was forward-looking and idiosyncratic: Q3 guidance implied deceleration to ~29% because its largest customer (a nine-figure AI account widely believed to be OpenAI) is cutting usage from Q3 [32]. DDOG then rebounded +11.5% on 10 Aug [3]. **The lesson for ESTC is not about AI-customer concentration — Elastic's 11% concentration is a channel partner, not an AI hyperscaler [36] — it is about the reaction function: in this tape, a beat-and-raise into a rich setup is not sufficient, and forward commentary dominates the print.**

**Other peers.** SNOW +36.5% on 28 May 2026 and MDB +10.6% the same day, on their own prints [3] — the same cohort has produced enormous *positive* earnings gaps this year too. **Both SNOW (2 Sep 2026) and MDB (1 Sep 2026) report *after* ESTC** [41][42], so Elastic prints without a same-quarter read from its two closest data-platform comparables and will itself be the read-through *for* them. That raises the odds of an outsized cross-asset reaction: ESTC is the first data-platform datapoint of the September cycle.

**Rates and FX.** US 10-year at **4.664%** on 2026-08-26, up from 4.455% when FY27 guidance was set on 28 May [43-fx]. Long-duration software has re-rated *despite* higher rates — an AI-narrative-driven move, not a discount-rate one, and therefore more fragile. **FX is a modest headwind, not a tailwind:** EUR/USD was 1.1653 on 28 May (guidance-setting), 1.1729 at the 30 Apr quarter start, and had fallen to **1.1524 by 30 July** (DXY 99.02 → 99.80) [43-fx]. Q4 FY26 reported growth exceeded constant-currency growth by ~200bp [2]; on the May–July quarter's currency path that tailwind should be **smaller** in Q1 FY27. *(Inference, mine — I did not source Elastic's specific FX assumptions.)*

**Customer/supplier read-throughs.** Public-sector cloud is a bright spot management called out: U.S. federal agencies using SIEM-as-a-service have "already exceeded" initial $26M commitments [9]. Log-management tool consolidation and legacy-SIEM displacement are the two demand vectors Rosenblatt underwrites [23], both of which are share-shift, not budget-expansion, stories — durable but slow.

---

## 9. Bull case / bear case / base case

**Bull case.** The backlog is already telling you FY27 is fine: total RPO +28% y/y, the best in four years, and non-current RPO +43% with no change in discounting [2][9]. Net expansion has been rock-stable at ~112% for four quarters and $100k+ customers keep compounding +50–60/quarter to 1,720+, with a record $1M-deal quarter and 240+ million-dollar customers [2][36]. The AI cohort — 600+ six-figure customers using Elastic AI features, growing ~500bp faster than the rest [9] — is the mechanism by which cloud re-accelerates, and Rosenblatt models cloud at +19%, above the $229M consensus [23]. On top of that, the 7% June restructuring ($22–25M of charges, ~250 roles) was announced *after* the ~14.0% Q1 and ~19.0% FY27 margin guides were set [18][2], so there is un-guided cost relief that can drive a clean EPS beat and a plausible FY27 margin raise. Valuation is not the obstacle: 24.4× forward earnings, EV $7.46B with $779M net cash, ~13× CY27 EV/FCF per Stifel [5][22]. Positioning is not the obstacle either: 5–7% short interest with 2–4 days to cover [5], negligible retail crowding (5,977 Stocktwits followers, 1st percentile) [27], and no downside skew bid [4]. Beat cloud, raise FY27, and there is nothing positioned to stop a 12–15% gap up in a tape that gave SNOW +36% and MDB +10.6% on a single day this year [3].

**Bear case.** The stock has done the work already — **+35.1% in 24 sessions and +41.9% in a month** [3][7] — for reasons that had nothing to do with the July quarter: a soft PPI print, a Black Hat AI-security narrative, an AV-Comparatives test result and an AWS competency badge [28][29]. It now sits ~6% below the most generous consensus target and *above* two others [6][46][47], with sell-side targets being raised *after* the move. Meanwhile the fundamental deceleration Morgan Stanley downgraded on in July is unrefuted: **Elastic Cloud declined sequentially for the first time ever in Q4** [2][22], cloud y/y growth has stepped 24% → 22% → 21% → 20% and consensus asks for 17.1% [11][12][10][2][7], and monthly self-serve cloud is growing 3% and was written off by management as "a flattish business" [9]. Management itself pre-announced that Q1 is the trough — 13.1% growth, EPS *down* 3.3% y/y — and the Street is parked exactly on the guide with no cushion [2][7]. The product organisation lost its CPO on 17 July [17] and 7% of staff went in June [18]. A 5.18% holder sold 527,565 shares net into the rally, including 152,158 at $85.96 on 19 August [14]. The buyback slowed from $190.9M in Q3 FY26 to $40.0M in Q4 as the price recovered [15]. And the cohort's own precedent this month is Datadog: beat, raise, **−19%** [32]. Five of the last eight ESTC prints were down; the median absolute reaction is 14.7% [3].

**Base case (my read).** Elastic beats its own Q1 guide by roughly 1–2% on revenue (~$474–480M) and beats more comfortably on EPS because the June layoff savings are not in the guide — call it $0.62–0.68. Cloud lands close to $228–233M, technically a sequential rebound but with y/y growth stepping down again toward 17–19%, which will be described as "in line" and read by bulls and bears alike as confirmation of their prior. FY27 revenue guidance is reiterated or nudged to the top half rather than raised outright, because management deliberately front-loaded conservatism in May and has three quarters of execution risk still in front of it [9]. That is a good quarter into a stock that has already priced a good quarter. With ~13% implied and 14.7% median realised, I think the distribution is genuinely fat on both tails but **modestly skewed down**, because the marginal buyer at $79 arrived in the last four weeks on narrative rather than numbers, and because Q1 structurally cannot deliver the back-half acceleration proof the story needs. **Preliminary direction score −20, prob_up 42%.** I hold this with **medium** conviction only: the fundamental beat probability is high, the FY27 margin raise is a real and under-modelled catalyst, and this name has twice in the last four quarters reversed its entire initial reaction by the close — so **reversal risk is 70/100**, unusually high, and any directional read should be sized against that rather than against the sign of the gap.

---

## 10. What would flip the consensus view

The single most credible reversal is **an FY27 revenue and margin raise driven by an Elastic Cloud print of $234M or better.**

Concretely: if Elastic reports Q1 cloud revenue ≥ $234M (≥ +19.5% y/y, ≥ +7.6% q/q — better than the +6.0% q/q it managed in Q3 FY26), *and* raises the FY27 revenue range above $2.000B, *and* lifts the ~19.0% FY27 non-GAAP operating-margin guide toward 20%+ on the back of the June restructuring, then three separate bear pillars break at once. The cloud deceleration story that underpinned Morgan Stanley's July downgrade [20] is falsified; the "AI search isn't showing up in the numbers" critique loses its only quantitative support; and the +43% non-current RPO stops being a promise and starts being revenue. In that world the stock is not expensive at 24× forward earnings and ~13× CY27 EV/FCF [5][22], there is no short base to slow it [5], nobody owns downside protection [4], and a 15%+ gap higher is entirely available — the same cohort produced SNOW +36.5% and MDB +10.6% on single days this year [3].

The mirror-image flip, which I regard as slightly more likely: **cloud ≤ $225M with FY27 merely reiterated.** That is a second consecutive soft cloud quarter, and given the run-up it would take the stock back toward the mid-$60s in one session.

**Watch for the gap fade either way.** Both the May 2026 and August 2025 prints saw the initial reaction fully reverse intraday [3][8]. Whatever prints at 16:05 ET is not the answer.

---

## 11. Coverage gaps

| Gap | Why it matters |
| --- | --- |
| **No quoted event-implied move.** ESTC has no weekly options; the nearest expiry is 22 days out. My 12.9% is derived from the Sep/Oct IV term structure [4], not quoted by a vendor. | The panel sizes its move against this. A ±1.5pt error changes what counts as a "big" reaction. The two published implied-move articles I found were dated Aug-2024 and Jun-2024 and were discarded. |
| **IV rank / IV percentile: not sourced.** MarketChameleon returned 503, Barchart's volatility page rendered without data, OptionCharts returned "invalid ticker". CBOE gives a level (iv30 79.85%) but no history. | Without a rank we cannot say whether 86% front-month IV is expensive *for this name*. Given a 14.7% median realised move, it may not be. |
| **Borrow fee / shares available to borrow: not sourced.** Fintel returned HTTP 403. | Would tell us whether the mid-single-digit short base is a conviction short or index/hedge flow. |
| **Short-interest figures disagree** (5.68M / 6.71% of float, DTC 3.57 [5] vs 7.08M / 6.81% as of 2026-08-04 with DTC ~2.15 [snippet]). | Both point to "not a squeeze," so the disagreement is low-stakes, but neither is confirmed to a FINRA settlement date I could open. |
| **Whisper number: unavailable.** EarningsWhispers is gated. | The printed consensus is literally the guidance midpoint, so the real bar is entirely in the unpublished whisper. This is the most consequential single gap in the dossier. |
| **60- and 90-day estimate revision series: not sourced.** Only a 30-day figure (+18.2%) which I believe is mechanical catch-up to a May guide. | Genuine revision momentum would materially change the read on whether the buy-side has moved above guidance. |
| **Quantified 7/14/30-day social sentiment trend: not sourced.** Only 3-month follower flatness [27] and a 90-day directional characterisation [26]. | Retail is a small factor in this name (1st-percentile Stocktwits following), so the impact is limited. |
| **Google Trends / web-traffic detail beyond a single 3-month delta.** | elastic.co traffic is a weak proxy for a sales-led enterprise motion; low impact. |
| **Filing-language / risk-factor diff between the FY25 and FY26 10-Ks: not performed.** | Tone shifts in risk factors occasionally front-run guidance changes; I could not do this without pulling and diffing two very large documents. |
| **Identity of the 13G/A filer (CIK 1167557, filed 2026-08-13): not resolved** [13]. | Could be a meaningful institutional position change alongside Pictet's selling. |
| **Elastic's specific FX assumptions inside FY27 guidance: not sourced.** My FX-headwind read is inferred from spot EUR/USD and DXY paths [43-fx]. | Determines whether a reported-revenue beat is real or currency. |
| **Live spot on 2026-08-27.** Market had not opened when this was written (10:36 UTC). All price anchors are 2026-08-26 closes. | The stock has moved 3%+ on four of the last six sessions; spot at the print could differ materially from $79.25. |
| **Sequential guide-vs-actual beat history before Q3 FY26** — I could source only two quarters of guidance midpoints against actuals. | A longer beat series would tighten the "what is a normal beat" estimate. |

Domains that could not be reached (record for the run log): **fintel.io (403), marketchameleon.com (503), stockstory.org (403), macrotrends.net (403), alphaquery.com (503), earningswhispers.com (gated), Yahoo options API (401 / crumb rate-limited), stooq.com (JS anti-bot challenge).**

---

## 12. Sources

1. Elastic IR — "Elastic to Announce First Quarter Fiscal 2027 Earnings Results on Thursday, August 27, 2026" (press release 2026-08-13) — event date, AMC session, 17:00 ET call, quarter ended 2026-07-31. https://ir.elastic.co/News--Events/news/news-details/2026/Elastic-to-Announce-First-Quarter-Fiscal-2027-Earnings-Results-on-Thursday-August-27-2026/default.aspx
2. Elastic IR — "Elastic Reports Fourth Quarter and Fiscal 2026 Financial Results" (2026-05-28) — Q4/FY26 actuals, cloud $217.4M, RPO, NER, customers, and full Q1 FY27 + FY27 guidance. https://ir.elastic.co/News--Events/news/news-details/2026/Elastic-Reports-Fourth-Quarter-and-Fiscal-2026-Financial-Results/default.aspx
3. Yahoo Finance chart API, ESTC 2-year daily OHLC (pulled 2026-08-27) — spot, 52-week range, all historical earnings-day moves, open-to-close reversals, run-up/drawdown. https://query1.finance.yahoo.com/v8/finance/chart/ESTC?range=2y&interval=1d
4. CBOE delayed options quotes for ESTC, snapshot 2026-08-26T15:59:59 ET — full chain, ATM straddles, IV term structure, skew, open interest, iv30, absence of weekly expiries. https://cdn.cboe.com/api/global/delayed_quotes/options/ESTC.json
5. stockanalysis.com — ESTC statistics (2026-08-26) — market cap, shares out, short interest/float/days-to-cover, beta, forward P/E, EV, cash and debt. https://stockanalysis.com/stocks/estc/statistics/
6. stockanalysis.com — ESTC forecast (2026-08-26) — consensus rating, 31 analysts, average PT $84.41, range $53–$120, FY27 revenue/EPS consensus. https://stockanalysis.com/stocks/estc/forecast/
7. Yahoo Finance / Zacks — "Countdown to Elastic (ESTC) Q1 Earnings: Wall Street Forecasts for Key Metrics" (2026-08-24) — metric-level consensus incl. Elastic Cloud $229.23M, 30-day revision, +46.5% one-month return, Zacks Rank #3. https://sg.finance.yahoo.com/news/countdown-elastic-estc-q1-earnings-131504554.html
8. Investing.com — "Elastic shares tumble nearly 9% on weaker-than-expected Q1 earnings guidance" (2026-05-28) — after-hours reaction, Q1 EPS guide vs $0.63 consensus, FY27 guide vs $2.84 consensus. https://www.investing.com/news/earnings/elastic-shares-tumble-nearly-9-on-weakerthanexpected-q1-earnings-guidance-93CH-4715593
9. Motley Fool — Elastic (ESTC) Q4 FY2026 earnings call transcript (2026-05-28) — annual vs monthly cloud, 600+ AI customers / 500bp, sales-capacity commitment, FY27 guidance philosophy, non-current RPO +43%, public-sector SIEM. https://www.fool.com/earnings/call-transcripts/2026/05/28/elastic-estc-q4-2026-earnings-transcript/
10. SEC — Elastic 8-K Ex-99.1, Q3 FY26 results (filed 2026-02-26) — Q3 revenue $450M, cloud $218M, NER, customers 1,660+, cRPO $1.055B, Q4/FY26 guidance. https://www.sec.gov/Archives/edgar/data/1707753/000170775326000003/a26q3erex991.htm
11. SEC — Elastic 8-K Ex-99.1, Q1 FY26 results (filed 2025-08-28) — year-ago comparables: revenue $415.3M, cloud $195.8M, services $26.7M, non-GAAP EPS $0.60, op margin 15.7%, cRPO $956.5M. https://www.sec.gov/Archives/edgar/data/1707753/000170775325000034/a26q1erex991.htm
12. SEC — Elastic 8-K Ex-99.1, Q2 FY26 results (filed 2025-11-20) — Q2 revenue $423.5M, cloud $205.7M, Q3 guidance midpoint $438M, buyback disclosure (1.4M shares @ $84.45). https://www.sec.gov/Archives/edgar/data/1707753/000170775325000053/a26q2erex991.htm
13. SEC EDGAR — Elastic N.V. submissions index, CIK 0001707753 (pulled 2026-08-27) — 8-K cadence, absence of filings since 2026-06-24, Form 4 / 144 clusters, 13D and 13G/A filings, 10-K filing date. https://data.sec.gov/submissions/CIK0001707753.json
14. SEC — Pictet Asset Management SA, Schedule 13D/A No. 2 on Elastic N.V. (event 2026-08-19, filed 2026-08-20) — 5,393,567 shares / 5.18%, engagement-not-control Item 4, full transaction schedule showing 527,565 shares sold vs 83,640 bought 23 Jun–19 Aug 2026. https://www.sec.gov/Archives/edgar/data/1361570/000136157026000015/primary_doc.xml
15. SEC XBRL — Elastic, PaymentsForRepurchaseOfCommonStock — FY26 buyback $340.088M full-year, $109.175M H1, $300.075M 9M (implies $190.9M in Q3, $40.0M in Q4). https://data.sec.gov/api/xbrl/companyconcept/CIK0001707753/us-gaap/PaymentsForRepurchaseOfCommonStock.json
16. SEC XBRL — Elastic, CommonStockSharesOutstanding — 105,534,887 (2025-04-30) → 104,751,470 (2026-04-30). https://data.sec.gov/api/xbrl/companyconcept/CIK0001707753/us-gaap/CommonStockSharesOutstanding.json
17. SEC — Elastic 8-K, estc-20260618 (filed 2026-06-24) — CPO Ken Exner resignation notified 2026-06-18, departure 2026-07-17, engineering leadership reporting change. https://www.sec.gov/Archives/edgar/data/1707753/000170775326000024/estc-20260618.htm
18. StockTitan — Elastic 8-K summary, 7% workforce reduction with $22–25M charges (2026-06-24) — plan committed 2026-06-23, charges mostly in Q1 FY27, continued GTM hiring. https://www.stocktitan.net/sec-filings/ESTC/8-k-elastic-n-v-reports-material-event-7184dc9cebd6.html
19. The Register — "Elastic stretches workforce 7% thinner as AI does more of the heavy lifting" (2026-06-25) — ~250 roles, framing of the cut. https://www.theregister.com/databases/2026/06/25/elastic-stretches-workforce-7-thinner-as-ai-does-more-of-the-heavy-lifting/5261993
20. Investing.com — "Morgan Stanley downgrades Elastic stock rating on growth concerns" — OW→EW, AI-search taking longer than expected, −4.4% session. https://www.investing.com/news/analyst-ratings/morgan-stanley-downgrades-elastic-stock-rating-on-growth-concerns-93CH-4801979
21. Sahm Capital — "Morgan Stanley Downgrades Elastic to Equal-Weight, Lowers Price Target to $66" (2026-07-21) — date and PT $73→$66. https://www.sahmcapital.com/news/content/morgan-stanley-downgrades-elastic-to-equal-weight-lowers-price-target-to-66-2026-07-21
22. Investing.com — "Stifel raises Elastic stock price target to $90 on valuation" (2026-08-18) — Buy, $65→$90, first sequential cloud decline, ~13× CY27 EV/FCF, 76% gross margin. https://www.investing.com/news/analyst-ratings/stifel-raises-elastic-stock-price-target-to-90-on-valuation-93CH-4865235
23. Investing.com — "Rosenblatt reiterates Buy on Elastic stock ahead of earnings" (2026-08-26) — Buy, PT $83, in-line-to-marginal beat expected, cloud +19% in Q1 vs 20% in Q4, demand drivers. https://www.investing.com/news/analyst-ratings/rosenblatt-reiterates-buy-on-elastic-stock-ahead-of-earnings-93CH-4877005
24. MarketBeat — "Elastic Target of Unusually High Options Trading" (2026-08-14) — 4,771 calls vs 2,375 average, +101%. https://www.marketbeat.com/instant-alerts/elastic-target-of-unusually-high-options-trading-nyseestc-2026-08-14/
25. Fintel — ESTC options sentiment — OI put/call ratio 0.36 (snippet only; page 403 on direct fetch). https://fintel.io/sopt/us/estc
26. AltIndex — ESTC (2026-08-27) — AI Score 38/100, sentiment score 91/100, web traffic 1.2M −7.4% 3m, 340 job postings +6.6%, social mention counts, employee outlook −27.4%. https://altindex.com/ticker/estc
27. AltIndex — ESTC Stocktwits subscribers — 5,977 followers, roughly flat over 3 months, 1st-percentile industry ranking. https://altindex.com/ticker/estc/stocktwits-subscribers
28. StocksToTrade — "ESTC Stock Climbs As AI Security Wins Battle Analyst Downgrade" (2026-08-13) — agentic-SOC positioning ahead of Black Hat USA 2026, AV-Comparatives result, AWS AI Security competency, +10.48% intraday. https://stockstotrade.com/news/elastic-nv-estc-news-2026_08_13/
29. StartupHub.ai — AI stocks daily, 2026-08-13 — MNDY +9.7%, MDB +7.9%, NET +6.2%, soft PPI, S&P 500 record close 7,798.99. https://www.startuphub.ai/ai-news/ai-stocks-daily/2026/ai-stocks-2026-08-13
30. Elastic IR — "Elastic Completes Acquisition of Deductive AI" (2026-08-24). https://ir.elastic.co/News--Events/news/news-details/2026/Elastic-Completes-Acquisition-of-Deductive-AI/default.aspx
31. Investing.com — "Elastic completes acquisition of AI firm Deductive AI" — $85.0M purchase price. https://www.investing.com/news/company-news/elastic-completes-acquisition-of-ai-firm-deductive-ai-93CH-4874001
32. Benzinga — "Datadog Beat Earnings, Raised Guidance — but DDOG Stock Still Plunged 19%…" (2026-08-06) — peer reaction function, $1.12B revenue +36%, $0.65 EPS, Q3 guide ~29% on one AI customer. https://www.benzinga.com/markets/earnings/26/08/61033569/datadog-beat-earnings-raised-guidance-but-ddog-stock-still-plunged-19-as-wall-street-says-it-all-comes-down-to-one-customer
33. Elastic IR — "Elastic Announces $500 Million Share Repurchase Program" (October 2025) — authorisation, no expiration date. https://ir.elastic.co/news/news-details/2025/Elastic-Announces-500-Million-Share-Repurchase-Program/default.aspx
34. TipRanks — "Elastic Stock (ESTC) Rallies on Guidance Upgrade, $500M Share Repurchase Plan" — Analyst Day, +8% session, ~50%-of-FCF return policy. https://www.tipranks.com/news/elastic-stock-estc-rallies-on-guidance-upgrade-500m-share-repurchase-plan
35. SEC — Elastic FY2026 10-K Exhibit 23.1, PwC consent dated 2026-06-08 covering the financial statements and the effectiveness of internal control over financial reporting. https://www.sec.gov/Archives/edgar/data/0001707753/000170775326000018/a26q4ex231.htm
36. MarketScreener — Elastic N.V. FY2026 Form 10-K summary — one channel-partner customer at 11% of FY26 revenue (11% FY24, 12% FY25); $1M+ ACV cohort 240+, >$5M customers +30%. https://www.marketscreener.com/news/elastic-n-annual-report-for-fiscal-year-ending-april-30-2026-form-10-k-ce7f5dd3dd88f325
37. GuruFocus — "Elastic NV (ESTC) Shares Surge 7.4%…" (2026-08-07) — the 7 Aug session move to $75.11. https://www.gurufocus.com/news/9018766/elastic-nv-estc-shares-surge-74-what-gf-score-of-73-tells-investors
38. StockTitan — Elastic Form 4 filings, CEO and CPO — 2026-06-08 RSU/PRSU vesting and 2026-06-09 sale of 40,373 shares at $60.61 as a mandated sell-to-cover. https://www.stocktitan.net/sec-filings/ESTC/form-4-elastic-n-v-insider-trading-activity-7642fffa0cd1.html
39. StockTitan — Elastic CPO Form 4, RSU vesting and tax share sale. https://www.stocktitan.net/sec-filings/ESTC/form-4-elastic-n-v-insider-trading-activity-ce3d465f091c.html
40. TipRanks — ESTC earnings history — independent corroboration of the last four reaction percentages (+12.31%, −15.44%, −14.67%, −3.11%) and EPS actual vs forecast. https://www.tipranks.com/stocks/estc/earnings
41. Snowflake IR — Q2 FY2027 results to be released 2026-09-02 (i.e. after ESTC). https://www.snowflake.com/en/news/press-releases/snowflake-to-announce-financial-results-for-the-second-quarter-of-fiscal-2027/
42. MongoDB IR — Q2 FY2027 results to be released 2026-09-01 (i.e. after ESTC). https://investors.mongodb.com/news-releases/news-release-details/mongodb-inc-announces-date-second-quarter-fiscal-2027-earnings
43. Yahoo Finance chart API — peer and macro series pulled 2026-08-27: DDOG, MDB, SNOW, S, CRWD, PANW, NOW, IGV (3-month daily), and `DX-Y.NYB`, `EURUSD=X`, `^TNX` (6-month daily) for the FX/rates read. https://query1.finance.yahoo.com/v8/finance/chart/DDOG?range=3mo&interval=1d
44. Nasdaq option-chain API — ESTC "LAST TRADE: $79.25 (AS OF AUG 27, 2026)", corroborating spot; also confirms no near-dated expiries before 2026-09-18. https://api.nasdaq.com/api/quote/ESTC/option-chain?assetclass=stocks&limit=500&excode=oprac&callput=callput&money=all&type=all
45. Revelio Labs — Elastic headcount, ~3,890 employees (March 2026), +35.2% vs 2023; 1,115 active job postings in 2026, +84.3% vs 2025. https://www.reveliolabs.com/companies/elastic/employees
46. Investing.com — ESTC consensus estimates — 18 buy / 12 hold / 1 sell, 27 analysts, average 12-month target $77.41, high $120, low $53 (snippet only). https://www.investing.com/equities/elastic-consensus-estimates
47. Barchart — ESTC quote page — S&P Global consensus rating "Buy" from 30 analysts, average target $71.40 (snippet only). https://www.barchart.com/stocks/quotes/ESTC
48. StockStory via FinancialContent — "Earnings To Watch: Elastic (ESTC) Reports Q2 Results Tomorrow" (2026-08-26) — last quarter's revenue $450.7M +16%, "impressive beat of analysts' billings estimates but a slight miss of annual recurring revenue estimates" (snippet only; direct fetch 403). https://markets.financialcontent.com/stocks/article/stockstory-2026-8-26-earnings-to-watch-elastic-estc-reports-q2-results-tomorrow
49. GuruFocus — "Elastic NV (ESTC) Shares Fall 3.1%…" (2026-08-24) — 24 Aug close $83.24. https://www.gurufocus.com/news/9050444/elastic-nv-estc-shares-fall-31-what-gf-score-of-79-tells-investors
50. Businesswire — "Elastic Reports Fourth Quarter and Fiscal 2026 Financial Results" (2026-05-27/28) — primary wire copy of the Q4 release. https://www.businesswire.com/news/home/20260527847546/en/Elastic-Reports-Fourth-Quarter-and-Fiscal-2026-Financial-Results

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
