# Malarky Charters — Project Brief

This file is the source of truth for working on `clients/malarky/`. Read it at the start of every session that touches this folder.

---

## What Malarky is

Malarky Charters is one of five Boatr-owned brands operating private yacht charters on San Diego Bay. It is **not a Relaunch demo prospect** — it is a real operating business that is being moved onto the Relaunch tech stack (static HTML / Netlify / GitHub) from its previous WP Engine WordPress site.

The four sibling brands (Triton, Alana, Athena, Aquata) currently run elsewhere. **Don't bundle them with Malarky on tryrelaunch infrastructure** — there's an SEO-penalty concern if the same operator's brands all share visible hosting fingerprints (Netlify subdomains, IPs, etc.). Each brand should have its own dedicated Netlify project. Malarky was the first to move.

---

## Where it lives

- **Repo path:** `clients/malarky/` inside the `tryrelaunch/relaunch` GitHub repo.
- **Netlify project:** `malarky-charters` (NOT `client-malarky` — we deliberately avoided the `client-*` naming to keep it from looking like a Relaunch productized site).
- **Temporary URL:** `https://malarky-charters.netlify.app/`
- **Production domain (pending DNS flip):** `https://malarkycharters.com/`
- **Domain registrar:** hover.com
- **Currently still pointed at:** WP Engine (the old WordPress site). Will be cut over once we're confident in the new site.
- **Phone:** (844) 724-5787
- **Owner email:** info@malarkycharters.com
- **Dock / departure:** 2700 Shelter Island Dr, San Diego, CA
- **Google Business Profile CID:** `12410663655035935065` (canonical URL: `https://www.google.com/maps?cid=12410663655035935065`) — used in JSON-LD `sameAs`.
- **FareHarbor account (shared with siblings):** `missionbaysportcenter` (verify before launch)

---

## The boat

- **Vessel:** Malarky — a 47-foot Voyage performance sailing catamaran
- **Builder:** Voyage, Cape Town, South Africa
- **Layout:** 4 staterooms · 2 heads · indoor lounge · covered aft deck (seats ~8) · bow trampoline
- **Capacity:** Up to **12 guests** maximum
- **3D walkthrough Matterport ID:** `eqFeXUDe9Dn` (iframe is on the homepage, optimized with `qs=1&play=0` and preconnect)

---

## Operating policy — get these right sitewide, no exceptions

These have been re-swept across all 24 pages. Don't reintroduce the old language anywhere.

1. **Captain is HIRED SEPARATELY at $50/hour.** Never "included." Never "complimentary." Paid directly to the captain on arrival via Apple Pay, Venmo, PayPal, or cash. USCG-licensed. Meta descriptions, hero copy, FAQs, pricing pages, trust strips — all must reflect this.
2. **Open Pacific sailing only on full-day (4+ hour) charters.** Shorter charters stay inside San Diego Bay. Don't say "we don't go on the ocean" anywhere — that was an older policy and is now wrong.
3. **Sailing actually happens.** If wind cooperates the catamaran sails (it's not a motor-only floating platform). Mention this where relevant.
4. **Crew acts as bartender / host.** They serve your BYOB drinks, manage the boat, handle hospitality.
5. **BYOB allowed.** Bring your own food and drinks. Two rules: **no glass containers** (transfer to plastic before boarding) and **no red wine**. Don't claim "San Diego's only BYOB" anywhere — that's not defensible. Just say BYOB is allowed.
6. **Private charters only.** No shared cruises, no other guests aboard, no tour-group format.
7. **No license / no experience required.** The captain handles everything.
8. **Reviews are real.** AggregateRating + 3 Review objects in JSON-LD are kept. Don't strip them. Nothing on the site is fake.

---

## Page inventory (24 pages, all under `clients/malarky/`)

Each page is its own folder with an `index.html`. Standard static-site convention. All internal links are absolute (`/menu/`, `/styles.css`, etc.) so the Netlify base-directory setup serves them correctly at the root of `malarkycharters.com`.

Core / hub:
- `/` — homepage
- `/info/` — FAQ hub
- `/booking-info/`
- `/contact-us/`
- `/articles/` — resources hub
- `/privacy-policy/`
- `/yacht-charter-pricing-san-diego/`
- `/yacht-charter-deals-san-diego/`

Service landing pages (one per high-intent search term):
- `/private-yacht-charter-san-diego/`
- `/luxury-yacht-rental-san-diego/`
- `/yacht-rental-san-diego/` *(flagged as thinner by SEO audit — strengthen post-launch)*
- `/byob-yacht-charter-san-diego/`
- `/private-catamaran-charter-san-diego/`
- `/sailboat-charters-san-diego/`
- `/private-sunset-yacht-charter-san-diego/`
- `/party-yacht-rental-san-diego/`
- `/boat-rental-with-water-toys-san-diego/`

Occasion pages:
- `/wedding-yacht-charter-san-diego/`
- `/bachelorette-yacht-charters-san-diego/`
- `/birthday-yacht-charter-san-diego/`
- `/anniversary-yacht-charter-san-diego/`
- `/proposal-yacht-charter-san-diego/`
- `/corporate-yacht-charter-san-diego/`
- `/executive-yacht-charter-san-diego/`

Internal-only (not exposed publicly):
- `/edit/` — staff edit interface placeholder (paying clients don't get the public widget)

---

## Architecture quirks (don't fight these)

### Nav and footer are GLOBAL — edit the partials, not the pages

Site-wide nav/footer changes go through:
- `clients/malarky/_partials/nav.html` — single source for the nav. Contains placeholders `__BASE__` (relative path back to root) and `__HOME_HREF__` (root-relative home URL) that get filled in per-page.
- `clients/malarky/_partials/footer.html` — single source for the footer.

A build script `clients/malarky/sync-partials.py` walks every `index.html` under `clients/malarky/`, finds the `<!-- NAV:START --> ... <!-- NAV:END -->` and `<!-- FOOTER:START --> ... <!-- FOOTER:END -->` marker blocks, and replaces the contents from the partials.

**`deploy.bat` runs `sync-partials.py` automatically before committing** (skip with the `/skip-sync` flag if you really need to). Python 3.x is required on PATH — use `py -3` (Python launcher) rather than `python` directly to avoid the Microsoft Store shim. Install via `winget install Python.Python.3.12` if missing.

This was added specifically because earlier sessions kept making nav/footer fixes per-page, leading to inconsistent state across the 24 pages. Don't go back to per-page edits.

### Type scale

All body paragraphs use `clamp(17px, 1.3vw, 18px)` (or a flat 17px on mobile). Don't reintroduce mixed sizes — every hero-lede / sec-lede / paragraph that was at 15px or 16px was hunted down and unified. If you see a body paragraph using anything else, it's a regression.

### Cache busting

CSS is loaded as `css/main.css?v=2026051039`. Bump the version string (date-based) whenever main.css changes substantively, so visitors don't get the stale cached version.

### Image conventions

- `images/boat/` — boat photography (hero, gallery, aerial, interior)
- `images/people/` — people on the boat
- Hero image is `images/boat/boat-hero-skyline-group-27.webp`
- All images use `loading="lazy" decoding="async"` except above-the-fold hero which uses `fetchpriority="high"`

### Gallery slider

The "Meet Malarky" homepage gallery is a native CSS scroll-snap carousel — no JS framework. The slider script is in `js/main.js` and adds button/dot controls. CSS lives in `css/main.css` (`.gallery-slider`, `.gallery-track`, `.gallery-slide`).

### Schema markup

JSON-LD `@graph` on the homepage includes:
- LocalBusiness (with AggregateRating + 3 Review objects — these are real, don't remove)
- Service
- Vehicle (the catamaran)
- ImageObject (the hero photo)
- FAQPage
- BreadcrumbList
- `sameAs` array including Google Maps CID URL, Instagram, Facebook, Yelp, Tripadvisor

### Fonts

Loaded via `<link rel="preconnect">` + `<link rel="stylesheet">` (NOT via `@import` in CSS — that's render-blocking). Cabin + Montserrat from Google Fonts. The preconnect block is present on all 24 pages.

---

## Deploy workflow

From a Command Prompt or PowerShell on Nate's machine:

```
cd C:\Users\Nsini\Code\relaunch\relaunch-website
deploy.bat "your commit message here"
```

`deploy.bat` does, in order:
1. Runs `sync-partials.py` (unless `/skip-sync` is passed)
2. `git add .`
3. `git commit -m "<your message>"` (prompts if you didn't pass one inline)
4. `git push origin main`

Netlify auto-deploys `malarky-charters.netlify.app` in ~60s. Production domain (once flipped) will deploy at the same time.

**Known recurring issue:** if `.git/index.lock` is present from a crashed previous git process, you'll get "Unable to create '.git/index.lock': File exists." Fix:

```
del .git\index.lock
```

Then retry.

---

## Pending — pre-launch

1. **Final QA walk** on `malarky-charters.netlify.app`: every page loads, hamburger works, gallery slider works, 3D tour loads, footer renders.
2. **Strengthen `/yacht-rental-san-diego/`** — SEO audit flagged it as thinner than core pages.
3. **DNS flip** at hover.com — add the domain to Netlify, get the A + CNAME records, update at hover, wait for propagation, confirm SSL provisions. Leave WP Engine running for a couple weeks as safety net before cancelling.

## Pending — post-launch

- Inline-style refactor → utility classes (maintainability)
- Possibly: separate GA4 properties per Boatr brand
- Audit the other 4 Boatr brands for a similar rebuild path

---

## Things that have bitten us — read before making bulk changes

- **Bulk Python regex passes on HTML have repeatedly truncated pages.** Six pages lost body content from a sed-style pass earlier this session. If you need to do bulk edits across all 24 pages, prefer per-page Edit-tool string replacements over regex bulk-bumps, OR check out a known-good commit before running.
- **Per-page nav edits create drift.** Use the partials. Always.
- **The "Captain & Crew Included" trust strip used to be on every page.** It's now "USCG Captain Available ($50/hr)." If you ever see "Captain Included" copy somewhere, it's a regression — kill it.
- **Don't say "San Diego's only BYOB."** Just "BYOB allowed."
- **Don't strip AggregateRating or Review JSON-LD** — those are real reviews from Yelp/Google/Tripadvisor.
- **Don't claim open-ocean for short charters.** 4+ hours only.

---

## SEO / structured-data state at last audit

- Canonical: `https://malarkycharters.com/` (note: malarkycharters.com, no trailing dash anywhere)
- robots.txt + sitemap.xml present in `clients/malarky/`
- `_redirects` file present for old WordPress URL preservation (legacy URLs that have backlinks → new equivalents)
- Facebook + Google site verification meta tags present
- AggregateRating (4.9 / 5, real reviews) preserved
- openingHours: `Mo-Su 08:00-20:00`
- Schema-validated — last check passed all critical items in the audit

That's Malarky.
