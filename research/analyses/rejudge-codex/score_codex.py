#!/usr/bin/env python3
"""Two OpenAI models (GPT-6 Astra and GPT-6, label sol61) beside the four Claude judges,
on the same blind packs: do they add anything to the Claude panel? (operator, 2026-10-14)

Sample: exactly the US names `../panel-mean-pct/panel_mean_pct.py` reads, so the Codex
judges are measured on the same names and the same returns as the four Claude judges and
as SubQ Snap in `../snap-juror-backtest/`.

- `backtest`: the blind four-model re-judge of 2026-08-31 to 2026-09-22 (Opus 5-era
  hunts; September Opus 5.5 out by the ledger's `sept_opus55` flag). Codex got the same
  packs (input/A-backtest), anonymised ones as anonymised.
- `oktober`: the live E-P panels 2026-10-05..10-13; Codex got each run's own packs
  (input/B-oktober). The Claude scores are the live judges' own.

The tests are the Snap analysis's, in the same order, so the two can be read side by side:

1. Each judge's own skill: within-day Spearman of impact_sum against the move (mean over
   days with >= 3 names, within-day permutation p) and the return of its own top
   10/20/30/50/100% (percentile of |impact_sum| within the sample, traded on its sign).
2. Independence: Spearman between signed percentiles, every pair.
3. Added value, THE ANSWER: the panel with a GPT member (4 + astra, 4 + sol61, 4 + both)
   against the four-judge mean, top 10/20/30%, and at an equal number of names (the k
   largest |mean|). Plus the panel's top 20% split by whether the GPT pair agrees on sign.
4. Incremental information: the part of the GPT pair's signed percentile that the Claude
   mean does not explain (residual of a least-squares fit on the Claude mean, per sample),
   ranked within the day against the move. If the GPT judges carry information the panel
   lacks, this is where it shows.
5. Leakage: within-day rho split anonymised / named. Codex reports no training cutoff
   after the events (sol61 says 2024-06, Astra unknown), but nothing enforces it.

Returns: the strategy exit entered at 19:30 CET (`e1930`) and at the close (`e2200`).
Gross, equal weight. Nothing here selects, sizes or trades.

  python3 research/analyses/rejudge-codex/score_codex.py
"""
import bisect, glob, json, random, statistics as st, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'research' / 'analyses' / 'panel-mean-pct'))
import panel_mean_pct as pm  # noqa: E402

REJ = REPO / 'research/analyses/rejudge-four-models'
CLAUDE = pm.MEMBERS
GPT = ('astra', 'sol61')
MOVES = ('e1930', 'e2200')
TOPS = (10, 20, 30, 50, 100)
KS = (10, 15, 20, 30)
PANELS = {'panel4': CLAUDE, 'gpt2': GPT, 'panel4+astra': CLAUDE + ('astra',),
          'panel4+sol61': CLAUDE + ('sol61',), 'panel6': CLAUDE + GPT}


def sgn(x): return (x > 0) - (x < 0)


# ------------------------------------------------------------------------------ sample
def codex_scores():
    """(model, pack id) -> impact_sum, for both parts."""
    out = {}
    for m in GPT:
        for f in glob.glob(str(HERE / 'out' / m / '*-*.json')):
            if Path(f).name == 'meta.json':
                continue
            for o in json.load(open(f)):
                out[(m, o['id'])] = float(o.get('impact_sum') or 0)
    return out


def sample():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    mk = {}
    for v in json.load(open(REPO / 'dashboard/data/markets.json'))['markets'].values():
        for r in v['names']:
            mk[(r.get('run_date'), r['ticker'])] = r
    kidx = {(k['day'], k['ticker']): k for k in json.load(open(REJ / 'key.json')) if k['region'] == 'us'}
    cx = codex_scores()
    out, missing = [], []
    for ds, names in (('backtest', pm.load_backtest(led, mk).get('US', [])),
                      ('oktober', pm.load_october(led).get('US', []))):
        for n in names:
            pid = ((lambda k: k.get('pid') or k['id'])(kidx[(n['date'], n['ticker'])]) if ds == 'backtest'
                   else f"us/{n['date']}/{n['ticker']}")
            if all(n['moves'][m] is None for m in MOVES):
                continue
            g = {m: cx.get((m, pid)) for m in GPT}
            if any(v is None for v in g.values()):
                missing.append((ds, pid))
                continue
            out.append({**n, 'ds': ds, 'pid': pid, 'anon': pid.startswith('anon/'),
                        'score': {**n['impact_sum'], **g}})
    return out, missing


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


def stats(s):
    return {'n': len(s), 'mean': round(st.mean(s), 2),
            'se': round(st.stdev(s) / len(s) ** .5, 2) if len(s) > 1 else None,
            'hit': round(sum(y > 0 for y in s) / len(s), 3)}


def book(rows, f, top, mk):
    v = [r for r in rows if r['moves'][mk] is not None and f(r) and abs(f(r)) >= 100 - top]
    return {'top': top, **stats([sgn(f(r)) * r['moves'][mk] for r in v])} if v else None


def book_k(rows, f, k, mk):
    v = sorted((r for r in rows if r['moves'][mk] is not None and f(r)), key=lambda r: -abs(f(r)))[:k]
    return {'k': k, **stats([sgn(f(r)) * r['moves'][mk] for r in v])} if len(v) == k else None


# ----------------------------------------------------------------------------- analysis
def analyse(names):
    doc = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'samples': {}}
    judges = CLAUDE + GPT
    for ds in ('backtest', 'oktober', 'pooled'):
        rows = [n for n in names if ds == 'pooled' or n['ds'] == ds]
        refs = {m: sorted(abs(r['score'][m]) for r in rows) for m in judges}
        for r in rows:
            r['p'] = {m: pctl(refs[m], r['score'][m]) for m in judges}
            for lab, mem in PANELS.items():
                r['p'][lab] = st.mean(r['p'][m] for m in mem)
        # residual of the GPT pair on the Claude mean (least squares), per sample
        x = [r['p']['panel4'] for r in rows]; y = [r['p']['gpt2'] for r in rows]
        mx, my = st.mean(x), st.mean(y)
        b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
        for r in rows:
            r['p']['gpt2_resid'] = r['p']['gpt2'] - (my + b * (r['p']['panel4'] - mx))
        D = {'n': len(rows), 'days': len({r['date'] for r in rows}),
             'anon': sum(r['anon'] for r in rows), 'gpt2_on_panel4_slope': round(b, 3),
             'short_all': {mk: round(st.mean(-r['moves'][mk] for r in rows if r['moves'][mk] is not None), 2)
                           for mk in MOVES}}
        D['skill'] = {}
        for col in list(judges) + list(PANELS) + ['gpt2_resid']:
            f_raw = (lambda r, c=col: r['score'][c]) if col in judges else (lambda r, c=col: r['p'][c])
            f_p = lambda r, c=col: r['p'][c]
            D['skill'][col] = {mk: {'within_day': within_day(rows, f_raw, mk),
                                    'tops': ([b for t in TOPS if (b := book(rows, f_p, t, mk))]
                                             if col != 'gpt2_resid' else []),
                                    'k': ([b for k in KS if (b := book_k(rows, f_p, k, mk))]
                                          if col in PANELS else [])}
                               for mk in MOVES}
        cols = list(judges) + ['panel4', 'gpt2']
        D['corr'] = {f'{a}~{c}': round(spear([r['p'][a] for r in rows], [r['p'][c] for r in rows]), 3)
                     for i, a in enumerate(cols) for c in cols[i + 1:]}
        # inside the panel's top 20%: do the GPT judges agree on the sign?
        D['agree_split'] = {}
        for mk in MOVES:
            top = [r for r in rows if r['moves'][mk] is not None and abs(r['p']['panel4']) >= 80]
            g = {}
            for lab, sel in (('both_agree', lambda r: all(sgn(r['p'][m]) == sgn(r['p']['panel4']) for m in GPT)),
                             ('not_both', lambda r: not all(sgn(r['p'][m]) == sgn(r['p']['panel4']) for m in GPT))):
                s = [sgn(r['p']['panel4']) * r['moves'][mk] for r in top if sel(r)]
                g[lab] = stats(s) if s else {'n': 0}
            D['agree_split'][mk] = g
        # the names a GPT member would add to / drop from the panel's top 20%
        D['swap'] = {}
        for lab in ('panel4+astra', 'panel4+sol61', 'panel6'):
            for mk in MOVES:
                a = {r['pid'] for r in rows if abs(r['p']['panel4']) >= 80 and r['moves'][mk] is not None}
                c = {r['pid'] for r in rows if abs(r['p'][lab]) >= 80 and r['moves'][mk] is not None}
                byid = {r['pid']: r for r in rows}
                inn = [sgn(byid[i]['p'][lab]) * byid[i]['moves'][mk] for i in c - a]
                out = [sgn(byid[i]['p']['panel4']) * byid[i]['moves'][mk] for i in a - c]
                D['swap'][f'{lab}|{mk}'] = {'kept': len(a & c), 'added': stats(inn) if inn else {'n': 0},
                                            'dropped': stats(out) if out else {'n': 0}}
        D['leak_split'] = {}
        for lab, sel in (('anonymised', lambda r: r['anon']), ('named', lambda r: not r['anon'])):
            g = [r for r in rows if sel(r)]
            D['leak_split'][lab] = {'n': len(g), **{m: within_day(g, lambda r, c=m: r['score'][c], 'e1930')
                                                    for m in judges}} \
                if len(g) >= 3 else {'n': len(g)}
            for m in ('panel4', 'gpt2'):
                if len(g) >= 3:
                    D['leak_split'][lab][m] = within_day(g, lambda r, c=m: r['p'][c], 'e1930')
        doc['samples'][ds] = D
    doc['rows'] = [{'ds': r['ds'], 'date': r['date'], 'ticker': r['ticker'], 'pid': r['pid'],
                    'anon': r['anon'], 'moves': r['moves'], 'score': r['score']} for r in names]
    return doc


def report(doc):
    for ds, D in doc['samples'].items():
        print(f"\n=== {ds}: {D['n']} names, {D['days']} days, anon {D['anon']}, short all {D['short_all']}")
        for mk in MOVES:
            print(f"  [{mk}]  {'':13s} {'rho (p)':>16s}   " + '   '.join(f'top{t:<3d}' for t in TOPS)
                  + '  |  ' + '   '.join(f'k{k:<5d}' for k in KS))
            for col, S in D['skill'].items():
                w = S[mk]['within_day']
                tops = {b['top']: b for b in S[mk]['tops']}
                ks = {b['k']: b for b in S[mk]['k']}
                cells = [f"{tops[t]['n']:3d} {tops[t]['mean']:+5.1f}" if t in tops else '         ' for t in TOPS]
                kc = [f"{ks[k]['mean']:+5.1f}" if k in ks else '     ' for k in KS]
                ws = f"{w['rho']:+.3f} ({w['p']:.3f})" if w else '-'
                print(f"   {col:13s} {ws:>16s}   " + '  '.join(cells) + '  |  ' + '   '.join(kc))
        print('  corr:', D['corr'])
        print('  slope gpt2 on panel4:', D['gpt2_on_panel4_slope'])
        print('  panel top20 by GPT agreement:', D['agree_split'])
        print('  swaps:', D['swap'])
        print('  leak split:', {k: {m: (v[m] or {}).get('rho') for m in ('panel4', 'gpt2', 'astra', 'sol61')}
                                if 'panel4' in v else v for k, v in D['leak_split'].items()})


def main():
    names, missing = sample()
    print(f"sample: {len(names)} names ({sum(n['ds'] == 'backtest' for n in names)} backtest, "
          f"{sum(n['ds'] == 'oktober' for n in names)} oktober); no Codex score for {missing}")
    doc = analyse(names)
    doc['missing_codex'] = missing
    json.dump(doc, open(HERE / 'results.json', 'w'), indent=1)
    report(doc)


if __name__ == '__main__':
    main()
