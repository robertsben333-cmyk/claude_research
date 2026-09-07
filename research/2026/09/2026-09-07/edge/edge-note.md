# Edge hunt — 2026-09-08 bmo

**Run date 2026-09-07 (US Labor Day holiday) · window: today's `amc` plus the next
trading day's `bmo`, which resolved to six names all reporting before the open on
Tuesday 8 September 2026 · sealed 14:07–14:10 UTC, hunters launched 14:20 UTC.**

## The ranking

Six of six names are rankable, with six distinct scores and a strict order.

| # | Ticker | Company | `edge_score` | `edge_pct` | Confidence | Uncertainty | Baseline quality | Source clusters |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | ABM | ABM Industries | **+1.7** | +0.09% | 18.0 | 0.04% | 0.40 | 4 |
| 2 | WDH | Waterdrop | **+1.5** | +0.07% | 9.6 | 0.04% | 0.24 | 2 |
| 3 | DLNG | Dynagas LNG Partners | **−8.7** | −0.44% | 14.9 | 0.22% | 0.24 | 3 |
| 4 | UNFI | United Natural Foods | **−9.0** | −0.45% | 42.1 | 0.23% | 0.87 | 4 |
| 5 | CAN | Canaan | **−9.9** | −0.50% | 3.8 | 1.01% | 0.24 | 1 |
| 6 | GMHS | Gamehaus Holdings | **−11.3** | −0.57% | 13.9 | 0.28% | 0.24 | 4 |

**`edge_score` is a ranking key, not a forecast.** GMHS at −11.3 means "last of six",
not "expected down 11.3%". The residual in points of spot spans only **+0.09% to
−0.57%** — less than seven tenths of a point across the whole table — against an
option-implied move of 13.15% on UNFI, the one name where a real chain exists. Nobody
should read any number in this table as a predicted move.

That compression does not weaken the test. Rank correlation reads order, not magnitude,
so a tightly compressed but strictly ordered table is exactly as falsifiable as a wide
one — `scripts/edge_resolve.py` will score it either way. Compression is what an honest
adversary pass does to a set of findings, and it is the expected shape of this output.

**One day is an anecdote.** Six names cannot produce a meaningful rank correlation at
any significance level worth quoting. Only the figure pooled across many days is a
result, and this note is one row of that pool. Do not read the order below as a finding
about these six companies.

## What drives the top and the bottom

### Top: ABM (+1.7)

The finding: **US energy storage installed a record 20.2 GWh in calendar Q2 2026 (H1
30.8 GWh), and SEIA/Benchmark raised the full-year 2026 forecast to 71 GWh against 59
GWh installed in 2025** — published 2026-09-01, twelve weeks after ABM last guided.
Source: https://www.ess-news.com/2026/09/01/us-adds-record-20-2-gwh-of-energy-storage-in-q2/
(independently carried the same day at
https://www.solarpowerworldonline.com/2026/09/q2-was-biggest-quarter-ever-for-energy-storage-installs-in-the-us/).
ABM's Technical Solutions segment grew 27.2% in fiscal Q2 explicitly on battery energy
storage, and the entire FY2026 adjusted-EPS guide rests on that ramping in the back
half.

What the price already says: ABM is **−3.07% over 20 days** and −4.68% from its 52-week
high on unusually low 15.1% realised vol. The tape is not paying for a storage
inflection. But the adversary put this at **55% priced** and cut the size to +0.8pt,
because roughly 89% of that record is utility-scale, where ABM does not compete — and
in the same release the commercial and industrial segment ABM actually serves was
running 13% *below* 2025's full-year total. It also noted the sign is ambiguous:
management said the equipment-heavy BESS work carries compressed margins, and the
published preview frames this print entirely around margin recovery. A record install
quarter is a revenue tailwind and a mix headwind at once.

ABM ranks first partly because it is the only name of six with a positive-leaning hunt
at all, and its four findings were judged 55/66/78/88% priced — the *least* refuted set
of the day, not the most compelling.

### Bottom: GMHS (−11.3)

The finding driving it: **the fiscal Q4 2026 revenue guide of US$23–26m implies a
year-over-year decline of −15% to −25%, two to three times the −7.5% / −7.8% / −9.1%
printed in the prior three quarters.** Source (the guide):
http://www.prnewswire.com/news-releases/gamehaus-holdings-inc-announces-unaudited-financial-results-for-the-third-quarter-of-fiscal-2026-ended-march-31-2026-302793775.html
(2026-06-08). Supporting it, and judged less priced: on 2026-08-12 the company said it
will "progressively optimize its third-party publishing business in casual titles, and
in particular in the social casino category" with user acquisition "allocated according
to return on investment rather than scale" — a deliberate wind-down of the line
producing ~90% of revenue, effective the current quarter, on a session that traded
22,908 shares. Source:
http://www.prnewswire.com/news-releases/gamehaus-announces-strategic-shift-toward-ai-generated-content-302849250.html

What the price already says: GMHS is **+11.95% over five days** and −64.4% from its
52-week high. That five-day run-up is almost entirely one session — 2026-08-31,
+16.51% on 7.31m shares, roughly 27% of the non-affiliate float and 20× the 20-day
average — reacting to a 6-K that merely *extended* an existing US$5m buyback of which
only ~US$600,000 had been used in twelve months. No new authorisation and no new
dollars. The identical event a year earlier produced a ~93% spike that fully retraced.

## What the adversary broke

The pass judged all 34 findings on both sides, with a **median `priced_in_pct` of 65.5**
across a 38–88 range. Three findings were refuted on fact, not merely discounted, and
in each case the refutation is the more useful output than the score:

- **GMHS#0 — premise false.** The claim's whole novelty rested on Q4 FY2025 revenue
  being "a figure the company has never reported", derivable only by subtracting a
  nine-month cumulative from a full year. The company reported it verbatim, twice, under
  an explicit "Fourth Quarter of Fiscal Year 2025" header, in its EDGAR-filed release of
  2025-09-09: "Total revenue was US$30.7 million, representing a 2.9% decrease from
  US$31.6 million." Source:
  https://www.sec.gov/Archives/edgar/data/2000530/000149315225012895/ex99-1.htm
  Judged 85% priced. The derived base (30.609) was also slightly wrong against the
  reported 30.7.
- **CAN-a#2 — premise false.** The claim was that a June insider buy cluster was
  "essentially invisible" because a 20-F filer is assumed to have no Section 16
  reporting. Canaan issued a dedicated press release about it on 2026-06-24 —
  "Zhang and Cheng together acquired a total of 1,065,000 American Depositary Shares
  … at an average price of US$0.35" — carried by Morningstar and TipRanks, and the
  stock fell 5.87% that day. Source:
  https://www.sec.gov/Archives/edgar/data/0001780652/000110465926077092/tm2618773d1_ex99-1.htm
  The claim also under-enumerated the cluster at 565,000 ADSs against the real
  1,065,000. Judged 88% priced.
- **WDH#2 — three factual assertions failed.** Chiefly, the claim called RMB639.6m an
  "undisclosed revenue line" in the FY2025 20-F, while WDH#0 *in the same brief*
  correctly cites it as disclosed by name in the 2026-03-25 release. The claim's "no
  head of finance" is also contradicted by the very 6-K it cites, which is signed by a
  VP of Finance and Head of Strategy and Capital Markets. Judged 85% priced.

**Conceded the fact but refused the sign** — a different and weaker kind of break, worth
keeping separate: on DLNG#0 the adversary independently *confirmed* the finding's
highest-value fact-check, that the four "Clean"-prefixed hulls in the NGO release
(Clean Planet, Clean Ocean, Clean Vision, Clean Horizon) belong to Dynagas Holding and
Dynagas Equity Holding, not to the listed partnership, whose six ships are Clean Energy,
Ob River, Amur River, Arctic Aurora, Yenisei River and Lena River. It then argued the
inference is arguably sign-reversed: if only 2 of 6 listed hulls carry Yamal cargo, the
NYSE entity carries *less* headline sanctions risk than the release implies. It also
showed the July round trip is complete — the stock closed $3.65 on 15 July, $3.32 on
16 July, $3.85 on 23 July, and $3.66 on 4 September, one cent above the pre-scare
close — so there is no carve-out premium left to deflate. Judged 76% priced.

**Survived best:** DLNG#1 at **38% priced** — Clean Energy, moved onto a Rio Grande LNG
charter at end-April 2026, sitting at anchor in ballast in South East Asia since
departing Singapore on 5 August, 33 days idle, while a second hull is contracted to the
same pre-operational charterer from September–November. The adversary verified the AIS
reading itself from the same page and found no financial-media coverage of it, so the
fact is close to unpublished. It cut the size to −1.2pt for two sound reasons: on a time
charter, hire is paid whether the ship moves or not, so this is a counterparty
observation about NextDecade rather than a DLNG revenue observation — and the idling
began 5 August, which is Q3, while the 8 September release covers the quarter ended 30
June. Next best: WDH#4 at 40% (a 30-day-average listing-threshold computation nobody
has published), then CAN-a#1, DLNG#2 and GMHS#6 at 45%.

**The most interesting single output of the day, though, is a resolved disagreement.**
The two isolated CAN hunters returned −6.0 and −4.0 from the same sealed baseline, and
they disagreed on a matter of fact: one rested a finding on shelf capacity and motive
for equity issuance; the other asserted from a share-count reconciliation that no ATM
issuance has occurred at all. The adversary settled it from primary filings and both are
consistent: EDGAR shows Canaan's last 424B5 on 2025-11-04 and none in 2026, so there has
been no registered takedown — and the one large 2026 issuance, 806,439,900 Class A
shares to Cipher Mining as acquisition consideration, is *unregistered*, which is
precisely why the second hunter's Rule 144 lock-up argument works. Neither hunter was
wrong. That resolution exists only because neither could see the other.

## The sign balance

**Seven of eight hunts leaned negative; one leaned positive.**

| Hunt | `expected_move_pct` |
| --- | ---: |
| ABM | +1.5 |
| WDH | −1.4 |
| DLNG | −1.6 |
| UNFI-a | −2.5 |
| UNFI-b | −2.5 |
| CAN-b | −4.0 |
| CAN-a | −6.0 |
| GMHS | −6.0 |

This is more one-sided than the 6-of-8 recorded on 2026-08-31, and it is more plausibly
an artefact of asking hunters to find what the market has *missed* into a print than a
fact about these six companies. Two runs is not a pattern, but the direction of the
skew is now consistent across both, and it should be watched: if it recurs, the hunter
prompt is generating pessimism rather than detecting it. Recording the count in every
note is the only way that becomes visible.

Note that the ranking does **not** simply reproduce the hunt leans. WDH ranks second on
a −1.4 hunt because the adversary left more of its findings standing relative to the
size claimed, while CAN ranks fifth on a −6.0/−4.0 pair whose largest findings were
judged 68% and 82% priced. That is the pass doing its job.

## How much of the baseline was measured rather than inferred

**One name of six has a usable option chain. Not two.**

- **UNFI** — genuinely measured. 13.15% implied move, +6.97-point 25-delta put skew,
  1,789 contracts of open interest, ATM spread 23% of mid. This is a real, tradeable
  statement of what the market has priced, and it is the only one in the table. UNFI's
  `baseline_quality` of 0.87 against 0.24–0.40 for every other name is that fact
  showing up in the arithmetic.
- **ABM** — nominally 8.13% implied, but total front-expiry open interest is **93
  contracts** and the ATM bid-ask is **78% of mid**. The scorer already discounts this
  (`options` quality component 0.0, `atm_spread_frac` 0.778) and the adversary was
  instructed to treat it as unusable and did, declining to read the skew in either
  direction. Call it inferred, not measured.
- **WDH, CAN, DLNG, GMHS** — no listed options at all. For these four, `priced_lean_pct`
  falls back to −0.05 × the 20-day run-up and `expected_move_pct` is a historical
  median rather than a priced expectation. So the agreement discount fires against a
  lean *inferred from a run-up*, which is much weaker evidence of what is priced than
  the rule assumes. That matters most for CAN, whose −3.41% inferred lean comes off a
  +68.2% 20-day run-up, and least for WDH and GMHS, where the inferred lean is a tenth
  of a point.

Five of six names therefore have their "what the market priced" figure inferred rather
than observed. A ranking built mostly on names with no options is measuring something
weaker than the table's precision suggests, and the confidence column reflects it: CAN
carries confidence 3.8 with uncertainty 1.01%, an order of magnitude wider than any
other name, driven by the 2.0-point spread between its two hunters.

## Names that could not be ranked

None. **Six of six were confirmed and all six are rankable.**

That is itself the most improved figure in this run's history. The sweep confirmed every
calendar row from a company source with an hour attached: **zero phantom rows, zero
unsettled sessions** — against eight of eight phantoms on the first 2026-08-31 run
(which passed `--include-unknown`) and zero of ten on the second. `--include-unknown`
was withheld here and `edge_universe --window` returned 6 of 34 calendar rows with no
unresolved-session rows to drop.

Three things the sweep caught that would otherwise have corrupted this run:

- **DLNG's session was announced twice.** The company's release of 2026-09-01 said
  results would come "after market closes in New York on Monday, September 7, 2026";
  the superseding release of 2026-09-02 says "before the New York market opens on
  Tuesday, September 8, 2026" — almost certainly because 2026-09-07 is Labor Day. A
  hunter reading only the first release would have had the wrong session, and
  `edge_resolve.py` measures the move over the session recorded. Note that Dynagas holds
  no earnings call and gives no release hour, so "before the open" is the strongest
  available statement; the session rests on company wording, not on a call time.
- **Four of six baselines carry an unusable reaction history.** CAN, DLNG and GMHS all
  returned `unknown` with `cadence_implausible: true` (inferred cadences of 13, 21 and
  55 days — no quarterly reporter has one), because for a foreign private issuer filing
  no item 2.02 the 6-K text matcher catches monthly bitcoin-production updates,
  distribution declarations, charter updates and the results-date announcements
  themselves. Each hunter was told this explicitly, so that none of them used a base
  rate built from operational updates.
- **WDH's baseline was amended DOWNWARD before any hunter launched**, from
  `fits_cadence` to `unknown`, and it is the only amendment in this pass. The event is
  real and company-confirmed for 2026-09-08 pre-open, but the "fits" verdict was an
  artefact: the filing set contains three 6-Ks inside one quarter (2026-06-17, 06-23,
  07-24) where at most one earnings release can exist, it carries a literal duplicate
  (2025-12-03 twice with an identical +1.07%), and its "last print 2026-07-24, 46 days
  ago" would make 2026-09-08 a second print in the same quarter. CAN, DLNG and GMHS were
  deliberately **not** upgraded despite company-confirmed dates with the hour, because
  upgrading would forgive a history defect and hand each a multiplier it has not earned.
  Per-name warnings went to the hunters instead. A pass whose only entry lowers a
  verdict is worth stating plainly: no name gained an event multiplier in this run.

## Budget and process

15 of the `edge_hunt` cap of 20 subagents: **1 sweep + 8 hunters + 6 adversaries.** No
shed was required and `budget.edge_degrade_order` was not invoked. The two-hunter split
was applied to the top two names by `hunt_priority` (UNFI 78, CAN 72) and adversary
coverage of every finding on both sides was complete — `edge_brief.py --check` reports
**34 findings, 34 verdicts joined, JOIN CLEAN**, so no finding silently defaulted to
mostly-priced.

Baselines were sealed and pushed (commit `cb92bbd`) before any agent launched, and the
heartbeat published before the sweep. Every hunt and adversary file was published as it
landed rather than once at the end.

One judgement worth recording: the skill advises keeping names with a live option chain
even where they rank low on `hunt_priority`. No deviation was needed here — the two
names with any chain at all (UNFI 78, ABM 61) were both above the median priority and
would have been kept regardless.

## Resolution

Once the window closes:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-07/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'   # the real number
```

The normalised correlation — `edge_score` against the realised move divided by the
implied move — is the skill measure. Sorting a 13%-implied grocery wholesaler above a
name with no options at all is easy and means nothing on its own.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
