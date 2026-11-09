"""Option 15-min trade bars by constructed OCC symbols (Alpaca's contract list misses many names):
Friday expiries within 35 days after the reaction day, strikes on a price-dependent grid within 12%.
Usage: fetch_opt2.py ev.json cache out_dir [max_day]. Keys from env, never printed."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error, collections
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
EV, C, OUT = sys.argv[1:4]; MAXD = sys.argv[4] if len(sys.argv) > 4 else '2026-11-06'; os.makedirs(OUT, exist_ok=True)
def iso(day, m): return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(m // 60, m % 60), NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def et(t):
    x = dt.datetime.fromisoformat(t.replace('Z', '+00:00')).astimezone(NY); return x.date().isoformat(), x.hour * 60 + x.minute
def get(url):
    for a in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(min(30, 2 ** a)); continue
            if e.code in (400, 422): return {'bars': {}}
            time.sleep(2 ** a)
        except Exception: time.sleep(2 ** a)
    raise RuntimeError('retries')
def bars(syms, start, end):
    out = collections.defaultdict(list); tok = None
    while True:
        q = dict(symbols=','.join(syms), timeframe='15Min', start=start, end=end, limit=10000)
        if tok: q['page_token'] = tok
        d = get('https://data.alpaca.markets/v1beta1/options/bars?' + urllib.parse.urlencode(q))
        for s, v in (d.get('bars') or {}).items(): out[s] += v
        tok = d.get('next_page_token')
        if not tok: return out
def grid(P):
    st = 0.5 if P < 50 else (2.5 if P < 200 else 5.0)
    lo, hi = P * 0.88, P * 1.12; k = (lo // st + 1) * st; out = []
    while k <= hi: out.append(round(k, 2)); k += st
    return out
E = json.load(open(EV)); by = collections.defaultdict(list)
for e in E:
    rd = e.get('react_day')
    if not rd or rd < '2026-08-31' or rd > MAXD: continue
    p = f"{C}/{e['ticker']}_{e['event_date']}.json"
    if not os.path.exists(p): continue
    d = json.load(open(p)); pc = [x for x in d['q15'] if x[0] == d['prev'] and x[1] == 945]
    if pc: by[rd].append((e['ticker'].replace('-', '').replace('.', ''), f"{e['ticker']}_{e['event_date']}", d['prev'], pc[-1][2]))
def do_day(rd):
    p = f'{OUT}/{rd}.json'
    if os.path.exists(p): return rd, 'cached'
    r0 = dt.date.fromisoformat(rd)
    fr = [r0 + dt.timedelta(days=k) for k in range(1, 36) if (r0 + dt.timedelta(days=k)).weekday() == 4]
    sym2 = {}
    for und, key, prev, P0 in by[rd]:
        for ex in fr:
            for k in grid(P0):
                for t in 'CP': sym2[f"{und}{ex.strftime('%y%m%d')}{t}{int(round(k * 1000)):08d}"] = (key, ex.isoformat(), t, k)
    syms = list(sym2); prev = by[rd][0][2]; B = {}
    for j in range(0, len(syms), 100): B.update(bars(syms[j:j + 100], iso(prev, 900), iso(rd, 960)))
    res = collections.defaultdict(list)
    for s, v in B.items():
        key, ex, t, k = sym2[s]; res[key].append(dict(x=ex, t=t, k=k, b=[[*et(z['t']), z['c'], z['v']] for z in v]))
    json.dump(res, open(p, 'w')); return rd, len(res), len(by[rd])
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(do_day, sorted(by)): print(*r, flush=True)
print('done')
