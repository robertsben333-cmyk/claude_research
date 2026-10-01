# Judging skill (learned from 124 resolved cases, fold 0)

Your job is to pick the few names worth money and leave the rest low. In the casebook, the
hunter's own signed sum was close to a coin flip, or worse, everywhere except at the top of
its range. So most of what follows is about what keeps a name **low**.

Your pack does not show the hunter's sizes. Build your own `impact_sum` from the evidence
items, as the hunter definition would, and then apply the rules below to that number.
"Sum" below means the net signed sum of the item sizes, in points of spot.

## Rules

**1. Magnitude is the gate. Only a large net sum earns high certainty.** In the casebook, by
the hunter's |impact_sum|:

| \|sum\| | sign right | note |
|---|---|---|
| 5 or more | **11 of 14** | every right call moved 3.5% or more; spread over six days |
| 3 to 5 | 10 of 20 | net loss when traded |
| 1.5 to 3 | 11 of 23 | |
| 0.6 to 1.4 | 8 of 21 | |
| 0.5 or less | 9 of 23 | |

Below 5, the sign is no better than chance, and below 1.5 it is worse. A sum of 5 or more
almost always came from **at least three independent items pointing the same way**. Each was
grounded in a primary document (a filing, the company's own release, a court or regulator
record) and carried a quantified gap. Real counter-evidence was small (9 of 11 right when
three or more same-direction items made up the sum). One big item alone was 1 of 2 at this
size. Do not reach 5 by inflating a single item.

**2. No findings means no view.** 23 cases had no findings or only zero-size items. Their
realised moves ran from −21% to +11%, so do not guess a direction. Set direction 0 and
certainty 0 to 5.

**3. A documented crowded short points up. Never put a confident short against one.** When an
item records heavy or building short interest (roughly 8% of float or more, high days to
cover, or a record level on a short register), the stock rose **11 of 14** times. Longs
backed by such an item were right 8 of 11. Shorts placed against one were right **0 of 3**,
and those were the largest losses in the book. If such an item is present, cap a short at
certainty 20. For a long, the item can add about 5 to 10 certainty on top of other evidence.

**4. Proxy and macro data are anti-informative as a main basis.** Weather, industry
statistics, price indices, commodity prices, web traffic and app or device counts were cited
as leading evidence 18 times. The direction they implied was right **6 of 18**. Names whose sum
rested mainly on such proxies were right 1 of 8. Do not count a proxy item as one of the
"three primary-document items" in rule 1. A name built mainly on proxies stays at certainty
25 or below, whatever its size.

**5. Peer read-across and sector windfall themes carry no weight.** Peer prints ("the closest
comparable reported strong or weak") implied the right direction 9 of 17 times. Tariff-refund
or one-off windfall items were 5 of 8, and they are one shared theme across many names, so
they are a correlated bet and not evidence. Size them small and add no certainty for them.

**6. "The bar is too high" works; "they will beat a low bar" does not.** Items arguing that
consensus sits above what the company's own guidance, pre-announcements or arithmetic can
support were right **10 of 14**. Items arguing that consensus is too low, management
sandbags, or a beat is mechanical were right **4 of 10**. Weight the first kind fully. Halve
the second kind, and never let it be the main basis of a long above certainty 35.

**7. Stacked primary-document distress supports a short.** Examples are going-concern
language, an exchange delisting or minimum-bid clock, an adverse court ruling, an auditor
dismissal, an expiring lock-up, an insider buying plan going quiet, a pending impairment
larger than the market value, or revenue pulled forward from a one-off balance. When two or
more of these stacked on a small cap and the hunter was short, it was right **7 of 9**. This is
the most common route to a valid sum of 5 or more on the short side. The two misses carried
a contrary positioning or squeeze item (see rule 3).

**8. Moderate shorts are where money was lost.** Shorts sized 3 to 5 were right **3 of 9**, and
the six misses averaged a +15% move against the book. Shorts of 1.5 to 5 were right 8 of 19
overall, against 13 of 24 for longs of the same size. A short below 5 stays at certainty 35
or below. There is a weaker tilt as well: shorts on names that rose over the five sessions
before the print were right 5 of 13, against 12 of 17 for names already falling. Much of that
gap comes from one bad day, so let it lower certainty by about 5, never more.

**9. Small-reaction markets (tentative).** In European packs with no option-implied move and
median past reactions of about 2 to 6%, sums of 1.5 or more were right 7 of 9. That covers
only two days. It can lift such a name to 40 to 55, but on its own it is not enough for 60.

## Calibration

- Leave most names below 30. In the casebook, about **1 name in 8 or 9** met the bar for 60 or
  more. Expect to place one or two names out of a dozen there, and none on some days.
- **60 to 75** needs all four of these:
  - your own sum is 5 or more,
  - it is built from at least three primary-document items in one direction,
  - it is not resting on proxies (rule 4),
  - for a short, there is no crowded-short item (rule 3).
  Do not go above 75. Even this bucket was wrong 3 times in 14, once by 32%.
- **40 to 55**: a sum of 3 to 5 on a long backed by bar-too-high-for-shorts logic or a
  crowded short, or a European name under rule 9.
- **15 to 35**: a sum of 1.5 to 5 that does not qualify above, and every short below 5.
- **0 to 15**: a sum below 1.5, mostly proxy evidence, or no findings at all.
- Set `expected_move_pct` from the pack's implied move, or failing that its median past
  reaction. Raise it only for a high-certainty name where distress or a squeeze is
  documented.

## Per-company checklist

1. Are there any findings with a nonzero size? If not, direction 0 and certainty 0 to 5.
2. Size each item yourself and sum. Mark which items are primary documents and which are
   proxies, peer read-across or windfall themes. Shrink the latter.
3. Is the net sum 5 or more, built from three or more same-direction primary items? If not,
   the ceiling is 55, and 35 for a short.
4. Is there a crowded or building short item? If so, cap a short at 20, and allow a long +5
   to +10.
5. Is the case "bar too high" (keep it) or "they'll beat a low bar" (halve it)?
6. For a short, is there stacked distress in filings (supports it), and did the stock rise
   into the print (−5)?
7. Place the certainty in its calibration band. Check that across the whole set only about
   one name in seven or eight sits at 60 or more.
8. Write `basis` naming the item indices behind the sum, and `against` naming the strongest
   contrary item, especially any short-interest or proxy weakness.
