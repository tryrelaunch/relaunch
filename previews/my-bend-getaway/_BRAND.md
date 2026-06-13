# _BRAND — My Bend Getaway

*Required brand doc (HARD RULE: no build without it). Palette derived from the prospect's own logo + live site, 2026-06-12.*

## One-sentence vibe
Retro-outdoor Bend energy made sleek — a golden sun over the Cascades, coral and teal, big mountain photography, and clean modern type. Bold and adventurous, but easy to book.

## Palette (CSS variables)
| Token | Hex | Role | How derived |
|---|---|---|---|
| `--brand-primary` | `#FF6B5A` | Coral — primary CTA, links, "Book" buttons | **Measured** (computed style of the live site's BOOK NOW links + dominant colored bg) |
| `--brand-sun` | `#F5BE00` | Golden sun — highlights, accents, hover | Read from logo (zoom-sampled) |
| `--brand-teal` | `#36BCD4` | Teal water — secondary accent, tags, icons | Read from logo (zoom-sampled) |
| `--brand-earth` | `#6E4326` | Mountain brown — deep accents, footer | Read from logo (zoom-sampled) |
| `--ink` | `#2A2622` | Warm near-black — body text, headings | Refined from site `#333333` |
| `--ink-soft` | `#6B6259` | Muted brown-gray — secondary text | Derived |
| `--bg` | `#FFFFFF` | Page background | Measured (site bg) |
| `--bg-warm` | `#FBF6EF` | Warm off-white — alternating sections | Derived to sit under the sun/coral |
| `--line` | `#ECE4D9` | Hairlines, card borders | Derived |

Gradient signature (from the wordmark): coral → sun, `linear-gradient(90deg, #FF6B5A, #F5BE00)`. Use sparingly for hero accents / the logo lockup, not body UI.

## Type
- **Current site:** Abril Fatface (display) + Lora (serif). Reads dated/wedding-y, not "sleek modern."
- **Rebuild direction:** modernize while keeping warmth and a bold display voice.
  - **Headings:** a strong contemporary display/grotesk — proposed **Fraunces** (high-contrast serif, has personality, still modern) *or* **Clash/Archivo**-style geometric if we want sharper. Lead choice: **Fraunces** for headings.
  - **Body/UI:** clean, legible sans — proposed **Inter** (or **Plus Jakarta Sans**).
  - One display + one sans, nothing more.

## Imagery feel
- Big, bright Cascade + Deschutes River photography; warm golden-hour where possible.
- Their own listing photos (Lodgify CDN, `l.icdbcdn.com`) are the primary source — use them per unit.
- Lifestyle: bikes, floats/rafts on the river, downtown Bend, snow at Mt. Bachelor. Adventurous but inviting.
- Avoid generic "anywhere" stock; this is a specific, walkable Bend brand.

## Logo
- Retro badge: golden sun, brown Cascade peaks with snowcaps, teal water lines, arched coral→gold "MY BEND GETAWAY" wordmark.
- Only asset on hand is the Lodgify CDN PNG (`5e177100-...png`). **Request vector/hi-res from Nate** for crisp nav + footer use.

## Do / Don't
- **Do** anchor CTAs in coral, accent with sun + teal, keep generous whitespace and large type.
- **Do** modernize the retro feel — keep the sun/mountain motif as a subtle accent, not a literal sticker.
- **Don't** ship the EUR currency bug, the "Home" title, or "Powered by Lodgify" branding.
- **Don't** fabricate review counts, ratings, or amenities not in `_INTAKE.md`.
