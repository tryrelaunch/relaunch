# Moore Than Clean — Relaunch Preview

**Client:** Moore Than Clean (moorethanclean.com)
**Owner/Technician:** Jacob Moore — 541-305-8600 — Info@moorethanclean.com
**Location:** Prineville, Oregon
**Built by:** Boatr Marketing for Relaunch · tryrelaunch.com

---

## What's preserved (their existing site)

Every word of their original copy stays exactly as written:

- **Hero tagline:** "Your Floor Deserves Moore"
- **Hero subhead:** "Professional Carpet Cleaning Services Based in Prineville, Oregon"
- **Hero subtext:** Original eco-friendly statement
- **About / Mission:** Full mission statement preserved verbatim
- **All 9 services:** Residential, Commercial, Upholstery, Mattress, Auto & RV, Rugs, Tile, Stain & Odor, Fabric Protectant — every description used word-for-word
- **Contact info:** Phone, email, hours, social links
- **Tagline:** "Don't settle for clean, get Moore than clean."
- **Products We Trust:** All 7 product names and truckmountforums.com links preserved exactly
- **Reviews:** Reviewer names from current Google reviews (Gerald Lee, Ginny Beard, Tom Joy)

URL structure preserved: `/`, `/gallery`, `/products-we-trust`

---

## What's new (the SEO upgrade)

### 1. Individual service pages (the big one)

Their current site has all 9 services as cards on the homepage — Google sees one page when it should see nine. We added dedicated pages for the four most searchable:

- `/residential-carpet-cleaning` — targets "residential carpet cleaning Prineville"
- `/commercial-carpet-cleaning` — targets "commercial carpet cleaning Prineville Oregon"
- `/upholstery-cleaning` — targets "upholstery cleaning Prineville"
- `/tile-and-grout-cleaning` — targets "tile and grout cleaning Prineville"

Each page has 500-800 words of original content, full Service schema markup, FAQ schema for AI search visibility, and breadcrumb schema for rich results.

### 2. Schema markup (currently zero on their site)

Every page now ships with proper schema.org markup:

- **LocalBusiness** schema on home with full geo, NAP, areaServed (Prineville, Bend, Redmond, Madras), opening hours, aggregate rating (5.0/8 reviews), and full service offer catalog
- **Service** schema on each service page
- **FAQPage** schema for AI search visibility (ChatGPT, Perplexity, Google AI Overview)
- **BreadcrumbList** schema for rich results
- **AboutPage** + **ContactPage** + **ImageGallery** schemas where appropriate

### 3. NAP (Name/Address/Phone) consistency

Phone, email, location, hours appear the same way on every page — Google's local algorithm rewards this.

### 4. New pages

- `/about` — Jacob's story, family-owned narrative, eco-friendly philosophy
- `/contact` — dedicated contact page (currently buried in homepage scroll)
- `/faq` — comprehensive 35+ question FAQ covering pricing, drying time, pet stains, eco-friendly products, frequency, scheduling, warranties, and more — with full FAQPage schema for AI search citations (ChatGPT, Perplexity, Google AI Overview)

### 5. Relaunch live editor widget (the SaaS demo)

Floating button in the bottom-right corner of every page. Click it and Jacob can type changes — "change the hero photo", "add a holiday banner", "update the phone number" — and see what the live AI editor experience feels like.

This is the demonstration of what Relaunch's $99-499/mo subscription delivers: edits without code, without designers, without waiting. The widget runs as a self-contained mock in the preview (so it's safe to deploy without a live backend), but on a real Relaunch site it would wire into the production edit.js endpoint to push real changes.

---

## File structure

```
moore-than-clean/
├── index.html                      Home (preserves all current content)
├── residential-carpet-cleaning.html    [NEW — SEO win]
├── commercial-carpet-cleaning.html     [NEW — SEO win]
├── upholstery-cleaning.html            [NEW — SEO win]
├── tile-and-grout-cleaning.html        [NEW — SEO win]
├── about.html                          [NEW]
├── faq.html                            [NEW — 35+ Q&As, FAQPage schema, AI search bait]
├── gallery.html                        Gallery (preserved concept)
├── products-we-trust.html              Products (preserved verbatim)
├── contact.html                        [NEW — dedicated]
├── css/main.css                        Design system
├── js/main.js                          Mobile menu
├── js/relaunch-editor.js               [NEW — live editor widget, SaaS demo]
└── README.md                           This file
```

---

## Design choices

- **Palette:** Deep teal (#0e7187) as primary accent (clean, water, professional), coral/red (#d8412c) for CTAs (action, trust), gold (#d4a64a) for trust signals, navy (#0f1d2e) for type
- **Type:** Bricolage Grotesque (display) + Inter (body) — clean, modern, approachable
- **Modeled on:** triton-charters.com structure — same multi-page service-business architecture used for the boatr clients
- **Mobile-first:** Sticky nav with services dropdown on desktop, full mobile menu on smaller screens

---

## Photos

Hero, service page, and gallery photos are Unsplash placeholders. The about-page service van photo is **pulled directly from their existing site** (img1.wsimg.com hotlink). Same for the products-we-trust page — those product photos are theirs.

During onboarding we'd swap in:

- Real Jacob/team photos
- Before-and-after gallery from real Prineville jobs
- Service van photo (their own)
- Hero photo (could be the truck-mounted equipment, Jacob in action, or a clean carpet beauty shot)

---

## Reviews section

Featured reviews on the homepage use the **real reviewer names from Jacob's Google profile** (Gerald Lee, Ginny Beard, Tom Joy). The review text is paraphrased placeholder — during onboarding, we'd transcribe exact review text or pull dynamically from the Google reviews API.

---

## What still needs Jacob's input (during onboarding)

1. **Real review text** — currently paraphrased; need exact wording
2. **Photos of Jacob/team** — for hero, about, service pages
3. **Before/after gallery photos** — currently stock; would use real job photos
4. **Service area confirmation** — we listed Prineville/Bend/Redmond/Madras; should confirm full coverage
5. **Pricing positioning** — the "free estimate" CTA is everywhere; if there's a starting price he wants public, we can add it
6. **Review schema accuracy** — ratings/counts current as of preview build

---

## Going live

Drop the folder into Netlify or move to subfolder of an existing project. Update `<link rel="canonical">` and Open Graph URLs once final domain is confirmed (currently set to `https://moorethanclean.com/...` so SEO juice transfers cleanly to the new site).

The 301 redirects from old GoDaddy URLs to new URLs are critical for SEO preservation:

- `/` → `/` (no change)
- `/gallery` → `/gallery` (no change)
- `/products-we-trust` → `/products-we-trust` (no change)

All new URLs (about, service pages, contact) are NEW pages — no redirects needed, just sitemap inclusion.

---

Built by Nate Sinisgalli · Boatr Marketing · for Relaunch · tryrelaunch.com
