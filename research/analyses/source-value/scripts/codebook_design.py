#!/usr/bin/env python3
"""Phase 1, layer 2: one Opus call designs the closed list of source subtypes.

  python3 scripts/codebook_design.py           # writes codebook/design-input.json, codebook/design-raw.json

Input: every item text (with its kind and mechanical fields) from a seeded random 15%
of the packs of every stratum. No outcome, no ticker-level result, no live size reaches
the call: items carry only the text, the kind tag, the section (dossiers) and the
mechanical source fields. The call is isolated like every other (scripts/llm.py).
"""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import llm  # noqa: E402

SEED = 20261005
SEEDS = """company's own: earnings pre-announcement; guidance change outside the print; contract or customer win; product launch; executive departure or hire; restructuring or impairment; financing (ATM, convertible, offering); buyback or dividend; going-concern or covenant language; late-filing notice; risk-factor or MD&A wording change; prior-quarter call commentary; investor-day targets; insider buying; insider selling;
other companies: peer earnings result; peer guidance; supplier or customer disclosure; competitor pricing or capacity; M&A in the sector;
official records: FDA or clinical-trial events; court or litigation dockets; government contracts (FPDS, SAM); tariff, trade or customs rulings; macro statistics (BLS, EIA, Census, Fed); company registries abroad;
market data: short interest level and change; option skew or implied volatility; price run-up or drawdown; fund flows; analyst rating or price-target change; consensus estimate and revisions; valuation multiple;
media: major business press report; trade-press report; local news; foreign-language press; retail-finance portal article (auto-generated or opinion); social media or forum;
alternative data: web traffic; app downloads or ranks; job postings; employee reviews; consumer reviews or complaints; foot traffic; shipping or AIS data; pricing scrapes; card or POS panels; search trends;
the researcher's own: arithmetic on public numbers; seasonality or history pattern; absence of a disclosure; search note (searched, found nothing)."""

SYSTEM = """You design a coding scheme (a codebook) for evidence items that researchers collected about listed companies shortly before each company reported quarterly results. You never see what happened after, and you are not asked to forecast anything.

The goal: a CLOSED list of 40 to 70 SOURCE SUBTYPES that a person would recognise ("the company's own 8-K announcing a contract", "a peer's earnings release", "web-traffic data", "a retail-finance portal article", "short-interest data"), so that every item can be assigned to exactly one subtype by a second, cheaper model following your decision rules, and two independent runs of that model agree on at least 80% of items.

A subtype describes WHAT KIND OF SOURCE AND CLAIM the item rests on, not whether it is good news or bad news, and not how reliable it is.

You are given (1) a seed list of candidate subtypes to merge, split or add to, and (2) every item from a random sample of packs, with mechanical fields already computed (`sec_form`, `sec_items` = 8-K item numbers, `newswire_own` = a newswire release by the focal company, `domain_class`). Items come from three strata: US hunts (kinds: filed finding / put outside the window / rejected / searched-and-found-nothing note), US research dossiers (cited claims), and European, Japanese and Australian hunts (where regulators and exchanges differ: RNS, TDnet, ASX announcements count as the company's own disclosure; national short registers count as short-interest data).

Rules for the list:
- 40 to 70 subtypes. Each belongs to exactly one of these GROUPS: company_own, other_company, official_record, market_data, media, alt_data, researcher_own, search_note.
- Cover every item in the sample: every item must fit some subtype. Include one `*_other` catch-all per group so nothing is forced into a wrong subtype; keep catch-alls small.
- Split a candidate only where a second model could tell the parts apart from the item text alone. Merge candidates that would be confused. Prefer subtypes that are common enough to matter (several items in the sample) unless the seed list names them.
- The 'searched, found nothing' notes are numerous: give them subtypes by WHAT was searched for (e.g. no pre-announcement or guidance change found; no insider or ownership filing found; no litigation/regulatory event found; general search found nothing), because "absence of a disclosure" is a claim and "searched broadly, nothing" is not.
- Each subtype: `id` (snake_case, prefixed by a short group code: own_, oth_, off_, mkt_, med_, alt_, res_, srch_), `group`, `name` (plain English, under 8 words), `definition` (one line), `decision_rule` (one or two lines that resolve the likely confusions with named neighbouring subtypes), `examples` (2 short paraphrased example items from the sample, NO company names or tickers).
- Also give `precedence`: an ordered list of short tie-break rules for items that could fit two subtypes (e.g. "an article that reports the company's own 8-K: if it quotes the filing's numbers, code the filing subtype; if it is commentary, code the media subtype").

Reply with ONE JSON object only: {"version": "v1", "groups": {...one-line description per group...}, "subtypes": [...], "precedence": [...], "notes": "..."}."""


def main():
    rnd = random.Random(SEED)
    mech = json.load(open(f'{SV}/data/mechanical.json'))
    items = json.load(open(f'{SV}/data/items.json'))
    by_pack = {}
    for it in items:
        by_pack.setdefault(it['pack_id'], []).append(it)
    sample = []
    for s in ('A', 'B', 'C'):
        ps = sorted(p for p in by_pack if p.startswith(s + '-'))
        k = max(3, round(0.15 * len(ps)))
        sample += sorted(rnd.sample(ps, k))
    packs = {}
    for s in ('A', 'B', 'C'):
        for p in json.load(open(f'{SV}/data/packs-{s}.json')):
            packs[p['id']] = p
    rows = []
    for pid in sample:
        for ev in packs[pid]['evidence']:
            m = mech[f'{pid}#{ev["i"]}']
            r = {'ref': f'{pid}#{ev["i"]}', 'kind': ev['kind'], 'text': (ev.get('text') or '')[:500]}
            if ev.get('section'):
                r['section'] = ev['section']
            if ev.get('source') and not str(ev.get('source')).startswith('http'):
                r['source'] = str(ev['source'])[:160]
            r.update({k: m[k] for k in ('sec_form', 'sec_items', 'newswire_own', 'domain_class') if m.get(k)})
            if m.get('domain'):
                r['domain'] = m['domain']
            rows.append(r)
    os.makedirs(f'{SV}/codebook', exist_ok=True)
    json.dump({'seed': SEED, 'packs': sample, 'n_items': len(rows)}, open(f'{SV}/codebook/design-input.json', 'w'), indent=1)
    user = ('SEED CANDIDATES:\n' + SEEDS + '\n\nSAMPLE ITEMS (' + str(len(rows)) + ' items from ' + str(len(sample)) + ' packs):\n' +
            '\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n\nReply with the JSON object only.')
    print('packs', len(sample), 'items', len(rows), 'chars', len(user))
    if '--dry' in sys.argv:
        return
    text, meta = llm.call(SYSTEM, user, 'claude-opus-5-5', 'codebook_design', 'design', timeout=3000)
    j = llm.parse(text)
    json.dump({'meta': meta, 'raw': text, 'parsed': j}, open(f'{SV}/codebook/design-raw.json', 'w'), indent=1, ensure_ascii=False)
    print(meta, 'subtypes', len((j or {}).get('subtypes') or []))


if __name__ == '__main__':
    main()
