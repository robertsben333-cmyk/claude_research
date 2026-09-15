# TCOM — Trip.com Group Limited

**Dossier as of 2026-09-15 ~09:00 UTC. `event_confirmed: true`** — the date and session are confirmed from the company's own 6-K exhibit filed with the SEC on 2026-09-02 [1].

**What this print is about.** This is not a demand quarter, it is a *take-rate and regulatory-reset* quarter. On 2026-01-14 China's SAMR opened an Anti-Monopoly Law probe into Trip.com; the ADS fell 17.05% that day [2][21]. On 2026-07-25 SAMR closed it with a total penalty of RMB5,301m (US$781.3m): RMB122m of hotel security deposits refunded, RMB1,658m of gains confiscated and a RMB3,521m fine equal to 7.5% of 2025 China revenue — the largest platform penalty since Alibaba in 2021 [3][4]. Trip.com "sincerely accepted" it and committed to dismantle the machinery that produced the profits: no more hotel exclusivity, no more "lowest-price-across-the-internet" requirements, no more unilateral rate changes, and the Tier-1 delegated distribution programme is being wound down into a new multi-tier framework [3][5][6]. So the print has three jobs at once: (i) land Q2 revenue inside a guide of +3–8% YoY that management set on 2026-06-24 and that the stock fell 12.55% on [7][8]; (ii) tell the market how and when the RMB5.3bn penalty hits the P&L, since the decision post-dates the 30 June balance-sheet date [9]; and (iii) — the part that actually matters — quantify what the remediated hotel model does to accommodation take rate and margin from Q3 onward. The stock comes in at a 52-week low, down 13.1% in 20 sessions and 50.5% from its 2026-01-12 high, having underperformed KWEB by ~4.7pp over the same 20 sessions [10][11]. Everything bad is known; almost nothing about the *new* economics is quantified.

---

## 1. Event & anchors

| Item | Value | Source / note |
| --- | --- | --- |
| Event confirmed | **Yes** | Company 6-K exhibit, filed 2026-09-02 [1] |
| Report date | **2026-09-15 (Tue), U.S. time** | [1] |
| Session | **amc** — "after the market closes" | [1] |
| Conference call | **20:00 ET 2026-09-15** (08:00 HKT 2026-09-16) | [1]. Note: unusually late even for TCOM (prior calls 19:00 ET) |
| Fiscal period | **Q2 2026 and H1 2026**, three and six months ended 2026-06-30 | [1] |
| HK release | Before HKEX trading 2026-09-16 | [1] |
| Audit committee approval | Met 2026-09-14 to approve results | [1] |
| Date changed / pre-announcement | No date change announced. **But the cadence has slipped since the probe** — see Forensics §8 | [1][12][13] |
| Spot | **$39.08**, close 2026-09-14 16:00 ET (20:00Z) | Yahoo chart API, `regularMarketTime` 2026-09-14T20:00Z [10] |
| Pre-market 2026-09-15 | $39.55 (+1.20%) | stockanalysis.com, as-of 2026-09-15 [14] — `snippet_only` |
| Market cap | **$24.61bn** (629.71m shares × $39.08) | [14] |
| 52-week range | **$38.04 – $78.99**; stock is at the low end | [14]; series low close $38.70 on 2026-09-10 [10] |
| Trailing P/E | 5.93 — distorted by fair-value gains (see §5) | [14] |
| Event-implied move | **≈7.0%** (range 6.2–8.0%) | My own computation from the 2026-09-18 chain, below |
| IV rank / percentile | **unavailable** | No IV history source reachable |
| Front-week ATM IV (18 Sep) | **~83%** | Derived, below |
| 30-day ATM IV (16 Oct) | **~38.6%** | Derived, below |
| 90-day ATM IV (18 Dec) | **~38.7%** | Derived, below |
| 20d / 60d realised vol | **28.9% / 39.9%** annualised | Computed from [10] |
| 20d ADV / $ADV | 3.15m sh / **$133m** a day | Computed from [10] — no capacity constraint |

### Implied move — how I got it, and its confidence

`WebFetch` to Market Chameleon was refused (Access Denied) and no published implied-move figure for this event was findable, so this is **my own calculation**, not a cited third-party number. Source: Yahoo's option chain API for TCOM, expiry 2026-09-18 (the first expiry after the print), snapshot taken 2026-09-15, quote timestamp 2026-09-14T20:00Z [15].

- Nearest strike to spot is **$40** (chain is $5-wide — coarse for a $39 stock). Call last $1.00, put last $1.84; straddle $2.84 = **7.27% of spot**.
- Put-call parity checks out (C−P = −0.84 vs S−K = −0.92), so the two prices are internally consistent rather than stale in opposite directions.
- Black-Scholes on those prices, T = 4 calendar days, r = 4.1%: call IV 85.1%, put IV 81.3%, **ATM IV ≈ 83.2%**. That gives E|move| to expiry = **6.95%** and a 1σ move of 8.71%.
- The 0.85×straddle convention gives **6.18%**.
- Front-vs-back vol decomposition (83.2% front-week against 38.6% at 16 Oct) isolates an earnings-day move of **~8.0%**.

**I use 7.0% as the central estimate with a 6.2–8.0% band.** Caveats the panel should weigh: bid/ask fields were zeroed in the snapshot (post-close), reported open interest was implausible (728 calls / 5 puts), and the $5 strike grid forces a 0.92-point moneyness adjustment. Treat this as a good-faith derived anchor, not a vendor print. The term structure is the strongest evidence it is right: **83% front-week against 38.6% at one month and 38.7% at three months** is a textbook single-event vol kink.

### Realised one-day earnings moves — computed, not sourced from a vendor

Report dates confirmed individually from company releases [1][7][12][13][16][17][18]; close-to-close moves computed from the Yahoo daily series [10]. All eight prints are `amc`, so the reaction is the next session.

| Quarter | Reported (amc) | Reaction day | Prev close | Open (gap) | Close | **1-day move** | Volume |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q2 2024 | 2024-08-26 | 2024-08-27 | 42.34 | 46.45 (+9.71%) | 45.97 | **+8.57%** | 9.5m |
| Q3 2024 | 2024-11-18 | 2024-11-19 | 61.32 | 63.90 (+4.21%) | 62.74 | **+2.32%** | 5.7m |
| Q4 2024 | 2025-02-24 | 2025-02-25 | 64.66 | 59.04 (−8.69%) | 57.30 | **−11.38%** | 17.8m |
| Q1 2025 | 2025-05-19 | 2025-05-20 | 67.10 | 63.65 (−5.14%) | 63.38 | **−5.54%** | 7.6m |
| Q2 2025 | 2025-08-27 | 2025-08-28 | 65.29 | 70.19 (+7.50%) | 75.03 | **+14.92%** | 9.0m |
| Q3 2025 | 2025-11-17 | 2025-11-18 | 70.89 | 70.96 (+0.10%) | 72.44 | **+2.19%** | 2.8m |
| Q4 2025 | 2026-02-25 | 2026-02-26 | 53.66 | 52.18 (−2.76%) | 52.27 | **−2.59%** | 6.6m |
| Q1 2026 | 2026-06-24 | 2026-06-25 | 46.30 | 40.16 (−13.26%) | 40.49 | **−12.55%** | 14.4m |

- **Eight quarters:** mean |move| **7.51%**, median |move| **7.05%**, max |move| **14.92%**, **4 up / 4 down**.
- **Last six quarters:** [−11.38, −5.54, +14.92, +2.19, −2.59, −12.55] → mean |move| **8.20%**, median **8.46%**, max **14.92%**, **2 up / 4 down**.
- **Pattern worth naming:** the last two prints were both down and the direction has alternated in runs, not randomly. The gap and the close agree in direction on 8 of 8 — TCOM does not round-trip its earnings gap. On 6 of 8 the close extended the gap.
- **Implied vs realised:** 7.0% implied against an 8.20% six-quarter mean absolute. Options are mildly *cheap* versus this stock's own recent earnings behaviour.

---

## 2. The bar

| Item | Value | Source |
| --- | --- | --- |
| Consensus EPS (Q2 2026, non-GAAP/ADS) | **$0.8730** | Zacks via Yahoo [19] — `snippet_only` |
| Street EPS range cited | $0.87 – $0.98 | [20] — `snippet_only` |
| Consensus revenue | **$2.2907bn** | [19] — `snippet_only` |
| Consensus revenue in RMB | **≈RMB15.4bn at spot USDCNY 6.7127** → **+3.9% YoY** | My computation; FX from Yahoo `CNY=X`, 2026-09-15 [11]. Other write-ups quote "approximately RMB16bn" using a weaker rate [9] — see caveat |
| 30-day EPS revision | **−8.07%** (one source); **−4.08%** (Zacks basis) | [19] — `snippet_only`, the two disagree |
| 60/90-day revisions | **unavailable** as discrete figures | — |
| FY2026 estimate drift | Revenue **CN¥70.9bn → CN¥68.0bn**; EPS **CN¥25.28 → CN¥20.50** (−18.9%) | Simply Wall St [22] — `snippet_only` |
| Company guidance (given 2026-06-24) | Net revenue **+3% to +8% YoY** | [7][8] |
| Guidance in RMB terms | **RMB15.24bn – RMB15.98bn** vs RMB14.8bn in Q2 2025 | [9][17] |
| Whisper number | **unavailable** — no credibly published whisper found | — |
| Q2 2025 comparison base | Revenue RMB14.8bn (+16%); accommodation RMB6.2bn (+21%); transport RMB5.4bn (+11%); packaged tours RMB1.1bn (+5%); corporate RMB692m (+9%); adj. EBITDA RMB4.9bn (**33% margin**) | [17] |
| Q1 2026 actual | Revenue $2.35bn vs $2.30bn est (**beat**); EPS $0.83 vs $0.85 est (**miss**) | [23][24] |
| Analyst count | 29–31 | [25][26] — `snippet_only` |
| Rating distribution | 28 of 30 Buy-or-better; 0 Sell | [25][27] — `snippet_only` |
| Average PT | **$59.89–$77.05** depending on vendor; S&P Global panel $60.29 | [14][25] — `snippet_only`, wide dispersion |

**What the company has to deliver just to hold the stock flat — my inference, not a sourced figure.** Three conditions, and all three have to hold:

1. **Revenue ≥ RMB15.5bn (+4.7% YoY)**, i.e. at or above the midpoint of its own guide. Consensus at spot FX sits near +3.9%, so the bar on the *top line* is low — which is exactly why the top line will not move the stock.
2. **A Q3 revenue guide no worse than mid-single-digit growth.** Nobody has this number; it is the first datum in the release the market will read.
3. **An accommodation-margin statement that caps the take-rate damage.** The Street's FY2026 EPS has already been cut ~19% [22], but that cut is mostly the fine plus softer revenue, not a structural take-rate reset. If management sizes the reset at more than a couple of points of accommodation revenue, numbers go down again from here.

**The GAAP/non-GAAP trap.** SAMR's decision is dated 2026-07-25, *after* the 30 June balance-sheet date [3]. Under ASC 450 the underlying conduct existed before 30 June and the amount became estimable before issuance, so the RMB5,301m is very likely a recognised (Type 1) subsequent event accrued in the Q2 GAAP accounts. RMB5.3bn against ~660m diluted ADS is roughly **RMB8.0 / ~US$1.19 per ADS** — larger than the entire consensus quarter. Trip.com's stated non-GAAP bridge excludes only share-based compensation, fair-value changes on equity securities and exchangeable notes, and tax effects [28] — *a regulatory fine is not on that list*. So there are two live scenarios and the Street is not obviously aligned on either: (a) the fine sits in GAAP only and management adds a new non-GAAP add-back, in which case $0.87 is comparable and the headline GAAP number is ugly but ignorable; or (b) the fine flows through non-GAAP too, in which case the "miss" will be enormous and meaningless. One preview asserts flatly that the penalty "impacts Q2 results" [20][29]; another says the treatment is genuinely unclear and the company "may recognize a provision in Q2... or explain different timing" [9]. **I could not resolve this from any primary source and flag it as the single largest mechanical risk of misinterpretation in the first minutes after the tape.**

---

## 3. The one metric that matters

**Accommodation-segment take rate / margin under the post-remediation hotel model, and the Q3 revenue guide that embeds it.**

Not EPS. Not revenue. Here is why, and how I know:

- The remedies are *structural*, not a fine. Trip.com must "redesign core parts of its relationship with hotels, including merchant classifications, commission arrangements, traffic allocation and pricing tools"; stop requiring exclusivity; remove the lowest-price-across-all-platforms requirement; discontinue certain pricing tools; stop changing room rates without hotel consent; and it is "ceasing its Tier 1 delegated distribution program" [5][6]. Tier-1 delegated distribution is the high-margin arrangement. mLex's own framing: "If the new model cuts commission rates or forces greater spending on hotel subsidies and marketing, margins in the accommodation business could be squeezed even if volumes keep growing" [5].
- Accommodation is the profit engine: RMB6.5bn of RMB16.2bn revenue in Q1 2026 (+17%) [7], RMB6.2bn of RMB14.8bn in Q2 2025 (+21%) [17].
- The sell-side has explicitly identified this as the swing item. HSBC's Parash Jain downgraded to Hold with a **$48** target on 2026-09-03 citing "antitrust remedies forcing Trip.com to abandon high-margin exclusive distribution and pressuring hotel segment margins" [30][31]. The stock fell 5.11% that day on 6.88m shares — the largest single-day volume of the last month [10][30]. BofA cut its target on antitrust costs [32]; Barclays cut to $60 from $75 [27]; Citi to $62 from $64; JPMorgan to $75 from $80 [22][33].
- The Seeking Alpha preview frames it identically: "Regulatory changes require TCOM to remove exclusivity with hotels and automatic price adjustments, raising concerns over take rate and market share" [29].
- And the margin is already moving the wrong way *before* the remedies bite: adjusted EBITDA margin was **30% in Q1 2026 against 33% in Q2 2025** [7][9][17], with marketing expense reported up 24% [34] — `snippet_only`.

**What the market expects for it.** No published consensus for accommodation take rate exists — I could not source one and that is a real gap. What I can source is the shape of expectations: FY2026 Street EPS has been cut from CN¥25.28 to CN¥20.50 [22] and revenue from CN¥70.9bn to CN¥68.0bn, and at least one analyst is willing to pay ~9× FY2027 earnings for the recovery [29]. My inference: **the Street is modelling a temporary dent, not a permanent reset.** That is the asymmetry. The number that decides this print is whatever management says — or refuses to say — about accommodation margin in H2 2026 and 2027.

---

## 4. Fundamentals — what changed, what is at stake

**Q1 2026 (reported 2026-06-24) — the last full data point** [7]:

| Line | Q1 2026 | YoY |
| --- | --- | --- |
| Net revenue | RMB16.2bn (US$2.4bn) | +17% |
| Accommodation | RMB6.5bn (US$944m) | +17% |
| Transportation | RMB6.1bn (US$877m) | +12% |
| Packaged tours | RMB1.1bn (US$164m) | +19% |
| Corporate travel | RMB690m (US$100m) | +20% |
| Other | RMB1.8bn (US$265m) | — |
| Adjusted EBITDA | RMB4.8bn (US$701m), **30% margin** | vs RMB4.2bn |
| GAAP net income | **RMB2.5bn (US$367m)** | vs RMB4.3bn |
| Non-GAAP net income | RMB3.9bn (US$568m) | vs RMB4.2bn |
| GAAP diluted EPS/ADS | RMB3.67 (US$0.53) | — |
| Non-GAAP diluted EPS/ADS | RMB5.73 (US$0.83) | — |
| Cash + investments | **RMB104.0bn (US$15.1bn)** | — |

**Volume vs price.** The demand signal is not the problem. Q1 international OTA gross bookings **+65% YoY**, inbound bookings **+90% YoY**, core OTA gross bookings ~RMB300bn [7][35]. Management set a target of serving **200m inbound travellers over five years** [35]. Into Q2, international air ticketing volumes were reported up 40–50% YoY and overseas packaged tours doubled to >10% of segment revenue [36] — `snippet_only`. The problem is price and mix: management attributed the Q2 deceleration to "higher airfares," "macro headwinds including energy pricing and geopolitical volatility," and "operational adjustments for regulatory compliance" [7][8].

**The China price environment is deflationary and that is the read-through into the guide.** Goldman Sachs put industry RevPAR at **−6% YoY through late July** after **−1% in June**, driven by a 3pp occupancy decline and 1% lower ADR [30][37] — `snippet_only`. CNBC ran the whole theme as "tourism price wars threaten to dim a rare bright spot in China's consumer spending" [38]. Average domestic flight booking prices in the first week of July were reported **~20% lower YoY** [39] — `snippet_only`. June sits inside Q2; July and August sit inside the Q3 guide.

**Balance sheet and capital return.** RMB104.0bn (US$15.1bn) of cash and investments at 31 March 2026 [7]; approximately **US$6.7bn of net cash, ~22% of market cap** [40] — `snippet_only`. A **US$5bn** repurchase authorisation is running; ~**20,285,355 shares for ~US$916m** had been completed across two tranches as at late April 2026 [40][41] — `snippet_only`. At a 52-week low with $6.7bn of net cash and $4bn of authorisation left, the company has unusual latitude to lean into the print — and buyback pace is a live, checkable item in the release.

**Why trailing P/E is meaningless here.** Q3 2025 diluted EPS/ADS was **RMB28.61** [16] — roughly RMB18bn of net income in one quarter, driven by fair-value moves on equity investments (Trip.com holds a large MakeMyTrip position) rather than operations. Trip.com's non-GAAP bridge exists precisely to strip these [28]. GAAP net income has swung RMB4.3bn → RMB2.5bn YoY in Q1 2026 on the same mechanism [7]. Use EV/non-GAAP earnings, not the 5.93× headline [14].

**Customer concentration:** not applicable in a meaningful sense — this is a consumer marketplace. **Supplier concentration is the live issue**: the hotel supply base is precisely the counterparty SAMR found Trip.com was coercing, and the remediation hands those suppliers pricing and multi-homing freedom back.

---

## 5. Positioning & options

| Item | Value | As of | Source |
| --- | --- | --- | --- |
| Short interest | **12,168,964 sh**, +1,292,154 (+11.9%) | 2026-08-31 settlement (FINRA) | [42] — `snippet_only` |
| Short interest % shares out | **≈1.93%** (12.17m / 629.71m) | my computation | [42][14] |
| Days to cover (FINRA basis) | **6.10** | 2026-08-31 | [42] — `snippet_only` |
| Days to cover (20d ADV 3.15m) | **≈3.9** | 2026-09-14 | computed from [10][42] |
| Modelled next SI | 11.24m (−7.6%), range 9.04–12.97m; FINRA release due 2026-09-24 | 2026-09-15 settle | [42] — model, not fact |
| Borrow fee | **unavailable** | — | — |
| Front-week ATM IV | ~83% | 2026-09-14 close | derived from [15] |
| 1m / 3m ATM IV | 38.6% / 38.7% | 2026-09-14 close | derived from [15] |
| Skew (18 Sep) | 25-delta-ish proxy: **P$35 IV 89.3% vs C$45 IV 95.3%** → mild *call* skew | 2026-09-14 close | derived from [15] |
| P/C volume, 18 Sep expiry | **3.62** all strikes; **1.32** excluding deep-ITM puts (K≥50) | 2026-09-14 | computed from [15] |
| Published P/C snippet | 0.22 (42 puts / 190 calls) | undated | [43] — `snippet_only`, contradicts the chain; low confidence |
| 5d / 10d / 20d / 60d run-up | **−4.75% / −13.83% / −13.12% / −16.37%** | 2026-09-14 | computed from [10] |
| KWEB same windows | −5.07% / −6.04% / −8.44% / −2.56% | 2026-09-14 | computed from [11] |
| HK line 9961.HK 20d | −11.14% | 2026-09-15 | computed from [11] |
| Institutional ownership | 35.41%; 270 buyers / 206 sellers LTM; inflows $5.28bn vs outflows $4.08bn | LTM | [44] — `snippet_only` |

**Reading it.** This is not a crowded short. 1.93% of shares out is nothing, and even the +11.9% build into the print leaves the position small. The crowding is on the **other** side: 28 of 30 analysts at Buy-or-better with a consensus target between $60 and $77 against a $39 tape [25][27] — the sell-side is 50–95% above spot and has been cutting in a straight line all year (JPM $80→$75, Barclays $75→$60, Citi $64→$62, HSBC to Hold at $48, BofA down on antitrust costs) [22][27][31][32][33]. The marginal seller here is a long-only holder capitulating, not a short covering.

The drawdown into the print is the single strongest positioning fact: **−13.1% over 20 sessions against KWEB −8.4%**, i.e. ~4.7pp of idiosyncratic decline, into a 52-week low ($38.04 intraday; $38.70 closing low on 2026-09-10) [10][11][14]. Two identifiable catalysts inside that window: the HSBC downgrade on 2026-09-03 (−5.11%, 6.88m shares — the month's largest volume day) and a continued grind lower through 2026-09-08/09/10 on rising volume (4.6m, 5.3m, 5.1m) with no company news I could source [10][30][31].

Front-week option volume is thin in absolute terms (~11,500 contracts across the three nearest expiries [15]) and open-interest data from this feed is not usable, so I will not claim unusual options activity either way. The **P/C figure is genuinely ambiguous**: 3.62 all-strikes looks bearish, but 4,793 of the 7,572 put contracts sit in deep-ITM $50 and $55 strikes, which are as likely to be synthetic-short or roll machinery as directional bets. Stripping them gives 1.32 — mildly put-heavy, unremarkable. The IV surface carries mild *call* skew at the wings, which is the one option-market datum leaning positive.

---

## 6. Sentiment & alt-data

**Analyst actions and PT drift (all downward, all 2026):**

| Firm | Action | Date | Source |
| --- | --- | --- | --- |
| HSBC (Parash Jain) | **Buy → Hold**, PT $48 | 2026-09-03 | [30][31] |
| BofA | PT lowered on antitrust costs | 2026 (post-fine) | [32] |
| Barclays | PT $75 → $60, keeps Overweight | 2026 | [27] |
| Citi | PT $64 → $62, keeps Buy | 2026 | [22] |
| JPMorgan | PT $80 → $75 | 2026 | [33] |
| Benchmark | PT trimmed to $72 | 2026 | [45] |
| CFRA | PT raised, maintains Hold | 2026 | [46] |
| Simply Wall St fair value | $77.09 → $61.65 → $59.89 | through Sep 2026 | [22][47] |

The direction is unambiguous and the *level* is the tell: even after all the cuts, the consensus target sits 53–97% above spot [14][25]. That is a consensus that has repriced its multiples but not yet its thesis.

**Retail / social.** Weaker sourcing here and I flag it. Stocktwits sentiment was reported as having "declined to 'neutral' from 'bullish'" with message volume "extremely high" from "high" — but that snapshot is from **June 2026**, not the last few sessions, so it does not meet the recency bar and I am recording it as colour only [48] — `snippet_only`. A more recent Stocktwits/TradingView item is headlined "TCOM Stock On Track To Hit Lowest Levels Since August 2024" [48]. I could not source a dated 7/14/30-day retail sentiment trend and record that as a gap. Also on the record: a **securities class action** with a 2024-04-30 to 2026-01-13 class period and a 2026-05-11 lead-plaintiff deadline, actively promoted through repeated press releases from March to May 2026 [21][49] — that generates a persistent negative retail news stream independent of fundamentals.

**Alt-data proxies I could source (all company- or Google-originated, so treat as directionally favourable but not independent):**

- Golden Week (1–7 Oct 2026): searches for Mid-Autumn Festival and National Day travel **+116% by 24 August**; bookings made >30 days in advance **+20% YoY**; international flight bookings for 25 Sep–7 Oct **>1.28m, +11% YoY** [50] — `snippet_only`.
- China summer aviation: **151m air passengers** over the summer season [51] — `snippet_only`.
- Google Trends via the Trip.com/Google 2026 trends report: "help planning my trip" searches **+190% YoY**; culinary-related bookings on Trip.com **+43%** [52] — marketing material, weak evidence.
- Against that, price: China hotel prices at multi-year lows, August weekend medians US$28 (Kashgar) to US$88 (Shanghai) [37][38].

**App ranks and web traffic: unavailable.** I could not source a dated app-download or web-traffic series for Ctrip/Trip.com and record it as a gap — for an OTA this is a meaningful hole, because it is the one place a volume-versus-take-rate divergence would show up independently.

---

## 7. Forensics

**This is the richest section on the name and it leans negative.**

**1. The Executive Chairman's family vehicle monetised 1,000,000 ADS near the highs, and disclosed it eight months later.** Form 4 filed 2026-04-28 by **Liang Jianzhang (James Liang), director**: on **2025-09-03**, *Smart Charm Limited* — a BVI company "wholly owned and controlled by the Reporting Person's spouse" — entered a **prepaid variable forward contract** with an unaffiliated third-party buyer, obliging it to deliver up to 1,000,000 ADSs across three settlement dates in September 2028, "in exchange for assuming this obligation, Smart Charm Limited received a cash payment." 1,000,000 ADSs were pledged as security; voting rights retained [53]. TCOM closed at **$71.23 on 2025-09-03** [10]. The stock is now $39.08 — **−45%** from the transaction date. Three Form 144s were filed 2025-09-02, 09-03 and 09-05, consistent with the same programme [12].
  - This is a **discretionary** transaction, not a 10b5-1 plan — no Rule 10b5-1 representation appears in the filing [53].
  - It is a downside hedge dressed as a financing: the floor/cap structure caps upside and, critically, **protects the holder below the Floor Level**. It was struck roughly four months before the SAMR probe became public.
  - Floor and Cap levels are **not disclosed** in the filing [53].
  - I am not alleging anything. I am recording that the most senior insider's household monetised and hedged a seven-figure ADS block near the all-time high, and that the market learned about it in late April 2026.

**2. Section 16 filings appeared where there had previously been none.** Trip.com filed **ten Form 3s on 2026-03-18** (Sun Jie CEO, Xiong Xing COO, Wang Xiaofan, Liang Jianzhang, Li Gabriel and others) and **one Form 4 on 2026-04-28** [12][53][54]. Across the company's entire EDGAR history the counters are: 263 6-Ks, 23 20-Fs, **10 Form 3s and 1 Form 4** [12]. A foreign private issuer is exempt from Section 16 under Rule 3a12-3(b); a simultaneous batch of initial-ownership statements is what happens when that exemption stops being relied upon. **The company nonetheless filed a 20-F for FY2025 on 2026-04-28** [55], so it is still using the FPI reporting regime. I could not reconcile these two facts from any primary source and flag it as an open question — but the practical consequence for the panel is concrete: **insider-transaction visibility for TCOM is near-zero historically and only began in March 2026**, so "no recent Form 4 activity" here means "no disclosure regime," not "no selling."

**3. Two founding-quartet co-founders left the board weeks after the probe.** Min Fan and Qi Ji — both 1999 founding team — stepped down from their board positions **effective 2026-02-25**, announced with the Q4 2025 results on 2026-02-26, "with no explanation" per the class-action complaints [21][56]. May Yihong Wu and Iris Yang Xiao were appointed independent directors at the same time [56]. James Liang remains Executive Chairman and Neil Shen remains an independent director [56]. The departures landed six weeks after SAMR opened the probe.

**4. The reporting calendar has slipped, twice, and only since the probe.**

| Quarter | Reported | Prior-year analogue | Slip |
| --- | --- | --- | --- |
| Q4 2025 | 2026-02-25 [18] | 2025-02-24 [12] | +1 day |
| Q1 2026 | **2026-06-24** [13] | 2025-05-19 [12] | **+36 days** |
| Q2 2026 | **2026-09-15** [1] | 2025-08-27 [17] | **+19 days** |

Q4 2025 (the quarter ending before the probe became public) was on time. Both quarters since are materially late. The Q2 date was announced on **2026-09-02 — thirteen days' notice**, against 12 days for Q3 2025 (announced 2025-11-05 for 2025-11-17 [16]), 13 days for Q1 2026 (2026-06-11 for 2026-06-24 [13]) and 16 days for Q4 2025 (2026-02-09 for 2026-02-25 [12]). So the *notice* is normal; the *date itself* is late. A reasonable benign explanation is the accounting and legal work around a RMB5.3bn subsequent-event provision and the remediation programme. It is still a slip, twice, and it is the kind of thing that precedes messy disclosure.

**5. 8-K/6-K cadence.** Trip.com files 6-Ks, not 8-Ks. The 2026 run is sparse and every item is explicable: 2026-01-15 (probe disclosure), 2026-02-09 (Q4 date), 2026-02-26 (Q4 results + board changes), 2026-04-28 (20-F), 2026-05-27, 2026-06-11 (Q1 date), 2026-06-25 (Q1 results), 2026-06-30 (AGM results, signed by CFO Cindy Xiaofan Wang), 2026-07-27 (**acceptance of the SAMR penalty**), 2026-09-02 (Q2 date) [12][57]. **No pre-announcement, no profit warning, no 6-K between 2026-07-27 and 2026-09-02** — a six-week silence spanning the whole peak travel season. That silence is itself a data point: management had a window to pre-frame a bad quarter and did not use it.

**6. Auditor and controls: clean.** PricewaterhouseCoopers Zhong Tian LLP issued a report dated 2026-04-28 covering both the FY2025 financial statements and the effectiveness of internal control over financial reporting, included in the FY2025 Form 20-F filed 2026-04-28 [55][58]. **No restatement, no auditor change, no material weakness found.**

**7. Filing-language / tone shift.** The 2026-07-27 release is notable for its register: the company "**sincerely accepts** the Decision," will adopt "rectification measures in accordance with applicable laws and regulations," and will "strengthen its long-term governance mechanisms to support sustainable travel industry development" [3]. That is submission language, not contestation language — consistent with Benzinga's read that the company was "hit with fines... but spared a major overhaul" [59]. Trip.com **did not appeal**.

---

## 8. Macro & peer read-through

**Regime.** China internet is the factor here, and it is weak but not disorderly: KWEB −8.44% over 20 sessions and −6.04% over 10 [11]. The Hang Seng Tech index has chopped around 4,500 in early September (4,533 on 4 Sep, 4,502 on 8 Sep) [60] — `snippet_only`. TCOM's −13.1% over 20 days is therefore **~4.7pp of idiosyncratic underperformance** [10][11], and the HK line (9961.HK, −11.1% over 20 days [11]) confirms it is the company and not the ADR wrapper.

**FX.** USDCNY at **6.7127** on 2026-09-15, −0.40% over 20 days and −0.91% over 60 days (RMB strengthening) [11]. Against an average near 7.18 in Q2 2025, a materially stronger RMB is a **tailwind to USD-translated revenue and EPS** of several points — which is exactly why the guide (stated in RMB growth) and the US-dollar consensus can look inconsistent. It also means a USD "beat" on revenue can coexist with an RMB result at the low end of guidance. **The panel should not read a dollar-revenue beat as an operational beat.**

**Rates/commodities.** Management named **energy pricing** and **higher airfares** as drivers of the Q2 deceleration [7][8]; Barclays named "rising fuel costs" in its PT cut [27]. Jet fuel is therefore a genuine, if second-order, sensitivity for transportation ticketing volumes.

**Peers who already reported:**

- **Tongcheng Travel (0780.HK)** — Q2 2026: total revenue **+6.8% YoY to RMB5.0bn**, adjusted net profit **+9.8% to RMB851m**, **accommodation reservation revenue +12.8%**, international accommodation room nights **+50%**, but **monthly paying users −5.8% YoY to 43.7m** [61][62]. Read-through: the *accommodation* line is still compounding double-digits at the number-two player; the *user* line is shrinking. Tongcheng also said it had "not observed any material impact on hotel operations, user traffic, or financial performance from adjustments to hotel traffic distribution systems by industry peers" [62] — i.e. Trip.com's remediation had not yet visibly moved share as of Tongcheng's Q2. That is mildly **supportive** for TCOM volumes and mildly negative for the "share-loss is already happening" bear case.
- **Meituan** — in-store, hotel and travel maintained steady growth in domestic room nights and GTV, with order volume **+60% YoY** [63] — `snippet_only`, and I could not pin the exact reporting period, so treat with care. If directionally right, it is the clearest evidence that the competitive set is taking volume at lower price points, which is the mechanism by which TCOM's take rate gets reset regardless of what SAMR ordered.
- **Industry supply-side**: Goldman's China hotel RevPAR −6% in July, −1% in June, occupancy −3pp, ADR −1% [30][37]; CNBC on tourism price wars [38]. This is the read-through that matters for the **Q3 guide**, not for Q2.

**Calendar context around the event:** China's August activity data prints the same day as the earnings, and a Xi Jinping US visit is scheduled for 2026-09-24 [20] — `snippet_only`. Both are exogenous sources of China-beta noise in the reaction window.

---

## 9. Bull case / bear case / base case

**Bull.** The stock has already taken the punishment: −50.5% from the 2026-01-12 high of $78.96, −16.4% in 60 days, −13.1% in 20 days, sitting at a 52-week low [10][14]. The regulatory overhang that caused the de-rating is *resolved* — SAMR closed the case on 2026-07-25, the company accepted without appeal, and the amount is known and payable out of RMB104.0bn of cash and investments [3][7]. The demand engine is undamaged: international OTA gross bookings +65%, inbound +90%, corporate +20% [7], with Golden Week searches +116% and >30-day advance bookings +20% YoY [50]. Tongcheng — the closest comparable, already reported — grew accommodation revenue 12.8% and explicitly said it had seen no disruption from peers' traffic-distribution changes [61][62]. Valuation is ~9× FY2027 earnings on one analyst's math with US$6.7bn of net cash at ~22% of market cap and ~$4bn of a $5bn buyback still unspent [29][40][41]. The option market is asking 7.0% for an event whose last six realisations averaged 8.20% [15]. And the closest analogue in the record is Q2 2025: the stock went into that print beaten down and printed **+14.92%** [10][17]. If the fine is quarantined as a GAAP-only item and the Q3 guide is merely mediocre rather than bad, a short, violent mean-reversion is entirely available from a 52-week low with a 1.9% short base and a sell-side consensus 50%+ above spot.

**Bear.** The remedies are permanent and this is the quarter they get priced. Trip.com must abandon hotel exclusivity, the lowest-price-across-the-internet requirement, its automatic price-adjustment tools, and the **Tier-1 delegated distribution programme** — and redesign merchant classification, commission arrangements and traffic allocation [5][6]. mLex's own conclusion is that accommodation margins get squeezed "even if volumes keep growing" [5]; HSBC downgraded on exactly this [30][31]. The margin is already going the wrong way before the remedies bite: adjusted EBITDA margin 30% in Q1 2026 versus 33% in Q2 2025, with marketing spend +24% [7][17][34]. The industry price environment is deflationary — RevPAR −6% in July, ADR −1%, domestic airfares −20% in early July [30][37][39] — which means the Q3 guide, the first thing the market reads, is very likely soft; HSBC explicitly flagged a "softer-than-expected travel season" [30]. Meituan's travel order volume +60% shows the volume is going somewhere cheaper [63]. FY2026 Street EPS has already been cut 18.9% [22] and is probably still too high. There is a live securities class action over exactly these disclosures [21][49], two founding co-founders left the board weeks after the probe [56], the reporting calendar has slipped 36 and 19 days in the two quarters since [1][12][13], and the Executive Chairman's family vehicle hedged 1,000,000 ADS near the highs and told the market eight months later [53]. The last two prints were **−2.59%** and **−12.55%** [10]. A stock making 52-week lows into a print whose central unknown is one-directionally bad is not obviously a bargain.

**Base case (mine).** Roughly balanced, with a modest positive tilt that rests on positioning rather than fundamentals. My read: Q2 revenue lands **inside** the +3–8% guide, probably at or slightly above the RMB15.5bn midpoint, helped by a ~6% FX translation tailwind that flatters the dollar line [11]. The RMB5.3bn penalty most likely appears as a Q2 GAAP charge with a non-GAAP add-back, producing an ugly headline that is fully known and largely ignorable — but a real risk of a violent first-minute misread. The Q3 guide is the swing factor and the evidence says it will be underwhelming; the question is whether "underwhelming" is already in a stock 50% off its high with the sell-side 50%+ above spot. I think most of it is, which is why I do not lean hard down despite bad fundamental news flow. The event itself should be large: implied 7.0% against a six-quarter realised mean of 8.20%, and TCOM's gap and close have agreed in direction on 8 of 8 prints — this name does not fade its reaction. **Preliminary direction score +12, prob_up 54, conviction Low-Med.** I am explicitly flagging that this is close to a coin flip with a fat two-sided tail, and that the *magnitude* read is much more confident than the *direction* read.

---

## 10. What would flip the consensus view

The single most credible reversal, stated concretely: **management quantifies the accommodation take-rate reset on the call and it is smaller than feared — and pairs it with an accelerated buyback.**

Specifically: if on the 20:00 ET call management says that ending Tier-1 delegated distribution and the exclusivity/lowest-price requirements costs accommodation revenue less than ~2–3 points of take rate, guides Q3 net revenue to high-single-digit growth or better, and confirms it is stepping up repurchases against the remaining ~$4bn of the $5bn authorisation at a 52-week low [40][41] — then the entire bear thesis reduces to a one-off RMB5.3bn cash payment against RMB104.0bn of cash [7], and the sell-side's $60+ targets stop looking absurd. In that world the 1.9%-short, 28-of-30-Buy, 52-week-low setup unwinds violently upward and the +14.92% Q2 2025 analogue is the template.

The mirror image is equally concrete and, on the present evidence, at least as likely: **a Q3 guide at or below low-single-digit growth combined with an explicit accommodation-margin reduction**. HSBC's $48 becomes the new consensus ceiling rather than the floor, the FY2027 "9× earnings" that anchors the bull case turns out to be 9× a number that has not yet been cut, and a stock at a 52-week low with no short base to squeeze has nothing underneath it.

Lower-probability but high-impact flips: **a further regulatory action** (SAMR's remedies are being implemented under supervision; a finding of inadequate rectification would be new information), or **an unexpected non-GAAP treatment of the fine** that makes the headline EPS number unrecognisable versus the $0.87 consensus in either direction.

---

## 11. Coverage gaps

Every figure I could not source, and why it matters:

1. **Vendor-published implied move / IV rank / IV percentile.** Market Chameleon returned Access Denied to `WebFetch`, and no press-published implied move for this event exists. My 7.0% is derived from Yahoo option prices, not cited. **Matters:** the panel's whole calibration of "is this move big" rests on this anchor, and mine carries model risk from a $5-wide strike grid and zeroed bid/ask.
2. **Open interest and reliable put/call.** The Yahoo feed returned 728 call / 5 put open interest, which is not credible. The one published P/C (0.22) is undated and contradicts my chain computation (3.62 / 1.32). **Matters:** I cannot say whether options positioning is directional.
3. **Borrow fee / utilisation.** No source. **Matters:** less than usual — short interest is only 1.9% of shares out, so borrow is almost certainly cheap and there is no squeeze fuel.
4. **Whisper number.** None credibly published. **Matters:** with a possible fine-in-EPS ambiguity, the buyside bar may differ materially from $0.87 and I cannot measure it.
5. **60- and 90-day estimate revisions as discrete figures.** Only the 30-day number is sourceable, and two vendors disagree on it (−8.07% vs −4.08%). **Matters:** revision momentum is one of the better pre-earnings predictors and I have it only coarsely.
6. **Consensus for the one metric — accommodation take rate or segment margin.** No published Street number. **Matters:** this is the metric I claim the print trades on, and I cannot state the expectation quantitatively, only its shape.
7. **Accounting treatment of the RMB5.3bn penalty — which quarter, GAAP vs non-GAAP.** Not resolvable from any primary source; two previews disagree [9][20]. **Matters:** most likely single cause of a first-minute misreaction.
8. **Dated retail/social sentiment with a 7/14/30-day trend.** The only Stocktwits datum I found is from June 2026 and fails the recency bar. **Matters:** leaves §6 thin.
9. **App download ranks and web-traffic series for Ctrip / Trip.com.** Unavailable. **Matters:** the only independent way to separate volume from take rate ahead of the print.
10. **Meituan's travel disclosure period.** The +60% order-volume figure could not be pinned to a confirmed quarter. **Matters:** it is a load-bearing competitive datum in the bear case and I have downgraded it accordingly.
11. **Why ten Form 3s appeared in March 2026 while the company still files 20-Fs.** Could not reconcile. **Matters:** determines whether future insider selling will be visible at all.
12. **Floor and Cap levels on the Liang prepaid variable forward.** Not disclosed in the Form 4 [53]. **Matters:** determines how much downside protection the chairman's household actually bought.
13. **Q2 2025 non-GAAP EPS per ADS**, needed for a clean YoY comparison against the $0.873 consensus. Only GAAP RMB7.34 was sourceable.
14. **Unreachable domains** (recorded for the run log): `marketchameleon.com` (Access Denied), `benzinga.com` (403), `wsj.com` (blocked), `investors.trip.com` (503). Yahoo's chart and options APIs and `data.sec.gov` were reachable via Bash and carried the heavy lifting.

---

## 12. Sources

1. https://www.sec.gov/Archives/edgar/data/0001269238/000119312526379443/d431415dex991.htm — 6-K exhibit filed 2026-09-02: Q2/H1 2026 results on 2026-09-15 U.S. time after the close; call 20:00 ET; audit committee meets 2026-09-14. **Event confirmation.**
2. https://skift.com/2026/01/14/trip-com-faces-antitrust-investigation-as-china-tightens-platform-rules/ — SAMR probe opened 2026-01-14.
3. https://www.sec.gov/Archives/edgar/data/0001269238/000119312526316761/d256213d6k.htm — 6-K, 2026-07-27: SAMR decision 2026-07-25, penalty breakdown (RMB122m refund / RMB1,658m confiscation / RMB3,521m fine = RMB5,301m, US$781.3m), Articles 22(4)/(5), "sincerely accepts," rectification and governance commitments.
4. https://www.scmp.com/tech/policy/article/3361818/china-hits-tripcom-us765-million-antitrust-penalty-after-six-month-investigation — US$765m headline, six-month probe, traffic-allocation / exclusivity / lowest-price findings.
5. https://www.mlex.com/mlex/articles/2505888/trip-com-announces-corrective-measures-after-china-s-765m-antitrust-sanction — corrective measures: merchant classification, commission arrangements, traffic allocation, pricing tools; margin-squeeze framing.
6. https://finance.yahoo.com/economy/policy/articles/trip-com-accepts-china-antitrust-penalty-180209107.html — ceasing Tier-1 delegated distribution, transition to multi-tier partnership framework; no exclusivity, no lowest-price requirement, no unilateral rate changes.
7. https://www.prnewswire.com/news-releases/tripcom-group-limited-reports-unaudited-first-quarter-of-2026-financial-results-302809167.html — Q1 2026 results: revenue, segments, adj. EBITDA and margin, GAAP/non-GAAP net income and EPS, cash RMB104.0bn, Q2 guidance +3–8%.
8. https://www.stocktitan.net/news/TCOM/trip-com-group-limited-reports-unaudited-first-quarter-of-2026-dx2ntnhg2l6b.html — Q1 revenue +17%, net income fell to RMB2.5bn, Q2 guide slowdown, SAMR probe disclosure.
9. https://ts2.tech/en/trip-com-earnings-preview-a-3-8-growth-test-meets-a-rmb5-3-billion-antitrust-order/ — guidance arithmetic RMB15.24–15.98bn; penalty accounting treatment "unclear," issued after Q2 closed; Q1 adj. EBITDA margin 30% vs 33% in Q2 2025.
10. https://query1.finance.yahoo.com/v8/finance/chart/TCOM?range=3y&interval=1d — TCOM daily OHLCV, `regularMarketTime` 2026-09-14T20:00Z. **Source for spot, all eight historical earnings moves, run-ups, realised vol, ADV, and the 2025-09-03 and 2026-01-14 prices.**
11. https://query1.finance.yahoo.com/v8/finance/chart/KWEB?range=1y&interval=1d (also `CNY=X` and `9961.HK`) — KWEB relative performance, USDCNY 6.7127, HK line 9961.HK.
12. https://data.sec.gov/submissions/CIK0001269238.json — complete EDGAR filing history: form-type counts, 6-K cadence, ten Form 3s on 2026-03-18, one Form 4 on 2026-04-28, Form 144s 2025-09-02/03/05, prior-year report dates.
13. https://www.stocktitan.net/news/TCOM/trip-com-group-limited-to-report-first-quarter-of-2026-financial-s8r0pzgz6toq.html — Q1 2026 results date 2026-06-24 announced 2026-06-11.
14. https://stockanalysis.com/stocks/tcom/ — spot $39.08, prev close $39.02, market cap $24.61bn, 629.71m shares, P/E 5.93, 52-week range $38.04–$78.99, next earnings 2026-09-15, consensus PT $59.89.
15. https://query1.finance.yahoo.com/v7/finance/options/TCOM (expiries 2026-09-18, 2026-10-16, 2026-12-18) — option chain used to derive the implied move, ATM IV term structure, wing skew and put/call volume.
16. https://investors.trip.com/news-releases/news-release-details/tripcom-group-limited-report-third-quarter-2025-financial — Q3 2025 reported 2025-11-17 amc, announced 2025-11-05.
17. https://www.prnewswire.com/news-releases/tripcom-group-limited-reports-unaudited-second-quarter-and-first-half-of-2025-financial-results-302539677.html — Q2 2025 base: revenue RMB14.8bn (+16%), segment detail, adj. EBITDA RMB4.9bn / 33% margin; reported 2025-08-27.
18. https://ctripcominternationalltd.gcs-web.com/news-releases/news-release-details/tripcom-group-limited-report-fourth-quarter-and-full-year-2025/ — Q4 2025 reported 2026-02-25 amc.
19. https://finance.yahoo.com/markets/stocks/articles/earnings-preview-trip-com-tcom-140005918.html — Zacks: consensus EPS $0.8730, revenue $2.2907bn, YoY decline expected, 30-day revision −8.07% / −4.08%.
20. https://www.optionstradingreport.com/2026/09/trip-com-faces-a-765m-fine-tomorrow-growth-says-buy-anyway/ — Street EPS range $0.87–$0.98, revenue ~$2.29bn, penalty "impacts Q2," ~9× forward earnings, China August data same day, Xi US visit 2026-09-24.
21. https://www.prnewswire.com/news-releases/tcom-shareholder-update-tripcom-tcom-facing-securities-class-action-after-ai-pricing-controversy-and-anti-monopoly-probe-sends-shares-tumbling----hagens-berman-302761306.html — class period 2024-04-30 to 2026-01-13, −17.05% on 2026-01-14, AI price-adjustment tool allegations, co-founder resignations "with no explanation."
22. https://simplywall.st/stocks/us/consumer-services/nasdaq-tcom/tripcom-group/future — FY2026 revenue CN¥70.9bn → CN¥68.0bn, EPS CN¥25.28 → CN¥20.50; fair value $77.09 → $61.65; Citi $64 → $62.
23. https://finance.yahoo.com/markets/stocks/articles/trip-com-tcom-lags-q1-231502828.html — Q1 2026 EPS $0.83 vs $0.85 Zacks consensus.
24. https://www.marketbeat.com/instant-alerts/upcoming-tripcom-group-tcom-expected-to-post-earnings-on-thursday-2026-09-10/ — Q1 2026 revenue $2.35bn vs $2.30bn expected.
25. https://www.investing.com/equities/ctrip.com-international-consensus-estimates — 29 analysts, 28 Buy / 1 Hold / 0 Sell, average PT $77.05 (high $92.48, low $61.15).
26. https://www.chartmill.com/stock/quote/TCOM/analyst-ratings — 31 analysts, average PT $66.97.
27. https://stocktwits.com/news-articles/markets/equity/tocm-stock-on-track-to-hit-lowest-levels-since-august-2024-analysts-cut-price-targets-q1-earnings/cZ1cNFjR7g1 — Barclays $75 → $60 Overweight, fuel costs and regulation; 28 of 30 brokers at Buy or higher.
28. https://investors.trip.com/news-releases/news-release-details/tripcom-group-limited-reports-unaudited-first-quarter-2026 — non-GAAP definition: excludes SBC, fair-value changes on equity securities and exchangeable senior notes, and tax effects.
29. https://seekingalpha.com/article/4945819-tripcom-q2-earnings-preview-regulatory-penalty-creates-a-buying-opportunity-upgrade — RMB3.5bn fine + RMB1.6bn confiscation "impacting Q2 results"; remedies raise take-rate and share concerns; upgrade at ~9× FY2027.
30. https://seekingalpha.com/news/4640071-tripcom-falls-5-as-hsbc-downgrades-to-hold-on-regulatory-travel-demand-concerns — HSBC Buy → Hold, −5%; soft peak season; Goldman China RevPAR −6% through late July, −1% in June, occupancy −3pp, ADR −1%.
31. https://www.thecerbatgem.com/2026/09/03/trip-com-group-nasdaqtcom-rating-lowered-to-hold-at-hsbc.html — HSBC downgrade dated 2026-09-03; Parash Jain, PT $48.
32. https://uk.investing.com/news/stock-market-news/tripcom-stock-price-target-lowered-by-bofa-on-antitrust-costs-93CH-4796372 — BofA PT cut on antitrust costs.
33. https://www.tipranks.com/news/the-fly/trip-com-price-target-lowered-to-75-from-80-at-jpmorgan — JPMorgan $80 → $75.
34. https://www.benzinga.com/z/35895117 — marketing expense +24%, compliance costs pressuring margins (`snippet_only`, weak sourcing).
35. https://seekingalpha.com/news/4607077-trip-com-targets-serving-200m-inbound-travelers-over-5-years-while-expecting-q2-net-revenue — 200m inbound travellers over five years; Q2 guide +3–8%.
36. https://www.dbs.com.sg/treasures/aics/templatedata/article/equity/data/en/DBSV/012014/9961_HK.xml — Q2 2026 international air ticketing +40–50%, overseas packaged tours doubled to >10% of segment revenue, domestic ADR modestly positive, low domestic visibility into Q3 (`snippet_only`).
37. https://www.travelerstoday.com/articles/60725/20260803/china-hotels-are-cheap-right-now-what-6-revpar-drop-means-your-summer-trip.htm — Goldman RevPAR −6% in July; China hotel prices at multi-year lows.
38. https://www.cnbc.com/2026/08/03/china-price-demand-tourism-hotel.html — tourism price wars; August weekend rates from Trip.com listings.
39. https://www.travelarbitrage.net/en/blog/peak-season-china-flights-july-august-2026/ — average domestic flight booking price in the first week of July ~20% lower YoY (`snippet_only`).
40. https://seekingalpha.com/article/4911867-tripcom-domestic-travel-strength-and-global-expansion-remain-on-track — ~US$6.7bn net cash, ~22% of market cap; $5bn repurchase ongoing.
41. https://simplywall.st/stocks/us/consumer-services/nasdaq-tcom/tripcom-group/news/is-tripcoms-buybacks-amid-ai-antitrust-suits-altering-the-in/amp — 20,285,355 shares repurchased for ~US$916m across two tranches as at late April 2026.
42. https://equibles.com/stocks/tcom/short-interest — FINRA 12,168,964 shares short at 2026-08-31 settlement, +1,292,154; days to cover 6.10; modelled 2026-09-15 figure 11.24m; next FINRA release 2026-09-24.
43. https://www.barchart.com/stocks/quotes/TCOM/put-call-ratios — put/call 0.22 (42 puts / 190 calls), undated (`snippet_only`, low confidence).
44. https://fintel.io/so/us/tcom — 35.41% institutional ownership; 270 buyers / 206 sellers LTM; $5.28bn in / $4.08bn out.
45. https://finance.yahoo.com/news/benchark-trimmed-target-price-trip-194054386.html — Benchmark PT trimmed to $72.
46. https://finance.yahoo.com/news/cfra-hikes-price-target-trip-173634674.html — CFRA raises PT, maintains Hold.
47. https://www.aaii.com/investingideas/article/503496-why-tripcom-group-limited8217s-tcom-stock-is-down-1570 — fair-value estimate trimmed $61.65 → $59.89; −12% weekly move to $39.84; −10.01% month to date.
48. https://www.tradingview.com/news/stocktwits:741027ec2094b:0-tcom-stock-on-track-to-hit-lowest-levels-since-august-2024-a-look-at-wall-street-s-take-on-trip-com/ — Stocktwits sentiment bullish → neutral, message volume high → extremely high (June 2026 snapshot); "lowest levels since August 2024" headline.
49. https://www.tipranks.com/news/class-action/trip-com-investors-file-securities-suit-over-alleged-antitrust-risk-disclosure-failures — securities suit over antitrust risk disclosure; lead-plaintiff deadline 2026-05-11.
50. https://www.chinatradingdesk.com/post/china-golden-week-2026-travel-trends-outbound-demand-and-retail-opportunities — Golden Week 1–7 Oct 2026; searches +116% by 24 Aug; >30-day advance bookings +20% YoY; international flight bookings 25 Sep–7 Oct >1.28m, +11% YoY.
51. https://www.travelandtourworld.com/news/article/ar74e8hglpjg/ — 151m air passengers over the Chinese summer season.
52. https://www.prnewswire.com/news-releases/tripcom-group-reveals-travel-trends-for-2026-302638988.html — Trip.com/Google 2026 trends: "help planning my trip" searches +190% YoY; culinary bookings +43%.
53. https://www.sec.gov/Archives/edgar/data/1269238/000119312526183482/xslF345X06/ownership.xml — **Form 4, Liang Jianzhang (director), filed 2026-04-28 for period 2026-03-18.** Smart Charm Limited (BVI, wholly owned by reporting person's spouse) entered a prepaid variable forward on 2025-09-03 over up to 1,000,000 ADSs settling Sep 2028, cash received upfront, 1,000,000 ADSs pledged, voting retained; Floor/Cap levels undisclosed; transaction code J, indirect ownership.
54. https://www.sec.gov/Archives/edgar/data/0001269238/000119312526113913/ownership.xml — Form 3, 2026-03-18 (one of ten filed that day).
55. https://www.sec.gov/Archives/edgar/data/0001269238/000119312526183379/d27369d20f.htm — FY2025 Form 20-F, filed 2026-04-28.
56. https://www.chinatravelnews.com/article/189387/ — co-founders Min Fan and Qi Ji step down from board effective 2026-02-25; May Yihong Wu and Iris Yang Xiao appointed independent directors; James Liang remains Executive Chairman, Neil Shen independent director.
57. https://www.sec.gov/Archives/edgar/data/1269238/000119312526289388/d313478d6k.htm — 6-K, 2026-06-30: 2026 AGM results, signed by CFO Cindy Xiaofan Wang.
58. https://www.sec.gov/Archives/edgar/data/0001269238/000119312526183379/d27369dex153.htm — PricewaterhouseCoopers Zhong Tian LLP consent/report dated 2026-04-28 covering FY2025 financial statements and ICFR effectiveness.
59. https://www.benzinga.com/Opinion/26/07/60851399/trip-com-hit-with-fines-after-anti-monopoly-probe-but-spared-a-major-overhaul — "hit with fines... but spared a major overhaul."
60. https://www.dimsumdaily.hk/hang-seng-index-rises-as-technology-and-financial-shares-drive-market-recovery/ — Hang Seng Tech 4,533 on 2026-09-04; 4,502 on 2026-09-08 (`snippet_only`).
61. https://ca.investing.com/news/company-news/tongcheng-travel-q2-2026-slides-revenue-up-68-as-user-growth-slows-93CH-4814041 — Tongcheng Q2 2026 revenue +6.8% to RMB5.0bn; user growth slowing.
62. https://finance.yahoo.com/markets/stocks/articles/tongcheng-travel-holdings-ltd-stu-030139468.html — Tongcheng Q2 2026: adjusted net profit +9.8% to RMB851m, accommodation revenue +12.8%, international room nights +50%, MPU −5.8% to 43.7m; no material impact observed from peers' traffic-distribution adjustments.
63. https://www.chinatravelnews.com/article/183926/ — Meituan in-store/hotel/travel steady growth, order volume +60% YoY (`snippet_only`, reporting period unconfirmed).

---

*This is a forecasting exercise over public information. It is not investment advice and must not be presented as such.*
