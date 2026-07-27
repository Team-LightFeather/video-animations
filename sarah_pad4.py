#!/usr/bin/env python3
"""Sarah v4 (Marco 7-27): v3 clipped her raised hands — the crop top sat at
y=70 while her hands reach up to source row ~49. This one is 10% bigger
(zoom 1.14 -> ~1.036) with the crop top at y=20 (29px clearance above her
highest reach) and keeps her head on Marco's line (head-top ~row 93 of 454,
same as the approved v3 placement).

Geometry (576x572 source):
  crop 556x514 @ x=10,y=20   (bottom 38px of source exit the tile, like the
                              other clips' torso cut)
  pad to 556x584, content y=70 (wall-color pad above)
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
vf = (f"crop=556:514:10:20,pad=w=556:h=584:x=0:y=70:color={wall},"
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
