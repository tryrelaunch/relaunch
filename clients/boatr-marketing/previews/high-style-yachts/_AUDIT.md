# Audit & Migration Plan — High Style Yachts (M/Y Tourbillon)

*Boatr · cold speculative build · 2026-06-12. Approve this + the URL map before any build.*

## 1. Current page inventory (5 pages, Wix)

| URL | Title | Notes |
|---|---|---|
| `/` | Luxury charter yacht \| Baja California Sur \| High Style Yachts | Card teasers (Special Occasions, Welcome, Fishing, Sunset) all link to one rates page; photo gallery (28 imgs incl. Russell Wilson/Ciara) |
| `/tourbillon` | Tourbillon yacht | Best page — full vessel spec, gear, staterooms, video, Matterport 3D, 519 lb marlin |
| `/excursions-rates` | Excursions & Rates | 3 offerings, all "call for pricing"; capacity figures; multi-day Sea of Cortez detail |
| `/explore-cabo` | Explore Cabo San Lucas | Thin — just 5 outbound travel links, no original content |
| `/contact` | Contact us | Form + two phone numbers; map |

## 2–5. Protect / improve / create / remove

**Protect (the equity worth keeping):**
- Brand entity "High Style Yachts" + "Tourbillon" + "Cabo San Lucas" naming throughout.
- 190 referring domains pointing at the root/branded pages — preserve URL paths so links don't break.
- Real proof assets: 519 lb black marlin, Russell Wilson & Ciara, Bisbee/Pelagic sponsorship, Matterport 3D, drone video.
- Verbatim vessel spec copy (it's specific and credible — exactly what AI shouldn't invent).

**Keep + improve:**
- `/tourbillon` — strong content, weak structure/schema. Add Service/Product schema, answer-first intro, image alt.
- `/excursions-rates` — split intent (see architecture) into dedicated, indexable service pages.

**Create (money pages the site is missing — this is where the 0 keywords come from):**
- `/cabo-sportfishing-charter/` — primary money term, no dedicated page today.
- `/sunset-cruise/` and `/whale-watching/` — have demand, currently buried in a shared page.
- `/multi-day-charters/` (Sea of Cortez / La Paz / Loreto) — high-value, differentiated.
- `/special-occasions/` — weddings/anniversaries/proposals (teased on home, no page).
- `/faq/` — 35+ Q&A for AI-citation + long-tail (none exists today).

**Consolidate / fix:**
- `/explore-cabo` is thin outbound links → rebuild as a genuine "Explore Cabo" guide or fold into FAQ/About. Low priority.

**Remove:** nothing with equity. (No pages should be deleted; 301 only if a slug changes.)

## 6. URL decision map

| Old URL | New URL | Action | Priority | Why |
|---|---|---|---|---|
| `/` | `/` | Keep + improve | High | Entity/home; holds most refdomains |
| `/tourbillon` | `/tourbillon/` (the yacht) | Keep + improve | High | Best page; preserve path |
| `/excursions-rates` | `/excursions-rates/` (hub) + new service pages | Keep + split | High | Don't drop the ranking/linked path; spawn money pages |
| Missing | `/cabo-sportfishing-charter/` | Create | High | Primary money keyword, no page |
| Missing | `/sunset-cruise/` | Create | High | Distinct intent currently buried |
| Missing | `/whale-watching/` | Create | Med | Seasonal Cabo demand |
| Missing | `/multi-day-charters/` | Create | High | Differentiated, high-ticket |
| Missing | `/special-occasions/` | Create | Med | Teased on home, no page |
| Missing | `/faq/` | Create | High | AI-Overview citation + long-tail |
| `/explore-cabo` | `/explore-cabo/` | Keep + improve (or fold to FAQ) | Low | Thin today; preserve path if links exist |
| `/contact` | `/contact/` | Keep + improve | High | Add NAP, map, click-to-call, form |

## 7. Recommended architecture

```
/
/tourbillon/              (the vessel — spec, gallery, 3D, video)
/cabo-sportfishing-charter/
/sunset-cruise/
/whale-watching/
/multi-day-charters/
/special-occasions/
/excursions-rates/        (rates hub linking the service pages)
/explore-cabo/            (optional guide)
/faq/
/contact/
```
Every page built by **copying the template** (incl. subpages — never from scratch).

## 8. Metadata plan
- Preserve the working keyword pattern: "Cabo San Lucas," "sportfishing," "luxury charter yacht," "Tourbillon."
- Unique title + meta per page; one H1 per page; answer-first first 50 words.
- Avoid throwing away the query (don't replace "Cabo Sportfishing Charter" with "Explore the Water Your Way").

## 9. Schema plan
- Home/Contact: `LocalBusiness` (subtype where valid) + `TouristTrip` / `TouristAttraction`, geo (Cabo), telephone, `sameAs`.
- Each service page: `Service` (`serviceType: "Sportfishing Charter"`, `"Sunset Cruise"`, `"Yacht Charter"`).
- `/tourbillon/`: `Product`/`Boat`-style spec + `ImageObject` gallery.
- `/faq/`: `FAQPage` (35+ Q).
- `BreadcrumbList` site-wide. No fake `AggregateRating` until real review data is supplied.

## 10. Internal linking
- Home → each money page (not just the rates page).
- Service pages → `/contact/` + `/tourbillon/`.
- FAQ answers → relevant service pages with natural anchors ("Cabo sportfishing charter," "multi-day Sea of Cortez").

## 11. Image / photo needs
- Scrape the prospect's own Wix media (`static.wixstatic.com/media/61a767_*`) — they have strong real photos. Target 70% from their site.
- Convert to WebP, add width/height + mobile hero variant (PSI gate).
- Do NOT generate fake captains/boats/guests. Real photos only.

## 12. Conversion / CTA risks
- **No online booking** — phone (US + MX) + email form only. Every CTA = click-to-call + email. Confirm whether they want FareHarbor/Peek added (default: keep call/email).
- Two phone numbers (US booking + MX captain) — label clearly so users call the right one.
- "Call for rates" everywhere — decide whether to keep (luxury norm) or publish real numbers.

## 13. Launch risk checklist
- Preserve all existing paths (190 refdomains); 301 only on slug changes; no redirect loops; no flat `X.html` beside dir `X/`.
- robots.txt allows AI bots; sitemap.xml; remove template `noindex` before any real launch.

## 14. Facts that need client verification (gates final copy — postmortem #3)
1. Real **pricing** (or confirm "call for rates" stays).
2. **Booking platform** — phone/email only, or wire FareHarbor/Peek?
3. **Departure marina/dock** address in Cabo + real **email** inbox.
4. **Capacity** per trip type (day 10 / sunset 18 / multi-day 10 — confirm).
5. **Years in business / years running Tourbillon**; any **license/USCG/MX** credentials to foreground.
6. **GBP / TripAdvisor / social** + real **review counts** (needed for banner credential + AggregateRating schema).
7. What day-trip charters **include** vs. what guests bring (licenses/bait/food) — don't invent.
