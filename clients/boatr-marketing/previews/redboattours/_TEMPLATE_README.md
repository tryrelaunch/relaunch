# THE GOLDEN GOOSE — Canonical Preview Template

**Status:** Source of truth for every Relaunch and Boatr preview build.
**Based on:** Alligator Reef Boat Rentals preview (the best-built preview to date).
**Last promoted:** 2026-05-22.

> **READ THIS FIRST.** Before building a new preview, copy this entire folder, then read the rules below. The header (SEO banner), sticky claim bar, AI editor widget, and footer in this template are the **gold standard**. Don't rewrite them. Don't redesign them. Don't experiment. Copy them verbatim and only swap content where this README says it's safe to.

---

## How to use the template

```bash
# Boatr preview
cp -r clients/boatr-marketing/previews/_template/ clients/boatr-marketing/previews/[slug]/

# Relaunch preview
cp -r clients/boatr-marketing/previews/_template/ previews/[slug]/
# Then apply the Relaunch brand swap (Section 4 below)
```

After copying, work through the five sections of this README in order: ① frozen elements (never touch), ② safe swap zones (content only), ③ **brand identity extraction (pull from the prospect's current site)**, ④ brand swap (Relaunch vs Boatr badge/voice), ⑤ pre-ship checklist.

---

## 1. FROZEN — never modify these

These five pieces are the canonical product experience. They are identical across every Relaunch and Boatr preview. **If you touch the HTML structure, CSS class names, or JS function names in any of these, the partials sync will break and consistency dies.**

### 1.0 The top nav (including mobile hamburger)
- Search the HTML for `<nav class="nav">` or class names starting with `.nav-`.
- Desktop: horizontal menu. Mobile (below ~768px): hamburger button (`.nav-toggle`) that toggles a slide-down `.nav-menu`.
- The hamburger JS toggle function (look for `toggleNav()` or similar) is frozen.
- The `@media (max-width: 768px)` CSS block that swaps desktop nav for the hamburger is frozen.

**KNOWN FAILURE MODE:** previous rebuilds have shipped with broken mobile hamburgers because Claude rewrote the nav from scratch instead of copying it. The hamburger silently failed on mobile while the desktop nav looked fine. **Do not rewrite the nav.** Copy it verbatim from the template, then change only the link list (menu items) and the logo text.

You may change: the link list (menu items + logo). Not the toggle button, the toggle JS, the media-query CSS, or any nav class names.

### 1.1 The SEO banner (top of page)
- Search the HTML for `class="seo-banner"` — everything inside that container is frozen.
- The collapsed state ("Hey [Business] — we rebuilt your site. Here's why it matters 👇" + "Read this first ▼") is frozen.
- The expanded panel structure (greeting → two-column grid → footnote → CTA strip) is frozen.
- The `toggleSEO()` JS function is frozen.
- The CSS class names (`.seo-banner`, `.seo-top`, `.seo-panel`, `.seo-grid`, `.seo-row`, `.seo-ico.x`, `.seo-ico.c`, `.seo-cta-row`) are frozen.

You may change: the **copy** inside the banner (greeting text, problem rows, win rows, CTA copy). Not the structure.

### 1.2 The sticky claim bar (bottom of viewport)
- Search for `class="sticky-bar"`.
- Three elements, fixed order: text → CTA button → close button.
- Pattern: `"Like this? <span>Let's make it [customerdomain].com.</span>"` + `"Make this my site →"` button.
- The close-button JS (`closeBar()`) and `localStorage` "remember closed state" behavior are frozen.

You may change: the `[customerdomain]` reference and the prospect-name query string in the CTA. Not the structure or button copy.

### 1.3 The AI editor widget (floating, bottom-right)
- Search for `class="edit-fab"` and `class="edit-panel"`.
- The floating green pill button "Edit this site" with the animated dot is frozen.
- The chat-panel UI (welcome message, suggestion chips, typing indicator, textarea, send button) is frozen.
- The `toggleEditPanel()`, `addMessage()`, `useChip()`, `handleKey()`, `autoResize()`, `sendEdit()` JS functions are frozen.
- The endpoint is `/.netlify/functions/edit` (preview phase only). When this preview is promoted to a live customer, the endpoint becomes `/.netlify/functions/edit-persistent` — that's the only widget change post-payment.

You may change: the welcome message copy and the four suggestion chip examples (tailor them to the prospect's actual content — "Change [their menu item] to $20" etc.). Not the structure or widget classes.

### 1.4 The footer
- Search for `<footer>`.
- The three-column layout (logo/tag/mini → Visit links → Connect links) is frozen.
- The bottom row pattern (© year · address  /  "Site rebuilt by [Brand]") is frozen.

You may change: the link list and the address/phone strings. Not the layout. **The "Site rebuilt by [Brand]" line is mandatory** — this is the visible footprint the AI widget removes on Phase 2 promotion. Do not change wording without updating the promotion script.

---

## 2. SAFE TO CHANGE — content swap zones

Everything else is fair game. Specifically:

- All hero copy, body copy, service/tour descriptions, FAQ entries, pricing tables, testimonial blocks
- All images (replace `/images/*.jpg` with the new prospect's images)
- The `<title>`, `<meta description>`, `<meta og:*>` tags
- All `<link rel="canonical">` URLs
- All schema markup (JSON-LD `<script type="application/ld+json">` blocks)
- All FareHarbor / booking-platform embed slugs
- All phone numbers, addresses, hours
- All `id="edit-..."` element IDs are part of the FROZEN structure, but the **text inside** them is content — swap freely

---

## 3. BRAND IDENTITY EXTRACTION — pull from the prospect's site FIRST

**The principle:** we are not reinventing this business. We are rebuilding their site **better, faster, and SEO-stronger** while keeping the brand identity their customers already recognize. The template ships with placeholder marine colors and a default font stack — that is **not** what the prospect's preview should ship with.

Before doing the BRAND SWAP in Section 4, do this extraction:

### 3.1 Open the prospect's current website in a browser

Have their live site open in a tab. You'll be reading colors and fonts directly out of it. The values go into `_INTAKE.md` under the "Brand identity (extracted from current site)" section (see `brain/NEW_CLIENT_HANDOFF.md`).

### 3.2 Extract the color palette

Pull hex values for at least these four roles:

- **Primary** — the dominant brand color. Usually the logo color, nav background, or hero accent.
- **Secondary** — supporting color used on section backgrounds, secondary CTAs, or accents.
- **Accent** — the CTA / call-to-action color (the "Book Now" button, link hover state).
- **Neutral / text** — the body text color and the page background.

How to pull them: open DevTools → inspect their hero, nav, primary CTA button, and footer → read the computed `background-color` and `color` values. Or use a color-picker browser extension on screenshot pixels. If their logo has 2–3 distinct colors, those usually drive the primary/secondary.

Write the values into the CSS variable block at the top of the template's `<style>` (look for `--leaf`, `--green-lt`, etc.). The variable names stay; the hex values become the prospect's.

### 3.3 Extract the typography

Inspect the prospect's headlines (`h1`, `h2`) and body text in DevTools and record the `font-family` for each:

- **Headline font family** — what their hero and section headers use.
- **Body font family** — what their paragraph text uses.

If they use a Google Font, note it by name (e.g. `Montserrat`, `Lato`). If their `font-family` is a generic system stack (`Helvetica Neue, Arial, sans-serif`), pick the closest Google Font equivalent (e.g. `Inter` for clean modern sans, `Source Serif Pro` for a sober serif). Add the matching `<link rel="preconnect">` + Google Fonts `<link>` to the `<head>` and swap the template's font-family declarations.

### 3.4 Extract the imagery feel

Write a one- or two-sentence note describing their photography style. This guides what new images get sourced and how they're treated. Examples:

- "Rustic + warm — golden-hour lifestyle shots, slightly faded, family-on-the-water vibe."
- "Polished travel-magazine — high saturation, dramatic skies, professional-looking gear shots."
- "Muted editorial — desaturated, lots of negative space, lifestyle over product."
- "Generic stock photos — no consistent through-line."

This note isn't applied to CSS; it's a brief for sourcing new images (and for filter/treatment choices if any post-processing is applied).

### 3.5 No-identity fallback — ASK NATE

If the prospect's site has no clear brand identity — generic Wix template, no consistent colors, default Times-New-Roman, stock photos with no through-line — **stop and ask Nate** in chat before picking a palette. Do NOT default to Boatr marine or to a Relaunch neutral on instinct. Nate will either pick a direction or pick a palette that fits the vertical. Record his answer in `_INTAKE.md` under the brand-identity section, with a note like "No existing identity to preserve — Nate chose [palette] on [date]."

### 3.6 Apply to the template

In the template's `<style>` block at the top of `index.html`, replace:
- The hex values inside the CSS variable declarations (`--leaf`, `--green-lt`, accent variables, neutral/text) with the extracted palette.
- The `font-family` declarations on `body`, `h1`-`h6`, and any explicit font rules with the extracted typography (and add the Google Fonts `<link>` to the `<head>`).

Do not change the variable **names** — only the values. The frozen elements (banner, sticky bar, widget, footer) all reference these variables, so a clean swap re-themes the whole preview in one place.

### 3.7 Why this section exists

The most recent build shipped with the same marine teal as the Alligator Reef template because nothing in the docs forced extraction. Prospects who see "their" rebuilt site in someone else's colors don't feel ownership of it, and the preview-to-Stripe conversion suffers. We're not reinventing them — we're upgrading them. Their identity stays; the speed, SEO, and structure get better.

---

## 4. BRAND SWAP (Relaunch vs Boatr badge/voice — NOT colors)

Section 3 already handled the prospect's colors and typography. This section is only about the **brand badge, attribution, and voice** swap that distinguishes Relaunch vs Boatr previews. Colors and fonts do NOT change here — those came from the prospect.

| Find | Replace with |
|---|---|
| `<div class="seo-badge">Built by Boatr</div>` | `<div class="seo-badge">Built by Relaunch</div>` (Relaunch preview only) |
| `Site rebuilt by <a href="https://boatrmarketing.com">Boatr Marketing</a>` | `Site rebuilt by <a href="https://tryrelaunch.com">Relaunch</a>` (Relaunch preview only) |
| Banner voice tone | Boatr → captain / tour-operator. Relaunch → practical SMB-owner. |
| CTA href starts with `/onboard/?prospect=...` | Same path — both brand sites serve `/onboard/`, no URL change needed |

Everything else is identical. Same banner structure, same sticky bar, same widget, same footer layout. Prospect-extracted palette and typography apply to both brands.

---

## 5. PRE-SHIP CHECKLIST

Before this preview ships, verify:

- [ ] **MOBILE HAMBURGER WORKS.** Open the preview on a real phone (not desktop responsive view). Tap the hamburger icon. Menu should slide open and links should be tappable. If the icon does nothing or the menu doesn't appear, the nav toggle JS or media-query CSS got dropped during build. Diff against the template and restore.
- [ ] **PALETTE + TYPOGRAPHY MATCH THE PROSPECT'S CURRENT SITE.** Open the prospect's live site and the preview side by side. The colors and fonts should feel like the same brand, not the marine/teal template default. If they match the template default, you skipped Section 3 — go back and extract.
- [ ] `<meta name="robots" content="noindex,nofollow">` is **REMOVED** before production launch (it's in the template so the staging URL doesn't pollute search; remove it the moment this goes live for a real prospect)
- [ ] `<title>`, meta description, canonical URL match the prospect
- [ ] SEO banner greeting has the prospect's real owner name(s) + their actual credential (review count, longevity, award)
- [ ] SEO banner gut-punch is specific to their site (not generic)
- [ ] Banner left-column problems pull real Ahrefs / PageSpeed data — no placeholders
- [ ] Banner CTA links to `/onboard/?prospect=[slug]&business=[Name]&url=[domain]&phone=[number]` with all params filled
- [ ] Sticky bar copy mentions the prospect's actual domain (e.g. `Let's make it joesplumbing.com`)
- [ ] Editor widget suggestion chips are tailored to the prospect's content
- [ ] Footer "Site rebuilt by [Brand]" line shows the correct brand
- [ ] No `alligator-reef` / `Alligator Reef` / `alligatorreefboats.com` strings anywhere
- [ ] No `305-990-5207` (Alligator Reef phone) anywhere
- [ ] All images replaced with prospect's images
- [ ] Schema markup updated with prospect's NAP + service types

---

## 6. The full sequence — preview to /edit page

Every preview → live customer journey follows this sequence. Do not deviate.

```
1. Preview deploys at:
     [brand-domain]/preview/[slug]/      (with banner + sticky + widget on TEMP endpoint)

2. Prospect clicks "Make this my site →" or "Make it mine →"
   → Lands on [brand-domain]/onboard/?prospect=[slug]&business=...&url=...&phone=...

3. /onboard/ presents Stripe checkout (tier selection: $99/$299/$499)
   → Stripe webhook fires on successful subscription

4. On payment success:
   a. Copy clients/boatr-marketing/previews/[slug]/ → clients/[slug]/
   b. STRIP the SEO banner from clients/[slug]/index.html
   c. STRIP the sticky-claim-bar from clients/[slug]/index.html
   d. STRIP the "Site rebuilt by [Brand]" footer line from clients/[slug]/index.html
   e. SWAP widget endpoint from /.netlify/functions/edit → /.netlify/functions/edit-persistent
   f. Create clients/[slug]/edit/ subfolder (PIN gate — see RELAUNCH_OPERATIONS §6)
   g. Generate 6-digit PIN, bcrypt-hash, write to config/clients/[slug].json
   h. Send customer welcome email with PIN + DNS instructions

5. Customer points DNS at the new Netlify project
   → Custom domain attached, HTTPS auto-provisions

6. Customer's site is now live at customerdomain.com
   Editor is now at customerdomain.com/edit (PIN-gated, persistent edits commit to GitHub)
```

**Everything in steps 4a–4d should eventually be automated by a `promote-to-client.py` script** that takes the slug, performs all the strips and the endpoint swap, and creates the PIN config. Until that script is built, follow the steps manually using this README as the checklist.

---

## 7. Why this template exists

Three previous problems this fixes:

1. **Inconsistent banners across previews.** Each one diverged. Hawk & Huck had no sticky bar. Mandon-Welch had no checkout CTA. Now they all share one source of truth.
2. **Docs that described the widget got out of sync with the code.** Now the code IS the doc. Update the template, every new preview inherits.
3. **Onboarding a new Cowork project required pasting prose specs into chat.** Now: pin `brain/`, point Claude at this template, copy it, swap content, ship. Done.

**Consistency is king.** Every Relaunch and Boatr preview that ships should look like it came from the same factory. This template IS that factory.

---

*Save to: `clients/boatr-marketing/previews/_template/_TEMPLATE_README.md`*
*Related: `brain/PREVIEW_TEMPLATE.md` (high-level overview), `brain/RELAUNCH_OPERATIONS.md` (platform mechanics)*
