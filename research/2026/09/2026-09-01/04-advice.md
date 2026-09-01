# Earnings advice — 2026-09-01

**Window:** after today's US close (Tue 2026-09-01) through before tomorrow's open (Wed 2026-09-02). 6 names deep-researched in stage 2, 2 panelled in stage 3 (`panel.names = 2` per `config/pipeline.yaml`; no budget degradation applied — stage 2 completed both batches on schedule).

## The calls

```
DELL — Dell Technologies Inc.   |   AMC 2026-09-01   |   Spot $452.70
CALL: Neutral / No Edge   |   unsigned band 5.7%–34.4% (implied ≈±11.4%)
P(down) 53.9%   |   Certainty Med   |   reversal risk High (64)
Reason: panel leans mildly negative (-10.1) on ISG-margin/memory-cost fear, but
        the lean is thin and one persona reads it bullish on options skew.
Caveat: 5 of 7 personas cited the same margin-narrative article — certainty
        downgraded from the script's High for that reason.
Dossier: research/2026/09/2026-09-01/03-panel/DELL-dossier.md
```

```
CXM — Sprinklr, Inc.   |   BMO 2026-09-02   |   Spot $7.79 (corrected — see caveat)
CALL: Neutral / No Edge   |   unsigned band 3.4%–17.4% (no implied move — dead options chain)
P(down) 56.8%   |   Certainty Med   |   reversal risk High (61)
Reason: all 7 personas score negative (consensus -22.3, just short of Lean Down)
        on cRPO deceleration and a stock up ~60% into the print on sector beta.
Caveat: every persona, not only red-team, independently named the same specific
        squeeze/reacceleration risk — an unusually corroborated reversal case.
        Anchor packet given to the panel carried a stale spot ($8.16, actually
        2026-08-28 data); true spot is ~$7.79, corrected here but not in the
        panel's own reasoning below the surface.
Dossier: research/2026/09/2026-09-01/03-panel/CXM-dossier.md
```

Both calls landed at **Neutral / No Edge** — not because the panels found nothing, but because both found a coherent lean *and* a specific, well-evidenced case against acting on it. That is the conviction gate working as intended, not two blank results.

## Ranked field (all 6 deep-researched names)

| Ticker | Panel priority | Prelim. direction | Implied move | Evidence completeness | Panelled |
| --- | --- | --- | --- | --- | --- |
| DELL | 50.0 | +20 | ±11.4% | 84/100 | **Yes** |
| CXM | 49.55 | −25 | unavailable (no options mkt) | 78/100 | **Yes** |
| GIII | 49.4 | −20 | unavailable (derived ~9.5%) | 84/100 | No |
| GTLB | 49.4 (tiebreak loser vs GIII) | −20 | ±14.0% | 80/100 | No |
| MDB | 48.9 | +10 | ±15.77% | 84/100 | No |
| CRDO | 48.8 | +10 | ±12.0% | 78/100 | No |

Full dossiers for GIII, GTLB, MDB and CRDO — deep-researched but not panelled — are at `research/2026/09/2026-09-01/02-dossiers/<TICKER>.md`.

## What would change these calls

- **DELL:** ISG operating margin printing above 10.5% (management's own guided bar) *with* AI-server revenue above $17B and backlog above $60B would break the margin-compression thesis and validate the bull case outright. The mirror case — margin flat or down, paired with any language that memory-cost pass-through lags a quarter or more — is the single most credible reversal and the one the panel currently leans toward without full conviction.
- **CXM:** FY27 subscription revenue guidance raised above $781.5M with the $139–141M operating-income range defended or raised, and cRPO growth accelerating toward high single digits, would convert the last six weeks from a sector-beta trade into a fundamental one and neutralise the bear case. A second consecutive operating-income cut, or cRPO decelerating back toward Q4 FY26's +1%, would flip the "fade" thesis into a "rout" thesis.
- **Cross-cutting:** both names carry unusually high reversal-risk scores (64 and 61, both High tier) relative to their modest consensus direction scores — this is a day where the panels found real, specific counter-evidence to their own leans rather than a lack of information. Watch for confirmation or refutation of the named mechanism (margin pass-through for DELL, guidance restoration for CXM) in the actual prints rather than treating either call as a coin flip with no structure.

## Coverage and caveats

- No budget degradation was applied this stage — stage 2 completed both dossier batches on schedule and the config's default `panel.names = 2` was used without shedding.
- All 7 panel seats were filled for both names (14/14 subagents completed, no retries needed).
- CXM carries a genuine anchor-quality problem: it has no functioning options market at all (zero open interest across every strike, first post-event expiry 17 days out), so its expected-move sizing rests entirely on 8 quarters of historical realised moves rather than a market-cleared price. Its spot price was also initially sourced stale ($8.16, actually 2026-08-28 data); the true 2026-09-01 intraday price (~$7.79, a ~5% same-day decline with no identified company-specific news) was caught mid-panel and corrected in the anchors and dossiers above, though the seven persona verdicts themselves reasoned against the original figure.
- Two chair overrides were applied, both to `certainty_tier` only (never to `call` or `signed_estimated_move`), both downgrading from the script's computed High to Med: DELL for a shared-source independence gap (5 of 7 personas cited one article), CXM for the stale-anchor issue above. Full reasoning for both is in each ticker's `chair_override_note` inside `03-panel/<TICKER>.json`.
- GIII and GTLB (both `event_implied_move_pct` reliant on illiquid or derived anchors) and MDB/CRDO were deep-researched but not panelled under the config's default panel size of 2; their preliminary reads are unverified by an independent panel and should be weighted accordingly if used.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
