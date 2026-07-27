#!/usr/bin/env python3
"""Bake page: one fixed-size TRANSPARENT tile per person, the locked engine,
and Marco's merged finals — plus a window.__bake driver so a headless run can
step the master clock frame by frame and capture each tile as PNG-with-alpha.

The capture protocol (bake_run.js):
  await __bake.ready()            -> all 9 videos decoded
  await __bake.setPhase(k, fps)   -> seek every video to its finals window
                                     position at phase k/fps (awaits seeked),
                                     then render every tile in stem order
  __bake.grab(i)                  -> dataURL PNG of tile i (transparent bg)

Pixels are baked WHITE (255,255,255 + per-cell alpha); the site tints
non-white palettes at play time with one cheap composite per frame."""
import json
import pathlib
import subprocess

import render_core as rc

OUT = pathlib.Path(__file__).parent / "bake.html"

rc.CLIPS_DIR = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select")
rc.STEMS = ["Sarah", "Marco", "Nate", "Ruben", "Sheelagh", "Isaiah", "Ryan",
            "Morgan", "Shelley"]

FINALS = json.loads(
    (pathlib.Path(__file__).parent / "lf-select-final-merged-20260727-1212.json")
    .read_text())
assert sorted(FINALS["stems"]) == sorted(rc.STEMS)
END_AUTO = 6.5


def duration(stem: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=duration", "-of", "csv=p=0",
         str(rc.CLIPS_DIR / f"{stem}.mp4")],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip().rstrip(","))


DURS = {s: round(duration(s), 3) for s in rc.STEMS}
BASE = dict(FINALS["settings"]["global"])
O = FINALS["settings"]["perVideo"]

HTML = r"""<title>bake</title>
<style>
__FONTS__
body{margin:0;background:transparent;}
.tile{position:relative;width:432px;height:454px;}
.tile canvas{position:absolute;inset:0;width:100%;height:100%;}
</style>
<div id="tiles"></div>
<script>
const BASE = __BASE__;
const O = __O__;
const STEMS = __STEMS__;
const CLIPS = __CLIPS__;
const DURS = __DURS__;
const END_AUTO = __END_AUTO__;
__CORE__
window.__PAL = {bright:"255,255,255", dim:"148,224,196"};
function eff(i){ const o = O[STEMS[i]]; return o ? Object.assign({}, BASE, o) : BASE; }
const loopLen = Math.max(0.5, BASE.loopLen || 1);
function playWin(i, d){
  const s = eff(i);
  const st = Math.min(s.start||0, Math.max(0, d-0.4));
  const en = (s.end==null || s.end>=END_AUTO)
    ? Math.min(d, st + loopLen)
    : Math.min(Math.max(s.end, st+0.2), d);
  return {st, en, rate: Math.min(4, Math.max(0.25, (en-st)/loopLen))};
}
const holder = document.getElementById("tiles");
const tiles = [];
const loads = [];
CLIPS.forEach((clip,i)=>{
  const el = document.createElement("div"); el.className = "tile";
  const v = document.createElement("video");
  v.muted = true; v.playsInline = true; v.preload = "auto";
  const c = document.createElement("canvas"); el.appendChild(c);
  holder.appendChild(el);
  const t = initTile(clip, c, v);
  tiles.push(t);
  loads.push(new Promise(res => v.addEventListener("loadeddata", res, {once:true})));
  v.src = clip.src; v.load();
});
window.__bake = {
  ready: () => Promise.all(loads).then(()=>{
    tiles.forEach(t=>{ sizeTile(t); resetTone(t); });
    return tiles.length;
  }),
  setPhase: async (k, fps) => {
    const phi = (k / fps) % loopLen;
    await Promise.all(tiles.map((t,i)=>{
      const d = DURS[STEMS[i]];
      const w = playWin(i, d);
      const target = Math.min(w.en - 0.001, w.st + phi * w.rate);
      if (Math.abs(t.src.currentTime - target) < 0.0005) return Promise.resolve();
      const p = new Promise(res => t.src.addEventListener("seeked", res, {once:true}));
      t.src.currentTime = target;
      return p;
    }));
    tiles.forEach((t,i)=>renderTile(t, eff(i)));
    return k;
  },
  grab: (i) => tiles[i].c.toDataURL("image/png"),
};
</script>
"""

html = (HTML
        .replace("__FONTS__", rc.fonts_css())
        .replace("__BASE__", json.dumps(BASE))
        .replace("__O__", json.dumps(O))
        .replace("__STEMS__", json.dumps(rc.STEMS))
        .replace("__CLIPS__", rc.build_clips("video"))
        .replace("__DURS__", json.dumps(DURS))
        .replace("__END_AUTO__", json.dumps(END_AUTO))
        .replace("__CORE__", rc.JS_CORE))
OUT.write_text(html)
print("wrote", OUT, f"{OUT.stat().st_size/1024:.0f} KB",
      f"(loop {BASE['loopLen']}s, {len(rc.STEMS)} tiles)")
