# Edge hunt — 2026-09-02 amc + 2026-09-03 bmo

**Generated** 2026-09-02 15:13 UTC · **run** `research/2026/09/2026-09-02/edge`

Eight names ranked, eight distinct scores, a strict order. `edge_score` is a
**ranking key on −100…+100, not a forecast of a move**. There is no call, no
threshold and no direction label anywhere below, and no cutoff has been applied —
selection is yours, made afterwards on the complete table.

## The ranking

| # | Ticker | Company | Event | edge_score | edge_pct | confidence | unc_pct | baseline_quality | option chain credited | clusters | hunters |
|---|--------|---------|-------|-----------:|---------:|-----------:|--------:|-----------------:|:---------------------:|---------:|--------:|
| 1 | DLTH | Duluth Holdings | 09-03 bmo | **+38.5** | +2.03 | 7.3 | 1.01 | 0.40 | no | 1 | 1 |
| 2 | DOO | BRP Inc. | 09-03 bmo | **+5.5** | +0.28 | 13.2 | 0.14 | 0.24 | no | 3 | 1 |
| 3 | WOOF | Petco | 09-02 amc | **+5.5** | +0.27 | 16.8 | 0.14 | 0.40 | no | 3 | 1 |
| 4 | NTSK | Netskope | 09-02 amc | **+1.9** | +0.10 | 52.2 | 0.05 | 0.71 | yes | 5 | 1 |
| 5 | MEI | Methode Electronics | 09-02 amc | **−1.2** | −0.06 | 25.2 | 1.01 | 0.47 | yes | 6 | 2 |
| 6 | AGX | Argan | 09-02 amc | **−2.3** | −0.12 | 37.1 | 0.06 | 0.88 | yes | 3 | 1 |
| 7 | AI | C3.ai | 09-02 amc | **−3.9** | −0.20 | 38.6 | 0.10 | 0.92 | yes | 3 | 1 |
| 8 | GOLD | Gold.com | 09-02 amc | **−7.9** | −0.39 | 21.0 | 1.56 | 0.38 | no | 5 | 2 |

DOO and WOOF tie at +5.5 on the rounded score; on the unrounded residual DOO sits
marginally above WOOF (`edge_pct` +0.284 vs +0.274). That is a distinction too fine
to mean anything and should be read as a tie.

**Rank 1 is not "the best-measured name" — it is close to the worst.** DLTH has the
lowest confidence in the table (7.3), the fewest independent source clusters (1),
one hunter, and no credited option chain. It tops the ranking because its single
finding has the largest surviving residual, not because the day is most certain
about it. NTSK is the opposite: the highest confidence (52.2), five clusters, a real
chain — and almost no edge left, because the adversary found nearly all of it
already in the price.

## What is driving the top and the bottom

### Top — DLTH, +38.5

**The finding.** On the 2026-06-08 Q1 call Duluth's CFO said: *"For the IEEPA
tariffs of approximately $12 million paid last year, we have applied for refunds but
have not included any potential benefit in the results this quarter or in the full
year guidance."* That is ~8.7% of a $137.6M market cap and ~$0.32 a share, carried at
**zero** in both the affirmed FY2026 adjusted-EBITDA guide of $28–32M and the single
sell-side estimate of $(0.05). Duluth's Q2 ended 2026-08-02 — inside the window in
which comparable importers actually booked these recoveries.

**Source.** https://www.fool.com/earnings/call-transcripts/2026/06/08/duluth-dlth-q1-2026-earnings-transcript/ (2026-06-08)

**Independent corroboration of the timing**, from three different filers: Boot Barn
recognised $14.7M of tariff refunds in COGS in a quarter ended 2026-06-27
([8-K exhibit](https://www.sec.gov/Archives/edgar/data/1610250/000110465926088137/boot-20260728xex99d1.htm));
Ross Stores recognised ~$253M in a quarter ended 2026-08-01, one day before Duluth's
quarter end
([10-Q](https://www.sec.gov/Archives/edgar/data/0000745732/000074573226000041/rost-20260801.htm));
CBP's CAPE refund process opened 2026-04-20 with a stated 60–90 day turnaround.

**What the price says.** There is no option chain at all on this name, so the price
makes no statement about direction or magnitude. The only priced input is the tape,
and it went the other way: DLTH is −13.4% over 20 days and −4.2% over five, drifting
down through the exact weeks (Target 2026-08-20, Ross 2026-08-27) when tariff refunds
were the dominant retail-earnings story. The `priced_lean_pct` of +0.67% in the table
is a **fallback derived from the run-up, not a priced expectation** — see the
measurement section below.

**What the adversary did to it.** Judged **45% priced**, and its own independent size
(+12.0%) came in *above* the hunter's (+10.0%). Every hard fact survived primary-source
checking — the quote is verbatim, the arithmetic is right, the peer-timing premise
holds. The 45% is diffusion, not refutation: the transcript was republished the same
day by five outlets and the sector frame appeared in gated research on 2026-08-27, so
what remains genuinely undrawn is the magnitude and the this-quarter inference.

### Bottom — GOLD, −7.9

**The finding.** Gold.com's Direct-to-Consumer segment is 67% of gross profit and
earns *premium × ounces*, not the gold price. In the fiscal Q4 being reported
(Apr–Jun 2026), US Mint American Eagle silver bullion sales were 380,500 / **0** /
260,000 coins — 640,500 in total, down 76% year on year and down 92% from fiscal Q3's
8,180,000, with **May 2026 the first calendar month of zero bullion Silver Eagle
sales in the program's 40-year history**. The retail premium on 1oz Silver Eagles
peaked at 19.16% on 2026-02-17 (inside fiscal Q3, which printed $2.09 EPS) and fell to
a 5.30% low on 2026-04-24 and ~7.93% across fiscal Q4 — and has kept falling, 8.48% in
July against 6.87% in August.

**Sources.** https://findbullionprices.com/blog/silver-eagle-sales-hit-zero-in-may-2026-the-retail-buyer-has-left/
and the premium series at
https://findbullionprices.com/premium-history/silver-coins/2026-american-silver-eagle-1-oz-bu-coin/
· volumes cross-checked against
https://www.coinnews.net/2026/07/02/silver-eagle-soars-in-return/ (URL path `/2026/07/`)
and the Mint's own tidy CSV.

**The least-priced item in the whole day** is GOLD's third leg, at **32% priced**:
third-party e-commerce panels put jmbullion.com revenue at $66.4M in July 2026, down
24% over the trailing three months
(https://gripsintelligence.com/insights/retailers/jmbullion.com), corroborated by a
different vendor with a different method
(https://www.similarweb.com/website/jmbullion.com/). JM Bullion is 27% of gross profit
on the company's own disclosure and no terminal carries this.

**What the price says.** The option chain is nominally live but the ATM bid-ask is
~62% of mid, and **the scorer credited it as zero** — correctly. The 25-delta skew is
only +0.59 vol points (effectively flat) and put/call open interest is 0.29, i.e.
call-dominated. The 20-day run-up is still +2.3%. So the market is marking this name
to gold beta while the premium-and-volume regime that actually sets its gross margin
went the other way.

**What the adversary did to it.** Judged the two hunters' overlapping work very
differently: GOLD-1's Mint-volume and premium legs survived at 58 / 52 / **32** / 78,
while GOLD-2's broader reads were priced out at 85 / 70 / 88. Nothing here was
refuted on facts.

## Sign balance

**6 of 10 hunts leaned positive, 4 negative, none returned zero.**

| hunt | expected_move_pct | | hunt | expected_move_pct |
|---|---:|---|---|---:|
| DLTH-1 | +9.5 | | AI-1 | −2.0 |
| AGX-1 | +4.0 | | GOLD-2 | −2.5 |
| WOOF-1 | +3.5 | | MEI-2 | −5.0 |
| DOO-1 | +2.5 | | GOLD-1 | −5.0 |
| MEI-1 | +1.8 | | | |
| NTSK-1 | +1.5 | | | |

This is worth recording because it is the **opposite** of the previous run, where six
of eight leaned negative and the note flagged that as more plausibly an artefact of
asking hunters to find what the market has missed into a print than a fact about those
companies. One run in each direction is not a pattern; the count is only interpretable
pooled across many days, which is why every note records it.

Two hunts came back with an honest positive *and* an honest negative finding in the
same file (WOOF's IEEPA refund against its stale diesel assumption; AGX's stale
estimate stub against a backlog down two quarters), which is the shape a hunt should
have and is more reassuring than the aggregate count.

## The two-hunter split, which is the point of running it

**MEI's two isolated hunters returned opposite signs from the same sealed baseline:
+1.8 and −5.0.** Neither could see the other. That disagreement is the most
informative single output of this run, and it has a locatable cause rather than being
noise: the two hunters were reading **different lines of the same release**.

- MEI-1 built a positive read on the **revenue** line, arguing the Q2 consensus stub
  had gone stale — never re-based after Q1 beat by 78% on EPS — and sits ~7% below what
  the company's own disclosed FY27 building blocks imply.
- MEI-2 built a negative read on the **recovery-adjusted EBITDA** base, arguing the
  entire $19.6M sequential jump that caused the +37.5% re-rating was ~$19M of one-time
  EV-programme customer recoveries, making Q1 FY27 the first quarter without them.

Both are arithmetic on public documents and both can be true. The scorer sees this as
`hunter_dispersion_pct` 1.0 and lowers MEI's certainty accordingly — MEI lands mid-table
at −1.2 with an uncertainty of 1.01 points, the joint-widest in the table. That is the
mechanism working as designed.

GOLD's two hunters agreed in sign (−5.0 and −2.5) but were 2× apart in magnitude, with
dispersion 1.6.

## What the adversary broke

36 findings, all 36 judged, on both sides. `edge_brief.py --check` reports the join
clean: no unjudged finding, no orphan verdict, no null, no duplicate. Mean
`priced_in_pct` **69.6**, range 26–92.

**Broken on facts — the two clearest cases, both on AI (C3.ai):**

- **AI-1#0** claimed zero federal contract actions under C3.ai's own name in August
  2026 against three in each prior August. The adversary verified the blank was real
  and unpublished — then established it covered the **wrong fiscal quarter**, that the
  comparison base is only ~$4M, that a continuing-resolution new-start freeze and
  Carahsoft/ECS reseller routing explain it, and that the finding **omitted a
  $14.125M Missile Defense Agency Other Transaction Agreement signed inside the
  reported quarter**. Judged 58.
- **AI-1#1** claimed 11 federal/defense-titled open requisitions as evidence of a
  funded defense rebuild. The adversary pulled per-posting dates from the same
  Greenhouse feed and found **most predate the 3 June print, one dating from
  2023-05-24**, against headcount cut from 1,075 to 700. That is precisely the check
  the hunter said it could not make (Wayback was blocked). Judged 75.

**Conceded but re-scoped:** NTSK-1#4, the cross-data-plane authentication outage of
2026-07-16, is the one finding the NTSK adversary agreed is genuinely unpublished —
**26% priced, the second-lowest number of the day** — while arguing its mechanism
reaches churn quarters later, not a quarter that ended two weeks after it. That is a
different report from a refutation and is kept as such.

**Conceded outright, against the hunter's own direction:** on AGX the adversary went to
EDGAR itself and **confirmed** the absence claim — no power-EPC award 8-K or press
release since 2026-04-08 — leaving AGX-1#3 (the *bearish* backlog finding) as the only
materially undrawn item in that name at 68, while breaking the insider-sale and
data-centre-policy legs on same-day wire copy. So the adversary partly inverted its
hunter, which is what an honest both-sides pass looks like.

**The decisive primary-source check of the run, on DOO:** the hunter's central claim was
that the 50% Section 338 Canada tariff, which took DOO down 10.8% over three sessions,
does not stack with Section 232 — and it flagged that it could not render the primary
HTS code list. The adversary rendered it: the carve-out is verbatim in the **Federal
Register of 2026-07-23** and implemented as **CBP zero-rate HTS 9903.03.15** covering
"derivative aluminum or steel articles", *a month before the selloff*. Judged 65 — the
fact stands, the question is how much of it the market had.

**Survived best:** DLTH-1#0 at 45% priced with the adversary sizing it *larger* than the
hunter, and DOO-1#1 (the unmodelled IEEPA refund, read across from Polaris booking
US$74m in the exactly-overlapping quarter) also at 45.

**Priced out hardest:** MEI-2#1 at 92 and MEI-2#0 at 90 — the recovery-adjusted EBITDA
argument, which the adversary judged the market had already made.

## How much of the baseline was measured rather than inferred

This is the caveat that most changes how the table should be read.

- **17 of 32** names in the window had a computable ATM straddle when the baselines were
  sealed. That is far better than the previous run's 3 of 10 — the 14:04 UTC firing put
  the snapshot half an hour into a live, two-sided session rather than against weekend
  marks.
- But of the **8 ranked** names, only **4** have an option chain the scorer credits:
  NTSK (0.7), MEI (0.6), AGX (0.7), AI (0.8). For **DLTH, DOO, WOOF and GOLD the
  credited options quality is 0.0** — DLTH and WOOF have no usable chain at all, and DOO
  (~65% of mid) and GOLD (~62% of mid) were nominally live but too wide to mean
  anything, which the scorer correctly refused to credit.
- For those four, `priced_lean_pct` is **−0.05 × the 20-day run-up** and the "expected
  move" is a **historical median**, not a priced expectation. And all eight names
  register `agrees_with_price: true`, so every one of them took the agreement discount —
  for half the table that discount fired against a lean **inferred from a run-up**,
  which is much weaker evidence of what is priced than the rule assumes.
- Three of the four weakest-measured names are ranks 1, 2 and 3. Read the top of this
  table with that in mind.

Separately, two baseline-history defects were found *by the agents* and are worth
carrying forward:

- **MEI's baseline has `history.n` = 0** — a records bug, not a quiet name. Both hunters
  and the adversary were told so, and the adversary independently reconstructed the last
  four prints as **+12.2%, −10.9%, −11.8%, +37.5%**, against a 7.4% option-implied event
  move. (MEI-1 reconstructed the most recent print as +23.7% where MEI-2 and the
  adversary both got +37.5%; the two-against-one reading is more likely right, and the
  disagreement is left visible rather than resolved by fiat.)
- **GOLD-2 found the baseline's own reaction history half contaminated**: the +9.87%
  move attributed to the 2026-02-05 earnings release was in fact the same-evening 16:10
  ET announcement of a $150M Tether PIPE at $44.50 with a board seat. That leaves
  2026-05-06 (+0.95% on a 4.5× sequential EPS beat) as the only clean earnings reaction
  this registrant has produced — which is a magnitude constraint on the whole name, and
  the reason its 8.87% event-implied move should not be trusted.
- The **MEI consensus discrepancy is resolved**: the calendar carried $(0.47) on one
  estimate; the adversary settled it at **$(0.27) on $237.99M over ~4 analysts**, calling
  the calendar figure an outlier. That difference is load-bearing — it moves the bar from
  "very low" to "roughly flat year on year" — and it is why MEI-1 built on revenue rather
  than EPS.

## Spread, and why compression does not weaken the test

The eight ranked names span `edge_pct` **+2.03 to −0.39 points of spot**. Against
option-implied moves of 7.4% (MEI), 11.3–13.0% (AI, NTSK at 17.8%) and 15.7% (AGX)
where a chain exists, that is a very compressed table, and DLTH's +2.03 is a lone
outlier — the other seven names fit inside 0.7 of a point.

**Nobody should read `edge_score −7.9` as a forecast of a −7.9% move.** The score is a
ranking key. GOLD at rank 8 means "last of eight", not "expected down 7.9%".

Compression does not weaken the falsification test: **rank correlation reads order, not
magnitude**, so a tightly compressed but strictly ordered table is exactly as
falsifiable as a wide one. What compression does mean is that an honest adversary
discounted most of what was found — mean 69.6% priced — which is the expected outcome
when the question is "what has the market missed" and the answer is usually "not much".

## Names that could not be ranked

24 of 32. Every name in the window is still in `edge-scores.json` with a stated reason
rather than dropped from the file.

**Shed for budget** (22 names): `budget.edge_hunt` caps the stage at 20 subagents. The
arithmetic is 1 sweep + (confirmed names + `double_hunt_top_n`) hunters + (tickers with
findings) adversaries, so 30 confirmed hunt targets was never affordable — it would have
needed 1 + 32 + 30 = 63. Shed per `budget.edge_degrade_order`: unconfirmed names first,
then lowest `hunt_priority`. The stage spent **19 of 20**: 1 sweep, 10 hunters, 8
adversaries. Not shed at any point: the two-hunter split, and adversary coverage of
every finding on both sides.

Shed by priority: MTRX (68), PSNY (66), TLYS (63), MOMO (61), CHPT (60), GCO (58),
BRC (57), WLY (56), PHR (55), VBNK (53), VSXY (52), LE (50), CIEN (49), ZGN (47),
PVH (46), FIVE (44), HPE (42), NTAP (38), AVGO (36), TTC (33), SNOW (30), CPB (25).

**Deliberate deviation from strict `hunt_priority` order, recorded as the skill
requires:** MTRX (priority 68) was dropped in favour of AI (priority 65). MTRX has no
computable straddle at all — ATM spread 125% of mid on 998 contracts — so its priced
lean would have been inferred from a run-up, while AI has a genuinely measured chain
(12.7% implied, 135,726 contracts) and a trustworthy 8-print history. Near-equal
priority, materially better-measured baseline. This is the skill's own option-chain
judgement call, applied once.

**AMBR — unconfirmed event.** The only evidence for a 2026-09-03 print is the calendar
row. Amber has always pre-announced by 6-K (the 2026-05-21 6-K set the 2026-05-28 Q1
call), and every 6-K on CIK 0001697818 since July — 2026-07-28, 2026-08-10, 2026-08-31 —
carries no results date with the supposed print one day out. Last year's comparable
half-year report landed 2025-09-10, a week later than the calendar's date. Baseline
downgraded `fits_cadence` → `unknown`, not `suspect`: that states what is known, which
is that the event is unestablished, without barring the name from ranking on absence of
evidence alone.

**WLYB — not a separate event.** John Wiley class B, same CIK (0000107140) and same 8-K
as WLY. The calendar carries both rows with an identical market cap and an identical
year-ago EPS, which is the tell. Class B trades ~247 shares a day and two of its seven
recorded "reactions" are exactly 0.00% — an unchanged last trade, not a price series.
Baseline downgraded to `unknown`.

## Sweep result, and what it says about the phantom problem

**31 of 32 rows carry a company-sourced date. Zero phantoms.** One duplicate (WLYB), one
unconfirmed (AMBR), so the day is 31 companies and 30 distinct hunt targets. Withholding
`--include-unknown` again cost nothing and the window resolved 0 time-not-supplied rows,
so the eight-of-eight phantom rate that wrecked the first run has not recurred in two
consecutive runs.

**All four `cadence_implausible` flags were false positives** of the 6-K text matcher, as
briefed, and all four events are real and company-confirmed: DOO's 7 matches are monthly
6-K wrappers, PSNY's 8 are monthly delivery updates (one of them the scheduling release
itself), VBNK's 8 are near-daily regulatory and capital-ratio filings, ZGN's 8 are
quarterly revenue announcements plus a 20-F notice.

The baseline amendment was applied **symmetrically before any hunter launched** — two
upgrades, two downgrades — and is recorded in `scripts/edge_baseline_amend.py` and the
run log. DOO, PSNY, VBNK and ZGN were **deliberately not upgraded** despite their flags
being false positives: their events are real but their recorded medians are reactions to
non-earnings filings, so `unknown` (0.6) is the honest middle, and upgrading to
`fits_cadence` would have forgiven the history defect and handed each a 1.0 multiplier it
had not earned.

Six `amc` names release tonight and hold their call either this afternoon or tomorrow
morning (MEI, MTRX and PVH the next morning). In every case the release is `amc` and the
reaction is carried by the 2026-09-03 session, which is what `edge_resolve.py` should
measure.

## One day is an anecdote

**Eight names cannot produce a meaningful rank correlation.** This note contains no
correlation figure and no hit rate because neither would mean anything at n=8. The
result this stage is testing is the **pooled** figure across many days:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-02/edge   # this day
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'          # the real number
```

The normalised correlation — `edge_score` against realised move divided by implied move
— is the skill measure. Sorting a 22%-implied name above a 5.6%-implied one is easy and
means nothing.

Two structural cautions on reading even the pooled number, both of which apply to this
day:

- **Coverage tracks market cap** (`backtest/FINDINGS.md` §27 measured news coverage as a
  near-monotonic function of size). This day's hunted set is small and mid caps —
  $137M to $6.2B — which is where unpriced information is most likely to exist and also
  where sourcing is thinnest. It is not comparable to a day of mega-caps.
- **Half the ranked table has no credited option chain**, so for those names the
  denominator in the normalised correlation is a historical median rather than a priced
  expectation. Ranks 1, 2 and 3 are all in that half.

Until many days have pooled, this ranking is not better than anything.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
