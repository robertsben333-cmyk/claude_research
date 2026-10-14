# Het panel in procenten: betalen de hoogste scores? (oktober, per regio)

**Vraag (operator, 2026-10-14).** Laat de 3-van-4-regel voor deze lezing los en stel de
vaste vraag: als we elke naam boven een drempel handelen, wat levert dat op en hoeveel
namen zijn dat? Werk in procenten, zodat het getal direct leesbaar is en een toekomstig
model erbij kan zonder de andere te herschalen. Doe het voor elke regio.

**Methode.** `panel_mean_pct.py`. Een rechter geeft al een percentage terug:
impact_sum = (2 × p_up / 100 − 1) × abs_move_pct, de verwachte beweging met teken in
procent van de koers (`config/panel-judge.md`). Per naam wordt het gemiddelde van de vier
genomen zoals ze het geven, zonder schaling, fit of historie. Alleen oktober: de
Opus 5.5-zoektochten van september tellen niet mee. VS: stage E-P, beweging close tot
close en strategie-exit uit `dashboard/data/ledger.json`. Andere regio's: het panel dat de
marktstages sinds 2026-10-08 draaien, in het eigen venster van elke markt. Japan 10-13 en
Europa 10-12 zijn voor deze analyse opgelost en staan in `resolved/`, niet in de dagmap.
`build_chart.py` maakt `panel-mean-pct.html`, met een tab per regio.

**Waarom niet per model omgerekend.** De voor de hand liggende kalibratie (de beweging die
een model verwacht naast de werkelijke) verandert niets: alle vier schatten de beweging
even groot in (VS mediaan 7 tot 8%, Japan 3,5 tot 4,5%). Het verschil tussen de modellen
zit in `p_up`, hoe zeker ze zijn: Opus 5 is twee keer zo zeker als Sonnet 5.5. Een
omrekening die dat gelijktrekt heeft het teken van de uitkomst nodig (κ, gerealiseerde
beweging per gesteld procentpunt). Die staat per model in de JSON en op de pagina, maar
wordt nergens voor gebruikt: op 35 en 50 namen is hij ruis. Hij ligt nu voor bijna elk
model tussen 1,5 en 2,1, dus de modellen zijn in procenten eerder te voorzichtig dan te
stellig.

**Resultaat.**

| drempel \|gem.\| | VS namen | VS rendement | Japan namen | Japan rendement |
|---|---|---|---|---|
| 0% (alles) | 35 | +2.04% (se 1.23) | 50 | +1.99% (se 1.09) |
| 0,5% | 23 | +3.38% (se 1.45) | 24 | +2.89% (se 1.42) |
| 1,0% | 11 | +3.33% (se 2.49) | 12 | +1.32% (se 2.02) |
| 1,5% | 7 | +4.73% (se 2.39) | 6 | +4.37% (se 3.01) |
| 2,0% | 4 | +5.69% (se 4.03) | 5 | +1.96% (se 2.22) |

Alles shorten zonder onderzoek: VS +1.17%, Japan −0.38%. Europa, Australië en Canada
hebben nog geen opgeloste panelnaam (Europa 1, Canada 0).

**Wat het niet laat zien.** De VS zijn zes dagen, Japan twee. Boven 1% rust elk punt op
twaalf namen of minder en valt de band over de lijn van alles shorten. De curve is over
alle drempels gelezen, dus het beste punt is het optimistische. Bruto, zonder kosten.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
  python3 research/analyses/panel-mean-pct/build_chart.py
