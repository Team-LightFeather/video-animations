#!/usr/bin/env python3
"""Faithful offline render of the people-ascii effect (matches the JS) so we can
tune params against zoomout.png. Real glyphs (Space Grotesk) on the green band."""
import subprocess, pathlib, sys
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path("/private/tmp/claude-501/-Users-marcoopertti-LF-Website/e8b6147a-7a6a-45e2-a0f9-c91d3a655e86/scratchpad")
LV = BASE / "lv"
FONT = "/Users/marcoopertti/LF-Website/brand-assets/fonts/SpaceGrotesk-VariableFont_wght.ttf"
RAMP = list(" .·:-=+i1lvtfcLF#")
GREEN = (13, 62, 61)      # --bg2
WHITE = (255, 255, 255)

def smooth(x):
    x = 0.0 if x < 0 else 1.0 if x > 1 else x
    return x * x * (3 - 2 * x)

def frame(stem, at=1.5):
    out = pathlib.Path("/tmp/_pv.png")
    subprocess.run(["ffmpeg", "-y", "-ss", str(at), "-i", str(LV / f"{stem}.mp4"),
                    "-frames:v", "1", str(out)], capture_output=True)
    return Image.open(out).convert("RGB")

def _median(vals):
    s = sorted(vals); m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2

def render(stem, cols=60, cell=9, ec=0.15, dil=2, bright=0.82, dark=0.02, floor=0.10,
           span=0.78, solid=None, margin=0.15, mask_edges=False, fill_by_luma=True, at=1.5):
    img = frame(stem, at)
    W, H = img.size
    rows = max(1, round(cols * H / W))
    small = img.resize((cols, rows), Image.BILINEAR).convert("L")
    px = list(small.getdata())
    lum = [p / 255 for p in px]
    n = cols * rows
    # adaptive cutoff: estimate wall brightness from the top corners (almost always wall
    # above the shoulders); take the brighter corner in case one holds a raised arm.
    if solid is None:
        pw, ph = max(2, round(cols * 0.16)), max(2, round(rows * 0.12))
        tl = [lum[y * cols + x] for y in range(ph) for x in range(pw)]
        tr = [lum[y * cols + x] for y in range(ph) for x in range(cols - pw, cols)]
        wall = max(_median(tl), _median(tr))
        solid = min(0.86, max(0.42, wall - margin))
    # focus mask
    mask = [0] * n
    for y in range(rows):
        for x in range(cols):
            k = y * cols + x; c = lum[k]; d = 0
            if x > 0: d += abs(c - lum[k - 1])
            if x < cols - 1: d += abs(c - lum[k + 1])
            if y > 0: d += abs(c - lum[k - cols])
            if y < rows - 1: d += abs(c - lum[k + cols])
            if d > ec: mask[k] = 1
    m = mask
    for _ in range(dil):
        nx = [0] * n
        for y in range(rows):
            for x in range(cols):
                k = y * cols + x
                if m[k]: nx[k] = 1; continue
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < cols and 0 <= yy < rows and m[yy * cols + xx]:
                            nx[k] = 1
        m = nx
    # canvas
    cw, ch = cols * cell, rows * cell
    canvas = Image.new("RGBA", (cw, ch), GREEN + (255,))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, max(6, round(cell * 1.16)))
    for y in range(rows):
        for x in range(cols):
            k = y * cols + x; l = lum[k]
            if 1 - l < floor: continue
            if fill_by_luma:
                if mask_edges:
                    if not (l < solid or (m[k] and l < bright)): continue
                else:
                    if l >= solid: continue     # pure luma cutoff: darker-than-wall = subject
            else:
                if l > bright: continue
                if not (m[k] or l < dark): continue          # original rule
            dk = 1 - l
            tc = smooth(smooth((dk - floor) / span))
            gi = round(tc * (len(RAMP) - 1))
            ch_ = RAMP[gi]
            if ch_ == " ": continue
            a = int((0.45 + 0.55 * tc) * 255)
            draw.text((x * cell, y * cell), ch_, font=font, fill=WHITE + (a,))
    return canvas.convert("RGB")

def montage(stems, **kw):
    imgs = [render(s, **kw) for s in stems]
    w = max(i.width for i in imgs); h = max(i.height for i in imgs)
    cols_m = 3; rows_m = (len(imgs) + cols_m - 1) // cols_m
    sheet = Image.new("RGB", (w * cols_m, h * rows_m), GREEN)
    for i, im in enumerate(imgs):
        sheet.paste(im, ((i % cols_m) * w, (i // cols_m) * h))
    return sheet

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "test"
    rule = (sys.argv[2] != "mask") if len(sys.argv) > 2 else True
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    stems = ["IMG_0949","IMG_1685","IMG_2140","IMG_3621","Niamien","alex","isaiah","morgan","sarah"]
    out = BASE / f"pv_{tag}.png"
    montage(stems, cols=cols, fill_by_luma=rule).save(out)
    print("wrote", out)
