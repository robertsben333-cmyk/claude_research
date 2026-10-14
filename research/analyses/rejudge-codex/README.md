# Het panel door Codex: GPT-6 Astra en GPT-5.6 Sol op dezelfde blinde packs

**Vraag (operator, 2026-10-14).** Kunnen twee OpenAI-modellen, via Codex in de ChatGPT-app,
dezelfde rol spelen als de vier Claude-rechters van stage E-P? Eerst op de packs die al
zijn opgelost, voordat er iets dagelijks draait. De Opus 5.5-zoektochten van september
tellen niet mee (`sept_opus55`, zoals overal).

**Status: klaargezet, nog niet gedraaid.** Er is nog geen uitkomst.

## Wat er in de bundel zit

`build_bundle.py` maakt `codex-panel-rejudge.zip`; `manifest.json` telt de namen.

| deel | packs | namen | definities |
|---|---|---|---|
| `A-backtest` | de vier-modellen-herbeoordeling (`../rejudge-four-models/`), gefilterd zoals de backtest in `../panel-mean-pct/` | 140: VS 119, Europa 18, Japan 3 | zoals de Claude-rechters ze lazen, commit `2a817d14` |
| `B-oktober` | de eigen packs van stage E-P, 2026-10-05 t/m 10-13 | 44, VS | `main` van vandaag |

In deel A blijven de packbestanden zoals bij de Claude-run, min de septembernamen, zodat
elke rechter dezelfde buren ziet. In de bundel zit geen enkele uitkomst: geen `key.json`,
geen ledger, geen opgelost bestand, geen uitspraak van een andere rechter. Gecontroleerd
op velden als `move`, `impact_sum` en `p_up` in de packs: geen treffers.

## Hoe het draait

1. Pak de zip uit in een **lege map buiten deze repository** en open die map als project in
   Codex. Niet de GitHub-repo zelf: daar staan de uitkomsten één bestand verderop.
2. Zet webzoeken en netwerk uit voor de taken.
3. Eén nieuwe taak per packbestand per model, met de tekst uit `PROMPT.md`: 13 packs × 2
   modellen = 26 taken. `AGENTS.md` bevat de vaste regels en wordt door Codex zelf gelezen.
4. Controleer per taak de `.meta.json`: alle namen geschreven, geen andere bestanden gelezen.
5. Zet de bestanden uit `out/` terug in `research/analyses/rejudge-codex/out/`. Het scoren
   (zelfde methode als `../panel-mean-pct/` en `../rejudge-four-models/score_full.py`)
   wordt gebouwd zodra die er zijn.

## Wat het al niet kan laten zien

- **Trainingsdata.** De gebeurtenissen lopen van 2026-08-31 tot 2026-10-13. Een model met
  een latere trainingsgrens kan uitkomsten kennen. Daarom vraagt de prompt elk model zijn
  eigen grens, en wordt bij het scoren gekeken of de geanonimiseerde namen (`anon/`) slechter
  scoren dan de benoemde. Bij de Claude-rechters scoorden de geanonimiseerde juist het best.
- **Model-ID's.** De namen `gpt-6-astra` en `gpt-5.6-sol` komen uit berichtgeving van derden.
  De `.meta.json` legt vast wat de modelkiezer echt toonde.
- **Andere omgeving.** De Claude-rechters hadden alleen Read en Write; Codex heeft een
  shell. De regels in `AGENTS.md` en de `files_read`-controle vangen dat op, maar dwingen
  het niet af.
- **Klein.** Oktober is 44 namen, waarvan een deel nog niet is opgelost. Deel A is de
  eigenlijke toets.
