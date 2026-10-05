#!/usr/bin/env python3
"""Phase 0: the sample, one row per print (event) and per evidence item, per stratum.

  python3 scripts/build.py

Writes data/events.json, data/items.json and data/packs-<stratum>.json.

Strata (reported separately, pooled only where a test says they agree):

  A   US edge hunts (stage E). Taken from ../source-types/data, which build.py there made
      from the dashboard ledger; the ledger on this branch (generated 2026-10-05T06:47Z)
      resolves exactly those 163 hunts / 158 prints, so a rebuild changes nothing. The
      items, their order and the anonymised packs are identical, so the earlier labels
      and the four-model re-judges still join on (pack id, i).
  A2  stage E-P searcher hunts: none resolved at the cut-off. Recorded, empty.
  B   retired stage-2 dossiers with a scored outcome in archive/pipeline/PREDICTIONS.csv.
      Items are extracted MECHANICALLY (no model): every bullet or table row in the
      evidence sections that carries a numbered citation becomes one item, with the
      cited URLs resolved from the dossier's own source list. Sections 1 (anchors),
      9-10 (bull/bear, flip), 11 (gaps) and 12 (sources) are not evidence items.
  C   Europe, Japan, Australia: every resolved row with a realised move, an event that
      occurred and a hunt on disk. Same item extraction as A (findings, outside-window,
      rejected, searched-and-found-nothing). Priced move = the baseline's median past
      reaction (no market here has an option anchor).

No outcome enters a pack. Packs whose company or ticker appears in the context any
model might be shown (CLAUDE.md, the hunter core, every hunter definition, every
LESSONS file) are anonymised with the source-types scrubber; every pack has an opaque id.
"""
import csv, glob, json, os, re, sys
from collections import Counter
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
R = os.path.abspath(os.path.join(SV, '..', '..', '..'))
ST = os.path.join(SV, '..', 'source-types')
sys.path.insert(0, ST)
import build as STB  # noqa: E402  (source-types/build.py: raw_items, scrubber, trim, ...)

CUTOFF = '2026-10-05T06:47Z (dashboard ledger on this branch); ex-US resolved files on disk at build time'


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


def context_text():
    files = ['CLAUDE.md', 'config/hunter-core.md'] + sorted(glob.glob(f'{R}/.claude/agents/unpriced-hunter*.md')) + \
        sorted(glob.glob(f'{R}/researcher_*/LESSONS.md'))
    return '\n'.join(open(os.path.join(R, p)).read() for p in files if os.path.exists(os.path.join(R, p)))


def turnover_band(tv):
    if tv is None:
        return 'unknown'
    return 'lt1m' if tv < 1e6 else ('1to25m' if tv < 25e6 else 'gt25m')


def cap_band(mc):
    if mc is None:
        return 'unknown'
    return 'micro' if mc < 3e8 else 'small' if mc < 2e9 else 'mid' if mc < 1e10 else 'large'


# ------------------------------------------------------------------ stratum A
def stratum_a():
    E = json.load(open(f'{ST}/data/events.json'))
    I = json.load(open(f'{ST}/data/items.json'))
    P = json.load(open(f'{ST}/data/packs.json'))
    ledger = {(n['run_date'], n['ticker']): n for n in json.load(open(f'{R}/dashboard/data/ledger.json'))['names']}
    twin_day = {e['event_key']: e['day'] for e in E if not e['duplicate_hunt']}
    events, items, packs = [], [], []
    for e in E:
        n = ledger.get((e['day'], e['ticker']), {})
        ev = dict(e)
        ev.update({'stratum': 'A', 'market': 'us', 'pack_id': 'A-' + e['pack_id'], 'perm_day': 'A/' + twin_day.get(e['event_key'], e['day']),
                   'cap_band': cap_band(e['market_cap']), 'turnover_band': turnover_band(e['dollar_vol']),
                   'option_anchor': bool(e['implied_move']), 'old_pack_id': e['pack_id'],
                   'move_strategy': e['move'], 'runup_10d': n.get('runup_10d'), 'conviction_live': n.get('conviction'),
                   'above_floor': n.get('above_floor'), 'traded': n.get('traded'), 'sept_opus55': n.get('sept_opus55'),
                   'easy_to_borrow': n.get('easy_to_borrow')})
        events.append(ev)
    for it in I:
        x = dict(it)
        x['stratum'] = 'A'
        items.append(x)
    for p in P:
        q = dict(p)
        q['id'] = 'A-' + p['id']
        packs.append(q)
    pid = {e['id']: e['pack_id'] for e in events}
    for x in items:
        x['pack_id'] = pid[x['event']]
    return events, items, packs


# ------------------------------------------------------------------ stratum C
def resolved_rows():
    out = []
    for f in sorted(glob.glob(f'{R}/research/2026/*/*/*/*-resolved.json')):
        mk = f.split('/')[-2]
        if mk not in ('europe', 'japan', 'australia'):
            continue
        j = json.load(open(f))
        for r in j['rows']:
            mv = r.get('realised_move_pct') if 'realised_move_pct' in r else r.get('move_pct')
            if r.get('event_occurred') is False or r.get('move_pending') or mv is None or r.get('rankable') is False:
                continue
            out.append((mk, j, r, num(mv), f))
    return out


def stratum_c(ctxt, start):
    events, items, packs = [], [], []
    for mk, j, r, mv, f in resolved_rows():
        run = (j.get('run') or os.path.dirname(f)).rstrip('/')
        run = run if run.startswith('/') else f'{R}/{run}'
        t = r['ticker']
        hs = sorted(glob.glob(f'{run}/hunts/{t}.json') + glob.glob(f'{run}/hunts/{t}-*.json'))
        bpath = f'{run}/baselines/{t}.json'
        if not hs or not os.path.exists(bpath):
            continue
        b = json.load(open(bpath))
        hist, tape = b.get('history') or {}, b.get('tape') or {}
        em = b.get('expected_move') if isinstance(b.get('expected_move'), dict) else {}
        hmed = num(hist.get('median_abs_move_pct'))
        priced = hmed or num(em.get('pct')) or 5.0
        tv = num(tape.get('median_turnover_usd_20d')) or num(r.get('median_turnover_usd_20d'))
        if tv is None and tape.get('median_turnover_jpy_20d'):
            tv = num(tape['median_turnover_jpy_20d']) / 150.0  # approximate JPY->USD, band only
        day = os.path.basename(os.path.dirname(run))
        eid = f'{mk}/{day}/{t}'
        if any(e['id'] == eid for e in events):
            continue
        ri = STB.raw_items(hs)
        lk = STB.leaked(t, b.get('company') or r.get('company'), ctxt)
        ev = {'id': eid, 'stratum': 'C', 'market': mk, 'submarket': b.get('submarket') or r.get('submarket') or mk,
              'event_key': f"{mk}/{t}/{b.get('event_date')}", 'duplicate_hunt': False, 'role': 'exus', 'day': day,
              'perm_day': f'C/{mk}/{day}', 'ticker': t, 'company': b.get('company') or r.get('company'),
              'sector': b.get('sector'), 'industry': b.get('industry'), 'session': b.get('session'),
              'event_date': b.get('event_date'), 'move': mv, 'move_strategy': mv, 'move_open': None, 'move_close': mv,
              'dollar_vol': tv, 'market_cap': None, 'cap_band': 'unknown', 'turnover_band': turnover_band(tv),
              'option_anchor': False, 'vol20': num(tape.get('realised_vol_20d_pct')),
              'runup_5d': num(tape.get('run_up_5d_pct')), 'runup_20d': num(tape.get('run_up_20d_pct')),
              'priced_lean_pct': num(b.get('priced_lean_pct')), 'implied_move': None, 'priced_move': max(priced, 1.0),
              'hist_median_move': hmed, 'history_basis': hist.get('basis'), 'live_impact': num(r.get('impact_sum')),
              'n_hunts': len(hs), 'leak': lk, 'rejudge': {}, 'resolved_file': os.path.relpath(f, R)}
        pid = f'C-pack-{start + len(packs):03d}'
        ev['pack_id'] = pid
        events.append(ev)
        for e, raw in ri:
            src = e.get('source') or ''
            items.append({'event': eid, 'event_key': ev['event_key'], 'stratum': 'C', 'role': 'exus', 'pack_id': pid, 'i': e['i'],
                          'kind': e['kind'], 'hunt': e['hunt'], 'text': e.get('text'), 'source': src, 'domain': domain(src) if src.startswith('http') else None,
                          'source_date': e.get('source_date'), 'lands_on': e.get('lands_on'), 'resolves_by': e.get('resolves_by'),
                          'live_size': num(raw.get('expected_impact_pct')) if isinstance(raw, dict) else None,
                          'text_len': len(e.get('text') or '')})
        b = {k: v for k, v in b.items() if not k.startswith('event_occurred')}  # amended after the outcome
        p = {'id': pid, 'baseline': STB.trim(b), 'first_hunter_context': STB.ctx(hs[0]), 'evidence': [e for e, _ in ri]}
        if lk:
            fsc, rx = STB.scrubber(t, ev['company'])
            p = fsc(p)
            p['baseline']['ticker'] = '[REDACTED]'
            p['baseline']['company'] = '[REDACTED]'
            p['anonymised'] = True
            p['id'] = pid
        packs.append(p)
    return events, items, packs


# ------------------------------------------------------------------ stratum B
CITE = re.compile(r'\[(\d{1,3})\]')
REF = re.compile(r'^\s*(\d{1,3})\.\s+(.*)$')
SKIP_SECTIONS = re.compile(r'^(1\.|9\.|10\.|11\.|12\.)|sources|coverage gaps|bull case|what would flip|event & anchors', re.I)


def dossier_items(md):
    lines = md.split('\n')
    refs, in_src = {}, False
    for ln in lines:
        if re.match(r'^##\s+(\d+\.\s+)?Sources', ln, re.I):
            in_src = True
            continue
        if in_src and ln.startswith('## '):
            in_src = False
        if in_src:
            m = REF.match(ln)
            if m:
                refs[int(m.group(1))] = (m.group(2), STB.URLS.findall(m.group(2)))
    out, sec, sub = [], None, None
    for ln in lines:
        if ln.startswith('## '):
            sec, sub = ln[3:].strip(), None
            continue
        if ln.startswith('### '):
            sub = ln[4:].strip()
            continue
        if sec is None or SKIP_SECTIONS.search(sec):
            continue
        s = ln.strip()
        if not s or set(s) <= set('|-: '):
            continue
        if not (s.startswith(('-', '*', '|')) or re.match(r'^\d+\.\s', s)):
            continue
        cites = [int(c) for c in CITE.findall(s)]
        if not cites:
            continue
        urls = []
        for c in cites:
            urls += refs.get(c, ('', []))[1]
        out.append({'section': sec, 'subsection': sub, 'text': s[:700], 'cites': cites,
                    'source': urls[0] if urls else None, 'urls': urls[:6],
                    'source_titles': [refs.get(c, ('', []))[0][:160] for c in cites[:4]]})
    return out


def stratum_b(ctxt):
    rows = list(csv.DictReader(open(f'{R}/archive/pipeline/PREDICTIONS.csv')))
    events, items, packs = [], [], []
    for x in rows:
        if not x.get('actual_move'):
            continue
        t, rd = x['ticker'], x['run_date']
        g = glob.glob(f'{R}/archive/pipeline/2026/*/{rd}/02-dossiers/{t}.md')
        if not g:
            continue
        md = open(g[0]).read()
        js = g[0][:-3] + '.json'
        dj = json.load(open(js)) if os.path.exists(js) else {}
        its = dossier_items(md)
        if not its:
            continue
        implied = num(x.get('event_implied_move')) or num(dj.get('event_implied_move_pct'))
        hmed = num(dj.get('historical_move_median_abs'))
        priced = implied or hmed or 5.0
        ekey = f"{t}/{x['event_date']}"
        dup = any(e['event_key'] == ekey for e in events)
        eid = f'dossier/{rd}/{t}'
        pid = f'B-pack-{len(packs):03d}'
        lk = STB.leaked(t, x.get('company'), ctxt)
        mc = num(dj.get('market_cap_usd'))
        ev = {'id': eid, 'stratum': 'B', 'market': 'us', 'event_key': ekey, 'duplicate_hunt': dup, 'role': 'dossier', 'day': rd,
              'perm_day': f'B/{x["event_date"]}', 'ticker': t, 'company': x.get('company'), 'sector': dj.get('sector'),
              'session': x.get('session'), 'event_date': x['event_date'], 'move': num(x['actual_move']),
              'move_strategy': None, 'move_close': num(x['actual_move']), 'market_cap': mc, 'cap_band': cap_band(mc),
              'dollar_vol': None, 'turnover_band': 'unknown', 'option_anchor': bool(implied), 'implied_move': implied,
              'priced_move': max(priced, 1.0), 'hist_median_move': hmed, 'leak': lk, 'pack_id': pid,
              'live_impact': num(x.get('preliminary_direction_score')), 'call': x.get('call'),
              'source_file': os.path.relpath(g[0], R), 'rejudge': {}}
        events.append(ev)
        ev_items = []
        for k, it in enumerate(its):
            ev_items.append({'i': k, 'kind': 'dossier_claim', 'section': it['section'] + (f' / {it["subsection"]}' if it['subsection'] else ''),
                             'text': it['text'], 'source': it['source'], 'cited_titles': it['source_titles']})
            items.append({'event': eid, 'event_key': ekey, 'stratum': 'B', 'role': 'dossier', 'pack_id': pid, 'i': k, 'kind': 'dossier_claim',
                          'section': it['section'], 'text': it['text'], 'source': it['source'],
                          'domain': domain(it['source']) if it['source'] else None, 'domains_all': sorted({domain(u) for u in it['urls'] if domain(u)}),
                          'n_urls': len(it['urls']), 'text_len': len(it['text'])})
        base = {k: dj.get(k) for k in ('event_date', 'session', 'spot', 'spot_as_of', 'market_cap_usd', 'event_implied_move_pct',
                                       'historical_moves_pct', 'historical_move_median_abs', 'key_metric')}
        base.update({'ticker': t, 'company': x.get('company'), 'sector': dj.get('sector')})
        p = {'id': pid, 'baseline': base, 'first_hunter_context': {'note': 'a stage-2 research dossier; items are its cited claims'},
             'evidence': ev_items}
        if lk:
            fsc, rx = STB.scrubber(t, x.get('company'))
            p = fsc(p)
            p['baseline']['ticker'] = '[REDACTED]'
            p['baseline']['company'] = '[REDACTED]'
            p['anonymised'] = True
            p['id'] = pid
        packs.append(p)
    return events, items, packs


def main():
    ctxt = context_text()
    EA, IA, PA = stratum_a()
    EB, IB, PB = stratum_b(ctxt)
    EC, IC, PC = stratum_c(ctxt, 0)
    os.makedirs(f'{SV}/data', exist_ok=True)
    events = EA + EB + EC
    items = IA + IB + IC
    json.dump(events, open(f'{SV}/data/events.json', 'w'), indent=0, ensure_ascii=False)
    json.dump(items, open(f'{SV}/data/items.json', 'w'), indent=0, ensure_ascii=False)
    for s, P in (('A', PA), ('B', PB), ('C', PC)):
        json.dump(P, open(f'{SV}/data/packs-{s}.json', 'w'), ensure_ascii=False)
    summ = {'cutoff': CUTOFF, 'A2_stage_EP_searcher': 'no resolved E-P hunt at the cut-off (first E-P fire 2026-10-02, no hunts on disk)',
            'D_sealed_corpus': 'excluded (INCLUDE_CORPUS not set)'}
    for s, E, I in (('A', EA, IA), ('B', EB, IB), ('C', EC, IC)):
        summ[s] = {'events': len(E), 'prints': len({e['event_key'] for e in E}), 'items': len(I),
                   'kinds': Counter(i['kind'] for i in I), 'cap_band': Counter(e['cap_band'] for e in E if not e['duplicate_hunt']),
                   'turnover_band': Counter(e['turnover_band'] for e in E if not e['duplicate_hunt']),
                   'option_anchor': Counter(e['option_anchor'] for e in E if not e['duplicate_hunt']),
                   'anonymised': sum(bool(e['leak']) for e in E), 'markets': Counter(e['market'] for e in E),
                   'days': len({e['perm_day'] for e in E})}
    json.dump(summ, open(f'{SV}/data/sample.json', 'w'), indent=1, default=dict)
    print(json.dumps(summ, indent=1, default=dict))


if __name__ == '__main__':
    main()
