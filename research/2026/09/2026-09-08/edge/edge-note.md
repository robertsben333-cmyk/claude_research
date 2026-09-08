# Edge hunt — 2026-09-08 amc + 2026-09-09 bmo

**One signed number per company, so the day can be ranked.** There is no call, no
threshold and no direction label anywhere below. `edge_score` is a **ranking key** on
−100…+100, not a forecast of a percentage move.

24 names in the window · 23 confirmed by a company source · **0 phantoms** · 8 hunted
and rankable · 16 not ranked, all for budget, all listed with their reason.

## The ranking

| # | Ticker | Company | Session | edge_score | edge_pct | conf | unc% | baseline | eIM |
|---|--------|---------|---------|-----------:|---------:|-----:|-----:|----------|----:|
| 1 | TTAN | ServiceTitan | 09-08 amc | **+7.7** | +0.39 | 32.5 | 0.19 | measured | 10.1% |
| 2 | CNM | Core & Main | 09-09 bmo | **+7.2** | +0.36 | 20.8 | 0.18 | measured | 9.2% |
| 3 | SUNB | Sunbelt Rentals | 09-09 bmo | **−2.8** | −0.14 | 12.1 | 0.07 | measured | 9.8% |
| 4 | SIG | Signet Jewelers | 09-09 bmo | **−4.1** | −0.20 | 29.2 | 0.10 | measured | 10.1% |
| 5 | INNV | InnovAge | 09-08 amc | **−6.5** | −0.32 | 12.0 | 0.16 | inferred | — |
| 6 | NNOX | Nano-X Imaging | 09-09 bmo | **−13.1** | −0.66 | 11.5 | 0.33 | inferred | — |
| 7 | ODD | ODDITY Tech | 09-09 bmo | **−15.9** | −0.80 | 28.7 | 0.40 | measured | 20.7% |
| 8 | YQ | 17 Education | 09-08 amc | **−31.9** | −1.65 | 10.6 | 0.83 | inferred | — |

Eight names, eight distinct scores, a strict order. `edge_pct` is the residual in
points of spot after the adversary discount; `eIM` is the option-implied move for the
event where a chain existed.

### Read the spread before you read the order

The whole table spans **+0.39 to −1.65 points of spot** — against implied moves of
9.2%, 9.8%, 10.1%, 10.1% and 20.7% on the five names where the market actually quoted
one. Nobody should read `edge_score −31.9` as a forecast of a −31.9% move, or even of
a −1.65% one with any confidence. What the number says is "last of eight".

The compression does not weaken the test. Rank correlation reads order, not magnitude,
so a tightly compressed but strictly ordered table is exactly as falsifiable as a wide
one. The spread is wider than 2026-08-31's (+0.04 to −0.58), but that is two days, not
a trend.

## What drives the top and the bottom

**Top — TTAN, +7.7.** Three primary series say the US residential trades market
strengthened *inside* the exact fiscal quarter being reported (1 May – 31 July 2026):
July 2026 was the warmest month in the 131-year contiguous-US record, all 48 states
above their 20th-century average — [NOAA NCEI, 2026-08-10](https://www.ncei.noaa.gov/news/national-climate-202607).
Record cooling load drives the emergency HVAC service calls that flow through Gross
Transaction Volume and the payments take-rate. Corroborated by BLS JOLTS construction
hires at 366,000 in July, +9.9% y/y, and by AHRI June shipments +21.7% y/y against
Lennox's weaker company-specific print.

*What the price says:* the opposite. The chain pays 5.14 vol points more for downside
than upside (`priced_direction_lean: downside paid`), the stock is 29% below its
52-week high, and it fell 13.7% in the five sessions into the print. This is the one
name where the finding and the priced lean point in genuinely opposite directions on a
tightly-quoted chain (ATM bid-ask 17% of mid — the best-measured baseline of the day).

**Bottom — YQ, −31.9.** The +42.5% twenty-day and +74% five-day run-in rests on three
documents that contain no new economics, and the least-priced finding of the entire day
is the reason: deferred revenue and customer advances fell from RMB165.9m to RMB104.5m
across Q1, so **RMB61.4m of the RMB99.5m of revenue behind the "+359% y/y" headline was
a drawdown of pre-sale orders**, while cash fell RMB54.6m against a reported net loss of
RMB19.4m — [Q1 6-K exhibit, 2026-06-17](https://www.sec.gov/Archives/edgar/data/0001821468/000119312526273326/yq-ex99_1.htm).
Both isolated hunters found this independently, from partly different filings, and the
adversary scored it 30 and 32 — the two lowest priced-in numbers of 34 findings.

*What the price says:* there is no option chain at all, so "what is priced" here is only
the run-up, and the run-up is the thing being contradicted. This is also the one name
where the score *agrees* with the priced lean rather than cutting against it.

## Sign balance

Six of eight rankable names scored negative. At hunter level, 3 of 10 hunts leaned
positive (TTAN, CNM, INNV) and 7 leaned negative.

**This is the second consecutive run at six-of-eight negative**, and it is more
plausibly an artefact of asking hunters to find what the market has missed *into a
print* than a fact about these eight companies. If it recurs, the hunter prompt is
generating pessimism rather than detecting it. Recorded here so the count is poolable.

## What the adversary broke

Median `priced_in_pct` across all 34 findings was **73** — the pass again left very
little standing, which is why the residuals are small.

**Refuted on the facts, not merely priced:**

- **SIG#1 → 90.** The hunter claimed a 15% Section 122 global surcharge expired
  2026-07-24 and was replaced by 10–12.5% Section 301 duties, a 2.5–5 point step down
  on India. The adversary established from the 2026-02-20 White House proclamation that
  the Section 122 surcharge was **10%, not 15%**, and that India is 10% under Section
  301 — so there is no step down at all. The finding's premise is wrong.
- **ODD-a#2.** The hunter's rebuild of which of ODDITY's eight recorded "prints" are
  real earnings called the 2026-06-12 6-K a proxy statement. EDGAR says it is the
  $50m exchangeable-note repurchase — which is what the *other*, isolated ODD hunter
  independently filed as its own finding.
- **YQ-a#0.** The claim that the expiring buyback programme ended "four days before"
  the new one started is backwards: the prior programme ran to 2026-09-04, one day
  *after* the new authorisation. The recurrence pattern itself survived (scored 35).
- **YQ-b#2.** The 10b5-1 plan is disclosed in Item 3 of the 13D/A, not Item 6.
- **SUNB#0 → 61.** Treasury-share endpoints verified correct, but the headline "85%
  collapse" is a peak-week-to-trough-week artefact, and "monotonically decaying" is
  refuted by the hunter's own cited notice showing 47,000 shares for 31 Aug–4 Sep. The
  real step-down dates to the 1 May Reliant close, disclosed 23 June.

**Conceded on the facts but refused on the sign** — a different and weaker verdict:

- **CNM#0 → 68.** The adversary pulled BLS series WPU072106038 itself and reports every
  figure reconciles exactly: the plastics water-main pipe PPI did turn y/y positive
  inside CNM's fiscal Q2. It is discounted because the CFO pre-stated that shape on
  2026-06-10 and put the benefit in FQ3, not because the data is wrong.
- **INNV#0 → 70.** The implied-Q4 arithmetic was verified correct against primary
  filings. Discounted because consensus already sits at the top of the implied range,
  and the identical setup a year earlier paid −2.81% on a beat.

**Survived best:** YQ's deferred-revenue drawdown at **30**, then the same finding from
the other hunter at 32, then YQ's buyback-recycling at 38.

**Most priced:** CNM#2 (July housing starts, 93), NNOX#2 (the corrected earnings
history, 91), SIG#1 (90, and refuted above).

**One adversary adjudicated a hunter disagreement.** The two isolated ODD hunters read
the same options evidence in opposite directions — one as a crowded short book buying
call protection, the other as size sold to dealers leaving the downside tail unhedged.
The adversary found 24,012 puts traded against 4 calls on the day the skew inverted,
which supports the second reading.

## How much of the baseline was measured

**Five of the eight ranked names carry a live option chain** and therefore a measured
statement of what the market priced: TTAN, CNM, SUNB, SIG, ODD. Across the full 24-name
universe, 12 had a live chain and 9 a usable event-implied move.

That is a large improvement on 2026-08-31, where seven of ten names had no listed
options and `priced_lean_pct` fell back to −0.05 × the 20-day run-up. **The 10:04 New
York fire time is why** — half an hour into the session, chains are two-sided. ATM
spreads came in at 17% of mid on TTAN and 17% on SAIL, against 41% of mid on a weekend
mark in the earlier run.

For the three inferred names — INNV, NNOX, YQ — `priced_lean_pct` is still a function
of the run-up, so the agreement discount fires against a lean that is much weaker
evidence than the rule assumes. Two of those three sit at the bottom of the table, and
that is worth holding in mind before reading their position as information. Even among
the measured five, four carry a spread warning (SIG 65% of mid, CNM 72%, SUNB 46%,
ODD 42%), so their implied moves are indicative rather than firm.

## Names that could not be ranked

All 16 sit in `edge-scores.json` with `rankable: false`. The reasons:

**Unconfirmed event (1).** **CRMT** — the only name of 24 the sweep could not confirm.
America's Car-Mart pre-announces every print by GlobeNewswire 7–14 days ahead and has
not; EDGAR carries no scheduling 8-K; three vendors carry three different date/session
combinations, one of them 2026-09-17; and its previous print already slipped a month.
Its baseline verdict was amended `fits_cadence → suspect` this morning.

**No priced-in baseline exists (1).** **JMKE** — Jersey Mike's IPO'd in 2026, so
`priced_in.py` produced no baseline at all: 28 usable price bars, no options, no
reaction history. The event *is* company-confirmed for 2026-09-09 bmo and its
hunt_priority was 79.4, second-highest of the day. But "is this already priced" is
unanswerable with nothing to price it against, so it was dropped rather than hunted
against a baseline that does not exist.

**Budget (14).** The `edge_hunt` cap is 20 subagents for the whole stage and the run
spent 19 (1 sweep + 10 hunters + 8 adversaries). Not hunted, by hunt_priority: AVO 66.9,
MIND 65.4, CGNT 63.7, DXLG 61.2, PPIH 59.6, OCC 57.3, CAL 54.8, JILL 52.1, KFY 49.7,
SAIL 42.4, ASO 40.8, BRZE 38.2, CHWY 29.6, CASY 21.4.

The selection deviated from straight hunt_priority order, deliberately and recorded in
the run log: the top 4 were taken unconditionally, then the remaining 4 slots went to
the highest-priority names carrying a *measured* option-implied move. A straight top-8
would have had only 2 of 8 measured baselines. The visible cost is that SAIL — priority
42.4 but the joint-tightest chain of the day at 17% of mid — went unhunted.

## One day is an anecdote

Eight names cannot produce a meaningful rank correlation. Nothing in this note is a
result. The falsification test is `scripts/edge_resolve.py`, which reports Spearman
rank correlation against the realised move — raw and normalised by the implied move —
with a permutation p-value, and the number that matters is the one pooled across many
days:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-08/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'
```

The normalised correlation is the skill measure. Sorting a 20.7%-implied ODD above a
9.2%-implied CNM is easy and means nothing on its own.

Two sessions carry these eight names. TTAN, INNV and YQ release after today's close;
CNM, SUNB, SIG, NNOX and ODD release before tomorrow's open. `edge_resolve.py` measures
the move over the session recorded in each baseline, and every one of the eight has a
company-sourced release hour.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
