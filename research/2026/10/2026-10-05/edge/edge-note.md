# Edge hunt — 2026-10-05 window (2026-10-05 amc + 2026-10-06 bmo)

**Late run.** The Routine fired 2026-10-05 17:04 UTC. The session stalled on a permission denial and resumed at 06:55 UTC on 10-06. The 10-05 amc half had no confirmed rows. All three ranked names are 2026-10-06 bmo, and all three were sealed and hunted *before* their releases: hunts finished at ~07:05 UTC, while the releases come at 08:00–09:00 ET. Ranking key, per `edge-scores.json`: **`impact_sum`**. No name clears the 2.8 conviction floor.

| # | ticker | session | pre-lessons | **post-lessons (key)** | scaled | V2 | floor | tradable | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | APOG | bmo 10-06 | +2.30 | **+2.50** | +1.92 | +0.78 | no | yes, long, $9.5m/day, ok | +10.78 |
| 2 | RPM | bmo 10-06 | +0.10 | **+0.30** | +0.26 | −0.03 | no | yes, long, $99.4m/day, ok | +9.69 |
| 3 | LW | bmo 10-06 | −0.70 | **−0.80** | −0.40 | −0.94 | no | yes, short, Alpaca lends, $88.3m/day, ok | +10.63 |

Three columns are measured beside the key and are not the key: pre-lessons, scaled and V2. **The book selects on `impact_scaled` ≥ 1.76 since 2026-10-02, and APOG's +1.92 clears it.** No order was placed (see Execution).

## Top and bottom

- **APOG +2.50.** The driver is a likely EPS beat (+3.5). Q2 consensus is $0.63, from two analysts, and sits 36% below last year's $0.98. Management repeated the Q1 wording ("slightly lower sales, lower adjusted EPS y/y"), and Q1 printed $0.57 against a $0.41–0.43 bar, a +15.2% day. The hunter bridges Q1 to Q2 at roughly $0.68–0.88. Source: https://www.fool.com/earnings/call-transcripts/2026/06/26/apogee-apog-q1-2027-earnings-call-transcript/. Against it is guide risk from the weak architecture billings index (ABI 47.2), sized −1.0: https://www.metalconstructionnews.com/news/increased-pessimism-among-architecture-firm-leaders-about-q4-2026-billings/. The price already shows −10.8% over 20 days, −27% from the high, with the whole Q1 reaction given back.
- **LW −0.80.** The driver is the European crop: EU-4 output is down ~24% and free-buy potatoes are up roughly 10× since spring (−1.2). Source: https://www.potatonewstoday.com/2026/09/25/eu-4-potato-production-set-to-fall-by-almost-a-quarter/. It is offset by put/call at 2.08, its 52-week high (+1.0 relief if the FY27 guide is reaffirmed): https://ortex.news/articles/177222/lamb-weston-heads-into-earnings-with-options-traders-at-peak-caution. The price already shows −10.6% over 20 days and target cuts from JPM and Stephens.

## Critical read

No name clears the 2.8 floor, so nothing here is recommended on the floor rule. APOG is the only row worth reading closely. Its size rests on a single `reported_quarter` inference, a model of the bridge rather than a reported number. Its own history shows beats are sold when the guide is cut (Oct 2025: −4.4% on a beat). The hunter's two numbers agree in sign: print_vs_bar +15%, expected move +1.92. The bar rests on two analysts. Turnover is $9.5m/day, so the name is not thin.

## Names not ranked

None. The 10-05 amc half had 0 confirmed rows. AEHR was company-announced for 10-05 amc but Nasdaq listed it as `time-not-supplied`; it had already printed when this session resumed and was not hunted.

## Standing caveats

- **Order versus sign.** Below the floor the sign has been a coin flip: 53% over 38 events. Above it, the rank of conviction predicted whether the sign was right at ρ=+0.514. Every name today is below the floor, so read these signs as an order and not as views. `impact_sum` ranks and does not size the move.
- **Control.** −run_up_20d orders the names APOG > LW > RPM; the hunt orders them APOG > RPM > LW. Both put the same name on top. The hunt has not yet been shown to beat this free control.
- **Sign balance.** 2 of 3 names lean positive and 1 leans negative.
- **Nothing checked the findings.** There was no adversary and no second hunter. On paired hunts in the past, the key differed by a median of 2.40 points and 4 of 12 pairs had opposite signs, which is about the size of today's whole table.
- **Baseline measured versus inferred.** 0 of 3 names have an option anchor. The late seal made `priced_in.py` read the event date as passed and refuse the chain, so the expected move is the historical median. Stage E-P sealed the same three names at 17:12 UTC on 10-05 *with* chains.
- **Capacity.** All three names clear the $200k floor, and none is thin.
- **One day is an anecdote.** Three names cannot produce a meaningful rank correlation.

## Execution

`execution.enabled` is true. The step 0b calls `verify --fix --submit` and `close --submit` were **refused by the session's auto-mode permission classifier** ("real-world transactions"). That is the sixth run since 09-28 with this refusal. Close AMC at 10:16 UTC on 10-05 had found 0 held, so no exit was owed. Step 7 was not attempted. The entry window for this run was the 10-05 US session, which had closed long before the hunt finished, so APOG (the only name clearing the 1.76 `impact_scaled` floor) could not have been bought on time even without the refusal. Result: 0 orders, gross 0%.

## Context: retail, search and volatility (not used for selection)

These are context only. Nothing ranks, selects, sizes or trades on them.
- APOG: retail 42 (no), search failed, vol 23% (no)
- RPM: retail 22 (no), search sparse, vol 23% (no)
- LW: retail 41 (no), search 1.43x (not quiet), vol 34% (no)

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
