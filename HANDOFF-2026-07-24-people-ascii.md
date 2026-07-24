# HANDOFF — People-ASCII / LF Select Command Center
**Date: 2026-07-24** · written for the next Claude session taking over this work.

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

## Current deliverables (all live)

| Artifact | URL | What |
|---|---|---|
| **LF Select Command Center** 🎬 | https://claude.ai/code/artifact/5e39ceea-a914-4d81-895e-30ce4d92dd17 | THE active tuner. 5 finals (Marco, Nate, Ruben, Sheelagh, Isaiah), 3×2 grid, locked LF-Blocks preset as base, synced loops, per-clip start sliders. |
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
  isaiah.MOV 2160×2314, MarcoFinal.jpeg = still of Marco's take).
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
