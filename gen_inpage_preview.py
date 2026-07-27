#!/usr/bin/env python3
"""In-page preview: all nine people rendered with MARCO'S SAVED FINALS
(lf-select-final-20260727-1023.json — Save final export from the 200-col
command center: global look + per-person gamma/cols/start/end), positioned
EXACTLY as the people mosaic sits on the two real site pages that use it:

  1. /careers — green caphero band, people in the right 54% panel
  2. /about   — light (paper) ab-hero band, same right 54% panel, dark-teal px

Layout numbers are lifted 1:1 from lf-next (master-pages.css +
CareersPeopleHero.module.css): .cr-hpeople right:0 width:54%, grid at
top:50%/height:86%/padding:0 28px, 3 cols x 3 rows for 9 clips (the
component's gcols=min(4,ceil(sqrt(9)))=3 rule), gap 12px, tile radius 10px,
left-edge fade masks (13% on /careers per the module, 26% on /about).

Playback = same master clock as the select command center (shared loop, all
videos in lockstep, per-person start/end windows from the finals). Each
person has ONE <video>, drawn to a canvas in each section. No knobs — this
page is a locked preview of Marco's finals."""
import json
import pathlib
import subprocess

import render_core as rc

OUT = pathlib.Path(__file__).parent / "lf-people-inpage-preview.html"

rc.CLIPS_DIR = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select")
rc.STEMS = ["Marco", "Nate", "Ruben", "Sheelagh", "Isaiah", "Ryan", "Morgan",
            "Sarah", "Shelley"]

FINALS = json.loads(
    (pathlib.Path(__file__).parent / "lf-select-final-merged-20260727-1212.json")
    .read_text())
assert FINALS["stems"] == rc.STEMS, "finals stem order must match STEMS"
END_AUTO = 6.5  # end >= this means "auto" (start + loopLen), as in the CC


def duration(stem: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=duration", "-of", "csv=p=0",
         str(rc.CLIPS_DIR / f"{stem}.mp4")],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip().rstrip(","))


DURS = {s: round(duration(s), 2) for s in rc.STEMS}
LOOP_DEFAULT = round(min(DURS.values()), 1)

# BASE = Marco's saved-final GLOBAL settings (2026-07-27); per-person
# overrides ride on top in O (keyed by stem name, exactly as exported).
BASE = dict(FINALS["settings"]["global"])
O = FINALS["settings"]["perVideo"]

HTML = r"""<title>LF People — In-Page Preview</title>
<style>
__FONTS__
*{box-sizing:border-box;}
:root{--green:#0D3E3D;--green2:#0A4F4B;--mint:#00FFA8;--mint20:#2FC189;
  --ink:#302421;--cream:#FFFBF8;--lightmint:#D9EBE6;}
body{margin:0;font-family:'Space Grotesk',system-ui,sans-serif;}
.wrap{max-width:1280px;margin:0 auto;padding:0 56px;}
@media(max-width:1000px){.wrap{padding:0 22px;}}

/* ---- section chip (not part of the real pages; labels the mockup) ---- */
.pagechip{position:absolute;top:18px;right:20px;z-index:3;font-size:11px;font-weight:600;
  letter-spacing:.08em;padding:5px 12px;border-radius:999px;pointer-events:none;}
.caphero .pagechip{background:rgba(0,0,0,.35);color:#B9F5DD;border:1px solid rgba(0,255,168,.3);}
.abhero .pagechip{background:rgba(13,62,61,.06);color:var(--green);border:1px solid rgba(13,62,61,.22);}

/* ================= /careers hero (caphero caphero-careers) ================= */
.caphero{position:relative;overflow:hidden;min-height:100vh;display:flex;align-items:center;
  background:radial-gradient(120% 120% at 70% 45%,#0E4A47 0%,#0D3E3D 45%,#082625 100%);}
.caphero::before{content:'';position:absolute;inset:0;z-index:0;opacity:.16;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%27110%27%20height%3D%27104%27%3E%3Ctext%20x%3D%270%27%20y%3D%2712%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E1F%3EL%3C0%2F1F%3E%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%2725%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E0%2F1F%3EL%3C0%2F1%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%2738%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3EL%3C0%2F1F%3EL%3C0%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%2751%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3EF%3EL%3C0%2F1F%3EL%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%2764%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E%2F1F%3EL%3C0%2F1F%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%2777%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E%3C0%2F1F%3EL%3C0%2F%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%2790%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E%3EL%3C0%2F1F%3EL%3C%3C%2Ftext%3E%3Ctext%20x%3D%270%27%20y%3D%27103%27%20textLength%3D%27110%27%20lengthAdjust%3D%27spacing%27%20font-family%3D%27monospace%27%20font-size%3D%2712%27%20fill%3D%27%232FC189%27%3E1F%3EL%3C0%2F1F%3E%3C%2Ftext%3E%3C%2Fsvg%3E");
  background-size:62px 59px;animation:codeflow 38s linear infinite;}
@keyframes codeflow{to{background-position:0 700px;}}
.caphero-c{position:relative;z-index:2;width:100%;}
.caphero-c>div{max-width:640px;}
.bkc-d{display:inline-flex;align-items:center;gap:7px;border:1.5px solid rgba(0,255,168,.55);
  color:#fff;border-radius:100px;padding:7px 15px;font-weight:600;font-size:13px;
  text-decoration:none;font-family:system-ui,sans-serif;}
.eyebrow2{font-family:'Space Grotesk';font-weight:500;font-size:13px;letter-spacing:.28em;
  text-transform:uppercase;color:var(--mint20);margin-bottom:20px;}
.caph-title{font-family:'Space Grotesk';font-weight:700;font-size:clamp(40px,5.4vw,68px);
  line-height:1.02;letter-spacing:-.02em;color:#fff;max-width:13ch;min-height:1.05em;margin:0;}
.caph-title b{background:linear-gradient(100deg,#1E6F63,#2FC189 18%,#00FFA8 34%,#EAFBF4 49%,#FFFFFF 52%,#EAFBF4 55%,#00FFA8 70%,#2FC189 86%,#1E6F63);
  background-size:280% 100%;-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent;animation:sheen 4.5s linear infinite;}
@keyframes sheen{to{background-position:280% 0;}}
.caph-sub{color:var(--lightmint);font-size:clamp(16px,1.3vw,19px);line-height:1.6;
  max-width:500px;margin:24px 0 32px;}
.btn{display:inline-flex;align-items:center;gap:10px;border-radius:100px;padding:15px 30px;
  font-weight:600;font-size:15px;text-decoration:none;border:none;font-family:system-ui,sans-serif;}
.btn-mint{background:var(--mint);color:var(--green);}
.btn-dark{background:var(--green);color:#fff;}
.btn-outline{background:transparent;color:var(--green);border:1.5px solid var(--green);}
.mb16{margin-bottom:16px;}.mb18{margin-bottom:18px;}

/* right-side people panel (.cr-hpeople) — exact site numbers */
.cr-hpeople{position:absolute;right:0;top:0;bottom:0;width:54%;z-index:1;overflow:hidden;
  pointer-events:none;}
.caphero .cr-hpeople{-webkit-mask-image:linear-gradient(90deg,transparent,#000 13%);
  mask-image:linear-gradient(90deg,transparent,#000 13%);}
.abhero .cr-hpeople{-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 26%);
  mask-image:linear-gradient(90deg,transparent 0,#000 26%);}
.cr-hgrid{position:absolute;top:50%;transform:translateY(-50%);left:0;right:0;height:86%;
  padding:0 28px;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:12px;}
.cr-ptile{position:relative;overflow:hidden;border-radius:10px;}
.cr-ptile canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}
@media(max-width:960px){.cr-hpeople{width:100%;opacity:.34;}
  .abhero .cr-hpeople{opacity:.3;}}

/* ================= /about hero (ab-hero ab-hero-lightppl) ================= */
.abhero{position:relative;overflow:hidden;background:var(--cream);min-height:86vh;
  display:flex;align-items:center;}
.ab-hero-c{position:relative;z-index:2;width:100%;}
.ab-hero-inner{max-width:620px;margin:0;padding:56px 0 72px;}
.bkc{display:inline-flex;align-items:center;gap:7px;border:1.5px solid var(--mint20);
  color:var(--green);border-radius:100px;padding:7px 15px;font-weight:600;font-size:13px;
  text-decoration:none;font-family:system-ui,sans-serif;}
.ab-title{position:relative;font-size:clamp(40px,5.4vw,68px);font-weight:700;line-height:1.05;
  color:var(--green);margin:8px 0 18px;max-width:1060px;font-family:'Space Grotesk';letter-spacing:-.02em;}
.ab-sub{font-size:19px;line-height:1.7;max-width:540px;color:var(--ink);margin:0;}
.ab-btns{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px;}
</style>

<!-- ============ 1 · /careers hero ============ -->
<section class="caphero">
  <span class="pagechip">as on /careers</span>
  <div class="cr-hpeople" aria-hidden="true"><div class="cr-hgrid" id="gridCareers"></div></div>
  <div class="wrap caphero-c">
    <div>
      <div class="mb16"><a class="bkc-d" href="#">&larr; Home</a></div>
      <div class="eyebrow2">Careers &middot; Now hiring</div>
      <h1 class="caph-title">Do serious work that <b>matters</b>.</h1>
      <p class="caph-sub">LightFeather builds the software, data platforms, and secure systems
        federal agencies depend on. Work on hard problems with a team that values technical
        depth and operational excellence.</p>
      <div><a class="btn btn-mint" href="#">Browse Open Roles</a></div>
    </div>
  </div>
</section>

<!-- ============ 2 · /about hero ============ -->
<section class="abhero">
  <span class="pagechip">as on /about</span>
  <div class="cr-hpeople" aria-hidden="true"><div class="cr-hgrid" id="gridAbout"></div></div>
  <div class="wrap ab-hero-c">
    <div class="ab-hero-inner">
      <div class="mb18"><a class="bkc" href="#">&larr; Home</a></div>
      <div class="eyebrow2">About us</div>
      <h1 class="ab-title">We make complexity predictable.</h1>
      <p class="ab-sub">Engineering, analytics, and program delivery your mission can count on.</p>
      <div class="ab-btns">
        <a class="btn btn-dark" href="#">Request a Walkthrough</a>
        <a class="btn btn-outline" href="#">Explore the Mission</a>
      </div>
    </div>
  </div>
</section>

<script>
const BASE = __BASE__;
const O = __O__;          // Marco's per-person finals, keyed by stem name
const END_AUTO = __END_AUTO__;
const CLIPS = __CLIPS__;
const STEMS = __STEMS__;
__CORE__
function eff(i){ const o = O[STEMS[i]]; return o ? Object.assign({}, BASE, o) : BASE; }
/* pixel palettes: white pixels on the green band, dark-teal on the paper band */
const PAL_GREEN = {bright:"255,255,255", dim:"148,224,196"};
const PAL_LIGHT = {bright:"13,62,61",   dim:"96,132,127"};
window.__PAL = PAL_GREEN;

const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion:reduce)").matches;

/* one <video> per person; a canvas tile in EACH section shares it */
const videos = [], tiles = [];
function addTile(grid, clip, v, pal, idx){
  const el = document.createElement("div"); el.className = "cr-ptile";
  const c = document.createElement("canvas"); el.appendChild(c);
  const t = initTile(clip, c, v);
  t.pal = pal; t.el = el; t.idx = idx;
  grid.appendChild(el); tiles.push(t);
  return t;
}
const gC = document.getElementById("gridCareers");
const gA = document.getElementById("gridAbout");
CLIPS.forEach((clip,i)=>{
  const v = document.createElement("video");
  v.muted = true; v.loop = true; v.autoplay = true; v.playsInline = true;
  v.setAttribute("muted",""); v.setAttribute("playsinline","");
  videos.push(v);
  const tc = addTile(gC, clip, v, PAL_GREEN, i);
  const ta = addTile(gA, clip, v, PAL_LIGHT, i);
  v.addEventListener("loadeddata", ()=>{
    if(reduce){ [tc,ta].forEach(t=>{ sizeTile(t); drawTile(t); }); try{v.pause();}catch(e){} }
    else { v.play().catch(()=>{}); [tc,ta].forEach(sizeTile); }
  });
  v.src = clip.src; v.load();
});
window.__tiles = tiles;  // for headless verification scripts

function drawTile(t){ window.__PAL = t.pal; renderTile(t, eff(t.idx)); }

/* master clock — same engine as the select command center, with each
   person's start/end window from the finals (rate auto-derives, so all
   nine loop in lockstep exactly as tuned) */
const t0 = performance.now();
function loopLen(){ return Math.max(0.5, BASE.loopLen || 1); }
function playWin(i, d){
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
  videos.forEach((v,i)=>{
    const d = v.duration;
    if(!d || v.readyState<2) return;
    const w = playWin(i, d);
    if(Math.abs(v.playbackRate - w.rate) > 0.01) v.playbackRate = w.rate;
    const target = Math.min(w.en - 0.03, w.st + phi*w.rate);
    if(Math.abs(v.currentTime - target) > 0.13){
      try{ v.currentTime = target; }catch(e){}
    }
  });
}
setInterval(syncClock, 200);
let last=0;
function loop(ts){ if(ts-last>85){ last=ts; tiles.forEach(drawTile); } requestAnimationFrame(loop); }
if(!reduce) requestAnimationFrame(loop);
addEventListener("resize", ()=>tiles.forEach(sizeTile));
addEventListener("click", ()=>videos.forEach(v=>{ if(v.paused && !reduce) v.play().catch(()=>{}); }));
</script>
"""

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__BASE__", json.dumps(BASE))
        .replace("__O__", json.dumps(O))
        .replace("__END_AUTO__", json.dumps(END_AUTO))
        .replace("__STEMS__", json.dumps(rc.STEMS))
        .replace("__CLIPS__", rc.build_clips("video"))
        .replace("__CORE__", rc.JS_CORE))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB",
      f"(loop default {LOOP_DEFAULT}s)")
