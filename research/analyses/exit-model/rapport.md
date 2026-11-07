# Eerder of later uitstappen? Een theoriegestuurd model getoetst (US, amc en bmo)

*Gemeten op 7 november 2026. Model, factoren, tekens en toetsen lagen vast in `PREREG.md` (gecommit om 22:42 UTC, voordat er één koers was opgehaald). Alpaca SIP-minuutbars, bruto, koersen en geen fills. Onderzoek, geen beleggingsadvies.*

## Kort antwoord

**Het model werkt niet.** Tien factoren uit de literatuur, met het teken dat de theorie voorschrijft en zonder te fitten, voorspellen op de holdout (21 oktober tot 6 november, 1.472 earnings-gaps over 13 dagen) niet of een koers na de opening doorloopt of terugvalt: ρ −0,02, p 0,69. Op onze eigen calls levert de regel die erop gebouwd is niets op: +0,02 punt per call op E-P v2 (n 131) en +0,03 op v3 (n 120), beide t 0,1.

**Stage M voorspelt wel iets, maar andersom dan bedoeld.** Hoe meer ruimte de analist nog ziet aan onze kant, hoe slechter de positie het na de opening doet (ρ −0,33 over 76 namen, 10 ochtenden). Dat bevestigt wat op 28 oktober al op 36 namen zichtbaar was. Op de nieuwe ochtenden wijst het dezelfde kant op, maar is het niet significant.

**Wat dit betekent voor de exits:** de standaard (amc op de opening, bmo om 13:00) blijft staan. Er is geen combinatie van prijs-, volume- en aandachtsfactoren gevonden die per naam zegt wanneer eerder of later beter is.

## Wat ik heb gebouwd

### De vraag in één getal

Voor elke earnings-gap van minstens 2% meet ik de beweging van de opening tot 13:00 in de richting van de gap (Y1). Is Y1 positief, dan loopt de gap door; negatief, dan valt hij terug. Voor onze positie betekent dat:

- **amc:** staat de positie aan de kant van de gap en loopt hij door, dan was later uitstappen (13:00) beter dan de opening.
- **bmo:** valt de gap terug terwijl wij aan de kant van de gap zitten, dan was eerder uitstappen (de opening) beter dan 13:00.

Daarnaast heb ik 10:00 (Y2), 13:00 tot het slot (Y3, bmo later) en voor amc de pre-market tot de opening (Y0, eerder dan de opening) getoetst.

### De factoren en waarom

| # | Factor | Verwacht | Theorie | Holdout (ρ met teken van de theorie) |
|---|---|---|---|---|
| F1 | Gap gedeeld door de optie-implied move | terugval | Overreactie op grote verrassingen; optiehandelaren overschatten de volatiliteit na earnings (Goyal & Saretto) | −0,01 (p 0,83) |
| F2 | Aantal concurrerende earnings die dag | doorlopen | Beperkte aandacht: drukke dagen geven een tragere reactie en meer drift (Hirshleifer, Lim & Teoh 2009) | −0,01 (p 1,0) |
| F3 | Pre-market dollarvolume tegen normaal | terugval | Particuliere aandacht duwt de opening te ver, die herstelt in de dag (Berkman, Koch, Tuttle & Zhang 2012) | **−0,06 (p 0,03): omgekeerd** |
| F4 | Omvang en liquiditeit | doorlopen | Liquiditeitsgedreven terugval is groter waar weinig marktmakers zijn (So & Wang 2014; Dai, Medhat, Novy-Marx & Rizova) | −0,01 (p 0,76) |
| F5 | Aanloop van 20 dagen in de richting van de gap | terugval | Kortetermijnomkering | **−0,06 (p 0,02): omgekeerd** |
| F6 | Opening voorbij de pre-market | terugval | Druk van marktorders in de openingsveiling (Berkman et al.; Barclay & Hendershott 2003) | +0,04 (p 0,18) |
| F7 | Late pre-market-drift (08:00 tot 09:30) | doorlopen | Geleidelijke verspreiding van informatie (Gao, Han, Li & Zhou 2018) | +0,06 (p 0,05) |
| F8 | Neerwaartse gap | doorlopen | Slecht nieuws verspreidt zich trager (Hong, Lim & Stein 2000) | +0,06 (p 0,03) |
| F9 | bmo in plaats van amc | doorlopen | Minder tijd om te verwerken voor de opening | −0,01 (p 0,83) |
| F10 | Volatiliteit over 20 dagen | terugval | Voorraadrisico van marktmakers vraagt een hogere vergoeding | −0,04 (p 0,12) |

Training (31 augustus tot 20 oktober): 221 gaps over 32 dagen. Holdout: 1.472 gaps over 13 dagen. Factoren zijn gestandaardiseerd op de training.

**Het hoofdmodel (M-A)** telt de tien factoren op met het teken van de theorie, zonder iets te fitten. **De variant (M-B)** fit een regressie op de training en laat factoren vallen waarvan het teken tegen de theorie ingaat. Daarvan bleven er vier over, en in de praktijk is M-B vooral factor F8 (neerwaartse gap).

## Uitkomsten

### Toets 1: de hele markt, holdout

| Model | Uitkomst | n | ρ | p (eenzijdig) |
|---|---|---|---|---|
| **M-A (primair)** | **opening → 13:00** | **1.472** | **−0,02** | **0,69** |
| M-A | opening → 10:00 | 1.472 | −0,05 | 0,98 |
| M-A | 13:00 → slot | 1.472 | +0,01 | 0,20 |
| M-B | opening → 13:00 | 1.472 | +0,05 | 0,02 |
| M-B | opening → 10:00 | 1.472 | −0,06 | 0,99 |
| M-A, pre-market | amc pre-market → opening | 625 | −0,05 | 0,72 |

Het hoofdmodel faalt op alle horizonnen. M-B haalt formeel de drempel (p 0,02), maar met ρ +0,05 verklaart het vrijwel niets. Het rust bovendien op de neerwaartse gaps, en dat effect is per dag niet stabiel: gepoold +0,4 tot +0,5 punt, maar op 4 van 11 (amc) en 3 van 13 (bmo) dagen positief, t over dagen −0,4 en −0,6. Het gemiddelde komt dus van een paar drukke dagen.

### Toets 2: de regel op onze calls, holdout

De regel grijpt alleen in als het model sterk is (boven het 67e percentiel van de training): amc langer vasthouden als het model doorlopen in ons voordeel ziet, bmo op de opening verkopen als het terugval tegen ons ziet.

| Calls | n | Winst per call vs standaard | t | Per dag |
|---|---|---|---|---|
| E-P v2, alle | 131 | +0,02 | 0,09 | t −0,14, 5 van 7 dagen |
| E-P v2, sterk | 33 | +0,50 | 0,99 | t 1,11 |
| E-P v3, alle | 120 | +0,03 | 0,09 | t 0,07 |
| E-P v3, sterk | 22 | +0,07 | 1,30 | ingegrepen op 3 calls |

Het model ordent ook de winst van langer vasthouden niet (ρ −0,04 op v2, −0,03 op v3). Volgens de vooraf vastgelegde regel telt het niet, want de markttoets faalde.

### Toets 3: de informatie van stage M

76 namen met een stage M-review (promptversie v2, 21 oktober tot 6 november, 10 ochtenden). Elk signaal is zo gericht dat positief betekent: langer vasthouden is beter.

| Signaal | ρ met winst opening → 13:00 | ρ met winst 13:00 → slot |
|---|---|---|
| S1 verwachte beweging na de opening, volgens de analist | −0,22 | +0,09 |
| S2 kans op terugval voor 10:00, volgens de analist | −0,27 | +0,08 |
| S3 release read voorbij de pre-market, aan onze kant | **−0,33** | +0,12 |
| S4 verrassing, guidance en over/undershoot | +0,02 | −0,06 |
| Gemiddelde van de vier | −0,22 | +0,08 |

Drie van de vier analistensignalen wijzen tegen de uitkomst in. Waar de analist denkt dat er nog ruimte is aan onze kant, liep de koers tot 13:00 juist tegen ons. Bij bmo is het gemiddelde van de vier het sterkst negatief (ρ −0,39, n 26). De fundamentele verrassing en de guidance (S4) zeggen niets.

## Verkennend, na het zien van de uitkomsten

Dit is niet vooraf vastgelegd en geldt dus als aanwijzing, niet als bewijs.

**Stage M als tegensignaal, per periode.** De namen waar de release read meer dan 3 punt voorbij de pre-market ligt aan onze kant:

| Periode | Read ver voorbij pre-market: opening → 13:00 | De rest: opening → 13:00 |
|---|---|---|
| 21 tot 27 oktober (al eerder gezien) | −4,66 (n 14, 0 van 5 dagen positief) | +1,81 (n 15) |
| 28 oktober tot 6 november (nieuw) | −1,71 (n 14, t −0,94) | +2,74 (n 23, t 1,22) |

Op de nieuwe ochtenden is het verschil kleiner maar wijst het dezelfde kant op. Het is niet significant: 14 namen over 5 dagen. Waarschijnlijk de verklaring: de analist houdt vast aan zijn eigen lezing van de cijfers, terwijl de markt het bij de opening al anders zag. Daarin had de markt meestal gelijk.

**Wat in de holdout wél richting gaf, was momentum en geen omkering.** Meer pre-market-aandacht, een aanloop in de richting van de gap en late pre-market-drift gingen alle drie samen met dóórlopen. Dat past bij recent onderzoek naar particuliere handel rond earnings (Michels; Friedman & Zeng: meer drift waar particulieren actief zijn) en niet bij de omkeringen uit 1996 tot 2008 (Berkman et al.). Er lijkt een nieuw model in te zitten, maar ik heb het gekozen na het zien van de data. Het moet eerst vooruit bewijzen dat het werkt.

## Wat ik zou doen

1. **Exits niet veranderen.** Geen model of regel verslaat "amc op de opening, bmo om 13:00", en dat sluit aan bij alle eerdere studies in dit project.
2. **Stage M niet laten afwijken op basis van zijn eigen fundamentele lezing.** Als stage M iets meegeeft, is het het tegendeel: ziet de analist veel ruimte die de pre-market niet heeft ingeprijsd, dan is de opening eerder te laat dan te vroeg. Dat sluit aan bij de bevinding van 4 november (stage M verliest op amc). Ik zou het één tot twee maanden vooruit loggen: read min pre-market per naam, en daarna afrekenen. Bij de huidige spreiding van ongeveer 5 punt per call is voor een echt verschil van 2 punt zo'n 50 namen per groep nodig.
3. **Het momentummodel alleen vooruit toetsen.** Leg het vast (F3, F5 en F7 met het omgekeerde teken, plus F8) en reken het na een maand af, op nieuwe dagen.

## Kanttekeningen

- **De training is klein en anders.** 221 gaps in september en begin oktober, buiten het earnings-seizoen. De holdout valt midden in het seizoen, met meer en grotere bedrijven. Daardoor kon M-B weinig leren, maar het hoofdmodel had niets te leren en faalde ook.
- **13 holdoutdagen.** Namen op één dag delen dezelfde markt, dus de t over dagen is de eerlijke, en die is overal zwak.
- **Stage M:** 76 namen op 10 ochtenden is te weinig om iets vast te stellen. Het tegensignaal is consistent in richting, maar niet bewezen.
- Koersen en geen fills. In dunne namen kost een tweede order (10:00 of 13:00) spread. Een voordeel onder ongeveer 0,3 punt overleeft dat niet.

## Reproduceren

Scripts in `scripts/` (ook op branch `claude/project-thread-k81smj`, `research/analyses/exit-model/`): `events.py` (events en calls, vanuit de repo-root), `fetch2.py` (Alpaca-bars, sleutels uit de omgeving), `build.py` (factoren en uitkomsten), `analyse.py` (de vooraf vastgelegde toetsen, uitvoer in `results.txt`), `explore.py` (de verkennende delen, uitvoer in `explore.txt`).

## Bronnen

- Berkman, Koch, Tuttle & Zhang (2012), [Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/paying-attention-overnight-returns-and-the-hidden-cost-of-buying-at-the-open/F9AAD159B512C651F09D5D52011D88E0), JFQA
- Hirshleifer, Lim & Teoh (2009), [Driven to Distraction](https://econpapers.repec.org/RePEc:bla:jfinan:v:64:y:2009:i:5:p:2289-2325), Journal of Finance
- So & Wang (2014), [News-driven return reversals: Liquidity provision ahead of earnings announcements](https://ideas.repec.org/a/eee/jfinec/v114y2014i1p20-35.html), JFE; Dai, Medhat, Novy-Marx & Rizova, [Reversals and the returns to liquidity provision](https://mysimon.rochester.edu/novy-marx/research/RRLP.pdf)
- Barclay & Hendershott (2003), [Price discovery and trading after hours](https://typeset.io/pdf/price-discovery-and-trading-after-hours-37izopiu7w.pdf), RFS; Jiang, Likitapiwat & McInish (2012), [Information content of earnings announcements: evidence from after-hours trading](https://ideas.repec.org/a/cup/jfinqa/v47y2012i06p1303-1330_00.html)
- Llorente, Michaely, Saar & Wang (2002), [Dynamic Volume-Return Relation of Individual Stocks](https://www.nber.org/papers/w8312), RFS
- Gao, Han, Li & Zhou (2018), [Market Intraday Momentum](https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414), JFE
- Lou, Polk & Skouras (2019), [A Tug of War: Overnight Versus Intraday Expected Returns](https://personal.lse.ac.uk/polk/research/TugOfWar.pdf), JFE
- Goyal & Saretto, via [RePEc](https://ideas.repec.org/a/eee/empfin/v40y2017icp220-235.html) (overschatting van volatiliteit na earnings)
- Michels, [Retail investor trade and the pricing of earnings](https://link.springer.com/article/10.1007/s11142-024-09825-9), Review of Accounting Studies; Friedman & Zeng, [Retail Investor Trading and Market Reactions to Earnings Announcements](https://scholarspace.manoa.hawaii.edu/items/ac246f3a-13bf-43f8-b5c0-55a302f690e9)
- Zhang (2008), [Analyst responsiveness and post-earnings-announcement drift](https://business.columbia.edu/sites/default/files-efs/pubfiles/3737/zhang.pdf), JAE

## Vervolg (7 november): amc verkopen op de opening of 1 tot 2 minuten later

Script `scripts/amc_minutes.py`, uitvoer `amc-minutes.txt`. Koers om 09:31 = slot van de minuutbar van 09:30, enzovoort. Verschil met verkopen op de opening, in punten aan de kant van de positie (positief = later is beter).

| Groep | n | 09:31 | 09:32 | 09:33 | 09:35 |
|---|---|---|---|---|---|
| Markt, amc-gaps ≥2%, kant van de gap, t/m 27 okt | 153 (27 dagen) | −0,28 (t −1,5) | −0,16 | −0,42 | −0,58 |
| Markt, idem, 28 okt t/m 6 nov | 569 (7 dagen) | **−0,66 (t over dagen −3,0)** | **−0,56 (t over dagen −2,4)** | −0,50 | −0,42 |
| E-P v2, alle | 68 | +0,10 | −0,30 | −0,40 | −0,37 |
| E-P v2, sterk | 22 | +1,21 (t 1,6) | +0,63 | +0,30 | +0,46 |
| E-P v3, alle | 69 | −0,44 | +0,12 | −0,13 | −0,52 |
| E-P v3, sterk | 14 | −0,45 | +1,26 | +1,56 | +1,81 |

Op de hele markt is de opening de beste prijs voor wie aan de kant van de gap zit. Al in de eerste minuten geeft de koers gemiddeld een halve punt terug, en in de nieuwe periode is dat duidelijk significant. Op onze calls is het ruis: de tekens wisselen tussen v2 en v3 en tussen 09:31 en 09:32, en geen cel haalt t 2. Bij v2 deed 09:32 het slechter bij posities die op de opening verlies stonden (−0,76, n 35, t −1,9). Bij v3 was dat juist beter. Conclusie: een of twee minuten wachten levert niets op, en op de markt als geheel kost het geld. Een kanttekening: een order die in de pre-market klaarstaat, wordt in de praktijk rond 09:30 tot 09:31 gevuld, dus de echte "opening" ligt al iets later dan de openingsprint.
