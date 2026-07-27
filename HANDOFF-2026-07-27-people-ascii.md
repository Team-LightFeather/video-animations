# HANDOFF — People-ASCII: finals locked, site integrated, deploy pending
**Date: 2026-07-27** · written for the next Claude session taking over.
Supersedes `HANDOFF-2026-07-24-people-ascii.md` (still valid for tuner-page
rules and history; THIS file is the current state).

## Where things stand (TL;DR)

Marco's people-ascii look is FINAL and INTEGRATED into the real Next.js site
as **pre-baked video** (zero runtime rendering) on branch
**`people-ascii-finals`** of Team-LightFeather/lightfeather-rebrand-next
(tip `2c68595`, pushed, NOT merged). The only missing step is PUBLIC deploy:
creating the `develop` branch (auto-deploys to the sandbox) is blocked for
Claude by the permission classifier — **Marco must run**:

```bash
cd ~/lf-next && git fetch origin && git push origin origin/people-ascii-finals:refs/heads/develop
```

→ deploy.yml auto-runs → **https://next.lightfeathersandbox.com/careers**
(+ /about-us, / join band) goes live in ~3-4 min. Watch the run
(`gh run watch -R Team-LightFeather/lightfeather-rebrand-next`); if the AWS
OIDC step fails ("Not authorized to perform sts:AssumeRoleWithWebIdentity"),
the deploy role's trust policy doesn't list `develop` — infra fix needed
(role arn:aws:iam::063989428983:role/lf-website-next-deploy). Manual
workflow_dispatch on other refs FAILS for this reason (verified).
Production deploys only manually from `main` (deploy-prod.yml) — untouched.

A local review server may still be running: **http://localhost:3777**
(serves the static export from the worktree, see below).

## The look (locked)

- Marco's merged finals: **`lf-select-final-merged-20260727-1212.json`**
  (in `.tmp/people-ascii-mockup/` + the video-animations repo) = his 10:23
  all-hands export + Ruben/Shelley solo-tuner finals merged as per-video
  overrides. One deviation from his saved values: Shelley wdDist 0.08→0.12
  (0.08 let the wall flash on AE dips; sweep-verified, figure identical).
- **Current bake pins cols=120 for everyone** (Marco picked the 120-col look
  from the preview variant; per-person cols overrides stripped, everything
  else from the finals).
- Display order everywhere except the main CC: **Sarah first**
  (`Sarah, Marco, Nate, Ruben, Sheelagh, Isaiah, Ryan, Morgan, Shelley`).
  ⚠️ The MAIN command center keeps `[Marco, Nate, …]` — its localStorage
  overrides are INDEX-keyed; never reorder there.

## Clip states (LF-Website/quality_test_outputs/nv2select/, 432×454 crf20)

- **Sarah = v4** (`sarah_pad4.py`, in video-animations repo): SarahVId.mov,
  ~3.6% zoom, crop top source-y=20 (her raised hands reach row ~49 — v3's
  y=70 crop CLIPPED them, Marco caught it), head aligned to Marco's line
  (content sits 70px down in the 556×584 pre-scale tile). History:
  sarah_pad.py (top pad) → pad2 (14% zoom) → pad3 (+15% down-shift, clipped
  hands) → **pad4 (current)**.
- **Shelley** = Shelley2.MOV via `shelley2_pad.py`: right 44px cropped
  (door + shadow band the mask can't separate), ~20% zoom-out, pads =
  measured wall green 0x49944D, bottom-anchored.
- **Ruben** = 7-24 white-shirt take (gray wall), `--pad`.
- Others: level_clips.py standard/--pad, full takes. Marco's clip from
  IMG_3893.MOV one-off crop.

## Site integration (branch `people-ascii-finals`)

**Architecture: baked video, not live rendering** (Marco's lag report — the
live engine at ~190 cols × 9 tiles ran 6fps; baked = main thread idle):

- `public/people-ascii/baked/{Stem}_{dark,light}.mp4` — 18 clips, ~13 MB,
  864×908 H.264 crf28, each EXACTLY one loop (3.9s = 117 frames @30fps) so
  the nine stay in lockstep; a 200ms drift-sync nudges stragglers.
- **Transparency = blend modes, not alpha video** (alpha was ~5× bigger):
  dark bands play white-on-black with `mix-blend-mode:screen`; the paper
  band plays teal-on-white with `multiply`. Pixel-identical to alpha
  compositing for these mono palettes.
- ⚠️ **Blend placement** (`CareersPeopleHero.tsx`): hero people panels
  (`.cr-hpeople` / module `.people`) are stacking contexts (z-index/mask) —
  the blend goes ON THE PANEL there; in the `.join-art` card (own bg +
  caption) it stays on the grid. Setting it on the videos fails (transparent
  backdrop → baked black/white boxes reappear).
- ⚠️ **Decode suspension**: `display:none` or detached `<video>` gets its
  decode suspended (readyState pins at 1, motion degrades to 5Hz
  seek-jumps). The videos are real rendered elements inside the tiles.
- `CareersPeopleMosaic` keeps its old API (className/pal/count/ticker/rows);
  `pal` presence selects the light variant. Used on /careers hero,
  /about-us hero (pal), home + about-us join bands, styleguide.
- The runtime engine files were REMOVED from the site repo (engine.js,
  clips.ts, original clips) — dead weight; everything regenerates from
  LF-Website.

**Re-bake pipeline** (after any finals/clip change), from
`LF-Website/.tmp/people-ascii-mockup/`:
1. `python3 gen_bake_page.py 120` (argv = cols pin; omit for finals cols)
2. `node <scratchpad>/bake_run.js` — frame-steps bake.html headless
   (playwright + system Chrome), writes PNG-alpha frames to
   `<scratchpad>/bake/{Stem}/f_%03d.png` (bake_run.js is also in the
   video-animations repo)
3. ffmpeg per stem, two variants (exact commands in git log `3542054` /
   the repo's bake_run.js commit):
   dark: black bg overlay → x264 crf28; light: tint 0x0D3E3D → white bg.
4. Copy into `public/people-ascii/baked/`, `npx next build`, commit.

**Worktree**: this session used a git worktree of ~/lf-next at
`<session scratchpad>/lf-next-finals` (node_modules symlinked from
~/lf-next). A NEW session should either `git worktree add` its own from
`origin/people-ascii-finals` or work in ~/lf-next directly (it currently
sits on the old `people-ascii-refined` WIP branch — DON'T build on that;
it's the superseded July-21 algorithm). Local review: `npx next build &&
npx serve out -l 3777` (site is `output: export` — `next start` won't run).

**Headless verification recipe**: playwright from ~/lf-next/node_modules
driving system Chrome, args
`--ignore-gpu-blocklist --enable-gpu-rasterization --use-angle=metal`
(without GPU, fps under-reads and video decode starves). `window.__tiles`
on pages = verification hook. NEVER `pkill "Google Chrome"` — use
`pkill -f playwright_chromiumdev`.

## Live artifacts (all claude.ai/code, republish by URL from new sessions)

| What | URL | Note |
|---|---|---|
| Main tuner (200 cols) 🎨 | https://claude.ai/code/artifact/d17551b1-e748-4e5a-ba58-17f3a24a1b14 | key `lfSelectCC2X`, INDEX-keyed STEMS `[Marco,…]`, Save final button (downloads capability — keep it declared) |
| Finals in-page preview 📄 | https://claude.ai/code/artifact/b6eb0091-c452-44f6-ab4f-e6f1918afa2e | live-engine render of merged finals on both hero layouts |
| 120-col preview 🔳 | https://claude.ai/code/artifact/58d05fea-86a7-4387-b587-4e4869cc3703 | the look Marco picked for the site |
| Shelley solo tuner 🧍 | https://claude.ai/code/artifact/8c6d19fa-c577-4bb0-acf3-8f3c13c41565 | key `lfShelleyCC1`, wdTone/wdDist knobs |
| Ruben solo tuner 🕺 | https://claude.ai/code/artifact/00a867f7-9520-4518-aaa4-b1e92a570ca4 | key `lfRubenCC1`, contrast to 16 |

Older pages (gallery, ink-blocks CC, 5-person select CC) — see the 7-24
handoff. Artifact discipline: same file path in the owning conversation (or
`url` param elsewhere) = same URL; new path = NEW url and orphans
localStorage.

## Engine facts that bite (render_core.py — source of truth in
LF-Website/.tmp/people-ascii-mockup/, copy in video-animations repo)

- wd (dark/colored wall, wall luma <0.55) mask BRANCHES on wall saturation:
  neutral gray (Ruben) = original chroma+extremes test (don't replace — a
  color-distance mask let wall shading through, Marco flagged it);
  saturated (Shelley green) = chromaticity distance > wdDist (default 0.12,
  knob), NO dark-luma rescue.
- wdTone settings field: "wall" (|brv−0.5|×2, Ruben) vs "std" (normal ink —
  Shelley; the wall-distance map INVERTED her: skin filled, features empty).
- Clean SOURCE pads beat mask cleverness: bad pad colors (AE ramp) and
  in-frame objects (doors) rendered as subject — fix at the clip
  (crop/pad with measured wall color), not the mask.
- Bake loop must be INTEGER frames: loopLen 3.9s × 30fps = 117 exactly.

## Git / repos

- Site: Team-LightFeather/lightfeather-rebrand-next — branch
  `people-ascii-finals` @2c68595. Old WIP branch `people-ascii-refined` =
  superseded. main = production (manual deploy only).
- Tools/mockups: Team-LightFeather/video-animations (public) — everything
  pushed through `20b3545` (gen_*.py, render_core, sarah_pad4, shelley2_pad,
  gen_bake_page, bake_run.js, finals JSONs, built tuner/preview pages,
  clips-select/).
- LF-Website repo itself: remote = marco-opertti-lightfeatherio private
  (see 7-24 handoff for account/token rules). Commit as
  `Marco Opertti <marco.opertti@lightfeather.io>`.

## Open items

1. **Marco creates `develop`** → sandbox link goes public (command at top).
   Verify: baked clip 200s at
   https://next.lightfeathersandbox.com/people-ascii/baked/Sarah_dark.mp4.
2. If sandbox look is approved → PR `people-ascii-finals` → `main`, then
   manual prod deploy (their process).
3. Old branch `people-ascii-refined` can be deleted once merged.
4. If Marco re-tunes: Save final on a tuner → merge into the master finals
   JSON (name-keyed) → re-bake (pipeline above) → republish previews.
