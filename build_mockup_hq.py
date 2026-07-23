#!/usr/bin/env python3
"""Assemble the people-ascii mockup — 9 LEVELED clips as the careers/about hero.

Split-hero composition matching the live site: copy on the left, the people
mosaic as a left-faded right-hand panel on the green band, mint-sheen headline,
code-rain texture. Green/White toggle for both bands. Clips leveled to a uniform
718x754 frame (scaled to 432x454), ~4s, natural speed.

v6 render (photographic, like the original zoomout.png look):
- brightness -> glyph density: lit skin/shirts dense+bright, dark features
  (eyebrows, eyes, mouth, hair) sparse, so faces stay clear and features pop;
  tonal range normalized per clip; single color per mode (white / dark teal)
- small disconnected components dropped (< 18% of the largest blob)
- per-clip "guard zones" backed by a BAKED static-background grid (temporal
  max luma over the loop): inside a zone, a cell only draws if it is clearly
  darker than the background's brightest state (kills the door/mirror/paper
  in morgan's clip and wall shadows in sarah's, while moving hands survive)."""
import base64, json, pathlib, subprocess

BASE = pathlib.Path("/private/tmp/claude-501/-Users-marcoopertti-LF-Website/b79342c2-4395-4a95-bab0-271135cf64d3/scratchpad")
CLIPS_DIR = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/lv20")
FONT_DIR = pathlib.Path("/Users/marcoopertti/lf-next/public/fonts")
OUT = BASE / "people-ascii-mockup-hq.html"

BG_COLS = 60
# guard zones per clip: [x0, y0, x1, y1, dark_cap|None]
ZONES = {
    "morgan": [[0.58, 0.0, 1.0, 1.0, None]],
    "sarah": [[0.0, 0.70, 0.34, 1.0, 0.38], [0.0, 0.90, 0.62, 1.0, 0.38]],
    "alex": [[0.0, 0.0, 0.07, 1.0, None]],
    "IMG_0949": [[0.0, 0.0, 0.32, 1.0, 0.40], [0.68, 0.0, 1.0, 1.0, 0.40],
                 [0.32, 0.0, 0.68, 0.16, 0.40]],
    "Niamien": [[0.0, 0.0, 0.16, 1.0, None], [0.84, 0.0, 1.0, 1.0, None],
                [0.16, 0.70, 0.30, 1.0, None], [0.70, 0.70, 0.84, 1.0, None]],
}


def b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


def bake_bgmax(clip: pathlib.Path) -> tuple[str, int, int]:
    """Per-cell temporal MAX luma over the loop at ASCII-grid resolution.
    Background is the brightest state of a cell (walls are lighter than people)."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(clip)],
        check=True, capture_output=True, text=True).stdout.strip().split(",")
    vw, vh = int(probe[0]), int(probe[1])
    bh = round(vh / vw * BG_COLS)
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(clip),
         "-vf", f"fps=4,scale={BG_COLS}:{bh}", "-pix_fmt", "gray",
         "-f", "rawvideo", "-"],
        check=True, capture_output=True).stdout
    n = BG_COLS * bh
    frames = len(raw) // n
    grid = bytearray(n)
    for f in range(frames):
        off = f * n
        for k in range(n):
            v = raw[off + k]
            if v > grid[k]:
                grid[k] = v
    return base64.b64encode(bytes(grid)).decode(), BG_COLS, bh


sg = b64(FONT_DIR / "SpaceGrotesk-latin.woff2")
inter = b64(FONT_DIR / "Inter-latin.woff2")

STEMS = ["IMG_0949", "IMG_1685", "IMG_2140",
         "IMG_3621", "Niamien", "alex",
         "isaiah", "morgan", "sarah"]
EC = 0.15
clip_data = []
for stem in STEMS:
    bg, bgw, bgh = bake_bgmax(CLIPS_DIR / f"{stem}.mp4")
    clip_data.append({"ec": EC, "src": "data:video/mp4;base64," + b64(CLIPS_DIR / f"{stem}.mp4"),
                      "bg": bg, "bgw": bgw, "bgh": bgh, "zones": ZONES.get(stem, []),
                      "wr": stem == "IMG_0949"})
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

  <div class="foot" id="foot">people-ascii hero mockup &middot; HQ clips &middot; v6 render: photographic feature accents, subjects isolated &middot; 9 clips, leveled to one frame &middot; live ASCII on canvas &middot; toggle Green / White</div>
</div>

<script>
const CLIPS = __CLIPS__;
const RAMP = " .·:-=+i1lvtfcLF#".split("");
const PAL_GREEN = "255,255,255";
const PAL_LIGHT = "13,62,61";
const CFG = {cols:60, margin:0.18, bgDelta:0.13, minComp:0.18, glyphFloor:0.08, wallCap:0.40, wallEps:0.06, fringe:0.06, throttle:78};
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
  const n=cols*rows;
  if(t.n!==n){ t.n=n; t.lum=new Float32Array(n); t.keep=new Uint8Array(n); t.tmp=new Uint8Array(n); t.lbl=new Int32Array(n); t.stk=new Int32Array(n); }
  const lum=t.lum, keep=t.keep, tmp=t.tmp, lbl=t.lbl, stk=t.stk, bgw=t.clip.bgw, bgh=t.clip.bgh;
  for(let k=0;k<n;k++){const i=k*4; lum[k]=(0.299*data[i]+0.587*data[i+1]+0.114*data[i+2])/255;}
  // 1) keep = darker than the wall cutoff (t.solid precomputed from the BAKED background,
  // so a raised fist in frame one can never poison the wall estimate)
  for(let k=0;k<n;k++) keep[k]=lum[k]<t.solid?1:0;
  // 2) guard zones: static background (door/mirror/poster/shadow corners) dies there,
  // while moving hands stay (they are darker than the baked background's bright state)
  for(const z of t.clip.zones){
    const x0=z[0],y0=z[1],x1=z[2],y1=z[3],cap=z[4];
    for(let y=0;y<rows;y++){
      const fy=y/rows; if(fy<y0||fy>y1) continue;
      const by=Math.min(bgh-1,Math.round(y*(bgh-1)/Math.max(1,rows-1)));
      for(let x=0;x<cols;x++){
        const k=y*cols+x; if(!keep[k]) continue;
        const fx=x/cols; if(fx<x0||fx>x1) continue;
        const bl=t.bg[by*bgw+Math.min(bgw-1,x)]/255;
        if(lum[k]>=bl-CFG.bgDelta || (cap!=null && lum[k]>=cap)) keep[k]=0;
      }
    }
  }
  // 3) wall-cell rule (only clips flagged wr): a cell whose baked max is near bare wall
  // is one the subject merely transits -- mid-bright content there is her cast shadow
  if(t.clip.wr){
    for(let y=0;y<rows;y++){
      const by=Math.min(bgh-1,Math.round(y*(bgh-1)/Math.max(1,rows-1)));
      for(let x=0;x<cols;x++){
        const k=y*cols+x;
        if(keep[k] && lum[k]>=CFG.wallCap && t.bg[by*bgw+Math.min(bgw-1,x)]/255>=t.wall-CFG.wallEps) keep[k]=0;
      }
    }
  }
  // 4) fringe: silhouette-boundary cells that are nearly wall-bright are shadow residue
  tmp.set(keep);
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const k=y*cols+x;
    if(!keep[k] || lum[k]<t.solid-CFG.fringe) continue;
    let edge=0;
    for(let dy=-1;dy<=1&&!edge;dy++)for(let dx=-1;dx<=1;dx++){
      const nx=x+dx, ny=y+dy;
      if(nx<0||ny<0||nx>=cols||ny>=rows||!keep[ny*cols+nx]){edge=1;break;}
    }
    if(edge) tmp[k]=0;
  }
  keep.set(tmp);
  // 5) drop small disconnected blobs (background remnants)
  lbl.fill(0);
  const sizes=[0];
  let m=0, largest=0;
  for(let s=0;s<n;s++){
    if(!keep[s]||lbl[s]) continue;
    m++; let sp=0, size=0;
    stk[sp++]=s; lbl[s]=m;
    while(sp){
      const k=stk[--sp]; size++;
      const cx=k%cols, cy=(k/cols)|0;
      for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
        if(!dx&&!dy) continue;
        const nx=cx+dx, ny=cy+dy;
        if(nx<0||ny<0||nx>=cols||ny>=rows) continue;
        const nk=ny*cols+nx;
        if(keep[nk]&&!lbl[nk]){lbl[nk]=m; stk[sp++]=nk;}
      }
    }
    sizes.push(size); if(size>largest) largest=size;
  }
  const minSize=Math.max(6,Math.round(largest*CFG.minComp));
  for(let k=0;k<n;k++) if(keep[k]&&sizes[lbl[k]]<minSize) keep[k]=0;
  // 4) PHOTOGRAPHIC mapping (the original zoomout look): brightness -> density.
  // Lit skin and shirts render dense+bright; dark features (eyebrows, eyes, mouth
  // shadows, hair) go sparse, so faces stay clear and features read as accents.
  // Tonal range normalized per clip (cached) so all nine tiles match.
  if(t.lo==null){
    const kept=[]; for(let k=0;k<n;k++) if(keep[k]) kept.push(lum[k]);
    kept.sort((a,b)=>a-b);
    t.lo=kept.length?kept[Math.floor(kept.length*0.05)]:0;
    t.hi=kept.length?kept[Math.min(kept.length-1,Math.floor(kept.length*0.95))]:1;
  }
  const rng=Math.max(0.15,t.hi-t.lo);
  ctx.clearRect(0,0,t.cw,t.ch);
  ctx.font=fnt+"px 'Space Grotesk',monospace"; ctx.textBaseline="top";
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const k=y*cols+x;
    if(!keep[k]) continue;
    const tc=smooth((lum[k]-t.lo)/rng);
    const gi=Math.min(RAMP.length-1,Math.round((CFG.glyphFloor+(1-CFG.glyphFloor)*tc)*(RAMP.length-1)));
    ctx.fillStyle="rgba("+PAL+","+(0.45+0.55*tc).toFixed(2)+")";
    ctx.fillText(RAMP[gi], ox+x*cell, oy+y*cell);
  }
}
function makeTile(clip){
  const el=document.createElement("div"); el.className="ptile";
  const v=document.createElement("video");
  v.muted=true; v.loop=true; v.autoplay=true; v.playsInline=true;
  v.setAttribute("muted",""); v.setAttribute("playsinline","");
  const c=document.createElement("canvas"); el.appendChild(c);
  const bgs=atob(clip.bg), bg=new Uint8Array(bgs.length);
  for(let i=0;i<bgs.length;i++) bg[i]=bgs.charCodeAt(i);
  const pw=Math.max(2,Math.round(clip.bgw*0.16)), ph=Math.max(2,Math.round(clip.bgh*0.12)), btl=[], btr=[];
  for(let y=0;y<ph;y++){for(let x=0;x<pw;x++)btl.push(bg[y*clip.bgw+x]/255); for(let x=clip.bgw-pw;x<clip.bgw;x++)btr.push(bg[y*clip.bgw+x]/255);}
  const wall=Math.max(median(btl),median(btr));
  const t={el, v, c, ctx:c.getContext("2d"), clip, bg, wall,
    solid:Math.min(0.86,Math.max(0.42,wall-CFG.margin)), ready:false, cw:0, ch:0, n:0};
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
