#!/usr/bin/env python3
"""Render edge/performance/dashboard.html from data/ledger.json.

One self-contained file: no CDN, no build step, no network. Open it from disk.
Everything it shows comes out of the ledger, so this script computes nothing --
if a number looks wrong, it is wrong in build_ledger.py.

    python3 edge/performance/scripts/build_dashboard.py
"""
import argparse
import json
from datetime import datetime, timezone
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
.wrap { max-width:1180px; margin:0 auto; padding:24px 16px 72px; }
header { display:flex; flex-wrap:wrap; gap:12px; align-items:baseline; justify-content:space-between; }
h1 { font-size:22px; margin:0; letter-spacing:-0.01em; }
h2 { font-size:17px; margin:28px 0 6px; }
h3 { font-size:14px; margin:0 0 10px; color:var(--ink2); font-weight:600; }
p  { margin:8px 0; color:var(--ink2); max-width:78ch; }
p.lead { color:var(--ink); }
small, .meta { color:var(--muted); font-size:12.5px; }
a { color:var(--s1); }
button { font:inherit; }
.toggle {
  background:var(--surface); color:var(--ink2); border:1px solid var(--ring);
  border-radius:8px; padding:5px 11px; cursor:pointer;
}
nav { display:flex; flex-wrap:wrap; gap:4px; margin:20px 0 4px; border-bottom:1px solid var(--grid); }
nav button {
  background:none; border:none; border-bottom:2px solid transparent; color:var(--ink2);
  padding:9px 13px; cursor:pointer; border-radius:6px 6px 0 0;
}
nav button:hover { background:var(--surface); }
nav button[aria-selected="true"] { color:var(--ink); border-bottom-color:var(--s1); font-weight:600; }
section[hidden] { display:none; }
.card {
  background:var(--surface); border:1px solid var(--ring); border-radius:12px;
  padding:16px 18px; margin:14px 0;
}
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(168px,1fr)); gap:10px; margin:14px 0; }
.tile { background:var(--surface); border:1px solid var(--ring); border-radius:12px; padding:13px 15px; }
.tile .k { font-size:12px; color:var(--muted); text-transform:none; }
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
.chart { position:relative; width:100%; }
.chart svg { display:block; width:100%; height:auto; overflow:visible; }
.tip {
  position:fixed; pointer-events:none; opacity:0; transition:opacity .08s;
  background:var(--surface); border:1px solid var(--ring); border-radius:8px;
  padding:7px 10px; font-size:12.5px; color:var(--ink); box-shadow:0 4px 16px rgba(0,0,0,.14);
  z-index:9; max-width:280px;
}
.note { border-left:3px solid var(--s2); padding-left:12px; margin:14px 0; }
.warnbox { border-left:3px solid var(--warn); padding-left:12px; margin:14px 0; }
.empty { color:var(--muted); font-style:normal; padding:22px 0; text-align:center; }
code { font-family:var(--mono); font-size:12.5px; background:var(--plane); padding:1px 5px; border-radius:5px; }
ul { color:var(--ink2); max-width:78ch; }
li { margin:4px 0; }
@media (max-width:640px){ .wrap{padding:16px 16px 60px;} h1{font-size:19px;} }
</style>
</head>
<body>
<div class="wrap">
<header>
  <div>
    <h1>Edge hunt — performance</h1>
    <div class="meta" id="stamp"></div>
  </div>
  <button class="toggle" id="theme">donker / licht</button>
</header>

<nav id="tabs" role="tablist"></nav>
<div id="panels"></div>
<div class="tip" id="tip"></div>
</div>

<script id="ledger" type="application/json">__LEDGER__</script>
<script>
const D = JSON.parse(document.getElementById('ledger').textContent);
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const n1 = x => x === null || x === undefined ? '–' : (+x).toFixed(1);
const n2 = x => x === null || x === undefined ? '–' : (+x).toFixed(2);
const n3 = x => x === null || x === undefined ? '–' : (+x).toFixed(3);
const pc = x => x === null || x === undefined ? '–' : (x > 0 ? '+' : '') + (+x).toFixed(2) + '%';
const usd = x => x === null || x === undefined ? '–' :
  (x < 0 ? '−$' : '$') + Math.abs(+x).toLocaleString('en-US', {maximumFractionDigits:0});
const sgn = x => x === null || x === undefined ? '' : (x > 0 ? 'pos' : x < 0 ? 'neg' : '');
const esc = s => String(s ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const tip = document.getElementById('tip');
function showTip(e, html) {
  tip.innerHTML = html; tip.style.opacity = 1;
  const r = tip.getBoundingClientRect();
  let x = e.clientX + 14, y = e.clientY - 10;
  if (x + r.width > innerWidth - 8) x = e.clientX - r.width - 14;
  if (y + r.height > innerHeight - 8) y = innerHeight - r.height - 8;
  tip.style.left = x + 'px'; tip.style.top = Math.max(8, y) + 'px';
}
const hideTip = () => tip.style.opacity = 0;

/* ---------------------------------------------------------------- charts */
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
  const svg = el('svg', {viewBox: `0 0 ${w} ${h}`, width: w, height: h}, host);
  return {svg, w, h};
}
function axes(svg, x0, x1, y0, y1, ticks, fmt, label) {
  const g = css('--grid'), m = css('--muted');
  ticks.forEach(t => {
    el('line', {x1:x0, x2:x1, y1:t.y, y2:t.y, stroke:g, 'stroke-width':1}, svg);
    const tx = el('text', {x:x0-8, y:t.y+4, fill:m, 'font-size':11, 'text-anchor':'end'}, svg);
    tx.textContent = fmt ? fmt(t.v) : t.v;
  });
  el('line', {x1:x0, x2:x1, y1:y1, y2:y1, stroke:css('--axis'), 'stroke-width':1}, svg);
  if (label) {
    const t = el('text', {x:x0, y:12, fill:m, 'font-size':11}, svg);
    t.textContent = label;
  }
}
function scaleTicks(min, max, n) {
  if (min === max) { min -= 1; max += 1; }
  const span = max - min, raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1,2,2.5,5,10].map(m => m*mag).find(s => s >= raw) || mag*10;
  const lo = Math.floor(min/step)*step, hi = Math.ceil(max/step)*step, out = [];
  for (let v = lo; v <= hi + 1e-9; v += step) out.push(+v.toFixed(10));
  return out;
}

function lineChart(host, spec) {
  const {svg, w, h} = frame(host, spec.height || 240);
  const pad = {l:52, r:16, t:18, b:26};
  const rows = spec.series;
  const xs = spec.x, x0 = pad.l, x1 = w - pad.r, y0 = pad.t, y1 = h - pad.b;
  const vals = rows.flatMap(s => s.values.filter(v => v !== null));
  if (!vals.length) { host.innerHTML = '<div class="empty">geen data</div>'; return; }
  let mn = Math.min(...vals, spec.zero ? 0 : Infinity), mx = Math.max(...vals);
  const tv = scaleTicks(mn, mx, 4); mn = tv[0]; mx = tv[tv.length-1];
  const X = i => x0 + (xs.length < 2 ? (x1-x0)/2 : i*(x1-x0)/(xs.length-1));
  const Y = v => y1 - (v-mn)/(mx-mn)*(y1-y0);
  axes(svg, x0, x1, y0, y1, tv.map(v => ({v, y:Y(v)})), spec.fmtY, spec.labelY);
  if (mn < 0 && mx > 0) el('line', {x1:x0, x2:x1, y1:Y(0), y2:Y(0),
      stroke:css('--axis'), 'stroke-width':1}, svg);
  xs.forEach((lab, i) => {
    if (xs.length > 10 && i % Math.ceil(xs.length/8)) return;
    const t = el('text', {x:X(i), y:h-8, fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = lab;
  });
  rows.forEach(s => {
    const pts = s.values.map((v,i) => v === null ? null : [X(i), Y(v)]).filter(Boolean);
    if (pts.length > 1)
      el('path', {d:'M' + pts.map(p => p.join(' ')).join(' L'), fill:'none',
                  stroke:s.color, 'stroke-width':2, 'stroke-linejoin':'round',
                  'stroke-dasharray': s.dash || ''}, svg);
    pts.forEach(p => el('circle', {cx:p[0], cy:p[1], r:3.5, fill:s.color,
                                   stroke:css('--surface'), 'stroke-width':2}, svg));
    if (pts.length) {
      const last = pts[pts.length-1];
      const t = el('text', {x:Math.min(last[0]+8, x1), y:last[1]-9, fill:s.color,
                            'font-size':11.5, 'text-anchor':'end'}, svg);
      t.setAttribute('x', last[0]); t.setAttribute('text-anchor', 'middle');
      t.textContent = s.label;
    }
  });
  xs.forEach((lab, i) => {
    const hit = el('rect', {x:X(i)-(x1-x0)/(2*Math.max(1,xs.length-1)), y:y0,
                            width:(x1-x0)/Math.max(1,xs.length-1), height:y1-y0,
                            fill:'transparent'}, svg);
    hit.addEventListener('mousemove', e => showTip(e,
      `<b>${esc(lab)}</b><br>` + rows.map(s =>
        `<span style="color:${s.color}">■</span> ${esc(s.label)}: ` +
        (s.values[i] === null ? '–' : (spec.fmtT ? spec.fmtT(s.values[i]) : n2(s.values[i])))
      ).join('<br>')));
    hit.addEventListener('mouseleave', hideTip);
  });
}

function barChart(host, spec) {
  const items = spec.items;
  const {svg, w, h} = frame(host, spec.height || 240);
  const pad = {l:52, r:16, t:18, b:34};
  const x0 = pad.l, x1 = w - pad.r, y0 = pad.t, y1 = h - pad.b;
  if (!items.length) { host.innerHTML = '<div class="empty">geen data</div>'; return; }
  const vals = items.map(i => i.v);
  const tv = scaleTicks(Math.min(0, ...vals), Math.max(0, ...vals), 4);
  const mn = tv[0], mx = tv[tv.length-1];
  const Y = v => y1 - (v-mn)/(mx-mn)*(y1-y0);
  axes(svg, x0, x1, y0, y1, tv.map(v => ({v, y:Y(v)})), spec.fmtY, spec.labelY);
  const step = (x1-x0)/items.length, bw = Math.max(6, Math.min(52, step-8));
  items.forEach((it, i) => {
    const cx = x0 + step*i + step/2, base = Y(0), top = Y(it.v);
    const col = it.color || (it.v >= 0 ? css('--good') : css('--bad'));
    const y = Math.min(base, top), hh = Math.max(2, Math.abs(base-top));
    el('rect', {x:cx-bw/2, y, width:bw, height:hh, rx:4, fill:col}, svg);
    const t = el('text', {x:cx, y:h-18, fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = it.label;
    if (it.sub) {
      const s = el('text', {x:cx, y:h-5, fill:css('--muted'), 'font-size':10,
                            'text-anchor':'middle'}, svg);
      s.textContent = it.sub;
    }
    const hit = el('rect', {x:cx-step/2, y:y0, width:step, height:y1-y0, fill:'transparent'}, svg);
    hit.addEventListener('mousemove', e => showTip(e, it.tip ||
      `<b>${esc(it.label)}</b><br>${spec.fmtT ? spec.fmtT(it.v) : n2(it.v)}`));
    hit.addEventListener('mouseleave', hideTip);
  });
  el('line', {x1:x0, x2:x1, y1:Y(0), y2:Y(0), stroke:css('--axis'), 'stroke-width':1}, svg);
}

function scatterChart(host, spec) {
  const {svg, w, h} = frame(host, spec.height || 320);
  const pad = {l:52, r:18, t:18, b:38};
  const x0 = pad.l, x1 = w - pad.r, y0 = pad.t, y1 = h - pad.b;
  const pts = spec.points.filter(p => p.x !== null && p.y !== null);
  if (!pts.length) { host.innerHTML = '<div class="empty">geen data</div>'; return; }
  const xt = scaleTicks(Math.min(...pts.map(p=>p.x)), Math.max(...pts.map(p=>p.x)), 5);
  const yt = scaleTicks(Math.min(...pts.map(p=>p.y)), Math.max(...pts.map(p=>p.y)), 4);
  const X = v => x0 + (v-xt[0])/(xt[xt.length-1]-xt[0])*(x1-x0);
  const Y = v => y1 - (v-yt[0])/(yt[yt.length-1]-yt[0])*(y1-y0);
  axes(svg, x0, x1, y0, y1, yt.map(v => ({v, y:Y(v)})), spec.fmtY, spec.labelY);
  xt.forEach(v => {
    el('line', {x1:X(v), x2:X(v), y1:y0, y2:y1, stroke:css('--grid'), 'stroke-width':1}, svg);
    const t = el('text', {x:X(v), y:h-20, fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = spec.fmtX ? spec.fmtX(v) : v;
  });
  if (xt[0] < 0 && xt[xt.length-1] > 0)
    el('line', {x1:X(0), x2:X(0), y1:y0, y2:y1, stroke:css('--axis'), 'stroke-width':1}, svg);
  if (yt[0] < 0 && yt[yt.length-1] > 0)
    el('line', {x1:x0, x2:x1, y1:Y(0), y2:Y(0), stroke:css('--axis'), 'stroke-width':1}, svg);
  if (spec.labelX) {
    const t = el('text', {x:(x0+x1)/2, y:h-4, fill:css('--muted'), 'font-size':11,
                          'text-anchor':'middle'}, svg);
    t.textContent = spec.labelX;
  }
  pts.forEach(p => {
    const c = el('circle', {cx:X(p.x), cy:Y(p.y), r:p.r || 5, fill:p.color || css('--s1'),
                            stroke:css('--surface'), 'stroke-width':2,
                            'fill-opacity':p.open ? 0.35 : 0.95}, svg);
    c.addEventListener('mousemove', e => showTip(e, p.tip));
    c.addEventListener('mouseleave', hideTip);
  });
}

/* ------------------------------------------------------------- components */
function tiles(list) {
  return `<div class="tiles">` + list.map(t => `<div class="tile">
    <div class="k">${esc(t.k)}</div>
    <div class="v ${t.cls || ''}">${t.v}</div>
    ${t.s ? `<div class="s">${t.s}</div>` : ''}</div>`).join('') + `</div>`;
}
function table(cols, rows, opts) {
  opts = opts || {};
  if (!rows.length) return '<div class="empty">geen rijen</div>';
  return `<div class="scroll"><table><thead><tr>` +
    cols.map(c => `<th>${esc(c.h)}</th>`).join('') + `</tr></thead><tbody>` +
    rows.map(r => `<tr>` + cols.map(c => {
      const v = c.f(r);
      return `<td class="${c.cls ? c.cls(r) : ''}">${v === undefined || v === null ? '–' : v}</td>`;
    }).join('') + `</tr>`).join('') + `</tbody></table></div>`;
}
function legend(items) {
  return `<div class="legend">` + items.map(i =>
    `<span><i style="background:${i.color}"></i>${esc(i.label)}</span>`).join('') + `</div>`;
}
function chartBlock(id, height) {
  return `<div class="chart" id="${id}" style="min-height:${height || 240}px"></div>`;
}
function bookRow(label, b) {
  if (!b) return null;
  return {label, n:b.n, hit:b.hit_rate_pct, mean:b.mean, med:b.median, t:b.t,
          ci:b.ci95 ? `${b.ci95[0]} … ${b.ci95[1]}` : '–'};
}
const BOOKCOLS = [
  {h:'', f:r => esc(r.label)},
  {h:'n', f:r => r.n},
  {h:'raak %', f:r => n1(r.hit)},
  {h:'gem. %', f:r => `<span class="${sgn(r.mean)}">${pc(r.mean)}</span>`},
  {h:'mediaan %', f:r => pc(r.med)},
  {h:'t', f:r => n2(r.t)},
  {h:'95% interval', f:r => r.ci}];

/* ------------------------------------------------------------------ tabs */
const S = D.stats, TR = S.trading, RK = S.ranking, BK = S.buckets, TM = S.timing;
const closed = D.trades.filter(t => t.closed && t.ret_pct !== null && t.ret_pct !== undefined);
const openPos = D.trades.filter(t => !t.closed);
const drawers = [];

function tabOverzicht() {
  const eq = TR.equity || {};
  const pt = TR.per_trade || {};
  const ctl = TR.control_short_everything;
  let html = `<p class="lead">Wat het geld deed, over ${eq.days || 0} handelsdagen.
    Dit is de rekening, niet het onderzoek: alleen namen die de conviction-floor,
    de omzetvloer en de borrow-check haalden staan hier in.</p>`;
  html += tiles([
    {k:'rendement rekening', v:pc(eq.return_pct), cls:sgn(eq.return_pct),
     s:`${usd(eq.start)} → ${usd(eq.last)}`},
    {k:'gerealiseerde P&L', v:usd(TR.total_pnl_usd), cls:sgn(TR.total_pnl_usd),
     s:`${TR.n_closed} afgeronde posities`},
    {k:'per trade', v:pc(pt.mean), cls:sgn(pt.mean),
     s:`t=${n2(pt.t)}, 95% ${pt.ci95 ? pt.ci95.join(' … ') : '–'}`},
    {k:'trefkans', v:`${n1(pt.hit_rate_pct)}%`, s:`${pt.hits}/${pt.n} posities in de plus`},
    {k:'grootste terugval', v:pc(eq.max_drawdown_pct), cls:'neg',
     s:'piek naar dal, dagelijkse equity'},
    {k:'gratis controle', v:ctl ? pc(ctl.mean) : '–', cls:ctl ? sgn(ctl.mean) : '',
     s:'alles shorten, geen research, zelfde dagen'}]);

  html += `<div class="card"><h3>Equity, zoals de broker hem rapporteert</h3>
    ${chartBlock('c-equity', 250)}
    <small>Het laatste punt is intraday en beweegt nog: er staan
    ${openPos.length} open posities.</small></div>`;

  html += `<div class="card"><h3>Gerealiseerde P&L per instapdag</h3>
    ${legend([{color:css('--good'), label:'winst'}, {color:css('--bad'), label:'verlies'}])}
    ${chartBlock('c-daypnl', 220)}
    <small>Toegerekend aan de dag waarop de positie is geopend, niet aan de dag
    waarop hij sloot.</small></div>`;

  const warn = [];
  if (RK.rho_impact_sum !== undefined && RK.rho_impact_sum < 0.1)
    warn.push(`De rangschikking over alle ${RK.days} dagen staat op ρ=${n3(RK.rho_impact_sum)}
      (${RK.n} namen). De gratis controle <code>-run_up_20d_pct</code> staat op
      ρ=${n3(RK.rho_control_neg_runup)}. Op deze steekproef sorteert de hunt de dag niet.`);
  if (closed.length < 20)
    warn.push(`${closed.length} afgeronde posities. Bij deze n zegt elk rendement hier
      vrijwel niets: het 95%-interval per trade loopt van
      ${pt.ci95 ? pt.ci95.join(' tot ') : '–'} procent.`);
  if (TR.by_side && TR.by_side.long && TR.by_side.short)
    warn.push(`Het resultaat zit in één been: long ${pc(TR.by_side.long.mean)} over
      ${TR.by_side.long.n} posities tegen ${pc(TR.by_side.short.mean)} over
      ${TR.by_side.short.n} shorts. Dat is geen strategie-resultaat maar een
      marktrichting in een week.`);
  html += `<div class="card warnbox"><h3>Wat dit niet bewijst</h3><ul>` +
    warn.map(w => `<li>${w}</li>`).join('') + `</ul></div>`;

  drawers.push(() => {
    const c = (D.account && D.account.curve) || [];
    lineChart(document.getElementById('c-equity'), {
      x: c.map(p => p.date.slice(5)),
      series: [{label:'equity', color:css('--s1'), values:c.map(p => p.equity)}],
      fmtY: v => '$' + (v/1000).toFixed(1) + 'k', fmtT: v => usd(v), height:250});
    barChart(document.getElementById('c-daypnl'), {
      items: TR.daily.map(d => ({label:d.date.slice(5), v:d.pnl_usd,
        sub:`${d.n}×`,
        tip:`<b>${d.date}</b><br>${esc(d.symbols)}<br>inzet ${usd(d.notional_usd)}
             (${n1(d.gross_pct_of_equity)}% van equity)<br>
             P&amp;L ${usd(d.pnl_usd)} = ${pc(d.ret_on_notional_pct)} op de inzet`})),
      fmtY: v => usd(v), fmtT: v => usd(v), height:220});
  });
  return html;
}

function tabTrades() {
  let html = `<p class="lead">Elke ronde die de rekening echt heeft gedaan, uit de
    fill-stroom van de broker gematcht: open tot weer vlak. Deelverkopen over
    meerdere dagen tellen als één positie met een gewogen uitstap.</p>`;
  const rows = [bookRow('alle afgeronde posities', TR.per_trade),
                bookRow('long', (TR.by_side||{}).long),
                bookRow('short', (TR.by_side||{}).short),
                bookRow('amc', (TR.by_session||{}).amc),
                bookRow('bmo', (TR.by_session||{}).bmo),
                bookRow('uitstap door stage E', (TR.by_exit_source||{})['stage E']),
                bookRow('uitstap met de hand', (TR.by_exit_source||{}).manual),
                bookRow('controle: alles shorten', TR.control_short_everything)
               ].filter(Boolean);
  html += `<div class="card"><h3>Rendement per snede</h3>${table(BOOKCOLS, rows)}
    <small>De laatste rij is geen trade maar de gratis controle over dezelfde dagen:
    elke naam in de run shorten en geen research doen.</small></div>`;

  html += `<div class="card"><h3>Rendement per positie</h3>
    ${legend([{color:css('--good'), label:'in de plus'}, {color:css('--bad'), label:'in de min'}])}
    ${chartBlock('c-trades', 240)}
    <small>Volgorde van instap. Kleur is de uitkomst, niet de richting.</small></div>`;

  const cols = [
    {h:'ticker', f:t => `<b>${esc(t.symbol)}</b>`},
    {h:'kant', f:t => t.side},
    {h:'sessie', f:t => t.session || '–'},
    {h:'impact', f:t => t.impact_sum === undefined ? '–' : n1(t.impact_sum)},
    {h:'in', f:t => t.entry_utc.slice(5,16).replace('T',' ')},
    {h:'uit', f:t => t.exit_utc ? t.exit_utc.slice(5,16).replace('T',' ') : 'open'},
    {h:'uren', f:t => n1(t.hold_hours)},
    {h:'inzet', f:t => usd(t.entry_notional_usd)},
    {h:'rendement', f:t => `<span class="${sgn(t.ret_pct)}">${pc(t.ret_pct)}</span>`},
    {h:'P&L', f:t => `<span class="${sgn(t.pnl_usd)}">${usd(t.pnl_usd)}</span>`},
    {h:'uitstap', f:t => `${t.exit_source || '–'}${t.exit_tif ? ' / '+t.exit_tif : ''}`},
    {h:'deel-fills', f:t => `${t.n_exit_fills || 0}${t.partial_exit_days > 1 ? ` (${t.partial_exit_days}d)` : ''}`},
    {h:'spread in %', f:t => n2(t.entry_spread_pct)}];
  html += `<div class="card"><h3>Alle posities</h3>${table(cols, D.trades)}
    <small>Een uitstap met <code>opg</code> of <code>cls</code> die niet kruiste,
    laat de positie openstaan; de kolom deel-fills en de kolom uren laten dat zien.</small></div>`;

  drawers.push(() => {
    barChart(document.getElementById('c-trades'), {
      items: closed.map(t => ({label:t.symbol, v:t.ret_pct,
        sub:t.entry_utc.slice(5,10),
        tip:`<b>${esc(t.symbol)}</b> ${t.side}, ${t.session || '?'}<br>
             ${t.entry_utc.slice(0,16).replace('T',' ')} → ${(t.exit_utc||'').slice(0,16).replace('T',' ')}<br>
             ${pc(t.ret_pct)} · ${usd(t.pnl_usd)} · ${n1(t.hold_hours)} uur<br>
             impact_sum ${t.impact_sum ?? '–'} · uitstap ${t.exit_source}`})),
      fmtY: v => v.toFixed(0) + '%', fmtT: v => pc(v), height:240});
  });
  return html;
}

function tabScore() {
  let html = `<p class="lead">Het onderzoeksniveau: elke gerangschikte naam van elke
    run, of er nu geld op stond of niet (${RK.n} namen over ${RK.days} dagen).
    Het rendement hier is het bord-rendement — de koersbeweging in de richting van
    het teken van <code>impact_sum</code>, zonder spread en zonder uitvoering.</p>`;
  html += tiles([
    {k:'ρ rangschikking', v:n3(RK.rho_impact_sum),
     s:`impact_sum tegen de beweging, binnen dagen gepoold`},
    {k:'ρ gratis controle', v:n3(RK.rho_control_neg_runup), s:'−run-up 20 dagen'},
    {k:'ρ conviction', v:n3(RK.rho_conviction_vs_sign),
     s:'voorspelt |impact| of het teken klopte'},
    {k:'teken raak', v:`${RK.sign_hits}/${RK.sign_n}`,
     s:`${n1(100*RK.sign_hits/RK.sign_n)}% over alle namen`}]);

  html += `<div class="card"><h3>Rendement per score-emmer</h3>
    ${legend([{color:css('--s1'), label:'boven de conviction-floor'},
              {color:css('--muted'), label:'eronder — zou niet gehandeld worden'}])}
    ${chartBlock('c-buckets', 240)}
    <small>Emmers over |impact_sum|. De conviction-floor staat op
    ${D.conviction_floor}: alles rechts daarvan is wat er gehandeld zou worden.</small></div>`;

  html += `<div class="card"><h3>Score tegen realisatie</h3>
    ${legend([{color:css('--s1'), label:'amc'}, {color:css('--s2'), label:'bmo'}])}
    ${chartBlock('c-scatter', 330)}
    <small>Rechtsboven en linksonder is het teken goed. Een wolk zonder helling is
    een rangschikking die niet werkt.</small></div>`;

  html += `<div class="card"><h3>Per dag</h3>` +
    table([{h:'run', f:r => r.run_date}, {h:'namen', f:r => r.n},
           {h:'ρ impact_sum', f:r => `<span class="${sgn(r.rho)}">${n3(r.rho)}</span>`},
           {h:'ρ controle', f:r => n3(r.rho_control)},
           {h:'boven floor', f:r => r.floor_n},
           {h:'gem. bord-rendement', f:r => `<span class="${sgn(r.floor_mean_ret_pct)}">${pc(r.floor_mean_ret_pct)}</span>`}],
          RK.per_day) +
    `<small>Eén dag is een anekdote. De kolom ρ wisselt hier van +0.9 tot −0.3 op
     acht namen per dag; dat is precies wat ruis eruit ziet.</small></div>`;

  html += `<div class="card"><h3>Long tegen short</h3>` +
    table(BOOKCOLS, BK.by_signed_impact.map(b => bookRow(b.label, b))) + `</div>`;

  drawers.push(() => {
    barChart(document.getElementById('c-buckets'), {
      items: BK.by_abs_impact.map(b => ({label:b.label, v:b.mean,
        sub:`n=${b.n}`, color: b.lo >= D.conviction_floor ? css('--s1') : css('--muted'),
        tip:`<b>|impact_sum| ${esc(b.label)}</b><br>n=${b.n}, trefkans ${n1(b.hit_rate_pct)}%<br>
             gemiddeld ${pc(b.mean)}, mediaan ${pc(b.median)}<br>t=${n2(b.t)}`})),
      fmtY: v => v.toFixed(0) + '%', fmtT: v => pc(v), height:240});
    scatterChart(document.getElementById('c-scatter'), {
      points: BK.scatter.map(p => ({x:p.impact_sum, y:p.move,
        color: p.session === 'amc' ? css('--s1') : css('--s2'),
        r: p.traded ? 7 : 4.5, open: !p.traded,
        tip:`<b>${esc(p.ticker)}</b> ${p.run_date} ${p.session}<br>
             impact_sum ${n1(p.impact_sum)} → beweging ${pc(p.move)}<br>
             ${p.traded ? 'gehandeld' : 'niet gehandeld'}`})),
      labelX:'impact_sum (punten van spot)', labelY:'gerealiseerde beweging %',
      fmtY: v => v.toFixed(0) + '%', height:330});
  });
  return html;
}

function tabLessons() {
  const L = S.lessons;
  let html = `<p class="lead">De enige meting van <code>edge/LESSONS.md</code>: de
    hunter maakt zijn sommen eerst zonder het bestand, dat wordt bevroren als
    <code>pre_lessons</code>, daarna leest hij het en herziet. Beide getallen worden
    tegen dezelfde beweging gerangschikt.</p>`;
  if (!L.n) {
    html += `<div class="card warnbox"><h3>Nog geen meting</h3>
      <p>${esc(L.coverage_note)}</p>
      <p>Zodra één run <code>diagnostics.impact_sum_pre_lessons</code> draagt, vult dit
      tabblad zich vanzelf: ρ voor en na, het boek voor en na, en de namen waar het
      bestand de som het hardst verzette.</p></div>`;
    return html;
  }
  html += tiles([
    {k:'ρ vóór LESSONS.md', v:n3(L.rho_before), s:`${L.n} namen, ${L.days} dagen`},
    {k:'ρ ná LESSONS.md', v:n3(L.rho_after), s:'zelfde namen, zelfde beweging'},
    {k:'boek vóór', v:pc((L.book_before||{}).mean), cls:sgn((L.book_before||{}).mean)},
    {k:'boek ná', v:pc((L.book_after||{}).mean), cls:sgn((L.book_after||{}).mean)}]);
  html += `<div class="card"><h3>Per naam</h3>` +
    table([{h:'run', f:r => r.run_date}, {h:'ticker', f:r => `<b>${esc(r.ticker)}</b>`},
           {h:'vóór', f:r => n1(r.before)}, {h:'ná', f:r => n1(r.after)},
           {h:'verschil', f:r => `<span class="${sgn(r.delta)}">${n1(r.delta)}</span>`},
           {h:'beweging', f:r => pc(r.move)}], L.rows) + `</div>`;
  return html;
}

function tabTiming() {
  const H = TM.horizons;
  let html = `<p class="lead">Waar op de klok het rendement zit. Instap staat vast —
    de slotkoers vóór de print — dus alleen de uitstap beweegt. Alles vóór de opening
    is een prijs die bestond, geen omvang die kon handelen: de bron levert geen volume
    buiten de reguliere sessie.</p>`;
  const rows = H.map(h => ({h, all:TM.all[h], amc:TM.amc[h], bmo:TM.bmo[h]}));
  html += `<div class="card"><h3>Rendement per uitstapmoment, boek boven de floor</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-horizon', 250)}</div>`;
  html += `<div class="card"><h3>Per uitstapmoment</h3>` +
    table([{h:'moment', f:r => `<code>${esc(r.h)}</code>`},
           {h:'n', f:r => r.all.n},
           {h:'ρ', f:r => n3(r.all.rho_impact_sum)},
           {h:'ρ conviction', f:r => n3(r.all.rho_conviction_vs_sign)},
           {h:'teken %', f:r => n1(r.all.sign_hit_rate)},
           {h:'boek %', f:r => `<span class="${sgn(r.all.floor_mean_ret_pct)}">${pc(r.all.floor_mean_ret_pct)}</span>`},
           {h:'t', f:r => n2(r.all.floor_t)},
           {h:'amc %', f:r => `<span class="${sgn((r.amc||{}).floor_mean_ret_pct)}">${pc((r.amc||{}).floor_mean_ret_pct)}</span>`},
           {h:'bmo %', f:r => `<span class="${sgn((r.bmo||{}).floor_mean_ret_pct)}">${pc((r.bmo||{}).floor_mean_ret_pct)}</span>`},
           {h:'deel van de dagbeweging', f:r => n2(r.all.median_frac_of_close_move)}],
          rows) +
    `<small><code>ext_early</code> is een half uur nabeurs voor amc en de vroege
     voorbeurs voor bmo; <code>close</code> is de reguliere slotkoers van de
     reactiesessie en is de huidige basis.</small></div>`;

  html += `<div class="card"><h3>Per uur na de instapkoers</h3>
    ${legend([{color:css('--s1'), label:'alles'}, {color:css('--s2'), label:'amc'},
              {color:css('--s3'), label:'bmo'}])}
    ${chartBlock('c-hourly', 260)}
    <small>17.5 is de opening van de reactiesessie, 24 de slotkoers. De uren 5 tot 11
    ontbreken: daar bestaat wel een prijs maar geen uitstap.</small></div>`;

  const legs = TM.legs || {};
  html += `<div class="card"><h3>De twee benen van de hold</h3>` +
    table([{h:'been', f:r => esc(r.k)}, {h:'n', f:r => r.v.n},
           {h:'ρ', f:r => n3(r.v.rho_impact_sum)},
           {h:'boek %', f:r => `<span class="${sgn(r.v.floor_mean_ret_pct)}">${pc(r.v.floor_mean_ret_pct)}</span>`},
           {h:'t', f:r => n2(r.v.floor_t)},
           {h:'gem. |beweging|', f:r => n2(r.v.mean_abs_move_pct)}],
          Object.entries(legs).map(([k,v]) => ({k,v}))) +
    `<small>Als de gap betaalt en de sessie daarna teruggeeft, zit je zes punten
     beweging uit voor niets.</small></div>`;

  drawers.push(() => {
    lineChart(document.getElementById('c-horizon'), {
      x: H,
      series: [
        {label:'alles', color:css('--s1'), values:H.map(h => TM.all[h].floor_mean_ret_pct ?? null)},
        {label:'amc', color:css('--s2'), values:H.map(h => (TM.amc[h]||{}).floor_mean_ret_pct ?? null)},
        {label:'bmo', color:css('--s3'), values:H.map(h => (TM.bmo[h]||{}).floor_mean_ret_pct ?? null)}],
      fmtY: v => v.toFixed(0) + '%', fmtT: v => pc(v), zero:true, height:250});
    const hrs = TM.hourly.grid_hours.map(String);
    lineChart(document.getElementById('c-hourly'), {
      x: hrs,
      series: [
        {label:'alles', color:css('--s1'), values:hrs.map(h => (TM.hourly.all[h]||{}).mean_ret_pct ?? null)},
        {label:'amc', color:css('--s2'), values:hrs.map(h => (TM.hourly.amc[h]||{}).mean_ret_pct ?? null)},
        {label:'bmo', color:css('--s3'), values:hrs.map(h => (TM.hourly.bmo[h]||{}).mean_ret_pct ?? null)}],
      fmtY: v => v.toFixed(0) + '%', fmtT: v => pc(v), zero:true, height:260});
  });
  return html;
}

function tabCapaciteit() {
  let html = `<p class="lead">Wat het boek aan kapitaal bezet, en wat de namen aan
    omzet dragen. Twee lezingen van dezelfde vraag: het rendement per ingezette
    dollar per dag, en het rendement per liquiditeitsklasse van de naam.</p>`;
  html += `<div class="card"><h3>Inzet en opbrengst per dag</h3>` +
    table([{h:'dag', f:d => d.date}, {h:'posities', f:d => d.n},
           {h:'inzet', f:d => usd(d.notional_usd)},
           {h:'% van equity', f:d => n1(d.gross_pct_of_equity)},
           {h:'omzet', f:d => usd(d.turnover_usd)},
           {h:'P&L', f:d => `<span class="${sgn(d.pnl_usd)}">${usd(d.pnl_usd)}</span>`},
           {h:'op de inzet', f:d => `<span class="${sgn(d.ret_on_notional_pct)}">${pc(d.ret_on_notional_pct)}</span>`},
           {h:'op de equity', f:d => `<span class="${sgn(d.ret_on_equity_pct)}">${pc(d.ret_on_equity_pct)}</span>`},
           {h:'namen', f:d => `<span class="t">${esc(d.symbols)}</span>`}],
          TR.daily) +
    `<small>Omzet is wat er die dag verhandeld is, in en uit samen: de basis waarop
     transactiekosten drukken. Inzet is de bruto positie bij instap.</small></div>`;

  html += `<div class="card"><h3>Rendement op de inzet tegen wat er omging</h3>
    ${legend([{color:css('--good'), label:'dag in de plus'}, {color:css('--bad'), label:'dag in de min'}])}
    ${chartBlock('c-turnover', 230)}
    <small>Eén punt per handelsdag. Een dag met veel omzet en weinig rendement is
    waar de kosten het verschil maken.</small></div>`;

  html += `<div class="card"><h3>Bord-rendement per liquiditeitsklasse</h3>
    ${chartBlock('c-adv', 230)}
    <small>Dagomzet van de naam zelf (prijs × gemiddeld volume 20 dagen), over alle
    gerangschikte namen. De uitvoeringsvloer van stage E staat op $200k; de
    backtest liet het beste resultaat in de dunste namen vallen, en daar is de
    positie precies niet te vullen.</small></div>`;

  const adv = BK.by_adv.map(b => bookRow(b.label, b));
  html += `<div class="card"><h3>Per klasse</h3>` + table(BOOKCOLS, adv) + `</div>`;

  drawers.push(() => {
    scatterChart(document.getElementById('c-turnover'), {
      points: TR.daily.filter(d => d.ret_on_notional_pct !== null).map(d => ({
        x:d.turnover_usd/1000, y:d.ret_on_notional_pct,
        color: d.pnl_usd >= 0 ? css('--good') : css('--bad'),
        tip:`<b>${d.date}</b><br>omzet ${usd(d.turnover_usd)}, inzet ${usd(d.notional_usd)}<br>
             ${pc(d.ret_on_notional_pct)} op de inzet · ${usd(d.pnl_usd)}`})),
      labelX:'verhandelde omzet die dag', labelY:'rendement op de inzet %',
      fmtY: v => v.toFixed(0) + '%', fmtX: v => '$' + v.toFixed(0) + 'k', height:230});
    barChart(document.getElementById('c-adv'), {
      items: BK.by_adv.map(b => ({label:b.label, v:b.mean, sub:`n=${b.n}`,
        color: css('--s1'),
        tip:`<b>${esc(b.label)} dagomzet</b><br>n=${b.n}, trefkans ${n1(b.hit_rate_pct)}%<br>
             gemiddeld ${pc(b.mean)}, t=${n2(b.t)}<br>${b.above_floor} boven de conviction-floor`})),
      fmtY: v => v.toFixed(0) + '%', fmtT: v => pc(v), height:230});
  });
  return html;
}

function tabData() {
  let html = `<p class="lead">Waar alles vandaan komt en wat er niet in zit.</p>`;
  html += `<div class="card"><h3>Herkomst</h3><ul>
    <li>Runs: ${D.runs.length}, van ${esc(D.runs[0])} tot ${esc(D.runs[D.runs.length-1])}</li>
    <li>Namen geprijsd: ${D.names.length} · in de rangschikking: ${RK.n} (dubbele events eruit)</li>
    <li>Broker: ${D.account ? esc(D.account.endpoint) + (D.account.paper ? ' (paper)' : ' (live)') : '–'}</li>
    <li>Koersen: Yahoo dag- en 5-minutenbalken, gecached in <code>.cache/bars</code></li>
    <li>Gebouwd: ${esc(D.generated_utc)}</li>
    ${D.broker_error ? `<li class="neg">Broker: ${esc(D.broker_error)}</li>` : ''}
  </ul></div>`;
  if (D.problems && D.problems.length)
    html += `<div class="card"><h3>Wat niet geprijsd kon worden (${D.problems.length})</h3>
      <div class="scroll"><ul>` + D.problems.map(p => `<li>${esc(p)}</li>`).join('') +
      `</ul></div></div>`;
  const cols = [
    {h:'run', f:r => r.run_date}, {h:'ticker', f:r => `<b>${esc(r.ticker)}</b>`},
    {h:'sessie', f:r => r.session}, {h:'event', f:r => r.event_date},
    {h:'impact_sum', f:r => n1(r.impact_sum)},
    {h:'bevindingen', f:r => r.n_findings},
    {h:'−run-up', f:r => n1(r.neg_runup)},
    {h:'dagomzet', f:r => usd(r.dollar_vol || r.plan_dollar_volume_usd)},
    {h:'beweging', f:r => pc(r.mv_close)},
    {h:'bord-rendement', f:r => `<span class="${sgn(r.ret_close)}">${pc(r.ret_close)}</span>`},
    {h:'gehandeld', f:r => r.traded ? `ja (${pc(r.trade_ret_pct)})` : '–'},
    {h:'dubbel', f:r => r.duplicate_event ? 'ja' : ''}];
  html += `<div class="card"><h3>Alle gerangschikte namen</h3>${table(cols, D.names)}
    <small>Ook in <code>edge/performance/data/names.csv</code> en
    <code>trades.csv</code>, voor wie liever zelf rekent.</small></div>`;
  html += `<div class="card"><h3>Ververs dit dashboard</h3>
    <p>Eén knop, in de repo-root:</p>
    <p><code>./edge/performance/update.sh</code></p>
    <p>Die haalt de fills en de equity bij de broker op, herprijst elke run die nog
    openstond, herbouwt <code>data/ledger.json</code> en rendert dit bestand
    opnieuw. Zonder netwerk: <code>./edge/performance/update.sh --offline</code>,
    dat houdt de vorige broker-stand aan.</p></div>`;
  return html;
}

/* ------------------------------------------------------------------ boot */
const TABS = [
  ['Overzicht', tabOverzicht], ['Trades', tabTrades], ['Score', tabScore],
  ['Lessons', tabLessons], ['Timing', tabTiming], ['Capaciteit', tabCapaciteit],
  ['Data', tabData]];
const nav = document.getElementById('tabs'), panels = document.getElementById('panels');
TABS.forEach(([name, fn], i) => {
  const b = document.createElement('button');
  b.textContent = name; b.setAttribute('role', 'tab');
  b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
  b.onclick = () => select(i);
  nav.appendChild(b);
  const s = document.createElement('section');
  s.hidden = i !== 0; s.dataset.idx = i;
  panels.appendChild(s);
});
function select(i) {
  [...nav.children].forEach((b, j) => b.setAttribute('aria-selected', i === j ? 'true' : 'false'));
  [...panels.children].forEach((s, j) => s.hidden = i !== j);
  render(i);
}
const built = new Set();
function render(i) {
  const s = panels.children[i];
  if (!built.has(i)) {
    drawers.length = 0;
    s.innerHTML = TABS[i][1]();
    s.__drawers = [...drawers];
    built.add(i);
  }
  (s.__drawers || []).forEach(d => d());
}
document.getElementById('stamp').textContent =
  `gebouwd ${D.generated_utc} · ${D.runs.length} runs · ${RK.n} namen · ` +
  `${closed.length} afgeronde posities · conviction-floor ${D.conviction_floor}`;
document.getElementById('theme').onclick = () => {
  const now = document.documentElement.getAttribute('data-theme');
  const dark = now ? now === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
  [...panels.children].forEach((s, i) => { if (built.has(i)) render(i); });
};
let rt;
addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => {
  [...panels.children].forEach((s, i) => { if (built.has(i) && !s.hidden) render(i); });
}, 120); });
select(0);
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
    kb = len(html.encode()) / 1024
    print(f"wrote {a.out}  ({kb:.0f} kB, {len(led['names'])} names, "
          f"{len(led['trades'])} positions)")


if __name__ == "__main__":
    main()
