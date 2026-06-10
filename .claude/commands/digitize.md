Digitize one or more photographed pages of "Ev İçin" into recipe JSONs.

Usage:
- `/digitize IMG_8154` (or full filename / path) — process one photo
- `/digitize` with no arguments — batch mode: process every photo in `images/` not yet marked done in `images/manifest.json`

This skill handles the photo → verified Turkish text part of the work. For
everything downstream (continuation detection, file naming, JSON structure,
tags, index.json entries, translation conventions) **follow
`.claude/commands/add-recipe.md` exactly** — read it before writing any file.

Full rationale, validation results, and model requirements are recorded in
`docs/adr/0001-digitization-pipeline.md`. Short version: run this skill on a
model with high-resolution vision (Fable 5 or Opus 4.7+); smaller models
raise the flag rate but cannot corrupt data, because acceptance requires
two-source agreement.

## Why this procedure exists

Reading a full 12MP page photo downscaled in one go makes small print
illegible, and a vision model will silently guess at what it cannot resolve.
Two rules eliminate that failure mode:

1. **Never transcribe from the full-page view.** Use it only for layout. All
   verbatim text comes from native-resolution crops.
2. **Never trust a single source.** Every ingredient line and every number
   must be confirmed by Apple's OCR (an independent system) or, failing that,
   flagged to the user. Agreement between two independent readings is the
   acceptance criterion — your own confidence is not.

## Per-photo procedure

### 1. Prepare the image

If the file is HEIC and no `.jpg` sibling exists:
`sips -s format jpeg images/X.HEIC --out images/X.jpg`

Work from the JPG. Check orientation with `sips -g pixelWidth -g pixelHeight`;
a landscape page photo is probably a two-page spread — crop it into two
portrait halves and treat each as its own page.

### 2. Layout pass (full page, downscaled is fine)

Read the JPG with the Read tool. Determine only:
- page number (bottom corner) and recipe title(s)
- whether the page is a continuation of the previous recipe (see add-recipe.md)
- vertical extents of the regions: ingredient block (Ölçüler), instruction
  block (İşlemler), notes (BESİN BİLGİSİ / GENEL BİLGİ / Not)
- whether the ingredient list is two-column

### 3. Transcription pass (native-resolution crops)

Crop the page into horizontal bands at **full native resolution** and read
each band. Bands of ~25–30% page height from a ~3000px-wide photo are crisply
legible. The OCR output (step 4 — run it first if convenient) gives exact
fractional y-coordinates for `Ölçüler :`, `İşlemler :`, and note headings;
use those for band boundaries instead of eyeballing.

Give the ingredient block its own band, with generous margin below — the
right column may continue past the `İşlemler :` heading. Crop with
`tools/crop.py` (fractions of the upright image, EXIF handled):

`python3 tools/crop.py images/X.jpg 0.05 0.30 /tmp/digitize/X_ing.jpg`

Transcribe verbatim — book notation
exactly as printed (`1,5` not `1.5`, spelling and punctuation untouched).
Merge two-column ingredient lists left column top-to-bottom, then right.

### 4. OCR cross-check

Run the independent OCR (Apple Vision via pyobjc; no build step):

`python3 tools/ocr.py images/X.jpg`

Output is `minX <tab> minY <tab> text` per line, normalized coordinates,
origin top-left — so column membership is visible from x (left column lines
share a small minX; right column starts near 0.5) and reading order from y.

Compare against your transcription:
- **Every ingredient line**: amount, unit, and ingredient must match the OCR
  text (modulo OCR's own line-wrap artifacts — a number alone on one OCR line
  followed by the unit on the next is a match).
- **Every number inside instructions** (quantities, times, temperatures).
- Title, page number.
- **Omissions, both directions**: every OCR line in the ingredient region
  must be accounted for in your transcription, and vice versa. Beware: the
  right column often runs *below* the left column's `İşlemler :` heading, so
  an ingredient crop bounded by that heading can silently cut the last
  right-column lines (this happened with `5-6 dal maydanoz` on p86). The OCR
  output is full-page, so use it as the completeness reference.

For each disagreement, crop that single line tightly at native resolution and
re-read it. If the close read clearly resolves it, accept the close read and
note which source was wrong. If it is still ambiguous (blur, thumb over text,
damaged print), the line is **flagged**.

### 5. Review gate

- No flags → proceed silently.
- Flags → show the user only the flagged lines: both readings side by side
  plus the crop path so they can look at the photo region themselves
  (`open /tmp/digitize/X_line.jpg`). Wait for their answer before writing.

Never write a guessed value. A flag answered by the user is the only way an
unverified line gets into a file.

### 6. Write files

Follow add-recipe.md: create `recipes/pNNN_slug.json` (or update the previous
recipe if continuation), add the `index.json` entry with tags, strip leading
step numbers from instructions. Translate to English yourself — translation
needs no cross-check, only the Turkish source text does.

### 7. Update the manifest

`images/manifest.json` maps photo filename → result:

```json
{
  "IMG_8151.jpg": { "status": "done", "pages": [82], "slugs": ["p082_soslu_pirzola"] }
}
```

Other statuses: `"skip"` (not a recipe page — cover, tips, index pages; add a
`"note"`), `"flagged"` (waiting on user input). HEIC and JPG of the same
photo are one entry, keyed by the JPG name.

## Batch mode

When called with no arguments: list `images/*.jpg` plus `images/*.HEIC`
without a JPG sibling, drop entries already in the manifest, and run the
per-photo procedure on each remaining photo in filename order. Collect flags
as you go and present them all in one review gate at the end (one
interruption instead of many), then write all files. Finish with a summary
table: photo → page → recipe → flags resolved.

## Verification

After writing, spot-check: `python3 -m json.tool` each new file, confirm the
index.json entry is in page order, and confirm `index.html` would find the
slug (slug in file name matches `slug` field).
