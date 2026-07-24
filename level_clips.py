#!/usr/bin/env python3
"""Level + transcode the people-ascii clips (quality-fixed encode).

Replaces the ad-hoc v3 command recorded in .tmp/HANDOFF-READY.md:

    -vf scale=718:-2,crop=718:754:0:0,scale=432:-2   (libx264, crf 30, preset medium)

That starved the encoder (~170 kbps) and resampled twice with the default
bicubic scaler. This script keeps the exact same leveling geometry
(uniform 718:754 aspect crop from the top, delivered at 432x454) but:

  * crops at SOURCE resolution and downscales ONCE, with Lanczos
  * encodes with libx264 crf 18 preset slow (visually transparent)
  * carries the source color metadata (matrix/primaries/transfer/range)
    explicitly through the encode

Usage:
    python3 tools/level_clips.py -o OUTDIR SOURCE.MOV [SOURCE2.MOV ...]

Output name = source stem + .mp4 (Niamien_IMG_0947 shortens to Niamien,
matching the existing lv/ naming).
"""
import argparse
import json
import pathlib
import subprocess
import sys

# Same geometry as the approved leveling spec: every tile is a 718:754-aspect
# crop anchored at the top of the frame, delivered at 432px wide.
FILTER = r"crop=iw:min(ih\,round(iw*754/718)):0:0,scale=432:-2:flags=lanczos"
DURATION = "4"  # seconds, as approved for the mockup (v3)


def probe_color(src: pathlib.Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries",
         "stream=width,height,color_space,color_primaries,color_transfer,color_range",
         "-of", "json", str(src)],
        check=True, capture_output=True, text=True).stdout
    return json.loads(out)["streams"][0]


def sample_wall(src: pathlib.Path) -> str:
    """Median color of the brighter top corner (same wall estimate the render
    engine uses) — the pad color must read as background to the mask."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", "0.5", "-i", str(src),
         "-frames:v", "1", "-vf", "scale=32:32", "-pix_fmt", "rgb24",
         "-f", "rawvideo", "-"],
        check=True, capture_output=True).stdout

    def corner(x0, x1):
        px = [raw[(y * 32 + x) * 3:(y * 32 + x) * 3 + 3]
              for y in range(6) for x in range(x0, x1)]
        med = [sorted(p[c] for p in px)[len(px) // 2] for c in range(3)]
        return med

    tl, tr = corner(0, 10), corner(22, 32)
    wall = max(tl, tr, key=lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2])
    return "0x{:02X}{:02X}{:02X}".format(*wall)


def pad_filter(iw: int, ih: int, color: str) -> str:
    """For sources NARROWER than the 718:754 tile: widen the frame to the tile
    aspect with flat wall-colored borders — the full person is preserved,
    nothing is cropped or stretched, and the pad masks away as background.
    (Edge-smear was tried first and fails when the subject touches the frame
    edge: their pixels smear into solid bars that render as subject.)"""
    target_w = round(ih * 718 / 754 / 2) * 2
    if target_w <= iw:
        return FILTER  # already wide enough; standard top-anchored crop
    left = (target_w - iw) // 2
    return (f"pad=w={target_w}:h=ih:x={left}:y=0:color={color},"
            f"scale=432:-2:flags=lanczos")


def transcode(src: pathlib.Path, outdir: pathlib.Path, crf: int = 18,
              duration: str = DURATION, pad: bool = False) -> pathlib.Path:
    stem = "Niamien" if src.stem.startswith("Niamien") else src.stem
    dst = outdir / f"{stem}.mp4"
    color = probe_color(src)
    vf = (pad_filter(int(color["width"]), int(color["height"]), sample_wall(src))
          if pad else FILTER)
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", "-vf", vf,
           "-c:v", "libx264", "-preset", "slow", "-crf", str(crf)]
    if duration != "full":
        cmd[4:4] = ["-t", duration]
    for probe_key, flag in [("color_space", "-colorspace"),
                            ("color_primaries", "-color_primaries"),
                            ("color_transfer", "-color_trc"),
                            ("color_range", "-color_range")]:
        val = color.get(probe_key)
        if val and val != "unknown":
            cmd += [flag, val]
    cmd += ["-movflags", "+faststart", str(dst)]
    subprocess.run(cmd, check=True)
    return dst


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sources", nargs="+", type=pathlib.Path)
    ap.add_argument("-o", "--outdir", type=pathlib.Path, required=True)
    ap.add_argument("--crf", type=int, default=18,
                    help="x264 CRF; 18 = served files, 20 = base64-embedded mockup")
    ap.add_argument("--duration", default=DURATION,
                    help="seconds to keep, or 'full' for the whole clip")
    ap.add_argument("--pad", action="store_true",
                    help="widen narrow sources to the 718:754 tile aspect "
                         "(edge-smear pad) instead of cropping")
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    for src in args.sources:
        dst = transcode(src, args.outdir, args.crf, args.duration, args.pad)
        kb = dst.stat().st_size / 1024
        print(f"{src.name} -> {dst}  ({kb:.0f} KB)")


if __name__ == "__main__":
    sys.exit(main())
