# Ochtendadvies 2026-10-26 — stage M

Bron: `research/2026/10/2026-10-23/edge-panel` (stage E-P). Regel: panel_pct >= 60, >= 3 judges, print in this morning's window (amc 2026-10-23 or bmo 2026-10-26); top 10 by panel_pct. Positie = de kant van het panel, instap 13:30 ET op de instapdag. **Er worden geen orders geplaatst.**

Markt premarket: SPY +0.26%, QQQ +0.45%, IWM +0.12%

| Naam | Sessie | Positie | panel_pct | Cijfers wijzen op | Premarket vs slot | Positie tot nu | Voorbeurs stil | Verwacht open | Verwacht 10:00 | Verwacht open→slot | **Advies** | Limiet | Vaste regel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MED | bmo | long | 96.5* | +14.00% | +5.95% | +6.85% | nee | +6.50% | +7.50% | +4.00% | **Wachten tot slot** | — | Uit om 13:00 ET |
| BMRC | bmo | long | 66.3 | +3.00% | —% | —% | ja | +2.00% | +2.30% | +1.00% | **Limietorder** | 28.05 | Uit om 13:00 ET |
| DEA | bmo | short | 63.9 | -2.00% | —% | —% | ja | -1.00% | -1.20% | -0.80% | **Wachten tot slot** | — | Uit om 13:00 ET |

`*` = door het panel geselecteerd (top 20%). Premarket = de mediaan van de laatste vijf voorbeurstransacties om 09:24. *Cijfers wijzen op* = de beweging van slot tot slot die de analist op grond van alleen het cijferbericht verwacht, vastgelegd voordat hij de koers zag. Rendementen in % vanaf de kant van de positie; verwachtingen zijn ten opzichte van het slot van gisteren.

## MED — Wachten tot slot

De cijfers bevestigen de koopreden duidelijk: het verlies per aandeel was veel kleiner dan verwacht en het bedrijf verwacht in het vierde kwartaal winst. De koers staat voorbeurs pas zo'n 6% hoger, terwijl de vorige twee vergelijkbare meevallers 22% en 34% opleverden; bij een ochtendcijfer loopt de herprijzing vaak de hele dag door. Daarom de positie aanhouden en pas bij het slot verkopen.

*Wat dit advies verandert:* Als de voorbeurskoers voor 09:30 terugzakt naar onder ongeveer 12,00 (de winst van vanochtend grotendeels weg), dan liever bij de opening verkopen.

## BMRC — Limietorder

De cijfers bevestigen de long: winst per aandeel $0,62 tegen $0,57 verwacht, en de rentemarge (3,48%) is hoger dan het management in juli had beloofd. Er is nog niets voorbeurs gehandeld, dus de markt moet het nieuws nog verwerken, en bij een kleine bank gaat dat meestal de hele dag door. Zet daarom een verkooplimiet op $28,05 (ongeveer +3,5%). Wordt die niet geraakt, dan gaat de positie eruit bij de slotkoers. De conference call om 11:30 New Yorkse tijd is het belangrijkste risico; de grotere probleemleningen kunnen daar ter sprake komen.

*Wat dit advies verandert:* Als er voor 09:30 toch voorbeurshandel verschijnt ruim boven $28 (meer dan +4%), dan verkopen bij de opening; staat de koers voorbeurs onder de slotkoers van vrijdag, dan alleen tot 10:00 houden.

## DEA — Wachten tot slot

Er is voor de opening nog niets gehandeld, dus de koers bevat het cijfer nog niet; de prognose voor 2027 ligt onder het eigen groeidoel van het bedrijf, wat de short steunt. Bij een ochtendcijfer loopt de reactie vaak de hele dag door, en de toelichting om 11:00 kan de zwakke groei nog benadrukken; daarom aanhouden tot het slot in plaats van al bij de opening te dekken.

*Wat dit advies verandert:* Als er voor 09:30 toch handel op of boven het slot van vrijdag (22,67) verschijnt of een analist het cijfer positief ontvangt, dan liever bij de opening dekken.

## Niet meegenomen

- ARLP: panel_pct 55.2 below 60
- ABOS: panel_pct 49.1 below 60
- BOH: panel_pct 38.6 below 60
- RCBC: panel_pct 36.1 below 60
- BFST: panel_pct 34.0 below 60
- CX: panel_pct 30.8 below 60
- VZ: panel_pct 28.9 below 60
- MMYT: panel_pct 25.1 below 60
- HBT: panel_pct 18.9 below 60

## Hoe dit te lezen

Elk advies wordt na het slot gescoord tegen de vaste regel (amc uit bij opening, bmo uit om 13:00 ET) op dezelfde namen (`morning.py resolve`, `pool`). Eén ochtend is een anekdote: pas over veel ochtenden blijkt of de beoordeling iets toevoegt aan de vaste regel.

*Voorbeurs stil* = de laatste voorbeurstransactie ligt 31 minuten of meer voor de opening, of er waren minder dan zes 5-minutenbars. Gemeten over 231 earnings-events houdt de opening meestal de hele voorbeursbeweging vast en zakt de koers daarna tot 10:00 terug; bij een stille voorbeurs is de opening onbetrouwbaar en is de richting daarna onzeker (`researcher_us/analysis/open-lag.md`).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
