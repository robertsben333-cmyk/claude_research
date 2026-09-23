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
