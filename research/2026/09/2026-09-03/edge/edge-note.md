# Edge hunt — 2026-09-03 `amc` + 2026-09-04 `bmo`

**One signed number per company, so the day can be ranked.** No call, no threshold, no
direction label. Sort on `edge_score` and cut wherever you like; the cut is the reader's.

Sealed at 14:08 UTC, hunted 14:20–15:40 UTC, scored 15:05 UTC. Releases land 20:00 UTC.

## The ranking

| # | Ticker | `edge_score` | `edge_pct` | conf | unc | qual | clusters | price lean | chain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SWBI | **+20.8** | +1.05 | 41.3 | 0.53 | 0.79 | 5 | +0.44% | measured |
| 2 | ASAN | **+12.3** | +0.62 | 44.7 | 0.31 | 0.93 | 3 | −4.76% | measured |
| 3 | MAMA | **+10.9** | +0.55 | 14.8 | 0.27 | 0.26 | 4 | +0.79% | inferred |
| 4 | AMBA | **+0.1** | +0.00 | 16.5 | 0.68 | 0.40 | 3 | +1.00% | inferred |
| 5 | DOMO | **−7.1** | −0.35 | 5.7 | 0.18 | 0.40 | 1 | −0.02% | none |
| 6 | LULU | **−7.2** | −0.36 | 26.5 | 0.18 | 0.95 | 3 | +13.10% | measured |
| 7 | NX | **−23.3** | −1.19 | 14.7 | 0.59 | 0.40 | 2 | +0.50% | inferred |
| 8 | PL | **−32.5** | −1.68 | 29.0 | 0.84 | 0.58 | 3 | +0.81% | inferred |

**Not rankable (13):** AOUT, BBCP, CURV, DOCU, EGAN, GROW, GWRE, IOT, KNOP, LND, OXM,
PATH, ZS — every one for the same reason, `no hunt`, and none because its event was in
doubt. See *What was shed* below.

### Read the score as a ranking key, not a forecast

`edge_score −32.5` on PL does **not** mean "PL down 32.5%". It means *last of eight*.
The underlying residuals span **+1.05 to −1.68 points of spot** — a 2.73-point spread —
against option-implied moves of 18.2% (PL), 14.4% (AMBA, ASAN), 13.2% (SWBI), 12.3% (NX)
and 9.4% (LULU, MAMA). Every name's residual is an order of magnitude smaller than its
own implied move, which is what an honest adversary pass does to a day's findings.

Compression does not weaken the test. Rank correlation reads order, not magnitude, so a
tightly compressed but **strictly ordered** table is exactly as falsifiable as a wide
one. All eight scores are distinct and there are no ties, so the ordering is testable at
every k. For reference, the 2026-08-31 run spanned 0.62 points across eight names; this
one spans 2.73, so the order is less likely to be an artefact of rounding — but that is a
statement about resolution, not about accuracy.

**One day is an anecdote.** Eight names cannot produce a meaningful rank correlation.
Nothing here should be read as a result. The number that matters is the pooled Spearman
across many days from `scripts/edge_resolve.py --pool`, and until many days have
accumulated this stage is not established as better than anything.

## What drives the top and the bottom

### Top: SWBI (+20.8)

Two isolated hunters **converged** on this name (+5.0 and +4.5), both independently
deriving the same arithmetic: SWBI's 2026-06-17 guide of Q1 revenue +15–20% was set when
only May adjusted NICS (+3.2% y/y) had published; June (+11.7%) and July (+8.5%) landed
afterwards, taking the quarter-aligned May–July industry figure to **+7.70% y/y**
(3,290,647 vs 3,055,402) — a 6.5-point acceleration on the +1.20% backdrop against which
the company printed revenue +26.7% last quarter.

- Driver (`SWBI-b#0`, adversary 50% priced, residual **+1.75**) —
  https://www.theoutdoorwire.com/releases/2026/07/nssf-adjusted-nics-background-checks-for-june-2026/
- Same series, other hunter (`SWBI-a#0`, 58% priced, +1.47) —
  https://raw.githubusercontent.com/bobsut/NSSF-Adjusted-background-checks/main/data/nssf-adjusted-nics.csv

**What the price already says:** the opposite. SWBI is −16.35% over 20 sessions and
−26.2% off its 52-week high, with the 25-delta skew at −0.67 (calls marginally bid) and
put/call OI 0.70 — i.e. the options market has taken essentially *no* directional view
while the equity de-rated. Both hunters flagged that they could not source a cause for
the decline, and that is the honest cap on this name. The adversary made it sharper (see
below).

### Bottom: PL (−32.5)

- Driver (`PL#0`, adversary 55% priced, residual **−2.14**): remaining performance
  obligations fell sequentially, $852.4M at 2026-01-31 to $816.0M at 2026-04-30 — a
  $36.4M decline against $94.2M of revenue recognised — while Planet reports RPO only as
  a YoY percentage, so the sequential figure must be differenced by hand across two
  releases. https://www.tradingview.com/news/tradingview:709103f111d6b:0-planet-labs-delivers-record-fy26-revenue-307-7m-backlog-900m-fy26-adj-ebitda-15-5m/
- Second (`PL#1`, 50% priced, −1.75): Planet's own Q3 FY26 release states the NRO renewed
  its baseline EOCL contract for $13.2M *"through June 2026"* — the anchor US
  intelligence contract expired inside the quarter just reported, with no renewal
  announced since. https://www.businesswire.com/news/home/20251210070707/en/Planet-Reports-Financial-Results-for-Third-Quarter-of-Fiscal-Year-2026

**What the price already says:** PL is −62.9% from its high and −16.1% over 20 sessions,
so a great deal of bearishness is already in. There is **no 25-delta skew** for this name
and put/call OI is call-heavy at 0.59, so the option book offers no directional statement
to be on the wrong side of. The striking baseline fact is not direction but variance: the
18.23% implied move sits well below the 25.98% median of the last seven reactions.

## What the adversary broke

The pass judged **all 33 findings on both sides** — `edge_brief.py --check` reports
`JOIN CLEAN`, every finding carrying a number, no orphan verdicts and no silent drops.
Mean `priced_in_pct` 65.7, median 64.0, range 42–90. Not one finding survived below 42%
priced, which is why the whole table compresses into under three points.

**Factually broken.** The PL adversary refuted a limb of the day's largest single claim.
`PL#0` asserted the quarter contained "no announced nine-figure booking at all, only two
seven-figure deals" — but NGA exercised a **$22M Luno B option year** on 2026-06-04,
inside the window, press-released and carried by trade press
(https://www.satellitetoday.com/government-military/2026/06/04/nga-awards-planet-22m-luno-b-option-for-maritime-domain-awareness/).
The adversary also noted the hunter selected the one book metric that fell (RPO) while
backlog *rose* $900M→$906M over the same quarter. The claim was priced up on that basis
rather than discarded, because the sequential-RPO fact itself stands.

**Misdated sources caught.** `SWBI-b#0` cites the Outdoor Wire URL path `/releases/2026/07/`
— the June release, published 2026-07-06 — as source for a July datapoint that did not
publish until the `/releases/2026/08/` release. The claim's substance survives (the July
figure is real and the adversary supplied the correct URL) but its citation was wrong.
Separately, three hunters independently reported discarding year-relabelled search
results: SWBI-b caught an SGB "adjusted NICS +4.0% in July" article that is dated
**2024-08-06** — and which the sweep row had itself cited as a 2026 source — plus a 2018
Sportsman's Warehouse piece and a 2024 Yahoo item; ASAN's hunter caught two previews
quoting FY2026 figures as FY2027; LULU's caught a PFAS headline resolving to an April
investigation; PL's caught a €240M German satellite deal that is 2025-07-01. The
URL-path rule is earning its place in the skill.

**Conceded but refused.** The distinction the skill asks to preserve shows up cleanly on
SWBI. The adversary did not dispute a single one of the seven bullish facts. It attacked
the *inference*, and did so with a fact neither hunter had: over 2026-08-19 to 2026-09-03,
**RGR was flat ($38.20 → $38.32) while SWBI fell 11.7%**. So the market had every
bullish datapoint during exactly the window it de-rated the stock, and the
underperformance is idiosyncratic rather than sectoral — evidence of a SWBI-specific
negative that none of the eight claims addresses. That is a stronger objection than
refuting any individual claim would have been, and it is why SWBI's confidence is 41.3
rather than higher despite five independent source clusters.

**Survived best.** `MAMA#2` at **42% priced** — $94m raised at $18.00 on 2026-06-30
explicitly to fund "the acquisition of businesses or other assets", no 8-K item 1.01/2.01
filed in the two months since, and the company has form for announcing deals into this
exact calendar slot (the Crown I asset purchase, 8-K dated 2025-09-02, six days before
last year's Q2 print, +14.4% that day). The adversary sized it at **+6.0 points against
the hunter's +3.5** — the largest hunter-vs-adversary size disagreement of the run, and
one where the adversary was the *more* bullish party.

**Most dismissed.** `ASAN#4` and `PL#2`, both at 90%: respectively "trades above the
sell-side average target after a run-up" and "FY27 EBITDA guided below last year's
actual". Both are restatements of published guidance or published targets, correctly
priced as such.

**Where the two sides disagreed most on magnitude** (the scorer averages them, so the
disagreement is absorbed rather than discarded): MAMA#2 5.0 points, NX#1 4.0, DOMO#1 3.1,
MAMA#1 3.0, PL#1 3.0.

## The two-hunter split, and what it bought

Only **AMBA** produced hunter disagreement, and it produced a lot: **+2.0 against −4.0**
from the same sealed baseline, the same 10-Q and the same reported takeover story. The
two read one fact in opposite directions — the stock's −20.1% 20-day drawdown is the
round-trip of a 31 July NXP takeover-rumour spike, leaving it 5.4% *below* the last
undisturbed pre-rumour close with no report anywhere that the talks ended:

- Hunter A: this removes the "washed-out, low bar" premise a reader would take from the
  baseline's run-up field, so the standard oversold-bounce setup is not there.
- Hunter B: the erased premium means the market prices deal probability at ~zero, so the
  left tail is self-limiting and there is an unpriced right tail into the first
  management commentary in five weeks.

Both are defensible readings of one fact, and neither could see the other. The result is
`hunter_dispersion_pct` 0.68 — the highest of the eight — which flows into AMBA's
uncertainty (0.68) rather than into a gate, and lands AMBA at `edge_score +0.1`,
essentially the middle of the table. **That is the split working as designed:** two
opposite views on one name resolve to "no rankable edge here", with the disagreement
recorded as uncertainty instead of averaged away silently.

SWBI's split did the opposite and is equally informative: two hunters, independent,
converged to within 0.5 points and to the same primary series. Dispersion 0.38.

## Sign balance

**6 of 10 hunts leaned positive, 4 negative** — SWBI-a +5.0, SWBI-b +4.5, MAMA +3.0,
AMBA-a +2.0, ASAN +2.0, DOMO +1.0 against NX −3.5, PL −3.0, LULU −3.0, AMBA-b −4.0. By
name it is 4 positive, 3 negative and one split.

This is worth recording because it **reverses** 2026-08-31, when six of eight leaned
negative and the note flagged that as more plausibly an artefact of asking hunters to
find what the market has missed into a print than a fact about those companies. One day
in each direction is not a pattern. The count is only interpretable pooled across many
days, and it is only poolable because each note records it.

## How much of the baseline was measured, not inferred

This is the most improved part of the run and also the place where a raw count would
mislead, so both figures belong here.

- **Universe:** 12 of 21 names carried a quoted front-expiry straddle.
- **Hunted set:** 7 of 8 carried a quoted implied move (all but DOMO).
- **But only 3 of 8 — SWBI, ASAN, LULU — carry a 25-delta skew.**

That last figure is the one that matters, because `priced_lean_pct` is computed from skew
when it exists and otherwise falls back to −0.05 × the 20-day run-up. So for **five of
eight** ranked names the agreement discount fired against a lean *inferred from a price
run-up*, which is much weaker evidence of what is priced than the rule assumes. Against
2026-08-31, where seven of ten had no listed options at all, three measured leans out of
eight is a real improvement — but "12 names with a chain" overstates it and should not be
quoted alone.

Chain quality within the hunted set varies enormously and the scorer handles it correctly
via `opt_q = 1 − spread/0.6`:

| Ticker | ATM spread / mid | Total OI | `q_opt` |
| --- | --- | --- | --- |
| LULU | 9.0% | 34,908 | 0.85 |
| ASAN | 11.8% | 19,494 | 0.80 |
| PL | 29.2% | 37,644 | 0.51 |
| SWBI | 36.4% | 5,452 | 0.39 |
| MAMA | 55.3% | 526 | 0.08 |
| AMBA | 68.7% | 5,641 | 0.00 |
| NX | 73.7% | 199 | 0.00 |
| DOMO | no chain | 201 | 0.00 |

NX and AMBA have technically live chains that are effectively dead — 199 contracts at a
74%-of-mid spread for NX — and both adversaries were told explicitly not to appeal to
"the options market already says this". Both complied and reasoned from reaction history
and the coverage gap instead.

**The 16:04 Amsterdam firing did its job.** ZS's ATM spread is 9% of mid against 41% on
the first run's stale weekend marks, and LULU's is 9.0% with 34,908 contracts of open
interest. Sealing the baseline half an hour into a live two-sided session is the reason
three names have a usable skew at all.

## What was shed, and why

21 confirmed names against an `edge_hunt` cap of 20 subagents. **8 hunted, 13 shed.**
Step 1 of `budget.edge_degrade_order` (`drop_unconfirmed_names_first`) had nothing to
shed, because the sweep confirmed all 21, so the shed ran entirely on step 2
(`drop_lowest_hunt_priority_names`). Rigour was never reduced on a kept name: the
two-hunter split and full adversary coverage of every finding on both sides are in
`budget.edge_never_degrade` and neither was touched.

The 13 shed names are **not filtered out of `edge-scores.json`** — they sit in the table
as `rankable: false` with `not_rankable_because: "no hunt"`, which is the visible loss the
skill prefers to keeping a name and measuring it worse.

**One deliberate deviation from the sweep's ordering:** NX (`hunt_priority` 56, live
chain) was hunted in place of CURV (59, no chain). Three priority points traded for a
baseline where what the market priced is measured rather than inferred. Recorded here and
in the run log because it is a judgement call, not a rule.

**One override deliberately declined.** GWRE (49) has the most striking tape of the day —
+26.3% over 20 sessions into a fiscal-year-end print, still −22.7% off its 52-week high,
puts bid at +3.44 skew on a 12.96% straddle, and a reaction history that is empty
(`hist_n=0`) because every prior 8-K item 2.02 on the CIK was filed under a former name.
It was not hunted. The sweep is the designated priority authority, and a second override
on my own read of what looks interesting is exactly the contamination this stage forbids.
Flagging it as the most obvious candidate for tomorrow's ordering to revisit.

## Data-integrity notes

**Zero phantom calendar rows — 21 of 21 events confirmed.** 20 from a company source (IR
release, GlobeNewswire/BusinessWire/PRNewswire, or the company's own site). Only LND
(BrasilAgro) is press-corroborated rather than company-confirmed: `ri.brasil-agro.com`
served an unpopulated template and no pre-announcing 6-K was found. Withholding
`--include-unknown` continues to be the right call — on the first 2026-08-31 run, eight of
eight `time-not-supplied` rows had no earnings event at all.

**Two sessions unsettled**, and `session_confirmed` is not `event_confirmed`:
- **LND** — no release hour recoverable. Brazilian issuers typically release after the
  B3 close, consistent with `amc`, but the baseline's matched 6-K reactions include bmo,
  amc and intraday stamps, so the calendar's label is not established.
- **GROW** — the company gave only "prior to the webcast", with the webcast Friday
  2026-09-04 08:30 ET. Prior five 8-K item 2.02 filings were all `amc`, supporting
  2026-09-03 `amc`, but a `bmo` 2026-09-04 release is equally consistent with the wording.

Both are shed names, so neither enters the ranking — but `edge_resolve.py` measures the
move over the session recorded, so this would matter if either were hunted.

**A third session wrinkle that does affect a ranked name.** NX releases `amc` 2026-09-03
but holds its call the **next morning, 2026-09-04 at 11:00 ET**. Numbers and management
commentary arrive in two tranches ~19 hours apart. The scoring window (close before the
print to close after the first full following session) captures both, but the split is
worth recording for resolution.

**No baseline amendment, deliberately.** `edge_baseline_amend.py` correctly refused to
run — its amendments table is still 2026-08-31's (AMBR/GOLD/MEI/WLYB) and it exits
non-zero rather than reporting "nothing to amend", which is exactly how a stale table
should behave. On the merits there was nothing to amend: **no baseline returned
`suspect`**, so nothing was gated out of ranking by the suspect rule, and no baseline
denied its event. Four carry `cadence_implausible` (KNOP 14d, LND 15d, MAMA 56d, AOUT
69d) and GWRE has no recoverable cadence, but all five sit at `unknown` (`event_q` 0.6)
rather than `suspect` (0.05).

Of those, only **MAMA** was hunted. Upgrading it to `fits_cadence` would have raised its
quality multiplier from 0.6 to 1.0 while the defect it rests on is in the reaction
**history**, not the event flag — MAMA's event is company-confirmed with an explicit hour,
but its 8 recorded "prints" at a 56-day cadence are contaminated by non-earnings 8-Ks. An
amend pass would therefore have moved exactly one hunted name, upward, which is the
asymmetric tuning the skill forbids. MAMA's hunter was warned explicitly instead — and it
did the right thing: it **rebuilt the reaction history by hand**, establishing that 6 of
the 8 recorded dates map to genuine Jan-31-quarter prints (median |move| 2.8%) and that
2025-09-02 is verifiably the Crown I acquisition 8-K rather than an earnings event. MAMA
still scores on `q_ev` 0.6 and `baseline_quality` 0.26, the lowest of the eight, which is
the correct outcome: the event is real, what is priced is genuinely poorly measured.

DOMO's history was flagged untrustworthy for a different reason — its 7 reactions and
~18% median all pre-date the announced asset sale, from when this was an operating-results
event with a release and a call. Tonight it files a 10-Q only, with no press release and
no conference call. Its hunter was told, and it correctly refused to inherit the 18%
median, landing at +1.0 instead.

**Budget.** 1 sweep + 10 hunters + 8 adversaries = **19 of 20**. Concurrency ran at 5
rather than the configured 4, and briefly at 8 while early adversaries overlapped late
hunters, because every hunted name reports at 20:00 UTC tonight and the skill sanctions
exceeding the concurrency guideline for `amc` names rather than letting an adversary land
after its event. Total spend stayed inside the cap.

## Falsification

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-03/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'   # the real number
```

The normalised correlation — `edge_score` against realised move divided by implied move —
is the skill measure. Ranking a 18%-implied space name above a 9%-implied retailer is easy
and means nothing. **The pooled figure across many days is the result; this single day is
not one.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
