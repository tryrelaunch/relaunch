# _AUDIT.md — Blue Water Boat Rental (bluewaterboatrental.com)

*Audit date: 2026-06-07. Public-page crawl only (no GSC/GA4/GBP access — speculative preview). Ahrefs sheet data: 1,551/mo organic, DR 33. Status: AWAITING NATE'S APPROVAL before any copy or build work.*

## 1. Current page inventory

| URL | What it is |
|---|---|
| `/` | Homepage. Two H1s ("BOAT RENTAL NEAR PALM BEACH" + "Blue Water Boat Rental") — confirmed in crawl, matches the sheet's "2 competing H1s" |
| `/rates/` | The money page. All 10 boats + per-vessel pricing + policies + Peek checkout links |
| `/blue-water-boat-rental-frequently-asked-questions-faq/` | FAQ — strong owner-fact content, weak URL |
| `/boating-lessons-intro-to-boating/` | Intro to Boating lesson, $375/2 students |
| `/boat-rental-gift-card/` | Gift cards (Peek) |
| `/virtual-tour/` | Virtual tour |
| `/dockside-restaurants/` | Captained Dockside Dining trip ($450) + 15 partner restaurants. Blog post, not a page |
| `/local-islands/` | Peanut/Munyon/Singer Island. 2015 blog post, thin (2 paragraphs) |
| `/jupiter-inlet/`, `/palm-beach-inlet/` | Destination posts |
| `/scavenger-hunt-adventure-on-the-water/` | Promo |
| `/social-media-influencer-program/` | Promo |
| `/category/...` (fleet, boating-tips, tours-sights) | WP category archives |
| Blog posts (snorkel gear add-on, pontoon near Singer Island, Volt 17, Tritoon 20ft) | Fleet/SEO posts |
| `/author/bluewaterstaff/` | Author page |

Tech: WordPress + Divi, GTM, FB pixel, reviews-feed plugin, YouTube embeds. Sheet: site stalls on load; 7/18 images missing alt.

## 2. SEO-value pages to protect

- **`/rates/`** — Protect. Every booking flows through it; almost certainly their top organic lander after `/`.
- **`/`** — Protect + fix (single H1, keep "Boat Rental near Palm Beach / Peanut Island / Riviera Beach" intent).
- **FAQ page** — Protect content verbatim (real owner-facts: deposit, fuel, qualifications, dogs, captains).
- **`/dockside-restaurants/`** — Protect. Unique local content competitors can't fake; 15 named partner restaurants.
- **`/palm-beach-inlet/`, `/jupiter-inlet/`, `/local-islands/`** — Keep + improve. Long-lived URLs (2015) likely carrying backlink/age equity.

## 3. Weak but worth improving

- `/local-islands/` — two paragraphs for the #1 destination (Peanut Island). Their location across from Peanut Island is the whole pitch; this should be the strongest page on the site.
- Homepage class blurbs — "from" prices conflict with per-vessel pricing on `/rates/` (e.g. "$190" vs $225). Confusing and a trust leak.
- Blog fleet posts ("Customers Enjoying the Volt 17...") — thin, no schema, unclear if vessels are current fleet.

## 4. Missing pages to create

- **`/peanut-island-boat-rental/`** — Create, High. Their core differentiator has no dedicated money page ("peanut island" queries are the obvious local win — exact volumes Needs verification, no Ahrefs keyword export yet).
- **Per-class or per-boat fleet pages** (at minimum `/fleet/` index) — Create, Medium. 10 boats live in one long page; no Product/Service schema anywhere.
- **`/contact/`** — Create, Medium. No contact page; NAP only in footer. No email published anywhere — Needs verification.
- FAQPage schema on the FAQ, LocalBusiness schema sitewide — Create (schema, not pages).

## 5. Remove / consolidate / redirect

- Category archives — noindex or leave (low value, no harm).
- Thin fleet blog posts — Consolidate into fleet pages at launch (301), pending owner confirmation vessels are current.

## 6. URL decision map

| Old URL | New URL | Action | Priority | Why |
|---|---|---|---|---|
| `/` | `/` | Keep + improve (ONE H1) | High | Entity page; fix competing H1s |
| `/rates/` | `/rates/` | Protect + improve | High | Money page, keep URL exactly |
| `/blue-water-boat-rental-frequently-asked-questions-faq/` | same | Protect + improve | High | Ranking FAQ; URL ugly but changing it risks equity — revisit only with GSC data |
| `/boating-lessons-intro-to-boating/` | same | Keep + improve | Med | Unique service, real pricing |
| `/dockside-restaurants/` | same | Protect + improve | High | Unique local content + $450 captained product |
| `/local-islands/` | same | Keep + improve | Med | Age equity; beef up Peanut Island content |
| `/palm-beach-inlet/`, `/jupiter-inlet/` | same | Keep + improve | Med | Destination equity |
| `/boat-rental-gift-card/`, `/virtual-tour/` | same | Keep | Low | Functional |
| Missing | `/peanut-island-boat-rental/` | Create | High | Core money query, no page |
| Missing | `/contact/` | Create | Med | Conversion + NAP |
| Thin fleet blog posts | fleet pages | Consolidate + 301 (at launch) | Low | Needs owner verification first |

## 7. Recommended architecture (preview scope)

Preview ships: `/` + `/rates/` + `/faq/`* + `/dockside-restaurants/` + `/peanut-island/`* + `/boating-lessons/`*
(*preview subfolder names — production keeps the old URLs per the map above; preview is on boatrmarketing.com/preview/bluewater-boat-rental/ so parity matters at launch, not preview.)

## 8. Page-by-page content plan

- `/` — single H1 "Boat Rental near Palm Beach"; location lead (Riviera Beach Marina, across from Peanut Island, minutes from the Inlet); 5 class cards with CONSISTENT per-vessel from-prices; weather guarantee; reviews; NAP + hours + directions.
- `/rates/` — all 10 vessels with real pricing/age/seats from their site, Peek links preserved per-item, policies accordion (deposit, fuel, cancellation, qualifications).
- FAQ — their 14 real Q&As, FAQPage schema, answer-first.
- Dockside — $450 captained trip up top (answer-first), then north/south restaurant lists with NAP.
- Peanut Island — destination + how-to-get-there-by-rental, snorkel add-on, island facilities (from their copy).
- Lessons — $375/2 students, 3-hr curriculum, FL 1988 license rule.

## 9. Metadata plan

Keep query-bearing titles ("Boat Rental" + Palm Beach/Riviera Beach/Peanut Island modifiers). One title/description per page, no stuffing. Homepage keeps brand suffix.

## 10. Schema plan

LocalBusiness (BoatRental subtype N/A — use LocalBusiness + `additionalType`) with geo, hours (8-5 daily), NAP, sameAs (4 socials). Service schema per class; Product schema per vessel on rates page (real prices); FAQPage on FAQ; TouristAttraction on Peanut Island page. Only mark up visible content.

## 11. Internal linking plan

Home → rates (every class card), FAQ, lessons, dockside, Peanut Island. Every informational page → `/rates/` CTA. Footer: core pages only. Anchors: "Palm Beach boat rentals", "Peanut Island", "fleet and rates".

## 12. Image/photo needs

Their own uploads first (`wp-content/uploads/`): fleet cards (10 vessels — current photos exist), aerial Peanut Island, marina site plan, dockside dining, lessons. All converted to WebP, width/height attrs, descriptive alt on every image (fixes 7/18 missing alt). Hero: their Riviera-Beach-Marina/Peanut-Island aerial.

## 13. Conversion tracking and CTA risks

- Peek links are per-item — must carry over EXACTLY (16 item codes captured in `_INTAKE.md`). **Peek rule: no `data-button-text` when wrapping cards** (BOATR_OPERATIONS §7B).
- Waverunner books through FareHarbor (`getwetwatersports-fl`, item 352016) and is a third party — keep attribution to Get Water Sports + their phone.
- tel: links sitewide; GTM/FB pixel continuity is a launch-phase item, not preview.

## 14. Launch risk checklist (for the eventual real migration)

Redirects for any URL that changes (none planned); preserve FAQ URL until GSC says otherwise; NAP must match GBP (Needs verification); noindex stays ON for preview, comes OFF at launch; sitemap + GSC submission; annotate launch date.

## 15. Facts needing client verification

See `_INTAKE.md` "Facts that need verification" — owner names, years in business, email, GBP/review counts, homepage-vs-rates from-price conflicts, current fleet status of Volt 17 / Tritoon 20, electric-boat policy scope.
