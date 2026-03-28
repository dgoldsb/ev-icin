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

## TODO

- [ ] Favouriting recipes (store favourites in `localStorage`, show on index page)
- [ ] Macro calculation per recipe — build a small ingredient database (`ingredients.json`) mapping common ingredients to macros (kcal, protein, fat, carbs per 100g); the set of ingredients across these recipes is limited enough to cover manually. Recipe page would look up each ingredient and display a nutrition summary.
- [ ] Add partner's personal recipes in the same style, extending the book beyond the original source.
