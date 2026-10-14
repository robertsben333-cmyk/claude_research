# Het panel door Codex: GPT-6.1 Sol (en eventueel GPT-6 Astra) op dezelfde blinde packs

**Vraag (operator, 2026-10-14).** Kunnen twee OpenAI-modellen, via Codex in de ChatGPT-app,
dezelfde rol spelen als de vier Claude-rechters van stage E-P? Eerst op de packs die al
zijn opgelost, voordat er iets dagelijks draait. De Opus 5.5-zoektochten van september
tellen niet mee (`sept_opus55`, zoals overal).

**Status: klaargezet, nog niet gedraaid.** Er is nog geen uitkomst.

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
ongeldig. Het scoren (zelfde methode als `../panel-mean-pct/` en
`../rejudge-four-models/score_full.py`) wordt gebouwd zodra er uitvoer is.

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
