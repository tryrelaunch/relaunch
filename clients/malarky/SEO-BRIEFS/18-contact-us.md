# Page Brief 18 — Contact Us

**URL:** `/contact-us/` (unchanged)
**Status:** Existing page has good form bones — needs: schema upgrade (ContactPage), update "Corporate Outing" occasion option to "Executive Charter" per brief #13 reposition, slightly expanded copy on response time and channels, hours-of-operation block.
**Target state:** ~600-800 words, ContactPage schema.

## Title (60 chars)
```
Contact Malarky Charters | San Diego Yacht Charter Inquiries
```
(59 chars)

## Meta (147 chars)
```
Contact Malarky Charters for San Diego yacht charter inquiries — call (844) 724-5787, email info@malarkycharters.com, or fill the form. 1-hour response.
```

## H1
```
Contact Malarky Charters
```

## Page Outline

1. Hero — H1 + lede on response-time commitment (1 business hour 8am-8pm Pacific)
2. Contact Channels — Phone, email, form. Each with use case (phone for complex/urgent, email for date holds with details, form for general)
3. Form (preserve existing Formspree integration; update occasion options)
4. Office & Dock Address — 2700 Shelter Island Dr, dock location behind Ketch Kitchen & Taps
5. Hours of Operation — 8am-8pm Pacific daily for response; charter hours by appointment
6. Sidebar with direct contact + map link

**Form occasion options updated:**
- Birthday Party → Birthday Charter (keep)
- Bachelorette Party (keep)
- Anniversary / Romance (keep)
- Wedding Reception → Wedding Charter
- Proposal (keep)
- **Corporate Outing → Executive Charter** (per brief #13 reposition)
- Sunset Cruise → Private Sunset Charter
- General Charter (keep)
- ADD: Water Toys Day

## Schema
- BreadcrumbList
- ContactPage (with contactPoint sub-entity for phone/email)
- LocalBusiness reference (link to homepage @id)

NO AggregateOffer / AggregateRating. NO dollar amounts.

## Acceptance Criteria
- ContactPage schema added
- Form occasion list updated (Executive replaces Corporate)
- Response time committed in copy (1 business hour, 8am-8pm Pacific)
- Sitemap entry added (priority 0.7)
- Single H1, valid title/meta lengths
- No fleet rule violations
