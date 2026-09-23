# Edge hunt — 2026-09-23 amc + 2026-09-24 bmo

**Ranking key: `impact_sum`**, as `edge-scores.json`'s own `ranking_key` field names it. It is
the hunters' signed per-finding sizes added up, in points of spot. This note has no call, no
threshold and no direction label.

8 names in the window (of 44 calendar rows). The sweep confirmed all 8 from company press
releases. 0 phantom rows, 0 sessions unsettled, 8 of 8 rankable. **1 name clears the
conviction floor of 3.0, and it cannot be traded.** The 29 `time-not-supplied` rows were
checked with `session_resolve.py`: EDGAR killed 3, press releases confirmed 0, and 26 were
carried unresolved. None was added.

## The ranked table

| # | ticker | session | event | pre-lessons | **post-lessons** (`impact_sum`) | V2 (grounded, % spot) | floor | tradable | control `-run_up_20d_pct` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SFIX | amc | 2026-09-23 | +2.30 | **+0.80** | +0.74 | – | yes, long, $4.60m/day, ok | +14.59 |
| 2 | BB | bmo | 2026-09-24 | +1.50 | **+0.50** | +0.53 | – | yes, long, $84.31m/day, ok | −9.11 |
| 3 | MITQ | bmo | 2026-09-24 | +0.20 | **+0.20** | −0.02 | – | **no**, $0.09m/day, below the $0.2m floor | −6.37 |
| 4 | DRI | bmo | 2026-09-24 | +0.20 | **+0.00** | +0.00 | – | yes, $229.88m/day, ok | +4.91 |
| 5 | FUL | amc | 2026-09-23 | +0.00 | **+0.00** | +0.00 | – | yes, $30.59m/day, ok | +13.71 |
| 6 | SNX | bmo | 2026-09-24 | +1.00 | **+0.00** | +0.00 | – | yes, $204.35m/day, ok | −20.61 |
| 7 | NEOV | amc | 2026-09-23 | −2.00 | **−1.50** | −4.63 | – | yes, short, Alpaca lends it, $5.51m/day, ok | −6.69 |
| 8 | UXIN | bmo | 2026-09-24 | −3.50 | **−3.00** | −3.63 | **yes** | **no**, $0.05m/day, below the $0.2m floor | +5.70 |

`alpaca_trade.py assets` generated the session and tradable columns. Borrow was checked live at
about 17:30 UTC. Pre-lessons and V2 sit beside the key as measurements and are not traded. V2
is calibrated today (170 ledger observations) and is compared forward only. Only
post-lessons places orders.

## Read this first: the day is mostly zeros, and the one conviction name cannot be bought

Six of the eight hunts came back at or near zero. DRI, FUL and SNX report no findings at all.
Each of those hunters had one lead: a Placer foot-traffic read on DRI, an Avery Dennison
pre-buy read-through on FUL, and a guide-conservatism beat pattern on SNX. Each dropped its
lead under `LESSONS.md` (narrow proxy, a finding already in the wire, the reaction function
overruling the fundamental read). SNX shows the gap most clearly. Its hunter expects revenue
about 4.5% above the bar (`print_vs_bar_pct` +4.5) and sizes the stock reaction at 0: the
last, larger beat-and-raise closed −1.97%, and the stock is up 20.6% in 20 days.

The lessons file moved 6 of 8 names, always toward zero or smaller. The day's sum of absolute
sizes went from 10.7 before lessons to 6.0 after.

**UXIN is the only floor-clearer, and it turns over about $50k a day**, a quarter of the
turnover floor. The strongest conviction of the day sits outside capacity again, as it did on
2026-09-10 (AENT, RENT) and 2026-09-22 (AYTU). **So today's traded book is empty.**

## The floor-clearer, read critically

### UXIN −3.00: not recommended, because it cannot be traded and its reaction history is rebuilt by hand

- **Lands on:** `guidance` −2.5 and `financing` −0.5. The guidance finding is arithmetic on
  the company's own numbers. The reaffirmed FY2026 target of ">100% retail volume growth"
  needs more than 102,220 units against a 51,110 FY2025 base. H1 comes to about 35k, so H2
  would need about 67k, at a Q2 run rate of about 18.5k and with no new superstore open since
  2026-03-31. So the Q3 guide should be well short of the pace the target needs. Source:
  https://www.sec.gov/Archives/edgar/data/0001729173/000149315226028826/ex99-1.htm. Guide
  deceleration is the line this stock has sold hardest (−10.4% on 2026-06-16), so this is the
  right line and not a one-off.
- **The hunter's two numbers point opposite ways, and `flags` records it:**
  `print_vs_bar_pct` +1.5 against `expected_move_pct` −2.0. That is coherent rather than an
  unresolved caveat. The quarter was guided with two weeks left and should land at the top of
  the range. The reaction is expected to come from the forward guide. The emitted −2.0 sits 1.0
  below the sum, because anyone could have done this arithmetic in June and the stock is down
  about 29% since.
- **Bar:** sourced to the company guide. No sell-side consensus exists.
- **Positioning:** 526k ADS short, 0.2% of shares outstanding. The 9.3 days to cover only
  reflects tiny turnover, so this is not a crowded short. There is no options market. A known
  buyer, the CEO's US$5M 10b5-1 plan, can start on 2026-09-28. That is after the exit, so it
  sits in `outside_window` at +1.0.
- **Baseline quality is the worst of the day (0.24).** The sealed reaction history came from
  monthly operational 6-Ks, which gave an 11-day "cadence". The hunter was told and rebuilt
  the history from five confirmed releases (median absolute move 8.5%, against the baseline's
  3.25%).
- **Flags:** a print/reaction sign split, and one finding worth +1.00 dated after the exit
  window, kept out of the key.
- **Verdict: not recommended, because it is untradeable.** On the research alone it would be
  "recommended with a named reservation", the reservation being that the evidence is
  arithmetic anyone could have done in June.

## What drives the other ends of the table

- **Top, SFIX +0.80, lands on `positioning`.** 11.9% of float short at 9.4 days to cover,
  and short interest *rose* 8.2% into the 2026-08-31 settlement. The stock hit a 52-week low
  on print day (−6.2%), and open interest runs 5:1 calls. So a clean beat carries squeeze
  fuel that a miss does not. Source: https://equibles.com/stocks/sfix/short-interest. What
  the price already says: a 21.6% implied move against a 10.5% median reaction, with no
  skew. The hunter kept the size small because the line that sank last year's Q4 print
  (−16.5%, negative year-on-year client growth) is guided negative again. This finding agrees
  with the free control (+14.59), so it is close to the control rather than beyond it.
- **Next to bottom, NEOV −1.50, lands on `guidance`.** Comparing the company's own releases
  side by side, the Pendergrass factory ramp slipped from "Q3 CY26, testing done by end of
  August" (2026-06-22) to "on track for Q4 CY26, testing underway" (2026-09-17). Meanwhile
  the only FY27 revenue consensus found ($102.29M, stockanalysis, single source) has not moved.
  Source:
  https://www.globenewswire.com/news-release/2026/09/17/3363986/0/en/neovolta-announces-capacity-reservation-agreement-with-infinite-grid-capital-ahead-of-pendergrass-facility-grand-opening.html.
  What the price already says: calls bid (skew −8.78) and a thin 22.75% implied move. The
  stock has already given back 4.6% since 09-17. V2 puts this name at −4.63, the largest
  grounded number of the day, because NEOV's realised volatility is high. V2 is not traded.

## Names that could not be ranked

None. All eight are rankable. MITQ is rankable but below the turnover floor, and its
baseline history was also flagged untrustworthy by the sweep (history dates do not match
its releases), so its hunter rebuilt the reaction base from confirmed release dates.

## What this note must also say

- **Order and sign are separate questions.** Below the floor the sign is a coin flip on the
  evidence so far: 53% over 38 events. Above it, the rank of conviction predicted whether
  the sign was right at ρ=+0.514 (+0.361 with the double-hunt inflation removed, which is the
  number to expect now). Seven of these eight names are below the floor. Reading SFIX's +0.8
  or NEOV's −1.5 as a view is reading the table wrong.
- **`impact_sum` is not a forecast of the move.** It ranks the names and does not size a
  position. Findings from two sources can repeat one fact and be counted twice.
- **The free control gets its own line.** `-run_up_20d_pct` ranks the day SFIX, FUL, UXIN,
  DRI, MITQ, NEOV, BB, SNX. Against the key, Spearman is **ρ = +0.10**, so the hunt's order
  is nearly orthogonal to the free control today. That is the opposite of 09-22 (ρ +0.857).
  The stage has still not been shown to beat that control on the pooled sample, and the
  control itself has stopped working on the larger sample (−0.42% per trade over 105 events).
- **Sign balance:** 3 names positive (SFIX, BB, MITQ), 3 at zero (DRI, FUL, SNX), 2 negative
  (NEOV, UXIN). Before lessons it was 5 positive, 1 at zero and 2 negative. No pessimism
  pattern today.
- **Nothing checked the findings.** There is no adversary pass and no second hunter, so a
  factually wrong finding enters the key at full size.
- **The key is not reproducible to better than its own size.** When the stage still ran two
  hunters per name, 12 paired names came back with a median gap of 2.40 points, and 4 of the
  12 had opposite signs. On a day where the largest non-floor number is 1.5, the order of
  rows 1 to 7 is inside that noise.
- **How much of the baseline was measured:** 6 of 8 names have a live option chain. UXIN and
  MITQ have none, so their lean falls back to −0.05 × run-up and their expected move is a
  historical median. Both of those also have sweep-flagged, untrustworthy reaction histories.
  Several chains are thin (FUL: 855 open interest, ATM spread 29% of mid; NEOV: 40% ATM
  spread). Their implied moves are indicative only.
- **What it would have cost to trade:** 6 of 8 names clear the $200k turnover floor, and all
  6 are `ok` on liquidity. The two that fail, UXIN and MITQ, are the name the key puts at the
  bottom and the name it puts third. **The only extreme that clears the floor is the
  untradeable one**, so today's ranking is a research result and not a signal.
- **One day is an anecdote.** Eight names cannot produce a meaningful rank correlation. The
  pooled figure across many days is the result.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
