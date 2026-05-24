#!/usr/bin/env python3
"""
CH Steak Lounge - preview builder.

Reads:
  _build/template.html  - page skeleton with {{TOKENS}}
  _build/banner.html    - Relaunch SEO banner (inline)
  _build/widget.html    - Relaunch edit widget (inline)

Emits to previews/ch-steak-lounge/:
  index.html . menu.html . music.html . hours.html . reservations.html . contact.html

Pattern mirrors previews/hidden-bridge/_build/build.py.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "_build"
OUT = ROOT

# ------------------------------------------------------------------------------
# Sitewide facts (verified from prospect_chsteaklounge.md + live scrape)
# ------------------------------------------------------------------------------

BUSINESS = {
    "name": "CH Steak Lounge",
    "alt_name": "Char",
    "url": "https://chsteaklounge.com",
    "phone": "+1-931-520-2427",
    "phone_display": "(931) 520-2427",
    "phone_tel": "9315202427",
    "street": "14 South Washington Avenue",
    "city": "Cookeville",
    "region": "TN",
    "postal": "38501",
    "country": "US",
    # Approximate Cookeville-square coordinates from the embedded Google Map iframe
    # on /location/ (3221.178591097992!2d-85.50112968478241!3d36.16220851105065)
    "lat": 36.16220851,
    "lng": -85.50112968,
    "price_range": "$$",
    "cuisine": ["Steakhouse", "American", "Bar"],
}

# ------------------------------------------------------------------------------
# Menu - sourced from live homepage scrape (verified items + prices)
# Sections marked PLACEHOLDER are reasonable inserts for a steakhouse menu that
# need owner confirmation before publishing.
# ------------------------------------------------------------------------------

MENU = [
    {
        "section": "Appetizers",
        "note": "House favorites - perfect for sharing or starting strong.",
        "items": [
            {"name": "Smoked Chicken Wings", "price": "$12", "desc": "Jumbo wings, hickory smoked in house. Plain, mild, hot, stupid hot, teriyaki, BBQ, or Cajun dry rub.", "flag": "Famous"},
            {"name": "Pizza Rockafella", "price": "$16.50", "desc": "Thin crust pizza topped with spinach artichoke dip, freshly ground chicken breast, mozzarella, sun dried tomatoes and jalapenos. Served with hot sauce."},
            {"name": "Cheese Stick Roulette", "price": "$13", "desc": "Assorted types of cheese sticks fried and served with marinara. Mozzarella sticks only $9."},
        ],
    },
    {
        "section": "Salads & Pastas",
        "note": "Bright sides and full-meal pastas.",
        "items": [
            {"name": "CH's Signature Salad (Sweet)", "price": "$6 / $12", "desc": "Dried cranberries, candied pecans, mandarin oranges, seasonal fruit, cherry tomatoes, feta cheese. House citrus vinaigrette recommended."},
            {"name": "Rattlesnake Pasta", "price": "$19", "desc": "Fettuccini tossed in a spicy Caribbean Alfredo sauce with broccoli and mushrooms. Add chicken +$6, shrimp or steak +$7.50, or shrimp, scallops and crab +$15.50.", "flag": "Hot"},
            {"name": "Heavenly Seafood Pasta", "price": "$32.50", "desc": "Angel hair pasta loaded with shrimp, scallops and blue crab cooked in a lemon pepper cream sauce."},
        ],
    },
    {
        "section": "Steaks",
        "note": "The best steaks in town, guaranteed. Served with two sides.",
        "items": [
            # PLACEHOLDER - the namesake of the restaurant is barely on the live site.
            # Owner to confirm cuts, weights, and prices before publishing.
            {"name": "Filet Mignon (8 oz)", "price": "$38", "desc": "Hand-cut tenderloin, broiled to your preferred temperature. The leanest, most tender cut on the menu."},
            {"name": "Ribeye (12 oz)", "price": "$36", "desc": "Bone-in, well-marbled, broiled. Steakhouse classic done right."},
            {"name": "Ribeye (16 oz)", "price": "$44", "desc": "The big one. 16 oz of well-marbled ribeye for the steak you came here for."},
            {"name": "New York Strip (12 oz)", "price": "$34", "desc": "Center-cut strip, firm and full-flavored. Recommended medium-rare."},
            {"name": "Top Sirloin (8 oz)", "price": "$26", "desc": "Lean cut, broiled. The weeknight steak."},
            {"name": "Surf & Turf", "price": "$48", "desc": "Petite filet plus shrimp scampi or scallops. The steakhouse classic."},
        ],
    },
    {
        "section": "Entrees",
        "note": "Beyond the steaks - chicken, salmon, and the kitchen's specialty creations.",
        "items": [
            {"name": "Stuffed Louisiana Chicken", "price": "$23.50", "desc": "Pan-fried chicken breast stuffed with Cajun sausage, served over garlic-infused rice, and topped with a spicy Tasso ham cream sauce."},
            {"name": "Fresh North Atlantic Salmon", "price": "$18.50", "desc": "Teriyaki-glazed, Cajun blackened, spicy sweet & sour, lemon peppered, or plain."},
            {"name": "Grilled Chicken Breast", "price": "$15.50", "desc": "Cajun, citrus, Italian, BBQ or plain."},
        ],
    },
    {
        "section": "Burgers & Sandwiches",
        "note": "Hand-formed patties, served with hand-cut fries.",
        "items": [
            # PLACEHOLDER - homepage says "the biggest/tastiest burger in Cookeville"
            # but no detail. Owner to confirm cuts, toppings, and prices.
            {"name": "The CH Burger", "price": "$14", "desc": "Half-pound hand-formed patty, lettuce, tomato, onion, pickle, on a toasted brioche bun. The one we built the reputation on."},
            {"name": "Smoked Brisket Sandwich", "price": "$15", "desc": "House-smoked brisket, slaw, pickles, brioche. Served with BBQ sauce on the side."},
            {"name": "Buffalo Chicken Sandwich", "price": "$13", "desc": "Hand-breaded chicken breast, buffalo sauce, lettuce, tomato, blue cheese crumbles."},
        ],
    },
    {
        "section": "Sides",
        "note": "$5 each, or included with steaks and entrees.",
        "items": [
            {"name": "Loaded Baked Potato", "price": "$5", "desc": "Butter, sour cream, cheddar, bacon, chives."},
            {"name": "Garlic Mashed Potatoes", "price": "$5", "desc": "Real potatoes, real butter, real garlic."},
            {"name": "Hand-Cut Fries", "price": "$5", "desc": "Russet potatoes, cut in house, fried twice."},
            {"name": "Sauteed Mushrooms", "price": "$5", "desc": "Cremini and button mushrooms, butter, garlic, fresh thyme."},
            {"name": "Asparagus", "price": "$5", "desc": "Lightly grilled with lemon and sea salt."},
            {"name": "Seasonal Vegetable", "price": "$5", "desc": "Ask your server for tonight's preparation."},
        ],
    },
]


# ------------------------------------------------------------------------------
# Live music schedule - PLACEHOLDER - owner-confirmed before publishing
# ------------------------------------------------------------------------------
MUSIC_EVENTS = [
    {"date": "Fri, May 29 2026", "iso_date": "2026-05-29T21:00", "act": "The Whiskey Dogs", "genre": "Southern rock / blues", "time": "9:00 PM"},
    {"date": "Sat, May 30 2026", "iso_date": "2026-05-30T21:00", "act": "Hattie Mae & The Holler", "genre": "Americana / country", "time": "9:00 PM"},
    {"date": "Thu, Jun 4 2026", "iso_date": "2026-06-04T20:00", "act": "Open Mic Night", "genre": "All welcome - sign up at the bar", "time": "8:00 PM"},
    {"date": "Fri, Jun 5 2026", "iso_date": "2026-06-05T21:00", "act": "Lonesome Pine String Band", "genre": "Bluegrass", "time": "9:00 PM"},
    {"date": "Sat, Jun 6 2026", "iso_date": "2026-06-06T21:00", "act": "The Squaretown Soul Revue", "genre": "Soul / R&B", "time": "9:00 PM"},
    {"date": "Fri, Jun 12 2026", "iso_date": "2026-06-12T21:00", "act": "Cookeville Stomp", "genre": "Honky-tonk", "time": "9:00 PM"},
    {"date": "Sat, Jun 13 2026", "iso_date": "2026-06-13T21:00", "act": "Hayride Highway", "genre": "Country rock", "time": "9:00 PM"},
]


# ------------------------------------------------------------------------------
# Schema builders
# ------------------------------------------------------------------------------

def restaurant_schema():
    """Full Restaurant + LocalBusiness markup - referenced from multiple pages."""
    menu_items_schema = []
    for section in MENU:
        for item in section["items"]:
            menu_items_schema.append({
                "@type": "MenuItem",
                "name": item["name"],
                "description": item["desc"],
                "offers": {
                    "@type": "Offer",
                    "price": _price_to_number(item["price"]),
                    "priceCurrency": "USD",
                },
                "menuAddOn": [],
                "suitableForDiet": [],
            })

    return {
        "@context": "https://schema.org",
        "@type": ["Restaurant", "LocalBusiness", "BarOrPub"],
        "@id": f"{BUSINESS['url']}/#restaurant",
        "name": BUSINESS["name"],
        "alternateName": BUSINESS["alt_name"],
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
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"],
                "opens": "11:00",
                "closes": "21:00",
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Friday", "Saturday"],
                "opens": "11:00",
                "closes": "22:00",
            },
        ],
        "sameAs": [
            "https://www.facebook.com/CharCookeville/",
            "https://twitter.com/charcookeville",
            "https://restaurantguru.com/Char-Cookeville",
        ],
        "hasMenu": {
            "@type": "Menu",
            "name": "CH Steak Lounge Menu",
            "hasMenuSection": [
                {
                    "@type": "MenuSection",
                    "name": section["section"],
                    "description": section["note"],
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": item["name"],
                            "description": item["desc"],
                            "offers": {
                                "@type": "Offer",
                                "price": _price_to_number(item["price"]),
                                "priceCurrency": "USD",
                            },
                        }
                        for item in section["items"]
                    ],
                }
                for section in MENU
            ],
        },
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Live music", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Full bar", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Happy hour", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Carry-out", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Reservations accepted", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Wheelchair accessible", "value": True},
        ],
        # NOTE: AggregateRating intentionally NOT stubbed - connect real Google Reviews
        # before publishing per feedback_pagespeed_positioning sister-rule on review honesty.
    }


def _price_to_number(price_str):
    """Strip $ and grab the first numeric value. Handles '$12', '$6 / $12', '$16.50'."""
    m = re.search(r"\$?(\d+(?:\.\d+)?)", price_str)
    return float(m.group(1)) if m else 0


def event_schema(ev):
    """Event schema for a live-music night."""
    return {
        "@context": "https://schema.org",
        "@type": "MusicEvent",
        "name": f"{ev['act']} at CH Steak Lounge",
        "startDate": ev["iso_date"],
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
            "@type": "Place",
            "name": BUSINESS["name"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": BUSINESS["street"],
                "addressLocality": BUSINESS["city"],
                "addressRegion": BUSINESS["region"],
                "postalCode": BUSINESS["postal"],
                "addressCountry": BUSINESS["country"],
            },
        },
        "performer": {"@type": "MusicGroup", "name": ev["act"]},
        "organizer": {"@type": "Restaurant", "@id": f"{BUSINESS['url']}/#restaurant"},
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": f"{BUSINESS['url']}/music",
            "description": "No cover - food and drink minimums apply",
        },
        "description": f"Live {ev['genre']} at CH Steak Lounge on the square in Cookeville, TN.",
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
# Sitewide FAQ pool (>=30 questions sitewide for AI-search citation)
# ------------------------------------------------------------------------------
FAQS = {
    "index": [
        ("Where is CH Steak Lounge?",
         "CH Steak Lounge is at 14 South Washington Avenue, right on the square in downtown Cookeville, Tennessee."),
        ("Is CH Steak Lounge the same as Char?",
         "Yes - CH Steak Lounge was formerly branded simply as Char, which is why some of our older reviews, social media, and signage still use that name. Same restaurant, same owners, same kitchen."),
        ("What kind of food does CH Steak Lounge serve?",
         "CH Steak Lounge is a steakhouse and bar. We're best known for our steaks, our famous smoked chicken wings, Rattlesnake Pasta, and the biggest burger in Cookeville. Full bar with daily happy hour."),
        ("Does CH Steak Lounge have live music?",
         "Yes - we book live music most nights after 9 PM. Bluegrass, country, blues, Americana, soul, open mic - see the Live Music page for the current schedule."),
        ("Do you take reservations?",
         "Yes. You can request a reservation through our Reservations page or by calling (931) 520-2427. Walk-ins are always welcome too."),
    ],
    "menu": [
        ("What are the most popular items on the CH Steak Lounge menu?",
         "Our most-ordered items are the Smoked Chicken Wings, Pizza Rockafella, Rattlesnake Pasta, the CH Burger, and our hand-cut steaks. The Signature Salad is a long-time customer favorite."),
        ("Do you have vegetarian options?",
         "We have salads, pastas without meat, and several sides that work as a vegetarian meal. Ask your server - the kitchen can adjust most dishes."),
        ("How are your wings cooked?",
         "Our wings are jumbo, hickory smoked in house, and finished to order. Choose from plain, mild, hot, stupid hot, teriyaki, BBQ, or our Cajun dry rub."),
        ("Can I get the Rattlesnake Pasta less spicy?",
         "Yes - the kitchen can dial the heat down on request. Just tell your server."),
        ("Do you have a kids' menu?",
         "Yes, we have simpler portions and milder options for children. Ask your server for the kids' menu when you sit down."),
    ],
    "music": [
        ("When is live music at CH Steak Lounge?",
         "Live music plays most nights starting around 9 PM, with bands typically going until close. Check the Live Music page for the current week's schedule."),
        ("Is there a cover charge for live music?",
         "No cover - dinner and drink minimums apply. Just buy something at the bar or restaurant and enjoy the show."),
        ("What kinds of music does CH Steak Lounge book?",
         "We book a wide mix - bluegrass, country, Americana, blues, southern rock, soul, and open mic night every other Thursday. The Live Music page has each act's genre."),
        ("Can my band play at CH Steak Lounge?",
         "We're always listening for new acts. Send a link to your music and a few available dates through the Contact page and we'll get back to you."),
        ("Where should I park to come hear live music?",
         "Public parking is available around the Cookeville square, with additional spots within a short walk on the side streets. Spaces fill up on busy Friday and Saturday nights - arrive early."),
    ],
    "hours": [
        ("What are CH Steak Lounge's hours?",
         "Monday through Thursday: 11 AM to 9 PM. Friday and Saturday: 11 AM to 10 PM. Closed Sunday."),
        ("When is happy hour at CH Steak Lounge?",
         "Happy hour is every day from 2 PM to 6 PM. $7 appetizers, $2.50 domestic drafts, and $4 wells and wines."),
        ("Are you open on Sunday?",
         "CH Steak Lounge is closed on Sundays."),
        ("Do you have late-night drink specials?",
         "Yes - drink specials run every evening from 9 PM until close, in addition to the daily happy hour."),
        ("Do you serve dinner music?",
         "Dinner music plays occasionally - call ahead at (931) 520-2427 if you're planning a date night and want to confirm the night's music."),
    ],
    "reservations": [
        ("Can I make a reservation at CH Steak Lounge?",
         "Yes - request a reservation through the Reservations page, or call (931) 520-2427. We confirm by phone for parties of 6 or more."),
        ("How far in advance should I reserve?",
         "Friday and Saturday nights and any night with a popular live-music act fill up fast - we recommend reserving at least a few days ahead. Weeknights you can usually book the same day."),
        ("Can I reserve a table for a special occasion?",
         "Yes. Tell us in the reservation request - birthday, anniversary, work celebration, first date - and we'll make a note so the team takes care of you."),
        ("Do you host private events?",
         "Yes. We host birthday dinners, rehearsal dinners, work parties, and other private events. Tell us the date, party size, and what you're celebrating - we'll put a package together."),
        ("Do you do carry-out?",
         "Yes - carry-out is available during all open hours. Call (931) 520-2427 to place an order."),
    ],
    "contact": [
        ("What's the phone number for CH Steak Lounge?",
         "CH Steak Lounge can be reached at (931) 520-2427."),
        ("Where can I find the address?",
         "We're at 14 South Washington Avenue, Cookeville, TN 38501 - right on the downtown square."),
        ("How do I get to CH Steak Lounge from I-40?",
         "Take exit 287 (TN-136 / Burgess Falls Rd) into Cookeville. Follow Washington Avenue to the downtown square - we're on the south side of the square."),
        ("Is there parking near CH Steak Lounge?",
         "Public parking is available around the Cookeville square and on the surrounding side streets. There's no dedicated lot - first-come first-served street parking."),
        ("Is CH Steak Lounge wheelchair accessible?",
         "Yes, our entrance and seating are wheelchair accessible. If you have specific accessibility needs for a reservation, let us know when you book and we'll set up the right table."),
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


def render_menu_html():
    """Render the full menu as nested sections - reused on index (excerpt) and menu page."""
    out = ""
    for s_idx, section in enumerate(MENU):
        items_html = ""
        for i_idx, item in enumerate(section["items"]):
            flag = ""
            if "flag" in item:
                flag_class = "hot" if item["flag"].lower() == "hot" else ""
                flag = f' <span class="menu-item-flag {flag_class}">{item["flag"]}</span>'
            items_html += f'''
            <div class="menu-item-row">
              <div class="menu-item-top">
                <h3 class="menu-item-name" id="edit-menu-{s_idx}-{i_idx}-name">{item["name"]}{flag}</h3>
                <span class="menu-item-price" id="edit-menu-{s_idx}-{i_idx}-price">{item["price"]}</span>
              </div>
              <p class="menu-item-desc" id="edit-menu-{s_idx}-{i_idx}-desc">{item["desc"]}</p>
            </div>'''
        out += f'''
        <div class="menu-section">
          <div class="menu-section-head">
            <h2 id="edit-menu-{s_idx}-section">{section["section"]}</h2>
            <span class="menu-section-note" id="edit-menu-{s_idx}-note">{section["note"]}</span>
          </div>
          <div class="menu-grid">
            {items_html}
          </div>
        </div>'''
    return out


# ------------------------------------------------------------------------------
# Page main-content generators
# ------------------------------------------------------------------------------

def main_index():
    # Show first 2 menu sections as a homepage tease; full menu on menu.html.
    # Show first 3 upcoming shows as a live-music tease.
    music_rows = ""
    for ev in MUSIC_EVENTS[:4]:
        music_rows += f'''
          <tr>
            <td class="event-date">{ev["date"]}</td>
            <td><span class="event-act">{ev["act"]}</span><br/><span style="color: var(--ch-ink-3); font-size: 0.85rem;">{ev["genre"]}</span></td>
            <td class="event-time">{ev["time"]}</td>
          </tr>'''

    return f'''
<section class="hero">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline" id="edit-hero-tagline">Cookeville, TN &middot; On the Square</span>
    <h1>
      <span id="edit-hero-h1-main">Great food. Cold drinks.</span>
      <span class="accent" id="edit-hero-h1-accent">Best live music in town.</span>
    </h1>
    <p class="hero-lede" id="edit-hero-lede">A steakhouse on the Cookeville square - famous smoked wings, hand-cut steaks, and live music most nights after 9. Open Monday through Saturday.</p>
    <div class="hero-ctas">
      <a href="reservations.html" class="btn btn-primary">Make a Reservation</a>
      <a href="menu.html" class="btn btn-ghost">See the Menu</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="stats">
      <div class="stat"><div class="stat-num">15+</div><div class="stat-label">Years on the Square</div></div>
      <div class="stat"><div class="stat-num">6</div><div class="stat-label">Days a Week</div></div>
      <div class="stat"><div class="stat-num">9pm</div><div class="stat-label">Music Most Nights</div></div>
      <div class="stat"><div class="stat-num">2-6pm</div><div class="stat-label">Daily Happy Hour</div></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid grid-2" style="align-items: center;">
      <div>
        <span class="eyebrow">About CH Steak Lounge</span>
        <h2 id="edit-mission-h2">A Cookeville steakhouse with a bar attached and a stage in the corner.</h2>
        <p id="edit-mission-p1">CH Steak Lounge (formerly Char) has been on the Cookeville square for years, serving great food, pouring cold drinks, and booking the best live music in town. Our menu favorites include our famous smoked chicken wings, Pizza Rockafella, Rattlesnake Pasta, the Signature Summer Salad, and the biggest and tastiest burger in Cookeville.</p>
        <p id="edit-mission-p2">And don't forget - CH Steak Lounge has the best steaks in town. Hand-cut, broiled, served with two real sides. That's what the name's about.</p>
        <a href="menu.html" class="btn btn-oxblood">See the Full Menu</a>
      </div>
      <div>
        <div style="aspect-ratio: 4 / 5; background: linear-gradient(160deg, var(--ch-oxblood) 0%, var(--ch-ink) 60%, var(--ch-smoke) 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: var(--ch-shadow); position: relative; overflow: hidden;">
          <div style="text-align: center; color: var(--ch-cream); padding: 32px;">
            <div style="font-family: var(--font-display); font-size: 4rem; font-weight: 700; color: var(--ch-brass); line-height: 1; margin-bottom: 16px;">CH</div>
            <div style="font-family: var(--font-display); font-size: 1.6rem; font-weight: 600; margin-bottom: 6px;">Steak Lounge</div>
            <div style="font-size: 0.8rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ch-brass-2);">Est. on the Cookeville Square</div>
            <div style="margin-top: 32px; font-style: italic; color: rgba(243,231,200,0.7); font-size: 0.9rem;">Real photo will go here - owner to provide interior or food shot</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Off the menu</span>
    <h2>A taste of what we serve</h2>
    <p class="section-lede">The full menu lives on the <a href="menu.html">Menu page</a>. A few of the dishes we're best known for:</p>

    <div class="menu-section">
      <div class="menu-section-head">
        <h2>House Favorites</h2>
      </div>
      <div class="menu-grid">

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-wings-name">Smoked Chicken Wings <span class="menu-item-flag">Famous</span></h3>
            <span class="menu-item-price" id="edit-feat-wings-price">$12</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-wings-desc">Jumbo wings hickory smoked in house. Plain, mild, hot, stupid hot, teriyaki, BBQ, or Cajun dry rub.</p>
        </div>

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-rattlesnake-name">Rattlesnake Pasta <span class="menu-item-flag hot">Hot</span></h3>
            <span class="menu-item-price" id="edit-feat-rattlesnake-price">$19</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-rattlesnake-desc">Fettuccini tossed in a spicy Caribbean Alfredo sauce with broccoli and mushrooms. Add chicken, shrimp, steak, or the seafood trio.</p>
        </div>

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-ribeye-name">Ribeye (16 oz)</h3>
            <span class="menu-item-price" id="edit-feat-ribeye-price">$44</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-ribeye-desc">The big one. 16 oz of well-marbled, bone-in ribeye, broiled to your preferred temperature. Served with two sides.</p>
        </div>

        <div class="menu-item-row">
          <div class="menu-item-top">
            <h3 class="menu-item-name" id="edit-feat-rockafella-name">Pizza Rockafella</h3>
            <span class="menu-item-price" id="edit-feat-rockafella-price">$16.50</span>
          </div>
          <p class="menu-item-desc" id="edit-feat-rockafella-desc">Thin crust topped with spinach artichoke dip, ground chicken, mozzarella, sun-dried tomatoes, and jalapenos. Served with hot sauce.</p>
        </div>

      </div>
    </div>

    <div style="text-align: center; margin-top: 24px;">
      <a href="menu.html" class="btn btn-oxblood">See the full menu &rarr;</a>
    </div>
  </div>
</section>

<section class="section smoke">
  <div class="container">
    <span class="eyebrow">This week on stage</span>
    <h2 style="color: var(--ch-cream);">Live music most nights after 9 PM</h2>
    <p class="section-lede">Bluegrass, country, blues, Americana, soul, and open mic. No cover - dinner and drink minimums apply.</p>

    <div style="background: rgba(0,0,0,0.30); border-radius: 10px; overflow: hidden;">
      <table class="events-table" style="background: transparent;">
        <thead>
          <tr><th>Date</th><th>Act</th><th>Start</th></tr>
        </thead>
        <tbody>
          {music_rows}
        </tbody>
      </table>
    </div>

    <div style="text-align: center; margin-top: 24px;">
      <a href="music.html" class="btn btn-primary">See the full music schedule &rarr;</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">What we do</span>
    <h2>Find what you came for</h2>
    <div class="grid grid-3">

      <a href="menu.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">M</span>
        <h3 id="edit-svc-menu-title">The Menu</h3>
        <p id="edit-svc-menu-desc">Steaks, smoked wings, the Rattlesnake Pasta, burgers, salads, sides. Hand-cut and prepared in house.</p>
      </a>

      <a href="music.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">&#9835;</span>
        <h3 id="edit-svc-music-title">Live Music</h3>
        <p id="edit-svc-music-desc">Live bands most nights after 9 PM. Bluegrass, country, soul, blues, open mic. No cover.</p>
      </a>

      <a href="reservations.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">R</span>
        <h3 id="edit-svc-rsvp-title">Reservations &amp; Events</h3>
        <p id="edit-svc-rsvp-desc">Book a table, plan a birthday, host a rehearsal dinner. We'll set you up.</p>
      </a>

      <a href="hours.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">H</span>
        <h3 id="edit-svc-hours-title">Hours &amp; Location</h3>
        <p id="edit-svc-hours-desc">Mon-Thu 11a-9p &middot; Fri-Sat 11a-10p &middot; Happy hour every day 2-6pm.</p>
      </a>

      <a href="hours.html#happy-hour" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">$</span>
        <h3 id="edit-svc-hh-title">Happy Hour</h3>
        <p id="edit-svc-hh-desc">Every day 2pm to 6pm. $7 apps, $2.50 domestic drafts, $4 wells and wines.</p>
      </a>

      <a href="contact.html" class="card" style="text-decoration: none; color: inherit;">
        <span class="card-icon">&rarr;</span>
        <h3 id="edit-svc-contact-title">Contact &amp; Directions</h3>
        <p id="edit-svc-contact-desc">14 South Washington on the square. Parking around the square and side streets.</p>
      </a>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="quote">
      <span id="edit-quote-text">Best steaks in Cookeville, period. The wings are worth driving in for on their own, and there's almost always a good band playing.</span>
      <span class="quote-attr" id="edit-quote-attr">- a Cookeville regular &middot; placeholder, replace with a real Google review when reviews are connected</span>
    </div>
  </div>
</section>
''' + render_faq_section("index")


def main_menu():
    return f'''
<section class="hero" style="min-height: 380px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">The Menu</span>
    <h1>
      <span id="edit-menu-h1-main">Steaks, smoke,</span>
      <span class="accent" id="edit-menu-h1-accent">and Cookeville classics.</span>
    </h1>
    <p class="hero-lede" id="edit-menu-lede">Hand-cut steaks, smoked-in-house wings, pastas with attitude, burgers built right. Full bar, daily happy hour, live music after 9.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Menu</span>
    <h2>What's on the table tonight</h2>
    <p class="section-lede">Prices may change with season and supply. For the freshest version, call (931) 520-2427 or stop in - we're on the south side of the square.</p>

    {render_menu_html()}

    <div class="card" style="background: var(--ch-cream); border-color: var(--ch-brass); margin-top: 24px;">
      <p style="margin: 0; color: var(--ch-ink-2);"><strong>Menu pending owner confirmation.</strong> Appetizers, Salads &amp; Pastas, and Entrees are from the live homepage. Steaks, Burgers, and Sides are reasonable placeholders for a Cookeville steakhouse - replace with real cuts, weights, and prices before going live. Edit any item through chat: <em>"raise the ribeye to $46"</em> or <em>"add a new side called brussels sprouts at $6"</em>.</p>
    </div>
  </div>
</section>
''' + render_faq_section("menu")


def main_music():
    rows = ""
    for ev in MUSIC_EVENTS:
        rows += f'''
        <tr>
          <td class="event-date">{ev["date"]}</td>
          <td><span class="event-act">{ev["act"]}</span></td>
          <td>{ev["genre"]}</td>
          <td class="event-time">{ev["time"]}</td>
        </tr>'''
    return f'''
<section class="hero" style="min-height: 380px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Live Music</span>
    <h1>
      <span id="edit-music-h1-main">Most nights after 9.</span>
      <span class="accent" id="edit-music-h1-accent">No cover.</span>
    </h1>
    <p class="hero-lede" id="edit-music-lede">Bluegrass, country, soul, blues, southern rock, Americana, and open mic. The best stage on the Cookeville square.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">This week and next</span>
    <h2>Upcoming shows</h2>
    <p class="section-lede">Music typically starts at 9 PM and runs until close. No cover charge - food and drink minimums apply. Call (931) 520-2427 to confirm the night-of lineup, since weather and travel sometimes shift things.</p>

    <table class="events-table">
      <thead>
        <tr><th>Date</th><th>Act</th><th>Genre</th><th>Start</th></tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

    <div class="card" style="background: var(--ch-cream); border-color: var(--ch-brass); margin-top: 24px;">
      <p style="margin: 0; color: var(--ch-ink-2);"><strong>Music calendar pending owner confirmation.</strong> The shows above are placeholders sized for a typical CH lineup. Replace with the real booking calendar. Edit through chat: <em>"change Friday May 29 to The Cumberland Plateau Boys"</em> or <em>"add a Saturday June 20 show with The Highway 70 Band, country, 9pm"</em>.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <span class="eyebrow">How it works</span>
        <h2 id="edit-music-how-h2">A live-music night at CH</h2>
        <p id="edit-music-how-p1">Most nights, the band starts around 9 PM and plays until close. The kitchen stays open through Fri-Sat 10 PM, and the bar serves drink specials every evening from 9 PM until close. Seats around the stage fill up first - arrive earlier for a good view.</p>
        <p id="edit-music-how-p2">If you're coming specifically for an act, calling ahead (931) 520-2427 to reserve a table is a good move on Friday and Saturday nights. The smaller weeknight shows usually have walk-up seating.</p>
        <a href="reservations.html" class="btn btn-oxblood">Reserve for a show</a>
      </div>
      <div class="card">
        <h3 id="edit-music-bands-title">Booking your band at CH</h3>
        <p id="edit-music-bands-desc">We're always listening for new acts that fit the room - country, Americana, blues, bluegrass, soul, classic rock, songwriter-style. Send a link to a few songs and the dates you're available through our Contact page, and we'll get back to you about an opening.</p>
        <a href="contact.html" class="btn btn-ghost" style="color: var(--ch-oxblood) !important; border-color: var(--ch-oxblood); margin-top: 10px;">Pitch your band &rarr;</a>
      </div>
    </div>
  </div>
</section>
''' + render_faq_section("music")


def main_hours():
    return '''
<section class="hero" style="min-height: 340px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Hours &amp; Location</span>
    <h1>
      <span id="edit-hours-h1-main">14 South Washington.</span>
      <span class="accent" id="edit-hours-h1-accent">Right on the square.</span>
    </h1>
    <p class="hero-lede" id="edit-hours-lede">Open Monday through Saturday for lunch, dinner, and the late hours when the music starts.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">

      <div>
        <span class="eyebrow">Hours</span>
        <h2>When we're open</h2>
        <div class="hours-card">
          <div class="hours-row"><span class="hours-day" id="edit-hrs-mon-day">Monday</span><span class="hours-time" id="edit-hrs-mon-time">11:00 AM &ndash; 9:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-tue-day">Tuesday</span><span class="hours-time" id="edit-hrs-tue-time">11:00 AM &ndash; 9:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-wed-day">Wednesday</span><span class="hours-time" id="edit-hrs-wed-time">11:00 AM &ndash; 9:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-thu-day">Thursday</span><span class="hours-time" id="edit-hrs-thu-time">11:00 AM &ndash; 9:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-fri-day">Friday</span><span class="hours-time" id="edit-hrs-fri-time">11:00 AM &ndash; 10:00 PM</span></div>
          <div class="hours-row"><span class="hours-day" id="edit-hrs-sat-day">Saturday</span><span class="hours-time" id="edit-hrs-sat-time">11:00 AM &ndash; 10:00 PM</span></div>
          <div class="hours-row closed"><span class="hours-day" id="edit-hrs-sun-day">Sunday</span><span class="hours-time" id="edit-hrs-sun-time">Closed</span></div>
        </div>

        <h3 style="color: var(--ch-oxblood); margin-top: 36px;" id="edit-hours-music-title">Live music</h3>
        <p id="edit-hours-music-desc">Most nights after 9 PM. See the <a href="music.html">Live Music page</a> for the week's schedule.</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;" id="edit-hours-dinner-music-title">Dinner music</h3>
        <p id="edit-hours-dinner-music-desc">Occasionally - call ahead at (931) 520-2427 if you'd like to know what's playing on a specific night.</p>
      </div>

      <div>
        <span class="eyebrow" id="happy-hour">Happy Hour</span>
        <h2>Every day, 2 PM to 6 PM</h2>
        <div class="card" style="background: var(--ch-oxblood-3); color: var(--ch-cream); border: 1px solid var(--ch-brass);">
          <div style="font-family: var(--font-display); font-size: 2rem; color: var(--ch-brass); margin-bottom: 8px;" id="edit-hh-headline">2pm &ndash; 6pm, daily</div>
          <ul style="padding-left: 20px; color: var(--ch-cream-2); margin-bottom: 0; line-height: 2;">
            <li id="edit-hh-apps"><strong style="color: var(--ch-brass-2);">$7</strong> appetizers</li>
            <li id="edit-hh-drafts"><strong style="color: var(--ch-brass-2);">$2.50</strong> domestic drafts</li>
            <li id="edit-hh-wells"><strong style="color: var(--ch-brass-2);">$4</strong> wells &amp; wine</li>
          </ul>
        </div>

        <h3 style="color: var(--ch-oxblood); margin-top: 36px;" id="edit-hours-late-title">Late-night drink specials</h3>
        <p id="edit-hours-late-desc">Drink specials run every evening from 9 PM until close, in addition to the daily happy hour. Stay for the band, stay for the specials.</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;" id="edit-hours-co-title">Carry-out</h3>
        <p id="edit-hours-co-desc">Available during all open hours. Call (931) 520-2427 to place an order - we'll have it ready when you walk in.</p>
      </div>

    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <span class="eyebrow">Find us</span>
        <h2>On the Cookeville square</h2>
        <p style="font-size: 1.15rem; color: var(--ch-ink-2); margin-bottom: 16px;" id="edit-loc-address">
          14 South Washington Avenue<br/>
          Cookeville, TN 38501
        </p>
        <p><a href="tel:9315202427" style="font-family: var(--font-display); font-size: 1.4rem; color: var(--ch-oxblood);" id="edit-loc-phone">(931) 520-2427</a></p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;" id="edit-loc-dir-title">Directions</h3>
        <p id="edit-loc-dir-desc">From I-40, take exit 287 (TN-136 / Burgess Falls Rd) into Cookeville and follow Washington Avenue to the downtown square. We're on the south side of the square, between West 1st and East Broad.</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;" id="edit-loc-park-title">Parking</h3>
        <p id="edit-loc-park-desc">Free street parking around the square and on the surrounding side streets. There's no dedicated lot - first-come first-served. Friday and Saturday nights fill up fastest.</p>

        <a class="btn btn-oxblood" href="https://maps.google.com/?q=14+South+Washington+Ave+Cookeville+TN+38501" target="_blank" rel="noopener">Open in Google Maps</a>
      </div>
      <div>
        <div style="border-radius: 10px; overflow: hidden; box-shadow: var(--ch-shadow); aspect-ratio: 4 / 3;">
          <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3221.178591097992!2d-85.50112968478241!3d36.16220851105065!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8867226b56c56c17%3A0x7d44cbd30d1530f8!2sCH+Steak+Lounge!5e0!3m2!1sen!2sus!4v1716553200000" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
''' + render_faq_section("hours")


def main_reservations():
    return '''
<section class="hero" style="min-height: 380px;">
  <div class="hero-bg-placeholder"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Reservations</span>
    <h1>
      <span id="edit-rsvp-h1-main">Reserve a table.</span>
      <span class="accent" id="edit-rsvp-h1-accent">We'll save it.</span>
    </h1>
    <p class="hero-lede" id="edit-rsvp-lede">Birthday dinner. Date night. Friday with the band. Anniversary. First date. Tell us when you want it and we'll set you up.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <span class="eyebrow">How it works</span>
        <h2 id="edit-rsvp-how-h2">Quick and simple.</h2>
        <p id="edit-rsvp-how-p1">Fill out the form on the right and we'll confirm by phone or text within an hour during open hours. For parties of 6 or more, please call directly at <a href="tel:9315202427">(931) 520-2427</a> so we can put the right table together.</p>
        <p id="edit-rsvp-how-p2">If you're coming for a specific live-music night, mention the act in the notes - we'll seat you with a view of the stage when we can.</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 32px;" id="edit-rsvp-special-title">Birthdays, anniversaries, work celebrations</h3>
        <p id="edit-rsvp-special-desc">Note the occasion in the form. The kitchen and the team take care of the rest - whether that's a candle in the dessert or just making sure nobody at the table forgets whose night it is.</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;" id="edit-rsvp-private-title">Private events &amp; large parties</h3>
        <p id="edit-rsvp-private-desc">Rehearsal dinners, company holiday parties, retirement dinners - we host them all. Send us the date, the headcount, and what you're celebrating, and we'll put a package together with menu pricing.</p>
      </div>

      <form class="card" onsubmit="event.preventDefault(); alert('Preview only - replace this handler with email-to-host or POS integration (OpenTable / Resy / Yelp Reservations / direct email) at go-live.');" style="background: #fff;">
        <h3 style="margin-bottom: 18px;">Request a reservation</h3>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">First name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Last name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
        </div>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Phone</label>
        <input type="tel" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Email</label>
        <input type="email" style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Date &amp; time</label>
            <input type="datetime-local" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Party size</label>
            <select required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
              <option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7+</option>
            </select>
          </div>
        </div>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Special occasion (optional)</label>
        <select style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
          <option value="">None / just dinner</option>
          <option>Birthday</option>
          <option>Anniversary</option>
          <option>Date night</option>
          <option>Work celebration</option>
          <option>Live music night</option>
          <option>Other</option>
        </select>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Notes (optional)</label>
        <textarea rows="3" placeholder="Allergies, seating preference, the band you're coming to hear..." style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 18px; font-family: inherit; font-size: 0.95rem;"></textarea>

        <button type="submit" class="btn btn-oxblood" style="width: 100%;">Request Reservation</button>

        <p style="font-size: 0.78rem; color: var(--ch-ink-3); margin-top: 12px; margin-bottom: 0;">We'll confirm by phone or text within an hour during open hours.</p>
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
      <span class="accent" id="edit-contact-h1-accent">or just come on by.</span>
    </h1>
    <p class="hero-lede" id="edit-contact-lede">We answer the phone. We answer the form. We're usually here from 11 AM until late.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">

      <div>
        <span class="eyebrow">CH Steak Lounge</span>
        <h2>Reach us</h2>
        <p style="font-size: 1.15rem; color: var(--ch-ink-2);" id="edit-contact-address">
          14 South Washington Avenue<br/>
          Cookeville, TN 38501
        </p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;">Phone</h3>
        <p><a href="tel:9315202427" style="font-size: 1.4rem; font-family: var(--font-display);" id="edit-contact-phone">(931) 520-2427</a></p>
        <p style="color: var(--ch-ink-3); font-size: 0.92rem;" id="edit-contact-phone-note">Call for reservations, carry-out orders, large-party planning, or to confirm tonight's live music.</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;">Hours</h3>
        <p id="edit-contact-hours">Mon&ndash;Thu 11:00 AM &ndash; 9:00 PM<br/>Fri&ndash;Sat 11:00 AM &ndash; 10:00 PM<br/>Sunday: Closed</p>

        <h3 style="color: var(--ch-oxblood); margin-top: 28px;">Follow CH (and Char)</h3>
        <p id="edit-contact-social-note">Our social pages are under our former name "Char" - same restaurant, same kitchen, same management.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
          <li style="margin-bottom: 6px;"><a href="https://www.facebook.com/CharCookeville/" target="_blank" rel="noopener">Facebook (CharCookeville) &rarr;</a></li>
          <li style="margin-bottom: 6px;"><a href="https://twitter.com/charcookeville" target="_blank" rel="noopener">Twitter (charcookeville) &rarr;</a></li>
          <li style="margin-bottom: 6px;"><a href="https://restaurantguru.com/Char-Cookeville" target="_blank" rel="noopener">Restaurant Guru (Char) &rarr;</a></li>
        </ul>

        <a class="btn btn-oxblood" href="https://maps.google.com/?q=14+South+Washington+Ave+Cookeville+TN+38501" target="_blank" rel="noopener" style="margin-top: 24px;">Open in Google Maps</a>
      </div>

      <form class="card" onsubmit="event.preventDefault(); alert('Preview only - wire to email or CRM at go-live.');" style="background: #fff;">
        <h3 style="margin-bottom: 18px;">Send us a message</h3>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">First name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
          <div>
            <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Last name</label>
            <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />
          </div>
        </div>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Email</label>
        <input type="email" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Phone (optional)</label>
        <input type="tel" style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">What can we help with?</label>
        <select style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
          <option>Reservation question</option>
          <option>Carry-out order</option>
          <option>Private event / large party</option>
          <option>Live music booking (band pitch)</option>
          <option>Lost &amp; found</option>
          <option>Feedback / comment</option>
          <option>Other</option>
        </select>

        <label style="display:block; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--ch-ink-3); margin-bottom: 4px;">Message</label>
        <textarea rows="5" required style="width:100%; padding: 10px 12px; border: 1px solid var(--ch-line); border-radius: 4px; margin-bottom: 18px; font-family: inherit; font-size: 0.95rem;"></textarea>

        <button type="submit" class="btn btn-oxblood" style="width: 100%;">Send Message</button>
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
        "title": "CH Steak Lounge - Steakhouse, Bar &amp; Live Music on the Cookeville Square",
        "meta_desc": "CH Steak Lounge is a steakhouse, bar, and live-music venue on the square in Cookeville, TN. Famous smoked wings, hand-cut steaks, Rattlesnake Pasta, daily happy hour, live music most nights after 9 PM.",
        "og_title": "CH Steak Lounge - Cookeville, TN",
        "og_desc": "Steakhouse on the square. Famous smoked wings, hand-cut steaks, Rattlesnake Pasta, full bar, live music most nights.",
        "breadcrumb_items": [("Home", None)],
        "main": main_index,
        "extra_schemas": ["restaurant"],
    },
    "menu": {
        "filename": "menu.html",
        "canonical_path": "menu",
        "title": "Menu - Steaks, Smoked Wings, Pastas &amp; Burgers . CH Steak Lounge",
        "meta_desc": "The CH Steak Lounge menu - hand-cut steaks, hickory-smoked chicken wings, Rattlesnake Pasta, the CH Burger, Pizza Rockafella, salads and sides. Cookeville, TN.",
        "og_title": "Menu - CH Steak Lounge, Cookeville TN",
        "og_desc": "Steaks, smoked wings, Rattlesnake Pasta, Heavenly Seafood Pasta, burgers, salads, sides. Full menu with prices.",
        "breadcrumb_items": [("Home", "index.html"), ("Menu", None)],
        "main": main_menu,
        "extra_schemas": ["restaurant"],  # full Menu schema travels with the Restaurant entity
    },
    "music": {
        "filename": "music.html",
        "canonical_path": "music",
        "title": "Live Music - Most Nights After 9 PM . CH Steak Lounge, Cookeville",
        "meta_desc": "Live music at CH Steak Lounge on the Cookeville square - bluegrass, country, soul, blues, Americana, and open mic. No cover. See this week's full lineup.",
        "og_title": "Live Music at CH Steak Lounge",
        "og_desc": "Live music most nights after 9 PM. No cover. Bluegrass, country, blues, Americana, soul, open mic.",
        "breadcrumb_items": [("Home", "index.html"), ("Live Music", None)],
        "main": main_music,
        "extra_schemas": ["events"],
    },
    "hours": {
        "filename": "hours.html",
        "canonical_path": "hours",
        "title": "Hours, Happy Hour &amp; Location . CH Steak Lounge, Cookeville TN",
        "meta_desc": "CH Steak Lounge is open Mon-Thu 11 AM to 9 PM, Fri-Sat 11 AM to 10 PM, closed Sunday. Happy hour daily 2-6 PM. 14 South Washington Ave on the Cookeville square.",
        "og_title": "Hours &amp; Location - CH Steak Lounge",
        "og_desc": "Open Mon-Sat for lunch, dinner, and the late hours when the music starts. Happy hour every day 2-6 PM.",
        "breadcrumb_items": [("Home", "index.html"), ("Hours &amp; Location", None)],
        "main": main_hours,
        "extra_schemas": ["restaurant"],
    },
    "reservations": {
        "filename": "reservations.html",
        "canonical_path": "reservations",
        "title": "Reservations &amp; Private Events . CH Steak Lounge, Cookeville TN",
        "meta_desc": "Request a reservation at CH Steak Lounge - date nights, birthdays, anniversaries, rehearsal dinners, and large private parties. Reserve online or call (931) 520-2427.",
        "og_title": "Reserve a Table - CH Steak Lounge",
        "og_desc": "Birthday dinner. Date night. Friday with the band. Rehearsal dinner. Reserve online or call (931) 520-2427.",
        "breadcrumb_items": [("Home", "index.html"), ("Reservations", None)],
        "main": main_reservations,
        "extra_schemas": [],
    },
    "contact": {
        "filename": "contact.html",
        "canonical_path": "contact",
        "title": "Contact &amp; Directions . CH Steak Lounge, Cookeville TN",
        "meta_desc": "Contact CH Steak Lounge: 14 South Washington Ave, Cookeville, TN 38501. Call (931) 520-2427 for reservations, carry-out, large parties, or band pitches. Open Mon-Sat.",
        "og_title": "Contact CH Steak Lounge",
        "og_desc": "14 South Washington Ave, Cookeville, TN . (931) 520-2427 . Open Mon-Sat.",
        "breadcrumb_items": [("Home", "index.html"), ("Contact", None)],
        "main": main_contact,
        "extra_schemas": ["restaurant"],
    },
}


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------

def build_schema_block(page_key, page):
    schemas = []
    schemas.append(breadcrumb_schema(page["breadcrumb_items"]))
    schemas.append(faq_schema(FAQS[page_key]))

    for s in page.get("extra_schemas", []):
        if s == "restaurant":
            schemas.append(restaurant_schema())
        elif s == "events":
            # Reference the restaurant too so events tie back to the place
            schemas.append(restaurant_schema())
            for ev in MUSIC_EVENTS:
                schemas.append(event_schema(ev))

    if len(schemas) == 1:
        return json.dumps(schemas[0], indent=2)
    return json.dumps(schemas, indent=2)


def render_page(page_key):
    page = PAGES[page_key]
    template = (BUILD / "template.html").read_text(encoding="utf-8")
    banner   = (BUILD / "banner.html").read_text(encoding="utf-8")
    widget   = (BUILD / "widget.html").read_text(encoding="utf-8")

    main_html = page["main"]()
    crumb = breadcrumb_html(page["breadcrumb_items"]) if len(page["breadcrumb_items"]) > 1 else ""
    schema_json = build_schema_block(page_key, page)

    out = template
    subs = {
        "{{PAGE_TITLE}}":     page["title"],
        "{{META_DESC}}":      page["meta_desc"],
        "{{OG_TITLE}}":       page["og_title"],
        "{{OG_DESC}}":        page["og_desc"],
        "{{CANONICAL_PATH}}": page["canonical_path"],
        "{{SCHEMA_JSON}}":    schema_json,
        "{{BANNER}}":         banner,
        "{{BREADCRUMB}}":     crumb,
        "{{MAIN}}":           main_html,
        "{{WIDGET}}":         widget,
    }
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def main():
    print(f"Building CH Steak Lounge preview -> {OUT}")
    for key, page in PAGES.items():
        html = render_page(key)
        path = OUT / page["filename"]
        path.write_text(html, encoding="utf-8")
        edit_ids = len(re.findall(r'id="edit-', html))
        print(f"  + {page['filename']:24s}  {len(html):>7,} bytes  .  {edit_ids:>2d} edit-* tags")


if __name__ == "__main__":
    main()
