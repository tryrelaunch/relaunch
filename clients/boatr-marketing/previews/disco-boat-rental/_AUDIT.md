# Disco Boat Rentals — Audit + Migration Plan

*Created: 2026-05-23. Owner: Nate Sinisgalli (this is Nate's own business). Companion doc to `_INTAKE.md`. Audit run on public info only — items requiring owner facts are flagged `Needs verification` in-line and consolidated at the bottom.*

> **Stop point:** when this doc is read and approved, the next step is copy + page-by-page HTML. Do not write copy until Nate signs off on the architecture, URL map, schema plan, and page briefs below.

---

## TL;DR — the four things that matter

1. **There is almost nothing to protect.** The current site is essentially a one-page WordPress landing page plus a two-post blog. Total indexable URLs: 4. Both blog posts have real long-tail value (`disco party planning guide`, `mission bay vs san diego bay`) — those are the only URLs we treat as protected. Everything else is greenfield.
2. **The site is in "Waiting List" mode — there's no booking flow to preserve.** The primary CTA is a GoHighLevel waiting-list form (`link.boatrmarketing.com/widget/form/UKKEdzivMdsNJ2b5tZHI`). Rebuild should keep the same GHL form during the pre-launch phase and add a real booking flow once Nate flips to "open for bookings."
3. **Three concrete defects on the live site** need fixing on day one of the rebuild — they are NOT going to be carried forward: (a) footer address is wrong (Bahia Resort link / 92109 — actual is 2700 Shelter Island Dr / 92106); (b) the disco-party-planning-guide has a broken internal link to `/disco-party-decor-rentals/` that 404s; (c) the boat-rental-mission-bay post has a malformed CTA link (`/boat-rental-mission-bay/www.discoboatrentals.com`).
4. **Schema is missing entirely.** No LocalBusiness, no TouristAttraction, no FAQPage, no Service, no Product. The Boatr template ships with these baked in — that's an instant upgrade.

---

## 1. Current page inventory

Public-facing URLs found via crawl (`discoboatrentals.com`, plural, confirmed target):

| # | URL | Title | Published | Last modified | Word-count est. | Notes |
|---|---|---|---|---|---|---|
| 1 | `/` | Disco Boat Rentals \| San Diego's Newest Party Boat Rental | 2024-04-15 | 2026-03-30 | ~450 | Single landing page. Hero + four feature blocks (rooftop, fold-down windows, throwback interior, "meet the boat"). One CTA → waiting-list form. |
| 2 | `/articles/` | The Grooviest Articles \| Disco Boat Rental San Diego | 2025-06-18 | 2025-08-11 | ~120 | Blog index. Lists 2 posts. "Coming soon..." placeholder visible. |
| 3 | `/disco-party-planning-guide/` | Disco Party Planning Guide: How to Throw the Best Disco Bash | 2025-06-04 | 2025-06-05 | ~2,300 | Long-form (10-min read). Amazon affiliate-style with ~70 product links (most appear to be placeholder ASINs — needs verification). One broken internal link to `/disco-party-decor-rentals/`. |
| 4 | `/boat-rental-mission-bay/` | Boat Rental Mission Bay \| Disco Boat Rental | 2025-07-30 | 2025-08-13 | ~600 | Comparison piece: Mission Bay vs San Diego Bay. One malformed self-link at the bottom. One healthy outbound to coronadovisitorcenter.com. |

URLs NOT found (= structural gaps): `/about/`, `/contact/`, `/faq/`, `/book/`, `/pricing/`, `/captain/`, `/safety/`, `/bachelorette/`, `/birthday-parties/`, `/themed-charters/`, `/pride/`, `/sunset-cruise/`, `/the-boat/`, `/san-diego-bay/`, `/photo-gallery/`, `/sitemap.xml` (couldn't fetch — needs verification once we have hosting access), `/robots.txt` (couldn't fetch — same).

**Tech stack of the existing site:**

- WordPress, theme unknown, `performance-lab` plugin v4.1.0 (Google's WP performance plugin)
- Author byline credit: "David"
- Schema present: none visible in the HTML scrape (Boatr template will add it)
- Mobile viewport meta: `width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0` — fixed-scale (accessibility yellow flag, but not a blocker)
- Two-column footer with bad address Google Maps link to Bahia Resort Hotel (wrong)

---

## 2. Protect / Keep + improve / Redirect / Consolidate / Create / Remove

**Decision map for everything currently on the site:**

| URL | Action | Reason |
|---|---|---|
| `/` | **Keep + improve** | Homepage / entity page. New homepage gets full Boatr template chrome, real schema, multi-section content, but the URL stays. |
| `/articles/` | **Keep + improve** | Blog index. Keep URL, rebuild as `/articles/` (or move to `/blog/` — see decision below). Remove "Coming soon..." placeholder; populate with real article cards. |
| `/disco-party-planning-guide/` | **Protect** | Two-month-old long-form, ranks for "disco party planning guide" intent. Don't touch the URL. Strip the broken `/disco-party-decor-rentals/` link, audit the Amazon ASINs (most look like fake placeholders), keep the content shape. |
| `/boat-rental-mission-bay/` | **Protect (with fixes)** | Targets a real long-tail money keyword. Don't touch the URL. Fix the malformed self-link. Tighten the closing CTA so it actually points to the Disco Boat product, not to itself. |

**New URLs to CREATE (architecture decision below in §4):** all the use-case pages, destination/area pages, FAQ, about, contact, book, captain bio, pricing, photo gallery, plus the orphaned `/disco-party-decor-rentals/` since the disco-party-planning-guide already internally links to it.

**Nothing to REMOVE.** Live site is too small to consolidate or kill anything.

**Nothing to REDIRECT.** All existing URLs stay at their current slugs.

---

## 3. URL decision map

| Old URL | New URL | Action | Priority | Why |
|---|---|---|---|---|
| `/` | `/` | Keep + improve | P0 | Homepage. Rebuild as Boatr template, same URL. |
| `/articles/` | `/articles/` | Keep + improve | P1 | Blog index. Same URL. (Decision: stay on `/articles/`, don't move to `/blog/`. The brand voice already calls them "Groovy Articles," and `/articles/` is what's indexed.) |
| `/disco-party-planning-guide/` | `/disco-party-planning-guide/` | Protect | P0 | Top-of-funnel ranking content. Same URL. Fix broken internal link + audit Amazon ASINs. |
| `/boat-rental-mission-bay/` | `/boat-rental-mission-bay/` | Protect + fix | P0 | Money-keyword content. Same URL. Fix malformed self-link, rewrite closing CTA to actually push toward Disco Boat booking. |
| Missing | `/the-boat/` | Create | P0 | Dedicated page for the boat itself — specs, capacity, photos, what's onboard. The single most important "money page" for this business. |
| Missing | `/book/` | Create | P0 | Dedicated booking landing. Pre-launch = waiting-list form; post-launch = real booking flow. |
| Missing | `/pricing/` | Create | P0 | Charter rates, captain vs. self-drive delta, deposit, cancellation policy. (Currently invisible on the live site — that's a conversion-killer.) |
| Missing | `/faq/` | Create | P0 | FAQ page with 35+ questions (per BRAIN.md §3 step 5). Schema-rich. Drives AI Overview citations. |
| Missing | `/about/` | Create | P1 | The story of the boat, the build, the owner. Trust signals. E-E-A-T. |
| Missing | `/contact/` | Create | P1 | NAP, hours, parking, dock directions. LocalBusiness schema lives here too. |
| Missing | `/captain/` | Create | P1 | Captain bio + credentials + USCG status. Trust signal, especially for bachelorette / corporate inquiries. |
| Missing | `/bachelorette-party-boat-san-diego/` | Create | P1 | Use-case money page. Bachelorette is one of the two callouts on the current homepage — give it its own URL. |
| Missing | `/birthday-party-boat-san-diego/` | Create | P1 | Use-case money page. Same reasoning. |
| Missing | `/themed-charters/` | Create | P2 | 1970s disco night, pride events — the custom theme builds. Differentiator from competitors. |
| Missing | `/pride-boat-charter-san-diego/` | Create | P2 | Pride is called out explicitly on the live site as a theme build. SD has a huge Pride market. |
| Missing | `/sunset-cruise-san-diego/` | Create | P2 | Sunset rooftop disco-ball moment is the visual differentiator. Own the keyword. |
| Missing | `/self-drive-boat-rental-san-diego/` | Create | P2 | "Self-drive" is the marketing angle that distinguishes Disco Boat from captain-only competitors (Maverick et al). Worth its own URL. |
| Missing | `/captained-charter-san-diego/` | Create | P2 | Pair to the self-drive page. Lets the user pick. |
| Missing | `/san-diego-bay-boat-rental/` | Create | P2 | Area page. Companion to the existing `/boat-rental-mission-bay/` post. Together they form a topic cluster. |
| Missing | `/photo-gallery/` | Create | P2 | Real photos of the boat. Currently the site has ~6 — needs ~25+ once we pull from Instagram + any unposted shoot library. |
| Missing | `/disco-party-decor-rentals/` | Create | P2 | The `/disco-party-planning-guide/` post already links to this URL internally — it 404s today. Filling the gap fixes a known broken link AND opens a new revenue angle (rent the decor without the boat). Needs Nate verification on whether this is a real service offering. |
| Missing | `/sitemap.xml` | Create | P0 | Auto-generated on build. |
| Missing | `/robots.txt` | Create | P0 | Explicitly allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, anthropic-ai per AI_OVERVIEW_READINESS Pillar 4. |
| Missing | `/404.html` | Create | P0 | Branded 404. |

**No 301 redirects required.** No URLs are changing. (If Nate decides post-audit to consolidate any of the use-case pages, we add redirects then.)

---

## 4. Recommended new architecture

### The strategic call: multi-page, NOT single-page long-scroll

The canonical Boatr preview template (`_template/index.html`, modeled on Alligator Reef) ships as a **single long-scroll homepage** with anchored sections (`#fleet`, `#lighthouse`, `#sandbar`, `#sunset`). That works for Alligator Reef because they have 10 boats and 3 named destinations — the long-scroll absorbs the variety.

Disco Boat is the opposite case: **one boat**, lots of **use cases** (bachelorette, birthday, pride, themed, sunset). Per the practitioner refinement in `GOOGLE_2026_SEO_FINDINGS.md` §11 ("consolidate when you have authority, fragment when you don't"), and per the boat-rental archetype in `NEW_CLIENT_HANDOFF.md` (which shows separate URLs per money intent: `/fleet/`, `/sunset-cruise/`, `/sandbar/`, `/[destination]/`), Disco Boat should fragment.

**Each use case gets its own slug**, because the slug is the single most important on-page relevance signal (per the same doc, §11) and because Disco Boat has zero topical authority to spend — fragmentation > consolidation at this stage.

The frozen Boatr template chrome (nav, SEO banner, sticky bar, AI widget, footer) is copied to **every** page. Same factory, same product, every page.

### Proposed sitemap

```
/                                            Homepage (use-case grid, social proof, hero)
/the-boat/                                   The boat itself: specs, capacity, photos, onboard
/book/                                       Booking landing (pre-launch = waiting list; post = real flow)
/pricing/                                    Charter rates, captain vs self-drive, deposit, cancellation

# Use-case pages (money-keyword landings)
/bachelorette-party-boat-san-diego/
/birthday-party-boat-san-diego/
/themed-charters/
/pride-boat-charter-san-diego/
/sunset-cruise-san-diego/

# Service-shape pages (decision modifiers)
/self-drive-boat-rental-san-diego/
/captained-charter-san-diego/

# Area pages
/san-diego-bay-boat-rental/                  Companion to existing /boat-rental-mission-bay/

# Trust / utility
/about/
/captain/
/contact/
/faq/
/photo-gallery/

# Existing / protected
/articles/
/disco-party-planning-guide/                 (protected URL)
/boat-rental-mission-bay/                    (protected URL)
/disco-party-decor-rentals/                  (NEW — closes the existing broken link gap)

# Infrastructure
/sitemap.xml
/robots.txt
/404.html
```

That's 21 pages total. Comparable in scope to the alligator-reef build, just shaped around use cases instead of fleet variety.

### Where the Boatr chrome lives on every page

- Top nav (with mobile hamburger) — copied verbatim per template freeze rules
- SEO banner (top of page, collapsible two-column) — present on every preview page during pre-launch; stripped on Phase 2 promotion
- Sticky claim bar (`Like this? Let's make it discoboatrentals.com.`) — present during preview; stripped on promotion
- AI editor widget — present everywhere; endpoint `/edit` during preview, `/edit-persistent` post-payment
- Footer — three-column + bottom row "Site rebuilt by Boatr" (will be stripped — but since Nate owns Disco Boat AND Boatr, this is a marketing call rather than a customer-attribution requirement; flag for decision)

### Architecture trade-off Nate should consider

Three options, in order of recommendation:

1. **Multi-page (recommended).** As mapped above. Best for query fan-out + AI Overview citations + slug-first relevance. Cost: ~21 pages to draft instead of ~1.
2. **Single-page long-scroll, matching Alligator Reef structure.** Faster to build. Worse for SEO on a low-authority new domain. Acceptable if Nate wants to ship fast and iterate.
3. **Hybrid: rich single-page homepage + 3-5 use-case pages.** Compromise. Less SEO upside than full multi-page, more than long-scroll only. Probably the right ship-first move if budget for copy is tight.

Default below assumes option 1. Flag if you want 2 or 3.

---

## 5. Page-by-page briefs

Following `NEW_CLIENT_HANDOFF.md`'s page-brief template. Every brief includes `Needs verification` items where I don't have owner facts. Once Nate fills these in, we write copy.

### 5.1 `/` — Homepage

```md
Page: Homepage
URL: /
Action: Keep + improve (same URL)
Primary search intent: Brand search "disco boat rentals san diego" + category search "party boat rental san diego"
Primary keyword: Disco boat rentals San Diego
Secondary topics: Party boat rental, bachelorette boat charter, birthday party boat
Location modifiers: San Diego, Point Loma, Shelter Island
Business goal: Waiting list signups (pre-launch) → Bookings (post-launch)
Primary CTA: "Join the Waiting List" (current phase) — swap to "Check Availability" on launch
Required facts: Owner first name(s) for SEO banner greeting; "what makes this different" sentence; 1-2 testimonials/quotes if available (else, social proof from the 4 Google reviews); any awards/press
Proof needed: Real photos of the boat exterior, interior, rooftop, fold-down windows in action
Internal links in: All other pages link home from nav + logo
Internal links out: → /the-boat/, → /bachelorette-party-boat-san-diego/, → /birthday-party-boat-san-diego/, → /pricing/, → /book/, → /faq/, → /about/
Schema type: LocalBusiness + TouristAttraction (combined, per Alligator Reef pattern)
Client verification needed: Real owner name, USCG/captain credentials for trust strip, hourly rate range for pricing teaser
```

### 5.2 `/the-boat/` — The Boat Itself

```md
Page: The Boat
URL: /the-boat/
Action: Create (new money page — the single most important new URL)
Primary search intent: "Disco boat san diego," "32 foot suntracker party boat san diego," informational pre-booking
Primary keyword: The Disco Boat / 32' party boat San Diego
Secondary topics: Capacity, what's onboard, rooftop deck, dance pole, bar, windows
Location modifiers: San Diego Bay
Business goal: Conversion from interest → booking inquiry
Primary CTA: "Check Availability" → /book/
Required facts: Exact USCG passenger rating (the marketing says "up to 12" — confirm what the certificate of inspection actually says), boat build year, engine make/model, max speed, restroom availability, climate control / fans, food/drink policy
Proof needed: 8-12 high-quality photos of every space onboard
Internal links in: ← /, ← /bachelorette..., ← /pricing/, nav
Internal links out: → /book/, → /pricing/, → /faq/, → /captain/
Schema type: Product (with Offer if pricing is real and visible) + nested LocalBusiness reference
Client verification needed: USCG capacity, boat year, engine specs, exact list of onboard amenities
```

### 5.3 `/book/` — Booking Landing

```md
Page: Book
URL: /book/
Action: Create
Primary search intent: Transactional. "Rent disco boat san diego," "book party boat san diego"
Primary keyword: Book the Disco Boat
Secondary topics: Availability, deposit, cancellation policy
Location modifiers: San Diego
Business goal: Form submission (waiting list now; real booking once available)
Primary CTA: GHL form embed (link.boatrmarketing.com/widget/form/UKKEdzivMdsNJ2b5tZHI) OR direct booking widget once available
Required facts: Decision on booking platform once live (stay on GHL? Move to FareHarbor? Direct Stripe?); deposit %, cancellation window
Proof needed: 3-4 photos showing happy guests onboard (once Nate has them)
Internal links in: Every page links here. Nav CTA. Sticky-bar CTA.
Internal links out: → /pricing/, → /faq/ (cancellation + weather questions)
Schema type: ReserveAction (once live) — for now, leave to template defaults
Client verification needed: Booking platform decision (waiting-list-only vs real booking); deposit / cancellation terms
```

### 5.4 `/pricing/` — Pricing

```md
Page: Pricing
URL: /pricing/
Action: Create
Primary search intent: "Disco boat rental cost," "san diego party boat price," "how much to rent a party boat san diego"
Primary keyword: Disco boat pricing
Secondary topics: Hourly rate, captain fee, deposit, what's included, add-ons
Location modifiers: San Diego
Business goal: Pre-qualify (filter out tire-kickers, attract serious buyers)
Primary CTA: "Check Availability" → /book/
Required facts: ALL OF IT. Hourly rate, minimum charter length, captain vs. self-drive delta, deposit %, cancellation policy, add-on prices (playlist, lighting, photography setup, decor), tax/fee structure
Proof needed: None specific to this page
Internal links in: ← /, ← /the-boat/, ← /book/, nav
Internal links out: → /book/, → /faq/
Schema type: PriceSpecification (within the LocalBusiness markup)
Client verification needed: EVERYTHING. This page cannot be written without owner pricing.
```

### 5.5 `/faq/` — FAQ

```md
Page: FAQ
URL: /faq/
Action: Create
Primary search intent: Long-tail informational + objection handling
Primary keyword: Disco boat FAQ (but really fragmented across 35+ questions)
Secondary topics: Booking, pricing, what to bring, alcohol, food, weather, safety, captain, self-drive, restroom, music, decor
Location modifiers: San Diego, Point Loma, Shelter Island
Business goal: AI Overview citations + remove every objection between visitor and booking
Primary CTA: "Check Availability" → /book/ (sticky throughout)
Required facts: 35+ real questions with real answers (see Q-bank draft in §10 below — Nate fills in answers)
Proof needed: None
Internal links in: Footer link, every page CTA strip, nav
Internal links out: Each FAQ answer links to the relevant deep page (alcohol Q → /faq/ or /book/; captain Q → /captain/; etc.)
Schema type: FAQPage (canonical, per AI_OVERVIEW_READINESS pillars)
Client verification needed: ALL answers
```

### 5.6 `/about/` — About

```md
Page: About
URL: /about/
Action: Create
Primary search intent: Brand discovery, E-E-A-T research
Primary keyword: About Disco Boat Rentals
Secondary topics: The story, the build, why disco, who runs it
Location modifiers: San Diego
Business goal: Trust + character. Differentiation.
Primary CTA: "Check Availability" → /book/
Required facts: The actual story (when did Nate build the boat? Why disco? What's the build history?)
Proof needed: Build photos if they exist, photo of Nate / the team
Internal links in: Footer, nav
Internal links out: → /captain/, → /the-boat/, → /book/
Schema type: AboutPage + Person (founder) + Organization
Client verification needed: The story; ownership/LLC name for schema
```

### 5.7 `/captain/` — Captain Bio

```md
Page: Captain
URL: /captain/
Action: Create
Primary search intent: Trust research, especially for higher-stakes bookings (corporate, bachelorette)
Primary keyword: Disco boat captain San Diego
Secondary topics: USCG license, years on water, safety record
Location modifiers: San Diego Bay
Business goal: Trust
Primary CTA: "Check Availability" → /book/
Required facts: Captain name(s), USCG license #, years on water, prior charter experience, photo
Proof needed: Captain photo, license credential (visible badge or signed certificate)
Internal links in: ← /about/, ← /the-boat/, ← /faq/, nav
Internal links out: → /book/
Schema type: Person nested inside LocalBusiness
Client verification needed: Captain identity + credentials
```

### 5.8 `/contact/` — Contact

```md
Page: Contact
URL: /contact/
Action: Create
Primary search intent: NAP lookup, parking, dock directions
Primary keyword: Disco Boat Rentals contact
Secondary topics: Address, phone, email, parking, dock slip, meet-up
Location modifiers: 2700 Shelter Island Dr, Point Loma, San Diego 92106
Business goal: Reduce day-of confusion. Make showing up easy.
Primary CTA: Phone link (tel:+18557823988) + GHL form
Required facts: Dock slip number / meet-up landmark, parking instructions, what to bring on day-of
Proof needed: Map embed + parking diagram if possible
Internal links in: Footer, nav
Internal links out: → /book/, → /faq/
Schema type: ContactPage + LocalBusiness (canonical NAP)
Client verification needed: Dock slip / meet-up details, parking
```

### 5.9 Use-case pages: `/bachelorette-party-boat-san-diego/`, `/birthday-party-boat-san-diego/`, `/themed-charters/`, `/pride-boat-charter-san-diego/`, `/sunset-cruise-san-diego/`

```md
Pattern (apply to each):
Page: [Use case] party boat
URL: /[use-case]-boat-san-diego/
Action: Create
Primary search intent: High-intent local + use-case
Primary keyword: [Use case] party boat San Diego
Secondary topics: What's included, group size, photos of [use case], price range, add-ons
Business goal: Capture the long-tail "bachelorette party san diego boat" / "birthday boat san diego" intent that the homepage cannot rank for
Primary CTA: "Check Availability for Your [Use Case]" → /book/?utm_source=[use-case]
Required facts: Real photos from past charters of this type; specific testimonial from a guest of this type; any common requests / decor for this type
Proof needed: 4-6 use-case photos (or general boat photos if use-case-specific don't exist yet)
Internal links in: ← / hero strip, ← /the-boat/, ← other use cases as "also consider"
Internal links out: → /book/, → /pricing/, → /faq/
Schema type: Service (with serviceType matching the use case) + nested LocalBusiness
Client verification needed: Use-case photos, real customer story per page if available
```

### 5.10 Service-shape pages: `/self-drive-boat-rental-san-diego/`, `/captained-charter-san-diego/`

```md
Pattern:
Page: [Service shape] San Diego
URL: /[shape]-boat-rental-san-diego/
Action: Create
Primary search intent: Decision-stage modifier ("self drive" or "captained" filter)
Primary keyword: [Shape] boat rental San Diego
Secondary topics: License requirements (self-drive: California Boater Card?), captain bio (captained), price delta
Business goal: Decision-modifier ranking + reduce inbound "do you have a captain?" inquiries
Primary CTA: "Check Availability" → /book/?utm_source=[shape]
Required facts: Self-drive: California Boater Card requirement, orientation length, eligible age/experience, additional insurance. Captained: captain name + photo + credentials, what's included with captain fee.
Proof needed: Photo of self-drive customer at the helm; photo of captain at the helm
Internal links in: ← /, ← /the-boat/, ← /pricing/, ← /captain/ (from /captained-.../)
Internal links out: → /book/, → /pricing/
Schema type: Service
Client verification needed: License/orientation policy (self-drive); captain credential details (captained)
```

### 5.11 Area pages: `/san-diego-bay-boat-rental/` (the existing `/boat-rental-mission-bay/` is the companion piece)

```md
Page: San Diego Bay boat rental
URL: /san-diego-bay-boat-rental/
Action: Create
Primary search intent: Area-specific informational
Primary keyword: San Diego Bay boat rental
Secondary topics: USS Midway, Coronado Bridge, downtown skyline, what to see, where Disco Boat cruises
Location modifiers: San Diego Bay, Coronado, downtown SD
Business goal: Topical authority pair with /boat-rental-mission-bay/ — together they form the "San Diego boat rental geographic" cluster
Primary CTA: "Cruise San Diego Bay" → /book/
Required facts: Which area Disco Boat actually launches into (San Diego Bay from Shelter Island, or does it ever cross to Mission Bay?); approved cruising zones
Proof needed: Photos of the boat actually on San Diego Bay with landmarks visible
Internal links in: ← /, → /boat-rental-mission-bay/ (sister piece)
Internal links out: → /boat-rental-mission-bay/, → /book/, → /the-boat/
Schema type: TouristAttraction + Article
Client verification needed: Cruising zones, landmarks Nate wants featured
```

### 5.12 `/articles/` — Blog Index

```md
Page: Articles
URL: /articles/
Action: Keep + improve
Primary search intent: Site exploration
Primary keyword: Disco boat articles / disco party guide
Business goal: Topical authority hub. Internal link distribution.
Required facts: Plan for ongoing publishing cadence — $299 Boatr tier includes 1/mo, but Nate owns this and can publish however he wants
Proof needed: Article thumbnails
Schema type: CollectionPage
Client verification needed: Future article plan
```

### 5.13 `/disco-party-planning-guide/` — Protected blog post

```md
Page: Disco Party Planning Guide
URL: /disco-party-planning-guide/
Action: Protect (preserve URL + structure) + fix
Fixes needed:
  - Remove the broken internal link to /disco-party-decor-rentals/ OR create that page (recommended: create it, since the post drives intent to that URL)
  - Audit all ~70 Amazon affiliate links — the ASINs (B07XYZ1234, B08ABC3456, etc.) look like placeholders, not real products. If real, leave them. If placeholder, replace with real ASINs or strip.
  - Strip the [Amazon dp/...] formatting where ASINs are clearly fake to avoid "deceptive content" signals
Keep: All copy, the table of contents, the H2 structure, the existing meta
Schema type: Article + (optionally) HowTo if we want to rebuild as a how-to guide
Client verification needed: Are the Amazon ASINs real or were they AI-generated placeholders?
```

### 5.14 `/boat-rental-mission-bay/` — Protected blog post

```md
Page: Boat Rental Mission Bay (vs San Diego Bay)
URL: /boat-rental-mission-bay/
Action: Protect (preserve URL) + fix
Fixes needed:
  - Fix the malformed closing link: `https://discoboatrentals.com/boat-rental-mission-bay/www.discoboatrentals.com` → just `https://discoboatrentals.com/` or → `/the-boat/`
  - Rewrite the closing CTA (currently weak): from "For a boat rental in Mission Bay, consider disco boat!" to a real CTA strip pointing at /the-boat/ + /book/
  - Add an obvious internal link to the new /san-diego-bay-boat-rental/ companion page once it exists
Keep: All comparison content, the table, the outbound link to coronadovisitorcenter.com
Schema type: Article
Client verification needed: None (these are mechanical fixes)
```

### 5.15 `/photo-gallery/` — Gallery

```md
Page: Photo Gallery
URL: /photo-gallery/
Action: Create
Primary search intent: Visual research before booking
Primary keyword: Disco boat photos / disco boat san diego pictures
Business goal: Trust + visual proof
Primary CTA: "Check Availability" → /book/
Required facts: Source photos from Instagram (@discoboats), any unposted shoot library, customer-submitted (with permission)
Proof needed: 25+ high-quality photos covering: exterior, rooftop, interior, fold-down windows, dance pole, bar, sunset, guests, captain
Schema type: ImageGallery
Client verification needed: Photo library access; permission for any guest-featuring shots
```

### 5.16 `/disco-party-decor-rentals/` — Closes the broken-link gap

```md
Page: Disco Party Decor Rentals
URL: /disco-party-decor-rentals/
Action: Create (closes the existing broken internal link from the disco-party-planning-guide post)
Primary search intent: Decor rental adjacent to the boat — could be a real ancillary revenue line
Primary keyword: Disco party decor rentals San Diego
Business goal: Decision: is this a real service? If yes, page captures the long-tail. If no, page redirects /disco-party-decor-rentals/ → /themed-charters/.
Required facts: Does Disco Boat actually rent decor separately from the boat? If yes, inventory + price list. If no, this page becomes a "we don't rent decor separately, but every charter includes [X]" + redirect existing internal link target.
Schema type: Service (if real) OR a 301 (if not)
Client verification needed: Is this a real offering?
```

---

## 6. Metadata plan

For every page, follow this pattern:

- **Title:** `[Primary keyword] | Disco Boat Rentals` (≤ 60 chars where possible)
- **Meta description:** Plain-English summary, includes location, ends with a soft CTA. ≤ 155 chars.
- **Canonical:** Self-referencing `<link rel="canonical">` on every page
- **OG title / description / image:** Match the title/meta, og:image = page-relevant photo
- **Twitter card:** `summary_large_image`
- **Viewport:** `width=device-width, initial-scale=1` (drop the `maximum-scale=1, user-scalable=0` from the current site — it blocks pinch-zoom and is an accessibility yellow flag)
- **Robots:** `index, follow` on all production pages. Preview-phase pages get `noindex, nofollow` (per `_TEMPLATE_README.md §4 checklist`).

**Specific title drafts:**

| Page | Title | Char count |
|---|---|---|
| `/` | Disco Boat Rentals \| San Diego's Party Boat | 47 |
| `/the-boat/` | The Disco Boat — 32' Party Cruiser \| San Diego | 49 |
| `/book/` | Book the Disco Boat \| San Diego Party Charter | 49 |
| `/pricing/` | Disco Boat Pricing \| San Diego Party Boat Rental | 50 |
| `/bachelorette-party-boat-san-diego/` | Bachelorette Party Boat San Diego \| Disco Boat | 49 |
| `/birthday-party-boat-san-diego/` | Birthday Party Boat San Diego \| Disco Boat | 47 |
| `/themed-charters/` | Themed Party Boat Charters \| Disco Boat San Diego | 51 |
| `/pride-boat-charter-san-diego/` | Pride Party Boat San Diego \| Disco Boat Charter | 49 |
| `/sunset-cruise-san-diego/` | Sunset Cruise San Diego \| Disco Boat | 38 |
| `/self-drive-boat-rental-san-diego/` | Self-Drive Boat Rental San Diego \| Disco Boat | 47 |
| `/captained-charter-san-diego/` | Captained Charter San Diego \| Disco Boat | 42 |
| `/san-diego-bay-boat-rental/` | San Diego Bay Boat Rental \| Disco Boat Charter | 48 |
| `/faq/` | Disco Boat FAQ \| San Diego Party Boat Questions | 49 |
| `/about/` | About Disco Boat Rentals \| San Diego | 38 |
| `/captain/` | Meet the Captain \| Disco Boat Rentals San Diego | 49 |
| `/contact/` | Contact Disco Boat Rentals \| Point Loma San Diego | 51 |
| `/photo-gallery/` | Disco Boat Photo Gallery \| San Diego Party Boat | 49 |
| `/articles/` | The Grooviest Articles \| Disco Boat Rentals | 45 (keep current) |
| `/disco-party-planning-guide/` | Disco Party Planning Guide: How to Throw the Best Disco Bash | 60 (keep current — ranks already) |
| `/boat-rental-mission-bay/` | Boat Rental Mission Bay \| Disco Boat | 38 (keep current — ranks already) |
| `/disco-party-decor-rentals/` | Disco Party Decor Rentals San Diego \| Disco Boat | 50 |

---

## 7. Schema plan

Site-wide pattern (per `SEO_PLAYBOOK.md §7` + `BOATR_OPERATIONS.md §6` "marine-specific schema"):

- **Sitewide (homepage canonical):** `LocalBusiness` + `TouristAttraction` combined block (same pattern as Alligator Reef preview). `geo` with real lat/long for 2700 Shelter Island Dr. `openingHoursSpecification` Mon–Sun 08:00–22:00. `sameAs` for Instagram + Facebook. `image` array with 4-6 photos. `priceRange` ("$$$" placeholder until pricing is confirmed).
- **`/the-boat/`:** `Product` with `name: "The Disco Boat — 32' Suntracker Party Cruiser"`, nested `brand`, `aggregateRating` (only if real reviews are present — currently 4 Google reviews, can include `AggregateRating` with `reviewCount: 4, ratingValue: 5.0`), `offers: AggregateOffer` (once pricing exists).
- **`/book/`:** `ReserveAction` (once real booking exists) + nested `LocalBusiness` reference.
- **Use-case pages (`/bachelorette/`, `/birthday/`, etc.):** `Service` with `serviceType` matching the use case, `provider: { @id: "[homepage]#localbusiness" }`, `areaServed: "San Diego, CA"`.
- **`/sunset-cruise-san-diego/`:** `TouristTrip` (per `SEO_PLAYBOOK.md §7`) + `Service`.
- **`/faq/`:** `FAQPage` with `mainEntity: [Question + Answer]` for every Q in the bank (§10 below).
- **`/about/`:** `AboutPage` + `Organization` + `Person` (founder).
- **`/captain/`:** `Person` (nested in `LocalBusiness#employee`).
- **`/contact/`:** `ContactPage` + canonical `LocalBusiness` NAP.
- **Blog posts (`/disco-party-planning-guide/`, `/boat-rental-mission-bay/`):** `Article` with `author`, `datePublished`, `dateModified`, `mainEntityOfPage`.
- **`/photo-gallery/`:** `ImageGallery`.

Validate every block in the Schema.org validator before launch.

---

## 8. Internal linking plan

Following `SEO_PLAYBOOK.md §9` rules: preserve high-value link patterns, use natural anchor text, avoid keyword stuffing.

- **Nav:** Home, The Boat, Pricing, Book, FAQ, About, Articles. (Use-case pages reachable via homepage grid, not crammed in nav.)
- **Homepage:** hero CTA → /book/; secondary grid → all 5 use-case pages; trust strip → /captain/; "what's onboard" → /the-boat/
- **`/the-boat/`:** outbound to /book/, /pricing/, /captain/, /faq/; inbound from every use-case page + homepage
- **Use-case pages:** outbound to /book/, /pricing/, /the-boat/; cross-link to 2 sibling use cases ("also consider:")
- **`/articles/`:** outbound to both protected blog posts; inbound from every page's footer
- **`/disco-party-planning-guide/`:** keep all internal links; the existing reference to `/disco-party-decor-rentals/` becomes a real link once that page exists
- **`/boat-rental-mission-bay/`:** add a real CTA-strip outbound to /the-boat/ + /book/; add a sister-piece link to /san-diego-bay-boat-rental/
- **Footer:** Visit / Connect / Articles columns. Avoid the "every page in the footer" anti-pattern.

---

## 9. Image / photo needs

Per `BRAIN.md §12` image-scrape ladder:

1. ~6 photos already on the WordPress site at `wp-content/uploads/2025/08/` (exterior, fold-down windows, interior). Pull these via `wget`.
2. Pull Instagram @discoboats photos for the gallery. (Some are video reels — extract frames where useful.)
3. Pull any GBP photos.
4. **Marine vertical fallback library** (per `BOATR_OPERATIONS.md §6`): sunset on San Diego Bay, Point Loma skyline, marine layer — use sparingly, only where Disco Boat's own photos don't cover.
5. **No AI-generated people, no AI-generated boats.** (Per `BOATR_OPERATIONS.md §6` warning.)

**Photo slots that need real content (flag to Nate by name):**

- `/the-boat/` hero — boat exterior at the dock
- `/the-boat/` rooftop deck with disco ball lit at sunset
- `/the-boat/` interior with leopard walls + dance pole
- `/bachelorette/` — real bachelorette group on the boat (or generic boat-party scene if not available)
- `/birthday/` — birthday on the boat
- `/pride/` — pride-themed charter (or stock pride imagery on the boat)
- `/sunset-cruise/` — golden hour rooftop with the boat on the bay
- `/captain/` — captain at the helm
- `/about/` — Nate (or whoever the public face is) on the boat
- `/contact/` — Shelter Island dock with the boat in slip
- `/photo-gallery/` — 25+ across all of the above

---

## 10. FAQ Q-bank draft (for `/faq/`)

Draft 35 questions to satisfy the BRAIN.md §3 step 5 requirement and to feed FAQPage schema. Answers TBD by Nate.

**Booking & pricing**

1. How do I book the Disco Boat?
2. How much does it cost to charter the Disco Boat?
3. What's the minimum charter length?
4. What's the deposit and when's the balance due?
5. What's your cancellation policy?
6. Can I rent for a few hours or only a full day?
7. Do you offer discounts for off-peak or weekday charters?
8. What payment methods do you accept?

**The boat**

9. How many people fit on the Disco Boat?
10. Is there a bathroom on board?
11. Is there shade from the sun?
12. Is the boat ADA accessible?
13. What's the rooftop deck capacity?
14. Can we use the dance pole?
15. Do the fold-down windows actually open?
16. Is there air conditioning or fans?

**Self-drive vs. captained**

17. Can I drive the boat myself, or do I need a captain?
18. Do I need a California Boater Card to self-drive?
19. What's the captain fee and what's included?
20. How long is the orientation if I self-drive?

**On the day**

21. Where do we meet the boat?
22. Where do we park?
23. What time should we arrive before our charter?
24. What should we bring?
25. Can we bring our own food and drinks?
26. Can we bring our own playlist?
27. Can we bring our own decor?

**Safety, weather, and policy**

28. What if the weather is bad — do we still go?
29. Is alcohol allowed onboard?
30. Are kids allowed?
31. Are pets allowed?
32. What's your USCG capacity and inspection status?
33. What safety equipment is on board?

**Themed and use-case**

34. Do you do bachelorette parties?
35. Do you do birthday parties?
36. Do you host Pride events or themed nights?
37. Can we set up specific décor for our theme?
38. Do you offer photography?

(That's 38. Trim to your favorite 35 once Nate answers them.)

---

## 11. Launch risk checklist

Pre-launch (run after the rebuild HTML is written, before DNS cutover):

**SEO preservation**

- [ ] All 4 existing URLs (/, /articles/, /disco-party-planning-guide/, /boat-rental-mission-bay/) return 200 on the new build
- [ ] No accidental URL changes on any of the 4
- [ ] Existing GBP website link still works (post-launch verify)
- [ ] `<meta name="robots">` set to `noindex, nofollow` on staging Netlify URL; flipped to `index, follow` once on the live custom domain
- [ ] AI bots allowed in robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, anthropic-ai)
- [ ] `sitemap.xml` includes all 21 production URLs
- [ ] `canonical` on every page is the production URL (not the staging Netlify URL)

**Content & defects fixed**

- [ ] Footer address corrected (2700 Shelter Island Dr, Point Loma 92106 — NOT Bahia Resort / 92109)
- [ ] Broken internal link `/disco-party-decor-rentals/` resolves (either the new page exists, or it's removed from the disco-party-planning-guide post)
- [ ] Malformed link in `/boat-rental-mission-bay/` is fixed
- [ ] WordPress generator meta tag removed
- [ ] No placeholder / lorem-ipsum / `B07XYZ1234`-style fake Amazon ASINs anywhere
- [ ] No "Coming soon..." placeholder on /articles/

**Schema**

- [ ] LocalBusiness + TouristAttraction validates on schema.org validator
- [ ] FAQPage validates
- [ ] Every page has a self-referencing canonical
- [ ] No conflicting `noindex` headers

**Mobile + AI-Overview pillars (per `AI_OVERVIEW_READINESS.md`)**

- [ ] **Mobile hamburger works** — explicit test on real phone per `_TEMPLATE_README.md §4` KNOWN FAILURE MODE
- [ ] Lighthouse mobile Performance ≥ 90, SEO ≥ 90 on /, /the-boat/, /book/
- [ ] First 50 words of body copy on every page directly answer the page's title question
- [ ] Every H2 leads with its answer in the first 1-2 sentences
- [ ] Outbound citations on /boat-rental-mission-bay/ (already has coronadovisitorcenter.com — preserve)
- [ ] Outbound citations added on /disco-party-planning-guide/ if Wikipedia disco link is preserved
- [ ] `<title>` + meta description unique per page
- [ ] One H1 per page; logical H2/H3 structure
- [ ] No JS-only content (everything readable with JS disabled)
- [ ] Page weight < 2 MB per `GOOGLE_2026_SEO_FINDINGS.md §4`

**Booking & conversion**

- [ ] GHL form on /book/ loads and submits to the right pipeline
- [ ] Phone link (tel:+18557823988) works on mobile
- [ ] Every page has a clear CTA above the fold

**Boatr template freeze rules** (per `_TEMPLATE_README.md`)

- [ ] Top nav copied verbatim from template (mobile hamburger functional)
- [ ] SEO banner present + collapsible + populated with real prospect-name greeting
- [ ] Sticky bar present, references `discoboatrentals.com` correctly
- [ ] AI editor widget present, endpoint `/edit` (preview phase)
- [ ] Footer "Site rebuilt by Boatr" line present (TBD whether to strip immediately since Nate owns both — see open item)
- [ ] Banner CTA links to `/onboard/?prospect=disco-boat-rental&business=Disco+Boat+Rentals&url=discoboatrentals.com&phone=+18557823988`

Post-launch (first 48h → 2 weeks → 30 days, per `SEO_PLAYBOOK.md §15`):

- [ ] All 4 protected URLs still indexed
- [ ] Search Console annotation added for launch date
- [ ] GBP website link updated (if it points anywhere different)
- [ ] No 404s in Search Console
- [ ] All 21 production URLs crawled within 2 weeks

---

## 12. Facts that still need Nate's verification

Carrying over from `_INTAKE.md` items 4-17 + new items surfaced during the audit:

**Operational**

1. **Pricing** — hourly rate, minimum charter length, captain vs. self-drive delta, deposit %, cancellation policy, add-on pricing
2. **USCG status** — passenger rating on the certificate of inspection, inspection date, insurance carrier
3. **Captain identity** — name, license #, bio, photo
4. **Self-drive policy** — California Boater Card requirement, orientation length, eligible age/experience, additional insurance
5. **Booking platform decision** — stay on GHL waiting list, or move to a real booking flow (FareHarbor? Direct Stripe? GHL booking calendar?)
6. **Day-of logistics** — dock slip / meet-up landmark, parking instructions, arrival window, what to bring
7. **Alcohol / food policy** — BYOB allowed? Outside food? Any restrictions?
8. **Weather / cancellation policy** — when do you cancel, what's refunded vs. rebooked

**Content sourcing**

9. **Real testimonials** — pull the 4 Google reviews? Any soft-launch guests with quotes?
10. **Photo library** — beyond the ~6 photos on the WP site + Instagram, is there a shoot library?
11. **Captain bio detail** — full credentials, years on the water, prior charter experience
12. **The story for `/about/`** — when did Nate build the boat? Why disco? What's the build history?

**Existing-content questions**

13. **Amazon affiliate links in `/disco-party-planning-guide/`** — are the ~70 ASINs real Amazon products, or placeholder/AI-generated? If placeholder, replace or strip.
14. **`/disco-party-decor-rentals/`** — is decor rental a real ancillary offering, or does the page just exist to close the broken internal link? Decision changes whether it's a real page or a redirect.

**Access**

15. **Google Search Console** — set up + grant access
16. **Google Business Profile** — grant access; confirm direct URL
17. **Domain registrar / DNS** — confirm access for the DNS cutover
18. **WordPress hosting** — access for the cancellation snapshot (per `BRAIN.md §9`) — even though it's Nate's own site, the snapshot habit should still apply

**Architectural decisions**

19. **Architecture** — confirm option 1 (full multi-page, 21 URLs), option 2 (long-scroll matching Alligator Reef), or option 3 (hybrid: rich homepage + 3-5 use-case pages)
20. **Footer attribution** — keep "Site rebuilt by Boatr" footer line as marketing for Boatr (you own both brands), or strip since this is your own business?
21. **Tier framing** — even though there's no customer to charge, do we still operationally treat this as a $499-tier build (blog cadence, SMS/email blasts, GHL fully wired)? Affects what we plan post-launch.
22. **Goals + success metric** — what does success look like in 90 days? Waiting-list size? First N bookings? GBP review count? Specific keyword positions?

---

## Revision 1 — Architecture trimmed (2026-05-23, post-Nate review)

Nate's feedback: "do not be repetitive about the boat rental in this build." Original 21-page plan had too many use-case pages that would have shared ~80% of the body copy (bachelorette/birthday/corporate are the same product to the same audience). Revising to 12 production pages where each one has a genuinely distinct reason to exist.

### Pages CUT from original plan

| Cut URL | Reason | Where the intent now lives |
|---|---|---|
| `/birthday-party-boat-san-diego/` | Bachelorette and birthday are the same product. Body copy would be nearly identical. | Birthday is named on homepage hero strip + covered in `/bachelorette-party-boat-san-diego/` social proof. |
| `/pride-boat-charter-san-diego/` | Pride is a theme, not a separate product offering. | Folded into `/themed-charters/` with prominent Pride section. |
| `/self-drive-boat-rental-san-diego/` | Self-drive vs captained is a decision modifier on the same boat, not a separate experience. | Becomes a "captain or self-drive?" decision block on `/the-boat/`. |
| `/captained-charter-san-diego/` | Same reason. | Decision block on `/the-boat/` plus `/captain/` for the bio. |
| `/san-diego-bay-boat-rental/` | Thin area page with no distinct content. | Folded into homepage location section + adds an internal link from `/boat-rental-mission-bay/`. |
| `/photo-gallery/` | A gallery is a section, not a page. | Becomes a section on `/the-boat/`. |
| `/disco-party-decor-rentals/` | Only create if it's a real service offering. | Held pending Nate's answer to verification item #14. Default: leave as a 301 to `/themed-charters/`. |

### Revised production sitemap (12 pages)

```
/                                           Homepage
/the-boat/                                  Boat + onboard + captain-or-self-drive decision + gallery
/pricing/                                   Charter rates + what's included + cancellation
/book/                                      Booking landing (GHL waitlist → real flow)

# Use-case money pages (each genuinely distinct)
/bachelorette-party-boat-san-diego/         Bachelorette market — distinct audience, photos, add-ons
/themed-charters/                           Disco night, Pride, custom theme — distinct decor world
/sunset-cruise-san-diego/                   Golden-hour rooftop disco-ball experience — distinct visual + time

# Trust / utility
/about/                                     Story of the build
/captain/                                   Captain bio + credentials
/faq/                                       35+ Q + FAQPage schema
/contact/                                   NAP + parking + dock directions
/articles/                                  Blog index

# Protected existing content (URLs unchanged)
/disco-party-planning-guide/                Top-of-funnel ranking content
/boat-rental-mission-bay/                   Money-keyword comparison piece

# Infrastructure
/sitemap.xml
/robots.txt
/404.html
```

12 production pages + 2 protected blog pieces + 3 infrastructure = 17 URLs total. Down from 21.

### Build approval

✅ Nate approved on 2026-05-23: "go for it."

Starting build immediately. Order of operations:
1. Copy `_template/` → `disco-boat-rental/` (verbatim, preserving FROZEN elements per `_TEMPLATE_README.md §1`)
2. Pull boat photos from current WP site into `disco-boat-rental/images/`
3. Build `/` (homepage) end-to-end as the first page
4. Build out remaining 11 production pages
5. Update internal linking, schema, sitemap.xml, robots.txt
6. Run pre-ship checklist before handing back

Page-level copy still flagged `Needs verification` per §12 will use the best inference from public info now and get refined when Nate fills in the operational gaps (pricing, USCG, captain bio, etc.).
