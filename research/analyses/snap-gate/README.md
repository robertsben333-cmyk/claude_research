# Snap als poort over de vier rechters (2026-10-14)

**Vraag (operator, 2026-10-14).** Andere opzet dan `../snap-juror-backtest/`: SubQ Snap krijgt
de rapporten van de vier panelrechters en beslist ja of nee: is het verwachte rendement van
deze trade boven 3%?

**Antwoord: als ja/nee-poort voegt het niets toe, en het kost geld.** Snap zegt op 20 van 153
namen ja, en 18 daarvan zitten al in de top 20% van het panel. De zes topnamen die Snap
afwijst, leveren samen +13,1% per naam op (5 van 6 goed, met VRA +36%, WOOF +20% en APOG
+16%). Bij een gelijk aantal namen is het gelijkspel. **Wel een spoor:** de kans die Snap
geeft, gebruikt als doorlopende score, rangschikt de dag minstens zo goed als het
panelpercentiel, en in oktober beter. Maar de lekcontrole rangschikt oktober ook, dus dat
spoor is op deze steekproef niet te lezen.

## Opzet

`snap_gate.py`. Dezelfde 153 VS-namen als de vorige analyse (één naam valt af omdat het
panel er geen kant koos). Snap krijgt per naam:

- de vier rapporten, als `judge_1` tot `judge_4`, zonder modelnamen;
- een minimale baseline: datum, sessie, implied move, mediane eerdere reactie, aanloop
  over 20 dagen;
- de kant van de trade, vooraf vastgelegd: de kant van het gemiddelde percentiel van de
  vier rechters, zoals in de live E-P-regel.

Eén vraag (ja/nee): is het verwachte rendement van die trade over het venster, bruto,
boven 3% van de instapprijs? Ja betekent P(ja) > 0,5.

**Wat "de rapporten" zijn, verschilt per steekproef.** In de backtest (aug/sep) schreven de
rechters alleen hun drie getallen weg (`abs_move_pct`, `p_up`, `impact_sum`); bij 38 namen
schreef minstens één rechter ook een toelichting. In oktober bevat elk rapport de
bevindingen met de gebruikte bewijsstukken en een toelichting.

Drie armen: `gate` (de opzet onder test), `gate_pct` (plus het percentiel van elke rechter in
de eigen verdeling, verkennend) en `gate_bare` (lekcontrole: alleen ticker, naam, datum,
sessie en kant). De toetsen staan in de docstring en zijn vastgelegd vóór de eerste call.

## Resultaat, samen (instap 19:30 CET, op de kant van het panel)

| | namen | rendement per naam | goed |
|---|---|---|---|
| alle namen op de kant van het panel | 150 | +1,74% | 61% |
| top 20% van het panel (live regel) | 24 | **+7,18%** (se 2,9) | 79% |
| **Snap zegt ja** | 19 | **+5,09%** (se 3,1) | 79% |
| Snap zegt nee | 131 | +1,25% | 59% |
| top 20% van het panel, Snap zegt nee | 6 | +13,11% | 83% |
| gelijk aantal (20): Snap top 20 / panel top 20 | 20 / 20 | +5,73% / +5,68% | 80% / 80% |

Instap op de slotkoers geeft hetzelfde beeld (ja +4,91% tegen top 20% +6,95%).

- **Snap is als poort te streng, en dat kost.** Mediane P(ja) is 0,12. De ja-groep haalt wel
  ruim 3% (+5,1%) en de nee-groep niet (+1,25%), dus de uitspraak klopt als bewering. Maar de
  live regel doet hetzelfde met meer namen en een hoger rendement.
- **Buiten de top 20% vindt Snap vrijwel niets:** één ja-naam (+3,1%). Met de percentielen
  erbij (`gate_pct`) zes, samen +3,6%.
- **Als doorlopende score is het wel bruikbaar.** De rangcorrelatie binnen de dag van P(ja)
  met het rendement is +0,335 (p 0,0005), tegen +0,289 voor |panelpercentiel| op dezelfde
  namen. In de backtest, met alleen getallen, is het gelijk (+0,232 tegen +0,245). In oktober,
  met volledige rapporten, hoger (+0,575 tegen +0,392, 35 namen). P(ja) volgt het
  panelpercentiel sterk (rangcorrelatie 0,70).

## De lekcontrole

`gate_bare` zegt nergens ja (mediane P 0,10), maar rangschikt binnen de dag toch: +0,18 samen
(p 0,05 tot 0,07) en **+0,36 in oktober (p 0,05)**, zonder enig bewijs, alleen ticker en kant.
Op 9 namen na liggen alle namen vóór de release van Snap. De winst van Snap boven het panel in
oktober kan dus voor een deel uit de training komen; dat is hier niet te scheiden. De
conclusie over de poort staat wel: lekken kan Snap alleen bevoordelen, en de poort verliest
toch.

## Wat het niet laat zien

153 namen, 21 dagen, bruto. Oktober is 35 namen over 6 dagen. De zes afgewezen topnamen zijn
zes namen; het verschil met de ja-groep valt binnen twee standaardfouten. Snap is
deterministisch maar gevoelig voor de vorm van de request, dus dit geldt voor deze precieze
vraag.

## Wat zou het oordeel veranderen

Een toekomstgerichte steekproef na de release, met volledige rapporten, waarin P(ja) als score
het panelpercentiel binnen de dag duidelijk verslaat. Dat is de enige variant die hier iets
liet zien, en precies de variant die de lekcontrole niet vrijpleit.

## Bestanden

- `snap_gate.py`: opbouw, calls (met cache), analyse; `--analyse-only` rekent opnieuw zonder
  te bellen. Heeft `researcher_us/scripts/snap_juror.py` nodig (branch
  `claude/gallant-bohr-hzsesq`).
- `responses.jsonl`: 435 antwoorden, alle `ok`, model `subq-snap-preview`, 0,72 miljoen input
  tokens, $0,04.
- `results.json`: alle tabellen en de rijen per naam.
