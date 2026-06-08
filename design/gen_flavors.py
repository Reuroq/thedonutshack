"""Generate a consistent set of single-donut flavor photos for the menu cards."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gen import gen

STYLE = (" — a single beautiful artisan donut centered, slightly above 3/4 angle, on a soft {bg} pastel "
         "background, soft natural light with a gentle shadow, premium appetizing close-up food photography, "
         "dreamy, clean and minimal, high detail, no text, no hands, no props.")

FLAVORS = [
    ("flavor-strawberry", "A glossy strawberry-pink glazed donut topped with crushed freeze-dried strawberries and tiny gold flecks", "blush pink"),
    ("flavor-vanilla", "A glossy ivory vanilla-bean glazed donut with delicate gold shimmer sprinkles", "warm cream"),
    ("flavor-lavender", "A soft lavender glazed donut with a honey drizzle and real edible lavender flowers", "pale lavender"),
    ("flavor-lemon", "A pale-yellow lemon glazed donut topped with a torched, golden toasted meringue swirl", "soft butter yellow"),
    ("flavor-caramel", "A dark chocolate glazed donut with ribbons of salted caramel drizzle and flaky sea salt", "warm tan"),
    ("flavor-pistachio", "A pale-green pistachio glazed donut sprinkled with crushed pistachios and pink rose petals", "soft rose"),
    ("flavor-cookies", "A cookies-and-cream glazed donut loaded with chunks of crushed chocolate sandwich cookies", "soft warm grey-cream"),
    ("flavor-matcha", "A green matcha glazed donut with elegant white chocolate drizzle", "soft mint"),
    ("flavor-maple", "A glossy maple-brown glazed donut with a few candied bacon bits", "warm cream"),
    ("flavor-birthday", "A white glazed donut completely covered in colorful rainbow sprinkles", "soft blush"),
    ("flavor-biscoff", "A warm caramel cookie-butter glazed donut with a crunchy spiced cookie crumble", "soft tan"),
    ("flavor-cinnamon", "A classic donut generously rolled in cinnamon sugar, served warm", "warm cream"),
]

if __name__ == "__main__":
    for slug, desc, bg in FLAVORS:
        out = f"static/img/{slug}.png"
        try:
            gen(out, desc + STYLE.format(bg=bg), "1024x1024")
        except Exception as e:
            print(f"FAILED {slug}: {str(e)[:80]}")
    print("flavor generation complete")
