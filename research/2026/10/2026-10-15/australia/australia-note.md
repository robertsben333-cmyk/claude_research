# Stage AU — Australia researcher — 2026-10-15

**1 scheduled, 1 eligible, 1 hunted, 1 rankable, 0 above the conviction floor.**
`selection.method`: all 1 eligible names (at or under the cap of 20), so there was no
random draw (seed `au-2026-10-15` unused). `session_unresolved`: 0 of 1. 1,571 vendor
rows were scanned and dates were shifted to Sydney time (`event_date_basis`: converted
from the vendor's UTC instant). The baseline was sealed Wed 2026-10-14 at 06:42 UTC, after
the Sydney close, for Thursday's session. Each hunter ran one English pass with
`pre_lessons` frozen. `LESSONS.md` is empty, so the freeze changed nothing, which is the
correct result.

## The ranking

The ranking key is `impact_sum` (from `edge-scores.json`) and the conviction floor is 2.8.
**One name cannot be ranked against anything.** The table records its size and nothing
more.

| rank | ASX | company | session | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | priced_lean | short % (08/10) |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | BOQ | Bank of Queensland | bmo | +0.40 (p32) | +0.33 (p40) | 5.5 | 53 | +2.22 | 4.486 |

**What drives it.**

- **Largest positive (+0.5):** the 1H26 deck guides 2H margin tailwinds from rising cash
  rates, TD spreads and hedging, and peer BEN has already printed a 2H26 NIM of 1.98%,
  +6bp HoH. Source: https://announcements.asx.com.au/asxpdf/20260422/pdf/06yqnk5f5h2d6l.pdf
- **Largest negative (−0.4):** APRA's monthly ADI statistics show BOQ's resident housing
  loans falling from $52,790m (Feb 2026) to $50,731m (Aug 2026), −3.9% over 2H26. That is
  the same pace as 1H, against the company's guide that the contraction was easing.
  Source: https://www.apra.gov.au/system/files/2026-09/Monthly%20authorised%20deposit-taking%20institution%20statistics%20back-series%20March%202019%20-%20August%202026.xlsx
- **The rest:** a capital surplus with most of the buyback unspent (+0.4); the 2H notable
  items, pre-released on 10 Aug (0.0); a possible further statutory hit from the
  Challenger loan sale (−0.1).
- **The hunter's verdict:** a near non-result. The pre-print shocks were all disclosed on
  10 Aug 2026.
- **Event confirmed:** the ASX "FY26 Results Webcast" notice of 6 Oct sets results for 15
  Oct, with a briefing at 10:00 AEDT. All five prior results were lodged 08:15–08:43
  Sydney.

**Not ranked:** none.

## The four-model panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1) re-sized the hunter's
evidence. **The panel ranks beside `impact_sum` and replaces nothing.** All four members
ran on their pinned agents, with no fallback.

| rank | ticker | selected | consensus_k | sign agreement | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | impact_sum |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | BOQ | no | 0 | 4/4 | +0.34 | +0.50 | +0.18 | +0.18 | +0.53 | +0.40 |

- **No name was selected.** No member put BOQ in its own top 20%.
- **The judges agree with the hunter.** All four are mildly positive, with member sums
  from +0.2 to +0.96. Opus 5 and Fable 5.1 sized both the APRA volume finding (−1.3) and
  the capital surplus (+0.9 to +1.4) larger than the hunter did. The net is still small.
- **What the panel numbers are not:**
  - `panel_score` ranks; it does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.
  - The member scales are mostly the frozen E-P seed.
  - In the four-model re-judge, the judges ranked Australia WORSE than the live hunt.

## What this market carries that the number does not

- **Filer-type mix:** 1 of 1 is `results` (a full-year Appendix 4E, FY ending 31 Aug).
  There were no 4C/5B quarterly cash-flow filers today. The baseline's five-print history
  was read cleanly from the ASX archive. Those are observed lodgement dates, with a median
  |reaction| of 5.54%.
- **Register lag: 4 sessions.** The ASIC file is as of 2026-10-08: 4.49% short, up 0.26pp
  from 10-01. That shows shorts "building", but over a period that ended before the seal.
  Since then the stock went 6.38 → 6.69 → 6.49, including −3.0% on 14 Oct with the sector
  (BEN −3.5%, CBA −2.2%).
- **The lean is +2.22**, made of short_squeeze +2.69, short_building −0.52 and runup
  +0.05. Its weights are **priors carried over from stage J**, with no Australian
  measurement behind them.
- **`lean_vs_free_control_rho`:** the last resolved run that could compute it is
  2026-09-28, which read **0.262 over 8 names**. The 2026-09-30 run could not compute it,
  with only 4 names. The 0.80 at validation has not recurred.
- **Conviction floor:** BOQ sits far below the 2.8 floor. Over the US sample, the sign
  below the floor was a coin flip.
- **No option anchor.** This stage runs anchor-less, in the regime
  `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073 (p=0.45) over 104 events.

**What the day does not establish:** nothing has resolved in Australia that ranks.
A single name cannot be ranked. A +0.40 against a 5.5% expected move is a non-result, not
a direction.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
