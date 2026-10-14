# Het panel door Codex: GPT-6 Astra en GPT-6 (sol61) op dezelfde blinde packs

**Vraag (operator, 2026-10-14).** Kunnen twee OpenAI-modellen, via Codex in de ChatGPT-app,
dezelfde rol spelen als de vier Claude-rechters van stage E-P? Eerst op de packs die al
zijn opgelost, voordat er iets dagelijks draait. De Opus 5.5-zoektochten van september
tellen niet mee (`sept_opus55`, zoals overal).

**Antwoord (2026-10-14): nee, de twee GPT-modellen voegen niets toe aan het Claude-panel.**
Elk rangschikt de dag zwakker dan elk van de vier Claude-rechters, als vijfde of zesde lid
verzwakken ze de top 20% van het panel, en het deel van hun oordeel dat het panel niet al
bevat, rangschikt de verkeerde kant op. Zelfde steekproef, rendementen en toetsen als
`../snap-juror-backtest/`, dus de twee uitkomsten zijn naast elkaar te lezen.

## Resultaat

`score_codex.py` schrijft `results.json`. Steekproef: de VS-namen van `../panel-mean-pct/`,
154 namen over 21 dagen (backtest 119 namen op 15 dagen, oktober 35 op 6). Percentielen per
steekproef uit alle namen in die steekproef, zonder uitkomst. Rendement: strategie-exit,
instap 19:30 CET, bruto, gelijk gewogen. Op de slotkoers is het beeld hetzelfde.

**1. Eigen vaardigheid, samen (154 namen).**

| | rho binnen de dag (p) | top 10% | top 20% |
|---|---|---|---|
| Opus 5 | +0.263 (0.005) | +7.0% (14) | +6.1% (29) |
| Opus 5.5 | +0.177 (0.049) | +1.6% (14) | +4.8% (29) |
| Sonnet 5.5 | +0.286 (0.003) | +9.6% (14) | +8.9% (28) |
| Fable 5.1 | +0.242 (0.005) | +3.9% (14) | +3.9% (24) |
| **panel (4 Claude)** | **+0.271 (0.003)** | +9.9% (11) | **+7.3% (25), 84% goed** |
| GPT-6 Astra | +0.055 (0.31) | +5.6% (15) | +2.0% (29) |
| GPT-6 (sol61) | +0.125 (0.12) | +5.8% (14) | +3.2% (29) |
| GPT-paar (2) | +0.095 (0.19) | +4.9% (13) | +2.9% (28) |
| SubQ Snap (ter vergelijking) | +0.159 (0.066) | +3.0% (14) | +4.1% (29) |

Alles shorten: +0.28%. Per steekproef apart hetzelfde: backtest ρ +0.054 (Astra) en +0.117
(sol61) tegen +0.173 voor het panel; oktober +0.058 en +0.147 tegen +0.448. Beide GPT-modellen
zitten onder Snap, dat al te zwak was voor een plaats in het panel.

**2. Als extra lid (de eigenlijke vraag).**

| samen, instap 19:30 | rho | top 10% | top 20% | k=10 | k=20 | k=30 |
|---|---|---|---|---|---|---|
| panel (4) | +0.271 | +9.9% (11) | +7.3% (25) | +9.2% | +6.7% | +5.9% |
| 4 + Astra | +0.244 | +7.9% (10) | +6.5% (24) | +7.9% | +5.6% | +4.7% |
| 4 + sol61 | +0.256 | +9.7% (12) | +5.3% (25) | +9.2% | +5.1% | +5.4% |
| 4 + beide | +0.226 | +8.1% (9) | +4.0% (25) | +7.9% | +5.0% | +5.3% |

k is een vast aantal namen (de k grootste |gemiddelde|), zodat een ander aantal namen het
verschil niet maakt. Bij elke k en op de top 10% en 20% ligt elke combinatie met GPT gelijk
aan of onder het panel alleen, in de backtest en samen. Twee uitzonderingen: op de top 30%
liggen de combinaties samen iets hoger (+4.6 tot +4.8% tegen +4.2%), maar op minder namen
(37 tot 39 tegen 41), en bij k=30 op gelijk aantal weer lager; en in oktober winnen de
combinaties met Astra de top 20% met één wissel op vijf namen (+9.9% tegen +8.4%).

**3. Wat de wissels doen.** In de top 20% (samen) houdt het panel met beide GPT-modellen 21
van de 25 namen. De 4 die eruit vallen, brachten +16.2% per naam op (4 van 4 goed); de 4 die
erin komen −4.5% (2 van 4). Met alleen sol61: 3 eruit op +18.8%, 3 erin op +2.4%.

**4. Het onafhankelijke deel draagt niets, of het verkeerde.** De getekende percentielen van
het GPT-paar correleren 0.92 met het panelgemiddelde (oktober 0.85), de Claude-rechters
onderling 0.91 tot 0.95. Het stuk van het GPT-oordeel dat het panel niet verklaart (residu
van een kleinste-kwadratenfit op het panelgemiddelde) rangschikt binnen de dag op ρ −0.150
(p 0.92): waar GPT afwijkt van Claude, zit Claude er vaker naast dan GPT niet. In de top 20%
van het panel geven beide GPT-modellen altijd hetzelfde teken als het panel (25 van 25), dus
als poort of veto doen ze ook niets.

**5. Lekken.** sol61 noemt een trainingsgrens van 2024-06, Astra geeft er geen. Geen van
beide las iets buiten deze map (`meta.json`: alleen `input/` en `check_outputs.py`). Op de
25 geanonimiseerde namen rangschikken de GPT-modellen even goed als het panel (ρ +0.25 en
+0.20 tegen +0.21); op de 129 benoemde namen rond nul (−0.06 en 0.00 tegen +0.18). Kennis
van de uitkomst zou juist de benoemde namen bevoordelen, dus er is geen teken van lekken bij
GPT. Het gat tussen GPT en Claude zit volledig in de benoemde namen; waarom, is met 25
anonieme namen niet te zeggen.

## Wat het niet laat zien

21 dagen en 154 namen, bruto. De toppen rusten op 9 tot 29 namen met standaardfouten van
2 tot 4 punten, dus geen enkel verschil in rendement hierboven haalt twee standaardfouten.
Wat wel consistent is: op elke drempel, in beide steekproeven en bij beide instappen ligt
GPT onder Claude, en toevoegen verlaagt het panel. Europa (18 namen) en Japan (3) zijn ook
beoordeeld maar niet gescoord: te weinig om iets te lezen. De Codex-runs deden alle packs in
één context per model, de Claude-rechters één verse sessie per pack; dat kan GPT benadelen.
sol61 meldt als model "GPT-6", niet GPT-6.1 Sol zoals gepland. De oktobernamen van 10-13
zijn deels nog niet opgelost en tellen pas mee na een nieuwe ledger.

**Advies: geen GPT-model in het panel.** Wie het opnieuw wil proberen, draait het vooruit als
schaduwkolom met een verse sessie per pack, zodat het niet steeds op een steekproef wordt
beoordeeld waarop het al verloren heeft.

    python3 research/analyses/rejudge-codex/score_codex.py

## Wat er klaarstaat

`build_bundle.py` schrijft `input/` en `manifest.json`; `check_outputs.py` controleert de
uitvoer van één model en zegt wat nog moet.

| deel | packs | namen | definities |
|---|---|---|---|
| `input/A-backtest` | de vier-modellen-herbeoordeling (`../rejudge-four-models/`), gefilterd zoals de backtest in `../panel-mean-pct/` | 140: VS 119, Europa 18, Japan 3 | zoals de Claude-rechters ze lazen, commit `2a817d14` |
| `input/B-oktober` | de eigen packs van stage E-P, 2026-10-05 t/m 10-13 | 44, VS | `main` van 2026-10-14 |

In deel A blijven de packbestanden zoals bij de Claude-run, min de septembernamen, zodat
elke rechter dezelfde buren ziet. In `input/` zit geen enkele uitkomst: geen `key.json`,
geen ledger, geen opgelost bestand, geen uitspraak van een andere rechter. Gecontroleerd
op velden als `move`, `impact_sum` en `p_up` in de packs: geen treffers. De definities
staan onder `_claude/` en niet `.claude/`, zodat Claude Code ze nooit naast de live agents
oppikt; de paden in de packs zijn daarop aangepast, verder zijn de packs ongewijzigd.

## Hoe het draait

Codex krijgt de repository (operator, 2026-10-14). Eén taak per model doet alle 13 packs
achter elkaar, met de tekst uit `PROMPT.md`; een afgebroken taak gaat met dezelfde tekst
verder waar hij stopte, omdat `check_outputs.py` bijhoudt wat klaar is. Uitvoer in
`out/<model>/`. Omdat de rest van de repo de uitkomsten bevat, noemt de prompt de enige
paden die open mogen en is het taaklog de controle: één lezing daarbuiten maakt de run
ongeldig. Gescoord met `score_codex.py` (zie Resultaat).

## Wat het al niet kan laten zien

- **Trainingsdata.** De gebeurtenissen lopen van 2026-08-31 tot 2026-10-13. Een model met
  een latere trainingsgrens kan uitkomsten kennen. Daarom vraagt de prompt elk model zijn
  eigen grens, en wordt bij het scoren gekeken of de geanonimiseerde namen (`anon/`) slechter
  scoren dan de benoemde. Bij de Claude-rechters scoorden de geanonimiseerde juist het best.
- **Model-ID's.** `meta.json` legt vast welk model de taak echt draaide.
- **Andere omgeving.** De Claude-rechters hadden alleen Read en Write; Codex heeft een
  shell en de hele repository, met de uitkomsten erin. De prompt verbiedt het en het
  taaklog laat het zien, maar niets dwingt het af.
- **Eén lange taak.** De Claude-rechters kregen een verse sessie per pack; Codex doet
  alle packs in één context. Wat de ene pack kleurt, kan de volgende raken.
- **Klein.** Oktober is 44 namen, waarvan een deel nog niet is opgelost. Deel A is de
  eigenlijke toets.
