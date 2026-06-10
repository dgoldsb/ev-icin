# Ev İçin — Project Context

## What This Is

A digital version of the Turkish classic household book "Ev İçin" (For the Home). The book contains recipes, household tips, and other domestic guidance. The website is primarily focused on recipes.

## Tech Philosophy

- Simple, mostly plain HTML/CSS
- Minimal JavaScript — only when genuinely needed
- No frameworks unless complexity demands it
- Content first; aesthetics can be refined later

## Site Structure

- `index.html` — homepage; JS fetches `index.json` to render the recipe list
- `index.json` — source of truth: ordered list of all recipes (page, slug, names)
- `recipe.html` — single template; JS reads `?id=` param and fetches the recipe JSON
- `style.css` — shared stylesheet
- `recipes/` — one JSON file per recipe
- `tips/` — household tips (lower priority, not yet started)
- `images/` — page photos from the book; `images/manifest.json` tracks which photos are digitized
- `tools/` — digitization helpers: `ocr.py` (Apple Vision OCR with line coordinates), `crop.py` (EXIF-aware native-resolution crops)
- `docs/adr/` — architecture decision records

## Architecture

Content lives in JSON. Two HTML files handle all rendering via vanilla JS — no frameworks, no build step. Adding a recipe means adding a JSON file and an entry in `index.json`.

## Recipes

Recipes come from the Turkish book "Ev İçin". Each JSON file has parallel
`_tr` and `_en` fields: `name`, `ingredients`, `instructions`, plus optional
`notes` and `variations`. Turkish fields are verbatim from the book, never
altered. Full schema and conventions live in `.claude/commands/add-recipe.md`.

### File naming

`recipes/p{PAGE_NUMBER}_{snake_case_name}.json`
Page number zero-padded to 3 digits. Turkish characters normalized (ç→c, ş→s, ğ→g, ü→u, ö→o, ı→i).
Example: page 42, "Izgara Köfte" → `recipes/p042_izgara_kofte.json`

### Two-column ingredient lists

The book often prints ingredients in two columns. When reading from a photo, merge them in reading order (left column top-to-bottom, then right column) before storing.

### Number formatting

Use the book's notation verbatim. Fractions appear as `1,5` (comma decimal), not `1½` or `1.5`. Reproduce this exactly in both `_tr` and `_en` fields.

## Digitization pipeline

Photos of book pages go into `images/` (HEIC straight from the phone is
fine). `/digitize` turns them into recipe JSONs: it reads native-resolution
crops with vision, cross-checks every ingredient line and number against an
independent Apple Vision OCR pass (`tools/ocr.py`), and only interrupts the
user for lines where the two sources disagree. Never transcribe from a
downscaled full-page view, and never accept a line on one source alone —
these two rules are what keep hallucinated quantities out of the data.
Rationale, validation results, and model requirements (run the parsing
session on Fable 5 or Opus 4.7+ for high-resolution vision) are in
`docs/adr/0001-digitization-pipeline.md`.

## Skills

- `/digitize` — turn page photos in `images/` into recipe JSONs (photo → verified text → files)
- `/add-recipe` — recipe conventions and scaffolding (used by `/digitize` for the file-writing half)
- `/webdev` — web development guidance and conventions for this project
