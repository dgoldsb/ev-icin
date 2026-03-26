Add a new recipe to the Ev İçin website.

## Inputs expected from the user

- **Page number** — the page number in the source book (required)
- **Turkish text** — the original recipe text as it appears in the book (required). If the user provides a photo of the page, read it carefully — ingredients are often in two columns and must be merged in reading order.
- **English translation** — translated name, ingredients, and instructions (required)

## File naming

`recipes/p{PAGE_NUMBER}_{snake_case_name}.json`

- Page number is zero-padded to 3 digits: page 7 → `007`, page 42 → `042`
- Snake case name derived from the Turkish recipe name: lowercase, spaces → underscores, normalize Turkish characters (ç→c, ş→s, ğ→g, ü→u, ö→o, ı→i)
- Example: page 42, "Izgara Köfte" → `recipes/p042_izgara_kofte.json`

## Turkish text rule

Copy Turkish text exactly as it appears in the source — spelling, punctuation, and all — with one exception: **remove the leading step number from each instruction** (e.g. "1 — " or "2 — ") before storing in `instructions_tr`. The `<ol>` element provides numbering automatically; keeping it in the text would duplicate it.

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
    "1 — Yıkanmış kemik bol su ile ateşe konur.",
    "2 — ..."
  ],
  "notes_tr": "Optional Turkish note (omit field if none)",
  "ingredients_en": [
    "Ingredient one",
    "Ingredient two"
  ],
  "instructions_en": [
    "Step one.",
    "Step two."
  ],
  "notes_en": "Optional English note (omit field if none)",
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

1. Create `recipes/p{PAGE_NUMBER}_{slug}.json` with the structure above.

2. Add an entry to `index.json` in page-number order:
   ```json
   { "page": 56, "slug": "p056_et_suyu", "name_tr": "ET SUYU", "name_en": "Meat Broth" }
   ```

3. Report the file path created.
