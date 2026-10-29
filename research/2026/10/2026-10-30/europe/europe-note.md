# Stage EU — Europe ranking for 2026-10-30

Sealed 2026-10-29 at about 15:00 UTC, while the European markets were still trading, so every sealed spot and `run_up_20d_pct` is an **intraday price, not a close**. Ranked on `impact_sum`, the key `edge-scores.json` reports. Research only; no orders.

**Answer first: a quiet day.** No name clears the 2.8 conviction floor. The largest hunter number is EBP +1.10 and the most negative is ACX −1.20. The four-model panel selects two shorts:

- **ACX:** 4 of 4 judges, `panel_pct` 90.
- **GXI:** 3 of 4 judges, `panel_pct` 79.

Both are bmo names whose session is not confirmed by the issuer. Two names, GSJ and SCYR, have no print on this date and are not ranked.

| # | ticker | mkt | session | impact_sum | floor 2.8 | abs_move | p_up | impact_scaled | panel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | EBP | pl | bmo (precedent 07:24) | +1.10 | no | 4.5 | 56 | +0.54 | 61 L |
| 2 | SAN | fr | bmo (precedent 05:30) | +0.95 | no | 4.5 | 53 | +0.27 | 17 L |
| 3 | SCATC | no | bmo (issuer 07:00) | +0.40 | no | 8.5 | 52 | +0.34 | 16 S |
| 4 | LOOMIS | se | bmo (issuer 07:30) | +0.30 | no | 6.0 | 53 | +0.36 | 34 L |
| 5 | BONHR | no | bmo (issuer) | +0.25 | no | 4.0 | 54 | +0.32 | 9 L |
| 6 | ACA | fr | bmo (precedent 07:00) | +0.10 | no | 3.5 | 52 | +0.14 | 14 L |
| 7 | NONG | no | bmo (precedent 05:30 UTC) | +0.10 | no | 3.5 | 54 | +0.28 | 2 L |
| 8 | GIL | de | not checked (no timestamp) | −0.05 | no | 0.5 | 50 | +0.00 | 2 S |
| 9 | UNI | es | bmo (presentation 11:00) | −0.10 | no | 4.5 | 48 | −0.18 | 5 S |
| 10 | ANORA | fi | bmo (issuer 08:30 EET) | −0.40 | no | 5.5 | 46 | −0.44 | 56 S |
| 11 | MDATA | no | bmo (precedent 07:00) | −0.40 | no | 6.5 | 48 | −0.26 | 15 S |
| 12 | NWG | uk | bmo (RNS 07:00) | −0.50 | no | 4.5 | 51 | +0.09 | 15 S |
| 13 | KMAR | no | bmo (issuer 07:00) | −0.60 | no | 6.0 | 46 | −0.48 | 52 S |
| 14 | CABK | es | bmo (webcast 09:00) | −0.70 | no | 4.5 | 46 | −0.36 | 57 S |
| 15 | TUB | es | bmo (issuer calendar 09:00) | −0.70 | no | 4.5 | 44 | −0.54 | 47 S |
| 16 | GXI | de | bmo (issuer calendar; precedent ~09:00) | −0.90 | no | 6.0 | 48 | −0.24 | **79 S sel** |
| 17 | TRIFOR | dk | bmo (issuer 07:00) | −0.90 | no | 7.0 | 47 | −0.42 | 35 S |
| 18 | ACX | es | bmo (issuer calendar) | −1.20 | no | 6.5 | 44 | −0.78 | **90 S sel** |

`impact_scaled` is the hunter's second measurement, (2·p_up/100 − 1)·abs_move. It is not the key, it is never pooled with it, and the floor does not apply to it.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.

- All four members ran on their pinned `-intl-` agents, with no fallback.
- Selection rule: 3 of 4 judges in their own top 20%, on the panel's side.
- Each judge's own top 20% starts at |impact_sum| of: Opus 5 1.44, Opus 5.5 0.96, Sonnet 5.5 0.80, Fable 5.1 0.98 (189 live sizes each).

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 ACX      bmo?    yes  90 short    3  opus5: 90S* opus55: 91S* sonnet55: 84S* fable51: 93S*  4  -1.63
   2 GXI      bmo?    yes  79 short   14  opus5: 93S* opus55: 84S* sonnet55: 55S  fable51: 83S*  3  -1.20
   3 EBP      bmo?         61 long    18  opus5: 52L  opus55: 91L* sonnet55: 55L  fable51: 46L   1  +0.65
   4 CABK     bmo?         57 short   17  opus5: 70S  opus55: 51S  sonnet55: 32S  fable51: 76S   0  -0.77
   5 ANORA    bmo          56 short   17  opus5: 67S  opus55: 51S  sonnet55: 32S  fable51: 76S   0  -0.74
   6 KMAR     bmo          52 short   12  opus5: 32S  opus55: 57S  sonnet55: 55S  fable51: 63S   0  -0.70
   7 TUB      bmo?         47 short    8  opus5: 42S  opus55: 51S  sonnet55: 38S  fable51: 57S   0  -0.56
   8 TRIFOR   bmo          35 short   15  opus5: 32S  opus55: 47S  sonnet55: 12S  fable51: 50S   0  -0.48
   9 LOOMIS   bmo          34 long    17  opus5: 21L  opus55: 51L  sonnet55: 12L  fable51: 50L   0  +0.45
  10 SCATC    bmo          16 short   56  opus5: 63S  opus55: 66L  sonnet55:  6L  fable51: 73S   0  -0.33
  11 MDATA    bmo?         15 short    5  opus5: 15S  opus55:  7S  sonnet55: 17S  fable51: 22S   0  -0.24
  12 NWG      bmo          15 short    7  opus5: 12S  opus55:  7S  sonnet55: 17S  fable51: 25S   0  -0.22
  13 ACA      bmo?         14 long     7  opus5:  9L  opus55:  7L  sonnet55: 17L  fable51: 25L   0  +0.20
  14 SAN      bmo?         17 long    32  opus5: 13S  opus55: 56L  sonnet55: 43L  fable51: 17S   0  +0.17
  15 UNI      bmo?          5 short   10  opus5: 12L  opus55: 14S  sonnet55:  6S  fable51: 10S   0  -0.14
  16 BONHR    bmo           9 long     5  opus5:  6L  opus55:  7L  sonnet55:  6L  fable51: 18L   0  +0.13
  17 NONG     bmo?          2 long     4  opus5:  4L  opus55:  7L  sonnet55:  3S  fable51:  0-   0  +0.05
  18 GIL      bmo?          2 short    2  opus5:  0-  opus55:  3S  sonnet55:  3S  fable51:  0-   0  -0.03
```

**ACX (Acerinox), short, selected by 4 of 4.**

- **The case:** the July guide promised Q3 EBITDA "slightly higher" than Q2's €176m and did not mention energy. Since then:
  - Spanish wholesale power averaged €143.3/MWh in September, the highest month since 2022.
  - MIBGAS gas is up 143.5% year on year.
  - Aperam, the closest peer, put energy at about €20m of EBITDA a quarter.
  - LME nickel fell from about $17,064/t to about $15,700/t, which the company itself warned would pull surcharges and prices down.
  - Aperam described European demand as "unchanged at a low level".
  - The Q4 guide, which moved the stock +10.7% in July, is the line all of this lands on.
- **Strongest case against:**
  - The macro is public.
  - The stock is already about 7% below its early-September level.
  - North American Stainless raised base prices from 1 October.
  - No CNMV short register can be read, so positioning is unknown.
- Sources: the Acerinox investor calendar and the Aperam Q3 release, via `hunts/ACX.json`.

**GXI (Gerresheimer), short, selected by 3 of 4** (Sonnet 5.5 at p55, outside its top 20%).

- **The case:** the company publishes a Vara consensus dated 2026-10-21.
  - The full-year adjusted EBITDA margin of 17.2% sits at the bottom of the 17–18% guide.
  - Free cash flow of −€101.7m is outside the −€50m to −€100m guide.
  - Hitting the guide needs €223–255m of H2 EBITDA against a Q2 run rate of €102m.
  - The stock is up 15.4% in 20 sessions to a 52-week high, above 13 of 15 broker targets, with no catalyst found.
  - Disclosed shorts are covering, 3.87% → 3.38%.
- **Strongest case against:**
  - Q3 closed on 31 Aug, and management still held the guide on 30 Sep with no ad-hoc since, so a large Q3 miss is unlikely.
  - The sealed lean is +2.24, the most positive of the day, driven by the short-squeeze component.
  - The issuer calendar says 15:00 CET. That is probably the call, with the release earlier as on the last three prints, but it is not settled.

**Where the panel and the hunters disagree most**

- **EBP:** the hunters' #1 at +1.10, but only Opus 5.5 puts it in its own top 20%, so `panel_pct` is 61.
- **SAN:** the hunters' #2 at +0.95; the judges split on its sign (Opus 5 and Fable short, Opus 5.5 and Sonnet long), so `panel_pct` is 17.
- **SCATC:** the widest disagreement of the day (sd 56). Opus 5 and Fable put it short around p63–73, Opus 5.5 long at p66, Sonnet 5.5 near zero.
- **NWG:** the hunter's sum is −0.50 but its scaled number is +0.09, an internal split the hunter itself recorded.

**What the panel numbers are not**

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- Member scales outside the US are still mostly the frozen stage E-P seed, until Europe has about 200 panel names of its own.
- In the four-model re-judge, the judges ranked Europe better than the live hunt, on 48 names. That is a lead, not a result.

## Names not ranked

- **GSJ (Grupo Empresarial San José, es): no results release on 2026-10-30.**
  - The issuer's own periodic-information page shows every nine-month report since 2016 uploaded on 5–21 November, after the close (last on 2025-11-20).
  - The vendor date is a cadence guess, and it already missed Q1.
  - `event_confirmed: false`. Spain has no day archive, so `eu_resolve.py` cannot confirm the absence either.
- **SCYR (Sacyr, es): reports 2026-11-03 after the close, not 2026-10-30.**
  - Source: the issuer's convocation notice of 21/10/2026, which reads *"La publicación de los resultados será el martes día 3 de noviembre de 2026 tras el cierre de mercado"* ("results will be published on Tuesday 3 November 2026 after the market close").
  - https://sacyr.com/-/anuncio-convocatoria-resultados-9m-2026
  - Phantom for this window.

Both phantoms are Spanish rows. ACX and TUB, also Spanish, entered from Yahoo's calendar and were then confirmed by their issuers.

## What every note must say

**Selection**

- Method: `random sample of 33 eligible, seed 'eu-2026-10-30'`. 61 rows were scheduled and 33 eligible above the $100k floor.
- Eligible by market: uk 3, de 4, fr 3, se 3, dk 1, no 8, fi 3, it 0, es 7, pl 1.
- Hunted by market: uk 1, de 2, fr 2, se 1, dk 1, no 5, fi 1, it 0, es 6, pl 1.
- The draw is random among the eligible names.
- **Market concentration:** Spain is the largest market at 6 of 20 (0.30), and nine markets are represented. No single market dominates the day, but **two of the six Spanish names were phantoms**.

**Calendar sources**

- TradingView, plus the UK RNS crawl (5 RNS-dated rows for the target date, none added).
- Yahoo added four rows: ACA and SAN (fr), ACX and TUB (es).
- Issuer calendars read for de, se, dk, no and fi. Poland's bankier source read **unavailable** (HTTP error).

**Session**

- Every name is `bmo`.
- `session_unresolved: true` at seal on 13 names: ACA, ACX, CABK, EBP, GIL, GSJ, GXI, MDATA, NONG, SAN, SCYR, TUB, UNI. Each hunter checked the session; the session column above gives the basis.
- **GIL** has no release timestamp at all, so the resolver should measure both windows.
- **GXI's** issuer time is 15:00 CET, which is inside the Xetra session either way.

**Options and anchors**

- `options` is null in all ten markets. Europe runs in the anchor-less regime, the one `archive/backtest/FINDINGS.md` §33 priced at ρ = +0.073, p = 0.45 over 104 events.
- Short registers that resolved: uk, de, fr, se, dk, no, fi. Spain and Poland have none.
- **4 of 20 names carry `anchor_covered: true`**: GXI, LOOMIS, NWG, SCATC.
- Nine more were read and not named: ACA, ANORA, BONHR, GIL, KMAR, MDATA, NONG, SAN, TRIFOR. That is a truncated zero, not an anchor.

**Weak markets**

- **Spain and Poland: 7 of 20 names** (es 6, pl 1). They have no positioning anchor, their `priced_lean_pct` is the run-up (the free control itself), and they can never be confirmed or killed after the fact.
- **Germany: 2 names** (GIL, GXI), which cannot reach `event_occurred: false` either.
- **Nordic names: 8** (SCATC, BONHR, KMAR, MDATA, NONG, LOOMIS, TRIFOR, ANORA). The Sweden, Denmark and Finland ones (LOOMIS, TRIFOR, ANORA) must be **resolved within about a week**, or the Nasdaq Nordic feed stops reaching them.

**Lean against the free control**

- The last resolved European run is 2026-10-16. There `lean_vs_free_control_rho` was reported only for se, at 0.6.
- **No European run sealed after 2026-10-16 has been resolved.** The 10-19 to 10-23 Nordic names are at or past their roughly 12-day archive window.
- The lean's weights are priors borrowed from the US runs, measured nowhere in Europe.

**History basis**

- **Estimated cadence on 14 names**, a scale and not a record of dates: ACA, ACX, ANORA, CABK, EBP, GIL, GSJ, GXI, LOOMIS, SAN, SCYR, TRIFOR, TUB, UNI.
- Observed history: NWG (`observed_rns`) and the five Oslo names (`observed_newsweb`).
- GSJ is the worked example of what an estimated cadence can do: its estimated history dates (for example 2025-10-29) are not its real release dates (2025-11-20).

**Conviction floor**

- No name sits above `conviction_floor` 2.8.
- Over the whole US sample the sign was a coin flip below the floor, and every name today is below it.

**Already public and new in release**

- **SCATC** pre-released the period: on 21 Oct it cut its FY power-production EBITDA guide by NOK 300m and fell 23.9%. The print carries "further updates" and a strategy update, which is why its `abs_move_pct` is the day's largest at 8.5.
- **GXI** pre-released Q1 and Q2 and published its own consensus.
- **ANORA** and **NWG** have published bars (an analyst consensus and a company-compiled consensus, respectively).
- **GIL**'s minority payout is fixed by its profit-and-loss transfer agreement (DPLTA), so a near-zero move is structural.
- Everyone else's quarter is new numbers with the guidance line in play:
  - **CABK:** the CFO deferred any NII guide refinement to January.
  - **NWG:** full-year consensus already sits above the guide.
  - **ACX:** the Q4 guide.
  - **UNI:** a possible small raise.

**Language notes worth quoting**

- **ACX:** the Spanish energy press (OMIE and Grupo ASE via roams.es) carried the power and gas numbers no English source tied to the company.
- **EBP:** the bar, the peer tables and the bank's own current reports were Polish-only.
- **MDATA:** the data-centre moratorium story appeared only in E24/NTB.
- **GSJ** and **SCYR:** the decisive date evidence was Spanish-only.
- **NWG:** the domestic UK sources added nothing.

**Run notes**

- All 20 hunts returned `search_complete: true`.
- `scripts/hunt_status.py`, the backstop CLAUDE.md describes, is not on `main`, so that cross-check could not be run.

**One day is not a result.**

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
