# Ochtendadvies 2026-11-05 — stage M

Bron: `research/2026/11/2026-11-04/edge-panel` (stage E-P). Regel: panel_pct >= 60, >= 3 judges, print in this morning's window (amc 2026-11-04 or bmo 2026-11-05); top 10 by panel_pct. Positie = de kant van het panel, instap 13:30 ET op de instapdag. **Er worden geen orders geplaatst.**

Markt premarket: SPY -0.06%, QQQ -1.14%, IWM +0.14%

| Naam | Sessie | Positie | panel_pct | Cijfers wijzen op | Premarket vs slot | Positie tot nu | Voorbeurs stil | Verwacht open | Verwacht 10:00 | Verwacht open→slot | **Advies** | Limiet | Vaste regel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U | bmo | long | 93.4* | +20.00% | +18.36% | +19.81% | nee | +18.00% | +17.00% | +1.00% | **Wachten tot slot** | — | Uit om 13:00 ET |
| CAVA | amc | short | 85.4* | -6.00% | -10.37% | +12.09% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| BYND | amc | short | 81.6* | -6.00% | -4.34% | +8.21% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| ROOT | amc | short | 79.4 | -3.00% | -13.72% | +10.64% | ja | -12.00% | -11.00% | +1.50% | **Verkopen bij opening** | — | Verkopen bij opening |
| FSLY | amc | long | 77.2 | +9.00% | -15.86% | -16.74% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| ELF | amc | short | 72.8 | +6.00% | +4.00% | +0.24% | ja | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| CORZ | bmo | long | 65.0 | +5.00% | +0.31% | +1.64% | nee | +0.50% | +1.00% | +1.00% | **Limietorder** | 13.30 | Uit om 13:00 ET |

`*` = door het panel geselecteerd (top 20%). Premarket = de mediaan van de laatste vijf voorbeurstransacties om 09:24. *Cijfers wijzen op* = de beweging van slot tot slot die de analist op grond van alleen het cijferbericht verwacht, vastgelegd voordat hij de koers zag. Rendementen in % vanaf de kant van de positie; verwachtingen zijn ten opzichte van het slot van gisteren.

## U — Wachten tot slot

Voorlopig: de cijfers bevestigen de these ruim; houden tot het slot.

*Wat dit advies verandert:* Een voorbeurskoers die al ver boven de 20% stijging staat.

## CAVA — Geen advies

Voorlopig: statische regel (amc op de opening).

*Wat dit advies verandert:* Nog niet beoordeeld.

Niet bruikbaar: expected.open_pct_vs_prev_close missing; expected.open_to_close_pct missing; expected.px_1000_pct_vs_prev_close missing; expected.p_open_lags missing or outside 0-100; expected.p_fade_by_1000 missing or outside 0-100

## BYND — Geen advies

Niet bruikbaar: action None is not one of ('exit_open', 'exit_1000', 'exit_limit', 'exit_close', 'none')

## ROOT — Verkopen bij opening

De short staat voorbeurs al ruim 10% in de plus: het aandeel noteert rond 13,7% lager, veel meer dan de cijfers volgens ons rechtvaardigen (winst ruim boven verwachting, groei zwak maar in lijn met de eigen prognose, plus inkoop van eigen aandelen). Grote dalingen na cijfers die 's nachts al verwerkt zijn, veren vaak deels terug, dus dek de short in bij de opening, zoals de standaardregel ook doet.

*Wat dit advies verandert:* Als de voorbeurs vlak voor 09:30 actief verder zakt onder 49 dollar met meerdere nieuwe transacties, of er komen koersdoelverlagingen binnen, dan is vasthouden tot 10:00 te verdedigen.

## FSLY — Geen advies

Voorlopig: amc-naam, standaardregel (verkopen bij de opening).

*Wat dit advies verandert:* Nog niet beoordeeld.

Niet bruikbaar: expected.open_pct_vs_prev_close missing; expected.open_to_close_pct missing; expected.px_1000_pct_vs_prev_close missing; expected.p_open_lags missing or outside 0-100; expected.p_fade_by_1000 missing or outside 0-100

## ELF — Geen advies

Niet bruikbaar: action None is not one of ('exit_open', 'exit_1000', 'exit_limit', 'exit_close', 'none')

## CORZ — Limietorder

De cijfers zijn duidelijk beter dan verwacht (omzet ongeveer 17% boven de raming), maar de koers staat voor de opening vrijwel vlak nadat hij eerst tot 13,60 opliep. Leg een verkooplimiet op 13,30: haalt de koers dat vandaag, dan nemen we de winst; zo niet, dan gaat de positie aan het slot weg, omdat een ochtendcijfer vaak de hele dag doorwerkt.

*Wat dit advies verandert:* Zakt de voorbeurskoers voor 09:30 onder 12,50 (het voorbeurslaagste) of komt er nieuws dat het gesprek negatief was over Texas of CoreWeave, verkoop dan op de opening.

## Niet meegenomen

- LMND: panel_pct 52.0 below 60
- RUN: panel_pct 49.9 below 60
- CHYM: panel_pct 49.8 below 60
- PTON: panel_pct 45.6 below 60
- CELH: panel_pct 45.4 below 60
- SEZL: panel_pct 44.0 below 60
- OSCR: panel_pct 37.4 below 60
- WOLF: panel_pct 24.6 below 60
- LEU: panel_pct 22.6 below 60
- JOBY: panel_pct 21.4 below 60
- EOSE: panel_pct 8.4 below 60
- FIG: panel_pct 8.4 below 60
- NVAX: panel_pct 4.1 below 60

## Hoe dit te lezen

Elk advies wordt na het slot gescoord tegen de vaste regel (amc uit bij opening, bmo uit om 13:00 ET) op dezelfde namen (`morning.py resolve`, `pool`). Eén ochtend is een anekdote: pas over veel ochtenden blijkt of de beoordeling iets toevoegt aan de vaste regel.

*Voorbeurs stil* = de laatste voorbeurstransactie ligt 31 minuten of meer voor de opening, of er waren minder dan zes 5-minutenbars. Gemeten over 231 earnings-events houdt de opening meestal de hele voorbeursbeweging vast en zakt de koers daarna tot 10:00 terug; bij een stille voorbeurs is de opening onbetrouwbaar en is de richting daarna onzeker (`researcher_us/analysis/open-lag.md`).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
