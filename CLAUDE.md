# CLAUDE.md — Relaunch Project Brief

This file is your context for working in this repo. It describes what Relaunch is, how the codebase is organized, and how things ship. Read it once at the start of any session.

---

## What Relaunch is

Relaunch is a productized service that rebuilds local business websites with AI before the business asks. It targets local businesses (restaurants, charters, salons, dentists, contractors, gyms — any small business with a public-facing website that's underperforming). The thesis is that most local business sites are stuck in 2014: slow, ugly, no schema, no SEO, bad mobile, weird Squarespace or GoDaddy templates, broken booking flows. Owners know it's bad but rebuilding feels expensive, slow, and risky.

Relaunch removes every objection at once. We rebuild the site for them — completely, end-to-end, modern HTML/CSS, proper SEO schema, real photography, fast load times, mobile-first — and we send it to them as a working live URL before they've paid a dollar. They click the link, see their own business reimagined, and the only decision left is whether to keep it.

## How the offer is structured

Three tiers:

- **Starter — $99/mo:** they get the rebuilt site, hosted, maintained.
- **Growth — $299/mo:** site + ongoing SEO work, monthly content updates, performance monitoring.
- **Full Service — $499/mo:** site + SEO + Google Business management + monthly reporting + priority edits.

No contracts. Cancel anytime. The customer's only commitment is a credit card on file via Stripe. The pitch in the cold email is essentially: *"I rebuilt your website. Here's the link. If you want to make it your real site, it's $99/month and I'll point your domain at it tomorrow. If not, no hard feelings, the demo stays up for a month."*

## How we acquire customers

One cold email per prospect. The email includes the live demo link. The prospect clicks, sees their own business with a beautiful new site, and is converted by the artifact itself, not by the copy. The email's job is just to deliver the link. The site does the selling.

That's why the demo has to be good. Not "AI-generated boilerplate good." Genuinely better than what they have. Real photos pulled from their existing presence (their Squarespace, their Yelp, their Google Business profile, their Instagram). Their actual menu items, actual prices, actual hours. Their actual reviews quoted on the page. The prospect should look at it and think "wait, this is mine."

## The editable on-page chat widget — how it works

Every demo site has a small floating widget pinned to the bottom-right corner of every page. The prospect can click it and type something like "make the hero blue instead of green" or "swap the second photo for the team picture" or "shorten the about section." The widget sends that prompt plus the current page's HTML to a Netlify Function called `edit.js`, which calls the Anthropic API using **Claude Haiku 4.5**, gets back modified HTML, and live-replaces the relevant section in the browser.

The edits are session-only — they don't persist to the file on the server. This is intentional. The widget is a sales tool: it lets the prospect feel like they have control before they've paid. Once they sign up, real edits become a paid workflow we handle on our side via the GitHub repo.

The widget is a self-contained `<script>` block at the bottom of each demo's `index.html`. It includes a button, a chat input, the prompt-handling JS, and a `fetch()` call to `/.netlify/functions/edit.js`. The function itself lives in the repo at `netlify/functions/edit.js` and uses an `ANTHROPIC_API_KEY` env var on Netlify. The function has rate limiting (10 edits/min/IP), prompt length caps (500 chars), HTML payload caps (50KB), and strips `<script>` tags from Claude's response before the demo replaces DOM. The model name is read from `ANTHROPIC_MODEL` env var so models can be swapped in Netlify without redeploying code.

Every demo also has a thin banner at the top of the page that lists what we improved. Something like:

> ✨ We rebuilt this site for [Business Name]. Improvements: 3.2x faster page load · proper SEO schema (JSON-LD) · mobile-optimized · 12 new conversion CTAs · Restaurant menu now in HTML (was a JPG image) · Full FAQ section with schema markup. Click any text to edit it live.

That banner is the prospect's first impression. It tells them concretely what changed and why it matters. Below the banner, the site is the site.

There's also a sticky bar at the bottom of the demo: *"Make this my real site — $99/month →"* linking to `tryrelaunch.com/onboard?prospect=[name]`. That's the conversion path. The onboarding form collects business info, captures payment via Stripe Checkout, and triggers the DNS handoff workflow.

## How the business is structured technically

One GitHub repo: **`tryrelaunch/relaunch`**. One Netlify account with multiple sites attached to that one repo. No CMS, no database, no framework, no build step. Pure static HTML, CSS, and one Netlify Function for the edit widget.

**The local dev folder on your machine:**

```
C:\Users\Nsini\Code\relaunch\relaunch-website\
```

(This was previously at `C:\Users\Nsini\Downloads\relaunch-website\` — moved into `Code\relaunch\` for a cleaner home for active projects. Anything referencing the old path is stale and should be updated.)

That folder is the entire business. Everything ships from there. Every demo, every paying client's site, the sales site itself, the onboarding form, the edit function — all of it.

**The repo structure:**

```
relaunch-website/
│
├── index.html                      ← tryrelaunch.com homepage (the sales site)
├── onboard.html                    ← /onboard signup form (Stripe Checkout pending)
│
├── previews/                       ← every prospect demo lives here
│   ├── valentines-deli/
│   │   └── index.html              ← tryrelaunch.com/previews/valentines-deli/
│   ├── spork/
│   │   ├── index.html              ← tryrelaunch.com/previews/spork/
│   │   └── images/                 ← 15 images (dishes, interior, cocktails, etc.)
│   ├── malarky/
│   │   └── index.html              ← tryrelaunch.com/previews/malarky/
│   └── [next-prospect]/
│       ├── index.html
│       └── images/
│
├── clients/                        ← paying clients' sites live here
│   └── spork/                      ← first paying client (graduated from preview)
│       ├── index.html              ← homepage
│       ├── images/                 ← all client photos (mirrored from preview)
│       └── edit/
│           └── index.html          ← internal edit interface (NOT the public widget)
│
├── netlify/
│   └── functions/
│       └── edit.js                 ← AI edit widget endpoint, calls Claude Haiku 4.5
│
├── netlify.toml                    ← Netlify build config
├── deploy.bat                      ← one-click deploy script for Windows
├── package.json / package-lock.json ← deps for the Netlify function (@anthropic-ai/sdk)
├── node_modules/                   ← gitignored; only present locally
│
├── CLAUDE.md                       ← THIS FILE — project brief for Claude Code
├── STATUS.md                       ← current project state / what's in flight
├── RUNBOOK.md                      ← ops procedures (deploy, DNS handoff, etc.)
├── CHANGELOG.md                    ← what's shipped, in reverse-chron
└── README.md
```

Every prospect demo is its own folder under `previews/`. The folder name becomes the URL slug — `previews/spork/` is served at `tryrelaunch.com/previews/spork/`. Self-contained. Its own HTML. Its own images. **No shared dependencies between prospects, so a change to one demo can never break another.**

Subpages are folders with their own `index.html`. Standard static-site convention. So `previews/spork/menu/index.html` would be served at `tryrelaunch.com/previews/spork/menu/`. Clean URLs, no `.html` extensions visible. Same for paying clients — a client's `/contact/` URL is served by `clients/[name]/contact/index.html`.

### Note: Spork currently exists in both `previews/` and `clients/`

Spork is the first paying client. The brief's stated lifecycle is "their site moves from `previews/[name]/` to `clients/[name]/`" — single location at a time. Right now, Spork sits in **both** locations because we haven't yet pruned the preview after conversion. Treat `clients/spork/` as the production source of truth; `previews/spork/` is legacy and can be deleted whenever convenient. New paying clients should follow the move-on-conversion pattern — don't duplicate.

## How Netlify is set up

One Netlify account. Multiple Netlify sites, all connected to the same GitHub repo. Each site has a different **base directory** setting that scopes it to one folder of the repo.

- **Site 1: tryrelaunch** — base directory is the repo root. Custom domain `tryrelaunch.com`. Serves the sales site, the onboarding form, all the prospect demos under `/previews/`.
- **Site N: any paying client** — base directory `clients/[name]/`. Custom domain `theirbusiness.com`. The `clients/[name]/` prefix is invisible to visitors — they see `theirbusiness.com/contact/`, which Netlify resolves to `clients/[name]/contact/index.html` in the repo.

Every site auto-deploys on every push to `main`. Push once, every changed site rebuilds simultaneously. Netlify is smart about it — only sites whose base directory has changed files actually rebuild, so you can push 50 demos without slowing anything down.

The Netlify Function (`netlify/functions/edit.js`) lives in the root and is shared across all sites — every demo can call `/.netlify/functions/edit.js` and hit the same endpoint. The function is wired to the prospect demos for now. **Paying clients won't have the public edit widget; their edits go through us.**

## How a new prospect demo ships, end-to-end

1. **Pick a prospect.** Restaurant, charter, salon, whatever. Doesn't matter — the workflow is identical.
2. **Recon their existing site.** Pull their current HTML, photos, menu, hours, reviews, schema. Identify the gaps: bad mobile, JPG menu, missing schema, slow load, weak SEO, ugly hero, no CTAs.
3. **Build the demo in a Claude chat.** Write `previews/[name]/index.html` and resize/rename their photos into `previews/[name]/images/`. The build matches their brand colors, uses their actual content, includes the SEO improvements banner at top, the edit widget at bottom-right, and the "Make this my real site" sticky bar.
4. **Drop it in.** Unzip into `C:\Users\Nsini\Code\relaunch\relaunch-website\previews\[name]\`.
5. **Deploy.** Open Command Prompt or PowerShell in the repo folder and run `deploy.bat`. The script does:
   ```
   git add .
   git commit -m "[message]"
   git push origin main
   ```
6. **Netlify auto-builds and deploys.** About 60 seconds later, `tryrelaunch.com/previews/[name]/` is live.
7. **Send the cold email.** It contains exactly one link: that demo URL.
8. **Prospect clicks.** Sees the rebuilt site. Maybe plays with the edit widget. Maybe clicks "Make this my real site." If they do, they're in the Stripe Checkout flow on `/onboard`.
9. **If they convert,** move their demo from `previews/[name]/` to `clients/[name]/`, set up a new Netlify site pointed at that folder, take ownership of their domain DNS, and they're live on the new site within hours.
10. **If they don't convert,** the demo stays up for a month, then we either remove it or repurpose it.

Volume target: dozens of demos per week. The whole point of the static-file architecture is that there's no per-prospect overhead. Every demo is a folder. Every folder is independent. Every push deploys instantly.

## How a paying client is structured differently from a prospect demo

When a prospect converts, their site graduates from `previews/[name]/` to `clients/[name]/`. Same repo, but the structure changes:

- **No edit widget.** Production sites don't have a public AI editor. Edits go through us, via Claude in chat, into the repo. (An internal `clients/[name]/edit/` page may exist for staff use — not exposed to the public.)
- **No "Make this my real site" sticky bar.** It's already their real site.
- **No SEO improvements banner at the top.** The improvements are baked in invisibly.
- **Multiple subpages.** Real sites have real navigation. `/menu/`, `/about/`, `/contact/`, `/gallery/`, etc. Each is its own folder with `index.html`.
- **Real domain on Netlify.** `theirbusiness.com`, not a subfolder of `tryrelaunch.com`.
- **Schema markup is comprehensive.** LocalBusiness, Product, FAQPage, VideoObject — whatever applies. Search rankings depend on it.
- **Surgical SEO preservation.** When migrating from an existing site, preserve every URL Google has indexed. Even ugly URLs stay if they're ranking. Backlinks still work. Search console history doesn't reset.

This is the pattern for every paying client. Restaurant with a homepage, menu, about, contact, gallery — that's 5 folders, 5 `index.html` files, one shared `styles.css`, one shared `images/` folder. Every page links absolutely (`/styles.css`, `/menu/`, `/images/hero.jpg`) so paths never break.

## How `deploy.bat` works

Single Windows batch file at the repo root. Double-click it, or run from Command Prompt / PowerShell:

```bat
@echo off
cd /d "C:\Users\Nsini\Code\relaunch\relaunch-website"
git add .
git commit -m "deploy %date% %time%"
git push origin main
echo Pushed. Netlify will deploy in ~60 seconds.
pause
```

(The actual `deploy.bat` in the repo is slightly fancier — it prompts for a commit message and does empty-commit detection — but the cd/add/commit/push core is the same.)

That's the entire deploy pipeline. No CI server, no build minutes to manage, no SSH keys, no FTP, no hosting control panel. **Files → git → live.**

## DNS handoff for paying clients

When a customer signs up:

1. Their site moves from `previews/[name]/` to `clients/[name]/` in the repo.
2. New Netlify site created, base directory pointed at the new folder.
3. The temporary `clients-[name].netlify.app` URL gets tested — every page loads, every link works, every image renders, schema validates, mobile is clean.
4. Add their custom domain (`theirbusiness.com`) to the Netlify site. Netlify gives you DNS records.
5. Customer's domain is at GoDaddy / Namecheap / Squarespace Domains / wherever. Update the A record and CNAME to Netlify's load balancer.
6. DNS propagates — typically 15 min to a few hours.
7. Their old hosting can stay paid for a couple weeks as a safety net, then cancel.

## Where this is going

The thesis is **volume**. The architecture is built so we can ship 10–50 prospect demos per week. Each demo costs essentially nothing to host (Netlify free tier covers it, the AI edit widget runs on cheap Haiku tokens). Conversion rate doesn't need to be high — even at 2–3%, the math works because the cost per demo is near zero and the recurring revenue per conversion is meaningful.

Every paying client gets the same folder pattern, same shared deployment, same one-button workflow. As clients scale from 1 to 10 to 100, nothing about the system changes. You don't outgrow this stack — it's specifically designed to keep working at every volume because there's no shared state, no database to migrate, no framework to upgrade.

That's Relaunch.

---

## Operating notes for Claude Code

- **Repo root for all work in this project:** `C:\Users\Nsini\Code\relaunch\relaunch-website\`
- **Every prospect demo is a self-contained folder** under `previews/`. Don't share assets between prospects.
- **Every paying client is a self-contained folder** under `clients/`. Use absolute paths inside their site (`/styles.css`, `/menu/`, etc.) so the Netlify base-directory setup serves them at the root of their custom domain.
- **The edit widget (`netlify/functions/edit.js`) is shared** by all preview sites. Don't duplicate per-prospect.
- **Companion docs in the repo root:** `STATUS.md` (what's currently in flight), `RUNBOOK.md` (ops procedures), `CHANGELOG.md` (shipped work). Skim these before starting non-trivial changes.
- **Push hygiene:** use `deploy.bat` for a guided commit, or run `git add . && git commit -m "..." && git push origin main` directly. Netlify deploys on every push to `main`.
- **GitHub remote:** `https://github.com/tryrelaunch/relaunch.git`. If git auth fails on push, the cached credential is probably for a different account — clear `git:https://github.com` from Windows Credential Manager and re-auth.
- **Don't commit `node_modules/`** — already gitignored. The Netlify function pulls deps at build time.
