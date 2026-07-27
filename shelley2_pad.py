#!/usr/bin/env python3
"""Shelley take 2 (Shelley2.MOV 644x704) with ZOOM OUT per Marco 7-27:
pad ~20% around her with the measured wall green (0x49944D) so she reads
wider/smaller in the tile. All vertical pad goes on TOP (bottom-anchored —
bottom pad would float her torso off the tile edge). The right 44px (x>=600)
are CROPPED first: deep wall shadow + door edge whose near-black chroma noise
defeats the hue mask, and which her hair/arm periodically connects to the
figure (so the min-component filter can't drop it). Her sleeve grazes that
band for ~1s at the bottom corner — the clip reads as the sleeve exiting the
frame, same as Nate/Ruben.
644x704 -> crop 600x704 -> pad 806x846 (x=103, y=142) -> Lanczos 432x454,
crf 20, full take."""
import pathlib
import subprocess
import sys

sys.path.insert(0, "/Users/marcoopertti/LF-Website/tools")
import level_clips as lc

src = pathlib.Path("/Users/marcoopertti/LF-Website/newvids2/Shelley2.MOV")
dst = pathlib.Path("/Users/marcoopertti/LF-Website/quality_test_outputs/nv2select/Shelley.mp4")

color = lc.probe_color(src)
vf = ("crop=600:704:0:0,pad=w=806:h=846:x=103:y=142:color=0x49944D,"
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
