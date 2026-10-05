#!/usr/bin/env python3
"""Build the item-level dataset over every resolved US hunt on disk.

  python3 build.py      # writes data/events.json, data/items.json, data/packs.json

One EVENT row per hunted name in the dashboard ledger (163: the 154 of the four-model
re-judge, the five 09-04 hunts of the 09-08 prints that were hunted again on 09-07, and
MKC, AYI, ACN, NKE resolved since). `event_key` (ticker + event date) groups the 09-04
duplicates with their 09-07 twins, so no statistic counts one print twice.

One ITEM row per evidence item, in exactly the order `../rejudge-four-models/build_packs.py`
numbers them (findings, then outside-window, then rejected, then searched-and-found-
nothing, hunt file by hunt file), so `i` joins to the re-judge packs and to the labels.
Each item keeps what the packs strip: the live hunter's signed size and range.

`role` follows judge-lab's frozen day split. Days it never assigned: 09-04 joins its
twin day (train); 10-01 is `new`. The judge-lab TEST days are `test` and analysis code
keeps them out unless asked to unseal.

`packs.json` holds one blinded pack per event for the labeler, anonymised where the
ticker or company appears in the context every model sees (CLAUDE.md, the core, the
hunter definition, the US lessons file), with the re-judge's own scrubber.
"""
import glob, json, os, re, sys
from datetime import date
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'judge-lab'))
import judge_lab as J  # noqa: E402

REJ = os.path.join(HERE, '..', 'rejudge-four-models')
SIZE = re.compile(r'\b[Ss]ized? (at|to) [^.;]*|\bcut (it )?from [-+]?\d[^.;]*|\(lesson[^)]*\)|\blesson \d+\b[^.;]*|\bp_up\b[^.;]*|\babs_move[^.;]*', re.I)
URLS = re.compile(r'https?://[^\s)\]>"\',;]+')
DATE = re.compile(r'(20\d\d)-(\d\d)-(\d\d)')
STOP = {'inc', 'inc.', 'plc', 'ltd', 'ltd.', 'corp', 'corp.', 'corporation', 'company', 'co', 'co.', 'sa', 'se', 'ag', 'nv', 'ab',
        'asa', 'oyj', 'spa', 's.p.a.', 'the', 'group', 'holdings', 'holding', 'limited', 'a/s', '&', 'and', 'of', 'international',
        'technologies', 'plc.', 'n.v.', 's.a.'}
URL_SCRUB = re.compile(r'(https?://|www\.)\S+|\b[\w-]+\.(com|net|org|co\.uk|de|fr|it|se|no|dk|fi|pl|es|jp|com\.au|ca|io|ai)\b[/\S]*', re.I)


def sc(s):
    return SIZE.sub('[sizing note removed]', s) if isinstance(s, str) else s


def trim(o):
    if isinstance(o, dict):
        return {k: trim(v) for k, v in o.items() if k not in ('headlines', 'raw', 'bars', 'series')}
    if isinstance(o, list):
        return [trim(x) for x in o[:12]]
    if isinstance(o, str) and len(o) > 600:
        return o[:600] + '…'
    return o


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def domain(u):
    try:
        d = urlparse(u).netloc.lower()
    except ValueError:
        return None
    return d[4:] if d.startswith('www.') else (d or None)


def first_date(s):
    m = DATE.search(s or '')
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def raw_items(hfiles):
    """Pack evidence plus the raw fields, in build_packs order."""
    out = []
    for h in hfiles:
        j = json.load(open(h))
        tag = os.path.basename(h)
        for f in j.get('findings') or []:
            out.append(({'kind': 'filed_by_first_hunter', 'hunt': tag, 'text': sc(f.get('finding')), 'lands_on': f.get('lands_on'),
                         'leg': f.get('leg'), 'resolves_by': f.get('resolves_by'), 'source': f.get('source'), 'source_date': f.get('source_date'),
                         'reaction_history_on_this_line': sc(f.get('reaction_history_on_this_line')),
                         'why_not_priced': sc(f.get('why_not_priced')), 'independence': sc(f.get('independence'))}, f))
        for o in j.get('outside_window') or []:
            od = o if isinstance(o, dict) else {}
            out.append(({'kind': 'put_outside_window_by_first_hunter', 'hunt': tag, 'text': sc(od.get('finding') if od else o),
                         'resolves_by': od.get('resolves_by'), 'source': od.get('source')}, od))
        for r in j.get('rejected_candidates') or []:
            out.append(({'kind': 'rejected_by_first_hunter', 'hunt': tag, 'text': sc(r.get('candidate')), 'source': r.get('source'),
                         'first_hunter_reason': r.get('reason')}, r))
        for s in j.get('searched_and_found_nothing') or []:
            out.append(({'kind': 'listed_as_searched_and_found_nothing', 'hunt': tag,
                         'text': sc(s if isinstance(s, str) else json.dumps(s))}, s if isinstance(s, dict) else {}))
    for i, (e, _) in enumerate(out):
        e['i'] = i
    return out


def ctx(h):
    d = json.load(open(h))
    return {'bar': sc(d.get('bar')), 'positioning_check': d.get('positioning_check'), 'already_public': d.get('already_public'),
            'new_in_release': d.get('new_in_release'), 'session_check': d.get('session_check')}


def context_text():
    files = ['CLAUDE.md', 'config/hunter-core.md', '.claude/agents/unpriced-hunter.md', 'researcher_us/LESSONS.md']
    return '\n'.join(open(os.path.join(R, p)).read() for p in files if os.path.exists(os.path.join(R, p)))


def leaked(t, company, ctxt):
    if re.search(r'(?<![A-Za-z0-9])' + re.escape(t) + r'(?![A-Za-z0-9])', ctxt):
        return 'ticker'
    words = [w for w in re.split(r'\s+', (company or '').replace(',', ' ')) if w and w.lower() not in STOP]
    if words and len(' '.join(words[:2])) >= 6 and ' '.join(words[:2]) in ctxt:
        return 'company'
    return None


def scrubber(t, company):
    pats = [re.escape(t)]
    c = (company or '').replace(',', ' ')
    if c.strip():
        pats.append(re.escape(c.strip()))
    ws = [w for w in re.split(r'\s+', c) if w and w.lower() not in STOP]
    if ws:
        if len(' '.join(ws[:2])) >= 4:
            pats.append(re.escape(' '.join(ws[:2])))
        if len(ws[0]) >= 4:
            pats.append(re.escape(ws[0]))
    rx = re.compile(r'(?<![A-Za-z0-9])(' + '|'.join(sorted(set(pats), key=len, reverse=True)) + r')(?![A-Za-z0-9])', re.I)

    def f(o):
        if isinstance(o, dict):
            return {k: f(v) for k, v in o.items()}
        if isinstance(o, list):
            return [f(x) for x in o]
        if isinstance(o, str):
            return rx.sub('[THE COMPANY]', URL_SCRUB.sub('[url removed]', o))
        return o
    return f, rx


def rejudges():
    """Every four-model re-judge output, keyed by the key.json id."""
    key = json.load(open(f'{REJ}/key.json'))
    pid = {k.get('pid', k['id']): k['id'] for k in key}
    out = {}
    for f in glob.glob(f'{REJ}/out-*-*.json'):
        m = os.path.basename(f)[:-5].split('-')[-1]
        for o in json.load(open(f)):
            if o['id'] in pid:
                out.setdefault(pid[o['id']], {})[m] = {k: o.get(k) for k in ('impact_sum', 'p_up', 'abs_move_pct')}
    return out


def rated():
    """The rated Sonnet judge of ../skillopt-judge (two runs) and its ratings."""
    out = {}
    base = os.path.join(HERE, '..', 'skillopt-judge')
    for sp in ('train', 'val', 'test'):
        p = f'{base}/data/{sp}/items.json'
        if not os.path.exists(p):
            continue
        ids = {i['id']: i['name_id'] for i in json.load(open(p))}
        for k in (0, 1):
            f = f'{base}/runs/rated-{sp}-{k}/rollouts.json'
            if not os.path.exists(f):
                continue
            for r in json.load(open(f)):
                try:
                    j = json.loads(r.get('predicted_answer') or '')
                except ValueError:
                    j = {}
                out.setdefault(ids[r['id']], []).append({'impact_sum': r['impact_sum'], 'p_up': num(j.get('p_up')),
                                                         'abs_move_pct': num(j.get('abs_move_pct')),
                                                         'reliability': num(j.get('evidence_reliability')),
                                                         'sufficiency': num(j.get('evidence_sufficiency')), 'key_gap': j.get('key_gap')})
    return out


def main():
    S = json.load(open(J.SPLIT))['days']
    ledger = json.load(open(f'{R}/dashboard/data/ledger.json'))['names']
    ctxt = context_text()
    RJ, RT = rejudges(), rated()
    events, items, packs = [], [], []
    for n in ledger:
        if n.get('pending') or n.get('mv_strategy') is None:
            continue
        d, t = n['run'].rstrip('/'), n['ticker']
        hs = sorted(glob.glob(f'{R}/{d}/hunts/{t}.json') + glob.glob(f'{R}/{d}/hunts/{t}-*.json'))
        bpath = f'{R}/{d}/baselines/{t}.json'
        if not hs or not os.path.exists(bpath):
            continue
        day = n['run_date']
        eid = f'us/{day}/{t}'
        role = S.get(f'us/{day}') or {'2026-09-04': 'train'}.get(day) or 'new'
        b = json.load(open(bpath))
        opt, tape, hist = b.get('options') or {}, b.get('tape') or {}, b.get('history') or {}
        em = b.get('expected_move') if isinstance(b.get('expected_move'), dict) else {}
        implied = num(opt.get('event_implied_move_pct')) or num(em.get('pct'))
        priced = implied or num(b.get('expected_move_pct')) or num(hist.get('median_abs_move_pct')) or 5.0
        lk = leaked(t, n.get('company'), ctxt)
        ri = raw_items(hs)
        ev = {
            'id': eid, 'event_key': f"{t}/{n.get('event_date')}", 'duplicate_hunt': bool(n.get('duplicate_event')),
            'role': role, 'day': day, 'ticker': t, 'company': n.get('company'), 'sector': n.get('sector'), 'industry': n.get('industry'),
            'session': n.get('session'), 'event_date': n.get('event_date'), 'entry_date': n.get('entry_date'),
            'move': n['mv_strategy'], 'move_open': n.get('mv_open'), 'move_close': n.get('mv_close'), 'move_pre_open': n.get('mv_pre_open'),
            'dollar_vol': n.get('dollar_vol'), 'market_cap': n.get('market_cap_usd'), 'tradable': (n.get('dollar_vol') or 0) >= 2e5,
            'vol20': num(n.get('realised_vol_20d')) or num(tape.get('realised_vol_20d_annualised_pct')),
            'runup_5d': n.get('runup_5d'), 'runup_20d': n.get('runup_20d'), 'retail_tilt': n.get('retail_tilt'),
            'search_spike': n.get('search_spike'), 'priced_lean_pct': n.get('priced_lean_pct'),
            'implied_move': implied, 'priced_move': max(priced, 1.0), 'hist_median_move': num(hist.get('median_abs_move_pct')),
            'baseline_quality': num((b.get('baseline_quality') or {}).get('score') if isinstance(b.get('baseline_quality'), dict) else b.get('baseline_quality')),
            'skew_25d': num(opt.get('skew_25d_vol_points')), 'put_call_oi': num(opt.get('put_call_open_interest_ratio')),
            'options_status': opt.get('status'), 'priced_direction_lean': opt.get('priced_direction_lean'),
            'live_impact': n.get('impact_sum'), 'n_findings': n.get('n_findings'), 'hunter_model': n.get('model_short') or n.get('model'),
            'prompt_version': n.get('prompt_version'), 'n_hunts': len(hs), 'shortable': n.get('shortable'),
            'leak': lk, 'rejudge': RJ.get(eid, {}), 'rated': RT.get(eid, []),
            'bar_present': bool(ctx(hs[0]).get('bar')),
        }
        events.append(ev)
        entry = first_date(n.get('entry_date'))
        for e, raw in ri:
            urls = sorted(set(URLS.findall(json.dumps(raw, ensure_ascii=False)) + ([e['source']] if (e.get('source') or '').startswith('http') else [])))
            sd = first_date(e.get('source_date') or raw.get('source_date') if isinstance(raw, dict) else None)
            items.append({
                'event': eid, 'event_key': ev['event_key'], 'role': role, 'i': e['i'], 'kind': e['kind'], 'hunt': e['hunt'],
                'text': e.get('text'), 'source': e.get('source'), 'domain': domain(e.get('source') or ''),
                'n_urls': len(urls), 'domains_all': sorted({domain(u) for u in urls if domain(u)}),
                'source_date': str(sd) if sd else None, 'age_days': (entry - sd).days if (sd and entry) else None,
                'lands_on': e.get('lands_on'), 'leg': e.get('leg'), 'resolves_by': e.get('resolves_by'),
                'why_not_priced': e.get('why_not_priced'), 'first_hunter_reason': e.get('first_hunter_reason'),
                'has_reaction_history': bool(e.get('reaction_history_on_this_line')),
                'live_size': num(raw.get('expected_impact_pct')) if isinstance(raw, dict) else None,
                'live_low': num(raw.get('impact_low_pct')) if isinstance(raw, dict) else None,
                'live_high': num(raw.get('impact_high_pct')) if isinstance(raw, dict) else None,
                'live_category': J.cat_of(raw) if e['kind'] == 'filed_by_first_hunter' and isinstance(raw, dict) else None,
                'text_len': len(e.get('text') or ''),
            })
        p = {'id': eid, 'baseline': trim(b), 'first_hunter_context': ctx(hs[0]), 'evidence': [e for e, _ in ri]}
        if lk:
            f, rx = scrubber(t, n.get('company'))
            p = f(p)
            p['baseline']['ticker'] = '[REDACTED]'
            p['baseline']['company'] = '[REDACTED]'
            p['anonymised'] = True
            left = rx.findall(json.dumps({k: v for k, v in p.items() if k != 'id'}, ensure_ascii=False))
            assert not left, (eid, left[:3])
        # an opaque id for every pack: the event id carries the ticker
        p['id'] = f'pack-{len(packs):03d}'
        ev['pack_id'] = p['id']
        packs.append(p)
    os.makedirs(f'{HERE}/data', exist_ok=True)
    json.dump(events, open(f'{HERE}/data/events.json', 'w'), indent=0, ensure_ascii=False)
    json.dump(items, open(f'{HERE}/data/items.json', 'w'), indent=0, ensure_ascii=False)
    json.dump(packs, open(f'{HERE}/data/packs.json', 'w'), ensure_ascii=False)
    from collections import Counter
    print('events', len(events), Counter(e['role'] for e in events), 'unique prints', len({e['event_key'] for e in events}),
          'anonymised', sum(bool(e['leak']) for e in events))
    print('items', len(items), Counter(i['kind'] for i in items))


if __name__ == '__main__':
    main()
