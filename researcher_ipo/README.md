# Stage IPO — the IPO researcher

Built 2026-10-09 on the operator's instruction: "another US routine, examining IPOs, the
same approach as the US panel agent, with IPO-predicting mechanisms". It is stage E-P's
method (hunters collect evidence, four blind judges on four different models size it,
`panel_score.py` combines them) pointed at two dated events in the life of a new US
listing, on NYSE, NYSE American and Nasdaq alike. **Research only. It places no orders
and there is no code path that could.**

## The two events, and the one window shape

| event | the session | window (the key) | recorded beside it, ranks nothing |
| --- | --- | --- | --- |
| `debut` | the first session the IPO trades | first trade (the opening cross) → that session's close | offer → first trade (the pop), offer → close, day-1 close → day-2 close |
| `lockup` | first session after Nasdaq's lock-up expiration date | that session's open → its close | the expiration-date session (the other convention), close(D−1) → close(D) |

The operator chose the window: the first price a person using this repo can trade at,
to the same day's close. Nobody here gets an IPO allocation, so the pop is measured and
ranks nothing. The quiet-period expiry was considered and left out (operator's choice).

## What phase 0 found, before any agent existed

`scripts/ipo_backtest.py`, 2026-10-09, over every priced deal on Nasdaq's IPO calendar
from 2024-09 to 2026-10: 751 deals, 318 SPACs dropped, deals of $25m or more.
`analysis/phase0-base-rates.json` holds the whole table and `analysis/phase0-rows.json`
every event it was computed on.

**Debuts, first trade → close (189):** median **−0.48%**, mean +1.60%, median absolute
4.83%, 42% up. Net of IWM, median −0.87%. Nasdaq listings 36% up (median −1.20%), NYSE
52% (+0.05%). One name dominates the dispersion: Newsmax rose +478% from its first trade
to the close; without it the mean is −0.94% and the standard deviation 13.6.

**The pop is large, real, and says nothing about the session.** Offer → first trade has
a median of +11.1% (t = 8.2). It ranks the session at ρ = +0.01; every pop bucket has a
session median between −0.25% and −0.70%. Nothing known before the cross ranks the
session (deal size ρ +0.07).

**Lock-ups, open → close of the first free session (137):** median **+0.32%**, mean
+0.44%, median absolute 2.78%, 55% up; net of IWM +0.73% and 62% up (t 1.17). **The
textbook lock-up sell-off is not in this window.** Volume rises (median 1.35x), the
session does not fall, and the expiration-date session is flat too (+0.25%). The names
with 85% or more of the company locked rose most (+2.43% mean, t 2.1 on 40), a lead
chosen after looking, not a rule. 139 of 141 lock-ups were 180 days.

**Volume:** in the last 365 days, 108 debuts and 96 lock-ups cleared the floors over 251
sessions: **0.81 events a session.** Most sessions carry none or one.

### What that means for the stage, stated before it runs

1. **There is no free control to beat, and the base rates are close to zero.** On
   earnings, the hunt has to beat `-run_up_20d_pct`. Here nothing ranks the window, so
   the bar is zero: a hunt that ranks these events at all is new information.
2. **The debut question is hard and that was a choice.** The predictable part of an IPO
   is the pop, and it is excluded on purpose because it cannot be captured. What is left
   is a session that, on average, goes nowhere.
3. **A within-day ranking mostly does not exist.** At 0.81 events a session, the stage is
   judged POOLED: `ipo_resolve.py --pool` ranks every resolved name on the move net of
   IWM, debuts and lock-ups apart. Expect about four months before 100 names have
   resolved, and longer before either leg can say anything.

### Biases in phase 0, and they all point the same way

- Yahoo serves today's listings: an IPO that delisted since has no bars (4 debuts, 4
  lock-ups), which removes some of the worst outcomes.
- The lock-up date is Nasdaq's nominal one; staged early releases and follow-on lock-ups
  are invisible to it. The live hunter checks the 424B4 and the filings since.
- The day-1 open is the opening cross. A real order sent after it fills at the NBBO a
  moment later, and day-1 spreads in a new listing are wide.

## Where the data comes from (measured 2026-10-09 from this container)

| source | gives | note |
| --- | --- | --- |
| `api.nasdaq.com/api/ipo/calendar?date=YYYY-MM` | priced, upcoming, filed, withdrawn deals, ALL US exchanges | `pricedDate` is the first trading day on 5 of 6 checked; ACCV slipped 6 days, so the resolver reads the tape |
| `api.nasdaq.com/api/ipo/overview/?dealId=` | lock-up days and expiration date, quiet period, shares outstanding, secondary shares, CIK | does not carry early-release terms |
| `efts.sec.gov`, `data.sec.gov/submissions` | the 424B4, follow-ons, 8-Ks, Form 144s, full-text probes | cut at the event date in every baseline |
| Yahoo daily bars | first trade, the session, IWM for the excess move | adjusted; the pop uses the raw open |

## The pipeline

```
ipo_universe.py     debuts first-trading today + lock-ups whose first free session is today
ipo_priced_in.py    sealed baselines: deal, recent debuts or the tape, EDGAR, phase 0
unpriced-hunter-ipo one per name (the shared core, IPO mechanisms, searcher duties)
edge_score.py       the shared scorer, unchanged: impact_sum
market_panel.py     --market IPO: packs, four panel-judge-ipo-* judges, check, score
ipo_resolve.py      after the close: key moves, excess, pooled ranking by event type
ipo_synth.py        synthetic hunts and judges, for validation only
ipo_backtest.py     phase 0
```

The panel's judges are their own set, `panel-judge-ipo-*`, generated from
`config/panel-judge-ipo.md` by `scripts/sync_hunter_core.py`, because a judge left to its
earnings habits would size the offer-to-open pop. The panel history
(`analysis/panel-history.json`) was seeded once with stage E-P's history and is read
over the last **60** names rather than 200, so this stage's own sizes replace the
earnings-scale seed within a few months rather than most of a year. Until they do, "own
top 20%" is measured against earnings prints, and the selection will be sparse.

## Validation, 2026-10-09

`analysis/validation/2026-08-05/ipo/`: a past session with one debut (ATTO, offer $17,
$289m) and three lock-ups (EIKN, BOBS, FPS; a fourth fell below the turnover floor),
sealed, hunted with SYNTHETIC findings (`ipo_synth.py`), scored, packed (no size left in
the packs), judged by four synthetic members, combined (`--dry-run`, so nothing entered
the history) and resolved against the real tape. ATTO opened +23.5% above its offer and
then rose +4.3% from the first trade to the close; that second number is the scored
one. It is a plumbing check on four names and says nothing about the hunt. FPS shows the
case the hunter is told to check: its filings carry a follow-on and waiver language
before the nominal lock-up date.

## Not yet done

- **The Routine does not exist yet.** The text is in `routine-prompts/ipo-hunt.md`;
  proposed cron `35 12 * * 1-5` (08:35 New York), moving to `35 13` on or after
  2026-11-02.
- **No real hunter has run.** The first live day is the first test of the hunter
  definition.
- **The dashboard has no IPO tab.** `dashboard/scripts/build_markets.py` does not read
  `research/*/ipo/` yet.

This is research, not investment advice.
