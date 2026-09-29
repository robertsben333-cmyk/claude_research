# Stage J — Japan researcher — 2026-09-29

**8 scheduled / 4 eligible / 4 hunted.**

- `selection.method`: "all 4 eligible names (at or under the cap)". No draw was needed, so the seeded draw (`jp-2026-09-29`) was not used.
- Four names fell to the ¥30m turnover floor: 3607, 7068, 9253 and 9976.
- Calendar sheets: `kessan07_0904` (as of 2026-09-03) and `kessan08_0918` (as of 2026-09-17).
- `market_closed` is null.
- The window runs from the 15:00 JST close on 2026-09-29 to the next session.

## The ranking

| # | code | company | impact_sum | conviction | above floor (3.0) | priced_lean | baseline_quality |
| --- | --- | --- | ---: | ---: | :---: | ---: | ---: |
| 1 | 7921 | TAKARA & COMPANY | +1.00 | 1.00 | — | +0.05 | 0.725 |
| 2 | 3050 | DCMホールディングス | +0.50 | 0.50 | — | +0.12 | 0.725 |
| 3 | 8217 | オークワ OKUWA | 0.00 | 0.00 | — | +0.32 | 0.725 |
| 4 | 2792 | ハニーズHD HONEYS | −1.50 | 1.50 | — | +0.09 | 0.725 |

The ranking key is `impact_sum`, as `edge-scores.json` reports it. All four names are rankable. **None clears the conviction floor of 3.0.**

## What drives the top and bottom

### Top: 7921 TAKARA & COMPANY, +1.0 on the reported quarter

- The FY2026/5 決算短信 shows the order backlog at 2026-05-31 up **+23.0% YoY** (¥7,979m against ¥6,488m). The 金商法関連 part of it rose +35.8%.
- Q4 sales grew only +2.2%, so work was booked but not yet billed going into the June 有報 peak, which falls in Q1.
- Against the company's own guide (FY OP ¥4,900m, Q1 bar about ¥1.9–2.0bn at historical progress rates), the hunter puts Q1 OP near ¥2.0bn. That is `print_vs_bar_pct` of +3.
- Why it may not be priced: the July headline was the dividend and the medium-term plan, not the backlog, which sits on page 3 of the 短信.
- The finding is sized net of a weak read from Pronexus (7893), the listed peer: its organic Apr–Jun was flat and its 招集通知 volume fell.
- The hunter emitted `expected_move_pct` +0.8 rather than +1.0. The release comes at 15:00 while the TSE trades until 15:30, and last year's Q1 was sold −2.36% in the window.
- Source: https://tdnet-pdf.kabutan.jp/20260708/140120260707589312.pdf

### Bottom: 2792 ハニーズ, −1.5 on the reported quarter

- Honeys' own 月次 put Q1 (Jun–Aug) all-store sales at **93.3%** and 既存店 at 93.5% of last year.
- The H1 plan assumed 既存店 99.1%.
- Running that shortfall through the plan's gross-margin and SG&A lines puts Q1 OP near ¥0.45bn (range 0.25–0.7), against ¥1.21bn last year. That is about 20% progress on the ¥2.2bn H1 guide, against 37–44% in the last two years. `print_vs_bar_pct` is −45.
- **That OP figure is the hunter's own arithmetic from company numbers, not a sourced estimate.**
- The finding is sized small because the sales series has been public since 2 September.
- No analyst covers the name, and margin longs rose 81% into the print.
- Source: https://www.honeys.co.jp/ir/data_back/y/2027

### The middle two

- **3050 DCM, +0.5.** The Q1 over-delivery (OP 117% of the Q1 plan) outweighs the Q2 shortfall implied by the 月次, so H1 OP lands about 3.5% above plan. It is mostly public, and 5 of 7 recent prints faded at the close.
- **8217 オークワ, 0, no findings.** A 業績予想の修正 on 2026-09-25 cut H1 OP from ¥600m to −¥57m, which pre-releases the print. The tape took −3.36% on 09-28.
  - Its three prior pre-revised H1 prints gapped only +0.1% to +1.7%.
  - The release **time** is unconfirmed: the company's IR host resets the connection. Last year's H1 came out at 13:00 JST, inside the session, and if that repeats, most of the reaction lands before the window opens.

**Names that could not be ranked:** none.

## What must be read with it

- **No option anchor; it is substituted.** `options` is all null. The lean comes from JPX's disclosed short register and 信用倍率.
  - **All four names are absent from the register.** That is a truncated zero, meaning nothing at or above 0.5%, with no change.
  - So on every name the lean is only `margin_overhang` plus `runup`. Two of the three positioning components resolved, the register level and the margin ratio. The short-register change is identically zero.
  - **The register file is dated 2026-09-18, eleven days before the seal**, so the level and the change are that stale.
  - The lean weights are **priors with no Japanese measurement behind them.**
- **`lean_vs_free_control_rho`: still not computable.** Japan has three resolved events in total:
  - 09-24: 4716, scored −3.50, moved +8.15%.
  - 09-25: 3333, scored −2.50, moved +0.23%.
  - 09-25: 2742, scored −3.90, moved −1.15%.
  - The resolver computes no statistics under three rows per run, so no lean-vs-control check exists yet.
- **`history` is an estimated cadence**, not a record of dates. Median absolute moves are 2.27–2.97% over 11 estimated events per name. That is a scale, and no date in it is a fact.
- **Daily 値幅制限 price limits truncate the tail**, so a large finding can be right and still not be paid in full.
- **Below the conviction floor.** Every name sits at |impact_sum| ≤ 1.5. Over the whole US sample the sign was a coin flip below the floor.
- **The lessons control is inert.** `researcher_japan/LESSONS.md` has no rules yet, and `pre_lessons` equals the final sum on all four names.
- **Three of the four names are retailers with public 月次.** Most of what the print reveals about sales is already out, and every hunter sized small for that reason. 8217 is a pre-revised name for LESSONS open question 3.
- **One day is not a result.** Four small numbers on one day carry almost no rank information.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
