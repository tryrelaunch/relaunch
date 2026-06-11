# _INTAKE.md — Monhegan Boat Line

*Historical record of every fact + decision behind this preview build. Underscore-prefixed so Netlify ignores it.*

## 0. Brand assignment (CONFIRMED, not inferred)

```
Brand: Boatr   ← Nate confirmed in chat on: 2026-06-10
Reason: Year-round passenger ferry / marine vertical.
```

**Voice-scan override (§0) — approved.** Residual `voice-scan.sh` hits in this build come only from FROZEN platform elements, not authored site copy:
- The `.seo-banner` rows use the template's `<strong>X.</strong>` bold-term pattern and several em dashes. This is the gold-standard banner, frozen and copied verbatim (same approved override as Red Boat Tours, 2026-06-05).
- The `<title>`, meta description, and JSON-LD schema `name` fields use a conventional em dash (e.g. "Monhegan Island Ferry — Port Clyde to Monhegan"). Standard SEO formatting, not prose.
- The frozen edit-widget welcome line and the booking-iframe `title` each contain one em dash.

All *authored* body copy (hero, about, schedule, fares, boats, cruises, getting-here, footer) was cleaned: no `<strong>X.</strong>`/`<strong>X:</strong>` bold-term patterns, banned words, banned phrases, or banned structures, and em dashes reduced to ~zero (schedule separators converted to middots). Per `PREVIEW_TEMPLATE.md` pre-ship gates, treat the script's banner/head hits as informational for this client.

## Multipage build (2026-06-11)

Expanded from one page to a multipage site matching their live menu. Pages: `/` (home overview), `/schedule/` (schedule + fares + policy), `/boats/` (Laura B + Elizabeth Ann), `/cruises/` (puffin + lighthouse + sunset + charters), `/port-clyde/` (Getting Here + directions + map). Nav + footer link through to these on every page; "Buy Tickets" everywhere opens the FareHarbor modal (ferry 89753 / puffin 89759 / gift).

Two deliberate deviations from the single-file frozen template, both to make multipage reliable and consistent:
- **Shared assets:** the frozen CSS/JS were moved to `assets/site.css` + `assets/site.js` and linked by every page (one source of truth; identical buttons/behavior across pages). Frozen class names and JS function names are unchanged. NOTE for promotion: the widget endpoint to swap (`/edit` → `/edit-persistent`) and the fab label now live in `assets/site.js`, not inline.
- **Mobile hamburger added:** the template shipped with `.nav-links{display:none}` on mobile and no toggle — the menu was unusable on phones (most of their traffic). Added a `.nav-toggle` + `toggleNav()`; nav now works on mobile.

Stray `images/lb_*.jpg` and `images/ea_*.jpg` are leftover 404 probes (couldn't delete — mount is create/overwrite-only); neutralized to valid images, unreferenced. Safe to delete on Nate's machine.

## Basic Info

```
Client:                Monhegan Boat Line
Current website:       monheganboat.com (WordPress)
Business type:         Year-round passenger ferry + nature/charter cruises
Primary location:      Port Clyde, Maine (St. George Peninsula)
Full address:          880 Port Clyde Road, Port Clyde, Maine 04855
Phone:                 1 (207) 372-8848   (tel:12073728848)
Email:                 via /contact-us (not public on site)
Google Business Profile: Needs verification
Primary CTA:           Buy Ferry Tickets (FareHarbor)
Secondary CTA:         View 2026 Schedule
Booking platform:      FareHarbor — account slug `monheganboat`
Services platform:     FareHarbor (gift certificates too)
Social:                facebook.com/MonheganBoatLine · instagram.com/monheganboat · pinterest.com/monheganboat
Sister retail:         Sea Star Shop (seastarshop.com) — shares the dock/ticket office
```

## Business Goals (inferred from site + brief — confirm w/ owner at conversion)

```
Wants more of:    Ferry reservations (core); puffin/nature cruise bookings; charter inquiries
Most profitable:  Ferry round trips (year-round backbone); Puffin & Nature cruise (seasonal premium)
Don't-push:       n/a
Best customers:   Island day-trippers & overnight visitors, artists/tourists, seasonal residents; planners researching Jan–Apr on mobile
Competitors:      Near-monopoly on the Port Clyde→Monhegan route; "the original and only year-round" service. (Hardy Boat Cruises runs New Harbor→Monhegan seasonally — different port.)
```

## Real Business Details (verified from live site 2026-06-10)

**What makes them different:** The original and *only* year-round ferry to Monhegan. A genuine island lifeline — mail, packages, freight, fuel, and essentials 365 days a year. Real heritage in the boats.

**The two boats (heritage = a real differentiator):**
- **Laura B** — built 1943, 65 ft. Former U.S. Army T-57; served WWII in the Pacific as a patrol/troop boat, carried two .50-cal machine guns, came under fire. Brought to Maine 1946, ran lobsters Vinalhaven→Boston/NYC. Now the early-morning summer run + all year-round freight. Indoor + outdoor seating. Described by a marine surveyor as the best-maintained wooden vessel on the Eastern Seaboard. **70 min one way.**
- **Elizabeth Ann** — launched 1995, 65 ft. Heated glassed-in cabin, covered stern, sightseeing deck, two bathrooms. Year-round passengers + mail. **55 min one way.**

**Route:** Port Clyde ⇄ Monhegan Island, 10 miles off the Maine coast, through Muscongus Bay. Passengers only — no cars on the island.

**Ferry fares (2026, verified):** $52 adult round trip · $35 child (2–12) round trip · $35 adult one way · $20 child one way · $10 pet. Two luggage pieces (≤50 lb) included; extra/oversized $6/item. Parking at the Port Clyde dock $10/day (weekly/monthly available). Boarding 15 min before departure. **Advance reservations required.**

**Reservation policy (verified):** Tickets held until ½ hr before departure with full payment. Payment transferable to another date if you call ≥24 hrs prior. Refundable less $5/person deposit if you call ≥24 hrs prior.

**2026 Ferry Schedule (verified verbatim from /schedule/):**

| Dates | Depart Port Clyde | Depart Monhegan |
|---|---|---|
| Jan – Mar | Mon* & Thu 9:30 AM | Mon* & Thu, immediately upon reloading |
| April | Mon/Wed/Fri 9:30 AM | Mon/Wed/Fri, immediately upon reloading |
| May 1–14 | 9:30 AM (no Sun) | 11:30 AM (no Sun) |
| May 15–31 | 10:30 AM / 3:00 PM | 12:30 PM / 4:30 PM |
| Jun 1–30 | 7:00 AM (Wed–Sat) + daily 10:30 AM / 3:00 PM | 9:00 AM (Wed–Sat) + daily 12:30 PM / 4:30 PM |
| Jul 1 – Aug 31 | 7:00 AM (Tue–Sat) + daily 10:30 AM / 3:00 PM | 9:00 AM (Tue–Sat) + daily 12:30 PM / 4:30 PM |
| Sep 1–15 | 7:00 AM (Wed–Sat) + daily 10:30 AM / 3:00 PM | 9:00 AM (Wed–Sat) + daily 12:30 PM / 4:30 PM |
| Sep 16–30 | 7:00 AM (Wed & Sat) + daily 10:30 AM / 3:00 PM | 9:00 AM (Wed & Sat) + daily 12:30 PM / 4:30 PM |
| Oct 1–12 | Daily 10:30 AM / 3:00 PM | Daily 12:30 PM / 4:30 PM |
| Oct 13 | 9:30 AM | 11:30 AM |
| Oct 14 – Dec 31 | Mon*/Wed/Fri 9:30 AM | Mon*/Wed/Fri, immediately upon reloading |

\*Excludes postal holidays; boat runs the next business day.

**Puffin & Nature Cruise (verified):** 2½ hrs, depart 11:30 AM, return ~2 PM. $55 adult / $25 child. Out to Eastern Egg Rock (Audubon Project Puffin nesting site); seals, porpoises, minke whales, live lobster-trap haul + expert commentary. **2026 dates:** Jun 17–30 (Wed–Sat); Jul 1–Aug 22 (Tue–Sat). FareHarbor sheet `89759`.

**Maine Lighthouse Cruise (verified — private charter only):** Marshall Point (the "Forrest Gump" lighthouse), Whitehead, Two Bush Light, Southern Island (Jamie Wyeth's studio in the pyramid bell tower). No fixed pricing — contact for charter.

**Sunset Cruise (verified — private charter only):** Protected waters around Port Clyde at golden hour. No fixed pricing — contact for charter.

**Charters (verified):** Customized private charters — birthdays/anniversaries, family reunions, wedding-weekend cruises, group outings & fundraisers, memorial services. Call for rates. Also island freight hauling. (Photo credit: Peter Brandon Photography.)

**Gift certificates:** Sold via FareHarbor.

**Getting here / Port Clyde (verified):** Working fishing village at the tip of the St. George Peninsula. ~2 hrs from Portland or Bangor (full driving directions on /port-clyde/). Sea Star Shop shares the dock. Nearby: Marshall Point Light (~2-mi round-trip walk, since 1833), Herring Gut Learning Center. Map: maps.app.goo.gl/o69qAoDiQjs2r8FRA. Rose Cottage Guest House available to stay.

**Facts needing verification at conversion:** GBP URL; public email; whether to keep Rose Cottage / Sea Star cross-links; any seasonal schedule update after build.

## Brand identity (extracted — see `_BRAND.md` for measured detail)

```
Primary (logo nautical blue):   #0060A0
Primary dark (navy):            #003960
Secondary (steel-blue water):   #48607D
Accent / CTA (sunset gold):     #C8842D
Ink / body text:                #312D2E
Background:                     #F4F8FB
Headline font:                  Lora (serif, heritage)
Body font:                      Source Sans 3
Imagery feel:                   Warm golden-hour working-harbor documentary; weathered, nostalgic New England coastal. Reuse their own photos; no slick stock / no AI.
No-identity fallback:           N/A — clear existing identity (blue logo + golden-hour photography).
```

## SEO Evidence Packet

```
GSC access:        No (not yet provided)
GA4 access:        No
GBP access:        No
Hosting/CMS:       WordPress (no access)
DNS:               No
```

**Audit basis:** public crawl only (no GSC). Needs-verification list maintained in the audit (Task 3).

### The hook (from build brief — pitch informs the build)
They are the **#1 organic result** for "monhegan island ferry," "monhegan island ferry schedule," and "monhegan boat line" — yet the homepage has **no H1, no schema, no meta description, and 10 of 16 images missing alt text.** They win on brand + a near-monopoly route, not on the site. The preview shows what #1 *should* look like and makes the schedule + FareHarbor booking instant on mobile (most Jan–Apr planning traffic is phones). Outreach timing: off-season Nov–Mar (Nate's call).

## FareHarbor wiring (embed, don't rebuild)
```
Account slug:   monheganboat
Ferry flow:     https://fareharbor.com/embeds/book/monheganboat/items/?selected-items=60827,60831&sheet=89753&full-items=yes
Puffin flow:    https://fareharbor.com/embeds/book/monheganboat/items/?selected-items=60827,60831&sheet=89759&full-items=yes
Gift certs:     https://fareharbor.com/embeds/book/monheganboat/items/
Lightframe:     <script src="https://fareharbor.com/embeds/api/v1/?autolightframe=yes"></script>
Primary CTA:    Buy Ferry Tickets → ferry flow (FH lightframe)
```

## Photo assets (their own — reuse, re-export hi-res, compress to WebP)
- Logo: `/mblines/wp-content/uploads/2023/11/mbl-2.png`
- Hero slides (7): `/mblines/wp-content/uploads/2023/12/MBL-HOMEpage-slideshows-rev{,2..7a}.jpg`
- Laura B: `/mblines/wp-content/uploads/2023/11/LauraB-300x225-1.jpg` (low-res; pull full-res)
- Elizabeth Ann: `/mblines/wp-content/uploads/2023/11/The-Elizabeth-Ann-300x169-1.jpg` (low-res; pull full-res)
- Downloaded to `images/` for this build: logo.png, hero1–3.jpg, laurab.jpg, elizabethann.jpg.
