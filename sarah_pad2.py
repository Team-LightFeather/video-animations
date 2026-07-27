#!/usr/bin/env python3
"""Sarah ZOOMED IN 14% (Marco 7-27). From SarahVId.mov 576x572:
crop window = frame/1.14 -> 506x502, centered horizontally (x=35) and
BOTTOM-anchored (y=70: trims headroom, keeps her torso at the tile edge —
edge strips verified pure wall at all phases, nothing of her is cut).
Then the usual top pad to the 718:754 tile aspect with the sampled wall
color and a single Lanczos scale to 432x454, crf 20, full take."""
import pathlib
import subprocess
import sys

sys.path.insert(0, "/Users/marcoopertti/LF-Website/tools")
import level_clips as lc

src = pathlib.Path("/Users/marcoopertti/LF-Website/newvids2/SarahVId.mov")
dst = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select/Sarah.mp4")

color = lc.probe_color(src)
wall = lc.sample_wall(src)
# 506 wide at tile aspect needs h=532 (even); all 30 pad rows on top
vf = (f"crop=506:502:35:70,pad=w=506:h=532:x=0:y=30:color={wall},"
      "scale=432:-2:flags=lanczos")
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
