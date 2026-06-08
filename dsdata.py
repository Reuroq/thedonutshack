"""dsdata.py — The Donut Shack content spine (concept build: a woman-founded mobile artisan
donut truck in Las Vegas). All copy is evocative placeholder content — easy to swap for real
details (founder name, flavors, prices, phone, social handles are marked PLACEHOLDER)."""
from __future__ import annotations

NAME = "The Donut Shack"
TAGLINE = "Las Vegas's sweetest little donut truck."
CITY = "Las Vegas"
# PLACEHOLDER contact details — replace with the real ones before launch.
PHONE = "(702) 555-0137"
EMAIL = "hello@thedonutshack.com"
INSTAGRAM = "@thedonutshacklv"
FOUNDER = "Daisy"   # PLACEHOLDER founder name

SUB = ("Hand-crafted, small-batch artisan donuts — rolled fresh and delivered to your celebration "
       "from our little pink truck. Weddings, parties, pop-ups and everything in between, all over the valley.")

# ── what we do (the food-truck services; booking-led, no checkout) ──
SERVICES = [
    {"slug": "book-the-truck", "name": "Book the Truck", "icon": "truck",
     "short": "Our pink truck rolls right up to your party, pool day, or pop-up and serves warm donuts to order.",
     "long": "Birthdays, bachelorettes, pool parties, grand openings, block parties — wherever the fun is, the Shack shows up. "
             "We bring the donuts, the smiles, and a little pink magic; you just tell us where and when.",
     "for": ["Birthdays & bachelorettes", "Pool & backyard parties", "Grand openings & pop-ups", "Block parties & festivals"]},
    {"slug": "donut-walls", "name": "Donut Walls", "icon": "heart",
     "short": "The showstopper for weddings and showers — a wall of pastel donuts, dressed in flowers.",
     "long": "Our signature donut walls are pure Vegas-wedding magic: an ivory wall hung with dozens of glazed donuts, draped "
             "in eucalyptus and blush roses, styled to match your colors. Equal parts dessert and decor.",
     "for": ["Weddings & receptions", "Bridal & baby showers", "Engagement parties", "Quinceañeras & sweet sixteens"]},
    {"slug": "catering-corporate", "name": "Catering & Corporate", "icon": "box",
     "short": "Dozens (or hundreds) delivered fresh for offices, meetings, and big days.",
     "long": "Sweeten the office, the client meeting, the conference, or the team celebration. We deliver fresh, beautifully "
             "boxed donuts across the valley — coffee runs and dietary-friendly options welcome.",
     "for": ["Office mornings & meetings", "Conferences & expos", "Client gifting", "Team celebrations"]},
    {"slug": "custom-boxes", "name": "Custom Boxes", "icon": "gift",
     "short": "Build a personalized dozen for a birthday, a thank-you, or a 'just because.'",
     "long": "Pick your flavors, add a hand-tied bow and a little note, and we'll make someone's whole day. Perfect for "
             "birthdays, gifts, and treating yourself (no judgment here).",
     "for": ["Birthday surprises", "Thank-you gifts", "New-baby & welcome boxes", "Just because"]},
]

# ── the menu (creative artisan flavors; img filenames are generated where available) ──
FLAVORS = [
    {"name": "Strawberry Champagne", "img": "flavor-strawberry", "tags": ["Signature", "Pink"],
     "desc": "Strawberry glaze, freeze-dried berries and a whisper of bubbly — our celebration in a donut."},
    {"name": "Vanilla Bean Dream", "img": "flavor-vanilla", "tags": ["Classic"],
     "desc": "Madagascar vanilla bean glaze finished with a shimmer of gold sprinkles."},
    {"name": "Lavender Honey", "img": "flavor-lavender", "tags": ["Floral"],
     "desc": "Soft lavender glaze, a drizzle of local honey, and real edible flowers."},
    {"name": "Lemon Meringue", "img": "flavor-lemon", "tags": ["Bright"],
     "desc": "Tart lemon glaze under a torched, toasty meringue swirl."},
    {"name": "Salted Caramel Cocoa", "img": "", "tags": ["Rich"],
     "desc": "Dark chocolate, ribbons of salted caramel, a pinch of flaky sea salt."},
    {"name": "Pistachio Rose", "img": "", "tags": ["Floral"],
     "desc": "Toasted pistachio glaze scattered with rose petals — pretty and a little fancy."},
    {"name": "Cookies & Cream", "img": "", "tags": ["Crowd-pleaser"],
     "desc": "Cookies-and-cream glaze loaded with crushed chocolate sandwich cookies."},
    {"name": "Matcha White Chocolate", "img": "", "tags": ["New"],
     "desc": "Stone-ground matcha glaze drizzled with silky white chocolate."},
    {"name": "Maple Brown Butter", "img": "", "tags": ["Cozy"],
     "desc": "Brown-butter maple glaze — add candied bacon if you're feeling it."},
    {"name": "Birthday Cake", "img": "", "tags": ["Party"],
     "desc": "Vanilla cake glaze buried in rainbow sprinkles. It's a party, every time."},
    {"name": "Biscoff Butter", "img": "", "tags": ["Fan favorite"],
     "desc": "Warm cookie-butter glaze with a crunchy spiced-cookie crumble."},
    {"name": "Cinnamon Sugar Classic", "img": "", "tags": ["Classic"],
     "desc": "Just-fried, rolled in cinnamon sugar, served warm. The one that started it all."},
]

# ── the story (concept; founder name is a placeholder) ──
STORY = [
    f"The Donut Shack started where a lot of good things do — a tiny home kitchen, a stand mixer that wouldn't quit, and "
    f"{FOUNDER}'s stubborn belief that a donut could be both ridiculously pretty and ridiculously good.",
    f"After years of bringing boxes to every birthday, baby shower, and bridal brunch in the valley, the asks kept coming: "
    f"'Can you do my wedding?' 'Can you bring these to the office?' So {FOUNDER} did the only sensible thing — she put the "
    f"whole operation on wheels and painted it pink.",
    "Today the Shack rolls all over Las Vegas, hand-glazing small-batch donuts to order with real ingredients, real flowers, "
    "and a whole lot of joy. Every event we pull up to feels a little more like a celebration — and that's exactly the point.",
]

WHY = [
    {"icon": "sparkle", "title": "Made fresh, small-batch", "text": "Hand-glazed to order with real ingredients — never frozen, never sad."},
    {"icon": "heart", "title": "Almost too pretty to eat", "text": "Pastel glazes, edible flowers, and toppings styled to match your day."},
    {"icon": "truck", "title": "We come to you", "text": "From the Strip to Summerlin to Henderson — the truck rolls anywhere the party is."},
    {"icon": "star", "title": "A little Vegas magic", "text": "Donut walls, custom flavors, and a pink truck that makes every event pop."},
]

FAQ = [
    ("Where is the truck today?", f"We pop up all over the valley and post the week's spots on Instagram ({INSTAGRAM}). For a private event, just book us and we'll come to you."),
    ("How far in advance should I book?", "For weddings and big events, 4–8 weeks is ideal; for smaller parties and catering, a week or two usually works. Last-minute? Ask — we'll try to make it happen."),
    ("Do you do donut walls for weddings?", "Yes — they're our signature. We style the wall to your colors with fresh flowers and greenery. Tell us your date on the booking form."),
    ("Can you accommodate dietary needs?", "We can usually offer vegan and other options for catering and large orders with notice. Mention it when you book."),
    ("What areas do you serve?", "All of Las Vegas, Henderson, Summerlin, North Las Vegas and the surrounding valley. Outside that? Ask and we'll see what we can do."),
]
