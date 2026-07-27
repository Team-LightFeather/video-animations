#!/usr/bin/env python3
"""Shared core for the people-ascii gallery: variant definitions, clip metadata
(baked background grids, guard zones), and the JS render engine used by BOTH the
offline browser test harness and the final gallery page."""
import base64
import json
import pathlib
import subprocess

CLIPS_DIR = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/lv20")
FONT_DIR = pathlib.Path("/Users/marcoopertti/lf-next/public/fonts")
FRAMES_DIR = pathlib.Path(__file__).parent / "frames"

STEMS = ["IMG_0949", "IMG_1685", "IMG_2140",
         "IMG_3621", "Niamien", "alex",
         "isaiah", "morgan", "sarah"]

BG_COLS = 60
ZONES = {
    "morgan": [[0.58, 0.0, 1.0, 1.0, None]],
    "sarah": [[0.0, 0.70, 0.34, 1.0, 0.38], [0.0, 0.90, 0.62, 1.0, 0.38]],
    "alex": [[0.0, 0.0, 0.07, 1.0, None]],
    "IMG_0949": [[0.0, 0.0, 0.32, 1.0, 0.40], [0.68, 0.0, 1.0, 1.0, 0.40],
                 [0.32, 0.0, 0.68, 0.16, 0.40]],
    "Niamien": [[0.0, 0.0, 0.16, 1.0, None], [0.84, 0.0, 1.0, 1.0, None],
                [0.16, 0.70, 0.30, 1.0, None], [0.70, 0.70, 0.84, 1.0, None]],
}
WALL_RULE = {"IMG_0949"}
# per-clip cutoff margin: sarah's satin shirt sits just under wall luma
MARGINS = {"sarah": 0.12}

RAMP_FINE = " .·:-=+i1lvtfcLF#"
RAMP_BLOCKY = " .:-=+*%#@"
RAMP_BRAND = " .:=iltLF#"

# Every variant is a complete settings object (same fields the tuner knobs edit):
# cols (pixel size), gamma (contrast), floor (fill), minOp (min opacity),
# bright (master brightness), edge (contour boost), scan (scanline strength),
# gScale (glyph size vs cell), weight (font weight), dir, ramp, color.
VARIANTS = [
    {"key": "v3", "name": "3.0 · Original", "desc": "Version 3 exactly as picked: dark features drawn as bright strokes, skin nearly empty.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.35, "bright": 1.0, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3bright", "name": "3.1 · Brighter", "desc": "Same ink, lifted: stronger strokes, nothing else touched.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.45, "bright": 1.25, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3contrast", "name": "3.2 · High Contrast", "desc": "Harder curve: features punch, skin drops away further.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.9, "floor": 0.0, "minOp": 0.30, "bright": 1.2, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3bold", "name": "3.3 · Bold Strokes", "desc": "Thicker pen: heavier glyphs at the same density.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.40, "bright": 1.1, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.28, "weight": 700, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3full", "name": "3.4 · Fuller Figures", "desc": "A touch of fill + contours so light clothing stays visible.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.14, "minOp": 0.40, "bright": 1.1, "color": "mono", "scan": 0.0, "edge": 0.25, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3chunky", "name": "3.5 · Chunky Ink", "desc": "Same ink at bigger pixels.",
     "cols": 44, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.40, "bright": 1.1, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3fine", "name": "3.6 · Fine Ink", "desc": "Same ink at smaller pixels — more delicate.",
     "cols": 80, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.38, "bright": 1.1, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3calm", "name": "3.7 · Calm Ink", "desc": "Original look with gentle anti-shimmer — strokes hold still until real movement.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.35, "bright": 1.0, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.05, "smooth": 0.5, "bands": 0, "blur": 0},
    {"key": "v3blocks", "name": "3.8 · Ink Blocks", "desc": "The ink look drawn as small square pixels instead of letters.",
     "cols": 64, "ramp": "PIXEL", "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.40, "bright": 1.15, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3duo", "name": "3.9 · Duo Ink", "desc": "Ink in two tones: bright strokes over dim mint mids.",
     "cols": 60, "ramp": RAMP_FINE, "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.40, "bright": 1.1, "color": "duo", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 400, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0},
    {"key": "v3lf", "name": "3.10 · LF Blocks", "desc": "Solid one-color blocks for the body; L and F letterforms where a block doesn't fit — the silhouette edge and the finest details.",
     "cols": 44, "ramp": "PIXLF", "dir": "ink", "gamma": 1.5, "floor": 0.0, "minOp": 0.40, "bright": 1.15, "color": "mono", "scan": 0.0, "edge": 0.0, "gScale": 1.16, "weight": 700, "stab": 0.0, "smooth": 0.0, "bands": 0, "blur": 0, "lfThr": 0.75, "pixFill": 0.82, "lfEdge": 1, "lfFill": "blocks"},
]


def b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


def bake_bgmax(clip: pathlib.Path):
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
    grid = bytearray(n)
    for f in range(len(raw) // n):
        off = f * n
        for k in range(n):
            if raw[off + k] > grid[k]:
                grid[k] = raw[off + k]
    return base64.b64encode(bytes(grid)).decode(), BG_COLS, bh


def build_clips(media: str) -> str:
    """media: 'video' embeds the mp4s, 'frame' embeds still JPEGs (test harness)."""
    out = []
    for stem in STEMS:
        bg, bgw, bgh = bake_bgmax(CLIPS_DIR / f"{stem}.mp4")
        if media == "video":
            src = "data:video/mp4;base64," + b64(CLIPS_DIR / f"{stem}.mp4")
        else:
            src = "data:image/jpeg;base64," + b64(FRAMES_DIR / f"{stem}.jpg")
        out.append({"src": src, "bg": bg, "bgw": bgw, "bgh": bgh,
                    "zones": ZONES.get(stem, []), "wr": stem in WALL_RULE,
                    "mg": MARGINS.get(stem, 0.18)})
    return json.dumps(out)


def fonts_css() -> str:
    sg = b64(FONT_DIR / "SpaceGrotesk-latin.woff2")
    return ("@font-face{font-family:'Space Grotesk';font-weight:400 700;"
            "src:url(data:font/woff2;base64," + sg + ") format('woff2');}")


# The render engine. Expects globals: VARIANTS, CLIPS, and per-page wiring that
# creates tiles via initTile(clip, canvasEl, srcEl) and calls renderTile(t, V).
JS_CORE = r"""
const MASK = {margin:0.18, bgDelta:0.13, minComp:0.18, wallCap:0.40, wallEps:0.06, fringe:0.06};
const smooth = x => {x = x<0?0:x>1?1:x; return x*x*(3-2*x);};
const median = a => {a.sort((p,q)=>p-q); return a[a.length>>1];};
const off = document.createElement("canvas");
const octx = off.getContext("2d",{willReadFrequently:true});
const off2 = document.createElement("canvas");
const o2ctx = off2.getContext("2d",{willReadFrequently:true});

function initTile(clip, c, srcEl){
  const bs=atob(clip.bg), bg=new Uint8Array(bs.length);
  for(let i=0;i<bs.length;i++) bg[i]=bs.charCodeAt(i);
  const pw=Math.max(2,Math.round(clip.bgw*0.16)), ph=Math.max(2,Math.round(clip.bgh*0.12)), tl=[], tr=[];
  for(let y=0;y<ph;y++){for(let x=0;x<pw;x++)tl.push(bg[y*clip.bgw+x]/255); for(let x=clip.bgw-pw;x<clip.bgw;x++)tr.push(bg[y*clip.bgw+x]/255);}
  const wall=Math.max(median(tl),median(tr));
  // wd = dark-wall clip (e.g. Ruben's 2026-07-24 take: gray wall, white shirt).
  // The luma-only "darker than wall" mask inverts on these; they use a
  // chroma+extremes mask in renderTile instead.
  return {clip, c, ctx:c.getContext("2d"), src:srcEl, bg, wall, wd:wall<0.55,
          solid:Math.min(0.86,Math.max(0.42,wall-(clip.mg||MASK.margin))),
          cw:0, ch:0, n:0, lo:null, hi:null, ready:false, emaOk:false, lastT:0};
}
function sizeTile(t){
  const w=t.c.clientWidth||200, h=t.c.clientHeight||210, dpr=Math.min(2,window.devicePixelRatio||1);
  t.c.width=w*dpr; t.c.height=h*dpr; t.ctx.setTransform(dpr,0,0,dpr,0,0);
  t.cw=w; t.ch=h; t.ready=true;
}
function resetTone(t){
  t.lo=null; t.hi=null; t.emaOk=false;
  if(t.pKeep) t.pKeep.fill(0);
  if(t.pGi) t.pGi.fill(-1);
}

function renderTile(t, V){
  if(!t.ready) return;
  const el=t.src;
  const vw=el.videoWidth||el.naturalWidth||16, vh=el.videoHeight||el.naturalHeight||10;
  if(el.readyState!==undefined && el.readyState<2) return;
  const ctx=t.ctx, cols=V.cols, arv=vw/vh;
  let rw=t.cw, rh=rw/arv;
  if(rh>t.ch){rh=t.ch; rw=rh*arv;}
  const ox=(t.cw-rw)/2, oy=(t.ch-rh)/2, cell=rw/cols;
  const rows=Math.max(1,Math.round(rh/cell)), fnt=Math.ceil(cell*(V.gScale||1.16));
  let data;
  try{
    if(V.blur){
      // pre-blur: sample at half grid resolution, bilinear upscale -> sensor noise gone
      const hc=Math.max(8,cols>>1), hr=Math.max(8,rows>>1);
      off.width=hc; off.height=hr;
      octx.drawImage(el,0,0,vw,vh,0,0,hc,hr);
      off2.width=cols; off2.height=rows;
      o2ctx.imageSmoothingEnabled=true;
      o2ctx.drawImage(off,0,0,hc,hr,0,0,cols,rows);
      data=o2ctx.getImageData(0,0,cols,rows).data;
    } else {
      off.width=cols; off.height=rows;
      octx.drawImage(el,0,0,vw,vh,0,0,cols,rows);
      data=octx.getImageData(0,0,cols,rows).data;
    }
  }catch(e){ return; }
  const n=cols*rows;
  if(t.n!==n){ t.n=n; t.lum=new Float32Array(n); t.ema=new Float32Array(n); t.keep=new Uint8Array(n); t.tmp=new Uint8Array(n);
               t.lbl=new Int32Array(n); t.stk=new Int32Array(n); t.grd=new Float32Array(n);
               t.pKeep=new Uint8Array(n); t.pGi=new Int16Array(n); t.pGi.fill(-1);
               t.emaOk=false; t.lo=null; t.hi=null; }
  // video looped or seeked backwards -> temporal buffer no longer valid
  const ct = el.currentTime!==undefined ? el.currentTime : 0;
  if(ct < t.lastT-0.05) t.emaOk=false;
  t.lastT = ct;
  const lum=t.lum, ema=t.ema, keep=t.keep, tmp=t.tmp, lbl=t.lbl, stk=t.stk, bgw=t.clip.bgw, bgh=t.clip.bgh;
  for(let k=0;k<n;k++){const i=k*4; lum[k]=(0.299*data[i]+0.587*data[i+1]+0.114*data[i+2])/255;}
  // per-cell temporal EMA (Smoothing knob: 0 = off, higher = more stable)
  const eA=1-(V.smooth||0);
  if(!t.emaOk || eA>=1){ ema.set(lum); t.emaOk=true; }
  else for(let k=0;k<n;k++) ema[k]+=(lum[k]-ema[k])*eA;
  const bx = x => Math.min(bgw-1, Math.round(x*(bgw-1)/Math.max(1,cols-1)));
  const byf = y => Math.min(bgh-1, Math.round(y*(bgh-1)/Math.max(1,rows-1)));
  // -- shared isolation pipeline (identical for every variant, runs on smoothed luma) --
  const S=V.stab||0;
  if(t.wd){
    // dark/colored-wall clip (Ruben's gray wall, Shelley's green wall): a
    // luma-only "darker than wall" mask inverts, and "has chroma" fails when
    // the wall itself is saturated. Keep cells whose COLOR sits far from the
    // wall's own color, estimated per frame from the top corner patches /
    // pad bars and EMA-stabilized against hands passing through a corner.
    const pw=Math.max(2,cols>>4), ph=Math.max(2,rows>>4), rs=[], gs=[], bs=[];
    for(let y=0;y<ph;y++) for(const x0 of [0, cols-pw]) for(let x=x0;x<x0+pw;x++){
      const i=(y*cols+x)*4; rs.push(data[i]); gs.push(data[i+1]); bs.push(data[i+2]);
    }
    const m=[median(rs), median(gs), median(bs)];
    if(!t.wRGB) t.wRGB=m; else for(let c=0;c<3;c++) t.wRGB[c]+=(m[c]-t.wRGB[c])*0.2;
    const wr=t.wRGB[0], wg=t.wRGB[1], wb=t.wRGB[2],
          wSat=(Math.max(wr,wg,wb)-Math.min(wr,wg,wb))/255;
    if(wSat<0.08){
      // NEUTRAL gray wall (Ruben): the original chroma+extremes test — wall
      // shading/shadows stay invisible because gray has no chroma. (A plain
      // color-distance mask was tried 7-27 and let the shading through.)
      for(let k=0;k<n;k++){const i=k*4;
        const mx=Math.max(data[i],data[i+1],data[i+2]), mn=Math.min(data[i],data[i+1],data[i+2]);
        keep[k]=((mx-mn)/255>0.10 || ema[k]>0.66 || ema[k]<0.18)?1:0;}
    } else {
      // SATURATED wall (Shelley's green): "has chroma" would keep the wall
      // itself, and absolute RGB distance keeps its lighting falloff. Compare
      // CHROMATICITY (hue, brightness-independent) instead: wall shading has
      // the wall's hue and vanishes; skin/hair/clothes differ in hue and stay.
      // (No "very dark = subject" rescue: deep wall/door shadow dips under
      // any luma floor and reads as an edge strip — Shelley2, 7-27.)
      // thr 0.12: measured on Shelley2 — wall hue variation peaks ~0.07
      // (deeper green on the less-lit side), subject is 0.22+ (hair/skin/shirt)
      const ws=wr+wg+wb+1, wcx=wr/ws, wcy=wg/ws,
            thr=V.wdDist||t.clip.wdDist||0.12;  // knob-tunable mask reach
      for(let k=0;k<n;k++){const i=k*4;
        const s3=data[i]+data[i+1]+data[i+2]+1;
        const dx=data[i]/s3-wcx, dy=data[i+1]/s3-wcy;
        keep[k]=Math.sqrt(dx*dx+dy*dy)>thr?1:0;}
    }
  } else if(S>0){
    // hysteresis: a cell flips its kept-state only when it clearly crosses the cutoff
    for(let k=0;k<n;k++) keep[k]=(t.pKeep[k]?ema[k]<t.solid+S*0.5:ema[k]<t.solid-S*0.5)?1:0;
  } else {
    for(let k=0;k<n;k++) keep[k]=ema[k]<t.solid?1:0;
  }
  for(const z of t.clip.zones){
    const x0=z[0],y0=z[1],x1=z[2],y1=z[3],cap=z[4];
    for(let y=0;y<rows;y++){
      const fy=y/rows; if(fy<y0||fy>y1) continue;
      const by=byf(y);
      for(let x=0;x<cols;x++){
        const k=y*cols+x; if(!keep[k]) continue;
        const fx=x/cols; if(fx<x0||fx>x1) continue;
        const bl=t.bg[by*bgw+bx(x)]/255;
        if(ema[k]>=bl-MASK.bgDelta || (cap!=null && ema[k]>=cap)) keep[k]=0;
      }
    }
  }
  if(t.clip.wr){
    for(let y=0;y<rows;y++){
      const by=byf(y);
      for(let x=0;x<cols;x++){
        const k=y*cols+x;
        if(keep[k] && ema[k]>=MASK.wallCap && t.bg[by*bgw+bx(x)]/255>=t.wall-MASK.wallEps) keep[k]=0;
      }
    }
  }
  tmp.set(keep);
  if(!t.wd){  // fringe-eater assumes a bright wall; skip on dark-wall clips
    for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
      const k=y*cols+x;
      if(!keep[k] || ema[k]<t.solid-MASK.fringe) continue;
      let edge=0;
      for(let dy=-1;dy<=1&&!edge;dy++)for(let dx=-1;dx<=1;dx++){
        const nx=x+dx, ny=y+dy;
        if(nx<0||ny<0||nx>=cols||ny>=rows||!keep[ny*cols+nx]){edge=1;break;}
      }
      if(edge) tmp[k]=0;
    }
  }
  keep.set(tmp);
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
  const minSize=Math.max(6,Math.round(largest*MASK.minComp));
  for(let k=0;k<n;k++) if(keep[k]&&sizes[lbl[k]]<minSize) keep[k]=0;
  // -- tone mapping --
  if(t.lo==null){
    const kept=[]; for(let k=0;k<n;k++) if(keep[k]) kept.push(ema[k]);
    kept.sort((a,b)=>a-b);
    t.lo=kept.length?kept[Math.floor(kept.length*0.05)]:0;
    t.hi=kept.length?kept[Math.min(kept.length-1,Math.floor(kept.length*0.95))]:1;
  }
  const rng=Math.max(0.15,t.hi-t.lo);
  // Sobel magnitude on smoothed luma (contour detection)
  if(V.edge>0){
    const g=t.grd;
    for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
      const x0=x>0?x-1:x, x1=x<cols-1?x+1:x, y0=y>0?y-1:y, y1=y<rows-1?y+1:y;
      const a=ema[y0*cols+x0], b=ema[y0*cols+x], c=ema[y0*cols+x1],
            d0=ema[y*cols+x0], e0=ema[y*cols+x1],
            f=ema[y1*cols+x0], gg=ema[y1*cols+x], h=ema[y1*cols+x1];
      const gx=(c+2*e0+h)-(a+2*d0+f), gy=(f+2*gg+h)-(a+2*b+c);
      g[y*cols+x]=Math.sqrt(gx*gx+gy*gy)/4;
    }
  }
  const isPix=(V.ramp==="PIXEL"), isLF=(V.ramp==="PIXLF"), RAMP=V.ramp,
        rlen=(isPix||isLF)?32:RAMP.length, inv=1/(rlen-1);
  const lfT=V.lfThr!=null?V.lfThr:0.55, pixSide=cell*(V.pixFill!=null?V.pixFill:0.82),
        pixPad=(cell-pixSide)/2, pixA=Math.min(1,0.92*(V.bright||1)),
        lfEdgeOn=isLF&&V.lfEdge!=null&&V.lfEdge>0,
        lfLines=isLF&&V.lfFill!=="blocks",
        LNR=" .·:-=+i1lvtfc";
  const N=(V.bands|0), useQ=N>=3;
  const eThr=0.34-0.30*(V.edge||0);
  ctx.clearRect(0,0,t.cw,t.ch);
  ctx.font=(V.weight||400)+" "+fnt+"px 'Space Grotesk',monospace"; ctx.textBaseline="top";
  const PAL=window.__PAL;
  const sideBase=cell*0.8*((V.gScale||1.16)/1.16);
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const k=y*cols+x;
    if(!keep[k]){ t.pGi[k]=-1; continue; }
    const brv=Math.min(1,Math.max(0,(ema[k]-t.lo)/rng));
    let d=V.dir==="ink"?1-brv:brv;
    // dark-wall clips: ink = distance from the wall's mid-gray, so dark hair
    // AND bright clothing both read dense while midtone skin stays light.
    // V.wdTone="std" opts a clip back into the normal ink mapping (Shelley:
    // the wall-distance map inverted her — skin filled, features emptied)
    if(t.wd && V.wdTone!=="std") d=Math.min(1,Math.abs(brv-0.5)*2);
    d=Math.pow(smooth(d),V.gamma);
    // contour cells bypass quantization and keep the full glyph range
    const isEdge=V.edge>0 && t.grd[k]>=eThr;
    if(isEdge) d=Math.max(d,(V.edge)*Math.min(1,t.grd[k]/0.22));
    const dq=(useQ&&!isEdge)?Math.round(d*(N-1))/(N-1):d;
    let gi=Math.min(rlen-1,Math.round((V.floor+(1-V.floor)*dq)*(rlen-1)));
    // glyph hysteresis: switch only when the value crosses the boundary by the margin
    const pg=t.pGi[k];
    if(S>0 && pg>=0 && gi!==pg && Math.abs(gi-pg)===1){
      const bnd=(((gi>pg?pg+0.5:pg-0.5)*inv)-V.floor)/(1-V.floor);
      if(gi>pg ? dq<bnd+S : dq>bnd-S) gi=pg;
    }
    t.pGi[k]=gi;
    if(gi===0 && !lfEdgeOn) continue;
    let gc=((gi*inv)-V.floor)/(1-V.floor);
    gc=gc<0?0:gc>1?1:gc;
    let a=Math.min(1,(V.bright||1)*(V.minOp+(1-V.minOp)*gc));
    if(V.scan>0&&(y&1)) a*=(1-V.scan);
    const col=V.color==="duo"?(gc>0.55?PAL.bright:PAL.dim):PAL.bright;
    ctx.fillStyle="rgba("+col+","+a.toFixed(2)+")";
    if(isPix){
      const side=sideBase*(0.55+0.45*gc), pad=(cell-side)/2;
      ctx.fillRect(ox+x*cell+pad, oy+y*cell+pad, side, side);
    } else if(isLF){
      // body fill (lines like the original hero, or flat blocks); L/F
      // letterforms take over at the finest details (lfThr) and, optionally,
      // the silhouette boundary where a block/stroke doesn't fit (lfEdge)
      let bnd=0;
      if(lfEdgeOn){
        for(let dy=-1;dy<=1&&!bnd;dy++)for(let dx=-1;dx<=1;dx++){
          const nx=x+dx, ny=y+dy;
          if(nx<0||ny<0||nx>=cols||ny>=rows||!keep[ny*cols+nx]){bnd=1;break;}
        }
      }
      if(gc>=lfT || bnd){
        ctx.fillStyle="rgba("+col+","+Math.min(1,(V.bright||1)).toFixed(2)+")";
        ctx.fillText(((x+y)&1)?"F":"L", ox+x*cell, oy+y*cell);
      } else if(gi>0){
        if(lfLines){
          const li=Math.round(gc*(LNR.length-1));
          if(li>0){
            ctx.fillStyle="rgba("+col+","+a.toFixed(2)+")";
            ctx.fillText(LNR[li], ox+x*cell, oy+y*cell);
          }
        } else {
          ctx.fillStyle="rgba("+col+","+pixA.toFixed(2)+")";
          ctx.fillRect(ox+x*cell+pixPad, oy+y*cell+pixPad, pixSide, pixSide);
        }
      }
    } else ctx.fillText(RAMP[gi], ox+x*cell, oy+y*cell);
  }
  t.pKeep.set(keep);
}
"""
