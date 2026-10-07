# Edge hunt — 2026-10-07 window (2026-10-07 amc + 2026-10-08 bmo)

The Routine fired at 17:04 UTC (13:04 New York). All ten hunts were finished by 17:23 UTC, before every release: the four amc names report after today's 16:00 ET close and the six bmo names report tomorrow before the open. Ranking key, per `edge-scores.json`: **`impact_sum`**. **One name clears the 2.8 conviction floor: RELL.** The same name, and only that name, clears the book's `impact_scaled` floor of 1.76.

| # | ticker | session | pre-lessons | **post-lessons (key)** | scaled | V2 | floor | tradable | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RELL | amc 10-07 | +5.00 | **+4.80** | +3.00 | +3.56 | **yes** | yes, long, $2.3m/day, ok | −8.32 |
| 2 | LEVI | amc 10-07 | +2.40 | **+2.10** | +1.20 | +1.20 | no | yes, long, $56.1m/day, ok | +3.14 |
| 3 | APLD | amc 10-07 | +1.50 | **+1.30** | +0.66 | +2.25 | no | yes, long, $413.7m/day, ok | +11.82 |
| 4 | ANGO | bmo 10-08 | +0.50 | **+0.30** | +0.75 | +0.25 | no | yes, long, $8.5m/day, ok | +6.66 |
| 5 | TLRY | bmo 10-08 | +0.40 | **+0.30** | +1.00 | +0.06 | no | yes, long, $14.0m/day, ok | +11.28 |
| 6 | PEP | bmo 10-08 | +0.40 | **+0.20** | +0.27 | +0.05 | no | yes, long, $1,153m/day, ok | +9.18 |
| 7 | NG | bmo 10-08 | +0.00 | **+0.10** | +0.00 | −0.20 | no | yes, long, $35.6m/day, ok | +21.05 |
| 8 | BYRN | bmo 10-08 | −1.20 | **−0.40** | −1.20 | −0.56 | no | yes, short, Alpaca lends, $1.1m/day, ok | −5.57 |
| 9 | RGP | amc 10-07 | −0.40 | **−0.50** | −0.90 | −0.44 | no | yes, short, Alpaca lends, $1.3m/day, ok | +3.62 |
| 10 | HELE | bmo 10-08 | −1.30 | **−0.60** | −0.84 | −0.50 | no | yes, short, Alpaca lends, $10.5m/day, ok | +8.71 |

Three columns are measured beside the key and are not the key: pre-lessons, scaled and V2. V2 is calibrated today on 186 ledger observations. The book selects on `impact_scaled` ≥ 1.76 (since 2026-10-02); see Execution. Borrow was asked live, because no plan existed when `assets` ran.

## Top and bottom

- **RELL +4.80.** Two findings drive it, each +2.0, both landing on the reported quarter.
  - **The street bar looks low against the peers.** It has revenue falling 11% sequentially (from $66.2m to $59.0m, EPS $0.09). Meanwhile every semi-equipment peer that reported after RELL last spoke accelerated over RELL's June–August quarter. Applied Materials posted a record $9.12bn and guided Q4 to $10.25bn against $9.54bn expected: https://www.appliedmaterials.com/us/en/newsroom/press-releases/081326-applied-materials-announces-third-quarter-2026-results.html. Advanced Energy, MKS and Tokyo Electron reported strong quarters too.
  - **Backlog is up against a flat bar.** Year-end backlog was $164.4m, +22.5% y/y, with "faster turns than prior years": https://www.rell.com/webfoo/wp-content/uploads/2026/08/RELL-Q4-FY26-Investor-Presentation-Midwest-IDEAS-Conf-Final.pdf.
  - **Smaller items.** Short interest is 9.2% of float with 9.0 days to cover (+1.0). Nine insiders sold after July (−0.5).
  - **What the price already says.** The stock is +8.3% over 20 days and +6.4% over 5 days. The option-implied move is 13–14%, and skew is mildly call-rich.
- **HELE −0.60.** The largest negative finding is the bar. Revenue consensus of $443.2m sits at the top of the company's own first-half sales guide (−0.7). A possible Phase 2 tariff refund on the $71m still owed could fall into adjusted EPS (+1.0), and 12.8% of float is short. These are netted against each other, not resolved, and the table's flags say so. The price already shows −8.7% over 20 days and −9.0% over 5 days, and HELE fell 10.2% on its last print, when it raised sales guidance and held EPS.

## Critical read of the floor-clearer

**RELL (+4.80, scaled +3.00).**
- **What it lands on.** 4.0 of the 4.8 points sit on the `reported_quarter`. One of the two big findings is a *peer proxy*: other companies' quarters, not RELL's own numbers. The other is a public company figure. LESSONS says a narrow proxy is a hypothesis, and the hunter's conviction note calls this "a lean built on a proxy plus a public company number".
- **Whether the hunter's two numbers agree.** They agree in sign: print_vs_bar +5.0%, expected move +3.0%. The expected move is 63% of the sum of the findings, so the caveats mostly reached the key.
- **The bar and positioning.** The bar is sourced and two aggregators agree (MarketBeat $0.09; EarningsWhispers $58.99m revenue). This is a long, so the 9.2% short base is tailwind rather than a crowded-short risk.
- **The worry.** The stock has already run +8.3% into the print and sits near the post-July high. That is the `-run_up_20d` control pointing the other way: the free control ranks RELL **last** of ten.
- **Liquidity.** $2.3m a day is above the $1m thin line but small; a 33–50% equity position would be a large share of a day's volume.
- **Flags.** None.
- **Verdict: recommended with a named reservation.** The reservation is that half the size rests on a peer proxy, in a name that has already run into the print, and the free control disagrees.

## Names not ranked

None. All 10 rows were confirmed by the sweep from company sources, with sessions settled: 0 phantoms and 0 unsettled. No `time-not-supplied` rows were added: the window had exactly 10 names, so the thin-day check was not triggered.

## Standing caveats

- **Order versus sign.** Below the floor the sign has been a coin flip, 53% over 38 events. Above it, the rank of conviction predicted whether the sign was right at ρ=+0.514. Nine of ten names today are below the floor, so read their signs as an order and not as views. `impact_sum` ranks and does not size the move; two findings on one fact are double-counted.
- **Control.** The hunt's order against −run_up_20d gives a Spearman of **−0.17** on these ten names: the two order the day almost oppositely. The control ranks NG top and RELL bottom. The hunt has not yet been shown to beat this free control, and on the larger sample the control itself stopped working (−0.42% per trade over 105 events).
- **Sign balance.** 7 names lean positive and 3 lean negative. Seven of ten hunts were near non-results, |impact_sum| ≤ 0.6.
- **Nothing checked the findings.** There was no adversary and no second hunter, so a wrong fact enters the key at full size. In past paired hunts the key differed by a median of 2.40 points and 4 of 12 pairs had opposite signs, which is larger than every row today except RELL.
- **How much of the baseline was measured.** 8 of 10 names have a live option chain. RGP and BYRN have unusable chains and run on the historical-median fallback. BYRN's reaction history is also mixed with pre-announcements, and the sweep marked it untrustworthy.
- **Capacity.** All ten clear the $200k turnover floor and none is thin, though BYRN ($1.1m) and RGP ($1.3m) are close to the line. The top of the table, RELL, is reachable at $2.3m a day.
- **One day is an anecdote.** Ten names cannot produce a meaningful rank correlation; the pooled number is the result.

## Execution

`execution.enabled` is true. **No order was placed.** The session's auto-mode permission classifier refused the broker calls as "Real-World Transactions", the same block recorded on every run since 2026-09-28.
- **Step 0b.** `verify --scan … --fix --submit` was refused, so `close` and `status` were not run. Whatever bmo exit legs were due today were not sold from this session, and nothing here re-reads the account.
- **Step 7.** `plan` ran, since it is read-only. It priced equity at $11,201 and selected **one name: RELL long, 193 shares, $3,679 notional, 32.8% of equity**, entry 2026-10-07 and exit 2026-10-08 (amc → the opening print). `open --submit --no-flatten` was then refused. The plan is on disk as `alpaca-plan.json`.

Result: 0 orders, 0% gross. Nine names were not traded, all below the 1.76 `impact_scaled` floor. The fix is a narrow allow rule for `researcher_us/scripts/alpaca_trade.py` in `.claude/settings.json`, which a session may not write itself.

## Context: retail, search and volatility (not used for selection)

These are context only. Nothing ranks, selects, sizes or trades on them.
- RELL: retail 52 (yes), search sparse, vol 43% (no)
- LEVI: retail 28 (no), search sparse, vol 21% (no)
- APLD: retail 63 (yes), search 1.32x (not quiet), vol 71% (yes)
- ANGO: retail 53 (yes), search sparse, vol 31% (no)
- TLRY: retail 70 (yes), search sparse, vol 41% (no)
- PEP: retail 13 (no), search 1.23x (not quiet), vol 14% (no)
- NG: retail 61 (yes), search failed, vol 54% (no)
- BYRN: retail 72 (yes), search sparse, vol 46% (no)
- RGP: retail 63 (yes), search sparse, vol 37% (no)
- HELE: retail 57 (yes), search 0.38x (quiet), vol 41% (no)

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
