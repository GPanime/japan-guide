"""Smoke test for the built page. Run after build_site.py, before publishing.

    python3 source/test_site.py                 # tests index.html in the repo
    python3 source/test_site.py https://japan.zhunior.com/   # tests the live site

Checks, on a desktop and a phone-sized window:
  * the password lock: locked on arrival, wrong password refused, right one opens the linked tab, device remembered
  * every stop's tab opens its own section and only that one
  * filters work without JavaScript (category and mood chips change the card count)
  * card photos open full screen and close again
  * every stop shows the autumn leaves forecast, and the Autumn leaves filter shows exactly the leaves spots
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

import lock
URL = sys.argv[1] if len(sys.argv) > 1 else "file://" + os.path.join(os.path.dirname(HERE), "index.html")   # the locked page
PLAIN = "file://" + os.path.join(os.path.dirname(HERE), "index-plain.html")   # the same page before locking (built locally)
PW = lock.password()
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


def open_page(pg, url, wait):
    """Open the locked page and type the password (the page then shows the linked tab)."""
    pg.goto(url, wait_until="domcontentloaded"); pg.wait_for_timeout(500)
    if pg.query_selector("#lock"):
        pg.fill("#pw", PW); pg.click("#go")
    pg.wait_for_timeout(wait)


def visible_cards(pg, k):
    return pg.evaluate(f"[...document.querySelectorAll('#jp-city-{k} .jp-bytype .card')].filter(c => c.offsetParent).length")


with sync_playwright() as pw:
    b = pw.chromium.launch()

    print("Password lock:")
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    pg = ctx.new_page()
    pg.goto(URL + "#jp-city-kyoto", wait_until="domcontentloaded"); pg.wait_for_timeout(500)
    check(pg.query_selector("#lock") is not None and pg.query_selector("#jp26") is None, "the page opens on the password screen, with no guide content")
    pg.fill("#pw", "not-the-password"); pg.click("#go"); pg.wait_for_timeout(2500)
    check(pg.query_selector("#jp26") is None and "didn't work" in pg.inner_text("#err"), "a wrong password is refused")
    pg.fill("#pw", PW); pg.click("#go"); pg.wait_for_timeout(3000)
    check(pg.query_selector("#jp26") is not None and shown(pg) == ["kyoto"], "the right password opens the guide on the linked tab")
    pg.evaluate("localStorage.getItem('jpguide-tries')") is None or check(False, "a right password clears the wrong-password count")
    pg.goto(URL + "#jp-city-osaka", wait_until="domcontentloaded"); pg.wait_for_timeout(2500)
    check(pg.query_selector("#jp26") is not None and shown(pg) == ["osaka"], "a remembered device opens straight away")
    ctx.close()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded"); pg.wait_for_timeout(500)
    for _ in range(lock.MAX_TRIES):
        pg.fill("#pw", "wrong"); pg.click("#go"); pg.wait_for_function("!document.getElementById('go').disabled || document.getElementById('pw').disabled", timeout=15000)
    check(pg.is_disabled("#pw") and "Too many" in pg.inner_text("#err"), f"{lock.MAX_TRIES} wrong passwords lock the form")
    pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(500)
    check(pg.is_disabled("#pw") and "Too many" in pg.inner_text("#err"), "the lockout survives a reload")
    pg.evaluate("localStorage.setItem('jpguide-tries', JSON.stringify({n: 0, until: Date.now() + 1500}))")
    pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    check(not pg.is_disabled("#pw"), "the form opens again when the lockout ends")
    ctx.close()

    print("Without JavaScript (tabs and filters must still work, checked on the page before locking):")
    pg = b.new_context(viewport={"width": 1280, "height": 900}, java_script_enabled=False).new_page()
    for c in CITIES:
        k = c["key"]
        pg.goto(PLAIN + f"#jp-city-{k}"); pg.wait_for_timeout(300)
        check(shown(pg) == [k], f"{k}: tab shows only its own section")
        check(visible_cards(pg, k) == len(c["places"]), f"{k}: all {len(c['places'])} cards visible")
        cat = pg.query_selector(f"#jp-city-{k} label[for^='{k}-jc-']:not([for='{k}-jc-all'])")
        if cat:
            cat.click(); pg.wait_for_timeout(200)
            n = visible_cards(pg, k)
            check(0 < n < len(c["places"]), f"{k}: category filter narrows the list ({n} shown)")
            pg.click(f"#jp-city-{k} .clr"); pg.wait_for_timeout(200)
        check(pg.query_selector(f"#jp-city-{k} .leaves .lvrow") is not None, f"{k}: autumn leaves forecast is shown")
        leaf = pg.query_selector(f"#jp-city-{k} label[for='{k}-jm-6']")   # the "Autumn leaves" mood chip
        if leaf:
            leaf.click(); pg.wait_for_timeout(200)
            n = visible_cards(pg, k)
            want = pg.evaluate(f"document.querySelectorAll('#jp-city-{k} .jp-bytype .card[data-tags*=\\'Autumn leaves\\']').length")
            check(n == want > 0, f"{k}: Autumn leaves filter shows the {want} leaves spots ({n} shown)")
            pg.click(f"#jp-city-{k} .clr"); pg.wait_for_timeout(200)
    ph = pg.query_selector(".card.hasph")
    if ph:   # a card photo opens full screen and closes again, without JavaScript, keeping its tab open
        k = ph.evaluate("e => e.closest('.city').id.replace('jp-city-', '')")
        pg.goto(PLAIN + f"#jp-city-{k}"); pg.wait_for_timeout(300)
        pg.click(".card.hasph .ph > a"); pg.wait_for_timeout(300)
        box = pg.query_selector(".phbox:target")
        ok = box is not None and box.evaluate("b => { const i = b.querySelector('img'); return i.complete && i.naturalWidth > 0; }")
        check(ok and shown(pg) == [k], f"{k}: card photo opens full screen and the image loads")
        if box:
            pg.click(".phbox:target .phclose", position={"x": 5, "y": 5}); pg.wait_for_timeout(300)
            check(pg.query_selector(".phbox:target") is None and shown(pg) == [k], f"{k}: tapping closes the photo")
    print("With JavaScript, dark mode, desktop:")
    errors = []
    pg = b.new_page(viewport={"width": 1280, "height": 900}, color_scheme="dark")
    pg.on("pageerror", lambda e: errors.append(str(e)))
    k = KEYS[0]
    open_page(pg, URL + f"#jp-city-{k}", 3500)
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
    open_page(p2, URL + f"#jp-city-{k}", 3000)
    p2.click(f"#jp-city-{k} .onmap[data-onmap='1']"); p2.wait_for_timeout(1200)
    check(p2.evaluate(f"document.querySelector('#{k}-maptog').checked"), "'Show on map' opens the folded map on a phone")
    check(p2.evaluate("document.documentElement.scrollWidth") <= 390, "no sideways scroll on a phone")
    p2.screenshot(path=os.path.join(SHOTS, "phone.png"))
    check(not errors, f"no script errors {errors if errors else ''}")
    b.close()

print("\nAll checks passed." if not problems else f"\n{len(problems)} problem(s): " + "; ".join(problems))
sys.exit(1 if problems else 0)
