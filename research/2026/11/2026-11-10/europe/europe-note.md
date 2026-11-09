# Stage EU — Europe ranking for 2026-11-10 (Tue)

Sealed Mon 2026-11-09 at ~14:47 UTC while the European markets were still trading, so every sealed `spot` and `run_up_20d_pct` is an **intraday price, not a close**. Ranked on `impact_sum` (`edge-scores.json` `ranking_key`), conviction floor 2.8. **No name clears the floor. One name is selected by the panel: DIA, long, 4 of 4.**

## Ranking

| # | ticker | market | session | impact_sum | floor | impact_scaled | abs_move | p_up | panel_pct | panel sel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DIA | uk | bmo (inferred, 07:00 pattern) | +1.60 | no | +0.65 | 6.5 | 55 | 90 L | **yes** |
| 2 | TERNOR | se | bmo 07:30 | +1.10 | no | +0.56 | 7.0 | 54 | 67 L | |
| 3 | JEN | de | bmo (inferred) | +1.00 | no | +0.50 | 5.0 | 55 | 31 L | |
| 4 | INW | it | **amc** per hunter (18:08 pattern) | +0.40 | no | +0.14 | 3.5 | 52 | 23 L | |
| 5 | SNTIA | no | bmo 07:00 | +0.20 | no | +0.18 | 4.5 | 52 | 30 L | |
| 6 | PAH3 | de | bmo (inferred) | +0.10 | no | +0.05 | 2.3 | 51 | 12 L | |
| 7 | SHOT | se | bmo 07:30 | +0.10 | no | +0.28 | 7.0 | 52 | 14 S | |
| 8 | SJF | dk | in session (~10–11h) | +0.00 | no | −0.06 | 3.0 | 49 | 20 S | |
| 9 | UN0 | de | unsettled (baseline bmo) | +0.00 | no | +0.00 | 3.0 | 50 | 13 S | |
| 10 | BFF | it | **amc** per hunter (18:20 pattern) | −0.10 | no | +0.72 | 9.0 | 54 | 74 L | |
| 11 | BGN | it | in session (~12:30) | −0.15 | no | +0.16 | 4.0 | 52 | 24 S | |
| 12 | FF | it | in session (~13:30–14:00) | −0.20 | no | −0.75 | 7.5 | 45 | 59 S | |
| 13 | EG7 | se | bmo 07:00 | −0.30 | no | −0.60 | 10.0 | 47 | 27 S | |
| 14 | SDF | de | bmo 07:00 | −0.30 | no | −0.10 | 5.0 | 49 | 5 S | |
| 15 | BMED | it | in session (~11–12h) | −0.40 | no | +0.12 | 3.0 | 52 | 33 S | |
| 16 | ELG | de | bmo (~07:40 pattern) | −0.50 | no | −0.16 | 8.0 | 49 | 25 L | |
| 17 | A2A | it | in session / pre-open | −0.70 | no | −0.40 | 4.0 | 45 | 72 S | |
| 18 | ABDP | uk | bmo 07:00 | −0.80 | no | −0.48 | 6.0 | 46 | 67 S | |

`impact_scaled` = (2·p_up/100 − 1)·abs_move is the hunter's second measurement; it is not the key and is never pooled with it.

## The four-model panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing.** All four members ran on their pinned agents (`panel-judge-intl-*`), 18/18 packs each, no fallback. Own-top-20% thresholds: opus5 |1.20|, opus55 |0.84|, sonnet55 |0.70|, fable51 |0.90| (200 live sizes each).

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 DIA      bmo?    yes  90 long     8  opus5: 96L* opus55:100L* sonnet55: 82L* fable51: 80L*  4  +1.69
   2 BFF      bmo?         74 long    20  opus5: 74L  opus55: 42L  sonnet55: 94L* fable51: 87L*  2  +1.28
   3 ABDP     bmo?         67 short   26  opus5: 92S* opus55: 80S* sonnet55: 24S  fable51: 72S   2  -1.17
   4 A2A      bmo?         72 short   11  opus5: 80S  opus55: 82S* sonnet55: 54S  fable51: 72S   2  -1.12
   5 FF       bmo?         59 short   22  opus5: 54S  opus55: 30S  sonnet55: 60S  fable51: 92S*  1  -0.81
   6 TERNOR   bmo          67 long     4  opus5: 70L  opus55: 71L  sonnet55: 60L  fable51: 68L   0  +0.97
   7 ELG      bmo?         25 long    28  opus5: 36L  opus55: 22S  sonnet55: 33L  fable51: 52L   0  +0.48
   8 BMED     bmo?         33 short   14  opus5: 28S  opus55: 51S  sonnet55: 14S  fable51: 40S   0  -0.47
   9 SNTIA    bmo          30 long     6  opus5: 28L  opus55: 22L  sonnet55: 40L  fable51: 30L   0  +0.41
  10 EG7      bmo          27 short   18  opus5: 28S  opus55: 30S  sonnet55: 50S  fable51:  0-   0  -0.38
  11 INW      bmo?         23 long     6  opus5: 13L  opus55: 30L  sonnet55: 24L  fable51: 26L   0  +0.36
  12 JEN      bmo?         31 long    20  opus5: 13L  opus55: 62L  sonnet55: 36L  fable51: 12L   0  +0.35
  13 BGN      bmo?         24 short   12  opus5: 22S  opus55: 42S  sonnet55: 22S  fable51: 10S   0  -0.31
  14 SJF      bmo?         20 short    4  opus5: 26S  opus55: 22S  sonnet55: 16S  fable51: 18S   0  -0.28
  15 SHOT     bmo          14 short   20  opus5: 22S  opus55:  8S  sonnet55: 40S  fable51: 16L   0  -0.22
  16 UN0      bmo          13 short   11  opus5:  6S  opus55: 30S  sonnet55: 16S  fable51:  0-   0  -0.19
  17 SDF      bmo           5 short   30  opus5: 22L  opus55:  8L  sonnet55:  6L  fable51: 56S   0  +0.14
  18 PAH3     bmo?         12 long    12  opus5:  6L  opus55: 32L  sonnet55:  3L  fable51:  6L   0  +0.12
```

**DIA (selected, long, panel_pct 90, 4 of 4).** All four judges named the same item: Dialight's own trading statements guide H1 FY27 to a 15%+ return on sales, which implies roughly $12–13m of underlying operating profit in the half against a two-analyst, undated FY27 EBIT bar of about £13.6m (~$18m), so a further upgrade is more likely than a cut ([trading statement](https://www.investegate.co.uk/announcement/rns/dialight--dia/trading-statement/9747116)); the stock has given back the September upgrade (−8.2% over 20 days) and earlier upgrades moved it +9% to +38%. **The strongest case against:** the bar is one undated aggregator figure; the half's direction is already public (sales above the 3–5% guide, gross margin above 45%, FY27 PBT "significantly ahead"); the session is inferred from the 07:00 pattern, not a timestamp; and Hubbell's Q3 flagged heavy-industrial softness in Dialight Lighting's core market.

**Where the panel and `impact_sum` disagree most:**
- **BFF**: `impact_sum` −0.10, panel +74 long (two judges in their top 20%). The judges sized the hunter's guidance arithmetic (H1 adjusted €81.3m against a €115–140m FY guide) and sized the 10→11 Nov window, since BFF releases after the close; the hunter's write-down finding (−1.5) netted its sum to zero.
- **A2A** and **ABDP**: the hunter's two most negative names; the panel agrees on side and sizes them larger (72 and 67 short), but neither reaches 3 of 4.
- No name is above the floor, so there is no floor-clearer the panel declined.

**What the numbers are not.** `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing; the members' scales are still largely the frozen E-P seed until this market has about 200 panel names of its own; and in the four-model re-judge the judges ranked Europe better than the live hunt, which does not establish anything about this market's panel. The EU panel has no measured edge yet (2026-10-21: ρ +0.22, p 0.19 on 45 names).

## Top and bottom name

- **Top, DIA +1.60**: driven by the guidance finding (+1.5) above — [Investegate RNS](https://www.investegate.co.uk/announcement/rns/dialight--dia/trading-statement/9747116).
- **Bottom, ABDP −0.80**: driven by the company's own numbers implying H2 FY26 order intake of about £26m against about £44m a year earlier, ahead of the first FY27 outlook (−1.2) — [pre-close trading update](https://www.investegate.co.uk/announcement/rns/ab-dynamics--abdp/pre-close-trading-update/9776214). The full year itself was pre-released on 17 Sep.

## Not ranked

- **BAHN_B** (se): no event. The issuer calendar on MFN and Inderes puts Q3 on **2026-11-17**; the stock is also pinned at Telenor's unconditional SEK 62 mandatory offer (Oslo Børs messageId 685864), acceptances closing 7 Dec.
- **BEAMMW_B** (se): phantom by one day. The issuer's Q2 report, its website and MFN all date the Q3 report **2026-11-11**.

Both were vendor-calendar dates (`time` assumed bmo); 2 of 20 is this day's phantom rate.

## Sessions and windows — read before resolving

- **BFF and INW release AFTER the close** (hunters' `session_check` opens `amc`, with timestamped precedents: BFF H1 at 18:20, INW Q1 at 18:08; INW's 9M 2025 moved −0.05% on the day and −11.76% the next). The sealed bmo window close(11-09)→close(11-10) holds **no release** for them; the reaction is close(11-10)→close(11-11). `eu_resolve.py` reads the session from `session_check`.
- BGN, BMED, FF, SJF and A2A release **in session**; close(D−1)→close(D) still contains the release.
- **UN0's** release time could not be read (uniper.energy blocks curl and WebFetch), so its `session_check` does not settle it; the baseline's bmo stands.
- `session_unresolved: true` was set at seal for 13 of 20 names (all marked `bmo?` above); every hunter checked the timing against the issuer's own record.

## The day, honestly described

- **Selection:** `random sample of 42 eligible, seed 'eu-2026-11-10'` — 68 scheduled, 42 above the $100k/day floor, 20 drawn at random. By market: **it 6, de 5, se 5, uk 2, dk 1, no 1**, fr/fi/es/pl 0 (eligible: uk 9, de 13, se 6, dk 2, no 3, fi 1, it 8).
- **Market concentration:** largest market Italy at 30%, six markets represented. Italy's six are mostly financials and utilities reporting into the same budget-bill tax change (IRAP/IRES surcharges named by A2A, BGN), a correlated exposure the scorer cannot see.
- **Calendar sources:** UK RNS calendar read; issuer calendars read for de/se/dk/no/fi/pl; Yahoo firm dates `unavailable` for all ten markets.
- **Options:** `null` in all ten markets. Europe runs in the anchor-less regime (`archive/backtest/FINDINGS.md` §33: ρ=+0.073, p=0.45 over 104 events).
- **Short registers:** uk, de, se, dk, no, it read; **4 of 20 names carry `anchor_covered: true`** (ABDP 0.55%, BFF 4.33%, SDF 4.04%, SHOT 2.69%). Every other register zero is a truncated zero, not an anchor. Denmark's register publishes from 0.1%, not 0.5%.
- **Spain and Poland: 0 names** today. **Germany: 5 names** (ELG, JEN, PAH3, SDF, UN0), which cannot reach `event_occurred: false`. **Italy (6)** cannot either: eMarket STORAGE is not universal, and the A2A, BFF and INW hunters each found that their issuer does not file there.
- **`lean_vs_free_control_rho`** from the previous resolved run (2026-10-16): se 0.60; no other market reported. No European run after 10-16 has an `eu-resolved.json` yet.
- The lean's weights are priors borrowed from the US runs, measured nowhere in Europe.
- **`history.basis`:** observed only for ABDP and DIA (`observed_rns`) and SNTIA (`observed_newsweb`). The other 17 are **estimated cadences**: a scale, never a record of dates. Several hunters (BGN, SJF, SHOT) found the estimated reaction dates miss the real release days.
- **Conviction floor:** nothing above 2.8. Over the whole US sample the sign below the floor was a coin flip.

## Already public / likely guidance change (per name)

- **Period pre-released** (`already_public` carries the period): ABDP (17 Sep pre-close: FY revenue £91.6m, margin 20%), JEN (21 Oct ad-hoc: 9M revenue >€800m, EBITDA ~€180m, margin guide raised to ~22%; +12.1% that day), UN0 (4 Nov ad-hoc: 9M adj. EBITDA €1,024m, NI guide raised; 6 Nov dividend policy), SJF (12 Oct FY PBT guide raised to DKK 825–900m), PAH3 (18 Sep guide cut; VW Q3 published 29 Oct), DIA (outline of the half in the 22 Jul and 1 Sep updates), BMED and BGN (monthly inflows).
- **Not pre-released, guidance line live** (`new_in_release`): ELG (FY consensus at the top of the 12% ±2pp guide, no ad-hoc raise), TERNOR (revenue guide easy, 3.9% margin guide needs ~5% in H2), A2A (a possible first 2027 guide against the IRAP surcharge; the Nov 2025 first guide closed −9.3%), ABDP (first FY27 outlook), SHOT (first Dalata pro forma), EG7 (first disclosure on Aliens: Fireteam Elite 2 sales and the ~SEK 385m asset), SDF (likely FY range narrowing), FF, BFF.
- On the first resolved days these two facts decided the size of the move (3.1% against 7.4%, and 9.0% against 2.3%) while the emitted sizes barely differed; compare the `abs_move` column against them when this day resolves.

## Language notes worth quoting

- **BFF** (it): only the Italian press (MF) carried the exact Cerberus terms (€180m for 30%, then up to €220m in a rights issue) and the Bank of Italy's €2.7bn loan reclassification; English coverage had a vaguer €300–400m.
- **TERNOR** (se): the Swedish-only Q3 report of state-owned peer Svevia: «Störst ökning återfanns inom division Drift till följd av ökade volymer i befintliga kontrakt» (the largest order-intake increase came in road maintenance, from higher volumes in existing contracts).
- **SNTIA** (no), **SHOT** (se), **EG7** (se), **BEAMMW_B** (se): bilingual issuers; the local-language sources added nothing on the filings, as expected for the Nordics.
- **ELG** (de): the confirmed date came only from the German Finanzkalender; one German aggregator carried a wrong 9 Nov date.

## IBKR handoff (step 6b)

`ibkr-handoff.json` written after the note; no broker call from this session, and `execution_eu.enabled` is false, so the executor places nothing. Offline plan under the rule panel_pct >= 70 with all four judges: **BUY BFF** (74.4, 2,520 @ 1.984 EUR, 50%), **SELL A2A** (72.0, 2,057 @ 2.43 EUR, 50%). DIA, the panel's one selection, is not taken: turnover $0.14m is below the executor's $0.20m floor. BFF's release is after the close (see Sessions), so a position entered on 11-09 would hold through 11-10 before the print.

## Housekeeping

- A hunter reported that `eu_archive.day('it', d)` raises `fromisoformat: argument must be str` when given a `datetime.date`; it works with an ISO string. Not fixed in this run.
- **Resolve:** `eu_resolve.py --run research/2026/11/2026-11-10/europe` after Yahoo's bars catch up (one session for `.L`, about two for `.DE`/`.MI`). Resolve the Swedish, Danish and Norwegian rows **within about a week**, because the Nasdaq Nordic feed pages back only ~12 days. Then `market_panel.py resolve --market EU`.

**One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
