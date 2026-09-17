# Performance log

Append-only. One dated section per update, written by the `edge-performance` skill.
Three things in every entry: what closed and what resolved, the pooled ranking figure
beside its free control, and one sentence of critical read.

## 2026-09-17 — first build

Thirteen runs, 107 names priced, 102 in the ranking sample over 11 days (five names
are duplicate events: the 09-04 run re-hunted names the 09-07 run hunted again for
the same 09-08 prints, and the run closest to the print is the one kept). Eleven
positions at the broker, nine closed.

Closed so far, in entry order: HOFT +7.1%, ORCL −6.2%, FEIM −29.1%, RH −1.1%,
CODA −6.2%, FPS +15.6%, VRA +41.8%, RLGT +17.2%, LUXE +25.4%. Six of the nine were
closed by hand, not by stage E — three `opg`/`cls` orders filled, and HOFT and CODA
sat 95 hours before someone sold them. Open: ALMU and LEN, both entered 09-16.

Pooled over all 11 days: **ρ = −0.145** for `impact_sum` against the realised move,
against **−0.137** for the free control `-run_up_20d_pct`. The conviction test
(does the rank of |impact_sum| predict whether its sign was right) is +0.185, and
the sign was right on 59 of 101 names. Per day the picture splits cleanly: the five
days `edge/EDGE_ANALYSIS.md` was written on (08-31 … 09-07) pool at ρ ≈ +0.38 and
the conviction test at +0.44, in line with the +0.453 and +0.514 recorded there;
every day from 09-08 onward is at or below zero — 09-08 −0.333, 09-09 −0.290,
09-10 −0.200, 09-11 −0.316 — with 09-14 (+0.828) and 09-15 (+0.800) on four and
nine names pulling back the other way.

Account: $10,000 → $11,729, +17.3% over eight sessions, max drawdown −6.9%. Mean
per closed position +7.18% with a 95% interval of −6.4% to +20.8%.

**Read.** Nothing here is established and two things are worth watching. The
ranking has not beaten its free control on any pooled cut, and since 09-08 neither
of them sorts the day at all — which is the same window in which the sample stopped
being the one `EDGE_ANALYSIS.md` was written on. The account's +17% is one leg: six
longs at +17.7% against three shorts at −13.9%, in a week when shorting everything
paid −1.7% a name. Nine positions cannot separate a strategy from a market. The
number to watch over the next ten days is the conviction test on new days only,
because that is the one finding the repo rests its trading rule on.

*(This build re-prices every run from the raw `edge-scores.json` and Yahoo bars
rather than reading `edge/analysis/edge-rows.json`, so its figures for the first
six days sit a few hundredths from the frozen ones in `EDGE_ANALYSIS.md` — same
method, freshly computed, and the duplicate-event rule is derived rather than
hard-coded to a date.)*

## 2026-09-17 — dashboard uitgebreid, eerste doorsnedes

Geen nieuwe runs of posities sinds de eerste build; wat er bij kwam zijn de sneden.
Het dashboard filtert en rekent nu client-side, dus lens (onderzoek of handel),
uitstapmoment, drempel, verhandelbaarheid, sessie en sector leiden elk getal op de
pagina opnieuw af. Nieuw in de ledger: sector en industrie per ticker (Yahoo),
shortability (het `alpaca-assets.json` van de run zelf waar dat bestaat, anders een
actuele lookup), theoretisch tegen werkelijk rendement per positie, en een kostenblok
per run.

Vier dingen die de sneden laten zien en de gepoolde cijfers niet:

1. **De drempel werkt tegengesteld voor de twee sessies.** Over alle namen loopt bmo
   monotoon op met de drempel — +2.5% bij ≥0 tot +12.0% bij ≥7 — terwijl amc er mee
   daalt, van −0.7% naar −2.9% en −9.1% bij ≥10. De gepoolde curve (+0.7% naar +3.8%)
   is het gemiddelde van twee tegengestelde bewegingen. Als dit standhoudt is een
   drempel per sessie het eerste dat aan de config moet veranderen; n is nu 46 bmo
   tegen 56 amc en bij ≥7 nog 9 tegen 11, dus standhouden is precies de vraag.
2. **Het rendement zit in de dunne helft.** Gesplitst op de mediane dagomzet ($5.2m)
   staat de dunne helft op +3.12% zonder drempel en +4.87% bij ≥3 (n=51 en 33); de
   dikke helft staat op −1.69% en +0.26% (n=51 en 21). Dat is dezelfde waarschuwing
   die `EDGE_ANALYSIS.md` al gaf over DLTH, nu over de hele steekproef.
3. **Uitvoering kostte niets en leverde iets op.** Over de negen afgeronde posities is
   het werkelijke rendement +7.18% tegen +4.57% theoretisch: +2.62 procentpunt
   verschil, t=1.27. Op het uur dat werkelijk gesloten werd is het verschil −2.09%
   (n=5), dus het positieve verschil komt uit het instapmoment en de uitstaptiming,
   niet uit betere fills. Bij n=9 zegt geen van beide iets.
4. **Meer tokens is geen beter rendement.** De proxy (tekens op schijf gedeeld door
   vier) geeft een helling van −10 procentpunt per 100k tokens met r²=0.10 over elf
   dagen. Dat is ruis, maar de meting loopt nu; `data/costs.csv` staat klaar voor
   echte tokenaantallen.

De gepoolde cijfers zijn onveranderd: ρ = −0.145 tegen −0.137 voor de gratis controle,
102 namen over 11 dagen, rekening +17.3% over acht sessies op negen posities. Het
nieuwe overzicht zet het boek samengesteld naast die controle: het boek loopt tien van
de elf dagen áchter en haalt hem pas op de laatste dag in.

**Read.** De drempel-per-sessie is het eerste dat het waard is om vooruit te testen, en
het is precies het soort splitsing dat op deze n vanzelf ontstaat. Niets veranderen aan
de config voordat er tien dagen bij zijn.
