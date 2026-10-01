#!/usr/bin/env python3
"""Write portfolio.html: a day-by-day account simulator over the re-judge sample.

Reads key.json and the out-*-*.json files (the same 231 names score_full.py scores) and
inlines one row per name. Everything else happens in the page: per day the selected arm's
names that pass the cut go into one book, the equity is split over them (equal or by
score) with a per-name cap, the rest stays in cash, and the day's return compounds into
the next. Gross: no spread, commission or borrow. Research level, not the broker's fills.
"""
import json, glob, os
D = os.path.dirname(os.path.abspath(__file__))
key = {r['id']: r for r in json.load(open(f'{D}/key.json'))}
pid = {r.get('pid', r['id']): r['id'] for r in key.values()}
ARMS = ['opus5', 'opus', 'sonnet', 'fable']
imp = {a: {} for a in ARMS}; pup = {a: {} for a in ARMS}
for f in glob.glob(f'{D}/out-*-*.json'):
    m = os.path.basename(f)[:-5].split('-')[-1]
    for o in json.load(open(f)):
        if o['id'] in pid:
            imp[m][pid[o['id']]] = float(o.get('impact_sum') or 0)
            pup[m][pid[o['id']]] = float(o['p_up']) - 50
ids = sorted(set.intersection(*(set(imp[a]) for a in ARMS)))
rows = []
for i in ids:
    r = key[i]
    tradable = r['region'] != 'us' or (r.get('dollar_vol') or 0) >= 2e5
    rows.append([r['region'], r['day'], r['ticker'], round(r['move'], 3), int(tradable),
                 round((r.get('dollar_vol') or 0)/1e6, 2), int(bool(r.get('anon'))),
                 round(float(r['live'] or 0), 3)] +
                [round(imp[a][i], 3) for a in ARMS] + [pup[a][i] for a in ARMS])

HTML = r'''<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portfolio per dag</title>
<style>
:root{color-scheme:light;--bg:#fcfcfb;--card:#f3f3f1;--fg:#1d1d1b;--mut:#5f5e57;--grid:#e2e1dc;--zero:#a3a29b;--ref:#7b7a73;--pos:#1a7f4b;--neg:#c2410c;
--s0:#2a78d6;--s1:#eb6834;--s2:#1baf7a;--s3:#eda100;--s4:#e87ba4}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])){color-scheme:dark;--bg:#1a1a19;--card:#232321;--fg:#ffffff;--mut:#c3c2b7;--grid:#34342f;--zero:#6b6a63;--ref:#9a998f;--pos:#4ade80;--neg:#fb923c;
--s0:#3987e5;--s1:#d95926;--s2:#199e70;--s3:#c98500;--s4:#d55181}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#1a1a19;--card:#232321;--fg:#ffffff;--mut:#c3c2b7;--grid:#34342f;--zero:#6b6a63;--ref:#9a998f;--pos:#4ade80;--neg:#fb923c;
--s0:#3987e5;--s1:#d95926;--s2:#199e70;--s3:#c98500;--s4:#d55181}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:0 auto;padding:20px 16px 48px}
h1{font-size:22px;margin:0 0 6px}h2{font-size:16px;margin:22px 0 8px}
p{margin:6px 0;color:var(--mut);max-width:82ch}
.ctl{background:var(--card);border-radius:10px;padding:12px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:12px 18px;margin-top:14px}
.ctl label{display:block;font-size:12.5px;color:var(--mut);margin-bottom:4px;font-weight:600}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--grid);border-radius:7px;overflow:hidden}
.seg button{border:0;background:var(--bg);color:var(--fg);padding:5px 9px;font:inherit;font-size:13px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
.seg button:disabled{opacity:.35;cursor:not-allowed}
.rng{display:flex;align-items:center;gap:8px}.rng input[type=range]{flex:1}
.rng output,.rng input[type=number]{font-variant-numeric:tabular-nums;min-width:58px;font:inherit;font-size:13.5px}
.rng input[type=number]{width:90px;padding:3px 6px;border:1px solid var(--grid);border-radius:6px;background:var(--bg);color:var(--fg)}
.chk{display:flex;align-items:center;gap:6px;font-size:13.5px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:14px}
.tile{background:var(--card);border-radius:10px;padding:10px 12px}
.tile .k{font-size:12px;color:var(--mut)}.tile .v{font-size:22px;font-weight:650;font-variant-numeric:tabular-nums}
.tile .s{font-size:12px;color:var(--mut)}
.card{background:var(--card);border-radius:10px;padding:12px;margin-top:14px}
svg.ch{width:100%;height:auto;display:block;touch-action:none}
.cap{font-size:11.5px;fill:var(--mut)}
table{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}
th,td{padding:4px 6px;border-bottom:1px solid var(--grid);text-align:right;vertical-align:top}
th:first-child,td:first-child{text-align:left}th{color:var(--mut);font-weight:600}
td.pos{text-align:left;font-size:12.5px;line-height:1.55}
.up{color:var(--pos)}.dn{color:var(--neg)}
.tw{overflow-x:auto}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;margin:2px 0 6px}
.legend span{display:inline-flex;align-items:center;gap:6px}
#tip{position:fixed;pointer-events:none;background:var(--bg);color:var(--fg);border:1px solid var(--grid);padding:7px 9px;border-radius:7px;font-size:12px;display:none;box-shadow:0 3px 12px rgba(0,0,0,.18);z-index:9;font-variant-numeric:tabular-nums}
#tip td{padding:1px 5px;border:0}
.pill{display:inline-block;padding:0 6px;border-radius:5px;background:var(--bg);border:1px solid var(--grid);margin:1px 3px 1px 0;white-space:nowrap}
</style></head><body><main>
<h1>Portfolio per dag</h1>
<p>Dag voor dag doorgerekend over de blinde herbeoordeling (__N__ namen). Elke dag gaat het hele vermogen naar de namen van die dag die de selectie halen: gelijk of naar score verdeeld, met een maximum per aandeel. Wat over is blijft cash. Long bij een positieve score, short bij een negatieve. Het dagresultaat compoundeert in de volgende dag. Bruto: geen spread, commissie of leenkosten. US met strategie-exit en $200k omzetvloer, andere markten met het venster van hun resolver. Dit is het onderzoeksniveau, niet wat de broker werkelijk vulde.</p>
<div class="ctl">
 <div><label>Model</label><div class="seg" id="arm"></div></div>
 <div><label>Sleutel</label><div class="seg" id="key"><button data-v="impact">impact_sum</button><button data-v="pup">p_up − 50</button></div></div>
 <div><label>Markt</label><div class="seg" id="mkt"><button data-v="us">US</button><button data-v="europe">Europa</button><button data-v="apac">Japan + Australië</button><button data-v="all">Alles</button></div></div>
 <div><label>Selectie</label><div class="seg" id="sel"><button data-v="abs">Absolute drempel</button><button data-v="pct">Top % per dag</button></div></div>
 <div id="thrbox"><label for="thr">Drempel |score| ≥</label><div class="rng"><input type="range" id="thr"><output id="thro"></output></div></div>
 <div id="pctbox"><label for="pct">Top % van de namen van die dag</label><div class="rng"><input type="range" id="pct" min="5" max="100" step="5"><output id="pcto"></output></div></div>
 <div><label for="cap">Max % van het vermogen per aandeel</label><div class="rng"><input type="range" id="cap" min="5" max="100" step="5"><output id="capo"></output></div></div>
 <div><label>Weging</label><div class="seg" id="wt"><button data-v="eq">Gelijk</button><button data-v="score">Naar |score|</button></div></div>
 <div><label for="start">Startvermogen ($)</label><div class="rng"><input type="number" id="start" min="100" step="100"></div></div>
 <div><label>Steekproef</label><label class="chk" style="font-weight:400;color:var(--fg)"><input type="checkbox" id="clean"> zonder de 42 geanonimiseerde namen</label></div>
</div>
<div class="tiles" id="tiles"></div>
<div class="card">
 <div class="legend" id="legend"></div>
 <div id="chart"></div>
</div>
<h2>Alle modellen bij dezelfde instellingen</h2>
<div class="card tw" id="cmp"></div>
<h2>Per dag: <span id="dayarm"></span></h2>
<div class="card tw" id="days"></div>
<p style="margin-top:14px;font-size:13px">Gelijke weging: elke naam krijgt 1/N van het vermogen, maximaal het ingestelde percentage; bij weinig namen blijft dus cash over. Weging naar |score|: aandelen naar grootte van de score, waarbij een naam boven het maximum wordt afgetopt en het overschot over de rest wordt verdeeld zolang er ruimte is. Top % per dag rondt naar boven af en neemt alleen namen met een score ongelijk aan 0. Een short op een aandeel dat meer dan verdubbelt kan meer dan zijn inleg verliezen; dat wordt niet afgekapt. "Alles shorten": elke verhandelbare naam van die dag short, gelijk gewogen met hetzelfde maximum. Rijen op dezelfde datum uit verschillende markten vallen bij "Alles" in één boek.</p>
</main><div id="tip" role="status"></div>
<script>
const R=__DATA__;
// row: 0 region,1 day,2 ticker,3 move,4 tradable,5 dv$m,6 anon,7 live,8-11 impact opus5/opus/sonnet/fable,12-15 pup
const ARMS=[["live","Live hunt"],["opus5","Opus 5"],["opus","Opus 5.5"],["sonnet","Sonnet 5.5"],["fable","Fable 5.1"]];
const IDX={impact:{live:7,opus5:8,opus:9,sonnet:10,fable:11},pup:{opus5:12,opus:13,sonnet:14,fable:15}};
const col=a=>`var(--s${ARMS.findIndex(x=>x[0]==a)})`,LAB=Object.fromEntries(ARMS);
const st={arm:"live",key:"impact",mkt:"us",sel:"abs",thr:3,pct:30,cap:50,wt:"eq",start:10000,clean:true};
try{Object.assign(st,JSON.parse(localStorage.getItem("pf1")||"{}"))}catch(e){}
const save=()=>{try{localStorage.setItem("pf1",JSON.stringify(st))}catch(e){}};
const usd=x=>"$"+Math.round(x).toLocaleString("nl-NL");
const pc=(x,d=1)=>x==null||!isFinite(x)?"–":(x>0?"+":"")+x.toFixed(d).replace(".",",")+"%";
const inMkt=r=>st.mkt=="all"||(st.mkt=="apac"?(r[0]=="japan"||r[0]=="australia"):r[0]==st.mkt);
function weights(sc,cap){const n=sc.length;if(!n)return[];
 if(st.wt=="eq"){const w=Math.min(1/n,cap);return sc.map(()=>w)}
 let w=new Array(n).fill(0),free=sc.map((_,i)=>i),budget=1;
 for(let it=0;it<n&&free.length&&budget>1e-12;it++){const tot=free.reduce((s,i)=>s+Math.abs(sc[i]),0);if(tot<=0)break;
  let over=false;const nf=[];for(const i of free){const x=budget*Math.abs(sc[i])/tot;if(x>=cap-1e-12){w[i]=cap;over=true}else nf.push(i)}
  if(!over){for(const i of free)w[i]=budget*Math.abs(sc[i])/tot;break}
  budget=1-w.reduce((s,x)=>s+x,0);free=nf}
 return w}
function simulate(arm){const ix=IDX[st.key][arm];if(ix==null)return null;
 const rows=R.filter(r=>inMkt(r)&&(!st.clean||!r[6]));
 const days=[...new Set(rows.map(r=>r[1]))].sort();const cap=st.cap/100;
 let eq=st.start,peak=eq,mdd=0,eqS=st.start;const out=[];let trades=0,hits=0,tdays=0,wins=0,expo=0;
 for(const d of days){const dr=rows.filter(r=>r[1]==d);const cand=dr.filter(r=>r[4]&&r[ix]!=0);
  let pick;
  if(st.sel=="abs")pick=cand.filter(r=>Math.abs(r[ix])>=st.thr-1e-9);
  else{const k=Math.ceil(cand.length*st.pct/100);pick=cand.slice().sort((a,b)=>Math.abs(b[ix])-Math.abs(a[ix])).slice(0,k)}
  const w=weights(pick.map(r=>r[ix]),cap);
  const pos=pick.map((r,i)=>({t:r[2],m:r[0],side:r[ix]>0?1:-1,w:w[i],mv:r[3],sc:r[ix],dv:r[5]}));
  const ret=pos.reduce((s,p)=>s+p.w*p.side*p.mv/100,0);const gross=pos.reduce((s,p)=>s+p.w,0);
  const before=eq;eq=eq*(1+ret);peak=Math.max(peak,eq);mdd=Math.min(mdd,eq/peak-1);
  if(pos.length){tdays++;if(ret>0)wins++;expo+=gross;trades+=pos.length;hits+=pos.filter(p=>p.side*p.mv>0).length}
  const sh=dr.filter(r=>r[4]),ws=Math.min(1/Math.max(1,sh.length),cap),sret=sh.reduce((s,r)=>s-ws*r[3]/100,0);eqS*=1+sret;
  out.push({d,mk:[...new Set(dr.map(r=>r[0]))],n:dr.length,nc:cand.length,pos,ret,gross,before,eq,eqS})}
 return {days:out,eq,ret:eq/st.start-1,mdd,tdays,wins,trades,hits,expo:tdays?expo/tdays:0,eqS}}
function stats(s){const dr=s.days.filter(x=>x.pos.length).map(x=>x.ret);const m=dr.length?dr.reduce((a,b)=>a+b,0)/dr.length:null;
 const sd=dr.length>1?Math.sqrt(dr.reduce((a,b)=>a+(b-m)**2,0)/(dr.length-1)):null;return {m,sd,t:sd?m/(sd/Math.sqrt(dr.length)):null}}
function segs(){
 const a=document.getElementById("arm");a.innerHTML=ARMS.map(([k,l])=>`<button data-v="${k}" ${IDX[st.key][k]==null?"disabled title='geen p_up voor de live hunt'":""}>${l}</button>`).join("");
 for(const id of ["arm","key","mkt","sel","wt"])document.querySelectorAll(`#${id} button`).forEach(b=>{b.setAttribute("aria-pressed",b.dataset.v==st[id]);b.onclick=()=>{if(b.disabled)return;st[id]=b.dataset.v;
  if(id=="key"){if(st.key=="pup"&&st.arm=="live")st.arm="opus5";st.thr=st.key=="pup"?10:3}save();draw()}})}
function sliders(){const t=document.getElementById("thr");if(st.key=="pup"){t.min=0;t.max=35;t.step=1}else{t.min=0;t.max=8;t.step=.1}
 t.value=st.thr;document.getElementById("thro").textContent=st.key=="pup"?st.thr+" pt":(+st.thr).toFixed(1).replace(".",",");
 const p=document.getElementById("pct");p.value=st.pct;document.getElementById("pcto").textContent=st.pct+"%";
 const c=document.getElementById("cap");c.value=st.cap;document.getElementById("capo").textContent=st.cap+"%";
 document.getElementById("start").value=st.start;document.getElementById("clean").checked=st.clean;
 document.getElementById("thrbox").style.display=st.sel=="abs"?"":"none";document.getElementById("pctbox").style.display=st.sel=="pct"?"":"none"}
function draw(){segs();sliders();
 const sims={};ARMS.forEach(([a])=>{const s=simulate(a);if(s)sims[a]=s});const S=sims[st.arm];
 if(!S||!S.days.length){document.getElementById("chart").innerHTML="<p>Geen dagen in deze selectie.</p>";return}
 const z=stats(S);
 document.getElementById("tiles").innerHTML=[
  ["Eindvermogen",usd(S.eq),`start ${usd(st.start)}`],["Totaal rendement",`<span class="${S.ret>=0?"up":"dn"}">${pc(100*S.ret)}</span>`,`alles shorten ${pc(100*(S.eqS/st.start-1))}`],
  ["Max drawdown",pc(100*S.mdd),"van piek tot dal"],["Dagen gehandeld",`${S.tdays} / ${S.days.length}`,`${S.wins} winstdagen`],
  ["Trades",S.trades,S.trades?`${Math.round(100*S.hits/S.trades)}% goed teken`:""],["Gem. per handelsdag",pc(100*(z.m??NaN),2),z.t!=null?`t ${z.t.toFixed(2).replace(".",",")}`:""],
  ["Gem. belegd",pc(100*S.expo,0).replace("+",""),"van het vermogen, op handelsdagen"]
 ].map(([k,v,s])=>`<div class="tile"><div class="k">${k}</div><div class="v">${v}</div><div class="s">${s}</div></div>`).join("");
 // chart
 const W=1100,H=380,L=70,Rr=96,T=14,B=46,days=S.days,nD=days.length;
 const X=i=>L+(W-L-Rr)*i/nD;   // 0 = start, i = end of day i
 const vals=[st.start];Object.values(sims).forEach(s=>s.days.forEach(d=>vals.push(d.eq)));days.forEach(d=>vals.push(d.eqS));
 let lo=Math.min(...vals),hi=Math.max(...vals);const span=hi-lo||1;lo-=span*.06;hi+=span*.06;
 const raw=(hi-lo)/6,mag=10**Math.floor(Math.log10(raw)),step=[1,2,2.5,5,10].map(x=>x*mag).find(x=>x>=raw);
 lo=Math.floor(lo/step)*step;hi=Math.ceil(hi/step)*step;const Y=v=>T+(H-T-B)*(hi-v)/(hi-lo);
 let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" role="img" aria-label="Vermogen per dag per model">`;
 for(let v=lo;v<=hi+1e-6;v+=step)s+=`<line x1="${L}" x2="${W-Rr}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--grid)"/><text class="cap" x="${L-6}" y="${Y(v)+4}" text-anchor="end">${usd(v)}</text>`;
 s+=`<line x1="${L}" x2="${W-Rr}" y1="${Y(st.start)}" y2="${Y(st.start)}" stroke="var(--zero)"/>`;
 const every=Math.max(1,Math.ceil(nD/12));s+=`<text class="cap" x="${X(0)}" y="${H-B+16}" text-anchor="middle">start</text>`;days.forEach((d,i)=>{if((i+1)%every==0||i==nD-1)s+=`<text class="cap" x="${X(i+1)}" y="${H-B+16}" text-anchor="middle">${d.d.slice(5)}</text>`});
 s+=`<text class="cap" x="${(L+W-Rr)/2}" y="${H-6}" text-anchor="middle">handelsdag (maand-dag), ${nD} dagen</text>`;
 const lbl=[];
 const line=(pts,c,wd,dash,op)=>`<path d="M${[st.start,...pts].map((v,i)=>X(i)+","+Y(v)).join("L")}" fill="none" stroke="${c}" stroke-width="${wd}" ${dash?`stroke-dasharray="${dash}"`:""} stroke-opacity="${op}" stroke-linejoin="round"/>`;
 s+=line(days.map(d=>d.eqS),"var(--ref)",1.6,"4 4",1);lbl.push({t:"alles shorten",y:Y(days[nD-1].eqS),c:"var(--mut)"});
 for(const [a,l] of ARMS){const sm=sims[a];if(!sm)continue;const sel=a==st.arm;s+=line(sm.days.map(d=>d.eq),col(a),sel?3:1.6,null,sel?1:.6);
  if(sel)sm.days.forEach((d,i)=>{if(d.pos.length)s+=`<circle cx="${X(i+1)}" cy="${Y(d.eq)}" r="3" fill="${col(a)}" stroke="var(--card)" stroke-width="1.5"/>`});
  lbl.push({t:l,y:Y(sm.eq),c:"var(--fg)",b:sel})}
 lbl.sort((p,q)=>p.y-q.y);for(let i=1;i<lbl.length;i++)if(lbl[i].y-lbl[i-1].y<13)lbl[i].y=lbl[i-1].y+13;
 lbl.forEach(l=>s+=`<text x="${W-Rr+6}" y="${l.y+4}" font-size="12" fill="${l.c}" font-weight="${l.b?700:500}">${l.t}</text>`);
 s+=`<line id="xh" x1="0" x2="0" y1="${T}" y2="${H-B}" stroke="var(--fg)" stroke-opacity=".35" visibility="hidden"/><rect id="hit" x="${L}" y="${T}" width="${W-L-Rr}" height="${H-T-B}" fill="transparent"/></svg>`;
 document.getElementById("chart").innerHTML=s;
 document.getElementById("legend").innerHTML=ARMS.filter(([a])=>sims[a]).map(([a,l])=>`<span><svg width="18" height="8"><line x1="0" x2="18" y1="4" y2="4" stroke="${col(a)}" stroke-width="${a==st.arm?3:1.6}"/></svg>${l}${a==st.arm?" (gekozen)":""}</span>`).join("")+`<span><svg width="18" height="8"><line x1="0" x2="18" y1="4" y2="4" stroke="var(--ref)" stroke-width="1.6" stroke-dasharray="4 4"/></svg>alles shorten</span>`;
 const svg=document.querySelector("#chart svg"),xh=svg.querySelector("#xh"),tip=document.getElementById("tip");
 svg.querySelector("#hit").addEventListener("pointermove",ev=>{const pt=svg.createSVGPoint();pt.x=ev.clientX;pt.y=ev.clientY;const p=pt.matrixTransform(svg.getScreenCTM().inverse());
  const i=Math.max(0,Math.min(nD-1,Math.round((p.x-L)/(W-L-Rr)*nD)-1));xh.setAttribute("x1",X(i+1));xh.setAttribute("x2",X(i+1));xh.setAttribute("visibility","visible");
  const d=days[i];const rows=ARMS.filter(([a])=>sims[a]).map(([a,l])=>{const q=sims[a].days[i];return `<tr><td><span style="color:${col(a)}">●</span> ${l}</td><td>${usd(q.eq)}</td><td class="${q.ret>=0?"up":"dn"}">${q.pos.length?pc(100*q.ret,2):"cash"}</td><td>${q.pos.length} pos.</td></tr>`}).join("");
  tip.innerHTML=`<b>${d.d}</b> · ${d.mk.join(", ")} · ${d.n} namen<table>${rows}<tr><td>alles shorten</td><td>${usd(d.eqS)}</td><td></td><td></td></tr></table>`;
  tip.style.display="block";const tw=tip.offsetWidth;tip.style.left=Math.min(ev.clientX+14,innerWidth-tw-8)+"px";tip.style.top=(ev.clientY+14)+"px"});
 svg.querySelector("#hit").addEventListener("pointerleave",()=>{tip.style.display="none";xh.setAttribute("visibility","hidden")});
 // comparison
 document.getElementById("cmp").innerHTML=`<table><tr><th>model</th><th>eindvermogen</th><th>rendement</th><th>max drawdown</th><th>handelsdagen</th><th>winstdagen</th><th>trades</th><th>goed teken</th><th>gem./handelsdag</th><th>t</th></tr>`+
  ARMS.filter(([a])=>sims[a]).map(([a,l])=>{const q=sims[a],zz=stats(q);return `<tr${a==st.arm?' style="font-weight:650"':""}><td><span style="color:${col(a)}">●</span> ${l}</td><td>${usd(q.eq)}</td><td class="${q.ret>=0?"up":"dn"}">${pc(100*q.ret)}</td><td>${pc(100*q.mdd)}</td><td>${q.tdays}</td><td>${q.wins}</td><td>${q.trades}</td><td>${q.trades?Math.round(100*q.hits/q.trades)+"%":"–"}</td><td>${pc(100*(zz.m??NaN),2)}</td><td>${zz.t!=null?zz.t.toFixed(2).replace(".",","):"–"}</td></tr>`}).join("")+
  `<tr><td>alles shorten</td><td>${usd(S.eqS)}</td><td>${pc(100*(S.eqS/st.start-1))}</td><td colspan="7"></td></tr></table>`;
 // days
 document.getElementById("dayarm").textContent=LAB[st.arm];
 document.getElementById("days").innerHTML=`<table><tr><th>dag</th><th>markt</th><th>namen</th><th>posities (zijde, gewicht, koers)</th><th>belegd</th><th>dagrendement</th><th>vermogen</th></tr>`+
  days.map(d=>`<tr><td>${d.d}</td><td style="text-align:left">${d.mk.join(", ")}</td><td>${d.nc}/${d.n}</td><td class="pos">${d.pos.length?d.pos.map(p=>`<span class="pill" title="score ${p.sc}, omzet $${p.dv}m">${p.t} ${p.side>0?"L":"S"} ${Math.round(100*p.w)}% <span class="${p.side*p.mv>=0?"up":"dn"}">${pc(p.mv)}</span></span>`).join(""):"<span style='color:var(--mut)'>cash</span>"}</td><td>${d.pos.length?Math.round(100*d.gross)+"%":"0%"}</td><td class="${d.ret>=0?"up":"dn"}">${d.pos.length?pc(100*d.ret,2):"–"}</td><td>${usd(d.eq)}</td></tr>`).join("")+"</table>";
}
document.getElementById("thr").oninput=e=>{st.thr=+e.target.value;save();draw()};
document.getElementById("pct").oninput=e=>{st.pct=+e.target.value;save();draw()};
document.getElementById("cap").oninput=e=>{st.cap=+e.target.value;save();draw()};
document.getElementById("start").onchange=e=>{st.start=Math.max(100,+e.target.value||10000);save();draw()};
document.getElementById("clean").onchange=e=>{st.clean=e.target.checked;save();draw()};
draw();
</script></body></html>'''
open(f'{D}/portfolio.html', 'w').write(HTML.replace('__DATA__', json.dumps(rows)).replace('__N__', str(len(rows))))
print('wrote portfolio.html with', len(rows), 'names')
