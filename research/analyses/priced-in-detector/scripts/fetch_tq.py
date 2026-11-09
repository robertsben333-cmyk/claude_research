"""Alpaca SIP quotes+trades in 5-minute windows, aggregated to features per symbol and window.
Usage: fetch_tq.py ev.json cal.json out_dir [max_day]. Keys from env, never printed."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error, collections, bisect
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
EV, CALP, OUT = sys.argv[1:4]; MAXD = sys.argv[4] if len(sys.argv) > 4 else '2026-11-06'
os.makedirs(OUT, exist_ok=True); CAL = json.load(open(CALP))
def iso(day, m): return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(m // 60, m % 60), NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def ts(t): return dt.datetime.fromisoformat(t[:26].rstrip('Z') + '+00:00' if 'Z' in t else t).timestamp()
def multi(kind, syms, start, end):
    out = collections.defaultdict(list); tok = None
    while True:
        q = dict(symbols=','.join(syms), start=start, end=end, feed='sip', limit=10000)
        if tok: q['page_token'] = tok
        url = f'https://data.alpaca.markets/v2/stocks/{kind}?' + urllib.parse.urlencode(q)
        for a in range(8):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120) as r: d = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(min(30, 2 ** a)); continue
                print('HTTP', e.code, e.read()[:150], flush=True); time.sleep(2 ** a)
            except Exception: time.sleep(2 ** a)
        else: raise RuntimeError('retries')
        for s, v in (d.get(kind) or {}).items():
            if kind == 'quotes': out[s] += [(ts(x['t']), x['bp'], x['ap']) for x in v]
            else: out[s] += [(ts(x['t']), x['p'], x['s'], x.get('x')) for x in v]
        tok = d.get('next_page_token')
        if not tok: return out
def feats(Q, T, t1):
    Q = [q for q in Q if q[1] > 0 and q[2] > q[1] and (q[2] - q[1]) / ((q[2] + q[1]) / 2) < 0.5]
    if len(Q) < 3: return None
    Q.sort(); tq = [q[0] for q in Q]; w = sp = 0.0
    for k, q in enumerate(Q):
        dtw = (tq[k + 1] if k + 1 < len(Q) else t1) - q[0]
        if dtw <= 0: continue
        w += dtw; sp += dtw * (q[2] - q[1]) / ((q[2] + q[1]) / 2)
    b = s = tot = rb = rs = 0.0
    for t, p, sz, x in T:
        i = bisect.bisect_right(tq, t) - 1
        if i < 0: continue
        bp, ap = Q[i][1], Q[i][2]; mid = (bp + ap) / 2; tot += sz
        if p >= ap or (p > mid and p < ap): b += sz
        elif p <= bp or p < mid: s += sz
        if x == 'D':
            c = round((p * 100) % 1, 4)
            if 0.6 <= c < 1: rb += sz
            elif 0 < c <= 0.4: rs += sz
    return dict(spread=sp / w if w else None, nq=len(Q), vol=tot, buy=b, sell=s, rbuy=rb, rsell=rs)
E = json.load(open(EV))
by = collections.defaultdict(set)
for e in E:
    rd = e.get('react_day')
    if not rd or rd < '2026-08-31' or rd > MAXD: continue
    by[rd].add((e['ticker'].replace('-', '.'), e['session']))
WIN = {'amc': [('dec0925', 0, 560), ('ref0800', 0, 480), ('nrm0925', -5, 560)],
       'bmo': [('dec0925', 0, 560), ('ref0800', 0, 480), ('nrm0925', -5, 560),
               ('dec1255', 0, 770), ('ref0950', 0, 590), ('nrm1255', -5, 770)]}
def do_day(day):
    p = f'{OUT}/{day}.json'
    if os.path.exists(p): return day, 'cached'
    i = CAL.index(day); res = collections.defaultdict(dict)
    jobs = collections.defaultdict(set)
    for sym, sess in by[day]:
        for name, off, m0 in WIN[sess]: jobs[(name, off, m0)].add(sym)
    for (name, off, m0), syms in jobs.items():
        d = CAL[i + off]; syms = sorted(syms); t1 = dt.datetime.fromisoformat(iso(d, m0 + 5).replace('Z', '+00:00')).timestamp()
        for j in range(0, len(syms), 30):
            ch = syms[j:j + 30]
            Q = multi('quotes', ch, iso(d, m0), iso(d, m0 + 5)); T = multi('trades', ch, iso(d, m0), iso(d, m0 + 5))
            for s in ch: res[s][name] = feats(Q.get(s, []), T.get(s, []), t1)
    json.dump(res, open(p, 'w')); return day, len(res)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(do_day, sorted(by)): print(*r, flush=True)
print('done')
