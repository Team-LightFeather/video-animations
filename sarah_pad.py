#!/usr/bin/env python3
"""One-off: SarahVId.mov (576x572) is slightly WIDER than the 718:754 tile.
Marco's rule: never crop people. So pad the TOP with the sampled wall color
(bottom pad would float her torso off the tile edge) to reach the tile
aspect, then the usual single Lanczos scale to 432x454, crf 20, full take."""
import pathlib
import subprocess
import sys

sys.path.insert(0, "/Users/marcoopertti/LF-Website/tools")
import level_clips as lc

src = pathlib.Path("/Users/marcoopertti/LF-Website/newvids2/SarahVId.mov")
dst = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select/Sarah.mp4")

color = lc.probe_color(src)
wall = lc.sample_wall(src)
# 576 wide at tile aspect needs h=606 (even); all 34 pad rows go on top
vf = f"pad=w=576:h=606:x=0:y=34:color={wall},scale=432:-2:flags=lanczos"
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
