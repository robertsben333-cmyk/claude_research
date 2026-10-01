# Stage J — Japan researcher — 2026-10-01

**6 scheduled / 4 eligible / 4 hunted.**

- `selection.method`: "all 4 eligible names (at or under the cap)". No draw was needed, so the seeded draw (`jp-2026-10-01`) was not used.
- Two names fell to the ¥30m turnover floor: 2493 イーサポートリンク (¥1.9m/day) and 5942 日本フイルコン.
- Calendar sheets: `kessan07_0904` (as of 2026-09-03) and `kessan08_0918` (as of 2026-09-17). `market_closed` is null. Every hunter re-confirmed the 10/01 date against the issuer or kabutan.
- Window: after the 15:00 JST close on 2026-10-01, scored close(10-01) → close(10-02).

## The ranking

| # | code | company | impact_sum | conviction | above floor (3.0) | priced_lean | run-up 20d |
| --- | --- | --- | ---: | ---: | :---: | ---: | ---: |
| 1 | 7545 | 西松屋チェーン (Nishimatsuya) | +1.60 | 1.60 | — | −0.11 | −2.99% |
| 2 | 7447 | ナガイレーベン (Nagaileben) | −1.00 | 1.00 | — | −0.44 | −3.88% |
| 3 | 8276 | 平和堂 (Heiwado) | −1.60 | 1.60 | — | +0.33 | −4.24% |
| 4 | 3549 | クスリのアオキHD (Kusuri no Aoki) | −2.00 | 2.00 | — | +0.15 | −10.72% |

The ranking key is `impact_sum`, as `edge-scores.json` reports it. All four names are rankable. **None clears the conviction floor of 3.0.** `baseline_quality` reads 0.6 on all four, below the 0.725 of earlier runs, because the short register is a truncated zero for every name.

**The hunt's order is exactly the reverse of the free control's.** `-run_up_20d_pct` puts 3549 first (−10.7% over 20 days) and 7545 last. On four names that is a rank correlation of −1.0, which arrives by chance one time in 24, and it is not evidence of anything. It does mean that tomorrow, the hunt and the control cannot both be right.

## What drives the top and bottom

### Top: 7545 西松屋チェーン, +1.6, lands mostly on capital return

- **+1.2, capital return.** Every H1 and FY release since October 2024 has come with a ¥500m buyback. At those prints the stock opened +3.1 / −0.1 / +4.9 / +7.2 / +4.7, against a mean of −2.5 at Q1/Q3 prints, which carry no buyback. A repeat is likely today, and nothing in the tape is building for one.
  - Source: https://tdnet-pdf.kabutan.jp/20251001/140120251001566503.pdf
- **+0.7, guidance.** September same-store sales were +12.4%, which supports holding the FY guide. The stock has fully given back its reaction to that release, and IFIS consensus is still 4% under the guide.
- **−0.3, reported quarter.** The 月次 put H1 operating profit about 1% light of plan.
- **Caveat.** The capital-return pattern rests on five prints and is a habit, not an announcement. The hunter emitted `expected_move_pct` +1.4.

### Bottom: 3549 クスリのアオキHD, −2.0, lands on the reported quarter

- **The finding.** Q1 existing-store sales ran about 99.5% (97.5 / 100.3 / 100.7) against the 102.9% H1 premise behind a +14.9% H1 OP guide. That puts Q1 ordinary profit near ¥6.8–7.1bn: 46–48% of the H1 plan, against the 62.6% five-year average progress rate that kabutan prints automatically. Last year's Q1 gapped −5.5% on a smaller miss with a normal progress rate.
  - Source: https://tdnet-pdf.kabutan.jp/20260904/140120260904531805.pdf
- **Why only −2.0.** The monthly figures are public, and the stock is already −10.7% over 20 sessions against −4% to −7% for its peers. The two sell-side Q1 bars disagree: IFIS ¥7.35bn, against about ¥6.4bn implied by Yahoo's single-analyst EPS. Oasis (16.14%) has been buying.
- **Outside the window.** An unused ¥24bn buyback authorisation (0 shares bought by 08-31) and the Oasis activism are undated, so neither is in the sum.

### Middle

- **7447 Nagaileben (−1.0).** FY8/26 will miss a never-revised guide by about 10% at OP, the third straight miss. The October prints fell −7.0% and −5.3% on the same headline. But IFIS already sits at the miss, so the miss finding is sized −1.0. Two smaller findings offset each other: +0.5 for a lowered FY27 bar and −0.5 for a completed buyback while Fidelity sells down from 9.30% to 7.34%.
  - Source: https://kabutan.jp/stock/news?code=7447&b=k202606290005
- **8276 Heiwado (−1.6).** H1 OP will miss the company plan by an estimated 10–15% (≈¥6.15bn against ¥6.9bn), with Q2 down YoY.
  - Source: https://www.heiwado.jp/ir/sales/monthly
  - **Timing risk.** Heiwado released at 13:30 JST, *during the session*, on its prints from 2024-10 to 2026-04; the most recent one, Q1 on 2026-06-25, came at 15:30. If it does so today, part of the reaction lands before the sealed close(10-01) and outside the scored window.

**Names that could not be ranked:** none.

## What must be read with it

- **No option anchor; it is substituted.** `options` is all null. The lean comes from JPX's disclosed short register (file 20260929) and 信用倍率. The lean weights are **priors with no Japanese measurement behind them**.
- **Which positioning components resolved today.**
  - Register: a truncated zero on all four names (no holder at or above 0.5%), so `short_squeeze` and `short_building` carry nothing today.
  - 信用倍率: resolved on all four. Two hunters say it is distorted:
    - 8276 (0.58): the hunter reads it as a 株主優待 cross-trade artefact.
    - 7447 (18.23): the hunter reads it as the dividend-record cross unwinding.
  - In practice today's lean is the run-up plus a noisy margin term.
- **`lean_vs_free_control_rho`.** The 2026-09-29 run was resolved this morning: 4/4 usable, **`lean_vs_free_control_rho` = −0.4**. That is not near 1.0, so the lean has not collapsed into the free control. It is also four names, and its sign is noise.
  - On that same run the hunt ranked at ρ −0.6 (p 0.42), against +0.4 for the free control. One day is not a result.
- **`history` is an estimated cadence**, not a record of dates. It is a scale for how much the name moves, and no date in it is a fact.
- **Daily 値幅制限 price limits truncate the tail**, so a large finding can be right and still not be paid in full.
- **Below the conviction floor.** Every name sits at |impact_sum| ≤ 2.0. Over the whole US sample the sign was a coin flip below the floor.
- **The lessons control is not clean today.** `researcher_japan/LESSONS.md` still has no rules. 8276's `pre_lessons` (−1.9) differs from its key (−1.6), but the hunter attributes the change to its own re-check (it folded a same-document tax finding into the main one), not to the lessons file. The scorer counts it as "moved by lessons". It was not.
- **Correlated exposure.** Three of the four names are domestic retailers (drugstore, supermarket, children's apparel), and two are Hokuriku/Kansai regional chains that sold off with their peers this week.
- **One day is not a result.** Four small numbers carry almost no rank information.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
