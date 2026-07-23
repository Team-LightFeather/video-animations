#!/usr/bin/env python3
"""Sim v6: PHOTOGRAPHIC mapping (brightness -> density, like the original zoomout look)
+ v5 background isolation (cutoff, guard zones, component filter)."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

SCRATCH = pathlib.Path(__file__).parent
FRAMES = SCRATCH / "frames"
BAKE = SCRATCH / "bake"
STEMS = ["IMG_0949", "IMG_1685", "IMG_2140",
         "IMG_3621", "Niamien", "alex",
         "isaiah", "morgan", "sarah"]
ZONES = {"morgan": [(0.58, 0.0, 1.0, 1.0, None)],
         "sarah": [(0.0, 0.70, 0.34, 1.0, 0.38), (0.0, 0.90, 0.62, 1.0, 0.38)],
         "alex": [(0.0, 0.0, 0.07, 1.0, None)],
         "IMG_0949": [(0.0, 0.0, 0.32, 1.0, 0.40), (0.68, 0.0, 1.0, 1.0, 0.40),
                      (0.32, 0.0, 0.68, 0.16, 0.40)],
         "Niamien": [(0.0, 0.0, 0.16, 1.0, None), (0.84, 0.0, 1.0, 1.0, None),
                     (0.16, 0.70, 0.30, 1.0, None), (0.70, 0.70, 0.84, 1.0, None)]}
MARGINS = {}
WALL_RULE = {"IMG_0949"}
BG_DELTA = 0.13
RAMP = " .·:-=+i1lvtfcLF#"
COLS = 60
BG = (13, 62, 61)
FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
CELL = 9
TILE_W = COLS * CELL


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def smooth(x):
    x = clamp(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def luma_of(img):
    px = img.convert("RGB").load()
    w, h = img.size
    return [[(0.299 * px[x, y][0] + 0.587 * px[x, y][1] + 0.114 * px[x, y][2]) / 255
             for x in range(w)] for y in range(h)], w, h


def luma_grid(img):
    w = COLS
    h = round(img.height * w / img.width)
    return luma_of(img.convert("RGB").resize((w, h)))


def bake_bgmax(stem):
    grids = []
    for f in sorted((BAKE / stem).glob("f*.png")):
        lum, w, h = luma_of(Image.open(f))
        grids.append(lum)
    h, w = len(grids[0]), len(grids[0][0])
    return [[max(g[y][x] for g in grids) for x in range(w)] for y in range(h)], w, h


BGMAX = {s: bake_bgmax(s) for s in STEMS}


def wall_cutoff(lum, w, h, margin=0.18):
    pw, ph = max(2, round(w * 0.16)), max(2, round(h * 0.12))
    tl = sorted(lum[y][x] for y in range(ph) for x in range(pw))
    tr = sorted(lum[y][x] for y in range(ph) for x in range(w - pw, w))
    wall = max(tl[len(tl) // 2], tr[len(tr) // 2])
    return clamp(wall - margin, 0.42, 0.86)


def components(keep, w, h):
    lbl = [[0] * w for _ in range(h)]
    comps = []
    for sy in range(h):
        for sx in range(w):
            if not keep[sy][sx] or lbl[sy][sx]:
                continue
            cells, stack = [], [(sx, sy)]
            lbl[sy][sx] = 1
            while stack:
                x, y = stack.pop()
                cells.append((x, y))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and keep[ny][nx] and not lbl[ny][nx]:
                            lbl[ny][nx] = 1
                            stack.append((nx, ny))
            comps.append(cells)
    return comps


def render_tile(img, stem):
    lum, w, h = luma_grid(img)
    tile = Image.new("RGB", (TILE_W, h * CELL), BG)
    d = ImageDraw.Draw(tile, "RGBA")
    # wall estimated from the BAKED temporal-max grid, not the current frame:
    # transient limbs/shadows can never pollute the estimate
    bgm, bw0, bh0 = BGMAX[stem]
    solid = wall_cutoff(bgm, bw0, bh0, MARGINS.get(stem, 0.18))
    keep = [[lum[y][x] < solid for x in range(w)] for y in range(h)]
    for (x0, y0, x1, y1, cap) in ZONES.get(stem, []):
        bg, bw, bh = BGMAX[stem]
        for y in range(h):
            for x in range(w):
                if not keep[y][x]:
                    continue
                if x0 <= x / w <= x1 and y0 <= y / h <= y1:
                    bl = bg[min(bh - 1, round(y * (bh - 1) / max(1, h - 1)))][min(bw - 1, x)]
                    if lum[y][x] >= bl - BG_DELTA or (cap is not None and lum[y][x] >= cap):
                        keep[y][x] = False
    # WALL-CELL rule: a cell whose baked temporal-max is near the wall estimate is a
    # cell the subject only transits (bare wall shows at some point in the loop). Any
    # mid-bright content there is cast shadow -> only truly dark content may draw.
    if stem in WALL_RULE:
        bgall, bw2, bh2 = BGMAX[stem]
        wall_est = solid + MARGINS.get(stem, 0.18)
        for y in range(h):
            by = min(bh2 - 1, round(y * (bh2 - 1) / max(1, h - 1)))
            for x in range(w):
                if keep[y][x] and bgall[by][min(bw2 - 1, x)] >= wall_est - 0.06 and lum[y][x] >= 0.40:
                    keep[y][x] = False
    # boundary fringe: silhouette-edge cells that are nearly wall-bright are residue
    fringe = []
    for y in range(h):
        for x in range(w):
            if not keep[y][x]:
                continue
            edge = False
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if nx < 0 or ny < 0 or nx >= w or ny >= h or not keep[ny][nx]:
                        edge = True
            if edge and lum[y][x] >= solid - 0.06:
                fringe.append((x, y))
    for x, y in fringe:
        keep[y][x] = False
    comps = components(keep, w, h)
    largest = max((len(c) for c in comps), default=0)
    min_size = max(6, round(largest * 0.18))
    for cells in comps:
        if len(cells) < min_size:
            for x, y in cells:
                keep[y][x] = False
    kept = sorted(lum[y][x] for y in range(h) for x in range(w) if keep[y][x])
    if not kept:
        return tile
    lo = kept[int(len(kept) * 0.05)]
    hi = kept[min(len(kept) - 1, int(len(kept) * 0.95))]
    rng = max(0.15, hi - lo)
    # PHOTOGRAPHIC: brightness -> density. Lit skin/shirts dense+bright; dark
    # features (brows, eyes, mouth, hair) sparse -> they read as accents/holes.
    for y in range(h):
        for x in range(w):
            if not keep[y][x]:
                continue
            tc = smooth((lum[y][x] - lo) / rng)
            gi = min(len(RAMP) - 1, round((0.08 + 0.92 * tc) * (len(RAMP) - 1)))
            a = int(255 * (0.45 + 0.55 * tc))
            d.text((x * CELL, y * CELL), RAMP[gi], font=FONT, fill=(255, 255, 255, a))
    return tile


def strip(stem, times, out):
    tiles = [render_tile(Image.open(FRAMES / f"{stem}_{t}.png"), stem) for t in times]
    th = max(t.height for t in tiles)
    gap = 8
    im = Image.new("RGB", (len(tiles) * TILE_W + (len(tiles) - 1) * gap, th), BG)
    for i, t in enumerate(tiles):
        im.paste(t, (i * (TILE_W + gap), 0))
    im.save(SCRATCH / out)
    print("wrote", out)


strip("IMG_0949", ["0.2", "1.0", "1.8", "2.6", "3.4"], "strip_0949.png")
strip("Niamien", ["0.2", "1.0", "1.8", "2.6", "3.4"], "strip_niamien.png")
strip("sarah", ["0.2", "1.8", "3.4"], "strip_sarah.png")
strip("morgan", ["0.2", "1.0", "1.8", "2.6", "3.4"], "strip_morgan.png")


tiles = [render_tile(Image.open(FRAMES / f"{s}.png"), s) for s in STEMS]
th = max(t.height for t in tiles)
gap = 8
grid = Image.new("RGB", (3 * TILE_W + 2 * gap, 3 * th + 2 * gap), BG)
for i, t in enumerate(tiles):
    grid.paste(t, ((i % 3) * (TILE_W + gap), (i // 3) * (th + gap)))
grid.save(SCRATCH / "grid_v6.png")
print("wrote grid_v6.png")
