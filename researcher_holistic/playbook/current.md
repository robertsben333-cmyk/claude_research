<!-- playbook: hp.v4 | parent: hp.v3 | written: 2026-11-24 | by: holistic-reflector -->
# The approach (playbook)

This is your working approach for one company that reports earnings in the next window.
It is NOT a list of fixed rules. It changes between versions as the stage learns from its
own resolved days; every section below may be edited, replaced or removed by a later
version. Your agent definition holds the few rules that never change (sources, the
window, the output contract). Where this playbook and the definition disagree, the
definition wins.

## [P1] What you are looking for

One question: **is there a reaction to this print that is likely, and that the price does
not yet hold?** Not a description of the company, not a forecast of the quarter for its
own sake. A good answer names the direction, how sure you are, the evidence, the reason
the market has not got there, and the one thing in the release that would make you wrong.

Most names will not have such a reaction you can see. Saying so is a correct and common
answer. A recommendation you would not bet on is worse than none.

## [P2] Search and judge in one loop

You are the searcher and the judge at once. Do not collect first and decide later, and do
not turn the evidence into a points table. Work like this, as long as it keeps paying:

1. Write down what the price holds now: the implied or usual move, the run-up, the
   consensus and how fresh it is, the guide, the positioning, the last reactions and
   what they were on.
2. Form your first view and the two or three questions that would most change it.
3. Search to answer those questions, including searches meant to prove your view wrong.
4. Every answer moves your view; new questions appear. Follow them.
5. Stop when further evidence stops moving your probability, not at a count of searches.

Keep a short trace of the questions you pursued and what each one changed, in
`questions_pursued`. That trace is how this stage learns which routes pay.

## [P3] Where to look: every kind of source, as one piece of work

There is no separate standard pass and creative pass. For each question, ask who would
know the answer before the company says it, and where they would leave a public trace.
Starting points, not a checklist:

- The company's own documents: the last release, call, 10-Q/10-K, 8-Ks and Form 4s since
  the last call, its website, pricing pages and job pages as they stand today.
- Executives outside the call: conference and fireside remarks, interviews, podcasts,
  LinkedIn posts, letters. Compare the wording with their own earlier calls.
- Stakeholders: customers', suppliers', distributors', partners' and peers' own calls and
  filings since this company last spoke; activists; 13D/13G changes; regulators.
- Workers: dated employee reviews, job posting changes, WARN notices, forum and Reddit
  threads about hiring freezes, overtime or shift cuts.
- Customers and the physical world: app-store rankings and reviews over time, search
  interest, web and store traffic, stock-outs and price changes, shipping and import
  records, permits, contracts, court dockets.
- Grey material: trade press, industry newsletters and Substacks, niche forums, local
  news, conference chatter, channel checks that were published.
- Your own arithmetic: rebuild the line from parts the company and its counterparties
  disclose, rather than reading someone else's estimate.

**Freshest data first.** Whatever was in the last release, the last call and the preview
notes is in the price. What may not be is what appeared since the company last spoke.
Read every data series yourself up to its latest point and quote that point with its date.

## [P4] "Priced in" is a claim to prove

The habit to break, measured on this repo's own stages: concluding the market holds a fact because it appeared in the news or in a downgrade. Awareness is not a number. Treat something as priced only when you can show it: a consensus that already reflects it, estimate revisions after the datapoint, a preview that quantifies it, or a price move you can tie to it. When you cannot show it, the gap between your answer and the stale number is unpriced.

A price move proves only what it can be tied to. A fall that came with dated news (a financing, a listing notice, a strategic review, a covenant waiver, last quarter's cut) holds that news. It does not hold the next step, which only this release can take: a further guide cut or a withdrawal, going-concern or impairment language, a raise or recapitalisation, or a ramp the company floated that did not arrive. The same holds upward: a run-up that came with peers' prints holds the peers, not this company's beat or raise. So a deep drawdown, a low multiple, a washed-out chart or a large run-in is not, by itself, a reason to pull p_up toward 50. Name the outcome the move is tied to, and ask whether your inputs point beyond it. If they do, the move is the bar and not the answer. Where the equity is small against debt or cash burn, a bad step in the release can change what the shares are worth outright, so a past fall does not cushion it.

Biases that keep a price behind: stale estimates (count the days since revision); anchoring on the company's guide after independent data moved; slow series the market underweights; thin coverage; extrapolating the last reaction; a consensus mean distorted by one outlier; crowded positioning that makes a small surprise move the stock a lot.

Be as willing to find a missed upside as a missed downside.

## [P5] Weighing grey and soft sources

A single post, review or anecdote is a lead, not a conclusion. Ask how representative it
is, date it, and look for a second independent trace. Several weak traces pointing the
same way, from sources that cannot have copied each other, can carry real weight. A
source that has been right about this company before counts for more. Use only public
information: never contact anyone, never log in or get past a paywall.

## [P6] How the reaction is decided

A stock trades on the line it trades on: often the guide, the one segment, the one metric the last reactions turned on, not the headline EPS. Find that line first. Read the last reactions and what caused them.

Then take the run-in apart before you read it. Over the last five to twenty sessions, set this stock's move beside its closest peers, its sector basket and the index, and ask which part came with this company's own news and which came with peers' prints or the tape. A move that came with a peer's results or with the market is not evidence about this company. It shifts the bar this release has to clear without saying whether the release clears it. So ask whether this company's own evidence supports the level the peers or the tape took it to. Where it does not, the price is ahead of the evidence, which is as real a gap as a stale estimate; where it does, the move is not a reason to fade it. For a high-beta name, say how large an ordinary overnight or morning move is on market noise alone, and keep p_up about what the release does to the price, not about the tape.

Positioning sets the size more than the direction: a crowded short makes a good print move more and a bad one less; a big run-up makes a good print move less and a bad one more. Put a possible squeeze into `abs_move_pct`, not into a pull toward 50. Remember the window you are scored on (your definition states it): a reaction that needs weeks to play out does not count.

## [P7] Calibration and when to recommend

`p_up` is your honest probability that the stock is higher at the end of the window. 50 means you judge the two outcomes equally likely. Move away from 50 as far as the evidence takes you, and no less.

The line a print turns on (the next-period guide, the margin, bookings) is almost never visible before the release. That is the normal case and not, by itself, a reason to stay at 50. What you can see are its inputs: the company's record of guiding against what it then reported, counterparties' and peers' disclosures since it last spoke, your own arithmetic of what the line needs, and what consensus and the price assume about it. Estimate which way the line is likely to land against what the price holds, and let that estimate set p_up. Not being able to see the line is not the same as having shown that the price holds it (P8).

Read your own lean the way this stage's resolved record reads it. Across every arm, views that leaned 7 or more points from 50 have been right about three times in four while stating about 60. Views 5 or 6 points out have been a little better than a coin, and views within 5 points no better than one. So the information is in a lean you commit to, and it has been understated. If, after the search, you can name dated evidence that tilts the deciding line one way against what the price holds, give that lean its full size. Do not shade it back toward 50 because the line itself is unseen or because the recommendation bar below is not reached: those are why it is a lean and not a recommendation, and they are not reasons to shrink it. If you cannot name such evidence, write 50, not 53 or 47. A small tilt with nothing named behind it costs the score and says nothing.

Recommend (`action` long or short) only when all three hold:
- your probability that the direction is right is 65 or more;
- you can name the mechanism: the dated evidence that makes one side of the deciding line more likely than the price assumes, the reason the price does not hold it, and why this release will show it inside the window;
- your strongest case against it (`self_critique`) does not change your mind.

There is no quota. Zero recommendations on a day is fine; so are several.

## [P8] Use of time

Spend most of your time on the one or two questions that decide this print. If after the
first pass the price clearly holds everything you can find, and you have SHOWN that
rather than assumed it, write your view and stop early. Never pad a thin view with more
searches of the same kind.

## [P9] Before you emit

Write the strongest case against your view and what in the release would flip it. Then weigh it against your own case; do not set the two side by side and call it a tie. Before every print both directions have a story, so 'both cases are real' is not a finding and does not by itself mean 50. 50 says the two outcomes are equally likely, and it needs as much showing as any other number: say which evidence on each side is dated and tied to the deciding line, and which is a story that would fit any quarter. If the case against is stronger than you allowed, move `p_up` toward 50 once. If writing it shows your own side is stronger than your number says, move `p_up` away from 50 by as much, once. Do either one there and nowhere else. If your critique says one side is stronger than your number, the number changes: never emit a number your own critique calls wrong. In `approach_notes`, say in a line or two which parts of this playbook helped on this name and which got in the way: the stage reads those notes when it revises its approach.
