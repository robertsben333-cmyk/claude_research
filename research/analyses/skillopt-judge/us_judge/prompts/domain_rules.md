## Rules specific to this skill (they override anything above)

The agent is a judge that sizes earnings evidence for one US company before its print.
Each trajectory's Hidden Reference gives what the stock then did. Read these rules
before proposing any edit.

1. **One outcome is one noisy draw.** US earnings moves have a standard deviation near
   10 points and about half of all signs are coin flips. A trajectory that lost money may
   have reasoned well, and one that made money may have been lucky. Propose an edit only
   for a pattern you can see in at least three trajectories of this batch, and state the
   count in your reasoning.
2. **No names, no dates, no hindsight.** Never write a company, ticker, product, person,
   date or price level into an edit. Every edit must be a rule a judge can apply to an
   unseen company using only its pack and the fixed reference documents.
3. **No blanket direction.** Do not add a rule that tilts every judgement up or down
   ("lean short", "the market overreacts"). A direction learned from a few days is that
   week's drift, not skill. Rules about WHICH evidence qualifies, how `p_up` moves with
   its strength, and when `abs_move_pct` departs from what the baseline priced are fair.
4. **Do not touch the output contract.** The Output section and its JSON shape must stay
   exactly as they are. Do not edit or contradict the fixed reference documents (the
   hunter definition, the shared core, the lessons file); you may only add judging rules
   on top of them.
5. Keep the skill short. Prefer replacing or deleting a weak rule over appending a new
   one.
