# Edge hunt — 2026-09-01 amc + 2026-09-02 bmo

**Eight of sixteen names ranked, in a strict order, on one signed score each.** Sixteen
calendar rows, sixteen confirmed events, **zero phantoms**. Eight names hunted, 34
findings raised, all 34 judged by an adversary on both sides.

`edge_score` is a **ranking key on −100…+100, not a forecast of a move.** Read the
table as an order, nothing more. The whole table spans 1.37 points of spot
(`edge_pct` +1.13 to −0.25) against option-implied event moves of 7.8% to 14.5%. Nobody
should read `edge_score 22.2` as a call for a 22% move, or `−4.9` as a short.

## The ranking

| # | Ticker | Company | Session | `edge_score` | `edge_pct` | Confidence | Baseline quality | Priced lean | Agrees with price |
|---|---|---|---|---|---|---|---|---|---|
| 1 | SPWH | Sportsman's Warehouse | 09-01 amc | **+22.2** | +1.13% | 15.8 | 0.40 | −0.15% | no |
| 2 | CRDO | Credo Technology | 09-01 amc | **+11.6** | +0.58% | 51.6 | 0.94 | −3.51% | no |
| 3 | DELL | Dell Technologies | 09-01 amc | **+8.2** | +0.41% | 14.4 | 0.98 | +4.32% | yes |
| 4 | FCEL | FuelCell Energy | 09-02 bmo | **+7.7** | +0.39% | 24.4 | 0.81 | −6.03% | no |
| 5 | CXM | Sprinklr | 09-02 bmo | **−3.6** | −0.18% | 0.0 | **0.00** | −1.13% | yes |
| 6 | PANW | Palo Alto Networks | 09-01 amc | **−3.8** | −0.19% | 22.9 | 0.51 | +6.64% | no |
| 7 | MDB | MongoDB | 09-01 amc | **−4.5** | −0.22% | 14.9 | 0.93 | +0.12% | no |
| 8 | GTLB | GitLab | 09-01 amc | **−4.9** | −0.25% | 35.3 | 0.88 | −4.69% | yes |

**Rank order is not confidence order, and the reader should not conflate them.** The
top-ranked name (SPWH, confidence 15.8) is among the *least* well-supported; the
best-supported name (CRDO, 51.6) ranks second. CXM sits fifth on a baseline quality of
**exactly zero** — no option chain and no reaction history, so nothing about its position
is measured. Selection is the reader's, applied to the complete table; no cutoff has
been applied here.

### What drives the top name

**SPWH (+22.2).** NSSF-adjusted NICS background checks for the three calendar months
that are SPWH's fiscal Q2 (quarter ended 1 Aug 2026) ran +7.7% year on year — 3,290,647
against 3,055,402 — accelerating about 5.4 points from roughly +2.3% in the fiscal Q1 in
which the company comped +2.1%.
Source: <https://www.theoutdoorwire.com/releases/2026/08/nssf-adjusted-nics-background-checks-for-july-2026/>
(July release, 2026-08-05). Both isolated hunters found it independently. Corroborated
from the supply side by Sturm Ruger's Q2 (sell-through +19%, distributor inventories
down 45,800 units, <https://www.businesswire.com/news/home/20260729922943/en/Sturm-Ruger-Company-Inc.-Reports-Second-Quarter-2026-Results>)
and Olin's Winchester segment (+11.8% on higher commercial ammunition volume *and*
price).

**What the price says:** almost nothing, and this is the weakest link in the top rank.
SPWH has 23 contracts of total open interest, so there is no chain, no implied move and
no skew. The `priced_lean_pct` of −0.15% is *inferred* from a +3.04% 20-day run-up — and
the adversary's point stands that at roughly 0.4 sigma against 28.3% realised vol, that
run-up is statistically indistinguishable from no move and cannot bear a "priced in"
argument in either direction. The adversary also put the demand data at 58–60% priced,
because NICS is the most-published datapoint in the sector (six-plus outlets on
2026-08-05); what is *not* published is the link to SPWH's own estimate line, where the
2026-08-30 preview has consensus revenue flat and never mentions firearms demand.

### What drives the bottom name

**GTLB (−4.9).** A Reg FD 8-K furnished 2026-07-08 restated the paid Consumption Run
Rate touted five weeks earlier from "nearly $20 million" to "closer to $15 million",
because the calculation "now excludes certain one-time credit incentives granted to
paying customers" — roughly a quarter of the headline AI number was giveaway credits to
existing paying seats.
Source: <https://www.sec.gov/Archives/edgar/data/1653482/000165348226000145/gtlb-20260708.htm>

**What the price says:** it already leans the same way. GTLB carries a +6.53 vol-point
25-delta put skew — puts bid, the market paying for downside — giving a
`priced_lean_pct` of −4.69%, and `agrees_with_price` is true. A negative finding that
agrees with a measured negative lean is largely priced, which is why the residual is a
quarter of a point of spot and not more. The adversary put this finding at 80% priced
and, decisively, showed the restatement text sits in the **plain HTML body** of the 8-K
(not the 48-JPEG exhibit the hunt treated as obfuscation), was carried by StockTitan and
TradingView the same day, and that the stock rose **7.8%** on the disclosure.

## The eight names that could not be ranked

None was excluded on its findings; all eight sat out for stated, visible reasons.

| Ticker | Priority | Why not ranked |
|---|---|---|
| BF.B | 39 | Baseline generation failed entirely (`bars_failed`, dotted symbol) — no spot, no history, no chain. Unmeasurable, so not hunted. |
| BF.A | 11 | **Duplicate of BF.B** — one company, one release, two share classes. Scoring both would double-count one event and pollute a rank correlation with a near-duplicate. |
| GIII | 65 | Shed for budget. |
| REX | 63 | Shed for budget. |
| DAKT | 57 | Shed for budget. |
| YSG | 55 | Shed for budget. FPI history also contaminated (see below). |
| GASS | 51 | Shed for budget. |
| OLLI | 43 | Shed for budget — the one live-chain name dropped, lowest priority of the seven and widest spread (0.50 of mid). |

The budget cap of 20 subagents allows about eight hunted names (1 sweep + 10 hunters + 8
adversaries = 19). Deviation from strict `hunt_priority`, recorded as the skill requires:
GIII (65), REX (63) and DAKT (57) outrank DELL (53) and MDB (47) and were dropped anyway.
The policy applied was to keep the top two by priority regardless of chain (they take the
double hunt), then fill on **baseline measurement quality** — DELL and MDB carry the two
tightest chains of the day, and taking them lifted measured-baseline coverage in the
hunted set from 4 of 8 to 6 of 8.

## How much of the baseline was measured rather than inferred

**Six of the eight ranked names have a live two-sided option chain** — CRDO, DELL, FCEL,
PANW, MDB, GTLB — so for those, "what the market has priced" is measured. ATM spreads:
DELL 0.033 of mid, CRDO 0.105, MDB 0.115, PANW 0.157, GTLB 0.203, FCEL 0.320.

This is the single biggest improvement over the run of 2026-08-31, where **seven of ten**
names had no listed options and `priced_lean_pct` fell back to −0.05 × the 20-day run-up.
The cause is the fire time: this stage now runs at 14:04 UTC / 10:04 New York, about
half an hour into the US session, instead of against stale weekend marks. On 08-31 an ATM
spread read 41% of mid; today the best six run 3.3% to 32%.

**The two exceptions matter and should not be glossed.** SPWH (rank 1) and CXM (rank 5)
have no usable chain, so the agreement discount for those two fired against a lean
inferred from a run-up. For CXM there is not even a reaction history — `baseline_quality`
is 0.00 and confidence is 0.0. Its rank-5 position is the least evidenced number in the
table.

## Sign balance

**Hunters: 6 of 10 hunts leaned positive.** By name, 5 of 8 (SPWH +11.25 summed finding
impact, DELL +5.25, CRDO +2.35, FCEL +1.30, MDB +0.50) against 3 negative (CXM −9.20,
PANW −2.60, GTLB −2.15).

**After the adversary: exactly 4 positive and 4 negative.**

This is worth recording against 2026-08-31, when six of eight leaned negative and the
concern was that asking hunters to find what the market has missed into a print
generates pessimism rather than detecting it. Today's balance does not support that
worry, and MDB is the clearest case of the adversary doing the work: the hunt summed to
+0.50 and the name finished at −4.5 once its lead finding was priced at 94.

## What the adversary broke

The adversary pass found a **concrete factual or logical defect in the load-bearing
finding of every one of the eight names.** Median `priced_in_pct` across the 34 findings
was 78, mean 72.2; 16 findings were judged ≥80% priced and only 7 at ≤55.

Findings that were **factually wrong or inverted**, not merely priced:

- **SPWH — the causal premise was wrong, and both hunters made the same error.** Both
  claimed the June 2026 extension of the revolver and ABL term loan to 2031 removes the
  mechanism behind this stock's −29.8% and +97.9% prints. It does not: the −29.8% of
  2025-12-04 was a full-year EBITDA guidance cut on softening consumer spending, and the
  +97.9% of 2025-04-01 was an EBITDA beat with a $27.3m net-debt reduction. Both were
  guidance events, not maturity events — so the claim would lead a reader to *narrow*
  the tail at exactly the print where a $30–36m FY EBITDA guide against −$8.1m in Q1
  means it should not be narrowed. Judged 87–88% priced (the refinancing was press-released
  and on four wires the same day).
- **DELL — the sign of one finding was refuted by a closer comparable.** The claim that
  the memory shortage is a pricing-power event rather than a margin event for OEMs rests
  on IDC data covering two of Dell's three months. HP Inc reported on 2026-08-26 for a
  quarter ended 31 July — a *full* three-month overlap — with Personal Systems operating
  margin **down** to 4.6% from 5.4% because commodity costs "more than offset repricing",
  and DELL fell 3.7% on 28 Aug in its wake. The adversary also found Super Micro had
  *pre-announced* its margin beat on 2026-07-21, six weeks before the print the finding
  cited, and that DELL rose ~4% on 2026-08-13 on this exact read-across with wire
  headlines naming it. The claimed "20–40%" price increases reconcile to about +18% in
  IDC's own forecast. Judged 78% and 86% priced.
- **MDB — the novelty claim collapsed.** The remaining-performance-obligation surge was
  presented as visible only in a 10-Q footnote cited by none of August's price-target
  raises. It was a **headline line item in MongoDB's own 2026-05-28 press release**
  ("RPO $1,458.6 million, up 88% year-over-year"), quantified verbally on the call and
  carried in wire copy as "backlog up 88%" — and the derived "+72% committed next-12-month
  revenue" is a less accurate restatement of a disclosed cRPO of +69%. Judged 94% priced,
  the most-priced finding of the day.
- **FCEL — the alt-data evidence did not survive inspection.** The load-bearing finding
  read an end-to-end third shift into 61 of 80 job requisitions at the Torrington cell
  plant. The adversary found the "Facility Tech (Third Shift)" posting states its hours
  as "M-F 3:30 pm to 11:30 pm" — second-shift hours — so at least one of the nine cited
  titles is mislabelled; the flagship third-shift supervisor requisition is a **two-month-old
  repost of an unfilled role**, which argues the shift is *not* running; and the datable
  requisitions are 4 and 15 August, *after* the 31 July quarter end. Marked
  `reaches_this_print: false`.
- **GTLB — the obscurity premise was false**, as set out above; and GitLab 19.3, on which
  two further findings rest, shipped 2026-08-20, twenty days *after* the quarter closed,
  so the usage caps cannot touch the reported print at all.
- **PANW — the attribution was wrong.** The +12.83% session of 2026-08-27 was attributed
  to an acquisition rumour alone; CrowdStrike beat and raised the prior evening and had
  its best day ever (+20%) with Okta +29%, and CNBC named PANW among cyber peers up at
  least 10%. Worse for novelty, the reaction-function claim was published in *that
  morning's own* pre-print preview ("Four consecutive beats. Three consecutive sell-offs",
  average ~−5.2%), and the hunt omitted the fourth data point. Judged 85% priced.
- **CRDO — two findings are mirror images that cannot both be the operative fact.** One
  infers from a supplier proxy that Credo is running far above its guide; the other
  observes that Credo said nothing, where it *did* pre-announce the last time it was
  blowing out. Scoring both as independent positives would double-count a contradiction.
  The supplier read was also corrected from +31% to **+22.7% QoQ** on a like-for-like
  fiscal mapping (the February base is Chinese-New-Year depressed), with Credo plausibly
  only 7–8% of that supplier's consolidated revenue.
- **CXM — the flow attribution was refuted from the tape.** The claim that the 20-day
  run-up was driven by accelerated-share-repurchase buying fails because the programme ran
  continuously from 2026-03-16 while the stock *fell* from 6.01 to 4.91; and the "no news
  gap" assertion is wrong (2026-08-27 was +6.3% in one session, on a sector move).

**The finding that survived best:** Sprinklr's Q1 FY27 10-Q geographic disaggregation,
showing Americas revenue **fell** to $112.9m from $117.6m (−4.0% YoY) while "Other"
jumped 86%, so 48.6% of revenue is now outside the Americas — the home market is
contracting and all growth comes from the regions carrying the Middle East disruption
and FX. Judged **40% priced**, the lowest of all 34, with the adversary's independent
size estimate (−0.7%) close to the hunter's (−1.1%).
Source: <https://www.sec.gov/Archives/edgar/data/1569345/000156934526000028/cxm-20260430.htm>

Note the distinction the skill asks to preserve: on SPWH, DELL and MDB the adversary
**refuted a fact or an inference**; on GTLB, CRDO and PANW it largely **conceded the
facts and rejected the novelty or the sign**. Those are different verdicts.

## The double hunt: convergence is not corroboration

Both double-hunted names produced hunters that **agreed** — SPWH +5.5 and +4.0 (dispersion
0.475), CXM −4.0 and −3.2 (dispersion 0.205). On 2026-08-31 the two isolated hunters on
one name returned *opposite* numbers, and that disagreement was the most informative
output of the run.

Agreement turned out to be worth less, and this is the run's most useful methodological
result. In both cases the adversary showed the convergence reflected a **shared blind
spot rather than independent confirmation**:

- On SPWH both hunters built the same wrong causal claim about the credit facility, and
  hunter B additionally misstated a company figure (+7.4% hunting-and-shooting where the
  release says 6.3%) — so on the company side they were not corroborating each other at
  all.
- On CXM both independently dug out the same obscure 10-Q footnote (the $125m repurchase
  terminating 2026-09-01) and **both missed the same caveat in the same disclosure** —
  that the bank may terminate early at its discretion — which StockTitan had published,
  with the date, on 2026-06-04.

Two isolated searches landing on one document is evidence the document is *findable*, not
that the market has missed it. Keep the two-hunter split, but do not read agreement as
validation.

## Corrections made before any hunter launched

The sweep found three real baseline defects, amended symmetrically from company sources
and committed before the first agent spawned:

- **A systematic former-name filter bug in `priced_in.py`** zeroed the reaction history of
  PANW (all 28 prints on CIK 0001327567, cutoff 2026-08-27) and CXM (all 21 on CIK
  0001569345, cutoff 2026-08-19). Neither company changed its name; two registrants
  producing the identical artefact two weeks apart is a bug. Both amended
  `unknown → fits_cadence`.
- **GASS "suspect" was a false positive** — the 6-K text matcher counted StealthGas' own
  2026-08-28 *scheduling release* as an earnings print, giving an impossible 5-day gap
  against an 88-day cadence. Amended `suspect → unknown`.
- **YSG was DOWNGRADED** `fits_cadence → unknown`, the symmetric half: its history holds a
  literal duplicate (2026-03-02 twice, identical −8.99%) plus a non-earnings 6-K five days
  before the real print, so at least three of eight rows are not distinct earnings
  reactions.

Disclosing the arithmetic effect, since it favoured names that were hunted: the PANW
amendment raised its `baseline_quality` from about 0.31 to 0.508 and is material to its
rank. The CXM amendment was **arithmetically inert** — its quality is 0.00 either way,
because 0 × 1.0 = 0 — so it gained nothing. Symmetry here means one standard applied, not
an equal count; the sweep found no other name whose `fits_cadence` rested on a defect, and
inventing a downgrade for numerical balance would be its own distortion.

Two tooling defects were fixed in the same commit. `scripts/edge_baseline_amend.py` still
carried the 2026-08-31 amendments table, and a stale table prints only "SKIP no baseline"
lines and then "DRY RUN" — indistinguishable from "nothing to amend"; it now exits
non-zero when no entry matches a baseline in the target directory. Its printed
upgrade/downgrade label also called every non-suspect change a downgrade, mislabelling
`unknown → fits_cadence` and hiding whether a pass was symmetric; it now ranks by the
`event_q` multiplier the scorer actually applies.

## Universe quality

**Zero phantom rows out of sixteen** — every row backed by a company-issued scheduling
release, and session confirmed for all sixteen. The trend across three runs: 8 of 8
phantom on the first 2026-08-31 run (with `--include-unknown`), 0 of 10 on the second,
0 of 16 today.

Four rows had an intraday *call* time with a pre-open *release* — BF.A/BF.B (release by
08:00 ET, call 10:00 ET), FCEL (10:00 ET), REX (11:00 ET), DAKT (11:00 ET). The release
sets the session; all are correctly `bmo`. Reading the call hour would have mislabelled
four of sixteen names, and `edge_resolve.py` measures the move over the session recorded.

Three date traps were caught and discarded rather than used: a 23-store-closure story that
is from **March 2009**, a Sprinklr "15% layoff" served as August 2026 that is **February
2025**, and a Sprinklr "Wall Street projections" piece served as current that is **August
2024**. Dates came off URL paths, not snippets.

## One day is an anecdote

**This table cannot establish anything on its own.** Eight names cannot produce a
meaningful rank correlation, and no result here should be read as evidence the method
works. The pooled figure across many days is the only number that answers the question
this stage exists to test, via:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-01/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'
```

The normalised correlation — `edge_score` against the realised move divided by the implied
move — is the skill measure. Sorting a 14.5%-implied database company above a
7.8%-implied security company is easy and means nothing.

One point in this run's favour as a *test*, separate from whether the order is right: the
compression is not a weakness. Rank correlation reads order, not magnitude, so eight
distinct scores in a strict order over 1.37 points of spot is exactly as falsifiable as a
wide table would be. What would invalidate the test is ties or rounding into buckets, and
there are none.

Two structural caveats to carry into the pooled result. Coverage tracks market cap
(`backtest/FINDINGS.md` §27), and this day skews large — PANW at $303bn and DELL at
$296bn against SPWH at $45m — so the hunt is flattered relative to the small,
high-change-expectation names the pipeline normally shortlists. And SPWH at a $1.185 spot
on ~276k shares a day will produce a noisy realised move regardless of what was found,
which is measurement error in the dependent variable and attenuates correlation on its
own.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.*
