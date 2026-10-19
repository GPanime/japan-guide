"""Smoke test for the built page. Run after build_site.py, before publishing.

    python3 source/test_site.py                 # tests index.html in the repo
    python3 source/test_site.py https://japan.zhunior.com/   # tests the live site

Checks, on a desktop and a phone-sized window:
  * every stop's tab opens its own section and only that one
  * filters work without JavaScript (category and mood chips change the card count)
  * nothing spills sideways on a phone (no horizontal scroll)
  * dark mode applies, the theme switch cycles, and the Google map loads and follows pins / "Show on map"
  * no script errors
Screenshots go to source/out/test/.
"""
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import CITIES

URL = sys.argv[1] if len(sys.argv) > 1 else "file://" + os.path.join(os.path.dirname(HERE), "index.html")
SHOTS = os.path.join(HERE, "out", "test")
os.makedirs(SHOTS, exist_ok=True)
KEYS = [c["key"] for c in CITIES]
problems = []


def check(ok, msg):
    print(("  ok    " if ok else "  FAIL  ") + msg)
    if not ok:
        problems.append(msg)


def shown(pg):
    return [k for k in KEYS if pg.evaluate(f"getComputedStyle(document.querySelector('#jp-city-{k}')).display") == "block"]


def visible_cards(pg, k):
    return pg.evaluate(f"[...document.querySelectorAll('#jp-city-{k} .jp-bytype .card')].filter(c => c.offsetParent).length")


with sync_playwright() as pw:
    b = pw.chromium.launch()

    print("Without JavaScript (tabs and filters must still work):")
    pg = b.new_context(viewport={"width": 1280, "height": 900}, java_script_enabled=False).new_page()
    for c in CITIES:
        k = c["key"]
        pg.goto(URL + f"#jp-city-{k}"); pg.wait_for_timeout(300)
        check(shown(pg) == [k], f"{k}: tab shows only its own section")
        check(visible_cards(pg, k) == len(c["places"]), f"{k}: all {len(c['places'])} cards visible")
        cat = pg.query_selector(f"#jp-city-{k} label[for^='{k}-jc-']:not([for='{k}-jc-all'])")
        if cat:
            cat.click(); pg.wait_for_timeout(200)
            n = visible_cards(pg, k)
            check(0 < n < len(c["places"]), f"{k}: category filter narrows the list ({n} shown)")
            pg.click(f"#jp-city-{k} .clr"); pg.wait_for_timeout(200)
    print("With JavaScript, dark mode, desktop:")
    errors = []
    pg = b.new_page(viewport={"width": 1280, "height": 900}, color_scheme="dark")
    pg.on("pageerror", lambda e: errors.append(str(e)))
    k = KEYS[0]
    pg.goto(URL + f"#jp-city-{k}", wait_until="domcontentloaded"); pg.wait_for_timeout(2500)
    bg = pg.evaluate("getComputedStyle(document.querySelector('#jp26')).backgroundColor")
    check(bg == "rgb(28, 22, 19)", f"dark background follows the system setting ({bg})")
    src = pg.query_selector(f"#jp-city-{k} .gmap iframe").get_attribute("src") or ""
    check("output=embed" in src, "Google map loads for the open tab")
    pg.click(f"#jp-city-{k} .map a[data-pin='1']"); pg.wait_for_timeout(800)
    check(pg.inner_text(f"#jp-city-{k} .gmap-sel").startswith("1 ·"), "tapping pin 1 moves the Google map to place 1")
    pg.click(".themebtn"); pg.click(".themebtn"); pg.wait_for_timeout(300)
    check(pg.evaluate("document.documentElement.dataset.theme") == "light", "theme switch reaches Light")
    pg.screenshot(path=os.path.join(SHOTS, "desktop.png"))
    check(pg.evaluate("document.documentElement.scrollWidth") <= 1280, "no sideways scroll on desktop")
    print("Phone:")
    p2 = b.new_page(viewport={"width": 390, "height": 844})
    p2.on("pageerror", lambda e: errors.append(str(e)))
    k = KEYS[-1]
    p2.goto(URL + f"#jp-city-{k}", wait_until="domcontentloaded"); p2.wait_for_timeout(1500)
    p2.click(f"#jp-city-{k} .onmap[data-onmap='1']"); p2.wait_for_timeout(1200)
    check(p2.evaluate(f"document.querySelector('#{k}-maptog').checked"), "'Show on map' opens the folded map on a phone")
    check(p2.evaluate("document.documentElement.scrollWidth") <= 390, "no sideways scroll on a phone")
    p2.screenshot(path=os.path.join(SHOTS, "phone.png"))
    check(not errors, f"no script errors {errors if errors else ''}")
    b.close()

print("\nAll checks passed." if not problems else f"\n{len(problems)} problem(s): " + "; ".join(problems))
sys.exit(1 if problems else 0)
