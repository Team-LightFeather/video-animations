#!/usr/bin/env python3
"""200-COL + BRAND-COLOR clone of the SELECT command center
(gen_command_center_select.py). Identical page — same BASE (72 cols) — plus:
- Pixel size slider reaches 200 cols (very fine grid)
- Pixel color pickable from the LightFeather brand palette
  (brand-assets/tokens.css), globally AND per person: a new `pxc` settings
  field ("auto" = follow G/W mode, else a brand hex), with an always-visible
  "Clip colors" swatch row per person (same pattern as Clip start times).
Writes its own HTML file and uses its own localStorage key (lfSelectCC2X) so
it can NEVER touch Marco's tuned settings on the other command centers.

Playback is driven by a MASTER CLOCK so every video loops in sync: one global
Loop length (default = the shortest take), and per-video Start / End / Speed.
Each video plays the window [start, end] of its take fitted to the shared
period — its playback rate auto-derives from the window length, so adjusting
where a clip starts/ends (or how fast it goes) never breaks the sync."""
import json
import pathlib
import subprocess

import render_core as rc

OUT = pathlib.Path(__file__).parent / "lf-select-command-center-200.html"

rc.CLIPS_DIR = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select")
rc.STEMS = ["Marco", "Nate", "Ruben", "Sheelagh", "Isaiah"]

END_AUTO = 6.5  # End-knob max = "auto": window ends start+loopLen into the take


def duration(stem: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=duration", "-of", "csv=p=0",
         str(rc.CLIPS_DIR / f"{stem}.mp4")],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip().rstrip(","))


DURS = {s: round(duration(s), 2) for s in rc.STEMS}
LOOP_DEFAULT = round(min(DURS.values()), 1)

# The locked LF Blocks preview settings (2026-07-23) + playback fields.
BASE = {
    "cols": 72, "ramp": "PIXLF", "dir": "ink", "gamma": 2.5, "floor": 0.0,
    "minOp": 0.10, "bright": 0.65, "color": "mono", "scan": 0, "edge": 0.15,
    "gScale": 1.28, "weight": 700, "stab": 0, "smooth": 0, "bands": 0,
    "blur": 0, "lfThr": 0.75, "pixFill": 0.66, "lfEdge": 0, "lfFill": "blocks",
    "pxc": "auto", "loopLen": LOOP_DEFAULT, "start": 0, "end": END_AUTO,
}

HTML = r"""<title>LF Select — Command Center · 200 cols + brand colors</title>
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
#mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);
  gap:clamp(6px,0.8vw,10px);width:100%;max-width:calc((100vh - 150px)*1296/908);
  aspect-ratio:1296/908;max-height:calc(100vh - 150px);}
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
.sec .note{font-size:10px;color:#8FB9AB;line-height:1.4;margin-top:-3px;}
body[data-mode="white"] .sec .note{color:#4E6E67;}
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
.swatches{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;}
.sw{appearance:none;border:1px solid rgba(255,255,255,.28);border-radius:6px;height:22px;
  cursor:pointer;padding:0;}
body[data-mode="white"] .sw{border-color:rgba(13,62,61,.28);}
.sw[aria-pressed="true"]{outline:2px solid #00FFA8;outline-offset:1px;}
body[data-mode="white"] .sw[aria-pressed="true"]{outline-color:#2FC189;}
.sw.auto{background:linear-gradient(135deg,#fff 0 50%,#0D3E3D 50% 100%);}
.swatches.mini{gap:4px;}
.swatches.mini .sw{height:15px;border-radius:4px;}
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
  <h1><span class="dot"></span>LF Select &middot; Command Center &middot; 200 cols + colors<small>Marco &middot; Nate &middot; Ruben &middot; Sheelagh &middot; Isaiah &middot; synced loops</small></h1>
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
<footer>one shared loop (Loop length, default = shortest take) keeps every video in sync &middot; Start/End/Speed per video pick which slice of a take plays &mdash; the rate auto-derives so sync never breaks &middot; G/W mode &middot; click a tile = per-video tuning</footer>

<script>
const BASE = __BASE__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
const DURS = __DURS__;
const END_AUTO = __END_AUTO__;
__CORE__
const PALS = {
  green: {bright:"255,255,255", dim:"148,224,196"},
  white: {bright:"13,62,61", dim:"96,132,127"},
};
/* LightFeather brand palette (brand-assets/tokens.css) for pixel color */
const BRAND = [
  ["auto",    "Auto (G/W mode)"],
  ["#FFFFFF", "Base White"],
  ["#00FFA8", "Pulse Mint"],
  ["#2FC189", "Pulse Mint 20"],
  ["#00FFFF", "Data Lagoon"],
  ["#26C4C4", "Data Lagoon 20"],
  ["#FFDF8C", "Harvest Gold"],
  ["#FF9B66", "Ember Clay"],
  ["#FFB5D7", "Founder Pink"],
  ["#0D3E3D", "System Green"],
  ["#3C525E", "System Slate"],
  ["#7395A8", "Interface Gray"],
];
function rgbOf(hex){ const n=parseInt(hex.slice(1),16); return (n>>16)+","+((n>>8)&255)+","+(n&255); }
function palFor(s){
  if(!s.pxc || s.pxc==="auto") return PALS[mode];
  const c = rgbOf(s.pxc);
  return {bright:c, dim:c};
}
const FIELDS = Object.keys(BASE);
const GROUPS = [
  {title:"Pixel grid", knobs:[
    {f:"cols",    label:"Pixel size",   min:24, max:200, step:2, rtl:true, hero:true, fmt:v=>Math.round(v)+"<small>cols</small>"},
    {f:"pixFill", label:"Pixel fill",   min:0.4, max:1, step:0.02, fmt:v=>Math.round(v*100)+"%"},
  ]},
  {title:"Playback", note:"All videos share one loop. Start/End choose the slice of a take; its speed auto-derives so everything stays in sync. Speed moves End for you.", knobs:[
    {f:"loopLen", label:"Loop length (all)", min:1, max:6.3, step:0.1, fmt:v=>v.toFixed(1)+"s"},
    {f:"start",   label:"Start",  min:0, max:5.5, step:0.1, fmt:v=>v.toFixed(1)+"s"},
    {f:"end",     label:"End",    min:0.5, max:6.5, step:0.1, fmt:v=>v>=END_AUTO?"auto":v.toFixed(1)+"s"},
    {f:"speed",   label:"Speed",  min:0.4, max:2, step:0.05, fmt:v=>v.toFixed(2)+"×"},
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
    {f:"smooth", label:"Smoothing",   min:0, max:0.95, step:0.05, fmt:v=>v?v.toFixed(2):"off"},
    {f:"stab",   label:"Stability",   min:0, max:0.15, step:0.01, fmt:v=>v?v.toFixed(2):"live"},
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
    if(reduce){ sizeTile(t); redraw(i); try{v.pause();}catch(e){} }
    else { v.play().catch(()=>{}); sizeTile(t); }
  });
  v.src = clip.src; v.load();
  el.addEventListener("click", ev=>{ ev.stopPropagation(); select(sel===i?null:i); });
  tiles.push(t); mosaic.appendChild(el);
});
window.__tiles = tiles;  // for headless verification scripts

// ---- master clock: every video loops on the same period ----
const t0 = performance.now();
function loopLen(){ return Math.max(0.5, G.loopLen || 1); }
function playWin(i, d){
  // the slice of take i that plays each period, and the rate that fits it
  const s = eff(i);
  const st = Math.min(s.start||0, Math.max(0, d-0.4));
  const en = (s.end==null || s.end>=END_AUTO)
    ? Math.min(d, st + loopLen())
    : Math.min(Math.max(s.end, st+0.2), d);
  return {st, en, rate: Math.min(4, Math.max(0.25, (en-st)/loopLen()))};
}
function syncClock(){
  if(reduce) return;
  const phi = ((performance.now()-t0)/1000) % loopLen();
  tiles.forEach((t,i)=>{
    const d = t.src.duration;
    if(!d || t.src.readyState<2) return;
    const w = playWin(i, d);
    if(Math.abs(t.src.playbackRate - w.rate) > 0.01) t.src.playbackRate = w.rate;
    const target = Math.min(w.en - 0.03, w.st + phi*w.rate);
    if(Math.abs(t.src.currentTime - target) > 0.13){
      try{ t.src.currentTime = target; }catch(e){}
    }
  });
}
setInterval(syncClock, 200);
function redraw(only){ tiles.forEach((t,i)=>{ if(only==null||only===i){
  const s = eff(i); window.__PAL = palFor(s); renderTile(t, s);
} }); }
let last=0;
function loop(ts){ if(ts-last>85){ last=ts; syncClock(); redraw(); } requestAnimationFrame(loop); }
if(!reduce) requestAnimationFrame(loop);
addEventListener("resize", ()=>tiles.forEach(sizeTile));
addEventListener("click", ()=>tiles.forEach(t=>{ if(t.src.paused && !reduce) t.src.play().catch(()=>{}); }));

// ---- command rail ----
const groupsEl = document.getElementById("groups"), inputs = {};
groupsEl.style.display="flex"; groupsEl.style.flexDirection="column"; groupsEl.style.gap="10px";
const segUpdaters = [], clipStarts = [], clipColors = [];
function swatchStrip(mini, getCur, onPick){
  const btns = document.createElement("div"); btns.className = mini?"swatches mini":"swatches";
  BRAND.forEach(([v,name])=>{
    const b = document.createElement("button");
    b.className = "sw"+(v==="auto"?" auto":"");
    if(v!=="auto") b.style.background = v;
    b.title = name; b.dataset.v = v;
    b.addEventListener("click", ()=>onPick(v));
    btns.appendChild(b);
  });
  btns.update = ()=>{
    const cur = getCur()||"auto";
    [...btns.children].forEach(b=>b.setAttribute("aria-pressed", b.dataset.v===cur));
  };
  return btns;
}
function brandName(v){ const e=BRAND.find(x=>x[0]===(v||"auto")); return e?e[1]:v; }
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
  if(g.note){ const n=document.createElement("div"); n.className="note"; n.textContent=g.note; sec.appendChild(n); }
  g.knobs.forEach(k=>{
    const w = document.createElement("div"); w.className="knob"+(k.hero?" hero":"");
    const row = document.createElement("div"); row.className="row";
    const lb = document.createElement("label"); lb.textContent = k.label;
    const val = document.createElement("span"); val.className="val";
    row.appendChild(lb); row.appendChild(val);
    const inp = document.createElement("input");
    inp.type="range"; inp.min=k.min; inp.max=k.max; inp.step=k.step;
    if(k.rtl) inp.style.direction="rtl";
    inp.addEventListener("input", ()=>{
      const v = parseFloat(inp.value);
      if(k.f==="speed"){
        // Speed is a view on the window: it moves End so sync is preserved
        const wv = winSel();
        setField("end", Math.min(END_AUTO-0.01, Math.max(0.5, wv.st + loopLen()*v)));
      } else {
        setField(k.f, v);
      }
      val.innerHTML = k.fmt(v);
    });
    w.appendChild(row); w.appendChild(inp);
    sec.appendChild(w);
    inputs[k.f] = {inp, val, fmt:k.fmt};
  });
  if(g.title==="Pixel grid"){
    sec.appendChild(segEl("Fill style", [{label:"Blocks",value:"blocks"},{label:"Lines",value:"lines"}], "lfFill", ()=>effSel().lfFill||"blocks"));
    // pixel color from the brand palette (follows the global/per-video scope)
    const w = document.createElement("div"); w.className="knob";
    const row = document.createElement("div"); row.className="row";
    const lb = document.createElement("label"); lb.textContent="Pixel color";
    const val = document.createElement("span"); val.className="val";
    row.appendChild(lb); row.appendChild(val);
    const strip = swatchStrip(false, ()=>effSel().pxc,
      v=>{ setField("pxc", v); refreshPanel(); });
    w.appendChild(row); w.appendChild(strip);
    sec.appendChild(w);
    segUpdaters.push(()=>{ strip.update(); val.textContent = brandName(effSel().pxc); });
  }
  if(g.title==="Letter detail"){
    sec.appendChild(segEl("L/F at silhouette edges", [{label:"On",value:1},{label:"Off",value:0}], "lfEdge", ()=>String(effSel().lfEdge==null?0:effSel().lfEdge)));
  }
  if(g.title==="Motion"){
    sec.appendChild(segEl("Noise blur", [{label:"Off",value:0},{label:"On",value:1}], "blur", ()=>String(effSel().blur||0)));
  }
  groupsEl.appendChild(sec);
  if(g.title==="Pixel grid"){
    // per-clip colors, always visible — one brand-swatch row per person
    const cc = document.createElement("div"); cc.className="sec";
    const cct = document.createElement("div"); cct.className="st"; cct.textContent="Clip colors";
    cc.appendChild(cct);
    STEMS.forEach((name,i)=>{
      const w = document.createElement("div"); w.className="knob";
      const row = document.createElement("div"); row.className="row";
      const lb = document.createElement("label"); lb.textContent = name;
      const val = document.createElement("span"); val.className="val";
      row.appendChild(lb); row.appendChild(val);
      const strip = swatchStrip(true, ()=>eff(i).pxc, v=>{
        (O[i] = O[i]||{}).pxc = v;
        redraw(i); markTweaks(); save(); updateJson(); updateClipColors();
        if(sel===i) refreshPanel();
      });
      w.appendChild(row); w.appendChild(strip);
      cc.appendChild(w);
      clipColors.push({strip, val, i});
    });
    groupsEl.appendChild(cc);
  }
  if(g.title==="Playback"){
    // per-clip start times, always visible — one slider per person
    const cs = document.createElement("div"); cs.className="sec";
    const cst = document.createElement("div"); cst.className="st"; cst.textContent="Clip start times";
    cs.appendChild(cst);
    STEMS.forEach((name,i)=>{
      const w = document.createElement("div"); w.className="knob";
      const row = document.createElement("div"); row.className="row";
      const lb = document.createElement("label"); lb.textContent = name;
      const val = document.createElement("span"); val.className="val";
      row.appendChild(lb); row.appendChild(val);
      const inp = document.createElement("input");
      inp.type="range"; inp.min=0; inp.max=Math.max(0.5,(DURS[name]||END_AUTO)-0.4); inp.step=0.1;
      inp.addEventListener("input", ()=>{
        const v = parseFloat(inp.value);
        (O[i] = O[i]||{}).start = v;
        resetTone(tiles[i]); redraw(i); markTweaks(); save(); updateJson();
        val.textContent = v.toFixed(1)+"s";
        if(sel===i) refreshPanel();
      });
      w.appendChild(row); w.appendChild(inp);
      cs.appendChild(w);
      clipStarts.push({inp, val, i});
    });
    groupsEl.appendChild(cs);
  }
});
function updateClipStarts(){
  clipStarts.forEach(c=>{
    const v = eff(c.i).start||0;
    c.inp.value = v; c.val.textContent = v.toFixed(1)+"s";
  });
}
function updateClipColors(){
  clipColors.forEach(c=>{
    c.strip.update();
    c.val.textContent = brandName(eff(c.i).pxc);
  });
}
function effSel(){ return sel==null ? G : eff(sel); }
function winSel(){
  const d = sel==null ? END_AUTO : (tiles[sel].src.duration || END_AUTO);
  return playWin(sel==null ? -1 : sel, d);
}
function setField(f, v){
  if(f==="loopLen"){ G[f]=v; }                       // sync period is global-only
  else if(sel==null){ G[f]=v; }
  else { (O[sel] = O[sel]||{})[f]=v; markTweaks(); }
  if(sel==null){ tiles.forEach(resetTone); redraw(); }
  else { resetTone(tiles[sel]); redraw(sel); }
  save(); updateJson();
}
function refreshPanel(){
  const s = effSel();
  Object.keys(inputs).forEach(f=>{
    if(f==="speed") return;
    inputs[f].inp.value = s[f]; inputs[f].val.innerHTML = inputs[f].fmt(s[f]);
  });
  const w = winSel();
  inputs.speed.inp.value = w.rate;
  inputs.speed.val.innerHTML = inputs.speed.fmt(w.rate);
  segUpdaters.forEach(u=>u());
  document.getElementById("scopeLbl").textContent = sel==null ? "Tuning: all videos" : "Tuning: "+(sel+1)+" · "+STEMS[sel];
  document.getElementById("backAll").style.display = sel==null ? "none" : "";
  document.getElementById("resetVid").style.display = sel==null ? "none" : "";
  updateClipStarts();
  updateClipColors();
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
function save(){ try{ localStorage.setItem("lfSelectCC2X", JSON.stringify({G,O})); }catch(e){} }
(function restore(){
  try{
    const st = JSON.parse(localStorage.getItem("lfSelectCC2X")||"null");
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
        .replace("__CORE__", rc.JS_CORE)
        .replace("__DURS__", json.dumps(DURS))
        .replace("__END_AUTO__", json.dumps(END_AUTO)))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB",
      f"(loop default {LOOP_DEFAULT}s)")
