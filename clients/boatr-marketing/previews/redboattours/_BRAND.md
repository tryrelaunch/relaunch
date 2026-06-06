# Red Boat Tours — Brand Doc (source of truth for the preview's theme)

*Extracted 2026-06-06 from Red Boat Tours' own assets (logo, watermark, BYOB + awards graphics, site photos). Every CSS variable in `index.html` derives from this doc. Do not theme by instinct; change this doc first, then the variables.*

## The vibe

Playful, hand-drawn, family-first. The logo is bouncy cartoon lettering in bright cherry red with a white pelican mascot standing on a little red boat over sky-blue splashes (the boat is named *Pellicano* — the pelican IS the brand). Tagline on the live site: "Your Family Friendly Choice in St. Augustine!" This is a sunny red-white-and-blue family brand, NOT a corporate marine/teal brand. If the preview reads "sleek nautical agency," it's wrong; it should read "the fun red boat the kids remember."

## Color palette (measured, not guessed)

| Role | Hex | Source |
|---|---|---|
| **Boat Red** (primary, CTAs, brand marks) | `#FF000C` | exact dominant pixel of the logo lettering |
| **Hull Red** (hover/darker red) | `#C2262E` | boat-hull shading in the logo |
| **Splash Blue** (secondary, light accents) | `#25AAE1` | exact water-splash blue (logo + watermark + BYOB graphic) |
| Deep Ocean (dark sections; Splash Blue darkened) | `#0F3D5C` / `#14517A` / `#1A6396` | derived: hue of #25AAE1 at low lightness |
| Light Splash (accent text on dark) | `#8FD4F4` | derived tint of Splash Blue |
| Charcoal ink (body text) | `#1F242B` | #202020 text in their BYOB graphic, slightly tempered |
| Sunny Gold (award accents) | `#D9A93F` | gold in the USA Today 10Best badge art |
| Warm sand / cream neutrals | `#F4E4C1` / `#FDFBF6` | beach-day neutrals consistent with their sunny photo library |

Rule of thumb: red is for action (buttons, brand), blue is for atmosphere (darks, accents), white/cream carries the page. Red and teal never mix — there is **no teal anywhere** in this brand.

## Typography

The logo face is hand-drawn rounded comic lettering. Their WordPress site's computed fonts can't be read headlessly, so these are the closest Google-Font matches to the brand's own lettering (flagged for Nate's approval):

- **Headings:** `Baloo 2` (bold weights) — bouncy and rounded like the logo, but readable at headline length. Harder-match alternatives if Nate wants to go fuller cartoon: `Luckiest Guy`, `Chewy`.
- **Body:** `Nunito` — friendly rounded sans that doesn't fight the headings.
- Script accent (`Caveat`) carried over from the template for handwritten touches only.

## Imagery feel

Real photos only, theirs: dolphins mid-jump, the big red *Pellicano*, golden-hour sunsets, families on deck, holiday lights on the water. Bright, saturated, daylight-forward. No stock, no AI, no moody desaturated edits.

## Voice cues (for any new copy)

Family-first, warm, a little playful ("The yardwork can wait one more day"), proud of the crew and the awards. Captain Tony's line is the brand promise: "We're not happy unless you're ecstatic."
