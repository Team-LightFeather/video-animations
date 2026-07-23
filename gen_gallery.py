#!/usr/bin/env python3
"""Build the people-ascii GALLERY + TUNER page: 9 embedded clips rendered live,
10 style presets, full knob panel — global AND per-video (click a tile)."""
import json
import pathlib

import render_core as rc

OUT = pathlib.Path(__file__).parent / "people-ascii-gallery.html"

HTML = r"""<title>People-ASCII — Version 3 variations</title>
<style>
__FONTS__
*{box-sizing:border-box;}
body{margin:0;background:#0D3E3D;font-family:'Space Grotesk',monospace;color:#EAF6F0;
  min-height:100vh;display:flex;flex-direction:column;}
body[data-mode="white"]{background:#F1ECE0;color:#0D3E3D;}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:14px clamp(14px,2.5vw,30px) 8px;flex-wrap:wrap;}
h1{font-size:clamp(15px,2vw,20px);font-weight:700;margin:0;letter-spacing:-.01em;}
h1 .dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#00FFA8;
  box-shadow:0 0 12px #00FFA8;margin-right:9px;}
body[data-mode="white"] h1 .dot{background:#2FC189;box-shadow:none;}
.toggle{display:flex;border:1px solid rgba(255,255,255,.28);border-radius:999px;overflow:hidden;
  font-size:12px;font-weight:600;}
body[data-mode="white"] .toggle{border-color:rgba(13,62,61,.3);}
.toggle button{appearance:none;border:0;background:transparent;color:inherit;
  padding:6px 14px;cursor:pointer;font:inherit;}
.toggle button[aria-pressed="true"]{background:#00FFA8;color:#04211c;}
body[data-mode="white"] .toggle button[aria-pressed="true"]{background:#2FC189;color:#fff;}
nav{display:flex;gap:6px;flex-wrap:wrap;padding:0 clamp(14px,2.5vw,30px) 8px;}
nav button{appearance:none;border:1px solid rgba(255,255,255,.22);border-radius:999px;
  background:transparent;color:inherit;font:inherit;font-size:12px;font-weight:600;
  padding:6px 12px;cursor:pointer;}
body[data-mode="white"] nav button{border-color:rgba(13,62,61,.28);}
nav button[aria-pressed="true"]{background:#00FFA8;color:#04211c;border-color:transparent;}
body[data-mode="white"] nav button[aria-pressed="true"]{background:#2FC189;color:#fff;}
main{flex:1;display:flex;gap:16px;padding:0 clamp(14px,2.5vw,30px) 16px;align-items:stretch;min-height:0;}
#stageWrap{flex:1;display:flex;align-items:center;justify-content:center;min-width:0;}
#mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);
  gap:clamp(6px,0.8vw,10px);width:100%;max-width:calc((100vh - 170px)*432/454);
  aspect-ratio:calc(3*432)/calc(3*454);max-height:calc(100vh - 170px);}
.ptile{position:relative;overflow:hidden;border-radius:9px;cursor:pointer;}
.ptile canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}
.ptile.sel{outline:2px solid #00FFA8;outline-offset:2px;}
body[data-mode="white"] .ptile.sel{outline-color:#2FC189;}
.ptile .tag{position:absolute;left:6px;top:6px;font-size:10px;font-weight:600;letter-spacing:.05em;
  background:rgba(0,0,0,.45);color:#B9F5DD;padding:2px 7px;border-radius:999px;opacity:0;transition:opacity .15s;}
.ptile:hover .tag,.ptile.sel .tag{opacity:1;}
.ptile.tweaked .tag{opacity:1;background:rgba(0,255,168,.25);}
#panel{width:280px;flex:none;overflow-y:auto;padding:2px 2px 10px;
  display:flex;flex-direction:column;gap:9px;font-size:12px;}
#scope{font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:8px;min-height:26px;}
#scope .back{appearance:none;border:1px solid rgba(255,255,255,.25);background:transparent;color:inherit;
  border-radius:999px;font:inherit;font-size:11px;padding:3px 9px;cursor:pointer;display:none;}
body[data-mode="white"] #scope .back{border-color:rgba(13,62,61,.3);}
#hint{font-size:10.5px;color:#8FB9AB;margin-top:-5px;}
body[data-mode="white"] #hint{color:#4E6E67;}
.knob{display:flex;flex-direction:column;gap:2px;}
.knob .row{display:flex;justify-content:space-between;align-items:baseline;}
.knob label{font-weight:600;}
.knob .val{font-size:11px;color:#9CC8B9;font-variant-numeric:tabular-nums;}
body[data-mode="white"] .knob .val{color:#41645D;}
.knob input[type=range]{width:100%;accent-color:#00FFA8;margin:0;}
body[data-mode="white"] .knob input[type=range]{accent-color:#2FC189;}
.seg{display:flex;flex-direction:column;gap:3px;}
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
  padding:7px 8px;white-space:pre-wrap;word-break:break-all;max-height:130px;overflow-y:auto;user-select:all;}
body[data-mode="white"] #json{color:#40615A;background:rgba(13,62,61,.07);}
footer{padding:0 clamp(14px,2.5vw,30px) 12px;font-size:10.5px;letter-spacing:.04em;color:rgba(185,217,207,.5);}
body[data-mode="white"] footer{color:rgba(13,62,61,.45);}
@media (max-width:860px){ main{flex-direction:column;} #panel{width:100%;} #mosaic{max-width:none;max-height:none;} }
</style>

<header>
  <h1><span class="dot"></span>People-ASCII &middot; version 3 family</h1>
  <div class="toggle" role="group" aria-label="Color mode">
    <button id="mGreen" aria-pressed="true">Green</button>
    <button id="mWhite" aria-pressed="false">White</button>
  </div>
</header>
<nav id="nav" aria-label="Preset"></nav>
<main>
  <div id="stageWrap"><div id="mosaic"></div></div>
  <div id="panel">
    <div id="scope"><span id="scopeLbl">Tuning: all videos</span><button class="back" id="backAll">&larr; all</button></div>
    <div id="hint">Click a video to tune it on its own; its tweaks sit on top of the global settings.</div>
    <div id="knobs"></div>
    <div class="seg"><label>Glyph set</label><div class="btns" id="segRamp"></div></div>
    <div class="seg"><label>Basis</label><div class="btns" id="segDir"></div></div>
    <div class="seg"><label>Color</label><div class="btns" id="segColor"></div></div>
    <div class="seg"><label>Noise blur</label><div class="btns" id="segBlur"></div></div>
    <div class="acts">
      <button id="resetVid" style="display:none">Reset this video</button>
      <button id="clearTweaks">Clear all video tweaks</button>
      <button id="copyBtn">Copy settings</button>
    </div>
    <div id="json"></div>
  </div>
</main>
<footer>keys 1&ndash;0 presets &middot; G/W mode &middot; click a tile = per-video tuning &middot; settings auto-save in this browser</footer>

<script>
const VARIANTS = __VARIANTS__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
__CORE__
const PALS = {
  green: {bright:"255,255,255", dim:"148,224,196"},
  white: {bright:"13,62,61", dim:"96,132,127"},
};
const RAMPS = {fine:" .·:-=+i1lvtfcLF#", blocky:" .:-=+*%#@", brand:" .:=iltLF#"};
const FIELDS = ["cols","ramp","dir","gamma","floor","minOp","bright","color","scan","edge","gScale","weight","stab","smooth","bands","blur"];
const KNOBS = [
  {f:"cols",   label:"Pixel size",    min:32, max:96, step:2, rtl:true, fmt:v=>v+" cols"},
  {f:"gamma",  label:"Contrast",      min:0.4, max:2.5, step:0.05, fmt:v=>v.toFixed(2)},
  {f:"bright", label:"Brightness",    min:0.5, max:1.6, step:0.05, fmt:v=>v.toFixed(2)},
  {f:"floor",  label:"Fill",          min:0, max:0.5, step:0.01, fmt:v=>v.toFixed(2)},
  {f:"minOp",  label:"Min opacity",   min:0.1, max:0.95, step:0.05, fmt:v=>v.toFixed(2)},
  {f:"edge",   label:"Contour boost", min:0, max:1, step:0.05, fmt:v=>v.toFixed(2)},
  {f:"scan",   label:"Scanlines",     min:0, max:0.8, step:0.05, fmt:v=>v?v.toFixed(2):"off"},
  {f:"smooth", label:"Smoothing",     min:0, max:0.95, step:0.05, fmt:v=>v?v.toFixed(2):"off"},
  {f:"stab",   label:"Stability",     min:0, max:0.15, step:0.01, fmt:v=>v?v.toFixed(2):"live"},
  {f:"bands",  label:"Bands",         min:0, max:12, step:1, fmt:v=>v>=3?""+Math.round(v):"off"},
  {f:"gScale", label:"Glyph size",    min:0.9, max:1.5, step:0.02, fmt:v=>v.toFixed(2)},
  {f:"weight", label:"Glyph weight",  min:400, max:700, step:50, fmt:v=>""+Math.round(v)},
];
let mode="green", curPreset=0, sel=null;
let G = pick(VARIANTS[curPreset]);
let O = {};
window.__PAL = PALS[mode];
function pick(v){ const o={}; FIELDS.forEach(f=>o[f]=v[f]); return o; }
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

// ---- panel ----
const knobsEl = document.getElementById("knobs"), inputs = {};
KNOBS.forEach(k=>{
  const w = document.createElement("div"); w.className="knob";
  const row = document.createElement("div"); row.className="row";
  const lb = document.createElement("label"); lb.textContent = k.label;
  const val = document.createElement("span"); val.className="val";
  row.appendChild(lb); row.appendChild(val);
  const inp = document.createElement("input");
  inp.type="range"; inp.min=k.min; inp.max=k.max; inp.step=k.step;
  if(k.rtl) inp.style.direction="rtl";
  inp.addEventListener("input", ()=>{ setField(k.f, parseFloat(inp.value)); val.textContent = k.fmt(parseFloat(inp.value)); });
  w.appendChild(row); w.appendChild(inp);
  knobsEl.appendChild(w);
  inputs[k.f] = {inp, val, fmt:k.fmt};
});
function seg(id, opts, field, getVal){
  const box = document.getElementById(id);
  opts.forEach(o=>{
    const b = document.createElement("button");
    b.textContent = o.label;
    b.addEventListener("click", ()=>{ setField(field, o.value); refreshPanel(); });
    b.dataset.v = typeof o.value==="string"?o.value:JSON.stringify(o.value);
    box.appendChild(b);
  });
  return ()=>{ const cur=getVal();
    [...box.children].forEach(b=>b.setAttribute("aria-pressed", b.dataset.v===cur)); };
}
const upRamp = seg("segRamp", [{label:"Fine",value:RAMPS.fine},{label:"Blocky",value:RAMPS.blocky},{label:"Brand",value:RAMPS.brand},{label:"Pixels",value:"PIXEL"}], "ramp", ()=>effSel().ramp);
const upDir = seg("segDir", [{label:"Ink",value:"ink"},{label:"Photo",value:"photo"}], "dir", ()=>effSel().dir);
const upColor = seg("segColor", [{label:"Mono",value:"mono"},{label:"Duo",value:"duo"}], "color", ()=>effSel().color);
const upBlur = seg("segBlur", [{label:"Off",value:0},{label:"On",value:1}], "blur", ()=>String(effSel().blur||0));
function effSel(){ return sel==null ? G : eff(sel); }
function setField(f, v){
  if(sel==null){ G[f]=v; tiles.forEach(resetTone); redraw(); }
  else { (O[sel] = O[sel]||{})[f]=v; resetTone(tiles[sel]); redraw(sel); markTweaks(); }
  save(); updateJson();
}
function refreshPanel(){
  const s = effSel();
  KNOBS.forEach(k=>{ inputs[k.f].inp.value = s[k.f]; inputs[k.f].val.textContent = k.fmt(s[k.f]); });
  upRamp(); upDir(); upColor(); upBlur();
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

// ---- presets ----
const nav = document.getElementById("nav");
VARIANTS.forEach((V,i)=>{
  const b = document.createElement("button");
  b.textContent = V.name;
  b.title = V.desc;
  b.addEventListener("click", ()=>setPreset(i));
  nav.appendChild(b);
});
function setPreset(i){
  curPreset = (i+VARIANTS.length)%VARIANTS.length;
  G = pick(VARIANTS[curPreset]);
  [...nav.children].forEach((b,j)=>b.setAttribute("aria-pressed", j===curPreset));
  tiles.forEach(resetTone); redraw(); refreshPanel(); save();
}

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
  if(e.key>="1" && e.key<="9") setPreset(parseInt(e.key)-1);
  else if(e.key==="0") setPreset(9);
  else if(e.key==="Escape") select(null);
  else if(e.key==="g"||e.key==="G") setMode("green");
  else if(e.key==="w"||e.key==="W") setMode("white");
});

// ---- persistence ----
function save(){ try{ localStorage.setItem("lfAsciiTunerV3", JSON.stringify({G,O,curPreset})); }catch(e){} }
(function restore(){
  try{
    const st = JSON.parse(localStorage.getItem("lfAsciiTunerV3")||"null");
    if(st && st.G){ G = Object.assign(pick(VARIANTS[st.curPreset||0]), st.G); O = st.O||{}; curPreset = st.curPreset||0; }
  }catch(e){}
})();
[...nav.children].forEach((b,j)=>b.setAttribute("aria-pressed", j===curPreset));
markTweaks(); refreshPanel();
</script>
"""

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__VARIANTS__", json.dumps(rc.VARIANTS))
        .replace("__STEMS__", json.dumps(rc.STEMS))
        .replace("__CLIPS__", rc.build_clips("video"))
        .replace("__CORE__", rc.JS_CORE))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
