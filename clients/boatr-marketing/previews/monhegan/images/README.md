# Alligator Reef preview — image drop-in list

Save the source photos from the chat into this folder with the exact filenames below. The HTML is wired to expect them.

## Required files (site won't look right without these)

| Filename | Which photo from the batch you sent |
|---|---|
| `logo.png` | The circular **Alligator Reef Boat Rentals logo** with the lighthouse + palm trees + boat illustration. Save as transparent-bg PNG if possible. |
| `hero.jpg` | The **white rental boat in turquoise water with the Alligator Reef logo decal visible on the hull**. This is the strongest hero — shows the brand, the boat, and the destination water in one frame. Recommended export: 1800px wide, JPEG quality 80. |
| `owners.jpg` | **Mitchell + Michael standing between two boats at the dock**, both wearing the light-blue Alligator Reef polo shirts. This is the "new ownership" image inside the About card. Recommended: 1200×675 (16:9). |
| `lighthouse.jpg` | The **Alligator Reef Lighthouse with boats + people around it**, turquoise water, the rusty iron lighthouse structure. Goes in the Alligator Reef section. Recommended: 1600×600 (wide banner aspect). |
| `sandbar.jpg` | The **clustered-boats sandbar shot with people swimming**, crystal turquoise water. Goes in the Islamorada Sandbar section. Recommended: 1600×600. |
| `sunset.jpg` | The **aerial Breezy Palms sunset shot** with the palm trees + pink/purple sky over the resort. Goes in the Sunset Cruise section. Recommended: 1600×600. |

## Guest gallery (4 photos — social proof, near the booking CTA)

| Filename | Which photo |
|---|---|
| `guest-1.jpg` | The **couple selfie at the sandbar with the rental boat behind them** in shallow turquoise water. |
| `guest-2.jpg` | The **family on the boat with the barracudas** at the dock. |
| `guest-3.jpg` | The **two young anglers with their catch** on the dock — bonus, the Alligator Reef sign is visible behind them. |
| `guest-4.jpg` | The **three-person selfie on the boat** — sun behind, blue water. |

Recommended export for guests: 800×1066 (3:4 portrait), JPEG quality 78.

## Anything else?

Skipped from the batch:
- The two **dog photos** — cute but not on-brand for a booking page. Save somewhere else if you ever do a "Pets welcome" page.
- The **catering snack cups** — looks like Mitch's wife's catering side. Doesn't fit the rental site. Could be its own section later if they want.
- The **other lone-boat shots** (Deep Impact, Honda outboard 200) — not in the rental fleet based on the Peek widget. Skip unless Mitch confirms ownership.

## After dropping files

Just commit and push:

```
cd C:\Users\Nsini\Code\relaunch\relaunch-website
git add clients/boatr-marketing/previews/alligator-reef/images/
git commit -m "Add real Alligator Reef photos to preview"
git push origin main
```

Netlify rebuilds in ~60s and the preview gets the real photos. URL stays the same: `https://boatrmarketing.com/previews/alligator-reef/`
