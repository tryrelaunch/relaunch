# CH Steak Lounge — Relaunch preview

Generated 2026-05-24. Source of truth for narrative + audit data: `../prospect_chsteaklounge.md`.

## Deploy path

Drop this folder into the Relaunch monorepo at:

```
C:\Users\Nsini\Code\relaunch\relaunch-website\previews\ch-steak-lounge\
```

Then from PowerShell:

```powershell
cd C:\Users\Nsini\Code\relaunch\relaunch-website
git add previews/ch-steak-lounge
git commit -m "Add CH Steak Lounge preview"
git push origin main
```

Netlify auto-deploys → `tryrelaunch.com/previews/ch-steak-lounge/` in ~60 seconds.

## Pages

| Path | Purpose | edit-* tags |
|------|---------|-------------|
| `index.html`        | Home — hero + stats + about + menu tease + music tease + 6 service cards + quote + FAQ | 48 |
| `menu.html`         | Full menu — 6 sections, 24 items, prices, descriptions, flag badges | 102 |
| `music.html`        | Live-music schedule (7 events), how-it-works, band-pitch CTA | 23 |
| `hours.html`        | Hours grid, happy hour card, location, embedded Google Map, directions, parking | 50 |
| `reservations.html` | Reservation request form + private events + large-party section | 25 |
| `contact.html`      | Full NAP, social links (Char & CH), hours, message form | 23 |

**271 total `edit-*` tags** — every meaningful piece of copy is addressable by the edit widget.

## Structure

```
ch-steak-lounge/
├── index.html              ← 6 final pages, banner + widget inline per page
├── menu.html
├── music.html
├── hours.html
├── reservations.html
├── contact.html
├── README.md               ← this file
├── assets/
│   ├── css/site.css        ← brand palette + restaurant layout
│   ├── js/site.js          ← mobile nav, active-link highlight
│   └── images/             ← (empty — placeholder hero gradients until real photos arrive)
└── _build/
    ├── build.py            ← regenerate any time from this script
    ├── template.html       ← page skeleton with {{TOKENS}}
    ├── banner.html         ← Relaunch SEO banner (sitewide)
    └── widget.html         ← Relaunch edit widget (sitewide)
```

To regenerate all 6 HTML files after editing content:

```bash
cd previews/ch-steak-lounge
python3 _build/build.py
```

## Brand palette

Steakhouse-evening palette — oxblood + cream + brass on a charcoal/sepia ground:

- `--ch-oxblood: #6e1f1f`   primary — namesake & mark
- `--ch-cream:   #f3e7c8`   warm tablecloth cream
- `--ch-brass:   #c19a3c`   accent / CTA
- `--ch-ink:     #1a1310`   text / dark backgrounds
- `--ch-ember:   #b8311c`   "Hot" flag accent

Display font: **Playfair Display** (menu items, headings). Body: **Inter**.

All defined in `assets/css/site.css`. Mark is a circular oxblood badge with a brass ring and "CH" wordmark — no logo file needed.

## Schema injected

Each page carries:
- `BreadcrumbList`
- `FAQPage` (5 questions/page · 30 total sitewide)

Plus per-page:
- **index, menu, hours, contact:** full `Restaurant + LocalBusiness + BarOrPub` with `OpeningHoursSpecification` (Mon–Thu + Fri–Sat blocks), NAP, geo (lat/lng pulled from the embedded Google Map iframe on `/location/`), `priceRange`, `servesCuisine`, `amenityFeature` (live music, full bar, happy hour, carry-out, reservations, wheelchair accessible), `sameAs` (Facebook/CharCookeville, Twitter/charcookeville, Restaurant Guru/Char-Cookeville), and a full nested `Menu` → `MenuSection` → `MenuItem` graph with all 24 items priced.
- **music.html:** full Restaurant schema + 7 individual `MusicEvent` blocks per band, with `performer`, `location` (full address), `organizer` (linked to the Restaurant @id), and `offers` (no cover).
- **reservations.html:** Breadcrumb + FAQ only — the Restaurant schema is already discoverable from sister pages.

`AggregateRating` is **deliberately not stubbed in** — connect real Google Reviews before publishing. Fake star ratings poison both AI search and the customer relationship.

## Banner

Locked narrative from `../prospect_chsteaklounge.md`. Lead with the three indefensible details:

1. **MySpace** is still a survey option on the homepage. "Magzine" typo (sic) has been live since 2016.
2. **Contact page has no phone, no address, no email** — just a form.
3. **Zero structured data.** Google can't tell it's a restaurant. Menu items with prices on the homepage, none of it in `Menu` schema.

Plus the Char/CH brand-split angle as a real business problem.

CTA → `tryrelaunch.com/onboard?business=CH%20Steak%20Lounge`

Banner palette adapted to CH brand (oxblood + cream + brass).

## Edit widget

Identical across all 6 pages. Three blocks (CSS + HTML + JS) inline per page. POSTs to `/.netlify/functions/edit` (preview mode — temp edits, lost on refresh).

Auto-discovers all elements with `id="edit-..."` — 271 total across the site.

## Open items before publishing

### Owner confirmation required
- [ ] **Steak section** in `menu.html` is fully placeholder — Filet, Ribeye (12 oz & 16 oz), NY Strip, Top Sirloin, Surf & Turf. The live site barely mentions steaks despite being the namesake. Confirm cuts, weights, and prices, or replace with the actual steak menu.
- [ ] **Burgers & Sandwiches section** is placeholder — the CH Burger, Smoked Brisket, Buffalo Chicken. Live site says "biggest burger in Cookeville" but no detail. Confirm or replace.
- [ ] **Sides** are placeholder at $5 each. Confirm pricing and lineup.
- [ ] **Music calendar** in `music.html` is 7 placeholder bands (The Whiskey Dogs, Hattie Mae & The Holler, Lonesome Pine String Band, etc.). Replace with real upcoming acts before going live.
- [ ] **Hours grid** matches what's on `/hours/` — Mon–Thu 11a–9p, Fri–Sat 11a–10p, closed Sun. Confirm no recent changes.
- [ ] **Happy hour** — $7 apps / $2.50 drafts / $4 wells & wine. Pulled from live site; confirm still current.
- [ ] **Brand decision** — sitewide assumes CH Steak Lounge as primary, with "formerly Char" cross-references in Contact + Home. If owner wants to re-unify under Char, swap throughout.

### Asset upgrades needed
- [ ] **All photos.** Site currently uses CSS gradients as hero placeholders. The 2016 JPEGs on the live site (`slide4`, `slider`, `slide3`) are 1290×602 — usable as a starting point but the modern hero wants 2400×1200+. Ideal:
  - Hero: warm interior shot, dim lights, the bar visible
  - Steak hero: a finished plate, low angle, on the wood table
  - Music hero: a band on stage, audience visible, warm tones
  - Logo: an actual CH wordmark / monogram SVG would replace the CSS-built circular mark
- [ ] **Owner photo or chef portrait** — useful for an About page once we build one out (currently just an About section on the home page).

### Schema gaps
- [ ] Wire `AggregateRating` to real Google Reviews via API.
- [ ] Add `priceRange` granularity once steak prices are confirmed.
- [ ] Confirm lat/lng (`36.16220851, -85.50112968`) — pulled from the Google Maps embed iframe coordinates; verify against the actual storefront.

### Functional integrations (live-customer phase)
- [ ] Reservation form currently `alert()`s. Wire to one of: OpenTable / Resy / Yelp Reservations / direct email-to-host / POS integration.
- [ ] Contact form same — wire to email or CRM.
- [ ] Carry-out — currently "call (931) 520-2427." Worth pricing a real online-ordering integration (Toast, ChowNow, Square) as upsell.
- [ ] PIN auth + edit-persistent function for the live editor (Section 7 of RELAUNCH_OPERATIONS.md).

### SEO follow-ups (post-launch)
- [ ] Pull Ahrefs data (DR, organic keywords, top pages, competitors) once preview is in front of owner — banner can be sharpened with real keyword data.
- [ ] PageSpeed score — retry `audit.py` once Google's daily quota resets (was 429'd on 2026-05-24).
- [ ] Scrape `/menu/` page on the live site to see if their published menu is HTML or a JPEG/PDF (would strengthen the banner if image-only).

## Reproducibility note

This preview was built by `_build/build.py` from templates. To change banner copy, palette, navigation, or footer, edit the templates in `_build/` then re-run `python3 _build/build.py`. All 6 HTML files regenerate in under a second.
