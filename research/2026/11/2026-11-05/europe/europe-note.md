# Stage EU — Europe ranking for 2026-11-05 (Thu)

Sealed Wed 2026-11-04, about 14:45 UTC (15:45 Amsterdam), roughly two hours before the
European close. Every sealed spot and every `run_up_20d_pct` is an **intraday price, not a
close**. The ranking key is `impact_sum`, read from `edge-scores.json`'s `ranking_key`.
The conviction floor is 2.8.

**No name clears the floor.** The top is ASC and DIS at +2.50 and the bottom is ZV at
−1.60. All twenty drawn names were hunted. Every hunt finished its search
(`search_complete`), every hunt confirmed the event in its window, and all twenty are
ranked. The four-model panel selected four names: **ZV short (4 of 4), AUTO long, INISS_B
long and NRC short (3 of 4 each)**. This stage places no orders and reads no broker.

## Ranked

| # | ticker | market | session (checked) | impact_sum (key) | abs_move | p_up | impact_scaled | anchor | history | pre-released? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ASC | uk | bmo? → bmo (07:00 RNS) | +2.50 | 9.0 | 55 | +0.90 | yes | observed_rns | **yes**, FY26 in the 24 Sep pre-close |
| 2 | DIS | it | bmo? → **in-session** (~12:00 CET) | +2.50 | 7.0 | 57 | +0.98 | no | estimated | Q3 cover disclosed |
| 3 | ENX | fr | amc (17:45 CET) | +1.70 | 5.5 | 58 | +0.88 | no | estimated | Q3 volumes, 7 Oct |
| 4 | AKE | fr | bmo (07:00) | +1.20 | 5.0 | 58 | +0.80 | no | estimated | no |
| 5 | AMBU_B | dk | bmo? → bmo (07:00–08:00) | +0.90 | 9.0 | 51 | +0.18 | no (**join miss**, see below) | estimated | no |
| 6 | AUTO | no | bmo (06:00) | +0.80 | 12.0 | 55 | +1.20 | yes | observed_newsweb | no |
| 7 | SFQ | de | bmo? → bmo (~07:15) | +0.80 | 5.5 | 54 | +0.44 | yes | estimated | no |
| 8 | LR | fr | bmo (07:30) | +0.60 | 6.0 | 55 | +0.60 | yes | estimated | no |
| 9 | SMHN | de | bmo? → bmo (~07:30) | +0.60 | 5.5 | 53 | +0.33 | yes | estimated | **yes**, 27 Oct ad-hoc guide cut |
| 10 | FBK | it | bmo? → bmo (07:00) | +0.35 | 3.5 | 52 | +0.14 | no | estimated | **mostly**, monthly sales and brokerage |
| 11 | INISS_B | se | amc (22:30 CET) | +0.30 | 5.5 | 57 | +0.77 | no | estimated | **partly**, 21 Oct target raise |
| 12 | PKO | pl | bmo? → bmo (pattern) | +0.20 | 3.5 | 52 | +0.14 | no (no register) | estimated | CHF cost, raport 37/2026 |
| 13 | ORSTED | dk | bmo (08:00 CET) | +0.10 | 4.5 | 52 | +0.18 | no (**join miss**) | estimated | **yes**, 8 Oct pre-close call |
| 14 | HFG | de | bmo? → bmo (~07:00) | −0.10 | 5.0 | 47 | −0.30 | yes | estimated | **yes**, 24 Sep ad-hoc guide cut |
| 15 | SKA_B | se | bmo (07:30 CET) | −0.10 | 4.0 | 45 | −0.40 | no | estimated | contracts announced |
| 16 | CAPMAN | fi | bmo (08:00 EET) | −0.40 | 4.5 | 49 | −0.09 | no | estimated | carry and fees in previews |
| 17 | AMV0 | de | bmo | −0.70 | 6.0 | 45 | −0.60 | yes | estimated | **yes**, Q3 margin at the 5 Oct pre-close |
| 18 | DEZ | de | bmo? → bmo (~07:30) | −1.00 | 7.0 | 47 | −0.42 | yes | estimated | no |
| 19 | NRC | no | bmo (07:00) + CMU | −1.00 | 9.0 | 47 | −0.54 | no | observed_newsweb | no |
| 20 | ZV | it | bmo → **in-session** (board 09:30) | −1.60 | 5.5 | 43 | −0.77 | yes | estimated | no |

`bmo?` marks a name sealed with `session_unresolved`. Each was settled by its hunter's
`session_check`, from the issuer's own notice or its release-time history. **Two Italian
names release during the session, not before the open.** DIS (d'Amico: prior releases at
12:14, 11:31 and 12:09 CET) and ZV (board at 09:30; prior releases at 11:38 and 14:38) both
land inside the sealed close(11-04) → close(11-05) window, so that window holds the whole
reaction. Their sessions are `bmo` by window, not by clock. The two `amc` names were both
confirmed after the close: ENX at 17:45 CET and INISS_B at 22:30 CET. Their window is
close(11-05) → close(11-06).

Names likely to carry a guidance change (`new_in_release`):

- **NRC**: FY26 revenue guide plus a Capital Markets Update reset of the 2028 targets, at 07:00.
- **AUTO**: the ~USD 700m FY26 guide.
- **AMBU_B**: its first FY26/27 guide.
- **ASC**: its first FY27 guide.
- **ENX**: revised 2026 cost guidance.
- **AMV0**: a narrowing to the low end.
- **DEZ**: a revenue narrowing.
- **LR**: a narrowing to the top of +8–10%.

Already pre-released, in full or in part: ASC, SMHN, HFG, AMV0, ORSTED, FBK and INISS_B.
On the first resolved European days those two facts decided the size of the move, while
the emitted sizes barely differed.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four ran on their
own `-intl-` agents, with no fallback, and each covered 20 of 20 names. Not every judge read
the six hunter definitions the packs name:

- **Sonnet 5.5** opened none of them, only `config/hunter-core.md` and `LESSONS.md`. Yesterday's Sonnet judge did the same.
- **Opus 5** read one of the six (fr).
- **Opus 5.5 and Fable 5.1** read all six.

Every member's sizes are scored as returned.

The selection rule is `consensus_k` ≥ 3 of 4, each judge in its own top 20%. A judge's top
20% starts at: Opus 5 |1.40|, Opus 5.5 |0.84|, Sonnet 5.5 |0.70|, Fable 5.1 |0.96|. Each
threshold comes from that judge's last 200 live sizes in this market.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ZV | bmo (in-session) | **yes** | 89 | short | 3 | 89S* | 92S* | 90S* | 84S* | 4 | −1.66 | −1.60 |
| 2 | AUTO | bmo | **yes** | 91 | long | 14 | 68L | 98L* | 100L* | 98L* | 3 | +2.49 | +0.80 |
| 3 | INISS_B | amc | **yes** | 86 | long | 10 | 79L | 94L* | 97L* | 74L | 3 | +1.67 | +0.30 |
| 4 | NRC | bmo | **yes** | 85 | short | 8 | 86S* | 92S* | 71S | 91S* | 3 | −1.58 | −1.00 |
| 5 | AMV0 | bmo | | 78 | short | 16 | 68S | 90S* | 96S* | 57S | 2 | −1.28 | −0.70 |
| 6 | DIS | bmo (in-session) | | 78 | long | 14 | 57L | 84L* | 95L* | 74L | 2 | +1.25 | +2.50 |
| 7 | AKE | bmo | | 71 | long | 8 | 63L | 70L | 84L* | 68L | 1 | +0.93 | +1.20 |
| 8 | SMHN | bmo | | 60 | long | 22 | 71L | 62L | 84L* | 24L | 1 | +0.92 | +0.60 |
| 9 | SKA_B | bmo | | 66 | short | 12 | 71S | 76S | 71S | 46S | 0 | −1.02 | −0.10 |
| 10 | ASC | bmo | | 70 | long | 9 | 78L | 61L | 78L | 61L | 0 | +1.01 | +2.50 |
| 11 | LR | bmo | | 67 | long | 11 | 71L | 79L | 68L | 50L | 0 | +1.01 | +0.60 |
| 12 | SFQ | bmo | | 58 | long | 13 | 36L | 64L | 68L | 66L | 0 | +0.90 | +0.80 |
| 13 | ENX | amc | | 62 | long | 9 | 53L | 70L | 71L | 54L | 0 | +0.84 | +1.70 |
| 14 | HFG | bmo | | 25 | short | 18 | 42S | 14S | 0- | 44S | 0 | −0.38 | −0.10 |
| 15 | DEZ | bmo | | 15 | long | 24 | 36L | 14L | 36L | 24S | 0 | +0.33 | −1.00 |
| 16 | PKO | bmo | | 16 | long | 4 | 21L | 14L | 20L | 10L | 0 | +0.24 | +0.20 |
| 17 | FBK | bmo | | 14 | long | 7 | 12L | 25L | 8L | 10L | 0 | +0.18 | +0.35 |
| 18 | ORSTED | bmo | | 11 | short | 14 | 12S | 6S | 8L | 32S | 0 | −0.15 | +0.10 |
| 19 | CAPMAN | bmo | | 9 | short | 7 | 4S | 6S | 5S | 21S | 0 | −0.12 | −0.40 |
| 20 | AMBU_B | bmo | | 8 | long | 42 | 71L | 22S | 20L | 36S | 0 | +0.00 | +0.90 |

**ZV (selected, short, 4 of 4, the tightest agreement of the day, sd 3).** Italian
wholesale gas (PSV) averaged about 75 €/MWh month to date in September 2026, against about
35 a year earlier, and about 58 against 36 in August
(https://www.comparasemplice.it/informazioni/news/psv-gas-del-mercoledi-30-09-2026-077360-e-smc-37).
Zignago's own H1 release flagged "pressioni rialziste" on energy. The last comparable
shock, Q1 2025, took the EBITDA margin from 21.8% to 14.2% and the stock −10.3% on the day.
O-I's European segment profit fell from $95m to $2m, which points the same way
independently. **The strongest case against:** Zignago does not disclose its hedge ratio,
so a well-hedged Q3 would mute all of it. Verallia said Italy held steady. No consensus
exists (two analysts), so the bar is a naive flat EBITDA. Four of the last five release
days closed up.

**AUTO (selected, long, 3 of 4; Opus 5 at 68).** The ~USD 700m FY26 guide, given for the
first time at Q2, implies H2 of about USD 171m a quarter, against Q2's USD 192.1m and a
backlog of USD 596m
(https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=679547). A raise or firmer
guide is the likelier event. A buyback of about 550k shares a day runs through the window.
AutoStore's observed results-day moves since 2025 run 13.5–29.8%, so every judge sized a
large move (abs_move 12–13). **The strongest case against:** the bar is unsourced, since no
Q3 consensus was found. KION's Dematic orders rose only +1.4% y/y in Q3, and the company
itself guided H2 margins slightly below H1. The hunter's own key is only +0.80. The panel's
size comes mostly from the large abs_move and not from any one finding.

**INISS_B (selected, long, 3 of 4; Fable 5.1 at 74).** On 21 Oct, after Q3 closed,
Inission raised its FY26 revenue target to SEK 2.6–2.7bn from 2.3–2.5bn
(https://view.news.eu.nasdaq.com/view?id=b52377aec51d9a3ea9b3384d61a5c1f18&lang=sv&src=listed).
That implies Q3 sales of roughly SEK 630–680m, against the only visible estimate (ABG,
580m, 14 Oct, never updated). The last three reports beat that same bar and rose 9.7%,
6.8% and 9.4%. **The strongest case against:** the raise rose 5.2% on the day and fully
faded, so the revenue is effectively pre-released. Q2 operating cash flow was −4.8 MSEK,
and Scanfil flagged working capital burdening cash. The hunter's own key is +0.30, the
panel's read is much larger. It is a $216k-a-day First North name with no positioning
anchor, released at 22:30 CET.

**NRC (selected, short, 3 of 4; Sonnet 5.5 at 71).** The FY26 revenue guide of about NOK
7.5bn needs H2 up about 30% y/y, after H1 fell 6%
(https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=679568). The same 07:00
release carries a Capital Markets Update. Its 2028 targets (above NOK 10bn revenue, above
5% EBIT) do not fit 2027 consensus of NOK 7.02bn
(https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=685118). **The strongest
case against:** consensus (3 analysts) already sits about 10% below the guide, so a cut
may be priced. The NOK 566m ETM claim against Bane NOR, about a third of market cap, is
open with an upward-skewed range. The two guidance findings rest on the same
revenue-shortfall evidence.

**Where the panel and the hunter disagree most:**

- **DIS**: the hunter's joint-top name (+2.50) is not selected (k 2, panel_pct 78). Opus 5 (57) reads the Q4-fixtures read-through as a peer proxy.
- **ASC**: the hunter's other joint-top name (+2.50) reaches panel_pct 70, with no judge in its top 20%. The cyber-quantification finding did not persuade them.
- **DEZ**: the hunter is −1.00, while the panel leans long (+0.33). Opus 5 has it at +0.5, on a 27% drawdown and strong construction-equipment peers.
- **AMBU_B**: the hunter is +0.90, the panel 0.00, with the widest spread of the day (sd 42). Opus 5 reads it 71L on the crowded 6.08% short; Opus 5.5 and Fable 5.1 lean short on the twice-cut growth guide.
- **ENX**: the hunter is +1.70, the panel 62. The judges sized a smaller move (abs 3.5–4.0) than the hunter's 5.5.

No name is above the floor, so there is no "above the floor but not selected" case.

**What the numbers are not.** `panel_score` ranks; it does not forecast. There is no
`expected_edge_pct` off the US. Certainty (`p_up`) is recorded and decides nothing. The
member scales are still mostly the frozen E-P seed, until this market has about 200 panel
names of its own. In the four-model re-judge the judges ranked Europe better than the live
hunt (ρ +0.33/+0.34 on 48 names) but Japan and Australia worse, so nothing about this
market's panel is established.

## Top and bottom of the key

- **Top, ASC +2.50.** The largest finding is +1.5, on the "other" line. The 6 Oct cyber
  incident took about 10% off the stock, and these results are the first chance to
  quantify it. The company's own RNS reported no operational disruption
  (https://www.investegate.co.uk/announcement/rns/asos--asc/update-regarding-cyber-incident-/9809595).
  The stock has round-tripped the whole September upgrade (430p, then 508p, now 428p). The
  first FY27 guide adds +1.0 against a stale consensus.
- **Top, DIS +2.50.** The largest finding is +2.5, on guidance. Q4-to-date fixtures are new
  in this release, and peers' published Q4 books sit far above DIS's Q3 spot of about
  US$30k. TORM's MR book is 49% fixed at US$59,722
  (https://www.stocktitan.net/news/TRMD/torm-plc-q3-2026-results-dividend-distribution-and-financial-outlook-7mtk2wsugj1m.html).
  It is damped by the ~55% of DIS's days on time charter, and by a sector that sold good
  news on 4 Nov (−1.0).
- **Bottom, ZV −1.60.** The Q3 energy cost, as in the panel paragraph above (−1.5).

## Two defects found, not fixed in the baselines

- **The Danish short register is not joined to its issuers.** Both Danish names sealed
  `short_ratio_pct` 0.0. The Finanstilsynet table lists **AMBU A/S at 6.08%** (03-11-2026),
  the fourth-largest disclosed short in Denmark, and **Ørsted A/S at 0.54%** (15-10-2026).
  The repo's own `eu-short-cache.json` holds Ambu under the key "AMBU A S", so the
  issuer-name join in `eu_positioning` fails for Danish names. The share-class suffix and
  the "A/S" punctuation are the likely cause. Their `anchor_covered`, and Ambu's
  `priced_lean_pct`, are understated. Baselines are sealed and were not revised. Both
  hunters read the register directly. The panel saw it through the packs, and Opus 5
  counted it as a finding. Worth fixing before the next Danish name is sealed.
- **The `publish.sh` rebase is blocked by a dirty `eu-short-cache.json`.** Something
  rewrote the cache while hunters ran, and every wave publish after the first failed with
  "behind its remote". Each was committed and rebased by hand. It is a working-tree
  issue, not a remote one.

## The day, and what it is not

- **Selection**: `random sample of 109 eligible, seed 'eu-2026-11-05'`. 195 were scheduled,
  109 eligible above the **$100k/day** floor, and 20 drawn at random.
  - By market: de 5, fr 3, it 3, dk 2, no 2, se 2, uk 1, fi 1, pl 1, es 0.
  - Eligible by market: de 26, se 18, it 17, dk 10, no 9, uk 8, fr 7, pl 7, fi 5, es 2.
  - **`market_concentration`**: Germany is the largest market at 25%, with 9 markets represented. That is a spread day.
- **Calendar sources**: TradingView, plus:
  - the UK RNS calendar (read; it confirmed ASC);
  - Yahoo, read in all ten markets this time (it added FBK, among others);
  - EQS events for DE;
  - Euronext Oslo for NO;
  - Inderes and the Nasdaq Nordic financial calendar for SE/DK/FI.

  **bankier (PL) returned 403.**
- **Options are null in all ten markets.** Europe runs in the anchor-less regime that
  produced ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
- **Short registers**: de, dk, fi, fr, it, no, se and uk read; es and pl have none.
  - **9 of 20 names carry `anchor_covered: true`**: AMV0, ASC, AUTO, DEZ, HFG, LR, SFQ, SMHN, ZV.
  - Every other zero is the 0.5% truncation (0.1% in Denmark), not a measurement.
  - The exceptions are the two Danish join misses above, which are real positions.
- **Spain and Poland: 1 name (PKO)**, which has no positioning anchor and can never be
  confirmed or killed. **Germany: 5 names** (AMV0, DEZ, HFG, SFQ, SMHN), for which
  `event_occurred: false` is unreachable. Italy's three (DIS, FBK, ZV) cannot reach it
  either. All three were confirmed from the issuers' own calendars.
- **`lean_vs_free_control_rho`**: no European run has resolved since 2026-10-16, whose only
  per-market reading is se 0.60. **Resolve this run by ~2026-11-13**, inside the Nordic
  feed's ~12-day window (dk 2, no 2, se 2, fi 1).
- **The lean's weights are priors borrowed from the US runs**, measured nowhere in Europe.
- **`history.basis` is estimated** (a scale, not a record of dates) for 17 of the 20 names.
  Only ASC (`observed_rns`), AUTO and NRC (`observed_newsweb`) carry observed histories.
  Several hunters found that their name's real report-day moves run well above the
  baseline's estimate: AMBU_B a median of about 8.7% against 2.63%, AUTO 13.5–29.8%.
- **Conviction floor**: none above 2.8. Over the whole US sample the sign was a coin flip
  below it.
- **`language_note`, where it mattered**:
  - Polish: PKO's bar (its own 20-broker consensus table), raport 37/42 and the calendar came only from Polish sources.
  - German: DEZ's job cuts, the FFG WirtschaftsWoche story and the FactSet consensus were German-only. So were SMHN's Berenberg preview and target resets, and HFG's Deutsche Bank estimates.
  - Italian: ZV's board time and the PSV series, DIS's release timestamps and Equita's US$30k assumption all came from Italian sources.
  - French: Legrand's Q3 2025 comp miss, Rexel's country split, and ENX's JPMorgan note and CEO item came from French wire copy.
  - Finnish: CapMan's BROEN sale date, which puts its carry in Q3, came from the Finnish release.
  - Swedish: SKA_B's Jefferies downgrade was only on EFN.
  - Elsewhere the notes read "nothing the English sources did not already carry", which is the expected Nordic answer.
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
