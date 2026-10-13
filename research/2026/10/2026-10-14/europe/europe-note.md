# Stage EU — Europe ranking for 2026-10-14

**The answer: no name clears the 2.8 conviction floor. Six names were ranked. Every
`impact_sum` sits between −0.6 and +1.6. AVARDA (Avarda Bank, SE) and VTU (Vertu Motors, UK)
share the top at +1.60. JHD (James Halstead, UK) is the bottom at −0.60. The panel selected
no name, although AVARDA was the closest: two of four members put it in their own top 20%.
A seventh name, DEMANT (Demant, DK), was a phantom: 14 October is the first day of its
quiet period, and its Q3 report is on 3 November.**

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Tuesday 2026-10-13 at about 13:45 UTC, while the European markets were still
trading. Every sealed spot is therefore an **intraday price, not a close**. The realised move
is measured from daily bars, close(2026-10-13) → close(2026-10-14).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | AVARDA | Avarda Bank | **+1.60** (p75) | no | +0.96 (p70) | 6.0 | 58 | bmo. The issuer's invitation says 06:30 CEST |
| 2 | uk | VTU | Vertu Motors | **+1.60** (p75) | no | +0.70 (p58) | 5.0 | 57 | bmo, `session_unresolved` in the seal. Every prior Vertu RNS went out at 07:00 |
| 3 | uk | BOOM | Audioboom | **+1.20** (p65) | no | +0.75 (p61) | 7.5 | 55 | bmo, `session_unresolved` in the seal. Prior updates went out at 07:00 |
| 4 | se | CRED_A | Creades A | **+0.10** (p14) | no | +0.00 (p7) | 2.5 | 50 | bmo, `session_unresolved` in the seal. The Q2 report gives "14 oktober 2026, kl 8.30" |
| 5 | uk | SCT | Softcat | **+0.10** (p14) | no | +0.07 (p16) | 3.5 | 51 | bmo, `session_unresolved` in the seal. Prior results went out at 07:00 |
| 6 | uk | JHD | James Halstead | **−0.60** (p44) | no | −0.21 (p29) | 3.5 | 47 | bmo, `session_unresolved` in the seal. Prior results went out at 07:00 |
| — | dk | DEMANT | Demant | not ranked | — | — | 2.1 | 50 | no event in the window (see below) |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by
Opus 5.5. They describe scale, not rank. AVARDA and VTU tie on the key. The scorer's order
between them carries no information.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their own pinned `-intl-` agents, with no fallback, and each covered 6 of 6 packs.

| rank | ticker | selected | consensus_k | sign agreement | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AVARDA | no | 2 | 4/4 | +1.11 | +1.30* | +1.10 | +1.12 | +1.11* | +1.60 |
| 2 | VTU | no | 0 | 4/4 | +0.61 | +0.58 | +0.63 | +0.47 | +0.65 | +1.60 |
| 3 | BOOM | no | 0 | 4/4 | +0.47 | +0.35 | +0.59 | +1.03 | +0.17 | +1.20 |
| 4 | JHD | no | 0 | 4/4 | −0.23 | −0.38 | −0.25 | −0.19 | −0.22 | −0.60 |
| 5 | SCT | no | 0 | 3/4 | +0.10 | +0.10 | +0.21 | +0.09 | +0.00 | +0.10 |
| 6 | CRED_A | no | 0 | 4/4 | +0.05 | +0.04 | +0.06 | +0.09 | +0.04 | +0.10 |

`*` marks a member's own top 20%. Only Opus 5 and Fable 5.1 put AVARDA there, so **no name is
selected** (the rule is 3 of 4). The members agree on the sign of five of the six names.
SCT is the exception: Fable 5.1 sized it at exactly 0.

The members' sizes, as `impact_sum` / `abs_move_pct` / `p_up`:

| ticker | Opus 5 | Opus 5.5 | Sonnet 5.5 | Fable 5.1 |
| --- | --- | --- | --- | --- |
| AVARDA | +2.40 / 7.5 / 66 | +1.40 / 7.0 / 60 | +1.20 / 6.0 / 60 | +1.54 / 7.0 / 61 |
| VTU | +1.08 / 4.5 / 62 | +0.80 / 5.0 / 58 | +0.50 / 3.0 / 58 | +0.90 / 4.5 / 60 |
| BOOM | +0.65 / 6.5 / 55 | +0.75 / 7.5 / 55 | +1.10 / 7.0 / 58 | +0.24 / 6.0 / 52 |
| JHD | −0.70 / 3.5 / 40 | −0.32 / 4.0 / 46 | −0.20 / 2.8 / 47 | −0.30 / 3.0 / 45 |
| SCT | +0.18 / 4.5 / 52 | +0.27 / 4.5 / 53 | +0.10 / 3.5 / 52 | 0.00 / 3.5 / 50 |
| CRED_A | +0.08 / 2.0 / 52 | +0.07 / 1.8 / 52 | +0.10 / 1.8 / 52 | +0.06 / 1.5 / 50 |

**Where the panel and the hunter disagree most:** nowhere on sign. Each judge sized VTU at
roughly half the hunter's +1.6 and BOOM at about half or less, so the judges rank AVARDA
clearly first where the hunter has a tie. Two judges (Opus 5 and Opus 5.5) re-filed
AVARDA's rising loan-loss ratio, which the hunter had rejected as a duplicate, at −0.1.
No name is above the floor, so there is no unselected floor-clearer to report.

What these numbers are not:

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed, until Europe has about 200 panel
  names of its own.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but
  nothing about this market's panel is established.

## Top and bottom

**Top, AVARDA +1.60** (Avarda Bank, formerly TF Bank, Q3 interim report). This is the only
name of the day whose quarter's P&L has **not** been pre-released.

- **+1.5, the largest finding.** It is the hunter's own inference from the company's past
  releases. Operating profit rose from Q2 to Q3 by 21% in 2024 (157.7 → 191.3 MSEK) and by 18%
  in 2025 (195.1 → 230.9 MSEK). The 3.27 SEK EPS bar implies only about +10% QoQ. Sources:
  https://mfn.se/cis/a/tf-bank/tf-bank-ab-publ-interim-report-january-september-2025-9edae04f
  and https://mb.cision.com/Main/13973/4373343/4189231.pdf.
- **The bar.** It is one estimate (SB1 Markets) that Finwire reports as "i linje med
  konsensus" ("in line with consensus"):
  https://www.placera.se/telegram/avarda-bank-sb1-hojer-vinstprognoserna-for-avarda--upprepar-kop-20261008.
- **+0.6, the September-end loan book.** July and August are already public, at 27,407 MSEK
  ("Totala låneportföljen uppgick vid utgången av augusti månad 2026 till 27 407 MSEK", i.e.
  the total loan portfolio stood at 27,407 MSEK at the end of August 2026).
- **−0.5, capital headroom.** The hunter's own arithmetic puts total-capital headroom below
  the 2.5pp target.
- **The case against.** The sell-side may already model the seasonality.

**Bottom, JHD −0.60** (James Halstead, FY26 prelims).

- **What is already public.** FY26 sales and profit were pre-released on 22 July:
  https://www.investegate.co.uk/announcement/rns/james-halstead--jhd/trading-update/9680620.
  The prelims therefore carry about 0 on the reported year.
- **−0.5, FY27 outlook.** The company named a June pull-forward ahead of its July price
  increases, so the outlook starts from a weak base.
- **−0.4, audit delay.** BDO needed two more weeks to finish the audit; the company says it
  has "not been informed of any material audit issues":
  https://www.investegate.co.uk/announcement/rns/james-halstead--jhd/delay-in-publication-of-fy26-audited-results/9792824.
- **+0.3, dividend.** A 50th consecutive dividend increase is signalled and mostly priced.

## What could not be ranked

- **DEMANT (dk) has no event in the window.**
  - Demant's own 2026 financial calendar makes 14 October the start of its quiet period, not a
    report date:
    https://view.news.eu.nasdaq.com/view?id=b0bdfc2ea6d7161a83b5c1d7c7ef65070&lang=en&src=listed.
  - Its 9 October inside-information announcement dates the Q3 IMS to 3 November after
    17:00 CET:
    https://view.news.eu.nasdaq.com/view?id=ba0fd3fc4a25323136b3094846414492a&lang=en&src=listed.
  - That same announcement already published the Q3 figures and raised FY guidance.
  - The vendor and Nasdaq-fincal row is therefore a phantom, and the scorer excludes the name
    ("hunter found no event on this date").
  - The baseline stays sealed with `event_occurred: null`. It should be amended to `false`
    once the window has passed. Denmark is inside the Nasdaq Nordic feed's window, so
    `eu_resolve.py` should be able to reach that verdict if it runs within about a week.

## What the day is, before any pooled statement

- **Selection.** All 7 eligible names were hunted, which is under the cap of 20, so no random
  draw was needed (seed `eu-2026-10-14`). `by_market`: uk 4, se 2, dk 1, the other seven
  markets 0. Ten were scheduled; three fell below the $100k floor: RWA ($84k), ALSMA ($6k)
  and DUST ($82k).
- **Concentration.** `market_concentration`: the UK is 57% of the day (4 of 7), across 3
  markets. Of the 6 ranked names, the UK is 4.
- **Calendar sources.** UK RNS calendar: 5 dated for the day, of which RWA, BOOM and JHD were
  added and VTU and SCT confirmed. Inderes (SE) added CRED_A. Nasdaq Nordic fincal (DK) added
  DEMANT, which was the phantom. **Yahoo's quote calendar read `unavailable` on all ten
  markets** ("failed on every batch").
- **Sessions.** Five of the six ranked names carry `session_unresolved` from the seal (VTU,
  BOOM, CRED_A, SCT and JHD). Each hunter then found the release time or a consistent 07:00 /
  08:30 history pointing to bmo. AVARDA is the only one confirmed bmo in the seal.
- **No option anchor.** `options` is null in all ten markets, so Europe runs in the
  anchor-less regime (ρ=+0.073, p=0.45 over 104 events on the sealed corpus).
- **Short registers.** UK (FCA, as of 2026-10-12), SE (as of 2026-10-12) and DK (as of
  27-08-2026, position date 12-10-2026) all resolved.
  - **Only 2 of the 7 names carry `anchor_covered: true`**: JHD (0.2%) and DEMANT (3.94% on
    Denmark's 0.1% threshold, which is not comparable with the others' 0.5%).
  - Among the 6 ranked names, only JHD has an anchor. The other five are truncated zeros
    (`register_read_no_position`), and their `priced_lean_pct` is the run-up.
- **Weak legs.** No name came from Spain or Poland, and none from Germany. One name came from
  Denmark and two from Sweden. Those three markets can reach `event_occurred: false` only
  inside the Nordic feed's ~12-day window, so **resolve this run within about a week**.
- **Lean against the free control.** On the last resolved run (2026-10-08), UK
  `lean_vs_free_control_rho` was 1.0 on 3 names. On that few names it says nothing, but it is
  the reading. The lean's weights are priors borrowed from the US runs and measured nowhere
  in Europe.
- **History basis.** The UK names (BOOM, JHD, SCT, VTU) carry `observed_rns` history. AVARDA,
  CRED_A and DEMANT carry an **estimated** cadence (`estimated_from_cadence`), which is a
  scale, not a record of dates.
- **Pre-released periods (`already_public`).**
  - Most of the day's prints are pre-released periods. JHD (FY26 in July), SCT (FY26 and the
    first FY27 guide on 17 Sep), VTU (five of the six months, with the August upgrade) and
    DEMANT (Q3 on 9 Oct) all pre-released.
  - CRED_A's NAV can be about 84% worked out from public prices.
  - AVARDA and BOOM carry genuinely new P&L. On the first resolved days, pre-released periods
    moved about 3.1% against 7.4%, and the hunters' `abs_move_pct` follows that split
    (2.5–5.0 against 6.0–7.5).
- **Guidance (`new_in_release`).** A likely guidance or outlook line is flagged for JHD (FY27
  outlook), VTU (FY27 against the September car market) and BOOM (a statement against market
  expectations). None is a sourced, unpublished number.
- **Floor.** No name sits above `conviction_floor` 2.8. Over the whole US sample the sign was
  a coin flip below it.
- **Language notes.** Every hunter reported that the local sources added nothing the English
  ones did not, with two exceptions worth quoting:
  - AVARDA's bar and its Q1/Q2 consensus tables came **only** from Swedish wire copy (Finwire
    on placera.se).
  - SCT's TR-1, showing JPMorgan AM trimming its holding from 5.55% to 5.22% after the
    placing, was carried by no English article.
- **One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
