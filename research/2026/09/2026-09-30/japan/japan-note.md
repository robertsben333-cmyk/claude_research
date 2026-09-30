# Stage J — Japan researcher — 2026-09-30

**10 scheduled / 5 eligible / 5 hunted.**

- `selection.method`: "all 5 eligible names (at or under the cap)". No draw was needed, so the seeded draw (`jp-2026-09-30`) was not used.
- Five names fell to the ¥30m turnover floor: 192A, 2935, 3089, 9265 and 9651.
- Calendar sheets: `kessan07_0904` (as of 2026-09-03) and `kessan08_0918` (as of 2026-09-17). `market_closed` is null.
- Window: after the 15:00 JST close on 2026-09-30, scored close(09-30) → close(10-01).

## The ranking

| # | code | company | impact_sum | conviction | above floor (3.0) | priced_lean | baseline_quality |
| --- | --- | --- | ---: | ---: | :---: | ---: | ---: |
| 1 | 2685 | アンドエスティHD (and ST HD) | +1.50 | 1.50 | — | +0.42 | 0.725 |
| 2 | 2354 | YE DIGITAL | +1.00 | 1.00 | — | +2.38 | 0.688 |
| 3 | 2975 | スター・マイカHD (Star Mica) | +1.00 | 1.00 | — | −0.04 | 0.725 |
| 4 | 6083 | ERIホールディングス | +1.00 | 1.00 | — | −0.50 | 0.725 |
| 5 | 9369 | キユーソー流通システム (K.R.S.) | −0.80 | 0.80 | — | −0.51 | 0.725 |

The ranking key is `impact_sum`, as `edge-scores.json` reports it. All five names are rankable, and each carries exactly one finding. **None clears the conviction floor of 3.0.** Ranks 2–4 are a three-way tie at +1.00.

## What drives the top and bottom

### Top: 2685 アンドエスティHD, +1.5, lands on guidance

- Q1 operating profit was ¥7.9bn. For Q2 the hunter estimates ¥2.9–3.9bn, read from the August 月次: same-store sales −0.8%, but spend per customer +1.5% (+4.0% in August), which is the reduced discounting that lifted Q1 gross margin.
- Together that puts H1 operating profit near ¥11bn, about 65% of an unchanged ¥17.2bn full-year guide. Keeping the guide would imply H2 profit about 35% below last year.
- The last time the company ran this far ahead of its guide, in 2023, it raised the guide at H1.
- Why it is small: the one consensus source (IFIS, ordinary ¥19.4bn) already expects a raise, and this name sold a roughly 19% Q1 beat by −2.7%. The hunter emitted `expected_move_pct` +1.2.
- What may not be priced: the stock is −10% over 20 days, about 4–5 points worse than apparel peers, while consensus went up.
- Source: https://www.release.tdnet.info/inbs/140120260902530724.pdf

### Bottom: 9369 キユーソー流通システム, −0.8, lands on the reported quarter

- The H1 segment trends, applied to last year's Q3 base, put Q3 operating profit roughly flat year on year at about ¥1.38bn.
- The unrevised H2 plan implies a Q3 pace of about ¥1.47bn, so that is a miss of about 5% on operating profit.
- This stock traded operating profit year on year, not 経常 progress, when it fell −9.9% on the same mixed setup a year ago.
- Why it is small: the inputs are public and the stock is already −7% over 20 days. The hunter emitted −0.5.
- Source: https://tdnet-pdf.kabutan.jp/20260703/140120260703587699.pdf

### The middle three (tied at +1.00)

- **2354 YE DIGITAL (positioning).** The H1 miss was pre-released on 09-18 and the full-year guide was kept. Disclosed shorts have since built to about 5.3% (Barclays 2.33%, Goldman Sachs International 1.84%, Morgan Stanley MUFG 1.09%, calculation date 09-25) against the sealed 3.17%, going into a print with no new bad number. Against it: a margin-long overhang of about 8.8% of shares, and the name's history of weak reactions after pre-released prints.
  - Source: https://www.jpx.co.jp/markets/public/short-selling/t13vrt0000026855-att/20260929_Short_Positions.xls
- **2975 Star Mica (guidance).** H1 ordinary profit already covers 72.5% of the full-year guide, and the ¥5.0bn DBJ fund sale is booked in Q3, so an upward revision looks near-certain. IFIS consensus already sits 15.7% above the guide, which is why the finding is small.
  - Source: https://f.irbank.net/pr/20260727/140120260727599881.pdf
- **6083 ERI (reported quarter).** The company's own 月次 plus the rising completion-inspection fee per case point to Q1 ordinary profit of ¥0.95–1.05bn, against a ¥938m seasonal bar. This name has sold record prints that came without a raise (−15.1% in March 2026), so the hunter emitted +0.5.
  - Source: https://www.h-eri.co.jp/ir/finance/genjyo.html

**Names that could not be ranked:** none.

## What must be read with it

- **No option anchor; it is substituted.** `options` is all null. The lean comes from JPX's disclosed short register and 信用倍率. The lean weights are **priors with no Japanese measurement behind them**.
- **The short register was stale because of a defect, found today and fixed.** `jp_positioning.load()` returned the newest *cached* register file without asking JPX for a newer one.
  - Every stage J seal since 2026-09-19 therefore used the **20260918** file, including today's. The "11 days stale" in the 09-29 note was this bug, not JPX: JPX had files up to 20260929.
  - The 2354 hunter caught it by reading the newer files. The loader now checks JPX's index first (commit e336548), and the 20260929 file reads 2354 at 4.17%.
  - **Today's baselines stay sealed on 20260918 and were not revised.** 2354's short term is understated in its sealed lean. That affects the baseline and not the ranking key, because `impact_sum` is the hunters' sum and the 2354 hunter sized the newer register itself.
- **Which positioning components resolved.**
  - Register level: 2354 and 2685 are in the register. The other three are truncated zeros, meaning nothing disclosed at or above 0.5%.
  - 信用倍率: resolved on four names. 2354's is null because it is not a 貸借銘柄 and has no margin shorts.
- **`lean_vs_free_control_rho`: still not computable.** No Japanese run has had three or more resolved rows. Resolved events to date:
  - 09-24: 4716 scored −3.50, moved +8.15%.
  - 09-25: 3333 scored −2.50, moved +0.23%.
  - 09-25: 2742 scored −3.90, moved −1.15%.
  - 09-28: 8227 scored −0.50, moved +2.76%. Resolved this morning.
- **`history` is an estimated cadence**, not a record of dates: 11 estimated events per name, median absolute move 3.57–5.65%. That is a scale, and no date in it is a fact.
- **Daily 値幅制限 price limits truncate the tail**, so a large finding can be right and still not be paid in full.
- **Below the conviction floor.** Every name sits at |impact_sum| ≤ 1.5. Over the whole US sample the sign was a coin flip below the floor.
- **The lessons control is inert.** `researcher_japan/LESSONS.md` has no rules yet, and `pre_lessons` equals the final sum on all five names.
- **Three of five findings agree with the free control.** 2685, 2975 and 9369 all point the same way as their 20-day mean-reversion lean. What each adds is a dated mechanism, not an independent direction.
- **One day is not a result.** Five small numbers, three of them tied, carry almost no rank information.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
