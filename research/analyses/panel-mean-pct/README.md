# Het panel per eigen top: betalen de hoogste scores? (oktober en backtest, per regio)

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

## Vervolg 1: de backtest van augustus en september

Dezelfde regel op de blinde herbeoordeling door de vier modellen
(`research/analyses/rejudge-four-models/`): de modellen beoordeelden zonder web het bewijs
dat de live hunters verzamelden. Zonder de Opus 5.5-zoektochten van september blijven de
Opus 5-zoektochten van 2026-08-31 tot 2026-09-22 over: VS 119 namen over 15 dagen, Europa
18, Japan 3 (te weinig). De percentielen komen uit diezelfde namen. In de herbeoordeling is
`impact_scaled` per contract gelijk aan `impact_sum`.

| top (VS, `impact_sum`) | namen | instap 19:30 | instap slot |
|---|---|---|---|
| 10% | 8 | +11.66% (8/8 goed) | +11.02% (9 namen) |
| 20% | 19 | +6.85% (79% goed) | +7.30% (20) |
| 30% | 33 | +4.64% | +4.46% (34) |
| 50% | 54 | +3.05% | +3.13% (55) |
| alles | 115 | +1.41% | +1.54% (118) |

Alles shorten: +0.32%. Het patroon van oktober komt terug: het rendement loopt op naar
de top. Kanttekeningen: het bewijs komt van de Opus 5-hunters, niet van de oktoberzoeker;
de opdracht aan de rechters wijkt licht af van `config/panel-judge.md`; 25 van de 119
namen staan in CLAUDE.md of een agentbestand en zijn geanonimiseerd beoordeeld; en de
judge lab (`../judge-lab/`) is op deze zelfde herbeoordeling ontwikkeld, dus deze data is
voor de panelaanpak niet vers.

## Vervolg 2: helpt onenigheid?

Drie manieren om onenigheid mee te wegen, op dezelfde schaal zodat "top X%" overal
|score| ≥ 100 − X blijft: `eensgezind` (alleen bij hetzelfde teken), `zwakste` (het
laagste van de vier percentielen; top 10% betekent dan dat alle vier de naam in hun eigen
top 10% zetten) en `gem_min_spreiding` (gemiddelde min de spreiding van de vier). Plus een
splitsing binnen de top: de helft met de minste spreiding tegen de helft met de meeste.

- **Op gelijk aantal namen wint geen variant consistent.** Backtest VS, instap 19:30, de
  beste 10 namen: gemiddelde +10.30%, zwakste +6.75%; de beste 20: gemiddelde +6.71%,
  zwakste +8.34%. Oktober VS: alle vier vrijwel gelijk. `eensgezind` is in de top gelijk
  aan het gemiddelde, want daar geven alle vier al hetzelfde teken.
- **Binnen de top doet weinig spreiding het in de VS beter, in Japan niet.** Backtest VS
  top 30%: +7.03% tegen +2.11% (t 1.0); top 50%: +5.34% tegen +0.75% (t 1.3). Oktober VS
  top 20%: +10.15% tegen +3.36% (t 1.7). Japan oktober top 50%: +0.16% tegen +5.19%
  (t −1.6). Nergens twee standaardfouten.

Conclusie: onenigheid als poort of straf toevoegen helpt niet aantoonbaar. Leg de
spreiding vast als variabele, met de voorspelling vooraf (minder spreiding is beter), en
meet die vooruit.

## Vervolg 3: van percentiel naar verwacht rendement per trade

`expected_return.py`. De drempelcurve is geen verwacht rendement: "top 20%: +7%" is het
gemiddelde van alles op of boven 80, dus een naam op precies 80 verdient minder en een
naam op 98 meer. Per naam is nodig E[kant × beweging | |panel_pct|]. Model: kernelregressie
op |panel_pct| (bandbreedte 12 punten), gekrompen naar nul met een prior van 8 namen,
monotoon gemaakt (hoger percentiel nooit lager verwacht), en een bootstrap over hele dagen
voor een 80%-interval. Steekproef: 148 opgeloste VS-panelnamen (115 backtest, 33 oktober)
op het venster van het scorebord (13:30 ET in; amc uit op de volgende opening, bmo om
13:00 ET). Buiten de steekproef getoetst: gefit op de backtest voorspelt het oktober met
correlatie +0,32 en helling 1,66; het is dus eerder te voorzichtig dan te stellig.

| \|panel_pct\| | verwacht per trade | 80%-interval |
|---|---|---|
| 0 tot 50 | +0.29% | ongeveer −0.6 tot +0.9 |
| 60 | +0.82% | −0.09 tot +2.27 |
| 70 | +1.55% | +0.26 tot +3.16 |
| 80 | +2.61% | +0.69 tot +4.52 |
| 90 | +4.10% | +2.03 tot +6.09 |
| 100 | +5.11% | +3.41 tot +6.74 |

Bruto, zonder kosten. Japan en de andere markten hebben te weinig opgeloste namen om zo'n
curve te schatten.

**Live gezet via `researcher_us/scripts/panel_calibrate.py` (zelfde dag).** Precies deze
curve, één verwacht rendement per percentiel, met een 80%-band uit een bootstrap over
hele dagen en de trefkans per percentiel. Een variant die per naam ook de verwachte
bewegingsgrootte meenam, is gebouwd en op instructie van de operator dezelfde dag
teruggedraaid: het percentiel leidt. Hij staat per naam in de panel-output en op het
scorebord (tab "Panel %"). `expected-return-<dag>.json` bevat de curve en de namen van die dag.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
  python3 research/analyses/panel-mean-pct/build_chart.py
  python3 research/analyses/panel-mean-pct/expected_return.py --day <YYYY-MM-DD>
