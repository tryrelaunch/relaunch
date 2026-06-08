# _INTAKE.md — Blue Water Boat Rental

*Filled 2026-06-07 from the prospect's live site only (owner-facts rule: nothing invented). Unknowns marked `Needs verification`.*

## 0. Brand assignment (CONFIRMED, not inferred)

```md
Brand: Boatr   ← Nate confirmed in the project instructions for this Cowork project, 2026-06-07
Reason given: boat rental, marine vertical
```

### voice-scan override (frozen-template hits only)

Same situation as Red Boat (approved 2026-06-05): the remaining voice-scan hits are the frozen
Boatr banner's own format, not page copy. Per file: 16 bold-term hits in the frozen `.seo-row`
grid + 1 in the frozen `.seo-cta-row`, and 5 em dashes in frozen elements (banner signature line,
banner close button, nav aria-label, and two template code comments). All bold-term and em-dash
violations in page copy were fixed before this note was written; `grep -E "<strong>[^<]*[.:]</strong>"`
excluding `.seo-row`/`.seo-cta-row` returns zero across all 6 pages. Documented 2026-06-07.

## Basic Info

```md
Client: Blue Water Boat Rental (entity name on site: "Blue Water Power Boat Rentals" / "Blue Water Powerboat Rental")
Current website: https://bluewaterboatrental.com
Business type: Powerboat / pontoon / waverunner rental + boating lessons + captained trips
Primary location: Riviera Beach Marina (Marina Village), across from Peanut Island, minutes from Lake Worth (Palm Beach) Inlet
Full address: 200 East 13th Street, Riviera Beach, FL 33404, USA
Phone: (561) 840-7470
Email: Needs verification (no email published on site)
Google Business Profile URL: Needs verification (Google reviews widget present on homepage)
Primary CTA: BOOK NOW → /rates/ → Peek hosted checkout
Secondary CTA: Call (561) 840-7470
Booking/reservation platform: Peek Pro — account URL book.peek.com/s/1317293c-eaa8-45d8-9022-37bb972df127/<item>
  Known Peek item codes: 23' Powercat=3b3YE, 24' Pontoon=9RkB8, 21' CC=LDy4, 22' CC=9Ork, 18' Deck=AdDYO,
  21' Deck=E8Eg, 23' Deck=rPYy, 24' Deck=Xj28x, 21' Dual Console=LDLz, 22' Fundeck=xVWVz,
  Waitlist=3bE4A, Boating Lesson=WBe7v, Dockside Dining Trip=7vBey, Electric Cruise=emRdv,
  Lesson gift card=mveLM, Boat-ride gift card=peek.com/purchase/gift_card/54ff527bcf04c5c1bc000b3d
  Waverunners: provided by Get Water Sports — FareHarbor account `getwetwatersports-fl`, item 352016, flow 674868, phone 561-243-8938
Menu/fleet/services platform: WordPress + Divi (Elementor-free), reviews-feed plugin, PixelYourSite, GTM-MWPR223B
Social profiles: facebook.com/BlueWaterBoatRental · x.com/bwboatrent · instagram.com/bluewaterrentals · youtube.com/@bluewaterboatrental
```

## Business Goals

```md
What does the client want more of?
- Needs verification (prospect not yet contacted — preview is speculative)

Most profitable services/offers:
- Needs verification

Services/offers they do NOT want to push:
- Needs verification

Best customer types (inferred from site copy — verify):
- Families/groups visiting Peanut Island (snorkel, sandbar)
- Offshore anglers (center consoles)
- Larger parties (8-14, pontoons/deck boats)
- New local boaters (lessons)

Main competitors:
- Needs verification
```

## Real Business Details (from their site — verbatim facts)

```md
What makes this business different:
- Location: inside Riviera Beach Marina, directly across from Peanut Island, minutes from Palm Beach (Lake Worth) Inlet for easy ocean access
- Weather guarantee: $50 reimbursement for rentals returned 2 hours early due to rain/thunderstorms
- Waitlist system for last-minute availability (free to join, text/email notification)
- Dogs welcome ("All well-behaved pups are welcome")
- Higher experience standard than some rentals (2-yr similar-vessel rule)
- Golf-cart pickup from parking if guests need help with gear

Signature services/products/experiences:
- Self-drive fleet (classes S, V, O, H): 18'-24' deck boats, 21'-23' center consoles, 23' twin-outboard powercat, 24' pontoon, 22' Fundeck pontoon
- Waverunner rentals $149/hr (provided by Get Water Sports, 1-3 people / 350 lbs max, 18+, separate phone 561-243-8938)
- Intro to Boating: 3-hour lesson, $375 for two students, USCG-licensed Captain instructor, minimum 2 students
- Captained Dockside Dining Trip: $450, up to 4 guests, 4 hours (11am-3pm), boat + Captain + restaurant reservation included; food/drinks + gratuity not included; arrive 10:45am
- 33' Greenline Hybrid Electric Cruise "Adagio": captained charter, up to 6 people, $856/2hr to $3,424/8hr (solar + Volvo D3 diesel, silent electric mode)
- Gift cards (boat ride + lessons, via Peek)
- Scavenger Hunt ("Explore & Score: The Blue Water Scavenger Hunt")
- Snorkel gear rental add-on (premium adult gear), pre-stocked ice add-on, licensed Captain add-on, extra hour 5-6 PM add-on

Fleet & rates (from /rates/, per-vessel):
- 23' Twin Outboard Powercat CC (S,O) — seats 8 — 2hr $450 / half $650 / full $850 — 25+
- 24' Pontoon (H) — seats 13 — 2hr $425 / half $550 / full $750 — 25+
- 21' Center Console (S,O) — seats 6 — 2hr $225 / half $300 / full $425 — 25+
- 22' Center Console (O) — seats 8 — 2hr $375 / half $475 / full $600 — 25+
- 18' Deck Boat (S) — seats 6 — 2hr $225 / half $325 / full $450 — 25+
- 21' Deck Boat (S,H) — seats 10 — 2hr $295 / half $395 / full $520 — 25+
- 23' Deck Boat (H) — seats 12 — 2hr $350 / half $450 / full $575 — 30+
- 24' Deck Boat (H) — seats 12 — 2hr $375 / half $475 / full $600 — 30+
- 21' Dual Console (V,O) — seats 7 — 2hr $275 / half $375 / full $500 — 30+
- 22' Fundeck Pontoon (H) — seats 12 — 2hr $375 / half $475 / full $600 — 25+
- Waverunner — 3 people/350 lbs — $149/hr — 18+
NOTE: homepage "from" prices and the /rates/ "Understanding Vessel Classes" blurb quote LOWER from-prices
(e.g. S "2 hours from $190/$225") that conflict with per-vessel cards — flag as Needs verification, do not propagate the conflict.

Vessel classes (their own definitions):
- (S) Standard, 16'-21', 3-6 people — Intracoastal cruising, fishing, snorkeling around Peanut Island
- (V) Versatility Angler, 20'-23', 6-7 people — V-hull, offshore or Intracoastal
- (O) Offshore Angler, 20'-27', 6-8 people — center consoles, offshore fishing
- (H) High Occupancy, 21'-24', 8-13/14 people — deck boats/pontoons, Intracoastal cruising

Neighborhoods / waters / landmarks that matter:
- Peanut Island (snorkeling, museum / JFK nuclear bomb shelter), Munyon Island, Singer Island
- Palm Beach Inlet (aka Lake Worth Inlet), Jupiter Inlet / Loxahatchee River / Jupiter Lighthouse
- Intracoastal Waterway, Lake Worth Lagoon, Palm Beach, West Palm Beach, Palm Beach Gardens,
  Boynton Beach, Lantana (dockside-restaurant routes north + south)
- Dockside restaurant partners: Rafiki Tiki, Sailfish Marina, Frigate's, Seasons 52, the River House,
  Calaveras Cantina, Dive Bar, Guanabanas, U-Tiki Beach, Square Grouper, Lucky Shuks (north);
  E.R. Bradley's, Old Key Lime House, Two Georges, Prime Catch (south)

Arrival, parking, dock, entrance, or pickup instructions:
- Arrive 15 minutes early (10:45 for dining trip); rental shack/dock in Riviera Beach Marina;
  Parking Area 7 = shortest walk; golf-cart pickup available; I-95 directions on site (Blue Heron Blvd
  exit from north / 45th St Exit 74 from south → US-1 → 13th Street east into marina)

Hours and seasonal notes:
- Open 7 days, 8:00 am - 5:00 pm; optional add-on extra hour 5-6 PM; holiday/blackout periods excluded from promos

Pricing, minimums, deposits, quote expectations:
- MINIMUM $1,000 security deposit on all rentals without a licensed Captain
- Fuel and taxes NOT included; depart full tank, top off on return, deposit refunded minus fuel (barring damage/late fees)
- Reservations required; changes allowed up to 24 hours out

Licenses, certifications, safety details, credentials, experience:
- Renter qualification: 2+ years operating similar type/size (within 10 ft) vessels on tidal/navigable (non-lake)
  waters; no marine losses 10 yrs; no violations/suspensions (incl. auto) 5 yrs; no criminal convictions/no-contest pleas
- Failure to prove qualification on arrival = forfeited deposit
- FL law: born 1988+ needs NASBLA-approved boating license (temp test for waverunners, lifetime test for powerboats)
- Age minimums per vessel: 25+ most boats, 30+ on 23'/24' deck boats + 21' dual console, 18+ waverunner
- Captains available for parties of 6 or fewer (USCG limit); for 7+ they provide names of licensed captains
  but renter coordinates/pays directly (Coast Guard regulation)
- Safety equipment provided for whole group incl. child life jackets; complimentary coolers + dive flags;
  waterway map + ocean-conditions briefing at departure
- Staff: certified boating instructors, seasoned captains ("decades of combined experience")

Common customer questions (their FAQ, verbatim topics):
- Experience requirement / do I qualify; license requirement; baby counts as passenger (yes);
  dogs allowed (yes); captain for 7+; cancellation/weather; fuel costs; what to bring; tubing/wakeboarding (no)

Common customer objections:
- Strict experience requirement (their answer: add a Captain, parties ≤6)
- No towable watersports — insurance restriction (they point to other local captained-watersports businesses)

Things customers should bring, know, or avoid:
- Bring: ID, credit card, boating license if required; provisions welcome
- Provided: safety equipment, life jackets (incl. children's), coolers, dive flags, waterway map
- For purchase/rent on-site: ice, snorkel gear; marina ship store sells drinks/snacks/frozen bait; full-service restaurant on property
- NOT provided: fishing supplies — they recommend the Rod Room (gear) and Seven Seas Bait and Tackle (live shrimp/frozen bait) on Blue Heron Blvd
- No tubes/skis/wakeboards (insurance)
- Cancellation: full refund ≥24 hr; store credit if no-show without notice; after 5pm EST day-before = deposit forfeited
- Electric boat cancellation differs: full refund minus $20 fee ≥5 days; 24hr-5days = reschedule/raincheck; same-day non-refundable

Words, claims, or tone to avoid:
- Do not claim they rent waverunners directly (it's Get Water Sports)
- Do not claim captains for 7+ passengers (USCG restriction)
- Do not promise towable watersports
- "Promotions can not be combined"

Facts that need verification:
- Owner name(s) — not published on site (site byline is "BlueWater Staff")
- Years in business (blog posts go back to 2015 — implies 10+ yrs, verify before claiming)
- Email address; GBP URL; review count/rating
- Homepage vs /rates/ from-price conflicts (see fleet section)
- Whether "Volt 17 Electric Boat" / "TRITOON 20ft" (blog mentions) are current fleet
- Electric boat policy refers to cruises — confirm which vessels it covers
```

## Brand identity (extracted from current site)

See **`_BRAND.md`** in this folder (measured programmatically 2026-06-07 — hard rule satisfied).

```md
Color palette:
- Primary:    #0276BD  (logo dominant blue, 177k px)
- Secondary:  #064872  (logo navy)
- Accent:     #EDF000  (their BOOK NOW yellow, black text)
- Supporting: #0FB2E4  (logo cyan)
- Neutral/text: #666666 body / #333333 headings
- Background: #FFFFFF

Typography:
- Headline font family: Open Sans (wt 500)
- Body font family: Open Sans, Arial, sans-serif
- Google Fonts equivalent: Open Sans (native GF)

Imagery feel:
Bright, saturated, sunny Florida marina photography — real fleet shots at the dock, aerial Peanut
Island, customers aboard. Friendly and functional, not luxury-polished.

No-identity fallback: N/A — clear identity exists (blue/white/yellow, consistent logo use).
```

## SEO Evidence Packet

### Access Available

```md
Google Search Console access: No (speculative preview)
GA4 or analytics access: No
Google Business Profile access: No
Current hosting/CMS access: No (WordPress + Divi, Site Kit, GTM observed)
Domain/DNS access: No
Booking/form/CRM access: No (Peek Pro observed)
```

No GSC access yet. Crawl/audit inferred from public pages only — Needs Verification list above covers
anything that requires GSC, analytics, GBP, or client confirmation.

### Ahrefs-verified target data (from the rebuild-targets sheet)

```md
Organic traffic: 1,551/mo
Domain Rating: 33
On-page issues: 2 competing H1s; 7 of 18 images missing alt text; site stalls on load
```
