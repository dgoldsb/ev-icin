#!/usr/bin/env python3
"""Crop a region from a page photo at native resolution.

Usage: tools/crop.py <image> <top> <bottom> <out.jpg> [<left> <right>]

top/bottom (and optional left/right) are fractions 0-1 of the *upright* image
(EXIF orientation is applied first, so coordinates match what you see when
viewing the photo). Output is a full-resolution JPG of the region.
"""

import sys

from PIL import Image, ImageOps

if len(sys.argv) not in (5, 7):
    sys.exit("usage: crop.py <image> <top> <bottom> <out.jpg> [<left> <right>]")

path, top, bottom, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
left, right = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) == 7 else (0.0, 1.0)

img = ImageOps.exif_transpose(Image.open(path))
w, h = img.size
region = img.crop((int(left * w), int(top * h), int(right * w), int(bottom * h)))
region.save(out, quality=92)
print(f"{out}: {region.size[0]}x{region.size[1]} from {w}x{h}")
