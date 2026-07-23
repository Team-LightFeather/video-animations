#!/usr/bin/env python3
"""Build the locked LF-Blocks preview page (Marco's exact command-center
settings, screenshot 2026-07-23 1:25 PM): 72-col one-color blocks, L/F
letterform details at 25%, contour boost 0.15, contrast 2.5, brightness 0.65.
No knobs — just the mosaic + Green/White toggle, same palettes as the
command center."""
import json
import pathlib

import render_core as rc

OUT = pathlib.Path(__file__).parent / "people-ascii-preview-lf.html"

# Exact global settings read off Marco's command-center screenshot.
SETTINGS = {
    "cols": 72, "ramp": "PIXLF", "dir": "ink", "gamma": 2.5, "floor": 0.0,
    "minOp": 0.10, "bright": 0.65, "color": "mono", "scan": 0, "edge": 0.15,
    "gScale": 1.28, "weight": 700, "stab": 0, "smooth": 0, "bands": 0,
    "blur": 0, "lfThr": 0.75, "pixFill": 0.66, "lfEdge": 0, "lfFill": "blocks",
}

MODES = {
    "green": {"label": "Green", "bg": "#0D3E3D", "text": "#EAF6F0",
              "accent": "#00FFA8", "accentText": "#04211c", "glow": True,
              "border": "rgba(234,251,244,.35)", "footer": "rgba(234,251,244,.5)",
              "pal": {"bright": "255,255,255", "dim": "148,224,196"}},
    "white": {"label": "White", "bg": "#FFFBF8", "text": "#0D3E3D",
              "accent": "#2FC189", "accentText": "#fff", "glow": False,
              "border": "rgba(13,62,61,.3)", "footer": "rgba(13,62,61,.45)",
              "pal": {"bright": "13,62,61", "dim": "96,132,127"}},
}
DEFAULT = "green"

HTML = r"""<title>People-ASCII — LF Blocks Preview</title>
<style>
__FONTS__
*{box-sizing:border-box;}
body{margin:0;font-family:'Space Grotesk',monospace;min-height:100vh;
  display:flex;flex-direction:column;}
__MODECSS__
header{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:14px clamp(14px,2.5vw,30px) 10px;flex-wrap:wrap;}
h1{font-size:clamp(15px,2vw,20px);font-weight:700;margin:0;letter-spacing:-.01em;}
h1 .dot{display:inline-block;width:10px;height:10px;margin-right:9px;}
.toggle{display:flex;border:1px solid;border-radius:999px;overflow:hidden;
  font-size:12px;font-weight:600;}
.toggle button{appearance:none;border:0;background:transparent;color:inherit;
  padding:6px 14px;cursor:pointer;font:inherit;}
main{flex:1;display:flex;align-items:center;justify-content:center;
  padding:0 clamp(14px,2.5vw,30px) 14px;min-height:0;}
#mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);
  gap:clamp(6px,0.8vw,10px);width:100%;max-width:calc((100vh - 118px)*432/454);
  aspect-ratio:calc(3*432)/calc(3*454);max-height:calc(100vh - 118px);}
.ptile{position:relative;overflow:hidden;border-radius:9px;}
.ptile canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}
footer{padding:0 clamp(14px,2.5vw,30px) 12px;font-size:10.5px;letter-spacing:.04em;}
</style>

<header>
  <h1><span class="dot"></span>People-ASCII &middot; LF blocks preview</h1>
  <div class="toggle" role="group" aria-label="Color mode">__TOGGLE__</div>
</header>
<main><div id="mosaic"></div></main>
<footer>locked LF Blocks look &middot; 72 cols &middot; one-color blocks + L/F letterform details &middot; G/W to switch mode</footer>

<script>
const SETTINGS = __SETTINGS__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
__CORE__
const MODES = __MODES__;
let mode = __DEFAULT__;
window.__PAL = MODES[mode].pal;
document.body.dataset.mode = mode;

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

function setMode(m){
  mode = m; window.__PAL = MODES[m].pal;
  document.body.dataset.mode = m;
  document.querySelectorAll(".toggle button").forEach(b=>
    b.setAttribute("aria-pressed", b.dataset.m===m));
  tiles.forEach(resetTone); redraw();
}
document.querySelectorAll(".toggle button").forEach(b=>
  b.addEventListener("click", ()=>setMode(b.dataset.m)));
addEventListener("keydown", e=>{
  if(e.key==="g"||e.key==="G") setMode("green");
  else if(e.key==="w"||e.key==="W") setMode("white");
});
</script>
"""


def mode_css():
    rules = []
    for name, m in MODES.items():
        s = f'body[data-mode="{name}"]'
        glow = f'box-shadow:0 0 12px {m["accent"]};' if m["glow"] else "box-shadow:none;"
        rules.append(f'{s}{{background:{m["bg"]};color:{m["text"]};}}')
        rules.append(f'{s} h1 .dot{{background:{m["accent"]};{glow}}}')
        rules.append(f'{s} .toggle{{border-color:{m["border"]};}}')
        rules.append(f'{s} .toggle button[aria-pressed="true"]'
                     f'{{background:{m["accent"]};color:{m["accentText"]};}}')
        rules.append(f'{s} footer{{color:{m["footer"]};}}')
    d = MODES[DEFAULT]
    rules.insert(0, f'body{{background:{d["bg"]};color:{d["text"]};}}')
    return "\n".join(rules)


toggle = "".join(
    f'<button data-m="{name}" aria-pressed="{str(name == DEFAULT).lower()}">'
    f'{m["label"]}</button>'
    for name, m in MODES.items())

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__MODECSS__", mode_css())
        .replace("__TOGGLE__", toggle)
        .replace("__SETTINGS__", json.dumps(SETTINGS))
        .replace("__STEMS__", json.dumps(rc.STEMS))
        .replace("__CLIPS__", rc.build_clips("video"))
        .replace("__CORE__", rc.JS_CORE)
        .replace("__MODES__", json.dumps(MODES))
        .replace("__DEFAULT__", json.dumps(DEFAULT)))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
