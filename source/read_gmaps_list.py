"""Read a shared Google Maps list into JSON (name, your note, coordinates, Maps link, distances).

    python3 source/read_gmaps_list.py https://maps.app.goo.gl/XXXX  [base_lat base_lon]  > list.json

The list must be shared with "Anyone with the link". Google Maps renders lists with JavaScript, so this
opens the link in headless Chromium (Playwright) and captures the list data the page downloads
(an "entitylist/getlist" response), which holds every place at once, including the note you wrote on it.

Each entry also gets a Google Maps link built from the place id (maps.google.com/?cid=...).
If base coordinates are given (for example the hotel), each entry gets a straight-line distance in km.
"""
import json, math, sys
from playwright.sync_api import sync_playwright


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    return 2 * 6371 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


def read_list(url):
    captured = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(locale="en-US", viewport={"width": 1300, "height": 1000})
        page.on("response", lambda r: captured.append(r.text()) if "entitylist/getlist" in r.url else None)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)
        browser.close()
    if not captured:
        raise SystemExit("No list data captured. Is the list shared with 'Anyone with the link'?")
    raw = captured[0]
    if raw.startswith(")]}'"):
        raw = raw[raw.index("\n") + 1:]
    data = json.loads(raw)[0]
    title, entries = data[4], data[8]
    places = []
    for x in entries:
        info = x[1]
        lat, lon = info[5][2], info[5][3]
        cid = int(info[6][1]) & ((1 << 64) - 1)          # the place id, as an unsigned number
        places.append({"name": x[2], "note": x[3] or "", "lat": lat, "lon": lon,
                       "address": info[4] or info[2] or "", "maps": f"https://maps.google.com/?cid={cid}"})
    return title, places


if __name__ == "__main__":
    title, places = read_list(sys.argv[1])
    if len(sys.argv) >= 4:
        base = (float(sys.argv[2]), float(sys.argv[3]))
        for p in places:
            p["km"] = round(km(base, (p["lat"], p["lon"])), 1)
    json.dump({"list": title, "count": len(places), "places": places}, sys.stdout, ensure_ascii=False, indent=1)
