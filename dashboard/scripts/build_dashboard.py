#!/usr/bin/env python3
"""Render dashboard/dashboard.html from data/ledger.json.

One self-contained file: no CDN, no build step, no network. Open it from disk, or
serve it with `dashboard/scripts/serve.py` and the page's own refresh
button rebuilds for real.

The page filters and recomputes client-side — the lens (research or money), the
conviction threshold, the tradability floors, the session and the sector all
re-derive every statistic on the page from the rows in the ledger. That is
deliberate: a threshold you cannot move is a threshold you cannot test.

    python3 dashboard/scripts/build_dashboard.py
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dashboard" / "data"

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
  /* A filled control is not a chart line. --s1 is tuned to read as a series on
     the plane; white on it is 4.4:1 light and 3.6:1 dark, which fails AA both
     ways. So the filled state gets its own pair, darker in light mode and
     dark-on-bright in dark mode, and the series colour stays untouched. */
  --fill:#1a5fb4; --on-fill:#ffffff;
  --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --plane:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,0.10);
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --good:#0ca30c; --bad:#d03b3b;
    --fill:#3987e5; --on-fill:#0b0b0b;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --plane:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,0.10);
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --good:#0ca30c; --bad:#d03b3b;
  --fill:#3987e5; --on-fill:#0b0b0b;
}
* { box-sizing:border-box; }
/* The parts of the page the stylesheet did not draw still carry the design. A
   1px UA outline is invisible on the dark plane, and this page is operated from
   the keyboard as much as the mouse. */
:focus-visible { outline:2px solid var(--s1); outline-offset:2px; border-radius:4px; }
::selection { background:var(--s1); color:#fff; }
.scroll { scrollbar-width:thin; scrollbar-color:var(--axis) transparent; }
.scroll::-webkit-scrollbar { width:10px; height:10px; }
.scroll::-webkit-scrollbar-thumb {
  background:var(--axis); border-radius:6px; border:2px solid var(--surface);
}
.scroll::-webkit-scrollbar-track { background:transparent; }
/* Touch. A 30px segment is a mouse target; a finger needs 44. */
@media (pointer:coarse) {
  .seg button, nav button, .btn { min-height:44px; }
}
@media (prefers-reduced-motion:reduce) {
  * { transition-duration:0.01ms !important; animation-duration:0.01ms !important; }
}
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
/* Een regel van 110 tekens leest niet. De tabellen mogen de volle breedte
   hebben, de lopende tekst erboven niet. */
p.lead { color:var(--ink); max-width:74ch; }
.card > p, .card > ul { max-width:82ch; }
small, .meta { color:var(--muted); font-size:12.5px; }
.muted { color:var(--muted); }
a { color:var(--s1); }
button, select, input { font:inherit; }
.btn {
  background:var(--surface); color:var(--ink); border:1px solid var(--ring);
  border-radius:8px; padding:6px 12px; cursor:pointer;
}
.btn:hover { border-color:var(--axis); }
.btn.primary { background:var(--fill); color:var(--on-fill); border-color:transparent; }
.btn[disabled] { opacity:.55; cursor:progress; }
/* De markt is de bovenste as. Hij staat boven de tabbladen en niet ertussen,
   want een markt kiezen en een analyse kiezen zijn niet dezelfde handeling. */
.marketbar { display:flex; flex-wrap:wrap; gap:6px; margin:14px 0 0; }
.marketbar button {
  display:flex; flex-direction:column; gap:1px; text-align:left; cursor:pointer;
  background:var(--surface); color:var(--ink2); border:1px solid var(--ring);
  border-radius:10px; padding:7px 13px;
}
.marketbar button:hover { border-color:var(--axis); }
.marketbar button[aria-pressed="true"] {
  background:var(--fill); color:var(--on-fill); border-color:transparent;
}
.marketbar .mk { font-size:14px; font-weight:600; }
.marketbar .mc { font-size:11.5px; opacity:.8; font-variant-numeric:tabular-nums; }
/* De rij is de index: de tabbladen staan in groepen met hun groepsnaam erboven,
   zodat twintig tabbladen niet als één ongesorteerde reeks lezen. Het label is
   een opschrift en geen knop. */
nav { display:flex; flex-wrap:wrap; gap:2px 16px; margin:10px 0 6px; align-items:flex-end;
      border-bottom:1px solid var(--grid); }
.tabgroup { display:flex; flex-wrap:wrap; gap:2px; align-items:flex-end; }
.tabgroup .gl {
  width:100%; font-size:10.5px; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted); padding:0 4px 2px;
}
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
/* `display:flex` above beats the browser's own rule for [hidden], so hiding the
   filter bar on a market tab needs saying here or it silently does nothing. */
.controls[hidden], .filterline[hidden] { display:none; }
/* The market tabs hide the bar above and carry their own, so it has to look
   like that bar and not like a card with two buttons in it. */
.mctl {
  display:flex; flex-wrap:wrap; gap:10px 18px; align-items:center;
  padding:0 0 12px; margin:0 0 4px; border-bottom:1px solid var(--grid);
}
.mctl .hint { font-size:12.5px; color:var(--muted); max-width:62ch; }
.ctl { display:flex; align-items:center; gap:7px; }
.ctl > label { font-size:12.5px; color:var(--muted); }
.seg { display:inline-flex; border:1px solid var(--ring); border-radius:8px; overflow:hidden; }
.seg button {
  background:var(--surface); border:none; color:var(--ink2); padding:5px 11px; cursor:pointer;
  border-right:1px solid var(--ring); font-size:13.5px;
}
.seg button:last-child { border-right:none; }
.seg button[aria-pressed="true"] { background:var(--fill); color:var(--on-fill); font-weight:600; }
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
.badge { font-size:11.5px; color:var(--good); border:1px solid var(--good);
         border-radius:999px; padding:1px 8px; }
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
/* hypothesis register: a verdict is a chip, so the eye finds the ones that moved */
.hyp { border-top:1px solid var(--grid); padding:14px 0; }
.hyp:last-child { border-bottom:1px solid var(--grid); }
.hyp h4 { margin:0 0 3px; font-size:14.5px; font-weight:600; display:flex; flex-wrap:wrap;
          gap:9px; align-items:baseline; }
.hyp .claim { color:var(--ink2); font-size:13.5px; margin:0 0 8px; max-width:78ch; }
.hyp .why { color:var(--muted); font-size:12.5px; margin:7px 0 0; max-width:78ch; }
.chip { font-family:var(--mono); font-size:10px; letter-spacing:.06em; text-transform:uppercase;
        padding:2px 7px; border-radius:3px; border:1px solid currentColor; white-space:nowrap; }
.c-yes  { color:var(--good); }
.c-no   { color:var(--muted); }
.c-anti { color:var(--bad); }
.c-thin { color:var(--muted); opacity:.75; }
.c-maybe { color:var(--warn); }
.hyp table { margin-top:6px; }
.warn { border-left:3px solid var(--warn); background:var(--surface); padding:11px 15px;
        border-radius:0 4px 4px 0; margin:12px 0; font-size:13.5px; color:var(--ink2); }
.warn b { color:var(--ink); }
code { font-family:var(--mono); font-size:12.5px; background:var(--plane); padding:1px 5px; border-radius:5px; }
ul { color:var(--ink2); max-width:80ch; }
li { margin:4px 0; }
.log { font-family:var(--mono); font-size:12px; white-space:pre-wrap; color:var(--ink2);
       max-height:240px; overflow:auto; margin-top:8px; }
.log a { color:var(--s1); }
.log .row { white-space:normal; display:flex; flex-wrap:wrap; gap:6px; align-items:center;
            margin-top:8px; }
.log input { background:var(--surface); color:var(--ink); border:1px solid var(--ring);
             border-radius:7px; padding:4px 7px; font:12px var(--mono); min-width:260px; }
.badge.ci { color:var(--ink2); border-color:var(--ring); }
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
    <span class="badge" id="served" hidden></span>
    <button class="btn primary" id="refresh">Ververs</button>
    <button class="btn" id="theme">donker / licht</button>
  </div>
</header>
<div class="log" id="refreshlog" hidden></div>

<!-- Markt, dan tabblad, dan filters. Dat is ook de volgorde van de beslissing,
     en op een telefoon duwde de filterbalk de marktkiezer anders een heel scherm
     naar beneden: de bovenste as stond onder de onderste. -->
<div class="marketbar" id="marketbar" role="group" aria-label="markt"></div>
<nav id="tabs" role="tablist"></nav>

<div class="controls" id="controls"></div>
<div class="filterline" id="filterline"></div>
<div id="panels"></div>
<div class="tip" id="tip"></div>
</div>

<script id="ledger" type="application/json">__LEDGER__</script>
<script id="markets" type="application/json">__MARKETS__</script>
<script id="v2" type="application/json">__V2__</script>
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
const HZ_CET = {strategy:'amc 15:30 / bmo 20:00',
                ext_early:'22:30 / 14:00', pre_open:'15:25', open:'15:30', m15:'15:45',
                m30:'16:00', m60:'16:30', midday:'18:00', close:'22:00'};
/* The exit the strategy aims at is not one moment: amc goes into the opening print
   and bmo four and a half hours later. `strategy` resolves per session in the ledger
   and is carried as a horizon so every tab reads it the same way as the rest. It is
   the default, because the book is what the page is about; the fixed horizons stay
   in the list so any of them can still be swept. */
const HORIZONS = ['strategy', ...(D.horizons || [])];
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
  lens: 'research', horizon: 'strategy',
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
       <code>dashboard/data/costs.csv</code>
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
  let html = `<p class="lead">De enige meting van <code>researcher_us/LESSONS.md</code>: de hunter
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
    `<small>Ook in <code>dashboard/data/names.csv</code> en <code>trades.csv</code>,
     ongefilterd, voor wie liever zelf rekent.</small></div>`;
  const repo = (D.build || {}).repo || '';
  html += `<div class="card"><h3>Ververs dit dashboard</h3>
    <p>De knop rechtsboven werkt op twee manieren, en zegt zelf in welke hij staat.</p>
    <p><b>Op je eigen machine.</b> Eén keer per sessie
    <code>./dashboard/update.sh --serve-bg</code>, en de knop werkt — ook in dit bestand
    van schijf. Dat start een rebuilder op <code>127.0.0.1:8765</code> en geeft je je
    shell terug; de pagina zoekt die server bij het laden en zet er <b>live</b> naast.
    Een pagina die als bestand is geopend mag zelf geen script draaien — een
    browserregel, geen instelling — maar praten met een server die al draait mag wel.</p>
    <p><b>Als opgehaalde pagina.</b> Dan is er geen machine om op te bouwen, en de knop
    start de workflow <code>dashboard.yml</code>${repo ? ' in ' + esc(repo) : ''} in
    plaats daarvan: GitHub Actions herbouwt de ledger, commit hem en publiceert deze
    pagina opnieuw. Er staat dan <b>CI</b> naast de knop. Een klik zonder token opent de
    workflow, waar dezelfde run één klik is; met een token (alleen <i>Actions: read and
    write</i>, bewaard in deze browser) doet de knop het zelf en herlaadt als de run
    klaar is. De workflow draait sowieso op een schema.</p>
    <p>Andere vormen: <code>--serve</code> houdt de server op de voorgrond,
    <code>--offline</code> slaat de broker over, <code>--fresh</code> gooit de
    koerscache weg, <code>--publish</code> commit en pusht.</p></div>`;
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
      <div class="ctl" title="Op welk moment de positie zou zijn gesloten. De optie strategie is niet één moment: amc gaat op de opening (15:30 CET), bmo om 20:00 CET. De instap ligt vast op de slotkoers vóór de print, behalve op het tabblad Instap.">
        <label>uitstap</label>
        <select id="f-horizon">${HORIZONS.map(h =>
          `<option value="${h}" ${h===F.horizon?'selected':''}>${h==='strategy'?'strategie':h} · ${HZ_CET[h]||''}${h==='strategy'?' CET':' CET'}</option>`).join('')}
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
  bits.push(F.horizon === 'strategy'
    ? 'uitstap strategie (amc 15:30, bmo 20:00 CET)'
    : `uitstap ${F.horizon} (${HZ_CET[F.horizon]} CET)`);
  bits.push(`${F.from} t/m ${F.to}`);
  document.getElementById('filterline').innerHTML =
    `${esc(bits.join(' · '))} — <b>${withRet.length}</b> namen over ${nDays} dagen` +
    (pend ? `, ${pend} nog in afwikkeling` : '');
}


/* ===================================================================== aanloop
   Does what the stock did BEFORE the print say anything about the call, and does
   it pay when run-up and prediction point the same way? Both recomputed from the
   filtered rows, so every control above moves them. */
const RUNUPS = ['2d','5d','10d','20d'];
const ruOf = (r, w) => r['runup_' + w];

function tabAanloop() {
  const rk = rankRows().filter(r => retOf(r) !== null && retOf(r) !== undefined);
  if (!rk.length) return `<div class="empty">geen rijen onder deze filters</div>`;
  const sgnOf = r => r.impact_sum > 0 ? 1 : r.impact_sum < 0 ? -1 : 0;
  const hitOf = r => (sgnOf(r) !== 0 && Math.sign(mvOf(r)) === sgnOf(r)) ? 1 : 0;

  // question 1: does the run-up rank whether the sign turned out right
  const q1 = RUNUPS.map(w => {
    const g = rk.filter(r => ruOf(r,w) !== null && ruOf(r,w) !== undefined && sgnOf(r) !== 0);
    const days = byDay(g);
    const terc = [...g].sort((a,b)=>ruOf(a,w)-ruOf(b,w));
    const k = Math.floor(terc.length/3);
    const rate = seg => seg.length ? 100*seg.reduce((s,r)=>s+hitOf(r),0)/seg.length : null;
    return {w, n:g.length,
            rho: pooledRho(days, r=>ruOf(r,w), r=>hitOf(r)),
            rhoAbs: pooledRho(days, r=>Math.abs(ruOf(r,w)), r=>hitOf(r)),
            lo: rate(terc.slice(0,k)), mid: rate(terc.slice(k,2*k)), hi: rate(terc.slice(2*k))};
  });

  // question 2: does agreement pay
  const q2 = RUNUPS.map(w => {
    const ok = r => ruOf(r,w) !== null && ruOf(r,w) !== undefined && sgnOf(r) !== 0;
    const ag = rk.filter(r => ok(r) && Math.sign(ruOf(r,w)) === sgnOf(r));
    const di = rk.filter(r => ok(r) && Math.sign(ruOf(r,w)) !== sgnOf(r));
    const B = g => book(g.map(r => retOf(r) === null ? null : retOf(r)).filter(v=>v!==null));
    return {w, a:B(ag), d:B(di)};
  });
  const base = book(rk.map(retOf).filter(v=>v!==null));

  let html = `<p class="lead">De aanloop is het rendement over de 2, 5, 10 en 20 sessies
    <b>tot 20:00 CET op de instapdag</b> — het moment waarop stage E het boek plaatst, niet
    de slotkoers erna. Twee vragen: voorspelt dat of het teken klopte, en levert het meer op
    als aanloop en voorspelling dezelfde kant op wijzen.</p>`;

  html += `<div class="card"><h3>Voorspelt de aanloop of het teken klopte?</h3>` + table([
    {h:'venster', f:r=>`<code>${esc(r.w)}</code>`},
    {h:'n', f:r=>r.n},
    {h:'ρ aanloop', f:r=>n3(r.rho)},
    {h:'ρ |aanloop|', f:r=>n3(r.rhoAbs)},
    {h:'raak laag', f:r=>r.lo===null?'–':n1(r.lo)+'%'},
    {h:'midden', f:r=>r.mid===null?'–':n1(r.mid)+'%'},
    {h:'hoog', f:r=>r.hi===null?'–':n1(r.hi)+'%'}], q1) +
    `<small>Raak is <code>sign(impact_sum)</code> gelijk aan het teken van de gerealiseerde
     beweging. ρ is binnen dagen gepoold. Terciles zijn op de aanloop gesorteerd.</small></div>`;

  html += `<div class="card"><h3>Eens tegen oneens</h3>
    ${legend([{color:css('--s1'), label:'aanloop eens met de voorspelling'},
              {color:css('--s2'), label:'oneens'}])}
    ${chartBlock('c-runup', 250)}
    <small>De twee lijnen wisselen van plaats tussen de vensters. Dat kruisen is het
    antwoord: als meebewegen hielp, zou blauw overal boven oranje liggen.</small>` + table([
    {h:'venster', f:r=>`<code>${esc(r.w)}</code>`},
    {h:'eens n', f:r=>r.a.n},
    {h:'eens raak %', f:r=>n1(r.a.hit)},
    {h:'eens %', f:r=>`<span class="${sgn(r.a.mean)}">${pc(r.a.mean)}</span>`},
    {h:'oneens n', f:r=>r.d.n},
    {h:'oneens raak %', f:r=>n1(r.d.hit)},
    {h:'oneens %', f:r=>`<span class="${sgn(r.d.mean)}">${pc(r.d.mean)}</span>`},
    {h:'verschil', f:r=>`<span class="${sgn(r.a.mean-r.d.mean)}">${pc(r.a.mean-r.d.mean)}</span>`}], q2) +
    `<small>Hele selectie ter vergelijking: ${pc(base.mean)} per naam over ${base.n}.
     Zet de <b>drempel</b> hierboven aan en weer uit: het teken van de laatste kolom keert
     om tussen de volledige steekproef en het verhandelde boek. Twee deelverzamelingen van
     dezelfde data die tegengesteld wijzen zijn geen twee bevindingen.</small></div>`;

  html += `<div class="card"><h3>20-daagse aanloop tegen het rendement</h3>
    ${chartBlock('c-runup-sc', 300)}
    <small>Eén punt per naam. Blauw boven de conviction floor, grijs eronder.</small></div>`;

  draw.push(() => {
    lineChart(document.getElementById('c-runup'), {
      x: q2.map(r=>r.w), height:250, zero:true, fmtY:v=>v.toFixed(0)+'%', fmtT:pc,
      series:[{label:'eens', color:css('--s1'), values:q2.map(r=>r.a.n?r.a.mean:null)},
              {label:'oneens', color:css('--s2'), values:q2.map(r=>r.d.n?r.d.mean:null)}],
      tipX:i=>`aanloopvenster ${q2[i].w} — eens n=${q2[i].a.n}, oneens n=${q2[i].d.n}`});
    scatterChart(document.getElementById('c-runup-sc'), {
      height:300, labelX:'20-daagse aanloop tot 20:00 CET (%)', labelY:'rendement (%)',
      fmtX:v=>v.toFixed(0)+'%', fmtY:v=>v.toFixed(0)+'%',
      points: rk.filter(r=>ruOf(r,'20d')!==null && retOf(r)!==null).map(r=>({
        x:ruOf(r,'20d'), y:retOf(r),
        color: Math.abs(r.impact_sum) >= D.conviction_floor ? css('--s1') : css('--muted'),
        tip:`<b>${esc(r.ticker)}</b> ${esc(r.run_date)}<br>aanloop ${pc(ruOf(r,'20d'))}<br>impact_sum ${n2(r.impact_sum)}<br>rendement ${pc(retOf(r))}`}))});
  });
  return html;
}

/* ====================================================================== instap
   The Timing tab moves the exit with the entry fixed at the 22:00 CET close. This
   moves the ENTRY with the exit fixed at whichever horizon is selected above. */
const ENTRY_KEYS = ['1000','1030','1100','1130','1200','1230','1300','1330','1400',
                    '1430','1500','1530','1555'];
const ENTRY_CET = {'1000':'16:00','1030':'16:30','1100':'17:00','1130':'17:30','1200':'18:00',
                   '1230':'18:30','1300':'19:00','1330':'19:30','1400':'20:00','1430':'20:30',
                   '1500':'21:00','1530':'21:30','1555':'21:55'};

function tabInstap() {
  const rk = rankRows();
  if (!rk.length) return `<div class="empty">geen rijen onder deze filters</div>`;
  const exitPx = r => (r.px || {})[F.horizon];
  const ret = (r, k) => {
    const e = (r.enpx || {})[k], x = exitPx(r);
    if (!e || !x) return null;
    const v = (x/e - 1)*100;
    return r.impact_sum > 0 ? v : r.impact_sum < 0 ? -v : null;
  };
  const stat = (k, sel) => {
    const g = rk.filter(r => (!sel || sel(r)) && ret(r,k) !== null);
    const b = book(g.map(r => ret(r,k)));
    return {...b, rho: pooledRho(byDay(g), r=>r.impact_sum, r=>ret(r,k))};
  };
  const rows = ENTRY_KEYS.map(k => ({k, all:stat(k),
                                     amc:stat(k, r=>r.session==='amc'),
                                     bmo:stat(k, r=>r.session==='bmo')}));
  const anchor = rows.find(r=>r.k==='1400');
  const withN = rows.filter(r=>r.all.n>=3);
  const best = withN.reduce((a,b)=>b.all.mean>a.all.mean?b:a, withN[0]||rows[0]);
  const worst = withN.reduce((a,b)=>b.all.mean<a.all.mean?b:a, withN[0]||rows[0]);
  // what the wait costs before any prediction is applied
  const drift = ENTRY_KEYS.slice(0,-1).map(k => {
    const g = rk.filter(r => (r.enpx||{})[k] && (r.enpx||{})['1555']);
    const xs = g.map(r => (r.enpx['1555']/r.enpx[k] - 1)*100);
    return {k, n:xs.length, ...book(xs)};
  });

  const HZNAME = F.horizon === 'strategy' ? 'strategie (amc 15:30, bmo 20:00 CET)'
                                          : F.horizon;
  let html = `<p class="lead">De uitstap staat vast op <code>${esc(HZNAME)}</code> en alleen
    de <b>instap</b> schuift, van 16:00 tot 21:55 CET. Elk verschil tussen twee rijen is dus
    instapmoment en niets anders. Stage E koopt nu om 20:00 CET.</p>`;
  html += tiles([
    {k:'om 20:00 CET', v:pc(anchor && anchor.all.mean), cls:sgn(anchor && anchor.all.mean),
     s:`${anchor ? anchor.all.n : 0} namen`},
    {k:'beste moment', v:ENTRY_CET[best.k]||best.k, s:pc(best.all.mean)},
    {k:'slechtste', v:ENTRY_CET[worst.k]||worst.k, s:pc(worst.all.mean)},
    {k:'spreiding over de sessie', v:n2(best.all.mean-worst.all.mean)+'pp',
     s:`sd per naam ${n1(anchor && anchor.all.sd)}`}]);

  html += `<div class="card"><h3>Rendement per instapmoment</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-entry', 250)}
    <small>De kolom met <b>nu</b> eronder is 20:00 CET, de huidige instap.</small></div>`;

  html += `<div class="card"><h3>Per instapmoment</h3>` + table([
    {h:'instap (CET)', f:r=>`${ENTRY_CET[r.k]||r.k}${r.k==='1400'?' <b>·  nu</b>':''}`},
    {h:'n', f:r=>r.all.n}, {h:'ρ', f:r=>n3(r.all.rho)},
    {h:'raak %', f:r=>n1(r.all.hit)},
    {h:'boek %', f:r=>`<span class="${sgn(r.all.mean)}">${pc(r.all.mean)}</span>`},
    {h:'t', f:r=>n2(r.all.t)},
    {h:'vs 20:00', f:r=>anchor?`<span class="${sgn(r.all.mean-anchor.all.mean)}">${n2(r.all.mean-anchor.all.mean)}pp</span>`:'–'},
    {h:'amc %', f:r=>`<span class="${sgn(r.amc.mean)}">${pc(r.amc.mean)}</span>`},
    {h:'bmo %', f:r=>`<span class="${sgn(r.bmo.mean)}">${pc(r.bmo.mean)}</span>`}], rows) +
    `<small>Reguliere sessie, dus elke prijs hier had omvang. De spread zit er niet in en
     is het enige argument dat vóór later instappen pleit: hij is het breedst rond de opening
     en het smalst tegen de close.</small></div>`;

  html += `<div class="card"><h3>Wat het wachten kost vóór er een voorspelling op zit</h3>` + table([
    {h:'instap (CET)', f:r=>ENTRY_CET[r.k]||r.k}, {h:'n', f:r=>r.n},
    {h:'drift naar 21:55', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'t', f:r=>n2(r.t)}], drift) +
    `<small>Ongetekend. Is dit vlak, dan valt er niets te timen en is de grafiek hierboven
     vlak om die reden.</small></div>`;

  draw.push(() => {
    lineChart(document.getElementById('c-entry'), {
      x: ENTRY_KEYS.map(k=>ENTRY_CET[k]||k), height:250, zero:true,
      fmtY:v=>v.toFixed(0)+'%', fmtT:pc,
      sub: ENTRY_KEYS.map(k => k==='1400' ? 'nu' : ''),
      series:[{label:'alles', color:css('--s1'), values:rows.map(r=>r.all.n>=3?r.all.mean:null)},
              {label:'amc', color:css('--s2'), values:rows.map(r=>r.amc.n>=3?r.amc.mean:null)},
              {label:'bmo', color:css('--s3'), values:rows.map(r=>r.bmo.n>=3?r.bmo.mean:null)}],
      tipX:i=>`instap ${ENTRY_CET[ENTRY_KEYS[i]]} CET — n=${rows[i].all.n}, ρ ${n3(rows[i].all.rho)}`});
  });
  return html;
}

/* ================================================================= zoekvolume */
function tabZoek() {
  const rk = rankRows().filter(r => retOf(r) !== null && retOf(r) !== undefined);
  const meas = rk.filter(r => r.search_state === 'measured' && r.search_spike !== null
                           && r.search_spike !== undefined);
  const counts = {measured:0, sparse:0, silent:0, unmeasured:0};
  rk.forEach(r => { counts[r.search_state] = (counts[r.search_state]||0) + 1; });
  if (!meas.length) return `<p class="lead">Geen meetbare Trends-reeks onder deze filters.</p>`;

  const days = byDay(meas);
  const rhoTrade = pooledRho(days, r=>r.search_spike, r=>retOf(r));
  const rhoMove  = pooledRho(days, r=>r.search_spike, r=>Math.abs(mvOf(r)));
  const srt = [...meas].sort((a,b)=>a.search_spike-b.search_spike);
  const k = Math.floor(srt.length/3);
  const bucket = (g, label) => ({label, n:g.length, ...book(g.map(retOf)),
    lo:g.length?g[0].search_spike:null, hi:g.length?g[g.length-1].search_spike:null,
    absMove: g.length ? spread(g.map(r=>Math.abs(mvOf(r)))).median : null});
  const buckets = [bucket(srt.slice(0,k),'lage zoekpiek'), bucket(srt.slice(k,2*k),'midden'),
                   bucket(srt.slice(2*k),'hoge zoekpiek')];
  const mdDV = g => g.length ? spread(g.map(r=>advOf(r)||0)).median : null;

  let html = `<p class="lead">Google Trends, dagelijks, VS, de 90 dagen tot de instapdag. De
    <b>zoekpiek</b> is de intensiteit op de instapdag gedeeld door de eigen mediaan. Eén vaste
    zoekterm per bedrijf: de naam zonder rechtsvorm, nooit de ticker.</p>`;
  html += tiles([
    {k:'meetbaar', v:counts.measured||0, s:`van ${rk.length} namen`},
    {k:'te dun', v:counts.sparse||0, s:'mediaan nul, geen basislijn'},
    {k:'nul op elke dag', v:counts.silent||0, s:'onder Googles drempel'},
    {k:'ρ piek vs rendement', v:n3(rhoTrade), cls:sgn(rhoTrade), s:'binnen dagen gepoold'}]);

  html += `<div class="card"><h3>Zoekpiek tegen het rendement</h3>
    ${chartBlock('c-zoek', 300)}
    <small>Blauw boven de conviction floor, grijs eronder. De verticale as is het rendement
    op de geselecteerde uitstap.</small></div>`;

  html += `<div class="card"><h3>Per tercile</h3>` + table([
    {h:'bak', f:r=>`${esc(r.label)} <span class="mut">(${n2(r.lo)}×–${n2(r.hi)}×)</span>`},
    {h:'n', f:r=>r.n}, {h:'raak %', f:r=>n1(r.hit)},
    {h:'boek %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'t', f:r=>n2(r.t)},
    {h:'mediane |beweging|', f:r=>n2(r.absMove)+'%'}], buckets) +
    `<small>De rechterkolom is het aannemelijke deel: namen met veel aandacht bewegen
     minder, dus hun print was al uitgekauwd. Als <em>rang</em>correlatie over alle namen
     is datzelfde verband er niet — ρ van de piek tegen |beweging| is ${n3(rhoMove)} —
     dus het zit in de staarten, niet in een monotoon verband.</small></div>`;

  html += `<div class="card"><h3>Wat de meetdrempel selecteert</h3>` + table([
    {h:'groep', f:r=>esc(r.k)}, {h:'n', f:r=>r.n},
    {h:'mediane omzet/dag', f:r=>r.dv===null?'–':'$'+(r.dv/1e6).toFixed(1)+'m'}],
    [{k:'meetbaar', n:meas.length, dv:mdDV(meas)},
     {k:'te dun of stil', n:rk.filter(r=>r.search_state==='sparse'||r.search_state==='silent').length,
      dv:mdDV(rk.filter(r=>r.search_state==='sparse'||r.search_state==='silent'))}]) +
    `<small>Elke correlatie hierboven geldt dus voor de liquide helft van het boek en zegt
     niets over de helft die deze stage het vaakst verhandelt.</small></div>`;

  draw.push(() => {
    scatterChart(document.getElementById('c-zoek'), {
      height:300, labelX:'zoekpiek op de instapdag (× de eigen mediaan)', labelY:'rendement (%)',
      fmtX:v=>v.toFixed(1)+'×', fmtY:v=>v.toFixed(0)+'%',
      points: meas.map(r=>({x:r.search_spike, y:retOf(r),
        color: Math.abs(r.impact_sum) >= D.conviction_floor ? css('--s1') : css('--muted'),
        tip:`<b>${esc(r.ticker)}</b> ${esc(r.run_date)}<br>piek ${n2(r.search_spike)}×, niveau ${n1(r.search_level)}<br>impact_sum ${n2(r.impact_sum)}<br>rendement ${pc(retOf(r))}`}))});
  });
  return html;
}

/* ====================================================================== agenda */
function tabAgenda() {
  const C = D.calendar;
  if (!C || !C.by_date) return `<p class="lead">Geen agenda in de ledger. Draai
    <code>python3 researcher_us/scripts/edge_calendar.py</code> en bouw opnieuw.</p>`;
  const dates = Object.keys(C.by_date).sort();
  const rows = [];
  dates.forEach(d => {
    const all = C.by_date[d] || [];
    const conf = all.filter(n => n.session === 'amc' || n.session === 'bmo');
    const tr = conf.filter(n => n.clears_liquidity)
                   .sort((a,b)=>(b.dollar_vol||0)-(a.dollar_vol||0));
    (tr.length ? tr : [null]).forEach((n, i) => rows.push({
      d: i===0 ? d : '', conf: i===0 ? conf.length : '', unk: i===0 ? all.length-conf.length : '',
      n}));
  });
  let html = `<p class="lead">Vooruitblik, geen meting: wat er komende week rapporteert en
    hoeveel daarvan door de twee poorten komt die bepalen of de hunt een naam ziet.</p>`;
  html += tiles([
    {k:'kalenderregels', v:C.totals.rows, s:`over ${dates.length} handelsdagen`},
    {k:'bevestigde sessie', v:C.totals.confirmed_session, s:'de enige die stage 0 houdt'},
    {k:'halen de omzetvloer', v:C.totals.clears_liquidity,
     s:`$${Number(C.liquidity_floor_usd).toLocaleString('nl-NL')}/dag`},
    {k:'weggelaten', v:C.totals.rows - C.totals.confirmed_session, s:'time-not-supplied'}]);
  html += `<div class="card"><h3>De namen</h3>` + table([
    {h:'datum', f:r=>esc(r.d)},
    {h:'bevestigd', f:r=>r.conf}, {h:'onbekend', f:r=>r.unk},
    {h:'naam', f:r=>r.n ? `<b>${esc(r.n.ticker)}</b> <span class="mut">${esc((r.n.company||'').slice(0,38))}</span>` : '<span class="mut">geen verhandelbare naam</span>'},
    {h:'sessie', f:r=>r.n?esc(r.n.session):''},
    {h:'omzet/dag', f:r=>r.n && r.n.dollar_vol ? '$'+(r.n.dollar_vol/1e6).toFixed(1)+'m' : '–'},
    {h:'eps-verwachting', f:r=>r.n ? esc(r.n.eps_estimate ?? '–') : ''}], rows) +
    `<small>Geen voorspelling en geen ranking — die komen uit een hunt die nog niet heeft
     gedraaid. Opgehaald ${esc((C.generated_utc||'').slice(0,16))} UTC.</small></div>`;
  return html;
}


/* ================================================================== hypotheses
   A register, not a conclusion. Two halves and the order matters:

   1. INTERMEDIATE VARIABLES are screened first, against three outcomes that are
      not the same question -- was the SIGN right, what did the BOOK earn, and how
      far did the stock MOVE. A variable that only predicts the third is a
      volatility proxy and says nothing about skill.
   2. HYPOTHESES are named, directional and were written AFTER reading that screen.
      That is the honest order to work in and the dishonest order to report, so the
      page says so at the top rather than presenting them as predictions.

   Everything recomputes from the filtered rows, so any hypothesis can be re-asked
   under a different exit, threshold, period or sector. */

const SCREEN_VARS = [
  ['priced_lean_pct', 'prijs-lean uit de baseline'],
  ['retail_tilt',     'retail tilt (consumentenkarakter)'],
  ['realised_vol_20d','gerealiseerde vol 20d'],
  ['n_findings',      'aantal findings'],
  ['baseline_quality','baseline-kwaliteit'],
  ['neg_runup',       'min de 20d aanloop (gratis controle)'],
  ['runup_20d',       '20d aanloop tot 20:00 CET'],
  ['search_spike',    'Google-zoekpiek'],
  ['dollar_vol',      'omzet per dag'],
  ['market_cap_usd',  'marktkapitalisatie'],
  ['churn_pct',       'churn'],
  ['conviction',      '|impact_sum| (conviction)'],
  ['rank',            'rang binnen de dag'],
];

function hypRows() {
  return rankRows().filter(r => r.impact_sum !== 0 && retOf(r) !== null
                             && retOf(r) !== undefined);
}
const hitOf  = r => (Math.sign(r.impact_sum) === Math.sign(mvOf(r))) ? 1 : 0;
const rateOf = g => g.length ? 100 * g.reduce((s,r)=>s+hitOf(r),0) / g.length : null;

/* ONE VERDICT LADDER, applied to every hypothesis so none gets a kinder reading.
   The middle rung is the important one: a difference can be large enough to matter
   and still be indistinguishable from nothing on 13 days, and calling that "geen
   effect" throws away the thing most worth measuring forward. So:

     steun               right sign, |t| >= 2
     mogelijk            right sign, |t| < 2, but the gap is practically large
     geen effect         small either way
     mogelijk andersom   wrong sign, practically large, |t| < 2
     tegengesteld        wrong sign, |t| >= 2
     te dun              under eight names on a side

   PRACTICALLY LARGE is 1.5 percentage points per name. That is not a statistical
   bar; it is the smallest difference that would change what you do on a book whose
   floor rule is worth about 6 points. */
const PRACTICAL_PP = 1.5;

function rungOf(gap, t, expect) {
  const right = expect > 0 ? gap > 0 : gap < 0;
  const big = Math.abs(gap) >= PRACTICAL_PP;
  if (t != null && isFinite(t) && Math.abs(t) >= 2)
    return right ? ['steun', 'c-yes'] : ['tegengesteld', 'c-anti'];
  if (big) return right ? ['mogelijk · meer data', 'c-maybe']
                        : ['mogelijk andersom', 'c-maybe'];
  return ['geen effect', 'c-no'];
}
/* How many events this would need to settle, at the size it is showing now. The
   standard error falls with sqrt(n), so n_needed = n * (2/t)^2. It is a rough number
   and it is the most useful one on the page: it turns "not significant" into "come
   back after this many more prints". */
function needN(n, t) {
  if (!t || !isFinite(t) || Math.abs(t) >= 2) return null;
  return Math.ceil(n * Math.pow(2 / Math.abs(t), 2));
}

function verdict(a, b, expect) {
  if (!a || !b || a.n < 8 || b.n < 8) return ['te dun', 'c-thin'];
  const gap = a.mean - b.mean;
  const se = Math.sqrt((a.sd ?? 0)**2 / a.n + (b.sd ?? 0)**2 / b.n);
  if (!isFinite(se) || se <= 0) return ['geen effect', 'c-no'];
  return rungOf(gap, gap / se, expect);
}
/* The gap, its uncertainty, and -- when it falls short -- how much more data it
   would take. */
function gapNote(a, b) {
  if (!a || !b || !a.n || !b.n) return '';
  const gap = a.mean - b.mean;
  const se = Math.sqrt((a.sd ?? 0)**2 / a.n + (b.sd ?? 0)**2 / b.n);
  const t = se > 0 ? gap / se : null;
  const need = needN(a.n + b.n, t);
  return `verschil ${pc(gap)}, t ${n2(t)}` +
         (need ? ` — zou ongeveer ${need} namen nodig hebben in plaats van ${a.n + b.n}`
               : ` — haalt de lat`);
}
/* A PAIRED hypothesis compares the same names at two exits. Running that as two
   independent groups inflates the standard error by roughly the between-name spread,
   which on this book is an order of magnitude larger than the difference being
   tested -- so it reports "geen effect" for anything. The per-name difference is the
   right series to test, and it is also the one a reader can act on. */
function pairedSide(rows, fa, fb, labelA, labelB) {
  const pairs = rows.filter(r => fa(r) != null && fb(r) != null)
                    .map(r => ({a: fa(r), b: fb(r)}));
  if (!pairs.length) return null;
  const d = pairs.map(x => x.a - x.b);
  const st = ttest(d);
  return {n: pairs.length, diff: st.mean, t: st.t, sd: st.sd,
          ci: st.ci, wins: d.filter(x=>x>0).length,
          a: book(pairs.map(x=>x.a)), b: book(pairs.map(x=>x.b)),
          labelA, labelB};
}
function pairedVerdict(pr, expect) {
  if (!pr || pr.n < 8) return ['te dun', 'c-thin'];
  if (pr.t == null || !isFinite(pr.t)) return ['geen effect', 'c-no'];
  return rungOf(pr.diff, pr.t, expect);
}
function pairedBlock(h) {
  const pr = h.pair;
  const [v, cls] = pairedVerdict(pr, h.expect ?? 1);
  const rows = pr ? [{...pr.a, label: pr.labelA}, {...pr.b, label: pr.labelB}] : [];
  return `<div class="hyp">
    <h4>${esc(h.id)} · ${esc(h.title)} <span class="chip ${cls}">${esc(v)}</span></h4>
    <p class="claim">${h.claim}</p>
    ${table([{h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n},
             {h:'raak %', f:r=>r.hit===null?'–':n1(r.hit)},
             {h:'per naam', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
             {h:'t', f:r=>n2(r.t)}], rows)}
    <p class="why"><code>${pr ? `gepaard over ${pr.n} namen: verschil ${pc(pr.diff)}, ` +
      `t ${n2(pr.t)}, ${pr.wins}/${pr.n} in de voorspelde richting` +
      (needN(pr.n, pr.t) ? ` — zou ongeveer ${needN(pr.n, pr.t)} namen nodig hebben`
                         : ' — haalt de lat') : 'te weinig paren'}</code></p>
    ${h.why ? `<p class="why">${h.why}</p>` : ''}
  </div>`;
}

function side(rows, label) {
  const b = book(rows.map(retOf));
  return {...b, label, hit: rateOf(rows)};
}
function hypBlock(h) {
  const [v, cls] = verdict(h.a, h.b, h.expect ?? 1);
  const rows = [h.a, h.b].filter(x => x && x.n);
  return `<div class="hyp">
    <h4>${esc(h.id)} · ${esc(h.title)} <span class="chip ${cls}">${esc(v)}</span></h4>
    <p class="claim">${h.claim}</p>
    ${table([{h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n},
             {h:'raak %', f:r=>r.hit===null?'–':n1(r.hit)},
             {h:'per naam', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
             {h:'mediaan', f:r=>pc(r.med ?? r.median)},
             {h:'t', f:r=>n2(r.t)}], rows)}
    <p class="why"><code>${esc(gapNote(h.a, h.b))}</code></p>
    ${h.why ? `<p class="why">${h.why}</p>` : ''}
  </div>`;
}

function tabHypotheses() {
  const rk = hypRows();
  if (rk.length < 12) return `<div class="empty">te weinig rijen onder deze filters</div>`;
  const dd = byDay(rk);
  const FLOOR = D.conviction_floor ?? 3;
  const above = rk.filter(r => Math.abs(r.impact_sum) >= FLOOR);
  const below = rk.filter(r => Math.abs(r.impact_sum) <  FLOOR);
  const medOf = k => { const v = above.map(r=>r[k]).filter(x=>x!==null&&x!==undefined)
                                      .sort((a,b)=>a-b);
                       return v.length ? v[Math.floor(v.length/2)] : null; };

  let html = `<p class="lead">Een register van vermoedens, geen conclusies. Elke regel
    herberekent uit de rijen die door de filters hierboven komen, dus je kunt elke
    hypothese opnieuw stellen onder een andere uitstap, drempel, periode of sector.</p>`;

  html += `<div class="warn"><b>Lees dit eerst.</b> Deze hypotheses zijn geschreven
    <i>nadat</i> de screen hieronder was bekeken. Dat is de eerlijke volgorde om in te
    werken en de oneerlijke om in te rapporteren, dus het staat er. Er zijn ${SCREEN_VARS.length}
    variabelen tegen drie uitkomsten gezet plus een stuk of tien splitsingen: bij
    p&nbsp;&lt;&nbsp;0,05 horen daar twee tot drie toevalstreffers tussen te zitten.
    Niets hier is gecorrigeerd voor meervoudig toetsen, en ${dd.length} dagen is geen
    steekproef waarop een weegfactor hoort te worden gekalibreerd. Gebruik het om te
    kiezen wát je vooruit gaat meten, niet om nu iets te wegen.</div>`;

  /* ------------------------------------------------- 1. intermediate variables */
  html += `<div class="card"><h3>1. Tussenvariabelen, eerst gescreend</h3>
    <p class="claim">Drie uitkomsten die niet dezelfde vraag zijn. <b>Raak</b> is of het
    teken klopte. <b>Boek</b> is wat de trade opleverde. <b>|beweging|</b> is hoe ver het
    aandeel ging, in welke richting dan ook — een variabele die alleen dát voorspelt is
    een volatiliteitsmaat en zegt niets over of de hunt gelijk had. ρ is binnen dagen
    gepoold, p is een permutatie-p.</p>`;
  const scr = SCREEN_VARS.map(([k, label]) => {
    const g = rk.filter(r => r[k] !== null && r[k] !== undefined);
    if (g.length < 20) return {k, label, n: g.length, thin: true};
    const gd = byDay(g);
    return {k, label, n: g.length,
            ra: pooledRho(gd, r=>r[k], r=>hitOf(r)),
            rr: pooledRho(gd, r=>r[k], r=>retOf(r)),
            rm: pooledRho(gd, r=>r[k], r=>Math.abs(mvOf(r)))};
  });
  /* Bold means "clears a rough 2/sqrt(n) bar", not "is a number". Marking every
     value emphatic is how a screen starts reading like a result. */
  const mark = (v, n) => v == null ? '–'
    : (Math.abs(v) >= 2 / Math.sqrt(Math.max(n, 1)) ? `<b>${n3(v)}</b>` : n3(v));
  html += table([
    {h:'variabele', f:r=>`${esc(r.label)}<br><code>${esc(r.k)}</code>`},
    {h:'n', f:r=>r.n},
    {h:'ρ raak', f:r=>r.thin?'–':mark(r.ra, r.n)},
    {h:'ρ boek', f:r=>r.thin?'–':mark(r.rr, r.n)},
    {h:'ρ |beweging|', f:r=>r.thin?'–':mark(r.rm, r.n)},
  ], scr) + `<small>Vet is <code>|ρ| ≥ 2/√n</code>, een ruwe 5%-lat — geen p-waarde, en
    zeker geen p-waarde die is gecorrigeerd voor de ${SCREEN_VARS.length}&nbsp;×&nbsp;3
    cellen in deze tabel. Leeg betekent minder dan 20 namen onder deze filters.
    <code>priced_lean_pct</code> en <code>conviction</code> komen uit de run zelf; de rest
    uit de tape of van buiten. Let op de derde kolom: als een variabele alléén daar vet
    staat, voorspelt hij hoe hard het aandeel beweegt en niet of de hunt gelijk had — dat
    is volatiliteit, geen vaardigheid.</small></div>`;

  /* -------------------------------------------------------- 2. the hypotheses */
  /* THE HYPOTHESES ARE ASKED OF THE TRADED BOOK, not of every ranked name. A rule
     that only works on names the stage never buys cannot change anything, and the
     names below the floor are a different population: their sign is a coin flip, so
     mixing them in dilutes every split with noise the book never carries. The cost is
     power -- roughly half the sample -- which is why the middle rung of the ladder
     exists. H6 is the exception: it IS the floor, so it has to see both sides. */
  const HS = above;
  const ctx = (fa, fb, expect) => {          // the same split over ALL names, for context
    const a = side(rk.filter(fa), ''), b = side(rk.filter(fb), '');
    if (!a.n || !b.n) return '';
    const gap = a.mean - b.mean;
    const se = Math.sqrt((a.sd ?? 0)**2 / a.n + (b.sd ?? 0)**2 / b.n);
    return `alle namen (n=${a.n}+${b.n}): verschil ${pc(gap)}, t ${n2(se ? gap/se : null)}`;
  };
  const H = [];

  H.push({id:'H1', title:'bmo is beter voorspelbaar dan amc',
    claim:`Een <code>bmo</code>-print heeft twee dunne voorbeurs-uren gehad, een
      <code>amc</code>-print een hele nacht. Als de hunt iets vindt dat de markt nog moet
      verwerken, hoort dat bij bmo langer beschikbaar te zijn.`,
    a: side(HS.filter(r=>r.session==='bmo'), 'bmo'),
    b: side(HS.filter(r=>r.session==='amc'), 'amc'), expect: 1,
    why:`Boven de conviction floor. ` + ctx(r=>r.session==='bmo', r=>r.session==='amc')});

  const sgnRet = (r, k) => r[k] == null ? null : (r.impact_sum > 0 ? r[k] : -r[k]);
  H.push({id:'H2a', title:'amc is méér waard verkocht op de opening dan op de close',
    paired: true, expect: 1,
    claim:`Een <code>amc</code>-print heeft een hele nacht gehad om verwerkt te worden, dus
      de beweging hoort in de openingsprint te zitten en daarna terug te lopen. Dezelfde
      namen op twee uitstappen, dus dit is een <b>gepaarde</b> toets: het verschil per naam,
      niet twee groepen naast elkaar.`,
    pair: pairedSide(above.filter(r=>r.session==='amc'),
                     r=>sgnRet(r,'mv_open'), r=>sgnRet(r,'mv_close'),
                     'amc, uit op de opening (15:30)', 'amc, uit op de close (22:00)'),
    why:`Alleen namen boven de conviction floor, want daar wordt op gehandeld.`});

  H.push({id:'H2b', title:'bmo is méér waard verkocht op de close dan op de opening',
    paired: true, expect: 1,
    claim:`De spiegel van H2a: een <code>bmo</code>-print heeft twee dunne voorbeurs-uren
      gehad en herprijst de hele sessie door, dus vasthouden hoort te lonen. Als H2a en H2b
      allebei staan, is er geen één uitstap voor dit boek maar twee.`,
    pair: pairedSide(above.filter(r=>r.session==='bmo'),
                     r=>sgnRet(r,'mv_close'), r=>sgnRet(r,'mv_open'),
                     'bmo, uit op de close (22:00)', 'bmo, uit op de opening (15:30)'),
    why:`De huidige standaarduitstap verkoopt bmo om 20:00 CET, tussen deze twee in.`});

  const tilt = medOf('retail_tilt');
  if (tilt !== null) {
    H.push({id:'H3', title:'namen met een consumentenkarakter zijn beter voorspelbaar',
      claim:`<code>retail_tilt</code> is de samengestelde maat uit de ledger: churn, kleine
        kap, lage koers en volatiliteit. Het vermoeden is dat een retail-gehouden naam
        reageert op wat een lezer kan vinden, en een institutioneel gehouden naam niet.
        Mediaan onder deze filters is ${n1(tilt)}.`,
      a: side(HS.filter(r=>r.retail_tilt >= tilt), `tilt ≥ ${n1(tilt)}`),
      b: side(HS.filter(r=>r.retail_tilt <  tilt), `tilt < ${n1(tilt)}`), expect: 1,
      why:`Let op de interactietabel onderaan: het effect zit niet in de tilt zelf maar in
        de combinatie met de conviction floor.`});
  }

  const bySec = {};
  HS.forEach(r => { const k = r.sector || 'onbekend';
                    (bySec[k] = bySec[k] || []).push(r); });
  const secs = Object.entries(bySec).filter(([,g]) => g.length >= 8)
                     .map(([k,g]) => side(g, k)).sort((a,b)=>b.mean-a.mean);
  if (secs.length >= 2) {
    H.push({id:'H4', title:'één sector draagt het resultaat',
      claim:`Als de hunt in één sector werkt en nergens anders, is dat een selectieregel
        en geen weegfactor. Beste tegen slechtste sector met minstens zes namen.`,
      a: secs[0], b: secs[secs.length-1], expect: 1,
      why:`Alle sectoren staan in de tabel hieronder. Dit is de hypothese waar het
        meervoudig-toetsen-probleem het hardst bijt: met negen sectoren is de beste
        ervan altijd goed.`});
  }

  const lean = medOf('priced_lean_pct');
  if (lean !== null) {
    H.push({id:'H5', title:'de hunt betaalt méér als hij mét de prijs mee wijst',
      claim:`<code>priced_lean_pct</code> is wat de sealed baseline zegt dat de prijs al
        leunt, vóór er een hunter draaide. De stage heet "zoek wat de markt heeft gemist",
        dus als dit iets oplevert wijst het de verkeerde kant op: dan verdient de hunt
        juist waar hij de markt <i>volgt</i>.`,
      a: side(HS.filter(r=>r.priced_lean_pct >= lean), `lean ≥ ${n2(lean)}`),
      b: side(HS.filter(r=>r.priced_lean_pct <  lean), `lean < ${n2(lean)}`), expect: 1,
      why:`Dit is de enige continue variabele in de screen die op zowel raak als boek iets
        laat zien. Het is ook de meest ongemakkelijke uitkomst in dit register, en daarom
        de eerste die vooruit gemeten hoort te worden in plaats van weggeredeneerd.`});
  }

  H.push({id:'H6', title:'de conviction floor werkt (het anker)',
    claim:`Geen nieuwe hypothese maar de controle waar de rest tegen afgezet hoort te
      worden: dit is de enige regel in <code>researcher_us/EDGE_ANALYSIS.md</code> die een
      familiegewijze correctie overleefde. Als een nieuwe splitsing minder doet dan deze,
      is hij het niet waard.`,
    a: side(above, `|impact_sum| ≥ ${FLOOR}`),
    b: side(below, `< ${FLOOR}`), expect: 1});

  H.push({id:'H7', title:'meer findings is een betere voorspelling',
    claim:`Een naam waar de hunter zes dingen vond hoort beter gelezen te zijn dan een
      naam met één. Als dat niet zo is, meet <code>impact_sum</code> vooral hoeveel er
      te schrijven viel.`,
    a: side(HS.filter(r=>r.n_findings >= 4), 'vier findings of meer'),
    b: side(HS.filter(r=>r.n_findings <  4), 'minder dan vier'), expect: 1,
    why: ctx(r=>r.n_findings>=4, r=>r.n_findings<4)});

  const dv = medOf('dollar_vol');
  if (dv !== null) {
    H.push({id:'H8', title:'de edge zit in de kleine, dun verhandelde namen',
      claim:`Waar minder ogen kijken, hoort meer onverwerkt te zijn. Dit is ook de
        hypothese met de meeste praktische gevolgen: als hij klopt, zit het rendement
        precies waar het niet te handelen is.`,
      a: side(HS.filter(r=>(advOf(r)||0) <  dv), `omzet < $${n1(dv/1e6)}m`),
      b: side(HS.filter(r=>(advOf(r)||0) >= dv), `omzet ≥ $${n1(dv/1e6)}m`), expect: 1,
      why: ctx(r=>(advOf(r)||0)<dv, r=>(advOf(r)||0)>=dv)});
  }

  const meas = HS.filter(r => r.search_state === 'measured' && r.search_spike != null);
  if (meas.length >= 16) {
    const sp = [...meas].map(r=>r.search_spike).sort((a,b)=>a-b)[Math.floor(meas.length/2)];
    H.push({id:'H9', title:'veel zoekverkeer betekent een slechtere trade',
      claim:`Uit het tabblad Zoekvolume, hier als toetsbare regel gezet: aandacht hoort
        bij een print die al is uitgekauwd. Alleen de namen die Google überhaupt meet.`,
      a: side(meas.filter(r=>r.search_spike <  sp), `zoekpiek < ${n2(sp)}×`),
      b: side(meas.filter(r=>r.search_spike >= sp), `zoekpiek ≥ ${n2(sp)}×`), expect: 1});
  }

  html += `<div class="card"><h3>2. De hypotheses</h3>
    <p class="claim"><b>Alles hieronder wordt gevraagd van het verhandelde boek</b> —
    de namen boven de conviction floor — en niet van elke gerangschikte naam. Een regel
    die alleen werkt op namen die de stage nooit koopt kan niets veranderen, en onder de
    floor is het teken een muntje, dus die namen verdunnen elke splitsing met ruis die het
    boek niet draagt. Dat kost ongeveer de helft van de steekproef, en daarvoor is de
    middelste trede. H6 is de uitzondering: dat <i>is</i> de floor, dus die ziet beide
    kanten.</p>
    <p class="claim">Verdict per regel: <b>steun</b> als het verschil het voorspelde teken
    heeft en |t| ≥ 2; <b>mogelijk · meer data</b> als het teken klopt en het verschil
    praktisch groot is (≥ ${PRACTICAL_PP} procentpunt per naam) maar |t| nog onder 2 zit;
    <b>geen effect</b> als het klein is;
    <b>tegengesteld</b> als het even groot is maar de andere kant op; <b>geen effect</b>
    als het kleiner is; <b>te dun</b> onder acht namen per kant. Eén regel voor alle
    hypotheses, zodat geen enkele een vriendelijker lezing krijgt.</p>
    <p class="claim">Een gepaarde hypothese (dezelfde namen, twee uitstappen) wordt op het
    verschil <i>per naam</i> getoetst; twee losse groepen zouden daar de hele spreiding
    tussen namen in de standaardfout stoppen en dus nooit iets vinden.</p>
    <p class="claim">De drempel is geen vast aantal punten maar twee standaardfouten van
    het verschil zelf — ruwweg een t-toets op p&nbsp;&lt;&nbsp;0,05. Een vaste drempel van
    twee procentpunt gaf zeven van de negen hypotheses <i>steun</i> op een boek met een
    standaardafwijking van twaalf per naam, en dat is wat een te losse regel doet.</p>
    ${H.map(h => h.paired ? pairedBlock(h) : hypBlock(h)).join('')}</div>`;

  /* --------------------------------------------- 3. the two supporting displays */
  const HZ = D.horizons;
  const curve = sess => HZ.map(h => {
    const g = above.filter(r => r.session === sess && r['mv_'+h] != null);
    return g.length >= 5
      ? book(g.map(r => r.impact_sum > 0 ? r['mv_'+h] : -r['mv_'+h])).mean : null;
  });
  html += `<div class="card"><h3>H2 in beeld — rendement per uitstapmoment, per sessie</h3>
    ${legend([{color:css('--s2'), label:'amc'}, {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-hyp-exit', 250)}
    <small>Alleen namen boven de conviction floor, want daar wordt op gehandeld. Als de
    twee lijnen tegengesteld hellen is dat H2; als ze parallel lopen is er één uitstap
    voor het hele boek en niet twee.</small></div>`;

  const secRows = Object.entries(bySec).map(([k,g]) => ({...side(g, k), sec:k}))
                        .sort((a,b)=>b.n-a.n);
  html += `<div class="card"><h3>H4 in tabel — alle sectoren</h3>` + table([
    {h:'sector', f:r=>esc(r.sec)}, {h:'n', f:r=>r.n},
    {h:'raak %', f:r=>r.hit===null?'–':n1(r.hit)},
    {h:'per naam', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'t', f:r=>n2(r.t)}], secRows) +
    `<small>Sector komt van Yahoo en is per ticker gecached. Met negen sectoren over
     ${rk.length} namen is de beste ervan per constructie goed — lees dit als de spreiding,
     niet als een keuze.</small></div>`;

  if (tilt !== null) {
    const cross = [];
    for (const [tl, tf] of [['tilt hoog', r=>r.retail_tilt>=tilt], ['tilt laag', r=>r.retail_tilt<tilt]])
      for (const [cl, cf] of [[`≥ ${FLOOR}`, r=>Math.abs(r.impact_sum)>=FLOOR],
                              [`< ${FLOOR}`, r=>Math.abs(r.impact_sum)<FLOOR]]) {
        const g = rk.filter(r => tf(r) && cf(r));
        if (g.length) cross.push({...side(g, `${tl} · conviction ${cl}`)});
      }
    html += `<div class="card"><h3>H3 × H6 — waar de twee elkaar raken</h3>` + table([
      {h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n},
      {h:'raak %', f:r=>r.hit===null?'–':n1(r.hit)},
      {h:'per naam', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
      {h:'t', f:r=>n2(r.t)}], cross) +
      `<small>Dit is de cel die een weegfactor zou raken als hij standhoudt: het is geen
       optelsom van twee effecten maar een interactie, en vier cellen over ${rk.length}
       namen is precies het aantal waarop een interactie er overtuigend uitziet zonder
       het te zijn.</small></div>`;
  }

  html += `<div class="warn"><b>Wat hiermee te doen.</b> Niets wegen. Kies één of twee
    regels, leg ze vandaag vast met een datum, en meet ze vooruit op dagen die nog niet
    bestaan. Elke regel die op deze ${dd.length} dagen is gekozen én op deze ${dd.length}
    dagen wordt beoordeeld, is per constructie goed.</div>`;

  draw.push(() => {
    lineChart(document.getElementById('c-hyp-exit'), {
      x: HZ.map(h=>HZ_CET[h]||h), sub: HZ, height:250, zero:true,
      fmtY:v=>v.toFixed(0)+'%', fmtT:pc,
      series:[{label:'amc', color:css('--s2'), values:curve('amc')},
              {label:'bmo', color:css('--s3'), values:curve('bmo')}],
      tipX:i=>`${HZ[i]} · ${HZ_CET[HZ[i]]||''} CET`});
  });
  return html;
}


/* ===================================================================== weging
   w2: the conviction floor stays the gate and the four factors set the SIZE. w1 let a
   tilt push a name over the floor and lost on exactly those names; this cannot, so a
   wrong factor costs size and never buys membership.

   The tab's job is to separate two things the headline number mixes: raising the
   per-name cap from 33% to 50% deploys more capital on thin days, and the weighting
   redistributes within a day. Those are a risk decision and a research claim, and they
   have to be read apart. */
function w2Weight(r) {
  const S = r.w2_strength || {};
  const sum = (S.evidence||0) + (S.retail||0) + (S.lean_agree||0) + (S.search_quiet||0);
  const g = (D.weighting_w2 && D.weighting_w2.g) || 0.125;
  return Math.max(0.5, Math.min(1.5, 1 + g * sum));
}
/* Same shape as the live sizer: pro rata, cap, redistribute what the cap refused. */
function allocate(rows, gross, cap, weighted) {
  const share = new Map();
  let live = rows.slice(), budget = gross;
  const w = r => weighted ? w2Weight(r) : 1;
  for (let i = 0; i <= rows.length; i++) {
    const tot = live.reduce((s,r)=>s+w(r), 0);
    if (!live.length || tot <= 0 || budget <= 1e-9) break;
    const capped = live.filter(r => budget * w(r) / tot >= cap - 1e-9);
    if (!capped.length) { live.forEach(r => share.set(r, budget * w(r) / tot)); break; }
    capped.forEach(r => share.set(r, cap));
    budget -= cap * capped.length;
    const drop = new Set(capped);
    live = live.filter(r => !drop.has(r));
  }
  return share;
}

function tabWeging() {
  const W2 = D.weighting_w2 || {};
  const FLOOR = D.conviction_floor ?? 3;
  const rk = rankRows().filter(r => r.impact_sum !== 0 && r.w2_strength
                                 && retOf(r) !== null && retOf(r) !== undefined);
  if (rk.length < 8) return `<div class="empty">te weinig rijen onder deze filters</div>`;
  const bk = rk.filter(r => Math.abs(r.impact_sum) >= FLOOR);   // NOT `book`: that is the global stats helper
  const dayGroups = byDay(bk).filter(g => g.length);

  const runBook = (gross, cap, weighted) => {
    const per = dayGroups.map(g => {
      const a = allocate(g, gross, cap, weighted);
      let ret = 0, dep = 0;
      g.forEach(r => { const sh = a.get(r) || 0; ret += sh * retOf(r) / 100; dep += sh; });
      return {d: g[0].run_date, ret, dep, n: g.length,
              top: g.reduce((b,r)=>(a.get(r)||0) > (a.get(b)||0) ? r : b, g[0]),
              topPct: Math.max(...g.map(r => a.get(r) || 0))};
    });
    const xs = per.map(p => p.ret);
    const s = ttest(xs);
    let cum = 1; xs.forEach(v => cum *= 1 + v/100);
    return {...s, per, cum: 100*(cum-1),
            green: xs.filter(v=>v>0).length,
            dep: per.reduce((a,p)=>a+p.dep,0) / (per.length || 1)};
  };
  const A = runBook(100, 33, false);
  const B = runBook(100, W2.max_pct_per_name ?? 50, false);
  const C = runBook(100, W2.max_pct_per_name ?? 50, true);
  const Dd = runBook(100, 33, true);
  const books = [{...A, label:'A · normale routine, gelijk gewicht, cap 33%'},
                 {...B, label:'B · alleen de cap naar 50%, nog steeds gelijk'},
                 {...C, label:'C · w2 gewogen, cap 50%'},
                 {...Dd, label:'D · w2-weging, cap terug op 33%'}];

  let html = `<p class="lead">De conviction floor blijft de poort: <b>geen enkele factor
    voegt een naam toe of haalt er een weg</b>. De vier factoren bepalen alleen hoeveel
    er per naam in gaat, en één naam mag tot <b>${W2.max_pct_per_name ?? 50}%</b> van het
    vermogen worden in plaats van de 33% die de stage nu gebruikt. Versie
    <b>${esc(W2.version || 'w2')}</b>, bevroren <b>${esc(W2.frozen || '—')}</b>.</p>`;

  html += `<div class="warn"><b>Twee dingen zitten in het kopgetal en ze horen apart.</b>
    De cap van 33% naar 50% zet meer geld aan het werk op dunne dagen; dat is een
    risicobesluit. De weging herverdeelt binnen een dag; dat is de onderzoeksclaim. Rij A
    tegen B isoleert de cap, B tegen C de weging. Lees ze niet als één getal.</div>`;

  html += `<div class="card"><h3>Vier boeken, dezelfde namen</h3>` + table([
    {h:'boek', f:r=>esc(r.label)},
    {h:'per dag', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'sd', f:r=>n2(r.sd)}, {h:'t', f:r=>n2(r.t)},
    {h:'samengesteld', f:r=>`<span class="${sgn(r.cum)}">${pc(r.cum)}</span>`},
    {h:'groene dagen', f:r=>`${r.green}/${r.n}`},
    {h:'gem. inzet', f:r=>n1(r.dep)+'%'},
    {h:'per eenheid inzet', f:r=>n3(100*r.mean/(r.dep||1))+'%'}],
    books.map(b => ({...b, n: b.per.length}))) +
    `<small>De laatste kolom is het rendement gedeeld door hoeveel van het vermogen
     daadwerkelijk aan het werk stond. Een boek dat alleen meer inzet is, wint op
     <i>per dag</i> en niet op deze kolom.</small></div>`;

  // table() hands the formatter the ROW and nothing else, so the paired day has to be
  // folded into the row rather than looked up by index.
  const perDay = A.per.map((a, i) => ({
    d: a.d, n: a.n, a: a.ret, c: C.per[i].ret, gap: C.per[i].ret - a.ret,
    top: C.per[i].top.ticker, topPct: C.per[i].topPct}));
  html += `<div class="card"><h3>Per dag, en waar de grootste positie zat</h3>` + table([
    {h:'dag', f:r=>esc(r.d)}, {h:'namen', f:r=>r.n},
    {h:'A normaal', f:r=>`<span class="${sgn(r.a)}">${pc(r.a)}</span>`},
    {h:'C w2', f:r=>`<span class="${sgn(r.c)}">${pc(r.c)}</span>`},
    {h:'verschil', f:r=>`<span class="${sgn(r.gap)}">${pc(r.gap)}</span>`},
    {h:'grootste in C', f:r=>`${esc(r.top)} ${n1(r.topPct)}%`}], perDay) + `</div>`;

  // THE FACTORS ARE JUDGED ON EVERY ONDERZOCHTE NAAM, NOT ON THE BOOK.
  // The conviction floor is the trading gate and stays the trading gate -- the four
  // books above are placed on `bk` and nothing here changes that. But a factor is a
  // claim about the hunt, and the hunt ranked roughly twice as many names as it
  // traded. Judging the factor on the traded half alone throws away the other half of
  // the evidence for no reason: the floor selects on |impact_sum|, which is not what
  // any of these four measure. Both columns are printed because they can disagree, and
  // a factor that only works on the side it was chosen from is the thing to catch.
  const S = ['evidence','retail','lean_agree','search_quiet'];
  const NL = {evidence:'meer findings', retail:'retail tilt', lean_agree:'lean wijst mee',
              search_quiet:'minder zoekverkeer'};
  const cell = rows => rows.length >= 5 ? book(rows.map(retOf)) : {n: rows.length};
  const rowsF = [];
  S.forEach(k => [1,-1].forEach(v => {
    const a = cell(rk.filter(r => (r.w2_strength||{})[k] === v));
    const b = cell(bk.filter(r => (r.w2_strength||{})[k] === v));
    if ((a.n || 0) + (b.n || 0) === 0) return;
    rowsF.push({k: `${NL[k]} ${v > 0 ? '+1' : '\u22121'}`, a, b,
                gap: (a.mean != null && b.mean != null) ? b.mean - a.mean : null});
  }));
  const num = (o, f) => o.n >= 5 ? f(o) : `<span class="muted">n=${o.n}</span>`;
  html += `<div class="card"><h3>De vier factoren, op alle onderzochte namen en op het boek</h3>` +
    table([
    {h:'factor', f:r=>`<code>${esc(r.k)}</code>`},
    {h:'n alle', f:r=>r.a.n},
    {h:'raak % alle', f:r=>num(r.a, o=>n1(o.hit))},
    {h:'per naam alle', f:r=>num(r.a, o=>`<span class="${sgn(o.mean)}">${pc(o.mean)}</span>`)},
    {h:'t alle', f:r=>num(r.a, o=>n2(o.t))},
    {h:'n boek', f:r=>r.b.n},
    {h:'raak % boek', f:r=>num(r.b, o=>n1(o.hit))},
    {h:'per naam boek', f:r=>num(r.b, o=>`<span class="${sgn(o.mean)}">${pc(o.mean)}</span>`)},
    {h:'t boek', f:r=>num(r.b, o=>n2(o.t))},
    {h:'verschil', f:r=>r.gap == null ? '—' : `<span class="${sgn(r.gap)}">${pc(r.gap)}</span>`}],
    rowsF) +
    `<small><b>Alle</b> is elke gerangschikte naam met een uitkomst onder deze filters
     (${rk.length}); <b>boek</b> is de deelverzameling boven de conviction floor
     (${bk.length}), de namen die daadwerkelijk gekocht zouden zijn. De vier boeken
     hierboven staan op de tweede kolomgroep; deze tabel staat er alleen om te zien of
     een factor buiten het boek hetzelfde doet. Een factor die alleen boven de floor
     werkt is niet weerlegd, maar hij is ook niet bevestigd op de helft van de namen die
     hem zou kunnen bevestigen. <code>meer findings</code> staat hier op instructie en
     draagt een voorbehoud dat de andere drie niet hebben: H7 mat <code>n_findings</code>
     op zichzelf als <i>geen effect</i>. Het is de enige factor zonder steun in het
     register en de eerste die eruit gaat als w2 tegenvalt.</small></div>`;

  // The below-floor half is the only part of the sample the factors were NOT chosen on:
  // every hypothesis in the register was asked of the traded book. It is not a clean
  // out-of-sample test -- same days, same hunters, and the names are there because the
  // hunt found little -- but a factor whose sign flips here was worth exactly the 56
  // names it was fitted to.
  const sub = rk.filter(r => Math.abs(r.impact_sum) < FLOOR);
  const rowsU = [];
  S.forEach(k => {
    const up = cell(sub.filter(r => (r.w2_strength||{})[k] === 1));
    const dn = cell(sub.filter(r => (r.w2_strength||{})[k] === -1));
    if (up.n >= 5 && dn.n >= 5)
      rowsU.push({k: NL[k], up, dn, gap: up.mean - dn.mean,
                  bookGap: (() => {
                    const a = cell(bk.filter(r => (r.w2_strength||{})[k] === 1));
                    const b = cell(bk.filter(r => (r.w2_strength||{})[k] === -1));
                    return (a.n >= 5 && b.n >= 5) ? a.mean - b.mean : null; })()});
  });
  html += `<div class="card"><h3>Het deel waar geen enkele factor op gekozen is</h3>
    <p class="lead">De ${sub.length} namen <i>onder</i> de conviction floor. Elke hypothese
    in het register is aan het boek gesteld, dus dit is het enige stuk van dezelfde dagen
    dat de factoren niet heeft gezien. Deze namen renderen als groep slecht
    (${pc(book(sub.map(retOf)).mean)} per naam tegen
    ${pc(book(bk.map(retOf)).mean)} boven de floor), dus lees het teken van het gat en
    niet het niveau.</p>` + table([
    {h:'factor', f:r=>`<code>${esc(r.k)}</code>`},
    {h:'+1', f:r=>`${r.up.n} · <span class="${sgn(r.up.mean)}">${pc(r.up.mean)}</span>`},
    {h:'\u22121', f:r=>`${r.dn.n} · <span class="${sgn(r.dn.mean)}">${pc(r.dn.mean)}</span>`},
    {h:'gat onder de floor', f:r=>`<span class="${sgn(r.gap)}">${pc(r.gap)}</span>`},
    {h:'gat in het boek', f:r=>r.bookGap == null ? '—'
        : `<span class="${sgn(r.bookGap)}">${pc(r.bookGap)}</span>`},
    {h:'zelfde teken', f:r=>r.bookGap == null ? '—'
        : ((r.gap > 0) === (r.bookGap > 0)
           ? '<span class="c-yes">ja</span>' : '<span class="c-anti">nee</span>')}],
    rowsU) +
    `<small>Geen van deze gaten haalt twee standaardfouten; ze zijn er om het teken te
     lezen, niet om iets te bevestigen. w2 verandert hier niets door: de floor blijft de
     poort en deze namen worden hoe dan ook niet gekocht.</small></div>`;

  html += `<div class="warn"><b>Wat de hogere cap kost.</b> De per-naam cap is het enige
    risicoinstrument in deze stage. Van 33% naar 50% betekent dat één print het vermogen
    met de helft van zijn eigen gat kan bewegen: het gat van 23% dat de rekening 4,5%
    bewoog bij een cap van 20% en ongeveer 7,5% bij 33%, beweegt hem ongeveer 11,5% bij
    50%. Er is niets bijgekomen dat dat compenseert, en w2 staat nergens aan — hij wordt
    naast de live regel berekend zodat de twee vergeleken kunnen worden.</div>`;
  return html;
}


/* ====================================================== de andere markten
   Stage EU, stage J, stage AU en stage CA: dezelfde jacht, dezelfde scorer, vier
   andere beurzen. Geen van vieren plaatst een order, dus er is hier geen geldniveau
   en er komt er geen: de ledger hierboven gaat over de Alpaca-rekening, die deze
   markten niet kent. Alles op deze tabbladen is het onderzoeksniveau.

   De gerealiseerde beweging komt uit de resolver van de markt zelf
   (eu_resolve.py, jp_resolve.py, au_resolve.py, ca_resolve.py) en nergens anders
   vandaan. Elk venster is anders: Europa en Australië rapporteren vóór de opening,
   Tokio na de slotbel. Die logica hoort in één bestand per markt te staan, niet ook hier. Staat
   er geen beweging, dan is de run nog niet opgelost. */
const MRAW = document.getElementById('markets');
const M = MRAW ? JSON.parse(MRAW.textContent) : {markets:{}, problems:[]};
const MS = {val:false, thr:0};
function mSet(k, v) {
  MS[k] = (k === 'thr' ? +v : v);
  /* De validatieknop kan een analysetabblad openen of sluiten, dus de rij wordt
     opnieuw gezet en hetzelfde tabblad bij naam teruggezocht. */
  if (MKT !== 'US') {
    const keep = TABS[active] && TABS[active][0];
    TABS = marketTabs(MKT);
    buildTabs(keep);
  }
  refresh();
}

const MNOTE = {
  EU: `Tien Europese markten in één stage: het VK, Frankrijk, Duitsland, Zweden,
       Denemarken, Noorwegen, Finland, Italië, Spanje en Polen. Het venster is
       <code>slot(D−1) → slot(D)</code>, want 339 van 379 gemeten Britse
       resultaten kwamen vóór 08:00 Londen. De baseline wordt twee uur vóór de
       Europese sluiting verzegeld, dus de verzegelde spot is een koers tijdens de
       handel en nooit een slotkoers. Er is geen optie-anker, en Spanje en Polen
       hebben ook geen short-register: hun <code>priced_lean_pct</code> ís de
       gratis benchmark, dus die namen kunnen die benchmark per definitie niet
       verslaan. De Nordics moeten binnen een week worden opgelost, want de Nasdaq
       Nordic-feed kent geen datumquery en gaat ongeveer twaalf dagen terug.`,
  JP: `Tokio. Geen optie-anker, dus de lean komt uit het JPX short-register, de
       verandering daarin en 信用倍率. Samen brengen die de
       <code>baseline_quality</code> op 0,725, tegen 0,40 toen de lean nog de run-up
       zelf was. Het venster loopt van de slotbel naar de volgende opening. De beurs
       is vaker dicht dan de cron: een lege dag met <code>market_closed</code> is een
       feestdag en geen storing.`,
  CA: `Toronto, en de reden is niet de agenda. Canada is de enige markt hier waar de
       <b>mét en zonder optie-anker</b> naast elkaar in één dag zitten: de Montréal
       Exchange noteert opties op 360 namen (96% boven $25m per dag, 10% eronder),
       terwijl het CIRO short-register 87–88% van élke omzetband dekt. Zo splitst
       één Canadese dag in een arm die precies als een Amerikaanse naam is verankerd
       en een arm die het als een Japanse of Europese doet, in dezelfde markt en
       door dezelfde scorer. Die vergelijking is de reden dat de stage bestaat; de
       rangschikking is bijvangst. Wat het kost: <code>sedarplus.ca</code> en
       <code>ciro.ca</code> zijn hier dicht, dus alles loopt via één stack bij TMX,
       en één storing is dan één storing en geen vier.`,
  AU: `De ASX. Het venster is <code>slot(D−1) → slot(D)</code>, want 91% van de
       gemeten Australische resultaten landt vóór de opening van 10:00 Sydney, en de
       Routine draait daarom zondag tot en met donderdag. Eén Engelse jachtronde,
       bewust geen tweede taalronde. Het ASIC-register is het enige
       positie-anker hier dat elk niveau publiceert in plaats van alleen boven
       0,5%, maar het loopt ongeveer vier handelsdagen achter. En de helft van de
       ASX levert een 4C- of 5B-kasstroomrapport in plaats van een winstcijfer:
       <code>filer_type</code> zegt welke van de twee.`,
};

const mRows = (code, allThr) => {
  const d = (M.markets || {})[code] || {names: [], runs: []};
  const val = new Set(d.runs.filter(r => r.validation_only).map(r => r.run));
  const thr = allThr ? 0 : MS.thr;
  return d.names.filter(r => (MS.val || !val.has(r.run))
                          && (!thr || Math.abs(r.impact_sum || 0) >= thr));
};
const mRuns = code => {
  const d = (M.markets || {})[code] || {runs: []};
  return d.runs.filter(r => MS.val || !r.validation_only);
};

/* Vijf namen is de ondergrens, en dat is geen preutsheid. Op drie namen komt een
   rangcorrelatie van precies 1,0 één keer op de zes toevallig uit. au_resolve.py
   schrijft dat zelf op, nadat de eerste synthetische Australische run er netjes
   een produceerde. */
const MMIN = 5;

function mStat(rows) {
  const v = rows.filter(r => r.realised_move_pct !== null
                          && r.realised_move_pct !== undefined
                          && r.impact_sum !== null && r.impact_sum !== undefined);
  const o = {n: v.length, rows: v};
  if (v.length >= MMIN) {
    o.rho = corr(ranks(v.map(r => r.impact_sum)),
                 ranks(v.map(r => r.realised_move_pct)));
    const ctl = v.filter(r => r.run_up_20d_pct !== null && r.run_up_20d_pct !== undefined);
    o.ctlN = ctl.length;
    o.ctl = ctl.length >= MMIN
      ? corr(ranks(ctl.map(r => -r.run_up_20d_pct)),
             ranks(ctl.map(r => r.realised_move_pct))) : null;
  }
  const signed = v.filter(r => r.impact_sum);
  o.signN = signed.length;
  o.signRight = signed.filter(r => r.sign_right).length;
  o.book = book(v.filter(r => r.ret !== null && r.ret !== undefined).map(r => r.ret));
  return o;
}

/* ---------------------------------------------------- de markt-tabbladen
   Eén context per render. Elk tabblad hieronder werkt op dezelfde gefilterde
   verzameling, zodat een getal op het ene tabblad en een getal op het andere
   over dezelfde namen gaan. */
function mCtx(code, allThr) {
  const d = (M.markets || {})[code] || null;
  if (!d) return null;
  const runs = mRuns(code), rows = mRows(code, allThr);
  /* Een naam zonder jacht is geen nul, het is een lege plek. Op 2026-09-23 bleven
     zeven Britse namen ongejaagd omdat de sessie geen subagenten kon starten, en
     die staan in edge-scores.json met impact_sum 0 en rankable false. Ze horen in
     de namentabel, want ze laten zien wat er is afgevallen, maar in geen enkel
     getal: een nul die niemand heeft gemeten trekt elke rangschikking naar het
     midden. */
  const ranked = rows.filter(r => r.rankable !== false);
  return {code, d, runs, rows, ranked,
          unranked: rows.length - ranked.length,
          st: mStat(ranked),
          hasVal: d.runs.some(r => r.validation_only),
          floor: (d.runs.find(r => r.conviction_floor) || {}).conviction_floor || 3,
          hunted: runs.filter(r => r.n_rows > 0),
          resolved: ranked.filter(r => r.realised_move_pct !== null
                                    && r.realised_move_pct !== undefined)};
}

const MNAAM = {EU:'Europa', JP:'Japan', AU:'Australië', CA:'Canada'};

/* De twee knoppen die elk markttabblad deelt. `want` zegt welke van de twee er
   iets onder zich hebben: een drempel op de runtabel filtert niets. */
function mControls(c, want) {
  if (want === 'none') return '';
  let h = `<div class="mctl">`;
  if (want !== 'val') h += `<span class="seg" role="group" aria-label="conviction-drempel">
      <button aria-pressed="${!MS.thr}" onclick="mSet('thr',0)">alle namen</button>
      <button aria-pressed="${MS.thr === c.floor}" onclick="mSet('thr',${c.floor})">|impact_sum| ≥ ${c.floor}</button>
    </span>`;
  if (c.hasVal) h += `<span class="seg" role="group" aria-label="validatieruns">
      <button aria-pressed="${!MS.val}" onclick="mSet('val',false)">alleen echte runs</button>
      <button aria-pressed="${MS.val}" onclick="mSet('val',true)">validatieruns meetellen</button>
    </span>
    <span class="hint">Een validatierun draaide op <b>synthetische</b> vondsten om de keten
      te testen. Die namen zijn geen onderzoek en horen standaard niet in een getal.</span>`;
  return h + `</div>`;
}

/* Elk markttabblad begint hier: geen marktbestand, of geen run op schijf, en dan
   is er niets te tonen en zegt het tabblad dat in plaats van nullen te zetten. */
function mGuard(c, code) {
  if (!c) return `<div class="card warnbox"><h3>Geen marktbestand</h3>
    <p>De bouw vond geen <code>dashboard/data/markets.json</code>. Draai
    <code>python3 dashboard/scripts/build_markets.py</code> en bouw opnieuw.</p></div>`;
  if (!c.d.runs.length) return `<div class="card warnbox"><h3>Nog geen run op schijf</h3>
    <p>Er staat geen enkele map onder <code>research/*/*/*/${esc(c.d.dir)}/</code>, dus
    valt er niets te tonen: geen nul, geen leeg getal, geen tabel. De stage bestaat wel
    en heeft zijn eigen Routine; wat ontbreekt is een fire die iets heeft gepubliceerd.</p>
    <p>De validatie van deze stage is buiten <code>research/</code> gedraaid en is hier
    dus ook niet te zien. Zodra één fire publiceert, vullen deze tabbladen zich vanzelf.</p></div>`;
  return null;
}

/* Waarom een getal ontbreekt, in de taal van wat het nodig heeft. Elk
   analysetabblad dat nog niet kan rekenen, eindigt hier en niet in een lege
   tabel: een leeg vak leest als een meting die nul opleverde. */
function mNeeds(c, need) {
  const pend = c.runs.filter(r => !r.has_resolved_file && r.n_rows).length;
  if (!c.st.n) return `<div class="card warnbox"><h3>Nog niets opgelost</h3>
    <p>Er is in ${MNAAM[c.code]} nog geen enkele naam met een gerealiseerde beweging, dus
    staat hier geen prestatiegetal. Dat is de stand, niet een fout in dit tabblad.</p>
    <p>Van de ${c.runs.length} runs hebben er ${pend} nog geen
    <code>${esc(c.d.resolved_file)}</code>. Een run wordt pas oplosbaar als zijn venster
    dicht is; daarna vult dit tabblad zich vanzelf met
    <code>python3 dashboard/scripts/build_markets.py --resolve</code>, of per dag met
    <code>python3 ${esc(c.d.resolver)} --run &lt;rundir&gt; -o &lt;rundir&gt;/${esc(c.d.resolved_file)}</code>.</p></div>`;
  return `<div class="card warnbox"><h3>${c.st.n} opgeloste namen, en dit vraagt er ${need}</h3>
    <p>Op drie namen komt een rangcorrelatie van precies 1,0 één keer op de zes toevallig
    uit; <code>au_resolve.py</code> schrijft dat zelf op nadat de eerste synthetische
    Australische run er netjes een produceerde. Onder ${need} namen staat hier daarom niets
    in plaats van een getal dat blijft hangen. De namen zelf staan op <b>Namen</b>.</p></div>`;
}

/* ------------------------------------------------------------- Overzicht */
function mtOverzicht(code) {
  const c = mCtx(code);
  const g = mGuard(c, code);
  let html = `<p class="lead">${MNOTE[code]}</p>`;
  if (g) return html + g;

  html += mControls(c, 'both');
  html += tiles([
    {k:'jachtdagen', v:c.hunted.length, s:`${c.runs.length} runs in de map`},
    {k:'namen', v:c.ranked.length,
     s: (MS.thr ? `boven ${MS.thr}` : 'gejaagd en gerangschikt')
        + (c.unranked ? ` · ${c.unranked} ongejaagd` : '')},
    {k:'vondsten', v:c.ranked.reduce((s,r)=>s+(r.n_findings||0),0), s:'over die namen'},
    {k:'opgelost', v:c.st.n, s:'met een gerealiseerde beweging'},
    {k:'teken goed', v: c.st.signN ? `${c.st.signRight}/${c.st.signN}` : '–',
     s: c.st.signN ? n1(100*c.st.signRight/c.st.signN) + '%' : 'nog niets opgelost'}]);

  if (c.st.n >= MMIN) {
    html += `<div class="card"><h3>Waar het vandaag op staat</h3>` +
      table([{h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n}, {h:'ρ', f:r=>n3(r.rho)}],
        [{label:'de jacht · impact_sum', n:c.st.n, rho:c.st.rho},
         {label:'gratis controle · −run_up_20d_pct', n:c.st.ctlN, rho:c.st.ctl}]) +
      `<p class="meta">Uitgesplitst op <b>Score</b>, per drempel op <b>Drempel</b>.</p></div>`;
  } else {
    html += mNeeds(c, MMIN);
  }

  /* Welke tabbladen er nog niet staan, en wat ze openzet. Zonder deze regel is
     een korte tabbladenrij niet te onderscheiden van een dashboard dat die
     analyses niet kent. */
  const cg = mCtx(code, true);
  const gated = MTABDEFS.filter(t => (!t.only || t.only === code)
                                  && t.when && !t.when(cg));
  if (gated.length) html += `<div class="card"><h3>Wat hier nog niet staat</h3>
    <p>Deze markt heeft de tabbladen van de VS, maar een tabblad verschijnt pas als zijn
    data het draagt. Nog dicht:</p>` + table([
      {h:'tabblad', f:r=>`<b>${esc(r.name)}</b>`},
      {h:'gaat open bij', f:r=>esc(r.needs)}],
      gated.map(t => ({name:t.name, needs:t.needs}))) + `</div>`;

  if ((M.problems || []).length) html += `<div class="card warnbox"><h3>Problemen bij het verzamelen</h3>
    <ul>${M.problems.map(p => `<li>${esc(p)}</li>`).join('')}</ul></div>`;
  return html;
}

/* ----------------------------------------------------------------- Score */
function mtScore(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  let html = mControls(c, 'both');
  if (c.st.n < MMIN) return html + mNeeds(c, MMIN);

  html += `<div class="card"><h3>Rangschikking tegen de gerealiseerde beweging</h3>` +
    table([{h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n}, {h:'ρ', f:r=>n3(r.rho)}],
      [{label:'de jacht · impact_sum', n:c.st.n, rho:c.st.rho},
       {label:'gratis controle · −run_up_20d_pct', n:c.st.ctlN, rho:c.st.ctl}]) +
    `<p class="meta">Eén pool over alle dagen, niet per dag gecentreerd: daar zijn het er
     nog niet genoeg voor. Geen permutatietest en geen correctie voor meervoudig toetsen:
     op ${c.st.n} namen zou allebei meer precisie suggereren dan er is. De jacht moet de
     gratis controle verslaan om iets te hebben vastgesteld; gelijk spel is geen
     resultaat.</p></div>`;

  if (c.st.book.n) html += `<div class="card"><h3>Bord-rendement</h3>` +
    table(BOOKCOLS, [bookRow('elke opgeloste naam, in de richting van het teken', c.st.book)].filter(Boolean)) +
    `<p class="meta">Bord-rendement: de beweging in de richting van het teken van
     <code>impact_sum</code>. Deze stage plaatst geen orders, dus er zit geen spread, geen
     instapmoment en geen uitvoering in. Dit is wat het onderzoek zei, niet wat het
     opbracht.</p></div>`;

  const bySess = ['amc','bmo'].map(s => {
    const g2 = c.resolved.filter(r => r.session === s);
    return g2.length ? {label:s, ...book(g2.map(r=>r.ret).filter(x=>x!==null&&x!==undefined)),
                        rho: g2.length >= MMIN
                          ? corr(ranks(g2.map(r=>r.impact_sum)), ranks(g2.map(r=>r.realised_move_pct)))
                          : null} : null;
  }).filter(Boolean);
  if (bySess.length) html += `<div class="card"><h3>Per sessie</h3>` + table([
    {h:'sessie', f:r=>`<b>${esc(r.label)}</b>`}, {h:'n', f:r=>r.n},
    {h:'raak %', f:r=>n1(r.hit)}, {h:'gem. %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'ρ', f:r=>n3(r.rho)}], bySess) +
    `<p class="meta">De VS-steekproef splitst hier hard uiteen: amc en bmo willen tegengestelde
     uitstapmomenten. Of dat elders ook zo is, is precies wat deze rij moet uitwijzen, en
     twee cijfers per sessie zeggen er nog niets over.</p></div>`;
  return html;
}

/* --------------------------------------------------------------- Drempel */
const MTHR = [0, 1, 2, 3, 4, 5, 6, 8];
function mtDrempel(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  let html = mControls(c, 'val');
  if (c.st.n < MDREMPEL) return html + mNeeds(c, MDREMPEL);

  const rows = MTHR.map(t => {
    const g2 = c.resolved.filter(r => Math.abs(r.impact_sum) >= t);
    if (g2.length < 3) return null;
    const b = book(g2.map(r=>r.ret).filter(x=>x!==null&&x!==undefined));
    return {t, n:g2.length, hit:b.hit, mean:b.mean,
            rho: g2.length >= MMIN
              ? corr(ranks(g2.map(r=>r.impact_sum)), ranks(g2.map(r=>r.realised_move_pct)))
              : null};
  }).filter(Boolean);

  html += `<div class="card"><h3>De drempel doorgerekend</h3>` + table([
    {h:'|impact_sum| ≥', f:r=>`<b>${n1(r.t)}</b>`},
    {h:'namen', f:r=>r.n},
    {h:'teken goed %', f:r=>n1(r.hit)},
    {h:'bord %', f:r=>`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'ρ', f:r=>n3(r.rho)}], rows) +
    `<p class="meta">De conviction-floor is de enige regel in dit onderzoek die in de VS ooit
     een familiegewijze correctie doorstond, en hij is daar op dertien dagen gekozen. Deze
     tabel toont of hij hier iets doet; hij is géén uitnodiging om de drempel te verzetten op
     de dagen die hem hebben voortgebracht. De rij met de hoogste waarde is bijna altijd de
     rij met de minste namen.</p></div>`;
  return html;
}

/* --------------------------------------------------------------- Aanloop */
function mtAanloop(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  let html = mControls(c, 'both');
  if (c.st.n < MMIN) return html + mNeeds(c, MMIN);

  const ctl = (key, label) => {
    const v = c.resolved.filter(r => r[key] !== null && r[key] !== undefined);
    if (v.length < MMIN) return {label, n:v.length, rho:null, agree:null, dis:null};
    const rho = corr(ranks(v.map(r => -r[key])), ranks(v.map(r => r.realised_move_pct)));
    const A = v.filter(r => (r.impact_sum > 0) === (r[key] < 0));
    const B = v.filter(r => (r.impact_sum > 0) !== (r[key] < 0));
    return {label, n:v.length, rho,
            agree: A.length ? book(A.map(r=>r.ret)).mean : null, an:A.length,
            dis: B.length ? book(B.map(r=>r.ret)).mean : null, bn:B.length};
  };
  html += `<div class="card"><h3>De aanloop naar de print</h3>` + table([
    {h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n}, {h:'ρ tegen de beweging', f:r=>n3(r.rho)},
    {h:'eens met de jacht', f:r=>r.agree===null?'–':`${pc(r.agree)} <span class="meta">(${r.an})</span>`},
    {h:'oneens', f:r=>r.dis===null?'–':`${pc(r.dis)} <span class="meta">(${r.bn})</span>`}],
    [ctl('run_up_20d_pct','−run-up 20 sessies · de gratis controle'),
     ctl('run_up_5d_pct','−run-up 5 sessies')]) +
    `<p class="meta">De gratis controle is één getal uit de verzegelde baseline, beschikbaar
     vóór er één subagent draait. In de VS gaven de twee deelverzamelingen — alle namen en het
     verhandelde boek — tegengestelde tekens met overlappende intervallen, wat ruis is die
     twee keer is gemeten. Lees deze tabel dus als twee getallen naast elkaar en niet als een
     regel. Bij stage J is <code>run_up_5d_pct</code> apart verzegeld omdat de 20-daagse de
     beweging verborg die ertoe deed.</p></div>`;
  return html;
}

/* ----------------------------------------------------- Deelmarkt (alleen EU) */
function mtDeelmarkt(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  let html = mControls(c, 'both');
  const subs = [...new Set(c.ranked.map(r => r.submarket))].sort();
  const rows = subs.map(s => {
    const g2 = c.ranked.filter(r => r.submarket === s);
    const res = g2.filter(r => r.realised_move_pct !== null && r.realised_move_pct !== undefined);
    const t = g2.map(r=>r.turnover_usd).filter(x=>x!==null&&x!==undefined).sort((a,b)=>a-b);
    return {sub:s, n:g2.length, res:res.length,
            anch:g2.filter(r=>r.anchor_covered).length,
            turn: t.length ? t[Math.floor(t.length/2)] : null,
            find: g2.reduce((a,r)=>a+(r.n_findings||0),0),
            mean: res.length ? book(res.map(r=>r.ret)).mean : null,
            rho: res.length >= MMIN
              ? corr(ranks(res.map(r=>r.impact_sum)), ranks(res.map(r=>r.realised_move_pct)))
              : null};
  });
  html += `<div class="card"><h3>Per deelmarkt</h3>` + table([
    {h:'markt', f:r=>`<b>${esc(r.sub)}</b>`}, {h:'namen', f:r=>r.n},
    {h:'vondsten', f:r=>r.find}, {h:'opgelost', f:r=>r.res},
    {h:'anker', f:r=>`${r.anch}/${r.n}`},
    {h:'mediane omzet', f:r=>usdM(r.turn)},
    {h:'bord %', f:r=>r.mean===null?'–':`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'ρ', f:r=>n3(r.rho)}], rows) +
    `<p class="meta">Een dag kan één markt zijn: 15 van de 20 namen waren Zweeds op
     2026-10-22. De trekking is bewust <b>niet</b> gestratificeerd, want een quotum per markt
     is een tweede selectie die de scorer niet ziet, en deze stage heeft al één keer betaald
     voor een snede die hij niet kon zien. <code>anker</code> telt de namen die het
     short-register van hun eigen markt noemt; Spanje en Polen hebben er geen, dus hun
     <code>priced_lean_pct</code> ís de gratis controle en die namen kunnen die benchmark per
     definitie niet verslaan. Een gepoolde ρ die niet zegt hoeveel ervan <code>es</code> en
     <code>pl</code> is, wordt oververkocht.</p></div>`;
  return html;
}

/* ------------------------------------------------- Ankerarm (alleen Canada) */
function mtAnker(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  let html = mControls(c, 'both');
  const arm = v => {
    const g2 = c.ranked.filter(r => r.anchor_covered === v);
    const res = g2.filter(r => r.realised_move_pct !== null && r.realised_move_pct !== undefined);
    return {label: v ? 'mét optie-anker' : 'zonder, alleen het short-register',
            n:g2.length, res:res.length,
            mean: res.length ? book(res.map(r=>r.ret)).mean : null,
            rho: res.length >= MMIN
              ? corr(ranks(res.map(r=>r.impact_sum)), ranks(res.map(r=>r.realised_move_pct)))
              : null};
  };
  html += `<div class="card"><h3>De twee ankerarmen</h3>` + table([
    {h:'', f:r=>esc(r.label)}, {h:'namen', f:r=>r.n}, {h:'opgelost', f:r=>r.res},
    {h:'bord %', f:r=>r.mean===null?'–':`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'ρ', f:r=>n3(r.rho)}], [arm(true), arm(false)]) +
    `<p class="meta">Dit is de reden dat stage CA bestaat, en niet de agenda. Canada is de
     enige markt hier waar beide regimes in <b>één dag namen</b> zitten: de Montréal Exchange
     noteert opties op 360 namen, het CIRO short-register dekt 87–88% van elke omzetband.
     <code>archive/backtest/FINDINGS.md</code> §33 prijsde het ankerloze regime op ρ=+0,073
     (p=0,45) over 104 events en kon het anker niet scheiden van de markt waarin het gemeten
     was. Deze tabel houdt de markt vast en scheidt ze wel — zodra er iets is opgelost. De
     validatierun van 2026-08-13 verzegelde met Toronto dicht, dus alle 19 namen landden op de
     registerarm en de optiearm is door geen enkele echte run aangeraakt.</p></div>`;
  return html;
}

/* ------------------------------------------- Filer-type (alleen Australië) */
function mtFiler(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  let html = mControls(c, 'both');
  const kinds = [...new Set(c.ranked.map(r => r.filer_type || 'onbekend'))].sort();
  const rows = kinds.map(k => {
    const g2 = c.ranked.filter(r => (r.filer_type || 'onbekend') === k);
    const res = g2.filter(r => r.realised_move_pct !== null && r.realised_move_pct !== undefined);
    return {k, n:g2.length, res:res.length,
            mean: res.length ? book(res.map(r=>r.ret)).mean : null,
            rho: res.length >= MMIN
              ? corr(ranks(res.map(r=>r.impact_sum)), ranks(res.map(r=>r.realised_move_pct)))
              : null};
  });
  html += `<div class="card"><h3>Winstcijfer of kasstroomrapport</h3>` + table([
    {h:'soort', f:r=>`<b>${esc(r.k)}</b>`}, {h:'namen', f:r=>r.n}, {h:'opgelost', f:r=>r.res},
    {h:'bord %', f:r=>r.mean===null?'–':`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
    {h:'ρ', f:r=>n3(r.rho)}], rows) +
    `<p class="meta">De helft van de ASX levert een Appendix 4C of 5B kwartaalrapport onder
     Listing Rule 4.7B in plaats van een winstcijfer. Dat is een echt koersbewegend event —
     de elf waargenomen van IperionX hebben een mediane absolute reactie van 4,66% — maar met
     een volstrekt andere lat. Een gepoolde ρ die de mix niet noemt, verbergt twee
     verschillende vragen in één getal.</p></div>`;
  return html;
}

/* ----------------------------------------------- Lessons en de taalcontrole */
function mDelta(c, key, title, note) {
  const v = c.ranked.filter(r => r[key] !== null && r[key] !== undefined);
  if (!v.length) return `<div class="card warnbox"><h3>${title}: nog geen bevroren draft</h3>
    <p>Geen enkele naam draagt <code>${esc(key)}</code>. ${note}</p></div>`;
  const res = v.filter(r => r.realised_move_pct !== null && r.realised_move_pct !== undefined);
  let h = `<div class="card"><h3>${title}</h3>`;
  if (res.length >= MMIN) h += table(
    [{h:'', f:r=>esc(r.label)}, {h:'n', f:r=>r.n}, {h:'ρ', f:r=>n3(r.rho)},
     {h:'bord %', f:r=>r.mean===null?'–':`<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`}],
    [{label:'vóór', n:res.length,
      rho: corr(ranks(res.map(r=>r[key])), ranks(res.map(r=>r.realised_move_pct))),
      mean: book(res.map(r => r[key] > 0 ? r.realised_move_pct : -r.realised_move_pct)).mean},
     {label:'ná', n:res.length,
      rho: corr(ranks(res.map(r=>r.impact_sum)), ranks(res.map(r=>r.realised_move_pct))),
      mean: book(res.map(r=>r.ret)).mean}]);
  else h += `<p class="meta">${res.length} van deze ${v.length} namen is opgelost, dus er staat
    hier geen ρ. Het verschil per naam is wel al zichtbaar.</p>`;
  h += table([
    {h:'dag', f:r=>r.run_date},
    ...(c.code === 'EU' ? [{h:'mkt', f:r=>esc(r.submarket)}] : []),
    {h:'ticker', f:r=>`<b>${esc(r.ticker)}</b>`},
    {h:'vóór', f:r=>n1(r[key])}, {h:'ná', f:r=>n1(r.impact_sum)},
    {h:'verschil', f:r=>`<span class="${sgn(r.impact_sum-r[key])}">${n1(r.impact_sum-r[key])}</span>`},
    {h:'beweging', f:r=>r.realised_move_pct===null||r.realised_move_pct===undefined
        ? '<span class="meta">niet opgelost</span>' : pc(r.realised_move_pct)}], v);
  return h + `<p class="meta">${note}</p></div>`;
}

function mtLessons(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  return mControls(c, 'both') + mDelta(c, 'impact_sum_pre_lessons', 'Vóór en ná LESSONS.md',
    `De hunter maakt zijn sommen eerst met alleen de baseline, dat wordt bevroren als
     <code>pre_lessons</code>, daarna leest hij het bestand en herziet. Het bestand kan
     daardoor geen zoektocht meer sturen, alleen een omvang en een selectie. Let op de
     valkuil die stage EU al één keer maakte: draait één context beide hunts en heeft die
     <code>LESSONS.md</code> al gelezen, dan is de freeze per constructie gelijk aan de
     uitkomst en meet dit niets. ${code === 'AU' || code === 'CA'
       ? 'Het LESSONS.md van deze markt is bewust nog leeg tot er een run oplost.' : ''}`);
}

function mtTaal(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  const uk = c.ranked.filter(r => r.submarket === 'uk'
                               && r.impact_sum_pre_local !== null
                               && r.impact_sum_pre_local !== undefined).length;
  return mControls(c, 'both') + mDelta(c, 'impact_sum_pre_local', 'Vóór en ná de lokale ronde',
    `<b>Deze controle is op 2026-09-22 gestopt en dit tabblad is geschiedenis.</b> Tot die
     dag draaide elke hunter eerst Engels, werd die versie bevroren als
     <code>pre_local</code>, en pas daarna de ronde in de eigen taal; dat mat of zoeken in
     het Duits, Frans, Italiaans, Pools, Spaans of een Scandinavische taal rangcorrelatie
     oplevert of alleen tokens kost. De hunters doen nu één tweetalige ronde, dus een run
     die na die datum is verzegeld staat hier niet en dat is geen fout. <b>Er was nog geen
     Europese dag opgelost toen de freeze liep</b>, dus deze meting heeft nooit één getal
     tegen een echte uitkomst opgeleverd; wat is opgegeven is een toekomstig cijfer en geen
     resultaat. Wat ervoor in de plaats komt is <code>language_note</code> per hunt: proza,
     niet te rangschikken, en niet zichtbaar op deze pagina.
     <b>Het Britse geval was ontaard en telde niet mee</b>: de tweede ronde varieerde daar
     bronlokaliteit (RNS, Investegate, de vakpers) en geen taal, dus <code>eu_resolve.py</code>
     weigert dat verschil te poolen met het Duitse en Franse. ${uk ? `Er staan ${uk} Britse
     namen in deze tabel; lees hun verschil apart.` : ''}`);
}

/* ----------------------------------------------------------------- Namen */
function mtNamen(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  const shown = [...c.rows].sort((a,b) => (b.run_date).localeCompare(a.run_date)
                                       || Math.abs(b.impact_sum||0) - Math.abs(a.impact_sum||0));
  return mControls(c, 'both') + `<div class="card"><h3>Elke gerangschikte naam</h3>` + table([
    {h:'dag', f:r=>r.run_date},
    ...(code === 'EU' ? [{h:'mkt', f:r=>esc(r.submarket)}] : []),
    {h:'ticker', f:r=>`<b>${esc(r.ticker)}</b>`},
    {h:'bedrijf', f:r=>esc((r.company||'').slice(0,34))},
    {h:'sessie', f:r=>esc(r.session)},
    {h:'impact_sum', f:r=> r.rankable === false
        ? `<span class="meta">${esc(r.not_rankable_because || 'niet gerangschikt')}</span>`
        : `<span class="${sgn(r.impact_sum)}">${n1(r.impact_sum)}</span>`},
    {h:'vondsten', f:r=>r.n_findings},
    {h:'lean %', f:r=>n2(r.priced_lean_pct)},
    {h:'run-up 20d', f:r=>pc(r.run_up_20d_pct)},
    {h:'omzet/dag', f:r=>usdM(r.turnover_usd)},
    ...(code === 'AU' ? [{h:'soort', f:r=>esc(r.filer_type || '–')}] : []),
    {h:'anker', f:r=>r.anchor_covered === true ? 'ja' : r.anchor_covered === false ? 'nee' : '–'},
    {h:'beweging', f:r=>r.realised_move_pct === null || r.realised_move_pct === undefined
        ? `<span class="meta">${r.move_pending ? 'wacht op bar' : 'niet opgelost'}</span>`
        : pc(r.realised_move_pct)},
    {h:'bord %', f:r=>r.ret === null || r.ret === undefined ? '–'
        : `<span class="${sgn(r.ret)}">${pc(r.ret)}</span>`},
  ], shown) + `<p class="meta"><code>impact_sum</code> is de som van de door de hunter
    opgegeven maten, in punten spot, zonder richtinglabel en zonder drempel. Een rij die
    <b>${'niet gerangschikt'}</b> zegt, is niet gejaagd en telt in geen enkel getal mee.</p></div>`;
}

/* ------------------------------------------------------------------ Runs */
function mtRuns(code) {
  const c = mCtx(code), g = mGuard(c, code);
  if (g) return g;
  return mControls(c, 'val') + `<div class="card"><h3>Elke run op schijf</h3>` + table([
    {h:'dag', f:r=>`<b>${esc(r.run_date)}</b>`},
    {h:'namen', f:r=>r.n_rows || (r.quiet_reason ? `<span class="meta">${esc(r.quiet_reason)}</span>` : 0)},
    {h:'hunters', f:r=>r.n_hunts},
    {h:'vondsten', f:r=>r.n_findings},
    {h:'opgelost', f:r=>r.n_rows ? `${r.n_resolved}/${r.n_rows}` : '–'},
    {h:'gedood', f:r=>r.n_killed || '–'},
    {h:'lean vs controle', f:r=>n2((r.resolver_stats||{}).lean_vs_free_control_rho)},
    {h:'trekking', f:r=>{
      const s = r.selection || {};
      const mc = (s.market_concentration || {});
      return mc.largest_market
        ? `${esc(mc.largest_market)} ${n1(100*(mc.largest_market_share||0))}%`
        : (s.eligible !== undefined ? `${s.hunted ?? '–'}/${s.eligible}` : '–');
    }},
    {h:'soort', f:r=>r.validation_only ? '<span class="meta">validatie</span>' : 'echt'},
  ], c.runs) + `<p class="meta"><b>gedood</b> is <code>event_occurred: false</code>: het venster
    ging voorbij en er kwam geen publicatie, dus de naam valt uit elke rangschikking. <b>lean vs
    controle</b> is het alarm van de resolver — loopt die richting 1,0, dan is het register
    gestopt met laden en ís de lean de gratis controle geworden; leeg betekent dat de resolver
    hem niet berekende, meestal wegens te weinig namen. <b>trekking</b> is hoeveel van de
    in aanmerking komende namen gejaagd zijn, en voor Europa hoe geconcentreerd die dag in één
    markt zat.</p></div>`;
}

/* ------------------------------------------------------------------ Data */
function mtData(code) {
  const c = mCtx(code);
  if (!c) return mGuard(c, code);
  let html = `<p class="lead">Waar deze cijfers vandaan komen en wat er niet in zit.</p>`;
  html += `<div class="card"><h3>Herkomst</h3><ul>
    <li>Stage <b>${esc(c.d.stage)}</b>, runmap <code>research/*/*/*/${esc(c.d.dir)}/</code></li>
    <li>Verzamelaar: <code>dashboard/scripts/build_markets.py</code> →
        <code>dashboard/data/markets.json</code>, gebouwd ${esc(M.generated_utc || '–')}</li>
    <li>Resolver: <code>${esc(c.d.resolver)}</code>, schrijft
        <code>${esc(c.d.resolved_file)}</code> in de runmap</li>
    <li>Scorer: <code>researcher_us/scripts/edge_score.py</code>, ongewijzigd gedeeld met
        de VS — een Amerikaanse run herscoort identiek</li>
    <li>${c.d.n_runs} runs · ${c.d.n_names} namen · ${c.d.n_resolved} met een gerealiseerde
        beweging</li></ul></div>`;
  html += `<div class="card warnbox"><h3>Wat hier bewust niet staat</h3>
    <p><b>Er is geen geldniveau.</b> Deze stage plaatst geen orders: geen broker, geen fills,
    geen equity-curve. De handels-, capaciteits-, kosten- en wegingstabbladen van de VS bestaan
    hier daarom niet, en de ledger van stage E zegt niets over deze markt. Elk getal hier is
    bord-rendement: de koersbeweging in de richting van het teken, zonder spread en zonder
    uitvoering.</p>
    <p><b>Het venster is niet van dit dashboard.</b> Europa en Australië rapporteren vóór de
    opening, dus daar loopt het van <code>slot(D−1)</code> tot <code>slot(D)</code>; Tokio loopt
    van de slotbel naar de volgende opening. Die logica hoort in de resolver van de markt zelf
    en staat nergens hier. Een gerealiseerde beweging op deze tabbladen is door die resolver
    berekend of hij staat er niet.</p></div>`;
  html += `<div class="card"><h3>Per run</h3>` + table([
    {h:'dag', f:r=>`<b>${esc(r.run_date)}</b>`},
    {h:'event', f:r=>esc(r.event_date)},
    {h:'verzegeld', f:r=>esc((r.sealed_utc||'–').slice(0,16).replace('T',' '))},
    {h:'gescoord', f:r=>esc((r.scored_utc||'–').slice(0,16).replace('T',' '))},
    {h:'opgelost', f:r=>esc((r.resolved_utc||'–').slice(0,16).replace('T',' '))},
    {h:'sleutel', f:r=>esc(r.ranking_key || '–')},
    {h:'floor', f:r=>n1(r.conviction_floor)},
    {h:'cap', f:r=>r.cap ?? '–'},
    {h:'omzetdrempel', f:r=>usdM(r.min_turnover_usd)}], c.d.runs) + `</div>`;
  if ((M.problems || []).length) html += `<div class="card warnbox"><h3>Problemen bij het verzamelen</h3>
    <ul>${M.problems.map(p => `<li>${esc(p)}</li>`).join('')}</ul></div>`;
  return html;
}

/* De suite per markt. `when` bepaalt of een tabblad vandaag iets onder zich
   heeft; wat dicht is, staat met zijn voorwaarde op Overzicht, zodat een korte
   rij niet leest als een dashboard dat die analyse niet kent. */
const MDREMPEL = 10;
const MTABDEFS = [
  {name:'Overzicht', fn:mtOverzicht},
  {name:'Score',     fn:mtScore,     needs:`${MMIN} opgeloste namen`,
   when:c => c.st.n >= MMIN},
  {name:'Drempel',   fn:mtDrempel,   needs:`${MDREMPEL} opgeloste namen`,
   when:c => c.st.n >= MDREMPEL},
  {name:'Aanloop',   fn:mtAanloop,   needs:`${MMIN} opgeloste namen`,
   when:c => c.st.n >= MMIN},
  {name:'Deelmarkt', fn:mtDeelmarkt, needs:'een gejaagde naam', only:'EU',
   when:c => c.ranked.length > 0},
  {name:'Ankerarm',  fn:mtAnker,     needs:'een naam met een ankerstatus', only:'CA',
   when:c => c.ranked.some(r => r.anchor_covered !== null && r.anchor_covered !== undefined)},
  {name:'Soort',     fn:mtFiler,     needs:'een naam met een filer_type', only:'AU',
   when:c => c.ranked.some(r => r.filer_type)},
  {name:'Lessons',   fn:mtLessons,   needs:'een bevroren pre_lessons-draft',
   when:c => c.ranked.some(r => r.impact_sum_pre_lessons !== null
                             && r.impact_sum_pre_lessons !== undefined)},
  {name:'Taal',      fn:mtTaal,      needs:'een run van vóór 2026-09-22 met een bevroren pre_local-draft', only:'EU',
   when:c => c.ranked.some(r => r.impact_sum_pre_local !== null
                             && r.impact_sum_pre_local !== undefined)},
  {name:'Namen',     fn:mtNamen,     needs:'een gejaagde naam',
   when:c => c.rows.length > 0},
  {name:'Runs',      fn:mtRuns,      needs:'een run op schijf',
   when:c => c.runs.length > 0},
  {name:'Data',      fn:mtData},
  {name:'Index',     fn:() => tabIndex()},
];

function marketTabs(code) {
  const c = mCtx(code, true);
  return byGroup(MTABDEFS
    .filter(t => !t.only || t.only === code)
    .filter(t => !t.when || !c || t.when(c))
    .map(t => [t.name, () => t.fn(code), 1]));
}

/* Op groep sorteren, stabiel. De rij tekent een groepskop zodra de groep
   verandert, dus een groep die niet aaneengesloten staat, krijgt twee koppen —
   op de Europese rij stond DOORSNEDES twee keer omdat Lessons ertussen viel. */
function byGroup(tabs) {
  return tabs
    .map((t, i) => [t, i])
    .sort((a, b) => (TABGROUPS.indexOf(tabGroup(a[0][0])) -
                     TABGROUPS.indexOf(tabGroup(b[0][0]))) || (a[1] - b[1]))
    .map(x => x[0]);
}

/* ===================================================================== V2 */
/* Stage E V2 naast V1. De koersen komen uit ledger.json, net als op elk ander
   tabblad, dus pre-lessons, post-lessons en V2 worden tegen dezelfde uitstap en
   onder dezelfde filters gerangschikt. Alleen de V2-score zelf komt uit v2.json. */
const V2RAW = document.getElementById('v2');
const V2 = (V2RAW && JSON.parse(V2RAW.textContent)) || {ledger:null, names:{}, runs:[]};
ALL.forEach(r => {
  const g = (V2.names || {})[r.run + '|' + r.ticker];
  r.v2 = g ? g.v2 : null;
  r.v2_vol_only = g ? g.vol_only : null;
  r.v2_status = g ? g.status : null;
});

function tabV2() {
  const L = V2.ledger;
  let html = `<p class="lead">Stage E V2 rekent de sommen van de hunters om via κ: hoe
    hard de koers bewoog op openbare 8-K's die een blinde scorer op dezelfde schaal
    scoorde, zonder marktbeta en per eenheid σ. <b>V1 blijft de sleutel die handelt.</b>
    Dit tabblad zet drie scores naast elkaar: vóór LESSONS.md, erna (V1) en V2, plus
    V1 × σ zonder κ. V2 voegt pas iets toe als het díe controle verslaat.</p>`;
  if (!L) {
    return html + `<div class="card warnbox"><h3>Geen V2-data</h3><p>De bouw vond geen
      <code>dashboard/data/v2.json</code>. Draai <code>dashboard/scripts/build_v2.py</code>.</p></div>`;
  }
  const bs = L.by_status || {};
  const prim = V2.primary_horizon;
  const pooledPrim = ((L.matrix || {})._pooled || {})[prim];
  const calibrated = pooledPrim && pooledPrim.n >= V2.min_n;
  html += tiles([
    {k:'8-K-filings in de ledger', v:L.items, s:`sinds ${esc(V2.min_event_date)}`},
    {k:'gescoord', v:(bs.scored||0)+(bs.measuring||0)+(bs.measured||0),
     s:`${bs.collected||0} wachten op de scorer`},
    {k:`waarnemingen bij ${esc(prim)}`, v:pooledPrim ? pooledPrim.n : 0,
     s:`min_n = ${V2.min_n}`},
    {k:'status', v: calibrated ? 'gekalibreerd' : 'nog niet',
     s: calibrated ? 'V2 krijgt getallen' : 'elke run leest uncalibrated'}]);

  const rows = rowsFor(r => r.impact_sum_pre_lessons !== null && r.impact_sum_pre_lessons !== undefined
                         || r.v2 !== null);
  const days = byDay(rows);
  const withV2 = rows.filter(r => r.v2 !== null && r.v2 !== undefined);
  const dV2 = byDay(withV2);
  html += `<div class="card"><h3>Drie scores tegen dezelfde beweging</h3>` + table([
    {h:'score', f:r=>r.label}, {h:'ρ binnen dagen', f:r=>`<span class="${sgn(r.rho)}">${n3(r.rho)}</span>`},
    {h:'namen', f:r=>r.n}, {h:'wat het is', f:r=>r.what}], [
    {label:'<b>pre-lessons</b>', rho:pooledRho(days, r=>r.impact_sum_pre_lessons, mvOf),
     n:rows.filter(r=>r.impact_sum_pre_lessons!==null && r.impact_sum_pre_lessons!==undefined).length,
     what:'de som vóór LESSONS.md, bevroren'},
    {label:'<b>post-lessons (V1)</b>', rho:pooledRho(days, r=>r.impact_sum, mvOf), n:rows.length,
     what:'<code>impact_sum</code>, de sleutel en het enige dat handelt'},
    {label:'<b>V2</b>', rho:pooledRho(dV2, r=>r.v2, mvOf), n:withV2.length,
     what:'<code>impact_sum_grounded</code>, alleen gekalibreerde runs'},
    {label:'controle: V1 × σ', rho:pooledRho(dV2, r=>r.v2_vol_only, mvOf), n:withV2.length,
     what:'zelfde namen als V2, geen κ'}]) +
    `<small>ρ is binnen dagen gepoold, op de gekozen uitstap en onder de filters bovenaan.
     V2 en de controle staan op dezelfde namen; vergelijk V2 met de controle, niet met V1.
     ${withV2.length ? '' : 'Nog geen gekalibreerde run, dus V2 en de controle zijn leeg.'}</small></div>`;

  const tf = L.timeframes || [];
  const pooled = (L.matrix || {})._pooled || {};
  html += `<div class="card"><h3>κ per horizon, gepoold</h3>` + table([
    {h:'horizon', f:r=> r.tf === prim ? `<b>${esc(r.tf)}</b>` : esc(r.tf)},
    {h:'κ', f:r=>r.k ? n3(r.k.kappa) : '–'},
    {h:'95%-interval', f:r=>r.k && r.k.ci95 ? `${n3(r.k.ci95[0])} … ${n3(r.k.ci95[1])}` : '–'},
    {h:'n', f:r=>r.k ? r.k.n : 0},
    {h:'pearson', f:r=>r.k ? n2(r.k.pearson) : '–'},
    {h:'bruikbaar', f:r=>r.k && r.k.n >= V2.min_n ? 'ja' : `<span class="meta">onder ${V2.min_n}</span>`}],
    tf.map(t => ({tf:t, k:pooled[t]}))) +
    `<small>κ is de beweging zonder beta, gedeeld door σ, per scorepunt. Een κ van 0,5 bij een
     σ van 2% betekent: een finding van +1 punt is +1% waard. Vetgedrukt is de horizon waarop
     V2 rangschikt.</small></div>`;

  const lines = Object.keys(L.matrix || {}).filter(k => k !== '_pooled');
  if (lines.length) {
    html += `<div class="card"><h3>κ per regel bij ${esc(prim)}</h3>` + table([
      {h:'regel', f:r=>esc(r.line)}, {h:'κ', f:r=>r.k ? n3(r.k.kappa) : '–'},
      {h:'n', f:r=>r.k ? r.k.n : 0},
      {h:'gebruikt', f:r=>r.k && r.k.n >= V2.min_n ? 'eigen κ' : 'gepoolde κ'}],
      lines.map(l => ({line:l, k:(L.matrix[l] || {})[prim]}))) + `</div>`;
  }

  const runs = V2.runs || [];
  if (runs.length) {
    html += `<div class="card"><h3>Runs met een V2-bestand</h3>` + table([
      {h:'run', f:r=>esc(r.run.split('/').slice(-2,-1)[0])},
      {h:'status', f:r=>esc(r.status)}, {h:'namen met V2', f:r=>r.n_grounded},
      {h:'κ zoals op', f:r=>`<span class="meta">${esc(r.matrix_as_of||'–')}</span>`},
      {h:'waarnemingen', f:r=>r.observations}], runs) +
      `<small>Elke run gebruikt κ zoals die stond toen zijn baselines verzegeld werden: een
       waarneming telt alleen als het eindpunt van haar horizon vóór die seal lag.</small></div>`;
  }
  const perName = rows.filter(r => r.v2_status);
  if (perName.length) {
    html += `<div class="card"><h3>Per naam</h3>` + table([
      {h:'run', f:r=>r.run_date}, {h:'ticker', f:r=>`<b>${esc(r.ticker)}</b>`},
      {h:'pre-lessons', f:r=>n2(r.impact_sum_pre_lessons)},
      {h:'post-lessons', f:r=>n2(r.impact_sum)},
      {h:'V2', f:r=> r.v2 === null || r.v2 === undefined ? `<span class="meta">${esc(r.v2_status)}</span>` : n2(r.v2)},
      {h:'beweging', f:r=>pc(mvOf(r))}], perName) + `</div>`;
  }
  return html;
}

/* ------------------------------------------------------- de index van de pagina
   Twintig tabbladen in één platte rij zijn geen index. Drie dingen maken er wel
   een van: elk tabblad hoort bij een groep, elk tabblad heeft één regel die zegt
   welke vraag het beantwoordt, en elk tabblad heeft een adres. Dat adres staat in
   de hash (`#eu/score`), dus een tabblad is te bookmarken, te delen en te herladen
   — en de Ververs-knop, die de pagina met een cache-buster herlaadt, brengt je
   terug waar je stond in plaats van op Overzicht. */
const TABGROUPS = ['Stand', 'Rangschikking', 'Klok', 'Doorsnedes', 'Register', 'Bronnen'];
const TABMETA = {
  /* Stand */
  'Overzicht':  {g:'Stand', q:'Wat staat er vandaag, op één scherm: dagen, namen, vondsten en of er al iets is opgelost.'},
  'Handel':     {g:'Stand', q:'Elke positie die de rekening echt heeft geopend en gesloten, met de spread en de uitstap die er werkelijk was.'},
  /* Rangschikking */
  'Score':      {g:'Rangschikking', q:'Rangschikt de jacht de dag beter dan de gratis controle, en wat levert het teken op?'},
  'Drempel':    {g:'Rangschikking', q:'Wat doet de conviction-floor als je hem verzet: rendement, raakpercentage, ρ en n bij elke snede.'},
  'Aanloop':    {g:'Rangschikking', q:'Zegt de koersbeweging vóór de print iets, en betaalt het als die het met de jacht eens is?'},
  /* Klok */
  'Timing':     {g:'Klok', q:'Waar hoort de uitstap te liggen: elke horizon van de nabeurs tot de slotkoers, per sessie.'},
  'Instap':     {g:'Klok', q:'Maakt het uur van instappen uit, met de uitstap vastgehouden?'},
  /* Doorsnedes */
  'Sector':     {g:'Doorsnedes', q:'Leeft de edge in één sector, en zit hij in de namen die particulieren verhandelen?'},
  'Zoekvolume': {g:'Doorsnedes', q:'Zegt de Google-aandacht rond de print iets over de uitkomst?'},
  'Capaciteit': {g:'Doorsnedes', q:'Hoeveel van het resultaat zit in namen die te dun zijn om in te handelen?'},
  'Kosten':     {g:'Doorsnedes', q:'Wat kost een run aan subagenten, en wat levert die run op?'},
  'Deelmarkt':  {g:'Doorsnedes', q:'Per beurs: namen, vondsten, ankerdekking, omzet en rangcorrelatie — en hoe scheef de trekking zat.'},
  'Ankerarm':   {g:'Doorsnedes', q:'Mét optie-anker tegen alleen het short-register, binnen één markt en één dag. De reden dat stage CA bestaat.'},
  'Soort':      {g:'Doorsnedes', q:'Winstcijfer tegen Appendix 4C/5B-kasstroomrapport: twee verschillende latten in één getal.'},
  'Taal':       {g:'Doorsnedes', q:'Leverde de aparte ronde in de eigen taal rangcorrelatie op? (controle gestopt 2026-09-22; alleen runs van vóór die datum)'},
  /* Register */
  'Lessons':    {g:'Register', q:'Kost of levert LESSONS.md: de bevroren draft tegen de uiteindelijke som.'},
  'V2':         {g:'Register', q:'Pre-lessons, post-lessons en V2 naast elkaar, en of κ iets toevoegt boven V1 × σ.'},
  'Hypotheses': {g:'Register', q:'Het hypotheseregister met één verdictregel, en wat er tot nu toe overeind blijft.'},
  'Weging':     {g:'Register', q:'De bevroren wegingen w1 en w2 naast de vlakke regel, per dag meegerekend.'},
  /* Bronnen */
  'Agenda':     {g:'Bronnen', q:'Wat er de komende week rapporteert, met beide poorten apart geteld. Geen voorspelling.'},
  'Namen':      {g:'Bronnen', q:'Elke gerangschikte naam met zijn sleutel, zijn baseline en zijn uitkomst.'},
  'Runs':       {g:'Bronnen', q:'Elke run op schijf: trekking, hunters, vondsten, wat er gedood is en het alarm van de resolver.'},
  'Data':       {g:'Bronnen', q:'Waar de cijfers vandaan komen en wat er bewust niet in zit.'},
  'Index':      {g:'Bronnen', q:'Elk tabblad van elke markt, met de vraag die het beantwoordt en of het al open staat.'},
};
const tabGroup = name => (TABMETA[name] || {}).g || 'Bronnen';
const tabQ = name => (TABMETA[name] || {}).q || '';

/* Het adres. Diakrieten eruit, want een hash met é of ë overleeft niet elke
   plek waar iemand hem plakt. */
const slug = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
                   .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/* ------------------------------------------------------------------ Index */
function tabIndex() {
  let html = `<p class="lead">Elk tabblad van elke markt, met de vraag die het beantwoordt.
    Een tabblad van een markt zonder broker bestaat niet en een analysetabblad verschijnt
    pas als zijn data het draagt; hieronder staat allebei, met de voorwaarde erbij.</p>`;
  for (const [code, label] of MARKETS) {
    const open = code === 'US' ? US_TABS.map(t => t[0]) : marketTabs(code).map(t => t[0]);
    const shut = code === 'US' ? [] : MTABDEFS
      .filter(t => (!t.only || t.only === code) && !open.includes(t.name))
      .map(t => ({name: t.name, needs: t.needs}));
    const rows = [...open.map(n => ({name:n, open:true})),
                  ...shut.map(t => ({name:t.name, open:false, needs:t.needs}))]
      .sort((a, b) => TABGROUPS.indexOf(tabGroup(a.name)) - TABGROUPS.indexOf(tabGroup(b.name)));
    html += `<div class="card"><h3>${esc(label)}</h3>` + table([
      {h:'groep', f:r=>`<span class="meta">${esc(tabGroup(r.name))}</span>`},
      {h:'tabblad', f:r=> r.open
          ? `<a href="#${slug(code)}/${slug(r.name)}"><b>${esc(r.name)}</b></a>`
          : `<span class="meta">${esc(r.name)}</span>`},
      {h:'de vraag', f:r=>esc(tabQ(r.name))},
      {h:'staat', f:r=> r.open ? 'open'
          : `<span class="meta">dicht · ${esc(r.needs || '')}</span>`},
    ], rows) + `</div>`;
  }
  html += `<div class="card"><h3>Adressen</h3>
    <p>Elk tabblad heeft er een: <code>#markt/tabblad</code>, bijvoorbeeld
    <a href="#eu/deelmarkt"><code>#eu/deelmarkt</code></a> of
    <a href="#us/drempel"><code>#us/drempel</code></a>. Zo'n adres is te bookmarken en te
    delen, en het overleeft de Ververs-knop, die de pagina met een cache-buster herlaadt.
    Wijst een adres naar een tabblad dat bij die markt niet bestaat of nog dicht is, dan
    opent Overzicht van die markt.</p></div>`;
  return html;
}

/* ------------------------------------------------------------------- boot */
/* De markt is de bovenste as van deze pagina, en de tabbladenrij hangt eronder.
   De VS heeft een broker, dus die houdt zijn handels-, capaciteits-, kosten- en
   wegingstabbladen. De andere vier plaatsen geen orders, dus die tabbladen
   bestaan daar niet: een rij die per markt verschilt, vertelt precies dat. */
/* Op groepsvolgorde, want de rij zelf is de index. Stand · Rangschikking ·
   Klok · Doorsnedes · Register · Bronnen; zie TABMETA voor wat elk tabblad
   beantwoordt. */
const US_TABS = [['Overzicht',tabOverzicht], ['Handel',tabHandel],
              ['Score',tabScore], ['Drempel',tabDrempel], ['Aanloop',tabAanloop],
              ['Timing',tabTiming], ['Instap',tabInstap],
              ['Sector',tabSector], ['Zoekvolume',tabZoek],
              ['Capaciteit',tabCapaciteit], ['Kosten',tabKosten],
              ['Lessons',tabLessons], ['V2',tabV2], ['Hypotheses',tabHypotheses], ['Weging',tabWeging],
              ['Agenda',tabAgenda], ['Data',tabData], ['Index',tabIndex]];
US_TABS.splice(0, US_TABS.length, ...byGroup(US_TABS));
const MARKETS = [['US','Verenigde Staten'], ['EU','Europa'], ['JP','Japan'],
                 ['AU','Australië'], ['CA','Canada']];
let MKT = 'US';
let TABS = US_TABS;
let active = 0;
const bar = document.getElementById('marketbar');
const nav = document.getElementById('tabs'), panels = document.getElementById('panels');

/* Eén regel per markt met wat erachter zit, zodat de keuze niet blind is. */
const mCount = code => {
  if (code === 'US') return `${D.runs.length} runs · ${ALL.length} namen · handel`;
  const d = (M.markets || {})[code];
  if (!d) return 'geen data';
  return d.n_runs ? `${d.n_runs} runs · ${d.n_names} namen · ${d.n_resolved} opgelost`
                  : 'nog geen run';
};
MARKETS.forEach(([code, label]) => {
  const b = document.createElement('button');
  b.innerHTML = `<span class="mk">${esc(label)}</span>` +
                `<span class="mc">${esc(mCount(code))}</span>`;
  b.setAttribute('aria-pressed', code === MKT ? 'true' : 'false');
  b.onclick = () => setMarket(code);
  bar.appendChild(b);
});

/* De knoppen in leesvolgorde, los van de groepsblokken waarin ze staan. Alles
   wat met een index werkt (toetsenbord, aria-selected, de hash) telt op deze
   lijst en niet op nav.children, want dat zijn de groepen. */
let navBtns = [];

function buildTabs(keepName) {
  nav.innerHTML = ''; panels.innerHTML = ''; navBtns = [];
  let group = null, box = null;
  TABS.forEach(([name], i) => {
    const g = tabGroup(name);
    if (g !== group) {
      group = g;
      box = document.createElement('span');
      box.className = 'tabgroup';
      box.innerHTML = `<span class="gl">${esc(g)}</span>`;
      nav.appendChild(box);
    }
    const b = document.createElement('button');
    b.textContent = name; b.setAttribute('role','tab');
    b.id = 'tab-' + i;
    b.title = tabQ(name);
    b.setAttribute('aria-controls', 'panel-' + i);
    b.onclick = () => { active = i; refresh(); };
    box.appendChild(b);
    navBtns.push(b);
    const s = document.createElement('section');
    s.id = 'panel-' + i; s.setAttribute('role','tabpanel');
    s.setAttribute('aria-labelledby', 'tab-' + i);
    s.tabIndex = 0;                    /* the panel scrolls, so it must focus */
    panels.appendChild(s);
  });
  /* Een filter mag een getal versmallen, nooit het tabblad onder je wegtrekken.
     Verandert de rij toch (de validatieknop kan een analysetabblad openen), dan
     wordt hetzelfde tabblad bij naam teruggezocht en anders Overzicht. */
  const i = keepName ? TABS.findIndex(t => t[0] === keepName) : -1;
  active = i >= 0 ? i : 0;
}

function setMarket(code) {
  MKT = code;
  TABS = code === 'US' ? US_TABS : marketTabs(code);
  [...bar.children].forEach((b, i) =>
    b.setAttribute('aria-pressed', MARKETS[i][0] === code ? 'true' : 'false'));
  buildTabs();
  refresh();
}

/* Roving tabindex: een tablist is ÉÉN tabstop en de pijlen bewegen erbinnen.
   Met twintig tabbladen is het alternatief twintig toetsaanslagen voor de
   pagina zelf. */
nav.addEventListener('keydown', e => {
  const step = {ArrowRight:1, ArrowLeft:-1, Home:-Infinity, End:Infinity}[e.key];
  if (step === undefined) return;
  e.preventDefault();
  active = !isFinite(step) ? (step < 0 ? 0 : TABS.length - 1)
                           : (active + step + TABS.length) % TABS.length;
  refresh();
  navBtns[active].focus();
});

/* ---- het adres van een tabblad ------------------------------------------
   `#markt/tabblad`. replaceState en niet pushState: met twintig tabbladen maal
   vijf markten zou de Terug-knop anders door de klikgeschiedenis lopen in plaats
   van de pagina te verlaten. Wijst een adres nergens heen, dan opent Overzicht
   van die markt in plaats van een foutmelding. */
let hashLock = false;
function writeHash() {
  if (hashLock) return;
  const h = '#' + slug(MKT) + '/' + slug((TABS[active] || [''])[0]);
  if (location.hash !== h) history.replaceState(null, '', location.pathname + location.search + h);
}
function readHash() {
  const m = /^#([a-z]{2})\/(.+)$/.exec(location.hash.toLowerCase());
  if (!m) return false;
  const code = MARKETS.find(([c]) => slug(c) === m[1]);
  if (!code) return false;
  hashLock = true;
  setMarket(code[0]);
  hashLock = false;
  const i = TABS.findIndex(t => slug(t[0]) === m[2]);
  if (i >= 0) { active = i; }
  refresh();
  return true;
}
/* Een adres dat nergens heen wijst, wordt rechtgezet in plaats van te blijven
   staan: refresh schrijft de hash terug naar waar de pagina werkelijk staat. */
addEventListener('hashchange', () => { if (!readHash()) refresh(); });
buildTabs();
function refresh() {
  navBtns.forEach((b,j) => {
    b.setAttribute('aria-selected', j===active ? 'true':'false');
    b.tabIndex = j === active ? 0 : -1;
  });
  writeHash();
  [...panels.children].forEach((s,j) => s.hidden = j !== active);
  /* De filterbalk hoort bij de ledger van stage E: lens, cap, sector en uitstap-
     horizon bestaan alleen daar. Op een markttabblad zou hij filters tonen die
     niets onder zich hebben, dus daar verdwijnt hij en zet het tabblad zijn eigen
     twee knoppen neer. */
  const isMarket = !!TABS[active][2];
  document.getElementById('controls').hidden = isMarket;
  document.getElementById('filterline').hidden = isMarket;
  if (!isMarket) filterLine();
  draw.length = 0;
  panels.children[active].innerHTML = TABS[active][1]();
  draw.forEach(fn => fn());
}
document.getElementById('stamp').textContent =
  `gebouwd ${D.generated_utc}` +
  ((D.build || {}).where === 'github-actions'
     ? ` door GitHub Actions (${(D.build.sha || '?')})` : '') +
  ` · ${D.runs.length} runs · ${D.names.length} namen` +
  (ALL.length !== D.names.length ? ` (${ALL.length} na aftrek dubbele events)` : '') + ` · ` +
  `${D.trades.filter(t=>t.closed).length} afgeronde posities · ` +
  `conviction-floor uit de config ${D.conviction_floor}`;
document.getElementById('theme').onclick = () => {
  const now = document.documentElement.getAttribute('data-theme');
  const dark = now ? now === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
  refresh();
};
/* The refresh button, three ways, and it says which one it is in.

   lokaal  a rebuilder answers on 127.0.0.1:8765 (`./dashboard/update.sh --serve-bg`).
           A click rebuilds the ledger and rewrites this very file on disk. A file://
           page may not run a script -- a browser rule, not a setting -- but it may
           talk to a server that is already running, and serve.py answers one on
           purpose.
   ci      no local rebuilder, but the repository is known: a click asks GitHub
           Actions to run the `dashboard` workflow, which rebuilds the ledger,
           commits it and republishes this page. That is the mode a hosted copy is
           in, because a page on the web cannot reach your laptop and must not
           pretend it can.
   uit     neither is reachable, so the button hands over the command.

   An https page cannot probe http://127.0.0.1 -- mixed content -- so the local probe
   only runs where it can succeed: a file, or a page served from localhost. The
   dispatch needs a token GitHub will accept; without one the button opens the
   workflow's own page, where the same run is one click away. The token is kept in
   this browser's localStorage and goes nowhere but api.github.com. */
const PORT = 8765;
const ONFILE = location.protocol === 'file:';
const LOCALHOST = /^(127\.0\.0\.1|localhost|\[::1\])$/.test(location.hostname);
const LOCAL = ONFILE ? `http://127.0.0.1:${PORT}` : (LOCALHOST ? location.origin : null);
const CMD = './dashboard/update.sh';
const BUILD = D.build || {};
const REPO = BUILD.repo || '';
const WF = 'dashboard.yml';
const API = REPO ? `https://api.github.com/repos/${REPO}` : '';
const WFURL = REPO ? `https://github.com/${REPO}/actions/workflows/${WF}` : '';
const TOKKEY = 'edge-dashboard-gh-token';
const btn = document.getElementById('refresh');
const log = document.getElementById('refreshlog');
const badge = document.getElementById('served');
let mode = 'uit';

const tok = () => { try { return localStorage.getItem(TOKKEY) || ''; } catch (_) { return ''; } };
function setTok(v) {
  try { v ? localStorage.setItem(TOKKEY, v) : localStorage.removeItem(TOKKEY); } catch (_) {}
}
function gh(extra) {
  const h = Object.assign({'Accept':'application/vnd.github+json',
                           'X-GitHub-Api-Version':'2022-11-28'}, extra || {});
  if (tok()) h['Authorization'] = `Bearer ${tok()}`;
  return h;
}
function show(text) { log.hidden = false; log.textContent = text; }
function showHTML(html) { log.hidden = false; log.innerHTML = html; }
function setBadge(text, title, cls) {
  badge.hidden = false; badge.textContent = text; badge.title = title || '';
  badge.className = 'badge' + (cls ? ' ' + cls : '');
}
function stamp(d) {
  try { return new Date(d).toLocaleString('nl-NL', {dateStyle:'short', timeStyle:'short'}); }
  catch (_) { return d; }
}

async function lastRun() {
  if (!API) return null;
  try {
    const r = await fetch(`${API}/actions/workflows/${WF}/runs?per_page=1`,
                          {headers: gh(), cache:'no-store'});
    if (!r.ok) return null;
    return ((await r.json()).workflow_runs || [])[0] || null;
  } catch (_) { return null; }
}

/* Is there a finished build newer than the data on this page? On a hosted copy
   that means a reload is all it takes; in a file it means `git pull`. */
function newerThanThisPage(run) {
  if (!run || run.status !== 'completed' || run.conclusion !== 'success') return false;
  if (!D.generated_utc) return false;
  return new Date(run.updated_at) > new Date(D.generated_utc);
}

async function probe() {
  if (LOCAL) {
    try {
      const j = await (await fetch(`${LOCAL}/ping`, {cache:'no-store'})).json();
      if (j && j.ok) {
        mode = 'lokaal';
        setBadge('live', `Rebuilder op poort ${PORT}: een klik herbouwt dit bestand.`);
        btn.title = 'Herbouwt de ledger en dit dashboard, hier op deze machine.';
        return;
      }
    } catch (_) {}
  }
  if (!API) {
    btn.title = `Geen rebuilder op poort ${PORT} en geen repo bekend. Klik voor het commando.`;
    return;
  }
  mode = 'ci';
  btn.title = 'Laat GitHub Actions de ledger en deze pagina opnieuw bouwen.';
  const run = await lastRun();
  if (!run) {
    setBadge('CI', 'Workflow-status niet op te halen (limiet of geen netwerk).', 'ci');
    return;
  }
  const busy = run.status !== 'completed';
  setBadge(busy ? 'CI bezig' : 'CI',
           `Laatste run: ${run.status}${run.conclusion ? ' / ' + run.conclusion : ''} ` +
           `om ${stamp(run.updated_at)}`, 'ci');
  if (newerThanThisPage(run)) {
    showHTML(`Er is een nieuwere build klaar (${stamp(run.updated_at)}) dan de data op ` +
             `deze pagina (${stamp(D.generated_utc)}).\n` +
             (ONFILE ? `Dit is een bestand op schijf: haal hem op met <code>git pull</code>.`
                     : `<a href="#" id="hardreload">Herlaad deze pagina</a> om hem te zien.`));
    const a = document.getElementById('hardreload');
    if (a) a.onclick = (e) => { e.preventDefault(); bust(); };
  }
}

/* The published copy comes off a CDN, so a plain reload can hand back the old
   file. A changing query string cannot. */
function bust() {
  location.replace(location.pathname + '?b=' + Date.now() + location.hash);
}

function explainLocal() {
  show(`Deze pagina kan zelf geen script draaien.\n\n` +
       `Eén keer dit draaien in de repo-root, dan werkt deze knop — ook in dit bestand:\n` +
       `    ${CMD} --serve-bg\n\n` +
       `Die start een servertje op 127.0.0.1:${PORT} en geeft je je shell terug. Ververs\n` +
       `daarna deze pagina; de knop vindt de server vanzelf.\n\n` +
       `Liever eenmalig en zonder server:\n    ${CMD}`);
  navigator.clipboard?.writeText(`${CMD} --serve-bg`).catch(() => {});
}

function explainCI() {
  showHTML(
    (ONFILE
      ? `Dit bestand staat op schijf en er draait geen rebuilder. Wil je HIER bouwen, dan\n` +
        `is het <code>${CMD} --serve-bg</code> in de repo-root, en daarna deze pagina\n` +
        `verversen.\n\n`
      : `Deze pagina draait niet op jouw machine, dus de knop kan hier niets bouwen.\n`) +
    `Wat hij wél kan: de workflow <code>${WF}</code> starten in ${REPO}. Die herbouwt de\n` +
    `ledger, commit hem en publiceert de gepubliceerde pagina opnieuw` +
    (ONFILE ? ` — niet dit bestand, dat haal je daarna op met <code>git pull</code>` : ``) +
    `.\n\n` +
    `Eén klik hier: <a href="${WFURL}" target="_blank" rel="noopener">open de workflow</a> ` +
    `en kies “Run workflow”.\n\n` +
    `Of laat deze knop het doen. Daarvoor is een GitHub-token nodig met alleen\n` +
    `<b>Actions: read and write</b> op deze repo (fine-grained, of een classic met <code>repo</code>).\n` +
    `Hij wordt alleen in deze browser bewaard en gaat alleen naar api.github.com.\n` +
    `<div class="row"><input type="password" id="ghtok" placeholder="github_pat_…" ` +
    `autocomplete="off" spellcheck="false">` +
    `<button class="btn small" id="ghtoksave">bewaren</button>` +
    `<button class="btn small" id="ghtokclear">vergeten</button></div>`);
  const inp = document.getElementById('ghtok');
  document.getElementById('ghtoksave').onclick = () => {
    const v = (inp.value || '').trim();
    if (!v) return;
    setTok(v); inp.value = '';
    show('token bewaard — klik nu op Ververs.');
  };
  document.getElementById('ghtokclear').onclick = () => {
    setTok(''); show('token gewist uit deze browser.');
  };
}

async function rebuildLocal() {
  btn.disabled = true; btn.textContent = 'bezig…';
  show('ledger en dashboard opnieuw bouwen…');
  try {
    const j = await (await fetch(`${LOCAL}/rebuild`, {method:'POST'})).json();
    show(j.log || '(geen uitvoer)');
    if (j.ok) {
      log.textContent += '\nklaar — pagina wordt herladen';
      setTimeout(() => location.reload(), 900);
      return;
    }
  } catch (_) {
    mode = 'uit';
    explainLocal();
  }
  btn.disabled = false; btn.textContent = 'Ververs';
}

/* Fire the workflow and then watch it. The run is only reported complete once the
   build AND the publish step are done, so when this says klaar the page behind the
   URL really has changed. */
async function rebuildCI() {
  if (!tok()) { explainCI(); return; }
  btn.disabled = true; btn.textContent = 'bezig…';
  show('GitHub Actions starten…');
  const t0 = Date.now() - 120000;
  let r;
  try {
    r = await fetch(`${API}/actions/workflows/${WF}/dispatches`, {
      method: 'POST',
      headers: gh({'Content-Type': 'application/json'}),
      body: JSON.stringify({ref: 'main', inputs: {}})});
  } catch (err) {
    show(`starten mislukt: ${err}\nProbeer de workflow zelf: ${WFURL}`);
    btn.disabled = false; btn.textContent = 'Ververs'; return;
  }
  if (!r.ok) {
    const why = r.status === 401 || r.status === 403
      ? 'het token wordt niet geaccepteerd (verlopen, of zonder Actions-schrijfrecht)'
      : r.status === 404
        ? `workflow ${WF} niet gevonden op de hoofdbranch van ${REPO}`
        : `HTTP ${r.status}`;
    showHTML(`Starten mislukt: ${why}.\n` +
             `<a href="${WFURL}" target="_blank" rel="noopener">Open de workflow</a> en ` +
             `draai hem daar, of zet een ander token.`);
    btn.disabled = false; btn.textContent = 'Ververs'; return;
  }
  show('gestart — wachten tot de build klaar is (meestal twee tot vier minuten)…');
  for (let i = 0; i < 150; i++) {
    await new Promise(res => setTimeout(res, 6000));
    const run = await lastRun();
    if (!run || new Date(run.created_at).getTime() < t0) {
      show('gestart — de run staat nog in de wachtrij…');
      continue;
    }
    if (run.status !== 'completed') {
      show(`bezig: ${run.status}${run.conclusion ? ' / ' + run.conclusion : ''} — ` +
           `${run.html_url}`);
      continue;
    }
    if (run.conclusion === 'success') {
      if (ONFILE) {
        showHTML(`Klaar. Dit is een bestand op schijf, dus het verandert er niet van: ` +
                 `<code>git pull</code> haalt de nieuwe versie op. ` +
                 `<a href="${run.html_url}" target="_blank" rel="noopener">De run</a>.`);
        btn.disabled = false; btn.textContent = 'Ververs';
        return;
      }
      show('klaar — pagina wordt opnieuw opgehaald');
      setTimeout(bust, 1200);
      return;
    }
    showHTML(`De run eindigde als <b>${run.conclusion}</b>. ` +
             `<a href="${run.html_url}" target="_blank" rel="noopener">Bekijk het logboek</a>.`);
    break;
  }
  btn.disabled = false; btn.textContent = 'Ververs';
}

btn.onclick = () => {
  if (mode === 'lokaal') return rebuildLocal();
  if (mode === 'ci') return rebuildCI();
  return explainLocal();
};
probe();
probe();
let rt;
addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(refresh, 150); });
renderControls();
/* Pas hier, want readHash kan een markt en een tabblad zetten en die render moet
   de filterbalk al kennen. Geen adres in de URL: gewoon de VS op Overzicht. */
if (!readHash()) refresh();
</script>
</body>
</html>
"""



def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=str(DATA / "ledger.json"))
    ap.add_argument("--markets", default=str(DATA / "markets.json"))
    ap.add_argument("--v2", default=str(DATA / "v2.json"))
    ap.add_argument("--out", default=str(ROOT / "dashboard" / "dashboard.html"))
    a = ap.parse_args()

    led = json.loads(Path(a.ledger).read_text(encoding="utf-8"))
    # `</script>` inside the payload would close the tag it is embedded in.
    blob = json.dumps(led, separators=(",", ":")).replace("</", "<\\/")
    html = HTML.replace("__LEDGER__", blob)

    # The other three researchers. A missing file is not an error: stage EU, J and
    # AU place no orders and their tabs say so themselves, and a rebuild must not
    # fail because a feeder that only feeds three tabs did not run.
    mk = Path(a.markets)
    mblob = (mk.read_text(encoding="utf-8").strip() if mk.exists()
             else json.dumps({"markets": {}, "problems":
                              [f"{mk} does not exist: run "
                               "dashboard/scripts/build_markets.py"]}))
    html = html.replace("__MARKETS__", mblob.replace("</", "<\\/"))
    # Stage E V2. Missing is not an error either: the tab says so itself.
    v2 = Path(a.v2)
    vblob = v2.read_text(encoding="utf-8").strip() if v2.exists() else "null"
    html = html.replace("__V2__", vblob.replace("</", "<\\/"))
    Path(a.out).write_text(html, encoding="utf-8")
    print(f"wrote {a.out}  ({len(html.encode())/1024:.0f} kB, {len(led['names'])} names, "
          f"{len(led['trades'])} positions)")


if __name__ == "__main__":
    main()
