"""Autumn leaves forecast for each stop, from two forecasters. build_site.py draws it as a timeline in every tab
and adds a line to matching cards.

How to refresh it (details in docs/GUIDE.md, "Autumn leaves forecast"):
  1. Weathernews: open each spot page (weathernews.jp/koyo/spot/<id>/; the ids are in WN_IDS below). It says
     見頃予想 "見頃 X月Y日頃〜" (peak from) and "落葉はじめ X月Y日頃" (leaves start to fall).
  2. tenki.jp (Japan Weather Association): open each spot page (tenki.jp/kouyou/6/<pref>/<id>.html; prefecture lists
     at tenki.jp/kouyou/6/). It says 今年の見頃予想, a period to the nearest ten days such as "11月下旬～12月上旬".
     Copy it as it is; it's turned into dates when the page is built.
  3. Update the dates below, CHECKED and the verdicts, then rebuild. Stay badges are worked out from the dates.

SPOTS[city] lists forecast spots in the order shown: (name, Weathernews peak "M/D", Weathernews falling "M/D", tenki.jp period).
Either source can be missing (None for Weathernews, "" for tenki.jp).
SHOW[city] picks the two or three spots drawn in the tab's panel, to give the overall picture. The rest of SPOTS is kept
as reference (and for NOTES).
CARDS[city] links a card (by its name in data.py) to a spot: those cards get the "Autumn leaves" filter tag.
NOTES[city] is a short line shown on a card, only where its timing stands out from the rest of the area.
"""
import datetime as _dt
import re as _re

YEAR = 2026
CHECKED = "Nov 9, 2026"
START, END = "11/1", "12/20"          # the chart's date range

SOURCES = [
    ("Weathernews", "https://weathernews.jp/koyo/area/kinki/"),
    ("tenki.jp", "https://tenki.jp/kouyou/expectation.html"),
    ("tenki.jp spots", "https://tenki.jp/kouyou/6/"),
    ("Nippon Kisho", "https://www.nippon.com/ja/japan-data/h02888/"),
    ("JMA", "https://www.data.jma.go.jp/sakura/data/phn_014.html"),
]
# One line on the city-level forecasts, shown under the sources.
CONTEXT = ("City-level forecasts for when the maples are fully red: Kyoto Dec 11, Osaka Dec 4, Wakayama Dec 11 (Nippon Kisho). "
           "The usual dates are Kyoto Dec 5, Osaka Dec 1, Nara Nov 21, Hikone Nov 28 (Japan Meteorological Agency).")

# the days we are there (or could go, for optional stops): (label, first day, last day)
STAYS = {
    "osaka": [("Our stay", "11/16", "11/20")],
    "wakayama": [("Our stop", "11/20", "11/20")],
    "shirahama": [("Our stay", "11/20", "11/23")],
    "kyoto": [("Stay 1", "11/23", "11/27"), ("Stay 2", "11/29", "12/2")],
    "nara": [("Osaka", "11/17", "11/19"), ("Kyoto 1", "11/24", "11/26"), ("Kyoto 2", "11/30", "12/1")],   # days we could go, from each base
    "shiga": [("Our stay", "11/27", "11/29")],
}

VERDICT = {
    "osaka": "A bit early: Katsuo-ji in Minoh peaks from about Nov 20, our last day, and the city parks only from about Nov 22, just after we leave.",
    "wakayama": "Too early in the city (from about Nov 30). Koyasan is earlier: its leaves start falling around Nov 16, before Nov 20.",
    "shirahama": "Not a leaves stop: the nearest spots inland peak after we leave.",
    "kyoto": "The best timing of the trip. Most temples now peak from about Nov 23-26: the first stay catches the start, and the second stay should be at its best.",
    "nara": "Nara Park peaks from about Nov 20 into early December, so any day from Nov 20 works. The Kasugayama hike is right behind the park.",
    "shiga": "Good timing for the temples near Hikone: Koto Sanzan and Eigen-ji peak from about Nov 16-20. Genkyū-en in Hikone itself peaks from about Nov 30, just after we leave; its evening light-up runs until Nov 29.",
}

SPOTS = {
    "osaka": [("Katsuo-ji, Minoh", "11/20", "12/8", "11月下旬～12月上旬"), ("Expo '70 Commemorative Park", "11/22", "12/11", "11月中旬～12月上旬"),
              ("Osaka Castle Park", "11/22", "12/12", ""), ("Minoo Park", "11/22", "12/7", "11月下旬～12月上旬")],
    "wakayama": [("Koyasan", "11/7", "11/16", "10月下旬～11月上旬"), ("Momijidani garden, Wakayama Castle", "11/30", "12/17", "12月上旬"),
                 ("Negoro-ji", "12/1", "12/12", "11月下旬～12月上旬")],
    "shirahama": [("Kozagawa gorge", "11/27", "12/7", "11月下旬～12月上旬"), ("Kumano Nachi Taisha", "11/28", "12/8", "")],
    "kyoto": [("Enryaku-ji, Mount Hiei", "11/9", "11/23", "11月上旬～11月中旬"), ("Ōhara Sanzen-in", "11/20", "12/8", "11月下旬～12月上旬"),
              ("Jōjakkō-ji", "11/25", "12/12", "11月下旬～12月上旬"), ("Hiyoshi Taisha, Sakamoto", "11/25", "12/8", "11月下旬～12月上旬"),
              ("Enkōji", "11/24", "12/9", "11月下旬～12月上旬"), ("Tōfuku-ji", "11/24", "12/11", "11月下旬～12月上旬"),
              ("Nanzen-ji", "11/25", "12/9", ""), ("Eikandō", "11/24", "12/6", "11月下旬～12月上旬"),
              ("Arashiyama", "11/23", "12/9", "11/13～"), ("Kiyomizu-dera", "11/25", "12/10", "12月上旬"),
              ("Kyoto Gyoen ginkgo trees", "11/26", "12/6", ""), ("Byōdō-in, Uji", "11/25", "12/8", "11月下旬～12月上旬"),
              ("Uji River gorge", "11/25", "12/13", ""), ("Ryōan-ji", "11/28", "12/15", "12月上旬"),
              ("Kōshō-ji, Uji", "11/30", "12/9", "12月上旬"), ("Shimogamo Shrine", None, None, "12月上旬～12月中旬")],
    "nara": [("Murō-ji", "11/12", "11/27", "11月下旬～12月上旬"), ("Hase-dera", "11/20", "12/7", "11月上旬～11月下旬"),
             ("Chōgaku-ji", "11/25", "12/11", "12月上旬"), ("Nara Park", "11/20", "12/9", "10月下旬～12月上旬"),
             ("Shōryaku-ji", "11/25", "12/13", "11月中旬～12月上旬")],
    "shiga": [("Koto Sanzan (Hyakusai-ji)", "11/16", "12/6", "11月上旬～11月下旬"), ("Eigen-ji", "11/20", "12/8", "11月下旬～12月上旬"),
              ("Kyorinbo", "11/27", "12/11", ""), ("Genkyū-en, Hikone Castle", "11/30", "12/13", "12月上旬"),
              ("Keisokuji", None, None, "11月下旬～12月上旬")],
}
# The spots drawn in each tab's panel: a couple that show the area's overall timing.
SHOW = {
    "osaka": ["Osaka Castle Park", "Minoo Park"],
    "wakayama": ["Momijidani garden, Wakayama Castle", "Koyasan"],
    "shirahama": ["Kozagawa gorge"],
    "kyoto": ["Tōfuku-ji", "Arashiyama"],
    "nara": ["Nara Park", "Shōryaku-ji"],
    "shiga": ["Genkyū-en, Hikone Castle", "Keisokuji"],
}

# Shown on a card when its timing is very different from the rest of the area.
NOTES = {
    "wakayama": {"Koyasan": "Earlier than the city, up in the mountains: at its peak now, and leaves start falling around Nov 16 (Weathernews). By Nov 20 it will be past its best."},
    "kyoto": {
        "Mount Hiei": "Earlier than the city: at its peak now, and leaves start falling around Nov 23 (Weathernews). Only worth it on the first day or two of the first stay.",
        "Kōshō-ji": "Later than most of Kyoto: peak from about Nov 30 (Weathernews), early December on tenki.jp. Best in the second stay.",
        "Shimogamo Shrine": "One of the latest in Kyoto: tenki.jp expects the peak in early to mid December, so the second stay is better. Same for Tadasu-no-Mori, Kawai Shrine and the Mitsui Villa next to it.",
        "Kinkaku-ji": "A bit later than most: nearby Ryōan-ji peaks from about Nov 28 (Weathernews), early December on tenki.jp. Better in the second stay.",
    },
}

# Weathernews spot ids (weathernews.jp/koyo/spot/<id>/) and tenki.jp pages, for the next refresh.
WN_IDS = {"Tōfuku-ji": 26111, "Kiyomizu-dera": 26112, "Arashiyama": 26101, "Jōjakkō-ji": 26134, "Ryōan-ji": 26131, "Kyoto Gyoen ginkgo trees": 26140,
          "Ōhara Sanzen-in": 26103, "Nanzen-ji": 26105, "Enkōji": 26114, "Eikandō": 26120, "Byōdō-in, Uji": 26136, "Kōshō-ji, Uji": 26155,
          "Uji River gorge": 26173, "Koyasan": 26503, "Enryaku-ji, Mount Hiei": 26104, "Kyorinbo": 26021, "Koto Sanzan (Hyakusai-ji)": 26008,
          "Eigen-ji": 26001, "Hiyoshi Taisha, Sakamoto": 26003, "Genkyū-en, Hikone Castle": 26107, "Osaka Castle Park": 26207, "Minoo Park": 26202,
          "Katsuo-ji, Minoh": 26222, "Expo '70 Commemorative Park": 26205, "Kumano Nachi Taisha": 26513, "Kozagawa gorge": 26512,
          "Negoro-ji": 26504, "Momijidani garden, Wakayama Castle": 26514, "Nara Park": 26402, "Hase-dera": 26403, "Shōryaku-ji": 26410,
          "Chōgaku-ji": 26411, "Murō-ji": 26422}

CARDS = {
    "osaka": {"Osaka Castle": ("Osaka Castle Park", False)},
    "wakayama": {"Wakayama Castle": ("Momijidani garden, Wakayama Castle", False), "Koyasan": ("Koyasan", False)},
    "kyoto": {
        "Mount Hiei": ("Enryaku-ji, Mount Hiei", False),
        "Kurama Onsen": ("Ōhara Sanzen-in", "Ōhara, also in the northern hills"),
        "Jōjakkō-ji": ("Jōjakkō-ji", False),
        "Daihikaku Senkō-ji": ("Arashiyama", "Arashiyama"),
        "Arashiyama Yusai-Tei": ("Arashiyama", "Arashiyama"),
        "Togetsukyō Bridge": ("Arashiyama", "Arashiyama"),
        "Arashiyama Park Nakanoshima": ("Arashiyama", "Arashiyama"),
        "Seiryōji (Saga Shakadō)": ("Jōjakkō-ji", "Jōjakkō-ji nearby"),
        "Gohodo Benzaiten": ("Jōjakkō-ji", "Jōjakkō-ji nearby"),
        "Enrian": ("Jōjakkō-ji", "Jōjakkō-ji nearby"),
        "Former Chikurin-in": ("Hiyoshi Taisha, Sakamoto", "Hiyoshi Taisha next door"),
        "Enkōji": ("Enkōji", False),
        "Tōfuku-ji": ("Tōfuku-ji", False),
        "Nanzen-ji": ("Nanzen-ji", False),
        "Ginkaku-ji": ("Eikandō", "Eikandō, on the same hillside"),
        "Anraku-ji": ("Eikandō", "Eikandō, on the same hillside"),
        "Kiyomizu-dera": ("Kiyomizu-dera", False),
        "Honnō-ji": ("Kyoto Gyoen ginkgo trees", "the ginkgo trees at Kyoto Gyoen"),
        "Kinkaku-ji": ("Ryōan-ji", "Ryōan-ji nearby"),
        "Kōshō-ji": ("Kōshō-ji, Uji", False),
        "Ujikami Shrine": ("Byōdō-in, Uji", "Byōdō-in, across the river"),
        "Momiji-dani trail": ("Uji River gorge", "the Uji River gorge"),
        "Amagase Bridge": ("Uji River gorge", "the Uji River gorge"),
        "Shimogamo Shrine": ("Shimogamo Shrine", False),
        "Tadasu-no-Mori Forest": ("Shimogamo Shrine", "Shimogamo Shrine, in the same forest"),
        "Kawai Shrine": ("Shimogamo Shrine", "Shimogamo Shrine next door"),
        "Old Mitsui Family Villa": ("Shimogamo Shrine", "Shimogamo Shrine nearby"),
    },
    "nara": {"Kaminonegi-michi Trail": ("Nara Park", "Nara Park, right next to it")},
    "shiga": {"Hikone Castle": ("Genkyū-en, Hikone Castle", False), "Kyorinbo": ("Kyorinbo", False),
              "Keisokuji": ("Keisokuji", False), "Shakudoji": ("Keisokuji", "Keisokuji next door"),
              "Yoshirou Shrine": ("Keisokuji", "Keisokuji nearby"), "Kamisaki Shrine": ("Keisokuji", "Keisokuji nearby")},
}


def day(s):
    m, d = s.split("/")
    return _dt.date(YEAR, int(m), int(d))


def fmt(d):
    return f"{d.strftime('%b')} {d.day}"


def fmt_range(a, b):
    if a == b: return fmt(a)
    return f"{fmt(a)}-{b.day}" if a.month == b.month else f"{fmt(a)}-{fmt(b)}"


STAY_TITLE = {"nara": "Days we could go from"}   # legend wording for the shaded days, when "our stay" doesn't fit

_PART = {"上旬": ("early", 1, 10), "中旬": ("mid", 11, 20), "下旬": ("late", 21, None)}


def _last(m):
    return (_dt.date(YEAR, m % 12 + 1, 1) - _dt.timedelta(days=1)).day


def tenki_range(s):
    """tenki.jp's period ("11月下旬～12月上旬", "12月上旬", "11/13～") -> (first day, last day, English label), or None."""
    if not s or s.strip("-") == "": return None
    m = _re.fullmatch(r"(\d+)/(\d+)～", s)
    if m:   # a single start date ("from Nov 13"): drawn as ten days
        a = _dt.date(YEAR, int(m[1]), int(m[2]))
        return a, a + _dt.timedelta(days=9), f"from {fmt(a)}"
    parts = _re.findall(r"(\d+)月(上旬|中旬|下旬)", s)
    if not parts: return None
    (m1, p1), (m2, p2) = parts[0], parts[-1]
    a = _dt.date(YEAR, int(m1), _PART[p1][1])
    b = _dt.date(YEAR, int(m2), _PART[p2][2] or _last(int(m2)))
    mon = lambda mm: _dt.date(YEAR, int(mm), 1).strftime("%b")
    l1, l2 = f"{_PART[p1][0]} {mon(m1)}", f"{_PART[p2][0]} {mon(m2)}"
    return a, b, l1 if (m1, p1) == (m2, p2) else f"{l1}-{l2}"


def window(spot):
    """(peak, fall) used for the stay badges: Weathernews when there is one, else tenki.jp's period."""
    name, p, f, t = spot
    if p: return day(p), day(f)
    a, b, _ = tenki_range(t)
    return a, b + _dt.timedelta(days=1)


def status(peak, fall, a, b):
    """What the leaves look like during the days a..b (dates). Returns (css class, label)."""
    if b < peak: return "early", "still colouring"
    if a >= fall: return "late", "leaves falling"
    if peak > a: return "peak", f"peak from {fmt(peak)}"
    if fall <= b: return "peak", f"peak, falling from {fmt(fall)}"
    return "peak", "at peak"
