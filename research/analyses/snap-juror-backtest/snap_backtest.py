#!/usr/bin/env python3
"""SubQ Snap beside the four-model panel, on the full US backtest without the September
Opus 5.5 hunts (operator, 2026-10-14): does a non-Anthropic juror asked the judges'
question add anything to the panel?

Sample: exactly the US names `research/analyses/panel-mean-pct/panel_mean_pct.py` reads,
so Snap is measured on the same names and the same returns as the four judges.

- `backtest`: the blind four-model re-judge of 2026-08-31 to 2026-09-22 (Opus 5-era
  hunts; September Opus 5.5 out by the ledger's `sept_opus55` flag). Snap gets the same
  packs the judges got, from `research/analyses/rejudge-four-models/packs-*.json`,
  anonymised ones included as anonymised.
- `oktober`: the live E-P panels, packs from each run's `panel/packs.json`.

Three arms, one request each per name (Snap is deterministic for identical bytes):

- `v2` THE ARM UNDER TEST: `snap_juror.py` as committed, the judges' brief, hunter
  definition and lessons inlined, answered as abs_move_pct and p_up;
  snap_impact = (2 p_up/100 - 1) x E|move|.
- `v1`: the question of the first live test (commit ccef4c9d), a signed 24-bin move
  distribution, E[move]. Context only: did the new question change anything?
- `bare`: LEAKAGE CONTROL. The v2 questions with only ticker, company, event date and
  session, no evidence. Every name but the 10-12 ones was sealed BEFORE Snap's release
  (2026-10-12), so its training may hold the outcome. If `bare` predicts the move, the
  other two arms cannot be read. Anonymised names have no identity and are skipped.

Fixed before any call was made, in this order:

1. Snap's own skill: the within-day Spearman of snap_impact against the move (mean over
   days, within-day permutation p), and the return of Snap's own top 10/20/30/50/100%
   (percentile of |snap_impact| within the sample, traded on its sign), beside each
   judge and the four-judge mean on the same names.
2. Independence: Spearman between Snap's signed percentile and each judge's, beside the
   judges' correlations with each other.
3. Added value, THE ANSWER: the five-member mean (four judges + Snap) against the
   four-judge mean, top 10/20/30%, same rule as the live selection. Plus the panel's
   top 20% split by whether Snap agrees on the sign.
4. `bare` through tests 1, and `v2` split by leak flag and by pre/post release.

Returns: the strategy exit entered at 19:30 CET (`e1930`, the backtest README's lead)
and at the close (`e2200`). Gross, equal weight. Nothing here selects, sizes or trades.

  python3 research/analyses/snap-juror-backtest/snap_backtest.py [--arms v2,v1,bare]
                                                                  [--analyse-only]
The key is SUBQ_API_KEY and is never written down. Responses are cached in
`responses.jsonl` by request hash, so a rerun calls only what is missing.
"""
import argparse, bisect, glob, json, os, random, statistics as st, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'researcher_us' / 'scripts'))
sys.path.insert(0, str(REPO / 'research' / 'analyses' / 'panel-mean-pct'))
import snap_juror as sj            # noqa: E402
import panel_mean_pct as pm        # noqa: E402

REJ = REPO / 'research/analyses/rejudge-four-models'
CACHE = HERE / 'responses.jsonl'
MEMBERS = pm.MEMBERS
MOVES = ('e1930', 'e2200')
TOPS = (10, 20, 30, 50, 100)
V1_COMMIT = 'ccef4c9d'
BARE_BRIEF = ("Judge one US-listed company that reports quarterly earnings in the window "
              "below, from what you know about it. Answer the two questions as the core of "
              "an earnings hunter would: p_up, the probability the stock closes the window "
              "higher (0.5 is no view); abs_move_pct, how far it moves whatever the "
              "direction. Use nothing you may know about what happened after the event date.")


def sgn(x): return (x > 0) - (x < 0)


# ------------------------------------------------------------------------------ sample
def sample():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    mk = {}
    for v in json.load(open(REPO / 'dashboard/data/markets.json'))['markets'].values():
        for r in v['names']:
            mk[(r.get('run_date'), r['ticker'])] = r
    key = json.load(open(REJ / 'key.json'))
    kidx = {(k['day'], k['ticker']): k for k in key if k['region'] == 'us'}
    rpacks = {}
    for f in sorted(glob.glob(str(REJ / 'packs-*.json'))):
        for p in json.load(open(f)):
            rpacks[p['id']] = p
    out = []
    for ds, names in (('backtest', pm.load_backtest(led, mk).get('US', [])),
                      ('oktober', pm.load_october(led).get('US', []))):
        opacks, company = {}, {}
        for n in names:
            if ds == 'backtest':
                k = kidx[(n['date'], n['ticker'])]
                pack = rpacks.get(k.get('pid') or k['id'])
                comp = k.get('company')
            else:
                if n['date'] not in opacks:
                    f = REPO / f"research/{n['date'][:4]}/{n['date'][5:7]}/{n['date']}/edge-panel"
                    pp = f / 'panel' / 'packs.json'
                    opacks[n['date']] = ({p['baseline']['ticker']: p for p in json.load(open(pp))}
                                         if pp.exists() else {})
                    u = f / 'universe.json'
                    company[n['date']] = ({r.get('ticker'): r.get('company') or r.get('name')
                                           for r in json.load(open(u)).get('names', [])}
                                          if u.exists() else {})
                pack = opacks[n['date']].get(n['ticker'])
                comp = company[n['date']].get(n['ticker'])
            if pack is None or all(n['moves'][m] is None for m in MOVES):
                continue
            out.append({**n, 'ds': ds, 'pack': pack, 'company': comp,
                        'anon': str(pack.get('id', '')).startswith('anon/')})
    return out


# ----------------------------------------------------------------------------- requests
def v1_module():
    """The first-live-test script, from git, with its own bins (the v2 config dropped
    them)."""
    src = subprocess.run(['git', 'show', f'{V1_COMMIT}:researcher_us/scripts/snap_juror.py'],
                         cwd=REPO, capture_output=True, text=True, check=True).stdout
    path = HERE / '.v1_snap_juror.py'
    path.write_text(src)
    import importlib.util
    spec = importlib.util.spec_from_file_location('snap_juror_v1', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    path.unlink()
    c = dict(sj.cfg(), bin_edges_inner=[-20, -15, -12, -10, -8, -6, -5, -4, -3, -2, -1, 0, 1, 2,
                                        3, 4, 5, 6, 8, 10, 12, 15, 20], tail_values=[-25, 25])
    return m, c


def bodies(n, arm, ctx):
    c = sj.cfg()
    if arm == 'v2':
        return sj.body_of(n['pack'], c, sj.bins(c))
    if arm == 'v1':
        m, c1 = ctx['v1']
        return m.body_of(n['pack'], c1, m.bins(c1))
    if arm == 'bare':
        if n['anon']:
            return None
        b = n['pack']['baseline']
        return {'model': c['model'],
                'state': {'brief': BARE_BRIEF, 'window': sj.PREAMBLE,
                          'company': {'ticker': n['ticker'], 'name': n['company'],
                                      'event_date': b.get('event_date'),
                                      'session': b.get('session')}},
                'questions': sj.questions(sj.bins(c))}


def derive(arm, resp, ctx):
    if arm == 'v1':
        m, c1 = ctx['v1']
        return m.derive(resp, m.bins(c1))['snap_impact']
    return sj.derive(resp, sj.bins(sj.cfg()))['snap_impact']


def call_all(names, arms, ctx):
    cache = {}
    if CACHE.exists():
        for line in CACHE.open():
            r = json.loads(line)
            cache[(r['arm'], r['request_sha256'])] = r
    key = os.environ.get('SUBQ_API_KEY')
    todo = []
    for n in names:
        for arm in arms:
            body = bodies(n, arm, ctx)
            if body is None:
                continue
            h = sj.sha(body)
            n.setdefault('req', {})[arm] = h
            if (arm, h) not in cache:
                todo.append((n, arm, body, h))
    print(f"{len(todo)} calls to make, {len(cache)} cached")
    if todo and not key:
        sys.exit('SUBQ_API_KEY is not set; nothing called')
    c = sj.cfg()

    def one(t):
        n, arm, body, h = t
        resp, status, why, tries = sj.post(body, c, key)
        return {'arm': arm, 'request_sha256': h, 'id': n['pack'].get('id'), 'date': n['date'],
                'ticker': n['ticker'], 'status': status, 'reason': why, 'attempts': tries,
                'called_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'docs_sha256': sj.docs_sha(n['pack']) if arm == 'v2' else None,
                'script_version': sj.SCRIPT_VERSION if arm != 'v1' else 'snap.v1',
                'response': resp}

    with CACHE.open('a') as fh, ThreadPoolExecutor(4) as ex:
        for i, r in enumerate(ex.map(one, todo)):
            fh.write(json.dumps(r, ensure_ascii=False) + '\n'); fh.flush()
            cache[(r['arm'], r['request_sha256'])] = r
            if r['status'] != 'ok':
                print('  ', r['arm'], r['id'], r['status'], r['reason'])
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{len(todo)}")
    return cache


# ------------------------------------------------------------------------------- stats
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spear(a, b):
    if len(a) < 3: return None
    ra, rb = rank(a), rank(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return num / den if den else None


def within_day(rows, f, mk, n_perm=2000, seed=20261014):
    """Mean of per-day Spearman (days with >= 3 names), and a permutation p that shuffles
    moves within each day."""
    days = {}
    for r in rows:
        if r['moves'][mk] is not None and f(r) is not None:
            days.setdefault(r['date'], []).append((f(r), r['moves'][mk]))
    days = [d for d in days.values() if len(d) >= 3]
    if not days: return None

    def stat(ds):
        v = [spear([x for x, _ in d], [y for _, y in d]) for d in ds]
        v = [x for x in v if x is not None]
        return st.mean(v) if v else 0.0
    obs = stat(days); rnd = random.Random(seed); hits = 0
    for _ in range(n_perm):
        sh = []
        for d in days:
            ys = [y for _, y in d]; rnd.shuffle(ys); sh.append([(x, y) for (x, _), y in zip(d, ys)])
        hits += stat(sh) >= obs
    return {'rho': round(obs, 3), 'p': round((hits + 1) / (n_perm + 1), 4), 'days': len(days),
            'n': sum(len(d) for d in days)}


def pctl(ref, v):
    if v is None or v == 0: return 0.0
    return sgn(v) * 100.0 * bisect.bisect_left(ref, abs(v)) / len(ref)


def book(rows, f, top, mk):
    v = [r for r in rows if r['moves'][mk] is not None and f(r) and abs(f(r)) >= 100 - top]
    if not v: return None
    s = [sgn(f(r)) * r['moves'][mk] for r in v]
    return {'top': top, 'n': len(s), 'mean': round(st.mean(s), 2),
            'se': round(st.stdev(s) / len(s) ** .5, 2) if len(s) > 1 else None,
            'hit': round(sum(y > 0 for y in s) / len(s), 3)}


def analyse(names, cache, arms, ctx):
    for n in names:
        n['snap'] = {}
        for arm in arms:
            h = (n.get('req') or {}).get(arm)
            r = cache.get((arm, h)) if h else None
            if r and r['status'] == 'ok':
                try: n['snap'][arm] = derive(arm, r['response'], ctx)
                except ValueError: pass
    doc = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
           'script_version_v2': sj.SCRIPT_VERSION,
           'models_returned': sorted({(r.get('response') or {}).get('model') for r in cache.values()
                                      if r.get('response')} - {None}),
           'samples': {}}
    for ds in ('backtest', 'oktober', 'pooled'):
        rows = [n for n in names if ds == 'pooled' or n['ds'] == ds]
        # percentiles within the sample, from every name judged there (no outcome used)
        refs = {m: sorted(abs(r['impact_sum'][m]) for r in rows) for m in MEMBERS}
        for arm in arms:
            refs[arm] = sorted(abs(r['snap'][arm]) for r in rows if arm in r['snap'])
        for r in rows:
            r['p'] = {m: pctl(refs[m], r['impact_sum'][m]) for m in MEMBERS}
            for arm in arms:
                r['p'][arm] = pctl(refs[arm], r['snap'].get(arm)) if arm in r['snap'] else None
            r['p']['panel4'] = st.mean(r['p'][m] for m in MEMBERS)
            if r['p'].get('v2') is not None:
                r['p']['panel5'] = st.mean([r['p'][m] for m in MEMBERS] + [r['p']['v2']])
        D = {'n': len(rows), 'days': len({r['date'] for r in rows}),
             'n_v2': sum('v2' in r['snap'] for r in rows), 'leak': sum(1 for r in rows if r['leak']),
             'short_all': {mk: round(st.mean(-r['moves'][mk] for r in rows if r['moves'][mk] is not None), 2)
                           for mk in MOVES}}
        cols = list(MEMBERS) + ['panel4'] + [a for a in arms] + (['panel5'] if 'v2' in arms else [])
        D['skill'] = {}
        for col in cols:
            if col in MEMBERS:
                f_raw = lambda r, c=col: r['impact_sum'][c]
            elif col in arms:
                f_raw = lambda r, c=col: r['snap'].get(c)
            else:
                f_raw = lambda r, c=col: r['p'].get(c)
            f_p = lambda r, c=col: r['p'].get(c)
            D['skill'][col] = {mk: {'within_day': within_day(rows, f_raw, mk),
                                    'tops': [b for t in TOPS if (b := book(rows, f_p, t, mk))]}
                               for mk in MOVES}
        # independence: Spearman of signed percentiles
        sub = [r for r in rows if r['p'].get('v2') is not None]
        D['corr'] = {f'{a}~{b}': round(spear([r['p'][a] for r in sub], [r['p'][b] for r in sub]), 3)
                     for i, a in enumerate(list(MEMBERS) + ['v2'])
                     for b in (list(MEMBERS) + ['v2'])[i + 1:]} if len(sub) > 2 else {}
        D['corr']['panel4~v2'] = (round(spear([r['p']['panel4'] for r in sub], [r['p']['v2'] for r in sub]), 3)
                                  if len(sub) > 2 else None)
        # inside the panel's top 20%: does Snap agree on the sign?
        D['agree_split'] = {}
        for mk in MOVES:
            top = [r for r in sub if r['moves'][mk] is not None and abs(r['p']['panel4']) >= 80]
            g = {}
            for lab, sel in (('snap_agrees', lambda r: sgn(r['p']['v2']) == sgn(r['p']['panel4'])),
                             ('snap_disagrees', lambda r: sgn(r['p']['v2']) != sgn(r['p']['panel4']))):
                s = [sgn(r['p']['panel4']) * r['moves'][mk] for r in top if sel(r)]
                g[lab] = {'n': len(s), 'mean': round(st.mean(s), 2) if s else None,
                          'hit': round(sum(y > 0 for y in s) / len(s), 3) if s else None}
            D['agree_split'][mk] = g
        # v2 split by leak flag and release
        D['v2_splits'] = {}
        for lab, sel in (('anonymised', lambda r: r['anon']), ('named', lambda r: not r['anon']),
                         ('pre_release', lambda r: r['date'] < '2026-10-12'),
                         ('post_release', lambda r: r['date'] >= '2026-10-12')):
            g = [r for r in rows if sel(r)]
            D['v2_splits'][lab] = {'n': len(g), **{mk: within_day(g, lambda r: r['snap'].get('v2'), mk)
                                                   for mk in MOVES}}
        doc['samples'][ds] = D
    doc['rows'] = [{'ds': r['ds'], 'date': r['date'], 'ticker': r['ticker'], 'anon': r['anon'],
                    'leak': r['leak'], 'moves': r['moves'], 'impact_sum': r['impact_sum'],
                    'snap': r['snap']} for r in names]
    return doc


def report(doc, arms):
    for ds, D in doc['samples'].items():
        print(f"\n=== {ds}: {D['n']} names, {D['days']} days, v2 answered {D['n_v2']}, "
              f"short all {D['short_all']}")
        for mk in MOVES:
            print(f"  [{mk}]  {'':8s} {'rho (p)':>16s}   " + '   '.join(f'top{t:<3d}' for t in TOPS))
            for col, S in D['skill'].items():
                w = S[mk]['within_day']
                tops = {b['top']: b for b in S[mk]['tops']}
                cells = [f"{tops[t]['n']:3d} {tops[t]['mean']:+5.1f}" if t in tops else '   -     ' for t in TOPS]
                ws = f"{w['rho']:+.3f} ({w['p']:.3f})" if w else '-'
                print(f"   {col:9s} {ws:>16s}   " + '  '.join(cells))
        print('  corr:', D['corr'])
        print('  panel top20 by Snap agreement:', D['agree_split'])
        print('  v2 splits:', {k: (v['n'], (v['e1930'] or {}).get('rho'), (v['e1930'] or {}).get('p'))
                               for k, v in D['v2_splits'].items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arms', default='v2,v1,bare')
    ap.add_argument('--analyse-only', action='store_true')
    a = ap.parse_args()
    arms = a.arms.split(',')
    ctx = {'v1': v1_module()} if 'v1' in arms else {}
    names = sample()
    print(f"sample: {len(names)} names ({sum(n['ds'] == 'backtest' for n in names)} backtest, "
          f"{sum(n['ds'] == 'oktober' for n in names)} oktober)")
    if a.analyse_only:
        for n in names:
            for arm in arms:
                b = bodies(n, arm, ctx)
                if b is not None: n.setdefault('req', {})[arm] = sj.sha(b)
        cache = {}
        for line in CACHE.open():
            r = json.loads(line); cache[(r['arm'], r['request_sha256'])] = r
    else:
        cache = call_all(names, arms, ctx)
    doc = analyse(names, cache, arms, ctx)
    toks = sum(int(((r.get('response') or {}).get('usage') or {}).get('input_tokens') or 0)
               for r in cache.values())
    doc['input_tokens_cached'] = toks
    doc['cost_usd_cached'] = round(toks * float(sj.cfg()['usd_per_m_input_tokens']) / 1e6, 4)
    json.dump(doc, open(HERE / 'results.json', 'w'), indent=1)
    report(doc, arms)
    print(f"\nmodels returned: {doc['models_returned']}; {toks} input tokens, ${doc['cost_usd_cached']}")


if __name__ == '__main__':
    main()
