# Digitization progress (resumable state)

This file is a human- and agent-readable snapshot so the `/digitize` batch can
resume after a context compaction. **Source of truth is `images/manifest.json`**
(per-photo status) plus the files in `recipes/` and `index.json`. Nothing
depends on conversation history.

## Status as of p126–366

- **Digitized:** pages 126–366 (plus the pre-existing 56–125). Through the
  tart section and into the jam/marmalade section (kayısı/ayva/incir/çilek/ekşi
  elma/greyfrut reçeli) — with a 3rd section-intro page "Reçel Marmelat... Kısa
  Bilgiler". 232 index entries; all recipe files validate and every index entry
  has a file.
- **Next unprocessed photo:** IMG_8636 (≈ p367). ~56 photos remaining
  (→ IMG_8659 main sequence, then reshoot batch IMG_8660–8695).
- **Gaps/reshoots in the p336–362 stretch** (all in reshoot-needed.md): p336,
  p348 (chestnut-cake head; tail on p349 deferred), p350, p351–352 (blurry
  multi-component pasta), p358 (last cake recipe), p361 (jam, misframed), p362
  (jam, blurry).
- **Convention added (p319+):** filled-pastry recipes with separate dough/
  filling ingredient blocks store the book's labels as literal list entries
  (`"Hamurunun Ölçüleri:"` / `"İçinin Ölçüleri:"`, EN `"For the dough:"` /
  `"For the filling:"`) inside the flat `ingredients_*` array. See
  p319_elmali_ay, p321_cevizli_ay.
- **Dessert-section gaps found (all in `reshoot-needed.md`):** p278, p281–282,
  p285–286 not captured; p274 (Revani) blurry/deferred; several deferred tails
  (p243, p249, p265, p275, p283) and one deferred variation (Tuzlu Krep Süzet).
- Every ingredient line cross-checked against `tools/ocr.py`; quantities
  re-cropped at native resolution wherever OCR was incomplete. No data guessed.
- All output in `recipes/*.json` + `index.json`; every processed photo marked
  in `images/manifest.json`.

### New conventions added this run (p223+)
- **Section-intro pages** (e.g. KANEPELER): own entry with `"kind":"section"`
  and `body_tr`/`body_en` paragraph arrays. `recipe.html` renders these as
  title + paragraphs (no Malzemeler/İşlemler); `index.html` styles them with
  `.toc-section`. They carry no `tags`, so they only show under the "All"
  filter.
- **Prose recipes with no ingredient block** (canapés): `ingredients_*` is `[]`
  and the whole paragraph goes in `instructions_*`. `recipe.html` hides the
  empty Ingredients heading.

### New gaps found this run (need reshoot / not photographed)
- **p240** (`IMG_8509`) — blurry, illegible.
- **p242** (`IMG_8511`) — blurry; its tail on legible **p243** (`IMG_8512`) is
  saved under "Deferred continuations" in `docs/reshoot-needed.md`.
- **p248** — PIRASALI İÇ head never photographed (stuck pages); its tail on
  legible **p249** (`IMG_8518`) is saved under "Deferred continuations".
  `IMG_8517` is a blurry duplicate of p249 (skipped).
- **p252** (`IMG_8521`) — full recipe page (likely ÇİĞ BÖREK), blurry/illegible.
- **p264** (`IMG_8533`) — blurry/illegible; head of a yaprak-hamuru börek
  (references Talaş böreği). Its tail on legible **p265** (`IMG_8534`) is saved
  under "Deferred continuations".

All deferred tails and new gaps are detailed in `docs/reshoot-needed.md`.
The reshoot batch `IMG_8660–8695` (not yet processed) should fill these.

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
