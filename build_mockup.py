#!/usr/bin/env python3
"""Assemble the people-ascii mockup — 9 LEVELED clips as the careers/about hero.

Split-hero composition matching the live site: copy on the left, the people
mosaic as a left-faded right-hand panel on the green band, mint-sheen headline,
code-rain texture. Green/White toggle for both bands. Clips leveled to a uniform
718x754 frame (scaled to 432x454), ~4s, natural speed."""
import base64, json, pathlib

BASE = pathlib.Path("/private/tmp/claude-501/-Users-marcoopertti-LF-Website/e8b6147a-7a6a-45e2-a0f9-c91d3a655e86/scratchpad")
CLIPS_DIR = BASE / "lv"
FONT_DIR = pathlib.Path("/Users/marcoopertti/lf-next/public/fonts")
OUT = BASE / "people-ascii-mockup.html"


def b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


sg = b64(FONT_DIR / "SpaceGrotesk-latin.woff2")
inter = b64(FONT_DIR / "Inter-latin.woff2")

STEMS = ["IMG_0949", "IMG_1685", "IMG_2140",
         "IMG_3621", "Niamien", "alex",
         "isaiah", "morgan", "sarah"]
EC = 0.15
clip_data = [{"ec": EC, "src": "data:video/mp4;base64," + b64(CLIPS_DIR / f"{stem}.mp4")} for stem in STEMS]
CLIPS_JSON = json.dumps(clip_data)

HTML = r"""
<style>
@font-face{font-family:'Space Grotesk';font-weight:400 700;font-display:swap;
  src:url(data:font/woff2;base64,__SG__) format('woff2');}
@font-face{font-family:'InterLF';font-weight:400 600;font-display:swap;
  src:url(data:font/woff2;base64,__INTER__) format('woff2');}

:root{
  --bg1:#0E4A47; --bg2:#0D3E3D; --bg3:#082625;
  --mint:#00FFA8; --mint2:#2FC189; --lightmint:#B9D9CF;
  --paper:#F1ECE0; --ink:#0D3E3D;
}
*{box-sizing:border-box;}
body{margin:0;}
.stage{
  font-family:'InterLF',system-ui,sans-serif; color:#fff;
  min-height:100vh; position:relative; overflow:hidden;
  display:flex; flex-direction:column;
  background:radial-gradient(125% 125% at 72% 42%,var(--bg1) 0%,var(--bg2) 46%,var(--bg3) 100%);
  transition:background .5s ease,color .5s ease;
}
.stage::before{content:'';position:absolute;inset:0;z-index:0;opacity:.13;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http://www.w3.org/2000/svg%27%20width%3D%27110%27%20height%3D%27104%27%3E%3Ctext%20x%3D%270%27%20y%3D%2712%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E1F%3EL%3C0/1F%3E%3C/text%3E%3Ctext%20x%3D%270%27%20y%3D%2738%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3EL%3C0/1F%3EL%3C0%3C/text%3E%3Ctext%20x%3D%270%27%20y%3D%2764%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E/1F%3EL%3C0/1F%3C/text%3E%3Ctext%20x%3D%270%27%20y%3D%2790%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E%3EL%3C0/1F%3EL%3C%3C/text%3E%3C/svg%3E");
  background-size:62px 59px; animation:flow 40s linear infinite;}
@keyframes flow{to{background-position:0 700px;}}
.stage[data-mode="white"]{color:var(--ink);
  background:radial-gradient(125% 125% at 72% 42%,#FBF8F0,var(--paper) 55%,#E4DDCC);}
.stage[data-mode="white"]::before{opacity:.05;}

/* top bar */
.bar{position:relative;z-index:5;display:flex;align-items:center;justify-content:space-between;
  padding:22px clamp(20px,4vw,64px);}
.brand{font-family:'Space Grotesk';font-weight:700;font-size:20px;letter-spacing:-.01em;
  display:flex;align-items:center;gap:9px;}
.brand .dot{width:11px;height:11px;border-radius:50%;background:var(--mint);box-shadow:0 0 15px var(--mint);}
.stage[data-mode="white"] .brand .dot{background:var(--mint2);box-shadow:none;}
.toggle{display:flex;border:1px solid rgba(255,255,255,.26);border-radius:999px;overflow:hidden;
  font-family:'Space Grotesk';font-size:12px;font-weight:600;letter-spacing:.02em;}
.stage[data-mode="white"] .toggle{border-color:rgba(13,62,61,.26);}
.toggle button{appearance:none;border:0;background:transparent;color:inherit;padding:8px 17px;cursor:pointer;
  transition:background .25s,color .25s;}
.toggle button[aria-pressed="true"]{background:var(--mint);color:#04211c;}
.stage[data-mode="white"] .toggle button[aria-pressed="true"]{background:var(--mint2);color:#fff;}
.toggle button:focus-visible{outline:2px solid var(--mint);outline-offset:2px;}

/* hero */
.hero{position:relative;flex:1;display:flex;align-items:center;}
.copy{position:relative;z-index:2;max-width:min(560px,90vw);
  padding:0 0 40px clamp(20px,6vw,88px);
  animation:rise .8s cubic-bezier(.2,.7,.3,1) both;}
@keyframes rise{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:none;}}
.eyebrow{font-family:'Space Grotesk';font-weight:600;font-size:12.5px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--mint2);margin:0 0 16px;}
.stage[data-mode="white"] .eyebrow{color:#1E6F63;}
h1{font-family:'Space Grotesk';font-weight:700;line-height:1.0;letter-spacing:-.025em;
  font-size:clamp(38px,5.4vw,66px);margin:0;text-wrap:balance;max-width:13ch;}
h1 b{background:linear-gradient(100deg,#1E6F63,#2FC189 18%,#00FFA8 34%,#EAFBF4 50%,#00FFA8 66%,#2FC189 84%,#1E6F63);
  background-size:280% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  color:transparent;animation:sheen 4.5s linear infinite;}
.stage[data-mode="white"] h1 b{background:linear-gradient(100deg,#1E6F63,#2FC189 42%,#0D3E3D);
  background-size:280% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}
@keyframes sheen{to{background-position:280% 0;}}
.sub{font-size:clamp(15px,1.3vw,18px);line-height:1.62;max-width:46ch;margin:22px 0 0;color:var(--lightmint);}
.stage[data-mode="white"] .sub{color:#3C5C55;}
.btns{display:flex;gap:14px;flex-wrap:wrap;margin-top:34px;}
.btn{display:inline-flex;align-items:center;gap:8px;font-family:'Space Grotesk';font-weight:600;font-size:15px;
  padding:13px 26px;border-radius:999px;text-decoration:none;cursor:pointer;transition:transform .2s,box-shadow .2s,background .3s;}
.btn-mint{background:var(--mint);color:#04211c;box-shadow:0 8px 26px rgba(0,255,168,.26);}
.btn-mint:hover{transform:translateY(-2px);box-shadow:0 12px 34px rgba(0,255,168,.4);}
.stage[data-mode="white"] .btn-mint{background:var(--mint2);color:#fff;box-shadow:0 8px 22px rgba(47,193,137,.32);}
.btn-ghost{border:1px solid rgba(255,255,255,.28);color:inherit;}
.stage[data-mode="white"] .btn-ghost{border-color:rgba(13,62,61,.3);}
.btn:focus-visible{outline:2px solid var(--mint);outline-offset:3px;}

/* right people panel */
.panel{position:absolute;right:0;top:0;bottom:0;width:54%;z-index:1;overflow:hidden;pointer-events:none;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 22%,#000 100%);
  mask-image:linear-gradient(90deg,transparent 0,#000 22%,#000 100%);}
.grid{position:absolute;top:50%;left:0;right:0;transform:translateY(-50%);height:90%;
  padding:0 clamp(20px,2.5vw,44px) 0 0;display:grid;grid-template-columns:repeat(3,1fr);
  grid-template-rows:repeat(3,1fr);gap:clamp(8px,1vw,14px);}
.ptile{position:relative;overflow:hidden;border-radius:11px;}
.ptile canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}

/* foot */
.foot{position:relative;z-index:2;padding:0 clamp(20px,4vw,64px) 20px;
  font-family:'Space Grotesk';font-size:11px;letter-spacing:.04em;color:rgba(185,217,207,.5);}
.stage[data-mode="white"] .foot{color:rgba(13,62,61,.45);}

/* responsive: panel becomes a faded backdrop, copy sits on top */
@media (max-width:960px){
  .panel{width:100%;opacity:.26;}
  .stage[data-mode="white"] .panel{opacity:.5;}
  .copy{max-width:none;padding-right:clamp(20px,6vw,88px);}
}
@media (max-width:640px){
  .panel{opacity:.16;}
  h1{font-size:clamp(34px,10vw,46px);} .sub{font-size:15px;}
  .btns{flex-direction:column;align-items:flex-start;}
}
@media (prefers-reduced-motion:reduce){.stage::before,h1 b,.copy{animation:none;}}
</style>

<div class="stage" data-mode="green" id="stage">
  <header class="bar">
    <div class="brand"><span class="dot"></span>LightFeather</div>
    <div class="toggle" role="group" aria-label="Color mode">
      <button id="mGreen" aria-pressed="true">Green</button>
      <button id="mWhite" aria-pressed="false">White</button>
    </div>
  </header>

  <section class="hero">
    <div class="copy">
      <p class="eyebrow">About &middot; Careers</p>
      <h1>Do serious work that <b>matters</b>.</h1>
      <p class="sub">LightFeather builds the software, data platforms, and secure systems federal
        agencies depend on. Work on hard problems with a team that values technical depth and
        operational excellence.</p>
      <div class="btns">
        <a class="btn btn-mint" href="#" onclick="return false">Browse Open Roles</a>
        <a class="btn btn-ghost" href="#" onclick="return false">Meet the team</a>
      </div>
    </div>
    <div class="panel" aria-hidden="true"><div class="grid" id="mosaic"></div></div>
  </section>

  <div class="foot" id="foot">people-ascii hero mockup &middot; 9 clips, leveled to one frame &middot; live ASCII on canvas &middot; toggle Green / White</div>
</div>

<script>
const CLIPS = __CLIPS__;
const RAMP = " .·:-=+i1lvtfcLF#".split("");
const PAL_GREEN = ["255,255,255","255,255,255","255,255,255"];
const PAL_LIGHT = ["92,120,120","45,74,72","13,62,61"];
const CFG = {cols:60, margin:0.16, floor:0.10, span:0.78, throttle:78};
const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion:reduce)").matches;
let PAL = PAL_GREEN;
const smooth = x => {x = x<0?0:x>1?1:x; return x*x*(3-2*x);};
const off = document.createElement("canvas");
const octx = off.getContext("2d",{willReadFrequently:true});
const mosaic = document.getElementById("mosaic");
const tiles = [];

function setup(t){
  const w=t.el.clientWidth||180, h=t.el.clientHeight||188, dpr=Math.min(2,window.devicePixelRatio||1);
  t.c.width=w*dpr; t.c.height=h*dpr; t.ctx.setTransform(dpr,0,0,dpr,0,0);
  t.cw=w; t.ch=h; t.ready=true;
}
const median = (arr) => { arr.sort((a,b)=>a-b); return arr[arr.length>>1]; };
function render(t){
  if(!t.ready || t.v.readyState<2) return;
  const ctx=t.ctx, vw=t.v.videoWidth||16, vh=t.v.videoHeight||10, cols=CFG.cols;
  const arv=vw/vh; let rw=t.cw, rh=rw/arv;
  if(rh>t.ch){rh=t.ch; rw=rh*arv;}
  const ox=(t.cw-rw)/2, oy=(t.ch-rh)/2, cell=rw/cols;
  const rows=Math.max(1,Math.round(rh/cell)), fnt=Math.ceil(cell*1.16);
  off.width=cols; off.height=rows;
  let data;
  try{ octx.drawImage(t.v,0,0,vw,vh,0,0,cols,rows); data=octx.getImageData(0,0,cols,rows).data; }catch(e){ return; }
  const n=cols*rows, lum=new Float32Array(n);
  for(let k=0;k<n;k++){const i=k*4; lum[k]=(0.299*data[i]+0.587*data[i+1]+0.114*data[i+2])/255;}
  // Per-clip adaptive cutoff (computed once): estimate the wall brightness from the brighter
  // top corner (wall above the shoulders), then keep only pixels darker than it. Darkness -> glyph
  // density, so shirts fill solidly (L/F/#) and the clean wall drops out entirely.
  if(t.solid==null){
    const pw=Math.max(2,Math.round(cols*0.16)), ph=Math.max(2,Math.round(rows*0.12)), tl=[], tr=[];
    for(let y=0;y<ph;y++){for(let x=0;x<pw;x++)tl.push(lum[y*cols+x]); for(let x=cols-pw;x<cols;x++)tr.push(lum[y*cols+x]);}
    const wall=Math.max(median(tl),median(tr));
    t.solid=Math.min(0.86,Math.max(0.42,wall-CFG.margin));
  }
  ctx.clearRect(0,0,t.cw,t.ch);
  ctx.font=fnt+"px 'Space Grotesk',monospace"; ctx.textBaseline="top";
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const k=y*cols+x, l=lum[k];
    if(l>=t.solid) continue;
    const dk=1-l, tc=smooth(smooth((dk-CFG.floor)/CFG.span));
    const gi=Math.round(tc*(RAMP.length-1));
    const col = tc>0.66?PAL[2]:tc>0.38?PAL[1]:PAL[0];
    ctx.fillStyle="rgba("+col+","+(0.45+0.55*tc).toFixed(2)+")";
    ctx.fillText(RAMP[gi], ox+x*cell, oy+y*cell);
  }
}
function makeTile(clip){
  const el=document.createElement("div"); el.className="ptile";
  const v=document.createElement("video");
  v.muted=true; v.loop=true; v.autoplay=true; v.playsInline=true;
  v.setAttribute("muted",""); v.setAttribute("playsinline","");
  const c=document.createElement("canvas"); el.appendChild(c);
  const t={el, v, c, ctx:c.getContext("2d"), clip, ready:false, cw:0, ch:0};
  v.addEventListener("loadeddata", ()=>{ if(reduce){setup(t);render(t);try{v.pause();}catch(e){}} else {v.play().catch(()=>{});setup(t);} });
  v.src=clip.src; v.load();
  return t;
}
CLIPS.forEach(clip=>{const t=makeTile(clip); tiles.push(t); mosaic.appendChild(t.el);});
let last=0;
function loop(ts){ if(ts-last>CFG.throttle){last=ts; for(const t of tiles) render(t);} requestAnimationFrame(loop); }
if(!reduce) requestAnimationFrame(loop);
addEventListener("resize", ()=>tiles.forEach(setup));
addEventListener("click", ()=>tiles.forEach(t=>{ if(t.v.paused && !reduce) t.v.play().catch(()=>{}); }));
const stage=document.getElementById("stage");
const bG=document.getElementById("mGreen"), bW=document.getElementById("mWhite");
function setMode(mode){
  stage.dataset.mode=mode; PAL = mode==="white"?PAL_LIGHT:PAL_GREEN;
  bG.setAttribute("aria-pressed",mode==="green"); bW.setAttribute("aria-pressed",mode==="white");
  for(const t of tiles) render(t);
}
bG.addEventListener("click",()=>setMode("green"));
bW.addEventListener("click",()=>setMode("white"));
</script>
"""

HTML = HTML.replace("__SG__", sg).replace("__INTER__", inter).replace("__CLIPS__", CLIPS_JSON)
OUT.write_text(HTML)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
