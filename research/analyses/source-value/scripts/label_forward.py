#!/usr/bin/env python3
"""Label the items of every US hunt resolved AFTER the v1 cut-off with the frozen codebook v1.

  python3 scripts/label_forward.py [--dry]

Finds resolved, hunted US names in dashboard/data/ledger.json that are not in data/events.json
(stage E `edge/`; stage E-P `edge-panel/` searcher hunts are kept as their own stratum A2),
builds blinded packs exactly like stratum A (../source-types/build.py's item order, scrubber
and opaque ids), and labels them twice with codebook/labeler-v1.md through the same isolated
call. Writes data/forward/{events,items,packs}.json and labels/forward/run{0,1}/. Never edits
v1's data or labels. Then run scripts/update_registry.py.
"""
import glob, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
R = os.path.abspath(os.path.join(SV, '..', '..', '..'))
sys.path.insert(0, os.path.join(SV, '..', 'source-types'))
import build as STB  # noqa: E402  (source-types/build.py: raw_items, scrubber, leaked, trim, ctx)

SVB = None


def main():
    global SVB
    import importlib.util
    spec = importlib.util.spec_from_file_location('svbuild', f'{HERE}/build.py')
    SVB = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(SVB)
    have = {e['id'] for e in json.load(open(f'{SV}/data/events.json'))}
    ledger = json.load(open(f'{R}/dashboard/data/ledger.json'))['names']
    ctxt = SVB.context_text()
    events, items, packs = [], [], []
    for n in ledger:
        if n.get('pending') or n.get('mv_strategy') is None:
            continue
        d, t = n['run'].rstrip('/'), n['ticker']
        eid = f"us/{n['run_date']}/{t}"
        if eid in have:
            continue
        stratum = 'A2' if d.endswith('edge-panel') else 'A'
        hs = sorted(glob.glob(f'{R}/{d}/hunts/{t}.json') + glob.glob(f'{R}/{d}/hunts/{t}-*.json'))
        bpath = f'{R}/{d}/baselines/{t}.json'
        if not hs or not os.path.exists(bpath):
            continue
        b = json.load(open(bpath))
        opt, hist = b.get('options') or {}, b.get('history') or {}
        em = b.get('expected_move') if isinstance(b.get('expected_move'), dict) else {}
        implied = STB.num(opt.get('event_implied_move_pct')) or STB.num(em.get('pct'))
        priced = implied or STB.num(b.get('expected_move_pct')) or STB.num(hist.get('median_abs_move_pct')) or 5.0
        pid = f'F-pack-{len(packs):03d}'
        ri = STB.raw_items(hs)
        lk = STB.leaked(t, n.get('company'), ctxt)
        mc = n.get('market_cap_usd')
        ev = {'id': eid, 'stratum': stratum, 'forward': True, 'market': 'us', 'event_key': f"{t}/{n.get('event_date')}", 'duplicate_hunt': bool(n.get('duplicate_event')),
              'day': n['run_date'], 'perm_day': f'F/{n["run_date"]}', 'ticker': t, 'company': n.get('company'), 'sector': n.get('sector'),
              'session': n.get('session'), 'move': n['mv_strategy'], 'move_strategy': n['mv_strategy'], 'move_open': n.get('mv_open'),
              'move_close': n.get('mv_close'), 'dollar_vol': n.get('dollar_vol'), 'market_cap': mc, 'cap_band': SVB.cap_band(mc),
              'turnover_band': SVB.turnover_band(n.get('dollar_vol')), 'option_anchor': bool(implied), 'implied_move': implied,
              'priced_move': max(priced, 1.0), 'runup_20d': n.get('runup_20d'), 'live_impact': n.get('impact_sum'), 'pack_id': pid,
              'leak': lk, 'rejudge': {}}
        events.append(ev)
        for e, raw in ri:
            src = e.get('source') or ''
            items.append({'event': eid, 'event_key': ev['event_key'], 'stratum': stratum, 'pack_id': pid, 'i': e['i'], 'kind': e['kind'],
                          'text': e.get('text'), 'source': src, 'domain': SVB.domain(src) if src.startswith('http') else None,
                          'live_size': STB.num(raw.get('expected_impact_pct')) if isinstance(raw, dict) else None})
        p = {'id': pid, 'baseline': STB.trim({k: v for k, v in b.items() if not k.startswith('event_occurred')}),
             'first_hunter_context': STB.ctx(hs[0]), 'evidence': [e for e, _ in ri]}
        if lk:
            f, rx = STB.scrubber(t, n.get('company'))
            p = f(p)
            p['baseline']['ticker'] = p['baseline']['company'] = '[REDACTED]'
            p['anonymised'] = True
            p['id'] = pid
        packs.append(p)
    os.makedirs(f'{SV}/data/forward', exist_ok=True)
    for k, v in (('events', events), ('items', items), ('packs', packs)):
        json.dump(v, open(f'{SV}/data/forward/{k}.json', 'w'), ensure_ascii=False)
    print('forward prints', len(events), 'items', len(items))
    if packs and '--dry' not in sys.argv:
        subprocess.run([sys.executable, f'{HERE}/label.py', '--forward', f'{SV}/data/forward/packs.json', '--out-dir', f'{SV}/labels/forward', '--runs', '2'], check=True)


if __name__ == '__main__':
    main()
