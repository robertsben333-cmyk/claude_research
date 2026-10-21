# Onderzoek Europees panel (stage EU, vier modellen)

Peildatum 21 oktober 2026. Alle rendementen zijn bruto, zonder spread of kosten, en met het teken van het panel (long als het panel omhoog zegt, short als het omlaag zegt). Elke uitsplitsing is verkennend.

## Kort antwoord

**Effectiviteit.** Op de zeven live paneldagen (12 tot en met 20 oktober, 45 namen) rangschikt het panel de dag licht in de goede richting, maar niet meetbaar: binnen de dag ρ +0,22 (permutatie p 0,19). Over alle namen verdient de panelkant niets (−0,08% per naam, 53% raak) en blijft hij onder "alles long" (+0,97%). Alleen de sterke calls (panel_pct ≥ 70, de scorebord-drempel) wijzen de goede kant op: 3 van 4 raak, +1,85% gemiddeld, t 0,41. Dat zijn vier namen; daar valt niets uit te concluderen.

**Instap en uitstap.** Het tijdstip van instappen maakt weinig uit: direct na het panel instappen in plaats van op de slotkoers levert gemiddeld +0,28% per naam op (t 1,60, n 45). Het tijdstip van uitstappen maakt meer uit. Bij de sterke calls verliest verkopen op de opening op de reactiedag (−1,71% live, n 4), terwijl vasthouden tot het slot wint (+1,85% live; +6,17% in de backtest, n 7). In beide sets loopt de handelsdag zelf, van opening tot slot, met het panel mee. De huidige score-window, close(D−1) naar close(D), is dus de goede. Of nog een dag langer houden helpt, verschilt per set (live +8,2% op 3 namen, backtest −2,2% op 7) en is nog niet te zeggen.

**Voor welke aandelen.** Niets is significant na correctie. De sporen die het waard zijn om te volgen: namen waar de vier rechters het eens zijn (lage spreiding: +1,17% tegen −1,38%), volatiele namen (20-daagse vol ≥ 40%: +5,2%, t 2,34, n 6, p 0,07) en hoge scores die vooral grotere bewegers aanwijzen. Zwak lijken de namen met 0 tot 2 analisten (−4,6%, n 6). Een shortregister (anchor) helpt hier niet zichtbaar.

**Het belangrijkste voorbehoud.** Twee versies, kleine aantallen, en één markt domineert: live zijn 20 van de 45 namen Zweeds en 16 Brits.

## Wat er gemeten is

| set | dagen | namen | hunters | rechters | opmerking |
|---|---|---|---|---|---|
| Live | 12, 13, 14, 15, 16, 19, 20 okt | 45 van 47 | v7-familie (uk.v7, de.v7, nordic.v5, …), Opus 5.5 met gedeelde core | `panel-judge-intl-*` | INVE_A neutraal (panel 0), DB1 (amc) nog niet afgerond |
| Backtest | 22 en 23 sep | 18 | uk.v3/de.v3 enz., Opus 5 | blinde herbeoordeling van 1 okt | 8 van de 18 waren geanonimiseerd; alle Britse namen op één na |

De september-runs van Opus 5.5 (24 sep tot en met 1 okt) zijn weggelaten, zoals afgesproken. De twee sets zijn verschillende promptversies en worden **nooit samengevoegd**. Op 7 en 8 oktober (ook v7) is geen panel gedraaid; die dagen zouden de live set met ongeveer 15 namen kunnen vergroten.

Alle namen live zijn bmo. Live is R dus de rapportagedag D, en close(D−1) is gelijk aan de slotkoers van de paneldag.

**Twee correcties op de resolver.** `eu_resolve.py` markeerde Ericsson (ERIC_A) en Nordea (NDA_FI) op 15 oktober als "geen cijfers gepubliceerd". Beide publiceerden die ochtend hun Q3-cijfers ([Ericsson](https://capital.com/en-int/news/ericsson-reports-third-quarter-results-2026), [Nordea](https://www.nordea.com/en/press/2026-10-01/nordea-to-present-its-third-quarter-results-2026-on-15-october)) en bewogen +9,9% en −7,8%. Ze tellen hier mee. Dit is de TRT-fout in omgekeerde richting, in de koppeling met de Nordic-feed, en moet apart worden opgelost. Daarnaast is op geen enkele EU-paneldag sinds 8 oktober een `eu-resolved.json` in de repo gezet. Het scorebord prijst de calls zelf, maar de resolver van de stage loopt achter.

**Twee schalen voor panel_pct.** Live leest elke rechter zijn percentiel af tegen zijn eigen eerdere groottes. De eerste EU-dagen hadden nog geen Europese geschiedenis en lazen af tegen de Amerikaanse E-P-groottes, met een top-20%-grens rond 2,8. Daardoor kwamen vroege Europese namen laag uit. Naast de live schaal staat daarom een "uniforme" schaal: elke rechter tegen al zijn Europese oktobergroottes. Die gebruikt alleen groottes en geen uitkomsten. Op de uniforme schaal halen 12 namen de 70 in plaats van 4. Die 12 halen +0,60% met 58% raak, dus de extra namen verbeteren niets.

## 1. Hoe effectief is het panel?

### Live, close(R−1) → close(R)

| rangschikker | ρ binnen de dag | p | n |
|---|---|---|---|
| panel_pct (live schaal) | +0,22 | 0,19 | 44 |
| panel_pct (uniforme schaal) | +0,20 | 0,25 | 44 |
| hunter impact_sum | +0,18 | 0,28 | 44 |
| gratis controle −run_up_20d | +0,25 | 0,15 | 44 |
| rechter Opus 5 / Opus 5.5 / Sonnet 5.5 / Fable 5.1 | +0,11 / +0,16 / +0,13 / +0,17 | 0,35 tot 0,51 | 44 |

| boek (met het teken van het panel) | n | gemiddeld | mediaan | raak | t | p |
|---|---|---|---|---|---|---|
| alle namen | 45 | −0,08% | +0,87% | 53% | −0,08 | 0,93 |
| controle: alles long | 45 | +0,97% | +1,07% | 58% | 1,00 | 0,32 |
| panel_pct 0–50 | 31 | −0,28% | +0,87% | 52% | −0,23 | 0,82 |
| panel_pct 50–70 | 10 | −0,22% | −0,20% | 50% | −0,12 | 0,91 |
| **panel_pct ≥ 70** | **4** | **+1,85%** | +5,62% | 75% | 0,41 | 0,71 |
| panel_pct ≥ 60 (= consensus 3 van 4 op deze dagen) | 7 | +2,61% | +5,02% | 71% | 1,01 | 0,35 |

De vier sterke calls zijn AVARDA (long, +7,8%), AIRA (short, +4,6%), ITM (short, +6,7%) en BMAX (short, −11,6%). Eén misser van 11,6% bepaalt het gemiddelde. De rangschikking van het panel is niet beter dan die van de gratis controle −run_up_20d (ρ +0,25).

Hoge scores wijzen wel grotere bewegers aan: de mediane absolute beweging is 7,2% bij ≥ 70, tegen 3,7% bij 50–70 en 3,1% daaronder. Het panel herkent dus een print die ertoe doet. Of het de richting goed heeft, is met vier namen niet te zeggen.

### Backtest (22–23 sep, Opus 5-hunts, blinde herbeoordeling)

| | n | resultaat |
|---|---|---|
| ρ panel binnen de dag | 18 | +0,39, p 0,12 (hunter zelf +0,25, controle +0,13) |
| alle namen | 18 | +2,15%, 61% raak, t 1,24 |
| panel_pct ≥ 70 | 7 | +6,17%, 86% raak, t 2,15, p 0,08 |
| panel_pct ≥ 80 | 4 | +11,2%, 4 van 4 |

Hier rangschikt het panel beter en zijn de sterke calls 6 van 7 raak. Dat sluit aan bij de herbeoordeling van 1 oktober, waar de rechters Europa beter rangschikten dan de hunt zelf. Er zijn wel drie kanttekeningen. Het gaat om twee dagen met bijna alleen Britse namen. Acht van de achttien waren geanonimiseerd omdat hun naam bekend was, dus herkenning is niet uitgesloten. En de groottes van de hunters komen uit een oudere prompt.

## 2. Hoeveel maken instap- en uitstaptijd uit?

**Instap:** "seal" is de koers in de 5-minutenbar waarin het panel klaar was, rond 14:00–14:40 UTC op de paneldag (de seal zelf was rond 13:45). Daarnaast staat close(D−1), de slotkoers van die dag. **Uitstap:** de opening van de reactiedag R (eerste 5-minutenbar), +30 minuten, +1, +2 en +4 uur na de officiële opening (Londen 08:00, continent 09:00 lokale tijd), close(R), en close(R+1), R+2 en R+5.

### Live, sterke calls (≥ 70, n 4), gemiddeld rendement met het teken van het panel

| instap \ uitstap | open R | +30m | +1u | +2u | +4u | close R | close R+1 |
|---|---|---|---|---|---|---|---|
| seal | −0,58 | +2,76 | +2,30 | +3,20 | +1,10 | +2,87 | +9,74 (n3) |
| close D−1 | −1,71 | +1,77 | +1,31 | +2,22 | +0,06 | +1,85 | +8,15 (n3) |

### Live, alle namen (n 45)

| instap \ uitstap | open R | +1u | +2u | close R | close R+1 (n35) | close R+2 (n31) |
|---|---|---|---|---|---|---|
| seal | −0,13 | −0,06 | +0,05 | +0,17 | +0,97 | +0,02 |
| close D−1 | −0,41 | −0,31 | −0,21 | −0,08 | +0,59 | −0,32 |

### Backtest, sterke calls (≥ 70, n 7)

| instap \ uitstap | open R | +30m | +1u | +2u | +4u | close R | close R+1 | close R+5 |
|---|---|---|---|---|---|---|---|---|
| seal | +3,18 | +4,06 | +3,99 | +4,50 | +4,90 | **+6,33** (86% raak, t 2,4) | +4,09 | +3,84 |
| close D−1 | +3,06 | +3,92 | +3,84 | +4,35 | +4,72 | **+6,17** (86%, t 2,1) | +3,98 | +3,72 |

### De beweging opgedeeld in stukken (met het teken van het panel)

| stuk | live alle (n 45) | live ≥ 70 (n 4) | backtest alle (n 18) | backtest ≥ 70 (n 7) |
|---|---|---|---|---|
| seal → slot paneldag | +0,28%, t 1,60 | +1,09% | +0,11% | +0,10% |
| slot → opening R (gap) | −0,41% | −1,71% | +1,26% | +3,06% |
| opening → slot R | +0,34% | **+3,42%** (3 van 4) | +0,94% | **+3,10%** (6 van 7, t 2,12) |
| slot R → slot R+1 | −0,04% (n 35) | +1,80% (n 3) | **−1,25%** (22% raak, t −1,88) | −2,15% |
| slot R → slot R+5 | n 6, te vroeg | | −1,41% | −2,51% |

Gemiddeld zit 55% (live) en 43% (backtest) van de absolute beweging van slot tot slot al in de openingsgap. De rest ontstaat tijdens de dag.

**Wat dit betekent:**

- **Instap.** Direct na het panel instappen of op de slotkoers ligt dicht bij elkaar. Live is direct instappen 0,28 punt per naam beter (t 1,6), in de backtest 0,1 punt. Een slotveiling is voor deze dunne namen waarschijnlijk de goedkopere uitvoering, en dat zal meer schelen dan dit verschil.
- **Uitstap op de opening is de zwakste keuze voor de sterke calls.** In beide sets loopt de handelsdag na de opening mee met het panel (+3,4% en +3,1%). Dat is hetzelfde patroon als bij de Amerikaanse bmo-namen: de markt verwerkt een ochtendprint gedurende de dag. Het slot van de reactiedag is in beide sets de beste of bijna de beste uitstap.
- **Na close R is het onduidelijk.** Live gaat dag twee door (n 3), in de backtest draait hij terug (−1,25%, t −1,88). Houd daarom close(R) aan en meet dag twee verder.
- **Wat de data niet kan.** De Europese pre-market (handel vóór de opening) bestaat niet als bruikbare tape. De opening is de eerste 5-minutenbar van Yahoo, en bij dunne Britse namen (SDG, BKS, BOOM) wijkt die tot 4% af van de dagopening. Spreads zijn niet gemeten. Close R+5 kan live alleen voor de dagen tot 14 oktober (n 6). Amc-namen zaten live niet in de set.

## 3. Voor welke aandelen werkt het beter?

Live, close(R−1) → close(R), met het teken van het panel. Elke cel is verkennend. Met 45 namen en ongeveer 40 vergelijkingen zijn een of twee "p < 0,10"-uitkomsten precies wat toeval oplevert.

| uitsplitsing | groep | n | gemiddeld | raak | t / p | ρ binnen groep |
|---|---|---|---|---|---|---|
| markt | Zweden | 20 | −0,82% | 55% | −0,64 | −0,21 |
| | VK | 16 | −0,64% | 44% | −0,41 | +0,23 |
| | Noorwegen | 3 | +1,83% | 33% | | |
| | continent (de/fr/es) + fi/dk | 6 | n te klein | | | |
| omzet per dag | < $1m | 23 | −0,41% | 48% | −0,35 | +0,12 |
| | $1–5m | 14 | +0,29% | 57% | 0,12 | +0,24 |
| | > $5m | 8 | +0,24% | 63% | | |
| shortregister (anchor) | ja | 14 | −1,18% | 50% | −0,67 | −0,01 |
| | nee | 31 | +0,42% | 55% | 0,35 | +0,22 |
| analisten | 0–2 | 6 | **−4,56%** | 17% | −2,19 / 0,08 | −0,49 |
| | 3–7 | 5 | +1,28% | 80% | | |
| | onbekend (Noordse namen) | 31 | +1,16% | 58% | 1,06 | +0,35 |
| spreiding tussen rechters | laag | 23 | **+1,17%** | 61% | 1,13 / 0,27 | **+0,39** |
| | hoog | 22 | −1,38% | 45% | −0,82 | −0,08 |
| rechters eens over richting | 4 van 4 | 35 | +0,58% | 57% | 0,62 | +0,18 |
| | 3 of minder | 10 | −2,37% | 40% | | |
| 20-daagse volatiliteit | ≥ 40% | 6 | **+5,22%** | 83% | 2,34 / 0,07 | +0,26 |
| | 25–40% | 16 | −1,92% | 50% | −1,00 | |
| | < 25% | 23 | −0,17% | 48% | | −0,21 |
| kant | long | 23 | +0,87% | 61% | 0,93 | |
| | short | 22 | −1,07% | 45% | −0,61 | |
| sector | Finance | 12 | +0,43% | 42% | | |
| | Technology Services | 11 | −0,42% | 64% | | +0,37 |
| | overige sectoren | 1–4 per groep | te klein | | | |
| dagomvang | 1–5 namen | 14 | −0,14% | 50% | | +0,32 |
| | 6–11 | 16 | −1,59% | 56% | | |
| | 12+ | 15 | +1,60% | 53% | | |

**Wat ik eruit lees:**

1. **Eensgezindheid van de rechters is het meest bruikbare spoor.** Lage spreiding en 4 van 4 eens over de richting gaan samen met beter rendement en een positieve ρ. Op deze dagen vallen consensus (3 van 4 in de eigen top) en ≥ 60 samen. Dit is een vervolgtest waard, maar nog geen regel.
2. **Volatiele namen.** Het panel scoort beter waar de koers het meest beweegt (n 6). Dat kan vaardigheid zijn, maar ook ruis van grote bewegingen. In de VS bleek de trefkans eerder mee te lopen met volatiliteit zonder dat het rendement per naam volgde (analyses/signal-vs-noise).
3. **Long tegen short zegt weinig.** Long +0,87% tegen short −1,07% is grotendeels de markt: alles long gaf zelf al +0,97%.
4. **Het shortregister helpt niet.** De namen mét register doen het slechter (−1,18% tegen +0,42%). Dat is het tegenovergestelde van wat het ontwerp verwacht. De groepen zijn klein, maar er is geen aanwijzing dat de anchor de rechters helpt.
5. **Markt en sector zijn niet te scheiden.** Zweden en het VK maken samen 36 van de 45 namen uit. Het continent heeft 4 namen, Spanje en Polen samen 1. Daarover valt niets te zeggen.

## Wat nodig is voor een echt antwoord

- **Meer dagen.** Om een trefkans van 60% bij de sterke calls te onderscheiden van een muntworp zijn ongeveer 50 sterke calls nodig. Met 4 per week duurt dat ruim twee maanden. Panelscores voor 7 en 8 oktober (zelfde v7-hunts, nog geen panel) zouden goedkoop ongeveer 15 namen toevoegen.
- **Kosten.** De meeste namen handelen voor minder dan $1m per dag. Zonder spreadmeting is elk rendement hier een bovengrens.
- **Resolver repareren.** Ericsson en Nordea zijn ten onrechte afgewezen, en de EU-resolver heeft sinds 8 oktober niet meer in de repo gedraaid.
- **Vooraf vastleggen** dat de volgende meting kijkt naar (a) sterke calls op close(R), (b) open→close R als aparte stap, en (c) de spreiding tussen rechters als splitsing, zodat dit niet achteraf wordt uitgezocht.

## Bestanden

- `report.txt` (in de projectmap `tabellen.txt`): de volledige output, met alle cellen, alle uitsplitsingen en de tabel per naam.
- Scripts: `collect.py` (dataset, prijzen via Yahoo 1d en 5m), `analyse.py` (alle tabellen, `report.txt`); `rescore/` bevat per dag de panelscores (dry-run, huidige methode) en de resolver-output.
