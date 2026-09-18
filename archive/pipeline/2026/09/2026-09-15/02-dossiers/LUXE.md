# LUXE — LuxExperience B.V. (formerly MYT Netherlands Parent B.V. / Mytheresa)

**What this print is about.** LuxExperience reports Q4 and full fiscal 2026 (year ended 30 June 2026) before the US open on Wednesday 16 September 2026, with the call at 08:00 ET [1][2]. Almost nothing about the quarter itself is in doubt: management told the Q3 call that Q4 adjusted EBITDA would be "around Q3 levels" [22], and my arithmetic off the sourced 9M actuals says that lands FY26 inside both legs of the €2.5–2.7bn GMV / −1% to +1% adjusted-EBITDA-margin guidance [8][10]. What is genuinely unknown is **the first-ever FY2027 guidance**, which management has said repeatedly will be given on this call [8][22]. That guide has to bridge a group adjusted EBITDA margin of roughly −0.1% in FY26 to a "medium-term" 7–9% target [8][22], against a Street that is not even internally consistent about the share count, the currency or the loss per share. Layered on top is a structurally extreme setup: a ~17m-share free float, 3.96m shares short, 25–47 days to cover [13][14], and effectively **no listed option market at all** — bids of zero, open interest of zero and last trades months stale [4]. This name has moved a mean 10.4% and a median 8.5% on its last eight earnings days (13.1% / 12.8% over the last six) and has never once gapped one way and closed the other [own calculation from 5][6]. It is a high-variance, low-liquidity, guidance-driven event on a company whose auditor issued an **adverse opinion on internal control** eleven months ago [17] and which misstated its own diluted share count in an earnings press release seven months ago [16].

---

## 1. Event & anchors

| Item | Value | As of | Source |
|---|---|---|---|
| **Event confirmed** | **Yes** | — | [1][2] |
| Report date | **2026-09-16** | announced 2026-08-26 | [1][2] |
| Session | **bmo** — "before the U.S. market opens" | — | [1][2] |
| Conference call | 08:00 ET, 2026-09-16 (webcast, no dial-in published) | — | [2] |
| Fiscal period | Q4 FY2026 and full FY2026, year ended **2026-06-30** | — | [1] |
| Corroborating feed | Yahoo `earningsTimestamp` = 2026-09-16 08:30 ET, `isEarningsDateEstimate: false` | 2026-09-15 | [5] |
| Date changed / pre-announced? | No. Date announced 2026-08-26 and unchanged; no pre-announcement, no 6-K since 2026-05-19 | — | [1][2][15] |
| **Spot** | **$7.44** (+0.68%, prev close $7.39; day range 7.34–7.52; volume 77,975) | **2026-09-14T20:00Z** | [5][6] |
| Market cap | **$1,021,226,304** | 2026-09-14 close | [5] |
| Shares outstanding | 137,261,608 | 2026-09-14 | [5] |
| Free float | **17.19m shares (12.5% of shares out)** per stockanalysis; MarketBeat implies ~84m. *Discrepancy unresolved — see gaps* | 2026-09-15 / 2026-08-31 | [13][14] |
| Book value / share | $10.29 → **P/B 0.72** | 2026-09-14 | [5] |
| EV | $883.76m; EV/EBITDA 1.27; P/S 0.36; P/E 1.92 (distorted by YNAP bargain-purchase gain) | 2026-09-15 | [13] |
| 52-week range | $6.54 – $11.38 (low set 2026-05-19, the last earnings day) | — | [5][6] |
| 50d / 200d MA | $7.86 / $8.28 → spot −5.3% / −10.1% | 2026-09-15 | [13] |
| **Event-implied move** | **UNAVAILABLE — no functioning option market** (see below) | 2026-09-14 | [4] |
| Working proxy (mine) | **≈11–13%** — see triangulation below | — | derived |
| IV rank / IV percentile | **unavailable** — optioncharts paywalled, no vendor figure found | — | [21] |
| Realised vol (own calc) | 20d **29.8%** ann. · 60d 38.3% · 120d 47.2% | 2026-09-14 | own calc from [6] |
| $ ADV (20d, own calc) | **$781,817/day**; 103,155 shares/day | 2026-09-14 | own calc from [6] |

### Why there is no implied move

The full Yahoo option chain for LUXE was retrieved successfully on 2026-09-14 [4]. It is not a market:

- Only **four** expiries exist (2026-09-18, 2026-10-16, 2026-12-18, 2027-03-19) on a **six-strike** grid ($2.50/5/7.50/10/15/17.50).
- On the first post-event expiry (2026-09-18) every single call and put shows **bid = 0.00**, and total open interest across the whole expiry is **95 contracts**.
- The ATM $7.50 call last traded **2026-05-04**. The $10 call last traded 2026-08-12 for one contract.
- The only fresh print anywhere is the 2026-09-18 **$7.50 put at $0.45, traded 2026-09-14, volume 1, open interest 0, no bid, no ask** [4].

**Triangulation of the working proxy (all mine, all labelled inference):**

| Method | Result |
|---|---|
| That single $0.45 put print, Black-Scholes inverted (S=7.44, K=7.50, T=4d, r=4.1%) | ATM IV 135%, E\|move\| **11.3%** |
| 2× that put as a straddle × 0.85 | **10.3%** |
| Mean absolute earnings-day move, last 8 quarters | **10.4%** |
| Median absolute earnings-day move, last 6 quarters | **12.8%** |

Four methods land in a 10.3–12.8% band. I use **~11–12%** as the working anchor and set the JSON field to `null`, because a one-lot print with a zero bid is not a sourced implied move. The repo's own resolver already normalises on a median historical reaction when no option anchor exists; that is the right treatment here.

### Realised earnings-day moves (all BMO — reaction is the same session)

Computed by me from Yahoo daily bars [6]; each date independently confirmed as a BMO release from the company's own release or its earnings-date press release [1][2][7][8][9][10][11][12].

| Fiscal qtr | Report date | Prev close | Open | Close | **Gap** | **Close-to-close** | Intraday after open | Day+2 c2c | Volume |
|---|---|---|---|---|---|---|---|---|---|
| FY24 Q4 | 2024-09-12 | 3.86 | 3.90 | 3.90 | +1.17% | **+1.17%** | 0.00% | +0.91% | 126,200 |
| FY25 Q1 | 2024-11-19 | 6.10 | 6.52 | 6.32 | +6.89% | **+3.61%** | −3.07% | +18.52% | 195,400 |
| FY25 Q2 | 2025-02-11 | 10.00 | 10.80 | 12.38 | +8.00% | **+23.80%** | +14.63% | +22.80% | 437,500 |
| FY25 Q3 | 2025-05-14 | 8.90 | 10.08 | 10.12 | +13.26% | **+13.71%** | +0.40% | +9.33% | 903,100 |
| FY25 Q4 | 2025-09-25 | 8.17 | 9.46 | 8.42 | +15.79% | **+3.06%** | −10.99% | +1.84% | 4,063,000 |
| FY26 Q1 | 2025-11-19 | 9.15 | 8.70 | 8.67 | −4.92% | **−5.25%** | −0.34% | −8.09% | 540,700 |
| FY26 Q2 | 2026-02-10 | 7.73 | 9.00 | 9.36 | +16.43% | **+21.09%** | +4.00% | +28.72% | 1,253,800 |
| FY26 Q3 | 2026-05-19 | 7.79 | 7.29 | 6.87 | −6.42% | **−11.81%** | −5.76% | −5.78% | 1,848,300 |

- **All 8 quarters:** mean abs **10.44%**, median abs **8.53%**, max abs **23.80%**, pattern **6 up / 2 down**.
- **Last 6:** mean abs **13.12%**, median abs **12.76%**, pattern **4 up / 2 down**.
- **Gap and close agreed in direction 8 of 8 times.** The open tells you the sign.
- But the close does **not** just repeat the gap: mean abs gap 9.11% vs mean abs close 10.44%, and the session **extended** the gap in 5 of 8. The two exceptions are violent: FY25 Q4 gapped +15.79% and closed +3.06% (−11.0% intraday fade), FY25 Q1 gapped +6.89% and closed +3.61%.
- The earnings-day mean absolute move is **5.6× a normal 1σ day** at current 20-day realised vol.
- **Caveat on the two biggest up-moves.** The +21.09% on 2026-02-10 is materially contaminated: the Q2 FY26 press release **understated the fully diluted share count** (~87m vs an actual ~140m), a correction JPMorgan later priced at "approximately a $5 per share headwind to equity value" [16]. See Forensics.

---

## 2. The bar

### Consensus is not coherent on this name

Five providers, five different numbers, and they cannot all be describing the same thing:

| Source | Quarter EPS | Quarter revenue | FY26 EPS | FY27 | Analysts | As of |
|---|---|---|---|---|---|---|
| Nasdaq (via stage-0 universe) | **−$0.17** | — | — | — | 2 | 2026-09-15 [0] |
| Aggregated preview (snippet) | **−$0.11** (−102.4% YoY) | **$739.43M** (+197.1% YoY) | — | — | — | 2026-09-14 [19] |
| stockanalysis.com | — | — | **−$0.48** | rev $2.60B (+5.4%), EPS −$0.07 | 5 | 2026-09-15 [20] |
| MarketBeat | — | — | **−$0.79** | **−$0.36** | n/d | 2026-09-15 [12] |
| Simply Wall St narrative | — | — | **−€1.20** (raised from −€1.03) | — | 6 | 2026 (undated) [18] |
| Yahoo `epsCurrentYear` / `epsForward` | — | — | **−$0.4816** | **−$0.0816** | — | 2026-09-15 [5] |

The spread is not noise; it is the **share-count error propagating**. −€1.20 × 87m ≈ −€104m; −$0.48 × 137m ≈ −$66m; −$0.79 × 137m ≈ −$108m. Providers are dividing broadly similar loss estimates by two different denominators. **Treat any "beat/miss vs EPS consensus" headline tomorrow as uninformative.** That is a finding, not a gap.

`snippet_only: true` on every row above except Yahoo's and stockanalysis's.

### Revisions

- Last 3 months: **1 upward / 2 downward** on EPS and the same on revenue [19]. `snippet_only`.
- FY26 consensus loss per share widened from **−€1.03 to −€1.20**; consensus price target fell from **$10.38 to $9.25** [18]. Undated — `snippet_only`, recency unverified.
- Discrete 30/60/90-day revision percentages: **unavailable**.

### The surprise history is bad and it does not matter

- The company has **beaten consensus EPS just once in the last four quarters** [23].
- Q1 FY26 (2025-11-19): consensus −$0.28, actual −$0.71, **missed by $0.43** [12]. Stock −5.25%.
- Q2 FY26: consensus −$0.08, actual −$0.17, **surprise −112.5%** [23]. Stock **+21.09%**.
- Q3 FY26 (2026-05-19): Zacks consensus −$0.16, Zacks ESP +22.58%, Zacks Rank #3 [23]. Stock **−11.81%**.

A −112.5% EPS surprise produced +21%; a positive-ESP setup produced −11.8%. **EPS is not the transmission channel.** This is the strongest single argument that the print trades on guidance.

### What the company has to deliver just to hold flat — my derivation

All inputs sourced; the arithmetic is mine.

**Sourced 9M FY26 actuals** [8][9][10]:

| | Q1 FY26 | Q2 FY26 | Q3 FY26 | **9M** |
|---|---|---|---|---|
| GMV (€m) | 589.0 | 684.8 | 653.7 | **1,927.5** |
| Net sales (€m) | 557.2 | 645.1 | 618.4 | **1,820.7** |
| Adj. EBITDA margin | −5.0% | +2.0% | +0.9% | **−0.49%** |
| Adj. EBITDA (€m) | −27.9 (derived) | +13.2 | +5.7 | **−9.0** |

**FY26 guidance** (raised at Q2 from €2.4–2.7bn / −2% to +1%) [9][10]: GMV **€2.5–2.7bn**, adj. EBITDA margin **−1% to +1%**.

- Implied Q4 GMV to hit the guide: **€572.5m – €772.5m** (i.e. −12.4% to +18.2% sequentially off Q3). That is an enormous window; the low end is essentially un-missable.
- Management already told the Q3 call Q4 adj. EBITDA would be **"around Q3 levels"** [22] — call it +€5.7m. That puts FY26 adj. EBITDA at ≈ **−€3.3m** on ≈€2,436m of net sales = **−0.14% margin**, comfortably inside the −1%/+1% band but **below the midpoint and nowhere near the +1% top end** (which would need a Q4 margin of ~+5.3%, six times Q3's).
- **Conclusion (mine): FY26 guidance is very likely met on both legs, and the market should already assume that.** Meeting it is therefore worth ~nothing. The stock does not hold flat on FY26 delivery.

**The revenue line has a presentational trap.** Consensus revenue of $739.43M converted at the Apr–Jun 2026 average EUR/USD of 1.1626 [own calc from 26] is **€636m**, i.e. +2.8% sequentially on Q3's €618.4m. That is achievable, but **THE OUTNET was reclassified to discontinued operations under IFRS 5 in the Q3 FY26 interim report** [24][25] and it is not established that the consensus revenue figure was restated for it. A headline "revenue miss" driven purely by a discontinued-ops reclassification is a live risk tomorrow morning.

### Whisper number

**None found.** No credibly published whisper for LUXE. Recorded as a gap.

---

## 3. The one metric that matters

> **The FY2027 adjusted EBITDA margin guidance, and specifically whether the bridge from ~0% in FY26 toward the 7–9% medium-term target starts with a credible first step — with the NET-A-PORTER / MR PORTER FY27 profitability commitment as the sub-metric that validates it.**

**Why I am confident this is it, not EPS or revenue:**

1. Management said so, twice. On the Q3 call: *"Same as last year, we will communicate our fiscal year '27 guidance in our Q4 earnings call"* [22]. Confirmed again in the Q3 release framing [8].
2. FY26 delivery is pre-announced and un-newsworthy (§2 above).
3. The EPS surprise history has zero correlation with the reaction (§2 above).
4. The stock is a 0.72× book, 1.27× EV/EBITDA option on the transformation working [5][13]. Only the forward guide prices that.

**What the market expects for it, and how I know:**

- **JPMorgan carries CY2027 EBITDA of €117m** and values the equity at 8× that over ~140m shares [16]. On ~€2.55bn of FY27 net sales that is a **~4.6% adjusted EBITDA margin**. This is the single most concrete published FY27 margin expectation I could source.
- stockanalysis consensus FY27: revenue **$2.60bn (+5.4%)**, EPS **−$0.07** [20] — i.e. the Street models near-breakeven at the bottom line, consistent with a low-to-mid single-digit EBITDA margin.
- **The CFO pre-committed the shape 48 hours ago.** At the Goldman Sachs Global Consumer and Retail Conference on **2026-09-14**, Martin Beer said NET-A-PORTER and MR PORTER were *"guided to break even in fiscal 2026 and become profitable in fiscal 2027"*, YOOX to *"reach profitability by fiscal 2028"*, and long-term growth of *"low-double-digit … about a 10% compound annual growth rate"* toward *"EUR 4 billion in net sales and adjusted EBITDA margins of 7% to 9%"* [3].
- On the Q3 call management framed the bridge as absolute SG&A cuts + a **1,000bp+ SG&A-ratio opportunity at NAP/MRP** to reach Mytheresa's 12.2% ratio + top-line reacceleration, and said *"Every year, will continue to see increasing adjusted EBITDA margins to 7% to 9%"* [22].

**My read of the goalposts:** an FY27 group adjusted EBITDA margin guide of **~3–5%** with high-single/low-double-digit ex-FX growth clears the bar. **Below ~2%, or any softening of the €4bn / 7–9% medium-term language, is the bear trigger.** Above ~5% with NAP/MRP guided clearly profitable is the squeeze trigger. The CFO's appearance two days before the print, reiterating the framework unchanged, is a mild positive tilt — companies about to cut a framework do not usually restate it on a conference stage 48 hours prior. That is my inference.

**Secondary metrics that will be read on the same call:**
- Mytheresa Q4 adj. EBITDA margin. FY26 came in at *"approximately 6%"* per the CFO on 2026-09-14 [3], against Q4 FY25's 6.5% [11] — so the segment's margin went **sideways-to-down** year on year even as it grew double digits. Expect questions.
- NAP/MRP Q4 margin: guided to **break even in H2 FY26** [22]; Q3 was −0.5% [8]. Breakeven or better is required for the FY27 profitability claim to be believed.
- Mytheresa **active customers were −7.5% YoY at 774k in Q3** while AOV was +12.5% to €847 [8]. Growth is coming from spend per top customer, not from more customers. Any further deterioration in the customer count undermines the €4bn target arithmetic.

---

## 4. Fundamentals — what changed, what is at stake

### The company

LuxExperience is the old Mytheresa, renamed 2025-05-01 after acquiring **YOOX NET-A-PORTER (YNAP) from Richemont on 2025-04-23** [15][17]. Richemont *paid* Mytheresa to take YNAP, which is why trailing net income is positive ($533m TTM, P/E 1.92) on a loss-making business — it is a bargain-purchase gain, not earnings [13]. Three segments:

| Segment | FY25 net sales | FY25 GMV | Q3 FY26 net sales growth ex-FX | Q3 FY26 adj. EBITDA margin |
|---|---|---|---|---|
| Luxury \| **Mytheresa** | €916.1m | €988.5m | **+9.9%** | **+5.5%** |
| Luxury \| **NAP & MR PORTER** | €1,048.8m (illustrative) | €1,098.7m | **−5.1%** | **−0.5%** |
| Off-price \| **YOOX** (+ THE OUTNET, now sold) | n/d in extract | n/d | **−7.4%** | **−5.5%** |

Sources: FY25 figures [17]; Q3 FY26 figures [8].

### What changed since the last print (2026-05-19)

1. **THE OUTNET sale closed 2026-04-30** to The O Group LLC (renamed The Outnet Operations US, LLC) for **USD 30m**, announced 2025-10-31 [24]. Reclassified as a **discontinued operation under IFRS 5** in the Q3 FY26 interim report [25]. Q4 will be the first full quarter without it — and the first where the comparatives question bites.
2. **US de minimis exemption eliminated globally, effective 2026-02-24** [28]. Q3 FY26 caught ~5 weeks of it and management quantified the hit: *"U.S. tariff changes increased Mytheresa's shipping and payment cost ratio by 250 basis points in Q3"* [22]. **Q4 FY26 (Apr–Jun) is the first full quarter under the new regime**, in Mytheresa's fastest-growing market (US +33.8% cc in Q3, 25.8% of segment sales [22]).
3. **IEEPA tariffs struck down by the Supreme Court 6-3 on 2026-02-20 and revoked the same day** — but **the de minimis termination and Section 232/301 remain in force** [29]. Two-sided: some ad-valorem burden reversed inside Q4, the parcel-level compliance cost did not.
4. **700-person layoff programme fully concluded**, severance paid mostly in Q3, *"full effect to be visible in Q4"* [22].
5. **Cash burn running ahead of plan**: 9M operating cash burn **€117.9m** against a **€150m** full-year maximum; management guided FY burn *"significantly better than"* €150m and Q4 operating cash flow *"slightly positive"* [22].
6. **Q4 marketing cost ratio guided higher** on US investment and promotional phasing, including *"a fantastic event in June in L.A."* [22]. A known, pre-flagged margin drag.
7. **Analyst actions:** JPMorgan (Boss) cut Overweight→Neutral, $14→$10 on 2026-02-18 over the share-count correction [16]; trimmed $10→$9 after a management meeting (date not pinned) [27]; TD Cowen raised $8→$9, Buy, on 2026-08-19 [14].

### Balance sheet and cash

| Item | Value | As of | Source |
|---|---|---|---|
| Cash and cash investments | **€436.1m** | 2026-03-31 | [8][22] |
| Total available funds | **€612.8m** | 2026-03-31 | [22] |
| Total debt | **Debt-free** | 2026-03-31 | [8][22] |
| Inventory | **€997.7m** | 2026-03-31 | [8] |
| Cash / total debt (US$) | $358.72m / $221.26m | 2026-09-15 | [13] |
| Free cash flow TTM | **−$164.98m** | 2026-09-15 | [13] |
| Going concern | Clean — *"adequate resources … for the foreseeable future"* | FY25 20-F | [17] |

Note the disagreement between the company's *"debt-free"* (€436.1m cash, 2026-03-31) and stockanalysis's $221.26m total debt / $358.72m cash [13] — most likely IFRS 16 lease liabilities being counted as debt by the data provider. I have not resolved it; the company's own statement is the higher-hierarchy source.

**Cash is ~43% of the market cap and inventory alone (€997.7m ≈ $1.16bn) exceeds it.** At 0.72× book, the market is pricing the inventory and the working capital at a discount to carrying value.

### Buyback / dilution

- **No buyback.** No dividend [13].
- **Shares outstanding +61.08% year on year** [13], from the 49,741,342 ordinary shares issued to Richemont Italia at the YNAP closing [17]. The dilution is the entire story of the share-count confusion.

### Customer concentration

- **Top customers now >40% of revenue, up from ~25–30% around the 2021 IPO** — CFO, 2026-09-14 [3].
- Mytheresa LTM active customers **774k, −7.5% YoY**; LTM AOV **€847, +12.5%**; NPS 86.8 [8].
- The 20-F carries an explicit risk factor on dependence on top customers and on the unguaranteed supply relationships with brand partners [17].
- Customer overlap between Mytheresa and NAP/MRP is *"only 10%"* per the CFO [3] — management's argument that the two brands are not cannibalising.

---

## 5. Positioning & options

### The option market does not exist

Covered in §1. To restate the load-bearing facts, all from the Yahoo chain retrieved 2026-09-14 [4]:

- Four expiries, six strikes, **zero bid on every contract in the first post-event expiry**, **95 contracts of total open interest** in that expiry, ATM call last traded 2026-05-04.
- **IV term structure: unavailable.** **Skew: unavailable.** **IV rank / percentile: unavailable** [21].
- **Put/call: not computable.** Open interest is 0 on almost every line; the one aggregator snippet claims "7 calls and 7 puts, IV near 1.67, put/call open-interest ratio around 2.06" for the 2026-09-18 expiry [30] — this contradicts the raw chain (5 calls, 5 puts, OI 95) and I do not rely on it. `snippet_only`, low confidence.
- **Unusual options activity: none, by construction.** A single 1-lot put on 2026-09-14 is the only recent trade.

**Implication for the panel:** there is no options-market opinion to fade or respect. Nobody is hedged. Whatever happens tomorrow happens in the cash market alone, into $780k/day of liquidity.

### Short interest — the dominant positioning fact

| Settlement | Shares short | Change | % of float (MarketBeat) | Days to cover (MarketBeat) |
|---|---|---|---|---|
| **2026-08-31** | **3,959,681** | **+0.3%** | 4.7% | **47.23** |
| 2026-08-14 | 3,947,000 | −0.3% | 4.7% | 25.66 |
| 2026-07-31 | 3,959,989 | +1.6% | 4.7% | 33.35 |
| 2026-07-15 | 3,898,637 | −2.2% | 4.6% | 31.05 |

Source: MarketBeat [14]. Corroborated on share count by stockanalysis: **3.95m shares short, "22.53% of shares outstanding", short ratio 34.29 days, as of 2026-09-15** [13].

Three readings of the same 3.95m shares, and the difference matters:

- vs **137.26m shares outstanding** → **2.88%**. Unremarkable.
- vs **MarketBeat's implied ~84m float** → **4.7%**. Unremarkable.
- vs **stockanalysis's 17.19m float** → **~23%**. Extreme.

stockanalysis's own "% of shares outstanding: 22.53%" is arithmetically impossible against 137m shares (that would be 30.9m shares), and 3.95/17.19 = 23.0% — so **that label is mis-stated and the figure is really % of float**. The 17.19m float is the one consistent with the ownership structure: **MYT Holding LLC ~47–48% + Richemont ~36% = ~84%** of the register in two hands [31], leaving ~16% ≈ 22m shares, of which index and long-only holdings absorb more.

**What is not in dispute, on either float estimate, is days to cover.** Using my own 20-day share ADV of 103,155 [own calc from 6], **3,959,681 / 103,155 = 38.4 days**. MarketBeat's own range across the last four settlements is **25.7 to 47.2 days**. Whichever number you take, the short book cannot exit into a positive surprise. This is the single most asymmetric feature of the setup.

- **Short interest trend: flat.** +0.3% / −0.3% / +1.6% / −2.2% across four settlements [14]. Nobody is pressing the short into the print; nobody is covering either. It is a stuck position.
- **Borrow fee / utilisation: unavailable.** No source found. Given the float, I would expect it to be non-trivial, but that is speculation and I will not put a number on it.

### Ownership and the supply overhang

| Holder | Stake | Constraint | Source |
|---|---|---|---|
| **MYT Holding LLC** | ~47.2–48.4% | No lock-up disclosed. Holds **registration rights** (A&R agreement 2024-10-07) requiring LuxExperience to file a resale registration within 180 days of written request | [17][31] |
| **Compagnie Financière Richemont** (via Richemont Italia) | **49,741,342 shares, ~36.2%** | One-year **lock-up** from the 2025-04-23 closing → **expired ~2026-04-23**. Now in a one-year **leak-out period to ~2027-04-23**, capped at **15% of that day's ADV** | [17][31] |
| Insiders (Supervisory + Management Board) | 2.48% (3,406,791 ADSs) | — | [17] |

The Richemont leak-out cap is ~15,000 shares/day at current ADV — a trickle, but it is a permanent bid-side ceiling and it is **live right now**. Richemont's CFO Burkhart Grund sits on the Supervisory Board under the Relationship Agreement [17]. The MYT Holding registration right is the larger latent overhang: a demand would put a multi-million-share secondary into a 17m-share float.

### Run-in to the print

| Window | LUXE | Sector context |
|---|---|---|
| 5 days | **−3.63%** | in line with peers (−2.7% to −7.7%) |
| 20 days | **−2.62%** | **better than every luxury peer except Zalando** |
| 60 days | −2.62% | vs LVMH −15.2%, Moncler −13.7%, Kering −10.7% |
| 120 days | −6.30% | vs S&P 500 +15.8% |

All own calculations from Yahoo daily bars, as of 2026-09-14/15 [6].

**There is no run-up to unwind.** The stock is 34.6% below its 52-week high, 13.8% above its 52-week low (set on the last earnings day), below both moving averages, and has modestly **outperformed** a luxury complex that has fallen 5–9% in twenty sessions. On the repo's own free control (`−run_up_20d_pct`), LUXE scores a weak long at +2.62.

**How crowded is the trade?** Long side: not crowded — 5 analysts, media coverage of three items in three weeks [20], and **Stocktwits shows 30 total messages stretching back to February 2026, the most recent dated 2026-06-08** [32]. There is effectively no retail participation to squeeze out. Short side: stuck, at 25–47 days to cover. The asymmetry runs long.

---

## 6. Sentiment & alt-data

### Analyst ratings and target drift

| Date | Firm | Action | PT |
|---|---|---|---|
| 2025-12 | JPMorgan (Boss) | Neutral maintained | $8 → **$9** [27] |
| 2026-02 (≈11th) | JPMorgan (Boss) | **Neutral → Overweight** | $9 → **$14** [27] |
| **2026-02-18** | **JPMorgan (Boss)** | **Overweight → Neutral**, on the share-count correction | **$14 → $10** [16] |
| 2026-08-19 | TD Cowen (Chen) | **Buy** maintained, "strong Americas performance" | $8 → **$9** [14][20] |
| undated (recent) | JPMorgan (Boss) | Neutral maintained, after a management meeting | $10 → **$9** [27] |

Earlier in 2026 TD Cowen had cut $12 → $8 [27]. Net drift over 2026: **sharply down, then stabilising in the $9–$10 zone.**

**Current consensus:**

| Metric | Value | Source |
|---|---|---|
| Rating | **Buy** (2 Strong Buy, 0 Buy, 3 Hold, 0 Sell) | stockanalysis, 2026-09-15 [20] |
| Avg PT | **$9.29** (+24.9%), range $7.70–$11.88, **5 analysts** | stockanalysis, 2026-09-15 [20] |
| Avg PT (alt) | $9.75 (+26.8% / +32.6%) | aggregator snippets [27][32] `snippet_only` |
| Avg PT (alt) | $9.50, mid-August | MarketBeat-derived snippet [27] `snippet_only` |

Every published target sits **above** spot. The low end of the range ($7.70) is only 3.5% above the current price — there is no analyst who thinks this is a short.

### Retail and social — effectively zero

- **Stocktwits: 30 messages total in the symbol stream, spanning 2026-02-12 to 2026-06-08.** Nineteen tagged Bullish, eleven untagged, **zero Bearish**. Most recent message is **99 days old** [32].
- **7/14/30-day social trend: not computable — the message volume is zero over all three windows.** That is the finding: no retail flow, no meme risk, no crowding, and no social signal either way.
- Media tone: "59% of articles about LUXE were positive this week, compared to its sector average of 57%" [32] — `snippet_only`, provider-scored, and I would not weight it.

### Alt-data proxies

| Proxy | Result |
|---|---|
| Google Trends ("mytheresa") | **Unavailable** — trends.google.com returned HTTP 429 |
| Web traffic | Only stale, non-comparable snapshots: mytheresa.com **8.12m visits (April 2026)**, net-a-porter.com **7.02m visits (March 2026)**, per Semrush-sourced snippets [33]. Different months, no YoY series, **not usable for a Q4 (Apr–Jun) read**. `snippet_only`. |
| App download ranks | **Unavailable** |
| Job postings | **Unavailable** — and note the 700-person layoff programme [22] makes headcount a poor demand proxy this year |
| Supply-chain / brand-partner commentary | Covered in §9 via Richemont and LVMH direct results |

Alt-data is the weakest area of this dossier by some margin.

---

## 7. Forensics

### The auditor issued an adverse opinion on internal control

Read directly from the FY2025 Form 20-F, filed 2025-10-30 [17]:

> *"In our opinion, because of the effect of the material weaknesses, described below, on the achievement of the objectives of the control criteria, the Company **has not maintained effective internal control over financial reporting** as of June 30, 2025"* — KPMG AG Wirtschaftsprüfungsgesellschaft (PCAOB ID 1021), auditor since 2019.

The financial statements themselves carry an **unqualified** opinion. The ICFR opinion is **adverse**. Specifically:

- The FY2024 material weakness on **risk assessment and monitoring** *"has not been fully remediated as of June 30, 2025, and therefore continues to be a material weakness."*
- **Six new material weaknesses** were identified in FY2025: control activities over financial statement disclosures; controls affected by changes in business operations; controls maintained by **service organisations**; **IT general and application controls**; controls over information supporting financial reporting; and **manual journal entries**.
- Management **excluded YNAP entirely** from the FY2025 ICFR assessment under the first-year-after-acquisition accommodation. YNAP was **27% of net revenue and 69% of total assets** at 2025-06-30 [17]. So the adverse opinion covers only the ~31% of the balance sheet that *was* assessed.
- Disclosure controls and procedures were concluded **not effective** [17].

*Colour, not load-bearing:* the 20-F contains "route cause assessment" for "root cause" and "CONSOLIDATED FINANICAL STATEMENTS" in the index header.

### And then they misstated the share count in an earnings release

On **2026-02-18**, JPMorgan downgraded Overweight → Neutral and cut $14 → $10 because *"management corrected the fully diluted share count following an error in the company's second-quarter 2026 press release,"* a correction worth *"approximately a $5 per share headwind to equity value"* — prior ~87m shares, revised **~140m** [16]. The company issued a **"CORRECTING and REPLACING Q2 FY26 Results"** press release and filed a **6-K/A on 2026-02-12** [9][15].

Sequence, with prices from [6]:

| Date | Event | Close | Move |
|---|---|---|---|
| 2026-02-09 | day before print | $7.73 | — |
| **2026-02-10** | Q2 FY26 results (with the wrong share count) | $9.36 | **+21.09%** |
| 2026-02-11 | JPMorgan upgrades to OW, PT $14 | $9.95 | +6.30% |
| **2026-02-12** | **6-K/A; correcting release.** Opens $11.28, high $11.38 (the 52-week high), closes $10.08 | $10.08 | +1.31% close, **−10.6% from the open** |
| 2026-02-18 | JPMorgan downgrades to Neutral, PT $10 | $9.89 | −3.70% |
| 2026-02-25 | — | $9.63 | — |

**This is the most important forensic fact in the dossier.** A company with an adverse ICFR opinion, an unremediated risk-assessment weakness and a specific material weakness in *"control activities over financial statement disclosures"* then published an earnings press release with a materially wrong share count. The probability of another reporting error, a correcting release, or a restated comparative on 2026-09-16 is not negligible, and the market has a fresh memory of exactly that.

### Insider activity

- **Zero Form 4s.** LuxExperience insiders became subject to Section 16 on **2026-03-18** under the **Holding Foreign Insiders Accountable Act** (signed 2025-12-18), which ended the FPI exemption and set an initial Form 3 deadline of 2026-03-18 [34]. Ten Form 3s were filed that day [15]. **In the nearly six months since, not a single Form 4 has been filed** [15]. No insider buying and no insider selling, discretionary or 10b5-1, in the entire window in which transactions have been visible. Neutral, and cleanly sourced.
- The ten March Form 3s are a **regulatory artefact, not a signal** — every FPI on the NYSE filed them the same day.
- **CEO Michael Kliger's option strikes** (Form 3, 2026-03-18) [35]: 621,961 @ $8.68; 1,036,602 @ $11.58; 402,294 @ $4.00; 1,175,867 @ $5.07; 707,332 @ $7.89 — plus 889,172 RSUs and PRSUs. At $7.44 **three of five option tranches are underwater**, including the most recent ($7.89) which is 6% out of the money. CFO Martin Beer holds 152,182 shares directly [34].
- **Rule 144 notices: 17 filed between 2025-03-11 and 2026-02-11** [15] — a steady cadence of affiliate sale notices, consistent with MYT Holding and/or insiders trimming. **I could not retrieve the individual filings (SEC rate-limited on the attempt) so I cannot attribute them or size them.** Recorded as a gap. The last one was 2026-02-11, i.e. **seven months ago and one day after the Q2 print** — the cadence appears to have stopped.

### Departures, restatements, filing cadence

- **No executive or director departures found.** Michael Kliger remains CEO (signed the 20-F 2025-10-30 [17]); Martin Beer remains CFO (signed the Q3 6-K 2026-05-19 [15]; presented at Goldman 2026-09-14 [3]).
- **No restatement.** The Q2 FY26 event was a corrected press release and a 6-K/A, not a restatement of audited financials.
- **Filing cadence: silent.** The last SEC filing of any kind is the Q3 FY26 6-K on **2026-05-19** — **119 days of nothing** [15]. The 2026-08-26 earnings-date announcement was not furnished on a 6-K. There is no pre-announcement, no 8-K-equivalent, no guidance update. As an FPI (the May 2026 6-K still checks the Form 20-F box [15]) the FY2026 annual report is due within four months of year-end, i.e. **by 2026-10-31**; last year's landed on 2025-10-30, exactly at the deadline [15].
- **Language/tone shift:** the release headlines have moved from FY25's *"Strong FY25 Results … Adj. EBITDA Growing +73%"* [11] to Q2's *"return to Adjusted EBITDA profitability, fully confirming the transformation plan targets"* [9] to Q3's *"Positive Adjusted EBITDA Profitability for the Second Consecutive Quarter, Confirming Full Fiscal Year 2026 Guidance as Transformation Plan Is Fully on Track"* [8]. The trend is from performance claims to **process-and-reaffirmation claims** — a softening, though the underlying guidance was in fact raised at Q2 [9].

---

## 8. Macro & peer read-through

### Sector regime: luxury is in a sharp drawdown right now

Own calculations from Yahoo daily bars, as of 2026-09-14/15 [6]:

| Name | Last | 5d | **20d** | 60d | 120d |
|---|---|---|---|---|---|
| **LUXE** | $7.44 | −3.63% | **−2.62%** | −2.62% | −6.30% |
| Richemont (CFR.SW) | CHF 170.80 | −7.00% | **−8.69%** | −4.23% | +23.95% |
| LVMH (MC.PA) | €408.35 | −4.27% | **−8.44%** | −15.17% | −11.68% |
| Kering (KER.PA) | €237.70 | −2.74% | **−7.55%** | −10.67% | −5.69% |
| Moncler (MONC.MI) | €44.23 | −3.76% | **−6.01%** | −13.65% | −15.14% |
| Burberry (BRBY.L) | 994.6p | −7.74% | **−5.28%** | −9.79% | −4.46% |
| Zalando (ZAL.DE) | €22.54 | −3.55% | **−1.05%** | −10.70% | +4.98% |
| Revolve (RVLV) | $20.49 | −4.03% | **−13.51%** | −0.77% | −7.62% |
| Coupang (CPNG) | $15.11 | −1.18% | **−6.27%** | −19.76% | −21.75% |
| XRT (retail ETF) | $85.52 | −2.36% | −3.86% | +1.15% | +7.09% |
| S&P 500 | 7,619.98 | −1.28% | −2.13% | +2.69% | +15.79% |

Every luxury name is below its 50-day average and the group is down 5–9% in twenty sessions against an S&P down 2.1%. **LUXE is the second-best performer in the group over that window.** Going into the print, the factor wind is against the sector but LUXE has not been the vehicle for it.

### Peers who already reported the same calendar quarter (Apr–Jun 2026)

This is the strongest available read-through, because LUXE's Q4 FY26 *is* Apr–Jun 2026.

- **Richemont Q1 FY27** (quarter ended 2026-06-30, reported 2026-07-15): group sales **€6.3bn, +20% at constant rates / +17% actual**, growth in every region, **Europe +11%**, Americas double-digit, Jewellery Maisons **+24%** (seventh consecutive double-digit quarter), Asia Pacific broadly flat with China/HK/Macau declines offset elsewhere [36]. Note Richemont owns **36% of LUXE** and its CFO sits on the Supervisory Board [17][31] — it is both a bellwether and an interested party.
- **LVMH Q2 2026**: Fashion & Leather Goods organic **+1% to €9.01bn — the first rise in two years** after seven consecutive declining quarters [37]. This is the more relevant comparator for LUXE's soft-luxury apparel mix: stabilising, not booming.
- **Revolve Q2 2026** (Apr–Jun): net sales **$347m, +12%**, EPS $0.26 vs $0.20 consensus, adj. EBITDA $27m *including a $5.6m benefit from IEEPA tariff refunds* (~160bp of gross margin), **July net sales +18%**; stock **+3.17%** on the print [38]. US online apparel demand in exactly LUXE's Q4 window was strong.
- **Coupang Q2 2026**: revenue $8.86bn, **missed by 2.2%**; gross margin −188bp; **stock −3.4%** [38]. Farfetch (Coupang-owned) cited as a growth driver in Developing Offerings but no standalone disclosure.

**Net read-through:** the demand backdrop for the Apr–Jun 2026 quarter was **good** — better than the Jan–Mar quarter LUXE last reported on. High-end held up (Richemont +20%), soft luxury inflected positive (LVMH F&LG +1%), US online apparel accelerated (Revolve +12%, July +18%). If LUXE's Q4 ex-FX growth does *not* improve on Q3's flat, that is a share-loss signal, not a market signal.

### The FX flip — a mechanical, underpriced tailwind to the headline

Own calculation from Yahoo EUR/USD daily [26]. LuxExperience reports in EUR [5][17] and sells heavily in USD and other non-EUR currencies.

| Fiscal quarter | Avg EUR/USD | Prior-year avg | **YoY change** |
|---|---|---|---|
| Q3 FY26 (Jan–Mar 2026) | 1.1705 | 1.0525 | **+11.21%** |
| **Q4 FY26 (Apr–Jun 2026)** | **1.1626** | **1.1343** | **+2.49%** |

Q3 FY26 printed **−5.2% reported** against **+0.0% ex-FX** — a ~5pp translation drag [8]. In Q4 the EUR/USD headwind is **less than a quarter as large**. Holding ex-FX growth constant, the **reported** headline should improve by roughly 3–4 percentage points purely on translation. Reported group net sales could go from −5.2% to roughly flat-to-positive without a single unit of underlying improvement. This is arithmetic, it is not in any published preview I found, and the headline is what hits the tape at 08:30 ET. **Labelled as my inference.**

### Tariffs and rates

- **De minimis: eliminated globally 2026-02-24 and still eliminated** [28][29]. Q4 FY26 is the first full quarter. Cost quantified by management at **250bp on Mytheresa's shipping-and-payment ratio** in the partial Q3 [22].
- **IEEPA: struck down 6-3 on 2026-02-20 and revoked by executive order the same day**; Section 232/301 and the de minimis termination survive [29]. Refunds of up to $175bn are flowing industry-wide — Revolve booked $5.6m of them in Apr–Jun 2026 [38]. **Whether LuxExperience, as a DDP cross-border shipper that may have been importer of record, books a similar one-off IEEPA refund in Q4 FY26 is a live upside item I could not source either way.** Flagged as an inference and a gap, not a claim.
- **Rate sensitivity: minimal.** The company is debt-free with €436.1m of cash [8][22] — net interest income, not expense.
- **Commodity sensitivity:** indirect only, via air-freight fuel surcharges, which the CEO flagged as a near-term headwind [22].

---

## 9. Bull case / bear case / base case

### Bull case

The print is a squeeze into a vacuum. **3,959,681 shares are short against a float that on the most structurally coherent estimate is ~17m shares, at 25–47 days to cover** [13][14], in a stock that trades **$782k a day** [own calc from 6] and has **no options market to hedge in** [4]. There has been **no run-up** — LUXE is −2.62% over twenty sessions while Richemont is −8.7% and LVMH −8.4% [6] — and **no retail crowding whatsoever** (30 Stocktwits messages since February, none in 99 days) [32]. Into that, the quarter should look better than the last one for reasons that are mechanical rather than hopeful: the EUR/USD translation drag collapses from 11.2% to 2.5% year on year [26], which alone should carry reported group growth from −5.2% toward flat-or-positive; the 700-person layoff programme has its **"full effect … visible in Q4"** [22]; and the demand backdrop in the exact Apr–Jun window was strong (Richemont +20% cc, LVMH F&LG's first rise in two years, Revolve +12% with July +18%) [36][37][38]. Underneath, the transformation is measurably working — NAP/MRP gross margin **+700bp YoY** and adj. EBITDA margin from −2.5% in H1 to −0.5% in Q3, YOOX from −17.3% to −5.5% [8][22] — and the CFO stood up at Goldman **two days before the print** and reaffirmed the whole framework unchanged: NAP/MRP profitable in FY27, YOOX by FY28, ~10% CAGR to €4bn at 7–9% margins [3]. The stock is **0.72× book** with **€436.1m of cash, no debt** and €997.7m of inventory against a $1.02bn market cap [5][8][13]. Every one of the five published analyst targets is above spot, the lowest at $7.70 [20]. Four of the last six prints were up and two of those were **+21.09% and +23.80%** [own calc from 6].

### Bear case

The one thing that matters is the FY27 guide, and the bar is high and pre-set. JPMorgan carries **CY2027 EBITDA of €117m** — roughly a **4.6% margin** — against an FY26 that my arithmetic puts at about **−0.14%** [16][8][9][10][22]. The CFO's own Goldman remarks have already spent the good news [3], so the guide can only match or disappoint. Meanwhile the quarter itself has three known drags management pre-flagged: **Q4 marketing cost ratio higher** on US promotional spend and a June LA event, **Q4 adj. EBITDA only "around Q3 levels"** (≈0.9%), and **US tariff changes already costing 250bp** of Mytheresa's shipping-and-payment ratio in a *partial* quarter — with Q4 the first *full* quarter of the de minimis elimination in the segment's fastest-growing market [22][28][29]. The growth quality is deteriorating underneath: **Mytheresa's active customers fell 7.5% YoY** while AOV rose 12.5%, and **top customers are now >40% of revenue versus 25–30% at the IPO** [8][3] — a narrower and narrower base. Two of three segments are still shrinking ex-FX (NAP −5.1%, YOOX −7.4%) [8]. And the reporting is not trustworthy: **KPMG issued an adverse ICFR opinion for FY2025** with one unremediated prior-year weakness and six new ones including manual journal entries and disclosure controls, with **YNAP — 69% of total assets — excluded from the assessment entirely** [17]; seven months ago the company then **misstated its own diluted share count in an earnings press release**, a $5/share error that forced a 6-K/A and a JPMorgan downgrade [16][15]. Consensus is incoherent as a direct result (−$0.11 / −$0.17 / FY −$0.48 / −$0.79 / −€1.20) [0][12][18][19][20], the company has beaten EPS **once in four quarters** [23], the luxury complex is down 5–9% in twenty sessions [6], **Richemont's 49.7m-share lock-up expired in April 2026** and it is now free to leak out at 15% of a $782k ADV [17], MYT Holding's registration right sits unexercised over ~47% of the register [17][31], and the last print was **−11.81%** [own calc from 6].

### Base case

A messy headline followed by a call that decides everything. FY26 GMV and adjusted EBITDA margin both land inside guidance (my derivation: ~€2.58bn and ~−0.1%), which is worth nothing because management effectively pre-announced it on the Q3 call [22]. Reported revenue growth looks conspicuously better than Q3's −5.2% on the FX flip [26], but the comparison is muddied by THE OUTNET's IFRS 5 reclassification [25] and by a consensus revenue figure ($739.43M ≈ €636m) that may not be restated for it [19] — so a presentational "revenue miss" headline at 08:30 ET is a real possibility even on a fine quarter. EPS misses, as it almost always does, and as usual nobody trades on it [23][12]. The stock then moves on the FY27 adjusted EBITDA margin guide: **~3–5% with high-single-digit-plus ex-FX growth and NAP/MRP guided profitable is a clear positive** into a short book that needs 25–47 days to cover; **below ~2%, or any softening of the €4bn / 7–9% medium-term language, and the May 2026 pattern repeats.** I lean modestly positive — the positioning asymmetry, the absent run-up, the mechanical FX relief and the CFO's unchanged framework 48 hours out outweigh a steep FY27 bar — but the conviction is low and the magnitude conviction is far higher than the direction conviction. Sizing should respect a distribution whose last six realised moves had a **12.76% median absolute** value and a 23.80% maximum, in a name with **$782k of daily liquidity and no options to hedge in**.

**Preliminary direction score: +15. Preliminary probability of an up move: 55%.** Conviction in my own read: **Low-Med**.

---

## 10. What would flip the consensus view

The most credible reversal is **not** a bad quarter — it is a **credible, quantified FY27 guide that the market cannot dismiss, delivered into the most illiquid short book in the day's universe.**

Concretely: if on the 08:00 ET call management guides FY27 to **group adjusted EBITDA margin of 4% or better** on **high-single-digit or better ex-FX net sales growth**, with **NAP/MRP explicitly guided to positive adjusted EBITDA for the full year** and the €4bn / 7–9% medium-term framework reaffirmed with a dated path — then the €117m CY27 EBITDA that JPMorgan already carries [16] stops being a hopeful model input and becomes company guidance. At 8× that is JPMorgan's own $10 target, 34% above spot, on a stock at 0.72× book with 43% of its market cap in cash [5][13]. The short book is 3.96m shares and the stock trades 103k shares a day [6][14]; there is no option market to hedge into [4] and no retail float to sell into [32]. The mechanics of that unwind are what produced **+21.09%** on 2026-02-10 and **+23.80%** on 2025-02-11 [own calc from 6].

The mirror image — and the reason my conviction is low — is equally concrete and needs no bad quarter either: **FY27 guided to ~1–2% adjusted EBITDA margin**, or the €4bn target re-described as "beyond FY29", or (worst) **a second reporting error or a restated comparative in the release itself**, given the adverse ICFR opinion and the February precedent [16][17]. Any of those and the 2026-05-19 template repeats: gapped −6.4% and closed −11.8%, with the session *extending* the gap.

Three cheap tells to watch in order, all resolvable within minutes of 08:30 ET:
1. **Is the FY27 adjusted EBITDA margin guided as a number, or only as "improving"?** A qualitative guide is itself the bear outcome.
2. **Does the release restate the prior-year comparatives for THE OUTNET discontinued operation?** If not, the headline growth rate is not what it appears.
3. **The open.** Gap and close have agreed in direction 8 of 8 prints [own calc from 6]; but the session extended the gap in only 5 of 8, and the two fades were violent (−11.0% intraday on 2025-09-25). Direction is readable at 09:30; magnitude is not.

---

## 11. Coverage gaps

| Gap | Why it matters |
|---|---|
| **No event-implied move, no IV, no IV rank, no skew, no term structure** | The chain exists but is not a market: zero bids, 95 contracts of OI in the front expiry, ATM call last traded 2026-05-04 [4]. optioncharts is paywalled [21]. The panel has no market-priced expectation to anchor on; my 11–12% proxy is a historical-reaction estimate plus one 1-lot put print, not a quote. **This is the single biggest gap.** |
| **Put/call ratio not computable** | Open interest is 0 on almost every line. The one published figure (2.06) contradicts the raw chain and is unusable [30]. |
| **Borrow fee and utilisation unavailable** | With 25–47 days to cover on a possibly-17m-share float, the borrow rate is the direct measure of squeeze pressure. Its absence means I can assert the days-to-cover asymmetry but cannot price it. |
| **Float is unresolved: 17.19m [13] vs MarketBeat's implied ~84m [14]** | Changes short-interest-as-%-of-float from ~23% to 4.7% — i.e. from "extreme" to "unremarkable". I argue for the low float from the 47%+36% ownership structure [31] and from the $782k ADV, but I could not source a definitive free-float figure. Days-to-cover (25–47) is unaffected and is the more robust statistic. |
| **Consensus EPS is incoherent across five providers** (−$0.11 / −$0.17 / FY −$0.48 / −$0.79 / −€1.20) | No reliable "bar" on the bottom line. Any beat/miss headline tomorrow is near-meaningless. Root cause is the 87m-vs-140m share-count error [16]. |
| **Discrete 30/60/90-day estimate revisions unavailable** | Only "1 up / 2 down over 3 months" [19] and an undated FY26 EPS walk from −€1.03 to −€1.20 [18]. |
| **No credibly published whisper number** | — |
| **No published Street expectation for the one metric** (FY27 adj. EBITDA margin) | The closest proxy is JPMorgan's CY27 EBITDA of €117m [16], which I converted to ~4.6% myself. There is no consensus FY27 margin. |
| **Whether consensus revenue $739.43M is restated for THE OUTNET discontinued operation** | Determines whether a headline revenue "miss" tomorrow is real or presentational [19][25]. |
| **Q4 FY25 group comparatives (with YNAP, ex-OUTNET) not sourced** | Nasdaq returned 503, the IR PDFs are image-heavy and did not parse. I therefore cannot state the YoY base for Q4 FY26 group GMV/net sales, only Mytheresa's (€265.9m GMV, €248.9m net sales, 6.5% adj. EBITDA margin) [11]. |
| **Form 144 filings not retrieved** (17 between 2025-03-11 and 2026-02-11) | SEC rate-limited the request. I cannot attribute or size affiliate selling — the only channel through which MYT Holding's ~47% stake becomes visible, since it files no Form 4s. |
| **Google Trends unavailable** (HTTP 429); web traffic stale and non-comparable; no app-rank or job-postings data | No independent demand proxy for the Apr–Jun quarter. Alt-data is the weakest section here. |
| **7/14/30-day social sentiment trend not computable** | Stocktwits volume is zero across all three windows (last message 2026-06-08) [32]. Reported as the finding rather than imputed. |
| **Whether LuxExperience books an IEEPA tariff refund in Q4 FY26** | Revolve booked $5.6m in the same calendar quarter [38]. A one-off refund would flatter Q4 adj. EBITDA. Could not source either way. |
| **Debt figure disagrees**: company says "debt-free" [22], stockanalysis says $221.26m total debt [13] | Probably IFRS 16 leases. Unresolved but low impact. |
| **Domains unreachable / degraded this run** | trends.google.com (429); nasdaq.com press release (503); stocktitan Q3 permalink (410); sec.gov (429 on three attempts, mitigated by pacing); optioncharts.io (paywall); Yahoo v7 options and quoteSummary required a cookie-and-crumb handshake; company IR PDFs on s206.q4cdn.com returned image-only PDFs that would not parse to text. |

---

## 12. Sources

| # | URL | What it supports |
|---|---|---|
| 0 | `/home/user/claude_research/research/2026/09/2026-09-15/00-universe.json` | Nasdaq-sourced quarter EPS estimate −$0.17, analyst count 2, session bmo, event date 2026-09-16, market cap $1.0078bn |
| 1 | https://investors.luxexperience.com/news/news-details/2026/LuxExperience-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Earnings-Release-and-Conference-Call-Participating-in-Upcoming-Investor-Conference/default.aspx | **Event confirmation**: Q4/FY2026 results before the US market open 2026-09-16, call 08:00 ET |
| 2 | https://www.stocktitan.net/news/LUXE/lux-experience-announces-fourth-quarter-and-full-fiscal-year-2026-2wewlwz2rmu5.html | Same, plus release published 2026-08-26 08:00, and CFO Martin Beer at Goldman Sachs Global Consumer and Retail Conference, New York, Sept 14–15 2026 |
| 3 | https://www.investing.com/news/transcripts/luxexperience-at-goldman-sachs-conference-top-customers-drive-growth-93CH-4899755 | CFO remarks 2026-09-14: Mytheresa FY26 ~6% adj. EBITDA margin; NAP/MRP breakeven FY26 → profitable FY27; YOOX profitable by FY28; ~10% CAGR to €4bn at 7–9%; top customers >40% of revenue vs 25–30% at IPO; AOV >€800; US +20–30%; "K-shaped" luxury; 10% customer overlap; fine jewellery push with Richemont brands |
| 4 | https://query2.finance.yahoo.com/v7/finance/options/LUXE (expiries 2026-09-18, 2026-10-16, 2026-12-18) | **Full option chain**: four expiries, six strikes, zero bids, 95 contracts OI in the front expiry, ATM call last traded 2026-05-04, the single $7.50 put print at $0.45 on 2026-09-14 |
| 5 | https://query2.finance.yahoo.com/v7/finance/quote?symbols=LUXE | Spot $7.44 @ 2026-09-14T20:00Z, market cap $1,021,226,304, 137,261,608 shares, book value $10.29, P/B 0.72, 52wk 6.54–11.38, ADV10 121,660 / ADV3m 125,147, financialCurrency EUR, `earningsTimestamp` 2026-09-16 08:30 ET with `isEarningsDateEstimate: false`, epsCurrentYear −0.4816, epsForward −0.0816 |
| 6 | https://query1.finance.yahoo.com/v8/finance/chart/LUXE?range=5y&interval=1d | **All historical earnings-day moves, run-ups, realised vol, ADV** (1,254 daily bars, 2021-09-15 → 2026-09-14). Also used for all peer/index run-ups. |
| 7 | https://investors.mytheresa.com/news/news-details/2024/Mytheresa-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2024-Earnings-Release-and-Conference-Call/default.aspx | FY24 Q4 reported BMO 2024-09-12 |
| 8 | https://investors.luxexperience.com/news/news-details/2026/Q3-FY26-Results-LuxExperience-Group-Reports-Positive-Adjusted-EBITDA-Profitability-for-the-Second-Consecutive-Quarter-Confirming-Full-Fiscal-Year-2026-Guidance-as-Transformation-Plan-Is-Fully-on-Track/default.aspx (and https://www.stocktitan.net/news/LUXE/q3-fy26-results-lux-experience-group-reports-positive-adjusted-1qzs1dwtpk98.html) | **Q3 FY26 full detail**: group GMV €653.7m (−4.9% / +0.3% ex-FX), net sales €618.4m (−5.2% / +0.0% ex-FX), gross margin 45.5%, adj. EBITDA €5.7m (0.9%), net loss €31.2m, SG&A 18.3%; Mytheresa GMV €279.6m (+11.3% ex-FX), net sales €256.0m (+9.9% ex-FX), GM 47.1%, adj. EBITDA €14.1m (5.5%), active customers 774k (−7.5%), AOV €847 (+12.5%), NPS 86.8; NAP/MRP net sales €231.6m (−5.1% ex-FX), GM 48.5% (+700bp), adj. EBITDA −€1.1m (−0.5%); YOOX net sales €130.7m (−7.4% ex-FX), adj. EBITDA −€7.2m (−5.5%); cash €436.1m, debt-free, inventory €997.7m; FY26 guidance GMV €2.5–2.7bn and adj. EBITDA margin −1% to +1% |
| 9 | https://investors.luxexperience.com/news/news-details/2026/CORRECTING-and-REPLACING-Q2-FY26-Results-LuxExperience-Group-reports-Net-Sales-growth-of-5-7-ex-FX-and-return-to-Adjusted-EBITDA-profitability-fully-confirming-the-transformation-plan-targets-4f2057ca0/default.aspx (and https://www.stocktitan.net/news/LUXE/q2-fy26-results-lux-experience-group-reports-net-sales-growth-of-5-7-y8sglcjhqdmr.html) | **Q2 FY26** GMV €684.8m (+4.7% ex-FX), net sales €645.1m (+5.7% ex-FX), adj. EBITDA €13.2m (2.0%), net loss €12.6m, cash €44.4m at 2025-12-31, inventory €1,033.1m, 6M operating cash flow −€29.3m; **guidance raised** to GMV €2.5–2.7bn (from €2.4–2.7bn) and margin −1%/+1% (from −2%/+1%); **and the existence of a "CORRECTING and REPLACING" release** |
| 10 | https://www.businesswire.com/news/home/20251119052534/en/Q1-FY26-Results-... | **Q1 FY26** GMV €589.0m (−4.3% vs €615.3m), net sales €557.2m (−4.2% vs €581.8m), adj. EBITDA margin −5.0%, gross margin 44.1% (+190bp); Mytheresa GMV €245.9m (+13.5%), net sales €226.3m (+12.2%); YOOX GMV €118.6m (−19.3%), margin −18.1% |
| 11 | https://www.businesswire.com/news/home/20250925296884/en/Q4-FY25-and-Full-FY25-Results-... | **Q4 FY25** reported BMO 2025-09-25; Mytheresa Q4 net sales €248.9m (+11.5%), GMV €265.9m (+11.1%), adj. EBITDA margin 6.5% (+180bp); FY25 margin 4.9%; YNAP consolidated for the first time; medium-term 10–15% growth, €4bn, 7–9% reaffirmed |
| 12 | https://www.marketbeat.com/stocks/NYSE/LUXE/earnings/ | Report date 2026-09-16 "Before Market Opens", **Confirmed**; Q1 FY26 consensus −$0.28 vs actual −$0.71 (missed by $0.43), revenue est $680.63m vs actual $670.38m; current-year EPS consensus ($0.79), next-year ($0.36) |
| 13 | https://stockanalysis.com/stocks/luxe/statistics/ and https://stockanalysis.com/stocks/luxe/ | Price $7.44 @ 2026-09-14 16:00 EDT; market cap $1.02bn; EV $883.76m; shares 137.26m; **float 17.19m**; YoY share change **+61.08%**; **short interest 3.95m shares, "22.53%", short ratio 34.29 days, as of 2026-09-15**; beta 1.06; 50d $7.86 / 200d $8.28; P/E 1.92, P/S 0.36, EV/EBITDA 1.27; revenue TTM $2.81bn, net income $533.05m, FCF −$164.98m, cash $358.72m, debt $221.26m; next earnings 2026-09-16 |
| 14 | https://www.marketbeat.com/stocks/NYSE/LUXE/short-interest/ and https://www.marketbeat.com/instant-alerts/td-cowen-increases-luxexperience-bv-nyseluxe-price-target-to-900-2026-08-19/ | **Short interest history**: 2026-08-31 3,959,681 (+0.3%, 4.7% of float, 47.23 DTC); 2026-08-14 3,947,000 (25.66 DTC); 2026-07-31 3,959,989 (33.35); 2026-07-15 3,898,637 (31.05); ADV 99,252. Plus **TD Cowen $8 → $9, Buy, 2026-08-19** |
| 15 | https://data.sec.gov/submissions/CIK0001831907.json and https://www.sec.gov/Archives/edgar/data/1831907/000110465926063602/tm2612972d1_6k.htm | **Full filing history**: last filing of any kind is the Q3 FY26 6-K on 2026-05-19; 6-K/A on 2026-02-12; ten Form 3s on 2026-03-18; **zero Form 4s ever**; 17 Form 144s 2025-03-11 → 2026-02-11; 20-F filed 2025-10-30. The 2026-05-19 6-K cover page still checks **Form 20-F** (FPI status intact) and is signed by CFO Dr. Martin Beer |
| 16 | https://www.investing.com/news/analyst-ratings/jpmorgan-downgrades-luxexperience-stock-rating-on-share-count-issue-93CH-4510524 | **2026-02-18**: JPMorgan (Boss) Overweight → Neutral, $14 → $10; *"management corrected the fully diluted share count following an error in the company's second-quarter 2026 press release"*; ~87m → ~140m shares; *"approximately a $5 per share headwind to equity value"*; CY27 EBITDA estimate held at **€117m**, valued at 8× over ~140m shares; risk/reward band $6–$11 |
| 17 | https://www.sec.gov/Archives/edgar/data/1831907/000110465925104454/luxe-20250630x20f.htm | **FY2025 Form 20-F, filed 2025-10-30.** Auditor **KPMG AG Wirtschaftsprüfungsgesellschaft (PCAOB ID 1021), since 2019**; **adverse opinion on ICFR** as of 2025-06-30; unremediated FY24 risk-assessment material weakness plus six new ones; YNAP (27% of revenue, **69% of total assets**) excluded from the ICFR assessment; disclosure controls not effective; unqualified opinion on the financial statements; going concern clean. Also: **Richemont Italia lock-up over 49,741,342 shares for one year from the 2025-04-23 closing, then a one-year leak-out capped at 15% of ADV**; A&R MYT Holding Registration Rights Agreement (2024-10-07, 180-day filing obligation); Voting Agreement; Relationship Agreement (Richemont board nominee Burkhart Grund, Richemont CFO); board/management beneficial ownership 3,406,791 ADSs (2.48%); FY25 segment figures (Mytheresa €916.1m net sales / €988.5m GMV; NAP & MRP illustrative €1,048.8m / €1,098.7m); top-customer and brand-partner risk factors |
| 18 | https://simplywall.st/community/narratives/us/retail/nyse-luxe/luxexperience-bv/... | FY26 consensus loss per share widened **−€1.03 → −€1.20**; consensus PT **$10.38 → $9.25**; 6 analysts revised targets. *Undated — snippet_only* |
| 19 | https://wp.madrestravels.com/2026/09/14/luxexperience-b-v-q4-2026-earnings-preview/ | Consensus EPS **−$0.11** (−102.4% YoY), revenue **$739.43M** (+197.1% YoY); 3-month revisions 1 up / 2 down on both EPS and revenue. *Low-quality aggregator; it also states the wrong session ("Tuesday September 15th, after market close"), contradicting [1][2]. snippet_only* |
| 20 | https://stockanalysis.com/stocks/luxe/forecast/ | Consensus **Buy**; avg PT **$9.29** (+24.87%), range $7.70–$11.88, **5 analysts**; 2 Strong Buy / 3 Hold; FY26 revenue $2.46bn (+95.27%), FY27 $2.60bn (+5.40%); FY26 EPS −$0.48, FY27 −$0.07; three analyst actions dated early-to-late August 2026 |
| 21 | https://optioncharts.io/options/LUXE/volatility-skew | **No IV data accessible** — paywalled |
| 22 | https://www.fool.com/earnings/call-transcripts/2026/05/19/luxexperience-luxe-q3-2026-earnings-transcript/ | **Q3 FY26 call**: *"Same as last year, we will communicate our fiscal year '27 guidance in our Q4 earnings call"*; Q4 adj. EBITDA **"around Q3 levels"**; Q4 marketing cost ratio higher (US investment, June LA event); Q4 operating cash flow "slightly positive"; 9M operating cash burn **€117.9m** vs €150m max; **US tariff changes +250bp on Mytheresa shipping-and-payment cost ratio**; Mytheresa US +33.8% cc, 25.8% of segment sales; NAP/MRP to break even in H2 FY26, top-line reacceleration "as of Q4", 1,000bp+ SG&A-ratio opportunity vs Mytheresa's 12.2%; YOOX profitable in 12–15 months, top-line growth in FY27; *"Every year, will continue to see increasing adjusted EBITDA margins to 7% to 9%"*; **700-person layoff concluded, "full effect to be visible in Q4"**; cash €436.1m, total available funds €612.8m, debt free; inventory Mytheresa +3.1%, NAP/MRP +2.8%, YOOX −11%; Asia "seen the bottom"; air-freight fuel surcharges a headwind |
| 23 | https://finance.yahoo.com/markets/stocks/articles/luxexperience-b-v-sponsored-adr-140005343.html | Zacks preview 2026-05-12: ESP **+22.58%**, Rank #3 (Hold), Q3 consensus **−$0.16**, revenue $734.21m (+187.8%); prior quarter est −$0.08 vs actual −$0.17 (**−112.5% surprise**); **beaten consensus just once in the last four quarters** |
| 24 | https://investors.luxexperience.com/news/news-details/2025/LuxExperience-Has-Reached-an-Agreement-to-Sell-the-Set-of-Assets-Powering-THE-OUTNET-Platform... | THE OUTNET asset sale agreed 2025-10-31 to The O Group LLC for **USD 30m**; closed 2026-04-30; transfer of brand rights, customer data, full inventory, US DC and workforce; ongoing at-cost service arrangement |
| 25 | https://www.theglobeandmail.com/investing/markets/stocks/LUXE-N/pressreleases/2039966/luxexperience-files-q3-fy-2026-interim-report-and-reclassifies-the-outnet-as-discontinued-operation/ | 2026-05-20: **THE OUTNET reclassified as a discontinued operation under IFRS 5**; illustrative comparatives for the April 2025 YNAP acquisition |
| 26 | https://query1.finance.yahoo.com/v8/finance/chart/EURUSD=X?range=2y&interval=1d | **FX**: avg EUR/USD Q3 FY26 (Jan–Mar 2026) **1.1705** vs 1.0525 (+11.21% YoY); Q4 FY26 (Apr–Jun 2026) **1.1626** vs 1.1343 (**+2.49% YoY**); latest 1.1542 on 2026-09-15 |
| 27 | https://www.gurufocus.com/news/8628023/jp-morgan-downgrades-luxexperience-luxe-and-lowers-price-target-luxe-stock-news and https://www.tipranks.com/stocks/luxe/forecast | JPMorgan rating/PT timeline: Dec-2025 $8→$9 Neutral; Feb-2026 upgrade to OW $9→$14; downgrade to Neutral $14→$10; most recently **$10→$9 Neutral after a management meeting** (date not pinned). Consensus PT $9.75 / $9.35. *snippet_only* |
| 28 | https://blog.gettransport.com/logistics-guide/us-de-minimis-suspension-2026-importer-status-guide/ and https://carraglobe.com/us-de-minimis-exemption-suspended-2026/ | **US $800 de minimis exemption eliminated globally effective 2026-02-24**; formal customs entry required on every shipment regardless of value; broker fees $150–$300 per formal entry |
| 29 | https://www.whitecase.com/insight-alert/united-states-terminates-ieepa-based-tariffs-following-supreme-court-decision and https://www.congress.gov/crs-product/LSB11398 | **Supreme Court 6-3 struck down IEEPA tariffs 2026-02-20**; revoked by executive order the same day; **de minimis termination and Section 232/301 remain in effect**; up to $175bn of refunds projected |
| 30 | https://www.barchart.com/etfs-funds/quotes/LUXE | Claimed 2026-09-18 chain: 7 calls / 7 puts, IV ~1.67, put/call OI ~2.06. **Contradicts the raw chain [4]; not relied upon.** *snippet_only* |
| 31 | https://simplywall.st/stocks/us/retail/nyse-luxe/luxexperience-bv/ownership and https://www.marketscreener.com/quote/stock/LUXEXPERIENCE-B-V-117926049/company/ | Ownership: **MYT Holding LLC ~47.2–48.4%**, **Richemont ~35–36.2%**, individual insiders 2.33%, institutions 15.2% |
| 32 | https://api.stocktwits.com/api/2/streams/symbol/LUXE.json and https://www.thecerbatgem.com/2026/09/05/head-to-head-comparison-luxexperience-b-v-luxe-vs-its-competitors.html | **Stocktwits: 30 total messages, 2026-02-12 → 2026-06-08, 19 Bullish / 0 Bearish / 11 untagged; most recent 99 days old.** Plus consensus PT $9.75 and "59% of articles positive this week vs sector 57%" *(snippet_only)* |
| 33 | https://www.similarweb.com/website/mytheresa.com/ and https://www.semrush.com/website/net-a-porter.com/competitors/ | mytheresa.com 8.12m visits (April 2026), net-a-porter.com 7.02m visits (March 2026). **Different months, no YoY series — not usable for the Apr–Jun quarter.** *snippet_only* |
| 34 | https://corpgov.law.harvard.edu/2026/01/18/section-16a-insider-reporting-legislation-ends-foreign-private-issuer-exemption/ and https://www.dorsey.com/newsresources/publications/client-alerts/2025/12/section-16-reporting-requirements | **Holding Foreign Insiders Accountable Act signed 2025-12-18**; FPI officers/directors became Section 16 reporters with initial Form 3 due **2026-03-18** — explaining the ten simultaneous Form 3s as a regulatory artefact. Also CFO Martin Beer 152,182 shares direct; director Burkhart Grund zero shares; director Nora Aufreiter 76,477 shares |
| 35 | https://www.sec.gov/Archives/edgar/data/1831907/000110465926030521/xslF345X06/tm268949-10_3seq1.xml | **CEO Michael Kliger Form 3, 2026-03-18**: options 621,961 @ $8.68 (exp 2031-01-20), 1,036,602 @ $11.58, 402,294 @ $4.00 (exp 2033-07-01), 1,175,867 @ $5.07 (exp 2034-07-01), 707,332 @ $7.89 (exp 2035-07-01); RSUs 468,958 + 283,332 + 136,882; plus PRSUs |
| 36 | https://www.richemont.com/news-media/press-releases-news/richemont-posts-strong-start-to-the-year-with-sales-up-by-20-at-constant-rates-for-its-first-quarter-ended-30-june-2026/ | **Richemont Q1 FY27 (quarter ended 2026-06-30, reported 2026-07-15)**: sales €6.3bn, **+20% cc / +17% actual**; Europe +11%; Americas, Asia Pacific and Japan double-digit; Middle East & Africa back to growth; Jewellery Maisons +24%; Asia Pacific flat with China/HK/Macau declines offset |
| 37 | https://wwd.com/business-news/financial/lvmh-fashion-leather-goods-q2-2026-increase-1239083331/ | **LVMH Q2 2026 Fashion & Leather Goods organic +1% to €9.01bn — first rise in two years** after seven declining quarters |
| 38 | https://www.prnewswire.com/news-releases/revolve-group-announces-second-quarter-2026-financial-results-302842702.html and https://finance.yahoo.com/markets/stocks/articles/q2-online-retail-earnings-review-192052687.html | **Revolve Q2 2026**: net sales $347m (+12%), EPS $0.26 vs $0.20 consensus, adj. EBITDA $27m including **$5.6m of IEEPA tariff refunds** (~160bp of gross margin, $0.06/share), July net sales **+18%**, stock +3.17%. **Coupang Q2 2026**: revenue $8.86bn, missed by 2.2%, gross margin −188bp, stock −3.4% |

---

*This is research, not investment advice. The output is a forecasting exercise over public information and must not be presented as investment advice. Every company-specific figure above is either sourced to a URL or explicitly marked unavailable; figures marked as derived or inferred are the author's own calculations from sourced inputs and are labelled as such.*
