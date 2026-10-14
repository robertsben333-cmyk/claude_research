# Mag de panelselectie dagafhankelijk zijn?

**Vraag (Xavier, 2026-10-14).** Op dagen met veel kandidaten strenger, op dagen met weinig
kandidaten ook namen met een panelscore van 50, 60 of 70 meenemen. Hoe had dat uitgepakt?

**Kort antwoord.** Niet beter. In de enige steekproef die groot genoeg is om iets te
zeggen, de blinde backtest, levert aanvullen per dag op rekeningniveau +0,1 pp op tot
−0,8 pp, en geen regel komt in de buurt van significant (beste t 0,14). In oktober kost
elke dagregel geld, maar dat zijn vijf dagen en 24 namen. De vaste drempel van 80 blijft
staan.

## Opzet

`day_rules.py`. Elf regels, **vastgelegd voordat er één is doorgerekend**, en allemaal
gerapporteerd:

| regel | wat |
|---|---|
| vast80 | \|pct\| ≥ 80, de live regel van stage E-P |
| aanvul K/F | ≥ 80; heeft de dag minder dan K zulke namen, vul aan met de hoogste tot vloer F (K 2 of 3, F 50/60/70) |
| top3/F | precies de drie hoogste van de dag, niet onder F (een drukke dag wordt afgetopt) |
| staffel | drempel naar aantal beoordeelde namen: ≥ 12 namen 85, 7–11 80, 4–6 70, ≤ 3 60 |

Venster van het scorebord: instap 13:30 ET op de rundag, amc uit op de volgende opening,
bmo uit om 13:00 ET op de rapportdag. Bruto, gelijk gewogen.

Twee niveaus, omdat ze iets anders vragen. **Per call** is het gemiddelde over alle
gekozen namen; aanvullen verlaagt dat bijna per definitie. **Per dag** is wat de rekening
merkt: elke dag een volledig belegd boek uit wat gekozen is, een dag zonder keuze levert 0,
gemiddeld over alle dagen. Daar zou aanvullen kunnen winnen, want dat geld lag anders stil.
Het verschil met vast80 is gepaard per dag getoetst.

Steekproeven apart, nooit gepoold: de blinde herbeoordeling van de Opus 5-hunters
(aug–sep, één versie) en de live oktoberruns per zoekerversie.

## Uitkomst, backtest (115 namen, 15 dagen, mediaan 8 namen per dag)

| regel | calls | goed | per call | per dag | vs vast80 (t) | aangevulde namen |
|---|---|---|---|---|---|---|
| vast80 | 19 | 79% | +6.80% | +4.74% | | |
| aanvul 2/50 | 29 | 69% | +5.95% | +4.85% | +0.11 pp (0.09) | 10, gem +4.31% |
| aanvul 2/60 | 26 | 73% | +5.72% | +4.87% | +0.13 pp (0.14) | 7, gem +2.78% |
| aanvul 2/70 | 25 | 72% | +5.81% | +4.64% | −0.10 pp (−0.11) | 6, gem +2.67% |
| aanvul 3/50 | 36 | 64% | +4.17% | +3.94% | −0.80 pp (−0.54) | 17, gem +1.22% |
| aanvul 3/60 | 33 | 67% | +3.83% | +3.97% | −0.78 pp (−0.61) | 14, gem −0.21% |
| aanvul 3/70 | 30 | 67% | +4.37% | +4.23% | −0.51 pp (−0.46) | 11, gem +0.16% |
| staffel | 22 | 73% | +5.78% | +4.59% | −0.16 pp (−0.49) | 3, gem −0.71% |

`top3/F` is hier gelijk aan `aanvul 3/F`: geen dag had meer dan drie namen boven 80, dus
de "strenger op drukke dagen"-kant heeft in deze data nooit iets gedaan.

**Het mechanisme zelf.** De namen tussen 50 en 79 (n 35) leveren gemiddeld +0,85% (t 0,46).
Op dagen met minder dan twee namen boven 80 is dat +2,52% (n 17), op drukkere dagen
−0,73% (n 18): verschil +3,2 pp, t 0,88. Die richting past bij het idee, maar is ruis.
Per band: 50–59 +2,0% (n 12), 60–69 −2,2% (n 9), 70–79 +1,8% (n 14); geen monotone lijn.

## Uitkomst, oktober

- **us-searcher.v1 (10-02 t/m 10-09), 24 namen, 5 dagen.** vast80: 5 calls, 5 goed,
  +10,2% per call, +6,5% per dag. Elke dagregel voegt 3 tot 5 namen toe die gemiddeld
  −0,9% tot −2,0% opleveren en kost 2,3 tot 3,1 pp per dag (t −1,3 tot −1,7, p 0,08 tot
  0,21). Vijf dagen: te klein om iets te besluiten.
- **us-searcher.v2 (10-12), 9 namen, 1 opgeloste dag.** Niemand boven 80; aanvullen had
  één naam gekocht (+3,8%). Eén naam op één dag zegt niets.

## Vervolg (Xavier, 2026-10-14): meer meetdagen en een portefeuillerun

Het punt is niet de winst per dag, maar dat je op meer dagen meet. Twee lezingen erbij.

**Meetkracht per call (backtest).** vast80 geeft calls op 11 van de 15 dagen: 19 calls,
t 1,97. Aanvul 2/50 geeft 14 dagen, 29 calls, t 2,43; 2/60 26 calls, t 2,20; 2/70 25 calls,
t 2,15. Aanvullen tot 3 verlaagt de t (1,65 tot 1,88). Voor het meten zelf is selectie
niet nodig: elke beoordeelde naam wordt opgelost en telt mee in de kalibratiecurve.

**Portefeuille** (de regel van `../portfolio-simulator/`: gelijk gewogen, maximaal X% per
naam, rest in kas, samengesteld; start $10.000, bruto). Backtest, 15 dagen:

| regel | cap 50%: eind | max dd | belegd | cap 33%: eind | belegd |
|---|---|---|---|---|---|
| vast80 | +56.8% | −19.0% | 57% | +48.5% | 42% |
| aanvul 2/50 | +91.0% | −19.6% | 90% | +69.8% | 64% |
| aanvul 2/60 | +71.7% | −19.6% | 80% | +57.9% | 57% |
| aanvul 2/70 | +68.8% | −19.6% | 77% | +56.1% | 55% |
| aanvul 3/50 | +69.9% | −10.1% | 90% | +58.5% | 79% |
| staffel | +53.8% | −19.6% | 63% | +47.4% | 48% |

Met een cap per naam staat op een dag met één naam de helft (of twee derde) in kas, en
aanvullen zet dat geld aan het werk. Daarom wint aanvullen hier wel, waar het in het
volledig belegde boek van boven niet won. Gepaard per dag tegen vast80 (cap 50%): 2/50
+1,44 pp per dag, t 1,33, 4 dagen beter en 4 slechter; 2/60 +0,65 pp, t 0,89; 2/70
+0,53 pp, t 0,73. Niet significant, en het verschil zit in een handvol dagen.

Oktober v1 (5 dagen, cap 50%): vast80 +22,2%, aanvulregels +17,5% tot +19,8%. Daar kost
het, op vier extra calls. Oktober v2: één dag, aanvullen +1,9% tegen 0.

**Lezing.** Of aanvullen loont, hangt vooral af van de cap: die bepaalt hoeveel geld er op
een dunne dag stil ligt. De richting in de backtest is gunstig voor aanvullen tot 2 namen,
in oktober ongunstig, en geen van beide is genoeg om op te handelen.

## Europa

Niet doorgerekend. Het EU-panel draait sinds 2026-10-12 en heeft één opgeloste dag; de
backtest heeft 18 Europese namen. Dat is te weinig voor een dagregel.

## Waarom dit voorzichtig gelezen moet worden

- Elf regels op dezelfde data: het beste resultaat is het optimistische. Ook de beste
  regel (+0,13 pp, t 0,14) is na die correctie niets.
- De backtest is de data waarop het panel zelf ontwikkeld is (judge lab), dus niet vers.
- De percentielen in de backtest komen uit dezelfde namen; live worden ze per dag tegen
  de eerdere live range gelezen.
- De kalibratiecurve (`../panel-mean-pct/`) zegt al dat een naam op 60–70 ongeveer +0,8%
  tot +1,6% verwacht, tegen +2,6% op 80. Aanvullen koopt dus trades met een kleine
  verwachte winst en dezelfde spreiding; het helpt de rekening alleen als dunne dagen
  systematisch beter betalen in de middenband, en dat is niet aangetoond.

## Wat vooruit te meten valt

De ene toetsbare hypothese die overblijft: namen op 50–79 betalen beter op dagen met
weinig namen boven 80. Leg die vast en lees hem na een paar weken op zoekerversie v2 alleen.
Er verandert niets aan de scorer of de Routines.
