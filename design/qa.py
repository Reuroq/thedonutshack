"""qa.py — pre-deploy visual QA for The Donut Shack.

Screenshots EVERY page at desktop + mobile, and runs an automated lint that flags any oversized
icon (an <svg> rendering > 80px) or element overflowing the viewport — the class of bug that
shipped the giant phone/mail icons. Run before every deploy; review the screenshots; fix flags.

  python design/qa.py [base_url]   (default: the live site)
"""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://thedonutshack.onrender.com").rstrip("/")
PAGES = ["/", "/donuts", "/events", "/story", "/book"]
VIEWS = [("desktop", 1440, 900), ("mobile", 390, 844)]
OUT = Path(__file__).parent / "qa"
OUT.mkdir(exist_ok=True)

LINT_JS = """() => {
  const flags = [];
  document.querySelectorAll('svg').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 80 || r.height > 80) flags.push({type:'oversized-icon', w:Math.round(r.width), h:Math.round(r.height), cls:el.parentElement?.className||''});
  });
  if (document.documentElement.scrollWidth > window.innerWidth + 2)
    flags.push({type:'horizontal-overflow', sw:document.documentElement.scrollWidth, vw:window.innerWidth});
  return flags;
}"""


def run():
    issues = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for label, w, h in VIEWS:
            pg = b.new_page(viewport={"width": w, "height": h})
            for path in PAGES:
                for attempt in range(3):
                    try:
                        pg.goto(BASE + path, wait_until="networkidle", timeout=60000); break
                    except Exception:
                        time.sleep(5)
                pg.wait_for_timeout(1500)
                name = (path.strip("/") or "home")
                pg.screenshot(path=str(OUT / f"{name}-{label}.png"), full_page=True)
                flags = pg.evaluate(LINT_JS)
                status = "OK" if not flags else f"⚠ {flags}"
                if flags:
                    issues += len(flags)
                print(f"  {label:8} {path:10} -> {status}")
            pg.close()
        b.close()
    print(f"\n{'PASS — no visual lint flags' if issues == 0 else f'{issues} FLAG(S) — review design/qa/ screenshots before deploying'}")
    return issues


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
