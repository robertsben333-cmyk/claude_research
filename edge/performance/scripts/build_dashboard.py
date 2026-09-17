#!/usr/bin/env python3
"""Render edge/performance/dashboard.html from data/ledger.json.

One self-contained file: no CDN, no build step, no network. Open it from disk, or
serve it with `edge/performance/scripts/serve.py` and the page's own refresh
button rebuilds for real.

The page filters and recomputes client-side — the lens (research or money), the
conviction threshold, the tradability floors, the session and the sector all
re-derive every statistic on the page from the rows in the ledger. That is
deliberate: a threshold you cannot move is a threshold you cannot test.

    python3 edge/performance/scripts/build_dashboard.py
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "edge" / "performance" / "data"

HTML = r"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edge hunt — performance</title>
<style>
:root {
  color-scheme: light;
  --plane:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,0.10);
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a;
  --good:#0ca30c; --bad:#d03b3b; --warn:#fab219;
  --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --plane:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,0.10);
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --good:#0ca30c; --bad:#d03b3b;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --plane:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,0.10);
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --good:#0ca30c; --bad:#d03b3b;
}
* { box-sizing:border-box; }
body {
  margin:0; background:var(--plane); color:var(--ink);
  font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;
}
.wrap { max-width:1240px; margin:0 auto; padding:20px 16px 72px; }
header { display:flex; flex-wrap:wrap; gap:12px; align-items:flex-start; justify-content:space-between; }
h1 { font-size:22px; margin:0; letter-spacing:-0.01em; }
h2 { font-size:17px; margin:26px 0 6px; }
h3 { font-size:14px; margin:0 0 10px; color:var(--ink2); font-weight:600; }
p  { margin:8px 0; color:var(--ink2); max-width:80ch; }
p.lead { color:var(--ink); }
small, .meta { color:var(--muted); font-size:12.5px; }
a { color:var(--s1); }
button, select, input { font:inherit; }
.btn {
  background:var(--surface); color:var(--ink); border:1px solid var(--ring);
  border-radius:8px; padding:6px 12px; cursor:pointer;
}
.btn:hover { border-color:var(--axis); }
.btn.primary { background:var(--s1); color:#fff; border-color:transparent; }
.btn[disabled] { opacity:.55; cursor:progress; }
nav { display:flex; flex-wrap:wrap; gap:4px; margin:16px 0 0; border-bottom:1px solid var(--grid); }
nav button {
  background:none; border:none; border-bottom:2px solid transparent; color:var(--ink2);
  padding:9px 12px; cursor:pointer; border-radius:6px 6px 0 0;
}
nav button:hover { background:var(--surface); }
nav button[aria-selected="true"] { color:var(--ink); border-bottom-color:var(--s1); font-weight:600; }
section[hidden] { display:none; }

/* --- the control bar --- */
.controls {
  position:sticky; top:0; z-index:8; background:var(--plane);
  border-bottom:1px solid var(--grid); padding:10px 0 11px; margin-bottom:6px;
  display:flex; flex-wrap:wrap; gap:8px 18px; align-items:center;
}
.ctl { display:flex; align-items:center; gap:7px; }
.ctl > label { font-size:12.5px; color:var(--muted); }
.seg { display:inline-flex; border:1px solid var(--ring); border-radius:8px; overflow:hidden; }
.seg button {
  background:var(--surface); border:none; color:var(--ink2); padding:5px 11px; cursor:pointer;
  border-right:1px solid var(--ring); font-size:13.5px;
}
.seg button:last-child { border-right:none; }
.seg button[aria-pressed="true"] { background:var(--s1); color:#fff; font-weight:600; }
.sw { display:inline-flex; align-items:center; gap:6px; font-size:13.5px; color:var(--ink2); cursor:pointer; }
input[type=number] {
  width:104px; background:var(--surface); color:var(--ink); border:1px solid var(--ring);
  border-radius:7px; padding:4px 7px; font-variant-numeric:tabular-nums;
}
input[type=range] { width:120px; accent-color:var(--s1); }
select {
  background:var(--surface); color:var(--ink); border:1px solid var(--ring);
  border-radius:7px; padding:4px 7px; max-width:190px;
}
.ctl.off { opacity:.45; }
.ctlrow { display:flex; flex-wrap:wrap; gap:8px 16px; align-items:center; width:100%; }
.ctl { border:1px solid transparent; border-radius:9px; padding:2px 6px; }
.ctl:has(input[type=checkbox]:checked) { border-color:var(--ring); background:var(--surface); }
.btn.small { padding:4px 10px; font-size:13px; }
.ctl .dash { color:var(--muted); }
input[type=date] { background:var(--surface); color:var(--ink); border:1px solid var(--ring);
                   border-radius:7px; padding:3px 6px; font-size:13px; }
.help { width:100%; background:var(--surface); border:1px solid var(--ring); border-radius:12px;
        padding:14px 18px; margin:6px 0 2px; }
.help dl { margin:6px 0; color:var(--ink2); max-width:86ch; }
.help dt { font-weight:600; color:var(--ink); margin-top:9px; }
.help dd { margin:2px 0 0 0; }
.controls { flex-direction:column; align-items:stretch; gap:8px; }
.filterline { font-size:12.5px; color:var(--muted); margin:2px 0 0; }

.card {
  background:var(--surface); border:1px solid var(--ring); border-radius:12px;
  padding:16px 18px; margin:14px 0;
}
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(168px,1fr)); gap:10px; margin:14px 0; }
.tile { background:var(--surface); border:1px solid var(--ring); border-radius:12px; padding:13px 15px; }
.tile .k { font-size:12px; color:var(--muted); }
.tile .v { font-size:25px; margin-top:3px; letter-spacing:-0.02em; }
.tile .s { font-size:12px; color:var(--ink2); margin-top:2px; }
.pos { color:var(--good); } .neg { color:var(--bad); }
table { border-collapse:collapse; width:100%; font-size:13px; font-variant-numeric:tabular-nums; }
th, td { text-align:right; padding:6px 8px; border-bottom:1px solid var(--grid); white-space:nowrap; }
th { color:var(--muted); font-weight:600; position:sticky; top:0; background:var(--surface); }
th:first-child, td:first-child { text-align:left; }
td.t { font-family:var(--mono); }
.scroll { overflow:auto; max-height:520px; }
.legend { display:flex; flex-wrap:wrap; gap:14px; margin:2px 0 10px; font-size:12.5px; color:var(--ink2); }
.legend i { width:10px; height:10px; border-radius:3px; display:inline-block; margin-right:6px; vertical-align:-1px; }
.legend i.dash { height:0; border-top:2px dashed currentColor; border-radius:0; width:14px; }
.chart { position:relative; width:100%; }
.chart svg { display:block; width:100%; height:auto; overflow:visible; }
.tip {
  position:fixed; pointer-events:none; opacity:0; transition:opacity .08s;
  background:var(--surface); border:1px solid var(--ring); border-radius:8px;
  padding:7px 10px; font-size:12.5px; color:var(--ink); box-shadow:0 4px 16px rgba(0,0,0,.14);
  z-index:20; max-width:300px;
}
.note { border-left:3px solid var(--s2); padding-left:12px; margin:14px 0; }
.warnbox { border-left:3px solid var(--warn); padding-left:12px; }
.empty { color:var(--muted); padding:22px 0; text-align:center; }
code { font-family:var(--mono); font-size:12.5px; background:var(--plane); padding:1px 5px; border-radius:5px; }
ul { color:var(--ink2); max-width:80ch; }
li { margin:4px 0; }
.log { font-family:var(--mono); font-size:12px; white-space:pre-wrap; color:var(--ink2);
       max-height:180px; overflow:auto; margin-top:8px; }
@media (max-width:640px){ .wrap{padding:14px 16px 60px;} h1{font-size:19px;} .controls{position:static;} }
</style>
</head>
<body>
<div class="wrap">
<header>
  <div>
    <h1>Edge hunt — performance</h1>
    <div class="meta" id="stamp"></div>
  </div>
  <div style="display:flex;gap:8px;align-items:center">
    <button class="btn primary" id="refresh">Ververs</button>
    <button class="btn" id="theme">donker / licht</button>
  </div>
</header>
<div class="log" id="refreshlog" hidden></div>

<div class="controls" id="controls"></div>
<div class="filterline" id="filterline"></div>

<nav id="tabs" role="tablist"></nav>
<div id="panels"></div>
<div class="tip" id="tip"></div>
</div>

<script id="ledger" type="application/json">__LEDGER__</script>
<script>
const D = JSON.parse(document.getElementById('ledger').textContent);
/* ------------------------------------------------------------- formatting */
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const n1 = x => x === null || x === undefined ? '–' : (+x).toFixed(1);
const n2 = x => x === null || x === undefined ? '–' : (+x).toFixed(2);
const n3 = x => x === null || x === undefined ? '–' : (+x).toFixed(3);
const pc = x => x === null || x === undefined ? '–' : (x > 0 ? '+' : '') + (+x).toFixed(2) + '%';
const usd = x => x === null || x === undefined ? '–' :
  (x < 0 ? '−$' : '$') + Math.abs(+x).toLocaleString('en-US', {maximumFractionDigits:0});
const usdM = x => x === null || x === undefined ? '–' :
  x >= 1e9 ? '$' + (x/1e9).toFixed(1) + 'b' :
  x >= 1e6 ? '$' + (x/1e6).toFixed(1) + 'm' :
  x >= 1e3 ? '$' + (x/1e3).toFixed(0) + 'k' : '$' + x.toFixed(0);
const sgn = x => x === null || x === undefined ? '' : (x > 0 ? 'pos' : x < 0 ? 'neg' : '');
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const tip = document.getElementById('tip');
function showTip(e, html) {
  tip.innerHTML = html; tip.style.opacity = 1;
  const r = tip.getBoundingClientRect();
  let x = e.clientX + 14, y = e.clientY - 10;
  if (x + r.width > innerWidth - 8) x = e.clientX - r.width - 14;
  if (y + r.height > innerHeight - 8) y = innerHeight - r.height - 8;
  tip.style.left = Math.max(8, x) + 'px'; tip.style.top = Math.max(8, y) + 'px';
}
const hideTip = () => tip.style.opacity = 0;

/* CET on the clock. Entry is the 16:00 ET close, which is 22:00 CET while both
   zones are on summer time — every event in this sample is. Winter shifts both
   by an hour and the offset holds; a US-only shift week would not, and would
   show up as a horizon label an hour out. */
const ET_TO_CET = 6;
const cetOfHour = h => {                       // h = hours after the 16:00 ET entry
  const m = Math.round((22 + h) * 60) % (24*60);
  return String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0');
};
const HZ_CET = {ext_early:'22:30 / 14:00', pre_open:'15:25', open:'15:30', m15:'15:45',
                m30:'16:00', m60:'16:30', midday:'18:00', close:'22:00'};
const HZ_LABEL = h => `${h} · ${HZ_CET[h] || ''}`;

/* ------------------------------------------------------------------ stats */
function ranks(xs) {
  const idx = xs.map((v,i)=>i).sort((a,b)=>xs[a]-xs[b]); const r = new Array(xs.length);
  let i = 0;
  while (i < idx.length) {
    let j = i; while (j+1 < idx.length && xs[idx[j+1]] === xs[idx[i]]) j++;
    const avg = (i+j)/2 + 1; for (let k=i;k<=j;k++) r[idx[k]] = avg; i = j+1;
  }
  return r;
}
function corr(a, b) {
  const n = a.length; if (n < 3) return null;
  const ma = a.reduce((s,x)=>s+x,0)/n, mb = b.reduce((s,x)=>s+x,0)/n;
  let num=0, da=0, db=0;
  for (let i=0;i<n;i++){ const x=a[i]-ma, y=b[i]-mb; num+=x*y; da+=x*x; db+=y*y; }
  return (da && db) ? num/Math.sqrt(da*db) : null;
}
const centred = xs => { const r = ranks(xs), m = r.reduce((s,x)=>s+x,0)/r.length;
                        return r.map(x=>x-m); };
/* Within-day ranks, centred, correlated across days — the same pooling the
   python side uses. Concatenating raw pairs across days lets market-wide drift
   into the rank structure. */
function pooledRho(days, fx, fy) {
  const A = [], B = [];
  for (const d of days) {
    const v = d.filter(r => fx(r) !== null && fx(r) !== undefined
                         && fy(r) !== null && fy(r) !== undefined);
    if (v.length < 3) continue;
    A.push(...centred(v.map(fx))); B.push(...centred(v.map(fy)));
  }
  return A.length < 3 ? null : corr(A, B);
}
function convictionRho(rows, fx, fy) {
  const v = rows.filter(r => fx(r) && fy(r) !== null && fy(r) !== undefined);
  if (v.length < 4) return null;
  return corr(ranks(v.map(r=>Math.abs(fx(r)))), v.map(r => (fx(r)>0) === (fy(r)>0) ? 1 : 0));
}
function ttest(xs) {
  const n = xs.length; if (!n) return {n:0};
  const m = xs.reduce((s,x)=>s+x,0)/n;
  if (n < 3) return {n, mean:m};
  const sd = Math.sqrt(xs.reduce((s,x)=>s+(x-m)*(x-m),0)/(n-1)), se = sd/Math.sqrt(n);
  return {n, mean:m, sd, t: se ? m/se : null, ci: se ? [m-1.96*se, m+1.96*se] : null};
}
function book(rets) {
  const o = ttest(rets);
  o.hits = rets.filter(x=>x>0).length;
  o.hit = rets.length ? 100*o.hits/rets.length : null;
  o.median = rets.length ? [...rets].sort((a,b)=>a-b)[Math.floor(rets.length/2)] : null;
  return o;
}
/* Spread, not just the middle. A mean with no dispersion beside it hides whether a
   book is a steady edge or one trade carrying eight. */
function spread(xs) {
  if (!xs.length) return {n:0};
  const v = [...xs].sort((a,b)=>a-b), q = f => {
    const i = (v.length-1)*f, lo = Math.floor(i), hi = Math.ceil(i);
    return v[lo] + (v[hi]-v[lo])*(i-lo);
  };
  const o = ttest(xs);
  return {...o, median:q(0.5), p25:q(0.25), p75:q(0.75), iqr:q(0.75)-q(0.25),
          min:v[0], max:v[v.length-1],
          hits: xs.filter(x=>x>0).length, hit: 100*xs.filter(x=>x>0).length/xs.length};
}
/* Compound a list of period returns in percent. */
const compound = rs => (rs.reduce((a,r)=>a*(1+r/100), 1) - 1) * 100;

/* Least squares through the points, for a trend line. Reported with its r², so a
   line drawn through noise announces itself. */
function ols(pts) {
  const n = pts.length; if (n < 3) return null;
  const mx = pts.reduce((s,p)=>s+p.x,0)/n, my = pts.reduce((s,p)=>s+p.y,0)/n;
  let sxy=0, sxx=0, syy=0;
  for (const p of pts){ sxy+=(p.x-mx)*(p.y-my); sxx+=(p.x-mx)**2; syy+=(p.y-my)**2; }
  if (!sxx) return null;
  const b = sxy/sxx;
  return {slope:b, intercept:my - b*mx, r2: syy ? (sxy*sxy)/(sxx*syy) : null, n};
}

/* ------------------------------------------------------- filters and lenses */
const DATES = [...new Set(D.names.map(r => r.run_date))].sort();
const DEFAULTS = {
  lens: 'research', horizon: 'close',
  thrOn: false, thr: D.conviction_floor ?? 3,
  tradeOn: false, minLong: 200000, minShort: 1000000, reqShort: true,
  session: 'all', sector: 'all',
  from: DATES[0] || '', to: DATES[DATES.length-1] || '',
  capOn: false, capPct: 33, grossPct: 100
};
const F = {...DEFAULTS};
/* How much of the equity a day actually puts to work. The stage splits a gross
   budget equally over the day's names and caps each one, so a day with few names is
   deliberately under-invested and a day with many is diluted. With the cap off every
   day counts as fully invested, which is the research view. */
const deployedPct = n => F.capOn ? Math.min(F.grossPct, n * F.capPct) : 100;
const ALL = D.names.filter(r => !r.duplicate_event);
const advOf = r => r.dollar_vol ?? r.plan_dollar_volume_usd ?? null;
const mvOf = r => r['mv_' + F.horizon];
const boardOf = r => r['ret_' + F.horizon];
/* The money lens uses the broker's own return on the position that name became;
   a name that was never traded simply leaves the lens. */
const retOf = r => F.lens === 'trading' ? (r.trade_ret_pct ?? null) : boardOf(r);

function passesFilters(r) {
  if (F.from && r.run_date < F.from) return false;
  if (F.to && r.run_date > F.to) return false;
  if (F.session !== 'all' && r.session !== F.session) return false;
  if (F.sector !== 'all' && (r.sector || 'onbekend') !== F.sector) return false;
  if (F.thrOn && Math.abs(r.impact_sum) < F.thr) return false;
  if (F.tradeOn) {
    const adv = advOf(r), short = r.impact_sum < 0;
    if (adv === null) return false;
    if (adv < (short ? F.minShort : F.minLong)) return false;
    if (short && F.reqShort && r.shortable !== true) return false;
  }
  return true;
}
const rowsFor = (extra) => ALL.filter(r => passesFilters(r) && retOf(r) !== null
                                        && retOf(r) !== undefined && (!extra || extra(r)));
const rankRows = () => ALL.filter(r => passesFilters(r) && mvOf(r) !== null
                                    && mvOf(r) !== undefined);
function byDay(rows) {
  const m = new Map();
  rows.forEach(r => { if (!m.has(r.run)) m.set(r.run, []); m.get(r.run).push(r); });
  return [...m.entries()].sort((a,b)=>a[0]<b[0]?-1:1).map(e=>e[1]);
}
/* Trades pass the same filters, through the name row they came from. A position
   whose name is not in this run's ranking (a hand trade) is kept: it is money. */
const inRange = d => (!F.from || d >= F.from) && (!F.to || d <= F.to);
const curveRows = () => ((D.account && D.account.curve) || []).filter(c => inRange(c.date));
const dailyRows = () => ((D.stats.trading || {}).daily || []).filter(d => inRange(d.date));
const nameIndex = new Map(ALL.map(r => [r.run_date + '|' + r.ticker, r]));
const nameOfTrade = t => nameIndex.get(t.run_date + '|' + t.symbol) || null;
function tradesFiltered(closedOnly) {
  return D.trades.filter(t => {
    if (closedOnly && (t.ret_pct === null || t.ret_pct === undefined)) return false;
    const r = nameOfTrade(t);
    if (!r) return !(F.thrOn || F.tradeOn || F.sector !== 'all' || F.session !== 'all');
    return passesFilters(r);
  });
}

/* ----------------------------------------------------------------- charts */
const SVG = 'http://www.w3.org/2000/svg';
function el(tag, attrs, parent) {
  const e = document.createElementNS(SVG, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function frame(host, h) {
  host.innerHTML = '';
  const w = Math.max(320, host.clientWidth || 640);
  return {svg: el('svg', {viewBox:`0 0 ${w} ${h}`, width:w, height:h}, host), w, h};
}
function scaleTicks(min, max, n) {
  if (!isFinite(min) || !isFinite(max)) { min = 0; max = 1; }
  if (min === max) { min -= 1; max += 1; }
  const raw = (max-min)/n, mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1,2,2.5,5,10].map(m=>m*mag).find(s=>s>=raw) || mag*10;
  const lo = Math.floor(min/step)*step, hi = Math.ceil(max/step)*step, out = [];
  for (let v = lo; v <= hi + 1e-9; v += step) out.push(+v.toFixed(10));
  return out;
}
function yAxis(svg, x0, x1, ticks, Y, fmt, label) {
  const g = css('--grid'), m = css('--muted');
  ticks.forEach(v => {
    el('line', {x1:x0, x2:x1, y1:Y(v), y2:Y(v), stroke:g, 'stroke-width':1}, svg);
    const t = el('text', {x:x0-8, y:Y(v)+4, fill:m, 'font-size':11, 'text-anchor':'end'}, svg);
    t.textContent = fmt ? fmt(v) : v;
  });
  if (label) { const t = el('text', {x:x0, y:12, fill:m, 'font-size':11}, svg);
               t.textContent = label; }
}
function noData(host) { host.innerHTML = '<div class="empty">geen rijen onder deze filters</div>'; }

function lineChart(host, spec) {
  const h = spec.height || 240, {svg, w} = frame(host, h);
  const pad = {l:54, r:18, t:18, b: spec.sub ? 40 : 28};
  const xs = spec.x, x0 = pad.l, x1 = w-pad.r, y0 = pad.t, y1 = h-pad.b;
  const vals = spec.series.flatMap(s => s.values.filter(v => v !== null && v !== undefined));
  if (!vals.length) { noData(host); return; }
  const tv = scaleTicks(Math.min(...vals, spec.zero ? 0 : Infinity),
                        Math.max(...vals, spec.zero ? 0 : -Infinity), 4);
  const mn = tv[0], mx = tv[tv.length-1];
  const X = i => x0 + (xs.length < 2 ? (x1-x0)/2 : i*(x1-x0)/(xs.length-1));
  const Y = v => y1 - (v-mn)/(mx-mn)*(y1-y0);
  yAxis(svg, x0, x1, tv, Y, spec.fmtY, spec.labelY);
  if (mn < 0 && mx > 0)
    el('line', {x1:x0, x2:x1, y1:Y(0), y2:Y(0), stroke:css('--axis'), 'stroke-width':1}, svg);
  const every = xs.length > 12 ? Math.ceil(xs.length/9) : 1;
  xs.forEach((lab, i) => {
    if (i % every) return;
    const t = el('text', {x:X(i), y:h-(spec.sub?24:8), fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = lab;
    if (spec.sub && spec.sub[i]) {
      const s = el('text', {x:X(i), y:h-8, fill:css('--muted'), 'font-size':10,
                            'text-anchor':'middle'}, svg);
      s.textContent = spec.sub[i];
    }
  });
  const ends = [];
  spec.series.forEach(s => {
    const pts = s.values.map((v,i) => (v === null || v === undefined) ? null : [X(i), Y(v)]).filter(Boolean);
    if (pts.length > 1)
      el('path', {d:'M'+pts.map(p=>p.join(' ')).join(' L'), fill:'none', stroke:s.color,
                  'stroke-width':2, 'stroke-linejoin':'round',
                  'stroke-dasharray': s.dash || ''}, svg);
    pts.forEach(p => el('circle', {cx:p[0], cy:p[1], r:3.5, fill:s.color,
                                   stroke:css('--surface'), 'stroke-width':2}, svg));
    if (pts.length && spec.label !== false)
      ends.push({x:pts[pts.length-1][0], y:pts[pts.length-1][1]-9, s});
  });
  // Push overlapping end labels apart, nearest-first, so two series ending at the
  // same value do not print one word on top of another.
  ends.sort((a,b)=>a.y-b.y);
  for (let i=1;i<ends.length;i++)
    if (ends[i].y - ends[i-1].y < 13) ends[i].y = ends[i-1].y + 13;
  ends.forEach(e => {
    const t = el('text', {x:e.x, y:Math.min(e.y, y1-2), fill:e.s.color, 'font-size':11.5,
                          'text-anchor':'middle'}, svg);
    t.textContent = e.s.label;
  });
  xs.forEach((lab, i) => {
    const bw = (x1-x0)/Math.max(1, xs.length-1);
    const hit = el('rect', {x:X(i)-bw/2, y:y0, width:bw, height:y1-y0, fill:'transparent'}, svg);
    hit.addEventListener('mousemove', e => showTip(e, `<b>${esc(spec.tipX ? spec.tipX(i) : lab)}</b><br>` +
      spec.series.map(s => `<span style="color:${s.color}">■</span> ${esc(s.label)}: ` +
        (s.values[i] === null || s.values[i] === undefined ? '–'
         : (spec.fmtT ? spec.fmtT(s.values[i]) : n2(s.values[i])))).join('<br>')));
    hit.addEventListener('mouseleave', hideTip);
  });
}

function barChart(host, spec) {
  const items = spec.items, h = spec.height || 240, {svg, w} = frame(host, h);
  const pad = {l:54, r:18, t:18, b:36};
  const x0 = pad.l, x1 = w-pad.r, y0 = pad.t, y1 = h-pad.b;
  if (!items.length) { noData(host); return; }
  const tv = scaleTicks(Math.min(0, ...items.map(i=>i.v)), Math.max(0, ...items.map(i=>i.v)), 4);
  const mn = tv[0], mx = tv[tv.length-1], Y = v => y1 - (v-mn)/(mx-mn)*(y1-y0);
  yAxis(svg, x0, x1, tv, Y, spec.fmtY, spec.labelY);
  const step = (x1-x0)/items.length, bw = Math.max(5, Math.min(52, step-8));
  items.forEach((it, i) => {
    const cx = x0+step*i+step/2, base = Y(0), top = Y(it.v);
    const col = it.color || (it.v >= 0 ? css('--good') : css('--bad'));
    el('rect', {x:cx-bw/2, y:Math.min(base,top), width:bw,
                height:Math.max(2,Math.abs(base-top)), rx:4, fill:col}, svg);
    const t = el('text', {x:cx, y:h-20, fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = it.label;
    if (it.sub) { const s = el('text', {x:cx, y:h-7, fill:css('--muted'), 'font-size':10,
                                        'text-anchor':'middle'}, svg); s.textContent = it.sub; }
    const hit = el('rect', {x:cx-step/2, y:y0, width:step, height:y1-y0, fill:'transparent'}, svg);
    hit.addEventListener('mousemove', e => showTip(e, it.tip ||
      `<b>${esc(it.label)}</b><br>${spec.fmtT ? spec.fmtT(it.v) : n2(it.v)}`));
    hit.addEventListener('mouseleave', hideTip);
  });
  el('line', {x1:x0, x2:x1, y1:Y(0), y2:Y(0), stroke:css('--axis'), 'stroke-width':1}, svg);
}

function histChart(host, spec) {
  const xs = spec.values;
  if (xs.length < 2) { noData(host); return; }
  const lo = Math.min(...xs), hi = Math.max(...xs);
  const t = scaleTicks(lo, hi, spec.bins || 8);
  const step = t[1]-t[0];
  const bins = t.slice(0,-1).map((b,i) => ({lo:b, hi:t[i+1], v:0, rows:[]}));
  xs.forEach((x,i) => {
    let k = Math.min(bins.length-1, Math.max(0, Math.floor((x-t[0])/step)));
    bins[k].v++; bins[k].rows.push(spec.labels ? spec.labels[i] : null);
  });
  barChart(host, {height: spec.height || 200, fmtY: v=>v.toFixed(0),
    labelY: spec.labelY || 'aantal',
    items: bins.map(b => ({label: b.lo.toFixed(0) + (spec.unit || ''),
      v: b.v, color: b.hi <= 0 ? css('--bad') : b.lo >= 0 ? css('--good') : css('--muted'),
      tip:`<b>${b.lo.toFixed(1)}${spec.unit||''} tot ${b.hi.toFixed(1)}${spec.unit||''}</b><br>
           ${b.v} ${b.v===1?'positie':'posities'}${b.rows.filter(Boolean).length
             ? '<br>'+esc(b.rows.filter(Boolean).join(', ')) : ''}`}))});
}

function scatterChart(host, spec) {
  const h = spec.height || 320, {svg, w} = frame(host, h);
  const pad = {l:56, r:20, t:18, b:40};
  const x0 = pad.l, x1 = w-pad.r, y0 = pad.t, y1 = h-pad.b;
  const pts = spec.points.filter(p => p.x !== null && p.y !== null
                                   && isFinite(p.x) && isFinite(p.y));
  if (pts.length < 1) { noData(host); return; }
  const xt = scaleTicks(Math.min(...pts.map(p=>p.x)), Math.max(...pts.map(p=>p.x)), 5);
  const yt = scaleTicks(Math.min(...pts.map(p=>p.y)), Math.max(...pts.map(p=>p.y)), 4);
  const X = v => x0 + (v-xt[0])/(xt[xt.length-1]-xt[0])*(x1-x0);
  const Y = v => y1 - (v-yt[0])/(yt[yt.length-1]-yt[0])*(y1-y0);
  yAxis(svg, x0, x1, yt, Y, spec.fmtY, spec.labelY);
  xt.forEach(v => {
    el('line', {x1:X(v), x2:X(v), y1:y0, y2:y1, stroke:css('--grid'), 'stroke-width':1}, svg);
    const t = el('text', {x:X(v), y:h-22, fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = spec.fmtX ? spec.fmtX(v) : v;
  });
  if (xt[0] < 0 && xt[xt.length-1] > 0)
    el('line', {x1:X(0), x2:X(0), y1:y0, y2:y1, stroke:css('--axis'), 'stroke-width':1}, svg);
  if (yt[0] < 0 && yt[yt.length-1] > 0)
    el('line', {x1:x0, x2:x1, y1:Y(0), y2:Y(0), stroke:css('--axis'), 'stroke-width':1}, svg);
  if (spec.labelX) { const t = el('text', {x:(x0+x1)/2, y:h-5, fill:css('--muted'),
                                           'font-size':11, 'text-anchor':'middle'}, svg);
                     t.textContent = spec.labelX; }
  if (spec.diagonal) {                       // y = x, for theoretical against actual
    const lo = Math.max(xt[0], yt[0]), hi = Math.min(xt[xt.length-1], yt[yt.length-1]);
    if (hi > lo) el('line', {x1:X(lo), y1:Y(lo), x2:X(hi), y2:Y(hi), stroke:css('--muted'),
                             'stroke-width':1.5, 'stroke-dasharray':'5 4'}, svg);
  }
  let fit = null;
  if (spec.trend !== false && pts.length >= 4) {
    fit = ols(pts);
    if (fit) {
      const a = xt[0], b = xt[xt.length-1];
      const ya = fit.intercept + fit.slope*a, yb = fit.intercept + fit.slope*b;
      const cl = (v) => Math.min(Math.max(v, yt[0]), yt[yt.length-1]);
      el('line', {x1:X(a), y1:Y(cl(ya)), x2:X(b), y2:Y(cl(yb)), stroke:css('--s2'),
                  'stroke-width':2, 'stroke-dasharray':'6 4'}, svg);
    }
  }
  pts.forEach(p => {
    const c = el('circle', {cx:X(p.x), cy:Y(p.y), r:p.r || 5, fill:p.color || css('--s1'),
                            stroke:css('--surface'), 'stroke-width':2,
                            'fill-opacity': p.open ? 0.35 : 0.95}, svg);
    c.addEventListener('mousemove', e => showTip(e, p.tip));
    c.addEventListener('mouseleave', hideTip);
  });
  if (fit && spec.trendNote !== false) {
    const t = el('text', {x:x1, y:y0+2, fill:css('--s2'), 'font-size':11,
                          'text-anchor':'end'}, svg);
    t.textContent = `trend: helling ${n2(fit.slope)}, r² ${n2(fit.r2)} (n=${fit.n})`;
  }
}

/* ------------------------------------------------------------- components */
function tiles(list) {
  return `<div class="tiles">` + list.map(t => `<div class="tile">
    <div class="k">${esc(t.k)}</div><div class="v ${t.cls || ''}">${t.v}</div>
    ${t.s ? `<div class="s">${t.s}</div>` : ''}</div>`).join('') + `</div>`;
}
function table(cols, rows) {
  if (!rows.length) return '<div class="empty">geen rijen onder deze filters</div>';
  return `<div class="scroll"><table><thead><tr>` +
    cols.map(c => `<th>${esc(c.h)}</th>`).join('') + `</tr></thead><tbody>` +
    rows.map(r => `<tr>` + cols.map(c => {
      const v = c.f(r);
      return `<td class="${c.cls ? c.cls(r) : ''}">${v === undefined || v === null ? '–' : v}</td>`;
    }).join('') + `</tr>`).join('') + `</tbody></table></div>`;
}
const legend = items => `<div class="legend">` + items.map(i =>
  `<span style="color:${i.color}"><i class="${i.dash?'dash':''}" style="background:${i.dash?'none':i.color}"></i><span style="color:var(--ink2)">${esc(i.label)}</span></span>`).join('') + `</div>`;
const shortSector = x => { const w = String(x).split(' ');
  return w.length < 2 ? w[0] : w[0].slice(0,9) + '. ' + w[1].slice(0,4) + '.'; };
const chartBlock = (id, h) => `<div class="chart" id="${id}" style="min-height:${h||240}px"></div>`;
const bookRow = (label, b, extra) => b && b.n ? Object.assign(
  {label, n:b.n, hit:b.hit, mean:b.mean, med:b.median, t:b.t,
   ci: b.ci ? `${n1(b.ci[0])} … ${n1(b.ci[1])}` : '–'}, extra || {}) : null;
const BOOKCOLS = [
  {h:'', f:r => esc(r.label)},
  {h:'n', f:r => r.n},
  {h:'raak %', f:r => n1(r.hit)},
  {h:'gem. %', f:r => `<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
  {h:'mediaan %', f:r => pc(r.med)},
  {h:'t', f:r => n2(r.t)},
  {h:'95% interval', f:r => r.ci}];
const draw = [];

/* -------------------------------------------------------------------- tabs */
const LENSNOTE = () => F.lens === 'trading'
  ? `De lens staat op <b>handel</b>: alleen namen waar een positie op is gegaan, met het
     rendement dat de broker werkelijk maakte — inclusief spread, instapmoment en een
     uitstap die soms met de hand gebeurde.`
  : `De lens staat op <b>onderzoek</b>: elke gerangschikte naam, of er geld op stond of
     niet, met het bord-rendement — de koersbeweging in de richting van het teken van
     <code>impact_sum</code>, zonder spread en zonder uitvoering.`;

function tabOverzicht() {
  const rows = rowsFor(), rk = rankRows(), days = byDay(rk);
  const perUnit = spread(rows.map(retOf));
  const rho = pooledRho(days, r=>r.impact_sum, mvOf);
  const ctl = pooledRho(days, r=>r.neg_runup, mvOf);
  const conv = convictionRho(rk, r=>r.impact_sum, mvOf);
  const closed = tradesFiltered(true);
  const pnl = closed.reduce((s,t)=>s+(t.pnl_usd||0), 0);
  const curve = curveRows(), daily = dailyRows();

  /* Per day: the mean of that day's names, scaled by how much of the equity the
     sizing rule would actually have deployed. Every day weighs the same, whatever
     its name count — which is the only way a 22-name day does not drown a 4-name one. */
  const dayRows = byDay(rows);
  const dayRets = dayRows.map(d => {
    const m = d.reduce((s,x)=>s+retOf(x),0)/d.length;
    return {date: d[0].run_date, n: d.length, mean: m,
            deployed: deployedPct(d.length), ret: m * deployedPct(d.length)/100};
  });
  const perDay = spread(dayRets.map(d=>d.ret));
  const total = compound(dayRets.map(d=>d.ret));
  const ctlDay = dayRows.map(d => d.reduce((s,x)=>s-(mvOf(x)??0),0)/d.length
                                  * deployedPct(d.length)/100);
  const eqStart = curve.length ? curve[0].equity : null;
  const eqEnd = curve.length ? curve[curve.length-1].equity : null;
  const eqRet = (eqStart && eqEnd) ? (eqEnd/eqStart - 1)*100 : null;

  let html = `<p class="lead">${LENSNOTE()}</p>`;
  html += tiles([
    {k: F.lens === 'trading' ? 'per positie' : 'per naam', v:pc(perUnit.mean),
     cls:sgn(perUnit.mean), s:`n=${perUnit.n}, sd ${n1(perUnit.sd)}, t=${n2(perUnit.t)}`},
    {k:'per dag', v:pc(perDay.mean), cls:sgn(perDay.mean),
     s:`${perDay.n} dagen, sd ${n1(perDay.sd)}${F.capOn?`, ${n1(dayRets.reduce((s,d)=>s+d.deployed,0)/Math.max(1,dayRets.length))}% belegd`:''}`},
    {k:'totaal, samengesteld', v:pc(total), cls:sgn(total),
     s: F.capOn ? `max ${F.capPct}% per naam` : 'gelijk gewogen, volledig belegd'},
    {k:'rekening', v:pc(eqRet), cls:sgn(eqRet),
     s:`${usd(eqStart)} → ${usd(eqEnd)}${pnl?`, P&L ${usd(pnl)}`:''}`},
    {k:'ρ rangschikking', v:n3(rho), s:`tegen ${n3(ctl)} voor de gratis controle`},
    {k:'ρ conviction', v:n3(conv), s:'voorspelt |impact| of het teken klopte'}]);

  html += `<div class="card"><h3>Drie niveaus van rendement, en de spreiding erin</h3>` +
    table([
      {h:'niveau', f:r=>esc(r.label)}, {h:'n', f:r=>r.n},
      {h:'gemiddeld', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
      {h:'mediaan', f:r=>pc(r.median)},
      {h:'sd', f:r=>n2(r.sd)},
      {h:'p25 … p75', f:r=>r.p25===undefined?'–':`${n1(r.p25)} … ${n1(r.p75)}`},
      {h:'slechtste', f:r=>`<span class="neg">${pc(r.min)}</span>`},
      {h:'beste', f:r=>`<span class="pos">${pc(r.max)}</span>`},
      {h:'raak %', f:r=>n1(r.hit)},
      {h:'t', f:r=>n2(r.t)},
      {h:'95% interval', f:r=>r.ci?`${n1(r.ci[0])} … ${n1(r.ci[1])}`:'–'}],
      [{label: F.lens === 'trading' ? 'per positie' : 'per naam', ...perUnit},
       {label:'per dag (boek)', ...perDay},
       {label:'gratis controle per dag', ...spread(ctlDay)}]) +
    `<small>De spreiding is het punt: op dit aantal waarnemingen is de standaarddeviatie
     per ${F.lens === 'trading' ? 'positie' : 'naam'} ${n1(perUnit.sd)} procentpunt tegen
     een gemiddelde van ${n1(perUnit.mean)}. Samengesteld over de periode:
     <b>${pc(total)}</b>${F.capOn ? ` bij max ${F.capPct}% per naam en ${F.grossPct}% bruto`
     : ' gelijk gewogen'}.</small></div>`;

  html += `<div class="card"><h3>Spreiding per ${F.lens === 'trading' ? 'positie' : 'naam'}</h3>
    ${legend([{color:css('--good'), label:'in de plus'}, {color:css('--bad'), label:'in de min'}])}
    ${chartBlock('c-hist', 210)}
    <small>Waar de staart zit. Eén naam in de rechterstaart kan het hele gemiddelde
    dragen; de tooltip noemt ze.</small></div>`;

  html += `<div class="card"><h3>Samengesteld rendement van het geselecteerde boek</h3>
    ${legend([{color:css('--s1'), label:'het boek onder deze filters'},
              {color:css('--s2'), label:'gratis controle: alles shorten'}])}
    ${chartBlock('c-cum', 250)}
    <small>Per dag het gemiddelde rendement van de namen die door de filters komen,
    ${F.capOn ? `geschaald naar wat de sizing-regel zou hebben ingelegd (max ${F.capPct}% per naam, bruto ${F.grossPct}%)`
    : 'gelijk gewogen en volledig belegd'}, samengesteld. Geen kosten.</small></div>`;

  html += `<div class="card"><h3>Equity, zoals de broker hem rapporteert</h3>
    ${chartBlock('c-equity', 230)}
    <small>De rekening zelf: alleen de periode volgt de filters, de inhoud niet — dit is
    wat er werkelijk gehandeld is.</small></div>`;
  html += `<div class="card"><h3>Gerealiseerde P&L per instapdag</h3>
    ${legend([{color:css('--good'), label:'winst'}, {color:css('--bad'), label:'verlies'}])}
    ${chartBlock('c-daypnl', 200)}</div>`;

  const pend = ALL.filter(r => passesFilters(r) && r.pending);
  const warn = [];
  if (pend.length) {
    const byd = [...new Set(pend.map(r=>r.run_date))].join(', ');
    warn.push(`${pend.length} namen (${esc(byd)}) zijn nog in afwikkeling: de reactiesessie
      is niet gesloten, dus op <code>close</code> hebben ze geen rendement en vallen ze uit
      elke grafiek. Zet uitstap op <code>pre_open</code> of <code>ext_early</code> om te
      zien waar ze nu staan. ${esc(pend.map(r=>r.ticker+' '+pc(r.mv_pre_open ?? r.mv_ext_early)).join(', '))}.`);
  }
  if (rho !== null && ctl !== null && rho <= ctl)
    warn.push(`De rangschikking (ρ=${n3(rho)}) verslaat de gratis controle
      <code>-run_up_20d_pct</code> (ρ=${n3(ctl)}) niet.`);
  if (perUnit.n < 25)
    warn.push(`n=${perUnit.n}. Het 95%-interval loopt van
      ${perUnit.ci ? n1(perUnit.ci[0])+'% tot '+n1(perUnit.ci[1])+'%' : '–'}.`);
  if (perUnit.n) {
    const top = rows.slice().sort((a,b)=>Math.abs(retOf(b))-Math.abs(retOf(a)))[0];
    const without = spread(rows.filter(r=>r!==top).map(retOf));
    warn.push(`Zonder de grootste enkele uitslag (${esc(top.ticker)} ${pc(retOf(top))})
      gaat het gemiddelde van ${pc(perUnit.mean)} naar ${pc(without.mean)}.`);
  }
  html += `<div class="card warnbox"><h3>Wat dit niet bewijst</h3><ul>` +
    warn.map(w=>`<li>${w}</li>`).join('') + `</ul></div>`;

  draw.push(() => {
    histChart(document.getElementById('c-hist'), {
      values: rows.map(retOf), labels: rows.map(r=>r.ticker), unit:'%', bins:9, height:210,
      labelY:'aantal namen'});
    let cum = 1, cumC = 1;
    const labels = [], book_ = [], ctl_ = [];
    dayRets.forEach((d,i) => {
      cum *= (1 + d.ret/100); cumC *= (1 + ctlDay[i]/100);
      labels.push(d.date.slice(5)); book_.push((cum-1)*100); ctl_.push((cumC-1)*100);
    });
    lineChart(document.getElementById('c-cum'), {
      x: labels, sub: dayRets.map(d=>`n=${d.n}`),
      series:[{label:'boek', color:css('--s1'), values:book_},
              {label:'controle', color:css('--s2'), values:ctl_}],
      zero:true, fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:250,
      tipX:i=>`${dayRets[i].date} · ${dayRets[i].n} namen · dag ${pc(dayRets[i].ret)}` +
              (F.capOn ? ` · ${n1(dayRets[i].deployed)}% belegd` : '')});
    lineChart(document.getElementById('c-equity'), {
      x: curve.map(p=>p.date.slice(5)),
      series:[{label:'equity', color:css('--s1'), values:curve.map(p=>p.equity)}],
      fmtY: v=>'$'+(v/1000).toFixed(1)+'k', fmtT: usd, height:230});
    barChart(document.getElementById('c-daypnl'), {
      items: daily.map(d => ({label:d.date.slice(5), v:d.pnl_usd, sub:`${d.n}×`,
        tip:`<b>${d.date}</b><br>${esc(d.symbols)}<br>inzet ${usd(d.notional_usd)}
             (${n1(d.gross_pct_of_equity)}% van equity)<br>P&amp;L ${usd(d.pnl_usd)}
             = ${pc(d.ret_on_notional_pct)} op de inzet`})),
      fmtY: usd, fmtT: usd, height:200});
  });
  return html;
}

function tabHandel() {
  const closed = tradesFiltered(true), all = tradesFiltered(false);
  let html = `<p class="lead">Elke ronde die de rekening echt deed, uit de fill-stroom
    gematcht: open tot weer vlak. Deelverkopen over meerdere dagen zijn één positie met
    een gewogen uitstap.</p>`;
  const g = (k) => { const v = closed.map(t=>t[k]).filter(x=>x!==null&&x!==undefined);
                     return v.length ? book(v) : null; };
  const pol = g('policy_gap_pct'), ex = g('exec_gap_pct');
  const act = book(closed.map(t=>t.ret_pct));
  const theo = book(closed.filter(t=>t.theo_ret_close_pct!==undefined&&t.theo_ret_close_pct!==null)
                          .map(t=>t.theo_ret_close_pct));
  html += tiles([
    {k:'werkelijk, per positie', v:pc(act.mean), cls:sgn(act.mean), s:`n=${act.n}`},
    {k:'theoretisch, zelfde namen', v:pc(theo.mean), cls:sgn(theo.mean),
     s:'bord-rendement slot→slot'},
    {k:'verschil beleid', v: pol ? pc(pol.mean) : '–', cls: pol ? sgn(pol.mean) : '',
     s:'instapmoment + spread + uitstaptiming'},
    {k:'verschil uitvoering', v: ex ? pc(ex.mean) : '–', cls: ex ? sgn(ex.mean) : '',
     s:'op het uur dat echt gesloten werd'}]);

  html += `<div class="card"><h3>Theoretisch tegen werkelijk</h3>
    ${legend([{color:css('--s1'), label:'amc'}, {color:css('--s2'), label:'bmo'},
              {color:css('--muted'), label:'y = x: uitvoering deed niets', dash:true}])}
    ${chartBlock('c-theo', 320)}
    <small>Boven de lijn kreeg de rekening méér dan de koersreeks belooft, eronder minder.
    Het theoretische been loopt van de slotkoers vóór de print naar de slotkoers erna; de
    echte instap is een marktorder rond 13:24 ET, dus het verschil bevat ook een halve
    handelsdag koersbeweging vóór die slotkoers.</small></div>`;

  const rows = [bookRow('alle afgeronde posities', act),
                bookRow('long', book(closed.filter(t=>t.side==='long').map(t=>t.ret_pct))),
                bookRow('short', book(closed.filter(t=>t.side==='short').map(t=>t.ret_pct))),
                bookRow('amc', book(closed.filter(t=>t.session==='amc').map(t=>t.ret_pct))),
                bookRow('bmo', book(closed.filter(t=>t.session==='bmo').map(t=>t.ret_pct))),
                bookRow('uitstap door stage E',
                        book(closed.filter(t=>t.exit_source==='stage E').map(t=>t.ret_pct))),
                bookRow('uitstap met de hand',
                        book(closed.filter(t=>t.exit_source==='manual').map(t=>t.ret_pct))),
                bookRow('theoretisch, zelfde posities', theo)].filter(Boolean);
  html += `<div class="card"><h3>Rendement per snede</h3>${table(BOOKCOLS, rows)}</div>`;
  html += `<div class="card"><h3>Rendement per positie</h3>
    ${legend([{color:css('--good'), label:'in de plus'}, {color:css('--bad'), label:'in de min'}])}
    ${chartBlock('c-trades', 230)}</div>`;

  const cols = [
    {h:'ticker', f:t=>`<b>${esc(t.symbol)}</b>`},
    {h:'sector', f:t=>esc((nameOfTrade(t)||{}).sector || '–')},
    {h:'kant', f:t=>t.side}, {h:'sessie', f:t=>t.session || '–'},
    {h:'impact', f:t=>n1(t.impact_sum)},
    {h:'in', f:t=>t.entry_utc.slice(5,16).replace('T',' ')},
    {h:'uit', f:t=>t.exit_utc ? t.exit_utc.slice(5,16).replace('T',' ') : 'open'},
    {h:'uren', f:t=>n1(t.hold_hours)},
    {h:'inzet', f:t=>usd(t.entry_notional_usd)},
    {h:'werkelijk', f:t=>`<span class="${sgn(t.ret_pct)}">${pc(t.ret_pct)}</span>`},
    {h:'theoretisch', f:t=>pc(t.theo_ret_close_pct)},
    {h:'verschil', f:t=>`<span class="${sgn(t.policy_gap_pct)}">${pc(t.policy_gap_pct)}</span>`},
    {h:'P&L', f:t=>`<span class="${sgn(t.pnl_usd)}">${usd(t.pnl_usd)}</span>`},
    {h:'uitstap', f:t=>`${t.exit_source||'–'}${t.exit_tif?' / '+t.exit_tif:''}`},
    {h:'fills uit', f:t=>`${t.n_exit_fills||0}${t.partial_exit_days>1?` (${t.partial_exit_days}d)`:''}`},
    {h:'spread in %', f:t=>n2(t.entry_spread_pct)}];
  html += `<div class="card"><h3>Alle posities</h3>${table(cols, all)}
    <small>Een <code>opg</code>- of <code>cls</code>-order dat niet kruiste laat de positie
    openstaan; dat is te zien aan de kolommen uren en fills uit.</small></div>`;

  draw.push(() => {
    scatterChart(document.getElementById('c-theo'), {
      points: closed.filter(t=>t.theo_ret_close_pct!==null&&t.theo_ret_close_pct!==undefined)
        .map(t => ({x:t.theo_ret_close_pct, y:t.ret_pct,
          color: t.session === 'amc' ? css('--s1') : css('--s2'), r:7,
          tip:`<b>${esc(t.symbol)}</b> ${t.side}, ${t.session||'?'}<br>
               theoretisch ${pc(t.theo_ret_close_pct)} → werkelijk ${pc(t.ret_pct)}<br>
               verschil ${pc(t.policy_gap_pct)} · uitstap ${t.exit_source}`})),
      diagonal:true, labelX:'theoretisch bord-rendement %', labelY:'werkelijk rendement %',
      fmtY: v=>v.toFixed(0)+'%', fmtX: v=>v.toFixed(0)+'%', height:320});
    barChart(document.getElementById('c-trades'), {
      items: closed.map(t => ({label:t.symbol, v:t.ret_pct, sub:t.entry_utc.slice(5,10),
        tip:`<b>${esc(t.symbol)}</b> ${t.side}, ${t.session||'?'}<br>
             ${pc(t.ret_pct)} · ${usd(t.pnl_usd)} · ${n1(t.hold_hours)} uur<br>
             theoretisch ${pc(t.theo_ret_close_pct)} (verschil ${pc(t.policy_gap_pct)})`})),
      fmtY: v=>v.toFixed(0)+'%', fmtT: pc, height:230});
  });
  return html;
}

function tabScore() {
  const rk = rankRows(), days = byDay(rk), rows = rowsFor();
  const rho = pooledRho(days, r=>r.impact_sum, mvOf);
  const ctl = pooledRho(days, r=>r.neg_runup, mvOf);
  const conv = convictionRho(rk, r=>r.impact_sum, mvOf);
  const hits = rk.filter(r=>r.impact_sum && (r.impact_sum>0)===(mvOf(r)>0)).length;
  const nz = rk.filter(r=>r.impact_sum).length;
  let html = `<p class="lead">${LENSNOTE()} Uitstapmoment: <code>${HZ_LABEL(F.horizon)}</code>.</p>`;
  html += tiles([
    {k:'ρ rangschikking', v:n3(rho), s:`${rk.length} namen over ${days.length} dagen`},
    {k:'ρ gratis controle', v:n3(ctl), s:'−run-up 20 dagen'},
    {k:'ρ conviction', v:n3(conv), s:'rang van |impact| tegen teken-raak'},
    {k:'teken raak', v:`${hits}/${nz}`, s: nz ? n1(100*hits/nz)+'% van de namen' : ''}]);

  const BK = [[0,1],[1,2],[2,3],[3,5],[5,8],[8,1e9]];
  const buckets = BK.map(([lo,hi]) => {
    const g = rows.filter(r => Math.abs(r.impact_sum) >= lo && Math.abs(r.impact_sum) < hi);
    return {label: `${lo}–${hi>1e8?'∞':hi}`, lo, ...book(g.map(retOf))};
  }).filter(b => b.n);
  html += `<div class="card"><h3>Rendement per score-emmer</h3>
    ${legend([{color:css('--s1'), label:'boven de drempel'},
              {color:css('--muted'), label:'eronder'}])}
    ${chartBlock('c-buckets', 230)}</div>`;
  html += `<div class="card"><h3>Score tegen realisatie</h3>
    ${legend([{color:css('--s1'), label:'amc'}, {color:css('--s2'), label:'bmo'},
              {color:css('--s2'), label:'kleinste-kwadratenlijn', dash:true}])}
    ${chartBlock('c-scatter', 330)}
    <small>Rechtsboven en linksonder klopt het teken. Een helling die door nul loopt is een
    rangschikking die niets sorteert; de r² zegt hoeveel van de spreiding hij dekt.</small></div>`;

  const perDay = days.map(d => {
    const fl = d.filter(r => retOf(r) !== null && retOf(r) !== undefined);
    return {run_date:d[0].run_date, n:d.length, rho:pooledRho([d], r=>r.impact_sum, mvOf),
            ctl:pooledRho([d], r=>r.neg_runup, mvOf), fn:fl.length,
            mean: fl.length ? book(fl.map(retOf)).mean : null};
  });
  html += `<div class="card"><h3>Per dag</h3>` +
    table([{h:'run', f:r=>r.run_date}, {h:'namen', f:r=>r.n},
           {h:'ρ impact_sum', f:r=>`<span class="${sgn(r.rho)}">${n3(r.rho)}</span>`},
           {h:'ρ controle', f:r=>n3(r.ctl)}, {h:'in het boek', f:r=>r.fn},
           {h:'gem. rendement', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`}], perDay) +
    `<small>Eén dag is een anekdote: op acht namen springt ρ van +0.9 naar −0.3 op ruis
     alleen.</small></div>`;
  html += `<div class="card"><h3>Long tegen short</h3>` + table(BOOKCOLS, [
    bookRow('short (impact < 0)', book(rows.filter(r=>r.impact_sum<0).map(retOf))),
    bookRow('long (impact > 0)', book(rows.filter(r=>r.impact_sum>0).map(retOf)))
  ].filter(Boolean)) + `</div>`;

  draw.push(() => {
    barChart(document.getElementById('c-buckets'), {
      items: buckets.map(b => ({label:b.label, v:b.mean, sub:`n=${b.n}`,
        color: b.lo >= (F.thrOn ? F.thr : D.conviction_floor) ? css('--s1') : css('--muted'),
        tip:`<b>|impact_sum| ${esc(b.label)}</b><br>n=${b.n}, trefkans ${n1(b.hit)}%<br>
             gemiddeld ${pc(b.mean)}, mediaan ${pc(b.median)}, t=${n2(b.t)}`})),
      fmtY: v=>v.toFixed(0)+'%', fmtT: pc, height:230});
    scatterChart(document.getElementById('c-scatter'), {
      points: rk.map(r => ({x:r.impact_sum, y:mvOf(r),
        color: r.session === 'amc' ? css('--s1') : css('--s2'),
        r: r.traded ? 7 : 4.5, open: !r.traded,
        tip:`<b>${esc(r.ticker)}</b> ${r.run_date} ${r.session}<br>${esc(r.sector||'')}<br>
             impact_sum ${n1(r.impact_sum)} → beweging ${pc(mvOf(r))}<br>
             ${r.traded ? 'gehandeld: '+pc(r.trade_ret_pct) : 'niet gehandeld'}`})),
      labelX:'impact_sum (punten van spot)', labelY:'gerealiseerde beweging %',
      fmtY: v=>v.toFixed(0)+'%', height:330});
  });
  return html;
}

const THR_GRID = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,6,7,8,10];
/* One sweep of the threshold, on a given subset. The filters other than the
   threshold still apply, so this answers "given what I am willing to trade, where
   does the cut belong" rather than a question about a different universe. */
function thresholdCurve(sel) {
  const base = ALL.filter(r => {
    if (F.session !== 'all' && r.session !== F.session) return false;
    if (F.sector !== 'all' && (r.sector||'onbekend') !== F.sector) return false;
    if (F.tradeOn) {
      const adv = advOf(r), short = r.impact_sum < 0;
      if (adv === null || adv < (short ? F.minShort : F.minLong)) return false;
      if (short && F.reqShort && r.shortable !== true) return false;
    }
    return retOf(r) !== null && retOf(r) !== undefined && (!sel || sel(r));
  });
  return THR_GRID.map(t => {
    const g = base.filter(r => Math.abs(r.impact_sum) >= t);
    const b = book(g.map(retOf));
    const days = byDay(g.filter(r => mvOf(r) !== null && mvOf(r) !== undefined));
    return {thr:t, ...b, rho: pooledRho(days, r=>r.impact_sum, mvOf),
            names: g.length, days: days.length};
  });
}

function tabDrempel() {
  const all = thresholdCurve(null);
  const amc = thresholdCurve(r=>r.session==='amc');
  const bmo = thresholdCurve(r=>r.session==='bmo');
  const advs = [...ALL].map(advOf).filter(x=>x!==null).sort((a,b)=>a-b);
  const med = advs.length ? advs[Math.floor(advs.length/2)] : 0;
  const thin = thresholdCurve(r=>(advOf(r)??0) < med);
  const thick = thresholdCurve(r=>(advOf(r)??0) >= med);
  const best = all.filter(r=>r.n>=5).sort((a,b)=>(b.mean??-99)-(a.mean??-99))[0];

  let html = `<p class="lead">De drempel is het enige dat in dit onderzoek ooit een
    familiegewijze correctie overleefde, en hij is met dezelfde data gekozen als waarmee
    hij wordt beoordeeld. Deze curve laat zien hoe gevoelig dat is: als het rendement
    langzaam oploopt met de drempel is er iets, als het één piek is op één waarde is dat
    een keuze uit ${THR_GRID.length} kandidaten.</p>`;
  if (best) html += tiles([
    {k:'beste drempel hier', v:`≥ ${n1(best.thr)}`, s:`n=${best.n}, ${n1(best.hit)}% raak`},
    {k:'rendement daar', v:pc(best.mean), cls:sgn(best.mean),
     s:`t=${n2(best.t)}, 95% ${best.ci?n1(best.ci[0])+' … '+n1(best.ci[1]):'–'}`},
    {k:'ρ daar', v:n3(best.rho), s:`${best.days} dagen`},
    {k:'nu ingesteld', v: F.thrOn ? `≥ ${n1(F.thr)}` : 'uit',
     s:'de rest van het dashboard gebruikt deze'}]);

  html += `<div class="card"><h3>Rendement tegen drempel</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-thr-ret', 250)}
    <small>De onderste regel per punt is n. Waar n onder ongeveer tien zakt is de lijn
    een enkele naam die beweegt.</small></div>`;
  html += `<div class="card"><h3>Rangschikking tegen drempel</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-thr-rho', 230)}
    <small>ρ binnen dagen gepoold. Een drempel snijdt namen weg, dus hoger is hier niet
    vanzelf beter: met drie namen per dag is een rangcorrelatie bijna betekenisloos.</small></div>`;
  html += `<div class="card"><h3>Drempel tegen dagomzet</h3>
    ${legend([{color:css('--s1'), label:`dun (< ${usdM(med)}/dag)`},
              {color:css('--s2'), label:`dik (≥ ${usdM(med)}/dag)`}])}
    ${chartBlock('c-thr-adv', 230)}
    <small>Als het rendement alleen in de dunne helft met de drempel meeloopt, koopt de
    drempel illiquiditeit en geen informatie.</small></div>`;

  const cols = [
    {h:'drempel', f:r=>`≥ ${n1(r.thr)}`},
    {h:'n', f:r=>r.n}, {h:'dagen', f:r=>r.days},
    {h:'raak %', f:r=>n1(r.hit)},
    {h:'gem. %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'t', f:r=>n2(r.t)},
    {h:'95% interval', f:r=>r.ci?`${n1(r.ci[0])} … ${n1(r.ci[1])}`:'–'},
    {h:'ρ', f:r=>n3(r.rho)},
    {h:'amc %', f:(r,i)=>''}, {h:'bmo %', f:(r,i)=>''}];
  const merged = all.map((r,i) => ({...r, amc:amc[i], bmo:bmo[i]}));
  html += `<div class="card"><h3>Per drempel</h3>` + table([
    {h:'drempel', f:r=>`≥ ${n1(r.thr)}`}, {h:'n', f:r=>r.n}, {h:'dagen', f:r=>r.days},
    {h:'raak %', f:r=>n1(r.hit)},
    {h:'gem. %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'t', f:r=>n2(r.t)},
    {h:'95% interval', f:r=>r.ci?`${n1(r.ci[0])} … ${n1(r.ci[1])}`:'–'},
    {h:'ρ', f:r=>n3(r.rho)},
    {h:'amc n', f:r=>r.amc.n}, {h:'amc %', f:r=>`<span class="${sgn(r.amc.mean)}">${pc(r.amc.mean)}</span>`},
    {h:'bmo n', f:r=>r.bmo.n}, {h:'bmo %', f:r=>`<span class="${sgn(r.bmo.mean)}">${pc(r.bmo.mean)}</span>`}
  ], merged) + `</div>`;

  draw.push(() => {
    const xs = THR_GRID.map(t=>'≥'+t);
    const sub = all.map(r=>'n='+r.n);
    lineChart(document.getElementById('c-thr-ret'), {
      x: xs, sub,
      series:[{label:'alles', color:css('--s1'), values:all.map(r=>r.mean ?? null)},
              {label:'amc', color:css('--s2'), values:amc.map(r=>r.n>=3?r.mean:null)},
              {label:'bmo', color:css('--s3'), values:bmo.map(r=>r.n>=3?r.mean:null)}],
      zero:true, fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:250,
      tipX:i=>`drempel ≥ ${THR_GRID[i]} · n=${all[i].n}`});
    lineChart(document.getElementById('c-thr-rho'), {
      x: xs,
      series:[{label:'alles', color:css('--s1'), values:all.map(r=>r.rho)},
              {label:'amc', color:css('--s2'), values:amc.map(r=>r.rho)},
              {label:'bmo', color:css('--s3'), values:bmo.map(r=>r.rho)}],
      zero:true, fmtY:v=>v.toFixed(2), fmtT:n3, height:230});
    lineChart(document.getElementById('c-thr-adv'), {
      x: xs, sub: thin.map((r,i)=>`${r.n}/${thick[i].n}`),
      series:[{label:'dun', color:css('--s1'), values:thin.map(r=>r.n>=3?r.mean:null)},
              {label:'dik', color:css('--s2'), values:thick.map(r=>r.n>=3?r.mean:null)}],
      zero:true, fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:230});
  });
  return html;
}

const med = xs => { const a = xs.filter(x=>x!==null&&x!==undefined).sort((x,y)=>x-y);
                    return a.length ? a[Math.floor(a.length/2)] : null; };
function tabSector() {
  const rows = rowsFor();
  const by = new Map();
  rows.forEach(r => { const k = r.sector || 'onbekend';
                      if (!by.has(k)) by.set(k, []); by.get(k).push(r); });
  const secs = [...by.entries()].map(([k,v]) => ({sector:k, ...book(v.map(retOf)),
      long: v.filter(r=>r.impact_sum>0).length, short: v.filter(r=>r.impact_sum<0).length,
      amc: book(v.filter(r=>r.session==='amc').map(retOf)),
      bmo: book(v.filter(r=>r.session==='bmo').map(retOf)),
      medAdv: med(v.map(advOf)), tilt: med(v.map(r=>r.retail_tilt)),
      churn: med(v.map(r=>r.churn_pct)), cap: med(v.map(r=>r.market_cap_usd)),
      price: med(v.map(r=>r.spot)), vol: med(v.map(r=>r.realised_vol_20d))}))
    .sort((a,b)=>b.n-a.n);
  let html = `<p class="lead">Sector en industrie komen van Yahoo, per ticker opgezocht en
    gecached. Met ${rows.length} namen over ${secs.length} sectoren is elke cel hier klein:
    lees dit als een plek om een vermoeden te halen, niet om er een te bevestigen.</p>`;
  html += `<div class="card"><h3>Rendement per sector</h3>
    ${chartBlock('c-sector', 250)}
    <small>Gesorteerd op aantal namen, niet op rendement — anders leest de volgorde zelf
    als een resultaat.</small></div>`;
  html += `<div class="card"><h3>Hoeveel consumentengeld er in de sector handelt</h3>
    ${chartBlock('c-tilt', 240)}
    <small><b>Wat dit is en niet is.</b> Er bestaat geen gratis bron voor eigendom —
    Yahoo's ownership zit achter een crumb, 13F is per kwartaal en alleen institutioneel.
    Dit is daarom een <i>proxy</i> uit vier dingen die allemaal dezelfde kant op wijzen:
    dagomzet gedeeld door marktkap (een naam die een groot deel van zichzelf per dag
    omzet wordt verhandeld, niet gehouden), kleine marktkap (institutionele mandaten
    hebben ondergrenzen), lage koers per aandeel, en realised vol. Elk als percentiel
    over de hele steekproef, gemiddeld tot 0–100. Lees het als een kanteling, niet als een
    meting; de componenten staan in de tabel en in de tooltip.</small></div>`;
  html += `<div class="card"><h3>Consumentenkanteling tegen rendement</h3>
    ${legend([{color:css('--s1'), label:'naam'},
              {color:css('--s2'), label:'kleinste-kwadratenlijn', dash:true}])}
    ${chartBlock('c-tiltret', 300)}
    <small>De vraag waar de indicator voor is: zit de edge in de namen waar consumenten
    handelen, of juist niet. Een helling door nul betekent dat het niets uitmaakt.</small></div>`;
  html += `<div class="card"><h3>Per sector</h3>` + table([
    {h:'sector', f:r=>esc(r.sector)}, {h:'n', f:r=>r.n},
    {h:'long/short', f:r=>`${r.long}/${r.short}`},
    {h:'raak %', f:r=>n1(r.hit)},
    {h:'gem. %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'t', f:r=>n2(r.t)},
    {h:'amc n', f:r=>r.amc.n}, {h:'amc %', f:r=>`<span class="${sgn(r.amc.mean)}">${pc(r.amc.mean)}</span>`},
    {h:'bmo n', f:r=>r.bmo.n}, {h:'bmo %', f:r=>`<span class="${sgn(r.bmo.mean)}">${pc(r.bmo.mean)}</span>`},
    {h:'mediane dagomzet', f:r=>usdM(r.medAdv)},
    {h:'consumenten­kanteling', f:r=>`<b>${n1(r.tilt)}</b>`},
    {h:'churn %/dag', f:r=>n2(r.churn)},
    {h:'mediane marktkap', f:r=>usdM(r.cap)},
    {h:'mediane koers', f:r=>r.price===null?'–':'$'+n2(r.price)},
    {h:'vol 20d', f:r=>n1(r.vol)}], secs) +
    `<small>Churn is de dagomzet als percentage van de marktkap. De kanteling is het
     gemiddelde percentiel van churn, kleine kap, lage koers en vol.</small></div>`;
  const inds = new Map();
  rows.forEach(r => { const k = r.industry || 'onbekend';
                      if (!inds.has(k)) inds.set(k, []); inds.get(k).push(r); });
  const ind = [...inds.entries()].map(([k,v]) => ({industry:k, ...book(v.map(retOf))}))
    .filter(r=>r.n>=3).sort((a,b)=>b.n-a.n);
  html += `<div class="card"><h3>Industrieën met drie of meer namen</h3>` + table([
    {h:'industrie', f:r=>esc(r.industry)}, {h:'n', f:r=>r.n},
    {h:'raak %', f:r=>n1(r.hit)},
    {h:'gem. %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`}], ind) + `</div>`;
  draw.push(() => {
    barChart(document.getElementById('c-sector'), {
      items: secs.map(s => ({label: shortSector(s.sector), v:s.mean, sub:`n=${s.n}`,
        color: css('--s1'),
        tip:`<b>${esc(s.sector)}</b><br>n=${s.n} (${s.long} long / ${s.short} short)<br>
             gemiddeld ${pc(s.mean)}, trefkans ${n1(s.hit)}%, t=${n2(s.t)}<br>
             mediane dagomzet ${usdM(s.medAdv)}`})),
      fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:250});
    barChart(document.getElementById('c-tilt'), {
      items: secs.filter(s=>s.tilt!==null).map(s => ({label: shortSector(s.sector),
        v:s.tilt, sub:`n=${s.n}`, color: css('--s3'),
        tip:`<b>${esc(s.sector)}</b> — kanteling ${n1(s.tilt)} van 100<br>
             churn ${n2(s.churn)}% van de marktkap per dag<br>
             mediane marktkap ${usdM(s.cap)} · koers $${n2(s.price)} · vol ${n1(s.vol)}<br>
             n=${s.n}, gemiddeld rendement ${pc(s.mean)}`})),
      fmtY:v=>v.toFixed(0), labelY:'percentiel 0–100', height:240});
    scatterChart(document.getElementById('c-tiltret'), {
      points: rows.filter(r=>r.retail_tilt!==null&&r.retail_tilt!==undefined).map(r => ({
        x:r.retail_tilt, y:retOf(r), r: r.traded ? 7 : 4.5, open: !r.traded,
        color: css('--s1'),
        tip:`<b>${esc(r.ticker)}</b> ${r.run_date} · ${esc(r.sector||'')}<br>
             kanteling ${n1(r.retail_tilt)} (churn ${n2(r.churn_pct)}%/dag,
             kap ${usdM(r.market_cap_usd)}, koers $${n2(r.spot)})<br>
             rendement ${pc(retOf(r))}`})),
      labelX:'consumentenkanteling (percentiel)', labelY:'rendement %',
      fmtY:v=>v.toFixed(0)+'%', height:300});
  });
  return html;
}

function tabTiming() {
  const H = D.horizons, rk = rankRows(), days = byDay(rk);
  const stat = (h, sel) => {
    const g = rk.filter(r => (!sel || sel(r)) && r['mv_'+h] !== null && r['mv_'+h] !== undefined
                          && Math.abs(r.impact_sum) >= (F.thrOn ? F.thr : 0));
    const b = book(g.map(r => r.impact_sum > 0 ? r['mv_'+h] : -r['mv_'+h]));
    const dd = byDay(rk.filter(r => (!sel||sel(r)) && r['mv_'+h] !== null && r['mv_'+h] !== undefined));
    return {...b, rho: pooledRho(dd, r=>r.impact_sum, r=>r['mv_'+h])};
  };
  const hourStat = (h, sel) => {
    const k = 'hr_' + h;
    const g = rk.filter(r => (!sel||sel(r)) && r[k] !== null && r[k] !== undefined
                          && Math.abs(r.impact_sum) >= (F.thrOn ? F.thr : 0));
    return g.length >= 3 ? book(g.map(r => r.impact_sum > 0 ? r[k] : -r[k])) : {n:g.length};
  };
  const rows = H.map(h => ({h, all:stat(h), amc:stat(h, r=>r.session==='amc'),
                            bmo:stat(h, r=>r.session==='bmo')}));
  let html = `<p class="lead">Waar op de klok het rendement zit. De instap ligt vast — de
    slotkoers vóór de print, 22:00 CET — dus alleen de uitstap beweegt. Tijden op de assen
    zijn CET. Alles vóór 15:30 CET is een prijs die bestond, geen omvang die kon handelen:
    deze bron levert geen volume buiten de reguliere sessie.</p>`;
  html += `<div class="card"><h3>Rendement per uitstapmoment</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-horizon', 250)}</div>`;
  html += `<div class="card"><h3>Per uitstapmoment</h3>` + table([
    {h:'moment (CET)', f:r=>`<code>${esc(r.h)}</code> ${HZ_CET[r.h]||''}`},
    {h:'n', f:r=>r.all.n}, {h:'ρ', f:r=>n3(r.all.rho)},
    {h:'raak %', f:r=>n1(r.all.hit)},
    {h:'boek %', f:r=>`<span class="${sgn(r.all.mean)}">${pc(r.all.mean)}</span>`},
    {h:'t', f:r=>n2(r.all.t)},
    {h:'amc n', f:r=>r.amc.n},
    {h:'amc %', f:r=>`<span class="${sgn(r.amc.mean)}">${pc(r.amc.mean)}</span>`},
    {h:'bmo n', f:r=>r.bmo.n},
    {h:'bmo %', f:r=>`<span class="${sgn(r.bmo.mean)}">${pc(r.bmo.mean)}</span>`}], rows) +
    `<small><code>ext_early</code> is een half uur nabeurs voor amc (22:30 CET) en de vroege
     voorbeurs voor bmo (14:00 CET) — het enige moment waar de twee sessies een andere klok
     hebben. <code>close</code> is de reguliere slotkoers, 22:00 CET, en is de huidige
     basis.</small></div>`;
  const grid = D.hour_grid;
  html += `<div class="card"><h3>Per uur, op de klok</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-hourly', 260)}
    <small>15:30 CET is de opening van de reactiesessie, 22:00 de slotkoers. Het gat tussen
    03:00 en 09:00 CET is de nacht: daar bestaat wel een prijs maar geen uitstap.</small></div>`;
  html += `<div class="card"><h3>De twee benen van de hold</h3>` + table([
    {h:'been', f:r=>esc(r.k)}, {h:'n', f:r=>r.v.n}, {h:'ρ', f:r=>n3(r.v.rho_impact_sum)},
    {h:'boek %', f:r=>`<span class="${sgn(r.v.floor_mean_ret_pct)}">${pc(r.v.floor_mean_ret_pct)}</span>`},
    {h:'t', f:r=>n2(r.v.floor_t)},
    {h:'gem. |beweging|', f:r=>n2(r.v.mean_abs_move_pct)}],
    Object.entries((D.stats.timing||{}).legs || {}).map(([k,v])=>({k,v}))) +
    `<small>Deze tabel komt uit de ongefilterde bouw en beweegt niet met de filters —
     de benen zijn gedefinieerd op de hele steekproef.</small></div>`;
  draw.push(() => {
    lineChart(document.getElementById('c-horizon'), {
      x: H.map(h=>HZ_CET[h]||h), sub: H,
      series:[{label:'alles', color:css('--s1'), values:rows.map(r=>r.all.n>=3?r.all.mean:null)},
              {label:'amc', color:css('--s2'), values:rows.map(r=>r.amc.n>=3?r.amc.mean:null)},
              {label:'bmo', color:css('--s3'), values:rows.map(r=>r.bmo.n>=3?r.bmo.mean:null)}],
      zero:true, fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:250,
      tipX:i=>`${H[i]} · ${HZ_CET[H[i]]||''} CET`});
    const a = grid.map(h=>hourStat(h)), am = grid.map(h=>hourStat(h, r=>r.session==='amc')),
          bm = grid.map(h=>hourStat(h, r=>r.session==='bmo'));
    lineChart(document.getElementById('c-hourly'), {
      x: grid.map(cetOfHour),
      series:[{label:'alles', color:css('--s1'), values:a.map(s=>s.n>=3?s.mean:null)},
              {label:'amc', color:css('--s2'), values:am.map(s=>s.n>=3?s.mean:null)},
              {label:'bmo', color:css('--s3'), values:bm.map(s=>s.n>=3?s.mean:null)}],
      zero:true, fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:260,
      tipX:i=>`${cetOfHour(grid[i])} CET · ${grid[i]}u na de instapkoers`});
  });
  return html;
}

function tabCapaciteit() {
  const rows = rowsFor();
  const daily = (D.stats.trading || {}).daily || [];
  const BK = [[0,1e6],[1e6,5e6],[5e6,25e6],[25e6,1e15]];
  const buckets = BK.map(([lo,hi]) => {
    const g = rows.filter(r => { const a = advOf(r); return a !== null && a >= lo && a < hi; });
    const lab = lo === 0 ? `< ${usdM(hi)}` : hi > 1e14 ? `≥ ${usdM(lo)}` : `${usdM(lo)}–${usdM(hi)}`;
    return {label:lab, ...book(g.map(retOf)),
            traded: g.filter(r=>r.traded).length};
  }).filter(b=>b.n);
  let html = `<p class="lead">Wat het boek aan kapitaal bezet, en wat de namen aan omzet
    dragen. De beste trade in deze steekproef zat in een naam die $170k per dag verhandelt;
    daar is een positie van $2.000 al een procent van de dagomzet.</p>`;
  html += `<div class="card"><h3>Inzet en opbrengst per dag</h3>` + table([
    {h:'dag', f:d=>d.date}, {h:'posities', f:d=>d.n},
    {h:'inzet', f:d=>usd(d.notional_usd)},
    {h:'% van equity', f:d=>n1(d.gross_pct_of_equity)},
    {h:'omzet', f:d=>usd(d.turnover_usd)},
    {h:'P&L', f:d=>`<span class="${sgn(d.pnl_usd)}">${usd(d.pnl_usd)}</span>`},
    {h:'op de inzet', f:d=>`<span class="${sgn(d.ret_on_notional_pct)}">${pc(d.ret_on_notional_pct)}</span>`},
    {h:'op de equity', f:d=>`<span class="${sgn(d.ret_on_equity_pct)}">${pc(d.ret_on_equity_pct)}</span>`},
    {h:'namen', f:d=>`<span class="t">${esc(d.symbols)}</span>`}], daily) +
    `<small>Omzet is wat er die dag verhandeld is, in en uit samen: de basis waarop
     transactiekosten drukken. Inzet is de bruto positie bij instap.</small></div>`;
  html += `<div class="card"><h3>Rendement op de inzet tegen wat er omging</h3>
    ${legend([{color:css('--good'), label:'dag in de plus'}, {color:css('--bad'), label:'dag in de min'},
              {color:css('--s2'), label:'kleinste-kwadratenlijn', dash:true}])}
    ${chartBlock('c-turnover', 230)}</div>`;
  html += `<div class="card"><h3>Rendement per liquiditeitsklasse</h3>
    ${chartBlock('c-adv', 230)}
    <small>Dagomzet van de naam zelf, prijs maal gemiddeld volume over 20 dagen. De
    uitvoeringsvloer van stage E staat op $200k; met de filter hierboven kun je zien wat er
    van het resultaat overblijft als je die vloer optrekt.</small></div>`;
  html += `<div class="card"><h3>Per klasse</h3>` + table(
    BOOKCOLS.concat([{h:'gehandeld', f:r=>r.traded}]),
    buckets.map(b=>bookRow(b.label, b, {traded:b.traded})).filter(Boolean)) + `</div>`;
  draw.push(() => {
    scatterChart(document.getElementById('c-turnover'), {
      points: daily.filter(d=>d.ret_on_notional_pct !== null).map(d => ({
        x:d.turnover_usd/1000, y:d.ret_on_notional_pct,
        color: d.pnl_usd >= 0 ? css('--good') : css('--bad'), r:7,
        tip:`<b>${d.date}</b><br>omzet ${usd(d.turnover_usd)}, inzet ${usd(d.notional_usd)}<br>
             ${pc(d.ret_on_notional_pct)} op de inzet · ${usd(d.pnl_usd)}`})),
      labelX:'verhandelde omzet die dag', labelY:'rendement op de inzet %',
      fmtY:v=>v.toFixed(0)+'%', fmtX:v=>'$'+v.toFixed(0)+'k', height:230});
    barChart(document.getElementById('c-adv'), {
      items: buckets.map(b => ({label:b.label, v:b.mean, sub:`n=${b.n}`, color:css('--s1'),
        tip:`<b>${esc(b.label)} dagomzet</b><br>n=${b.n}, trefkans ${n1(b.hit)}%<br>
             gemiddeld ${pc(b.mean)}, t=${n2(b.t)}<br>${b.traded} daadwerkelijk gehandeld`})),
      fmtY:v=>v.toFixed(0)+'%', fmtT:pc, height:230});
  });
  return html;
}

function tabKosten() {
  const costs = D.costs || [];
  const daily = new Map(((D.stats.trading||{}).daily || []).map(d=>[d.date, d]));
  const rows = rowsFor();
  const perDay = new Map();
  rows.forEach(r => { if (!perDay.has(r.run_date)) perDay.set(r.run_date, []);
                      perDay.get(r.run_date).push(r); });
  const merged = costs.map(c => {
    const g = perDay.get(c.run_date) || [];
    const b = g.length ? book(g.map(retOf)) : {n:0};
    const m = c.measured || {};
    const tokens = (m.tokens_in || 0) + (m.tokens_out || 0) || c.est_output_tokens;
    const money = daily.get(c.run_date);
    return {...c, tokens, measured_tokens: (m.tokens_in||m.tokens_out) ? tokens : null,
            usd: m.usd ?? null, note: m.note || '',
            in_book: b.n, mean: b.n ? b.mean : null,
            per_name: c.n_names ? tokens / c.n_names : null,
            pnl: money ? money.pnl_usd : null,
            ret_equity: money ? money.ret_on_equity_pct : null};
  });
  const anyMeasured = merged.some(r=>r.measured_tokens);
  let html = `<p class="lead">Wat een run kostte, naast wat hij opleverde. ${anyMeasured
    ? 'Gemeten tokens komen uit <code>data/costs.csv</code>.'
    : `<b>Er is nergens een tokenaantal vastgelegd</b>, dus dit is een proxy: de tekens die
       de run zelf op schijf schreef, gedeeld door vier, plus het aantal subagents. Vul
       <code>edge/performance/data/costs.csv</code>
       (<code>run_date,tokens_in,tokens_out,usd,note</code>) en die getallen worden gebruikt,
       met de proxy ernaast.`}</p>`;
  const withRet = merged.filter(r=>r.mean !== null);
  const fit = ols(withRet.map(r=>({x:r.tokens, y:r.mean})));
  const fitPer = ols(withRet.filter(r=>r.per_name).map(r=>({x:r.per_name, y:r.mean})));
  html += tiles([
    {k:'tokens per run (proxy)', v: merged.length
      ? Math.round(merged.reduce((s,r)=>s+r.tokens,0)/merged.length).toLocaleString('en-US') : '–',
     s:'gemiddeld over alle runs'},
    {k:'per naam', v: merged.filter(r=>r.per_name).length
      ? Math.round(merged.filter(r=>r.per_name).reduce((s,r)=>s+r.per_name,0)
        / merged.filter(r=>r.per_name).length).toLocaleString('en-US') : '–',
     s:'tokens gedeeld door namen in de run'},
    {k:'trend inzet → rendement', v: fit ? n2(fit.slope*1e5) : '–',
     s: fit ? `procentpunt per 100k tokens, r² ${n2(fit.r2)} (n=${fit.n})` : 'te weinig dagen'},
    {k:'gecorrigeerd per naam', v: fitPer ? n2(fitPer.slope*1e4) : '–',
     s: fitPer ? `per 10k tokens per naam, r² ${n2(fitPer.r2)}` : 'te weinig dagen'}]);
  html += `<div class="card"><h3>Inzet tegen dagrendement</h3>
    ${legend([{color:css('--s1'), label:'run'}, {color:css('--s2'),
              label:'kleinste-kwadratenlijn', dash:true}])}
    ${chartBlock('c-cost', 250)}
    <small>Meer tokens is meer namen en meer bevindingen. Als de lijn vlak of dalend is,
    koopt extra inzet geen rendement — en met ${withRet.length} dagen is dat nog geen van
    beide, alleen het begin van de meting.</small></div>`;
  html += `<div class="card"><h3>Per run</h3>` + table([
    {h:'run', f:r=>r.run_date}, {h:'namen', f:r=>r.n_names},
    {h:'hunters', f:r=>r.n_hunters}, {h:'bevindingen', f:r=>r.n_findings},
    {h:'tokens', f:r=>Math.round(r.tokens).toLocaleString('en-US') +
      (r.measured_tokens ? '' : ' <span class="meta">(proxy)</span>')},
    {h:'per naam', f:r=>r.per_name ? Math.round(r.per_name).toLocaleString('en-US') : '–'},
    {h:'usd', f:r=>r.usd === null ? '–' : usd(r.usd)},
    {h:'in het boek', f:r=>r.in_book},
    {h:'gem. rendement', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'P&L die dag', f:r=>`<span class="${sgn(r.pnl)}">${usd(r.pnl)}</span>`},
    {h:'notitie', f:r=>esc(r.note)}], merged) + `</div>`;
  draw.push(() => {
    scatterChart(document.getElementById('c-cost'), {
      points: withRet.map(r => ({x:r.tokens/1000, y:r.mean, r:7, color:css('--s1'),
        tip:`<b>${r.run_date}</b><br>${Math.round(r.tokens).toLocaleString('en-US')} tokens
             ${r.measured_tokens?'(gemeten)':'(proxy)'} over ${r.n_names} namen<br>
             ${r.n_hunters} hunters, ${r.n_findings} bevindingen<br>
             gemiddeld rendement ${pc(r.mean)} over ${r.in_book} namen in het boek`})),
      labelX:'tokens die run (duizend)', labelY:'gemiddeld rendement die dag %',
      fmtY:v=>v.toFixed(0)+'%', fmtX:v=>v.toFixed(0)+'k', height:250});
  });
  return html;
}

function tabLessons() {
  const L = D.stats.lessons;
  let html = `<p class="lead">De enige meting van <code>edge/LESSONS.md</code>: de hunter
    maakt zijn sommen eerst zonder het bestand, dat wordt bevroren als
    <code>pre_lessons</code>, daarna leest hij het en herziet. Beide getallen worden tegen
    dezelfde beweging gerangschikt.</p>`;
  if (!L.n) {
    html += `<div class="card warnbox"><h3>Nog geen meting</h3><p>${esc(L.coverage_note)}</p>
      <p>Zodra één run <code>diagnostics.impact_sum_pre_lessons</code> draagt, vult dit
      tabblad zich vanzelf: ρ vóór en ná, het boek vóór en ná, en de namen waar het bestand
      de som het hardst verzette.</p></div>`;
    return html;
  }
  const rows = rowsFor(r => r.impact_sum_pre_lessons !== null
                         && r.impact_sum_pre_lessons !== undefined);
  const days = byDay(rows);
  html += tiles([
    {k:'ρ vóór LESSONS.md', v:n3(pooledRho(days, r=>r.impact_sum_pre_lessons, mvOf)),
     s:`${rows.length} namen, ${days.length} dagen`},
    {k:'ρ ná LESSONS.md', v:n3(pooledRho(days, r=>r.impact_sum, mvOf)), s:'zelfde namen'},
    {k:'boek vóór', v:pc(book(rows.filter(r=>Math.abs(r.impact_sum_pre_lessons) >= F.thr)
        .map(r => r.impact_sum_pre_lessons > 0 ? mvOf(r) : -mvOf(r))).mean)},
    {k:'boek ná', v:pc(book(rows.map(retOf)).mean)}]);
  html += `<div class="card"><h3>Per naam</h3>` + table([
    {h:'run', f:r=>r.run_date}, {h:'ticker', f:r=>`<b>${esc(r.ticker)}</b>`},
    {h:'vóór', f:r=>n1(r.impact_sum_pre_lessons)}, {h:'ná', f:r=>n1(r.impact_sum)},
    {h:'verschil', f:r=>`<span class="${sgn(r.impact_sum-r.impact_sum_pre_lessons)}">${
      n1(r.impact_sum-r.impact_sum_pre_lessons)}</span>`},
    {h:'beweging', f:r=>pc(mvOf(r))}], rows) + `</div>`;
  return html;
}

function tabData() {
  const rows = ALL.filter(passesFilters);
  let html = `<p class="lead">Waar alles vandaan komt en wat er niet in zit.</p>`;
  html += `<div class="card"><h3>Herkomst</h3><ul>
    <li>Runs: ${D.runs.length}, van ${esc(D.runs[0])} tot ${esc(D.runs[D.runs.length-1])}</li>
    <li>Namen geprijsd: ${D.names.length} · na aftrek dubbele events: ${ALL.length}
        · onder de huidige filters: ${rows.length}</li>
    <li>Broker: ${D.account ? esc(D.account.endpoint) + (D.account.paper?' (paper)':' (live)') : '–'}</li>
    <li>Koersen: Yahoo dag- en 5-minutenbalken, gecached in <code>.cache/bars</code></li>
    <li>Sector en industrie: Yahoo search, gecached in <code>data/sectors.json</code></li>
    <li>Shortability: het bestand <code>alpaca-assets.json</code> van de run zelf waar dat
        bestaat, anders een <b>actuele</b> lookup — die zegt niets over wat drie weken
        geleden te lenen was</li>
    <li>Gebouwd: ${esc(D.generated_utc)}</li>
    ${D.broker_error ? `<li class="neg">Broker: ${esc(D.broker_error)}</li>` : ''}</ul></div>`;
  if (D.problems && D.problems.length)
    html += `<div class="card"><h3>Wat niet geprijsd kon worden (${D.problems.length})</h3>
      <div class="scroll"><ul>` + D.problems.map(p=>`<li>${esc(p)}</li>`).join('') +
      `</ul></div></div>`;
  html += `<div class="card"><h3>Namen onder de huidige filters</h3>` + table([
    {h:'run', f:r=>r.run_date}, {h:'ticker', f:r=>`<b>${esc(r.ticker)}</b>`},
    {h:'sector', f:r=>esc(r.sector||'–')}, {h:'sessie', f:r=>r.session},
    {h:'impact_sum', f:r=>n1(r.impact_sum)}, {h:'bevindingen', f:r=>r.n_findings},
    {h:'−run-up', f:r=>n1(r.neg_runup)}, {h:'dagomzet', f:r=>usdM(advOf(r))},
    {h:'short?', f:r=>r.shortable === true ? 'ja' : r.shortable === false ? 'nee' : '–'},
    {h:'beweging', f:r=>pc(mvOf(r))},
    {h:'bord-rendement', f:r=>`<span class="${sgn(boardOf(r))}">${pc(boardOf(r))}</span>`},
    {h:'kanteling', f:r=>n1(r.retail_tilt)},
    {h:'gehandeld', f:r=>r.traded ? `ja (${pc(r.trade_ret_pct)})` : '–'},
    {h:'status', f:r=>r.pending ? '<span class="meta">in afwikkeling</span>' : ''}], rows) +
    `<small>Ook in <code>edge/performance/data/names.csv</code> en <code>trades.csv</code>,
     ongefilterd, voor wie liever zelf rekent.</small></div>`;
  html += `<div class="card"><h3>Ververs dit dashboard</h3>
    <p>De knop rechtsboven werkt echt als de pagina geserveerd wordt:</p>
    <p><code>./edge/performance/update.sh --serve</code></p>
    <p>Geopend als bestand kan een pagina geen script draaien; de knop kopieert dan het
    commando. Zonder broker: <code>./edge/performance/update.sh --offline</code>. Met
    publiceren: <code>--publish</code>.</p></div>`;
  return html;
}

/* --------------------------------------------------------------- controls */
const SECTORS = [...new Set(ALL.map(r => r.sector || 'onbekend'))].sort();
function renderControls() {
  const c = document.getElementById('controls');
  const days = ALL.filter(r => inRange(r.run_date)).length;
  c.innerHTML = `
    <div class="ctlrow">
      <div class="ctl" title="Onderzoek = elke gerangschikte naam met het bord-rendement. Handel = alleen namen die een positie werden, met het rendement van de broker.">
        <label>lens</label>
        <span class="seg" id="seg-lens">
          <button data-v="research" aria-pressed="${F.lens==='research'}">onderzoek</button>
          <button data-v="trading" aria-pressed="${F.lens==='trading'}">handel</button>
        </span></div>
      <div class="ctl" title="Op welk moment de positie zou zijn gesloten. De instap ligt vast op de slotkoers vóór de print.">
        <label>uitstap</label>
        <select id="f-horizon">${D.horizons.map(h =>
          `<option value="${h}" ${h===F.horizon?'selected':''}>${h} · ${HZ_CET[h]||''} CET</option>`).join('')}
        </select></div>
      <div class="ctl" title="Welke runs meetellen. Verschuift ook de x-as van elke grafiek.">
        <label>periode</label>
        <span class="seg" id="seg-period">
          ${[['alles',0],['20d',20],['10d',10],['5d',5]].map(([lab,n]) =>
            `<button data-n="${n}" aria-pressed="${periodIs(n)}">${lab}</button>`).join('')}
        </span>
        <input type="date" id="f-from" value="${F.from}" min="${DATES[0]}" max="${DATES[DATES.length-1]}">
        <span class="dash">–</span>
        <input type="date" id="f-to" value="${F.to}" min="${DATES[0]}" max="${DATES[DATES.length-1]}">
      </div>
    </div>
    <div class="ctlrow">
      <div class="ctl ${F.thrOn?'':'off'}" title="Alleen namen waarvan |impact_sum| minstens deze waarde is. Aan betekent dat élke tabel en grafiek op de pagina alleen die namen gebruikt.">
        <label class="sw"><input type="checkbox" id="f-thron" ${F.thrOn?'checked':''}>
          <b>drempel</b> |impact_sum| ≥</label>
        <input type="number" id="f-thr" step="0.5" min="0" max="20" value="${F.thr}">
        <input type="range" id="f-thrr" step="0.5" min="0" max="12" value="${F.thr}">
      </div>
      <div class="ctl ${F.tradeOn?'':'off'}" title="Namen die te dun verhandeld worden of niet te lenen zijn, eruit. De vloer voor shorts ligt hoger, want een short heeft omvang én een borrow nodig.">
        <label class="sw"><input type="checkbox" id="f-tradeon" ${F.tradeOn?'checked':''}>
          <b>verhandelbaar</b></label>
        <label>long ≥</label><input type="number" id="f-minlong" step="100000" min="0" value="${F.minLong}">
        <label>short ≥</label><input type="number" id="f-minshort" step="100000" min="0" value="${F.minShort}">
        <label class="sw"><input type="checkbox" id="f-reqshort" ${F.reqShort?'checked':''}> alleen leenbaar</label>
      </div>
      <div class="ctl ${F.capOn?'':'off'}" title="Simuleert de sizing-regel: een bruto budget gelijk verdeeld over de namen van de dag, met een plafond per naam. Uit = gelijk gewogen en altijd volledig belegd.">
        <label class="sw"><input type="checkbox" id="f-capon" ${F.capOn?'checked':''}>
          <b>positiecap</b> max</label>
        <input type="number" id="f-cappct" step="1" min="1" max="100" value="${F.capPct}">
        <label>% per naam, bruto</label>
        <input type="number" id="f-grosspct" step="5" min="10" max="200" value="${F.grossPct}">
        <label>%</label>
      </div>
      <div class="ctl" title="amc rapporteert na de slotbel, bmo vóór de opening. De twee gedragen zich meetbaar anders.">
        <label>sessie</label>
        <select id="f-session">${['all','amc','bmo'].map(x =>
          `<option value="${x}" ${x===F.session?'selected':''}>${x==='all'?'alle':x}</option>`).join('')}
        </select></div>
      <div class="ctl" title="Sector volgens Yahoo, per ticker opgezocht.">
        <label>sector</label>
        <select id="f-sector"><option value="all">alle</option>${SECTORS.map(x =>
          `<option value="${esc(x)}" ${x===F.sector?'selected':''}>${esc(x)}</option>`).join('')}
        </select></div>
      <button class="btn small" id="f-help" aria-expanded="false">? uitleg</button>
      <button class="btn small" id="f-reset">herstel</button>
    </div>
    <div class="help" id="helpbox" hidden>
      <h3>Wat de knoppen doen</h3>
      <dl>
        <dt>lens</dt><dd><b>onderzoek</b> rekent met elke gerangschikte naam en het
          <i>bord-rendement</i>: de koersbeweging in de richting van het teken van
          <code>impact_sum</code>, zonder spread, zonder uitvoering. <b>handel</b> houdt
          alleen namen over die een echte positie werden en gebruikt het rendement dat de
          broker maakte. Het verschil tussen die twee is wat uitvoering kostte.</dd>
        <dt>uitstap</dt><dd>Acht momenten, van een half uur na de print tot de slotkoers
          van de reactiesessie. De instap staat vast op de slotkoers vóór de print, dus dit
          verandert alleen waar je verkoopt. Alles vóór 15:30 CET is een prijs die bestond,
          geen omvang die kon handelen.</dd>
        <dt>periode</dt><dd>Welke runs meedoen. De knoppen nemen de laatste N handelsdagen
          uit de archieven; de twee datumvelden zetten een eigen venster. Elke grafiek
          volgt: dit is ook de x-as.</dd>
        <dt>drempel</dt><dd>De conviction-floor. Alleen namen met |impact_sum| ≥ deze
          waarde tellen mee — in élke tabel en grafiek, niet alleen in het overzicht.
          Uit is de volledige steekproef. De config staat op
          ${D.conviction_floor}; het tabblad <b>Drempel</b> laat zien wat andere waarden
          zouden hebben gedaan.</dd>
        <dt>verhandelbaar</dt><dd>Twee omzetvloeren en een borrow-check. Een naam met te
          weinig dagomzet kun je niet vullen zonder de koers te bewegen, en een short die
          niemand uitleent kun je helemaal niet doen. Daarom staat de shortvloer standaard
          hoger dan de longvloer.</dd>
        <dt>positiecap</dt><dd>De sizing-regel van stage E, nagerekend: het bruto budget
          gelijk verdeeld over de namen van die dag, met een plafond per naam. Bij drie
          namen en 33% is de rekening voor 99% belegd, bij één naam voor 33%, bij tien
          namen voor 100% met 10% per naam. Uit betekent gelijk gewogen en altijd volledig
          belegd — dat is het onderzoeksgetal, niet wat een rekening doet.</dd>
        <dt>sessie en sector</dt><dd>amc rapporteert na de slotbel, bmo vóór de opening; op
          deze steekproef gedragen ze zich tegengesteld. Sector komt van Yahoo.</dd>
      </dl>
      <p><b>Drie rendementen, en ze zijn niet hetzelfde.</b> Per positie is het gemiddelde
      van losse trades, met een spreiding die hier groter is dan het gemiddelde. Per dag
      weegt elke dag even zwaar, ongeacht hoeveel namen erin zaten. Totaal is samengesteld
      over de periode en is het enige getal dat een rekening ook echt ziet.</p>
    </div>`;
  const on = (id, ev, fn) => { const e = document.getElementById(id);
                               if (e) e.addEventListener(ev, fn); };
  document.querySelectorAll('#seg-lens button').forEach(b =>
    b.addEventListener('click', () => { F.lens = b.dataset.v; redraw(); }));
  document.querySelectorAll('#seg-period button').forEach(b =>
    b.addEventListener('click', () => { setPeriod(+b.dataset.n); redraw(); }));
  on('f-from','change', e => { F.from = e.target.value; redraw(); });
  on('f-to','change', e => { F.to = e.target.value; redraw(); });
  on('f-horizon','change', e => { F.horizon = e.target.value; redraw(); });
  on('f-thron','change', e => { F.thrOn = e.target.checked; redraw(); });
  on('f-thr','change', e => { F.thr = +e.target.value; F.thrOn = true; redraw(); });
  on('f-thrr','input', e => { F.thr = +e.target.value; F.thrOn = true; redraw(); });
  on('f-tradeon','change', e => { F.tradeOn = e.target.checked; redraw(); });
  on('f-minlong','change', e => { F.minLong = +e.target.value; redraw(); });
  on('f-minshort','change', e => { F.minShort = +e.target.value; redraw(); });
  on('f-reqshort','change', e => { F.reqShort = e.target.checked; redraw(); });
  on('f-capon','change', e => { F.capOn = e.target.checked; redraw(); });
  on('f-cappct','change', e => { F.capPct = +e.target.value; F.capOn = true; redraw(); });
  on('f-grosspct','change', e => { F.grossPct = +e.target.value; F.capOn = true; redraw(); });
  on('f-session','change', e => { F.session = e.target.value; redraw(); });
  on('f-sector','change', e => { F.sector = e.target.value; redraw(); });
  on('f-reset','click', () => { Object.assign(F, DEFAULTS); redraw(); });
  on('f-help','click', e => {
    const box = document.getElementById('helpbox');
    box.hidden = !box.hidden;
    e.target.setAttribute('aria-expanded', String(!box.hidden));
  });
}
function periodIs(n) {
  const full = F.from === DATES[0] && F.to === DATES[DATES.length-1];
  if (!n) return full;
  // A preset wider than the archive IS the full range, and only "alles" should light
  // up for it — otherwise every preset reads as active on a short history.
  if (n >= DATES.length) return false;
  return F.from === DATES[DATES.length-n] && F.to === DATES[DATES.length-1] && !full;
}
function setPeriod(n) {
  F.to = DATES[DATES.length-1];
  F.from = n ? (DATES[Math.max(0, DATES.length-n)] || DATES[0]) : DATES[0];
}
/* Rebuild the controls too: the checkboxes carry state that a reset has to show. */
function redraw() { renderControls(); refresh(); }

function filterLine() {
  const kept = ALL.filter(passesFilters);
  const withRet = kept.filter(r => retOf(r) !== null && retOf(r) !== undefined);
  const pend = kept.filter(r => r.pending).length;
  const nDays = new Set(withRet.map(r=>r.run_date)).size;
  const bits = [F.lens === 'trading' ? 'lens handel' : 'lens onderzoek'];
  bits.push(F.thrOn ? `|impact_sum| ≥ ${F.thr}` : 'geen drempel');
  if (F.tradeOn) bits.push(`long ≥ ${usdM(F.minLong)}/dag, short ≥ ${usdM(F.minShort)}/dag` +
    (F.reqShort ? ', alleen leenbaar' : ''));
  if (F.capOn) bits.push(`max ${F.capPct}% per naam, bruto ${F.grossPct}%`);
  if (F.session !== 'all') bits.push(F.session);
  if (F.sector !== 'all') bits.push(F.sector);
  bits.push(`uitstap ${F.horizon} (${HZ_CET[F.horizon]} CET)`);
  bits.push(`${F.from} t/m ${F.to}`);
  document.getElementById('filterline').innerHTML =
    `${esc(bits.join(' · '))} — <b>${withRet.length}</b> namen over ${nDays} dagen` +
    (pend ? `, ${pend} nog in afwikkeling` : '');
}

/* ------------------------------------------------------------------- boot */
const TABS = [['Overzicht',tabOverzicht], ['Handel',tabHandel], ['Score',tabScore],
              ['Drempel',tabDrempel], ['Sector',tabSector], ['Timing',tabTiming],
              ['Capaciteit',tabCapaciteit], ['Kosten',tabKosten], ['Lessons',tabLessons],
              ['Data',tabData]];
let active = 0;
const nav = document.getElementById('tabs'), panels = document.getElementById('panels');
TABS.forEach(([name], i) => {
  const b = document.createElement('button');
  b.textContent = name; b.setAttribute('role','tab');
  b.setAttribute('aria-selected', i===0 ? 'true' : 'false');
  b.onclick = () => { active = i; refresh(); };
  nav.appendChild(b);
  const s = document.createElement('section'); s.hidden = i !== 0;
  panels.appendChild(s);
});
function refresh() {
  [...nav.children].forEach((b,j) => b.setAttribute('aria-selected', j===active ? 'true':'false'));
  [...panels.children].forEach((s,j) => s.hidden = j !== active);
  filterLine();
  draw.length = 0;
  panels.children[active].innerHTML = TABS[active][1]();
  draw.forEach(fn => fn());
}
document.getElementById('stamp').textContent =
  `gebouwd ${D.generated_utc} · ${D.runs.length} runs · ${D.names.length} namen · ` +
  `${D.trades.filter(t=>t.closed).length} afgeronde posities · ` +
  `conviction-floor uit de config ${D.conviction_floor}`;
document.getElementById('theme').onclick = () => {
  const now = document.documentElement.getAttribute('data-theme');
  const dark = now ? now === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
  refresh();
};
/* The refresh button. Served by serve.py it rebuilds for real; opened as a file it
   cannot run anything, so it hands over the command instead of pretending. */
const CMD = './edge/performance/update.sh';
document.getElementById('refresh').onclick = async (e) => {
  const btn = e.target, log = document.getElementById('refreshlog');
  btn.disabled = true; btn.textContent = 'bezig…';
  log.hidden = false; log.textContent = 'ledger en dashboard opnieuw bouwen…';
  try {
    const r = await fetch('rebuild', {method:'POST'});
    const j = await r.json();
    log.textContent = j.log || '(geen uitvoer)';
    if (j.ok) { log.textContent += '\nklaar — pagina wordt herladen'; setTimeout(()=>location.reload(), 900); return; }
  } catch (err) {
    log.textContent = `Deze pagina is als bestand geopend, dus de knop kan zelf niets draaien.\n\n` +
      `Draai in de repo-root:\n    ${CMD}\n\nOf serveer hem, dan werkt deze knop wel:\n` +
      `    ${CMD} --serve`;
    try { await navigator.clipboard.writeText(CMD + ' --serve');
          log.textContent += '\n\n(commando naar het klembord gekopieerd)'; } catch (_) {}
  }
  btn.disabled = false; btn.textContent = 'Ververs';
};
let rt;
addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(refresh, 150); });
renderControls();
refresh();
</script>
</body>
</html>
"""



def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=str(DATA / "ledger.json"))
    ap.add_argument("--out", default=str(ROOT / "edge" / "performance" / "dashboard.html"))
    a = ap.parse_args()

    led = json.loads(Path(a.ledger).read_text(encoding="utf-8"))
    # `</script>` inside the payload would close the tag it is embedded in.
    blob = json.dumps(led, separators=(",", ":")).replace("</", "<\\/")
    html = HTML.replace("__LEDGER__", blob)
    Path(a.out).write_text(html, encoding="utf-8")
    print(f"wrote {a.out}  ({len(html.encode())/1024:.0f} kB, {len(led['names'])} names, "
          f"{len(led['trades'])} positions)")


if __name__ == "__main__":
    main()
