"""Robustness checks for the report: hunter-only selection, leave-one-day-out, and the
largest contributors to the >=70 book."""
import json, statistics as st, runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path('analyse.py')
rows, block, day_t = g['rows'], g['block'], g['day_t']
out = []
for th in (1.0, 2.0):
    rs = [dict(r, ret=(1 if r['hunter_impact_sum'] > 0 else -1) * r['mv']) for r in rows
          if r['hunter_impact_sum'] is not None and abs(r['hunter_impact_sum']) >= th]
    out.append(block(f'hunter |impact_sum| >= {th} (own side)', rs))
    both = [r for r in rs if r['pp'] >= 70]
    out.append(block(f'  of which panel >= 70', both))
    out.append(block(f'  of which panel < 70', [r for r in rs if r['pp'] < 70]))
out.append(block('panel >= 70 but hunter |is| < 1.0', [r for r in rows if r['pp'] >= 70 and abs(r['hunter_impact_sum'] or 0) < 1.0]))
days = sorted({r['day'] for r in rows})
for th in (70, 80):
    lo = []
    for d in days:
        xs = [r['ret'] for r in rows if r['pp'] >= th and r['day'] != d]
        lo.append((st.mean(xs), d))
    out.append(f'>= {th} leave-one-day-out mean range {min(lo)[0]:+.2f} (without {min(lo)[1]}) .. {max(lo)[0]:+.2f} (without {max(lo)[1]})')
    s = sorted([r for r in rows if r['pp'] >= th], key=lambda r: -r['ret'])
    xs = [r['ret'] for r in s[3:]]
    out.append(f'>= {th} without its 3 best names: mean {st.mean(xs):+.2f}, n {len(xs)}; median all {st.median([r["ret"] for r in s]):+.2f}')
    out.append('   best: ' + ', '.join(f"{r['ticker']} {r['day'][5:]} {r['ret']:+.1f}" for r in s[:5]))
    out.append('   worst: ' + ', '.join(f"{r['ticker']} {r['day'][5:]} {r['ret']:+.1f}" for r in s[-5:]))
print('\n'.join(out))
open('extra.txt', 'w').write('\n'.join(out) + '\n')
