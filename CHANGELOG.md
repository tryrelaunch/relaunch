# Relaunch — CHANGELOG

Dated log of significant changes. Append new entries at the top.

Format:
- One section per session/day
- Bullet points of what shipped, what changed, what broke and got fixed
- Don't include trivia (commit messages cover that) — only meaningful work

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
