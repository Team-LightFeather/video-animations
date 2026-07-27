# HANDOFF — People-ASCII / LF Select Command Center
**Date: 2026-07-24** · written for the next Claude session taking over this work.

> **⚠️ SUPERSEDED for current state: read `HANDOFF-2026-07-27-people-ascii.md`
> FIRST** (finals locked, site integrated as baked video, deploy pending).
> This file remains the reference for tuner-page rules (localStorage keys,
> STEMS ordering, artifact URLs) and the full history.

## What this project is

Marco is iterating on an ASCII-video treatment ("people-ascii") of LightFeather
teammates dancing, for the website. The current focus is the **LF Select Command
Center** — a live tuner page with the five final videos, which Marco is using to
dial in the final look. When he's happy he exports settings and we lock them
into a knob-free "preview" page.

## ⚠️ RULE #1 — DO NOT LOSE MARCO'S TUNED SETTINGS

Marco tunes in his browser on the artifact page. His settings (global knobs +
per-video overrides for each person) are saved in **his browser's
localStorage**, key **`lfSelectCC2`**, on the artifact origin. They exist
NOWHERE else until he clicks **Copy settings** and pastes the JSON. He does not
want to re-enter per-person tweaks. Therefore:

1. **Never rename the localStorage key** (`lfSelectCC2` in
   `gen_command_center_select.py`). Bumping it orphans all his saved tuning.
   (It was bumped once deliberately — `lfInkBlocksCC`→`CC2` — to force a revert;
   don't do that again unless Marco explicitly wants stored settings discarded.)
2. **Never rename settings fields** (`cols, pixFill, lfFill, lfThr, gScale,
   weight, edge, lfEdge, gamma, bright, floor, minOp, smooth, stab, blur,
   loopLen, start, end`, …). Restore does `Object.assign({}, BASE, saved)` — 
   saved values override BASE by field name, and per-video overrides in `O`
   are keyed by tile index. Renaming a field silently drops his value; 
   **reordering STEMS breaks per-video overrides** (they're index-keyed), so
   keep STEMS order: `["Marco","Nate","Ruben","Sheelagh","Isaiah"]`.
3. **Always republish to the SAME artifact URL** (file
   `.tmp/people-ascii-mockup/lf-select-command-center.html` → artifact
   `https://claude.ai/code/artifact/5e39ceea-a914-4d81-895e-30ce4d92dd17`,
   favicon 🎬). From a new conversation pass that URL as the Artifact tool's
   `url` param. A new URL = new origin = his localStorage is left behind.
4. Rebuilding/republishing the page is SAFE for his settings as long as 1–3
   hold (localStorage survives redeploys of the same artifact).
5. **Before any risky change, ask Marco to click "Copy settings" and paste the
   JSON** (or screenshot the panel — settings have been read off screenshots
   before, see `people-ascii-preview-lf.html`). Once you have the JSON, bake it
   into a locked preview (pattern: `gen_preview_lf.py`) and/or make it the new
   `BASE` in `gen_command_center_select.py` — putting his values in BASE is
   harmless (saved settings just re-assert the same values).

Settings JSON shape (what Copy settings produces):
`{"global":{...all fields...},"perVideo":{"Nate":{"start":1.2},...}}`
— perVideo is keyed by stem NAME in the export (index-keyed only internally).

**MARCO'S FINALS — CANONICAL = `lf-select-final-merged-20260727-1212.json`**
(in `.tmp/people-ascii-mockup/` and the video-animations repo): the 10:23
all-hands export with Ruben's and Shelley's 12:12 solo-tuner finals merged
in as per-video overrides (Ruben: cols 186, gamma 8.75, bright .55, gScale
1.3, smooth .3, window 1.1–5.195; Shelley: cols 192, gamma 4.9, minOp .25,
bright .6, wdTone "std"). ⚠️ One deviation from his saved file: Shelley's
wdDist saved as 0.08 but merged as **0.12** — at 0.08 the wall flashed
through on AE dips (his report; sweep-verified: 7027 junk cells worst phase
at 0.08, zero at 0.12, figure identical). Marco signed off Ruben + Shelley
as DONE 7-27 (Ruben also sweep-verified: zero junk cells full-loop). Baked
into the in-page preview (`gen_inpage_preview.py` →
https://claude.ai/code/artifact/b6eb0091-c452-44f6-ab4f-e6f1918afa2e 📄).
Newer Save-final files supersede — re-merge + re-bake.
**Preview perf (7-27, was 6fps → now 68fps):** one master render per person
(about tile = source-in recolor blit, pixel-exact for MONO color only — if
duo/per-cell color ever returns, the blit must go), IntersectionObserver
gates sections + pauses videos, rAF renders round-robin in a ~7ms budget.
**Preview display order = Sarah first** — safe because the preview is
name-keyed; the MAIN CC stays `[Marco,Nate,…]` (index-keyed localStorage).

## Current deliverables (all live)

| Artifact | URL | What |
|---|---|---|
| **LF Select Command Center** 🎬 | https://claude.ai/code/artifact/5e39ceea-a914-4d81-895e-30ce4d92dd17 | THE active tuner. 5 finals (Marco, Nate, Ruben, Sheelagh, Isaiah), 3×2 grid, locked LF-Blocks preset as base, synced loops, per-clip start sliders. |
| Select CC — 120-col range 🔲 | https://claude.ai/code/artifact/67f697ba-4d66-4102-878b-da878a67dcad | Identical clone of the select CC (same BASE, 72 cols) but the Pixel size slider goes past 96 up to 120 cols. Own localStorage key `lfSelectCC2BP` — can never touch the original CC's tuning. `gen_command_center_select_bigpix.py`. |
| Select CC — 200 cols + brand colors 🎨 | https://claude.ai/code/artifact/d17551b1-e748-4e5a-ba58-17f3a24a1b14 | Same tuner with Pixel size up to 200 cols AND pixel color pickable from the brand palette (tokens.css): new `pxc` field ("auto"=G/W mode, else brand hex), global Pixel color swatches + always-visible per-person "Clip colors" rows. Own key `lfSelectCC2X`. **Nine people — Ryan, Morgan, Sarah, Shelley appended at END of STEMS** (`…,"Ryan","Morgan","Sarah","Shelley"]`, mosaic 3×3, top-aligned, 560px two-column panel) so index-keyed overrides don't shift; Ruben's clip = the 7-24 white-shirt replacement take. Sarah = SarahVId.mov top-padded (sarah_pad.py — never crop). Shelley = Shelley.MOV 720×808 GREEN wall, --pad, 3.2s = shortest take → loop default 3.2s. **Color is GLOBAL-ONLY** (7-27): Clip colors section removed, pxc always writes to G, stale per-video pxc ignored/stripped from exports (saved localStorage untouched). **Save final button** (7-27): `window.claude.downloads.save()` exports `lf-select-final-YYYYMMDD-HHMM.json` to Marco's Downloads — that file is the canonical handback; bake it into BASE + a locked preview. Artifact is published with `capabilities: {downloads: true}` — KEEP passing that on republish (or omit the field entirely; `{}` clears it and kills the button). Only this page has the new roster so far. `gen_command_center_select_200.py`. |
| In-page preview (careers/about) 🖥️ | https://claude.ai/code/artifact/5381c807-4c93-4f5c-8b03-3feaa127c2c0 | The 5 finals animated in 1:1 replicas of the two site heroes that use the mosaic: /careers green band (white px) and /about paper band (dark-teal px). Site-exact `.cr-hpeople`/grid geometry, locked BASE preset, no knobs. `gen_inpage_preview.py`. |
| Ink Blocks Command Center 🎛️ | https://claude.ai/code/artifact/b36aa0e7-9aa2-46c3-bae3-abcf2eab8335 | Earlier 9-clip tuner (original clip set). localStorage key `lfInkBlocksCC2`. |
| Gallery (11 presets) 🟩 | https://claude.ai/code/artifact/38d43acd-f535-4b20-a0f3-dd815726da24 | Version-3 family + 3.10 LF Blocks preset. Key `lfAsciiTunerV3`. |
| LF Blocks preview (locked) 🧱 | https://claude.ai/code/artifact/851774a5-e44b-4045-946b-d97ec0145b18 | Knob-free preview of Marco's 2026-07-23 settings (9 original clips). |

**GitHub repo (public, shared with team):**
https://github.com/Team-LightFeather/video-animations — everything is pushed
here after each change (latest commit at handoff: `5faeb73`).

## The look, as Marco has locked it so far

- **Blocks-first LF style** (`ramp:"PIXLF"`, `lfFill:"blocks"`): flat one-color
  square pixels for the body; L/F letterforms at the strongest detail cells
  (`lfThr`) and optionally the silhouette edge (`lfEdge`). Marco REJECTED a
  lines-based default ("go backwards its gotten a lot worse") — lines remain
  only as the Fill-style option. Don't re-default to lines or heavy smoothing.
- Locked 2026-07-23 preset (= select CC's BASE): 72 cols, pixFill 0.66,
  lfThr 0.75 (25% detail), gScale 1.28, weight 700, edge 0.15, lfEdge 0,
  gamma 2.5, bright 0.65, floor 0, minOp 0.10, smooth/stab/blur 0, mono.
- White mode background = brand token `--lf-cream` **#FFFBF8** ("paper white",
  from brand-assets/tokens.css). NOT the old cream #F1ECE0.
- Contrast slider range is 0.4–8 (Marco asked twice for more headroom).

## Dark/colored-wall clips (render_core `wd` mode, rewritten 7-27)

`initTile` flags `wd` when baked wall luma < 0.55 (Ruben's gray wall, Shelley's
green wall). The wd mask samples the wall's RGB each frame (median of top
corner patches / pad bars, EMA 0.2) and then BRANCHES on wall saturation:
- **Neutral gray wall** (wSat<0.08, Ruben): the ORIGINAL chroma+extremes test
  (`sat>0.10 || ema>0.66 || ema<0.18`). Do not replace it with color-distance:
  tried 7-27, it let the wall's shading through and Marco called it out.
- **Saturated wall** (Shelley's green): keep = CHROMATICITY distance from the
  wall hue > `clip.wdDist` (default 0.12; measured on Shelley2 — wall hue
  variation peaks ~0.07, subject is 0.22+). NO dark-luma rescue: deep wall/
  door shadow dips under any luma floor and reads as an edge strip.
  Shelley's ACTIVE clip = Shelley2.MOV (7-27, zoomed out 20%): crop the right
  44px (shadow+door band the mask can't separate — her hair connects it to
  the figure so minComp can't drop it), pad with measured wall green
  0x49944D, all vertical pad on TOP (bottom-anchored). See `shelley2_pad.py`.
wd tone mapping: ink = |brv−0.5|×2 UNLESS `wdTone:"std"` (settings field,
7-27) opts the clip back into the normal d=1−brv ink map — the wall-distance
map INVERTED Shelley (skin filled, features emptied; Marco's report). Ruben
stays on "wall". `wdDist` is also a settings field now (knob-tunable).
**Shelley solo tuner** 🧍 https://claude.ai/code/artifact/8c6d19fa-c577-4bb0-acf3-8f3c13c41565
(`gen_shelley_tuner.py` → `lf-shelley-tuner.html`, key `lfShelleyCC1`,
downloads capability): single-tile CC clone with Tone mapping + Mask reach
knobs, BASE = his finals with wdTone std/gamma 2.7. His Save final there
emits `lf-shelley-final-*.json` → merge as Shelley's per-video overrides in
the main finals (incl. wdTone!) and re-bake the in-page preview.
**Ruben solo tuner** 🕺 https://claude.ai/code/artifact/00a867f7-9520-4518-aaa4-b1e92a570ca4
(`gen_ruben_tuner.py` → `lf-ruben-tuner.html`, key `lfRubenCC1`, downloads
capability): same page for Ruben, Contrast range extended to 16 (his finals
had gamma 7.2 pinned at the old max 8), wdTone defaults "wall". Save final
→ `lf-ruben-final-*.json`, merge like Shelley's.
⚠️ Clean SOURCE pads matter more than mask cleverness: Shelley's first encode
had near-black pad bars (sample_wall hit an iPhone auto-exposure ramp) plus a
brown door at x≥676 — both rendered as "subject". Fixed in the CLIP
(`shelley_pad.py`: crop the door column — she never reaches it — and pad with
the measured wall green 0x4A974F). If a wd clip shows edge garbage, check the
clip's pads/edges before touching the mask.

## Sync engine (select CC) — how playback works

One master clock; every video loops on the same period:
- **Loop length** (global-only, default 3.7s = Nate's take, the shortest).
- Per video **Start/End** choose the slice of that person's take; its
  `playbackRate` auto-derives as `(end−start)/loopLen`, so any adjustment keeps
  all five looping in lockstep. **Speed** knob is a two-way view (it moves End).
- End="auto" means start+loopLen at 1× (capped at the clip's end).
- **Clip start times** section: five always-visible sliders (one per person)
  writing each video's `start` override directly.
- Implementation: `syncClock()` drives `currentTime` toward
  `start + phase×rate` (drift >0.13s → seek); phase wrap re-syncs everyone.
  `window.__tiles` is exposed for headless verification.

## Source material & clip processing

- Raw finals: `LF-Website/newvids2/` (NateFinal.mov 720×990 portrait,
  RubenFInal.MOV 720×878 portrait, SheelaghsFinal.MOV 714×714,
  isaiah.MOV 2160×2314, MarcoFinal.jpeg = still of Marco's take,
  `Ryan Motion Clip - Darker Shirt.mov` 1080×1302 → Ryan.mp4, full 6.7s,
  added 2026-07-24 pm. Marco first said square it without cropping (--pad),
  then asked for a ~15-20% zoom: one-off `crop=922:1112:79:60` + wall-color
  pad to 1058 + Lanczos 432 (≈17% zoom, y=60 keeps head clearance) — script
  ryan_zoom.py in the video-animations repo.
  `ruben.MOV` 720×778 = REPLACEMENT take of Ruben (white shirt, DARK gray
  wall) and `morgan.mov` 720×792 = Morgan (new person), both added 15:34,
  both --pad --duration full. ⚠️ Ruben's dark wall inverted the mask; fixed
  with a gated dark-wall mode in render_core JS_CORE (initTile `wd:wall<0.55`;
  keep = chroma>0.10 OR luma>0.66 OR luma<0.18; fringe-eater skipped; tone
  d=|brv−0.5|×2 so white shirt AND dark hair read dense). Light-wall clips
  are byte-identical in behavior. Only the 200-col page is rebuilt with it —
  other pages pick it up whenever their gen_*.py is rerun.).
  Marco's actual new video was `~/Downloads/IMG_3893.MOV` (portrait 1080×1920
  after rotation metadata).
- Processed clips (432×454 tile, crf20, full length):
  `LF-Website/quality_test_outputs/nv2select/` — {Marco,Nate,Ruben,Sheelagh,Isaiah}.mp4
- Tool: `LF-Website/tools/level_clips.py`
  - standard: top-anchored 718:754 crop → 432 wide, Lanczos, x264 slow.
  - `--pad`: for sources NARROWER than the tile (Nate, Ruben) — Marco said
    **never crop these**; widen with FLAT WALL-COLORED borders (color sampled
    from the video's brighter top corner). ⚠️ edge-smear padding was tried and
    FAILS: when arms touch the frame edge they smear into solid bars.
  - `--duration full` keeps the whole take (needed for start/end/speed range).
  - Marco's IMG_3893: one-off centered crop `crop=1080:1134:0:360` (top-anchored
    would cut off his pointing hand; y=360 matches MarcoFinal.jpeg framing) —
    done by importing level_clips and overriding FILTER, see git log `5faeb73`.

## Code map (source of truth: `LF-Website/.tmp/people-ascii-mockup/`)

- `render_core.py` — THE shared engine: VARIANTS presets, mask pipeline
  (baked-bg zones, wall rule), stabilization, and JS_CORE incl. the PIXLF
  draw path. `rc.CLIPS_DIR`/`rc.STEMS` are module globals — the select
  generator overrides them before `build_clips("video")`.
- `gen_command_center_select.py` → `lf-select-command-center.html` (ACTIVE).
- `gen_command_center.py` → `ink-blocks-command-center.html` (9 clips).
- `gen_gallery.py` → `people-ascii-gallery.html`; `gen_harness.py` →
  `harness.html` (still-frame test page, `?v=N&m=white` single variant).
- `gen_preview.py` (other session's locked previews), `gen_preview_lf.py`
  (locked LF Blocks preview) — the pattern for baking exported settings.
- Everything is regenerated by running the gen_*.py from that directory
  (needs ffmpeg/ffprobe on PATH; fonts from ~/lf-next/public/fonts).

## Verification workflow (IMPORTANT — raw headless Chrome HANGS)

`chrome --headless --screenshot` hangs forever on this machine (even
about:blank). Use **playwright from `~/lf-next/node_modules`** driving system
Chrome; H.264 clips DO decode there. Pattern (scripts in this session's
scratchpad, shoot*.js):

```js
const { chromium } = require('/Users/marcoopertti/lf-next/node_modules/playwright');
const browser = await chromium.launch({ headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
// ... page.goto(file://...), waitForTimeout(6000) for videos, screenshot ...
process.exit(0);           // browser.close() hangs — exit hard, then:
// pkill -f playwright_chromiumdev   (NEVER pkill "Google Chrome" broadly!)
```

## Git / accounts

- Shared repo: fresh clone in scratchpad with
  `gh auth token -u marco-opertti-lightfeatherio` embedded in the URL
  (do NOT `gh auth switch` — other sessions run concurrently), additive
  changes, `git pull --rebase` before push. Commit as
  `Marco Opertti <marco.opertti@lightfeather.io>`.
- LF-Website repo remote = marco-opertti-lightfeatherio/lf-website-marco-2026
  (private): push with that account's token too (Marcomercader gets
  "Repository not found").
- gh accounts: Marcomercader (active), marco-opertti-lightfeatherio (owns the
  repos, member of Team-LightFeather), LightFeatherIO-ChallengeEval.

## SITE INTEGRATION (7-27) — branch `people-ascii-finals`

The finals are integrated into the REAL site
(Team-LightFeather/lightfeather-rebrand-next, branch **people-ascii-finals**
off main @f9b06f6, NOT merged), and after Marco's lag report the runtime
engine was replaced with **BAKED VIDEO** (commit 3542054): the treatment is
pre-rendered offline and `CareersPeopleMosaic` just plays 9 small H.264
clips — zero runtime pixel work. Key facts:
- Bake pipeline (all in LF-Website/.tmp/people-ascii-mockup + repo):
  `gen_bake_page.py` → bake.html (engine+finals, __bake driver) →
  `bake_run.js` frame-steps ONE exact loop (3.9s = 117 frames @30fps) into
  PNG-alpha frames → ffmpeg flattens to
  `public/people-ascii/baked/{Stem}_{dark,light}.mp4` (crf 28, ~15 MB/18).
- Transparency = BLEND MODES, not alpha video (~5× smaller): dark bands play
  white-on-black with mix-blend-mode:screen, the paper band plays
  teal-on-white with multiply — pixel-identical to alpha for these palettes.
- ⚠️ Blend placement: hero panels (.cr-hpeople / module .people) are
  stacking contexts → blend goes ON THE PANEL; in the join-art card (own
  bg/content) it stays on the grid. On the VIDEOS it fails (transparent
  backdrop → tile boxes reappear).
- All clips share one exact duration; a 200ms drift-sync keeps lockstep.
- Re-bake after new finals: `gen_bake_page.py [cols]` → bake_run.js → the
  two ffmpeg variant encodes → replace baked/*.mp4. CURRENT bake (7-27):
  **cols pinned to 120** (Marco picked the 120-col look; per-person cols
  stripped) and **Sarah's clip zoomed in 14%** (`sarah_pad2.py`,
  bottom-anchored crop). Sandbox deploy ON HOLD per Marco; `develop`
  doesn't exist yet and the OIDC deploy role rejects other refs.
- Branch `people-ascii-refined` (WIP cb291b2, 7-21) is the OLD algorithm —
  superseded.

## Likely next steps

1. Marco finishes tuning → **Copy settings JSON** → bake a locked preview
   (`gen_preview_lf.py` pattern; include the playback fields — a locked page
   must replicate the sync engine's loopLen/start/end behavior, not just look).
2. Possibly port the locked look into the Next.js site
   (`~/lf-next`, careers hero = `src/app/_pages/PeopleGrid.tsx`; see memory
   notes `site-now-nextjs`, `careers-people-ascii-effect`).
3. If new/replacement videos appear in `newvids2/`: process with
   `level_clips.py` (--pad for narrow sources), drop into
   `quality_test_outputs/nv2select/`, keep STEM order stable (append new people
   at the END so index-keyed per-video settings don't shift), rebuild, republish
   same URL, push.

## Memory

Long-lived facts also live in auto-memory:
`video-animations-repo`, `people-ascii-gallery`, `careers-people-ascii-effect`,
`never-pkill-chrome`, `site-now-nextjs`. Update them if you change anything
structural.
