# Performance log

Append-only. One dated section per update, written by the `edge-performance` skill.
Three things in every entry: what closed and what resolved, the pooled ranking figure
beside its free control, and one sentence of critical read.

## 2026-09-18 (later still) — a hypothesis register, and a verdict rule that bites

A `Hypotheses` tab, deliberately outside the `edge-performance` skill: a place to test,
not a step in a routine.

**Intermediate variables were screened before any hypothesis was named**, against three
outcomes that are not the same question — sign right, book return, move size. What came
back:

| variable | what it ranks |
| --- | --- |
| `priced_lean_pct` | the book, ρ +0.33 (p 0.017), and accuracy at ρ +0.23 (p 0.099) |
| `retail_tilt` | move SIZE only, ρ +0.32 (p 0.017) |
| `realised_vol_20d` | move size, ρ +0.27 (p 0.047) |
| `rank` | move size, ρ −0.28 (p 0.044) |
| everything else | nothing at the rough bar |

Three of those four rank the same thing — how far the stock went — which is volatility,
not skill, and they are one finding rather than three. The tab marks that column
explicitly for that reason.

**Ten hypotheses, one verdict rule.** The gap must carry the predicted sign and clear two
standard errors of its own difference. A first version used a flat 2pp bar and returned
*steun* for seven of nine on a book with a per-name sd of twelve; that is what a loose
rule does, and the rewrite is recorded on the tab rather than quietly swapped.

Surviving: **H4** one sector carries it (Consumer Cyclical 27 names, 70.4%, +5.97%
against Technology 48.3%, −1.89%), **H5** the hunt pays more where it agrees with the
price lean, **H6** the conviction floor — the anchor.

H5 is the uncomfortable one and it is written up as such: the stage is called "find what
the market has missed", so a variable saying it earns most where it *follows* the price
points the other way. It is the first thing to measure forward.

Not surviving, including two the operator expected: **H1** bmo over amc, and **H2a/H2b**
the amc-early / bmo-late exit split. Both exit tests are PAIRED — same names, two exits,
tested on the per-name difference, because two independent groups would put the whole
between-name spread into the standard error and never find anything. amc open-minus-close
is +1.88pp (16/28, t 0.93); bmo close-minus-open is +2.18pp (19/28, t 1.20). Both lean
the predicted way, neither clears the bar. Those are the two to watch, not to act on.

**Also found, and it is the one that would change a weighting rule if it holds**: the
conviction floor and `retail_tilt` interact rather than add. High tilt and above the
floor is 78.1% and +4.90%; high tilt below the floor is 38.1% and −3.66%; low tilt is
~46% either way. Four cells over 105 names is exactly the count at which an interaction
looks convincing without being it, and the tab says so under the table.

Nothing here should move a weight. Thirteen days, no multiplicity correction, and every
rule was chosen after seeing these days.

## 2026-09-18 (later) — fresh broker data, and the default exit is now the strategy's

Rebuilt against the broker rather than `--offline`: **12 closed positions, none open**,
against nine at the last build. Equity $10,000 → $11,582 (+15.8%). The pooled ranking
is unchanged at ρ = −0.142 against −0.139 for the free control.

**`strategie` is the default exit.** One horizon cannot describe this book, because the
two sessions are sold at different moments:

| session | CET | ET | field |
| --- | --- | --- | --- |
| amc | 15:30 | 09:30 | `mv_open`, the opening print |
| bmo | 20:00 | 14:00 | `hr_22` |

It is carried as if it were a horizon — `mv_strategy`, `ret_strategy`, `px.strategy`,
resolved per session in `attach_strategy_exit()` — so every tab reads it the same way
as the eight fixed ones, which stay in the list and can still be swept. Coverage is
107 of 107 names. On the conviction book it is **+3.69% per name against +3.19% at the
close**, so switching the default is not free of consequence: it changes the headline
figure on the landing screen.

**The page and the account now disagree by one hour, and that is worth resolving.**
`orders.exit_mode` is `amc_open` and its bmo leg goes at plain market on stage E's own
13:05 ET run — 19:05 CET, not 20:00. On the 28 bmo names above the floor: +4.24% at
19:05, +4.36% at 20:00, +5.22% at the close. Monotonic, so the live config is the worst
of the three and the default now shown is the middle one. Neither gap is large against
the spread on these names.

## 2026-09-18 — moved to the top level, and four tabs

`edge/performance/` is now `dashboard/`, because the file you open should not be four
directories deep. Nothing about the build changed beyond the paths.

Four tabs, all recomputed from the filtered rows rather than from a frozen summary, so
each one moves with the lens, the exit horizon, the threshold, the period and the
session filter like everything else on the page.

- **Instap** — the entry side of the clock. `Timing` moves the exit with the entry
  fixed at the 22:00 CET close; this moves the entry with the exit fixed at whichever
  horizon is selected. New per-name field `enpx`: the entry-day price at every half
  hour of the regular session. On the current sample it does not matter — about half a
  point between the best and the worst entry of six hours, against a per-name standard
  deviation near 13 — and the unsigned drift to the close is flat at every hour, which
  is why. Reguliere sessie alleen: a pre/post bar from this source carries no volume.
- **Aanloop** — new fields `runup_2d/5d/10d/20d`, measured to the **20:00 CET bar**
  and not to the close, because the two hours after it are on the wrong side of the
  decision they are supposed to inform. Neither question comes back with anything: no
  |ρ| above 0.07 against whether the sign was right, and the agreement result flips
  sign between the full sample and the traded book. Two subsets of one dataset pointing
  opposite ways is noise measured twice, and the tab says so where the reader is.
- **Zoekvolume** — new fields `search_spike`, `search_level`, `search_state`, attached
  from `edge/scripts/edge_search_volume.py`. The one lead in the set: above the
  conviction floor a larger search spike goes with a worse outcome, and the
  high-attention names also move least. Two things keep it a lead rather than a
  finding — it is one cell of ten looked at, and half the book is below Google's
  reporting threshold, so the measurable half is systematically the liquid half and
  says nothing about the names this stage most often trades.
- **Agenda** — the forward week from `edge/scripts/edge_calendar.py`, with the session
  gate and the liquidity floor counted separately rather than folded together, so the
  candidate count is honest. The ledger drops it once it is more than three days old:
  a stale list of what is coming is a list of what already came.

The first run of the search script was wrong in a way worth keeping written down. Each
Trends series is normalised to its OWN maximum, so a name searched on three days out of
ninety reads 0…0,100, and a spike over a zero median came out at 100×. Eleven such
names filled the top tercile and the correlation looked strong. A series now needs a
non-zero median to be scored at all, which took the sample from 95 "measurable" names
to 47 real ones.

`update.sh` runs both feeders before the ledger; either may fail without costing the
rebuild, and `--no-feeders` skips them.

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

## 2026-09-17 — lopende dag zichtbaar, drie rendementsniveaus, positiecap

De 09-16 run stond nergens in: hij wordt afgewikkeld tegen de slotkoers van vandaag en
`edge_exit.py` weigert een horizon die nog niet bestaat, dus vielen alle vier de namen uit
de ledger en stopte elke grafiek een dag te vroeg zonder dat iets zei waarom.
`build_ledger.py` maakt daar nu een **pending-rij** van met de momenten die wél bestaan.
Stand vanochtend, voorbeurs: ALMU −16.6% (short, dus in het voordeel), LEN −2.6%,
IPHA −2.0%. Op `close` hebben ze nog geen rendement en tellen ze nergens in mee; het
overzicht noemt ze bij naam in plaats van de lijn te laten eindigen.

**Drie rendementen staan nu naast elkaar, want ze zijn niet hetzelfde.** Over de elf
afgewikkelde dagen, gelijk gewogen: per naam +0.71% met een standaarddeviatie van 13.1
(slechtste −42.4%, beste +34.5%), per dag +1.15% met sd 5.2, en samengesteld over de
periode +11.90%. De rekening zelf deed +12.9%. De spreiding is het verhaal: de sd per
naam is achttien keer het gemiddelde, en zonder de grootste enkele uitslag (FEIM −42.4%,
een short die won) zakt het gemiddelde van +0.71% naar +1.14%… omhoog, want die uitslag
zat in het voordeel van het boek.

**De positiecap doet op deze steekproef bijna niets, en dat is zelf de bevinding.**
Nagerekend over dezelfde dagen: gelijk gewogen +11.90%, cap 50% +11.90%, cap 33% +11.90%,
cap 20% +10.85%. Bij 33% bindt het plafond pas onder drie namen per dag en de dunste dag
had er vier; bij 20% bindt het op elke dag met vier namen en kost het ruim een
procentpunt. Met de drempel aan zakt het aantal namen per dag hard en gaat het plafond
wél knellen — dat is precies de combinatie om vooruit in de gaten te houden, want de
config ging op 2026-09-17 van 20% naar 33%.

**De consumentenkanteling per sector zegt niets over rendement, en dat is nuttig om te
weten.** Er is geen gratis eigendomsbron, dus het is een proxy uit vier percentielen
(churn over marktkap, kleine kap, lage koers, vol). Communication Services (58), Consumer
Defensive (64) en Basic Materials (80, n=1) staan het hoogst, Healthcare (34) en
Industrials (42) het laagst. Tegen het rendement uitgezet over 102 namen: helling 0.04,
r² 0.00. De edge zit dus niet zichtbaar in de namen waar consumenten handelen — maar de
indicator is er nu, dus als dat kantelt is het te zien.

**Read.** Niets aan de gepoolde cijfers veranderd. Wat erbij kwam is het vermogen om
vragen te stellen: periode, drempel, verhandelbaarheid, positiecap, sessie en sector
leiden nu elk getal op de pagina opnieuw af, en de lopende dag is niet langer onzichtbaar.
