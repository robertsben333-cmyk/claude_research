# Stage EU — Europe ranking for 2026-11-19

Sealed 2026-11-18 from 14:40 UTC, while the European markets were still trading. Spots are intraday, not closes. Ranking key: `impact_sum` (as `edge-scores.json` reports it). **No name clears the 2.8 conviction floor.** Over the whole US sample the sign below the floor was a coin flip. One day is not a result.

## Ranked table

| # | ticker | mkt | session | impact_sum | abs_move | p_up | already public | new in release |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SGE | uk | bmo | +0.95 | 6.5 | 56 | 9M revenue (+10% organic) | first FY27 guide, buyback |
| 2 | AUROORA | fi | bmo? (hunter: 09:00 EET, bmo) | +0.90 | 6.0 | 55 | nothing | Q3 numbers |
| 3 | LIO | uk | bmo | +0.80 | 5.0 | 53 | both quarters' AuMA/flows | margin, buyback |
| 4 | HLMA | uk | bmo | +0.60 | 6.5 | 55 | Sep trading update (margin guide raised) | H1 numbers, photonics guide |
| 5 | XPS | uk | bmo | +0.60 | 3.5 | 50 | H1 revenue, "slightly ahead" | H1 margin |
| 6 | GPE | uk | bmo | +0.35 | 3.0 | 53 | H1 leasing, Aldermanbury sale | valuation, NTA |
| 7 | MBR | pl | bmo? | +0.30 | 6.5 | 54 | company eco-bomb revenue guide | Q3, likely Q4 estimate raise |
| 8 | NEU | pl | bmo? | +0.20 | 4.5 | 57 | nothing | Q3, UOKiK fine accounting |
| 9 | SUBC | no | bmo | +0.20 | 4.5 | 51 | FY26 guide | first 2027 guide (and Saipem's, same session) |
| 10 | AGO | pl | bmo | +0.00 | 5.5 | 50 | nothing | Q3 |
| 11 | MHA | uk | bmo | +0.00 | 3.0 | 52 | H1 revenue, FY27 on track | H1 EBITDA |
| 12 | PAY | uk | bmo | +0.00 | 5.5 | 48 | FY27 "in line" three times | Q2 numbers, net debt |
| 13 | UBI | fr | **amc per hunter** (baseline bmo?) | +0.00 | 9.0 | 49 | Q2 bookings guide | FY guide reconfirm-or-cut |
| 14 | BAB | uk | bmo | −0.30 | 5.0 | 48 | AGM update in line | HY27, Gateway contract status |
| 15 | GRI | uk | bmo | −0.30 | 4.5 | 51 | 11-month trading update | first FY27 guide, buyback |
| 16 | ATT | pl | **amc per hunter** (baseline bmo?) | −0.80 | 5.0 | 48 | Q3 headline numbers (5 Nov) | Q4 commentary, cash flow |
| 17 | HAUTO | no | bmo | −1.00 | 6.5 | 46 | Q3 trading updates | dividend, Q4 guide |
| 18 | ELIOR | fr | amc | −1.20 | 13.0 | 44 | nothing (no Q3/Q4 revenue release) | first FY27 guide |

Not ranked: **AQ** (calendar phantom: the Q3 report came out 2026-10-15 and the next report is 2027-02-11, per the issuer's Q3 PDF; the row came from inderes) and **CMCX** (calendar phantom: the interims moved to 26 Nov per the company's 7 Oct release and its financial calendar).

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran; no fallback was used.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 ELIOR    amc     yes  99 short    1  opus5: 98S* opus55:100S* sonnet55:100S* fable51:100S*  4  -3.27
   2 AUROORA  bmo?    yes  86 long     3  opus5: 90L* opus55: 88L* sonnet55: 84L* fable51: 83L*  4  +1.40
   3 MBR      bmo?    yes  86 long    10  opus5: 71L  opus55: 90L* sonnet55: 98L* fable51: 83L*  3  +1.56
   4 HLMA     bmo          75 long     3  opus5: 75L  opus55: 78L  sonnet55: 70L  fable51: 76L   1  +1.07
   5 SGE      bmo          73 long    12  opus5: 68L  opus55: 76L  sonnet55: 90L* fable51: 56L   1  +0.97
   6 UBI      bmo?         14 short   58  opus5: 45L  opus55: 58S  sonnet55: 84S* fable51: 42L   1  -0.09
   7 LIO      bmo          56 long    12  opus5: 68L  opus55: 58L  sonnet55: 36L  fable51: 59L   0  +0.71
   8 SUBC     bmo          49 long    15  opus5: 65L  opus55: 26L  sonnet55: 54L  fable51: 52L   0  +0.67
   9 NEU      bmo?         56 long     8  opus5: 51L  opus55: 58L  sonnet55: 68L  fable51: 46L   0  +0.65
  10 ATT      bmo?         50 short    8  opus5: 38S  opus55: 62S  sonnet55: 48S  fable51: 52S   0  -0.59
  11 AGO      bmo          44 long    16  opus5: 52L  opus55: 34L  sonnet55: 66L  fable51: 23L   0  +0.48
  12 XPS      bmo          40 long    11  opus5: 38L  opus55: 56L  sonnet55: 42L  fable51: 26L   0  +0.43
  13 BAB      bmo          38 short   10  opus5: 30S  opus55: 41S  sonnet55: 53S  fable51: 29S   0  -0.39
  14 PAY      bmo          27 long    22  opus5: 30L  opus55: 42L  sonnet55: 46L  fable51: 10S   0  +0.38
  15 GPE      bmo          22 long    14  opus5:  8L  opus55: 28L  sonnet55: 43L  fable51: 10L   0  +0.22
  16 HAUTO    bmo          22 long    44  opus5: 77L  opus55: 54L  sonnet55: 20S  fable51: 23S   0  +0.18
  17 GRI      bmo           6 long    22  opus5: 28L  opus55:  8L  sonnet55: 29S  fable51: 18L   0  +0.16
  18 MHA      bmo           4 long     3  opus5:  4L  opus55:  5L  sonnet55:  8L  fable51:  0-   0  +0.07
```

`sel` = 3 of 4 judges in their own top 20% (the market panels' rule). `pct` = `panel_pct`, the size of the mean of the four signed percentiles, each read against that judge's own live range.

**Selected names:**

- **ELIOR, short, 4 of 4, panel_pct 99.** The judges named three things: the first FY2026-27 guide on a name whose guide days moved −24.3%, +6.8% and −26.8%; France's 1.6% SMIC rise from 1 Dec 2026, the first top-up since 2012, landing on cleaning and catering pay grades ([economiematin](https://www.economiematin.fr/?p=239530)); and Sodexo's FY27 guide coming in below consensus ([tradingsat](https://www.tradingsat.com/sodexo-FR0000121220/actualites/sodexo-pour-relancer-sa-croissance-sodexo-propose-un-menu-mi-figue-mi-raisin-au-marche-mais-un-grand-contrat-avec-meta-emballe-la-bourse-1166854.html)), all set against FY27 consensus that has EPS nearly doubling. **The strongest case against:** Italian press reports the loss-making Trenitalia contract moving to a newco from September, which removes an overhang. The FY27 consensus comes from one aggregator, and every negative is a macro or peer proxy. **The session is amc**: the window is the 19 Nov close to the 20 Nov close.
- **AUROORA, long, 4 of 4, panel_pct 86.** The judges named the issuer's own statement that earnings are weighted to H2, a record 169.6 MEUR backlog, small insider buys after the quarter closed, and acquisitions that Inderes says it has not yet modelled. **The strongest case against:** a single analyst sets the bar, a 90-day lock-up overhang follows the September ABB, and every finding is small.
- **MBR, long, 3 of 4, panel_pct 86** (Opus 5 at 71, outside its top 20%). The judges named the company's public eco-bomb revenue guide pointing above Erste's 47m EBITDA, and the CEO's remark that the Q4 estimate is "już jednak historia" (already history) after 28m PLN of Q4 tender wins. **The strongest case against:** Erste's sell-the-news warning on a thin 2027 backlog, a stock near its record, and a Q3 2025 release that came amc. A bmo window could miss the release.

**Where the panel and `impact_sum` disagree most:** ELIOR is the hunter's bottom name and the panel's strongest, the same sign at a much larger panel scale. MBR is 7th on `impact_sum` (+0.30) but selected by the panel. HAUTO is the hunter's second-most negative name (−1.00), while the panel reads it +0.18 long with the day's widest split (sd 44: Opus 5 at 77L, Sonnet 5.5 and Fable 5.1 short). LIO is 3rd on the key but unselected.

**What these numbers are not:** `panel_score` ranks and does not forecast. There is no `expected_edge_pct` off the US. Certainty (`p_up`) is recorded and decides nothing. The member scales are still mostly the frozen E-P seed until this market has about 200 panel names of its own. In the four-model re-judge the judges ranked Europe better than the live hunt, but the EU panel has no measured edge yet (2026-10-21: ρ +0.22, p 0.19 on 45 names).

## What drives the top and the bottom

- **Top, SGE +0.95:** the first FY27 guide (+1.0 finding). Q3 underlying revenue grew +12%, against FY27 consensus of 9.4% ([9M trading update](https://www.investegate.co.uk/announcement/rns/sage-group--sge/trading-update-for-nine-months-ended-30-june-2026/9692278)). This is an inference; management has said nothing on FY27. A buyback renewal by pattern adds +0.5.
- **Bottom, ELIOR −1.20:** the SMIC finding (−1.0, [economiematin](https://www.economiematin.fr/?p=239530)) and the Sodexo read-through (−0.5), partly offset by the Italian rail exit (+0.5).

## The day's composition and its caveats

- **The draw:** `selection.method` is a random sample of 34 eligible names, seed `eu-2026-11-19`. 79 were scheduled and 34 eligible (uk 15, pl 10, se 3, fr 2, no 2, dk 1, fi 1). The 20 drawn: uk 10, pl 4, fr 2, no 2, se 1, fi 1. **Largest market: UK, 50% of the day**, across 6 markets.
- **Calendar sources:**
  - UK RNS calendar read: 14 dated for the target, 2 added (SYS, JD.).
  - Yahoo read in all ten markets.
  - Issuer calendars: inderes (se, dk, fi) and Euronext Oslo were read.
  - **bankier (pl) returned HTTP 403**, so no Polish issuer calendar was read.
  - Two of the 20 drawn rows were phantoms: CMCX (vendor) and AQ (inderes).
- **Session:**
  - **`session_unresolved`:** AQ, ATT, AUROORA, MBR, NEU, UBI. Their window was assumed, and getting it wrong roughly halves the move.
  - The hunters settled AUROORA (09:00 EET, bmo) and NEU (bmo by overnight filing timestamps).
  - **They moved UBI and ATT to amc** on the issuers' filing patterns. That is inferred, not timestamped.
  - MBR stays bmo by its 2026 precedent, but Q3 2025 came out amc.
- **Option anchor:** `options` is null in all ten markets. Europe runs in the anchor-less regime (ρ=+0.073, p=0.45 over 104 events on the sealed corpus).
- **Short registers:**
  - Read: uk, fr, se, no, fi.
  - **pl is unreadable**: 4 names, all with no positioning anchor and no way to be confirmed or killed after the fact.
  - **No Spanish names** today.
  - **No German names**, so none that cannot reach `event_occurred: false` for that reason.
  - **`anchor_covered: true`: 9 of 20** (BAB, CMCX, GRI, LIO, PAY, SGE, XPS, ELIOR, UBI, and AQ, which is not ranked; so 9 of the 18 ranked).
  - The rest read as truncated zeros (GPE, HLMA, MHA, HAUTO, SUBC, AUROORA) or an unreadable register (the 4 Polish names).
- **`lean_vs_free_control_rho`:** the last resolved European run is **2026-10-16**, which reports se 0.6 only. Nothing European has been resolved for a month, and the Nordic names from that gap can no longer be confirmed or killed (the feed's window is about 12 days).
- **The lean's weights** are priors borrowed from the US runs, measured nowhere in Europe.
- **Estimated `history.basis`** (a scale, not a record of dates): AGO, AQ, ATT, AUROORA, MBR, NEU (pl/se/fi) and ELIOR, UBI (fr). Observed: the UK names (`observed_rns`) and HAUTO and SUBC (`observed_newsweb`). AGO's and AUROORA's hunters each found the baseline's estimated dates wrong.
- **Language notes worth quoting:**
  - ELIOR: the Trenitalia contract transfer reached only Italian regional press (Il Giorno), and the SMIC detail only French press.
  - SUBC: the decisive context (Saipem's calendar and previews) was Italian.
  - Polish names: every load-bearing source was Polish (ESPI filings, PAP consensus, Parkiet).
  - Most UK notes: "nothing the English sources did not already carry".

The orchestration ran up to 8 hunters at once (the platform's cap), not waves of 5, to reach the IBKR handoff before the European close.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
