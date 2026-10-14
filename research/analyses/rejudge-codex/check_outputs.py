"""Check one model's re-judge outputs against the packs, and say what is left to do.

Reads only input/*/packs/*.json and out/<model>/*.json; no outcome is opened, so the
judging model may run it. Per pack: missing, invalid JSON, ids missing or unknown,
impact_sum that is not the sum of the findings or not (2 x p_up / 100 - 1) x abs_move_pct.
Exit 0 when every pack is complete and clean.

  python3 research/analyses/rejudge-codex/check_outputs.py --model sol61
"""
import argparse, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ['A-backtest/us3', 'A-backtest/eu', 'A-backtest/x2', 'A-backtest/us1', 'A-backtest/us2',
         'A-backtest/x1']                      # part A first, small packs first; then October


def packs():
    out = [p for p in ORDER if (HERE / 'input' / p.replace('/', '/packs/')).with_suffix('.json').exists()]
    out += [f'B-oktober/{f.stem}' for f in sorted((HERE / 'input/B-oktober/packs').glob('*.json'))]
    return out


def check(model, pack):
    part, name = pack.split('/')
    ids = [x['id'] for x in json.load(open(HERE / 'input' / part / 'packs' / f'{name}.json'))]
    f = HERE / 'out' / model / f'{part}-{name}.json'
    if not f.exists():
        return 'todo', [f'{len(ids)} companies, no output yet']
    try:
        rows = json.load(open(f))
        assert isinstance(rows, list)
    except Exception as e:
        return 'bad', [f'not one valid JSON array: {e}']
    got = {r.get('id'): r for r in rows if isinstance(r, dict)}
    errs = []
    miss = [i for i in ids if i not in got]
    extra = [i for i in got if i not in ids]
    if miss: errs.append(f'{len(miss)} of {len(ids)} missing: {", ".join(miss[:5])}{" ..." if len(miss) > 5 else ""}')
    if extra: errs.append(f'unknown ids: {", ".join(map(str, extra[:5]))}')
    for i in ids:
        r = got.get(i)
        if r is None: continue
        try:
            a, p, s = float(r['abs_move_pct']), float(r['p_up']), float(r['impact_sum'])
            fs = sum(float(x['expected_impact_pct']) for x in r.get('findings') or [])
        except Exception:
            errs.append(f'{i}: abs_move_pct, p_up, impact_sum or a finding is not a number'); continue
        if not 0 <= p <= 100: errs.append(f'{i}: p_up {p} outside 0-100')
        if a < 0: errs.append(f'{i}: abs_move_pct {a} negative')
        if not math.isclose(s, fs, abs_tol=0.02): errs.append(f'{i}: impact_sum {s} != findings sum {fs:.2f}')
        if not math.isclose(s, (2 * p / 100 - 1) * a, abs_tol=0.02):
            errs.append(f'{i}: impact_sum {s} != (2 x p_up/100 - 1) x abs_move_pct = {(2 * p / 100 - 1) * a:.2f}')
    return ('partial' if miss else 'bad') if errs else 'done', errs


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--model', required=True)
    m = ap.parse_args().model
    todo = 0
    for pk in packs():
        state, errs = check(m, pk)
        todo += state != 'done'
        print(f'{state:8s} {pk}' + ''.join(f'\n         {e}' for e in errs))
    meta = HERE / 'out' / m / 'meta.json'
    print(f"\nmeta.json {'present' if meta.exists() else 'MISSING'}")
    print('ALL DONE' if not todo and meta.exists() else f'{todo} pack(s) still to do or fix')
    sys.exit(0 if not todo and meta.exists() else 1)


if __name__ == '__main__':
    main()
