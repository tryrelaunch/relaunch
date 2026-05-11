# Page Brief 17 — Articles / Charter Resources Hub

**URL:** `/articles/` (unchanged slug)
**Status:** Existing stub page — full rebuild as a "Charter Resources" themed hub. No net-new articles; the page organizes existing transactional content around editorial themes.
**Target state:** Approximately **1,400–1,800 words**, schema: CollectionPage + ItemList.

> Strategic role: Malarky doesn't have a deep blog archive. Rather than ship a thin "coming soon" articles page or invest in net-new evergreen articles for this build, the /articles/ page functions as a planning-resources index — themed editorial intros (each 150-250 words) that organize the existing transactional pages around how prospective customers actually research a charter. The page captures informational long-tail search intent ("how to plan a yacht proposal san diego," "yacht charter planning guide san diego") while routing users to the deeper pages that already exist.

---

## Keyword Targets

| Role | Keyword | Notes |
|---|---|---|
| Primary | yacht charter planning guide san diego | Informational |
| Primary | yacht charter resources san diego | Hub intent |
| Secondary | how to plan a yacht proposal san diego | Long-tail informational |
| Secondary | how to plan a yacht charter wedding san diego | Long-tail informational |
| Secondary | yacht charter ideas san diego | Variant |
| Tertiary | malarky charters blog | Brand+content |

**Off-limits:** Specific dollar amounts. Mission Bay / Pacific / small-boat / kid framing.

---

## Title Tag (60 chars)

```
Yacht Charter Planning Guide San Diego | Malarky Resources
```

(56 chars)

---

## Meta Description (149 chars)

```
Yacht charter planning resources for San Diego Bay — how to plan a proposal, anniversary, wedding, executive offsite, or BYOB charter on Malarky.
```

---

## H1 (single, on page)

```
Yacht Charter Planning Resources — San Diego Bay Bookings, Explained
```

---

## Page Outline

| # | Section | H-level | Target words | Content |
|---|---|---|---:|---|
| 1 | Hero | H1 | 180 | H1 + lede: "the planning-side of a Malarky charter. Each theme below links to the deeper page for the booking itself." Quick nav links to themes |
| 2 | Planning a Proposal Charter | H2 | 220 | The proposal-on-the-bow editorial intro. The bow-trampoline-at-golden-hour signature. The captain coordinating timing. Link to `/proposal-yacht-charter-san-diego/` |
| 3 | Planning a Wedding or Elopement | H2 | 200 | Micro-wedding/elopement framing. Ceremony on bow, 12-guest cap, vendor coordination. Link to `/wedding-yacht-charter-san-diego/` |
| 4 | Planning an Anniversary Charter | H2 | 200 | Milestone vs just-us-two scenarios. Link to `/anniversary-yacht-charter-san-diego/`. Cross-link to Alana's content for informational anniversary planning |
| 5 | Planning a Bachelorette or Birthday | H2 | 220 | Intimate-private-BYOB framing. Adult positioning (Rule 0a). Cross-link `/bachelorette-yacht-charters-san-diego/` and `/birthday-yacht-charter-san-diego/` |
| 6 | Planning an Executive Charter | H2 | 220 | Board offsite, client dinner, C-suite milestone. Discretion-trained crew. Link `/executive-yacht-charter-san-diego/` |
| 7 | The BYOB How-To | H2 | 180 | What to bring, what's forbidden, cost-savings story. Link `/byob-yacht-charter-san-diego/` |
| 8 | Water Toys Planning Guide | H2 | 180 | Five toys, bundle logic, mid-day timing. Link `/boat-rental-with-water-toys-san-diego/` |
| 9 | Final CTA | H2 | 60 | "Pick the right page for your booking" + FareHarbor + phone |

**Total target: ~1,650 words.**

---

## Schema Markup

```html
<!-- Schema #1: BreadcrumbList -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Home","item":"https://malarkycharters.com/"},
    {"@type":"ListItem","position":2,"name":"Charter Planning Resources","item":"https://malarkycharters.com/articles/"}
  ]
}
</script>

<!-- Schema #2: CollectionPage + ItemList -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "@id": "https://malarkycharters.com/articles/",
  "name": "Yacht Charter Planning Resources",
  "description": "Editorial planning guides for booking a Malarky yacht charter on San Diego Bay.",
  "url": "https://malarkycharters.com/articles/",
  "mainEntity": {
    "@type": "ItemList",
    "itemListElement": [
      {"@type":"ListItem","position":1,"name":"Planning a Proposal Charter","url":"https://malarkycharters.com/proposal-yacht-charter-san-diego/"},
      {"@type":"ListItem","position":2,"name":"Planning a Wedding or Elopement","url":"https://malarkycharters.com/wedding-yacht-charter-san-diego/"},
      {"@type":"ListItem","position":3,"name":"Planning an Anniversary Charter","url":"https://malarkycharters.com/anniversary-yacht-charter-san-diego/"},
      {"@type":"ListItem","position":4,"name":"Planning a Bachelorette or Birthday","url":"https://malarkycharters.com/bachelorette-yacht-charters-san-diego/"},
      {"@type":"ListItem","position":5,"name":"Planning an Executive Charter","url":"https://malarkycharters.com/executive-yacht-charter-san-diego/"},
      {"@type":"ListItem","position":6,"name":"BYOB How-To","url":"https://malarkycharters.com/byob-yacht-charter-san-diego/"},
      {"@type":"ListItem","position":7,"name":"Water Toys Planning Guide","url":"https://malarkycharters.com/boat-rental-with-water-toys-san-diego/"}
    ]
  }
}
</script>
```

**No FAQPage** (info page covers FAQs). **No Offer/AggregateOffer/AggregateRating.**

---

## Internal-Link Map

Every theme section links to its dedicated transactional page. The hub function is the primary value.

**Cross-fleet links — 1 allowed:** Alana for informational anniversary content (per Section 4 / brief #11 coordination).

---

## Image Plan

| Section | Filename | Alt text |
|---|---|---|
| Hero | `boat-aerial-skyline-25.webp` (existing — keep) | Malarky catamaran on San Diego Bay — yacht charter planning resources |

Single hero only. Themed sections are prose+links; per-section images would clutter the index function.

---

## Cross-References to Fleet Rules

- ❌ Do NOT include Offer / AggregateOffer / AggregateRating
- ❌ Do NOT include specific dollar amounts
- ❌ Do NOT include Mission Bay / Pacific / small-boat / kid framing
- ✅ Single H1
- ✅ Schema: BreadcrumbList + CollectionPage with ItemList
- ✅ Update sitemap.xml (add articles URL, priority 0.6)

---

## Acceptance Criteria

- [ ] Word count approximately 1,400-1,800
- [ ] Title ≤60, meta 140-155
- [ ] Single H1, exact text
- [ ] 9 sections (hero + 7 themes + final CTA)
- [ ] Schema: BreadcrumbList + CollectionPage+ItemList with 7 entries
- [ ] No Offer/AggregateOffer/AggregateRating
- [ ] No specific dollar amounts
- [ ] All internal links resolve
- [ ] No fleet rule violations
- [ ] Sitemap updated (priority 0.6)

---

*Next brief: `18-contact-us.md`.*
