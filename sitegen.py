"""sitegen.py — The Donut Shack static site generator. Warm, feminine, elevated bakery design;
booking/catering lead-capture; full on-page SEO. Rebuilds on boot."""
from __future__ import annotations
import html, json, os, re
from datetime import date
from pathlib import Path
import dsdata as D

ROOT = Path(__file__).parent
OUT = ROOT / "static" / "seo"
BASE = os.environ.get("DS_BASE_URL", "https://thedonutshack.com").rstrip("/")
GA = os.environ.get("DS_GA_ID", "").strip()


def esc(s): return html.escape(str(s if s is not None else ""), quote=True)


_S = 'fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "truck": f'<svg viewBox="0 0 24 24" {_S}><path d="M3 6h11v9H3zM14 9h4l3 3v3h-7zM7 18.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM18 18.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>',
    "heart": f'<svg viewBox="0 0 24 24" {_S}><path d="M12 20s-7-4.3-9.3-8.3C1 8.5 2.6 5 6 5c2 0 3.2 1.2 4 2.3C10.8 6.2 12 5 14 5c3.4 0 5 3.5 3.3 6.7C19 15.7 12 20 12 20z"/></svg>',
    "box": f'<svg viewBox="0 0 24 24" {_S}><path d="M3 7l9-4 9 4-9 4-9-4zM3 7v10l9 4 9-4V7M12 11v10"/></svg>',
    "gift": f'<svg viewBox="0 0 24 24" {_S}><path d="M20 12v9H4v-9M2 7h20v5H2zM12 22V7M12 7S9 7 9 4.5 12 7 12 7zM12 7s3 0 3-2.5S12 7 12 7z"/></svg>',
    "sparkle": f'<svg viewBox="0 0 24 24" {_S}><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/></svg>',
    "star": f'<svg viewBox="0 0 24 24" {_S}><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17.8 6.6 20l1-6.1L3.2 9.5l6.1-.9z"/></svg>',
    "pin": f'<svg viewBox="0 0 24 24" {_S}><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11zM12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>',
    "phone": f'<svg viewBox="0 0 24 24" {_S}><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    "mail": f'<svg viewBox="0 0 24 24" {_S}><path d="M3 5h18v14H3zM3 6l9 7 9-7"/></svg>',
    "insta": f'<svg viewBox="0 0 24 24" {_S}><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "check": f'<svg viewBox="0 0 24 24" {_S}><path d="M20 6L9 17l-5-5"/></svg>',
    "clock": f'<svg viewBox="0 0 24 24" {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "arrow": f'<svg viewBox="0 0 24 24" {_S}><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}
def ic(n): return ICONS.get(n, ICONS["star"])

_GLAZE = ["#F8D7DD", "#FBE7C9", "#E7DBF6", "#FDE6A8", "#E9C8B6", "#CDEBDD", "#F6C9D5", "#E5D4F2", "#F3D9B0", "#F8CEDA", "#EAD7C2", "#F4DCC3"]


def _analytics():
    if not GA:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            f"gtag('js',new Date());gtag('config','{GA}');</script>")


def _fonts():
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600&family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">')


NAVLINKS = [("Our Donuts", "/donuts"), ("Events & Catering", "/events"), ("Our Story", "/story")]


def nav():
    links = "".join(f'<a href="{h}">{esc(t)}</a>' for t, h in NAVLINKS)
    mlinks = links + '<a href="/book">Book the truck</a>'
    return (
        '<nav class="nav"><div class="wrap">'
        f'<a class="brand" href="/"><span class="dot"></span>The Donut <b>Shack</b></a>'
        '<input type="checkbox" id="navtog" class="navtog"><label for="navtog" class="hamb" aria-label="Menu"><span></span><span></span><span></span></label>'
        f'<div class="nav-links">{links}<a class="nav-cta" href="/book">Book the truck</a></div>'
        f'<div class="mobile-menu">{mlinks}</div>'
        '</div></nav>')


def foot():
    nav_ = "".join(f'<a href="{h}">{esc(t)}</a>' for t, h in NAVLINKS) + '<a href="/book">Book the Truck</a>'
    return (
        '<footer class="foot"><div class="wrap"><div class="foot-grid">'
        f'<div><a class="brand" href="/">The Donut <b>Shack</b></a>'
        f'<p style="margin-top:12px;max-width:34ch">{esc(D.TAGLINE)} Rolling fresh, small-batch artisan donuts all over the Las Vegas valley.</p></div>'
        f'<div class="foot-col"><h4>Explore</h4>{nav_}</div>'
        f'<div class="foot-col"><h4>Visit</h4><a href="/events">Weddings &amp; donut walls</a><a href="/events">Catering &amp; corporate</a><a href="/book">Find the truck</a></div>'
        f'<div class="foot-col"><h4>Say hello</h4><a href="tel:{D.PHONE.replace(" ","")}">{esc(D.PHONE)}</a>'
        f'<a href="mailto:{D.EMAIL}">{esc(D.EMAIL)}</a><a href="https://instagram.com/{D.INSTAGRAM.lstrip("@")}">{esc(D.INSTAGRAM)}</a></div>'
        '</div>'
        f'<div class="foot-bottom"><span>&copy; {date.today().year} {esc(D.NAME)} · {esc(D.CITY)}, NV</span>'
        '<span>Made with sprinkles 🍩</span></div></div></footer>')


def page(title, desc, path, body, jsonld=None, og="website"):
    canon = f"{BASE}{path}"
    ld = ""
    blocks = list(jsonld or [])
    if blocks:
        ld = "".join(f'<script type="application/ld+json">{json.dumps(b)}</script>' for b in blocks)
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{esc(og)}"><meta property="og:url" content="{esc(canon)}">
<meta property="og:site_name" content="{esc(D.NAME)}"><meta property="og:image" content="{BASE}/static/img/hero.png">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#E27D95">
<meta name="robots" content="index,follow">{_fonts()}
<link rel="stylesheet" href="/static/css/style.css">{ld}{_analytics()}
</head><body>{nav()}<main>{body}</main>{foot()}</body></html>"""


def _book_form(src="page"):
    occ = ["Wedding", "Bridal / baby shower", "Birthday party", "Corporate / office", "Grand opening / pop-up", "Pool / backyard party", "Other celebration"]
    opts = "".join(f"<option>{esc(o)}</option>" for o in occ)
    return f"""<form class="card" onsubmit="return dsBook(event)">
<div class="row2"><div class="field"><label>Your name</label><input name="name" required placeholder="First &amp; last"></div>
<div class="field"><label>Phone or email</label><input name="contact" required placeholder="So we can reach you"></div></div>
<div class="row2"><div class="field"><label>What's the occasion?</label><select name="occasion">{opts}</select></div>
<div class="field"><label>Event date</label><input name="event_date" type="text" placeholder="MM/DD/YYYY (or 'flexible')"></div></div>
<div class="row2"><div class="field"><label>Headcount (approx.)</label><input name="headcount" placeholder="e.g. 80 guests"></div>
<div class="field"><label>Where in the valley?</label><input name="area" placeholder="Henderson, the Strip, Summerlin…"></div></div>
<div class="field"><label>Tell us about your sweet plans</label><textarea name="message" placeholder="Donut wall? Custom flavors? A pink truck at your party? Spill it 🍩"></textarea></div>
<input type="hidden" name="source" value="{esc(src)}">
<button class="btn btn-primary" type="submit" style="width:100%">Send my request {ic("arrow")}</button>
<p id="book-out" class="form-out muted"></p>
<script>async function dsBook(e){{e.preventDefault();var f=e.target,o=f.querySelector('#book-out');
var d={{}};new FormData(f).forEach(function(v,k){{d[k]=v;}});
if(!d.name||!d.contact){{o.textContent='Please add your name and a way to reach you.';o.style.color='#C8546F';return false;}}
o.textContent='Sending…';o.style.color='';
try{{var r=await fetch('/api/book',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}});
if(r.ok){{if(typeof gtag==='function')gtag('event','generate_lead',{{source:d.source}});
f.reset();o.textContent='Yay! We got it — we\\'ll be in touch within a day. 🍩';o.style.color='#1aa06d';}}
else o.textContent='Hmm, that didn\\'t go through. Call us at {esc(D.PHONE)}?';}}
catch(_){{o.textContent='Network hiccup — try again or call {esc(D.PHONE)}.';}}return false;}}</script></form>"""


def _cta_band():
    return (f'<section><div class="wrap"><div class="cta-band">'
            f'<span class="eyebrow" style="color:#fff">Let\'s make it sweet</span>'
            f'<h2>Bring the pink truck to your party</h2>'
            f'<p>Weddings, birthdays, pool days, the office — wherever the celebration is, we\'ll roll up with warm donuts and a whole lot of joy.</p>'
            f'<a class="btn btn-white" href="/book">Book the truck {ic("arrow")}</a></div></div></section>')


def home():
    why = "".join(f'<div class="why-card"><div class="why-ic">{ic(w["icon"])}</div><h3>{esc(w["title"])}</h3><p>{esc(w["text"])}</p></div>' for w in D.WHY)
    svc = "".join(
        f'<a class="svc-card" href="/events" style="text-decoration:none"><div class="svc-ic">{ic(s["icon"])}</div>'
        f'<h3>{esc(s["name"])}</h3><p>{esc(s["short"])}</p></a>' for s in D.SERVICES)
    feat = D.FLAVORS[:6]
    flavors = "".join(
        f'<div class="flavor"><div class="flavor-img" style="background:linear-gradient(135deg,{_GLAZE[i%len(_GLAZE)]},#fff)"><span class="flavor-emoji">🍩</span></div>'
        f'<div class="flavor-body">{"".join(f"<span class=\"tag\">{esc(t)}</span>" for t in fl["tags"])}<h3>{esc(fl["name"])}</h3><p>{esc(fl["desc"])}</p></div></div>'
        for i, fl in enumerate(feat))
    body = f"""
<section class="hero"><div class="wrap"><div class="hero-copy">
<span class="eyebrow">Las Vegas · mobile donut truck</span>
<h1>Donuts that are <span class="accent">almost</span> too pretty to eat.</h1>
<p class="lead">{esc(D.SUB)}</p>
<div class="hero-cta"><a class="btn btn-primary" href="/book">Book the truck {ic("arrow")}</a><a class="btn btn-ghost" href="/donuts">See the flavors</a></div>
<div class="hero-trust"><span><span class="pip">{ic("heart")}</span> Weddings &amp; donut walls</span><span><span class="pip">{ic("truck")}</span> We come to you</span><span><span class="pip">{ic("sparkle")}</span> Fresh, small-batch</span></div>
</div><div class="hero-img"><img src="/static/img/hero.png" alt="Artisan donuts with pastel glazes and edible flowers">
<div class="badge"><b>🍩</b><span>Hand-glazed<br>to order</span></div></div></div></section>

<section class="why"><div class="wrap"><div class="why-grid">{why}</div></div></section>
<div class="on-cream"><div class="scallop"></div></div>

<section><div class="wrap"><div class="sec-head center"><span class="eyebrow">What we do</span>
<h2>The truck rolls up. The party levels up.</h2><p class="lead">From a wall of donuts at your wedding to a box at the office — here's how we sweeten your day.</p></div>
<div class="svc-grid">{svc}</div></div></section>

<section class="flavors"><div class="wrap"><div class="sec-head center"><span class="eyebrow">A few favorites</span>
<h2>Made fresh, glazed by hand</h2><p class="lead">Pastel glazes, real ingredients, edible flowers. A rotating menu of small-batch flavors — here's a taste.</p></div>
<div class="flavor-grid">{flavors}</div>
<div class="center" style="margin-top:36px"><a class="btn btn-ghost" href="/donuts">See the full menu {ic("arrow")}</a></div></div></section>

<section><div class="wrap"><div class="split">
<div class="split-img"><img src="/static/img/donut-wall.png" alt="A wedding donut wall draped in flowers"></div>
<div class="split-copy"><span class="eyebrow">{ic("heart")} The showstopper</span><h2>Donut walls, dressed in flowers</h2>
<p>Our signature wedding-and-shower centerpiece: an ivory wall hung with dozens of glazed donuts, draped in eucalyptus and blush roses, styled to your colors. Equal parts dessert and decor — and the photo everyone wants.</p>
<a class="btn btn-primary" href="/events">Plan a donut wall {ic("arrow")}</a></div></div></div></section>

<section class="flavors"><div class="wrap"><div class="split rev">
<div class="split-img"><img src="/static/img/truck.png" alt="The Donut Shack pink food truck on the Las Vegas Strip"></div>
<div class="split-copy"><span class="eyebrow">Our story</span><h2>One little pink truck, a whole lot of joy</h2>
<p>{esc(D.STORY[0])}</p><p>It grew into a pink truck that rolls all over the valley, hand-glazing small-batch donuts to order. Pretty, playful, and made with real ingredients.</p>
<a class="btn btn-ghost" href="/story">Read our story {ic("arrow")}</a></div></div></div></section>

{_cta_band()}"""
    ld = [{"@context": "https://schema.org", "@type": "Bakery", "name": D.NAME, "url": BASE,
           "description": D.SUB, "telephone": D.PHONE, "email": D.EMAIL,
           "areaServed": "Las Vegas Valley, NV", "servesCuisine": "Donuts", "image": f"{BASE}/static/img/hero.png"}]
    return page(f"{D.NAME} — Artisan Donut Truck in Las Vegas",
                f"{D.NAME}: a mobile artisan donut truck in Las Vegas. Fresh, hand-glazed small-batch donuts, donut walls for weddings, plus catering, corporate &amp; custom boxes. Book the truck.",
                "/", body, ld)


def donuts():
    cards = "".join(
        f'<div class="flavor"><div class="flavor-img" style="background:linear-gradient(135deg,{_GLAZE[i%len(_GLAZE)]},#fff)"><span class="flavor-emoji">🍩</span></div>'
        f'<div class="flavor-body">{"".join(f"<span class=\"tag{(' gold' if t in ('Signature','Fan favorite') else '')}\">{esc(t)}</span>" for t in fl["tags"])}'
        f'<h3>{esc(fl["name"])}</h3><p>{esc(fl["desc"])}</p></div></div>'
        for i, fl in enumerate(D.FLAVORS))
    body = f"""
<header class="page-head"><div class="wrap"><span class="eyebrow">The menu</span>
<h1>Our donuts</h1><p class="lead center">A rotating, seasonal line-up of small-batch flavors — hand-glazed to order with real ingredients and a little flair. Mix and match your custom dozen.</p></div></header>
<section class="flavors"><div class="wrap"><div class="flavor-grid">{cards}</div>
<div class="center" style="margin-top:14px"><p class="muted" style="margin-bottom:18px">Flavors rotate with the seasons &amp; what's fresh — ask about specials and dietary-friendly options.</p>
<a class="btn btn-primary" href="/book">Order a custom box {ic("arrow")}</a></div></div></section>
{_cta_band()}"""
    items = [{"@type": "ListItem", "position": i + 1, "name": fl["name"], "description": fl["desc"]} for i, fl in enumerate(D.FLAVORS)]
    ld = [{"@context": "https://schema.org", "@type": "Menu", "name": f"{D.NAME} Donut Menu",
           "hasMenuSection": {"@type": "MenuSection", "name": "Artisan Donuts",
                              "hasMenuItem": [{"@type": "MenuItem", "name": fl["name"], "description": fl["desc"]} for fl in D.FLAVORS]}}]
    return page(f"Our Donuts — The Menu | {D.NAME}",
                "The Donut Shack menu: small-batch artisan donut flavors hand-glazed in Las Vegas — Strawberry Champagne, Lavender Honey, Lemon Meringue, Pistachio Rose and more. Build a custom dozen.",
                "/donuts", body, ld)


def events():
    svc = "".join(
        f'<div class="svc-card"><div class="svc-ic">{ic(s["icon"])}</div><h3>{esc(s["name"])}</h3>'
        f'<p>{esc(s["long"])}</p><ul class="svc-for">{"".join(f"<li>{esc(x)}</li>" for x in s["for"])}</ul></div>'
        for s in D.SERVICES)
    body = f"""
<header class="page-head"><div class="wrap"><span class="eyebrow">Events &amp; catering</span>
<h1>Sweeten the celebration</h1><p class="lead center">Weddings, parties, offices, pop-ups — wherever Las Vegas is celebrating, the pink truck (and a wall of donuts) belongs there.</p>
<div style="margin-top:24px"><a class="btn btn-primary" href="/book">Check your date {ic("arrow")}</a></div></div></header>
<section><div class="wrap"><div class="svc-grid">{svc}</div></div></section>
<section class="flavors"><div class="wrap"><div class="split">
<div class="split-img"><img src="/static/img/donut-wall.png" alt="Wedding donut wall by The Donut Shack"></div>
<div class="split-copy"><span class="eyebrow">{ic("heart")} Weddings</span><h2>The donut wall everyone photographs</h2>
<p>Skip the cake-cutting cliché. Our donut walls are styled to your palette with fresh flowers and greenery — a dessert display that doubles as decor and gives your guests something to talk about (and Instagram).</p>
<a class="btn btn-primary" href="/book">Plan your wedding donuts {ic("arrow")}</a></div></div></div></section>
{_cta_band()}"""
    return page(f"Events &amp; Catering — Weddings, Donut Walls &amp; Corporate | {D.NAME}",
                "Book The Donut Shack for Las Vegas weddings (donut walls!), parties, corporate catering, grand openings and custom boxes. The pink artisan donut truck comes to you.",
                "/events", body)


def story():
    paras = "".join(f"<p>{esc(p)}</p>" for p in D.STORY)
    why = "".join(f'<div class="why-card"><div class="why-ic">{ic(w["icon"])}</div><h3>{esc(w["title"])}</h3><p>{esc(w["text"])}</p></div>' for w in D.WHY)
    body = f"""
<header class="page-head"><div class="wrap"><span class="eyebrow">Our story</span>
<h1>Hi, we're The Donut Shack</h1></div></header>
<section><div class="wrap"><div class="split">
<div class="split-img"><img src="/static/img/truck.png" alt="The Donut Shack pink truck in Las Vegas"></div>
<div class="split-copy prose">{paras}</div></div></div></section>
<section class="why"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Why folks love us</span><h2>Pretty, playful, and actually delicious</h2></div>
<div class="why-grid">{why}</div></div></section>
{_cta_band()}"""
    return page(f"Our Story | {D.NAME}",
                "The story behind The Donut Shack — a woman-founded mobile artisan donut truck rolling small-batch, hand-glazed donuts all over Las Vegas.",
                "/story", body)


def book():
    faq = "".join(f'<div class="faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in D.FAQ)
    body = f"""
<header class="page-head"><div class="wrap"><span class="eyebrow">Book the truck</span>
<h1>Let's plan something sweet</h1><p class="lead center">Tell us about your event and we'll get back to you within a day with availability and a quote. No deposit to ask.</p></div></header>
<section><div class="wrap"><div class="book-grid">
<div class="book-info"><span class="eyebrow">Here's how it works</span><h2>Easy as 1‑2‑🍩</h2>
<ul><li>{ic("check")}<div>Send your details<span>Date, headcount, where in the valley, and what you're dreaming up.</span></div></li>
<li>{ic("check")}<div>We confirm &amp; quote<span>We check the calendar and send availability + a simple quote within a day.</span></div></li>
<li>{ic("check")}<div>The truck rolls up<span>We arrive, set up the prettiest donuts in Vegas, and make your day.</span></div></li></ul>
<div style="margin-top:30px;padding-top:24px;border-top:1px solid var(--line)">
<p style="display:flex;align-items:center;gap:10px;font-weight:800;color:var(--cocoa);margin-bottom:8px">{ic("phone")} <a href="tel:{D.PHONE.replace(' ','')}">{esc(D.PHONE)}</a></p>
<p style="display:flex;align-items:center;gap:10px;font-weight:800;color:var(--cocoa);margin-bottom:8px">{ic("mail")} <a href="mailto:{D.EMAIL}">{esc(D.EMAIL)}</a></p>
<p style="display:flex;align-items:center;gap:10px;font-weight:800;color:var(--cocoa)">{ic("insta")} <a href="https://instagram.com/{D.INSTAGRAM.lstrip('@')}">{esc(D.INSTAGRAM)}</a></p></div></div>
<div>{_book_form("book")}</div></div></div></section>
<section class="flavors"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Good to know</span><h2>Questions, answered</h2></div>
<div style="max-width:760px;margin:0 auto">{faq}</div></div></section>"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in D.FAQ]}]
    return page(f"Book the Truck — Weddings, Parties &amp; Catering | {D.NAME}",
                "Book The Donut Shack for your Las Vegas event. Tell us your date, headcount and vision — weddings, donut walls, parties and corporate catering. We reply within a day.",
                "/book", body, ld)


def _write(rel, txt):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")


def build():
    pages = {"index.html": home(), "donuts.html": donuts(), "events.html": events(),
             "story.html": story(), "book.html": book()}
    for f, h in pages.items():
        _write(f, h)
    urls = ["/", "/donuts", "/events", "/story", "/book"]
    sm = ('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for u in urls) + "</urlset>")
    (ROOT / "static" / "sitemap.xml").write_text(sm, encoding="utf-8")
    (ROOT / "static" / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(pages)} pages.")
    return urls


if __name__ == "__main__":
    build()
