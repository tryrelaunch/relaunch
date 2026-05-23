# Malarky Charters — Launch Fix To-Do List

**For:** Claude / Codex executing against `malarky-charters.netlify.app` rebuild before promotion to `malarkycharters.com`
**Source:** Audit comparing live WP site to Netlify rebuild (2026-05-21)
**Rule:** Do NOT write final copy or invent facts. Use the exact strings provided below. Anything marked "[VERIFY WITH NATE]" is a placeholder — do not publish until confirmed.

---

## Phase 1 — Launch blockers (do not promote without these)

### 1. Noindex the staging site until cutover

**File:** every HTML template / layout file on the Netlify build
**Action:** add to `<head>`:

```html
<meta name="robots" content="noindex,nofollow">
```

**Acceptance:** view-source on `malarky-charters.netlify.app` shows the meta tag on every page.
**Remove this tag** as part of the production deploy — not before.

---

### 2. Verify the contact form endpoint

**File:** `/contact-us/` page form action
**Current value:** `https://formspree.io/f/malarky`

**Action:** confirm this Formspree project ID exists and is owned by Boatr/Malarky. If it's a placeholder (very likely — Formspree IDs are normally alphanumeric, not `malarky`), replace with the real endpoint OR swap to a working alternative (Netlify Forms is one option since the site is on Netlify — just add `data-netlify="true"` to the form tag).

**Acceptance:** submit a test inquiry from the contact form, confirm the inquiry lands in the destination inbox.

---

### 3. Replace all Netlify URLs with production domain

**Scope:** site-wide. Search the codebase for `malarky-charters.netlify.app` and replace with `https://malarkycharters.com`.

**Must update:**
- All `<link rel="canonical">` tags
- All `<meta property="og:url">` tags
- All internal `<a href="...">` (use root-relative `/wedding-yacht-charter-san-diego/` rather than absolute where possible)
- JSON-LD schema `url`, `@id`, `image` fields
- `sitemap.xml`
- `robots.txt` (sitemap reference)
- Any hardcoded image src (most should already be relative — verify)

**Acceptance:** grep the build output for `netlify.app` — zero matches.

---

### 4. Verify these claims before publishing

Each appears on the rebuild. None should ship without explicit confirmation from Nate / the client. If unverifiable, soften or remove.

| Claim | Where it appears | Status |
|---|---|---|
| "5.0 stars · 412 Google reviews" | Home + Wedding + Pricing | [VERIFY WITH NATE] |
| "USCG captain available ($50/hr)" | Throughout | [VERIFY WITH NATE] |
| "open Pacific on full-day charters" | Home + Wedding FAQ | [VERIFY WITH NATE] |
| "only sailing catamaran in San Diego's premium charter fleet" | (location TBC — search build) | [VERIFY WITH NATE] |
| "1-hour email quote turnaround" | Pricing | [VERIFY WITH NATE] |
| "Drink packages with full bar inventory are coming soon" | Home FAQ | [VERIFY WITH NATE — is this real?] |
| "Established 2020" footer | Footer all pages | [VERIFY WITH NATE] |

**Acceptance:** every row has a confirmed status before promotion. If "no" on any row, edit the copy to remove or hedge it (do not invent a substitute).

---

## Phase 2 — Homepage keyword preservation

The live site ranks for "luxury yacht rental San Diego." The rebuild leans hard into "yacht charter" instead. Don't change the homepage's primary intent during migration — keep "yacht rental" prominent on the homepage, let `/yacht-rental-san-diego/` deepen the topic.

### 5. Replace the homepage `<title>`

**File:** homepage HTML
**From:**
```html
<title>Luxury Private Yacht Charter San Diego | Malarky Charters</title>
```
**To:**
```html
<title>Luxury Yacht Rental San Diego | Private Catamaran Charter | Malarky Charters</title>
```

---

### 6. Replace the homepage meta description

**File:** homepage HTML
**From:**
> Private BYOB yacht charter on San Diego Bay. 47ft sailing catamaran, USCG captain available ($50/hr), up to 12 guests. San Diego Bay (open Pacific on full-day charters), no shared cruises. Reserve direct.

**To:**
> Luxury yacht rental in San Diego for up to 12 guests aboard Malarky, a private 47ft sailing catamaran. Captain and crew, BYOB food and drinks, San Diego Bay views, and easy online booking.

Also update the matching `<meta property="og:description">` and `<meta name="twitter:description">` to the same text.

---

### 7. Replace the homepage H1

**File:** homepage HTML
**From:**
```html
<h1>San Diego's Finest Yacht Charter — <strong>12 Guests, BYOB Welcome</strong></h1>
```
**To:**
```html
<h1>Luxury Yacht Rental in San Diego Bay for Up to 12 Guests</h1>
```

---

### 8. Rewrite the homepage hero paragraph

**File:** homepage HTML (the paragraph immediately below the H1)
**To:**
> Malarky Charters is a private luxury yacht rental in San Diego Bay aboard a 47-foot Voyage sailing catamaran. Includes captain and crew, BYOB food and drinks, room for up to 12 guests, and the whole boat reserved for your group.

---

### 9. Add a "Yacht Rental, Captain and Crew Included" section near the top of the homepage

**File:** homepage HTML — place after the hero, before "Meet Malarky / The boat, up close"
**Content:**
```html
<h2>Private Yacht Rental, Captain and Crew Included</h2>
<p>
  Your San Diego yacht rental includes a U.S. Coast Guard-licensed captain and crew to guide your charter through San Diego Bay. Bring your own food and drinks, settle into the shaded aft deck or bow trampoline, and enjoy a private day on the water with up to 12 guests.
</p>
```

---

### 10. Adjust the homepage stat labels

**File:** homepage HTML — the 4-stat row under the hero
**From:** "PRIVATE" → "USCG Captain"
**To:** one of:
- `PRIVATE YACHT RENTAL` → `USCG Captain`, OR
- `YACHT RENTAL + CHARTER` → `USCG Captain`

(Keep the other three stat blocks — 12 Guests Maximum, 47ft Voyage Catamaran, BYOB — unchanged.)

---

## Phase 3 — Content preservation from the old site

These exact phrases / details exist on the live site and should be naturally carried forward to the rebuild. Most belong on the homepage or `/yacht-rental-san-diego/`. Don't keyword-stuff — weave them into existing copy where they fit.

### 11. Reintroduce these phrases at least once each

Across the homepage + `/yacht-rental-san-diego/`:

- "luxury yacht rental San Diego"
- "yacht rental San Diego"
- "Malarky Charters Yacht Rental"
- "captain and crew" (lowercase, as a natural phrase)
- "Up to 12 Guests"
- "BYOB & Food" (use the ampersand exactly — this was the old hero copy)
- "San Diego Bay"

**Acceptance:** view-source on the homepage contains each of these strings at least once.

---

### 12. Restore Aquata + Alana sister-vessel references

**Action:** add an editorial mention with links — NOT a "Our Other Boats" widget. One contextual paragraph in the homepage or `/private-catamaran-charter-san-diego/` page.

**Suggested location:** at the end of the existing Triton mention. Suggested copy (only if Nate confirms these are still operational partners — otherwise skip):

> For groups larger than 12, our sister vessel [Triton Charters](https://triton-charters.com/) accommodates up to 100 guests. For a faster boat experience on the bay, see our sister [Aquata](https://aquatacharters.com/) — a luxury speedboat for up to 11 guests, hitting 55mph. For Bay Cruises and large private charters, see [Alana](https://alanayachtrental.com/) — San Diego Bay's newest 35-guest power catamaran.

[VERIFY WITH NATE — are Aquata and Alana still operational sister boats?]

---

### 13. Restore the arrival landmark detail

The old site has a useful arrival cue:

> Our office is located at 2700 Shelter Island Dr. and our charter is located on our commercial dock just south of our office. **If you are arriving for your charter, our vessel is located on our commercial dock behind Ketch Kitchen and Taps in Shelter Island.**

The rebuild's "Departure & Parking" section uses "Intrepid Boat Works Marina" as the landmark. Both can coexist — add the Ketch Kitchen and Taps reference as an alternate cue (different people find different landmarks; both are real and helpful).

**File:** homepage Departure & Parking section + `/info/` page
**Add a sentence:** "Our dock is in front of Intrepid Boat Works Marina, just behind Ketch Kitchen and Taps."

---

### 14. Verify the second FareHarbor flow

**Live site uses TWO FareHarbor flows:**
- `flow=1294652` — used by main "Book Now" buttons (rebuild keeps this — good)
- `flow=882335` — used by one specific CTA on the live homepage's boat section

**Action:** confirm with Nate whether `flow=882335` was a Malarky-specific deeper-booking flow (e.g., a customized question set or pricing structure) that should be restored, or if `flow=1294652` covers both cases.

[VERIFY WITH NATE — is flow=882335 still relevant?]

---

## Phase 4 — AI overview readiness fixes

From the rebuild audit against `AI-Overview-Readiness-Checklist.md` — current score 83/100. These fixes target the gaps.

### 15. Add JSON-LD schema (not currently visible in HTML fetch)

**Homepage** — add a `<script type="application/ld+json">` block with:
- `@type: LocalBusiness` (or more specific `Service` provider)
- `name`, `image`, `url`, `telephone`, `email`
- `address` (PostalAddress: 2700 Shelter Island Dr, San Diego, CA 92106, US)
- `geo` (lat/long for Shelter Island marina — look up)
- `priceRange: "$$$"` (yacht charter price tier)
- `openingHoursSpecification` (8am–8pm Pacific per the pricing page)
- `aggregateRating` with `ratingValue: 5.0` and `reviewCount: 412` (only if claim verified per Phase 1 step 4)
- `sameAs` array with Instagram, Google Maps URL, sister-boat URLs

**Each occasion page** (wedding, bachelorette, etc.) — add `Service` schema with `name`, `provider`, `areaServed: San Diego`, `serviceType`, `image`.

**Reservation CTA** — add `Reservation` schema or `Offer` schema on the booking links.

**Do NOT add `FAQPage` schema** if executing the FAQ-per-URL plan in step 18 — those compete.

**Acceptance:** `validator.schema.org` returns zero errors on home, wedding, and pricing pages.

---

### 16. Verify and fix robots.txt for AI crawlers

**File:** `/robots.txt` (production)
**Required content (minimum):**

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: anthropic-ai
Allow: /

Sitemap: https://malarkycharters.com/sitemap.xml
```

**Acceptance:** `https://malarkycharters.com/robots.txt` returns the above (or equivalent) after launch.

---

### 17. Add outbound citations to authoritative sources

**Why:** the rebuild scored 1/3 (6.7/20) on Pillar 3 of the AI Overview Readiness rubric. Pages that cite primary sources get cited back by LLMs.

**Targets — minimum 3 per long-form page.** Add as inline editorial links (no `nofollow`).

| Claim | Source to cite |
|---|---|
| USCG captain licensing | `https://www.uscg.mil/` or relevant licensing page |
| 47ft Voyage catamaran built in Cape Town | `https://www.voyageyachts.com/` |
| San Diego Bay wildlife (gray/blue whales, seals, dolphins) | NOAA Fisheries page, or `https://www.portofsandiego.org/` |
| Coronado Bridge | `https://dot.ca.gov/` page for the bridge, or Wikipedia as fallback |
| USS Midway Museum | `https://www.midway.org/` |
| Star of India | `https://sdmaritime.org/` (Maritime Museum) |
| Cabrillo National Monument | `https://www.nps.gov/cabr/` |
| BYOB legal context on California charters | California ABC reference (if cited) |

**Acceptance:** the homepage, wedding page, pricing page, and any "what we'll see" content each contain at least 3 outbound editorial citations to authoritative `.gov`, `.edu`, `.org`, or original-publisher domains.

---

### 18. Build the FAQ-per-URL hub

**Why:** playbook Section 12 — for sites without dominant authority, separate-URL FAQs out-rank consolidated FAQ schema.

**Action:** create `/faq/` index + the following individual pages. Each page = 100–300 words, tight slug, one-question H1, answer in first 50 words.

**Starter set:**

- `/faq/do-i-need-a-boating-license-to-charter-a-yacht-in-san-diego/`
- `/faq/is-malarky-a-private-charter-or-shared-cruise/`
- `/faq/can-the-captain-officiate-a-wedding/`
- `/faq/why-no-red-wine-on-the-yacht/`
- `/faq/how-far-in-advance-should-i-book-a-summer-charter/`
- `/faq/whats-the-difference-between-malarky-and-triton/`
- `/faq/can-i-bring-food-and-drinks-on-the-yacht/` (BYOB long-tail)
- `/faq/how-much-does-it-cost-to-charter-a-yacht-in-san-diego/` (pricing long-tail)
- `/faq/does-malarky-go-into-the-open-ocean/` (covers the full-day Pacific claim)

**Internal link rule:** each FAQ page links to the relevant occasion/service page; the consolidated FAQ blocks on home/wedding/pricing pages each link out to the matching individual FAQ URL.

**Acceptance:** `/faq/` index lists all 9 URLs; each individual page is indexable; no `FAQPage` schema (slug + H1 + page title carry the relevance).

---

### 19. Build the glossary hub

**Why:** playbook Section 12 — top-of-funnel curious searchers, highest-margin customers.

**Action:** create `/glossary/` index + the following individual pages. Each entry = 100–300 words explaining the term in plain language.

**Starter set:**

- `/glossary/voyage-catamaran/` (the boat builder + what makes a Voyage)
- `/glossary/uscg-captain/` (what the license means, why it matters)
- `/glossary/byob-charter/` (the model, the legal context, why rare)
- `/glossary/no-wake-zone-san-diego-bay/` (where they are, why they exist)
- `/glossary/micro-wedding/` (the format, the guest count range)
- `/glossary/golden-hour-sail/` (what it is, why it matters for photos)
- `/glossary/sailing-catamaran-vs-power-catamaran/` (the comparison)

**Acceptance:** `/glossary/` index lists all 7; each page indexable; internal-link from the relevant landing page (e.g., the wedding page links to `/glossary/micro-wedding/`).

---

## Phase 5 — Cutover & monitoring

### 20. Build a 301 redirect map for the WP image URLs

**Why:** any external backlinks to `malarkycharters.com/wp-content/uploads/...` will 404 after cutover.

**Action:** crawl the live site for image URLs, map each to the new `/images/...` path. Add 301s in `_redirects` (Netlify format) or equivalent for the new host.

**Acceptance:** the top 10 image URLs from the live site return 301 to the new image path on the rebuild.

---

### 21. Submit sitemap to GSC and Bing Webmaster after cutover

- Generate `sitemap.xml` covering every page on the rebuild (including new FAQ + glossary URLs from steps 18–19)
- Submit to Google Search Console
- Submit to Bing Webmaster Tools
- Add the sitemap reference to `robots.txt` (step 16)

---

### 22. Update the GBP website link

- Confirm Google Business Profile for Malarky Charters points to `https://malarkycharters.com/` (not the old WP-specific URL, not the Netlify URL)
- Verify the GBP primary category is set tight ("Boat rental service" or "Yacht charter service") and 3–5 secondary categories are filled
- Verify 20+ original photos are uploaded
- Verify business attributes are fully filled

---

### 23. Re-verify Site Kit / GSC / GA4 / Google Tag

The live site has Site Kit by Google installed (WordPress plugin). After cutover:
- Re-verify GSC for the production domain
- Add GA4 measurement ID to the rebuild templates
- Add Google Tag (gtag.js) if Site Kit was driving conversion tracking
- Verify Facebook Pixel from the live site (ID `1341176882596057`) is preserved if the client wants Meta ads continuity — [VERIFY WITH NATE]

---

### 24. Annotate the cutover date in GSC

After launch, add a custom annotation in Search Console for the cutover date — this is the "Custom annotations" feature shipped in 2026 (per `google-2026-seo-findings.md` Section 7). Future Nate will thank present Nate when reading the post-launch performance chart.

---

### 25. Test reservation flow + click-to-call on real mobile

- Pull out a real phone (not desktop responsive view)
- Test the FareHarbor booking flow end-to-end
- Test the click-to-call (`tel:+18447245787`)
- Test the "Get Directions" link to Google Maps
- Test the contact form (after Phase 1 step 2 fix)

---

## Final pre-launch checklist (single pass)

- [ ] All Phase 1 launch blockers cleared
- [ ] All [VERIFY WITH NATE] items confirmed
- [ ] Homepage view-source contains "luxury yacht rental San Diego"
- [ ] No `malarky-charters.netlify.app` strings in the build
- [ ] `noindex` removed from production HTML
- [ ] `robots.txt` allows AI crawlers
- [ ] JSON-LD schema validates without errors
- [ ] FAQ-per-URL hub published
- [ ] Glossary hub published
- [ ] Outbound citations live on home + wedding + pricing
- [ ] Sitemap submitted
- [ ] GBP updated
- [ ] GSC / GA4 re-verified
- [ ] Cutover annotation added to GSC
- [ ] Mobile test pass

---

## Things this list does NOT do (Nate's call)

- **Backlink audit on live site.** Whatever's pointing at the WordPress site needs a backlink scan (Bing Webmaster Tools is free per playbook Section 12). Anything deep-linking past the homepage needs a 301 in the redirect map. Not in this list because it needs GSC or Bing access.
- **GSC export → mining page-2 queries.** Once you have GSC for the live site, pull queries the homepage impresses for but doesn't win, and bake them into the rebuild's H2 structure. Highest-ROI post-launch task.
- **Lighthouse run.** Run on home + wedding + pricing templates. Confirm mobile Performance and SEO both ≥ 90 per the AI Overview Readiness Checklist.
