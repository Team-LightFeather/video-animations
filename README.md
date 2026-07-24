# Video Animations — LightFeather People-ASCII

ASCII-art video treatment used for the LightFeather careers "dancing people" hero, plus the gallery/tuner page for exploring style variations.

![Preview](preview.png)

## What's here

| File | Purpose |
|---|---|
| `people-ascii-gallery.html` | **The main deliverable** — self-contained gallery + tuner page. 9 embedded clips rendered live as ASCII, 11 style presets, full knob panel (global and per-video). Open directly in a browser — no server needed. |
| `ink-blocks-command-center.html` | **Ink Blocks command center** — dedicated tuner for the LF-Blocks style (Ink Blocks at 44 cols, evolved): one-color pixels for the body, L/F letterforms carrying the detail. Pixel-size changer, L/F detail amount, grouped controls, per-video tuning. |
| `gen_command_center.py` | Builds `ink-blocks-command-center.html` — the base settings live at the top of the script. |
| `people-ascii-preview.html` | **The picked look, locked** — the settings exported from the tuner on 2026-07-23 (54-col pixels · ink, contrast 0.65, brightness 0.75) in the live website's animation colors: the careers-hero mint 3-stop palette on the teal radial (Green) and the about-hero slate palette on cream (Light). `G`/`L` to switch. |
| `people-ascii-preview-2color.html` | **Two-color version** — same locked look reduced to exactly two colors: flat `#0D3E3D` background + solid `#00FFA8` ink at full opacity; square size alone carries the tone. |
| `people-ascii-preview-lf.html` | **LF Blocks preview, locked** — Marco's exact command-center settings (2026-07-23): 72-col one-color blocks, pixel fill 66%, L/F letterform details 25%, contour boost 0.15, contrast 2.5, brightness 0.65. No knobs; green/white toggle. Built by `gen_preview_lf.py`. |
| `gen_preview.py` | Builds both preview pages — locked settings and the website palettes live at the top of the script. |
| `lf-select-command-center.html` | **Select command center** — the newvids2 finals only (Nate, Ruben, Sheelagh, Isaiah) in a 2×2 mosaic, starting on the locked LF Blocks preset. Adds a **Clip length** knob (global and per-video) deciding how much of each video plays before looping. Nate/Ruben were portrait sources — widened to the square tile with wall-colored padding, not cropped. Built by `gen_command_center_select.py` from `clips-select/`. |
| `level_clips.py` | Clip leveling/transcode tool (`--pad` widens narrow sources to the 718:754 tile, `--duration full` keeps the whole take). |
| `clips-select/` | The processed newvids2 finals used by the select command center. |
| `lf-people-ascii-hero.html` | Standalone hero mockup — the effect as it appears in the careers page context. |
| `gen_gallery.py` | Builds `people-ascii-gallery.html` from the clips in `clips/`. |
| `render_core.py` | Shared toolchain — clip encoding, font embedding, the ASCII renderer JS. |
| `gen_harness.py`, `render_preview.py` | Verification harness + headless preview renderer. |
| `build_mockup.py`, `build_mockup_hq.py` | Earlier mockup builders (careers-page context). |
| `clips/` | Processed low-res source clips embedded into the pages. |

## Using the gallery

Open `people-ascii-gallery.html` in any browser. Keyboard shortcuts:

- `1`–`9`, `0` — switch style preset
- `g` / `w` — green / white mode
- Click a tile to tune that video individually; **Copy settings** exports the current knob values as JSON
- Settings persist in localStorage

## Rebuilding

```bash
python3 gen_gallery.py          # regenerates people-ascii-gallery.html from clips/
python3 gen_command_center.py   # regenerates ink-blocks-command-center.html
```

Requires Python 3 with the deps used by `render_core.py` (ffmpeg on PATH for clip re-encoding).

## Live preview

The rendered pages are also published as Claude artifacts (view-only):

- Gallery: https://claude.ai/code/artifact/38d43acd-f535-4b20-a0f3-dd815726da24
- Ink Blocks command center: https://claude.ai/code/artifact/b36aa0e7-9aa2-46c3-bae3-abcf2eab8335
