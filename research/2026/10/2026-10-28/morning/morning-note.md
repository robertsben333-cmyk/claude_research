# Ochtendadvies 2026-10-28 — stage M

Bron: `research/2026/10/2026-10-27/edge-panel` (stage E-P). Regel: panel_pct >= 60, >= 3 judges, print in this morning's window (amc 2026-10-27 or bmo 2026-10-28); top 10 by panel_pct. Positie = de kant van het panel, instap 13:30 ET op de instapdag. **Er worden geen orders geplaatst.**

Markt premarket: SPY +0.24%, QQQ +0.37%, IWM +0.14%

| Naam | Sessie | Positie | panel_pct | Cijfers wijzen op | Premarket vs slot | Positie tot nu | Voorbeurs stil | Verwacht open | Verwacht 10:00 | Verwacht open→slot | **Advies** | Limiet | Vaste regel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BOOM | amc | long | 95.8* | —% | +21.31% | +21.27% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| OI | amc | short | 94.2* | —% | -8.87% | +6.62% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| RBBN | amc | short | 90.4* | —% | +6.48% | -9.49% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| ENPH | amc | short | 85.6* | —% | -21.84% | +27.29% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| LUNG | amc | short | 85.0* | —% | +14.67% | -13.65% | nee | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| KIDS | amc | long | 83.7* | —% | +0.08% | -1.08% | ja | —% | —% | —% | **Geen advies** | — | Verkopen bij opening |
| AMRN | bmo | short | 70.7 | —% | +1.25% | -0.75% | ja | —% | —% | —% | **Geen advies** | — | Uit om 13:00 ET |
| JMKE | bmo | long | 61.5 | —% | +0.53% | -1.65% | nee | —% | —% | —% | **Geen advies** | — | Uit om 13:00 ET |

`*` = door het panel geselecteerd (top 20%). Premarket = de mediaan van de laatste vijf voorbeurstransacties om 09:24. *Cijfers wijzen op* = de beweging van slot tot slot die de analist op grond van alleen het cijferbericht verwacht, vastgelegd voordat hij de koers zag. Rendementen in % vanaf de kant van de positie; verwachtingen zijn ten opzichte van het slot van gisteren.

## BOOM — Geen advies

Niet bruikbaar: review missing

## OI — Geen advies

Niet bruikbaar: review missing

## RBBN — Geen advies

Niet bruikbaar: review missing

## ENPH — Geen advies

Niet bruikbaar: review missing

## LUNG — Geen advies

Niet bruikbaar: review missing

## KIDS — Geen advies

Niet bruikbaar: review missing

## AMRN — Geen advies

Niet bruikbaar: review missing

## JMKE — Geen advies

Niet bruikbaar: review missing

## Niet meegenomen

- DMC: panel_pct 54.6 below 60
- OPFI: panel_pct 54.2 below 60
- OTLY: panel_pct 53.1 below 60
- UCTT: panel_pct 49.8 below 60
- FSP: panel_pct 47.7 below 60
- BRSP: panel_pct 32.5 below 60
- INTA: panel_pct 27.8 below 60
- SEVN: panel_pct 22.8 below 60
- LU: panel_pct 16.2 below 60
- SLDE: panel_pct 10.1 below 60
- REPL: panel_pct 2.3 below 60
- BBNX: panel_pct 0.1 below 60

## Hoe dit te lezen

Elk advies wordt na het slot gescoord tegen de vaste regel (amc uit bij opening, bmo uit om 13:00 ET) op dezelfde namen (`morning.py resolve`, `pool`). Eén ochtend is een anekdote: pas over veel ochtenden blijkt of de beoordeling iets toevoegt aan de vaste regel.

*Voorbeurs stil* = de laatste voorbeurstransactie ligt 31 minuten of meer voor de opening, of er waren minder dan zes 5-minutenbars. Gemeten over 231 earnings-events houdt de opening meestal de hele voorbeursbeweging vast en zakt de koers daarna tot 10:00 terug; bij een stille voorbeurs is de opening onbetrouwbaar en is de richting daarna onzeker (`researcher_us/analysis/open-lag.md`).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
