# Snap naast het panel: de volledige backtest (2026-10-14)

**Vraag (operator, 2026-10-14).** Stel SubQ Snap dezelfde vraag als de vier Claude-rechters
en draai de volledige backtest zonder de Opus 5.5-zoektochten van september. Heeft Snap
toegevoegde waarde?

**Besluit (operator, 2026-10-14): Snap wordt geen panellid**, en draait ook niet als
schaduwkolom mee. De koppeling staat op branch `claude/gallant-bohr-hzsesq` en is niet
gemerged; de E-P Routine is ongewijzigd.

**Antwoord: nee, niet aantoonbaar.** Snap rangschikt de dag zwakker dan elk van de vier
rechters (ρ +0.159 tegen +0.177 tot +0.286), en als vijfde lid verandert het de selectie nauwelijks: 80 tot 100% van de
namen in de top blijft dezelfde, en in de top 20% van het panel spreekt Snap het panel op
het teken nooit tegen (0 van 25). Het panel met Snap erbij wint op sommige drempels en
verliest op andere, binnen de ruis.

## Wat Snap nu gevraagd wordt (snap.v2)

`researcher_us/scripts/snap_juror.py` stuurt per naam de teksten die de rechters lezen:
`config/snap-judge.md` (de taaksectie van `config/panel-judge.md` woordelijk, alleen het
lezen en het uitvoerformaat aangepast), de hunter-definitie met de core erin, LESSONS en de
pack. Twee vragen, de twee maten uit de core: `abs_move_pct` (een keuze over bins van
|beweging|) en `p_up` (ja/nee). `snap_impact` = (2 x p_up / 100 − 1) x E|beweging|, precies
het `impact_sum` van de rechters. snap.v1 (de eerste live test) vroeg een verdeling van de
getekende beweging, zonder hunter-definitie.

## Steekproef en methode

`snap_backtest.py`. Dezelfde VS-namen als `../panel-mean-pct/`: de blinde herbeoordeling van
2026-08-31 tot 2026-09-22 (Opus 5-zoektochten, 119 namen, 15 dagen, 25 geanonimiseerd) en de
live E-P-panels van oktober (35 namen, 6 dagen). Snap kreeg dezelfde packs als de rechters.
Percentielen per steekproef, uit alle namen in die steekproef, zonder uitkomst. Rendement:
strategie-exit, instap 19:30 CET (`e1930`) en op de slotkoers (`e2200`), bruto. De toetsen
staan vast in de docstring van het script en zijn vastgelegd vóór de eerste call.

Drie armen, één call per naam: `v2` (de arm onder test), `v1` (ter vergelijking) en `bare`,
een lekcontrole met alleen ticker, naam, datum en sessie, zonder bewijs.

## Resultaat, samen (154 namen, 21 dagen, instap 19:30)

| | rho binnen de dag (p) | top 10% | top 20% | top 30% |
|---|---|---|---|---|
| Opus 5 | +0.263 (0.005) | +7.0% (14) | +6.1% (29) | +3.2% (45) |
| Opus 5.5 | +0.177 (0.049) | +1.6% (14) | +4.8% (29) | +3.5% (45) |
| Sonnet 5.5 | +0.286 (0.003) | +9.6% (14) | +8.9% (28) | +5.8% (42) |
| Fable 5.1 | +0.242 (0.005) | +3.9% (14) | +3.9% (24) | +5.2% (45) |
| **panel (4)** | **+0.271 (0.003)** | +9.9% (11) | **+7.3% (25)** | +4.2% (41) |
| **Snap v2** | **+0.159 (0.066)** | +3.0% (14) | **+4.1% (29)** | +3.1% (45) |
| Snap v1 | +0.195 (0.034) | +1.2% (15) | +1.3% (29) | +3.0% (44) |
| bare (lekcontrole) | +0.125 (0.134) | +3.8% (11) | +2.4% (24) | +2.2% (36) |
| **panel (4 + Snap)** | +0.258 (0.003) | +11.5% (8) | +6.8% (22) | +4.6% (40) |

Alles shorten: +0.28%. Top 20% van het panel +7.3% (se 2.8), van het panel met Snap +6.8%
(se 3.1). Per steekproef apart hetzelfde beeld: in de backtest ρ +0.123 voor Snap tegen
+0.173 voor het panel, in oktober +0.243 tegen +0.448.

**Bij een gelijk aantal namen** (de k grootste |score|), samen: k=10 +12.6% met Snap tegen
+9.2% zonder, k=15 +6.5% tegen +7.1%, k=20 +7.5% tegen +6.7%, k=30 +5.5% tegen +5.9%. Het
verschil is één of twee namen die wisselen.

**Onafhankelijk, maar het onafhankelijke deel draagt niets.** De getekende percentielen van
Snap correleren 0.84 tot 0.87 met die van de rechters, de rechters onderling 0.91 tot 0.95;
in oktober 0.53 tot 0.69 tegen 0.86 tot 0.95. Snap wijkt dus meer af dan de rechters van
elkaar, maar juist waar het afwijkt, rangschikt het slechter. Op de namen waar het panel
het zekerst is, zegt Snap hetzelfde.

**De nieuwe vraag helpt in de staart, niet in de rangorde.** v2 tegen v1: top 20% +4.1% tegen
+1.3%, ρ +0.159 tegen +0.195.

## De lekcontrole, en waarom de conclusie toch staat

Op 9 namen na (2026-10-12) ligt de hele steekproef vóór de release van Snap
(2026-10-12), dus de training kan de uitkomst bevatten. De `bare`-arm, zonder enig bewijs,
haalt op de 94 benoemde backtestnamen ρ +0.170 (p 0.11), terwijl v2 op dezelfde namen
−0.023 haalt; in oktober haalt `bare` +0.04. Niet significant, maar lekken is daarmee niet
uitgesloten, en een positief resultaat op deze steekproef was dus niet te lezen geweest.
Een negatief resultaat wel: lekken kan Snap alleen bevoordelen, en zelfs dan voegt het niets
toe. Op de 9 namen na de release haalt v2 ρ −0.07, een anekdote.

## Wat het niet laat zien

21 dagen, 154 namen, bruto, en de toppen rusten op 8 tot 29 namen met standaardfouten van
ongeveer 3 punten. Snap is deterministisch maar gevoelig voor de vorm van de request
(`researcher_us/SNAP_JUROR_HANDOFF.md`), dus dit geldt voor deze precieze vraag. De
geanonimiseerde namen dragen het meeste signaal voor iedereen: ρ van het panel is +0.047 op
de benoemde backtestnamen.

## Bestanden

- `snap_backtest.py`: steekproef, calls (met cache), analyse. `--analyse-only` rekent
  opnieuw zonder te bellen. Het importeert `researcher_us/scripts/snap_juror.py` en het
  `snap_juror`-blok in `config/pipeline.yaml`, die alleen op branch
  `claude/gallant-bohr-hzsesq` staan: daar draait het, op `main` niet.
- `responses.jsonl`: elk antwoord van Snap, per arm, met de requesthash. Model overal
  `subq-snap-preview`; 3,8 miljoen input tokens, $0,19.
- `results.json`: alle tabellen en de rijen per naam.
