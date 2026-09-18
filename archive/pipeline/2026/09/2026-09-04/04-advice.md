# Earnings advice — 2026-09-04

Window: after Friday 2026-09-04 close through before Tuesday 2026-09-08 open (Monday 2026-09-07 is Labor Day; the window rolls to Tuesday). 2 names researched, 2 panelled — the day's universe was thin (5 raw candidates, 2 cleared the market-cap floor), so both eligible names went straight to deep dive with no triage screen, and both went to the full seven-persona panel.

## The calls

**ABM — ABM Industries Incorporated**
Call: **Neutral / No Edge**  ·  Unsigned band 3.6%–11.6% (event-implied ≈ ±8.26%)  ·  P(down) 52.8%  ·  Certainty Med  ·  Reversal risk 57.6 (Med)
Reason: the panel splits into a four-persona bearish cluster (KPI arithmetic, options positioning, red-team, insider forensics, all −18 to −22 on a stretched H2 margin bridge) against a two-persona bullish cluster (sentiment, macro/peers, +12/+14 on strong facilities-services peer momentum and an uncrowded stock).
Caveat: red-team reversal risk hits 70/100, the panel's ceiling, on a specific, well-sourced case — the FY26 guide needs +25–42% YoY H2 EPS growth after flat H1.
Dossier: `research/2026/09/2026-09-04/03-panel/ABM-dossier.md`

**UNFI — United Natural Foods, Inc.**
Call: **Neutral / No Edge**  ·  Unsigned band 5.1%–19.4% (event-implied ≈ ±10.7%)  ·  P(down) 51.5%  ·  Certainty Med  ·  Reversal risk 61.6 (High)
Reason: the panel is genuinely aligned near zero (disparity 26.5, the tightest of the day) — this is UNFI's fiscal Q4, which carries the first FY2027 guide from a CFO four weeks into the seat, and personas disagree about which way that single catalyst cuts rather than about the underlying facts.
Caveat: reversal risk peaks at 72/100 and the tier reads High even though direction is aligned — two of the last three Q4/initial-guidance-type prints in the historical sample were the two largest moves of the eight (+30.56%, +18.45%), so whichever way this breaks, it has tended to break big.
Dossier: `research/2026/09/2026-09-04/03-panel/UNFI-dossier.md`

Neither name cleared the conviction gate for a directional call. Both `signed_estimated_move` values are null by design — the synthesis script's Neutral / No Edge band sits within its own arithmetic (consensus scores of −8.9 and −4.4, both inside the ±24 Neutral band), not a hard gate override. No chair overrides were applied to either name; the panel's own numbers stood as computed.

## Ranked field

| Ticker | Company | Event-implied move | Preliminary direction (stage 2) | Evidence completeness | Panelled |
| --- | --- | --- | --- | --- | --- |
| ABM | ABM Industries Incorporated | 7.0% (stage-2 derivation; refreshed to 8.26% for the panel) | −18 | 80 | Yes |
| UNFI | United Natural Foods, Inc. | 10.6% (stage-2 derivation; refreshed to 10.7% for the panel) | −8 | 80 | Yes |

Both of the day's only two deep-dive dossiers were panelled — the universe was too thin (2 eligible names) for a ranked-but-unpanelled tier to exist today.

## What would change these calls

- **ABM:** a Q3 segment operating margin of 8.0%+ with an unqualified guidance reaffirmation would flip this bullish fast, since thin options liquidity (~88 contracts of open interest on the only usable expiry) means little dealer flow to absorb the move. The mirror case — any narrowing toward the low end of $3.85–$4.15, a margin print below 7.66% (last year's Q3 level), or a fresh self-insurance charge — would rerun the September 2025 script that has produced four −8% to −9% prints since FY24.
- **UNFI:** an initial FY2027 adjusted EBITDA guide at or above ~$750M with an explicit statement that reported wholesale sales grow (even net of the ongoing project-work drag) points toward the stock's historical +18–30% Q4/initial-guide template. A midpoint below ~$720M, or a refusal to guide FY27 sales growth at all, points toward the −10% to −17% template the stock has already printed twice this fiscal year.
- **Cross-name:** both prints land on the same post-Labor-Day Tuesday morning with no other major macro data (CPI/PPI/FOMC) in the immediate window, so the day's tape should reflect company-specific news rather than being swamped by a macro surprise — a rates-driven backdrop (10-year yield near cycle highs, elevated September rate-hike odds) was flagged by the macro persona on both names as a mild market-wide headwind, not a name-specific one.

## Coverage and caveats

- **Universe was thin by design, not by failure.** Only 5 raw candidates existed in the window and only 2 cleared the $500M market-cap and liquidity floors (WDH, CAN and GMHS were excluded). Stage 1 triage was skipped per config (universe ≤ 10), so neither name carries a `change_expectation` score from a scout screen — the ranking formula was renormalized to drop that term rather than fabricate a value (documented in `02-ranking.json`).
- **All seven panel seats were filled for both names** — no missing personas, no retries needed.
- **Anchors were refreshed for both names before the panel ran**, per the stage 3 protocol: spot and event-implied move were re-sourced same-day (both essentially unchanged from stage 2's pre-market figures) rather than carried stale from stage 2's early-morning research.
- **Both companies report the same morning (2026-09-08 BMO)** with no other confirmed reporters in the window, so this is a two-name day rather than a partial slice of a larger field.
- **No budget degradation was applied.** Stage 2 completed both batches cleanly and on schedule; both panel-eligible names received the full seven-persona panel per `panel.names=2` — no shedding to one name was needed.
- **Coverage gaps carried from stage 2 remain live caveats for both names**: ABM's options market is thin enough (88 contracts total OI) that its implied move is a rough derivation rather than a liquid market price; UNFI's FY2027 EBITDA figures circulating in sell-side commentary are analyst constructions, not company guidance, and the panel treated them as such throughout.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
