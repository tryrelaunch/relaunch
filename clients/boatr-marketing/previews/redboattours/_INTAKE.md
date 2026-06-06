# Red Boat Tours — Boatr Preview Intake

Slug: `redboattours` · Brand: **Boatr** · Built: 2026-06-05
Preview URL (on deploy): https://boatrmarketing.com/preview/redboattours/
Source site: https://redboattours.com (WordPress + Elementor 4.1.1)

## §0 — Voice-scan override (approved)

`voice-scan.sh` reports 22 BOLD-TERM hits on `index.html`. All 22 are the **frozen SEO banner's** `<strong>lead.</strong>` rows, which are part of the golden template's frozen structure (`_TEMPLATE_README §1.1` — copy verbatim, do not restructure). Reworking them would mean editing a frozen component.

**Override approved by Nate, 2026-06-05:** keep the frozen banner as-is and skip the bold-term check for this client. The em-dash rule passes (1 em-dash in `index.html`, the banner signature). No banned words or phrases present.

## Business

- Name: Red Boat Tours, LLC
- Owners: Captain Tony & Jennifer (family-owned Florida LLC, not affiliated with other operators)
- Vessel: *Pellicano* — 2022 50' Trident pontoon, 16' wide, twin 250 Suzuki outboards, USCG certified, 85% covered, restroom aboard
- Dock: Vilano Beach Fishing Pier, 260 Vilano Road, Vilano Beach, FL 32084 (free parking)
- Phone: 904-436-3566
- Booking: FareHarbor, account slug `redboatwatertours`
- Tours: Dolphin Odyssey ($39, 1.5 hr, 96% dolphin success) · Sunset BYOB (1.5 hr, all ages Sun–Wed, adults Thu–Sat) · Private Cruise (50+, call for pricing) · Nights of Lights (seasonal, $40–$49)
- Awards: TripAdvisor Travelers' Choice (2024), USA Today 10Best (2022)
- Social: instagram.com/redboattours · facebook.com/redboattours

## Brand identity (extracted from current site)

- Palette: Red `#C8102E` (logo red) on deep navy `#0a2540`, cream/sand neutrals. Applied to the template's `--b-orange` accent.
- Typography: template default retained (Archivo headings / Manrope body).
- Imagery: 23 real photos pulled from redboattours.com (dolphins, sunset, Nights of Lights, the Pellicano, the family). No AI or stock imagery.

## Audit used in the SEO banner (verified only)

- Live homepage title is "HOME - Red Boat Tours" (no target keyword)
- Ranks #5 for "st augustine boat tours" (1,100 searches/mo, Ahrefs)
- Meta description is a Father's Day promo (seasonal)
- Platform: Elementor 4.1.1 (dated)
- No tour-level schema on the live site
- Mobile PageSpeed: **TBD** — run `psi-check.sh` on the deploy URL. PSI free quota was exhausted 2026-06-05; the banner intentionally makes no speed claim until the real number is captured.

## Status

- [x] Homepage built from golden template; content swapped; 5 frozen components intact
- [x] Schema: LocalBusiness/TouristAttraction, Product+Offer per tour, FAQPage (Red Boat NAP, FareHarbor)
- [x] voice-scan: em-dash pass; bold-term overridden (§0)
- [ ] `psi-check.sh` on deployed URL (fills the banner speed line)
- [ ] git push to `tryrelaunch/relaunch` (authed as `tryrelaunch`) — pending Nate's go + Netlify-team verify
