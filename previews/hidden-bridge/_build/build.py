#!/usr/bin/env python3
"""
Hidden Bridge Golf Club — preview builder.

Reads:
  _build/template.html  — page skeleton with {{TOKENS}}
  _build/banner.html    — Relaunch SEO banner (inline)
  _build/widget.html    — Relaunch edit widget (inline)

Emits to previews/hidden-bridge/:
  index.html · course.html · rates.html · membership.html ·
  events.html · proshop.html · contact.html

Per RELAUNCH_OPERATIONS.md Section 4 roadmap — this is the "audit JSON → banner
HTML" generator stub, applied to a full 7-page build.
"""

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "_build"
OUT = ROOT

# ------------------------------------------------------------------------------
# Sitewide facts (verified from prospect_hidden_bridge.md + scorecard image)
# ------------------------------------------------------------------------------

BUSINESS = {
    "name": "Hidden Bridge Golf Club",
    "url": "https://www.hiddenbridgegolf.com",
    "phone": "+1-307-752-6625",
    "phone_display": "307-752-6625",
    "street": "550 Mydland Rd",
    "city": "Sheridan",
    "region": "WY",
    "postal": "82801",
    "country": "US",
    "lat": 44.815,    # approx (Sheridan WY centroid — owner to confirm exact)
    "lng": -106.948,
    "opened_year": 2013,
}

# ------------------------------------------------------------------------------
# Schema builders — emit JSON-LD per page
# ------------------------------------------------------------------------------

def golf_course_schema():
    """Full GolfCourse + LocalBusiness markup — referenced from multiple pages."""
    return {
        "@context": "https://schema.org",
        "@type": ["GolfCourse", "LocalBusiness"],
        "@id": f"{BUSINESS['url']}/#golfcourse",
        "name": BUSINESS["name"],
        "url": BUSINESS["url"],
        "telephone": BUSINESS["phone"],
        "image": f"{BUSINESS['url']}/assets/images/hidden-bridge-2013-034.jpg",
        "logo": f"{BUSINESS['url']}/assets/images/logo.png",
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
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "07:00",
            "closes": "20:00",
            "validFrom": "2026-04-15",
            "validThrough": "2026-10-31",
        }],
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "18 holes", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Par 72",   "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Driving range or practice area", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Pro shop / snack bar",          "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Cart rental",                   "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Event hosting",                 "value": True},
        ],
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Number of Holes", "value": 18},
            {"@type": "PropertyValue", "name": "Par",             "value": 72},
            {"@type": "PropertyValue", "name": "Yardage (Black/Blue tees)",  "value": 6600},
            {"@type": "PropertyValue", "name": "Yardage (Blue/White tees)",  "value": 5877},
            {"@type": "PropertyValue", "name": "Yardage (White/Yellow tees)","value": 5117},
            {"@type": "PropertyValue", "name": "Yardage (Yellow/Red tees)",  "value": 4685},
            {"@type": "PropertyValue", "name": "Course Rating (Men's Black/Blue)",   "value": "71.1"},
            {"@type": "PropertyValue", "name": "Slope Rating (Men's Black/Blue)",    "value": "119"},
            {"@type": "PropertyValue", "name": "Course Rating (Women's White/Yellow)","value": "68.1"},
            {"@type": "PropertyValue", "name": "Slope Rating (Women's White/Yellow)", "value": "118"},
            {"@type": "PropertyValue", "name": "Opened", "value": BUSINESS["opened_year"]},
        ],
        "areaServed": [
            {"@type": "City", "name": "Sheridan"},
            {"@type": "AdministrativeArea", "name": "Sheridan County, Wyoming"},
        ],
        # NOTE: AggregateRating left as a stub — owner should connect Google reviews
        # before publishing. Pulling reviews into structured data is part of the
        # Relaunch live-customer phase.
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


def service_schema(name, desc, page_path):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": desc,
        "provider": {"@type": "GolfCourse", "@id": f"{BUSINESS['url']}/#golfcourse"},
        "areaServed": {"@type": "City", "name": "Sheridan"},
        "url": f"{BUSINESS['url']}/{page_path}",
    }


# ------------------------------------------------------------------------------
# Breadcrumb HTML helper
# ------------------------------------------------------------------------------
def breadcrumb_html(items):
    """items is [(name, path_or_None)]; last item is current (no link)."""
    parts = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1 or path is None:
            parts.append(f'<span aria-current="page">{name}</span>')
        else:
            parts.append(f'<a href="{path}">{name}</a>')
    inner = '<span class="sep">›</span>'.join(parts)
    return f'<div class="breadcrumb"><div class="container">{inner}</div></div>'


# ------------------------------------------------------------------------------
# Sitewide FAQ pool (≥35 questions for AI search citation — Section 3 step 6)
# Split across pages so each contributes ~5 to its own FAQPage schema.
# ------------------------------------------------------------------------------
FAQS = {
    "index": [
        ("Where is Hidden Bridge Golf Club located?",
         "Hidden Bridge Golf Club is at 550 Mydland Road in Sheridan, Wyoming — minutes from downtown Sheridan and the Big Horn Mountains."),
        ("Is Hidden Bridge open to the public?",
         "Yes. Hidden Bridge is a public 18-hole golf course. Members get reserved tee times and reduced fees, but anyone can play."),
        ("How long is Hidden Bridge Golf Club?",
         "The course plays 4,685 yards from the forward tees up to 6,600 yards from the championship tees, with par 72 across all sets."),
        ("When did Hidden Bridge Golf Club open?",
         "Hidden Bridge opened in 2013 and has served Sheridan-area golfers, families, and visitors every season since."),
        ("Can I host a tournament or event at Hidden Bridge?",
         "Yes. We host scrambles, charity tournaments, family reunions, and corporate outings. See the Tournaments &amp; Events page for details."),
    ],
    "course": [
        ("What is the course rating and slope at Hidden Bridge?",
         "From the Men's Black/Blue tees the course rating is 71.1 with a slope of 119. From the Women's White/Yellow tees the rating is 68.1 with a slope of 118."),
        ("How many tee sets does Hidden Bridge have?",
         "Hidden Bridge has four tee sets: Black/Blue (6,600 yards), Blue/White (5,877), White/Yellow (5,117), and Yellow/Red (4,685)."),
        ("Is Hidden Bridge a links-style or parkland course?",
         "Hidden Bridge plays through rolling prairie with water on the back nine and big views of the Big Horn Mountains — closer to a high-plains layout than a traditional parkland."),
        ("Are there water hazards on the course?",
         "Yes. Several holes feature water — most notably the lake on the back nine that catches the Big Horn reflection at sunset."),
        ("What are the on-course distance markers?",
         "Fairway distance stakes are marked: Blue = 200 yards, White = 150, Red = 100, Yellow = 50 — all measured to the center of the green."),
    ],
    "rates": [
        ("How much is a round at Hidden Bridge Golf Club?",
         "Daily green fees, 9-hole rates, junior and senior pricing, and cart rentals are listed on the Rates page. Please confirm 2026-season rates by phone before booking."),
        ("Can I book a tee time online?",
         "Yes — use the tee-time request form on the Rates page or call 307-752-6625. We'll confirm by phone within an hour during operating hours."),
        ("Do you offer season passes?",
         "Yes. Individual, family, and junior season passes are available. See the Membership page or call the course for current pricing."),
        ("What are the cart rental rates?",
         "Walking carts and motorized carts are available. Rates are listed on the Rates page — call the pro shop with questions."),
        ("Do you accept walk-ups?",
         "Walk-ups are welcome when the tee sheet allows. Calling ahead is the best way to guarantee your preferred time."),
    ],
    "membership": [
        ("What does a Hidden Bridge membership include?",
         "Annual members receive unlimited green fees, advance tee-time booking, discounted cart rentals, and member-only event access."),
        ("Is there a family membership option?",
         "Yes — family memberships cover the primary member, spouse, and dependent juniors under 18. See the Membership page for details."),
        ("Are there junior memberships?",
         "Yes. Discounted junior memberships are available for golfers under 18 and student golfers. Contact the course to apply."),
        ("Can members reserve tee times in advance?",
         "Members can reserve tee times further in advance than the public — exact lead times are listed on the Membership page."),
        ("How do I apply for membership?",
         "Membership applications are available at the course and can be requested through the form on the Membership page."),
    ],
    "events": [
        ("Can I host a wedding or private event at Hidden Bridge?",
         "Yes. The course hosts weddings, family reunions, charity events, and corporate outings. Contact us for available dates and packages."),
        ("Does Hidden Bridge run weekly leagues?",
         "Yes — recurring leagues run through the season. Check the Tournaments &amp; Events page for current schedules and to join."),
        ("How do I sign up a team for a tournament?",
         "Team sign-up information for each scheduled tournament is posted on the Tournaments &amp; Events page. Calling the course is the fastest way to register."),
        ("Do you run charity tournaments?",
         "Yes. Hidden Bridge regularly hosts charity scrambles for local Sheridan organizations. Contact us to discuss hosting one."),
        ("Is the course closed during private events?",
         "Most events use a shotgun or block of holes — the course remains open in most cases. Call the pro shop for the day's status."),
    ],
    "proshop": [
        ("What does the pro shop sell?",
         "The pro shop carries soft drinks, Gatorade, beer and mixed drinks, snacks, and basic golf accessories. Hidden Bridge keeps the pricing reasonable."),
        ("Can I rent clubs or a cart?",
         "Yes — both pull carts and motorized carts are available, and basic club rentals can be arranged. Call ahead for availability."),
        ("Do you offer lessons or clinics?",
         "Lesson availability varies by season. Contact the course to inquire about current instructor schedules and clinic dates."),
        ("Is there a driving range or practice area?",
         "Yes — a practice area is available for warm-up. Hours and access are posted at the pro shop."),
        ("Can I buy a Hidden Bridge gift card?",
         "Yes. Gift cards are available at the pro shop — call to purchase by phone."),
    ],
    "contact": [
        ("What is the phone number for Hidden Bridge Golf Club?",
         "Hidden Bridge Golf Club can be reached at 307-752-6625."),
        ("When is Hidden Bridge open?",
         "The course is open daily during the 2026 season, typically from mid-April through October — weather permitting."),
        ("How do I get to Hidden Bridge from downtown Sheridan?",
         "Hidden Bridge is at 550 Mydland Road, minutes from downtown Sheridan. From I-90 take the Sheridan exit and follow Mydland — the course is on the west side of town."),
        ("Is the course near the Big Horn Mountains?",
         "Yes. Hidden Bridge sits at the foot of the Big Horns — the mountains form the backdrop of most holes on the back nine."),
        ("Is there a dress code at Hidden Bridge?",
         "Hidden Bridge keeps things friendly — proper golf attire is appreciated. Call the pro shop with specific questions before you visit."),
    ],
}


# ------------------------------------------------------------------------------
# PAGE MAIN-CONTENT GENERATORS
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
        <h2>Questions golfers ask before they visit</h2>
        <div style="max-width: 820px;">
          {rows}
        </div>
      </div>
    </section>'''


def main_index():
    return '''
<section class="hero">
  <img src="assets/images/hidden-bridge-2013-034.jpg" alt="Hidden Bridge Golf Club fairway and lake with Big Horn Mountains behind" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline" id="edit-hero-tagline">Sheridan, Wyoming · Since 2013</span>
    <h1>
      <span id="edit-hero-h1-main">It's a great day</span>
      <span class="accent" id="edit-hero-h1-accent">to play.</span>
    </h1>
    <p class="hero-lede" id="edit-hero-lede">A friendly 18-hole public course at the foot of the Big Horns — par 72, water on the back nine, sunsets people drive out to see.</p>
    <div class="hero-ctas">
      <a href="rates.html#tee-time-form" class="btn btn-primary">Request a Tee Time</a>
      <a href="course.html" class="btn btn-ghost">See the Course</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="stats">
      <div class="stat"><div class="stat-num">18</div><div class="stat-label">Holes</div></div>
      <div class="stat"><div class="stat-num">72</div><div class="stat-label">Par</div></div>
      <div class="stat"><div class="stat-num">6,600</div><div class="stat-label">Yards (tips)</div></div>
      <div class="stat"><div class="stat-num">2013</div><div class="stat-label">Opened</div></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid grid-2" style="align-items: center;">
      <div>
        <span class="eyebrow">About Hidden Bridge</span>
        <h2 id="edit-mission-h2">Friendly, no-pressure golf at the foot of the Big Horns.</h2>
        <p id="edit-mission-p1">Since 2013, Hidden Bridge Golf Club has served Sheridan-area families with affordable golf for every level of play. We're the place you bring the kids, the in-laws, the work crew — and the place you come back to alone at sunset.</p>
        <p id="edit-mission-p2">With water on the back nine and a view of the Big Horn Mountains from most holes, Hidden Bridge is built for a great walk, a great social round, and a course you'll actually finish in under five hours.</p>
        <a href="course.html" class="btn btn-maroon">Explore the Course</a>
      </div>
      <div>
        <img src="assets/images/from-bridge.jpg" alt="View from Hidden Bridge across the prairie wetland and natural cattails" style="border-radius: 10px; box-shadow: 0 12px 32px rgba(28, 22, 18, 0.18);" />
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">What you'll find here</span>
    <h2>Everything a Sheridan round needs</h2>
    <p class="section-lede">Six ways to spend a day at Hidden Bridge — from a quick nine on your lunch break to a full club tournament.</p>
    <div class="grid grid-3">

      <a href="course.html" class="card" style="text-decoration: none; color: inherit;">
        <div class="card-img"><img src="assets/images/hidden-bridge-wy-3-13.jpg" alt="Hidden Bridge scorecard with tee sets and yardages" /></div>
        <span class="card-icon">⛳</span>
        <h3 id="edit-svc-course-title">The Course</h3>
        <p id="edit-svc-course-desc">18 holes, par 72, four tee sets from 4,685 to 6,600 yards. See the scorecard, hole-by-hole, and local rules.</p>
      </a>

      <a href="rates.html" class="card" style="text-decoration: none; color: inherit;">
        <div class="card-img"><img src="assets/images/golfing-couple.jpg" alt="Golfers walking the fairway at Hidden Bridge" /></div>
        <span class="card-icon">$</span>
        <h3 id="edit-svc-rates-title">Rates &amp; Tee Times</h3>
        <p id="edit-svc-rates-desc">Daily green fees, 9-hole rates, cart rentals, and season passes. Request a tee time online.</p>
      </a>

      <a href="membership.html" class="card" style="text-decoration: none; color: inherit;">
        <div class="card-img"><img src="assets/images/hidden-bridge-2013-034.jpg" alt="Mountain view across Hidden Bridge fairway" /></div>
        <span class="card-icon">★</span>
        <h3 id="edit-svc-membership-title">Membership</h3>
        <p id="edit-svc-membership-desc">Individual, family, and junior memberships. Reserved tee times, member events, and unlimited play.</p>
      </a>

      <a href="events.html" class="card" style="text-decoration: none; color: inherit;">
        <div class="card-img"><img src="assets/images/sunset.jpg" alt="Sunset over Hidden Bridge with a golf cart on the fairway" /></div>
        <span class="card-icon">⚑</span>
        <h3 id="edit-svc-events-title">Tournaments &amp; Events</h3>
        <p id="edit-svc-events-desc">Weekly leagues, charity scrambles, weddings, corporate outings, and family reunions on the course.</p>
      </a>

      <a href="proshop.html" class="card" style="text-decoration: none; color: inherit;">
        <div class="card-img"><img src="assets/images/hidden-bridge-2013-034.jpg" alt="Hidden Bridge pro shop and clubhouse area" /></div>
        <span class="card-icon">🛍</span>
        <h3 id="edit-svc-proshop-title">Pro Shop</h3>
        <p id="edit-svc-proshop-desc">Drinks, snacks, cart rentals, gift cards, and golf basics. Stop in before the round.</p>
      </a>

      <a href="contact.html" class="card" style="text-decoration: none; color: inherit;">
        <div class="card-img"><img src="assets/images/from-bridge.jpg" alt="Hidden Bridge course view across the prairie" /></div>
        <span class="card-icon">↗</span>
        <h3 id="edit-svc-contact-title">Visit &amp; Contact</h3>
        <p id="edit-svc-contact-desc">Hours, directions from downtown Sheridan, parking, and the contact form.</p>
      </a>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="quote">
      <span id="edit-quote-text">A real Sheridan course at a real Sheridan price. The Big Horn view from the back nine is worth the round on its own.</span>
      <span class="quote-attr" id="edit-quote-attr">— a Sheridan local · placeholder, replace with a real Google review when you connect reviews</span>
    </div>
  </div>
</section>
''' + render_faq_section("index")


def main_course():
    return '''
<section class="hero" style="min-height: 420px;">
  <img src="assets/images/hidden-bridge-2013-034.jpg" alt="Hidden Bridge fairway with Big Horn Mountains behind" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">The Course</span>
    <h1>
      <span id="edit-course-h1-main">Par 72.</span>
      <span class="accent" id="edit-course-h1-accent">Wyoming sky.</span>
    </h1>
    <p class="hero-lede" id="edit-course-lede">Four tee sets from 4,685 to 6,600 yards, water on the back nine, and a view of the Big Horns from nearly every hole.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Scorecard</span>
    <h2>Yardage and ratings</h2>
    <p class="section-lede">Four tee sets so every golfer in the group plays the course that fits them. Par 72 across all sets.</p>

    <div style="overflow-x: auto;">
      <table class="scorecard">
        <thead>
          <tr>
            <th>Tees</th>
            <th>Front 9</th>
            <th>Back 9</th>
            <th>Total Yardage</th>
            <th>Par</th>
            <th>Rating / Slope</th>
          </tr>
        </thead>
        <tbody>
          <tr><td class="tee-black">Black/Blue</td><td id="edit-tee-blackblue-front">3,406</td><td id="edit-tee-blackblue-back">3,194</td><td><strong>6,600</strong></td><td>72</td><td id="edit-tee-blackblue-rating">71.1 / 119 (M)</td></tr>
          <tr><td class="tee-blue">Blue/White</td><td id="edit-tee-bluewhite-front">3,029</td><td id="edit-tee-bluewhite-back">2,848</td><td><strong>5,877</strong></td><td>72</td><td id="edit-tee-bluewhite-rating">—</td></tr>
          <tr><td class="tee-white">White/Yellow</td><td id="edit-tee-whiteyellow-front">2,693</td><td id="edit-tee-whiteyellow-back">2,424</td><td><strong>5,117</strong></td><td>72</td><td id="edit-tee-whiteyellow-rating">68.1 / 118 (W)</td></tr>
          <tr><td class="tee-yellow">Yellow/Red</td><td id="edit-tee-yellowred-front">2,424</td><td id="edit-tee-yellowred-back">2,261</td><td><strong>4,685</strong></td><td>72</td><td id="edit-tee-yellowred-rating">—</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size: 0.85rem; color: var(--hb-ink-3); margin-top: 14px;">Front/back yardage splits are estimated from the published scorecard total. Confirm exact hole-by-hole numbers with the pro shop before publishing.</p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid grid-2" style="align-items: start; gap: 36px;">
      <div>
        <span class="eyebrow">Course Map</span>
        <h2>The layout</h2>
        <p>Hidden Bridge plays through rolling prairie with the Big Horn Mountains as a constant backdrop. Water comes into play on the back nine, and several short par-4s reward placement over distance.</p>
        <p>The course is walkable end-to-end — most rounds finish in 4 to 4.5 hours.</p>
      </div>
      <div>
        <img src="assets/images/hidden-bridge-wy-3-132.jpg" alt="Hidden Bridge course layout and local rules" style="border-radius: 10px; box-shadow: 0 12px 32px rgba(28, 22, 18, 0.18); width: 100%;" />
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Local Rules</span>
    <h2>What you need to know before you tee off</h2>
    <div class="grid grid-2" style="max-width: 920px;">
      <div class="card">
        <h3>Out of bounds &amp; hazards</h3>
        <ul style="margin: 0; padding-left: 20px; color: var(--hb-ink-2);">
          <li id="edit-rules-ob">White stakes and fences bordering the course are out of bounds.</li>
          <li id="edit-rules-hazards">Hazards are defined by yellow and red stakes or lines.</li>
          <li id="edit-rules-gur">Painted white lines or rope are ground under repair.</li>
          <li id="edit-rules-trees">Free drop from all staked or marked trees.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Distance markers</h3>
        <ul style="margin: 0; padding-left: 20px; color: var(--hb-ink-2);">
          <li id="edit-marker-blue"><strong>Blue stake:</strong> 200 yards to center of green</li>
          <li id="edit-marker-white"><strong>White stake:</strong> 150 yards</li>
          <li id="edit-marker-red"><strong>Red stake:</strong> 100 yards</li>
          <li id="edit-marker-yellow"><strong>Yellow stake:</strong> 50 yards</li>
        </ul>
      </div>
      <div class="card">
        <h3>Pace &amp; etiquette</h3>
        <ul style="margin: 0; padding-left: 20px; color: var(--hb-ink-2);">
          <li id="edit-etiquette-marks">Please repair all ball marks and replace all divots.</li>
          <li id="edit-etiquette-attire">Proper golf attire must be worn at all times.</li>
          <li id="edit-etiquette-carts">Keep carts at least 30 feet from all greens and tees.</li>
          <li id="edit-etiquette-fence">All protective fences near tee boxes are immovable obstructions.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Quick facts</h3>
        <ul style="margin: 0; padding-left: 20px; color: var(--hb-ink-2);">
          <li>18 holes · Par 72</li>
          <li>4 tee sets · 4,685 to 6,600 yards</li>
          <li>Opened 2013</li>
          <li>Walkable layout — 4 to 4.5 hour rounds</li>
        </ul>
      </div>
    </div>
  </div>
</section>
''' + render_faq_section("course")


def main_rates():
    return '''
<section class="hero" style="min-height: 360px;">
  <img src="assets/images/golfing-couple.jpg" alt="Golfers on the Hidden Bridge fairway" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Rates &amp; Tee Times</span>
    <h1>
      <span id="edit-rates-h1-main">Sheridan-priced golf,</span>
      <span class="accent" id="edit-rates-h1-accent">no surprises.</span>
    </h1>
    <p class="hero-lede" id="edit-rates-lede">Walk-on or call ahead. Use the form below and we'll confirm your tee time by phone.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">2026 Season Rates</span>
    <h2>Green fees</h2>
    <p class="section-lede">Same rates 7 days a week. Carts and pull carts are extra. Junior and senior pricing available — call the pro shop with questions.</p>

    <table class="rates-table" style="margin-bottom: 28px;">
      <thead>
        <tr><th>Round</th><th style="text-align:right;">Rate</th><th>Notes</th></tr>
      </thead>
      <tbody>
        <tr><td>18 Holes (Adult)</td><td class="rate" style="text-align:right;" id="edit-rate-18-adult">$38</td><td id="edit-rate-18-adult-note">Walking, all day, no time restrictions</td></tr>
        <tr><td>9 Holes (Adult)</td><td class="rate" style="text-align:right;" id="edit-rate-9-adult">$22</td><td id="edit-rate-9-adult-note">Front or back, your choice</td></tr>
        <tr><td>18 Holes (Junior, under 18)</td><td class="rate" style="text-align:right;" id="edit-rate-18-junior">$18</td><td id="edit-rate-18-junior-note">Bring 'em out — golf grows here</td></tr>
        <tr><td>18 Holes (Senior, 65+)</td><td class="rate" style="text-align:right;" id="edit-rate-18-senior">$30</td><td id="edit-rate-18-senior-note">Weekdays</td></tr>
        <tr><td>Twilight (after 4pm)</td><td class="rate" style="text-align:right;" id="edit-rate-twilight">$22</td><td id="edit-rate-twilight-note">Until close — chase the sunset</td></tr>
        <tr><td>Cart (18 holes, per rider)</td><td class="rate" style="text-align:right;" id="edit-rate-cart-18">$16</td><td id="edit-rate-cart-18-note">Motorized · advance reserve recommended</td></tr>
        <tr><td>Pull Cart</td><td class="rate" style="text-align:right;" id="edit-rate-pullcart">$5</td><td id="edit-rate-pullcart-note">Always available walk-up</td></tr>
      </tbody>
    </table>

    <div class="card" style="background: var(--hb-cream); border-color: var(--hb-gold); border-width: 1px;">
      <p style="margin: 0; color: var(--hb-ink-2);"><strong>Rates pending owner confirmation.</strong> The numbers above match typical Sheridan-area public-course pricing and are placeholders for the Relaunch preview — confirm 2026 rates with the pro shop before publishing. Edit any number by clicking the chat button and saying e.g. <em>"change the 18-hole adult rate to $42"</em>.</p>
    </div>
  </div>
</section>

<section class="section alt" id="tee-time-form">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <span class="eyebrow">Tee Time Request</span>
        <h2 id="edit-tt-form-h2">Tell us when you'd like to play.</h2>
        <p id="edit-tt-form-lede">We'll confirm your tee time by phone within an hour during operating hours. For groups of 8 or more, call the pro shop direct at 307-752-6625.</p>
        <p>If you're a member, advance booking lead times are listed on the <a href="membership.html">Membership page</a>.</p>
      </div>
      <form class="card" onsubmit="event.preventDefault(); alert('Preview only — replace this handler with your booking integration (foreUP / GolfNow / Chronogolf) at go-live.');" style="background: #fff;">
        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Name</label>
        <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Phone</label>
        <input type="tel" required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Date &amp; time</label>
        <input type="datetime-local" required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Players</label>
        <select required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
          <option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option>
        </select>

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Notes (optional)</label>
        <textarea rows="3" style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 18px; font-family: inherit; font-size: 0.95rem;"></textarea>

        <button type="submit" class="btn btn-maroon" style="width: 100%;">Send Request</button>
      </form>
    </div>
  </div>
</section>
''' + render_faq_section("rates")


def main_membership():
    return '''
<section class="hero" style="min-height: 360px;">
  <img src="assets/images/sunset.jpg" alt="Sunset at Hidden Bridge Golf Club" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Membership</span>
    <h1>
      <span id="edit-mbr-h1-main">Play all season.</span>
      <span class="accent" id="edit-mbr-h1-accent">It's that simple.</span>
    </h1>
    <p class="hero-lede" id="edit-mbr-lede">Unlimited rounds, advance tee-time booking, member events, and a course you'll start calling "yours" by mid-summer.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">2026 Season Memberships</span>
    <h2>Pick your tier</h2>
    <div class="grid grid-3">

      <div class="card">
        <span class="eyebrow">Junior</span>
        <h3 id="edit-mbr-junior-title">Junior</h3>
        <div class="stat-num" style="color: var(--hb-maroon); font-size: 2rem;" id="edit-mbr-junior-price">$250</div>
        <p style="font-size: 0.78rem; color: var(--hb-ink-3); margin-bottom: 14px;">per season · golfers under 18</p>
        <ul style="padding-left: 20px; color: var(--hb-ink-2); margin-bottom: 18px;">
          <li>Unlimited play, season-long</li>
          <li>Free range / practice access</li>
          <li>Invite to junior clinics</li>
          <li>Standard tee-time booking window</li>
        </ul>
        <a href="contact.html" class="btn btn-ghost" style="color: var(--hb-maroon) !important; border-color: var(--hb-maroon);">Apply →</a>
      </div>

      <div class="card" style="border: 2px solid var(--hb-gold); position: relative;">
        <div style="position: absolute; top: -12px; right: 20px; background: var(--hb-gold); color: var(--hb-ink); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 4px 10px; border-radius: 3px;">Most popular</div>
        <span class="eyebrow">Individual</span>
        <h3 id="edit-mbr-individual-title">Individual</h3>
        <div class="stat-num" style="color: var(--hb-maroon); font-size: 2rem;" id="edit-mbr-individual-price">$850</div>
        <p style="font-size: 0.78rem; color: var(--hb-ink-3); margin-bottom: 14px;">per season · single adult</p>
        <ul style="padding-left: 20px; color: var(--hb-ink-2); margin-bottom: 18px;">
          <li>Unlimited play, 7 days a week</li>
          <li>14-day advance tee-time booking</li>
          <li>20% off cart rentals</li>
          <li>Member-only event access</li>
          <li>Free range / practice access</li>
        </ul>
        <a href="contact.html" class="btn btn-maroon">Apply →</a>
      </div>

      <div class="card">
        <span class="eyebrow">Family</span>
        <h3 id="edit-mbr-family-title">Family</h3>
        <div class="stat-num" style="color: var(--hb-maroon); font-size: 2rem;" id="edit-mbr-family-price">$1,400</div>
        <p style="font-size: 0.78rem; color: var(--hb-ink-3); margin-bottom: 14px;">per season · 2 adults + juniors</p>
        <ul style="padding-left: 20px; color: var(--hb-ink-2); margin-bottom: 18px;">
          <li>Unlimited play for all members</li>
          <li>Includes dependent juniors under 18</li>
          <li>14-day advance booking</li>
          <li>20% off cart rentals</li>
          <li>Member-only event access</li>
        </ul>
        <a href="contact.html" class="btn btn-ghost" style="color: var(--hb-maroon) !important; border-color: var(--hb-maroon);">Apply →</a>
      </div>
    </div>

    <div class="card" style="background: var(--hb-cream); border-color: var(--hb-gold); margin-top: 32px;">
      <p style="margin: 0; color: var(--hb-ink-2);"><strong>Membership pricing pending owner confirmation.</strong> The numbers above are placeholders sized for Sheridan-area public courses. Confirm 2026 rates with the pro shop, then edit any number through the chat — e.g. <em>"set the individual membership to $895"</em>.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <span class="eyebrow">What's included</span>
    <h2>What membership means at Hidden Bridge</h2>
    <div class="grid grid-3">
      <div>
        <h3 style="color: var(--hb-maroon);">Play all season</h3>
        <p>Unlimited 18-hole and 9-hole rounds, no per-round green fee, weekdays or weekends. Walk on or call ahead.</p>
      </div>
      <div>
        <h3 style="color: var(--hb-maroon);">Reserved tee times</h3>
        <p>Members can book up to 14 days in advance. The public window is 7 days — members get the prime weekend morning slots.</p>
      </div>
      <div>
        <h3 style="color: var(--hb-maroon);">Member-only events</h3>
        <p>Member-guest tournaments, weekly leagues, end-of-season banquet, and member-pricing on private events.</p>
      </div>
    </div>
  </div>
</section>
''' + render_faq_section("membership")


def main_events():
    return '''
<section class="hero" style="min-height: 360px;">
  <img src="assets/images/from-bridge.jpg" alt="Hidden Bridge prairie wetland view" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Tournaments &amp; Events</span>
    <h1>
      <span id="edit-evt-h1-main">Bring the team.</span>
      <span class="accent" id="edit-evt-h1-accent">Bring the whole family.</span>
    </h1>
    <p class="hero-lede" id="edit-evt-lede">Charity scrambles, weekly leagues, weddings, reunions, and corporate outings — Hidden Bridge runs them all.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">What we host</span>
    <h2>Three kinds of events</h2>
    <div class="grid grid-3">
      <div class="card">
        <span class="card-icon">⛳</span>
        <h3 id="edit-evt-tournaments-title">Tournaments &amp; Scrambles</h3>
        <p id="edit-evt-tournaments-desc">Charity scrambles, member-guest events, club championships, and corporate tournaments. Shotgun or tee-time formats — your call.</p>
      </div>
      <div class="card">
        <span class="card-icon">⚑</span>
        <h3 id="edit-evt-leagues-title">Weekly Leagues</h3>
        <p id="edit-evt-leagues-desc">Men's, women's, mixed, and senior leagues run through the season. Drop in or commit to a full slate — it's friendly competition either way.</p>
      </div>
      <div class="card">
        <span class="card-icon">♥</span>
        <h3 id="edit-evt-private-title">Weddings, Reunions, Corporate</h3>
        <p id="edit-evt-private-desc">Big Horn views make for a memorable backdrop. We host weddings, family reunions, work social events, and end-of-quarter team days.</p>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <span class="eyebrow">2026 Schedule</span>
    <h2>Upcoming tournaments &amp; leagues</h2>
    <p class="section-lede">Sign-up is via the pro shop — call 307-752-6625 or use the contact form. Final dates may shift with weather.</p>

    <table class="rates-table">
      <thead>
        <tr><th>Event</th><th>Date</th><th>Format</th><th>Sign-up</th></tr>
      </thead>
      <tbody>
        <tr>
          <td id="edit-evt-1-name">Opening Day Scramble</td>
          <td id="edit-evt-1-date">Sat, May 2 · 2026</td>
          <td id="edit-evt-1-format">4-person scramble, shotgun start</td>
          <td><a href="contact.html">Sign up →</a></td>
        </tr>
        <tr>
          <td id="edit-evt-2-name">Wednesday Night Men's League</td>
          <td id="edit-evt-2-date">Every Wed, May–Aug</td>
          <td id="edit-evt-2-format">9-hole league, 5:30 tee time</td>
          <td><a href="contact.html">Sign up →</a></td>
        </tr>
        <tr>
          <td id="edit-evt-3-name">Thursday Women's League</td>
          <td id="edit-evt-3-date">Every Thu, May–Aug</td>
          <td id="edit-evt-3-format">9-hole league, 5:30 tee time</td>
          <td><a href="contact.html">Sign up →</a></td>
        </tr>
        <tr>
          <td id="edit-evt-4-name">Hidden Bridge Member-Guest</td>
          <td id="edit-evt-4-date">Sat–Sun, Jul 11–12</td>
          <td id="edit-evt-4-format">Two-day tournament, members + invited guest</td>
          <td><a href="contact.html">Sign up →</a></td>
        </tr>
        <tr>
          <td id="edit-evt-5-name">Club Championship</td>
          <td id="edit-evt-5-date">Sat–Sun, Aug 22–23</td>
          <td id="edit-evt-5-format">36-hole stroke play, members</td>
          <td><a href="contact.html">Sign up →</a></td>
        </tr>
        <tr>
          <td id="edit-evt-6-name">Sheridan Charity Open</td>
          <td id="edit-evt-6-date">Sat, Sep 12</td>
          <td id="edit-evt-6-format">4-person scramble, public, charity beneficiary TBA</td>
          <td><a href="contact.html">Sign up →</a></td>
        </tr>
      </tbody>
    </table>

    <div class="card" style="background: var(--hb-cream); border-color: var(--hb-gold); margin-top: 28px;">
      <p style="margin: 0; color: var(--hb-ink-2);"><strong>Tournament calendar pending owner confirmation.</strong> The events above match typical small-club calendars — replace dates and event names with the real 2026 slate. Edit through chat: <em>"change Opening Day to April 25"</em>.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Private events</span>
    <h2>Hosting at Hidden Bridge</h2>
    <div class="grid grid-2">
      <div>
        <p>The course is open for weddings, rehearsal dinners, family reunions, corporate team days, charity tournaments, and end-of-quarter celebrations. With the Big Horn Mountains as a backdrop and the lake on the back nine, the property photographs as well as it plays.</p>
        <p>Standard packages include course rental, cart use, the pro shop's drink and snack menu, and on-course event support. Custom catering and bar service available — talk to us.</p>
        <a href="contact.html" class="btn btn-maroon">Talk to us about your event</a>
      </div>
      <div>
        <img src="assets/images/sunset.jpg" alt="Sunset at Hidden Bridge — golf cart on the fairway" style="border-radius: 10px; box-shadow: 0 12px 32px rgba(28, 22, 18, 0.18); width: 100%;" />
      </div>
    </div>
  </div>
</section>
''' + render_faq_section("events")


def main_proshop():
    return '''
<section class="hero" style="min-height: 340px;">
  <img src="assets/images/golfing-couple.jpg" alt="Hidden Bridge golfers" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Pro Shop</span>
    <h1>
      <span id="edit-shop-h1-main">Before the round.</span>
      <span class="accent" id="edit-shop-h1-accent">After the round.</span>
    </h1>
    <p class="hero-lede" id="edit-shop-lede">Drinks, snacks, rentals, gift cards, and golf basics — at reasonable prices.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">What's in the shop</span>
    <h2>Stocked for a day on the course</h2>

    <div class="grid grid-2">
      <div>
        <h3 style="color: var(--hb-maroon);">Snacks &amp; drinks</h3>
        <p id="edit-shop-snacks">Soft drinks, Gatorade, beer, and mixed drinks. Chips, candy, and other sweet and savory snack options. Reasonable prices — bring cash or card.</p>

        <h3 style="color: var(--hb-maroon); margin-top: 32px;">Cart &amp; rental</h3>
        <p id="edit-shop-rentals">Motorized cart rental, pull carts, and basic club rental are all available. Call ahead for cart reservations on weekend mornings — they go fast in peak season.</p>

        <h3 style="color: var(--hb-maroon); margin-top: 32px;">Gift cards</h3>
        <p id="edit-shop-gifts">A Hidden Bridge gift card covers green fees, cart rental, snacks, and a season pass — call the pro shop to purchase by phone.</p>
      </div>
      <div>
        <img src="assets/images/hidden-bridge-2013-034.jpg" alt="Hidden Bridge course view" style="border-radius: 10px; box-shadow: 0 12px 32px rgba(28, 22, 18, 0.18); width: 100%;" />
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <span class="eyebrow">Lessons &amp; instruction</span>
    <h2 id="edit-lessons-h2">Lessons by appointment</h2>
    <div class="grid grid-2" style="align-items: start;">
      <div>
        <p id="edit-lessons-p1">Hidden Bridge offers individual lessons and group clinics through the season. Instructor availability shifts — call the pro shop for current openings.</p>
        <p id="edit-lessons-p2">Junior clinics run on weekday mornings during the summer and are open to non-members. Bring 'em out — golf grows here.</p>
        <a href="contact.html" class="btn btn-maroon">Ask about lessons</a>
      </div>
      <div class="card">
        <h3>What's typically offered</h3>
        <ul style="padding-left: 20px; color: var(--hb-ink-2); margin-bottom: 0;">
          <li id="edit-lessons-item1">Individual lessons (30 or 60 minutes)</li>
          <li id="edit-lessons-item2">Group lessons (2–4 golfers)</li>
          <li id="edit-lessons-item3">Junior summer clinics</li>
          <li id="edit-lessons-item4">Pre-tournament short-game tune-ups</li>
        </ul>
      </div>
    </div>
  </div>
</section>
''' + render_faq_section("proshop")


def main_contact():
    return '''
<section class="hero" style="min-height: 340px;">
  <img src="assets/images/from-bridge.jpg" alt="Hidden Bridge prairie view" class="hero-img" />
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <span class="hero-tagline">Contact</span>
    <h1>
      <span id="edit-contact-h1-main">Find us,</span>
      <span class="accent" id="edit-contact-h1-accent">call us, come see us.</span>
    </h1>
    <p class="hero-lede" id="edit-contact-lede">Minutes from downtown Sheridan, on Mydland Road. Open daily through the 2026 season.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items: start;">

      <div>
        <span class="eyebrow">Visit</span>
        <h2>Hidden Bridge Golf Club</h2>
        <p style="font-size: 1.1rem; color: var(--hb-ink-2);" id="edit-contact-address">
          550 Mydland Road<br/>
          Sheridan, WY 82801
        </p>

        <h3 style="color: var(--hb-maroon); margin-top: 28px;">Hours</h3>
        <p id="edit-contact-hours">Open daily, dawn until dusk, mid-April through October. Hours vary by season and weather — call ahead.</p>

        <h3 style="color: var(--hb-maroon); margin-top: 28px;">Phone</h3>
        <p><a href="tel:3077526625" style="font-size: 1.3rem; font-family: var(--font-display);" id="edit-contact-phone">307-752-6625</a></p>

        <h3 style="color: var(--hb-maroon); margin-top: 28px;">Directions</h3>
        <p id="edit-contact-directions">From I-90, take the Sheridan exit and follow Coffeen Avenue into town. Mydland Road runs west — the course is on the west side of Sheridan, about 5 minutes from downtown.</p>
        <a class="btn btn-maroon" href="https://maps.google.com/?q=550+Mydland+Rd+Sheridan+WY+82801" target="_blank" rel="noopener">Open in Google Maps</a>
      </div>

      <form class="card" onsubmit="event.preventDefault(); alert('Preview only — wire up form submission to the email or CRM integration of your choice at go-live.');" style="background: #fff;">
        <h3 style="margin-bottom: 18px;">Send us a message</h3>

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Name</label>
        <input type="text" required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Email</label>
        <input type="email" required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Phone (optional)</label>
        <input type="tel" style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;" />

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">What can we help with?</label>
        <select style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 14px; font-family: inherit; font-size: 0.95rem;">
          <option>Tee time question</option>
          <option>Membership inquiry</option>
          <option>Tournament or event</option>
          <option>Wedding / private event</option>
          <option>Lessons</option>
          <option>Other</option>
        </select>

        <label style="display:block; font-size:0.8rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; color: var(--hb-ink-3); margin-bottom: 4px;">Message</label>
        <textarea rows="5" required style="width:100%; padding: 10px 12px; border: 1px solid var(--hb-line); border-radius: 4px; margin-bottom: 18px; font-family: inherit; font-size: 0.95rem;"></textarea>

        <button type="submit" class="btn btn-maroon" style="width: 100%;">Send Message</button>
      </form>
    </div>
  </div>
</section>
''' + render_faq_section("contact")


# ------------------------------------------------------------------------------
# PAGE CONFIG — declarative per-page metadata + schema
# ------------------------------------------------------------------------------

PAGES = {
    "index": {
        "filename": "index.html",
        "canonical_path": "",
        "title": "Hidden Bridge Golf Club — Public 18-hole Course in Sheridan, WY",
        "meta_desc": "Hidden Bridge is a friendly 18-hole public golf course in Sheridan, Wyoming. Par 72, Big Horn mountain views, water on the back nine, and Sheridan-priced golf. Open daily through the 2026 season.",
        "og_title": "Hidden Bridge Golf Club — Sheridan, Wyoming",
        "og_desc": "Friendly 18-hole public course at the foot of the Big Horns. Par 72, water on the back nine, sunsets people drive out to see.",
        "breadcrumb_items": [("Home", None)],
        "main": main_index,
        "extra_schemas": ["golf_course"],
    },
    "course": {
        "filename": "course.html",
        "canonical_path": "course",
        "title": "The Course — Par 72, 18 Holes, 4 Tee Sets · Hidden Bridge Golf Club",
        "meta_desc": "Hidden Bridge plays par 72 across four tee sets from 4,685 to 6,600 yards. Course rating 71.1/119 (Men's Black/Blue). See the scorecard, course map, and local rules.",
        "og_title": "The Course — Hidden Bridge Golf Club",
        "og_desc": "Par 72 · 18 holes · four tee sets · water on the back nine · Big Horn Mountain views.",
        "breadcrumb_items": [("Home", "index.html"), ("The Course", None)],
        "main": main_course,
        "extra_schemas": ["service:The Course"],
    },
    "rates": {
        "filename": "rates.html",
        "canonical_path": "rates",
        "title": "Rates &amp; Tee Times — Hidden Bridge Golf Club, Sheridan WY",
        "meta_desc": "2026 green fees, 9-hole and twilight rates, cart rentals, and junior/senior pricing at Hidden Bridge Golf Club. Request a tee time online or call 307-752-6625.",
        "og_title": "Rates &amp; Tee Times — Hidden Bridge Golf Club",
        "og_desc": "Sheridan-priced public golf. Walking, 9-hole, twilight, junior, senior — and a fast tee-time request form.",
        "breadcrumb_items": [("Home", "index.html"), ("Rates &amp; Tee Times", None)],
        "main": main_rates,
        "extra_schemas": ["service:Green Fees &amp; Tee Time Booking"],
    },
    "membership": {
        "filename": "membership.html",
        "canonical_path": "membership",
        "title": "Membership — Junior, Individual &amp; Family · Hidden Bridge Golf Club",
        "meta_desc": "Junior, Individual, and Family season memberships at Hidden Bridge Golf Club. Unlimited play, advance tee-time booking, member events, and cart discounts.",
        "og_title": "Membership — Hidden Bridge Golf Club",
        "og_desc": "Play all season. Unlimited rounds, 14-day advance tee-time booking, member events.",
        "breadcrumb_items": [("Home", "index.html"), ("Membership", None)],
        "main": main_membership,
        "extra_schemas": ["service:Season Membership"],
    },
    "events": {
        "filename": "events.html",
        "canonical_path": "events",
        "title": "Tournaments &amp; Events — Weddings, Leagues, Scrambles · Hidden Bridge Golf Club",
        "meta_desc": "Charity scrambles, weekly leagues, weddings, family reunions, and corporate events at Hidden Bridge Golf Club in Sheridan, Wyoming. 2026 tournament calendar inside.",
        "og_title": "Tournaments &amp; Events — Hidden Bridge Golf Club",
        "og_desc": "Charity scrambles, weekly leagues, weddings, reunions, and corporate outings.",
        "breadcrumb_items": [("Home", "index.html"), ("Tournaments &amp; Events", None)],
        "main": main_events,
        "extra_schemas": ["service:Tournaments &amp; Private Events"],
    },
    "proshop": {
        "filename": "proshop.html",
        "canonical_path": "proshop",
        "title": "Pro Shop — Drinks, Snacks, Rentals &amp; Lessons · Hidden Bridge Golf Club",
        "meta_desc": "The Hidden Bridge pro shop carries snacks, drinks, cart rentals, club rentals, gift cards, and arranges lessons and junior clinics. Sheridan, WY.",
        "og_title": "Pro Shop — Hidden Bridge Golf Club",
        "og_desc": "Drinks, snacks, rentals, gift cards, and lessons by appointment.",
        "breadcrumb_items": [("Home", "index.html"), ("Pro Shop", None)],
        "main": main_proshop,
        "extra_schemas": ["service:Pro Shop &amp; Rentals"],
    },
    "contact": {
        "filename": "contact.html",
        "canonical_path": "contact",
        "title": "Contact &amp; Directions — Hidden Bridge Golf Club, Sheridan WY",
        "meta_desc": "Hidden Bridge Golf Club is at 550 Mydland Road, Sheridan, WY 82801. Call 307-752-6625 or send a message. Open daily through the 2026 season.",
        "og_title": "Contact Hidden Bridge Golf Club",
        "og_desc": "550 Mydland Road, Sheridan, WY 82801 · 307-752-6625 · Open daily through the 2026 season.",
        "breadcrumb_items": [("Home", "index.html"), ("Contact", None)],
        "main": main_contact,
        "extra_schemas": [],  # contact info is already in GolfCourse schema below
    },
}


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------

def build_schema_block(page_key, page):
    """Assemble all JSON-LD schema for a page."""
    schemas = []

    # Every page gets BreadcrumbList + FAQPage
    schemas.append(breadcrumb_schema(page["breadcrumb_items"]))
    schemas.append(faq_schema(FAQS[page_key]))

    # Index gets the full GolfCourse/LocalBusiness block
    for s in page.get("extra_schemas", []):
        if s == "golf_course":
            schemas.append(golf_course_schema())
        elif s.startswith("service:"):
            name = s[len("service:"):]
            schemas.append(service_schema(
                name=name,
                desc=page["meta_desc"],
                page_path=page["canonical_path"],
            ))

    # Contact page also references golf_course schema (full NAP context)
    if page_key == "contact":
        schemas.append(golf_course_schema())

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
    print(f"Building Hidden Bridge preview → {OUT}")
    for key, page in PAGES.items():
        html = render_page(key)
        path = OUT / page["filename"]
        path.write_text(html, encoding="utf-8")
        # Quick byte count + edit-tag count for sanity
        edit_ids = len(re.findall(r'id="edit-', html))
        print(f"  ✓ {page['filename']:20s}  {len(html):>7,} bytes  ·  {edit_ids:>2d} edit-* tags")


if __name__ == "__main__":
    main()
