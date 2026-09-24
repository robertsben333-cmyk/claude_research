# Run log — 2026-09-24

## Stage AU — Australia researcher — STARTED
- Logged at 2026-09-23 06:37 UTC
- Fired 06:37 UTC 2026-09-23 (16:37 Sydney). Sealing for the next ASX session, expected 2026-09-24.
- Plan: au_universe -> au_priced_in seal -> unpriced-hunter-au in waves of 5, one per name -> edge_score -> note. No orders.

## Stage AU — Australia researcher — DONE
- Logged at 2026-09-23 06:53 UTC
- 34 scheduled / 12 eligible / 12 hunted (no draw, under cap 20) / 4 rankable. session_unresolved 0. No name above floor 3.0. Ranked: AAR 0, SOL 0, PMV -0.5, PEN -1.0.
- 8 names not ranked (event unconfirmed): BCM CHN CXO GLN PNR RML VMM WIA. All map to the June-FY statutory annual report (due 30/09), which the vendor dates as a print. Late-September calendar defect: 8 of 12 hunts spent on it.
- AAR hunter set event_confirmed true on cadence alone (TRT pattern); check at resolve.
- Defect: au_priced_in history classifier misses 'Annual Report to Shareholders'/'Half-year Report' (CXO) and counts 'Quarterly Results Presentation' as results (PNR). Not fixed in this run; baselines are sealed.
- Defect: ASX announcement PDFs are RC4-encrypted with an empty password; eu_pdftext.py and WebFetch cannot read them. Hunters used ad-hoc scratch decryptors not in the repo.
- ASIC register 2026-09-17, lag 3 sessions. No resolved AU run, so lean_vs_free_control_rho unavailable (validation 0.80).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-23 13:38 UTC
- Fired 2026-09-23 13:38 UTC (intraday, ~2h before the European close). Sealing for event date 2026-09-24 (Thu), the next European session.
- Plan: eu_universe.py --date 2026-09-24 over ten markets, cap 20, $200k floor, seal baselines, one bilingual hunter per name in waves of 5, publish after each wave, edge_score.py, note.
- Checkout note: local main had diverged from a force-updated origin/main (ahead 82 / behind 58); work was done on a fresh branch cut from origin/main 4a28ef10 so publish.sh would not rebase stale history onto main. EARNINGS_DATA_BRANCH=main pinned.

## Stage EU — universe and baselines sealed
- Logged at 2026-09-23 13:44 UTC
- 46 scheduled, 14 eligible above $200k, all 14 hunted (at or under cap 20; no draw). by_market uk 9, fr 2, de 1, se 1, es 1. Concentration: UK 64.3%.
- Baselines sealed ~13:44-13:49 UTC on INTRADAY spots (markets open), not closes.
- Registers read: uk (as of 09-19), de (09-22), fr (09-21), se (09-22); es none.

## Stage EU — hunter observations (wave 1)
- Logged at 2026-09-23 13:54 UTC
- ATE: vendor date wrong. Alten's AMF-filed H1 revenue release sets H1 results for 2026-09-25 after the close (~17:40 Paris). Neither window holds the print. 0 findings. Candidate for event_occurred: false on 09-24 at resolve time.
- ADOC: real print on 09-24 but amc (all 2026 AMF releases stamped 18h00 CEST), so the resolver's alternative window, close 09-24 -> close 09-25, is the relevant one. 0 findings.
- SLR: the hunter read the CNMV per-issuer short register at https://www.cnmv.es/portal/consultas/ee/posicionescortas?nif=A83511501&lang=es from this container: 7 live positions, 5.61% total. This contradicts CAPABILITY['es'] (register unreachable). Worth re-probing before trusting the 'Spain has no register' line; the baseline stays sealed as-is.

## Stage EU — DEFECT: Swedish register name join missed H&M
- Logged at 2026-09-23 13:55 UTC
- HM_B baseline sealed short_ratio_pct 0.0 / anchor_coverage.state register_read_no_position, but the cached FI register carries 'H M HENNES MAURITZ AB' at 4.53% (4.42% on the prior cache day). The join on issuer name failed against the vendor's 'H&M Hennes & Mauritz AB Class B' (share-class suffix and/or '&' normalisation). Confirmed by grep of researcher_europe/analysis/eu-short-cache.json.
- The baseline is sealed and NOT revised; its lean (+0.37) is run-up only. The hunter carried the true level (4.53%, building) as a finding. Any Nordic share-class name (… AB Class A/B) may read a false zero the same way. Fix eu_positioning's name normalisation in a development session, not in this run.

## Stage EU — CNE is under offer
- CNE: recommended all-cash DNO scheme at US$5.214 (RNS 17 Sep, Court Meeting 16 Oct). The interim print cannot move a fixed-price offer; 0 findings. Its run-up is takeover premium, so the free control means nothing on this row.

## Stage EU — CHAR date unconfirmed
- CHAR: no Notice of Results. The 24 Sep date is vendor/Fidelity 'Sep 2026' only. eu_resolve should confirm or kill it against Investegate. The 1-for-25 consolidation approved 22 Sep has no effective date; if it lands in the window an unadjusted Yahoo bar would show a ~25x jump — the resolver must check.

## Stage EU — KEFI likely phantom
- KEFI: vendor row has placeholder time and stale last-release (2022-09-28); last three interims came 29/30 Sep with no notice. Likely a phantom for 09-24; eu_resolve should check Investegate. 0 findings.

## Stage EU — ALTN date unconfirmed
- ALTN: no Notice of Results; vendor date is exactly 52 weeks after last year's release. Hunter puts ~30% on the 24th. Both findings moved to outside_window; 0 findings.

## Stage EU — LIVE: resolver/ex-dividend issue and a Yahoo data defect
- LIVE's whole -1.4 is the Q2 dividend (1.4475p, 1.92% of spot) going ex on 24 Sep, the results day. It ranks only because eu_resolve.py closes() reads unadjusted Yahoo closes. Not an information edge. The resolver should either adjust for in-window ex-dates or flag them; until then any European name going ex in its window carries a mechanical move the baseline does not see.
- Yahoo LIVE.L closes around 8-10 Jul 2026 read 0.768 (a pence/pounds error), which makes the baseline's realised_vol_60d_pct 20132.93. That field is garbage for LIVE.

## Stage EU — UK register served from a stale cache
- The UK register was read as of 2026-09-19 at a 2026-09-23 seal (eu_positioning serves today's file from cache unless --refresh). RPI: baseline 0.70% and covering; the live FCA file shows 0.92% dated 18/09 (a rebuild). RKH: baseline 'building' +0.33, live file 1.21% (covering from 1.43%). Both hunters carried the live level; baselines left sealed. Consider --refresh on the UK register at seal time.

## Stage EU — Europe researcher — DONE
- Logged at 2026-09-23 14:10 UTC
- 14 hunted, 14 returned, 9 rankable, 0 above conviction floor 3.0. Top SLR +2.50, bottom LIVE -1.40 (mechanical ex-dividend; real bottom VBK -0.50). Not ranked: ATE (wrong date, prints 09-25 amc), KEFI/ALTN/CHAR/RKH (date unconfirmed).
- Note: research/2026/09/2026-09-24/europe/europe-note.md. Published to main with EARNINGS_DATA_BRANCH=main pinned.

## Stage J — Japan researcher — DONE (resumed)
- Logged at 2026-09-24 01:05 UTC
- Scheduled fire 01:04 UTC. Output for 2026-09-24 already existed from the 2026-09-18 validation run (4716 impact_sum -3.50, above floor). Universe re-read to scratch: unchanged, 2 scheduled / 1 eligible / 1 hunted, market_closed null. No new hunt, baseline not revised; addendum appended to japan/japan-note.md. No resolved JP run yet, so no lean_vs_free_control_rho.

## Close AMC — opening-auction exit run — 2026-09-24
- Logged at 2026-09-24 10:16 UTC
- Guard: python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg -> exit 0 (amc placed as a market DAY order queued in the pre-market since auction_orders is False; exit_mode=amc_open).
- verify --scan before closing: all 14 tracked exit legs across the 10 runs on disk already read ok / still held 0.0 — nothing carried an open position into today.
- close --scan --submit: 2026-09-23's run opened 0 positions (no name cleared the floor that day), so there was no leg with an exit date of 2026-09-24 to submit. No new order was sent.
- status --scan confirms the account is flat: equity == cash == $11,200.86, buying power $44,803.44. Every historical entry/exit shows filled or expired, nothing pending.
- Nothing to place this morning. Today's stage E run (19:04 UTC) has not fired yet, so there is no book from today to worry about; if it opens a position tonight, that leg's amc exit (if any) is this Routine's job tomorrow.
- Separately, and outside this task's scope: the primary session checkout at /home/user/claude_research had a stale local 'main' branch (80 commits, no common ancestor with origin/main) left over from container state. It was left untouched (no force-push) and the session's designated feature branch was restored; flagging it here in case it is unexpected.

## Edge hunt — 2026-09-24 amc + 2026-09-25 bmo — STARTED
- Logged at 2026-09-24 17:13 UTC
- Fired 17:05 UTC (13:05 ET). execution.enabled true, exit_mode amc_open. Step 0b: verify/close/status over 10 runs, 14 exit legs all ok, 0 held — account already flat, nothing sold (2026-09-23 opened a book of MANU/WOR whose exits filled 09-23; no leg due today).
- Universe --window: 4 of 28 rows (COST, SCHL, LGCY amc 09-24; TBN bmo 09-25). Thin day, so session_resolve.py run over the 22 time-not-supplied rows: 4 killed already_reported (HUBG 09-15, TRT 09-24, DAVA 09-21, ENLV 09-22), 0 confirmed announced, 18 carried and not hunted. Baselines sealed and committed; COST is the only live option chain (implied 3.22%). Plan: 1 sweep + 4 hunters.

## Edge hunt — 2026-09-24 amc + 2026-09-25 bmo — DONE
- Logged at 2026-09-24 17:28 UTC
- Execution ON (paper). Step 0b: verify/close over 10 runs, 14 exit legs, all ok, 0 held; nothing sold, nothing overdue. Account flat at $11,200.86 equity.
- Universe 4 (COST, SCHL, LGCY amc 09-24; TBN bmo 09-25). The sweep confirmed 4/4 from company sources, 0 phantoms, 0 sessions unsettled. The 22 time-not-supplied rows were checked by session_resolve: 4 killed (already reported), 0 confirmed, 18 not hunted.
- 1 sweep + 4 hunters (5 of 20 subagents). Every hunt carries pre_lessons, print_vs_bar_pct and expected_move_pct, so the agent definition in the tree is the one that ran.
- Ranking (impact_sum): SCHL +0.30, COST 0.00, LGCY 0.00, TBN 0.00. 0 of 4 clear floor 3.0. Pre-lessons: SCHL +1.5, COST +0.3, LGCY -1.0, TBN 0.0; LESSONS.md dropped 4 of 5 draft findings. V2 calibrated (n 175): SCHL +0.19, the rest 0.
- Step 7: plan/open/status. 0 names met the benchmark, 0 orders sent, gross 0% of equity. Refused: all 4 were below the conviction floor. Opened 155 min before the close, so the entry margin was not the constraint.
- V2 shadow ledger: 6 8-Ks collected (1 TBN 8-K skipped, no document text), 6 scored blind, 6 ingested, 0 refused. Pooled session_close n 175, kappa 0.358 (se 0.069).

## Stage CA — Canada researcher — STARTED
- Logged at 2026-09-24 18:33 UTC
- Fired 18:33 UTC (14:33 ET). Plan: ca_universe -> seal baselines before 16:00 ET close -> one unpriced-hunter-ca per name in waves of 5 -> edge_score -> note. Research only, no orders.

## Stage CA — Canada researcher — EMPTY DAY
- Logged at 2026-09-24 18:34 UTC
- TSX open (market_closed null). 8 scheduled / 0 eligible / 0 hunted: all 8 below the $200k turnover floor (max MMY $114k); 5 of the 8 were also filing_only. Calendar: confirmed 1, vendor_only 7, disputed 0. No baselines sealed, so no register snapshot stored. Yahoo CAD/USD failed again (fallback 0.71), not decisive. TMX stack answered. Note: research/2026/09/2026-09-24/canada/canada-note.md

## Stage R — reversal researcher — STARTED
- Logged at 2026-09-24 19:04 UTC
- 19:04 UTC = 15:04 ET, inside the 13:30–16:05 ET screen window. Plan: rev_universe --intraday --k 15 on the open 2026-09-24 session, seal baselines, 15 reversal-hunters in parallel, edge_score, resolve 2026-09-23, note before 16:00 ET. Repo was present (no clone); HEAD on origin/main.

## Stage R — reversal researcher — universe and baselines sealed
- Logged at 2026-09-24 19:06 UTC
- 19:05 UTC: rev_universe --intraday screened 15:04 EDT; 80 above floors, 15 hunted; Health Care 8 of 15 (53%) — one bet, not fifteen. SPY −0.09% at screen. JAGX screener −74.1% vs adjusted −23.7% (gap −50pp, likely reverse split / corporate action); several names show screener ~−10% vs adjusted ~−6.5%, a live-bar lag, recorded not corrected. 15 baselines sealed 19:05 UTC before any hunter. Harness caps concurrent subagents at 8: first wave JAGX TVRD KPLT NCT EOSE BYND RCKT ZBIO; BW OBX BLSM AMTX SLDB MEDS VEEA queued. Resolve: 2026-09-23 run all pending (window closes today); 2026-09-22 run resolved on only 5 of 15 names (resolver drops rows), lean_vs_free_control_rho 0.0, impact_sum rho −0.30 (p 0.69) vs neg_atr14 −0.60, neg_ret_d +0.10 — does not beat the free controls.

## Stage R — reversal researcher — DONE
- Logged at 2026-09-24 19:12 UTC
- Note published 19:12 UTC (before 16:00 ET). 15 of 15 hunted, none shed; 15 rankable; one above the floor: JAGX −3.50 (leg 2, dated supply: ATM refreshed 09:22 ET today at ~115% of market cap plus 547,898 3(a)(9) exchange shares). All nine non-zero names are leg 2 supply; leg 1 empty (overshoot_pct 0 on all 15); six zeros. Health Care 8/15. Summed half-spreads 8.75 vs prediction sd 0.90. impact_sum vs priced_lean rank corr +0.25. Defects noted, constants untouched: (1) rev_resolve keeps only 5 of 15 rows on the 2026-09-22 run; (2) live-bar lag: screener vs adjusted fall differs 3–5pp on six names (AIRS −14.6 screener vs −5.8 adjusted, not hunted); (3) baseline spot_basis reads 'unadjusted close of the drop day' on an intraday seal; (4) harness caps concurrent subagents at 8, so hunters went in two waves — no names lost. No orders placed; no execution step exists in this stage.
