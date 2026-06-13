# _INTAKE — My Bend Getaway

*Relaunch preview intake packet. Source: live site fetch + Chrome inspection, 2026-06-12. Copy preserved verbatim where quoted.*

## §0 — voice-scan override (approved)
`voice-scan.sh` reports 23 hits on `index.html`. **All are inside the frozen SEO sales banner** (the `<strong>Headline.</strong> explanation` row pattern and the banner's em-dashes), which is the canonical template banner structure and is intentionally exempt — same precedent as Red Boat (2026-06-05). Verified 2026-06-12: zero voice hits exist in the actual site body copy (hero, listings, area guide, FAQ, footer were rewritten to remove em-dash overuse and bold-term lists). Skip voice-scan for this client; do not "fix" the banner. `preflight.sh` passes clean.

## Business
- **Name:** My Bend Getaway
- **Vertical:** Short-term / vacation rental portfolio (lodging). **Brand = Relaunch** (non-marine).
- **Location:** Bend, Oregon (downtown / Westside / Old Bend / Parks District)
- **Live site:** https://mybendgetaway.com/
- **Properties:** ~11 individually-listed units (see roster below)
- **Positioning angle:** "Live like a local" walkable downtown Bend stays, close to Drake Park, the Deschutes River, the Old Mill District, and Mt. Bachelor.

## Booking platform — KEEP (do not replace)
- **System:** Lodgify (confirmed — footer "Powered by Lodgify"; search bar is the Lodgify search widget)
- **Account slug:** `mybendgetaway`
- **Checkout host:** `checkout.lodgify.com/mybendgetaway`
- **Owner property group id (seen in markup):** `oid=372959`
- **Current per-property booking URLs:** `mybendgetaway.com/en/[property-slug]` (Lodgify-hosted)
- **Integration plan for rebuild:** embed Lodgify's **search box widget** on the home/listings page and a per-property **booking widget** (or "Reserve" link to the property's Lodgify page) on each listing page. Same pattern the platform already uses for FareHarbor/Peek. **Need from Nate:** Lodgify embed/widget IDs (or confirmation to deep-link to existing `/en/[slug]` pages).

## Property roster (verbatim names + current slugs)
| # | Name (verbatim) | Beds/Baths (stated) | Current slug | Notes |
|---|---|---|---|---|
| 1 | Farmhouse in Bend — "Hawkeye House" | 4 bed · 6 beds · 4 bath | `hawkeye-house-farmhouse-escape` | Celebrity chef **Brian Malarkey**'s place; ties to Hawkeye & Huckleberry Lounge (also a Relaunch preview). Hero/flagship. |
| 2 | Newly Remodeled Contemporary Cottage — "Drake Park Cottage" | — | `drake-park-cottage` | Steps from Drake Park, Deschutes River, downtown. |
| 3 | Charming 1 Bedroom Apartment in Historic Old Bend | 1 bed | `charming-1-bedroom-apartment-in-historic-old-bend` | 2nd-floor walk-up; bedroom up spiral staircase. Not for young kids / mobility issues. |
| 4 | Gorgeous 3 Bedroom Home on Bend's Westside — "Downtown Awbrey" | 3 bed | `gorgeous-3-bedroom-home-on-bends-westside` | Designed by HGTV's **Shannon Quimby**. Hot tub, cruiser bikes. |
| 5 | Spacious 1 Bedroom across from Drake Park | 1 bed | `spacious-1-bedroom-across-from-drake-park` | Historic — Bend's first maternity hospital, converted to apartments. Bikes + rafts. No pets. |
| 6 | 2 Bedroom Gem in the Heart of Bend Parks District | 2 bed | `2-bedroom-gem-in-the-heart-of-bend-parks-district` | Same 1919 building. Loft bedroom up spiral staircase. **30-day min stay.** |
| 7 | Hip Fun 1 Bed on Bend's Westside — "The Drake" | 1 bed | `hip-fun-1-bed-on-bends-westside` | HGTV's Shannon Quimby design. Newer listing, fewer reviews. |
| 8 | Cute 1 Bedroom with Great Location | 1 bed | `cute-1-bedroom-with-great-location` | Newest listing. 3 blocks to downtown, 2 to Drake Park. |
| 9 | Delightful 2 Bedroom Close to River | 2 bed | `delightful-2-bedroom-close-to-river` | 2 blocks to Drake Park; floaties + pump provided. |
| 10 | Adorable 2 bedroom 1/2 mile to Downtown & Old Mill | 2 bed (3rd loft) | `adorable-2-bedroom-12-mile-to-downtown-old-mill` | Loft bedroom via staircase ladder, 6 ft A-frame peak. |
| 11 | Sweet Studio 1/2 mile Downtown & Old Mill District | studio | *(BUG: links to #10's URL)* | Netted hammock built in. Ladder access — not for mobility issues. |

## Site-wide amenities (verbatim)
WiFi · Parking · Air Conditioning · Laundry · Bikes · Kayaks · Floats · No Smoking · No Pets (unless stated otherwise) · Check-in 4 pm · Check-out 11 am

## Location anchors (for area guide + SEO + map)
Drake Park · Deschutes River · Downtown Bend · Old Mill District · Mt. Bachelor (~25 min) · Mirror Pond · Newport Ave · The Box Factory · Cascade Lakes Scenic Byway · Bend Westside · Old Bend / Parks District

## Audit findings (on-page, already verified)
1. **`<title>` is literally "Home"** — no brand, no city, no keywords. Catastrophic for local SEO.
2. **Meta description and keywords are both "Home"** — zero search value.
3. **Currency defaults to EUR** on a Bend, Oregon site — trust/conversion killer for US guests.
4. **No structured data** (LocalBusiness / LodgingBusiness / VacationRental / FAQ) — invisible to AI search.
5. **"Powered by Lodgify" footer branding** — looks like a template, not a brand.
6. **Broken/duplicate link** — "Sweet Studio" points to the "Adorable 2 bedroom" URL.
7. **All ~11 listings on one long homepage** — no individual indexable property pages, so no unit ranks for its own searches.
8. **No area/neighborhood guide** — missing the highest-intent Bend content (and the section Nate prioritized).
9. **No reviews/ratings surfaced