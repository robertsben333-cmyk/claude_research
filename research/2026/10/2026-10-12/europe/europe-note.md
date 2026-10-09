# Stage EU — Europe ranking for 2026-10-12

**The answer: one rankable name. Two of the three calendar rows were phantoms. SDG
(Sanderson Design Group) is at +1.10, below the 2.8 conviction floor, and the panel did not
select it. Treat this as a day with no signal.**

Two of the three rows had no earnings event. Both came from the UK RNS calendar reading a
date in a sentence that was not about results, so the scraper caused this, not the
vendor. See "The two phantoms" below.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Friday 2026-10-09 at about 13:45 UTC, while the European markets were still
trading. Every sealed spot is therefore an **intraday price, not a close**. The realised
move is measured from daily bars, close(2026-10-09) → close(2026-10-12).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | uk | SDG | Sanderson Design Group PLC | **+1.10** (p57) | no | +0.28 (p29) | 3.5 | 54 | bmo. `session_unresolved` in the seal. Every SDG results RNS has gone out at 07:00, and there is an investor meeting at 10:00 |
| — | uk | FXPO | Ferrexpo plc | not ranked | — | — | 3.5 | 50 | no event on this date |
| — | uk | SWC | Smarter Web Company PLC | not ranked | — | — | 8.0 | 50 | no event on this date |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by
Opus 5.5. They describe scale, not rank.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunter's
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their own pinned agents, with no fallback.

| rank | ticker | selected | consensus_k | sign agreement | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SDG | no | 1 | 4/4 | +0.68 | +0.74 | +0.46 | +1.17* | +0.62 | +1.10 |

`*` marks a member's own top 20%. Only Sonnet 5.5 put SDG there, so SDG is **not selected**
(the rule is 3 of 4). All four members agree on the sign, which on its own carried nothing
in the judge lab (127 of 151 names, 50%).

The members' sizes:

| member | impact_sum | abs_move_pct | p_up |
| --- | --- | --- | --- |
| Opus 5 | +1.43 | 6.5 | 61 |
| Opus 5.5 | +0.6 | 5.0 | 56 |
| Sonnet 5.5 | +1.3 | 6.5 | 60 |
| Fable 5.1 | +0.9 | 4.5 | 60 |

The panel and the hunter agree on direction. No name is above the floor, so there is no
disagreement to report.

What these numbers are not:

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed, until Europe has about 200 panel
  names of its own.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but
  nothing about this market's panel is established.
- One name cannot be ranked.

## The only ranked name: SDG, +1.10

The period is pre-released. On 2026-08-07 the company published:

- H1 revenue +6% to £51.4m;
- North American brand sales +19%;
- net cash of £10.2m;
- FY27 trading "in line" with £6.5m of adjusted underlying PBT.

Source: https://www.investegate.co.uk/announcement/rns/sanderson-design-group--sdg/half-year-trading-update-/9709634.

The new lines are H1 profit, the interim dividend, H2 trading, and any commentary on
Designers Guild or the requisition.

The findings:

| finding | size | source |
| --- | --- | --- |
| The board pulled the interims forward from 21 Oct to Mon 12 Oct, two weeks after LBV Actio (≈14%) requisitioned a GM to remove the chair. This is inference that joins two documents; nothing states the motive | **+0.5** | https://www.investegate.co.uk/announcement/rns/sanderson-design-group--sdg/notice-of-updated-interim-results-date/9812290 |
| H1 adjusted PBT is the one undisclosed number. It is likely above H1 FY26's £2.2m, but flattered by £3.6m of accelerated IFRS 15 licensing income | +0.2 | the 2026-08-07 RNS above |
| Peer Colefax to 18 Sep: US +14%, UK −4.5% | +0.2 | https://www.investegate.co.uk/announcement/rns/colefax-group--cfx/agm-statement/9787926 |
| Designers Guild licence, announced 25 Sep with no price reaction | +0.2 | https://www.investegate.co.uk/announcement/rns/sanderson-design-group--sdg/strategic-licensing-agreement/9792372 |

**The case against:** the name's interim-results days include −16.34% (Oct 2024). Five of
twelve recorded reactions are worse than −12%. The up case is an inference plus a peer
proxy. The bar is the company-stated £6.5m FY PBT plus ii.co.uk's FY27 EPS of 6.4p and DPS
of 2.0p. There is no sourced H1 PBT bar.

**Already public, and what is new:** the whole H1 revenue line and the FY guide are public.
New in the release are:

- H1 profit;
- the dividend;
- H2 trading;
- the board's case against the requisition.

A change to guidance is unlikely, so on the first resolved days' evidence this is a
small-move setup (~3%).

`language_note` (UK, source locality): the ii.co.uk Stockwatch column carried what the RNS
did not:

- LBV Asset Management's link to the requisitioner;
- Stephen Brooke's private-equity background;
- Fidelity at 9.8%;
- the FY27 consensus.

## The two phantoms

Both rows reached the universe through `uk_rns_calendar.py` on `basis: financial_calendar`,
which picked a date out of a sentence that was not about results.

**FXPO.** The quoted sentence is *"The next hearing before the Supreme Court is scheduled
for 12 October 2026"*, from the FY2025 results RNS
(https://www.investegate.co.uk/announcement/rns/ferrexpo--fxpo/full-year-financial-results-for-2025/9754947).

- Ferrexpo's own calendar puts the next release, 3Q Production Results, on **2026-10-14**,
  outside the window (https://www.ferrexpo.com/investors/financial-calendar/).
- The Ukrainian Supreme Court hearing on the UAH4.7bn sureties claim *is* inside the
  window. It has been adjourned repeatedly and the claim is fully provisioned. The hunter
  recorded it as unsized tail risk.
- The hunter also flagged that FXPO's sealed `run_up_60d_pct` and `realised_vol_60d_pct`
  are Yahoo artefacts. The suspended-period bars read 0.2858, a pence/pounds error, until
  2026-08-28.

**SWC.** The quoted sentence is *"result of the IPO is expected to be announced on or
around 12 October 2026"*. It refers to the MORE preferred-share offer, not earnings
(https://www.investegate.co.uk/announcement/rns/the-smarter-web-company-plc--swc/quarterly-investor-update-/9800231).

- FY26 ends on 31 October, and the Q3 update was already out on 1 October.
- An IPO-result RNS still lands on a bitcoin-treasury stock with 168% realised volatility
  inside the window. Nothing about demand is published, so it is unsized.

`edge_score.py` marks both names not rankable ("hunter found no event on this date").
Once the window passes, the resolver should confirm the absence. The UK can reach
`event_occurred: false`.

**Scraper defect, recorded and not fixed in this run.** The `financial_calendar` basis
needs a guard against court, hearing, IPO and offer context. The SDG row, by contrast,
came from a real `notice` ("Notice of Updated Interim Results Date").

## What this day is and is not

- **Selection:** "all 3 eligible names (at or under the cap)".
  - 5 were scheduled: uk 4, pl 1.
  - 3 were eligible at the $100k floor. No random draw was needed.
  - Eligible and hunted by market: uk 3; zero in the other nine.
  - Dropped below the floor: AREC ($27k a day) and pl HPM ($2k a day).
- **Concentration:** 100% UK, one market. It is one market's day, and the effective sample
  is a single name.
- **Calendar sources:**
  - The UK RNS calendar was read. It added AREC, SWC and FXPO and confirmed SDG; two of its
    three additions that cleared the floor were phantoms.
  - Yahoo was read in all ten markets and added nothing.
  - The issuer calendars were read: EQS, Inderes, Nasdaq fincal, Euronext Oslo, and
    bankier, which added HPM.
  - No source read `unavailable`. No market was `market_closed`.
- **`session_unresolved`:** all three rows were defaulted to bmo. SDG's bmo rests on
  precedent: every results RNS at 07:00, plus the 10:00 meeting.
- **Options:** `options` is null in all ten markets, so Europe runs in the **anchor-less
  regime**. On the sealed corpus that regime priced at ρ=+0.073, p=0.45 over 104 events.
- **Short registers:**
  - The FCA register was read as of 2026-10-08.
  - **`anchor_covered: true` on 1 of 3** (FXPO, 0.38% and covering).
  - SDG and SWC are truncated zeros, not anchors.
  - The ranked name, SDG, has **no positioning anchor**. Its lean of +0.10 is the run-up
    term.
- **Spain and Poland:** 0 names (HPM was dropped on turnover). **Germany:** 0 names.
- **`lean_vs_free_control_rho`:** UK 0.4 on the last resolved run with statistics
  (2026-09-30). The lean's weights are priors borrowed from the US runs and have been
  measured nowhere in Europe.
- **`history.basis`:** `observed_rns` on all three. None is a cadence estimate.
- **Conviction floor:** no name is above the 2.8 floor. Over the whole US sample the sign
  was a coin flip below it.
- **Provenance:** uk.v7, hunters on claude-opus-5-5.
- **One day is not a result**, and one ranked name is not a ranking.

## Resolve

Run `eu_resolve.py --run research/2026/10/2026-10-12/europe` from about 2026-10-14. Yahoo's
`.L` closes lag a session. The resolver should confirm SDG on Investegate and confirm the
absence for FXPO and SWC. Then run `market_panel.py resolve --market EU`.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
