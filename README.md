# Ev İçin

A digital version of the Turkish classic household book *Ev İçin* (For the Home), focusing on recipes.

## Local development

From the project root:

```bash
python3 -m http.server
```

Then open [http://localhost:8000](http://localhost:8000).

## Deploying to GitHub Pages

1. Push the repository to GitHub.
2. Go to **Settings → Pages**.
3. Under **Source**, select the `main` branch and `/ (root)` folder.
4. Save. The site will be available at `https://dgoldsb.github.io/ev-icin/`.

No build step required — the site is plain HTML, CSS, and JS.

The site is live at [https://dgoldsb.github.io/ev-icin/](https://dgoldsb.github.io/ev-icin/).

## Adding pages from the book

1. Photograph the page(s) and drop the files into `images/` (HEIC is fine,
   AirDrop straight from the phone).
2. In Claude Code, run `/digitize` — it picks up every photo not yet listed
   in `images/manifest.json`, transcribes it from native-resolution crops,
   cross-checks every quantity against an independent Apple Vision OCR pass
   (`tools/ocr.py`), and writes the recipe JSON plus `index.json` entry.
3. You are only asked about lines where the two readings disagree; everything
   else is written without interruption.

`tools/ocr.py` and `tools/crop.py` need the system Python with `pyobjc` and
`Pillow` (both already present via pyenv); there is no build step.

## TODO

- [ ] Favouriting recipes (store favourites in `localStorage`, show on index page)
- [ ] Macro calculation per recipe — build a small ingredient database (`ingredients.json`) mapping common ingredients to macros (kcal, protein, fat, carbs per 100g); the set of ingredients across these recipes is limited enough to cover manually. Recipe page would look up each ingredient and display a nutrition summary.
- [ ] Add partner's personal recipes in the same style, extending the book beyond the original source.
