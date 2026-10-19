"""Google My Maps import files, one KML per stop, from the guide data.

    python3 source/build_mymaps.py   ->  source/out/mymaps/*.kml
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import CATS, CITIES, photos

ICON = "https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png"
STAR = "https://www.gstatic.com/mapspro/images/stock/1000-star.png"

def kml_color(hexrgb):            # #RRGGBB -> aabbggrr
    h = hexrgb.lstrip("#")
    return "ff" + h[4:6] + h[2:4] + h[0:2]

def esc(s): return html.escape(s, quote=False)

out = []
for n, city in enumerate(CITIES, 1):
    styles = []
    for key, c in CATS.items():
        styles.append(f'''<Style id="cat-{key}"><IconStyle><color>{kml_color(c["color"])}</color><scale>1.1</scale><Icon><href>{ICON}</href></Icon></IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style>''')
    styles.append(f'''<Style id="hotel"><IconStyle><color>ff2a2e3a</color><scale>1.3</scale><Icon><href>{STAR}</href></Icon></IconStyle></Style>''')
    marks = []
    hotels = [(city["hotel"], city["hotel_name"], city["dates"])]
    if city.get("hotel2"):
        hotels.append((city["hotel2"], city["hotel2_name"], city["hotel2_dates"]))
    for k, (h, name, dates) in enumerate(hotels, 1):
        label = "Hotel" if len(hotels) == 1 else f"Hotel {k}"
        marks.append(f'''<Placemark><name>{esc(label)} · {esc(name)}</name><styleUrl>#hotel</styleUrl>
<description>{esc(f"Where we stay, {dates}. Google Maps: {h['maps']}")}</description>
<ExtendedData><Data name="Category"><value>Hotel</value></Data></ExtendedData>
<Point><coordinates>{h["lon"]},{h["lat"]},0</coordinates></Point></Placemark>''')
    for i, p in enumerate(city["places"], 1):
        cat, name, area, km, tags, desc, maps, pq, lat, lon = p
        ctitle = city.get("titles", {}).get(cat, CATS[cat]["title"])
        lines = [f"{ctitle} · {area} · {km}"]
        if tags: lines.append("Tags: " + ", ".join(tags))
        lines += ["", desc, "", f"Google Maps: {maps}", f"Photos: {photos(pq)}"]
        marks.append(f'''<Placemark><name>{i} · {esc(name)}</name><styleUrl>#cat-{cat}</styleUrl>
<description>{esc(chr(10).join(lines))}</description>
<ExtendedData><Data name="Category"><value>{esc(ctitle)}</value></Data><Data name="Number"><value>{i}</value></Data></ExtendedData>
<Point><coordinates>{lon},{lat},0</coordinates></Point></Placemark>''')
    doc = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>{esc(city["name"])} · {esc(city.get("tabdates", city["dates"]))}</name>
{"".join(styles)}
{chr(10).join(marks)}
</Document></kml>
'''
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "mymaps"); os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"Map_{n}_{city['name']}.kml")
    open(path, "w").write(doc)
    out.append((path, len(city["places"]) + len(hotels)))
for p, c in out: print(os.path.basename(p), c, "pins")
