# Stage EU — Europe ranking for 2026-10-29

Sealed 2026-10-28 ~14:15 UTC, while the European markets were still trading, so every sealed spot and `run_up_20d_pct` is an **intraday price, not a close**. Ranked on `impact_sum` (the key `edge-scores.json` reports). Research only; no orders.

| # | ticker | mkt | session | impact_sum | floor 2.8 | abs_move | p_up | impact_scaled | panel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BOHUS | no | bmo (issuer 06:30) | +1.40 | no | 5.5 | 55 | +0.55 | 50 L |
| 2 | FDR | es | bmo (precedent) | +1.20 | no | 6.0 | 57 | +0.84 | **83 L sel** |
| 3 | IG | it | in session | +0.90 | no | 2.7 | 55 | +0.27 | 52 L |
| 4 | PDX | se | bmo (issuer 08:00) | +0.80 | no | 6.0 | 54 | +0.48 | 21 L |
| 5 | DNO | no | bmo (issuer 07:00) | +0.70 | no | 3.2 | 52 | +0.13 | 27 L |
| 6 | ENENTO | fi | in session (11:00 EET) | +0.60 | no | 4.0 | 58 | +0.64 | 65 L |
| 7 | NESTE | fi | bmo (issuer 09:00 EET) | +0.30 | no | 8.0 | 54 | +0.64 | **80 L sel** |
| 8 | AMP | it | **amc per hunter** | +0.20 | no | 6.5 | 52 | +0.26 | 51 L |
| 9 | NTGY | es | bmo / in session | +0.20 | no | 3.2 | 52 | +0.13 | 1 S |
| 10 | STMPA | fr | bmo (issuer) | +0.20 | no | 10.0 | 50 | +0.00 | 53 L |
| 11 | ENGCON_B | se | bmo (issuer 08:00) | +0.10 | no | 7.5 | 50 | +0.00 | 47 S |
| 12 | IDR | es | bmo (issuer) | +0.10 | no | 5.0 | 52 | +0.20 | 40 L |
| 13 | PPH | uk | bmo (precedent) | +0.05 | no | 5.0 | 47 | -0.30 | 3 S |
| 14 | KOG | no | bmo (issuer 07:00) | -0.10 | no | 6.5 | 47 | -0.39 | 27 S |
| 15 | RDC | de | bmo (precedent 06:30) | -0.20 | no | 6.5 | 50 | +0.00 | 2 S |
| 16 | DVD | no | bmo (precedent) | -0.30 | no | 6.0 | 45 | -0.60 | 75 S |
| 17 | AKRBP | no | bmo (issuer 06:00) | -0.40 | no | 3.3 | 47 | -0.20 | 34 S |
| 18 | EPR | no | bmo (issuer 07:00) | -0.70 | no | 6.0 | 42 | -0.96 | **81 S sel** |
| 19 | POSTI | fi | bmo (issuer 08:30 EET) | -0.80 | no | 5.5 | 47 | -0.33 | 60 S |
| 20 | AL2SI | fr | **amc per hunter** | -4.50 | **yes** | 13.0 | 45 | -1.30 | **93 S sel** |

`impact_scaled` is the hunter's second measurement, not the key; it is never pooled with it and the floor does not apply to it.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing. All four members ran, on their pinned `-intl-` agents, no fallback. Selection: 3 of 4 judges in their own top 20% on the panel's side.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 FDR      bmo     yes  83 long     4  opus5: 80L  opus55: 89L* sonnet55: 82L* fable51: 81L*  4  +1.19
   2 AL2SI    bmo?    yes  93 short    9  opus5: 99S* opus55: 78S  sonnet55: 98S* fable51: 98S*  3  -2.87
   3 EPR      bmo     yes  81 short    6  opus5: 80S  opus55: 89S* sonnet55: 72S  fable51: 84S*  3  -1.30
   4 NESTE    bmo     yes  80 long     4  opus5: 73L  opus55: 82L* sonnet55: 83L* fable51: 81L*  3  +1.18
   5 DVD      bmo?         75 short   18  opus5: 70S  opus55: 89S* sonnet55: 48S  fable51: 93S*  2  -1.23
   6 STMPA    bmo          53 long    22  opus5: 58L  opus55: 57L  sonnet55: 79L  fable51: 17L   1  +0.73
   7 ENGCON_B bmo          47 short   24  opus5: 22S  opus55: 27S  sonnet55: 54S  fable51: 83S*  1  -0.50
   8 ENENTO   bmo          65 long     7  opus5: 67L  opus55: 63L  sonnet55: 55L  fable51: 74L   0  +0.84
   9 POSTI    bmo          60 short    7  opus5: 68S  opus55: 52S  sonnet55: 54S  fable51: 68S   0  -0.76
  10 IG       bmo?         52 long     7  opus5: 57L  opus55: 57L  sonnet55: 39L  fable51: 53L   0  +0.68
  11 BOHUS    bmo?         50 long    20  opus5: 73L  opus55: 37L  sonnet55: 67L  fable51: 25L   0  +0.63
  12 AMP      bmo?         51 long    12  opus5: 37L  opus55: 69L  sonnet55: 55L  fable51: 44L   0  +0.60
  13 IDR      bmo          40 long    23  opus5: 21L  opus55: 52L  sonnet55: 73L  fable51: 15L   0  +0.47
  14 AKRBP    bmo          34 short   10  opus5: 28S  opus55: 22S  sonnet55: 44S  fable51: 44S   0  -0.46
  15 DNO      bmo          27 long     6  opus5: 35L  opus55: 20L  sonnet55: 30L  fable51: 22L   0  +0.34
  16 KOG      bmo?         27 short   16  opus5: 22S  opus55: 22S  sonnet55:  9S  fable51: 53S   0  -0.32
  17 PDX      bmo          21 long    20  opus5:  5S  opus55: 37L  sonnet55:  9L  fable51: 44L   0  +0.30
  18 PPH      bmo?          3 short   11  opus5: 14S  opus55:  0-  sonnet55: 14L  fable51: 12S   0  -0.09
  19 RDC      bmo?          2 short   47  opus5: 44S  opus55: 30L  sonnet55: 59L  fable51: 51S   0  -0.07
  20 NTGY     bmo           1 short    7  opus5: 11S  opus55:  2S  sonnet55:  0-  fable51: 10L   0  -0.04
```

`pct` is `panel_pct`, 0-100: the size of the mean of the four judges' signed percentiles, each against that judge's own live range (169 live sizes per member before today). Hunter `impact_sum` is in the ranked table above.

**Selected names.**

- **FDR long (4/4, pct 83).** Fluidra's largest US distributor and peers reported 22–28 Oct with a healthy channel: Pool Corp sales +4% with inventory −3%, Hayward North America +9% with "balanced channel inventories" and a raised guide, Pentair Pool saying its destock is complete. The peers rose 11–14% on their prints against about +4% for FDR. Against: no sourced Q3 consensus at all, Fluidra's own IR pages were unreachable (Incapsula), and the session is bmo only by precedent, not by timestamp; the read-across is a proxy, partly priced.
- **AL2SI short (3/4, pct 93; Opus 5.5 at 78, outside its top 20%).** 2CRSI's FY25/26 EBITDA guide (">36 M EUR") needs a 12.5% H2 margin against 4.7% in H1 (https://fr.ftp.opendatasoft.com/datadila/INFOFI/EQS/2026/03/FCEQS008141_20260326.pdf), the EUR1bn FY26/27 ambition was hedged on 12 Oct, and the final conclusions of the independent investigation into the Grizzly short report are due with these accounts. Against: the investigation is a two-sided tail (first instalment came back clean, +9.2% next session), and **the hunter dates the release amc** (FY24/25 at 18:33Z, H1 at 18:10Z), so the sealed bmo window close(10-28)→close(10-29) probably contains no release. Every judge sized it on the amc window. `eu_resolve.py` must be read on both windows for this name.
- **EPR short (3/4, pct 81).** SSB's store-sales value index for Europris's category (NACE 47.19) reads −0.3% y/y for Q3 against a +10.7% LFL comp, and the series has tracked the chain within about 2pp for five quarters (https://data.ssb.no/api/v0/no/table/07129); September was published the morning of the seal. Against: the bar is unsourced, Norwegian non-food peers (Clas Ohlson Norway +8% organic in September) were healthy, and the strong NOK should lift gross margin.
- **NESTE long (3/4, pct 80; Opus 5 at 73).** TotalEnergies' European refining marker averaged 33.2 $/bbl in Q3 against 13.5 in Q2, implying a Neste refining margin above the ~36 $/bbl in the Vara consensus (comparable EBITDA 1,195 MEUR), and Eni's Enilive biorefining EBIT rose 39% q/q. Against: Diamond Green Diesel's margin fell 36% q/q, the RP volume guide is at risk of a trim (H1 1,900 kt against a ~4.1 Mt full-year guide), and the name sold its record Q2 by −6.4%.

**Where the panel and the key disagree most.**

- **BOHUS** is the key's top name (+1.40) and the panel splits it (pct 50; Opus 5 73L, Fable 25L): its upside rests on a guidance raise against an unsourced EBIT bar.
- **DVD**: the key has it near zero (−0.30) and the panel at 75 short (two members in their top 20%): judges weighted the cash shell at ~3× the company's own NAV estimate more than the hunter did.
- **RDC**: Opus 5 read the 28 Sep ad-hoc as having pre-released the quarter and the raise and sized it net negative; the hunter and two others leaned long. Spread 47, panel 2.
- **NTGY**: Opus 5 resolved the two offsetting findings toward Endesa's derived Q3 (−12% EBITDA); the panel is at 1.
- **AL2SI**, the only floor-clearer, is selected, but on a window the sealed baseline does not hold (above).

**What the panel is not.** `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing; the member scales are still largely the frozen E-P seed until Europe has ~200 panel names of its own; and in the four-model re-judge the judges ranked Europe better than the live hunt (ρ +0.33/+0.34 on 48 names) — nothing about this market's panel is established.

## The universe

- **Event date 2026-10-29 (Thu)**; all ten markets open (`market_closed` null everywhere).
- `selection.method`: random sample of 78 eligible, seed `eu-2026-10-29`. 115 scheduled, 78 eligible above the $100k floor (uk 5, de 11, fr 6, se 11, dk 4, no 18, fi 12, it 3, es 6, pl 2), 20 hunted.
- `by_market`: **no 6**, fi 3, es 3, fr 2, se 2, it 2, uk 1, de 1, dk 0, pl 0. `market_concentration`: largest market Norway at **30%**, 8 markets represented. Norway's six include two oil producers (AKRBP, DNO) whose Q3 was pre-released on the same Brent run-up, and NESTE (fi) and NTGY (es) carry energy-price exposure too: a correlated exposure the scorer cannot see.
- Calendar sources: TradingView vendor plus UK RNS (PPH was added by `rns`), EQS for DE, Euronext Oslo for NO (DVD and BOHUS added there), Inderes and Nasdaq FinCal for SE/DK/FI. **Yahoo's calendar read `unavailable` in all ten markets** ("quote endpoint failed on every batch"); **bankier (PL) unavailable** (HTTP 403).
- `session_unresolved` at seal: RDC, AL2SI, AMP, IG, BOHUS, DVD, KOG, PPH. The hunters then settled most: BOHUS, KOG and RDC bmo on the issuer's own timing; DVD and PPH bmo by precedent; IG and ENENTO release **inside the session** (inside the bmo window); **AL2SI and AMP report amc** (AMP's results call is at 18:30 CET), so their sealed bmo window probably holds no release. Getting the session wrong roughly halves the move.

## The floor-clearer, and the name the key ranks top

- **AL2SI −4.50**, the only name above the 2.8 floor. Driving finding: the EBITDA guide shortfall (−3.0), source https://fr.ftp.opendatasoft.com/datadila/INFOFI/EQS/2026/03/FCEQS008141_20260326.pdf. abs_move 13 and p_up 45 carry the investigation's two-sided tail. Read it with the amc caveat above. Over the US sample the sign was a coin flip below the floor; above it is where the direction lived, and that has not been measured in Europe.
- **BOHUS +1.40**, top of the key. Driving finding: Q3 like-for-like +12.2% (pre-released 8 Oct) against a "mid single digit" short-term outlook, so a raise is plausible (+1.0). The revenue itself is `already_public`; EBIT is `new_in_release` against an unsourced bar.

Per name, the hunters flagged **already-public** periods for AKRBP, DNO, BOHUS (revenue), RDC (Rx and margin lines, 28 Sep ad-hoc) and DVD (residual cash); a **likely guidance change** (`new_in_release` on guidance) for BOHUS, IG, AMP, RDC, NESTE (volume-guide trim risk), IDR and AL2SI. On the first resolved days those two facts decided the size of the move (3.1% against 7.4% for pre-released periods, 9.0% against 2.3% on a guide change).

## Unranked and flagged

- No name is unrankable; all 20 rank.
- **STMPA**: the hunter found the baseline's 3.85% median reaction came from cadence-estimated dates; on EDGAR-checked results dates the median is ~13%, so abs_move is 10.
- **KOG**: the baseline's 0.28% reaction median came from annual-report dates; real results days ran a 6.8% median.
- **DVD**: `run_up_20d_pct` −86.6% and 352% vol are the 20.60 NOK ex-dividend gap, not a price fall, so its `priced_lean_pct` (+4.7) is an artefact.

## Instrumentation, every time

- **`options` is null in all ten markets**; Europe runs in the anchor-less regime (`archive/backtest/FINDINGS.md` §33: ρ=+0.073, p=0.45 over 104 events).
- **`anchor_covered: true` for 5 of 20**: AMP and IG (CONSOB, 1.91% / 0.5%), DVD (Finanstilsynet, 0.79%, a single market maker), PPH (FCA, 0.2%, covering) and RDC (Bundesanzeiger, 4.28%, four sellers). Every other name's register zero is the 0.5% truncation floor, not an anchor.
- Registers that resolved: uk, de, fr, se, no, fi, it. **Spain has none**: three names (FDR, IDR, NTGY) carry no positioning anchor, so their lean is the free control, and they can never be confirmed or killed after the fact. **No Polish names today.** **One German name (RDC)**, which cannot reach `event_occurred: false` either; nor can the two French and two Italian names.
- **Nordic resolve deadline**: ENGCON_B, PDX (se), ENENTO, NESTE, POSTI (fi) must be resolved within about a week or their rows resolve null.
- `lean_vs_free_control_rho` from the latest resolved run (2026-10-16): Sweden 0.6; no other market reported one.
- The lean's weights are priors borrowed from the US runs and measured nowhere in Europe.
- `history.basis`: **estimated from cadence** for AL2SI, AMP, ENENTO, ENGCON_B, FDR, IDR, IG, NESTE, NTGY, PDX, POSTI, RDC, STMPA (13 names) — a scale, never evidence a print happened on a date. Observed for the six Norwegian names (`observed_newsweb`) and PPH (`observed_rns`).
- **Language notes worth reading**: EPR's load-bearing series (SSB 47.19) is Norwegian-only; NESTE's HVO/gasoil spread readings came from the Finnish Inderes forum; FDR's Q2 refund and before-the-open practice from Renta 4 (Spanish); NTGY's Endesa Q3 derivation and price-spike drivers from Expansión only; IDR's "the new team prefers to wait" from Renta 4; ENENTO's bank barometer from Finance Finland. AKRBP, DNO and BOHUS: nothing the English sources did not carry.
- The `pre_lessons` freeze ran in every hunt; the retired `pre_local` control reports 0 names, by design.

**One day is not a result.** Twenty names, Norway-heavy, one floor-clearer whose sealed window probably does not hold its release.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
