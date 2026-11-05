# Stage EU — Europe ranking for 2026-11-06 (Fri)

I sealed the baselines on Thu 2026-11-05 at about 14:40 UTC (15:40 Amsterdam), roughly two
hours before the European close. Every sealed spot and every `run_up_20d_pct` is an
**intraday price, not a close**. The ranking key is `impact_sum`, read from the
`ranking_key` field of `edge-scores.json`. The conviction floor is 2.8.

**No name clears the floor.** The top of the ranking is ORK at +0.85 and the bottom is
HAYPP at −1.50.

- All twenty drawn names were hunted, and every hunt finished its search (`search_complete`).
- Eighteen names are ranked. Two have no event in the window:
  - **EGTX** released its Q3 a day early, on 11-05, together with a recommended cash bid.
  - **TRUE_B** is a phantom: it reported on 11-03.
- **The four-model panel selected three names, all short and each 4 of 4: TBCG, OUT1V and
  HAYPP.** Those are also three of the hunters' five most negative names.

This stage places no orders and reads no broker.

## Ranked

| # | ticker | market | session (checked) | impact_sum (key) | abs_move | p_up | impact_scaled | anchor | history | pre-released / guide change? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ORK | no | bmo (07:00 CET, NewsWeb notice) | +0.85 | 5.5 | 53 | +0.33 | no | observed_newsweb | India sub pre-released 4 Nov; no guide (CMD in Dec) |
| 2 | LOG | es | bmo? → bmo ("antes de apertura", 19 Oct filing) | +0.40 | 3.5 | 55 | +0.35 | no (no register) | estimated | first FY27 guide + dividend commitment |
| 3 | TES | it | bmo? → **in-session** (~12:40 CET) | +0.30 | 8.0 | 51 | +0.16 | no | estimated | no |
| 4 | ATT | se | bmo (07:00 CET) | +0.20 | 6.0 | 55 | +0.60 | no | estimated | no forecast given; buyback renewal likely |
| 5 | BMPS | it | bmo? → bmo (~07:40 CET pattern) | +0.15 | 1.6 | 51 | +0.03 | no | estimated | pinned by Intesa exchange offer |
| 6 | HEX | no | bmo (07:00 CET) | +0.10 | 8.5 | 52 | +0.34 | no | observed_newsweb | possible guide change either way |
| 7 | IAG | uk | bmo? → bmo (07:00 pattern) | +0.10 | 5.5 | 49 | −0.11 | no (**join miss**, see below) | observed_rns | fuel scenario likely revised |
| 8 | REC | uk | bmo (07:00) | +0.10 | 5.0 | 51 | +0.10 | no | observed_rns | **yes**, Q2 trading update 22 Oct |
| 9 | SCHO | dk | bmo? → bmo (08:00 pattern) | +0.10 | 5.5 | 54 | +0.44 | no (real near-zero at 0.1%) | estimated | **partly**: BioMar's raise public 2 Nov; group guide raise near-certain |
| 10 | PIA | it | bmo? → **in-session** (~12:35 CET) | +0.05 | 5.5 | 51 | +0.11 | no | estimated | no |
| 11 | SEA1 | no | bmo? → bmo (07:00 CET notice) | −0.10 | 4.5 | 52 | +0.18 | no | observed_newsweb | no |
| 12 | CLNX | es | bmo? → **amc 11-05** (same window) | −0.40 | 3.2 | 46 | −0.26 | no (no register) | estimated | possible "low end" wording; 2027 return package |
| 13 | DTG | de | bmo (07:00 CET) | −0.60 | 4.5 | 47 | −0.27 | no | estimated | Q3 units public 8 Oct; TNA unit-guide narrowing risk |
| 14 | GUBRA | dk | bmo? → bmo (07:30 pattern) | −0.80 | 5.5 | 47 | −0.33 | **yes** (1.34%) | estimated | CRO margin guide cut likely |
| 15 | TBCG | uk | bmo (07:00 GMT RNS) | −0.90 | 7.0 | 42 | −1.12 | no | observed_rns | Uzbek statutory Q3 loss already in local press |
| 16 | AMS | es | bmo (vendor + pattern; no timestamp) | −1.10 | 4.0 | 45 | −0.40 | no (no register) | estimated | guide pointed to low end / trim |
| 17 | OUT1V | fi | bmo (~09:00 EET) | −1.10 | 7.0 | 43 | −0.98 | no | estimated | **new Q4 guide** is the event |
| 18 | HAYPP | se | bmo (07:45 CET) | −1.50 | 6.0 | 45 | −0.60 | no | estimated | no |
| — | EGTX | se | release moved to **11-05 07:30** with ANI SEK 11.25 bid | not ranked | 0.5 | 50 | — | no | estimated | event out of window |
| — | TRUE_B | se | **phantom**: Q3 was 11-03, next print 2027-02-17 | not ranked | 2.5 | 50 | — | no | estimated | — |

`bmo?` marks a name sealed with `session_unresolved`. Each hunter settled its session in
`session_check`, from the issuer's own notice or its release-time history.

- **Two Italian names release during the session**: TES at about 12:40 CET and PIA at about
  12:35 CET. Both releases land inside the sealed close(11-05) → close(11-06) window, so
  that window holds the whole reaction.
- **CLNX releases after the Madrid close on 11-05.** The same window therefore starts after
  the release and is still the right one; an amc reading of 11-06 would score the wrong
  two days.
- **AMS** has no release timestamp. Its bmo rests on the vendor flag and its past pattern.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.**

- All four ran on their own `-intl-` agents with no fallback, and each covered 18 of 18 names.
- **Sonnet 5.5** opened none of the five hunter definitions the packs name; it judged from
  `config/hunter-core.md`, `LESSONS.md` and the packs. This repeats earlier days.
- **Opus 5.5** read the es definition in full and only the market sections of the other four.
- **Opus 5 and Fable 5.1** read all five.

The selection rule is `consensus_k` ≥ 3 of 4, each judge in its own top 20%. A judge's top
20% starts at: Opus 5 |1.28|, Opus 5.5 |0.84|, Sonnet 5.5 |0.70|, Fable 5.1 |0.90|. Each
threshold comes from that judge's last 200 live sizes in this market.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TBCG | bmo | **yes** | 98 | short | 2 | 98S* | 99S* | 94S* | 99S* | 4 | −2.52 | −0.90 |
| 2 | OUT1V | bmo | **yes** | 91 | short | 5 | 93S* | 95S* | 82S* | 94S* | 4 | −1.89 | −1.10 |
| 3 | HAYPP | bmo | **yes** | 91 | short | 6 | 93S* | 98S* | 81S* | 94S* | 4 | −1.84 | −1.50 |
| 4 | ATT | bmo | | 66 | long | 6 | 66L | 74L | 68L | 56L | 0 | +0.95 | +0.20 |
| 5 | AMS | bmo | | 61 | short | 4 | 56S | 58S | 68S | 61S | 0 | −0.82 | −1.10 |
| 6 | GUBRA | bmo? | | 48 | short | 13 | 29S | 47S | 52S | 66S | 0 | −0.66 | −0.80 |
| 7 | DTG | bmo | | 44 | short | 8 | 33S | 54S | 42S | 49S | 0 | −0.60 | −0.60 |
| 8 | LOG | bmo? | | 48 | long | 8 | 61L | 42L | 42L | 46L | 0 | +0.59 | +0.40 |
| 9 | SCHO | bmo? | | 39 | long | 26 | 12L | 62L | 68L | 14L | 0 | +0.54 | +0.10 |
| 10 | REC | bmo | | 44 | short | 12 | 63S | 46S | 35S | 33S | 0 | −0.51 | +0.10 |
| 11 | CLNX | bmo? | | 39 | short | 3 | 40S | 38S | 35S | 44S | 0 | −0.50 | −0.40 |
| 12 | ORK | bmo | | 29 | long | 8 | 28L | 20L | 25L | 42L | 0 | +0.37 | +0.85 |
| 13 | HEX | bmo | | 23 | long | 12 | 18L | 15L | 17L | 44L | 0 | +0.25 | +0.10 |
| 14 | SEA1 | bmo? | | 11 | long | 6 | 0- | 12L | 17L | 14L | 0 | +0.19 | −0.10 |
| 15 | IAG | bmo? | | 16 | short | 33 | 63S | 23L | 4L | 28S | 0 | −0.15 | +0.10 |
| 16 | PIA | bmo? | | 18 | long | 24 | 10L | 59L | 4L | 0- | 0 | +0.12 | +0.05 |
| 17 | BMPS | bmo? | | 5 | long | 2 | 2L | 4L | 7L | 6L | 0 | +0.08 | +0.15 |
| 18 | TES | bmo? | | 8 | long | 14 | 0- | 0- | 0- | 33L | 0 | +0.00 | +0.30 |

**TBCG (selected, short, 4 of 4, the tightest agreement of the day, sd 2).**
- **The evidence.** TBC Bank Uzbekistan's own statutory 9M statements came out on 30 Oct
  after the London close, in soum, with no London coverage. They show:
  - a Q3 net loss of 357.7bn soum (about GEL 80m), after an H1 profit of 288.1bn;
  - non-performing loans up from 10.4% to 13.4%;
  - the loan book down about 9% on the quarter;
  - implied Q3 provisions of about 556bn soum, against about 322bn a quarter in H1.

  This contradicts the August release's "stabilised and starting to return to growth". It
  is the same line that produced −11.9% on the Q3 2025 day and −4.2% on Q1 2026. The
  hunter's source is the UzDaily report of those statements.
- **The strongest case against.** Local accounts have diverged from IFRS before: in Q3 2025
  they showed a loss while IFRS Uzbekistan earned GEL 41m. Georgia is 95% of group
  earnings, and the snippet-only NBG data put its nine-month profit at +18%. TBCG also fell
  8.9% on 30 Oct for no cause the hunter found, so part of the Uzbek news may already be
  in the price.
- **Hunter versus panel.** The hunter's own key is −0.90; the panel read it 2–3× larger.

**OUT1V (selected, short, 4 of 4).**
- **The evidence.** Q3 is fenced at about EUR 100m adjusted EBITDA: the company's own July
  guide says "similar level" to Q2, and the consensus median is 100. So the move is in the
  Q4 guide, where consensus asks for 104. Four things point the other way:
  - Aperam on 6 Oct: European demand "unchanged at a low level", order books not improving
    (https://www.placera.se/pressmeddelanden/aperam-aperam-update-on-q3-2026-market-financial-trends-20261006);
  - Acerinox on 30 Oct: Q4 below Q3 on US year-end seasonality;
  - LME nickel down from $17,064/t (July average) to $15,240/t (30 Oct);
  - the last two Q4-guide days printed −9.3% and −7.6%.
- **The strongest case against.** Every input is a peer or a proxy. The stock is already
  down 20% over 60 days. And a "similar" Q4 guide against that weakness could be read as
  relief.

**HAYPP (selected, short, 4 of 4).**
- **The evidence.** Svensk Handel's survey of Swedish online nicotine and tobacco spending
  shows Q3 down 9% y/y, after +19% in Q2. In Q2 it tracked Haypp's Core segment (Sweden
  and Norway, about 70% of sales) closely. Yet the three-analyst consensus of 3 Nov moved
  UP, to sales +27.3% and adjusted EBIT 30 MSEK. Adjusted EBIT missed consensus in both
  2026 quarters, and the balance sheet tightened in Q2 (net debt 221.6 MSEK, cash 16.4 MSEK).
- **The strongest case against.**
  - The survey covers about 2,000 people a month, and its own method note flags larger
    uncertainty at category level.
  - It covers Sweden only, while the US/UK segment grows on an easy comparison.
  - Q2's EBIT miss rallied 6%.

**Where the panel and the hunters disagree most:**
- **REC**: hunter +0.10, panel short at 44. Opus 5 weighted the run into the print.
- **IAG**: hunter +0.10, panel split. Opus 5 is short at 63; Opus 5.5 and Sonnet 5.5 are long; sd 33.
- **SEA1**: hunter −0.10, panel slightly long. Both are noise.
- **ORK**: the hunters' top name at +0.85; the panel has it at only 29 long.

**What these numbers are not.**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed until this market has about 200
  panel names of its own.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but
  nothing about this market's panel is established.

## Top and bottom of the hunters' key

- **Top, ORK +0.85: ten small findings and no single driver.** The largest are four broker
  target and forecast cuts after the two 2026 misses (a lower bar, +0.3) and the NOK 4bn
  buyback, which buys about a quarter of daily turnover and runs through the print (+0.3).
  Against them sit FX (euro and krona about 7% weaker against the krone, −0.3) and Jotun's
  raw-material warning (−0.3). The event is Orkla's own NewsWeb invitation, msg 684677: 07:00
  CET on 6 Nov. The stock is up 8.9% in 20 days into the print.
- **Bottom, HAYPP −1.50.** The Svensk Handel −9% series is the largest finding at −1.0;
  the bar is Haypp's own Modular Finance consensus of 3 Nov. See the panel paragraph above.

## Not ranked

- **EGTX (Egetis).** The Q3 report came out on 2026-11-05 at 07:30 CET, a day ahead of the
  calendared 11-06. It was released alongside ANI Pharmaceuticals' recommended SEK 11.25
  cash offer (https://view.news.eu.nasdaq.com/view?id=b155f6f007fe4aef95600f54e1bedcd81&lang=en&src=listed).
  - 42.2% of shares carry irrevocable undertakings to accept.
  - ANI says it will not raise the price: "ANI kommer inte att höja priset i Erbjudandet"
    (ANI will not increase the price in the Offer).
  - The window holds only merger-arbitrage drift.

  **This is a release that moved out of its window, not a phantom row.** The resolver
  should find the release on 11-05.
- **TRUE_B (Truecaller).** The vendor's date is wrong. The Q3 interim came out on 2026-11-03
  at 07:30 CET, and the company's own calendar, in the Q3 PDF, puts the next report on
  2027-02-17. Nothing was filed on 11-04 or 11-05. This is a **phantom**.

## The day

**Universe.**
- Selection: `random sample of 27 eligible, seed 'eu-2026-11-06'`. 66 names were
  scheduled, 27 cleared the $100k turnover floor, and 20 were drawn at random among them.
- Drawn by market: uk 3, de 1, fr 0, se 4, dk 2, no 3, fi 1, it 3, es 3, pl 0.
- `market_concentration`: the largest market is se at 20%, and eight markets are
  represented. No single market dominates the day.

**Calendar sources.**
- Beyond the vendor, these rows were added:
  - the UK RNS crawler added RMV and NOG;
  - Yahoo's firm dates added IAG (uk), GUBRA (dk) and BMPS (it).
- Poland's issuer calendar (bankier) read `unavailable`.

**No option anchor.** `options` is null in all ten markets, so Europe runs in the
anchor-less regime: ρ=+0.073, p=0.45 over 104 events on the sealed corpus.

**Positioning.**
- The short registers resolved for uk, de, se, dk, no, fi and it. Spain has no register,
  and the Spanish names are AMS, CLNX and LOG.
- **Only 1 of 20 names carries `anchor_covered: true`: GUBRA (1.34%).** The rest are
  truncated zeros, or unreadable for Spain.
- Two register-join defects, neither of which revised a sealed baseline:
  - **IAG was a UK join miss.** The FCA register lists "INTERNATIONAL CONSOLIDATED AIRLINES
    GROUP, S.A." at 1.36% as of 02/11, and the baseline sealed 0.0. The likely cause is
    an issuer-name join on the ", S.A." suffix in `eu_positioning.py`.
  - The Danish join miss of 11-05 did not recur: the GUBRA and SCHO hunters checked the
    register by name and ISIN.

**Weak legs.**
- **3 names came from Spain (AMS, CLNX, LOG) and 0 from Poland.** These have no
  positioning anchor, so their lean is the run-up, which is also the free control. They
  also cannot be confirmed or killed after the fact.
- **1 name came from Germany (DTG)**, where `event_occurred: false` is unreachable as well.

**Lean against the free control.** The last resolved European run (2026-10-16) has
`lean_vs_free_control_rho` only for se (0.60 on 5 names); later runs are unresolved. The
lean's weights are priors borrowed from the US runs and measured nowhere in Europe.

**History basis.**
- **Estimated cadence, a scale and not a record of dates:** AMS, ATT, BMPS, CLNX, DTG,
  EGTX, GUBRA, HAYPP, LOG, OUT1V, PIA, SCHO, TES, TRUE_B.
- Observed: IAG, REC, TBCG (`observed_rns`) and HEX, ORK, SEA1 (`observed_newsweb`).
- Several hunters found the estimated reaction scale understates the real report-day moves:
  - ATT: observed median 4.66% against 2.33% estimated;
  - LOG: the real results days were all up, median +2.46%;
  - SCHO: median about 5% against 1.6%;
  - TBCG: its observed dates were also one or two days off.

**Below the floor.** No name sits above `conviction_floor` 2.8. Over the whole US sample
the sign was a coin flip below it.

**Release timing and the size of the move.**
- `already_public` is substantive on six names:
  - REC (Q2 update);
  - SCHO (BioMar raise);
  - ORK (India sub);
  - DTG (Q3 units);
  - BMPS (the offer pins it);
  - TBCG (the Uzbek statutory loss).
- `new_in_release` points to a likely guidance change on OUT1V, AMS, GUBRA, SCHO, IAG,
  LOG and DTG.
- On the first resolved days those two facts decided the size of the move while the
  emitted sizes barely differed.

**Release-time checks against the vendor.** The release moved out of the window for EGTX,
TRUE_B is a phantom, TES and PIA release in-session, and CLNX releases amc the day before.
A vendor session flag is a guess until a timestamp says otherwise.

**Interesting `language_note` lines.**
- OUT1V: the Finnish Inderes preview carried the only consensus table:
  "Myös konsensuksen Q4:n oikaistun käyttökatteen mediaaniennuste on 104 MEUR" (consensus's
  median Q4 adjusted EBITDA forecast is also 104 MEUR).
- AMS: a Spanish press misreport (El Debate, "guide maintained at +4.5% traffic") would have
  flipped the guidance read, and was rejected against the company's own release.
- TBCG: the decisive sources were Uzbek and Georgian press, not UK domestic ones.
- Nordic names mostly report "nothing the English sources did not already carry", as expected.

**Defects and process.**
- One curl from the ATT hunter, to a consensus widget, was refused by the auto-mode
  permission check. That is not a budget limit; `search_complete` stays true.
- The `pre_lessons` freeze ran on every hunt.

**One day is not a result.** Resolve within about a week (the Nordic feed window), so by
about 2026-11-13.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
