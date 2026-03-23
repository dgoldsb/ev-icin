# Ev İçin — Project Context

## What This Is

A digital version of the Turkish classic household book "Ev İçin" (For the Home). The book contains recipes, household tips, and other domestic guidance. The website is primarily focused on recipes.

## Tech Philosophy

- Simple, mostly plain HTML/CSS
- Minimal JavaScript — only when genuinely needed
- No frameworks unless complexity demands it
- Content first; aesthetics can be refined later

## Site Structure

- `index.html` — homepage / table of contents
- `style.css` — shared stylesheet
- `recipes/` — one HTML file per recipe
- `recipes/_template.html` — base template for new recipe pages
- `tips/` — household tips (lower priority, not yet started)

## Recipes

Recipes come from the Turkish book "Ev İçin". Each recipe page has two sections:
1. **Turkish original** — verbatim text from the book, never altered
2. **English translation** — structured with ingredients and instructions

### File naming

`recipes/p{PAGE_NUMBER}_{snake_case_name}.html`
Page number zero-padded to 3 digits. Turkish characters normalized (ç→c, ş→s, ğ→g, ü→u, ö→o, ı→i).
Example: page 42, "Izgara Köfte" → `recipes/p042_izgara_kofte.html`

## Skills

- `/add-recipe` — scaffold a new recipe page
- `/webdev` — web development guidance and conventions for this project
