# _BRAND — High Style Yachts (M/Y Tourbillon)

*HARD RULE artifact. Palette MEASURED programmatically (k-means) from the prospect's own logo + brand photos on 2026-06-12. Every CSS variable in the preview derives from the values below. Not eyeballed.*

## Source assets measured
- `logo.png` (500×389, original Wix media `61a767_2714…png`) — primary source of truth
- `hero_tourbillon.jpg`, `sportfish.jpeg`, `interior.jpg` — confirm ocean/teak tones

## Measured palette (from the logo, white dropped)

| Role | Hex | Source (measured) | Use |
|---|---|---|---|
| Ink / darkest | `#0E1130` | logo `#0E0F2A` (27%) | hero overlay, footer, dark sections |
| **Primary** (deep navy) | `#151A64` | logo `#151A64` (24%) | brand, nav, headings |
| **Secondary** (cobalt) | `#2C3CA0` | logo `#2C3CA0` (24%) | links, secondary accents, section accents |
| Warm accent (measured) | `#6B4E2F` | logo bronze (7.8%) | source hue for the CTA gold below |
| **Accent / CTA gold** | `#C6A04B` | derived from measured bronze `#6B4E2F` (same warm hue, lifted for button legibility) | "Book / Call" CTAs, hovers, rule lines |
| Cream / light bg | `#F4F1EC` | logo cream `#D6D2CE` (11%), lightened | alternating section backgrounds |
| Neutral / body text | `#1B1E2A` | near-navy black | body copy |
| Page background | `#FFFFFF` | — | base |
| Ocean mid (optional tertiary) | `#3C6193` | photos (`#3C6193`/`#4071AA`) | image tints, info chips if needed |

Photo cross-check: ocean blues `#16406F · #4071AA · #3C6193`; warm teak/sand `#E0CCAA · #6B4E2F` — consistent with the navy+gold logo system.

## Typography
- **Headlines:** `Montserrat` (700/800), often all-caps — matches their current all-caps H1 treatment ("HIGH STYLE YACHTS — CABO SAN LUCAS"). Clean geometric sans, reads as premium charter.
- **Body:** `Inter` (400/500). Neutral, fast, high legibility on mobile.
- Add Google Fonts `<link>` for both to `<head>`; replace the template's font-family declarations.
- (Closest-match: current site is Wix default sans, no custom brand font to preserve.)

## Imagery feel
Aspirational blue-water luxury: marlin/sportfishing action, teak-and-leather yacht interiors, Cabo arches and sunsets. High-end but real — actual photos of the Tourbillon. Pull from their own Wix media (70% target); no AI-generated boats/captains/guests. Treat warm and bright; let navy + gold UI frame the photography.

## One-sentence vibe
A navy-and-gold luxury sportfishing yacht brand — Cabo blue water, tournament credibility, watch-grade refinement.

## CSS variable mapping (apply to template `<style>` — names stay, values become these)
```
--ink:      #0E1130;
--primary:  #151A64;   /* was template marine default */
--secondary:#2C3CA0;
--accent:   #C6A04B;   /* CTA gold */
--accent-d: #6B4E2F;   /* deep bronze for hovers/borders */
--cream:    #F4F1EC;
--text:     #1B1E2A;
--bg:       #FFFFFF;
--ocean:    #3C6193;
```
*Map these onto whatever the template's actual variable names are (`--leaf`, `--green-lt`, etc.) — do not change the variable names, only the values, and sweep for hardcoded rgba().*
