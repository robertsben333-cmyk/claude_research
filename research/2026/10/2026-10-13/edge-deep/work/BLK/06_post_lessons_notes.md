# After reading researcher_us/LESSONS.md (read ~18:03 UTC) and post-freeze checks
- Post-freeze arithmetic (not from LESSONS): back-test of my rebuild on Q2-26 from Q1-26 actuals + Q2 market averages
  reproduces base+SL within 0.2% but under-predicts revenue ~1.9% (perf fees 305 vs ~200 modelled, tech, other) and EPS ~4.5% (operating leverage, nonop +145).
  Q4-25 release: adj EPS 13.16, perf fees 754, nonop -122 (Q3-25 -106, Q1-26 +22, Q2-26 +145) => nonop central 0 +/-100.
  => central adj EPS ~$14.25 raw, ~$14.5 with half the back-test correction (vs $14.25-14.30 consensus). P(>=14.80) ~25%.
- LESSONS rule 1 (reaction function): BLK buys modest beats (Q3-25 ~2.5% EPS beat + record flows -> +3.4%); F1 smaller.
- Rule 6 (bar): revenue bar disputed ($7.45B Zacks-implied vs $7.56-7.60B) -> revenue part of F1 capped; AUM bar single-source (Zacks $15.67T) -> F3 capped.
- Rule 7 (skew): my sign is against a call-bid skew (-6.43); reason given (consensus already absorbed Q3 tailwind; 4/4 history is what the skew extrapolates) but it is inference -> sizes smaller, p_up toward 50. SI 1.3%, DTC 3.6: not crowded.
- Rule 5 (proxy): F2 flows rest on ETFGI brand data + BLK H1 subtraction and an industry series -> small.
- Core: 'priced is a claim you have to prove' -> the whisper above consensus is NOT shown; vs the shown consensus my EPS answer is in line/slight beat.
- Final sizes: F1 -0.3, F2 -0.2, F3 -0.2, F4 +0.1, F5 +0.2 => impact_sum -0.4. abs_move 4.7, p_up 47 => expected -0.28.
## Bar re-verification prompted by LESSONS rule 6 (post-freeze; disclosed)
- Nasdaq API (Zacks) fetched 2026-10-13: Q3-26 consensus $14.01 (6 ests, 13.59-14.40), 1 month ago $14.24, 1 week ago $14.04; 4 down / 0 up in 4 weeks; FY26 $55.69 (from $55.86); Q4-26 $15.09.
  Zacks surprise history: Q3-25 +3.22%, Q4-25 +6.21%, Q1-26 +9.34%, Q2-26 +9.79%.
- => EPS bar DISPUTED: $14.01 (Zacks, cut into the print) vs $14.25 (Benzinga) / $14.28 (TickerLeague). My central ~$14.35 is a modest beat (+1.4% vs midpoint $14.15).
- F1 sign flips to small positive (+0.3): Q3-25-type beat against a lowered bar on a name that has bought beats.
- Final: F1 +0.3, F2 -0.2, F3 -0.2, F4 +0.1, F5 +0.2 => impact_sum +0.2; abs_move 4.7; p_up 52 => expected +0.19. Decision no_trade.
