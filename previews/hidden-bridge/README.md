# Hidden Bridge Golf Club — Relaunch preview

Generated 2026-05-19. Source of truth for narrative + audit data: `../prospect_hidden_bridge.md`.

## Deploy path

Drop this folder into the Relaunch monorepo at:

```
C:\Users\Nsini\Code\relaunch\relaunch-website\previews\hidden-bridge\
```

Then from PowerShell:

```powershell
cd C:\Users\Nsini\Code\relaunch\relaunch-website
git add previews/hidden-bridge
git commit -m "Add Hidden Bridge Golf Club preview"
git push origin main
```

Netlify auto-deploys → `tryrelaunch.com/previews/hidden-bridge/` in ~60 seconds.

## Pages

| Path | Purpose | edit-* tags |
|------|---------|-------------|
| `index.html`      | Home — hero + stats + 6 service cards + quote + FAQ | 36 |
| `course.html`     | Scorecard, course map, local rules, distance markers | 42 |
| `rates.html`      | Green fees, cart rates, tee-time request form | 34 |
| `membership.html` | Junior / Individual / Family tiers + benefits | 24 |
| `events.html`     | Tournaments + leagues table, private events | 42 |
| `proshop.html`    | Snacks/drinks, rentals, lessons | 28 |
| `contact.html`    | NAP, hours, contact form, directions | 22 |

## Structure

```
hidden-bridge/
├── index.html              ← 7 final pages, banner + widget inline per page
├── course.html
├── rates.html
├── membership.html
├── events.html
├── proshop.html
├── contact.html
├── README.md               ← this file
├── assets/
│   ├── css/site.css        ← brand palette + Triton-adapted layout
│   ├── js/site.js          ← mobile nav, active-link highlighting
│   └── images/             ← 7 photos (pheasant logo + 6 course shots)
└── _build/
    ├── build.py            ← rebuild any time from this script
    ├── template.html       ← page skeleton with {{TOKENS}}
    ├── banner.html         ← Relaunch SEO banner (sitewide)
    └── widget.html         ← Relaunch edit widget (sitewide)
```

To regenerate all 7 HTML files after editing content:

```bash
cd previews/hidden-bridge
python3 _build/build.py
```

## Brand palette

Sampled from the pheasant logo (`assets/images/logo.png`):

- `--hb-maroon: #6f2a22`   primary — wordmark color
- `--hb-cream:  #f5ead0`   logo background
- `--hb-gold:   #c9933a`   accent / CTA
- `--hb-ink:    #1c1612`   text / dark mode
- `--hb-sky:    #5d87a8`   Big Horn Mountain backdrop tone

All defined in `assets/css/site.css`.

## Schema injected

Each page carries:
- `BreadcrumbList`
- `FAQPage` (5 questions/page · 35 total sitewide — meets Section 3 spec)

Plus per-page:
- **index.html, contact.html:** full `GolfCourse + LocalBusiness` with `OpeningHoursSpecification`, NAP, geo, amenityFeature (18 holes, Par 72, range, pro shop, carts, events), and additionalProperty (yardages, course rating, slope, opening year)
- **course.html, rates.html, membership.html, events.html, proshop.html:** `Service` schema linked back to the main `GolfCourse` entity

`AggregateRating` is **deliberately not stubbed in** — connect the owner's real Google reviews before publishing. Fake star ratings poison both AI search and the customer relationship.

## Banner

Locked narrative from `../prospect_hidden_bridge.md`. Lead with the three indefensible details:

1. Footer says ©2019, body says "open for the 2026 season"
2. Facebook icon links to `facebook.com/wix`
3. Scorecard, course map, and rates only exist as JPEGs/PDFs

CTA → `tryrelaunch.com/onboard?business=Hidden%20Bridge%20Golf%20Club`

Banner palette adapted to Hidden Bridge brand (maroon + cream + gold). Identical Spork-pattern structure across pages.

## Edit widget

Identical across all 7 pages per Section 5. Three blocks (CSS + HTML + JS) inline per page. POSTs to `/.netlify/functions/edit` (preview mode — temp edits, lost on refresh).

Auto-discovers all elements with `id="edit-..."` — 228 total across the site.

## Open items before publishing

### Owner confirmation required
- [ ] **Rates** in `rates.html` are placeholders matching Sheridan-area public-course norms. Confirm 2026 green fees, cart, junior, senior, twilight rates.
- [ ] **Membership pricing** in `membership.html` is placeholder. Confirm Junior / Individual / Family rates.
- [ ] **Tournament calendar** in `events.html` is a representative slate. Replace with the real 2026 event schedule.
- [ ] **Lat/lng** in schema is a Sheridan-centroid approximation. Replace with course-exact coordinates.
- [ ] **Hours** ("dawn until dusk, mid-April through October") needs confirmation.
- [ ] **Real social URLs** — replace the Wix-default Facebook/Twitter/LinkedIn links. (Currently no social block in footer; add after we know the real URLs.)

### Asset upgrades needed
- [ ] **Hi-res photos.** The 7 images in `assets/images/` are Wix-resized thumbnails — largest is 1526×480. Hero would benefit from a 2400×1200+ shot. Ideally:
  - Mountain-and-water shot (currently `hidden-bridge-2013-034.jpg` at 673×440) → needs 2400×1500
  - Sunset shot (currently 448×293) → needs 1920×1080
  - Logo → vector SVG would be ideal
- [ ] **Scorecard image** is legible at full size — keep as-is or commission a proper HTML rendering.
- [ ] **No driving-range or hole-by-hole photos** in the asset set. Pro shop interior, range, individual holes would round out the gallery.

### Schema gaps
- [ ] Wire `AggregateRating` to real Google Reviews via API.
- [ ] Confirm `openingHoursSpecification` validFrom/validThrough dates (currently 2026-04-15 to 2026-10-31 placeholder).
- [ ] Add `priceRange` to LocalBusiness once rates are confirmed.

### Functional integrations (live-customer phase)
- [ ] Tee-time form currently just `alert()`s. Wire to one of:
  - foreUP (most common for small public courses)
  - GolfNow / Chronogolf
  - Custom email-to-staff
- [ ] Contact form same — wire to email or CRM.
- [ ] PIN auth + edit-persistent function for the live editor (handled at customer-onboarding time per Section 7).

## Reproducibility note

This preview was built by `_build/build.py` from a small set of templates. If you change the banner copy, palette, navigation, or footer, edit the templates in `_build/` then re-run `python3 _build/build.py`. The 7 HTML files regenerate in under a second.

This pattern is the Section 4 roadmap item — "banner-content generator that takes audit JSON → banner HTML" — applied to a full 7-page build. The next step toward the auto-pipeline is parameterizing `build.py` to read a prospect JSON instead of hard-coding values.
