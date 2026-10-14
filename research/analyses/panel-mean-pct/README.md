# Het panel per eigen top: betalen de hoogste scores? (oktober, per regio)

**Vraag (operator, 2026-10-14).** Laat de 3-van-4-regel voor deze lezing los en stel de
vaste vraag: betalen de hoogste scores, en hoeveel namen zijn dat? "Top 10%" is per model
de eigen top 10%: bij Opus 5 kan dat bij 1,8 beginnen, bij Opus 5.5 bij 0,9. Zo weegt elk
model eerlijk mee, op welke schaal het ook scoort, en kan een nieuw model erbij zonder de
andere te herschalen. Doe het voor `impact_sum` en `impact_scaled`, en voor elke regio.
VS: alleen de strategie-exit, met instap om 19:30 CET en op de slotkoers.

**Methode.** `panel_mean_pct.py`.

- Per regio en per model is de referentie elke oktobernaam die dat model in die regio
  beoordeelde, opgelost of niet; er gaat geen uitkomst in. Het percentiel van een naam is
  het aandeel van die referentie met een kleinere |score|, × 100 (score 0 telt als 0),
  met het teken van het model.
- Het panel is het gemiddelde van de vier percentielen. "Top X%" zijn de namen met een
  |gemiddelde| van 100 − X of hoger, gehandeld op het teken, gelijk gewogen, bruto. Elk
  model wordt ook los zo berekend.
- `impact_sum` zoals de rechter hem schreef; `impact_scaled` = (2 × p_up / 100 − 1) ×
  abs_move_pct, opnieuw berekend zoals `edge_score.py` dat doet. De VS-rechters moeten die
  twee gelijk houden (`config/panel-judge.md`), dus daar vallen ze vrijwel samen; in Japan
  verschillen ze.
- VS: stage E-P. Strategie-exit uit `dashboard/data/ledger.json` (`px.strategy`: amc op
  de openingsprint, bmo om 20:00 CET), vanaf twee instappen: 19:30 CET (`enpx['1330']`) en
  de slotkoers voor de cijfers (`mv_strategy`).
- Andere regio's: het panel dat de marktstages sinds 2026-10-08 draaien, in het eigen
  venster van elke markt. Daar bestaan geen strategie-exit en geen instap om 19:30. Japan
  10-13 en Europa 10-12 zijn voor deze analyse opgelost en staan in `resolved/`, niet in
  de dagmap.
- Alleen oktober: de Opus 5.5-zoektochten van september tellen niet mee.

`build_chart.py` maakt `panel-mean-pct.html`, met knoppen voor regio, score en losse
modellen.

**Resultaat, `impact_sum`.**

| top | VS namen | VS instap 19:30 | VS instap slot | Japan namen | Japan |
|---|---|---|---|---|---|
| 10% | 4 | +10.15% (4/4 goed) | +6.58% | 5 | +1.96% |
| 20% | 7 | +7.24% (6/7) | +4.92% | 8 | +1.94% |
| 30% | 11 | +5.56% | +3.80% | 14 | +1.24% |
| 50% | 17 | +5.02% | +3.97% | 21 | +2.56% |
| alles | 35 | +2.63% | +2.14% | 50 | +1.99% |

Alles shorten zonder onderzoek: VS +0.12% (19:30) en +0.53% (slot), Japan −0.38%. De
huidige 3-van-4-regel: VS 5 namen, +9.50% (19:30); Japan 4 namen, +2.17%. `impact_scaled`
geeft in de VS bijna hetzelfde (top 20%: 6 namen, +7.78%) en in Japan wat meer in de top
20% (+3.84%).

**Wat het niet laat zien.** De VS zijn zes dagen en 35 namen, Japan twee dagen. De top 10%
en 20% rusten op vier tot acht namen; de band is breed. In de VS loopt het rendement netjes
op naar de top, in Japan niet. De curve is over alle drempels gelezen, dus het beste punt
is het optimistische. De percentielen komen uit dezelfde oktobernamen en schuiven als er
dagen bijkomen. Bruto, zonder kosten.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
  python3 research/analyses/panel-mean-pct/build_chart.py
