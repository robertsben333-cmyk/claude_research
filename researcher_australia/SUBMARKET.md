# Australia, and why it was built

Everything below was measured from this container on 2026-09-22 against real sampled
dates. Where a number could not be measured it says so and does not guess. Korea was
killed on counts and Canada was declined on reachability; the same standard applies here.

**Verdict: build, with a $200k/day turnover floor, a cap of 20, a seeded random draw,
and one English hunting pass.** Australia is not the deepest calendar available. It was
chosen because it has the **best positioning anchor measured anywhere in this repo**, and
because the one thing every anchor-less stage needs is an anchor that can be tested.

---

## 1. Why Australia rather than Canada

Canada has the better calendar by a distance. Annualised by each name's own cadence above
a $200k/day floor, on the same TradingView instrument stage EU uses:

| market | names ≥$200k | annualised events | per trading day | median gap | % quarterly |
| --- | --- | --- | --- | --- | --- |
| Canada | 450 | 1,735 | **6.89** | 93d | 62% |
| UK (the reference leg of stage EU) | 690 | 1,262 | 5.01 | 210d | 3% |
| **Australia** | 409 | 777 | **3.08** | 187d | 0.5% |

Canada annualises larger than the entire UK leg and is genuinely quarterly. It was
declined on **reachability**, which is the axis this repo keeps paying for:

| source | role | result |
| --- | --- | --- |
| `sedarplus.ca` | the confirmation archive, Canada's EDGAR | **0 of 4, HTTP 403** |
| `ciro.ca` | the short register | **0 of 7, Cloudflare challenge** |
| `tsx.com` company directory | reference data | 3 of 3 |

So Canada today is Spain and Poland from stage EU: no positioning anchor and no way to
reach `event_occurred: false`. EDGAR does not rescue it for the band this stage targets —
only 166 of 456 eligible Canadian names match an EDGAR ticker, and that **36% is an upper
bound** because bare-ticker matching collides with US issuers. By turnover band it is 31%
at $0.2–1m and 26% at $1–5m against 59% above $25m: EDGAR reaches the large caps, which
are the names the thesis says are already well read.

Australia's equivalent sources both answer. That is the whole trade: a thinner calendar
for instruments that work.

## 2. Stream, and the honest version of it

Forward events by month, from the vendor calendar:

| | Sep | Oct | Nov | Dec | Jan | Feb | Mar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Australia (855 forward) | 110 | 11 | 34 | 5 | 1 | **427** | **249** |
| Canada, for contrast | 26 | 117 | 572 | 153 | 14 | 15 | 2 |

**Australia is a two-month market and this file will not pretend otherwise.** 676 of 855
forward events fall in February and March. Over the next 90 days (late September to
December, its off-season) it carries 65 events above $200k with **38 of 64 sessions
empty**. Median gap 187 days, 0.5% quarterly: it is semi-annual, reporting in February
and August.

Two things make that less bad than it reads, and one makes it worse.

**Less bad.** The vendor knows only each name's NEXT date, so a semi-annual market's
forward table understates its second season: the February cohort reports again in August.
Annualised by cadence the market runs 3.08 events a trading day above the floor, which is
a real number rather than a seasonal artefact. And Australia's peak months are the exact
months stage E's US calendar and Canada's are thinnest, so it is a seasonal complement
rather than a competitor for attention.

**Worse.** The thin days are not thin, they are empty. Outside February and August the
stage will publish empty universes on most sessions. The skill and the Routine prompt
both require the run to say which of three reasons an empty day has, because a shut
exchange, an unreadable tape and a genuinely quiet session look identical in
`scheduled_today: 0` and mean different things.

## 3. The anchor, which is the reason to build this

**There is no option chain**, measured 2026-09-22 on the repo's own authenticated Yahoo
path: AAPL 22 expiries, TSM 19, ITUB 8; `BHP.AX` and `CBA.AX` **zero**, as do every
Canadian, Hong Kong, Japanese, Swiss and Indian symbol tried. So stage AU runs
anchor-less, in the regime `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45
over 104 events. Nothing about Australia refutes that.

**What it has instead is ASIC's aggregated daily short position report, and it is a
different class of object from every other register in this repo.** The FCA, JPX, the
Bundesanzeiger and the AMF all publish positions at or above a 0.5% disclosure threshold,
one row per holder. ASIC publishes the aggregate for every product. Measured on the
2026-09-16 file:

| | value |
| --- | --- |
| products | 755 |
| minimum | 0.000000% |
| median | 0.309% |
| p90 | 4.57% |
| maximum | 17.30% |
| **rows below 0.5%** | **430 of 755** |

More than half the register is made of rows every other market here would have truncated
to zero. Three consequences:

1. **The level is real at every size.** A name at 0.3% is distinguishable from a name at
   nothing. There is no `anchor_covered` arm to split out, because there are no truncated
   zeros.
2. **The change moves when the position moves**, not when a holder crosses a line.
3. **It is backtestable.** ASIC's index carries **4,113 dated files back to 2010-06-16**.
   Nothing in this repo has yet tested a positioning anchor against outcomes on a long
   history. This is the series that can carry that test, and doing so needs no stage at
   all.

**What it costs is the lag.** ASIC publishes about four business days in arrears: on
2026-09-22 the newest file was 2026-09-16. Every baseline carries
`positioning.lag_sessions` and nothing may treat it as zero. On a name that has already
run, four sessions is the whole move.

### The weakness this build already has, measured

On the 2026-08-27 validation run, `lean_vs_free_control_rho` read **0.80 over 20 names**,
against stage J's healthy range of 0.446–0.59. The lean is `short_squeeze` +
`short_building` + `runup`, and the run-up term dominates whenever short interest is
small — which, on an untruncated register, is most names. **So Australia's lean is more
entangled with its own benchmark than Tokyo's is.** That is a real defect, it is the first
thing a resolved run should fix, and it is deliberately not fixed here: the weights are
Tokyo's priors and re-tuning a constant before any Australian measurement is exactly what
`w1` was frozen to prevent. `au_resolve.py` ranks every component separately so the
replacement can come from data.

## 4. The session, and the defect that would have been silent

Measured against the ASX announcement record, 80 vendor rows above the floor whose last
release fell between 2026-08-01 and 2026-09-19, each checked against that issuer's own
announcement history. 74 matched a results announcement within three days.

**When they land, Sydney local:**

| | count | share |
| --- | --- | --- |
| pre-open, before 10:00 | **67** | **91%** |
| post-close, 16:00 or later | 4 | 5% |
| in session | 3 | 4% |

More before-the-open than the UK's 89.4%. So the window is `close(D−1) → close(D)` and
the baseline must be sealed the evening before, which is why the Routine fires after the
Sydney close and seals for the NEXT session — and why its cron is Sunday to Thursday.

**The vendor's date is wrong by one day for 85% of rows:**

| vendor date minus ASX date | count |
| --- | --- |
| **+1 day** | **63 (85%)** |
| +0 day | 8 (11%) |
| other | 3 (4%) |

Not a vendor error: Sydney is UTC+10 or +11 and the vendor stamps the UTC instant. BHP
lodged its Appendix 4E at 08:31 on 18 August Sydney time, which is 22:31 on 17 August
UTC. Every one of the eight `+0` rows is an afternoon or post-close lodgement. So
`au_market.sydney_event_date()` converts the instant rather than adding a constant, which
survives the daylight-saving change on 2026-10-04.

**This is the defect most likely to have produced a plausible wrong answer.** It does not
throw. It seals on the wrong evening, measures the wrong window and hunts a name whose
print was yesterday.

The vendor's session flag is reliable once the shift is applied: 66 of 67 pre-open rows
carried flag −1 and 5 of 5 post-close or in-session rows carried +1.

## 5. Confirmation, and the phantom rate

The ASX announcement record answers on both `curl` and `WebFetch`:

- **whole day, today**: `todayAnns.do`, 471 announcements with timestamps on 2026-09-22
- **per issuer, by year, back years**: `announcements.do?by=asxCode&asxCode=<CODE>&timeframe=Y&year=<YYYY>`

The per-issuer archive is what makes `event_occurred: false` reachable and, unlike TDnet's
~31-day window, it does not expire — a late resolve loses nothing. What is missing is a
whole-day query for a PAST date, so a day-level phantom sweep is not available; confirmation
is per issuer, as it is for Germany.

**Phantom rate: 6 of 80 rows unmatched, which is an UPPER BOUND and not the rate.** The UK
measurement found six of its eight apparent misses were classifier gaps rather than missing
prints, and this classifier is deliberately narrower still. The 2026-08-27 validation run
confirmed 19 of 20 and left one `announced_unclassified` — Mayfield Group, which had lodged
"FY2026 Results Commentary" on the day. That state exists precisely so a classifier gap
never kills a name.

## 6. Two classes of print, and pooling them would have hidden it

**Half the ASX does not lodge a profit result at all.** Mining explorers and early-stage
companies lodge an Appendix 4C or 5B with a quarterly activities report under Listing Rule
4.7B: mandatory, quarterly, and genuinely market-moving for names whose whole story is cash
burn and drilling. IperionX is the worked example — three years of ASX history, not one
Appendix 4D or 4E, and the vendor schedules it as an earnings event anyway. Its eleven
observed quarterly reports carry a median absolute reaction of **4.66%**, so these are real
events with a real distribution; they simply have a different bar.

`history.filer_type` carries `results`, `quarterly_report_only` or `none_found`; the hunter
is told to size against the right bar; and `au_resolve.py` reports `by_filer_type` so a
pooled ρ can never hide the mix. `none_found` on an issuer whose archive read cleanly is a
reason to doubt the print exists at all — the cheap check that would have caught TRT.

## 7. The reaction history is observed, not estimated

Stage J applies this quarter's notified lag backwards to prior period ends and labels every
history row `estimated`, because TDnet keeps about 31 days. Reading a cadence prior as
evidence is how TRT was ranked, traded and never reported.

Australia does not need the proxy. The ASX per-issuer archive gives real lodgement dates
with real timestamps, so the session of each prior print is **measured** and the window is
the right one. History rows carry `basis: "observed"` and may be cited as facts about a
date. `anchor_quality.magnitude` pays 0.55 for that where stage J pays 0.5.

Three classifier defects came out of building it and all three are fixed, each having
scored a non-event as a reaction: a "Results Release Date" notice (Myer, −3.53%), two
"Details" notices of presentation arrangements (TUA, −2.09% and +0.32%), and an S&P index
rebalance announcement (−4.88%). This is the Oslo defect stage EU already measured, where
"Invitation to Q4 results" counted as a print for 12 of Nordic Semiconductor's 25 rows.

## 8. The tail is intact

The ASX has **no daily price limit**. Unlike Tokyo, where 値幅制限 truncates exactly the
events a hunt most wants credit for, a correct large call here can be paid in full. Realised
move distributions are not measured in this file and should be, on the first pooled sample.

## 9. Access from this container

Measured 2026-09-22. `curl` and `WebFetch` do not always agree, so the hunter is told to try
both before giving up.

| source | `curl` | `WebFetch` |
| --- | --- | --- |
| ASX announcements | 200 | ok |
| ASIC | 200 | — |
| AFR | 200 | **refused** |
| Sydney Morning Herald / The Age, ABC News | 200 | — |
| Stockhead, Small Caps, Intelligent Investor, Listcorp, Simply Wall St | 200 | — |
| The Australian, Market Index, HotCopper, Livewire | **403** | — |
| ASIC Connect (company register) | **403** | — |
| Reuters | 401 | — |

The Japanese `curl`-beats-`WebFetch` finding partly applies: AFR is reachable by `curl` and
refused by `WebFetch`. The ASX archive answers both.

## 10. One English pass, and why there is no second one

Every other market in this repo runs two hunting passes: an English draft frozen as
`pre_local`, then a local-language or domestic-source pass. **Stage AU runs one**, on the
operator's instruction, and the reason it is right is already in the repo.

Stage EU's UK hunter is the degenerate case. Its local language is English, so it varies
*source locality* instead; `eu_resolve.py` **refuses to pool** its delta with the German and
French ones; and its own definition says in as many words that a UK zero is not evidence
about language. Australia is that case and more so: there is no Australian-language press
the international wires do not read, and the entire regulated disclosure channel is one
English feed everybody reads.

A second pass here would spend tokens measuring a variable that does not exist, and would
emit a structurally zero delta that somebody would later pool with the German and French
ones and read as evidence. `unpriced-hunter-au` therefore has no `pre_local` field and
`smoke_test.py` asserts it does not acquire one. The `pre_lessons` control still runs, and
`researcher_australia/LESSONS.md` is deliberately empty until a run resolves.

## 11. What would change the verdict

- **The register ranks at zero on a pooled sample.** Then the one reason to prefer Australia
  over Canada is gone, and the stage should be retired rather than tuned.
- **`lean_vs_free_control_rho` stays near 0.8.** The lean is then not an anchor, it is the
  free control with extra steps. The fix is a re-weighting that measurement chooses, not an
  edited constant.
- **Canada's sources open.** `sedarplus.ca` and `ciro.ca` were both refused on every attempt
  here, but France's `data.gouv.fr` was written off on four connection resets and later found
  to answer one request in three. Re-test before treating 0 of 7 as permanent.
- **The off-season is emptier than this file expects.** If the stage publishes empty
  universes for most of October to January, the honest answer is to run it seasonally rather
  than daily.
