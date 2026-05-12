# Relaunch — CHANGELOG

Dated log of significant changes. Append new entries at the top.

Format:
- One section per session/day
- Bullet points of what shipped, what changed, what broke and got fixed
- Don't include trivia (commit messages cover that) — only meaningful work

---

## 2026-05-11

**Malarky Charters — full rebuild + moved to dedicated Netlify project. Pre-launch QA.**

- **Created `clients/malarky/CLAUDE.md`** capturing client-specific policy, architecture, page inventory, deploy workflow, and known-bite traps. Future sessions touching Malarky should read this first.
- **Created dedicated Netlify project `malarky-charters`** (base dir + publish dir `clients/malarky`, no functions). Deliberately NOT named `client-malarky` — avoiding hosting fingerprints that link Boatr brands together (SEO penalty concern).
- **Site is live at `malarky-charters.netlify.app`** — 24 pages, all internal links resolving. DNS flip from hover.com (still pointed at WP Engine) pending.
- **Built partials infrastructure to fix recurring nav/footer drift:**
  - `clients/malarky/_partials/nav.html` + `_partials/footer.html` — single source for nav/footer with `__BASE__` / `__HOME_HREF__` placeholders
  - `clients/malarky/sync-partials.py` — Python build script that walks every `index.html` and replaces marker-wrapped (`<!-- NAV:START --> ... <!-- NAV:END -->`) blocks
  - `deploy.bat` now runs `sync-partials.py` automatically before commit/push (skip with `/skip-sync` flag)
  - Requires Python 3 on PATH (`py -3`) — installed via `winget install Python.Python.3.12`
- **Sitewide captain-policy sweep:** every "captain & crew included" / "captain handles" rewritten to "USCG captain available, $50/hr, hired separately." Meta descriptions, hero copy, trust strips, FAQ pages, pricing pages — every variant scrubbed across all 24 pages. Captain paid directly via Apple Pay / Venmo / PayPal / cash on arrival.
- **Open-ocean policy reversal:** old language was "we don't run open ocean." New policy: open Pacific allowed on full-day (4+ hour) charters. Updated sitewide.
- **BYOB policy clarification:** allowed (no glass, no red wine). Removed indefensible "San Diego's only BYOB" claim everywhere.
- **Sailing + crew-as-bartender features added:** the catamaran does sail when wind cooperates; crew serves drinks and handles hospitality. Mentioned where relevant.
- **Type scale unified:** every body paragraph standardized to 17px mobile / `clamp(17px, 1.3vw, 18px)` desktop. No more drift across sections/pages.
- **Hero image updated** — new composite from P1451861.jpg, cropped for impact, mobile uniform overlay at 0.72 opacity for WCAG AA contrast.
- **Meet Malarky gallery slider** built with native CSS scroll-snap (no JS framework). 3-up tiles desktop, 240px tablet, 72vw mobile peek. Button + dot navigation.
- **3D Matterport walkthrough** optimized — preconnect, `qs=1&play=0&dh=0&lp=0&hl=1`, rounded corners + shadow via `.matterport-embed`.
- **Fonts converted from render-blocking `@import` to non-blocking `<link rel="preconnect"> + <link rel="stylesheet">`** for Cabin + Montserrat on all 24 pages.
- **Schema markup restored + tightened:**
  - AggregateRating + 3 real Review objects kept (these are real reviews from Yelp/Google/Tripadvisor — earlier session had stripped them per a misread of the audit, since restored)
  - Google Business Profile linked via canonical CID URL (`12410663655035935065`) in `sameAs`
  - openingHours `Mo-Su 08:00-20:00`
  - Service + Vehicle + ImageObject + FAQPage + BreadcrumbList all valid
- **Homepage trim:** removed redundant yacht spec row (Length / Bedrooms·Bathrooms / Builder) — facts band under hero + section title already cover it.
- **17 truncated HTML pages repaired** — earlier sed-style regex passes had killed body content on info, pricing, deals, booking-info, articles, privacy-policy, plus broken `</a>`/`</section>` tags on homepage CTA and FAQ. Restored from healthy commits + surgical Edit-tool fixes.
- **CSS recovered from 115-line truncation** caused by a Python regex bulk-bump that lost the `@media` mobile-nav block. Restored from commit 28fdd42 and re-applied type bumps with single-line string replacements only — bulk regex on HTML/CSS is now flagged as a recurring-issue trap.

**Lessons logged into `clients/malarky/CLAUDE.md`:**
- Don't run bulk Python regex passes on HTML — they keep truncating pages. Use per-page Edit-tool string replacements or check out a known-good commit first.
- Don't edit nav/footer per-page — use the partials.
- Don't strip AggregateRating/Review schema — these reviews are real.
- Don't reintroduce "Captain Included" or "San Diego's only BYOB" language anywhere.
- Don't claim open-ocean for short charters.

---

## 2026-05-05

**Phase 1 shipped: persistent AI editing with PIN auth.**

- Built and deployed `auth.js` and `edit-persistent.js` Netlify functions on `tryrelaunch.com`
- Built `widget.js` (production edit widget, loaded cross-origin from `tryrelaunch.com/widget.js`)
- Built `templates/edit-page.html` — per-client PIN entry page
- Rewrote `strip-demo.py` as `strip-demo.js` (Node, since Python wasn't installed)
- Added `netlify.toml` redirects to block `/config/*` and `/netlify/*` from public access
- Added env vars to Netlify: `JWT_SECRET`, `GITHUB_TOKEN`
- Generated fine-grained GitHub PAT, scoped to repo + Contents R/W, 90-day expiry
- Installed npm deps: `jsonwebtoken`, `bcryptjs`, `cheerio`
- Promoted Spork from demo to live customer (`clients/spork/` + `config/clients/spork.json`)
- Created Netlify site for Spork at `client-spork.netlify.app`
- Verified end-to-end: PIN auth → JWT → widget injects → edit → Claude → GitHub commit → Netlify rebuild → live
- Three real test edits committed to Spork's HTML through the production widget
- Spork test PIN `845984` is currently in play — needs rotation before any live use
- Stripe still in TEST mode; live flip pending

**Earlier in the same session:**
- Stripe Checkout integration deployed and tested end-to-end (test mode)
  - `create-checkout-session.js` function with rate limiting, metadata capture
  - Updated `onboard.html` to remove fake card form, use real Stripe redirect
  - $99 test charge succeeded, subscription created with full metadata
  - Live mode price IDs noted but not deployed yet
- Initial `strip-demo.py` written (later rewritten as JS)
- Architecture critiqued by senior-dev review; v1.1 plan finalized
  - Decided on PIN auth (not magic link) for Phase 1
  - Decided on cross-origin functions at `tryrelaunch.com` (not duplicated per-site)
  - Decided on structured Claude responses (not raw HTML) for safety
  - Decided on `config/clients/[slug].json` at repo root (not in published dirs)

**Earlier the same day:**
- `.gitignore` and interactive `deploy.bat` shipped (Fix #2)
- Removed `node_modules` from git tracking; repo cleaned to HTML 98.3% / JS 1.5%
- Edit endpoint hardened with rate limiting, $50/mo Anthropic spend cap (Fix #1)

---

## 2026-05-04 (and earlier sessions)

- Built initial Relaunch marketing site at `tryrelaunch.com`
- Built onboarding flow `onboard.html` (4 steps: details → domain → plan → payment)
- Built first demo: Spork (Bend, OR restaurant) — full content, AI widget, SEO banner, sticky CTA
- Built second demo: Valentine's Sandwich Shop
- Initial Netlify setup with `tryrelaunch` site
- Initial `edit.js` Netlify function (session-only AI edits for demos)
- Architecture established: one repo, multiple Netlify sites with different base directories
