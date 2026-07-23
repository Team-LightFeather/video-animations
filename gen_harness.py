#!/usr/bin/env python3
"""Build the offline browser test harness: still JPEG frames + the real render
engine + real fonts. Open with ?v=N to render variant N as a large 3x3 grid."""
import json
import pathlib

import render_core as rc

OUT = pathlib.Path(__file__).parent / "harness.html"

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
__FONTS__
body{margin:0;background:#0D3E3D;font-family:'Space Grotesk',monospace;}
body[data-mode="white"]{background:#FFFBF8;}
#hdr,.hdr{color:#B9D9CF;padding:14px 20px 6px;font-size:17px;}
body[data-mode="white"] #hdr,.hdr{color:#0D3E3D;}
#grid,.grid{display:grid;grid-template-columns:repeat(3,300px);grid-auto-rows:315px;gap:10px;padding:8px 20px 20px;}
#grid canvas{width:300px;height:315px;display:block;}
</style></head><body data-mode="green">
<div id="hdr">loading…</div><div id="grid"></div>
<script>
const VARIANTS = __VARIANTS__;
const CLIPS = __CLIPS__;
__CORE__
const q = new URLSearchParams(location.search);
const mode = q.get("m")==="white" ? "white" : "green";
document.body.dataset.mode = mode;
window.__PAL = mode==="white"
  ? {bright:"13,62,61", dim:"96,132,127"}
  : {bright:"255,255,255", dim:"148,224,196"};
document.getElementById("hdr").remove();
document.getElementById("grid").remove();
const imgs = [];
let loaded = 0;
CLIPS.forEach(clip=>{
  const img = new Image();
  imgs.push(img);
  img.onload = ()=>{ if(++loaded===CLIPS.length) drawAll(); };
  img.src = clip.src;
});
function drawAll(){
  document.fonts.ready.then(()=>{
    const only = q.get("v");
    const VARS = only==null ? VARIANTS : [VARIANTS[(+only)%VARIANTS.length]];
    VARS.forEach((V,vi)=>{
      const hdr = document.createElement("div");
      hdr.id = "hdr"; hdr.textContent = V.name + " — " + V.desc;
      document.body.appendChild(hdr);
      const grid = document.createElement("div");
      grid.id = "grid";
      document.body.appendChild(grid);
      CLIPS.forEach((clip,ci)=>{
        const c = document.createElement("canvas");
        grid.appendChild(c);
        const t = initTile(clip, c, imgs[ci]);
        sizeTile(t); renderTile(t, V);
      });
    });
    document.title = "RENDERED";
  });
}
</script></body></html>
"""

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__VARIANTS__", json.dumps(rc.VARIANTS))
        .replace("__CLIPS__", rc.build_clips("frame"))
        .replace("__CORE__", rc.JS_CORE))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
