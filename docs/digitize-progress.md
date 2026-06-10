# Digitization progress (resumable state)

This file is a human- and agent-readable snapshot so the `/digitize` batch can
resume after a context compaction. **Source of truth is `images/manifest.json`**
(per-photo status) plus the files in `recipes/` and `index.json`. Nothing
depends on conversation history.

## Status as of p126–221

- **Digitized this run:** pages 126–221 (plus the pre-existing 56–125).
- **Flag rate:** zero — every ingredient line cross-checked clean against
  `tools/ocr.py`. No data is guessed.
- All output committed to `recipes/*.json` + `index.json`; every processed
  photo marked `status: "done"` in `images/manifest.json`.

## How to resume

1. Regenerate the worklist (next unprocessed photos):
   ```sh
   python3 - <<'PY'
   import json,os
   m=json.load(open('images/manifest.json'))
   heics=sorted(f for f in os.listdir('images') if f.lower().endswith('.heic'))
   left=[os.path.splitext(f)[0] for f in heics
         if m.get(os.path.splitext(f)[0]+'.jpg',{}).get('status') not in ('done','reshoot','flagged','skip')]
   print('next:', left[:8], '... remaining', len(left))
   PY
   ```
2. Continue the per-photo procedure in `.claude/commands/digitize.md` from the
   next photo (main sequence resumes at **IMG_8492 ≈ p223**).

## Two pending follow-up passes (do after the main sequence)

1. **Reshoot pass.** The user re-photographed the blurry/missing pages as
   **IMG_8660–8695** (36 photos, out of page order). OCR each to read its page
   number, then digitize the gap pages. Gaps awaiting these: see
   `docs/reshoot-needed.md` (131–132, 159–160, 174, 180, 182, 194, 198, 204,
   217-dup, 222, plus the rest of the blurry list).
2. **Completeness audit (user-requested).** After everything is in, list every
   digitized page number from `index.json`, find numeric gaps, and report any
   still missing — these would be pages stuck together that weren't
   photographed. Cross-check against the reshoot list so genuine gaps are
   distinguished from known-pending reshoots.
