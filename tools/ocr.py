#!/usr/bin/env python3
"""Apple Vision OCR for Ev İçin page photos.

Usage: tools/ocr.py <image> [more images...]

Output: one line per recognized text line, tab-separated:
    <minX>\t<minY>\t<text>

Coordinates are normalized 0-1 with origin at TOP-left (minY 0 = top of
image), so lines print in reading order and two-column layouts can be
separated by x. A "== <path>" header precedes each image's output.
Reads JPG and HEIC alike; EXIF orientation is respected.
"""

import sys

import Quartz
import Vision


def ocr(path):
    url = Quartz.CFURLCreateWithFileSystemPath(
        None, path, Quartz.kCFURLPOSIXPathStyle, False
    )
    src = Quartz.CGImageSourceCreateWithURL(url, None)
    if src is None:
        sys.exit(f"cannot read image: {path}")
    image = Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)

    props = Quartz.CGImageSourceCopyPropertiesAtIndex(src, 0, None) or {}
    orientation = props.get(Quartz.kCGImagePropertyOrientation, 1)

    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setRecognitionLanguages_(["tr-TR"])
    request.setUsesLanguageCorrection_(True)

    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_orientation_options_(
        image, orientation, {}
    )
    ok, error = handler.performRequests_error_([request], None)
    if not ok:
        sys.exit(f"OCR failed for {path}: {error}")

    lines = []
    for obs in request.results() or []:
        candidates = obs.topCandidates_(1)
        if not len(candidates):
            continue
        box = obs.boundingBox()  # Vision origin is bottom-left; flip Y.
        lines.append(
            (
                box.origin.x,
                1.0 - (box.origin.y + box.size.height),
                candidates[0].string(),
            )
        )
    lines.sort(key=lambda line: line[1])

    print(f"== {path}")
    for x, y, text in lines:
        print(f"{x:.3f}\t{y:.3f}\t{text}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: ocr.py <image>...")
    for path in sys.argv[1:]:
        ocr(path)
