Web development guidance and conventions for the Ev İçin project.

## Project Conventions

- **Plain HTML/CSS first.** Add JavaScript only when there is a clear, specific need.
- **No build tools or bundlers.** Files are served directly; no npm, webpack, or similar.
- **No CSS frameworks.** Write styles from scratch in `style.css`.
- **Relative links.** Use relative paths (`../style.css`, `../index.html`) so the site works without a server.
- **Language:** Pages are in Turkish (`lang="tr"`), with English translations where helpful.
- **Character encoding:** Always `<meta charset="UTF-8">` to handle Turkish characters (ç, ş, ğ, ü, ö, ı).

## File Layout

```
ev-icin/
  index.html        ← homepage / table of contents
  style.css         ← shared styles
  recipes/          ← one .html file per recipe
  tips/             ← household tips (lower priority)
```

## Style Principles

- Readable typography, comfortable line length (~65–75 chars)
- Sufficient contrast
- Mobile-friendly (use relative units, simple layouts)
- No decorative complexity until content is stable

## When Asked to Do Web Work

1. Read relevant existing files before making changes.
2. Keep changes minimal and focused.
3. Validate that links and paths are correct relative to file location.
4. Do not introduce dependencies (CDN links, frameworks) without discussing first.
