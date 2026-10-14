#!/usr/bin/env python3
"""SubQ Snap as a GATE over the four judges (operator, 2026-10-14): Snap reads the four
panel judges' reports on a name and answers one yes/no question, is the expected return
of trading this name on the panel's side above 3%?

Sample: the same 154 US names as `../snap-juror-backtest/` (the Aug-Sep blind re-judge
without the September Opus 5.5 hunts, plus the October E-P panels), same returns.

What "the reports" are differs by sample, and that is a property of the data, not a
choice: in the backtest the judges wrote only their numbers (abs_move_pct, p_up,
impact_sum); in October every report also lists the evidence items it counted, with the
size it gave each, and a note. Each finding's item number is resolved to that item's
text, so a report reads on its own. Judges are labelled judge_1..judge_4 in a fixed
order (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1); model names are not shown.

The trade is fixed before Snap is asked: the panel's side, the sign of the mean of the
four judges' signed percentiles (each judge's |impact_sum| ranked within the sample, no
outcome used), the live E-P rule. A name where that mean is 0 has no trade and is left
out.

Three arms, one call per name (Snap is deterministic for identical bytes):

- `gate` THE ARM UNDER TEST: the four reports, a minimal baseline (event date, session,
  implied move, median past reaction, 20-day run-up) and the trade side.
- `gate_pct`: the same plus each judge's percentile in its own range. Exploratory: the
  live panel has that number, the raw reports do not.
- `gate_bare`: LEAKAGE CONTROL. Only ticker, company, event date, session and the side.
  145 of the names were sealed before Snap's release (2026-10-12).

Fixed before any call, in this order:

1. The yes group (P(yes) > 0.5): number of names, mean return on the panel's side, hit
   rate, standard error, against the no group and against all names on the panel's side.
2. Against the live rule on the same names: the panel's top 20% (|mean pct| >= 80), and
   at an equal number of names, the k names with the highest P(yes) against the k with
   the highest |mean pct|, k = the yes count.
3. Inside the panel's top 20%: Snap yes against Snap no. Outside it: does a yes find
   winners the panel would not trade?
4. The within-day Spearman of P(yes) with the signed return.
Reported per sample (backtest numbers-only, October full reports) and pooled; returns at
the strategy exit entered 19:30 CET (e1930) and at the close (e2200), gross.

  python3 research/analyses/snap-gate/snap_gate.py [--arms gate,gate_pct,gate_bare]
                                                   [--analyse-only]
Needs `researcher_us/scripts/snap_juror.py` (branch claude/gallant-bohr-hzsesq) and
SUBQ_API_KEY, which is never written down. Responses are cached in responses.jsonl.
"""
import argparse, glob, json, os, statistics as st, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'researcher_us' / 'scripts'))
sys.path.insert(0, str(REPO / 'research' / 'analyses' / 'snap-juror-backtest'))
import snap_juror as sj           # noqa: E402
import snap_backtest as sb        # noqa: E402

REJ = REPO / 'research/analyses/rejudge-four-models'
CACHE = HERE / 'responses.jsonl'
MEMBERS = sb.MEMBERS
REJ_MODEL = {'opus5': 'opus5', 'opus': 'opus55', 'sonnet': 'sonnet55', 'fable': 'fable51'}
MOVES = sb.MOVES
GATE_VERSION = 'snap-gate.v1'

BRIEF = (
    "Four independent judges, each a different AI model, read the same research evidence "
    "about one US company that reports quarterly earnings in the window below. Each "
    "reported abs_move_pct (how far the stock moves over the window, whatever the "
    "direction, in percent), p_up (the probability, 0 to 100, that it closes the window "
    "higher; 50 is no view) and impact_sum (its signed expected move in points, about "
    "(2 x p_up / 100 - 1) x abs_move_pct). Some reports also list the evidence items the "
    "judge counted, with the size it gave each, and a one-line note. The judges size on "
    "different scales, so one judge's typical number is not another's. The panel trades "
    "this name on the side in `trade.side`: long buys at the entry and sells at the exit, "
    "short sells at the entry and buys back at the exit. Decide whether the expected "
    "return of that trade over the window, gross of costs, is above 3% of the entry price. "
    "Use only what is in this state, and nothing you may know about what happened after "
    "the event date.")
PCT_NOTE = (" Each report also carries pct_in_own_range: where that judge's |impact_sum| sits "
            "among all the sizes that judge gave in this sample, 0 to 100.")
BARE_BRIEF = (
    "One US company reports quarterly earnings in the window below, and a trader takes the "
    "side in `trade.side` (long buys at the entry and sells at the exit, short the reverse). "
    "From what you know about the company, decide whether the expected return of that trade "
    "over the window, gross of costs, is above 3% of the entry price. Use nothing you may "
    "know about what happened after the event date.")
QUESTION = {"above_3pct": {"type": "noul", "instructions": (
    "Is the expected return of the trade in `trade`, over the window, above 3% of the "
    "entry price?")}}


def sgn(x): return (x > 0) - (x < 0)


# --------------------------------------------------------------------------- reports
def judge_outputs():
    """(date, ticker) -> {member: judge output}, from the re-judge files and the October
    panel files."""
    key = json.load(open(REJ / 'key.json'))
    back = {k.get('pid', k['id']): (k['day'], k['ticker']) for k in key if k['region'] == 'us'}
    back.update({k['id']: (k['day'], k['ticker']) for k in key if k['region'] == 'us'})
    out = {}
    for f in glob.glob(str(REJ / 'out-*-*.json')):
        m = REJ_MODEL.get(Path(f).stem.split('-')[-1])
        if not m: continue
        for o in json.load(open(f)):
            if o['id'] in back:
                out.setdefault(back[o['id']], {})[m] = o
    for d in sorted(glob.glob(str(REPO / 'research/2026/10/*/edge-panel/panel'))):
        date = Path(d).parents[1].name
        for m in MEMBERS:
            f = Path(d) / f'{m}.json'
            if f.exists():
                for o in json.load(open(f)):
                    out.setdefault((date, o['id'].split('/')[-1]), {})[m] = o
    return out


def report(o, pack, pct=None):
    r = {k: o.get(k) for k in ('abs_move_pct', 'p_up', 'impact_sum')}
    if pct is not None:
        r['pct_in_own_range'] = round(abs(pct))
    ev = {e['i']: e for e in pack.get('evidence') or []}
    if o.get('findings'):
        r['findings'] = []
        for f in o['findings']:
            e = ev.get(f.get('i')) or {}
            r['findings'].append({'expected_impact_pct': f.get('expected_impact_pct'),
                                  'item': (e.get('text') or '')[:400], 'kind': e.get('kind'),
                                  'source': e.get('source')})
    if o.get('note'):
        r['note'] = o['note']
    return r


def baseline_min(pack):
    b = pack.get('baseline') or {}
    return {'ticker': b.get('ticker'), 'event_date': b.get('event_date'),
            'session': b.get('session'),
            'implied_move_pct': (b.get('options') or {}).get('event_implied_move_pct'),
            'expected_move_pct': b.get('expected_move_pct'),
            'median_abs_past_reaction_pct': (b.get('history') or {}).get('median_abs_move_pct'),
            'run_up_20d_pct': (b.get('tape') or {}).get('run_up_20d_pct')}


def body(n, arm):
    c = sj.cfg()
    side = 'long' if n['side'] > 0 else 'short'
    if arm == 'gate_bare':
        if n['anon']: return None
        b = n['pack']['baseline']
        state = {'brief': BARE_BRIEF, 'window': sj.PREAMBLE,
                 'company': {'ticker': n['ticker'], 'name': n['company'],
                             'event_date': b.get('event_date'), 'session': b.get('session')},
                 'trade': {'side': side}}
    else:
        with_pct = arm == 'gate_pct'
        state = {'brief': BRIEF + (PCT_NOTE if with_pct else ''), 'window': sj.PREAMBLE,
                 'baseline': baseline_min(n['pack']),
                 'reports': {f'judge_{i + 1}': report(n['judges'][m], n['pack'],
                                                      n['pct'][m] if with_pct else None)
                             for i, m in enumerate(MEMBERS)},
                 'trade': {'side': side}}
    return {'model': c['model'], 'state': state, 'questions': QUESTION}


# ------------------------------------------------------------------------------- run
def build():
    names = sb.sample()
    J = judge_outputs()
    keep = []
    for ds in ('backtest', 'oktober'):
        rows = [n for n in names if n['ds'] == ds and all(m in J.get((n['date'], n['ticker']), {})
                                                         for m in MEMBERS)]
        refs = {m: sorted(abs(n['impact_sum'][m]) for n in rows) for m in MEMBERS}
        for n in rows:
            n['judges'] = J[(n['date'], n['ticker'])]
            n['pct'] = {m: sb.pctl(refs[m], n['impact_sum'][m]) for m in MEMBERS}
            n['panel'] = st.mean(n['pct'].values())
            n['side'] = sgn(n['panel'])
            n['full_report'] = any('note' in n['judges'][m] for m in MEMBERS)
            if n['side']:
                keep.append(n)
    return keep


def call(names, arms):
    cache = {}
    if CACHE.exists():
        for line in CACHE.open():
            r = json.loads(line); cache[(r['arm'], r['request_sha256'])] = r
    todo = []
    for n in names:
        for arm in arms:
            b = body(n, arm)
            if b is None: continue
            h = sj.sha(b); n.setdefault('req', {})[arm] = h
            if (arm, h) not in cache: todo.append((n, arm, b, h))
    print(f"{len(todo)} calls to make, {len(cache)} cached")
    key = os.environ.get('SUBQ_API_KEY')
    if todo and not key: sys.exit('SUBQ_API_KEY is not set; nothing called')
    c = sj.cfg()

    def one(t):
        n, arm, b, h = t
        resp, status, why, tries = sj.post(b, c, key)
        return {'arm': arm, 'request_sha256': h, 'date': n['date'], 'ticker': n['ticker'],
                'status': status, 'reason': why, 'attempts': tries, 'version': GATE_VERSION,
                'called_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'response': resp}
    with CACHE.open('a') as fh, ThreadPoolExecutor(4) as ex:
        for r in ex.map(one, todo):
            fh.write(json.dumps(r, ensure_ascii=False) + '\n'); fh.flush()
            cache[(r['arm'], r['request_sha256'])] = r
            if r['status'] != 'ok': print('  ', r['arm'], r['date'], r['ticker'], r['status'], r['reason'])
    return cache


def p_yes(r):
    a = ((r or {}).get('response') or {}).get('answers', {}).get('above_3pct')
    q = a.get('noul') if isinstance(a, dict) else a
    return None if q is None else float(q)


def grp(rows, mk):
    s = [r['side'] * r['moves'][mk] for r in rows if r['moves'][mk] is not None]
    if not s: return {'n': 0}
    return {'n': len(s), 'mean': round(st.mean(s), 2), 'hit': round(sum(x > 0 for x in s) / len(s), 3),
            'se': round(st.stdev(s) / len(s) ** .5, 2) if len(s) > 1 else None}


def analyse(names, cache, arms):
    for n in names:
        n['p'] = {a: p_yes(cache.get((a, (n.get('req') or {}).get(a)))) for a in arms}
    doc = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
           'version': GATE_VERSION, 'models_returned': sorted({(r.get('response') or {}).get('model')
                                                              for r in cache.values() if r.get('response')} - {None}),
           'samples': {}}
    for ds in ('backtest', 'oktober', 'pooled'):
        rows = [n for n in names if ds == 'pooled' or n['ds'] == ds]
        D = {'n': len(rows), 'days': len({r['date'] for r in rows}),
             'full_reports': sum(r['full_report'] for r in rows)}
        top = [r for r in rows if abs(r['panel']) >= 80]
        for mk in MOVES:
            M = D.setdefault(mk, {})
            M['all_on_panel_side'] = grp(rows, mk)
            M['panel_top20'] = grp(top, mk)
            for a in arms:
                have = [r for r in rows if r['p'][a] is not None]
                yes = [r for r in have if r['p'][a] > 0.5]
                no = [r for r in have if r['p'][a] <= 0.5]
                k = len(yes)
                byp = sorted([r for r in have if r['moves'][mk] is not None], key=lambda r: -r['p'][a])
                bypan = sorted([r for r in have if r['moves'][mk] is not None], key=lambda r: -abs(r['panel']))
                M[a] = {'answered': len(have), 'yes': grp(yes, mk), 'no': grp(no, mk),
                        'p_yes_median': round(st.median(r['p'][a] for r in have), 3) if have else None,
                        'equal_n': {'k': k, 'snap_top_k': grp(byp[:k], mk) if k else None,
                                    'panel_top_k': grp(bypan[:k], mk) if k else None,
                                    'overlap': len({id(r) for r in byp[:k]} & {id(r) for r in bypan[:k]})},
                        'inside_panel_top20': {'snap_yes': grp([r for r in top if r['p'][a] is not None and r['p'][a] > 0.5], mk),
                                               'snap_no': grp([r for r in top if r['p'][a] is not None and r['p'][a] <= 0.5], mk)},
                        'outside_panel_top20_yes': grp([r for r in yes if abs(r['panel']) < 80], mk),
                        'within_day': sb.within_day([dict(r, moves={mk: (r['side'] * r['moves'][mk]
                                                                          if r['moves'][mk] is not None else None)})
                                                     for r in have], lambda r, a=a: r['p'][a], mk)}
        doc['samples'][ds] = D
    doc['rows'] = [{'ds': n['ds'], 'date': n['date'], 'ticker': n['ticker'], 'anon': n['anon'],
                    'side': n['side'], 'panel_mean_pct': round(n['panel'], 1), 'full_report': n['full_report'],
                    'p_yes': n['p'], 'moves': n['moves']} for n in names]
    return doc


def show(doc, arms):
    for ds, D in doc['samples'].items():
        print(f"\n=== {ds}: {D['n']} names on a panel side, {D['days']} days, full reports {D['full_reports']}")
        for mk in MOVES:
            M = D[mk]
            f = lambda g: f"{g['n']:3d} {g['mean']:+5.2f}% ({g['hit']:.0%}, se {g['se']})" if g and g.get('n') else '  0'
            print(f" [{mk}] all on panel side {f(M['all_on_panel_side'])} | panel top20 {f(M['panel_top20'])}")
            for a in arms:
                A = M[a]; e = A['equal_n']
                print(f"   {a:9s} yes {f(A['yes'])} | no {f(A['no'])} | median P {A['p_yes_median']}")
                print(f"   {'':9s} equal n={e['k']}: snap {f(e['snap_top_k']) if e['snap_top_k'] else '-'} vs panel "
                      f"{f(e['panel_top_k']) if e['panel_top_k'] else '-'} (overlap {e['overlap']})")
                print(f"   {'':9s} in panel top20: yes {f(A['inside_panel_top20']['snap_yes'])} | no "
                      f"{f(A['inside_panel_top20']['snap_no'])} | yes outside top20 {f(A['outside_panel_top20_yes'])}"
                      f" | within-day rho {A['within_day']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arms', default='gate,gate_pct,gate_bare')
    ap.add_argument('--analyse-only', action='store_true')
    a = ap.parse_args()
    arms = a.arms.split(',')
    names = build()
    print(f"{len(names)} names with all four reports and a panel side "
          f"({sum(n['ds'] == 'backtest' for n in names)} backtest, {sum(n['ds'] == 'oktober' for n in names)} oktober)")
    if a.analyse_only:
        cache = {}
        for line in CACHE.open():
            r = json.loads(line); cache[(r['arm'], r['request_sha256'])] = r
        for n in names:
            for arm in arms:
                b = body(n, arm)
                if b is not None: n.setdefault('req', {})[arm] = sj.sha(b)
    else:
        cache = call(names, arms)
    doc = analyse(names, cache, arms)
    toks = sum(int(((r.get('response') or {}).get('usage') or {}).get('input_tokens') or 0) for r in cache.values())
    doc['input_tokens_cached'] = toks
    doc['cost_usd_cached'] = round(toks * float(sj.cfg()['usd_per_m_input_tokens']) / 1e6, 4)
    json.dump(doc, open(HERE / 'results.json', 'w'), indent=1)
    show(doc, arms)
    print(f"\nmodels returned {doc['models_returned']}; {toks} input tokens, ${doc['cost_usd_cached']}")


if __name__ == '__main__':
    main()
