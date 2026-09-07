# Earnings advice — 2026-09-07

Window: after Monday 2026-09-07 close (Labor Day, no trading) through before Tuesday 2026-09-08 open. 2 names researched, 2 panelled — the day's universe was thin (6 raw candidates, 2 cleared the market-cap floor), so both eligible names went straight to deep dive with no triage screen, and both went to the full seven-persona panel.

**Note on this run:** ABM and UNFI's 2026-09-08 BMO print was already given a full panel on 2026-09-04, whose window rolled through the Sept 7 Labor Day holiday to the same Sept 8 open (`research/2026/09/2026-09-04/04-advice.md`). Today's run is a fresh, independent re-panel one day closer to the print, with all seven personas re-researching from scratch and anchors re-sourced today rather than carried forward. It is not a correction of the earlier note — both stand as independent reads at different distances from the event.

## The calls

**ABM — ABM Industries Incorporated**
Call: **Neutral / No Edge**  ·  Unsigned band 3.7%–11.8% (event-implied ≈ ±8.4%)  ·  P(down) 55.9%  ·  Certainty Med  ·  Reversal risk 60.6 (High)
Reason: all seven personas land in a tight -12 to -20 bearish cluster on a stretched back-half FY26 margin bridge (H1 adjusted EPS flat YoY, requiring +24–42% H2 growth), but the consensus score of -16.7 sits inside the mechanical Neutral band and four of seven personas leaned in part on the same single source for a shared "no squeeze fuel" framing element — certainty was chair-overridden down from a mechanical High to Med as a result.
Caveat: red-team reversal risk hits 65/100 on a specific, sourced case (a margin-inflection bar after two straight contraction quarters), but ABM has repeatedly not been punished for exactly this kind of miss — three of the last four large EPS misses produced flat-to-up sessions.
Dossier: `research/2026/09/2026-09-07/03-panel/ABM-dossier.md`

**UNFI — United Natural Foods, Inc.**
Call: **Neutral / No Edge**  ·  Unsigned band 5.2%–24.2% (event-implied ≈ ±11.7%)  ·  P(down) 53.8%  ·  Certainty Med  ·  Reversal risk 61.5 (High)
Reason: six of seven personas lean mildly bearish (-6 to -25) on a first FY2027 guide from a CFO four weeks into the seat, but one persona (options-positioning, +12) genuinely dissents on de-risked, call-heavy positioning — a real disagreement, not shared sourcing, keeping the consensus at -11.7 and disparity at 24, the widest spread of the day.
Caveat: reversal risk peaks at 68/100, the panel's ceiling, on a case built around the very same new-leadership catalyst the bear case rests on; UNFI's own fiscal-Q4/initial-guidance prints have produced its two largest historical moves (+18.45% and larger), so whichever way this breaks, it has tended to break big.
Dossier: `research/2026/09/2026-09-07/03-panel/UNFI-dossier.md`

Neither name cleared the conviction gate for a directional call — both consensus scores (-16.7 and -11.7) sit inside the synthesis script's own Neutral band (-24…+24), not a hard gate override. Both `signed_estimated_move` values are null by design. One chair override was applied: ABM's certainty_tier was moved from a mechanical High to Med (see `chair_override_note` in `03-panel/ABM.json`) because four of seven personas shared a single source for part of their bearish framing, which the chair judged inflated the apparent independence behind the panel's unusually tight 6.6-point disparity. No override was applied to UNFI's call, certainty, or move.

## Ranked field

| Ticker | Company | Event-implied move | Preliminary direction (stage 2) | Evidence completeness | Panelled |
| --- | --- | --- | --- | --- | --- |
| ABM | ABM Industries Incorporated | 8.4% (stage-2 figure; reconfirmed unchanged for the panel) | +12 | 86 | Yes |
| UNFI | United Natural Foods, Inc. | 11.9% (stage-2 figure; refreshed to 11.7% for the panel) | -8 | 85 | Yes |

Both of the day's only two deep-dive dossiers were panelled — the universe was too thin (2 eligible names) for a ranked-but-unpanelled tier to exist today. Note that the panel's directional read diverges from stage 2's preliminary score on ABM (stage 2 leaned mildly positive at +12; the panel leans mildly negative at -16.7) — by design, the panel never saw the preliminary score and is free to disagree with it.

## What would change these calls

- **ABM:** a Q3 print at or above $1.04 EPS with segment operating margin up year over year (roughly 8.2%+, vs. 7.3% last quarter) plus a guide narrowed into the upper half of $3.85–$4.15 would validate the promised back-half ramp and likely produce a relief move — thin options liquidity (~93 contracts front-expiry OI) means little dealer flow to absorb it either way. The mirror case — margin still below ~7.66% (last year's Q3 level) or any fresh guidance walk-down — reruns the pattern that has produced -8% to -9% prints twice in the last six quarters.
- **UNFI:** an initial FY2027 adjusted EBITDA guide at or above the company's own long-term algorithm (~$740–755M+) with an explicit "return to net sales growth" statement and a refreshed buyback authorization points toward the stock's +18–20%+ fiscal-Q4/initial-guide template. A midpoint materially below that, or a refusal to frame FY27 sales growth explicitly, points toward the -10% template the stock has already printed twice this fiscal year — exactly the June 2026 pattern where a large profit beat still produced a double-digit down day on a revenue miss.
- **Cross-name:** both prints land on the same Tuesday morning with no first-tier US macro data in the immediate window (CPI is 09-11, FOMC 09-16, Fed in blackout since 09-05) — the macro-peers persona on both names read the day as macro-quiet, so company-specific news should dominate the tape rather than being swamped by a surprise. Rising diesel/fuel costs were flagged as a mild sector headwind on both names independently (ABM Aviation via airline capacity cuts; UNFI via distribution fuel surcharges).

## Coverage and caveats

- **Universe was thin by design, not by failure.** Only 6 raw candidates existed in the window and only 2 (ABM, UNFI) cleared the $500M market-cap and confirmed-timing floors; 4 were excluded on market cap (WDH, CAN, DLNG, GMHS). Stage 1 triage was skipped per config (universe ≤ 10), so neither name carries a `change_expectation` score from a scout screen — the ranking formula was renormalized to drop that term, per the documented 2026-08-28 precedent (see `02-ranking.json`).
- **All seven panel seats were filled for both names** — no missing personas. One duplicate persona run occurred during the fan-out (a UNFI sentiment-persona subagent was accidentally launched twice while tracking concurrency-limited retries); the duplicate verdict was discarded and only one of the two independent runs is included in the panel file. No seat was left empty.
- **Anchors were refreshed for both names before the panel ran.** No trading session occurred between stage 2's Friday 2026-09-04 close and today (Saturday/Sunday/Labor Day), so re-sourced spot and implied-move figures came back essentially unchanged from stage 2's — this was confirmed via CBOE options quotes and put-call parity rather than simply carried forward.
- **This event was already panelled once before, on 2026-09-04**, because that day's window also rolled through the Sept 7 holiday to the same Sept 8 print. Both notes are preserved in the archive as independent reads at different distances from the event; readers comparing them should treat today's as the more current one, not a correction.
- **One chair override was applied** (ABM certainty High → Med, source-independence concern); none applied to UNFI. No budget degradation was needed — both panel-eligible names fit within `panel.names=2` with no shedding required.
- **Coverage gaps carried from stage 2 remain live caveats for both names**: ABM's options market is thin (front-expiry OI in the tens of contracts), so its implied move is a rough derivation rather than a liquid market price; UNFI's FY2027 EBITDA figures circulating in retail/sell-side commentary are analyst or author constructions, not confirmed company guidance, and the panel treated them as such throughout.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
