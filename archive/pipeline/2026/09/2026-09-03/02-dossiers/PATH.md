# PATH — UiPath, Inc.

**Event confirmed: YES**, from a company source. UiPath announced on 2026-08-06 that it
will report Q2 FY2027 results (quarter ended 2026-07-31) **after the market closes on
Thursday, 2026-09-03**, with a conference call at **5:00 pm ET** [1][2].

**What this print is about.** UiPath goes into this report having roughly doubled off its
May low ($9.20 on 2026-05-14) to $17.99, up 27.6% in a month and 54% in three months —
and the rally was overwhelmingly *sector beta and narrative*, not company news. Its two
biggest August up-days (+9.31% on 08-13, +9.37% on 08-27) were both explicitly attributed
to Salesforce's beat and a broadening software bid, with no UiPath-specific catalyst
[24][25]. The result is a setup where the stock trades roughly **30% above the average
sell-side price target** ($13.87, 20 analysts, as of 2026-08-31) [12] and the sell-side is
raising targets *to catch up to the price while keeping Neutral ratings* (UBS to $19 from
$12, Neutral, 2026-08-31) [20]. The print itself is a low-drama one on the reported
numbers — the guided bar is ~$30M of net new ARR, which UBS's own channel checks call
achievable [20] — and the genuinely important guidance event, preliminary FY2028, is
expected at the **Investor Day on 2026-09-22**, nineteen days *after* this print [21][20].
So the question is not "will they beat" (they beat both lines in 7 of the last 8 quarters
[19]) but "is there anything left to say on 2026-09-03 that justifies a price 30% above
where analysts think it belongs, three weeks before the event where they would normally
say it." Triage's framing — "history of blowing through implied moves (35.8% in Dec)" — is
**wrong on the facts**, and I show why in §2.

---

## 1. Event & anchors

| Item | Value | As-of | Source |
| --- | --- | --- | --- |
| Report date | 2026-09-03 | confirmed | [1][2] company PR |
| Session | **amc** (after close), call 5:00 pm ET | confirmed | [1][2] |
| Fiscal period | Q2 FY2027, quarter ended 2026-07-31 | — | [1][2] |
| Date changed / pre-announced? | No. Announced 2026-08-06, unchanged. No 8-K since 2026-06-29 (item 5.07, annual meeting) | 2026-09-03 | [1][22] EDGAR |
| Spot | **$17.99** (close) | 2026-09-02 16:00 ET | [3] stockanalysis; corroborated by CBOE `close: 17.99` [4] |
| Prior close / 09-01 | $18.14 | 2026-09-01 | [4][5] |
| Market cap | **$9.32B** (518.12M sh) | 2026-09-02 | [3] |
| Cash + marketable securities | $1.42B | 2026-04-30 | [6] |
| EV / forward ARR | **≈4.1x** ($9.32B − $1.42B) ÷ $1.932B Q2 ARR guide midpoint | *my calculation* | [3][6] |
| 52-wk high / low | $19.84 (2025-12-08) / $9.20 (2026-05-14) | *my calculation from* [5] | [5] |
| **Event-implied move** | **13.81%** — ATM straddle, 2026-09-04 expiry, K=$18.00, mid $2.485 ÷ $17.99 | 2026-09-02 close | *my calculation from* [4] CBOE delayed chain |
| — cross-check, published | 14.01% (OptionSlam weekly implied move) | 2026-09-02/03 | [7] |
| — cross-check, published | 11% ("options data compiled by Bloomberg") | 2026-08-27 | [8] |
| — conservative convention | ~11.7% (0.85 × straddle) | 2026-09-02 | *my calculation from* [4] |
| iv30 | **85.14%** | 2026-09-02 | [4] CBOE |
| 30-day realised vol | **60.6%** annualised (close-to-close) | 2026-09-02 | *my calculation from* [5]; AlphaQuery independently reports 60.65% [9] |
| IV / RV ratio | **1.40x** | 2026-09-02 | *my calculation* |
| **IV rank / percentile** | **unavailable** — every source found is paywalled (Barchart, MarketChameleon, OptionCharts, AlphaQuery historical) | — | see §12 |

### Historical realised one-day earnings reactions

Computed by me from the daily OHLC series [5], measured close-on-report-day → close-on-
next-session. Report dates cross-checked against company press releases and the 8-K
cadence [1][6][10].

| Quarter | Reported (amc) | Reaction day | Pre-$ | Post-$ | **1-day %** | Open gap % | Intraday high % | Intraday low % | 21d run-up into print |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q2 FY25 | 2024-09-05 | 2024-09-06 | 12.74 | 11.97 | **−6.04** | +7.14 | +10.36 | −6.89 | +16.99 |
| Q3 FY25 | 2024-12-05 | 2024-12-06 | 14.95 | 14.81 | **−0.94** | +2.14 | +2.61 | −8.56 | +19.22 |
| Q4 FY25 | 2025-03-12 | 2025-03-13 | 11.83 | 9.97 | **−15.72** | −17.16 | −12.68 | −19.70 | −16.87 |
| Q1 FY26 | 2025-05-29 | 2025-05-30 | 12.94 | 13.31 | **+2.86** | +14.84 | +15.80 | −0.23 | +9.48 |
| Q2 FY26 | 2025-09-04 | 2025-09-05 | 10.85 | 11.49 | **+5.90** | +2.86 | +6.45 | +0.37 | −3.30 |
| Q3 FY26 | 2025-12-03 | 2025-12-04 | 14.86 | 18.48 | **+24.36** | +8.34 | +25.84 | +5.99 | −6.36 |
| Q4 FY26 | 2026-03-11 | 2026-03-12 | 12.38 | 11.37 | **−8.16** | −11.55 | −3.27 | −13.57 | +11.83 |
| Q1 FY27 | 2026-05-28 | 2026-05-29 | 11.58 | 11.72 | **+1.21** | −7.60 | +3.80 | −10.02 | +9.66 |

- **Last 8:** mean |move| **8.15%**, median |move| **5.97%**, max |move| **24.36%**, split **4 up / 4 down**.
- **Last 6:** mean |move| **9.70%**, median |move| **7.03%**, max **24.36%**, split **4 up / 2 down**.
- Pattern: **big open-gap reversals are the norm.** In 5 of the last 8 the close was on the
  opposite side of, or dramatically inside, the opening gap (Q1 FY26 gapped +14.8% and
  closed +2.9%; Q1 FY27 gapped −7.6% and closed +1.2%; Q4 FY26 gapped −11.6%, closed −8.2%
  after touching −13.6%). Fading the gap has been right more often than not.

**Two data conflicts I am flagging rather than resolving silently:**

1. **Triage's premise fails.** Triage cited "a history of blowing through implied moves
   (35.8% in Dec)". My computed series says the December 2025 reaction was **+24.36%**, not
   35.8%. The 35.8% figure traces to an Investing.com summary of Bloomberg options data
   [8], which also reports "May 28: +8.8%" (my series: **+1.21%**) and "March 11 2026:
   +3.0%" (my series: **−8.16%**). Where that article is independently checkable it matches
   my series (it says PATH "exceeded the options-implied move in 2 of its past 8
   announcements" — my series gives exactly 2 of 8 above ~14%: Dec-25 at +24.4% and Mar-25
   at −15.7%), so I treat its *aggregate* claim as sound and its *individual quarter*
   figures as unreliable. **PATH's history is the opposite of "blows through implied": it
   has underdelivered versus the implied move in 6 of the last 8 prints**, with a median
   realised 5.97% against implied moves that have consistently been 12–15% [8].
2. **OptionSlam independently corroborates my Q1 FY27 numbers**, reporting for 2026-05-28 a
   pre-earnings close of $11.58, a −7.59% post-earnings open and a +1.2% one-day close move
   [7] — matching my $11.58 / −7.60% / +1.21% exactly. That is strong validation of the
   price series and of the report-date mapping.

### Run-up into this print (my calculation from [5], to 2026-09-02 close)

| Window | Move | From |
| --- | --- | --- |
| 5 sessions | **+7.34%** | $16.76 (2026-08-26) |
| 10 sessions | **+14.01%** | $15.78 (2026-08-19) |
| 21 sessions (~1m) | **+27.59%** | $14.10 (2026-08-04) |
| 63 sessions (~3m) | **+54.16%** | $11.67 (2026-06-03) |
| 252 sessions (~12m) | **+65.05%** | $10.90 (2025-09-02) |

Press reports of "+36%" [23] and "+40%" [19] over a month are consistent with this
depending on the exact start date; my +27.6% is measured over exactly 21 sessions.

---

## 2. The bar

| Item | Value | Source |
| --- | --- | --- |
| Consensus non-GAAP EPS (Q2 FY27) | **$0.15** | [19][23][11] |
| — dissenting consensus | $0.13 (AltIndex) | [26] `snippet_only` |
| Consensus revenue (Q2 FY27) | **$397.85M** (one source: $397.95M) | [19][11][23] |
| Company Q2 revenue guidance | **$395–400M** | [6] company PR |
| Company Q2 ARR guidance | **$1.929–1.934B** as of 2026-07-31 | [6] company PR |
| Implied net new ARR bar | **$28–33M; ~$30M at midpoint** | [11]; UBS uses "$30M" [20] |
| Company FY27 revenue guidance | $1.776–1.781B | [6] |
| Company FY27 ARR guidance | $2.058–2.063B as of 2027-01-31 | [6] |
| Company FY27 non-GAAP op income | ~$430M | [6] |
| FY27 Street revenue | $1.78B (20 analysts) | [12] |
| FY27 Street non-GAAP EPS | $0.78 | [12] |
| Prior-year Q2 base | Revenue $362M, ARR $1.723B | [10] |
| **Implied Q2 YoY revenue growth at consensus** | **+9.9%** vs **+17.3%** in Q1 FY27 | *my calculation* from [6][10][19] |
| **Implied Q2 YoY ARR growth at guide midpoint** | **+12.1%** — flat vs Q1's +12% | *my calculation* from [6][10] |
| Consensus price target | **$13.87**, 20 analysts, Hold (2 Strong Buy / 1 Buy / 16 Hold / 1 Sell) | [12] as-of 2026-08-31 |
| — alternate | $13.20, 24 analysts, Hold (0/6/16/2/0); avg PT **down 2.59% over 3 months** | [13] `snippet_only` |
| — alternate | $14.07 (Finviz) | [14] |
| **Spot vs consensus PT** | **spot is +29.7% above the $13.87 average target** | *my calculation* |
| Whisper number | **unavailable** — no credibly published whisper found | see §12 |
| 30/60/90-day estimate revisions | **Direction only, no deltas sourced.** Near-term Q2 estimates described as "relatively stable throughout the past 30 days"; FY27 full-year estimates revised *up* over recent months | [15] `snippet_only` |

**What the company has to deliver just to hold the stock flat (my inference).** The
reported quarter is close to a formality: revenue is guided to $395–400M and consensus sits
at $397.85M, i.e. at the top of the guide, and net new ARR of ~$30M is a bar UBS's own
channel work calls achievable and possibly helped by WorkFusion seven-figure deals [20].
Beating that is table stakes. To *hold* $17.99 the company plausibly needs, in addition:
(a) an **FY27 ARR guidance raise** above $2.058–2.063B, not a reiteration; (b) an updated,
larger **AI/agentic ARR** number against the ~$200M disclosed at Q4 FY26 [16]; and (c) some
forward framing that does not simply defer everything to the 2026-09-22 Investor Day. The
structural problem is that (c) cuts against (a) and (b): a management team holding an
Investor Day in nineteen days has every incentive to keep its powder dry.

---

## 3. The one metric that matters

**Q2 net new ARR, and — more decisive for the stock — whether the FY27 ARR guide of
$2.058–2.063B is raised.**

Not EPS. Not headline revenue. UiPath's revenue line is distorted by upfront licence
recognition and by FX ($9M of the $49M Q1 net new ARR and $7M of Q1 revenue were FX
tailwind [17]), which is precisely why the Q2 revenue optics (+9.9% YoY against Q1's
+17.3%) will look worse than the business is. ARR is the metric management guides, the
metric the sell-side models, and the metric that has driven the last several reactions.

**The expectation, and how I know it:**

- Company guide implies **$28–33M net new ARR**, midpoint ~$30M [6][11].
- **UBS (2026-08-31, PT to $19 from $12, Neutral)** ran investor checks ahead of the print
  and concluded the demand backdrop is stable and "the company's $30 million net new
  annual recurring revenue target for Q2 appears achievable, particularly if bolstered by
  large WorkFusion deals, noting one seven-figure deal occurred in June" [20]. This is the
  single most specific, most recent, most credible statement of the bar I could source.
- For scale: net new ARR was **$49M in Q1 FY27** [6][17], **$59M in Q3 FY26** [10]. The
  Q2 bar of ~$30M is seasonally normal (Q2 FY26 added ~$30M: $1.693B→$1.723B) but is not a
  number that, if merely met, changes anyone's growth model.
- Supporting metrics management discloses and the market will read: **customers >$1M ARR**
  (374, +18% YoY at Q1 [17]), **customers >$100K ARR** (2,620, +11% [17]), **dollar-based
  net retention** (109%, 108% normalised [17]), **gross retention** (97% [17]), and the
  **AI/agentic ARR** figure first disclosed at ~$200M in March 2026 [16].

**My inference:** meeting $30M net new ARR is already in the price at $17.99. The
asymmetry sits in the FY27 ARR guide. A raise to ~$2.07B+ with a bigger AI ARR number is
the bull trigger; a reiteration — the most likely outcome given the Investor Day sits 19
days later — is a "sell the news" setup against a 27.6% one-month run-up.

---

## 4. Fundamentals — what changed, what is at stake

**Q1 FY2027 (reported 2026-05-28), the base for this print** [6][17]:

| Metric | Q1 FY27 | Comment |
| --- | --- | --- |
| Revenue | $418M, +17% YoY (+15% ex-FX) | $7M FX tailwind |
| ARR | $1.901B, +12% YoY | $49M net new, incl. $9M FX |
| Dollar-based net retention | 109% (108% normalised) | up from 107% at Q3 FY26 [10] |
| Gross retention | 97% | |
| GAAP operating income | **+$28M (7% margin)** | **first GAAP-profitable Q1 in company history**, vs −$16M LY |
| Non-GAAP operating income | $92M (22% margin) | +250bp YoY |
| GAAP gross margin / non-GAAP | 82% / 83% | |
| GAAP / non-GAAP diluted EPS | $0.04 / $0.15 | |
| Operating cash flow | $132M | |
| Non-GAAP adjusted FCF | $130M | |
| Cash + marketable securities | $1.42B | |
| Share repurchases in quarter | $244M | |
| RPO / current RPO | $1.413B (+15%) / $988M (+17%) | cRPO growing faster than ARR [18] |
| Customers >$1M ARR / >$100K | 374 (+18%) / 2,620 (+11%) | [17] |

**What changed since the last print:**

1. **WorkFusion closed 2026-02-06** (financial-crime-compliance AI agents, AML/KYC), inside
   fiscal Q1 FY27. Terms undisclosed. It is now cited by UBS as a source of large Q2 deals
   [20][27]. It also contaminates the organic ARR comparison — management normalises for
   "FX and M&A" [17], and the panel should treat any ARR beat that leans on WorkFusion as
   lower quality.
2. **Balance-sheet/capital-return posture shifted.** The prior $1B of authorisations was
   exhausted by 2026-03-10; the board authorised a new **$500M** programme on 2026-03-05,
   of which **$436.9M remained at 2026-04-30** [28]. *My inference:* the buyback was
   enormously accretive when it was executed against a $9–12 stock in H1 2026; at $17.99 it
   buys ~40% fewer shares per dollar. Buyback-driven EPS support is materially weaker from
   here, and the market has not obviously repriced that.
3. **Agentic products moved from pilot to production**, per management, one year into GA;
   16 of the top 20 Q1 deals included AI, and AI expansion deals were described as 6x
   larger than non-AI [17]. This is the entire bull narrative and it is, so far, a
   qualitative claim attached to one quantitative disclosure (~$200M AI ARR, March 2026
   [16]).
4. **Index inclusion is already behind it.** PATH joined the S&P MidCap 400 effective
   2026-01-02 (announced 2025-12-24) [29]. The forced-buying flow is spent; it is not a
   source of support into this print.

**Unit economics / margin trajectory.** 83% non-GAAP gross margin, 22% non-GAAP operating
margin expanding 250bp YoY, FY27 guided to ~$430M non-GAAP op income on $1.78B revenue
(~24%) [6]. The profitability story is genuinely good and genuinely improving. The growth
story is not: ARR +12%, guided flat at +12% for Q2, and UBS models ~9% ARR growth on its
CY27 numbers [20]. **What is at stake is which of those two the market is paying for.** At
~4.1x EV/ARR (*my calculation*) and 16x CY27 FCF per UBS [20], the multiple embeds an
acceleration that the guide does not contain.

**Customer concentration:** no material concentration disclosed or found; 2,620 customers
>$100K ARR [17]. **Headcount:** ~3,754 worldwide as of December 2025, +2.2% YoY, with 270
active job postings in 2025 (+80.5% vs 2024) — after three rounds of layoffs since 2022,
the most recent being ~10% (≈420 roles) announced July 2024 [30] `snippet_only`. Modest
rehiring, not expansion.

---

## 5. Positioning & options

All computed by me from the CBOE delayed options chain snapshot taken 2026-09-03 08:33 UTC,
reflecting the **2026-09-02 close** (`last_trade_time: 2026-09-02T15:59:59`) [4].

**IV term structure — steeply inverted, textbook event kink:**

| Expiry | ATM K | Straddle mid | % of spot | ATM call IV | ATM put IV |
| --- | --- | --- | --- | --- | --- |
| **2026-09-04** | 18.00 | $2.485 | **13.81%** | **233.0%** | **232.7%** |
| 2026-09-11 | 18.00 | $2.765 | 15.37% | 129.0% | 116.6% |
| 2026-09-18 | 18.00 | $3.045 | 16.93% | 99.9% | 102.9% |
| 2026-10-16 | 18.00 | $3.970 | 22.07% | 81.0% | 79.1% |
| 2026-11-20 | 18.00 | $4.960 | 27.57% | 74.2% | 75.4% |
| 2027-01-15 | 18.00 | $6.320 | 35.13% | 73.7% | 72.6% |

Front-week IV of 233% collapsing to ~100% one week out and ~74% by November. IV crush after
the print will be violent — roughly 130 vol points on the front week.

**Skew — essentially flat, and this matters.** At the 2026-09-04 expiry the ATM call IV
(233.0%) and ATM put IV (232.7%) are indistinguishable. Wings: the $16.00 put prints 233.4%
against the $20.00 call at 229.2%; the $15.00 put 229.9% against the $21.00 call 230.4%.
There is **no downside crash premium being paid.** AlphaQuery's independent 30-day figures
agree in direction: IV skew −0.0019, put/call IV ratio 1.0291 [9]. *My inference:* the
options market is pricing a large move with **no directional bias**, which is unusual for a
name that has just run 27.6% — a positioned-for-upside market usually shows call skew, and
a fearful one shows put skew. This one shows neither, which is consistent with a genuine
two-sided distribution rather than a consensus lean.

**Put/call — heavily call-tilted, with visible lottery-ticket buying:**

| Measure | Value | Source |
| --- | --- | --- |
| Whole-chain P/C open interest | **0.518** (call OI 412,276 / put OI 213,631) | *my calculation from* [4] |
| Whole-chain P/C volume | 0.687 (call 23,987 / put 16,488) | *my calculation from* [4] |
| 2026-09-04 expiry P/C open interest | 0.792 | *my calculation from* [4] |
| 2026-09-04 expiry P/C volume | 0.991 | *my calculation from* [4] |
| AlphaQuery 30-day P/C volume | 0.169 | [9] — conflicts sharply; different methodology/window, I trust my own computation |
| AlphaQuery 30-day P/C open interest | 0.267 | [9] — same caveat |

The most striking single line in the chain: on 2026-09-02 the **largest call volume in the
entire 2026-09-04 expiry was the $23.00 strike — 1,550 contracts traded at $0.10–0.12**,
against 1,086 open interest. $23.00 is **+27.8% above spot on a two-day option**. The
$24.00 strike traded 521 contracts at $0.05–0.08. Large resting call OI also sits at $17.00
(4,303), $19.00 (3,491), $18.00 (3,224) and $20.00 (2,545) [4]. *My inference:* this is
retail/speculative upside crowding, not institutional hedging. It is exactly the
configuration that produces a violent unwind if the print is merely fine.

**Short interest — large, but not squeezable:**

| Measure | Value | As-of | Source |
| --- | --- | --- | --- |
| Shares short | **117,881,355** | 2026-08-14 settle | [31] MarketBeat |
| % of float | **29.33%** | 2026-08-14 | [31]; Finviz corroborates 29.27% / 117.88M [14] |
| Days to cover | **1.7** | 2026-08-14 | [31]; Finviz 1.75 [14] |
| Change vs prior period | −3.02% | 2026-08-14 | [31] |
| Peak short interest | 138,917,884 (34.6% of float) | 2026-06-30 | [31] |
| FINRA shares short | 120M = 23.46% of shares outstanding, DTC 1.42, ADV 85.5M | 2026-07-31 | [32] |
| **Borrow fee** | **0.38%** | **2026-09-02** | [32] ShortInterestTracker |
| Shares available to borrow | 7.6M (7.3M on 09-01, 7.8M on 08-31) | 2026-09-02 | [32] |
| Conflicting figure | 52.29M shares, 12.95% of float, DTC 4.3 | undated | [33] Benzinga `snippet_only` — inconsistent with two agreeing sources; I discount it |
| Institutional / insider ownership | 68.82% / 22.26% | — | [14] |

*My inference:* the "29% short float" headline overstates the squeeze case badly. At a
**0.38% borrow fee** with **7.6M shares still available to lend** and **1.4–1.7 days to
cover** on 60–85M-share average daily volume, shorts are neither trapped nor bleeding.
They can exit inside two sessions for essentially nothing. Moreover **21 million shares of
short interest were already covered between the 2026-06-30 peak (138.9M) and 2026-08-14
(117.9M)** — a meaningful part of the squeeze fuel has been consumed *during* the rally,
which is very likely part of what caused it.

**How crowded does the trade look?** Crowded long. Retail sentiment "extremely bullish"
with 7-day message volume +90% and PATH a top-10 trending ticker at recent readings [34];
whole-chain P/C OI at 0.52; speculative far-OTM call buying on the event expiry; and a
27.6% one-month run-up. Against that, the sell-side is 16-of-20 Hold with a target 30%
below spot [12]. **Price is being set by momentum and retail, not by the marginal
fundamental buyer.**

---

## 6. Sentiment & alt-data

- **Retail / social.** Stocktwits has repeatedly shown PATH at "extremely bullish"
  sentiment (93/100 at one reading) with "extremely high" message volume, 7-day message
  volume +90%, top-10 trending, and at spikes +1,090% chatter in 24 hours [34]. Retail
  framing includes "it will be next Palantir" [29]. **A current 7/14/30-day sentiment
  series is unavailable** — Stocktwits' sentiment page is login-gated and returned N/A for
  every window [35]. The readings above are directional context, not a recent measurement,
  and I am treating them as supporting colour only.
- **Analyst rating changes and PT drift.** The drift is *up in level, unchanged in
  conviction*:
  - **UBS, 2026-08-31: PT $19 from $12, Neutral maintained.** Checks show "a stable demand
    backdrop"; $30M net new ARR "appears achievable"; cautions the stock is ~16x CY27 FCF
    against ~9% ARR growth; flags the late-September investor day as the key catalyst with
    preliminary FY2028 guidance expected [20].
  - **RBC (Matthew Hedberg): PT $15 from $12, Sector Perform maintained** [20-adjacent
    listing]; RBC separately described "business trends stabilizing as automation demand
    grows" [36].
  - Barclays PT to $16 from $15 [37]; Needham upgraded Hold→Buy on 2026-03-12 [13].
  - Consensus PT $13.87 / 20 analysts / Hold [12]; a second provider has $13.20 / 24
    analysts and notes the **average PT fell 2.59% over three months** [13].
  - *My inference:* four separate firms have raised targets into the rally while holding
    Neutral-equivalent ratings. That is the signature of analysts marking to market, not of
    conviction changing. No upgrade wave has accompanied the +54% three-month move.
- **Alt-data.** **Largely unavailable.** No Google Trends series, app-rank, web-traffic or
  review data could be sourced for PATH. The one usable proxy is hiring: ~3,754 employees
  (Dec 2025, +2.2% YoY) with 270 active job postings in 2025, +80.5% vs 2024 [30]
  `snippet_only` — consistent with stabilising-to-modestly-expanding go-to-market, not with
  an acceleration. UBS's investor checks [20] are the closest thing to a demand-side channel
  read I could source, and they say "stable", not "inflecting".

---

## 7. Forensics

All Form 4 detail below is parsed by me directly from the primary XML on SEC EDGAR [22].

| Date | Insider | Role | Code | Shares | Price | Held after | Plan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-08-19 | **Daniel Dines** | CEO & Chairman, >10% owner | S (sale) | **1,402,347** | $16.0726 avg (range $16.00–16.16) | 26,491,238 direct | **10b5-1** |
| 2026-08-13 | Hitesh Ramani | Chief Accounting Officer | S | 25,000 | $16.50 | 260,052 | **10b5-1** |
| 2026-08-14 | Hitesh Ramani | Chief Accounting Officer | S | 25,000 | $16.75 | 235,052 | **10b5-1** |
| 2026-07-01 | R. Malpani | CPO & CTO | F (tax withhold) | 27,932 | $10.87 | 596,106 | n/a — routine RSU/PSU vest |
| 2026-07-01 | A. Gupta | COO & CFO | F | 42,792 | $10.87 | 1,029,716 | n/a — routine |
| 2026-07-01 | B. Brubaker | GC & CLO | F | 22,019 | $10.87 | 828,906 | n/a — routine; also ESPP purchase of 1,367 sh at $9.14 on 2026-06-10 |
| 2026-07-01 | H. Ramani | CAO | F | 8,980 | $10.87 | 285,052 | n/a — routine |
| 2026-06-25 | K. Terrell | Director | A (grant) | 19,175 RSU | $0.00 | 100,292 | annual director comp |
| 2026-06-25 | D. Springer | Director | A (grant) | 19,175 RSU | $0.00 | 154,294 | annual director comp |

**Reading it:**

- **Every sale is 10b5-1, none discretionary.** Dines' sales run under a plan adopted
  **2026-04-15** permitting up to **2,975,000 shares through 2026-10-14**, subject to limit
  prices, held via IceVulcan Investments Ltd.; the company framed it as personal
  diversification representing <5% of his holdings [38]. He retains 26.49M shares directly
  [22]. **This is not a signal.** The plan predates the rally by four months.
- **But note what is absent:** no insider has bought on the open market, and **no insider
  sold above $16.75** despite the stock trading $17.99–18.67 for the last four sessions.
  Dines' plan carries limit prices [38] — the panel should not read the absence of
  August-end sales as a bullish tell; it is more likely a blackout-window effect ahead of a
  2026-09-03 print. Form 144s were filed 08-13, 08-14 and 08-19 and none since [22].
- **No executive or director departures** found. Ashim Gupta remains COO & CFO (a role he
  expanded into in September 2024, not a 2026 change) [39]. Dines remains CEO & Chairman.
- **No auditor change, restatement, material weakness or going-concern language** found in
  any 2026 filing or news search.
- **8-K cadence is quiet and clean.** The most recent 8-K is 2026-06-29 (item 5.07, annual
  meeting voting results); before that 2026-05-28 (Q1 results) and 2026-03-11/03-05 (Q4
  results and buyback authorisation) [22][28]. **No pre-announcement, no guidance update,
  no strategic 8-K in the nine weeks before this print.** For a stock that has run 54% in
  three months, management's silence is itself informative: nothing has been
  pre-signalled, so the print carries the full information load.
- **Filing-language / tone:** no shift detectable from the sources I could reach. The Q1
  FY27 call language was confident but explicitly framed as a "prudent outlook" on guidance
  [17] — management has been deliberately conservative on ARR guides, which cuts both ways
  (easier to beat, less credible when they raise).

---

## 8. Macro & peer read-through

**The tape is the bull case.** Enterprise software has been re-rating hard into this print:

- **Salesforce** (reported late August 2026): revenue $11.35B vs $11.32B consensus, adjusted
  EPS $5.90 vs $3.27, FY revenue range raised to $46.1–46.4B from $45.9–46.0B [24][40].
- **Snowflake** (reported ~2026-09-01/02): revenue +35% to $1.55B vs $1.48B expected,
  adjusted EPS $0.62 vs $0.45, product revenue guided to $6.1B (+36%) [40][41].
- **Workday** also reported strongly the prior week [41].
- Commentary framing: these results "further undermine those who claim software companies
  are in danger of disruption from artificial intelligence agents", with analysts
  "separating durable AI consumption winners from cyclically softer SaaS incumbents" [41].
- **Automation-software cohort specifically:** the group beat Q2 revenue consensus by 5.2%
  on average and guided next-quarter revenue 3.8% above consensus [42]. Pegasystems and
  Appian both carry favourable estimate revisions on AI/workflow-automation demand [42].

**But the read-through cuts against PATH's price, not for it.** UiPath's own August rally
was *caused* by these peer prints, explicitly and repeatedly:

- **2026-08-13, +9.31%** on 104.5M shares: "UiPath shares jumped 9% and Pegasystems rose 4%
  despite neither company reporting earnings this week… driven by Salesforce's strong
  earnings report… not by any news specific to UiPath itself" [24].
- **2026-08-27, +9.37%** on 72.0M shares: "UiPath Rallies 9% as the Software Bid Broadens
  Beyond the Earnings Winners" [25].

*My inference:* PATH has already been paid, twice, for other companies' good news. The
sector-beta credit is spent. This print has to be paid for on UiPath's own numbers, at a
price 30% above where the sell-side thinks the company is worth. Note also that on
**2026-09-02, the day Snowflake blew out its print, PATH fell 0.83%** [5] — the sympathy
bid had already stopped working.

**Rate / FX / commodity sensitivity.** Long-duration unprofitable-to-recently-profitable
software; rate-sensitive via multiple, not via P&L. FX is a live and material item for
this specific print: $9M of Q1's $49M net new ARR and $7M of Q1 revenue were FX tailwind
[17], and Q1 FY27 RPO grew 15% reported / 16% ex-FX [18]. A weaker dollar flatters the Q2
ARR print; the panel should discount an ARR beat that is FX-driven. No commodity exposure.

---

## 9. Bull case / bear case / base case

**Bull case (≈30% likelihood, my estimate).** UiPath beats the low $30M net new ARR bar
comfortably — helped by WorkFusion, whose seven-figure deals UBS's checks already picked up
[20] — raises the FY27 ARR guide above $2.063B, and puts a materially larger number on
AI/agentic ARR against the ~$200M last disclosed in March 2026 [16]. The sector tape is
maximally supportive (Salesforce, Snowflake, Workday all beat and raised [40][41]; the
automation cohort beat revenue by 5.2% and guided 3.8% above [42]), the demand backdrop is
independently described as stable [20], and the company has beaten both lines in 7 of 8
quarters [19]. Into that, ~118M shares (29% of float) are still short [31], the whole-chain
P/C OI is 0.52 with visible far-OTM call crowding [4], and the front-week straddle only
needs a 13.8% move to pay — PATH has delivered +24.4% once in the last eight prints [5].
This is precisely the Q3-FY26 configuration that produced +24.36%. Rests on: [20][40][41][42][31][4][5][19].

**Bear case (≈45%, my estimate).** Nothing about the reported quarter is in doubt and
therefore nothing about it can be worth 27.6% of one-month upside. The guide requires only
$30M of net new ARR against $49M in Q1 [6][17]; consensus revenue of $397.85M is +9.9% YoY
against Q1's +17.3%, so the headline will read "growth halved" [6][10][19]; ARR growth is
guided flat at 12% [6]; and **the FY28 guidance that would justify the multiple is expected
at the 2026-09-22 Investor Day, not on this call** [20][21] — management has a strong
incentive to say nothing new. Meanwhile the stock trades 29.7% above a $13.87 consensus
target that 16 of 20 analysts still rate Hold [12], and the four firms that moved targets
recently all kept Neutral-equivalent ratings [20][13][37]. Positioning is crowded long
(P/C OI 0.52; 1,550 contracts of the +27.8% OTM $23 strike bought on 2026-09-02 [4]) while
the short base that could squeeze has already shrunk 21M shares from its June peak and
costs 0.38% to carry with 1.4 days to cover [31][32] — i.e. the fuel is spent and the
shorts are comfortable. Finally, **PATH's own history is unambiguous on this specific
configuration**: the four largest positive 21-day run-ups into a print (+17.0%, +19.2%,
+9.7%, +9.5%) produced reactions of −6.04%, −0.94%, +1.21% and +2.86% — mean −0.73%, never
better than +3% — while both of the two big up-moves (+24.4%, +5.9%) came off *negative*
run-ups (−6.4%, −3.3%) [5]. The current run-up, +27.6%, is **larger than any of the eight**.
Rests on: [5][6][12][17][19][20][21][4][31][32].

**Base case (≈50% of probability mass on magnitude, my estimate).** A clean beat on
revenue and EPS, net new ARR at or slightly above $30M, FY27 ARR guide reiterated or
nudged rather than raised, warm agentic commentary, and everything forward-looking punted
to 2026-09-22. The stock gaps on the headline and then reverts — which is literally what it
has done in 5 of the last 8 prints [5] — and **the realised move comes in well inside the
13.8% implied**. The median realised |move| over the last eight is 5.97% and PATH has
exceeded a ~14% implied move only twice in eight tries [5][8]. Direction inside that band
leans mildly negative on the run-up and valuation evidence above.

---

## 10. What would flip the consensus view

**The most credible reversal is a raised FY27 ARR guide paired with a hard AI-ARR number.**
Concretely: if management guides FY27 ARR to **above $2.08B** (vs the current $2.058–2.063B
[6]) *and* discloses AI/agentic ARR of **$300M or more** (vs ~$200M at Q4 FY26 [16]) *and*
frames net new ARR as re-accelerating into H2 rather than deferring to the Investor Day,
then the bear case collapses. That combination would convert the story from "12% ARR
grower trading at 4.1x ARR on narrative" to "ARR re-accelerating with a quantified AI
line", which is exactly the distinction the market has been rewarding across software this
quarter [41]. In that world the 29%-of-float short base [31] and the call-heavy chain [4]
turn the +24.36% December-2025 outcome into a live scenario rather than a tail.

The second, cheaper reversal: **management pre-releases elements of the FY28 framework on
this call rather than saving them for 2026-09-22.** UBS explicitly expects preliminary FY28
guidance at the Investor Day and "a formal multi-year forecast appears unlikely" [20]. If
that expectation is wrong and FY28 arrives on 2026-09-03 with an ARR growth number starting
with a 1, the "nothing left to say" pillar of my bear case is gone.

A third, weaker one: I have been unable to source **IV rank/percentile** or a **whisper
number** (§12). If IV rank turns out to be low rather than high — i.e. 85% iv30 is normal
for this name rather than elevated — then the 13.8% implied move is less obviously rich
versus a 5.97% median realised, and my "priced for more than it usually delivers" argument
weakens.

---

## 11. My read

**Preliminary direction score: −22. Preliminary probability of an up move: 41%.
Conviction: Medium.**

The single most important thing I found is that **triage's premise is factually wrong**.
PATH does not blow through its implied move; it has come in *under* the implied move in 6
of the last 8 prints, with a median realised absolute move of 5.97% against implied moves
that have run 12–15% [5][8]. The 35.8% December figure triage relied on does not exist in
the price data — the actual reaction was +24.36% [5]. That does not make the name
uninteresting; it inverts the framing. The dispersion is real but the *option is expensive
relative to the historical distribution*, and the more likely error for a panel here is
over-forecasting magnitude, not under-forecasting it.

On direction I lean modestly negative, and the strongest single piece of evidence is
PATH-specific rather than generic: in this name, large pre-print run-ups have consistently
produced flat-to-negative reactions (four biggest 21-day run-ups → mean −0.73%, max +2.86%),
while both big up-moves came off negative run-ups [5]. The current +27.6% run-up is the
largest in the eight-quarter sample. Layer on a stock 29.7% above consensus PT [12], a
guidance bar that is easy but a guidance *event* that has been deliberately scheduled 19
days later [20][21], and options positioning that is crowded on the call side with
lottery-ticket buying on the event expiry [4] — and the risk is asymmetric to the downside
on a merely-good print. n=8 is small; that is why conviction is Medium and not High.

---

## 12. Coverage gaps

| Gap | Why it matters | What I tried |
| --- | --- | --- |
| **IV rank / IV percentile — unavailable** | Without it I cannot say whether 85.1% iv30 is high *for PATH*. My "options are expensive vs history" claim leans on IV/RV (1.40x) and on implied-vs-realised move history instead, which is weaker. | Barchart (403/empty), MarketChameleon (paywall), OptionCharts (paywall), AlphaQuery historical (free access expired). |
| **Whisper number — unavailable** | If the buy-side bar is above the $0.15 / $397.85M sell-side bar, a "beat" could still disappoint. I have only UBS's qualitative "$30M net new ARR is achievable" [20]. | Multiple targeted searches; nothing credibly published. |
| **30/60/90-day estimate-revision magnitudes — direction only** | I can say Q2 estimates were "relatively stable" over 30 days and FY27 estimates drifted up [15], but I have no deltas. A quantified revision trend would sharpen the "bar" section materially. | Zacks/Yahoo/StockAnalysis searches returned prose, not numbers. |
| **Current retail sentiment 7/14/30-day series — unavailable** | My social read rests on undated Stocktwits articles, not a recent measurement. Stocktwits' own sentiment page is login-gated and returned N/A. | [35]. |
| **Google Trends / web traffic / app-rank alt-data — unavailable** | No independent demand proxy for the quarter. Job postings [30] are the only alt-data I could source and they are 2025-vintage. | Multiple searches; nothing usable found. |
| **Cloud ARR — not disclosed** | UiPath stopped breaking out cloud ARR after Q2 FY26 ($1.080B, +>25% [10]). Its absence removes a mix-quality check on the ARR line. | Q3 FY26, Q4 FY26 and Q1 FY27 releases checked — not present [6][10]. |
| **WorkFusion purchase price / ARR contribution — undisclosed** | Any Q2 ARR beat could be inorganic and I would not be able to tell. Management normalises for M&A but does not size it [17][27]. | [27] and IR searches; terms not disclosed. |
| **Exact share count / market cap basis** | StockAnalysis: 518.12M shares, $9.32B [3]; Finviz: 455.76M shares, $9.43B [14]. Likely Class A vs. all classes. My EV/ARR of 4.1x moves with this. | Both cited; I used [3]. |
| **Short-interest conflict** | Benzinga's 52.29M / 12.95% / 4.3 DTC [33] contradicts MarketBeat and Finviz, which agree exactly at 117.88M / ~29.3% / 1.7 [31][14]. I used the two that agree. | All three checked. |
| **Domains unreachable via WebFetch** | Recorded for the run log: **benzinga.com (403)**, **seekingalpha.com (403)**, **barchart.com (empty body)**, **marketchameleon.com / optioncharts.io / optionslam.com detail (paywalled)**, **stocktwits.com sentiment (login-gated)**. Figures from these are marked `snippet_only` where used. | WebSearch snippets used as fallback throughout. |

**Recency note.** Every positioning, price and options figure in this dossier is from the
**2026-09-02 close** (the last completed session before the event) except the borrow-fee
series, which is dated 2026-09-02 [32], and short interest, which is the 2026-08-14
settlement [31] / 2026-07-31 FINRA record [32] — the most recent available. Nothing here is
older than three weeks except where explicitly dated.

---

## 13. Sources

1. UiPath IR — "UiPath Announces Second Quarter Fiscal 2027 Financial Results Conference Call" (2026-08-06): confirms 2026-09-03 amc, 5:00pm ET, quarter ended 2026-07-31. https://ir.uipath.com/news/detail/456/uipath-announces-second-quarter-fiscal-2027-financial-results-conference-call
2. BusinessWire, same release (2026-08-06): event confirmation. https://www.businesswire.com/news/home/20260806817905/en/UiPath-Announces-Second-Quarter-Fiscal-2027-Financial-Results-Conference-Call
3. StockAnalysis PATH overview: spot $17.99 (2026-09-02 16:00 EDT), market cap $9.32B, 518.12M shares, 52-wk range. https://stockanalysis.com/stocks/PATH/
4. CBOE delayed options chain, PATH (snapshot 2026-09-03 08:33 UTC, last trade 2026-09-02T15:59:59): close $17.99, iv30 85.138, full chain — basis for all straddle, term-structure, skew, P/C OI and volume calculations. https://cdn.cboe.com/api/global/delayed_quotes/options/PATH.json
5. StockAnalysis daily price history API, PATH, 5-year daily OHLCV: basis for all historical earnings-reaction, run-up, 52-week and realised-volatility calculations. https://stockanalysis.com/api/symbol/s/path/history?range=5Y&period=Day (page: https://stockanalysis.com/stocks/path/history/)
6. UiPath IR — "UiPath Reports First Quarter Fiscal 2027 Financial Results" (2026-05-28): Q1 FY27 revenue/ARR/margins/EPS/FCF/cash/buyback, Q2 and FY27 guidance. https://ir.uipath.com/news/detail/452/uipath-reports-first-quarter-fiscal-2027-financial-results
7. OptionSlam PATH earnings page: next earnings 2026-09-03, weekly implied move 14.01%, monthly 17.07%; 2026-05-28 pre-earnings close $11.58, open −7.59%, 1-day close +1.2%, max −10.01%. https://www.optionslam.com/earnings/stocks/PATH
8. Investing.com (2026-08-27) — "UiPath shares may move 11% on earnings release next week": Bloomberg-sourced 11% implied move; "exceeded the options-implied move in 2 of its past 8 announcements"; the individual-quarter figures I dispute in §2. https://www.investing.com/news/stock-market-news/uipath-shares-may-move-11-on-earnings-release-next-week-93CH-4879714
9. AlphaQuery PATH volatility & option statistics (2026-09-02): 30-day IV mean 0.8557, IV calls 0.8434, IV puts 0.8679, HV close-to-close 0.6065, IV skew −0.0019, put/call IV ratio 1.0291, P/C volume 0.1691, P/C OI 0.2665. https://www.alphaquery.com/stock/PATH/volatility-option-statistics/30-day/iv-mean
10. UiPath IR — "UiPath Reports Third Quarter Fiscal 2026 Financial Results" (2025-12-03): Q3 FY26 revenue $411M, ARR $1.782B, net new ARR $59M, DBNR 107%, Q4 guidance; also Q2 FY26 comparatives (revenue $362M, ARR $1.723B, cloud ARR $1.080B). https://ir.uipath.com/news/detail/420/uipath-reports-third-quarter-fiscal-2026-financial-results
11. MoneyCheck — UiPath Q2 FY2027 earnings preview: consensus $0.15 / $397.85M; Q2 guidance implies $28–33M net new ARR, ~$30M midpoint. https://moneycheck.com/uipath-path-stock-q2-fiscal-2027-earnings-preview-and-what-analysts-predict
12. StockAnalysis PATH forecast (as-of 2026-08-31): consensus PT $13.87, 20 analysts, Hold, 2/1/16/1/0 breakdown; FY27 revenue $1.78B, EPS $0.78. https://stockanalysis.com/stocks/path/forecast/
13. MarketBeat PATH forecast: PT $13.20 / 24 analysts / Hold (0/6/16/2/0); average PT −2.59% over 3 months; Needham upgrade Hold→Buy 2026-03-12. `snippet_only` https://www.marketbeat.com/stocks/NYSE/PATH/forecast/
14. Finviz PATH short-interest page: short float 29.27%, 117.88M shares short, short ratio 1.75, shares out 455.76M, float 402.77M, market cap $9.43B, avg vol 67.22M, inst. own 68.82%, insider own 22.26%, analyst target $14.07. https://finviz.com/quote.ashx?t=PATH&ty=si
15. MoneyCheck / Zacks-sourced commentary on estimate revisions: Q2 estimates "relatively stable" over past 30 days; FY27 full-year estimates revised up in recent months. `snippet_only` https://moneycheck.com/uipath-path-stock-q2-fiscal-2027-earnings-preview-and-what-analysts-predict
16. Investing.com — UiPath Q4 FY26 coverage: first-time disclosure of ~$200M ARR from AI-related offerings (agents, Maestro, IDP), March 2026. `snippet_only` https://www.investing.com/news/earnings/uipath-forecasts-full-year-revenue-above-expectations-stock-seesaws-after-hours-4555553
17. Motley Fool — UiPath (PATH) Q1 FY2027 earnings call transcript (2026-05-28): net new ARR $49M incl. $9M FX; revenue +17% incl. $7M FX (+15% ex-FX); DBNR 109%/108%, GRR 97%; customers >$1M ARR 374 (+18%), >$100K 2,620 (+11%); 16 of top 20 deals included AI, AI expansion deals 6x larger; "prudent outlook" guidance philosophy. https://www.fool.com/earnings/call-transcripts/2026/05/28/uipath-path-q1-2027-earnings-transcript/
18. UiPath Q1 FY27 RPO disclosure: RPO $1.413B (+15%, +16% ex-FX ~$9M headwind), cRPO $988M (+17%). https://www.sec.gov/Archives/edgar/data/0001734722/000173472226000041/path-20260430.htm
19. Seeking Alpha (2026-09-02) — "UiPath up 40% in a month; now Q2 earnings will test the AI story": consensus $0.15 / $397.85M near high end of $395–400M guide; beat both lines in 7 of last 8 quarters. `snippet_only` (403 on fetch) https://seekingalpha.com/news/4639454-uipath-up-40-in-a-month-now-q2-earnings-will-test-the-ai-story
20. Investing.com (2026-08-31) — "UBS raises UiPath stock price target to $19 on stable demand": PT $19 from $12, Neutral; checks show stable demand backdrop; $30M Q2 net new ARR "achievable", WorkFusion seven-figure deal in June; ~16x CY27 FCF vs ~9% ARR growth; 83% gross margin; late-September investor day the key catalyst with preliminary FY2028 guidance expected, formal multi-year forecast unlikely. Also carries RBC PT $15 from $12, Sector Perform (Matthew Hedberg). https://www.investing.com/news/analyst-ratings/ubs-raises-uipath-stock-price-target-to-19-on-stable-demand-93CH-4882598
21. StockTitan — UiPath Investor Day, Las Vegas, 2026-09-22, 11:30am PT / 2:30pm ET, webcast. https://www.stocktitan.net/news/PATH/ui-path-announces-upcoming-investor-awazeopqq9hi.html
22. SEC EDGAR, UiPath (CIK 0001734722) filing index and Form 4 primary XML documents — full insider-transaction detail in §7, plus 8-K cadence (latest 2026-06-29 item 5.07) and Form 144 dates (08-13, 08-14, 08-19). https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001734722&type=4&dateb=&owner=include&count=40 ; e.g. Dines 2026-08-19: https://www.sec.gov/Archives/edgar/data/1734722/000185576726000017/primarydocument.xml ; Ramani 2026-08-13/14: https://www.sec.gov/Archives/edgar/data/1734722/000185576426000009/primarydocument.xml
23. Benzinga (2026-09) — "UiPath Q2 Preview: Stock Up 36% in One Month, Will Earnings Keep the Rally Going?": +36% one-month, consensus $0.15/$397.85M, agentic pilot-to-production framing. `snippet_only` (403 on fetch) https://www.benzinga.com/trading-ideas/previews/26/09/61581608/uipath-q2-preview-stock-up-36-in-one-month-will-earnings-keep-the-rally-going
24. Pluang / 24-7 Wall St coverage of 2026-08-13: UiPath +9%, Pegasystems +4% with neither reporting; driven by Salesforce's Q2 FY27 beat and raise; IGV +3% vs QQQ +1%. https://pluang.com/en/news-feed/ui-path-dan-pegasystems-naik-sektor-perangkat-lunak-menguat-pasca-laporan
25. 24/7 Wall St (2026-08-27) — "UiPath Rallies 9% as the Software Bid Broadens Beyond the Earnings Winners, Pegasystems Gains 4%". https://247wallst.com/investing/2026/08/27/uipath-rallies-9-as-the-software-bid-broadens-beyond-the-earnings-winners-pegasystems-gains-4/
26. AltIndex PATH earnings page: next report 2026-09-03 amc, EPS estimate $0.13, price $18.14, +55.4% over 3 months. `snippet_only` https://altindex.com/earnings-calendar/path
27. WorkFusion / UiPath — acquisition of WorkFusion (financial-crime compliance AI agents), completed 2026-02-06, terms undisclosed. https://www.workfusion.com/news/uipath-acquires-workfusion-strengthening-agentic-solutions-for-financial-services/ and https://www.uipath.com/newsroom/uipath-acquires-workfusion-strengthening-agentic-solutions-for-financial-services
28. UiPath Form 10-Q for quarter ended 2026-04-30 and 8-K 2026-03-05: $500M repurchase authorisation approved 2026-03-05; prior $1B of authorisations (Sept 2023 + Aug 2024) fulfilled by 2026-03-10; $436.926M remaining at 2026-04-30. https://www.sec.gov/Archives/edgar/data/0001734722/000173472226000041/path-20260430.htm ; https://www.sec.gov/Archives/edgar/data/1734722/000173472226000007/path-20260305.htm
29. Investing.com / Stocktwits — S&P MidCap 400 inclusion announced 2025-12-24, effective before the open 2026-01-02 (replacing Synovus); retail "next Palantir" framing. https://www.investing.com/analysis/uipath-jumps-as-sp-midcap-400-entry-triggers-forced-buying-dynamics-200672322 ; https://stocktwits.com/news-articles/markets/equity/ui-path-gains-spotlight-with-key-index-inclusion/cLessLOREvG
30. Revelio Labs / NBC News — UiPath headcount 3,754 worldwide as of Dec 2025 (+2.2% YoY), 270 active job postings in 2025 (+80.5% vs 2024); July 2024 restructuring cut ~10% of workforce (≈420 roles). `snippet_only` https://www.reveliolabs.com/companies/uipath/employees/ ; https://www.nbcnews.com/business/business-news/uipath-lay-10-workforce-companywide-restructuring-rcna160993
31. MarketBeat PATH short interest: 2026-08-14 settlement 117,881,355 shares, 29.33% of float, 1.7 days to cover, −3.02% MoM; peak 138,917,884 (34.6%) at 2026-06-30. https://www.marketbeat.com/stocks/NYSE/PATH/short-interest/
32. ShortInterestTracker PATH (2026-09-02): borrow fee 0.38%, 7.6M shares available (7.3M 09-01, 7.8M 08-31); FINRA 2026-07-31 120M shares short = 23.46% of shares outstanding, ADV 85.5M, days-to-cover 1.42. https://shortinteresttracker.com/stock/PATH
33. Benzinga PATH short interest: 52.29M shares, 12.95% of float, days-to-cover 4.3, −6.67% MoM. `snippet_only`, conflicts with [31][14] and discounted. https://www.benzinga.com/quote/PATH/short-interest
34. Stocktwits news coverage of PATH retail sentiment: "extremely bullish" (93/100), "extremely high" message volume, 7-day message volume +90%, top-10 trending; separate episodes of +1,090% 24h chatter and +188% user message count. Undated relative to this print — supporting colour only. https://stocktwits.com/news-articles/markets/equity/ui-path-stock-turns-retail-traders-more-bullish-after-nvidia-led-ai-partnerships/ch6brWiR3X4 ; https://stocktwits.com/news-articles/markets/equity/uipaths-agentic-ai-bet-is-winning-over-retail-investors/cmU1L4sR47n
35. Stocktwits PATH sentiment page — login-gated, returned N/A for all windows (1d/1w/1m/3m/6m/1y). Recorded as a coverage gap. https://stocktwits.com/symbol/PATH/sentiment
36. MarketScreener — "UiPath Business Trends Stabilizing as Automation Demand Grows, RBC Says". `snippet_only` https://www.marketscreener.com/news/uipath-business-trends-stabilizing-as-automation-demand-grows-rbc-says-ce7d50dadb8aff20
37. TipRanks/The Fly — UiPath price target raised to $16 from $15 at Barclays. `snippet_only` https://www.tipranks.com/news/the-fly/uipath-price-target-raised-to-16-from-15-at-barclays
38. UiPath 8-K / disclosure of Dines 10b5-1 plan: IceVulcan Investments Ltd. adopted 2026-04-15, up to 2,975,000 shares through 2026-10-14 subject to limit prices, announced 2026-05-28, described as <5% of holdings. https://www.sec.gov/Archives/edgar/data/0001734722/000173472226000037/path-20260528.htm
39. UiPath IR / BusinessWire — Ashim Gupta expanded to COO in addition to CFO, effective 2024-09-05 (no 2026 change). https://ir.uipath.com/news/detail/357/uipath-chief-financial-officer-ashim-gupta-takes-on-expanded-role-as-chief-operating-officer
40. Benzinga (2026-08) — "Snowflake Stock Rises as Salesforce's Beat Lifts Enterprise Software": Salesforce revenue $11.35B vs $11.32B, adj. EPS $5.90 vs $3.27, FY guide raised to $46.1–46.4B. https://www.benzinga.com/trading-ideas/movers/26/08/61478008/snowflake-stock-rises-as-salesforces-beat-lifts-enterprise-software
41. SiliconANGLE (2026-09-02) — Snowflake revenue +35% to $1.55B vs $1.48B expected, adj. EPS $0.62 vs $0.45, product revenue guided $6.1B (+36%); framing that these results "undermine those who claim software companies are in danger of disruption from AI agents". https://siliconangle.com/2026/09/02/snowflake-knocks-it-out-the-park-with-a-stellar-earnings-and-revenue-beat/
42. StockStory — "Q2 Earnings Highlights: Pegasystems Vs The Rest Of The Automation Software Stocks": cohort beat revenue consensus by 5.2%, next-quarter guidance 3.8% above; favourable estimate revisions for PEGA and APPN. https://stockstory.org/us/stocks/nasdaq/pega/news/earnings/q2-earnings-highlights-pegasystems-nasdaqpega-vs-the-rest-of-the-automation-software-stocks

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
