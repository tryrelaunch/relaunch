#!/usr/bin/env python3
"""
Fay's Diner & Cafe - preview builder.

Reads:
  _build/template.html  - page skeleton with {{TOKENS}}
  _build/banner.html    - Relaunch SEO banner (inline)
  _build/widget.html    - Relaunch edit widget (inline)
  _build/menu.json      - real menu scraped from faysdiner.com (125 items)

Emits to previews/fays-diner/:
  index.html . menu.html . hours.html . reservations.html . contact.html

Pattern mirrors previews/ch-steak-lounge/_build/build.py.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "_build"
OUT = ROOT

# ------------------------------------------------------------------------------
# Sitewide facts (verified from prospect_faysdiner.md + live scrape 2026-06-08)
# ------------------------------------------------------------------------------

BUSINESS = {
    "name": "Fay's Diner & Cafe",
    "url": "https://faysdiner.com",
    "phone": "+1-858-397-2530",
    "phone_display": "(858) 397-2530",
    "phone_tel": "+18583972530",
    "street": "10006 Scripps Ranch Boulevard",
    "city": "San Diego",
    "region": "CA",
    "postal": "92131",
    "country": "US",
    # APPROXIMATE coordinates for 10006 Scripps Ranch Blvd - confirm against the
    # Google Business Profile pin before publishing (live site renders its map via
    # JS, so exact lat/lng was not in the page source).
    "lat": 32.90981,
    "lng": -117.09972,
    "price_range": "$$",
    "cuisine": ["American", "Breakfast", "Cafe", "Californian"],
    "facebook": "https://www.facebook.com/112806368390004",
    "instagram": "https://www.instagram.com/faysdiner",
    "yelp": "https://www.yelp.com/biz/fays-diner-and-cafe-san-diego",
}

# Map embed (keyless query embed - no API key needed)
MAP_EMBED = ("https://www.google.com/maps?q=10006+Scripps+Ranch+Blvd,"
             "+San+Diego,+CA+92131&output=embed")

# Order meals appear on the menu page
MEAL_ORDER = ["Breakfast", "Kids", "Lunch", "Dinner"]
MEAL_BLURB = {
    "Breakfast": "Served all day, every day from 6:30 AM. The reason most people come back.",
    "Kids": "Smaller plates for smaller appetites - each served with a side.",
    "Lunch": "Sandwiches, salads, burgers, and plates - served daily alongside breakfast.",
    "Dinner": "A full sit-down dinner menu, Wednesday through Saturday, 4 PM to 8 PM.",
}

# ------------------------------------------------------------------------------
# Menu - loaded from the real scrape (menu.json)
# ------------------------------------------------------------------------------

MENU = json.loads((BUILD / "menu.json").read_text(encoding="utf-8"))


def _clean_name(raw):
    """Strip (V)/(GF)/(VG) markers from a display name; return (name, flag)."""
    flag = None
    m = re.search(r"\((V|VG|GF|VEG)\)\s*$", raw, re.I)
    if m:
        token = m.group(1).upper()
        flag = "GF" if token == "GF" else "V"
        raw = raw[:m.start()].strip()
    return raw, flag


def _price_to_number(item):
    """Best-effort numeric price for schema. Checks price field then description."""
    for src in (item.get("price", ""), item.get("desc", "")):
        m = re.search(r"\$(\d+(?:\.\d+)?)", src or "")
        if m:
            return float(m.group(1))
    return None


# ------------------------------------------------------------------------------
# Schema builders
# ------------------------------------------------------------------------------

def restaurant_schema():
    """Full Restaurant + LocalBusiness markup - referenced from multiple pages."""
    sections_schema = []
    for sec in MENU:
        items = []
        for item in sec["items"]:
            name, _flag = _clean_name(item["name"])
            offer = {}
            price = _price_to_number(item)
            if price is not None:
                offer = {"offers": {"@type": "Offer", "price": price, "priceCurrency": "USD"}}
            entry = {"@type": "MenuItem", "name": name}
            if item.get("desc"):
                entry["description"] = item["desc"]
            entry.update(offer)
            items.append(entry)
        sections_schema.append({
            "@type": "MenuSection",
            "name": f'{sec["meal"]} - {sec["section"]}',
            "hasMenuItem": items,
        })

    return {
        "@context": "https://schema.org",
        "@type": ["Restaurant", "LocalBusiness"],
        "@id": f"{BUSINESS['url']}/#restaurant",
        "name": BUSINESS["name"],
        "url": BUSINESS["url"],
        "telephone": BUSINESS["phone"],
        "priceRange": BUSINESS["price_range"],
        "servesCuisine": BUSINESS["cuisine"],
        "image": f"{BUSINESS['url']}/assets/images/og-hero.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BUSINESS["street"],
            "addressLocality": BUSINESS["city"],
            "addressRegion": BUSINESS["region"],
            "postalCode": BUSINESS["postal"],
            "addressCountry": BUSINESS["country"],
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": BUSINESS["lat"],
            "longitude": BUSINESS["lng"],
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Sunday", "Monday", "Tuesday"],
                "opens": "06:30",
                "closes": "15:00",
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "06:30",
                "closes": "15:00",
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "16:00",
                "closes": "20:00",
            },
        ],
        "sameAs": [BUSINESS["facebook"], BUSINESS["instagram"], BUSINESS["yelp"]],
        "hasMenu": {
            "@type": "Menu",
            "name": "Fay's Diner & Cafe Menu",
            "hasMenuSection": sections_schema,
        },
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "All-day breakfast", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Dinner service (Wed-Sat)", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Kids menu", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Vegetarian options", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Gluten-free options", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Takeout", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Private parties / catering", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Wheelchair accessible", "value": True},
        ],
        # NOTE: AggregateRating intentionally NOT stubbed - connect real Google/Yelp
        # reviews before publishing. Fake stars poison both AI search and trust.
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": f"{BUSINESS['url']}/{path}" if path else BUSINESS["url"],
            }
            for i, (name, path) in enumerate(items)
        ],
    }


def faq_schema(qa_pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa_pairs
        ],
    }


# ------------------------------------------------------------------------------
# Breadcrumb HTML helper
# ------------------------------------------------------------------------------
def breadcrumb_html(items):
    parts = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1 or path is None:
            parts.append(f'<span aria-current="page">{name}</span>')
        else:
            parts.append(f'<a href="{path}">{name}</a>')
    inner = '<span class="sep">&rsaquo;</span>'.join(parts)
    return f'<div class="breadcrumb"><div class="container">{inner}</div></div>'


# ------------------------------------------------------------------------------
# Sitewide FAQ pool (>=25 questions sitewide for AI-search citation)
# ------------------------------------------------------------------------------
FAQS = {
    "index": [
        ("Where is Fay's Diner & Cafe?",
         "Fay's Diner & Cafe is at 10006 Scripps Ranch Boulevard in San Diego, CA 92131, in the Scripps Ranch neighborhood."),
        ("What are Fay's Diner's hours?",
         "Fay's serves breakfast and lunch every day from 6:30 AM to 3:00 PM. Dinner is served Wednesday through Saturday from 4:00 PM to 8:00 PM."),
        ("Does Fay's serve breakfast all day?",
         "Yes - the full breakfast menu is available every day we're open, from 6:30 AM until we close. You can order French toast or a Benedict at lunchtime."),
        ("What kind of food does Fay's Diner serve?",
         "Fay's is an all-day California cafe: classic and upscale breakfast (Benedicts, omelettes, French toast, burritos), lunch (salads, sandwiches, burgers), and a full dinner menu Wednesday through Saturday with entrees like Steak Frites, Chicken Piccata, and Filet Oscar."),
        ("Does Fay's take reservations?",
         "Yes. You can request a table through our Reservations page or call (858) 397-2530. Walk-ins are always welcome, especially for breakfast."),
    ],
    "menu": [
        ("What's popular for breakfast at Fay's?",
         "Guest favorites include the Berries and Cream French Toast, the Crab Cake Benedict, Santa Fe Hash, the Cali Breakfast Burrito, and Steak & Eggs. The house-made cinnamon rolls sell out."),
        ("Does Fay's have vegetarian and gluten-free options?",
         "Yes. Many dishes are marked vegetarian (V) on the menu - like the Veggie Omelette, Florentine Benedict, and Avocado Toast - and several are gluten-free (GF), such as the Chile Verde and the Blackened Salmon and Veggies. Ask your server for the full list."),
        ("What's on the dinner menu at Fay's?",
         "Dinner (Wednesday through Saturday) includes starters and small plates, plus entrees like Chicken Piccata, Shrimp Scampi, Steak Frites, Chicken Pot Pie, Beef Bourguignon Pasta, and chef's specials like Filet Oscar and Pan Seared Halibut."),
        ("Is there a kids' menu?",
         "Yes - the kids' menu includes a Mickey Mouse Pancake, grilled cheese, chicken tenders, a kids' burger, French toast, and spaghetti, each served with a side."),
        ("Does Fay's have dessert?",
         "Yes - house-made cinnamon rolls, an ice cream sundae, the Fay's Banana Split, milkshakes, floats, and a Mixed Berry New York Cheesecake."),
    ],
    "hours": [
        ("What time does Fay's open?",
         "Fay's opens at 6:30 AM every day for breakfast and lunch."),
        ("What days does Fay's serve dinner?",
         "Dinner is served Wednesday, Thursday, Friday, and Saturday from 4:00 PM to 8:00 PM. Sunday, Monday, and Tuesday we close at 3:00 PM after lunch."),
        ("Is Fay's open on Sunday?",
         "Yes - Fay's is open Sunday from 6:30 AM to 3:00 PM for breakfast and lunch. There is no dinner service on Sunday."),
        ("Where is Fay's located and is there parking?",
         "Fay's is at 10006 Scripps Ranch Boulevard, San Diego, CA 92131, with parking available in the shopping center lot."),
        ("Does Fay's do takeout?",
         "Yes - call (858) 397-2530 to place a takeout order during open hours."),
    ],
    "reservations": [
        ("Can I make a reservation at Fay's Diner?",
         "Yes - request a table through the Reservations page or call (858) 397-2530. Reservations are especially helpful for dinner (Wed-Sat) and weekend breakfast."),
        ("Does Fay's host private parties?",
         "Yes. Fay's hosts birthday breakfasts, family gatherings, showers, and small private events. Tell us your date, party size, and what you're planning and we'll put together a plan."),
        ("Do I need a reservation for breakfast?",
         "Not usually - breakfast is mostly walk-in. On busy weekend mornings a reservation can cut your wait, and large groups should always call ahead."),
        ("Can Fay's accommodate a large group?",
         "Yes - for parties of 8 or more, please call (858) 397-2530 so we can set up the right tables and, if you'd like, a simplified group menu."),
        ("Does Fay's cater?",
         "We can put together trays and group orders for events. Call (858) 397-2530 or use the contact form with your date, headcount, and what you have in mind."),
    ],
    "contact": [
        ("What's the phone number for Fay's Diner?",
         "Fay's Diner & Cafe can be reached at (858) 397-2530."),
        ("What's the address for Fay's Diner & Cafe?",
         "Fay's is at 10006 Scripps Ranch Boulevard, San Diego, CA 92131."),
        ("How do I get to Fay's in Scripps Ranch?",
         "Fay's is on Scripps Ranch Boulevard in the Scripps Ranch neighborhood of San Diego, just off I-15. Use the Get Directions link to open it in Google Maps."),
        ("Is Fay's on social media?",
         "Yes - find Fay's on Facebook, Instagram (@faysdiner), and Yelp. Links are on the Contact page."),
        ("Is Fay's wheelchair accessible?",
         "Yes, the entrance and dining room are wheelchair accessible. If you have specific seating needs, let us know when you book."),
    ],
}


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def render_faq_section(page_key):
    rows = ""
    for q, a in FAQS[page_key]:
        rows += f'''
        <div class="faq-item">
          <p class="faq-q">{q}</p>
          <p class="faq-a">{a}</p>
        </div>'''
    return f'''
    <section class="section alt">
      <div class="container">
        <span class="eyebrow">Frequently asked</span>
        <h2>Questions guests ask us</h2>
        <div style="max-width: 820px;">
          {rows}
        </div>
      </div>
    </section>'''


def _flag_html(flag):
    if not flag:
        return ""
    cls = "gf" if flag == "GF" else "veg"
    return f' <span class="menu-item-flag {cls}">{flag}</span>'


def render_full_menu_html():
    """Render the entire menu grouped by meal -> section -> items."""
    out = ""
    current_meal = None
    s_idx = 0
    for sec in MENU:
        meal = sec["meal"]
        if meal != current_meal:
            if current_meal is not None:
                out += "\n    </div>"  # close previous meal wrapper
            current_meal = meal
            out += f'''
    <div class="menu-meal">
      <div class="menu-meal-head">
        <h2>{meal}</h2>
        <p>{MEAL_BLURB.get(meal, "")}</p>
      </div>'''
        items_html = ""
        for i_idx, item in enumerate(sec["items"]):
            name, flag = _clean_name(item["name"])
            price = item.get("price", "").strip()
            price_html = f'<span class="menu-item-price" id="edit-menu-{s_idx}-{i_idx}-price">{price}</span>' if price else ""
            desc = item.get("desc", "").strip()
            desc_html = f'<p class="menu-item-desc" id="edit-menu-{s_idx}-{i_idx}-desc">{desc}</p>' if desc else ""
            items_html += f'''
            <div class="menu-item-row">
              <div class="menu-item-top">
                <h4 class="menu-item-name" id="edit-menu-{s_idx}-{i_idx}-name">{name}{_flag_html(flag)}</h4>
                {price_html}
              </div>
              {desc_html}
            </div>'''
        out += f'''
      <div class="menu-section">
        <div class="menu-section-head">
          <h3 id="edit-menu-{s_idx}-section">{sec["section"]}</h3>
        </div>
        <div class="menu-grid">
          {items_html}
        </div>
      </div>'''
        s_idx += 1
    out += "\n    </div>"  # close last meal wrapper
    return out


# ------------------------------------------------------------------------------
# Page main-content generators
# ------------------------------------------------------------------------------

def main_index():
    return '''
<section class="hero">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline" id="edit-hero-tagline">Scripps Ranch &middot; San Diego</span>
    <h1>
      <span id="edit-hero-h1-main">All-day breakfast.</span>
      <span class="accent" id="edit-hero-h1-accent">Real dinner on the weekend.</span>
    </h1>
    <p class="hero-lede" id="edit-hero-lede">A bright neighborhood cafe in Scripps Ranch. Benedicts, French toast, omelettes, and burritos from 6:30 AM every day &mdash; plus a full sit-down dinner menu Wednesday through Saturday.</p>
    <div class="hero-ctas">
      <a href="menu.html" class="btn btn-primary">See the Menu</a>
      <a href="reservations.html" class="btn btn-ghost">Reserve a Table</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="stats">
      <div class="stat"><div class="stat-num">6:30a</div><div class="stat-label">Open Daily</div></div>
      <div class="stat"><div class="stat-num">All Day</div><div class="stat-label">Breakfast</div></div>
      <div class="stat"><div class="stat-num">Wed&ndash;Sat</div><div class="stat-label">Dinner Service</div></div>
      <div class="stat"><div class="stat-num">100+</div><div class="stat-label">Dishes Made Fresh</div></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid grid-2" style="align-items: center;">
      <div>
        <span class="eyebrow">About Fay's</span>
        <h2 id="edit-mission-h2">Classic diner comfort, cooked like someone cares.</h2>
        <p id="edit-mission-p1">Fay's Diner & Cafe is a family-run, all-day cafe in the heart of Scripps Ranch. We do breakfast the way it should be done &mdash; from Berries and Cream French Toast and house-made cinnamon rolls to Crab Cake Benedicts and a Cali Breakfast Burrito the size of your forearm &mdash; and we serve it every day we're open, all day long.</p>
        <p id="edit-mission-p2">Wednesday through Saturday evenings we turn into a proper little dinner spot, with Steak Frites, Chicken Piccata, fresh seafood, and a few chef's specials. Same friendly room, same fair prices, just with the lights turned down a notch.</p>
        <a href="menu.html" class="btn btn-teal">See the Full Menu</a>
      </div>
      <div>
        <div style="aspect-ratio: 4 / 5; background: linear-gradient(160deg, var(--fd-teal) 0%, var(--fd-teal-3) 55%, var(--fd-slate) 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: var(--fd-shadow); position: relative; overflow: hidden;">
          <div style="text-align: center; color: var(--fd-cream); padding: 32px;">
            <div style="font-family: var(--font-display); font-size: 4rem; font-weight: 700; color: var(--fd-sun); line-height: 1; margin-bottom: 16px;">Fay's</div>
            <div style="font-family: var(--font-display); font-size: 1.5rem; font-weight: 600; margin-bottom: 6px;">Diner &amp; Cafe</div>
            <div style="font-size: 0.8rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--fd-sun-2);">Scripps Ranch &middot; San Diego</div>
            <div style="margin-top: 32px; font-style: italic; color: rgba(251,244,230,0.7); font-size: 0.9rem;">Real photo will go here &mdash; owner to provide an interior or food shot</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">A few favorites</span>
    <h2>What people order again</h2>
    <p class="section-lede">A taste of the menu. The full breakfast, lunch, and dinner lineup lives on the <a href="menu.html">Menu page</a>.</p>

    <div class="menu-section">
      <div class="menu-grid">

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-frenchtoast-name">Berries &amp; Cream French Toast <span class="menu-item-flag veg">V</span></h3>
            <span class="menu-item-price" id="edit-feat-frenchtoast-price">$20.00</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-frenchtoast-desc">Brioche bread, berry compote, cream anglaise, maple bourbon syrup, and fresh strawberries.</p>
        </div>

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-crabbenedict-name">Crab Cake Benedict</h3>
            <span class="menu-item-price" id="edit-feat-crabbenedict-price">$25.00</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-crabbenedict-desc">Two house-made lump crab cakes, avocado, arugula, poached eggs, and hollandaise.</p>
        </div>

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-steakeggs-name">Steak &amp; Eggs</h3>
            <span class="menu-item-price" id="edit-feat-steakeggs-price">$31.00</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-steakeggs-desc">8 oz New York steak smothered in house-made hollandaise, with two eggs any style.</p>
        </div>

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-filetoscar-name">Filet Oscar <span class="menu-item-flag gf">Dinner</span></h3>
            <span class="menu-item-price" id="edit-feat-filetoscar-price">$45.00</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-filetoscar-desc">Filet mignon topped with jumbo crab meat and Bearnaise sauce. A Wed&ndash;Sat dinner special.</p>
        </div>

      </div>
    </div>

    <div style="text-align: center; margin-top: 24px;">
      <a href="menu.html" class="btn btn-teal">See the full menu &rarr;</a>
    </div>
  </div>
</section>

<section class="section teal">
  <div class="container">
    <div class="grid grid-3">
      <a href="menu.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">B</span>
        <h3 id="edit-svc-breakfast-title">All-Day Breakfast</h3>
        <p id="edit-svc-breakfast-desc">Benedicts, omelettes, French toast, burritos, hashes, and house-made cinnamon rolls &mdash; from 6:30 AM, all day.</p>
      </a>
      <a href="menu.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">D</span>
        <h3 id="edit-svc-dinner-title">Dinner, Wed&ndash;Sat</h3>
        <p id="edit-svc-dinner-desc">Steak Frites, Chicken Piccata, fresh seafood, and chef's specials, 4 PM to 8 PM Wednesday through Saturday.</p>
      </a>
      <a href="reservations.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">P</span>
        <h3 id="edit-svc-parties-title">Reservations &amp; Parties</h3>
        <p id="edit-svc-parties-desc">Reserve a table, plan a birthday breakfast, or book the room for a small private gathering.</p>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="quote">
      <span id="edit-quote-text">The kind of neighborhood breakfast spot you wish was on your corner &mdash; generous plates, real cooking, and people who remember your order.</span>
      <span class="quote-attr" id="edit-quote-attr">Placeholder &mdash; replace with a real Google or Yelp review once reviews are connected</span>
    </div>
  </div>
</section>
''' + render_faq_section("index")


def main_menu():
    return f'''
<section class="hero" style="min-height: 360px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">The Menu</span>
    <h1>
      <span id="edit-menu-h1-main">Breakfast, lunch,</span>
      <span class="accent" id="edit-menu-h1-accent">and weekend dinner.</span>
    </h1>
    <p class="hero-lede" id="edit-menu-lede">Everything made fresh in house. Breakfast and lunch served daily from 6:30 AM; the full dinner menu Wednesday through Saturday, 4 to 8 PM.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Menu</span>
    <h2>Everything we make</h2>
    <p class="section-lede">Prices and availability can change with the season. For the freshest version, call <a href="tel:+18583972530">(858) 397-2530</a> or stop in. <span class="menu-item-flag veg" style="margin:0;">V</span> = vegetarian &nbsp; <span class="menu-item-flag gf" style="margin:0;">GF</span> = gluten-free.</p>

    {render_full_menu_html()}

    <div class="card" style="background: var(--fd-cream); border-color: var(--fd-sun); margin-top: 24px;">
      <p style="margin: 0; color: var(--fd-ink-2);"><strong>This menu is pulled live from your current site &mdash; all real items and prices.</strong> Edit any item just by asking in the chat box: <em>"raise the Denver Omelette to $22"</em> or <em>"add a weekend special called Lobster Benedict at $28"</em>. Changes go live instantly &mdash; no dashboard.</p>
    </div>
  </div>
</section>
''' + render_faq_section("menu")


def main_hours():
    return f'''
<section class="hero" style="min-height: 340px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Hours &amp; Location</span>
    <h1>
      <span id="edit-hours-h1-main">On Scripps Ranch Blvd.</span>
      <span class="accent" id="edit-hours-h1-accent">Open from 6:30 every morning.</span>
    </h1>
    <p class="hero-lede" id="edit-hours-lede">Breakfast and lunch every day, plus dinner Wednesday through Saturday evening.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">

      <div>
        <span class="eyebrow">Hours</span>
        <h2>When we're open</h2>
        <div class="hours-card">
          <div class="hours-row"><span class="hours-day" id="edit-hrs-sun-day">Sunday</span><span class="hours-time" id="edit-hrs-sun-time">6:30 AM &ndash; 3:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-mon-day">Monday</span><span class="hours-time" id="edit-hrs-mon-time">6:30 AM &ndash; 3:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-tue-day">Tuesday</span><span class="hours-time" id="edit-hrs-tue-time">6:30 AM &ndash; 3:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-wed-day">Wednesday <span class="hours-tag">+ Dinner</span></span><span class="hours-time" id="edit-hrs-wed-time">6:30 AM &ndash; 3:00 PM &middot; 4:00 &ndash; 8:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-thu-day">Thursday <span class="hours-tag">+ Dinner</span></span><span class="hours-time" id="edit-hrs-thu-time">6:30 AM &ndash; 3:00 PM &middot; 4:00 &ndash; 8:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-fri-day">Friday <span class="hours-tag">+ Dinner</span></span><span class="hours-time" id="edit-hrs-fri-time">6:30 AM &ndash; 3:00 PM &middot; 4:00 &ndash; 8:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-sat-day">Saturday <span class="hours-tag">+ Dinner</span></span><span class="hours-time" id="edit-hrs-sat-time">6:30 AM &ndash; 3:00 PM &middot; 4:00 &ndash; 8:00 PM</span></div>
        </div>

        <h3 style="color: var(--fd-teal-3); margin-top: 32px;" id="edit-hours-breakfast-title">Breakfast is all day</h3>
        <p id="edit-hours-breakfast-desc">The full breakfast menu is available the entire time we're open &mdash; order a Benedict at 2 PM if you like. Lunch items come out from late morning on.</p>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;" id="edit-hours-dinner-title">Dinner, Wednesday&ndash;Saturday</h3>
        <p id="edit-hours-dinner-desc">Our sit-down dinner menu runs 4:00 to 8:00 PM, Wednesday through Saturday. Sunday, Monday, and Tuesday we close after lunch at 3:00 PM.</p>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;" id="edit-hours-takeout-title">Takeout</h3>
        <p id="edit-hours-takeout-desc">Available all open hours &mdash; call <a href="tel:+18583972530">(858) 397-2530</a> and we'll have it ready.</p>
      </div>

      <div>
        <span class="eyebrow">Find us</span>
        <h2>In Scripps Ranch</h2>
        <p style="font-size: 1.15rem; color: var(--fd-ink-2); margin-bottom: 16px;" id="edit-loc-address">
          10006 Scripps Ranch Boulevard<br/>
          San Diego, CA 92131
        </p>
        <p><a href="tel:+18583972530" style="font-family: var(--font-display); font-size: 1.4rem; color: var(--fd-red);" id="edit-loc-phone">(858) 397-2530</a></p>

        <div style="border-radius: 12px; overflow: hidden; box-shadow: var(--fd-shadow); aspect-ratio: 4 / 3; margin-top: 18px;">
          <iframe src="{MAP_EMBED}" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>

        <a class="btn btn-teal" href="https://maps.google.com/?q=10006+Scripps+Ranch+Blvd+San+Diego+CA+92131" target="_blank" rel="noopener" style="margin-top: 18px;">Open in Google Maps</a>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;" id="edit-loc-park-title">Parking</h3>
        <p id="edit-loc-park-desc">Parking is available in the shopping-center lot right out front &mdash; easy in, easy out, even on a busy weekend morning.</p>
      </div>

    </div>
  </div>
</section>
''' + render_faq_section("hours")


def main_reservations():
    return '''
<section class="hero" style="min-height: 360px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Reservations</span>
    <h1>
      <span id="edit-rsvp-h1-main">Save your table.</span>
      <span class="accent" id="edit-rsvp-h1-accent">Or the whole room.</span>
    </h1>
    <p class="hero-lede" id="edit-rsvp-lede">Weekend breakfast with the family, a birthday brunch, a Wednesday-night dinner, a small private party. Tell us when and we'll set it up.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <span class="eyebrow">How it works</span>
        <h2 id="edit-rsvp-how-h2">Quick and simple.</h2>
        <p id="edit-rsvp-how-p1">Fill out the form and we'll confirm by phone or text during open hours. For parties of 8 or more, please call directly at <a href="tel:+18583972530">(858) 397-2530</a> so we can put the right tables together.</p>
        <p id="edit-rsvp-how-p2">Breakfast is mostly walk-in, but a reservation can save you a wait on a busy weekend morning. Dinner (Wed&ndash;Sat) reservations are a good idea.</p>

        <h3 style="color: var(--fd-teal-3); margin-top: 32px;" id="edit-rsvp-special-title">Birthdays &amp; celebrations</h3>
        <p id="edit-rsvp-special-desc">Note the occasion in the form &mdash; a birthday breakfast, an anniversary, a graduation brunch &mdash; and we'll make sure the table's ready and the team's in on it.</p>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;" id="edit-rsvp-private-title">Private parties &amp; groups</h3>
        <p id="edit-rsvp-private-desc">Showers, family gatherings, team breakfasts, small private events &mdash; we can reserve a section or, for the right size group, the room. Send the date, headcount, and what you're planning and we'll come back with a simple plan.</p>
      </div>

      <form class="card" onsubmit="event.preventDefault(); alert('Preview only - replace this handler with email-to-host or a reservation integration (Resy / OpenTable / Yelp Reservations / direct email) at go-live.');" style="background: #fff;">
        <h3 style="margin-bottom: 18px;">Request a table</h3>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">First name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Last name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
        </div>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Phone</label>
        <input type="tel" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Email</label>
        <input type="email" style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Date &amp; time</label>
            <input type="datetime-local" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Party size</label>
            <select required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
              <option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8+</option>
            </select>
          </div>
        </div>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Occasion (optional)</label>
        <select style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
          <option value="">None / just a meal</option>
          <option>Birthday</option>
          <option>Anniversary</option>
          <option>Weekend brunch</option>
          <option>Private party / group</option>
          <option>Other</option>
        </select>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Notes (optional)</label>
        <textarea rows="3" placeholder="High chair, allergies, seating preference, group menu..." style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 18px; font-family: inherit; font-size: 0.95rem;"></textarea>

        <button type="submit" class="btn btn-teal" style="width: 100%;">Request Table</button>

        <p style="font-size: 0.78rem; color: var(--fd-ink-3); margin-top: 12px; margin-bottom: 0;">We'll confirm by phone or text during open hours.</p>
      </form>
    </div>
  </div>
</section>
''' + render_faq_section("reservations")


def main_contact():
    return '''
<section class="hero" style="min-height: 340px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Contact</span>
    <h1>
      <span id="edit-contact-h1-main">Call, message,</span>
      <span class="accent" id="edit-contact-h1-accent">or just stop in.</span>
    </h1>
    <p class="hero-lede" id="edit-contact-lede">We answer the phone and we read the form. We're here from 6:30 every morning.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <span class="eyebrow">Fay's Diner &amp; Cafe</span>
        <h2>Reach us</h2>
        <p style="font-size: 1.15rem; color: var(--fd-ink-2);" id="edit-contact-address">
          10006 Scripps Ranch Boulevard<br/>
          San Diego, CA 92131
        </p>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;">Phone</h3>
        <p><a href="tel:+18583972530" style="font-size: 1.4rem; font-family: var(--font-display);" id="edit-contact-phone">(858) 397-2530</a></p>
        <p style="color: var(--fd-ink-3); font-size: 0.92rem;" id="edit-contact-phone-note">Call for takeout orders, reservations, large groups, or private-party planning.</p>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;">Hours</h3>
        <p id="edit-contact-hours">Breakfast &amp; lunch daily 6:30 AM &ndash; 3:00 PM<br/>Dinner Wed&ndash;Sat 4:00 PM &ndash; 8:00 PM</p>

        <h3 style="color: var(--fd-teal-3); margin-top: 28px;">Follow Fay's</h3>
        <ul style="list-style: none; padding: 0; margin: 0;">
          <li style="margin-bottom: 6px;"><a href="https://www.facebook.com/112806368390004" target="_blank" rel="noopener">Facebook &rarr;</a></li>
          <li style="margin-bottom: 6px;"><a href="https://www.instagram.com/faysdiner" target="_blank" rel="noopener">Instagram (@faysdiner) &rarr;</a></li>
          <li style="margin-bottom: 6px;"><a href="https://www.yelp.com/biz/fays-diner-and-cafe-san-diego" target="_blank" rel="noopener">Yelp &rarr;</a></li>
        </ul>

        <a class="btn btn-teal" href="https://maps.google.com/?q=10006+Scripps+Ranch+Blvd+San+Diego+CA+92131" target="_blank" rel="noopener" style="margin-top: 24px;">Open in Google Maps</a>
      </div>

      <form class="card" onsubmit="event.preventDefault(); alert('Preview only - wire to email or CRM at go-live.');" style="background: #fff;">
        <h3 style="margin-bottom: 18px;">Send us a message</h3>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">First name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Last name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
        </div>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Email</label>
        <input type="email" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Phone (optional)</label>
        <input type="tel" style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">What can we help with?</label>
        <select style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
          <option>Reservation question</option>
          <option>Takeout order</option>
          <option>Private party / large group</option>
          <option>Catering</option>
          <option>Feedback / comment</option>
          <option>Other</option>
        </select>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--fd-ink-3); margin-bottom: 4px;">Message</label>
        <textarea rows="5" required style="width:100%; padding: 10px 12px; border: 1px solid var(--fd-line); border-radius: 4px; margin-bottom: 18px; font-family: inherit; font-size: 0.95rem;"></textarea>

        <button type="submit" class="btn btn-teal" style="width: 100%;">Send Message</button>
      </form>

    </div>
  </div>
</section>
''' + render_faq_section("contact")


# ------------------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------------------

PAGES = {
    "index": {
        "filename": "index.html",
        "canonical_path": "",
        "title": "Fay's Diner &amp; Cafe - All-Day Breakfast &amp; Dinner in Scripps Ranch, San Diego",
        "meta_desc": "Fay's Diner & Cafe is an all-day breakfast and lunch cafe in Scripps Ranch, San Diego, with a full dinner menu Wednesday through Saturday. Benedicts, French toast, burritos, burgers, and weekend dinner entrees.",
        "og_title": "Fay's Diner & Cafe - Scripps Ranch, San Diego",
        "og_desc": "All-day breakfast and lunch every day, full dinner menu Wed-Sat. Benedicts, French toast, burritos, burgers, and more in Scripps Ranch.",
        "breadcrumb_items": [("Home", None)],
        "main": main_index,
        "extra_schemas": ["restaurant"],
    },
    "menu": {
        "filename": "menu.html",
        "canonical_path": "menu",
        "title": "Menu - Breakfast, Lunch &amp; Dinner . Fay's Diner &amp; Cafe, Scripps Ranch",
        "meta_desc": "The full Fay's Diner & Cafe menu - all-day breakfast (Benedicts, omelettes, French toast, burritos), lunch (salads, sandwiches, burgers), and a Wednesday-through-Saturday dinner menu. Scripps Ranch, San Diego.",
        "og_title": "Menu - Fay's Diner & Cafe",
        "og_desc": "All-day breakfast, lunch, and weekend dinner. Benedicts, omelettes, burritos, burgers, salads, and dinner entrees with prices.",
        "breadcrumb_items": [("Home", "index.html"), ("Menu", None)],
        "main": main_menu,
        "extra_schemas": ["restaurant"],
    },
    "hours": {
        "filename": "hours.html",
        "canonical_path": "hours",
        "title": "Hours &amp; Location . Fay's Diner &amp; Cafe, Scripps Ranch San Diego",
        "meta_desc": "Fay's Diner & Cafe is open daily 6:30 AM to 3:00 PM for breakfast and lunch, with dinner Wednesday through Saturday 4 to 8 PM. 10006 Scripps Ranch Blvd, San Diego, CA 92131.",
        "og_title": "Hours & Location - Fay's Diner & Cafe",
        "og_desc": "Open daily 6:30 AM-3 PM for breakfast & lunch; dinner Wed-Sat 4-8 PM. 10006 Scripps Ranch Blvd, San Diego.",
        "breadcrumb_items": [("Home", "index.html"), ("Hours &amp; Location", None)],
        "main": main_hours,
        "extra_schemas": ["restaurant"],
    },
    "reservations": {
        "filename": "reservations.html",
        "canonical_path": "reservations",
        "title": "Reservations &amp; Private Parties . Fay's Diner &amp; Cafe, Scripps Ranch",
        "meta_desc": "Request a table at Fay's Diner & Cafe - weekend brunch, weekday breakfast, Wed-Sat dinner, birthdays, and small private parties. Reserve online or call (858) 397-2530.",
        "og_title": "Reserve a Table - Fay's Diner & Cafe",
        "og_desc": "Weekend brunch, dinner Wed-Sat, birthdays, and small private parties. Reserve online or call (858) 397-2530.",
        "breadcrumb_items": [("Home", "index.html"), ("Reservations", None)],
        "main": main_reservations,
        "extra_schemas": [],
    },
    "contact": {
        "filename": "contact.html",
        "canonical_path": "contact",
        "title": "Contact &amp; Directions . Fay's Diner &amp; Cafe, Scripps Ranch San Diego",
        "meta_desc": "Contact Fay's Diner & Cafe: 10006 Scripps Ranch Blvd, San Diego, CA 92131. Call (858) 397-2530 for takeout, reservations, large groups, or private parties. Open daily from 6:30 AM.",
        "og_title": "Contact Fay's Diner & Cafe",
        "og_desc": "10006 Scripps Ranch Blvd, San Diego, CA . (858) 397-2530 . Open daily from 6:30 AM.",
        "breadcrumb_items": [("Home", "index.html"), ("Contact", None)],
        "main": main_contact,
        "extra_schemas": ["restaurant"],
    },
}


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------

def build_schema_block(page_key, page):
    schemas = [breadcrumb_schema(page["breadcrumb_items"]), faq_schema(FAQS[page_key])]
    for s in page.get("extra_schemas", []):
        if s == "restaurant":
            schemas.append(restaurant_schema())
    if len(schemas) == 1:
        return json.dumps(schemas[0], indent=2)
    return json.dumps(schemas, indent=2)


def render_page(page_key):
    page = PAGES[page_key]
    template = (BUILD / "template.html").read_text(encoding="utf-8")
    banner = (BUILD / "banner.html").read_text(encoding="utf-8")
    widget = (BUILD / "widget.html").read_text(encoding="utf-8")

    main_html = page["main"]()
    crumb = breadcrumb_html(page["breadcrumb_items"]) if len(page["breadcrumb_items"]) > 1 else ""
    schema_json = build_schema_block(page_key, page)

    out = template
    subs = {
        "{{PAGE_TITLE}}": page["title"],
        "{{META_DESC}}": page["meta_desc"],
        "{{OG_TITLE}}": page["og_title"],
        "{{OG_DESC}}": page["og_desc"],
        "{{CANONICAL_PATH}}": page["canonical_path"],
        "{{SCHEMA_JSON}}": schema_json,
        "{{BANNER}}": banner,
        "{{BREADCRUMB}}": crumb,
        "{{MAIN}}": main_html,
        "{{WIDGET}}": widget,
    }
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def main():
    print(f"Building Fay's Diner preview -> {OUT}")
    for key, page in PAGES.items():
        html = render_page(key)
        path = OUT / page["filename"]
        path.write_text(html, encoding="utf-8")
        edit_ids = len(re.findall(r'id="edit-', html))
        h1s = len(re.findall(r"<h1[ >]", html))
        print(f"  + {page['filename']:20s}  {len(html):>7,} bytes  .  {edit_ids:>3d} edit-* . {h1s} h1")


if __name__ == "__main__":
    main()
