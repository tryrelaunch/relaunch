# Relaunch — STATUS

**Last updated:** 2026-05-05

> Read this first whenever you start a new session. It's the source of truth
> for "what's the state of the world right now?"

---

## What is Relaunch?

A service that rebuilds small business websites with AI, hosts them, and lets
the owner self-serve text edits via a chat widget. Pricing: $99 / $299 / $499
per month, no contracts.

Stack: pure HTML/CSS in one GitHub repo (`tryrelaunch/relaunch`), auto-deployed
to multiple Netlify sites — one per customer, each pointing at their own
folder (`clients/[slug]/`). Functions live exclusively at `tryrelaunch.com`.

---

## What's deployed and working

### Public surfaces
- ✅ Marketing site at `tryrelaunch.com`
- ✅ Demo previews at `tryrelaunch.com/previews/[slug]/` (currently: spork, valentines)
- ✅ Onboarding flow at `tryrelaunch.com/onboard.html` (4 steps, accepts URL params for prefill)

### Stripe (test mode currently)
- ✅ Stripe Checkout flow wired end-to-end (test card 4242 works)
- ✅ Customer metadata captured on subscription record (business_name, phone, slack_email, domain choice, plan)
- ⚠️ **Currently in TEST mode.** Statement descriptor still says "BOATR MARKETING."

### Phase 1 — Persistent AI editing
- ✅ Per-customer auth via 6-digit PIN (bcrypt-hashed, JWT issued, 30d expiry)
- ✅ Persistent AI text edits (commits to GitHub via Contents API, Netlify rebuilds)
- ✅ Production widget injection (only renders when valid JWT in localStorage)
- ✅ Public visitors see no edit UI
- ✅ Allowlist-based safety (only `id="edit-..."` elements can be modified, server validates)
- ✅ Deny-by-default CORS (per-client allowed_origins in config)
- ✅ Rate limiting (5 PINs/15min, 10 edits/hr — best-effort in-memory)
- ✅ Spork is fully promoted (`clients/spork/` + `config/clients/spork.json`)
- ✅ Spork edit widget proven with multiple real commits

### Infrastructure
- ✅ Netlify env vars: `JWT_SECRET`, `GITHUB_TOKEN`, `STRIPE_SECRET_KEY`, `CLAUDE_API_KEY`, `ANTHROPIC_MODEL` (all marked Secret)
- ✅ Netlify config blocks `/config/*` and `/netlify/*` from public access
- ✅ Multi-site Netlify topology (`tryrelaunch` and `client-spork` both deploying from same repo)
- ✅ `.gitignore` keeps node_modules out of repo
- ✅ `deploy.bat` for one-shot pushes (note: bug with new directories — see RUNBOOK)

### Tooling
- ✅ `strip-demo.js` — promotes a demo to production (strips demo elements, generates edit page, hashes PIN, writes config)
- ⏳ Still works manually — no `--auto-pin` flag yet

---

## Pending — must-do before sending cold emails

These are blockers for accepting real customers:

1. **Rotate Spork's test PIN** (`845984` was pasted in chat — currently public).
   ```
   node strip-demo.js spork --pin <new 6 digits> --rotate-only
   git add config/clients/spork.json
   git commit -m "Rotate spork test PIN"
   git push origin main
   ```

2. **Flip Stripe from test to live mode**:
   - Update Netlify env var `STRIPE_SECRET_KEY` to `sk_live_...` (overwrite test value)
   - In `netlify/functions/create-checkout-session.js`, swap the three TEST price IDs to LIVE:
     - Starter: `price_1TTqNlP1XFF6NaBoEakSDPe3`
     - Growth: `price_1TTqO6P1XFF6NaBo6qMV0Xfa`
     - Full Service: `price_1TTqOhP1XFF6NaBoNfjleuHK`
   - Push.

3. **Update Stripe statement descriptor** at https://dashboard.stripe.com/settings/account → set to `TRYRELAUNCH.COM` so customer cards don't show "BOATR MARKETING."

4. **Test the full prospect → customer flow** on the Valentine's preview (see RUNBOOK).

---

## Pending — nice-to-have (not blocking)

| Task | Time | When |
|---|---|---|
| `--auto-pin` flag in strip-demo.js | 5 min | Whenever |
| Replace mailto: with copyable email modal in widget | 10 min | If Windows app picker keeps annoying you |
| Apply / Discard preview before commit | ~2 hr | After 3-5 customers, if needed |
| Welcome email template stored in repo | 10 min | Before customer #1 |
| Better commit messages going forward | habit | Going forward |
| Fix `deploy.bat` to detect new untracked folders | 15 min | Whenever it bites again |

---

## Pending — Phase 2 (when you hit ~5 paying customers)

- Magic link auth (replaces PIN) — Resend/Postmark
- Customer dashboard at `tryrelaunch.com/dashboard`
- Stripe webhook → automated provisioning (no manual xcopy + script run + Netlify UI clicking)
- Distributed rate limiting (Netlify Blobs or Upstash)
- Edit history / undo from customer side
- Help-request form posting to Plain.com or similar
- Calendly integration for Full Service tier
- Image upload, layout edits, new section creation

---

## Pending — Phase 3+ (when you hit ~30 customers)

- Multi-user accounts per business
- Approval workflow (preview before publishing)
- Real-time collaboration
- Customer-facing analytics dashboard
- Edit approval workflow

---

## Architectural decisions on file (don't re-litigate)

- **One repo, multi-site Netlify deploys.** Customers don't have their own Netlify accounts. Each customer's site = a new Netlify "site" with base directory `clients/[slug]/`, all pointing at the same GitHub repo.
- **No database for now.** Configs are JSON files at repo root (`config/clients/[slug].json`). Read at runtime via GitHub Contents API.
- **PIN auth over magic link for Phase 1.** Faster to ship, no email service dependency. Magic link in Phase 2.
- **Static HTML, no frameworks.** Keep it simple.
- **localStorage JWT not HttpOnly cookie.** Acceptable for MVP because static sites have minimal XSS surface and AI edits are constrained to text-only via server-side allowlist.
- **Functions live only at tryrelaunch.com.** Customer sites call cross-origin. CORS is deny-by-default.
- **Claude returns structured JSON, not HTML.** Server validates against ID allowlist and applies via text-node replacement only.

---

## Open questions (not yet decided)

- Domain provisioning workflow when customer chooses "Get a new domain" (do we register at Namecheap/Cloudflare via API, or manually for now?)
- When does a customer's Netlify site get auto-created vs requiring manual UI work?
- What happens when a customer's monthly subscription fails to renew (dunning, then? cancel?)
- How do we handle a customer who wants to GIVE someone else access to edit their site? (multi-PIN per slug, or wait for accounts in Phase 2?)
