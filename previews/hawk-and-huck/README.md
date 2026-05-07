# Hawk & Huck — Relaunch Preview Build

## What's in this preview

Four pages, single shared CSS, premium "Refined Modern Cowboy" design language. Designed to wow Jayme and look credible enough to bring to Brian & James.

```
hawk-and-huck/
├── index.html              Homepage — celebrity chef + Tumalo + canvas tent angle
├── menu.html               Real text menu (vs their JPG-only menu — the tactical win)
├── private-events.html     4 spaces detailed: La Pine Tent, Huckleberry Lounge, Sisters DR, Buyout
├── our-story.html          Malarkey brothers narrative + ranch-to-plate ethos
├── css/main.css            Full design system, mobile-first responsive
└── js/main.js              Mobile menu toggle
```

## Personal touches

- **Preview banner** at the top of every page: *"Hey Jayme — sketch by Boatr Marketing for Hawk & Huck. Click around, then let's grab a drink."* with a reply mailto link.
- **Footer credit**: "Sketch by Relaunch" linking to tryrelaunch.com — soft conversion signal.
- **Menu page note**: A clear callout to Jayme explaining that the menu items shown are placeholder content, and the structural difference (text vs JPG) is the real win. Frames the preview honestly.

## The pitch baked in

**For Brian/James (brand level):**
- Homepage leads with celebrity chef + Tumalo ranch + canvas tent dining, all above the fold (vs. their current homepage which is just a logo PNG)
- "A few of our favorites" section spotlights the 32oz Tomahawk, Huckleberry Old Fashioned, and Bone Marrow — clear hero items with proper photography slots

**For Jayme (operational level):**
- Real text menu = no more Squarespace JPG uploads when prices change
- Private events page converts inquiries via the existing Toast Tab flow
- OpenTable reservation CTA in nav, hero, and visit section
- Mobile-first responsive (Squarespace mobile is template-y)
- Schema.org Restaurant markup on homepage = better Google rich results
- Live music Friday + Happy Hour both surfaced in the top strip on every page

## SEO upside (for the cold email)

Their Ahrefs data showed:
- **DR 24, +150 organic traffic** in the last 6 months — recovery happening
- **But 23% of pages are 404s** — major technical issue
- **Lost 52 keywords** in the same period (from 71 to 19)
- **Invisible for "best restaurants in bend oregon"** (1.1K vol) — bendblacksmith.com sits at #7
- **Invisible for "restaurants bend oregon"** (1.5K vol) — same competitor at #8
- **0 AI citations outside Google's AI Overview** — invisible to ChatGPT/Perplexity/Gemini

The redesign solves all of these:
- Structured text replaces JPG menus → indexable
- Schema markup → AI-search visible
- Clean URL structure → no 404s
- Local SEO content (Bend, Tumalo, steakhouse) baked in
- Real meta descriptions per page

## Deploy

Drop this folder into `Code\relaunch\relaunch-website\previews\hawk-and-huck\`.

```
git add previews/hawk-and-huck
git commit -m "Add Hawk & Huck preview build"
git push origin main
```

Netlify auto-deploys. Preview lives at:
`https://tryrelaunch.com/previews/hawk-and-huck/`

## To verify before sending to Jayme

1. Click through all 4 pages on desktop — design system consistent, navigation works
2. Resize browser to mobile width (~375px) — hamburger menu opens, layouts collapse cleanly
3. Confirm OpenTable link (`https://www.opentable.com/r/hawkeye-and-huckleberry-lounge-bend`) — I guessed at the slug, may need to update
4. Confirm Toast Tab inquiry link — that's their actual link from the current site
5. Replace `nate@boatrmarketing.com` in the preview banner reply link if you want a different contact email

## What's intentionally NOT here

- **Reservations page** — using OpenTable link instead. Standard for a steakhouse.
- **Contact page** — info is on homepage in the Visit section. One less page to maintain.
- **Mother's Day / Easter / event pages** — those are time-sensitive and would be added during onboarding.
- **Gift cards page** — link in footer, but no dedicated page since they sell via Squarespace cart currently.
- **Real menu content** — clearly noted as placeholder. Real menu transcribes from their PDFs in 30 minutes during onboarding.

## Suggested cold email line for Jayme

> "Yo Jayme — built H&H a sketch over the weekend. The current site has 6 broken pages and Google can't read your menu (it's all JPGs). Loop on this with me when you have 5 min: tryrelaunch.com/previews/hawk-and-huck/. Could replace your Squarespace in a week."

(Tweak as needed — but the "Google can't read your menu" line is the hook.)
