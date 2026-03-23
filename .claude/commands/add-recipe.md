Add a new recipe page to the Ev İçin website.

## Inputs expected from the user

- **Page number** — the page number in the source book (required, used in filename)
- **Turkish text** — the original recipe text as it appears in the book (required)
- **English translation** — translated name, ingredients, and instructions (required)

## File naming

`recipes/p{PAGE_NUMBER}_{snake_case_name}.html`

- Page number is zero-padded to 3 digits: page 7 → `007`, page 42 → `042`
- Snake case name is derived from the Turkish recipe name: lowercase, spaces → underscores, normalize Turkish characters (ç→c, ş→s, ğ→g, ü→u, ö→o, ı→i)
- Example: page 42, "Izgara Köfte" → `recipes/p042_izgara_kofte.html`

## Turkish text rule

**Do not alter the Turkish text in any way.** Copy it exactly as provided — spelling, punctuation, line breaks, and all. Wrap each paragraph in `<p>` tags, splitting on blank lines. Do not parse, rephrase, correct, or restructure it.

## Steps

1. Derive the filename from the page number and Turkish recipe name.

2. Copy `recipes/_template.html` as the starting point. Replace all placeholder values:
   - `RECIPE_NAME_TR` — Turkish recipe name
   - `RECIPE_NAME_EN` — English recipe name
   - `TURKISH_TEXT_VERBATIM` — the Turkish text, split into `<p>` blocks on blank lines, unmodified
   - `PAGE_NUMBER` — the source book page number

3. Fill in the English translation section with structured ingredients and instructions.

4. Add a link to `index.html` inside `<ul id="recipe-list">`, in page-number order:
   ```html
   <li>
     <a href="recipes/FILENAME.html">
       <span>RECIPE_NAME_TR — RECIPE_NAME_EN</span>
       <span class="page-num">p. PAGE_NUMBER</span>
     </a>
   </li>
   ```

5. Report the file path created.
