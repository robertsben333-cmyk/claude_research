# Ochtendadvies 2026-11-12 — stage M

Bron: `research/2026/11/2026-11-11/edge-panel` (stage E-P). Regel: panel_pct >= 60, >= 3 judges, print in this morning's window (amc 2026-11-11 or bmo 2026-11-12); top 10 by panel_pct. Positie = de kant van het panel, instap 13:30 ET op de instapdag. **Er worden geen orders geplaatst.**

Markt premarket: SPY -0.71%, QQQ -1.43%, IWM -0.41%

| Naam | Sessie | Positie | panel_pct | Cijfers wijzen op | Premarket vs slot | Positie tot nu | Voorbeurs stil | Verwacht open | Verwacht 10:00 | Verwacht open→slot | **Advies** | Limiet | Vaste regel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CURI | amc | short | 93.6* | +12.00% | +18.07% | -18.75% | nee | +17.00% | +14.50% | -3.00% | **Verkopen om 10:00** | — | Verkopen bij opening |
| CTVA | amc | short | 87.2* | -10.00% | -13.10% | +11.68% | nee | -13.00% | -12.30% | +1.00% | **Verkopen bij opening** | — | Verkopen bij opening |
| CAE | amc | short | 74.0 | +4.00% | +2.87% | -3.84% | ja | +3.20% | +3.00% | +0.30% | **Verkopen bij opening** | — | Verkopen bij opening |

`*` = door het panel geselecteerd (top 20%). Premarket = de mediaan van de laatste vijf voorbeurstransacties om 09:24. *Cijfers wijzen op* = de beweging van slot tot slot die de analist op grond van alleen het cijferbericht verwacht, vastgelegd voordat hij de koers zag. Rendementen in % vanaf de kant van de positie; verwachtingen zijn ten opzichte van het slot van gisteren.

## CURI — Verkopen om 10:00

De cijfers spreken de short-these tegen (omzet en licenties boven verwachting, jaarprognose omhoog, dividend behouden), dus deze positie moet vandaag dicht. De koers staat voorbeurs ruim 18% hoger, meer dan de cijfers rechtvaardigen gezien de lagere brutomarge en de dunne kaspositie; zo'n grote sprong zakt in het eerste half uur vaak wat terug, dus dekken om 10:00 in plaats van bij de opening.

*Wat dit advies verandert:* Als de voorbeurskoers voor 09:30 verder oploopt boven $2,85 (de voorbeurshoogste) of er een koersdoelverhoging of positief verslag van de call verschijnt, dan direct bij de opening dekken.

## CTVA — Verkopen bij opening

De cijfers bevestigen de short-these duidelijk (omzet en winst onder verwachting, jaarprognose fors verlaagd), maar de voorbeurs staat al ongeveer 13% lager, meer dan de cijfers en de optieprijzen rechtvaardigen. Grote koersgaten na cijfers van de avond ervoor geven vaak een deel terug, en om 10:30 volgt de conference call, dus de winst van ruim 12% bij de opening nemen.

*Wat dit advies verandert:* Als de voorbeurs voor 09:30 verder wegzakt onder 10,50 met veel transacties en er nog koersdoelverlagingen binnenkomen, dan is vasthouden tot 10:00 te verdedigen.

## CAE — Verkopen bij opening

De cijfers spreken de short tegen: hogere winst dan verwacht en een verhoogde jaarverwachting, terwijl de koers voorbeurs (+2,9%) nog minder is gestegen dan de cijfers rechtvaardigen. Er is geen goede reden om langer tegen deze stijging in te blijven zitten; dek de short bij de opening, gelijk aan de standaardregel.

*Wat dit advies verandert:* Als de voorbeurskoers voor 09:30 terugzakt naar het slot van gisteren (rond 27,4) of als er negatieve signalen uit de call van 08:00 komen, kan wachten tot 10:00 beter zijn.

## Niet meegenomen

- NBIS: panel_pct 52.6 below 60
- TTEK: panel_pct 47.1 below 60
- CINT: panel_pct 37.8 below 60
- ITRG: panel_pct 36.6 below 60
- LUNR: panel_pct 36.5 below 60
- DGII: panel_pct 36.0 below 60
- AVEX: panel_pct 31.1 below 60
- YETI: panel_pct 30.0 below 60
- ALVO: panel_pct 26.0 below 60
- EZPW: panel_pct 16.9 below 60
- XNDU: panel_pct 14.4 below 60
- ASND: panel_pct 13.2 below 60
- AGBK: panel_pct 10.6 below 60
- DDI: panel_pct 4.8 below 60
- VYLR: panel_pct 4.5 below 60
- ENS: panel_pct 0.4 below 60
- ACOG: panel_pct 0.2 below 60

## Hoe dit te lezen

Elk advies wordt na het slot gescoord tegen de vaste regel (amc uit bij opening, bmo uit om 13:00 ET) op dezelfde namen (`morning.py resolve`, `pool`). Eén ochtend is een anekdote: pas over veel ochtenden blijkt of de beoordeling iets toevoegt aan de vaste regel.

*Voorbeurs stil* = de laatste voorbeurstransactie ligt 31 minuten of meer voor de opening, of er waren minder dan zes 5-minutenbars. Gemeten over 231 earnings-events houdt de opening meestal de hele voorbeursbeweging vast en zakt de koers daarna tot 10:00 terug; bij een stille voorbeurs is de opening onbetrouwbaar en is de richting daarna onzeker (`researcher_us/analysis/open-lag.md`).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
