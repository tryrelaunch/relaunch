# _AUDIT.md — Monhegan Boat Line

*Public-crawl audit (no GSC access). Decision language: Protect / Keep+improve / Redirect / Consolidate / Create / Remove / Needs verification.*
*Date: 2026-06-10.*

## The situation in one line

They rank **#1 organically** for the money terms ("monhegan island ferry," "...ferry schedule," "monhegan boat line") while the homepage has **no H1, no meta description, no structured data, and 10/16 images missing alt text.** They win on brand + a near-monopoly route, not on-page SEO. So the job is **protect the ranking, fix the on-page foundation, and make schedule+booking instant on mobile** — never throw away proven URLs.

## 1. Current page inventory (from crawl)

| URL | Purpose | Notes |
|---|---|---|
| `/` | Homepage | No H1; title OK; **no meta description**; 7-slide hero; intro + 3 cards (Ferry/Puffin/Charters). |
| `/schedule/` | 2026 schedule + fares + policies | Their highest-intent page. Schedule buried in a wide table; fares jammed into a table footnote. |
| `/boats/` | Laura B + Elizabeth Ann | Strong heritage content; low-res images. |
| `/puffin-cruise/` | Puffin & Nature Cruise | Real dates + fares; FH sheet 89759. |
| `/charters/` | Private charters | Occasion list; "call for rates." |
| `/lighthouse-cruise/` | Lighthouse cruise | **Private charter only**, no fixed price. |
| `/sunset-cruise/` | Sunset cruise | **Private charter only**, no fixed price. |
| `/port-clyde/` | Getting here | Rich local copy + driving directions + map. |
| `/monhegan/`, `/about-monhegan/` | The island | Destination/visitor content. |
| `/monhegan-ferry/` | Ferry landing | Returned empty on fetch — **needs verification**. |
| `/contact-us/` | Contact | Email not public. |
| `/rose-cottage-guest-house/` | Lodging | Ancillary. |

## 2. Protect (do not lose these)

- **Homepage `/`** — entity/brand page, ranks #1 for "monhegan boat line."
- **`/schedule/`** — ranks for "monhegan island ferry schedule." Highest-intent URL on the site. **Keep the URL.**
- **`/boats/`, `/puffin-cruise/`, `/port-clyde/`** — real ranking/იntent pages with unique content. Keep URLs, improve on-page.

## 3. URL decision map

| Old URL | New URL | Action | Priority | Why |
|---|---|---|---|---|
| `/` | `/` | Keep + improve | High | Add H1 "Monhegan Island Ferry", meta desc, schema. **Preview = this page.** |
| `/schedule/` | `/schedule/` | Keep + improve | High | Mobile-first schedule table + fares pulled out of the footnote. Preserve URL. |
| `/boats/` | `/boats/` | Keep + improve | Med | Heritage cards; hi-res images; FerryTrip/About schema. |
| `/puffin-cruise/` | `/puffin-cruise/` | Keep + improve | Med | TouristTrip schema; firm 2026 dates; FH sheet 89759. |
| `/port-clyde/` | `/port-clyde/` | Keep + improve | Med | Directions + map + LocalBusiness geo. |
| `/charters/`, `/lighthouse-cruise/`, `/sunset-cruise/` | same | Keep + improve | Low | Charter-only; consolidate cruises under one "Special Cruises" hub but **keep the individual URLs as 301-safe** if consolidated. |
| `/monhegan/` + `/about-monhegan/` | `/about-monhegan/` | Consolidate + 301 | Low | Two island pages → one; 301 the weaker. Needs verification of which ranks. |
| `/monhegan-ferry/` | `/` or `/schedule/` | Needs verification | — | Fetched empty. Confirm it exists/ranks before redirecting. |

**Rule for the live migration (not the preview):** preserve every ranking URL; 301 one-hop only when consolidating; never collapse the schedule or service pages into the homepage. The preview demonstrates the upgraded **homepage**; the multi-page build-out follows the map above.

## 4. Preview scope (what gets built now)

Single rich, mobile-first **homepage** (template copy) — the sales spec that shows #1 done right:

1. **Hero** — H1 `Monhegan Island Ferry` (their literal #1 keyword, currently no H1). Sub: "The original and only year-round ferry from Port Clyde, Maine." CTAs: Buy Ferry Tickets (FH) / View 2026 Schedule.
2. **2026 Schedule** — clean mobile-first table, anchor-linked from nav. The thing most visitors come for.
3. **Fares & what's included** — pricing, luggage, parking, reservation policy (pulled out of the footnote).
4. **The boats** — Laura B (1943 WWII heritage) + Elizabeth Ann cards.
5. **Special cruises** — Puffin & Nature (booked), Lighthouse / Sunset / Charters (contact) cards.
6. **Getting here** — Port Clyde, parking, "passengers only, no cars," map link.
7. **Footer** — NAP, click-to-call, socials, Sea Star Shop, "Site rebuilt by Boatr."

## 5. Metadata plan

- `<title>`: `Monhegan Island Ferry | Schedule & Tickets — Port Clyde, ME` (≤60 chars).
- `<meta name="description">`: schedule + fares + year-round value prop (they have none today).
- Canonical, OG + Twitter tags (for the FB/Pinterest/Instagram shares they clearly use).

## 6. Schema plan (they have zero today)

- `LocalBusiness` (or `TouristInformationCenter`) — name, address, geo, phone, openingHours, priceRange, sameAs socials.
- `FerryTrip` / `TouristTrip` — the Port Clyde⇄Monhegan route, provider, offers ($52 RT).
- `BreadcrumbList`.
- `FAQPage` — reservations, parking, luggage, pets, cars-on-island, sailing time.
- Only mark up what's visible on the page.

## 7. Internal linking

Nav anchors: Schedule · Fares · Boats · Cruises · Getting Here · Buy Tickets. Footer → Sea Star Shop, socials. (Full build: home→schedule, schedule→fares, cruises→puffin, getting-here→port-clyde.)

## 8. Image plan

Reuse their own hero slideshow + boat photos (downloaded to `images/`). Pull full-res Laura B / Elizabeth Ann from the media library (homepage versions are 300px). Convert all to WebP, add width/height + alt text on every image (fixes the 10/16-missing-alt problem). No stock, no AI.

## 9. Launch / conversion risks + needs-verification

- **Needs verification:** GBP URL, public email, `/monhegan-ferry/` status, which island page ranks, GSC data to confirm ranking URLs before any 301.
- **Don't invent:** keep "what to bring"/water-condition claims out unless owner-confirmed (Alligator Reef lesson). Ferry copy here is logistics-only, low risk.
- **FareHarbor:** lightframe overlay must clear the sticky nav z-index; test the embedded calendar on a real phone.
- **Preserve "year-round"** as the identity throughout — it's the differentiator vs. seasonal operators.
