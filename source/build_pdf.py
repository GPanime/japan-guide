"""Older printable PDF (Osaka and Shirahama only, 120 x 213 mm pages). Not kept in sync with the web page.

    python3 source/build_pdf.py source/out/Guide.pdf
Needs Playwright with Chromium, and the Fredoka and Nunito font files in ~/.fonts.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
OUT = sys.argv[1]

# ---------- html ----------
def card(i, p):
    cat, name, area, km, tags, desc, maps, pq = p[:8]
    c = CATS[cat]
    tags_h = "".join(tag_html(t) for t in tags)
    return f'''<div class="card" style="--c:{c['color']};--t:{c['tint']}">
  <div class="num">{i}</div>
  <div class="cbody">
    <h3>{esc(name)}</h3>
    <div class="meta">{esc(area)} <span class="dot">•</span> {esc(km)}</div>
    {f'<div class="tags">{tags_h}</div>' if tags else ''}
    <p>{esc(desc)}</p>
    <div class="btns"><a class="btn" href="{esc(maps)}"><span class="bi">{PIN}</span>Open in Maps</a>
    <a class="btn ghost" href="{esc(photos(pq))}"><span class="bi">{CAM}</span>Photos</a></div>
  </div></div>'''

def section(city, key):
    c = CATS[key]
    items = [(i + 1, p) for i, p in enumerate(city["places"]) if p[0] == key]
    if not items: return ""
    cards = "\n".join(card(i, p) for i, p in items)
    title = city.get("titles", {}).get(key, c["title"])
    icon = ICONS[city["icons"].get(key, c["icon"])]
    return f'''<section class="sec" style="--c:{c['color']};--t:{c['tint']}">
  <div class="sechead"><div class="secicon">{icon}</div>
    <div><div class="jp">{c['jp']}</div><h2>{title}</h2></div></div>
  <p class="lead">{esc(city['leads'].get(key, ''))}</p>
  {cards}
</section>'''

def areas_html():
    num = {i + 1: p for i, p in enumerate(P)}
    rows = []
    for name, dist, names in AREAS:
        ids = [IDX[n] for n in names]
        chips = "".join(
            f'<a class="achip" href="{esc(num[i][6])}" style="--c:{CATS[num[i][0]]["color"]}"><b>{i}</b>{esc(num[i][1])}</a>'
            for i in ids)
        rows.append(f'<div class="arow"><div class="aname">{esc(name)}<span>{esc(dist)}</span></div><div class="achips">{chips}</div></div>')
    return "\n".join(rows)

legend_html = "".join(f'<div class="lg">{tag_html(t)}<span>{esc(d)}</span></div>' for t, d in TAGS)
catkey_html = "".join(f'<span class="ck"><i style="background:{c["color"]}"></i>{c["title"]}</span>' for c in CATS.values())

later_html = "".join(f'<div class="lat" style="--c:{c}"><div class="latdot"></div><div><div class="latjp">{jp}</div>'
                     f'<h3>{n}</h3><div class="meta">{d}</div></div></div>' for n, d, jp, c, _ in LATER)

def city_pages(city):
    secs = "\n".join(section(city, k) for k in CATS)
    return f'''
<div class="cover cover-{city['key']}">
  <div class="top">
    <div class="kicker">Japan trip guide · stop {city['stop']}</div>
    <h1>{city['name']}</h1>
    <div class="jpbig">{city['jp']}</div>
    <div class="sub">{city['sub']}</div>
    <div class="pill">{city['dates']}, 2026 · {city['nights']}</div>
  </div>
  {ART[city['art']]}
</div>
<div class="glance">
  <div class="pagehead"><h2>{city['name']} at a glance</h2><span class="hand">{city['dates']}</span></div>
  <div class="box" style="--c:{INK}"><h3>Home base · {city['nights']}</h3>
    <div class="meta">{esc(city['hotel_name'])} · {esc(city['hotel_note'])}</div>
    <div class="btns" style="margin-top:2mm"><a class="btn" href="{esc(city['hotel']['maps'])}"><span class="bi">{PIN}</span>Open in Maps</a></div></div>
  <div class="box day1"><span class="hand">Still researching</span>
    <p style="margin:1mm 0 0">Only a few places so far. More food and sights will be added before the trip.</p></div>
  {build_map(city).replace('class="map"', 'class="map map-sq"', 1)}
  <div class="mapnote">Tap a pin to open it in Maps. Distances are straight-line from the hotel.</div>
</div>
{secs}'''

CSS = f'''
@font-face {{ font-family: Fredoka; src: url("file://{FONTS}/Fredoka.ttf"); font-weight: 300 700; }}
@font-face {{ font-family: Nunito; src: url("file://{FONTS}/Nunito.ttf"); font-weight: 200 1000; }}
@page {{ size: 120mm 213mm; margin: 11mm 10mm 12mm; background: #FFF8EE; }}
@page cover {{ margin: 0; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
html {{ background: #FFF8EE; }}
body {{ margin: 0; font-family: Nunito, sans-serif; color: {INK}; font-size: 9.4pt; line-height: 1.45; }}
a {{ color: inherit; text-decoration: none; }}
h1, h2, h3 {{ font-family: Fredoka, sans-serif; font-weight: 600; margin: 0; }}
.jp {{ font-family: "Noto Sans CJK JP", sans-serif; font-weight: 700; }}
.hand {{ font-family: Fredoka, sans-serif; font-weight: 500; }}

.cover {{ page: cover; width: 120mm; height: 213mm; position: relative; overflow: hidden;
  background: linear-gradient(180deg, #FFE2C6 0%, #FFD3B4 55%, #FBC1A3 100%); break-after: page; }}
.cover .top {{ padding: 16mm 12mm 0; }}
.cover .kicker {{ font-family: Fredoka; font-weight: 500; letter-spacing: .18em; font-size: 8pt; text-transform: uppercase; color: #A2533E; }}
.cover h1 {{ font-size: 44pt; line-height: .95; margin-top: 3mm; color: #3A2E2A; }}
.cover .jpbig {{ font-family: "Noto Sans CJK JP"; font-weight: 900; font-size: 20pt; color: #D9483B; margin-top: 1mm; letter-spacing: .1em; }}
.cover .sub {{ font-family: Fredoka; font-weight: 400; font-size: 13pt; color: #6A4A3C; margin-top: 3mm; line-height: 1.3; }}
.coverart {{ position: absolute; left: 0; right: 0; bottom: 0; width: 120mm; }}
.cover .pill {{ display: inline-block; margin-top: 5mm; background: #fff; border: 1.6px solid {INK}; border-radius: 99px; padding: 1.2mm 3.6mm;
  font-family: Fredoka; font-weight: 500; font-size: 9pt; }}

.pagehead {{ display: flex; align-items: baseline; gap: 3mm; margin-bottom: 3mm; }}
.pagehead h2 {{ font-size: 18pt; }}
.pagehead .hand {{ font-size: 9.5pt; color: #C0674D; }}
.box {{ background: #fff; border-radius: 5mm; padding: 3.4mm 4.2mm; border: 1.4px solid #F0E2CF; margin-bottom: 3mm; }}
.box h3 {{ font-size: 11pt; margin-bottom: 1.5mm; }}
.lgrid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 3mm; }}
.lg {{ display: flex; flex-direction: column; align-items: flex-start; gap: .5mm; margin: 1.1mm 0; font-size: 7.8pt; line-height: 1.2; color: #6B5A50; }}
.lg .tag {{ }}
.ck {{ display: inline-flex; align-items: center; gap: 1.4mm; margin: 0 3mm 1mm 0; font-size: 8.6pt; font-weight: 700; }}
.ck i {{ width: 3mm; height: 3mm; border-radius: 50%; display: inline-block; }}
.day1 {{ background: #3A2E2A; color: #FFF3E3; border: none; }}
.day1 .hand {{ color: #F7B267; font-size: 11pt; }}

.tags {{ display: flex; flex-wrap: wrap; gap: 1.2mm; margin: 1.4mm 0 1.6mm; }}
.tag {{ display: inline-flex; align-items: center; gap: .8mm; font-size: 7.4pt; font-weight: 800; padding: .5mm 2.2mm; border-radius: 99px;
  background: #F3ECE3; color: #6B5A50; }}
.tag.must {{ background: #E2604A; color: #fff; }}
.ti svg {{ width: 2.6mm; height: 2.6mm; display: block; }}

.sec {{ break-before: page; }}
.sechead {{ display: flex; align-items: center; gap: 3.5mm; }}
.secicon {{ width: 17mm; height: 17mm; border-radius: 50%; background: var(--t); display: flex; align-items: center; justify-content: center;
  border: 1.6px solid var(--c); flex: none; }}
.secicon svg {{ width: 12mm; height: 12mm; }}
.sechead h2 {{ font-size: 21pt; color: var(--c); line-height: 1; }}
.sechead .jp {{ font-size: 8pt; color: var(--c); opacity: .8; letter-spacing: .3em; }}
.lead {{ font-family: Fredoka; font-weight: 400; font-size: 10.5pt; line-height: 1.35; margin: 2.5mm 0 4mm; color: #6A4A3C; }}

.card {{ display: flex; gap: 3mm; background: #fff; border-radius: 5mm; padding: 3.6mm 4mm 3.8mm 3.4mm; margin-bottom: 3.6mm;
  border: 1.4px solid #F0E2CF; box-shadow: 0 1.2mm 0 var(--t); break-inside: avoid; position: relative; }}
.card::before {{ content: ""; position: absolute; left: 0; top: 4mm; bottom: 4mm; width: 1.2mm; border-radius: 0 2mm 2mm 0; background: var(--c); }}
.num {{ flex: none; width: 7.4mm; height: 7.4mm; border-radius: 50%; background: var(--c); color: #fff; font-family: Fredoka; font-weight: 600;
  font-size: 10pt; display: flex; align-items: center; justify-content: center; margin-left: 1.2mm; }}
.cbody {{ flex: 1; min-width: 0; }}
.card h3 {{ font-size: 12pt; line-height: 1.15; }}
.meta {{ font-size: 8.2pt; color: #8A766A; font-weight: 700; margin-top: .4mm; }}
.meta .dot {{ color: var(--c); }}
.card p {{ margin: 0 0 2.4mm; }}
.meta + p {{ margin-top: 1.6mm !important; }}
.btns {{ display: flex; gap: 2mm; }}
.btn {{ display: inline-flex; align-items: center; gap: 1.2mm; background: var(--c); color: #fff; font-family: Fredoka; font-weight: 500;
  font-size: 8.6pt; padding: 1.3mm 3.4mm; border-radius: 99px; }}
.btn.ghost {{ background: #fff; color: var(--c); border: 1.3px solid var(--c); }}
.bi svg {{ width: 3.4mm; height: 3.4mm; display: block; }}

.mapwrap {{ break-before: page; }}
.map {{ width: 100mm; height: 150mm; display: block; }}
.map .area {{ font-family: Fredoka; font-weight: 600; font-size: 2.6px; letter-spacing: .12em; fill: #B79E88; }}
.map .pinnum {{ font-family: Fredoka; font-weight: 600; font-size: 3.1px; fill: #fff; }}
.map .hotel {{ font-size: 3.6px; fill: #F7B267; }}
.map .hotellbl {{ font-family: Fredoka; font-size: 3.4px; fill: {INK}; font-weight: 600; }}
.map .far {{ font-family: Fredoka; font-size: 2.8px; font-weight: 500; fill: {INK}; }}
.map .scale {{ font-family: Fredoka; font-size: 2.6px; fill: #8A766A; }}
.mapnote {{ font-size: 8.2pt; color: #8A766A; margin-top: 2mm; }}

.areas {{ break-before: page; }}
.arow {{ background: #fff; border-radius: 4mm; padding: 1.5mm 3.2mm; margin-bottom: 1.3mm; border: 1.4px solid #F0E2CF; break-inside: avoid; }}
.aname {{ font-family: Fredoka; font-weight: 600; font-size: 10.5pt; display: flex; justify-content: space-between; align-items: baseline; }}
.aname span {{ font-family: Nunito; font-weight: 700; font-size: 7.8pt; color: #8A766A; }}
.achips {{ display: flex; flex-wrap: wrap; gap: 1mm; margin-top: .7mm; }}
.achip {{ display: inline-flex; align-items: center; gap: 1.2mm; font-size: 8pt; font-weight: 700; padding: .5mm 2.4mm .5mm .6mm;
  border-radius: 99px; background: #FBF5EC; border: 1px solid #EEE1CF; }}
.achip b {{ background: var(--c); color: #fff; border-radius: 50%; width: 4.4mm; height: 4.4mm; display: inline-flex; align-items: center;
  justify-content: center; font-family: Fredoka; font-weight: 600; font-size: 7pt; }}

.later {{ break-before: page; }}
.glance {{ break-before: page; }}
.map.map-sq {{ width: 100mm; height: 100mm; margin-top: 1mm; }}
.cover-shirahama {{ background: linear-gradient(180deg, #FFE7CC 0%, #F8C9A8 60%, #F4B79A 100%); }}
.cover .coverart {{ overflow: hidden; }}
.lat {{ display: flex; gap: 4mm; align-items: center; padding: 3.4mm 0; border-bottom: 1.4px dashed #E6D3BC; }}
.latdot {{ width: 5mm; height: 5mm; border-radius: 50%; background: var(--c); flex: none; box-shadow: 0 0 0 2mm #fff, 0 0 0 2.4mm var(--c); margin: 0 2mm; }}
.lat h3 {{ font-size: 13pt; }}
.latjp {{ font-family: "Noto Sans CJK JP"; font-weight: 700; color: var(--c); font-size: 8pt; letter-spacing: .3em; }}
.soon {{ font-family: Fredoka; font-weight: 500; font-size: 11pt; color: #C0674D; margin-top: 6mm; text-align: center; }}
'''

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><title>Japan Trip Guide</title><style>{CSS}</style></head><body>

<div class="cover">
  <div class="top">
    <div class="kicker">Japan trip guide · stop 1</div>
    <h1>Osaka</h1>
    <div class="jpbig">大阪</div>
    <div class="sub">curry, coffee, takoyaki &amp;<br>a torii with a view</div>
    <div class="pill">Nov 16-20, 2026 · 4 nights</div>
  </div>
  {COVER_ART}
</div>

<div class="pagehead"><h2>How this works</h2><span class="hand">no schedules!</span></div>
<div class="box"><p style="margin:0">Nothing here is planned by the hour. Each day, pick from the options by mood, energy and weather.
Tap <b>Open in Maps</b> for directions and opening hours, or <b>Photos</b> to see what a place looks like.
Numbers match the map on the next page.</p></div>
<div class="box"><h3>Colours</h3>{catkey_html}<h3 style="margin-top:2.6mm">Tags</h3><div class="lgrid">{legend_html}</div></div>
<div class="box" style="--c:{INK}"><h3>Home base · all four nights</h3>
  <div class="meta">Best Western Plus Hotel Fino Osaka Kitahama · by Kitahama station</div>
  <div class="btns" style="margin-top:2mm"><a class="btn" href="{esc(HOTEL['maps'])}"><span class="bi">{PIN}</span>Open in Maps</a></div></div>
<div class="box day1"><span class="hand">Day 1 · Mon Nov 16</span>
  <p style="margin:1mm 0 0">Late arrival, so just a late dinner. Easiest is something near the hotel. With energy left, the Namba bars are about 2.5 km away, a short taxi ride.</p></div>

<div class="mapwrap">
  <div class="pagehead"><h2>Osaka at a glance</h2><span class="hand">Nov 17-19</span></div>
  {build_map(OSAKA)}
  <div class="mapnote">Tap a pin to open it in Maps. Distances in the guide are straight-line from the hotel.</div>
</div>

<div class="areas">
  <div class="pagehead"><h2>Pick by area</h2><span class="hand">combine what's close</span></div>
  {areas_html()}
</div>

{"".join(section(OSAKA, k) for k in CATS)}
{city_pages(SHIRAHAMA)}

<div class="later">
  <div class="pagehead"><h2>Still to plan</h2><span class="hand">coming soon</span></div>
  {later_html}
  <div class="soon">more pages on the way ✿</div>
</div>
</body></html>'''

open(OUT.replace(".pdf", ".html"), "w").write(HTML)
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto("file://" + OUT.replace(".pdf", ".html"))
    pg.wait_for_timeout(500)
    pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True)
    b.close()
print("ok")
