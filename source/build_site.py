"""Builds the travel guide web page.

    python3 source/build_site.py

Writes:
  index.html                          the live page (GitHub Pages serves it at japan.zhunior.com)
  source/out/squarespace-v<VER>.html  the older Squarespace Code Block variant (no JavaScript), kept for reference

How the page works (details in docs/GUIDE.md):
  * Everything is generated from source/data.py (stops, hotels, places) and source/common.py (icons, art, maps).
  * Tabs switch stops with :target (plain anchor links); filters use hidden inputs + CSS :has(). No JS needed for these.
  * The GitHub version adds a small script for dark mode, the theme switch and the embedded Google map.
"""
import os, re, sys, itertools, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CATS, CITIES, LATER, TAGS, ICONS, ART, PIN, CAM, HEART, build_map, esc, tag_html, photos
import styles  # base stylesheet, scoped under #jp26

R = "#jp26"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUTDIR = os.path.join(HERE, "out")
os.makedirs(OUTDIR, exist_ok=True)
EXT = 'target="_blank" rel="noopener"'
MOODS = ["Must-go", "Quick bite", "Late night", "Low energy", "Outdoors", "Photo spot"]
CATKEYS = ["food", "sweets", "coffee", "drinks", "onsen", "sights", "trips"]
FILTER_MIN = 8  # show filters only when a city has this many places
JP_CHARS = "大阪絶対ごはん甘味珈琲乾杯温泉名所日帰り白浜京都彦根和歌山"


def card_cat(p): return "food" if p[0] == "must" else p[0]
def matches(p, c, M): return (c == "all" or card_cat(p) == c) and all(m in p[4] for m in M)


def card(city, i, p, view):
    cat, name, area, km, tags, desc, maps, pq = p[:8]
    c = CATS[cat]
    tags_h = "".join(tag_html(t) for t in tags)
    return f'''<article class="card" id="jp-{city['key']}-{view}-{i}" data-n="{i}" data-cat="{cat}" data-tags="{esc('|'.join(tags))}" style="--c:{c['color']}">
  <div class="num" aria-hidden="true">{i}</div>
  <div class="cbody">
    <h3>{esc(name)}</h3>
    <div class="meta"><span class="catlbl">{c['title']} · </span>{esc(area)} <span class="dot">•</span> {esc(km)}</div>
    {f'<div class="tags">{tags_h}</div>' if tags else ''}
    <p>{esc(desc)}</p>
    <div class="btns"><a class="btn" href="{esc(maps)}" {EXT}><span class="bi i-pin"></span>Open in Maps</a>
    <a class="btn ghost" href="{esc(photos(pq))}" {EXT}><span class="bi i-cam"></span>Photos</a>
    <button type="button" class="btn ghost onmap" data-onmap="{i}" hidden><span class="bi i-map"></span>Show on map</button></div>
  </div></article>'''


def by_type(city):
    num = {i + 1: p for i, p in enumerate(city["places"])}
    out = []
    for key, c in CATS.items():
        items = [(i, p) for i, p in num.items() if p[0] == key]
        if not items: continue
        icon = ICONS[city["icons"].get(key, c["icon"])]
        cards = "\n".join(card(city, i, p, "p") for i, p in items)
        out.append(f'''<section class="sec" data-cat-sec="{key}" style="--c:{c['color']};--t:{c['tint']}">
  <div class="sechead"><div class="secicon">{icon}</div>
    <div><div class="jp">{c['jp']}</div><h2>{city.get('titles', {}).get(key, c['title'])}</h2><p class="lead">{esc(city['leads'].get(key, ''))}</p></div></div>
  <div class="grid">{cards}</div>
</section>''')
    return "\n".join(out), [[p for p in city["places"] if p[0] == k] for k in CATS if any(p[0] == k for p in city["places"])]


def area_panel(city):
    num = {i + 1: p for i, p in enumerate(city["places"])}
    idx = {p[1]: i for i, p in num.items()}
    rows = []
    for name, dist, names in city["areas"]:
        chips = "".join(
            f'<a class="achip {pcls_for(num[idx[n]])}" data-pin="{idx[n]}" href="#jp-{city["key"]}-p-{idx[n]}" style="--c:{CATS[num[idx[n]][0]]["color"]}"><b>{idx[n]}</b>{esc(n)}</a>'
            for n in names)
        rows.append(f'<div class="arow"><div class="aname">{esc(name)}<span>{esc(dist)}</span></div><div class="achips">{chips}</div></div>')
    return (f'<details class="areas"><summary>Pick by area <span>places close together, to combine in one outing</span></summary>'
            f'<div class="arows">{"".join(rows)}</div></details>')


def pcls_for(p):
    return " ".join([f"pc-{card_cat(p)}"] + [f"pt-{MOODS.index(m)}" for m in p[4] if m in MOODS])


def by_area(city):
    num = {i + 1: p for i, p in enumerate(city["places"])}
    idx = {p[1]: i for i, p in num.items()}
    out, groups = [], []
    for name, dist, names in city["areas"]:
        cards = "\n".join(card(city, idx[n], num[idx[n]], "a") for n in names)
        groups.append([num[idx[n]] for n in names])
        out.append(f'''<section class="sec asec">
  <div class="ahead"><h2>{esc(name)}</h2><span>{esc(dist)} from the hotel</span></div>
  <div class="grid">{cards}</div>
</section>''')
    return "\n".join(out), groups


def minimal_failing(cards):
    out = []
    for c in ["all"] + CATKEYS:
        fails = []
        for r in range(len(MOODS) + 1):
            for M in itertools.combinations(MOODS, r):
                if any(matches(p, c, M) for p in cards): continue
                if any(set(F) <= set(M) for F in fails): continue
                fails.append(M)
        for M in fails:
            if c != "all" and any(cc == "all" and set(f) <= set(M) for cc, f in out): continue
            out.append((c, M))
    return out


def city_panel(city, nxt):
    k = city["key"]; P = city["places"]; n = len(P)
    filters = n >= FILTER_MIN
    pid = lambda s: f"{k}-{s}"
    tsec, tgroups = by_type(city)
    areas_h = area_panel(city) if city["areas"] else ""
    has_area = False
    agroups = []

    # ----- controls -----
    controls = ""
    if filters:
        seg = (f'<div class="seg"><input class="vh" type="radio" name="{pid("view")}" id="{pid("jv-type")}" checked><label for="{pid("jv-type")}">By type</label>'
               f'<input class="vh" type="radio" name="{pid("view")}" id="{pid("jv-area")}"><label for="{pid("jv-area")}">By area</label></div>') if has_area else ""
        present = [c for c in CATKEYS if any(card_cat(p) == c for p in P)]
        cats = [("all", "Everything", None)] + [(c, CATS[c]["title"] if c != "food" else "Food", CATS[c]["color"]) for c in present]
        cat_h = "".join(
            f'<input class="vh jc" type="radio" name="{pid("cat")}" id="{pid("jc-" + c)}"{" checked" if c == "all" else ""}>'
            f'<label class="chip" for="{pid("jc-" + c)}">{f"<i style=background:{col}></i>" if col else ""}{label}</label>' for c, label, col in cats)
        moods = [m for m in MOODS if any(m in p[4] for p in P)]
        mood_h = "".join(
            f'<input class="vh jm" type="checkbox" id="{pid("jm-" + str(MOODS.index(m)))}"><label class="chip mood{" must" if m == "Must-go" else ""}" for="{pid("jm-" + str(MOODS.index(m)))}">'
            f'{"<span class=ti>" + HEART + "</span>" if m == "Must-go" else ""}{esc(m)}<em>{sum(1 for p in P if m in p[4])}</em></label>' for m in moods)
        controls = f'''<form class="controls" id="{pid("f")}" action="#" autocomplete="off">
        <div class="ctrlhead"><h2>{city["planner"]}<span>pick by mood</span></h2>{seg}</div>
        <div class="row"><span class="rowlbl">Show</span>{cat_h}</div>
        <div class="row"><span class="rowlbl">Feeling</span>{mood_h}</div>
      </form>'''
        status = (f'<div class="status"><span class="cnt-all">All {n} places</span><span class="cnt-some">Showing <span class="cnt"></span> of {n}</span>'
                  f'<input type="reset" form="{pid("f")}" class="linkbtn clr" value="Clear filters"></div>')
        empty = '<div class="empty">Nothing matches all of those at once. Untick one, or tap <b>Clear filters</b>.</div>'
    else:
        controls = f'<div class="controls"><div class="ctrlhead"><h2>{city["planner"]}<span>{n} so far</span></h2></div><p class="soonnote">More places are on the way as research continues.</p></div>'
        status = empty = ""

    num_ = {i + 1: p for i, p in enumerate(P)}
    pcls = lambda i: pcls_for(num_[i])
    map_t = build_map(city, pin_href=lambda i: f"#jp-{k}-p-{i}", pin_class=pcls).replace('class="map"', 'class="map map-t"', 1)
    map_a = build_map(city, pin_href=lambda i: f"#jp-{k}-a-{i}", pin_class=pcls).replace('class="map"', 'class="map map-a"', 1) if has_area else ""

    day1 = ""
    if city["day1"]:
        day1 = f'<div class="box dark"><h3>{city["day1"][0]}</h3><p>{esc(city["day1"][1])}</p></div>'
    how = ""
    if city["stop"] == 1:
        how = ('<div class="box how"><h3>How this works</h3><p>Nothing here is planned by the hour. Each day, pick from the options by mood, '
               'energy and weather. Filter below, tap <b>Open in Maps</b> for directions, or <b>Photos</b> to see what a place looks like.</p></div>')
    if city.get("hotel2"):
        hotel_boxes = (f'<div class="box"><h3>Hotel 1 · {city["dates"]}</h3><p>{esc(city["hotel_name"])}, {esc(city["hotel_note"])}.</p>'
                       f'<a class="btn" style="--c:#3A2E2A" href="{esc(city["hotel"]["maps"])}" {EXT}><span class="bi i-pin"></span>Open in Maps</a></div>'
                       f'<div class="box"><h3>Hotel 2 · {city["hotel2_dates"]}</h3><p>{esc(city["hotel2_name"])}, {esc(city["hotel2_note"])}.</p>'
                       f'<a class="btn" style="--c:#3A2E2A" href="{esc(city["hotel2"]["maps"])}" {EXT}><span class="bi i-pin"></span>Open in Maps</a></div>')
    else:
        hotel_boxes = (f'<div class="box"><h3>{city.get("hotel_box_title") or "Home base · " + city["nights"]}</h3><p>{esc(city["hotel_name"])}, {esc(city["hotel_note"])}.</p>'
                       f'<a class="btn" style="--c:#3A2E2A" href="{esc(city["hotel"]["maps"])}" {EXT}><span class="bi i-pin"></span>Open in Maps</a></div>')
    basics_cls = "basics" if (how or city.get("hotel2")) else "basics two"
    nxt_h = ""
    if city.get("next_back"):
        b = city["next_back"]
        nxt_h = f'<a class="nextstop" href="#jp-city-{b[0]}">Next stop: <b>{b[1]}</b> <span>{b[2]} →</span></a>'
    elif nxt and nxt.get("optional"):
        after = CITIES[CITIES.index(nxt) + 1]
        nxt_h = (f'<a class="nextstop" href="#jp-city-{after["key"]}">Next stop: <b>{after["name"]}</b> <span>{after["dates"]} →</span></a>'
                 f'<a class="nextstop opt" href="#jp-city-{nxt["key"]}">Maybe on the way: <b>{nxt["name"]}</b> <span>optional stop →</span></a>')
    elif nxt:
        nxt_h = f'<a class="nextstop" href="#jp-city-{nxt["key"]}">Next stop: <b>{nxt["name"]}</b> <span>{nxt["dates"]} →</span></a>'
    else:
        nxt_h = '<a class="nextstop" href="#jp-city-osaka">Back to <b>Osaka</b> <span>←</span></a>'

    html = f'''<div class="city" id="jp-city-{k}">
  <section class="hero hero-{k}">
    <div class="txt">
      <div class="kicker">{city.get("kicker") or "Japan trip guide · stop " + str(city["stop"])}</div>
      <h1>{city["name"]}</h1>
      <div class="jpbig">{city["jp"]}</div>
      <div class="sub">{city["sub"]}</div>
      <div class="pill">{city.get("pill") or (city["dates"] + " · " + city["nights"] if not city.get("hotel2") else city["dates"] + " &amp; " + city["hotel2_dates"])}</div>
    </div>
    <div class="art">{ART[city["art"]]}</div>
  </section>
  <section class="{basics_cls}">
    {how}
    {hotel_boxes}
    {day1 or '<div class="box dark"><h3>Still researching</h3><p>Only a few places so far. More food and sights will be added before the trip.</p></div>'}
  </section>
  <div class="planner">
    <div class="maincol">
      {controls}
      <div class="jp-bytype">{tsec}</div>
      {areas_h}
      {status}
      {empty}
    </div>
    <aside class="mapcol">
      <div class="mapbox"><input class="vh maptog" type="checkbox" id="{pid("maptog")}"><label class="maphead" for="{pid("maptog")}">{city["name"]} at a glance <span>{n} places</span></label>
        <div class="mapbody">{map_t}{map_a}
        <p class="mapnote">Tap a pin to jump to that place. Distances are straight-line from {"hotel 1 / hotel 2" if city.get("hotel2") else ("JR Wakayama Station" if city.get("optional") else "the hotel")} (★).</p>
        <div class="gmap" data-city="{k}" hidden><div class="gmap-head"><span class="gmap-sel"></span><a class="gmap-open" href="#" {EXT}>Open in Google Maps</a></div>
          <iframe title="Google map of {esc(city["name"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          <a class="gmap-jump" href="#" hidden>Go to this place's card ↓</a></div></div>
      </div>
    </aside>
  </div>
  {nxt_h}
</div>'''

    # ----- per-city CSS -----
    C = f"{R} #jp-city-{k}"
    on = lambda i: f":has(#{pid(i)}:checked)"
    css = []
    if filters:
        rules = []
        for c in CATKEYS:
            sel = f'.card:not([data-cat="{c}"])' + (':not([data-cat="must"])' if c == "food" else "")
            rules.append(f"{C}{on('jc-' + c)} {sel}")
        for m in MOODS:
            rules.append(f'{C}{on("jm-" + str(MOODS.index(m)))} .card:not([data-tags*="{m}"])')
        css.append(",\n".join(rules) + " { display: none; }")

        def state_sel(c, M):
            return C + ("" if c == "all" else on("jc-" + c)) + "".join(on("jm-" + str(MOODS.index(m))) for m in M)
        g = []
        for cont, groups in ((".jp-bytype", tgroups), (".jp-byarea", agroups)):
            for gi, cards in enumerate(groups, 1):
                for c, M in minimal_failing(cards):
                    g.append(f"{state_sel(c, M)} {cont} > div:nth-child({gi})")
        if g: css.append(",\n".join(g) + " { display: none; }")
        css.append(",\n".join(f"{state_sel(c, M)} .empty" for c, M in minimal_failing(P)) + " { display: block; }")
        pins = [f'{C}{on("jc-" + c)} a[data-pin]:not(.pc-{c})' for c in CATKEYS]
        pins += [f'{C}{on("jm-" + str(j))} a[data-pin]:not(.pt-{j})' for j in range(len(MOODS))]
        css.append(",\n".join(pins) + " { opacity: .16; }")
        filt = f"{C}:has(.jm:checked, .jc:not(#{pid('jc-all')}):checked)"
        css.append(f"{filt} .cnt-all {{ display: none; }} {filt} .cnt-some {{ display: inline; }} {filt} .clr {{ display: inline; }}")
        if has_area:
            css.append(f"{C}:has(#{pid('jv-area')}:checked) .jp-byarea, {C}:has(#{pid('jv-area')}:checked) .map-a {{ display: block; }}")
            css.append(f"{C}:has(#{pid('jv-area')}:checked) .jp-bytype, {C}:has(#{pid('jv-area')}:checked) .map-t {{ display: none; }}")
            css.append(f"{C}:has(#{pid('jv-area')}:checked) .catlbl {{ display: inline; }}")
    return html, "\n".join(css)


VERSION = "1.2.1"
VDATE = "Oct 16, 2026"
CHANGELOG = [
    ("1.2.1", "Oct 16, 2026", "Stronger instructions telling search engines not to list, cache or preview the page."),
    ("1.2", "Oct 16, 2026", "Moved to japan.zhunior.com (GitHub Pages). Dark mode with an Auto/Dark/Light switch. Google map in every tab: tap a pin or Show on map."),
    ("1.1", "Oct 16, 2026", "New optional Wakayama stop tab (11 places from the Wakayama list plus Kishi, Awashima, Koyasan moved from Shirahama). Version numbers added."),
    ("1.0", "Oct 16, 2026", "Shirahama list added (12 places, new Hot springs section). Pick-by-area panels replace the By area view to keep the file small."),
]


def build():
    panels, city_css = [], []
    for i, city in enumerate(CITIES):
        nxt = CITIES[i + 1] if i + 1 < len(CITIES) else None
        h, c = city_panel(city, nxt)
        panels.append(h); city_css.append(c)

    tabs = "".join(f'<a class="tab{" opt" if c.get("optional") else ""}" href="#jp-city-{c["key"]}" data-city="{c["key"]}"><b>{c["name"]}</b><small>{c.get("tabdates", c["dates"])}</small></a>' for c in CITIES)
    tabs += "".join(f'<span class="tab off" aria-disabled="true" title="Coming soon"><b>{n}</b><small>{d}</small></span>' for n, d, *_ in LATER)
    later = "".join(f'<div class="lat" style="--c:{c}"><div class="latjp">{jp}</div><h3>{n}</h3>'
                    f'<div class="latd">{d}</div><div class="latn">{note}</div><span class="soon">Coming soon</span></div>'
                    for n, d, jp, c, note in LATER)

    body = f'''
<header class="bar"><div class="wrap">
  <a class="brand" href="#jp-city-osaka"><i></i>Japan<span>&nbsp;2026</span></a>
  <nav class="tabs" aria-label="Trip stops">{tabs}</nav>
</div></header>
<main class="wrap">
  {"".join(panels)}
  {"" if not LATER else '<section class="later">' + "<h2>Still to plan</h2><p>Options for the rest of the trip are on the way.</p>" + f'<div class="latgrid">{later}</div></section>'}
  <section class="later-old" hidden>
    <h2>Still to plan</h2>
    <p>Options for the rest of the trip are on the way.</p>
    <div class="latgrid">{later}</div>
  </section>
  <footer>Japan trip guide · Version {VERSION} · updated {VDATE}</footer>
</main>'''
    body = body.replace("<footer>", '<div class="foot">').replace("</footer>", "</div>")
    body = re.sub(r"<(/?)(header|main|nav|section|aside|article)\b", r"<\1div", body)

    keys = [c["key"] for c in CITIES]
    first = keys[0]
    targeted = ", ".join(f"#jp-city-{k}:target, #jp-city-{k} :target" for k in keys)
    city_switch = [f"{R} .city {{ display: none; scroll-margin-top: 110px; }}",
                   f"{R}:not(:has({targeted})) #jp-city-{first} {{ display: block; }}",
                   f"{R}:not(:has({targeted})) .tab[data-city=\"{first}\"] {{ background: var(--dark); color: var(--onDark); }}",
                   f"{R}:not(:has({targeted})) .tab[data-city=\"{first}\"] small {{ color: color-mix(in srgb, var(--onDark) 70%, transparent); }}"]
    for k in keys:
        city_switch.append(f"{R} #jp-city-{k}:target, {R} #jp-city-{k}:has(:target) {{ display: block; }}")
        city_switch.append(f"{R}:has(#jp-city-{k}:target, #jp-city-{k} :target) .tab[data-city=\"{k}\"] {{ background: var(--dark); color: var(--onDark); }}")
        city_switch.append(f"{R}:has(#jp-city-{k}:target, #jp-city-{k} :target) .tab[data-city=\"{k}\"] small {{ color: color-mix(in srgb, var(--onDark) 70%, transparent); }}")

    EXTRA = f'''
/* ---- no-JavaScript controls ---- */
{R} .vh {{ position: absolute; opacity: 0; width: 1px; height: 1px; margin: 0; pointer-events: none; }}
{R} label.chip {{ user-select: none; }}
{R} .vh:checked + label.chip {{ background: var(--dark); color: var(--onDark); border-color: var(--dark); }}
{R} .vh:checked + label.chip em {{ color: color-mix(in srgb, var(--onDark) 70%, transparent); }}
{R} .vh:checked + label.chip.must {{ background: #E2604A; border-color: #E2604A; color: #fff; }}
{R} .vh:checked + label.chip.must .ti svg {{ color: #fff; }}
{R} .vh:focus-visible + label {{ outline: 3px solid var(--sun); outline-offset: 2px; }}
{R} .seg label {{ padding: 7px 16px; border-radius: 99px; font-family: var(--display); font-weight: 500; font-size: 15px; cursor: pointer; }}
{R} .seg .vh:checked + label {{ background: var(--surface); box-shadow: 0 1px 3px rgba(0,0,0,.12); }}
{R} .clr {{ font: inherit; font-weight: 800; -webkit-appearance: none; appearance: none; display: none; }}
{R} .cnt-some {{ display: none; }}
{R} .maincol {{ display: flex; flex-direction: column; counter-reset: jpshown; }}
{R} .controls {{ order: 1; }} {R} .status {{ order: 2; }} {R} .jp-bytype, {R} .jp-byarea {{ order: 4; }} {R} .empty {{ order: 5; }}
{R} .card {{ counter-increment: jpshown; scroll-margin-top: 130px; }}
{R} .status {{ order: 2; margin-top: 12px; }}
{R} .cnt::after {{ content: counter(jpshown); }}
{R} .card:target {{ animation: jp26flash 1.6s ease-out; }}
{R} .jp-byarea, {R} .map-a {{ display: none; }}
{R} .areas {{ order: 3; margin-top: 16px; background: var(--surface); border: 1.5px solid var(--line); border-radius: var(--r); padding: 14px 16px; }}
{R} .areas summary {{ font-family: var(--display); font-weight: 600; font-size: 17px; cursor: pointer; display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }}
{R} .areas summary span {{ font-family: var(--body); font-size: 13px; font-weight: 700; color: var(--muted); }}
{R} .areas summary::after {{ content: "Show ▸"; margin-left: auto; font-family: var(--body); font-size: 13px; font-weight: 800; color: var(--accent); }}
{R} .areas[open] summary::after {{ content: "Hide ▾"; }}
{R} .arows {{ display: grid; gap: 10px; margin-top: 12px; }}
{R} .arow {{ border-top: 1.5px dashed var(--line); padding-top: 10px; }}
{R} .aname {{ font-family: var(--display); font-weight: 600; font-size: 15px; display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; }}
{R} .aname span {{ font-family: var(--body); font-weight: 700; font-size: 12.5px; color: var(--muted); }}
{R} .achips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }}
{R} .achip {{ display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 800; padding: 3px 10px 3px 3px; border-radius: 99px;
  background: var(--chip); border: 1px solid var(--line); text-decoration: none; color: var(--ink); transition: opacity .2s; }}
{R} .achip b {{ background: var(--c); color: #fff; border-radius: 50%; width: 21px; height: 21px; display: inline-flex; align-items: center; justify-content: center;
  font-family: var(--display); font-weight: 600; font-size: 11.5px; }}
{R} .achip:hover {{ border-color: var(--muted); }}
{R} .empty {{ display: none; }}
{R} .latgrid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
@media (max-width: 680px) {{ {R} .latgrid {{ grid-template-columns: minmax(0, 1fr); }} }}
{R} .soonnote {{ color: var(--muted); font-weight: 700; font-size: 14px; margin-top: 6px; }}
{R} .basics.two {{ grid-template-columns: 1fr 1fr; }}
{R} .tab {{ color: var(--ink); }}
{R} .map .mriver {{ stroke: #A9D3E0; }}
{R} .bi {{ width: 15px; height: 15px; display: inline-block; background: currentColor; flex: none; }}
{R} .i-pin {{ -webkit-mask: url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 22s7-7.2 7-12.2A7 7 0 0 0 5 9.8C5 14.8 12 22 12 22z M12 7.2a2.6 2.6 0 1 0 0 5.2a2.6 2.6 0 1 0 0-5.2z' fill-rule='evenodd'/%3E%3C/svg%3E\") center / contain no-repeat; mask: url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 22s7-7.2 7-12.2A7 7 0 0 0 5 9.8C5 14.8 12 22 12 22z M12 7.2a2.6 2.6 0 1 0 0 5.2a2.6 2.6 0 1 0 0-5.2z' fill-rule='evenodd'/%3E%3C/svg%3E\") center / contain no-repeat; }}
{R} .i-cam {{ -webkit-mask: url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'%3E%3Cpath d='M4 8h3l1.6-2.4h6.8L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z'/%3E%3Ccircle cx='12' cy='13' r='3.4'/%3E%3C/svg%3E\") center / contain no-repeat; mask: url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'%3E%3Cpath d='M4 8h3l1.6-2.4h6.8L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z'/%3E%3Ccircle cx='12' cy='13' r='3.4'/%3E%3C/svg%3E\") center / contain no-repeat; }}
{R} .i-map {{ -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'%3E%3Cpath d='M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14'/%3E%3C/svg%3E") center / contain no-repeat; mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linejoin='round'%3E%3Cpath d='M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14'/%3E%3C/svg%3E") center / contain no-repeat; }}
{R} .nextstop.opt {{ margin-top: 10px; border-style: dashed; }}
{R} .tab.opt {{ border: 1.5px dashed var(--muted); padding: 4.5px 12.5px; }}
{R} .tab.opt small {{ font-style: italic; }}
{R} .hero-wakayama {{ background: linear-gradient(170deg, #FFF2DC, #FAD9B4 60%, #F5C5A0); border: 2px dashed #E0B892; }}
{R} .hero-hikone {{ background: linear-gradient(170deg, #FFF0D8, #F8D6AE 60%, #F2C096); }}
{R} .hero-kyoto {{ background: linear-gradient(170deg, #FFE6CF, #F7C7A6 60%, #F1AE8E); }}
{R} .hero-shirahama .txt {{ position: relative; z-index: 1; }}
@media (min-width: 681px) {{ {R} .hero-shirahama .art svg {{ overflow: hidden !important; }} {R} .hero-shirahama .sea-full {{ display: none; }} {R} .hero-shirahama .sea-fade {{ display: inline; }} }}
{R} .hero-shirahama {{ background: linear-gradient(170deg, #FFE7CC, #F8C9A8 60%, #F4B79A); }}
{R} .nextstop {{ display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 34px; padding: 18px; border-radius: var(--r);
  background: var(--surface); border: 1.5px solid var(--line); font-family: var(--display); font-size: 18px; color: var(--ink); }}
{R} .nextstop b {{ font-weight: 600; color: var(--accent); }}
{R} .nextstop span {{ color: var(--muted); font-size: 15px; }}
{R} .nextstop:hover {{ border-color: var(--muted); }}
{R} .maphead {{ font-family: var(--display); font-weight: 600; font-size: 19px; display: flex; justify-content: space-between; align-items: center; }}
{R} .maphead span {{ font-family: var(--body); font-size: 13px; font-weight: 700; color: var(--muted); }}
@media (max-width: 1020px) {{
  {R} .maphead {{ cursor: pointer; }}
  {R} .maphead::after {{ content: "Show ▸"; font-family: var(--body); font-size: 13px; font-weight: 800; color: var(--accent); margin-left: 8px; }}
  {R} .maptog:checked + .maphead::after {{ content: "Hide ▾"; }}
  {R} .mapbody {{ display: none; }}
  {R} .maptog:checked ~ .mapbody {{ display: block; }}
}}
@media (max-width: 680px) {{ {R} .basics.two {{ grid-template-columns: minmax(0, 1fr); }} {R} .maphead span {{ display: none; }} }}
{chr(10).join(city_switch)}
{chr(10).join(city_css)}
'''
    fonts_import = ('@import url("https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Nunito:wght@400;700;800&display=swap");\n'
                    '@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@700;900&display=swap&text=' + urllib.parse.quote(JP_CHARS) + '");\n')
    base = styles.scoped_css().replace(":where(h1,", ":where(form, h1,")
    css = fonts_import + base + EXTRA
    log = "\n".join(f"  v{v} ({dt}): {txt}" for v, dt, txt in CHANGELOG)
    snippet = f'''<!-- Japan trip guide · VERSION {VERSION} · {VDATE}
  Paste everything into a Squarespace Code Block (HTML mode). No JavaScript needed.
Changes:
{log}
-->
<style>{css}</style>
<div id="jp26">{body}</div>
'''
    assert "<script" not in snippet
    visible = re.sub(r"<style>.*?</style>", "", snippet, flags=re.S)
    for bad in (r"\bPhil\b", "Sicong", "—", "–"):
        assert not re.search(bad, visible), bad
    open(os.path.join(OUTDIR, f"squarespace-v{VERSION}.html"), "w").write(snippet)
    # ---------- GitHub Pages version: same page + dark mode + Google map (needs JavaScript) ----------
    import json as _json
    jpdata = {}
    for c in CITIES:
        hs = [c["hotel"]] + ([c["hotel2"]] if c.get("hotel2") else [])
        jpdata[c["key"]] = {
            "hotels": [{"name": (c["hotel_name"] if i == 0 else c["hotel2_name"]), "lat": h["lat"], "lon": h["lon"], "url": h["maps"]} for i, h in enumerate(hs)],
            "places": {str(i + 1): {"name": p[1], "lat": p[8], "lon": p[9], "url": p[6]} for i, p in enumerate(c["places"])},
        }
    DARK = ("--bg: #1C1613; --surface: #28201C; --surface2: #221B17; --ink: #F4E8DA; --soft: #E2CDB8; --muted: #B29D8D; "
            "--line: #3B302A; --chip: #362B25; --accent: #F07261; --dark: #F4E8DA; --onDark: #2A211C; --hero1: #3B2A2B; --hero2: #5E3B34; "
            "--mapgrid: #3E3330; --maplbl: #8C7869; --day: #4A3229; color-scheme: dark;")
    HEROES = (".hero-shirahama {{ background: linear-gradient(170deg, #3A2A30, #5B3A3A 60%, #6A4038); }} "
              ".hero-kyoto {{ background: linear-gradient(170deg, #3B2A2B, #5E3934 60%, #6E3F35); }} "
              ".hero-hikone {{ background: linear-gradient(170deg, #2F2E26, #4A3F30 60%, #5A4733); }} "
              ".hero-wakayama {{ background: linear-gradient(170deg, #3A2E2A, #5A4234 60%, #684A38); border-color: #8A6A50; }}").replace("{{", "{").replace("}}", "}")
    def dark_block(pre):
        heroes = " ".join(f"{pre} #jp26 {h.strip()}" for h in HEROES.split("} ") if h.strip())
        heroes = heroes.replace("#jp26 .hero", "#jp26 .hero").replace(")", ")").rstrip("}") + "}"
        return f"{pre} #jp26 {{ {DARK} }} {pre}, {pre} body {{ background: #1C1613; }} " + " ".join(
            f"{pre} #jp26 {x.strip()}{'' if x.strip().endswith('}') else '}'}" for x in HEROES.split("} ") if x.strip())
    GH_CSS = f'''
html, body {{ margin: 0; background: #FFF8EE; }}
@media (prefers-color-scheme: dark) {{ {dark_block('html:not([data-theme="light"])')} }}
{dark_block('html[data-theme="dark"]')}
#jp26 .bar {{ position: sticky; top: 0; z-index: 20; }}
#jp26 .bar .wrap {{ gap: 12px; }}
#jp26 .themebtn {{ flex: none; border: 1.5px solid var(--line); background: var(--surface); color: var(--ink); border-radius: 99px; padding: 6px 12px;
  font-family: var(--display); font-weight: 500; font-size: 14px; cursor: pointer; }}
#jp26 .themebtn:hover {{ border-color: var(--muted); }}
@media (max-width: 680px) {{ #jp26 .themebtn {{ font-size: 12.5px; padding: 5px 10px; }} }}
#jp26 .basics .btn {{ background: var(--dark); border-color: var(--dark); color: var(--onDark); }}
@media (min-width: 1021px) {{ #jp26 .mapcol {{ max-height: calc(100vh - 100px); overflow: auto; scrollbar-width: thin; }}
  #jp26 .map {{ max-height: calc(100vh - 480px); min-height: 240px; }} }}
#jp26 .gmap {{ margin-top: 12px; border-radius: 16px; overflow: hidden; border: 1.5px solid var(--line); background: var(--surface2); }}
#jp26 .gmap-head {{ display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 9px 12px; font-size: 13.5px; font-weight: 800; flex-wrap: wrap; }}
#jp26 .gmap-sel {{ font-family: var(--display); font-weight: 600; font-size: 15px; }}
#jp26 .gmap-open, #jp26 .gmap-jump {{ color: var(--accent); text-decoration: underline; text-underline-offset: 3px; font-weight: 800; font-size: 13px; }}
#jp26 .gmap iframe {{ display: block; width: 100%; height: 300px; border: 0; }}
#jp26 .gmap-jump {{ display: block; padding: 9px 12px; }}
#jp26 .map a.sel .mpin {{ stroke: var(--ink); stroke-width: 1.2; }}
'''
    GH_JS = """
(() => {
  const D = __DATA__;
  const root = document.getElementById("jp26"); if (!root) return;
  const html = document.documentElement;
  // theme: auto (follows the phone) / dark / light
  const KEY = "jpguide-theme";
  const get = () => { try { return localStorage.getItem(KEY) || "auto"; } catch (e) { return "auto"; } };
  const set = v => { try { localStorage.setItem(KEY, v); } catch (e) {} };
  const btn = root.querySelector(".themebtn");
  const LABEL = { auto: "Theme · Auto", dark: "Theme · Dark", light: "Theme · Light" };
  const apply = v => { if (v === "auto") html.removeAttribute("data-theme"); else html.setAttribute("data-theme", v); if (btn) btn.textContent = LABEL[v]; };
  apply(get());
  if (btn) { btn.hidden = false; btn.addEventListener("click", () => { const order = ["auto", "dark", "light"]; const v = order[(order.indexOf(get()) + 1) % 3]; set(v); apply(v); }); }
  root.querySelectorAll(".onmap, .gmap").forEach(el => el.hidden = false);
  root.querySelectorAll(".mapnote").forEach(el => el.textContent = "Tap a pin to see it on the Google map below. Distances are straight-line from the starred point.");
  const src = (lat, lon, z) => `https://maps.google.com/maps?q=${lat},${lon}&z=${z}&hl=en&output=embed`;
  function show(city, n, scroll) {
    const box = root.querySelector(`.gmap[data-city="${city}"]`); if (!box) return;
    const d = D[city]; const p = n ? d.places[n] : d.hotels[0]; if (!p) return;
    box.querySelector("iframe").src = src(p.lat, p.lon, n ? 16 : 14);
    box.querySelector(".gmap-sel").textContent = n ? `${n} · ${p.name}` : `★ ${p.name}`;
    box.querySelector(".gmap-open").href = p.url;
    const j = box.querySelector(".gmap-jump");
    if (n) { j.hidden = false; j.href = `#jp-${city}-p-${n}`; } else j.hidden = true;
    root.querySelectorAll(`#jp-city-${city} .map a[data-pin]`).forEach(a => a.classList.toggle("sel", a.dataset.pin === String(n)));
    if (scroll) {
      const tog = root.querySelector(`#${city}-maptog`); if (tog && !tog.checked && matchMedia("(max-width: 1020px)").matches) tog.checked = true;
      const smooth = !matchMedia("(prefers-reduced-motion: reduce)").matches;
      box.scrollIntoView({ behavior: smooth ? "smooth" : "auto", block: "center" });
    }
  }
  function visibleCity() {
    const h = decodeURIComponent(location.hash || "");
    let m = h.match(/^#jp-city-([a-z]+)$/) || h.match(/^#jp-([a-z]+)-p-[0-9]+$/);
    if (m && D[m[1]]) return m[1];
    const c = root.querySelector(".city"); return c ? c.id.replace("jp-city-", "") : null;
  }
  function lazy() { const c = visibleCity(); if (!c) return; const f = root.querySelector(`.gmap[data-city="${c}"] iframe`); if (f && !f.getAttribute("src")) show(c, null, false); }
  root.addEventListener("click", e => {
    const pin = e.target.closest(".map a[data-pin]");
    if (pin) { e.preventDefault(); const c = pin.closest(".city").id.replace("jp-city-", ""); show(c, pin.dataset.pin, false); return; }
    const b = e.target.closest(".onmap");
    if (b) { const c = b.closest(".city").id.replace("jp-city-", ""); show(c, b.dataset.onmap, true); }
  });
  window.addEventListener("hashchange", () => setTimeout(lazy, 50));
  lazy(); window.addEventListener("load", lazy);
})();
""".replace("__DATA__", _json.dumps(jpdata, ensure_ascii=False))
    gh_body = snippet.replace('<nav class="tabs"', '<nav class="tabs"', 1)
    gh_body = re.sub(r'(<div class="tabs" aria-label="Trip stops">.*?</div>)', r'\1<button type="button" class="themebtn" hidden aria-label="Switch light or dark theme">Theme · Auto</button>', gh_body, count=1, flags=re.S)
    gh_body = gh_body.replace("Paste everything into a Squarespace Code Block (HTML mode). No JavaScript needed.", "GitHub Pages version (japan.zhunior.com), with dark mode and Google maps.")
    gh_page = (f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet">
<meta name="bingbot" content="noindex, nofollow, noarchive">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="color-scheme" content="light dark">
<title>Japan Trip Guide</title>
<style>{GH_CSS}</style>
</head><body>
{gh_body}
<script>{GH_JS}</script>
</body></html>
''')
    open(os.path.join(REPO, "index.html"), "w").write(gh_page)
    print(f"index.html v{VERSION}: {len(gh_page):,} characters")
    print(f"squarespace variant: {len(snippet):,} characters (Squarespace Code Block limit is about 300,000)")


if __name__ == "__main__":
    build()
