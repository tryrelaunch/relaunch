# _BRAND.md — Monhegan Boat Line

*HARD-RULE artifact. Palette measured programmatically from the prospect's own logo + hero photography (not eyeballed). Every CSS variable in the preview derives from this file.*

**Source assets measured:** `images/logo.png` (their `mbl-2.png`), `images/hero1.jpg`–`hero3.jpg` (their homepage slideshow), `images/laurab.jpg`, `images/elizabethann.jpg`.
**Method:** PIL/NumPy. Logo: opaque-pixel quantization + saturated-blue cluster average. Heroes: downscaled mean + saturated-cluster + warm-highlight extraction.
**Measured:** 2026-06-10.

---

## Color palette (measured)

| Role | Hex | How it was measured |
|---|---|---|
| **Primary — nautical blue** | `#0060A0` | Dominant saturated color in the logo (mode of quantized opaque pixels, 7.8% — the single most common colored pixel). This is the recognizable Monhegan Boat Line logo blue. |
| **Primary dark — navy** (nav, footer, headers) | `#003960` | Shade of the logo blue at L×0.6. Used for dark chrome / depth. |
| **Secondary — steel blue** (section accents, water) | `#48607D` | Saturated-cluster average of hero1 (the blue water/sky homepage slide). |
| **Accent / CTA — sunset gold** | `#C8842D` | Saturated reading of the warm golden-hour tones measured in hero2/hero3 (`#A87B5A`, `#AE8B5D`). Drawn from their own sunset photography; high contrast against the blue. |
| **Ink / body text** | `#312D2E` | Average of the darkest (lettering) pixels in the logo — a warm charcoal, not pure black. |
| **Background — light** | `#F4F8FB` | Very light blue-tinted white to sit under the blue palette. |
| **Surface white** | `#FFFFFF` | Cards, panels. |

CSS-variable mapping (apply to the template's `<style>` var block, keep names, swap values):
```
--leaf / primary       → #0060A0
--green-lt / secondary → #48607D
dark chrome            → #003960
accent / CTA           → #C8842D
text/ink               → #312D2E
bg                     → #F4F8FB
```
The Boatr widget chrome (`--b-dark` #0F172A, `--b-orange` #FE8D01) stays as-is — that's the platform widget, not the prospect's palette.

## Typography

- **Headline:** `Lora` (Google Font). Warm, classic serif — fits a heritage brand (1943 Laura B, "old-fashioned memories," a century of year-round service). Conveys longevity the way a generic sans can't.
- **Body:** `Source Sans 3` (Google Font). Clean, highly legible at small sizes — important because most Jan–Apr planning traffic is on phones.
- Add the two `<link>`s to `<head>`; swap the template's `font-family` declarations on `body`, `h1`–`h6`.

## Imagery feel

Warm, golden-hour, working-harbor documentary — boats at the dock, sunset water turning the bay gold, lobster gear, candid family-on-the-water moments. New England coastal and a little nostalgic, not polished travel-magazine. Their own slideshow photos already carry this; reuse them (re-export at higher res from the media library, compress to WebP). Do not replace with slick stock or AI imagery — the weathered authenticity is the brand.

## Vibe (one sentence)

The original and only year-round ferry to Monhegan — a weathered, trustworthy Maine institution that's carried passengers, mail, and freight across Muscongus Bay for generations.
