#!/usr/bin/env python3
"""Sarah v3 (Marco 7-27): 14% zoom (as sarah_pad2) PLUS pushed DOWN 15% of
the tile so her head lines up with Marco's. Same 506x422-effective window,
same bottom-exit behavior as every clip: the extra 80px of top pad shifts
her down and her lowest 80px of torso exits the tile bottom.

Geometry (pre-scale, 506-wide space, tile = 506x532 -> 432x454):
  crop 506x422 @ x=35,y=70   (top-anchored: head position unchanged in crop)
  pad to 506x532 with y=110  (was 30; +80 = 15% of 532)
  Lanczos -> 432x454, crf 20, full take."""
import pathlib
import subprocess
import sys

sys.path.insert(0, "/Users/marcoopertti/LF-Website/tools")
import level_clips as lc

src = pathlib.Path("/Users/marcoopertti/LF-Website/newvids2/SarahVId.mov")
dst = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select/Sarah.mp4")

color = lc.probe_color(src)
wall = lc.sample_wall(src)
vf = (f"crop=506:422:35:70,pad=w=506:h=532:x=0:y=110:color={wall},"
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
