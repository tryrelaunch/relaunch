# Relaunch — RUNBOOK

Operational procedures. Look here when you need to do a thing — don't
re-derive it from memory.

---

## How to onboard a new paying customer (manual, Phase 1)

When you get a Stripe payment notification:

### 1. Check Stripe to get their info
- Go to https://dashboard.stripe.com/payments
- Click into the latest payment
- Note down: business name, email, phone, slug (you derive from business name), domain choice
- Click into the subscription to confirm it's recurring

### 2. Pick a slug
Lowercase, dashes for spaces, no special characters. Examples:
- "Mario's Pizza" → `marios-pizza`
- "Valentine's Sandwich Shop" → `valentines`
- "Joe's Auto Body" → `joes-auto`

### 3. Check that you have a demo for them
```
dir previews
```
If no demo exists for this customer yet, you'll need to build one first.
(Most customers will be coming from a cold email that already linked them
to their demo, so it should exist.)

### 4. Promote the demo to a client folder
Open Command Prompt:
```
cd C:\Users\Nsini\Downloads\relaunch-website
xcopy /E /I previews\<slug> clients\<slug>
```

### 5. Generate a random PIN (until --auto-pin ships)
```
node -e "console.log(String(Math.floor(100000+Math.random()*900000)))"
```
Copy the 6-digit output.

### 6. Run strip-demo.js
```
node strip-demo.js <slug> --pin <pin> --owner-email <their email> --allowed-origins https://client-<slug>.netlify.app https://<their-domain> https://www.<their-domain>
```

If they don't have a domain yet, omit the last two origins — you can add
them later when their domain is set up.

### 7. Push to GitHub
```
git add .
git commit -m "Promote <slug> to live customer"
git push origin main
```

### 8. Create the Netlify site
- https://app.netlify.com → **Add new site** → **Import an existing project**
- Connect GitHub repo `tryrelaunch/relaunch`
- Site settings:
  - **Site name:** `client-<slug>`
  - **Branch to deploy:** `main`
  - **Base directory:** `clients/<slug>`
  - **Build command:** *(leave empty)*
  - **Publish directory:** `clients/<slug>`
- Click Deploy

### 9. Connect their domain (if they have one)
Three paths based on their onboarding answer:

**A) "Keep my existing domain"**
- In Netlify: site → Domain management → Add custom domain → enter their domain
- Netlify gives you DNS records (or 4 nameservers). Email customer with instructions for their registrar.
- Once they update DNS, propagation is 1–24 hrs. Netlify auto-provisions SSL.

**B) "Get a new domain"**
- Register at Namecheap or Cloudflare (~$10–15/yr)
- Use Netlify DNS for simplicity
- Add to their site as custom domain
- SSL auto-provisions

**C) "I don't have a domain"**
- Tell them their site is at `client-<slug>.netlify.app` for now
- Offer to register one for them when they're ready

### 10. Send the welcome email

Manually send to their email (use your normal email client until automated):

> Subject: Welcome to Relaunch — your site is live
>
> Hi [first name],
>
> Welcome aboard! Your new site is live at **https://[their-domain or netlify URL]/**.
>
> **How to edit your site:**
> 1. Visit https://[their-domain]/edit/
> 2. Enter your edit PIN: **[6-digit pin]**
> 3. Click the green "Edit your site" button anytime to type changes — "update Saturday hours to 11–10", "change the phone number to 555-1234" — and we'll ship it in seconds.
>
> Your PIN works for 30 days. If you get locked out, just reply to this email.
>
> **For anything bigger** (new pages, redesigns, photo updates, integrations) just reply to this email. We'll respond within 24 hours.
>
> **Billing:** Your $99/month renews on [date]. Cancel any time by replying.
>
> Got questions? Reply — you'll always get a real human.
>
> — Nate
> Relaunch

---

## How to rotate a customer's PIN

If a customer forgets their PIN, asks for a new one, or you suspect leakage:

```
cd C:\Users\Nsini\Downloads\relaunch-website
node strip-demo.js <slug> --pin <new 6 digits> --rotate-only
git add config/clients/<slug>.json
git commit -m "Rotate <slug> PIN"
git push origin main
```

Wait ~30s for Netlify to rebuild. Email the customer the new PIN. The old
PIN is dead the moment the deploy finishes (because the bcrypt hash changed
in the config file).

Note: Existing JWTs issued under the old PIN are still valid until they
expire. To force-logout, change `JWT_SECRET` in Netlify env vars (this
invalidates ALL active JWTs across all customers — use with caution).

---

## How to flip Stripe from test to live

When ready to accept real money:

1. **Get live keys.** https://dashboard.stripe.com/apikeys (toggle off "Test mode" first). Click "Reveal live key." Copy `sk_live_...`.

2. **Update Netlify env var.** Site `tryrelaunch` → Site configuration → Environment variables → edit `STRIPE_SECRET_KEY` → paste live value. Save.

3. **Update price IDs in code.** Edit `netlify/functions/create-checkout-session.js`. Replace the three test price IDs with live versions:
   - Starter: `price_1TTqNlP1XFF6NaBoEakSDPe3`
   - Growth: `price_1TTqO6P1XFF6NaBo6qMV0Xfa`
   - Full Service: `price_1TTqOhP1XFF6NaBoNfjleuHK`

4. **Deploy.**
   ```
   git add netlify/functions/create-checkout-session.js
   git commit -m "Flip Stripe to live mode"
   git push origin main
   ```

5. **Update statement descriptor.** Settings → Account → Public details → Statement descriptor → set to `TRYRELAUNCH.COM`. Otherwise customers see "BOATR MARKETING" on their cards.

6. **Test with a real card.** Make a $99 charge to yourself, refund it. Confirm subscription record looks right.

---

## How to deploy

### Standard push (when there are file changes you want to keep)

```
cd C:\Users\Nsini\Downloads\relaunch-website
git add .
git commit -m "<short descriptive message>"
git push origin main
```

Netlify auto-deploys all affected sites in ~30–90s.

### Using deploy.bat (for tracked-file edits only)
```
deploy.bat
```

⚠️ **Known bug:** `deploy.bat` doesn't detect new directories — only modified
existing files. If you've added a new folder (e.g. `clients/[new-customer]/`),
use the manual `git add . && git commit && git push` flow above. Fix is on
the backlog.

### Verify deploy succeeded
- https://app.netlify.com/projects/tryrelaunch/deploys (main site)
- https://app.netlify.com/projects/client-<slug>/deploys (customer sites)

Look for "Published" in green. If a deploy fails, click into it → Deploy log
→ scan the last 30 lines.

---

## How to add a new editable element to a customer's site

If a customer wants AI-editable text in a section that doesn't currently
have an `id="edit-..."` attribute:

1. Edit `clients/<slug>/index.html` directly
2. Add `id="edit-<descriptive-name>"` to the element (must be a leaf element with text only — no nested HTML)
3. Push

The new ID becomes editable on the next AI edit attempt — the function
extracts the allowlist from the live HTML each time, so no function redeploy
needed.

⚠️ **Don't** add `id="edit-..."` to elements that contain nested HTML (e.g.
`<div>text <span>label</span> more text</div>`). The function skips those for
safety. To make those editable, restructure so the AI-editable part is a
pure-text leaf.

---

## How to debug common issues

### "Widget doesn't appear after PIN entry"
1. Open browser DevTools Console — check for errors
2. Verify `localStorage.relaunch_jwt` has a token (Application tab → Storage → Local Storage)
3. Check Network tab for `widget.js` request — should be 200 from `tryrelaunch.com`
4. View the page source — confirm the bootstrap `<script>` block is present at end of body
5. If bootstrap is missing, re-run `node strip-demo.js <slug> --pin <existing pin> --rotate-only` to regenerate

### "Sign in returns 403 origin_not_allowed"
1. Open `config/clients/<slug>.json` on GitHub
2. Verify `allowed_origins` array contains the EXACT origin you're loading from (including protocol, no trailing slash)
3. Add the missing origin and re-commit

### "Edit returns 500 no_editable_elements"
The customer's HTML has no `id="edit-..."` elements that are pure text. This usually means all the editable IDs are on elements with nested HTML (e.g. menu descriptions with `<span class="gf">GF</span>`).

Fix: restructure the HTML so at least some `edit-*` IDs are on simple text-only elements. Or accept that this customer's site can only be edited by you manually.

### "GitHub commit fails with 409 conflict"
Two edits raced. The function retries automatically up to 3 times. If you keep seeing 409s in logs:
1. Check whether someone is pushing manual commits to the same file simultaneously
2. If automated retries aren't working, manually push a tiny commit to advance HEAD, then retry the customer's edit

### "JWT verification fails / 401 invalid_token"
1. Verify `JWT_SECRET` env var is set in Netlify on `tryrelaunch` site
2. Customer should clear `localStorage.relaunch_jwt` and re-enter PIN
3. If it persists, check Netlify function logs for the exact JWT verification error

### "Stripe API error: No such price"
Mode mismatch. You're in test mode but using live price IDs (or vice versa).
- Check `STRIPE_SECRET_KEY` env var: is it `sk_test_...` or `sk_live_...`?
- Check the price IDs in `create-checkout-session.js`
- They must match — both test or both live

---

## How to delete a test customer

```
cd C:\Users\Nsini\Downloads\relaunch-website
rmdir /s /q clients\<slug>
del config\clients\<slug>.json
git add .
git commit -m "Remove <slug> test customer"
git push origin main
```

Then in Netlify: Site → Site configuration → Danger zone → Delete this project.

---

## How to add a new demo to previews/

This is a separate workflow from customer onboarding. Demos are for
prospects to see before they buy.

1. Create folder: `previews/<slug>/`
2. Create `index.html` with the standard Relaunch demo template (SEO banner, sticky CTA, AI widget, real content)
3. Make sure all editable text has `id="edit-..."` attributes
4. Add images to `previews/<slug>/images/`
5. Test locally by opening the file in a browser
6. Push to deploy

---

## Common environment variables (reference)

All set in Netlify on the `tryrelaunch` site. All marked Secret. All scoped
to Builds, Functions, Runtime.

| Var | Used by | Notes |
|---|---|---|
| `CLAUDE_API_KEY` | edit.js, edit-persistent.js | Anthropic API key |
| `ANTHROPIC_MODEL` | edit.js, edit-persistent.js | `claude-haiku-4-5-20251001` |
| `STRIPE_SECRET_KEY` | create-checkout-session.js | Test or live, swap when going live |
| `JWT_SECRET` | auth.js, edit-persistent.js | 32-byte hex, regenerate to invalidate all sessions |
| `GITHUB_TOKEN` | auth.js, edit-persistent.js | Fine-grained PAT, repo-scoped, Contents R/W only, 90-day expiry |
