import math, os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from data import HOTEL, CATS, P, AREAS, TAGS, OUTLIERS, photos, CITIES, OSAKA, SHIRAHAMA, LATER
IDX = {p[1]: i + 1 for i, p in enumerate(P)}

INK = "#3A2E2A"
FONTS = os.path.expanduser("~/.fonts")

def esc(s): return html.escape(s, quote=True)

# ---------- icons (original, simple) ----------
S = f'stroke="{INK}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"'
ICONS = {
 "curry": f'''<svg viewBox="0 0 64 64"><path d="M22 14 q3 -4 0 -8 M30 12 q3 -4 0 -8" fill="none" {S} opacity=".45"/>
   <ellipse cx="32" cy="42" rx="27" ry="10" fill="#fff" {S}/>
   <ellipse cx="23" cy="36" rx="13" ry="9" fill="#fff" {S}/>
   <path d="M29 41 Q34 27 50 31 Q60 37 52 44 Q40 49 29 41Z" fill="#D9842F" {S}/>
   <circle cx="44" cy="36" r="2.4" fill="#F4C26B"/><circle cx="38" cy="40" r="2" fill="#E8654A"/></svg>''',
 "takoyaki": f'''<svg viewBox="0 0 64 64"><path d="M6 40 L58 40 L51 52 L13 52Z" fill="#EBC995" {S}/>
   <circle cx="19" cy="34" r="9" fill="#E09A45" {S}/><circle cx="45" cy="34" r="9" fill="#E09A45" {S}/>
   <circle cx="32" cy="29" r="9.5" fill="#E09A45" {S}/>
   <path d="M12 32 q4 -3 8 0 t8 -4 t8 0 t8 4 t8 0" fill="none" stroke="#6B3A1F" stroke-width="2.6" stroke-linecap="round"/>
   <circle cx="27" cy="24" r="1.3" fill="#5E9E6E"/><circle cx="37" cy="26" r="1.3" fill="#5E9E6E"/><circle cx="47" cy="30" r="1.3" fill="#5E9E6E"/></svg>''',
 "coffee": f'''<svg viewBox="0 0 64 64"><path d="M24 14 q3 -4 0 -8 M32 13 q3 -4 0 -8" fill="none" {S} opacity=".45"/>
   <ellipse cx="30" cy="52" rx="24" ry="5" fill="#fff" {S}/>
   <path d="M12 22 H48 V36 Q48 50 30 50 Q12 50 12 36Z" fill="#fff" {S}/>
   <path d="M48 26 Q58 26 56 34 Q54 40 47 40" fill="none" {S}/>
   <ellipse cx="30" cy="23" rx="17" ry="3.2" fill="#B07A52"/>
   <path d="M30 27 c-3 -4 -8 0 0 6 c8 -6 3 -10 0 -6Z" fill="#F7E7D8"/></svg>''',
 "glass": f'''<svg viewBox="0 0 64 64"><path d="M18 8 H46 Q46 30 32 34 Q18 30 18 8Z" fill="#fff" {S}/>
   <path d="M19.5 16 H44.5 Q43 29 32 32 Q21 29 19.5 16Z" fill="#9B5FB8"/>
   <path d="M32 34 V52 M22 54 H42" fill="none" {S}/>
   <circle cx="26" cy="21" r="1.6" fill="#fff" opacity=".7"/><circle cx="36" cy="25" r="1.2" fill="#fff" opacity=".7"/></svg>''',
 "torii": f'''<svg viewBox="0 0 64 64"><path d="M6 14 Q32 6 58 14 L56 20 Q32 13 8 20Z" fill="#D9483B" {S}/>
   <rect x="12" y="25" width="40" height="5" rx="1" fill="#D9483B" {S}/>
   <path d="M17 18 L15 56 M47 18 L49 56" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
   <path d="M17 18 L15 56 M47 18 L49 56" fill="none" stroke="#D9483B" stroke-width="3" stroke-linecap="round"/>
   <rect x="29" y="17" width="6" height="9" fill="#F6E3C6" {S}/></svg>''',
}

PIN = '<svg viewBox="0 0 24 24"><path d="M12 22s7-7.2 7-12.2A7 7 0 0 0 5 9.8C5 14.8 12 22 12 22z" fill="currentColor"/><circle cx="12" cy="9.8" r="2.6" fill="#fff"/></svg>'
CAM = '<svg viewBox="0 0 24 24"><path d="M4 8h3l1.6-2.4h6.8L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.4" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
HEART = '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" fill="currentColor"/></svg>'

COVER_ART = f'''<svg viewBox="0 0 200 170" class="coverart">
  <circle cx="132" cy="62" r="34" fill="#F7B267"/>
  <circle cx="132" cy="62" r="34" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 7" opacity=".7"/>
  <path d="M14 48 q8 -10 18 -4 q6 -8 16 -2 q10 0 8 8 H14Z" fill="#fff" opacity=".9"/>
  <path d="M150 28 q6 -8 14 -3 q5 -6 12 -1 q8 0 6 6 H150Z" fill="#fff" opacity=".9"/>
  <path d="M0 132 Q40 92 82 116 Q120 82 160 108 Q182 98 200 106 V170 H0Z" fill="#F4A98F"/>
  <path d="M0 148 Q50 120 100 140 Q150 118 200 136 V170 H0Z" fill="#E98A72"/>
  <g transform="translate(62 70)">
    <path d="M-4 10 Q38 0 80 10 L77 18 Q38 9 -1 18Z" fill="#D9483B" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
    <rect x="4" y="26" width="68" height="7" rx="1.5" fill="#D9483B" stroke="{INK}" stroke-width="2.6"/>
    <path d="M12 16 L9 74 M64 16 L67 74" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
    <path d="M12 16 L9 74 M64 16 L67 74" stroke="#D9483B" stroke-width="5" stroke-linecap="round"/>
    <rect x="33" y="15" width="10" height="12" fill="#FFF3E0" stroke="{INK}" stroke-width="2.4"/>
  </g>
  <g fill="#fff" opacity=".85"><circle cx="30" cy="96" r="2"/><circle cx="176" cy="82" r="1.6"/><circle cx="20" cy="70" r="1.4"/></g>
  <g transform="translate(26 118) rotate(-18)"><ellipse rx="5" ry="2.6" fill="#E0642F"/></g>
  <g transform="translate(176 126) rotate(24)"><ellipse rx="5" ry="2.6" fill="#E9A23B"/></g>
  <g transform="translate(160 150) rotate(-30)"><ellipse rx="4" ry="2.1" fill="#D9483B"/></g>
</svg>'''

# ---------- extra icons / art for Shirahama ----------
ICONS["sushi"] = f'''<svg viewBox="0 0 64 64"><ellipse cx="32" cy="50" rx="27" ry="6" fill="#fff" {S}/>
   <rect x="9" y="30" width="22" height="13" rx="6" fill="#FBF6EC" {S}/>
   <path d="M8 31 Q20 22 32 31 Q22 36 8 31Z" fill="#F08A5D" {S}/>
   <path d="M13 29 l3 3 M19 27 l3 4 M25 28 l3 3" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
   <rect x="34" y="27" width="21" height="16" rx="4" fill="#3B4A3E" {S}/>
   <ellipse cx="44.5" cy="27" rx="10.5" ry="4" fill="#FBF6EC" {S}/>
   <circle cx="44.5" cy="27" r="2.6" fill="#E2604A"/></svg>'''

ICONS["dango"] = f'''<svg viewBox="0 0 64 64"><path d="M14 54 L52 12" stroke="#C99A62" stroke-width="3.4" stroke-linecap="round"/>
   <circle cx="21" cy="46" r="8.5" fill="#9CC48A" {S}/><circle cx="32" cy="34" r="8.5" fill="#FFF6EA" {S}/><circle cx="43" cy="22" r="8.5" fill="#F4A3BE" {S}/>
   <circle cx="40" cy="19" r="1.8" fill="#fff" opacity=".8"/></svg>'''

def _leaf(x, y, s, r, col):
    return (f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M0 -10 L2.4 -4 L8.5 -6 L5 -1 L10 2 L4 2.6 L5 8 L0 4.4 L-5 8 L-4 2.6 L-10 2 L-5 -1 L-8.5 -6 L-2.4 -4Z" '
            f'fill="{col}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/><path d="M0 4.4 L0 11" stroke="{INK}" stroke-width="1.2"/></g>')

KYOTO_ART = f'''<svg viewBox="0 0 200 170" class="coverart">
  <circle cx="150" cy="52" r="24" fill="#F7B267"/>
  <circle cx="150" cy="52" r="24" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 7" opacity=".7"/>
  <path d="M10 40 q8 -10 18 -4 q6 -8 16 -2 q10 0 8 8 H10Z" fill="#fff" opacity=".9"/>
  <path d="M0 124 Q50 96 100 116 Q150 92 200 112 V170 H0Z" fill="#EFA27F"/>
  <path d="M0 146 Q60 124 120 142 Q160 130 200 140 V170 H0Z" fill="#E1866A"/>
  <g transform="translate(92 30)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round">
    <path d="M8 4 L8 -6" stroke-linecap="round"/><circle cx="8" cy="-8" r="2" fill="#F7B267"/>
    <path d="M-6 10 L22 10 L16 4 L0 4Z" fill="#5A3B32"/><rect x="0" y="10" width="16" height="9" fill="#D9483B"/>
    <path d="M-10 24 L26 24 L19 18 L-3 18Z" fill="#5A3B32"/><rect x="-1" y="24" width="18" height="10" fill="#D9483B"/>
    <path d="M-14 39 L30 39 L22 33 L-6 33Z" fill="#5A3B32"/><rect x="-2" y="39" width="20" height="11" fill="#D9483B"/>
    <path d="M-18 55 L34 55 L25 49 L-9 49Z" fill="#5A3B32"/><rect x="-3" y="55" width="22" height="12" fill="#D9483B"/>
    <path d="M-22 72 L38 72 L28 65 L-12 65Z" fill="#5A3B32"/><rect x="-4" y="72" width="24" height="18" fill="#D9483B"/>
    <rect x="4" y="78" width="8" height="12" fill="#FFF3E0"/>
  </g>
  {_leaf(36, 84, 1.2, -20, "#E2604A")}{_leaf(62, 104, .9, 25, "#E9A23B")}{_leaf(170, 96, 1.1, 15, "#D9483B")}
  {_leaf(184, 136, .8, -35, "#E9A23B")}{_leaf(22, 140, .9, 40, "#D9483B")}{_leaf(150, 150, .7, -10, "#E2604A")}
</svg>'''

ICONS["onsen"] = f'''<svg viewBox="0 0 64 64"><path d="M22 26 q-5 -6 0 -12 q5 -6 0 -12 M32 26 q-5 -6 0 -12 q5 -6 0 -12 M42 26 q-5 -6 0 -12 q5 -6 0 -12" fill="none" stroke="#E2604A" stroke-width="3.2" stroke-linecap="round"/>
   <path d="M8 34 H56 Q56 54 32 54 Q8 54 8 34Z" fill="#8FB4E8" {S}/><path d="M14 40 q6 -3 12 0 t12 0 t12 0" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>'''

ICONS["train"] = f'''<svg viewBox="0 0 64 64"><rect x="14" y="10" width="36" height="38" rx="8" fill="#5FA8C2" {S}/>
   <rect x="19" y="16" width="26" height="13" rx="3" fill="#E9F5F9" {S}/><circle cx="23" cy="38" r="3" fill="#FFE08A" {S}/><circle cx="41" cy="38" r="3" fill="#FFE08A" {S}/>
   <path d="M20 48 L14 56 M44 48 L50 56 M17 53 H47" fill="none" {S}/></svg>'''

HIKONE_ART = f'''<svg viewBox="0 0 200 170" class="coverart">
  <circle cx="44" cy="54" r="22" fill="#F7B267"/>
  <circle cx="44" cy="54" r="22" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 7" opacity=".7"/>
  <path d="M130 34 q8 -10 18 -4 q6 -8 16 -2 q10 0 8 8 H130Z" fill="#fff" opacity=".9"/>
  <path d="M0 132 Q50 108 100 124 Q150 104 200 120 V170 H0Z" fill="#9CC48A"/>
  <path d="M0 150 Q60 132 120 148 Q160 138 200 146 V170 H0Z" fill="#7DAF6E"/>
  <g transform="translate(100 40)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round">
    <path d="M-40 92 L-32 62 L32 62 L40 92Z" fill="#B9A894"/>
    <path d="M-34 74 H34 M-37 84 H37" stroke-width="1.6" fill="none" opacity=".7"/>
    <rect x="-26" y="40" width="52" height="22" fill="#FFF8EE"/>
    <path d="M-34 42 Q0 30 34 42 L28 36 Q0 26 -28 36Z" fill="#4A4A55"/>
    <rect x="-18" y="18" width="36" height="18" fill="#FFF8EE"/>
    <path d="M-26 20 Q0 8 26 20 L20 14 Q0 4 -20 14Z" fill="#4A4A55"/>
    <path d="M-12 14 L0 2 L12 14Z" fill="#4A4A55"/>
    <rect x="-20" y="46" width="6" height="8" fill="#4A4A55"/><rect x="-3" y="46" width="6" height="8" fill="#4A4A55"/><rect x="14" y="46" width="6" height="8" fill="#4A4A55"/>
    <rect x="-10" y="22" width="5" height="7" fill="#4A4A55"/><rect x="5" y="22" width="5" height="7" fill="#4A4A55"/>
  </g>
  {_leaf(30, 110, 1.0, -20, "#E2604A")}{_leaf(176, 100, 1.1, 15, "#E9A23B")}{_leaf(160, 146, .8, -30, "#D9483B")}{_leaf(40, 150, .8, 30, "#E9A23B")}
</svg>'''

WAKAYAMA_ART = f'''<svg viewBox="0 0 200 170" class="coverart">
  <circle cx="150" cy="56" r="24" fill="#F7B267"/>
  <circle cx="150" cy="56" r="24" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 7" opacity=".7"/>
  <path d="M18 44 q8 -10 18 -4 q6 -8 16 -2 q10 0 8 8 H18Z" fill="#fff" opacity=".9"/>
  <path d="M0 104 Q40 84 80 98 Q120 80 160 94 Q182 88 200 92 V130 H0Z" fill="#B8CF96"/>
  <rect x="0" y="128" width="200" height="42" fill="#7FB8C9"/>
  <g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".8"><path d="M20 146 q6 -4 12 0 t12 0"/><path d="M120 156 q6 -4 12 0 t12 0"/></g>
  <rect x="0" y="122" width="200" height="6" fill="#8C7A6B"/>
  <g stroke="{INK}" stroke-width="2.2" stroke-linejoin="round">
    <path d="M24 120 V102 Q24 94 34 94 H70 V120Z" fill="#F4F1EA"/>
    <rect x="74" y="94" width="44" height="26" rx="3" fill="#F4F1EA"/>
    <rect x="122" y="94" width="44" height="26" rx="3" fill="#F4F1EA"/>
    <path d="M24 112 H166" stroke="#E2604A" stroke-width="3"/>
    <rect x="34" y="99" width="9" height="7" fill="#9FCBD6"/><rect x="48" y="99" width="9" height="7" fill="#9FCBD6"/>
    <rect x="80" y="99" width="9" height="7" fill="#9FCBD6"/><rect x="94" y="99" width="9" height="7" fill="#9FCBD6"/>
    <rect x="128" y="99" width="9" height="7" fill="#9FCBD6"/><rect x="142" y="99" width="9" height="7" fill="#9FCBD6"/>
  </g>
</svg>'''

ART = {"osaka": COVER_ART, "wakayama": WAKAYAMA_ART, "kyoto": KYOTO_ART, "hikone": HIKONE_ART, "shirahama": f'''<svg viewBox="0 0 200 170" class="coverart" style="overflow:visible">
  <circle cx="58" cy="70" r="26" fill="#F7B267"/>
  <circle cx="58" cy="70" r="26" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 7" opacity=".7"/>
  <path d="M120 40 q8 -10 18 -4 q6 -8 16 -2 q10 0 8 8 H120Z" fill="#fff" opacity=".9"/>
  <defs><linearGradient id="shfade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#7FB8C9" stop-opacity="0"/><stop offset=".45" stop-color="#7FB8C9"/></linearGradient>
    <linearGradient id="shfade2" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#9FCBD6" stop-opacity="0"/><stop offset=".45" stop-color="#9FCBD6"/></linearGradient></defs>
  <g class="sea-full"><path d="M-800 96 H1000 V400 H-800Z" fill="#7FB8C9"/><path d="M-800 96 H1000 V104 H-800Z" fill="#9FCBD6"/></g>
  <g class="sea-fade" display="none"><path d="M0 96 H200 V170 H0Z" fill="url(#shfade)"/><path d="M0 96 H200 V104 H0Z" fill="url(#shfade2)"/></g>
  <g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".8">
    <path d="M70 112 q6 -4 12 0 t12 0"/><path d="M96 122 q6 -4 12 0 t12 0"/><path d="M58 136 q6 -4 12 0 t12 0"/></g>
  <path d="M84 170 L96 128 Q130 112 200 118 V170Z" fill="#D9B48A" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
  <path d="M100 140 Q140 128 200 132 M94 154 Q140 142 200 147 M108 128 Q150 120 200 124" fill="none" stroke="#B88E62" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M86 166 q10 -8 22 -2" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".9"/>
  <g transform="translate(150 96)"><path d="M0 0 q4 -8 8 0" fill="none" stroke="{INK}" stroke-width="1.6"/><path d="M10 -6 q4 -8 8 0" fill="none" stroke="{INK}" stroke-width="1.6"/></g>
</svg>'''}


# ---------- map ----------
_MAPN = 0
def build_map(city, pin_href=None, pin_class=None):
    pin_class = pin_class or (lambda i: "")
    places = city["places"]; hotel = city["hotel"]; m = city["map"]
    num = {i + 1: p for i, p in enumerate(places)}
    idx = {p[1]: i for i, p in num.items()}
    pin_href = pin_href or (lambda i: num[i][6])
    out_names = [n for o in m["outliers"] for n in (o[0] if isinstance(o[0], list) else [o[0]])]
    hotels = [hotel] + ([city["hotel2"]] if city.get("hotel2") else [])
    central = [i for i in num if num[i][1] not in out_names]
    lats = [num[i][8] for i in central] + [h["lat"] for h in hotels]
    lons = [num[i][9] for i in central] + [h["lon"] for h in hotels]
    W, H, k = m["W"], m["H"], m["k"]
    cl = math.cos(math.radians(sum(lats) / len(lats)))
    cx_lon = (min(lons) + max(lons)) / 2
    cy_lat = (min(lats) + max(lats)) / 2
    def xy(lat, lon):
        return (W / 2 + (lon - cx_lon) * 111.32 * cl * k, H / 2 + m["ycenter_shift"] - (lat - cy_lat) * 111.0 * k)
    anchors = {i: xy(num[i][8], num[i][9]) for i in central}
    hxy = [xy(h["lat"], h["lon"]) for h in hotels]
    hx, hy = hxy[0]
    pos = {i: list(a) for i, a in anchors.items()}
    R = 3.0
    fixed = [(x, y, 3.4) for x, y in hxy]
    for _ in range(600):
        for i in central:
            fx = (anchors[i][0] - pos[i][0]) * 0.04
            fy = (anchors[i][1] - pos[i][1]) * 0.04
            for j in central:
                if i == j: continue
                dx = pos[i][0] - pos[j][0]; dy = pos[i][1] - pos[j][1]
                d = math.hypot(dx, dy) or 0.01
                if d < 2 * R + 1.2:
                    push = (2 * R + 1.2 - d) * 0.5
                    fx += dx / d * push; fy += dy / d * push
            for (ax, ay, ar) in fixed:
                dx = pos[i][0] - ax; dy = pos[i][1] - ay
                d = math.hypot(dx, dy) or 0.01
                if d < R + ar + 1.2:
                    push = (R + ar + 1.2 - d) * 0.6
                    fx += dx / d * push; fy += dy / d * push
            pos[i][0] += fx; pos[i][1] += fy
    parts = [f'<svg viewBox="0 0 {W:g} {H:g}" class="map" style="aspect-ratio:{W:g}/{H:g}" xmlns="http://www.w3.org/2000/svg">',
             f'<rect x="0" y="0" width="{W:g}" height="{H:g}" rx="6" class="mbg" fill="#FFFDF8" stroke="#EADCC8" stroke-width=".5"/>']
    global _MAPN
    _MAPN += 1
    gid = f"jpdots{_MAPN}"
    parts.append(f'<defs><pattern id="{gid}" x="2.5" y="2.5" width="5" height="5" patternUnits="userSpaceOnUse">'
                 f'<circle cx="2.5" cy="2.5" r=".22" class="mgrid" fill="#E6D6C1"/></pattern></defs>'
                 f'<rect x="2.5" y="2.5" width="{W - 5:g}" height="{H - 5:g}" fill="url(#{gid})"/>')
    if m.get("river"):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (xy(la, lo) for la, lo in m["river"]))
        parts.append(f'<polyline points="{pts}" class="mriver" fill="none" stroke="#A9D3E0" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    for t, la, lo, anc in m["labels"]:
        x, y = xy(la, lo)
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" class="area">{t}</text>')
    for i in central:
        ax, ay = anchors[i]; px, py = pos[i]
        if math.hypot(px - ax, py - ay) > 0.8:
            parts.append(f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{px:.2f}" y2="{py:.2f}" stroke="{INK}" stroke-width=".3" opacity=".55" class="mlead"/>')
    for i in central:
        ax, ay = anchors[i]
        parts.append(f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r=".8" class="manchor" fill="{INK}"/>')
    for hi, (hx_, hy_) in enumerate(hxy):
        lbl = city.get("hotel_label", "hotel") if len(hxy) == 1 else f"hotel {hi + 1}"
        parts.append(f'<g><circle cx="{hx_:.2f}" cy="{hy_:.2f}" r="3.4" class="mhotel" fill="{INK}"/>'
                     f'<text x="{hx_:.2f}" y="{hy_ + 1.25:.2f}" text-anchor="middle" class="hotel">★</text>'
                     f'<text x="{hx_ + 4.4:.2f}" y="{hy_ + 1.1:.2f}" class="hotellbl">{lbl}</text></g>')
    for i in central:
        px, py = pos[i]; c = CATS[num[i][0]]["color"]
        parts.append(f'<a href="{esc(pin_href(i))}" data-pin="{i}" class="{pin_class(i)}"><circle cx="{px:.2f}" cy="{py:.2f}" r="{R}" class="mpin" fill="{c}" stroke="#fff" stroke-width=".6"/>'
                     f'<text x="{px:.2f}" y="{py + 1.05:.2f}" text-anchor="middle" class="pinnum">{i}</text></a>')
    for spec in m["outliers"]:
        names, y, lbl = spec[:3]; side = spec[3] if len(spec) > 3 else "right"
        names = names if isinstance(names, list) else [names]
        step = 7.0
        for k_, name in enumerate(names):
            o = idx[name]; c = CATS[num[o][0]]["color"]
            x0 = (W - 8 - k_ * step) if side == "right" else (8 + k_ * step)
            parts.append(f'<a href="{esc(pin_href(o))}" data-pin="{o}" class="{pin_class(o)}"><g transform="translate({x0:g} {y})"><circle r="3" class="mpin" fill="{c}" stroke="#fff" stroke-width=".6"/>'
                         f'<text y="1.05" text-anchor="middle" class="pinnum">{o}</text></g></a>')
        n = len(names)
        tx, anc = ((W - 8 - (n - 1) * step - 4.6), "end") if side == "right" else ((8 + (n - 1) * step + 4.6), "start")
        parts.append(f'<text x="{tx:g}" y="{y + 1.2:g}" text-anchor="{anc}" class="far">{lbl}</text>')
    sk = k * m["scale_km"]
    parts.append(f'<g transform="translate({W - 17 - sk:g} {H - 6:g})"><line x1="0" y1="0" x2="{sk:g}" y2="0" class="mscale" stroke="{INK}" stroke-width=".6"/>'
                 f'<line x1="0" y1="-1" x2="0" y2="1" class="mscale" stroke="{INK}" stroke-width=".6"/><line x1="{sk:g}" y1="-1" x2="{sk:g}" y2="1" class="mscale" stroke="{INK}" stroke-width=".6"/>'
                 f'<text x="{sk + 2:g}" y="1" class="scale">{m["scale_lbl"]}</text></g>')
    parts.append(f'<text x="{W - 6:g}" y="{H - 12:g}" text-anchor="end" class="scale">N ↑</text>')
    parts.append('</svg>')
    return "".join(parts)


# ---------- shared html bits ----------
def tag_html(t):
    cls = "tag must" if t == "Must-go" else "tag"
    ic = f'<span class="ti">{HEART}</span>' if t == "Must-go" else ""
    return f'<span class="{cls}">{ic}{esc(t)}</span>'

