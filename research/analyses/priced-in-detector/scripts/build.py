"""Observations (event x checkpoint) with features and forward returns, plus per-event rule paths.
Usage: build.py ev.json cache_dir out.json"""
import json, sys, os, math, bisect, statistics as st, collections
EV, C, OUT = sys.argv[1:4]
E = json.load(open(EV))
AMC_CP = [-450, -390, -300, 420, 510, 565, 575, 585, 600, 630, 660, 720]
BMO_CP = [420, 510, 565, 575, 585, 600, 630, 660, 720]
LATE = [750, 780, 810, 840, 870, 900, 930]
def build(e):
    p = f"{C}/{e['ticker']}_{e['event_date']}.json"
    if not os.path.exists(p): return None
    d = json.load(open(p)); rd, prev = d['day'], d['prev']
    B = []
    for b in d['m1']:
        t = b[1] if b[0] == rd else (b[1] - 1440 if b[0] == prev else None)
        if t is None: continue
        B.append((t, b[2], b[5], b[6], b[7] or b[5]))   # t, open, close, vol, vwap
    B.sort()
    R = -480 if e['session'] == 'amc' else 240
    # prior regular close P0: amc = event day (prev) regular close; bmo = prev session close. From 15-min bars.
    q = d['q15']
    pc = [x for x in q if x[0] == prev and x[1] == 945]
    if not pc: return None
    P0 = pc[-1][2]
    # normal volume per 15-min slot (exclude the event day for amc)
    days = sorted({x[0] for x in q if not (e['session'] == 'amc' and x[0] == prev)})
    if len(days) < 15: return None
    slot = collections.defaultdict(float)
    for x in q:
        if e['session'] == 'amc' and x[0] == prev: continue
        slot[x[1]] += x[3]
    def norm_rate(minute):     # normal shares per minute at clock minute (minute of day)
        m = minute % 1440; s = (m // 15) * 15
        return max(slot.get(s, 0.0) / len(days), 100.0) / 15.0
    if not B: return None
    T = [b[0] for b in B]
    def px(t, stale=30):
        i = bisect.bisect_left(T, t) - 1
        if i < 0 or t - T[i] > stale: return None
        return B[i][2]
    def vol_in(a, b):
        i, j = bisect.bisect_left(T, a), bisect.bisect_left(T, b)
        return sum(B[k][3] for k in range(i, j))
    def av(t):
        n = sum(norm_rate(m) for m in range(t - 15, t))
        return vol_in(t - 15, t) / n
    reg_open = [b for b in B if 570 <= b[0] <= 574]
    popen = reg_open[0][1] if reg_open else None
    def feats(t):
        Pt = px(t)
        if Pt is None or t <= R + 15: return None
        M = (Pt / P0 - 1) * 100; dd = 1 if M >= 0 else -1
        W = 30 if t > 570 else 60
        Pw = px(t - W, stale=60)
        i0, i1 = bisect.bisect_left(T, R), bisect.bisect_left(T, t)
        seg = B[i0:i1]
        if len(seg) < 10: return None
        rets = [math.log(seg[k][2] / seg[k - 1][2]) * 100 for k in range(1, len(seg)) if seg[k - 1][2] > 0 and seg[k][2] > 0]
        sig = st.pstdev(rets) if len(rets) > 5 else None
        nw = sum(1 for b in seg if b[0] >= t - W)
        TR = None
        if Pw and sig and nw >= 2: TR = dd * math.log(Pt / Pw) * 100 / (sig * math.sqrt(nw))
        vv = sum(b[3] for b in seg)
        VW = dd * (Pt - sum(b[3] * b[4] for b in seg) / vv) / P0 * 100 if vv > 0 else None
        a = av(t)
        r0 = R if t <= 570 else 570
        peak = max([av(x) for x in range(r0 + 15, t + 1, 5)] + [a])
        DEC = a / peak if peak > 0 else None
        return dict(t=t, M=round(M, 3), d=dd, TR=None if TR is None else round(TR, 3), VW=None if VW is None else round(VW, 3),
                    AV=round(a, 2), DEC=None if DEC is None else round(DEC, 3), P=Pt)
    cps = AMC_CP if e['session'] == 'amc' else BMO_CP
    obs = [f for f in (feats(t) for t in cps + LATE) if f]
    p13, pcl = px(780), px(955)
    if p13 is None or pcl is None or popen is None: return None
    for o in obs:
        o['F13'] = round(o['d'] * (p13 - o['P']) / P0 * 100, 3) if o['t'] < 780 else None
    for k in range(len(obs) - 1):
        obs[k]['F1'] = round(obs[k]['d'] * (obs[k + 1]['P'] - obs[k]['P']) / P0 * 100, 3)
    return dict(ticker=e['ticker'], event_date=e['event_date'], session=e['session'], day=rd, P0=P0, open=popen,
                p13=p13, pclose=pcl, close_move=round((pcl / P0 - 1) * 100, 3), obs=obs, calls=e['calls'])
rows = []
for e in E:
    if not e.get('react_day') or not ('2026-08-31' <= e['react_day'] <= '2026-11-06'): continue
    try: r = build(e)
    except Exception as ex: print('err', e['ticker'], ex); r = None
    if r: rows.append(r)
json.dump(rows, open(OUT, 'w'))
print(len(rows), 'events', sum(len(r['obs']) for r in rows), 'obs')
