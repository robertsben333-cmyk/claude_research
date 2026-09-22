# Run 1 for 2026-09-23 — superseded, kept

Built **2026-09-19T02:10:47Z** as the first real German and French hunts of stage EU.
Moved here on 2026-09-22 by the scheduled stage EU fire, which re-ran the day properly.

Why it was superseded rather than resumed:

- **It is a three-market universe.** `markets: ["uk", "de", "fr"]`. The ten-market
  expansion (se, dk, no, fi, it, es, pl) and the cap of 20 landed the same day and this
  file was built before them, so it is not the universe this stage draws from today.
- **Its baselines were sealed three sessions early.** The spot and `run_up_20d_pct` in
  every one of the nine baselines are struck on 2026-09-19, while the window
  `eu_resolve.py` measures is close(2026-09-22) → close(2026-09-23). The free control is
  therefore struck days away from the hunt it is supposed to be compared against, which
  is the one comparison this stage exists to make.
- **It is not a ranking and says so.** Seven of its nine names were never hunted — that
  session could not spawn subagents — so two names carry a score and seven carry
  `not ranked: no hunt`.

What is real in here and worth keeping: two genuine hunts (KWS SAAT `impact_sum` −2.10,
Quadient +0.90), both with a real `pre_local` freeze, and the first end-to-end proof that
the DE and FR chain runs. `pre_lessons` in both is **not** a measurement — one context ran
both hunts having already read `LESSONS.md`, so the freeze equals the emitted set by
construction.

Do not pool these two names with run 2's. They were scored against a different seal.
