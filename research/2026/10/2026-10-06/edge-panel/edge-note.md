# Edge hunt (panel): 2026-10-06 amc

**This is stage E-P. Opus 5.5 searchers gathered the evidence, a blind panel of four models judged it, and no orders were placed.**
All four members ran on their pinned models: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. No fallback was used.
One day of six names is an anecdote. It is not a measurement of the panel.

## Window

`edge_universe.py --window` gave 6 of 14 calendar rows, all 2026-10-06 amc. There were 0 bmo rows for 10-07 with a stated session.

The day was thin, so the time-not-supplied rows were checked as well. That added one name, ARTW. `session_resolve.py` left it unresolved and the only evidence for it is the cadence prior, so it was not hunted.

The sweep confirmed **6 of 6** against each company's own release, with 0 phantoms and 0 sessions unsettled. Baselines were sealed at about 17:07 UTC, before any searcher launched. Three of the six have a live option chain (STZ, PENG, NEOG). WS, SAR and AXIL use the historical-reaction fallback.

## The panel table

Columns:

- **k** is the number of members that put the name in their own top 20% on the panel's side.
- **agree** is sign agreement across the four members.
- The member columns show each member's z against its own history; `*` means the name is in that member's top 20%.
- **searcher** is the searcher's own `impact_sum`.

| # | ticker | session | selected | k | agree | panel_score | opus5 | opus55 | sonnet55 | fable51 | searcher | expected_edge_pct | weight_equal | weight_precision_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PENG | 10-06 amc | **yes** | 4 | 4/4 | +2.58 | +2.12* | +1.27* | +3.78* | +3.03* | +4.40 | +3.35 | 1.0 | 0.90 |
| 2 | NEOG | 10-06 amc | **yes** | 4 | 4/4 | +2.11 | +1.38* | +2.08* | +2.60* | +2.14* | +2.00 | +3.35 | 1.0 | 1.25 |
| 3 | WS | 10-06 amc | **yes** | 3 | 4/4 | −1.25 | −1.38* | −0.74 | −1.34* | −1.16* | −0.80 | −3.35 | 1.0 | 1.00 |
| 4 | AXIL | 10-06 amc | – | 0 | 4/4 | +0.65 | +0.39 | +0.67 | +1.00 | +0.62 | +0.50 | – | 0 | 0 |
| 5 | STZ | 10-06 amc | – | 0 | 4/4 | +0.58 | +0.64 | +0.82 | +0.41 | +0.53 | +0.60 | – | 0 | 0 |
| 6 | SAR | 10-06 amc | – | 0 | 4/4 | −0.38 | −0.29 | −0.45 | −0.31 | −0.48 | −0.80 | – | 0 | 0 |

Turnover (spot × 20-day volume, from the sealed baselines):

| name | turnover per day | note |
|---|---|---|
| STZ | $253m | |
| PENG | $95m | |
| NEOG | $57m | |
| WS | $13m | |
| SAR | $2.2m | |
| AXIL | $0.08m | below the $200k floor, so it is not tradable at size |

Borrow and the tradable column were not looked up: this stage makes no `alpaca_trade.py` call of any kind.

## The selected names

**PENG, selected 4/4, long side.** All four members rest on the same three things:

- FY27 consensus EPS ($3.38) still equals the company's 7 July preliminary +30% view.
- DRAM contract prices (TrendForce) and module-maker ADATA's June–August revenue both point to Memory above the July guide.
- This name has moved on guidance: +25% and +13% on its last two raises, −14% on a hold.

The searcher filed a 14% of float short that built 9.5% month on month, against a calls-bid chain (skew −23.7).

The strongest case against:

- The evidence is proxies, not company documents.
- The stock has run +15.7% in 20 days. It also rose +11.6% on a 2 Oct "expects a raise" note.
- DRAM price increases are slowing sharply (+58–63% → +13–18% → +10–15% a quarter).
- Micron's blowout guide on 30 Sept was sold.

Opus 5.5 is the most cautious member at +1.7, for exactly these reasons. PENG is the searcher's only name above the 2.8 floor.

**NEOG, selected 4/4, long side.** The members rest on one pattern. The Q4 FY26 actual beat the guide implied in April by about 5% on revenue and 6.6% on EBITDA. The CFO said targets are set to rebuild credibility, and Q1 consensus sits at the midpoint of the guide. The name has paid well for beats (+22.7%, +31.6%, +16.5%).

The strongest case against:

- The put skew is +15.3, so downside is being paid for.
- Q1 is a pre-guided quarter.
- An Investor Day at 09:00 ET on 10-07 falls inside the window. It widens the move without telling us which way.
- The Zoetis Genomics sale is still waiting on two antitrust regulators.

**WS, selected 3/4, short side.** Opus 5.5 was the one member that did not put it in its top 20%.

The case rests on WS's own pro forma in its 8-K/A. It puts combined EPS near $0.19 a quarter after the 7.75% notes, the SOFR+400 term loan and the 38% Klöckner minority. The visible aggregator bar is $1.16, but it is a standalone number that excludes Klöckner. The stock also ran +10% in five sessions with no catalyst found, and has fallen on 6 of its last 7 prints.

The strongest case against:

- Klöckner's own Q2 2026 EBITDA was €63m, with "Q3 started strong". That run-rate is about €17m a quarter above what the pro forma carries.
- The covering analysts' combined models are not public. They may already hold the dilution, and then the $1.16 bar is a strawman.
- Revenue will print at about 3× every aggregator bar for purely mechanical reasons.

## Where the panel and the searcher disagree

- **WS**: the panel is more negative than the searcher (Opus 5 −2.8 against the searcher's −0.8). The searcher capped every finding for the disputed bar; the judges let the pro forma carry more weight.
- **PENG**: Opus 5.5 at +1.7 against a searcher +4.4 and three judges at +4.1 to +4.4. It discounted the half that the skew and the run-up already price.
- **SAR**: the searcher's −0.8 is the most negative read. The judges sit at −0.6 to −0.7 raw because the bear case is largely priced at 0.69× NAV and an 18.8% yield.

## Comparison with stage E

Stage E's `edge-scores.json` exists. All 6 names are ranked by both stages.

| stock | stage E `impact_sum` | panel_score |
|---|---|---|
| PENG | +2.8 | +2.58 |
| NEOG | +1.5 | +2.11 |
| SAR | +0.4 | −0.38 |
| STZ | +0.2 | +0.58 |
| AXIL | −0.1 | +0.65 |
| WS | −1.5 | −1.25 |

**Spearman ρ = 0.77** (n = 6). The top two and the bottom name agree. SAR and AXIL change places, and their signs flip between the two stages.

## What the numbers are not

- **`expected_edge_pct` (±3.35) is a shrunk in-sample prior** from the judge-lab development names (selected names went 18/24, +6.7% net). It is not a forecast for these three names.
- **The weights are research only.** Nothing trades them.
- **The members' `p_up` is recorded and decides nothing.** It was not monotonic on the development names.
- **`panel_score` reads size against each member's own history.** It is not a probability.
- **Below the floor, the searcher's sign has been a coin flip**: 53% over 38 events.
- **Nothing checked the findings for factual error.** There is no adversary pass.
- **The key is not reproducible to better than its own size.** When pairs were double-hunted, the median gap was 2.4 points, and 4 of 12 pairs had opposite signs.
- **The free control** `-run_up_20d_pct` would rank SAR (−8.4%) and STZ (−4.6%) top and PENG (+15.7%) bottom. That is close to the reverse of the panel's ranking.

## Context: retail, search and volatility (not used for selection)

These labels come from `edge_context.py` and are context only.

| name | retail tilt ≥ 50 | search spike under 1.0x | 20-day vol ≥ 58% |
|---|---|---|---|
| PENG | yes (61) | sparse | yes (74) |
| NEOG | yes (62) | no (1.19x) | no (53) |
| STZ | no (24) | no (1.15x) | no (19) |
| AXIL | yes (59) | sparse | no (44) |
| SAR | no (43) | sparse | no (21) |
| WS | no (40) | sparse | no (41) |

V2 grounded (`edge-scores-grounded.json`) was written at 17:22 UTC, before the 20:00 UTC releases, for 6 of 6 names.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
