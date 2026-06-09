# Fay's Diner & Cafe — Relaunch preview

Generated 2026-06-08. Source of truth for narrative + audit data: `../../prospect_faysdiner.md`.

## Deploy path

Drop this folder into the Relaunch monorepo at:

```
C:\Users\Nsini\Code\relaunch\relaunch-website\previews\fays-diner\
```

Then from PowerShell:

```powershell
cd C:\Users\Nsini\Code\relaunch\relaunch-website
git add previews/fays-diner
git commit -m "Add Fay's Diner preview"
git push origin main
```

Netlify auto-deploys → `tryrelaunch.com/previews/fays-diner/` in ~60 seconds.

## Pages

| Path | Purpose | edit-* tags |
|------|---------|-------------|
| `index.html`        | Home — hero + stats + about + 4 featured dishes + 3 service cards + quote + FAQ | 42 |
| `menu.html`         | Full real menu — 15 sections, **125 items**, grouped Breakfast / Kids / Lunch / Dinner | 376 |
| `hours.html`        | Hours grid (split Wed–Sat dinner), all-day-breakfast note, location, embedded map, parking | 42 |
| `reservations.html` | Table-request form + birthdays + private parties / groups | 25 |
| `contact.html`      | Full NAP, social links (FB / IG / Yelp), hours, message form | 22 |

**507 total `edit-*` tags** sitewide — every meaningful piece of copy is addressable by the edit widget.

## Structure

```
fays-diner/
├── index.html              ← 5 final pages, banner + widget inline per page
├── menu.html
├── hours.html
├── reservations.html
├── contact.html
├── README.md               ← this file
├── assets/
│   ├── css/site.css        ← Fay's palette + cafe layout
│   ├── js/site.js          ← mobile nav, active-link highlight
│   └── images/             ← (empty — placeholder hero gradients until real photos arrive)
└── _build/
    ├── build.py            ← regenerate any time from this script
    ├── menu.json           ← the real 125-item menu scraped from faysdiner.com
    ├── template.html       ← page skeleton with {{TOKENS}}
    ├── banner.html         ← Relaunch SEO banner (sitewide)
    └── widget.html         ← Relaunch edit widget (sitewide)
```

Regenerate all 5 HTML files after editing content:

```bash
cd previews/fays-diner
python3 _build/build.py
```

## Brand palette

Bright all-day California cafe — turquoise + sun-yellow + tomato on warm cream. Chosen to match the actual business (an upscale-casual, breakfast-forward diner — $20 French toast, Filet Oscar at dinner — **not** a 1950s chrome-and-neon kitsch place).

- `--fd-teal:  #1c8c86`   primary — classic diner turquoise
- `--fd-sun:   #f2b33d`   accent / CTA — egg-yolk yellow
- `--fd-red:   #d24a3a`   tomato — mark + section rules
- `--fd-cream: #fbf4e6`   warm page ground
- `--fd-ink:   #232a2c`   cool charcoal text

Display font: **Fraunces** (warm modern serif). Body: **Inter**. The mark is a circular tomato-red badge with a sun-yellow ring and an "F" — no logo file needed.

## Menu — this is the real thing

`menu.json` is the **actual current menu**, scraped from faysdiner.com on 2026-06-08: 125 items across 15 sections, grouped into Breakfast (incl. Benedicts, omelettes, burritos, sides), Kids, Lunch (salads, sandwiches, burgers, desserts), and Dinner (starters, entrees, chef's specials). Names, prices, and descriptions are verbatim from their site. `(V)` and `(GF)` markers are pulled through into vegetarian / gluten-free badges.

This is a deliberate contrast point with the live site: **their menu already exists in HTML but carries zero `Menu` schema.** The rebuild puts every one of these 125 items into machine-readable `MenuItem` markup.

## Schema injected

Each page carries `BreadcrumbList` + `FAQPage` (5 Q&A per page · 25 sitewide).

Plus, on **index / menu / hours / contact**, a full `Restaurant + LocalBusiness` entity with:
- NAP + `GeoCoordinates` (⚠ approximate — see open items)
- **`OpeningHoursSpecification` × 3** encoding the split schedule: Sun–Tue 06:30–15:00; Wed–Sat 06:30–15:00 **and** 16:00–20:00. This is the standout schema win — their unusual "dinner only Wed–Sat" hours are exactly what `OpeningHoursSpecification` exists to disambiguate, and the live site gives Google nothing.
- `servesCuisine`, `priceRange`, `sameAs` (Facebook / Instagram / Yelp)
- `amenityFeature` (all-day breakfast, dinner Wed–Sat, kids menu, vegetarian + gluten-free options, takeout, private parties, wheelchair accessible)
- Full nested `Menu → MenuSection → MenuItem` graph — **all 125 items, priced.**

`AggregateRating` is **deliberately not stubbed in** — connect real Google/Yelp reviews before publishing. Fake star ratings poison both AI search and the customer relationship.

`reservations.html` carries Breadcrumb + FAQ only; the Restaurant entity is already discoverable from its sister pages.

## Banner

Locked narrative from `../../prospect_faysdiner.md`. Lead detail is the **broken link preview** — `og:site_name` is the literal word "null" and `og:description` is "..." on the live site. Other verified ammo: zero structured data, 15 H1s (first = a map-pin icon + the address), insecure `http://` in share data, and the fact they're **already paying SpotHopper** for the site that shipped this way.

Two auto-flagged "tells" were checked and **rejected** as not defensible (documented in the prospect doc and not used in the banner): the `email@example.com` form-validation hint, and the `tel:` JS templates that actually render to working tap-to-call links.

CTA → `tryrelaunch.com/onboard?business=Fay's Diner`. Banner palette: teal + sun + tomato.

## Edit widget

Identical across all 5 pages. Three inline blocks (CSS + HTML + JS). POSTs to `/.netlify/functions/edit` (preview mode — temp edits, lost on refresh). Auto-discovers all `id="edit-..."` elements — 507 total.

## Build verification (2026-06-08)

- ✅ All 5 pages emit; JSON-LD parses on every page
- ✅ Exactly **1 `<h1>` per page** (source-clean — the live site has 15)
- ✅ Meta description present on every page; OG title/description/image all real (no "null", no "...")
- ✅ `og:url` and canonical on **https**
- ✅ Tap-to-call (`tel:+18583972530`) present 3–5× per page
- ✅ 125 menu items rendered in HTML **and** present in `Menu` schema (15 sections)
- ✅ No stray `--ch-` variables, no leftover `{{TOKENS}}`

## Open items before publishing

### Owner confirmation required
- [ ] **Hours** — confirm the split Wed–Sat dinner service (4:00–8:00 PM) and that Sun/Mon/Tue close at 3:00 PM are still current. Pulled from the live site 2026-06-08.
- [ ] **Menu** — 125 items are verbatim from the live site, but a few price cells were merged into descriptions on the source (e.g. Pancakes "Short $14 / Full $16", Soup "Cup/Bowl"). These render fine but read the menu page once to confirm nothing looks odd. Confirm there are no 86'd items.
- [ ] **Reservations** — does Fay's actually take reservations, or is it walk-in only? The live site listed "Reservations," so the page assumes yes. If walk-in only, repoint that nav item to a "Private Parties" page instead.
- [ ] **Private parties / catering** — page asserts Fay's hosts small private parties and can do group orders. Confirm before publishing.

### Asset upgrades needed
- [ ] **All photos.** Pages use CSS gradient placeholders. Pull real food + interior shots — Instagram `@faysdiner` is the obvious source. Needed: a hero (interior or a hero plate), the 4 featured-dish photos, and a real `assets/images/og-hero.jpg` for the link preview (currently referenced but not present).
- [ ] **Logo** — an actual "Fay's" wordmark/SVG would replace the CSS-built circular "F" mark.

### Schema gaps
- [ ] **Confirm `lat`/`lng`** in `build.py` — currently **approximate** (32.90981, -117.09972) because the live site renders its map via JS and exact coords weren't in the source. Verify against the Google Business Profile pin.
- [ ] Wire `AggregateRating` to real Google/Yelp reviews via API once review counts are confirmed.

### Functional integrations (live-customer phase)
- [ ] Reservation form currently `alert()`s — wire to Resy / OpenTable / Yelp Reservations / direct email-to-host at go-live.
- [ ] Contact form same — wire to email or CRM.
- [ ] Takeout currently "call (858) 397-2530." Worth pricing an online-ordering integration (Toast / ChowNow / Square) as an upsell — they already route ordering through SpotHopper today.
- [ ] PIN auth + edit-persistent function for the live editor (Section 7 of RELAUNCH_OPERATIONS.md).

### SEO follow-ups (post-launch)
- [ ] Pull Ahrefs data (DR, organic keywords, top pages, competitors) for "breakfast scripps ranch," "diner scripps ranch," "all day breakfast san diego" once the preview is in front of the owner. Keep to owner-readable depth per `feedback_banner_metrics`.
- [ ] PageSpeed score — `audit.py` 429'd again (Google throttles the sandbox IP). Retry from a different network; optional, the OG/schema/H1 ammo carries the banner.
- [ ] Screenshot the live "null" / "..." link-preview card (text it to yourself) — it's the single best proof point for the banner and the cold email.

## Reproducibility note

Built by `_build/build.py` from templates + `menu.json`. To change banner copy, palette, navigation, or footer, edit the templates in `_build/` then re-run `python3 _build/build.py`. All 5 HTML files regenerate in under a second.
