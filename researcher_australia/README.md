# Stage AU — the Australian researcher

The unpriced-information hunt, run over the ASX. Same question as stages E, J and EU,
same output contract, and **deliberately the same scorer**
(`researcher_us/scripts/edge_score.py`, unchanged) so the four markets' numbers mean the
same thing.

**It places no orders.** There is no execution block, no broker call and there must not
be one. Alpaca does not carry the ASX, and execution would be a separate build against a
different broker. That is the one thing separating it from stage E.

Built 2026-09-22. **Nothing has resolved in Australia.** The stack was validated end to
end against 2026-08-27 with *synthetic* findings, which ranked at ρ=0.215, p=0.36 on 20
names — what random findings should do.

## Why this market

`SUBMARKET.md` has the measurements. In one paragraph: Australia has the **best
positioning anchor in this repo**, because ASIC publishes an aggregated daily short
position for every product rather than a 0.5% disclosure register — 430 of the 755 rows
on 2026-09-16 were below 0.5%, minimum 0.000000% — with **4,113 dated files back to
2010-06-16**, so it is the only positioning anchor here that can be backtested over a
long history. What it costs is a two-month calendar (676 of 855 forward events in
February and March) and a four-session publication lag on the register.

Canada has the better calendar by a wide margin and was declined because both of its
instruments are shut from this container: `sedarplus.ca` 0 of 4 and `ciro.ca` 0 of 7.

## The files

```
researcher_australia/
  SUBMARKET.md          why this market, with the counts behind it
  README.md             this file
  LESSONS.md            deliberately empty until a run resolves
  scripts/
    au_market.py        the two load-bearing facts: the Sydney date shift and the
                        trading calendar, plus the three headline classifiers
    au_positioning.py   ASIC's aggregated daily short register, level and change
    au_priced_in.py     the sealed baseline
    au_resolve.py       score a finished run against what the stock did
  routine-prompts/
    australia-hunt.md   the text in the Routine, kept in step by hand
  analysis/             short-positions-cache.json and anything the scripts generate
```

Plus, outside this directory: `.claude/skills/researcher-australia-hunt/SKILL.md`,
`.claude/agents/unpriced-hunter-au.md`, and the `australia_hunt` block in
`config/pipeline.yaml`.

## Running it by hand

```bash
RUN=research/2026/09/2026-09-23/australia
python3 researcher_australia/scripts/au_universe.py -o $RUN/universe.json
python3 researcher_australia/scripts/au_priced_in.py --universe $RUN/universe.json \
        --out-dir $RUN/baselines
# ... one unpriced-hunter-au per name, writing $RUN/hunts/<CODE>-h1.json ...
python3 researcher_us/scripts/edge_score.py --run $RUN
python3 researcher_australia/scripts/au_resolve.py --run $RUN -o $RUN/resolved.json
```

`au_universe.py --date` defaults to the **next** ASX session, not today, because the
baseline has to be sealed the evening before a pre-open print. That default is correct;
overriding it with today's date seals after the event.

## The five things a reader gets wrong

**1. The vendor's date is one day early for 85% of rows.** Sydney is UTC+10 or +11 and
the vendor stamps the UTC instant, so BHP's 08:31 lodgement on 18 August reads as 17
August. `au_market.sydney_event_date()` converts the instant rather than adding a
constant, so it survives the 2026-10-04 daylight-saving change. Every row carries
`event_date_basis`. Do not "correct" it back.

**2. An absent product in the short register is a measured zero, and an unreadable
register is not.** `positioning.covered` keeps those apart. Because ASIC does not
truncate at 0.5%, an absent product genuinely has no reported position — which is a
stronger statement than the same absence in London or Tokyo.

**3. The register is four sessions stale.** `positioning.lag_sessions`. "Shorts are
building" may be describing history on a name that has already moved.

**4. Half the ASX lodges a cash-flow report, not a profit result.**
`history.filer_type` is `results` (Appendix 4D/4E), `quarterly_report_only` (Appendix
4C/5B under Listing Rule 4.7B) or `none_found`. Different events, different bars.
`au_resolve.py` splits the ranking by it. `none_found` on an issuer whose three years of
archive read cleanly is a reason to doubt the print exists.

**5. `history` is observed, unlike stage J's.** Real ASX lodgement dates with real
timestamps, so its dates may be cited as facts. What is still inferred is the headline
classifier.

## The known defect, stated rather than fixed

On the 2026-08-27 validation run `lean_vs_free_control_rho` read **0.80 over 20 names**,
against stage J's healthy 0.446–0.59. The lean is `short_squeeze` + `short_building` +
`runup`, and the run-up term dominates whenever short interest is small — which, on an
untruncated register, is most names. **Australia's lean is therefore more entangled with
its own benchmark than Tokyo's is.**

It is not fixed here on purpose. The weights are Tokyo's priors with no Australian
measurement behind them, and re-tuning a constant before any resolved run is precisely
what `w1` was frozen to prevent: a constant that moves with the data is not a hypothesis.
`au_resolve.py` ranks every component separately so the replacement can come from
measurement. This is the first thing a resolved run should settle.

## What the stage cannot do

- **No option anchor.** Measured 2026-09-22: AAPL 22 expiries, `BHP.AX` zero. This stage
  runs in the regime `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over
  104 events. Every note must say so.
- **No whole-day phantom sweep for a past date.** The ASX serves a whole-day archive for
  today only; confirmation for a past date is per issuer, as it is for Germany.
- **No spread measurement.** Entirely unmeasured, and it is the cost that would matter
  most in the band this stage targets.
- **No orders.** See the top of this file.

## The Routine

`trig_01Qy7FjBpjY4dEGcZsYGnpt3`, cron `30 6 * * 0-4` — 06:30 UTC, Sunday to Thursday,
which is 16:30 or 17:30 Sydney, after the 16:00 close. **Sunday to Thursday is not a
typo**: the stage seals for the next session, so the fire that seals for Monday happens
on Sunday. `routine-prompts/australia-hunt.md` has the table and must be changed in the
same commit as any re-paste, since `update_trigger` works on this Routine.
