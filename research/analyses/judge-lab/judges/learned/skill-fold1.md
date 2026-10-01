# Judging skill (fold 1): which names to be sure about

Learned from 125 resolved cases on other days: 83 US names with a hunter call, 19
European, 4 Australian and 3 Japanese, plus 16 names with no findings. Every count
below comes from that casebook. "Right" means the realised move had the hunter's sign.
Rules about a single finding are counted per finding. Rules about a whole name are
counted per name.

## The starting point: the hunter's sign is a coin flip

**R1. Start every name low.** Across regions the hunter's sign was right 56 of 109
times. In the US it was right 42 of 83, while 45 of those 83 names fell, so shorting
every name would have done slightly better. Nothing in a pack is reliable just because
the hunter filed it. Start at certainty 15 to 25 and move up only for the evidence
types in R4 to R7.

**R2. Leave tiny sums alone.** Names with |impact_sum| below 1 were right 11 of 32,
which is worse than chance. That holds in every region: Australia was 0 of 4, and US
names below 1 were 6 of 19. Give them certainty 10 or less, whatever the story.

**R3. Size helps only a little.** In the US the hit rate by |impact_sum| was:
- 5 or more: right 12 of 20
- 3 to 5: right 9 of 18
- 1 to 3: right 15 of 26

The sum of the hunter's sizes does not raise certainty by itself. Seven names had
|impact_sum| of 10 or more and only 4 of them were right. Read the size as "the hunter
found a lot". The evidence type is what decides whether that matters.

## Evidence types that earned certainty

**R4. "The bar is above what the company's own guide allows" works going down. "The
bar is too low" does not work going up.** Down findings were right 12 of 16. They
include:
- consensus at or above the top of the guide
- a guide that needs a large back-half ramp
- a backlog that is shrinking while revenue is held flat

These were spread over six days, and 7 of 10 were right after removing the
best-performing day. Up findings of the mirror kind were right only 9 of 18. These
include:
- "the bar is low"
- "they always beat their own guide"
- "consensus implies too little"

Four of those up misses fell 9% or more. Pay for downside arithmetic. Treat expected
beats as noise.

**R5. Turnover among the CFO, the revenue chief or the accounting officer points
down.** This covers a new CFO on a first call, an interim CFO, a revenue chief
mid-transition, and a guide inherited from a departed author. As down findings they
were right 7 of 8, across five days.

**R6. Balance-sheet pressure points down.** This covers:
- covenant headroom rolling off
- minimum-bid or listing deadlines
- court liability
- a cash runway that depends on proceeds that have not closed
- unprovisioned related-party receivables
- an insider buyer who stopped buying
- goodwill or impairment tests landing in the reported quarter

As findings these were right 12 of 17. Names whose main case was this kind of pressure
were right 8 of 11.

**R7. Hard data covering the exact reported period, from a direct peer or a count.**
This means a direct peer's print for the same quarter, or an industry count for exactly
the reported months, such as:
- background checks
- registrations
- server-maker margins
- peer same-store sales

When this was the name's largest item it was right 8 of 12. The two largest correct
calls in the casebook rested on several independent series of this kind all pointing
the same way. A "peer" that is only loosely related, or that covers a different
window, does not count.

## Evidence types that should lower certainty

**R8. Macro inputs are weak evidence.** This covers commodity prices, freight rates,
spot charter rates, weather and oil. When the case rested on them it was right 5 of
13. Use them only as a tie-breaker.

**R9. Short-interest and squeeze arguments for an up move fail.** This covers high
short interest, days to cover, "shorts will have to cover" and a family or holder
buying on print days. These up findings had the right sign 4 of 11 times, and only
once did the move exceed 2%. If positioning is the main reason for an up call, keep
certainty at 20 or less.

**R10. One-off or non-operating gains do not lift the stock.** This covers tariff
refunds, a deferred divestiture gain, a tax-asset release and a fair-value gain on
held shares. As up findings they were right 4 of 10. Twice the hunter's largest finding
was a refund, and both names fell 10 to 19%. Findings saying "the market strips these
refunds out" were right both times.

**R11. Up calls carry the left tail.** US up calls were right 19 of 41 and down calls
23 of 42. Among up calls, 13 fell more than 9% and only 7 rose more than 9%. An up call
needs R7-quality evidence to reach 60. A down call can reach 60 on R4, R5 or R6.

**R12. Very large implied moves lower certainty.** When options priced a move of 12% or
more, the hunter was right only 7 of 18 times. The one large clean win in that group
had several independent R7 series. Without that, cap these names at 45.

**R13. Watch for regional and day effects.** Europe was right 13 of 19. But 15 of the
23 European names fell, and European down calls (9 of 11 right) were mostly riding the
same tape. European sizes are also small, mostly under 1. Do not push a European name
past 50 on direction alone. Australia and Japan together were right 1 of 7, so treat
them as R2.

The same caution applies in the US. On the busiest US day, 14 of 22 names fell and the
down calls went 8 of 12. A pattern that holds only on one day's names is the market
moving together, not a rule.

**R14. No findings means no view.** Sixteen names had no findings. Give them direction
0 and certainty 0, even when the stock has run up or sold off. Those 16 later moved
anywhere from −25% to +7%, and nothing in their packs predicted which.

## Calibration

- Aim for about one name in seven at certainty 60 or above. Most names belong between
  10 and 40.
- **To reach 60, a name needs all three of these:**
  - |impact_sum| of about 3 or more, or your own re-sum of the pack's items at that
    level.
  - A main basis from R4, R5, R6 (down calls) or R7 (either direction).
  - No main reliance on R8, R9 or R10, and an implied move under 12%. R7 with several
    independent series is the exception to the implied-move limit.

  In this casebook that filter selected 13 of the 38 US names at |impact_sum| ≥ 3, and
  10 of the 13 were right. The four large up calls it rejected all lost.
- **70 and above** is only for names where two qualifying types agree. Examples:
  guide arithmetic plus finance-officer turnover, or several R7 series in the same
  direction.
- **Below 25:** anything resting on positioning, refunds, macro inputs or "the bar is
  low". Also any sum under 1, and any name outside the US and Europe.
- Set `impact_sum` to your own signed re-sum. Drop items in the R8 to R10 classes or
  shrink them hard. Keep R4 to R7 items at the hunter's size.

## Checklist (run for each company)

1. Are there findings? If not, set direction 0 and certainty 0.
2. Is |impact_sum| under 1, or is the market Australia or Japan? If so, set certainty
   10 or less.
3. Name the largest one or two items and put each in a class: R4 down, R5, R6, R7, R8,
   R9, R10, or "bar too low".
4. Is the call up? Then it needs R7 hard data for the exact period to go above 45.
5. Is the implied move 12% or more? Then cap at 45 unless several R7 series agree.
6. Do items of a different qualifying class oppose the call? Then subtract 10 to 20.
7. Is the main case positioning, refunds or one-offs, macro inputs, or an expected
   beat? Then cap at 25.
8. Count how many names are at 60 or above. If it is more than about one in six, cut
   the weakest back to 50.
9. Write `basis` naming the class and the item indexes. Write `against` naming the
   strongest opposing item, or the base rate if nothing in the pack opposes the call.
