"""Alpaca option contracts (nearest expiry after the reaction day, strikes within 15% of the prior close)
and their 15-min trade bars from the prior session's 15:00 ET to the reaction day's 16:00 ET.
Usage: fetch_opt.py ev.json cache out_dir [max_day]. Keys from env, never printed."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error, collections
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
EV, C, OUT = sys.argv[1:4]; MAXD = sys.argv[4] if len(sys.argv) > 4 else '2026-11-06'; os.makedirs(OUT, exist_ok=True)
def iso(day, m): return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(m // 60, m % 60), NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def get(url):
    for a in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(min(30, 2 ** a)); continue
            body = e.read()[:300]
            if e.code == 422: return {'invalid': body.decode(errors='ignore')}
            print('HTTP', e.code, body[:150], flush=True); time.sleep(2 ** a)
        except Exception: time.sleep(2 ** a)
    raise RuntimeError('retries')
def contracts(unds, d0, d1):
    unds = list(unds)
    while unds:
        r = _contracts(unds, d0, d1)
        if isinstance(r, list): return r
        bad = r.split('invalid underlying symbols:')[-1].split('"')[0].strip().split(',')
        bad = {b.strip() for b in bad}
        if not bad & set(unds): return []
        unds = [u for u in unds if u not in bad]
    return []
def _contracts(unds, d0, d1):
    out = []
    for status in ('active', 'inactive'):
        tok = None
        while True:
            q = dict(underlying_symbols=','.join(unds), expiration_date_gte=d0, expiration_date_lte=d1, status=status, limit=10000)
            if tok: q['page_token'] = tok
            d = get('https://paper-api.alpaca.markets/v2/options/contracts?' + urllib.parse.urlencode(q))
            if 'invalid' in d: return d['invalid']
            out += d.get('option_contracts') or []; tok = d.get('next_page_token')
            if not tok: break
    return out
def bars(syms, start, end):
    out = collections.defaultdict(list); tok = None
    while True:
        q = dict(symbols=','.join(syms), timeframe='15Min', start=start, end=end, limit=10000)
        if tok: q['page_token'] = tok
        d = get('https://data.alpaca.markets/v1beta1/options/bars?' + urllib.parse.urlencode(q))
        if 'invalid' in d: print('bars 422', d['invalid'][:120], flush=True); return out
        for s, v in (d.get('bars') or {}).items(): out[s] += v
        tok = d.get('next_page_token')
        if not tok: return out
def et(t):
    x = dt.datetime.fromisoformat(t.replace('Z', '+00:00')).astimezone(NY); return x.date().isoformat(), x.hour * 60 + x.minute
E = json.load(open(EV)); by = collections.defaultdict(list)
for e in E:
    rd = e.get('react_day')
    if not rd or rd < '2026-08-31' or rd > MAXD: continue
    p = f"{C}/{e['ticker']}_{e['event_date']}.json"
    if not os.path.exists(p): continue
    d = json.load(open(p)); pc = [x for x in d['q15'] if x[0] == d['prev'] and x[1] == 945]
    if pc: by[rd].append((e['ticker'].replace('-', '.'), f"{e['ticker']}_{e['event_date']}", d['prev'], pc[-1][2]))
def do_day(rd):
    p = f'{OUT}/{rd}.json'
    if os.path.exists(p): return rd, 'cached'
    d0 = (dt.date.fromisoformat(rd) + dt.timedelta(days=1)).isoformat(); d1 = (dt.date.fromisoformat(rd) + dt.timedelta(days=12)).isoformat()
    items = by[rd]; res = {}
    for j in range(0, len(items), 20):
        ch = items[j:j + 20]
        cs = contracts(sorted({x[0] for x in ch}), d0, d1)
        bu = collections.defaultdict(list)
        for c in cs: bu[c['underlying_symbol']].append(c)
        want = {}
        for und, key, prev, P0 in ch:
            cc = bu.get(und) or []
            if not cc: continue
            ex = min(c['expiration_date'] for c in cc)
            sel = [c for c in cc if c['expiration_date'] == ex and abs(float(c['strike_price']) / P0 - 1) <= 0.15]
            if sel: want[key] = (ex, prev, sel)
        syms = [c['symbol'] for v in want.values() for c in v[2]]
        if not syms: continue
        prev = ch[0][2]
        B = {}
        for k in range(0, len(syms), 100): B.update(bars(syms[k:k + 100], iso(prev, 900), iso(rd, 960)))
        for key, (ex, prev, sel) in want.items():
            res[key] = dict(expiry=ex, c=[dict(t=c['type'][0], k=float(c['strike_price']),
                       b=[[*et(x['t']), x['c'], x['v']] for x in B.get(c['symbol'], [])]) for c in sel])
    json.dump(res, open(p, 'w')); return rd, len(res)
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(do_day, sorted(by)): print(*r, flush=True)
print('done')
