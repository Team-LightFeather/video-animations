#!/usr/bin/env python3
"""Build people-ascii-preview.html: the 9-clip mosaic rendered live with ONE
locked look — the settings Marco exported from the gallery tuner on 2026-07-23
(previewss.png). No presets, no knobs; just the picked look + G/W mode toggle."""
import json
import pathlib

import render_core as rc

OUT = pathlib.Path(__file__).parent / "people-ascii-preview.html"

# Exact global settings from the tuner's Copy-settings readout in previewss.png.
SETTINGS = {
    "cols": 54, "ramp": "PIXEL", "dir": "ink", "gamma": 0.65, "floor": 0.03,
    "minOp": 0.25, "bright": 0.75, "color": "duo", "scan": 0, "edge": 0.15,
    "gScale": 1.16, "weight": 400, "stab": 0.01, "smooth": 0.1, "bands": 0,
    "blur": 0,
}

HTML = r"""<title>People-ASCII — Preview</title>
<style>
__FONTS__
*{box-sizing:border-box;}
body{margin:0;background:#0D3E3D;font-family:'Space Grotesk',monospace;color:#EAF6F0;
  min-height:100vh;display:flex;flex-direction:column;}
body[data-mode="white"]{background:#FAFAF8;color:#0D3E3D;}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:14px clamp(14px,2.5vw,30px) 10px;flex-wrap:wrap;}
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
main{flex:1;display:flex;align-items:center;justify-content:center;
  padding:0 clamp(14px,2.5vw,30px) 14px;min-height:0;}
#mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);
  gap:clamp(6px,0.8vw,10px);width:100%;max-width:calc((100vh - 118px)*432/454);
  aspect-ratio:calc(3*432)/calc(3*454);max-height:calc(100vh - 118px);}
.ptile{position:relative;overflow:hidden;border-radius:9px;}
.ptile canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}
footer{padding:0 clamp(14px,2.5vw,30px) 12px;font-size:10.5px;letter-spacing:.04em;
  color:rgba(185,217,207,.5);}
body[data-mode="white"] footer{color:rgba(13,62,61,.45);}
</style>

<header>
  <h1><span class="dot"></span>People-ASCII &middot; preview</h1>
  <div class="toggle" role="group" aria-label="Color mode">
    <button id="mGreen" aria-pressed="false">Green</button>
    <button id="mWhite" aria-pressed="true">White</button>
  </div>
</header>
<main><div id="mosaic"></div></main>
<footer>locked look &middot; 54 cols &middot; pixels/ink/duo &middot; contrast 0.65 &middot; brightness 0.75 &middot; G/W to switch mode</footer>

<script>
const SETTINGS = __SETTINGS__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
__CORE__
const PALS = {
  green: {bright:"255,255,255", dim:"148,224,196"},
  white: {bright:"13,62,61", dim:"96,132,127"},
};
let mode = "white";
window.__PAL = PALS[mode];

const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion:reduce)").matches;
const mosaic = document.getElementById("mosaic");
const tiles = [];
CLIPS.forEach((clip,i)=>{
  const el = document.createElement("div"); el.className = "ptile";
  const v = document.createElement("video");
  v.muted = true; v.loop = true; v.autoplay = true; v.playsInline = true;
  v.setAttribute("muted",""); v.setAttribute("playsinline","");
  const c = document.createElement("canvas"); el.appendChild(c);
  const t = initTile(clip, c, v);
  v.addEventListener("loadeddata", ()=>{
    if(reduce){ sizeTile(t); renderTile(t, SETTINGS); try{v.pause();}catch(e){} }
    else { v.play().catch(()=>{}); sizeTile(t); }
  });
  v.src = clip.src; v.load();
  tiles.push(t); mosaic.appendChild(el);
});
function redraw(){ tiles.forEach(t=>renderTile(t, SETTINGS)); }
let last=0;
function loop(ts){ if(ts-last>85){ last=ts; redraw(); } requestAnimationFrame(loop); }
if(!reduce) requestAnimationFrame(loop);
addEventListener("resize", ()=>tiles.forEach(sizeTile));
addEventListener("click", ()=>tiles.forEach(t=>{ if(t.src.paused && !reduce) t.src.play().catch(()=>{}); }));

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
  if(e.key==="g"||e.key==="G") setMode("green");
  else if(e.key==="w"||e.key==="W") setMode("white");
});
document.body.dataset.mode = "white";
</script>
"""

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__SETTINGS__", json.dumps(SETTINGS))
        .replace("__STEMS__", json.dumps(rc.STEMS))
        .replace("__CLIPS__", rc.build_clips("video"))
        .replace("__CORE__", rc.JS_CORE))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
