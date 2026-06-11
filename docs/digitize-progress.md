# Digitization progress (resumable state)

This file is a human- and agent-readable snapshot so the `/digitize` batch can
resume after a context compaction. **Source of truth is `images/manifest.json`**
(per-photo status) plus the files in `recipes/` and `index.json`. Nothing
depends on conversation history.

## MAIN SEQUENCE COMPLETE (p56–392)

- **The entire main photo run IMG_8396–8659 is processed.** The book ends at
  p392 (bibliography, skipped as end matter). Digitized through the ice-cream
  section and serving-ideas page. **249 index entries**; all recipe files
  validate, every index entry has a file. 4 section-intro pages
  (`kind:"section"`): KANEPELER, Kek/Pandispanya Bilgileri, Reçel/Marmelat
  Bilgileri, Dondurmalarla Hazırlanan Hafif Tatlılar.

## Remaining work

1. **Reshoot pass — IMG_8660–8695 (35 photos, out of page order).** OCR each to
   read its page number and fill the gaps listed in `reshoot-needed.md`
   (p131–132, 159–160, 174, 180, 182, 194, 198, 204, 222, 240, 242, 248, 252,
   264, 274, 278, 281–282, 285–286, 336, 348, 350, 351–352, 358, 361, 362, 369,
   373, 376–377, 379, 381). Several "deferred tails" in reshoot-needed.md can be
   joined to their now-reshot heads.
2. **Completeness audit (user-requested).** After the reshoot pass, list every
   page number present in `index.json`, find numeric gaps, and report any pages
   still genuinely missing (stuck-together pages never photographed).

## Reshoot batch page map (IMG_8660–8695 → page)

8660→174 (Etli Kuru Fasulye) · 8661→180 (enginar tail) · 8662→198 (Fasulye
Turşusu) · 8663→222 (börek tail) · 8664→240 (note) · 8665→264 + 8666→265
(Yaprak Hamuru ile Talaş Böreği) · 8667→281 + 8668→282 (Güllaç) · 8669→283
(milk-dessert tail) · 8670→285 + 8671→286 (Hoşmerim) · 8672→204 · 8673→236
(dup of Su Böreği tail?) · 8674→242 (Hazır Börek) · 8675→248 + 8676→249
(Patlıcanlı Börek / Pırasalı İç) · 8677→? (Kolay Oğeleme, blurry) · 8678→252
(Çiğ Börek) · 8679→264 + 8680→265 (dup of 8665/8666) · 8681→275 (Revani tail)
· 8682→336 · 8683→350 (Şuale Krem) · 8684→358 (Mozaik Pastası) · 8685→361 +
8695→361 (Bal Kabağı Reçeli) · 8686→362 (Kayısı Reçeli) · 8687→372 (dup Ayva
Jölesi) · 8688→373 (Kolay Meyva Jölesi) · 8689→376 (Kestane Şekerlemesi) ·
8690→377 (Boza) · 8691→381 (Portakal Likörü) · 8692→380 (dup Mevsimlik Şurup)
· 8693→315 (Halka).
**Still NOT covered by reshoots → genuinely missing:** p131–132, p159–160,
p182, p194, p278, p348/349 (chestnut cake), p351–352, p369, p379.
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
