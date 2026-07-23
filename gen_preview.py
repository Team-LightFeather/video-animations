#!/usr/bin/env python3
"""Build the locked-look people-ascii preview pages (settings from Marco's
2026-07-23 tuner export, previewss.png). Two outputs:

  people-ascii-preview.html        — the locked look in the WEBSITE's animation
      colors: the deployed CareersPeopleHero palettes from lf-next origin/main
      (careers mint 3-stop on the teal radial; about slate 3-stop on cream),
      including the site's 3-stop threshold logic (tc>0.66 / tc>0.38).
  people-ascii-preview-2color.html — strictly TWO colors: flat #0D3E3D
      background + solid #00FFA8 ink at full opacity; square size carries tone.

The 3-stop palette support is patched into this page's copy of JS_CORE only —
render_core.py itself is untouched (shared with the gallery/harness)."""
import json
import pathlib

import render_core as rc

DIR = pathlib.Path(__file__).parent

# Exact global settings from the tuner's Copy-settings readout in previewss.png.
BASE = {
    "cols": 54, "ramp": "PIXEL", "dir": "ink", "gamma": 0.65, "floor": 0.03,
    "minOp": 0.25, "bright": 0.75, "color": "duo", "scan": 0, "edge": 0.15,
    "gScale": 1.16, "weight": 400, "stab": 0.01, "smooth": 0.1, "bands": 0,
    "blur": 0,
}

# Deployed website animation (lf-next origin/main, CareersPeopleHero.tsx):
# palette stops low->high, picked at tc>0.66 / tc>0.38.
CAREERS_PAL = ["47,193,137", "0,255,168", "234,251,244"]   # careers hero, green
ABOUT_PAL = ["115,149,168", "60,82,94", "13,62,61"]        # about hero, light
CAREERS_BG = ("radial-gradient(120% 120% at 70% 45%,"
              "#0E4A47 0%,#0D3E3D 45%,#082625 100%)")

PAGES = [
    {
        "out": "people-ascii-preview.html",
        "title": "People-ASCII — Preview",
        "heading": "People-ASCII &middot; preview",
        "footer": ("locked look &middot; 54 cols &middot; pixels/ink &middot; "
                   "website palettes: careers (green) / about (light) &middot; "
                   "G/L to switch mode"),
        "settings": BASE,
        "default": "green",
        "keys": {"g": "green", "l": "light", "w": "light", "c": "light"},
        "modes": {
            "green": {"label": "Green", "bg": CAREERS_BG, "text": "#EAFBF4",
                      "accent": "#00FFA8", "accentText": "#04211c", "glow": True,
                      "border": "rgba(234,251,244,.35)",
                      "footer": "rgba(234,251,244,.5)", "pal": CAREERS_PAL},
            "light": {"label": "Light", "bg": "#FFFBF8", "text": "#0D3E3D",
                      "accent": "#0D3E3D", "accentText": "#FFFBF8", "glow": False,
                      "border": "rgba(13,62,61,.3)",
                      "footer": "rgba(13,62,61,.45)", "pal": ABOUT_PAL},
        },
    },
    {
        "out": "people-ascii-preview-2color.html",
        "title": "People-ASCII — Two-Color",
        "heading": "People-ASCII &middot; two-color",
        "footer": ("two colors only &middot; background #0D3E3D &middot; "
                   "ink #00FFA8 &middot; square size carries tone"),
        # flat full-opacity ink: minOp 1 + bright 1 pins alpha at 1, so the
        # only tonal signal left is the per-cell square size.
        "settings": {**BASE, "color": "mono", "minOp": 1.0, "bright": 1.0},
        "default": "green",
        "keys": {},
        "modes": {
            "green": {"label": "Green", "bg": "#0D3E3D", "text": "#EAFBF4",
                      "accent": "#00FFA8", "accentText": "#04211c", "glow": True,
                      "border": "rgba(234,251,244,.35)",
                      "footer": "rgba(234,251,244,.5)",
                      "pal": ["0,255,168"] * 3},
        },
    },
]

TEMPLATE = r"""<title>__TITLE__</title>
<style>
__FONTS__
*{box-sizing:border-box;}
body{margin:0;font-family:'Space Grotesk',monospace;min-height:100vh;
  display:flex;flex-direction:column;}
__MODECSS__
header{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:14px clamp(14px,2.5vw,30px) 10px;flex-wrap:wrap;}
h1{font-size:clamp(15px,2vw,20px);font-weight:700;margin:0;letter-spacing:-.01em;}
h1 .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:9px;}
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
  <h1><span class="dot"></span>__HEADING__</h1>
__TOGGLE__
</header>
<main><div id="mosaic"></div></main>
<footer>__FOOTER__</footer>

<script>
const SETTINGS = __SETTINGS__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
__CORE__
const MODES = __MODES__;
const KEYS = __KEYS__;
let mode = __DEFAULT__;
window.__PAL = {p: MODES[mode].pal};
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
  mode = m; window.__PAL = {p: MODES[m].pal};
  document.body.dataset.mode = m;
  document.querySelectorAll(".toggle button").forEach(b=>
    b.setAttribute("aria-pressed", b.dataset.m===m));
  redraw();
}
document.querySelectorAll(".toggle button").forEach(b=>
  b.addEventListener("click", ()=>setMode(b.dataset.m)));
addEventListener("keydown", e=>{
  const m = KEYS[e.key.toLowerCase()];
  if(m) setMode(m);
});
</script>
"""


def mode_css(page):
    rules = []
    for name, m in page["modes"].items():
        s = f'body[data-mode="{name}"]'
        glow = f'box-shadow:0 0 12px {m["accent"]};' if m["glow"] else "box-shadow:none;"
        rules.append(f'{s}{{background:{m["bg"]};color:{m["text"]};}}')
        rules.append(f'{s} h1 .dot{{background:{m["accent"]};{glow}}}')
        rules.append(f'{s} .toggle{{border-color:{m["border"]};}}')
        rules.append(f'{s} .toggle button[aria-pressed="true"]'
                     f'{{background:{m["accent"]};color:{m["accentText"]};}}')
        rules.append(f'{s} footer{{color:{m["footer"]};}}')
    d = page["modes"][page["default"]]
    rules.insert(0, f'body{{background:{d["bg"]};color:{d["text"]};}}')
    return "\n".join(rules)


def toggle_html(page):
    if len(page["modes"]) < 2:
        return ""
    btns = "".join(
        f'<button data-m="{name}" aria-pressed="{str(name == page["default"]).lower()}">'
        f'{m["label"]}</button>'
        for name, m in page["modes"].items())
    return f'  <div class="toggle" role="group" aria-label="Color mode">{btns}</div>'


# Patch the page-local copy of the engine: 3-stop palette (site thresholds)
# via window.__PAL.p, falling back to the stock bright/dim behaviour.
OLD_COL = 'const col=V.color==="duo"?(gc>0.55?PAL.bright:PAL.dim):PAL.bright;'
NEW_COL = ('const col=PAL.p?(gc>0.66?PAL.p[2]:gc>0.38?PAL.p[1]:PAL.p[0])'
           ':(V.color==="duo"?(gc>0.55?PAL.bright:PAL.dim):PAL.bright);')
assert OLD_COL in rc.JS_CORE, "render_core JS_CORE changed; re-check the palette patch"
CORE = rc.JS_CORE.replace(OLD_COL, NEW_COL)

FONTS = rc.fonts_css()
CLIPS = rc.build_clips("video")

for page in PAGES:
    html = (TEMPLATE
            .replace("__TITLE__", page["title"])
            .replace("__HEADING__", page["heading"])
            .replace("__FOOTER__", page["footer"])
            .replace("__FONTS__", FONTS)
            .replace("__MODECSS__", mode_css(page))
            .replace("__TOGGLE__", toggle_html(page))
            .replace("__SETTINGS__", json.dumps(page["settings"]))
            .replace("__STEMS__", json.dumps(rc.STEMS))
            .replace("__CLIPS__", CLIPS)
            .replace("__CORE__", CORE)
            .replace("__MODES__", json.dumps(page["modes"]))
            .replace("__KEYS__", json.dumps(page["keys"]))
            .replace("__DEFAULT__", json.dumps(page["default"])))
    out = DIR / page["out"]
    out.write_text(html)
    print("wrote", out, f"{out.stat().st_size/1024:.0f} KB")
