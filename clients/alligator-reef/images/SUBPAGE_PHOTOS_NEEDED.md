# Photo request — three new subpages

Three new SEO pages were built for the live site on 2026-05-23 to target high-volume Florida Keys queries that the homepage alone can't capture:

- `/alligator-reef-lighthouse/` — targets "alligator reef lighthouse" (1,900 searches/mo, KD 9)
- `/islamorada-sandbar/` — targets "islamorada sandbar" (800 searches/mo, KD 2)
- `/sunset-cruise/` — targets "islamorada sunset cruise" (150 searches/mo, KD 2)

Each page currently uses one existing photo (`lighthouse.jpg`, `sandbar.jpg`, `sunset.jpg`) as both hero and inline banner. They look fine, but each page would carry more weight with 2–3 additional real shots from the actual trips. **Real photos only — no stock, no AI-generated images.** Mitch's actual boats, dock, and water.

## How to deliver

Save each photo to `clients/alligator-reef/images/` using the exact filenames below. The HTML is wired to pick them up automatically. Recommended export: JPEG quality 78–82, max 1800px on the long edge.

---

## Lighthouse page — `/alligator-reef-lighthouse/`

| Filename | What to capture |
|---|---|
| `lighthouse-detail.jpg` | Close-up of the iron lighthouse structure, ideally showing the screw-pile design and the rust patina. Shot from a boat at one of the mooring buoys. 1200×900. |
| `lighthouse-snorkel.jpg` | Underwater or surface shot near the lighthouse: fish, coral, or a snorkeler in the water with the lighthouse visible above the surface. 1200×900. |
| `lighthouse-approach.jpg` | A rental boat approaching the lighthouse, lighthouse fills 1/3 of the frame, turquoise water dominant. 1600×900. |

Optional but valuable: a wide shot from outside the sanctuary buoys showing the lighthouse with multiple rental boats moored around it on a calm day.

---

## Sandbar page — `/islamorada-sandbar/`

| Filename | What to capture |
|---|---|
| `sandbar-lowtide.jpg` | The firm sandbar exposed at low tide, with people standing in ankle-to-knee-deep water. Shows scale of the flat. 1600×900. |
| `sandbar-weekday.jpg` | Quiet weekday vibe: one or two boats anchored, family or small group, kids splashing or floats out. 1200×900. |
| `sandbar-weekend.jpg` | Saturday party vibe: multiple boats anchored stem-to-stern, people in the water, music/cooler scene (no faces if you don't have releases — wide shot or backs of heads is fine). 1600×900. |

Optional: a shot of the channel/cut going through to the sandbar, with one of the rental boats heading out.

---

## Sunset cruise page — `/sunset-cruise/`

| Filename | What to capture |
|---|---|
| `sunset-onboard.jpg` | Passenger POV looking forward over the bow into the sunset. Bow rail or boat detail in foreground, sky and water filling the frame. 1600×900. |
| `sunset-guests.jpg` | People on the deck during golden hour, front-lit by the sunset. Smiling, drink in hand, real-looking — no staged corporate shot. Backs of heads or candid profiles work fine. 1200×900. |
| `sunset-dock.jpg` | The boat tied at Breezy Palms dock in evening light, the sky going pink or purple behind it. 1600×900. |

Optional: a "BYOB welcome" shot — a cooler with ice and bottles on the deck, sunset behind. Lifestyle, not staged.

---

## What we already have (don't re-shoot)

- `hero.jpg` — boat in turquoise water (homepage hero)
- `lighthouse.jpg` — wide banner of the lighthouse with boats (already used as hero on the lighthouse page)
- `sandbar.jpg` — wide banner of boats clustered at the sandbar (already on sandbar page)
- `sunset.jpg` — aerial Breezy Palms sunset (already on sunset page)
- `owners.jpg`, `guest-1.jpg` through `guest-4.jpg` — homepage shots

The "Optional" photos at the bottom of each section are nice-to-haves. The three core shots per page are what would move the needle most.

## After dropping files

```
cd C:\Users\Nsini\Code\relaunch\relaunch-website
git add clients/alligator-reef/images/
git commit -m "Alligator Reef: add subpage photos"
git push origin main
```

Netlify rebuilds in ~60s and the pages pick up the new images automatically — the `<img src>` paths are already in place.
