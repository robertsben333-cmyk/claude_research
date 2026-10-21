# Ochtendadvies 2026-10-21 — stage M

Bron: `research/2026/10/2026-10-20/edge-panel` (stage E-P). Regel: panel_pct >= 60, >= 3 judges, print in this morning's window (amc 2026-10-20 or bmo 2026-10-21); top 10 by panel_pct. Positie = de kant van het panel, instap 13:30 ET op de instapdag. **Er worden geen orders geplaatst.**

Markt premarket: SPY +0.30%, QQQ +0.62%, IWM +0.38%

| Naam | Sessie | Positie | panel_pct | Cijfers wijzen op | Premarket vs slot | Positie tot nu | Voorbeurs stil | Verwacht open | Verwacht 10:00 | Verwacht open→slot | **Advies** | Limiet | Vaste regel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NP | amc | long | 83.2* | +6.00% | —% | —% | ja | +2.50% | +2.50% | +0.50% | **Limietorder** | 30.40 | Verkopen bij opening |
| WFRD | amc | long | 80.8* | +1.00% | —% | —% | ja | +4.50% | +3.50% | -1.00% | **Verkopen bij opening** | — | Verkopen bij opening |
| ALK | amc | short | 75.2 | -5.00% | -1.05% | +1.25% | nee | -1.00% | -1.00% | +0.30% | **Verkopen bij opening** | — | Verkopen bij opening |
| MCB | amc | long | 63.7 | +4.00% | +3.51% | +4.45% | ja | +3.20% | +2.60% | -0.50% | **Verkopen bij opening** | — | Verkopen bij opening |

`*` = door het panel geselecteerd (top 20%). Premarket = de mediaan van de laatste vijf voorbeurstransacties om 09:24. *Cijfers wijzen op* = de beweging van slot tot slot die de analist op grond van alleen het cijferbericht verwacht, vastgelegd voordat hij de koers zag. Rendementen in % vanaf de kant van de positie; verwachtingen zijn ten opzichte van het slot van gisteren.

## NP — Limietorder

De cijfers zijn duidelijk goed (omzet ongeveer 8% boven verwachting, jaarprognose verhoogd), maar er is voorbeurs nog niets gehandeld, dus de koers bij de opening is onzeker. Zet een verkooporder met limiet op $30,40 (ruim 3% boven gisteren); wordt die niet geraakt, dan gaat de positie bij het slot.

*Wat dit advies verandert:* Als er voor 09:30 toch voorbeurshandel verschijnt die al rond of boven $30,40 staat, dan gewoon verkopen bij de opening; staat die duidelijk onder gisteren, dan ook bij de opening eruit.

## WFRD — Verkopen bij opening

Gisteravond na de cijfers stond het aandeel ruim 6% hoger, meer dan de cijfers zelf rechtvaardigen: betere marges en kasstroom, maar het Midden-Oosten bleef vlak en de winst per aandeel is opgeblazen door een belastingmeevaller. De positie staat op winst; verkoop bij de opening (de standaardregel) en neem de kans op terugval in de sessie niet.

*Wat dit advies verandert:* Als er voor 09:30 actieve voorbeurshandel verschijnt die duidelijk boven +6% blijft en analisten koersdoelen verhogen, kan vasthouden tot het slot overwogen worden.

## ALK — Verkopen bij opening

De jaarprognose is een groot verlies door dure brandstof, maar na een hele nacht daalt het aandeel voorbeurs maar ongeveer 1%: de markt had dit grotendeels verwacht. Het gesprek met beleggers is pas om 11:30 en kan beide kanten op; dek de short bij de opening en neem de kleine winst, zoals de standaardregel.

*Wat dit advies verandert:* Als de voorbeurs voor 09:30 wegzakt onder 33,90 met doorlopende handel, is de markt de prognose alsnog aan het verwerken en is vasthouden tot het slot het overwegen waard.

## MCB — Verkopen bij opening

De cijfers bevestigen de long-these (winst per aandeel $2,58 boven de lat, rentemarge omhoog, kredietverliezen laag) en de voorbeurs staat al ongeveer waar de cijfers het rechtvaardigen (+3,5%). Bij avondcijfers geeft de koers na de opening vaak iets terug en de analistencall loopt nog tijdens de opening, dus de winst meenemen bij de opening, zoals de standaardregel.

*Wat dit advies verandert:* Als de call vóór 09:30 een duidelijke opwaartse NIM- of winstverwachting of de beloofde terugvorderingen bevestigt en de voorbeurs richting $93 of hoger loopt, dan is vasthouden tot de slotkoers te overwegen.

## Niet meegenomen

- LAD: panel_pct 58.2 below 60
- NFLX: panel_pct 56.9 below 60
- DHR: panel_pct 55.2 below 60
- PM: panel_pct 53.4 below 60
- ABT: panel_pct 52.6 below 60
- MHO: panel_pct 50.8 below 60
- WAB: panel_pct 44.8 below 60
- CB: panel_pct 28.4 below 60
- LRN: panel_pct 23.2 below 60
- COF: panel_pct 20.8 below 60
- UAL: panel_pct 19.7 below 60
- ELV: panel_pct 15.8 below 60
- OZK: panel_pct 10.0 below 60
- WGO: panel_pct 7.4 below 60
- IART: panel_pct 1.3 below 60

## Hoe dit te lezen

Elk advies wordt na het slot gescoord tegen de vaste regel (amc uit bij opening, bmo uit om 13:00 ET) op dezelfde namen (`morning.py resolve`, `pool`). Eén ochtend is een anekdote: pas over veel ochtenden blijkt of de beoordeling iets toevoegt aan de vaste regel.

*Voorbeurs stil* = de laatste voorbeurstransactie ligt 31 minuten of meer voor de opening, of er waren minder dan zes 5-minutenbars. Gemeten over 231 earnings-events houdt de opening meestal de hele voorbeursbeweging vast en zakt de koers daarna tot 10:00 terug; bij een stille voorbeurs is de opening onbetrouwbaar en is de richting daarna onzeker (`researcher_us/analysis/open-lag.md`).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
