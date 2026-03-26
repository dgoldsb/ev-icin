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

## Architecture

Content lives in JSON. Two HTML files handle all rendering via vanilla JS — no frameworks, no build step. Adding a recipe means adding a JSON file and an entry in `index.json`.

## Recipes

Recipes come from the Turkish book "Ev İçin". Each JSON file has:
1. **`turkish`** — array of paragraphs, verbatim from the book, never altered
2. **English fields** — `ingredients_en`, `instructions_en`, `notes_en` (optional), `variations` (optional)

### File naming

`recipes/p{PAGE_NUMBER}_{snake_case_name}.json`
Page number zero-padded to 3 digits. Turkish characters normalized (ç→c, ş→s, ğ→g, ü→u, ö→o, ı→i).
Example: page 42, "Izgara Köfte" → `recipes/p042_izgara_kofte.json`

### Two-column ingredient lists

The book often prints ingredients in two columns. When reading from a photo, merge them in reading order (left column top-to-bottom, then right column) before storing.

## Skills

- `/add-recipe` — scaffold a new recipe page
- `/webdev` — web development guidance and conventions for this project
