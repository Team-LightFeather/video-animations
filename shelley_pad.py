#!/usr/bin/env python3
"""One-off: Shelley.MOV (720x808, saturated green wall) has a brown DOOR in
the right ~44px (x>=676) and sample_wall() picked a dark corner (iPhone
auto-exposure ramp at 0.5s), so the --pad bars came out near-black — both
broke the ascii mask. Reprocess: crop the door column (she never reaches it;
the person is untouched), pad both sides with the MEASURED wall green
(74,151,79 from x20..130 y80..300 at t=1.6s), single Lanczos scale to
432x454, crf 20, full take."""
import pathlib
import subprocess
import sys

sys.path.insert(0, "/Users/marcoopertti/LF-Website/tools")
import level_clips as lc

src = pathlib.Path("/Users/marcoopertti/LF-Website/newvids2/Shelley.MOV")
dst = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select/Shelley.mp4")

color = lc.probe_color(src)
# 676x808 after door crop; tile aspect needs w=770 -> 47px wall-green pad/side
vf = ("crop=676:808:0:0,pad=w=770:h=808:x=47:y=0:color=0x4A974F,"
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
