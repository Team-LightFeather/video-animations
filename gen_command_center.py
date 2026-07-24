#!/usr/bin/env python3
"""Build the INK BLOCKS COMMAND CENTER page: the LF-Blocks version (one-color
pixels, L/F letterforms as the detail) at 44 cols, with a dedicated grouped
control rail. Standalone sibling of the gallery — same clips, same engine."""
import json
import pathlib

import render_core as rc

OUT = pathlib.Path(__file__).parent / "ink-blocks-command-center.html"

# The version this page exists for: Ink Blocks at 44 cols — solid blocks for
# the body, L/F letterforms at the silhouette edge and finest details.
# (Lines fill remains available as an option.)
BASE = {
    "cols": 44, "ramp": "PIXLF", "dir": "ink", "gamma": 1.5, "floor": 0.0,
    "minOp": 0.40, "bright": 1.15, "color": "mono", "scan": 0.0, "edge": 0.0,
    "gScale": 1.16, "weight": 700, "stab": 0.0, "smooth": 0.0, "bands": 0,
    "blur": 0, "lfThr": 0.75, "pixFill": 0.82, "lfEdge": 1, "lfFill": "blocks",
}

HTML = r"""<title>Ink Blocks 44 — Command Center</title>
<style>
__FONTS__
*{box-sizing:border-box;}
body{margin:0;background:#0D3E3D;font-family:'Space Grotesk',monospace;color:#EAF6F0;
  min-height:100vh;display:flex;flex-direction:column;}
body[data-mode="white"]{background:#FFFBF8;color:#0D3E3D;}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:14px clamp(14px,2.5vw,30px) 8px;flex-wrap:wrap;}
h1{font-size:clamp(15px,2vw,20px);font-weight:700;margin:0;letter-spacing:-.01em;}
h1 .dot{display:inline-block;width:10px;height:10px;background:#00FFA8;
  box-shadow:0 0 12px #00FFA8;margin-right:9px;}
body[data-mode="white"] h1 .dot{background:#2FC189;box-shadow:none;}
h1 small{font-weight:400;font-size:.72em;opacity:.65;margin-left:10px;letter-spacing:.02em;}
.toggle{display:flex;border:1px solid rgba(255,255,255,.28);border-radius:999px;overflow:hidden;
  font-size:12px;font-weight:600;}
body[data-mode="white"] .toggle{border-color:rgba(13,62,61,.3);}
.toggle button{appearance:none;border:0;background:transparent;color:inherit;
  padding:6px 14px;cursor:pointer;font:inherit;}
.toggle button[aria-pressed="true"]{background:#00FFA8;color:#04211c;}
body[data-mode="white"] .toggle button[aria-pressed="true"]{background:#2FC189;color:#fff;}
main{flex:1;display:flex;gap:16px;padding:0 clamp(14px,2.5vw,30px) 16px;align-items:stretch;min-height:0;}
#stageWrap{flex:1;display:flex;align-items:center;justify-content:center;min-width:0;}
#mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);
  gap:clamp(6px,0.8vw,10px);width:100%;max-width:calc((100vh - 150px)*432/454);
  aspect-ratio:calc(3*432)/calc(3*454);max-height:calc(100vh - 150px);}
.ptile{position:relative;overflow:hidden;border-radius:9px;cursor:pointer;}
.ptile canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}
.ptile.sel{outline:2px solid #00FFA8;outline-offset:2px;}
body[data-mode="white"] .ptile.sel{outline-color:#2FC189;}
.ptile .tag{position:absolute;left:6px;top:6px;font-size:10px;font-weight:600;letter-spacing:.05em;
  background:rgba(0,0,0,.45);color:#B9F5DD;padding:2px 7px;border-radius:999px;opacity:0;transition:opacity .15s;}
.ptile:hover .tag,.ptile.sel .tag{opacity:1;}
.ptile.tweaked .tag{opacity:1;background:rgba(0,255,168,.25);}
#panel{width:300px;flex:none;overflow-y:auto;padding:2px 2px 10px;
  display:flex;flex-direction:column;gap:10px;font-size:12px;}
#scope{font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:8px;min-height:26px;}
#scope .back{appearance:none;border:1px solid rgba(255,255,255,.25);background:transparent;color:inherit;
  border-radius:999px;font:inherit;font-size:11px;padding:3px 9px;cursor:pointer;display:none;}
body[data-mode="white"] #scope .back{border-color:rgba(13,62,61,.3);}
#hint{font-size:10.5px;color:#8FB9AB;margin-top:-6px;}
body[data-mode="white"] #hint{color:#4E6E67;}
.sec{display:flex;flex-direction:column;gap:8px;border:1px solid rgba(255,255,255,.13);
  border-radius:10px;padding:9px 10px 11px;}
body[data-mode="white"] .sec{border-color:rgba(13,62,61,.16);}
.sec .st{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:#8FB9AB;}
body[data-mode="white"] .sec .st{color:#4E6E67;}
.knob{display:flex;flex-direction:column;gap:2px;}
.knob .row{display:flex;justify-content:space-between;align-items:baseline;}
.knob label{font-weight:600;}
.knob .val{font-size:11px;color:#9CC8B9;font-variant-numeric:tabular-nums;}
body[data-mode="white"] .knob .val{color:#41645D;}
.knob input[type=range]{width:100%;accent-color:#00FFA8;margin:0;}
body[data-mode="white"] .knob input[type=range]{accent-color:#2FC189;}
.knob.hero .val{font-size:19px;font-weight:700;color:#00FFA8;}
body[data-mode="white"] .knob.hero .val{color:#1E9E6E;}
.knob.hero .val small{font-size:11px;font-weight:600;opacity:.75;margin-left:3px;}
.seg{display:flex;flex-direction:column;gap:3px;}
.seg label{font-weight:600;}
.seg .btns{display:flex;gap:5px;}
.seg button{flex:1;appearance:none;border:1px solid rgba(255,255,255,.22);border-radius:7px;
  background:transparent;color:inherit;font:inherit;font-size:11px;font-weight:600;padding:5px 0;cursor:pointer;}
body[data-mode="white"] .seg button{border-color:rgba(13,62,61,.28);}
.seg button[aria-pressed="true"]{background:#00FFA8;color:#04211c;border-color:transparent;}
body[data-mode="white"] .seg button[aria-pressed="true"]{background:#2FC189;color:#fff;}
.acts{display:flex;flex-wrap:wrap;gap:5px;margin-top:2px;}
.acts button{appearance:none;border:1px solid rgba(255,255,255,.25);border-radius:7px;background:transparent;
  color:inherit;font:inherit;font-size:11px;font-weight:600;padding:6px 9px;cursor:pointer;}
body[data-mode="white"] .acts button{border-color:rgba(13,62,61,.3);}
#json{font-size:9.5px;line-height:1.45;color:#8FB9AB;background:rgba(0,0,0,.18);border-radius:7px;
  padding:7px 8px;white-space:pre-wrap;word-break:break-all;max-height:110px;overflow-y:auto;user-select:all;}
body[data-mode="white"] #json{color:#40615A;background:rgba(13,62,61,.07);}
footer{padding:0 clamp(14px,2.5vw,30px) 12px;font-size:10.5px;letter-spacing:.04em;color:rgba(185,217,207,.5);}
body[data-mode="white"] footer{color:rgba(13,62,61,.45);}
@media (max-width:860px){ main{flex-direction:column;} #panel{width:100%;} #mosaic{max-width:none;max-height:none;} }
</style>

<header>
  <h1><span class="dot"></span>Ink Blocks &middot; Command Center<small>one-color blocks &middot; L/F letterform detail</small></h1>
  <div class="toggle" role="group" aria-label="Color mode">
    <button id="mGreen" aria-pressed="true">Green</button>
    <button id="mWhite" aria-pressed="false">White</button>
  </div>
</header>
<main>
  <div id="stageWrap"><div id="mosaic"></div></div>
  <aside id="panel">
    <div id="scope"><span id="scopeLbl">Tuning: all videos</span><button class="back" id="backAll">&larr; all</button></div>
    <div id="hint">Click a video to tune it on its own; its tweaks sit on top of the global settings.</div>
    <div id="groups"></div>
    <div class="acts">
      <button id="resetBase">Reset to base</button>
      <button id="resetVid" style="display:none">Reset this video</button>
      <button id="clearTweaks">Clear video tweaks</button>
      <button id="copyBtn">Copy settings</button>
    </div>
    <div id="json"></div>
  </aside>
</main>
<footer>drag Pixel size for bigger/smaller blocks &middot; Fill style = blocks or lines &middot; L/F detail = how much becomes letters &middot; G/W mode &middot; click a tile = per-video tuning &middot; auto-saves in this browser</footer>

<script>
const BASE = __BASE__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
__CORE__
const PALS = {
  green: {bright:"255,255,255", dim:"148,224,196"},
  white: {bright:"13,62,61", dim:"96,132,127"},
};
const FIELDS = Object.keys(BASE);
const GROUPS = [
  {title:"Pixel grid", knobs:[
    {f:"cols",    label:"Pixel size",   min:24, max:96, step:2, rtl:true, hero:true, fmt:v=>Math.round(v)+"<small>cols</small>"},
    {f:"pixFill", label:"Pixel fill",   min:0.4, max:1, step:0.02, fmt:v=>Math.round(v*100)+"%"},
  ]},
  {title:"Letter detail", knobs:[
    {f:"lfThr",  label:"L/F detail",     min:0.15, max:0.9, step:0.05, rtl:true, fmt:v=>Math.round((1-v)*100)+"%"},
    {f:"gScale", label:"Letter size",    min:0.9, max:1.5, step:0.02, fmt:v=>v.toFixed(2)},
    {f:"weight", label:"Letter weight",  min:400, max:700, step:50, fmt:v=>""+Math.round(v)},
    {f:"edge",   label:"Contour boost",  min:0, max:1, step:0.05, fmt:v=>v?v.toFixed(2):"off"},
  ]},
  {title:"Tone", knobs:[
    {f:"gamma",  label:"Contrast",    min:0.4, max:8, step:0.05, fmt:v=>v.toFixed(2)},
    {f:"bright", label:"Brightness",  min:0.5, max:1.6, step:0.05, fmt:v=>v.toFixed(2)},
    {f:"floor",  label:"Fill",        min:0, max:0.5, step:0.01, fmt:v=>v.toFixed(2)},
    {f:"minOp",  label:"Min opacity", min:0.1, max:0.95, step:0.05, fmt:v=>v.toFixed(2)},
  ]},
  {title:"Motion", knobs:[
    {f:"smooth", label:"Smoothing",  min:0, max:0.95, step:0.05, fmt:v=>v?v.toFixed(2):"off"},
    {f:"stab",   label:"Stability",  min:0, max:0.15, step:0.01, fmt:v=>v?v.toFixed(2):"live"},
  ]},
];
let mode="green", sel=null;
let G = Object.assign({}, BASE);
let O = {};
window.__PAL = PALS[mode];
function eff(i){ return O[i] ? Object.assign({}, G, O[i]) : G; }

const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion:reduce)").matches;
const mosaic = document.getElementById("mosaic");
const tiles = [];
CLIPS.forEach((clip,i)=>{
  const el = document.createElement("div"); el.className = "ptile";
  const tag = document.createElement("span"); tag.className="tag"; tag.textContent = (i+1)+" · "+STEMS[i];
  const v = document.createElement("video");
  v.muted = true; v.loop = true; v.autoplay = true; v.playsInline = true;
  v.setAttribute("muted",""); v.setAttribute("playsinline","");
  const c = document.createElement("canvas"); el.appendChild(c); el.appendChild(tag);
  const t = initTile(clip, c, v);
  t.el = el;
  v.addEventListener("loadeddata", ()=>{
    if(reduce){ sizeTile(t); renderTile(t, eff(i)); try{v.pause();}catch(e){} }
    else { v.play().catch(()=>{}); sizeTile(t); }
  });
  v.src = clip.src; v.load();
  el.addEventListener("click", ev=>{ ev.stopPropagation(); select(sel===i?null:i); });
  tiles.push(t); mosaic.appendChild(el);
});
function redraw(only){ tiles.forEach((t,i)=>{ if(only==null||only===i) renderTile(t, eff(i)); }); }
let last=0;
function loop(ts){ if(ts-last>85){ last=ts; redraw(); } requestAnimationFrame(loop); }
if(!reduce) requestAnimationFrame(loop);
addEventListener("resize", ()=>tiles.forEach(sizeTile));
addEventListener("click", ()=>tiles.forEach(t=>{ if(t.src.paused && !reduce) t.src.play().catch(()=>{}); }));

// ---- command rail ----
const groupsEl = document.getElementById("groups"), inputs = {};
groupsEl.style.display="flex"; groupsEl.style.flexDirection="column"; groupsEl.style.gap="10px";
const segUpdaters = [];
function segEl(label, opts, field, getVal){
  const wrap = document.createElement("div"); wrap.className="seg";
  const lb = document.createElement("label"); lb.textContent=label;
  const btns = document.createElement("div"); btns.className="btns";
  opts.forEach(o=>{
    const b = document.createElement("button");
    b.textContent = o.label;
    b.addEventListener("click", ()=>{ setField(field, o.value); refreshPanel(); });
    b.dataset.v = typeof o.value==="string"?o.value:JSON.stringify(o.value);
    btns.appendChild(b);
  });
  wrap.appendChild(lb); wrap.appendChild(btns);
  segUpdaters.push(()=>{ const cur=getVal();
    [...btns.children].forEach(b=>b.setAttribute("aria-pressed", b.dataset.v===cur)); });
  return wrap;
}
GROUPS.forEach(g=>{
  const sec = document.createElement("div"); sec.className="sec";
  const st = document.createElement("div"); st.className="st"; st.textContent=g.title;
  sec.appendChild(st);
  g.knobs.forEach(k=>{
    const w = document.createElement("div"); w.className="knob"+(k.hero?" hero":"");
    const row = document.createElement("div"); row.className="row";
    const lb = document.createElement("label"); lb.textContent = k.label;
    const val = document.createElement("span"); val.className="val";
    row.appendChild(lb); row.appendChild(val);
    const inp = document.createElement("input");
    inp.type="range"; inp.min=k.min; inp.max=k.max; inp.step=k.step;
    if(k.rtl) inp.style.direction="rtl";
    inp.addEventListener("input", ()=>{ setField(k.f, parseFloat(inp.value)); val.innerHTML = k.fmt(parseFloat(inp.value)); });
    w.appendChild(row); w.appendChild(inp);
    sec.appendChild(w);
    inputs[k.f] = {inp, val, fmt:k.fmt};
  });
  if(g.title==="Pixel grid"){
    sec.appendChild(segEl("Fill style", [{label:"Lines",value:"lines"},{label:"Blocks",value:"blocks"}], "lfFill", ()=>effSel().lfFill||"lines"));
  }
  if(g.title==="Letter detail"){
    sec.appendChild(segEl("L/F at silhouette edges", [{label:"On",value:1},{label:"Off",value:0}], "lfEdge", ()=>String(effSel().lfEdge==null?0:effSel().lfEdge)));
  }
  if(g.title==="Motion"){
    sec.appendChild(segEl("Noise blur", [{label:"Off",value:0},{label:"On",value:1}], "blur", ()=>String(effSel().blur||0)));
  }
  groupsEl.appendChild(sec);
});
function effSel(){ return sel==null ? G : eff(sel); }
function setField(f, v){
  if(sel==null){ G[f]=v; tiles.forEach(resetTone); redraw(); }
  else { (O[sel] = O[sel]||{})[f]=v; resetTone(tiles[sel]); redraw(sel); markTweaks(); }
  save(); updateJson();
}
function refreshPanel(){
  const s = effSel();
  Object.keys(inputs).forEach(f=>{ inputs[f].inp.value = s[f]; inputs[f].val.innerHTML = inputs[f].fmt(s[f]); });
  segUpdaters.forEach(u=>u());
  document.getElementById("scopeLbl").textContent = sel==null ? "Tuning: all videos" : "Tuning: "+(sel+1)+" · "+STEMS[sel];
  document.getElementById("backAll").style.display = sel==null ? "none" : "";
  document.getElementById("resetVid").style.display = sel==null ? "none" : "";
  updateJson();
}
function select(i){
  sel = i;
  tiles.forEach((t,j)=>t.el.classList.toggle("sel", j===sel));
  refreshPanel();
}
function markTweaks(){ tiles.forEach((t,i)=>t.el.classList.toggle("tweaked", !!O[i] && Object.keys(O[i]).length>0)); }
function updateJson(){
  const pv={}; Object.keys(O).forEach(i=>{ if(Object.keys(O[i]).length) pv[STEMS[i]]=O[i]; });
  document.getElementById("json").textContent = JSON.stringify({global:G, perVideo:pv});
}
document.getElementById("backAll").addEventListener("click", ()=>select(null));
document.getElementById("resetBase").addEventListener("click", ()=>{
  G = Object.assign({}, BASE); tiles.forEach(resetTone); redraw(); refreshPanel(); save();
});
document.getElementById("resetVid").addEventListener("click", ()=>{
  if(sel!=null){ delete O[sel]; resetTone(tiles[sel]); redraw(sel); markTweaks(); refreshPanel(); save(); }
});
document.getElementById("clearTweaks").addEventListener("click", ()=>{
  O={}; tiles.forEach(resetTone); redraw(); markTweaks(); refreshPanel(); save();
});
document.getElementById("copyBtn").addEventListener("click", ()=>{
  const txt = document.getElementById("json").textContent;
  if(navigator.clipboard) navigator.clipboard.writeText(txt).then(()=>{
    const b=document.getElementById("copyBtn"); b.textContent="Copied ✓";
    setTimeout(()=>b.textContent="Copy settings", 1200);
  }).catch(()=>{});
});

// ---- mode ----
const bG = document.getElementById("mGreen"), bW = document.getElementById("mWhite");
function setMode(m){
  mode = m; window.__PAL = PALS[m];
  document.body.dataset.mode = m==="white" ? "white" : "green";
  bG.setAttribute("aria-pressed", m==="green");
  bW.setAttribute("aria-pressed", m==="white");
  redraw();
}
bG.addEventListener("click", ()=>setMode("green"));
bW.addEventListener("click", ()=>setMode("white"));
addEventListener("keydown", e=>{
  if(e.target && e.target.tagName==="INPUT") return;
  if(e.key==="Escape") select(null);
  else if(e.key==="g"||e.key==="G") setMode("green");
  else if(e.key==="w"||e.key==="W") setMode("white");
});

// ---- persistence ----
function save(){ try{ localStorage.setItem("lfInkBlocksCC2", JSON.stringify({G,O})); }catch(e){} }
(function restore(){
  try{
    const st = JSON.parse(localStorage.getItem("lfInkBlocksCC2")||"null");
    if(st && st.G){ G = Object.assign({}, BASE, st.G); O = st.O||{}; }
  }catch(e){}
})();
markTweaks(); refreshPanel();
</script>
"""

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__BASE__", json.dumps(BASE))
        .replace("__STEMS__", json.dumps(rc.STEMS))
        .replace("__CLIPS__", rc.build_clips("video"))
        .replace("__CORE__", rc.JS_CORE))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
