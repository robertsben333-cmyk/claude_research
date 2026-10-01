#!/usr/bin/env python3
"""Write threshold-chart.html from scores.json. Run score_full.py first."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(f'{D}/scores.json'))

HTML = r'''<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Drempel en rendement</title>
<style>
:root{color-scheme:light;--bg:#fcfcfb;--card:#f3f3f1;--fg:#1d1d1b;--mut:#5f5e57;--grid:#e2e1dc;--zero:#a3a29b;--ref:#7b7a73;--band:.13;
--s0:#2a78d6;--s1:#eb6834;--s2:#1baf7a;--s3:#eda100;--s4:#e87ba4}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])){color-scheme:dark;--bg:#1a1a19;--card:#232321;--fg:#ffffff;--mut:#c3c2b7;--grid:#34342f;--zero:#6b6a63;--ref:#9a998f;--band:.2;
--s0:#3987e5;--s1:#d95926;--s2:#199e70;--s3:#c98500;--s4:#d55181}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#1a1a19;--card:#232321;--fg:#ffffff;--mut:#c3c2b7;--grid:#34342f;--zero:#6b6a63;--ref:#9a998f;--band:.2;
--s0:#3987e5;--s1:#d95926;--s2:#199e70;--s3:#c98500;--s4:#d55181}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:0 auto;padding:20px 16px 48px}
h1{font-size:22px;margin:0 0 6px}
p{margin:6px 0;color:var(--mut);max-width:80ch}
.bar{position:sticky;top:0;z-index:4;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--grid);display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
.seg{display:inline-flex;border:1px solid var(--grid);border-radius:7px;overflow:hidden}
.seg button{border:0;background:var(--card);color:var(--fg);padding:5px 10px;font:inherit;font-size:13px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--grid);background:var(--card);color:var(--fg);border-radius:999px;padding:3px 10px 3px 8px;font:inherit;font-size:13px;cursor:pointer}
.chip[aria-pressed="false"]{opacity:.45}
.chip svg{width:16px;height:12px}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,540px),1fr));gap:16px;margin-top:16px}
.panel{background:var(--card);border-radius:10px;padding:12px 12px 8px}
.panel h2{font-size:16px;margin:0}
.sub{font-size:12.5px;color:var(--mut)}
svg.ch{width:100%;height:auto;display:block;touch-action:none}
.cap{font-size:11.5px;fill:var(--mut)}
.stats{width:100%;border-collapse:collapse;font-size:12.5px;margin:6px 0 2px;font-variant-numeric:tabular-nums}
.stats th,.stats td{padding:2px 5px;text-align:right;border-bottom:1px solid var(--grid);white-space:nowrap}
.stats th:first-child,.stats td:first-child{text-align:left}
.stats th{font-weight:600;color:var(--mut)}
.tw{overflow-x:auto}
#tip{position:fixed;pointer-events:none;background:var(--bg);color:var(--fg);border:1px solid var(--grid);padding:7px 9px;border-radius:7px;font-size:12px;display:none;box-shadow:0 3px 12px rgba(0,0,0,.18);z-index:9;font-variant-numeric:tabular-nums}
#tip table{border-collapse:collapse}#tip td{padding:1px 5px;text-align:right}#tip td:first-child{text-align:left}
details{margin-top:22px}summary{cursor:pointer;font-weight:600}
.note{font-size:13px}
</style></head><body><main>
<h1>Wat doet de impact-drempel met het rendement per trade?</h1>
<p>Blinde herbeoordeling van elke opgeloste run in de US, Europa, Japan en Australië, __N__ namen, door vier modellen: Opus 5, Opus 5.5, Sonnet 5.5 en Fable 5.1. Elk model kreeg het bewijs van de live hunter zonder diens getallen en woog het opnieuw onder de gedeelde prompt, zonder internet. De namen die eerder als lek werden uitgesloten, zijn nu meegenomen met een geanonimiseerd pakket. Rendement per trade = teken × gerealiseerde koers. US met strategie-exit en $200k omzetvloer.</p>
<div class="bar">
 <div class="seg" id="key" role="group" aria-label="sleutel"><button data-v="impact">impact_sum</button><button data-v="pup">p_up − 50 (zonder absolute move)</button></div>
 <div class="seg" id="mode" role="group" aria-label="x-as"><button data-v="abs">Absolute drempel</button><button data-v="pct">Gelijke selectiviteit</button></div>
 <div class="seg" id="band" role="group" aria-label="band"><button data-v="on">95%-band aan</button><button data-v="off">uit</button></div>
 <div class="chips" id="chips" aria-label="reeksen"></div>
</div>
<div class="panels" id="panels"></div>
<p class="note" style="margin-top:14px"><b>Lezen.</b> Boven: gemiddeld rendement per trade, met de 95%-band (±1,96 standaardfout) waar er minstens 5 trades zijn. Midden: aandeel trades met het goede teken. Onder: aantal trades dat de drempel haalt. Lijnen stoppen onder 3 trades; holle punten hebben 3 of 4 trades. Grijze stippellijn: alle verhandelbare namen shorten. Verticale stippellijn: de huidige vloer van 3,0. Gekleurde driehoekjes op de x-as: per arm de herafgeleide vloer, dat is de drempel die bij die arm hetzelfde aandeel namen selecteert als 3,0 deed bij de live hunt op de Opus 5-dagen (__SHARE__). Alles is bruto: er zijn geen kosten aangenomen (geen spread, commissie of leenkosten).</p>
<p class="note"><b>Sleutel.</b> <code>impact_sum</code> = (2 × p_up / 100 − 1) × abs_move: richting maal verwachte grootte. <code>p_up − 50</code> laat de grootte weg en rangschikt alleen op hoe zeker de beoordelaar is van de richting, in punten (55 wordt +5, 38 wordt −12). De live hunts van vóór de gedeelde prompt geven geen p_up, dus bij die sleutel ontbreekt de live arm. De herafgeleide vloer gebruikt in beide gevallen hetzelfde aandeel namen.</p>
<p class="note">De absolute drempel bevoordeelt wie groot sized: de herbeoordelingen sizen kleiner en hebben bij 3 geen namen meer. Gelijke selectiviteit vergelijkt elke arm op het eigen bovenste deel van de verdeling. Familiewise p: de beste t over 25 drempels, getoetst tegen hetzelfde maximum bij geschudde koersen binnen elke dag. Leave-one-day-out: kies de drempel op de andere dagen, handel de weggelaten dag.</p>
<details><summary>Tabel met alle punten</summary><div class="tw" id="tbl"></div></details>
</main><div id="tip" role="status"></div>
<script>
const S=__DATA__;
const ARMS=Object.keys(S.arms), LAB=S.arms;
const SHAPES=["circle","square","triangle","diamond","cross"];
const G=[["all","Alle regio's"],["all_clean","Alle regio's, zonder geanonimiseerde namen"],["us","US"],["us_clean","US, zonder geanonimiseerde namen"],["ex_us","Buiten de US"],["europe","Europa"],["apac","Japan en Australië"],["us_opus5_era","US, runs t/m 09-22 (Opus 5-hunters)"],["us_opus55_era","US, runs vanaf 09-23 (Opus 5.5-hunters)"],["anonymised","Eerder uitgesloten namen (geanonimiseerd)"]].filter(g=>S.groups[g[0]]);
const st={key:"impact",mode:"abs",band:"on",hide:{}};
const GR=()=>S.keys[st.key];
const present=a=>!!GR().all[a];
try{Object.assign(st,JSON.parse(localStorage.getItem("thr4")||"{}"))}catch(e){}
const save=()=>{try{localStorage.setItem("thr4",JSON.stringify(st))}catch(e){}};
const col=a=>`var(--s${ARMS.indexOf(a)})`;
const f1=(x,d=2)=>x==null?"–":(x>0?"+":"")+x.toFixed(d);
function mark(shape,x,y,r,c,hollow){const f=hollow?"var(--card)":c,s=`fill="${f}" stroke="${c}" stroke-width="1.6"`;
 if(shape=="circle")return `<circle cx="${x}" cy="${y}" r="${r}" ${s}/>`;
 if(shape=="square")return `<rect x="${x-r*.88}" y="${y-r*.88}" width="${r*1.76}" height="${r*1.76}" rx="1" ${s}/>`;
 if(shape=="triangle")return `<path d="M${x},${y-r*1.15}L${x+r},${y+r*.7}L${x-r},${y+r*.7}Z" ${s}/>`;
 if(shape=="diamond")return `<path d="M${x},${y-r*1.2}L${x+r*1.1},${y}L${x},${y+r*1.2}L${x-r*1.1},${y}Z" ${s}/>`;
 return `<path d="M${x-r},${y-r}L${x+r},${y+r}M${x+r},${y-r}L${x-r},${y+r}" stroke="${c}" stroke-width="2"/>`}
function series(g,a){const s=GR()[g][a],c=st.mode=="abs"?s.curve:s.pct_curve;
 return c.map(p=>({x:st.mode=="abs"?p.thr:p.pct,n:p.n,h:p.hits,m:p.mean,se:p.se,hr:p.n?100*p.hits/p.n:null}))}
function chips(){const el=document.getElementById("chips");el.innerHTML="";
 ARMS.forEach((a,k)=>{if(!present(a))return;const b=document.createElement("button");b.className="chip";b.setAttribute("aria-pressed",!st.hide[a]);
  b.innerHTML=`<svg viewBox="0 0 16 12"><line x1="0" x2="16" y1="6" y2="6" stroke="${col(a)}" stroke-width="2"/>${mark(SHAPES[k],8,6,3.2,col(a),false)}</svg>${LAB[a]}`;
  b.onclick=()=>{st.hide[a]=!st.hide[a];save();draw()};el.appendChild(b)})}
const W=560,L=46,R=74,X0=L,X1=W-R;
function draw(){
 for(const id of ["key","mode","band"])document.querySelectorAll(`#${id} button`).forEach(b=>b.setAttribute("aria-pressed",b.dataset.v==st[id]));
 chips();
 const box=document.getElementById("panels");box.innerHTML="";let rows="";
 const vis=ARMS.filter(a=>!st.hide[a]&&present(a)),PUP=st.key=="pup";
 const xm=st.mode=="abs"?(PUP?35:6):90,X=x=>X0+(X1-X0)*x/xm;
 for(const [g,lab] of G){
  const gg=GR()[g],ref=gg.short_all;
  const P={};vis.forEach(a=>P[a]=series(g,a).filter(p=>p.m!=null&&p.n>=3));
  // panel A: mean return
  let ys=[ref??0];vis.forEach(a=>P[a].forEach(p=>{ys.push(p.m);if(st.band=="on"&&p.n>=5&&p.se)ys.push(p.m-1.96*p.se,p.m+1.96*p.se)}));
  let step=4,lo=Math.floor(Math.min(-2,...ys)/step)*step,hi=Math.ceil(Math.max(2,...ys)/step)*step;
  if(hi-lo>40){step=10;lo=Math.floor(lo/10)*10;hi=Math.ceil(hi/10)*10}else if(hi-lo<=12){step=2}
  const HA=230,TA=10,BA=HA-8,YA=y=>TA+(BA-TA)*(hi-y)/(hi-lo);
  const HB=96,TB=HA+18,BB=TB+HB-14,YB=y=>TB+(BB-TB)*(100-y)/100;
  const nmax=Math.max(5,...vis.map(a=>Math.max(0,...series(g,a).map(p=>p.n))));const nstep=nmax>100?50:nmax>40?20:nmax>16?10:5;const ntop=Math.ceil(nmax/nstep)*nstep;
  const HC=96,TC=BB+24,BC=TC+HC-14,YC=y=>TC+(BC-TC)*(ntop-y)/ntop,H=BC+34;
  let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" role="img" aria-label="${lab}: rendement, hitrate en aantal trades per drempel">`;
  const yax=(v,Y,fmt)=>`<line x1="${X0}" x2="${X1}" y1="${Y}" y2="${Y}" stroke="var(${v==0&&fmt!="n"&&fmt!="hr"?"--zero":"--grid"})"/><text class="cap" x="${X0-6}" y="${Y+4}" text-anchor="end">${fmt=="%"?(v>0?"+":"")+v+"%":fmt=="hr"?v+"%":v}</text>`;
  for(let y=lo;y<=hi+1e-9;y+=step)s+=yax(y,YA(y),"%");
  s+=`<text class="cap" x="${X0}" y="${TA-1}" font-weight="600">gem. rendement per trade (bruto)</text>`;
  for(const y of [0,25,50,75,100])s+=yax(y,YB(y),"hr");
  s+=`<line x1="${X0}" x2="${X1}" y1="${YB(50)}" y2="${YB(50)}" stroke="var(--zero)" stroke-dasharray="2 3"/>`;
  s+=`<text class="cap" x="${X0}" y="${TB-5}" font-weight="600">hitrate (goed teken)</text>`;
  for(let y=0;y<=ntop;y+=nstep)s+=yax(y,YC(y),"n");
  s+=`<text class="cap" x="${X0}" y="${TC-5}" font-weight="600">aantal trades</text>`;
  const xt=st.mode=="abs"?(PUP?[0,5,10,15,20,25,30,35]:[0,1,2,3,4,5,6]):[0,20,40,60,80];
  for(const x of xt){s+=`<line x1="${X(x)}" x2="${X(x)}" y1="${TA}" y2="${BC}" stroke="var(--grid)" stroke-dasharray="1 4"/><text class="cap" x="${X(x)}" y="${BC+15}" text-anchor="middle">${st.mode=="abs"?"≥"+x:"top "+(100-x)+"%"}</text>`}
  s+=`<text class="cap" x="${(X0+X1)/2}" y="${H-3}" text-anchor="middle">${st.mode=="abs"?(PUP?"drempel |p_up − 50| in punten":"drempel |impact_sum|"):(PUP?"aandeel namen met de grootste |p_up − 50|":"aandeel namen met de grootste |impact_sum|")}</text>`;
  if(st.mode=="abs"){if(!PUP)s+=`<line x1="${X(3)}" x2="${X(3)}" y1="${TA}" y2="${BC}" stroke="var(--ref)" stroke-dasharray="5 4"/><text class="cap" x="${X(3)+4}" y="${TA+11}">vloer 3,0</text>`;
   vis.forEach((a,k)=>{const f=gg[a].floor_same_share;if(f!=null&&f<=xm){const x=X(f);s+=`<path d="M${x},${BC+1}l-4,7h8z" fill="${col(a)}"><title>${LAB[a]}: herafgeleide vloer ${f.toFixed(2)}</title></path>`}})}
  if(ref!=null)s+=`<line x1="${X0}" x2="${X1}" y1="${YA(ref)}" y2="${YA(ref)}" stroke="var(--ref)" stroke-dasharray="3 3"/><text class="cap" x="${X1+4}" y="${YA(ref)+4}">short alles<tspan x="${X1+4}" dy="12">${f1(ref,1)}%</tspan></text>`;
  if(st.band=="on")vis.forEach(a=>{const B=P[a].filter(p=>p.n>=5&&p.se);if(B.length>1){let d="M"+B.map(p=>X(p.x)+","+YA(p.m+1.96*p.se)).join("L")+"L"+B.slice().reverse().map(p=>X(p.x)+","+YA(p.m-1.96*p.se)).join("L")+"Z";s+=`<path d="${d}" fill="${col(a)}" fill-opacity="var(--band)" stroke="none"/>`}});
  const lbl=[];
  vis.forEach(a=>{const k=ARMS.indexOf(a),c=col(a),Q=P[a];if(!Q.length)return;
   const path=(Y,v)=>"M"+Q.filter(p=>p[v]!=null).map(p=>X(p.x)+","+Y(p[v])).join("L");
   s+=`<path d="${path(YA,"m")}" fill="none" stroke="${c}" stroke-width="2" stroke-linejoin="round"/>`;
   s+=`<path d="${path(YB,"hr")}" fill="none" stroke="${c}" stroke-width="1.6" stroke-linejoin="round"/>`;
   const N=series(g,a);s+=`<path d="M${N.map(p=>X(p.x)+","+YC(p.n)).join("L")}" fill="none" stroke="${c}" stroke-width="1.6"/>`;
   const every=st.mode=="abs"?(PUP?5:5):1;
   Q.forEach((p,i)=>{if(i%every==0||i==Q.length-1){s+=mark(SHAPES[k],X(p.x),YA(p.m),3.3,c,p.n<5)}});
   const e=Q[Q.length-1];lbl.push({a,y:YA(e.m),x:X(e.x)})});
  lbl.sort((p,q)=>p.y-q.y);for(let i=1;i<lbl.length;i++)if(lbl[i].y-lbl[i-1].y<12)lbl[i].y=lbl[i-1].y+12;
  lbl.forEach(l=>{const tx=Math.min(l.x+6,X1+4);s+=`<text x="${tx}" y="${l.y+4}" font-size="11.5" fill="var(--fg)" font-weight="600">${LAB[l.a]}</text>`});
  s+=`<line class="xh" x1="0" x2="0" y1="${TA}" y2="${BC}" stroke="var(--fg)" stroke-opacity=".35" visibility="hidden"/>`;
  s+=`<rect class="hit" x="${X0}" y="${TA}" width="${X1-X0}" height="${BC-TA}" fill="transparent"/></svg>`;
  const tr=vis.map(a=>{const q=gg[a],b=q.book_same_share||{},l=q.loo||{};
   return `<tr><td><span style="color:${col(a)}">●</span> ${LAB[a]}</td><td>${f1(q.rho)}${q.p!=null?` <span class="sub">(${q.p.toFixed(2)})</span>`:""}</td><td>${q.zeros}</td><td>${q.median_abs.toFixed(2)}</td><td>${q.floor_same_share==null?"–":q.floor_same_share.toFixed(2)}</td><td>${b.n?`${f1(b.mean,1)}% <span class="sub">n${b.n}</span>`:"–"}</td><td>${q.familywise_p==null?"–":q.familywise_p.toFixed(2)}</td><td>${l.n?`${f1(l.mean,1)}% <span class="sub">n${l.n}</span>`:"–"}</td></tr>`}).join("");
  const el=document.createElement("div");el.className="panel";
  el.innerHTML=`<h2>${lab}</h2><div class="sub">${gg[vis[0]||Object.keys(gg).find(k=>k!="short_all")].n} namen · alles shorten ${f1(gg.short_all,1)}%</div>${s}
   <div class="tw"><table class="stats"><tr><th>arm</th><th title="Spearman binnen de dag (permutatie-p)">ρ (p)</th><th title="namen op 0">nul</th><th title="mediaan |impact_sum|">med</th><th title="herafgeleide vloer: zelfde aandeel als 3,0 live">vloer</th><th title="gemiddeld rendement per trade bij die vloer">bij vloer</th><th title="familiewise p van de beste drempel">fw p</th><th title="leave-one-day-out, gemiddeld per trade">LOO</th></tr>${tr}</table></div>`;
  box.appendChild(el);
  const svg=el.querySelector("svg"),xh=svg.querySelector(".xh"),tip=document.getElementById("tip");
  const xs=series(g,Object.keys(gg).find(k=>k!="short_all")).map(p=>p.x);
  const move=ev=>{const pt=svg.createSVGPoint();pt.x=ev.clientX;pt.y=ev.clientY;const p=pt.matrixTransform(svg.getScreenCTM().inverse());
   const xv=(p.x-X0)/(X1-X0)*xm;let best=xs[0];for(const x of xs)if(Math.abs(x-xv)<Math.abs(best-xv))best=x;
   xh.setAttribute("x1",X(best));xh.setAttribute("x2",X(best));xh.setAttribute("visibility","visible");
   const rowsT=vis.map(a=>{const q=series(g,a).find(z=>z.x==best);return `<tr><td><span style="color:${col(a)}">●</span> ${LAB[a]}</td><td>${q&&q.n?q.n:0}</td><td>${q&&q.n?Math.round(q.hr)+"%":"–"}</td><td>${q&&q.m!=null?f1(q.m)+"%":"–"}</td><td>${q&&q.se?"±"+(1.96*q.se).toFixed(1):""}</td></tr>`}).join("");
   tip.innerHTML=`<b>${st.mode=="abs"?"drempel ≥"+(PUP?best:best.toFixed(1)):"top "+(100-best)+"%"}</b> · bruto<table><tr><td></td><td>n</td><td>hit</td><td>gem.</td><td>95%</td></tr>${rowsT}</table>`;
   tip.style.display="block";const tw=tip.offsetWidth;tip.style.left=Math.min(ev.clientX+14,innerWidth-tw-8)+"px";tip.style.top=(ev.clientY+14)+"px"};
  svg.querySelector(".hit").addEventListener("pointermove",move);
  svg.querySelector(".hit").addEventListener("pointerleave",()=>{tip.style.display="none";xh.setAttribute("visibility","hidden")});
  for(const a of vis)for(const p of series(g,a))if(st.mode=="pct"||(PUP?p.x%5==0:Math.round(p.x*10)%5==0))rows+=`<tr><td>${lab}</td><td>${LAB[a]}</td><td>${st.mode=="abs"?"≥"+(PUP?p.x:p.x.toFixed(1)):"top "+(100-p.x)+"%"}</td><td>${p.n}</td><td>${p.n?Math.round(p.hr)+"%":""}</td><td>${p.m==null?"":f1(p.m)+"%"}</td><td>${p.se?"±"+(1.96*p.se).toFixed(1):""}</td></tr>`;
 }
 document.getElementById("tbl").innerHTML=`<table class="stats"><tr><th>groep</th><th>arm</th><th>drempel</th><th>trades</th><th>hitrate</th><th>gem. (bruto)</th><th>95%</th></tr>${rows}</table>`;
}
for(const id of ["key","mode","band"])document.querySelectorAll(`#${id} button`).forEach(b=>b.onclick=()=>{st[id]=b.dataset.v;save();draw()});
draw();
</script></body></html>'''
open(f'{D}/threshold-chart.html', 'w').write(
    HTML.replace('__DATA__', json.dumps(S)).replace('__N__', str(S['n']))
        .replace('__SHARE__', f"{S['floor_share']:.0%} van de niet-nul verhandelbare namen"))
print('wrote threshold-chart.html')
