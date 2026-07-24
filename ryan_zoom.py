#!/usr/bin/env python3
"""One-off: Ryan zoomed in ~17% (Marco asked 15-20%), same pipeline otherwise.

Source 1080x1302 -> crop a 922x1112 window (centered x, y=60 so his head
keeps clearance), pad to the 718:754 tile aspect with the sampled wall color
(pattern from level_clips --pad), single Lanczos scale to 432x454, crf 20."""
import pathlib
import subprocess
import sys

sys.path.insert(0, "/Users/marcoopertti/LF-Website/tools")
import level_clips as lc

src = pathlib.Path("/Users/marcoopertti/LF-Website/newvids2/Ryan Motion Clip - Darker Shirt.mov")
dst = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select/Ryan.mp4")

color = lc.probe_color(src)
wall = lc.sample_wall(src)
vf = (f"crop=922:1112:79:60,"
      f"pad=w=1058:h=1112:x=68:y=0:color={wall},"
      f"scale=432:-2:flags=lanczos")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", "-vf", vf,
       "-c:v", "libx264", "-preset", "slow", "-crf", "20"]
for pk, flag in [("color_space", "-colorspace"),
                 ("color_primaries", "-color_primaries"),
                 ("color_transfer", "-color_trc"),
                 ("color_range", "-color_range")]:
    v = color.get(pk)
    if v and v != "unknown":
        cmd += [flag, v]
cmd += ["-movflags", "+faststart", str(dst)]
subprocess.run(cmd, check=True)
print("wrote", dst, f"{dst.stat().st_size/1024:.0f} KB")
