Add a new recipe to the Ev İçin website.

## Inputs expected from the user

- **Page number** — the page number in the source book (required)
- **Turkish text** — the original recipe text as it appears in the book (required). The preferred source is an **Apple text copy/OCR extract** pasted directly by the user — use this verbatim. If only a photo is provided, read it carefully, but numbers are error-prone: quantities like `2` vs `3`, fractions like `½` vs `1`, and units like `çorba kaşığı` vs `çay kaşığı` are easy to misread. Always prefer asking the user for the text extract over guessing from a photo.
- **English translation** — translated name, ingredients, and instructions (required)

### Handling raw OCR paste

Apple's text copy from photos is not pretty — line breaks fall mid-word, numbers may appear on their own line, and columns run together. Reconstruct ingredient lines carefully:
- A number on its own line (e.g. `2`) followed by a unit on the next line (e.g. `su bardağı süt`) is a single ingredient: `2 su bardağı süt`
- Two-column layouts appear as interleaved lines; merge left column top-to-bottom, then right column top-to-bottom
- Include general-knowledge sections at the end (BESİN BİLGİSİ, GENEL BİLGİ) in `notes_tr`, with their label, just like any other note

## Detecting continuations

Before creating a new file, check whether the page is a **continuation** of the previous recipe rather than a new one. Signs of a continuation:
- The page does not start with a new recipe title — it begins mid-sentence or mid-list
- It adds variations, notes, or extra sub-recipes to a recipe that started on the previous page
- The previous recipe's page in `index.json` has a `page_end` that would reach this page, or no `page_end` yet and this page follows directly

**If the page is a continuation:**
- Do NOT create a new JSON file
- Add any new variations or notes to the existing recipe's JSON file
- Update the `page_end` field in `index.json` for that recipe (add it if not present)
- Do not add a new entry to `index.json`

## File naming (new recipes only)

`recipes/p{PAGE_NUMBER}_{snake_case_name}.json`

- Page number is zero-padded to 3 digits: page 7 → `007`, page 42 → `042`
- Snake case name derived from the Turkish recipe name: lowercase, spaces → underscores, normalize Turkish characters (ç→c, ş→s, ğ→g, ü→u, ö→o, ı→i)
- Example: page 42, "Izgara Köfte" → `recipes/p042_izgara_kofte.json`

## Turkish text rule

Copy Turkish text exactly as it appears in the source — spelling, punctuation, and all — with one exception: **remove the leading step number from each instruction** (e.g. "1 — " or "2 — ") before storing in `instructions_tr`. The `<ol>` element provides numbering automatically; keeping it in the text would duplicate it.

**Numbers matter most.** The most common errors when reading from photos are wrong quantities (e.g. `2` vs `3` çorba kaşığı), wrong units (e.g. `çorba kaşığı` vs `çay kaşığı`), and missing ingredients entirely. When using OCR text, transcribe these exactly. When working from a photo alone, flag any number you are not certain about rather than guessing.

## JSON structure

Both languages use the same fields, with `_tr` and `_en` suffixes. The renderer applies an identical template to both, so structure must be consistent.

```json
{
  "page": 56,
  "slug": "p056_et_suyu",
  "name_tr": "ET SUYU",
  "name_en": "Meat Broth",
  "ingredients_tr": [
    "İstenilen miktar kemik",
    "1 çorba kaşığı limon suyu veya sirke"
  ],
  "instructions_tr": [
    "Yıkanmış kemik bol su ile ateşe konur.",
    "..."
  ],
  "notes_tr": "Not: Single note — use a plain string.",
  "ingredients_en": [
    "Ingredient one",
    "Ingredient two"
  ],
  "instructions_en": [
    "Step one.",
    "Step two."
  ],
  "notes_en": "Note: Single note — use a plain string. If multiple notes (e.g. a recipe Not: and a GENEL BİLGİ:), use an array of strings instead — each renders as a separate paragraph.",
  "variations": [
    {
      "name_tr": "TANELİ SEBZE ÇORBASI",
      "name_en": "Chunky Vegetable Soup",
      "description_tr": "Turkish description.",
      "description_en": "English description."
    }
  ]
}
```

Omit `notes_tr`, `notes_en`, and `variations` if not present in the recipe.

## Steps

1. Determine if this is a continuation (see above). If so, update the existing recipe and stop.

2. Otherwise, create `recipes/p{PAGE_NUMBER}_{slug}.json` with the structure above.

3. Add an entry to `index.json` in page-number order. For single-page recipes:
   ```json
   { "page": 56, "slug": "p056_et_suyu", "name_tr": "ET SUYU", "name_en": "Meat Broth" }
   ```
   For recipes that span multiple pages, include `page_end`:
   ```json
   { "page": 57, "page_end": 58, "slug": "p057_ezme_sebze_corbasi", "name_tr": "EZME SEBZE ÇORBASI", "name_en": "Puréed Vegetable Soup" }
   ```

4. Report the file path created.
