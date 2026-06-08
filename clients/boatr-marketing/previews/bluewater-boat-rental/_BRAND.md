# _BRAND.md — Blue Water Boat Rental (bluewater-boat-rental)

*Measured 2026-06-07. Method: downloaded the prospect's own logo files and homepage CSS; extracted dominant opaque pixels programmatically with Pillow (full-resolution pixel counts, not eyeballed). Source files: `blue-water-boat-rental-round-logo.png` (1200x1200), `favicon.png` (64x64), `logo-mobile.png` (400x298, white-on-transparent nav variant), homepage `<style>` blocks.*

## Measured palette

| Role | Hex | Source / pixel evidence |
|---|---|---|
| Primary | `#0276BD` | Logo's dominant blue — 177,471 px in the round logo (full res, exact value); also appears 15x in their site CSS |
| Secondary (dark) | `#064872` | Logo's dark navy ring/wave — 62,626 px |
| Supporting cyan | `#0FB2E4` | Logo's bright cyan wave — 55,790 px |
| Accent (CTA) | `#EDF000` | Their actual BOOK NOW button: `.et_pb_button{background-color:#edf000; color:#000000}` and active-nav highlight. A variant `#FFF000` appears on one button — standardize on `#EDF000` |
| Accent text | `#000000` | Black text on the yellow CTA (their own rule, `!important`) |
| Neutral / body text | `#666666` | `body{color:#666}` in their CSS |
| Headings | `#333333` | `h1..h6{color:#333}` |
| Background | `#FFFFFF` | `body{background-color:#fff}`; header is white (`#main-header{background-color:#fff}`) |
| Logo knockout white | `#F8F8F8` | 100% of opaque px in the white nav logo variant; 70.7% of the round logo (text + lifering) |

## Typography

- Headline font family: `Open Sans` (Divi theme, weight 500, no custom heading font set)
- Body font family: `Open Sans, Arial, sans-serif` (`font-size:14px; line-height:1.7em; font-weight:500`)
- Google Fonts equivalent: **Open Sans** (already a Google Font — load weights 500/600/700)

## Imagery feel

Bright, sunny, saturated South-Florida marina photography: boats at the dock, aerial Peanut Island shots, real customers aboard, daylight blue water. Functional and friendly rather than polished travel-magazine — real fleet photos on white/blue cards. Source new images from their own uploads (`/wp-content/uploads/`) first.

## One-sentence vibe

Clean nautical blue-on-white with a loud safety-yellow "BOOK NOW" punch — a no-nonsense, family-friendly marina operation that sells fun, not luxury.

## CSS variable mapping (template swap)

Every CSS variable in the preview derives from the values above:

- `--leaf` (primary) → `#0276BD`
- dark/nav/footer derivative → `#064872`
- light/section-tint derivative → tint of `#0FB2E4`
- CTA/button accent → `#EDF000` with `#000` text
- body text → `#666666`, headings `#333333`, page bg `#FFFFFF`

(Exception per PREVIEW_TEMPLATE.md: the AI editor widget keeps Boatr's own `--b-dark #0F172A` / `--b-orange #FE8D01` chrome — platform brand, not prospect brand.)
