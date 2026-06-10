# ADR 0001 — Two-source verification pipeline for digitizing book pages

Date: 2026-06-10
Status: accepted

## Context

Recipes are digitized from phone photos of "Ev İçin" pages. The original
workflow was manual: open the photo, use Apple's select-text OCR, paste the
raw text into Claude for structuring, then hand-correct the ingredient
amounts that came out jumbled.

An earlier attempt to automate this by pasting photos directly into Claude
produced recipes that were *completely wrong*. The root cause: chat clients
downsample a 12MP page photo to ~1.5MP, the ingredient print drops below
legibility, and a vision model fills in unreadable text from its prior
("a köfte recipe probably has 2 onions…") — silent hallucination, which is
worse than no automation because errors look plausible.

Hand-corrected accuracy is the core value of this site. Any automation must
make errors *detectable*, not just rare.

## Decision

The `/digitize` skill (`.claude/commands/digitize.md`) enforces two rules:

1. **Never transcribe from a downscaled full-page view.** The full-page read
   is for layout only. All verbatim text comes from native-resolution crops
   (`tools/crop.py`), which give each region the full pixel budget.
2. **Never accept a line on one source alone.** Every ingredient line and
   every number must agree between the vision read and an independent Apple
   Vision OCR pass (`tools/ocr.py`, the same engine as the manual
   select-text flow). Agreement → accept; disagreement → flag to the user
   with the photo crop. A flagged line answered by a human is the only way
   an unverified value enters a file.

The two sources have **uncorrelated failure modes** — Apple OCR jumbles
column order but doesn't invent text; the vision model reads layout
correctly but can hallucinate under low resolution. Where they agree the
line is almost certainly right; where they disagree the error is caught.
This was chosen over a single-model "judge" pass, because a model verifying
its own transcription tends to confirm its own hallucinations.

### Model requirement for the parsing session

Run `/digitize` on a model with **high-resolution vision** — Fable 5 or
Opus 4.7+ (2576px max long edge). Sonnet 4.6 / Haiku 4.5 / Opus 4.6 cap at
1568px, which renders the 3024px-wide crops at ~52% of native instead of
~85%. Crops were sized to stay legible even at the lower cap, so a smaller
model degrades to a *higher flag rate* (more human review), not silent
errors — data integrity comes from the cross-check, which is
model-independent. Haiku is not recommended: weakest perception tier, and
the English translation (which has no cross-check) also rides on model
quality.

## Validation

Tested against six hand-corrected recipes (p082–p086, p089; ~55 ingredient
lines) using Fable 5: zero content errors. The one pipeline mistake that
occurred — a crop bounded by the `İşlemler :` heading truncating a
right-column ingredient (`5-6 dal maydanoz`, p86) — was caught by the OCR
omission check exactly as designed, validating the detectability property.
Fable 5 is the only model configuration with this empirical backing; before
trusting a smaller model, repeat the validation against a few corrected
recipes.

## Consequences

- Adding a page is: drop the photo in `images/`, run `/digitize`, answer
  only flagged lines. No manual OCR or amount-checking pass.
- Errors shift from "silently wrong recipe" to "explicit flag on the
  ambiguous line" — review effort scales with photo quality.
- The pipeline depends on macOS (Apple Vision via pyobjc, `sips`) and an
  interactive Claude Code session; it is not a headless batch script.
- `images/manifest.json` tracks digitization state and lives, deliberately,
  inside gitignored `images/` — it describes local photos and travels with
  them.
